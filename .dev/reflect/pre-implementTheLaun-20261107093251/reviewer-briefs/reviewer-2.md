## T1 card excerpt

```yaml
# Tier-1 reflection card (UC-1, pre-execution). Produced by the orchestrator inline (hypothesis_source: inline).
mode: pre
spec: .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md
tasklist: .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/TASK-WF-implementTheLaun-20261107-092804.md
driving_design: docs/designs/sc-issue-launch-level-hook.md
structural_signals:
  S_scope: 22            # tasklist items
  S_domains: 4           # code (hooks, cli, skill script), tests, docs, config (hooks.json)
  coverage_pct: null     # parsed-only: spec carries no labeled ids
  coverage_pct_union: 1.0
  coverage_degraded: parsed-sparse
  S_dev_density: 0.0
requirements:   # Step 1B.0 Pass 2, quote-pinned
  - {id: INF-001, quote: "Implement the launch-level enforcement hook for issue #394 from the design docs/designs/sc-issue-launch-level-hook.md", citation: ".dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md:1", matched_task: 22, ratio: 0.9167}
  - {id: INF-002, quote: "The B-CTX feasibility gate must be the first plan step.", citation: ".dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md:1", matched_task: 1, ratio: 0.8571}
  - {id: INF-003, quote: "Code: src/superclaude/hooks/, src/superclaude/cli/install_hooks.py, src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py, tests/hooks/.", citation: ".dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md:1", matched_task: 18, ratio: 0.9333}
```

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-07T09:33:00Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook projectPath=/home/coder/workspaces/worktrees/IronClaude/issue-394-launch-level-hook

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

### .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md:1-1

```text
Implement the launch-level enforcement hook for issue #394 from the design docs/designs/sc-issue-launch-level-hook.md, the requirements in .dev/brainstorms/20261105-170229-launch-level-hook/merged-requirements.md and .dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag/launch-levels-addendum.md, and the cheatsheet .dev/issues/394/issue-summary.md. The B-CTX feasibility gate must be the first plan step. Code: src/superclaude/hooks/, src/superclaude/cli/install_hooks.py, src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py, tests/hooks/.
```

### .dev/reflect/pre-implementTheLaun-20261107093251/artifacts/coverage-matrix.json:1-60

```json
{
  "parsed_ids": [],
  "parsed_count": 0,
  "inferred_count": 3,
  "coverage_pct": null,
  "coverage_pct_union": 1.0,
  "unmapped_requirements_union": [],
  "coverage_degraded": "parsed-sparse",
  "coverage_undefined": false,
  "task_count": 22,
  "S_dev_density": 0.0,
  "rows": [
    {
      "id": "INF-001",
      "source": "inferred",
      "quote": "Implement the launch-level enforcement hook for issue #394 from the design docs/designs/sc-issue-launch-level-hook.md",
      "citation": "source.md:1",
      "best_task": 22,
      "best_ratio": 0.9167,
      "match_method": "containment",
      "matched_task_ids": [
        22
      ]
    },
    {
      "id": "INF-002",
      "source": "inferred",
      "quote": "The B-CTX feasibility gate must be the first plan step.",
      "citation": "source.md:1",
      "best_task": 1,
      "best_ratio": 0.8571,
      "match_method": "containment",
      "matched_task_ids": [
        1
      ]
    },
    {
      "id": "INF-003",
      "source": "inferred",
      "quote": "Code: src/superclaude/hooks/, src/superclaude/cli/install_hooks.py, src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py, tests/hooks/.",
      "citation": "source.md:1",
      "best_task": 18,
      "best_ratio": 0.9333,
      "match_method": "containment",
      "matched_task_ids": [
        18
      ]
    }
  ]
}```

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

### docs/designs/sc-issue-launch-level-hook.md:296-337

```markdown
## 11. Test plan

`tests/hooks/test_launch_level_guard.py` (proposed) runs the real script with `subprocess.run`, a temporary `HOME` and a controlled `PATH`, like `test_block_bare_python.py`. Oracle `EXPECTED` is hand-written from section 4. Observed checks are `pytest.skip(...)` bodies. Run `uv run pytest tests/hooks/ -v`. Every T- id of MR 8.2 is built; minimum per AC:

| AC | Cases |
|---|---|
| AC-1 | T-GRID-3, T-SKL-1, T-APR-5, T-APR-9, T-NRM-8, T-GIT-18 |
| AC-2 | T-GRID-4, T-GRID-5, T-GIT-17, T-PSH-8, T-PSH-11, T-GH-12 |
| AC-3 | T-APR-1 to T-APR-4, T-APR-10, T-TRN-1, T-TRN-4 |
| AC-4 | T-ISO-1, T-ISO-4, T-ISO-7, T-ISO-8, T-ISO-9, T-REG-3 |
| AC-5 | T-BIND-2, T-BIND-7, T-BIND-13, T-TAM-1, T-TAM-2, T-TAM-6, T-FC-2 |
| AC-6 | T-PSH-4, T-PSH-12, T-GIT-9, T-GIT-14, T-NRM-1, T-GH-2, T-GH-11, T-GH-14, T-MCP-1, T-COR-2 |
| AC-7 | T-MSG-1, T-MSG-2, T-MSG-3, T-FC-3 |
| AC-8 | T-GRID-1, T-GRID-2, T-SPD-1..5, T-COR-1, T-GAP-1 |

**Corpus.** Preserve MR section 8 (8.3/8.4) case inputs and historical outcomes as baseline provenance, but do not copy obsolete expected results unchanged (revised DD-2). Explicit overrides here: top-level typed JSON dispatch, identity-loss ordinary allowance instead of store-wide W, removal of the 64-id early allow, exact/no-replacement state publication, nonempty PR repo operands, and combined L2 protected-destination checks. Add panel F1–F8 regression cases and maintain a hand-written current oracle; report each intentional override rather than claiming MR was synchronized. Categories: push routes (T-ATK-1, 13, 25, 29, 50); aliases and variable subcommands (T-ATK-10, 35, 42); `gh api` writes (T-ATK-6, 18, 47); merges (T-ATK-48, 49, 51); tamper and escape (T-ATK-21, 55, 60); accepted leaks pinned `allow` (T-ATK-26 to 28, N-ATK-7, 31, 36); benign (T-OK-1 to 36); pinned over-blocks (T-OVR-1 to 6); amendment attacks (N-ATK-1 to 39). T-COR-2 replays the rows MR marks "real" on a temporary bare remote.

**Observed checks.**

- **OB-H1** (first; log-only hook). Records: (1) subagent and nested-subagent `session_id`, `agent_id`, `agent_type` (U1); (2) Skill keys, name form (U2); (3) Agent name, `isolation` (U3, U13); (4) typed `/sc:implement x` (O-4); (5) exact `prompt` of a Monitor line `approved` and of background-Bash and background-subagent notices (U4, O-17); (6) `TaskCreate` versus the anchored matcher (U15); (7) SendMessage, MCP names (U12); (8) `claude` without `-p` (U14); (9) Bash, Edit, Write, Skill names (U21).
- **OB-H2** (after the claim feature ships). Session file before the first tool call (U8); exact first prompt and marker position (U7); hook `HOME` and `CLAUDE_CONFIG_DIR`; IR-4 refusals; LL-NOBIND visibility (U20).
- **OB-H3** (test issue, each level, after all prior gates). `W` stops and unlocks by both routes; `F` logs git commands (U10); `FS` runs one authorized `/sc:pr-submit --monitor 3` cycle logging pushes and inline `gh api` (O-18, O-19) and a conflict (O-10). Protected-push/merge refusal tests use disposable repositories, never an actual protected branch on the fork. L2 observation follows §19.5. Count LL-PUSH-FORM, LL-GH-WRITE, LL-TEXT and NM1a/G2 UNKNOWN; separately count **am-only blocked first attempts and retries** before any O-21 reconsideration. Record Orca preamble (O-11), one live message (AC-7), timing, and exact harness/config versions. A skipped observation remains pending, not passed.
- **OB-CTX** is the first blocking feasibility check described in §19.1. Extend OB-H1/H2 capture to valid top-level event/id types on every supported governed leaf call. No probe or observation in this specification has been executed by this panel.

## 12. Acceptance criteria map

**Historical matrix only:** these verdicts belong to `plan-review-3.md` before this panel, not to the current refined design. Its reviewer tested an amended prototype; this panel reviewed/refined the design without rerunning executable behavior. No current AC has a runtime pass here. The earlier wording 'unreviewed' below records that historical review boundary.

| AC | Historical verdict | Earlier amendments (then unreviewed) | Historical remaining issues |
|---|---|---|---|
| AC-1 | NOT MET | B-1, B-2, B-3 close one-line commit, merge, push routes | built names (R1), R9, O-8 |
| AC-2 | NOT MET | B-3 redirect keys, B-4 `.config/git`, B-10 retry block | O-10, O-18, O-19, O-21 |
| AC-3 | NOT MET | B-1 makes `tm\`, `or\` spellings UNKNOWN | U4, O-17, R16 |
| AC-4 | MET WITH CAVEAT | none (U21 added) | OB-H1 item 1, else O-9 |
| AC-5 | NOT MET | B-1, B-2 close N-ATK-29, 30, 32, 33; B-9 reinstall | R3, O-16, N-ATK-31 |
| AC-6 | NOT MET | B-1 to B-4, B-7; copy blocked 35 of 38 | R1, R11; O-22 |
| AC-7 | MET | B-1, B-7 wording | none |
| AC-8 | MET WITH CAVEAT | amendment corpus added | only corpus routes shown; speed untimed |

**Current acceptance additions (all pending execution):** AC-4 requires concurrent governed/ordinary actors in the same worktree, including a human terminal, with no marker-removal workaround. AC-5 requires no-replacement binding, exact state reads and ordinary isolation under identity loss, with that fail-open limit stated. AC-6 requires actual field-3 L2 checks only after B-CTX; scripts/aliases using ordinary Git push are covered only if actor selection demonstrably follows them. AC-8 adds F1–F8 boundary regressions and all §19.5 lifecycle/fixture checks. Acceptance is limited to tested routes; local hooks do not establish universal no-merge/no-main-write protection. B-CTX blocks declaring the complete feature ready, independently of any old MET label.

## 13. Registration, install and claim-feature interface requests
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|--------------------|---------|--------|-----------|
| INF-001 | Task 22 | covered (containment 0.9167) | .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md:1 |
| INF-002 | Task 1 | covered (containment 0.8571) | .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md:1 |
| INF-003 | Task 18 | covered (containment 0.9333) | .dev/tasks/to-do/TASK-WF-implementTheLaun-20261107-092804/source.md:1 |
