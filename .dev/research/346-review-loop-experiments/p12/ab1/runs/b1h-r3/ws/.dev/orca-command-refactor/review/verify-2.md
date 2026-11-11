# Verification 2: blocking findings R2-1 and R2-2

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
sha256: `e28114855e5685eb7f3f2e2652a756ffaac57ed4c9ffb0b7423b91d78a8e8d19`

Checked with `grep -nF` and `sed -n` against the candidate. `commands-b.md` (cited by R2-1 as `commands-b.md:49`) is not present in the workspace, so that citation is UNVERIFIED. The R2-1 claim about the P0 report path does not depend on it: the candidate's own line `:91` names `REPORT.md` for troubleshoot.

| id | found text | exists | outcome follows | verdict | reason |
|---|---|---|---|---|---|
| R2-1 | `:201` AC-0.4: "steps 1-3 and 5-7 pass, where step 3's report path is the one the command writes today"; `:189` step 3: "Pass: exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path."; `:201` "Step 4 is replaced for P0, because the contract arrives in P1"; `:91` troubleshoot "`REPORT.md` (`report_path`)" | yes (the finding's quotes are abridged; AC-0.4 uses a comma, not a semicolon, and the phrases match) | yes | confirm | AC-0.4 relaxes only the report-path clause of step 3. Its outcome-to-contract `status` clause stays in force, and `:201` states no contract exists in P0, so no `status` can be matched. Step 3 therefore cannot pass, and "steps 1-3 ... pass" cannot hold for troubleshoot. The `commands-b.md:49` citation is UNVERIFIED (file absent from the workspace); `:91` alone supports the REPORT.md claim. |
| R2-2 | `:62` WC-4: "`<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)"; `:90` tdd row: "`--output <file>`" with report "the TDD at `--output`"; `:87` init-lite row: "`--output <file>`"; `:208` AC-2.2: "`/sc:tdd "auth" --unattended --output <file>`"; `:190` step 4: "`test -s <contract>`" | yes | yes | confirm | `:62` defines `<output-dir>` as a directory the coordinator passed, while `:87` and `:90` pass a file to the same flag. The candidate gives no rule for deriving a directory from a file value, so the WC-4 contract path is undefined for tdd and init-lite, and the `<contract>` in AC-2.2 step 4 cannot be resolved. Reading the file's parent directory would be an added assumption, which the candidate does not state. |

confirmed: R2-1, R2-2
