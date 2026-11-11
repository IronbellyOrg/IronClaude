# Verification of blocking findings M4 and N1

Candidate: `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
sha256: `7c8aa27b2871ce92c01502f179de64ec96be2031fdf14b1198dc4230f55a9adc`
Method: `grep -nF` and line reads of the candidate. Line numbers below are candidate lines.

| id | found text | exists | outcome follows | confirm or reject | reason |
|---|---|---|---|---|---|
| M4 | Line 206: "step 4 is `test -s` on that report"; line 206: "the report path against the command's existing report"; line 195: "In P0 only `test -s` on the command's existing report applies"; line 83 (adversarial row): "contract, but filename not fixed" | yes | yes | confirm | The candidate's own adversarial row says the filename is not fixed, and no P0 text names the existing adversarial report file. Step 4 therefore cannot be run on adversarial without the implementer choosing a file. INV-A:35 and INV-A:60 are cited in the finding but are not in the workspace, so they are UNVERIFIED; the confirmation does not rely on them. |
| N1 | Line 207: "the test asserts that every command in sections 3.1-3.2 except `load` has a `## Unattended mode` section naming `return-contract.yaml` and `~/.claude/WORKER-CONTRACT.md`" | yes | yes | confirm | AC-1.1 is a P1 check (line 207). Line 159 (P1 scope) adds the `--unattended` flag to every command in 3.1 and 3.2 but names no section for 3.2 commands. Line 79 adds the section only to the ten ready 3.1 commands. auggie-review is phased P2 (line 100), so P1 does not change it, and the literal AC-1.1 check fails on it. The finding's remark that the spec "does not say which phase adds it" is only partly accurate: lines 52 and 76 say every changed command gains the section, so the phase is implied by the phase column. The wrong outcome still follows from the literal check text without that inference. Phase rule at line 167 confirmed: a phase passes only when every check in its block passes. Row counts confirmed: 27 section 3.2 rows, 18 phased P2 to P4. |

confirmed: M4, N1
