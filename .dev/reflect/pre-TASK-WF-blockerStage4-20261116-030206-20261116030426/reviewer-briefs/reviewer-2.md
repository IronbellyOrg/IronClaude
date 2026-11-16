# Reviewer brief 2 (persona: qa; model class: haiku)

## T1 card excerpt

## Coverage and acceptance

The source has no labelled requirement ids (parsed_count 0). Step 1B.0 Pass 2 emitted 16 quote-pinned inferred rows (`artifacts/coverage-matrix.yaml`; each quote is a verbatim substring of its cited `source.md` line, asserted by the script). The deterministic containment rule matched 10 of 16, so `coverage_pct_union` is 0.625 and the parse-density guard fired (inferred 16 greater than parsed 0: `coverage_degraded: parsed-sparse`). The six mechanical misses are all requirements that live in the Constraints block, not in a task:

- INF-002 (reuse base Tasks 41 to 46): the task bodies are the reused text; the plan does not name the base plan id. Covered by the task bodies.
- INF-012 (state stage 4, last package, strict T2 here) is at P4:20; INF-013 (end points for later-falsified acceptance lines) is at P4:24; INF-015 and INF-016 (not-to-be-done list, no Jev call) are at P4:22. Covered.
- INF-008 (two `pointer-only` rows stay; cap sentences kept by content): Task 2 holds the pointer-only statement (P4:50, P4:54); the cap kept is checked in Task 3 (P4:64) and Task 4 (P4:75) but Task 2 has no cap acceptance line even though it edits four prompts and the source says caps are kept for the old Tasks 42 to 44 (`source.md:12`). Partly covered (minor).

Every other source requirement maps to a task: templates and allow-list removal (Task 1, P4:33 to 41), rule prompts (Task 2), builders (Task 3), consumer line (Task 4), spec-panel (Task 5), plugin mirror order and the three-test acceptance (Task 6, P4:99 to 105), the owner summary (Task 7, P4:111 to 116).

## Resolution of the earlier review (`.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md`, findings that touch stage 4)

- F3/F9/F13 (plugin-mirror allow-list ordering): resolved in Task 6. The plugin mirror of `refs/rule.md` is added to the `canonical` registry rows and to the "Merge-rule allow-list" of `refs/scale-map.md` by path only, then the folder is copied, then the three tests run (P4:99). The existence check on every allow-listed file (OLD:477, stage 3 request) would fail between the allow-list edit and the copy, but no test is run between them.
- F4 (analysis template): resolved. `agent_template_analysis.md` gets the merge-rule text only and the registry keeps 11 `digest` rows (P4:33, P4:38, P4:39); `S1:96` confirms the registry has no analysis row.
- F5/F12 (T3 scope): resolved in text. Task 2 states the `document_review_loop_prompts.md` row is `pointer-only`, checked by T3 and never T1 (P4:50); Task 5 leaves the `src/superclaude/examples/...` mention (`src/superclaude/commands/spec-panel.md:220`, plugin twin :218) in place (P4:87); `S1:209` defines T3 so that `pointer-only` rows are exempt from the `src/superclaude` path check.
- F6 (later tasks falsify earlier acceptance lines): the Constraints add the "until Task N" rule (P4:24). I found no acceptance line in this plan that a later task falsifies, so no end point is needed anywhere.


Persona instructions (qa): audit the coverage matrix AGAINST the spec body in your grounding hunks (the spec here is the 20-line stage 4 request, `source.md`); surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding. Then check three things. (1) Does every change the request lists have a task with an acceptance line that tests it, and does any task contradict the request? (2) Compare the plan's Tasks 1 to 6 with the base Tasks 41 to 46 (OLD:486-552) and list every change in wording; judge whether each change is required by the request or the earlier review, or drops something the base text had. (3) For each finding of the earlier review (the report hunk) that touches stage 4 (F3, F4, F5, F6, F9, F12, F13), say whether this plan resolves it, citing the plan line.

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

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:1-35
```markdown
1: # Stage requests for the blocker-classification work (issue #552): one plan per stage
2: 
3: Decision (owner, 2026-11-16): one managed plan package per stage, each generated with `/sc:workflow` and run with `/sc:implement`. `/sc:implement` cannot pause for an owner go, ignores `Depends on:` lines between packages and fails on a plan changed after its first task, so each owner gate sits between two packages and is a chat message from the owner, not a task.
4: 
5: This replaces the single 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (its pre-execution review, `.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md`, found 8 blocking defects). That plan stays on disk as the base text for the task bodies; each stage request below names the base tasks it reuses and the changes the review required.
6: 
7: ## How to use
8: 
9: 1. Generate a stage's package only after the owner's go for it: `/sc:workflow @<request file> --depth standard --handoff none`.
10: 2. Read the plan and its reflect report; run `/sc:implement <printed plan path>` only when execution is wanted.
11: 3. When the package is done, the owner reads its owner summary file and says go for the next stage in chat. Record the go and the package id in the table below (the owner or the session that receives the go writes the row).
12: 
13: ## Stage ledger
14: 
15: | Stage | Request file | Base tasks (revised plan) | Package id | Owner go (date, where) |
16: |---|---|---|---|---|
17: | 0 Measurement | `stage0-request.md` | 1 to 10 | `TASK-WF-blockerStage0-20261116-021044` (generated 2026-11-16; its pre-execution review says NEEDS-REVISION, 2 blocking findings, so revise before running it) | not needed (no change under `src/`) |
18: | 1 Offline scaffold | `stage1-request.md` | 11 to 25 | | |
19: | 2 Shadow | `stage2-request.md` | 26 to 30 | | |
20: | 3 Pilot | `stage3-request.md` | 31 to 40 | | |
21: | 4 Propagation | `stage4-request.md` | 41 to 46 | | |
22: 
23: ## Decisions applied to every stage (from the review findings F1 to F15)
24: 
25: - **Gates (F1, F8).** No gate task. The owner's go is a chat message recorded in the ledger above. Each package ends with an owner summary file under its `./artifacts/` that holds the numbers the owner needs for the next go.
26: - **Cross-package evidence.** A later package reads an earlier package's evidence by package id, found by that folder name under `.dev/tasks/to-do/` or `.dev/tasks/done/` (the package moves when archived). A task never embeds either prefix in an operational link.
27: - **Merge-rule allow-list staging (F3, F9, F13).** The allow-list in `refs/scale-map.md` lists files by path only and never writes the three merge-rule phrases (`highest severity`, `more severe rating`, `higher severity`) or the old definition sentence. Stage 3's scan test allow-lists only files that exist then. Stage 4 adds the plugin mirror to the allow-list and the registry before it copies the folder, then re-runs the scan.
28: - **Analysis template (F4).** `agent_template_analysis.md` gets the merge-rule text only. It is not a digest carrier: the registry keeps exactly 11 `digest` rows, and the template count in stage 4 is four digest templates plus the analysis template's merge-rule edit.
29: - **T3 scope (F5, F12).** The `src/superclaude` path check of T3 applies to `digest` and `canonical` rows only. `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointer-only` row only once its pointer is present. The existing `src/superclaude/examples/...` mention in `commands/spec-panel.md` (and its plugin twin and the installed variants) is left as it is; it is a read-path note outside this work.
30: - **Installed files (F15).** No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path; the M, C and E input rule is stated in words.
31: - **Seeded recall (F2, F10, F11).** Stage 0 defines and sizes the set (with a stated minimum n per gating class, or the set's pass line is called advisory and the interval shown). Stage 3 runs it with fresh agent spawns per pass and alternated order, and Task 33's acceptance line requires the result file to show pass on all three requirements.
32: - **Classifier evaluation (F7).** Stage 2 evaluates the classifier on the fresh-findings set, the held-out half and the reviewer-called-minor set (all from the stage 0 package) and writes the result for the owner.
33: - **Superseded acceptance lines (F6).** Resolved by the split: a package's final review covers only its own tasks. Inside a package, a line that a later task of the same package makes false is written with its end point ("until Task N").
34: - **Unchanged from the revision request.** Three owner gates stay (stage 0 results read before stage 1; stage 1 exit before stage 2; owner go for stages 3 and 4), plus the existing not-built list, the no-authority classifier rule (OD4) and the owner-decision defaults of the first plan.
35: 
```

### .dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md:37-55
```markdown
37: Full text with all citations: `adversarial/merged-review-card.md`. Severity follows the rule in the reviewer brief: blocking means a requirement or check that cannot be met whose fix needs a decision the plan does not make, or a silent wrong or missing result.
38: 
39: | # | Blocking | Finding |
40: |---|---|---|
41: | F1 | yes | The three owner gates (four go points in PLAN:20) cannot be enforced: `/sc:implement` has no phase option, no pause path, ignores a plan edited after the first task, and QA anchors a constraint breach only in a diff. |
42: | F2 | yes | Task 31 only reports the seeded-recall result and Task 33 depends on it finishing, not passing. A stronger `Depends on` line would gate nothing because `/sc:implement` ignores it; only an acceptance line on Task 33 works, and Task 31 cannot move out of Phase 4. |
43: | F3 | yes | Task 40's allow-list names the plugin mirror of `rule.md` and requires every named file to exist, but Task 46 creates the mirror later; Task 13's allow-list text does not list it. |
44: | F4 | yes | Task 41 gives `agent_template_analysis.md` a digest and a `v2` registry row, but the registry has exactly 11 digest rows without it and the file has no definition sentence. |
45: | F5 | yes | Task 25's T3 check fails on `commands/spec-panel.md:220` (and its plugin twin, line 218, and the installed variants). |
46: | F6 | yes | Later tasks make earlier acceptance lines false (Tasks 16, 25, 27, 13), so the final review cannot pass and the package cannot archive. New, from the probe. |
47: | F7 | yes | The fresh-findings set and the held-out split are never evaluated by any task. |
48: | F8 | yes | "Safety miss" is defined nowhere, and the stage 2 and 3 exit numbers have no task that measures them, so the owner has no numbers to read at the gates. New, from the probe. |
49: | F9 | no | Task 46 copies the skill folder before adding the plugin `canonical` registry row (part of the F3 combined fix). |
50: | F10 | no | The seeded-recall pass line has no minimum sample size. |
51: | F11 | no | Task 31 does not alternate pass order or require fresh spawns. |
52: | F12 | no | T3 may fail a `pointer-only` row before its pointer exists. |
53: | F13 | no | Wording-dependent scan trips: `scale-map.md` naming the three phrases, `rule.md` quoting the old sentence. |
54: | F14 | no | Coverage-matrix omissions in the review run. |
55: | F15 | no | Installed reference files cite package-relative `.dev/` paths. |
```

### .dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md:81-135
```markdown
81: ### Recommendation R-001: Make the owner gates and the entry numbers real
82: 
83: - **File:** `.dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md` (Constraints, Tasks 11, 26, 31, 41, and a new measuring task per gate)
84: - **Change:** Choose one mechanism the executor honours: one managed plan per stage (regenerate each with `/sc:workflow`; move the `./artifacts/` inputs into each package), or a gate task at each boundary whose acceptance line accepts only an owner Ruling. Define "safety miss" and the stage 2 and 3 exit numbers (ledger volume, `consumer-unknown` share, offers answered, shadow agreement, revert triggers), and add a task that writes them for the owner before each gate.
85: - **Verifier:** each gated phase's first task has an acceptance line naming the Ruling; `grep -n "safety miss" <plan>` finds a definition; a task per gate writes its summary file.
86: - **Linked deviation(s):** F1, F8
87: - **Priority:** P0
88: 
89: ### Recommendation R-002: Gate Task 33 on the seeded-recall result by an acceptance line
90: 
91: - **File:** the same plan, Task 33 (and Task 31)
92: - **Change:** Add an acceptance line to Task 33 requiring `./artifacts/seeded-recall-result.md` to show pass on all three requirements; keep Task 31 in Phase 4. State a minimum sample size or call the pass line advisory, and require fresh spawns with alternated order.
93: - **Verifier:** Task 33's acceptance lines name the result file; Task 31 names fresh spawns and the alternation.
94: - **Linked deviation(s):** F2, F10, F11
95: - **Priority:** P0
96: 
97: ### Recommendation R-003: Fix the Task 13, 40 and 46 allow-list trio together
98: 
99: - **File:** the same plan, Tasks 12, 13, 40, 46
100: - **Change:** Choose one staging for the plugin-mirror entry (for example Task 40 allow-lists only existing files, and Task 46 adds the mirror to the allow-list and the registry before it copies the folder). Require `scale-map.md` to list files by path without the three phrases, and require `rule.md` not to quote the old definition sentence. Add a re-run of the merge-rule scan to Task 46's acceptance lines.
101: - **Verifier:** `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severity_plugin_parity.py -v` is named in Tasks 40 and 46.
102: - **Linked deviation(s):** F3, F9, F13
103: - **Priority:** P0
104: 
105: ### Recommendation R-004: Settle the registry and T3 contradictions
106: 
107: - **File:** the same plan, Tasks 16, 25, 41, 45
108: - **Change:** Decide that `agent_template_analysis.md` gets the merge-rule text only (then Task 41 covers four template files), or add a twelfth registered carrier. Exempt `pointer-only` and `installed-only` rows from the `src/superclaude` path check, keep the test off `~/.claude`, and check a pointer-only row only once its pointer is present.
109: - **Verifier:** Task 16 and Task 41 counts agree; Task 25's T3 text names the exemptions.
110: - **Linked deviation(s):** F4, F5, F12
111: - **Priority:** P0
112: 
113: ### Recommendation R-005: Scope the acceptance lines that later tasks supersede
114: 
115: - **File:** the same plan, Tasks 13, 16, 25, 27
116: - **Change:** Add "until Task N" (or "at the end of this phase") to each acceptance line that a later task makes false, so the final review does not read it as a standing requirement.
117: - **Verifier:** a re-read of Tasks 13, 16, 25 and 27 shows each superseded line with its end point.
118: - **Linked deviation(s):** F6
119: - **Priority:** P0
120: 
121: ### Recommendation R-006: Give the fresh-findings set and the held-out split a consuming task
122: 
123: - **File:** the same plan (a new Phase 3 task, or reword PLAN:93)
124: - **Change:** Add a stage 2 task that runs the classifier on `./artifacts/fresh-findings.md`, the held-out half and the reviewer-called-minor set with a recorded judge, and writes the result for the owner; or state that the evaluation is deferred past this plan and why.
125: - **Verifier:** `grep -n "fresh-findings" <plan>` finds a task after Phase 1 that consumes the file.
126: - **Linked deviation(s):** F7
127: - **Priority:** P0
128: 
129: ### Recommendation R-007: Tidy the minor notes
130: 
131: - **File:** the same plan (Task 15) and the review run's matrix
132: - **Change:** Reword Task 15 so installed references do not cite package-relative `.dev/` paths; the matrix omissions need no plan change.
133: - **Verifier:** `grep -n "artifacts/classifier-input-availability" src/superclaude/skills/sc-review-severity/refs/classifier-questions.md` prints nothing after Task 15.
134: - **Linked deviation(s):** F14, F15
135: - **Priority:** P2
```

### .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md:17-28
```markdown
17: ## Constraints
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md`, the blocker characteristics in `06-blocker-characteristics.md` and the classifier sketch in `07-classifier/`.
20: - Owner gates. Phase 1 is stage 0 (measurement, no change under `src/`). Phase 2 (stage 1, offline scaffold) starts only after the owner has read the stage 0 results (Task 10 writes them in one file) and said go in chat. Phase 3 (stage 2, shadow) starts only after the stage 1 exit (every Phase 2 acceptance check green) and the owner's say-so. Phase 4 (stage 3, the pilot) starts only after the owner says so; its entry conditions per spec section 12 also need at least 5 observed shadow runs with zero safety misses and no capture failure (the owner or operator runs those shadow runs over time; no task here can produce them), the seeded-recall result of Task 31 and stage 0c (Task 4). Phase 5 (stage 4) starts only after the owner says so after the pilot's audit window. Run `/sc:implement` on one phase at a time and stop at each gate.
21: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
22: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
23: - Classifier facts that bind every classifier task: the 5-run test of PF `08-test/results.md` used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (Task 20 builds the supplier), the "M or C is Y gives BLOCKING" row is never enabled for any gate in this plan, and confidence is reported as an ordinal band, never as a probability.
24: - Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing.
25: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
26: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
27: - Task-owned evidence and generated outputs go under `./artifacts/` in this package.
28: 
```

### .dev/tasks/to-do/TASK-WF-loosenBlockerRev-20261115-210254/TASK-WF-loosenBlockerRev-20261115-210254.md:486-552
```markdown
486: ## Task 41: Move the templates to digest v2
487: 
488: Depends on: Task 40
489: 
490: Edit the digest carriers in `src/superclaude/templates/`: `documents/agent_template_qa.md` (the definition bullet near line 161, the merge rule near line 85, the Rule 6 text near line 333 per OD16, and the FAIL-by-label bullet "Any CRITICAL or IMPORTANT issue exists" near line 158, rewritten or kept as a named mechanical gate recorded in `refs/scale-map.md`), `documents/agent_template_analysis.md` (the merge rule near line 466), `documents/skill_template.md` (the definition near line 828), `workflow/01_mdtm_template_generic_task.md` (near line 644) and `workflow/02_mdtm_template_complex_task.md` (near line 655). Each gets the digest and pointer in place of the definition bullets and the L1 merge text; update their registry rows to `v2`; remove `agent_template_qa.md` and `agent_template_analysis.md` from the allow-list of Task 40. Task files already generated from the old templates keep the old text and are not migrated.
491: 
492: Acceptance criteria:
493: - Each of the five template files holds exactly one digest and no `more severe rating` text.
494: - Their registry rows say `v2` and T1 passes for them.
495: - `grep -rn "Grade every review finding as blocking or minor" src/superclaude/templates` prints nothing, and `grep -c "Any CRITICAL or IMPORTANT issue exists" src/superclaude/templates/documents/agent_template_qa.md` prints 0 or the remaining line is listed in `refs/scale-map.md`.
496: - `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the two templates removed from its allow-list.
497: 
498: ## Task 42: Move the rule prompts to digest v2 and set the two pointer-only rows
499: 
500: Depends on: Task 41
501: 
502: Edit the digest carriers in `src/superclaude/rules/prompts/`: `automated_qa_workflow_qa_prompt.md` (near line 11), `doc_code_analyst_qa_prompt.md` (near line 27), `documentation_expert_qa_prompt.md` (near line 28) and `recruiting_expert_qa_prompt.md` (near line 27); update those four registry rows to `v2`. Edit `document_review_loop_prompts.md` (the Medium wording near lines 31, 32 and 48 becomes the pointer and the ledger sentence inside an existing section; its structure and the `"src/superclaude" not in TEXT` assertion of `tests/review/test_review_rules_text.py` must still hold): its registry row is of kind `pointer-only` and stays so; it is checked by T3 and never by T1.
503: 
504: Acceptance criteria:
505: - Each of the four rule prompts holds exactly one digest and its registry row says `v2`.
506: - `document_review_loop_prompts.md` holds the pointer and the ledger sentence and no digest, and its registry row stays `pointer-only`.
507: - `uv run pytest tests/review/test_review_rules_text.py tests/skills/test_review_prompt_overrides.py tests/skills/test_review_severity_registry.py -v` passes and the zero-finding and "no minimum count" sentences still exist.
508: 
509: ## Task 43: Replace the merge rule in the builder and researcher skills
510: 
511: Depends on: Task 40
512: 
513: Edit the stage 4 merge-rule lines of spec section 10.3: `src/superclaude/skills/tech-reference/SKILL.md` (two lines near 510 and 513), `src/superclaude/skills/readme/SKILL.md` (two lines near 542 and 547), `src/superclaude/skills/tdd/refs/build-request-template.md` (near line 122) and `src/superclaude/skills/operational-guide/SKILL.md` (near line 511), each to the L1 text; and remove those four files from the allow-list of Task 40 in the same change.
514: 
515: Acceptance criteria:
516: - `grep -rniE "highest severity|more severe rating|higher severity" src/superclaude/skills/tech-reference src/superclaude/skills/readme src/superclaude/skills/tdd src/superclaude/skills/operational-guide` prints nothing.
517: - `uv run pytest tests/skills/test_review_merge_rule_scan.py -v` passes with the four skills removed from its allow-list.
518: - The cap text in each of the four files is unchanged (each file still contains its "After 2 fix cycles" sentence).
519: 
520: ## Task 44: Add the consumer line to the task builder and MDTM templates
521: 
522: Depends on: Task 41
523: 
524: Edit `src/superclaude/skills/task-builder/SKILL.md` and the MDTM templates `src/superclaude/templates/workflow/01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md` so the task builder writes a consumer line for each phase output ("feeds item X, reads column Y"), which gives upstream gates a declared consumer list (L4, spec section 4.3 option A for upstream outputs only). Keep the cap sentence in `src/superclaude/skills/task-builder/SKILL.md` ("After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings", one occurrence today) unchanged; `src/superclaude/agents/rf-task-builder.md` holds no such sentence and is not edited.
525: 
526: Acceptance criteria:
527: - Both MDTM templates and the task-builder skill contain the consumer-line instruction.
528: - `uv run pytest tests/skills/test_task_builder_merge.py -v` passes.
529: - The cap sentence is still present in `src/superclaude/skills/task-builder/SKILL.md` (`grep -c` prints 1), and `git diff --stat` shows no edit to `src/superclaude/agents/rf-task-builder.md`.
530: 
531: ## Task 45: Narrow spec-panel and update the plugin twins
532: 
533: Depends on: Task 42
534: 
535: Edit `src/superclaude/commands/spec-panel.md`: the Review Loop bullets (the Grading and Cap bullets near lines 259 to 261) and the always-CRITICAL dimensional-mismatch sentence ("Any dimensional mismatch identified by the Consistency Check is classified as **CRITICAL** severity", near line 372) are narrowed to the three conditions (CRITICAL stays blocking, a MAJOR stays blocking only when it names a concrete wrong outcome), its `follow-up candidates` list becomes the follow-up ledger, and the Unattended mode section gains one line for the ledger and the three contract keys. Apply the same edits to the hand-kept twins `plugins/superclaude/commands/spec-panel.md` and `plugins/superclaude/rules/prompts/document_review_loop_prompts.md`; the `spec-panel` source and plugin copies differ today, so edit each file in place and do not copy one over the other. The `commands/sc/spec-panel.md` registry row stays `pointer-only`.
536: 
537: Acceptance criteria:
538: - `uv run pytest tests/skills/test_spec_panel_review_loop.py tests/skills/test_review_loop_extension.py -v` passes and the cap sentence `at most 2 fix cycles (3 reviews)` is still in `src/superclaude/commands/spec-panel.md`.
539: - `grep -n "follow-up candidates" src/superclaude/commands/spec-panel.md` prints nothing and the ledger is named instead.
540: - The plugin twins carry the same pointer and ledger sentence as their source twins, and a parity assertion for the two files is part of `tests/skills/test_review_severity_registry.py`.
541: 
542: ## Task 46: Mirror the skill folder into the plugin and make the drift scan strict
543: 
544: Depends on: Task 41, Task 42, Task 43, Task 44, Task 45
545: 
546: Copy `src/superclaude/skills/sc-review-severity/` to `plugins/superclaude/skills/sc-review-severity/` by hand (the plugin's `skills/` is hand-kept and holds 4 entries today), add a `canonical` registry row for the plugin mirror of `refs/rule.md`, add `tests/skills/test_review_severity_plugin_parity.py` for T15 (the mirror equals the source), set every `digest` row to `v2` where its file now holds the digest, and switch T2 of `tests/skills/test_review_severity_registry.py` to strict mode so any legacy definition sentence left in `src/` or `plugins/` fails. Run `make sync-dev` and `make verify-sync`.
547: 
548: Acceptance criteria:
549: - `uv run pytest tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passes with strict T2, and the plugin mirror of `refs/rule.md` is accepted by the reverse scan through its `canonical` row.
550: - `make verify-sync` passes.
551: - `grep -rn "Grade every review finding as blocking or minor" src/superclaude plugins/superclaude` prints nothing; the five installed-only spec-panel variants are outside the scan and stay listed `installed-only`.
552: - No file under the project `.claude/` folder other than `.claude/settings.json` appears in `git diff --cached --name-only`.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/stage3-request.md:1-19
```markdown
1: # Stage 3 plan request: pilot the new rule (issue #552)
2: 
3: Fourth of five plan packages (see `stage-requests/README.md`). This package changes the live review rule in `pragmatic.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md` and the task skill. Generate it only when ALL of these hold, each verified by reading the files and not by memory: the owner's go in chat is recorded in the stage ledger; the stage 2 package's `./artifacts/stage2-summary-for-owner.md` exists and the owner has read it; at least 5 shadow runs have been observed with zero safety misses (by the stage 0 definition) and no capture failure; stage 0b's escape result is written and stage 0c's re-grade is written. The seeded-recall result is produced INSIDE this package (first task) and gates the rule switch by an acceptance line, not by a dependency line.
4: 
5: ## Base text
6: 
7: Reuse Tasks 31 to 40 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 4, stage 3; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 3 parts). Earlier stages' evidence is read by package id.
8: 
9: ## Changes to apply
10: 
11: - **Constraints.** State this is stage 3 and say what must be true at start (the list above). Stage 4 starts only after one audit window with no revert trigger tripped (the spec's section 13.2 triggers RT1 and RT2) and the owner's go in chat. State that `/sc:implement` runs the whole package in order, so the rule switch cannot start unless the first tasks pass.
12: - **Task 1 (the old Task 31, seeded recall run).** Read the seeded set and answer key from the stage 0 package by id. Each pass (old rule text, new rule text) is run with freshly spawned agents, never agents continued from an earlier pass, and the pass order is alternated across the three reviewers. Write `./artifacts/seeded-recall-result.md` with per-class recall under both texts and the intervals, the cosmetic block share under both, and a pass or fail line for each of the three spec requirements.
13: - **Task for pragmatic.md (the old Task 33).** Its acceptance lines gain: `./artifacts/seeded-recall-result.md` exists and shows pass on all three requirements (safety recall equal to the old rule's, decision-bearing and missing recall within 5 points, cosmetic block share falls); when a line shows fail, the task's check fails and the run halts for the owner's Ruling. Keep the other lines (three bullets replaced, cap and own-scale bullets pinned by content, hook check through `src/superclaude/hooks/hooks.json`). Do not rely on `Depends on:` for this gate.
14: - **Constraints on the scan test (the old Task 40).** `tests/skills/test_review_merge_rule_scan.py` reads the allow-list from `refs/scale-map.md` and allow-lists only files that exist in this stage: the auggie file, `refs/rule.md` and the six stage 4 files. The plugin mirror is NOT in the allow-list here (stage 4 adds it). The existence check applies to every file named in the allow-list and passes in this stage.
15: - **Acceptance lines inside this package** that a later task of the same package makes false get an end point ("until Task N").
16: - **New final task: stage 3 audit and owner summary (finding F8).** Write `./artifacts/stage3-summary-for-owner.md`: the seeded-recall result headline, the re-pinned test results, and the audit-window measures the spec's section 13 defines (the M-numbers it lists for stage 3 including M12, the rf-qa FAIL count per pilot gate, and the revert triggers RT1 and RT2 with their current state, read from the spec's text and not restated from memory). Say that the audit window runs after this package and is observed by the owner or operator, and end with the sentence that the owner's go for stage 4 is given in chat and not by this file.
17: 
18: ## Not to be done by the plan
19: 
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:859-871
```markdown
859: ### 10.5 Loop and cap text
860: 
861: Those cap-family files that need an edit because they say who counts, merges or escalates:
862: 
863: | Group | Files and lines | Edit |
864: |---|---|---|
865: | Task skill | `skills/task/SKILL.md`: 252 (merge) [V], 254 (fix agent) [V], 258 (halt at the cap) [V], 361 (Follow-Up Items) [V], 372 [E] | L1, L2, L3, ledger |
866: | QA agents | `agents/rf-qa.md` 398, 402 to 415, 549 [E]; `agents/rf-qa-qualitative.md` 110, 809, 994 [E]; `agents/rf-task-builder.md` 383 to 389, 415 to 421 [E] | the cap counts Blocking only; fix-step checks (L2) |
867: | Builders and researchers | `skills/task-builder/SKILL.md` 875 [E]; `skills/tech-research/SKILL.md` 488 to 490, 517 to 519, 555, 562 [E]; `skills/roadmap`, `readme`, `tech-reference`, `operational-guide` cap lines [E] | point at the shared rule; the consumer line (L4) in the task builder |
868: | Tasklist | `skills/sc-tasklist-protocol/SKILL.md` 1439, 1450, 1531, 1567, 1571, 1610, 1614 [V] | only if OD7 says so |
869: | Reflect | `skills/sc-reflect-protocol/SKILL.md` 1540 [V] | only if OD6 says so |
870: | Worker contract | `core/WORKER-CONTRACT.md` 33 (key list), WC-4 status mapping, 39 (coordinator duties) [V] | the three keys of REQ-12 (stage 2) |
871: | Routing doc | `core/HOW-WE-WORK.md` 65 [E] | the level text names the cap; check wording |
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:944-950
```markdown
944: | 0. Measure (this program, offline) | this spec reviewed | 0a: the scored table and five runs with a fixture or approved judge, only if the table exists. 0b: the retrospective escape test on run 2 (section 8.4). 0c: three blind agents that did not write the rule re-grade the table under the old and the new text, paired, only if the table exists. Inventory freeze: every Grep of section 10 re-run, including the frozen FAIL-trigger Grep (REQ-30), with results stored | a written result: escape estimate with its interval; when the table exists, how many old-blocking rows become non-blocking and the confusion matrix | nothing changed |
945: | 1. Offline scaffold | stage 0 result written; owner go | the skill folder with registry rows all `legacy` (T1 and T2 accept the legacy text in registered rows); the ledger reader and writer with the codec; ledger adapters; the fixture judge; property tests; crash, reconcile and consent tests; the install check. No carrier is edited | T1 to T4, T6 to T8, T11 to T13 and T17 green offline | delete the new files |
946: | 2. Shadow beside the old rule | stage 1 exit | the task skill and tech-research gates write the ledger and make the per-run offer (it replaces the output style's "once per loop" ask for that run); reviewers emit `rests_on` while the old definition still decides; the classifier runs in shadow; the safety route GR12 is live; the final-gate sweep GR7 is built; `core/WORKER-CONTRACT.md` gains the three keys (REQ-12) | at least 5 shadow runs observed; ledger volume and `consumer-unknown` share known; offers answered; shadow agreement reported; zero safety misses and no capture failure | stop writing the ledger; restore the old carrier text by the three-step revert (section 9.4) |
947: | 3. Pilot | 0b result written; at least 5 shadow runs observed with zero safety misses and no capture failure (an observation minimum, not a safety claim); seeded recall (section 8.3) met; 0c as well when the table exists; owner go | `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md` move to digest v2 together; the stage 3 merge-rule lines of section 10.3 (task skill, rf-qa, rf-qa-qualitative, rf-analyst; L1); L2 fix-pass checks; L6 for rf-qa, and Rule 6 if OD16 chooses (b), with its test re-pinned in the same change; the cadence pins move | one audit window (section 8.2) with no revert trigger tripped; M12 reported | the three-step revert of the pilot rows to `legacy` |
948: | 4. Propagate | stage 3 exit; owner go | templates, rule prompts, builders and researchers to v2; the stage 4 lines of section 10.3; the spec-panel narrowing; the plugin mirror and parity test; T2 becomes strict (no legacy definition sentence in `src/` or `plugins/`) | drift tests green and strict; a second audit window clear | per-row three-step revert |
949: 
950: Why shadow comes before the pilot: the whole design rests on reviewers being able to name a consumer honestly. Stage 2 measures that while the old definition still decides, so a failure costs nothing.
```

### .dev/reflect/pre-TASK-WF-blockerStage4-20261116-030206-20261116030426/artifacts/coverage-matrix.yaml:1-80
```yaml
1: parsed_ids: []
2: parsed_count: 0
3: inferred_count: 16
4: rows:
5:   - id: INF-001
6:     citation: source.md:3
7:     quote: "Generate it only after the stage 3 package is done, one audit window has passed with no revert trigger tripped (the spec's section 13.2), the owner has read `./artifacts/stage3-summary-for-owner.md`, and the owner's go in chat is recorded in the stage ledger."
8:     containment_match: Task 1
9:     containment_ratio: 0.636
10:   - id: INF-002
11:     citation: source.md:7
12:     quote: "Reuse Tasks 41 to 46 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 5, stage 4; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward, with its `## Constraints` (stage 4 parts)."
13:     containment_match: none
14:     containment_ratio: 0.105
15:   - id: INF-003
16:     citation: source.md:11
17:     quote: "The digest goes into four templates: `agent_template_qa.md`, `skill_template.md`, `01_mdtm_template_generic_task.md` and `02_mdtm_template_complex_task.md`."
18:     containment_match: Task 1
19:     containment_ratio: 0.625
20:   - id: INF-004
21:     citation: source.md:11
22:     quote: "`agent_template_analysis.md` gets the merge-rule text only (no digest, no registry row, no fence)."
23:     containment_match: Task 1
24:     containment_ratio: 0.875
25:   - id: INF-005
26:     citation: source.md:11
27:     quote: "The registry keeps exactly 11 `digest` rows."
28:     containment_match: Task 1
29:     containment_ratio: 0.833
30:   - id: INF-006
31:     citation: source.md:11
32:     quote: "Acceptance: \"four template files hold exactly one digest\", the analysis template holds none and no `more severe rating` text, and `agent_template_qa.md` holds none of the \"Any CRITICAL or IMPORTANT issue exists\" FAIL bullet unless it is listed as a kept mechanical gate in `refs/scale-map.md`."
33:     containment_match: Task 1
34:     containment_ratio: 0.852
35:   - id: INF-007
36:     citation: source.md:11
37:     quote: "Remove `agent_template_qa.md` and `agent_template_analysis.md` from the scan allow-list in the same change."
38:     containment_match: Task 1
39:     containment_ratio: 0.714
40:   - id: INF-008
41:     citation: source.md:12
42:     quote: "As the base text, with the two `pointer-only` rows left at `pointer-only` and the cap sentences kept by content."
43:     containment_match: none
44:     containment_ratio: 0.444
45:   - id: INF-009
46:     citation: source.md:13
47:     quote: "As the base text; the existing `src/superclaude/examples/...` mention in `commands/spec-panel.md` and its twins stays, since T3 does not check `pointer-only` rows for that path."
48:     containment_match: Task 5
49:     containment_ratio: 0.667
50:   - id: INF-010
51:     citation: source.md:14
52:     quote: "Order the work so the registry and the allow-list are correct BEFORE the copy: first add the plugin mirror of `refs/rule.md` to the `canonical` registry rows and to the allow-list in `refs/scale-map.md` (path only, no merge-rule phrases), then copy the skill folder to `plugins/superclaude/skills/sc-review-severity/`, then run T15 parity, strict T2 and the merge-rule scan."
53:     containment_match: Task 6
54:     containment_ratio: 0.815
55:   - id: INF-011
56:     citation: source.md:14
57:     quote: "Acceptance includes `uv run pytest tests/skills/test_review_merge_rule_scan.py tests/skills/test_review_severity_plugin_parity.py tests/skills/test_review_severity_registry.py -v` passing, `make verify-sync` passing, and no `.claude/` path other than `.claude/settings.json` staged."
58:     containment_match: Task 6
59:     containment_ratio: 0.824
60:   - id: INF-012
61:     citation: source.md:15
62:     quote: "State this is stage 4 and the last package; strict T2 is switched on here."
63:     containment_match: none
64:     containment_ratio: 0.375
65:   - id: INF-013
66:     citation: source.md:15
67:     quote: "Acceptance lines that a later task of this package makes false get an end point."
68:     containment_match: none
69:     containment_ratio: 0.3
70:   - id: INF-014
71:     citation: source.md:16
72:     quote: "Write `./artifacts/stage4-summary-for-owner.md`: per carrier the digest state and the test that pins it, the final scan and parity results, and the revert command per row (the spec's three-step revert), ending with the sentence that a second audit window is observed by the owner or operator and is not a task of this package."
73:     containment_match: Task 7
74:     containment_ratio: 0.926
75:   - id: INF-015
76:     citation: source.md:20
77:     quote: "No change to `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the severity code under `src/superclaude/cli/**/*.py`, the cap of 2 fix cycles or the 35 percent target."
78:     containment_match: none
79:     containment_ratio: 0.267
80:   - id: INF-016
```

## Coverage slice

| Requirement | Card ID | Status | Grounding |
|---|---|---|---|
| INF-001 (source.md) | INF-001 | mapped by orchestrator | Task 1 AC1 and AC2 (P4:36-37) |
| INF-002 (source.md) | INF-002 | mapped by orchestrator | task bodies (P4:33-111); no explicit sentence |
| INF-003 (source.md) | INF-003 | mapped by orchestrator | Task 1 (P4:33) |
| INF-004 (source.md) | INF-004 | mapped by orchestrator | Task 1 (P4:33,38) |
| INF-005 (source.md) | INF-005 | mapped by orchestrator | Task 1 AC4 (P4:39) |
| INF-006 (source.md) | INF-006 | mapped by orchestrator | Task 1 AC3 and AC5 (P4:38,40) |
| INF-007 (source.md) | INF-007 | mapped by orchestrator | Task 1 (P4:33) and AC6 (P4:41) |
| INF-008 (source.md) | INF-008 | mapped by orchestrator | Task 2 (P4:50,54); Task 3 AC3 (P4:64); Task 4 AC3 (P4:75) |
| INF-009 (source.md) | INF-009 | mapped by orchestrator | Task 5 AC1 (P4:87) |
| INF-010 (source.md) | INF-010 | mapped by orchestrator | Task 6 (P4:99) |
| INF-011 (source.md) | INF-011 | mapped by orchestrator | Task 6 AC1 to AC4 (P4:102-105) |
| INF-012 (source.md) | INF-012 | mapped by orchestrator | Constraints (P4:20) |
| INF-013 (source.md) | INF-013 | mapped by orchestrator | Constraints (P4:24) |
| INF-014 (source.md) | INF-014 | mapped by orchestrator | Task 7 (P4:111-116) |
| INF-015 (source.md) | INF-015 | mapped by orchestrator | Constraints (P4:22) |
| INF-016 (source.md) | INF-016 | mapped by orchestrator | Constraints (P4:22) |
