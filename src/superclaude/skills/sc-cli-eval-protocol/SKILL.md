---
name: sc:cli-eval-protocol
description: "Full behavioral protocol for sc:cli-eval — author a new cliEval suite (create) or interactively select and supervise a run of an existing suite (run), with a mandatory fresh-context load on both paths."
allowed-tools: Read, Glob, Grep, Edit, Write, Bash, TodoWrite, Task, Skill, AskUserQuestion
argument-hint: "create|run [--name <stem>] [--from @<spec>] [--suite <name>] [--eval <id>] [--agents opus,sonnet,haiku]"
---

<!-- Extended metadata (for documentation, not parsed):
category: testing
complexity: advanced
mcp-servers: [sequential, context7, serena]
personas: [architect, analyzer, qa, scribe]
version: 1.0.0
-->

# cliEval Suite Lifecycle Protocol

## Purpose

Govern the two highest-value cliEval lifecycle operations behind one command:

- **create** — author a NEW suite manifest well: propose → critique → debate/merge → author →
  schema-validate → document.
- **run** — interactively select an EXISTING suite, confirm a safe invocation, supervise a live run,
  and report results faithfully.

`sc:cli-eval-protocol` is invoked ONLY by the `sc:cli-eval` command via `Skill sc:cli-eval-protocol`
in its `## Activation` section. It is never invoked directly by users.

**Core objective**: never reason from a stale or hardcoded eval contract. Both pipelines begin by
re-reading the live CLI/schema/artifact surface and citing it. The skill orchestrates existing
components (`/sc:spec-panel`, `/sc:adversarial`, `/sc:document`) rather than reinventing them, and
adds NO flags to the `superclaude eval` CLI.

## Input Contract

### Required (STOP if missing)

- `$1` ∈ {`create`, `run`} — the pipeline selector. STOP and ask if neither is present.

### Optional

- create: `--name <stem>` (snake_case), `--from @<spec>`, `--agents <spec>[,...]` (default `opus,sonnet,haiku`).
- run: `--suite <name>`, `--eval <id>` (pre-selections; otherwise interactive).

## Wave 0 — Shared: Mandatory Fresh-Context Load (BOTH pipelines)

**This wave is non-negotiable and runs before any create/run action.**

1. Parse `$1`; STOP if not `create`/`run`. Initialize a TodoWrite checklist for the chosen branch.
2. **Delegate the fresh-context load** to the `eval-docs-loader` agent (Task tool). It re-reads the
   canonical sources and returns a citation-bearing digest: the `eval` subcommand+flag matrix, the
   suite.schema.json field reference, the artifact layout + run-id format, the summary.json schema +
   status enum, the exit-code map, the FR-G5 gate + empty-HOME workaround, and `--no-pty` semantics.
3. **Gate**: if the loader reports a missing/moved canonical source, surface it and confirm with the
   user before proceeding — do NOT substitute a remembered value. The digest is the ONLY authority
   for flags/fields the rest of this protocol uses. If you ever need a flag/field not in the digest,
   re-invoke the loader; never hardcode.

**Refs Loaded**: none yet. (The digest the loader returns supersedes any remembered contract.)

After Wave 0, branch on `$1`.

---

## CREATE PIPELINE

**Refs Loaded (create)**: Read `refs/create-pipeline.md` for the full step detail and
`refs/integration-map.md` for the exact `/sc:spec-panel` and `/sc:adversarial` invocation syntax.
Load `refs/eval-contracts.md` only if the loader digest is insufficient and you must re-derive.

### W1 — Draft the design spec

Draft (or load via `--from`) an eval-suite design spec into
`.dev/eval-workspaces/cli-eval/design/<stem>-spec.md`: what behavior the suite guards, scenarios,
fixtures, isolation strategy, cadence, and the assertions each eval will make. Ground every contract
claim (flags, schema fields) in the Wave-0 digest.

### W2 — Critique with the multi-expert panel (REUSE)

Invoke: `Skill sc:spec-panel` with `@<stem>-spec.md --mode critique --focus requirements,architecture`.
Fold the panel's findings back into the spec. Do not reimplement a review panel.

### W3 — Produce 2-3 competing designs + debate/merge (REUSE)

Produce 2-3 competing suite designs (different scenarios / fixtures / assertions / cadence /
isolation). Then merge them with `Skill sc:adversarial-protocol`:

- Mode-B (generate then merge): `--source <stem>-spec.md --generate eval-suite --agents <agents>`.
- Mode-A (you already wrote the variants): `--compare designA.md,designB.md,designC.md`.
Capture the merged design + transcript under `.dev/eval-workspaces/cli-eval/design/`.

### W4 — Author the manifest schema-first (DELEGATE)

Delegate to the `eval-suite-author` agent (Task). It authors `src/superclaude/cli/eval/suites/<stem>.yaml`
(+ fixtures + `<stem>_callbacks.py` only if the design needs them) in the house style of
`eval_smoke.yaml` / `installer_sync_drift.yaml`, then self-validates.

### W5 — Validate (done-ness gate)

A suite is DONE only when `uv run superclaude eval describe --suite <stem>` returns loader exit 0
and `uv run superclaude eval list --json` shows it. On non-zero exit, return to W4 with the loader
error. Do not mark create complete on an unvalidated manifest.

### W6 — Document (REUSE)

Update the inventory in `docs/eval/suites-guide.md` and the "what lives in this directory" table in
`src/superclaude/cli/eval/suites/README.md` via `Skill sc:document` (or the `technical-writer` agent).
Optionally run `evidence-validator` over the doc edits to confirm every cite resolves.

**Create return contract**: see the Return Contract section.

---

## RUN PIPELINE

**Refs Loaded (run)**: Read `refs/run-pipeline.md` for the full step detail (menu construction,
gotcha handling, monitoring, reporting).

### W1 — Enumerate the library via the CLI

Run `uv run superclaude eval list --json` (NEVER scrape the directory by hand — go through the loader
so the menu matches exactly what `eval run --suite` will accept). Parse the `{name, version,
eval_count}` array.

### W2 — Interactive selection (AskUserQuestion)

Present the suites as an `AskUserQuestion` menu (name — version — eval_count). On selection, optionally
drill in with `uv run superclaude eval describe --suite <name>` and show its evals, isolation
strategy, timeouts, and any `no_pty: skip` markers. Honor `--suite`/`--eval` pre-selections by
pre-filling the menu.

### W3 — Confirm the invocation + flags (AskUserQuestion)

Before launching, confirm the EXACT invocation with the user: the suite (+ optional `--eval <id>`),
`--parallel`, and the safety flags from the digest (`--no-pty`, `--no-mcp`, `--json`, `--junit`,
`--timeout-mult`, `--keep-home`, `--max-disk-mb`, `--output-dir`). Surface the two operational gotchas:

- **FR-G5 coverage gate (exit 2)**: the doctor preflight checks every `~/.claude/settings.json`
  matcher against the suite. If it would fail, offer the empty-HOME workaround from the digest
  (`TMPHOME=$(mktemp -d) HOME=$TMPHOME ...; rm -rf "$TMPHOME"`).
- **`--no-pty` → SKIPPED**: PTY-driven evals (`no_pty: skip`) short-circuit to SKIPPED with
  `skip_reason="--no-pty"`. Make clear whether the user wants a real run (omit `--no-pty`) or the
  CI-canary skip path.

### W4 — Monitor a live run (background Bash + Monitor)

Launch `uv run superclaude eval run --suite <name> [confirmed flags]` as a **background** Bash job and
attach a **Monitor** that emits per-eval PASS/SKIP/FAIL/ERROR signals and the terminal exit (per-eval
timeouts can reach 3600s, so do not block). Capture the run output path. Prefer `--verbose` (not only
`--json`) so a non-production-executor warning is not suppressed (see W5 authoritativeness).

### W5 — Parse + report (DELEGATE)

Delegate to the `eval-run-reporter` agent (Task) to parse `summary.json` (machine-readable truth;
`summary.md` is the operator table) under `<output_root>/.dev/eval-runs/<YYYY-MM-DD>/<run-id>/` and
produce the operator report: per-eval status/duration/skip_reason, the run-dir path, the exit-code
interpretation, and the preserved failed-HOME paths (from each eval's `artifacts{}`). **Surface any
non-zero exit / FAIL / ERRORED / TIMEOUT as a result — never a silent pass.** SKIPPED ≠ PASS.
**Authoritativeness**: establish which executor produced the result; if a non-production/stubbed
executor was used (it may emit a `results MUST NOT be treated as authoritative` warning, suppressed by
`--json`), label the run NON-AUTHORITATIVE (plumbing only) and state what unblocks a real run. A
stubbed PASS is never reported as a real eval pass.

**Run return contract**: see the Return Contract section.

---

## Delegation Pattern

| Agent / Skill | Role | Pipeline | Instantiation |
|---------------|------|----------|---------------|
| `eval-docs-loader` | Fresh-context digest (cited) | both | Task, Wave 0 |
| `Skill sc:spec-panel` | Multi-expert spec critique | create W2 | Skill (REUSE) |
| `Skill sc:adversarial-protocol` | Debate/merge + variant generation | create W3 | Skill (REUSE) |
| `eval-suite-author` | Schema-first manifest authoring + self-validate | create W4 | Task |
| `Skill sc:document` / `technical-writer` | Docs inventory updates | create W6 | Skill/Task (REUSE) |
| `evidence-validator` | Optional doc-citation re-check | create W6 | Task (REUSE) |
| `eval-run-reporter` | summary.json parse + operator report | run W5 | Task |

## Return Contract

| Field | Type | Description |
|-------|------|-------------|
| `pipeline` | string | `create` or `run` |
| `status` | string | `success`, `partial`, `failed` |
| `fresh_context_ok` | bool | Wave-0 loader returned a complete cited digest |
| `suite` | string | Suite stem authored (create) or run (run) |
| `validated` | bool | create: `eval describe` exit 0 |
| `run_dir` | string | run: `<output_root>/.dev/eval-runs/<date>/<run-id>/` |
| `outcome` | object | run: counts/totals from summary.json + process exit code |
| `artifacts_dir` | string | Design/run artifacts under `.dev/eval-workspaces/cli-eval/` |
| `unresolved` | list | Open items (failed validation, FAIL/ERROR evals, missing sources) |

## Error Handling

| Scenario | Behavior | Fallback |
|----------|----------|----------|
| `$1` not create/run | STOP, ask which pipeline | None |
| Fresh-context source missing/moved | Surface as finding, confirm before proceeding | Do NOT use remembered value |
| `/sc:spec-panel` or `/sc:adversarial` errors | Retry once with reduced payload | Proceed with the un-merged best design + note the gap |
| `eval describe` non-zero (create) | Read loader error, fix manifest, re-validate | Max 3 fix loops, then report blocked |
| FR-G5 coverage gate (exit 2, run) | Offer empty-HOME workaround from digest | Re-run under `TMPHOME`/`HOME` |
| Run exits non-zero / any FAIL/ERRORED/TIMEOUT | Report it as the result via reporter | Preserve + cite failed HOMEs |
| All evals SKIPPED (e.g. `--no-pty`) | Report as skipped, NOT pass; state why | Offer the real-run (no `--no-pty`) invocation |
| Non-production/stubbed executor (canned PASS) | Label run NON-AUTHORITATIVE; state what unblocks a real run | Re-run `--verbose` to surface the warning `--json` suppressed |

## Will Do

- Re-read + cite the live eval contract surface before every create/run action.
- Reuse `/sc:spec-panel`, `/sc:adversarial`, `/sc:document` instead of reinventing them.
- Treat `eval describe` exit 0 as the only definition of a finished suite.
- Supervise real runs and surface failures + forensic HOME paths honestly.

## Will Not Do

- Add or modify any flag on the `superclaude eval` CLI.
- Hardcode a flag list or schema field not present in the Wave-0 digest.
- Mark a suite done without schema validation, or present a non-green run as green.
- Edit `.claude/` directly (source of truth is `src/superclaude/`; sync via `make sync-dev`).
