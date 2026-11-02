# Troubleshoot Report

**Target**: PR #349 Codex finding — docs/releases/v5.0.0.md migration step 2 tells upgraders to run `superclaude update`
**Type**: docs
**Tier reached**: 1
**Confidence**: 1.00
**Status**: partial
**Escalation reason**: none
**Test is wrong**: false
**Behavior is documented**: true
**Doc context card**: .dev/troubleshoot/docs-pr349-migration-step-2-update-20261102190100/doc-context.md
**Duration**: 1039
**Date**: 2026-11-02T19:18:19Z

---

## Summary

Status is partial only because the end-to-end measurement M1 is pending; the cause is established by code and passing tests. The 5.0.0 release notes send upgraders through `pipx install --force ...` then `superclaude update`, but `superclaude update` by design never runs the codegraph install phase or the codebase-memory/Serena retire step; only `superclaude install` (with or without `--force`) runs them, and `./update.sh` runs `superclaude install --force`. A user following the notes ends up with skills that expect codegraph, no codegraph registration and the old registrations still present, and the notes' step-4 check (`superclaude doctor` passes) cannot detect it. The fix is docs-only: point the upgrade at `superclaude install --force` and make step 4 check something that shows a missing codegraph.

## Documentation Context

- **Relevant refs**: .dev/releases/current/v5.0.0/DECISIONS.md, .dev/releases/current/v5.0.0/RELEASE-READINESS.md, docs/user-guide/mcp-installation.md, docs/reference/mcp-server-guide.md, docs/getting-started/installation.md, .dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md
- **Documented behavior**: `superclaude update` never touches MCP registrations; `superclaude install` (and so `./update.sh`) installs codegraph and runs the retire step (decision D7).
- **Restrictions honored**: main.py:407 and D7 stay unchanged (no code change); the notes keep migration notes for breaking changes (changelog_maintenance.md:180).
- **Restrictions overridden**: None
- **Card path**: .dev/troubleshoot/docs-pr349-migration-step-2-update-20261102190100/doc-context.md

## Diagnosability Context

**Verdict**: partial
**Complexity classification**: trivial
**Captured-bytes (failing run)**: n/a

Existing signals: update's phase banners, doctor's codegraph check, the legacy-entry notice.
Gap: after `superclaude update` with no codegraph, update says nothing about codegraph, plain `superclaude doctor` passes, and the session hook is silent; the "no codegraph registration" line prints only with `--verbose`.
Implication: the root cause is fully grounded in static code and pinned tests; the gap means the fixed notes must tell users to verify with a command whose output shows a missing codegraph.

(Full card: /home/coder/workspaces/worktrees/IronClaude/release-v5.0.0/.dev/troubleshoot/docs-pr349-migration-step-2-update-20261102190100/diagnosability-context.md)
(Tasklist (informational): /home/coder/workspaces/worktrees/IronClaude/release-v5.0.0/.dev/troubleshoot/docs-pr349-migration-step-2-update-20261102190100/diagnosability-tasklist.md)

## Diagnosis

**Root cause**: The release notes treat `superclaude update` as the full upgrade, but `update()` only refreshes framework files and never runs the codegraph phase or the retire step, which run only in `install()`.

**Cause class**: Build / packaging (a required install step missing from the documented upgrade path); the defect is in documentation, not code.

**Detailed explanation**: `update()` calls the framework installers and then, by the documented design (decision D7), leaves MCP registrations alone (Evidence 2, 3). `install()` runs the same installers and then `install_codegraph_mcp` and `run_retire_step` (Evidence 4), and `update.sh` uses `install --force` (Evidence 5), so the notes' claim that `./update.sh` "does the same" as the pipx + update pair is false. The repo's tests pin both behaviours (Evidence 7). Because doctor's codegraph check passes when codegraph is absent and hides its hint without `--verbose` (Evidence 6), the notes' step-4 verification also misses the gap.

## Evidence

1. `docs/releases/v5.0.0.md:147` — `superclaude update` (step 2); `:3` "Upgrade with superclaude update."; `:69` "An upgrade needs `superclaude update` (not a plain `superclaude install`)"; `:150` "From a clone, `./update.sh` does the same"; `:152` "`superclaude doctor` passes"
2. `src/superclaude/cli/main.py:407` — `# Read-only: update never touches MCP registrations.`
3. `src/superclaude/cli/main.py:365` — `core_success, core_message = install_core_files(force=True)` (update's installers run with force=True through :404; no codegraph or retire call)
4. `src/superclaude/cli/main.py:246` — `codegraph_success, codegraph_message = install_codegraph_mcp(scope="user")`; `:263` — `run_retire_step(codegraph_success and codegraph_ready()[0])` (inside `install()`)
5. `update.sh:8` — `superclaude install --force`
6. `src/superclaude/cli/doctor.py:164` — `details.append("no codegraph registration; run \`superclaude install\`")` (check stays passed, doctor.py:158); details print only with --verbose (`src/superclaude/cli/main.py:497`)
7. Command: `timeout 120 uv run pytest tests/cli/test_update_command.py -q -p no:cacheprovider -k codegraph` → "9 passed, 11 deselected in 0.46s" (includes `tests/cli/test_update_command.py:329` test_update_never_runs_the_codegraph_phase and `:318` test_install_force_is_not_forwarded_to_codegraph)
8. `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md:848` — D7: "`update.sh` and `superclaude update` unchanged ... `update.sh:8` already runs `install --force`; `update` is documented never to touch MCP state"
9. `docs/user-guide/mcp-installation.md:70` — "`superclaude update` keeps its existing framework behavior and never touches MCP registrations"

## Proposed Fix

**Files to change**:
- `docs/releases/v5.0.0.md` — :3 and :69 name `superclaude install --force` as the upgrade command; :143 adds that `superclaude update` skips the codegraph install and retire step; :147 becomes `superclaude install --force`; :150 stays (now true); :152 (step 4) checks `superclaude doctor --verbose` for no "no codegraph registration" line and `superclaude install --list` for a codegraph executable and "User registration: matches", and tells anyone who already ran `superclaude update` to run `superclaude install`; add a Known Issues line that `superclaude install --force` exits 1 if the codegraph phase fails (no network, unsupported platform).

**Files that MUST NOT change**:
- `src/superclaude/cli/main.py` (`update()`) — making update install MCP state regresses decision D7, main.py:407 and the pinned test tests/cli/test_update_command.py:329.

**Test to verify**:
- `tests/cli/test_update_command.py` (existing; unchanged) still passes; re-read the edited notes against main.py:242-267, :407 and update.sh:7-8.

**Apply with**: applied by the calling `/sc:pr-submit` run (fix authorized, docs-only edit in S3_FIXING).

## Risk + Rollback

- **Likelihood of regression**: low in docs/releases/v5.0.0.md (text only)
- **Test coverage of the changed code**: none needed for prose; the described behaviour is test-pinned
- **Rollback**: `git revert` the docs commit

## Follow-up tasks

- docs/getting-started/installation.md upgrade section (:329-333, :363, :365) has the same update-vs-install conflation. Suggested type: docs.
- .dev/releases/current/v5.0.0/DECISIONS.md decision 7.6 treats `superclaude update` and `./update.sh` as equivalent, and gate G7 (RELEASE-READINESS.md:198) runs only `./update.sh`, so it never tests the update path. Suggested type: docs.
- docs/user-guide/mcp-installation.md:71 "install --force reinstalls framework files only" reads as if codegraph is skipped. Suggested type: docs.
- Optional: make `superclaude doctor` (non-verbose) or `superclaude update` visibly warn when codegraph is unregistered (doctor.py:158-164). Suggested type: observability.

## Grounding Gaps

- MCP `auggie` tools were not available in this session; grounding used Read/Grep/Glob only (all Wave 1.5/1.6 branches degraded: true).
- codegraph not initialized for this worktree (graph:not_initialized); no graph lookups.
- Measurement M1 (end-to-end: a pre-codegraph install upgraded with the old step 2 leaves codegraph unregistered) is pending: needs a throwaway HOME; re-run permitted: unknown. The pinned tests cover update()'s control flow with stubbed installers.
- Calibration sensitivity: a strictly literal rubric cross-tab (doc_contract × source_static) would score Runtime check 0.5 → calibrated 0.80 → escalate; the calibrator used the test-assertion anchor given the captured test run.

## Next Steps

- Core M1: pending (needs a throwaway HOME; re-run permitted: unknown); predictions: claim-true "no codegraph registration; run `superclaude install`" / registration absent, claim-false a registered codegraph command; outcomes consistent / refuted / unobserved on empty or error.
- Apply the docs fix (the calling /sc:pr-submit run does this), then file the follow-up tasks above.

## Pipeline Hardening Closure

HC0: `pipeline_hardening_applicable=false` — boundary scan: the change is release-note prose only; no CLI/subprocess code, file/stdin/prompt delivery, generated-artifact parser, gate/severity/status enum, duplicated evaluator, persisted/resume state, review/audit selector or sibling pipeline is touched. pipeline_hardening_verdict: not_applicable.
