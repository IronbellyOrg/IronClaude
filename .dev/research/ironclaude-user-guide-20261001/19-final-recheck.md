# QA Report: Fix Verification (Final Recheck of 6 Edits)

**Topic:** IronClaude new-user guide, recent fix edits
**Date:** 2026-10-02
**Phase:** fix-cycle (targeted, adversarial, report-only; guide NOT edited)
**Guide:** `IRONCLAUDE-NEW-USER-GUIDE.md`
**Source root (SRC):** `/Users/cmerritt/GFxAI/IronClaude-tier-tools/src/superclaude/`

---

## Overall Verdict: FAIL

One edit (item 5, the new `/operational-guide` resume row) is factually wrong against source and contradicts the guide's own resume rule for sibling skills. The other five checks pass.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | 3.4 step 1 (guide L121): "`--depth deep` always brings in several agents testing competing explanations after that first pass." | PASS | `SRC/commands/troubleshoot.md:51` "`deep` (force Tier 2 with adversarial debate)"; `:76` Tier 2 = "2-4 specialist agents fan out in parallel; each produces a hypothesis card"; `:177` Tier 1 still runs first; `SRC/skills/sc-troubleshoot-protocol/SKILL.md:330` "`--depth deep` -> ALWAYS escalate to Tier 2", `:598` Tier 1 runs first and feeds Tier 2. "Several" matches 2-4; "after that first pass" matches. |
| 2 | Section 5 row (guide L231): "check each group of items after the setup group" | PASS | `SRC/skills/task/SKILL.md:188` "QA verification is mandatory for every phase except Phase 1 (which is setup-only ...)"; `:117` gate is minimum 6 agents (panel) per phase, Phase 2+. |
| 3 | 3.7 step 2 (guide L161) `/sc:cleanup` auto-fix list | PASS | `SRC/commands/cleanup.md:110-115` Auto-fix: unused imports, dead code with zero references, empty blocks, redundant type annotations. Exact 4-item match. `/sc:improve` half also matches `SRC/commands/improve.md:110-115` (formatting/naming, unused variables, import organization, simple type annotations). |
| 4 | 3.9 `/operational-guide` (L177) and `/readme` (L178) examples now carry Output paths | PASS | Output location is mandatory input: `SRC/skills/operational-guide/SKILL.md:61`, `SRC/skills/readme/SKILL.md:61`. README lives at module root (`readme/SKILL.md:61`, `:146` "Final README `[module-dir]/README.md`"): `src/billing/README.md` conforms. Ops guide user-specified path is allowed (convention applies only "if not specified", `operational-guide/SKILL.md:98`). |
| 5 | 3.12 (guide L206-207): `/readme` added to rerun-to-resume row; new `/operational-guide` row says it does not resume | **FAIL** | `/readme` part correct: `readme/SKILL.md:194` and A.1 `:200-210`. Folder naming correct: `operational-guide/SKILL.md:37,140` `TASK-OPSGUIDE-<subject>-YYYYMMDD-HHMMSS`. But the "does not resume; starts a new folder each time" claim is false: see Issue 1. |
| 6 | 3.10 last sentence (guide L188) | PASS | `/sc:implement` takes a path to a tasklist/notes (`SRC/commands/implement.md:6,32`); `@<plan.md>` form matches guide L15. Reflect output dir `.dev/reflect/<mode>-<slug>-<ts>/` (`SRC/skills/sc-reflect-protocol/SKILL.md:87`) matches `pre-<name>-<timestamp>`. Sentence sits in the "skipped / unchecked" bullet, so no conflict with the pass/fail bullet's "Do not run the check again". |
| 7 | Whole-guide scan for U+2014 / U+2013 | PASS | `grep -cP '[\x{2013}\x{2014}]'` on the guide returned 0. |

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Guide 3.12, L207 | Quoted: "An operational guide (`/operational-guide`) \| Do not run it again; it starts a new folder each time. Find its task file under `.dev/tasks/to-do/TASK-OPSGUIDE-<subject>-<timestamp>/` and run `/task <path to that task file>`." `/operational-guide` resumes on rerun exactly like `/readme`. | See below. |

**Issue 1 evidence:**
- `SRC/skills/operational-guide/SKILL.md:188`: "If a task file already exists for this procedure (from a previous session), skip Stage A and invoke `/task` with the existing task file path to resume from the first unchecked item." (Same sentence as `readme/SKILL.md:194`.)
- `SRC/skills/operational-guide/SKILL.md:194-200` (A.1 Check for Existing Task File): looks in `.dev/tasks/to-do/` for a `TASK-OPSGUIDE-*/` folder, and "If unchecked items exist -> skip to Stage B (resume execution)". Identical structure to `readme/SKILL.md:200-206`.
- `SRC/skills/operational-guide/SKILL.md:1649-1652`: session resume checks for `TASK-OPSGUIDE-*/` and invokes `/task`.
- The rationale used by `18-final-qa-part2.md:61` ("Each invocation creates a self-contained folder", `operational-guide/SKILL.md:136`) does not distinguish it: the same wording is in `readme/SKILL.md:33` ("Every skill invocation creates a self-contained folder") and `tech-research/SKILL.md:35`, both of which the guide (correctly) lists as resume-by-rerun. The prior finding missed A.1 at `:194`.
- Internal contradiction: L206 says document skills resume by rerun; L207 singles out a document skill with the identical mechanism as the exception.

**Replacement:**
- L206: change the skill list to "(`/tech-research`, `/prd`, `/tdd`, `/tech-reference`, `/readme`, `/operational-guide`, `/roadmap`)".
- **Proposed removal (user adjudicates):** delete row L207 (the `/operational-guide` "Do not run it again" row). Why: it is false per `operational-guide/SKILL.md:188,194-200` and is fully covered once `/operational-guide` joins the L206 row. If the author prefers to keep a direct fallback, replace L207 instead of deleting it with: "| Any of the above, if rerunning does not pick it up | Find its task file under `.dev/tasks/to-do/TASK-<TYPE>-<subject>-<timestamp>/` and run `/task <path to that task file>`. |"

## Summary
- Checks passed: 6 / 7
- Checks failed: 1
- Critical issues: 0; Important: 1
- Issues fixed in-place: 0 (report-only by instruction)

## Confidence
- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 0 | Grep: 0 | Glob: 0 | Bash: 10 (grep/sed reads of guide and SRC files; each mapped to a specific check) | Write: 1 | Edit: 3. No web research.

## Recommendations
- Apply the Issue 1 replacement (and adjudicate the L207 removal), then this recheck item can be closed without another full QA round; only L206-207 need re-verification.

## QA Complete
