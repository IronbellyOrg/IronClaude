# MultiModelSwarm — Documentation Index

`superclaude swarm` fans a single prompt across **N heterogeneous OpenAI-compatible
workers**, normalizes each worker's output through a **lens recipe**, and (in the
full pipeline) amalgamates the results into a caller-facing **ResultContract**. It is
the CLI substrate behind the multi-model review/troubleshoot/spec workflows.

> **Implementation status (read this first).** As of this writing `swarm run` executes
> **Wave 0 preflight + Wave 1 dispatch** and writes the observability artifacts
> (`execution-log.{jsonl,md}`, `manifest.json`, `.swarm-state.json`). The **Wave 2/3
> amalgamation writer** — `merged.md`, `return-contract.yaml`, and the `done.json`
> terminal sentinel on the success path — is the **M5 milestone and is not yet wired
> into the run path**. Where a doc describes merged output or the return contract, it is
> describing the **target contract**; this index calls out what a run emits *today*.
> See [What a run emits today](#what-a-run-emits-today).

---

## Start here

| If you want to… | Read |
|---|---|
| **Be guided through swarm in plain language (no jargon)** | [**Swarm Wizard Guide** (`/sc:swarm-wizard`)](wizard-guide.md) |
| Run your first swarm in 2 minutes | [User Guide → Quickstart](user-guide.md#1-quickstart-your-first-swarm-stub-transport) |
| Step-by-step worked examples across use cases | [**User Guide**](user-guide.md) |
| Look up a command's flags and exit codes | [**Command Reference**](command-reference.md) |
| Understand the 7 lenses and 6 recipes | [**Lens & Recipe Catalog**](lens-catalog.md) |
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
| `run` | Run a job (Wave 0 preflight → Wave 1 dispatch). | [ref](command-reference.md#swarm-run) |
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
| `custom` | — | (escape hatch) | — | — | `--custom-prompt-dir` |

> The registry has **8 entries**; `validate-lenses` validates **7** (the `custom`
> escape hatch is intentionally skipped — its prompt body flows in from
> `--custom-prompt-dir` at preflight).

---

## Transports

| Transport | Network? | Use when |
|---|---|---|
| `stub` | **No** — in-process, deterministic | CI, tests, docs, dry-runs, quick-dispatch (the default for `--lens` and `scaffold`). |
| `openai_compat` | Yes — httpx → `<base_url>/chat/completions` | Real fan-out against the T2 proxy. Requires the [env contract](runbook.md#t2-proxy-env-contract-ac-017). |

Phase-1 **excludes** streaming, function-calling/tool-use, and vision input — see
[Transport Limits](transport-limits.md).

---

## What a run emits today

After a successful **fresh** `swarm run ... --output <dir>` (stub or proxy — i.e. *not*
`--resume`), `<dir>` contains **exactly four** files:

| File | Shape | Doc |
|---|---|---|
| `execution-log.jsonl` | One JSON event per line (machine surface) | [Command Ref → logs](command-reference.md#swarm-logs) |
| `execution-log.md` | Human-readable mirror of the same stream | same |
| `manifest.json` | Lens snapshot + preflight summary + caller metadata (resume anchor) | [Command Ref → run artifacts](command-reference.md#run-artifacts) |
| `.swarm-state.json` | Coarse wave phase (`preflight_ok`…`terminal`) | [Command Ref → status](command-reference.md#swarm-status) |

**Not** emitted by the fresh run path: `merged.md`, `return-contract.yaml`,
`done.json`, and the per-worker `*.md` / `*.meta.json` outputs — the fresh path is
dispatch-only (Wave 0 + Wave 1), so the Wave 2/3 amalgamation writer (**M5**) is not yet
wired into it. (A missing proxy env contract fails the run at transport construction with
a clear `missing: …` diagnostic and exit `1`, writing only `manifest.json` +
`.swarm-state.json` — see [User Guide §6c](user-guide.md#6c-if-the-env-is-missing).)

> **Resume mode is different.** `swarm run --resume` re-runs **Wave 2 normalize +
> Wave 3 reduce** (`reduce_wave3`), so a resumed job's `<dir>` *additionally* contains
> `return-contract.yaml` and `done.json`, plus **`merged.md` when
> `amalgamation_mode == normalize+merge`** and the per-worker normalized outputs. The
> four-file set above is the **fresh-run** contract only. See
> [User Guide §8](user-guide.md#8-resuming-a-partial-job) and
> [Command Ref → run artifacts](command-reference.md#run-artifacts).

The `--output` **flag** is what wires these artifacts. A spec-file run *without*
`--output` dispatches but writes nothing to disk.

---

## Two-minute smoke test

No network, no proxy — proves the CLI is wired and the dispatch path works:

```bash
# 1. Validate the bundled lens registry (expect: "registry OK (8 ... 7 validated)")
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
| [lens-catalog.md](lens-catalog.md) | Skill authors | The 7 lenses, 6 recipes, custom-py loader, and how to author a lens. |
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
