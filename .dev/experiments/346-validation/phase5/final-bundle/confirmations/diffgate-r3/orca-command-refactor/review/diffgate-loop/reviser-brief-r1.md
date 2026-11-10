# Reviser brief: review 1 of 3

Your task list is this file, not the whole report. It lists the blocking
findings only; minor findings never reach it.

| id | label | at | hunk | chain | finding |
|---|---|---|---|---|---|
| R1.1 | major | [195, 195] | - | R1.1 | AC-1.1 contradicts the load row and the Decisions table |
| R1.2 | major | [159, 159] | - | R1.2 | P1 accepts --unattended on gated commands without defining it |
| R1.3 | major | [92, 92] | - | R1.3 | workflow cannot meet the WC-4 known-before-dispatch path |
| R1.4 | major | [83, 83] | - | R1.4 | adversarial contract path differs from WC-4 |
| R1.5 | major | [200, 200] | - | R1.5 | AC-2.2 outcome depends on the optional WC-3 branch |
| R1.6 | major | [61, 61] | - | R1.6 | re-run directory after ask is undefined |
| R1.7 | major | [185, 185] | - | R1.7 | git status step fails on prior runs' output |
| R1.8 | major | [158, 158] | - | R1.8 | P0 core Orca text conflicts with AC-C1 |
| R1.9 | major | [65, 65] | - | R1.9 | WC-7 omits the Skill-tool invocation |
| R1.16 | major | [62, 62] | - | R1.16 | existing status values collide with the WC-4 set |

Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; write the fix map only inside your own disposition file, as a `## Diffgate fixmap` block with a `doc_sha:` first line and one line per changed hunk naming its blocking ids, or `declined <id> <reason>`; run the script's read-only `fixcheck --dry-run --map <disposition file>` until it exits 0; report the byte size before and after, which `fixcheck` prints. The next review refuses to open while any hunk maps to no listed finding.

Fix map hunk ids are H2.<n>; `fixcheck` prints them.
