### F-01 (MAJOR, BLOCKING): AC-0.4 step 3 cannot pass in Phase 0

- Location: spec line 194 (AC-0.4) against line 182 (7.2 step 3) and line 158 (P0, "no command edits"). Inventory: `commands-b.md:272` (workflow contract is `.dev/tasks/to-do/<id>/return-contract.yaml`), `commands-a.md:55` (init-lite writes no contract).
- Issue: AC-0.4 requires steps 1-3 to pass, and step 3 requires "its report path is the WC-4 contract path". AC-0.4 also says the WC-4 contract "arrives in P1". Phase 0 therefore has no WC-4 path for step 3 to match.
- Grading check: "An implementer who runs AC-0.4 as written in P0 finds step 3 cannot pass for any of the three commands, and that is wrong because P0 is the gate that decides whether section 1 stands (line 194, "a failure here reopens section 1")." This holds with no added assumption: the two stated texts contradict each other.
- Recommendation: in AC-0.4, make step 3 check the report path against the command's existing report file (`REPORT.md` for troubleshoot, the workflow `return-contract.yaml`, `<output>/adversarial/return-contract.yaml` as actually written), and state the WC-4 path check starts in P1.
- Expert: Adzic (acceptance criteria that cannot pass), Wiegers (traceability of the gate to its phase).
