---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-removeScImproveP-20261117-223014
version: "1"
priority: Medium
created_date: "2026-11-17"
---

# Remove /sc:improve (IronClaude 6.0.0, PR 8)

Source: ./source.md
Goal: `/sc:improve` is gone from the commands, the plugin mirror, the legacy root commands folder, the routing guide, the worker contract, the launch-level hook, the docs and the tests that pin it, with no file outside the historical records naming it, and the full test suite shows no new failure.

## Constraints

- Source of truth is `src/superclaude/`. Never stage anything under `.claude/` except `.claude/settings.json`; the local mirror copy of the command in the project's `.claude` folder is gitignored sync output.
- Do not edit historical records: `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, past `CHANGELOG.md` entries, and anything under `.dev/` other than this plan's own package. Do not add a `CHANGELOG.md` entry.
- `/sc:cleanup`, `/sc:analyze` and `/sc:adversarial` stay; only the lines that point a reader to `/sc:improve` change, with the smallest edit that stays true. The `--improve` flag of `/sc:spec-panel` and the word "improve" in ordinary prose stay.
- Swarm and everything in the issue's "Kept for now" list stays untouched. In `launch-level-guard.sh` and its test edit only the `/sc:improve` lines.
- The frozen research package `.dev/tasks/to-do/TASK-RESEARCH-recommend-refresh-20261024-044336/` is not edited; the 47-command record at the end of `tests/recommend/fixtures/routing_refresh_cases.json` stays as it is.
- Do not fix the improve half of issue 506 (usage line versus examples); it goes away with the removal.
- Never hardcode `src/superclaude/` paths in installed primitives.
- Detail and line numbers for every item are in `.dev/cleanup/improve/dependency-map.md`. `.dev/tasks/` is always staged with the commit.

## Phase 1: Remove the command and the pointers to it

## Task 1: Delete the command file and its copies

Delete `src/superclaude/commands/improve.md`, `plugins/superclaude/commands/improve.md` and `commands/sc-improve.md` from the repo, and delete the untracked local mirror `.claude/commands/sc/improve.md` (gitignored; never staged).

Acceptance criteria:
- None of the four paths exists, and `ls src/superclaude/commands | grep -c '^improve'` prints 0.
- `git status` shows exactly three tracked deletions for this task and no staged `.claude/` path.

## Task 2: Remove the pointers in kept commands, skills and the recommend prompt

Depends on: Task 1

Edit each of these, smallest true edit: `src/superclaude/commands/analyze.md` line 139 becomes "**Next Step**: After review, use `/sc:cleanup` for dead code removal." (drop the improve clause); `src/superclaude/commands/adversarial.md` line 195, delete the `/sc:improve` row of the integration table; `src/superclaude/skills/sc-recommend/SKILL.md` line 171 and its copy `plugins/superclaude/skills/sc-recommend/SKILL.md`, "cleanup/improve exception" becomes "cleanup exception"; `src/superclaude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md` line 41 and its plugin copy, "`/sc:cleanup` and `/sc:improve` exception" becomes "`/sc:cleanup` exception"; `src/superclaude/cli/recommend/prompts.py` line 195, "contained-folder cleanup/improve exception" becomes "contained-folder cleanup exception"; `src/superclaude/skills/sc-cli-portify-protocol/refs/analysis-protocol.md` line 222, "Found in: implement, improve" becomes "Found in: implement"; `src/superclaude/core/BUSINESS_PANEL_EXAMPLES.md` and its copy `plugins/superclaude/core/BUSINESS_PANEL_EXAMPLES.md`, delete the "Combined with /improve" block (lines 78-84), the `→ /improve roadmap` step (line 168) and the `/improve` stage (line 211), keeping the surrounding lists valid.

Acceptance criteria:
- `git grep -n -E 'sc:improve|/improve\b|cleanup/improve' -- src/superclaude/commands src/superclaude/skills src/superclaude/cli src/superclaude/core/BUSINESS_PANEL_EXAMPLES.md plugins/superclaude/skills plugins/superclaude/core` prints nothing except the routing-guide hits handled by Task 3.
- Any test that pins the recommend prompt text still passes (`uv run pytest tests/recommend tests/skills/test_sc_recommend_routing_contract.py -q`, run after Task 6).
- The BUSINESS_PANEL_EXAMPLES list around each removed line still reads as a valid list.

## Phase 2: Routing guide, worker contract and launch-level hook

## Task 3: Remove /sc:improve from the routing guide, core CLAUDE.md and the guide's twin

Depends on: Task 1

In `src/superclaude/core/HOW-WE-WORK.md`: line 22, "contained `/sc:cleanup` and `/sc:improve` work on a folder" becomes "contained `/sc:cleanup` work on a folder"; line 169, "no cleanup, improve or commit" becomes "no cleanup or commit"; lines 171-173 (section 3.7 item 2) become a cleanup-only item: "Small, contained cleanups, only when requested", keep the `/sc:cleanup src/billing/ --type code --safe --interactive` example, delete the `/sc:improve` example, the "Improve also supports..." sentence, the "improve can change formatting, naming, imports and annotations" clause and the "improvement-only request" sentence, and write "The command's example-only preview or validation controls do not establish a supported flag"; line 249, "Stop before cleanup, improve or commit" becomes "Stop before cleanup or commit"; delete the "Contained improvement" row (line 250) and the `contained-improve` row (line 377); line 365 (the cleanup row notes), drop "and improvement-only uses contained-improve, with no compulsory cleanup/improve chain" and keep "report-only uses cleanup-audit-only"; line 376, "no cleanup, improve or commit" becomes "no cleanup or commit"; line 398, "improve and cleanup skip approval-required items" becomes "cleanup skips approval-required items". Make the same edit to the level-table sentence at line 84 of `src/superclaude/core/CLAUDE.md`. Copy `HOW-WE-WORK.md` byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`.

Acceptance criteria:
- `diff src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` prints nothing, and `grep -n -i 'improve' src/superclaude/core/HOW-WE-WORK.md src/superclaude/core/CLAUDE.md` prints only unrelated prose hits (none of them naming the command or the removed row).
- The level-table block in `src/superclaude/core/CLAUDE.md` equals the one in `HOW-WE-WORK.md` (the tests in Task 6 check this).

## Task 4: Update the converted-command counts and the approval sentence in the worker contract

Depends on: Task 1

In `src/superclaude/core/WORKER-CONTRACT.md` line 330 change "the 14 commands converted in P2" to "the 13 commands" and delete `improve, ` from the list (auggie-review, cleanup, improve, cli-eval, ...); in line 331 change "`/sc:improve` and `/sc:cleanup` skip every approval-required item" to "`/sc:cleanup` skips every approval-required item".

Acceptance criteria:
- `grep -n -i 'improve' src/superclaude/core/WORKER-CONTRACT.md` prints nothing.
- The never-as-worker list in the same file is unchanged.

## Task 5: Remove improve from the launch-level guard and its plugin twin

Depends on: Task 1

In `src/superclaude/hooks/scripts/launch-level-guard.sh` change line 43 to `b='starting /sc:implement, /task or /sc:cleanup (or their skills).'` and line 409 to `implement | task | cleanup) LL_CLASSES+='IMPL ' ;;`. Make the same two edits in `plugins/superclaude/hooks/scripts/launch-level-guard.sh`, keeping both files identical.

Acceptance criteria:
- `diff src/superclaude/hooks/scripts/launch-level-guard.sh plugins/superclaude/hooks/scripts/launch-level-guard.sh` prints nothing, and `grep -c improve` on either file prints 0.
- `bash -n src/superclaude/hooks/scripts/launch-level-guard.sh` exits 0.

## Phase 3: Tests that pin the command

## Task 6: Update the routing, routing-refresh and fixture tests

Depends on: Task 2, Task 3

In `tests/core/test_how_we_work_routing_table.py`: delete `"contained-improve"` from the expected row ids (line 83); change the assertion at line 500 to "contained `/sc:cleanup` work on a folder"; change the S04 phrase at line 644 to "no cleanup or commit"; delete the S05 scenario tuple (lines 647-656); in `test_cleanup_audit_and_improvement_have_separate_authority_boundaries` (line 874) rename it to `test_cleanup_audit_has_report_only_authority_boundary`, keep the audit assertions, delete the `improve` assertions (lines 884-888) and fix the docstring. In `tests/recommend/test_routing_refresh.py`: add `"improve"` to `_POST_REFRESH_REMOVALS` (line 39) and update its comment; retire S05 in the id check (lines ~140) and in the module docstring; in `test_flag_value_check_rejects_undeclared_enumerated_value` (line 299) replace the `improve.md` example-only-flag check with another kept command that has the same property, found by reading `src/superclaude/commands`, or drop only that sub-assertion if none fits. In `tests/recommend/fixtures/routing_refresh_cases.json`: delete case S05 (lines 133-151), change the S04 guide phrase to "no cleanup or commit" (lines 122-123 including the `must_not` text if it names improve), and delete `"sc:improve"` from the competitor lists at lines 123, 186 and 578. Leave line 706 (the frozen 47-command record) and the `T13` pin unchanged.

Acceptance criteria:
- `uv run pytest tests/core/test_how_we_work_routing_table.py tests/recommend tests/skills/test_sc_recommend_routing_contract.py -q` shows no new failure against the baseline in `.dev/issues/v6-improve/BASELINE.md`.
- `grep -n -i 'sc:improve\|contained-improve' tests/core/test_how_we_work_routing_table.py tests/recommend/test_routing_refresh.py` prints nothing, and `tests/recommend/fixtures/routing_refresh_cases.json` keeps only its frozen `analyses/improve.md` record.

## Task 7: Update the launch-level guard test

Depends on: Task 5

In `tests/hooks/test_launch_level_guard.py` add the rewrite from `/task, /sc:improve or /sc:cleanup` to `/task or /sc:cleanup` to `_REMOVED_COMMAND_TEXT` after the build entry (line 82) and fix the comment above it (line 79) to name `/sc:improve`, and delete `"sc:improve"` from `IMPL_SPELLINGS` (line 916). The design document is a historical record and is not edited.

Acceptance criteria:
- `uv run pytest tests/hooks/test_launch_level_guard.py -q` shows no new failure.
- `grep -n 'sc:improve' tests/hooks/test_launch_level_guard.py` prints only the rewrite entry inside `_REMOVED_COMMAND_TEXT` and its comment.

## Task 8: Update the worker-contract test pins

Depends on: Task 1, Task 4

In `tests/skills/test_worker_contract.py` delete `"improve"` from `P2_COMMANDS` (line 498) and fix the comment "The fifteen commands" (line 493) to the true count, delete the `improve` entry of `UNATTENDED_EXPECT` (lines 624-635), change the 14 checks in `_check_p2_set` to 13 including the messages (lines 1630-1631), change the 29 check to 28 including its message (line 1637), and delete the two `("improve", ...)` rows of `P2_GATES` (lines 1755-1756). Leave the `--improve` flag in the `spec-panel` entry (line 650).

Acceptance criteria:
- `uv run pytest tests/skills/test_worker_contract.py -q` shows no new failure, and `grep -n '"improve"' tests/skills/test_worker_contract.py` prints nothing.
- The P1 set has 15 names, the P2 set 13, and `UNATTENDED_EXPECT` 28.

## Task 9: Update the install test file lists

Depends on: Task 1

In `tests/unit/test_cli_install.py` delete `improve.md` from the two expected command-file lists (lines 116 and 403), keeping each line's order and wrapping.

Acceptance criteria:
- `uv run pytest tests/unit/test_cli_install.py -q` shows no new failure.
- `grep -n 'improve.md' tests/unit/test_cli_install.py` prints nothing.

## Phase 4: Docs and legacy command copies

## Task 10: Remove /sc:improve from the user guide and the onboarding page

Depends on: Task 1

In `docs/user-guide/commands.md` delete the `/sc:improve` row of the command table (line 82) and the whole `### /sc:improve - Code Improvement` section with its trailing `---` (lines 1039-1067). In `docs/user-guide/flags.md` delete the `### Improve Command Flags (/sc:improve)` block (lines 75-81). In `docs/user-guide/mcp-servers.md` lines 91-93 delete the two-line "Automatic activation" example that uses `/sc:improve` and keep the API key setup. In `docs/user-guide/agents.md` line 157 change "`/sc:implement` and `/sc:improve` do not call it" to "`/sc:implement` does not call it" and delete the `/sc:improve` row of the Command-Agent Mapping table (line 846). In `docs/onboarding/ironclaude-onboarding.html` change "contained /sc:cleanup and /sc:improve work" to "contained /sc:cleanup work" at lines 318, 323, 335 and 341.

Acceptance criteria:
- `git grep -n -E 'sc:improve|scimprove' -- docs/user-guide docs/onboarding` prints nothing, and no anchor link `#scimprove---code-improvement` remains in `docs/`.
- The Morphllm section of `docs/user-guide/mcp-servers.md` still reads as valid markdown with its code block closed.

## Task 11: Update the architecture reference and the developer guide

Depends on: Task 4, Task 8

In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` drop `improve` from the IMPL class row (line 1605) and change each converted-command count: 29 becomes 28 and the phase 2 count 14 becomes 13 at lines 81, 196, 290, 317, 710, 745, 1319, 1321, 1840, 1958, 2197, 2203 (31 converted, 29 remain becomes 28 remain) and 2230; read each line in place first, and read line 1315 to see whether it names the command. In `docs/developer-guide/SuperClaude-Developer-Guide-Commands-Skills-Agents.md` line 976 change the count to 28 commands (15 from phase 1, 13 from phase 2) and "those 29 entries" to 28.

Acceptance criteria:
- `git grep -n 'sc:improve' -- docs/architecture docs/developer-guide` prints nothing.
- Each edited converted-command count agrees with `grep -rl '^## Unattended mode' src/superclaude/commands | wc -l`, which prints 28.

## Task 12: Remove the command from the legacy root commands

Depends on: Task 1

In `commands/sc-help.md` delete the `/sc:sc:improve` table row (line 40). In `commands/sc-analyze.md` line 98 change to "**Next Step**: After review, use `/sc:sc:cleanup` for dead code removal." In `commands/sc-troubleshoot.md` line 120 read the line in place and either point it to `/sc:sc:cleanup` when that is true or delete the line. In `commands/sc-recommend.md` remove each `/sc:sc:improve` entry (lines 117, 131, 152, 159, 166, 179, 184-185, 268, 306, 465, 498, 757, 809, 817, 822), reading each line in place: drop the list entry, renumber the numbered flows, remove the `improve_category` block's improve command while keeping its `/sc:sc:cleanup` entry, and drop the `improve` keyword from the keyword rule at line 117.

Acceptance criteria:
- `git grep -n -E 'sc:sc:improve|sc:improve|sc-improve' -- commands docs/generated` prints nothing.
- `git diff --stat commands/sc-recommend.md` shows only changed lines of the improve entries, and each edited list or numbered flow still reads as valid.
