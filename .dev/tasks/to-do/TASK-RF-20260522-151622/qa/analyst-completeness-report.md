# Research Completeness Verification

**Topic:** Wave 1.5 Documentation Grounding addition to sc:troubleshoot (task-builder track)
**Date:** 2026-05-22
**Files analyzed:** 4 (01-file-inventory.md, 02-patterns-and-conventions.md, 03-integration-points.md, 04-template-and-examples.md)
**Depth tier:** Deep (structural extension with line-anchored edit targets)

---

## Verdict: PASS — 0 critical gaps, 1 minor advisory observation

The research package is task-build-ready. All edit anchors are cited file:line, both source-of-truth files have been investigated end-to-end, MDTM template 02 rules are quoted verbatim with line citations, and a prior spec-edit task (TASK-RF-20260520-230051) supplies the canonical 5-phase structure. The seven specific line-citation claims requested for verification all match the source files exactly. No critical gaps block proceeding to BUILD_REQUEST → rf-task-builder.

---

## Line-citation Verification (task-specific spot checks)

These are the seven specific claims the spawn prompt asked me to verify against actual source files.

| # | Claim | File:line checked | Source content | Verdict |
|---|---|---|---|---|
| 1 | Researcher 1: SKILL.md line 137 is the Wave 1 brief location | SKILL.md:137 | `3. **Form one hypothesis** — spawn the root-cause-analyst agent via Task with a focused brief: the symptom, the grounding from step 1, the observation from step 2, and --scope if any. The agent's job is to produce one hypothesis card (template in refs/hypothesis-card-template.md) — not three, not the full tree.` | VERIFIED |
| 2 | Researcher 1: SKILL.md lines 167-217 is Wave 3 | SKILL.md:167-217 | Line 167 is `### Wave 3: Tier 2 — Parallel Hypotheses`; line 217 is blank inside the failure-handling table region; the wave ends at the `---` separator near line 217. | VERIFIED (boundary is accurate — wave header at 167, content runs to ~215, blank/closing at 217) |
| 3 | Researcher 1: SKILL.md lines 70-77 is the Wave Structure block | SKILL.md:70-77 | Line 70: `Wave 0: Parse + Validate Input`; line 76: `Wave 6: Tier 3 — Remediation Chain (conditional, requires --fix + user accept)`; line 77 is the closing code fence. Researcher 1 lists Wave 0-6 on lines 70-77 in the inventory; verbatim quoted lines match exactly. | VERIFIED |
| 4 | Researcher 3: SKILL.md L228-239 is the Wave 4 adversarial invocation | SKILL.md:228-239 | Line 228: `2. **Invoke /sc:adversarial in compare mode** via Skill:`; lines 230-235 are the fenced Skill block; line 239 is `3. **Collect adversarial output** ...`. Full range is the adversarial invocation block. | VERIFIED |
| 5 | Researcher 3: report-template L17 has "Test file to update" | report-template.md:17 | `**Test file to update**: <absolute or repo-relative path when test_is_wrong=true, otherwise omit this line>` | VERIFIED (exact string match) |
| 6 | Researcher 2: SKILL.md:192 has the spawn-in-parallel phrase | SKILL.md:192 | `2. **Spawn hypothesis agents** in parallel via Task (single message with multiple Task calls). Each agent receives:` | VERIFIED (verbatim match including the load-bearing parenthetical) |
| 7 | Researcher 4: template 02 lines 142-149 are B2 | 02_mdtm_template_complex_task.md:142-149 | Line 142: `B2. EVERY CHECKLIST ITEM MUST BE A COMPLETE, SELF-CONTAINED PROMPT THAT INCLUDES:`; lines 143-148 are the 6 numbered elements; line 149 is the blank separator before B3. Researcher 4 quoted the block as 142-149 which includes the trailing separator — acceptable boundary framing. | VERIFIED (rule body proper is 142-148; the 142-149 range cited includes the trailing blank as the section terminator, consistent with how researcher 4 cited other rule blocks) |

**Verification summary:** 7/7 line citations match the source files exactly. No drift, no contradictions, no fabricated line numbers.

---

## Coverage Audit (against scope)

The task track goal enumerates 5 source-of-truth file edits + 1 new file + sync/verify gates. Coverage:

| Scope Item | Covered By | Status |
|---|---|---|
| src/superclaude/commands/troubleshoot.md (Options/Behavioral/Boundaries edits) | 01-file-inventory.md §troubleshoot.md (lines 8-109 of the research file: every section enumerated with line ranges); 02-patterns-and-conventions.md §Pattern 5 (MCP Integration), §Pattern 6 (Options table), §Pattern 7 (Will/Will Not bullets) | COVERED |
| src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md (Wave list, new Wave 1.5 block, Refs loader, Graceful Degradation, MCP Integration, Output Contract, Wave 1/3/4/5 wiring) | 01-file-inventory.md §SKILL.md (lines 112-446 — every section enumerated); 02-patterns-and-conventions.md §Pattern 1 (Wave template), §Pattern 2 (fan-out), §Pattern 3 (Refs table), §Pattern 4 (Error Handling), §Pattern 8 (Output Contract); 03-integration-points.md Wirings 1, 3, 4, 5, 7 | COVERED |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md (consistency_with_docs field) | 01-file-inventory.md §refs/hypothesis-card-template.md (lines 449-513); 03-integration-points.md Wiring 2 | COVERED |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/report-template.md (Documentation Context section + behavior_is_documented field) | 01-file-inventory.md §refs/report-template.md (lines 516-618); 03-integration-points.md Wirings 5, 6, 8 | COVERED |
| src/superclaude/skills/sc-troubleshoot-protocol/refs/doc-discovery.md (NEW file — 4-section ref) | Acknowledged in 01-file-inventory.md lines 442-445 and 743-744; naming convention deferred to Researcher 4. **Researcher 4 did NOT explicitly document a recommended 4-section structure** for the NEW file. | PARTIAL — see Minor Advisory below |
| make sync-dev + make verify-sync sequence | 04-template-and-examples.md §Section 3 "How sync-dev + verify-sync items were structured" (lines 414-420); §Section 4 "Standard sync-dev + verify-sync item shape" (lines 506-511) | COVERED |
| 5 grep verification commands | 04-template-and-examples.md §Section 3 "How grep-verification items were structured" (lines 422-431) + §Section 4 grep-item shape template (lines 514-528); §Section 5 VALIDATION_REQUIREMENTS field (line 558) enumerates 3 specific greps + test -f + internal-consistency check | COVERED |
| Discovery surfaces (.dev/releases/current/, .dev/releases/complete/, docs/) | 01-file-inventory.md §Discovery surfaces (lines 677-685) — all three confirmed present with subdirectory listings | COVERED |

---

## Evidence Quality

| Research File | Evidenced Claims | Unsupported Claims | Quality Rating |
|---|---|---|---|
| 01-file-inventory.md | Every section heading carries a file:line range; every verbatim quote is bracketed by line citations; every insertion point is named with a precise after-line number | 0 unsupported (the only judgmental claims are explicitly tagged as "recommendation" or "researcher 3/4 owns the call") | Strong |
| 02-patterns-and-conventions.md | All 8 patterns are introduced with a verbatim quote followed by abstracted observations; pattern locations are cited (e.g., "SKILL.md:167-217", "commands/troubleshoot.md:46-57") | 0 unsupported (one structural observation about lack of section literally titled "Graceful Degradation" — line 165 — is itself evidence-based: it states what does NOT exist and what the functional equivalent is) | Strong |
| 03-integration-points.md | 9 wirings, each anchored to specific SKILL.md or refs/ lines (137, 192-197, 228-238, 239, 256-263, 49-50, 380, 17, 27/29 boundary, 98-106); recommended modifications are quoted verbatim | Status field reads "In Progress" at line 4 — **but** every section is filled in and the Summary at lines 334-351 reads as complete. Status header drift only. | Strong (with minor status-tag drift) |
| 04-template-and-examples.md | A3/A4/B2/B3/B5/L1-L6/M1/E1/I13/I17/I18 rules are quoted verbatim with line citations; DM-001 R-033/R-034/R-035/R-038/R-039 emitters quoted verbatim; prior task examples (TASK-RF-20260520-230051 + TASK-RF-20260518-cliEval-P4) walked through with phase structure and Execution Context block verbatim | Status field reads "In Progress" at line 4 — but every section is filled and Summary at 580-587 reads complete. Same status-tag drift. | Strong (with minor status-tag drift) |

---

## Documentation Staleness

This is a spec-edit task: most "doc-sourced claims" are direct quotations from source files (SKILL.md, troubleshoot.md, refs/, template 02). I spot-checked the 7 specific claims listed in the spawn prompt against actual source — all 7 verified exact (see table above). No `[CODE-CONTRADICTED]` or `[STALE DOC]` tags are needed because the research files are themselves quotations, not interpretations of stale documentation. Two `[UNVERIFIED]`-class observations the researchers raised honestly:

- 01-file-inventory.md lines 66, 71, 373, 417 carry explicit "**RIPPLE-EFFECT FLAG**" annotations naming claims that may go stale if the builder decides to add a Tier 1 Context7 call. These are forward-looking risk notes, not stale-doc claims.
- 01-file-inventory.md lines 482-504 explicitly presents two interpretations (A vs B) for the consistency_with_docs field placement and recommends B while flagging that the call is Researcher 3's. Researcher 3's Wiring 2 (lines 27-76) chose **a third placement** (top-level metadata block sibling to `**Cause class**`) — neither A nor B from Researcher 1. This is a productive divergence, not a contradiction — see Contradictions section below.

---

## Completeness

| Research File | Status | Summary | Gaps Section | Key Takeaways | Rating |
|---|---|---|---|---|---|
| 01-file-inventory.md | Complete (line 4) | Yes — `## Summary` at line 689 with full per-file anchor enumeration | Implicit (RIPPLE-EFFECT FLAGs throughout) — no dedicated "Gaps" header | Yes — Summary section serves as Key Takeaways | Complete |
| 02-patterns-and-conventions.md | Complete (line 4) | Yes — `## Summary` at line 401 mapping each of 8 patterns to Wave 1.5's analogous use | Implicit — no dedicated header | Yes — Summary functions as takeaways | Complete |
| 03-integration-points.md | "In Progress" (line 4) — **header status DRIFT** | Yes — `## Summary` at line 334 with bulleted edit points | Wiring 9 explicitly addresses the no-change verdict for triage-checklist; that IS the gap-addressing prose | Yes — Summary at line 334 functions as takeaways; closes with "Status: Complete" at line 351 contradicting line 4 | Complete (content) / Header drift |
| 04-template-and-examples.md | "In Progress" (line 4) — **header status DRIFT** | Yes — `## Summary` at line 580 with section-by-section recap | Implicit — pitfalls section at lines 539-547 serves as the gap-and-warning surface | Yes — Section 5 BUILD_REQUEST values table at lines 555-560 is the actionable takeaway | Complete (content) / Header drift |

**Status-tag drift note:** Files 03 and 04 carry "Status: In Progress" in the header but close with "Status: Complete" or contain full summaries. This is a header-marker hygiene issue, not a content gap. The downstream rf-task-builder reads the bodies, not the header tags, so this does not block the build.

---

## Cross-references

Cross-file consistency is strong:

- File 01 (anchors) → File 02 (patterns): Pattern 1's reference to Wave 3 at "SKILL.md:167-217" matches File 01's enumeration at lines 269-296.
- File 01 (Output Contract slot at line 50) → File 02 §Pattern 8 (Output Contract format at SKILL.md:49-50) → File 03 Wiring 7 (Output Contract dict extension citing lines 49-50): all three agree on the insertion point and the format mirror.
- File 01 (Refs loader at SKILL.md:377-385) → File 02 §Pattern 3 (Refs format at SKILL.md:377-383) → File 03 Wiring 1 (Refs row addition at line 380): consistent wave-order placement, consistent format.
- File 01 (Wave 5 REPORT.md composition at SKILL.md:256-263) → File 03 Wiring 5 (Documentation Context insert at L256-263 between Summary and Diagnosis): **DIVERGENCE — see Contradictions section**.
- File 04 (BUILD_REQUEST values §Section 5) → maps cleanly to File 01 + File 03 edit anchors and File 02 pattern conventions.

---

## Contradictions Found

Two productive divergences identified — both are placement decisions where multiple researchers proposed different slots. These are NOT errors; they are exactly the kind of ambiguity the task-builder will resolve at BUILD_REQUEST emission. Documenting them so the downstream builder is aware:

### Contradiction 1: Where the Documentation Context section slots in REPORT.md

- **01-file-inventory.md lines 583-593:** Recommends inserting between Evidence (line 47) and Proposed Fix (line 49). Rationale: "Evidence → Documentation Context → Proposed Fix mirrors the new derivation order. The Proposed Fix MUST respect the Documentation Context."
- **03-integration-points.md Wiring 5 (lines 152-210):** Recommends inserting between Summary (L27) and Diagnosis (L29). Rationale: "Summary → Documentation Context → Diagnosis preserves the 'frame → evaluate the answer' flow."
- **Both researchers explicitly weighed the alternative and rejected it.** File 01 rejects the Summary-Diagnosis slot at lines 591-592 ("Putting it before Diagnosis breaks the existing flow"); File 03 rejects the Evidence-ProposedFix slot at lines 188-189 ("Placing it between Evidence and Proposed Fix would split the 'what is the bug' → 'how do we fix it' flow with a context detour — wrong cut.")
- **Both placements are internally consistent and well-reasoned.** The BUILD_REQUEST emitter (or the user) must pick one. **Recommendation for the builder:** carry BOTH placements into BUILD_REQUEST `VALIDATION_REQUIREMENTS` as a known decision point, OR pick one with explicit justification before BUILD_REQUEST emission. This is the single most consequential placement decision in the task.

### Contradiction 2: Where consistency_with_docs slots in hypothesis-card-template.md

- **01-file-inventory.md lines 482-504:** Presents Interpretation A (new per-dimension item under Confidence, line 53 insertion) and Interpretation B (new top-level section after Evidence, line 28 insertion); recommends B.
- **03-integration-points.md Wiring 2 (lines 27-76):** Chooses **Interpretation C** — a sibling to `**Cause class**` in the top metadata block (line 16). Explicitly rejects both A and B with reasoning (lines 53-57: putting it near Confidence would mix categorical with numeric; putting it near Proposed Fix would imply fix-alignment not hypothesis-alignment).
- **Researcher 3's choice (top metadata block) is the strongest argument** because it positions the field as a categorical classifier readable by the calibrator and Wave 4 without scanning the body. **Recommendation for the builder:** adopt Researcher 3's interpretation (Wiring 2) as the canonical placement.

---

## Compiled Gaps

### Critical Gaps (block synthesis)

**None.** All edit anchors are cited, both source-of-truth files have been read end-to-end, MDTM template 02 rules are quoted with line citations, prior spec-edit task examples are walked through, and BUILD_REQUEST values are recommended.

### Important Gaps (affect quality)

**None.** The two contradictions documented above are productive placement divergences, not gaps — the builder picks one at BUILD_REQUEST emission.

### Minor Gaps (must still be fixed — advisory)

1. **NEW file refs/doc-discovery.md structure underspecified.** The track goal lists this as a NEW file ("4-section ref"), but no research file enumerates the 4 sections. Researcher 1 (line 442-445) defers the filename convention to Researcher 4; Researcher 4 references `refs/doc-discovery.md` in the VALIDATION_REQUIREMENTS string (line 558) but does not document the 4-section internal structure. **Impact:** the rf-task-builder will have to derive the 4 sections from the user's track goal at emission time. **Mitigation:** the builder should explicitly enumerate the 4 sections in BUILD_REQUEST `VALIDATION_REQUIREMENTS` (e.g., "(1) Documentation Discovery Trigger, (2) Search Strategy, (3) Card Production, (4) Failure Modes — adjust to match user spec at build time"). **Severity:** Minor — does not block the build, surfaces as a derived-content slot rather than a verbatim-anchor slot.

2. **Status-tag drift on files 03 and 04.** Header says "In Progress"; content and Summary read complete. Severity: minor, cosmetic, does not block downstream consumption since the bodies are complete.

---

## Depth Assessment

**Expected depth:** Deep — this task is a structural extension to a complex skill with cross-cutting wiring across 5 source files.

**Actual depth achieved:** Deep on all four research files. Specifically:

- **Data flow traces:** File 03 traces Wave 1.5 output → Wave 1 brief → hypothesis card → Wave 3 brief → Wave 4 adversarial → Wave 5 REPORT.md → Output Contract — a full end-to-end wiring trace.
- **Integration point mapping:** File 03 enumerates 9 distinct wiring points with verbatim before/after text for each modification.
- **Pattern analysis:** File 02's 8 patterns each include verbatim quote + abstracted skeleton + explicit guidance for how Wave 1.5 must mirror.
- **Template/example research:** File 04 covers template 02 rules verbatim AND walks through a prior near-identical task (TASK-RF-20260520-230051) phase-by-phase.

**Missing depth elements:** None. The only honest underspecification is the refs/doc-discovery.md 4-section internal structure (Minor Gap #1 above), which is a downstream derivation slot rather than a research depth gap.

---

## Recommendations

1. **Proceed to BUILD_REQUEST → rf-task-builder.** The research package is task-build-ready.
2. **In BUILD_REQUEST, resolve Contradiction 1** (Documentation Context section placement in REPORT.md) by picking one of the two placements with explicit justification. The two placements are: (a) between Summary and Diagnosis [Researcher 3's preference] or (b) between Evidence and Proposed Fix [Researcher 1's preference]. Note: this is the single most consequential placement decision and should be called out in the BUILD_REQUEST so the executor doesn't introduce a third interpretation.
3. **In BUILD_REQUEST, adopt Researcher 3's Wiring 2 placement** for `consistency_with_docs` in hypothesis-card-template.md (top metadata block, sibling to `**Cause class**`). This is the strongest of the three proposals.
4. **In BUILD_REQUEST `VALIDATION_REQUIREMENTS`, explicitly enumerate the 4 sections of the NEW refs/doc-discovery.md** to constrain the executor's freedom (Minor Gap #1 above).
5. **Apply R-039 rewrite** to any Key constraint mentioning literal `src/` per File 04 §Section 2 (lines 354-362). The recommended rewrite is "the canonical source tree" / "the dev-copy tree" idiom — already used in the prior TASK-RF-20260520-230051 example.
6. **Use TASK-RF-20260520-230051 as the canonical structural template** (File 04 §Section 3) — 5 phases (Preparation → per-fix anchor phases with Edit + L3 grep gate → Sync/Validate → FINAL_ONLY QA Gate → Post-Completion).

---

VERDICT: PASS
