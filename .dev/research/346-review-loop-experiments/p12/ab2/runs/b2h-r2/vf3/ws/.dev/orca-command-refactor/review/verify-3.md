# Verification of B-2 against the candidate spec

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (sha256 `b72ae0165828ae31e6e86c4c17ddcc94a378f90648e36bc5398fab3017942e03`, 286 lines).

Sandbox note: the workspace holds only the candidate spec. `command.md`, `cmd/spec-panel.md`, and `INV-B` (cited as the evidence for the outcome) are not in the workspace, so every citation to them is UNVERIFIED here.

## Quoted text located in the candidate

- spec:120 (spec-panel row, `grep -nF` hit): `add `--output-dir <dir>` (B-2; no output flag exists today, `INV-B:182`; UNVERIFIED item 15 applies if the command already takes a directory flag)`
- spec:286 (item 15): `P2 checks it first: if a directory flag exists, the spec-panel row uses that name and adds no second flag (B-2).`
- spec:286 also contains: `that file is outside the inventory and was not checked in the B-2 revision.`
- spec:62 (WC-4): `In unattended mode the command writes `<output-dir>/return-contract.yaml`` (the "written on every outcome" wording is in the same row).
- spec:201 (AC-2.3): `Happy-path run per P2 command with every required flag in the brief`.

## Table

| id | found text | exists | outcome follows | confirm or reject | reason |
|---|---|---|---|---|---|
| B-2 | spec:120 "add `--output-dir <dir>` ... UNVERIFIED item 15 applies if the command already takes a directory flag" and spec:286 "if a directory flag exists, the spec-panel row uses that name and adds no second flag (B-2)" | yes (both quotes match the candidate verbatim) | no | reject | The stated wrong outcome (command refused before any work without `--report-dir`, so no contract is written) rests on `command.md:460` and `command.md:461`, which are outside the candidate and not in the workspace, and on `INV-B:182`. The candidate does not state that the spec-panel command lacks a directory flag or refuses `--output-dir`. Spec:120 is itself conditioned on item 15 ("UNVERIFIED item 15 applies if ..."), so it is not a flat instruction to add a flag that contradicts spec:286; the two texts agree that the check decides the row. Without the external command text, the chain to a failed WC-4 or AC-2.3 is an unstated assumption. |

confirmed: none
