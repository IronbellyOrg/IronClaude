# T13: golden worker-list samples and per-call timing

Calls made: 3 (one for the sample, the rest only to time the call). Rows in the sample: 100.

| Call | Duration (s) |
|---|---|
| 1 | 0.220 |
| 2 | 0.197 |
| 3 | 0.187 |

Slowest: 0.220 s. Decision: keep the 10 s default; it stays unmeasured beyond this run (slowest call 0.22 s).

Redaction rules applied:

- dispatchId, taskId, runId, resource.id, worktreeId, host.id, workspace.id replaced by stable placeholders (w-001, t-001, run-a, res-001, wt-001, host-a, ws-a)
- resource.ownerDispatchId and originDispatchId mapped to the dispatch placeholder when they name a collected row, else w-ext-N
- stage.detail and stage.activity replaced by fixed synthetic text (free text is never copied)
- all timestamps shifted by one constant so the newest lands on 2026-11-08T12:00:00Z; unparsable ones become redacted-time
- keys outside the verified worker-list set are kept by name only with the value redacted; page.nextCursor becomes cursor-1; warnings become redacted warning
- any remaining string containing a slash, a terminal handle marker, a URL, an at sign or a 24+ character token is replaced by redacted

Orca version string: not read (only the two allowed read-only calls are made, and neither reports one).

Not measured: behaviour under load, a reply with more than one page, a reply with a non-empty `warnings` list unless the sample had one, any failing call. The fixtures were written to `src/superclaude/cli/observe/fixtures/golden-*.json`.
