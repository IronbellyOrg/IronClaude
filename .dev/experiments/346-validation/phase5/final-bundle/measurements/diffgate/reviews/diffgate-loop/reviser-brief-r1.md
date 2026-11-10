# Reviser brief: review 1 of 3

Your task list is this file, not the whole report. It lists the blocking
findings only; minor findings never reach it.

| id | label | at | hunk | chain | finding |
|---|---|---|---|---|---|
| R1.1 | major | [62, 62] | - | R1.1 | WC-4 report location is unknowable or undefined for workflow, tdd, init-lite and a missing flag |
| R1.2 | major | [62, 62] | - | R1.2 | the new status field collides with existing contract status fields |
| R1.3 | major | [64, 64] | - | R1.3 | WC-6 fresh directory conflicts with the brief-fixed directory of WC-4 |
| R1.4 | major | [65, 65] | - | R1.4 | WC-7 does not require the Skill invocation and no check detects its absence |
| R1.5 | major | [172, 172] | - | R1.5 | AC-C1 scans the folder that holds the contract file SA-2 lets mention Orca |
| R1.6 | major | [195, 195] | - | R1.6 | load has no report but AC-1.1 requires one |
| R1.7 | major | [228, 228] | - | R1.7 | no parse rule for the --unattended token |

Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; write the fix map only inside your own disposition file, as a `## Diffgate fixmap` block with a `doc_sha:` first line and one line per changed hunk naming its blocking ids, or `declined <id> <reason>`; run the script's read-only `fixcheck --dry-run --map <disposition file>` until it exits 0; report the byte size before and after, which `fixcheck` prints. The next review refuses to open while any hunk maps to no listed finding.

Fix map hunk ids are H2.<n>; `fixcheck` prints them.
