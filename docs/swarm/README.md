# MultiModelSwarm — Documentation Index

`superclaude swarm` fans a single prompt across **N heterogeneous OpenAI-compatible
workers**, normalizes each worker's output through a **lens recipe**, and (in the
full pipeline) amalgamates the results into a caller-facing **ResultContract**. It is
the CLI substrate behind the multi-model review/troubleshoot/spec workflows.

> **What a run does.** A fresh `swarm run … --output <dir>` executes **Wave 0
> preflight → Wave 1 dispatch → Wave 2 normalize → Wave 3 reduce**. Besides the
> observability files it writes the per-worker outputs, `merged.md` (in the
> `normalize+merge` mode every bundled lens uses) and `return-contract.yaml`. The
> `done.json` sentinel is written only by `swarm kill <job_id> --output <dir>`. See
> [What a run emits](#what-a-run-emits).

---

## Start here

| If you want to… | Read |
|---|---|
| **Be guided through swarm in plain language (no jargon)** | [**Swarm Wizard Guide** (`/sc:swarm-wizard`)](wizard-guide.md) |
| Run your first swarm in 2 minutes | [User Guide → Quickstart](user-guide.md#1-quickstart-your-first-swarm-stub-transport) |
| Step-by-step worked examples across use cases | [**User Guide**](user-guide.md) |
| Look up a command's flags and exit codes | [**Command Reference**](command-reference.md) |
| Understand the 8 lenses and 6 recipes | [**Lens & Recipe Catalog**](lens-catalog.md) |
| Run against a real model proxy | [Runbook → T2 Proxy Env Contract](runbook.md#t2-proxy-env-contract-ac-017) |
| Watch a long-running job | [Monitoring Patterns](monitoring-patterns.md) |
| Know what transports are/aren't supported | [Transport Limits](transport-limits.md) |
| See what shipped in v1 | [Release Notes v1](release-notes-v1.md) |
| Read the design rationale for edge cases | [Open-Question Resolutions](oq-resolutions.md) |

---

## Command surface

Eight subcommands, registered under `superclaude swarm`
(`cli/swarm/__init__.py:172-179`, wired into the root CLI at `cli/main.py:430`):

| Command | One-line purpose | Full reference |
|---|---|---|
| `run` | Run a job (preflight → dispatch → normalize → reduce and return contract). | [ref](command-reference.md#swarm-run) |
| `scaffold` | Emit a starter JobSpec for a lens. | [ref](command-reference.md#swarm-scaffold) |
| `validate` | Schema-check a JobSpec JSON file. | [ref](command-reference.md#swarm-validate) |
| `validate-lenses` | Validate the bundled lens registry. | [ref](command-reference.md#swarm-validate-lenses) |
| `status` | Report a job's wave phase / status. | [ref](command-reference.md#swarm-status) |
| `logs` | Dump or tail a job's execution log. | [ref](command-reference.md#swarm-logs) |
| `attach` | Re-attach to a detached tmux session. | [ref](command-reference.md#swarm-attach) |
| `kill` | Terminate a detached tmux session. | [ref](command-reference.md#swarm-kill) |

```bash
uv run superclaude swarm --help          # list subcommands
uv run superclaude swarm run --help       # per-command flags
```

---

## Lenses & recipes (catalog)

A **lens** is a named review intent (prompt + worker count + recipe + downstream
hand-off). A **recipe** normalizes each worker's raw output into a canonical shape
**without judging, scoring, deduping, or reordering** (AC-011). Full details in the
[Lens & Recipe Catalog](lens-catalog.md).

| Lens | Workers | Recipe | Stability | Suspect | Hands off to |
|---|---|---|---|---|---|
| `bare-review` | 3 | `bare-review-v1` | stable | yes | `/sc:adversarial` |
| `refactor-find` | 3 | `findings_table_v1` | experimental | no | `/sc:code-review` |
| `edge-case-hunt` | 4 | `findings_table_v1` | experimental | no | `/sc:adversarial` |
| `spec-completeness` | 3 | `verdict_only_v1` | experimental | no | `/sc:reflect` |
| `feasibility-probe` | 3 | `verdict_only_v1` | experimental | no | `/sc:research` |
| `troubleshoot-hypothesis` | 4 | `hypothesis_table_v1` | experimental | no | `/sc:troubleshoot` |
| `doc-completeness` | 3 | `findings_table_v1` | experimental | no | `/sc:document` |
| `reflect-review` | 3 | `passthrough` | stable | yes | `/sc:adversarial` |
| `custom` | — | (escape hatch) | — | — | prompts from the JobSpec `custom_prompt_dir` field |

> The registry has **9 entries** (8 bundled lenses plus `custom`); `validate-lenses`
> validates **8** (the `custom` escape hatch is intentionally skipped — its prompt body
> flows in at preflight from the directory named by the JobSpec field
> `custom_prompt_dir`, which is not a command-line flag). `reflect-review` is the
> reviewer lens that `superclaude reflect` Tier 2 fans out.

---

## Transports

| Transport | Network? | Use when |
|---|---|---|
| `stub` | **No** — in-process, deterministic | CI, tests, docs, dry-runs, quick-dispatch (the default for `--lens` and `scaffold`). |
| `openai_compat` | Yes — httpx → `<base_url>/chat/completions` | Real fan-out against the T2 proxy. Requires the [env contract](runbook.md#t2-proxy-env-contract-ac-017). |

Phase-1 **excludes** streaming, function-calling/tool-use, and vision input — see
[Transport Limits](transport-limits.md).

---

## What a run emits

After a successful **fresh** `swarm run ... --output <dir>` (stub or proxy), `<dir>`
contains:

| File | Shape | Doc |
|---|---|---|
| `execution-log.jsonl` | One JSON event per line (machine surface) | [Command Ref → logs](command-reference.md#swarm-logs) |
| `execution-log.md` | Human-readable mirror of the same stream | same |
| `manifest.json` | Lens snapshot + preflight summary + caller metadata (resume anchor) | [Command Ref → run artifacts](command-reference.md#run-artifacts) |
| `.swarm-state.json` | Coarse wave phase (`preflight_ok`…`terminal`) | [Command Ref → status](command-reference.md#swarm-status) |
| `<lens>-NN-<model>.final.md` | One normalized output per worker (Wave 2) | [Command Ref → run artifacts](command-reference.md#run-artifacts) |
| `<lens>-NN-<model>.meta.json` | Per-worker sidecar (status, attempts, timing) | same |
| `merged.md` | All worker outputs merged (Wave 3; written when `amalgamation_mode` is `normalize+merge`, the default for every bundled lens) | same |
| `return-contract.yaml` | Run status (`success` / `partial` / `failed`), worker counts, output paths, recommended next command | same |

A stub `bare-review` run, for example, leaves 12 entries: the four observability files,
three `bare-review-0N-lens-default-model-0.final.md` + `.meta.json` pairs, `merged.md`
and `return-contract.yaml`.

**Not** emitted by a run: `done.json`. Only `swarm kill <job_id> --output <dir>` writes
it (with `terminal_status=killed`). (A missing proxy env contract fails the run at
transport construction with a clear `missing: …` diagnostic and exit `1`, writing only
`manifest.json` + `.swarm-state.json` — see
[User Guide §6c](user-guide.md#6c-if-the-env-is-missing).)

> **Resume mode.** `swarm run --resume` skips succeeded workers, re-dispatches the rest,
> re-runs Wave 2 normalize on them and Wave 3 reduce (`reduce_wave3(resume=True)`),
> regenerating `merged.md` and `return-contract.yaml`. See
> [User Guide §8](user-guide.md#8-resuming-a-partial-job) and
> [Command Ref → run artifacts](command-reference.md#run-artifacts).

The `--output` **flag** is what wires these artifacts. A spec-file run *without*
`--output` dispatches but writes nothing to disk.

---

## Two-minute smoke test

No network, no proxy — proves the CLI is wired and the dispatch path works:

```bash
# 1. Validate the bundled lens registry (expect: "registry OK (9 entries inspected, 8 validated)")
uv run superclaude swarm validate-lenses

# 2. Fan a deterministic stub review across 3 workers
printf 'def add(a, b):\n    return a - b  # off-by-sign bug for demonstration only\n' \
  > /tmp/swarm-demo.py
uv run superclaude swarm run \
  --lens bare-review --target /tmp/swarm-demo.py \
  --output /tmp/swarm-demo-out --transport stub

# 3. Inspect the result (expect: phase=terminal, exit 0)
uv run superclaude swarm status --output /tmp/swarm-demo-out
uv run superclaude swarm logs   --output /tmp/swarm-demo-out
```

Walk-through with expected output for each step: [User Guide](user-guide.md).

---

## Document map

| Doc | Audience | Scope |
|---|---|---|
| [user-guide.md](user-guide.md) | Operators, skill authors | Step-by-step examples across every use case. |
| [command-reference.md](command-reference.md) | Operators | Per-flag reference + exit codes for all 8 commands. |
| [lens-catalog.md](lens-catalog.md) | Skill authors | The 8 lenses, 6 recipes, custom-py loader, and how to author a lens. |
| [runbook.md](runbook.md) | Operators | Env mandate, Rich TUI dep, T2 proxy env, tmux modes. |
| [monitoring-patterns.md](monitoring-patterns.md) | CI / automation | Three ways to wait on a job. |
| [transport-limits.md](transport-limits.md) | Integrators | Phase-1 transport exclusions. |
| [release-notes-v1.md](release-notes-v1.md) | All | What shipped in v1; resume, inject-guard, custom-prompt migration. |
| [oq-resolutions.md](oq-resolutions.md) | Maintainers | Design rationale for INV-005/007, OQ-009/010. |

---

## Conventions used in these docs

- Commands are shown as `uv run superclaude swarm …` (the project-canonical form).
  A `VIRTUAL_ENV … will be ignored` warning on the first line is benign.
- **Stub transport** is used for every runnable example so you can copy-paste without a
  proxy. Swap `--transport stub` → `--transport openai_compat` (and set the env
  contract) to run for real.
- Exit codes follow a consistent convention: **0** success, **1** rule/contract failure,
  **2** usage error. Per-command specifics are in the [Command Reference](command-reference.md).
