# Research Notes: Fix reflect-wrapper marker leakage into the §6.1 step 5.5 verification subprocess

**Date:** 2026-06-11
**Scenario:** A (explicit bug, well-diagnosed) — but the fix SURFACE is research-to-confirm (operator chose "let research decide")
**Depth Tier:** Standard (4 researchers)
**Track Count:** 1
**Status:** Complete

---

## Problem statement (from the upstream dogfood failure)

`superclaude reflect run --depth deep --fix` exit-coded **11 (degraded / null-convergence)** on a clean deliverable. Root cause (traced during scope discovery): the wrapper exports `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE=1` into the reflect-audit subprocess env (correct — for nested-gate suppression), but that marker then leaks into the reflect skill's §6.1 step 5.5 **verification-triangle** subprocess (`pytest`), so when the audited change touches `tests/cli/reflect/`, the reflect-CLI tests (`test_cli_smoke`, `test_promote_plumbing`) invoke the reflect CLI, hit the `commands.py:69` recursion-breaker guard, and self-fail → false `degraded` / exit 11. Proof: `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` → all 10 pass; `verification_regressions_detected: 0`.

**The named files (`runner.py`/`commands.py`) are NOT the fix surface** — the marker MUST reach the reflect subprocess (nested-gate suppression). The leak is the verification GRANDCHILD inheriting it. The corrective fix strips the marker ONLY for the verification subprocess.

## EXISTING_FILES

- `src/superclaude/cli/reflect/commands.py` — `_WRAPPER_MARKER_ENV = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` (L44); group-callback recursion-breaker guard `if os.environ.get(_WRAPPER_MARKER_ENV, "").strip() == "1": exit 0` (L69). **Correct as-is** — this is the guard the verification tests trip on.
- `src/superclaude/cli/reflect/runner.py` — `_WRAPPER_MARKER = "SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE"` (L53); the reflect-audit ClaudeProcess is spawned with `env_vars={_WRAPPER_MARKER: "1"}` (L405-416), and the auto-run corrective-MDTM `/task` ClaudeProcess likewise (L440-448). The fix loop re-verifies by RE-RUNNING the audit (`_audit_once()`, L537), NOT by running pytest itself — so the verification pytest is inside the reflect skill subprocess.
- `src/superclaude/cli/pipeline/process.py` — `ClaudeProcess.build_env` (L145-160): `env = os.environ.copy(); if env_vars: env.update(env_vars)`. **This is the propagation mechanism** — the reflect subprocess inherits full os.environ + the marker; its `pytest` grandchild (Serena `Popen(shell=True)`) inherits the marker by default.
- `src/superclaude/skills/sc-reflect-protocol/SKILL.md` — **the likely fix surface.** §6.1 step 5.5 verification triangle (L467, L483, L491-500): runs non-mutating verification (`pytest`/`ruff`/`mypy`/`make`/build) via Serena `execute_shell_command` → `subprocess.Popen(command, shell=True)`. The §6.1.1 consumer-side safety envelope has 8 mandatory controls (a)-(h) (L491-500: verb allowlist, whole-command validation, per-invocation audit artifact, `--no-verify`, etc.). The fix adds a control: strip `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` from the verification subprocess env (run `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <cmd>`).
- `src/superclaude/skills/sc-reflect-protocol/refs/remediation-handoff.md` — L117 references the marker as the recursion-breaker (distinct from a headless signal). Confirms the marker's intended scope = recursion suppression, NOT verification-env participation.
- Tests: `tests/cli/reflect/test_marker_suppression.py` (5 tests — the recursion-breaker behavior), `test_cli_smoke.py`, `test_promote_plumbing.py`, `test_no_nesting_guard.py` (the reflect-CLI tests that trip under the marker).
- Authoritative contract: `/config/workspace/IronClaude/.claude/worktrees/reflectWrapper/.dev/handoffs/reflect-wrapper-contract.md` §3 (recursion breaker) — the marker suppresses nested gate EMISSION/execution; it does not sanction leaking into ordinary verification test runs.

## PATTERNS_AND_CONVENTIONS

- **Source of truth = `src/superclaude/`**; `.claude/` is `make sync-dev` output. Edit `src/`, then `make sync-dev` + `make verify-sync`. NEVER edit/stage `.claude/` (gitignored except settings.json).
- **UV only** for Python ops; tests in `tests/` via pytest.
- **CI ruff:** `make lint` runs only `ruff check`; CI separately runs `ruff format --check src/ tests/` — run `uv run ruff format --check` before declaring green.
- Reflect engine is "thin": `runner.py` launches ONLY via `ClaudeProcess` (never raw `subprocess.run`/`Popen`); no async/await; no sprint/roadmap imports (enforced by `test_no_nesting_guard.py` Layer B + thinness guards).
- The §6.1.1 envelope validates the WHOLE command structure under `shell=True` (not just the first verb) — an env-strip control must compose with that (e.g., the `env -u …` prefix must not break the verb-allowlist check at control (b), whose first token must be in `{pytest,ruff,mypy,make,uv,npm,tsc,cargo}` — so an `env -u` prefix may need the allowlist to treat `env` as a recognized wrapper, OR the env-strip is applied via the Popen `env=` kwarg rather than a command prefix. RESEARCH must resolve which mechanism the §6.1.1 envelope supports).

## GAPS_AND_QUESTIONS

1. **Exact fix mechanism in §6.1.1:** command-prefix (`env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <cmd>`) vs Popen `env=` kwarg (strip from the dict). The verb-allowlist control (b) checks the FIRST token — an `env -u` prefix would make `env` the first token, failing the allowlist unless handled. Research must determine the cleanest mechanism that composes with all 8 controls.
2. **Is the verification-command construction in the SKILL body (prose directive to the executing agent) or in code?** §6.1.1 is a skill-body safety envelope executed by the reflect agent via the Serena `execute_shell_command` tool — so the fix is a skill-body control instruction, not a Python edit. Confirm there is no Python wrapper around `execute_shell_command` in `cli/reflect/` that could host the env-strip.
3. **Regression-test surface:** the leak manifests only inside a live `claude --print` reflect subprocess (hard to unit-test end-to-end). The testable invariant: a verification-triangle command, when constructed by the §6.1.1 envelope, carries the marker-strip. Research must design a test that asserts the envelope's emitted command strips the marker (or that a marker-stripped pytest of `tests/cli/reflect/` passes while a marker-set one fails) WITHOUT requiring a live LLM subprocess.
4. **Does the contract (§3) need a clause** stating the marker is stripped for verification subprocesses? Research the contract to see whether the fix should also amend the contract's recursion-breaker semantics (§3.2) to document the verification-strip carve-out.

## RECOMMENDED_OUTPUTS

Research files (4 researchers, Standard tier), all under `research/`:
- `01-marker-propagation-trace.md` — R1 (Integration Points): the full env-propagation chain.
- `02-verification-envelope-surface.md` — R2 (Data Flow Tracer): §6.1.1 envelope + the precise fix insertion point + mechanism.
- `03-test-design.md` — R3 (Test & Verification): recursion-breaker test catalogue + regression-test design.
- `04-conventions-contract-template.md` — R4 (Patterns/Template/Contract): conventions, MDTM template 02 notes, marker contract semantics (§3.2).

## SUGGESTED_PHASES

- **R1 — Marker-propagation trace (Integration Points).** Scope: `commands.py` (L44/L69), `runner.py` (L53/L405-416/L440-448/L536-572), `pipeline/process.py` (`build_env` L145-160). Trace the marker from constant → group-guard → ClaudeProcess env_vars → os.environ.copy()+update → grandchild pytest inheritance. Confirm the marker MUST persist for the audit/nested-gate but is the leak source for verification. Output: `01-marker-propagation-trace.md`. Other researchers: R2 owns the verification envelope, R3 the tests, R4 conventions/contract — do not duplicate.
- **R2 — Verification-envelope surface (Data Flow Tracer).** Scope: `sc-reflect-protocol/SKILL.md` §6.1 step 5.5 + §6.1.1 (L467, L483-500), and any Python in `cli/reflect/` that constructs verification commands. Determine: where verification commands are constructed/run; the 8 §6.1.1 controls; the cleanest env-strip mechanism that composes with the verb-allowlist (control b); whether the fix is a skill-body control or code. Output: `02-verification-envelope-surface.md`. Other researchers: R1 propagation, R3 tests, R4 conventions/contract.
- **R3 — Test & Verification.** Scope: `tests/cli/reflect/test_marker_suppression.py`, `test_cli_smoke.py`, `test_promote_plumbing.py`, `test_no_nesting_guard.py`; test framework/patterns. Determine: how marker behavior is currently asserted; a regression-test design proving the verification subprocess strips the marker (without a live LLM run); the test file + naming + verification command. Output: `03-test-design.md`. Other researchers: R1 propagation, R2 envelope, R4 conventions/contract.
- **R4 — Patterns/Template/Contract.** Scope: MDTM template `02_mdtm_template_complex_task.md`; CLAUDE.md conventions (sync models, UV, ruff CI); the reflect-wrapper contract §3.2 marker semantics. Determine: template 02 required sections + B2 pattern; project conventions affecting item success (sync-dev, ruff format CI); the contract's intended marker scope (to ground "fix preserves nested-gate suppression" + whether §3.2 needs a verification-strip clause). Output: `04-conventions-contract-template.md`. Other researchers: R1 propagation, R2 envelope, R3 tests.

## TEMPLATE_NOTES

- **Template 02 (Complex Task):** the work is discovery (confirm the surface + mechanism) → fix (add the §6.1.1 env-strip control) → test (regression test) → validate (sync-dev/verify-sync/ruff/pytest) → final QA gate + POST reflect. Template 02 fits.
- **Tier Standard:** 4 researchers; the surface spans 3 components (cli/reflect engine, sc-reflect-protocol skill, tests) + the contract — more than Quick, not 20+ files.
- The generated task MUST include: a final-document QA gate (≥6 agents) per MDTM I19, and a POST_REFLECT_GATE per the wrapper contract — BUT note the recursion risk: this corrective task's own POST reflect gate would hit the SAME leak until the fix lands. The builder should either (a) make the POST gate `--no-verify` for this task, or (b) document that the POST gate validates the fix end-to-end (dogfood). Flag in Open Questions.

## GAP_FILL_RESOLUTIONS (orchestrator, post research-gate round 1)

The research gate (5 agents) returned 1 PASS + 4 FAIL — findings were cosmetic + builder-addressable, now resolved:

- **R2 status contradiction (4× flagged) → FIXED** directly: `02-verification-envelope-surface.md:3` normalized to `Status: Complete`.
- **R2 citation `693-698` → FIXED** to `694-698` (line 693 is `serena_summary_corroboration`; verification fields are 694-698).
- **R4 `.claude/templates` citation (MINOR)** → content is byte-identical to `src/superclaude/templates/workflow/02_mdtm_template_complex_task.md` (the authoritative source); the builder cites the `src/` path. Non-load-bearing.
- **Regression-test LOCATION (IMPORTANT) → DECISION: put the regression test in `tests/cli/reflect/test_marker_suppression.py`, NOT `test_no_nesting_guard.py`.** Rationale: (a) `test_no_nesting_guard.py` is already staged-modified by the sibling reflect-gate-wiring task (collision risk); (b) `test_marker_suppression.py` is the topically-correct home for marker-behavior assertions. The builder MUST target `test_marker_suppression.py`.
- **Verification command MUST include `test_marker_suppression.py` (IMPORTANT)** → re-proves nested-gate suppression is still intact after the fix (the marker must STILL suppress for the audit). Canonical verify cmd: `uv run pytest tests/cli/reflect/test_marker_suppression.py tests/cli/reflect/test_cli_smoke.py tests/cli/reflect/test_promote_plumbing.py -q`.
- **§6.1.1 edit anchor for the builder** → the §6.1.1 safety-envelope controls (a)-(h) live at `sc-reflect-protocol/SKILL.md:489-502`; verb allowlist `{pytest,ruff,mypy,make,uv,npm,tsc,cargo}` at `:494`. The builder authors: a NEW control (i) after (h) requiring verification commands run as `timeout <N> env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE <validated base command>`, PLUS a one-line clarification to control (b) that the verb-allowlist is checked against the BASE command (first token of the audited verification command), NOT the `env`/`timeout` wrapper prefix — so the env-strip wrapper composes with the allowlist.
- **`sc-tasklist-protocol/SKILL.md` marker refs → NO UPDATE NEEDED** → those occurrences are the O2 GATE-EMISSION skip guard (the generator emitting `SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE` into generated tasklists), unrelated to the verification-env leak. Confirmed out of scope.
- **Python-fallback test note** → the primary regression test is a source-contract test (asserts §6.1.1 carries `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE`), appropriate since the fix is skill-body. IF a future implementer moves the verification-command construction into Python, a direct unit test (env containing the marker → emitted verification invocation strips it) is required. The task documents this fallback.
- **Contract §3.2 carve-out** → add a narrow clause permitting marker removal ONLY for non-mutating verification/build/test subprocesses that cannot emit or execute reflect gates (R4). Keep the existing "MUST NOT clear/unset/overwrite" for the recursion-suppression path intact.

**Gate disposition:** cosmetic findings fixed + verified; substantive findings resolved by orchestrator decision (carried into the BUILD_REQUEST as explicit constraints). Proceeding to the builder; the A.10/A.10.25/A.10.5 task-validation gates (5 agents) provide downstream verification of the built task.

## AMBIGUITIES_FOR_USER

- **Named-surface divergence (RESOLVED by operator):** the request named `runner.py + commands.py`; scope discovery shows the fix surface is `sc-reflect-protocol/SKILL.md` §6.1.1. Operator chose "let research decide the surface" — the builder targets the evidence-supported surface and records the divergence + final target in the task's Open Questions.
- **POST-gate self-recursion:** this corrective task's own POST reflect gate would reproduce the exact leak it fixes (until applied). The builder should resolve whether the task's POST gate runs `--no-verify`, or is intentionally the end-to-end dogfood proof that the fix works. Flag in Open Questions for the executor.
