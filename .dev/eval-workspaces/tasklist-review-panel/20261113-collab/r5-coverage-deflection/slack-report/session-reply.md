| Status | Result |
|---|---|
| DONE | The cap is now `1.35 x B + PANEL_SLACK_S` (default 0). Code is in `lib/r5/timing.py` and `lib/r5/collab.py`; the launchers are `bin/launch.sh`, `run-panel.sh` and `pins-check.sh`. |
| DONE | Full suite: 125 passed, 0 failed, 0 skipped (108 old, 17 new). Slack values are in `config/values-slack30/{el2,hl2}/` with their own `SHA256SUMS`, and `pins-check` is OK. |
| NEXT | Owner decision: `k` is still 0 on all six el2/hl2 packages, so `PANEL_COLLAB=1` still exits 3 on both panels. |

- **No `config/SHA256SUMS`:** the design has no such file, so I wrote and check the per-panel `values-slack30/<panel>/SHA256SUMS` instead. All commands, the old-versus-new table, and what refuses to run and why are in `SLACK.md` in the design folder.
- **sl2:** it has no slack values (design 5 never runs there by owner order). `PANEL_SLACK_S=30` on sl2 exits 2 with a clear message.
- **Hang guard (your call):** it stayed at `1.5 x B`, so on el2 it fires 8 to 12 s before the new cap and kills reviewers that were still inside the allowed time. To let every reviewer finish, set the hang guard to `max(1.5 x B, 1.35 x B + 30)` (a one-line change, but the values files would need recomputing).
- **Test fix:** two re-ask tests first failed because this sandbox can't read `/proc/sys/kernel/random/uuid`. I gave `tests/fake/claude` a fallback session id.
- **Not run:** A1 launches on el2 and hl2 were not run (no model sessions).
