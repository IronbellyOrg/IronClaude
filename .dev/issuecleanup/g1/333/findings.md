# Issue #333 review

Template: current Task brief's required findings fields.
Scope: read-only issue review; no source or GitHub changes.

## Verdict and evidence
**Verdict: still-relevant.** Issue #333 remains open and the reported absent-session-directory defect is still present at checkout commit `a7ae3dd30fcf88aaab655c37e94e58e121c2d863` (2026-11-23 review).

- `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:8` enables `set -euo pipefail`.
- The directory check at `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:65-69` still uses `[[ -d "$SESSION_DIR" ]] || return`. A missing directory makes the helper return status 1.
- The unconditional assignment at `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:136` propagates this failure before output starts at line 143.
- `tests/unit/test_crash_recovery_bootstrap.py:22-47` creates the session directory and tests only the present-directory case.
- The issue's single comment, dated 2026-11-17, reports the same root cause and an isolated reproduction (exit 1, empty stdout without a session folder; exit 0 with one log). This is historical reporter evidence, not a fresh runtime measurement.
- Historical migration PR #329 merged as `2f10a0e1e43bee841a4143235a92fc16171c9707`; it did not remove this failure. No repair PR was returned by the bounded all-state PR searches for `333` or `bootstrap_scan`.

## Real current state
The bootstrap scanner exists and the required architecture analysis was run on that single source file through the Skill tool. Its command report is `analyze/analyze-report.md`; its contract is `analyze/return-contract.yaml` and records worker_status succeeded, meaning the analysis was produced, not that the scanner is repaired.

The existing implementation emits `has_memory` and `memory_count` in the JSON at `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:153-154`, but missing session storage aborts before these fields can be emitted. The existing regression tests do not cover that condition. There is no observed partial repair of this root cause in the inspected checkout.

The issue's impact needs narrowing: `src/superclaude/skills/sc-crash-recovery/SKILL.md:58-79` consumes the inventory to choose investigators, but lines 134-145 explicitly continue git-state and claude-sessions on scanner failure and mark pipeline-artifacts/project-memory unscanned. The inventory is lost, not necessarily the entire crash-recovery operation. Large-folder exit 141 remains UNVERIFIED; bounded head pipelines exist at scanner lines 60-61 and 67-68, but this review did not reproduce SIGPIPE.

Local path history's latest scanner/test change is migration commit `2f10a0e1e`; earlier entries include `c1621ae66` (session-path correction), `263521c63` (hardcoded-path correction) and `edf7ffefd` (sprint state migration). Historical path corrections are not evidence of a fix for the current missing-directory return.

## Concrete next steps
1. Change the absent-session guard to explicit success (`return 0`) in the canonical scanner, without broadly ignoring unrelated failures.
2. Extend `tests/unit/test_crash_recovery_bootstrap.py` with a project whose isolated HOME has no encoded session directory. Assert zero exit, parseable JSON, empty recent_sessions, session_log_dir_exists false, and the memory fields. Keep the existing present-directory case; add an empty-directory case.
3. Exercise large session and pipeline-artifact sets under pipefail to determine whether exit 141 is a second failure. If reproduced, repair the early-closing pipelines and keep a regression; otherwise explicitly leave that historical symptom unverified rather than claiming it fixed.
4. Run focused tests and the component sync checks when implementing the repair. No repair, sync or source mutation was performed in this review.

## Complexity and size
**Complexity: simple. Size: S.** The confirmed repair is a one-token shell change plus a few subprocess regression cases in one existing test file; high-volume SIGPIPE verification adds bounded investigation, not an architectural rewrite.

## Priority
**P2.** Missing session history is a normal new-project condition and currently removes bootstrap evidence from recovery, but documented fallback investigators still run. No demonstrated security/data-loss event, deployment blocker or hard dependency on another active feature justifies P0/P1.

## Dependencies
**Needs: none identified. Blocks: none recorded in the issue view.** The fix can be made independently of #323 (completed migration) and #571 (cleanup plan). Full timeline and formal relationship history are UNVERIFIED with the permitted CLI surface; this is not a claim that no unmentioned dependent exists.

## Related issues
- **#323, Replace Codememory-mcp with CodeGraph: CLOSED.** Discovery context for the renamed memory fields, not a prerequisite to this fix.
- **#571, Release 6.0.0 cleanup plan: OPEN.** Its body mentions crash-recovery as a consumer of other retired components. The inspected mentions do not establish that crash-recovery itself is scheduled for removal; they do not support closing #333 as not-planned.
- No additional related issue was verified in this narrow review.

## Related PRs
- **#329, replace codebase-memory and Serena with codegraph: MERGED** on 2026-10-30, merge commit `2f10a0e1e43bee841a4143235a92fc16171c9707`. Read its body, comment and merge metadata; this migration references issue #323, not a repair for #333.
- The all-state searches `333` and `bootstrap_scan`, each limited to 50 results, returned zero PRs. Unmentioned PRs that use different wording are UNVERIFIED.
- A lookup of #323 as a PR failed because GitHub could not resolve that PR number; the subsequent issue lookup confirmed #323 is the migration issue, not a PR.

## Verification limits
- Source and test inspection was static. No new runtime reproduction or test run was performed; historical exit codes are attributed to the issue's own dated reports. Deployed copies and origin/master beyond this checkout are UNVERIFIED; no fetch was performed.
- Read the issue body, the one returned comment and the normal issue view. That view exposes state, project status and empty relationship headings, but not the full event timeline. Full timeline events and any PR links appearing only there are **UNVERIFIED**: the brief permits only gh issue view/list and gh pr view/list, not the API needed for a full timeline. No forbidden API/browser workaround was used.
- PR #329's initial file-list response was large and truncated by the tool. Only its body/comment/merge metadata, later re-requested in bounded form, support this report; no claim relies on inspecting its full changed-file list.
- Codegraph was fresh but returned no indexed shell file. Native Read/Grep was used instead; this limitation is recorded as graph:empty in the analysis.
- No GitHub write, stage, commit, push, source edit, install or independent artifact publication was performed. All deliverables are confined to this Task's report directory.
- All source citations are relative to `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup`; analysis and handoff paths are relative to this findings file's directory unless shown otherwise.
