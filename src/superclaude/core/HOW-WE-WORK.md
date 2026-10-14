# IronClaude: How We Work

This guide tells you which IronClaude skills and commands to use for each kind of work, and in what order. Keep it open while you work. `superclaude install` copies this guide to `~/.claude/HOW-WE-WORK.md`; run `superclaude update` after upgrading IronClaude to refresh that copy. `superclaude update` overwrites every file it ships, including an edited `~/.claude/CLAUDE.md`, and keeps no backup. It also deletes and re-copies each shipped skill folder in `~/.claude/skills/`, so any file you added inside one is lost. Copy any file you changed or added before you run it. Plugin installs ship only some of these commands and skills; for the full set run `pipx install git+https://github.com/IronbellyOrg/IronClaude && superclaude install` (the `superclaude` package on PyPI is the upstream project, not IronClaude).

---

## 1. How much process does this job need?

Every job falls into one of six levels. Find the first row that describes your job. If you are unsure between two rows, choose the heavier one.

<!-- level-table:v1 -->

| Level | Use this when | What you run | What you end up with |
|---|---|---|---|
| **1. Ask a question** | You want to understand code, a decision, or how something works, and you do not want anything changed. | Ask Claude in plain English. For an explanation of specific code, `/sc:explain src/jobs/runner.py`. | An answer. No files change. |
| **2. Make a small, direct change** | The change is in one source file (plus its test file), needs five edits or fewer, and you already know exactly what it should be. | Ask Claude to make the change and run the related test, or use `/sc:task "Rename recieved_at to received_at in src/jobs/runner.py and update its tests"`. `/sc:task` prints a `Tier:` line at the start. If it says `STANDARD` or `STRICT`, it runs the affected tests itself; if it says `LIGHT` (typos, comments, formatting) or `EXEMPT` (no code change, such as explain or commit), it skipped checking, so run the test yourself afterwards. | The edited file and a passing test. |
| **3. Follow a simple checked plan** | The change touches a few files, the requirements are clear, and it fits in one or two sessions. | `/sc:workflow "<what to change, why, which files>" --depth quick` writes a plan in which every step has acceptance criteria (a written definition of "done" for that step), then checks the plan against your request automatically. It prints the plan path, `.dev/tasks/to-do/<id>/<id>.md`, and the check result. `<id>` is the plan folder's name, for example `TASK-WF-retry-limit-20261013-142530`; the plan file is `<id>.md` inside it. Copy the path `/sc:workflow` prints. Read the plan, then run `/sc:implement <that path>`. It builds one step at a time and has a reviewer check each step against its criteria. | A plan folder holding the plan and `progress.md` (one line per step), plus the code changes in your repository. If interrupted, run the same `/sc:implement` command again; it continues from the first unfinished step. When every step passes, a final independent review runs and the folder moves to `.dev/tasks/done/`. On any system other than Linux (including macOS) the move is refused on purpose: the folder stays in `.dev/tasks/to-do/` and the run reports archive-blocked. That is expected; never move the folder by hand. |
| **4. Build and run a task file** | The work touches many files, will take more than one session, or must not drift from what was agreed. | `/task-builder "<what to build, why, which code>"` researches the code and writes a task file: a checklist under `.dev/tasks/to-do/`. If you have a spec, PRD, or TDD, add `--spec <path to it>` so the task file is checked against it. Read the task file, then run `/task <path to task file>`. | `/task` works through the checklist item by item. The items are grouped into phases; after each phase except the first (setup) one, a panel of independent reviewer agents checks the work. At the end it runs the tests and an independent audit comparing what was built with the plan. It survives crashes. |
| **5. Research first** | You do not yet know how the current system works, what needs to change, or whether the idea is feasible. | `/tech-research "<question, why you need it, which code to look at>"`. Then build the task file from it: `/task-builder "<what to build> as recommended in <path to the report>. Code: <folders>"` (level 4). | A report at `.dev/tasks/to-do/TASK-RESEARCH-<topic>-<timestamp>/RESEARCH-REPORT-<topic>.md` with findings, options, and a recommended plan. |
| **6. Write a full specification** | You are building a new product, a new component, or a major feature that other people will build against. | `/prd`, then `/tdd`, then `/roadmap`. See workflow 3.1 of the routing guide (`HOW-WE-WORK.md`). | A product requirements document, a technical design document, a phased roadmap, and a task file for every phase. |

**Hard limit:** if the work needs more than 5 edits or touches more than one source file (its matching test file does not count), it must go through a written plan: level 3 for a few files with clear scope, level 4 for anything larger, longer, or riskier. An edit is one change in one place in a file (one block of consecutive changed lines); renaming a name used in 8 places is 8 edits. The one exception is `/sc:cleanup` and `/sc:improve` run on a folder (section 3.7 of the routing guide): commit first and review `git diff` afterwards.

<!-- /level-table -->

---

## 2. How to write a request

Every research, document, and task skill works from the same four things. If the first one is missing or vague, the skill stops and asks you for it. The other three are optional, but each one makes the result noticeably better and faster. Put all four in your first message:

1. **What** you want: the question, feature, or document.
2. **Why** you need it, and any constraints.
3. **Where to look:** the code folders and documents it should read, as paths.
4. **Where the result goes**, if it matters.

| Weak request | Strong request |
|---|---|
| `/tech-research "rate limiting"` | `/tech-research "What would it take to add per-tenant rate limits to the public API? One tenant is overloading it. Look at src/api/middleware/, src/tenants/, and config/limits.yaml. I need options with effort and risk, and a recommended plan."` |
| `/task-builder "add rate limits"` | `/task-builder "Add per-tenant rate limits as recommended in .dev/tasks/to-do/TASK-RESEARCH-rate-limits-<timestamp>/RESEARCH-REPORT-rate-limits.md. Code: src/api/middleware/, src/tenants/. Why: one tenant is overloading the API."` |
| `/tech-reference "rate limiting"` | `/tech-reference "Document the rate limiting feature we just built. Code: src/api/middleware/rate_limit/. Audience: engineers who maintain it. Output: docs/api/rate-limiting-technical-reference.md."` |

---

## 3. Workflows

### 3.1 Build a new product or major feature (full specification)

Use this when the work is big enough that people need to agree on *what* is being built and *how* before anyone writes code. The example builds usage-based billing.

1. **Shape the idea (only if it is still vague).**
   `/sc:brainstorm "Usage-based billing for API customers: metering, monthly invoices, overage alerts" --depth standard`
   It asks you questions, has several agents propose approaches, and merges them into `.dev/brainstorms/<timestamp>-<name>/merged-requirements.md`. It stops there. If you will build it directly without a PRD, add `--handoff task`: it then builds a task file from the merged requirements (level 4).

2. **Write the product requirements document (PRD).** The PRD defines *what* to build and *why*: users, problems, requirements, success measures, and scope.
   `/prd "Create a PRD for usage-based billing. Purpose: align product and engineering on the first release. Start from .dev/brainstorms/<timestamp>-usage-billing/merged-requirements.md. Relevant code: src/billing/, src/api/metering/. Output to docs/billing/PRD_BILLING.md."`
   The skill researches, writes, and reviews the PRD itself, including its own consistency checks.

3. **Get an expert critique of the PRD.**
   `/sc:spec-panel @docs/billing/PRD_BILLING.md --mode critique --focus requirements`
   A panel of named software-requirements experts judges whether the requirements are measurable, testable, and complete. It only reports. Decide which findings to accept, ask Claude to apply them to the PRD, then run the same command again until no critical findings remain.

4. **Write the technical design document (TDD) from the PRD.** The TDD defines *how* it will be built: architecture, data, interfaces, testing, and migration.
   `/tdd "Create a TDD for the billing service from docs/billing/PRD_BILLING.md. Relevant code: src/billing/, src/api/metering/. Output to docs/billing/TDD_BILLING.md."`

5. **Get an expert critique of the TDD.**
   `/sc:spec-panel @docs/billing/TDD_BILLING.md --mode critique --focus architecture,testing`
   Apply accepted findings the same way as step 3.

6. **Check whether it should be split (optional).** If the work looks too big for one release:
   `/sc:release-split docs/billing/TDD_BILLING.md`
   It writes its analysis to `docs/billing/release-split/`. "Do not split" is a normal answer. If it recommends a split, it writes a separate spec for each release: use the Release 1 spec in place of the TDD in step 7, and do not plan Release 2 until Release 1 is built and validated.

7. **Turn the PRD and TDD into a phased plan.**
   `/roadmap "Create a full roadmap from docs/billing/PRD_BILLING.md and docs/billing/TDD_BILLING.md. Each phase must be independently deployable and keep the old invoice API working. Project name: billing-v2. Dry run first so I can review the phase plan."`
   The dry run shows the proposed phases and waits for your yes. The finished run prints the roadmap path (under `.dev/tasks/to-do/TASK-ROADMAP-billing-v2-<timestamp>/`) and the list of phase task files in run order. At its full setting it also checks the phase task files against the roadmap and your PRD and TDD; those check reports are in the roadmap folder's `qa/` subfolder. Read the roadmap before running anything.
   - If the summary lists build requests (`build-requests/BUILD_REQUEST-phase-NN-<name>.md`) but no task files, the run chose its middle setting, which stops at build requests. (A build request is the short input file `/task-builder` turns into a task file.) Create each phase's task file with `/task-builder <path to that build request> --spec docs/billing/TDD_BILLING.md`. Saying "full roadmap" or "comprehensive" in the request avoids this.

8. **Build one phase at a time.**
   `/task <path to the phase 1 task file>`
   Let it run to the end. Each task file already contains everything that checks the work: reviewer panels after each group of items inside it (except the first, setup group), the tests, and, as its last steps, an independent audit (`/sc:reflect`) comparing what was built with the plan. Do not run those checks again yourself.

9. **Confirm the phase passed, then start the next one.** Open the task file and read the `reflect_post` entry at the top: the audit's verdict and the path to its report. Any problems the audit could not fix are listed under the task file's Open Questions. Decide each one with your lead (or yourself, if you work alone), the same way as a `/task` stop (note below): fix the code, correct the spec, or accept it in writing. Only if you changed anything to resolve them, re-confirm with `/sc:reflect --mode post --tasklist <path to the task file> --spec docs/billing/TDD_BILLING.md --diff <commit before the work started> --no-promote` before starting the next phase. Give that one commit, not a `..HEAD` range: a single commit is compared with your working tree, so the audit also sees work you have not committed (`/task` does not commit). Run `git add -A` first so that new files are included. Commit each phase once it passes, so that commit is the one you made when the previous phase passed (for the first phase, the commit before the work started). It is `HEAD` if you have not committed since this phase started; otherwise find it with `git log --oneline`. The final audit runs before the task is marked done, so the folder stays in `.dev/tasks/to-do/`. Leave the folder where it is; nothing in this guide needs it moved.

10. **Review and open a pull request.** Workflow 3.11.

11. **Document what was built.** Workflow 3.9 (`/tech-reference`).

**If `/task` stops partway:** it shows the reviewers' findings and writes them to the Task Log at the bottom of the task file (the file's `status` may say Blocked, with a reason). Decide the fix with your lead (or yourself, if you work alone): change the code, correct the spec, or amend the task item. Then run the same `/task <path>` command again; it continues from the first unchecked item. Never tick items by hand to get past a stop.

### 3.2 Add a feature to an existing system (no PRD needed)

Use this when the requirements are already clear and the feature extends something that exists. The example adds CSV export to an invoices page.

1. **Understand the current code (if you need to).**
   `/tech-research "How does the invoices list load and format its data, and what would need to change to add a monthly CSV export? Finance needs it for month-end. Look at src/invoices/ and src/api/routes/invoices.py."`

2. **Write and agree the spec.** Save a short spec file, for example `docs/specs/invoice-csv-export.md`, saying what changes, which files, and how you will know it works. If it includes a new interface or API, `/sc:design invoice-export-api --type api --format spec` drafts that part; paste its output into the spec file. Have your lead approve the spec.

3. **Build the task file, passing the spec.**
   `/task-builder "Implement monthly CSV export for the invoices list. Why: finance month-end. Code: src/invoices/, src/api/routes/invoices.py" --spec docs/specs/invoice-csv-export.md`
   Passing `--spec` makes task-builder check that every requirement in the spec has a task. The result is in the `reflect_pre` entry at the top of the task file. If the check fails (less than 90% of requirements covered), the missed requirements are added to the task file's Open Questions. Without `--spec` this check is skipped. Read the task file and its Open Questions before running it. To resolve an Open Question: for a spec requirement the task file missed, add it to the existing task file as a new unchecked checklist item (`- [ ]`) in the phase where it belongs (or ask Claude to add it), then run `/task <task file path>`; `/task` picks up from the first unchecked item. For an open question about intent, write the answer under the question in the task file before running `/task`. Do not tick checklist items.

4. **Run it.** `/task <path to task file>`. If it stops partway, see the note at the end of 3.1.

5. **Confirm and ship.** Read the task file's `reflect_post` verdict (as in 3.1 step 9), then workflow 3.11.

### 3.3 Make a small, well-defined change

1. **One source file (plus its test), five edits or fewer:** use level 2 (section 1).

2. **A few files with clear scope:**
   `/sc:workflow "Make the retry limit in src/jobs/runner.py configurable from settings.yaml, default 3, and cover it with a unit test" --depth quick`
   Read the plan at the path it prints (`.dev/tasks/to-do/<id>/<id>.md`; `<id>` is defined in section 1, level 3) and the check result printed with it, and check that each step's acceptance criteria clearly say what "done" means. Then:
   `/sc:implement .dev/tasks/to-do/<id>/<id>.md`
   It runs the tests itself as it goes.
   - **If a step fails its check twice,** `/sc:implement` stops with the code `E-HALT-QA` and prints the progress file path (`progress.md`, beside the plan). Either fix the code yourself and run the same command again, or, if your lead agrees the step should be accepted as it is, add this line to the progress file yourself, with the dashes exactly as shown: `T<step id>: Ruling: <what you decided> — <why> — <cost if wrong>`, then run the same command again. The tool rejects any other form and never writes the ruling for you. If you accepted a step this way, the plan folder only moves to `done/` after you also add `ARCHIVE: Ruling: <what, naming T<step id>> — <why> — <cost if wrong>` to the same progress file. (The rule's installed copy: `~/.claude/skills/sc-implement-protocol/refs/ledger.md`.) Do not edit the plan after the first step starts; the tool stops with `E-PLAN-CHANGED`.

3. **Ship.** Run the tests yourself only if nothing ran them (a plain edit, or a trivial `/sc:task` change). Then follow workflow 3.11. Its `/code-review` step looks for bugs, which the step-by-step reviewer does not.

### 3.4 Fix a bug

1. **Diagnose it.** Describe what happens, what you expected, how to reproduce it, and paste the exact error.
   `/sc:troubleshoot "Nightly invoice job fails with KeyError: 'tenant_id' in src/billing/invoice_job.py since yesterday's deploy. Expected: invoices for all tenants. Reproduce: python -m billing.invoice_job --date 2026-09-30" --type bug`
   Use `--type test`, `build`, `performance`, `deployment`, or `security` when that fits better. It finds the root cause with file and line evidence and changes nothing. A simple bug takes 1-3 minutes. If it is not confident, or the problem is intermittent or spans several areas, it automatically brings in more agents, which can take another 4-15 minutes. `--depth quick` stops it after the first pass; `--depth deep` always brings in several agents testing competing explanations after that first pass.
   If you suspect the fix will be larger or riskier than a few files with clear scope, add `--fix` now. If the diagnosis succeeds, it then offers to build a task file for the fix, and changes nothing unless you accept.

2. **Read the report** at `.dev/troubleshoot/<name>-<timestamp>/REPORT.md`. It says whether the fix belongs in the code, the test, or the documentation.

3. **Fix it.**
   - **Small fix (one source file plus its test, five edits or fewer):** first ask Claude to add a test that reproduces the bug (using the report's reproduction steps) and confirm the test fails. Then make the fix and run `/sc:test tests/billing/test_invoice_job.py --coverage` to confirm the new test and the existing ones pass.
   - **A few files with clear scope:** `/sc:workflow "<the fix described in REPORT.md, with a test that reproduces the bug>" --depth quick`, then `/sc:implement .dev/tasks/to-do/<id>/<id>.md` (the plan path it prints; level 3).
   - **Larger or riskier fix:** accept the task-file offer from step 1. If you did not pass `--fix`, do not diagnose again; build the task file from the report you already have: `/task-builder "Fix the root cause described in .dev/troubleshoot/<name>-<timestamp>/REPORT.md, with a test that reproduces the bug. Code: <files the report cites>"`. Then `/task <path>`; if it stops partway, see the note at the end of 3.1. The task file runs its own reviews, tests, and final audit; read its `reflect_post` verdict when it finishes.
   - **If the report says the cause is not confirmed:** do not fix anything yet. Run the checks the report lists, then run `/sc:troubleshoot` again with what you learned added to the description, or with `--depth deep`.

4. **Ship.** Workflow 3.11.

### 3.5 Investigate how something works, or whether an idea is feasible

| You want to know | Run |
|---|---|
| How part of our system works, what would need to change, or whether something is feasible | `/tech-research "How do background jobs get scheduled and retried today, and could we move them to a queue without downtime? Look at src/jobs/ and deploy/worker.yaml."` It writes a report with findings, options, and a recommended plan. |
| Something outside our code: a library, a standard, a best practice | `/sc:research "Current best practice for idempotent webhook handling with Stripe" --depth deep` (searches the web) |
| The general health of a module | `/sc:analyze src/billing/ --focus security` (or `quality`, `performance`, `architecture`). It reports only and changes nothing. |
| What a specific piece of code does | `/sc:explain src/billing/invoice_job.py` |

### 3.6 Make a hard decision or compare options

| Situation | Run |
|---|---|
| The idea or requirements are still unclear | `/sc:brainstorm "<the idea, who it is for, the main constraint>"`. It ends with merged requirements you can take into `/prd` (3.1). Add `--handoff task` to go straight to a task file instead. |
| You have two or more competing designs, plans, or drafts | `/sc:adversarial --compare docs/design-a.md,docs/design-b.md`. Agents debate them, score them, and merge the strongest parts into one document. |
| A spec, PRD, or TDD needs an outside expert critique | `/sc:spec-panel @docs/specs/invoice-csv-export.md --mode critique`. It only reports; you decide what to apply. |
| You want reviewers from other AI model families | `/sc:swarm-wizard`. It asks what you want reviewed, picks the settings, proves them with a safe dry run, and launches the real review only after you say go. Real runs need an OpenAI-compatible model proxy set in `~/.aienv`: one `export KEY=value` line each for `T2ProxyUrl` (proxy base URL), `T2ProxyKey` (API key), and `T2Model01` (model name), and make sure your shell sources the file (for example from your shell profile) before you start Claude; without it you get the dry run only. The full list of review styles by goal is in the IronClaude repository (not installed): https://github.com/IronbellyOrg/IronClaude/blob/master/docs/swarm/wizard-guide.md |
| The question is about business strategy, not code | `/sc:business-panel @docs/billing/PRD_BILLING.md` |

### 3.7 Refactor or clean up code

1. **Find what needs cleaning.**
   `/sc:cleanup-audit src/billing/ --pass all`
   It writes an evidence-backed report (under `.claude-audit/`) of files to delete, consolidate, move, or keep, and changes nothing. Without `--pass all` it runs only its quick first pass (delete, review, or keep). Leave out the path only when you mean the whole repository.

2. **Small, contained cleanups.** Commit first so every change can be undone. Then:
   `/sc:cleanup src/billing/ --type code --safe --interactive` removes dead code and unused imports.
   `/sc:improve src/billing/ --type quality --safe --interactive` improves code quality.
   `--interactive` asks before complex changes, but some changes are applied automatically even then: `/sc:cleanup` removes unused imports, code nothing references, empty blocks, and redundant type annotations; `/sc:improve` fixes formatting and naming, removes unused variables, reorders imports, and adds simple type annotations. Review `git diff` before keeping anything.

3. **Large refactors** (many files or a structural change): treat it as a feature. Write a spec and build a task file with `/task-builder ... --spec` (3.2), so every step is checked.

### 3.8 Run tests and check coverage

- `/sc:test tests/billing/ --coverage` runs the tests and reports coverage. Add `--type unit`, `integration`, or `e2e` to narrow it.
- `/sc:test` does not write new tests. To add tests, put them in the spec and the task file (3.2), or ask Claude to write them for a small change (3.4 step 3).

### 3.9 Document existing work

These skills document things that already exist. A PRD and a TDD are planning documents for something you are about to build; see 3.1.

| You need | Run |
|---|---|
| A technical reference for a built feature: architecture, how it works, how to extend it | `/tech-reference "Document the usage billing feature. Code: src/billing/, src/api/metering/. Audience: engineers who maintain it. Output: docs/billing/billing-technical-reference.md."` |
| Step-by-step instructions to install, deploy, or operate something | `/operational-guide "Write the operational guide for deploying the billing worker to staging and production, including rollback. Sources: deploy/worker.yaml, scripts/deploy_worker.sh. Audience: on-call engineers. Output: docs/billing/billing-worker-deploy-operational-guide.md."` |
| A README for a project, module, or package | `/readme "Write the README for the src/billing/ package: what it does, setup, configuration, and how to run its tests. Use docs/billing/billing-technical-reference.md if it exists. Audience: new engineers. Output: src/billing/README.md."` |
| Reference text for specific functions, classes, or API endpoints | `/sc:document src/api/routes/invoices.py --type api` |

### 3.10 Check a plan before you run it

For a task file, open it and read the `reflect_pre:` block in the file's header (between the first two `---` lines). That entry, not how the file was built, tells you whether the check already ran.

- **`verdict: pass` or `verdict: fail`:** it has already been checked against the spec. Resolve anything listed under Open Questions before running `/task`: for a spec requirement the task file missed, add it to the existing task file as a new unchecked checklist item (`- [ ]`) in the phase where it belongs (or ask Claude to add it), then run `/task <task file path>`; `/task` picks up from the first unchecked item. For an open question about intent, write the answer under the question in the task file before running `/task`. Do not run the check again.
- **A `/sc:workflow` plan:** it was checked against your request when it was written; the result is printed with the plan path and stored in the plan folder's `return-contract.yaml` (`reflect_status`, `reflect_report_path`). If a separate spec, PRD, or TDD exists beyond your request, run the check below against that spec.
- **`verdict: skipped`** (no spec was found when it was built, which can happen with task files made from roadmap build requests or from a research or troubleshoot report), or **a plan you wrote yourself:** it has not been checked. If you have a spec, PRD, or TDD for this work, run:
  `/sc:reflect --mode pre --spec docs/specs/invoice-csv-export.md --tasklist <task file or plan path>` (for a plan you wrote yourself, give the path to your plan file; for a plan made by `/sc:workflow`, the path is `.dev/tasks/to-do/<id>/<id>.md`)
  The report in `.dev/reflect/pre-<name>-<timestamp>/` lists every requirement the plan misses. For a task file: add each missed requirement to the existing task file as a new unchecked checklist item (`- [ ]`) in the phase where it belongs (or ask Claude to add it), then run `/task <task file path>`; `/task` picks up from the first unchecked item. For an open question about intent, write the answer under the question in the task file before running `/task`. For a plan, add the missing requirements to the plan before its first step starts, then run it: a `/sc:workflow` plan with `/sc:implement .dev/tasks/to-do/<id>/<id>.md`, a plan you wrote yourself with `/sc:implement <path to your plan file>`. If there is no spec, there is nothing to check against; read the plan yourself.

### 3.11 Review your work and open a pull request

1. **Commit locally** on your feature branch. Do not push yet.
2. **Bug review.** `/code-review`. Fix what it finds.
3. **Security review.** If you touched login, permissions, secrets, user input, or file paths: `/security-review`.
4. **Branch review.** `/sc:auggie-review --diff origin/<main branch>...HEAD --no-post-pr` (`git remote show origin | grep 'HEAD branch'` prints the main branch name). It reviews the whole branch for bugs, architecture risks, and bad patterns, and keeps results local. At the end it offers to plan fixes as a task file; accept only if you want one.
5. **Push.** Only after your lead approves.
6. **Open the PR.** You need the GitHub command-line tool (`gh`) installed and logged in.
   `/sc:pr-submit --monitor 1 --head feature/invoice-csv-export --title "Add monthly CSV export to invoices list" --body "Adds CSV export for finance month-end. Spec: docs/specs/invoice-csv-export.md. Tests: tests/invoices/test_export.py."`
   It opens the PR, waits for the automated review bot, checks each of its findings, and proposes fixes without changing your code. This needs the Augment Code review app on your repository. Without it, or if you are not sure the app is installed (the repository's Settings > GitHub Apps page lists it), use `--monitor 0`, which only opens the PR.

### 3.12 Resume after a crash or a lost session

There are two ways to resume. Use the first if you set it up; the second always works.

**1. Reopen the conversation (ccsession).** Do this before you need it: inside Claude, run `/ccsession-tag <name>` (letters, digits, `.`, `_`, `-`). Later, from a terminal in the same folder, run `ccsession <name>` to reopen that conversation. `ccsession --here` lists the names for the current folder. `superclaude install` sets this up; `~/.local/bin` must be on your `PATH`.

**2. Restart from the work's own files.** This works in a brand-new conversation.

- **A task file (`/task`).** Run `/task <path to the task file>` again. It continues from the first unchecked item. The same applies to the skills that write a task file (`/tech-research`, `/prd`, `/tdd`, `/tech-reference`, `/readme`, `/operational-guide`, `/roadmap`): run the same command with the same request, and it continues from its folder under `.dev/tasks/to-do/`.
- **A simple plan (`/sc:implement`).** Run `/sc:implement .dev/tasks/to-do/<id>/<id>.md` again. The `progress.md` file beside the plan records every finished step, and the run continues from the first unfinished one. If the folder has already moved to `.dev/tasks/done/`, the work is finished. Folders named `TASK-WF-*` are `/sc:workflow` plans: run them with `/sc:implement`, never with `/task`.
- **A brainstorm (`/sc:brainstorm`).** `/sc:brainstorm "<same topic>" --resume-from .dev/brainstorms/<timestamp>-<name>/seed-brief.md`
- **A pull request monitor (`/sc:pr-submit`).** `/sc:pr-submit --resume <repo root>/.dev/pr-monitor/pr-<PR number>-<timestamp>/monitor-run-<PR number>.jsonl` (the path must be absolute)

**You do not know what was running.** Paste this prompt: *"Run /sc-crash-recovery on this project with --since 24h. List every piece of work that was in progress, the state each one is in, and the exact command to resume each one. Do not change any files."*

`/sc:save` and `/sc:load` store and load Serena project memory. (Serena is an optional code-navigation tool; its project memory is notes it keeps between sessions.) They are not a way to resume work.

---

## 4. Rules everyone follows

- **Write it down.** Plans, research, and findings are saved to files (most under `.dev/`), not only into the chat. If the session dies, the files are what survives.
- **Let a skill finish.** Once a skill starts, let it run through all of its steps. Do not stop it halfway or skip steps.
- **Do not repeat a skill's own checks.** Task files already run reviewer panels, tests, and a final audit. Read their results instead of running the same checks again.
- **Never turn off a quality check.** Do not disable or skip a reviewer step to save time. If one seems wrong or too slow, raise it with your lead.
- **Read a plan or task file before you run it.** Make sure it matches what was agreed.
- **Never push without approval.** Commit locally, show your lead what changed, and push only when they say go.
- **Do only what was asked.** If you think something else should change, suggest it instead of doing it.
- **When unsure which tool to use,** run `/sc:recommend "<what you want to do, and why>"` or ask your lead before starting anything large.
- **A `/sc:` command whose file names a skill starts by loading that skill.** If Claude answers such a command without loading it, start a new chat and run the command again. Commands whose file names no skill (for example `/sc:help`, `/sc:explain`, `/sc:test`) run from their own file, so no skill load is expected.

Where this guide says "your lead", read "yourself" if you work alone.

---

## 5. Easy mix-ups and surprising defaults

| These look alike | The difference |
|---|---|
| `/task` and `/sc:task` | `/task` runs a task file from disk, with reviewer panels after each group of items except the first (setup) one. `/sc:task` does one job directly, with no file. |
| `/sc:workflow` + `/sc:implement` and `/task-builder` + `/task` | The first pair writes a short plan, checks it against your request, has one reviewer check each step, then runs one final independent review of the whole plan. The second pair researches the code, writes a full task file, and has a panel of reviewers check each group of items after the setup group. Use the second pair for many files, multi-session work, or anything that must not drift. |
| `/sc:design` and `/tdd` | `/sc:design` drafts one design (an API, a component, a schema) in a single pass. `/tdd` writes a full technical design document from the template, with research and independent reviewers. Use `/tdd` when other people will build against the design. |
| `/roadmap` and `/sc:roadmap` | `/roadmap` produces a roadmap plus task files you run with `/task`. `/sc:roadmap` belongs to a separate release pipeline (`/sc:tasklist`, then `superclaude sprint run`). Use `/roadmap` unless your lead says otherwise. |
| `/tech-reference` and `/sc:document` | `/tech-reference` researches a whole feature and writes a reviewed architecture document. `/sc:document` writes reference text for specific code in one pass. |
| `/tech-research` and `/sc:research` | `/tech-research` investigates our codebase. `/sc:research` searches the web. |
| `/sc:cleanup-audit` and `/sc:cleanup` | The audit only reports. Cleanup changes files. |

| Command | What it does unless you say otherwise | What to do |
|---|---|---|
| `/sc:reflect --mode post` | When you run it yourself on finished work and the audit passes, it moves the work folder to a "done" location. (The audit inside a `/task` run leaves the folder in place: the final audit runs before the task is marked done, so the folder stays in `.dev/tasks/to-do/`.) | Add `--no-promote` when you want a report only. |
| `/sc:auggie-review <PR number>` | Posts its review publicly on the PR. | Add `--no-post-pr` to keep it local. |
| `/sc:pr-submit` | With no `--monitor` setting it uses `--monitor 2` and edits your code to fix review findings. `--monitor 3` also pushes on its own. | Always pass `--monitor 1`. |
| `/tech-research` and `/roadmap` | Run at their deepest setting, with many agents, unless the request is clearly small. | For `/tech-research`, ask a narrow, specific question if you want a smaller run. For `/roadmap`, keep the full setting if you want a task file for every phase (3.1 step 7). |
| `/sc:implement` on a `/sc:workflow` plan | Moves the plan folder to `.dev/tasks/done/` when every step passes; on any system other than Linux (including macOS) it refuses on purpose and leaves the folder in `.dev/tasks/to-do/` | Nothing. Never move the folder by hand. |

---

## Other commands

These commands are installed but no workflow above routes to them.

<!-- other-commands:v1 -->

| Command | When to use it |
|---|---|
| `/sc:agent` | A general session controller. Prefer this guide's levels instead. |
| `/sc:build` | Build or package the project. |
| `/sc:cli-eval` | IronClaude contributors: write or run CLI evaluation suites. |
| `/sc:cli-portify` | IronClaude contributors: turn a skill into a CLI pipeline. |
| `/sc:git` | Commit with a generated message. Still never push without approval. |
| `/sc:help` | List the SuperClaude commands and skills installed here, show the six process levels, and point to the routing guide. |
| `/sc:index` | Build a documentation index for a project. |
| `/sc:index-repo` | Write `PROJECT_INDEX.md` and `.json` so later sessions read less. |
| `/sc:init-lite` | Check a project's Claude setup files without changing them. |
| `/sc:load` | Load Serena project memory. Not a way to resume work (3.12). |
| `/sc:pm` | Agent-coordinated work. Prefer this guide's levels instead. |
| `/sc:post-release` | After tagging a release. |
| `/sc:review-translation` | Review translated text. |
| `/sc:save` | Save Serena project memory. Not a way to resume work (3.12). |
| `/sc:spawn` | Break a large job into parts. For work that changes code, prefer `/task-builder`. |
| `/sc:tdd` | Same as `/tdd` (it invokes the same skill). Not test-driven development. |
| `/sc:validate-roadmap` | Part of the separate `/sc:roadmap` release pipeline (section 5). |
| `/sc:validate-tests` | IronClaude contributors: test `/sc:task` tier rules. |

One more user-facing skill: `/confidence-check` checks readiness before you start an implementation.

<!-- /other-commands -->

The 22 skills whose names end in `-protocol` are loaded by their `/sc:` commands and are not run directly. `sc-bare-review` is internal (used by `/sc:swarm-wizard`; its output can feed `/sc:adversarial`).

---

## Routing table

This table is read by `/sc:recommend` and checked by tests. Each row is one kind of job: its steps in order, the flags each step must carry, and where the guide explains it. Numbered steps run in order; lettered steps with the same number (3a, 3b, ...) are alternatives, so do only the one that fits. The `changes_files` column says whether following the row changes your work: `yes` means a step edits source code, docs, or git state (a commit, or a task folder moved to `done/`); `no` means it only answers, or saves a report under `.dev/`, `claudedocs/`, or the tool's own output folder.

<!-- routing-table:v1 -->

| id | intent | level | steps | mandatory_flags | changes_files | section | notes |
|---|---|---|---|---|---|---|---|
| ask | understand code; explain; how does something work; no changes wanted | 1 | 1. ask in plain English, or `/sc:explain <path>` | - | no | 1, 3.5 | - |
| small-change | one source file plus its test; five edits or fewer; exact change known | 2 | 1. `/sc:task "<change>"` or a plain edit<br>2. run the related test | - | yes | 1, 3.3 | `/sc:task` prints a `Tier:` line at the start; if it says `LIGHT` (typos, comments, formatting) or `EXEMPT` (no code change, such as explain or commit), it skipped its own checks, so run the test yourself afterwards |
| simple-plan | a few files; clear scope; one or two sessions | 3 | 1. `/sc:workflow "<what to change, why, which files>"`<br>2. read the printed plan `.dev/tasks/to-do/<id>/<id>.md` and the check result printed with it<br>3. `/sc:implement .dev/tasks/to-do/<id>/<id>.md` | 1: `--depth quick` | yes | 1, 3.3 | to resume, rerun step 3; on any system other than Linux (including macOS) the finished plan folder stays in `.dev/tasks/to-do/` and reports archive-blocked, which is expected |
| task-file | many files; more than one session; must not drift | 4 | 1. `/task-builder "<what to build, why, which code>"`<br>2. read the task file and its `reflect_pre` entry<br>3. `/task <task file>` | - | yes | 1, 3.2 | add `--spec <path>` to step 1 when a spec, PRD, or TDD exists |
| feature-existing | add a feature to an existing system; requirements clear; no PRD | 4 | 1. `/tech-research "<question, why, which code>"` (optional)<br>2. write and agree a spec file<br>3. `/task-builder "<what to build, why, which code>"`<br>4. `/task <task file>` | 3: `--spec <spec file>` | yes | 3.2 | `/sc:design <name> --type api --format spec` can draft an interface section for the spec |
| research-first | how does our system work; is it feasible; what would need to change | 5 | 1. `/tech-research "<question, why, which code>"`<br>2. `/task-builder "<what to build> as recommended in <report path>. Code: <folders>"`<br>3. `/task <task file>` | - | yes | 1, 3.5 | step 1 alone writes only a report |
| full-spec | new product; new component; major feature others build against | 6 | 1. `/sc:brainstorm "<idea>"` (only if the idea is vague)<br>2. `/prd "<request>"`<br>3. `/sc:spec-panel @<prd file>`<br>4. `/tdd "<request>"`<br>5. `/sc:spec-panel @<tdd file>`<br>6. `/sc:release-split <tdd file>` (optional)<br>7. `/roadmap "<request>"`<br>8. `/task <phase task file>` for each phase in order<br>9. read the task file's `reflect_post` entry, then follow review-pr | 3: `--mode critique --focus requirements`; 5: `--mode critique --focus architecture,testing` | yes | 3.1 | `/sc:brainstorm` uses `--depth standard` by default, so step 1 need not pass it; in step 7 ask for a full roadmap from the PRD and TDD and a dry run first; if anything changed to resolve step 9, re-confirm with `/sc:reflect --mode post --tasklist <task file> --spec <tdd file> --diff <commit before the work started> --no-promote` (row confirm-built) before the next phase |
| shape-idea | idea or requirements still unclear | - | 1. `/sc:brainstorm "<the idea, who it is for, the main constraint>"` | - | no | 3.1, 3.6 | add `--handoff task` to go straight to a task file when no PRD is needed (level 4); `--depth standard` is the default, so it need not be passed |
| bug | bug; error; stack trace; failing test | - | 1. `/sc:troubleshoot "<what happens, what you expected, how to reproduce, exact error>"`<br>2. read `.dev/troubleshoot/<name>-<timestamp>/REPORT.md`<br>3a. small fix (one source file plus its test, five edits or fewer): add a failing test, fix the code, then `/sc:test <test path>`<br>3b. a few files with clear scope: `/sc:workflow "<the fix from REPORT.md, with a test that reproduces the bug>"`, then step 4<br>3c. larger or riskier fix: accept the task-file offer, or `/task-builder "Fix the root cause described in <REPORT.md path>, with a test that reproduces the bug. Code: <folders>"` then `/task <task file>`<br>4. only after 3b: read the plan it prints, then `/sc:implement .dev/tasks/to-do/<id>/<id>.md` | 1: `--type <kind>`; 3a: `--coverage`; 3b: `--depth quick` | yes | 3.4 | kind is one of bug, test, build, performance, deployment, security; add `--fix` to step 1 only when the fix may be larger or riskier than a few files with clear scope; if the cause is not confirmed, rerun step 1 with `--depth deep` |
| external-research | library; standard; best practice outside our code | - | 1. `/sc:research "<question>"` | 1: `--depth deep` | no | 3.5 | - |
| module-health | general health of a module | - | 1. `/sc:analyze <path>` | 1: `--focus <area>` | no | 3.5 | area is one of security, quality, performance, architecture |
| compare-options | two or more designs, plans, or drafts; pick or merge | - | 1. `/sc:adversarial --compare <file a>,<file b>` | - | no | 3.6 | writes one merged document as its own output |
| critique-spec | review a spec, PRD, or TDD | - | 1. `/sc:spec-panel @<file>` | 1: `--mode critique` | no | 3.6 | - |
| business-strategy | business strategy, not code | - | 1. `/sc:business-panel @<file>` | - | no | 3.6 | - |
| multi-model-review | reviewers from other AI model families | - | 1. `/sc:swarm-wizard` | - | no | 3.6 | real runs need an OpenAI-compatible model proxy set in `~/.aienv` (T2ProxyUrl, T2ProxyKey, T2Model01); without it you get the dry run only |
| cleanup | dead code; unused imports; tidy a folder | - | 1. `/sc:cleanup-audit <path>`<br>2. commit<br>3. `/sc:cleanup <path>`<br>4. `/sc:improve <path>`<br>5. review `git diff` | 1: `--pass all`; 3: `--type code --safe --interactive`; 4: `--type quality --safe --interactive` | yes | 3.7 | for a large or structural refactor use feature-existing instead |
| tests | run tests; check coverage | - | 1. `/sc:test <path>` | 1: `--coverage` | no | 3.8 | add `--type unit`, `--type integration`, or `--type e2e` to narrow |
| document-built | technical reference; operational guide; README; API reference for existing code | - | 1. one of `/tech-reference "<request>"`, `/operational-guide "<request>"`, `/readme "<request>"`, `/sc:document <path>` | - | yes | 3.9 | for API reference use `/sc:document <path> --type api` |
| check-plan | check a plan or task file against a spec before running it | - | 1. `/sc:reflect --mode pre --spec <spec file> --tasklist <plan or task file>` | - | no | 3.10 | skip it when the task file's `reflect_pre` verdict is pass or fail; a `/sc:workflow` plan was already checked against its request when written |
| confirm-built | confirm finished work matches the plan | - | 1. `/sc:reflect --mode post --tasklist <task file> --spec <spec file> --diff <commit before the work started>` | - | yes | 3.1, 5 | give one commit, not a `..HEAD` range, so uncommitted work is audited too (`/task` does not commit); run `git add -A` first so new files are included; that commit is `HEAD` if nothing was committed since the work started, otherwise find it with `git log --oneline`; when re-confirming one roadmap phase, commit each phase once it passes and give the commit made when the previous phase passed; add `--no-promote` when you want a report only: without it a passing audit moves the work folder to its done location; when re-confirming a roadmap phase before the next one (3.1), always add `--no-promote`; inside `/task` this audit already runs, so read the `reflect_post` entry instead of running it again |
| review-pr | review the work and open a pull request | - | 1. commit locally<br>2. `/code-review`<br>3. `/security-review`<br>4. `/sc:auggie-review --diff origin/<main branch>...HEAD`<br>5. push only after approval<br>6. `/sc:pr-submit --head <branch> --title "<title>" --body "<body>"` | 4: `--no-post-pr`; 6: `--monitor 1` | yes | 3.11 | step 3 only when login, permissions, secrets, user input, or file paths changed; step 6 needs `gh` logged in and the Augment Code review app on the repository, without which use `--monitor 0` to only open the PR |
| resume | lost session; crash; continue earlier work | - | 1a. from a terminal, `ccsession <name>` if the session was tagged with `/ccsession-tag <name>`<br>1b. otherwise rerun the same command: `/task <task file>`, or `/sc:implement .dev/tasks/to-do/<id>/<id>.md`<br>1c. if you do not know what was running, paste the `/sc-crash-recovery` prompt from section 3.12 | - | yes | 3.12 | `/sc:brainstorm --resume-from <seed-brief path>` and `/sc:pr-submit --resume <repo root>/.dev/pr-monitor/pr-<PR number>-<timestamp>/monitor-run-<PR number>.jsonl` (an absolute path) also continue from on-disk state; `/sc:save` and `/sc:load` are not resume methods |
| unsure | which tool; how to start | - | 1. `/sc:recommend "<what you want to do, and why>"` | - | no | 4 | - |

<!-- /routing-table -->
