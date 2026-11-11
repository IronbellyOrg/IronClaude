# Verification of finding M1 against orca-worker-contract-spec.md

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`, sha256 `84aa3fdce83498845e1a3cf58e05e4b1f83a15e38b34520e6f0393658bd74d26`.

| id | found text | exists | outcome follows | confirm or reject | reason |
|---|---|---|---|---|---|
| M1 | Line 62 (WC-4) says cli-portify "leaves the location unnamed, so P2 names it before its live check"; line 105 says "file location unnamed"; lines 83 and 92 name paths | yes | no | reject | The deferral is stated in the candidate itself, with an owner (P2) and a trigger (before the live check), and WC-4's default `<output-dir>/return-contract.yaml` applies to a row that names no path, so no wrong outcome follows from the text. The "revise1.md:71" cite is outside the candidate and cannot be checked in this sandbox. |
| M1.a | Line 62 (WC-4) `<output-dir>/return-contract.yaml`; line 73 "so the report path is known before dispatch"; line 83 `<output>/adversarial/return-contract.yaml` | yes | no | reject | Line 62 itself says that where a section 3 row names another path "the command writes there (M1): adversarial `<output>/adversarial/return-contract.yaml` (row 3.1)", and line 76 repeats that the contract is "at the path WC-4 or the row names". An implementer who follows WC-4 in full opens the adversarial subfolder path, so the stated wrong outcome needs the reader to ignore that clause. |

confirmed: none
