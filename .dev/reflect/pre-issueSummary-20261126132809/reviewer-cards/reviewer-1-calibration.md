# Calibration of reviewer 1 card (saved by the orchestrator from the calibrator's returned text)

Calibrator class: sonnet alias (disjoint from the reviewer classes haiku and opus; the same class as the executor, so executor/calibrator separation is degraded).

Citations that do not match: 0. Every file:line cite in the card resolves and matches.

| Dimension | Score | Reason |
|---|---|---|
| Citation grounding | 0.80 | All cites resolve. The SPEC:35 paraphrase is stretched (the spec sentence is conditional). The "20 units / 17 adherent / units 1, 14, 15" numbering appears nowhere in the card, spec or plan. |
| Coverage completeness | 0.68 | Counts only (20, 17, 3), no unit list or gap registry. |
| Deviation-classification clarity | 0.55 | One category per finding, but finding 1 is "Regression" and findings 2 and 3 "Drift", all labelled Blocking (Missing), with no explanation. Two MEDIUM findings are counted as blocking. |
| Risk surface coverage | 0.60 | Main fail-open risk named (tests pass while the model mishandles the notes). No risk register, run cost or one-run-per-cell non-determinism. |
| Recommendation actionability | 0.40 | No recommendations section. |

C = (0.80 + 0.68 + 0.55 + 0.60 + 0.40) / 5 = 0.61

Per-finding evidence support (calibrator): finding 1 mostly supported, severity arguable (SPEC:35 is conditional, and the plan itself states at PLAN:81 that fixtures do not prove model behaviour, with Phase 3 running three scenarios against the real protocol); finding 2 supported; finding 3 supported with the qualification that SPEC:11 addresses the orchestrator, not the plan's tasks, and that a read-only recheck is allowed under the plan's no-writes rule.

Escalation recommendation: ESCALATE (low_confidence, C < 0.85). Per-card score only.
