# Evidence validation (Wave 5)

Validator: evidence-validator agent (sonnet slot), 2026-11-06T22:20:40Z, persisted by the orchestrator on receipt.
Scope: adversarial/merged-verdict.yaml (M-1..M-11, advisory, rejected) and reflection-card.yaml (RF-1..RF-3, risks line).

- Citations checked: 73
- Founded: 72
- Dropped: 1
- [INFERRED]: 0

## Dropped

| Finding | Citation | Reason |
|---------|----------|--------|
| M-1 | tests/skills/test_worker_contract.py:102-108 | Lines hold `RULE_PHRASES["WC-4"]`; M-1 concerns init-lite status wording (pins at :777-797). Stray citation; the same range is correct in M-5. Removed from M-1 in REPORT.md. |

## Notes applied in REPORT.md

- M-3: "report_path is the plan `<id>.md`" is at sc-workflow-protocol/refs/return-contract.md:51 (cited :52); corrected to :51.
- M-11: init_lite.py:247-262 are report-write refusals (protected context path, existing file without the generated marker), not an audit failure; wording changed to "report-write refusal". Conclusion unchanged (ClickException, non-zero exit).
- M-6: the index-repo half rests on inference (nothing cited shows `PROJECT_INDEX.json` ignored); tagged [INFERRED] in REPORT.md. The init-lite half is grounded (init_lite.py:294-298, :338).
- RF-2: plugin test.md claim true; checked separately.

Zero-drop flag: not applicable (1 drop). Status forced to partial (SKILL.md section 11.2).
