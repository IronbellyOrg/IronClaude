# Investigator Briefs

Each investigator is a parallel subagent spawned by the `crash-recovery` skill. They return structured fragments that synthesis merges into the final report. Each brief below is what you pass to `Task` as the `prompt`. Use `subagent_type: general-purpose` unless otherwise noted.

**Universal rule:** every investigator must enumerate ALL initiatives it finds, not pick "the most important one". Multiple work streams in flight is the norm, not an edge case. The synthesis step decides ordering; investigators report breadth.

---

## 1. pipeline-artifacts

**Goal:** report every in-flight or recently-failed pipeline run, with status and last event.

**Prompt skeleton:**

```
You are investigating pipeline artifacts in <PROJECT_PATH>. The user just survived a server crash and needs to know what was in flight.

Scan ALL of these locations and report on every artifact bundle (do not collapse to one):
- .dev/releases/current/*/ — sprint runs (look for manifest.json, execution-log.jsonl, .sprint-exitcode, tasklist-index.md, phase-*.md)
- .dev/releases/backlog/ and .dev/releases/complete/ — only check mtimes; flag anything modified in last 72h
- .dev/tasks/to-do/*/ and .dev/tasks/to-do/*.md — MDTM tasks; read frontmatter `status:` field
- .dev/tasks/done/ — only check most recent (last 5 by mtime); these should be settled but flag if frontmatter says InProgress
- .dev/research/*/ — research bundles
- docs/generated/*/ and any *.roadmap-state.json found in tree — roadmap runs
- .dev/resurrection-contracts/ — explicit recovery contracts

For each artifact bundle, return:
- name and full path
- pipeline type (sprint | roadmap | task | research | resurrection-contract | other)
- status (pass | fail | in-progress | unknown) with evidence (exit code, last log event, frontmatter field)
- last activity timestamp
- next-step hint (e.g. "phase 6 failed, see phase-6-tasklist.md")

For sprints: tail execution-log.jsonl and report the last phase_complete event verbatim.
For roadmaps: read .roadmap-state.json and report per-step status.
For tasks: report frontmatter `status:` and count of checked vs unchecked checklist items.

Return as a markdown table grouped by pipeline type. Be terse — paths, statuses, timestamps. No prose.

If you find more than 10 artifact bundles, return all of them anyway. The user wants completeness.
```

**Estimated time:** 30–90s depending on tree size.

---

## 2. claude-sessions

**Goal:** surface the last 1–3 Claude Code sessions for the project's cwd, with the user's last few prompts and the assistant's last few replies, so the user (and the synthesis) can see what was on-screen when the crash hit.

**Prompt skeleton:**

```
You are extracting the last working state from Claude Code session logs for project <PROJECT_PATH>.

Session log directory: <SESSION_LOG_DIR>
Most recent session files (already identified): <up to 3 paths>

For each of the top 3 most recent sessions (by mtime):
1. Run scripts/parse_session_log.py <session-file> --turns 8 to get the last 8 conversational turns
2. From those turns, extract:
   - the last user prompt (verbatim, truncated to ~300 chars)
   - the last 1-2 assistant text replies (verbatim, truncated to ~600 chars each)
   - the names of the last 5 tool calls used (just the tool names + brief input summary, not full payloads)
   - the timestamp of the last event

The point is to reconstruct "what was the user asking, what was the assistant doing, when did it stop". Multiple sessions because the user may have had multiple instances running at crash time.

Return as markdown with one subsection per session. Lead each subsection with the session file path and timestamp. DO NOT dump the raw JSONL or speculate about content you didn't read.
```

**Estimated time:** 15–30s. The parse script handles the heavy lifting.

---

## 3. serena-memory

**Goal:** surface project memory entries that record current state, working hypotheses, or recently-discovered context.

**Prompt skeleton:**

```
You are reading serena memory files for project <PROJECT_PATH>.

Location: <PROJECT_PATH>/.serena/memories/

For each .md file in that directory:
- Read the file
- Capture: filename, top-level heading, and any sections that mention current/in-progress/recent/blocked work
- Note the file's mtime

Prioritize memory files whose name or content suggests live state (e.g. "current_*", "in_progress_*", "session_*", "recent_*", "blockers", "next_steps", "todo"). Less-relevant memories (style guides, long-lived patterns) can be listed by name only.

Return as a markdown list. For each relevant memory: filename, mtime, 2-3 sentence summary of what it tells us about current work state. For non-relevant memories: just the filename.
```

**Estimated time:** 10–30s.

---

## 4. git-state

**Goal:** report uncommitted changes that represent literal in-flight work.

**Prompt skeleton:**

```
You are inspecting git state for project <PROJECT_PATH>. The user just survived a crash and unstaged changes likely represent the work they had in progress.

Run these commands (read-only, no modifications):
- git -C <PROJECT_PATH> status --short
- git -C <PROJECT_PATH> diff --stat
- git -C <PROJECT_PATH> diff --stat --staged
- git -C <PROJECT_PATH> log -10 --oneline
- git -C <PROJECT_PATH> stash list
- git -C <PROJECT_PATH> branch --show-current

Return:
- current branch
- last 5 commits (oneline)
- summary of dirty files (count + the most "interesting" 5–10 paths — prefer files in src/, .dev/tasks/, docs/, configs)
- any stashes
- whether the working tree looks like "mid-edit" (many small unstaged diffs across diverse files) or "single-feature" (concentrated in one subtree)

Be brief. Tables and paths, not prose. Do NOT run any write commands.
```

**Estimated time:** 5–15s.

---

## 5. auggie-semantic

**Goal:** catch work-in-progress signals that the structured scans miss — TODO markers, status fields in docs, half-written sections, comments that say "will continue tomorrow", etc.

**Prompt skeleton:**

```
You are doing a semantic sweep of project <PROJECT_PATH> using the auggie codebase-retrieval MCP tool. The user just survived a crash and wants to find any in-progress work that structured scans (manifest.json, frontmatter) might miss.

Run the following codebase-retrieval queries IN PARALLEL where possible:

1. "Files containing in-progress markers (TODO-WIP, FIXME-RECENT, XXX-RESUME, status: 🟡 InProgress, draft, WIP) that have been recently modified."
2. "Notes or comments that say things like 'will continue', 'next step', 'left off', 'TODO next session', 'resume here', 'pause point'."
3. "Recently modified source files (last 72 hours) whose changes look incomplete — empty function bodies, NotImplementedError, pass statements with comments, half-written imports."
4. "Documents (.md files) with frontmatter status field set to anything other than Done — InProgress, Draft, Blocked, Review, etc."

For each query, return the top 5 file paths plus a 1-line excerpt showing the matching signal. Group results under the four query headings.

Skip queries that return nothing. Be terse — paths, excerpts. No prose.
```

**Estimated time:** 30–90s depending on auggie response time.

---

## Spawning pattern

In one message, emit all needed Task tool calls. Example:

```
[Task: pipeline-artifacts for tracel3t]
[Task: claude-sessions for tracel3t]
[Task: serena-memory for tracel3t]
[Task: git-state for tracel3t]
[Task: auggie-semantic for tracel3t]
```

Skip any whose signal source the bootstrap scan reported as absent.

For `--all` mode, spawn the bundle once per project. With 10 projects that's 50 subagents; consider sequencing in waves of 3 projects at a time to avoid runaway parallelism.
