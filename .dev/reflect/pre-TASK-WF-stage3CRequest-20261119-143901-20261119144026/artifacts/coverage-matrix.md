# Coverage matrix (Wave 1B, UC-1): stage 3c request vs plan

- SPEC: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/source.md` (cited as `source.md:N`)
- PLAN: `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-WF-stage3CRequest-20261119-143901/TASK-WF-stage3CRequest-20261119-143901.md` (cited as `plan:N`)
- Rule: `~/.claude/skills/sc-reflect-protocol/refs/coverage-mapping.md`, D13 containment rule (case-folded, fixed stopword set removed, `[a-z0-9]+` tokens, content-word containment >= 0.6 against a single plan unit, ties to the first unit in plan order).
- Plan units, in plan order: Constraints (plan:17-27), Task 1 (plan:31-48), Task 2 (plan:52-61).
- Reproduce: `uv run python /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/reflect/pre-TASK-WF-stage3CRequest-20261119-143901-20261119144026/artifacts/coverage_match.py` (rewrites `coverage-matrix.json` next to it). Every quote is checked as a substring of its cited spec line; 0 rows were dropped.

## Summary

| Field | Value |
|---|---|
| parsed_count (Pass 1, ID_REGEX) | 0 |
| inferred_count (Pass 2) | 43 |
| matched count (containment) | 39 |
| total_count (union) | 43 |
| coverage_pct (parsed-only) | null (parsed_total is 0) |
| coverage_pct_union | 0.9070 |
| unmapped_requirements (parsed) | [] |
| unmapped_requirements_union | INF-001, INF-034, INF-037, INF-038 |
| missing_implementations_count | 0 (no abstract symbol in scope; markdown and a test edit only) |
| S_dev_density | 0.0930 (4 / 43; not above the 0.20 escalation line) |
| coverage_degraded | parsed-sparse (inferred_count 43 > parsed_count 0: the Step 1B.2b parse-density guard fires) |
| coverage_undefined | false (Pass 2 emitted valid rows) |

## Inferred requirements (Pass 2)

Quotes are verbatim; long ones are cut with "..." here and are whole in `coverage-matrix.json`.

| ID | Citation | Quote | Best unit | Ratio | Method |
|---|---|---|---|---|---|
| INF-001 | source.md:3 | Run it on a fresh branch made from `origin/master`. | Constraints | 0.4286 | none |
| INF-002 | source.md:3 | Do NOT run `/sc:implement` on the package until the owner says go in chat. | Constraints | 0.9000 | containment |
| INF-003 | source.md:20 | The stage 3b package ... is in the done subfolder of the repository task folder, and PR #605 is merged. | Constraints | 1.0000 | containment |
| INF-004 | source.md:20 | There is no owner gate inside this package. The owner's go to run it is a separate chat message recorded in the stage ledger ... | Constraints | 0.9000 | containment |
| INF-005 | source.md:24 | Task 1: edit `src/superclaude/agents/reflect-reviewer.md`. Re-read the place by its text first. | Task 1 | 1.0000 | containment |
| INF-006 | source.md:24 | One edit only: in the bullet that begins "- The Severity column ..." insert the passage below directly after ... and before ... "When no consumer can be established". | Task 1 | 0.9697 | containment |
| INF-007 | source.md:24 | Keep one space between sentences. | Task 1 | 1.0000 | containment |
| INF-008 | source.md:24 | Copy the passage from the fenced block below; do not retype it. It is byte-identical to the measured text (source file ..., sha256 `7696a2b2...`, ...). | Constraints | 0.7037 | containment |
| INF-009 | source.md:27 | Before you write `Medium:`, ask whether someone following the text as written could produce behaviour the spec forbids, ... If so, ... grade it `Blocking (Decision):` or `Blocking (Missing):`, not `Medium:`. | Task 1 | 0.6286 | containment |
| INF-010 | source.md:30 | In `tests/skills/test_review_severity_rule.py`, add two needles to the tuple in `test_c_reflect_reviewer_grade_bullets_pinned`: ... Make each needle a Python string that holds the exact text, backticks included. | Task 1 | 0.9333 | containment |
| INF-011 | source.md:32 | Do not change the frontmatter, the Behavioral Mindset, the Boundaries list, ... or the bullet that begins "- This grading applies". | Task 1 | 1.0000 | containment |
| INF-012 | source.md:34 | Before editing, run `git grep -n "reflect-reviewer" -- tests src` and write its output to `./artifacts/stage3c-task1-notes.md`, ... | Task 1 | 1.0000 | containment |
| INF-013 | source.md:34 | After the edit, run every test file that output names once and record each result in the same file. | Task 1 | 1.0000 | containment |
| INF-014 | source.md:39 | `grep -c "Before you write \`Medium:\`" ...` prints 1. | Task 1 | 1.0000 | containment |
| INF-015 | source.md:40 | `grep -c "A behaviour that would happen anyway (for example exit 0 on success) is not that." ...` prints 1. | Task 1 | 1.0000 | containment |
| INF-016 | source.md:41 | `grep -c "a HIGH that is only wording is a Note. Before you write" ...` prints 1. | Task 1 | 1.0000 | containment |
| INF-017 | source.md:42 | `git diff -- ...` shows exactly one changed line, the Severity column bullet. The removed and added versions ... differ only by the inserted passage plus one space. | Task 1 | 0.9600 | containment |
| INF-018 | source.md:43 | `uv run pytest tests/skills/test_review_severity_rule.py -v` passes with the two new needles. | Task 1 | 1.0000 | containment |
| INF-019 | source.md:44 | `uv run pytest` (the four test files) `-v` passes. | Task 1 | 1.0000 | containment |
| INF-020 | source.md:46 | the `git grep` output and its one sentence; | Task 1 | 1.0000 | containment |
| INF-021 | source.md:47 | the results of the other test files that output names; | Task 1 | 1.0000 | containment |
| INF-022 | source.md:48 | one line saying the reflect skill (`skills/sc-reflect-protocol`) and the adversarial merge were not edited. | Task 1 | 1.0000 | containment |
| INF-023 | source.md:50 | Task 2: run `make sync-dev` and `make verify-sync`, then run the four test files above once more after the last edit. | Task 2 | 0.9333 | containment |
| INF-024 | source.md:50 | Write the pass counts and the `make verify-sync` result to `./artifacts/stage3c-final-run.md`. | Task 2 | 1.0000 | containment |
| INF-025 | source.md:50 | Check that nothing under the project `.claude/` folder other than `.claude/settings.json` is staged. | Constraints | 0.7778 | containment |
| INF-026 | source.md:54 | `make verify-sync` passes. | Task 2 | 1.0000 | containment |
| INF-027 | source.md:55 | The four test files pass. | Task 1 | 1.0000 | containment |
| INF-028 | source.md:56 | `./artifacts/stage3c-final-run.md` exists. | Constraints | 0.8333 | containment |
| INF-029 | source.md:60 | That merge step is the reflect protocol's and the adversarial skill's, outside this file. No edit to `skills/sc-reflect-protocol`, the adversarial skill, or the merge text. | Constraints | 0.8667 | containment |
| INF-030 | source.md:61 | That is a detection problem, not a grading one, and is not addressed here. | Constraints | 0.7143 | containment |
| INF-031 | source.md:62 | No edit to the S1 to S3 bullets, `evidence-validator.md`, `sc-implement-protocol/refs/qa.md`, the own-scale primitives or `src/superclaude/cli/**/*.py`. No plugin surface. | Constraints | 1.0000 | containment |
| INF-032 | source.md:62 | No new question in any command. No Jev call. | Constraints | 1.0000 | containment |
| INF-033 | source.md:63 | The re-runs are not a task here. | Constraints | 1.0000 | containment |
| INF-034 | source.md:65 | Known limits to carry into the plan's summary | Constraints | 0.1667 | none |
| INF-035 | source.md:67 | The passage names two kinds of finding from spec E (...) as examples. It was measured with them, so they stay. | Constraints | 0.8000 | containment |
| INF-036 | source.md:67 | Its held-out result on spec B does not depend on them. | Constraints | 0.7500 | containment |
| INF-037 | source.md:68 | The measurement was small: one reviewer model (sonnet), three reviewers per arm, one scorer and no second reader. The briefs carried first-pass coverage hints for every arm. | Task 1 | 0.3500 | none |
| INF-038 | source.md:69 | Whether dropping "plain codepoint order" is a real blocker is a judgment: it changes the order of digits and apostrophes, not of lowercase letters. | Constraints | 0.2857 | none |
| INF-039 | source.md:73 | `src/superclaude/` is the source of truth: edit there, then run `make sync-dev`. | Constraints | 1.0000 | containment |
| INF-040 | source.md:74 | Stage nothing under the project `.claude/` folder; only `.claude/settings.json` is tracked. | Constraints | 0.8889 | containment |
| INF-041 | source.md:75 | Python work uses UV only (`uv run pytest ...`). | Constraints | 1.0000 | containment |
| INF-042 | source.md:76 | `.dev/tasks/` is always staged (`git add .dev/tasks`), packages and their `./artifacts/` included. Staging is not committing. | Constraints | 1.0000 | containment |
| INF-043 | source.md:77 | Acceptance checks are by content and quote the sentence they protect. Line numbers in a task body are hints; re-read each place by its text. | Constraints | 1.0000 | containment |

## Semantic check (beyond the containment numbers)

I read the plan against each row. Rows the plan does not actually carry, or carries wrongly:

| Row | Containment | What the plan really does | Plan evidence |
|---|---|---|---|
| INF-001 (fresh branch from `origin/master`) | none | Not carried. The plan never names a branch or `origin/master`; a case-insensitive search for "branch", "origin/master" and "summary" in the plan finds nothing. | plan:17-27 (Constraints), plan:31-61 (tasks) |
| INF-034 (limits go into the plan's summary) | none | Not carried. The plan has no summary section; only a one-line Goal. | plan:15 |
| INF-036 (spec B result does not depend on the two examples) | containment 0.75 (false positive) | Not carried. The ratio comes from shared words in the "held-out spec B" sentence of plan:21, which says something else. | plan:21-22 |
| INF-037 (measurement was small) | none | Not carried. The plan reports the scores and does not say one model, three reviewers per arm, one scorer, no second reader, coverage hints in the briefs. | plan:21 |
| INF-038 (codepoint order is a judgment) | none | Not carried, and contradicted: plan:21 calls the two spec B findings "two real gaps", while the spec says whether one of them is a real blocker is a judgment. | plan:21 |
| INF-009 (the passage itself) | containment 0.63 | Carried by reference, not quoted: the plan points to "the fenced block of `./source.md`". The package's `source.md` is next to the plan and named in its frontmatter (plan:3), so the executor can reach it. The spec's sha256 and variant path are not carried. | plan:22, plan:34 |
| INF-027, INF-028 (Task 2 acceptance) | matched to Task 1 / Constraints | Containment picked the wrong unit, but the plan does carry both in Task 2's acceptance lines. | plan:60 |
| INF-002 (no `/sc:implement` before the owner's go) | containment 0.90 | Carried in substance: the go is a chat message recorded in the stage ledger. The plan cannot gate its own run, so this falls to the operator. | plan:19 |

Semantic carriage: 38 of 43 rows carried, 5 not carried (INF-001, INF-034, INF-036, INF-037, INF-038). All of them are in the spec's preamble and "Known limits" sections. All change instructions, acceptance checks and exclusions are carried.
