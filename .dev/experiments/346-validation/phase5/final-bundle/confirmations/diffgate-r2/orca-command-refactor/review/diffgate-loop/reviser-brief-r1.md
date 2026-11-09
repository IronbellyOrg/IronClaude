# Reviser brief: review 1 of 3

Your task list is this file, not the whole report. It lists the blocking
findings only; minor findings never reach it.

| id | label | at | hunk | chain | finding |
|---|---|---|---|---|---|
| R1.1 | major | [62, 62] | - | R1.1 | WC-4 status vocabulary conflicts with existing contracts |
| R1.2 | major | [62, 62] | - | R1.2 | WC-4 assumes every command takes an output directory |
| R1.3 | major | [83, 83] | - | R1.3 | adversarial contract path differs from WC-4 |
| R1.4 | major | [159, 159] | - | R1.4 | --unattended behaviour on gated commands before their phase is unspecified |
| R1.5 | major | [68, 68] | - | R1.5 | WC-10 conflicts with WC-7 for Agent-tool waves |
| R1.6 | major | [65, 65] | - | R1.6 | WC-7 does not require or check the Skill or command call |
| R1.7 | major | [147, 147] | - | R1.7 | SA-2 allowance contradicts AC-C1 |
| R1.8 | major | [200, 200] | - | R1.8 | AC-2.2 ignores the WC-3 ask branch |

Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; write the fix map only inside your own disposition file, as a `## Diffgate fixmap` block with a `doc_sha:` first line and one line per changed hunk naming its blocking ids, or `declined <id> <reason>`; run the script's read-only `fixcheck --dry-run --map <disposition file>` until it exits 0; report the byte size before and after, which `fixcheck` prints. The next review refuses to open while any hunk maps to no listed finding.

Fix map hunk ids are H2.<n>; `fixcheck` prints them.
