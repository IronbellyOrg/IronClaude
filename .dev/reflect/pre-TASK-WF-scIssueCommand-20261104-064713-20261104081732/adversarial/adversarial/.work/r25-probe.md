# Round 2.5 Invariant Probe (fault-finder, independent)

Target: plan `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md` (plan:N) against `source.md` (source.md:N), same folder.
Consensus probed: round2-v1.md, round2-v2.md, round2-v3.md Updated Position Tables (PASS with notes; all surviving points minor).
Method: every plan/spec line cited below was re-read in this session; repo facts were checked with read-only Grep/Read/sed/git.

## Findings

### INV-001
ID: INV-001
CATEGORY: sufficiency_challenge
ASSUMPTION: C-001 fix step 1 alone makes every escaped write target an issue that "cannot exist on origin" (round2-v1.md:48-52, round2-v3.md:64-66), using the example URL `https://github.com/IronbellyOrg/issue302-no-such-repo/issues/999999999`.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE:
- The fix exists to survive a faulty Wave 0 parse/compare step. source.md:143 puts both jobs in one step: "Parse `<N>` from the argument. A URL must point at `<R>`; otherwise STOP `E-FOREIGN-REPO`." A correlated fault in that one step is the exact failure model the fix targets.
- The example repo name embeds the digits `302`. A lenient number parser that accepts the three argument forms of source.md:66 (`302`, `#302`, URL), for example a first-digits match such as `#?(\d+)` or `issues?[/#]?(\d+)`, returns N = 302 from `issue302-...`, not 999999999.
- #302 is the real issue on origin that this feature implements (source.md:4). Its current state was not checked (no gh in this probe; UNVERIFIED). If it is open and assigned to nobody or to the user, Wave 2 does not stop (source.md:155-157). Wave 3 then self-assigns it (source.md:162), and Wave 6 posts or edits two marked comments on it (source.md:178-179). Comments notify the issue's subscribers, and a notification cannot be taken back.
- So with this URL, "fix ALONE resolves it" is false. The double-fault escape lands on a live, watched issue instead of a number that does not exist, and the C-001 minor grading rests on "reversible on the user's own fork PR #1" (round2-v3.md:53-54, round2-v1.md:41). That basis no longer holds.
- Falsifying downstream condition: plan:259 ("No GitHub issue was assigned, commented on or created without the user's approval") fails under one parser fault plus one compare fault.
- Fix: use a foreign URL with no digits outside the issue-number segment, for example `https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999`. Add a Task 1 test that a URL with digits in the owner or repo name yields N from the `/issues/<N>` segment only.

### INV-002
ID: INV-002
CATEGORY: guard_conditions
ASSUMPTION: The agreed tests for the new URL-vs-origin check (round2-v1.md:53 and round2-v3.md:68: "a same-repo URL, a foreign URL and owner/repo case") pin the E-FOREIGN-REPO guard well enough to make AC 4 "checkable offline".
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- The chosen item-4 URL has the same owner as origin (`IronbellyOrg`, plan:39 output `IronbellyOrg/IronClaude`). A check that compares only the owner, or that uses a prefix test such as `startswith("https://github.com/IronbellyOrg/IronClaude")`, would accept `IronbellyOrg/IronClaudeX`. A "foreign URL" test with a different owner passes against both bugs.
- Neither round's test list separates the exit codes. Task 1 prints `E-NO-ORIGIN` on any non-zero exit (plan:32). If the new mode reuses that exit, the orchestrator cannot tell E-NO-ORIGIN from E-FOREIGN-REPO, and the item-4 row (plan:258 requires `E-FOREIGN-REPO`) could show the wrong code.
- Fix: add same-owner-different-repo, repo-name-prefix (`IronClaude` vs `IronClaudeX`), `/pull/<N>` on origin, and fragment/trailing-`/` cases. Have the check print `E-FOREIGN-REPO` itself, with an exit code distinct from E-NO-ORIGIN.

### INV-003
ID: INV-003
CATEGORY: count_divergence
ASSUMPTION: One real item-4 run that shows `E-FOREIGN-REPO` is enough for Task 17 to record section 20 item 4 as "run" (plan:254, plan:258; every round-2 C-001 fix).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- source.md:470 has two clauses: "A claim URL for any repo other than origin stops with `E-FOREIGN-REPO`; no `gh` call is made without `--repo <origin repo>`."
- plan:254 maps only the first clause. A-004 (all three round-2 tables) covers how `gh api` paths are spelled, not where the second clause is recorded in Task 17.
- Read literally, the second clause cannot hold. The spec's own calls `gh auth status` (source.md:144), `gh api user -q .login` (source.md:148) and `gh api -X PATCH repos/<R>/...` (source.md:178) take no `--repo` flag.
- Falsifying downstream condition: marking item 4 "run" on the E-FOREIGN-REPO output alone over-claims the second clause. That is a false claim in the acceptance record under the plan's own "states the truth" rule (plan:236 pattern, plan:257).
- Fix: split the item-4 row. Clause 1 is the real run. Clause 2 points at the Task 7 fork-safety test (plan:131) plus the A-004 `repos/<R>/` assertion, and states that `gh auth status` and `gh api` carry the repo in the path, not a flag.

### INV-004
ID: INV-004
CATEGORY: sufficiency_challenge
ASSUMPTION: C-003's fix ("put `--repo <R>` in the section-14 table cells, or scope 'runs gh' to code spans and fenced lines starting with `gh`", round2-v3.md:81) alone removes the conflict between required content and the fork-safety scans.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- There is a second scan with the same rule. Task 3's test (plan:58) requires "every `gh issue`, `gh pr` and `gh label` line in a body carries `--repo`". Its required body content (plan:56) is the workers' prohibition: they never write to GitHub. The natural wording, "never run `gh issue edit`, `gh issue comment` or `gh issue create`", is a backticked span that starts with `gh` and has no `--repo`. It trips plan:58, and also plan:131, which scans the agent bodies too. Option 2 of the fix does not exempt it, because the span starts with `gh`. Option 1 names only the section-14 cells.
- SKILL.md must state the orchestrator-only write rule (plan:111). source.md:320 words it as the list "`gh issue edit`, `gh issue comment`, `gh api -X PATCH`, `gh issue create`", with no `--repo`. That is the same class as source.md:336 and :340, and the fix does not name it.
- plan:131 bans the `{owner}/{repo}` placeholder in every skill and agent file. The section-13 rule an author would copy says "never `{owner}/{repo}`" (source.md:319), so copying the spec sentence fails the test. V1's "never write the placeholder even in prose" (diff-analysis.md:48, U-004) is not in the agreed C-003 fix.
- Fix: define the scan once for both tests. Every code span or fenced line that starts with `gh issue|pr|label` carries `--repo`, including prohibitions (write them as "`gh issue comment --repo <R>`"). Tell authors to write the placeholder rule without the literal token, for example "never a brace placeholder". Name plan:58 in the fix.

### INV-005
ID: INV-005
CATEGORY: interaction_effects
ASSUMPTION: The C-002 "single exit" fix, the C-006 "explicit end-of-Task-17 approval request", A-006's "the user's reply naming the task is the approval", and Task 16's "Ask the user only for the test issue URL and task ID" (plan:243) can each be carried out by the `/sc:implement` executor. Also, C-001 step 3's "post-Task-13 session" condition can be met on a normal run.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- src/superclaude/skills/sc-implement-protocol/refs/qa.md:288: "No other path may stop automation or prompt the user." Lines 278-286 list the seven allowed interrupts. None is a task-body request to restart, to name a task, or to approve a live run.
- src/superclaude/skills/sc-implement-protocol/SKILL.md:4: `allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, Skill`. The tool list has no AskUserQuestion.
- V2 used this same rule to show that "approval at that moment" never fires (round2-v2.md:88-91). The same rule also blocks the agreed remedy, "add one explicit ask" (round2-v2.md:109, round2-v3.md:134). By the literal text, the only conforming exit for Tasks 15, 16 and 17 is pending.
- The session that runs Tasks 1-14 in source order (SKILL.md:97) necessarily started before Task 13. The workers load only at session start (plan:233), and item 4 needs "a session that has the skill loaded (after Task 13)" (plan:254). So on the first pass, Task 15's smoke spawns and the item-4 run are always pending, unless the executor takes a stop the closed list does not grant. No later task or follow-up schedules them, which leaves source.md:473 (AC 7 smoke half) and source.md:470 unverified by design.
- This is not blocking: plan:15 and plan:236/246/258 allow truthful pending rows. It does falsify "C-002/C-006 fixes alone resolve" the gap. Whether a newly written skill becomes available mid-session without a restart was not checked (UNVERIFIED); that question affects only item 4, not the workers.
- Fix: make pending the single exit everywhere. End Task 17's artifact with a short post-restart runbook in source order: export the ClickUp variables, start a new session, run Task 15's spawns, run Task 16, run item 4. Or cite which closed-list row allows the stop.

### INV-006
ID: INV-006
CATEGORY: state_variables
ASSUMPTION: The Wave 2 `E-NOT-AN-ISSUE` STOP is "out of this plan's scope, so it is noted only" (round2-v2.md:96). The consensus treats it as a second barrier that only a fault can bypass (round2-v1.md:41, round2-v3.md:50).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- The orchestrator decides Wave 2 from `<D>/scout.md` alone (source.md:154). Task 4 defines the scout-report claim section as "state, assignees, current login, earlier claim and accuracy-check comment IDs, merged PRs ..., complexity and type guesses" (plan:78). It has no `url` or pull-request field, although Wave 1 fetches `url` (source.md:148).
- For an OPEN pull request, `state` is `OPEN`, the same as an issue. Per E4 (evidence-sheet.md:8), `gh issue view <PR number>` answers rather than failing. The guard therefore has no input. A user who types an open PR number (no fault needed) reaches Wave 3 `gh issue edit --add-assignee` (source.md:162) and two comments (source.md:178-179) on the PR. Whether `gh issue edit` accepts a PR number was not checked (UNVERIFIED); comments land either way.
- It is in scope. Task 4 writes the template and already goes beyond the spec field list ("whether that list was truncated", plan:78). One more field is the same kind of disclosed addition.
- No AC or test covers E-NOT-AN-ISSUE. Section 20 has none, and Task 6 checks only that the code string is present (plan:116).
- Fix: in Task 4, add `url` and `is_pull_request` (true when `url` contains `/pull/`) to the scout claim section, with an AC. In Task 5, make claim.md's Wave 2 STOP read that field.

### INV-007
ID: INV-007
CATEGORY: sufficiency_challenge
ASSUMPTION: A-006's fix, "compare the reported `task_id` with the named ID after the first run; on a mismatch make no second run" (round2-v3.md:93, round2-v1.md:62), resolves the wrong-task exposure.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- The script makes its PUT inside the first run (source.md:309). The comparison runs only after that write, so a mismatched task has already gained the user as assignee. The fix prevents only the second write.
- A mechanism that works before the run is already in scope. `CLICKUP_LIST_IDS` narrows the search to given lists (plan:43, source.md:298). The user can export it with the test task's list in the same pre-session step that plan:23 and plan:243 already require.
- Fix: in Task 16, ask the user to export `CLICKUP_LIST_IDS` set to the test list. On a mismatch, record the wrong `task_id` and tell the user to remove the assignment, rather than only skipping the second run.

### INV-008
ID: INV-008
CATEGORY: count_divergence
ASSUMPTION: The 19-row Round 2 tables are the whole consensus ledger, and the minors outside them carry over.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- The tables (round2-v1.md:90-110, round2-v2.md:100-120, round2-v3.md:125-145) rule only the 19 diff points. Several unique contributions have no disposition row: U-010 / S-5 `permissionMode: plan`, U-012 / S-7 tier-proxy rewrite, U-013 / S-8 `__pycache__`, U-015 / S-10 D26 wording, U-003 / A-6 invalid `CLICKUP_MAX_PAGES` (diff-analysis.md:54-60, :47).
- The only file that disposes them is base-selection.partial-1240.md:138, which pipeline.log marks "possibly partial ... not trusted".
- S-5 is the costly one if it is dropped. src/superclaude/agents/evidence-validator.md:8 carries `permissionMode: plan`, and plan:56 says to follow that file's frontmatter shape. Nothing in the Task 3 test (plan:58) or its ACs (plan:61-63) forbids the key. A copied key puts every worker in plan mode, so every live claim or create ends `E-WORKER-NO-OUTPUT` (source.md:335) and every Task 15 smoke spawn fails. A-6 is already covered by plan:43 and plan:45 (define and test the behaviour).
- Fix: the merge step should carry S-5 (Task 3 test asserts there is no `permissionMode` key), S-7 (Task 15 accepts a tier-member model in the external evidence when the log maps it to the picker ID), S-8 and S-10 as minors with explicit rows.

### INV-009
ID: INV-009
CATEGORY: guard_conditions
ASSUMPTION: With a non-existent issue number, plan:259 stays true even if both Wave 0 and Wave 2 fail, and ClickUp is never reached (round2-v1.md:49-50, N3).
STATUS: ADDRESSED (provided INV-001's URL correction is applied)
SEVERITY: LOW
EVIDENCE:
- source.md:162 and source.md:336: `gh issue edit --add-assignee` failing gives "STOP `E-ASSIGN-FAILED` before ClickUp and before any comment". source.md:163 runs ClickUp only after the assign.
- If that stop is also ignored (a third fault), `gh issue comment 999999999 --repo <R>` has no target and gives `E-POST-FAILED` (source.md:339). ClickUp rule 2's `#999999999` (source.md:307) has no plausible match.
- No falsifying downstream condition was found for a URL whose only number is 999999999. The residual risk sits in the URL choice (INV-001).

### INV-010
ID: INV-010
CATEGORY: collection_boundaries
ASSUMPTION: C-005's fix (each test clears all four `CLICKUP_*` variables) together with plan:50's `env -u` of two variables leaves no real environment reaching a test or check.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE:
- plan:43 reads four variables. plan:45 clears two. The agreed fix clears all four (round2-v1.md:98, round2-v3.md:133).
- plan:50's AC run unsets the token and workspace, and source.md:302's step 1 exits `skipped` before `CLICKUP_LIST_IDS` or `CLICKUP_MAX_PAGES` is read. So an exported list or page cap cannot change that output.
- The plan:23 vs plan:50 wording conflict (`env` banned, `env -u` used) is merged into C-005 with the rewording "`env -u` to unset it is allowed" (round2-v3.md:34). No falsifier found.

### INV-011
ID: INV-011
CATEGORY: sufficiency_challenge
ASSUMPTION: A-003's fix, a static test that the next-steps template's first line is the `/model` tier line (round2-v1.md:105, round2-v3.md:140), together with Task 7's flag-existence check, covers section 20 item 8.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE:
- source.md:474 requires that next-steps.md "contains only commands and flags listed in section 19". Task 7 checks that each chains.md flag exists in its command file (plan:129). That is weaker than the section-19 allowlist: a flag can exist in brainstorm.md without being among section 19's listed flags.
- next-steps.md follows `/sc:recommend` when it differs from the default row (source.md:438, D23). Its output can therefore carry flags that no static test of chains.md or the template sees.
- The Task 17 item-8 row must stay pending until a live claim. The static half should be described as "template and default rows", not as item 8.

### INV-012
ID: INV-012
CATEGORY: sufficiency_challenge
ASSUMPTION: Moving C-001, C-002 and C-003 down to minor is supported under the binding rule (blocking = wrong behaviour, a false claim, a missing required deliverable, or a security or data-loss risk).
STATUS: ADDRESSED for C-002 and C-003; conditional for C-001
SEVERITY: LOW
EVIDENCE:
- C-002: resume works through the start line plus Row S (refs/ledger.md:161; round2-v3.md:9-11). The defect is two exits (plan:233 vs plan:236), which is a wording issue. Supported.
- C-003: the conflict is satisfiable and surfaces as a red test that Task 7 fixes (plan:135). Supported, with INV-004's wider instance set.
- C-001: the downgrade rests on the escape landing "reversibly on the user's fork PR #1" (round2-v3.md:129). That holds for the octocat URL and for a fixed URL whose only number is 999999999. It does not hold for the example URL the consensus wrote down (INV-001). C-001 stays minor only if the fix uses a URL with no stray digits.


## Missed blocking defects

None found. Two items come close, and neither meets the binding rule. INV-001 (HIGH) is a defect in the consensus fix, not in the plan as written. INV-006 (MEDIUM) is a latent gap in the data path: plan:92 does require refs/claim.md to carry the pull-request STOP, so no deliverable is missing and no plan statement is false. Both should be fixed before Task 17's live run.

Self-audit (what was checked and why no blocking defect was concluded):
- **Section 15, Create rows (13 paths).** Mapped to Tasks 1-8:
  - `origin_repo.py`: Task 1.
  - `clickup_claim.py`: Task 2.
  - the three agents: Task 3.
  - the 14 templates: Task 4, counted one by one against source.md:359.
  - the 5 refs: Task 5.
  - `SKILL.md`: Task 6. Its return-contract fields match source.md:353, and its 9 STOP codes match section 14.
  - `issue.md`: Task 8.
- **Section 15, Change rows (7).** Task 10 covers HOW-WE-WORK, the plugin copy and `_OTHER_COMMANDS`. Task 11 covers the developer guide. Task 12 covers commands.md. Task 9 covers `test_issue_body_templates.py` and `_POST_REFRESH_ADDITIONS`. The "Not changed" list is honoured at plan:25.
- **Section 16, test rows (8).** Covered by Tasks 1, 2, 3, 7, 8 (new files) and Tasks 9, 10 (changed files). The replacement of `test_no_issue_skill_or_command_added` is Task 9, and its target exists at tests/cli/test_issue_body_templates.py:78-85. `test_claude_md_has_exactly_one_issue_rule_line` (line 57) is kept.
- **Section 17, items 1-5.**
  - Item 1: plan:20.
  - Item 2: Task 13 (`make sync-dev`, `make verify-sync`).
  - Item 3: Task 10, plain copy plus `cmp`, and `uv run pytest tests/core tests/commands`.
  - Item 4: Task 13, the path grep.
  - Item 5: the PR, explicitly deferred at plan:25 with the exact `/sc:pr-submit --monitor 3` command.
- **Section 20, items 1-9.** Each has a Task 17 row (plan:254, plan:257). The gaps are INV-003 (item 4, second clause), A-002 (item 5, first half) and INV-011 (item 8). None is a missing deliverable, because a pending row is allowed by plan:15.
- **Scheduled smoke checks.** One spawn per worker is Task 15 (source.md:434 D19, :473). The manual ClickUp claim is Task 16 (source.md:314).
- **Final full-suite step.** Task 14 runs `uv run pytest` (Makefile `test`), `make lint` and `make verify-sync`, plus the targeted run of source.md:400.
- **Plan statements checked against the repo.** All are true:
  - tests/skills/test_workflow_archive.py:24-27 loads archive_workspace.py by path.
  - ccsession-models.json:70-115 has tier1a, tier2 and tier3 under `tiers`.
  - evidence-validator.md:1-9 has the frontmatter shape (and the `permissionMode: plan` trap, INV-008).
  - tests/recommend/test_routing_refresh.py:32 has `_POST_REFRESH_ADDITIONS = {"graph", "impact"}`, and :613 has `test_command_dispositions_trace_appendix_c_and_inventory`. The :643 check `shipped - _POST_REFRESH_ADDITIONS == active` is why Task 9 is required.
  - tests/core/test_how_we_work_routing_table.py:27 has `_OTHER_COMMANDS`; :143 `_command_text`; :258 `test_every_notes_flag_exists_in_its_command`; :290 `test_other_commands_membership_and_live_references` (set equality at :296); :341 `test_guide_is_ascii_except_the_ruling_example`.
  - The other-commands markers exist in src/superclaude/core/HOW-WE-WORK.md.
  - tests/commands/test_routing_plugin_parity.py exists.
  - The developer guide has `### 4.1` at :388, `### 4.3` at :463 and `### 4.4` at :482.
  - docs/user-guide/commands.md has `### 8. UTILITIES` at :105 and the `/sc:graph` anchor link at :114.
  - src/superclaude/skills/task/SKILL.md exists.
  - Every chain flag in source section 9 exists in its src command file (brainstorm, workflow, design, troubleshoot, analyze; checked one by one).
- **Repo-wide tests the new files could break.** None found:
  - tests/agents/test_tavily_tool_parity.py: the new files declare no Tavily tools.
  - tests/agents/test_codegraph_rosters.py: it checks only four named agents.
  - tests/docs/test_retired_docs_absent.py: it checks link targets only.
  - tests/skills/test_codegraph_adoption.py: its Serena-name scan is not tripped.
  - src/superclaude/cli/install_skills.py:40-59: `sc-issue-protocol` does not map to `commands/issue-protocol.md`, so it installs standalone.
  - Makefile:117 and :178: sync-dev and verify-sync both exclude `__pycache__`.
  - The `.dev/issues/` scratch is not gitignored (.gitignore has no such entry), but `/sc:pr-submit` stages only explicit paths (sc-pr-submit-protocol SKILL.md:274). So the Task 15 smoke folder cannot be swept into a commit by that path.
- **Not checked.** Running any test. Any gh call (the state of #302, and `gh issue edit` on a PR number). Whether skills hot-load mid-session. These are marked UNVERIFIED where they are used.

## Summary

| Status | HIGH | MEDIUM | LOW | Total |
|---|---|---|---|---|
| UNADDRESSED | 1 (INV-001) | 7 (INV-002, 003, 004, 005, 006, 007, 008) | 1 (INV-011) | 9 |
| ADDRESSED | 0 | 0 | 3 (INV-009, 010, 012) | 3 |
| Total | 1 | 7 | 4 | 12 |

- The consensus verdict, PASS with notes, survives: no blocking plan defect was found (see above).
- The consensus's headline fix needs a correction before it is applied. INV-001: the example URL embeds `302`, the number of the real issue on origin. With that URL, plan:259 can fail under the same Wave 0 faults the fix is meant to absorb, and C-001's minor grade loses its "reversible on own fork #1" basis (INV-012).
- Three agreed fixes are insufficient on their own:
  - C-003 misses the Task 3 scan and the prohibition and placeholder wording (INV-004).
  - C-002, C-006 and A-006 rely on prompts the executor's closed interrupt list and tool list do not allow (INV-005).
  - A-006 compares the task only after the ClickUp write (INV-007).
- Ledger hole: the S-5 `permissionMode: plan` trap and the other unique contributions have no disposition row in the Round 2 tables (INV-008).

