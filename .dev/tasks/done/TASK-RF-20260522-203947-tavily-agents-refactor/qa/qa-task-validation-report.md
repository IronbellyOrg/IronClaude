# QA Report — Task Integrity Validation

**Topic:** Tavily-first agents refactor task file
**Date:** 2026-05-22
**Phase:** task-integrity
**Fix cycle:** 1
**Task file:** `.dev/tasks/to-do/TASK-RF-20260522-203947-tavily-agents-refactor/TASK-RF-20260522-203947-tavily-agents-refactor.md`
**Template:** 02 (complex)
**Adversarial stance:** Assume errors exist. Verify exhaustively. Zero leniency.

---

## Overall Verdict: PASS (with minor fixes applied in-place)

The task file is structurally sound, evidence-anchored, and faithful to the 10 pre-authored proposals. Two minor issues were found and fixed in-place. No CRITICAL or IMPORTANT issues remain.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete and well-formed | PASS | All mandatory fields present (id, title, status="🟡 To Do", created, type, task_type=static, related_docs with 12 entries). Lines 1-61. |
| 2 | All mandatory template-02 sections present | PASS | Task Overview, Key Objectives, Prerequisites & Dependencies (with Required Previous Stage Outputs, Handoff File Convention, Frontmatter Update Protocol), Execution Context, Detailed Task Instructions (6 phases + phase gate), Post-Completion Actions, Task Log / Notes (Task Summary, Open Questions, Execution Log, per-phase Findings sections). |
| 3 | Checklist items self-contained (context+action+output+verification+completion gate) | PASS | Every item read includes proposal-file context, Edit action, output file path under phase-outputs/, "ensuring..." verification clause, error-handling fallback, and "Once done, mark this item as complete." closing. Verified items 1.1-1.4, 2.1-2.10, PG.1-PG.2, 3.1-3.3, 4.1-4.2, 5.1-5.3, 6.1, plus 5 post-completion items. |
| 4 | Phase 2 has exactly 10 items, one per in-scope agent, no batching | PASS | `awk '/^### Phase 2/,/^### Phase Gate/' \| grep -c '^- \[ \]'` returns 10. Items 2.1-2.10 map 1:1 to the 10 in-scope agent files. Each item operates on a single file (no batching). |
| 5 | Evidence-based: items reference specific file paths from the proposals | PASS | All 10 Phase-2 items cite both `/config/workspace/IronClaude/.dev/releases/current/TavilyAgents/<proposal>.md` AND `/config/workspace/IronClaude/src/superclaude/agents/<agent>.md` by full absolute path. Each item names the proposal's edit anchors (frontmatter field, body subsection title, Critical Rule number). |
| 6 | No items based on [CODE-CONTRADICTED] / [UNVERIFIED] findings | PASS | Proposals were adversarially-reviewed via /sc:reflect and marked CODE-VERIFIED at authoring (2026-05-22, same-day as this task). Phase 1.2 freshness re-Read pass exists to detect any drift since then. |
| 7 | Open Questions documented (commit grouping; downstream .dev/ doc updates) | PASS | Open Questions section lines 343-355 documents both questions with chosen default + rationale + override path. |
| 8 | Phase dependencies are logical (Prep → 10 edits → Phase Gate → sync → verify → smoke → stage → commit → completion) | PASS | Phase 1 prep → Phase 2 (10 parallel edits) → Phase Gate (PG.1 aggregate + PG.2 rf-qa task-integrity) → Phase 3 (sync-dev → verify-sync → lint, each gated on prior) → Phase 4 (pytest + doctor) → Phase 5 (stage on verify-sync clean, commit, post-commit verify) → Phase 6 (aggregate) → Post-Completion. Each conditional branch explicitly handles both success and failure. |
| 9 | Estimated item count reasonable for scope | PASS | 37 total items for 10-file refactor + full sync/verify/test/stage/commit pipeline + aggregation. Well within TB-Add-2 bounds for single-track. |
| 10 | TB-Add-1: No TBD/TODO/FIXME tokens; no title-only items | PASS | `grep -c 'TBD\|TODO\|FIXME'` returns 0. All checklist items have full Context+Action+Output+Verification+CompletionGate body. |
| 11 | TB-Add-2: Item count within bounds (3-50 single-track) | PASS | 37 items, within bounds. |
| 12 | TB-Add-3: Blocked items reference Open Questions by index in Context | PASS | Step 5.2 explicitly references Open Question 1 ("commit grouping... user may override to 10 per-agent commits — see Open Questions"). Step 6.1 and Post-Completion items reference Open Question 2 (downstream .dev/ docs). |
| 13 | TB-Add-4: Item-to-item dependencies form a DAG | PASS | Walked execution: 1.1→1.2→1.3→1.4→Phase2 parallel(2.1..2.10)→PG.1(reads 10 reviews)→PG.2(reads PG.1 + re-verifies)→3.1→3.2(reads 3.1 summary)→3.3→4.1→4.2→5.1(reads 3.2 summary)→5.2(reads 5.1 status)→5.3→6.1(reads everything). No cycles. |
| 14 | TB-Add-5: XL/multi-file items split or annotated | PASS | Phase 2 atomized to 1-file-per-item (10 items). Each Phase-2 item is large (~70-90 lines) but operates on a single target file with the rationale embedded — and the "ONE Edit per discrete diff anchor" directive prevents internal batching. Phase 3 split into 3 separate sync/verify/lint items. |
| 15 | TB-Add-6: Uniform "ensuring..." verification phrasing and Pass/Fail Acceptance Criteria form | PASS | Every item uses "ensuring..." for the verification clause; per-agent reviews use Pass/Fail with explicit verdict line. Format consistent across all phases. |
| 16 | TB-Add-7: Execution Context "Source areas:" entries reappear in Phase-2 items; block contains NO file:line refs | PASS | `sed -n '136,158p' \| grep -cE 'src/\|/.*:[0-9]+'` returns **0**. Source areas (10 agent prompts + Makefile targets) all reappear: 10 agent prompts in Phase-2 items 2.1-2.10, Makefile sync-dev/verify-sync/lint/test targets in Phase 3 items 3.1-3.3. |
| 17 | TB-Add-8: Per-item Context evidence binding (file:line OR evidence-absence comment) | PASS (with advisory) | All Phase-2 items reference proposal files which themselves carry file:line anchors for every diff (proposal-as-evidence pattern). Items 2.1, 2.9, 2.10 cite explicit line numbers (line 14, line 97, line 98). Items 2.5-2.8 rely on structural anchors (section names, Critical Rule numbers). Acceptable for plan-driven refactor where the proposal carries the line-level evidence; advisory note for future task-builder tightening. |
| 18 | **CRITICAL — Phase 5 EXPLICITLY forbids `git add -f` on .claude/ paths and EXCLUDES .claude/agents/ from staged set** | PASS | Step 5.1 (line 291): "explicitly NOT staging anything under `.claude/agents/` (which is gitignored per CLAUDE.md absolute rule; `git add -f` on any `.claude/` path is FORBIDDEN; if the command would require `-f`, STOP and log a blocker)". Stages only the 10 named `src/superclaude/agents/*.md` paths. Post-stage verification check (b) explicitly verifies "no `.claude/agents/...` line appears in the staged set" with immediate `git reset HEAD .claude/` remediation. |
| 19 | **CRITICAL — Each Phase-2 item lifts verbatim acceptance criteria from its proposal** | PASS (1 issue found & fixed) | Verified by counting acceptance-criteria bullets per proposal vs counts cited in task items. 9 of 10 match exactly. Step 2.4 (rf-task-builder) said "nine acceptance criteria" but proposal has 10 (the "Do NOT use any web tool for" guardrail is criterion #10, not a "plus" addendum); FIXED in-place. |
| 20 | **CRITICAL — Execution Context header passes `grep -cE "src/\|/.*:[0-9]+" == 0`** | PASS | Confirmed 0 file:line references in the Execution Context block (lines 136-158). The reader-aid HTML comment at line 138 explicitly states "no specific file paths or line numbers in this header — those belong in per-item Context fields and the linked proposal files." |

---

## Summary

- Checks passed: 20 / 20
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 2 (one MINOR rule-count fix, one MINOR line-number fix)
- Advisories: 1 (TB-Add-8 partial — proposal-as-evidence is acceptable but file:line citations would be stronger for items 2.5-2.8)

---

## Issues Found & Fixed

| # | Severity | Location | Issue | Fix Applied | Status |
|---|----------|----------|-------|-------------|--------|
| 1 | MINOR | Step 2.4 (rf-task-builder) | Task said "nine acceptance criteria" but proposal has 10 (the "Do NOT use any web tool for" guardrail is criterion #10 in the proposal, not a "plus" addendum). Task also added "plus deferred sync/verify criterion" which is NOT in this proposal's acceptance criteria (other proposals have it; this one does not). | Updated to "ten acceptance criteria" with explicit (10) as the guardrail-preserved criterion, added a clarifying note that sync/verify is validated at project level in Phase 3 even though not enumerated per-proposal here. | FIXED in-place |
| 2 | MINOR | Step 2.10 (rf-qa-qualitative) | Task said "after the `---` fence around line 97 and before the first QA Phase section at line 100"; actual fence is at line 98 in current `rf-qa-qualitative.md`. | Updated to "around line 98". | FIXED in-place |

---

## Advisories (non-blocking)

| # | Location | Note |
|---|----------|------|
| 1 | Phase 2 items 2.5-2.8 | TB-Add-8 partial: these items rely on structural anchors (section name, Critical Rule number) rather than explicit file:line citations. Acceptable because the proposal files carry the line-level evidence (proposal-as-evidence pattern) and the freshness re-Read pass at Step 1.2 detects any drift. Future task-builder tightening could embed line numbers explicitly. |

---

## Actions Taken

1. **Verified TB-Add-7** by `sed -n '136,158p' ... | grep -cE 'src/\|/.*:[0-9]+'` → 0. PASS.
2. **Verified scope closure** by reading `_sweep-summary.md` reference, counting proposal files (10), and verifying all 10 corresponding `src/superclaude/agents/*.md` files exist via `ls`.
3. **Verified rule-numbering claims** for all 6 agents that involve Critical Rule additions:
   - rf-task-builder: current rule 13 (Execution Context emission) at line 526 → new rule 13 (Tavily-first) → existing rule 13 renumbers to 14. Task claim correct.
   - rf-team-lead: 10 current rules (lines 343-353) → new rule 11. Task claim correct.
   - rf-assembler: 9 current rules → new rule 10. Task claim correct.
   - rf-analyst: 8 current rules → new rule 9. Task claim correct.
   - rf-qa: 11 current rules → new rule 12. Task claim correct.
   - rf-task-executor: 6 current rules → new rule 7. Task claim correct.
4. **Verified anchor existence** for body subsection insertions:
   - rf-team-lead: "WebSearch — Understanding Unfamiliar Technologies" exists at line 292. ✓
   - rf-assembler: "Output Quality Standards" (195) and "Completion Protocol" (205). ✓
   - rf-analyst: "Quality Standards" (333) and "Completion Protocol" (342). ✓
   - rf-qa: "Verification Principles" header at line 84, `---` fence at 97, first QA Phase at 99. ✓
   - rf-qa-qualitative: `---` fence at 98 (not 97 as task said — FIXED).
5. **Verified Option/Direction selection**:
   - rf-task-executor: task correctly selects Option A (defensive guardrail) and explicitly forbids Option B (capability removal).
   - rf-assembler: task correctly selects Direction A (keep tools, gate use) and explicitly forbids Direction B.
6. **Verified frontmatter state for deep-research and deep-research-agent**: both currently have NO `tools:` block (only name/description/category). Task Step 2.1 and 2.2 correctly direct ADD (not reorder). ✓
7. **Verified Phase 5 staging constraint**: Step 5.1 stages exactly 10 named `src/superclaude/agents/*.md` paths, explicitly forbids `git add -f` on .claude/ paths, includes the STOP-and-log-blocker fallback for any `-f` requirement, and adds a post-stage verification check that any `.claude/agents/...` line in the staged set triggers immediate `git reset HEAD .claude/`. CLAUDE.md absolute rule honored.
8. **Counted acceptance criteria per proposal vs task claim** for all 10 proposals; found 1 mismatch (Step 2.4) and fixed in-place. Other 9 match exactly.
9. **Fixed 2 minor inaccuracies in-place** via Edit tool.

---

## Confidence Gate

- **Verified:** 20 / 20
- **Unverifiable:** 0
- **Unchecked:** 0
- **Confidence:** 100.0%
- **Tool engagement:** Read: 7 | Grep: 0 | Glob: 0 | Bash: 12 | Edit: 2

Every checklist item was verified with at least one tool call. The 2 in-place fixes were applied and confirmed via the Edit tool's successful application. The Execution Context grep check returned the byte-exact expected value (0). Rule numbering, anchor existence, and acceptance-criteria counts were all spot-checked against the source agent files and proposal files.

---

## Recommendations

The task is ready to execute. Recommended next steps:

1. The orchestrator can immediately spawn rf-task-executor on this task file.
2. Phase 2 items 2.1-2.10 should be spawned in parallel per the F2a exception (10 parallel agents — saves significant wall time).
3. The Phase Gate (PG.2) `fix_authorization: true` adversarial rf-qa spawn pattern matches feedback memory `feedback_rfqa_adversarial_pattern.md`.
4. Phase 5 staging will land cleanly because the absolute-rule constraint is encoded directly into the staging command.

## QA Complete

**VERDICT: PASS**

No unfixable issues. Two minor inaccuracies fixed in-place. Task file is ready for execution.
