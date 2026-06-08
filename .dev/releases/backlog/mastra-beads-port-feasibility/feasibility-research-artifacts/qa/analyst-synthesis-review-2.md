# Synthesis Quality Review (Partition 2 of 2)

**Date:** 2026-06-02
**Analysis type:** synthesis-review
**Topic:** Mastra + Backlog.md + Beads port feasibility report
**Reviewer:** rf-analyst
**Files reviewed:** 3

**Assigned files:**

- `synthesis/synth-04-options-recommendation.md` (Report Sections 6-7)
- `synthesis/synth-05-implementation-roadmap.md` (Report Section 8)
- `synthesis/synth-06-risk-questions-evidence.md` (Report Sections 9-10)

**Verification corpus read for cross-validation:** `research/03-sprint-execution-runtime.md`, `research/07-target-data-model-and-ownership.md`, `research/09-gap-fill-checkpoint-contract.md`, `gaps-and-questions.md`, and spot-checks of `research/web-01..04`.

> **[PARTITION NOTE: Cross-file checks (check 7 cross-section consistency, check 10 key-finding coverage) limited to the assigned subset synth-04/05/06. Full cross-file analysis against synth-01/02/03 requires merging partition 1's report.]**

---

## Overall Verdict: PASS (0 blocking issues; 2 minor advisory notes)

All three files pass all nine checklist items plus the special-verification items (Option D genuine-deferral, confidence band, four honesty statements). Two minor advisory notes are recorded for the merge step but neither blocks assembly.

---

## Per-File Review

### synth-04-options-recommendation.md (Sections 6-7)

**Sections covered:** 6.0 Scoping facts (F1-F11), 6.1-6.4 Options A/B/C/D, 6.5 Options Comparison, 7.1 Verdict, 7.2 Rationale, 7.3 Spike exit gates, 7.4 Honesty statements, 7.5 Bottom line.
**Verdict:** PASS

| Check # | Check | Result | Evidence / Issue |
|---------|-------|--------|------------------|
| 1 | Section headers match Report Structure | PASS | Section 6 (Options) and Section 7 (Recommendation) present, in order, with the expected subsection skeleton (per-option tables → comparison → verdict → rationale → honesty). |
| 2 | Table structures correct | PASS | Each option (6.1-6.4) uses the Effort/Risk/Reuse/Files/Pros/Cons dimension table. 6.5 comparison table has criterion + 4 option columns (Effort, Risk, Maintainability, Integration, Reuse, Multi-tenant readiness). 7.x uses Field/Value and Gate/Retires/Evidence tables. |
| 3 | No fabrication | PASS | Spot-traced load-bearing claims: F4 LOC (8,568 / executor.py 2,148) matches `research/03:10` verbatim; F1 `claude --print --verbose ... --output-format` seam matches `research/03:76` & `research/07:36`; the sprint stress-test quote ("Any Mastra port that only models phases and tasks…") matches `research/03:133` verbatim. No invented claims found. |
| 4 | Citations use actual file paths/URLs | PASS | Uses `RES/<file>:<line>` and `web-0N:line` conventions, defined explicitly in the evidence-convention header. Web-01 EE-licensing claims (F8) trace to `web-01` §6/§10 (verified). See Minor Note A on one line-offset. |
| 5 | Options analysis has 2+ options w/ pros/cons AND recommendation referencing comparison | PASS | Four options, each with Pros AND Cons rows. 7.2 "Rationale against the comparison" explicitly references the 6.5 comparison via a Why-A-over-B/C/D table. |
| 6 | Implementation plan steps specific | N/A | Section 8 (roadmap) is in synth-05. 7.3 spike gates (G1-G4) are specific and evidence-targeted, not generic. |
| 7 | Cross-section consistency | PASS | Gaps surfaced as options/risks; options→recommendation traceable (A chosen, B/C/D explained); Option D preserved as genuine, not silently answered. |
| 8 | No doc-only claims in Implementation Plan | N/A | No S8 content here; honesty statements correctly tag EE/Beads/Backlog claims to web sources, not docs. |
| 9 | Stale-doc/unverified surfaced | PASS | `[UNVERIFIED]` Mastra supervision parity carried into 6.2 Risk, 7.1, and G1; not promoted to fact. Explicit guardrail statement in synthesis summary. |

### synth-05-implementation-roadmap.md (Section 8)

**Sections covered:** 8.0 Ground rules, 8.1-8.6 Phases 0-5, 8.7 Consolidated decision gates, 8.8 Validation/eval strategy, 8.9 Summary.
**Verdict:** PASS

| Check # | Check | Result | Evidence / Issue |
|---------|-------|--------|------------------|
| 1 | Section headers match Report Structure | PASS | Section 8 with a coherent phased structure (Phase 0-5), each phase having Goal / Dependencies / step table / Go-No-Go gate. |
| 2 | Table structures correct | PASS | Every phase step table uses the **Step / Action / Files-or-systems / Details** column structure required by the template. Phase-overview, decision-gate, and validation-strategy tables are well-formed. |
| 3 | No fabrication | PASS | Sample-traced: checkpoint contract steps (0.3, 1.7, 3.6) match `research/09:127-154`, `09:121` (per-task branch skips `_verify_checkpoints()`), `09:48` (checkpoints.py accepts both forms) verbatim. Parser-compatibility step 0.2/1.6 matches `research/07:125,138`. The `tasklist validate` pilot rationale (8.3) is consistent with the single-step/strict-gate framing. |
| 4 | Citations use actual file paths/URLs | PASS | Cites `file:line` for codebase contracts (`sprint/config.py:374-377`, `executor.py:1259-1301`, `09-...:131-141`) and `web-0N:line` for external. Mixed-corpus example paths (`.dev/releases/complete/cliEval/phase-1-tasklist.md:251`) match `research/09:88` evidence. |
| 5 | Options analysis 2+ w/ recommendation | N/A | Options analysis is synth-04. synth-05 correctly states it assumes Option A (with an explicit note that synth-04 was absent at write time) and corroborates via `07-...:173`. See Minor Note B. |
| 6 | Implementation plan steps specific | PASS | Steps name concrete files, functions, and CLI verbs (`discover_phases()`, `parse_tasklist_file()`, `bd ready --json`, `bd update --claim`, `WorkspaceSandbox.executeCommand()`, `roadmap/executor.py:2003-2204` step graph). No generic "create a service" placeholders; the one genuinely-deferred build (control plane, 4.2) is explicitly `[DECISION-GATED]`. |
| 7 | Cross-section consistency | PASS | Decisions D1-D5 introduced in Phase 0 and consistently gated through Phases 4-5 and re-tabulated in 8.7. Go/No-Go gates G0-G5 chain correctly. Checkpoint gap (0.3) flagged as Phase 3 risk and resolved in step 3.6. Pilot pipeline (Phase 2) reused in 5.1. |
| 8 | No doc-only claims in Implementation Plan (S8) | PASS | All buildable steps anchor to code-traced contracts (research 02/03/07/09). External capabilities are gated as `[DECISION-GATED]`/`[UNVERIFIED]` (e.g. 0.7 D4, 2.3 safety spike, 2.4 durability) — never asserted as existing capability inside a build step. The Phase 4 governance plane is scoped as net-new, not described as a doc-sourced existing feature. |
| 9 | Stale-doc/unverified surfaced | PASS | Step 0.3 records the `_verify_checkpoints()` per-task gap as a Phase 3 risk; 1.7 mandates normalizing legacy `### Checkpoint:` headings; 3.2 explicitly says "Preserve, do not normalize" the `CERTIFY_GATE` not-wired-in-production fact — directly honoring `gaps RG-I6` and `research/09` stale-doc findings. |

### synth-06-risk-questions-evidence.md (Sections 9-10)

**Sections covered:** 9.A Strategic open questions (Q1-Q6), 9.B Verification/parity open questions (Q7-Q13), Risk Register (R1-R9), Section 10 Evidence Trail (10.1-10.6), Summary.
**Verdict:** PASS

| Check # | Check | Result | Evidence / Issue |
|---------|-------|--------|------------------|
| 1 | Section headers match Report Structure | PASS | Section 9 (Open Questions) and Section 10 (Evidence Trail) present in order, with a Risk Register support block between them as scoped in the file header. |
| 2 | Table structures correct | PASS | Open Questions tables use **# / Question / Impact / Suggested-Resolution**. Risk Register uses # / Risk / Source-Evidence / Impact / Likelihood / Severity / Mitigation / Owner-Gate. Evidence Trail tables use File / Path / Topic. All conform. |
| 3 | No fabrication | PASS | Sample-traced: R3/Q1 dual-owner-drift traces to `research/07` + `research/11:100` (verified `07` flags drift in Ownership Rules §1-2 and Gaps table); R4 Beads v1.0.5 traces to `web-03` §2/§7 (verified — v1.0.5 sync warning + Dolt-first correction present). R8 governance gap traces to `web-04` §1-15 (verified). No invented risks; cross-reference line (R1↔Q6 etc.) is internally consistent. |
| 4 | Citations use actual file paths/URLs | PASS | Every Evidence Trail row carries a real path. Risk/question rows cite `research/NN`, `web-0N §N`, `gaps RG-*`, `seed-brief`. Web citations use **section-anchor** (`§N`) style — valid because web-01..04 are organized into numbered `### N.` sections (verified); this is arguably more robust than line numbers. |
| 5 | Options analysis 2+ w/ recommendation | N/A | Not an options section. |
| 6 | Implementation plan steps specific | N/A | Not a roadmap section. |
| 7 | Cross-section consistency | PASS | Open questions Q1-Q13 are NOT answered elsewhere as fact — each carries an honest "unresolved/open" marker in the Suggested-Resolution column. Risk↔Question cross-reference map (R1↔Q6, R2↔Q5/Q11, R3↔Q1, R6↔Q5, R7↔Q8/Q12, R8↔Q2, R9↔Q10) is coherent. Evidence Trail correctly indexes all 6 synth files including itself. |
| 8 | No doc-only claims in Implementation Plan | N/A | Not a build section; risks/questions correctly tag external claims to web sources. |
| 9 | Stale-doc/unverified surfaced | PASS | This file IS the surfacing surface. Stale-doc items (checkpoint contract drift R7, certify-wiring Q12), `[UNVERIFIED]` items (Q5 subprocess parity, Q10 schemas), and SoT conflict (Q7) are all carried as explicit open questions/risks. Honesty note at end re-affirms unresolved items stay open, not resolved into facts. |

---

## Special-Verification Items (per spawn prompt)

| Item | Required | Found | Status |
|------|----------|-------|--------|
| **Option D preserved as genuine deferral** | D must be a live "do not port now" option, not a strawman | synth-04 §6.4 gives D a full Effort/Risk/Reuse/Files/Pros/Cons table with real Pros ("Honest response to the large `[UNVERIFIED]` external surface… avoids committing to immature Backlog↔Beads integration prematurely"). §7.5 bottom line: "deferral (D) is a legitimate and honest choice, not a failure." synth-04 header line 3 explicitly states deferral is "a genuine, live option — a port is NOT assumed worthwhile." | PASS — genuine |
| **Verdict has a confidence band** | Verdict must carry an explicit confidence figure | synth-04 §7.1: "Confidence band — Medium (≈70%) that Hybrid adapter-first is technically feasible… Low-Medium (≈55%) that a full company-wide multi-tenant layer is deliverable on the three components alone." Dual-band, quantified. | PASS |
| **Enterprise-licensing honesty statement** | Must state EE-gating of multi-tenant RBAC/SSO/audit | synth-04 §7.4 ¶1 + synth-05 §8.5 CRITICAL FLAG 1 + synth-06 R1/Q6. Traces to `web-01` §6/§10 (verified): RBAC/FGA/SSO/audit EE-linked, OSS leaves Studio/API public. | PASS |
| **Python/TS-boundary honesty statement** | Must state pure-Python reuse is lost crossing to TS | synth-04 §7.4 ¶2: "runtime-agnostic value (gates, models, deliverable decomposition, diagnostics — F3) is pure Python… Option B forces a TypeScript re-implementation, converting reuse into rewrite-and-re-test." Echoed in synth-06 R2. | PASS |
| **Beads-churn honesty statement** | Must state Dolt-first / v1.0.5 / version-pin mandate | synth-04 §7.4 ¶3: Dolt-first (corrects seed-brief), JSONL export-only, embedded single-writer, v1.0.5 "do not upgrade", mandates version pinning + server mode + tested backup/restore. Traces to `web-03` §7/§8/§2 (verified). Echoed synth-06 R4/R5, synth-05 D5. | PASS |
| **Governance honesty statement** | Must state a separate control-plane is required beyond the 3 components | synth-04 §7.4 ¶5: "Mastra+Backlog.md+Beads is an orchestration/task substrate, not a complete enterprise platform… requires an additional control-plane service." Traces to `web-04` §1-15 (verified). Echoed synth-05 §8.5 FLAG 2 + R8/Q2. | PASS |

All six special-verification items pass.

---

## Minor Advisory Notes (non-blocking)

**Minor Note A — one line-offset citation in synth-04 (severity: trivial).**
synth-04 cites `RES/03:240` for the `[UNVERIFIED]` Mastra subprocess-supervision-parity claim (appears in §6.2, §7.1, §7.3-G1). The actual bullet ("[UNVERIFIED] Mastra exact workflow primitives for long-running subprocess supervision") is in the Gaps section of `research/03` at approximately **line 233-234**, not 240 (file is 259 lines). The cited claim is real, faithfully represented, and in the correct file — only the line anchor is ~6 lines off. **Fix (optional, cosmetic):** adjust `RES/03:240` → `RES/03:233` or cite the section instead. Does not affect any verdict or factual claim. Not a fabrication.

**Minor Note B — synth-05 self-documents an ordering artifact (severity: informational).**
synth-05 line 5 states "`synth-04-options-recommendation.md` was not present at synthesis time; Option A is therefore assumed per task instruction." This is an honest disclosure, and the Option-A assumption is independently corroborated by `07-...:173`. Now that synth-04 exists and recommends D→A (hybrid), synth-05's Option-A foundation is consistent with synth-04's recommendation — no contradiction. **Fix (optional):** the assembler may drop or soften the "not present at synthesis time" sentence in the final report since synth-04 is now present. Content is correct as-is; this is purely a presentation cleanup for the assembled report.

---

## Issues Requiring Fixes

| # | File | Check | Severity | Issue | Required Fix |
|---|------|-------|----------|-------|--------------|
| — | — | — | — | None blocking. | The two minor notes (A line-offset, B ordering artifact) are optional cosmetic cleanups for the assembly step; neither is required for a PASS. |

---

## Summary

- **Files passed:** 3 / 3
- **Files failed:** 0
- **Total issues:** 0 blocking; 2 minor advisory (both cosmetic/presentational)
- **Critical issues (block assembly):** 0
- **Special-verification items:** 6 / 6 PASS (Option D genuine, confidence band present + quantified, all four honesty statements present and source-traced)

**Cross-validation outcome:** Every load-bearing claim sampled (sprint LOC, the `ClaudeProcess` seam, the sprint stress-test quote, the checkpoint-contract contradiction, the parser round-trip surface, EE licensing, Beads Dolt-first/v1.0.5, the governance gap) was traced to its cited research/web file and matched. No fabrication detected. Citation discipline is strong; `[UNVERIFIED]` items are consistently held as options/risks/open-questions rather than promoted to current-state facts, in line with the `gaps-and-questions.md` and `research/11` synthesis guardrails.

**Recommendation:** ACCEPT synth-04, synth-05, synth-06 for report assembly. Optionally apply Minor Notes A and B as cosmetic cleanups during assembly. No re-synthesis required.

> **[PARTITION NOTE: This report covers synth-04/05/06 only. The merge step should union these findings with partition 1's review of synth-01/02/03 and re-run any global cross-section checks — specifically check 7 (do Section-4 gaps map to Section-8 roadmap steps across the full report) and check 10 (key-finding coverage from research files 01-11 across all synthesis), which span both partitions.]**
