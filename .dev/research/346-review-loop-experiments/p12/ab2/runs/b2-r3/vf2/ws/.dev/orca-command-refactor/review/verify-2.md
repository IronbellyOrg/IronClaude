# Verification of B-2

Candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md

| id | found text | exists | outcome follows | verdict | reason |
|---|---|---|---|---|---|
| B-2 | S:62 (WC-4): "writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)". S:87 (init-lite): "`--output <file>`". S:90 (tdd): "`--output <file>`" and report "the TDD at `--output`". S:183 (7.2 step 4): "`test -s <contract>` ...". S:200 (AC-2.2): "`/sc:tdd "auth" --unattended --output <file>`" expecting contract `status: blocked`. A search for dirname, sibling, parent dir and report-dir finds no rule for placing the contract when `--output` is a file. | yes | yes | confirm | WC-4 calls the `--output` value a directory, while S:87, S:90 and S:200 make it a file. The candidate gives no placement rule for the file case, so following it as written puts the contract under the TDD file. The AC-2.2 and step-4 checks then have no readable contract. |

confirmed: B-2
