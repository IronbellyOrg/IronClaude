# Verification 3: finding N3

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
sha256: `005c14750dde7985fd4ffcf42529a7b23cc2ca06ed4169b3ad679316a9e00f9a`

| id | found text | exists | outcome follows | verdict | reason |
|---|---|---|---|---|---|
| N3 | candidate:62 (WC-4): "In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)." Exception: "Where section 3 names a different fixed path for a command, that path is the contract path instead (adversarial: section 3.1)." | yes | yes | confirm | WC-4 defines `<output-dir>` as the value passed by `--output`, and the only exception covers a different fixed contract path, not a changed flag type. Row 86 (candidate:86) passes `--output <dir>/context-audit.md`, a file, so an implementer following WC-4 writes the contract at `<dir>/context-audit.md/return-contract.yaml`. The coordinator opens `<dir>/return-contract.yaml` (candidate:86, and candidate:73 "the output directory, so the report path is known before dispatch (WC-4)"), finds no report, and WC-5 (candidate:63) maps "no report exists" to `--outcome failed`. |

Quoted text checked in the workspace: candidate:62 (WC-4), candidate:73 (section 2.3, "the output directory, so the report path is known before dispatch (WC-4)"), candidate:86 (init-lite row, "`--unattended --output <dir>/context-audit.md` ... `<dir>` is the WC-4 output directory, so the contract is `<dir>/return-contract.yaml`"), and candidate:63 (WC-5, "`--outcome failed` when ... no report exists").

confirmed: N3
