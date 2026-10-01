# QA Report — Task Integrity (Structure & Phase Ordering Lens)

**Topic:** Pipeline Hardening Closure mode (H0-H5) for sc:troubleshoot-protocol
**Date:** 2026-06-10
**Phase:** task-integrity
**Lens:** phase-structure
**Fix cycle:** N/A
**Fix authorization:** false

---

## Overall Verdict: FAIL

Two structural defects in the Post-Completion ordering plus minor checklist-additions gaps. The task file is otherwise structurally sound: correct template-02 section set, clean phase dependency chain, 8-lens M3 + 2-agent M4 gate structure, no placeholders, no malformed checkboxes, correct POST-reflect diff form.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | YAML frontmatter complete/well-formed | PASS | Lines 2-55: `id`, `title`, `status`, `created_date`, `spec_path`, `reflect_pre` (block), `reflect_post`, `related_docs` (list) all present with non-empty values. Frontmatter closes at line 55. |
| 2 | Mandatory template-02 sections present | PASS | `grep '^## '` → Task Overview, Key Objectives, Prerequisites & Dependencies, Execution Context, Open Questions, Detailed Task Instructions, Post-Completion Actions, Task Log / Notes (8 sections). |
| 3 | Phase dependencies logical; no build item before anchor capture | PASS | Step 1.4 (L174) captures insertion-anchors; all Phase 2 edit items (L184+) follow. Refs 2.1-2.5 are new-file creates (no anchor needed); edits 2.6-2.14 read the discovery inventory. Validation (P3) → M3 (P4) → M4 (P5) → post-completion ordering correct. |
| 4 | Edits before sync/verify-sync; validation before QA; M4 after M3 | PASS | P2 edits → P3 (sync-dev L260 → verify-sync L264 → markdownlint L268) → P4 M3 gate → P5 M4 gate. M4 explicitly runs after M3 (L336 rationale). |
| 5 | Anti-orphaning: completion items in FINAL phase; POST-reflect penultimate + SELF-RUN | **FAIL** | Completion items ARE in the final `## Post-Completion Actions` section (template-02 sanctions this) — anti-orphaning satisfied. BUT POST-reflect (L366) is NOT penultimate: Task Summary (L368) sits between it and Update-status-to-Done (L370). See Issue #1. POST-reflect is correctly SELF-RUN, not human-HALT (verified L366: no HALT/stop-execution language). |
| 6 | Task Log section at bottom | PASS | `## Task Log / Notes 📋` at L372, last section in file. |
| 7 | Item count reasonable for scope | PASS | 47 total items (`grep -c '- [ ]'`): P1=4, P2=14, P3=4, P4=14, P5=5, Post-Completion=6. Matches ~47 target for 9 file changes + 8-agent M3 + 2-agent M4. |
| 8 | Open Questions documented | PASS | 3 documented (L150-152): OQ1 G1 halt condition, OQ2 verdict-enum reconciliation (GF-5), OQ3 tests-out-of-scope. |
| 9 | M3 gate (8 lens agents, each own item) + M4 (≥2 fidelity) | PASS | P4: 4.2-4.5 = 4 rf-qa structural lenses, 4.6-4.9 = 4 rf-qa-qualitative content lenses = 8 lens agents, all `fix_authorization:false`, each its own `- [ ]` item; 4.11 serialized single fixer; 4.12-4.13 verification; 4.14 max-3-cycle control. P5: 5.1+5.2 = 2 M4 fidelity agents reading spec+output. 8≥8 for 500-1500 line tier. |
| 10 | TB-Add-1: no TBD/TODO/FIXME; no title-only items | PASS | `grep -E 'TBD\|TODO\|FIXME'` → 0 matches in live content (templates use HTML comments). All items carry full body. |
| 11 | TB-Add-3: blocked items reference Open Question by index | **PARTIAL FAIL (MINOR)** | Step 1.3 G1 item (L170) does NOT reference "Open Question 1" by index. OQ1 references "Step 1.3" forward but the item lacks the backward index ref. Mitigated: Step 1.3 is explicitly a recorded acknowledgement, NOT a blocking HALT, so TB-Add-3's strict trigger (blocked item) is arguable. See Issue #3. |
| 12 | TB-Add-4: item-to-item dependencies form a DAG | PASS | Dependency flow is strictly forward: discovery → build → validate → M3 → M4 → post-completion. No item references a later item as a prerequisite. Acyclic. |
| 13 | TB-Add-5 / item 10: XL/multi-file items split or justified | **PARTIAL FAIL (MINOR)** | Step 2.11 (L236, 2924 chars) modifies THREE distinct insertion points in SKILL.md (calibration-style gate block + Wave 6 precondition + Will Not Do bullet) in one item — borderline atomicity violation per item-10 "multiple distinct file modifications must be split." See Issue #2. Other large items (2.1=3841 chars) each touch ONE file = atomic. |
| 14 | TB-Add-6: uniform Verify/Acceptance form | PASS | Every item ends with the same "...ensuring [verification]... then mark this item complete. Once done, mark this item as complete." closure + a templated-blocker fallback. Consistent across all 47 items. |
| 15 | TB-Add-7: Execution Context "Source areas" reappear in items; no file:line in block | PASS | Execution Context block (L96-147) has ZERO `path:NN` file:line citations (grep confirmed). All 4 Source Areas (command, SKILL.md, 2 edit refs, 5 new refs) reappear in item bodies (command×9, SKILL×8, report-template×20, remediation-handoff×9, each new ref 5-8×). Bare `src/` paths in Source Areas listing are the intended Source-areas content, not file:line refs. |
| 16 | TB-Add-8: per-item Context referencing code surface has file:line OR evidence-absence | PASS | Items cite spec line ranges (e.g. "spec lines 136-151"), § sections, and named anchors ("Tier 2 calibration", "Wave 6 precondition", "status: success"). Edit items anchor on the discovery inventory (TEXT-anchor per GF-1) rather than absolute lines — a deliberate, justified evidence-binding approach. |
| 17 | POST-reflect: present, penultimate, SELF-RUN, merge-base working-tree diff, depth deep, --spec | **PARTIAL FAIL** | Present (L366), SELF-RUN ✓, `--diff <BASE>` where `<BASE>`=`git merge-base HEAD <integration-branch>` ✓ (NOT `start_commit..HEAD` — appears only inside a negation), `--depth deep` ✓, `--spec` set ✓, `git add -A` before ✓. ONLY defect: NOT penultimate (Task Summary L368 follows it). See Issue #1. |

## Summary
- Checks passed: 12 / 17 fully PASS
- Checks failed: 1 hard FAIL (item 5), 3 partial-FAIL (items 11, 13, 17 — item 17's only defect is the same ordering issue as item 5)
- Critical issues: 1 (POST-reflect not penultimate)
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Confidence Gate

- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 0 (via Bash) | Glob: 0 | Bash: 8
  - Note: Grep checks executed via Bash `grep` (8 targeted invocations, each mapping to a specific checklist item: item-count, placeholder scan, phase mapping, Execution-Context file:line scan, Source-area reappearance, POST-reflect form, G1 OQ-ref, item-size, section list). Tool calls (3 Read + 8 Bash = 11) vs 17 checklist items is below the 1:1 heuristic, but each Bash call verified multiple items via batched greps; no item is unverified.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | Post-Completion Actions, L366 vs L368/L370 | POST-reflect SELF-RUN gate (L366) is NOT penultimate. The "create Task Summary" item (L368) sits between POST-reflect and the final "Update status to Done" item (L370). The lens requires POST-reflect immediately before Update-status-to-Done. Risk: a reflect-surfaced deviation/regression could be appended to Open Questions AFTER the Task Summary is already written, so the summary won't reflect the reflect verdict, and Done could be set on a tasklist whose post-reflect remediation is unincorporated. | Reorder Post-Completion items so POST-reflect (L366) is the second-to-last item, immediately before "Update status to Done" (L370). Move "create Task Summary" (L368) to BEFORE the POST-reflect item. Canonical order: [verify outputs] → [no-testing rationale] → [re-confirm M3/M4] → [Task Summary] → [POST-reflect SELF-RUN] → [Update status to Done]. |
| 2 | IMPORTANT | Phase 2, Step 2.11 (L236) | Granularity/atomicity (item 10 / TB-Add-5): this single item performs THREE distinct modifications to SKILL.md — (a) a calibration-style completeness-gate block, (b) a Wave 6 precondition tightening, (c) a `## Will Not Do` bullet append. Item 10 states items "describing multiple distinct file modifications must be split." 2924 chars; executor cannot see it without scrolling. | Split Step 2.11 into three atomic sub-items: 2.11a (completeness-gate block), 2.11b (Wave 6 precondition), 2.11c (Will Not Do bullet) — each anchored on its own discovery-inventory text anchor. Same applies less severely to 2.9 (Wave 4.5 section + ASCII map line), though those two edits are tightly coupled and may stay together. |
| 3 | MINOR | Phase 1, Step 1.3 (L170) | TB-Add-3: the G1 acknowledgement item does not reference its Open Question by index. OQ1 (L150) is the numbered G1 open question and references "Step 1.3" forward, but Step 1.3 does not reference "Open Question 1 / OQ-1" backward. The lens explicitly calls out the G1 item. Mitigation: Step 1.3 is a recorded acknowledgement, NOT a blocking HALT, so TB-Add-3's strict trigger (blocked-item-depends-on-question) is arguable. | Add to Step 1.3 Context: "This addresses Open Question 1 (G1 halt condition) in the Open Questions section." for bidirectional cross-reference. |

## Actions Taken
None — `fix_authorization: false`. Report-only. All three issues documented with specific locations and required fixes for the fix-cycle.

## Recommendations
1. **MUST fix Issue #1 (CRITICAL) before execution.** The POST-reflect-not-penultimate ordering is the single hard FAIL; it undermines the self-run reflect gate's purpose (catch deviations before Done). Reorder so reflect is immediately before Update-status-to-Done.
2. **Should fix Issue #2 (IMPORTANT).** Split Step 2.11 into 3 atomic items so the executor edits one SKILL.md insertion point per item.
3. **Optional Issue #3 (MINOR).** Add backward OQ-index reference to Step 1.3.
4. Note for downstream content/fidelity lenses (out of this structural lens's scope): the verdict-enum reconciliation (OQ2/GF-5 — refs use full `not_applicable` enum, spec §8 report block omits it) is an intentional additive reconciliation, not a structural contradiction; content-lens agents should confirm it is consistently applied across all 9 files.

## QA Complete

VERDICT: FAIL
- CRITICAL: 1 (POST-reflect not penultimate — Issue #1)
- IMPORTANT: 1 (Step 2.11 multi-modification atomicity — Issue #2)
- MINOR: 1 (G1 item missing Open-Question backward index — Issue #3)
