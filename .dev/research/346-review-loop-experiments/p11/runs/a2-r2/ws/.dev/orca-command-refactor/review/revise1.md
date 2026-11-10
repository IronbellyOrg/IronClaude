# Revision 1: orca-worker-contract-spec.md

Candidate edited in place: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`.
Input findings: `.dev/orca-command-refactor/review/round1.md:249-251` (Reviser brief: blocking ids B1, B2; do not act on M1 to M13 or N1 to N8).
Contract kept: only text that B1 or B2 names was revised; every edit below cites its finding id; no new section or table; no PASS is claimed. Line numbers are those of the candidate before and after (no edit added or removed a line). Citations to the candidate are `S:N`; to the report `R1:N`.

## Byte accounting

Candidate size (`wc -c`): before 57763 bytes, after 58349 bytes, net +586 (57763 + 586 = 58349).

| Finding id | Bytes added | Bytes deleted | Net | Lines edited |
|---|---|---|---|---|
| B1 | 185 | 0 | +185 | S:76, S:195 |
| B2 | 804 | 403 | +401 | S:62, S:76, S:83, S:92 |
| Total | 989 | 403 | +586 | |

Method: "added" and "deleted" count the bytes of each replaced or inserted string as measured with `len(s.encode())` on the exact old and new strings of each edit; a replaced phrase counts as deleted in full and added in full. B1 edits are pure insertions. The nets reconcile with the two `wc -c` readings.

## Disposition table (one row per finding id)

| Id | Disposition | Where applied (candidate line) | Reason and citation |
|---|---|---|---|
| B1 | Applied | S:76: "Every changed command except `load` (no contract, row below) also gains the `## Unattended mode` section (section 2.1), in the phase its row names." S:195 (AC-1.1): the test now asserts the section on every command of 3.1-3.2 except `load` and the P4 commands implement, post-release, pr-submit (their sections arrive in P4 after D2-D4); asserts that `load` and no section-4 command has one. | R1:98-103. The contradiction was AC-1.1 requiring a section on `load` while the load row says report "none" (S:112) and Decisions says a report file would be unrequested (S:265); and AC-1.1 requiring pr-submit, implement and post-release sections before D2-D4 (S:162, S:225, D3(a) at S:240). The report's recommendation (R1:103) names both exclusions. Under D3(a) pr-submit gets no section, which the P4 exemption now permits. Load row (S:112), Decisions (S:265), P1 flag scope (S:159) and D2-D4 left unchanged: they are consistent with the revised AC-1.1 and S:76. |
| B2 | Applied | S:62 (WC-4): contract path is `<contract-dir>/return-contract.yaml`, where `<contract-dir>` is the brief's `--output-dir` or directory-valued `--output`, or the parent directory of a file-valued `--output` (tdd, init-lite); an output flag added in P1-P3 is directory-valued; a command whose contract sits elsewhere today also writes it here (adversarial, workflow). S:76: "Contract" now means `<contract-dir>/return-contract.yaml`. S:83 (adversarial): contract at `<output>/return-contract.yaml`, since the skill names no file today. S:92 (workflow): the brief also passes an output directory (new `--output-dir` flag, P1), the contract is also written to `<output-dir>/return-contract.yaml` including for pre-creation STOPs, because `<id>` is unknown before dispatch; the package copy stays as today. | R1:138-143. Case 1 (tdd, init-lite file-valued `--output`, S:87, S:90, AC-2.2 at S:200): covered by the parent-directory clause. Case 2 (adversarial subdirectory): the inventory says the skill names no filename and real runs wrote two different places (`inventory/commands-a.md:35`, `inventory/commands-a.md:60`), so choosing `<output>/return-contract.yaml` breaks no stated behaviour. Case 3 (workflow generated id, pre-creation STOP): `inventory/commands-b.md:272` states the contract is written only post-creation, in `.dev/tasks/to-do/<id>/`, and the id is unknown before dispatch; the passed directory fixes that. Case 4 (spec-panel new `--output` of unstated type, S:120): covered by "an output flag added in P1-P3 is directory-valued". 7.2 step 3 (S:182) and AC-1.2 (S:196) cite "the WC-4 contract path" and now resolve to one rule. The report's example used `--report-dir`; this revision reused the existing `--output-dir` / `--output` flags instead, so no new flag name is introduced beyond the workflow `--output-dir` the report required (R1:143). Whether `/sc:workflow` already has an output flag is UNVERIFIED (command file not in the workspace; `inventory/commands-b.md:52` and `:272` list none). |
| M1 to M13 | Not acted on | none | R1:251 (Reviser brief): do not act on M1 to M13 in this cycle. |
| N1 to N8 | Not acted on | none | R1:251. |

## Notes for the next reviewer

- Edits are the smallest that remove the stated contradictions; nothing was deleted from the Evidence columns, Decisions or open decisions.
- One consequence the reviewer may weigh: P1 (S:159) still says every command in 3.1 and 3.2 accepts `--unattended`. That statement is about the flag, not the section, and was not named as contradictory by B1 or B2, so it was left alone (it touches M4).
- Two byte figures are not independently verified by a tool other than `wc -c` and the string-length measurement named above.
