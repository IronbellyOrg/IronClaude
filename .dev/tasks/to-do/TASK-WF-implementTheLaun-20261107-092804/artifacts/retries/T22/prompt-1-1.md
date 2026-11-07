c3ed6e792050896f66c62b4b57c965eb7909edf1
Review one task for spec compliance.

Task brief: ## Task 22: Update the design status, claim documentation and ship-gate text, then run the full checks

Depends on: Task 20, Task 21, Task 17, Task 15

Update docs/designs/sc-issue-launch-level-hook.md: the status and planning_status lines and section 19 text that say the claim code does not implement the pipeline interface or that the L1 guard is not built (finding F6) now state what exists (guard script, registrations, installer entry, IR-4 to IR-7 detection) and what is still pending (OB-H1, OB-H2, OB-H3, OB-CTX, L2); keep the owner decisions and the historical review sections untouched. Update the places that describe W-ENFORCEMENT-ABSENT as a warning (src/superclaude/skills/sc-issue-protocol/SKILL.md, src/superclaude/skills/sc-issue-protocol/refs/claim.md, src/superclaude/commands/issue.md, docs/user-guide/commands.md and docs/designs/sc-issue-claim-pipeline-flag.md; the last one also states that IR-3 stays documentation only because no code writes pipeline.json) so they describe the refusal when the guard is missing or not effective, the W-L2-ABSENT warning (the launch continues and the L2 layer is not built yet), and the rule that no governed claim is used on a real issue until OB-H1 item 1 shows the parent session_id in subagent payloads, OB-H2 passes and OB-H3 passes (the U1 ship gate of design section 7). State in the design document, in one sentence, that pending launch records are not pruned (owner decision O-15). Run make sync-dev and make verify-sync, and update any plugin or mirror copy that a mirror test requires to stay byte-identical.

Acceptance criteria:
- grep for "does not implement this proposed pipeline interface" in docs/designs/sc-issue-launch-level-hook.md returns no match, and the status line names what is built and what is pending.
- grep of the five documents for W-ENFORCEMENT-ABSENT shows wording that describes a refusal, not a warning that lets the launch continue, and grep for W-L2-ABSENT shows wording that describes a warning.
- uv run pytest tests/hooks/ tests/cli/test_install_hooks.py tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py -v passes with the only skips being the pending observation tests of tests/hooks/test_launch_level_observations.py, the hook-order observation of Task 14, and the existing environment skips (non-Linux, running as root, the opt-in live probe).
- make verify-sync exits 0 and make lint exits 0.
- ./artifacts/final-check.md records the exact commands run, the pass and skip counts, and the list of pending observations (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX) with the statement that none has been run.

AC ids (source order):
T22.AC1: grep for "does not implement this proposed pipeline interface" in docs/designs/sc-issue-launch-level-hook.md returns no match, and the status line names what is built and what is pending.
T22.AC2: grep of the five documents for W-ENFORCEMENT-ABSENT shows wording that describes a refusal, not a warning that lets the launch continue, and grep for W-L2-ABSENT shows wording that describes a warning.
T22.AC3: uv run pytest tests/hooks/ tests/cli/test_install_hooks.py tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py -v passes with the only skips being the pending observation tests of tests/hooks/test_launch_level_observations.py, the hook-order observation of Task 14, and the existing environment skips (non-Linux, running as root, the opt-in live probe).
T22.AC4: make verify-sync exits 0 and make lint exits 0.
T22.AC5: ./artifacts/final-check.md records the exact commands run, the pass and skip counts, and the list of pending observations (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX) with the statement that none has been run.
Global constraints: - docs/designs/sc-issue-launch-level-hook.md is the authority for this plan. The requirements file .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md (called MR below) is the historical baseline for requirement ids and the test corpus; where the design says it overrides MR (design section 11, DD-2), the design wins. .dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md defines the claim side; the hook interface rules IR-1 to IR-7 in design section 13 win over it.
- This branch builds on open PR 425 (ironbelly/sc-issue-claim-pipeline-flag). The claim code in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py already writes the launch record and marks the prompt (IR-1, IR-2); do not rebuild that.
- The L1 guard is one flat bash script using only bash, jq, sed and tr: exit 0 allows, exit 2 blocks, no onFailure, no Python, no git or network call on ordinary classification. No new runtime service, managed settings deployment, shell parser, hook forwarding framework or git config migration (design section 1).
- Do not change src/superclaude/hooks/scripts/launch-job-identity.sh or tests/hooks/test_launch_job_identity.py. A conflict found with it goes into the record of Task 14, not into that file.
- Ordinary sessions are never blocked by any failure (FR-L-53). Only a positively identified governed session fails closed.
- Live observations (OB-H1, OB-H2, OB-H3, OB-CTX) need real governed sessions or real launches. This plan runs none of them and never launches a governed agent on a real issue or pushes to a real protected branch. They stay pending (a skipped test with a stated reason), never reported as passed. Tests use a temporary HOME and temporary bare remotes.
- Acceptance claims cover the routes the tests exercise. Nothing here claims universal merge protection or defence against a hostile agent (design sections 1 and 12).
- Gate: Task 1 writes the B-CTX verdict. If ./artifacts/b-ctx-verdict.md contains the line "L1: STOP", stop the run at Task 1 and report that verdict; do not start Task 2 or any later task. Every task after Task 1 depends on that verdict.
- Existing tests: any task that changes a check in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py also migrates the shared test fixture launch_scene in tests/skills/test_issue_orca_worktree.py (it writes only a bare shell stub today) and names every test whose result changes. Test code must unset CLAUDE_CONFIG_DIR and control which jq is on PATH, so results do not depend on the developer's machine.
- Edit only under src/superclaude/, plugins/superclaude/hooks/, tests/, docs/ and this package's ./artifacts/; run make sync-dev after hook or skill edits. The plugin copy of every hook script and hooks.json stays byte-identical to its src copy. Generated .claude/ mirrors made by make sync-dev stay out of the commit.
- UV only: run tests with uv run pytest.
- Findings of the issue analysis that this plan answers: F2 (Task 15), F3 (Task 14), F4 (Tasks 18 to 20), F6 (Task 22), F7 (Task 1). F5 (pending records are not pruned) is accepted under owner decision O-15 and is stated in Task 22.
Start sha: c3ed6e792050896f66c62b4b57c965eb7909edf1
Diff against the start snapshot: diff --git a/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/final-check.md b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/final-check.md
new file mode 100644
index 00000000..4c987ea4
--- /dev/null
+++ b/.dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/artifacts/final-check.md
@@ -0,0 +1,57 @@
+# Final check (Task 22, issue #394)
+
+Run on 2026-11-07 in the worktree `issue-394-launch-level-hook`, after the Task 22 document edits.
+
+## Commands run
+
+| Command | Exit code | Result |
+|---|---|---|
+| `make sync-dev` | 0 | mirrors regenerated (generated `.claude/` copies stay out of any commit) |
+| `make verify-sync` | 0 | "All components in sync." |
+| `make lint` | 0 | architecture policy: PASS with 5 warnings (pre-existing); `uv run ruff check .`: "All checks passed!" |
+| `uv run pytest tests/hooks/ tests/cli/test_install_hooks.py tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py tests/skills/test_worker_contract.py -v -rs` | 0 | **5093 passed, 12 skipped** in 398.71 s (log: `/tmp/impl-20261107/t22-full.log`) |
+| `uv run pytest tests/commands/test_issue_command.py tests/cli/test_issue_body_templates.py tests/skills/test_issue_worker_agents.py -q` | 0 | 93 passed (other tests that read the edited `issue.md`) |
+| `cmp src/superclaude/hooks/scripts/launch-level-guard.sh plugins/superclaude/hooks/scripts/launch-level-guard.sh` | 0 | identical; the src script was not changed in Task 22, so it was not re-copied |
+| `grep -c 'does not implement this proposed pipeline interface' docs/designs/sc-issue-launch-level-hook.md` | 1 (no match) | count 0 |
+
+## Skips (12)
+
+Every skip is a pending live observation of `tests/hooks/test_launch_level_observations.py:84`, reason "needs a real governed session and has not been run":
+
+| Skipped test | Reason class |
+|---|---|
+| OB-H1 item 1 to OB-H1 item 9 (9 tests) | pending observation |
+| OB-H2 | pending observation |
+| OB-H3 | pending observation |
+| OB-CTX | pending observation |
+
+No other skip occurred. The hook-order observation of Task 14 did not skip (its file runs on Linux; the open hook-order question is recorded in `hook-order.md` and belongs to OB-H3). The environment skips (non-Linux, running as root, the opt-in live probe) did not fire on this Linux, non-root host.
+
+## Pending observations (none has been run)
+
+OB-H1 items 1, 2, 3, 4, 5, 6, 7, 8 and 9; OB-H2; OB-H3; OB-CTX. None of them has been run. The L2 pre-push layer is not built (`l2-disposition.md`). Ship gate: no governed claim is used on a real issue until OB-H1 item 1 shows the parent `session_id` in subagent payloads, OB-H2 passes and OB-H3 passes (design section 7, U1).
+
+## Acceptance criteria of Task 22
+
+- The design status line names what is built (L1 guard, registrations, installer entry, claim IR-1 to IR-7 detection) and what is pending (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX, L2); the removed phrase has no match; section 19.8 holds the O-15 sentence; section 5.1 NM1a has the `LL_RE_NM1A` note.
+- `W-ENFORCEMENT-ABSENT` is described as a refusal (no agent, no launch record) and `W-L2-ABSENT` as a warning (the launch continues; L2 not built) in `SKILL.md`, `refs/claim.md`, `commands/issue.md`, `docs/user-guide/commands.md` and `docs/designs/sc-issue-claim-pipeline-flag.md`; each states the ship-gate rule; the last also states that IR-3 stays documentation only because no code writes `pipeline.json`.
+- The full test command passed with only the 12 pending-observation skips; `make verify-sync` and `make lint` exited 0.
+
+## Known limits and findings to carry into the pull request
+
+1. **Raw bound-id scan (Task 5):** on a broken JSON payload, the failure-path scan for a bound session id can block an ordinary session whose broken JSON contains a bound id nested inside it. The scan cost grows with the number of `session_id` strings (500 ids: 0.37 s).
+2. **NM1a design text (Task 6):** the printed design test never matched; the script holds the pattern in `LL_RE_NM1A`, and section 5.1 now carries a note saying so.
+3. **Git wrapper gaps (Task 7):** a git subcommand of the UNKNOWN class passes when a wrapper option takes a value (`env -u X git ci`, `timeout -s KILL 30 git ci`) or an assignment holds a space (`A="x y" git ci`). Commit, push and merge are still caught (G1); design G3 does not require more.
+4. **gh and curl gaps (Task 8):** a `curl` write passes when any word in the segment has basename `gh`; some `gh api` GET spellings of merge endpoints (trailing slash, `//graphql`, percent-encoding) are allowed. Rule H2 over-blocks reads containing `?`, `{`, `}`, `$` or quotes, and `gh pr create` with `--repo` on a continuation line is LL-REPO at FS.
+5. **Escape and tamper gaps (Task 9):** `orca terminal send` can pass when the segment ends in `-h` through a comment, here-string or quotes. Allowed tamper spellings include `cd ~/.claude/. && rm -rf state`, `cat ~/.claude/x/../settings.json` and `uvx superclaude@latest install`; byobu and zellij are not escape words, and `claude --print=x` is not an escape flag.
+6. **hooks.json files differ (Task 12):** the plugin `hooks.json` is a subset of the src one, not byte-identical. The test pins only that both hold the same two guard entries.
+7. **Installer order (Task 13):** `_merge_settings` now inserts a missing managed entry before the first entry owned by a later `hooks.json` entry, so an upgrade keeps `launch-job-identity` last. Fresh install and re-install behave as before.
+8. **Degraded level word (Task 14, decided open point):** the guard treats `degraded` as worktree with an LL-STATE note, but the pre-existing `launch-job-identity.sh` rejects it (exit 2 on every governed Bash call), so a degraded session cannot run Bash. A fix (add `degraded` to that hook's levels) needs a separate change.
+9. **Hook composition (Task 14):** if Claude Code gave the guard the identity hook's rewritten command (which names `~/.claude/hooks/launch-job-identity.sh`), the guard would block it as LL-TAMPER at every level. The real hook order and `updatedInput` handling are unobserved; this belongs in OB-H3.
+10. **Identity hook cost (Task 15):** `launch-job-identity.sh` costs a 79 ms median on ordinary Bash calls when the store holds only `pending/` (2 ms with no store). The worst T-SPD-5 run took 870 ms of its 1 s limit, so the speed test may flake on slow hosts.
+11. **Corpus and design ambiguities (Task 16):** corpus ids are `NATK-n`, not `N-ATK-n`; N-ATK-36 cites R17, not R1/R3/R11. An unknown event under a bound id gives LL-BROKEN; OK-33 expects LL-REPO at FS (design H4 over MR).
+12. **Unasserted attacks (Task 17):** T-ATK-54, 57 and 59 have no per-level assertion.
+13. **Preflight scope (Task 18):** the IR-4 preflight reads the claim process only (HOME, PATH, environment, user and worktree project settings). It does not check enterprise-managed settings, string forms of `disableAllHooks` or plain-word matcher semantics.
+14. **Release line (Task 19):** the release instruction uses a `<session id>` placeholder because the claim cannot know the id; the L2 `absent` line is also shown when git fails; the printed `rm` line breaks for a HOME containing a quote or `$`.
+15. **L2 disposition (Task 21):** the section 19.2 bullet of `l2-disposition.md` omits the design condition "publication/self-test succeeds".
+16. **IR-7 is a warning (decided open point):** the design asks for a refusal when L2 is absent; the claim only warns with `W-L2-ABSENT` because no L2 layer exists. The owner was asked and has not answered (`ir7-consequence.md`).
diff --git a/docs/designs/sc-issue-claim-pipeline-flag.md b/docs/designs/sc-issue-claim-pipeline-flag.md
index 7b6c1a51..2cb653fb 100644
--- a/docs/designs/sc-issue-claim-pipeline-flag.md
+++ b/docs/designs/sc-issue-claim-pipeline-flag.md
@@ -1,6 +1,7 @@
 # Design: `/sc:issue --claim --pipeline` (worktree, launch levels, `--submit`)
 
 **Status:** Design only (nothing implemented). Next: `/sc:workflow docs/designs/sc-issue-claim-pipeline-flag.md --depth quick --handoff none`, then `/sc:implement` on the plan it prints.
+**Update (issue #394):** the launch-level guard now exists and default D3 is replaced. When the guard is missing or not effective (`enforcement_preflight()`, hook IR-4) the claim refuses the launch with `W-ENFORCEMENT-ABSENT`: no agent starts and no launch record is written. When the worktree has no L2 pre-push layer the claim warns with `W-L2-ABSENT` and the launch continues, because the L2 layer is not built yet (hook IR-7, taken as a warning). IR-3 stays documentation only because no code writes `pipeline.json`. No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 shows the parent `session_id` in subagent payloads, OB-H2 passes and OB-H3 passes (the U1 ship gate of `docs/designs/sc-issue-launch-level-hook.md` section 7). Sections below that describe `W-ENFORCEMENT-ABSENT` carry this update.
 **Issue:** none. This feature had no tracking issue. Related follow-on: IronbellyOrg/IronClaude #394 (launch-level enforcement hook, `docs/designs/sc-issue-launch-level-hook.md`). Launch rule from #412 (merged).
 **Branch:** `ironbelly/sc-issue-claim-pipeline-flag`
 **Source requirements:** `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/merged-requirements.md` ("MR") as amended by `launch-levels-addendum.md` in the same folder ("AD", revision 2, after the owner's four corrections of 2026-11-05). Where MR and AD differ, AD wins. Where AD and the hook design differ on hook state, the hook design wins (section 3).
@@ -54,7 +55,7 @@ No level merges anything. Humans only review and merge; nobody opens a PR by han
 |---|---|---|---|
 | Level state file | AD FR-31: the skill writes `<wt>/.dev/issues/<N>/pipeline.json` as the hook's input | **Not built.** The hook's input is a launch record outside the worktree (section 6). | The hook design (IR-1 to IR-3) is later (2026-11-06) and says `pipeline.json` is documentation only: the agent can edit anything inside the worktree. A file nothing reads is not written. |
 | Git `pre-push` layer | AD FR-32: the claim installs a `pre-push` check in the new worktree | **Not built by the claim.** The hook feature's own installer owns it (hook design 19.2). The claim reports `enforcement_hook`. | Hook design 19 answers AD's open questions (place, chaining, removal) and makes installation part of #394. |
-| Hook refusal rules | Hook IR-4 and IR-7: refuse a governed launch when `jq`, the script, effective registration or L2 is missing | **Not built.** A missing hook script gives warning `W-ENFORCEMENT-ABSENT`; the launch proceeds (default D3). | The hook does not exist yet, and AD section 9 says phase 2 does not wait for it; OB-6 to OB-9 must run before it exists. #394 turns the warning into a refusal by extending one function (section 8). |
+| Hook refusal rules | Hook IR-4 and IR-7: refuse a governed launch when `jq`, the script, effective registration or L2 is missing | **Built in #394.** A guard that is missing or not effective gives the refusal `W-ENFORCEMENT-ABSENT`: no agent starts and no launch record is written. A missing L2 layer gives the warning `W-L2-ABSENT` and the launch continues (the L2 layer is not built yet). | This design first made it a warning (old default D3) because the hook did not exist; #394 turned it into a refusal (IR-4). IR-7 stays a warning until an L2 layer exists. |
 | `launch_status` values | AD FR-30: `launched \| failed \| not_requested` | Adds `already_launched` | AD FR-27 needs a state for a re-claim that finds a `launch` entry. |
 | Launch prompt | AD FR-22: one plain sentence, no leading `/` | The sentence is prefixed with the hook's marker `[sc-launch:v1:<nonce>] ` (hook IR-2). The prefix starts with `[`, so the no-leading-`/` rule holds. | The hook binds the session by that marker. |
 | Create JSON shape | MR R2 UNVERIFIED | AD observed `result.worktree.{id, path, branch, ...}`. FR-20 (path from a row-id difference) stays; the field is not relied on. | The set difference works with an opaque create result. |
@@ -127,9 +128,9 @@ The hook must read the level from state the launched agent cannot edit. Anything
 | Re-claim | a new nonce and a new session for every launch, never `--resume` (a re-claim that finds a `launch` entry launches nothing; the user removes the entry to launch again) | IR-5 |
 | `pipeline.json` | not written (section 3) | IR-3 |
 
-The word-to-level map the hook applies: `worktree` = W (planning only, `WA` after a person approves), `full` = F, `full-submit` = FS. The approval step of level `worktree` is the hook's (a person types `approved` or `/sc:implement` in the session). This design adds nothing for it; until the hook exists the stop at the plan is an instruction in the launch prompt only, and the claim says so (`W-ENFORCEMENT-ABSENT`).
+The word-to-level map the hook applies: `worktree` = W (planning only, `WA` after a person approves), `full` = F, `full-submit` = FS. The approval step of level `worktree` is the hook's (a person types `approved` or `/sc:implement` in the session). This design adds nothing for it. The hook enforces the stop; when the guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent, no launch record), so no level runs as a prompt-only instruction.
 
-`enforcement_hook` (contract field) is `installed` when `$HOME/.claude/hooks/launch-level-guard.sh` exists and is executable, else `missing`. It does not claim the hook is registered or effective. The check is one function, `enforcement_status()` in `orca_worktree.py`; #394 extends it with the IR-4 and IR-7 refusals (`jq`, registration, `CLAUDE_CONFIG_DIR`, L2) without touching the flag design.
+`enforcement_hook` (contract field) is `installed` when `$HOME/.claude/hooks/launch-level-guard.sh` exists and is executable, else `missing`. It does not claim the hook is registered or effective. The check is one function, `enforcement_status()` in `orca_worktree.py`; #394 replaced it with the IR-4 preflight `enforcement_preflight()` (`jq`, `uv`, the installed guard, effective registration, `CLAUDE_CONFIG_DIR`), which refuses the launch with `W-ENFORCEMENT-ABSENT`, and added the IR-7 check `l2_status()`, which only warns with `W-L2-ABSENT`.
 
 ## 7. Claim flow changes (`refs/claim.md`)
 
@@ -206,7 +207,7 @@ Arguments `--number <N> --source <D> --level worktree|full [--submit]`. Output `
 |---|---|
 | 1 | Read `<D>/worktree.json` through the record guard. Missing or failing: `failed`, `W-LAUNCH-FAILED` "no usable worktree record". |
 | 2 | A `launch` entry exists: `already_launched` with its `at` time; no `orca` call, no record written. |
-| 3 | `enforcement_hook = enforcement_status()` (section 6). `missing` sets `W-ENFORCEMENT-ABSENT` ("levels are instructions in the prompt only until the hook of #394 ships"); it does not stop the launch (default D3). |
+| 3 | `enforcement_hook = enforcement_status()` (section 6). `missing` sets `W-ENFORCEMENT-ABSENT`. Updated by #394: the IR-4 preflight refuses the launch here (`failed`, no agent, no launch record); old default D3 is replaced. |
 | 4 | Write `pending/<nonce>` (section 6). A write error: `failed`, `W-LAUNCH-FAILED`, no launch. |
 | 5 | `orca agent launch --agent claude --worktree path:<wt> --surface terminal --prompt "[sc-launch:v1:<nonce>] Read .dev/issues/<N>/launch-prompt.md and follow it." --json`. No `--model` or `--effort` (AD FR-22). A nonzero exit, a timeout, or `ok != true`: remove the pending record, `failed`, `W-LAUNCH-FAILED` with the first stderr line, and `hand_command` (the same call without the marker, with the note "an agent started by hand is not governed by the hook; re-running the claim is preferred"). A timeout may have started an agent; `detail` says to check Orca before re-running. |
 | 6 | Shim check (FR-28): take the terminal handle (the first string value under a key `handle` in the launch JSON, found by a recursive walk, because the `agent launch` result shape is UNVERIFIED), then `orca terminal read --terminal <handle> --screen --json` up to 5 times, 2 s apart. Pass when `result.terminal.tail` text holds `[ccsession]` or `Session name (Enter or Ctrl+C` (the question text of `.dev/evals/ccsession-orca-e2e-20261026/EVIDENCE.md`, check 11). No handle, no readable screen or no match: keep the launch and set `W-LAUNCH-NOT-CCSESSION` ("this agent is NOT behind the ccsession shim, or could not be verified; close it"). The pending record stays. |
@@ -278,7 +279,8 @@ Warnings (the claim `status` stays `success` for all of them). `W-ORCA-MISSING`
 | `W-WORKTREE-COPY-FAILED` | worktree (created, reused or failed) | files skipped as tracked, kept as `.prev`, or not copied | copy the named files by hand |
 | `W-LAUNCH-FAILED` | launch | no usable record, pending record not written, or `orca agent launch` failed | re-run the claim; the hand command is printed for reference |
 | `W-LAUNCH-NOT-CCSESSION` | launch (status `launched`) | the screen shows no `[ccsession]` and no session-name question, or could not be read | "this agent is NOT behind the ccsession shim; close it"; Orca's Claude command must be `/home/coder/.local/bin/ccsession-orca` (OB-5) |
-| `W-ENFORCEMENT-ABSENT` | launch (status `launched`) | hook script not installed | "the level is an instruction in the prompt only until the launch-level hook (#394) ships; do not use `full` or `--submit` on a real issue yet" |
+| `W-ENFORCEMENT-ABSENT` | launch (status `failed`; updated by #394) | the guard is missing or not effective (IR-4 preflight) | the launch was refused and no agent was started; fix each condition the `detail` names (usually `superclaude install`), then claim again |
+| `W-L2-ABSENT` | launch (status `launched`; added by #394) | the worktree has no L2 pre-push layer | the L2 layer is not built yet and the limits are enforced by the L1 guard only; the agent was started |
 
 A launch is never attempted when the worktree `status` is `failed` (FR-21).
 
@@ -336,7 +338,7 @@ All run with `uv run pytest`. The Orca and git seams are faked; no test calls a
 | LA-3 | launch failure (nonzero exit, timeout, `ok: false`) removes the pending record and gives `W-LAUNCH-FAILED` with a hand command; pending write failure (read-only store) makes no launch call |
 | LA-4 | a `launch` entry in the record: `already_launched`, no `orca` call, no new pending record; a record without one launches; the entry is written after a launch even when the shim check fails |
 | LA-5 | shim check: a screen with `[ccsession]` and a screen with the session-name question pass; a screen without either, an unreadable terminal and a launch JSON with no `handle` give `W-LAUNCH-NOT-CCSESSION` and status `launched` |
-| LA-6 | `enforcement_hook`: `missing` and `W-ENFORCEMENT-ABSENT` without `$HOME/.claude/hooks/launch-level-guard.sh`; `installed` with an executable file; the launch happens in both cases |
+| LA-6 | `enforcement_hook`: `missing` and `W-ENFORCEMENT-ABSENT` without `$HOME/.claude/hooks/launch-level-guard.sh`; `installed` with an executable file. Updated by #394: `missing` refuses the launch (no agent, no launch record), and `W-L2-ABSENT` is a warning on a `launched` result |
 | LA-7 | no launch call for a `failed` worktree record and no pending record for `none` (the skill never calls `launch` for `none`; the test pins the skill text, ST-9) |
 | ARG-1 | bad arguments of every subcommand exit 2 |
 
@@ -368,7 +370,7 @@ Each is a **design default**: a choice made where MR, AD and the hook design are
 |---|---|---|
 | D1 | This design lives at `docs/designs/sc-issue-claim-pipeline-flag.md` | The existing design-doc folder |
 | D2 | Worktree name `issue-<N>`, `--no-parent`, base `origin/<B>`, `--repo path:<main>`, `--comment "sc:issue <R>#<N>"`, no `--agent` on create | MR 2.3, AD 4.6: the create command stays as accepted; the agent is started by `agent launch` so a re-claimed worktree can be launched too |
-| D3 | A missing hook script is a warning (`W-ENFORCEMENT-ABSENT`), not a refusal, for every level | The hook is #394 and does not exist; AD section 9 says phase 2 does not wait for it and OB-6 to OB-9 must run first. The warning states that `full` and `--submit` should not be used on a real issue yet. Turning it into a refusal is a one-function change in #394 |
+| D3 | Replaced by #394: a guard that is missing or not effective refuses the launch (`W-ENFORCEMENT-ABSENT`; no agent, no launch record) for every level; a missing L2 layer is the warning `W-L2-ABSENT` and the launch continues | Originally a warning because the hook did not exist; #394 built the guard and its IR-4 preflight. No governed claim is used on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass (hook design section 7, U1) |
 | D4 | `version: "1.1.0"` in `commands/issue.md` only | MR 2.7 |
 | D5 | Pending-record words `worktree`, `full`, `full-submit` | The hook design's `pending/<nonce>` content (section 3) |
 | D6 | Shim check: 5 screen reads, 2 s apart (about 10 s). Pass on `[ccsession]` or the session-name question | The ccsession question falls back to untagged after 30 s (EVIDENCE check 11), so the window is inside it; the whole call stays inside the 120 s timeout |
diff --git a/docs/designs/sc-issue-launch-level-hook.md b/docs/designs/sc-issue-launch-level-hook.md
index bcc552c2..f3da7e87 100644
--- a/docs/designs/sc-issue-launch-level-hook.md
+++ b/docs/designs/sc-issue-launch-level-hook.md
@@ -3,18 +3,18 @@ title: "Launch-level enforcement hook: design"
 issue: IronbellyOrg/IronClaude#394
 type: architecture
 format: spec
-status: design draft; scoped job identity foundation implemented; full enforcement pending
+status: "built: L1 guard script, its two registrations, installer entry, claim IR-1 to IR-7 detection (IR-4 refusal, IR-7 as warning W-L2-ABSENT) and the scoped job identity foundation; pending: OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX and the L2 pre-push layer"
 review_status: "one authorized simulated spec-panel iteration, followed by scoped identity implementation and per-task compliance checks; full enforcement not runtime-approved"
 adversarial_status: partial
 historical_convergence: "1.00 by the earlier protocol rule (0.70 identical verdicts); not this panel's score"
-planning_status: "conditional: B-CTX feasibility gate must precede enforcement implementation"
+planning_status: "L1 built after the B-CTX evidence review (L1: PROCEED); L2 blocked on B-CTX (L2: BLOCKED); no governed claim on a real issue until OB-H1 item 1, OB-H2 and OB-H3 pass (§7 U1 ship gate, §14)"
 source: .dev/brainstorms/20261105-170229-launch-level-hook/
 generated: 2026-11-05
 ---
 
 # Launch-level enforcement hook: design
 
-> **Full enforcement is not runtime-approved.** The authorized specification panel found the blocking actor-selection prerequisite B-CTX (§19.1). The owner subsequently authorized a narrowly scoped launcher/harness identity integration. That Bash job identity foundation is implemented separately (§19.7); isolated live CLI observations distinguish a rewritten governed call from an unchanged ordinary call. This does not build the main classifier, claim pipeline or production pre-push guard, and does not prove real `/clear`, Monitor or every lifecycle variant. O-22 remains accepted. The earlier blocked plan stays blocked; OB-H1 to OB-H3 and full enforcement integration remain required.
+> **Full enforcement is not runtime-approved.** The authorized specification panel found the blocking actor-selection prerequisite B-CTX (§19.1). The owner subsequently authorized a narrowly scoped launcher/harness identity integration. That Bash job identity foundation is implemented separately (§19.7); isolated live CLI observations distinguish a rewritten governed call from an unchanged ordinary call. This does not build the main classifier, claim pipeline or production pre-push guard, and does not prove real `/clear`, Monitor or every lifecycle variant. O-22 remains accepted. The earlier blocked plan stays blocked; OB-H1 to OB-H3 and full enforcement integration remain required. The later implementation of issue #394 built the L1 guard and the claim-side checks; §19.8 lists what exists and what is still pending.
 
 This updated design is authoritative for **new planning**. `merged-requirements.md` ("MR"), the Q1–Q4 debate outputs and the earlier plan reviews are historical/advisory inputs, not synchronized copies. Identifiers FR-L-nn, IR-n, O-n, OD-..., R-n, U-n, LL-..., T-... retain traceability; explicit changes here override older wording/expected results. `[B-n]` identifies an earlier amendment's provenance, not a current approval. The earlier failed verdicts remain historical in §12/§15.2. Panel findings, the full guard boundary table, quantity-flow analysis and the written document-change plan are in `.dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md`. No further panel or debate loop is selected.
 
@@ -31,7 +31,7 @@ One script, `launch-level-guard.sh`, enforces the level that `/sc:issue --claim
 
 Policy intent: no level authorizes a merge or a push to `master` or `main`. Coverage is the explicitly checked routes, not universal prevention. Targets: TH1 (honest drift) and TH2 (specified one-step workarounds); not TH3 (deliberate evasion). Same-user guardrail, not a sandbox. A person's push from the **same** launched worktree must stay unrestricted by launch policy, even while an agent is active; deleting a marker is not a prerequisite for that right.
 
-In scope: L1 text/skill hook, two Claude registrations, installer-list entry, tests, IR-1 to IR-7 and accepted O-22 L2 pre-push design (§19). L1 uses bash plus `jq`, `sed`, `tr`: exit 0 allows, exit 2 blocks, no `onFailure`. L2 is a separate Git hook with Git's nonzero-veto convention and necessarily uses Git's resolved update stream. Its process-context candidate is Linux-only until proven otherwise; its process reads are not part of the old L1 subprocess budget. No new runtime service, server policy, managed settings deployment, shell parser, forwarding framework or config migration is authorized. Claim launching and ccsession implementation remain separate integration work; current claim code does not implement this proposed pipeline interface. Issue #322's source-write boundary and reading `pipeline.json` remain out of scope.
+In scope: L1 text/skill hook, two Claude registrations, installer-list entry, tests, IR-1 to IR-7 and accepted O-22 L2 pre-push design (§19). L1 uses bash plus `jq`, `sed`, `tr`: exit 0 allows, exit 2 blocks, no `onFailure`. L2 is a separate Git hook with Git's nonzero-veto convention and necessarily uses Git's resolved update stream. Its process-context candidate is Linux-only until proven otherwise; its process reads are not part of the old L1 subprocess budget. No new runtime service, server policy, managed settings deployment, shell parser, forwarding framework or config migration is authorized. Claim launching and ccsession implementation are separate integration work; the claim code now implements IR-1, IR-2 and IR-4 to IR-7 (IR-7 as the warning W-L2-ABSENT), and IR-3 stays documentation only because no code writes `pipeline.json` (§19.8). Issue #322's source-write boundary and reading `pipeline.json` remain out of scope.
 
 ## 2. Architecture and files
 
@@ -132,7 +132,7 @@ Message id is `LL-<class>`; PUSHFORM gives LL-PUSH-FORM, GHWRITE gives LL-GH-WRI
 
 `cmd` is the decoded `tool_input.command` of a Bash (foreground or background) or Monitor call. Monitor with only `ws`: NONE. No `${s//...}` over the text (fact T5).
 
-**Normalisation, in order.** NM1: over 65,536 bytes gives BIG, stop. NM1a [B-1]: `[[ $cmd =~ $'[^[:space:]\\\\]\\\\\n' ]]` gives UNKNOWN. NM2 and NM3 [B-2] give T. NM4 gives G (never split). NM5 and NM6 give W. Segments [B-6]: always `IFS=';' read -r -a segs <<< "$W"`; words `ws=($seg)` under `set -f`. NM7: basename is the text after the last `/`.
+**Normalisation, in order.** NM1: over 65,536 bytes gives BIG, stop. NM1a [B-1]: `[[ $cmd =~ $'[^[:space:]\\\\]\\\\\n' ]]` gives UNKNOWN. (Note: that printed test never matches, because a quoted `$'...'` on the right of `=~` is matched as literal text; the implemented script holds the pattern in a variable, `LL_RE_NM1A`, and tests `[[ $cmd =~ $LL_RE_NM1A ]]`.) NM2 and NM3 [B-2] give T. NM4 gives G (never split). NM5 and NM6 give W. Segments [B-6]: always `IFS=';' read -r -a segs <<< "$W"`; words `ws=($seg)` under `set -f`. NM7: basename is the text after the last `/`.
 
 ```bash
 T=$(printf '%s\n' "$cmd" | sed -E -e "s/\\\$(['\"])/\\1/g" -e "s/['\"\\\\]//g" -e 's#/+#/#g' -e 's#/(\./)+#/#g' -e 's/`/ $;/g')
@@ -503,7 +503,7 @@ Historical candidate steps, not adopted as an implementation contract:
 
 **OB-CTX / B-CTX completion evidence (not observed here):** a log-only probe must capture the actual main/subagent/nested/background Bash/Monitor-to-Git and hook process trees, same-worktree human terminal, ordinary Claude session, detached/reparented jobs, launch wrapper, process exit/PID reuse, resume in a new process, /clear/fork, and release while a job remains alive. Establish the needed ancestry bound from that evidence, with an explicit exhaustion rule. In particular, prove how an ordinary new session in a reused Claude process and an old governed background child can be distinguished at the same time. Kernel ancestry alone may not supply that distinction. No single PID-label lookup is accepted as a solution to it.
 
-**Current full-enforcement verdict:** B-CTX remains **OPEN/BLOCKING for the earlier plan's complete lifecycle coverage**. The owner authorized the new scoped integration; its per-job selector and isolated live Bash evidence are described in §19.7. That is not a retroactive PASS for the old controller-ancestry probe or for unobserved `/clear`, resume, Monitor, nested-subagent and auto-mode variants. Existing claim code still has no pipeline-launch implementation. Keep production activation conditional on the actual supported execution surfaces and their required observations, without a root service or weakening human isolation. O-22/O-21/O-13 are not reopened.
+**Current full-enforcement verdict:** B-CTX remains **OPEN/BLOCKING for the earlier plan's complete lifecycle coverage**. The owner authorized the new scoped integration; its per-job selector and isolated live Bash evidence are described in §19.7. That is not a retroactive PASS for the old controller-ancestry probe or for unobserved `/clear`, resume, Monitor, nested-subagent and auto-mode variants. The claim code now launches governed pipelines and refuses one when the L1 guard is not effective (§19.8); the L2 layer this section selects for is not built. Keep production activation conditional on the actual supported execution surfaces and their required observations, without a root service or weakening human isolation. O-22/O-21/O-13 are not reopened.
 
 ### 19.2 Placement and coexistence (Q1/Q2, narrowed)
 
@@ -562,4 +562,17 @@ The owner's subsequent authorization covers the missing launcher/harness identit
 
 **Observed versus simulated:** isolated actual CLI PreToolUse/PostToolUse records show one governed call rewritten without a permission-approval decision and reporting the same origin UUID from the executed selector; its ordinary counterpart is not rewritten and reports ordinary. Both actual CLI runs exited 0. The managed identity package `TASK-WF-authorizedNarrow-20261106-214325` retains the redacted `artifacts/live-harness-events.jsonl`. Controlled subprocess tests exercise old-background/new-ordinary overlap, release, stale process data, quoting, startup failure and signal behavior; they are not observations of real `/clear` or resume. Actual persistent-cwd tracking, background scheduling, `/clear`, resume, Monitor, auto mode, concurrent-hook composition and nested-subagent payload variants remain unobserved unless later evidence explicitly adds them.
 
-**Next integration:** a future claim launcher must create the private governed level record for the actual logical session, validate effective adapter/runtime availability and install the separately designed production pre-push policy. That policy may use this selector only on the tested local Bash surface; it must retain an explicit unsupported path for unknown or unadapted execution. This increment does not implement the claim pipeline, the full text classifier, automatic session binding from a claim marker or the production pre-push install/release policy. The earlier blocked workflow remains historical and immutable, not retroactively compliant.
+**Next integration:** a future claim launcher must create the private governed level record for the actual logical session, validate effective adapter/runtime availability and install the separately designed production pre-push policy. That policy may use this selector only on the tested local Bash surface; it must retain an explicit unsupported path for unknown or unadapted execution. This increment does not implement the claim pipeline, the full text classifier, automatic session binding from a claim marker or the production pre-push install/release policy. The earlier blocked workflow remains historical and immutable, not retroactively compliant. §19.8 records what the later issue #394 implementation added.
+
+### 19.8 Implementation status (issue #394)
+
+**Built:**
+
+- The L1 guard `src/superclaude/hooks/scripts/launch-level-guard.sh` (bash, `jq`, `sed`, `tr`; exit 0 allows, exit 2 blocks), with a byte-identical plugin copy.
+- Its two registrations, on `UserPromptSubmit` and on `PreToolUse` with the §13 matcher, in `src/superclaude/hooks/hooks.json` and `plugins/superclaude/hooks/hooks.json`.
+- The installer entry `"launch-level-guard.sh"` in `_FRESHNESS_SCRIPTS` of `src/superclaude/cli/install_hooks.py`.
+- Claim-side detection in `orca_worktree.py`: IR-1 and IR-2 (pending launch record and prompt mark), IR-4 (a read-only preflight that refuses the governed launch with `W-ENFORCEMENT-ABSENT` when `jq`, `uv`, the installed guard, its effective registrations or the job identity registration is missing or not effective; no agent starts and no record is written), IR-5 (new session and nonce per claim), IR-6 (release instruction and L1/L2 status lines) and IR-7 as the warning `W-L2-ABSENT` (the launch continues; the owner had not answered whether it should refuse). IR-3 stays documentation only: no code writes `pipeline.json`.
+
+**Pending, none run:** OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX, and the L2 pre-push layer of §19.2 to §19.5, which needs its own plan after B-CTX. No governed claim is used on a real issue until OB-H1 item 1 shows the parent `session_id` in subagent payloads, OB-H2 passes and OB-H3 passes (§7 U1 ship gate, §14).
+
+Pending launch records are not pruned: a person removes old state files (owner decision O-15).
diff --git a/docs/user-guide/commands.md b/docs/user-guide/commands.md
index 6fe2f43c..40ea41b6 100644
--- a/docs/user-guide/commands.md
+++ b/docs/user-guide/commands.md
@@ -378,7 +378,7 @@ When codegraph, the index or its lookup tools are not usable, it falls back to G
 | `full` with `--submit` | Does the same, then commits, pushes a feature branch to `origin` and opens a PR through `/sc:pr-submit --monitor 3` | Yes; never merges |
 | `none` | Creates the worktree and copies the files; launches no agent. You run `next-steps.md` there yourself | No |
 
-No level merges anything: people review and merge. The agent starts behind the ccsession shim (the claim warns with `W-LAUNCH-NOT-CCSESSION` if it cannot confirm that). The levels are instructions in the agent's prompt until the launch-level enforcement hook (issue 394) is installed; until then the claim warns with `W-ENFORCEMENT-ABSENT` and you should not use `full` or `--submit` on a real issue.
+No level merges anything: people review and merge. The agent starts behind the ccsession shim (the claim warns with `W-LAUNCH-NOT-CCSESSION` if it cannot confirm that). The launch-level guard (issue 394) enforces the level. When the guard is missing or not effective (for example not installed, not registered, or `jq` missing) the claim refuses the launch with `W-ENFORCEMENT-ABSENT`: no agent starts and no launch record is written; run `superclaude install` and claim again. When the worktree has no L2 pre-push layer the claim warns with `W-L2-ABSENT` and the launch continues; the L2 layer is not built yet, so only the L1 guard enforces the limits. Do not use a governed claim (`worktree` or `full`) on a real issue until OB-H1 item 1 shows the parent `session_id` in subagent payloads, OB-H2 passes and OB-H3 passes (the U1 ship gate, section 7 of `docs/designs/sc-issue-launch-level-hook.md`).
 
 **Examples:**
 
diff --git a/src/superclaude/commands/issue.md b/src/superclaude/commands/issue.md
index a0db85ff..9cd4bf92 100644
--- a/src/superclaude/commands/issue.md
+++ b/src/superclaude/commands/issue.md
@@ -13,7 +13,7 @@ argument-hint: "--claim <number|url> [--pipeline worktree|full|none] [--submit]
 
 Two modes on the repository that `origin` points at:
 
-- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then creates (or reuses) the Orca worktree `issue-<N>` and launches one Claude Code agent in it at the `--pipeline` level. Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted). The levels: `worktree` (the default) stops at a plan a human approves, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, and `none` creates the worktree and launches no agent. Nothing ever merges.
+- `--claim` takes an existing issue: assigns it to you on GitHub and, when one exists, on its ClickUp task; checks whether the issue text is still accurate against today's code and the pull requests merged since it was opened; writes a summary and a next-step prompt under `.dev/issues/<N>/`; posts two marked comments; then creates (or reuses) the Orca worktree `issue-<N>` and launches one Claude Code agent in it at the `--pipeline` level. Orca must be running (STOP `E-ORCA-REQUIRED` otherwise, before anything is assigned or posted). The levels: `worktree` (the default) stops at a plan a human approves, `full` also implements without a commit or a push, `full` with `--submit` also commits, pushes a feature branch and opens a PR through `/sc:pr-submit --monitor 3`, and `none` creates the worktree and launches no agent. Nothing ever merges. When the launch-level guard is missing or not effective the claim refuses the launch with `W-ENFORCEMENT-ABSENT` (no agent starts and no launch record is written); when the worktree has no L2 pre-push layer it warns with `W-L2-ABSENT` and the launch continues (the L2 layer is not built yet). No governed claim (`worktree` or `full`) is used on a real issue until OB-H1 item 1 shows the parent `session_id` in subagent payloads, OB-H2 passes and OB-H3 passes (the U1 ship gate, design section 7 of `sc-issue-launch-level-hook.md`).
 - `--create` turns a description into a GitHub issue built from one of four templates, with labels from a fixed set. GitHub only: no ClickUp task.
 
 Both modes post directly to GitHub; nothing is shown for approval first.
diff --git a/src/superclaude/skills/sc-issue-protocol/SKILL.md b/src/superclaude/skills/sc-issue-protocol/SKILL.md
index 0ecdaf08..fcd02ca7 100644
--- a/src/superclaude/skills/sc-issue-protocol/SKILL.md
+++ b/src/superclaude/skills/sc-issue-protocol/SKILL.md
@@ -89,7 +89,7 @@ Load `refs/claim.md` now. `<N>` is the issue number, `<D>` = `.dev/issues/<N>/`.
 6. **Wave 5, next steps.** Load `refs/chains.md`. Invoke `Skill sc-recommend` with the goal format of `refs/chains.md`; save its output verbatim to `<D>/recommend.md` from `templates/recommend-record.md`. Write `<D>/next-steps.md` from `templates/next-steps.md`, starting with the `/model` tier line and carrying the `Plan boundary: after step <K>` line. Unless `--pipeline none`, render `<D>/launch-prompt.md` with `orca_worktree.py prompt` (the script keeps the existing prompt only while a launch entry's worktree still exists).
 7. **Wave 6, post.** Post or edit (by marker) the accuracy-check comment and the claim comment (`templates/claim-comment.md`). Then continue with Wave 7 and Wave 8. A STOP in Waves 0 to 6 means no Orca call after the Wave 0 check. This skill never runs a step of `next-steps.md` (B2).
 8. **Wave 7, worktree.** `orca_worktree.py worktree --repo <R> --number <N> --base origin/<B> --source <D>` creates or reuses the worktree and copies `<D>` into it. Every failure is a warning: the claim `status` stays `success`.
-9. **Wave 8, launch.** Only when `--pipeline` is not `none` and Wave 7 `status` is `created` or `reused`: `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]` first checks that the launch-level guard would be effective (the IR-4 preflight; read only) and refuses the launch with `W-ENFORCEMENT-ABSENT` when it would not; otherwise it starts one agent in the worktree at the chosen level, behind the ccsession shim, and records the level for the enforcement hook, adding the warning `W-L2-ABSENT` when the worktree has no L2 pre-push layer (the launch still goes ahead). The agent, not this skill, runs the steps. Every failure, a refusal included, is a warning. Then print the final output of `refs/claim.md` (worktree line, tracking note, launch result with its release instruction and L1/L2 layer status lines, every warning with its remedy line), the return contract, and STOP.
+9. **Wave 8, launch.** Only when `--pipeline` is not `none` and Wave 7 `status` is `created` or `reused`: `orca_worktree.py launch --number <N> --source <D> --level <L> [--submit]` first checks that the launch-level guard would be effective (the IR-4 preflight; read only) and refuses the launch with `W-ENFORCEMENT-ABSENT` when the guard is missing or not effective (no agent starts and no launch record is written); otherwise it starts one agent in the worktree at the chosen level, behind the ccsession shim, and records the level for the enforcement hook, adding the warning `W-L2-ABSENT` when the worktree has no L2 pre-push layer (the launch still goes ahead; the L2 layer is not built yet). The agent, not this skill, runs the steps. Ship gate (U1, design section 7 of `sc-issue-launch-level-hook.md`): no governed claim (`--pipeline worktree` or `full`) is used on a real issue until OB-H1 item 1 shows the parent `session_id` in subagent payloads, OB-H2 passes and OB-H3 passes. Every failure, a refusal included, is a warning. Then print the final output of `refs/claim.md` (worktree line, tracking note, launch result with its release instruction and L1/L2 layer status lines, every warning with its remedy line), the return contract, and STOP.
 
 ## Create mode
 
diff --git a/src/superclaude/skills/sc-issue-protocol/refs/claim.md b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
index d22f606c..12627292 100644
--- a/src/superclaude/skills/sc-issue-protocol/refs/claim.md
+++ b/src/superclaude/skills/sc-issue-protocol/refs/claim.md
@@ -127,6 +127,8 @@ Read the one JSON object it prints: `status` (`launched`, `already_launched` or
 
 `W-L2-ABSENT` is added to a `launched` result whenever the L2 line says `absent`. The design (IR-7) asks for a refusal there; until an L2 layer is built the claim only warns, so the launch goes ahead. When `W-LAUNCH-NOT-CCSESSION` is also present it comes first: `warning` holds it and `detail` carries `also W-L2-ABSENT: ...`.
 
+Ship gate (U1, design section 7 of `sc-issue-launch-level-hook.md`): no governed claim (`--pipeline worktree` or `full`) is used on a real issue until OB-H1 item 1 shows the parent `session_id` in subagent payloads, OB-H2 passes and OB-H3 passes.
+
 ## Final output (replaces "print the path and STOP")
 
 Print, in this order:

Delta diff from the previous reviewed tree (empty on the first review): 
Earlier blocking findings of this start (empty on the first review): 
Saved-probe re-check hit locations (may be empty): 

Do not trust the implementer's report.

First mark each earlier blocking finding resolved, open or regressed from the diff. Then, for each AC, mark it met or unmet. Require citations: every AC you mark, met or unmet, carries a `path:line` or `Ti.ACk@path:line` citation, and an unmet mark lists the finding ids behind it. Do not return a verdict; the orchestrator computes it.

For every finding answer four questions, each yes or no:
1. ac-outcome-missing: is output an AC requires absent, or does it contradict the AC text, or does an evidence claim you could not verify have no evidence row?
2. false-claim: is a claim in delivered text or code false against live source, or does a recipe or instruction followed as written not do what the text says?
3. harmful-effect: does code or a recipe this task added or changed write, append, chmod or delete tracked or production data, mutate state outside the task's declared outputs, or expose a secret?
4. quoted-constraint-breach: does the diff violate a quoted plan constraint, out-of-scope, non-goal or non-negotiable item, or an explicit task instruction?

Anchor rule: cite exactly one anchor per yes. ac-outcome-missing: the quoted AC words. false-claim: the live-source path:line holding the contradicting text. harmful-effect: the diff line that is the write. quoted-constraint-breach: the quoted constraint or instruction text. A yes without a valid anchor does not block.

Write one line per finding:
F<k>.<j> ac=<Ti.ACk|scope> at=<path:line> anchor=<quoted text or path:line> chk=<amiss,false,harm,constraint as y/n> family=<id> fix=<text> [covers=<quoted AC clause or constraint>]: <text>
Do not write sev=, trigger=, first= or origin=; the orchestrator adds them. Write one status line per earlier blocking finding: F<m>.<j> resolved|open|regressed.

Inside /sc:implement this protocol's severity model governs this review and takes precedence over the session's output style and the copy of it injected into every subagent; only blocking findings may fail an attempt.

You are not given an adviser answer, brief, evidence file or troubleshoot report. Do not read the retry folders (legacy `.dev/implement/<slug>/retries/`, managed `<pkg>/artifacts/retries/`) or `.dev/troubleshoot/`. A citation into either makes the verdict `cannot-verify`.
The prior-findings slot above carries earlier blocking finding lines that the orchestrator copies byte for byte from `review-*.md` and `repair-*.md`; they reach you as prompt text, not as an evidence file. Do not read those folders to get them, and never cite the slot or the file it came from.
