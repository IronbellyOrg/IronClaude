# MultiModelSwarm — Command Reference

Per-flag reference and exit codes for all eight `superclaude swarm` subcommands.
Generated against the live `--help` surface; run `uv run superclaude swarm <cmd> --help`
for the authoritative text in your installed version.

**Global exit-code convention:** `0` success · `1` rule/contract failure · `2` usage
error. Per-command specifics below.

**Contents:** [run](#swarm-run) · [scaffold](#swarm-scaffold) · [validate](#swarm-validate)
· [validate-lenses](#swarm-validate-lenses) · [status](#swarm-status) · [logs](#swarm-logs)
· [attach](#swarm-attach) · [kill](#swarm-kill) · [run artifacts](#run-artifacts)

---

## `swarm run`

```text
superclaude swarm run [OPTIONS] [SPEC_PATH]
```

Run a swarm job: **Wave 0 preflight → Wave 1 dispatch → Wave 2 normalize → Wave 3
reduce**. When `--output` is set and the spec names a normalization recipe (every bundled
lens does), the run writes the per-worker outputs, `merged.md` and
`return-contract.yaml` before it marks the job `terminal` — see
[README](README.md#what-a-run-emits) and [Run artifacts](#run-artifacts).

### Four mutually-exclusive input modes

| Mode | Invocation | Notes |
|---|---|---|
| Spec file | `swarm run path/to/job.json` | Positional `SPEC_PATH`; a JobSpec JSON file. |
| Stdin | `… --stdin < job.json` | Read the JobSpec JSON from stdin. |
| Lens shortcut | `… --lens NAME --target … --output …` | Expands the named lens's defaults into a full JobSpec. Requires `--target` and `--output`. `custom`/unknown names rejected (exit 2). |
| Resume | `… --resume JOB_ID --output DIR` | Rehydrate from `manifest.json`; skip succeeded workers. |

### Options

| Flag | Arg | Meaning |
|---|---|---|
| `--stdin` | — | Consume the JobSpec JSON document from stdin instead of a file. |
| `--lens` | TEXT | Shortcut: dispatch with the named lens, expanding its defaults (system/user prompts, recipe, worker count, line cap, next-command template). Requires `--target` + `--output`. |
| `--resume` | TEXT | Resume a prior job from its manifest (requires `--output` pointing at the original job dir). Skips workers whose `*.meta.json` reports `status=success`. Mutually exclusive with `SPEC_PATH` / `--stdin` / `--lens`. |
| `--target` | PATH | Override `target.path` on the resolved spec. Required with `--lens`. |
| `--output` | DIR | Output directory. **Wires all observability artifacts** — without it, a spec-file run dispatches but writes nothing. Required with `--lens` / `--resume`. |
| `--transport` | `stub`\|`openai_compat` | Override `transport.kind`. `stub` (default for `--lens`) = in-process, no network. `openai_compat` = real T2 proxy. Spec-file and `--stdin` runs use the spec's `transport.kind`; when the spec omits it the default is `openai_compat` (a scaffolded spec sets `stub`). |
| `--reviewers` | INT | B-1 override of the bare-review reviewer (worker) count. Integer in the inclusive range `[2, 4]` (legacy `t2_preflight.sh` AC-1.4 invariant). Omitted → lens default (3 for bare-review) preserved; `workers.models` is resized to match so the INV-005 model-pool guard admits the requested count. |
| `--target-line-cap` | INT | B-2 override of the target truncation line cap (legacy `t2_preflight.sh --target-line-cap`, default `4000`). Omitted → lens default (4000 for bare-review) preserved. Threads through to `target.truncation.line_cap`. |
| `--timeout-sec` | INT | B-3 override of the per-worker timeout in seconds (legacy `t2_preflight.sh --timeout-sec` / `T2Timeout`, default `180`). Omitted → 180s default preserved. Applied to `workers.timeout_sec` and threaded into dispatch via `worker_spec`. |
| `--label` | TEXT | B-4 override of the caller invocation label (legacy `t2_preflight.sh --label`), stamped onto per-reviewer output frontmatter via the recipe `caller_label`. Omitted → default `swarm-run-lens-<lens>` label preserved. |
| `--force-relens` | — | With `--resume`: re-resolve lens-derived prompt/recipe fields from the **current** registry (FR-025). Requires `--resume`. |
| `--detached` | — | Launch inside a `tmux` session `swarm-<job_id>` (FR-014). Mutually exclusive with `--resume` and `--tui`. Exits `2` if tmux is unavailable — no silent inline fallback. |
| `--tui` | — | Render a live Rich progress dashboard while Wave 1 dispatch runs. Fresh runs only (not with `--resume`); needs a TTY (on a non-TTY pipe it silently runs the plain synchronous path); mutually exclusive with `--detached`. Ctrl-C during the dashboard exits `130`. |
| `--auto-inject-guard` | — | Prepend the canonical §11.5 injection-guard sentence to the `system.txt` in the `custom_prompt_dir` directory when it lacks it (idempotent, opt-in; the file on disk is not rewritten). Relevant only when migrating legacy custom prompt directories that predate §11.5 framing. |

> **Note — the custom prompt directory is not a `run` flag.** It is the JobSpec
> `custom_prompt_dir` field (FR-021), authored in a spec file with `"lens": "custom"`
> (`custom_prompt_dir` requires the `custom` lens — see [`swarm validate`](#swarm-validate)).
> The directory must hold `system.txt`, `user.txt` and `meta.yaml`. It is **not** a
> `swarm run` CLI option; only `--auto-inject-guard` (above) is the run-time flag
> that interacts with the `custom_prompt_dir` `system.txt`.

### Exit codes

| Code | Condition |
|---|---|
| `0` | Job ran to `terminal` (stub or proxy). stdout ends `swarm run: dispatched job (mode=…, workers=N, results=N)`. The run status (`success` / `partial` / `failed`) is in `return-contract.yaml`; read it with [`swarm status`](#swarm-status). |
| `1` | Preflight failed (e.g. `imm4.target_too_small`; `inv007.env_missing`). Structured rule block on stderr. Output dir **not** created on IMM-4 failure. |
| `2` | Usage error (unknown lens, conflicting input modes, `--detached` without tmux). |
| `130` | Interrupted with Ctrl-C during a `--tui` run (the terminal is restored and the dispatch thread drained first). |

### Examples

```bash
# Lens shortcut (stub)
superclaude swarm run --lens bare-review --target src/foo.py --output out --transport stub

# Full spec file
superclaude swarm run job.json --output out --transport stub

# From stdin
superclaude swarm scaffold --lens refactor-find | superclaude swarm run --stdin --target src/foo.py --output out

# Resume
superclaude swarm run --resume lens-bare-review-ab12cd34 --output out --transport openai_compat
```

---

## `swarm scaffold`

```text
superclaude swarm scaffold --lens NAME [-o/--output FILE]
```

Emit a fully-populated, schema-valid starter JobSpec for `NAME` (FR-006). The only
fields you must override before running are `target.path` and `output.dir` (both `""`).
Model IDs are `lens-default-model-<i>` placeholders that validate but never reach the
wire.

| Flag | Arg | Meaning |
|---|---|---|
| `--lens` | TEXT (**required**) | Lens to scaffold. `custom` and unknown names are rejected (custom has no registry defaults to expand). |
| `-o`, `--output` | FILE | Write the spec atomically to PATH. Omitted → print to stdout (pipe into `validate` / `run --stdin`). |

**Exit:** `0` rendered · `2` unknown/`custom` lens, or unwritable `--output`.

```bash
superclaude swarm scaffold --lens bare-review --output job.json
superclaude swarm scaffold --lens spec-completeness | superclaude swarm validate -
```

---

## `swarm validate`

```text
superclaude swarm validate [--strict] JOBSPEC_PATH
```

Schema-check a JobSpec JSON file (FR-007) — the DM-001 JSON-Schema **plus** cross-field
rules (spec-version pin, injection-guard substring, `custom_prompt_dir` requires
`custom` lens).

| Flag | Meaning |
|---|---|
| `--strict` | Reserved for future stricter rule sets. **Currently a no-op** — the bundled schema is already strict. |

**Exit:** `0` valid (stdout `validate: <path> OK`) · `1` schema-invalid (per-rule
diagnostic block on stderr) · `2` file unreadable / not valid JSON.

> **Scope:** schema layer only. The target-size floor (IMM-4), empty-pool (INV-005), and
> env-missing (INV-007) rules are **preflight** checks, not schema checks — a spec can
> pass `validate` and still fail `run` preflight.

---

## `swarm validate-lenses`

```text
superclaude swarm validate-lenses [--warning-mode]
```

Validate the bundled `LENSES` registry (FR-008): six structural assertions per entry
over every **non-`custom`** lens. The registry has 9 entries: the 8 bundled lenses
(`bare-review`, `refactor-find`, `edge-case-hunt`, `spec-completeness`,
`feasibility-probe`, `troubleshoot-hypothesis`, `doc-completeness`, `reflect-review`)
plus the unvalidated `custom` escape hatch.

| Flag | Meaning |
|---|---|
| `--warning-mode` | Emit per-entry diagnostics on stderr but exit `0` even on failure. For pre-commit / non-blocking CI advisories. Default is blocking. |

**Exit:** `0` all pass (stdout `validate-lenses: registry OK (9 entries inspected, 8
validated)`), or any mode with `--warning-mode` · `1` ≥1 entry failed (default blocking)
· `2` reserved.

---

## `swarm status`

```text
superclaude swarm status --output DIR [--job ID] [--watch …]
```

Report a job's wave phase from `<DIR>/.swarm-state.json` (FR-002). Phases:
`preflight_ok` → `dispatching` → `normalizing` → `reducing` → `terminal`.

| Flag | Arg | Meaning |
|---|---|---|
| `--output` | DIR (**required**) | Directory containing `.swarm-state.json`. |
| `--job` | TEXT | Verify against the state file's recorded `job_id`; mismatch → exit `2` (guards wrong-directory invocations). |
| `--watch` | — | Poll on an interval, re-emitting the status line until `terminal` (or Ctrl-C). One grep-friendly line per poll. |
| `--watch-interval` | FLOAT | Seconds between polls. Default `2.0` (min `0.01`). |
| `--watch-max-iterations` | INT | Optional ceiling on polls (mainly a test lever). |

**Exit:** `0` non-terminal phase, OR terminal+success, OR terminal with unreadable
contract (status unknown) · `1` terminal+partial or terminal+failed (as recorded in
`return-contract.yaml`) · `2` usage error (dir/state missing, corrupt JSON, `--job`
mismatch).

On a terminal job with a readable contract the line ends with `terminal_status=`:

```text
status: phase=terminal job_id=lens-bare-review-ab12cd34 updated=2026-06-09T00:18:03Z terminal_status=success
```

---

## `swarm logs`

```text
superclaude swarm logs --output DIR [--jsonl|--md] [--follow|--tail] [--lines N]
```

Dump or tail a job's execution log (FR-003). `execution-log.md` (default) and
`execution-log.jsonl` share the same record stream — the choice is cosmetic; use
`--jsonl` to pipe into `jq`.

| Flag | Arg | Meaning |
|---|---|---|
| `--output` | DIR (**required**) | Directory containing `execution-log.{jsonl,md}`. |
| `--job` | TEXT | Verify against `.swarm-state.json`'s `job_id` (missing state tolerated). |
| `--jsonl` / `--md` | — | JSONL machine surface vs Markdown human surface. Default `--md`. |
| `-f`, `--follow` | — | Live-tail: poll on `--watch-interval` until terminal / Ctrl-C. |
| `--tail` | — | Shorthand for `--jsonl --follow`. |
| `--lines` | INT | Show only the last N lines (dump and follow-seed). |
| `--watch-interval` | FLOAT | Seconds between polls under `--follow`/`--tail`. Default `0.5` (min `0.01`). |
| `--watch-max-iterations` | INT | Optional poll ceiling (test lever). |

**Exit:** `0` read OK / follow exited cleanly · `2` usage error (`--output` missing, log
file missing, `--job` mismatch).

---

## `swarm attach`

```text
superclaude swarm attach JOB_ID
```

Re-attach your terminal to a detached `swarm-<JOB_ID>` tmux session (FR-004). Blocks
until you detach (Ctrl-b d) or the session ends. No options.

**Exit:** `0` attached+detached cleanly, OR no live session for `JOB_ID` (graceful no-op
so poll wrappers don't error) · non-zero propagated from tmux on its own failure · `2`
tmux not installed, caller already nested in tmux, or `JOB_ID` has tmux-illegal
characters.

---

## `swarm kill`

```text
superclaude swarm kill JOB_ID [--output DIR]
```

Terminate a detached `swarm-<JOB_ID>` tmux session (FR-005). Idempotent — killing an
already-terminated job is a clean no-op.

| Flag | Arg | Meaning |
|---|---|---|
| `--output` | DIR | When supplied, also flips `<DIR>/.swarm-state.json` to `terminal` and writes `done.json` with `terminal_status=killed`, so polling consumers observe the termination. Omitted → only the tmux session is torn down. |

**Exit:** `0` terminated cleanly OR no live session present · `2` usage error (tmux
missing, nested tmux, illegal `JOB_ID`, or `--output` not a directory).

---

## Run artifacts

After a successful **fresh** `swarm run … --output <DIR>` (stub or proxy), `<DIR>`
contains the four observability files, the per-worker outputs, `merged.md` and
`return-contract.yaml`:

| File | Format | Key fields |
|---|---|---|
| `.swarm-state.json` | JSON | `state` (`preflight_ok`…`terminal`), `job_id`, `updated` (ISO-8601 `Z`). Flipped to `terminal` only after Wave 3 has written the contract. |
| `execution-log.jsonl` | JSONL | One record/line: `event_type` (`wave_transition`/`worker_start`/`worker_progress`/`worker_done`/`terminal`), `timestamp`, `worker_index` (int or null), `payload` (free-form). |
| `execution-log.md` | Markdown | `- [<ts>] <event_type> worker=<i\|->: <k=v …>` — same stream, human-rendered. |
| `manifest.json` | JSON | `contract_version`, `job_id`, `resolved_lens_entry` (durable lens snapshot), `preflight` (`target_checksum` / `workers_requested` / `transport_kind`), `caller_metadata` (`suspect` / `tier`). |
| `<lens>-NN-<model>.final.md` | Markdown | One normalized worker output per worker (Wave 2 recipe output). |
| `<lens>-NN-<model>.meta.json` | JSON | Per-worker sidecar; `--resume` skips workers whose sidecar reports `status=success`. |
| `merged.md` | Markdown | Wave 3 merge of the worker outputs; written when `amalgamation_mode` is `normalize+merge` (the default for every bundled lens). |
| `return-contract.yaml` | YAML | `status` (`success`/`partial`/`failed`), `job_id`, `lens`, `workers_requested` / `workers_succeeded` / `workers_failed`, `output_files` (per-worker paths), recommended next command. |

**Not** emitted by a run: `done.json`. Only [`swarm kill JOB_ID --output DIR`](#swarm-kill)
writes it (with `terminal_status=killed`). Preflight also writes `return-contract.yaml`
(`status: failed`, `reason: env-missing`) on the INV-007 env-missing path.

**`--resume`** re-dispatches only the workers that did not succeed, re-runs Wave 2
normalize on them and Wave 3 reduce (`reduce_wave3(resume=True)`), regenerating
`merged.md` and `return-contract.yaml`.

Full schemas: [Lens Catalog](lens-catalog.md) and the dataclass definitions in
`cli/swarm/models.py`.

> `.swarm-state.json` is a dotfile — `ls` hides it; use `ls -A`.
