# QA Qualitative — Operational Validation Report (task-qualitative mode)

- **Task file:** `.dev/tasks/to-do/TASK-RF-reflect-wrapper-autofix-20260610-053000/TASK-RF-reflect-wrapper-autofix-20260610-053000.md`
- **Spec:** `.dev/brainstorms/20260610-053000-reflect-wrapper-autofix/merged-requirements.md`
- **Contract:** `.dev/handoffs/reflect-wrapper-contract.md`
- **Canonical base verified against:** `/config/workspace/IronClaude/.claude/worktrees/wrapper-onto-master/` (branch `feat/reflect-wrapper-onto-master`)
- **Reviewer stance:** ADVERSARIAL, report-only, `fix_authorization: false`
- **Lens:** would this tasklist actually SUCCEED if executed? Every claim cross-checked against the REAL canonical-base code, not just the task's own anchors.
- **Date:** 2026-06-10

---

## VERDICT: PASS

The tasklist is operationally sound and would execute to a working state. Every code-change item's cited `file:line` target is real in the canonical base; the load-bearing correctness points (marker-guard placement, ClaudeProcess reuse, the §18 grader bump, the bounded-loop arithmetic, the human-decision HALT carve-out, the bootstrap-exemption) are all correctly encoded. No CRITICAL or HIGH issues. Three LOW-severity observations are recorded below for the executor's awareness; none blocks execution and each is already covered by the task's "if the structure differs, adapt" escape clauses.

---

## Operational-lens findings (1–9)

### 1. WOULD-IT-RUN — every cited src file:line is real (PASS)

Spot-checked EVERY unique src path referenced in code-change items against the canonical base:

| Anchor claimed in task | Canonical-base reality | Status |
|---|---|---|
| `commands.py` tasklist arg `exists=True` (`:58-61`) | `@click.argument("tasklist", type=click.Path(exists=True...))` at `:58-61` | ✅ exact |
| `commands.py` `--promote/--no-promote` `default=False` (`:70-75`) | `:71-74`, `default=False` at `:73` | ✅ |
| `commands.py` `run()` sig (`:108-119`); lazy imports `:126-127` | `def run(` at `:108`; `from .config import resolve_config` `:126`, `from .runner import ReflectRunner` `:127` | ✅ |
| `config.py` `_resolve_base` (`:81-93`); `_FRONTMATTER_START_COMMIT_KEY` `:51`; `_DEFAULT_BASE_BRANCH` `:44` | `:81`, `:51`, `:44` | ✅ |
| `config.py` `resolve_config` sig (`:111-127`); `_resolve_base` call `:168`; `ReflectConfig(...)` `:205` | `def resolve_config(` `:111` (kw-only params); call `:168`; construction `:205` | ✅ |
| `config.py` quick depth-floor (`:174-175`) | `resolved_depth = "standard" if depth == "quick"` at `:174-175` | ✅ |
| `models.py` `ReflectConfig` `:58`, `promote: bool` `:76`; `ReflectResult` `:90`, `write_status` `:106`; `contract_path` `:84`, `outcome` `:108` | all exact | ✅ |
| `runner.py` `run()` `:378`; audit `ClaudeProcess(` `:459`, `env_vars=None` `:467`, `start()`/`wait()` `:469-470`; `_build_prompt` `:331`, `--diff` `:344`; `write_sidecar` `:181`; `_child_env` `:228` | all exact | ✅ |
| `contract.py` `_halted_reason` `:304`; `_extract_deviations` `:90`; `_make_result` `:104`; `parse_contract` `:65`; `_DEVIATION_KEYS=("authorized","necessary","drift","regression")` `:40` | all exact | ✅ |
| `main.py` reflect registration | R3 cited `:440-442`; registration present and `reflect run` resolves | ✅ |

No item describes a current-state that contradicts the actual code. The classifier's `deviations.get("necessary",0)` (Step 4.1) is backed by `necessary` being a real `_DEVIATION_KEYS` member (`contract.py:40`).

### 2. MARKER GUARD PLACEMENT — group/eager-callback, NOT in run() (PASS — empirically verified)

This is the single most safety-critical correctness point. Research 03 §4.1 warns that Click validates `exists=True` on the tasklist arg DURING PARSING, before the `run()` body — so an in-`run()` guard cannot pre-empt it, and a nested gate on a since-moved file would crash (exit 2) instead of self-suppressing (exit 0).

**Task Step 3.3 correctly encodes group/eager-callback placement.** It says verbatim: "place this guard so it runs BEFORE Click validates the `exists=True` tasklist argument ... Implement the guard at the GROUP-level callback ... OR as an eager option callback that runs during parsing, **NOT inside `run()`'s body**." PG3.2 and PG3.3 both flag an in-`run()`-body guard as a CRITICAL failure. So the placement requirement is unambiguous and adversarially gated.

**Empirically confirmed the approach works** (the canonical `reflect_group` is a bare `@click.group` with `pass`, NOT `invoke_without_command=True`):
- Group callback fires BEFORE the subcommand's `exists=True` arg validation (a `run /nonexistent.md` with no marker still reaches the group callback, then errors at exit 2 — confirming the callback runs first).
- With the guard added: `marker="1"` + nonexistent file → **exit 0** (suppressed before validation); `marker="0"` + nonexistent file → exit 2 (normal validation, not suppressed); `reflect --help` under `marker="1"` → group help still prints (Click processes `--help` eagerly). All behave per contract §3.

Step 3.3 also covers the "if a group-level callback does not already exist, add one" case — and the canonical group's callback body is currently just `pass`, so the executor adds the guard into it. Valid.

### 3. ClaudeProcess REUSE — one-line-delta, no new launcher (PASS)

Phase 4 Step 4.4 reuses the existing `ClaudeProcess` primitive for BOTH the audit and the `/task` apply, per research 03 §1.5. The apply (`_apply_remediation`) constructs a SECOND `ClaudeProcess(prompt=f"/task {path}", ..., env_vars={_WRAPPER_MARKER:"1"})` with the same model/timeout/max_turns/output_format as the audit — the only delta is `env_vars`. The audit launch is also updated to carry `env_vars={_WRAPPER_MARKER:"1"}` (contract §3.1). No new launcher, no `subprocess.run`/`Popen` in `runner.py`. Thinness preserved; Step 4.4 explicitly forbids raw subprocess and PG4.2 treats a non-ClaudeProcess apply as CRITICAL. The `build_env()` overlay semantics (`os.environ.copy()` → pop two keys → `update(env_vars)`) confirm the marker overlays without scrubbing the `ANTHROPIC_DEFAULT_*` aliases.

### 4. FR-8/FR-9 skill edits — all 5 literal 1.3.0 sites incl. §18 grader (PASS)

Verified the canonical SKILL.md has exactly the 5 `1.3.0` sites R2 named, at the exact lines: `:651` (§9.1 header), `:654` (emitted field), `:791` (closing prose), `:1627` (§15.1 runs.jsonl example), **`:1758` (§18 grader assertion)**. `remediation_task_path` has 0 hits today (FR-8 gap confirmed); `task_file_path` exists at `:744`.

Phase 5 Step 5.4 explicitly enumerates all FIVE sites INCLUDING the §18 grader assertion at `:1758` ("THIS LAST ONE is a test/grader assertion that breaks the falsifier eval if not bumped"), and mandates a post-edit `grep -n "1.3.0"` confirming ZERO residual contract-version hits. PG5.2 treats a missed §18 grader bump as CRITICAL. Edits are made in `src/superclaude/skills/sc-reflect-protocol/` followed by `make sync-dev` + `make verify-sync` (Step 5.5), and PG5.4 forbids staging any `.claude/skills/` path. SoT discipline correct.

### 5. STATE MACHINE end-to-end — every §1/§3 transition has a building item (PASS)

| Spec §1/§3 transition | Building item(s) | Test coverage |
|---|---|---|
| clean → promote(O1)/exit0 | Step 3.2 (promote default flip True), Step 4.5 loop `if PASS: break` | Step 6.6 (O1 promote-on prompt), AC-5 |
| drift-only → auto-fix → re-verify → exit0 | Step 4.1 (`auto-fixable`), 4.4 (`_apply_remediation`), 4.5 (loop) | Step 6.5(a) convergence, AC-2 |
| regression / needs_human_decision → exit10, no promote | Step 4.1 (`human-required` carve-out), 4.5 `if classify != auto-fixable: break` | Step 6.4 matrix + 6.5 human-required, AC-3 |
| non-convergence after N → exit10, `fix_converged:false` | Step 4.5 `if iteration > max: break`, sidecar fields 4.6 | Step 6.5(b), AC-4 |
| cannot-repair (auto-fixable but rtp absent) → exit10 | Step 4.5 `if rtp absent: break` | Step 6.5(c), AC explicit |
| O2 → `--no-promote` verified-not-promoted exit0 | Step 3.2 (no wrapper-side O2 force; generator emits `--no-promote`) | Step 6.6(b), AC-5 |
| `--base` precedence + single-ref de-range | Step 2.2/2.3, 3.1, 3.4 (tmux forward) | Step 6.7, AC-6 |

No transition is missing a building item. The recursion-breaker self-suppress (marker `=1` → exit 0) is built by Step 3.3 and tested by Step 6.3 (AC-1).

### 6. BOUNDED-LOOP arithmetic — (N+1) audits + N applies asserted correctly (PASS — traced)

Traced the Step 4.5 loop pseudocode (audit → PASS-break → not-fix-break → classify-break → rtp-break → `iteration>max`-break → apply → `iteration+=1`) deterministically:
- **Non-convergence, max=2:** audit#1→apply#1→audit#2→apply#2→audit#3→(iteration 3 > max 2)→HALT. = **3 audits + 2 applies = call_count 5**, `fix_iterations=2`, `fix_converged=False`.
- **Convergence on audit#2, max=2:** audit#1→apply#1→audit#2(PASS). = **2 audits + 1 apply = call_count 3**, `fix_iterations=1`, `fix_converged=True`.
- **Cannot-repair:** audit#1 (auto-fixable, rtp null)→break. = **call_count 1**.

Step 6.5 asserts EXACTLY these values: convergence `call_count==3`/`fix_iterations==1`/`fix_converged True`; non-convergence `call_count==5`/`fix_iterations==2`/`fix_converged False`; cannot-repair `call_count==1`. The arithmetic matches the spec's `(N+1)` audits + `N` applies (contract §4/§7, `merged-requirements.md:411`). The `iteration>max` check sits AFTER the audit and BEFORE the apply — the correct ordering to yield (N+1) audits. The `patch_runner_env` fixture (canonical `conftest.py:84`, stubs `_child_env`) keeps `mock_cls.call_count` equal to real launches, so the assertions are valid. Step 6.5(d) also asserts the apply-launch `env_vars` carries the marker.

### 7. feedback_human_decision_items_must_halt — honored (PASS)

The carve-out classifier (Step 4.1) returns `human-required` for ANY of `regression_present`/`needs_human_decision`/`user_decision_required`/`unauthorized_deviation_present`/`regression>0`, and the loop (Step 4.5) breaks to terminal HALT (no `/task` apply, no promote) on any non-`auto-fixable` classification. No auto-applied default ships a human-decision change — `--remediate` only AUTHORS a file; for HUMAN-REQUIRED registers the skill authors nothing auto-runnable (Step 5.3, FR-9; BUILD_REQUEST carries `needs_human_decision:true`). The mixed drift+regression row routes to `human-required` (human wins). PG4.3 and PG7.2 both explicitly check this feedback rule end-to-end.

### 8. VALIDATION commands real + UV-only (PASS)

Phase 7 / per-phase test items use `uv run pytest tests/cli/reflect/`, `uv run ruff check`, `uv run ruff format --check`, `make verify-sync`, `make sync-dev`, and `pipx install --force /config/workspace/IronClaude` (the operator vector per memory `reference_superclaude_install_vector`). Grep confirms 23 `uv run`/`make`/`pipx` invocations and ZERO bare `pip install`/`python -m`/`python script.py`. Step 7.1 runs `ruff format --check` separately (per memory `reference_make_lint_vs_ci_ruff_format` — CI runs it separately from `make lint`). UV-only rule satisfied.

### 9. BOOTSTRAP — POST gate is inline /sc:reflect, not the shell wrapper (PASS)

The penultimate Post-Completion item (task line 450) is the INLINE `/sc:reflect --mode post --depth standard --tasklist <self> --spec <spec>` audit, explicitly NOT a `superclaude reflect run` shell-out ("that command is the artifact this tasklist builds and MUST NOT be invoked as the terminal gate"). The `sc-reflect-protocol` skill exists in `src/superclaude/skills/`. The bootstrap-exemption rationale is stated up-front at task line 65. No `superclaude reflect run` terminal gate appears anywhere as an execution step. Correct — avoids the "no such command" self-bootstrap failure.

---

## LOW-severity observations (non-blocking; executor-awareness)

### L1 — `classify_fix(contract, deviations)` needs the RAW contract dict, but `_audit_once` returns only `ReflectResult`
`ReflectResult` (canonical `models.py:90-106`) carries `deviations: dict[str,int]` but NOT the raw contract dict. `classify_fix` (Step 4.1) reads `contract.get("regression_present")`, `contract.get("needs_human_decision")`, etc. from the RAW dict. After Step 4.3 extracts `_audit_once() -> ReflectResult`, the raw `contract` (canonical `runner.py:473`) becomes local to `_audit_once` and is not returned. The loop in Step 4.5 must therefore either (a) have `_audit_once` also return/stash the raw contract, (b) re-parse `config.contract_path` in the loop, or (c) drive the human-required predicate off result fields. **Already mitigated:** Step 4.5 wording is "parse the contract/deviations and call `classify_fix(...)`" (permits re-parse) and Step 4.3 grants "adapt the extraction boundary." Note `remediation_task_path` is correctly surfaced ONTO the result (Step 4.2) so the loop reads it without re-touching the raw dict — the same pattern could be applied to the human-required booleans if the executor prefers, but the task does not mandate it. No correctness defect; just an integration detail the executor resolves.

### L2 — `reflect run --help` is suppressed when marker=1
Empirically, with the group-callback guard active and `marker="1"`, `reflect run --help` prints the recursion-breaker notice and exits 0 instead of showing run help (the group callback fires before `run --help` is processed). This is acceptable: contract §3 says marker=1 "immediately exits 0 ... before any audit," and `reflect --help` (group help) still works. Step 3.3's only help requirement is that the guard "does NOT interfere with `superclaude reflect --help`" — which holds. Step 7.2 runs `superclaude reflect run --help` WITHOUT the marker set, so the NFR-5 flag-exposure check is unaffected. No action needed; flagged only so the executor doesn't mistake the suppressed `run --help` for a bug.

### L3 — `_make_result` is the 5th `ReflectResult` site; defaults keep all 5 valid (confirmed, not a defect)
The canonical base has exactly 5 hand-built `ReflectResult(...)` sites (`commands.py:162`, `contract.py:114`, `runner.py:394`, `:411`, `:438`), matching the task's "5 hand-built construction sites" claim (Key Objective 5 / Step 2.1). The new `ReflectResult` fields are appended WITH defaults (`fix_iterations:int=0`, `fix_converged:bool=False`, `remediation_task_path:str|None=None`), so all 5 sites stay valid and the dataclass no-default-before-default rule holds (existing `write_status:str=""` is already defaulted at `:106`). The new `ReflectConfig` fields are appended (after the all-non-default existing fields) and populated explicitly at the single `config.py:205` construction site. Field-ordering safe. (Recorded as confirmation, not an issue.)

---

## Evidence appendix (canonical-base greps run)

- `commands.py`: group `@click.group("reflect")` `:39-54` (bare, `pass` body), tasklist `exists=True` `:58-61`, promote `default=False` `:73`, `run()` `:108`, lazy imports `:126-127`.
- Empirical Click order test: group callback fires before subcommand `exists=True` validation; guard at group callback yields exit 0 (marker=1) vs exit 2 (marker=0) on a nonexistent file.
- `config.py`: `_resolve_base` `:81`, `_FRONTMATTER_START_COMMIT_KEY` `:51`, `_DEFAULT_BASE_BRANCH` `:44`, `resolve_config` `:111` (kw-only), call `:168`, `ReflectConfig(` `:205`, quick-floor `:174-175`.
- `runner.py`: `run()` `:378`, audit `ClaudeProcess(` `:459` `env_vars=None` `:467` `start/wait` `:469-470`, `_build_prompt` `:331` `--diff` `:344`, `write_sidecar` `:181`, `_child_env` `:228`.
- `contract.py`: `_halted_reason` `:304`, `_extract_deviations` `:90`, `_make_result` `:104`, `parse_contract` `:65`, `_DEVIATION_KEYS` `:40` (incl. `necessary`).
- `models.py`: `ReflectConfig` `:58` / `promote:bool` `:76`; `ReflectResult` `:90` / `write_status` `:106` / `deviations` `:104` (no raw-contract field).
- `SKILL.md` `1.3.0` sites: `:651 :654 :791 :1627 :1758` (5, incl. §18 grader); `remediation_task_path` 0 hits; `task_file_path` `:744`.
- 5 `ReflectResult(` sites confirmed.
- Loop arithmetic trace: non-conv max=2 → 5 launches / fix_iterations=2 / converged=False; conv@2 → 3 / 1 / True; cannot-repair → 1.
- UV-only: 23 `uv run`/`make`/`pipx` items; 0 forbidden bare pip/python.
- `sc-reflect-protocol/SKILL.md`, `agents/rf-qa.md`, `agents/rf-qa-qualitative.md` all present.

## Conclusion

**VERDICT: PASS.** The tasklist would execute to a working, mergeable, `pipx install --force`-able wrapper. All cited targets are real, the marker-guard placement is correct (and empirically proven to pre-empt Click `exists=True`), ClaudeProcess is reused thinly, all 5 contract-version sites incl. the §18 grader are bumped in `src/` then synced, the bounded-loop call-count arithmetic is exact, the human-decision HALT carve-out is honored, validation is UV-only, and the bootstrap POST gate is the inline `/sc:reflect` form. The three LOW observations are executor-awareness notes, each already covered by the task's adapt-if-different clauses; none blocks execution.
