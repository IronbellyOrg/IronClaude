# QA Report — Task Integrity (Structure & Phase Ordering Lens)

**Topic:** Wire `--tui` into `superclaude swarm run` (Approach A)
**Date:** 2026-06-18
**Phase:** task-integrity
**Lens:** phase-structure
**Fix authorization:** false (report-only)

---

## Confidence
**Verified: 9/9 lens items + 8/8 TB-Add | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%**
**Tool engagement:** Read: 2 | Grep: 0 | Glob: 0 | Bash: 8

---

## Items Reviewed (Phase-Structure Lens)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete/well-formed | PASS | id, title, status, type, created_date, spec_path, start_commit (300c06a6 verified via `git cat-file -t` = commit), executor_model_class=sonnet, reflect_pre (block), reflect_post (room-comment, empty for wrapper write-back), related_docs (6), tags (5) all present, non-empty. Frontmatter delimited L1-67. |
| 2 | Mandatory Template-02 sections present | PASS | Task Overview (L71), Key Objectives (L81), Prerequisites & Dependencies (L95), Execution Context w/ References/Source Areas/Key Constraints (L114/116/125/133), Detailed Task Instructions (L167), Post-Completion Actions (L271), Task Log / Notes (L285). |
| 3 | Phase dependencies logical | PASS | Prep→Impl→Tests→Validation→Post-Completion. No circular/missing. P2 reads `wiring-inventory.md` (written P1.3); P3.8 reads `frozen-signatures.md` (written P1.3); P4 validates P2/P3. |
| 4 | Phase ordering: impl before tests, validation after | PASS | Impl (P2) before tests (P3) exercising `_tail_events`/`--tui`; Validation (P4) after both. |
| 5 | Completion items inside Post-Completion AND after POST reflect | **FAIL** | status→Done is POST item 6 (last), inside Post-Completion (anti-orphaning OK) and after reflect gate (item 4). BUT see Issue #1: reflect gate not penultimate. |
| 6 | POST reflect gate: present, penultimate, flat wrapper, NFR-7-clean | **FAIL** | Present (L279), flat `superclaude reflect run <task> --depth deep --fix --promote` in `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` skip guard, consumes exit (only 0 proceeds), NFR-7-clean (no `--reflect`/`<base>..HEAD`/agent-spawn/`/sc:reflect`). Byte-matches precedent. BUT NOT penultimate — Issue #1. |
| 7 | Task Log: Execution Log + per-phase Findings headers | PASS | Execution Log (L309), Phase 1-4 Findings (L319/329/338/340), Phase Gate (L342), Follow-Up (L346), Deviations (L352), Task Summary (L287). |
| 8 | Item count reasonable (28 across 4 phases + POST) | PASS | Total 28: P1=4, P2=6, P3=8, P4=4, POST=6. Exact match. |
| 9 | Open Questions / gaps documented | PASS (N/A) | No Open Questions (gaps resolved in 06-gapfill). Follow-Up section present for runtime gaps. |
| TB-1 | No TBD/TODO/FIXME, no title-only items | PASS | grep → none. Every item has Context+Action+Output+Verification+Completion body. |
| TB-3 | Blocked items reference blocking Open Question | PASS (N/A) | No Open Questions; no blocked items. |
| TB-4 | Item-to-item deps form a DAG | PASS | P2.1→P1.3, P2.6→P2.5, P3.x→P2.x, P3.8→P1.3, P4→P2/P3, POST→P4. All forward; no cycle. |
| TB-5 | XL/multi-file items split or justified | **FAIL** | Item 2.5 (L209) is ~40-line single item w/ 5 distinct sub-edits (a–e). Issue #2. |
| TB-6 | Uniform verification phrasing + AC form | PASS | Every item closes identically. Uniform across 28. |
| TB-7 | Source Areas reappear in items; block header no file:line | **PARTIAL** | All 7 Source Areas reappear (commands.py 12×, dispatch.py 3×, parallel.py 2×, tests/swarm/ 17×, tui.py 5×+6×, models.py 3×, state.py via module+`read_state`). Source Areas sub-block has NO file:line. BUT Key Constraints sub-block (same Execution Context block) DOES — Issue #3. |
| TB-8 | Per-item Context code-surface refs carry file:line/evidence-absence | PASS | Every code-surface item carries `path.py:NN`/`~line N` (2.1 commands.py ~1452-1469; 2.4 _drain_appended ~2834-2858; 3.8 dispatch.py:334-343). Verified vs source. |

---

## Source-Truth Verification

| Claim | Check | Result |
|---|---|---|
| `start_commit` 300c06a6… | `git cat-file -t` | PASS — commit |
| `dispatch_wave1` sig + dispatch.py:334-343 | Read dispatch.py:330-345 | PASS — exact (def @334) |
| `ParallelExecutor` parallel.py:80/100/103/169 | Grep parallel.py | PASS — class@80, __init__@100, plan@103, execute@169 |
| 6 production source files exist | `ls` | PASS — all present |

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Post-Completion items 4-6 (L279-283) | **POST reflect gate is NOT penultimate.** Lens item 6 requires the reflect gate positioned PENULTIMATE — immediately before the Update-status-to-Done item. Actual order is: reflect gate (POST item 4, L279) → **Task Summary write (POST item 5, L281)** → status→Done (POST item 6, L283). The Task Summary item is interposed between the gate and the Done flag. Intent is partially preserved (the Task Summary is a pure doc write with no spec/gate mutation and no Done flag), but the literal "immediately before" requirement is violated and the reflect verdict can go stale if the summary write prompts any revisit. | Reorder so the POST reflect gate (L279) immediately precedes the status→Done item. Move the Task Summary write (L281) to BEFORE the reflect gate (e.g., between the QA-waiver log item and the reflect gate), so the sequence becomes: …→ QA-waiver log → Task Summary → POST reflect gate → status→Done. |
| 2 | MINOR | Phase 2, Step 2.5 (L209) | **XL single item without a justifying comment (TB-Add-5 / item-atomicity).** Item 2.5 is ~3,400 chars / 5 distinct labelled sub-edits (a–e: thread closure, gated poll loop, join+finally teardown, re-raise, byte-identical fallback). Exceeds the ~15-line atomicity heuristic and cannot be executed without scrolling. Mitigating: all sub-edits are on ONE file (`commands.py`) and form one semantically-atomic change (the threaded-dispatch glue must land coherently or the file is left broken), so it is single-file, not multi-file. | Either (a) add a brief inline justification noting the sub-edits are one atomic glue change that cannot be partially landed, OR (b) split into 2.5a (thread + result/exception box + synchronous fallback) and 2.5b (gated poll loop + finally teardown + re-raise). Option (a) is sufficient given single-file cohesion. |
| 3 | MINOR (observational) | Execution Context → Key Constraints (L133-141) | **file:line citations inside the `## Execution Context` block.** The Key Constraints sub-block cites `dispatch.py:334-343`, `parallel.py:80/100/103/169`, `models.py:1820`, `commands.py:2264`. Per the lens note this is **explicitly out of TB-Add-7 scope** ("Key constraints bullet's presence or absence is irrelevant to TB-Add-7; cross-validates Source areas only"), and these citations are evidence-bearing (frozen-signature anchors the executor needs), so this is NOT a TB-Add-7 failure. Noted only because a strict producer-side R-039 re-grep of the whole block range would flag it. The TB-Add-7 target (the **Source Areas** sub-block) is clean — zero file:line. | No change required for TB-Add-7 compliance. Optional: if strict whole-block R-039 hygiene is desired, the frozen-signature anchors could move into the relevant per-item Contexts (they already reappear there: 3.8/4.4). Leaving as-is is acceptable. |

## Summary
- Lens checks passed: 7 / 9 (Issues #1 affects checks 5 and 6)
- TB-Add checks passed: 7 / 8 clean + TB-Add-5 MINOR (Issue #2); TB-Add-7 PASS with observation (Issue #3)
- Critical issues: 0
- Important issues: 1 (reflect-gate not penultimate)
- Minor issues: 2 (XL item 2.5 unjustified; observational file:line in Key Constraints)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Strong Positives Verified (extraordinary-evidence bar for clean checks)
- Frontmatter `start_commit` 300c06a6 confirmed a real commit (`git cat-file -t`).
- `dispatch_wave1` + `ParallelExecutor` signature claims byte-accurate vs live source (Read/Grep) — the frozen-signature contract the task pins is real, not fabricated.
- All 13 phase-output capture filenames PRODUCED in P1-P4 exactly match the 13 LISTED in the POST verification item (L273) — zero orphaned/missing capture references.
- Reflect wrapper form byte-matches the cited precedent TASK-RF-pr167-verdict-regex (skip-guard + flat shell-out + exit-code consumption + NFR-7-clean).
- Intra-phase write-before-read ordering holds for both handoff files (`wiring-inventory.md`, `frozen-signatures.md`).
- All 6 named production/test source files exist on disk.

## Recommendations (before execution)
1. **Fix Issue #1 (IMPORTANT):** reorder Post-Completion so the reflect gate is penultimate. This is the only finding that should block a PASS on the phase-structure lens.
2. **Address Issue #2 (MINOR):** add a one-line atomicity justification to item 2.5 (cheapest fix) or split it.
3. Issue #3 needs no action for TB-Add-7 compliance.

---

## VERDICT: FAIL

**Rationale:** One IMPORTANT structural deviation (Issue #1 — POST reflect gate is not positioned penultimate; a Task Summary write is interposed before the status→Done item) fails lens checks 5 and 6, which are explicit phase-ordering requirements. Per the QA zero-tolerance standard, an IMPORTANT positioning violation against an explicit gate-ordering rule is a FAIL, not a soft flag. The two MINOR items (XL item 2.5 lacking a justification comment; observational file:line in Key Constraints, which is out of TB-Add-7 scope) reinforce the FAIL but would not alone block. The task file is otherwise structurally strong: complete frontmatter, all Template-02 sections, logical phase + DAG dependencies, correct item counts (28), accurate source-truth claims, and a byte-correct NFR-7-clean reflect wrapper.

**To convert to PASS:** apply the Issue #1 reorder (move Task Summary before the reflect gate so the gate is immediately before status→Done) and optionally the Issue #2 justification. No source/frozen-signature claims need correction — those verified clean.

## QA Complete
