# QA Report: IronClaude New-User Guide, Accuracy Lens Re-Review (Fix Cycle 1)

**Topic:** Factual accuracy of the rewritten `IRONCLAUDE-NEW-USER-GUIDE.md` against IronClaude source
**Date:** 2026-10-02
**Phase:** fix-cycle (accuracy lens only, adversarial, report-only, guide NOT edited)
**Fix cycle:** 1
**Guide:** `/Users/cmerritt/GFxAI/IC-Harness/.dev/research/ironclaude-user-guide-20261001/IRONCLAUDE-NEW-USER-GUIDE.md` (240 lines, workflows now numbered 3.x)
**Prior report:** `/Users/cmerritt/GFxAI/IC-Harness/.dev/research/ironclaude-user-guide-20261001/12-review-accuracy.md`
**Source root:** `/Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/` (abbreviated `SRC/`), HEAD `47d7f9be` (same checkout as the prior review)

---

## Overall Verdict: FAIL

Prior errors: 7 of 8 resolved; Error 6 is only partly fixed (two lines still say "each/every phase"). The rewrite adds 8 new accuracy errors: 1 IMPORTANT, 7 MINOR. The IMPORTANT one is new: the guide says a passed task folder moves to `.dev/tasks/done/` on its own at the end of `/task`. The source's promotion gate blocks that move inside `/task`, and real reflect runs on disk confirm the block.

**Monotonicity note (Retry Monotonicity Protocol):** cycle 0 had |F|=8. Cycle 1 has |F|=9 (1 persisting + 8 new). The count did not shrink, so: `[HALT-MONOTONICITY] |F|=9`. The cause is not fixes failing. 7 of 8 fixes landed, and every new finding is about text added in the rewrite. Whether to run another cycle is the orchestrator's or the user's call.

## Part 1: Prior Errors 1-8

| # | Prior error | Status | New guide text (quoted) | Evidence |
|---|---|---|---|---|
| 1 | `/sc:task` does not always run tests | RESOLVED | L14: "For normal and risky changes `/sc:task` runs the affected tests itself; for trivial ones (typos, comments) it skips checking, so run the test yourself." L115: "Run the tests yourself only if nothing ran them: a plain edit, or a trivial `/sc:task` change." | `SRC/skills/sc-task-protocol/SKILL.md:126-129` (STRICT sub-agent, STANDARD "Direct test execution", LIGHT "Skip verification"); `:105` STANDARD step 4 also allows "document manual verification", but the verification table at `:127` supports the wording |
| 2 | Troubleshoot timing | RESOLVED | L121: "A simple bug takes 1-3 minutes. If it is not confident, or the problem is intermittent or spans several areas, it automatically brings in more agents, which can take another 4-15 minutes. `--depth quick` stops it after the first pass; `--depth deep` goes straight to several agents testing competing explanations." | `SRC/commands/troubleshoot.md:51,75-76` |
| 3 | Post reflect not given the plan | RESOLVED (restructured) | Users no longer run `/sc:reflect --mode post` by hand. L77: "as its last steps, an independent audit (`/sc:reflect`) comparing what was built with the plan." | `SRC/skills/task-builder/SKILL.md:2223`: the generated POST item passes `--tasklist {TASK_FILE} [--spec {SPEC_PATH}]`. The restructure added new Error N1 (below). |
| 4 | `--preview` not a declared flag | RESOLVED | L158-160: "`/sc:cleanup src/billing/ --type code --safe --interactive` ... `/sc:improve src/billing/ --type quality --safe --interactive` ... `--interactive` asks before complex changes, but unused imports and code nothing references are removed automatically even then." | `SRC/commands/cleanup.md:22,110-115`; `SRC/commands/improve.md:22`. The sentence is still wrong for `/sc:improve`: see N6. |
| 5 | Bare cleanup-audit is Pass 1 only | RESOLVED | L154-155: "`/sc:cleanup-audit src/billing/ --pass all` ... (under `.claude-audit/`) ... Without `--pass all` it runs only its quick first pass (delete, review, or keep)." | `SRC/commands/cleanup-audit.md:31,35-36,50-53` |
| 6 | Reviewer gates skip Phase 1 | **STILL FAILING (partial)** | Fixed at L16 ("After every working phase") and L226 ("after each working phase"). **Still wrong** at L77: "reviewer panels after each phase", and L227: "has a panel of reviewers check every phase." | `SRC/skills/task/SKILL.md:188` ("mandatory for every phase except Phase 1"), `:282` ("Phase 2+") |
| 7 | swarm-wizard omits dry run / go-ahead / proxy | RESOLVED | L148: "proves them with a safe dry run, and launches the real review only after you say go. Real runs need the model proxy configured; ask your lead." | `SRC/commands/swarm-wizard.md:52,84-87`; `SRC/skills/sc-swarm-wizard-protocol/SKILL.md:59-60` |
| 8 | release-split does more than analyze | RESOLVED | L68: "It writes its analysis to `docs/billing/release-split/`. \"Do not split\" is a normal answer. If it recommends a split, it writes a separate spec for each release" | `SRC/commands/release-split.md:53` (default `<spec-dir>/release-split/`), `:64` (Part 3 produces release specs) |

**Remaining fix for Error 6:**
- L77: replace "reviewer panels after each phase" with "reviewer panels after each working phase".
- L227: replace "has a panel of reviewers check every phase" with "has a panel of reviewers check every working phase".

## Part 2: New Errors in the Rewritten Guide

| # | Severity | Location | Issue |
|---|---|---|---|
| N1 | IMPORTANT | L79, L202, L236 | Inside `/task`, a passed task folder does NOT move to `.dev/tasks/done/` on its own |
| N2 | MINOR | L98 | Missed requirements reach Open Questions only when coverage is below 90%; `--spec` is not the only trigger |
| N3 | MINOR | L15 | The `/sc:implement` progress folder is not `.dev/implement/<plan name>/` |
| N4 | MINOR | L113 | The `E-HALT-QA` stop message does not show the ruling-line format |
| N5 | MINOR | L26 | Skills do not stop when items 2-4 are missing; only a vague request (no clear "what") stops them |
| N6 | MINOR | L160 | `/sc:improve` auto-applies different changes (formatting, naming, unused variables, import order) |
| N7 | MINOR | L122 | The `--fix` task-file offer comes only after a successful diagnosis |
| N8 | MINOR (unverified claim) | L182 | Roadmap phase task files may carry `reflect_pre: skipped`; their spec check sits in the roadmap's own QA reports |

### N1 (IMPORTANT): a passed task folder is not moved to `done/` during `/task`

- **Guide text:**
  - L79: "A passed task folder moves from `.dev/tasks/to-do/` to `.dev/tasks/done/`."
  - L202: "Unfinished task files are under `.dev/tasks/to-do/`; finished ones move to `.dev/tasks/done/`."
  - L236: "Inside `/task` this is expected: a passed task folder moves to `.dev/tasks/done/`."
- **Source:**
  - `SRC/skills/task-builder/SKILL.md:2310`: the POST reflect item is "positioned penultimate (immediately before Update-status-to-Done)". `:2233`: "THEN the Update-status-to-Done item proceeds." So reflect runs while its own item and the status item are still unchecked, and the status is still Doing.
  - `SRC/skills/sc-reflect-protocol/SKILL.md:1519`: promotion condition 3 is "`tasklist_completion_pct == 1.0` (every checklist item independently verified done)". `:1523`, condition 5b: "`status: done` ... MUST be declared. Any other value (including `in-progress` ...) fails 5b." No exception exists for reflect's own gate item: grep over `sc-reflect-protocol/` and `cli/reflect/` for an exclusion found none.
  - `SRC/skills/task/SKILL.md`: grep for `tasks/done`, `move.*done`, and `mv ` found no step that moves the folder. `/task` never moves it.
  - Empirical: `/Users/cmerritt/GFxAI/IronClaude-tier-tools/.dev/tasks/done/TASK-RF-per-phase-turn-budget-20260618-160752/reflect/post/33cc85abb962/return-contract.yaml:84` says "`promotion_skip_reason: gate-failed   # conditions 3 (completion 0.957 != 1.0) and 5b (frontmatter \"Doing\" != done) fail`". `.../TASK-RF-ensemble-adversarial-seam-20260621-135420/reflect/post/513e33739a4a/return-contract.yaml:88` records the same: "`PC.4 (this gate) + PC.5 (mark-done) pending BY DESIGN`". Every `return-contract.yaml` found under `done/*/reflect/post/` has `promotion_action: skipped`, so those folders were moved some other way.
  - A standalone `/sc:reflect --mode post`, run after the task is marked Done, does promote (`SRC/commands/reflect.md:103`). Only the "inside `/task`" claim is wrong.
- **Impact:** a new user who waits for the folder to move, or treats a folder still in `to-do/` as a failure, is misled. Section 3.12 also tells users finished work will be found in `done/`.
- **Replacement text:**
  - L79: "Open the task file and read the `reflect_post` entry at the top: the audit's verdict and the path to its report. Any problems the audit could not fix are added to the task file's Open Questions; resolve them before the next phase. The task folder stays in `.dev/tasks/to-do/` when `/task` finishes; moving it to `.dev/tasks/done/` is a separate step (ask your lead how your team does it)."
  - L202: "Run `/task <path to the task file>` again. It continues from the first unchecked item. Task files live under `.dev/tasks/to-do/` (and under `.dev/tasks/done/` once someone has moved them there)."
  - L236 (row `/sc:reflect --mode post`): "When you run it yourself on finished work, it moves the work folder to a \"done\" location if the audit passes. (Inside `/task` it does not move anything, because the task is not yet marked done when the audit runs.)" What to do: "Add `--no-promote` when you run `/sc:reflect` yourself and want a report only."
