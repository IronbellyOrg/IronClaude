# AC-0.6: do tool calls appear by name in the worker transcript?

Question (spec line 303): in `worker-read --source transcript`, do tool calls appear by name?

Answer: **yes**.

Evidence, from the saved worker-read output `./artifacts/lc1-transcript-limit1000.json` (50 transcript messages, the last 11 minutes of the run):

- Lines 29-30: `"type": "tool-call",` / `"name": "Agent",` with `"description": "Adversarial Step 5 merge execution"`.
- Lines 62-63: `"type": "tool-call",` / `"name": "Bash",` with `"description": "Log Steps 3-4 result and heartbeat"`.
- Lines 94-95 of the same file: `"type": "tool-call",` / `"name": "Read",`.
- Tally of all `tool-call` blocks in that file: `Agent=3 Bash=9 Read=3 Write=5` (each block carries `name`, `input` and a `callId`).
- The first read of the run (06:07 UTC, not saved as a file, seen in this session) showed `"name": "Write"` for `.dev/p0-live/troubleshoot/tier1-observation.md`.

Limit that applies to this answer: the transcript returned by worker-read is not complete (see `lc1-step5.md`, "worker-read completeness"). The answer is still yes, because every `tool-call` block in the returned window carries a `name`. Step 5 for checks 2 and 3 therefore uses the transcript source (this answer is not "no").
