# Executor notes (not part of the ledger grammar)

- Reviews: every per-task review and the final review were done inline by the executing session, not by fresh sub-agents. The protocol asks for fresh reviewers once N is above 3 and for the archive-gate review; the session runs under a standing user instruction not to start sub-agents, so this is a recorded deviation, not an independent review.
- T5 ledger line: the first write cited log lines 4 and 8 by mistake (line 8 does not exist); corrected in place to 4-5 and 7 before the next task started, so the ledger is not strictly append-only for that one line.
- Reflect finding F-1 (cap fixture totals): handled inside Task 5. The totals block also carried by_group prd-core and by_kind cap counts, which were updated too.
