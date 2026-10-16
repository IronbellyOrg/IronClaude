# QA Report: Fix-Cycle Re-Review, Redundancy Lens (IronClaude New User Guide)

**Topic:** Steps the guide tells the user to run that a skill already performs internally (or that repeat a skill run already done)
**Date:** 2026-10-02
**Phase:** fix-cycle (adversarial, redundancy lens; report-only, guide NOT edited)
**Fix cycle:** 1 (re-review of `11-review-redundancy.md`)
**Guide under review:** `/Users/cmerritt/GFxAI/IC-Harness/.dev/research/ironclaude-user-guide-20261001/IRONCLAUDE-NEW-USER-GUIDE.md` (239 lines; workflows renumbered 2.x to 3.x)
**Prior report:** `/Users/cmerritt/GFxAI/IC-Harness/.dev/research/ironclaude-user-guide-20261001/11-review-redundancy.md`
**Source truth:** `/Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/` (working tree `feat/tier-tools-update` @ 47d7f9be). `git diff origin/master` (50a8c7f4) is empty for every file cited below, so all cites are valid on master. All `path:line` cites are relative to `src/superclaude/`.

---

## Overall Verdict: FAIL

All 10 prior findings (R1-R7, W1-W3) are resolved. The re-scan found 3 remaining redundancy defects of the same class (N1-N3), all introduced or exposed by the new content: the model `/task-builder` request in section 2 still omits `--spec` (so the built-in spec check is skipped and the user is later sent to run it by hand), the new 3.10 sorts task files by "was `--spec` typed" instead of by the recorded check result (so it sends the user to re-run a check that already ran), and the 3.4 fallback re-runs a whole diagnosis that already exists on disk. Plus 2 advisory observations outside the strict class (O1, O2).

## Part 1: Prior findings, verified against the new text

| # | Prior finding | Result | New text (quoted, guide line) | Why it is resolved |
|---|---|---|---|---|
| R1 | 2.1 step 9 manual tests + `/sc:reflect --mode post` | RESOLVED | L79: "**Confirm the phase passed, then start the next one.** Open the task file and read the `reflect_post` entry at the top: the audit's verdict and the path to its report. If it lists unresolved problems, fix them before the next phase. A passed task folder moves from `.dev/tasks/to-do/` to `.dev/tasks/done/`." | No manual tests or reflect. Reads the result of the in-task POST item (`skills/task-builder/SKILL.md:2371` Rule 20: penultimate POST reflect item records `{verdict, run_id, report}` to `reflect_post`). |
| R2 | 2.2 step 5 manual tests + reflect | RESOLVED | L102: "**Confirm and ship.** Read the task file's `reflect_post` verdict (as in 3.1 step 9), then workflow 3.11." | Same. |
| R3 | 2.4 step 4 manual reflect on the `--fix` path | RESOLVED | L128: "...then `/task <path>`. The task file runs its own reviews, tests, and final audit; read its `reflect_post` verdict when it finishes." L130: "**Ship.** Workflow 3.11." | No manual reflect on either path. The guide also (correctly) does not tell the user to run troubleshoot's Phase D `/sc:reflect --type task --validate` (`commands/troubleshoot.md:193`, `skills/sc-troubleshoot-protocol/SKILL.md:560`), which would duplicate the in-task POST audit (prior S2). |
| R4 | 2.10 told the user to re-run PRE reflect on task-builder/roadmap files | RESOLVED (with a new defect, see N2) | L182: "**Task files from `/task-builder --spec` or from `/roadmap`** have already been checked against the spec. Read the `reflect_pre` entry at the top of the task file and resolve anything it lists before running `/task`." | The redundant case is removed. The replacement's sorting rule creates N2. |
| R5 | 2.2 step 3 omitted `--spec` | RESOLVED in 3.2 | L97: "`/task-builder \"Implement monthly CSV export ...\" --spec docs/specs/invoice-csv-export.md`"; L98: "Passing `--spec` makes task-builder check that every requirement in the spec has a task. Anything it missed is listed under Open Questions ... the check's result is in the `reflect_pre` entry at the top. Without `--spec` this check is skipped." | Accurate: `skills/task-builder/SKILL.md:1666` (skipped only when no spec resolves), `:1683` (fail appends `unmapped_requirements` to Open Questions), `:1689-1698` (`reflect_pre` block). Level 4 row L16 also carries `--spec`. Not resolved everywhere: section 2 L36 still omits it (N1). |
| R6 | 2.4 re-run with `--fix` repeats diagnosis | RESOLVED as proposed | L122: "If the fix may span several files, add `--fix` now. After the diagnosis it offers to build a task file for the fix, and changes nothing unless you accept." | Matches `commands/troubleshoot.md:54`, `:192` and `skills/sc-troubleshoot-protocol/SKILL.md:551-558`. The fallback parenthetical I proposed in 11 still repeats the diagnosis; see N3 (self-correction). |
| R7 | 2.3 step 3 unconditional "run the tests" | RESOLVED | L115: "**Before committing:** run `/code-review` (it looks for bugs, which the step-by-step reviewer does not). Run the tests yourself only if nothing ran them: a plain edit, or a trivial `/sc:task` change." L112: "It runs the tests itself as it goes." | `skills/sc-implement-protocol/SKILL.md:119` (Q6 runs tests); `skills/sc-task-protocol/SKILL.md:86-97` (STRICT runs `pytest`). |
| W1 | 2.1 step 8 "verify each phase" | RESOLVED | L77: "Let it run to the end. Each task file already contains everything that checks the work: reviewer panels after each phase, the tests, and, as its last steps, an independent audit (`/sc:reflect`) comparing what was built with the plan. Do not run those checks again yourself." | Explicit anti-duplication instruction. |
| W2 | Promote row + task-file location | RESOLVED | L236: "Moves the finished work folder to a \"done\" location. Inside `/task` this is expected: a passed task folder moves to `.dev/tasks/done/`. \| Add `--no-promote` only when you run `/sc:reflect` yourself." L202: "Unfinished task files are under `.dev/tasks/to-do/`; finished ones move to `.dev/tasks/done/`." | Matches the in-task POST run promoting by default (CLI arm passes `--promote` explicitly, `skills/task-builder/SKILL.md:2371`). |
| W3 | spec-panel described as the check `/prd` already ran | RESOLVED | L53: "The skill researches, writes, and reviews the PRD itself, including its own consistency checks." L57: "A panel of named software-requirements experts judges whether the requirements are measurable, testable, and complete. It only reports." | Distinguishes the built-in QA from the outside critique. Re-confirmed no RF skill invokes spec-panel (grep `spec-panel` in prd, tdd, roadmap, task-builder, task, tech-research: 0 hits). "It only reports" matches `commands/spec-panel.md` Boundaries "Will Not: Modify specifications without explicit user consent". |

Prior findings: 10 / 10 resolved. The rules section adds a general guard, L215: "**Do not repeat a skill's own checks.** Task files already run reviewer panels, tests, and a final audit. Read their results instead of running the same checks again."

## Part 2: Whole-guide re-scan, new and remaining defects

### N1 [IMPORTANT] Section 2 model request omits `--spec`, which skips the built-in check and routes the user to a manual re-run (guide L36)

- **Quoted (L36):** "`/task-builder \"Add per-tenant rate limits as recommended in .dev/tasks/to-do/TASK-RESEARCH-rate-limits-<timestamp>/RESEARCH-REPORT-rate-limits.md. Code: src/api/middleware/, src/tenants/. Why: one tenant is overloading the API.\"`"
- **Problem:** this is the "strong request" every new user copies, and it is the exact R5 defect in a different place. A plain path inside the goal is not `--spec` and not an `@file`, so the spec does not resolve and task-builder records `reflect_pre: verdict: skipped` (`skills/task-builder/SKILL.md:41`, `:285` resolution order; `:1666` skipped only when no spec resolves). 3.10 bullet 2 (L183) then tells the user that "a task file built without `--spec` ... has not been checked. Run: `/sc:reflect --mode pre ...`". Net effect: the user hand-runs the coverage audit that task-builder would have run itself, mandatorily, if the example had passed the report (`:1662-1666`, "When a `--spec` resolves, running reflect to completion is MANDATORY"). Level 5 (L17, "give the report it writes to `/task-builder` (level 4)") does not say how, so L36 is the only worked example.
- **Replacement (L36, right cell):** "`/task-builder \"Add per-tenant rate limits as recommended in the research report. Code: src/api/middleware/, src/tenants/. Why: one tenant is overloading the API.\" --spec .dev/tasks/to-do/TASK-RESEARCH-rate-limits-<timestamp>/RESEARCH-REPORT-rate-limits.md`"
- **Replacement (L17, Level 5 "What you run"):** "... Then build the task file from it: `/task-builder \"<what to build>\" --spec <path to the report>` (level 4)."

### N2 [IMPORTANT] 3.10 sorts task files by "was `--spec` typed", not by whether the check ran, so it sends users to re-run a check that already ran (guide L182-183)

- **Quoted (L182):** "**Task files from `/task-builder --spec` or from `/roadmap`** have already been checked against the spec."
- **Quoted (L183):** "**A `/sc:workflow` plan, a task file built without `--spec`, or a plan you wrote yourself** has not been checked. Run: `/sc:reflect --mode pre --spec ... --tasklist ...`"
- **Problem:** "built without `--spec`" is not the same as "not checked". Three cases are mis-sorted into the run-it-again bullet:
  1. **Spec resolved another way.** task-builder also resolves the spec from an `@file` in the goal or a `SPEC:`/`PRD:`/`TDD:` field in a build request (`skills/task-builder/SKILL.md:41`, `:285`), and then the PRE check is mandatory (`:1662-1666`). A user who wrote `@docs/specs/x.md` gets a checked file but is told to check it again.
  2. **`/sc:troubleshoot --fix` task files.** troubleshoot's Phase A builds the task file with no `--spec` (GOAL "Apply the fix described in `<REPORT.md path>`", `skills/sc-troubleshoot-protocol/SKILL.md:557`), then Phase B immediately runs `/sc:reflect --type task --analyze` on it (`:558`), which maps to `--mode pre` (`commands/reflect.md:47`, `:115`). The guide's 3.4 L128 sends the user to such a file; under 3.10 it is "built without `--spec`", so the user re-runs the pre-check troubleshoot already ran.
  3. **3.1 step 7 build-request path (new content, L73).** The user creates phase task files with "`/task-builder <path to that build request>`", which is literally "built without `--spec`", yet the same files are "from `/roadmap`". Both bullets match; the user cannot tell which applies. Whether task-builder resolves the spec from the roadmap build request is unverified: the build-request format lists sources as bullets "- PRD (if present): [path] §... L..." and "- TDD (if present): ..." under CONTEXT FILES (`skills/roadmap/SKILL.md:612-613`), not as a top-level `PRD:`/`TDD:` field, and roadmap itself invokes task-builder with only the build-request path (`:658`). The recorded `reflect_pre` verdict is the only reliable signal.
- **Replacement (L182-185, whole 3.10 body):**
  "Open the task file and read the `reflect_pre` entry at the top.
  - **`verdict: pass` or `fail`:** it has already been checked against the spec. Resolve anything it lists under Open Questions before running `/task`. Do not run the check again.
  - **`verdict: skipped`, a `/sc:workflow` plan, or a plan you wrote yourself:** it has not been checked. If `/sc:troubleshoot --fix` built it, the check already ran during that command; act on what it showed you. Otherwise run:
    `/sc:reflect --mode pre --spec docs/specs/invoice-csv-export.md --tasklist .dev/workflow/invoice-csv-export/plan.md`
    The report in `.dev/reflect/pre-<name>-<timestamp>/` lists every requirement the plan misses. Fix the plan, then build."

### N3 [MINOR] 3.4 fallback re-runs the whole diagnosis that already exists on disk (guide L128)

- **Quoted (L128):** "accept the task-file offer from step 1 (if you did not pass `--fix`, run the diagnosis again with it), then `/task <path>`."
- **Problem (self-correction of my own R6 text in report 11):** "run the diagnosis again" repeats Tier 1 and possibly Tier 2 (1-3 min, plus 4-15 min with extra agents, `commands/troubleshoot.md:75-76`) to regenerate a REPORT.md the user already has. The `--fix` chain adds nothing that needs the re-diagnosis: Phase A only calls task-builder with GOAL "Apply the fix described in `<REPORT.md path>`", WHERE = cited files (`skills/sc-troubleshoot-protocol/SKILL.md:557`), and Phase B is a `--mode pre` reflect (`:558`, `commands/reflect.md:115`), which task-builder runs itself when given `--spec` (`skills/task-builder/SKILL.md:1662-1666`). The source does sanction re-running (`commands/troubleshoot.md:191`), so this is not wrong, only wasteful; under the user's stated rule it should go.
- **Replacement (L128):** "**Fix across several files:** accept the task-file offer from step 1 and run `/task <path>`. If you did not pass `--fix`, do not diagnose again; build the task file from the report you already have: `/task-builder \"Apply the fix described in the report. Code: <files the report cites>\" --spec .dev/troubleshoot/<name>-<timestamp>/REPORT.md`, then `/task <path>`. The task file runs its own reviews, tests, and final audit; read its `reflect_post` verdict when it finishes."
- **Removal note (for user adjudication):** removes the instruction "run the diagnosis again with it". Why: it re-does a finished diagnosis.

## Part 3: Advisory observations (outside the strict class; do not drive the verdict)

| # | Location | Observation | Suggested text |
|---|---|---|---|
| O1 | 3.1 step 7, L72 vs sub-bullet L73 | Opposite of redundancy: L72 says "It has already checked every phase task file against the PRD and TDD." On the build-request path (L73) that is not true. Standard tier omits Phase 5, and roadmap's Stage 4 task-file validation (cross-task consistency, roadmap-to-task, input-to-task fidelity) lives inside Phase 5 (`skills/roadmap/SKILL.md:649`, `:654`, `:662`). Task files the user builds by hand from build requests get task-builder's own gates only. Belongs to the accuracy lens; flagged so the N2 fix is not read as "everything from `/roadmap` is checked". | Append to L73: "Task files you build this way skip the roadmap's final cross-phase check, so read each one's `reflect_pre` entry (3.10)." |
| O2 | 3.3 step 3 (L115) and 3.11 step 2 (L190) | 3.3 runs `/code-review` before committing; 3.3 has no ship step, but a user who then opens a PR via 3.11 runs `/code-review` again on the same unchanged diff. Guide-step repeat, not a skill's internal check. | L115: "**Before committing:** run `/code-review` ... If you will open a pull request, skip this step: workflow 3.11 step 2 runs it." Or end 3.3 with "4. **Ship.** Workflow 3.11." and drop `/code-review` from step 3. |

## Part 4: New content checked and kept (complementary, with evidence)

| # | Guide location | Suspected overlap | Verdict and evidence |
|---|---|---|---|
| K1 | 3.1 step 7 note (L73): `/task-builder <build request>` | Does roadmap already build these? | KEEP. Standard tier stops at build requests: "roadmap + BUILD_REQUESTs (no automatic task file creation)" (`skills/roadmap/SKILL.md:107`, `:649`). Nothing else creates the task files. "Full roadmap" forces Deep (`:112`), as the note says. |
| K2 | 3.1 step 7 (L71-72): "Dry run first", then confirm | Does confirming re-run the analysis? | KEEP. On "yes" the skill continues from A.5; it does not restart (`skills/roadmap/SKILL.md:2644`). Single run. |
| K3 | 3.1 step 3 (L57): re-run spec-panel until no critical findings | Does spec-panel loop internally (`--iterations`)? | KEEP. `--iterations N` is multi-pass review of the same text in one run (`commands/spec-panel.md:234-248`); spec-panel will not modify the spec without consent (Boundaries, "Will Not"). Re-running after the user applies fixes reviews new text. |
| K4 | 3.1 step 1 then step 2 (`/sc:brainstorm` then `/prd`) | Does brainstorm hand off to `/prd`? | KEEP. Handoff targets are `none`/`design`/`tasklist`/`task` only (`commands/brainstorm.md:60`); guide uses the default. |
| K5 | 3.2 step 3 (L97-98) `--spec` + "Read the task file and its Open Questions" | Re-checking what PRE did? | KEEP. Reading results, not re-running. Text is accurate (`skills/task-builder/SKILL.md:1683`). |
| K6 | 3.3 step 2 (L109-113) `/sc:workflow` then `/sc:implement`; `E-HALT-QA` ruling | Double invocation or duplicate tests? | KEEP. Default handoff `none` (`commands/workflow.md:42`; implement invoked only on `--handoff implement`, `skills/sc-workflow-protocol/SKILL.md:18`), one implement run; guide adds no test run after it (L112). `E-HALT-QA` matches `skills/sc-implement-protocol/SKILL.md:31`. |
| K7 | 3.4 step 1 (L122) `--fix` up front; step 3 small fix (L127) | Duplicate checks? | KEEP. `--fix` offers, never auto-applies (`commands/troubleshoot.md:54`). Small fix has no task file, so `/sc:test` is the only test run. |
| K8 | 3.4 omits troubleshoot Phase D `/sc:reflect --type task --validate` | Should the guide tell the user to run it? | KEEP the omission. Phase D (`skills/sc-troubleshoot-protocol/SKILL.md:560`, `commands/troubleshoot.md:193`) is a `--mode post` audit (`commands/reflect.md:48`, `:116`) on a task file whose own POST item already ran it (`skills/task-builder/SKILL.md:2371`). Source-side duplicate S2 from report 11 still stands for maintainers. |
| K9 | 3.7 step 3 (L162) large refactor via `/task-builder ... --spec` | Duplicate with `/sc:task` strict? | KEEP. Alternatives, not sequential. "refactor" keyword triggers STRICT (`skills/sc-task-protocol/SKILL.md:60`). |
| K10 | 3.10 bullet 1 (L182) | Re-run on checked files? | KEEP the intent (read, do not re-run). Sorting rule fixed by N2. |
| K11 | 3.11 steps 2-6 | pr-submit `--monitor 1` already reviewing? | KEEP (unchanged from report 11 K6/K7). The Augment-bot vs `/sc:auggie-review` engine-identity question remains Unverified (`skills/sc-pr-submit-protocol/SKILL.md:19`). |
| K12 | Rules section (L213-220) | Any rule ordering a duplicate check? | KEEP. L215 forbids repeating a skill's checks; L217 "Read a plan or task file before you run it" is a human read, not a re-run of PRE reflect. No rule orders a re-run. |
| K13 | Level 2/3/4 rows (L14-16) | Duplicate tests after `/sc:task` or `/sc:implement`? | KEEP. L14 asks for a manual test only when `/sc:task` skipped checking (trivial tier, `skills/sc-task-protocol/SKILL.md:124-129`). |

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | R1 resolved | PASS | Guide L79; task-builder Rule 20 `:2371` |
| 2 | R2 resolved | PASS | Guide L102 |
| 3 | R3 resolved | PASS | Guide L128, L130; troubleshoot `:193`, protocol `:560` |
| 4 | R4 resolved | PASS (new defect N2) | Guide L182 |
| 5 | R5 resolved | PASS in 3.2 / L16 (N1 elsewhere) | Guide L97-98; task-builder `:1666`, `:1683`, `:1689` |
| 6 | R6 resolved | PASS as proposed (N3 self-correction) | Guide L122; troubleshoot `:54`, `:192` |
| 7 | R7 resolved | PASS | Guide L112, L115; implement `:119` |
| 8 | W1 resolved | PASS | Guide L77 |
| 9 | W2 resolved | PASS | Guide L202, L236 |
| 10 | W3 resolved | PASS | Guide L53, L57; spec-panel Boundaries; grep 0 hits |
| 11 | Re-scan: section 1 and 2 | FAIL | N1 (L36, L17) |
| 12 | Re-scan: 3.1 incl. step 7 note | PASS for redundancy (O1 advisory) | K1, K2, K3, K4 |
| 13 | Re-scan: 3.2 step 3 `--spec` | PASS | K5 |
| 14 | Re-scan: 3.3 | PASS for redundancy (O2 advisory) | K6 |
| 15 | Re-scan: 3.4 `--fix` | FAIL | N3; K7, K8 |
| 16 | Re-scan: 3.5-3.9, 3.12 | PASS | No check-running steps beyond single skill runs; K9 |
| 17 | Re-scan: 3.10 | FAIL | N2 |
| 18 | Re-scan: 3.11 | PASS | K11 |
| 19 | Re-scan: rules section | PASS | K12 |

## Summary

- Prior findings resolved: 10 / 10.
- New or remaining redundancy defects: 3 (IMPORTANT: 2, N1 and N2; MINOR: 1, N3).
- Advisory observations outside the strict class: 2 (O1, O2).
- New content checked and kept: 13 (K1-K13).
- Checks passed: 16 / 19; failed: 3 (items 11, 15, 17).
- Issues fixed in place: 0 (report-only; guide not edited, per instruction).
- Source-side items for IronClaude maintainers from report 11 still open: S1 (`commands/reflect.md:275`, also `:260`, "The operator re-runs `/sc:reflect --mode post`") and S2 (troubleshoot Phase D). Not guide edits.

## Explicit removals proposed (each needs user adjudication)

- Remove from 3.4 step 3 (L128): "run the diagnosis again with it". Why: it repeats a finished diagnosis; replace with building the task file from the existing REPORT.md (N3).
- Remove from 3.10 (L183) the phrase "a task file built without `--spec`" as the trigger for a manual run. Why: it sends users to re-run checks that already ran; replace with the `reflect_pre` verdict test (N2).
- (Advisory, O2) Remove `/code-review` from 3.3 step 3 if 3.3 is made to end in workflow 3.11. Why: 3.11 step 2 runs it on the same diff.

## Confidence Gate

- **Confidence:** Verified: 19/19 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. One sub-point carried as explicitly Unverified and not affecting any verdict: whether task-builder resolves a spec from a roadmap build request's CONTEXT FILES bullets (N2 case 3); the N2 replacement is correct under either outcome because it keys on the recorded `reflect_pre` verdict. K11 Augment engine identity remains Unverified from report 11.
- **Tool engagement:** Read: 2 | Grep: 0 (content search through Bash grep/sed, 11 calls) | Glob: 0 | Bash: 12 | Write: 1 | Edit: 9. No web research (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0).
- **Fix-cycle monotonicity:** cycle 0 (report 11) |F| = 10; cycle 1 |F| = 3. Strictly shrinking; no regression (no prior PASS item now fails).

## Self-Audit

Not applicable as a PASS self-audit (verdict is FAIL). Evidence that the re-scan was real rather than a confirmation pass: every new-content area named in the request was checked against source (3.1 step 7 note: `roadmap/SKILL.md:107`, `:112`, `:649`, `:654`, `:662`, `:2644`; 3.2 step 3: `task-builder/SKILL.md:41`, `:1662-1698`; 3.3: `sc-implement-protocol/SKILL.md:31`, `:119`, `commands/workflow.md:42`; 3.4 `--fix`: `commands/troubleshoot.md:54`, `:75-77`, `:191-193`, `sc-troubleshoot-protocol/SKILL.md:557-560`, `commands/reflect.md:47-48`, `:115-116`; 3.10: as N2; 3.11: `sc-pr-submit-protocol/SKILL.md:19`; rules: guide L213-220). One defect (N3) is in text I proposed in report 11; it is flagged rather than defended.

## QA Complete
