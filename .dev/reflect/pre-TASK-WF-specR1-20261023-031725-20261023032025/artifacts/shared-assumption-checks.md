# Shared-assumption checks (orchestrator, read-only, 2026-10-23)

## A-001: /sc:implement execution order
$ sed -n 97p ~/.claude/skills/sc-implement-protocol/SKILL.md
Default sequential in source order. Parallel only when the source marks a set independent (literal `independent`, `parallel-ok`, or heading `Independent`) **and** set size ≤ 3. Unmarked = sequential. If overlap is obvious (`same file`), stay sequential. (a) A batch is formed only from tasks that have no `start` line, and it writes every member's `start` line, in source order, before any member begins Q1; a member not started by then waits for the next batch. (b) The next task or batch starts only after every member of the batch has its own `complete` or `halt` line; a `halt` then STOPs the run (Q8), it never lets the run continue. (c) A task that already has a `start` line (any resumed task) never joins a batch: it runs alone, and whether it is a batch task is read from the ledger (`refs/retry.md`), never from this invocation. A batch task gets no retry ladder: when A2 fails it halts `batch` (`E-HALT-QA`), and nothing in a batch is reverted.
-> HOLDS: tasks run sequentially in source order unless marked independent; the tasklist marks none independent, so Tasks 3-6 run before Tasks 8-9 at execution time.

## A-002: git stub reachability
$ grep -n "/usr/bin/git\|command git\|\\git " .github/workflows/pull-sync-framework.yml
(no match)
-> HOLDS: the run body calls git by bare name only, so a PATH-prepended stub intercepts it.

## A-003: not checkable by command; debated.

## Orchestrator note for Round 2: source:82 is satisfiable
Renumber so the Codecov research task sits immediately before the Codecov edit: 1 baseline, 2 GitHub settings/docs, 3 three-dot proof, 4 boundary-guard edit, 5 sync edit, 6 Codecov research, 7 Codecov edit, 8 workflows README, 9 scripts README + scope. Chain 2->1, 3->2, 4->3, 5->4, 6->5, 7->6, 8->7, 9->8: every Depends on names one lower-numbered task, Task 7 depends on the Codecov research task (not the sync task), and Tasks 8 and 9 have every earlier edit as an ancestor. So both sentences of source:82 can hold at once.
