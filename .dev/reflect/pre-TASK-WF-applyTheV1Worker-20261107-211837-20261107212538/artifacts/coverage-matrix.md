# Coverage matrix (UC-1, two-pass)

Spec: `.dev/tasks/to-do/TASK-WF-applyTheV1Worker-20261107-211837/source.md` (line 1, inline prompt).
Plan: `.dev/tasks/to-do/TASK-WF-applyTheV1Worker-20261107-211837/TASK-WF-applyTheV1Worker-20261107-211837.md`.

Pass 1 (explicit IDs: C-1..C-8, C-15..C-17) and Pass 2 (inferred rows INF-NNN, each quoting source.md:1).

| Req | Source text (source.md:1) | Plan location | Result |
|---|---|---|---|
| C-1 | "rules C-1 to C-8 and C-15 to C-17" | Task 1, plan:35 | covered |
| C-2 | "the C-2 progress token rides in the subject/phase or status body line" | Task 2, plan:46; Constraints plan:22 | covered |
| C-3 | rules C-1 to C-8 | Task 3, plan:57-58 | covered |
| C-4 | rules C-1 to C-8 | Task 3, plan:59 | covered |
| C-5 | rules C-1 to C-8 | Task 4 (WC-14), plan:72 | covered |
| C-6 | rules C-1 to C-8 | Task 4 (WC-15), plan:72 | covered |
| C-7 | "C-7 is a new 'Liveness supervision' subsection" | Task 6, plan:94-104 | covered |
| C-8 | rules C-1 to C-8 | Task 7, plan:117-121 | covered |
| C-15 | "a person-directed cancellation with confirmed quiescence settles a live attempt" | Task 5, plan:84 | covered |
| C-16 | rules C-15 to C-17 | Task 3, plan:60 | covered |
| C-17 | rules C-15 to C-17 | Task 1, plan:35 | covered |
| INF-001 | "never resend a mailbox copy ... report to the person at 15 minutes" | Task 6, plan:98; Constraints plan:26 | covered |
| INF-002 | "check --wait --types only decides when a waiter wakes ... shared by several waits on one Run inbox" | Task 6, plan:95 | covered |
| INF-003 | "worker-list rows carry projection.liveness {verdict live|unverifiable|exited, observedAt, source}, projection.stage.activity, projection.attention.categories, requiresAction/nextAction" | Task 6, plan:96 names "one `worker-list`" only | partial |
| INF-004 | "worker-read --source transcript entries carry millisecond timestamps" | not named in any task | partial |
| INF-005 | "'unverifiable' is absence and never authorizes stop/abandon/retry/release" | Constraints plan:27; Task 6 plan:101 | covered |
| INF-006 | "leave a wait only on positive proof" | Task 6 plan:99 (C-7 stall-proof sentence) | covered |
| INF-007 | five "Mark as UNVERIFIED" items | Constraints plan:25; Task 6 plan:102 | covered |
| INF-008 | "check whether WORKER-CONTRACT.md has other byte-for-byte copies" | Task 7 plan:129 | covered |
| INF-009 | "edit src/superclaude then run make sync-dev (never stage .claude/ mirrors)" | Task 7 plan:123; Constraints plan:21 | covered |
| INF-010 | "nothing for the v2 monitor, adapters, hooks or dashboard; no new code beyond tests" | Constraints plan:20 | covered |
| INF-011 | "make lint, make verify-sync and uv run pytest tests/skills pass" | Task 7 plan:123-128 | covered |
| INF-012 | "a background heartbeat loop is allowed ... a timer heartbeat is not progress evidence" | Task 2 plan:46 (keeps "evidence that the process exists, not that the work is progressing") | covered |

Parsed-only coverage: 11/11 = 1.00. Union coverage (partial = 0): 21/23 = 0.913. Union with partial = 0.5: 22/23 = 0.957.
Unmapped (union, strict): INF-003, INF-004 (both partial; both fall inside C-7's "summarising spec sections 4, 6, 7 and 8" scope).
