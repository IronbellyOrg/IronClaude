---
assertion: A10
domain: io
polarity: neg
expected_flags: []
---
--- file: REPORT.md ---
status: blocked
--- file: diagnosability-tasklist.md ---
**Round**: 1 of 3  **re-run permitted**: unknown  **capability-verdict**: blocked
## Emitter search
emitters-found: 0
already-read-files: 2
usable-capture-routes: 0
channels searched: startup.sh seed function, test-startup-boot.sh caller, job log, REPORT.md.draft
channel exclusions: seed and caller have no existing emitters or accessible predicate value; no job log was preserved; draft contains only generated analysis.
candidate exclusions: startup.sh:583 and test-startup-boot.sh:18 are the two read files; neither preserves the transient predicate value or exposes it to an invocation-site wrapper. Adding an expected value to the draft would not capture the datum.
## Discriminator rows
| row | value-if-true | value-if-false |
|---|---|---|
| uptime-regex | false | true |
