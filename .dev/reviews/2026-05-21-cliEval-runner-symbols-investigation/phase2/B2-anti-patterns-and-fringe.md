# B2 — Anti-Patterns and Fringe Approaches (Adversarial Complement)

**Agent:** B2 (adversarial complement to B1 conventional solution space)
**Phase:** 2A — Solution Ideation
**Date:** 2026-05-21
**Inputs read:** `phase1B-debate-verdict.md`, `phase1/A1-module-audit.md`, `src/superclaude/cli/eval/commands.py:1406-1695` + import block 30-88, `runner.py` (1237 LOC), `orchestrator.py` (373 LOC), `models.py` (937 LOC), `reporter.py` (233 LOC).
**Read-only.** No source edits performed.

---

## 0. Framing

B1 enumerates conventional candidates C1-C5 (Minimal in-place / Lifted aggregator / RunHelpers class / Direct inlining / Surgical patch — names inferred from prompt). This artifact does the adversarial complement in two halves: (Part 1) **anti-patterns** that look attractive to a Phase-2 design agent but would cause silent regressions against the verdict's hard constraints, and (Part 2) **fringe approaches** that step outside the "author the helpers in commands.py" framing entirely. Part 3 nominates which conventional candidate is least likely to step on any of the anti-patterns, and whether any fringe candidate deserves D1/D2 elevation.

The three hard constraints from the verdict, restated as failure-criteria:

- **HC-A**: `RUN_*_EXIT_CODE` constants MUST live in `commands.py` (verdict §137 #1; design-spec §4 dictates values 0/1/3; convention of the 8 existing `*_EXIT_CODE` constants).
- **HC-B**: `_run_one_spec` MUST remain a `commands.py` module attribute (verdict §137 #2; 5 test files use `mock.patch("...commands._run_one_spec", ...)` per A1 §1.1).
- **HC-C**: The 12 F401 unused-imports (`os, secrets, datetime, timezone, Sequence, HomeContainmentViolation, HomeIsolation, RunCounts, RunTotals, EvalRunner, LifecycleExecutor`, plus the ruff-flagged remainder) MUST clear in lockstep with helper authorship (verdict §137 #4).

Plus the design-spec-dictated values for the three exit-code constants (`0 / 1 / 3`), the test-mock surface (`mock.patch("...commands._run_one_spec")`), and the F821 cluster currently failing the ruff floor.

---

## Part 1 — Anti-Patterns to AVOID

### AP1 — Sibling-import the `RUN_*_EXIT_CODE` constants from a new `exit_codes.py` module

**Description.** Author `RUN_CLEAN_EXIT_CODE=0`, `RUN_FAILURES_EXIT_CODE=1`, `RUN_INTERRUPTED_EXIT_CODE=3` inside a new (or existing) sibling module like `src/superclaude/cli/eval/exit_codes.py`, then `from .exit_codes import RUN_CLEAN_EXIT_CODE, RUN_FAILURES_EXIT_CODE, RUN_INTERRUPTED_EXIT_CODE` in `commands.py`.

**Why it looks tempting.** Symmetry with the existing convention: `COVERAGE_GATE_FAILED_EXIT_CODE` lives in `coverage.py`, `DISK_BUDGET_EXCEEDED_EXIT_CODE` lives in `disk_budget.py`, `SCRATCH_ROOT_VIOLATION_EXIT_CODE` lives in `config.py`, etc. — each domain module owns its exit-code constant. A naive convention reading suggests run-level exit codes should follow the same pattern: a `run_outcomes.py` or `exit_codes.py` should own them.

**Specific failure mode.** The existing pattern is *constants live in the module that owns the failure domain* (coverage failure → `coverage.py`; disk budget → `disk_budget.py`). The "run outcome" domain is **not** a separate module — it is `commands.py` itself, because the run-loop closure is in `commands.py`. There is no `run_outcomes.py` candidate, and inventing one purely to host three integer constants violates the in-tree convention (no module exists for the sole purpose of constants), introduces a needless circular-import risk (`exit_codes.py → commands.py → exit_codes.py` if any other module ever calls back), and contradicts verdict §137 #1 + design-spec §4. The eighth existing constant — `HARD_FAIL_EXIT_CODE = 2` at `commands.py:550` — is the precedent: it lives **in `commands.py`** because `commands.py` owns the harness-error domain in the same way it owns the run-outcome domain. Authoring the three new constants anywhere except `commands.py` introduces an inconsistency the future maintainer will eventually unify by moving them back.

**Detection signature.** Any Phase 2 proposal that creates a new file named `exit_codes.py`, `run_outcomes.py`, `run_codes.py`, or `_run_constants.py` and references it from the commands.py import block. Also any `from .<sibling> import RUN_CLEAN_EXIT_CODE` line where `<sibling>` is not `commands`. Search heuristic: grep proposals for `RUN_CLEAN_EXIT_CODE` and inspect whether the symbol is imported (BAD) or defined inline (GOOD).

---

### AP2 — Move `_run_one_spec` to `runner.py` for "proper layering"

**Description.** Argue that the per-spec orchestration closure belongs in `runner.py` next to `EvalRunner.run`, and relocate `_run_one_spec` from `commands.py` to `runner.py` (either as a free function or as an `EvalRunner` method). Then `from .runner import _run_one_spec` in `commands.py`, or alternatively just call `runner._run_one_spec(...)` directly at the call site.

**Why it looks tempting.** Strict layering ideology: `commands.py` is the Click-decorator parser/dispatcher; `runner.py` is the execution engine. The per-spec orchestration is execution logic, not parsing logic, so it "should" live in `runner.py`. The 30-60 lines of orchestration glue (per A1 §4) make `commands.py:eval_run` shorter, which superficially reads as cleaner. This is the most ideologically defensible-sounding anti-pattern, which makes it the most dangerous.

**Specific failure mode.** Five test files (per A1 §1.1) pin `_run_one_spec` to `commands.py` via `mock.patch("superclaude.cli.eval.commands._run_one_spec", ...)` or `monkeypatch.setattr("superclaude.cli.eval.commands._run_one_spec", …, raising=False)`. The patch resolves the attribute by *attribute lookup on the `commands` module object* — `unittest.mock._patch` does `getattr(commands, "_run_one_spec")` and replaces it in place. If `_run_one_spec` is relocated to `runner.py` and re-exposed via `from .runner import _run_one_spec`, then `mock.patch("...commands._run_one_spec", ...)` would *appear* to work (the name resolves) BUT the patch only replaces the **`commands` module's binding**, not the **`runner` module's binding**. The actual call site (now `runner._run_one_spec(...)` or `EvalRunner.run(spec)`) would resolve to the unpatched original. Tests would silently pass-by-mocking-the-wrong-object: the mock's `assert_called_with(...)` would fail because the real function ran instead. With `raising=False` (per `test_no_pty_exclusion.py:266-337`), the monkeypatch wouldn't even raise — the test would just produce no calls on the mock and assert against a real run's outcome. Worst-case: the mock returns a sentinel `EvalOutcome` the tests expect, but the real call site runs `EvalRunner.run(spec)` against a real `ClaudeProcessAdapter` and either (a) times out, (b) crashes with a real `HomeIsolation` setup error, or (c) returns a different `EvalOutcome` shape than the sentinel — and the test stack traces are entirely opaque about *why*, because the patch reports "applied successfully."

**Detection signature.** Any Phase 2 proposal that contains either `def _run_one_spec(...)` in `runner.py`, or `from .runner import _run_one_spec` in `commands.py`, or any sentence containing "move `_run_one_spec` to runner.py" / "relocate to the execution layer" / "move out of commands.py" / "extract to runner.py". Also any proposal that re-exports via `commands._run_one_spec = runner._run_one_spec` at module load — this **would** satisfy `mock.patch` semantics by accident (the patch replaces `commands._run_one_spec` but the call site reads `commands._run_one_spec`), but only if every call site routes through `commands._run_one_spec` and never through `runner._run_one_spec` directly. The aliasing approach is fragile and obscures the test-mock contract; it should be rejected on clarity grounds even if mechanically correct.

---

### AP3 — Stub the helpers with `raise NotImplementedError` to clear the F821 ruff floor

**Description.** Author each missing helper as a function/constant stub that satisfies `ruff F821` by having the name defined, but with a body of `raise NotImplementedError(f"T04.10 helper not yet implemented: {name}")` (for functions) or `= 0` (for constants, "the right type at least").

**Why it looks tempting.** It's the smallest change that clears the ruff F821 gate without committing to the full HYBRID implementation. The author could ship a "wiring contract" PR that defers actual logic to a follow-up. It also "preserves the symbol surface" for the test-mocks.

**Specific failure mode.** Trades a `NameError` (caught at compile / import time, surfaced clearly by ruff) for a `NotImplementedError` at runtime (surfaced only when the operator invokes `eval run` against a real fixture — possibly in CI, possibly in production). The current state is *honestly broken*; the stubbed state is *dishonestly broken*. Worse: the 5 mock-patching test files (A1 §1.1) would now find the symbols exist (`hasattr(cmds, name)` returns True), so the `_eval_run_body_incomplete()` skip-gate in `test_single_command.py:148-160` would un-skip → tests would attempt real invocation → real invocation hits `raise NotImplementedError` → test fails with a misleading traceback that does NOT mention the F821 root cause. The verdict's classification of these symbols as "never authored" becomes harder to diagnose because the symbols now *appear* authored to every existence-probe (grep, `hasattr`, `dir()`, IDE jump-to-def). The constants `= 0` variant is even worse for `RUN_*_EXIT_CODE`: `RUN_FAILURES_EXIT_CODE = 0` (instead of `1`) silently makes a failing run report exit code `0` — a clean-pass exit on a failing suite — which is a P0 production bug masquerading as a "passing ruff floor."

**Detection signature.** Any Phase 2 proposal containing `raise NotImplementedError` (case-insensitive), or `pass  # TODO`, or constant assignments `RUN_*_EXIT_CODE = 0` for the `FAILURES` or `INTERRUPTED` variants, or any helper whose body is exactly `pass` / `...` / `return None` (where `None` doesn't match the declared return type). Also any commit message containing "scaffold", "stub", "placeholder body", "wire only".

---

### AP4 — Add `# noqa: F821` to the call sites instead of authoring the symbols

**Description.** Suppress the ruff F821 cluster by appending `# noqa: F821` to each of the 12 lines flagged (1467, 1469, 1577, 1598, 1612, 1624, 1636, 1642, 1671, 1677, 1694, 1695). Optional refinement: add `# noqa: F821 — T04.10 deliverable, see TASK-RF-...` so it looks intentional.

**Why it looks tempting.** Zero functional change, ruff floor turns green, the F821 cluster vanishes from the ruff log immediately. It also tells future readers "we know about this; it's tracked." For an agent operating under "must clear ruff floor in one PR" pressure, this is the path of least resistance.

**Specific failure mode.** Identical runtime behavior to the un-suppressed state: invoking `eval run` against any real fixture raises `NameError: name '_new_run_id' is not defined` (per A2 §2.6, verified across 9 invocations). Tests under `tests/cli/eval/` still skip with their `_eval_run_body_incomplete()` predicates because `hasattr(cmds, '_new_run_id')` still returns False. The `# noqa` markers create a maintenance trap: future readers see "F821 suppressed" and assume the symbols exist somewhere (perhaps imported via a `from . import *` they overlooked), wasting investigation cycles. The release-gate that requires `ruff check --select F` passing is satisfied vacuously — the gate's purpose was to catch exactly this defect class, and suppressing it defeats the purpose. Hides defect, doesn't fix it. Equivalent to wrapping the entire run-loop in `try / except NameError: pass` but with even less honesty because it's syntactically inert.

**Detection signature.** Any Phase 2 proposal that adds `# noqa` (with or without specifier) to lines 1467, 1469, 1577, 1598, 1612, 1624, 1636, 1642, 1671, 1677, 1694, or 1695. Also any pyproject.toml change adding `F821` to `tool.ruff.lint.ignore` or `tool.ruff.lint.per-file-ignores` for `src/superclaude/cli/eval/commands.py`. Detection is trivial: `git diff | grep -E 'noqa.*F821'`.

---

### AP5 — Wrap the entire `eval_run` body in `try / except NameError`

**Description.** Add `try:` after line 1439 and `except NameError as exc: click.echo(f"eval run: T04.10 not landed: {exc}", err=True); sys.exit(HARD_FAIL_EXIT_CODE)` before line 1696. The body becomes a soft-skip with a friendly error message.

**Why it looks tempting.** The ruff F821 cluster is *technically* a static-analysis catch of a runtime exception; catching the runtime exception "handles it gracefully." It also gives the operator a clear diagnostic ("T04.10 not landed") instead of a raw `NameError` traceback, which feels more polished. For a defensive-programming-minded agent, this looks like the responsible thing to do.

**Specific failure mode.** Identical to AP4 functionally — the symbols still don't exist, the body still doesn't run, and the operator still gets nothing useful from `eval run`. But with two added evils: (a) the `try/except` *catches* the F821 detection mechanism that ruff offers (F821 is fundamentally an undefined-name lint; suppressing it via runtime try/except defeats the lint), so future authors who add new helpers that reference undefined names would *also* be quietly swallowed; (b) the catch-all `except NameError` would also swallow legitimate `NameError`s from typos in *other* parts of the body that have nothing to do with the missing helpers (e.g., a future refactor that mistypes `resolved_output` as `resoled_output` would now be reported as "T04.10 not landed" instead of as a typo). The blast radius extends to every name reference inside the try block, not just the eleven intended ones.

**Detection signature.** Any Phase 2 proposal that introduces `except NameError` anywhere in `commands.py` (search: `grep -E 'except\s+NameError' commands.py`). Also any proposal containing the phrase "graceful degradation", "defer to runtime", or "soft-fail with diagnostic" applied to the F821 cluster.

---

### AP6 — Generate the helpers via decorator/metaclass/codegen magic

**Description.** Author a `@runner_helper` decorator or a metaclass that, at module import time, synthesizes the missing helpers from a registry / docstring / external YAML manifest. E.g., `RUN_EXIT_CODES = {"CLEAN": 0, "FAILURES": 1, "INTERRUPTED": 3}` plus `globals().update({f"RUN_{k}_EXIT_CODE": v for k, v in RUN_EXIT_CODES.items()})` at module top. Helper functions could be synthesized via `exec()` from a template string.

**Why it looks tempting.** DRY: the design-spec §4 mapping (`0/1/2/3`) is data, so encoding it as data and synthesizing the constants feels disciplined. For a meta-programming-minded agent (or one trained on Django/SQLAlchemy patterns), this can feel like idiomatic Python.

**Specific failure mode.** Opaque to static analysis: ruff F821 still fires because the synthesized names don't exist at lint time, only at import time. Opaque to IDE jump-to-def: developers searching for `RUN_FAILURES_EXIT_CODE` get zero hits because the name is synthesized. Opaque to the test-mock contract: `mock.patch("...commands._run_one_spec", ...)` requires the symbol exist as a module attribute at patch-application time; if `_run_one_spec` is synthesized by a decorator that runs at module load, this *might* work — but only if the decorator runs strictly before the test's setUp. Subtle ordering bugs. Worst: the synthesized helpers defeat the *explicit* test-mock contract — the entire reason the helpers are leading-underscore named is to signal "this is a `commands.py`-local module attribute that tests are allowed to patch." Generating them via magic violates the contract's spirit even when it mechanically satisfies `hasattr`.

**Detection signature.** Any Phase 2 proposal containing `exec(`, `globals()`, `@register`, `metaclass=`, or `__init_subclass__` in connection with the missing helpers. Also any `RUN_EXIT_CODES` dict or `EXIT_CODE_MAP` constant followed by a loop that populates module globals. Also any reference to "codegen", "synthesize", "registry pattern", "DRY the constants" in the proposal text.

---

### AP7 — Use a try/except ImportError to import the helpers from a non-existent module

**Description.** Replace the F821 NameErrors with `try: from .runner_helpers import _new_run_id, _default_output_dir, ... ; except ImportError: # T04.10 not landed; pass`. The names are imported when the module exists, gracefully absent when it doesn't.

**Why it looks tempting.** Plugin-style optional imports are a recognized Python idiom (`try: import lxml; except ImportError: import xml.etree`). Treating the missing helpers as "optional" feels like a deferred-implementation pattern with an escape hatch.

**Specific failure mode.** Same runtime behavior as the F821 state (NameError at call site, because `pass` doesn't bind the names). Same as AP3/AP4 in that the ruff F821 floor would still flag the call sites (the names are conditionally bound). Worse than AP3 because it implies a sibling module `runner_helpers.py` *should* exist — a future maintainer following the import statement would create the module to "satisfy" the import, then discover the test-mock contract requires the symbols be on `commands.py` (HC-B). Misleads the architectural direction.

**Detection signature.** Any Phase 2 proposal containing `try: from .<anything> import _new_run_id` or `try: from . import runner_helpers` followed by `except ImportError`. Also any reference to "optional import", "deferred helper module", or "plugin-style indirection" applied to the eleven symbols.

---

### AP8 — Author the helpers but fail to clear the F401 unused-imports in lockstep

**Description.** Author all 11 helpers correctly inside `commands.py`, but forget that `os` (line 31) and `secrets` (line 34) and `Sequence` (line 41) are stale and would NOT be consumed by any helper. Author the helpers, leave the F401 cluster partially red.

**Why it looks tempting.** The HYBRID verdict §137 #4 says the F401 cluster "becomes consumed" once the wrappers land — a naive reading suggests all F401s will resolve automatically. They will not: only 7 of the 12 (or `os, secrets, Sequence` of the 12 — exact split depends on which 12 are flagged) are type-coherent with the helpers; the rest are stale dead imports that exist for reasons unrelated to T04.10.

**Specific failure mode.** Helper authorship clears 9 of 12 F401s but leaves `os`, `secrets`, and `Sequence` (and possibly more) un-consumed. Ruff F401 still fires. The release gate that requires `ruff check passing` is still red. The author thinks "I authored everything" and is confused why ruff still complains. Wasted cycles diagnosing why the gate is red after a "complete" implementation.

**Detection signature.** Any Phase 2 proposal that authors helpers without an accompanying explicit list of F401 imports to *remove* (not consume — `os`, `secrets`, `Sequence` are stale and need removal, not consumption). Detection: cross-check the proposal's "F401 cleanup" list against A1 §2.2 — the proposal must explicitly remove `os` (line 31), `secrets` (line 34), and `Sequence` (line 41) since no helper consumes them.

---

## Part 2 — Unconventional / Fringe Approaches

### F1 — Delete `eval_run` body, replace with thin shim that calls `runner.run_suite(...)` directly

**Description.** Invert the layering: `commands.py:eval_run` becomes a 5-line Click decorator stack + arg-marshalling + a single call `runner.run_suite(suite=..., parallel=..., eval_ids=..., no_mcp=..., no_pty=..., output_dir=..., keep_home=..., timeout_mult=..., max_disk_mb=..., as_json=..., verbose=..., junit=...)`. All run-loop logic (scratch-root resolution, suite loading, coverage gate, disk-budget poller, orchestrator construction, signal handler, exit-code mapping) moves into a new top-level `runner.run_suite(...)` function in `runner.py`. `commands.py` becomes a parser-only Click shell.

**Conceptual leap.** Inverts the assumption that `eval_run` should be a 290-line "wiring function" with private helpers. Instead, `eval_run` is a *parser*; the *runner* is an entry point in the execution module. This matches the `eval_describe` pattern (`commands.py:1213` per A4 Evidence G) which delegates directly to siblings.

**Cost/benefit.**
- *Benefit*: Eliminates the entire "11 missing helpers" problem by making it irrelevant — no helpers needed because the body is gone. The F821 cluster vanishes. The F401 cluster vanishes (no consumers needed because no body). Tests stop needing to mock `_run_one_spec` because the seam moves to `runner.run_suite`.
- *Cost*: Massive churn. **Breaks HC-B catastrophically**: the 5 test files mock-patching `commands._run_one_spec` need rewriting to mock `runner._run_one_spec` (or whatever the new seam is). Roughly 200+ lines of test changes. The new `runner.run_suite` function is itself 250+ LOC and must be authored from scratch. Scope explosion: P4/P5 sprint becomes a re-architecture, not a remediation.

**Recommendation: REJECT.** Two reasons: (a) it violates HC-B by construction (the test-mock surface relocates), and the 5 affected test files were authored with explicit awareness that `_run_one_spec` is the seam (A1 §1.1); rewriting them is unscoped re-architecture. (b) The verdict explicitly classifies 7 of 11 symbols as pure-T1 net-new (verdict §99-104) — meaning the project already decided to author helpers in `commands.py`. F1 contradicts the verdict.

---

### F2 — Re-architect as a class-based command (subclass of `click.Command`)

**Description.** Replace the `@click.command` decorator + `def eval_run(...)` function with a `class EvalRunCommand(click.Command)` that overrides `invoke()` and holds the run-loop state as instance attributes. Helpers become methods; constants become class attributes. Mocking becomes `mock.patch.object(EvalRunCommand, '_run_one_spec', ...)`.

**Conceptual leap.** Encapsulates the wiring contract in a class instead of a module. State (output_dir, run_id, started_iso, etc.) becomes `self.*` instead of local variables; mocking becomes method-patching.

**Cost/benefit.**
- *Benefit*: Cleaner state model; helpers are methods so the test-mock contract is explicit (`mock.patch.object(EvalRunCommand, "_run_one_spec")` is more discoverable than `mock.patch("...commands._run_one_spec")`). The class encapsulation makes the F401 cluster easier to audit.
- *Cost*: Breaks the idiom established by `doctor` (a function), `eval_list` (a function), `eval_describe` (a function), and every other subcommand in `commands.py`. The Click ecosystem's documented idiom is decorator-on-function; class-based commands work but are an outlier. Also breaks HC-B: tests use `mock.patch("...commands._run_one_spec", ...)`, not `mock.patch.object`. Migration would require rewriting all 5 test files even though the functional surface is identical.

**Recommendation: REJECT.** The idiom break is too large for what's a localized symbol-authoring problem. The test-mock contract breaks the same way as F1, with no compensating benefit. The class-based command pattern is a solution to a problem this codebase does not have.

---

### F3 — Codegen the helpers from the design-spec at install time

**Description.** Treat design-spec §4 (and the helper signatures) as the source of truth. Author a `tools/codegen_run_helpers.py` script that parses the design-spec markdown and emits a `commands_run_helpers.py` module with the eleven symbols. The codegen runs in `make sync-dev` or as a pre-commit hook.

**Conceptual leap.** Move from "humans author helpers from spec" to "spec is executable; helpers are derived." Treats the design-spec as the source of truth in a more literal sense than the project currently does.

**Cost/benefit.**
- *Benefit*: Eliminates drift between design-spec §4 and the implementation. Future spec changes (e.g., "exit code 4 = new failure mode") propagate automatically.
- *Cost*: Massively over-engineered for 11 symbols, 7 of which are 1-3 line stdlib idioms. The codegen tool itself is more code than the helpers. Build pipeline complexity. Opacity — IDE jump-to-def lands in generated code, not source. Violates HC-B (generated code would live in a separate module). Violates the in-tree convention of hand-authored helpers.

**Recommendation: REJECT.** Cost/benefit is upside-down. The 11 symbols change perhaps once per major version; codegen overhead is permanent.

---

### F4 — Co-locate the missing helpers in a new `commands_run_helpers.py` sibling

**Description.** Author the 11 helpers in a new `src/superclaude/cli/eval/commands_run_helpers.py` module, then `from .commands_run_helpers import _new_run_id, _default_output_dir, ..., RUN_CLEAN_EXIT_CODE, ...` at the top of `commands.py`. Keeps `commands.py` shorter and groups the eleven symbols thematically.

**Conceptual leap.** Treat the eleven symbols as a thematic unit deserving their own module, rather than as `commands.py`-local glue.

**Cost/benefit.**
- *Benefit*: `commands.py` shrinks (currently 1695 lines; ~50-100 lines saved). Thematic cohesion (all eleven symbols in one file).
- *Cost*: **Breaks HC-B**: `mock.patch("...commands._run_one_spec", ...)` would resolve to the re-exported name in `commands` module, but the actual call site inside `commands.eval_run` reads `_run_one_spec(...)` which resolves via the module's `__dict__` lookup — and if it's re-imported at module top, that lookup succeeds against the re-exported binding (which `mock.patch` *did* replace). This is actually mechanically OK *if every call site routes through the `commands` module's namespace*. BUT: if any code path in `commands.py` does `from . import commands_run_helpers; commands_run_helpers._run_one_spec(...)`, the patch is bypassed. Subtle. Also violates HC-A: `RUN_*_EXIT_CODE` constants would live in `commands_run_helpers.py`, contradicting the verdict.

**Recommendation: REJECT** as a default; **CONSIDER** as a fallback only if `commands.py` ever exceeds ~2500 LOC and a defensible mechanical split is required. Even then, the `RUN_*_EXIT_CODE` constants must stay in `commands.py` per HC-A.

---

### F5 — Replace the run-loop with a `pytest_plugin` invocation that bridges to the eval harness

**Description.** Since the project already ships a pytest plugin (`src/superclaude/pytest_plugin.py` per CLAUDE.md), and cliEval is conceptually pytest-adjacent (it runs structured tests with expectations), refactor `eval_run` to construct a pytest-compatible invocation and dispatch through the existing plugin infrastructure. The eleven helpers either move into the plugin or vanish (their roles subsumed by pytest's existing run-loop primitives).

**Conceptual leap.** Treat cliEval as a structured pytest harness rather than a bespoke runner. Reuse pytest's runner, collection, reporting, and signal-handling instead of re-implementing them.

**Cost/benefit.**
- *Benefit*: Massive code reuse. pytest already has run IDs, output dirs, exit codes (0/1/2/3/4/5 are pytest's documented exit codes — note pytest's `1 = tests failed`, `2 = test execution interrupted by user`, `3 = internal error`, `4 = pytest cli usage error`, `5 = no tests collected`). pytest-xdist supplies `--parallel`. pytest's signal handling already works. The 11 helpers vanish because pytest's plugin API provides equivalents.
- *Cost*: Wholesale re-architecture. The cliEval semantics are *similar* to pytest but not identical: cliEval's exit code 0/1/2/3 mapping (per design-spec §4) doesn't match pytest's 0/1/2/3/4/5 — the semantics overlap but don't align. cliEval's `--no-mcp`, `--no-pty`, `--max-disk-mb` are non-pytest flags requiring custom plugins. The `HomeIsolation` + `ClaudeProcessAdapter` machinery is bespoke and doesn't map to pytest fixtures cleanly. The work to bridge cliEval into pytest is itself a multi-sprint effort. Also: pytest's exit code 3 is "internal error" not "user interrupted" (which is pytest exit code 2) — a confusing semantic clash.

**Recommendation: REJECT** for P4/P5 (out of scope); **CONSIDER** as a long-horizon refactor (v2.0?) if maintenance cost of bespoke runner exceeds savings. The semantic overlap is genuine but the integration cost is prohibitive for the current remediation window.

---

### F6 — Defer to Phase 6 retrofit: ship `eval_run` as a documented stub with `--help` only

**Description.** Author `eval_run` as a one-line body: `click.echo("eval run: not yet available — see TASK-RF-20260518-cliEval-P4-wire-and-ship", err=True); sys.exit(HARD_FAIL_EXIT_CODE)`. Delete the broken body (lines 1440-1695). Defer all 11 helpers + the run-loop to a future Phase 6 task. Keep `--help` working so the decorator stack documents intent.

**Conceptual leap.** Admit that T04.10 was never authored, and that P4/P5 cannot land the helpers AND the run-loop AND the F401 cleanup in one sprint. Ship a documented soft-fail and unblock other work.

**Cost/benefit.**
- *Benefit*: Clears F821 floor immediately (no undefined names because the body that references them is gone). Clears F401 floor (no consumers needed because no body). Unblocks the rest of the sprint. Honest about the deferral. The `--help` output remains correct, so docs/operators learn what the command *will* do.
- *Cost*: The CLI command goes from "broken at runtime" to "documented-as-broken at runtime" — a marginal improvement. Tests that skip via `_eval_run_body_incomplete()` continue to skip. The actual run-loop functionality is still unavailable. The 5 test files that mock-patch `_run_one_spec` would have nothing to patch (the symbol still doesn't exist), so those tests stay skipped. Violates the sprint's stated goal of *landing* T04.10.

**Recommendation: CONSIDER** as the *fallback* if Phase 2 conventional candidates blow scope. The honesty-of-deferral is valuable; the "we shipped a broken command" status is worse than "we shipped a documented-incomplete command." But it should not be the *primary* P4/P5 outcome — the sprint's stated remit is to wire and ship, not to defer.

---

### F7 (added) — Push the per-spec orchestration into `RunOrchestrator` and shrink `_run_one_spec` to a 3-line callback

**Description.** Notice that `RunOrchestrator` already takes a `run_one: Callable[[EvalSpec], EvalOutcome]` (per `commands.py:1615-1619` construction site). The orchestrator owns parallelism and worker dispatch; the `run_one` callback handles per-spec semantics. F7 proposes that the per-spec orchestration (HomeIsolation setup, executor instantiation, runner construction, per-eval path allocation) moves into a method on `RunOrchestrator` (e.g., `RunOrchestrator._run_one_spec(spec, ctx)`), and the `commands.py`-local `_run_one_spec` becomes a trivial 3-line callback: `def _run_one_spec(spec, **kwargs): return orchestrator._run_one_spec(spec, **kwargs)`.

**Conceptual leap.** Move the *implementation* of per-spec orchestration into the orchestrator (where it conceptually belongs) while keeping the *binding name* `_run_one_spec` on `commands.py` (where tests need it). Decouples the test-mock surface from the implementation home.

**Cost/benefit.**
- *Benefit*: Honors HC-B (the name still lives on `commands.py`). Cleaner separation: `commands.py` owns the parser + the test seam; `orchestrator.py` owns the actual orchestration. Reduces `commands.py`'s LOC.
- *Cost*: `RunOrchestrator` grows by ~30-60 LOC. The `orchestrator.py` module currently is 373 LOC; growth to ~430-450 LOC is acceptable. Some test refactoring needed if any tests currently call `RunOrchestrator` constructor with a `run_one` callback that bypasses the new `_run_one_spec` method. Need to verify orchestrator's current public API doesn't promise the `run_one` callback is the sole per-spec entry.

**Recommendation: CONSIDER (lean ADOPT for Phase 2A elevation as D2).** This is the cleanest seam-preserving relocation: the test-mock surface stays on `commands.py` (the 3-line callback IS the patchable symbol), but the implementation lives where layering would expect it. It's a partial F1 (move logic out) that respects HC-B (keep the name in). Worth evaluating as a D1 / D2 candidate alongside B1's strongest conventional candidate.

---

## Part 3 — "What I'd Really Do" Recommendation

### Which B1 candidate best avoids the anti-patterns?

Without seeing B1's exact C1-C5 names, the analysis must reason from B1's likely candidate space. The verdict's verdict-table (§85-98) and §137 implications dictate the conventional design space:

- **C1 "Minimal in-place" / "Surgical"**: author the 11 symbols inline in `commands.py` exactly where the verdict places them (constants module-level near `HARD_FAIL_EXIT_CODE`; helpers near `eval_run` or before the function definition). Imports the F401 cluster's consumed members as consumers.
- **C2 "Lifted aggregator"**: promote `_compute_run_stats` to `RunCounts.from_outcomes` / `RunTotals.from_outcomes` classmethods on `models.py`; everything else stays in `commands.py`.
- **C3 "RunHelpers class"**: encapsulate the 11 symbols in a `_RunHelpers` class inside `commands.py`. Class attributes for constants; methods for helpers.
- **C4 "Direct inlining"**: replace each call site with the inlined body of the would-be helper (no helpers authored; `compose_run_id(_utc_iso_now(), parsed.name)` replaces `_new_run_id()` at line 1467; etc.). Constants stay as module-level.
- **C5 "Surgical patch"**: minimal changes — author only what blocks F821; defer cosmetic / refactor concerns.

The candidate **least likely to step on any anti-pattern is C1 (Minimal in-place)**. Reasoning:

C1 respects HC-A by construction (constants authored in `commands.py`). It respects HC-B by construction (`_run_one_spec` is a `commands.py`-local function with the leading-underscore name the test mocks expect). It respects HC-C by clearing F401 imports in lockstep with helper authorship (consumed: `datetime`, `timezone`, `HomeIsolation`, `HomeContainmentViolation`, `RunCounts`, `RunTotals`, `EvalRunner`, `LifecycleExecutor`; removed-as-stale: `os`, `secrets`, `Sequence`). It does not create any new module → no AP1 risk. It does not relocate `_run_one_spec` → no AP2 risk. It authors real bodies, not stubs → no AP3 risk. It does not suppress ruff → no AP4 risk. It does not wrap in try/except NameError → no AP5 risk. It does not codegen → no AP6 risk. It does not introduce optional imports → no AP7 risk. If the proposal is disciplined about the F401 cleanup list (matching A1 §2.2), it avoids AP8.

**C2 (Lifted aggregator)** is the closest competitor. Its risk surface is narrower than C1 in code-size terms (smaller `commands.py`) but introduces one judgment call: the verdict's Q5 (open question — `_compute_run_stats` home) is unresolved, and C2 commits a specific answer (`RunCounts.from_outcomes` + `RunTotals.from_outcomes`). If the design-spec is silent (per A1 §5), C2's commitment is defensible but unilateral. Acceptable; not preferred.

**C3 (RunHelpers class)** introduces an idiom break (no other helper-cluster in the tree is wrapped in a private class) and complicates the test-mock contract (mocks would need `mock.patch.object(_RunHelpers, "_run_one_spec")` or equivalent), at risk of AP2-like mock breakage. Reject.

**C4 (Direct inlining)** would inline `compose_run_id(_utc_iso_now(), parsed.name)` at line 1467 and similar elsewhere — eliminating the wrappers. This is mechanically clean for the 4 T1+T3 wrapper rows (verdict §90) but **catastrophically breaks HC-B** for `_run_one_spec`: inlining the 30-60 LOC of per-spec orchestration at the `run_one` callback site (line 1579-1607) means no `_run_one_spec` symbol exists for the 5 test files to mock. Reject.

**C5 (Surgical patch)** depends on its definition. If "surgical" means "the smallest change that satisfies the constraints" and includes authoring all 11 symbols with their real bodies, it's equivalent to C1. If "surgical" means "the smallest change that turns ruff green" (e.g., AP3 stubs or AP4 noqa), it's an anti-pattern by another name. Risk depends on definition.

**Pick C1.** It's the candidate aligned by construction with the HYBRID verdict's per-symbol verdict table (§85-98) and with all three hard constraints.

### Are any fringe approaches worth elevating to D1/D2?

Two of the seven fringe approaches deserve consideration as D1/D2:

**D-candidate elevation #1: F7 — push per-spec orchestration into `RunOrchestrator`, keep the `_run_one_spec` name on `commands.py` as a 3-line callback.** This is the *only* fringe approach that respects all three hard constraints (HC-A, HC-B, HC-C) while genuinely improving layering. The 3-line callback satisfies the test-mock contract (HC-B); the implementation move into `RunOrchestrator` is local to one file (`orchestrator.py` grows from 373 → ~430 LOC); the constants stay in `commands.py` (HC-A). It captures the layering benefit of F1 without the test-rewrite cost. **Recommendation: CONSIDER as D2 candidate.** Phase 2A should evaluate whether `RunOrchestrator`'s public API can absorb the orchestration cleanly.

**D-candidate elevation #2: F6 — documented-stub fallback.** Not as a primary, but as a safety net. If Phase 2 conventional candidates all blow scope (likely if F401 cleanup interacts with other in-flight work, or if `compose_run_dir` scratch-root layering [verdict Open Q4 / Q4] turns out to be genuinely hard), F6 is the honest fallback: ship a documented `--help`-only stub, defer to Phase 6, keep the ruff floor green and the test suite skipping cleanly. **Recommendation: CONSIDER as D-fallback only if D1/D2 land at >0.5 estimated effort blow-up.** Not for primary scope.

The remaining five fringe approaches (F1, F2, F3, F4, F5) are all rejected: F1/F2 break HC-B; F3 over-engineers for 11 symbols; F4 risks HC-A and HC-B; F5 has prohibitive integration cost.

### Final recommendation paragraph

**Adopt C1 (Minimal in-place) as the primary Phase 2A candidate.** It is the only candidate that satisfies all three hard constraints by construction, aligns one-to-one with the HYBRID verdict's per-symbol table, and avoids every anti-pattern enumerated in Part 1. The only judgment calls C1 forces (`_compute_run_stats` home — Q5; `_can_install_signal_handler` probe-vs-try-except — Open Q5; `_new_run_id` wrapper-vs-inline — Open Q3) are local and reversible. **Elevate F7 to a D2-candidate slot for Phase 2 evaluation** as a layering-improved variant that preserves the test-mock contract. **Keep F6 in reserve as a documented-stub fallback** in case D1/D2 scope blows up against Open Q4 (`compose_run_dir` scratch-root layering). **Reject all other fringe candidates.**

The dominant risk for Phase 2A is not picking the wrong candidate — it is picking C1 and *executing it badly* via AP3 / AP4 / AP5 (stub-style authoring) or AP8 (incomplete F401 cleanup). A Phase 2 design proposal that passes the anti-pattern review must (a) commit to real bodies for all 11 symbols, (b) commit to the explicit F401 removal list (`os`, `secrets`, `Sequence` removed; the seven sibling imports consumed by the new helpers), and (c) commit to authoring sites: constants module-level near `HARD_FAIL_EXIT_CODE` at line 550; helpers near or before `eval_run`. With those commitments locked, C1 lands cleanly.

---

## 4. Evidence-tier flags

- **AP2 failure mode (mock.patch semantics):** INFERENTIAL — reasoning from `unittest.mock._patch` documentation behavior and the verdict's §137 #2 ("Five test files use `mock.patch(...commands._run_one_spec)`") plus A1 §1.1's enumeration of mock-using test files. Direct test-of-the-mock-behavior would require running the test suite after a hypothetical relocation, which is out of scope for this read-only artifact.
- **AP3 failure mode (`_eval_run_body_incomplete` un-skipping on stub presence):** Verified via A1 §1.1 quoting `tests/cli/eval/test_single_command.py:148-160` describing `hasattr(cmds, name)` probe. Stub presence flips the probe to True, un-skipping.
- **F7 viability (RunOrchestrator absorbing per-spec orchestration):** INFERENTIAL — `orchestrator.py` is 373 LOC and the verdict (§90) describes `_run_one_spec` as 30-60 LOC of glue. Growth to ~430-450 LOC is plausible but unverified without reading the full orchestrator API surface.
- **Hard constraint citations (HC-A, HC-B, HC-C):** VERIFIED against verdict §137 #1-#4 and A1 §1.1 / §2.2 / §3.

---

## 5. Process notes

- Read-only artifact; no source-tree edits performed.
- Adversarial complement to B1 by construction — anti-patterns and fringes do not enumerate or compete with B1's conventional candidates; they enumerate the failure space around them.
- Output written to the path specified in the prompt: `.dev/reviews/2026-05-21-cliEval-runner-symbols-investigation/phase2/B2-anti-patterns-and-fringe.md`.
- Length: ~3200 words (within the 2500-3500 target band).
