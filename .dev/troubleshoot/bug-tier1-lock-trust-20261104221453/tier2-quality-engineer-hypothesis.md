# Hypothesis: the trigger tests would all be skipped in CI (Python 3.10), and the step 5 pin has to check order inside step 5

**Agent**: quality-engineer (lens; worker troubleshoot-analyst)
**Tier**: 2
**Timestamp**: written by the parent on receipt (see audit.log)
**Cause class**: missing trust gate; test-design gap: CI runs only 3.10 (no TOML parser) and the order pins do not look inside step 5
**Claim class**: `mixed`
**Evidence class**: `runtime_repro` (parent probe, probe-lock-trust.out:6)
**Verdict direction**: `AFFIRM` (C3 and the Tier 1 fix; refines the test plan)
**Consistency with docs**: aligned with the owner decision (audit.log header); conflicts with the conflicts.py:11 docstring until tomllib is added
runs-in=tests/pr_submit/test_conflicts_core.py @ CI Python 3.10 (.github/workflows/test.yml:12, :22) and local 3.11.15
producer-citation-check: skipped — menu absent or empty (producers.md header-only)

## Claim
On 3.10 there is no tomllib, so every trigger test must skip there and CI (3.10 only) never runs them; only a 3.10-only test asserting "unreadable" covers the floor. Tests should reach the function as `c.lock_trust_findings` so a red run fails per test, not at collection. The order pins cover steps 1 and 10(a) only; a new pin must slice step 5 and check order inside it, which passes only when the gate sits between `--precheck` and `git checkout --ours`, i.e. inside the fenced block.

## Evidence
| # | Kind | Source | Content |
|---|---|---|---|
| E1 | source_citation | tests/pr_submit/test_conflicts_core.py:39, :41-58 | `from superclaude.pr_submit import conflicts as c`; top-level import list |
| E2 | test_assertion | tests/pr_submit/test_conflicts_core.py:2445, :2449-2468 | `_ALLOWED_STDLIB`; ast.walk sees imports inside try |
| E3 | test_assertion | tests/pr_submit/test_conflicts_core.py:2471-2479 | only bare-name calls banned; tomllib.loads passes |
| E4 | source_citation | .github/workflows/test.yml:12, :22 | Python "3.10" only |
| E5 | test_assertion | tests/pr_submit/test_conflict_sync_protocol.py:52-61, :94-111 | _assert_in_order uses first occurrence; order pins steps 1 and 10(a) |
| E6 | source_citation | src/superclaude/skills/sc-pr-submit-protocol/refs/conflict-mechanical.md:85-88, :92-94, :97 | fenced block precheck, checkout, uv lock; bullets after; Step 6 at :97 |
| E7 | source_citation | pyproject.toml:1-3 | hatchling, no dynamic/backend-path/sources: a real clean input |
| E8 | behaviour-definition | behaviour-definition: row 2, row 3 | path/editable not probed; tomllib 3.11+ only |

## Proposed Fix
Contract as in tier2-root-cause-analyst (fail closed on tomllib None, non-str, parse error, bad shapes; ordered findings; `backend-path` present including []; `project.dynamic` non-empty; sorted sources (path) then (editable)); tomllib bound in both branches. Tests via `c.lock_trust_findings`: skipif(<3.11): backend-path ["."] and []; dynamic ["version"]; dynamic []; path source inline and header; editable list of tables with markers inline and `[[...]]`; git/index/url sources -> []; repo pyproject -> []; all triggers ordered; malformed TOML (markers, duplicate key, unterminated header) -> unreadable; bad shapes -> unreadable. Every Python: tomllib monkeypatched None -> unreadable; None/bytes input -> unreadable. skipif(>=3.11): trigger and clean text -> unreadable (the CI 3.10 path). AST test for the guarded import. Add tomllib to `_ALLOWED_STDLIB`. Protocol pin: slice "**Step 5. Resolve.**" to "**Step 6", order ("--precheck", "lock_trust_findings", "git checkout --ours -- uv.lock", "uv lock --check") and "sync_tier3" present. Red run before the guard, saved to the run dir.

## Confidence
Self-reported 0.86 (calibrator re-grades).

## Risks
- CI never runs the trigger tests (local 3.11 only); a 3.11 CI job is out of scope.
- Workspace sources and direct path dependencies untested.

## If I'm wrong, it's probably because...
uv does not run the backend when `backend-path = []` (over-fires), or the owner wants bad shapes to raise.

## Falsification standard
The red run shows a collection error instead of per-test failures; the pin passes with the gate only in a bullet after the fence; the 3.10 test is skipped in CI.

## Alternatives considered
- tomli dev dependency: rejected (breaks stdlib-only and the allowlist).
- Presence-only MECHANICAL_PINS entry: rejected (does not prove order).
