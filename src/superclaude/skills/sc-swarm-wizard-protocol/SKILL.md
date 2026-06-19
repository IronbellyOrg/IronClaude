---
name: sc:swarm-wizard-protocol
description: "Behavioral protocol for /sc:swarm-wizard — the plain-language interactive guide to the superclaude swarm CLI. Interviews a non-expert about what they want reviewed and why, maps the goal to the correct lens/transport/flags from the live CLI surface, generates and validates the run components, proves the pipeline with a mandatory stub dry-run, then offers to launch the real swarm, monitors it, and summarizes the outcome plus the recommended next step in plain English. Use this skill whenever a user wants to run swarm, run a multi-model review, doesn't know which swarm lens or flags to pick, or finds the swarm documentation too technical to act on."
category: development
complexity: advanced
mcp-servers: [sequential]
personas: [scribe, devops, analyzer]
allowed-tools: Read, Grep, Glob, Write, AskUserQuestion, TodoWrite, Task, Monitor, Bash(uv run superclaude swarm *), Bash(ls *), Bash(wc *), Bash(test *), Bash(mkdir *)
argument-hint: "[--goal <text>] [--target <path>] [--output <dir>] [--real] [--detached] [--advanced] [--yes]"
---

# Swarm Wizard Protocol

## Purpose

Make the `superclaude swarm` CLI usable by someone who has never read its docs. The swarm tool is
powerful — it fans one prompt across several independent model "reviewers" and amalgamates their findings —
but its surface is dense with jargon (lenses, recipes, transports, Waves, IMM-4, INV-007) that stops a
non-expert from getting value. This skill is the translator and the driver: it **asks plain-language
questions**, **decides the technical settings on the user's behalf**, **proves the run works with a safe
practice run**, and then **launches, watches, and explains** the real run.

**What it does NOT do:** it does not replace the swarm CLI, re-implement review logic, or run real
models without an explicit go-ahead and a passing dry-run. It does not invent proxy endpoints or model
names. It is a guide, not a new engine.

**Why a wizard at all:** the cost of a wrong swarm invocation is a confusing failure (a rule code on
stderr, an empty output dir, or a hung monitor). Every gate in this protocol exists to convert one of
those failure modes into a plain-language question *before* it bites the user.

## Ground truth (read this first, every run)

The swarm CLI evolves and its shipped docs are partly stale. **Never reason from memory or from
`docs/swarm/`.** Two sources are authoritative, in this order:

1. The **live CLI**: `uv run superclaude swarm --help` and `uv run superclaude swarm run --help`.
2. The **verified facts-sheet**: `refs/cli-contract.md` in this skill (distilled + empirically confirmed),
   which also lists the specific doc claims that are STALE (e.g. `--tui` is real; the `--lens` default
   transport is `stub`; fresh runs DO emit `return-contract.yaml`).

If the live `--help` and the ref ever disagree, the live CLI wins and you tell the user the ref looks out
of date.

## Input Contract

### Required (STOP if missing — ask, do not guess)

- **Goal** — what the user wants to learn and why. Drives the lens choice. If absent and not derivable
  from `--goal`, ask Q1 from `refs/interview.md`.
- **Target** — the file or path to review. Must exist and contain **≥50 non-whitespace bytes** (the
  CLI's IMM-4 floor). If absent, ask Q2. If present but too small, STOP and explain.

### Optional (sensible defaults; confirm once)

- Transport intent (`--real`), watch mode (`--detached`), advanced branch (`--advanced`), output dir
  (`--output`), reviewer count, label. Defaults live in `refs/cli-contract.md`.

### WARN (proceed with a heads-up)

- `--real` requested but the T2 proxy env contract is unsatisfied → WARN and fall back to offering a
  stub run, or walk the user through `~/.aienv` setup. Never fabricate proxy values.

## Protocol

Track progress with Todo(s). The protocol is wave-gated: each wave has a precondition and an output, and
you load at most one ref per wave so the context stays lean.

### Wave 0 — Ground & orient

1. Confirm the swarm CLI is reachable: run `uv run superclaude swarm --help`. If it errors, STOP and tell
   the user swarm isn't installed/!reachable from here (see Error Handling).
2. **Load `refs/cli-contract.md`** — the verified flag surface, lens/recipe/transport catalog, env
   contract, validation rules, exit codes, and stale-doc warnings. This ref is your source of truth for
   every recommendation in later waves.
3. Cross-check: skim the live `run --help` output against the ref's flag table. If a flag in the ref is
   absent from `--help` (or vice-versa), trust `--help` and note the drift to the user.

Output: a confirmed, current understanding of what this installed swarm can do.

### Wave 1 — Interview (plain language, no jargon)

**Load `refs/interview.md`** — the question bank, the `AskUserQuestion` option sets, and the goal→lens
mapping table.

Conduct a short Socratic interview using `AskUserQuestion` (multiple-choice keeps it easy for a novice).
Most users only need Q1–Q3; infer the rest from defaults and confirm once. Honor `--yes` by asking only
the irreducible questions (goal + target) and defaulting everything else.

Never show raw lens IDs as the first thing — present the **plain-language "I want to…" options** from the
mapping table, then translate the user's pick into a lens behind the scenes. Collect:

- goal → lens, target → `--target`, transport intent → `stub` vs `openai_compat`, reviewer count →
  `--reviewers` (explain "more = broader but slower"), watch mode → `--tui` vs `--detached`, and (only on
  `--advanced`) whether they need a custom prompt.

Output: a complete answer set with no remaining ambiguity. If two lenses fit the goal equally, ask a
disambiguating question rather than picking silently.

### Wave 2 — Map, build & validate the run

Still using `refs/interview.md` (mapping) and `refs/cli-contract.md` (rules):

1. **Map** the answers to a concrete plan: `{lens, target, output_dir, transport, reviewers?, line_cap?,
   timeout?, label?, watch_mode}`. Default path = a `--lens` shortcut (no hand-authored JobSpec). Reserve
   scaffold/JobSpec authoring for the `--advanced` / custom branch.
2. **Pre-validate everything that the CLI would reject (EXIT 2) so the user never sees a usage error:**
   target exists + ≥50 non-ws bytes; exactly one input mode; `--reviewers` ∈ [2,4]; no mutually-exclusive
   flag pairs; `--tui` only with a TTY + `--output`; `--detached` only with tmux available and not nested
   in tmux; if `openai_compat`, the env contract (`T2ProxyUrl`/`T2ProxyKey`/`T2Model01..09`) is satisfied.
   The full checklist is in `refs/cli-contract.md` §"Pre-flight the user can't see fail".
3. **Registry sanity:** run `uv run superclaude swarm validate-lenses` and confirm it passes.
4. (Advanced/JobSpec branch only) scaffold the spec, then author the completed JobSpec with the **Write**
   tool (Write rewrites the whole file — no `Edit` grant needed; populate `target.path`+`output.dir` and
   the other required fields), then `uv run superclaude swarm validate <spec>.json`. Carry the §11.5
   injection-guard sentence verbatim; warn on `custom-py:` (it runs arbitrary host code).
5. Choose an **idempotent output dir** (default `.dev/swarm-runs/<lens>-<ts>/`; if it exists, append `-N`,
   never overwrite).

Output: a validated run plan + the exact `uv run superclaude swarm run …` command string, shown to the
user in plain language ("I'll run a 3-reviewer bare-review on src/auth.py, as a safe practice run first").

### Wave 3 — Stub dry-run (MANDATORY gate)

**Load `refs/run-monitor-summarize.md`** — command recipes + monitoring + the summary template + error
matrix.

Always run the plan once with `--transport stub` first, regardless of whether the user wants real models.
The stub run is deterministic, needs no credentials, and proves the whole pipeline end-to-end in well
under a second.

1. Run the dry-run command (stub) with the chosen `--output`.
2. Confirm success: exit 0, `.swarm-state.json` `state == "terminal"`, and `return-contract.yaml` present.
3. Tell the user, in plain language, that the practice run worked and **what stub output means** (the
   content is placeholder text, not real analysis — it only proves the machinery). If the dry-run fails,
   STOP, diagnose via the error matrix, and fix the plan before going further. Do NOT proceed to a real
   run on a failed dry-run.

Output: a green pipeline + an honest explanation of what was (and wasn't) just produced.

### Wave 4 — Launch & monitor the real run (only with go-ahead)

Only if the user wants real analysis AND the dry-run passed AND the env contract is satisfied:

1. **Ask for an explicit go-ahead** ("Ready to run this for real against the proxy? It will use your
   models and may take a bit."). No real run without a yes.
2. Launch using the safe monitoring approach for the user's situation (`refs/run-monitor-summarize.md`):
   - Foreground + real TTY → add `--tui` for a live dashboard.
   - Background / fire-and-forget → `--detached`, then poll the filesystem.
   - You (the wizard) tailing on their behalf in a non-TTY → arm a `Monitor` on `execution-log.jsonl`
     for `worker_done` events + watch `.swarm-state.json` reach `terminal`. Do NOT wait on `done.json`
     for an inline run — it is never written there and the wait will hang.
3. Surface progress in plain language as it streams (e.g. "Reviewer 2 of 3 finished").

Output: a launched, monitored run that reaches a terminal state.

### Wave 5 — Summarize the outcome

Using `refs/run-monitor-summarize.md` and `templates/summary.md`:

1. Parse `return-contract.yaml` (`status`, `workers_succeeded`/`requested`/`failed`, `output_files[]`,
   `merged_path`, `recommended_next_command`) and `.swarm-state.json` (`state`).
2. Render the plain-language summary from `templates/summary.md`: did it succeed, how many reviewers
   agreed/finished, where the merged findings live, and the single recommended next action (the lens's
   hand-off command, already rendered in the contract).
3. Offer the next step as a copy-paste command (e.g. `/sc:adversarial …`), and offer to re-run with
   different settings.

Output: a Return Contract (below) and a human-readable summary.

## Return Contract

Emit these typed fields so a caller can compose on this skill:

- `status`: for an executed run, mirrors the run contract's `status` (`success` | `partial` | `failed`).
  `cancelled` is a wizard-only value, set when the user declines the real run after a green dry-run (the
  run contract itself never emits `cancelled`).
- `lens`, `transport`, `target`, `output_dir`: the resolved plan.
- `dry_run_passed`: bool.
- `contract_path`: path to `return-contract.yaml` (real run) or the dry-run's contract.
- `workers_requested` / `workers_succeeded` / `workers_failed`: ints from the contract.
- `merged_path`: path to `merged.md` if produced, else null.
- `recommended_next_command`: the rendered hand-off command string.

## Error Handling

Diagnose against this matrix; full diagnostics + fixes are in `refs/run-monitor-summarize.md` §Errors.
The governing principle: **the user never sees a raw rule code or traceback without a plain-language
translation and a concrete next action.**

| Scenario | Behavior | Fallback |
|---|---|---|
| `swarm --help` errors (CLI not reachable) | STOP. Explain swarm isn't installed/reachable here. | Suggest `uv run superclaude swarm --help` from the repo root; offer to check the dir. |
| Target missing / <50 non-ws bytes (IMM-4) | STOP before running. Explain the size floor plainly. | Offer to pick a different/bigger file or point at a directory entry. |
| `--real` but env contract unsatisfied (INV-007) | WARN. List which of `T2ProxyUrl`/`T2ProxyKey`/`T2Model01` is missing (names only, never values). | Offer a stub run now, or walk through `~/.aienv` setup (use ONLY `.aienv` values). |
| Mutually-exclusive flags requested | Prevent it in Wave 2; explain why they can't combine. | Pick the one that matches the user's intent and confirm. |
| Dry-run fails | STOP. Diagnose via the matrix; do not proceed to a real run. | Fix the plan (target, env, flags) and re-dry-run. |
| Real run terminal status `partial`/`failed` | Report honestly which reviewers failed and why (per-worker `status`). | Offer a `--resume` (skips succeeded workers) or a retry. |
| Monitor / run hangs | Don't poll `done.json` on inline runs. Fall back to `status --watch` / state polling. | Offer `--detached` next time; surface the last log events. |
| User declines the real run | Return `status: cancelled` with the green dry-run summary. | Leave the validated command for them to run later. |

## Will Do

- Translate every swarm concept to plain language; ground every recommendation in the live `--help`.
- Always run a stub dry-run before any real run; verify the env contract before a real run; ask before launching.
- Monitor the run it launched and summarize the outcome + the single recommended next step.
- Keep output dirs idempotent (append `-N`, never overwrite).

## Will Not

- Launch a real-model run without an explicit go-ahead and a passing dry-run.
- Invent T2 proxy endpoints or model names (uses only `~/.aienv`).
- Promise a live `--tui` dashboard on a non-TTY stream, or combine mutually-exclusive flags.
- Expose raw rule codes / tracebacks without a plain-language explanation and a next action.
