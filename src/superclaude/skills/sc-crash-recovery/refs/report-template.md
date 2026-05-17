# Recovery Report Template

This is the canonical structure for the synthesis output. The user has seen this format before and parses it quickly. Don't reformat creatively.

A typical project has multiple work initiatives in different states. The report enumerates ALL of them — never collapse to "the active one". Order matters (most-urgent first), but everything detected appears.

## Single-project format

```markdown
# Post-crash recovery — <project name>
_Scan time: <ISO timestamp>, signals window: <since>_

## Snapshot
- Branch: <current branch> (<dirty | clean>)
- Last commit: <hash> — <message> (<relative time>)
- Active sessions found: <N> (last activity: <timestamp>)
- Pipeline artifact bundles detected: <N>
- Tasks in flight (frontmatter not Done): <N>

## Work initiatives — all detected
_Sorted: errored/failed → in-progress → idle but recent. Read top-to-bottom._

### 🔴 <initiative name>  —  <pipeline type>  —  FAILED
**Location:** `<path>`
**Last event:** <timestamp> — <event summary>
**Why it's here:** <one-line diagnosis>

| Step / Phase | Status | Note |
|---|---|---|
| ... | ... | ... |

**Root cause (if identified):** <short explanation tying signals together>

---

### 🟡 <initiative name>  —  <pipeline type>  —  IN PROGRESS
**Location:** `<path>`
**Status:** <frontmatter status / phase N of M>
**Last activity:** <timestamp>
**Next item:** <what to do next, from checklist or state file>

---

### ⚪ <initiative name>  —  <pipeline type>  —  IDLE
**Location:** `<path>`
**Last touched:** <timestamp>
**State:** <brief description>

---

(repeat for every initiative — research bundles, backlog items, tasks in to-do/, etc.)

## Recent Claude sessions
_Last 1-3 sessions for this project. The assistant's last reply often hints at the next step._

### Session 1 — <session file basename> — <timestamp>
**Last user prompt:** "<verbatim, truncated>"
**Last assistant reply:** "<verbatim, truncated>"
**Last tool calls:** Bash(...), Read(...), Edit(...), ...

### Session 2 — ...

## Serena memory highlights
- `<memory-name>.md` (<mtime>) — <one-line summary>
- ...

## Auggie semantic signals
- TODO-WIP / status-InProgress markers found in: `<paths>`
- "Resume here" / "continue tomorrow" notes in: `<paths>`

## Suggested next actions
_Numbered, copy-pasteable. SAFE = idempotent / read-only. REVIEW = changes state._

1. **SAFE** — Inspect the failed sprint phase:
   ```
   cat .dev/releases/current/<release>/phase-6-tasklist.md
   tail -5 .dev/releases/current/<release>/execution-log.jsonl
   ```

2. **REVIEW** — Resume the sprint from the failed phase:
   ```
   superclaude sprint run .dev/releases/current/<release>/tasklist-index.md --resume
   ```

3. **SAFE** — Validate the roadmap output:
   ```
   superclaude roadmap validate docs/generated/<run-slug>
   ```

4. **REVIEW** — Move the completed PRD task out of to-do/:
   ```
   mv .dev/tasks/to-do/TASK-PRD-<ts> .dev/tasks/done/
   ```

(commands sorted by recommended order: diagnose-then-act, lowest-risk-first)

## Conflicts and ambiguities
_Surface anything that doesn't line up — the user decides._

- Task X has `status: 🟢 Done` in frontmatter but `.sprint-exitcode = 1` for its sprint
- Serena memory `current_focus.md` says we're on Y; latest session log shows assistant working on Z
- ...

## What I could not determine
- Whether the haiku-architect step would succeed on retry (no error log present)
- ...
```

## Multi-project (--all) format

Wrap each project in its own section with the structure above. Lead with a fleet-level summary table:

```markdown
# Fleet-wide recovery scan
_<N> projects scanned, signals window: <since>_

## Fleet summary
| Project | Errors | In-progress | Idle | Last activity |
|---|---|---|---|---|
| IronClaude | 1 sprint failed | 2 tasks | 3 research | 2026-05-17T00:50Z |
| tracel3t | 0 | 0 | 1 task | 2026-05-15T... |
| ... | | | | |

_Project ordering: errors first, then in-progress count, then activity recency._

---

## IronClaude
(full single-project format here)

---

## tracel3t
(full single-project format here)

---
...
```

## Tone

- Tables and paths, not paragraphs.
- Verbatim file paths, exit codes, timestamps. Never paraphrase a status.
- Diagnose causation when you can (sprint failed → root cause → recommendation). Don't speculate when you can't.
- Use status markers consistently: 🔴 failed/blocked, 🟡 in-progress, ⚪ idle, 🟢 done.
- The user reads this fresh-off-a-crash. Signal density matters more than friendliness.
