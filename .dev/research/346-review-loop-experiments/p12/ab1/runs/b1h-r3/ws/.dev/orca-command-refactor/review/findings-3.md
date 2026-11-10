### R2-1
| R2-1 | blocking | **open** (partial repair) | Workflow and troubleshoot are repaired. The step-3 rule for adversarial (`spec:189`, `spec:201`) takes its file from "its existing contract file", which the spec never names. The adversarial row says "filename not fixed" (`spec:83`), and the inventory records two layouts (`INV-A:35`). The same root cause as M6 below. |
(text of this finding in the prior report)
### R2-1 (BLOCKING, origin=changed)
- Quoted: AC-0.4 (`orca-worker-contract-spec.md:201`): "steps 1-3 and 5-7 pass; step 3's report path is the one the command writes today". Step 3 (`:189`), which AC-0.4 depends on: "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- Sentence: An implementer who runs AC-0.4 on `/sc:troubleshoot "<real symptom>"` as written must make step 3's outcome match hold. Troubleshoot's P0 report is `REPORT.md` (`:91`; `commands-b.md:49`), and the contract does not exist before P1 (`:201`), so there is no `status` to match. Step 3 cannot pass, and P0 cannot pass.
- Origin: the step 3 text is unchanged from `spec-v1.md`, so the defect is older. It is counted as changed because it quotes the changed AC-0.4 line (`:201`) that depends on it.
- Suggested repair: for commands with no contract in P0, state where the outcome comes from (for example, the command's own report), or remove the outcome match from step 3 for P0.

### M6
### M6 (regressed, BLOCKING; origin=unchanged step 4, depends on changed `spec:201` step 3)
- Quoted: `spec:201`, adversarial step 4: "`adversarial`: `test -s` on its existing contract file (the inventory names no field list, `INV-A:35`)". Step 3 at `spec:189` and `spec:201` uses the same file: "its report path is that file".
- Sentence: An implementer who runs AC-0.4 on `/sc:adversarial --compare <two files> --depth quick --output <dir>` as written must run `test -s` on "its existing contract file". The spec names no path (`spec:83`: "filename not fixed"). The inventory records two layouts (`INV-A:35`). The check tests either the wrong file or no file, so step 4 and the step-3 rule built on it cannot pass as written.
- Note: `spec:83` gives the adversarial row's P1 fix as `<output>/return-contract.yaml`. That is P1, and P0 runs before it (`spec:158`).
- Suggested repair for the user to choose (not a brief, since the review is at 3): (a) name the P0 adversarial path explicitly, for example `<dir>/adversarial/return-contract.yaml` after checking that the output is deterministic; or (b) remove adversarial from P0, which needs only two commands, and test it first in P1, when `spec:83` fixes the path.
