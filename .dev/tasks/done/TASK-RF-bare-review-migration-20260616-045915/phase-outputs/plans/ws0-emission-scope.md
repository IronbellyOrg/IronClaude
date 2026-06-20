# WS-0 Emission-Scope Decision (Step 2.7 → drives Step 2.9 e2e-flip)

**Status: Complete**
**Decided:** 2026-06-16 (Step 2.7)
**Authority:** observed from a real `swarm run --lens bare-review --transport stub`
on-disk artifact set (probe at `/tmp/ws0probe/out`), cross-checked against
`reduce_wave3` source (`reduce.py:686-722`).

## Decision

The WS-0-wired inline path emits, for `swarm run --lens bare-review --target X
--output Y --transport stub` (no `--resume`):

| Artifact | Emitted by WS-0? | Source |
|----------|------------------|--------|
| per-reviewer `bare-review-NN-<slug>.final.md` (normalized bodies) | **YES** | `normalize_wave2` writes each to `final_path` |
| per-reviewer `bare-review-NN-<slug>.meta.json` (sidecars) | **YES** | `normalize_wave2` `_emit_meta` |
| `return-contract.yaml` | **YES** | `reduce_wave3` → internal `emit_contract` (`reduce.py:722`) |
| `merged.md` | **YES** | `reduce_wave3` mode dispatch — bare-review's `amalgamation_mode` is `normalize+merge` (lens default via `_build_spec_from_lens`), and M=3 ≥ floor=2 |
| `done.json` (done sentinel) | **NO** | `reduce_wave3` does NOT write the done sentinel; that is a separate `on_completion.write_done_sentinel` step not wired on this inline path |
| `.swarm-state.json`, `execution-log.jsonl`, `execution-log.md`, `manifest.json` | YES (pre-existing) | unchanged from the prior stub path |

## Why `merged.md` IS emitted (not "absent")

The BUILD_REQUEST framed WS-0 scope as "contract + normalized bodies" and noted
`merged.md`/`done.json` "may legitimately remain absent." In practice the
bare-review lens carries `amalgamation_mode = "normalize+merge"` (hardcoded for
all lenses in `_build_spec_from_lens`, `commands.py:852`), and the WS-0 wiring
honors the spec's mode rather than overriding it to `"normalize"`. Under
`normalize+merge` with M≥floor, `reduce_wave3` writes `merged.md` (`reduce.py:686-689`).
Overriding the lens amalgamation_mode to suppress the merge was judged
out-of-scope for WS-0 (it would change lens behavior, not just wire the path).

**Consequence for Step 2.9:** `return-contract.yaml` AND `merged.md` are now
PRESENT; only `done.json` (`DONE_SENTINEL_FILENAME`) remains ABSENT. So the
absent-test (`test_quickstart_does_not_emit_m5_artifacts`) is narrowed to assert
only `DONE_SENTINEL_FILENAME` absent, and the presence of `RESULT_CONTRACT_FILENAME`
+ `MERGED_FILENAME` moves to the Step 2.8 presence test. The exact-artifact-set
test (`test_quickstart_lens_bare_review_emits_four_artifacts`) is also updated to
the new (superset) emission set — a necessary, gate-mandated deviation since WS-0
inverts the inline-path contract that test pinned.

**Phase-4 note (WS-B):** the legacy `t2_normalize.py` is a per-reviewer
normalizer (no merge), so the frozen golden (Step 4.1) carries per-reviewer
`.md` + `return-contract.yaml` but NO `merged.md`. The WS-B parity gate compares
the per-reviewer bodies + the contract (not `merged.md`), so the extra `merged.md`
does not break parity. IF the legacy golden's contract records
`amalgamation_mode: normalize` while the CLI records `normalize+merge`, that
contract-field divergence surfaces at the WS-B gate (Step 4.5) and is resolved
there.
