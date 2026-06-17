# bare-review frozen golden — CLI-vs-golden parity reference

This tree is the **permanent** parity reference for
`tests/swarm/test_bare_review_parity.py`. It freezes the byte-exact per-reviewer
normalized markdown the legacy `t2_normalize.py` aggregator produced, so the
rebuilt parity gate can assert the live `superclaude swarm run --lens bare-review`
output against it **without needing the legacy script at run time** — the gate
survives WS-C's deletion of `t2_normalize.py`.

## Layout

```
golden/
  _review_target.py          # frozen review target; its sha256 == the golden target_checksum
  README.md                  # this file
  all-success/               # one dir per scenario
    bare-review-01-m.md      # normalized per-reviewer body (slot 1)
    bare-review-02-m.md
    bare-review-03-m.md
    return-contract.yaml     # legacy-schema contract (semantic reference)
  partial-with-timeout/      # slot 3 timed out -> no body (2 bodies)
  salvage-promoted/          # slot 3 parse_error promoted to success (3 bodies)
```

## How the golden is captured (and why it matches the live CLI)

`BareReviewV1.normalize` (the recipe the CLI runs) is a **byte-faithful port** of
legacy `t2_normalize` — so `legacy(args) == CLI-recipe(args)` for identical
`(raw body, args)`. The golden is therefore captured from the **real legacy
script** but with **CLI-aligned args** so the bytes equal what the live CLI emits:

| field | value | why |
|-------|-------|-----|
| `reviewer_model_id` / `reviewer_model_label` | `""` | the inline `run_cmd` path does not thread model identity into recipe_args |
| `caller_label` | `""` | empty unless `--label` is passed |
| `elapsed_ms` | `0` | stub transport |
| `target_checksum` | sha256 of `_review_target.py` | computed via the SAME `preflight._target_checksum` / `_truncate_target` the CLI uses |
| `generated` | `2026-06-01T17:59:55Z` | the one wall-clock field; pinned on both sides |

### Path normalization (portability)

The only non-portable field is the absolute target path. The golden stores it as
the sentinel `<<TARGET>>` (and any run-dir path as `<<OUTPUT_DIR>>`). The permanent
gate applies the **same** substitution to the live CLI body before byte
comparison — symmetric, so it can never mask a real divergence.

### Slot pairing

Golden files are 1-based `bare-review-NN-<slug>.md`; live CLI files are 0-based
`bare-review-NN-<slug>.final.md`. The gate pairs by **sorted body multiset**, not
filename (the stub serves `fixtures[counter % len]` in call order, so per-index
mapping is not guaranteed; the multiset comparison is order-independent).

### Contract

`return-contract.yaml` here is the **legacy flat schema** and is a *semantic*
reference only. The live CLI emits a different **nested** schema (`emit_contract`),
so the gate extracts and asserts specific fields (status, per-slot status set,
M/N counts, `suspect: true`, `recommended_next_command` containing
`/sc:adversarial --suspect-source`) against per-scenario expected values rather
than byte-comparing the whole contract.

## Regenerating the golden — DELIBERATE, HUMAN-APPROVED ONLY

Golden updates are **never auto-blessed** (consistent with the project's
"human-decision items must HALT" discipline). To re-bless after an intentional,
reviewed change to the normalizer/recipe:

```
SWARM_REGEN_GOLDEN=1 uv run pytest tests/swarm/test_bare_review_golden_regen.py -v
```

With `SWARM_REGEN_GOLDEN` unset (the CI default) the regen test SKIPS, so the
golden is never silently rewritten. The regen requires the legacy
`t2_normalize.py` to be present (pre-WS-C). **Post-deletion**, re-blessing must
drive the live CLI instead — a separate, explicitly human-approved step.

Editing `_review_target.py` changes its sha256 and therefore the golden
`target_checksum`; you MUST regenerate the golden afterward.
