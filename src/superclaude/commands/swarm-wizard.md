---
name: swarm-wizard
description: "Plain-language interactive guide to the superclaude swarm CLI — interviews a non-expert about what they want reviewed and why, maps the goal to the right lens/transport/flags, generates and validates the run components, proves the pipeline with a safe stub dry-run, then offers to launch the real swarm, monitor it live, and summarize the outcome in plain English. Use whenever someone wants to USE swarm, run a multi-model review, doesn't know which lens/flags to pick, or finds the swarm docs too technical."
category: development
complexity: advanced
mcp-servers: [sequential]
personas: [scribe, devops, analyzer]
argument-hint: "[--goal <text>] [--target <path>] [--output <dir>] [--real] [--detached] [--advanced] [--yes]"
version: "1.0"
---

# /sc:swarm-wizard - Guided Swarm Launcher

## Triggers

Use this command whenever a user wants to *use* the `superclaude swarm` CLI but isn't a swarm
expert. It is the friendly front door to a tool whose own docs are too technical for a layperson.

1. **Direct:** the user runs `/sc:swarm-wizard` (optionally with pre-seed flags).
2. **Intent-based:** the user says things like "I want to run a swarm", "review my code with multiple
   models", "how do I use swarm on this file", "which swarm lens should I pick", or pastes the swarm
   docs and says "I don't understand this".
3. **Programmatic:** another skill invokes the protocol via the Skill tool.

## Required Input

| Input | Required | Notes |
|-------|----------|-------|
| A goal (what to review and why) | Yes — gathered in the interview if absent | `--goal` pre-seeds it; otherwise the wizard asks. |
| A target file/path | Yes — gathered in the interview if absent | `--target` pre-seeds it. Must exist and hold ≥50 non-whitespace bytes. |

**STOP** and ask (do not guess) when: the goal is ambiguous between two lenses, the target is missing or
too small, or the user requests a real-model run (`--real`) but the T2 proxy env contract
(`T2ProxyUrl` / `T2ProxyKey` / `T2Model01`) is not satisfied.

## Usage

```text
/sc:swarm-wizard                                              # fully guided interview
/sc:swarm-wizard --target src/auth.py                         # pre-seed the target, ask the rest
/sc:swarm-wizard --goal "find bugs in my code" --target src/auth.py
/sc:swarm-wizard --real --target src/auth.py                  # intend a real run (still dry-runs first)
/sc:swarm-wizard --advanced                                   # unlock custom-prompt / JobSpec authoring
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--goal <text>` | — | Pre-seed the user's goal so the wizard can skip the first question. |
| `--target <path>` | — | Pre-seed the file/path to review. |
| `--output <dir>` | `.dev/swarm-runs/<lens>-<ts>/` | Where run artifacts land (idempotent; never overwrites). |
| `--real` | off | Signal intent to run against real models. A safe stub dry-run still runs first. |
| `--detached` | off | Prefer a background (tmux) run over a foreground live dashboard. |
| `--advanced` | off | Unlock the custom-lens / hand-authored-JobSpec branch (with trust-boundary warnings). |
| `--yes` | off | Accept sensible defaults and ask only the irreducible questions (power-user mode). |

## Behavioral Flow

This command ONLY parses the pre-seed flags, confirms the working directory holds the `superclaude swarm`
CLI, and hands off to the protocol skill. It contains NO interview logic, NO lens-mapping table, and NO
launch/monitor machinery — those live in the skill so the behavior stays in one place. The skill grounds
itself in the live CLI (`uv run superclaude swarm --help`) and the verified facts-sheet before asking the
user anything, so it never recommends a flag the installed CLI doesn't have.

## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:swarm-wizard-protocol

Pass the following context:

- Any pre-seed flags supplied: `--goal`, `--target`, `--output`, `--real`, `--detached`, `--advanced`, `--yes`.
- The current working directory (the skill verifies the swarm CLI is reachable from here).

Do NOT attempt to run the interview, build components, or launch a swarm using only this command file.
The full behavioral specification — the interview, the goal→lens/transport/flag mapping, component
generation + validation, the mandatory stub dry-run gate, the launch/monitor/summarize waves, and the
error-handling matrix — lives in the protocol skill.

## Boundaries

**Will:** speak plain language and translate every swarm concept (lens, transport, dry-run) for a
non-expert; ground recommendations in the live `--help` surface; always prove the pipeline with a stub
dry-run before any real run; verify the T2 proxy env contract before a real run; ask before launching;
monitor the run it launched and summarize the outcome plus the recommended next step.

**Will Not:** launch a real-model run without an explicit user go-ahead and a passing dry-run; invent T2
proxy endpoints or model names (uses only `~/.aienv`); promise a live `--tui` dashboard on a non-TTY
stream; combine mutually-exclusive flags (e.g. `--tui`+`--detached`); overwrite an existing run's
artifacts; expose raw rule codes / tracebacks to the user without a plain-language explanation.

## Related Commands

- `/sc:adversarial`, `/sc:troubleshoot`, `/sc:code-review`, `/sc:document`, `/sc:reflect`, `/sc:research`
  — the downstream skills a finished swarm run hands off to (the wizard surfaces the right one per lens).
- `/sc:pr-submit`, `/sc:auggie-review` — sibling review workflows for the PR path.
