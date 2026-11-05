# Hypothesis: The v5.0.0 upgrade steps treat `superclaude update` as the full upgrade, but `update` refreshes files only and never runs the codegraph phase or the retire step that only `superclaude install` runs.

**Agent**: root-cause-analyst (troubleshoot-analyst, read-only lens)
**Tier**: 1
**Timestamp**: 2026-11-02 (date only; worker did not observe the exact time)
**Cause class**: Build / packaging (an install step missing from the documented upgrade); fault in docs, not code
**Claim class**: `doc_contract`
**Evidence class**: `source_static` (plus parent-collected test run, see tier1-observation.md "Runtime evidence")
**Verdict direction**: `AFFIRM`
**Consistency with docs**: aligned (docs/user-guide/mcp-installation.md:64, :70; decision D7 at .dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md:848); disagrees only with the release-notes text under review and the installation guide
runs-in=src/superclaude/cli/main.py:340 @ the user's workstation shell
behaviour-definition: row 1

## Claim

Migration step 2 tells upgraders to run `pipx install --force ...` then `superclaude update`. `update()` calls the eight framework installers with `force=True` and stops; it never calls `install_codegraph_mcp` or `run_retire_step`, which run only inside `install()`. Following step 2 on a pre-codegraph install leaves fresh skills that expect codegraph, no codegraph registration, and Serena/codebase-memory registrations still in place. Line 150 says `./update.sh` "does the same", but it runs `superclaude install --force`. Step 4 (:152) cannot catch the gap: `superclaude doctor` passes when codegraph is not registered.

## Evidence

| # | Kind | Source | Content |
|---|------|--------|---------|
| E1 | source_citation | docs/releases/v5.0.0.md:3, :69, :143, :146-147, :150, :152 | ":3 Upgrade with superclaude update."; ":69 An upgrade needs `superclaude update` (not a plain `superclaude install`)"; ":147 superclaude update"; ":150 ./update.sh does the same"; ":152 superclaude doctor passes; superclaude install --list shows a codegraph block" |
| E2 | source_citation | src/superclaude/cli/main.py:365-404, :407, :242-263, :178-236 | update: 8 calls with force=True, then "# Read-only: update never touches MCP registrations." (:407); install: same 8 calls with force=force (:178-236), then install_codegraph_mcp(scope="user") (:246) and run_retire_step(...) (:263) |
| E3 | source_citation | update.sh:7-8 | `pipx install --force ./` then `superclaude install --force` |
| E4 | source_citation | src/superclaude/cli/doctor.py:158, :163-164; src/superclaude/cli/main.py:495-497; src/superclaude/cli/install_mcp.py:1082-1083, :1093-1099 | passed=True; missing registration only adds a detail shown under --verbose; install --list always prints the codegraph block, even with "User registration: absent" |
| E5 | test_assertion | tests/cli/test_update_command.py:329-333 (test_update_never_runs_the_codegraph_phase), :318-326 (test_install_force_is_not_forwarded_to_codegraph) | `assert "install_codegraph_mcp" not in calls`; install --force calls the phase with {"scope": "user"}. Parent ran them: 9 passed (tier1-observation.md, Runtime evidence) |

Producer-citation check: skipped — producers.md producer-count: 0 (documentation-text observation).

## Proposed Fix

Docs-only, docs/releases/v5.0.0.md:
- :3 → "Upgrade with `pipx install --force` and then `superclaude install --force`."
- :69 → "needs `superclaude install --force` (a plain `superclaude install` does not refresh existing files, and `superclaude update` skips the codegraph install and the retire step)".
- :143 → add "`superclaude update` refreshes files but never installs codegraph or retires old MCP registrations, so it is not enough for this release."
- :147 → `superclaude install --force`.
- :150 → "does the same" becomes true; optionally note it also runs `make sync-dev` and `superclaude doctor`.
- :152 (step 4) → `superclaude doctor --verbose` shows no "no codegraph registration" line; `superclaude install --list` codegraph block shows an Executable path and "User registration: matches"; add "If you already upgraded with `superclaude update`, run `superclaude install` now."
- :227/:229 reference step 2; no change needed once step 2 is fixed.
Verification: re-read edited notes against main.py:242-267, :407 and update.sh:7-8. M1 pending.

## Confidence

Self-reported: 0.92 (Evidence grounding 1.0; Runtime check 0.5 by the worker, before the parent's test run; Symptom coverage 1.0; Reproducibility fit 1.0; Fix directness 1.0; Domain coherence 1.0)

## Risks

- `install --force` exits 1 when the codegraph phase fails (main.py:278-280), e.g. unsupported platform or no network; add a Known Issues line.
- docs/user-guide/mcp-installation.md:71 ("install --force reinstalls framework files only") may mislead; out of scope here.
- Unverified whether `/sc:graph status` in step 4 reports an index state when codegraph is unregistered.

## If I'm wrong, it's probably because...

Maintainers intended `update` to gain the codegraph and retire phases before release; D7 and main.py:407 argue against it.

## Falsification standard

Wrong if, in a throwaway HOME with a pre-codegraph install, `superclaude update` then `superclaude install --list` prints a codegraph "User registration:" other than "absent", or if test_update_never_runs_the_codegraph_phase fails.

## Evidence classification

- Claim class: doc_contract. Evidence class: source_static (+ parent test run).
- Runtime check performed by worker: no (no shell). Parent ran the pinning tests.
- test_is_wrong: no. behavior_is_documented: yes for the code (update's behaviour is the documented design); the release notes deviate from it, so the remediation target is docs.

## Alternatives considered

- Make `update` run the codegraph and retire phases: rejected (breaks D7, main.py:407, docs and a pinned test; finding scope is docs).
- Change only :147: rejected (:3, :69, :150 still contradict; step 4 still passes after an incomplete upgrade).

## Related sites, same cause, outside this finding

docs/getting-started/installation.md:56, :329, :333, :363, :365; .dev/releases/current/v5.0.0/DECISIONS.md:7 (7.6); RELEASE-READINESS.md:13, :180, :227; docs/user-guide/mcp-installation.md:71; gate G7 (RELEASE-READINESS.md:198) never tests the `update` path.
