# Research 01 — Reflect CLI Surface (exact per-file change points D1–D7)

- **Topic:** reflect CLI package change points for the audit→fix→verify→promote evolution (D1–D7).
- **Scope:** `src/superclaude/cli/reflect/{commands,config,runner,models,contract}.py` + `cli/main.py` (reflect registration). Canonical base = worktree `wrapper-onto-master`.
- **Status:** Complete
- **Date:** 2026-06-10
- **Evidence rule:** every claim cites `relative/path.py:line` against the canonical base. Builder items must reference these RELATIVE paths (never the worktree absolute path).

> Cross-team note: this is the **wrapper** worktree's view of what the wrapper engine itself must change. R2 covers the reflect SKILL contract/refs (FR-8/FR-9 emission of `remediation_task_path`, headless `--remediate`); R3 covers ClaudeProcess API + tests + thinness guards. Where this file touches those, it is only to name the call site the builder will wire.

---

## 0. Decision → file map (orientation)

| Decision | Primary file(s) | Anchor lines |
|----------|-----------------|--------------|
| D1 fix-loop | `commands.py`, `runner.py`, `config.py`, `models.py` | commands `108-203`, runner `378-501`, config `111-222`, models `66-81` |
| D2 marker self-suppress | `commands.py` (command entry) | `108-130` (insert before `resolve_config`) |
| D3 `--max-fix-iterations` | `commands.py`, `config.py`, `models.py`, `runner.py` | commands option block `62-107`, config sig `111-127`, models `66-81`, runner loop |
| D4 classifier + FR-8 | `contract.py` | `_halted_reason` `304-325`, new pure classifier; `parse_contract` `65-82` |
| D5 promote flip | `commands.py` | `--promote/--no-promote` default `70-75` |
| D6 `--base` precedence | `commands.py`, `config.py`, `models.py` | commands option block, config `_resolve_base` `81-93` + `resolve_config` `111-222`, models field |
| D7 depth passthrough | `commands.py` `82-87` | **already present — no change** (FR-7 confirms `_DEFAULT_MAX_TURNS=250`, no `--max-turns` flag) |

---

## 1. D1 + D5 + D6 + D3 + D2 — `commands.py`

### 1a. D5 — promote-default flip (the `@click.option` block)

`commands.py:70-75` — current:

```python
@click.option(
    "--promote/--no-promote",
    "promote",
    default=False,
    help="Allow reflect's gated Wave-7 promotion (default: --no-promote, audit-only).",
)
```

**Change:** flip `default=False` → `default=True`; update help to say promote is the default (FR-5 / contract §5: O1 promote-by-default). Note the `task` adapter is reflect's, not the wrapper's — wrapper only passes/drops `--promote` to the audit prompt (see runner `_build_prompt` 336-337 below). Caveat for D5/FR-5 O2 scope: the wrapper itself does NOT force `--no-promote` for O2 — the **generator** emits `--no-promote` on the O2 gate line (contract §5; merged-requirements FR-5). So the only wrapper-side change for D5 is the default flip. **Unverified whether builder also wants a wrapper-side "O2 detection" — none exists in the canonical base; per contract §5 O2 forcing is the generator's job, so no wrapper code is needed. Recommend NO wrapper-side O2 auto-force.**

### 1b. D6 — new `--base` option

There is **no** `--base` option today. Option block runs `commands.py:62-107`; the `run()` signature is `commands.py:108-119`. Add:

```python
@click.option(
    "--base",
    "base_override",
    default=None,
    help="Explicit audit base ref (single ref vs working tree). Highest precedence over frontmatter start_commit + merge-base.",
)
```

- Add `base_override: str | None` to the `run()` parameter list (`commands.py:108-119`).
- Thread it into the `resolve_config(...)` call (`commands.py:131-144`) as `base_override=base_override`.
- Forward it through the tmux inner-command rebuild `_build_inner_command` (`commands.py:233-255`): currently rebuilds `--output/--depth/--timeout/--promote/--allow-single-vendor/--resume` (lines 235-254) but NOT base — add `if config.base_override: cmd += ["--base", config.base_override]` so the inner foreground reinvocation under `--tmux` preserves the pinned base. **This is a real gap: without it, `--tmux` + `--base` silently loses the base in the inner run.**

### 1c. D3 — `--max-fix-iterations` + D1 — `--fix/--no-fix`

Neither flag exists today. Add to the option block (`commands.py:62-107`):

```python
@click.option(
    "--fix/--no-fix",
    "fix",
    default=False,   # library default off; gate callers pass --fix (contract §2)
    help="Run the bounded audit→apply→re-verify auto-fix loop (gate default --fix).",
)
@click.option(
    "--max-fix-iterations",
    type=int,
    default=2,
    help="Max apply→verify cycles before terminal HALT (D3, default 2).",
)
```

- Add `fix: bool` and `max_fix_iterations: int` to `run()` signature (`commands.py:108-119`).
- Thread both into `resolve_config(...)` (`commands.py:131-144`).

> NOTE on the gate default: contract §2 / merged-requirements FR-1 say the **gate** default is `--fix`. The generators always pass `--fix` explicitly (contract §2 invocation shapes). So the Click default may be either; recommend `default=False` (library-thin, explicit-at-gate) — **flag this as a builder decision**, the brainstorm text in merged-requirements FR-1 says "gate default `--fix`" which is satisfied by the generator emitting `--fix`, not by the Click default. Unverified which the builder prefers; both honor the contract.

### 1d. D2 — `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` self-suppress guard

Where it must sit: at the **very top of `run()`**, before the `from .config import resolve_config` lazy import at `commands.py:126` and before any `resolve_config` call (`commands.py:131-144`). Contract §3 + merged-requirements FR-2 / state-machine line `39`: "reads the marker at startup; if `=1`, immediately exits 0 before any audit."

Insert at `commands.py:120` (start of the `run()` body, right after the docstring `120-125`):

```python
if os.environ.get("SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE", "").strip() == "1":
    click.echo("reflect-wrapper recursion breaker: nested gate suppressed", err=True)
    sys.exit(0)
```

`os` and `sys` are already imported (`commands.py:19,21`). Truthy value is EXACTLY the string `"1"` (contract §3 last line: absent/empty/any-other ⇒ not suppressed). This guard must run even for `--dry-run`/`--print-command` per the state machine (the breaker is the first node). **Unverified whether dry-run should bypass the breaker** — the state machine (`merged-requirements:39`) puts the breaker FIRST, before the dry-run branch, so put it before everything. Recommend: breaker first, unconditionally.

### 1e. Where the fix-loop is invoked from `commands.py`

The foreground path is `commands.py:188`: `result = ReflectRunner(config).run()`. The fix-loop is orchestrated INSIDE `ReflectRunner.run()` (see §3) so `commands.py` keeps calling `.run()` once and reads `result.verdict.exit_code` (`commands.py:189`). No structural change to the command's result-handling (`commands.py:196-203`) is required beyond the new flags — the loop is fully encapsulated in the runner. The sentinel write (`commands.py:191-194`) and exit (`commands.py:203`) stay.

---

## 2. D6 — `_resolve_base` precedence (`config.py`)

### Current chain — `config.py:81-93`

```python
def _resolve_base(cwd: Path, frontmatter: dict[str, str], base_branch: str) -> str:
    start_commit = frontmatter.get(_FRONTMATTER_START_COMMIT_KEY, "").strip()
    if start_commit:
        return start_commit
    try:
        return _git(cwd, "merge-base", "HEAD", base_branch)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError("base-unresolved") from exc
```

Today: `start_commit` else `merge-base HEAD master`. Called once at `config.py:168` (`base = _resolve_base(git_cwd, frontmatter, base_branch)`).

### New precedence (FR-6): `--base` > frontmatter `start_commit` > merge-base

Add a `base_override: str | None = None` param to `_resolve_base` and short-circuit first:

```python
def _resolve_base(cwd, frontmatter, base_branch, base_override=None):
    if base_override and base_override.strip():
        return base_override.strip()
    start_commit = frontmatter.get(_FRONTMATTER_START_COMMIT_KEY, "").strip()
    if start_commit:
        return start_commit
    try:
        return _git(cwd, "merge-base", "HEAD", base_branch)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError("base-unresolved") from exc
```

Preserve the F3 de-range invariant — `--base` is a SINGLE ref, never `<base>..HEAD` (FR-6; runner `_build_prompt:344` already emits `["--diff", config.base]` single ref — see §3b). No `..` parsing/splitting is added; `base_override` is stored verbatim.

### `resolve_config` signature + `ReflectConfig` construction

- `resolve_config` signature: `config.py:111-127`. Add keyword-only `base_override: str | None = None` (alongside `promote`, `tmux`, etc. at `config.py:121-126`).
- Pass it into the `_resolve_base` call at `config.py:168`: `base = _resolve_base(git_cwd, frontmatter, base_branch, base_override=base_override)`.
- `ReflectConfig(...)` construction is `config.py:205-222`. Add the three new fields here (values threaded from new params): `base_override=base_override`, `fix=fix`, `max_fix_iterations=max_fix_iterations`. Also add `fix: bool = False` and `max_fix_iterations: int = 2` to the `resolve_config` signature (`config.py:111-127`).

Constants already present and reusable: `_FRONTMATTER_START_COMMIT_KEY = "start_commit"` (`config.py:51`), `_DEFAULT_BASE_BRANCH = "master"` (`config.py:44`).

---

## 3. D1 — fix-loop orchestration (`runner.py`)

### 3a. Current `ReflectRunner.run()` structure — `runner.py:378-501`

Single-shot, no loop. Steps (current line anchors):
1. `expected_tier` computed `381`.
2. `preflight(config)` `384`.
3. `prompt = self._build_prompt()` `387`.
4. dry-run/print-command early return `391-404`.
5. `env_alias_count` `407`.
6. preflight-blocker → BLOCKED + sidecar return `410-428`.
7. resume short-circuit `431-455`.
8. **launch:** `ClaudeProcess(...)` construction `459-468`, `proc.start()` `469`, `rc = proc.wait()` `470`.
9. parse contract + derive verdict `473-480`.
10. write-back + sidecar `483-500`, return `501`.

This is the ONE audit the fix loop must wrap. The cleanest builder shape: extract steps 8-9 (launch + parse + derive) into a private `_audit_once() -> ReflectResult` helper, then wrap it in a loop in `run()`. The loop:

```
iteration = 1; max = config.max_fix_iterations
while True:
    result = _audit_once()            # steps 8-9 (launch + parse + derive)
    classification = classify_fix(result, contract)   # §4, contract.py pure fn
    if result.verdict is PASS: break
    if not config.fix: break          # audit-only, no loop
    if classification != AUTO_FIXABLE: break   # HUMAN-REQUIRED / DEGRADED / BLOCKED → terminal
    rtp = contract.get("remediation_task_path")
    if not rtp: break                 # cannot repair → terminal HALT (FR-4 / table line 182)
    if iteration > max: break         # FR-3 bound
    _apply_remediation(rtp)           # §3c: export marker + claude --print "/task <rtp>"
    iteration += 1
fix_iterations = iteration - 1
fix_converged = (result.verdict is PASS)
# then write-back + sidecar (steps 10), record fix_iterations/fix_converged
```

State-machine source: `merged-requirements:33-80`. The marker self-suppress (D2) is in `commands.py` per §1d, NOT here — but the runner MUST export the marker into the CHILD env for BOTH the audit subprocess and every `/task` apply (contract §3.1 / FR-2).

### 3b. `_build_prompt` — the `--diff <BASE>` single-ref line + `--remediate`

`runner.py:331-352`. Key line `344`: `parts += ["--diff", config.base]` — single ref (the F3 de-range, comment `338-343`). `config.base` already carries the resolved base (now `--base`-aware via §2), so **no change to line 344 needed** for D6 — the precedence is resolved upstream in config.

**FR-1 `--remediate` append (NEW):** when `config.fix`, append `--remediate` so reflect AUTHORS (never runs) the corrective MDTM. Insert after the `--depth` append (`runner.py:348`) or near `--output` (`351`):

```python
if config.fix:
    parts += ["--remediate"]
```

Current `_build_prompt` emits (in order): `/sc:reflect --mode post [--no-promote] --diff <base> --tasklist <path> [--spec <path>] --depth <d> [--executor-model <m>] --output <dir>` (`runner.py:334-352`). The `--no-promote` is conditional on `not config.promote` (`336-337`) — with D5 flipping the default to promote, the audit prompt will normally OMIT `--no-promote` (matching O1). **Cross-check needed (R2): does the reflect skill accept `--remediate`?** FR-9 says reflect's headless `--remediate` must auto-author under `--print`. This is R2's emission side; the wrapper only appends the flag.

### 3c. How `ClaudeProcess` is constructed/launched + marker export

Current construction `runner.py:459-468`:
```python
proc = ClaudeProcess(
    prompt=prompt,
    output_file=config.output_dir / "reflect-stdout.json",
    error_file=config.output_dir / "reflect-stderr.log",
    model=config.model,
    timeout_seconds=config.timeout_seconds,
    max_turns=config.max_turns,
    output_format="stream-json",
    env_vars=None,  # FR-10: bare real-env overlay (no custom scrub).
)
proc.start(); rc = proc.wait()  # 469-470
```

**Marker export (FR-2 / contract §3.1):** today `env_vars=None` (line 467) → `ClaudeProcess.build_env()` overlays the bare real env. To export `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` into the child, the audit + the `/task` apply must pass `env_vars={"SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE": "1"}` (merged with real env). **R3 owns the exact `ClaudeProcess` env-merge semantics** — `_child_env()` at `runner.py:228-241` builds a probe via `build_env()`; the builder must confirm whether `env_vars` is overlaid-on-top-of or replaces real env (R3). The `/task` apply subprocess is a NEW second `ClaudeProcess` with `prompt=f"/task {remediation_task_path}"`, same model/timeout/max_turns, plus the marker env. Note: per contract §3 the audit subprocess ALSO gets the marker — but the audit must NOT self-suppress (it's `/sc:reflect`, not `superclaude reflect run`, so the §1d guard doesn't fire on it). The marker only suppresses nested `superclaude reflect run` calls reached via the auto-run `/task`'s own terminal gate.

### 3d. `write_sidecar` fields — add `fix_iterations` / `fix_converged`

`write_sidecar` is `runner.py:181-225`. The `data` dict is built `runner.py:197-213`. Add two keys:
```python
"fix_iterations": result.fix_iterations,
"fix_converged": result.fix_converged,
```
(after `write_status` at line 212, or wherever field-order is chosen). These come from new `ReflectResult` fields (§5). `write_sidecar` is called from 3 sites — `commands.py:173` (config-error path), `runner.py:422-427` (preflight-blocker), `runner.py:449-454` (resume), `runner.py:495-500` (main). Default the new `ReflectResult` fields so the non-fix paths serialize cleanly (e.g. `fix_iterations=0`, `fix_converged` mirrors `verdict is PASS` or `None`). **Builder note:** the config-error sidecar in `commands.py:162-178` constructs a `ReflectResult` by hand — new fields need defaults or that call breaks.

Also surface them in the `reflect_post:` write-back: `_build_reflect_post_value` (`runner.py:83-107`) builds the frontmatter mapping `91-107` — optionally add `fix_iterations`/`fix_converged` there too (FR-3 says sidecar records them; frontmatter is optional — **Unverified** whether the contract requires them in `reflect_post:`; merged-requirements FR-3 only names the sidecar. Recommend sidecar-only to stay minimal).

---

## 4. D4 — classifier + FR-8 (`contract.py`)

### 4a. `derive_verdict` / `_halted_reason` — which fields → HALTED

`derive_verdict` `contract.py:127-243` (first-match-wins blocked→degraded→halted→pass). `_halted_reason` `contract.py:304-325` returns the first halted slug:
- `status == "failed"` → `status-failed` (`308-309`)
- `status == "partial"` → `status-partial` (`310-311`)
- `regression_present is True` → `regression` (`312-313`)
- `unauthorized_deviation_present is True` → `unauthorized-deviation` (`314-315`)
- `needs_human_decision is True` → `needs-human-decision` (`316-317`)
- `user_decision_required is True` → `user-decision-required` (`318-319`)
- `deviations["regression"] > 0` → `regression` (`320-322`)
- `deviations["drift"] > 0` → `drift` (`323-324`)

The HUMAN-REQUIRED trigger fields (contract §4 / merged-requirements FR-4) are EXACTLY: `regression_present`, `needs_human_decision`, `user_decision_required`, `unauthorized_deviation_present`, non-empty grounding-gaps, plus DEGRADED/BLOCKED verdicts. All of these except grounding-gaps are already read in `_halted_reason`. The DEGRADED/BLOCKED carve happens upstream in `derive_verdict` (degraded `208-222`, blocked `144-206`).

**grounding-gaps:** `needs_human_decision` is defined in contract §4 as `= grounding-gaps non-empty`. So the classifier can rely on `needs_human_decision` as the proxy. **Unverified** whether the contract ALSO carries a separate `grounding_gaps` list field that the classifier should read independently — `_halted_reason` does NOT read a `grounding_gaps` field today; it reads `needs_human_decision` only. R2 should confirm reflect emits `needs_human_decision: true` whenever grounding-gaps is non-empty (FR-4 equivalence). Recommend: classifier reads `needs_human_decision` (the bool), matching the existing `_halted_reason` field set — do NOT add a new grounding-gaps parse unless R2 confirms a distinct field.

### 4b. New pure AUTO-FIXABLE-vs-HUMAN-REQUIRED classifier

Where it lives: `contract.py` (pure module, off existing fields — merged-requirements §9 "add the AUTO-FIXABLE vs HUMAN-REQUIRED classifier (pure, off existing fields)"). It takes the parsed `contract: dict` (and/or the derived `ReflectResult.deviations`) and returns an enum/string. Mechanically (contract §4 / table `merged-requirements:171-184`):

```python
def classify_fix(contract: dict, deviations: dict[str, int]) -> str:
    # HUMAN-REQUIRED if any hard signal:
    if (contract.get("regression_present") is True
        or contract.get("needs_human_decision") is True
        or contract.get("user_decision_required") is True
        or contract.get("unauthorized_deviation_present") is True
        or deviations.get("regression", 0) > 0):
        return "human-required"
    # AUTO-FIXABLE iff halted solely by drift>0 and/or necessary-class:
    if deviations.get("drift", 0) > 0 or deviations.get("necessary", 0) > 0:
        return "auto-fixable"
    return "none"  # nothing to fix (already pass-shaped)
```

This is invoked by `runner.run()` (§3a) AFTER `derive_verdict` returns HALTED. DEGRADED/BLOCKED verdicts are terminal upstream — the classifier is only consulted on a HALTED result. **Builder must place it as a pure function in `contract.py` with NO Click/subprocess import (the module's purity invariant, `contract.py:5-8`).** The existing `_extract_deviations` (`contract.py:90-101`) yields the 4-key int dict the classifier needs.

### 4c. FR-8 — surface `remediation_task_path`

Today `parse_contract` (`contract.py:65-82`) returns the raw dict (read-and-ignore unknown fields, `71`), so `remediation_task_path` is ALREADY accessible via `contract.get("remediation_task_path")` once reflect emits it (R2's FR-8 emission). No parse change strictly required — but the builder should:
- surface it onto `ReflectResult` (new field, §5) so the runner's loop reads it without re-touching the raw dict, AND
- optionally record it in the sidecar (`write_sidecar` data dict, `runner.py:197-213`).

`_make_result` (`contract.py:104-124`) builds `ReflectResult` from contract fields — add `remediation_task_path=c.get("remediation_task_path")` here so it's populated on every derived result. **Cross-team:** the FIELD itself is emitted by reflect (R2 / FR-8, contract `1.4.0`); the wrapper only reads it. The wrapper MUST NOT guess "newest TASK-RF-* dir" (FR-8 explicit).

---

## 5. `models.py` — `ReflectConfig` / `ReflectResult` new fields

### `ReflectConfig` — `models.py:57-86` (fields `66-81`)

Add three fields (alongside `promote: bool` at `models.py:76`):
```python
base_override: str | None
fix: bool
max_fix_iterations: int
```
Dataclass has no defaults today (all positional-ish via construction in `config.py:205-222`), so add them with explicit values at construction (§2). **If the builder wants defaults**, they must go AFTER all non-default fields (Python dataclass rule) — current fields `66-81` are all non-default, so appending `base_override`, `fix`, `max_fix_iterations` (with or without defaults) at the end is safe. The `contract_path` property `83-86` is unaffected.

### `ReflectResult` — `models.py:89-111` (fields `98-106`)

Add (after `write_status: str = ""` at `models.py:106`, keeping default-fields-last):
```python
fix_iterations: int = 0
fix_converged: bool = False
remediation_task_path: str | None = None
```
All three have defaults so the 4 hand-built `ReflectResult(...)` call sites stay valid:
- `commands.py:162-171` (config-error BLOCKED)
- `runner.py:411-421` (preflight blocker)
- `runner.py:438-448` (resume)
- `contract.py:114-124` (`_make_result`, the main path)
- `runner.py:394-404` (dry-run)

The `outcome` property `108-111` is unaffected.

---

## 6. D7 — depth passthrough (NO change)

`commands.py:82-87` `--depth` Choice(`standard`,`deep`) and `config.py:174-175` quick-floor are ALREADY correct (FR-7). `_DEFAULT_MAX_TURNS=250` (`config.py:39`) already covers a deep T2 run; FR-7 confirms **no `--max-turns` flag** is added (Section-9 option set stays exact). The runner already passes `max_turns=config.max_turns` to `ClaudeProcess` (`runner.py:465`). **No task item needed for D7 beyond confirming callers pass `--depth deep` (generator-side, contract §2).**

---

## 7. `main.py` registration (NO change)

`cli/main.py:440-442`:
```python
from superclaude.cli.reflect.commands import reflect_group  # noqa: E402,I001
main.add_command(reflect_group, name="reflect")
```
Registration is already wired (`run` is a subcommand of `reflect_group`). New options on `run` need NO main.py change. NFR-5 (`pipx install --force` exposes the command) is a build/install step, not a code change here. **No task item for main.py.**

---

## 8. Summary — per-file builder checklist seeds

**`cli/reflect/commands.py`**
1. (D2) Insert marker self-suppress guard at top of `run()` body (~`commands.py:120`), before lazy import `126` / `resolve_config` `131` — `exit 0` when `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE == "1"`. `os`/`sys` already imported (`19`,`21`).
2. (D5) Flip `--promote/--no-promote` default `False`→`True` (`70-75`); update help.
3. (D6) Add `--base/base_override` option; add to `run()` sig (`108-119`); thread to `resolve_config` (`131-144`); add to `_build_inner_command` tmux rebuild (`233-255`) — **gap fix**.
4. (D1/D3) Add `--fix/--no-fix` + `--max-fix-iterations` options; add to `run()` sig; thread to `resolve_config`.
5. Config-error hand-built `ReflectResult` (`162-171`) — supply new field defaults.

**`cli/reflect/config.py`**
6. (D6) `_resolve_base` (`81-93`): add `base_override` param, short-circuit first (precedence `--base` > start_commit > merge-base).
7. (D6/D1/D3) `resolve_config` sig (`111-127`): add `base_override`, `fix`, `max_fix_iterations`; pass `base_override` into `_resolve_base` call (`168`); add `base_override`/`fix`/`max_fix_iterations` to `ReflectConfig(...)` (`205-222`).

**`cli/reflect/runner.py`**
8. (D1) Extract `_audit_once()` from `run()` steps 8-9 (`459-480`); wrap in bounded loop in `run()` (`378-501`) per §3a state machine.
9. (FR-1) `_build_prompt` (`331-352`): append `--remediate` when `config.fix` (after `--depth` `348`). `--diff <base>` line `344` unchanged (D6 resolved upstream).
10. (FR-2) Export `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` into audit + `/task`-apply child `env_vars` (`459-468` + new apply subprocess). **Confirm env-merge semantics with R3.**
11. (D1) New `_apply_remediation(path)` — second `ClaudeProcess` with `prompt=f"/task {path}"`, same model/timeout/max_turns + marker env.
12. (D3) `write_sidecar` data dict (`197-213`): add `fix_iterations`, `fix_converged`.

**`cli/reflect/contract.py`**
13. (D4) Add pure `classify_fix(contract, deviations)` → `auto-fixable|human-required|none` (off existing fields; HUMAN-REQUIRED = regression/needs_human/user_decision/unauthorized/regression>0). Keep module purity (no Click/subprocess).
14. (FR-8) `_make_result` (`104-124`): add `remediation_task_path=c.get("remediation_task_path")`.

**`cli/reflect/models.py`**
15. `ReflectConfig` (`66-81`): add `base_override: str | None`, `fix: bool`, `max_fix_iterations: int`.
16. `ReflectResult` (`98-106`): add `fix_iterations: int = 0`, `fix_converged: bool = False`, `remediation_task_path: str | None = None` (defaults — keep 5 hand-built call sites valid).

**`cli/main.py`** — no change (already registered `440-442`).
**`--depth`/`--max-turns`** — no change (FR-7; `config.py:39`, `commands.py:82-87`).

### Open / Unverified items for the builder
- U1: Click default for `--fix` — `False` (recommended, generators pass `--fix` explicitly) vs `True`. Both honor contract §2. (§1c)
- U2: Whether D2 breaker runs before OR after the dry-run branch — state machine puts it FIRST; recommend unconditional-first. (§1d)
- U3: `env_vars` overlay-vs-replace semantics for the marker export — **R3 owns ClaudeProcess env API.** (§3c)
- U4: Whether reflect emits a distinct `grounding_gaps` field or only `needs_human_decision` — **R2 owns the skill contract.** Classifier currently keys off `needs_human_decision`. (§4a)
- U5: Whether `fix_iterations`/`fix_converged` also belong in `reflect_post:` frontmatter (FR-3 names sidecar only — recommend sidecar-only). (§3d)
- U6: Whether the wrapper should auto-force `--no-promote` for O2 — canonical base has no O2 detection; contract §5 makes O2 the GENERATOR's job. Recommend NO wrapper-side O2 force. (§1a)
