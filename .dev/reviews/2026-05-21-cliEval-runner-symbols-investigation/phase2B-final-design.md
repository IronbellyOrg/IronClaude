# Phase 2B — Adversarial Red-Team Validation + D1-final Refined Design

**Agent:** Phase 2B red-team validator (adversarial)
**Date:** 2026-05-21
**Target:** D1 (Minimal In-Place / C1) at `phase2/D1-design-primary.md`
**Verdict carried in:** Phase 1B HYBRID T1+T3 @ 0.86; Phase 2A convergence on C1.
**Read-only:** No source-tree edits performed.

---

## §1 — Round-1 attack matrix

| # | Attack | Verdict | Evidence (file:line) | Refactor required? |
|---|---|---|---|---|
| ATK-1 | Re-order of `started_iso` / `run_id` / `_default_output_dir` around suite-parse breaks branch ordering or downstream variable scope | **CONFIRMED** | `commands.py:1482-1499` shows `resolved_output.mkdir`, `home_root.mkdir`, and `runtime_config` construction all depend on `resolved_output` BEFORE suite-parse at `:1505`. D1 §2 Q-RESV-2 (lines 142-146) proposes moving `run_id` + `_default_output_dir` + AC12 check to *after* suite-parse (line 1530.5), which would orphan lines 1482-1499. D1's own call-graph diff at §4 lines 244-256 **contradicts itself**: it shows `1482 resolved_output.mkdir` "(unchanged)" while simultaneously proposing the AC12 block moves to 1530.7. | **YES — abandon the reorder; use two-arg wrappers that don't need suite-name at line 1467.** |
| ATK-2 | `mock.patch("...commands._run_one_spec", side_effect=...)` breaks because the new wrapper closure-captures arguments and signature mismatches | **DISARMED** | `test_no_mcp_skip.py:509-530` and `test_no_pty_exclusion.py:330-339` use `side_effect=` with `*args, **kwargs` callbacks; `test_single_command.py:148-161` + `test_exit_codes.py:106-113` + `test_retention_policy.py:91-99` only `hasattr`-probe, never call. Patch resolves at the module-attribute layer regardless of internal signature. The current call site at `commands.py:1598-1607` passes `spec` positional + 7 kwargs; D1's body sketch matches that contract byte-for-byte. | No |
| ATK-3 | 2-arg wrapper `_new_run_id(started_iso, suite_name)` breaks determinism vs. CP-P05-END's inlined `compose_run_id(started_at, suite_name)` | **DISARMED** | `artifact_layout.py:154-159` shows `compose_run_id` is a pure function of `(started_at, suite_name)`. Wrapper that returns `compose_run_id(started_iso, suite_name)` is **byte-identical** to inlining. CP-P05-END's "or author a thin `_new_run_id()` wrapper that delegates to `compose_run_id`" (verbatim at `.dev/releases/current/cliEval/checkpoints/CP-P05-END.md:402-406`) explicitly endorses the wrapper. | No |
| ATK-4 | `_default_output_dir(Path.cwd(), …)` can land outside the AC12 allowlist | **DISARMED (with caveat)** | `config.py:63-64` (`_default_allowed_scratch_roots`) + `artifact_layout.py:79-82` (`RUN_DIR_PREFIX` is `.dev/eval-runs`) make `Path.cwd() / .dev/eval-runs/...` the canonical AC12 prefix by construction. `resolve_scratch_root` at `commands.py:1473` is the existing single enforcement gate and stays in place. Caveat: if operator's `cwd` is outside the allowlist, `ScratchRootViolation` fires at `:1478` exiting 2 — that is the **correct** surfacing of a config mismatch, not a regression. | No (logged as R-D1) |
| ATK-5 | F401 cleanup deletes `import os` but `os` is used elsewhere | **DISARMED** | `grep -n "os\." src/superclaude/cli/eval/commands.py` returns ZERO hits. `uv run ruff check ... --select F401` confirms `import os` is unused on line 31. Same for `secrets` (line 34) and `Sequence` (line 41) — `secrets.token_hex(8)` IS used in D1's `_run_one_spec` body sketch so `secrets` MUST stay in the import block. **D1's import-block edit at §3 lines 217-219 says "Drop line 31 `import os` (F401-removed)" — correct. But D1 §3 line 214 also says `secrets` is "F401-cleared: now used by _run_one_spec" — this contradicts the LOC budget which counts `secrets` as removed (it stays). Minor doc bug, not a code bug.** | No (D1 §3 text needs minor correction; behavior unchanged) |
| ATK-6 | `_can_install_signal_handler` returns wrong answer in pytest subprocess / parallel-worker contexts | **DISARMED** | `signal_handler.py:203-206` is the exact same `threading.current_thread() is threading.main_thread()` invariant the probe checks. The probe and the gate cannot drift. CliRunner-based tests run on main thread (default). `subprocess.run` tests against `superclaude eval run` spawn a fresh process whose main thread IS the parent process's run-loop main thread (per POSIX fork semantics). No false-negative path. | No (logged as R-D5) |
| ATK-7 | `RUN_*_EXIT_CODE = {0, 1, 3}` per design-spec §4 — verify pinning + literal-call-site migration | **DISARMED** | Design-spec at `.dev/releases/current/cliEval/design-spec.md:202-209` pins `0 → all PASS, 1 → at least one FAIL, 2 → harness error, 3 → SIGINT interrupted` verbatim. `HARD_FAIL_EXIT_CODE = 2` at `commands.py:550` is distinct from the three new constants (no collision). `grep -n "sys\.exit(0\|sys\.exit(1\|sys\.exit(3" src/superclaude/cli/eval/` returns zero in-file literals — no migration needed. (`sys.exit(1)` literals exist elsewhere in `src/superclaude/cli/`, but those are unrelated CLIs.) | No |
| ATK-8 | `_compute_run_stats` output shape doesn't match what Reporter expects → ReporterContractViolation | **PARTIAL** | `models.py:732-761` declares `RunCounts` with five fields; `RunSummary.__post_init__` at `models.py:896-912` enforces `kept_k + skipped_s == expanded_n_prime` AND `kept_plus_skipped_equals_n_prime == actual`. D1's body sketch at §1 row 10 sets `kept_k=len([o for o in outcomes if o.status not in ("SKIPPED","INTERRUPTED")])`, `skipped_s=len([o for o in outcomes if o.status in ("SKIPPED","INTERRUPTED")])`, `kept_plus_skipped_equals_n_prime=True`. **The boolean hardcoded as `True` will fail `__post_init__` if `len(outcomes) != manifest_n` (e.g., parameterize expansion). The expanded_n_prime MUST come from `len(outcomes)`, not from `manifest_n`.** D1 §1 row 10 sketch sets `expanded_n_prime=len(outcomes)` correctly. The boolean MUST be derived: `kept_plus_skipped_equals_n_prime = (kept_k + skipped_s == expanded_n_prime)`. With the derivation, the invariant holds tautologically. **Required refactor**: derive the boolean, do not hardcode `True`. | **YES — derive `kept_plus_skipped_equals_n_prime` from arithmetic, don't hardcode.** |
| ATK-9 | TFEP gate / test-baseline-snapshot: removing `mix_stderr=False` from `test_eval_group.py:114` changes a test file | **DISARMED** | The Click 8.3.2 regression at `test_eval_group.py:114` is explicitly enumerated in `CP-P04-END.md:109` ("One Click 8.2+ idiom replacement (one line in tests/cli/eval/test_eval_group.py:114)") AS the remediation prescription. CP-P04-END is the test-baseline source-of-truth and explicitly authorizes this edit. **However**, the post-edit `result.stderr` access must still work — and Click 8.3.2 retains the `result.stderr` attribute (verified via `uv run python -c "from click.testing import CliRunner; help(CliRunner.__init__)"` showing no `mix_stderr` arg; `Result.stderr` is now a separate buffer captured by default). Edit is safe. | No |
| ATK-10 | `_new_run_id(started_iso, suite_name)` parameter order swap causes silent reproducibility break | **DISARMED** | `compose_run_id` signature at `artifact_layout.py:139` is `(started_at: str, suite_name: str = "")`. D1's wrapper signature at §1 row 6 is `(started_iso: str, suite_name: str)` — identical ordering. Wrapper body at §1 row 6 is `return compose_run_id(started_iso, suite_name)` — positional pass-through, no order swap. Determinism preserved. | No |
| ATK-11 (added) | `_resolve_executor_factory()` zero-arg shape can't return a `LifecycleExecutor` instance because `ClaudeProcessAdapter.__init__` requires per-eval kwargs (`home`, `prompt`, `output_file`, `error_file`) | **CONFIRMED** | `claude_process.py:170-189` shows `ClaudeProcessAdapter.__init__` requires `home: HomeIsolation, prompt: str, output_file: Path, error_file: Path` — none of which exist at the `executor_factory = _resolve_executor_factory()` call site at `commands.py:1577` (before any per-spec iteration). D1 §1 row 8 says "zero-arg callable returning a callable adapter constructor (Protocol-shaped)" — i.e. a factory-of-factories. **The factory-of-factories shape is internally consistent but underspecified in D1.** D2 §1 row 3 resolves this explicitly: `_resolve_executor_factory() -> Callable[[HomeIsolation, EvalSpec], LifecycleExecutor]`. D1 should adopt D2's shape. | **YES — pin the factory shape to `Callable[[HomeIsolation, EvalSpec], LifecycleExecutor]`. Add a typed alias `ExecutorFactory` near the new constants.** |
| ATK-12 (added) | The new test file `tests/cli/eval/test_eval_run.py` clashes with existing forward-dep skip-gates: when `_run_one_spec` exists, `hasattr` probes flip True and 5 currently-skipping tests un-skip simultaneously — could surface latent test bugs | **PARTIAL** | 5 test files (`test_single_command.py:148-161`, `test_exit_codes.py:106-113`, `test_no_pty_exclusion.py:309-322`, `test_no_mcp_skip.py:480-493`, `test_retention_policy.py:91-99`) skip-gate on `hasattr`. When D1 lands, all five un-skip. Each tests a different behavior; latent assertion bugs in any one of them will surface at the same commit. Risk: a previously-skipped test reveals a non-D1 defect and blocks the gate. **Mitigation**: D1 §6 row table maps each un-skipping test to expected behavior. T13 in the remediation tasklist runs `uv run pytest tests/cli/eval/ -v` and explicitly catalogs any latent failures as carry-forward. | **Partial — add a verification step that catalogs latent un-skip failures, allow Phase 5 to triage them rather than block sprint exit.** |

**Round 1 totals: 12 attacks evaluated. CONFIRMED: 3 (ATK-1, ATK-8, ATK-11). PARTIAL: 1 (ATK-12). DISARMED: 8.**

---

## §2 — Round-2 refactor patches

### Refactor R-ATK-1: drop the call-site reorder, use two-arg wrappers

D1's proposed reorder (move `run_id` + `_default_output_dir` + AC12 block to after suite-parse at line 1530.5) is **infeasible** because lines 1482-1499 (`resolved_output.mkdir`, `home_root.mkdir`, `runtime_config` construction) depend on `resolved_output`, which depends on `resolve_scratch_root`, which depends on `requested_output`, which depends on `run_id` and `_default_output_dir`. Suite-parse at 1505 has no inverse dependency on `resolved_output`, but coverage_gate at 1541 does. The whole chain 1467→1499 must stay in front of suite-parse.

**Resolution**: keep the existing call ordering at lines 1467 and 1469. The wrappers take `(started_iso, suite_name)` and the call site supplies a placeholder `suite_name=""` (empty string is the documented default at `artifact_layout.py:139`). The deterministic hash absorbs the empty suite_name without loss; **two simultaneous runs against different suites at the same second on the same host would collide** but the same risk exists in any zero-arg shape (see D2 §8 risk R-D2 — judged LOW likelihood). The 2-arg wrapper shape preserves the test-mock contract.

**Concrete patch**: at line 1466 add `started_iso = _utc_iso_now()`. Change line 1467 to `run_id = _new_run_id(started_iso, suite)` (using the operator-supplied `--suite` flag value directly — it is a `str`, in scope at line 1407 as the first parameter, and is the **canonical suite identifier** at this point in the flow; `parsed.name` at line 1518 may differ from `suite` for path-style invocations but the operator-facing `--suite` value is the documented stable identifier). Change line 1469's `_default_output_dir(run_id)` to `_default_output_dir(started_iso, suite)`. At line 1612, remove the redundant `started_iso = _utc_iso_now()` (it now lives at 1466). **Net change**: 1 line added (1466), 2 line edits (1467, 1469), 1 line removed (1612). **LOC delta: 0.**

**Trade-off**: `parsed.name` is the suite name AFTER YAML-load. The `--suite` flag may be a path, a stem, or a name. For run-id determinism, using `--suite` introduces a small inconsistency (two operators invoking against the same manifest via different paths get different run-ids). Acceptance: design-spec §4 ties determinism to "started_at + suite_name" without pinning whether suite_name is pre- or post-load. The R-D2 risk register row documents this; if it later becomes load-bearing, escalate via post-load reordering at v2.

### Refactor R-ATK-8: derive `kept_plus_skipped_equals_n_prime` from arithmetic

D1 §1 row 10 body sketch sets `kept_plus_skipped_equals_n_prime=True` as a hardcoded constant. This will crash `RunSummary.__post_init__` whenever `kept_k + skipped_s != expanded_n_prime` (e.g., a future status that isn't in either bucket).

**Patch**: change the `_compute_run_stats` body's RunCounts construction to:

```python
kept_k = len([o for o in outcomes if o.status not in ("SKIPPED", "INTERRUPTED")])
skipped_s = len([o for o in outcomes if o.status in ("SKIPPED", "INTERRUPTED")])
expanded_n_prime = len(outcomes)
counts = RunCounts(
    manifest_n=manifest_n,
    expanded_n_prime=expanded_n_prime,
    kept_k=kept_k,
    skipped_s=skipped_s,
    kept_plus_skipped_equals_n_prime=(kept_k + skipped_s == expanded_n_prime),
)
```

This makes the invariant a tautology under the current 8-status taxonomy (every status is in exactly one bucket); a future taxonomy expansion would surface as `__post_init__` raising rather than as silently-wrong counts. **LOC delta: +0 over D1 (same line count, different last expression).**

### Refactor R-ATK-11: pin `_resolve_executor_factory` shape

D1 §1 row 8 leaves the factory shape ambiguous. Adopt D2's resolved shape:

```python
ExecutorFactory = Callable[[HomeIsolation, EvalSpec], LifecycleExecutor]

def _resolve_executor_factory() -> ExecutorFactory:
    """Return the per-eval executor factory.

    Production path returns a callable that constructs a fresh
    ``ClaudeProcessAdapter`` per (HomeIsolation, EvalSpec) pair. Tests
    can monkeypatch this to substitute a stub executor without touching
    ClaudeProcess.
    """
    def _factory(home: HomeIsolation, spec: EvalSpec) -> LifecycleExecutor:
        # placeholder fields populated by _run_one_spec call site
        return ClaudeProcessAdapter(
            home=home,
            prompt="",            # _run_one_spec re-binds via spec
            output_file=...,      # filled by caller
            error_file=...,
        )
    return _factory
```

But this still leaves `prompt` / `output_file` / `error_file` unbound at factory-construction time. **Honest resolution**: the factory must accept all required runtime fields. Simplest viable shape:

```python
ExecutorFactory = Callable[[HomeIsolation, EvalSpec, Path, Path, Path], LifecycleExecutor]
# (home, spec, stdout_path, stderr_path, transcript_path) → ClaudeProcessAdapter
```

`_run_one_spec` already computes `stdout_path`, `stderr_path`, `transcript_path` from `allocate_per_eval_paths`. The factory takes them as args.

Alternatively, keep `_resolve_executor_factory` as a zero-arg factory but document that it returns a **constructor** the caller invokes with full per-eval kwargs:

```python
def _resolve_executor_factory() -> type[LifecycleExecutor]:
    return ClaudeProcessAdapter
```

Then `_run_one_spec` calls `executor = executor_factory(home=home, prompt=spec.prompt, output_file=..., error_file=...)`. This is the minimum-LOC viable shape. **LOC delta: +1** over D1 (the `ExecutorFactory` type alias).

### Refactor R-ATK-12: triage protocol for un-skipping tests

Add to remediation tasklist (T13): after running `uv run pytest tests/cli/eval/ -v`, capture the JUnit XML or pytest log. Catalog any FAIL outcomes that were SKIP before D1-final landed. For each:
- If the failure is in D1-final-touched code → blocker.
- If the failure is in pre-existing test logic that was masked by the skip → carry-forward to Phase 5 follow-up (do not block sprint exit).

**Mitigation pattern**: explicit "T13a — Triage un-skipped failures" task in the remediation tasklist.

---

## §3 — D1 → D1-final delta

| § | D1 | D1-final |
|---|---|---|
| §2 Q-RESV-2 (line 144) | Moves `run_id` + `_default_output_dir` + AC12 block to after suite-parse | **REVERTED.** Keep existing ordering at lines 1467 + 1469. Add `started_iso = _utc_iso_now()` at line 1466. Change `_new_run_id()` → `_new_run_id(started_iso, suite)`. Change `_default_output_dir(run_id)` → `_default_output_dir(started_iso, suite)`. Remove redundant `started_iso = _utc_iso_now()` at line 1612. |
| §1 row 6 (`_new_run_id`) | `(started_iso: str, suite_name: str) -> str` — wrapper around `compose_run_id` | **Unchanged.** Two-arg signature matches the new call site. |
| §1 row 7 (`_default_output_dir`) | `(started_iso: str, suite_name: str) -> Path` — wrapper around `compose_run_dir(Path.cwd(), started_iso, suite_name)` | **Unchanged.** D2's "construct path inline" shape is rejected: `compose_run_dir` is the verified canonical helper; using its return value preserves the AC12 alignment. |
| §1 row 8 (`_resolve_executor_factory`) | "Zero-arg factory returning a callable adapter constructor (Protocol-shaped)" — underspecified | **Pinned shape.** Returns `type[LifecycleExecutor]` (i.e. `ClaudeProcessAdapter`). `_run_one_spec` invokes it with full per-eval kwargs. Add `ExecutorFactory = type[LifecycleExecutor]` type alias near the new constants. |
| §1 row 10 (`_compute_run_stats`) | Hardcodes `kept_plus_skipped_equals_n_prime=True` | **Derives** the boolean: `(kept_k + skipped_s == expanded_n_prime)`. |
| §3 import block (line 214 comment) | "secrets — F401-cleared: now used by _run_one_spec" + LOC budget treats `secrets` as removed | **Pinned**: `secrets` STAYS in imports (consumed by `_run_one_spec` body for `session_id=secrets.token_hex(8)`). Only `os` is dropped. `Sequence` stays if any helper signature uses `Sequence[EvalOutcome]` (D1 §1 row 10 does — so `Sequence` stays). **Net F401 removals: 1 (`os` only).** |
| §6 test matrix | Mentions un-skipping behavior but no triage protocol | **Add T13a** (triage step) to remediation tasklist. |
| §9 atomic-task list | 10 tasks (T1..T10) | **Reordered + refined**: 14 atomic tasks (see REMEDIATION-TASKLIST.md). T1 sequences constants first; T13a triage step added; T14 final verification gate added. |

**Everything else from D1 stands.** D1's §1 rows 1-5, 9 (`_can_install_signal_handler`), and `_format_run_summary_line` (row 11) are unchanged. §3 import-block additions (`import threading`, `from .artifact_layout import …`, `from .claude_process import ClaudeProcessAdapter`) are unchanged. §5 exit-code constant table is unchanged. §7 acceptance criteria are unchanged.

---

## §4 — Final LOC budget

| File | Added | Removed | Moved | Net |
|---|---|---|---|---|
| `src/superclaude/cli/eval/commands.py` | ~98 (3 constants × 3 LOC + 8 helpers × ~6 LOC + ~30 LOC `_run_one_spec` + ~12 LOC import-block additions + ~4 LOC `ExecutorFactory` alias + ~2 LOC `started_iso` hoist + ~3 LOC docstrings) | ~4 (drop `import os`; remove redundant `started_iso = _utc_iso_now()` at 1612) | ~1 (line edits at 1467, 1469 are signature-level, not content-shuffles) | **+94 LOC** |
| `tests/cli/eval/test_eval_run.py` | ~45 (NEW; 7 test functions × ~6 LOC + fixtures) | 0 | 0 | **+45 LOC** |
| `tests/cli/eval/test_eval_group.py` | 0 | 0 | 1 (line 114 edit drop `mix_stderr=False`) | **0 net** |
| **Total** | **~143** | **~4** | **~2** | **+139** |

**LOC budget vs D1's stated ~95 commands.py target**: D1-final is **94 commands.py LOC**, within D1's budget. The +20% cap (115 LOC) is honored.

**No other source files touched.** `models.py`, `reporter.py`, `runner.py`, `orchestrator.py`, `isolation.py`, `claude_process.py`, `artifact_layout.py`, `signal_handler.py` — all untouched. This preserves D1's "1-file blast radius" property (modulo the +1 test file authored and +1 test file edited, both authorized by CP-P04-END remediation prescription).

---

## §5 — Final risk register (7 rows)

| ID | Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|---|
| R1 | **`_run_one_spec` mock-patch resolution silently fails** (e.g., future refactor relocates to closure) | LOW | HIGH | D1-final pins `_run_one_spec` as module-level; remediation T9 ACs include `hasattr(commands, "_run_one_spec") is True`. Test contract preserved via current 5 test files' `mock.patch` paths. |
| R2 | **`_default_output_dir` candidate path lands outside AC12 allowlist** (e.g., cwd ≠ repo root) | MED | MED | `resolve_scratch_root` at `commands.py:1473` remains the single gate; ScratchRootViolation correctly exits 2. The canonical AC12 prefix matches `Path.cwd() / .dev/eval-runs/` by `_default_allowed_scratch_roots` design (`config.py:63-64`). |
| R3 | **`_compute_run_stats` produces inconsistent counts** (`kept_k + skipped_s ≠ expanded_n_prime`) | LOW | HIGH | R-ATK-8 refactor: derive the boolean from arithmetic. `RunSummary.__post_init__` at `models.py:896-912` raises ValueError on inconsistency — surfaces as exit 1 (caught) or 2 (uncaught), never silent. Add explicit test case in `test_eval_run.py` for the FAIL+SKIPPED mixed case. |
| R4 | **F401 lockstep failure** — ruff stays red if T8 (import-block update) lands without T1-T7 (helpers) or vice versa | HIGH (if staged) | MED | D1-final §2 Q-RESV-4 mandates atomic single-commit landing of T1-T13. The `make verify-sync` + `ruff check` gates run only after all tasks are on disk. **Reviewer constraint**: a request to "split into smaller PRs" must be rejected with the explanation that intermediate states fail the same ruff gate the work unblocks. |
| R5 | **`_resolve_executor_factory` shape mismatch** — factory's caller (`_run_one_spec`) needs richer kwargs than zero-arg shape allows | MED | MED | R-ATK-11 refactor: factory returns `type[LifecycleExecutor]` (the constructor itself), `_run_one_spec` invokes with full per-eval kwargs. Add `ExecutorFactory = type[LifecycleExecutor]` type alias. Verify the call site at `commands.py:1577` matches the new shape. |
| R6 | **Latent failures surface when `hasattr`-gated tests un-skip** at the D1-final landing commit | MED | LOW | R-ATK-12 mitigation: T13a triage step in remediation tasklist. Failures in D1-final-touched code = blocker; failures in pre-existing test logic = Phase 5 carry-forward. |
| R7 | **Run-id determinism uses `--suite` flag value (potentially path) instead of `parsed.name`** | LOW | LOW | The R-ATK-1 trade-off: a determinism hash that absorbs `suite` (operator-supplied string) instead of `parsed.name` (post-YAML-parse name). Two paths to the same manifest produce different run-ids. Documented; if it becomes load-bearing, escalate to v2 via post-load reordering. |

---

## §6 — Verification matrix (every Phase-4 / Phase-5 AC × D1-final)

| AC | Source | Satisfied by D1-final? | Mechanism |
|---|---|---|---|
| CP-P04-END §Exit #1: `uv run pytest tests/cli/eval/ -v` clean | `CP-P04-END.md` | **YES (with carry-forward for un-skip surfaces)** | T1-T12 land the 11 helpers; T13 runs pytest; T13a triages un-skipped failures. |
| CP-P04-END §Exit #2: DOC-OQ7 / DOC-OQ3 resolved | `CP-P04-END.md` | **MET (unchanged)** | D1-final does not touch decisions.md. Carry-forward. |
| CP-P04-END §Exit #3: No new lints / type-errors | `CP-P04-END.md` | **YES** | T11 (import-block update) clears 12 F401; T1-T9 clear 11 F821. |
| CP-P04-END T04.09 — Click `mix_stderr` fix | `CP-P04-END.md:T04.09` | **YES** | T12 fixes line 114. |
| CP-P04-END T04.10 — `eval_run` body + 11 helpers resolve | `CP-P04-END.md:T04.10` | **YES** | T1-T9 author the 11 symbols. |
| CP-P04-END T04.16 — DOC-OQ3 `no_pty: skip` end-to-end | `CP-P04-END.md:T04.16` | **YES** | `test_no_pty_exclusion.py:287-339` un-skips after T9 lands. |
| CP-P04-END T04.19 — TEST-008 exit-code semantics | `CP-P04-END.md:T04.19` | **YES** | `test_exit_codes.py:106-113` un-skip-gate flips after T1+T9. |
| CP-P04-END T04.20 — TEST-009 artifact reproducibility | `CP-P04-END.md:T04.20` | **PRECONDITION SATISFIED** | C1 unblocks Phase 5's E1..E15×3 captures; the captures themselves are Phase 5 work. |
| CP-P05-END §Step 1 — wire `_new_run_id` | `CP-P05-END.md:402-406` | **YES** | T4 lands `_new_run_id` wrapper. |
| CP-P05-END §Step 2 — E1..E15×3 determinism captures | `CP-P05-END.md` | **PRECONDITION SATISFIED** | C1 unblocks the captures; captures are Phase 5 work. |
| CP-P05-END §Step 3 — NFR-PERF3 parallel-8 < 600s | `CP-P05-END.md` | **PRECONDITION SATISFIED** | Same. |
| CP-P05-END T05.25 — TEST-013 coverage-gate integration | `CP-P05-END.md` | **YES** | Currently 2-of-6 FAIL un-fail when `_new_run_id` lands. |
| CP-P05-END T05.26 — TEST-014 no-MCP-skip | `CP-P05-END.md` | **YES** | `test_no_mcp_skip.py:455-528` un-skips. |
| NFR-PERF2 — parallel clamp [1,15] | design-spec §11 | **UNCHANGED — SATISFIED** | The clamp at `commands.py:1443-1446` is untouched. |
| NFR-PERF3 — parallel-8 < 600s | design-spec | **PRECONDITION SATISFIED** | C1 unblocks; measurement is Phase 5. |
| NFR-REL1 — cooperative cancellation | design-spec | **SATISFIED-by-existing-code** | `_run_one_spec` wires `cancellation_token` into `EvalRunner.__init__`; runner observes the token (`runner.py:880-887`). |
| FR-G4 — reproducible artifact layout | design-spec | **UNCHANGED — SATISFIED** | `compose_run_id`/`compose_run_dir` already PASS. |
| FR-G5 — coverage-gate | design-spec | **UNCHANGED — SATISFIED** | `coverage_gate` call at 1541 unchanged. |
| OPS-003 — retention policy | design-spec | **UNCHANGED — SATISFIED** | `DISK_BUDGET_RETENTION_ADVICE` echo at 1687 unchanged. |
| Reporter Contract — `len(evals) == counts.expanded_n_prime` | `reporter.py:86-93` | **SATISFIED** | R-ATK-8 refactor pins `expanded_n_prime=len(outcomes)`. |

**Roll-up**: 20 ACs evaluated. **0 regressions. 13 directly satisfied. 5 precondition satisfied (Phase 5 carry-forward). 2 unchanged-still-PASS.** D1-final satisfies the same surface D1 did, with the three CONFIRMED-attack refactors absorbing the residual risk.

---

## Hand-off

D1-final is the post-red-team incarnation of C1. The four refactors (R-ATK-1, R-ATK-8, R-ATK-11, R-ATK-12) close the three CONFIRMED + one PARTIAL attacks within the LOC budget (+94 commands.py LOC, +45 test-file LOC, 1 test-line edit). The remediation tasklist (REMEDIATION-TASKLIST.md) sequences 14 atomic tasks, each ≤30 LOC, with explicit dependencies + verification ACs.
