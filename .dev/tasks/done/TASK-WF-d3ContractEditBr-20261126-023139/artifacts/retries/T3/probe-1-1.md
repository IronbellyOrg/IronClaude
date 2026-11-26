f14ee7e5f5ca569ee4b6955811865b80a8fefa81
family=duplicated-definition
defect form: qa.md restates the WC-3 channel definition or its never-counts list instead of pointing to it
command: grep -n -E "authenticated login|relay of a message|row written by an agent|question id whose text" src/superclaude/skills/sc-implement-protocol/refs/qa.md
before-output:
254:A Ruling counts only when it is eligible under the Ruling eligibility rule in `refs/retry.md`. A person's confirmati
coupled sites: lines 217 and 248 (name the two channels only, in the table and the Halt row), line 256 (provenance wording)
after:
(no hit: the restated definition and never-list are gone from qa.md)
