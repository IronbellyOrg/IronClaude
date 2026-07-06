<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (CLI) — `.dev/brainstorms/20260529-multimodel-swarm-CLI/merged-requirements.md` -->
<!-- Incorporated: Variant 2 (SKILL) §13 lens registry, §5.5 mechanical-merge mode, §6.1 manifest snapshot, §12 consolidated Will/Will-Not, §13.1 lens validator, §18 mechanism-vs-policy framing -->



---
spec_id: SPEC-MULTIMODEL-SWARM
spec_version: 1.0.0-merged
status: adversarial-merge
date: 2026-05-29
sources:
  - .dev/brainstorms/20260529-multimodel-swarm-CLI/merged-requirements.md (v0.1.0-draft, base)
  - .dev/brainstorms/20260529-multimodel-swarm-SKILL/merged-requirements.md (v1.0.0-draft, incorporated)
debate_artifacts:
  - .dev/brainstorms/20260529-multimodel-swarm-COMPARE/adversarial/diff-analysis.md
  - .dev/brainstorms/20260529-multimodel-swarm-COMPARE/adversarial/debate-transcript.md
  - .dev/brainstorms/20260529-multimodel-swarm-COMPARE/adversarial/invariant-probe.md
  - .dev/brainstorms/20260529-multimodel-swarm-COMPARE/adversarial/base-selection.md
  - .dev/brainstorms/20260529-multimodel-swarm-COMPARE/adversarial/refactor-plan.md
  - .dev/brainstorms/20260529-multimodel-swarm-COMPARE/adversarial/merge-log.md
parent_spec: .dev/brainstorms/20260528030000-t2-bare-reviewer-adjunct/merged-requirements.md (v1.3.0-draft — bare-review)
convergence_score: 0.73 (raw) / 0.85+ (effective per advocate concession alignment)
unresolved_conflicts: 0
unaddressed_invariants: 0 (all 6 HIGH+UNADDRESSED items resolved by refactor plan)
scope: cross-cutting
  - new CLI verb `superclaude swarm` at src/superclaude/cli/swarm/
  - bundled lens registry at cli/swarm/lenses/ with 7 initial entries
  - new Recipe Protocol + open-class custom-py: normalizer plug-in
  - three amalgamation modes (raw | normalize | normalize+merge) with structural guards
  - migration of sc-bare-review SKILL.md + scripts/*.sh to a 60-line thin caller
forbidden_topics:
  - openharness / openhands integration  # verified non-precluding (§13); not designed for
---



# Multi-Model Parallel-Swarm Orchestrator — Merged Design Spec

> *"Mechanism in the orchestrator. Policy in the lens. Caller picks the lens, supplies the target, consumes the contract."*


## 1. Motivation & Framing

### 1.1 The mechanism / policy / caller split



The merged design is best understood as three concentric layers, each with a single owner:

- **Mechanism** (owned by the `superclaude swarm` orchestrator): parallel dispatch with code-enforced concurrency, target ingestion, IMM-3/IMM-4/IMM-5/IMM-6 invariant enforcement, §11.5 injection-guard enforcement, per-worker isolation, status determination, normalizer dispatch, durable observability.
- **Policy** (owned by the lens registry + the Recipe Protocol): which prompts to send, which output template to expect, which normalizer to run, whether outputs are suspect-by-construction, what tier label to apply, what downstream command to recommend.
- **Caller** (the parent skill / command / process): picks the lens (or supplies own prompts), hands target + output dir + worker count, consumes the structured return contract, decides whether to invoke the recommended next command.

This framing replaces V1's "skill vs CLI" sibling-comparison narrative with a positive architectural separation. The CLI is the orchestrator's home because mechanism wants code-enforcement; the lens registry lives inside the CLI package because policy wants bundled-vetted-distribution; the caller is anyone with `subprocess.run`.

### 1.2 What this design preserves from the parent spec

Every IMM-N invariant from bare-review v1.3.0-draft is preserved verbatim or strengthened:

- **IMM-3 (true-parallel dispatch).** Strengthened. ThreadPoolExecutor + a single ParallelGroup replaces the parent's "single message, N tool calls" structural assertion. The CLI is invoked as one Bash call by Claude (or one `subprocess.run` by any process); parallelism happens inside the Python process and is therefore code-enforced rather than attention-mediated.
- **IMM-4 (empty-target guard).** Preserved. Target with <50 non-whitespace bytes after truncation → write `failed`/`target-too-small` contract and STOP before any dispatch.
- **IMM-5 (success-first status determination).** Preserved. `M == N` → `success` first; `2 ≤ M < N` → `partial`; `M < 2` → `failed`. The `M == N == 2` edge resolves to `success`. The floor and success-first ordering are per-job configurable but default to (floor=2, success_first=true).
- **IMM-6 (atomic-write idempotency).** Preserved. Every output file via write-to-tmp + `os.replace` + deterministic filename.
- **§11.5 (prompt-injection guard).** Strengthened. Target wrapped in `<<<TARGET>>>` / `<<<END TARGET>>>` delimiters; system-prompt explicitly states data-vs-instructions separation. Enforcement extended to three prompt-input paths (Change #11): JSON Schema required-substring on `prompt.system`, lens registry validator at PR time, `--custom-prompt-dir` preflight substring check (closing INV-003/INV-014 invariant gaps).

### 1.3 What is explicitly out of scope



- Integration of openharness, openhands, OpenAI Assistants SDK, LangGraph, CrewAI, or any third-party agent harness. The job-spec / result-contract / monitoring contract is *non-precluding* for future integration (§13), but designing for them is out of scope here.
- Streaming, function-calling, vision input. Phase 1 of the parent spec excludes these (§7.3); inherited.
- A new merge/diff/scoring engine. `/sc:adversarial` remains the scored-merge pipeline; `normalize+merge` mode is **mechanical concat only** (structurally guarded; §5.5).
- The suspect-tag, evidence-validator, or `/sc:adversarial` extensions covered by Phases 2-5 of the parent spec — those are caller / downstream concerns.

### 1.4 Why the CLI layer (not a SKILL.md)

The architectural fork was decided in the adversarial debate (`debate-transcript.md`). Both advocates' R2 closings converged on the same hybrid: CLI orchestrator home + bundled lens registry inside. The CLI placement is decisive on three axes: (a) ThreadPoolExecutor enforces parallelism in code where SKILL.md prose cannot, (b) `subprocess.run` callability extends naturally to non-Claude callers under A-001 stress, (c) durable observability + detached + resume affordances are first-class. The SKILL placement loses these without compensating wins; its policy-curation advantage is achievable as a bundled lens registry inside the CLI package (§3).


## 2. Architecture Overview



```
┌──────────────────────────────────────────────────────────────────────┐
│  CALLER (skill / human / future-harness)                             │
│                                                                      │
│  1. Build a job spec from either:                                    │
│     (a) --lens <name>            — registry-driven defaults          │
│     (b) caller-supplied prompts  — JSON Schema validated             │
│     (c) --custom-prompt-dir      — escape hatch with guard parity    │
│  2. Invoke:  superclaude swarm run <spec.yaml>                       │
│  3. Monitor: tail execution-log.jsonl  OR  poll swarm status         │
│  4. Read return-contract.yaml when status reaches terminal state     │
└────────┬─────────────────────────────────────────────────────────────┘
         │ (process boundary — pure CLI in, files out)
         ▼
┌──────────────────────────────────────────────────────────────────────┐
│  superclaude swarm run                                               │
│  ─────────────────────────────────────────────────────────────────── │
│  Wave 0 — Preflight                                                  │
│    • Validate job spec (JSON Schema + cross-field rules + §11.5      │
│      required-substring rule on prompt.system)                       │
│    • Resolve --lens against cli/swarm/lenses/ registry; materialize  │
│      resolved_lens_entry into manifest.json                          │
│    • Resolve env (T2ProxyUrl / T2ProxyKey / T2Model0N defaults)      │
│    • Read + truncate target; checksum; IMM-4 empty-target guard      │
│    • Build prompts (with §11.5 injection-guard delimiters)           │
│    • Emit manifest.json + .swarm-state.json (state=preflight_ok)     │
│                                                                      │
│  Wave 1 — Parallel dispatch                                          │
│    • ParallelExecutor (ThreadPoolExecutor): 1 task per worker,       │
│      1 ParallelGroup                                                 │
│    • Each task: httpx POST → write .raw + .meta.json sidecar         │
│    • Per-worker hard timeout; retry-once-on-5xx; always-record       │
│    • Event log: worker_start / worker_progress / worker_done         │
│                                                                      │
│  Wave 2 — Normalize                                                  │
│    • For each worker: invoke configured Recipe                       │
│    • Atomic write to deterministic final path (IMM-6)                │
│    • Promote parse_error → success if §7.4 salvage succeeds          │
│                                                                      │
│  Wave 3 — Reduce + (optional) merge                                  │
│    • IMM-5 success-first: M==N→success / 2≤M<N→partial / M<2→failed  │
│    • If amalgamation_mode == normalize+merge:                        │
│        run swarm/merge.py (≤30 LOC; mechanical concat ONLY)          │
│    • Write return-contract.yaml                                      │
│    • Write done.json sentinel (atomic)                               │
│    • Emit final event; exit 0 (status lives in contract, not RC)     │
└──────────────────────────────────────────────────────────────────────┘
```

### 2.1 Module layout

<!-- Source: V1 §2.2 + lens registry from V2 §13 (refactor plan Change #1, #5, #8) -->

```
src/superclaude/cli/swarm/
├── __init__.py               # exports swarm_group
├── commands.py               # Click subcommands: run, status, logs, attach, kill, scaffold, validate, validate-lenses
├── config.py                 # SwarmConfig dataclass; path resolution
├── models.py                 # JobSpec, WorkerSpec, ResultContract, WorkerResult, SwarmState, EventRecord
├── schema.py                 # JSON Schema for job spec; cross-field validators; §11.5 required-substring rule
├── preflight.py              # Wave 0; lens resolution + materialization; custom-prompt-dir guard parity (INV-003)
├── dispatch.py               # Wave 1 (httpx ThreadPoolExecutor via execution.parallel.ParallelExecutor)
├── normalize.py              # Wave 2 dispatcher + Recipe Protocol + recipe registry
├── reduce.py                 # Wave 3 (status determination + resume merge regen INV-010)
├── merge.py                  # NEW: mechanical concat only; ≤30 LOC; PR-review-discipline guarded
├── state.py                  # .swarm-state.json read/write (atomic)
├── logging_.py               # dual JSONL + Markdown event log
├── tui.py                    # Rich Live dashboard (flag-gated --tui, NOT default — INV-012)
├── tmux.py                   # detached-run wrapper (mirrors sprint/tmux.py)
├── recipes/                  # NORMALIZER REGISTRY (open-class)
│   ├── __init__.py           # Recipe Protocol + REGISTRY dict; custom-py: loader
│   ├── bare_review_v1.py     # ports t2_normalize.py logic
│   ├── findings_table_v1.py  # extracted shape for findings-table lenses
│   ├── hypothesis_table_v1.py
│   ├── verdict_only_v1.py
│   ├── passthrough.py
│   └── custom.py             # custom-py:module:func dynamic loader
├── lenses/                   # NEW: LENS REGISTRY (bundled policy)
│   ├── __init__.py           # LENSES dict + LensEntry dataclass + helpers
│   ├── _validate.py          # validator covering: file refs, recipe resolution, suspect→suspect_files coupling, name uniqueness
│   ├── bare_review.py        # lens entry: bare-review (stable; suspect:true; tier:T2)
│   ├── refactor_find.py      # lens entry (experimental; tier:T2-code)
│   ├── edge_case_hunt.py     # lens entry (experimental; tier:T2-edge)
│   ├── spec_completeness.py  # lens entry (experimental; tier:T2-spec)
│   ├── feasibility_probe.py  # lens entry (experimental; tier:T2-feas)
│   ├── troubleshoot_hypothesis.py
│   └── doc_completeness.py   # lens entry (experimental; tier:T2-doc)
└── transports/
    ├── __init__.py           # Transport Protocol
    ├── openai_compat.py      # httpx implementation (Phase-1 reference transport)
    └── stub.py               # deterministic stub for tests
```

This module shape mirrors `src/superclaude/cli/sprint/` so operators who know sprint already know swarm.


## 3. Lens Registry (V2's signature contribution, hosted in V1)

<!-- Source: V2 §13 (lens registry concept + initial 7-entry set) + V1's package-as-Python-module form (refactor plan Change #1, Reject #3) -->

### 3.1 Why a bundled registry

The job-spec schema (§4) accepts caller-supplied `prompt.system` / `prompt.user_template` / `normalization.recipe` / `output.filename_template` etc. Without a registry, every caller writes these from scratch — reproducing the drift problem V1 §1.1 identified: every implementation gets its own injection-guard idiom, its own normalizer choice, its own status-determination semantics.

The lens registry is the vetted shortcut. A caller invokes `superclaude swarm run --lens bare-review --target X --output Y --workers 3` and the registry expands the lens entry's defaults into a full job spec at preflight time. The caller-supplied path remains available (and is required when no lens fits); the registry serves the common cases.

### 3.2 `LensEntry` schema

```python
# cli/swarm/lenses/__init__.py
@dataclass(frozen=True)
class LensEntry:
    name: str                                  # kebab-case unique identifier
    description: str                           # one-line use case
    system_prompt_fragment: str                # verbatim system-prompt content
    user_template: str                         # user-prompt template with {target_content} placeholder
    output_template_path: str | None           # abs path to refs/templates/<lens>-output.md, or None
    recipe_name: str                           # Recipe Protocol name (built-in or 'custom-py:mod:func')
    default_workers: int                       # 2-4
    default_target_line_cap: int               # 4000 default
    suspect: bool                              # by-construction-suspect framing
    tier: str                                  # short label (e.g., 'T2', 'T2-code', 'T2-spec')
    recommended_next_command_template: str     # with {compare_files} + optional {suspect_files}
    acceptance_notes: str                      # free-form PR-review notes
    stability: Literal["stable", "experimental"] = "experimental"
```

### 3.3 Initial 8-entry registry

|Name|Use case|Default workers|Suspect|Tier|Stability|Next-cmd template|
|------|----------|----------------:|---------|------|-----------|-------------------|
|`bare-review`|Unscaffolded native-instinct review (`sc-bare-review`'s lens)|3|true|T2|**stable**|`/sc:adversarial --compare {compare_files} --suspect-source {suspect_files}`|
|`refactor-find`|"Smallest cleanups that improve correctness, readability, efficiency"|3|false|T2-code|experimental|`/sc:code-review --apply {compare_files}`|
|`edge-case-hunt`|"What inputs / states break this?"|4|false|T2-edge|experimental|`/sc:adversarial --compare {compare_files}`|
|`spec-completeness`|"What's missing or under-specified in this spec?"|3|false|T2-spec|experimental|`/sc:reflect --merge {compare_files}`|
|`feasibility-probe`|"Would this approach actually work?"|3|false|T2-feas|experimental|`/sc:research --extend {compare_files}`|
|`troubleshoot-hypothesis`|"Given this failure, what's the most likely root cause?"|4|false|T2-tshoot|experimental|`/sc:troubleshoot --merge-hypotheses {compare_files}`|
|`doc-completeness`|"What's missing, unclear, or out-of-date in this doc?"|3|false|T2-doc|experimental|`/sc:document --apply {compare_files}`|
|`custom`|Power-user escape hatch — caller supplies own prompts via `--custom-prompt-dir`|(caller)|(caller)|(caller)|n/a|(caller)|

Entries beyond `bare-review` ship at `experimental` stability and are promoted to `stable` after a real caller wires the lens in production.

### 3.4 PR-review discipline

A new lens entry is a PR against `cli/swarm/lenses/<name>.py` + (if needed) `refs/templates/<name>-output.md`. PR reviewers verify per V2 §13.2:

- The lens has a real caller (not speculative).
- The prompt fragment includes the §11.5 injection-guard sentence (also enforced by `validate-lenses` subcommand).
- The `normalizer_strategy` matches the prompt's expected output shape.
- The `recommended_next_command_template` references a real downstream command/skill.
- `suspect: true` lenses get extra scrutiny: only by-construction-suspect lenses should declare this.

### 3.5 Registry validator (`swarm validate-lenses`)

<!-- Source: V2 §13.1 / U-008 — refactor plan Change #8 -->

The validator iterates `LENSES`, asserts each entry's references resolve, asserts `recipe_name` is a registered Recipe (including `custom-py:` dynamic resolution), asserts `suspect: true` entries include `{suspect_files}` in their next-cmd template, asserts name uniqueness, asserts `system_prompt_fragment` contains the §11.5 substring. Hookable via `make verify-sync` and pre-commit.

### 3.6 Materialization into manifest (`resolved_lens_entry`)

<!-- Source: V2 §6.1 — refactor plan Change #3 -->

At preflight (Wave 0), the resolved lens entry is captured as a snapshot into `manifest.json`:

```json
{
  "contract_version": "1.0",
  "job_id": "2026-05-29T18-22-04Z-bare-review-7f3a",
  "resolved_lens_entry": {
    "name": "bare-review",
    "system_prompt_fragment": "<verbatim>",
    "user_template": "<verbatim>",
    "recipe_name": "bare-review-v1",
    "default_workers": 3,
    "suspect": true,
    "tier": "T2",
    "recommended_next_command_template": "/sc:adversarial --compare {compare_files} --suspect-source {suspect_files}",
    "stability": "stable"
  },
  "...": "..."
}
```

This makes the lens definition at-time-of-dispatch a durable artifact. `swarm run --resume` reads it back rather than re-resolving the (possibly mutated) registry (§9.3, INV-001 resolution).


## 4. Job Spec Schema

<!-- Source: V1 §3 with V2-influenced additions (`lens`, `--custom-prompt-dir`, amalgamation_mode) per refactor plan -->

Compact summary; full schema lives in `cli/swarm/schema.py`. See V1 spec §3.2 for the unabridged YAML reference; the differences from V1 are noted inline below.

### 4.1 Top-level fields

```yaml
spec_version: "1.0"                       # bumped on structural changes
job_id: <auto-generated>                  # <ISO-timestamp>-<lens>-<short-hash>
created: <ISO 8601>
caller: { skill, skill_version, invocation_label, kind }   # informational only

# ─── NEW: lens-driven path (refactor plan Change #2) ───
lens: <lens-name OR 'custom' OR null>     # when set, defaults below are filled from LENSES[lens]
custom_prompt_dir: <path OR null>         # when lens=='custom', point at directory containing system.txt + user.txt + meta.yaml

# ─── workers ───
workers:
  count: <N ≥ status_policy.floor>
  models: [...]                            # explicit list; if absent, env-resolved
  timeout_sec: 180
  temperature: 0.2
  retry: { on_5xx: 1, on_5xx_backoff_sec: 2, on_4xx: 0, on_timeout: 0 }

# ─── transport ───
transport: { kind: openai_compat, base_url_env: T2ProxyUrl, api_key_env: T2ProxyKey }

# ─── prompt (caller supplies OR lens fills) ───
prompt:
  system: <verbatim system prompt>        # MUST contain §11.5 injection-guard sentence (schema validator)
  user_template: <verbatim user template>
  variables: { ... }

# ─── target ───
target:
  kind: file | inline_text | inline_bytes_b64
  path: <abs path>
  truncation: { line_cap: 4000, byte_floor: 50 }
  delimiters: { open: "<<<TARGET>>>", close: "<<<END TARGET>>>" }
  injection_guard:
    enabled: true                          # NEW: enforced at preflight; STOP if violated
    required_substring: "<canonical §11.5 sentence>"   # default; override for custom guards

# ─── normalization ───
normalization:
  recipe: <Recipe-Protocol name OR 'custom-py:module:callable'>
  template_path: <abs path>
  schema_version: "1.0"
  recipe_args: { ... }
  on_parse_error: { salvage: true, retain_raw: true }

# ─── output ───
output:
  dir: <abs path>
  filename_template: "{lens}-{index:02d}-{model_slug}.md"
  lens_name: <propagated from `lens` if set>
  atomic_write: true
  emit_meta_sidecar: true

# ─── NEW: amalgamation mode (refactor plan Change #5) ───
amalgamation_mode: raw | normalize | normalize+merge   # default 'normalize'

# ─── status policy ───
status_policy: { floor: 2, success_first: true, partial_threshold: null }

# ─── post-fan-out hint ───
recommended_next_command_template: <string>
recommended_next_command_substitutions: { ... }

# ─── runtime knobs ───
runtime:
  mode: inline | detached
  log_level: info
  on_completion: { write_done_sentinel: true, print_contract_to_stdout: true }
```

### 4.2 Lens-driven defaults

When `lens` is set to a registry entry, preflight expands defaults from `LENSES[lens]` into the spec:

- `prompt.system` ← `lens.system_prompt_fragment`
- `prompt.user_template` ← `lens.user_template`
- `normalization.recipe` ← `lens.recipe_name`
- `normalization.template_path` ← `lens.output_template_path`
- `workers.count` ← `lens.default_workers` (overridable)
- `target.truncation.line_cap` ← `lens.default_target_line_cap` (overridable)
- `output.filename_template` ← `"{lens}-{index:02d}-{model_slug}.md"`
- `output.lens_name` ← `lens.name`
- `recommended_next_command_template` ← `lens.recommended_next_command_template`
- `caller_metadata.suspect` ← `lens.suspect`
- `caller_metadata.tier` ← `lens.tier`

Caller-supplied values in the spec override lens defaults; missing values fall through to lens; lens entry without a value AND no caller-supplied default → schema validation error.

### 4.3 Custom-prompt-dir mode (escape hatch with guard parity)

<!-- Source: V2 §4 custom escape hatch + INV-003/INV-014 fix (refactor plan Change #7) -->

When `lens == 'custom'` AND `custom_prompt_dir` is set, preflight reads `<dir>/system.txt`, `<dir>/user.txt`, `<dir>/meta.yaml`. The `system.txt` content is loaded as `prompt.system` and the **§11.5 substring check applies identically** to the lens-driven and JSON-Schema-validated paths (closes INV-003). Default behavior: STOP with actionable error if substring absent; `--auto-inject-guard` flag opts into auto-prepending the canonical sentence (backward compat for existing custom-prompt-dir users).


## 5. Result Contract Schema

<!-- Source: V1 §4 base + V2 §6.2 additions (lens, amalgamation_mode, merged_path) per refactor plan Change #5 -->

```yaml
contract_version: "1.0"
status: success | partial | failed                  # IMM-5 success-first
job_id: <as in manifest>
started: <ISO 8601>
finished: <ISO 8601>
elapsed_ms: <int>

caller: { skill, skill_version, invocation_label }
lens: <lens name or null>                            # NEW
lens_source: registry | custom | null                # NEW

target:
  path: <abs path>
  checksum: <sha256[:12]>
  truncated: <bool>
  truncation_line_cap: 4000

workers_requested: <N>
workers_succeeded: <M>
workers_failed: <N - M>

output_files:
  - index: <int>
    path: <abs path or null on hard failure>
    raw_path: <abs path or null>
    meta_path: <abs path>
    model_id: <string>
    model_label: <string>
    bytes: <int>
    status: success | timeout | parse_error | proxy_error
    http_code: <int>
    attempts: <int>
    elapsed_ms: <int>

amalgamation_mode: raw | normalize | normalize+merge   # NEW
merged_path: <abs path or null>                        # NEW; null when mode != normalize+merge OR M < 2

caller_metadata:                                       # caller-attached; orchestrator passes through
  suspect: <bool from lens or caller>
  tier: <string>

recommended_next_command: <rendered template>

artifacts:
  manifest_path: <abs>
  state_path: <abs>
  event_log_jsonl: <abs>
  event_log_md: <abs>
  done_sentinel: <abs>
```


## 6. CLI Surface

<!-- Source: V1 §5 verbs + new validate-lenses (refactor plan Change #8) + --lens flag -->

```
superclaude swarm                                              (Click group)
  run              Execute a swarm job from a spec file, stdin, or --lens shortcut
  status           Show the state of a job (terminal or in-flight)
  logs             Tail or dump a job's execution log
  attach           Re-attach to a detached (tmux) job's TUI
  kill             Terminate a running detached job
  scaffold         Emit a starter job-spec file for a named lens
  validate         Validate a job-spec file without dispatching
  validate-lenses  Validate the bundled lens registry (referenced files, recipe resolution, coupling rules)
```

### 6.1 `swarm run` flag additions

- `--lens <name>` — resolves lens-registry entry; caller may then omit prompt/recipe/template fields.
- `--custom-prompt-dir <path>` — when `--lens custom`, point at directory containing prompts.
- `--auto-inject-guard` — backward-compat for custom-prompt-dir users; auto-prepends the canonical §11.5 sentence.
- `--amalgamation-mode {raw,normalize,normalize+merge}` — default `normalize`.
- `--tui` — opt-in Rich Live dashboard (NOT default; non-TTY callers do not get terminal control sequences).
- `--force-relens` — on `--resume`, ignore manifest's `resolved_lens_entry` and re-resolve from current registry (default: rehydrate from manifest, per INV-001 fix).

All other flags inherited from V1 §5.2.

### 6.2 Exit codes

Inherited from V1 §5.2: 0 = run reached Wave 3 (status in contract); 2 = spec validation failure; 3 = preflight failure; 10 = orchestrator internal error.


## 7. Monitoring Contract

<!-- Source: V1 §6 (winner) — three-layer durable observability -->

Unchanged from V1: `.swarm-state.json` (atomic on transition) + `execution-log.jsonl` (append-only, lock-coordinated) + `execution-log.md` (human log) + `done.json` (terminal sentinel). Three caller patterns supported:

1. **`Bash run_in_background` + `until [ -f done.json ]`** — single-notification fire-and-wait.
2. **`Monitor` tool tailing the JSONL** — one notification per significant event.
3. **`swarm status --watch`** — Rich-rendered status table refreshing every 1s.

The opt-in `--tui` flag enables a Rich Live dashboard inside the inline-mode swarm process (refactor plan INV-012 fix; was V1 default, now opt-in).


## 8. Concurrency Model

<!-- Source: V1 §8 with INV-002 resolution -->

Single Python `ThreadPoolExecutor` invoked via `superclaude.execution.parallel.ParallelExecutor`. All N workers in one ParallelGroup. Each worker thread:

1. Builds the HTTP request body (`json.dumps` with target_content via `--arg`-equivalent — never shell-interpolated).
2. POSTs via `httpx` with per-worker timeout.
3. On 5xx: retry once after `retry.on_5xx_backoff_sec`. On 4xx / timeout / network: no retry.
4. On 2xx: parse `choices[0].message.content`; write `.raw` + `.meta.json` atomically.
5. Appends `worker_done` event to JSONL under a `threading.Lock`-guarded write.
6. Updates `.swarm-state.json` under lock + atomic rename.

**INV-002 resolution:** Python threads call `httpx` directly. The V2-style `swarm_dispatch.sh` shell script is **retired** in the merged design — Python ThreadPoolExecutor owns dispatch end-to-end. This eliminates the dual-writer race that would arise from mixing Python lock-guarded appends with V2's PIPE_BUF-atomic shell appends. The PIPE_BUF assumption (Linux-only, ≤4KB lines) is documented as deprecated in `docs/swarm-design-rationale.md`.


## 9. Resume + Crash Recovery

<!-- Source: V1 §6.5 base + INV-001 + INV-010 + INV-016 resolutions -->

### 9.1 Crash semantics

If the orchestrator crashes mid-dispatch: `.swarm-state.json` retains last-known state; workers that completed have `.meta.json` sidecars; no `done.json`.

### 9.2 `swarm run --resume <job_id>`

Re-runs Wave 0 in resume mode:

1. **Lens rehydration (INV-001 fix).** Reads `manifest.resolved_lens_entry` and uses it verbatim. Does NOT re-resolve from `LENSES`. `--force-relens` opts into re-resolution.
2. **Worker skip.** Workers whose `.meta.json` reports `status: success` are skipped.
3. **Worker re-dispatch.** Remaining workers re-run.
4. **Normalize.** Wave 2 re-runs over all `.raw` files (existing successes re-write deterministically, no-op).
5. **Merge regeneration (INV-010 fix).** When `amalgamation_mode == normalize+merge`, Wave 3 unconditionally regenerates `merged.md` from current `final_path`s (after the re-dispatched workers' Wave 2 completes). This prevents stale-merge / mixed-timestamp provenance lies.
6. **Reduce.** Status determination + contract emit per IMM-5.

### 9.3 Manifest-as-source-of-truth (INV-016 resolution)

`manifest.resolved_lens_entry` is the durable definition of "what this swarm was supposed to do." `--resume` honors it; lens-registry mutations between runs do not affect a resumed job. This makes detached + resume + lens-materialization end-to-end consistent.


## 10. Amalgamation Modes



### 10.1 Three modes

- **`raw`** — Wave 2 is a no-op; final files are the workers' `.raw` outputs untouched. Useful when the caller wants the unmodified model responses and runs its own parser downstream (e.g., research with citation-extraction normalizer).
- **`normalize`** (default) — Wave 2 runs the configured Recipe per worker; final files are normalized `.md` per the lens template.
- **`normalize+merge`** — `normalize` + Wave 3 runs `swarm/merge.py` (mechanical concat) producing `<output>/merged.md` and setting `merged_path` in the contract.

### 10.2 `swarm/merge.py` — structural guards

The merge module is bounded by **four guards** copied verbatim from V2 §5.5:

1. **Explicit allowed/disallowed ops in module docstring:**
   - Allowed: read each worker's `final_path`, strip frontmatter, prepend `## From {model_label} ({elapsed_ms}ms)` provenance header, concat in slot-index order.
   - Disallowed: no reorder, no dedup, no scoring, no winner selection, no claim rewriting.
2. **Hard LOC ceiling:** module body ≤30 LOC (excluding imports + docstring).
3. **PR-review checklist:** any change to `swarm/merge.py` requires a "boundary preservation" review note.
4. **Boundary test:** `tests/swarm/test_merge_mechanical_only.py` asserts a 3-worker concat produces all 3 sections in slot-index order with no transformations beyond the provenance header. A CI rule flags PRs touching this test file for extra review.

### 10.3 Edge cases

- **M = 0 (status: failed):** `merged_path = null`; no merge file written.
- **M = 1:** `merged_path = null`; no merge file written (failed-by-IMM-5 since floor=2).
- **M ≥ 2 (status: partial or success):** `merged_path` populated; merge includes only successful workers' files.
- **`--resume` + `normalize+merge`:** ALWAYS regenerate `merged.md` after Wave 2 (INV-010 fix).


## 11. Boundaries (consolidated Will / Will Not)



### 11.1 The orchestrator WILL

- Dispatch N parallel proxy calls via Python ThreadPoolExecutor (code-enforced parallelism).
- Read `--target`, apply `--target-line-cap`, enforce IMM-4 empty-target guard, compute provenance checksum.
- Compose `prompt.system` + `prompt.user_template` from lens registry OR caller-supplied OR `--custom-prompt-dir`, with §11.5 injection-guard enforced in all three paths.
- Run the configured Recipe per worker; promote `parse_error → success` on §7.4 salvage.
- Apply per-worker hard timeout + 5xx-retry-once + 4xx-no-retry policy.
- Emit `manifest.json` with `resolved_lens_entry` snapshot.
- Emit `.swarm-state.json` (atomic on transition), `execution-log.jsonl` (lock-coordinated append), `execution-log.md` (human log), `done.json` (sentinel), `return-contract.yaml` (write-on-failure).
- Continue on partial success (≥`status_policy.floor` workers).
- Support `--detached` + `--resume` + `swarm attach` / `kill`.
- Run `normalize+merge` mode as mechanical concat ONLY (four structural guards).
- Validate the lens registry via `swarm validate-lenses`.

### 11.2 The orchestrator WILL NOT

- Score, deduplicate, reorder, rewrite, or filter worker findings (even in `normalize+merge` mode — guarded by `tests/swarm/test_merge_mechanical_only.py`).
- Make claims about review quality.
- Retry beyond a single 5xx retry per worker.
- Route to Anthropic models.
- Write outside `--output`.
- Cache responses across invocations.
- Auto-detect a lens from the target (caller must pick).
- Auto-invoke `recommended_next_command` (it's a suggestion, never an action).
- Modify the target file or any file outside `--output`.
- Bundle prompts as policy without lens-registry curation (caller-supplied path validates via JSON Schema; lens-driven path validates via registry validator).


## 12. Inheritance from Parent Spec — Verbatim Carry



All parent bare-review §3.3 / §4 / §7 / §8 / §11.5 invariants carry forward. See V1 spec §12 for the full field-by-field mapping (no changes; the merged design inherits the same way V1 does).

The bare-review-specific items that V2 inlined as universal — `suspect`, the compressed-markdown findings table, `/sc:adversarial --suspect-source` recommendation, severity vocab — remain caller-policy in this design:

- `caller_metadata.suspect` is set by the lens entry (e.g., `bare-review` lens has `suspect: true`).
- The compressed-markdown template lives in `bare_review_v1.py` recipe + `refs/templates/bare-review-output.md`.
- The `/sc:adversarial --suspect-source` hand-off lives in the `bare-review` lens entry's `recommended_next_command_template`.
- Severity vocab is a recipe argument.

Other lenses with different policies (e.g., `troubleshoot-hypothesis` is `suspect: false`, `tier: T2-tshoot`, `recommended_next_command: /sc:troubleshoot --merge-hypotheses ...`) are first-class registry entries.


## 13. Future-Harness Compatibility



The forbidden topic is integration with openharness / openhands / any third-party harness SDK. The required check is: does anything in this design *preclude* such integration later?

### 13.1 Verification

A future harness wants to:

1. **Build a job spec.** JSON Schema-validated YAML/JSON document, no Claude-specific fields. ✓
2. **Invoke the orchestrator.** `subprocess.run(["superclaude", "swarm", "run", "--detached", spec_path])` works from any language. ✓
3. **Monitor progress.** Three patterns (file-tail, sentinel poll, status command) — none require a Claude tool. ✓
4. **Receive results.** YAML `return-contract.yaml` + JSON `done.json` — stdlib-parseable everywhere. ✓
5. **Custom-extend.** `custom-py:<module>:<callable>` is Python-only; non-Python harnesses use `passthrough` recipe and post-process raw bodies. ✓
6. **Re-attach after crash.** `--resume` + `.swarm-state.json` + `done.json` give any caller crash-recovery. ✓

### 13.2 No Claude-Code-isms in the contract surface

- Job spec, result contract, CLI surface, monitoring contract have **zero** references to Claude tool names.
- `caller.kind` is informational only (`skill | command | harness | human`) and never used for routing.
- Detached mode guarantees the caller can die and the orchestrator continues.
- The lens registry is plain Python data; non-Python harnesses can read `manifest.resolved_lens_entry` after the fact for forensics, or skip lens-driven mode entirely and supply prompts via job spec.

### 13.3 Net assessment

Non-precluding. The design is implementable-by-extension for future openharness / openhands / OpenAI Assistants integration without breaking changes here.


## 14. Decisions, Refined



### 14.1 New top-level verb vs subcommand?

**New top-level verb (`superclaude swarm`).** Per V1 §14.1. Sprint is sequential-phase orchestration; roadmap is generative-graph orchestration; swarm is single-shot parallel fan-out. Three different primitives.

### 14.2 Where does prompt + template policy live?

**Hybrid: bundled lens registry inside the orchestrator package + caller-supplied job-spec path + custom-prompt-dir escape hatch.** All three paths enforce §11.5 injection-guard substring presence at preflight. The lens registry serves the common cases (V2 win on policy curation); the caller-supplied path preserves V1's "prompts as caller-state" affordance; custom-prompt-dir lets a caller use lens-style invocation with own prompts.

### 14.3 Monitoring shape for an inference-layer agent?

**Three patterns, all supported, with `Bash run_in_background` + `until [ -f done.json ]` as the recommended Claude-Code shape.** Per V1 §14.3.

### 14.4 Universal `M<floor → failed` vs per-job declared floor?

**Per-job declared floor, default 2.** Per V1 §14.4 with IMM-5 success-first preserved.

### 14.5 What's universal vs lens-specific?

Per V1 §14.5 table (universal in orchestrator: target ingestion, byte-floor STOP, provenance checksum, injection-guard delimiters, JSON-escape transport, per-worker timeout, sidecar emit, atomic-write, IMM-5; lens-specific via registry: prompts, output template, normalizer choice, `suspect`, tier, next-cmd, severity vocab).

### 14.6 Internal merge step?

**Yes, but only as mechanical concat with four structural guards.** Reversing V1 §14.6. The `normalize+merge` mode is opt-in (default `normalize`); the module is ≤30 LOC; PR review + boundary test prevent scope creep into judging. Scored merging remains `/sc:adversarial`'s job.

### 14.7 Future-harness compatibility check?

Pass. See §13. No Claude-Code-isms in the contract, monitoring, or CLI surface.


## 15. Risks & Tradeoffs



### 15.1 Lens-registry sprawl

If every new lens ships a built-in entry, the registry bloats. Mitigation: PR-review discipline requires a real caller; entries without a real caller are deferred to `custom-py:` + caller-side custom prompts.

### 15.2 Merge boundary erosion

`normalize+merge` mode could drift into judging via incremental PRs. Mitigation: four structural guards (docstring + LOC ceiling + PR review + boundary test) + CI rule on the boundary test.

### 15.3 Resume + lens-mutation interaction

`--resume` rehydrates from manifest (default); `--force-relens` opts into re-resolution. Mitigation: documented in §9.2; tests cover both paths.

### 15.4 Tmux dependency for detached mode

Same risk as sprint. Same mitigation: detached is optional; inline is default.

### 15.5 ThreadPoolExecutor surprise

Documented in `dispatch.py` docstring; tested with stub transport.

### 15.6 Custom-prompt-dir guard parity

Existing custom-prompt-dir users may need to add the §11.5 sentence to their `system.txt`. Mitigation: `--auto-inject-guard` flag for backward compatibility during migration.

### 15.7 Schema evolution drag

`spec_version` evolution: orchestrator at `1.1` can load specs at `1.0`. Forward-compat best-effort.


## 16. Migration Plan (sc-bare-review as the first caller)



|Phase|Scope|
|-------|-------|
|1|CLI scaffold + Click group + JobSpec data model + JSON Schema (§11.5 substring rule)|
|2|Preflight wave (env + target ingest + lens resolution + manifest emit with `resolved_lens_entry`)|
|3|Dispatch wave (httpx + ParallelExecutor + sidecar emission)|
|4|Normalize wave (Recipe Protocol + `bare_review_v1` + `passthrough` + Wave 3 amalgamation mode dispatcher + `merge.py` with 4 guards)|
|5|TUI + dual logs (Rich Live `--tui` opt-in, not default)|
|6|Detached mode (tmux + state file + sentinel + `swarm status` / `logs` / `attach` / `kill`); `--resume` with manifest rehydration (INV-001) and merge regeneration (INV-010)|
|7|Lens registry (cli/swarm/lenses/ with 7 entries) + `swarm validate-lenses` subcommand|
|8|sc-bare-review SKILL.md rewritten as ~60-line thin caller → builds `--lens bare-review` job spec → execs CLI → relays return contract; A/B parity test against today's bare-review output|
|9|scripts/*.sh deleted; sc-bare-review production migration|
|10|Wire additional callers progressively (reflect Wave 3 → `spec-completeness`; troubleshoot Tier 2 → `troubleshoot-hypothesis`; research → `feasibility-probe` or `raw` mode; document → `doc-completeness`; code-review → `refactor-find` + `edge-case-hunt`)|

### 16.1 Spec-fidelity gate (carried from V1 §10.5)

Every IMM-N invariant has a corresponding acceptance test in the orchestrator's test suite (IMM-3 via stub-worker parallelism test, IMM-4 via 49-byte target test, IMM-5 via parametrized status test, IMM-6 via mid-write kill test, §11.5 via target-containing-end-marker test).

### 16.2 Invariant remediation tests (NEW — from R2.5 fault-finder)

- `tests/swarm/test_resume_uses_manifest_lens.py` — INV-001 fix verification
- `tests/swarm/test_concurrency_python_only.py` — INV-002 fix verification (no shell dispatch)
- `tests/swarm/test_custom_prompt_dir_injection_guard.py` — INV-003 fix verification
- `tests/swarm/test_resume_regenerates_merge.py` — INV-010 fix verification
- `tests/swarm/test_escape_hatch_guard_parity.py` — INV-014 fix verification
- `tests/swarm/test_merge_mechanical_only.py` — §10.2 boundary test


## 17. Open Questions (deferred to implementation tasklist)

1. Should `validate-lenses` run as a pre-commit hook by default? (Probably yes; defer to tasklist for the hook wiring.)
2. Per-lens version pinning (`--lens-version v2`)? Defer until lens definitions mutate frequently in production.
3. Should `recommended_next_command` ever be auto-executed via `--auto-handoff`? Defer.
4. Prometheus / OpenMetrics output at event boundaries? Defer.
5. Per-model overrides (e.g., per-model temperature) within one swarm? Defer until a real lens asks (relates to A-005 shared assumption — partially open).
6. Concurrent-`--output`-dir protection? Defer; document caller-must-avoid for v1.
7. Workers > configured T2Models guard (INV-005) — adopt V1's "warn-on-exceed-with-defaults" or V2's STOP? Recommend V1's warn semantics; flag for tasklist confirmation.
8. Empty-pool failure path: write `failed`/`env-missing` contract OR pre-output-dir abort? (INV-007) Recommend write-on-failure when output dir is creatable; pre-output-dir abort otherwise.


## 18. Summary

This merged spec selects **Variant 1 (CLI) as the architectural base** for the multi-model swarm orchestrator and incorporates **Variant 2 (SKILL)'s lens registry, mechanical-merge mode with structural guards, mechanism-vs-policy framing, consolidated Will/Will-Not, and registry validator** as additive integrations. The 11 refactor-plan changes + 6 invariant remediations from Round 2.5 fault-finder are all addressed in-design.

Per the debate transcript: both advocates' Round 2 closing paragraphs converged on this hybrid independently. The architectural decision (V1 orchestrator home + V2 lens registry inside) is settled; the under-specified seams between V1 and V2 (resume + lens mutation, concurrency model, custom-prompt-dir guard parity, merge regeneration on resume, escape-hatch isomorphism, detached + lens-materialization end-to-end) are resolved by the fault-finder's recommended actions adopted verbatim.

The merged design preserves every IMM-N invariant from parent bare-review v1.3.0-draft, strengthens IMM-3 via code-enforced ThreadPoolExecutor, extends §11.5 enforcement to all three prompt-input paths, and ships skill-agnostic infrastructure that any skill can call via `subprocess.run` of the `superclaude swarm` CLI — including future non-Claude harnesses via the non-precluding contract surface (§13).

Open questions are bounded and deferred to the implementation tasklist; none block the v1 design.
