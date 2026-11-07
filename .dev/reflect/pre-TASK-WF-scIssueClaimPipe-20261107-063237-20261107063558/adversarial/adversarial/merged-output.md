# Merged review card: TASK-WF-scIssueClaimPipe-20261107-063237

<!-- Source: Base (original) header, verdict and counts rewritten per Changes 1-10 -->

- **Subject:** the plan `.dev/tasks/to-do/TASK-WF-scIssueClaimPipe-20261107-063237/TASK-WF-scIssueClaimPipe-20261107-063237.md` ("plan"), which adds `--pipeline worktree|full|none` and `--submit` to `/sc:issue --claim`, checked against the design snapshot `source.md` in the same folder.
- **Mode:** pre
- **Verdict:** FAIL, because blocking findings exist.
- **Counts:** 6 blocking findings (B-1 to B-6); 14 non-blocking findings, which are 6 Drift MEDIUM (M-1 to M-6) and 8 minor findings and notes (m-1 to m-8). Separately, 3 advisory correctness gaps (A-1 to A-3), which never gate.
- **Class:** every finding is Drift. Regression is not used (see Rejected or withdrawn).
- **Fix location vocabulary:** **plan only** means the plan author can fix it by editing the plan; **design first** means `source.md` (and `docs/designs/sc-issue-claim-pipeline-flag.md`) must change before the plan is right.
- **Not checked:** pytest was not run. Every file:line below was re-Read.

## Blocking findings

<!-- Source: Base (original) finding 2, reclassified per Change 1; Invariant probe INV-001 and INV-002 merged per Change 2 -->

### B-1 The plan never accounts for the write-verb audit

- **Class:** Drift. **Severity:** HIGH
- **Location:** plan:64, plan:105-107, plan:130-133 (Tasks 2, 5 and 7). Base location: plan:30-33, 49-64, 95-108, 128-135.
- **What diverged:**
  - The plan never mentions the write-verb audit in `tests/skills/test_worker_contract.py`. That audit scans every file under the skills, commands and agents folders for `git add`, `commit`, `push`, `merge`, `stash`, `update-ref`, `worktree add|remove` and `gh pr|api`.
  - Each hit must be classified by its exact stripped line text. `test_every_write_verb_hit_is_classified` and `test_classification_table_has_no_stale_entries` fail on an unclassified hit or on an edited classified line.
  - Task 5's template contains "Do not run ... git commit, git push" and `git push`, and Task 2's grep expects such text in the script. No task names `test_worker_contract.py`.
  - The suite will certainly fail from Task 5 on. The first gate that catches it is Task 7's `tests/skills` run, and no task tells the implementer how to fix it.
  - INV-002: Tasks 1, 3 and 4 also edit files in the audited roots. The template's push and commit lines, which the launched agent runs, fit none of the five categories. A read-only label is checked only for `gh api` lines.
  - INV-001 (LOW within this finding): SKILL.md:72, SKILL.md:135 and refs/claim.md:9 are already classified. Editing any of them without updating its key fails the stale-key test. The probe's claim that `--submit` makes those lines false is rejected.
- **Evidence:**
  - tests/skills/test_worker_contract.py:1090-1094 (AUDIT_ROOTS), :1098-1101 (WRITE_VERB_RE), :1103-1105 (the five categories)
  - tests/skills/test_worker_contract.py:1131-1152 (`_scan_write_verbs`), :1155-1162 (`_check_all_classified`)
  - tests/skills/test_worker_contract.py:2125-2179 (sc-issue keys), :2199-2200, :2203-2208 (the two tests), :2220-2226 (the read-only check, `gh api` only)
  - src/superclaude/skills/sc-issue-protocol/SKILL.md:72, :135; src/superclaude/skills/sc-issue-protocol/refs/claim.md:9
  - plan:64, plan:105-107, plan:133; source.md:309-310 (the design's change table leaves out the test file)
- **Orchestrator verification:** AUDIT_ROOTS, WRITE_VERB_RE, `_scan_write_verbs` and the two tests were re-Read at tests/skills/test_worker_contract.py:1090-1155 and 2199-2205.
- **Fix:**
  - Name `tests/skills/test_worker_contract.py` in every task that adds or edits a write-verb line (Tasks 1 to 5 and 7), and add it to their acceptance runs.
  - State that each new hit needs an exact-text classification entry with one of the five categories. Decide which category the template's push and commit lines get.
  - When a task edits an already-classified line, update its key in the same task.
  - Also add the file to the design's change table (source.md:309-310). This is not a precondition.
- **Fix location:** plan only. **Sources:** V1 finding 2; INV-001; INV-002; Round 2 (all three advocates: Drift HIGH)

<!-- Source: Base (original) finding 3; Variant 3 advisory 2, INV-003, INV-005 merged per Change 3 -->

### B-2 The worktree output carries no tracked-files data

- **Class:** Drift. **Severity:** MEDIUM-HIGH
- **Location:** plan:49, plan:57, plan:84; source.md:177, source.md:195
- **What diverged:**
  - The skill prints "untracked, do not stage" only when no file under `<wt>/.dev/issues/<N>/` is tracked. The `worktree` output (`status, path, branch, match_key, warning, detail`) has no tracked-file field; tracked files appear only in the free-text `detail`.
  - The script owns every worktree git call, so Task 4's claim.md step has no way to know the answer.
  - INV-005: the field belongs in the subcommand's stdout (a fixed key set, plan:49), not in the `worktree.json` `{path,status}` record (source.md:197). Adding it to the record would change the record guard and the launch inputs.
  - INV-003 (data loss): when `git ls-files` fails, `run()` returns a failed result and does not raise (plan:34). The tracked set then reads as empty, and a differing tracked file is renamed to `.prev` and overwritten. Neither source.md:195 nor plan:57 makes the copy fail in that case.
- **Evidence:** source.md:158, :165, :177, :195, :197; plan:34, plan:49, plan:57, plan:84
- **Fix:**
  - Amend design §8.3 to add a machine-readable tracked-files field to the `worktree` stdout. The field must tell "none tracked" apart from "unknown".
  - When `git ls-files` fails, the copy must fail without overwriting any differing file.
  - Then Task 2 implements and tests both, and Task 4's claim.md step reads the field.
- **Fix location:** design first. **Sources:** V1 finding 3; V3 advisory 2; INV-003; INV-005

<!-- Source: Variant 3 advisory 3 (C-013) and INV-007, merged per Change 4 -->

### B-3 The launch prompt is not fork-safe

- **Class:** Drift. **Severity:** HIGH (security: exposure to the wrong repository; INV-007 grade; debate C-013 was MEDIUM before the probe)
- **Location:** plan:101 (the template's `submit` block); source.md:226
- **What diverged:**
  - The `submit` block's "check that no PR is already open" step can be written as `gh pr list --head <branch>` with no `--repo`.
  - The fork-safety scan covers only `_FORK_FILES` (SKILL.md, refs/*.md and the agents). Templates are not in that set.
  - A launched agent could therefore reach the upstream repository while every test passes. The same gh line is also a write-verb hit (B-1).
- **Evidence:** source.md:226; plan:101; tests/skills/test_issue_protocol.py:288 (`_FORK_FILES`); tests/skills/test_issue_worker_agents.py:31-48 (`gh_lines_missing_repo`)
- **Fix:**
  - Design §9: every gh call in the `submit` block names `--repo IronbellyOrg/IronClaude`.
  - Design §13: extend `_FORK_FILES` to cover `templates/launch-prompt.md`, or add a pin that scans it.
  - Then Task 5 writes the template to match, and Task 7 adds the test.
- **Fix location:** design first. **Sources:** V3 advisory 3 / C-013; INV-007

<!-- Source: Invariant probe INV-004, added per Change 5 -->

### B-4 The plan would replace the shared return contract

- **Class:** Drift. **Severity:** MEDIUM (blocking)
- **Location:** plan:130 ("replace the claim-mode return contract"); source.md:241
- **What diverged:**
  - SKILL.md:101-115 is one return contract shared by both modes. It carries `status`, `issue_number` and `next_steps_path`, and source.md:161 still needs `status`.
  - The design says the ten fields "replace" the fixed list for claim mode, and Task 7 repeats that.
  - A literal replacement drops those fields or changes create mode. ST-10 only checks that the ten fields are present, so it would still pass.
- **Evidence:** src/superclaude/skills/sc-issue-protocol/SKILL.md:101-115; source.md:161, :241, :244-253, :356; plan:130
- **Fix:**
  - Design §10: extend the shared contract with the claim-mode fields instead of replacing it. Keep `status`, `issue_number`, `next_steps_path` and create mode unchanged.
  - Task 7 then edits SKILL.md to match, and ST-10 checks that the kept fields are still present.
- **Fix location:** design first. **Sources:** INV-004

<!-- Source: Base (original) finding 5; Variant 3 advisory 1 and INV-006 merged per Change 6 -->

### B-5 ST-4 has no workable matching rule

- **Class:** Drift. **Severity:** MEDIUM (blocking)
- **Location:** plan:130 (ST-4); source.md:350
- **What diverged:**
  - ST-4 bans the Orca link flags in the skill, refs, command and script, but gives no rule for matching them.
  - A substring scan fails on existing text: `--pr` is a prefix of `--prompt`; `--issue-url` and `--issue-number` already appear at refs/claim.md:49 and in clickup_claim.py; and prose such as refs/tiers.md:25 (the "`--model` flag") sits outside any orca command line.
  - The new script itself must contain `--agent`, `--prompt` and `--surface`.
  - INV-006: Task 9's format check (plan:162) wraps the launch argv, so `"--model",` sits on its own line. A line-by-line scan then misses it and cannot scope the outside-the-launch-call exemption.
- **Evidence:** source.md:350; src/superclaude/skills/sc-issue-protocol/refs/claim.md:49; src/superclaude/skills/sc-issue-protocol/scripts/clickup_claim.py:247-248; src/superclaude/skills/sc-issue-protocol/refs/tiers.md:25; plan:130, plan:162
- **Fix:**
  - Design §13 ST-4: match whole tokens only, and only on orca command lines, with the launch call excluded.
  - For `scripts/orca_worktree.py`, find the launch argv by parsing the file with `ast` instead of scanning lines.
  - Then Task 7 implements the rule.
- **Fix location:** design first. **Sources:** V1 finding 5; V3 advisory 1; INV-006

<!-- Source: Base (original) findings 6 and 9; Variant 2 findings 1-3 and Variant 3 findings 5-7 merged per Change 7 -->

### B-6 Required tests and safeguards have no owning task

- **Class:** Drift. **Severity:** MEDIUM. The Task 6 safeguards are MEDIUM (V2 grade); the ARG-1 part is LOW-MEDIUM.
- **Location:** plan:41-43 (Task 1), plan:86, plan:116, plan:119 (Task 6), plan:130 (Task 7)
- **What diverged:** no task owns the following required deliverables.
  - (a) LA-7 (source.md:340) is not among LA-1 to LA-6 (plan:119).
  - (b) ARG-1 (source.md:341) must hold for every subcommand. Task 1 can test only `preflight`, and a missing-required-argument check cannot be tested on `preflight` (plan:41-43). `worktree`, `prompt` and `launch` get no ARG-1 case.
  - (c) The ST-5 template row (source.md:351) is not pinned.
  - (d) ST-6 has no Wave 8 half (source.md:352). Wave 8 exists only after Task 7.
  - (e) Task 6 drops design step 5's timeout instruction that `detail` must say to check Orca before re-running (source.md:211; D9 at :377). A timeout writes no `launch` entry, so `already_launched` does not catch a re-run, and a duplicate agent can start.
  - (f) Task 6 drops the `hand_command` note that a hand-started agent is not governed by the hook (source.md:211).
  - (g) Task 6 drops "The pending record stays" (source.md:212). LA-3 asserts none of (e) to (g).
- **Evidence:** source.md:211, :212, :340, :341, :351, :352, :377; plan:41-43, plan:116, plan:119, plan:130
- **Fix:**
  - Task 6: add an LA-7 case. Copy source.md:211-212 into Task 6's steps, with LA assertions for (e) to (g).
  - Tasks 2, 5 and 6: add one ARG-1 case each, for `worktree`, `prompt` and `launch`.
  - Task 7: pin the ST-5 template row and add the ST-6 Wave 8 half.
- **Fix location:** plan only. **Sources:** V1 findings 6 and 9; V2 findings 1-3; V3 findings 5-7

## Non-blocking findings (Drift, MEDIUM)

<!-- Source: Base (original) finding 1, reclassified per Change 1, merged per Change 8 -->

### M-1 The inventory test is red between tasks

- **Class:** Drift. **Severity:** MEDIUM
- **Location:** plan:30 and plan:95 (the tasks that create the files); plan:86 and plan:130 (where the table rows arrive, late)
- **What diverged:**
  - The two-way inventory test requires a files-table row for every file under refs, templates and scripts.
  - Task 1 creates `scripts/orca_worktree.py`, but its row arrives in Task 4. Task 5 creates `templates/launch-prompt.md`, but its row arrives in Task 7.
  - The acceptance runs of Tasks 1, 2, 3, 5 and 6 use `-k` or single-file filters, so they never run the whole file.
  - The gap closes by itself and never gates: at Task 4's acceptance for the script row (plan:89 runs the whole test_issue_protocol.py), and at Task 7's (plan:133) for the template row.
- **Evidence:** tests/skills/test_issue_protocol.py:131-141; plan:41, 62, 75, 89, 106, 119, 133
- **Fix:** add the files-table row in Task 1 (for the script) and in Task 5 (for the template).
- **Fix location:** plan only. **Sources:** V1 finding 1; Round 2

<!-- Source: Base (original) finding 4; INV-008 merged per Change 8 -->

### M-2 One warning field, and no `enforcement_hook` value on `already_launched`

- **Class:** Drift. **Severity:** MEDIUM
- **Location:** plan:116, plan:119; plan:56-59
- **What diverged:**
  - The `launch` output has one `warning` field, but W-ENFORCEMENT-ABSENT and W-LAUNCH-NOT-CCSESSION can both apply to a launched result. The design does not say which takes precedence.
  - A temporary HOME has no hook script, so `enforcement_hook` is missing in LA-5 too.
  - For `already_launched`, the design returns before step 3, so `enforcement_hook` has no defined value.
  - INV-008: the `worktree` step has the same collision. W-ORIGIN-BASE-STALE and the `.prev` W-WORKTREE-COPY-FAILED can both apply. plan:59 keeps only the code that set the status, so the remedy for the other code is lost.
- **Evidence:** source.md:203, :208-209, :212, :253; plan:56-59
- **Fix:**
  - The design states the precedence, or makes `warning` carry every code that applies, for both `launch` and `worktree`.
  - The design defines `enforcement_hook` on `already_launched`.
  - Then Tasks 2 and 6 follow the design.
- **Fix location:** design first. **Sources:** V1 finding 4; INV-008

<!-- Source: Variant 3 finding 4 (C-007); Base (original) findings 7 and 8 merged per Change 8 -->

### M-3 Stale claim text in SKILL.md and commands/issue.md

- **Class:** Drift. **Severity:** MEDIUM for SKILL.md steps 6 and 7; LOW for the two `description` fields and the other command text
- **Location:** plan:70-72, plan:86, plan:130
- **What diverged:**
  - SKILL.md:87-88: step 7 says "Print the next-steps.md path and STOP". Task 4 changes step 7 only so that it continues to the worktree step, and Task 7 never adds the Wave 5 prompt call or Wave 8 to steps 6 and 7. A reader who follows SKILL.md stops before the launch.
  - The frontmatter `description` of SKILL.md (:3) and of commands/issue.md (:3) still says the claim then stops. The design names the SKILL.md description (source.md:303), but Tasks 4 and 7 leave it out, and the design leaves out the command's description.
  - issue.md:71 ("After a claim, open next-steps.md and run its commands in your own session") and issue.md:100 (Related Commands) are not in Task 3.
  - The Outputs row (issue.md:68) will list launch-prompt.md, although that file is not written for `--pipeline none` (source.md:236).
- **Evidence:** src/superclaude/skills/sc-issue-protocol/SKILL.md:3, :87, :88; src/superclaude/commands/issue.md:3, :68, :71, :100; source.md:236, :302-303
- **Fix:**
  - Tasks 4 and 7 rewrite SKILL.md steps 6 and 7 to cover Waves 5, 7 and 8 at each level, and update SKILL.md:3.
  - Task 3 updates issue.md:3, :68, :71 and :100. The Outputs row says that launch-prompt.md is not written for `none`.
- **Fix location:** plan only. **Sources:** V3 finding 4 (C-007); V1 findings 7 and 8; V2 finding 4

<!-- Source: Variant 3 finding 2 (C-009), merged per Change 8 -->

### M-4 Tasks 7 and 9 do not depend on Task 3

- **Class:** Drift. **Severity:** MEDIUM
- **Location:** plan:124, plan:153
- **What diverged:**
  - Tasks 7 and 9 consume Task 3's flags and STOP codes (plan:130 requires its text to match), but neither lists Task 3 as a dependency. Task 5 depends on Task 1 only (plan:97).
  - This replaces the base card's note that the task order is sound.
- **Evidence:** plan:97, plan:124, plan:130, plan:153
- **Fix:** add Task 3 to the dependencies of Tasks 7 and 9.
- **Fix location:** plan only. **Sources:** V3 finding 2 (C-009)

<!-- Source: Invariant probe INV-009, merged per Change 8 -->

### M-5 A re-claim rewrites the running agent's prompt

- **Class:** Drift. **Severity:** MEDIUM
- **Location:** source.md:145, :195, :208
- **What diverged:**
  - On a re-claim at a new level, Wave 5 rewrites launch-prompt.md (source.md:145) and Wave 7 copies it into the worktree (source.md:195). Only after that does Wave 8 return `already_launched` (source.md:208).
  - The running agent's prompt file then no longer matches the level in its launch record.
- **Evidence:** source.md:145, :195, :208
- **Fix:** the design states that, when a launch record already exists, Waves 5 and 7 do not replace the prompt file the running agent uses. The plan's tasks then follow the design.
- **Fix location:** design first. **Sources:** INV-009

<!-- Source: Round 2 new item N-001 (advocate 3), merged per Change 8 -->

### M-6 A create timeout looks the same as a failed create

- **Class:** Drift. **Severity:** MEDIUM (grouped here by the refactoring plan; Round 2 advocate 3 proposed LOW)
- **Location:** plan:34, plan:56, plan:62
- **What diverged:**
  - source.md:194 says a create that times out must be followed by a second list, while a nonzero exit fails at once.
  - Task 1's `run()` returns the same failed result for a timeout, a nonzero exit and a missing binary (plan:34).
  - Task 2 needs to tell these apart (plan:56), and no FO case tests a create timeout (plan:62).
  - The wording at source.md:165 ("a timeout is a failed command") encourages treating them the same.
  - Effect: a worktree created during a timeout is reported `failed` with no record. A rerun recovers it through the marker lookup.
- **Evidence:** source.md:165, :194; plan:34, plan:56, plan:62
- **Fix:**
  - Task 1's `run()` marks timeouts.
  - Task 2 handles a create timeout with the second list, and adds an FO case for it.
  - Optionally, reword source.md:165.
- **Fix location:** plan only. **Sources:** N-001 (Round 2)

## Minor findings and notes

<!-- Source: Variant 2 finding 5, Variant 3 findings 8-10, Variant 3 note U-004, INV-010, INV-013 merged per Change 9 -->

All items here are Drift and non-blocking. Debate points C-014 (directory modes for the pending store's intermediate folders) and C-015 (the `already_launched` time field and the naming of the `-k` filter) are recorded as A-1 to A-3 under Advisory correctness gaps.

### m-1 Constraints do not record the Orca dependency

- **Class:** Drift. **Severity:** LOW. **Location:** plan:17-26. **Fix location:** plan only. **Sources:** V2 finding 5 (C-010)
- **What diverged:** Constraints include the Orca-flag rule (plan:22) but not that `--pipeline worktree|full` depends on Orca being installed (design P1).
- **Evidence:** plan:17-26; source.md:39
- **Fix:** add the Orca dependency to Constraints.

### m-2 Task 2 is too large (note)

- **Class:** Drift. **Severity:** LOW. **Location:** plan:45-64. **Fix location:** plan only. **Sources:** V3 finding 10 (C-011)
- **What diverged:** Task 2 carries the whole `worktree` subcommand: create, list again, copy, record and warning.
- **Evidence:** plan:45-64; source.md:189-197
- **Fix:** optionally, split Task 2.

### m-3 The format check runs only in Task 9 (note)

- **Class:** Drift. **Severity:** LOW. **Location:** plan:162. **Fix location:** plan only. **Sources:** V3 finding 9 (C-011, partly withdrawn in Round 2)
- **What diverged:** the implement protocol runs `make lint` after every task as a non-gating extra, which is why most of V3's lint point was withdrawn. The format check is not among those extras, so `ruff format --check` first runs in Task 9.
- **Evidence:** plan:162; ~/.claude/skills/sc-implement-protocol/SKILL.md:146, :152; Makefile:48-50
- **Fix:** run the format check in every task that edits `scripts/orca_worktree.py` (Tasks 1, 2, 5 and 6).

### m-4 Design-doc edits placed in Phase 3

- **Class:** Drift. **Severity:** LOW. **Location:** plan:139-149 (Task 8). **Fix location:** plan only. **Sources:** V3 finding 8 (C-011)
- **What diverged:** design §16 places the design-doc edits in Phase 1 (source.md:405), but the plan puts them in Phase 3. Both phases ship in one PR.
- **Evidence:** source.md:405; plan:139-149
- **Fix:** move Task 8 earlier, or record why it moved.

### m-5 The pending store only grows

- **Class:** Drift. **Severity:** LOW. **Location:** source.md:212. **Fix location:** design first. **Sources:** INV-010
- **What diverged:** the design says "The pending record stays", but the hook that would consume pending records (#394) is not built, so nothing ever cleans them up.
- **Evidence:** source.md:212
- **Fix:** the design states who prunes pending records, or records that they keep growing until #394 lands.

### m-6 Task 9 never runs tests/docs

- **Class:** Drift. **Severity:** LOW. **Location:** plan:160. **Fix location:** plan only. **Sources:** INV-013
- **What diverged:** Task 9's test list leaves out `tests/docs`, although that folder exists.
- **Evidence:** plan:160; tests/docs/test_retired_docs_absent.py
- **Fix:** add `tests/docs` to Task 9's test list.

### m-7 The HOW-WE-WORK row must be ASCII

- **Class:** Drift. **Severity:** LOW. **Location:** plan:160 (Task 9). **Fix location:** plan only. **Sources:** INV-013
- **What diverged:** the new `/sc:issue` routing row must be ASCII-only, and Task 9 does not say so.
- **Evidence:** tests/core/test_how_we_work_routing_table.py:342-347; plan:160
- **Fix:** state the ASCII-only rule in Task 9.

### m-8 The literal `--repo` is banned in commands/issue.md (note, ADDRESSED)

- **Class:** Drift. **Severity:** LOW. **Location:** plan:75 (Task 3 acceptance). **Fix location:** plan only. **Sources:** V3 note (U-004); INV-012
- **What diverged:** nothing. `tests/commands/test_issue_command.py` asserts that the literal `--repo` does not appear in issue.md, and Task 3's acceptance run executes that test. The note is kept so the implementer writes the fork rule in issue.md without the literal flag.
- **Evidence:** tests/commands/test_issue_command.py:99-103; plan:75
- **Fix:** none needed; the implementer only needs to be aware of it.

## Advisory correctness gaps (non-gating)

<!-- Source: Base (original) correctness_gaps_advisory, kept per Change 10 -->

### A-1 Directory modes in the pending store

- **Class:** Drift. **Severity:** LOW. **Location:** source.md:120. **Fix location:** plan only. **Sources:** V1 advisory 1 (C-014)
- **What diverged:** `os.makedirs(mode=0o700)` applies the mode only to the leaf directory, so the intermediate state directories get default modes. LA-2 asserts only the pending directory.
- **Evidence:** source.md:120, :335
- **Fix:** create each level with mode 0o700, or chmod the parent directories, and extend LA-2 to the intermediate directories.

### A-2 Which field carries the `already_launched` time

- **Class:** Drift. **Severity:** LOW. **Location:** plan:116. **Fix location:** plan only. **Sources:** V1 advisory 2 (C-015)
- **What diverged:** the schema has `launched_at`, but the prose says "its at time", and plan:116 does not say which field carries it.
- **Evidence:** source.md:159, :203, :208; plan:116
- **Fix:** Task 6 names `launched_at` as the field.

### A-3 The `-k` filter selects the whole module

- **Class:** Drift. **Severity:** LOW. **Location:** plan:62. **Fix location:** plan only. **Sources:** V1 advisory 3 (C-015)
- **What diverged:** `-k "FO or worktree"` matches the module name `test_issue_orca_worktree.py`, so it selects the whole file. The filter's name overstates its scope.
- **Evidence:** plan:62
- **Fix:** drop the filter, or name the test ids.

## Rejected or withdrawn

<!-- Source: refactor-plan.md "Changes NOT Being Made" -->

| Diff point | Rejected alternative | Why rejected |
|---|---|---|
| S-002, X-001 | V1 and V3's Regression label for the test-order window | Round 2: all three advocates accepted Drift. The final repository state is correct, and the check is non-gating. |
| X-004 / V3 finding 5 | "ARG-1 and LA-7 never named" at MEDIUM, as written | Overstated: Task 1 tests a bad-subcommand exit, and Task 5 tests `--submit` with `worktree`. Only the missing per-subcommand coverage is kept (B-6). |
| Wave 6 hand-off overlap | V1's new LOW issue | Advocates 2 and 3 showed that plan:124-133 gives Task 7 the final wording. Not a separate defect. |
| C-011 lint gate | V3 finding 9 as a deviation | Withdrawn in Round 2: `make lint` runs after each task as a non-gating extra (~/.claude/skills/sc-implement-protocol/SKILL.md:132-154). The format-check gap is kept as m-3. |
| INV-001 premise | The probe's "`--submit` makes the classified lines false" | The classified lines describe the skill, which remains the only writer. A launched agent is a separate session. |
| A-005 | "Green between tasks is required" | Rejected as a universal rule. Only the acceptance gates and the final state must be green. |
