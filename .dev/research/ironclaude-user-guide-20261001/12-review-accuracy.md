# QA Report: IronClaude New-User Guide, Accuracy Lens

**Topic:** Factual accuracy of `IRONCLAUDE-NEW-USER-GUIDE.md` against IronClaude source
**Date:** 2026-10-01
**Phase:** report-validation (accuracy lens only, report-only, guide NOT edited)
**Fix cycle:** N/A
**Guide:** `/Users/cmerritt/GFxAI/IC-Harness/.dev/research/ironclaude-user-guide-20261001/IRONCLAUDE-NEW-USER-GUIDE.md`
**Source root:** `/Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/` (abbreviated `SRC/` below)

**Source-version note:** the checkout is on branch `feat/tier-tools-update` (HEAD `47d7f9be`), which is `origin/master` (`50a8c7f4`) plus 2 commits. `git diff origin/master HEAD` touches only 15 files; of the files cited in this report, only `sc-brainstorm-protocol/SKILL.md` and `sc-reflect-protocol/SKILL.md` differ, and only in model-alias lines unrelated to any guide claim. Every citation below therefore holds for current `origin/master`. The local `master` ref (`86c46321`) is stale and was not used.

---

## Overall Verdict: FAIL

8 errors found: 4 IMPORTANT, 4 MINOR. No fabricated command or flag names. Each error is a behavior description that overstates or misstates what the source does.

## Issues Found

| # | Severity | Location | Issue |
|---|----------|----------|-------|
| 1 | IMPORTANT | Section 1 level 2 row; also 2.3 step 1 | `/sc:task` does not always run tests |
| 2 | IMPORTANT | 2.4 step 1 | The 1-3 minute timing applies only to Tier 1; a default run can escalate |
| 3 | IMPORTANT | 2.1 step 9, 2.2 step 5, 2.4 step 4 | `/sc:reflect --mode post` is not given the plan, so it cannot check "built matches planned" |
| 4 | IMPORTANT | 2.7 step 2 | `--preview` is not a declared flag of `/sc:cleanup` or `/sc:improve` |
| 5 | MINOR | 2.7 step 1 | A bare `/sc:cleanup-audit` runs Pass 1 only (DELETE/REVIEW/KEEP), not consolidate/move |
| 6 | MINOR | Section 1 level 4 row; Section 4 first table | `/task` reviewer gates skip Phase 1 |
| 7 | MINOR | 2.6 swarm-wizard row | "runs it" leaves out the mandatory dry-run, the go-ahead, and the proxy prerequisite |
| 8 | MINOR | 2.1 step 6 | `/sc:release-split` also writes split release specs, not only an analysis |

### Error 1 (IMPORTANT): `/sc:task` does not always run the affected tests

- **Guide text (L14):** "or use `/sc:task \"<describe the change>\"`, which also runs the affected tests."
- **Guide text (L52, 2.3):** "`/sc:task \"<describe the change>\"`" offered as an equal alternative to "make the change and run the test".
- **Source:**
  - `SRC/skills/sc-task-protocol/SKILL.md:108-113`: LIGHT execution is "Quick scope check / Make changes / Quick sanity check / Proceed with judgment". No tests are run.
  - `SRC/skills/sc-task-protocol/SKILL.md:128`: "LIGHT | Skip verification | 0 | 0s".
  - `SRC/skills/sc-task-protocol/SKILL.md:105`: STANDARD step 4 is "Run affected tests OR document manual verification", so tests are not guaranteed there either.
  - `SRC/commands/task.md:84-87`: LIGHT keywords include typo, comment, minor, and "quick fix" / "minor change". These are exactly the small one-file changes that level 2 describes.
- **Corrected text (L14):** "or use `/sc:task \"<describe the change>\"`. For standard and strict changes it runs the affected tests (or records a manual check); trivial changes such as typos or comments skip verification, so run the related test yourself."

### Error 2 (IMPORTANT): the troubleshoot timing claim

- **Guide text (L58):** "A normal run takes 1-3 minutes."
- **Source:**
  - `SRC/commands/troubleshoot.md:51`: `--depth` default is `standard` ("auto-escalate by rubric"); "~1-3 min" is attached to `quick` (Tier 1 only).
  - `SRC/commands/troubleshoot.md:75-76`: Tier 1 is "1-3 min". Tier 2 auto-escalates on "confidence < 0.85, multi-domain, intermittent, security < 0.95" and adds "+4-15 min".
  - A default (`standard`) run is therefore 1-3 minutes only when Tier 1 is confident enough.
- **Corrected text:** "The first pass takes about 1-3 minutes. If it is not confident, or the problem is intermittent or spans several areas, it escalates automatically and takes another 4-15 minutes. Add `--depth quick` to cap it at the first pass."

### Error 3 (IMPORTANT): post-execution reflect is not given the plan

- **Guide text (L36, 2.1 step 9):** "`/sc:reflect --mode post --diff <commit or branch> --no-promote`, which independently checks that what was built matches what was planned."
- **The same command, without the plan, also appears at:** L48 (2.2 step 5) and L63 (2.4 step 4).
- **Source:**
  - `SRC/commands/reflect.md:84`: `--tasklist` is "**Strongly recommended for UC-2**".
  - `SRC/commands/reflect.md:83`: `--spec` is "Recommended for UC-2".
  - `SRC/skills/sc-reflect-protocol/SKILL.md:527` and `refs/ops-integration.md:198-203`: when neither `--spec` nor `--tasklist` is supplied, the reachability gate is skipped (`spec-and-tasklist-absent`, a "Telemetry-only legacy path").
  - `SRC/skills/sc-reflect-protocol/SKILL.md:1522`: the promotion gate also reads the tasklist frontmatter.
  - Without the plan, the audit has no "planned" reference to compare against.
- **Corrected text (2.1 step 9; apply the same change at 2.2 step 5 and 2.4 step 4):** "Run the tests, then `/sc:reflect --mode post --diff <commit or branch> --spec <path to TDD or spec> --tasklist <path to the phase's task file> --no-promote`, which independently checks that what was built matches what was planned."

### Error 4 (IMPORTANT): `--preview` is not a declared flag

- **Guide text (L87):** "preview first, then apply. `/sc:cleanup <path> --preview` removes dead code and unused imports; `/sc:improve <path> --type quality --preview` improves code quality. Run each again without `--preview` once the preview looks right."
- **Source:**
  - `SRC/commands/cleanup.md:22`: the usage line is `[--type code|imports|files|all] [--safe|--aggressive] [--interactive]`. It has no `--preview`.
  - `SRC/commands/improve.md:22`: the usage line is `[--type quality|performance|maintainability|style] [--safe] [--interactive]`. It has no `--preview`.
  - `--preview` appears only inside one example comment in each file (`cleanup.md:73`, `improve.md:81`). It is absent from `SRC/core/FLAGS.md` (grep across `core/` and `commands/` returned only those two example lines).
  - `SRC/commands/cleanup.md:110-115`: unused imports and zero-reference dead code are "Auto-fix (applies automatically)".
  - `SRC/commands/improve.md:110-115`: style fixes, unused variables, and import organization are auto-applied.
  - A user who relies on an undeclared preview flag may get changes applied immediately.
- **Corrected text:** "Small, contained cleanups: commit first so you can revert, then run `/sc:cleanup <path> --safe --interactive` to remove dead code and unused imports, or `/sc:improve <path> --type quality --safe --interactive` to improve code quality. `--interactive` asks before complex changes. Unused imports and code with zero references are removed automatically even then, so review the diff before committing."

### Error 5 (MINOR): a bare `/sc:cleanup-audit` does not produce a consolidate/move report

- **Guide text (L86):** "`/sc:cleanup-audit` produces an evidence-backed report of files to delete, consolidate, move, or keep. It changes nothing."
- **Source:**
  - `SRC/commands/cleanup-audit.md:50-53`: a bare `/sc:cleanup-audit` "Runs Pass 1 surface scan ... classify every file as DELETE/REVIEW/KEEP".
  - `SRC/commands/cleanup-audit.md:43,74-77`: consolidation needs Pass 3 (cross-cutting duplication), and the full classification needs `--pass all`.
  - `SRC/commands/cleanup-audit.md:43`: reports go to `.claude-audit/`, not `.dev/`.
  - The "changes nothing" part is correct (`cleanup-audit.md:97,103`).
- **Corrected text:** "`/sc:cleanup-audit --pass all` produces an evidence-backed report (under `.claude-audit/`) of files to delete, consolidate, move, or keep. Without `--pass all` it runs only the first, quick pass (delete / review / keep). It changes nothing."

### Error 6 (MINOR): `/task` reviewer gates do not run at every phase

- **Guide text (L16):** "with independent reviewer agents checking the work at each phase."
- **Guide text (L144):** "`/task` runs a task file from disk with reviewer checks at each phase."
- **Source:**
  - `SRC/skills/task/SKILL.md:188`: "QA verification is mandatory for every phase except Phase 1 (which is setup-only ...)".
  - `SRC/skills/task/SKILL.md:282`: "phase-gate verification on Phase 2+".
  - `SRC/skills/task/SKILL.md:286`: a separate post-completion validation runs before Done.
- **Corrected text (L16):** "with independent reviewer agents checking the work after every phase except the setup phase, plus a final validation before it is marked done."
- **Corrected text (L144):** "`/task` runs a task file from disk with reviewer checks after each working phase."

### Error 7 (MINOR): swarm-wizard "runs it" omits its required steps

- **Guide text (L81):** "`/sc:swarm-wizard`. It asks what you want reviewed, picks the settings, and runs it."
- **Source:**
  - `SRC/commands/swarm-wizard.md:52,84-87`: a "safe stub dry-run still runs first". It will not "launch a real-model run without an explicit user go-ahead and a passing dry-run".
  - `SRC/skills/sc-swarm-wizard-protocol/SKILL.md:59-60,193`: a real run needs the T2 proxy environment (`T2ProxyUrl` / `T2ProxyKey` / `T2Model01`) set in `~/.aienv`. Otherwise it falls back to offering a stub run.
- **Corrected text:** "`/sc:swarm-wizard`. It asks what you want reviewed, picks the settings, proves them with a safe dry run, and launches the real review only after you say go. Real runs need the model proxy set up in `~/.aienv` (ask your lead)."

### Error 8 (MINOR): `/sc:release-split` does more than analyze

- **Guide text (L33):** "`/sc:release-split <path to spec>` analyzes whether and where to split it."
- **Source:**
  - `SRC/commands/release-split.md:64` describes a "4-part sequential protocol": Part 3 is "execution ... produce release specs or tasklists" and Part 4 is fidelity verification. It "Produces 4-6 artifacts".
  - `SRC/commands/release-split.md:53`: the default output is `<spec-dir>/release-split/`.
  - The input form `<spec-file-path>` is correct (`release-split.md:19,52`).
- **Corrected text:** "`/sc:release-split <path to spec>` analyzes whether and where to split it. If a split is warranted, it writes the split release specs (into a `release-split/` folder next to the spec) and checks them against the original. \"Do not split\" is a valid result."

## Claims Verified Correct

| Guide claim (line) | Evidence |
|---|---|
| `/sc:explain <file or function>` exists (L13, L72) | `SRC/commands/explain.md:22` `/sc:explain [target] ...` |
| `/sc:workflow ... --depth quick` writes a plan in which every step has acceptance criteria (L15) | `SRC/commands/workflow.md:29,40`; `SRC/skills/sc-workflow-protocol/refs/quality-gates.md:18-22` (quick gate: "every Task has `Acceptance criteria:`") |
| Plan path `.dev/workflow/<name>/plan.md` (L15) | `SRC/commands/workflow.md:41,67` |
| `/sc:implement @<plan.md>` checks each step against its criteria; resumable with `--resume` (L15, L126) | `SRC/commands/implement.md:11,44,57`; `@plan.md` form recommended at `SRC/commands/workflow.md:82` |
| `--handoff implement` plans and then builds (L53) | `SRC/commands/workflow.md:42`; `SRC/skills/sc-workflow-protocol/refs/overlap-routing.md:5` |
| `/task-builder` researches the codebase and writes a task file under `.dev/tasks/` (L16) | `SRC/skills/task-builder/SKILL.md:8,10,25` |
| `/task` resumes from the first unchecked item; task files are under `.dev/tasks/to-do/` (L125) | `SRC/skills/task/SKILL.md:10,21,531-533,636` |
| `/tech-research` produces findings, options, and an implementation plan, using the codebase and the web (L17, L69) | `SRC/skills/tech-research/SKILL.md:3,97-103` |
| `/tdd "Create a TDD for <component> from <path to PRD>"` takes a PRD this way (L31) | `SRC/skills/tdd/SKILL.md:44,177,183,210` (PRD_REF extracted from the request) |
| TDD covers architecture, data, interfaces, testing, migration (L31) | `SRC/examples/tdd_template.md:362,426,472,857,986` |
| `/roadmap` accepts a PRD and a TDD and, at Deep tier, writes a roadmap, one BUILD_REQUEST per phase, and one task file per phase (L34, L18) | `SRC/skills/roadmap/SKILL.md:8,60,71,102-108,240` |
| `/sc:spec-panel @file --mode critique --focus requirements` and `architecture,testing` (L30, L32, L80) | `SRC/commands/spec-panel.md:22,119,129,140,151,398,418` |
| `/sc:brainstorm` uses questions, parallel proposals, and a merge; `--handoff task` invokes task-builder (L28, L78) | `SRC/commands/brainstorm.md:39,60,175`; `SRC/skills/sc-brainstorm-protocol/SKILL.md:329` |
| `/sc:troubleshoot --type bug/test/build/performance/deployment`, `--depth deep`, `--fix` (L58, L62) | `SRC/commands/troubleshoot.md:8,50-54` |
| Troubleshoot report in `.dev/troubleshoot/`, changes nothing by default (L58-59) | `SRC/commands/troubleshoot.md:56,191` |
| Troubleshoot reports whether the fix belongs in the code, the test, or the docs (L59) | `SRC/skills/sc-troubleshoot-protocol/SKILL.md:75` (`remediation_target` enum `test\|code\|docs\|none`) |
| `--fix` offers a task file after a successful diagnosis; the user runs `/task` (L62) | `SRC/commands/troubleshoot.md:54,170,192` |
| `/sc:analyze --focus quality\|security\|performance\|architecture`, report only (L71) | `SRC/commands/analyze.md:22,100` |
| `/sc:research` is web research (L70, L147) | `SRC/commands/research.md:3,25` |
| `/sc:test <path> --coverage`, `--type unit\|integration\|e2e`; does not write tests (L92-93) | `SRC/commands/test.md:22,104` |
| `/sc:adversarial --compare a,b` debates, scores, and merges (L79) | `SRC/commands/adversarial.md:23,58,76` |
| `/sc:business-panel @<document>` (L82) | `SRC/commands/business-panel.md:50` |
| `/sc:design "<component>"` (L45) | `SRC/commands/design.md:22` |
| `/sc:document <path>` (L104) | `SRC/commands/document.md:22` |
| `/sc:reflect --mode pre --spec --tasklist` lists missed requirements (L109) | `SRC/commands/reflect.md:27,41,84` |
| `/sc:reflect --mode post` promotes (moves the folder to done) unless `--no-promote` (L151) | `SRC/commands/reflect.md:103`; `SRC/skills/sc-reflect-protocol/SKILL.md:95` (promotes only when the strict gate passes, default on) |
| `/sc:auggie-review --diff origin/<main>...HEAD --no-post-pr`; it posts to a PR by default (L117, L152) | `SRC/commands/auggie-review.md:8,28,50-51,107` |
| `/sc:pr-submit --monitor 1 --head --title --body`: opens the PR, polls the review bot, verifies findings, proposes fixes, no edits (L119) | `SRC/commands/pr-submit.md:8,27,37,85` |
| `/sc:pr-submit` defaults to level 2 (local fixes, stops before push); level 3 pushes (L153) | `SRC/commands/pr-submit.md:26,38-39,47` |
| `/sc:pr-submit --resume <run log>` (L127) | `SRC/commands/pr-submit.md:40,56` |
| Crash recovery: the `sc-crash-recovery` skill exists, installs as a standalone skill, accepts `--since 24h`, and is read-only (L128) | `SRC/skills/sc-crash-recovery/SKILL.md:13,26,95,155`; `SRC/cli/install_skills.py:7-11,52-57` (no `commands/crash-recovery.md`, so the skill is installed) |
| "security, auth, database, migration, or refactor" switch `/sc:task` to strict mode automatically (L52) | `SRC/commands/task.md:73-77` (keywords security/database/migration/refactor; "minor auth change → still STRICT"; `auth/` path booster) |
| `/sc:roadmap` belongs to a separate pipeline (`/sc:tasklist`, then `superclaude sprint run`) (L145) | `SRC/commands/roadmap.md:3` (mirrors `superclaude roadmap run`), `:103`; `SRC/commands/tasklist.md:18,118` |
| `/sc:cleanup-audit` changes nothing; `/sc:cleanup` changes files (L146) | `SRC/commands/cleanup-audit.md:97,103`; `SRC/commands/cleanup.md:29,110` |
| `/tech-research` and `/roadmap` default to their deepest tier (L154) | `SRC/skills/tech-research/SKILL.md:97,106`; `SRC/skills/roadmap/SKILL.md:102,111` |
| `/sc:recommend "<goal>"` (L138) | `SRC/commands/recommend.md:8,24` |
| `/prd`, `/tdd`, `/roadmap`, `/task`, `/task-builder`, `/tech-research`, `/tech-reference`, `/operational-guide`, `/readme` exist as skills (throughout) | frontmatter `name:` in each `SRC/skills/<name>/SKILL.md` (checked all 9) |

**Not verifiable against IronClaude source (out of scope, not errors):** `/code-review` and `/security-review` (L54, L115-116) are Claude Code built-ins, not IronClaude files. The "Two hard limits" sentence (L20) and the Section 3 rules are team policy, not product behavior.

## Summary

- Checks performed: 46 claim groups (38 verified correct, 8 errors)
- Critical issues: 0; IMPORTANT: 4; MINOR: 4
- Issues fixed in-place: 0 (report-only by instruction)
- **Confidence:** Verified: 46/46 | Unverifiable: 0 (built-in commands and team policy are excluded from scope rather than counted) | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 1 | Grep: 0 (dedicated tool) | Glob: 0 | Bash: 30 (sed/grep/git reads of source files, all read-only). Bash was used for source reads because the source sits in a sibling repository and the session runs in bypass mode. tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0.

## Recommendations

- Apply the 8 corrected replacement texts above. Errors 1-4 change what a new user will actually experience, so fix them before the guide is distributed.
- Re-run this accuracy lens after the fixes are applied (fix-cycle 1).

## QA Complete

