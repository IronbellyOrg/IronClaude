# Calibration Report

Card: t1-card.md. Rubric: /home/coder/.claude/skills/sc-reflect-protocol/refs/reflection-rubric.md, five reflect dimensions. Tier1, mode pre, standard. Timestamp supplied: 2026-11-23T18:16:05Z. Requested opus. Reviewer gateway class unknown: calibrator diversity degraded/unproven, not full.

## Scores
| Dimension | Score | Justification |
|---|---:|---|
| Citation grounding | 0.90 | All spot-checked source and plan lines match. Analyst receipt, raw quotes and wizard-guide note not checked. |
| Coverage completeness | 0.55 | Machine coverage_pct_union=0.5 and parsed-sparse confirmed. Manual source-to-plan map is explicit but cannot replace arithmetic. |
| Deviation-classification clarity | 0.45 | Aggregate no drift/regression only; per-item categories missing for the two analyst Medium notes and proposed changes. |
| Risk surface coverage | 0.90 | Shared builder, sibling mapping, resume, caller precedence, identical-template provenance and path parsing all named. No current test-run success claimed. |
| Recommendation actionability | 0.70 | Next step is Tier2 scrutiny; no explicit success test for advisory follow-ups. |

Mean: (0.90+0.55+0.45+0.90+0.70)/5=0.70. No caps or troubleshoot rules applied. No self-confidence supplied, so delta N/A.

## Routing
ESCALATE to Tier2. Parsed-sparse prefilter sufficient on its own. Also C<0.85, three domains, density0.5>0.20. Four tasks. The rubric ref alone did not contain the full routing table; orchestrator must apply the loaded skill table. No execution restriction was stated in calibration inputs; the card itself remains plan-only and supplies no runtime success claim.

## Spot checks
All Read by independent calibrator: refactor_find.py:53; commands.py:2129-2157; adversarial.md:15,39; README.md:67; lens-catalog.md:25,49; user-guide.md:200; test_commands_run.py:507-542; plan lines19,25,37-39,60,67,69,71; coverage-matrix.json. All match. Relative ../../ plan reference resolves from the card's own directory, though calibrator noted wording ambiguity if interpreted relative to artifacts alone. No remote citations.

Not checked: coverage-analysis.md, requirements.json, source.md, wizard-guide.md:216. No structural pathology identified. Complete score and recommendation returned by plan-t1-calibration; parent persisted before consumption.
