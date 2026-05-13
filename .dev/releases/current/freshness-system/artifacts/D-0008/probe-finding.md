# D-0008 — T02.05 Probe Finding

**Date:** 2026-05-13
**Outcome:** Design assumption invalidated. Registration removed in v1.

## Probe execution

1. Ran `probe-deploy.sh` — swapped the production handler at `~/.claude/hooks/freshness-file-changed.sh` for a stdin-capture shim. Backed up the real handler to `…freshness-file-changed.sh.real`.
2. Started a fresh Claude Code session in `/tmp/freshness-test-1`.
3. Asked Claude to Read `compose.yml`. (Read tool fired; PostToolUse appended to reads.jsonl.)
4. From a separate terminal: `echo "# external change" >> /tmp/freshness-test-1/compose.yml`.
5. Asked Claude to check `~/.claude/logs/file-changed-probe-*.json`.
6. **No probe files existed.** FileChanged never fired.
7. Ran `probe-revert.sh` — real handler restored.

## Root cause (from [Claude Code hooks reference](https://code.claude.com/docs/en/hooks))

| Design assumption | Reality |
|---|---|
| `FileChanged` is a global filesystem watcher | It watches **only** files listed in the `matcher` field |
| `matcher: ".*"` matches all files | The matcher is parsed as `\|`-separated **literal filenames** (e.g., `.env\|.envrc`). `.*` matches a file named literally `.*` — usually nothing. |
| Stdin field: `path` + `change_type` | Stdin fields: `file_path` (absolute) + `event` ("change"/"add"/"unlink") |
| FileChanged can feed a block signal | FileChanged has **no decision control**. It cannot block anything. Exists for side effects (reload `.env`, log, refresh state). |
| Dynamic watching is automatic | Requires explicit `hookSpecificOutput.watchPaths` from CwdChanged or FileChanged hooks. Whether other events (e.g., PostToolUse) can emit watchPaths is **not documented**. |

## Decision: strip FileChanged from v1

- Removed `FileChanged` event registration from `src/superclaude/hooks/hooks.json` + plugins mirror.
- Removed `FileChanged` event from the user's live `~/.claude/settings.json` (backup at `~/.claude/settings.json.bak.filechanged-removal-20260513T010359Z`).
- `freshness-file-changed.sh` script remains in `src/` and is still copied to `~/.claude/hooks/` by `install_hooks` — for v1.5 re-implementation. The script's header now documents the v1 state.
- v1 active event count: **6** (was nominally 7 — FileChanged was always non-functional).

## What still works in v1 (verified live)

- `no_prior_read` blocking — confirmed by a `Write` attempt earlier in the same install session being correctly blocked with telemetry row.
- `read_too_old` blocking — code path independent of FileChanged; relies on `reads.jsonl` + 1800s horizon.
- Session-context envelope (per-turn) — independent.
- Background-agent counter — independent.
- Telemetry log — independent.

## What's missing in v1

- `external_change` block reason will never fire. If a user (or another process) modifies a file between Claude's last Read and the next Edit, the gate will allow the Edit (because the Read is recent enough, and there are no `changes.jsonl` entries).

## v1.5 paths

Two viable redesign approaches identified:

**Approach A: Static per-project watch list.**
- Each project's `.claude/settings.json` declares its watched files explicitly:
  `"matcher": "compose.yml|.env|Cargo.toml|package.json"`.
- Simple, predictable. Limited to declared files.

**Approach B: Dynamic via `watchPaths`.**
- Test whether `PostToolUse(Read)` can emit `hookSpecificOutput.watchPaths` to register the just-Read file for FileChanged watching.
- If supported: the watch list grows automatically as Claude Reads files. This is the design intent we wanted.
- If not supported: fall back to A, or experiment with `CwdChanged` emitting watchPaths seeded from `reads.jsonl`.

Both require fresh probes.

## Probe artifacts

- `probe-deploy.sh`, `probe-revert.sh`: at `.dev/releases/current/freshness-system/artifacts/D-0008/probe/`
- Captured probe payloads: NONE (FileChanged never fired)
- Pre-/post-revert handler hash: real handler bit-identical to source after revert (verified `head -5` shows our production body).
