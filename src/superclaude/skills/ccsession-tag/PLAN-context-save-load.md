---
title: ccsession context save/load via Serena memories
date: 2026-05-20
status: pre-build
---

# Plan: ccsession context save + load

## Goal

Add session-context persistence and resume-with-context to the ccsession
skill, using Serena as the storage layer.

- **Save:** one slash command (`/sc:save --all`) fans out subagents to read
  each labeled session's JSONL and write/update one Serena memory per label.
  Per-session save also supported via `/sc:save --session <name>`.
- **Tag-and-save combo:** `/ccsession-tag <name>` is extended to tag the
  session AND immediately fire `/sc:save --session <name>` so every newly
  tagged session has an initial memory file.
- **Resume with context:** new flag `ccsession <name> --load-context` resumes
  the JSONL AND injects the saved memory via the existing SessionStart hook.
- **Manual load by name:** `/sc:load --session <name>` deterministically
  loads the `ccsession-<name>` memory file via Serena.
- **Visibility:** `ccsession --list` shows saved / unsaved / stale status per
  label.

## Non-goals

- We are NOT building a new skill folder. We're extending the existing
  `/sc:save`, `/sc:load`, `/ccsession-tag` skills, plus the existing
  ccsession wrapper + hook.
- We are NOT auto-saving via a Stop hook. Saves are explicit (manual
  `/sc:save --all` invocation, single-session `/sc:save --session`, or the
  auto-save triggered by `/ccsession-tag`).
- We are NOT auto-loading on every resume. Loading is opt-in via
  `--load-context` (shell) or `/sc:load --session <name>` (in-session).

## Architecture overview

```
                    ┌─────────────────────────────────┐
  /sc:save --all  ──▶│  orchestrator (live LLM)        │
                     │  - lists labeled sessions       │
                     │  - dispatches Task subagents    │
                     │    (max 10 concurrent)          │
                     └─────────────────────────────────┘
                                  │
                                  ▼ (1 agent per labeled session)
                     ┌─────────────────────────────────┐
                     │  subagent                       │
                     │  - reads JSONL at given path    │
                     │  - creates/updates memory file  │
                     │    incrementally                │
                     │  - enforces 500-line cap        │
                     │  - skips if JSONL didn't grow   │
                     │  - calls Serena write_memory    │
                     └─────────────────────────────────┘
                                  │
                                  ▼
                  <workspace>/.serena/memories/
                       ccsession-<name>.md

  ──── load side ────

  ccsession brownfield --load-context
        │
        ▼ (wrapper sets env var, exec claude --resume)
  ┌──────────────────────────────────────┐
  │ SessionStart hook (existing)         │
  │  - if $CCSESSION_LOAD_TOPIC set:     │
  │    - resolve workspace via .cwd      │
  │    - read ccsession-<name>.md       │
  │    - emit additionalContext JSON     │
  └──────────────────────────────────────┘
        │
        ▼
  Claude's resumed session gets the saved
  memory as a system reminder in turn 1.
```

## Files touched

### 1. `/sc:save.md` (both user-level and repo copies)

**Paths:**
- `~/.claude/commands/sc/save.md` — verify presence at user level before editing.
- `.claude/commands/sc/save.md` — in this repo, already present.

**Changes:**
- Add `--all` flag handling: orchestrator behavior
- Add `--session <name>` flag handling: deterministic naming for current
  session
- Existing behavior (`/sc:save` no args) unchanged

**New invocations:**
- `/sc:save` — unchanged, in-context save with Serena's `think_about_*` and
  `write_memory`
- `/sc:save --session <name>` — save current session as
  `ccsession-<name>` (deterministic name, replaces any prior)
- `/sc:save --all` — fan out: list labeled sessions, dispatch up to 10
  concurrent Task subagents, each handles one label

### 1b. `/sc:load.md` (both user-level and repo copies)

**Paths:**
- `~/.claude/commands/sc/load.md`
- `.claude/commands/sc/load.md`

**Changes:**
- Add `--session <name>` flag handling.
- When passed: activate Serena project on the current workspace, then call
  `mcp__serena__read_memory(name="ccsession-<name>")`, return its content as
  loaded context.
- Existing behavior (`/sc:load` no args, `/sc:load <path>`, `/sc:load --type
  ...`) unchanged.

### 1c. `~/.claude/skills/ccsession-tag/SKILL.md` (both user + repo copies)

**Changes:**
- Existing behavior (write topic file + .cwd) unchanged.
- Add a follow-on step: after the tag bash completes, perform `/sc:save
  --session <name>` operations inline. Concretely the .md instructs Claude
  to:
  1. Run the existing tag bash
  2. Then summarize the current session and call
     `mcp__serena__write_memory(name="ccsession-<name>", content=<summary>)`
     so that an initial memory file exists immediately after tagging.
- The save step on initial tag follows the same memory format and 500-line
  cap as `/sc:save --session`.

### 2. `~/.claude/skills/ccsession-tag/ccsession` (the wrapper)

Also synced to the repo copy at
`.claude/skills/ccsession-tag/ccsession`.

**Changes:**
- Add `--load-context` (or `-l`) flag
- When set: `export CCSESSION_LOAD_TOPIC="$TOPIC"` before `exec claude
  --resume`
- Update `--help` text to document the new flag

### 3. `~/.claude/skills/ccsession-tag/hooks/session-start.sh`

Also synced to the repo copy.

**Changes:**
- Add a new branch at the end: if `$CCSESSION_LOAD_TOPIC` is set:
  - Resolve workspace path via `~/.claude/projects/<slug>/topics/.cwd`
  - Build memory file path: `<workspace>/.serena/memories/ccsession-<topic>.md`
  - If file exists, emit JSON to stdout:
    `{"additionalContext": "## Saved memory for ccsession-<topic>\n\n<file
    contents>"}`
  - Use `python3` for JSON encoding (no new deps; python3 already used)
  - If file doesn't exist, silently exit (no error, no noise)

### 4. `~/.claude/skills/ccsession-tag/ccsession` (the wrapper) — list output

**Changes:**
- `list_sessions` function gets a new column showing memory state per label
- Resolve memory path via `.cwd` cache → `<workspace>/.serena/memories/ccsession-<name>.md`
- Compare memory's recorded `last_save_bytes` (in frontmatter) vs current JSONL
  size
- Display:
  - `[saved YYYY-MM-DD HH:MM]` if memory exists and `last_save_bytes` matches
    current JSONL size (or close enough)
  - `[stale]` if memory exists but JSONL has grown beyond it
  - `[unsaved]` if memory doesn't exist

### 5. `~/.claude/skills/ccsession-tag/README.md`

Also synced to repo.

**Changes:**
- Document `--load-context` flag
- Document `/sc:save --all`, `/sc:save --session <name>`, `/sc:load --session <name>`, the `/ccsession-tag` tag+save combo, and `--load-context`
- Document memory file location and frontmatter format

## Detailed designs

### Memory file format

```markdown
---
ccsession_label: brownfield
workspace: /Users/cmerritt/GFxAI/GFxAI-with-RigorFlow
jsonl_uuid: 50c2925c-824c-42a8-85d3-65916067518a
last_save_bytes: 18234567
last_save_at: 2026-05-20T10:00:00Z
line_count: 487
---

# brownfield — Session Memory

## Goal
<one paragraph: what this conversation is for>

## Key Decisions
- <decision>: <rationale>
- ...

## Files Touched
- `path/to/file` — <what changed>
- ...

## Significant Tool Actions
- <action>: <outcome>
- ...

## Open Questions / Blockers
- ...

## Current State / Next Steps
- ...
```

The agent enforces ≤500 total lines including frontmatter.

### `/sc:save --all` orchestrator behavior

Pseudocode (executed by the live LLM in the session where `/sc:save --all`
was invoked):

```
1. Find all labeled sessions across all workspaces:
   for ws_dir in ~/.claude/projects/*/topics/:
     read .cwd to get real workspace path
     for label_file in *.txt:
       label = basename(label_file, .txt)
       session_uuid = contents of label_file
       jsonl_path = ws_dir/../<uuid>.jsonl
       record (workspace, label, jsonl_path)

2. Skip filtering:
   for each (workspace, label, jsonl_path):
     memory_path = workspace/.serena/memories/ccsession-<name>.md
     if memory_path exists:
       read frontmatter, get last_save_bytes
       current_size = stat jsonl_path
       if current_size <= last_save_bytes:
         mark as SKIP (no growth)

3. Dispatch in batches of 10:
   for each non-skipped (workspace, label, jsonl_path):
     spawn Task subagent with the AGENT PROMPT (below)
     pass: workspace, label, jsonl_path, memory_path,
           mode = CREATE | UPDATE

4. Wait for all to complete, collect results.

5. Report:
   "Saved: <list>
    Updated: <list>
    Skipped (no growth): <list>
    Failed: <list with error>"
```

### Agent prompt (the literal text sent to each subagent)

```
You are saving a Claude Code conversation's context to a Serena memory file.

INPUTS:
- workspace_path: <WORKSPACE>
- label: <LABEL>
- jsonl_path: <JSONL>
- memory_path: <MEMORY>
- mode: CREATE | UPDATE
- previous_bytes: <BYTES>   (UPDATE only — bytes already summarized)

TASK:
Produce or update a structured memory file that helps a user (or a future
Claude session) recall this conversation's state quickly.

STEPS:

1. Activate the project in Serena:
   call mcp__serena__activate_project(path="<WORKSPACE>")

2. Initialize the memory file structure (CREATE mode) or read existing
   structure (UPDATE mode):
   - If CREATE: call mcp__serena__write_memory with the empty skeleton
     (frontmatter + section headers, no content yet).
   - If UPDATE: call mcp__serena__read_memory to load existing content,
     parse out section bodies.

3. Read the JSONL in chunks:
   - CREATE mode: read entire file
   - UPDATE mode: skip the first <previous_bytes> bytes, then read the rest
   - Read in chunks of ~50k tokens at most per Read call to avoid blowing
     context
   - The JSONL is line-delimited JSON. Each line is one of:
     - {"type": "user", ...}
     - {"type": "assistant", ...}
     - {"type": "tool_use", ...}
     - {"type": "tool_result", ...}
     - {"type": "system", ...}
   - Extract meaningful state changes: decisions, files touched (look for
     Edit/Write tool calls), key tool actions (find_symbol results,
     command outputs), errors hit, plans made

4. After each chunk, update the memory file:
   - CREATE: append new findings into the appropriate sections via
     mcp__serena__edit_memory or rewrite via write_memory
   - UPDATE: merge new findings into existing sections, preserving prior
     content where still relevant

5. Enforce the 500-line cap on the final file (including frontmatter).
   If approaching the cap while still adding content, prune lower-value
   content:
   - Resolved "next steps" can be summarized into one line
   - Redundant decisions can be consolidated
   - Older "files touched" can be aggregated by directory
   - NEVER drop the frontmatter, the Goal, or the Current State sections

6. Final step: update frontmatter with:
   - last_save_bytes: <current JSONL byte size>
   - last_save_at: <current ISO timestamp>
   - line_count: <total lines in file>

7. Report completion: "Saved memory for <label> at <memory_path> (<lines> lines)"

CONSTRAINTS:
- Do NOT write the entire JSONL content verbatim — this is a recall aid,
  not a transcript dump
- Do NOT exceed 500 total lines including frontmatter
- Do NOT modify files outside the memory_path
- Use mcp__serena__write_memory and mcp__serena__edit_memory (not direct
  Write tool) so Serena's project scoping is respected
```

### Hook update — full new branch

```bash
# At end of session-start.sh, before the final exit 0:

# Auto-inject saved memory if --load-context was requested via wrapper.
if [ -n "$CCSESSION_LOAD_TOPIC" ]; then
  WS_SLUG=$(echo "$CWD" | sed 's|/|-|g')
  TOPIC_DIR="$HOME/.claude/projects/$WS_SLUG/topics"
  CWD_FILE="$TOPIC_DIR/.cwd"

  if [ -f "$CWD_FILE" ]; then
    WORKSPACE=$(cat "$CWD_FILE")
    MEMORY="$WORKSPACE/.serena/memories/ccsession-$CCSESSION_LOAD_TOPIC.md"

    if [ -f "$MEMORY" ]; then
      python3 -c "
import json, sys
with open('$MEMORY') as f:
    content = f.read()
print(json.dumps({
    'additionalContext':
    '## Saved memory for ccsession-$CCSESSION_LOAD_TOPIC\n\n' + content
}))
" 2>/dev/null
      exit 0
    fi
  fi
fi
```

## Acceptance criteria

1. `/sc:save --session brownfield` in the brownfield session creates
   `<workspace>/.serena/memories/ccsession-brownfield.md` with structured
   content and valid frontmatter.
2. `/sc:save --all` from any session dispatches one subagent per labeled
   session across all workspaces, ≤10 concurrent, skips sessions whose JSONL
   hasn't grown, and reports a summary.
3. `/ccsession-tag brownfield` writes the topic file AND immediately creates
   `ccsession-brownfield.md` memory with the current session's summary.
4. `/sc:load --session brownfield` reads
   `<workspace>/.serena/memories/ccsession-brownfield.md` and brings its
   content into the live session's context.
5. `ccsession brownfield --load-context` resumes the JSONL AND the resumed
   session's first turn includes the memory file content as a system
   reminder.
6. `ccsession brownfield` (without `--load-context`) resumes the JSONL
   only — no memory injected.
7. `ccsession --list` shows `[saved YYYY-MM-DD HH:MM]`, `[stale]`, or
   `[unsaved]` for each label.
8. All memory files stay ≤500 lines.
9. Re-running `/sc:save --all` immediately after a previous run skips every
   session as "no growth."
10. Build does not introduce new dependencies — uses bash + python3 +
    claude CLI + already-installed MCP servers.

## Open questions / decisions to confirm

1. **`--session <name>` for in-context single-session save** — confirmed
   needed (the new /ccsession-tag combo also exercises this code path).

2. **Stale threshold** — exact match of `last_save_bytes == current_size`,
   or allow some delta (e.g., grew by <1kb = still fresh)? Strict match is
   simplest; ambiguity-prone for edge cases like Claude appending its own
   bookkeeping line. I'd default to "stale if current_size > last_save_bytes
   by ANY amount" and let `--all` skip when equal. Confirm.

3. **CREATE mode incremental writes** — does Serena's `edit_memory` support
   appending efficiently, or does each call rewrite the whole file? If
   rewrite, "incremental" is just illusion. May not matter for correctness;
   does matter for performance on long sessions.

4. **Concurrent agent dispatch** — Task tool's actual parallelism limits
   need to be verified. The "10 concurrent" assumption rests on Task being
   able to fan out cleanly. If it can't, we serialize with a TODO list.

5. **`ccsession --list` shows memory state** — workspace must still exist on
   disk for the `.cwd` resolution to work. If a workspace was deleted but
   labels still exist in `~/.claude/projects/`, listing shows `[workspace
   missing]`. Acceptable?

## Build order

1. Update `/sc:save.md` (user + repo) with `--session` and `--all`
   orchestrator
2. Update `/sc:load.md` (user + repo) with `--session` flag
3. Update `/ccsession-tag/SKILL.md` (user + repo) to chain into
   `/sc:save --session <name>` after tagging
4. Update wrapper (`ccsession`) — add `--load-context` flag + memory status
   in `--list`
5. Update hook (`session-start.sh`) — add `$CCSESSION_LOAD_TOPIC` branch
6. Update README
7. Smoke test:
   - `/ccsession-tag test1` → verify tag file AND memory file both created
   - `/sc:load --session test1` → verify memory content loads into session
   - `ccsession test1 --load-context` → verify hook injects memory on resume
   - `/sc:save --all` → verify all labels get saved
   - `ccsession --list` → verify status column
   - `ccsession --rm test1` + manual memory file delete → cleanup

## Out of scope (deliberately)

- Stop hooks (manual save only)
- Auto-load on every resume (must use --load-context)
- Cron / scheduled saves
- Cross-workspace memory sharing
- Memory file versioning / history
- Hooking into compaction events (PreCompact)
