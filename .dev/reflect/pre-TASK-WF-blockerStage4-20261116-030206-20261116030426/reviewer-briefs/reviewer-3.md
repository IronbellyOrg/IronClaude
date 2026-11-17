# Reviewer brief 3 (persona: refactorer; model class: opus)

## T1 card excerpt

## Resolution of the earlier review (`.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md`, findings that touch stage 4)

- F3/F9/F13 (plugin-mirror allow-list ordering): resolved in Task 6. The plugin mirror of `refs/rule.md` is added to the `canonical` registry rows and to the "Merge-rule allow-list" of `refs/scale-map.md` by path only, then the folder is copied, then the three tests run (P4:99). The existence check on every allow-listed file (OLD:477, stage 3 request) would fail between the allow-list edit and the copy, but no test is run between them.
- F4 (analysis template): resolved. `agent_template_analysis.md` gets the merge-rule text only and the registry keeps 11 `digest` rows (P4:33, P4:38, P4:39); `S1:96` confirms the registry has no analysis row.
- F5/F12 (T3 scope): resolved in text. Task 2 states the `document_review_loop_prompts.md` row is `pointer-only`, checked by T3 and never T1 (P4:50); Task 5 leaves the `src/superclaude/examples/...` mention (`src/superclaude/commands/spec-panel.md:220`, plugin twin :218) in place (P4:87); `S1:209` defines T3 so that `pointer-only` rows are exempt from the `src/superclaude` path check.
- F6 (later tasks falsify earlier acceptance lines): the Constraints add the "until Task N" rule (P4:24). I found no acceptance line in this plan that a later task falsifies, so no end point is needed anywhere.


## Deviation and risk observations (new, from splitting the plan)

1. **Task 1 acceptance line 2 cannot be met as written.** It requires the stage 3 summary `./artifacts/stage3-summary-for-owner.md` to "state that one audit window has passed with no revert trigger tripped" (P4:37). The stage 3 plan makes that file say the opposite: it "states that the audit window runs after this package" and "that no revert trigger can be judged until the audit window has run" (S3:158, S3:162). The file is written inside stage 3, before the window, so nobody can satisfy P4:37 unless the owner edits the stage 3 file afterwards, which no package does. The owner's go row in the ledger (P4:36) is the record that exists after the window.
2. **Allow-list location is mis-named in Tasks 1 and 3.** Both say "remove ... from the allow-list of the stage 3 scan test" (P4:33, P4:59) and their acceptance lines say "passes with the two templates removed from its allow-list" (P4:41, P4:63). The scan test reads its allow-list from the "Merge-rule allow-list" section of `refs/scale-map.md` (`S1:59`, OLD:477), so the edit belongs in `scale-map.md`; the test file holds no list. Task 6 names `scale-map.md` correctly (P4:99), Tasks 1 and 3 do not.
3. **Task 3 acceptance line 3 is not literally true for one file.** It says each of the four files "still contains its 'After 2 fix cycles' sentence" (P4:64). `src/superclaude/skills/tdd/refs/build-request-template.md:125` holds the cap only as "Maximum 2 fix cycles - after 2 fix cycles (3 reviews), HALT and escalate ..." with a lowercase "after". A case-sensitive grep for "After 2 fix cycles" finds the other three files (tech-reference :538, readme :464, operational-guide :571) and misses the tdd file. The by-content pin rule (P4:24) lets an executor read it case-insensitively.
4. **Task 5 acceptance line 2 reaches an unlisted line.** `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` must print nothing (P4:89), but the phrase also sits in the FR-8 rule at `src/superclaude/commands/spec-panel.md:332` (and the plugin twin :330), outside the bullets Task 5 lists for editing (lines 259 to 261 and 372, P4:84). The sentence "its `follow-up candidates` list becomes the follow-up ledger" can be read to cover it; the edit list does not name it.
5. **Task 5 parity assertion is under-specified.** "a parity assertion for the two files is part of `tests/skills/test_review_severity_registry.py`" (P4:90): the plan names three files in the edit sentence and says the source and plugin spec-panel copies "differ today" (P4:84), so whole-file parity is impossible; the assertion can only be that the pointer and ledger sentence match. Task 5's acceptance lines do not run the registry test, so the new assertion is first run in Task 6.
6. **Task 1 leaves a PASS bullet next to the rewritten FAIL bullet.** `agent_template_qa.md:157` ("No CRITICAL or IMPORTANT issues") sits directly above the FAIL bullet at :158 that Task 1 rewrites or keeps; the plan names only :158 (P4:33, P4:40).
7. **Task 4's acceptance line is not pinned by content.** "contain the consumer-line instruction" (P4:73) names no sentence to quote, although the Constraints require pins by content (P4:24); the spec gives the form `feeds item X, reads column Y` (merged-requirements.md:249, :273).
8. **Pinning tests are run in one task only.** `tests/skills/test_review_prompt_overrides.py` pins "no minimum count" and the "Independent stance" sentence in `agent_template_qa.md` and the two MDTM templates and "no minimum count" in `tech-reference/SKILL.md` (test file lines 259 to 283). Only Task 2 runs it (P4:55); Tasks 1, 3, 4 and 6 edit those files and do not.
9. **Gate checks run after the edits.** The two owner-gate checks are the first two acceptance lines of Task 1 (P4:36 to 37), which QA reads after the task has edited five templates. `/sc:implement` has a user-authorized Ruling path (`src/superclaude/skills/sc-implement-protocol/refs/ledger.md:62`), so the halt exists, but the edits are already on disk when it fires.
10. **Spec section 10.5 lists `skills/tech-research/SKILL.md` and `skills/roadmap` cap lines under "Builders and researchers"** (merged-requirements.md:867); no task of this plan touches them. The request keeps cap sentences by content (`source.md:12`), so this may be intended.


Persona instructions (refactorer): audit sequencing, ordering and structure. Walk Task 6 step by step (allow-list and registry edit, folder copy, parity test, digest rows, strict T2, make targets, three tests) and say at each step what the registry, the allow-list, the plugin tree and the tests look like and whether any test run inside the task would fail between steps. Check the Depends on lines of Tasks 1 to 7 against the files each task edits (two tasks editing the same file, a task running a test another task's later edit can break), check that the files the plan edits in several tasks (the two MDTM templates, `refs/scale-map.md`, `tests/skills/test_review_severity_registry.py`) end in a consistent state, and check that no task makes an earlier task's acceptance line false. Facts already verified by the orchestrator, for you to confirm cheaply: `plugins/superclaude/skills/` holds the directories confidence-check, sc-implement-protocol, sc-recommend and sc-workflow-protocol plus `__init__.py`; the old definition sentence `Grade every review finding as blocking or minor` is found today in exactly 11 files under `src/superclaude` and none under `plugins/superclaude`; `src/superclaude/skills/sc-review-severity/` does not exist yet (stage 1 creates it).

Severity rule (use exactly this): grade every finding by consequence as blocking or minor. Blocking = a requirement or check that cannot be met, a wrong or missing result, or data loss. Minor = wording or format. A finding that needs a guess about which of two readings an executor picks is minor unless the worse reading is the only one the text allows. A zero-finding result is valid if you state what you checked; never invent a finding to avoid a zero; there is no minimum count. You are read-only: do not edit, write, move or delete anything, run no shell or git command. Audit the supplied hunks and what you can Read, Grep and Glob from the repository root. Use the codegraph tools only when the run-state line says index_state=fresh, passing the projectPath given; codegraph indexes .py and .yaml, not Markdown.

Return your card as one message, at most about 7000 characters, in this shape (no tables): a header `persona:`, `model_class:`, `model:` is added by the orchestrator, so start with `## Verdict` (one sentence), then `## Findings` with one line per finding: `F<n> | MAJOR or MINOR | blocking true or false | category (contradiction, data-loss, missing-requirement, unpassable-check, safety, other) | Who: <the executor or reader affected>. Wrong result: <the concrete wrong outcome>. | citations: <path:line "quote"> (1 to 6 real file:line citations, quotes verbatim, re-Read each before citing)`; then `## Checked` (bullets: what you verified and found fine, with citations), then `## Self-report` with `confidence: <0.00-1.00>` and `reviewer_model_self_report: <the model you are running as, one line>`. Cite repo-relative paths with the line numbers shown in the hunks or re-Read.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T03:10:16Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/TASK-WF-blockerStage4-20261116-030206.md:1-116
```markdown
1: ---
2: schema: workflow-plan/1.2
3: source: ./source.md
4: strategy: systematic
5: depth: standard
6: slug: TASK-WF-blockerStage4-20261116-030206
7: version: "1"
8: priority: Medium
9: created_date: "2026-11-16"
10: ---
11: 
12: # Stage 4 plan: propagate the new rule to the remaining carriers (issue #552)
13: 
14: Source: ./source.md
15: Goal: Move the remaining templates, rule prompts, builder and researcher skills and the spec-panel to the new rule, mirror the skill folder into the plugin, switch the drift scan to strict, and give the owner the final summary.
16: 
17: ## Constraints
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
20: - One package, one stage. This is stage 4 of five packages and the last (one plan per stage). It runs only after the stage 3 package is done, one audit window has passed with no revert trigger tripped (spec section 13.2), the owner has read the stage 3 summary and said go in chat, and the go is recorded in the stage ledger (Task 1 checks that). Strict T2 is switched on here.
21: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
22: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
23: - Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
24: - Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
25: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
26: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
27: - Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.
28: 
29: ## Phase 1: Move the templates
30: 
31: ## Task 1: Move the templates to digest v2
32: 
33: Edit the digest carriers in `src/superclaude/templates/`: `documents/agent_template_qa.md` (the definition bullet near line 161, the merge rule near line 85, the Rule 6 text near line 333 per OD16, and the FAIL-by-label bullet "Any CRITICAL or IMPORTANT issue exists" near line 158, rewritten or kept as a named mechanical gate recorded in `refs/scale-map.md`), `documents/agent_template_analysis.md` (the merge rule near line 466), `documents/skill_template.md` (the definition near line 828), `workflow/01_mdtm_template_generic_task.md` (near line 644) and `workflow/02_mdtm_template_complex_task.md` (near line 655). Each of the four digest templates (`agent_template_qa.md`, `skill_template.md` and the two MDTM templates) gets the digest and pointer in place of the definition bullets and the L1 merge text and its registry row is set to `v2`; `agent_template_analysis.md` gets the L1 merge text only (no digest, no fence, no registry row); remove `agent_template_qa.md` and `agent_template_analysis.md` from the allow-list of the stage 3 scan test. Task files already generated from the old templates keep the old text and are not migrated.
34: 
35: Acceptance criteria:
36: - The stage ledger `stage-requests/README.md` in PF has an owner go for stage 4 with a date (the go is a chat message recorded there by the session that received it); when the row has none, this check fails and the run halts for the owner's Ruling.
37: - The stage 3 package's `./artifacts/stage3-summary-for-owner.md` (read by package id) exists and states that one audit window has passed with no revert trigger tripped.
38: - Each of the four digest template files holds exactly one digest; `agent_template_analysis.md` holds no digest and no `more severe rating` text.
39: - The registry rows of the four digest templates say `v2`, T1 passes for them and the registry still has exactly 11 `digest` rows.
40: - `grep -rn "Grade every review finding as blocking or minor" src/superclaude/templates` prints nothing, and `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/templates/documents/agent_template_qa.md` prints 0 or the remaining line is listed in `refs/scale-map.md`.
41: - `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the two templates removed from its allow-list.
42: 
43: 
44: ## Phase 2: Move the rule prompts, builders, researchers and the consumer line
45: 
46: ## Task 2: Move the rule prompts to digest v2 and set the two pointer-only rows
47: 
48: Depends on: Task 1
49: 
50: Edit the digest carriers in `src/superclaude/rules/prompts/`: `automated_qa_workflow_qa_prompt.md` (near line 11), `doc_code_analyst_qa_prompt.md` (near line 27), `documentation_expert_qa_prompt.md` (near line 28) and `recruiting_expert_qa_prompt.md` (near line 27); update those four registry rows to `v2`. Edit `document_review_loop_prompts.md` (the Medium wording near lines 31, 32 and 48 becomes the pointer and the ledger sentence inside an existing section; its structure and the `"src/superclaude" not in TEXT` assertion of `tests/review/test_review_rules_text.py` must still hold): its registry row is of kind `pointer-only` and stays so; it is checked by T3 and never by T1.
51: 
52: Acceptance criteria:
53: - Each of the four rule prompts holds exactly one digest and its registry row says `v2`.
54: - `document_review_loop_prompts.md` holds the pointer and the ledger sentence and no digest, and its registry row stays `pointer-only`.
55: - `uv run pytest tests/review/test_review_rules_text.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_registry.py -v` passes and the zero-finding and "no minimum count" sentences still exist.
56: 
57: ## Task 3: Replace the merge rule in the builder and researcher skills
58: 
59: Edit the stage 4 merge-rule lines of spec section 10.3: `src/superclaude/skills/tech-reference/SKILL.md` (two lines near 510 and 513), `src/superclaude/skills/readme/SKILL.md` (two lines near 542 and 547), `src/superclaude/skills/tdd/refs/build-request-template.md` (near line 122) and `src/superclaude/skills/operational-guide/SKILL.md` (near line 511), each to the L1 text; and remove those four files from the allow-list of the stage 3 scan test in the same change.
60: 
61: Acceptance criteria:
62: - `grep -rniE "highest severity|more severe rating|higher severity" src/superclaude/skills/tech-reference src/superclaude/skills/readme src/superclaude/skills/tdd src/superclaude/skills/operational-guide` prints nothing.
63: - `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the four skills removed from its allow-list.
64: - The cap text in each of the four files is unchanged (each file still contains its "After 2 fix cycles" sentence).
65: 
66: ## Task 4: Add the consumer line to the task builder and MDTM templates
67: 
68: Depends on: Task 1
69: 
70: Edit `src/superclaude/skills/task-builder/SKILL.md` and the MDTM templates `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md` so the task builder writes a consumer line for each phase output ("feeds item X, reads column Y"), which gives upstream gates a declared consumer list (L4, spec section 4.3 option A for upstream outputs only). Keep the cap sentence in `src/superclaude/skills/task-builder/SKILL.md` ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", one occurrence today) unchanged; `src/superclaude/agents/rf-task-builder.md` holds no such sentence and is not edited.
71: 
72: Acceptance criteria:
73: - Both MDTM templates and the task-builder skill contain the consumer-line instruction.
74: - `uv run pytest tests/skills/test_task_builder_merge.py -v` passes.
75: - The cap sentence is still present in `src/superclaude/skills/task-builder/SKILL.md` (`grep -c` prints 1), and `git diff --stat` shows no edit to `src/superclaude/agents/rf-task-builder.md`.
76: 
77: 
78: ## Phase 3: Narrow spec-panel and update its twins
79: 
80: ## Task 5: Narrow spec-panel and update the plugin twins
81: 
82: Depends on: Task 2
83: 
84: Edit `src/superclaude/commands/spec-panel.md`: the Review Loop bullets (the Grading and Cap bullets near lines 259 to 261) and the always-CRITICAL dimensional-mismatch sentence ("Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL** severity", near line 372) are narrowed to the three conditions (CRITICAL stays blocking, a MAJOR stays blocking only when it names a concrete wrong outcome), its `follow-up candidates` list becomes the follow-up ledger, and the Unattended mode section gains one line for the ledger and the three contract keys. Apply the same edits to the hand-kept twins `plugins/superclaude/commands/spec-panel.md` and `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`; the `spec-panel` source and plugin copies differ today, so edit each file in place and do not copy one over the other. The `commands/sc/spec-panel.md` registry row stays `pointer-only`.
85: 
86: Acceptance criteria:
87: - The existing `src/superclaude/examples/...` mention in `src/superclaude/commands/spec-panel.md` and its twins is left as it is (T3 does not check `pointer-only` rows for that path).
88: - `uv run pytest tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_loop_extension.py -v` passes and the cap sentence `at most 2 fix cycles (3 reviews)` is still in `src/superclaude/commands/spec-panel.md`.
89: - `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` prints nothing and the ledger is named instead.
90: - The plugin twins carry the same pointer and ledger sentence as their source twins, and a parity assertion for the two files is part of `tests/skills/test_review_severity_registry.py`.
91: 
92: 
93: ## Phase 4: Mirror the skill folder into the plugin and write the summary
94: 
95: ## Task 6: Mirror the skill folder into the plugin and make the drift scan strict
96: 
97: Depends on: Task 1, Task 2, Task 3, Task 4, Task 5
98: 
99: Work in this order, because the registry and the allow-list must be correct before the copy. First add the plugin mirror of `refs/rule.md` (`plugins/superclaude/skills/sc-review-severity/refs/rule.md`) as a `canonical` row in `src/superclaude/skills/sc-review-severity/refs/registry.yaml` and as a path in the "Merge-rule allow-list" section of `refs/scale-map.md` (by path only; no merge-rule phrase is written there). Then copy `src/superclaude/skills/sc-review-severity/` to `plugins/superclaude/skills/sc-review-severity/` by hand (the plugin's `skills/` is hand-kept and holds 4 entries today). Then add `tests/skills/test_review_severity_plugin_parity.py` for T15 (the mirror equals the source), set every `digest` row to `v2` where its file now holds the digest (and repeat the copy if the registry changed), and switch T2 of `tests/skills/test_review_severity_registry.py` to strict mode so any legacy definition sentence left in `src/` or `plugins/` fails. Run `make sync-dev` and `make verify-sync`, then the three tests together.
100: 
101: Acceptance criteria:
102: - `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passes with strict T2, and the plugin mirror of `refs/rule.md` is accepted by the reverse scan through its `canonical` row and by the merge-rule scan through the allow-list.
103: - `make verify-sync` passes.
104: - `grep -rn "Grade every review finding as blocking or minor" src/superclaude plugins/superclaude` prints nothing; the five installed-only spec-panel variants are outside the scan and stay listed `installed-only`.
105: - No file under the project `.claude/` folder other than `.claude/settings.json` appears in `git diff --cached --name-only`.
106: 
107: ## Task 7: Write the stage 4 summary for the owner
108: 
109: Depends on: Task 1, Task 2, Task 3, Task 4, Task 5, Task 6
110: 
111: Write `./artifacts/stage4-summary-for-owner.md`: per carrier the digest state and the test that pins it, the final results of the merge-rule scan, the plugin parity test and the strict registry test with their observed pass counts, and the revert command per row (the spec's three-step revert). State that a second audit window is observed by the owner or operator and is not a task of this package, and list the open items.
112: 
113: Acceptance criteria:
114: - `./artifacts/stage4-summary-for-owner.md` lists every carrier row with its state (`v2` or the stated exception) and the test that pins it, and each named test file exists.
115: - The summary shows the observed pass counts of the scan, parity and strict registry tests and the `make verify-sync` result.
116: - The summary states the revert command per row and that the second audit window is not a task of this package.
```

### .dev/tasks/to-do/TASK-WF-blockerStage4-20261116-030206/source.md:1-20
```markdown
1: # Stage 4 plan request: propagate the new rule to the remaining carriers (issue #552)
2: 
3: Last of five plan packages (see `stage-requests/README.md`). Generate it only after the stage 3 package is done, one audit window has passed with no revert trigger tripped (the spec's section 13.2), the owner has read `./artifacts/stage3-summary-for-owner.md`, and the owner's go in chat is recorded in the stage ledger.
4: 
5: ## Base text
6: 
7: Reuse Tasks 41 to 46 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 5, stage 4; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 4 parts). Earlier stages' evidence is read by package id.
8: 
9: ## Changes to apply
10: 
11: - **Templates (the old Task 41).** The digest goes into four templates: `agent_template_qa.md`, `skill_template.md`, `01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md`. `agent_template_analysis.md` gets the merge-rule text only (no digest, no registry row, no fence). The registry keeps exactly 11 `digest` rows. Acceptance: "four template files hold exactly one digest", the analysis template holds none and no `more severe rating` text, and `agent_template_qa.md` holds none of the "Any CRITICAL or IMPORTANT issue exists" FAIL bullet unless it is listed as a kept mechanical gate in `refs/scale-map.md`. Remove `agent_template_qa.md` and `agent_template_analysis.md` from the scan allow-list in the same change.
12: - **Rule prompts, builders and researchers, consumer line (the old Tasks 42 to 44).** As the base text, with the two `pointer-only` rows left at `pointer-only` and the cap sentences kept by content.
13: - **Spec-panel (the old Task 45).** As the base text; the existing `src/superclaude/examples/...` mention in `commands/spec-panel.md` and its twins stays, since T3 does not check `pointer-only` rows for that path.
14: - **Plugin mirror (the old Task 46).** Order the work so the registry and the allow-list are correct BEFORE the copy: first add the plugin mirror of `refs/rule.md` to the `canonical` registry rows and to the allow-list in `refs/scale-map.md` (path only, no merge-rule phrases), then copy the skill folder to `plugins/superclaude/skills/sc-review-severity/`, then run T15 parity, strict T2 and the merge-rule scan. Acceptance includes `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passing, `make verify-sync` passing, and no `.claude/` path other than `.claude/settings.json` staged.
15: - **Constraints.** State this is stage 4 and the last package; strict T2 is switched on here. Acceptance lines that a later task of this package makes false get an end point.
16: - **New final task: stage 4 summary for the owner.** Write `./artifacts/stage4-summary-for-owner.md`: per carrier the digest state and the test that pins it, the final scan and parity results, and the revert command per row (the spec's three-step revert), ending with the sentence that a second audit window is observed by the owner or operator and is not a task of this package.
17: 
18: ## Not to be done by the plan
19: 
20: No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity code under `src/superclaude/cli/**/*.py`, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.
```

### .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md:473-482
```markdown
473: ## Task 40: Add the merge-rule reverse-scan test
474: 
475: Depends on: Task 34, Task 35, Task 36, Task 37
476: 
477: Create `tests/skills/test_review_merge_rule_scan.py` for T5. The scan reads Markdown files only (`*.md`), under `src/superclaude/agents`, `src/superclaude/skills`, `src/superclaude/templates`, `src/superclaude/rules`, `src/superclaude/commands`, `src/superclaude/output-styles` and `plugins/superclaude`, matches `highest severity`, `more severe rating` and `higher severity` case-insensitively, and fails on a hit outside the allow-list. Code files (`src/superclaude/cli/**/*.py`) are not scanned: the spec puts `fmea_classifier.py` and `remediate_parser.py` out of scope. The allow-list is read from the "Merge-rule allow-list" section of `refs/scale-map.md`: `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md`, `src/superclaude/skills/sc-review-severity/refs/rule.md` and its plugin mirror path, and, until Phase 5, the six stage 4 files (`src/superclaude/skills/tech-reference/SKILL.md`, `src/superclaude/skills/readme/SKILL.md`, `src/superclaude/skills/tdd/refs/build-request-template.md`, `src/superclaude/skills/operational-guide/SKILL.md`, `src/superclaude/templates/documents/agent_template_qa.md` and `src/superclaude/templates/documents/agent_template_analysis.md`). Each Phase 5 task that edits one of those files removes it from the allow-list in the same change.
478: 
479: Acceptance criteria:
480: - `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes on the current tree after Tasks 34 to 37, with no hit in `src/superclaude/cli/` counted.
481: - A temporary-tree test with `highest severity` in a Markdown file that is not allow-listed fails the scan, and a temporary-tree test with the phrase in a Python file under `cli/` passes.
482: - The allow-list is read from `refs/scale-map.md` and a test fails when a file named there does not exist.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:59-59
```markdown
59: Create `src/superclaude/skills/sc-review-severity/refs/scale-map.md` with one row per family of spec section 9.3: family, defining file, each native label, the shared outcome per label (Blocking, Medium, Note), and either "graded by the three conditions" or "keeps its own model because <reason>". The rows are the 12 families of that table: the CRITICAL, IMPORTANT, MINOR lens scale; the `/sc:implement` `refs/qa.md` checklist; spec-panel; the stoprule rubric and `finding-grader`; the reflect deviation taxonomy; tasklist High, Medium, Low; roadmap validate; `card_convert.py`; findings-v1 and v2; `sc-auggie-review-protocol/SKILL.md:228`; the PR severity router and Auggie rubric; and the code-assigned family. Include the sentence that a keep of a fixed FAIL trigger (L6) is recorded here, and a section "Merge-rule allow-list" that lists by path only the files allowed to contain the three merge-rule phrases of spec section 10.3 (the auggie file, `refs/rule.md`, and the six stage 4 files until the stage 4 package; this file never writes those phrases or the old definition sentence) so the stage 3 scan test reads its allow-list from one place. The plugin mirror is added to the list by the stage 4 package, not here.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:96-100
```markdown
96: Create `src/superclaude/skills/sc-review-severity/refs/registry.yaml`. Each row has the logical path relative to the install root, a `kind` (`digest`, `canonical`, `pointer-only` or `installed-only`), surfaces (source, installed, project `.claude/`, plugin, or `installed-only`), rollout stage, a state (`legacy` for a digest row until its file is moved), and an own-scale flag. Rows of kind `digest`, exactly the 11 definition carriers of spec section 10.1: `output-styles/pragmatic.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md`, `templates/documents/agent_template_qa.md`, `templates/documents/skill_template.md`, `templates/workflow/01_mdtm_template_generic_task.md`, `templates/workflow/02_mdtm_template_complex_task.md`, `rules/prompts/automated_qa_workflow_qa_prompt.md`, `rules/prompts/doc_code_analyst_qa_prompt.md`, `rules/prompts/documentation_expert_qa_prompt.md`, `rules/prompts/recruiting_expert_qa_prompt.md`. One row of kind `canonical`: `skills/sc-review-severity/refs/rule.md` (the one source digest; the stage 4 package adds its plugin mirror). Two rows of kind `pointer-only` (a pointer plus the ledger sentence, no digest): `rules/prompts/document_review_loop_prompts.md` and `commands/sc/spec-panel.md` (source `commands/spec-panel.md`). Five rows of kind `installed-only`: `commands/sc/spec-panel-armb.md`, `spec-panel-diffgate.md`, `spec-panel-ledger.md`, `spec-panel-ponytail.md` and `spec-panel-stoprule.md`. `skills/task/SKILL.md` gets no row: it is not a digest carrier. `templates/documents/agent_template_analysis.md` gets no row either: it holds no definition sentence, only a merge-rule line, which the stage 4 package edits as text only.
97: 
98: Acceptance criteria:
99: - `refs/registry.yaml` parses with `uv run python -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" src/superclaude/skills/sc-review-severity/refs/registry.yaml`.
100: - It has exactly 11 rows of kind `digest` (each with a source path that exists, state `legacy`, stage 3 for `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md`, stage 4 for the rest), 1 of kind `canonical`, 2 of kind `pointer-only` and 5 of kind `installed-only`, 19 rows in all.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:209-214
```markdown
209: Create `tests/skills/test_review_severity_registry.py` for T1 (every row of kind `digest` holds, in its file, exactly one digest whose flattened body equals the digest section of `refs/rule.md` for that row's version; a row at `legacy` is accepted; the `canonical` row holds the source digest), T2 (a reverse scan of the tracked `src/` and `plugins/` trees fails on any file that holds the old definition sentence or a fence opener and has no registry row of any kind; `canonical` and `pointer-only` rows count as registered; strict mode is a switch, off in this phase), T3 (each pointer names `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, ; the check that no carrier contains `src/superclaude` applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order only, a `pointer-only` row only once its pointer is present, and the test never reads `~/.claude`), T4 (each scale-map row names an existing file and a label present in it) and T14 (a `digest` row at `v2` holds the precedence sentence).
210: 
211: Acceptance criteria:
212: - A temporary-tree test shows each T3 exemption: a `pointer-only` row whose file holds a `src/superclaude` path passes the path check, a `pointer-only` row without its pointer yet passes, and a `digest` row whose file holds such a path fails.
213: - `uv run pytest tests/skills/test_review_severity_registry.py -v` passes with all `digest` rows at `legacy`.
214: - A test flips one `digest` row to `v2` without editing its file and fails, which shows T1 can fail; a `pointer-only` row at any state does not fail T1.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/stage3-request.md:9-15
```markdown
9: ## Changes to apply
10: 
11: - **Constraints.** State this is stage 3 and say what must be true at start (the list above). Stage 4 starts only after one audit window with no revert trigger tripped (the spec's section 13.2 triggers RT1 and RT2) and the owner's go in chat. State that `/sc:implement` runs the whole package in order, so the rule switch cannot start unless the first tasks pass.
12: - **Task 1 (the old Task 31, seeded recall run).** Read the seeded set and answer key from the stage 0 package by id. Each pass (old rule text, new rule text) is run with freshly spawned agents, never agents continued from an earlier pass, and the pass order is alternated across the three reviewers. Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts and the intervals, the cosmetic block share under both, and a pass or fail line for each of the three spec requirements.
13: - **Task for pragmatic.md (the old Task 33).** Its acceptance lines gain: `./artifacts/seeded-recall-result.md` exists and shows pass on all three requirements (safety recall equal to the old rule's, decision-bearing and missing recall within 5 points, cosmetic block share falls); when a line shows fail, the task's check fails and the run halts for the owner's Ruling. Keep the other lines (three bullets replaced, cap and own-scale bullets pinned by content, hook check through `src/superclaude/hooks/hooks.json`). Do not rely on `Depends on:` for this gate.
14: - **Constraints on the scan test (the old Task 40).** `tests/skills/test_review_merge_rule_scan.py` reads the allow-list from `refs/scale-map.md` and allow-lists only files that exist in this stage: the auggie file, `refs/rule.md` and the six stage 4 files. The plugin mirror is NOT in the allow-list here (stage 4 adds it). The existence check applies to every file named in the allow-list and passes in this stage.
15: - **Acceptance lines inside this package** that a later task of the same package makes false get an end point ("until Task N").
```

### .dev/tasks/to-do/TASK-WF-blockerStage3-20261116-030158/TASK-WF-blockerStage3-20261116-030158.md:12-30
```markdown
12: # Stage 3 plan: pilot the new rule for the blocker classification work (issue #552)
13: 
14: Source: ./source.md
15: Goal: Run the seeded-defect recall test under the old and the new rule text, then move `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md` and the task skill's consolidation text to the new rule, re-pin the tests that guard them, and give the owner the audit-window numbers before the stage 4 go.
16: 
17: ## Constraints
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
20: - One package, one stage. This is stage 3 of five packages (one plan per stage). It changes the live review rule. It runs only when all of these hold, each checked by reading files and not by memory (Task 1 checks them): the owner's go for stage 3 is recorded in the stage ledger; the stage 2 package's `./artifacts/stage2-summary-for-owner.md` exists and states at least 5 observed shadow runs with zero safety misses (by the definition the stage 0 spec edit drafted) and no capture failure; the stage 0 package's `stage0b-escape-test.md` and `stage0c-regrade.md` exist. `/sc:implement` runs this whole package in order, so the rule switch cannot start unless Task 1's checks and the seeded-recall result pass. Stage 4 starts only after one audit window with no revert trigger tripped (spec section 13.2) and the owner's go in chat.
21: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
22: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
23: - Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
24: - Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
25: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
26: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
27: - Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.
28: 
29: ## Phase 1: Produce the evidence before the switch
30: 
```

### Makefile:105-125
```makefile
105: 	@echo "✅ Translation complete!"
106: 	@echo "📝 Files updated: README-zh.md, README-ja.md"
107: 
108: # Sync src/superclaude/{skills,agents} → .claude/{skills,agents} for local dev
109: sync-dev:
110: 	@echo "🔄 Syncing src/superclaude/ → .claude/ for local development..."
111: 	@mkdir -p .claude/skills .claude/agents
112: 	@for skill_dir in src/superclaude/skills/*/; do \
113: 		skill_name=$$(basename "$$skill_dir"); \
114: 		case "$$skill_name" in __*) continue;; esac; \
115: 		if [ -f "$$skill_dir/SKILL.md" ] || [ -f "$$skill_dir/skill.md" ]; then \
116: 			mkdir -p ".claude/skills/$$skill_name"; \
117: 			find "$$skill_dir" -type f ! -name '__init__.py' ! -path '*/__pycache__/*' -exec sh -c ' \
118: 				src="$$1"; skill_dir="$$2"; target_base="$$3"; \
119: 				rel=$${src#$$skill_dir}; \
120: 				target_dir="$$target_base/$$(dirname "$$rel")"; \
121: 				mkdir -p "$$target_dir"; \
122: 				cp "$$src" "$$target_dir/" \
123: 			' _ {} "$$skill_dir" ".claude/skills/$$skill_name" \; ; \
124: 		fi; \
125: 	done
```

### Makefile:164-176
```makefile
164: 
165: # Verify src/superclaude/ and .claude/ are in sync (CI-friendly, exits 1 on drift)
166: verify-sync:
167: 	@echo "🔍 Verifying src/superclaude/ ↔ .claude/ sync..."
168: 	@drift=0; \
169: 	echo ""; \
170: 	echo "=== Skills ==="; \
171: 	for skill_dir in src/superclaude/skills/*/; do \
172: 		name=$$(basename "$$skill_dir"); \
173: 		case "$$name" in __*) continue;; esac; \
174: 		if [ ! -d ".claude/skills/$$name" ]; then \
175: 			echo "  ❌ MISSING in .claude/skills/: $$name"; \
176: 			drift=1; \
```

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| INF-010 | Task 6 | mapped | P4:99 order of work |
| INF-011 | Task 6 | mapped | P4:102-105 three tests, verify-sync, staging |
| INF-007 | Task 1 | mapped | P4:33,41 allow-list removal |
| INF-009 | Task 5 | mapped | P4:84,87 examples mention stays |
