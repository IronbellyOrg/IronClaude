# QA Report: Final Fix-Cycle, Part 2 (workflows 3.5-3.12, sections 4 and 5)

**Topic:** IronClaude new-user guide, final adversarial QA, all lenses (accuracy, redundancy, workflow completeness)
**Date:** 2026-10-01
**Phase:** fix-cycle (final)
**Guide:** `IRONCLAUDE-NEW-USER-GUIDE.md` (L133-242 in scope). Not edited.
**Source truth:** `/Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/` (cited as `SRC/`)
**Author decision respected:** `--spec` is only for a spec, PRD, or TDD (`SRC/skills/task-builder/SKILL.md:41`).

---

## Overall Verdict: FAIL

5 issues, all MINOR (0 CRITICAL, 0 IMPORTANT). 6 of the 7 prior findings in scope are resolved; Error 6 has one line left (Issue 1).

## Part 1: Prior findings in scope

| Prior finding | Status | New guide text (quoted) | Evidence |
|---|---|---|---|
| 14 N2 (3.10 sorts by "was `--spec` typed") | RESOLVED | L183: "For a task file, open it and read the `reflect_pre` entry at the top. That entry, not how the file was built, tells you whether the check already ran." L185-186 branch on `verdict: pass`/`fail` vs `verdict: skipped` | `SRC/skills/task-builder/SKILL.md:1666` (skipped only when no spec resolves), `:1689-1698` (verdict values). The author did not adopt the prior "troubleshoot already checked it" clause, which is correct: troubleshoot's Phase B runs `/sc:reflect --type task --analyze` with no spec (`SRC/skills/sc-troubleshoot-protocol/SKILL.md:558`), and `--mode pre` with no `--spec` is a STOP (`SRC/commands/reflect.md:32`). |
| 15 Error 6 ("reviewers check every phase") | NOT RESOLVED (one line left) | Fixed at L16, L77, L229 ("except the first (setup) one"). Still wrong at L230: "has a panel of reviewers check each group of items." | `SRC/skills/task/SKILL.md:188`: "mandatory for every phase except Phase 1 (which is setup-only ...)". See Issue 1. |
| 15 N1 (passed folder moves to `done/` inside `/task`) | RESOLVED | L205: "Task files live under `.dev/tasks/to-do/` (and under `.dev/tasks/done/` once someone has moved them there)." L239: "When you run it yourself on finished work and the audit passes, it moves the work folder to a \"done\" location. (The audit inside `/task` never moves anything.)" (L79, outside this scope, also fixed.) | Promotion needs `tasklist_completion_pct == 1.0` and `status: done` (`SRC/skills/sc-reflect-protocol/SKILL.md:1519`, `:1523`); the POST item runs before Update-status-to-Done (`SRC/skills/task-builder/SKILL.md:2311`). The CLI-mode wrapper passes `--promote` (`:2237`) but still goes through reflect's gated Wave 7 (`SRC/cli/reflect/commands.py:233`), so "never" holds. |
| 15 N6 (`/sc:improve` auto-fix list) | RESOLVED | L161: "`/sc:improve` fixes formatting and naming, removes unused variables, reorders imports, and adds simple type annotations." | `SRC/commands/improve.md:110-115` lists exactly these four. (The `/sc:cleanup` half of the same sentence is incomplete; see Issue 2.) |
| 15 N8 (roadmap task files may carry `skipped`) | RESOLVED | L186: "`verdict: skipped` (no spec was found when it was built, which can happen with task files made from roadmap build requests or from a research or troubleshoot report)" | Hedged with "can happen", which matches the unverified BUILD_REQUEST spec resolution (`SRC/skills/task-builder/SKILL.md:41`; roadmap BR lists PRD/TDD only as CONTEXT FILES bullets). |
| 16 N3 (roadmap task files claimed checked; no `skipped` branch) | RESOLVED (3.10 part in scope) | 3.10 now has a `skipped` branch (L186-188). | Same evidence as 14 N2. |
| 16 N8 (section 5 tells `/roadmap` users to narrow) | RESOLVED | L242 (verified line): "For `/tech-research`, ask a narrow, specific question if you want a smaller run. For `/roadmap`, keep the full setting if you want a task file for every phase (3.1 step 7)." | `SRC/skills/roadmap/SKILL.md:102-114`: only Deep creates task files; "If in doubt, pick Deep". |

## Part 2: Issues Found

| # | Severity | Lens | Location | Issue |
|---|---|---|---|---|
| 1 | MINOR | Accuracy | Section 5, L230 | Last leftover of Error 6: "check each group of items" omits the setup-group exception |
| 2 | MINOR | Accuracy | 3.7 step 2, L161 | `/sc:cleanup` auto-fix list omits two of its four automatic changes |
| 3 | MINOR | Workflow | 3.9, L177-178 | `/operational-guide` and `/readme` requests omit the output path, which both skills list as mandatory |
| 4 | MINOR | Workflow | 3.12, L206 | Resume table has no row for `/readme` or `/operational-guide`, both introduced in 3.9 |
| 5 | MINOR | Workflow | 3.10, L188 | "Fix the plan, then build." is wrong for a task file, which is already built |

### Issue 1: section 5 still says reviewers check every group

- **Quoted (L230):** "The second pair researches the code, writes a full task file, and has a panel of reviewers check each group of items."
- **Evidence:** `SRC/skills/task/SKILL.md:188`: "QA verification is mandatory for every phase except Phase 1 (which is setup-only ...)". The row directly above (L229) already says "except the first (setup) one", so the two adjacent rows disagree.
- **Replacement:** "The second pair researches the code, writes a full task file, and has a panel of reviewers check each group of items after the setup group."

### Issue 2: incomplete `/sc:cleanup` auto-fix list

- **Quoted (L161):** "`/sc:cleanup` removes unused imports and code nothing references;"
- **Evidence:** `SRC/commands/cleanup.md` "AUTO-FIX VS APPROVAL-REQUIRED", Auto-fix (applies automatically): "Unused imports removal", "Dead code with zero references", "Empty blocks removal", "Redundant type annotations". The guide lists 2 of 4. The `/sc:improve` half lists all 4 of its items (`SRC/commands/improve.md:110-115`), so the sentence is inconsistent.
- **Replacement:** "`/sc:cleanup` removes unused imports, code nothing references, empty blocks, and redundant type annotations;"

### Issue 3: two documentation requests omit the output path

- **Quoted (L177):** "`/operational-guide \"Write the operational guide for deploying the billing worker ... Audience: on-call engineers.\"`" (no output path)
- **Quoted (L178):** "`/readme \"Write the README for the src/billing/ package: ... Audience: new engineers.\"`" (no output path)
- **Evidence:** `SRC/skills/operational-guide/SKILL.md:61`: "2. **WHERE to write it** (mandatory) ... The output location." `SRC/skills/readme/SKILL.md:61`: "2. **WHERE to write it** (mandatory) ... The README.md output location." Both skills fall back to project convention (`operational-guide/SKILL.md:98`, `readme/SKILL.md:102`), so this does not block, but the operational-guide convention is `docs/docs-product/ops/[name]-operational-guide.md` (`:61`), a folder this project may not use. The tech-reference row (L176) already includes "Output: ...", so the three rows are inconsistent. The readme skill also treats an existing technical reference as primary input (`readme/SKILL.md:8`, `:59`); the example does not mention it.
- **Replacement (L177):** "`/operational-guide \"Write the operational guide for deploying the billing worker to staging and production, including rollback. Sources: deploy/worker.yaml, scripts/deploy_worker.sh. Audience: on-call engineers. Output: docs/billing/billing-worker-deploy-operational-guide.md.\"`"
- **Replacement (L178):** "`/readme \"Write the README for the src/billing/ package: what it does, setup, configuration, and how to run its tests. Use docs/billing/billing-technical-reference.md if it exists. Audience: new engineers. Output: src/billing/README.md.\"`"

### Issue 4: no resume instruction for `/readme` and `/operational-guide`

- **Quoted (L206):** "| A research, document, or roadmap skill (`/tech-research`, `/prd`, `/tdd`, `/tech-reference`, `/roadmap`) | Run the same command with the same request again. It finds its folder under `.dev/tasks/to-do/` and continues from the first unchecked item. |"
- **Evidence:** `/readme` resumes the same way: "If a task file already exists for this module (from a previous session), skip Stage A and invoke `/task` ... to resume" (`SRC/skills/readme/SKILL.md:194`, `:206`). `/operational-guide` has no "already exists, resume" step: "Each invocation creates a self-contained folder under `.dev/tasks/to-do/`" (`SRC/skills/operational-guide/SKILL.md:136`); `:158` only says to read prior research and build on it. Re-running it may start a new folder and repeat the research. A user who ran either skill from 3.9 finds no matching row.
- **Replacement (L206):** add `/readme` to the skill list, and add a row: "| An operational guide (`/operational-guide`) | Do not run it again; it starts a new folder. Find its task file under `.dev/tasks/to-do/TASK-OPSGUIDE-<subject>-<timestamp>/` and run `/task <path to that task file>`. |"

### Issue 5: "then build" after fixing an already-built task file

- **Quoted (L188):** "The report in `.dev/reflect/pre-<name>-<timestamp>/` lists every requirement the plan misses. Fix the plan, then build."
- **Problem:** The `skipped` bullet covers task files as well as plans. A task file is already built; "build" can read as "run `/task-builder` again", which repeats the research and the build. Output path itself is correct (`SRC/commands/reflect.md:92`: default `.dev/reflect/<mode>-<slug>-<ts>/`).
- **Replacement:** "Add the missing requirements to the plan or task file, then run it (`/task <path>` for a task file, `/sc:implement @<plan.md>` for a plan)."

## Part 3: Claims re-verified and passing (no change needed)

| Guide claim (location) | Result | Source evidence |
|---|---|---|
| `/sc:research "..." --depth deep` searches the web (3.5) | PASS | `SRC/commands/research.md:3` "Deep web research", `:25` `--depth quick\|standard\|deep\|exhaustive`. Note: it saves to `claudedocs/research_*.md` (`:104`), not `.dev/`; not stated by the guide, not wrong. |
| `/sc:analyze src/billing/ --focus security` (or quality, performance, architecture), reports only (3.5) | PASS | `SRC/commands/analyze.md:22`; Will Not "Modify source code or apply fixes without explicit user consent" (`:100`) |
| `/sc:explain src/billing/invoice_job.py` (3.5) | PASS | `SRC/commands/explain.md:22` `[target]` |
| `/sc:adversarial --compare a.md,b.md`, debate, score, merge (3.6) | PASS | `SRC/commands/adversarial.md:15`, `:23`, `:39` (2-10 files) |
| `/sc:spec-panel @file --mode critique`, only reports (3.6) | PASS | `SRC/commands/spec-panel.md:22`, `:119`; Will Not "Modify specifications without explicit user consent" (`:451`) |
| `/sc:swarm-wizard` dry run first, go-ahead, proxy for real runs (3.6) | PASS | `SRC/commands/swarm-wizard.md:32-33`, `:52`, `:82-87` |
| `/sc:business-panel @docs/...` (3.6) | PASS | `SRC/commands/business-panel.md:50` `[document_path_or_content]` |
| `/sc:cleanup-audit src/billing/ --pass all`, `.claude-audit/`, bare = Pass 1 only, changes nothing (3.7) | PASS | `SRC/commands/cleanup-audit.md:31`, `:37`, `:43`, `:53`, `:112` |
| `/sc:cleanup ... --type code --safe --interactive`; `/sc:improve ... --type quality --safe --interactive` (3.7) | PASS (flags) | `SRC/commands/cleanup.md:22`; `SRC/commands/improve.md:22`. Auto-fix list for cleanup: Issue 2. |
| "refactor" in a `/sc:task` request switches to strict (3.7) | PASS | `SRC/skills/sc-task-protocol/SKILL.md:60`, `SRC/commands/task.md:74` |
| `/task-builder ... --spec` for large refactors, only with a written spec (3.7) | PASS | Respects author decision; `SRC/skills/task-builder/SKILL.md:41` |
| `/sc:test tests/billing/ --coverage`, `--type unit\|integration\|e2e`, does not write tests (3.8) | PASS | `SRC/commands/test.md:22`; Will Not "Generate test cases" |
| `/tech-reference` request with code, audience, output (3.9) | PASS | `SRC/skills/tech-reference/SKILL.md:47` |
| `/sc:document src/api/routes/invoices.py --type api` (3.9) | PASS | `SRC/commands/document.md:22`, `:67` |
| 3.10 `reflect_pre` verdict logic, `/sc:reflect --mode pre --spec --tasklist`, report under `.dev/reflect/pre-<name>-<timestamp>/` | PASS (wording: Issue 5) | `SRC/skills/task-builder/SKILL.md:1666`, `:1683-1698`; `SRC/commands/reflect.md:27`, `:92` |
| `/sc:auggie-review --diff origin/main...HEAD --no-post-pr`, local only, remediation offer at end (3.11) | PASS | `SRC/commands/auggie-review.md:8`, `:28`, `:51-52`, `:160` (offer always needs confirmation) |
| `/sc:pr-submit --monitor 1 --head --title --body`, needs `gh`, proposes without edits (3.11) | PASS | `SRC/commands/pr-submit.md:8`, `:29-31` (gh checks), `:37` "arm + poll + propose (no edits)", `:85` "apply edits at L1" is a Will Not |
| 3.12 `/task` resume from first unchecked item | PASS | `SRC/skills/task/SKILL.md` F1 loop; doc skills `tech-research/SKILL.md:173`, `prd/SKILL.md:168`, `tdd/SKILL.md:149`, `tech-reference/SKILL.md:183`, `roadmap/SKILL.md:181` |
| 3.12 `/sc:implement @.dev/workflow/<name>/plan.md --resume` | PASS | `SRC/commands/implement.md:6`, `:57`; `SRC/commands/workflow.md:41`, `:67` |
| 3.12 brainstorm `--resume-from .dev/brainstorms/<timestamp>-<name>/seed-brief.md` | PASS | `SRC/commands/brainstorm.md:40`, `:61`, `:63`, `:192` |
| 3.12 pr-submit `--resume .dev/pr-monitor/pr-<N>-<timestamp>/monitor-run-<N>.jsonl` | PASS | `SRC/commands/pr-submit.md:40`, `:55-56` |
| 3.12 crash-recovery prompt with `--since 24h` | PASS | `SRC/skills/sc-crash-recovery/SKILL.md:26` |
| Section 4 rules | PASS | No source claim except `/sc:recommend "<goal>"`: `SRC/commands/recommend.md:8`, `:24` |
| Section 5: `/task` vs `/sc:task`; workflow+implement one reviewer per step | PASS (L229); L230 Issue 1 | `SRC/skills/task/SKILL.md:188`; `SRC/skills/sc-implement-protocol/SKILL.md:89`, `:112` |
| Section 5: `/roadmap` vs `/sc:roadmap` (`/sc:tasklist`, `superclaude sprint run`) | PASS | `SRC/commands/tasklist.md:18`, `:23` |
| Section 5: `/sc:design` single pass vs `/tdd` | PASS | `SRC/commands/design.md:22` |
| Section 5 defaults: promote, auggie posts on PR, pr-submit default `--monitor 2` edits and 3 pushes, deep default for tech-research/roadmap | PASS | `SRC/commands/reflect.md:103`; `SRC/commands/auggie-review.md:50`; `SRC/commands/pr-submit.md:26`, `:38-39`, `:47`; `SRC/skills/tech-research/SKILL.md:97`; `SRC/skills/roadmap/SKILL.md:102` |

### Redundancy lens (steps that repeat a skill's internal work)

- None found in scope beyond Issue 5's re-build risk. 3.10 now says "Do not run the check again" for pass/fail (L185). 3.11 `/code-review` (bugs) and `/sc:auggie-review` (architecture, patterns) are distinct reviewers; the guide's own `/task` audit is not re-run. Rule L217 ("Do not repeat a skill's own checks") is consistent with every step in scope.

## Removals to adjudicate

- None proposed by this review.

## Confidence Gate

- **Confidence:** Verified: 34/34 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (one residual uncertainty, not a checklist item: whether roadmap BUILD_REQUEST CONTEXT bullets resolve as a spec; the guide hedges it correctly with "can happen").
- **Tool engagement:** Read: 0 | Grep: 0 (all content searches ran through Bash grep/sed) | Glob: 0 | Bash: 22 | Write: 1 | Edit: 3 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
- **Retry monotonicity:** prior in-scope open findings |F|=7 (14 N2, 15 Error 6/N1/N6/N8, 16 N3/N8); now |F|=5, strictly fewer. No item that passed before regressed (Error 6 is a carry-over, not a regression).

## Summary

- Prior findings in scope: 6 of 7 resolved; Error 6 has one line left (L230).
- New issues: 5, all MINOR. Fix all 5 with the replacement text above; no structural change needed.
- Guide not edited (report-only).

## QA Complete
