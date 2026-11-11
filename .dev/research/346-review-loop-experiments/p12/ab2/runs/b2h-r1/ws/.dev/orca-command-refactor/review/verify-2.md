# Verification 2: N2-01

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md` (sha256 `00cb7b63ea6019f358ead17f8b721ad6058432fb1bebc97218c1af92404e5038`, 285 lines).

Checked with `grep -nF` and `sed` inside the workspace. `.dev/orca-command-refactor/inventory/commands-b.md` is not in the workspace, so the `commands-b.md:242` citation and the `INV-B:242` citation are UNVERIFIED and were not relied on.

| id | found text | exists | outcome follows | confirm or reject | reason |
|---|---|---|---|---|---|
| N2-01 | spec:182 step 3 pass condition: "**Pass:** exactly one `worker_done`; its `--outcome` matches the contract's `status` under WC-5; its report path is the WC-4 contract path." (line 182, exact match) | yes | yes | confirm | The clause is in step 3 and spec:194 (AC-0.4) overrides only step 4 and the step 3 outcome source, not the path clause. WC-4 (line 62) defines the contract as written "In unattended mode". The P0 smoke runs do not carry `--unattended`: section 3.1 (line 79) says the ready commands "run as workers now", the troubleshoot row (line 91) lists only "no `--fix`" and "Report today: `REPORT.md`", and P0 (line 158) is "no command edits" with smoke runs listed without the flag. `--unattended` is added only in P1 (line 159). So no WC-4 contract exists in P0, and the clause cannot be met by the file the run actually writes (`REPORT.md`, line 91). The spec's own P0 text (line 194) also confirms the contract "arrives in P1 (F-03)". |

Notes on the finding's citations:

- spec:81 and spec:91 are cited for the P0 flags. Line 81 is the table header row of section 3.1 and line 79 holds the "run as workers now if the brief uses the stated flags" sentence. The content is the same, only the line number differs.
- spec:194 quote ("since the contract arrives in P1 (F-03)") exists as quoted.
- spec:62 quote ("In unattended mode") exists as quoted.
- spec:91 quote (`REPORT.md`) exists as quoted.
- spec:158 quote ("no command edits") exists as quoted.
- One residual point: a literal reading could satisfy the clause by passing a path string equal to `<output-dir>/return-contract.yaml` even though no such file is written in P0. The candidate does not say to do that, and it would not be "the WC-4 contract" in any sense the spec defines, since WC-4 describes a file written on every outcome. The finding's outcome therefore holds for the reading the spec supports.
- Side observation, not part of N2-01: line 73 requires the brief to carry `--unattended` for every Task, which cannot be followed in P0 because the flag is not yet accepted (line 159). This is a separate issue and is not confirmed or rejected here.

confirmed: N2-01
