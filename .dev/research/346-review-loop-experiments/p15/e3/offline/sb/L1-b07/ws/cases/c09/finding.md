### B3. AC-0.4 cannot pass in P0 as written

- Spec text: AC-0.4 (line 194) says "steps 1-3 and 5-7 pass; step 4 uses the command's existing report file, since the contract arrives in P1". Step 3 (line 182) requires "its report path is the WC-4 contract path". Step 4 (line 183) asserts `d['status']` in a YAML contract and `d['command']`.
- Failure on `/sc:troubleshoot`: the no-`--fix` run writes `REPORT.md` as its `report_path`, and writes `return-contract.yaml` only with `--caller task-unified` (`INV-B:49`, `INV-B:242`). `REPORT.md` is not a YAML contract, so step 4 fails. Step 3 also fails, because the WC-4 contract path does not exist until P1.
- Failure on `/sc:workflow`: its contract has `status`, `plan_path` and `reflect_report_path` (`INV-B:272`) and no `command` key, so the `d['command']` assertion fails in P0.
- Grading sentence: an implementer who runs the P0 smoke test as written gets a failed step 3 and step 4 on two of the three named commands, and the spec says a failure "reopens section 1" (line 194), so P0 cannot pass.
- Severity: blocking, because P0 is the gate for the whole decision.
