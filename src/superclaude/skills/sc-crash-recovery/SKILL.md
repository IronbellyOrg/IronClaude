---
name: sc-crash-recovery
description: Post-crash work-state recovery. Fans parallel subagents across pipeline artifacts (.dev/releases, manifest.json, execution-log.jsonl, .roadmap-state.json), recent Claude Code session logs, serena memory, git status, and auggie semantic sweeps to produce a structured "where was I, what's in-flight, what to resume" report with concrete resume commands. Use this skill whenever the user mentions a server crash, reboot, machine restart, lost session, dropped pipelines, "where was I", "what was I working on", "what's in flight", "resume", "pick up where I left off", "recover state", or logs back in after an outage — even when they don't explicitly say "crash recovery". Also use after `superclaude sprint`, `superclaude roadmap`, or `/sc:task` pipelines fail or get interrupted, when investigating stalled work, or when starting a fresh session on a project that has unfinished pipeline runs. Supports a single project (default, current cwd) or fleet sweep across all workspaces with `--all`.
allowed-tools: Read, Glob, Grep, Bash(ls *), Bash(find *), Bash(wc *), Bash(cat *), Bash(head *), Bash(tail *), Bash(stat *), Bash(git status *), Bash(git diff *), Bash(git log *), Bash(git stash *), Bash(git branch *), Bash(git ls-files *), Bash(/config/.claude/skills/sc-crash-recovery/scripts/*), Bash(/config/workspace/IronClaude/.claude/skills/sc-crash-recovery/scripts/*), Task
metadata:
  type: workflow
---

# Crash Recovery

You are doing forensic triage of a project (or fleet of projects) after a crash, reboot, or session interruption. The user wants one thing: **a clear picture of what was in flight and what to do next**, with concrete resume commands.

The output is read-only diagnosis. The `allowed-tools` field enforces this — no `Edit`, no `Write`, no unrestricted `Bash`. You propose commands; the user runs them.

## The multi-initiative reality

A typical project has **3–7 work initiatives in different states simultaneously** — one sprint mid-run, two PRD tasks in `to-do/`, a recent research bundle, a backlog item, a resurrection contract. The user knows this; they need to see **all of them**, not your guess at "the active one".

Every investigator, and the final synthesis, must enumerate every initiative it finds. Order them by attention-priority (errored → in-progress → idle-but-recent), but never filter. The user picks where to focus; your job is to surface the full inventory accurately. Collapsing to a single "current task" is the most common failure mode — avoid it.

## When the user invokes this skill

Parse the invocation for these arguments (all optional):

- `--all` — sweep every project under `/config/workspace/`. Default is current cwd only.
- `--since <duration>` — limit signals to last N hours/days (e.g. `--since 24h`). Default: last 72 hours of activity.
- `<project-path>` — explicit project path overrides cwd.

If the user is vague ("the server crashed, help me figure out where I was"), default to current cwd, 72-hour window.

### Input validation (STOP conditions)

Before launching any investigation:

- **STOP** if `<project-path>` was supplied but does not resolve to an existing directory. Tell the user the path is invalid and ask them to clarify. Do not fall back to cwd silently — a typo'd path producing a confidently-empty "no in-flight state" report is worse than no report at all.
- **STOP** if `--all` was supplied and `/config/workspace/` contains zero project directories. Report the configuration issue.
- **WARN** (don't stop) if the resolved project path exists but has no `.dev/`, no `.git/`, no `.serena/`, and no recent session logs. Tell the user the project looks untouched; ask whether they want to continue anyway.

## How to work

The skill orchestrates **parallel fan-out** across forensic signals, then synthesizes. Do not investigate sequentially — that wastes tokens and time. Spawn the investigators in **one message with multiple Task tool calls** so they run concurrently.

### Step 1: Resolve scope (sequential, fast)

Determine the target projects.

```bash
# Single project mode (default)
PROJECT="$(pwd)"            # or the path the user supplied
PROJECTS=("$PROJECT")

# Fleet mode (--all)
PROJECTS=$(find /config/workspace -maxdepth 1 -mindepth 1 -type d)
```

If you got `--all`, tell the user how many projects you're sweeping and warn this will fan out a lot of subagents. Confirm before launching if there are more than 6 projects.

### Step 2: Run the bootstrap scan (sequential, fast)

Before fanning out, run `scripts/bootstrap_scan.sh <project>` for each project. This is a cheap shell scan that returns:

- whether `.dev/`, `docs/`, `.serena/`, `.git/` exist
- file counts and most-recent mtimes for known artifact directories
- the path of the most recent Claude Code session log for the cwd
- recent `.roadmap-state.json` / `manifest.json` / `execution-log.jsonl` / `.sprint-exitcode` files

The bootstrap output tells you which investigators to actually spawn — skip ones whose signal source doesn't exist. There's no point fanning out a `serena-memory` agent if `.serena/memories/` is empty.

Show the user a one-line summary per project after bootstrap (e.g. `tracel3t: 3 .dev/releases/current, 1 stalled sprint, 2 recent sessions, dirty git`). This gives them feedback while the heavy fan-out runs.

### Step 3: Fan out parallel investigators (parallel)

For each project that has signal, spawn these investigators in parallel via the Task tool. **All in one message, multiple tool calls in the same turn.** Each gets the project path and a focused brief. The investigators below are described in `refs/investigators.md` — read that file before spawning if you're unfamiliar with the layouts they target.

| Investigator | Skip if | Subagent type |
|---|---|---|
| pipeline-artifacts | no `.dev/releases/` and no `docs/` artifacts | general-purpose |
| claude-sessions | no `~/.claude/projects/<encoded-cwd>/*.jsonl` | general-purpose |
| serena-memory | no `.serena/memories/` | general-purpose |
| git-state | not a git repo | general-purpose |
| auggie-semantic | source tree is empty or trivially small | general-purpose |

Each investigator returns a structured fragment (see `refs/report-template.md`) — not raw logs. The fan-out is where context bloat lives, so the investigator prompts demand short, structured answers.

**Why parallel matters**: a single-project recovery report should land in roughly the time of the slowest investigator (typically `pipeline-artifacts` or `auggie-semantic`), not the sum of all five. Sequential investigation can take 5–10× longer.

### Step 4: Synthesize the report (sequential)

Once all investigators return, merge their fragments into the canonical report (see `refs/report-template.md`). The synthesis is *yours* to do — don't farm it out. You're the one who can see across investigators to spot a cascade failure (e.g. roadmap pipeline failed because the haiku agent silently produced nothing → debate then ran two identical files → flagged as no convergence).

Always end the report with a **"Suggested next actions"** block: numbered, copy-pasteable shell commands. No filler. Mark each as `SAFE` (idempotent, read-only or trivially reversible) or `REVIEW` (changes state, user should read first).

### Step 5: Propose, never execute

This skill is diagnostic. Do not run the resume commands yourself. The output ends with the commands; the user decides what to fire.

If the user follows up with "go ahead, run #2", do it then — but each command goes through normal approval, not implicit consent from invoking the skill.

## Auggie usage

Auggie's `codebase-retrieval` is the primary tool for the `auggie-semantic` investigator, and also useful as a secondary check in `pipeline-artifacts` when manifest data is ambiguous. Specific queries to use:

- *"What files contain in-progress markers (TODO-WIP, FIXME-RECENT, status fields like 🟡 InProgress) modified in the last 72 hours?"*
- *"Where are recovery or resume instructions documented for the sprint, roadmap, or task pipelines?"*
- *"What's the most recently touched feature work, by file mtime and content recency?"*

Do not use auggie as a substitute for reading manifest.json or execution-log.jsonl directly — those are exact, auggie is semantic. Use auggie when you need to find work-status signals scattered across the tree that no manifest will catch.

## Pipeline knowledge

The skill leans on hard-coded knowledge of these pipelines. See `refs/pipelines.md` for exact layouts, state-file locations, and resume commands per pipeline:

- **PRD** — `task-builder` skill, `.dev/tasks/to-do/TASK-PRD-*/`
- **TDD** — `tdd` skill, `.dev/tasks/{to-do,done}/TASK-TDD-*/`, often paired with `research/` subdir
- **Spec / Tech Reference / Tech Research** — `.dev/research/`, `claudedocs/`
- **Roadmap** — `superclaude roadmap run` → `docs/generated/<...>/.roadmap-state.json` or `.dev/research/roadmap-*/`
- **Tasklist** — `superclaude tasklist` → multi-file bundle per release in `.dev/releases/current/<release>/phase-N-tasklist.md` + `tasklist-index.md`
- **Sprint (task execution)** — `superclaude sprint run` → `.dev/releases/current/<release>/manifest.json` + `execution-log.jsonl` + `.sprint-exitcode`
- **Task (MDTM)** — single .md with frontmatter `status: 🟢 Done | 🟡 InProgress | 🔴 Blocked`, lives in `.dev/tasks/{to-do,done}/`

Each pipeline has a canonical *resume* idiom that the synthesis report should surface. The references file documents these — keep it open when generating the "Suggested next actions" block.

## Output style

The synthesis output should match the canonical structure in `refs/report-template.md`. The user has seen this format before and reads it quickly. Don't reformat creatively.

For multi-project (`--all`) runs: one section per project, sorted by "most likely to need attention first" — i.e., projects with `status: error` in execution-log.jsonl, dirty git with no recent commit, or `.sprint-exitcode != 0` rise to the top.

Keep prose minimal. Tables, file paths, exit codes, suggested commands. The user is fresh off a crash; they want signal, not narrative.

## Edge cases (data-level)

- **No artifacts found anywhere**: say so plainly. "No in-flight pipeline state detected. Most recent activity: <last git commit / last session log timestamp>." Don't fabricate work.
- **Conflicting signals** (e.g. task frontmatter says Done but `.sprint-exitcode = 1`): surface the conflict explicitly. Do not pick a side; the user will decide.
- **Stale claude-session logs that reference deleted files**: note the discrepancy — usually means files were cleaned up or moved during recovery.
- **`--all` with one obviously-busted project**: still report on all projects, but lead with the busted one and explain why it's first.
- **Pipeline still running** (a process holding `.sprint-exitcode` open, or recent execution-log entry within the last few minutes): flag explicitly — the user may be inspecting an active run, not a crashed one. Recommend they confirm before resuming.

## Tool-failure fallbacks

When an investigator's tool layer fails, do not silently drop its signal — the user's diagnosis must distinguish "found nothing" from "could not check":

| Failure | Behavior | Fallback |
|---|---|---|
| `bootstrap_scan.sh` exits non-zero or returns malformed JSON | Continue with the investigators that don't depend on it (git-state, claude-sessions); mark pipeline-artifacts and serena-memory as `unscanned: bootstrap_failed` in the final report | Read .dev/releases/current/* directly via Glob+Read as a degraded fallback |
| Auggie MCP unreachable / `codebase-retrieval` returns error | Skip the auggie-semantic investigator; emit `unscanned: auggie_unavailable` in the report; offer the user the option to run a Grep-based fallback for `TODO-WIP`/`status: 🟡` markers | Grep over the tree for the explicit marker strings |
| Task subagent times out or returns empty string | Re-spawn that one investigator once with a tighter prompt (cap output, narrower scope); if still empty, emit `unscanned: subagent_failure` and continue synthesis | None — the report is honest about the gap |
| Wave exit criterion: any investigator that returns neither a structured fragment nor an explicit "no signal" marker | Wait briefly, then treat as `unscanned`. Never let a silent-empty investigator slip through into a synthesis that looks complete | None |

The synthesis report must surface every `unscanned:` marker in a "What I could not determine" section so the user knows which signals are missing vs. genuinely clean.

## What this skill does not do

- It does not run recovery commands. It proposes them.
- It does not modify any files. Pure read-only — enforced by `allowed-tools`.
- It does not make judgment calls about whether to abandon vs. resume work — that's the user's call, informed by your diagnosis.
- It does not replace `/sc:load` (Serena project-context loader). They're complementary: `/sc:load` loads project context into the session; this skill diagnoses outstanding work.
