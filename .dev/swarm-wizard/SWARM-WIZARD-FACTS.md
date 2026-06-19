# Swarm Wizard — Canonical Facts-Sheet (ground truth for skill authoring)

> Built 2026-06-19 from 7 parallel `/sc:analyze` agents over `docs/swarm/` + `src/superclaude/cli/swarm/`,
> then **empirically verified** against the live CLI (`uv run superclaude swarm ... --help`) and a real
> stub run. Where docs and code disagree, **code wins** and the divergence is flagged in §9.
> This file is the single source of truth for the `sc:swarm-wizard` command + skill. Do not re-derive
> facts; cite this sheet. Every load-bearing claim below was confirmed first-hand this session.

---

## 1. Mission of the wizard

The existing swarm docs are too technical for a layperson. Build an **interactive Q&A command + skill**
that:

1. **Interviews** the user (Socratic, plain-language) to determine *what* they want reviewed, *why*, and
   *how* — gathering ALL inputs needed to run swarm successfully.
2. **Maps** their goal → the correct lens + transport + flags (no jargon leaks to the user).
3. **Generates** all components needed for the run (a validated JobSpec and/or a `--lens` shortcut
   invocation; a custom prompt dir only on the advanced path).
4. **QA/validates** the components (`swarm validate`, `swarm validate-lenses`) and runs a **stub dry-run**
   before any real-model run.
5. **Offers to run** the swarm in a shell, **monitors** it live, and **summarizes** the outcome in plain
   language with the recommended next action.

The wizard's prime directive: **a non-expert should never see `IMM-4`, `INV-007`, `Wave 0`, `M5`, or a raw
traceback.** Every prompt and every result is translated to plain language.

---

## 2. Command surface (VERIFIED against live `--help`)

`superclaude swarm` (Click group) exposes **8 subcommands**. Canonical invocation prefix is `uv run`.

| Subcommand | One-liner | Required inputs |
|---|---|---|
| `run` | Wave 0 preflight → Wave 1 dispatch (+ inline Wave 2/3 normalize+merge) | one input mode (see below) |
| `scaffold` | Emit a starter JobSpec for a lens | `--lens NAME` (non-custom) |
| `validate` | Schema-check a JobSpec JSON file | positional `JOBSPEC_PATH` |
| `validate-lenses` | Validate the bundled LENSES registry | (none; opt `--warning-mode`) |
| `status` | Report a job's phase + status | `--output DIR` |
| `logs` | Dump or tail a job's execution log | `--output DIR` |
| `attach` | Re-attach to a detached tmux session | positional `JOB_ID` |
| `kill` | Terminate a detached tmux session | positional `JOB_ID` |

**Global exit codes:** `0` ok · `1` rule/contract failure (preflight, schema, terminal-partial/failed) ·
`2` usage error.

### `swarm run` — full flag surface (VERIFIED)

Four **mutually-exclusive input modes** — exactly one: positional `SPEC_PATH` (JobSpec JSON file) ·
`--stdin` · `--lens NAME` · `--resume JOB_ID`.

| Flag | Type | Default | Notes |
|---|---|---|---|
| `--stdin` | flag | off | Read JobSpec JSON from stdin |
| `--lens TEXT` | str | — | Shortcut. Requires `--target` + `--output`. `custom`/unknown → EXIT 2 |
| `--resume TEXT` | str | — | Resume from `manifest.json`. Requires `--output`. XOR SPEC/stdin/lens/detached/tui |
| `--target PATH` | path | — | Override `target.path`. Required with `--lens` |
| `--output DIRECTORY` | dir | — | Wires ALL artifacts. Required with `--lens`/`--resume` |
| `--transport [openai_compat\|stub]` | choice | **stub on the `--lens` path** | `stub` = deterministic, no network (safe default). `openai_compat` = real T2 proxy. ⚠ the `--transport` help text says "openai_compat (default)" but the **lens-expansion default is `stub`** — verified in `--lens` help + live run |
| `--reviewers INTEGER` | int | lens default (3 bare-review) | **Inclusive range [2,4]** — outside → EXIT 2 |
| `--target-line-cap INTEGER` | int | 4000 | → `target.truncation.line_cap` |
| `--timeout-sec INTEGER` | int | 180 | per-worker timeout |
| `--label TEXT` | str | `swarm-run-lens-<lens>` | stamped on output frontmatter |
| `--force-relens` | flag | off | resume only; re-resolve lens from live registry. Requires `--resume` |
| `--detached` | flag | off | tmux session `swarm-<job_id>`. Needs tmux+`--output`. XOR `--resume`, XOR `--tui` |
| `--tui` | flag | off | **REAL FLAG (omitted from command-reference.md).** Live Rich dashboard. Fresh-run only, TTY-required (silent no-op on non-TTY), needs `--output`. XOR `--resume`, XOR `--detached` |
| `--auto-inject-guard` | flag | off | custom-prompt-dir migration only |

### Other subcommands (flags)

- `scaffold --lens NAME [-o/--output FILE]` — non-custom lens required; stdout if no `-o`.
- `validate [--strict] JOBSPEC_PATH` — `--strict` is a **no-op** today. Schema-only (not preflight).
- `validate-lenses [--warning-mode]` — blocking by default (exit 1 on fail); `--warning-mode` → exit 0 + warnings.
- `status --output DIR [--job ID] [--watch] [--watch-interval 2.0] [--watch-max-iterations N]`.
- `logs --output DIR [--job ID] [--jsonl|--md] [-f/--follow] [--tail] [--lines N] [--watch-interval 0.5]`.
  `--tail` == `--jsonl --follow`. `--md` is default.
- `attach JOB_ID` (no options). `kill JOB_ID [--output DIR]` (`--output` flips state→terminal + writes done.json terminal_status=killed).

---

## 3. The 7 lenses (the user's main choice) + recipes

`--lens` accepts these **7 dispatchable IDs** (exact strings; `custom` is rejected as a shortcut):

| Lens ID | Plain-language "pick me when…" | Workers | Recipe | Hands off to |
|---|---|---|---|---|
| `bare-review` | "Review my code for bugs / correctness" (**only stable lens**; flags suspect files) | 3 | `bare-review-v1` | `/sc:adversarial` |
| `refactor-find` | "Find small safe cleanups to apply" | 3 | `findings_table_v1` | `/sc:code-review --apply` |
| `edge-case-hunt` | "What inputs/states break my code?" | 4 | `findings_table_v1` | `/sc:adversarial` |
| `spec-completeness` | "Is my spec complete / what's missing?" | 3 | `verdict_only_v1` | `/sc:reflect` |
| `feasibility-probe` | "Will this approach actually work?" | 3 | `verdict_only_v1` | `/sc:research` |
| `troubleshoot-hypothesis` | "Why is this failing — rank root causes" | 4 | `hypothesis_table_v1` | `/sc:troubleshoot` |
| `doc-completeness` | "Audit my docs for gaps / staleness" | 3 | `findings_table_v1` | `/sc:document` |

- Only `bare-review` is `stable`; the other 6 are `experimental` (interfaces may shift — surface gently).
- All default `target_line_cap = 4000`.
- **6 recipe IDs** (exact spelling — note hyphen vs underscore): `bare-review-v1`, `findings_table_v1`,
  `hypothesis_table_v1`, `verdict_only_v1`, `passthrough`, `custom`. Plus a `custom-py:<module>:<callable>`
  dynamic loader. Recipes **never score/dedupe/reorder** (AC-011) — cross-worker judgement is the
  downstream hand-off skill's job. Recipe is implied by the lens; there is **no `--recipe` flag**.
- **`custom` lens is an advanced trap:** a bare `--lens custom` is rejected; it needs a spec file with
  `custom_prompt_dir` (a 3-file prompt dir: `system.txt`/`user.txt`/`meta.yaml`). `custom-py:` recipes
  execute arbitrary host code (no sandbox). Gate `custom` behind an explicit "advanced" branch + warning.

---

## 4. Transports + env contract

- **`stub`** — deterministic, no network. The **safe default + mandatory dry-run transport.** Output is
  placeholder text (`stub:<model>:<hash>`), not real analysis — the wizard must tell the user the dry-run
  proves the pipeline works but is NOT real review content.
- **`openai_compat`** — real models via the T2 proxy. Requires env vars (read at Wave 0):
  - `T2ProxyUrl` (base URL; `/chat/completions` appended) — required
  - `T2ProxyKey` (bearer token) — required
  - `T2Model01` … `T2Model09` (dense, one per worker slot, **max 9**) — at least `T2Model01` required
  - Missing any → `TransportEnvError` listing all missing names → run fails at Wave 0.
- **`.aienv` convention** (from project memory, NOT code-enforced): base must start with `:4000/cli`,
  models named `T2Model01..NN`. The transport does NOT validate the `:4000/cli` shape — surface it as
  guidance; a wrong base fails late as a `proxy_error`. Use ONLY endpoints/models from `~/.aienv`.
- Phase-1 transport supports **no streaming, no tool-calls, no vision** — single user message, string content.

---

## 5. Cross-field validation the wizard MUST mirror (all are EXIT 2 / hard fails)

To never hand the user a failing command, the wizard enforces these BEFORE emitting a command:

1. Exactly one input mode (spec / stdin / lens / resume).
2. `--resume` XOR {SPEC_PATH, `--stdin`, `--lens`, `--detached`, `--tui`}.
3. `--tui` XOR `--detached`; both require a fresh run.
4. `--force-relens` requires `--resume`.
5. `--reviewers` ∈ [2,4].
6. `--lens custom` and unknown lens names are rejected → use the advanced spec-file path for custom.
7. `--lens` requires BOTH `--target` and `--output`.
8. `--tui` needs a real TTY + `--output`; silently no-ops otherwise (don't promise a dashboard off-TTY).
9. `--detached` needs tmux on PATH and NOT already inside tmux (`TMUX` unset) + `--output`.
10. Target file must be ≥ **50 non-whitespace bytes** after truncation (IMM-4) — pre-check before running.
11. `job_id` must be tmux-legal (no `:`, `.`, whitespace) for attach/kill.
12. JobSpec authoring: `spec_version` = **`1.1`** (current; `1.0` deprecated-warns); every nested field is
    required (`additionalProperties:false`), only `custom_prompt_dir` is omittable; the §11.5 injection
    guard sentence must appear verbatim in `prompt.system` AND as `injection_guard.required_substring`.

---

## 6. End-to-end workflow the wizard drives

```
Interview → map goal to {lens, transport, target, output, overrides}
         → (default path) build a --lens shortcut invocation
            OR (custom/advanced) scaffold → edit → `swarm validate`
         → `swarm validate-lenses`  (registry sanity)
         → STUB DRY-RUN: swarm run --lens … --transport stub --output <dir>
            → confirm exit 0 + artifacts present (proves pipeline)
         → offer REAL run (openai_compat) ONLY after env contract verified
         → launch (foreground+--tui on a TTY, or --detached for fire-and-forget)
         → monitor (see §7)
         → summarize outcome + recommended_next_command (see §7)
```

The simplest layperson happy path is a **`--lens` shortcut**, not a hand-authored JobSpec. Reserve
scaffold/validate/JobSpec authoring for the custom/advanced branch.

---

## 7. Monitoring + summarization schema (EMPIRICALLY VERIFIED)

A fresh inline `--lens` run (even with `stub`) writes to `--output`:
`.swarm-state.json`, `execution-log.jsonl`, `execution-log.md`, `manifest.json`, `merged.md`,
`return-contract.yaml`, and per-worker `*.final.md` + `*.meta.json` (+ `*.raw.md`). **`done.json` is NOT
written on a fresh inline run** — it appears only on detached/resume completion + `swarm kill`.

**Completion detection:**
- Inline: `.swarm-state.json` `state == "terminal"` AND `return-contract.yaml` present. (Do NOT poll for
  `done.json` on inline runs — it never appears and the wait hangs. Use `status --watch` or poll state.)
- Detached/resume/kill: `done.json` present; outcome in `terminal_status` ∈
  {`success`,`partial`,`failed`,**`killed`**} (4 values — `killed` is outside the normal enum).

**`.swarm-state.json`** shape (verified): `{ "job_id", "state", "updated" }`. `state` ∈
`preflight_ok → dispatching → normalizing → reducing → terminal`.

**`return-contract.yaml`** = the wizard's summarization source (verified). Key fields:
- `status` ∈ `success | partial | failed`  ← headline outcome (IMM-5: M==N→success; 2≤M<N→partial; M<2→failed)
- `workers_requested` / `workers_succeeded` / `workers_failed`
- `output_files[]` — per worker: `final_path`, `status`, `model_label`, `bytes`, `elapsed_ms`, `http_code`
- `merged_path` — path to `merged.md` (only when `amalgamation_mode == normalize+merge` and M ≥ floor(2))
- `caller_metadata.suspect` / `.tier`
- `recommended_next_command` — **rendered** next-step command the wizard presents to the user

**Per-worker status** ∈ `success | timeout | parse_error | proxy_error` (in `*.meta.json` and log
`worker_done` events). Event types in `execution-log.jsonl`: `worker_start | worker_progress |
worker_done | wave_transition | terminal` (note: use `worker_done`, NOT `worker_complete`).

**Safe monitoring approach for a novice:**
- Foreground interactive TTY → `--tui` (single-writer gate is closed on this branch — REG-1 PTY test
  passes; safe to recommend). Gives a live dashboard, no extra tooling.
- Programmatic / background → `--detached` then poll the filesystem (`done.json` sentinel, or
  `status --watch`). Never mix `--tui` with `--detached`.
- The wizard tailing on the user's behalf (non-TTY) → tail `execution-log.jsonl` for `worker_done` +
  read `.swarm-state.json`; do NOT rely on `--tui` (no-op off-TTY).

---

## 8. The interview (suggested question flow — plain language, no jargon)

1. **What do you want to do?** → maps to lens (use the §3 "pick me when" column, never show lens IDs first).
2. **What should I look at?** → target file/path (validate exists + ≥50 non-ws bytes).
3. **Real models or a safe practice run first?** → transport. Always do a stub dry-run regardless.
4. **(if real)** Do you have the proxy configured? → verify `T2ProxyUrl`/`T2ProxyKey`/`T2Model01` present;
   if not, walk them through `~/.aienv` (do NOT invent endpoints/models — use `.aienv` only).
5. **How many independent reviewers?** → `--reviewers` [2,4] (default per lens). Explain "more = broader,
   slower".
6. **Watch it live or run in the background?** → `--tui` (TTY) vs `--detached`.
7. **(advanced, optional)** custom prompt? → gated branch with the trust-boundary warning.
Keep it short: most users only need Q1–Q3. Infer the rest from sensible defaults and confirm once.

---

## 9. STALE-DOC WARNINGS — do NOT trust these doc claims (code wins)

1. **`command-reference.md` omits `--tui` entirely** — it is a real, supported flag. Surface it.
2. **"Default transport is openai_compat"** (in `--transport` help + parts of CR) — the **`--lens`
   expansion default is `stub`**. Verified. Default the wizard to stub.
3. **"Fresh runs emit only 4 files / no return-contract.yaml / M5 not wired"** (README, user-guide, CR) —
   **STALE.** Verified: fresh inline `--lens` runs emit `merged.md` + `return-contract.yaml` + per-worker
   normalized outputs. The inline Wave 2/3 pipeline is wired.
4. **`user-guide.md` shows `--custom-prompt-dir` as a `swarm run` flag** — there is **no such CLI flag**;
   `custom_prompt_dir` is a JobSpec field only, and `--lens custom` is rejected. Don't offer it as a run flag.
5. **validate-lenses "five assertions"** in some `--help`/docstrings — the validator runs **six**. Minor;
   not wizard-blocking.
6. **`done.json` "wait for done" pattern** in monitoring-patterns.md — does NOT apply to inline runs
   (sentinel absent). Use state==terminal for inline.

---

## 10. Repo placement + sync constraints (CRITICAL — VERIFIED against in-repo pattern)

Naming/layout confirmed by inspecting the existing `pr-submit` command + `sc-pr-submit-protocol` skill:

- **Command:** `src/superclaude/commands/swarm-wizard.md` (flat — NO `sc/` subdir in src; the `sc:` prefix
  is applied at install). Installs as `/sc:swarm-wizard`. Thin (~80–150 lines), zero protocol logic.
  Frontmatter fields (verbatim set used by pr-submit): `name`, `description`, `category`, `complexity`,
  `mcp-servers`, `personas`, `argument-hint`, `version`. Body: `# /sc:swarm-wizard - <title>`, `## Triggers`,
  `## Required Input`, `## Usage`, `## Options`, `## Behavioral Flow`, **`## Activation`** (MANDATORY),
  `## Boundaries` (Will / Will Not), `## Related Commands`.
- **`## Activation` (MANDATORY)** must read: `**MANDATORY**: Before executing any protocol steps, invoke:`
  then `> Skill sc:swarm-wizard-protocol` — and instruct NOT to execute using only the command file.
- **Skill:** `src/superclaude/skills/sc-swarm-wizard-protocol/SKILL.md` (+ `refs/`, `templates/`, `rules/`
  as needed). Registered name `sc-swarm-wizard-protocol`. Frontmatter: `name`, `description` (~50-token
  trigger surface, "Use this skill when… Trigger on phrases like…"), plus `category`, `complexity`,
  `mcp-servers`, `personas`, `allowed-tools` (scoped — e.g. `Bash(uv run superclaude swarm *)`, NOT bare
  Bash; include `AskUserQuestion`, `Read`, `Write`, `Grep`, `Glob`, `TodoWrite`, `Task`, `Monitor`),
  `argument-hint`. SKILL.md ≤ ~500 lines = behavioral protocol (WHAT/WHEN); push question banks, build
  templates, command recipes, and the summary template into `refs/`/`templates/` (load per-wave on demand).
- **NEVER write the skill/command into `.claude/`** — `.claude/{skills,commands}` is gitignored sync-dev
  output. Author in `src/`, then `make sync-dev` → `make verify-sync`. Only `git add` the `src/` side.
- **Registration (after authoring):** update `src/superclaude/core/COMMANDS.md`, `ORCHESTRATOR.md`,
  `FLAGS.md` (any new flags), `PERSONAS.md` (if persona auto-activation). Skipping = command invisible to routing.
- skill-creator eval/iteration workspace → **`.dev/eval-workspaces/sc-swarm-wizard-protocol/`** (project
  override of the plugin's sibling-workspace convention), NEVER `.claude/skills/*-workspace/`.
- **Quality bar** (from the developer guide): Input Contract with STOP/WARN gates; typed Return Contract
  with a `status` field; mandatory Error-Handling matrix (validation-fail / dry-run-fail / launch-fail /
  mid-run-error / MCP-unavailable); idempotent artifact dirs (append `-N`, never overwrite); 3–5
  copy-paste examples; explicit Will / Will Not boundaries.
