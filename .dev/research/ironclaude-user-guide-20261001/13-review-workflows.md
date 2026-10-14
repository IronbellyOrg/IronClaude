# QA Report: Workflow Sequencing and Completeness Review (IronClaude New User Guide)

**Topic:** `IRONCLAUDE-NEW-USER-GUIDE.md` sections 1 (levels table) and 2.1-2.12, plus sections 3-4 where they affect workflows
**Date:** 2026-10-01
**Phase:** report-validation (adversarial, lens = workflow sequencing + completeness; report-only, guide NOT edited)
**Fix cycle:** N/A
**Source truth:** IronClaude master `/Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/` (abbreviated `MS/` below)
**Supporting research:** `02-planning-depth-ladder.md`, `03-quality-debug-review.md` (same folder)

---

## Overall Verdict: FAIL

The skill order is right in the main chains (brainstorm, then PRD, then TDD, then roadmap, then task). But the guide drops steps newcomers need: the roadmap tier caveat, what to do when a gate halts, the `--spec` hand-off, regression tests, and resume paths for the document skills. It also tells users to rerun a reflect audit that every task file already runs, and relies on a `--preview` flag that is not in the cleanup/improve syntax. Most example prompts are bare placeholders, even though the source skills document what a strong request looks like.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Main chain order brainstorm -> prd -> tdd -> roadmap -> task (2.1) | PASS | `MS/skills/roadmap/SKILL.md:12` ("fills the gap between upstream document skills (/prd, /tdd) and downstream execution (/task)"); prd -> tdd feed per 02 research Part 2 §3 |
| 2 | Does /roadmap need /task-builder separately | PARTIAL FAIL | Deep tier runs /task-builder per phase itself; Standard and Quick do NOT (`MS/skills/roadmap/SKILL.md:100-104`). Guide does not say this. See F1 |
| 3 | spec-panel `--downstream roadmap` placement | PASS (correctly omitted from 2.1) | It emits a `release-spec-template.md` spec for the `/sc:roadmap` sprint lane (`MS/commands/spec-panel.md:272, 280`); the RF `/roadmap` reads PRD+TDD directly (`MS/skills/roadmap/SKILL.md:58`) |
| 4 | release-split placement | FAIL | Placed correctly before roadmap, but input and what to do with its output are missing. See F9 |
| 5 | Redundant or wrong steps | FAIL | Manual POST reflect after `/task` duplicates the built-in gate (F3); 2.10 duplicates the task-builder PRE gate (F8) |
| 6 | Missing newcomer steps (inputs, output locations, gate failure) | FAIL | F1, F4, F5, F6, F7, F10, F13, F18, F19 |
| 7 | Right tool for the job (design vs tdd, document vs tech-reference, workflow vs task-builder) | PARTIAL FAIL | Choices are defensible, but the boundaries the user asked about are not explained in section 4. See F21 |
| 8 | Prompt concreteness | FAIL | F2, F10, F12, F17, F23 |
| 9 | Jargon | FAIL | F22 |
| 10 | Section 4 defaults table accuracy | PASS | `--no-promote` (`MS/commands/reflect.md:103`), `--post-pr` default true on PR (`MS/commands/auggie-review.md:50`), `--monitor` default 2 (`MS/commands/pr-submit.md:47`) |
| 11 | Flag/syntax accuracy of workflow invocations | PARTIAL FAIL | All checked flags exist except `--preview` on cleanup/improve, which appears only in examples, not usage syntax (F16) |
| 12 | Levels table internal consistency | FAIL | Hard-limit sentence contradicts the cited project rule (F20) |

## Findings

### F1 (IMPORTANT): 2.1 step 7, /roadmap does not always produce task files

- **Quoted:** "`/roadmap "Create a roadmap from <path to PRD> and <path to TDD>"`. For large work this produces the roadmap document, a build request for each phase, and a ready-to-run task file for each phase."
- **Problem:** The tier decides what you get. Quick gives the roadmap document only. Standard gives the roadmap plus build requests but no task files. Only Deep (the default) creates one task file per phase. A newcomer whose run lands on Standard reaches step 8 with no task file to run. The guide also never says where the roadmap and task files land, or that the roadmap should be read before any phase runs. A dry-run option exists for exactly that review.
- **Evidence:** `MS/skills/roadmap/SKILL.md:96-104` (tier table, "Default to Deep"); `:135-143` (output locations: `.dev/tasks/to-do/TASK-ROADMAP-<subject>-<timestamp>/ROADMAP-<NAME>.md`, `build-requests/BUILD_REQUEST-phase-NN-<name>.md`, phase task files in `.dev/tasks/to-do/TASK-*/`); `:247, :2614-2644` (dry run); `:671` (final summary lists phase task files and the `/task` command).
- **Replacement:**
  > 7. **Turn the PRD and TDD into a phased plan.** Run `/roadmap` with the document paths, the reason for the work, and a project name, for example: `/roadmap "Create a full roadmap from docs/billing/PRD_BILLING.md and docs/billing/TDD_BILLING.md. Each phase must be independently deployable and keep the old invoice API working. Project name: billing-v2. Dry run first so I can review the phase plan."` The dry run shows the proposed phases and waits for you to say yes. When it finishes, it prints the roadmap path (`.dev/tasks/to-do/TASK-ROADMAP-billing-v2-<timestamp>/ROADMAP-BILLING_V2.md`) and the list of phase task files in run order. Read the roadmap before you run anything.
  > - If the summary lists build-request files (`build-requests/BUILD_REQUEST-phase-NN-<name>.md`) but no task files, the run used its middle setting. Create each phase's task file with `/task-builder <path to that BUILD_REQUEST file>` before step 8. Saying "full roadmap" or "comprehensive" in the request avoids this.

### F2 (IMPORTANT): 2.1 step 7 and level-6 row, the roadmap prompt lacks the inputs the skill asks for

- **Quoted:** "`/roadmap "Create a roadmap from <path to PRD> and <path to TDD>"`"
- **Problem:** The roadmap skill names four inputs: what to build, why plus constraints, source paths, and a project name. It also says it will stop and ask for clarification when the request is thin. The guide's prompt supplies only paths.
- **Evidence:** `MS/skills/roadmap/SKILL.md:54-68` (four inputs, "WHY ... strongly recommended"); `:70-77` (strong prompt examples); `:86-98` (asks to clarify when incomplete).
- **Replacement:** covered by the F1 replacement example.

### F3 (IMPORTANT): 2.1 step 9 and 2.2 step 5, the manual POST reflect duplicates a gate every task file already runs

- **Quoted (2.1 step 9):** "Run the tests, then `/sc:reflect --mode post --diff <commit or branch> --no-promote`, which independently checks that what was built matches what was planned."
- **Quoted (2.2 step 5):** "Tests, then `/sc:reflect --mode post --diff <commit or branch> --no-promote`, then workflow 2.11."
- **Problem:** Every task file built by `/task-builder` (including the phase task files `/roadmap` creates) has a POST reflect item placed second to last, and it must run before the task can be marked Done. Rerunning it by hand repeats a multi-reviewer audit. The hand-run version has no `--tasklist` or `--spec`, so it has less to compare against than the built-in one. `/task` also already requires tests to pass for code-changing tasks. A newcomer cannot tell whether to trust the built-in verdict or the manual one.
- **Evidence:** `MS/skills/task-builder/SKILL.md:1077` (`POST_REFLECT_GATE: ENABLED` in every build request); `:2310, :2371` (POST item mandatory, second to last, before Update-status-to-Done); `MS/skills/task/SKILL.md:297` (tests must pass for code-modifying tasks); `MS/commands/reflect.md:83-84` (`--spec` recommended and `--tasklist` "Strongly recommended for UC-2").
- **Replacement (2.1 step 9):**
  > 9. **Check each phase's audit.** The last items of every task file run the tests and an independent audit (`/sc:reflect --mode post`) comparing what was built with the plan. When `/task` finishes, open the task file and read the `reflect_post` entry at the top (verdict and report path). If the verdict lists Drift or Regression items that were not fixed, resolve them before starting the next phase. Run `/sc:reflect` by hand only for work done outside a task file (see 2.3 and 2.4).
- **Replacement (2.2 step 5):**
  > 5. **Verify.** Read the task file's `reflect_post` verdict and report (see 2.1 step 9), then follow workflow 2.11.

### F4 (IMPORTANT): 2.1 step 8, 2.2 step 4, and level 4, nothing says what to do when /task stops

- **Quoted:** "`/task <path to the phase's task file>`. Finish and verify each phase before starting the next." / "**Run it.** `/task <path to task file>`."
- **Problem:** `/task` is allowed to stop in three cases: a phase's quality check fails 3 fix rounds, every remaining item is blocked by the same issue, or an item's result invalidates the rest of the file. When it stops, it logs the findings in the Task Log and asks the user. A newcomer gets no instruction. Section 3's "Never turn off a quality check" says what not to do, but not what to do.
- **Evidence:** `MS/skills/task/SKILL.md:120` (only three permitted halts); `:180` (status set to Blocked with a reason); `:254, :368` (after 3 failed fix cycles: HALT, log in Task Log, present findings, ask for guidance; do not continue without user approval).
- **Replacement (add after 2.1 step 8 and 2.2 step 4):**
  > If `/task` stops, it shows the reviewers' findings and writes them to the Task Log at the bottom of the task file. The file's `status` may say Blocked, with a `blocker_reason`. Read them, decide the fix with your lead (change the code, correct the spec, or amend the task item), then run the same `/task <path>` command again. It continues from the first unchecked item. Do not tick items by hand to get past a stop.

### F5 (IMPORTANT): level 3 and 2.3 step 2, nothing says what to do when /sc:implement halts on a failed step

- **Quoted:** "Then `/sc:implement @.dev/workflow/<name>/plan.md` builds it step by step and checks each step against its criteria."
- **Problem:** When a step still fails its acceptance check after one fix attempt, `/sc:implement` stops (error `E-HALT-QA`) and will not move on until the developer either fixes the work or writes a ruling line in the progress file. The tool may not write that line itself. A newcomer will see an error code and not know a ruling exists, its exact format, or where it goes.
- **Evidence:** `MS/skills/sc-implement-protocol/refs/qa.md:61-68` (HALT; next options `fix | ruling | resume`; executor MUST NOT write the Ruling); `MS/skills/sc-implement-protocol/refs/ledger.md:61-70` (format and regex); `MS/commands/implement.md:57-58` (ledger at `.dev/implement/<slug>/progress.md`, `--resume`).
- **Replacement (add to level 3 and 2.3):**
  > If a step fails its check twice, `/sc:implement` stops with `E-HALT-QA` and prints the progress file path (`.dev/implement/<name>/progress.md`). Either fix the code yourself and run `/sc:implement @<plan.md> --resume`, or, if your lead agrees the step should be accepted as is, add a ruling line to the progress file in the exact form `T<step number>: Ruling: <what you decided> <dash> <why> <dash> <cost if wrong>`, then resume.
- **Open issue for the author:** the ledger regex requires a literal em dash (U+2014) as the separator (`refs/ledger.md:64, :70`). The guide's no-em-dash style rule conflicts with the exact text a user must type. The guide needs to show the literal character in a code span with a note, or the format will fail validation. Do not silently substitute a hyphen.

### F6 (IMPORTANT): 2.3 step 2, `--handoff implement` skips reading the plan

- **Quoted:** "**A few files:** `/sc:workflow "<describe the change>" --depth quick --handoff implement` plans the change and builds it, checking each step."
- **Problem:** With `--handoff implement`, `/sc:workflow` hands straight to `/sc:implement`, so code changes start before anyone reads the plan or its acceptance criteria. The level-3 row in section 1 runs the two commands separately, so the guide contradicts itself. Section 3's "Read a task file before you run it" rule is broken here.
- **Evidence:** `MS/commands/workflow.md:42` (`implement` = Skill invoke); `:80-82` ("Plan only. Next: `/sc:implement @plan.md`").
- **Replacement:**
  > 2. **A few files:** `/sc:workflow "Make the retry limit in src/jobs/runner.py configurable from settings.yaml, default 3, and cover it with a unit test" --depth quick`. Read `.dev/workflow/<name>/plan.md` and check that each step's acceptance criteria say what "done" means. Then `/sc:implement @.dev/workflow/<name>/plan.md`.

### F7 (IMPORTANT): 2.2 step 3, task-builder is not given the spec with `--spec`

- **Quoted:** "`/task-builder "Implement <feature> as described in <path to spec or research report>"`. Read the task file it produces and confirm it matches the spec."
- **Problem:** `/task-builder` has a `--spec <path>` input. With it, task-builder automatically checks that the task file covers every requirement in the spec (the same check 2.10 tells users to run by hand), and the final audit checks the built work against that spec. Without it, the spec-coverage check is skipped. A newcomer would not know that, and the "confirm it matches the spec" step becomes a manual eyeball check.
- **Evidence:** `MS/skills/task-builder/SKILL.md:39` (input 5, `--spec` feeds the PRE coverage audit and the POST audit); 02 research §A.4 line 60 (PRE gate needs `coverage_pct >= 0.90`; no spec means `verdict: skipped`).
- **Replacement:**
  > 3. **Build the task file.** `/task-builder "Implement CSV export for the invoices list. Why: finance needs monthly exports. Code: src/invoices/, src/api/routes/invoices.py" --spec docs/specs/invoice-csv-export.md`. With `--spec`, task-builder checks that every requirement in the spec has a task and lists any it missed under Open Questions in the task file. Read the task file and those Open Questions before running it.

### F8 (MINOR): 2.10 duplicates the task-builder check without saying when it is needed

- **Quoted:** "If you have a spec and a plan or task file built from it, check that the plan covers everything in the spec before you start: `/sc:reflect --mode pre --spec <path to spec> --tasklist <path to plan or task file>`."
- **Problem:** For task files built with `--spec`, this check has already run (F7). The manual command is only needed for `/sc:workflow` plans, task files built without `--spec`, and plans written by hand. The guide does not say where the result lands.
- **Evidence:** `MS/skills/task-builder/SKILL.md:39`; `MS/commands/reflect.md:83, :92` (output `.dev/reflect/<mode>-<slug>-<ts>/`).
- **Replacement:**
  > Task files built with `/task-builder --spec` already get this check. For a `/sc:workflow` plan, a task file built without `--spec`, or a hand-written plan, run `/sc:reflect --mode pre --spec docs/specs/invoice-csv-export.md --tasklist .dev/workflow/invoice-csv-export/plan.md`. The report in `.dev/reflect/pre-<name>-<timestamp>/` lists every requirement the plan misses. Fix the plan, then build.

### F9 (IMPORTANT): 2.1 step 6, release-split input and follow-up are undefined

- **Quoted:** "**Check the size (optional).** If the work looks too big for one release, `/sc:release-split <path to spec>` analyzes whether and where to split it."
- **Problem:** At this point the user has a PRD and a TDD, so "spec" is ambiguous. The command needs a file with identifiable requirements or scope items, and the TDD is the right input here. The guide also never says what to do with the result. If it recommends a split, it writes separate release specs, and Release 2 must not be planned until Release 1 has passed real-world validation. Step 7 then roadmaps the original PRD and TDD as if nothing had split.
- **Evidence:** `MS/commands/release-split.md:13-16` (required input: release artifact with identifiable requirements); `:53` (default output `<spec-dir>/release-split/`); `:62-64` (Part 3 produces release specs or tasklists; "do not split" is a valid result); `:108-127` (Will Not: produce roadmaps directly; Release 2 planning gated on Release 1 real-world validation).
- **Replacement:**
  > 6. **Check the size (optional).** If the work looks too big for one release, run `/sc:release-split docs/billing/TDD_BILLING.md`. It writes its analysis to `docs/billing/release-split/`. "Do not split" is a normal answer. If it recommends a split, it writes a separate spec for each release. Use the Release 1 spec instead of the TDD in step 7, and do not plan Release 2 until Release 1 is built and validated.

### F10 (IMPORTANT): 2.1 steps 1-2, the brainstorm output path and the PRD inputs are missing

- **Quoted:** "`/prd "<product or feature>"`, and point it at the brainstorm output and any existing notes."
- **Problem:** "The brainstorm output" is not a file a newcomer can find. Brainstorm writes `merged-requirements.md` under `.dev/brainstorms/<timestamp>-<slug>/` and stops there. The PRD skill asks for four things: scope, purpose, code areas, and output location. It defaults the output to a GFxAI-style `docs/docs-product/tech/...` path, which may not suit other repos. A bare `"<product or feature>"` triggers the skill's clarification questions.
- **Evidence:** `MS/commands/brainstorm.md:61, :179-191` (output dir; stops after merged requirements; `merged-requirements.md`); `MS/skills/prd/SKILL.md:35-56` (inputs and strong examples); `:45, :130` (default output path); `:59-62, :68-72` (weak prompts trigger clarification).
- **Replacement:**
  > 1. **Shape the idea (only if it is still vague).** `/sc:brainstorm "usage-based billing for API customers: metering, monthly invoices, overage alerts" --depth standard`. It asks you questions, has several agents propose approaches, and merges them into `.dev/brainstorms/<timestamp>-<slug>/merged-requirements.md`. It stops there.
  > 2. **Write the product requirements document (PRD).** `/prd "Create a PRD for usage-based billing. Purpose: align product and engineering on the first release. Start from .dev/brainstorms/<timestamp>-usage-billing/merged-requirements.md. Relevant code: src/billing/, src/api/metering/. Output to docs/billing/PRD_BILLING.md."`

### F11 (MINOR): 2.1 steps 3 and 5, "Fix them" does not say how

- **Quoted:** "A panel of expert reviewers lists gaps and contradictions. Fix them before moving on." / "Fix what it finds."
- **Problem:** `/sc:spec-panel` does not change the document without explicit consent, so a newcomer may expect the fixes to happen on their own. The guide should say who applies them and that the panel should be rerun afterwards.
- **Evidence:** `MS/commands/spec-panel.md:448-451` (Will Not: modify specifications without explicit user consent); `:22, :234` (`--iterations N`).
- **Replacement:**
  > The panel only reports. Decide which findings to accept, ask Claude to apply those to the PRD file, then run the same `/sc:spec-panel` command again until no critical findings remain.

### F12 (IMPORTANT): placeholder-only prompts across the levels table, 2.2, 2.5, and 2.9

- **Quoted:** "`/tech-research "<question>"`" (level 5, 2.5); "`/task-builder "<goal, with paths to any spec or research>"`" (level 4); "`/tech-reference "<feature>"`", "`/operational-guide "<procedure>"`", "`/readme "<project or module>"`" (2.9); "`/sc:task "<describe the change>"`" (level 2, 2.3).
- **Problem:** Each of these skills documents what a strong request contains: what, why, which code paths, and where the output goes. Each lists bare-topic requests as weak prompts that trigger clarification questions or produce shallow output. The guide gives no worked example and never says what to include, and the user has asked that every example invocation be concrete.
- **Evidence:** `MS/skills/tech-research/SKILL.md:51-88` (inputs; strong vs weak, "Research the agent system." is weak); `MS/skills/task-builder/SKILL.md:29-41, :80-98`; `MS/skills/tech-reference/SKILL.md:34-74`; `MS/skills/tdd/SKILL.md:54-59`.
- **Replacement (add near the top of section 2, then use concrete examples in each row):**
  > **How to write a request.** Every document and task skill asks for the same four things. Put them all in your first message, or the skill will stop and ask:
  > 1. What you want (a question, a feature, a document).
  > 2. Why you need it and any constraints.
  > 3. The code or documents to look at (paths).
  > 4. Where the result should go, if you care.
  >
  > Examples:
  > - `/tech-research "What would it take to add per-tenant rate limits to the public API? We are getting abuse from one tenant. Look at src/api/middleware/, src/tenants/, and config/limits.yaml. I need options with effort and risk, plus a recommended plan."`
  > - `/task-builder "Add per-tenant rate limits as recommended in .dev/tasks/to-do/TASK-RESEARCH-rate-limits-<timestamp>/RESEARCH-REPORT-rate-limits.md. Code: src/api/middleware/, src/tenants/. Why: one tenant is overloading the API."` (Use `--spec <path>` only when you have a real spec, PRD, or TDD. The source documents `--spec` for those document types, not for research reports.)
  > - `/tech-reference "Document the rate limiting feature we just built. Root: src/api/middleware/rate_limit/. Audience: engineers maintaining it. Output: docs/api/rate-limiting-technical-reference.md."`
  > - `/sc:task "Rename the misspelled variable recieved_at to received_at in src/jobs/runner.py and update its tests"`

### F13 (IMPORTANT): 2.4 step 3, a small fix has no regression test

- **Quoted:** "Small fix: make it, then `/sc:test <path> --coverage`."
- **Problem:** `/sc:test` only runs existing tests; it does not write new ones (the guide says so itself in 2.8). The bug was not caught by the current tests, so rerunning them proves little. The newcomer needs to add a test that reproduces the bug, see it fail, then see it pass after the fix.
- **Evidence:** `MS/commands/test.md:22` (run/coverage/watch flags only); 03 research line 94 ("Will not generate new test cases", `M:commands/test.md:102-106`); guide 2.8 line 93.
- **Replacement:**
  > - Small fix: first ask Claude to add a test that reproduces the bug (using the reproduction steps from the report) and confirm it fails. Then make the fix and run `/sc:test tests/jobs/test_runner.py --coverage` to confirm the new test and the existing ones pass.

### F14 (MINOR): 2.4 steps 1-2, the run time and report location are wrong or vague

- **Quoted:** "A normal run takes 1-3 minutes." / "**Read the report** in `.dev/troubleshoot/`."
- **Problem:** 1-3 minutes applies only to the first, single-agent pass. The default depth escalates automatically to several agents (about 4-15 minutes) when confidence is low, the problem is intermittent, or it spans domains. The report is a specific file inside a per-run folder.
- **Evidence:** `MS/commands/troubleshoot.md:51` (`quick` ~1-3 min; `standard` auto-escalates); `:56` (`.dev/troubleshoot/<slug>-<timestamp>/` with REPORT.md); 03 research line 29 (Tier 2 4-15 min).
- **Replacement:**
  > A simple bug usually takes 1-3 minutes. If the tool is not confident, or the problem is intermittent, it automatically brings in more agents, which can take up to about 15 minutes. ... 2. **Read the report** at `.dev/troubleshoot/<name>-<timestamp>/REPORT.md`.

### F15 (MINOR): 2.4 step 4, the post-fix audit has nothing to compare against

- **Quoted:** "**Confirm.** `/sc:reflect --mode post --diff <commit or branch> --no-promote`, then workflow 2.11."
- **Problem:** For a small manual fix there is no plan or spec, so the audit has nothing to check the change against. The troubleshoot report is the natural spec. For the `--fix` path, the task file already ran this audit (F3). The command's `--diff` also needs a range such as `main..HEAD`, not just "a commit".
- **Evidence:** `MS/commands/reflect.md:83, :85` (`--spec` recommended for UC-2; `--diff` takes a git ref such as `HEAD~1..HEAD` or a branch); `MS/commands/troubleshoot.md:190-193` (after `/task`, user runs the reflect validate gate).
- **Replacement:**
  > 4. **Confirm.** For a small manual fix: `/sc:reflect --mode post --diff main..HEAD --spec .dev/troubleshoot/<name>-<timestamp>/REPORT.md --no-promote`. For a fix done through a task file, read the task file's `reflect_post` verdict instead (2.1 step 9). Then follow workflow 2.11.

### F16 (IMPORTANT): 2.7 step 2, the `--preview` safety flag is not in the documented syntax

- **Quoted:** "preview first, then apply. `/sc:cleanup <path> --preview` ... `/sc:improve <path> --type quality --preview` ... Run each again without `--preview` once the preview looks right."
- **Problem:** The guide builds its safety step on `--preview`, but neither command lists it in its usage syntax; it appears only in one example line each. The documented safety flags are `--safe` and `--interactive`. `/sc:cleanup` applies some changes automatically (unused imports, dead code with zero references). If `--preview` is not honored, the "preview" run changes files.
- **Evidence:** `MS/commands/cleanup.md:22` (usage `[--type code|imports|files|all] [--safe|--aggressive] [--interactive]`), `:73` (only `--preview` mention), `:108-115` (auto-fix list); `MS/commands/improve.md:22` (usage `[--safe] [--interactive]`), `:81-83` (only `--preview` mention).
- **Replacement:**
  > 2. **Small, contained cleanups:** commit first so every change can be undone. Then run `/sc:cleanup src/billing/ --type code --safe --interactive` to remove dead code and unused imports, or `/sc:improve src/billing/ --type quality --safe --interactive` to improve code quality. Both ask before any change that might affect other code. Review the diff with `git diff` before keeping it.

### F17 (MINOR): 2.7 step 1, the cleanup audit has no target

- **Quoted:** "`/sc:cleanup-audit` produces an evidence-backed report of files to delete, consolidate, move, or keep."
- **Problem:** With no path it audits the whole repository in three passes. That is slow and noisy for someone who wants to clean one area. The command takes a target path and a pass choice.
- **Evidence:** `MS/commands/cleanup-audit.md:31-39` (`[target-path] [--pass surface|structural|cross-cutting|all] [--focus ...]`), `:58`.
- **Replacement:**
  > 1. **Find what needs cleaning.** `/sc:cleanup-audit src/billing/ --pass all` produces an evidence-backed report of files to delete, consolidate, move, or keep. It changes nothing. Leave out the path only when you mean the whole repository.

### F18 (IMPORTANT): 2.12, resume rows are missing for the document skills, and the PR log path is unstated

- **Quoted:** the table rows cover only `/task`, `/sc:implement`, `/sc:pr-submit` ("`/sc:pr-submit --resume <path to its run log>`"), and the unknown case.
- **Problem:** The guide's heaviest runs (`/tech-research`, `/prd`, `/tdd`, `/tech-reference`, `/roadmap`) are the most likely to be interrupted, and the table has no row for them. Each one resumes when you run the same command again: it finds its existing task folder and continues from the first unchecked item. `/sc:brainstorm` resumes with `--resume-from`. A newcomer also has no idea where the PR monitor run log is.
- **Evidence:** `MS/skills/tech-research/SKILL.md:173`; `MS/skills/prd/SKILL.md:168, :180`; `MS/skills/tdd/SKILL.md:149, :161`; `MS/skills/tech-reference/SKILL.md:183, :195`; `MS/skills/roadmap/SKILL.md:181, :201` (existing task file means skip Stage A and resume via `/task`); `MS/commands/brainstorm.md:63` (`--resume-from` a saved seed-brief); `MS/commands/pr-submit.md:40, :55` (`.dev/pr-monitor/pr-<N>-<ts>/monitor-run-<N>.jsonl`).
- **Replacement (add rows):**
  > | A document or plan skill (`/tech-research`, `/prd`, `/tdd`, `/tech-reference`, `/roadmap`) | Run the same command with the same topic again. It finds its folder under `.dev/tasks/to-do/` (for example `TASK-RESEARCH-<topic>-<timestamp>/`) and continues from the first unchecked item. You can also run `/task` on the task file inside that folder. |
  > | A brainstorm (`/sc:brainstorm`) | `/sc:brainstorm "<same topic>" --resume-from .dev/brainstorms/<timestamp>-<slug>/seed-brief.md` |
  > | A pull request monitor (`/sc:pr-submit`) | `/sc:pr-submit --resume .dev/pr-monitor/pr-<PR number>-<timestamp>/monitor-run-<PR number>.jsonl` |

### F19 (MINOR): 2.11, the commit step and pr-submit prerequisites are missing

- **Quoted:** "5. **Push.** Only after your lead approves. 6. **Open the PR.** `/sc:pr-submit --monitor 1 --head <branch> ...`"
- **Problem:** No step says to commit before review and push. At `--monitor 1` the command stops if it cannot confirm the PR on the origin repository or if the GitHub CLI check-waiting preflight fails, so a newcomer needs `gh` installed and logged in. The review it waits for comes from the Augment Code bot. Step 4's `/sc:auggie-review` also ends by offering a remediation chain by default, which a newcomer should know they can decline.
- **Evidence:** `MS/commands/pr-submit.md:22-31` (required PR context; STOP conditions; `gh pr checks` preflight); `:64-66` (detection contract `augmentcode[bot]`); `MS/commands/auggie-review.md:52` (`--remediation-offer` default true).
- **Replacement:**
  > 1a. **Commit locally.** Commit your changes on your feature branch (do not push yet).
  > ... 4. ... At the end it offers to plan fixes for what it found. Accept only if you want a task file built for them.
  > ... 6. **Open the PR.** You need the GitHub CLI (`gh`) installed and logged in. `/sc:pr-submit --monitor 1 --head feature/invoice-csv-export --title "Add CSV export to invoices list" --body "Adds monthly CSV export for finance. Spec: docs/specs/invoice-csv-export.md. Tests: tests/invoices/test_export.py."`

### F20 (IMPORTANT, needs author ruling): section 1, the hard limit contradicts its own source rule

- **Quoted:** "Two hard limits: if the work needs more than 5 edits or touches more than one file, use level 3 or higher."
- **Problem:** The only source for a "more than 5 edits or more than one file" limit is the IC-Harness project rule, and it requires a task file (level 4), not a `/sc:workflow` plan (level 3). The supporting research cites it that way. IronClaude master has no such limit. Either the guide is relaxing the rule on purpose, which the user must approve, or it is a sequencing error. Level 3 is also resumable (`--resume` ledger), so the second sentence ("survive a crash ... level 4 or higher") understates level 3.
- **Evidence:** `/Users/cmerritt/GFxAI/IC-Harness/CLAUDE.md` Custom Project Rule 6 ("Any work >5 edits or involving multiple files MUST go through a task file"); 02 research Part 2 §1 rung 0 (line 224); `MS/commands/implement.md:57` (`--resume`).
- **Replacement (if the rule is kept as written):**
  > Two hard limits: if the work needs more than 5 edits or touches more than one file, use level 4 or higher (a task file). If it must run for hours or be checked by several independent reviewers, use level 4 or higher.
- **Alternative (only if the user approves relaxing it for IronClaude teams):** keep "level 3 or higher" and add one line saying this is looser than the IC-Harness rule on purpose.

### F21 (MINOR): section 4, the tool boundaries newcomers mix up are missing

- **Quoted:** section 4 lists only `/task` vs `/sc:task`, `/roadmap` vs `/sc:roadmap`, cleanup-audit vs cleanup, tech-research vs research.
- **Problem:** The workflows pick between `/sc:design` and `/tdd` (2.2 vs 2.1), `/sc:workflow`+`/sc:implement` and `/task-builder`+`/task` (levels 3 vs 4), and `/sc:document` and `/tech-reference` (2.9). Nothing explains how to choose. The choices in the guide are defensible but not explained.
- **Evidence:** `MS/commands/design.md:22, :88-115` (single-pass design spec; next step `/sc:implement`; no task file); `MS/skills/tdd/SKILL.md` description plus the Stage A/B task file run; `MS/commands/implement.md:120-127` (no `/task`, no 6-agent gates, one reviewer per step); `MS/commands/document.md:22` (`--type inline|external|api|guide`).
- **Replacement (add rows):**
  > | `/sc:design` and `/tdd` | `/sc:design` writes one quick design (an API, a component, a schema) in a single pass. `/tdd` writes a full technical design document from the template, with research and independent reviewers, and takes much longer. Use `/sc:design` for a change inside an existing system; use `/tdd` when other people will build against the design. |
  > | `/sc:workflow` + `/sc:implement` and `/task-builder` + `/task` | The first pair writes a short plan and checks each step with one reviewer. The second pair researches the code, writes a full task file, and checks every phase with a panel of reviewers. Use the second pair for many files, multi-session work, or anything that must not drift. |
  > | `/sc:document` and `/tech-reference` | `/sc:document` writes reference text for specific code (comments, API docs) in one pass. `/tech-reference` researches a whole feature and writes a reviewed architecture document. |

### F22 (MINOR): undefined jargon and an overloaded word

- **Quoted:** "a build request for each phase" (2.1 step 7); "Do not disable a reviewer step or QA gate" (section 3); "acceptance criteria" (level 3); "spec" (2.2, 2.10); "With no `--monitor` level it edits your code ... (level 2). Level 3 also pushes" (section 4).
- **Problem:** "Build request", "QA gate", "phase", and "spec" are never defined for a newcomer. "Level" means the six process levels in section 1 and also the `/sc:pr-submit` monitor setting in section 4, so "level 2" and "level 3" in section 4 read as process levels 2 and 3.
- **Evidence:** guide lines 11-18 (process levels) vs line 153 (monitor levels); `MS/commands/pr-submit.md:26, :47` (the flag is `--monitor {0,1,2,3}`).
- **Replacement:** add a five-line glossary after section 1 (spec: a document stating what must be built and how you will know it works; task file: a checklist file under `.dev/tasks/to-do/` that `/task` runs item by item; build request: the input file `/task-builder` turns into a task file; phase: a group of task-file items checked together before moving on; quality check (QA gate): a point where independent reviewer agents check the work and can stop the run). In section 4 write "With no `--monitor` setting it uses `--monitor 2` and edits your code ... `--monitor 3` also pushes on its own."

### F23 (MINOR): 2.2 step 2, the design step is vague

- **Quoted:** "Write a short spec (what changes, which files, how you will know it works). For interfaces or APIs, `/sc:design "<component>"` produces a design."
- **Problem:** `/sc:design` takes a type and a format, and the guide gives neither or a place to save the result. The spec written here should be saved as a file so step 3 can pass it with `--spec` (F7).
- **Evidence:** `MS/commands/design.md:22, :67` (`--type architecture|api|component|database`, `--format diagram|spec|code`; example `/sc:design payment-api --type api --format spec`).
- **Replacement:**
  > 2. **Agree the design.** Write a short spec file, for example `docs/specs/invoice-csv-export.md`, saying what changes, which files, and how you will know it works. For an interface or API, `/sc:design invoice-export-api --type api --format spec` drafts it. Save its output into that spec file. Have your lead approve the spec.

### F24 (MINOR): level 5, the research report location is missing

- **Quoted:** "`/tech-research "<question>"`. Then pass its report to `/task-builder` (level 4)."
- **Problem:** The newcomer is not told where the report lands. The research-to-task-builder hand-off is good practice but not a documented chain in source; that is acceptable if it is presented as advice.
- **Evidence:** `MS/skills/tech-research/SKILL.md:136` (`${TASK_DIR}RESEARCH-REPORT-[descriptor].md` under `.dev/tasks/to-do/TASK-RESEARCH-<subject>-<timestamp>/`); 02 research Part 2 §3 line 267 (hand-off INFERRED, not coded).
- **Replacement:**
  > `/tech-research "<question, why, code paths>"` (see "How to write a request"). The report is written to `.dev/tasks/to-do/TASK-RESEARCH-<topic>-<timestamp>/RESEARCH-REPORT-<topic>.md`. Then give that path to `/task-builder` (level 4).

## Summary

- Checks passed: 3 / 12 (items 1, 3, 10); partial or fail: 9
- Findings: 24 total. IMPORTANT: 14 (F1-F7, F9, F10, F12, F13, F16, F18, F20). MINOR: 10 (F8, F11, F14, F15, F17, F19, F21, F22, F23, F24). CRITICAL: 0
- Issues fixed in place: 0 (report-only lens; the guide was not edited)

## Issues Found (index)

| # | Severity | Location | Issue | Required fix |
|---|----------|----------|-------|-------------|
| F1 | IMPORTANT | 2.1 step 7 | /roadmap makes task files only at Deep; no output paths, no review step | F1 replacement |
| F2 | IMPORTANT | 2.1 step 7, level 6 | Roadmap prompt missing why/project name | F1 example |
| F3 | IMPORTANT | 2.1 step 9, 2.2 step 5 | Manual POST reflect duplicates built-in gate | Read `reflect_post` instead |
| F4 | IMPORTANT | 2.1 step 8, 2.2 step 4, level 4 | No instruction when /task halts | Add halt paragraph |
| F5 | IMPORTANT | level 3, 2.3 | No instruction for `E-HALT-QA` / Ruling line | Add halt paragraph; resolve em-dash conflict |
| F6 | IMPORTANT | 2.3 step 2 | `--handoff implement` skips plan review | Split into plan, read, implement |
| F7 | IMPORTANT | 2.2 step 3 | `--spec` not used | Add `--spec` |
| F8 | MINOR | 2.10 | Duplicates task-builder PRE check | Scope it to non-task-builder plans |
| F9 | IMPORTANT | 2.1 step 6 | release-split input and follow-up undefined | F9 replacement |
| F10 | IMPORTANT | 2.1 steps 1-2 | Brainstorm output path and PRD inputs missing | F10 replacement |
| F11 | MINOR | 2.1 steps 3, 5 | "Fix them" with no mechanism | Say who applies and rerun |
| F12 | IMPORTANT | levels table, 2.2, 2.5, 2.9 | Placeholder-only prompts | Add "How to write a request" + examples |
| F13 | IMPORTANT | 2.4 step 3 | No regression test | Add reproduce-test step |
| F14 | MINOR | 2.4 steps 1-2 | Run-time claim and report path | F14 replacement |
| F15 | MINOR | 2.4 step 4 | Reflect with no spec, single-commit diff | Pass REPORT.md as spec, use a range |
| F16 | IMPORTANT | 2.7 step 2 | `--preview` not in documented syntax | Use `--safe --interactive`, commit first |
| F17 | MINOR | 2.7 step 1 | Audit has no target | Add path and pass |
| F18 | IMPORTANT | 2.12 | Doc-skill and brainstorm resume rows missing; PR log path | Add rows |
| F19 | MINOR | 2.11 | No commit step; pr-submit prerequisites | Add steps |
| F20 | IMPORTANT | section 1 | Hard limit contradicts its source rule | Author ruling needed |
| F21 | MINOR | section 4 | design/tdd, workflow/task-builder, document/tech-reference boundaries missing | Add rows |
| F22 | MINOR | sections 2.1, 3, 4 | Undefined jargon; "level" overloaded | Glossary; rename to `--monitor` setting |
| F23 | MINOR | 2.2 step 2 | Design step vague | F23 replacement |
| F24 | MINOR | level 5 | Report location missing | F24 replacement |

## Recommendations

1. Apply F1, F3, F4, F5, F7, F12, F16, F18 first. These are the points where a newcomer either gets stuck (no task file, a halt with no instructions, no resume path) or does avoidable damage or duplicate work (preview flag, rerunning the audit).
2. Get the user's ruling on F20 (level 3 vs level 4 for multi-file work) and on F5's em-dash conflict before editing those sections.
3. Removals proposed (each needs user adjudication): none outright. F3 proposes replacing the manual `/sc:reflect --mode post` command in 2.1 step 9 and 2.2 step 5 with "read the task file's `reflect_post` verdict", because the task file already runs that audit. F6 proposes removing `--handoff implement` from 2.3 step 2, because it skips the plan review.

## Confidence Gate

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (for the checklist items; the verdict is FAIL because findings exist)
- **Tool engagement:** Read: 3 | Grep: 0 (content searches were run through Bash grep in this session) | Glob: 0 | Bash: 14 | tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0
- **Limitations:** The behavior of `--preview` on `/sc:cleanup` and `/sc:improve` was checked only against the command files. The underlying execution was not run, so F16 states "not in the documented syntax", not "does not work". Built-in Claude Code commands (`/code-review`, `/security-review`) are outside IronClaude source and were not verified. The skill-mode POST reflect promotion behavior (whether the built-in gate moves the task folder to done) was not traced end to end.

## QA Complete


