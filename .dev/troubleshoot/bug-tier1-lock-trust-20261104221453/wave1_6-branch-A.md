# Wave 1.6 Branch A (log-call inspection), persisted on receipt; degraded: false

| site (file:line) | emission | richness | note |
|---|---|---|---|
| refs/conflict-mechanical.md:35-44 | plan report before any edit: tier, path classes (`regen:uv.lock`), conflict_action row | rich (paths) | names the lock rule, not what regenerating it runs |
| refs/conflict-mechanical.md:71 | `sync_started{...merge identity..., paths, resumed}` before the merge | rich (merge identity) | no field for the lock command, build backend or pyproject content |
| refs/conflict-mechanical.md:84-90 (step 5) | precheck `{"precheck":"ok"}`; checkout --ours, uv lock, uv lock --check, git add | silent | nothing written to the run-log around `uv lock` |
| refs/conflict-mechanical.md:94, :290 | uv failure -> abort, `sync_merge_failed` with the failing command's output | minimal | failure only; a successful uv lock leaves no trace |
| refs/conflict-mechanical.md:216-223 | abort: MERGE_HEAD ownership check, `git merge --abort`, `sync_concluded{aborted}` | minimal | outcome and reason only |
| refs/conflict-mechanical.md:275, :279-302 | `terminal_halted{reason}` after `sync_concluded{halted|aborted, reason}` plus operator message | minimal | fixed reason codes |
| refs/conflict-mechanical.md:126 | "no tests ran for the regenerated lock file; CI on the merge head is the test signal" | minimal | VAL commentary |
| conflicts.py:202-210 | MECHANICAL_RULES uv.lock: sources ("pyproject.toml",), regenerate ("uv","lock"), check ("uv","lock","--check") | static | only declared input is the label pyproject.toml |
| conflicts.py:1302-1338 | merge_commit_message Tier 1 body "uv.lock regenerated from the merged pyproject.toml" + optional lock_changes | minimal | labels only (docstring :1316) |
| models.py:94-95 | EventType.SYNC_STARTED / SYNC_CONCLUDED | n/a | only conflict-cycle event types |

Before the fix nothing records which build backend or pyproject fields `uv lock` would execute (no `build-backend|build-system` match in src/superclaude).
