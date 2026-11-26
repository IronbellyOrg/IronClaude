2026-11-24T18:14:29Z clayphi
@ironbelly thank you for this list. A read-through of how the watcher behaves when it runs for a long time left three small questions. Please correct anything we have misread.

1. **Skips and the 100-issue stop (W8).** W8 plans an alert after three bad cycles. Could it also cover (a) a way to see which issues were skipped and why without reading audit.jsonl, and (b) the stop at 100 labelled issues ("truncated")? Claimed issues keep the trigger label, and the runbook says to remove it by hand, so the count only falls when an issue closes. Would removing the label when a claim finishes be acceptable, or is the label kept on purpose?
2. **Repos of other orgs.** By default only IronbellyOrg repos are watched. Is adding <private-org> planned, and where should the owners list live?
3. **Pace.** One launch per sweep and six per repo per day look right for a first live run. We would suggest revisiting both once the first runs show where work queues.

Happy to help with any of these.

