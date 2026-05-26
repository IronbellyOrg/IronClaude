# Merge Log

## Metadata

- Base variant: Variant 1 (opus, default persona)
- Executor: merge-executor
- Date: 2026-05-22
- Changes planned: 16
- Changes applied: 16
- Changes failed: 0
- Changes skipped: 0
- Overall status: success

## Changes Applied

| ID | Title | Status | Target Section | Provenance Tag | Validation |
|----|-------|--------|----------------|----------------|------------|
| CH-001 | Add R-009 conversion-rate risk | Applied | §6 Risk Register (append after R-008) | Source: Variant 2 (sonnet, default), §6.R-006 — merged per CH-001 | OK — new R-009 row inserted; no contradictions with R-001..R-008 |
| CH-002 | Sub-component performance budgets (§8.5) | Applied | §8 Quality Gates (new §8.5) | Source: Variant 2 (sonnet, default), §8.3 micro-benchmark gates — merged per CH-002 (V1 measurement rigor per R2 §2 walk-back) | OK — additive subsection; cross-reference to §8.4 bcrypt gate resolves |
| CH-003 | Lockout state durability on Redis flush | Applied | §2.M1 exit criteria (new criterion 9) + §6 R-002 mitigation (expanded) | Source: Invariant Probe (Round 2.5), INV-001 + INV-017 — merged per CH-003 | OK — M1 exit 9 added; R-002 mitigation expanded with fail-closed semantics |
| CH-004 | Audit-log durability M3 exit + §8.6 gate | Applied | §2.M3 exit criteria (new criterion 9) + §8 (new §8.6) | Source: Invariant Probe (Round 2.5), INV-002 — merged per CH-004 | OK — both M3 exit 9 and §8.6 added; consistent semantics |
| CH-005 | Refresh-token malformed-input guard | Applied | §2.M2 exit criteria (new criterion 11) | Source: Invariant Probe (Round 2.5), INV-004 — merged per CH-005 | OK — additive; mock-zero-hgets assertion explicit |
| CH-006 | Per-account DoS R-010 | Applied | §6 Risk Register (append after R-009) | Source: Invariant Probe (Round 2.5), INV-019 — merged per CH-006 | OK — new R-010 row; CAPTCHA-on-4th-attempt explicit |
| CH-007 | Legacy auth rollback operational viability | Applied | §7 Rollout & Release Gates (new Gate A pre-flight row) | Source: Invariant Probe (Round 2.5), INV-020 — merged per CH-007 | OK — Gate A pre-flight inserted before Gate A: Alpha Entry; references appear in legacy-auth ownership chain |
| CH-008 | Feature-flag flip half-state runbook step | Applied | §7 Rollback Procedure (new step 2.5) | Source: Invariant Probe (Round 2.5), INV-016 — merged per CH-008 | OK — step 2.5 inserted; subsequent steps re-numbered 4-7 (was 3-6); drain-window semantics explicit |
| CH-009 | Refresh-token cap decision (PRD-OQ-2) | Applied | §9 Open Questions — PRD-OQ-2 row restructured | Source: Variant 2 (sonnet, default), §9 PRD-OQ-2 cap=5 + Base eviction policy — merged per CH-009 | OK — recommendation → decision; eviction-vs-block disambiguated per INV-010; M2 integration test referenced |
| CH-010 | Roles cap decision (TDD-OQ-002) | Applied | §9 Open Questions — TDD-OQ-002 row restructured | Source: Variant 2 (sonnet, default), §9 OQ-002 cap=10 + Base explicit-rejection semantics — merged per CH-010 | OK — recommendation → decision; lower-bound (empty) + upper-bound (11th) both defined per INV-005/INV-011 |
| CH-011 | Lockout 5-fail off-by-one + window semantics | Applied | §2.M1 exit criterion 6 (rewritten) + Appendix A lockout row (rewritten) | Source: Invariant Probe (Round 2.5), INV-007 + INV-008 — merged per CH-011 | OK — fixed-window + 5th-attempt-as-trigger semantics pinned; time-travel test specified |
| CH-012 | 30-minute lockout cooldown | Applied | §2.M1 exit criterion 6 (cooldown sub-clause) + §9 PRD-OQ-3 row | Source: Variant 2 (sonnet, default), §9 PRD-OQ-3 + Base R2 §2 concession — merged per CH-012 | OK — 15-min → 30-min replaced; PRD-OQ-3 elevated to decision |
| CH-013 | M5 separate NFR-REL-001 vs NFR-PERF-001 exit gates | Applied | §2.M5 exit criteria (rows 3-4 restructured) | Source: Variant 2 (sonnet, default), R2 §3.1 evidence — merged per CH-013 | OK — bundled gate split; "neither metric can mask the other" note added |
| CH-014 | Appendix B Gantt visualization | Applied | Appendix B split into B.1 (matrix) + B.2 (Gantt) | Source: Variant 2 (sonnet, default), §Appendix B — merged per CH-014 | OK — B.1 (matrix) preserved unchanged; B.2 (Gantt) appended; WS-4 week-6 gap explicitly filled by SEC-4 |
| CH-015 | Beta-duration debate as rejected alternative | Applied | §7 Rollout & Release Gates (Phase 2 Beta sidebar) | Source: V1 R2 §3.1 + V2 R2 §4.2 concession — merged per CH-015 | OK — sidebar note inserted between phase gates table and feature flag plan; preserves debate evidence |
| CH-016 | M0 effort reduction with deliverable accountability | Applied | §1 capacity total (48 EW → 46 EW) + §2.M0 effort (8 EW → 6 EW) + §2 milestone roll-up | Source: V1 R2 §4.2 + V2 R2 §2 — merged per CH-016 | OK — three locations updated consistently (§1, §2.M0, milestone roll-up); PG/Redis deliverables annotated as platform-team-standard-work-0-EW |

## Post-Merge Validation

### Structural Integrity

- Status: Pass
- Heading hierarchy: All sections 1-10 plus Appendix A and Appendix B (B.1, B.2) preserved
- New subsections (§8.5, §8.6, Appendix B.2) introduced at appropriate depth (### under their parent ## section)
- No heading-level gaps; no orphan subsections
- Rollback procedure renumbering (step 2 → 2.5 → 4-7) maintains sequential flow
- Tables: column counts consistent across additions (R-009, R-010 match R-001..R-008 schema)

### Internal References

- Total references checked: 27
- Resolved: 27
- Broken: 0

Cross-reference verification:
- M0-M5 milestone references: all 6 milestones present and consistently referenced
- FR-AUTH-001 through FR-AUTH-005: all present in §4 traceability and milestone scopes
- NFR-PERF-001, NFR-PERF-002, NFR-REL-001, NFR-SEC-001, NFR-SEC-002: all preserved
- R-001 through R-010: all 10 risks present; new R-009 (CH-001) and R-010 (CH-006) integrate cleanly
- WS-1 through WS-5: 5-workstream taxonomy retained (per REJECT-B)
- H1 through H10: handoff matrix retained intact (per REJECT-E)
- AT-001 through AT-016: acceptance-test IDs preserved
- CH-NNN references in provenance comments: 16 changes referenced, all unique
- INV-NNN references in provenance comments: INV-001, INV-002, INV-004, INV-005, INV-007, INV-008, INV-010, INV-011, INV-016, INV-017, INV-019, INV-020 — all resolve to invariant-probe.md entries
- Appendix A new rows reference CH-003, CH-004, CH-005, CH-011, CH-012 — all map to applied changes
- §9 OQ decisions reference INV-005, INV-010, INV-011 — all map to invariant-probe entries

### Contradictions Re-Scanned

- New contradictions introduced: 0
- Notes:
  - Effort total: §1 (46 EW), §2.M0 row (6 EW), and milestone roll-up (M0=6 + M1=10 + M2=9 + M3=7 + M4=7 + M5=7 = 46) are all consistent post-CH-016
  - Lockout: §2.M1 exit 6 (CH-011/CH-012), §6 R-002 (CH-003), §9 PRD-OQ-3 (CH-012), and Appendix A lockout row all consistently describe 5-fail/15-min-fixed-window/5th-attempt-is-trigger/30-min-cooldown/Redis-fail-closed semantics
  - M5 exit: §2.M5 separates NFR-REL-001 and NFR-PERF-001 per CH-013; downstream §10 metrics tables remain consistent (uptime measured T+30d, latency T+7d)
  - Refresh-token cap: §9 PRD-OQ-2 (cap=5, oldest-evicted) is consistent with §2.M2 deliverable 2 (no explicit cap stated, leaves room for cap implementation per OQ decision); no contradiction
  - Roles cap: §9 TDD-OQ-002 (cap=10) consistent with §2.M0 deliverable 1 (UserProfile schema includes roles default `["user"]`); no contradiction
  - Rollback procedure: step 2.5 (CH-008) integrates without disrupting steps 1-2 above or steps 4-7 below; cookie-format drain window is internally consistent with §7 Gate A pre-flight (CH-007) legacy-cookie compatibility check

## Summary

- Planned: 16
- Applied: 16
- Failed: 0
- Skipped: 0
- Overall status: success
