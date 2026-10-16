# QA Report: Fix-Cycle Re-Review, Workflow Sequencing and Completeness (IronClaude New User Guide)

**Topic:** `IRONCLAUDE-NEW-USER-GUIDE.md` (rewritten: new section 2 "How to write a request"; workflows renumbered 2.x to 3.x)
**Date:** 2026-10-01
**Phase:** fix-cycle (adversarial; lens = workflow sequencing + completeness; report-only, guide NOT edited)
**Fix cycle:** 1 (re-verifies `13-review-workflows.md` F1-F24)
**Source truth:** `/Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/` (abbreviated `MS/`)
**Guide line numbers** refer to the current rewritten file (240 lines).

---

## Overall Verdict: FAIL

20 of the 24 prior findings are fixed, 1 was handled by removing the step, and 3 are not fully resolved (F5, F20, F22). The re-scan found 7 new issues. The blocking ones: the ruling-line instruction points to a stop message that does not show the format (F5); the new hard limit contradicts the guide's own level-2 example, the small-bug-fix path, and the cleanup step (F20); and the guide says roadmap phase task files carry a spec-coverage result, which source does not guarantee.

## Part 1: Prior findings F1-F24

| # | Status | New text (quoted) | Evidence checked |
|---|---|---|---|
| F1 | RESOLVED | L71-73: "`/roadmap "Create a full roadmap from ... Project name: billing-v2. Dry run first so I can review the phase plan."`" ... "If the summary lists build requests (`build-requests/BUILD_REQUEST-phase-NN-<name>.md`) but no task files, the run chose its middle setting ..." | `MS/skills/roadmap/SKILL.md:104-108` (Standard = BUILD_REQUESTs, no task files; "full roadmap" always Deep); `:247, :2644` (dry run waits for yes) |
| F2 | RESOLVED | Same L71 prompt carries why, constraint, project name | `MS/skills/roadmap/SKILL.md:71, :77` |
| F3 | RESOLVED | L77: "Each task file already contains everything that checks the work ... Do not run those checks again yourself." L79: "read the `reflect_post` entry at the top"; L102 same for 3.2 | `MS/skills/task-builder/SKILL.md:2231-2233` (POST item records `reflect_post`) |
| F4 | RESOLVED | L85: "**If `/task` stops partway:** it shows the reviewers' findings and writes them to the Task Log ... Never tick items by hand to get past a stop." Referenced from 3.2 step 4 (L100) | Prior evidence `MS/skills/task/SKILL.md:120, :180, :254` (not re-opened; text unchanged from prior replacement). See N5 for the 3.4 gap |
| F5 | **NOT RESOLVED** | L113: "add a ruling line to the progress file in the exact format the stop message shows, then resume." | The stop message does NOT show the format. See N1 |
| F6 | RESOLVED | L109-111: plan with `--depth quick`, "Read the plan ... Then: `/sc:implement @.dev/workflow/<name>/plan.md`" (no `--handoff implement`) | `MS/commands/workflow.md:42, :82` |
| F7 | RESOLVED | L97-98: `--spec docs/specs/invoice-csv-export.md` ... "Anything it missed is listed under Open Questions ... the check's result is in the `reflect_pre` entry at the top. Without `--spec` this check is skipped." | `MS/skills/task-builder/SKILL.md:41`; PRE gate fail appends `unmapped_requirements` to Open Questions and `verdict: skipped` only when no spec (`:1666`, sign-off block `:1689-1700`) |
| F8 | RESOLVED (but see N3) | L182-185: 3.10 splits "already checked" from "has not been checked" and gives the report path | `MS/commands/reflect.md:10` (flags) |
| F9 | RESOLVED | L66-68: input is the TDD, output `docs/billing/release-split/`, "Do not split" normal, Release 2 gated | `MS/commands/release-split.md:19, :53` |
| F10 | RESOLVED | L48-52: brainstorm output `merged-requirements.md` path; PRD prompt has purpose, source, code, output | `MS/commands/brainstorm.md:61, :191`; `MS/skills/sc-brainstorm-protocol/SKILL.md:108` |
| F11 | RESOLVED | L57: "It only reports. Decide which findings to accept, ask Claude to apply them to the PRD, then run the same command again until no critical findings remain." | `MS/commands/spec-panel.md:22` |
| F12 | RESOLVED | Section 2 (L24-37) four-part rule plus weak/strong table; concrete prompts in 3.2, 3.3, 3.5, 3.9 | Remaining `<...>` slots are in the levels table and 3.6 row, each backed by a concrete example elsewhere |
| F13 | RESOLVED | L127: "first ask Claude to add a test that reproduces the bug ... confirm the test fails. Then make the fix and run `/sc:test tests/billing/test_invoice_job.py --coverage`" | `MS/commands/test.md:22` |
| F14 | RESOLVED | L121: "A simple bug takes 1-3 minutes ... which can take another 4-15 minutes"; L124: `.dev/troubleshoot/<name>-<timestamp>/REPORT.md` | `MS/commands/troubleshoot.md:51, :57` |
| F15 | HANDLED BY REMOVAL | 3.4 step 4 is now "**Ship.** Workflow 3.11." The manual `/sc:reflect --mode post` was removed, not repaired | **Removal for user adjudication:** the hand-run post-fix audit for small manual bug fixes was dropped. Why acceptable: with no plan or spec it had little to compare against, and 3.11 still runs `/code-review`. The user should confirm this removal |
| F16 | RESOLVED | L157-160: commit first, `--safe --interactive`, "unused imports and code nothing references are removed automatically even then. Review `git diff`" | `MS/commands/cleanup.md:22` usage; auto-fix list (`Unused imports removal`, `Dead code with zero references`) at `:108-112`; `MS/commands/improve.md:22` |
| F17 | RESOLVED | L154-155: `/sc:cleanup-audit src/billing/ --pass all` ... "under `.claude-audit/`" | `MS/commands/cleanup-audit.md:31, :43` |
| F18 | RESOLVED | L203-206: doc-skill, brainstorm `--resume-from .../seed-brief.md`, pr-submit `--resume .../monitor-run-<PR number>.jsonl` rows | `MS/commands/brainstorm.md:63, :192`; `MS/commands/pr-submit.md:40, :55` |
| F19 | RESOLVED | L189 "**Commit locally**"; L192 remediation offer can be declined; L194 "You need the GitHub command-line tool (`gh`) installed and logged in." | `MS/commands/pr-submit.md:29-31`; `MS/commands/auggie-review.md:8` |
| F20 | **NOT RESOLVED (internal contradiction)** | L20: "if the work needs more than 5 edits or touches more than one file, it must go through a written plan" | Contradicts L14, L127, L157-159 of the same guide. See N2 |
| F21 | RESOLVED | L227-230: workflow/implement vs task-builder/task, design vs tdd, tech-reference vs document rows | `MS/commands/design.md:22`; `MS/commands/document.md:22` |
| F22 | PARTIAL (glossary removal accepted per author note) | Defined inline: acceptance criteria (L15), task file (L16), PRD/TDD (L51, L59), spec (L94), `--monitor` setting renamed (L238). Not defined: "phase" is used in two senses; "build request" | See N7 |
| F23 | RESOLVED | L94: spec file path, `/sc:design invoice-export-api --type api --format spec`, "paste its output into the spec file. Have your lead approve the spec." | `MS/commands/design.md:22` |
| F24 | RESOLVED (kept) | L17: "A report at `.dev/tasks/to-do/TASK-RESEARCH-<topic>-<timestamp>/RESEARCH-REPORT-<topic>.md`" | Prior evidence `MS/skills/tech-research/SKILL.md:136` |

## Part 2: Issues (unresolved prior findings plus new re-scan findings)

### N1 (IMPORTANT, prior F5 unresolved): 3.3 step 2, the stop message does not show the ruling format

- **Quoted (L113):** "add a ruling line to the progress file in the exact format the stop message shows, then resume."
- **Evidence:** The halt table says what the stop prints: "HALT `E-HALT-QA`. Print ledger path, Ti, verdict, missing citations. Next: `fix` | `ruling` | `resume`" (`MS/skills/sc-implement-protocol/refs/qa.md:61`). The format string appears only in the protocol references (`refs/qa.md:65-68`, `refs/ledger.md:61-70`). Those references require the long-dash separator, three non-empty fields, and a validation regex at `refs/ledger.md:70` with the long-dash separators. The executor "MUST NOT write the Ruling line" (`refs/qa.md:65`). A newcomer who follows the guide gets the word `ruling` and no format.
- **Replacement (keeps the guide free of the long-dash character):**
  > add a ruling line to the progress file yourself, then resume. Its exact form is in the "Ruling line" section of the `sc-implement-protocol` skill's `refs/ledger.md`: the step id, the word `Ruling:`, then what you decided, why, and the cost if wrong, separated by the long dash shown there (not hyphens). Example from that file: `T2: Ruling: drop pagination`, long dash, `AC-2 deferred to next spec`, long dash, `cost-if-wrong: list stays unpaginated`. The tool will never write this line for you.

### N2 (IMPORTANT, prior F20 unresolved as an internal contradiction): the hard limit contradicts three places in the guide

- **Quoted (L20):** "**Hard limit:** if the work needs more than 5 edits or touches more than one file, it must go through a written plan: level 3 for a few files with clear scope, level 4 for anything larger, longer, or riskier."
- **Contradictions inside the guide:**
  1. L14, the level 2 example (no written plan): "`/sc:task "Rename recieved_at to received_at in src/jobs/runner.py and update its tests"`". That edits `runner.py` and its test file, so it is two files.
  2. L127, 3.4 small fix (no written plan): "add a test that reproduces the bug ... Then make the fix". That is a test file plus a source file.
  3. L157-159, 3.7 step 2 (no written plan): "`/sc:cleanup src/billing/ --type code --safe --interactive`" runs over a whole folder. Auto-fixes apply without asking (`MS/commands/cleanup.md:108-112`), so it can easily make more than 5 edits across many files.
- **Replacement (L20):**
  > **Hard limit:** if the work needs more than 5 edits or touches more than one source file (a matching test file does not count), it must go through a written plan: level 3 for a few files with clear scope, level 4 for anything larger, longer, or riskier. `/sc:cleanup` and `/sc:improve` on a whole folder are the one exception: commit first and review `git diff` (3.7).
- **Alternative:** keep L20 as written, and change L14, L127, and L157-159 to route through level 3. The author or user must choose one of these. Leaving both as they are is the defect.

### N3 (IMPORTANT, new): 3.1 step 7 and 3.10 say roadmap task files already have a spec-coverage result, but source does not guarantee it

- **Quoted (L72):** "It has already checked every phase task file against the PRD and TDD."
- **Quoted (L182):** "**Task files from `/task-builder --spec` or from `/roadmap`** have already been checked against the spec. Read the `reflect_pre` entry at the top of the task file and resolve anything it lists before running `/task`."
- **Quoted (L73):** "Create each phase's task file with `/task-builder <path to that build request>`."
- **Evidence:**
  - task-builder resolves the spec in this order: `--spec`, then an `@file` in GOAL, then "a `SPEC:`/`PRD:`/`TDD:` field in a BUILD_REQUEST file", then none (`MS/skills/task-builder/SKILL.md:41, :285`). With none, `reflect_pre` is `verdict: skipped`, `skip_reason: no-spec` (`:1666`).
  - The roadmap BUILD_REQUEST template has no top-level `SPEC:`/`PRD:`/`TDD:` field. It lists the PRD and TDD only as bullets under `## CONTEXT FILES` ("- PRD (if present): [path] §...", `MS/skills/roadmap/SKILL.md:609-613`). The roadmap skill never passes `--spec` (no `--spec` match in `MS/skills/roadmap/SKILL.md`).
  - Whether those bullets resolve as a spec is **Unverified**. A newcomer may well find `reflect_pre: verdict: skipped`, and the guide gives no instruction for that case.
  - The roadmap's own end-to-end check (Stage 4, "Input → Roadmap → BUILD_REQUEST → Task File", `:34, :662`) runs only at Deep tier. Its results go to `${TASK_DIR}qa/qa-task-roadmap-alignment.md` (`:156`), not to `reflect_pre`.
  - For the middle-setting fallback (L73), the user runs `/task-builder` without `--spec`, so the PRE check is skipped for certain.
- **Replacement (L72 sentence):**
  > At its full setting it also checks the phase task files against the roadmap and your PRD and TDD; that check's reports are in the roadmap folder's `qa/` subfolder.
- **Replacement (L73):**
  > ... Create each phase's task file with `/task-builder <path to that build request> --spec docs/billing/TDD_BILLING.md`. ...
- **Replacement (L182):**
  > **Task files from `/task-builder --spec`** have already been checked against the spec. Read the `reflect_pre` entry at the top of the task file and resolve anything it lists before running `/task`. If `reflect_pre` says `skipped` (reason `no-spec`), which can happen with task files made by `/roadmap`, the check did not run: use the command below with your PRD or TDD as `--spec` and the task file as `--tasklist`.

### N4 (MINOR, new): the level 4 row makes `--spec` look mandatory, and the research hand-off would misuse it

- **Quoted (L16):** "`/task-builder "<what to build, why, which code>" --spec <path to your spec>`"
- **Quoted (L17):** "Then give the report it writes to `/task-builder` (level 4)."
- **Problem:** `--spec` is optional and is meant for a "driving spec/PRD/TDD" (`MS/skills/task-builder/SKILL.md:41`). A newcomer coming from level 5 will copy the level-4 shape and pass the research report as `--spec`. The section 2 example (L36) correctly leaves `--spec` out for a research report, but it never says why. The earlier review's caveat ("Use `--spec <path>` only when you have a real spec, PRD, or TDD") was dropped.
- **Replacement (L16):**
  > `/task-builder "<what to build, why, which code>"`, adding `--spec <path>` when you have a spec, PRD, or TDD (not a research report), researches the code ...

### N5 (MINOR, new): 3.4, `--fix` must be chosen before the diagnosis, there is no branch for an inconclusive diagnosis, and the `/task` stop note is not linked

- **Quoted (L122):** "If the fix may span several files, add `--fix` now."
- **Quoted (L128):** "accept the task-file offer from step 1 (if you did not pass `--fix`, run the diagnosis again with it), then `/task <path>`."
- **Problems:**
  1. The user cannot know the fix's size before the diagnosis. Rerunning the whole diagnosis (up to about 15 minutes) just to get the offer is wasteful.
  2. The offer is made "only when `--fix` is set AND REPORT.md status is `success`" (`MS/commands/troubleshoot.md:170`). When the diagnosis is inconclusive there is no offer, and the guide has no step for that case.
  3. Unlike 3.2 step 4 (L100), this `/task` run has no pointer to the "If `/task` stops partway" note (L85).
- **Replacement (L128):**
  > **Fix across several files:** accept the task-file offer from step 1. If you did not pass `--fix`, build the task file directly: `/task-builder "Fix the root cause described in .dev/troubleshoot/<name>-<timestamp>/REPORT.md, with a test that reproduces the bug" --spec .dev/troubleshoot/<name>-<timestamp>/REPORT.md`. Then `/task <path>`; if it stops partway, see the note at the end of 3.1. Read its `reflect_post` verdict when it finishes.
  > - **If the report says the cause is not confirmed,** do not fix yet. Run the checks the report lists, then run `/sc:troubleshoot` again with what you learned, or rerun it with `--depth deep`.
- **Note:** passing REPORT.md as `--spec` is a recommendation, not a documented chain. The documented `--fix` path builds the task file itself (`MS/commands/troubleshoot.md:54, :192`).

### N6 (MINOR, new): 3.3 has no ship step, and its `/code-review` repeats 3.11 step 2

- **Quoted (L115):** "**Before committing:** run `/code-review` (it looks for bugs, which the step-by-step reviewer does not). Run the tests yourself only if nothing ran them ..."
- **Problem:** 3.2 (L102) and 3.4 (L130) both end with "workflow 3.11"; 3.3 does not. A newcomer finishing a small change never reaches the commit, push-approval, and PR steps. Anyone who does go on to 3.11 runs `/code-review` twice (3.11 step 2, L190).
- **Replacement (L115):**
  > 3. **Ship.** Run the tests yourself only if nothing ran them (a plain edit, or a trivial `/sc:task` change). Then follow workflow 3.11. Its `/code-review` step looks for bugs, which the step-by-step reviewer does not.

### N7 (MINOR, prior F22 partial): "phase" means two things, and "build request" is never defined

- **Quoted (L16):** "After every working phase, a panel of independent reviewer agents checks the work."
- **Quoted (L75-77):** "**Build one phase at a time.** `/task <path to the phase 1 task file>` ... reviewer panels after each phase"
- **Quoted (L73):** "If the summary lists build requests ... Create each phase's task file with `/task-builder <path to that build request>`."
- **Problem:** In 3.1, "phase" means a roadmap phase (one task file each) and also a group of items inside a task file (one reviewer panel each). The same sentence uses both senses. "Working phase" is never explained. "Build request" is introduced without saying what it is. The author chose inline definitions over a glossary, so each term must be defined where it first appears.
- **Replacement (L16):** "... After each group of related items (the task file calls it a phase), a panel of independent reviewer agents checks the work."
- **Replacement (L77):** "... reviewer panels after each group of items inside the task file, the tests, and ..."
- **Replacement (L73), add:** "(a build request is the short input file `/task-builder` turns into a task file)"

### N8 (MINOR, new): the section 5 advice to narrow `/roadmap` conflicts with 3.1 step 7

- **Quoted (L239):** "| `/tech-research` and `/roadmap` | Run at their deepest setting, with many agents, unless the request is clearly small. | Ask a narrow, specific question. |"
- **Quoted (L73):** "Saying "full roadmap" or "comprehensive" in the request avoids this."
- **Problem:** For `/roadmap`, the deepest setting is the only one that creates phase task files (`MS/skills/roadmap/SKILL.md:104-108`). Section 5 tells users to narrow the request, which pushes `/roadmap` to the middle or quick setting, and 3.1 then has to repair that.
- **Replacement (L239):**
  > | `/tech-research` and `/roadmap` | Run at their deepest setting, with many agents, unless the request is clearly small. | For `/tech-research`, ask a narrow, specific question. For `/roadmap`, keep the full setting if you want task files for every phase (3.1 step 7). |

### N9 (MINOR, new): the progress-file path placeholder points to the wrong folder name

- **Quoted (L15):** "a progress file at `.dev/implement/<name>/progress.md`"
- **Problem:** For a file source, the folder name is the file's base name plus a hash of its absolute path, not the workflow name (`MS/skills/sc-implement-protocol/SKILL.md:52`: "`<slug>` = `{prefix}-{hash8}` where `prefix` is the basename without extension ... `hash8` is SHA-256 of the **absolute** path"). Every `/sc:workflow` plan is named `plan.md`, so the folder is `.dev/implement/plan-<8 characters>/`. A newcomer who looks for `.dev/implement/invoice-csv-export/` finds nothing. Elsewhere the same placeholder `<name>` means the workflow folder (L15 plan path, L110), which makes the mistake more likely.
- **Replacement (L15):** "... and a progress file under `.dev/implement/plan-<code>/progress.md` (the tool prints the exact path). If interrupted, add `--resume` to continue."

### N10 (MINOR, new): 3.1 step 9 says "fix them" without saying how

- **Quoted (L79):** "If it lists unresolved problems, fix them before the next phase."
- **Problem:** This repeats the pattern prior F11 fixed for spec-panel. The audit's unresolved items are either already in the task file's Open Questions or remediations it could not apply (`MS/skills/task-builder/SKILL.md:2231`: "If reflect surfaced deviations, the remediations were applied or the deviations were logged to `### Open Questions`"). A failed audit also leaves the folder in `.dev/tasks/to-do/`, which the step does not mention. The newcomer is not told who decides, how to apply the fix, or how to confirm it.
- **Replacement (L79), after the first sentence:**
  > If the verdict is not a pass, the task folder stays in `.dev/tasks/to-do/` and the unresolved items are listed under the task file's Open Questions. Decide each one with your lead, the same way as a `/task` stop (note at the end of 3.1): fix the code, correct the spec, or accept it in writing. Then run `/sc:reflect --mode post --tasklist <path to the task file> --spec docs/billing/TDD_BILLING.md --diff <first commit of this phase>..HEAD` to confirm before starting the next phase.

## Re-scan coverage (what was checked with no defect found)

| Area | Result | Evidence |
|---|---|---|
| Cross-references | All 15 references resolve (workflows 3.1-3.12, "3.1 step 9", "3.4 step 3", "section 1", "level 2/3/4"); no stale "2.x" workflow references remain | Bash grep over the guide, references at L17, 18, 20, 81, 83, 102, 106, 130, 145, 162, 167 |
| Long dashes and en dashes | 0 and 0 | Python count over the guide |
| Command flags | All cited flags exist in source usage: auggie-review `--diff <base>...HEAD`, `--no-post-pr`; test `--type unit|integration|e2e`; document `--type api`; analyze `--focus`; research `--depth deep`; adversarial `--compare`; spec-panel `--mode critique --focus requirements` and `architecture,testing`; design `--type api --format spec`; brainstorm `--depth`, `--resume-from`; release-split `<spec-file-path>`; pr-submit `--monitor --head --title --body --resume`; crash-recovery `--since 24h`; troubleshoot `--type --depth --fix` | argument-hint/usage lines in `MS/commands/*.md` (auggie-review:8, test:22, document:22, analyze:22, research:25, adversarial:23, spec-panel:22/25, design:22, brainstorm:34-40, release-split:19, pr-submit:8); `MS/skills/sc-crash-recovery/SKILL.md:26` |
| `/sc:task` level-2 claims | Correct: the L14 rename example matches no STRICT, EXEMPT, or LIGHT keyword, so it lands in STANDARD, which runs affected tests; LIGHT ("typo", "comment") executes directly; "refactor" is a STRICT keyword (L162) | `MS/commands/task.md:73-91, :100`; `MS/skills/sc-task-protocol/SKILL.md:105` |
| `/sc:implement` runs tests | Correct as "extras" (not the verdict) | `MS/skills/sc-implement-protocol/SKILL.md:119, :134` |
| Workflow plan has acceptance criteria | Correct | `MS/skills/sc-workflow-protocol/SKILL.md:44` |
| Task folder moves to done on pass | Correct (task adapter) | `MS/skills/sc-reflect-protocol/refs/promotion-adapters.md:11` |
| pr-submit `--monitor 1` does not edit | Correct ("apply edits at L1" is in Will Not) | `MS/commands/pr-submit.md:85` |
| Order of 3.11 (commit, reviews, push approval, open PR) | Correct. `pr-submit` opens the PR through `gh` on the origin repo, so pushing first (step 5) is the right order | `MS/commands/pr-submit.md:19, :83` |

## Summary

- Prior findings: 20 of 24 resolved, plus F15 handled by removal (needs user adjudication). Not fully resolved: F5 (N1), F20 (N2), F22 (N7).
- Current issues: 10 total (IMPORTANT 3: N1, N2, N3; MINOR 7: N4-N10; CRITICAL 0). The count fell from 24 to 10, so the monotonicity guard does not fire, and no item that passed before has regressed.
- Issues fixed in place: 0 (report-only; the guide was not edited)

## Issues Found (index)

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| N1 | IMPORTANT | 3.3 step 2 (L113) | The stop message does not show the ruling format (prior F5) | Point to `refs/ledger.md` "Ruling line" and give the worked example |
| N2 | IMPORTANT | Section 1 hard limit (L20) vs L14, L127, L157-159 | Contradicts level 2 example, small bug fix, folder cleanup (prior F20) | Exclude the matching test file and add the cleanup exception, or reroute the three places |
| N3 | IMPORTANT | 3.1 step 7 (L72-73), 3.10 (L182) | Claims roadmap task files carry a `reflect_pre` result; no branch for `skipped`; fallback omits `--spec` | Reword, add `--spec`, add the skipped branch |
| N4 | MINOR | Level 4 row (L16) | `--spec` looks mandatory; research report would be misused as spec | Mark optional and say what qualifies |
| N5 | MINOR | 3.4 (L122, L128) | `--fix` chosen before diagnosis; no inconclusive branch; no stop-note link | N5 replacement |
| N6 | MINOR | 3.3 step 3 (L115) | No ship step; `/code-review` duplicates 3.11 | Route to 3.11 |
| N7 | MINOR | L16, L73, L75-77 | "Phase" means two things; "build request" not defined (prior F22) | Inline definitions |
| N8 | MINOR | Section 5 (L239) | "Ask a narrow question" pushes `/roadmap` off the setting that makes task files | Split advice per skill |
| N9 | MINOR | Level 3 row (L15) | Progress folder is `plan-<hash>`, not the workflow name | Correct the path, note it is printed |
| N10 | MINOR | 3.1 step 9 (L79) | "Fix them" with no mechanism; folder stays in to-do on fail | N10 replacement |

## Removals to adjudicate

- **F15 removal (made by the author):** the manual `/sc:reflect --mode post` step for small bug fixes (old 2.4 step 4) is gone. Why: it had no plan or spec to compare against. The user should confirm.
- **No removals proposed by this review.**

## Confidence Gate

- **Checklist for this fix cycle:** 24 prior-finding re-checks plus 6 re-scan categories (order, missing steps, vague prompts, jargon, contradictions, cross-references) = 30 items.
- **Confidence:** Verified: 28/30 | Unverifiable: 2 | Unchecked: 0 | Confidence: 100.0% (28 / (30 - 2)). The verdict is FAIL because issues exist, not because of low confidence.
- **Unverifiable items:** (1) F4 and F24 source line ranges (`MS/skills/task/SKILL.md:120, :180, :254`; `MS/skills/tech-research/SKILL.md:136`) were not reopened this cycle, because the guide text matches the prior replacement word for word; I marked them resolved on that basis. (2) Whether roadmap BUILD_REQUEST CONTEXT FILES bullets resolve as a `PRD:`/`TDD:` spec field. That needs a live run, so N3 is written as "not guaranteed", not "wrong".
- **Tool engagement:** Read: 5 | Grep: 0 (content searches ran through Bash grep) | Glob: 0 | Bash: 17 | Edit: 6 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0

## QA Complete
