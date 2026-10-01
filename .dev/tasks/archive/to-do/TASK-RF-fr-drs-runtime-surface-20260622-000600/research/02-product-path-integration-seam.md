# R2 — Product-path Integration Seam (Integration Points + Data Flow)

**Status:** Complete
**Date:** 2026-06-22
**Researcher:** R2 (of 8)
**Topic:** How the new `run_sweep` module wires into the reflect CLI product path.
**Focus:** EXACT integration at `runner._audit_once` so the builder can write precise wiring items.
**Worktree root:** `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3`

> Evidence tags: **[CODE-VERIFIED]** = re-read from current source this session; **[UNVERIFIED]** = absent from source / must be added or designed; **[TDD]** = stated by the driving TDD (`.dev/reflect-hardening/issue-3-deterministic-runtime-surface-sweep/tdd.md`).

---

## 0. Files read (all line numbers re-verified against current source this session)

| File | What was read |
|------|---------------|
| `src/superclaude/cli/reflect/runner.py` | FULL — `_IndentDumper` (58-67), `_atomic_write_text` (70-89), `_audit_once` (394-453), fix loop re-audit (561-562), `parse_contract` call (445) |
| `src/superclaude/cli/reflect/models.py` | FULL — `Verdict` enum (26-54) + `exit_code` (38-49), `ReflectConfig` (57-98) all fields, `contract_path` property (95-98) |
| `src/superclaude/cli/reflect/ensemble.py` | `REFLECT_CONTRACT_VERSION` (59), `run_tier2_ensemble` (166-309), emit call site (309), `_emit_reflect_contract` (626-635) |
| `src/superclaude/cli/reflect/commands.py` | `run` (164-269), `ReflectRunner(config).run()` (254) |
| `src/superclaude/cli/reflect/config.py` | `resolve_config` (123), `ReflectConfig(...)` construction (234-256), base docstring (95) |
| TDD | §6.4 (D2/D4), §7.3/§7.5, §8.1.2, §11.1, §19.3 Phase 2, §21 Alt 1 |

---

## 1. `run_sweep` arg construction from `ReflectConfig` (DELIVER #1)

Designed signature **[TDD §8.1.2, tdd.md:655-665]**:

```python
def run_sweep(
    diff: str, base_ref: str, scope_worktree: Path, tasklist: Path,
    output_dir: Path, availability_surface: dict, *, lsp: LspOverlay | None = None,
) -> "SweepResult": ...
```

`ReflectConfig` fields available to source the args from (ALL fields enumerated, `models.py:66-93`) **[CODE-VERIFIED]**:

```
tasklist_path: Path            base: str               head: str
spec_path: Path | None         depth: str              executor_model: str | None
output_dir: Path               model: str              timeout_seconds: int
max_turns: int                 promote: bool           allow_single_vendor: bool
tmux: bool                     dry_run: bool           print_command: bool
resume: bool                   base_override: str|None  fix: bool
max_fix_iterations: int        transport: str = "openai_compat"   reviewers: int = 3
@property contract_path -> output_dir / "return-contract.yaml"   (models.py:95-98)
```

Per-arg sourcing — the builder MUST write an item per row:

| `run_sweep` arg | Source from `ReflectConfig` | Status |
|-----------------|------------------------------|--------|
| `base_ref` | `config.base` (`models.py:67`) — the single ref reused on every fix-loop re-audit (NFR-002 / NFR-4) | **[CODE-VERIFIED]** field present |
| `scope_worktree` | **NO config field.** TDD §8.1.2 says "from `ReflectConfig`" but no work-tree-root field exists. Candidate derivation: `Path.cwd()` (the reflect run executes at the worktree root), or derive from `config.tasklist_path` ancestry, OR **add a `scope_worktree`/`worktree_root` field to `ReflectConfig`** populated in `resolve_config`. Decide in the task. | **[UNVERIFIED]** field ABSENT — must add or derive |
| `tasklist` | `config.tasklist_path` (`models.py:66`) | **[CODE-VERIFIED]** field present |
| `output_dir` | `config.output_dir` (`models.py:72`) — SAME dir backing `config.contract_path` (`output_dir / "return-contract.yaml"`, `models.py:98`) | **[CODE-VERIFIED]** field present |
| `diff` (unified diff/patch text I1) | **NO config field.** `config.base` is only a **ref**, not diff text — `config.py:95` docstring: "diff against this ref is the working-tree diff reflect computes downstream." The wrapper passes `--diff <BASE>` as a single ref to `/sc:reflect` (`runner.py:356`) and never computes/holds the unified diff itself. So `run_sweep(diff=...)` needs the diff text materialized: run `git diff <base>` against the working tree inside `_audit_once` (or inside `run_sweep`), reusing `config.base`. | **[UNVERIFIED]** no diff-text field — must compute from `config.base` |
| `availability_surface` (Wave-0 §0.5d backend/tool availability) | **NO config field, NO probe anywhere in `config.py`/`models.py`** (grep for `availability\|wave.?0\|probe\|backend.*avail` returned nothing). TDD §8.1.2 claims "from the Wave-0 availability probe already on the config" — this is INCORRECT against current source. Must be added: a probe in `_audit_once` (or `resolve_config`) producing a `dict`, OR pass `{}`/an empty surface that forces the rg/AST floor (D3 DEGRADE-to-floor default). | **[UNVERIFIED]** field + probe ABSENT — must add |
| `lsp` (keyword, optional) | `None` default → rg/AST floor only (D3). No config field needed for v1; precision overlay deferred. | **[CODE-VERIFIED]** default `None` is the v1 floor path |

**KEY FINDING (Q for builder):** Of the 6 positional args, only **3 map cleanly to existing config fields** (`base_ref`←`base`, `tasklist`←`tasklist_path`, `output_dir`←`output_dir`). The other **3 (`diff`, `scope_worktree`, `availability_surface`) have NO backing field** and the TDD's "already on the config" claim is unverified against source. The task MUST specify how each is produced (compute diff via `git diff config.base`; derive/add `scope_worktree`; add an availability probe or pass a floor-forcing empty surface).

`SweepResult` (TypedDict) returns `ledger_rows`, `scalars` (the six fields), `ledger_path` **[TDD §8.1.2, tdd.md:667-671]**.

---

## 2. Merge-overwrite point + ledger write location (DELIVER #2)

`_audit_once` current body (`runner.py:394-453`) **[CODE-VERIFIED]**. The chokepoint window is between the author branch (ends 444 `rc = proc.wait()` / 425 `rc = 0`) and the consume line:

```
runner.py:445   contract = parse_contract(config.contract_path)
runner.py:446   result = derive_verdict(contract, expected_tier=..., allow_single_vendor=..., child_rc=rc)
runner.py:452   result.contract_path = str(config.contract_path)
runner.py:453   return result
```

**Exact insertion point:** the `run_sweep(...)` call + both writes go **after line 444** (Tier-1 `rc = proc.wait()`) / after line 425 (Tier-2 `rc = 0`) and **strictly BEFORE line 445** (`parse_contract`). Concretely, a new block inserted between current `runner.py:444` and `runner.py:445` — both author branches join here, so a single post-branch insertion covers Tier-1 and Tier-2 in one place (this is exactly why `_audit_once` is the chokepoint; see §3).

**The two writes the new block performs** **[TDD §7.5 tdd.md:605-608, §11.1 step 4-5 tdd.md:757-758]**:

1. **Ledger** → `config.output_dir / "artifacts" / "runtime-surface-ledger.yaml"` (i.e. `<output>/artifacts/runtime-surface-ledger.yaml`). `mkdir(parents=True, exist_ok=True)` the `artifacts/` dir; serialize `SweepResult.ledger_rows` via `_IndentDumper` (nested block sequences `production_referrers:`) + `_atomic_write_text`.
2. **Six-field merge-overwrite** into `config.contract_path` (= `<output>/return-contract.yaml`, `models.py:98`): read the just-authored contract, overwrite the six `runtime_surface_*` keys (`runtime_surface_requirements`, `runtime_surface_sweep_ran`, `runtime_surface_ledger_path`, `runtime_surface_unreached`, `runtime_surface_degraded`, **`unreached_surfaces`** — note the 6th has NO `runtime_surface_` prefix; do NOT use a prefix glob), re-dump via `_IndentDumper` + `_atomic_write_text`.

**CRITICAL ordering caveat — the contract must already exist on disk before the merge.** Both author branches write `config.contract_path` *before* line 445: Tier-2 via `run_tier2_ensemble(config)` → `_emit_reflect_contract(config.contract_path, contract)` (`ensemble.py:309`); Tier-1 via the launched `/sc:reflect` child writing `return-contract.yaml` into `config.output_dir`. So the merge step at the chokepoint reads-then-overwrites an existing file. (Edge case for the task: a Tier-2 M==0 / contract-missing run leaves the top-level contract absent — `ensemble.py:179-182` — so the merge step must tolerate a missing contract, mirroring `_emit_reflect_contract`'s unlink-on-None branch and `parse_contract`'s contract-missing handling.)

---

## 3. Ordering invariant — EMIT before `parse_contract` (DELIVER #3)

**Why `_audit_once` is the chokepoint** **[TDD §6.4 D2 tdd.md:461, D4 tdd.md:463; §21 Alt 1 tdd.md:1264]**:

- It is **tier-agnostic**: both the Tier-1 `ClaudeProcess` branch (`runner.py:430-444`) and the Tier-2 `run_tier2_ensemble` branch (`runner.py:421-425`) converge on the SAME `parse_contract(config.contract_path)` at `runner.py:445`. One insertion before 445 covers both authors.
- It sits **exactly between contract-authoring and contract-consume** — the only point where the deterministic scalars can overwrite LLM-typed/ad-hoc values *before* `derive_verdict` and the §5.3 forbid-STOP pre-filter read them. This makes the `len(unreached_surfaces) == runtime_surface_unreached` count invariant hold by construction at read time (D4 rationale).
- **D4 ordering [tdd.md:463]:** sweep + merge-overwrite **before** `parse_contract`; sweep-after-parse is rejected (would let `derive_verdict` read stale LLM-authored values before the deterministic overwrite lands).

**Fix-loop re-run [CODE-VERIFIED `runner.py:561-562`]:**

```
runner.py:561   while True:
runner.py:562       result = self._audit_once()  # SAME --base reused every re-audit (NFR-4)
```

`_audit_once` is re-invoked once per fix iteration (after `_apply_remediation`, `runner.py:586`), each time with the SAME `config.base` (NFR-4 / NFR-002). Because the sweep is inside `_audit_once`, it **re-runs on every re-audit** with the same `base_ref` — the post-fix tree is re-swept and the six scalars re-merged into the freshly re-authored contract each cycle. The builder must place the sweep INSIDE `_audit_once` (not in `run()` once-only) so the fix-loop re-audit gets fresh deterministic scalars.

---

## 4. Tier-1 vs Tier-2 author paths + the version-constant inconsistency (DELIVER #4)

The author branch in `_audit_once` (`runner.py:419-444`) **[CODE-VERIFIED]**:

```
runner.py:419  expected_tier = 2 if config.depth in {"standard", "deep"} else 1
runner.py:421  if expected_tier == 2 and ClaudeProcess is _ProductionClaudeProcess:
runner.py:425      run_tier2_ensemble(config); rc = 0          # TIER-2 author
runner.py:427  else:
runner.py:430      proc = ClaudeProcess(prompt=self._build_prompt(), ...)   # TIER-1 author
runner.py:443      proc.start(); rc = proc.wait()
runner.py:445  contract = parse_contract(config.contract_path)   # JOIN POINT
```

- **Tier-1 (grounded `/sc:reflect` via `ClaudeProcess`):** the launched child authors `return-contract.yaml` into `config.output_dir`. Also taken when a **test double** has replaced `ClaudeProcess` (the `ClaudeProcess is _ProductionClaudeProcess` guard, `runner.py:421`) — so the mocked-suite and `depth=action`/Tier-1 paths flow here.
- **Tier-2 (real ensemble):** `run_tier2_ensemble(config)` (`runner.py:425`, `ensemble.py:166`) fans out workers and emits the contract via `_emit_reflect_contract(config.contract_path, contract)` (`ensemble.py:309`).

**Both author paths must be covered** by the sweep wiring — placing the call after the `if/else` (between 444 and 445) covers both with one insertion. **[TDD §6.4 D2, §11.1 step 2 tdd.md:755 "Tier-1 LLM or Tier-2 ensemble authors return-contract.yaml".]**

**Version-constant inconsistency (Q4) [CODE-VERIFIED + TDD §8.3 tdd.md:694]:**

- `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` (`ensemble.py:59`), emitted into the Tier-2 contract as `"contract_version": REFLECT_CONTRACT_VERSION` (`ensemble.py:501`).
- This is **stale vs the SKILL-declared `1.6.0`** (the version at which the six `runtime_surface_*` fields were added, additive). The Tier-2 ensemble contract therefore carries `contract_version: "1.0"` while the producer/SKILL declare `1.6.0`.
- The port must reconcile this (bump the constant, or document why the ensemble path carries a different literal) so producer and declared version do not silently disagree. **OQ-DRS.3: likely no version bump** because the six fields are additive + read-and-ignore forward-compatible — but the `1.0` vs `1.6.0` disagreement on the Tier-2 path is a separate, real defect the task should flag.

---

## 5. MANDATORY writer convention — `_IndentDumper` + `_atomic_write_text` (DELIVER #5)

Both new writes (ledger + contract merge) MUST use the runner-local writer convention, **NOT** the ensemble's bare `safe_dump` + `write_text`. Signatures **[CODE-VERIFIED `runner.py:58-89`]**:

```python
class _IndentDumper(yaml.SafeDumper):                       # runner.py:58
    def increase_indent(self, flow=False, indentless=False):  # runner.py:66
        return super().increase_indent(flow, False)

def _atomic_write_text(path: Path, text: str) -> None:      # runner.py:70
    # randomized same-dir temp (.{name}.tmp.{pid}.{uuid}) + os.replace; finally-unlink
```

Canonical dump idiom already used in-file (e.g. `write_sidecar`, `runner.py:228-236`):

```python
_atomic_write_text(path, yaml.dump(data, Dumper=_IndentDumper, sort_keys=False,
                                   default_flow_style=False, allow_unicode=True))
```

**Why mandatory [TDD §7.5 note tdd.md:610]:** nested block sequences (`unreached_surfaces:`, `production_referrers:`) require `_IndentDumper` or pre-commit yamllint (`indent-sequences: true`) fails. The ensemble's bare path is the ANTI-pattern to avoid:

- `ensemble.py:634-635` **[CODE-VERIFIED]**: `text = yaml.safe_dump(contract, sort_keys=False, allow_unicode=True)` then `path.write_text(text, encoding="utf-8")` — bare `safe_dump` (no `_IndentDumper`, indentless sequences) + non-atomic `write_text`.

The builder must write the wiring item to explicitly reuse `runner._IndentDumper` + `runner._atomic_write_text` (both already module-local in `runner.py`, no import needed since the call site is in the same module). Do NOT copy the ensemble idiom.

---

## 6. Bare `claude -p` coverage gap — D2 / OQ-DRS.2 (DELIVER #6)

**`_audit_once` does NOT cover bare `claude -p "/sc:reflect ..."`** **[TDD §6.4 D2 tdd.md:461, §21 Alt 1 tdd.md:1270, R2 risk tdd.md:1223]**:

- `_audit_once` covers only `superclaude reflect run` (foreground, `--tmux` inner re-invocation, and the fix loop) — all of which enter the Python wrapper via `commands.run` → `ReflectRunner(config).run()` (`commands.py:254`).
- A direct `claude -p "/sc:reflect --mode post …"` never enters `commands.py`/`runner.py` at all, so a sweep wired ONLY into `_audit_once` leaves the bare path still LLM-emitting the six scalars.

**Therefore the SKILL demotion (Phase 4) cannot be unconditional** — it must branch on a "the module ran" detection signal:

- **Detection signal:** presence of **`runtime_surface_sweep_ran`** in `return-contract.yaml` **[TDD §6.4 D2 tdd.md:461, §8.2 tdd.md:682]**. When the Python sweep ran (runner-driven path), it authoritatively writes the six fields and sets `runtime_surface_sweep_ran: true` for surface diffs. Where the sweep did NOT run (bare `claude -p`), the SKILL retains the LLM emission as an explicit documented fallback.
- This delivery's wiring (`_audit_once`) handles ONLY the runner-driven paths; full bare-path coverage is a separate Wave-1A skill shell-out to the same importable module (§21 Alt 1, out of this seam's scope — owned by R6/SKILL).

**Builder note:** this seam's task items cover the runner-driven deterministic write; the SKILL-side conditional fallback (R6) keys off `runtime_surface_sweep_ran`. The two must agree on that exact field name as the detection contract.

---

## 7. Summary for the builder (precise wiring facts)

**The single insertion point:** add a `run_sweep(...)` call + two atomic writes in `runner._audit_once`, **between current `runner.py:444` and `runner.py:445`** (after both author branches join; strictly before `parse_contract`). Inside `_audit_once` (NOT `run()`) so the fix-loop re-audit at `runner.py:561-562` re-sweeps with the same `config.base` each cycle.

**Arg construction (3 clean, 3 gaps):**
- Clean: `base_ref=config.base`, `tasklist=config.tasklist_path`, `output_dir=config.output_dir`. **[CODE-VERIFIED]**
- GAPS the task MUST resolve: `diff` (compute `git diff config.base` vs working tree — no diff-text field exists), `scope_worktree` (no field — derive `Path.cwd()` or add a config field), `availability_surface` (no field, no Wave-0 probe exists — add one or pass a floor-forcing empty dict). The TDD §8.1.2 "already on the config" claim is **wrong against current source** for these three. `lsp=None` for v1.

**Two writes (both via `runner._IndentDumper` + `runner._atomic_write_text`, same-module, no import):**
1. Ledger → `<output>/artifacts/runtime-surface-ledger.yaml` (mkdir `artifacts/` first).
2. Merge-overwrite the six fields into `config.contract_path` (`<output>/return-contract.yaml`); the 6th field `unreached_surfaces` has NO prefix — key on exact names, never a `startswith("runtime_surface_")` glob.

**Tier coverage:** both Tier-1 (`ClaudeProcess` / mocked-double, `runner.py:430-444`) and Tier-2 (`run_tier2_ensemble`, `runner.py:425`) author `config.contract_path` before line 445 → one post-join insertion covers both. Tolerate a Tier-2 M==0 contract-missing run (`ensemble.py:179-182`).

**Defect to flag:** `ensemble.REFLECT_CONTRACT_VERSION = "1.0"` (`ensemble.py:59`, emitted at `ensemble.py:501`) is stale vs SKILL `1.6.0` — reconcile (Q4 / §8.3).

**Bare-path gap:** `_audit_once` does NOT cover bare `claude -p /sc:reflect`; SKILL demotion stays conditional, branching on `runtime_surface_sweep_ran` presence in the contract (detection contract shared with R6).

**Anti-pattern to avoid:** ensemble's bare `yaml.safe_dump` + `path.write_text` (`ensemble.py:634-635`) — do NOT copy it.

**Status:** Complete — 2026-06-22.
