# Flags decision

- Decided by: issue-worker-t2
- Depth: quick

| Field | Value | Reason |
|---|---|---|
| Mode | bug | The description reports an existing worker stalling indefinitely because of a verifier report-writing restriction, not a request for a new capability. |
| Type | agent | The reported failure concerns worker/verifier agent instructions and report-writing restrictions; the exact enforcement mechanism is not known yet. |
| Complexity | simple | follows depth (quick = simple, standard = medium, deep = complex); this is a depth label, not an estimate of all risks. |
