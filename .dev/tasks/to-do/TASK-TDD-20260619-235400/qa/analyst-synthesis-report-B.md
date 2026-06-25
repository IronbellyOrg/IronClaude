# Synthesis Quality Review — Report B (rf-analyst, adversarial)

**Date:** 2026-06-20
**Analysis type:** synthesis-review (synthesis gate, pre-assembly)
**Mode:** report-only (`fix_authorization: false`)
**Stance:** ADVERSARIAL — find problems
**Reviewer:** rf-analyst (instance B)
**Worktree root:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/`
**Task dir:** `.dev/tasks/to-do/TASK-TDD-20260619-235400/`

## Files reviewed (3, assigned)

- `synthesis/synth-04-data-api.md` (TDD §7 Data Models + §8 API Specs)
- `synthesis/synth-05-state-components-flows.md` (TDD §9 State / §10 Component Inventory / §11 User Flows)
- `synthesis/synth-06-error-security.md` (TDD §12 Error Handling / §13 Security)

## Cross-check sources read in full

- `research/02-reflect-contract-verdict.md` (authoritative reflect-side OI-1 consumer field set)
- `research/05-swarm-reduce-merge-contract.md` (authoritative swarm-side OI-1 producer DM-012)
- `research/00-prd-extraction.md` (the spec's verbatim (M,N) `mn_guard_table`, §5)
- `src/superclaude/examples/tdd_template.md` (section headers + §9/§10 conditional language)
- Live source spot-checks: `cli/swarm/models.py` (`LensEntry`), `cli/swarm/reduce.py` (M), `cli/reflect/contract.py` (`merge_method` trigger)

---

## Overall Verdict: PASS — 0 blocking issues, 2 minor observations (non-blocking)

All three assigned synthesis files pass the 9-criteria Synthesis Quality Review. All four special-attention probes resolve in the synthesis files' favor. The two observations below are coverage nuances, not contradictions or fabrications, and do not gate assembly.

---

## Special-Attention Probes (the 4 explicit asks)

### (1) OI-1 field-correspondence table (synth-04 §8.3) — COMPLETE, traceable, NOT truncated to 7 rows — PASS

The §8.3 table contains **23 distinct reflect-field rows** (25 table lines incl. the duplicate `status` PASS-conjunct row and the `child_rc` call-arg row). I enumerated every reflect verdict-driver field from research 02 (the AUTHORITATIVE consumer half, Stages 1–4 + `_make_result`) and confirmed each appears as a §8.3 row:

| research-02 authoritative field | in synth-04 §8.3? |
|---|---|
| `child_rc` (call-arg) | YES (final row, F0 veto noted) |
| `contract_version` | YES (re-map warning: do NOT forward swarm version) |
| `degraded_components` | YES (list-shape → BLOCKED guard noted) |
| `tier_reached` | YES (synthesize) |
| `regression_present` | YES |
| `unauthorized_deviation_present` | YES |
| `needs_human_decision` | YES |
| `user_decision_required` | YES |
| `adversarial_unavailable` | YES |
| `input_drift_detected` | YES |
| `verification_ran` | YES |
| `t2_model_class_diversity` | YES (compute over M) |
| `t2_vendor_diversity` | YES (compute over M; `--allow-single-vendor` noted) |
| `merge_method` | YES (derive from `amalgamation_mode`+M) |
| `adversarial_convergence_score` | YES (from adversarial stage, not swarm) |
| `verification_skip_reason` | YES |
| `citations_dropped` | YES |
| `status` | YES (re-map, name-collision-only; semantics diverge) |
| `deviation_count_by_class` | YES |
| `report_path` | YES (contract-emitted via `_make_result`) |
| `remediation_task_path` | YES (FR-8: READ-only) |
| `reviewer_count` (FR/brief synth name for M) | YES (maps from `workers_succeeded`) |

**Full ≥20-field set is covered (22 reflect fields + `child_rc` call-arg = 23 rows).** Every reflect verdict field with no swarm source is correctly flagged "synthesize in ensemble.py" or "compute/derive in ensemble.py." The right column traces to research 05 (swarm DM-012 producer): the only same-name key is `status`, and synth-04 correctly flags it as **re-map not passthrough** (swarm IMM-5 worker verdict ≠ reflect tier-success), matching research 05 §6/§7 and research 02 §5. The sizing conclusion ("of ~22 reflect verdict-driver fields, exactly one has a same-name swarm key") is accurate. **Not truncated.** PASS.

### (2) §9/§10 N/A markings carry rationale (synth-05) — PASS

Both §9 (State Management) and §10 (Component Inventory) are marked `N/A — backend CLI library, no client surface` with a substantive multi-sentence rationale each, NOT a bare skip. Each rationale:
- cites the template's exact conditional language ("Backend services, infrastructure, and libraries should skip this section entirely");
- cites the template line numbers (§9 → `tdd_template.md` L580; §10 → L624) — **both verified accurate against the live template** (template L580 and L624 carry that exact sentence);
- explains the affirmative reason (synchronous backend library, no async, two on-disk YAML artifacts are the only "state surface," documented in §7/§11);
- a "Cross-cutting notes" bullet reinforces "§9/§10 are genuinely N/A, not skipped for convenience."

PASS.

### (3) (M,N) divergence table in synth-06 matches spec EXACTLY — PASS

synth-06 §12.2.1 table vs the spec's `mn_guard_table` (research 00 §5, verbatim from spec §5.3):

| Branch | synth-06 | spec | Match |
|---|---|---|---|
| `M==0` | `blocked` / `2` / `ensemble-empty` | `blocked` / `2` / `ensemble-empty` | EXACT |
| `M==1` | `degraded` / `11` / `single-reviewer-fallback` | `degraded` / `11` / `single-reviewer-fallback` | EXACT |
| `M>=2` but `<2` classes | `degraded` / `11` / `degraded-model-diversity` | `degraded` / `11` / `degraded-model-diversity` | EXACT |
| `M>=2` AND `>=2` classes | `pass-eligible` / `0` / `pass` | `pass-eligible` / `0` / `pass` | EXACT |

All four rows match verdict, exit-code, and reason-slug. The diversity-over-M (not N) qualifier and the "two same-class survivors do NOT count as full" rule are preserved. synth-05 §11.2 carries the identical table — also exact. PASS.

### (4) D3 ensemble-empty reconciliation note present in synth-06 — PASS

The D3 note is present (§12.2.1 blockquote, flagged inline at the M==0 row with `*(see D3 reconciliation below)*`) and is well-formed:
- Correctly states `ensemble-empty` slug **does not exist** in `contract.py` today.
- Lists the 7 current BLOCKED slugs — **all 7 verified against research 02's authoritative set** (`timeout`, `child-crash`, `contract-missing`, `contract-version-missing`, `unknown-major-version`, `malformed-degraded-components`, `malformed-contract-boolean`). No invented slug.
- Surfaces the collision with FR-RH2.7 ("verdict map unchanged").
- Offers Option A (deliberate recorded `derive_verdict` change) vs Option B (route onto existing BLOCKED trigger), notes verdict/exit-code is identical either way, and records it as an Open Question for §22 (not silently resolved). The §22 deferral is echoed in the closing "Cross-References & Open Items."

This is exactly the surfacing-not-smoothing behavior the gate requires. PASS.

---

## 9-Criteria Synthesis Quality Review

| # | Check | synth-04 | synth-05 | synth-06 |
|---|-------|----------|----------|----------|
| 1 | Section headers match template | PASS (§7/§8) | PASS (§9/§10/§11) | PASS (§12/§13) |
| 2 | Table column structure correct | PASS | PASS | PASS |
| 3 | No fabrication beyond research | PASS | PASS | PASS |
| 4 | Findings cite file paths/evidence | PASS | PASS | PASS |
| 5 | Options analysis ≥2 options w/ tradeoffs | PASS (§8.4/cross-refs) | N/A (flows doc) | PASS (D3 Opt A/B) |
| 6 | Impl plan has specific steps+paths | PASS | PASS (11-step flow) | PASS |
| 7 | Cross-references consistent | PASS | PASS | PASS |
| 8 | No doc-only claims in §2/§8 | PASS | PASS | PASS |
| 9 | Stale-doc discrepancies surfaced | PASS | PASS | PASS (D3, D6) |
| 10 | Key-finding coverage | PASS | PASS | PASS |

**Header verification (Check 1):** template §7 Data Models, §8 API Specifications, §9 State Management, §10 Component Inventory, §11 User Flows & Interactions, §12 Error Handling & Edge Cases, §13 Security Considerations — all match the synth file headers exactly.

**Table structure (Check 2):** §8.3 OI-1 table (Reflect field / Type / Swarm source / Mapping / Notes), the (M,N) tables (M-condition / verdict / exit-code / reason-slug / [test-case]), the Threat Model (Threat / Likelihood / Impact / Mitigation), and the WorkerResult/ResultContract/LensEntry data tables all use coherent, consistent column structures.

**No fabrication + evidence (Checks 3-4):** Live-source spot-checks confirm:
- `LensEntry` @ `models.py:637` with **exactly 14 fields** and the `stability` `__post_init__` enum guard — matches synth-04's claim of a direct re-read this turn.
- `workers_succeeded = sum(... if w.status == "success")` @ `reduce.py:648` (the M predicate) — cited identically across synth-04/05/06.
- `merge_method == "single-reviewer-fallback"` trigger @ `contract.py:280` — matches synth-04/05/06 and research 02 trigger 10.
- D3's 7-slug list matches research 02 verbatim (no invented slug).

**Stale-doc / discrepancy surfacing (Check 9):** synth-06 carries TWO reconciliation notes (D3 ensemble-empty slug gap; D6 INV-005 arithmetic gap in `reduce_wave3`) and an `[UNVERIFIED]` carry-forward block (ensemble.py does not exist; path-confinement is design-not-enforcement). These correctly propagate research 05's `[CODE-CONTRADICTED]` gaps 1-2 and gap 4. synth-04 §8.4 also surfaces the "neither contract is wired today" grep evidence. Nothing smoothed over.

**Key-finding coverage (Check 10):** the load-bearing research takeaways are all reflected:
- research 02 ordering `blocked→degraded→halted→pass` first-match-wins → synth-04 §8.3 notes, synth-05 step 10, synth-06 §12.2.3 + §13.1.
- research 02 M==0→BLOCKED structural ordering → synth-04 §8.4 M==0 interaction, synth-06 verdict-ordering row.
- research 05 "two disjoint schemas, one filename" → synth-04 §8.3 + §8.4 Contract B, synth-06 §12.2.3 path-confinement row.
- research 05 `final_path` not `merged.md` → synth-04 §8.4 Contract A, synth-05 step 8, synth-06 §13.1.

---

## Contradictions Found

**None.** No cross-file contradiction between synth-04/05/06, and none against research 00/02/05 or the live source. The M, N convention; the M predicate (`status=="success"`); the (M,N) verdict table; the OI-1 disjoint-schema claim; and the path-confinement contracts are stated consistently across all three files and match their research sources.

---

## Minor Observations (non-blocking, no fix required this gate)

**OBS-1 — `degraded-tier1` slug not surfaced in synth-05/06 (coverage nuance, not an error).**
research 02 trigger 6 emits the slug `degraded-tier1` when `expected_tier >= 2 AND tier_reached == 1`. synth-05 §11.2 and synth-06 §12.3 describe the M==1 branch using `merge_method: single-reviewer-fallback` **and/or** `tier_reached: 1`, attributing the exit-11 to the `single-reviewer-fallback` slug (trigger 10) — which is correct and grounded. They reference `tier_reached:1` as a *contract value `ensemble.py` would emit*, NOT as a reason-slug, so there is no false claim. However, neither file names the distinct `degraded-tier1` slug that trigger 6 would independently produce from that same `tier_reached==1` value. This is a completeness nuance the TDD author may want in §12, not a contradiction. Severity: Minor. Files are internally consistent and consistent with the spec's (M,N) table (which itself uses `single-reviewer-fallback` for M==1).

**OBS-2 — research 05 §7 self-references research 02 as "stub header only."**
research 05 §7 (written 2026-06-19) states `02-reflect-contract-verdict.md` "is a stub header only (Status: In Progress)" and defers the reflect-side join to synth-04. research 02 is now Complete (2026-06-20) and synth-04 correctly sources its left column from the completed research 02. This is a stale intra-research timestamp artifact, NOT a synthesis defect — synth-04 used the authoritative completed file. No action on the synthesis files. Severity: Informational (flagging only so the assembler does not treat research 05 §7's "stub" remark as current).

---

## Recommendations

1. **PASS the synthesis gate for synth-04/05/06.** All 9 criteria and all 4 special-attention probes pass; no blocking issues.
2. (Optional, TDD-author discretion) Consider adding the `degraded-tier1` slug (research 02 trigger 6) alongside `single-reviewer-fallback` in the TDD §12 (M,N)/error narrative for slug completeness (OBS-1). Not required for gate passage.
3. No fix needed for OBS-2; it is an intra-research timestamp artifact already correctly handled by synth-04.

---

## Methodology

All findings are file-grounded. Authoritative reflect field set taken from `research/02` (consumer half), swarm producer from `research/05` (DM-012), the (M,N) table from `research/00 §5` (verbatim spec), template conditional language from `src/superclaude/examples/tdd_template.md` L580/L624. Three live-source spot-checks (`models.py:637`, `reduce.py:648`, `contract.py:280`) confirmed no fabricated citations. No web research performed or required (none authorized; all checks are file-local).

*Status: Complete*
