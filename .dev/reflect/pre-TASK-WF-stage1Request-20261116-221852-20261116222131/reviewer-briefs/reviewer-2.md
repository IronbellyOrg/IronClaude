# Reviewer 2 brief (persona: qa, model class: haiku)

Task: UC-1 pre-execution audit. Audit the plan .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md against its source .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/source.md (absolute: /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/...). Report deviations and gaps with file:line citations you have Read. You are read-only; do not run commands.

## T1 card excerpt

## QA slice (coverage and acceptance)

- Q1 coverage_pct 0.0 (parsed, artifact), coverage_pct_union 0.2083 (5 of 24), S_dev_density 0.7917, coverage_degraded parsed-sparse (inferred 15 > parsed 9). Unmapped inferred rows: INF-006 (cut list), INF-007 (not-built bullet), INF-008 (stage 2 withdrawn), INF-009 (depth quick), INF-010 (names stages 3 and 4 must match), INF-011 (third existing file), INF-012 (qa.md, cap, 35 percent, Jev), INF-013 (no carrier edit), INF-014 (carry-over of stage constraints), INF-015 (owner summary task, cut).
- Q2 Task acceptance lines are command-based (pytest lists, grep that prints nothing, sha256sum, cmp). Task 2's smoke check (a step-by-step simulation recorded in ./artifacts/print-smoke.txt) is an executor-performed walk-through, not a repeatable script.
- Q3 Task 1 entry check: PF stage ledger stage-requests/README.md stage 1 row now holds an owner go (recorded 2026-11-16 in the previous step of this session); it names the older package id (TASK-WF-blockerStage1-20261116-030154), not this package.


## Grounding hunks

codegraph run state: index_state=fresh checked_at=2026-11-16T22:19:30Z worktree_root=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel projectPath=/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel

### .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/source.md:59-67

```markdown
Applied to the plan in place (plan file name, slug and source path unchanged; the package now has 2 tasks in 2 phases and frontmatter `depth: quick`, down from 16 tasks in 4 phases). Source: `cuts-debate/final-cuts.md` (authoritative where it differs from the revisions above). The Goal, the title, every `Task N` and every `Depends on` line were rewritten.

- **Kept, as Task 1 (was Task 13, rebuilt standalone).** `src/superclaude/cli/review/safety_route.py` (GR1 vocabulary in one list, GR12 raise-only rule), `src/superclaude/cli/review/safety_cmd.py`, the subcommand `superclaude review safety-scan <file>` registered in the tuple of `src/superclaude/cli/review/__init__.py`, and the tests `tests/review/test_review_safety_route.py` and `tests/review/test_review_safety_cmd.py`. It takes plain row text, imports no codec and no classifier, reports unreadable or missing input as such (exit 2, never a hit count), and stores no tag.
- **Kept, as Task 2 (was stage 2 Task 3, shrunk to print-only).** Paragraph "Follow-up print (record and print only)." in `SKILL.md` ("Done") and `refs/managed-workspace.md` (after the closing fence of the `FINAL:` block, before step 6); prints every non-superseded minor line of every task's notes file, runs `superclaude review safety-scan` over each notes file, prints "no notes file for T<id>" for a missing file, asks nothing, changes no verdict or archive outcome; both files copied byte for byte to the plugin twin (pinned by `test_h_implement_protocol_plugin_twins_byte_equal`); `refs/qa.md` unedited (SHA-256 recorded at the task start); active-flow smoke check recorded in `./artifacts/print-smoke.txt`.
- **Cut: Tasks 1 to 12, 14, 15 and 16.** C1 (classifier, its inputs supplier and its command: Tasks 5, 9, 10, 11 and 12), C2 (follow-up ledger codec, filing logic and the ledger reference: Tasks 4, 7 and 8), C4 (skill folder, rule, scale map, registry, install check and registry drift tests: Tasks 1, 2, 3, 6, 14 and 15), C10 (the owner summary: Task 16). C3 shrank the stage 2 carrier to the print. C7 cut the shadow stage and the five-run gate, keeping only the print and its smoke check. One Constraints bullet states that these are not built.
- **Stage 2 is withdrawn into this package.** Its seven other tasks are cut (rows C2 and C7); its ledger row and request file are marked withdrawn by the main session.
- **Depth.** Two tasks fit `depth: quick` (2 to 4 phases, one task per phase). The program gate checker `/tmp/gate_check.py` requires `depth: standard` and 4 to 8 phases; it fails this package for that reason only.
- **Names stages 3 and 4 must match:** command `superclaude review safety-scan <file>` (option `--unattended`); files `src/superclaude/cli/review/safety_route.py`, `src/superclaude/cli/review/safety_cmd.py`, `tests/review/test_review_safety_route.py`, `tests/review/test_review_safety_cmd.py`; paragraph title "Follow-up print (record and print only)."; artifacts `./artifacts/qa-md-sha256-before.txt` and `./artifacts/print-smoke.txt`; no stored tag `protected-risk-dispute`.
- **Added after the reviewer pass (2026-11-16).** The Constraints now name `src/superclaude/cli/review/__init__.py` as the third existing file the package edits (Task 1 registers `safety_cmd`).
```

### .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md:17-30

```markdown
## Constraints

- Spec and cuts: the merged spec `02-brainstorm/merged-requirements.md` and the cuts list `cuts-debate/final-cuts.md` both sit inside the program folder `BLOCKER-CLASSIFICATION-PROGRAM-20261115` (found by that folder name under the repository's task folder). This plan calls that folder PF. The cuts list is authoritative where it differs from the earlier stage requests (revision 4 of the source says so); the rows C1 to C4, C7 and C10 of its section (a) decide what this package builds. Section numbers, requirement ids (REQ-nn) and guardrails (GR1, GR12) refer to the spec.
- One package, two tasks. This is stage 1 of four packages (stages 0, 1, 3 and 4); stage 2 is withdrawn into this package and has no package of its own. The package adds new files only (the scan module, its command module and their tests) and edits exactly three existing files: `src/superclaude/cli/review/__init__.py` (one name added to the tuple of subcommand modules, Task 1) and `SKILL.md` and `refs/managed-workspace.md` of the `sc-implement-protocol` skill (Task 2), plus the two plugin twins of those skill files. It edits no other review-loop carrier. It runs only after the owner has said go for stage 1 in chat and the go is recorded in the stage ledger `stage-requests/README.md` in PF (Task 1 checks that). Stage 3 starts only after this package is done, as its own entry check reads.
- Depth. The source's revision 4 says this package has two tasks in two phases and `depth: quick`; the program gate checker that requires `depth: standard` and 4 to 8 phases fails it for that reason only. The owner chose `quick` in chat on 2026-11-16.
- Not built (cuts rows C1, C2, C3, C4 and C10): the follow-up ledger and its codec, the classifier and its inputs supplier, the carrier registry and scale map, the new skill folder and its references, the install check for digest versions, the registry drift tests, the owner summary file, the sweep and the shadow stage. Nothing here reads, writes or names any of them, and no stored tag for a safety hit exists: the scan only prints.
- Also not built: any Jev or other external judge call, key or account (owner decision OD3 stays open; no finding text leaves the machine); any edit of `src/superclaude/skills/sc-implement-protocol/refs/qa.md` or its plugin twin (it keeps its own scale, and its final summary "never asks the user anything"); any edit of `src/superclaude/cli/review/ledger.py`, `WORKER-CONTRACT.md` or the own-scale primitives; code-assigned severity in `src/superclaude/cli/**/*.py`; any change to the cap of 2 fix cycles.
- Retired carriers stay unedited. `/sc:task` and task-builder are being retired (owner, 2026-11-16): no task edits `src/superclaude/skills/task/`, `src/superclaude/skills/task-builder/` or `src/superclaude/agents/rf-task-builder.md`.
- Plugin surface. IronClaude is installed from the Coder template or from a git clone plus `superclaude install`, not as a plugin, so this package creates no plugin surface. The one existing hand-kept twin it touches is `plugins/superclaude/skills/sc-implement-protocol/`, and only its two files `SKILL.md` and `refs/managed-workspace.md`, because `test_h_implement_protocol_plugin_twins_byte_equal` in `tests/skills/test_review_severity_rule.py` pins them byte for byte to their sources. The owner has not confirmed removing plugin parity (the program's open-questions file, section 3.4); this plan does not decide it.
- Carrier choice. The owner approved the final review step of `/sc:implement` as the follow-up carrier, "record and print only". The once-per-run offer question stays with the top-level session through the output style, so the added paragraph asks the user nothing, makes no offer and adds no stop code.
- Pins are by content. An acceptance check that must survive a task's own edit quotes the sentence it protects; it does not name a line number, because the edit moves the line. Line numbers in a task body are where the text sits today and are re-read before editing. New text added to installed primitives avoids the words the static scans pin (the halt, stop and ruling words of `tests/skills/test_implement_severity_static.py`, the old cap wording and the sweep-phrase patterns of `tests/skills/test_review_severity_rule.py`) and cites no `SKILL.md:<number>` style pointer.
- `src/superclaude/` is the source of truth. Edit there, then run `make sync-dev`; keep everything under the project `.claude/` folder out of `git add` (only `.claude/settings.json` is tracked). Installed primitives name installed paths (`~/.claude/skills/...`) first and project `.claude/...` second, never a `src/superclaude/` path.
- Python work uses UV only: `uv run pytest ...` and `uv run python ...`, never `python -m` or bare `pip`.
- Task-owned evidence and generated outputs go under `./artifacts/` in this package. `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included, and no document a task writes tells a reader to keep `.dev/tasks/` out of `git add`. Staging is not committing.
```

### .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md:34-36

```markdown
## Task 1: Build the safety scan module and the `safety-scan` command

Before creating any file, run the entry check: the stage ledger `stage-requests/README.md` in PF must hold an owner go for stage 1 with a date; when it does not, create nothing and report to the owner. Then create three things.
```

### .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/TASK-WF-stage1Request-20261116-221852.md:56-60

```markdown
## Task 2: Add the print-only follow-up paragraph to the final review step

Depends on: Task 1

Before editing, record the SHA-256 of `src/superclaude/skills/sc-implement-protocol/refs/qa.md` and of its plugin twin `plugins/superclaude/skills/sc-implement-protocol/refs/qa.md` in `./artifacts/qa-md-sha256-before.txt` (two lines; equal today). Then read `src/superclaude/skills/sc-implement-protocol/SKILL.md` (the "Done" section and the "Whole-list review" section), `src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md` (the archive gate, steps 1 to 6) and `refs/qa.md` (the notes-file definition: line 1 holds the `start` sha, lines 2 to m are the live lines, lines after m begin with `superseded `; and the closed list of interrupts), and edit only the first two files.
```

### Makefile:48-51

```make
lint: lint-architecture
	@echo "Running linter..."
	uv run ruff check .

```

### tests/skills/test_implement_severity_static.py:290-298

```python
# --- SPEC AC-11 (V1 F-11, V2 F-15): every halt/STOP/Ruling site classified ---
#
# blocking   reachable only while a blocking finding with a confirmed anchor is open
# stop-row   non-finding STOP row of the SKILL.md STOP table, or FR-019 items 5 and 6
# definition grammar, examples, the reason table, or a rule that writes nothing

_SITE = re.compile(r"\bhalt(s|ed|ing)?\b|E-HALT-QA|E-ARCHIVE-BLOCKED|\bRuling\b")

_ALLOW = [
```

Spec body (D13 recall backstop; whole file, 67 lines): Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

### .dev/tasks/to-do/TASK-WF-stage1Request-20261116-221852/source.md:1-67

```markdown
# Stage 1 plan request: offline scaffold for the blocker classification work (issue #552)

Second of five plan packages (see `stage-requests/README.md` for the one-plan-per-stage decision and the decisions that apply to every stage). Generate it only after the owner has read the stage 0 package's `./artifacts/stage0-summary-for-owner.md` and said go in chat, and after the stage ledger row for stage 0 has the package id. This stage creates new files only (the skill folder, new CLI modules, new tests, one doctor check); it edits no review-loop carrier.

## Base text

Reuse Tasks 11 to 25 of the revised 46-task plan `TASK-WF-loosenBlockerRev-20261115-210254` (Phase 2, stage 1; found by that folder name under `.dev/tasks/to-do/`), renumbered 1 onward. Read its `## Constraints` and carry over what applies to stage 1: spec and PF naming, owner-decision defaults, the not-built list, the classifier facts (M, C and E run only with code-supplied inputs; the "M or C is Y gives BLOCKING" row is never enabled; confidence is an ordinal band), pins by content, `src/superclaude/` as source of truth with `make sync-dev`, UV only. The stage 0 package's evidence (inventory freeze, availability counts, spec reconciliation) is read by package id.

## Changes to apply

- **Constraints.** State this package is stage 1: new files only, no carrier edited, every registry `digest` row stays `legacy`. The next package (stage 2) starts only after the owner's go in chat. Drop the base plan's Phase 3 to 5 gate prose.
- **Task 13 (scale map).** The "Merge-rule allow-list" section lists files by path and never writes the three merge-rule phrases or the old definition sentence. At stage 1 it lists the auggie file, `refs/rule.md` and the six stage 4 files. Say in the task that the plugin mirror is added in stage 4, not here.
- **Task 12 (rule).** `refs/rule.md` holds the GR5 sentence with the phrase `highest severity` (allow-listed) but never quotes the old definition sentence "Grade every review finding as blocking or minor" outside the digest's own fence history; state this as an acceptance line (`grep` of the old sentence over the skill folder prints nothing).
- **Task 15 (classifier questions) and all refs.** No file under `src/superclaude/skills/sc-review-severity/` cites a `.dev/` or `./artifacts/` path (acceptance: `grep -rn "\.dev/\|artifacts/" src/superclaude/skills/sc-review-severity` prints nothing). State the M, C and E input rule in words.
- **Task 16 (registry).** Keep exactly 11 `digest` rows, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows). Say the analysis template is not a carrier row (merge-rule text only in stage 4).
- **Task 25 (registry drift tests).** T3's `src/superclaude` check applies to `digest` and `canonical` rows only; `pointer-only` and `installed-only` rows are checked for pointer order only, and a `pointer-only` row only once its pointer is present; the test never reads `~/.claude`. T2 is non-strict (strict only in stage 4). Acceptance includes a temporary-tree test of each exemption.
- **Acceptance lines inside this package** that a later task of the same package makes false get an end point ("until Task N").
- **New final task: stage 1 exit summary for the owner.** Write `./artifacts/stage1-summary-for-owner.md`: for each task its artifact or file and its observed test result (the commands run and their pass counts), the list of files created, a statement that no carrier was edited (`git diff --stat` over carriers is empty), the open items, and the sentence that the owner's go for stage 2 is given in chat and not by this file. This is the stage 1 exit the spec requires.

## Not to be done by the plan

No edit of any carrier (`pragmatic.md`, agents, templates, rule prompts, task skill, tech-research, WORKER-CONTRACT) and no stage 2 to 4 task. Do not change `sc-implement-protocol/refs/qa.md`, the own-scale primitives, the cap of 2 fix cycles or the 35 percent target. No Jev call, key or account.

## Revision 2 (2026-11-16)

Applied to the plan in place (plan file name, slug and frontmatter unchanged; still 16 tasks, 4 phases). Sources: the pre-execution review `REPORT.md` of the stage 1 plan (findings F1 to F9, recommendations R-001 to R-007) and `revision2-brief.md` (shared decisions 1, 4, 5 and the follow-up carrier decision 2). This section supersedes the older lines above where they differ: the Task 13 line about "the plugin mirror is added in stage 4", and the Task 13 allow-list content.

- **F1, R-001 (blocking, applied).** Task 7: the line "shows only the new module and its command wiring" is replaced. It now reads: until Task 10 adds an importer, `grep -rln "follow_ups" src/superclaude/cli/review` lists only `follow_ups.py`; from Task 10 on the only other files it may list are `classifier_inputs.py`, `classify_cmd.py` and `safety_route.py`. The words "its command wiring" are gone (no task wires a command for `follow_ups`).
- **F2, R-002 option (a) (blocking, applied).** Task 3: the stoprule and `finding-grader` row is marked `installed-only`, names `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` and `~/.claude/agents/finding-grader.md`, cites no `.dev/` path, and is exempt from the exists-in-repository line; Task 15's T4 carries the same exemption (OD10 stays undecided). Checked: neither file exists under `src/` or `plugins/`; both exist installed.
- **F3, R-003 (applied).** Task 3's allow-list section also lists `cli/roadmap/remediate_parser.py` and `cli/pipeline/fmea_classifier.py` as `allowed` (they hold the phrases and are not changed). `stage3-request.md` line 14 repeated the old list and would have contradicted the plan, so it was edited the same way.
- **F4, R-004 and decision 5 (applied).** Task 7 records: `follow-ups.md` stays a separate file, no mapping to `review-ledger/1` rows, `ledger.py` untouched, the audit verdict decides whether a mapping is ever added; the "ledger adapters" are `follow_ups.py`, `classifier_inputs.py` and the classifier column writing of `classify_cmd.py`. Task 16 reports the audit verdict to the owner. `ledger.py` is added to the not-built list.
- **F5, R-005 (applied).** Task 3 fixes the table columns (`family`, `defining file`, `labels`, `model`, `file kind`), the `LABEL=Outcome;` pair format, the path root (relative to `src/superclaude/`, no prefix), the `none` value for a row without a native label (skipped by T4's label check) and `installed-only` rows. Tasks 9, 12 and 15 gain `Depends on: Task 3`.
- **F6, F7, R-006 (applied).** Task 10 depends on Task 7 and Task 9. `run_questions(judge, finding, allowed)` is assigned to Task 9 and `questions_to_ask(inputs)` to Task 10, so Task 11's M, C and E test uses only functions of Tasks 9 and 10. The second half of T12 ("except through the safety route") moves to Task 13, which now depends on Task 9 as well.
- **F8, F9, R-007 (applied).** Task 2's grep uses the full path; Task 12 names the seven review subcommands present today and says `lint` and `estimate` are optional names without modules; Task 4 defines `sweep-flagged` as a ninth state (the spec has eight; it comes from the stage 2 package's sweep) and the installed reference names no rollout stage.
- **Decision 1, retired carriers (applied).** New Constraints bullet; Task 3 lists `skills/task/SKILL.md`, `skills/task-builder/` and `agents/rf-task-builder.md` as `exempt-by-retirement` (path only) with the sentence that the exemption ends when the retirement removes the file; Task 6's note on `skills/task/SKILL.md` (no registry row) was re-read and made consistent; Task 16's carrier diff adds the task-builder folder. Of the 13 files that hold a merge-rule phrase today, only `skills/task/SKILL.md` is a retired carrier.
- **Decision 2, follow-up carrier (applied to stage 1 text).** New Constraints bullet and Task 4 wording: `/sc:implement`'s final review step records and prints only, the offer stays with the top-level session and the consent-bound filing path (OD15), `tech-research` writes the ledger and neither sweeps nor offers; `sc-implement-protocol` joins the not-edited list and the Task 16 diff.
- **Decision 4, no plugin surface (applied).** New Constraints bullet; Task 3 no longer says a plugin mirror comes in stage 4; Task 6's canonical row has no plugin surface (the word `plugin` stays only on the two pointer-only rows whose hand-kept twins exist); Task 15's T2 note says why `plugins/` is still scanned; Task 16 diff adds `plugins`. Registry counts unchanged: 11 `digest`, 1 `canonical`, 2 `pointer-only`, 5 `installed-only` (19 rows).
- **Gate wording (found while running the gate check).** Task 10's body quoted the "acceptance criteria" label with a colon, which broke the one-label-per-task rule; reworded. Two Constraints lines used the phrase the gate rejects for `git add`; reworded to "keep ... out of `git add`".

## Revision 3 (2026-11-16)

Fix cycle 2, applied to the plan in place (file name, slug and frontmatter unchanged; still 16 tasks, 4 phases). Source: the second pre-execution review `REPORT.md` (M-F1 to M-F10, R-001 to R-008). The first review's F1 to F9 are not reopened. Each finding was checked against the live files before the change.

- **M-F1, R-001 (blocking, applied).** Task 7: the line is now `grep -rln --include='*.py' --exclude-dir=__pycache__ "follow_ups" src/superclaude/cli/review` and says "lists no file other than" in both sentences, so compiled `.pyc` files (pytest writes them) and an empty result both pass.
- **M-F2, R-003 (applied).** Task 3 fixes three grammar rules: a lowercase `family` key (12 keys named), a `Conditional` outcome token (spec-panel MAJOR), and ` + ` between several `defining file` paths. Task 9 names the lookup key (the ledger row's `origin`, else the finding's `source`) and gives UNSET for an unknown family, an unlisted label or a `Conditional` label (test in Task 11). Task 15's T4 splits ` + ` cells and checks each label against at least one file, with temporary-tree tests for a two-file row and a conditional label.
- **M-F3, R-004 (applied).** REQ-09 now has an owner: Task 7 adds `earlier_decisions(rows, identity)` with a test. The offer step that calls it belongs to the stage 2 package (cross-stage fact for its plan).
- **M-F4, R-002 (applied, option: supply the inputs).** Task 10 adds the M absence-by-name precheck and the decision-basis excerpts (spec section 4.3, with Option Q at upstream gates); `questions_to_ask` returns S and W always, and M, C, E and D only with their inputs. Tasks 10, 11 and 12 follow (four count lines, D in the recording-judge test).
- **M-F5, R-005 (applied).** Task 12 writes the verdict for every finding to `classifier-results.json` and to the ledger row's `classifier` column only when a row exists; Task 7 adds `update_field(row_id, field, value, expected_revision)`.
- **M-F6, R-006 (applied).** Task 8: the resolver is an injected function like `gh`; the default loads `origin_repo.py` by file path and calls `read_origin()`; the T8 test passes a fake and one test shows the by-path load.
- **M-F7, R-007 (applied).** Task 4 writes the pr-submit exception without the gitignored-folder path and names no `src/superclaude/` file; its acceptance and Task 5's acceptance gain `src/superclaude` greps; Task 6 repeats both folder greps once `registry.yaml` exists.
- **M-F8 (applied).** Task 1 runs its go and stage 0 summary checks before it creates `SKILL.md` (first sentence of the body).
- **M-F9 (applied).** `verify` is now `verify-citations` in Task 12; the stray ", ;" and the T3 wording for `installed-only` rows (not checked by T3) are fixed in Task 15; Task 2's self-cancelling grep line says "prints nothing"; the tasklist Medium line count is 9 on 2026-11-16 (the spec says 7; the live count wins and is re-counted when the task runs).
- **M-F10 (applied).** Task 7's importer list has the end point "until the stage 2 package adds its own importer"; Task 9 keeps its constant off the names `THRESHOLDS` and `CONVERGENCE_THRESHOLDS`, and Tasks 9, 10, 12 and 13 gain a `make lint` acceptance line.
- **Added after the stage 2 fix cycle.** Task 7 gains an acceptance line: a later `write` or `update_field` never clears a ledger's capture state or a row's tags (the stage 2 package tests it).
- **Added after the stage 4 fix cycle.** Task 15 names the strict switch of T2 as the constant `STRICT_T2` (default `False`); the stage 4 package sets it `True`.

## Revision 4 (2026-11-16, cuts debate)

Applied to the plan in place (plan file name, slug and source path unchanged; the package now has 2 tasks in 2 phases and frontmatter `depth: quick`, down from 16 tasks in 4 phases). Source: `cuts-debate/final-cuts.md` (authoritative where it differs from the revisions above). The Goal, the title, every `Task N` and every `Depends on` line were rewritten.

- **Kept, as Task 1 (was Task 13, rebuilt standalone).** `src/superclaude/cli/review/safety_route.py` (GR1 vocabulary in one list, GR12 raise-only rule), `src/superclaude/cli/review/safety_cmd.py`, the subcommand `superclaude review safety-scan <file>` registered in the tuple of `src/superclaude/cli/review/__init__.py`, and the tests `tests/review/test_review_safety_route.py` and `tests/review/test_review_safety_cmd.py`. It takes plain row text, imports no codec and no classifier, reports unreadable or missing input as such (exit 2, never a hit count), and stores no tag.
- **Kept, as Task 2 (was stage 2 Task 3, shrunk to print-only).** Paragraph "Follow-up print (record and print only)." in `SKILL.md` ("Done") and `refs/managed-workspace.md` (after the closing fence of the `FINAL:` block, before step 6); prints every non-superseded minor line of every task's notes file, runs `superclaude review safety-scan` over each notes file, prints "no notes file for T<id>" for a missing file, asks nothing, changes no verdict or archive outcome; both files copied byte for byte to the plugin twin (pinned by `test_h_implement_protocol_plugin_twins_byte_equal`); `refs/qa.md` unedited (SHA-256 recorded at the task start); active-flow smoke check recorded in `./artifacts/print-smoke.txt`.
- **Cut: Tasks 1 to 12, 14, 15 and 16.** C1 (classifier, its inputs supplier and its command: Tasks 5, 9, 10, 11 and 12), C2 (follow-up ledger codec, filing logic and the ledger reference: Tasks 4, 7 and 8), C4 (skill folder, rule, scale map, registry, install check and registry drift tests: Tasks 1, 2, 3, 6, 14 and 15), C10 (the owner summary: Task 16). C3 shrank the stage 2 carrier to the print. C7 cut the shadow stage and the five-run gate, keeping only the print and its smoke check. One Constraints bullet states that these are not built.
- **Stage 2 is withdrawn into this package.** Its seven other tasks are cut (rows C2 and C7); its ledger row and request file are marked withdrawn by the main session.
- **Depth.** Two tasks fit `depth: quick` (2 to 4 phases, one task per phase). The program gate checker `/tmp/gate_check.py` requires `depth: standard` and 4 to 8 phases; it fails this package for that reason only.
- **Names stages 3 and 4 must match:** command `superclaude review safety-scan <file>` (option `--unattended`); files `src/superclaude/cli/review/safety_route.py`, `src/superclaude/cli/review/safety_cmd.py`, `tests/review/test_review_safety_route.py`, `tests/review/test_review_safety_cmd.py`; paragraph title "Follow-up print (record and print only)."; artifacts `./artifacts/qa-md-sha256-before.txt` and `./artifacts/print-smoke.txt`; no stored tag `protected-risk-dispute`.
- **Added after the reviewer pass (2026-11-16).** The Constraints now name `src/superclaude/cli/review/__init__.py` as the third existing file the package edits (Task 1 registers `safety_cmd`).
```

## Coverage slice

| Requirement | Source | Match | Task | Where |
|---|---|---|---|---|
| R-001 | parsed | none |  | line 26 |
| R-007 | parsed | none |  | line 26 |
| R-002 | parsed | none |  | line 29 |
| R-003 | parsed | none |  | line 30 |
| R-004 | parsed | none |  | line 31 |
| R-005 | parsed | none |  | line 32 |
| R-006 | parsed | none |  | line 33 |
| R-008 | parsed | none |  | line 42 |
| REQ-09 | parsed | none |  | line 46 |
| INF-001 | inferred | containment | T1 | line 61 |
| INF-002 | inferred | containment | T1 | line 61 |
| INF-003 | inferred | containment | T2 | line 62 |
| INF-004 | inferred | containment | T2 | line 62 |
| INF-005 | inferred | containment | T2 | line 62 |
| INF-006 | inferred | none |  | line 63 |
| INF-007 | inferred | none |  | line 63 |
| INF-008 | inferred | none |  | line 64 |
| INF-009 | inferred | none |  | line 65 |
| INF-010 | inferred | none |  | line 66 |
| INF-011 | inferred | none |  | line 67 |
| INF-012 | inferred | none |  | line 22 |
| INF-013 | inferred | none |  | line 22 |
| INF-014 | inferred | none |  | line 7 |
| INF-015 | inferred | none |  | line 18 |
