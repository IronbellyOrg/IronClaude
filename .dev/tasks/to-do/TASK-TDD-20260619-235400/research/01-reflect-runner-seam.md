# 01 — Reflect Runner Tier-2 Launch Seam

- **Topic:** The reflect runner Tier-2 launch seam (`_audit_once`) and where a new `cli/reflect/ensemble.py` driver wires in for FR-RH2.1.
- **Investigation type:** Code Tracer (codebase is source of truth)
- **Scope:** `src/superclaude/cli/reflect/runner.py`, `commands.py`, `contract.py`, `models.py`; swarm reuse targets in `src/superclaude/cli/swarm/`.
- **Status:** Complete
- **Date:** 2026-06-20
- **Worktree root:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/`

> Verification tags: `[CODE-VERIFIED]` (read in actual source this turn), `[CODE-CONTRADICTED]`, `[UNVERIFIED]`.
> Line numbers re-verified against the shipped source; the task's `~L` hints are corrected inline where they drifted.

## Line-number re-verification (spec `~L` vs actual)

All of `runner.py` (598 lines) was Read this turn; citations below are `[CODE-VERIFIED]`.

| Symbol | Spec `~L` | Actual `runner.py` | Note |
|---|---|---|---|
| `_MODEL_ALIAS_ENV_VARS` tuple | L38-40 | **L37-41** | The 3 alias env-var names. |
| `_WRAPPER_MARKER` const | — | L53 | `"SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"`. |
| `write_reflect_post` | L117 | **L117** | Exact. |
| `write_sidecar` | L188 | **L188** | Exact. |
| `_child_env` | L238 | **L238** | Exact. |
| `count_model_aliases` | L254 | **L254** | Exact. |
| `preflight` | L264 | **L264** | Exact. |
| `_build_prompt` | L341 | **L341** | Exact. |
| `_audit_once` | L392 | **L392** | Exact. |
| `_build_prompt` call inside `_audit_once` | L406 | **L406** | `prompt=self._build_prompt()`. |
| `_apply_remediation` | L430 | **L430** | Exact. |
| `run` | L453 | **L453** | Exact. |
| Re-audit loop (`while True` / `_audit_once` reuse) | L537 | loop opens **L536**, `result = self._audit_once()` at **L537** | base reused (NFR-4). |

CLI entry `run()` in `commands.py` spans **L148-249**. `[CODE-VERIFIED]`

## (a) The EXACT current Tier-2 launch mechanism — single `claude -p` wrapper expecting in-process Task fan-out

Today there is **no ensemble driver**. Tier 2 is launched as **one headless `claude --print` subprocess** that runs the `/sc:reflect --mode post` slash command; the *in-process fan-out of 2-3 heterogeneous reviewer agents happens inside that single child's own Task tool calls* (the `/sc:reflect` protocol), not in the wrapper. The wrapper only sees one child process and one `return-contract.yaml`. `[CODE-VERIFIED]`

### The prompt — `_build_prompt`, `runner.py` L341-366

The composed stdin prompt is a single `/sc:reflect` slash invocation with real reflect flags only:

```python
def _build_prompt(self) -> str:
    config = self.config
    parts = ["/sc:reflect", "--mode", "post"]
    if not config.promote:
        parts.append("--no-promote")          # FR-9 hard default
    parts += ["--diff", config.base]          # SINGLE ref vs working tree (#153), NOT <BASE>..HEAD
    parts += ["--tasklist", str(config.tasklist_path)]
    if config.spec_path is not None:
        parts += ["--spec", str(config.spec_path)]
    parts += ["--depth", config.depth]        # "standard"|"deep" -> Tier 2
    if config.fix:
        parts.append("--remediate")           # FR-1: author (not run) corrective MDTM
    if config.executor_model:
        parts += ["--executor-model", config.executor_model]
    parts += ["--output", str(config.output_dir)]
    return " ".join(parts)
```

There is no model-fan-out token in the prompt; the diversity instruction is implicit in the `/sc:reflect` skill protocol that the single child runs. `[CODE-VERIFIED]`

### The launch — `_audit_once`, `runner.py` L392-428

`_audit_once` is the only Tier-2 launch surface. It builds **one** `ClaudeProcess`, starts it, waits, then parses the pinned contract:

```python
def _audit_once(self) -> ReflectResult:
    config = self.config
    expected_tier = 2 if config.depth in {"standard", "deep"} else 1   # L403
    config.output_dir.mkdir(parents=True, exist_ok=True)
    proc = ClaudeProcess(
        prompt=self._build_prompt(),                                    # L406
        output_file=config.output_dir / "reflect-stdout.json",
        error_file=config.output_dir / "reflect-stderr.log",
        model=config.model,                 # single top-level orchestrator model
        timeout_seconds=config.timeout_seconds,
        max_turns=config.max_turns,         # G1 explicit, never primitive default 100
        output_format="stream-json",
        env_vars={_WRAPPER_MARKER: "1"},    # recursion breaker into the child
    )
    proc.start()
    rc = proc.wait()
    contract = parse_contract(config.contract_path)
    result = derive_verdict(
        contract,
        expected_tier=expected_tier,
        allow_single_vendor=config.allow_single_vendor,
        child_rc=rc,
    )
    result.contract_path = str(config.contract_path)
    return result
```

`[CODE-VERIFIED]` (`runner.py` L392-428)

### The argv that actually runs — `_claude_argv_preview`, `runner.py` L368-388

The real `claude` argv (mirrored byte-for-byte from `ClaudeProcess.build_command()`) is:

```
claude --print --verbose --dangerously-skip-permissions --no-session-persistence \
  --tools default --max-turns <N> --output-format stream-json [--model <M>]
```

So Tier 2 = **one `claude --print` headless run with `--tools default`** (Task tool enabled), and the slash prompt's `/sc:reflect` protocol fans out reviewers *inside* that single process. `[CODE-VERIFIED]`

### Confirming docstring intent (commands.py)

The `reflect_group` docstring (`commands.py` L49-61) states the design literally: *"Launches `/sc:reflect --mode post` as a top-level `claude --print` subprocess (**so Tier 2 fans out**)…"* — i.e. fan-out is delegated to the child's in-process Task surface, not orchestrated by the wrapper. `[CODE-VERIFIED]`

### Isolation guardrails the current mechanism upholds (runner.py L8-12)

- No imports from `superclaude.cli.sprint` / `superclaude.cli.roadmap`.
- Zero `async def` / `await`.
- The ONLY reflect-launch path is `ClaudeProcess` (subprocess) — never an Agent/Task surface (NFR-7). Verified: `grep` for `async|await|Task(` in `runner.py` finds only docstring mentions, no executable usage. `[CODE-VERIFIED]`

## (b) What `_audit_once` returns — the `ReflectResult` shape and how its fields are populated today

`_audit_once` returns a `ReflectResult` (dataclass, `models.py` L94-121). `[CODE-VERIFIED]`

### `ReflectResult` shape (`models.py` L103-116)

| Field | Type | Default | Populated by (today) |
|---|---|---|---|
| `verdict` | `Verdict` | (required) | `contract.derive_verdict` (first-match: blocked→degraded→halted→pass) |
| `status` | `str \| None` | (required) | `_make_result` from `contract["status"]` (`contract.py` L116) |
| `tier_reached` | `int \| None` | (required) | `_make_result` from `contract["tier_reached"]` if `int` else None (L117) |
| `reason` | `str` | (required) | `derive_verdict` slug (e.g. `pass`, `timeout`, `child-crash`, `degraded-components`, `single-vendor`, `regression`, `drift`, `tier-mismatch`) |
| `report_path` | `str \| None` | (required) | `contract["report_path"]` (L120) |
| `contract_path` | `str \| None` | (required) | set to `None` by `_make_result` (L121), then **overwritten** by `_audit_once` to `str(config.contract_path)` (`runner.py` L427) |
| `deviations` | `dict[str,int]` | `{}` | `_extract_deviations` → 4 keys authorized/necessary/drift/regression from `deviation_count_by_class` (L122, L90-101) |
| `child_exit_code` | `int \| None` | `None` | `derive_verdict(child_rc=rc)` where `rc = proc.wait()` (L123) |
| `write_status` | `str` | `""` | set to `""` by `_make_result` (L123); finalized later by `run()` (`runner.py` L586) — NOT by `_audit_once` |
| `fix_iterations` | `int` | `0` | set by `run()` at L575 (`iteration - 1`); `_audit_once` leaves default |
| `fix_converged` | `bool` | `False` | set by `run()` at L576; `_audit_once` leaves default |
| `remediation_task_path` | `str \| None` | `None` | `_make_result` from `contract["remediation_task_path"]` (`contract.py` L126) — FR-8 read-only pointer |

`ReflectResult` also exposes a derived `outcome` property: `"success"` iff `verdict is Verdict.PASS`, else `"failed"` (`models.py` L118-121). `[CODE-VERIFIED]`

### Population path for one `_audit_once` call

1. `rc = proc.wait()` — child exit code.
2. `contract = parse_contract(config.contract_path)` — parses pinned `return-contract.yaml` → `dict | None` (`None` when missing/unparseable/non-mapping, `contract.py` L65-82).
3. `result = derive_verdict(contract, expected_tier, allow_single_vendor, child_rc=rc)` — all verdict/status/tier/reason/deviations/remediation fields come from here via `_make_result` (`contract.py` L104-127). **The wrapper never classifies deviations itself (NFR-1 thinness).**
4. `result.contract_path = str(config.contract_path)` — the one field `_audit_once` mutates post-derive (`runner.py` L427).

So `_audit_once` returns a `ReflectResult` whose verdict-bearing fields are 100% derived from the single child's `return-contract.yaml`, with `write_status`/`fix_iterations`/`fix_converged` left at defaults for `run()` to finalize. `[CODE-VERIFIED]`

### Re-audit loop reuse (`run`, `runner.py` L536-572)

The bounded fix loop calls `_audit_once()` once per cycle (`result = self._audit_once()` at L537). The comment at L537 states *"SAME --base reused every re-audit (NFR-4)"* — `config.base` is immutable across the loop, so every re-audit diffs the same base against the (now-mutated) working tree. `_audit_once` reads `config` fresh each call but nothing rewrites `config.base`. `[CODE-VERIFIED]`

## (c) The PRECISE seam in `_audit_once` for FR-RH2.1 (route Tier-2 ensemble through `ensemble.py`)

`cli/reflect/ensemble.py` **does not exist yet** — `ls` of the `reflect/` package shows only `__init__.py, commands.py, config.py, contract.py, models.py, runner.py`. `[CODE-VERIFIED]`

The seam is the **launch-and-parse middle of `_audit_once`, `runner.py` L405-426** — specifically the block:

```python
proc = ClaudeProcess( ... env_vars={_WRAPPER_MARKER: "1"})   # L405-417
proc.start()                                                  # L418
rc = proc.wait()                                              # L419
contract = parse_contract(config.contract_path)               # L420
result = derive_verdict(contract, expected_tier=..., child_rc=rc)  # L421-426
```

For FR-RH2.1 (spec §4.2: *"`_audit_once` routes the Tier-2 ensemble through `ensemble.py` instead of relying on the single-agent fan-out"*), the seam is to **branch on `expected_tier`**:

- **`expected_tier == 2`** (i.e. `config.depth in {"standard","deep"}`, computed at L403): instead of constructing the single `ClaudeProcess` (L405-419), call into `ensemble.py` — an in-process driver that fans out N heterogeneous reviewers and writes/returns a `return-contract.yaml`-shaped artifact at `config.contract_path`.
- **`expected_tier == 1`**: keep the existing single `ClaudeProcess` path unchanged.

The clean wiring keeps the **parse + derive tail (L420-427) untouched**: the ensemble driver's only contract obligation is to land a parseable `return-contract.yaml` at `config.contract_path` (and return an `rc` for `derive_verdict(child_rc=...)`). Then `parse_contract` → `derive_verdict` → `result.contract_path = ...` run identically for both tiers. This preserves NFR-1 thinness (the wrapper still never classifies deviations; it only routes the launch and reads the pinned contract). `[CODE-VERIFIED]`

### Why the seam is exactly here (not in `run`)

- `expected_tier` is already computed **inside** `_audit_once` at L403, so the tier branch belongs here, not in `run`.
- `run`'s loop (L536-572) is launch-agnostic — it only consumes the returned `ReflectResult.verdict` and `remediation_task_path`. Routing T2 through `ensemble.py` inside `_audit_once` means the fix-loop, write-back (`write_reflect_post`), and sidecar (`write_sidecar`) all keep working with zero change, and NFR-4 base-reuse is automatically inherited (the ensemble driver reads the same `config.base`/working tree the prompt embeds via `_build_prompt`). `[CODE-VERIFIED]`
- The pinned contract path is the integration contract: `config.contract_path` = `output_dir / "return-contract.yaml"` (`models.py` L88-91). Both the current single-agent child and a future `ensemble.py` driver must write there; `_audit_once` L420 reads exactly that path. `[CODE-VERIFIED]`

## (d) How diversity is sourced today + how the result is serialized

### Diversity sourcing — `count_model_aliases` over `ANTHROPIC_DEFAULT_*` (runner.py L37-41, L254-261)

The alias set is a fixed 3-tuple (`runner.py` L37-41):

```python
_MODEL_ALIAS_ENV_VARS = (
    "ANTHROPIC_DEFAULT_OPUS_MODEL",
    "ANTHROPIC_DEFAULT_SONNET_MODEL",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL",
)
```

`count_model_aliases(env)` (L254-261) returns `sum(1 for var in _MODEL_ALIAS_ENV_VARS if (env.get(var) or "").strip())` — i.e. the count of present-and-non-empty aliases, **capped at 3** by the tuple length. Docstring semantics: `≥3` → full Tier-2 diversity; `2` → degraded; `0-1` → T1-only. The count is **recorded in the sidecar**, and low diversity surfaces as a `degraded` verdict *via the contract* (`t2_model_class_diversity != "full"` etc. in `contract.py` `_degraded_reason`), **not as a preflight blocker**. `[CODE-VERIFIED]`

These are all **Claude model-class aliases** — the diversity model is "3 Claude classes (Opus/Sonnet/Haiku)", resolved at Wave 0 per the L36 comment *"The three model-class aliases reflect resolves at Wave 0 for Tier-2 topology."* `[CODE-VERIFIED]`

#### Where the count is taken (`run`, runner.py L481)

`env_alias_count = count_model_aliases(_child_env())` is computed **once**, immediately past the dry-run gate (L480-481). `_child_env()` (L238-251) builds a throwaway `ClaudeProcess(prompt="", output_file=devnull, error_file=devnull)` and calls its public side-effect-free `build_env()`, so the count matches the EXACT env the child reflect will see (FR-10/FR-11). `build_env` preserves `ANTHROPIC_DEFAULT_*` and pops `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` (per the L238-244 docstring). `[CODE-VERIFIED]`

The actual reviewer diversity at runtime is sourced by the **child** `/sc:reflect` protocol from these same aliases (the wrapper does not itself spawn per-model reviewers); `count_model_aliases` is the wrapper's *observability* of how much diversity the child can achieve. `[CODE-VERIFIED]`

### Serialization — `write_reflect_post` (runner.py L117-185) and `write_sidecar` (L188-235)

**`write_reflect_post`** (FR-6) atomically replaces ONLY the `reflect_post:` frontmatter block in the tasklist:
- Reads tasklist bytes once, normalizes CRLF→LF for matching (L138-144).
- Builds the §6 mapping via `_build_reflect_post_value` (L90-114): fixed field order `verdict, status, run_id, tier_reached, report, contract, reason, deviations{authorized,necessary,drift,regression}, head, reviewed_at`. `run_id` = parent dir name of `contract_path` (L95-96).
- String-splices the new block in place (preserving every other frontmatter byte + body), dumping via `_IndentDumper` (yamllint-conformant block sequences, L56-65).
- **Race guard**: re-reads bytes; if changed since first read → returns `"frontmatter-stale"` (no write). Else `_atomic_write_text` (randomized same-dir temp + `os.replace`, L68-87) and returns `"written"`. Other return slugs: `"frontmatter-missing"` (L148). `[CODE-VERIFIED]`

**`write_sidecar`** (FR-7) — ALWAYS writes `wrapper-result.yaml`, any verdict (L188-235). Serialized fields: `verdict, status, tier_reached, reason, report, contract, deviations{4 keys}, child_exit_code, env_alias_count, write_status, fix_iterations, fix_converged`. Critically, **`env_alias_count` is a sidecar-only field** (the diversity count is NOT in `reflect_post:` per U5; comment L220) — it is passed into `write_sidecar(..., env_alias_count=...)` from `run()` (L499, L526, L594). Uses the same `_IndentDumper` + `_atomic_write_text`. `[CODE-VERIFIED]`

#### `run()` finalize sequence (runner.py L574-597)

After the loop: `result.fix_iterations = iteration - 1` (L575), `result.fix_converged = result.verdict is Verdict.PASS` (L576); then `write_status = write_reflect_post(...)` (L580-585), `result.write_status = write_status` (L586); FR-6 fail-closed: a non-`"written"` status on a PASS flips verdict→BLOCKED (L588-590); finally `write_sidecar(..., env_alias_count=env_alias_count, write_status=write_status)` (L591-596). `[CODE-VERIFIED]`

## Reuse-audit re-confirmation: `ensemble.py` = reuse-by-import (compose swarm)

**Recorded verdict:** reuse-by-import — import & compose swarm `dispatch_wave1` / `_resolve_run_transport_factory` / `reduce_wave3`; do NOT rebuild fan-out.

### All three swarm symbols exist and are sync (grounded evidence)

| Symbol | File:line | Signature shape | async? |
|---|---|---|---|
| `dispatch_wave1` | `swarm/dispatch.py` **L334** | `(preflight_result, transport=None, *, transport_for_slot=None, prompt="", parallel_executor=None, worker_spec=None, logger=None) -> list[WorkerResult]` | plain `def` (no `async`/`await`) |
| `_resolve_run_transport_factory` | `swarm/commands.py` **L612** | `(transport_kind, *, models=None, env=None, workers_requested=None) -> Callable[[int], Any]` | plain `def` |
| `reduce_wave3` | `swarm/reduce.py` **L555** | `(worker_results, mode="normalize+merge", *, output_dir=None, workers_requested=None, ... ) -> ResultContract` | plain `def` |

`grep` for `^async def|^    async def| await ` across `dispatch.py reduce.py commands.py` returned **no matches** — the swarm fan-out is fully synchronous. `[CODE-VERIFIED]`

Key reuse fit:
- `dispatch_wave1` already routes through `ParallelExecutor` (NOT raw `ThreadPoolExecutor`) and supports **heterogeneous per-slot models** via `transport_for_slot` — exactly the multi-model reviewer fan-out reflect needs. `[CODE-VERIFIED]` (`dispatch.py` L334-393)
- `_resolve_run_transport_factory` builds the `(slot_index) -> Transport` factory binding slot `i` to env model `T2Model0N` (openai_compat) or a shared `StubTransport` (stub). `[CODE-VERIFIED]` (`commands.py` L612-655)
- `reduce_wave3` emits a `ResultContract` and can write `merged.md` + `return-contract.yaml` to a caller-supplied `output_dir` (NFR-013). This is the bridge to `_audit_once`'s pinned `config.contract_path`. `[CODE-VERIFIED]` (`reduce.py` L555-594)

### Does `_audit_once` structurally support an import-and-compose in-process driver? YES.

- `_audit_once` is a plain sync method; the parse+derive tail (L420-427) is launch-agnostic and only needs `config.contract_path` populated + an `rc`. A sync `ensemble.run(...)` call slotting in at L405-419 returns naturally — no event loop, no `async` bridge needed. `[CODE-VERIFIED]`
- The reflect package's hard isolation rules (`runner.py` L8-12: no `async`, ONLY `ClaudeProcess`/subprocess launch, **never an Agent/Task surface**) are satisfied by an in-process driver that composes swarm functions: swarm `dispatch_wave1` fans out via `ParallelExecutor` + `Transport` (HTTP/proxy or stub), **not** via `Task(` or `subprocess`. So an `ensemble.py` that imports swarm adds NO `Task(`/`subprocess` to the reflect launch path. `[CODE-VERIFIED]`

### Constraints / caveats on the reuse-by-import path

1. **Cross-package import direction.** `runner.py` L8-9 forbids importing `superclaude.cli.sprint` / `superclaude.cli.roadmap` — but **says nothing about `superclaude.cli.swarm`**. So importing swarm is not blocked by the stated guardrail. However, `_resolve_run_transport_factory` is a **private** (`_`-prefixed) symbol in `swarm/commands.py`; importing a private cross-package symbol is a coupling smell the TDD should call out (consider promoting it to a public swarm API surface, or have `ensemble.py` build the factory via the public `_resolve_run_transport` building blocks). `[CODE-VERIFIED]` `[UNVERIFIED]` (whether a public equivalent exists — not exhaustively searched this turn).
2. **Contract-shape bridge.** swarm `reduce_wave3` emits a swarm `ResultContract` / `return-contract.yaml` whose schema is the **swarm** contract, while `parse_contract`/`derive_verdict` expect the **reflect** contract fields (`contract_version`, `tier_reached`, `deviation_count_by_class`, `t2_model_class_diversity`, `degraded_components`, `status`, etc., per `contract.py`). `ensemble.py` must **translate** the swarm reduction into the reflect contract shape before it lands at `config.contract_path`. This is the real integration work; the fan-out itself is pure reuse. `[CODE-VERIFIED]` (reflect contract fields read in `contract.py`; swarm `ResultContract` shape `[UNVERIFIED]` — `reduce_wave3` return type seen but `ResultContract` definition not read this turn.)
3. **Transport/env contract.** openai_compat fan-out reads the T2 proxy env contract (`T2Model0N` from `~/.aienv`), which is a DIFFERENT diversity source than reflect's `ANTHROPIC_DEFAULT_*` aliases. The TDD must reconcile: today reflect diversity = 3 Claude aliases; swarm fan-out diversity = `T2Model0N` proxy pool. FR-RH2.1 will need to decide which pool drives the ensemble and how `count_model_aliases` / the `degraded` triggers map onto it. `[CODE-VERIFIED]` (both sources read).

Resolved follow-ups (firmed this turn): both transport resolvers are private — `_resolve_run_transport` (`swarm/commands.py` **L510**) and `_resolve_run_transport_factory` (**L612**); the only public env entry is `read_env` (`swarm/transports/openai_compat.py` **L159**). `ResultContract` is defined at `swarm/models.py` **L877** and `WorkerResult` at **L1027**. So caveat #1's "public equivalent" is **`[CODE-CONTRADICTED]`** — there is NO public swarm transport-factory API; reuse-by-import must either import the private symbol or compose `read_env` + a transport class directly. `[CODE-VERIFIED]`

## Key Takeaways

1. **No ensemble driver exists today.** `cli/reflect/ensemble.py` is absent; Tier 2 today = a single `claude --print` subprocess running `/sc:reflect --mode post` whose own in-process Task fan-out (not the wrapper) produces the 2-3 reviewers. (`runner.py` L341-428; `commands.py` L49-61)
2. **The seam is `_audit_once` L405-419**, branched on `expected_tier` (computed at L403). The parse+derive tail (L420-427) stays untouched; the ensemble driver's only obligation is to land a reflect-shaped `return-contract.yaml` at `config.contract_path` and return an `rc`. NFR-1 thinness and NFR-4 base-reuse are preserved for free.
3. **`_audit_once` returns a `ReflectResult`** whose verdict-bearing fields are 100% derived from the single child's contract via `derive_verdict`/`_make_result`; the wrapper only overwrites `contract_path` (L427) and `run()` later fills `write_status`/`fix_iterations`/`fix_converged`.
4. **Diversity = `count_model_aliases` over the 3 `ANTHROPIC_DEFAULT_{OPUS,SONNET,HAIKU}_MODEL` aliases**, capped at 3 Claude classes; recorded as the sidecar-only `env_alias_count`. Low diversity surfaces as `degraded` via contract triggers, never as a preflight blocker.
5. **Reuse-by-import is structurally sound.** `dispatch_wave1` / `_resolve_run_transport_factory` / `reduce_wave3` are all sync `def`s; importing+composing them adds no `async`/`Task(`/`subprocess` to the reflect launch path, satisfying the L8-12 isolation rules. The real work is (a) a swarm-`ResultContract`→reflect-contract translation, and (b) reconciling the `T2Model0N` proxy pool vs the `ANTHROPIC_DEFAULT_*` alias model.

## Gaps and Questions

- **`[CODE-CONTRADICTED]`** caveat #1 "consider a public equivalent": there is no public swarm transport-factory API — both `_resolve_run_transport` (L510) and `_resolve_run_transport_factory` (L612) are private. Reuse-by-import either imports a private cross-package symbol (coupling smell) or recomposes `read_env` + transport classes. The TDD should decide and, if importing the private factory, note the coupling explicitly.
- **`[UNVERIFIED]`** Exact field schema of swarm `ResultContract` (`swarm/models.py` L877) was located but not Read this turn; the swarm→reflect contract translation in `ensemble.py` cannot be fully specced until that schema is diffed against the reflect contract fields (`contract_version`, `tier_reached`, `deviation_count_by_class`, `t2_model_class_diversity`, `t2_vendor_diversity`, `degraded_components`, `merge_method`, `adversarial_convergence_score`, etc.).
- **`[UNVERIFIED]`** Whether `dispatch_wave1`/`reduce_wave3` can produce the reflect-specific deviation-classification fields at all, or whether reviewer outputs must be post-processed by a reflect-side adversarial-merge step before the contract is emitted. swarm `merge` (`swarm/merge.py`) was not read this turn.
- **`[UNVERIFIED]`** How the spec wants `count_model_aliases`/`env_alias_count` to behave once the ensemble sources diversity from the proxy `T2Model0N` pool rather than `ANTHROPIC_DEFAULT_*`. The `degraded` triggers in `contract.py` key off `t2_model_class_diversity`/`t2_vendor_diversity` contract fields, so the ensemble driver must populate those honestly from whichever pool it actually used.

## Summary

The reflect Tier-2 launch is, today, a **single headless `claude --print` subprocess** (`_audit_once`, `runner.py` L392-428) running `/sc:reflect --mode post` (prompt from `_build_prompt`, L341-366); reviewer fan-out happens *inside* that one child's Task tool, not in the wrapper. `_audit_once` returns a `ReflectResult` (`models.py` L94-121) wholly derived from the child's pinned `return-contract.yaml` via `derive_verdict`/`_make_result`. The precise FR-RH2.1 seam is the launch block **`runner.py` L405-419**, branched on the already-computed `expected_tier` (L403): route `expected_tier==2` into a new in-process `ensemble.py` driver while leaving the L420-427 parse+derive tail and `run()`'s loop/write-back untouched. Diversity is sourced by `count_model_aliases` over the 3 `ANTHROPIC_DEFAULT_*` Claude aliases (cap 3), recorded as the sidecar-only `env_alias_count`; results serialize via `write_reflect_post` (frontmatter, FR-6) and `write_sidecar` (`wrapper-result.yaml`, FR-7). The recorded **reuse-by-import** verdict for `ensemble.py` is re-confirmed: swarm's `dispatch_wave1` (L334), `_resolve_run_transport_factory` (L612), and `reduce_wave3` (L555) are all sync, importable, and route through `ParallelExecutor`+`Transport` (no `Task(`/`subprocess`), so composing them satisfies the reflect package's isolation guardrails — the only real work is a swarm→reflect contract translation and a private-symbol coupling decision.

**Status: Complete**
