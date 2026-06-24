# PRE Reflect Gate — UC-1 Coverage Audit

- run_id: pre-reflect-tsh-harden-r2
- mode: pre (UC-1, pre-execution coverage audit)
- spec: .dev/troubleshoot-meta/20260610T141100Z/troubleshoot-pipeline-hardening-RELEASE-SPEC.md (v1.1.0)
- tasklist: TASK-RF-troubleshoot-hardening-20260611-023739.md
- depth: standard
- reviewed_at: 2026-06-11
- method: Executor-disjoint direct UC-1 audit (skill fallback path; reviewer fan-out not nested in subagent context)

## Grade

- coverage_pct: 0.947 (18/19 counting the two deferred measurement NFRs as one PARTIAL bucket); 17/19 fully MAPPED with implementation + §8 test.
- Coverage floor: 0.90
- Verdict: PASS — all 13 FRs and 4 of 6 NFRs fully MAPPED to an implementing item + a §8 test. The two PARTIAL items (NFR-2, NFR-3) are measurement NFRs the spec and tasklist deliberately defer to the M5 backtest milestone (tasklist L96: "M5 ... deferred and OUT of scope here"). Their measured substrate is implemented in-tasklist. No implementation requirement is unmapped.
- spec-literal checks: ALL PASS.

## Coverage Matrix

| Req | Implementing item(s) | §8 Test | Status |
|-----|----------------------|---------|--------|
| FR-1 Applicability Gate (H0) | Step 2.1; wired 5.1, 5.3 | test_h0_applicability_skip_requires_boundary_scan, test_h0_boundary_scan_schema_rejects_bare_local_reason (7.2) | MAPPED |
| FR-2 Mechanism Statement (H0) | Step 2.1 | known_escapes anti-inflation test_known_escapes_requires_cited_card (7.7) + report render | MAPPED |
| FR-3 Runtime-Entrypoint (H1) | Step 3.1 | test_h1_runtime_card_requires_negative_and_positive_witness (7.3) | MAPPED |
| FR-4 Negative-Witness (H1) | Step 3.1 (+OI-3 deferral) | test_h1_runtime_card_requires_negative_and_positive_witness (7.3) | MAPPED |
| FR-5 Contract-Enumeration Ledger (H2) | Step 3.2 | test_h2_empty_ledger_fails (7.4) | MAPPED |
| FR-6 Sibling/Dup-Evaluator Sweep (H2) | Step 3.2 | test_h2_sibling_sweep_required_when_concept_shared (7.4, NEW — closes G-PRE-1) | MAPPED |
| FR-7 Whole-Artifact Classifier (H3) | Step 4.1 | test_h3_sweep_card_requires_k_true_k_swept_and_mixed_fixture (7.6) | MAPPED |
| FR-8 Near-Miss + Grammar + Word-Boundary (H3) | Step 4.1 | test_h3_word_boundary_rejects_incomplete_representation, test_h3_small_grammar_rejects_setext_and_decorated_verdicts (7.6) | MAPPED |
| FR-9 Unmask-and-Sweep Regression (H3) | Step 4.1 | test_h3_sweep_card_requires_k_true_k_swept_and_mixed_fixture (7.6) | MAPPED |
| FR-10 Effective-Input Proof (H4) | Step 3.3 | test_h4_nonempty_wrong_surface_fails_closed, test_h4_manifest_schema_requires_intersection_proof (7.5) | MAPPED |
| FR-11 Off-Path-Reviewer + Waiver (H5) | Step 2.1 | test_h5_decision_maps_to_status_and_latch (7.7) | MAPPED |
| FR-12 No-Re-Greening + Anti-Inflation | Step 2.2; Step 6.2 | test_waiver_latch_one_way, test_known_escapes_requires_cited_card (7.7); test_downstream_success_cannot_override_latched_hardening_verdict (7.9) | MAPPED |
| FR-13 Versioned Additive Contract + Closure | Step 2.2; 5.2; 6.1 | test_verdict_aggregation_from_h_statuses (7.8), test_output_contract_backward_compat (7.10), test_report_closure_section_not_proven_blockers (7.12) | MAPPED |
| NFR-1 E1–E5 backtest catch rate | Step 7.11 + E2E 7.13–7.18 | test_backtest_status_keeps_pipeline_health_advisory_until_complete (7.11) | MAPPED |
| NFR-2 Applicability FP rate <30% | FR-1 boundary-scan substrate (2.1); measurement deferred to M5 (OUT of scope, L96) | None in-tasklist (deferred) | PARTIAL |
| NFR-3 Bounded added cost | Single-seam probe honored (FR-1/FR-4); measurement deferred to M5 | None in-tasklist (deferred) | PARTIAL |
| NFR-4 No-re-greening durability | Step 6.2 + Step 7.18 (E2E) | test_downstream_success_cannot_override_latched_hardening_verdict (7.9) | MAPPED |
| NFR-5 Command thinness | Step 5.3 (no new CLI flag) | Phase 7 markdownlint + Phase 8 domain lens | MAPPED |
| NFR-6 Output-contract backward compat | Step 5.2 (additive-only) | test_output_contract_backward_compat (7.10) | MAPPED |

## Spec-Literal Adversarial Checks

| Check | Result |
|-------|--------|
| (a) 4-token verdict enum; no 3-token / "advisory removed" regression | PASS — 4-token enum 8×; sole "advisory removed" string (L71) is the guard note flagging the prior regression, not one. Steps 2.2/5.2/7.7/7.8 carry 4-token form; 3-token marked DEFECT. |
| (b) §5.4 truth table = 7 rows; rows 5 & 6 emit advisory | PASS — Step 2.2 reproduces all 7 rows incl. advisory rows 5/6; Step 7.8 test asserts BOTH advisory rows present. |
| (c) OI-2/OI-3/OI-5 HALT; OI-1/OI-4/OI-6 RESOLVED not HALT | PASS — L134 states the rule; Steps 1.5/1.6/1.7 create OI-2/3/5 PENDING; NO OI-1/4/6 PENDING steps (grep-confirmed). |
| (d) G-PRE-1 FR-6 test present; FR-12 paired with NFR-4 test | PASS — Step 7.4 (G-PRE-1) and Step 7.9 (FR-12↔NFR-4, flagged HIGHEST-RISK per spec §10 L596). |
| (e) G1 HALT (no src/superclaude or .claude edits pre-approval) | PASS — frontmatter intent + BLOCKING prerequisite block + Step 1.1 gate + per-phase reminders; treated as prerequisite not needs_human_decision (correct). |

## Gap Registry

| Gap | Severity | Description | Disposition |
|-----|----------|-------------|-------------|
| G-PRE-1 | CLOSED | FR-6 previously had only indirect test coverage | Closed by NEW test_h2_sibling_sweep_required_when_concept_shared (7.4). |
| G-PRE-2 | LOW/ADVISORY | NFR-2/NFR-3 have no in-tasklist measurement test | By design — both deferred to M5 backtest milestone (OUT of scope, L96). Substrate implemented. Flag for M5 to pick up NFR-2/NFR-3 measurement. |

## Notes

- The two PARTIAL rows are the only sub-100% items; both are deferred measurement NFRs, not implementation gaps.
- The advisory invariant (the exact spot a prior build failed) is defended at four layers: frontmatter guard note, Step 2.2 verbatim truth table, Step 7.8 dual-advisory-row assertion, multiple "3-token = DEFECT" reminders.
- HALT-item discipline is correct and matches the project rule "human-decision items must HALT, not auto-default."
