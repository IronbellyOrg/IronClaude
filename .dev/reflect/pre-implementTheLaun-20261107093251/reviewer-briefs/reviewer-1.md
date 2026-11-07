## T1 card excerpt

```yaml
findings:
  - id: F-1
    claim: "B-CTX gate (INF-002) is Task 1, the first task, but it is an evidence-review verdict from existing artifacts, not the log-only live probe that design section 14 step 0 specifies."
    citation: ".dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:32 and docs/designs/sc-issue-launch-level-hook.md:359"
    note: "The plan Constraints (live observations are not run) make this a stated, deliberate narrowing."
  - id: F-2
    claim: "Task 20 makes the claim refuse every governed launch until an L2 layer ships, which disables the default --pipeline worktree launch; the task records the consequence but does not obtain an owner decision."
    citation: ".dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:314 and docs/designs/sc-issue-launch-level-hook.md:355,514"
  - id: F-3
    claim: "Task 20 detects 'the owned shared hook file and its recorded B-CTX contract marker', but neither the marker nor the ownership proof is defined, and Task 21 says no L2 artifact is built, so the pass case cannot occur in production."
    citation: ".dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:318 and docs/designs/sc-issue-launch-level-hook.md:512"
  - id: F-4
    claim: "Task 12 depends on Task 10 and not on Task 11, so a plan executor may register the guard before approval handling exists; ordering is by number so the risk is low."
    citation: ".dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:209-211"
  - id: F-5
    claim: "IR-3 (pipeline.json is documentation only; amend FR-31) has no task, and the design's own note says the claim code writes no pipeline.json."
    citation: "docs/designs/sc-issue-launch-level-hook.md:351"
  - id: F-6
    claim: "Task 18 turns the PR 425 warning W-ENFORCEMENT-ABSENT into a refusal and reorders the check before publish_pending; existing tests at tests/skills/test_issue_orca_worktree.py around lines 1303 and 1324 must change."
    citation: "src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:937-941,986-989"
risks:
  - "Task 15 asserts a 1.5x timing ratio against block-bare-python.sh; timing assertions can flake on a loaded host."
  - "Task 4, 5 and 7 are large single tasks (state machine, grid, git classifier) that rely on the executor reading design sections 3 to 5."
  - "Regression candidates: Task 18 and Task 20 change launch behaviour that PR 425 shipped (refusal instead of launch)."
recommendations:
  - {id: R-1, file: ".dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md", change: "Define the owned-hook proof and the contract marker in Task 20 or drop the pass case; add 'Depends on: Task 11' to Task 12.", verifier: "re-read Tasks 12 and 20; plan gate still passes"}
  - {id: R-2, file: "docs/designs/sc-issue-launch-level-hook.md", change: "Ask the owner whether governed claims should refuse to launch while L2 is absent (IR-7 as written) before Task 20 is implemented.", verifier: "owner reply recorded in the PR body"}
self_reported_confidence: 0.72
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-07T09:33:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook

### .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:14-30

```markdown
Source: ./source.md
Goal: A launch-level guard script is built, registered, installed and tested so that a session started by /sc:issue --claim --pipeline is held to its level (planning only, implement without publishing, or implement plus a feature-branch push and PR) while every other session is untouched, the claim refuses to launch a governed agent when the guard or its registrations are not effective, and every live observation the design requires is recorded as pending rather than claimed.

## Constraints

- docs/designs/sc-issue-launch-level-hook.md is the authority for this plan. The requirements file .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md (called MR below) is the historical baseline for requirement ids and the test corpus; where the design says it overrides MR (design section 11, DD-2), the design wins. .dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md defines the claim side; the hook interface rules IR-1 to IR-7 in design section 13 win over it.
- This branch builds on open PR 425 (ironbelly/sc-issue-claim-pipeline-flag). The claim code in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py already writes the launch record and marks the prompt (IR-1, IR-2); do not rebuild that.
- The L1 guard is one flat bash script using only bash, jq, sed and tr: exit 0 allows, exit 2 blocks, no onFailure, no Python, no git or network call on ordinary classification. No new runtime service, managed settings deployment, shell parser, hook forwarding framework or git config migration (design section 1).
- Do not change src/superclaude/hooks/scripts/launch-job-identity.sh or tests/hooks/test_launch_job_identity.py. A conflict found with it goes into the record of Task 14, not into that file.
- Ordinary sessions are never blocked by any failure (FR-L-53). Only a positively identified governed session fails closed.
- Live observations (OB-H1, OB-H2, OB-H3, OB-CTX) need real governed sessions or real launches. This plan runs none of them and never launches a governed agent on a real issue or pushes to a real protected branch. They stay pending (a skipped test with a stated reason), never reported as passed. Tests use a temporary HOME and temporary bare remotes.
- Acceptance claims cover the routes the tests exercise. Nothing here claims universal merge protection or defence against a hostile agent (design sections 1 and 12).
- Edit only under src/superclaude/, plugins/superclaude/hooks/, tests/ and docs/; run make sync-dev after hook or skill edits. The plugin copy of every hook script and hooks.json stays byte-identical to its src copy. Generated .claude/ mirrors made by make sync-dev stay out of the commit.
- UV only: run tests with uv run pytest.
- Findings of the issue analysis that this plan answers: F2 (Task 15), F3 (Task 14), F4 (Tasks 18 to 20), F6 (Task 22), F7 (Task 1). F5 (pending records are not pruned) is accepted under owner decision O-15 and is stated in Task 22.

## Phase 1: Feasibility gate and observation scaffolding
```

### .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:32-49

```markdown
## Task 1: Write the B-CTX feasibility verdict

Create ./artifacts/b-ctx-verdict.md. This is the design's step 0 (design sections 14 and 19.1): decide from evidence that already exists what the guard may rely on and what must wait. Evidence to read and cite by path and line: .dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/artifacts/live-harness-events.jsonl and identity-integration-evidence.md, tests/hooks/test_launch_job_identity.py, the header of src/superclaude/hooks/scripts/launch-job-identity.sh, and design sections 19.1 and 19.7.

The file has four parts. First, an evidence table with one row for every lifecycle case listed under "OB-CTX / B-CTX completion evidence" in design section 19.1 (main session, subagent, nested subagent, background Bash or Monitor to Git, same-worktree human terminal, ordinary Claude session, detached or reparented job, launch wrapper, process exit and PID reuse, resume in a new process, /clear and fork, release while a job is alive), each marked observed (cite the artifact line), simulated (cite the test) or unobserved. Second, an L1 verdict line, either "L1: PROCEED" or "L1: STOP", with the reason; the L1 text guard identifies a session by its top-level session_id, so B-CTX does not block writing it, and the ship gate U1 (design section 7) stays pending. Third, an L2 verdict line, either "L2: GO" or "L2: BLOCKED"; GO only if every required case is observed, otherwise BLOCKED with the exact missing launcher or harness integration named. Fourth, the F7 result: state whether .dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md and the four answers under .dev/brainstorms/20261106-l2-prepush-decisions/ exist in this tree, and list each design statement that depends on a missing file as unverified.

No new probe is run against a live session by this task.

Acceptance criteria:
- ./artifacts/b-ctx-verdict.md exists and contains the four parts above, with every row of the design 19.1 case list present.
- Every row marked observed cites an existing path and line of evidence; every case without such a citation is marked unobserved or simulated, never observed.
- The file contains exactly one line starting "L1:" and exactly one line starting "L2:", each with one of the allowed values.
- If the L2 line says BLOCKED, the file names the missing integration in one or more sentences a maintainer can act on.
- The F7 part lists the existence check result for the five named files and no file is invented or recreated.

## Task 2: Add the observation fixtures, the log-only probe and the pending-observation tests

Depends on: Task 1
```

### .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:209-222

```markdown
## Task 12: Register the guard on both events in hooks.json

Depends on: Task 10

Edit src/superclaude/hooks/hooks.json and plugins/superclaude/hooks/hooks.json (byte-identical to each other where they are today) as specified in design section 13 (FR-L-60 to FR-L-66): append to UserPromptSubmit one entry whose hook is the command ~/.claude/hooks/launch-level-guard.sh with timeout 5; append to PreToolUse one entry with the matcher regular expression printed in design section 13 and the same command and timeout. Existing entries, including Bash block-bare-python.sh and Bash launch-job-identity.sh, stay unchanged. Insert the new PreToolUse entry before the launch-job-identity.sh entry so that entry remains the last PreToolUse registration, which tests/cli/test_install_hooks.py (test_real_hooks_json_registers_launch_identity_without_replacing_policy) asserts. No UserPromptExpansion, SessionStart or onFailure registration is added.

Add tests to tests/cli/test_install_hooks.py (or a new tests/hooks/test_launch_level_guard_registration.py) that read both hooks.json files and assert: the guard appears exactly once under UserPromptSubmit and once under PreToolUse with timeout 5; the PreToolUse matcher equals the design string; no onFailure key; the Bash entries for block-bare-python.sh and launch-job-identity.sh are still present; the set of commands registered with the literal matcher Bash in tests/hooks/test_freshness_subagent_start_policy.py is unchanged (the guard's matcher is not the literal Bash).

Acceptance criteria:
- src/superclaude/hooks/hooks.json and plugins/superclaude/hooks/hooks.json both contain the two guard registrations and are identical to each other.
- uv run pytest tests/cli/test_install_hooks.py tests/hooks/test_freshness_subagent_start_policy.py -v passes without any edit to the existing launch-identity registration test.
- The new registration test compiles the PreToolUse matcher as a regular expression and asserts it matches the tool names Bash, Skill, Agent, Task, Edit, Write, NotebookEdit, Monitor, Workflow, RemoteTrigger, SendMessage, CronCreate, ScheduleWakeup and mcp__x__merge_pull_request, and does not match Read, Grep, Glob or TaskCreate.

## Task 13: Ship the guard through the installer and the plugin mirror
```

### .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:287-312

```markdown
## Task 18: Make the claim refuse a governed launch when the guard is not effective (IR-4)

Depends on: Task 13

In src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py replace the warning-only check enforcement_status() (which today only tests that ~/.claude/hooks/launch-level-guard.sh exists and is executable, and whose absence only adds W-ENFORCEMENT-ABSENT after the agent has already started) with the IR-4 check of design section 13, run before publish_pending() so a refused launch writes no pending record and starts no agent. The launch is refused, as a failed launch with the warning code W-ENFORCEMENT-ABSENT and a plain reason, unless all of these hold: jq is on PATH; the installed script exists, is executable and carries the line "# launch-level-guard-version: 1" (the version this plan ships, read from the installed file); the effective configuration enables both registrations, meaning the user settings file under the configured home holds the exact command ~/.claude/hooks/launch-level-guard.sh under UserPromptSubmit and under PreToolUse and neither that file nor the worktree's project settings files set disableAllHooks to true; and CLAUDE_CONFIG_DIR, when set, resolves to the same directory as the home .claude folder (otherwise the launch is refused, never inspecting one directory while another executes). The check never edits any configuration. A claim with --pipeline none is unaffected. Update REMEDY["W-ENFORCEMENT-ABSENT"] to say the launch was refused and what to run (superclaude install, then claim again).

Update tests/skills/test_issue_orca_worktree.py: the two existing tests that expect W-ENFORCEMENT-ABSENT as a warning on a launched claim (around lines 1303 and 1324) now expect a refusal with no orca agent launch call and no pending file; add cases for each failing condition (no jq, script not executable, wrong version line, missing UserPromptSubmit registration, missing PreToolUse registration, disableAllHooks true in user settings and in the worktree project settings, CLAUDE_CONFIG_DIR elsewhere) and a passing case that proceeds to the launch.

Acceptance criteria:
- uv run pytest tests/skills/test_issue_orca_worktree.py -v passes with the updated and new cases.
- For every refusal case the fake orca records no agent launch call, the home directory has no pending/<nonce> file, and the claim output names the failed condition.
- With the guard installed, both registrations present and jq available, the launch proceeds exactly as before this task and records the launch entry.
- The check reads configuration files only; a test asserts the settings files are byte-identical before and after.

## Task 19: State release instructions and layer status in the claim output, and pin re-claim behaviour (IR-5, IR-6)

Depends on: Task 18

In src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py add to the launched-claim result and its printed text the IR-6 information of design section 13: how a person releases the session (in their own terminal run rm on sessions/<session id> and sessions/<session id>.ok under ~/.claude/state/launch-level/, with the session id taken from the "Launch-level guard" block message), and the status of each layer (L1 guard: effective; L2 pre-push: absent until its plan ships, reported with the code W-L2-ABSENT as a status line, not by itself an additional refusal in this task). Add test cases in tests/skills/test_issue_orca_worktree.py that assert the result fields and printed text, and a re-claim case that pins IR-5: a claim whose worktree record already has a launch entry launches nothing and writes no new pending record, and after the launch entry is removed the next launch writes a new pending record with a different nonce (never resuming an earlier session).

Update src/superclaude/skills/sc-issue-protocol/refs/claim.md (Wave 8 section) to describe the release instructions and the layer status lines.

Acceptance criteria:
- A launched claim in the fake-orca test prints the release instruction containing the store path and both file names, and a layer line for L1 and for L2.
- Two launches in the same test home with the launch entry removed in between create two pending records with different names.
- uv run pytest tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py -v passes.
```

### .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:314-338

```markdown
## Task 20: Verify the L2 layer before a governed launch (IR-7)

Depends on: Task 19

In src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py add the IR-7 check of design section 13 and section 19.2: before a governed pipeline starts, verify that an owned, effective L2 pre-push layer is installed and that the B-CTX context contract is proven; absence or conflict preserves all existing hooks and files, reports W-L2-ABSENT with the reason, and refuses that governed launch (no pending record, no agent). A claim with --pipeline none is unaffected. Because Task 21 records that this plan builds no L2 artifact, the check looks for the owned shared hook file and its recorded B-CTX contract marker and reports absence plainly; this task adds only that detection and the refusal, not an installer. Add the warning code to REMEDY with the sentence that the claim cannot launch a governed agent until the L2 plan ships.

Update tests/skills/test_issue_orca_worktree.py with: L2 absent (refusal, W-L2-ABSENT, no launch call), L2 present and owned (proceeds), L2 present but foreign (refusal, the foreign file untouched, byte-identical before and after), and --pipeline none unaffected. Record in ./artifacts/ir7-consequence.md, in plain words, that until an L2 plan ships every governed claim (--pipeline worktree and full) will refuse to launch an agent, that this follows design section 13 IR-7 and section 19.2, and that the owner may want a decision on it.

Acceptance criteria:
- uv run pytest tests/skills/test_issue_orca_worktree.py -v passes with the L2 cases.
- In the refusal cases the fake orca records no agent launch call and no pending record exists; the foreign pre-push file used in the test is byte-identical afterwards.
- ./artifacts/ir7-consequence.md exists, states the consequence above, and cites the design sections.

## Phase 9: L2 disposition, documentation and final verification

## Task 21: Record the L2 pre-push disposition

Depends on: Task 1

Create ./artifacts/l2-disposition.md from the L2 verdict in ./artifacts/b-ctx-verdict.md. If that verdict is L2: BLOCKED, the file states that this plan builds no pre-push file, no L2 installer and no L2 test beyond the IR-7 detection, lists the exact missing launcher or harness integration copied from the verdict, and gives the follow-up scope as design sections 19.2 to 19.5 (one owned shared hooks/pre-push, no config change, no forwarding, refuse field-3 updates to refs/heads/main and refs/heads/master for a positively selected governed process, human pushes in the same worktree unrestricted, tests on a temporary bare remote) with the open items U28 and OB-H3 L2 observation. If the verdict is L2: GO, the file states that a follow-up plan for sections 19.2 to 19.5 is still required because the install place (U28) and the OB-H3 L2 observation are unverified, and this plan builds no L2 code either way.

Acceptance criteria:
- ./artifacts/l2-disposition.md exists and quotes the L2 line of ./artifacts/b-ctx-verdict.md.
- The file states that no pre-push or installer code was written by this plan, and a search of the diff for a file named pre-push finds none.
- The follow-up scope paragraph names design sections 19.2, 19.3, 19.4 and 19.5.
```

### .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:340-351

```markdown
## Task 22: Update the design status, claim documentation and ship-gate text, then run the full checks

Depends on: Task 20, Task 21, Task 17, Task 15

Update docs/designs/sc-issue-launch-level-hook.md: the status and planning_status lines and section 19 text that say the claim code does not implement the pipeline interface or that the L1 guard is not built (finding F6) now state what exists (guard script, registrations, installer entry, IR-4 to IR-7 detection) and what is still pending (OB-H1, OB-H2, OB-H3, OB-CTX, L2); keep the owner decisions and the historical review sections untouched. Update the places that describe W-ENFORCEMENT-ABSENT as a warning (src/superclaude/skills/sc-issue-protocol/SKILL.md, src/superclaude/skills/sc-issue-protocol/refs/claim.md, docs/user-guide/commands.md and docs/designs/sc-issue-claim-pipeline-flag.md) so they describe the refusal, the W-L2-ABSENT refusal, and the rule that no governed claim is used on a real issue until OB-H1 item 1 shows the parent session_id in subagent payloads, OB-H2 passes and OB-H3 passes (the U1 ship gate of design section 7). State in the design document, in one sentence, that pending launch records are not pruned (owner decision O-15). Run make sync-dev and make verify-sync, and update any plugin or mirror copy that a mirror test requires to stay byte-identical.

Acceptance criteria:
- grep for "does not implement this proposed pipeline interface" in docs/designs/sc-issue-launch-level-hook.md returns no match, and the status line names what is built and what is pending.
- grep of the four documents for W-ENFORCEMENT-ABSENT shows wording that describes a refusal, not a warning that lets the launch continue.
- uv run pytest tests/hooks/ tests/cli/test_install_hooks.py tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py -v passes with the only skips being the pending observation tests of tests/hooks/test_launch_level_observations.py.
- make verify-sync exits 0 and make lint exits 0.
- ./artifacts/final-check.md records the exact commands run, the pass and skip counts, and the list of pending observations (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX) with the statement that none has been run.
```

### docs/designs/sc-issue-launch-level-hook.md:349-366

```markdown
- **IR-1** Before `orca agent launch`, write `pending/<nonce>` (one word) atomically; nothing for `--pipeline none`.
- **IR-2** Nonce `secrets.token_hex(16)`; prompt starts `[sc-launch:v1:<nonce>] `.
- **IR-3** `pipeline.json` is documentation only; amend FR-31.
- **IR-4** Refuse a governed launch unless jq exists, the expected installed script/version is executable, and the effective configuration actually enables both registrations (not merely matching text in an ignored/disabled settings file). This increment supports `$HOME/.claude` for hook commands and state. An effective `CLAUDE_CONFIG_DIR` resolving elsewhere is unsupported and must refuse the governed launch, not inspect one directory while executing another. Do not edit global configuration to force compliance. OB-H2 must observe actual hook execution and bind-before-first-tool order.
- **IR-5** Re-claim: new session, new nonce, never `--resume`.
- **IR-6** Claim output says how to release a session and states active L1/L2 status. Release invalidates both layers' session membership; it does not require a person to remove a worktree marker to push ordinarily.
- **IR-7** Claim integration must verify owned/effective L2 installation and the proven B-CTX context contract before a governed pipeline starts. Conflict/absence preserves foreign hooks, reports W-L2-ABSENT and refuses that governed launch. No-pipeline claims stay unaffected. This is a requested interface, not existing claim capability.

## 14. Order of work

0. **B-CTX / OB-CTX feasibility gate (§19.1).** Validate the process-context candidate and same-worktree concurrent human isolation with a log-only bounded probe. If it cannot distinguish required lifecycle cases, stop the enforcement implementation and report the exact missing launcher/harness integration. Do not weaken isolation, add infrastructure or start another review loop. This is the first required task in downstream workflow planning.
1. **OB-H1.** Validate U1, typed top-level identity/event fields and turn wrapping. Gate: item 1 fails, stop (O-9); item 5 bare, apply O-17 alternative. Identity loss on a supported governed call stops deployment.
2. Skeleton (dispatch, store, binding, resolution, trap, printer). Proves harmless: T-ISO-1, 5, 6, T-FC-*, T-BIND-*.
3. Normalisation and classifiers: T-NRM, T-GIT, T-PSH, T-GH, T-MCP, T-SKL, T-ESC, T-TRN, T-TAM, T-COR.
4. Policy and messages: T-GRID, T-MSG.
5. Approval: T-APR.
6. Registration: T-REG, T-SPD.
7. Hand IR-1 to IR-7 to the claim feature. Build L2 only after B-CTX passes, using §19 rather than superseded MR 11.3 alternatives. Preserve foreign hooks and implement the isolated temporary-remote suite before any real launch.
```

### docs/designs/sc-issue-launch-level-hook.md:506-514

```markdown
**Current full-enforcement verdict:** B-CTX remains **OPEN/BLOCKING for the earlier plan's complete lifecycle coverage**. The owner authorized the new scoped integration; its per-job selector and isolated live Bash evidence are described in §19.7. That is not a retroactive PASS for the old controller-ancestry probe or for unobserved `/clear`, resume, Monitor, nested-subagent and auto-mode variants. Existing claim code still has no pipeline-launch implementation. Keep production activation conditional on the actual supported execution surfaces and their required observations, without a root service or weakening human isolation. O-22/O-21/O-13 are not reopened.

### 19.2 Placement and coexistence (Q1/Q2, narrowed)

The current run-4 merged artifacts prefer one owned shared `hooks/pre-push` plus a private-worktree marker, no config change, and no push-hook forwarding. Adopt this as the **conditional placement**, not the actor selector. Resolve common/private Git paths using Git, never assume `.git` is a directory. Existing `pre-commit`, `commit-msg` and other hook names remain untouched.

Install only if effective hooks lookup is the supported default, there is no foreign pre-push, and publication/self-test succeeds. Publish a complete executable without replacing an existing file, including a concurrent foreign install; recheck exact owned version/content before reuse. A header alone is not sufficient ownership proof. Do not enable `extensions.worktreeConfig`, migrate `core.hooksPath`, shadow foreign hooks, generate name-only stubs, or buffer/replay someone else's push hook in this increment.

Conflict or unsupported lookup: preserve all existing files/configuration; report `W-L2-ABSENT` with the reason. Unlike Q1/Q2's advisory 'continue claim', **do not launch a governed pipeline advertised as protected** when accepted L2 is absent. An ordinary/no-pipeline claim is unaffected. This preserves safety without silently treating a warning as O-22 compliance. A later request for coexistence beyond this boundary requires its own scoped design, not an automatic review loop.
```

### src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:722-725

```python
def enforcement_status() -> str:
    """``installed`` when the hook script exists and is executable, else ``missing``."""
    hook = home_dir() / HOOK_SCRIPT
    return "installed" if hook.is_file() and os.access(hook, os.X_OK) else "missing"
```

### src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:937-941

```python
    hook = enforcement_status()
    notes: list[tuple[str, str]] = []
    word = "full-submit" if args.submit else args.level
    try:
        nonce, pending = publish_pending(word)
```

### src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:986-989

```python
    if hook == "missing":
        notes.append(
            ("W-ENFORCEMENT-ABSENT", "the launch-level hook script is not installed")
        )
```

### src/superclaude/hooks/hooks.json:75-107

```json
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/freshness-pre-edit.sh",
            "timeout": 1
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/block-bare-python.sh",
            "timeout": 3
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude/hooks/launch-job-identity.sh",
            "timeout": 5
          }
        ]
      }
    ],
    "PostToolUse": [
```

### tests/cli/test_install_hooks.py:825-844

```python
@pytest.mark.parametrize("tree", ["src", "plugins"])
def test_real_hooks_json_registers_launch_identity_without_replacing_policy(tree):
    root = Path(__file__).resolve().parents[2]
    pre_tool = json.loads((root / tree / "superclaude/hooks/hooks.json").read_text())[
        "hooks"
    ]["PreToolUse"]
    entries = [
        reg
        for reg in pre_tool
        if any(h.get("command") == _LAUNCH_IDENTITY_HOOK for h in reg["hooks"])
    ]
    assert entries == [
        {
            "matcher": "Bash",
            "hooks": [
                {"type": "command", "command": _LAUNCH_IDENTITY_HOOK, "timeout": 5}
            ],
        }
    ]
    assert pre_tool[-1] == entries[0]
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001: implement the hook from the design | Task 22 (0.9167 containment); Tasks 3 to 13 carry the build | covered | .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:340 |
| INF-002: B-CTX gate is the first plan step | Task 1 | covered | .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:32 |
| INF-003: code scope hooks, install_hooks.py, orca_worktree.py, tests/hooks | Task 18 (0.9333 containment); Tasks 3 to 17 | covered | .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md:287 |
