# Context Freshness Hooks

A set of seven active shell hooks distributed by `superclaude install` that
protect against the **stale-fact-reuse failure mode** — citing a file line
number, IP, hostname, or other source-tied fact from working memory after the
underlying file has been modified. Installation also deploys the global Bash
inspection batching policy used by main sessions, subagents, and tasklists.

## What gets installed

After `superclaude install --force`:

| Path | Purpose |
|---|---|
| `~/.claude/hooks/session-init.sh` | Pre-existing init script (path-fixed in this release). |
| `~/.claude/hooks/freshness-session-start.sh` | Emits a `<session-context>` envelope on startup or `--resume`. On resume, includes recent commits, git status, memory index, and `resumed_after=` field. |
| `~/.claude/hooks/freshness-user-prompt.sh` | Per-turn envelope: `turn=`, `Δ=`, `git=dirty=…`, `bg=`. Conditional rendering (NFR-8) — minimal envelope when nothing fires. |
| `~/.claude/hooks/freshness-pre-edit.sh` | **The gate.** Blocks `Edit` / `Write` / `mcp__serena__replace_*` / `mcp__serena__insert_*_symbol` calls against files not Read in the last 30 minutes. Exits `2` with a factual stderr message; the assistant retries by Reading then re-attempting. |
| `~/.claude/hooks/freshness-post-read.sh` | Async tracker. Appends every successful `Read` to `~/.claude/state/reads.jsonl`. |
| `~/.claude/hooks/freshness-subagent-start.sh` | Synchronous SubagentStart hook: increments the background-agent counter and injects `BASH_INSPECTION_POLICY.md` before the agent's first action. Fails open if policy injection is unavailable. |
| `~/.claude/hooks/freshness-subagent-stop.sh` | Async background-agent counter decrement feeding `bg=N` in the per-turn envelope. |
| `~/.claude/BASH_INSPECTION_POLICY.md` | Global behavioral policy: five or more known, independent serial Bash inspections become one bounded `/tmp` batch call. Imported by `~/.claude/CLAUDE.md`; no hard Bash counter is installed. |
| `~/.claude/hooks/freshness-file-changed.sh` | **NOT registered in v1.** Script is copied to disk but the design's `FileChanged` registration was removed after live probing revealed Claude Code's matcher only accepts literal filenames, not regex. See "Known limitations" below. |

State files appear under `~/.claude/state/`:

```
~/.claude/state/
├── reads.jsonl           # every successful Read
├── changes.jsonl         # FileChanged events for files we Read
├── turns/<session>.txt
├── last-prompt-ts/<session>.txt
├── bg-agents/<session>.txt
└── tool-call-counter/<session>.txt
```

Telemetry appears at `~/.claude/logs/freshness-hook.jsonl` (one row per gate
decision; `decision` ∈ `allow`/`block`; `reason` ∈ `recent_read` / `no_prior_read` /
`read_too_old` / `external_change` / `create_allowed`).

## Behavioral changes you'll see

1. The first Edit against a file in a fresh session will be blocked with a
   message like:
   > `You have not Read \`/path/to/file.go\` in this session. Read it before editing.`
   The assistant Reads, then the next Edit attempt succeeds.

2. Resuming a session after >30 minutes inactivity will block any Edit until
   the file is re-Read:
   > `You last Read \`/path/to/file.go\` 4500s ago, beyond the 30-minute freshness horizon. Re-Read before editing.`

3. ~~If you (or another process) modifies a file between the assistant's Read and Edit, the Edit is blocked.~~ **Not active in v1** — see Known limitations.

4. Every user prompt is preceded (internally) by a `<session-context>` block
   with current turn number and conditional state. The assistant treats this
   as ground truth for the turn.

5. Main sessions load the Bash inspection policy through global `CLAUDE.md`.
   Subagents receive the same canonical text synchronously at SubagentStart.
   The policy is advisory execution guidance, not a permission or security
   gate; adaptive diagnostics and mutations remain individual calls.

## Known limitations (v1)

### No external-modification detection

The original design (`phase5.1-context-refresh-design.md` §3.5) called for a
`FileChanged` hook to detect when a file on disk is modified between Claude's
last Read and the next Edit — populating an `external_change` block reason in
the gate.

**Live probing during T05.01 revealed:**

- Claude Code's `FileChanged` matcher accepts only `|`-separated **literal
  filenames** in the working directory — not regex, not globs, not `*` as
  "match all". Our design used `matcher: ".*"` which silently watched a file
  literally named `.*` (which doesn't exist).
- `FileChanged` hooks have **no decision control** (cannot block anything);
  they exist for reactive side effects like reloading `.env`.
- Dynamic watch updates are possible via `hookSpecificOutput.watchPaths`, but
  the official examples only show this returned from `CwdChanged` and
  `FileChanged` events themselves.

**v1 decision:** strip the FileChanged registration. The gate still blocks
the two most common stale-fact paths — `no_prior_read` (Claude never opened
this file in the session) and `read_too_old` (last Read >30 min ago). The
external-edit-between-Read-and-Edit scenario is not caught in v1.

**v1.5 work item:** redesign the FileChanged piece — either pre-register
specific watched filenames per project, or test whether `watchPaths` output
is accepted from `PostToolUse(Read)` (which would let us watch every file
Claude has Read). Both approaches need a fresh probe to verify.

### ~~`Write` to nonexistent files is blocked~~ — resolved

**Resolved.** `freshness-pre-edit.sh` now allows `Write` against paths that do
not exist on disk via a new `create_allowed` branch (Proposal A from
`freshness-hook-fix-debate.md`). Telemetry emits `reason=create_allowed`. The
existing-file gate is unchanged — `Edit` or `Write` against an existing-but-unread
file still blocks with `no_prior_read`. Regression guard:
`tests/cli/test_install_hooks.py::test_real_hooks_json_gates_write_in_pre_tool_use`
pins the matcher so a future config change cannot silently drop `Write`.

## How to opt out

To disable selectively, remove the relevant entries from `~/.claude/settings.json`
under the `hooks` key. Each event (`SessionStart`, `UserPromptSubmit`, `PreToolUse`,
etc.) is independent.

To disable globally:

1. Backup: `cp ~/.claude/settings.json ~/.claude/settings.json.before-disable`
2. Edit `~/.claude/settings.json` and delete the 7 freshness entries (leave any
   `session-init.sh` or unrelated user hooks intact).
3. Optionally delete the scripts: `rm ~/.claude/hooks/freshness-*.sh`.

To re-enable later: `superclaude install -f`.

## FAQ

**Q: Why am I seeing `bash: jq: command not found` errors after install?**

The hooks require `jq` (already a SuperClaude build dependency). On systems
that don't have it: `sudo apt install jq` / `brew install jq`. Without `jq`,
hooks fail-open per NFR-3 — your session keeps working but freshness
enforcement is disabled.

**Q: Will repo-local hooks (`.claude/settings.json` in a project) work?**

No — the freshness system is user-scope only (per NFR-12). Claude Code's
`--add-dir` flag does not load repo-local hooks; they're silently bypassed.
Install once to `~/.claude/settings.json` and the protection applies across
all your projects.

**Q: What about long-running sessions where the 30-minute horizon is too tight?**

The 30-minute (1800s) window is a v1 default per design DQ-3. After ≥1 week
of telemetry under your real usage, tune `FRESH_HORIZON` in
`~/.claude/hooks/freshness-pre-edit.sh` if your usage pattern justifies a
different window. The telemetry log
(`~/.claude/logs/freshness-hook.jsonl`) is designed for this.

**Q: How do I check the system is actually firing?**

```bash
tail -F ~/.claude/logs/freshness-hook.jsonl
```

Then issue an `Edit` against a file you haven't Read this session. You should
see a `decision=block, reason=no_prior_read` row.

**Q: My settings.json got corrupted — what now?**

`install_hooks.py` backs up `~/.claude/settings.json` to
`~/.claude/settings.json.bak.<ISO-8601>` before every write and refuses to
overwrite an already-malformed target. To restore:

```bash
ls -t ~/.claude/settings.json.bak.* | head -1 | xargs -I{} cp {} ~/.claude/settings.json
```

## Design references

- Source design: `phase5.1-context-refresh-design.md` (InfraDocs)
- Token-budget envelope analysis: `phase5.1-token-budget-check.md`
- Implementation tasklist: `.dev/releases/current/freshness-system/`
