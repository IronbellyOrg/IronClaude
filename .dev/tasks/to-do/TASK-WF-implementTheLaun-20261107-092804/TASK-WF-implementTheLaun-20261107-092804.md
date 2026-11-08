---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: deep
slug: TASK-WF-implementTheLaun-20261107-092804
version: "1"
priority: Medium
created_date: "2026-11-07"
---

# Launch-level enforcement hook for claim-launched agents (issue #394)

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
- Gate: Task 1 writes the B-CTX verdict. If ./artifacts/b-ctx-verdict.md contains the line "L1: STOP", stop the run at Task 1 and report that verdict; do not start Task 2 or any later task. Every task after Task 1 depends on that verdict.
- Existing tests: any task that changes a check in src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py also migrates the shared test fixture launch_scene in tests/skills/test_issue_orca_worktree.py (it writes only a bare shell stub today) and names every test whose result changes. Test code must unset CLAUDE_CONFIG_DIR and control which jq is on PATH, so results do not depend on the developer's machine.
- Edit only under src/superclaude/, plugins/superclaude/hooks/, tests/, docs/ and this package's ./artifacts/; run make sync-dev after hook or skill edits. The plugin copy of every hook script and hooks.json stays byte-identical to its src copy. Generated .claude/ mirrors made by make sync-dev stay out of the commit.
- UV only: run tests with uv run pytest.
- Findings of the issue analysis that this plan answers: F2 (Task 15), F3 (Task 14), F4 (Tasks 18 to 20), F6 (Task 22), F7 (Task 1). F5 (pending records are not pruned) is accepted under owner decision O-15 and is stated in Task 22.

## Phase 1: Feasibility gate and observation scaffolding

## Task 1: Write the B-CTX feasibility verdict

Create ./artifacts/b-ctx-verdict.md. This is the design's step 0 (design sections 14 and 19.1): decide from evidence that already exists what the guard may rely on and what must wait. Evidence to read and cite by path and line: .dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/artifacts/live-harness-events.jsonl and identity-integration-evidence.md, tests/hooks/test_launch_job_identity.py, the header of src/superclaude/hooks/scripts/launch-job-identity.sh, and design sections 19.1 and 19.7.

The file has four parts. First, an evidence table with one row for every lifecycle case listed under "OB-CTX / B-CTX completion evidence" in design section 19.1 (main session, subagent, nested subagent, background Bash or Monitor to Git, same-worktree human terminal, ordinary Claude session, detached or reparented job, launch wrapper, process exit and PID reuse, resume in a new process, /clear and fork, release while a job is alive), each marked observed (cite the artifact line), simulated (cite the test) or unobserved. Second, an L1 verdict line, either "L1: PROCEED" or "L1: STOP", with the reason; the L1 text guard identifies a session by its top-level session_id, so B-CTX does not block writing it, and the ship gate U1 (design section 7) stays pending. Third, an L2 verdict line, either "L2: GO" or "L2: BLOCKED"; GO only if every required case is observed, otherwise BLOCKED with the exact missing launcher or harness integration named. Fourth, the F7 result: state whether .dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md and the four answers under .dev/brainstorms/20261106-l2-prepush-decisions/ exist in this tree, and list each design statement that depends on a missing file as unverified.

No new probe is run against a live session by this task. The file states in one sentence that the verdict is an evidence review and not the live probe of design section 14 step 0, and it names the existing opt-in probe tests/hooks/fixtures/launch_level/live_probe.py as the way a person can run the live observation later.

Acceptance criteria:
- ./artifacts/b-ctx-verdict.md exists and contains the four parts above, with every row of the design 19.1 case list present.
- Every row marked observed cites an existing path and line of evidence; every case without such a citation is marked unobserved or simulated, never observed.
- The file contains exactly one line starting "L1:" and exactly one line starting "L2:", each with one of the allowed values.
- If the L2 line says BLOCKED, the file names the missing integration in one or more sentences a maintainer can act on.
- The F7 part lists the existence check result for the five named files and no file is invented or recreated.

## Task 2: Add the observation fixtures, the log-only probe and the pending-observation tests

Depends on: Task 1

Create tests/hooks/fixtures/launch_level/ob_h1/ with one fixture file per OB-H1 item of design section 11, named item<n>-<shape>.json (DD-6): item 1 subagent and nested-subagent session_id, agent_id, agent_type; item 2 Skill input keys and name form; item 3 Agent name and isolation; item 4 a typed /sc:implement prompt; item 5 a Monitor line "approved" and background Bash and background subagent notices; item 6 TaskCreate against the anchored matcher; item 7 SendMessage and MCP names; item 8 claude without -p; item 9 Bash, Edit, Write and Skill tool names. Each is a synthetic payload in the documented hook input shape (top-level hook_event_name, session_id, tool_name, tool_input). Add tests/hooks/fixtures/launch_level/ob_h1/README.md saying every fixture is synthetic and listing, per item, what a real observation must capture.

Reuse the existing opt-in probe tests/hooks/fixtures/launch_level/live_probe.py where it already captures an item, and do not duplicate it. Create tests/hooks/fixtures/launch_level/ob_h1/log-only-probe.sh: a bash script that appends the stdin JSON as one line to the file named by the LAUNCH_LEVEL_PROBE_LOG environment variable and always exits 0, so it can be registered by a person for a real observation without ever blocking.

Create tests/hooks/test_launch_level_observations.py containing: real tests that the probe appends exactly one line per call, exits 0 when the log path is unwritable or unset, and never writes to stdout; and one skipped test per pending observation (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX) whose skip reason names the item and says it needs a real governed session and has not been run.

Acceptance criteria:
- tests/hooks/fixtures/launch_level/ob_h1/ holds nine item<n>-<shape>.json files that parse as JSON objects with a string hook_event_name, plus README.md and log-only-probe.sh (executable).
- uv run pytest tests/hooks/test_launch_level_observations.py -v shows the probe tests passing and exactly twelve skipped tests (nine OB-H1 items, OB-H2, OB-H3, OB-CTX), each with a reason that contains the item name.
- Running the probe with LAUNCH_LEVEL_PROBE_LOG unset prints nothing and exits 0.

## Phase 2: Guard core: script skeleton, binding and resolution

## Task 3: Create the guard script skeleton, messages and test harness

Depends on: Task 1

Create src/superclaude/hooks/scripts/launch-level-guard.sh (executable, first line #!/bin/bash) following the ten-part layout of design section 2 (DD-1): settings (LC_ALL=C, set -u -o pipefail, set -f, umask 077, no set -e, no ERR trap); the store path built from three literal parts so the script text never contains the string .claude/state (FR-L-01, T-TAM-8); the message table; dispatch on the parsed top-level hook_event_name equal to UserPromptSubmit or PreToolUse only (FR-L-08); the prompt branch and tool branch as stubs that allow; the empty-store fast exit using one directory test; an EXIT trap mapping any other exit code to LL-BROKEN (LL-NOBIND in the prompt branch); and a last line that denies with LL-BROKEN, exit 2. Add a line exactly "# launch-level-guard-version: 1" in the first ten lines; Task 18 reads it.

Messages: print every id of the design section 9 table (LL-IMPL, LL-COMMIT, LL-PUSH, LL-PUSH-FORM, LL-PROTECTED, LL-MERGE, LL-GH-WRITE, LL-SUBMIT, LL-REPO, LL-UNKNOWN, LL-MCP, LL-ESCAPE, LL-TURN, LL-TAMPER, LL-SKILL, LL-BIG, LL-BROKEN, LL-NOBIND) to stderr with the header "Launch-level guard: this session was started by /sc:issue --claim at level {level}." and the Blocked, Why and You can lines worded exactly as in that table; level names worktree, worktree (approved), full, full --submit; variables {level}, {store}, {sid} only; LL-NOBIND and LL-BROKEN print "Launch-level guard:" alone when the level is unknown; LL-TAMPER uses the LL-BROKEN wording when the session id is invalid; notes LL-STATE then LL-TEXT after the lines, only on a block. Amendment marks like B-1 are never printed (DD-3).

Create tests/hooks/test_launch_level_guard.py with the harness of tests/hooks/test_block_bare_python.py (real script through subprocess, temporary HOME, controlled PATH) and the first cases: ordinary session with no store allows silently; every message id prints the exact design text; the script text does not contain .claude/state; the script is executable and carries the version line; an event name other than the two allowed ones is handled by the identity-loss rule of design section 3.

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard.py -v passes for the cases above, with the header, LL-BROKEN and LL-NOBIND checked against the design section 9 text. The other sixteen ids are asserted where their class becomes reachable (Tasks 5 to 11) and in Task 17; this task only requires that the printer holds all eighteen texts.
- grep for the string .claude/state in the script returns no match, and the file passes bash -n.
- With HOME pointing at an empty temporary directory, any valid hook payload exits 0 with empty stdout and stderr.
- A payload whose hook_event_name is neither UserPromptSubmit nor PreToolUse exits 0 without output when no governed session is positively identified.

## Task 4: Implement session binding on the first prompt

Depends on: Task 3

In src/superclaude/hooks/scripts/launch-level-guard.sh fill the UserPromptSubmit branch with the binding rules of design section 3 (FR-L-09 as revised B1 to B13, O-20) and the state rules of FR-L-01 to FR-L-07. The store is ~/.claude/state/launch-level/ with pending/<nonce> (name matches ^[0-9a-f]{32}$, content one word: worktree, full or full-submit), sessions/<sid> and sessions/<sid>.ok. A valid session id is a top-level JSON string matching ^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$; numbers and objects are never coerced. A strict marker is the first match of \[sc-launch:v1:([0-9a-f]{32})\] anywhere in the prompt; a loose marker is a prompt that starts, after whitespace or a byte-order mark, with [sc-launch:. A nonempty string agent_id makes the prompt branch exit 0 without binding. No marker and no session records allows the empty-store fast exit. Create the store directories with mkdir -p under umask 077; pending, session and approval entries must be regular, non-symlink files in directories owned by the user.

Binding order: read and parse the envelope once; an unparseable envelope or missing jq with a recognizable launch-marker prompt blocks with LL-NOBIND (no inferred binding); an invalid session id with a marker blocks with LL-NOBIND; an already bound session keeps its level (a newly supplied pending nonce may be consumed and its record removed); an unbound session with no marker is allowed; otherwise consume one pending nonce once and publish sessions/<sid> atomically without replacing an existing file (for example by writing a complete temporary file and linking it into place, which fails when the target exists), and when publication loses a race re-read the winner. A missing or already used nonce with a leading loose marker publishes the word degraded under the same no-replacement rule; a strict marker found only in the middle of a prompt with no usable record blocks with LL-NOBIND; a malformed marker in the middle is ignored. A read-only sessions directory blocks with LL-NOBIND.

Extend tests/hooks/test_launch_level_guard.py with every T-BIND case of MR section 8.2 and the T-ISO and T-FC cases that concern binding, plus a concurrency test that starts at least eight guard processes at once on the same session id and nonce and asserts exactly one binding survives, no sessions/<sid> is overwritten, and every loser reads back the winner's level.

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard.py -k "bind or BIND" -v passes, covering strict and loose markers, reused nonce giving degraded, new marker in a bound session, read-only sessions directory, invalid id, agent_id prompt, and a malformed mid-prompt marker being ignored.
- The concurrency test passes ten consecutive runs.
- After a successful bind the file sessions/<sid> holds exactly one of worktree, full, full-submit or degraded, and the consumed pending file no longer exists.
- No code path overwrites an existing sessions/<sid>: a test that pre-creates the file with another word and then binds shows the pre-existing word unchanged.

## Task 5: Implement resolution, the policy grid and the Skill classifier

Depends on: Task 4

In src/superclaude/hooks/scripts/launch-level-guard.sh fill the PreToolUse branch with the resolution rules of design section 3 (FR-L-10 as revised P1 to P7, FR-L-11 to FR-L-14, identity loss) and the policy grid of section 4 (FR-L-20, FR-L-21).

Resolution: with an empty session store allow; otherwise one jq extraction of the top-level fields (session id, hook_event_name, tool_name and the typed tool_input fields, command kept as a string); remove the fixed-64 raw-id early-allow loop of MR. A nonstring tool field or an embedded NUL is an input error. skill is used if present and non-null, otherwise name; an explicit empty string stays empty and yields SKILL; the file-path fallback follows the same missing-or-null rule. A valid unbound id allows silently; a valid bound id reads its exact level from sessions/<sid> (exactly one allowed word plus an optional newline; empty, malformed or unreadable means worktree with the LL-STATE note on a block); sessions/<sid>.ok existing at worktree gives the worktree (approved) level. Missing or invalid id, or an unparseable envelope, without independent positive binding evidence allows without claiming enforcement (design section 3 identity loss); a positively identified governed input error or internal failure blocks with LL-BROKEN; jq missing with a positively bound session blocks LL-BROKEN. agent_id is not read on PreToolUse and no cwd fallback exists (FR-L-13, FR-L-14).

Policy: one literal case on CLASS:LEVEL implementing the grid of design section 4 for all sixteen classes and the four levels (W, WA, F, FS), message precedence BIG, TAMPER, MERGE, GHWRITE, PROTECTED, ESCAPE, MCP, UNKNOWN, SUBMIT, REPO, PUSH, PUSHFORM, COMMIT, TURN, IMPL, SKILL, and any blocked class blocking the whole call.

First classifier, FR-L-40: for the Skill tool take name via the skill-else-name rule, strip leading space, keep the first word, lower-case, drop one leading slash, keep the text after the last colon, drop one leading sc- and one trailing -protocol. implement, task, improve, cleanup, spawn, build give IMPL (owner decision O-13); pr-submit gives SUBMIT; issue gives ESCAPE; empty gives SKILL; anything else gives NONE (cleanup-audit and task-builder stay NONE).

Extend tests/hooks/test_launch_level_guard.py with the T-SKL cases, the T-ISO and T-FC cases that concern resolution, the identity-loss cases (missing id, invalid id, numeric id, nested forged id, unparseable envelope) and a hand-written oracle dictionary EXPECTED for the Skill rows of the grid across the four levels.

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard.py -v passes the Skill grid rows: at W the Skill sc:implement call exits 2 with LL-IMPL, at WA, F and FS it exits 0; pr-submit exits 2 with LL-SUBMIT at W, WA and F and exits 0 at FS; issue exits 2 with LL-ESCAPE at every level; an empty skill name exits 2 with LL-SKILL at W, WA and F and 0 at FS.
- A session file containing garbage blocks a Skill sc:implement call at W with the LL-STATE note, and the same call is allowed when sessions/<sid>.ok exists.
- A payload with a missing or invalid session id and a nonempty store exits 0 and prints nothing, and a test comment states it is a declared fail-open limit.
- With jq removed from PATH, a bound session blocks with LL-BROKEN and an unbound session is allowed.

## Phase 3: Command and tool classification

## Task 6: Implement Bash and Monitor normalisation

Depends on: Task 5

In src/superclaude/hooks/scripts/launch-level-guard.sh add the Bash and Monitor normalisation of design section 5.1 (FR-L-22 to FR-L-27, FR-L-44): cmd is the decoded tool_input.command of a Bash (foreground or background) or Monitor call; a Monitor call with only ws is NONE; no parameter-expansion substitution over the command text. Steps in order: NM1 a command over 65536 bytes gives BIG and stops; NM1a a backslash-newline continuation inside a word (the test [[ $cmd =~ $'[^[:space:]\\\\]\\\\\n' ]]) gives UNKNOWN; NM2 and NM3 build T with the sed expression of the design; NM4 builds G; NM5 and NM6 build W; segments are always split with IFS=';' read -r -a segs and words with ws=($seg) under set -f; NM7 basename is the text after the last slash. Use the exact sed and tr expressions printed in design section 5.1.

Extend tests/hooks/test_launch_level_guard.py with every T-NRM case of MR section 8.2 and the T-FC-7 multi-byte size case (65537 bytes of multi-byte text gives BIG), asserting the resulting class through the observable outcome (block id) at the level where it differs from NONE.

Acceptance criteria:
- A governed Bash call over 65536 bytes exits 2 with LL-BIG at every level, and one of exactly 65536 bytes does not.
- The in-word continuation spellings of cases B-1 in design section 4 (for example gi, backslash, newline, t push) exit 2 with LL-UNKNOWN at every level.
- The normalisation uses exactly one sed and four tr invocations for a Bash command and one sed for an edit path (counted in a test by running the script with a PATH of counting wrappers).
- uv run pytest tests/hooks/test_launch_level_guard.py -k "NRM or nrm" -v passes.

## Task 7: Implement git classification and the canonical push check

Depends on: Task 6

In src/superclaude/hooks/scripts/launch-level-guard.sh add the git rules of design section 5.1: the G0 word definitions (git word, gated COMMIT, PUSH and MERGE words including git-<name> forms), the G1 global rule applied to G, G2 (alias, pushurl, insteadof, hookspath, remote., url., include., includeif. and set-url give UNKNOWN), G3 command position (skipped NAME=value words, options, numeric words, wrappers env sudo nohup exec command builtin timeout xargs setsid time nice stdbuf ionice doas unbuffer eval, shells with a -c flag, reserved words if then else elif do while until coproc) with the subcommand table of the design (none, NONE, COMMIT, MERGE, PUSH and UNKNOWN rows including the long read-only list and the remote, config and worktree list exceptions), and G4 (a dollar sign in the subcommand after any git word adds UNKNOWN; a value-taking option with no following value adds UNKNOWN). Add the canonical push check (FR-L-33, FR-L-34): any call with PUSH tests the raw command against the anchored expression printed in design section 5.1; no match gives PUSHFORM; a match takes the destination (capture 5, else capture 3, minus one refs/heads/ or heads/ prefix); master or main gives PROTECTED; HEAD gives PUSHFORM.

Extend tests/hooks/test_launch_level_guard.py with the T-GIT and T-PSH cases of MR section 8.2, the accepted and rejected push lists PA1, PA4, PA6, PR1, PR3, PR6, PR13, PR15, PR24 and PD1, and the hand-written oracle rows for COMMIT, PUSH, PUSHFORM, PROTECTED, MERGE and UNKNOWN across W, WA, F and FS.

Acceptance criteria:
- At FS: git push origin feature, git push -u origin feature and git push origin 3f2a9c1e:feature/x exit 0; git push, git push --force origin f, git push origin f piped to tail, and cd x && git push origin a:b exit 2 with LL-PUSH-FORM; git push origin main and git push -u origin feature:main exit 2 with LL-PROTECTED.
- At W, WA and F every git push form exits 2 (LL-PUSH, LL-PUSH-FORM or LL-PROTECTED as the grid says) and git commit -m x exits 2 with LL-COMMIT; at FS git commit -m x exits 0.
- git merge x, git pull and git log --grep merge exit 2 with LL-MERGE at every level, and the LL-TEXT note is printed for the text-derived ones.
- git status, git diff, git log and git -C "$(git rev-parse --show-toplevel)" status exit 0 at every level.
- uv run pytest tests/hooks/test_launch_level_guard.py -k "GIT or PSH or git or push" -v passes.

## Task 8: Implement gh, curl and API classification

Depends on: Task 7

In src/superclaude/hooks/scripts/launch-level-guard.sh add the gh rules of design section 5.1 (FR-L-35 to FR-L-39): H1 group and action words (skipping -R and --repo values), H2 the gh api rule (GHWRITE unless the raw command matches the anchored read-only expression, no word after api matches the method, field or input options, and the endpoint exists, is not graphql and does not end /merge or /merges), H3 the first-match table (api no class; help or version NONE; merge, update-branch and sync give MERGE anywhere; alias and extension groups and any dollar sign give UNKNOWN; the read-only groups and actions give NONE; pr create, pr edit, pr comment, pr ready, issue create, issue edit and issue comment give SUBMIT anywhere; else UNKNOWN in command position), H4 each recognized pr create occurrence needs a nonempty operand after -R or --repo (or --repo=value) in its own segment, otherwise REPO, and H5 when no gh word is present a word with repos/ ending /merge or /merges gives MERGE and a word containing api.github.com or uploads.github.com gives GHWRITE. Print the LL-TEXT note when the class came from Bash or Monitor text.

Extend tests/hooks/test_launch_level_guard.py with the T-GH cases of MR section 8.2 and the oracle rows for SUBMIT, REPO and GHWRITE across the four levels.

Acceptance criteria:
- gh api repos/o/r/pulls/5 --jq .state exits 0 at every level; gh api -X POST repos/o/r/merges, gh api graphql with any query, and curl -X PATCH https://api.github.com/repos/o/r exit 2 with LL-GH-WRITE at every level.
- gh pr create --repo o/r --title x exits 2 with LL-SUBMIT at W, WA and F and 0 at FS; gh pr create --title x exits 2 with LL-REPO at FS.
- gh pr merge 5 and gh repo sync exit 2 with LL-MERGE at every level; gh pr view 5 and gh pr checks exit 0.
- gh alias set co with a merge value exits 2 with LL-UNKNOWN.
- uv run pytest tests/hooks/test_launch_level_guard.py -k "GH or gh" -v passes.

## Task 9: Implement tamper and escape classification

Depends on: Task 8

In src/superclaude/hooks/scripts/launch-level-guard.sh add the tamper rules (FR-L-49 to FR-L-51) and escape rules (FR-L-47, FR-L-48) of design section 5.1 and the Edit-tool part of section 5.2. Tamper: T, or an edit path after the same slash squeeze, containing .claude/state, .claude/settings, .claude/hooks, disableAllHooks, .gitconfig, .git/config or .config/git; Bash only: a word ending .claude or .claude/, a superclaude word followed later in its segment by install, a word containing install_hooks; Edit, Write and NotebookEdit only: a parent-directory segment or trailing parent-directory path. Contents, prompts and arguments are never checked. Edit, Write and NotebookEdit apply the tamper check only (FR-L-42, source edits are not gated, O-8). Escape: orca is NONE when the segment ends --help or -h, the first word is status, help or --version, or the first two words are worktree current, worktree list, worktree show, terminal list, terminal show, terminal read, or orchestration check, inbox, run-current, task-list, worker-show; any other orca word is ESCAPE; ccsession words are ESCAPE; claude and claude-code (basename cut at @) are ESCAPE when any word in the command is one of -p --print --continue --resume --bare --settings --dangerously-skip-permissions --fork-session --session-id --permission-mode; tmux, screen, xdotool and ydotool are ESCAPE.

Extend tests/hooks/test_launch_level_guard.py with the T-TAM and T-ESC cases of MR section 8.2 and the oracle rows for TAMPER and ESCAPE across the four levels.

Acceptance criteria:
- A governed Edit of ~/.claude/settings.json, a Write of ~/.config/git/config, and a Bash rm -rf ~/.claude/state exit 2 with LL-TAMPER at every level; an Edit of a source file under src/ exits 0; a Write whose content only quotes .claude/hooks exits 0.
- npx -y @anthropic-ai/claude-code@latest -p x, claude -p x, tmux send-keys approved Enter, and orca terminal send exit 2 with LL-ESCAPE at every level; orca worktree list and orca status exit 0.
- The LL-TAMPER message for a bound session includes the exact rm command naming the store and the session id, and for an invalid id uses the LL-BROKEN wording.
- uv run pytest tests/hooks/test_launch_level_guard.py -k "TAM or ESC or tamper or escape" -v passes.

## Task 10: Implement the remaining tool classifiers and the full grid oracle

Depends on: Task 9

In src/superclaude/hooks/scripts/launch-level-guard.sh add the classifiers of design section 5.2 not yet built: Agent and Task (FR-L-41) are NONE, background or not, unless isolation is remote (ESCAPE), and the prompt is never scanned; CronCreate, CronDelete, CronList and the Schedule tools give TURN (FR-L-43); RemoteTrigger, Workflow and SendMessage give ESCAPE (FR-L-46); MCP tools (FR-L-45) take N as the text after the last double underscore, lower-cased: no keyword from merge, push, commit, pull_request, create_or_update_file, delete_file, update_ref, create_ref, create_branch gives NONE, the prefixes list_, get_, search_ and read_ give NONE, a name holding merge gives MERGE, anything else gives MCP; anything else matched (FR-L-52) is NONE on an explicit allow path. The script re-checks tool names itself because the registration matcher anchors are unverified (FR-L-66, U15).

Extend tests/hooks/test_launch_level_guard.py with the T-TRN, T-MCP, T-COR and T-GAP cases of MR section 8.2 and complete the hand-written oracle EXPECTED so it covers all sixteen classes across W, WA, F and FS by driving real tool calls (T-GRID-1 to T-GRID-5), checking that every class has a test row and that the oracle is written independently of the script's case statement.

Acceptance criteria:
- CronCreate and ScheduleWakeup exit 2 with LL-TURN at W and exit 0 at WA, F and FS; a local Agent call exits 0 at every level; an Agent call with isolation remote, a Workflow call and a SendMessage call exit 2 with LL-ESCAPE.
- An MCP tool named mcp__github__merge_pull_request exits 2 with LL-MERGE, mcp__github__push_files exits 2 with LL-MCP, and mcp__github__list_issues exits 0.
- The pinned gaps of design section 4 row 33 (a variable-built git word, a bracketed binary name, a script file) exit 0 and their tests are marked as accepted leaks.
- uv run pytest tests/hooks/test_launch_level_guard.py -k "GRID or TRN or MCP or COR or GAP" -v passes, and the test module fails if any class in the grid has no oracle row.

## Phase 4: Human approval

## Task 11: Implement typed approval at the worktree level

Depends on: Task 10

In src/superclaude/hooks/scripts/launch-level-guard.sh add the approval rules of design section 6 (FR-L-15 to FR-L-19) to the UserPromptSubmit branch. The event is UserPromptSubmit only (O-4). A prompt matches when the whole prompt, trimmed and lower-cased, matches ^approved[.!]?$, or its first line matches ^/(sc:implement|sc:task|task)([[:space:]]|$); /task-builder, /tasks, /sc:implement-protocol, "please approved", "approved, but" and /sc:pr-submit do not match. Approval is written only for a bound session, a payload without agent_id, and a level of worktree (or an invalid word including degraded): touch sessions/<sid>.ok. At full and full-submit nothing is written. The effect is the WA level, which unlocks IMPL and TURN but never COMMIT, PUSH, SUBMIT or MERGE; a failed touch shows later as LL-IMPL; approval lasts until a person deletes the files (O-6). The prompt event runs before expansion, so the approval file exists before a Skill sc:implement-protocol call (T-APR-9 asserts the order with typed prompt then Skill call).

Extend tests/hooks/test_launch_level_guard.py with every T-APR case of MR section 8.2 and the T-TRN cases that depend on approval.

Acceptance criteria:
- At W: the prompt approved, the prompt /sc:implement x, and the prompt /task y each create sessions/<sid>.ok and exit 0; /task-builder x, please approved and approved, but create nothing.
- A prompt carrying agent_id creates nothing; at full and full-submit approved creates nothing.
- After approval a Skill sc:implement call exits 0 and git commit -m x, git push origin feature and gh pr create --repo o/r --title x still exit 2.
- A read-only sessions directory leaves no .ok file and the next Skill sc:implement call exits 2 with LL-IMPL.
- uv run pytest tests/hooks/test_launch_level_guard.py -k "APR or approval" -v passes.

## Phase 5: Registration, installer and packaging

## Task 12: Register the guard on both events in hooks.json

Depends on: Task 11

Edit src/superclaude/hooks/hooks.json and plugins/superclaude/hooks/hooks.json (byte-identical to each other where they are today) as specified in design section 13 (FR-L-60 to FR-L-66): append to UserPromptSubmit one entry whose hook is the command ~/.claude/hooks/launch-level-guard.sh with timeout 5; append to PreToolUse one entry with the matcher regular expression printed in design section 13 and the same command and timeout. Existing entries, including Bash block-bare-python.sh and Bash launch-job-identity.sh, stay unchanged. Insert the new PreToolUse entry before the launch-job-identity.sh entry so that entry remains the last PreToolUse registration, which tests/cli/test_install_hooks.py (test_real_hooks_json_registers_launch_identity_without_replacing_policy) asserts. No UserPromptExpansion, SessionStart or onFailure registration is added.

Add tests to tests/cli/test_install_hooks.py (or a new tests/hooks/test_launch_level_guard_registration.py) that read both hooks.json files and assert: the guard appears exactly once under UserPromptSubmit and once under PreToolUse with timeout 5; the PreToolUse matcher equals the design string; no onFailure key; the Bash entries for block-bare-python.sh and launch-job-identity.sh are still present; the set of commands registered with the literal matcher Bash in tests/hooks/test_freshness_subagent_start_policy.py is unchanged (the guard's matcher is not the literal Bash).

Acceptance criteria:
- src/superclaude/hooks/hooks.json and plugins/superclaude/hooks/hooks.json both contain the two guard registrations and are identical to each other.
- uv run pytest tests/cli/test_install_hooks.py tests/hooks/test_freshness_subagent_start_policy.py -v passes without any edit to the existing launch-identity registration test.
- The new registration test compiles the PreToolUse matcher as a regular expression and asserts it matches the tool names Bash, Skill, Agent, Task, Edit, Write, NotebookEdit, Monitor, Workflow, RemoteTrigger, SendMessage, CronCreate, ScheduleWakeup and mcp__x__merge_pull_request, and does not match Read, Grep, Glob or TaskCreate.

## Task 13: Ship the guard through the installer and the plugin mirror

Depends on: Task 12

Add "launch-level-guard.sh" to _FRESHNESS_SCRIPTS in src/superclaude/cli/install_hooks.py (the Makefile needs no change because make verify-sync imports that list). Copy src/superclaude/hooks/scripts/launch-level-guard.sh to plugins/superclaude/hooks/scripts/launch-level-guard.sh byte for byte with the executable bit. Add the name to the fake-script list at the top of the fixture in tests/cli/test_install_hooks.py (the list that already holds launch-job-identity.sh). Add tests in tests/cli/test_install_hooks.py modelled on test_launch_identity_script_is_packaged_listed_executable_and_mirrored and test_launch_identity_real_install_preserves_policies_and_is_idempotent: the script is listed, executable, byte-identical to its plugin mirror and starts with #!/bin/bash; a real install into an isolated HOME registers the guard under both UserPromptSubmit and PreToolUse exactly once, preserves permissions, user hooks and the other managed registrations, is idempotent on a second install with and without force, and copies a byte-identical executable script to ~/.claude/hooks/. If the merge logic in _merge_settings cannot register one command under two events or refreshes it by matcher alone, make the smallest change in install_hooks.py that registers and refreshes by exact command identity per event, and add a test for that case.

Run make sync-dev and then make verify-sync.

Acceptance criteria:
- uv run pytest tests/cli/test_install_hooks.py -v passes, including the new guard tests.
- make verify-sync exits 0 and its Installer Registration section reports no script missing from _FRESHNESS_SCRIPTS.
- diff of src/superclaude/hooks/scripts/launch-level-guard.sh and plugins/superclaude/hooks/scripts/launch-level-guard.sh prints nothing.
- A second install into the same isolated HOME leaves settings.json byte-identical to the first install result.

## Phase 6: Hook composition and performance

## Task 14: Test the guard together with the job identity hook

Depends on: Task 13

Create tests/hooks/test_launch_level_guard_with_identity.py and ./artifacts/hook-order.md (finding F3). The test runs src/superclaude/hooks/scripts/launch-level-guard.sh and src/superclaude/hooks/scripts/launch-job-identity.sh against the same PreToolUse Bash payload with a temporary HOME and the UV environment used by tests/hooks/test_launch_job_identity.py (UV_PYTHON set to sys.executable, UV_PYTHON_DOWNLOADS never). Cases: a governed session at full-submit with an allowed command (guard exit 0, identity output rewrites only the command through updatedInput, and the guard saw the original command); a governed session at worktree with a blocked command (guard exit 2 with the block message; the identity output is recorded but irrelevant to the decision); an ordinary session (both silent); a session whose file holds the word degraded (record what the identity hook does with a word outside its supported worktree, full and full-submit set, and what the guard does). ./artifacts/hook-order.md records the observed results, states that the order in which Claude Code runs two matching PreToolUse hooks and how it combines a block with an updatedInput is not observed here (it needs a live session, listed as pending in tests/hooks/test_launch_level_observations.py), and records any mismatch found for the degraded word with a one-sentence proposed resolution. Do not edit launch-job-identity.sh. Do not assert a fixed position of the guard in an installed settings.json: on an upgrade the installer appends a new registration at the end, so only a fresh install matches the shipped hooks.json order.

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard_with_identity.py -v passes for the four cases.
- ./artifacts/hook-order.md exists, lists the four observed outcomes, and says explicitly that hook ordering is unobserved.
- If the identity hook treats degraded as unsupported, the record says so and the guard's own handling of degraded (level worktree with the LL-STATE note) is asserted by a test.

## Task 15: Measure hook speed, including the cost the identity hook adds to ordinary sessions

Depends on: Task 14

Add the speed tests of design section 8 to tests/hooks/test_launch_level_guard.py and write the measured numbers to ./artifacts/speed-results.md (finding F2). Use 100 runs per case with time.monotonic(). T-SPD-1 and T-SPD-2: ordinary session, empty store and a store with 1,050 session files, report median and p95 against the targets 20 ms and 50 ms. T-SPD-3: ordinary median of the guard against src/superclaude/hooks/scripts/block-bare-python.sh in the same run, asserted at 1.5 times or less. T-SPD-4: governed allow and block, report p95 against 60 ms. T-SPD-5: governed commands of 64 KB and a 1 MB command, asserted under 1 second each. Add an envelope stress case with a very large non-command field and report time and memory or a timeout as an explicit result. For F2, also measure an ordinary Bash call through launch-job-identity.sh with a store directory that holds only a pending/ entry (the state a claim creates) and report the median against the same call with no store; the identity hook is not modified.

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard.py -k "SPD or speed" -v passes with T-SPD-3 and T-SPD-5 asserted.
- ./artifacts/speed-results.md exists with a table of case, runs, median, p95, target and result, a row for the large-envelope case, and a row for the identity hook with a non-empty store.
- If any asserted target fails, the failure is shown in the file and in the test output; no target is relaxed. If a reported-only target is exceeded, the file says so in one sentence and names the follow-up (no change to launch-job-identity.sh in this plan).

## Phase 7: Regression corpus

## Task 16: Port the push, git, alias, merge and benign corpus

Depends on: Task 11

Add to tests/hooks/test_launch_level_guard.py the corpus categories of design section 11 for git behaviour, taking case inputs from MR sections 8.2, 8.3 and 8.4 as historical baselines and writing expected results by hand from design section 4 (DD-2): push routes (T-ATK-1, 13, 25, 29, 50), aliases and variable subcommands (T-ATK-10, 35, 42), merges (T-ATK-48, 49, 51), the benign cases T-OK-1 to T-OK-36 that involve git and the pinned over-blocks T-OVR-1 to T-OVR-6, the amendment attacks N-ATK that concern git, the boundary cases of design section 10 that concern git (git stash push, git config --get remote.origin.url, a heredoc line all:\, git add of install_hooks.py), and the panel regression cases F1 to F8 only where their definitions can be found in the tree; the panel review file named in the design (.dev/brainstorms/20261105-170229-launch-level-hook/spec-panel-20261106/review.md) is absent, so record that in ./artifacts/f1-f8-missing.md and add regression cases only for the boundary rules the design states explicitly (typed top-level dispatch, identity loss, no-replacement binding, nonempty PR repo operand, protected destination); do not invent F-numbered cases. Add T-COR-2: replay the rows MR marks as real on a temporary bare remote and a temporary clone created by the test, asserting the remote refs before and after, so a push that should be blocked never reaches the remote and a permitted feature-branch push does. Where a result differs from the MR expectation, add a comment naming the design override (top-level typed dispatch, identity-loss allowance, no 64-id early allow, no-replacement publication, nonempty PR repo operand).

Acceptance criteria:
- uv run pytest tests/hooks/test_launch_level_guard.py -v passes with every listed corpus case present as a named test or parametrized id.
- The T-COR-2 test uses only a pytest temporary directory for the remote and the clone and asserts the remote ref list unchanged after each blocked case.
- The test module contains no expected value copied from MR without a matching row in design section 4 or an explicit override comment.
- Accepted leaks (T-ATK-26 to 28, N-ATK-7, 31 and 36) are pinned as allow with a comment citing the residual risk id (R1, R3 or R11) from design section 16.

## Task 17: Port the gh, MCP, tamper, escape and amendment corpus

Depends on: Task 16

Add to tests/hooks/test_launch_level_guard.py the remaining corpus categories of design section 11: gh api writes (T-ATK-6, 18, 47), tamper and escape (T-ATK-21, 55, 60), the benign cases and pinned over-blocks not covered by Task 16, the N-ATK amendment attacks 1 to 39 not covered by Task 16, the message cases T-MSG-1 to T-MSG-6 (T-MSG-4 to T-MSG-6 are defined at merged-requirements.md lines 1102 to 1104 and include the competing-class precedence assertions; plus one live-format check of the block message text through the real script), the acceptance map of design section 11 (each of AC-1 to AC-8 has at least the listed cases present), and the boundary cases of design section 10 not yet covered (PR title docs: explain git hooks at FS allowed, PR body naming pull request and git giving MERGE with LL-TEXT, orca with a continuation line, commit scope fix(ccsession): x giving ESCAPE, Write content quoting .claude/hooks allowed, Monitor with only ws, 65537 bytes of multi-byte text). Expected values are written by hand from design sections 4, 5 and 10.

Acceptance criteria:
- uv run pytest tests/hooks/ -v passes and the new tests are present as named or parametrized cases.
- A test maps AC-1 to AC-8 to their minimum case lists from design section 11 and fails if any listed case id is missing from the module.
- Each OB- item remains a skipped test in tests/hooks/test_launch_level_observations.py and is not duplicated here.

## Phase 8: Claim-side integration

## Task 18: Make the claim refuse a governed launch when the guard is not effective (IR-4)

Depends on: Task 13

In src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py replace the warning-only check enforcement_status() (which today only tests that ~/.claude/hooks/launch-level-guard.sh exists and is executable, and whose absence only adds W-ENFORCEMENT-ABSENT after the agent has already started) with the IR-4 check of design section 13, run before publish_pending() so a refused launch writes no pending record and starts no agent. The launch is refused, as a failed launch with the warning code W-ENFORCEMENT-ABSENT and a plain reason, unless all of these hold: jq is on PATH; the installed script exists, is executable and carries the line "# launch-level-guard-version: 1" (the version this plan ships, read from the installed file); the effective configuration enables both registrations, meaning the user settings file under the configured home holds the exact command ~/.claude/hooks/launch-level-guard.sh under UserPromptSubmit and under PreToolUse and neither that file nor the worktree's project settings files set disableAllHooks to true; and CLAUDE_CONFIG_DIR, when set, resolves to the same directory as the home .claude folder (otherwise the launch is refused, never inspecting one directory while another executes). "Registration enabled" also means the PreToolUse registration carries the matcher of design section 13 (so it fires for the governed tools) and the UserPromptSubmit registration has no matcher that prevents it from firing on a prompt; a registration that holds the command but cannot fire is refused. The preflight also checks the identity adapter's runtime prerequisites that design section 19.7 lists for a future governed launcher: uv on PATH, a Linux host with the process interfaces the adapter uses, and the launch-job-identity.sh registration on Bash PreToolUse. Put the new checks in cmd_launch after the already-launched and stale-prompt checks and before publish_pending, and state that order in a comment so the stale-prompt tests and la3 keep their meaning. The check never edits any configuration. The claim script cannot see the environment the launched agent runs in, so the refusal text says it verified the claim process only. A claim with --pipeline none is unaffected (it never reaches this script; test that at the claim-protocol level or by asserting the launch subcommand is not called). State in the task what the enforcement_hook result field means after the change (installed, missing or null today) and keep the ten-key return-contract test and SKILL.md in agreement. Update REMEDY["W-ENFORCEMENT-ABSENT"] to say the launch was refused and what to run (superclaude install, then claim again).

Update tests/skills/test_issue_orca_worktree.py: the two existing tests that expect W-ENFORCEMENT-ABSENT as a warning on a launched claim (around lines 1303 and 1324) now expect a refusal with no orca agent launch call and no pending file; add cases for each failing condition (no jq, script not executable, wrong version line, missing UserPromptSubmit registration, missing PreToolUse registration, disableAllHooks true in user settings and in the worktree project settings, CLAUDE_CONFIG_DIR elsewhere) and a passing case that proceeds to the launch.

Acceptance criteria:
- uv run pytest tests/skills/test_issue_orca_worktree.py -v passes with the updated and new cases.
- For every refusal case the fake orca records no agent launch call, the home directory has no pending/<nonce> file, and the claim output names the failed condition.
- With the guard installed, both registrations present and jq available, the launch proceeds exactly as before this task and records the launch entry.
- The check reads configuration files only; a test asserts the settings files are byte-identical before and after.
- launch_scene is migrated (a guard file with the version line and the executable bit, a settings.json with both registrations, a known jq, CLAUDE_CONFIG_DIR unset) and every test whose result changes is named in the task, including la2, la3, la6 and the tests at lines 1246, 1291, 1313 and the pr425 pair; the whole file passes with uv run pytest tests/skills/test_issue_orca_worktree.py -v.
- A registration that holds the guard command but whose matcher excludes the governed tools, and one under UserPromptSubmit with a matcher that prevents it from firing, are each refused by a test; a missing uv or a missing launch-job-identity.sh registration is refused by a test; none of these refusals writes a pending record or starts an agent.
- The refusal text for a stale installed guard names the command that actually replaces it (an existing installed script is skipped without force), not just superclaude install.

## Task 19: State release instructions and layer status in the claim output, and pin re-claim behaviour (IR-5, IR-6)

Depends on: Task 18

In src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py add to the launched-claim result and its printed text the IR-6 information of design section 13: how a person releases the session (in their own terminal run rm on sessions/<session id> and sessions/<session id>.ok under ~/.claude/state/launch-level/, with the session id taken from the "Launch-level guard" block message), and the status of each layer (L1 guard: effective, from the Task 18 preflight result; L2 pre-push: from a new function l2_status() that returns "absent" when the git path hooks/pre-push of the worktree is not an executable file and "present-unverified" otherwise, so the printed line always agrees with the preflight and never claims ownership of a hook it did not build). Add test cases in tests/skills/test_issue_orca_worktree.py that assert the result fields and printed text, and extend the existing re-claim test la2 (do not add a duplicate) to pin IR-5: a claim whose worktree record already has a launch entry launches nothing and writes no new pending record, and after the launch entry is removed from both the record and the git-dir mirror the next launch writes a new pending record with a different nonce (never resuming an earlier session).

Update src/superclaude/skills/sc-issue-protocol/refs/claim.md (Wave 8 section) to describe the release instructions and the layer status lines.

Acceptance criteria:
- A launched claim in the fake-orca test prints the release instruction containing the store path and both file names, and a layer line for L1 and for L2.
- Two launches in the same test home with the launch entry removed in between create two pending records with different names.
- uv run pytest tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py -v passes.

## Task 20: Report a missing L2 layer as the warning W-L2-ABSENT without refusing the launch (IR-7, owner option b)

Depends on: Task 19

Design section 13 IR-7 says the claim should refuse a governed launch while the L2 pre-push layer is absent. Task 21 records that this plan builds no L2 artifact, so a refusal would switch off every governed claim (--pipeline worktree and full) until a later plan ships, and would make the OB-H2 observation impossible because nothing could launch. The default taken here is therefore a warning, not a refusal; the owner can change it (the question was asked of the coordinator and not answered before implementation began).

In src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py, when l2_status() from Task 19 returns "absent", add the warning W-L2-ABSENT to the launch result with the reason, and let the launch continue. Do not look for any owned-hook marker or contract marker: no L2 artifact exists to match, and a header alone is not ownership proof (design section 19.2). Do not touch any existing hook file. Add W-L2-ABSENT to REMEDY with the sentence that the L2 layer is not built yet and the limits are enforced by the L1 guard only. The refusal of IR-4 (guard missing or not effective) from Task 18 is unchanged.

Update tests/skills/test_issue_orca_worktree.py with: l2_status absent gives the warning and the launch proceeds (a launch call is recorded, a pending record exists, status stays launched); a pre-push file present gives "present-unverified" and no W-L2-ABSENT; a foreign pre-push file is byte-identical before and after the claim. Record in ./artifacts/ir7-consequence.md, in plain words, that IR-7 is implemented as a warning, that the design text says refuse, why (the launch feature would be off and unobservable), and what to change when the L2 plan ships (turn the warning into a refusal in the same function).

Acceptance criteria:
- uv run pytest tests/skills/test_issue_orca_worktree.py -v passes with the L2 cases.
- With L2 absent the fake orca records the agent launch call, a pending record exists, and the result carries W-L2-ABSENT; with a foreign pre-push file present the file is byte-identical afterwards.
- ./artifacts/ir7-consequence.md exists, states the choice and the one-line change that makes it a refusal, and cites design sections 13 and 19.2.

## Phase 9: L2 disposition, documentation and final verification

## Task 21: Record the L2 pre-push disposition

Depends on: Task 1

Create ./artifacts/l2-disposition.md from the L2 verdict in ./artifacts/b-ctx-verdict.md. If that verdict is L2: BLOCKED, the file states that this plan builds no pre-push file, no L2 installer and no L2 test beyond the IR-7 detection, lists the exact missing launcher or harness integration copied from the verdict, and gives the follow-up scope as design sections 19.2 to 19.5 (one owned shared hooks/pre-push, no config change, no forwarding, refuse field-3 updates to refs/heads/main and refs/heads/master for a positively selected governed process, human pushes in the same worktree unrestricted, tests on a temporary bare remote) with the open items U28 and OB-H3 L2 observation. If the verdict is L2: GO, the file states that a follow-up plan for sections 19.2 to 19.5 is still required because the install place (U28) and the OB-H3 L2 observation are unverified, and this plan builds no L2 code either way.

Acceptance criteria:
- ./artifacts/l2-disposition.md exists and quotes the L2 line of ./artifacts/b-ctx-verdict.md.
- The file states that no pre-push or installer code was written by this plan, and a search of the diff for a file named pre-push finds none.
- The follow-up scope paragraph names design sections 19.2, 19.3, 19.4 and 19.5.

## Task 22: Update the design status, claim documentation and ship-gate text, then run the full checks

Depends on: Task 20, Task 21, Task 17, Task 15

Update docs/designs/sc-issue-launch-level-hook.md: the status and planning_status lines and section 19 text that say the claim code does not implement the pipeline interface or that the L1 guard is not built (finding F6) now state what exists (guard script, registrations, installer entry, IR-4 to IR-7 detection) and what is still pending (OB-H1, OB-H2, OB-H3, OB-CTX, L2); keep the owner decisions and the historical review sections untouched. Update the places that describe W-ENFORCEMENT-ABSENT as a warning (src/superclaude/skills/sc-issue-protocol/SKILL.md, src/superclaude/skills/sc-issue-protocol/refs/claim.md, src/superclaude/commands/issue.md, docs/user-guide/commands.md and docs/designs/sc-issue-claim-pipeline-flag.md; the last one also states that IR-3 stays documentation only because no code writes pipeline.json) so they describe the refusal when the guard is missing or not effective, the W-L2-ABSENT warning (the launch continues and the L2 layer is not built yet), and the rule that no governed claim is used on a real issue until OB-H1 item 1 shows the parent session_id in subagent payloads, OB-H2 passes and OB-H3 passes (the U1 ship gate of design section 7). State in the design document, in one sentence, that pending launch records are not pruned (owner decision O-15). Run make sync-dev and make verify-sync, and update any plugin or mirror copy that a mirror test requires to stay byte-identical.

Acceptance criteria:
- grep for "does not implement this proposed pipeline interface" in docs/designs/sc-issue-launch-level-hook.md returns no match, and the status line names what is built and what is pending.
- grep of the five documents for W-ENFORCEMENT-ABSENT shows wording that describes a refusal, not a warning that lets the launch continue, and grep for W-L2-ABSENT shows wording that describes a warning.
- uv run pytest tests/hooks/ tests/cli/test_install_hooks.py tests/skills/test_issue_orca_worktree.py tests/skills/test_issue_protocol.py -v passes with the only skips being the pending observation tests of tests/hooks/test_launch_level_observations.py, the hook-order observation of Task 14, and the existing environment skips (non-Linux, running as root, the opt-in live probe).
- make verify-sync exits 0 and make lint exits 0.
- ./artifacts/final-check.md records the exact commands run, the pass and skip counts, and the list of pending observations (OB-H1 items 1 to 9, OB-H2, OB-H3, OB-CTX) with the statement that none has been run.
