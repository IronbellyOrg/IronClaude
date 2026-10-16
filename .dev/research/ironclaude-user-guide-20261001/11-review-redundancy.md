# QA Report: Redundancy Lens (IronClaude New User Guide)

**Topic:** Steps the guide tells the user to run manually that an already-invoked skill (or the next skill in the chain) already performs internally
**Date:** 2026-10-01
**Phase:** report-validation (adversarial, redundancy lens; report-only, guide NOT edited)
**Fix cycle:** N/A
**Guide under review:** `/Users/cmerritt/GFxAI/IC-Harness/.dev/research/ironclaude-user-guide-20261001/IRONCLAUDE-NEW-USER-GUIDE.md` (154 lines)
**Source truth:** `/Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/` (working tree on branch `feat/tier-tools-update` @ 47d7f9be). Every cited file was diffed against `origin/master` @ 50a8c7f4 (2026-09-30): all cited files are byte-identical to master except `skills/sc-reflect-protocol/SKILL.md`, which differs by 3 lines in a model-alias table at L224-235 (net zero line shift; no cited line is affected). All `path:line` cites below are therefore valid on master.

---

## Overall Verdict: FAIL

Seven genuine redundancies (the user-caught one plus six more of the same kind), three wording/consequence defects created by them, and one source-side inconsistency that probably caused the original error. Six other suspected overlaps were checked and are complementary (keep).

## Source facts established (the evidence base for every finding)

| # | Fact | Evidence (path:line, relative to `src/superclaude/`) |
|---|---|---|
| F1 | task-builder runs its OWN PRE reflect gate (`/sc:reflect --mode pre --remediate --spec <spec>`) on every task file it builds, before handing it back. It is mandatory whenever a spec resolves; a missing report is a hard STOP. | `skills/task-builder/SKILL.md:210` (step 14), `:1662-1672` (A.10.7, "running reflect to completion is MANDATORY"), `:1701` (Mandatory-run check, hard STOP) |
| F2 | The PRE gate only fires if a spec resolves, in this order: `--spec <path>`, then an `@file` in the goal, then a `SPEC:`/`PRD:`/`TDD:` field in a BUILD_REQUEST. Otherwise it records `verdict: skipped (no-spec)`. | `skills/task-builder/SKILL.md:41`, `:1666`, `:1684` |
| F3 | Every task-builder task file carries `POST_REFLECT_GATE: ENABLED` and a penultimate item N.{X-1} in which a dedicated subagent runs `sc-reflect-protocol --mode post --remediate --diff {BASE}..HEAD --tasklist {TASK_FILE} [--spec ...]` end to end. The validator FAILs a task file without it. | `skills/task-builder/SKILL.md:1077`, `:2215-2233` (command at `:2223`), `:2310` (validator: present and penultimate) |
| F4 | That in-task POST run does NOT pass `--no-promote`, and reflect promotes by default, so on a pass it moves `.dev/tasks/to-do/TASK-*` to `.dev/tasks/done/TASK-*`. | `skills/task-builder/SKILL.md:2223`; `skills/sc-reflect-protocol/SKILL.md:95`, `:1508` |
| F5 | `/task` executes every item (so it executes the POST reflect item), runs a 6+ agent phase-gate QA after every phase from Phase 2 on, runs Post-Completion Validation, and in that validation runs the relevant test suite for any code-modifying task and HALTs on failure. It also reconciles the reflect return contract. | `skills/task/SKILL.md:116-119`, `:282`, `:286-297` (check 4 = tests), `:576` |
| F6 | task-builder must encode testing items in the task file whenever TESTING_REQUIREMENTS is not NONE. | `skills/task-builder/SKILL.md:2367` (Rule 18), `:1572-1574` |
| F7 | `/prd` and `/tdd` are two-stage skills: they spawn `rf-task-builder` and then run `/task`; their task files embed rf-analyst, rf-qa (research, synthesis, report gates) and rf-qa-qualitative content review, including an internal-consistency/contradiction check. No skill invokes `/sc:spec-panel`. | `skills/prd/SKILL.md:10`, `:154-165`, `:416-423`; `skills/prd/refs/agent-prompts.md:382`, `:436`; `skills/tdd/SKILL.md:10`, `:146`, `:407-414`; grep for `spec-panel` across prd, tdd, roadmap, task-builder, task, tech-research: 0 hits |
| F8 | `/roadmap` runs task-builder per phase AND validates the outputs: Stage 1 document QA with 2-4 source-fidelity agents against the PRD/TDD, Stage 2 forward/backward coverage validation, Stage 3 per-BUILD_REQUEST source-fidelity, Stage 4 post-creation task-file validation (cross-task consistency, roadmap-to-task and input-to-task fidelity). "The user's only remaining action after the skill completes is to execute each phase in order using `/task`." | `skills/roadmap/SKILL.md:8`, `:10`, `:27-33`, `:185-188`, `:426`, `:446-448`, `:564-589` |
| F9 | `/tech-research` uses task-builder and `/task` only to produce its research report. It never builds an implementation task file; Phase 7 only suggests `/tech-reference`. | `skills/tech-research/SKILL.md:10`, `:167`, `:589-605`, `:569-573` |
| F10 | `/sc:troubleshoot --fix` Tier 3 chain: Phase A invokes task-builder; Phase B runs reflect on the new task file; Phase C stops and hands the user `/task <path>`; Phase D runs `/sc:reflect --type task --validate` (or self-review) when the user reports back. There is no way to reuse an earlier REPORT.md; adding `--fix` means a full re-diagnosis. | `skills/sc-troubleshoot-protocol/SKILL.md:549-560`, `:604-605`; `commands/troubleshoot.md:54`, `:77`, `:191` |
| F11 | `/sc:workflow --handoff implement` invokes `sc:implement-protocol` itself. Without `--handoff` (default `none`) it only prints the next step. `/sc:workflow` has no spec-coverage audit (gate is schema-level). | `skills/sc-workflow-protocol/SKILL.md:18` (vocabulary row), Wave 3; `skills/sc-workflow-protocol/refs/overlap-routing.md:5`, `:10`; `commands/workflow.md:42` |
| F12 | `/sc:implement` runs a spec-compliance review after every task (reviewer, not implementer voice), then Q6 detects and runs lint/typecheck/tests, then a whole-list review. It is a spec-compliance reviewer, not a bug reviewer. | `skills/sc-implement-protocol/SKILL.md:9`, `:112-119`, `:134`, `:142-148` |
| F13 | `/sc:task` STRICT runs a quality-engineer verification agent plus `pytest`; STANDARD runs affected tests; LIGHT and EXEMPT skip verification. | `skills/sc-task-protocol/SKILL.md:86-97`, `:105`, `:124-129` |
| F14 | `/sc:pr-submit --monitor 1` opens the PR, waits for the Augment Code bot, verifies findings, sends verified ones to `/sc:troubleshoot`, proposes fixes without edits, then waits for CI. It does NOT run `/code-review`, `/security-review`, or `/sc:auggie-review` (auggie fallback only at L2+ on an oversized-PR decline). It does NOT push the branch. Its own test validator (VG-1..4) runs only at L2+. | `skills/sc-pr-submit-protocol/SKILL.md:76`, `:130`, `:134-137`, `:139`, `:144-149` |
| F15 | SOURCE-SIDE: the reflect command tells the operator to re-run `/sc:reflect --mode post` after `/task` completes. This predates/ignores the POST item that task-builder now embeds (F3) and is the most likely origin of the guide's error. | `commands/reflect.md:275` |


## Findings: genuinely redundant (remove or rewrite)

### R1 [CRITICAL, user-caught] 2.1 step 9 (guide L36)

- **Quoted:** "**Check each phase against the plan.** Run the tests, then `/sc:reflect --mode post --diff <commit or branch> --no-promote`, which independently checks that what was built matches what was planned."
- **Already done by:** `/roadmap` builds every phase task file through task-builder (F8), so each one carries the POST reflect item (F3), and `/task` executes it (F5). `/task` Post-Completion check 4 already ran the tests (F5, `task/SKILL.md:297`); the task file also has its own test items (F6). A manual second run audits the same diff twice and, because the in-task run already promoted the folder (F4), points at a moved task.
- **Corrected text:** "9. **Confirm each phase passed.** When `/task` finishes, open the task file. Its last items already ran the tests, the reviewer checks, and an independent plan-versus-build check (`/sc:reflect --mode post`). Check that the frontmatter `reflect_post` verdict is PASS and that anything it flagged is resolved in Open Questions. Do not run `/sc:reflect` again yourself. A passing task folder is moved from `.dev/tasks/to-do/` to `.dev/tasks/done/`."

### R2 [IMPORTANT] 2.2 step 5 (guide L48)

- **Quoted:** "**Verify.** Tests, then `/sc:reflect --mode post --diff <commit or branch> --no-promote`, then workflow 2.11."
- **Already done by:** the task file came from `/task-builder` in step 3, so it has the POST reflect item (F3) and `/task` ran it plus the tests (F5, F6). Same defect as R1.
- **Corrected text:** "5. **Verify.** Check the task file's `reflect_post` verdict is PASS (`/task` already ran the tests and the independent post-build check). Then follow workflow 2.11."

### R3 [IMPORTANT] 2.4 step 4 (guide L63), for the `--fix` path

- **Quoted:** "**Confirm.** `/sc:reflect --mode post --diff <commit or branch> --no-promote`, then workflow 2.11."
- **Already done by:** on the multi-file path the task file is built by task-builder inside `/sc:troubleshoot` Phase A (F10), so it carries the POST reflect item (F3) that `/task` runs (F5). `/sc:troubleshoot` Phase D also offers its own post-execution validation when you report back (F10, `sc-troubleshoot-protocol/SKILL.md:560`). The manual run is a third audit of the same diff.
- **Classification by path:** genuinely redundant for the `--fix` / task-file path. On the small-fix path (no task file) nothing else audits the change, so a manual reflect is complementary there, though `/sc:test` plus workflow 2.11 is already the guide's gate for a small fix.
- **Corrected text:** "4. **Confirm.** Small fix: workflow 2.11. Task-file fix: check the task file's `reflect_post` verdict is PASS (`/task` already ran the independent post-build check), then workflow 2.11."

### R4 [IMPORTANT] 2.10 as a whole (guide L106-110), applied to task files from `/task-builder` or `/roadmap`

- **Quoted:** "If you have a spec and a plan or task file built from it, check that the plan covers everything in the spec before you start: `/sc:reflect --mode pre --spec <path to spec> --tasklist <path to plan or task file>`."
- **Already done by:** task-builder runs exactly this PRE coverage audit itself whenever a spec resolves, and records it in the task file frontmatter as `reflect_pre` (F1). `/roadmap` additionally runs source-fidelity and forward/backward coverage validation on its phase task files (F8). Running it again by hand duplicates a mandatory built-in gate.
- **Complementary case (keep):** a `/sc:workflow` `plan.md` has no spec-coverage audit (F11), and a hand-written plan has none either. 2.10 is correct for those.
- **Corrected text:** "### 2.10 Check a plan before you run it\nTask files from `/task-builder` (when you pass `--spec`) and from `/roadmap` are already checked against the spec: look at `reflect_pre` in the task file's frontmatter and fix anything it lists before running `/task`. For a `/sc:workflow` plan or a plan you wrote yourself, run `/sc:reflect --mode pre --spec <path to spec> --tasklist <path to plan>`. It lists any requirement the plan misses. Fix the plan, then build."
- **Unverified (flag):** whether `/roadmap` phase BUILD_REQUESTs make task-builder's PRE gate fire. The BUILD_REQUEST format lists sources as `- PRD (if present): [path] ...` under CONTEXT FILES (`roadmap/SKILL.md:611-613`), while task-builder's resolver looks for a `SPEC:`/`PRD:`/`TDD:` field (`task-builder/SKILL.md:41`). If it does not resolve, the phase file says `reflect_pre: verdict: skipped`, and only then is a manual 2.10 run warranted. The corrected text above handles both outcomes because it tells the reader to look at `reflect_pre`.

### R5 [IMPORTANT] 2.2 step 3 (guide L46): omission that disables the built-in check and drives the user to the redundant manual one

- **Quoted:** "`/task-builder \"Implement <feature> as described in <path to spec or research report>\"`. Read the task file it produces and confirm it matches the spec."
- **Problem:** a plain path in quotes is not `--spec` and not an `@file`, so the PRE gate records `skipped (no-spec)` (F2) and the spec-coverage audit the user is then told to do by eye (or by hand via 2.10) never runs automatically.
- **Corrected text:** "3. **Build the task file.** `/task-builder \"Implement <feature> as described in the spec\" --spec <path to spec>`. Passing `--spec` makes task-builder check the task file against the spec for you. Read the task file, confirm it matches what was agreed, and check its `reflect_pre` verdict is PASS."

### R6 [MINOR] 2.4 step 3, second bullet (guide L62)

- **Quoted:** "Fix spread across several files: run `/sc:troubleshoot` again with `--fix`."
- **Already done by:** nothing reuses the first diagnosis; `--fix` re-runs the whole diagnosis (F10, `commands/troubleshoot.md:191`). The source sanctions this, so it is not wrong, but it repeats a 1-3 minute (or deep, multi-agent) run. `--fix` changes nothing without your acceptance (`commands/troubleshoot.md:54`), so it is safe on the first run.
- **Corrected text:** add to step 1: "If the fix may span several files, add `--fix` now; it only offers a task file after the diagnosis and changes nothing unless you accept." Then step 3 bullet 2 becomes: "Fix spread across several files: accept the task-file offer from step 1 (if you did not pass `--fix`, re-run with it), then `/task <path>`."

### R7 [MINOR] 2.3 step 3 (guide L54), the "run the tests" half

- **Quoted:** "**Before committing:** run the tests and `/code-review`."
- **Already done by:** on the `--handoff implement` path `/sc:implement` Q6 already detected and ran the tests after each task (F12); `/sc:task` STANDARD and STRICT already ran them (F13). Only `/sc:task` LIGHT/EXEMPT and a plain "ask Claude" edit leave tests unrun.
- **`/code-review` half: complementary, keep.** `/sc:implement` reviews spec compliance, not bugs (F12).
- **Corrected text:** "3. **Before committing:** run `/code-review`. Also run the tests if nothing ran them yet (a plain edit, or `/sc:task` reported LIGHT or EXEMPT)."

## Findings: wording and consequence defects caused by the same misunderstanding

### W1 [MINOR] 2.1 step 8 (guide L35)

- **Quoted:** "`/task <path to the phase's task file>`. Finish and verify each phase before starting the next."
- **Problem:** "verify" invites a manual verification pass that `/task` already performs (phase-gate QA, post-completion validation, tests, POST reflect: F5, F3).
- **Corrected text:** "8. **Build one phase at a time.** `/task <path to the phase's task file>`. Let it finish (it runs its own reviews, tests, and plan-versus-build check) and confirm its `reflect_post` verdict is PASS before starting the next phase."

### W2 [MINOR] Section 4 "surprising defaults" row for `/sc:reflect --mode post` (guide L151) and 2.12 first row (guide L125)

- **Quoted:** "`/sc:reflect --mode post` | Moves your finished work folder to a \"done\" location | Add `--no-promote`" and "Task files live under `.dev/tasks/to-do/`."
- **Problem:** once R1-R3 are fixed, the user never runs reflect post by hand; the run inside `/task` promotes by default (F4), so a finished task file moves to `.dev/tasks/done/`. The row as written implies the user controls this with a flag they will no longer type, and 2.12 does not mention where finished task files go.
- **Corrected text (row):** "`/sc:reflect --mode post` | Moves the finished work folder to a \"done\" location. The check that runs inside every `/task` run does this on a pass: the task folder moves from `.dev/tasks/to-do/` to `.dev/tasks/done/`. | Expected. Add `--no-promote` only when you run `/sc:reflect` yourself."
- **Corrected text (2.12):** append "Unfinished task files stay under `.dev/tasks/to-do/`; finished ones move to `.dev/tasks/done/`."

### W3 [MINOR] 2.1 steps 3 and 5 (guide L30, L32): description overlaps the built-in QA

- **Quoted:** "A panel of expert reviewers lists gaps and contradictions."
- **Problem:** `/prd` and `/tdd` already ran internal QA including an internal-consistency/contradiction check (F7). The step itself is NOT redundant (see K1), but the description sells it as the thing the skill already did.
- **Corrected text (step 3):** "**Review the PRD.** `/prd` already checked its own evidence and consistency. For an outside expert critique of requirement quality (measurable acceptance criteria, testability, missing scenarios), run `/sc:spec-panel @<path to PRD> --mode critique --focus requirements`. Fix what it finds before moving on." Step 5 analogously with "architecture and testing design" and `--focus architecture,testing`.

## Checked and complementary (keep, with evidence)

| # | Guide location | Suspected overlap | Why it is NOT redundant | Evidence |
|---|---|---|---|---|
| K1 | 2.1 steps 3, 5 (`/sc:spec-panel`) | `/prd` and `/tdd` have their own QA | No skill invokes spec-panel; built-in QA is evidence, structure, and consistency (rf-qa, rf-qa-qualitative), while spec-panel is a named-expert critique of requirement and design quality (Wiegers testability, Adzic examples, Nygard failure modes). Keep; fix wording per W3. | F7; `commands/spec-panel.md:25`, `:51-60` |
| K2 | 2.1 step 4, 2.2 step 2 | User told to write a TDD / design, then build a task file | `/prd`, `/tdd` internally use rf-task-builder plus `/task` only to produce the document (F7). The guide never tells the user to run task-builder for them, so no duplication. | F7 |
| K3 | Level 5 row, 2.5 (`/tech-research` then `/task-builder`) | tech-research already uses task-builder and task | Those internal runs produce the research report only; tech-research never builds the implementation task file (F9). Passing the report to `/task-builder` is the necessary next step. Optional improvement: pass the report with `--spec` so task-builder's PRE gate audits coverage of the recommended plan (F2). | F9; `tech-research/SKILL.md:573` |
| K4 | 2.1 step 7 (`/roadmap`) | Guide might add manual fidelity/coverage/validation | The guide adds none; it correctly states roadmap produces per-phase task files (F8). No change. 2.1 step 6 `/sc:release-split` is not performed by roadmap (grep: 0 hits in roadmap SKILL.md), so it is complementary. | F8 |
| K5 | Level 3 row, 2.3 step 2 (`/sc:workflow` then `/sc:implement`; `--handoff implement`) | Running `/sc:implement` after `--handoff implement` | The guide never does both. Level 3 uses default handoff `none` (prints the next step only) then runs `/sc:implement` once; 2.3 uses `--handoff implement` alone. Both are single invocations. | F11 |
| K6 | 2.11 steps 1-4 vs step 6 (`/sc:pr-submit --monitor 1`) | pr-submit already reviews | At L1 pr-submit runs none of `/code-review`, `/security-review`, `/sc:auggie-review`, and does not run its test validator (L2+ only); its CI wait happens after the PR is opened. Steps 1-4 are pre-push local gates. Step 1 (full suite across the branch) is broader than `/task`'s per-task "relevant" suite, so keep. Step 5 "Push" is needed: pr-submit never pushes the branch. | F14; F5 (`task/SKILL.md:297` "relevant test suite") |
| K7 | 2.11 steps 2 and 4 (`/code-review` and `/sc:auggie-review`) | Both look for bugs | Partial overlap on narrow bugs, but different engines and auggie-review adds architecture and anti-pattern lenses. Keep. Unverified (flag): whether the local `/sc:auggie-review` branch pass and the Augment Code PR bot in step 6 are effectively the same review engine on the same diff; if they are, step 4 would be optional when step 6 follows immediately. Not confirmed from source. | F14; `skills/sc-pr-submit-protocol/SKILL.md:19-23` |

## Source-side inconsistency (not a guide edit; report to IronClaude maintainers)

| # | Location | Problem | Recommended source fix |
|---|---|---|---|
| S1 | `commands/reflect.md:275` | "After `/task` completes: The operator re-runs `/sc:reflect --mode post --diff <new-diff>` as the post-commit gate." The remediation task file it refers to is built by task-builder and therefore already carries the POST reflect item (F3). This line is the likely source of the guide's R1-R3 error. | Reword to: "After `/task` completes: the task file's own POST reflect item has already run; check its `reflect_post` verdict." |
| S2 | `skills/sc-troubleshoot-protocol/SKILL.md:560`, `:605`; `commands/troubleshoot.md:54`, `:77` | Tier 3 Phase D runs a post-execution reflect/validate on a task-builder task file that already ran POST reflect inside `/task` (F3). Duplicate audit inside the source chain. | Make Phase D read the task file's `reflect_post` verdict instead of re-auditing, or document why the second pass is intended. |

## Items Reviewed (the checks the orchestrator required)

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Does task-builder run PRE reflect itself when a spec is given? (2.10, 2.2) | YES, mandatory. 2.10 redundant for task-builder files; 2.2 omits `--spec` so the built-in gate is skipped | F1, F2; R4, R5 |
| 2 | Does every task-builder task file include POST reflect, and does `/task` run it? (2.1 s9, 2.2 s5, 2.4 s4) | YES and YES. All three manual runs redundant | F3, F5; R1, R2, R3 |
| 3 | Do `/prd` and `/tdd` include their own QA, making spec-panel redundant? Do they use task-builder plus task? | Own QA yes; use rf-task-builder plus `/task` yes; spec-panel NOT redundant (different reviewer type) | F7; K1, K2, W3 |
| 4 | Does `/roadmap` deep run task-builder per phase, validate task files, and check fidelity/coverage? | YES to all. Guide adds no manual duplicate except via 2.1 s9 and 2.10 | F8; K4, R1, R4 |
| 5 | Does `/tech-research` run task-builder and task; is "pass its report to /task-builder" duplicate? | Runs both for the report only; handoff is NOT duplicate | F9; K3 |
| 6 | Does `/sc:troubleshoot --fix` chain task-builder, reflect pre, and require `/task` plus reflect post? | YES (Phases A-D). 2.4 s4 redundant on the fix path; re-run with `--fix` repeats diagnosis | F10; R3, R6, S2 |
| 7 | Does `/sc:workflow --handoff implement` run `/sc:implement`; does `/sc:implement` run tests/review? | YES; per-task spec review plus Q6 tests plus whole-list review. No double invocation in guide; 2.3 s3 tests half redundant | F11, F12; K5, R7 |
| 8 | Does `/task` run tests or code review? | Runs the relevant test suite (code tasks) plus 6+ agent QA per phase; no bug-focused code review | F5, F6; R1, R2, R7, K6 |
| 9 | Does `/sc:pr-submit` run reviews that 2.11 s2-4 duplicate? | NO at `--monitor 1` | F14; K6, K7 |
| 10 | Anything else in the guide | 2.1 s8 wording, Section 4 promote row and 2.12 location note, spec-panel description, source-side S1/S2 | W1, W2, W3, S1, S2 |

## Summary

- Checks where the guide is fully correct: 2 / 10 (checks 5 and 9). Check 7 is partly correct (no double invocation, but the R7 tests half is redundant). Checks with a defect: 1, 2, 3 (wording only), 4, 6, 7 (partial), 8, 10.
- Genuinely redundant steps: 7 (R1-R7). Critical: 1. Important: 4. Minor: 2.
- Wording/consequence defects: 3 (W1-W3, all minor).
- Complementary, keep: 7 (K1-K7), two with an explicitly unverified sub-point (R4 roadmap PRE-gate firing, K7 Augment engine identity).
- Source-side issues for IronClaude maintainers: 2 (S1, S2).
- Issues fixed in place: 0 (report-only; guide not edited, per instruction).

## Explicit removals proposed (each needs user adjudication)

- Remove from 2.1 step 9: "Run the tests, then `/sc:reflect --mode post --diff <commit or branch> --no-promote`". Why: `/task` already ran both (R1).
- Remove from 2.2 step 5: "Tests, then `/sc:reflect --mode post --diff <commit or branch> --no-promote`". Why: same (R2).
- Remove from 2.4 step 4 (task-file path only): "`/sc:reflect --mode post --diff <commit or branch> --no-promote`". Why: `/task` plus troubleshoot Phase D already audit it (R3).
- Remove from 2.10 the instruction to run PRE reflect on task files built by `/task-builder` with `--spec` or by `/roadmap`. Why: built in (R4). Keep it for `/sc:workflow` and hand-written plans.
- Remove from 2.3 step 3 the unconditional "run the tests". Why: already run on the implement and STANDARD/STRICT paths (R7). Keep it conditionally.

## Confidence Gate

- **Confidence:** Verified: 10/10 | Unverifiable: 0 (two sub-points inside items 4 and 9 are explicitly flagged Unverified in R4 and K7 and do not change those items' verdicts) | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 1 | Grep: 0 (content search done through Bash grep, 20 calls) | Glob: 0 | Bash: 22 | Write: 1 | Edit: 3. No web research performed (tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0).
- **Source pin:** cites valid on `origin/master` @ 50a8c7f4; only `skills/sc-reflect-protocol/SKILL.md` differs from the working tree (L224-235 alias table, no cited line affected).

## QA Complete
