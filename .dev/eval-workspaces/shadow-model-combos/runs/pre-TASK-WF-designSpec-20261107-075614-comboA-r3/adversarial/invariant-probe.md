# Invariant Probe Results (Round 2.5)
| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|-----------|--------|----------|----------|
| INV-001 | guard_conditions | Merged O-2 downgrade assumes no plan task CAN own a post-merge PR obligation | ADDRESSED | LOW | spec:326 assigns it to the owner's release gate; Task 1 records it |
| INV-002 | state_variables | Merged verdict assumes plan authored against 43-member base (45 ACs correct at authoring) | ADDRESSED | LOW | plan Task 2 asserts 43->45 as its own change; verified at authoring base e8db2fe6 per spec F1 |
| INV-003 | sufficiency_challenge | "Blocking" downgrades must not hide a real wrong-outcome risk | ADDRESSED | MEDIUM | X-1 narrowed claim retained as MAJOR; X-2 recorded as advisory with owner-decision citation |
Summary: 3 findings, 3 ADDRESSED, 0 UNADDRESSED. No HIGH items; convergence gate passes.
