# Analysis report: src/superclaude/cli/issue_watch (architecture, quick)

Run: `/sc:analyze src/superclaude/cli/issue_watch --focus architecture --depth quick --unattended --report-dir .dev/issuecleanup/b/12/analyze`
Master: f2894fc44 (worktree `/home/coder/workspaces/worktrees/IronClaude/Realign`). Date: 2026-11-24.
Codegraph: index_state=fresh, checked_at=2026-11-24T22:21:54Z; degraded: none

## Layout (codegraph_files, 15 python files, about 6,965 lines)

`record.py` (store: entries, lock, day cap), `cycle.py` (config, one poll cycle, status report), `dispatch.py` (run-all dispatcher), `first_run.py` (automatic first-run check), `cli.py` (verbs), `github.py`, `predicates.py`, `launch.py`, `audit.py`, `generate.py`, `defaults.py`, `repos.py`, `repo_init.py`, `runner.py`.

## Findings (architecture)

| # | Severity | Finding | Evidence |
|---|---|---|---|
| A1 | Low | The only unbounded growth in `dispatch.json` is `entries`. `considered` is pruned to the discovered issues on every save, and `consumed_log` is pruned to 24 h. No code removes a finished entry except `reset_entry`, and only for `abandoned` or `unknown`. | `record.py:738-745` (`set_considered`), `record.py:693-696` (`prune_consumed_log`), `record.py:706-720` (`reset_entry`, `_RESETTABLE` at `record.py:448`) |
| A2 | Low | An entry is also the at-most-once memory: a `claimed` or `pending` entry makes the cycle skip the issue (`already_dispatched`), an `abandoned` tombstone is reclaimed only through `_reclaim`. A prune rule must keep exactly those. | `cycle.py:981-996` |
| A3 | Info | The six entry states on master are the only states a prune rule can meet. The plan's wider list (woken, acked, waiting_reapproval) belongs to the not-adopted orchestrator design (owner row R38). | `record.py:34` (`ENTRY_STATES`), `requirements.md:64` (R38) |
| A4 | Low | The network-filesystem refusal exists in `cycle.load_config`, the one loader every verb uses, so one change there reaches `check-config`, `once`, `status`, `run-all` and the first-run check. Refusing there stops every cycle with `config_invalid`. | `cycle.py:293-295`, `cycle.py:50` (`NETWORK_FS_TYPES`) |
| A5 | Low | No non-persistent type (tmpfs, ramfs) is refused; tests pin both the deny set and tmpfs as allowed. | `tests/issue_watch/test_cycle.py:498-501`, `:520-525` |
| A6 | Info | Store size on the live host today: 1,631 bytes for IronClaude (read-only `stat`), against a 1 MiB trigger. The audit log, which already rotates, is the larger file (1,976,719 bytes). One sample entry measures about 619 bytes serialized (indent 2, sorted keys), so 1 MiB is about 1,700 entries. | `stat` on `~/.local/state/superclaude/issue-watch/IronClaude/`; `record.py:374` |

## Recommendations

1. #821: keep the item deferred; state the finished-entry rule and the `consumed_log` hand-off before any build (A1, A2).
2. #822: narrow to tmpfs/ramfs as a second set beside `NETWORK_FS_TYPES` (A4, A5).
3. #823: documentation only; the contradiction and the six-field cron line live in `docs/designs/issue-watcher-setup.md`.

No source changed. Nothing pushed, committed or staged.
