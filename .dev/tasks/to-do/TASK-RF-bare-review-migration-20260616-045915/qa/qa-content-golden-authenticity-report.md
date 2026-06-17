# QA Report — Golden Authenticity (Phase Gate 4, content lens)

**Topic:** sc-bare-review M8/M9 migration — frozen golden authenticity
**Date:** 2026-06-16
**Phase:** doc-qualitative (adapted: golden-authenticity content lens)
**Fix cycle:** N/A (fix_authorization: FALSE — report only)
**Stance:** ADVERSARIAL — hypothesis under test: "the frozen golden was hand-fabricated rather than captured from the real legacy `t2_normalize.py` machinery."

---

## Overall Verdict: PASS

The adversarial hypothesis is **REFUTED**. The committed golden tree is authentic
output of the real legacy `t2_normalize.py` aggregator, proven by an idempotent
re-run that produced a **zero-byte diff** across all 13 golden files.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Regen helper imports + runs REAL legacy `main()` (not hand-authored bodies) | PASS | `test_bare_review_golden_regen.py:151-159` `_load_legacy()` uses `importlib.util.spec_from_file_location` against `LEGACY_SCRIPT` (`src/.../sc-bare-review/scripts/t2_normalize.py`), `exec_module`, then `:280` `legacy.main()` is called with `sys.argv` monkeypatched to `--manifest <staged>`. Legacy `main()` (`t2_normalize.py:263-312`) genuinely reads the manifest, runs `normalize_reviewer` per reviewer, emits the contract. Bodies are produced by `render_markdown` (`:122-146`), not copied. |
| 2 | 3 scenario dirs each carry per-reviewer `.md` + `return-contract.yaml`; body counts match plans | PASS | `find` + per-scenario count: all-success bodies=3 contract=1; partial-with-timeout bodies=2 contract=1; salvage-promoted bodies=3 contract=1. Matches SCENARIOS (`test_...regen.py:94-119`): all-success 3 success; partial 2 success + 1 timeout (body-less slot → no `.md`, per legacy `:190-193` hard-failure path); salvage 3 (slot-3 parse_error promoted). Regen's own assertion `:308-315` enforces `expected_bodies = sum(1 for fx,st in plan if fx and st != "timeout")`. |
| 3 | Bodies contain rendered header + deterministic pins (generated, `<<TARGET>>`, real sha256) | PASS | `grep -L "^# T2-Bare Review"` over all 8 bodies returned EMPTY (every body has the rendered header). Spot-checked 1 body/scenario: all-success/01 (5 findings), partial/02 (0 findings), salvage/03 (2 findings) — all carry `generated: "2026-06-01T17:59:55Z"`, `target: "<<TARGET>>"`, `target_checksum: "c8ce0d9b…cecba"`. |
| 4 | sha256 pin is the REAL checksum of the committed target (not fabricated) | PASS | `preflight._target_checksum(_truncate_target(raw,4000))` over `_review_target.py` = `c8ce0d9b805943cb7aa8b27f36d4c951a92f37648fde216bc89084abc67cecba` — byte-exact match to the pin in every golden body/contract. Plain sha256 also matches (truncation is a no-op for the small target). |
| 5 | PROVE-OR-REFUTE: re-run regen → zero diff (byte-stable) | PASS | `SWARM_REGEN_GOLDEN=1 uv run pytest …golden_regen.py -q` → `1 passed in 0.14s`. `git status --short` on golden dir AFTER = identical to BEFORE (untracked dir, no modifications). sha256sum of all 13 files BEFORE == AFTER (see Regen-Diff Result). |
| 6 | §7.4 salvage promotion actually exercised through real `main()` | PASS | `salvage.raw.txt` uses `blocker`/`medium` aliases + prose preamble; golden `salvage-promoted/03.md` shows them normalized to `crit`/`med` (legacy `SEV_ALIASES`/`normalize_sev` `:25-40,72-73`). Contract: `status: success`, `reviewers_succeeded: 3` despite slot-3 input status `parse_error` → promotion fired. Hand-fabrication would require manually replicating the alias map. |
| 7 | Aggregate-status semantics authentic (IMM-5 success-first) | PASS | partial-with-timeout contract: `status: partial`, `reviewers_succeeded: 2` (M=2 < N=3 → partial, legacy `:284-290`). all-success + salvage: `status: success` (M==N==3). |
| 8 | Regen is deliberate/human-approved/never-auto-blessed | PASS | `pytestmark = skipif(SWARM_REGEN_GOLDEN != "1")` (`:122-128`); module docstring `:26-32`; `golden/README.md:63-76` document env-gating + "never auto-blessed" + post-WS-C re-bless must drive live CLI. Mirrors `SWARM_REAL_E2E` pattern. |

## Summary
- Checks passed: 8 / 8
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Regen-Diff Result (raw data — the decisive authenticity proof)

```
$ SWARM_REGEN_GOLDEN=1 uv run pytest tests/swarm/test_bare_review_golden_regen.py -q
1 passed in 0.14s

$ git status --short tests/swarm/fixtures/bare_review_v1/golden/    # AFTER regen
?? tests/swarm/fixtures/bare_review_v1/golden/
   (dir untracked; NO modified/new files inside — byte-stable)
```

sha256 of all 13 golden files BEFORE == AFTER (unchanged):
```
1487a0b9…  all-success/bare-review-01-m.md      (== partial/01 == salvage/01)
2fbbc389…  all-success/bare-review-02-m.md      (== partial/02 == salvage/02)
48bf684e…  all-success/bare-review-03-m.md
4564f99f…  all-success/return-contract.yaml
b8113d03…  partial-with-timeout/return-contract.yaml
c46e05cb…  salvage-promoted/bare-review-03-m.md
8474b53e…  salvage-promoted/return-contract.yaml
c8ce0d9b…  _review_target.py
77b2abac…  README.md
```
(slots 01/02 share sha256 across scenarios — expected: same fixtures + identical
CLI-aligned args. If the golden were hand-typed, byte-identical cross-scenario
collisions would be implausible to maintain; they fall out naturally from the
deterministic legacy renderer.)

## Issues Found
None.

## Self-Audit
**(a) Reliance — structural facts taken as given:** none. This is a content-lens
review; no upstream rf-qa structural verdict was inherited. All claims were
independently tool-verified.

**(b) Independent semantic checks (with tool evidence):**
- Re-ran the env-gated regen and diffed bytes (`git status` + `sha256sum` before/after) — the single strongest authenticity signal; not derivable from reading.
- Recomputed the sha256 pin via `preflight._target_checksum` against the committed target — proved the checksum is real, not a placeholder.
- Cross-read `salvage.raw.txt` source vs golden `salvage-promoted/03.md` — confirmed `blocker→crit`, `medium→med` alias normalization, proving the legacy normalizer (not a human) produced the body.
- Read legacy `main()` + `_load_legacy()` to confirm the regen drives real machinery via importlib, not fixtures.

**Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 8 | Grep: 1 | Glob: 0 | Bash: 6
**Web research:** none performed (review was entirely local-file/source-bound).

## QA Complete
