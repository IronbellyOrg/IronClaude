# Swarm CLI Contract — verified ground truth (load in Wave 0)

Distilled from `.dev/swarm-wizard/SWARM-WIZARD-FACTS.md`, built from 7 `/sc:analyze` agents over
`docs/swarm/` + `src/superclaude/cli/swarm/` and **empirically verified** against the live CLI on
2026-06-19. Where this disagrees with `docs/swarm/`, this file (and the live `--help`) win.

## Subcommands (8)

`run` · `scaffold` · `validate` · `validate-lenses` · `status` · `logs` · `attach` · `kill`.
Always prefix `uv run`. Global exit codes: **0** ok · **1** rule/contract failure · **2** usage error.

## `swarm run` — flag surface (the wizard's main build target)

Four mutually-exclusive **input modes** — exactly one: positional `SPEC_PATH` (JobSpec JSON file) ·
`--stdin` · `--lens NAME` · `--resume JOB_ID`. The layperson default is the **`--lens` shortcut**.

| Flag | Default | Wizard note |
|---|---|---|
| `--lens TEXT` | — | Requires `--target` + `--output`. `custom`/unknown → EXIT 2. |
| `--target PATH` | — | The file to review. Required with `--lens`. |
| `--output DIRECTORY` | — | Wires ALL artifacts. Required with `--lens`/`--resume`. |
| `--transport [openai_compat\|stub]` | **`stub` on the `--lens` path** | Default to `stub`. ⚠ `--transport` help text wrongly says "openai_compat default" — the lens-expansion default is `stub` (verified). |
| `--reviewers INTEGER` | lens default (3; 4 for edge-case-hunt & troubleshoot-hypothesis) | **Inclusive [2,4]** — outside → EXIT 2. |
| `--target-line-cap INTEGER` | 4000 | rarely changed. |
| `--timeout-sec INTEGER` | 180 | per-worker. |
| `--label TEXT` | `swarm-run-lens-<lens>` | cosmetic; must be tmux-legal if detached. |
| `--tui` | off | **REAL FLAG** (omitted from command-reference.md). Live dashboard. Fresh-run only, TTY-required (silent no-op off-TTY), needs `--output`. XOR `--resume`, XOR `--detached`. Safe to recommend on a real interactive terminal. |
| `--detached` | off | tmux session `swarm-<job_id>`. Needs tmux on PATH + NOT nested in tmux + `--output`. XOR `--resume`, XOR `--tui`. |
| `--resume TEXT` | — | Resume from `manifest.json`. Needs `--output`. XOR SPEC/stdin/lens/detached/tui. Skips succeeded workers. |
| `--force-relens` | off | resume-only. |
| `--stdin` | off | JobSpec from stdin. |
| `--auto-inject-guard` | off | custom-prompt-dir migration only. |

Other subcommands: `scaffold --lens NAME [-o FILE]` · `validate [--strict] JOBSPEC_PATH` (`--strict` is a
no-op; schema-only) · `validate-lenses [--warning-mode]` · `status --output DIR [--watch] [--watch-interval 2.0]`
· `logs --output DIR [--jsonl|--md] [-f|--follow] [--tail] [--lines N]` (`--tail` = `--jsonl --follow`) ·
`attach JOB_ID` · `kill JOB_ID [--output DIR]`.

## The 7 dispatchable lenses (exact IDs; `custom` is rejected as a shortcut)

| Lens ID | "Pick me when the user wants…" | Workers | Recipe | Hands off to |
|---|---|---|---|---|
| `bare-review` | "review my code for bugs / correctness" (**only stable lens**; flags suspect files) | 3 | `bare-review-v1` | `/sc:adversarial` |
| `refactor-find` | "find small safe cleanups to apply" | 3 | `findings_table_v1` | `/sc:code-review --apply` |
| `edge-case-hunt` | "what inputs/states break my code?" | 4 | `findings_table_v1` | `/sc:adversarial` |
| `spec-completeness` | "is my spec complete / what's missing?" | 3 | `verdict_only_v1` | `/sc:reflect` |
| `feasibility-probe` | "will this approach actually work?" | 3 | `verdict_only_v1` | `/sc:research` |
| `troubleshoot-hypothesis` | "why is this failing — rank root causes" | 4 | `hypothesis_table_v1` | `/sc:troubleshoot` |
| `doc-completeness` | "audit my docs for gaps / staleness" | 3 | `findings_table_v1` | `/sc:document` |

Only `bare-review` is `stable`; the other 6 are `experimental` (mention gently, don't alarm). Recipes are
implied by the lens (no `--recipe` flag). Recipes never score/dedupe/reorder — cross-worker judgement is
the downstream hand-off skill's job.

`custom` lens = advanced only: a bare `--lens custom` is rejected; it needs a spec file with
`custom_prompt_dir` (a `system.txt`/`user.txt`/`meta.yaml` dir). `custom-py:` recipes execute arbitrary
host code (no sandbox) — warn explicitly. Gate behind `--advanced`.

## Transports + the T2 proxy env contract

- **`stub`** — deterministic, no network, no credentials. The safe default AND the mandatory dry-run
  transport. Output is placeholder text (`stub:<model>:<hash>`), NOT real analysis — say so.
- **`openai_compat`** — real models. Reads env at Wave 0:
  - `T2ProxyUrl` (base URL; `/chat/completions` appended) — required
  - `T2ProxyKey` (bearer token) — required
  - `T2Model01` … `T2Model09` (dense, one per worker, **max 9**) — at least `T2Model01` required
  - Missing any → `TransportEnvError` → the run fails at Wave 0. Check before launch; report only the
    missing **names**, never values.
- **`~/.aienv` convention** (operator memory, NOT code-enforced): base must start with `:4000/cli`, models
  `T2Model01..NN`. Use ONLY endpoints/models from `~/.aienv`. A wrong base fails late as a `proxy_error`.
- No streaming / tool-calls / vision in Phase 1.

## Pre-flight the user can't see fail (mirror these BEFORE emitting a command — all are EXIT 2 / hard fail)

1. Exactly one input mode.
2. Target exists AND ≥ **50 non-whitespace bytes** after truncation (IMM-4). Check with e.g.
   `test -f <target>` and a non-whitespace byte count.
3. `--lens` requires BOTH `--target` and `--output`.
4. `--reviewers` ∈ [2,4].
5. `--lens custom` / unknown lens → rejected (use advanced spec path for custom).
6. `--resume` XOR {SPEC, `--stdin`, `--lens`, `--detached`, `--tui`}.
7. `--tui` XOR `--detached`; both fresh-run only.
8. `--tui` needs a real TTY + `--output` (else silent no-op — don't promise a dashboard off-TTY).
9. `--detached` needs tmux on PATH, NOT nested in tmux (`TMUX` unset), + `--output`.
10. `job_id`/`--label` tmux-legal (no `:`, `.`, whitespace) when detached.
11. (advanced JobSpec) `spec_version: "1.1"`; every nested field required; §11.5 guard sentence verbatim in
    `prompt.system` AND as `injection_guard.required_substring`.

## Artifacts a fresh inline `--lens` run writes to `--output` (VERIFIED)

`.swarm-state.json`, `execution-log.jsonl`, `execution-log.md`, `manifest.json`, `merged.md`,
`return-contract.yaml`, and per-worker `*.final.md` + `*.meta.json` (+ `*.raw.md`). **`done.json` is NOT
written on a fresh inline run** — only on detached/resume completion + `swarm kill`.

## Completion + summarization schema (VERIFIED)

- Inline completion = `.swarm-state.json` `state == "terminal"` AND `return-contract.yaml` present.
  Do NOT poll `done.json` for inline runs (never appears → hang).
- `.swarm-state.json` = `{job_id, state, updated}`; `state` ∈
  `preflight_ok → dispatching → normalizing → reducing → terminal`.
- `return-contract.yaml` headline fields: `status` ∈ `success|partial|failed` (IMM-5: M==N→success;
  2≤M<N→partial; M<2→failed); `workers_requested|succeeded|failed`; `output_files[]` (per worker:
  `final_path`, `status`, `model_label`, `bytes`, `elapsed_ms`); `merged_path`; `recommended_next_command`.
- Per-worker status ∈ `success|timeout|parse_error|proxy_error`. Detached/kill `done.json.terminal_status`
  ∈ `success|partial|failed|killed` (4 values).
- Log event types: `worker_start|worker_progress|worker_done|wave_transition|terminal` (use `worker_done`,
  NOT `worker_complete`).

## STALE-DOC WARNINGS — do not trust these doc claims (code wins)

1. `command-reference.md` omits `--tui` — it is real. Surface it.
2. "Default transport is openai_compat" — the `--lens` default is `stub`. Default the wizard to stub.
3. "Fresh runs emit only 4 files / no return-contract.yaml / M5 not wired" — STALE. Fresh inline runs DO
   emit `merged.md` + `return-contract.yaml`.
4. `user-guide.md` shows `--custom-prompt-dir` as a `run` flag — there is no such flag; it's a JobSpec field.
5. `done.json` "wait for done" pattern does NOT apply to inline runs.
