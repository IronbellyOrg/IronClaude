# Reviewer brief 1 (persona: analyzer; model class: sonnet)

## T1 card excerpt

**T1 reflection card (UC-1, pre-execution)**

Spec: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/source.md` (22 lines: the stage 1 plan request; a byte copy of `stage-requests/stage1-request.md` in the program folder)
Plan: `.dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md` (4 phases, 16 tasks, schema workflow-plan/1.2, 226 lines). Cited below as PLAN:<line>.
Author of this card: the reflect orchestrator, a self-review. It did not write the plan; the plan came from a `/sc:workflow` run in another session (executor class unknown). The T2 reviewers exist to break the self-review bias.
Program spec: `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md`, cited as SPEC:<line>. Base plan report: `.dev/reflect/pre-TASK-WF-loosenBlockerRev-20261115-210254-20261115211007/REPORT.md` (8 blocking findings; F3, F4, F5, F6, F9, F12, F13, F15 touch stage 1).

#### Deviation and risk observations

- O1 (acceptance check falsified by a later task, no end point): Task 7's acceptance line says `grep -rn "follow_ups" src/superclaude/cli/review` "shows only the new module and its command wiring" (PLAN:115). Task 10 must "Reuse the reader of Task 7" (PLAN:148), Task 12 writes the ledger row's `classifier` column (PLAN:171) and Task 13 tags ledger rows (PLAN:183), so `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py` all name `follow_ups`. No task creates a command wiring for `follow_ups` itself. The line is false from Task 10 on and carries no "until Task N" (PLAN:24, source.md:17).
- O2 (a defining file the repository does not hold): Task 3 requires 12 family rows "each naming a defining file that exists in the repository" (PLAN:62) and Task 15's T4 re-checks that each row names an existing file and a label in it (PLAN:209). The stoprule family (SPEC:740) is defined by `refs/rubric.md` of the `sc-spec-panel-stoprule-protocol` skill and by the `finding-grader` agent. Neither is under `src/superclaude/` (`ls src/superclaude/skills`, `ls src/superclaude/agents`: no match; SPEC:582 says finding-grader exists only under `~/.claude/agents/`). The only repository copies sit under `.dev/experiments/346-validation/phase5/final-bundle/builds/stoprule/`, and Task 5 forbids any `.dev/` path inside the skill folder (PLAN:87).
- O3 (allow-list content is narrower than the scan it feeds): Task 3's "Merge-rule allow-list" lists the auggie file, `refs/rule.md` and the six stage 4 files (PLAN:59, PLAN:65), and stage3-request.md:14 has the stage 3 scan read exactly that list. SPEC:845 lists `cli/roadmap/remediate_parser.py` as "Not changed", and that file holds `higher severity wins` (remediate_parser.py:55 and :301); `cli/pipeline/fmea_classifier.py:304` and `:323` hold `highest severity`. T5 scans all of `src/` (SPEC:920), so the stage 3 scan fails on those two files unless the section also lists them.
- O4 (acceptance weaker than the request): PLAN:49 allows the old definition sentence "inside the one fenced digest's own text"; source.md:13 asks for a grep that prints nothing over the skill folder. REQ-01's digest (SPEC:195-207) does not contain the old sentence, so the carve-out is vacuous but leaves room to keep it.
- O5 (mirror not re-synced): `make verify-sync` is required to report the new folder in sync at Task 1 (PLAN:40), but Tasks 2 to 6 add files to the folder afterwards; no later task or the exit summary re-runs `make sync-dev` or `make verify-sync` (PLAN:25 says to run sync-dev after editing). `verify-sync` diffs every skill folder (Makefile:166-180).
- O6 (no fixed table shape for a file that code reads): Task 9's `ReviewerJudge` and Task 12's disagreement matrix read the reviewer's label "through the scale map" (PLAN:136, PLAN:171) and Task 15's T4 parses its rows (PLAN:209), but Task 3 fixes only the column meanings in prose (PLAN:59), not the table layout or whether paths are install-relative or `src/`-relative (T3 forbids `src/superclaude` in carriers, PLAN:209).
- O7 (state not in the spec's ledger contract): `sweep-flagged` is an item state in Task 4 (PLAN:78) and Task 7 (PLAN:110), but the spec's item-state table has eight states and not this one (SPEC:379-390); it comes from the stage 2 request. An installed reference would also name stage numbers.
- O8 (spec stage 1 item without a task): SPEC:945 lists "ledger adapters" in stage 1; no task builds or drops them (SPEC:404 leaves the mapping to `review-ledger/1` to the plan; Task 7 only runs the reuse audit, PLAN:110).

Persona instructions (analyzer): look for deviations and internal contradictions between tasks, and for acceptance checks that cannot pass as written (a check that needs a file or state nothing in this package produces, or that a later task of the same package makes false). Walk the `Depends on:` edges, read each repository file a task names, and compare the plan's claims about those files with what is on disk at HEAD. Compare each task with the spec section it cites.

## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T03:11:43Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

Every hunk line is shown as `<real file line>: <text>`. The number before the colon is the line number in the real file, not a line of this brief. Cite those numbers; leave the `N: ` prefix out of any quote.

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:12-27
```markdown
12: # Stage 1 plan: offline scaffold for the blocker classification work (issue #552)
13: 
14: Source: ./source.md
15: Goal: Create the new skill folder, its references, the registry, the ledger and classifier modules, the classify command, the safety route, the install check and their tests, all offline; no review-loop carrier is edited and every registry `digest` row stays `legacy`. The owner reads `./artifacts/stage1-summary-for-owner.md` and decides whether to say go for stage 2.
16: 
17: ## Constraints
18: 
19: - Spec: the merged spec `02-brainstorm/merged-requirements.md` inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF and the spec file the spec. Section numbers, requirement ids (REQ-nn), loop changes (L1 to L6), guardrails (GR1 to GR12), tests (T1 to T17) and owner decisions (OD1 to OD17) refer to the spec. PF also holds the 5-run results in `08-test/results.md`, the reconciliation in `09-plan-input.md` and the stage ledger and the five stage requests in `stage-requests/`. Evidence of earlier stages is read from their packages by package id (the ids are in the stage ledger), found by that folder name in the to-do or done subfolder of the repository task folder.
20: - One package, one stage. This is stage 1 of five packages (one plan per stage, the owner's decision of 2026-11-16). It creates new files only (the skill folder, new CLI modules, new tests, one doctor check) and edits no review-loop carrier (`pragmatic.md`, agents, templates, rule prompts, the task skill, tech-research, `WORKER-CONTRACT.md`); every registry `digest` row stays `legacy`. It runs only after the stage 0 package is done, the owner has read the stage 0 summary and said go in chat, and the go is recorded in the stage ledger (Task 1 checks that). Stage 2 starts only after the owner reads this package's summary and says go.
21: - Owner decisions use the spec's recommendations unless the owner changes them: OD1 skill folder `sc-review-severity`; OD2 once per run plus at any escalation halt; OD4 the classifier has no authority in version 1; OD9 reviewer-named consumer, code-checked where quotable; OD11 replace label-max merging at all 13 lines in 10 files, staged; OD12 yes; OD13 short Note rows; OD14 a finding with an unknown consumer keeps the reviewer's label (no deferral); OD15 consent-bound body file posted by the attended top-level session; OD16 option (b) at stage 3. OD3 (finding text leaving the machine), OD5 to OD8 and OD10 are not decided here and no task depends on a different answer.
22: - Not built here: any Jev or other external judge call, any TypeSafe account or key, a Jev or LLM judge class (they wait for OD3), any change to `src/superclaude/skills/sc-implement-protocol/refs/qa.md` (it keeps its own scale), any change to the own-scale primitives listed in spec section 9.3 as unchanged, code-assigned severity in `src/superclaude/cli/**/*.py` (for example `fmea_classifier.py` and `remediate_parser.py`, out of scope by spec section 10.3), the 35 percent score target, and any change to the cap of 2 fix cycles.
23: - Classifier facts that bind every classifier task: the 5-run test (stage 0 package, `stage0a-result.md`, from PF `08-test/results.md`) used a text-only stand-in judge and got agreement with the panel of 58.5 percent (Cohen's kappa 0.27), and the missing-item, constraint and contradiction questions (M, C, E) were at chance without code-supplied inputs. So M, C and E run only when code supplies the required-item list, the constraint lines and the verified evidence (the classifier-inputs supplier of stage 1), the "M or C is Y gives BLOCKING" row is never enabled for any gate, and confidence is reported as an ordinal band, never as a probability.
24: - Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. An acceptance line that a later task of this package makes false carries its end point ("until Task N").
25: - `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; never stage anything under the project `.claude/` folder (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
26: - Python work uses UV only: `uv run pytest ...`, never `python -m` or bare `pip`.
27: - Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes says it is never staged. Staging is not committing.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:55-66
```markdown
55: ## Task 3: Write the scale map
56: 
57: Depends on: Task 1
58: 
59: Create `src/superclaude/skills/sc-review-severity/refs/scale-map.md` with one row per family of spec section 9.3: family, defining file, each native label, the shared outcome per label (Blocking, Medium, Note), and either "graded by the three conditions" or "keeps its own model because <reason>". The rows are the 12 families of that table: the CRITICAL, IMPORTANT, MINOR lens scale; the `/sc:implement` `refs/qa.md` checklist; spec-panel; the stoprule rubric and `finding-grader`; the reflect deviation taxonomy; tasklist High, Medium, Low; roadmap validate; `card_convert.py`; findings-v1 and v2; `sc-auggie-review-protocol/SKILL.md:228`; the PR severity router and Auggie rubric; and the code-assigned family. Include the sentence that a keep of a fixed FAIL trigger (L6) is recorded here, and a section "Merge-rule allow-list" that lists by path only the files allowed to contain the three merge-rule phrases of spec section 10.3 (the auggie file, `refs/rule.md`, and the six stage 4 files until the stage 4 package; this file never writes those phrases or the old definition sentence) so the stage 3 scan test reads its allow-list from one place. The plugin mirror is added to the list by the stage 4 package, not here.
60: 
61: Acceptance criteria:
62: - `refs/scale-map.md` has a row for each of the 12 families, each naming a defining file that exists in the repository.
63: - The tasklist row states that Medium is blocking today on 7 lines of `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` and that no stage 1 to 4 task changes it.
64: - The `card_convert.py` row states that its word translator maps `important` and `medium` to non-blocking while `src/superclaude/agents/rf-qa.md` treats IMPORTANT as blocking.
65: - The "Merge-rule allow-list" section exists and lists the auggie file, `refs/rule.md` and the six stage 4 files (until the stage 4 package).
66: - `grep -n -i "highest severity\|more severe rating\|higher severity" src/superclaude/skills/sc-review-severity/refs/scale-map.md` prints nothing.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:106-116
```markdown
106: ## Task 7: Build the follow-up ledger codec, reader and writer
107: 
108: Depends on: Task 4
109: 
110: First run the `reuse-auditor` agent on the proposed module against `src/superclaude/cli/review/ledger.py` (schema `review-ledger/1`) and record its verdict in `./artifacts/reuse-audit-follow-ups.md`; share code only where it says reuse-by-import. Then create `src/superclaude/cli/review/follow_ups.py`: one reader and one writer for `follow-ups.md` only (REQ-07 location rule, REQ-08 sole writer with an expected-revision check and atomic replace, REQ-10 entity codec with evidence blocks and a fence longer than any backtick run, identity tuple and observation import that is idempotent, the sort order of spec section 6.2, and the item states including `sweep-flagged`). A malformed ledger is preserved and reported, never reset. Create `tests/review/test_review_follow_ups.py` for T7: required columns, a Medium row without `why_not_blocking` is refused, identity never merges on a digest alone, codec round trip for pipes, backticks, a triple-backtick line, literal entities, Unicode and multiline text, a stale writer cannot overwrite a newer revision, a malformed ledger is preserved.
111: 
112: Acceptance criteria:
113: - `uv run pytest tests/review/test_review_follow_ups.py -v` passes and covers each T7 failure condition above.
114: - `./artifacts/reuse-audit-follow-ups.md` exists and the module imports from `ledger.py` only where the audit says to.
115: - Two readers of this ledger do not exist: `grep -rn "follow_ups" src/superclaude/cli/review` shows only the new module and its command wiring.
116: - `make lint` reports no new findings for the module.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:144-153
```markdown
144: ## Task 10: Build the supplier of the classifier's code-supplied inputs
145: 
146: Depends on: Task 9
147: 
148: Create `src/superclaude/cli/review/classifier_inputs.py` and `tests/review/test_review_classifier_inputs.py`. Given a deliverable file, its declared kind (spec, tasklist, report, code, other) and a finding, the module returns three things. The required-item list: for a spec, its requirement ids and acceptance criteria; for a tasklist, the `Acceptance criteria:` bullets of each task; for a report, the sections its governing template requires; for a kind declared to have no such list, the marker that makes the classifier read M as NA. The constraint lines: quoted constraints and non-goals (a `## Constraints` section, "Will Not" or "Not built" lists). The evidence excerpt: the finding's cited path and line re-read from disk and marked `verified` when the quoted text is present within 2 lines of the cited line and `unverified` otherwise. A missing or unreadable source gives UNSET for that input, never NA and never N. Reuse the reader of Task 7 for ledger rows and the parsers the existing `cli/review` modules already have (Read `src/superclaude/cli/review/findings_v2.py` and `src/superclaude/cli/review/card_convert.py` first and import from them where they cover the job).
149: 
150: Acceptance criteria:
151: - `uv run pytest tests/review/test_review_classifier_inputs.py -v` passes with fixtures for a spec, a tasklist and a report, a kind with no list (NA), an unreadable file (UNSET) and a cited line whose quote is absent (`unverified`).
152: - Each input function returns a value that says whether it was supplied, so a caller can count rows by input.
153: - `grep -n "subprocess\|requests\|httpx" src/superclaude/cli/review/classifier_inputs.py` prints nothing (read-only, no network).
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:167-188
```markdown
167: ## Task 12: Add the `superclaude review classify` command
168: 
169: Depends on: Task 7, Task 9, Task 10
170: 
171: Create `src/superclaude/cli/review/classify_cmd.py` exporting `command` (a click command named `classify`) and add `"classify_cmd"` to the tuple of subcommand module names in `src/superclaude/cli/review/__init__.py`. It reads findings plus a judge answers file, runs the classifier in shadow mode, asks M, C and E only for findings whose inputs `classifier_inputs.py` supplied, writes the verdict, band and judge id with version into the ledger row's `classifier` column beside the reviewer's label, and prints the per-run disagreement matrix read through the scale map (never through the Boolean of `card_convert.py`) and one count line per input (rows with a required-item list, rows with constraint lines, rows with a verified evidence excerpt). The name `classify` must not clash with the existing `panel`, `merge`, `ledger`, `telemetry`, `lint`, `estimate`, `cluster`, `verify` and `manifest` subcommands. Create `tests/review/test_review_classify_cmd.py`.
172: 
173: Acceptance criteria:
174: - `uv run superclaude review classify --help` exits 0 and `uv run superclaude review --help` still lists every earlier subcommand.
175: - `uv run pytest tests/review/test_review_classify_cmd.py tests/review/test_review_cli.py -v` passes.
176: - A run with no judge available records `classifier=unavailable` and leaves the reviewer's label standing; it never invents a verdict.
177: - The printed output includes the three input-count lines, and a test asserts them for a fixture with one supplied and one unsupplied input.
178: 
179: ## Task 13: Build the safety route
180: 
181: Depends on: Task 7
182: 
183: Create `src/superclaude/cli/review/safety_route.py` with the GR1 vocabulary scan (one list of destructive and secret words: delete, overwrite, force, token, secret, password, chmod and similar, kept in one place) and the GR12 rule: a hit on a non-blocking row, or a judge answer S = Y or S = U on a row a reviewer graded non-blocking, tags the row `protected-risk-dispute` and never writes it as a plain follow-up. It can only raise a grade. Add `tests/review/test_review_safety_route.py` for T17.
184: 
185: Acceptance criteria:
186: - `uv run pytest tests/review/test_review_safety_route.py -v` passes and covers a vocabulary hit, S = Y and S = U on a minor row.
187: - No function in the module lowers a grade (a test asserts the outcome order never decreases).
188: - Attended output text names the person prompt; unattended output sets the signal that makes the run `partial`, per spec section 6.4.
```

### .dev/tasks/to-do/TASK-WF-blockerStage1-20261116-030154/TASK-WF-blockerStage1-20261116-030154.md:205-215
```markdown
205: ## Task 15: Add the registry drift tests
206: 
207: Depends on: Task 2, Task 6
208: 
209: Create `tests/skills/test_review_severity_registry.py` for T1 (every row of kind `digest` holds, in its file, exactly one digest whose flattened body equals the digest section of `refs/rule.md` for that row's version; a row at `legacy` is accepted; the `canonical` row holds the source digest), T2 (a reverse scan of the tracked `src/` and `plugins/` trees fails on any file that holds the old definition sentence or a fence opener and has no registry row of any kind; `canonical` and `pointer-only` rows count as registered; strict mode is a switch, off in this phase), T3 (each pointer names `~/.claude/skills/sc-review-severity/...` before `.claude/skills/sc-review-severity/...`, ; the check that no carrier contains `src/superclaude` applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order only, a `pointer-only` row only once its pointer is present, and the test never reads `~/.claude`), T4 (each scale-map row names an existing file and a label present in it) and T14 (a `digest` row at `v2` holds the precedence sentence).
210: 
211: Acceptance criteria:
212: - A temporary-tree test shows each T3 exemption: a `pointer-only` row whose file holds a `src/superclaude` path passes the path check, a `pointer-only` row without its pointer yet passes, and a `digest` row whose file holds such a path fails.
213: - `uv run pytest tests/skills/test_review_severity_registry.py -v` passes with all `digest` rows at `legacy`.
214: - A test flips one `digest` row to `v2` without editing its file and fails, which shows T1 can fail; a `pointer-only` row at any state does not fail T1.
215: - The reverse scan accepts `refs/rule.md` (it has a `canonical` row) and reports a file that holds the definition sentence and is absent from the registry, using a temporary tree in the test.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:735-748
```markdown
735: | Family (where) | Keeps own scale? | Native label to shared outcome | Change, and who decides |
736: |---|---|---|---|
737: | CRITICAL / IMPORTANT / MINOR lens scale (rf-qa, rf-qa-qualitative, task, task-builder, tech-research, templates) | no: it is the shared rule's home | the label is information; the outcome comes from the three conditions | the S5 sentence "CRITICAL and IMPORTANT findings are blocking" (`pragmatic.md:229` and 6 other files, 7 in all [V]) becomes "grade by the three conditions; the label is information"; the fixed FAIL triggers follow L6 (section 10.4); Rule 6 of rf-qa-qualitative is OD16 |
738: | `/sc:implement` `refs/qa.md` four checklist answers (`qa.md:35-52` [V]; identical in `src` and `~/.claude` [V: `cmp`]) | yes (`pragmatic.md:228` [V]) | `ac-outcome-missing`: Missing; `harmful-effect`: Safety; `quoted-constraint-breach`: Decision; `false-claim` blocks any false claim in delivered text or code, which is broader than the rule; minor and note: Note | none in version 1; a "rests on" qualifier on `false-claim` and whether the classifier may fill the four answers are OD8 (recommended: no to both in version 1) |
739: | `/sc:spec-panel` CRITICAL / MAJOR / MINOR (`spec-panel.md:259` [V]) | yes | CRITICAL: Blocking; MAJOR: Blocking only when it names a concrete wrong outcome, else Medium; MINOR: Note | stage 4: narrow "CRITICAL is blocking" and the always-CRITICAL dimensional mismatch (`spec-panel.md:372` [E]) to the three conditions; its `follow-up candidates` list becomes the ledger |
740: | Stoprule rubric B1 to B3, `finding-grader`, and the installed-only spec-panel variants | yes, frozen: "a change is a new version" (`rubric.md:1` [V]) | B1, B2 and B3 together: Blocking; otherwise Note or Medium | registry rows marked `installed-only`; align or retire is OD10 |
741: | reflect deviation taxonomy (Authorized, Necessary, Drift, Regression) | yes | Regression: Blocking (it contradicts an acceptance criterion); Drift: Blocking today, it blocks promotion (`sc-reflect-protocol/SKILL.md:1540` [V]); Necessary and Authorized: Note | none in version 1; a Drift with no decision basis becoming a follow-up is OD6. Not reached by stages 1 to 4, so its over-blocking continues until OD6 |
742: | tasklist High / Medium / Low | yes | High: Blocking; Medium: Blocking today ("High or Medium" or "Medium (blocking)" on 7 lines: 1439, 1450, 1531, 1567, 1571, 1610, 1614 [V]); Low: Note | align Medium to non-blocking, or rename it, after the tasklist rows of the scored table are read (OD7). Not reached by stages 1 to 4 |
743: | roadmap validate BLOCKING / WARNING / INFO (prompt in `cli/roadmap/validate_prompts.py` [E]) | yes | BLOCKING: Blocking; WARNING: Medium; INFO: Note | putting the three conditions into the validator prompt is an adapter change with its own approval; not scheduled in stages 1 to 4 |
744: | `cli/review/card_convert.py` word translator (line 82 [V]) | yes: a translator, not a rule | its word lists decide a Boolean (`important` and `medium` map to non-blocking) | no code change. Document that `rf-qa.md:111` treats IMPORTANT as blocking [V]; shadow comparisons never use this Boolean (section 7.5) |
745: | findings-v1 and v2 Boolean `blocking` | yes | the Boolean is the outcome | none in version 1 |
746: | `sc-auggie-review-protocol/SKILL.md:228` ("keep the higher severity") [V] | yes: a code-review de-duplication on its own scale | its own labels | unchanged in version 1; allow-listed in the merge-rule reverse scan (T5) |
747: | PR severity router (Critical to Nit), Auggie rubric | yes, code-assigned | Low and Nit: Note rows if exported | none; "Medium routes to `--fix`" is a separate decision |
748: | roadmap structural checkers, `cli/roadmap/remediate_parser.py`, audit wiring gate, pipeline detectors, adversarial invariant probe, cli-portify | yes: code-assigned or not a review loop | not mapped | none; listed as out of scope so nobody asks again |
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/02-brainstorm/merged-requirements.md:828-845
```markdown
828: ### 10.3 "Highest severity wins": 13 lines in 10 files
829: 
830: **[REQ-05, location]** Label-max merging is replaced at all of these lines, in two stages [V: LC-04]:
831: 
832: | File | Lines | Stage |
833: |---|---|---|
834: | `skills/task/SKILL.md` | 252, 361 | 3 |
835: | `agents/rf-qa.md` | 83 | 3 |
836: | `agents/rf-qa-qualitative.md` | 84 | 3 |
837: | `agents/rf-analyst.md` | 75 | 3 |
838: | `skills/tech-reference/SKILL.md` | 510, 513 | 4 |
839: | `skills/readme/SKILL.md` | 542, 547 | 4 |
840: | `skills/tdd/refs/build-request-template.md` | 122 | 4 |
841: | `skills/operational-guide/SKILL.md` | 511 | 4 |
842: | `templates/documents/agent_template_qa.md` | 85 | 4 |
843: | `templates/documents/agent_template_analysis.md` | 466 | 4 |
844: 
845: Not changed: `skills/sc-auggie-review-protocol/SKILL.md:228` ("keep the higher severity") is a code-review de-duplication on its own scale, a scale-map row unchanged in version 1. `cli/roadmap/remediate_parser.py` (lines 55, 301, 365) assigns severity in code and is out of scope with the roadmap checkers. `cli/pipeline/fmea_classifier.py` and `pr_submit/severity_router.py` rank unrelated things [V: LC-04]. An earlier draft said the rule also sits in task-builder and tech-research; the Grep does not show that, and the claim is withdrawn. The reverse-scan test T5 searches `src/` and `plugins/` for `highest severity`, `more severe rating` and `higher severity`, with the scale-map rows as its allow-list.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/stage3-request.md:14-14
```markdown
14: - **Constraints on the scan test (the old Task 40).** `tests/skills/test_review_merge_rule_scan.py` reads the allow-list from `refs/scale-map.md` and allow-lists only files that exist in this stage: the auggie file, `refs/rule.md` and the six stage 4 files. The plugin mirror is NOT in the allow-list here (stage 4 adds it). The existence check applies to every file named in the allow-list and passes in this stage.
```

### .dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/stage-requests/README.md:15-21
```markdown
15: | Stage | Request file | Base tasks (revised plan) | Package id | Owner go (date, where) |
16: |---|---|---|---|---|
17: | 0 Measurement | `stage0-request.md` | 1 to 10 | `TASK-WF-blockerStage0-20261116-021044` (generated 2026-11-16; its pre-execution review says NEEDS-REVISION, 2 blocking findings, so revise before running it) | not needed (no change under `src/`) |
18: | 1 Offline scaffold | `stage1-request.md` | 11 to 25 | | |
19: | 2 Shadow | `stage2-request.md` | 26 to 30 | | |
20: | 3 Pilot | `stage3-request.md` | 31 to 40 | | |
21: | 4 Propagation | `stage4-request.md` | 41 to 46 | | |
```

### src/superclaude/cli/roadmap/remediate_parser.py:53-56
```python
53:     Deduplication rule (spec §8/OQ-003):
54:     1. Location match: same file + within 5 lines = candidate duplicate
55:     2. Severity resolution: higher severity wins (BLOCKING > WARNING > INFO)
56:     3. Fix guidance: merged from both reports
```

### src/superclaude/cli/roadmap/remediate_parser.py:299-302
```python
299: 
300:     Step 1: Location match -- same file + within 5 lines = candidate duplicate
301:     Step 2: Severity resolution -- higher severity wins; fix_guidance merged
302:     """
```

### src/superclaude/cli/pipeline/fmea_classifier.py:302-305
```python
302:     """Combine Signal 1 and Signal 2 into unified classification.
303: 
304:     Silent corruption from either signal = highest severity.
305:     """
```

### src/superclaude/cli/pipeline/fmea_classifier.py:321-324
```python
321:         combined_severity = max(s1.severity, s2.severity)
322: 
323:         # Silent corruption = always highest severity (wrong_state minimum)
324:         if combined_difficulty == DetectionDifficulty.SILENT:
```

## Coverage slice

| Requirement | Card ID (task) | Status | Grounding |
|---|---|---|---|
| INF-009: The "Merge-rule allow-list" section lists files by path and never writes the three merge-rule phrases or the old definition sentence. (source.md:12) | Task 3 | covered | PLAN:59, PLAN:66; mechanical rule: containment (task 3, ratio 1.0) |
| INF-010: At stage 1 it lists the auggie file, `refs/rule.md` and the six stage 4 files. (source.md:12) | Task 3 | covered (see O3) | PLAN:59, PLAN:65; mechanical rule: containment (task 3, ratio 1.0) |
| INF-011: Say in the task that the plugin mirror is added in stage 4, not here. (source.md:12) | Task 3 | covered | PLAN:59; mechanical rule: containment (task 3, ratio 0.857) |
| INF-012: `refs/rule.md` holds the GR5 sentence with the phrase `highest severity` (allow-listed) but never quotes the old definition sentence "Grade every r... (source.md:13) | Task 2 | partial (see O4) | PLAN:46, PLAN:49; mechanical rule: containment (task 2, ratio 0.765) |
| INF-013: No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path (acceptance: `grep -rn "\.dev/\/artifacts/" src/s... (source.md:14) | Task 5 | covered | PLAN:87; mechanical rule: containment (task 5, ratio 1.0) |
| INF-017: T3's `src/superclaude` check applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order ... (source.md:16) | Task 15 | covered | PLAN:209; mechanical rule: containment (task 15, ratio 1.0) |
| INF-018: T2 is non-strict (strict only in stage 4). (source.md:16) | Task 15 | covered | PLAN:209; mechanical rule: containment (task 3, ratio 0.6) |
| INF-019: Acceptance includes a temporary-tree test of each exemption. (source.md:16) | Task 15 | covered | PLAN:212; mechanical rule: containment (task 15, ratio 0.857) |
| INF-020: **Acceptance lines inside this package** that a later task of the same package makes false get an end point ("until Task N"). (source.md:17) | Constraints | partial (see O1) | PLAN:24, PLAN:65; mechanical rule: none (task 3, ratio 0.385) |
