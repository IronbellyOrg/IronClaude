# QA Report — TDD Qualitative Review (CROSSREF-CHAIN lens)

**Topic:** sc:reflect Tier-2 Reviewer Ensemble Swarm Re-Wiring TDD (FR-RH2)
**Date:** 2026-06-20
**Phase:** tdd-qualitative (report-validation, CROSSREF-CHAIN lens)
**Fix cycle:** N/A (fix_authorization: false — report-only)
**Document:** `.dev/reflect-hardening/issue-2-headless-ensemble/tdd.md` (1768 lines)
**Adversarial stance:** "Assume ≥15 broken cross-reference chains exist. Find them."

---

## Overall Verdict: FAIL

One genuine broken cross-reference (CRITICAL-for-lens: a citation to a spec section that does not exist) plus one
internal-anchor inconsistency (IMPORTANT) were found by following the chains end to end. The adversarial premise
("≥15 broken chains") is **not** borne out — the document's cross-reference web is unusually disciplined and the
overwhelming majority of links resolve, including the load-bearing OI-1 → §8.3 → §22 Q1 BLOCKING chain and every
code-terminated citation I spot-verified. But "fewer than expected" is not "zero," and the two defects below are real
and must be fixed before this TDD is trusted as the implementation contract.

---

## Items Reviewed

| # | Chain traced | Result | Evidence |
|---|--------------|--------|----------|
| 1 | FR-RH2.N → §5 requirement → §6 architecture → §15 test (sampled FR-RH2.1/.3/.4/.9) | PASS | See §"FR chains" below; all four resolve end-to-end with matching IDs in §5.1, §6.1/§6.2, §15.2/§15.3, §15.5 traceability |
| 2 | OI-1 → §8.3 correspondence table → §22 Q1 BLOCKING | PASS | OI-1 named in §5.1 (FR-003, L331/L341), §6.4 D5 (L551), §7 (L629/L663/L680), §8.3 (L761-793), §18.4, §19.1 Phase 0, §23 M0; §22 Q1 (L1520) is the BLOCKING gate; all mutually consistent |
| 3 | each §20 risk → its mitigation | PASS | R1–R9 (L1431-1439) each carry a non-empty, on-point Mitigation + Contingency column; R2/R3/R6 mitigations correctly cross-ref OI-1/FR-RH2.8/FR-RH2.3 |
| 4 | each §21 alternative → its "Why Not Chosen" | PASS | Alt 0/1/2 each have an explicit **Why Not Chosen** (L1465/L1482/L1499); Integration sub-decision has Pros/Cons + chosen rationale (L1501-1512) |
| 5 | §22 Open Questions ↔ §12/§19/§14 edge cases (ensemble-empty, NFR-7, --suspect-source) | PASS | ensemble-empty: §12.2.1 L951 + §14.4 L1123 + §15.3 I6 → §22 Q6 (L1525); NFR-7: §19.6 L1408/L1421 + R3/R9 → §22 Q2 (L1521); --suspect-source: §18.2 L1330 + §18.4 L1348 → §22 Q5 (L1524). All bidirectional. |
| 6 | §1 deliverables → appear in §6/§8 | PASS | All 4 deliverables (`ensemble.py`, `reflect-review` lens, `test_ensemble_stub_integration.py`, NFR-7 guard ext) recur in §6 (§6.1 diagram, §6.2 graph, §6.5 audit) and §8 (§8.1/§8.2/§8.3) and §15 |
| 7 | S4 directive — no orphaned "(Dn)" scaffolding cross-refs | PASS | `grep -E "\(D[0-9]+\)"` over tdd.md → **0 hits**. §6.4 uses D1–D5 as table-local decision labels with no dangling "(Dn)" pointers; the §6.4 preamble (L543) explicitly states "decision rows below are self-contained and do not cross-reference any external scaffolding labels." Directive held. |
| 8 | spec-section cross-refs (spec §5.3, §5.4, §7, §9, §4.6) | **FAIL** | TDD §15.3 I6 (L1189) cites **"spec §5.4 ordering"** — spec has NO §5.4 (headers: §5.1, §5.3 only). The mn_guard_table + ordering live in spec **§5.3** (spec L447). Broken spec cross-reference. |
| 9 | internal §5.4 anchor consistency (§4.1/§11.2/§14.3 ↔ TDD §5.4) | **FAIL (IMPORTANT)** | TDD §11.2 (L905) and §14.3 (L1101) reference the guard table as "(§4.1 / §5.4)" / "(§5.4)" — these resolve to the TDD's own §5.4 (L372, correct). But §15.3 I6 (L1189) writes "spec §5.4" for the SAME ordering fact, conflating the TDD's §5.4 with a nonexistent spec §5.4. Inconsistent anchoring of one fact across rows. |
| 10 | code-terminated citations underpinning chains (spot-verified vs shipped source) | PASS | runner.py:403, contract.py:267/280-281, dispatch.py:334, commands.py:589/612, reduce.py:555/648/140, merge.py:50, bare_review LensEntry, reflect/commands.py:320/325/327, contract.py:65, models.py:58/86/89 — ALL verified exact. `ensemble.py`/`reflect_review.py` correctly marked NET-NEW (confirmed absent). |

---

## Summary

- Chains traced: 10 / 10
- Chains passing: 8 / 10
- Chains failing: 2 (items 8 + 9 — the same root defect, manifesting as a broken spec-ref and an internal anchor inconsistency)
- Critical issues: 1 (broken cross-reference to a nonexistent spec section)
- Important issues: 1 (inconsistent anchoring of the same ordering fact)
- Minor issues: 0
- Issues fixed in-place: 0 (fix_authorization: false)
- Adversarial premise ("≥15 broken chains"): **NOT confirmed** — 2 found, not 15+. Reported honestly rather than manufacturing findings to hit a quota.

---

## FR chains (item 1 detail — the four sampled FRs)

| Sampled FR | §5 requirement | §6 architecture component | §15 test | Verdict |
|---|---|---|---|---|
| FR-RH2.1 (→ FR-001, L329) | FR-001 row present, source col `FR-RH2.1` | §6.1 seam diagram (`_audit_once` expected_tier==2 → ensemble.py); §6.2 edge `runner.py→ensemble.py` | U3, U7 (L1163/1167); §15.5 maps FR-RH2.1→U3,U7,B2 | resolves |
| FR-RH2.3 (→ FR-003, L331) | FR-003 row, gated-by-OI-1 callout | §6.4 D3 (Mode A scores); §6.2 edge `ensemble.py→/sc:adversarial` | U8, I1 (L1168/1184); §15.5 FR-RH2.3→U8,I1 | resolves |
| FR-RH2.4 (→ FR-004, L332) | FR-004 row, diversity-over-M AC | §6.1 "Diversity over M not N" invariant (L465); §11.1 step 6 | I1, U5; §15.5 FR-RH2.4→I1,U5 | resolves |
| FR-RH2.9 (→ FR-005, L333) | FR-005 row + explicit mapping note (L325) FR-005↔FR-RH2.9 | §5.4 (M,N) table; §11.2; §12.2.1; §14.3 | I3,I4,I5,I6; §15.5 FR-RH2.9→I3-I6 | resolves |

The FR-005↔FR-RH2.9 renumbering (TDD keeps numeric order, spec sequences .9 after .4) is explicitly documented at L325/L339 and the §15.5 traceability table closes every FR/NFR. No FR is orphaned; no test cites a nonexistent FR.

---

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | CRITICAL | tdd.md §15.3, row I6, L1189 (`FR-RH2.9; spec §5.4 ordering`) | **Broken spec cross-reference.** The TDD cites "spec §5.4 ordering" as the authority for the M==0→blocked ordering. The source spec (`spec.md`) has no §5.4 — its section headers are §5.1 (CLI Surface) and §5.3 (Phase Contracts); the `mn_guard_table` and the `blocked → degraded → halted → pass` ordering are defined under spec **§5.3** (spec.md L447). A reader following "spec §5.4" lands nowhere. This is the only genuinely dangling cross-reference in the document. | Change I6's trailing citation from `spec §5.4 ordering` to `spec §5.3 mn_guard_table ordering` (matching the §15.3 I8 row directly below it, which correctly cites `spec §5.3 path_confinement`, and matching TDD §5.4's own preamble L374 "Reproduced from spec §5.3"). |
| 2 | IMPORTANT | tdd.md §15.3 I6 (L1189) vs §11.2 (L905) / §14.3 (L1101) | **Inconsistent anchoring of one fact.** The verdict-ordering fact is cited three ways: §11.2/§14.3 reference the **TDD's own §5.4** ("(§4.1 / §5.4)", "(§5.4)") — correct, since TDD §5.4 (L372) is the "(M,N) Divergence Guard Table"; but I6 attributes the same ordering to "**spec** §5.4". The same fact must not be anchored to both an existing internal §5.4 and a nonexistent spec §5.4. This ambiguity will mislead an implementer about where the canonical ordering lives. | Make I6 consistent with §11.2/§14.3: cite the internal `§5.4` (TDD guard table) and/or `spec §5.3` for the upstream source — never "spec §5.4." Recommend: `FR-RH2.9; §5.4 / spec §5.3 ordering`. |

> **Note on a non-finding (spec §9):** The TDD's NFR-7 amendment text (§19.6 L1421, FR-009 L337, R3 L1433, Q2 L1521) repeatedly directs the NFR-7 amendment to be "recorded in spec §9." Spec §9 is "Migration & Rollout," which is a semantically odd home for an NFR amendment. **However, this is NOT a TDD-introduced broken link:** the source spec itself instructs exactly this (spec.md L319 "the amendment is recorded in this spec (§9)", L587 "record in §9"). The TDD faithfully transcribes the spec's own self-reference, and spec §9 does exist. Flagging for downstream awareness only — the chain is faithful, so it does not count against this lens.

---

## Actions Taken

None — `fix_authorization: false`. Both findings are documented above with exact line numbers and specific fixes for the author to apply.

---

## Self-Audit (MANDATORY)

1. **How many factual claims independently verified against source code?** 22 code-terminated citations grep/sed-verified against shipped source across 6 files: `runner.py` (L403, _audit_once L392), `reflect/contract.py` (derive_verdict L130, _degraded_reason L249, L267 t2_model_class_diversity, L280-281 single-reviewer-fallback, parse_contract L65, _make_result L104), `reflect/models.py` (ReflectConfig L58, max_fix_iterations L86, contract_path L89), `reflect/commands.py` (subprocess.run/tmux L320/325/327), `swarm/dispatch.py` (dispatch_wave1 L334 signature), `swarm/commands.py` (ModelPoolTooSmallError L589, _resolve_run_transport_factory L612, _resolve_run_transport L510), `swarm/reduce.py` (reduce_wave3 L555, workers_succeeded L648, DONE_SENTINEL_FILENAME L140, emit_done_sentinel L402/456), `swarm/merge.py` (mechanical_merge L50), `swarm/lenses/bare_review.py` (LensEntry suspect=True/tier=T2 L63-64). Plus NET-NEW absence confirmed for `ensemble.py` + `reflect_review.py`. Plus spec-section-header enumeration verified against `spec.md`.
2. **What specific files did I read?** The full TDD (1768 lines, read in 4 passes), `spec.md` (header map + FR/NFR/mn_guard_table/path_confinement/§9 anchors), and the 6 shipped source files above via Grep/sed.
3. **If I found few issues, why trust I checked thoroughly?** I did NOT find zero — I found 2, and I rejected a 3rd candidate (spec §9) after verifying it was a faithful transcription, not a broken link. Every PASS chain in the Items table cites the specific line numbers I followed (e.g., OI-1 traced across 8 distinct sections L331→L1520). The adversarial premise asked for ≥15; I report 2 and explain why the premise overshot rather than padding the count — manufacturing 13 phantom findings to hit a quota would itself be a QA failure. The tool-engagement count (below) exceeds the chains traced, satisfying the minimum.
4. **Web research?** None performed — this lens is entirely local-file-bound (TDD ↔ spec ↔ shipped source). Tavily not invoked; no fallback occurred. Nothing to record in a Tool-engagement web summary.

---

## Confidence

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 5 | Grep/Bash-grep: 7 | Glob: 0 | Bash(sed): included in Bash count
- All 10 chains were traced to a concrete resolution with cited line numbers; no chain was left unchecked, none was unverifiable.
- Tool-engagement minimum satisfied: 12 tool invocations ≥ 10 chains traced.

## Recommendations

1. Apply Issue #1 (CRITICAL): change I6's `spec §5.4` → `spec §5.3` (the mn_guard_table's real home). One-token fix, but it is a dangling pointer in the load-bearing test-strategy section.
2. Apply Issue #2 (IMPORTANT): harmonize I6's ordering citation with §11.2/§14.3 so the verdict-ordering fact is anchored consistently (internal §5.4 and/or spec §5.3, never "spec §5.4").
3. Optional (advisory, not a finding): consider whether the spec's own choice to record the NFR-7 amendment in spec §9 (Migration & Rollout) should be revisited upstream in the spec — but that is a spec defect, not a TDD cross-reference defect, and out of scope for this lens.
4. After fixing, no re-trace of the other 8 chains is needed — they passed cleanly with full line-cited evidence.

## QA Complete
