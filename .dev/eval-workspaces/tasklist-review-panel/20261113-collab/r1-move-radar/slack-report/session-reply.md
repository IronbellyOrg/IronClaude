Slack is in and tested, but it barely changes k: only 1 of 9 panel and package cells moved (sl2 designSpec reader k, 0 to 1). The searcher k stays 0 on sl2 and hl2, and el2 stays 0 everywhere. The reason is that k divides headroom by two receiver turns (24 to 88 s), so 30 s adds under 1.25 messages.
- **Code:** `PANEL_SLACK_S` (default 0) now adds the 30 s to k, the finish offset, the guard offset and the SLO alarm limit in `tools/values.py`, `tools/alarms.py` and `tools/launch.sh`. The 1.5 x B hang guard is unchanged.
- **Values:** the nine new files plus `.sha256` are in `values-slack30/` (recomputed from the Spike 4 rows on disk, no model calls), and the original `values/` files are byte-identical. With `PANEL_SLACK_S=30` the launcher exits 2 if a panel's slack values are missing, for collab 0 as well as collab 1.
- **Tests:** 148 passed (138 existing plus 10 new in `tests/test_slack.py`), ruff and `bash -n` clean. Nothing was staged or committed.
- **Still blocked or useless:**
  - The guard offset is at or below 0 on all of hl2 and 8 s on sl2 designSpec, so the hook skips every injection there.
  - Collab-0 reps 1-3 and `el2-c1-r0` are finished rows and exit 2, so a new collab-0 row under slack needs rep 4 or higher.
- Everything is in `.../20261113-collab/r1-move-radar/SLACK.md` (launch commands for the six panel and arm combinations, old and new k per cell).
