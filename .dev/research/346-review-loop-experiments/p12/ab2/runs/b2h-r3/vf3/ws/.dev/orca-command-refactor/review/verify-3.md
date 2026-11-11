# Verification 3: finding N-2

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
sha256: `39bbe6871713a48397dee32c0a486174eebbc1b08a14833316eed1593df495bb`

## Texts found in the candidate

- SPEC:62 (WC-4), first sentence: "In unattended mode the command writes `<output-dir>/return-contract.yaml`, where `<output-dir>` is the directory the coordinator passed (`--output` / `--output-dir`)."
- SPEC:62 (WC-4), F-02 clause: "F-02: a file-valued output (`--output <file>`, as in tdd and init-lite; `INV-B:47`, `INV-A:55`) uses the file's parent directory as `<output-dir>`, and its contract is `<output-stem>.return-contract.yaml` in that directory, where `<output-stem>` is the file name without its extension (N-1: two file outputs in one directory then write two contracts, not one shared `return-contract.yaml`)."
- SPEC:62, last sentences: "The worker passes the contract path as `worker_done --report-path`. Orca does not check the file, so the coordinator opens it."
- SPEC:69 (WC-11): "Two workers in one worktree must never write the same file."
- SPEC:87 (init-lite): "Contract at `<parent of --output>/<output-stem>.return-contract.yaml` (P1; F-02, F-04, N-1)"
- SPEC:90 (tdd): "`--output <file>`"

All quoted texts exist in the candidate as quoted. The `INV-A:55`, `INV-B:47`, `INV-B:52` and `RR:78` references point to files outside the sandbox and were not checked.

## Row

| id | found text | exists | outcome follows | confirm or reject | reason |
|---|---|---|---|---|---|
| N-2 | SPEC:62 F-02 clause (`<output-stem>.return-contract.yaml`, stem drops extension) with SPEC:62 first sentence (`<output-dir>/return-contract.yaml`); SPEC:69 WC-11 "must never write the same file"; SPEC:87 and SPEC:90 file-valued outputs | yes | no (grading sentence A follows; grading sentence B does not) | reject | Grading sentence A holds: `docs/a.md` and `docs/a.txt` in one worktree both map to `docs/a.return-contract.yaml` under the F-02 clause, which contradicts WC-11 and the N-1 promise on the same line, so the second write replaces the first. Grading sentence B fails: the first sentence names `<output-dir>` as "the directory the coordinator passed", which for `--output <file>` is a file, so it does not supply a parent directory. F-02 is the specific clause for file-valued outputs and names the stem-based path, so `docs/return-contract.yaml` for every file-valued run follows only if the general first sentence is assumed to override F-02, which the text does not say. The finding requires both outcomes, so it is rejected. The A case alone is text-supported and could be restated as a separate finding, but this verification does not add one. |

confirmed: none
