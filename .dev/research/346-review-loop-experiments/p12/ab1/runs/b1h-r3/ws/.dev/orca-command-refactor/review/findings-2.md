### R2-1
### R2-1 (BLOCKING, origin=changed)
- Quoted: AC-0.4 (`orca-worker-contract-spec.md:201`): "steps 1-3 and 5-7 pass; step 3's report path is the one the command writes today". Step 3 (`:189`), which AC-0.4 depends on: "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."
- Sentence: An implementer who runs AC-0.4 on `/sc:troubleshoot "<real symptom>"` as written must make step 3's outcome match hold. Troubleshoot's P0 report is `REPORT.md` (`:91`; `commands-b.md:49`), and the contract does not exist before P1 (`:201`), so there is no `status` to match. Step 3 cannot pass, and P0 cannot pass.
- Origin: the step 3 text is unchanged from `spec-v1.md`, so the defect is older. It is counted as changed because it quotes the changed AC-0.4 line (`:201`) that depends on it.
- Suggested repair: for commands with no contract in P0, state where the outcome comes from (for example, the command's own report), or remove the outcome match from step 3 for P0.

### R2-2
### R2-2 (BLOCKING, origin=changed)
- Quoted: WC-4 (`orca-worker-contract-spec.md:62`): "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". Against it: the tdd row (`:90`) "`--output <file>`" with report "the TDD at `--output`", and the init-lite row (`:87`) "`--output <file>`". AC-2.2 (`:208`) runs `/sc:tdd "auth" --unattended --output <file>` and checks the contract at `test -s <contract>` (step 4, `:190`).
- Sentence: An implementer who follows WC-4 for `/sc:tdd --unattended --output <file>` must write `<output-dir>/return-contract.yaml`. The flag the brief passes is a file, not a directory, so there is no `<output-dir>` for the coordinator to compute. The contract path is undefined, and AC-2.2 step 4 cannot run for tdd. The same holds for init-lite (`:87`).
- Stated texts that contradict: `:62` (the value is a directory) against `:87` and `:90` (the value is a file).
- Origin: `:62` is changed; `:87` and `:90` are unchanged. The conflict is in `spec-v1.md` at the same rows, so it is an older defect newly found in this review. It is the same class as M10, which named three rows and not these two.
- Suggested repair: give tdd and init-lite a directory flag for the contract, or name the contract location in their rows, as M10 did for the other rows.
