# QA Report — Task Integrity Validation

**Task File:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260522-151622/TASK-RF-20260522-151622.md`
**Template:** 02 (complex task)
**Date:** 2026-05-22
**Phase:** task-integrity
**Fix cycle:** 1
**Stance:** ADVERSARIAL — assume errors exist, find them
**Fix authorization:** TRUE

---

## Overall Verdict: **FAIL**

One critical unfixable issue (fabricated downstream flag) + one critical drift issue (fixed in-place during this pass).

---

## Confidence Gate

- **Verified:** 26/26 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: 5 | Glob: 0 | Bash: 5

All 26 checks (1-9 template, 10-17 TB-Add, A-H task-specific) verified with direct tool calls against the task file, source-of-truth files, and the sc:adversarial command surface.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Frontmatter schema complete | PASS | Read L1-44: all mandatory fields (id, title, status, type, priority, created_date, updated_date, related_docs, tags, template_schema_doc) present and well-formed |
| 2 | Mandatory template 02 sections present | PASS | Title (L46), Task Overview (L48), Key Objectives (L54), Prerequisites & Dependencies (L67), Execution Context (L74), Phase 1-12 (L84+), Task Log / Notes (L971) |
| 3 | Checklist items self-contained (B2 6-element) | PASS | Spot-checked Phase 1.1, 2.1, 3.1, 5.2, 6.3, 9.2, 11.2 — all have Goal/Context/Action/Output/Verification/Completion gate inline |
| 4 | Granularity per file | PASS | troubleshoot.md=5 items (4 edits + 1 gate), SKILL.md=19 items across Phase 4-7, hypothesis-card=2, report-template=5, doc-discovery=2 — matches expectations |
| 5 | Evidence-based (file paths + line numbers) | PASS | Every edit item cites a specific file path AND a specific line range; Phase 1 baseline-snapshot lines mirror per-anchor lines from research file 01 |
| 6 | No items based on [CODE-CONTRADICTED]/[UNVERIFIED] | PASS | Cross-checked against research-gate report (PASS verdict) — no unverified content |
| 7 | Open Questions documented | PASS | Open Questions section present at L1043, explicitly empty (BUILD_REQUEST locked all 5 placement decisions) |
| 8 | Phase dependencies logical | PASS | Phase 1 (prep) → Phase 2-9 (edits) → Phase 10 (sync) → Phase 11 (QA) → Phase 12 (completion); no circular |
| 9 | Item count reasonable | PASS | 45 items across 12 phases for a 5-file edit + 1 new file + sync + QA + completion task |
| 10 | TB-Add-1: Placeholder scan | PASS | grep returned no `TBD`/`TODO`/`FIXME` in item bodies; every item has Context+Action+Output+Verification+Completion |
| 11 | TB-Add-2: Item count bounds (advisory) | PASS | 45 within >=3 and <=50 single-track bounds |
| 12 | TB-Add-3: Clarification adjacency | N/A | No Open Questions exist |
| 13 | TB-Add-4: Circular dependency (DAG) | PASS | Item-to-item deps form a strict DAG via phase order |
| 14 | TB-Add-5: Granularity / XL splitting | PASS | refs/doc-discovery.md Write is a single-item creation (appropriate for new file); all other items per-anchor split |
| 15 | TB-Add-6: Verification format consistency | PASS | Every item has a "Pass criteria" / verification clause; tail-pattern "Once done, mark this item as complete" used uniformly |
| 16 | TB-Add-7: Execution Context source areas reappear; no file:line in block | PASS | Source areas "sc:troubleshoot command surface", "sc-troubleshoot-protocol skill body", "troubleshoot protocol refs subsystem" all reappear in per-item Contexts; awk-bounded grep on Execution Context block returned 0 file:line citations |
| 17 | TB-Add-8: Per-item Context evidence binding | PASS | Every item Context cites specific file paths and line ranges (e.g., L106-107, L141-145, L162-170, L228-239, L353-354, L380-381) |
| A | Verbatim old_string/new_string blocks | PARTIAL FAIL -> FIXED | Step 9.2 had paraphrased placeholder `<2-4 sentence executive summary...>` that did NOT match actual file content (lines 23-29 are real prose). FIXED in-place: old_string now matches actual file verbatim. Other sampled edits (Step 2.1/2.3/2.4 -> troubleshoot.md L56-57/L162-163/L170-171; Step 4.2 -> SKILL.md L49-51; Step 4.4 -> SKILL.md L65-67; Step 5.2 -> SKILL.md L143-147; Step 6.1 -> SKILL.md L137; Step 7.4 -> SKILL.md L314; Step 7.5 -> troubleshoot.md L85; Step 8.1 -> hypothesis-card-template.md L15-17; Step 9.1 -> report-template.md L16-18; Step 9.4 -> report-template.md L102-106) all confirmed verbatim against source files |
| B | R-039 hidden-input scan on Execution Context block | PASS | awk-bounded extraction of `## Execution Context` ... `---` block, then `grep -cE "src/\|/.*:[0-9]+"` returned 0 — no file paths in the header rollup |
| C | Decision 4 (Context7 ripple = false positive) | PASS | Only two mentions of L87/L95/L316 in task file are explicit "Do NOT modify" warnings (Phase 2 preamble L102, Step 7.4 reminder L741, Step 7.5 reminder L757). No item modifies these lines |
| D | The 5 placement decisions realised | PARTIAL | Decision 1: PASS Documentation Context inserted BETWEEN Summary and Diagnosis (Step 9.2 post-fix). Decision 2: PASS Consistency with docs added as top-metadata-block field sibling to Cause class (Step 8.1). Decision 3: PASS refs/doc-discovery.md has exactly 4 enumerated sections (Step 3.1). Decision 4: PASS Context7 lines untouched (check C). Decision 5: PASS 12-phase canonical structure mirrored (Prep -> per-anchor edits -> Sync -> FINAL QA -> Completion) |
| E | Sync workflow correctness | PASS | Phase 10 Step 10.1 runs `make sync-dev` FIRST; Step 10.2 runs `make verify-sync` AFTER. Correct order |
| F | PROHIBITED constraint — no new flags beyond --no-doc-discovery | FAIL — UNFIXABLE | Step 6.3 introduces `--context-file <output-dir>/doc-context.md` to the sc:adversarial-protocol invocation. `--context-file` is NOT a recognized flag for sc:adversarial (verified by reading adversarial.md flag table — only `--compare`, `--source`, `--generate`, `--agents`, `--pipeline*`, `--depth`, `--convergence`, `--interactive`, `--output`, `--focus`, `--blind`, `--auto-stop-plateau` are valid). This is either (a) inline fabrication of a new flag violating the constraint, or (b) hallucination that will fail at execution. Requires task-builder redesign — fix would be to embed the doc-context-card content directly in the compare fix-proposal artifacts, or convey via Skill brief prose, NOT a new flag |
| G | No protocol reimplementation inline | PASS | Wave 4 adversarial reference uses Skill hand-off (`Skill sc:adversarial-protocol with --compare ...`), not inline debate logic; Wave 6 task-builder reference also Skill hand-off |
| H | Verification command coverage | PASS | 42 verification grep checks distributed across Phase 2 (4), Phase 3 (6), Phase 4 (5), Phase 5 (6), Phase 6 (6), Phase 7 (6), Phase 8 (3), Phase 9 (6), plus 2 in Phase 10 = comprehensive coverage of all anchor edits |

---

## Summary

- Checks passed: 24 / 26
- Checks failed: 2 (one fixed in-place; one unfixable)
- Critical issues: 1 (Check F — fabricated `--context-file` flag)
- Issues fixed in-place: 1 (Check A — Step 9.2 verbatim drift)
- N/A: 1 (Check 12 / TB-Add-3 — no Open Questions exist)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Step 9.2 (task L820-852) | `old_string` placeholder text `<2-4 sentence executive summary of the diagnosis, evidence, and proposed fix.>` did NOT match actual file content at report-template.md L23-29 (which has two real paragraphs: "2–4 sentences. State the symptom..." and "If `status: partial`..."). Edit would have failed at execution. | FIXED IN-PLACE — old_string and new_string updated to match the actual file verbatim |
| 2 | CRITICAL | Step 6.3 (task L590-624) | Introduces `--context-file <output-dir>/doc-context.md` flag to `Skill sc:adversarial-protocol` invocation. This flag does NOT exist in sc:adversarial's flag schema (verified against `src/superclaude/commands/adversarial.md` flag table — supported flags are `--compare`, `--source`, `--generate`, `--agents`, `--pipeline*`, `--depth`, `--convergence`, `--interactive`, `--output`, `--focus`, `--blind`, `--auto-stop-plateau`). This violates the BUILD_REQUEST PROHIBITED constraint ("no new flag beyond `--no-doc-discovery`") AND introduces a fabricated flag that will fail at runtime. | UNFIXABLE BY QA — requires task-builder redesign. Options: (a) embed Documentation Context Card content directly into the fix-proposal compare artifacts so adversarial debate sees it via `--compare`, (b) convey doc-context via Skill brief prose around the invocation (no new flag), (c) add documented-constraints honoring as inline guidance the debate agents read from the brief. Recommend option (a) — embed a Documentation Context section at the top of each fix proposal artifact |

## Actions Taken

- **Fixed Step 9.2 verbatim drift** in `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260522-151622/TASK-RF-20260522-151622.md`:
  - `old_string` was the paraphrased 5-line block with placeholder `<2-4 sentence executive summary of the diagnosis, evidence, and proposed fix.>`
  - Updated to the actual 7-line block from report-template.md lines 23-29 (real prose paragraphs preserved)
  - `new_string` updated correspondingly so it still inserts the new `## Documentation Context` section between Summary and Diagnosis
  - Verified the new old_string matches the live file (Read report-template.md L23-29)

## Recommendations

- BLOCKER for execution: Step 6.3's `--context-file` flag must be redesigned by task-builder before the task is executable. Recommend embedding the Documentation Context Card directly into the comparison fix proposal artifacts (the `<output-dir>/fix-*.md` files passed via `--compare`) — that way Wave 4's adversarial debate sees the doc-context naturally as part of each artifact, without needing a new flag. The Wave 5 REPORT.md composition is unaffected by this redesign since it consumes the card directly from `<output-dir>/doc-context.md`.
- The Phase 11 final QA gate spawn (Step 11.2) is well-formulated with adversarial stance and `fix_authorization: true` — once the Step 6.3 redesign is in place, that gate is the last line of defense and should catch any further drift.

## QA Complete

VERDICT: FAIL — 1 unfixable critical issue requires task-builder redesign before execution. Unresolved: `--context-file` flag fabrication in Step 6.3.
