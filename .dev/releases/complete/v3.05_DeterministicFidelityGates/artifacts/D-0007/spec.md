# D-0007: Data Model Extensions

**Task**: T01.05
**Implements**: FR-3, FR-6 (partial)

## Finding Extensions (models.py)
New fields (all with string defaults for backward compatibility):
- `rule_id: str = ""` — machine key from SEVERITY_RULES
- `spec_quote: str = ""` — verbatim quote from spec
- `roadmap_quote: str = ""` — verbatim quote from roadmap
- `stable_id: str = ""` — deterministic finding identity

## SEVERITY_RULES (structural_checkers.py)
19 canonical rules: `dict[tuple[str, str], str]`
- signatures: 4 rules (2 HIGH, 2 MEDIUM)
- data_models: 4 rules (2 HIGH, 2 MEDIUM)
- gates: 4 rules (1 HIGH, 3 MEDIUM)
- cli: 2 rules (2 MEDIUM)
- nfrs: 5 rules (3 HIGH, 2 MEDIUM)

`get_severity(dimension, mismatch_type) -> str` raises KeyError on unknown combos.

## New Types
- `RegressionResult` — regression check result (structural_checkers.py)
- `RemediationPatch` — single remediation edit tracking (structural_checkers.py)
- `ParseWarning` — parser degradation warning (spec_parser.py)
- `RunMetadata` — already defined in convergence.py
