
Reviser brief: your task list is `.dev/orca-command-refactor/review/diffgate-loop/reviser-brief-r1.md` (blocking ids R1.1, R1.2, R1.3, R1.4, R1.5, R1.6, R1.7). Revise only text a blocking finding names; add no rule, mechanism or section no blocking finding calls for; each added paragraph or table cites its finding id; write the fix map only inside your own disposition file, as a `## Diffgate fixmap` block with a `doc_sha:` first line and one line per changed hunk naming its blocking ids, or `declined <id> <reason>`; run the script's read-only `fixcheck --dry-run --map <disposition file>` until it exits 0; report the byte size before and after, which `fixcheck` prints. The next review refuses to open while any hunk maps to no listed finding.

verdict: FAIL
