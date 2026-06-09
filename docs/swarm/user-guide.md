# MultiModelSwarm — User Guide

A task-oriented walkthrough of `superclaude swarm`. Every runnable example uses the
**stub transport** (in-process, deterministic, no network) so you can copy-paste each
block and reproduce the shown output exactly. To run against real models, swap
`--transport stub` → `--transport openai_compat` and set the
[T2 proxy env contract](runbook.md#t2-proxy-env-contract-ac-017).

**Before you start**, skim [What a run emits today](README.md#what-a-run-emits-today):
`swarm run` currently performs preflight + dispatch and writes four observability
artifacts; the merged-output / return-contract writer is the pending M5 milestone.

> **Conventions.** A `VIRTUAL_ENV=… will be ignored` warning may appear as the first
> output line — it is harmless. Exit codes: **0** success, **1** rule/contract failure,
> **2** usage error.

**Contents**

1. [Quickstart: your first swarm (stub transport)](#1-quickstart-your-first-swarm-stub-transport)
2. [Validate the bundled lens registry](#2-validate-the-bundled-lens-registry)
3. [Scaffold → edit → validate → run a full JobSpec](#3-scaffold--edit--validate--run-a-full-jobspec)
4. [Choosing a lens for your task](#4-choosing-a-lens-for-your-task)
5. [Inspecting results: status, logs, manifest](#5-inspecting-results-status-logs-manifest)
6. [Running against a real model proxy](#6-running-against-a-real-model-proxy)
7. [Monitoring a long-running job](#7-monitoring-a-long-running-job)
8. [Resuming a partial job](#8-resuming-a-partial-job)
9. [Prompt-injection guard & custom prompts](#9-prompt-injection-guard--custom-prompts)
10. [Authoring a custom normalization recipe](#10-authoring-a-custom-normalization-recipe)
11. [Troubleshooting common errors](#11-troubleshooting-common-errors)

---

## 1. Quickstart: your first swarm (stub transport)

**Goal:** fan a review across 3 workers and see the result, with zero setup.

```bash
# A target worth reviewing (must be >=50 non-whitespace bytes — see §11).
cat > /tmp/quickstart.py <<'PY'
def calculate_total(items, tax_rate):
    subtotal = 0
    for item in items:
        subtotal = subtotal - item.price   # bug: should be +=
    return subtotal + subtotal * tax_rate
PY

uv run superclaude swarm run \
  --lens bare-review \
  --target /tmp/quickstart.py \
  --output /tmp/quickstart-out \
  --transport stub
```

**Expected output (last line is the contract stub):**

```text
⚡ Parallel Executor: Planning 3 tasks
...
✅ All tasks completed in 0.00s
swarm run: dispatched job (mode=lens, workers=3, results=3)
```

**Exit code:** `0`. **What landed on disk:**

```bash
ls -A /tmp/quickstart-out
# .swarm-state.json  execution-log.jsonl  execution-log.md  manifest.json
```

Those four files are the complete artifact set for a run today (the merged-output and
return-contract writer is the pending M5 milestone). `bare-review` defaults to **3
workers**; `--transport stub` means each worker returns a deterministic placeholder, so
this is safe to run anywhere.

> **Why `--lens`?** It's the shortcut input mode: it expands the named lens's defaults
> (prompt, recipe, worker count, line cap, hand-off template) into a full JobSpec for
> you, so a bare `--lens NAME --target … --output …` is preflight-valid with no spec
> file. The other three input modes — a positional spec file, `--stdin`, and `--resume`
> — are covered below.

---

## 2. Validate the bundled lens registry

**Goal:** confirm the 7 bundled lenses are internally consistent (a good first-run
sanity check and a useful CI gate).

```bash
uv run superclaude swarm validate-lenses
```

**Expected output / exit:**

```text
validate-lenses: registry OK (8 entries inspected, 7 validated)
```

Exit `0`. The registry has **8** entries; **7** are validated — the `custom` escape
hatch is intentionally skipped (its prompt body arrives at preflight from
`--custom-prompt-dir`, not the registry). Each lens passes six structural assertions
(file-ref resolves, recipe registered, suspect↔`{suspect_files}` coupling, name unique,
injection-guard substring present, normalizer strategy registered) — see the
[Lens Catalog](lens-catalog.md#the-lens-validator-6-assertions).

For a **non-blocking** CI advisory (emit diagnostics but exit 0 even on failure):

```bash
uv run superclaude swarm validate-lenses --warning-mode
```

---

## 3. Scaffold → edit → validate → run a full JobSpec

**Goal:** when you need to override defaults (worker count, models, recipe args,
truncation), author a full JobSpec instead of using the `--lens` shortcut.

### 3a. Scaffold a starter spec

```bash
uv run superclaude swarm scaffold --lens bare-review --output /tmp/job.json
```

```text
swarm scaffold: wrote starter spec for lens 'bare-review' to /tmp/job.json
```

The emitted spec is a fully-populated, schema-valid JobSpec. The only fields you **must**
fill before running are `target.path` and `output.dir` (both scaffolded as `""`). Model
IDs are `lens-default-model-<i>` placeholders that validate but never reach the wire
(transport defaults to `stub`). Omit `--output` to print the spec to stdout instead (handy
for piping straight into `validate`).

### 3b. Edit the spec

Fill in the target and output directory (any editor; shown here with `python3` for
reproducibility):

```bash
python3 - <<'PY'
import json
p = "/tmp/job.json"
d = json.load(open(p))
d["target"]["path"] = "/tmp/quickstart.py"
d["output"]["dir"]  = "/tmp/job-out"
d["workers"]["count"] = 2          # example override: fewer workers
json.dump(d, open(p, "w"), indent=2)
print("patched", p)
PY
```

### 3c. Validate before running

```bash
uv run superclaude swarm validate /tmp/job.json
```

```text
validate: /tmp/job.json OK
```

Exit `0`. A schema-invalid spec exits `1` with a per-rule diagnostic block on stderr; an
unreadable / non-JSON file exits `2`.

> **Gotcha:** `swarm validate` runs the **schema** layer only. The target-size floor
> (IMM-4, ≥50 non-whitespace bytes) is a **preflight** rule, not a schema rule — so a
> spec pointing at a tiny target *passes* `validate` but its `run` fails preflight (exit
> 1). See [§11](#11-troubleshooting-common-errors).

### 3d. Run the spec

```bash
uv run superclaude swarm run /tmp/job.json --output /tmp/job-out --transport stub
```

```text
swarm run: dispatched job (mode=spec-file, workers=2, results=2)
```

Note `mode=spec-file` and `workers=2` (your override). **Always pass `--output` on the
command line** — observability artifacts key off the `--output` flag, not the spec's
`output.dir`. A spec-file run without `--output` dispatches but writes nothing to disk.

---

## 4. Choosing a lens for your task

Each lens encodes a review intent, a worker count, a normalization recipe, and a
downstream hand-off command. Pick by what you're reviewing:

| You're reviewing… | Use lens | Output shape | Hands off to |
|---|---|---|---|
| Code, for any bug (broad, unscaffolded) | `bare-review` | findings table + verdict | `/sc:adversarial` |
| Code, for the smallest worthwhile cleanups | `refactor-find` | findings table | `/sc:code-review` |
| Code, for inputs/states that break it | `edge-case-hunt` (4 workers) | findings table | `/sc:adversarial` |
| A spec, for gaps / under-specification | `spec-completeness` | verdict + rationale | `/sc:reflect` |
| An approach, for whether it'll work | `feasibility-probe` | verdict + rationale | `/sc:research` |
| A failure, for ranked root-cause hypotheses | `troubleshoot-hypothesis` (4 workers) | hypothesis table | `/sc:troubleshoot` |
| Docs, for missing / stale content | `doc-completeness` | findings table | `/sc:document` |

Full per-lens detail (prompts, recipes, templates): [Lens Catalog](lens-catalog.md).

### Example: hunt edge cases (4-worker lens)

```bash
uv run superclaude swarm run \
  --lens edge-case-hunt \
  --target /tmp/quickstart.py \
  --output /tmp/edge-out --transport stub
```

```text
swarm run: dispatched job (mode=lens, workers=4, results=4)
```

`edge-case-hunt` and `troubleshoot-hypothesis` default to **4** workers (vs 3 for the
others) — broader divergence for harder search problems. You can always override with a
full spec (§3) or by editing `workers.count`.

### Example: spec-completeness on a design doc

```bash
uv run superclaude swarm run \
  --lens spec-completeness \
  --target docs/swarm/transport-limits.md \
  --output /tmp/spec-out --transport stub
```

```text
swarm run: dispatched job (mode=lens, workers=3, results=3)
```

This lens's recipe is `verdict_only_v1` — its workers emit a `## Verdict`
(`yes`/`no`/`uncertain`) + `## Rationale`, rather than a findings table.

---

## 5. Inspecting results: status, logs, manifest

After any run, three commands read the `--output` directory.

### Phase / status

```bash
uv run superclaude swarm status --output /tmp/quickstart-out
```

```text
status: phase=terminal job_id=lens-bare-review-xxxxxxxx updated=2026-06-09T00:18:03Z
```

Exit `0` for a non-terminal phase, terminal+success, or terminal with no readable
contract. (Once the M5 contract writer lands, terminal+partial/failed will exit `1`.) A
missing directory or corrupt state exits `2`. Pass `--job <job_id>` to assert you're
reading the directory you think you are — a mismatch fails loudly with exit `2`.

### Execution log

```bash
# Human-readable Markdown (default)
uv run superclaude swarm logs --output /tmp/quickstart-out

# Canonical JSONL (pipe into jq)
uv run superclaude swarm logs --output /tmp/quickstart-out --jsonl | jq -c 'select(.event_type=="worker_done")'
```

Markdown lines look like:

```text
- [2026-06-09T00:18:03.886Z] wave_transition worker=-: from=preflight_ok to=dispatching workers_requested=3
- [2026-06-09T00:18:03.887Z] worker_done worker=0: attempts=1 elapsed_ms=0 http_code=200 status=success
- [2026-06-09T00:18:03.887Z] wave_transition worker=-: from=dispatching results_collected=3 success_count=3 to=dispatched
```

The `.jsonl` and `.md` files carry the **same record stream** — `--jsonl` is for parsing,
`--md` (default) for humans. `--lines N` caps the dump; `--follow` / `--tail` live-tail
(see [§7](#7-monitoring-a-long-running-job)).

### Manifest (resume anchor)

```bash
jq '{job_id, transport:.preflight.transport_kind, workers:.preflight.workers_requested, lens:.resolved_lens_entry.name}' \
  /tmp/quickstart-out/manifest.json
```

```json
{ "job_id": "lens-bare-review-xxxxxxxx", "transport": "stub", "workers": 3, "lens": "bare-review" }
```

`manifest.json` is the **durable lens snapshot** — `--resume` rehydrates the job from it
verbatim (§8), so registry edits after the original run don't change a resumed run.

---

## 6. Running against a real model proxy

The stub transport proves wiring; `openai_compat` does real fan-out against an
OpenAI-compatible **T2 proxy**.

### 6a. Set the env contract

```bash
export T2ProxyUrl="https://your-proxy.example.com/v1"     # /chat/completions is appended
export T2ProxyKey="sk-..."                                 # sent as: Authorization: Bearer
export T2Model01="gpt-4o-mini"                             # one var per worker slot…
export T2Model02="claude-3-5-sonnet"                       # …slots are T2Model01..T2Model09
export T2Model03="qwen2.5-coder"
```

Model slots are read densely in order from `T2Model01`…`T2Model09` (max 9). Full
contract and resolution semantics: [Runbook](runbook.md#t2-proxy-env-contract-ac-017).

### 6b. Run

```bash
uv run superclaude swarm run \
  --lens bare-review --target /tmp/quickstart.py \
  --output /tmp/real-out --transport openai_compat
```

### 6c. If the env is missing

With `--transport openai_compat` and any required env piece unset, the run fails fast at
**transport construction** with a clear diagnostic on stderr and **exit 1**:

```text
swarm run: cannot construct 'openai_compat' transport -- T2 proxy env contract
incomplete; missing: T2ProxyUrl, T2ProxyKey, T2Model01..9. Set T2ProxyUrl, T2ProxyKey,
and at least one T2Model01..9 slot.
```

The `missing:` list names exactly what's absent (e.g. just `T2Model01..9` when the URL
and key are set but no model slots are). `manifest.json` and `.swarm-state.json` are
written; the execution log and a return contract are **not** (the transport is
constructed before dispatch, so the run never enters Wave 1). Fail-loud with a clear
message, not a crash.

> The internal **INV-007** empty-pool contract (`return-contract.yaml`,
> `status: failed`, `reason: env-missing`) is a *preflight* artifact for the empty
> model-pool case; the common `--lens … --transport openai_compat` route reports the
> transport-construction error above instead.
>
> Streaming, tool-calling, and vision are **not** supported in Phase 1 — see
> [Transport Limits](transport-limits.md). The payload is a single string-content user
> message with `model` / `messages` / `temperature`.

---

## 7. Monitoring a long-running job

Real proxy fan-outs take time. Three patterns (full detail:
[Monitoring Patterns](monitoring-patterns.md)).

### Pattern A — phase watch

```bash
uv run superclaude swarm run --lens bare-review --target BIG --output /tmp/j --transport openai_compat &
uv run superclaude swarm status --output /tmp/j --watch --watch-interval 2
```

`--watch` re-emits one grep-friendly status line every interval until the state reaches
`terminal`, then exits. Add `--watch-max-iterations N` to bound it (mainly a test lever).

### Pattern B — live-tail the event stream

```bash
uv run superclaude swarm logs --output /tmp/j --tail | jq -c 'select(.event_type=="worker_done")'
```

`--tail` is shorthand for `--jsonl --follow`: it live-tails the canonical JSONL surface
and exits when the job reaches terminal state.

### Pattern C — detached + done-sentinel poll

```bash
JOB=$(uv run superclaude swarm run --lens bare-review --target BIG \
        --output /tmp/j --transport openai_compat --detached)
# … later, re-attach the terminal to the tmux session:
uv run superclaude swarm attach "$JOB"
```

`--detached` launches the run inside a `tmux` session named `swarm-<job_id>`; `attach`
re-binds your terminal, `kill <job_id>` tears it down. tmux is **optional** — inline runs
never need it, and `--detached` without tmux exits `2` with a clear error rather than
silently falling back.

> **Today's caveat:** the `done.json` terminal sentinel and `status --watch`'s
> partial/failed exit codes depend on the **M5** Wave-2/3 terminal writer. The current
> dispatch-only path does **not** emit `done.json`, so the `until [ -f done.json ]`
> poll in [Monitoring Patterns](monitoring-patterns.md) describes the **target**
> behavior. For now, poll `.swarm-state.json` reaching `terminal` via `status`.

---

## 8. Resuming a partial job

If a proxy run dies mid-flight (network drop, partial worker set), `--resume` continues
from the manifest instead of re-running succeeded workers.

```bash
uv run superclaude swarm run --resume <JOB_ID> --output /tmp/j --transport openai_compat
```

What it does (`preflight.resume_mode`):

- Reads `manifest.json` from `--output` and rehydrates the JobSpec from the **lens
  snapshot** taken at the original Wave 0 (INV-001/INV-016: **verbatim** — the live lens
  registry is not consulted, so edits since the first run are ignored).
- Skips workers whose `*.meta.json` sidecar reports `status=success`; re-dispatches the
  rest.
- `--resume` is mutually exclusive with a spec path, `--stdin`, `--lens`, and
  `--detached`; `--output` is required.

To intentionally pick up registry changes (re-resolve prompts/recipe from the **current**
lens), add `--force-relens` (requires `--resume`):

```bash
uv run superclaude swarm run --resume <JOB_ID> --output /tmp/j --force-relens --transport openai_compat
```

The lens **name**, worker count, and transport kind still come from the manifest; only
the lens-derived *body* fields are re-resolved.

---

## 9. Prompt-injection guard & custom prompts

Every bundled lens already embeds the §11.5 injection-guard sentence in its system
prompt, and wraps the target between `<<<TARGET>>>` / `<<<END TARGET>>>` delimiters so a
malicious target can't smuggle instructions. You normally don't touch this.

It matters only when you supply **your own** prompts via the `custom` lens escape hatch:

```bash
uv run superclaude swarm run \
  --lens custom --custom-prompt-dir /path/to/prompts \
  --target /tmp/quickstart.py --output /tmp/c-out \
  --transport stub --auto-inject-guard
```

`--auto-inject-guard` prepends the canonical guard sentence to a legacy `system.txt`
that predates it, so the run passes the guard check. It is **idempotent** (no double
prepend) and **opt-in** — without it, a custom system prompt lacking the guard sentence
is rejected at preflight. It's redundant with the bundled lenses (they already carry the
sentence). Migration detail: [Release Notes → custom-prompt migration](release-notes-v1.md#custom-prompt-migration-path-fr-021-escape-hatch).

---

## 10. Authoring a custom normalization recipe

The six bundled recipes cover findings tables, hypothesis tables, verdict-only, and
passthrough. To normalize worker output into your own shape, use the **`custom-py`**
loader:

```text
normalization.recipe = "custom-py:my_pkg.recipes.priority:PriorityRecipe"
```

Grammar: `custom-py:<module>:<callable>` (the **last** colon separates the callable, so
the module path may itself contain colons). The callable must be either a zero-arg class
whose instances satisfy the `Recipe` protocol (`normalize(raw_output, args) ->
NormalizedResult`) or a pre-built Recipe object. Like every recipe, it must **normalize
only** — no scoring, deduping, or reordering (AC-011).

> **Trust boundary:** `custom-py` imports an arbitrary module with full host
> privileges. Treat the spec string as trusted, PR-reviewed input. Full contract and
> examples: [Lens Catalog → custom-py loader](lens-catalog.md#the-custom-py-loader).

---

## 11. Troubleshooting common errors

| Symptom | Cause | Fix |
|---|---|---|
| `preflight FAILED (1 rule(s))` / `imm4.target_too_small` (exit 1) | Target has <50 non-whitespace bytes after truncation. | Point at a real target. The output dir is **not** created on preflight failure. |
| `validate` passes but `run` fails preflight | `validate` is schema-only; IMM-4 / INV-005 / INV-007 are preflight rules. | Run `swarm run` to exercise preflight; don't treat `validate` as a full gate. |
| Unknown lens (exit 2) | Typo, or `--lens custom` to `scaffold` (no defaults to expand). | Use a registry name (`validate-lenses` lists them); for `custom`, supply `--custom-prompt-dir`. |
| `run` exits 0 but no files on disk | Spec-file mode without the `--output` **flag**. | Always pass `--output <dir>`; the flag (not `spec.output.dir`) wires artifacts. |
| `cannot construct 'openai_compat' transport … incomplete; missing: …` (exit 1) | `openai_compat` with `T2ProxyUrl` / `T2ProxyKey` / `T2Model0*` slots unset. | Export the [env contract](#6a-set-the-env-contract); the `missing:` list names exactly what's absent. |
| `--detached` exits 2 | tmux not installed / nested in tmux. | Install tmux, or run inline (no `--detached`). |
| No `merged.md` / `return-contract.yaml` / `done.json` after a normal run | Expected — those are the pending **M5** Wave-2/3 writer. | Use the four observability artifacts (§5); see [README](README.md#what-a-run-emits-today). |
| `VIRTUAL_ENV … will be ignored` warning | Benign uv/venv notice. | Ignore, or filter with `grep -v VIRTUAL_ENV`. |

See also the [Command Reference](command-reference.md) for per-command exit-code tables
and the [Runbook](runbook.md) for environment and TUI prerequisites.
