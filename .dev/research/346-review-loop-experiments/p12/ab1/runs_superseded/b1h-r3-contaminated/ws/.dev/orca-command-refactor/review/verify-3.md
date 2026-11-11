# Verification 3: B2

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
sha256: d7bacfaaecc8fff9a059e1e70fe785b1e6c52aecb2a57c161ca8d51cdcb3aa3c

| id | found text | exists yes/no | outcome follows yes/no | confirm or reject | reason |
|---|---|---|---|---|---|
| B2 | spec:112 load row: "use it as a step inside another worker's brief, not as its own Task" | yes | yes | confirm | Quote matches line 112 exactly. Line 159 puts `load` in P1, line 197 (AC-1.2) requires "7.2 live check on each P1 command", and 7.2 step 1 (line 180) has the coordinator run `task-create` "For each command under test". So AC-1.2 cannot pass for `load` as written, and P1 cannot pass under line 167. |
| B2 | spec:159 P1 scope lists `load` | yes | yes | confirm | Line 159 names `load (usage line, and the ## Unattended mode section ...)` under P1, so `load` is a P1 command. |
| B2 | spec:196 (AC-1.1) "applies to each P1 command" | partly | yes | reject | The phrase "each P1 command" is not on line 196; line 196 says "every command in sections 3.1-3.2". Only line 197 (AC-1.2) says "each P1 command". The misattribution does not change the outcome, which rests on AC-1.2 and line 112. The B2 finding is confirmed on the AC-1.2 text. |
| B2 | spec:197 (AC-1.2) "7.2 live check on each P1 command with `--unattended --output <dir>`" / "all steps pass" | yes | yes | confirm | Exact text at line 197. Combined with line 159 it covers `load`. |
| B2 | spec:179-180 (7.2): "For each command under test, the coordinator runs: 1. `ORCA orchestration task-create --spec "<brief per section 2.3>"`, then `worker-start`" | yes | yes | confirm | Line 179 matches. Line 180 has `task-create --spec "<brief per section 2.3>" --json` then `worker-start --task <task_id> ...`. The quote is an abbreviation; it is accurate in substance. The section defines no exemption for `load`. |
| B2 | spec:182 (7.2 step 3): "its report path is the WC-4 contract path" | yes | yes | confirm | Exact text at line 182. This is an additional conflict with line 112, which says "no `report_path`", but it is not needed for the confirmation. |
| B2 | spec:167 "A phase passes only when every check in its block and every common check passes." | yes | yes | confirm | Exact match at line 167. It makes an unpassable AC-1.2 block P1. |

Not checked: the baseline files (`spec-v2.md:112`, `spec-v2.md:197`) and the review report and grading rules. These are outside the sandbox workspace or outside my brief, and the verdict above does not depend on them.

confirmed: B2
