# Reviser brief: review 2 of 3

Your task list is this file, not the whole report. It lists the blocking
findings only; minor findings never reach it.

| id | label | at | hunk | chain | finding |
|---|---|---|---|---|---|
| R2.1 | major | [196, 196] | - | R1.1 -> R2.1 | AC-1.2 passes --output to workflow and runs the contract check on load |
| R2.2 | major | [182, 182] | H2.11 | R1.2 -> R2.2 | step 3 needs worker_status that no P0 command writes |
| R1.3 | major | [64, 64] | - | R1.3 | WC-6 fresh directory conflicts with the brief-fixed directory of WC-4 |

Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; write the fix map only inside your own disposition file, as a `## Diffgate fixmap` block with a `doc_sha:` first line and one line per changed hunk naming its blocking ids, or `declined <id> <reason>`; run the script's read-only `fixcheck --dry-run --map <disposition file>` until it exits 0; report the byte size before and after, which `fixcheck` prints. The next review refuses to open while any hunk maps to no listed finding.

Fix map hunk ids are H3.<n>; `fixcheck` prints them.
