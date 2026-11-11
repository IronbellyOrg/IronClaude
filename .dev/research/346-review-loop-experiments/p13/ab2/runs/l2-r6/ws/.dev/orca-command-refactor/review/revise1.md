# Revise 1 (blocking ids: F1)

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Report: `review/round1.md` (Reviser brief at round1.md:185-192). Evidence checked: `inventory/commands-a.md:35,60`, `inventory/commands-b.md:272-273`, `inventory/orca-capabilities.md:72-74`. Not run: spec-panel; no verdict is given.

## Byte accounting
- Before: 57763 bytes (sha256 d3cdbe57...5200d, as in round1.md header). After: 58378 bytes. Net +615.
- Per finding id: F1 added 713 bytes, deleted 98 bytes (net +615). No other id touched; M1-M10 and N1-N5 left alone.
- Per line (spec line: added/deleted): 62: 386/23; 76: 37/0; 92: 145/31; 182: 33/5; 196: 44/11; 198: 68/28.

## Findings
| id | disposition | where |
|---|---|---|
| F1 | applied | WC-4 (spec:62): one rule, "path section 3 names, else `<output-dir>/return-contract.yaml`"; path derived from the brief, or from `--report-path` where it holds a command-created id (workflow, INV-B:272-273); a stop before the contract's directory exists writes no contract and reports in the `worker_done` body with no `--report-path` (allowed by `inventory/orca-capabilities.md:73`, which forbids only placeholder values; matches INV-B:272 "Not written for pre-creation STOPs"). Section 3 "Contract" definition (spec:76) aligned to the same rule. Adversarial row (spec:83) left unchanged: its `<output>/adversarial/return-contract.yaml` is now the row-named path, consistent with real runs (INV-A:35,60). Workflow row (spec:92): "write for pre-creation STOPs" replaced by the no-contract outcome. Live check step 3 (spec:182) and AC-1.2 (spec:196) now refer to the per-command path and the section 3 brief flags (workflow takes no `--output`). AC-1.4 (spec:198) states the adversarial path and the workflow no-contract outcome. |

## Notes
- Every addition cites F1.
- Residual: spec:~65 section 2.3 still says the output directory makes the report path "known before dispatch"; not named by F1, left alone (UNVERIFIED whether re-review treats it as inherited text).
- Process slip: I briefly wrote a before-copy outside the workspace (in the scratchpad parent) to count bytes; it was removed, and no other out-of-sandbox write happened.
