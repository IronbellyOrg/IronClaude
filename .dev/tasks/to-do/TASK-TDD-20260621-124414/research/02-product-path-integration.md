# Research 02 — Reflect CLI Product-Path Integration

**Investigation type:** Integration Mapper
**Topic:** Where and how the deterministic sweep is invoked, and how the 6 fields + ledger are written into the contract pipeline.
**Component root:** `src/superclaude/cli/reflect/`
**Status:** Complete

## Scope

Map the product-path integration surface for the deterministic sweep:
- Where `return-contract.yaml` is **written** (candidate invocation sites for the new ledger/6-field writer).
- Where it is **parsed/consumed** (the contract consumer that must read deterministically-written fields).
- The `IndentDumper` / `_atomic_write_text` conventions the new ledger writer must follow.
- Coverage tradeoffs of each candidate invocation site.

All file:line citations are tagged `[CODE-VERIFIED]` after reading the actual source.

## What "the 6 fields + ledger" refers to (anchoring)

The "deterministic sweep", the "6 fields", and the "ledger" do **not** yet exist anywhere
under `src/superclaude/cli/reflect/`. A grep for `runtime_surface`, `ledger`, `sweep`,
`reachab`, `deterministic sweep` across the whole CLI package returns only incidental
matches (`_atomic_write_text` docstring saying "NOT a deterministic `.tmp`"). [CODE-VERIFIED — `grep -rn` over `src/superclaude/cli/reflect/`, zero functional matches]

The spec for what must be produced lives in the SKILL refs, not the CLI:

- **The 6 contract scalars** (exact names, SKILL.md:731-736 [CODE-VERIFIED]):
  1. `runtime_surface_requirements: [<list str>]` (FR-RSR.1)
  2. `runtime_surface_sweep_ran: <bool>` (FR-RSR.2)
  3. `runtime_surface_ledger_path: <abs path> | null` (FR-RSR.2 — `<output>/artifacts/runtime-surface-ledger.yaml`)
  4. `runtime_surface_unreached: <int>` (FR-RSR.2/6 — drives §5.3 pre-filter)
  5. `runtime_surface_degraded: <bool>` (FR-RSR.3/8)
  6. `unreached_surfaces: [<list of UnreachedSurface>]` (FR-RSR.6)
- **The ledger** is `<output>/artifacts/runtime-surface-ledger.yaml`, one row per evaluated
  edge (`RuntimeSurfaceLedgerRow` TypedDict), per `refs/runtime-surface.md:61-101` [CODE-VERIFIED].
- **Count invariant** `len(unreached_surfaces) == runtime_surface_unreached` MUST hold
  (runtime-surface.md:96 [CODE-VERIFIED]).
- `contract_version` "1.6.0" is the additive bump that introduces `runtime_surface_*`
  (SKILL.md:672 [CODE-VERIFIED]).

The integration question this doc answers: **where in the product (Python) path does this
deterministic sweep get invoked, and where do its 6 fields + ledger get written so the
contract consumer (`contract.derive_verdict`) reads them.** Today the contract is authored by
an LLM (`/sc:reflect`) on the Tier-1 path and by `ensemble.build_reflect_contract` on the
Tier-2 path — neither emits the `runtime_surface_*` fields. So the new writer is a genuinely
new product-path surface that must be wired into one of the candidate sites below.

---

## File: `src/superclaude/cli/reflect/commands.py` (359 lines)

**Role:** Thin Click CLI surface — the `superclaude reflect run` command group. Lazy-imports
config + runner inside the command body; never duplicates verdict logic.

**Exports (top-level symbols):**
- `reflect_group` — `@click.group("reflect")` callback; FR-2 recursion breaker [CODE-VERIFIED commands.py:47-73].
- `run(...)` — `@reflect_group.command()` Click command with the full Section-9 option set [CODE-VERIFIED commands.py:76-269].
- Module helpers: `_is_tmux_available`, `_session_name`, `_write_exit_sentinel`,
  `_build_inner_command`, `_launch_tmux` [CODE-VERIFIED commands.py:277-359].

**Where the contract is touched:** commands.py does **not** write or parse
`return-contract.yaml` itself. It delegates the entire run to the runner:
- `result = ReflectRunner(config).run()` [CODE-VERIFIED commands.py:254].
- `exit_code = result.verdict.exit_code` [CODE-VERIFIED commands.py:255].
- The `contract:` echo the task brief flagged at "~line 266" is at **commands.py:266-267**
  [CODE-VERIFIED]:
  ```python
  if result.contract_path:
      click.echo(f"  contract: {result.contract_path}", err=True)
  ```
  This is **diagnostic stderr only** (printed on a non-zero verdict). It is NOT an invocation
  site for the sweep, and not a write of the contract — `result.contract_path` is the path the
  runner already parsed (`str(config.contract_path)`, set in `_audit_once` at runner.py:452).
  Treating commands.py:266 as the sweep invocation site would be a mis-read: by the time this
  echo runs the contract has already been authored, parsed, and the verdict derived.

**Candidate-invocation-site verdict for commands.py:** **Poor fit for the sweep itself.** The
only product-code seam here is line 254 (`ReflectRunner(config).run()`). Anything before it is
Click parsing/config-resolve; anything after it is exit-code wiring + sentinel + stderr echo.
A sweep call in `run()` (e.g. between config-resolve and `ReflectRunner(...).run()`) would have
to write the contract *before* the runner authors it — and the runner's `_audit_once` overwrites
`config.contract_path` wholesale on both tiers, so a pre-written sweep contract would be
clobbered. **Coverage tradeoff:** even if wired correctly, commands.py covers **only**
`superclaude reflect run`. It does NOT cover a bare `claude -p /sc:reflect ...` invocation
(the skill-driven path), because that never enters this Click command at all.

**Config-STOP sidecar branch (commands.py:211-247) [CODE-VERIFIED]:** on a `ValueError` from
`resolve_config`, the command writes a `Verdict.BLOCKED` sidecar via `write_sidecar` when
`--output` is set, then `sys.exit(2)`. This is the one place commands.py imports
`ReflectResult`/`Verdict`/`write_sidecar` directly. Relevant because a sweep writer that needs
an always-written artifact must mirror this fail-closed-even-before-runner posture.

---

## File: `src/superclaude/cli/reflect/runner.py` (622 lines)

**Role:** The thin orchestrator + atomic frontmatter write-back. `ReflectRunner.run()` is the
single entrypoint that derives → preflights → launches the audit → parses the contract →
derives the verdict → writes `reflect_post:` frontmatter + the `wrapper-result.yaml` sidecar.

**Exports / module-level conventions the new ledger writer MUST follow:**
- `_IndentDumper(yaml.SafeDumper)` [CODE-VERIFIED runner.py:58-67] — overrides
  `increase_indent(self, flow=False, indentless=False)` to `return super().increase_indent(flow, False)`
  so block sequences indent under their key (yamllint `indent-sequences: true` conformant).
  **The new ledger writer must dump through `_IndentDumper`, not bare `yaml.dump`/`safe_dump`**,
  or pre-commit yamllint fails on the `unreached_surfaces:`/`production_referrers:` sequences.
  (Note the divergence: `ensemble._emit_reflect_contract` uses plain `yaml.safe_dump` instead —
  see ensemble section. The ledger is a NEW machine-generated YAML artifact with nested
  sequences, so it must follow the runner's `_IndentDumper` convention, not the ensemble's.)
- `_atomic_write_text(path, text)` [CODE-VERIFIED runner.py:70-89] — randomized same-dir temp
  (`.{name}.tmp.{pid}.{uuid4hex}`) + `os.replace` + `finally`-unlink. `parent.mkdir(parents=True,
  exist_ok=True)` runs first. **The ledger + any sweep-authored contract overwrite should go
  through `_atomic_write_text`** for the parallel-session last-write-wins guarantee. (The task
  research-notes cited these at runner.py:66 and :70 — both [CONFIRMED] at those exact lines.)

**Contract-writing helpers (these write the contract-derived artifacts, NOT the contract):**
- `_build_reflect_post_value(result, *, head, reviewed_at)` [CODE-VERIFIED runner.py:92-116] —
  builds the fixed-order §6 `reflect_post` mapping. It surfaces only the 4-key
  `deviations` block (`authorized/necessary/drift/regression`) [runner.py:108-113]. **It does
  NOT carry `runtime_surface_*` (per U5 the auto-fix bookkeeping is sidecar-only; runtime-surface
  fields are not in this mapping today).** If the 6 fields must reach the tasklist frontmatter,
  this is where they would be added — but the spec routes them through the **contract**, not
  `reflect_post`, so the primary consumer is `contract.py`, not this helper.
- `write_reflect_post(tasklist_path, result, *, head, reviewed_at) -> str` [CODE-VERIFIED
  runner.py:119-187] — string-splices ONLY the `reflect_post:` block, race-guards against the
  on-disk bytes changing since read (`return "frontmatter-stale"`), atomic-writes. Returns
  `"written"` / `"frontmatter-stale"` / `"frontmatter-missing"`.
- `write_sidecar(output_dir, result, *, env_alias_count, write_status) -> Path` [CODE-VERIFIED
  runner.py:190-237] — ALWAYS writes `wrapper-result.yaml` (any verdict), via `_atomic_write_text`
  + `_IndentDumper` [runner.py:227-236]. Carries `deviations`, `child_exit_code`, `fix_iterations`,
  `fix_converged`. **This is the natural place to ALSO emit `runtime_surface_ledger_path` /
  `runtime_surface_*` into the always-written sidecar** if the sweep result must survive a
  frontmatter-stale failure — mirrors the existing `fix_iterations`/`fix_converged` precedent.

**THE invocation site — `ReflectRunner._audit_once` [CODE-VERIFIED runner.py:394-453]:**
This is the function that produces the contract the verdict is derived from. The control flow:
- `expected_tier = 2 if config.depth in {"standard", "deep"} else 1` [runner.py:419].
- `config.output_dir.mkdir(parents=True, exist_ok=True)` [runner.py:420].
- **Tier-2 branch** (`expected_tier == 2 and ClaudeProcess is _ProductionClaudeProcess`)
  [runner.py:421]: calls `run_tier2_ensemble(config)` then `rc = 0` [runner.py:425-426]. The
  ensemble WRITES `config.contract_path` internally (see ensemble section).
- **Tier-1 branch** (else) [runner.py:427-444]: constructs a real `ClaudeProcess` running
  `self._build_prompt()` (`/sc:reflect --mode post ...`) with `env_vars={_WRAPPER_MARKER: "1"}`,
  `proc.start()`, `rc = proc.wait()`. Here the **LLM (`/sc:reflect`) authors the contract**
  at `config.contract_path` as a side effect — the runner does not write it.
- **Then, on BOTH tiers** [runner.py:445-452]:
  ```python
  contract = parse_contract(config.contract_path)
  result = derive_verdict(contract, expected_tier=..., allow_single_vendor=..., child_rc=rc)
  result.contract_path = str(config.contract_path)
  ```
  → `parse_contract` is the single read of `return-contract.yaml` per audit [runner.py:445].

**Candidate-invocation-site verdict for runner.py (`_audit_once`):** **Strong fit.**
`_audit_once` is the one product-code chokepoint that runs on every audit of BOTH tiers, and it
sits exactly between "contract authored at `config.contract_path`" (Tier-1 LLM or Tier-2
ensemble) and "`parse_contract` reads it" (runner.py:445). A deterministic sweep wired here
(after the launch, before or merged-with `parse_contract`) could compute the 6 fields + ledger
from the diff/base in `config`, MERGE them into the just-authored contract (overwriting the
LLM's unreliable runtime_surface_* values per research-notes "ledger written in only 1/9 runs;
quiet-path field hallucination"), atomic-write the merged contract + ledger, then let
`derive_verdict` consume the deterministic values.
**Coverage tradeoff:** runner.py covers **all runner-driven paths** — `superclaude reflect run`
(foreground + the `--tmux` inner reinvocation, both land in `ReflectRunner.run`), AND the auto-fix
re-audit loop (`run()` calls `_audit_once()` once per loop turn, runner.py:562). It does NOT
cover a bare `claude -p /sc:reflect` that never goes through the CLI wrapper — that path only
runs the skill's own (LLM) sweep.

**The auto-fix loop (`ReflectRunner.run`) [CODE-VERIFIED runner.py:478-622]:** calls
`_audit_once()` at the top of each loop turn [runner.py:562], re-classifies via
`classify_fix(contract or {}, result.deviations)` [runner.py:576] (re-parses the contract at
runner.py:575), applies remediation via `_apply_remediation` [runner.py:455-476, 586], then
re-verifies. Because the sweep would live inside `_audit_once`, it re-runs deterministically on
every re-audit (NFR-4 "SAME --base reused"), so the 6 fields stay consistent across fix cycles.

---

## File: `src/superclaude/cli/reflect/contract.py` (366 lines)

**Role:** The PRIMARY consumer — the isolated `contract → verdict` map (spec Section 6) +
FR-11 degradation routing. Pure module: depends only on `.models` + stdlib + PyYAML; imports
nothing from `commands.py`/`runner.py`/`config.py`/`ensemble.py`.

**Exports relevant to contract consumption:**
- `parse_contract(path: Path) -> dict | None` [CODE-VERIFIED contract.py:65-82] — the **single
  contract reader**. `path.read_text` → `yaml.safe_load`; returns `None` when missing/
  YAML-unparseable/non-mapping (so the caller routes `blocked`). NFR-8 read-and-ignore: unknown
  top-level fields are tolerated → **the 6 new `runtime_surface_*` fields parse through here
  unchanged today, silently ignored until a consumer reads them.**
- `derive_verdict(contract, *, expected_tier, allow_single_vendor, child_rc) -> ReflectResult`
  [CODE-VERIFIED contract.py:130-246] — first-match-wins ordering **blocked → degraded →
  halted → pass** [contract.py:139]. This is the function the deterministically-written fields
  must influence.
- `_extract_deviations(contract) -> dict[str,int]` [CODE-VERIFIED contract.py:90-101] — pulls
  `deviation_count_by_class` as a 4-key int dict.
- `_degraded_reason(...)` [CODE-VERIFIED contract.py:249-304] — 14 FR-11 triggers, first match.
- `_halted_reason(contract) -> str | None` [CODE-VERIFIED contract.py:307-328] — audit-found
  problems (status failed/partial, regression/unauthorized/needs-human/user-decision booleans,
  then `deviations["regression"] > 0`, then `deviations["drift"] > 0`).
- `classify_fix(contract, deviations) -> str` [CODE-VERIFIED contract.py:331-366] — auto-fixable
  vs human-required carve-out (consumed by the runner fix loop).

**Where `runtime_surface_*` must plug into the consumer (today: NOT wired):**
The 6 deterministic fields have **no reader in `derive_verdict` / `_degraded_reason` /
`_halted_reason` today** [CODE-VERIFIED — grep `runtime_surface` in contract.py = 0 matches].
For the deterministic sweep to gate, a new trigger must be added. The natural seams:
- `runtime_surface_unreached >= 1` (UNREACHED symbols found) → this is the spec's §5.3 pre-filter
  that forces Tier 2 and `status: partial` (SKILL.md:402). At the wrapper-CLI verdict layer,
  an UNREACHED finding is an audit-found problem → belongs in **`_halted_reason`**
  (alongside `deviations["drift"] > 0` at contract.py:326-327).
- `runtime_surface_degraded is True` → a degrade routes through §10.6 Grounding Gaps (untrusted
  reachability) → belongs in **`_degraded_reason`** (the FR-11 family at contract.py:249-304).
- The count invariant `len(unreached_surfaces) == runtime_surface_unreached` is a malformed-
  contract guard candidate → mirror the existing `_LOAD_BEARING_BOOL_FIELDS` fail-closed block
  (contract.py:200-209) that routes BLOCKED on a malformed load-bearing field.

**Fail-closed conventions the consumer already enforces (the new fields should match):**
- F0: any non-zero `child_rc` vetoes the contract → BLOCKED before success fields are trusted
  [contract.py:148-159]. (On the Tier-2 ensemble path `rc` is hardcoded `0` at runner.py:426,
  so a sweep that detects its own incompleteness must signal via `runtime_surface_degraded`,
  NOT via rc.)
- `contract_version` gating: missing → BLOCKED `contract-version-missing`; major != "1" →
  BLOCKED `unknown-major-version` [contract.py:166-181]. **The "1.6.0" additive bump (SKILL.md:672)
  keeps major == "1", so the new fields pass this gate without a version-map change.** [CONFIRMED]
- F2: a PRESENT load-bearing boolean that is not an actual `bool` → BLOCKED
  `malformed-contract-boolean` [contract.py:200-209]. If `runtime_surface_degraded` is added to
  `_LOAD_BEARING_BOOL_FIELDS`, a `"true"`-string would correctly fail closed.

**Candidate-invocation-site note:** contract.py is the CONSUMER, never an invocation site for
the sweep (pure, no subprocess, no I/O beyond `parse_contract`'s single read). The sweep must
write its fields into `config.contract_path` *before* `parse_contract` reads it at runner.py:445.

---

## File: `src/superclaude/cli/reflect/models.py` (128 lines)

**Role:** Domain types only — no imports from the other reflect modules (types-only isolation).

**Exports relevant to contract creation/consumption:**
- `Verdict(str, Enum)` [CODE-VERIFIED models.py:26-54] — 4 states `PASS/HALTED/DEGRADED/BLOCKED`.
  `.exit_code` property [models.py:38-49] maps `pass→0, halted→10, degraded→11, blocked→2`
  (the single source of the exit-code contract; commands.py keys off `result.verdict.exit_code`).
  `.is_promotable` [models.py:51-54] = `self is Verdict.PASS`.
- `ReflectConfig` dataclass [CODE-VERIFIED models.py:57-98] — resolved launch inputs.
  **`contract_path` property [CODE-VERIFIED models.py:95-98]:**
  ```python
  @property
  def contract_path(self) -> Path:
      return self.output_dir / "return-contract.yaml"
  ```
  This is **THE pinned location** every writer and the single reader agree on:
  `ensemble._emit_reflect_contract(config.contract_path, ...)`, the LLM Tier-1 path, and
  `parse_contract(config.contract_path)` all resolve to `<output_dir>/return-contract.yaml`.
  The ledger, by spec, lives at the SIBLING `<output_dir>/artifacts/runtime-surface-ledger.yaml`
  (runtime-surface.md:63) — so a new `ledger_path` helper would be
  `self.output_dir / "artifacts" / "runtime-surface-ledger.yaml"`, parallel to this property.
  `config.depth`, `config.base`, `config.tasklist_path`, `config.reviewers`, `config.transport`
  are the inputs a deterministic sweep would read to scope the diff and enumerate roots.
- `ReflectResult` dataclass [CODE-VERIFIED models.py:101-128] — derived verdict + write-back
  outcome. Carries `deviations: dict[str,int]`, `child_exit_code`, `write_status`,
  `fix_iterations`, `fix_converged`, `remediation_task_path`. **No `runtime_surface_*` field
  today** — if the sweep result must travel from `_audit_once` through `write_sidecar`/
  `write_reflect_post`, a new optional field here (defaulted, to keep the 5 hand-built
  construction sites valid — same constraint the docstring at models.py:119-120 names) is the
  carrier. `.outcome` [models.py:125-128] = `"success"` iff `verdict is PASS`.

**Candidate-invocation-site verdict:** models.py is types-only; not an invocation site. Its
relevance is that the **`contract_path` property is the integration anchor** — the new ledger
writer should add a sibling `ledger_path` property here so all sites resolve the artifact path
identically (the same desync-avoidance discipline that `contract_path` enforces).

---

## File: `src/superclaude/cli/reflect/ensemble.py` (509 lines)

**Role:** The FR-RH2 Tier-2 ensemble driver. `run_tier2_ensemble(config)` fans out reviewer
workers via swarm dispatch, then **AUTHORS the Tier-2 `return-contract.yaml` deterministically
in Python** (not via an LLM). This is the OTHER place the contract is written.

**Exports relevant to contract creation:**
- `run_tier2_ensemble(config, *, prompt="", transport_for_slot=None, ...) -> dict | None`
  [CODE-VERIFIED ensemble.py:136-241] — the orchestrator. Builds preflight, resolves the per-slot
  transport, dispatches workers, normalizes, optionally scores adversarial convergence, builds
  the contract, and emits it. The **contract write happens at the end:**
  ```python
  contract = build_reflect_contract(normalized_workers, swarm_merged_path=..., ...)
  _emit_reflect_contract(config.contract_path, contract)   # ensemble.py:240
  return contract
  ```
  [CODE-VERIFIED ensemble.py:234-241].
- `build_reflect_contract(workers, *, swarm_merged_path=None, adversarial_convergence_score=None,
  adversarial_unavailable=False) -> dict | None` [CODE-VERIFIED ensemble.py:360-407] — the
  **deterministic contract author**. Returns `None` when zero reviewers succeeded (M==0 → the
  `contract-missing` branch). Otherwise returns the full top-level reflect contract dict
  [ensemble.py:377-407] with: `contract_version` ("1.0" — see Stale below), `status: "success"`,
  `tier_reached`, `reviewer_count`, `deviation_count_by_class` (all-zero), `t2_model_class_diversity`,
  `t2_vendor_diversity`, `verification_ran: True`, the FR-11 booleans (`regression_present` etc.
  all `False`), `degraded_components: []`, and more. **This dict is the exact template a
  deterministic sweep on the Tier-2 path would need to extend with the 6 `runtime_surface_*`
  fields** — `build_reflect_contract` produces NONE of them today
  [CODE-VERIFIED — grep `runtime_surface` in ensemble.py = 0 matches].
- `_emit_reflect_contract(path, contract) -> None` [CODE-VERIFIED ensemble.py:500-509] — the
  Tier-2 YAML writer the brief flagged at "~line 500". Verified shape:
  ```python
  def _emit_reflect_contract(path: Path, contract: dict | None) -> None:
      if contract is None:
          try: path.unlink()           # M==0 → remove → contract-missing branch
          except FileNotFoundError: pass
          return
      path.parent.mkdir(parents=True, exist_ok=True)
      text = yaml.safe_dump(contract, sort_keys=False, allow_unicode=True)
      path.write_text(text, encoding="utf-8")
  ```
  **Convention divergences from runner.py the new writer must reconcile:**
  1. Uses bare `yaml.safe_dump` (default Dumper), **NOT `_IndentDumper`** — its contract dict has
     flat scalars only, so indent-sequences is a non-issue here. But `unreached_surfaces:` and
     the ledger's `production_referrers:` ARE nested block sequences → the ledger writer MUST use
     `_IndentDumper` (runner convention), not copy this `safe_dump` call.
  2. Uses plain `path.write_text`, **NOT `_atomic_write_text`** — non-atomic. A new ledger writer
     following the runner convention should prefer `_atomic_write_text` for parallel-session safety.

**Supporting deterministic computers (prior art for sweep-style per-worker reduction):**
`compute_model_class_diversity` [ensemble.py:410-417], `compute_vendor_diversity`
[ensemble.py:420-438], `_vendor_from_model_id` [ensemble.py:441-457], `extract_convergence_score`
[ensemble.py:336-357]. These show the established pattern: derive contract scalars in pure Python
from worker facts, then bake them into `build_reflect_contract`'s dict. A runtime-surface sweep
would be the same shape — a pure computer feeding the contract dict.

**Candidate-invocation-site verdict for ensemble.py:** **Tier-2-only fit.** Wiring the sweep
into `run_tier2_ensemble` (compute fields, merge into `build_reflect_contract`'s return, write
via `_emit_reflect_contract`) covers the Tier-2 product path cleanly and is where the contract
is already authored deterministically. **BUT** it does NOT cover the Tier-1 path (which is LLM-
authored), nor a bare `claude -p /sc:reflect`. For the sweep to run on EVERY UC-2 audit
regardless of tier, the invocation must be at the tier-agnostic chokepoint
(`runner._audit_once`), with ensemble.py either deferring to that merged-write or having the
sweep applied to its dict before `_emit_reflect_contract`. The cleanest single-site coverage of
both runner-driven tiers is `_audit_once` post-launch (merge sweep into the just-written
contract); the cleanest *bare-`claude -p`* coverage is a **Wave-1A skill shell-out** (the skill
itself invokes the deterministic Python sweep), which is the only option that also covers the
non-CLI path.

---

## End-to-end contract pipeline (write → consume), as built today

```
superclaude reflect run TASK.md           bare: claude -p "/sc:reflect --mode post ..."
   │ commands.py:run()                          │ (never enters the CLI wrapper)
   │ resolve_config → ReflectConfig             │
   ▼                                            ▼
ReflectRunner(config).run()  [commands.py:254]   skill SKILL.md §6.1 runs the LLM audit
   │                                            │  + (today) LLM-authored runtime_surface_*
   ▼  runner.run() → loop → _audit_once()         │  → writes return-contract.yaml directly
   │  [runner.py:562 → :394]                     ▼
   ├─ Tier 2 (depth standard|deep, prod CP):    (no Python sweep on this path)
   │     run_tier2_ensemble(config)  [runner.py:425]
   │        └─ build_reflect_contract(...)  [ensemble.py:360]   ← deterministic, Python
   │        └─ _emit_reflect_contract(config.contract_path,…) [ensemble.py:240/500]  ← WRITE
   ├─ Tier 1 (else): ClaudeProcess(/sc:reflect …) [runner.py:430]  ← LLM authors contract  ← WRITE
   ▼
contract = parse_contract(config.contract_path)   [runner.py:445]                     ← READ (single)
result   = derive_verdict(contract, …)            [runner.py:446 → contract.py:130]   ← CONSUME
result.contract_path = str(config.contract_path)  [runner.py:452]
   ▼
write_reflect_post(...) [runner.py:605] + write_sidecar(...) [runner.py:616]          ← derived artifacts
   ▼
exit = result.verdict.exit_code  [commands.py:255 → models.py:exit_code]
```

**The single contract path constant:** `ReflectConfig.contract_path` = `output_dir /
"return-contract.yaml"` [models.py:95-98]. Every WRITE and the single READ resolve through it.
The new sweep must write the 6 fields into THIS file before runner.py:445, and the ledger into
the sibling `output_dir/artifacts/runtime-surface-ledger.yaml`.

## Candidate invocation sites — coverage tradeoff summary

| Site | File:line | Covers `reflect run` (fg + tmux + fix-loop) | Covers Tier-1 | Covers Tier-2 | Covers bare `claude -p /sc:reflect` | Notes |
|---|---|---|---|---|---|---|
| `commands.run()` (pre-`ReflectRunner.run`) | commands.py:254 | yes (entry only) | n/a (would predate authoring) | n/a | NO | Wrong layer: contract not yet authored; ensemble/LLM overwrite `contract_path` afterward. |
| `runner._audit_once()` (post-launch, pre/merge `parse_contract`) | runner.py:445 | YES | YES | YES | NO | **Best CLI-side single site.** Tier-agnostic chokepoint; re-runs each fix cycle; merge 6 fields into the just-written contract + emit ledger. |
| `ensemble.run_tier2_ensemble` / `build_reflect_contract` | ensemble.py:360-407, 240 | yes (T2 only) | NO | YES | NO | Tier-2-only; already deterministic-Python — natural to extend its dict, but misses Tier-1. |
| Wave-1A skill shell-out (SKILL §6.1 step 4b′ calls a Python sweep) | SKILL.md:465/487/491 (spec) | YES | YES | YES | **YES** | Only option covering the non-CLI path; requires a callable Python sweep module the skill shells out to. |

**Synthesis:** No single CLI-code site covers the bare `claude -p /sc:reflect` path — that path
never enters Python. To cover *all* invocation surfaces the sweep logic should live in a
**reusable pure-Python module** (research-notes proposes `cli/reflect/runtime_surface.py`) that
is (a) called from `runner._audit_once` for both runner-driven tiers, AND (b) shelled out to by
the skill (Wave-1A) for the bare path. The contract MERGE + ledger WRITE then follow the runner
conventions (`_IndentDumper` + `_atomic_write_text`) at whichever site does the writing.

## Gaps and Questions

- **Q1 — Merge vs author.** On the Tier-1 path the LLM authors the *entire* contract including
  (unreliably) `runtime_surface_*`. The deterministic sweep must MERGE-OVERWRITE those 6 keys
  into the parsed contract, not author a fresh contract (the LLM also writes
  `deviation_count_by_class`, `status`, etc. the sweep does not own). Where does the merge run —
  inside `_audit_once` between launch and `parse_contract`, or as a post-parse mutation before
  `derive_verdict`? (The latter is simpler but bypasses `config.contract_path` on disk; a later
  re-parse at runner.py:575 in the fix loop would then NOT see the merged values. Recommend
  on-disk merge before runner.py:445.)
- **Q2 — rc==0 hardcode on Tier-2.** `_audit_once` sets `rc = 0` for the ensemble path
  [runner.py:426]. A sweep that detects its own incompleteness cannot signal via `child_rc`
  (F0 BLOCKED veto, contract.py:156); it must signal via `runtime_surface_degraded: true` →
  `_degraded_reason`. Confirm the spec wants degrade (not blocked) for an incomplete sweep.
- **Q3 — Consumer wiring is unbuilt.** `derive_verdict`/`_degraded_reason`/`_halted_reason` read
  ZERO `runtime_surface_*` fields today. The TDD must add the trigger(s); this doc names the
  seams (`_halted_reason` for UNREACHED, `_degraded_reason` for degraded) but the exact ordering
  vs the existing 14 degraded triggers / drift-halt is a design decision for the implementer.
- **Q4 — Ledger dir creation.** `output_dir/artifacts/` does not exist today; the ledger writer
  must `mkdir(parents=True, exist_ok=True)` (as `_atomic_write_text` already does for the parent).
- **Q5 — `ReflectResult` carrier.** If the sweep result must reach `write_sidecar`/`reflect_post`,
  a new defaulted field on `ReflectResult` (models.py) is needed; otherwise the contract file is
  the only carrier and `result` stays unaware of runtime-surface state.

## Stale Documentation Found

- **`contract_version` mismatch (real, low-severity).** `ensemble.REFLECT_CONTRACT_VERSION = "1.0"`
  [CODE-VERIFIED ensemble.py:59, used at :378], but SKILL.md:672 declares the live contract
  version `"1.6.0"` and attributes the additive `runtime_surface_*` (6 fields) to the 1.6.0 bump.
  The Tier-2 ensemble therefore emits a contract stamped `1.0`, two minor-spec generations behind
  the skill's declared schema. The consumer gate only checks `major == "1"` [contract.py:174-175],
  so this does NOT break verdict derivation today — but when the ensemble path starts emitting the
  6 fields, stamping them as `1.0` while the skill calls that schema `1.6.0` is an internal
  inconsistency the implementer should reconcile (bump `REFLECT_CONTRACT_VERSION` to match, or
  document the wrapper's contract version as intentionally independent of the skill's).
- **Research-notes line numbers — CONFIRMED, not stale.** research-notes.md cited `IndentDumper`
  at runner.py:66 and `_atomic_write_text` at runner.py:70; both verified at those exact lines.
  No correction needed.
- No stale `file:line` citations were found in the five target source files themselves; their
  inline docstring references (e.g. `process.py:97-112`, `SKILL.md:754`) were not re-verified as
  out of scope, but nothing in the read code contradicted them.

## Summary

The deterministic runtime-surface sweep, its 6 `runtime_surface_*` contract fields, and the
`runtime-surface-ledger.yaml` ledger **do not exist in `src/superclaude/cli/reflect/` today** —
this is greenfield product-path work. The contract is currently authored two ways: (1) by the
LLM `/sc:reflect` on the Tier-1 path, and (2) deterministically in Python by
`ensemble.build_reflect_contract` → `_emit_reflect_contract(config.contract_path)`
[ensemble.py:240/500] on the Tier-2 path. Both write to the single pinned path
`ReflectConfig.contract_path` (`output_dir/return-contract.yaml`, models.py:95-98). The single
reader is `contract.parse_contract(config.contract_path)` at **runner.py:445**, immediately
feeding `contract.derive_verdict` (the primary consumer, contract.py:130) which today reads none
of the 6 fields.

**The strongest CLI-side invocation site is `ReflectRunner._audit_once` (runner.py:394-453)** —
the tier-agnostic chokepoint that runs on every audit and every fix-loop re-audit, sitting
exactly between contract-authoring and `parse_contract`. It covers all runner-driven paths
(`reflect run` foreground, `--tmux` inner, and the fix loop) but NOT a bare `claude -p
/sc:reflect`. Full coverage of the bare path additionally requires a **Wave-1A skill shell-out**
to a reusable pure-Python sweep module. The new ledger/contract writer must follow the runner
conventions — dump nested sequences through **`_IndentDumper`** (runner.py:58-67, yamllint-safe)
and write atomically via **`_atomic_write_text`** (runner.py:70-89) — NOT the ensemble's bare
`yaml.safe_dump` + `path.write_text` (ensemble.py:508-509). Consumer wiring in `contract.py`
(`_halted_reason` for UNREACHED, `_degraded_reason` for degraded) is unbuilt and is the TDD's
to add; the `contract_version` "1.0" vs skill "1.6.0" mismatch is the one stale-doc finding.

**Status:** Complete
