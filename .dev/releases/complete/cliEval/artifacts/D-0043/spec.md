# D-0043 — OPS-002 scratch-root policy enforcement

**Task**: T02.25 (Phase 2 — cliEval harness)
**Tier**: STRICT
**Risk**: Medium (Risk Drivers: scope — cross-cutting policy)
**Roadmap**: R-043 / OPS-002 ("Enforce scratch root policy across config/isolation/CLI")
**Cross-links**: D-0001 (`EvalConfig`, T01.01), D-0016 (`resolve_scratch_root`, T01.19), D-0029 (`containment_guard`, T02.08)

## Goal

OPS-002 is the **cross-module readout** for the AC12 scratch-root
allowlist. The allowlist itself was codified at T01.19 (D-0016 ships
`resolve_scratch_root` + `ScratchRootViolation`) and the defense-in-depth
HomeIsolation guard was codified at T02.08 (D-0029 ships
`containment_guard`). What was missing — and what D-0043 lands — is the
**operator-facing policy contract**: a canonical policy paragraph that
every CLI boundary quotes verbatim when refusing a non-allowlisted root,
plus the prose documentation that names the three allowed roots and how
they fit together.

The deliverable closes three drift surfaces:

1. **Prose drift** — without authoritative docs, operators reading a
   doctor failure could not tell whether the rejected path was a bug or
   an unstated policy. `docs/eval/scratch-roots.md` names the three
   roots and links to the implementation modules so a reader can
   navigate from prose to code.
2. **Message drift** — without a single rendering helper, the doctor
   and the (future) `eval run` command could each format
   `ScratchRootViolation` differently and quote the policy in
   inconsistent words. `format_scratch_root_violation()` is the one
   renderer; every CLI boundary funnels through it.
3. **Spec/code drift** — without a constant, the policy text would live
   only in prose docs (which can rot). `SCRATCH_ROOT_POLICY` in
   `config.py` is the single source of truth; the doc cross-references
   it and the tests assert the doc + constant + default allowlist all
   name the same three roots.

## Public surface (new)

| Symbol | Kind | Purpose |
|---|---|---|
| `SCRATCH_ROOT_POLICY` | `str` constant in `src/superclaude/cli/eval/config.py` | Canonical multi-line policy paragraph naming the 3 allowed roots, OPS-002/AC12 identifiers, and `docs/eval/scratch-roots.md` as the authoritative reference. |
| `format_scratch_root_violation(exc) -> str` | function in `src/superclaude/cli/eval/config.py` | Render a `ScratchRootViolation`: per-violation forensic detail + blank line + `SCRATCH_ROOT_POLICY` verbatim. Every CLI catch-site MUST funnel through this helper. |
| `superclaude eval doctor --output-dir <path>` | new Click option in `src/superclaude/cli/eval/commands.py` | Validates `<path>` against the policy via `resolve_scratch_root()`. Allowlisted → green doctor run (exit 0). Non-allowlisted → exit `SCRATCH_ROOT_VIOLATION_EXIT_CODE` (= 2); stderr quotes the policy verbatim via the renderer. Runs BEFORE HARD-capability probing so a misconfigured invocation does not spam unrelated capability failures. |
| `docs/eval/scratch-roots.md` | prose documentation | Authoritative reference: lists the three allowed roots, explains the allowlist-not-denylist rationale, walks through doctor + `eval run` + programmatic surfaces, and names the modules that enforce the policy. |

## The three allowed roots (verbatim)

| # | Root | Provenance |
|---|---|---|
| 1 | `/tmp/eval-runs/` | Canonical M1 scratch root. Lives in `_default_allowed_scratch_roots()` (D-0001). |
| 2 | `<repo>/.dev/eval-runs/` | Repo-relative scratch root. Resolves against process CWD via `Path.resolve()`. |
| 3 | `--output-dir <path>` | Operator-supplied, call-scoped: extends the allowlist for the current invocation only; never mutates `EvalConfig.allowed_scratch_roots`. |

The constant, the default-factory, and the prose doc MUST list the same
three roots. `tests/cli/eval/test_scratch_root_policy.py::test_default_allowlist_matches_policy_constant`
and `::test_scratch_roots_doc_names_three_allowed_roots` enforce the
spec/code/doc agreement.

## Test matrix

`tests/cli/eval/test_scratch_root_policy.py` (16 cases, all green).

| Section | Cases | Purpose |
|---|---|---|
| Policy constant | 3 | Names the 3 roots; references the doc; carries OPS-002/AC12 identifiers. |
| Renderer | 3 | Includes forensic detail; appends policy block; uses blank-line separator. |
| Doctor CLI | 4 | Rejects non-allowlisted, rejects real-HOME path, accepts allowlisted, scratch-violation takes precedence over HARD probes. |
| Single source of truth | 2 | Default allowlist matches policy constant; narrowed `EvalConfig` changes which paths `resolve_scratch_root` accepts. |
| Doc anti-drift | 3 | Doc file exists; names the 3 roots; cross-references the load-bearing module symbols (`EvalConfig.allowed_scratch_roots`, `resolve_scratch_root`, `containment_guard`). |
| Doctor / default-EvalConfig wiring | 1 | Doctor accepts `/tmp/eval-runs/` AND rejects `/tmp/other-runs/` in the same fixture — proves doctor uses the default `EvalConfig` allowlist, not an embedded copy. |

## Acceptance criteria

| AC | Source | Verified by |
|---|---|---|
| AC1 — File `docs/eval/scratch-roots.md` exists and documents the 3 allowed roots | T02.25 AC bullet 1 | `test_scratch_roots_doc_exists`, `test_scratch_roots_doc_names_three_allowed_roots` |
| AC2 — Doctor failure messages quote the policy text exactly when a non-allowlisted root is supplied | T02.25 AC bullet 2 | `test_doctor_rejects_non_allowlisted_output_dir`, `test_doctor_rejects_real_home_output_dir`, `test_doctor_uses_default_evalconfig_allowlist` |
| AC3 — `EvalConfig.allowed_scratch_roots` (T01.01) remains the single source of truth | T02.25 AC bullet 3 | `test_default_allowlist_matches_policy_constant`, `test_narrowing_config_changes_what_resolve_accepts` |
| AC4 — `D-0043/spec.md` records the cross-module policy | T02.25 AC bullet 4 | this document |
| AC5 — `uv run pytest tests/cli/eval/test_scratch_root_policy.py -v` exits 0 | T02.25 Steps[5] | `evidence/T02.25/pytest-T02.25.log` (16 passed in 0.14s) |

## Cross-module policy contract

| Module | Role | OPS-002 wiring |
|---|---|---|
| `config.EvalConfig.allowed_scratch_roots` | Sole allowlist source | Default tuple set in `_default_allowed_scratch_roots()`. No other module embeds a copy. |
| `config.resolve_scratch_root()` | Sole ingress for path validation | Raises `ScratchRootViolation` on non-allowlisted paths. CLI boundaries catch and render via `format_scratch_root_violation`. |
| `config.SCRATCH_ROOT_POLICY` | Sole policy text | Constant; doc + renderer + tests all read it. |
| `config.format_scratch_root_violation()` | Sole renderer for CLI surfaces | Returns forensic detail + policy. Doctor calls it; future `eval run` MUST call it. |
| `commands.doctor` (`--output-dir`) | Operator pre-flight | Validates a candidate path against the policy before HARD capability probing. |
| `isolation.containment_guard()` | FR-ISO2 defense in depth (D-0029) | Re-applies the same policy via `resolve_scratch_root` post-mkdtemp. Carries the same exit code semantics through `ScratchRootViolation`. |
| `docs/eval/scratch-roots.md` | Operator-facing prose | Authoritative reference; cross-linked from the policy constant. |

## Why a renderer, not just `str(exc)`?

The cliEval roadmap promises operators a consistent message across
modules. `str(ScratchRootViolation)` carries the per-violation forensic
detail (offending path, resolved form, allowlist that was checked) but
not the human-readable policy paragraph. A naïve implementation would
inline the policy at every catch site; the renderer enforces the "one
text, one place" guarantee. When the policy ever changes (e.g., adding
a fourth allowed root), the constant + doc + tests are the only
locations the change needs to land — every CLI boundary picks it up by
construction.

## Public API touched

* **Added (in `src/superclaude/cli/eval/config.py`):**
  - `SCRATCH_ROOT_POLICY` (`str`)
  - `format_scratch_root_violation(exc)` (function)
* **Added (in `src/superclaude/cli/eval/commands.py`):**
  - `eval doctor --output-dir <path>` Click option
* **Added (in `src/superclaude/cli/eval/__init__.py`):**
  - `SCRATCH_ROOT_POLICY` and `format_scratch_root_violation` re-exports
    (kept the `__all__` list alphabetized).

No existing symbols were renamed, removed, or had their signatures
changed. The sibling test family (`test_doctor.py`,
`test_scratch_root_allowlist.py`, `test_config.py`) stays green —
69-test re-run captured in `evidence/T02.25/pytest-policy-family.log`.
