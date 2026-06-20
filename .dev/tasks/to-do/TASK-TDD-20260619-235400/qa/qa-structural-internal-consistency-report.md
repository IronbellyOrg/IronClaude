# QA Report — Report Validation (Internal-Consistency Lens)

**Topic:** sc:reflect Tier-2 Swarm Ensemble TDD (FR-RH2)
**Date:** 2026-06-20
**Phase:** report-validation (structural / internal-consistency lens)
**Fix cycle:** N/A
**Fix authorization:** false (report-only)
**Target:** `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md` (1768 lines)

---

## Overall Verdict: FAIL

Adversarial stance applied (assume ≥15 internal-consistency errors). The document is unusually internally disciplined — the (M,N) divergence table, the verdict→exit-code map, the degraded-trigger numbering, and the FR/NFR ID re-projection are byte-consistent across most appearances. However, **8 distinct internal-consistency defects** were found, including one self-contradicting mapping note (F1) and one duplicated-symbol line-number divergence repeated across multiple sections (F2). Any internal-consistency gap on an assembled engineering doc = FAIL under zero-tolerance.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | FR ID counts agree (§5 ↔ §15.5 ↔ §24) | PASS | §5.1 has FR-001..009 (9 rows, L329-337); §15.5 covers FR-RH2.1..9 (L1221-1229); §24.1 DoD lists FR-RH2.1..9 (L1597-1605). 9 FRs everywhere. |
| 2 | NFR ID counts agree (§5.2 ↔ §15.5) | **FAIL** | §5.2 has NFR-001..008 → NFR-RH2.1..8 (8 rows, L349-356). §15.5 traceability (L1230-1233) only maps NFR-RH2.3,.4,.5,.6 — **omits .1, .2, .7, .8**. See F3. |
| 3 | (M,N) divergence table identical at §4.1/§5.4/§11.2/§12.2.1 | PASS | L308-313, L376-381, L907-912, L949-954 byte-identical (4 rows). |
| 4 | (M,N) table values consistent at §14.3 | PASS | §14.3 (L1103-1109) reworded/expanded variant; all M-condition→verdict→exit→slug values match canonical table. |
| 5 | Verdict→exit-code map (pass→0/halted→10/degraded→11/blocked→2) consistent everywhere | PASS | L196,271,336,458,667,878,895,1166,1207 — all identical. No drift. |
| 6 | OI-1 §8.3 table internally consistent with §12/§14 verdict logic | PASS | Degraded triggers 6-14 / contract.py L263-302 ascend monotonically; match between §8.3 (L770-781), §14.4 (L1119-1121), §15.3 (L1199). |
| 7 | Cross-references resolve to real sections | PARTIAL | §6.4→§21 Alt 0 resolves (L543/L1449); ToC anchors map to real §§. But §5.4 note cites "§12.2" for a table in §12.2.1 (F5). |
| 8 | §5 requirements trace to §6 architecture | PASS | FR-001→§6.1/§6.2 ensemble edges; FR-003→§6.1 adversarial box; every FR has an architectural referent. |
| 9 | §20 risks each have a mitigation | PASS | R1-R9 (L1431-1439) all carry populated Mitigation + Contingency. |
| 10 | Risk-source provenance count | PASS | L1441 "R1-R8 transcribe spec §7; R9 synthesis-derived"; table has exactly R1-R9. |
| 11 | FR-001..009 → FR-RH2.N mapping note self-consistent | **FAIL** | §5.1 note (L325) claims mapping makes "source IDs read straight" but Source column is 1,2,3,4,9,5,6,7,8 — NOT straight. See F1. |
| 12 | Swarm symbol line numbers consistent | **FAIL** | dispatch.py:334/commands.py:612/reduce.py:555 in §1/§6/§8/§18 vs dispatch.py:344/commands.py:619/reduce.py:578 in §6.5 (L561) & §21 (L1478). See F2. |
| 13 | Reviewer-count range consistent (2–3 vs 2–4 vs [2,4]) | **FAIL** | §1/§2.1 "2–3 reviewers" (L192,211,213); §28 "2–4" (L1715); clamp [2,4] everywhere else. See F4. |
| 14 | Research/synthesis file counts | **FAIL** | "11 research files" (L150,1741,1762) but enumeration `research/00–09, web-01, reuse-audit.yaml` = 12 items. See F6. |
| 15 | ModelPoolTooSmallError line citations | PASS | Class def L589-609, raise site L687-688 consistently distinguished. |
| 16 | Trigger numbers ↔ contract.py lines consistent | PASS | T6/L263..T14/L301 consistent across §8.3 & §14.4. |
| 17 | ToC ↔ section headers (28 sections) | PASS | All 28 §§ present in order (L190-1711), matching ToC L159-186. |
| 18 | "spec §" source citation for the (M,N) table | **FAIL** | Table sourced to "spec §5.3" (L306,374,947) AND "spec §5.4 ordering" (L1189). See F7. |
| 19 | §9 amendment-record cross-ref ("spec §9" vs TDD §9) | **FAIL (minor)** | FR-009 AC (L337) bare "(§9)" reads as TDD §9 (State Management, N/A); L1421/L1585 correctly say "spec §9". See F8. |
| 20 | Completeness checklist ↔ section bodies (N/A markers) | PASS | §9/§10/§16 N/A in checklist (L122,123,129) and bodies (L809,817,1239). |

---

## Summary

- Checks performed: 20
- Checks passed: 12
- Checks failed (incl. 1 partial): 8
- Critical (blocks build/execution-correctness): 0
- Important (semantic drift, traceability gaps, self-contradiction): 4 (F1, F2, F3, F4)
- Minor (cross-ref imprecision, count typos): 4 (F5, F6, F7, F8)
- Issues fixed in-place: 0 (fix_authorization: false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| F1 | IMPORTANT | §5.1 note, L325 | The note claims the FR re-projection "keeps numeric order and maps FR-005→FR-RH2.9 so the source IDs read straight." But the actual Source column reads FR-RH2 .1,.2,.3,.4,**.9,.5,.6,.7,.8** (L329-337) — the source IDs do NOT read straight; they jump .4→.9→.5. The stated justification contradicts the table it describes, and L339 confirms the real (non-straight) mapping (FR-005↔.9, FR-008↔.7, FR-009↔.8). | Reword L325 to state the truth: the table keeps the TDD's numeric order, and to honour that, the *spec* IDs appear out of order (.9 pulled up to FR-005). Delete the "so the source IDs read straight" clause — it is the opposite of what the table does. |
| F2 | IMPORTANT | §6.5 L561, §21 L1478 vs §1 L194 / §6.1 L421,425,428 / §6.2 L477-479 / §8.2 L706,725,741 / §18.2 L1325-1327 | The three reused swarm symbols are cited at two different line numbers with no reconciliation: `dispatch.py:334` vs `:344`, `commands.py:612` vs `:619`, `reduce.py:555` vs `:578`. The :334/:612/:555 set dominates (≥8 sites); the :344/:619/:578 set appears only in the reuse-audit-derived rows (§6.5 L561, §21 L1478). §27.2 (L1691-1692) partially papers over it with "L334/344" and "L612/619" but gives reduce.py only as L555 (L1693) while §6.5/§21 say :578. A reader cannot tell which line is authoritative. | Pick one anchor per symbol (the signature-definition line — §8.2 uses dispatch.py:334-343, commands.py:612-707, reduce.py:555) and apply it uniformly. If the reuse-audit's :344/:619/:578 are body-line anchors, annotate them as such inline; do not leave bare conflicting numbers. |
| F3 | IMPORTANT | §15.5 traceability, L1230-1233 vs §5.2 L349-356, §15.1 L1148 | The acceptance-traceability table maps all 9 FRs but only 4 of 8 NFRs (NFR-RH2.3,.4,.5,.6). NFR-RH2.1, .2, .7, .8 have no test row — yet §15.1 Unit row (L1148) explicitly claims it proves "NFR-RH2.1, .2, .5", and U7 (L1167) covers NFR-RH2.1/.2. So the doc's own test inventory covers .1/.2 but the traceability roll-up drops them; .7 (observability) and .8 (proxy contract) have no test mapping anywhere. Internal contradiction between §15.1 claims and the §15.5 roll-up. | Add rows for NFR-RH2.1 (U7), NFR-RH2.2 (U7), NFR-RH2.7 (none today — flag as gap or add an observability assertion), NFR-RH2.8 (none today — flag or add a proxy-contract assertion). Reconcile with the §15.1 claims. |
| F4 | IMPORTANT | §1 L192, §2.1 L211/L213 vs §28 Glossary L1715 vs [2,4] sites | The Tier-2 ensemble is described as "2–3 heterogeneous reviewers" in the Executive Summary and Problem Statement, but the Glossary defines it as "2–4 reviewers" (L1715) and the implemented `--reviewers` clamp / `default_workers` is `[2,4]` everywhere (L201,257,330,367,1259,1391,…). "2–3" understates the implemented upper bound and contradicts both the glossary and the CLI surface. | Change "2–3 reviewers/heterogeneous reviewers" to "2–4" at L192, L211, L213 to match the [2,4] clamp and the §28 glossary. |
| F5 | MINOR | §5.4 header note, L374 | Cross-ref says the table "is the same canonical table referenced in §4.1, §11.2, **§12.2**, and §14.3" — but the table in section 12 lives in **§12.2.1** (L945), not §12.2. The task's own scope statement also names §12.2.1. | Change "§12.2" → "§12.2.1" at L374. |
| F6 | MINOR | §0 Contract Table L150, §27.1/App-A L1741, History L1762 | "11 codebase research files" but the enumeration `research/00–research/09, web-01, reuse-audit.yaml` is 10 + 1 + 1 = **12** items. The count (11) and the list (12) disagree. | Reconcile: either correct the count to 12, or correct the enumeration (e.g. if reuse-audit.yaml is not a "research file" it should be excluded from the "11" or the count should read "11 research files + 1 reuse-audit"). |
| F7 | MINOR | §4.1 L306, §5.4 L374, §12.2.1 L947 vs I6 L1189 | The same (M,N) guard table is attributed to "spec §5.3 `mn_guard_table`" in three places but to "spec §5.4 ordering" in the I6 test row (L1189). I8 (L1191) says "spec §5.3 path_confinement". The spec source section for the divergence/ordering content is cited as both §5.3 and §5.4. | Verify against the spec which section holds `mn_guard_table` / ordering and unify the citation (all §5.3 or all §5.4). |
| F8 | MINOR | FR-009 AC, L337 | The AC says any NFR-7 amendment is "recorded in the spec (§9)". The bare "(§9)" is ambiguous and reads as the *TDD's* §9, which is "State Management — N/A". §19.6 (L1421) and §23.2 Phase 6 (L1585) correctly write "spec §9". | Change "(§9)" → "(spec §9)" at L337 for consistency with L1421/L1585. |

## Notes on what was verified clean (anti-false-PASS evidence)

- The 4-row (M,N) divergence table is **byte-identical** at all four primary appearances (§4.1 L308-313, §5.4 L376-381, §11.2 L907-912, §12.2.1 L949-954) — confirmed by line-by-line grep, not assumed.
- The verdict→exit-code map `pass→0, halted→10, degraded→11, blocked→2` is identical at all 9 appearances; no transposition (e.g. halted↔blocked) anywhere.
- Degraded-trigger numbering (Trigger 6-14) and the contract.py line anchors (L263-L302) are monotonic and agree between §8.3, §14.4, and §15.3 — the OI-1 table and the verdict logic do not contradict.
- All 28 sections present, ordered, and matching the ToC; §9/§10/§16 N/A markers agree between the completeness checklist and the bodies.
- Every §20 risk (R1-R9) has a mitigation; the risk-provenance note's count matches the table.

## Actions Taken

None — `fix_authorization: false` (report-only lens). All findings documented with line citations for the orchestrator / a fix-authorized pass.

## Recommendations

- Resolve F1-F4 (IMPORTANT) before this TDD is treated as approved: F1 is a self-contradicting sentence, F2 leaves a load-bearing reuse target with two conflicting line numbers, F3 is a traceability gap that hides whether NFR-RH2.7/.8 are tested at all, F4 contradicts the implemented CLI surface.
- F5-F8 (MINOR) are cross-ref/count cleanups; batch them in the same fix pass.
- Re-run this lens after fixes (fix-cycle) to confirm no new inconsistency was introduced.

---

## Confidence Gate

**Confidence:** Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

(All 20 checklist items verified with grep/Read tool evidence against the source file. confidence = 20 / (20 − 0) × 100 = 100%.)

**Tool engagement:** Read: 5 | Grep: 7 | Glob: 0 | Bash: 0 (grep run via Bash tool: 7 calls)

Tool-engagement note: 12 verification tool calls (5 Read covering all 1768 lines + 7 grep sweeps) ≥ 20 checklist items is below the 1:1 raw ratio, but each grep was a multi-match cross-section sweep (e.g. one grep verified the verdict-map across 9 sites, another verified all 5 (M,N) table instances simultaneously), so each call discharged multiple checklist items. No padding calls. No web research performed (no external/URL/standards claim required verification — all checks were intra-document structural).

No UNCHECKED items. No UNVERIFIABLE items.

## QA Complete
