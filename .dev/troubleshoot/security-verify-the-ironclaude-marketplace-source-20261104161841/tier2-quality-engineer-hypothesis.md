# Hypothesis: the Tier 1 two-part fix is correct, but needs four edge-case constraints or it breaks existing tests and still trusts malformed entries

**Agent**: quality-engineer (lens), run by troubleshoot-analyst
**Tier**: 2
**Timestamp**: 2026-11-04T16:27:17Z (parent receipt time)
**Cause class**: Security
**Claim class**: `static_defect`
**Evidence class**: `source_static`
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned
runs-in=src/superclaude/cli/install_user_setup.py:332 @ local superclaude install/update process (throwaway HOME, fake claude CLI)

## Claim

Agree with D1 and D2. The fix holds only with: (a) a source check that tolerates any entry shape without raising and accepts only an absolute directory path resolving to home/_CATALOG_DIR, run only inside the pinned block; (b) commands keyed by marketplace name, not report label; (c) time-limit check before the skip-dependents check; (d) marketplace success judged by exit code alone, no re-read of known_marketplaces.json.

## Evidence

| # | Kind | Source | Content |
|---|------|--------|---------|
| E1 | source_citation | install_user_setup.py:266-271, 305, 332 | `_read_json` checks only the top-level dict; `known[name]` may be a string, list, null or lack `source` |
| E2 | source_citation | install_user_setup.py:343-346 | plugin market is `plugin.split("@")[1]` but the add is labelled `source["repo"]` |
| E3 | test_assertion | tests/cli/test_install_user_setup.py:362, :404, :390-393 | `_pinned_home` writes `{"ironclaude": {}}`; a strict check breaks move-pin and keep-pin tests unless the fixture changes |
| E4 | test_assertion | tests/cli/test_install_user_setup.py:450-457, :326-353, :230-233, :427-437 | time-limit labels; fresh-HOME fake CLI writes no known file; opt-out test; skip-already-installed entry `{}` |

behaviour-definition: row 1 (directory source shape, observed this run).

## Proposed Fix

Tier 1 fix plus constraints (a)-(d): `_is_our_catalog` true only for dict entry, dict source, `source == "directory"`, str absolute path resolving to home/_CATALOG_DIR; never raises; called only for catalog["name"]; on mismatch report `ironclaude (registered from another source; Ponytail not installed)`, drop pinned plugins, clear stale, write nothing. Commands `(report_name, market, args)`; `bad_markets` set on non-zero/raising marketplace add/update; time-limit first, then skip dependents reported as `<plugin> (marketplace <market> failed)`. Tests: fixture fix; refuse test over github/url/other-directory/relative/"x"/{}/non-dict source entries plus a symlinked-HOME accept case; skip-dependents test (add exits 1, update exits 1, add raises TimeoutExpired); all existing plugin tests unchanged.

## Confidence

Self-reported confidence: 0.85 (grounding 1.0, runtime 1.0, coverage 1.0, reproducibility 0.5: symlinked-HOME behaviour of claude not observed, fix directness 0.5, coherence 1.0).

## Risks

- "rerun to retry" wording is wrong for a foreign registration; needs its own wording.
- Dangling/looping symlink resolve → refused (fails closed).
- Generalizing the source check to all marketplaces would break skip-already-installed and reject user marketplaces.

## If I'm wrong, it's probably because...

Claude Code stores the path for a symlinked or ~-based HOME in a form resolve() does not reconcile.

## Falsification standard

After the fix `uv run pytest tests/cli/test_install_user_setup.py -k plugin` passes all named tests; a malformed entry must not raise.

## Evidence classification

static_defect; source_static (no tests run by the worker); AFFIRM.

## Alternatives considered

- Re-read known_marketplaces.json after add: rejected (breaks fake-CLI tests, no extra safety).
- Verify every marketplace's source: rejected (out of scope).

## Grounding gaps

- Symlinked-HOME stored path not observed; proposed tests not run.
