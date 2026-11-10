# verify-2

Candidate sha256: 9d73c078966cd5e27ccbfd4e244c2f43fce5d76c7c7f2bcbc9c574c5b6690ea6

| id | found text | exists | outcome follows | confirm/reject | reason |
|---|---|---|---|---|---|
| N1 | l.159: P1 row says the flag and section go "in every command in sections 3.1 and 3.2 except load", and its Commands cell lists "analyze, build, ..., test, load (usage line only)". l.112: load "gets no `## Unattended mode` section (AC-1.1)", Report "none", "not as its own Task". l.196: "7.2 live check on each P1 command with `--unattended --output <dir>`" / "all steps pass". l.182: step 3 needs a report path equal to the WC-4 contract path. l.183: step 4 `test -s <contract>` plus YAML assertion. l.167: "A phase passes only when every check in its block and every common check passes." l.265: a report file for load "would be an unrequested addition". l.154: later phases do not start until earlier checks pass. | yes | yes | confirm | l.159 puts load in the P1 Commands cell, so l.196's "each P1 command" includes it. AC-1.1 (l.195) excludes load by name and AC-1.2 does not. Load gets no contract (l.112, l.265), so steps 3 and 4 have nothing to check, AC-1.2 cannot pass, and by l.167 and l.154 P1 does not pass and P2 does not start. |

confirmed: N1
