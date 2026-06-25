# Research: Reflect Package Launch/Config/Result Surface

- **Topic type:** File Inventory + Patterns (TRACK 1 of 1)
- **Scope:** `src/superclaude/cli/reflect/{runner,config,models,commands,__init__}.py`
- **Repo:** /config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3
- **Status:** In Progress
- **Date:** 2026-06-20

## Package file inventory (ground truth)

`src/superclaude/cli/reflect/` contains (sizes from `ls -la`):

| File | Bytes |
|---|---|
| `__init__.py` | 1131 |
| `commands.py` | 12561 |
| `config.py` | 9244 |
| `contract.py` | 14038 (R2 scope) |
| `models.py` | 3954 |
| `runner.py` | 25188 |

**`ensemble.py` — CONFIRMED ABSENT (NET-NEW).** `ls` of the package directory returns `No such file or directory` for `ensemble.py`. FR-RH2 must create it.

---

## 1. `runner.py` — the seam (anchor verification)

**Isolation guardrail comment block (top of file):** `runner.py:8-12` — module-docstring block forbidding the disallowed launch surfaces:
- `runner.py:9` — "No imports from `superclaude.cli.sprint` or `superclaude.cli.roadmap`."
- `runner.py:10` — "Zero `async def` / `await`."
- `runner.py:11-12` — "The only reflect-launch path is `ClaudeProcess` (subprocess) -- never an Agent/Task surface (NFR-7)."

**`_audit_once` method — full range: `runner.py:392-428`** (`def _audit_once(self) -> ReflectResult:` at L392; `return result` at L428).

**The `expected_tier` line — `runner.py:403`** (EXACT quote):
```python
        expected_tier = 2 if config.depth in {"standard", "deep"} else 1
```

**The Tier-2 launch block (THE SEAM where ensemble.py branches in) — `runner.py:405-419`.** This is the single-`ClaudeProcess` launch:
```python
        proc = ClaudeProcess(
            prompt=self._build_prompt(),
            output_file=config.output_dir / "reflect-stdout.json",
            error_file=config.output_dir / "reflect-stderr.log",
            model=config.model,
            timeout_seconds=config.timeout_seconds,
            max_turns=config.max_turns,  # G1: explicit, never the primitive's 100.
            output_format="stream-json",
            # Contract 3.1: marker exported into the audit child too. ...
            env_vars={_WRAPPER_MARKER: "1"},
        )
        proc.start()
        rc = proc.wait()
```
(`proc.start()` = L418, `rc = proc.wait()` = L419.) The FR-RH2 re-route would branch here: when `expected_tier == 2` and a swarm transport is selected, dispatch the reviewer ensemble through the swarm library instead of (or in addition to) this single `ClaudeProcess`.

**The parse + derive tail — `runner.py:420-428`:**
```python
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
`parse_contract` = L420, `derive_verdict(...)` = L421-426, `result.contract_path = ...` = L427, `return result` = L428.

**Imports already present (top of runner.py):** `from superclaude.cli.pipeline.process import ClaudeProcess` (L31); `from .contract import classify_fix, derive_verdict, parse_contract` (L33); `from .models import ReflectConfig, ReflectResult, Verdict` (L34). The `_MODEL_ALIAS_ENV_VARS` tuple (L37-41) and `_WRAPPER_MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` (L53) are module-level. `count_model_aliases` (L254-261) already counts the 3 `ANTHROPIC_DEFAULT_*_MODEL` aliases used for Tier-2 diversity.

---

## 2. `runner.py` — prompt / fix-loop / write-back / sidecar / max_turns

**`_build_prompt` — `runner.py:341-366`** (`def _build_prompt(self) -> str:` at L341; `return " ".join(parts)` at L366). Composes the `/sc:reflect --mode post ... --depth <depth> ... --output <dir>` stdin prompt. `--depth config.depth` is appended at **L358**. `--remediate` added under `--fix` at L361-362.

**`run()` fix-loop structure — `runner.py:453-597`** (`def run(self) -> ReflectResult:` at L453). Sequence:
- (1) preflight L458; (2) build prompt L461; (3) dry-run/print short-circuit L465-478;
- env alias count L481; preflight-blocker → BLOCKED L484-502;
- (3.5) resume short-circuit L505-529;
- (4-5) **bounded `while True` audit→classify→apply→re-verify loop L534-572** — calls `self._audit_once()` at **L537**, PASS break L539-540, audit-only (no `--fix`) break L542-543, untrusted (not HALTED) break L547-548, classify carve-out L550-551, remediation pointer L554-556, FR-3 bound break L558-559, apply L561, fail-closed break L562-571, `iteration += 1` L572;
- bookkeeping L575-576;
- (6) write-back + sidecar L579-596.

**`write_reflect_post` (FR-6 fail-closed) — `runner.py:117-185`** (`def write_reflect_post(...)` L117; `return "written"` L185). The race guard returns `"frontmatter-stale"` at L182; `"frontmatter-missing"` at L148. The PASS→BLOCKED demotion when the write is not `"written"` is in `run()` at **`runner.py:588-590`**:
```python
        if write_status != "written" and result.verdict is Verdict.PASS:
            result.verdict = Verdict.BLOCKED
            result.reason = write_status or "frontmatter-unwritable"
```

**`write_sidecar` (FR-7 always-write) — `runner.py:188-235`** (`def write_sidecar(...)` L188; `return sidecar_path` L235). Sidecar = `output_dir / "wrapper-result.yaml"` (L224). Records `env_alias_count` (L218) and `write_status` (L219) plus fix bookkeeping (L221-222).

**`max_turns` default value:** The runtime default is `_DEFAULT_MAX_TURNS = 250` in **`config.py:39`** (resolved into the config at `config.py:230` via `max_turns or _DEFAULT_MAX_TURNS`). `runner.py` itself holds no default — it passes `config.max_turns` straight to `ClaudeProcess` at `runner.py:411` (and again in `_apply_remediation` at L446).

---

## 3. `config.py` — resolve_config + depth floor + field flow

**`resolve_config` signature + range — `config.py:123-240`** (`def resolve_config(...)` L123; `return ReflectConfig(...)` L220-240). Keyword-only params after `tasklist_path`: `depth`, `spec_path`, `output_dir`, `model`, `timeout`, `max_turns`, `promote`, `allow_single_vendor`, `tmux`, `dry_run`, `print_command`, `resume`, `base_branch=_DEFAULT_BASE_BRANCH`, `base_override=None`, `fix=False`, `max_fix_iterations=2` (L124-141).

**`--depth` resolution / floor — `config.py:190`** (single line):
```python
    resolved_depth = "standard" if depth == "quick" else depth
```
(O4/FR-3: POST never runs quick; `quick` is floored to `standard`. The Click layer only offers `standard|deep` — see §5 — so the floor is belt-and-suspenders.) The floored value flows into the constructor at `config.py:225` (`depth=resolved_depth`).

**Field-flow pattern (how a resolved field reaches the constructor):** each CLI/derived input is normalized into a local `resolved_*` variable (e.g. `resolved_tasklist` L165, `resolved_model` L170, `resolved_depth` L190, `resolved_spec` L193-198, `resolved_executor_model` L205, `resolved_output` L208-218), then passed by keyword into the single `ReflectConfig(...)` call at **L220-240**. Defaulted scalars use the `value or _DEFAULT` idiom (`timeout or _DEFAULT_TIMEOUT_SECONDS` L229; `max_turns or _DEFAULT_MAX_TURNS` L230).

**Where new `--transport` / `--reviewers` resolution would attach:** add two keyword params to the `resolve_config` signature (after `max_fix_iterations`, L141), resolve them into `resolved_transport` / `resolved_reviewers` locals (alongside L190-218), and pass them into the `ReflectConfig(...)` constructor at L220-240 **after** the current tail field `max_fix_iterations=` (L239) — matching the dataclass append-at-tail rule (see §4). The Click option plumbing is in `commands.py` (see §5).

---

## 4. `models.py` — ReflectConfig / ReflectResult / Verdict

**`ReflectConfig` dataclass — `models.py:57-91`. Fields IN ORDER:**
1. `tasklist_path: Path` (L66)
2. `base: str` (L67)
3. `head: str` (L68)
4. `spec_path: Path | None` (L69)
5. `depth: str` (L70)
6. `executor_model: str | None` (L71)
7. `output_dir: Path` (L72)
8. `model: str` (L73)
9. `timeout_seconds: int` (L74)
10. `max_turns: int` (L75)
11. `promote: bool` (L76)
12. `allow_single_vendor: bool` (L77)
13. `tmux: bool` (L78)
14. `dry_run: bool` (L79)
15. `print_command: bool` (L80)
16. `resume: bool` (L81)
17. `base_override: str | None` (L84)
18. `fix: bool` (L85)
19. `max_fix_iterations: int` (L86) ← **CURRENT TAIL**

All fields are non-default (no `= ...`), so **new FR-RH2 fields (`transport`, `reviewers`, etc.) MUST append AFTER `max_fix_iterations` at L86** to keep dataclass field ordering valid. The comment at L82-83 documents this exact append-at-tail convention.

**`contract_path` property — `models.py:88-91`:** `return self.output_dir / "return-contract.yaml"`.

**`ReflectResult` dataclass — `models.py:94-121`. Fields:** `verdict: Verdict` (L103), `status: str | None` (L104), `tier_reached: int | None` (L105), `reason: str` (L106), `report_path: str | None` (L107), `contract_path: str | None` (L108), `deviations: dict[str,int] = field(default_factory=dict)` (L109), `child_exit_code: int | None = None` (L110), `write_status: str = ""` (L111), then defaulted tail: `fix_iterations: int = 0` (L114), `fix_converged: bool = False` (L115), `remediation_task_path: str | None = None` (L116). `outcome` property L118-121 (`"success"` only on `Verdict.PASS`).

**`Verdict` enum — `models.py:26-54`.** Values + exit codes (from `exit_code` property L38-49):
| Enum | str value | exit code |
|---|---|---|
| `Verdict.PASS` | `"pass"` | **0** (only exit-0 path) |
| `Verdict.HALTED` | `"halted"` | **10** |
| `Verdict.DEGRADED` | `"degraded"` | **11** |
| `Verdict.BLOCKED` | `"blocked"` | **2** |
`is_promotable` property (L51-54) → True only for `Verdict.PASS`.

---

## 5. `commands.py` — Click `reflect run` surface

**`_DEFAULT_MODEL` value — `commands.py:31`:** `_DEFAULT_MODEL = "claude-opus-4-8"`. The orchestrator model is sourced at runtime as `os.environ.get("ANTHROPIC_MODEL", "").strip() or _DEFAULT_MODEL` (**commands.py:172**).

**Group docstring "so Tier 2 fans out" — `commands.py:53`** (inside `reflect_group` docstring L49-61): *"Launches `/sc:reflect --mode post` as a top-level `claude --print` subprocess (so Tier 2 fans out), ..."*. (Runner module docstring `runner.py:1-7` carries a near-identical "escaping the Agent-tool nesting limit so Tier 2 fans out" phrasing.)

**Existing `@click.option` list on `run` — `commands.py:76-147`** (decorators above `def run(...)` L148-162):
- `--tmux` (L81-83, is_flag)
- `--print-command` (L84-88, is_flag)
- `--promote/--no-promote` default=True (L89-94)
- `--timeout` int default=None (L95-100)
- **`--depth` — `commands.py:101-106`** — `type=click.Choice(["standard", "deep"], case_sensitive=False)`, `default="standard"`. **CONFIRMED: Choice values are `standard|deep` only (NO `quick` at the Click layer).**
- `--output` (L107-111)
- `--allow-single-vendor` (L112-116, is_flag)
- `--dry-run` (L117-121, is_flag)
- `--resume` (L122-126, is_flag)
- `--fix/--no-fix` default=False (L127-132)
- `--max-fix-iterations` int default=2 (L133-138)
- `--base` → `base_override` default=None (L139-147)

**CONFIRMED: NO `--transport` and NO `--reviewers` options exist yet.** Verified by reading the full decorator stack L76-147 and the `def run(...)` parameter list L148-162. FR-RH2 must add both: a `@click.option` decorator (alongside L76-147), a new parameter in `def run(...)` (L148-162), and threading them into the `resolve_config(...)` call (L175-190).

**`resolve_config(...)` call site in `run()` — `commands.py:175-190`** (kwargs passed today: `depth, output_dir, model, timeout, promote, allow_single_vendor, tmux, dry_run, print_command, resume, fix, max_fix_iterations, base_override`). New transport/reviewers kwargs would be added here.

---

## Status: Complete

### TDD line-anchor DRIFT findings

The escalation brief listed the anchors the driving TDD claims. Verified against shipped source (zero-trust). Results:

- **`expected_tier` line:** TDD-style anchor verified present and EXACT at `runner.py:403`: `expected_tier = 2 if config.depth in {"standard", "deep"} else 1`. No drift.
- **`_audit_once` seam:** verified at `runner.py:392-428`; the single-`ClaudeProcess` launch (the FR-RH2 branch point) is `runner.py:405-419`. No drift.
- **Isolation guardrail comment:** verified at `runner.py:8-12` (NFR-7 "never an Agent/Task surface"). No drift.
- **`write_reflect_post` FR-6 PASS→BLOCKED rule:** the function is `runner.py:117-185`; the PASS→BLOCKED demotion lives in `run()` at `runner.py:588-590`, NOT inside `write_reflect_post` itself. **NUANCE (not drift):** anyone citing "write_reflect_post enforces PASS→BLOCKED" should know the demotion is in the `run()` caller (L588-590); `write_reflect_post` only RETURNS the non-`"written"` status string (`"frontmatter-stale"` L182 / `"frontmatter-missing"` L148).
- **`--depth` Choice values:** TDD-style claim of `standard|deep` confirmed EXACT at `commands.py:103`. The `quick→standard` floor exists ONLY at `config.py:190` (defensive — Click never emits `quick`).
- **`_DEFAULT_MODEL`:** `"claude-opus-4-8"` at `commands.py:31`. No drift.
- **`max_turns` default:** `_DEFAULT_MAX_TURNS = 250` at `config.py:39` (NOT in runner.py — runner is default-free, passes `config.max_turns` through). Any TDD anchor placing the 250 default in runner.py would be DRIFT.
- **`ensemble.py`:** CONFIRMED net-new (absent). No drift possible.

**No hard line-number drift detected** for the specific anchors I was asked to verify — the shipped source matches the claimed structure. The only cautions are the two "location nuances" above (PASS→BLOCKED lives in `run()` not `write_reflect_post`; the `max_turns`/`quick-floor` defaults live in `config.py` not `runner.py`). Absolute line numbers were not provided in the brief for cross-check, so any concrete `file:line` in the TDD body should be re-validated against the exact lines documented in §1-§5 above.
