# Launch-level guard architecture analysis

Template: analysis section structure in ../../362/report-template.md.

## Scope and grounding
Command: `/sc:analyze src/superclaude/hooks/scripts/launch-level-guard.sh --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/g1/442/analyze`.

The target is the narrowest production file implementing issue 442's launch-level checks. Companion reads cover registration, observation tests, saved live results, the watcher gate and launcher refusal switch. No unrelated hook audit was attempted.

Codegraph: index_state=fresh, checked_at=2026-11-23T23:11:15Z; degraded: graph:empty.

Access: mcp. The fresh index does not index this shell script: files returned one JavaScript file in the containing directory, and node reported no indexed target. Read/Grep supplied evidence; no call graph is invented. Brief guard passed: the global command has Unattended mode and the project copy is absent.

## Architecture and metrics
One Bash hook runs at two lifecycle boundaries. Prompt submission binds a strict launch marker to a session, consumes the pending launch, and creates a no-replace release file on an accepted typed command. Tool interception classifies actions against the recorded level. Registration: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/hooks.json:63-69` and `:115-122`; binding/release: `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-guard.sh:318-378`.

The live inventory has 12 cases: nine hook-input observations, launch checks, level-restriction checks and process-context checks. All 12 remain unconditional skips at `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_launch_level_observations.py:79-110` despite merged observations. No coverage percentage, timing benchmark or certification is claimed. This text-layer guard is not isolation against hostile same-user code.

## Severity-rated findings
1. **High, acceptance gap:** completed live evidence is not reflected in the executable observation inventory. The 12-case `_PENDING` list and unconditional skip remain in `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/tests/hooks/test_launch_level_observations.py:79-110`; the same module couples the watcher gate to four pending cases at lines 82-105. Consequence: synthetic tests cannot establish the missing live acceptance, and automatic governed levels remain gated.
2. **High, still missing live boundary evidence:** `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issues/442/observation-results.md:545-550` records merge refusal passing but protected push still pending, because the model declined without calling the tool. Consequence: a refusal by the model cannot verify the protected-branch guard path. This is a test gap, not proof of a successful unauthorized push.
3. **Medium, known parked limitation:** the classifier requires both a Claude command word and a launch-flag word before adding ESCAPE (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/src/superclaude/hooks/scripts/launch-level-guard.sh:456-468`, `:510`). Item 8 records a child-session turn on a bare invocation (`/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issues/442/observation-results.md:263-316`). Issue 678 parks this finding and explicitly says the actual governed escape has not been observed. No exploit was attempted here; do not promote this inference to a verified governed bypass.

## Recommendations and roadmap
Reconcile the newer issue-691 live evidence into the results first, then finish protected-push and missing input-shape observations with the owner's go in a disposable environment. Replace completed skips with reviewed evidence checks, and retain checked reasons for genuinely unavailable cases. Keep both activation switches off until their separately reviewed acceptance conditions are met. This requires no guard refactor or new dependency; issue 678 remains separate parked work.

## Verification limits
Static quick-depth analysis only. No live sessions, installs, protected pushes, test-suite execution or external writes. Existing saved results were checked as records, not rerun; hook ordering, completeness of OB-H2 formal acceptance and universal authorization enforcement remain UNVERIFIED. Codegraph could not index the shell target, so graph caller/impact metrics are unavailable. The GitHub timeline is limited to the issue/comments and related PR merge metadata exposed by the allowed view/list commands. No unrelated performance or security audit is claimed.
