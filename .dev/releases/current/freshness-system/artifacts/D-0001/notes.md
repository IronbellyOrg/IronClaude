# D-0001 notes — current location of `session-init.sh`

## Search

```bash
find /config/workspace/IronClaude -maxdepth 5 -name session-init.sh
```

## Findings

Two copies on disk (source + plugins mirror):

| Path | Role |
|---|---|
| `src/superclaude/scripts/session-init.sh` | Canonical source |
| `plugins/superclaude/scripts/session-init.sh` | Plugin distribution mirror |

Note: these live under `src/superclaude/scripts/` (NOT under `src/superclaude/hooks/scripts/`). The freshness hooks will live under `src/superclaude/hooks/scripts/` (created in T01.02). At install time, `install_hooks.py` (T04.01) must copy session-init.sh from `src/superclaude/scripts/session-init.sh` AND all freshness scripts from `src/superclaude/hooks/scripts/freshness-*.sh` into `~/.claude/hooks/`.

## Hand-off to T04.01

`install_hooks.py`'s script-copy list should include:

```python
SCRIPT_SOURCES = [
    ("src/superclaude/scripts/session-init.sh", "session-init.sh"),
    ("src/superclaude/hooks/scripts/freshness-session-start.sh", "freshness-session-start.sh"),
    ("src/superclaude/hooks/scripts/freshness-user-prompt.sh", "freshness-user-prompt.sh"),
    ("src/superclaude/hooks/scripts/freshness-pre-edit.sh", "freshness-pre-edit.sh"),
    ("src/superclaude/hooks/scripts/freshness-post-read.sh", "freshness-post-read.sh"),
    ("src/superclaude/hooks/scripts/freshness-file-changed.sh", "freshness-file-changed.sh"),
    ("src/superclaude/hooks/scripts/freshness-subagent-start.sh", "freshness-subagent-start.sh"),
    ("src/superclaude/hooks/scripts/freshness-subagent-stop.sh", "freshness-subagent-stop.sh"),
]
```

All 8 scripts deposited to `~/.claude/hooks/` with mode 0755.
