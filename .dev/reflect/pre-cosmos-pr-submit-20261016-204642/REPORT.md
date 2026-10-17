# Cosmos workflow preflight

Mode: pre-execution. Status: partial (advisory).

The independent requirements analyst mapped R1–R4 and A1–A16 to the four workflow tasks. The plan includes review attribution, complete poll snapshots, resolution-aware root selection, explicit normalization, protocol wiring, regression tests, and synchronization. Source task T5 is consolidated into plan Task4 and the executor-owned final verification; it is not a missing delivery task.

## Advisory findings

- Source section7 requires a fresh independent final reviewer and findings closure. Task4's wording that the executor performs its independent review is ambiguous in isolation. Execution must use the canonical managed-package protocol: a fresh separate reviewer reads actual delivery files, and archive requires a clean result. The workflow plan is not edited from this advisory finding.
- Source section7 requires reporting actual outcomes and limitations. This remains incorporated through the plan's global source constraint and must appear in the final execution handoff.

This is a bounded document-coverage preflight, not an implementation verdict or a claim that the full reflection ensemble/merge machinery completed. No product code or tasklist content was changed by this review. Reviewer coverage and evidence validation are recorded separately when returned. Missing advanced Serena configuration/activation surfaces in the available tool set prevent claiming the full protocol grounding chain; the workflow may proceed with this advisory partial result.

## Coverage owners

| Scope | Task |
|---|---|
| R1, A1–A9, A14 | T1 |
| R2, A4–A5, A10–A12, A14 | T1/T2 |
| R3, A13/A16 | T3 |
| R4, A15, protocol and final evidence | T1/T4 |

The source and plan remain immutable inputs to the forthcoming implementation ledger.
