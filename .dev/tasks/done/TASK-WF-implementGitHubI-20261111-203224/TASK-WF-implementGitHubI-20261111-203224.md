---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-implementGitHubI-20261111-203224
version: "1"
priority: Medium
created_date: "2026-11-11"
---

# Make --unattended the positive per-step default for coordinators (issue 507)

Source: ./source.md
Goal: A coordinator that reads the worker contract or the routing guide puts `--unattended` and exactly one report directory on every `Command:` line of the 16 phase 1 commands unless a numbered two-copy preflight fails, with no stale P0 text left, repair-naming guard refusals and updated phrase pins in the worker-contract test.

## Constraints

- Edit only these files: `src/superclaude/core/WORKER-CONTRACT.md`, `src/superclaude/core/HOW-WE-WORK.md`, `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` and `tests/skills/test_worker_contract.py`. Run `make sync-dev` afterwards; never stage anything under `.claude/`.
- Do not edit any of the 31 files in `src/superclaude/commands/`, `/sc:recommend`, the claim pipeline, Orca's own guide or skills, or any prose for headless callers (sprint, issue-watch, claim-launched agents, eval suites, Coder CI).
- Do not make a worker add the flag, install a copy or rewrite its brief. The guard stays report-only.
- Leave untouched, and do not decide, the owner decisions: the five gates that turn a person's check into a caller input (`/sc:review-translation --context`, `/sc:cli-portify --resume`, `/sc:cli-eval` W3, `/sc:reflect --remediate`, `/sc:tdd`), and whether cleanup, improve, task, tasklist and cli-eval are held out until phase 2 passes. The existing table rows for these commands keep their wording.
- Do not push and do not open a PR. Stage `.dev/tasks` with `git add .dev/tasks`. A local commit on the feature branch is allowed.

## Phase 1: Contract text in WORKER-CONTRACT.md

## Task 1: Make the three guard refusal texts name the repair

In `src/superclaude/core/WORKER-CONTRACT.md`, in the "Brief guard" term (lines 16-22 of the current file), keep each refusal string's existing words, including the prefix `guard refused:`, and append the repair for the coordinator after it. Case 1 (`guard refused: brief lacks --unattended`) names: add `--unattended` and exactly one report directory to that `Command:` line in a new Task. Case 2 (`guard refused: loaded command has no Unattended mode section ...`) names: refresh `~/.claude` (a stale installed copy) or drop `--unattended` for that command, then create a new Task. The disagree refusal (`guard refused: command copies disagree (stale copy): <paths>`) names: refresh the stale copy listed in `<paths>`, normally `~/.claude`, then create a new Task. After the "A command invoked by another command ..." sentence add one sentence stating the refusal is report-only: the worker never installs or refreshes a command copy and never rewrites its own brief; the coordinator repairs and creates a new Task (WC-6).

Acceptance criteria:
- Each of the three refusal strings in the file still contains its original text word for word, so the existing pins at lines 58-78 of `tests/skills/test_worker_contract.py` still match, and each is followed by a repair clause naming `--unattended` plus exactly one report directory (case 1) or refreshing `~/.claude` (case 2 and the disagree refusal).
- The file states that the worker never installs or refreshes a copy and never rewrites its brief on a refusal.
- `grep -c 'guard refused:' src/superclaude/core/WORKER-CONTRACT.md` still finds the prefix on every refusal line.

## Task 2: Add the numbered coordinator preflight before the first task-create

Depends on: Task 1

In `src/superclaude/core/WORKER-CONTRACT.md`, section 4, replace the single sentence at line 216 ("The coordinator decides whether a `Command:` line carries `--unattended` by the guard's own test ...") and its follow-on sentence with a new subsection heading `### Before the first task-create for a command` directly after the brief-layout text, holding a numbered list. The text must say: the coordinator decides by the two-copy test whether a `Command:` line carries `--unattended`; the test runs once per command per run before the first `task-create` for that command (a Task spec cannot be edited afterwards) and again after any change to a command file, `make sync-dev` or `superclaude install`; the steps read, as plain files, the target worktree's `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md` (a missing copy is skipped), look for a line equal to `## Unattended mode` in each existing copy, then act: every existing copy has it, so the `Command:` line carries `--unattended` and one report directory; the copies disagree, so no Task is created until the stale copy is refreshed; no existing copy has it, so the line carries no flag and the brief says why, and a run of that command that needs a person is a person-in-the-loop run, not a worker. Keep the sentence "A WC-3 re-invocation keeps every token of the `Command:` line and only adds the answer."

Acceptance criteria:
- `grep -n 'Before the first task-create for a command' src/superclaude/core/WORKER-CONTRACT.md` finds exactly one heading, inside section 4 before `## 5.`.
- The subsection contains the phrase `the coordinator decides by the two-copy test` and the phrase `re-invocation keeps every token`, names both copy paths, and the numbered steps appear in run order.
- The old line-216 sentence no longer exists as a separate paragraph.

## Task 3: Rewrite the section 5 template and slot rules to a positive default

Depends on: Task 2

In `src/superclaude/core/WORKER-CONTRACT.md` section 5 ("Coordinator brief template", from line 283), change the template `Command:` placeholder (line 296) so it reads `Command: /sc:<name> <arguments> --unattended <the report directory flag: the command's own directory flag where its table row names one, else --report-dir <dir>> <other flags this command's brief rule requires>`. Rewrite the slot rules below it: the first bullet (line 303) becomes the default rule: put `--unattended` and exactly one report directory on every `Command:` line, for each step and never as a session-wide setting, unless the two-copy test of "Before the first task-create for a command" fails for that command; the default set is the 16 phase 1 commands (keep the list adversarial, brainstorm, cleanup-audit, graph, impact, index-repo, init-lite, workflow, analyze, build, business-panel, design, document, explain, index, test) until a phase 2 live check passes. Keep the existing bullet that starts `- From P2 ` as one line and keep all 15 phase 2 command names in it (the test helper `_p2_bullet` reads it); reword it to say these commands accept the flag under the same guard test and join the default set only after a phase 2 live check passes, and that the coordinator flags one of them before that only when the user's instruction names it. Add a bullet that lists what the flag drops: improve and cleanup skip approval-required items, test ends `succeeded` when its suite fails (read the verdict in the report), research is forced to `--strategy planning`, workflow skips `--handoff implement`, and WC-9 turns off every push, PR and other outward action. Add a bullet that a command must be started through its Skill call (WC-7; reading the command file does not do it, decision P1-C5) and that a person-in-the-loop run is not a worker.

Acceptance criteria:
- The template's `Command:` line visibly contains `--unattended`, and the brief-template guard-before-command check in `tests/skills/test_worker_contract.py` (`_check_guard_before_command`) still passes.
- Section 5 contains the 16 phase 1 command names in the default rule, exactly one line starting `- From P2 ` that still names all 15 phase 2 commands, the five drop items, the Skill-call sentence and the person-in-the-loop sentence.
- No sentence in section 5 says the flag is allowed only where a section exists without also stating the default.
- The rows of the flags table for `/sc:review-translation`, `/sc:cli-portify`, `/sc:cli-eval`, `/sc:reflect` and `/sc:tdd` are unchanged.

## Task 4: Delete the stale P0 text from the contract

Depends on: Task 3

In `src/superclaude/core/WORKER-CONTRACT.md` remove or replace every P0 statement: the two sentences in WC-5 (line 59) that begin "Before P1, when no command writes a contract, a brief that states the AC-0.4 report file ..." through "... instead of `worker_status`." (keep the sentences before and after them); the bullet "at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5);" in "What the coordinator owes each worker" (line 89); the template line starting `P0 only: Report file:` (line 295); the slot-rule bullet starting "The `P0 only:` line is used only before P1" (line 305); in the paragraph starting "Flags the brief must pass" (line 307) the sentence "`--report-dir` is marked "from P1": no command accepts it at P0."; and in the flags table the `(from P1)` markers on the `/sc:cleanup-audit`, `/sc:index-repo`, `/sc:init-lite` and `/sc:workflow` rows and the `none at P0;` text on the `/sc:index-repo` row (lines 314, 319, 320, 327). Keep the table's 17 rows and each row's required flags.

Acceptance criteria:
- `grep -n 'P0\|AC-0.4\|from P1' src/superclaude/core/WORKER-CONTRACT.md` prints no line, except lines that are about phase 1 or phase 2 conversion and not about a P0 rule.
- The table still has 17 rows beginning `| \`/sc:` and the sentence naming "12 commands" and "17 rows" still matches the table.
- WC-5 still states the outcome mapping (`--outcome failed` when the contract's `worker_status` is `failed` or `blocked`, or no contract exists).

## Phase 2: Routing guide and developer guide

## Task 5: Rewrite the HOW-WE-WORK Orca bullet and keep the plugin copy identical

Depends on: Task 3

In `src/superclaude/core/HOW-WE-WORK.md`, in the "Orca coordination" section replace the bullet at line 403 ("**`--unattended` only where the command supports it.** ...") with a bullet headed `**\`--unattended\` is the default on a worker's \`Command:\` line.**` that says: put `--unattended` and exactly one report directory on every `Command:` line, per step and never session-wide, unless the two-copy test in `~/.claude/WORKER-CONTRACT.md` ("Before the first task-create for a command") fails for that command; the default set is the 16 phase 1 commands until a phase 2 live check passes; the flag drops approval-required items (improve, cleanup), a failing test suite still ends `succeeded`, research is forced to planning, workflow skips `--handoff implement`, and no push or PR; start each command through its Skill call; a person-in-the-loop run is not a worker. Do not change any other line, including the routing table and the level table. Then copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` (`cp`).

Acceptance criteria:
- `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` exits 0.
- `git diff --stat` shows only the one bullet changed in each of the two files, and `src/superclaude/core/CLAUDE.md` is unchanged because no level-table text changed.
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/commands/test_routing_plugin_parity.py tests/cli/test_how_we_work_install.py -q` passes.

## Task 6: Replace the stale rollout state in the developer guide

In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md`, under "#### Rollout state" (lines 983-987), replace the first two bullets (the P0 statement that no command accepts `--unattended` and that `UNATTENDED_COMMANDS` is empty, and the "Per the rollout plan ... from P1 on" bullet) with current text: all 31 converted commands have an `## Unattended mode` section (16 from phase 1, 15 from phase 2) and `UNATTENDED_EXPECT` in `tests/skills/test_worker_contract.py` holds exactly those 31 entries; coordinators put `--unattended` on the 16 phase 1 commands by default and the phase 2 commands join that default after a phase 2 live check; the coordinator decides by the two-copy test in `~/.claude/WORKER-CONTRACT.md` before the first task-create. Keep the third bullet (SA-1, without `--unattended` every command behaves as today) unchanged.

Acceptance criteria:
- `grep -n 'At P0' docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` prints nothing.
- The Rollout state section states 31 commands, 16 plus 15, and keeps the SA-1 bullet word for word.

## Phase 3: Phrase pins in the worker-contract test

## Task 7: Update the pins that required the stale P0 text

Depends on: Task 4

In `tests/skills/test_worker_contract.py` edit `RULE_PHRASES`: delete the `"WC-5-P0-override"` entry (lines 144-149); in `"brief-contents"` (lines 255-261) delete the phrase "at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5)" and keep the other phrase; in `"brief-template"` (lines 360-367) replace the two P0 phrases (`'\`--report-dir\` is marked "from P1": no command accepts it at P0'` and `"P0 only: Report file: <the command's report file under AC-0.4>."`) with phrases that exist in the rewritten contract: the heading `## 5. Coordinator brief template` stays, plus the `Command: /sc:<name> <arguments> --unattended` template prefix. Also update the pins at lines 58-78 if Task 1's wording requires adding the repair clauses as extra phrases (keep each original phrase). If any other test in this file reads the deleted text, fix it the same way. Do not change `UNATTENDED_EXPECT`, `P1_COMMANDS`, `P2_COMMANDS`, `NEVER_AS_WORKER` or the `_p2_bullet` helper.

Acceptance criteria:
- `grep -n 'P0\|AC-0.4' tests/skills/test_worker_contract.py` prints no pin that requires text about P0 in the contract.
- `uv run pytest tests/skills/test_worker_contract.py -q` passes after Tasks 1 to 4 and this task.

## Task 8: Add pins for the new coordinator rules, with a failing-case test

Depends on: Task 7

In `tests/skills/test_worker_contract.py` add new `RULE_PHRASES` entries and make sure the existing tests that iterate `RULE_PHRASES` pick them up. Add: a rule for the preflight whose phrases are `### Before the first task-create for a command`, `the coordinator decides by the two-copy test` and both copy paths `.claude/commands/sc/<name>.md` and `~/.claude/commands/sc/<name>.md`; a rule whose phrase is `re-invocation keeps every token` (it must also match the Brief guard paragraph); a rule for the positive default whose phrases include `on every \`Command:\` line` and `never as a session-wide setting`; a rule for the drop list whose phrases name `approval-required`, `--strategy planning`, `--handoff implement` and `WC-9`; a rule whose phrases are `a person-in-the-loop run is not a worker` and `Skill call`; a rule for the refusal repairs whose phrases are the repair clauses of Task 1. Add one negative test, in the style of `test_p2_brief_check_fails_when_until_p2_is_back`, that removes the `the coordinator decides by the two-copy test` phrase from the contract text and asserts the rule check raises `AssertionError`.

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -q` passes and its pass count is greater than before the change.
- The new negative test fails when the phrase `the coordinator decides by the two-copy test` is removed from a copy of the contract text.
- Every new pin phrase exists word for word in `src/superclaude/core/WORKER-CONTRACT.md` as written by Tasks 1 to 4.

## Phase 4: Sync and mirror checks

## Task 9: Sync the development copies and confirm the mirrors and path rule

Depends on: Task 5, Task 6, Task 8

Run `make sync-dev`, then `make verify-sync`. Run `grep -rn 'src/superclaude' src/superclaude/commands src/superclaude/skills src/superclaude/agents src/superclaude/core src/superclaude/hooks` and compare with the same grep on `git show origin/master` content (`git stash` is not allowed; use `git diff -U0` on the touched files instead) so any new hit is justified. Stage `.dev/tasks` only with `git add .dev/tasks`; never stage a path under `.claude/`.

Acceptance criteria:
- `make verify-sync` exits 0 and `git status --porcelain` shows no `.claude/` path staged.
- `git diff -U0` of the five edited files adds no line containing `src/superclaude/` in the contract or the routing guide.
- `git diff --name-only origin/master` lists only the five files named in the Constraints plus the `.dev/` paths.
