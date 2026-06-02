---
artifact: r1-3-codeassertion-design
phase: 8
release: R1.3
task: TASK-RF-20260531-042405
created_date: 2026-06-02
author: task-executor
status: draft
source_authorities:
  - "BUILD-REQUEST §MVR §2 (gate contract: GateCriteria admits code-graph predicates)"
  - "BUILD-REQUEST §Contract #2 (dispatch-reachability invariant)"
  - "master:§Flaw 1 (no code-graph predicates in gate signatures; certify unreachable)"
  - "Vector A — preserve/invert axes (GateCriteria is invert candidate)"
verified_against: "worktree HEAD daa10416 — refactor/roadmap-pipeline-r0-r1-rewrite branch"
---

# R1.3 — `GateCriteria.code_assertions` Slot + First `CodeAssertion` (Design)

## 1. Purpose & Scope

Extend the substrate `GateCriteria` dataclass with a new `code_assertions:
list[CodeAssertion] | None = None` slot that admits code-graph predicates
(import-and-call, AST walks) alongside the existing content-string
`semantic_checks`. Wire the FIRST `CodeAssertion` into `CERTIFY_GATE` so the
gate fails fast if `build_certify_step()` is not reachable from the
production pipeline dispatch map — operationalizing BUILD-REQUEST §MVR §2
verbatim ("CodeAssertion guarantees no future step ships unwired") and
killing master:§Flaw 1 evidence chain for the certify-step case.

This is the substrate change that makes R1.5's `verify-implementation`
terminal step possible. R1.3 ships ONE assertion as proof-of-concept; R1.5
will populate the full FR→AST link assertion set.

## 2. Source-of-Truth File:Line Citations (HEAD daa10416, this worktree)

| Concern | File | Lines | Notes |
| --- | --- | --- | --- |
| `SemanticCheck` analogue | `src/superclaude/cli/pipeline/models.py` | 81-87 | `check_fn: Callable[[str], bool \| str]` — string-content domain |
| `GateCriteria` (extension target) | `src/superclaude/cli/pipeline/models.py` | 90-105 | `semantic_checks: list[SemanticCheck] \| None = None` at L105 is the shape mirror |
| Gate dispatch (extension target) | `src/superclaude/cli/pipeline/gates.py` | 20-76 | `gate_passed`; semantic_checks loop L66-74 is the append point |
| Pipeline imports (NFR-007 boundary) | `src/superclaude/cli/pipeline/gates.py` | 17 | `from .models import GateCriteria` — NO `roadmap.*` imports allowed |
| `build_certify_step` | `src/superclaude/cli/roadmap/executor.py` | 2060-2105 | Step `id="certify"`, `gate=CERTIFY_GATE`, output `certification-report.md` |
| `_build_steps` (dispatch map) | `src/superclaude/cli/roadmap/executor.py` | 2108-2369 | Produces 13 Step literals — `certify` NOT in this list |
| `CERTIFY_GATE` (extension target) | `src/superclaude/cli/roadmap/gates.py` | 1430-1457 | STRICT tier, 3 semantic_checks today |
| `ALL_GATES` (registry) | `src/superclaude/cli/roadmap/gates.py` | 1532-1547 | 14 entries; `("certify", CERTIFY_GATE)` at L1546 |
| Certify envelope extractor | `src/superclaude/cli/roadmap/envelope.py` | 669-680 | `extract_certify_envelope_fields` already wired to POST_EXTRACTORS L688+ (Phase 7) |
| `roadmap_run_step` (wiring host) | `src/superclaude/cli/roadmap/executor.py` | 1021-1382 | `_roadmap_run_step_impl`; remediate branch L1079-L1080 |

The task preamble line numbers (`executor.py:1899` for build_certify_step,
`models.py:91` for GateCriteria) are BareReview-era stale — these have
shifted to L2060 and L90 respectively at HEAD daa10416 due to R0/R1
inserts. PG8.1 review should not flag the numbers above as drift.

## 3. `CodeAssertion` Dataclass — Canonical Shape

```python
# Lives in: src/superclaude/cli/pipeline/models.py (next to SemanticCheck)

@dataclass
class CodeAssertion:
    """Code-graph predicate applied at gate evaluation time.

    Unlike ``SemanticCheck`` (which inspects the rendered string content of an
    output file), a ``CodeAssertion`` inspects the live code graph -- it may
    parse Python source via ``ast``, import callables, or walk module-level
    constants. The widened ``(PipelineEnvelope, Path) -> Finding | None``
    signature is the BUILD-REQUEST §MVR §2 verbatim contract.

    Return convention:
      None     -> PASS (the assertion held)
      Finding  -> FAIL (assertion violated; ``severity``/``description``/
                  ``location`` populated for downstream gate reporters)
    """

    name: str
    check_fn: Callable[["PipelineEnvelope", Path], "Finding | None"]
    failure_message: str
```

**Signature divergence from `SemanticCheck` (intentional, per §MVR §2):**

| Field | `SemanticCheck.check_fn` | `CodeAssertion.check_fn` |
| --- | --- | --- |
| Input | `(str)` — file content | `(PipelineEnvelope, Path)` — envelope + repo root |
| Output | `bool \| str` — pass/fail or failure detail | `Finding \| None` — typed finding or None |
| Domain | string-content predicates | code-graph predicates |

The widened input gives a CodeAssertion access to envelope state (spec IDs,
accepted deviations, prior step results) and the repository root so it can
locate `src/superclaude/cli/roadmap/executor.py` and AST-parse it without
being coupled to a specific working directory.

**Forward-reference handling.** `PipelineEnvelope` is defined in
`src/superclaude/cli/roadmap/envelope.py` (a `roadmap` module). To preserve
NFR-007 (`pipeline.*` MUST NOT import from `roadmap.*` or `sprint.*`), the
type annotation MUST be a string forward reference (`"PipelineEnvelope"`)
and the import MUST be local to consumers, not module-level in `models.py`.
The Callable annotation `Callable[["PipelineEnvelope", Path], "Finding |
None"]` is valid because string forward refs in PEP 484/604 annotations
don't trigger import resolution at module load. Same treatment for
`Finding` (lives in `cli/roadmap/findings.py`).

`Path` is already imported in `models.py:13` so no new top-level import is
required. The string forward refs are documented in the dataclass
docstring so static type checkers (`mypy`, `pyright`) understand the
intent without requiring `from __future__ import annotations` (which
`models.py:8` already declares — string refs are honored automatically).

## 4. `GateCriteria` Slot Extension

```python
@dataclass
class GateCriteria:
    required_frontmatter_fields: list[str | tuple[str, ...]]
    min_lines: int
    enforcement_tier: Literal["STRICT", "STANDARD", "LIGHT", "EXEMPT"] = "STANDARD"
    semantic_checks: list[SemanticCheck] | None = None
    code_assertions: list[CodeAssertion] | None = None   # NEW (R1.3)
```

**Backward-compat invariants — MUST hold:**

1. **Default is `None`** (not `[]`) — matches the `semantic_checks` shape at
   L105. The dispatch in `gate_passed` checks `if criteria.code_assertions:`
   which treats `None` and `[]` identically (both falsy). Every existing
   `GateCriteria(...)` call site in `cli/roadmap/gates.py` (15+ gates per
   `grep -c "^[A-Z_]* = GateCriteria" gates.py`) keeps working unchanged
   because the new field has a default value.
2. **Position matters.** `code_assertions` MUST appear AFTER
   `semantic_checks` so positional-arg callers (if any) are unaffected. A
   keyword-only `*` boundary is NOT introduced (would break ergonomics).
3. **No mutation of existing fields.** `required_frontmatter_fields`,
   `min_lines`, `enforcement_tier`, `semantic_checks` types and defaults
   are untouched.
4. **No `__init__` override, no `__post_init__`.** The dataclass remains a
   plain frozen-incompatible dataclass per the existing `@dataclass`
   decorator at `models.py:90`.

**Schema versioning note.** This is an additive change. Any pickled
GateCriteria instances from R1.2 deserialize cleanly under R1.3 (older
pickles lack `code_assertions`, dataclass defaults populate `None`). No
pickle-safety hack required.

## 5. Dispatch Integration — `pipeline/gates.py:gate_passed`

The `code_assertions` slot is consumed by extending the existing
`gate_passed(output_file, criteria)` dispatch in
`src/superclaude/cli/pipeline/gates.py:20-76`. The new branch is appended
AFTER the `semantic_checks` loop (L66-74), so a `CodeAssertion` only
evaluates when all preceding STRICT-tier checks (file exists, line count,
frontmatter fields, semantic checks) have already passed. This ordering
matches the §MVR §2 escalating-strictness intent: cheap content checks
first, expensive code-graph checks last.

**Signature change.** `gate_passed` today is
`(output_file: Path, criteria: GateCriteria) -> tuple[bool, str | None]`.
A `CodeAssertion.check_fn` needs `(PipelineEnvelope, Path)`. Two integration
shapes are viable; R1.3 picks shape (B) for the reasons below.

| Shape | Signature | Pros | Cons |
| --- | --- | --- | --- |
| (A) Widen `gate_passed` to take envelope + repo_root | `gate_passed(output_file, criteria, *, envelope=None, repo_root=None)` | One entry point | Breaks 30+ call sites that pass only 2 positional args |
| (B) Add optional kwargs with `None` defaults; new branch is a no-op when missing | `gate_passed(output_file, criteria, *, envelope=None, repo_root=None)` | Backward-compat; old callers unchanged | Two-shape call surface (some callers pass envelope, some don't) |

**Decision: Shape (B), keyword-only optional kwargs with `None` defaults.**

```python
def gate_passed(
    output_file: Path,
    criteria: GateCriteria,
    *,
    envelope: "PipelineEnvelope | None" = None,
    repo_root: Path | None = None,
) -> tuple[bool, str | None]:
    # ... existing tier/exist/min_lines/frontmatter/semantic_checks logic unchanged ...

    # STRICT: code assertions (NEW — R1.3)
    if criteria.code_assertions:
        if envelope is None or repo_root is None:
            # Callers that do not yet pass envelope/repo_root see the gate as
            # if no code_assertions were defined. This is intentional: R1.3
            # ships the slot + CERTIFY_GATE wiring without forcing every
            # gate_passed call site to retrofit envelope plumbing in the
            # same release. Phase 9 (R1.4) and Phase 10 (R1.5) progressively
            # extend call sites; Phase 11 (R1.6) deletes this skip-path.
            return True, None
        for assertion in criteria.code_assertions:
            finding = assertion.check_fn(envelope, repo_root)
            if finding is not None:
                return (
                    False,
                    f"Code assertion '{assertion.name}' failed: "
                    f"{finding.description or assertion.failure_message}",
                )

    return True, None
```

**Why the "envelope-None → skip" branch is acceptable in R1.3.** The R1.3
acceptance criterion is *one* working CodeAssertion (the certify
dispatch-reachability one), invoked from *one* known call site
(`roadmap_run_step`-post-remediate, see §7 below). Other `gate_passed`
callers — resume probing in `_apply_resume` (executor.py:3247), step
re-eval in `_step_needs_rerun` (executor.py:3706), the test corpus — do
NOT need envelope plumbing in R1.3 because they evaluate gates whose
`code_assertions` list is empty/None. The skip-path is a *temporary*
backward-compat shim that R1.6 cleanup MUST delete once all consumers
pass envelope (Acceptance gate #6 + §Contract #5 zero-fail-open invariant).

**NFR-007 (pipeline imports nothing from roadmap/sprint) — Preserved.**
The `pipeline/gates.py` module gains string forward refs for
`PipelineEnvelope` and `Finding` but no actual module-level imports. The
type annotations are PEP 563 string refs honored by
`from __future__ import annotations` (already declared at the top of
`gates.py:12`). At runtime `gate_passed` receives a `PipelineEnvelope`
duck-typed object — it only reads attributes (`spec_ids`, `findings`,
etc.); no isinstance checks against the roadmap-side class. The
`pipeline → roadmap` arrow remains zero at module load.

## 6. First `CodeAssertion` — `assert_step_reachable` for `CERTIFY_GATE`

The first CodeAssertion realizes BUILD-REQUEST §MVR §2 verbatim: "Wire
`build_certify_step()` ... as the final step; CodeAssertion guarantees no
future step ships unwired." It also realizes §Contract #2 dispatch-
reachability as a CI-testable invariant.

### 6.1 Module location

```
src/superclaude/cli/roadmap/code_assertions.py   # NEW (Step 8.3)
```

Lives under `roadmap/` (not `pipeline/`) because:

- It imports the roadmap `PipelineEnvelope` and `Finding` types (concrete,
  not duck-typed) — keeps NFR-007 boundary clean (pipeline doesn't depend
  on roadmap; roadmap depends on pipeline).
- The first CodeAssertion is roadmap-specific (it ASTs `cli/roadmap/
  executor.py`); future generic ones can move to `pipeline/code_assertions.py`
  if and when they emerge.

### 6.2 `assert_step_reachable` — implementation contract

```python
# src/superclaude/cli/roadmap/code_assertions.py

import ast
from pathlib import Path

from superclaude.cli.roadmap.envelope import PipelineEnvelope
from superclaude.cli.roadmap.findings import Finding


def assert_step_reachable(
    envelope: PipelineEnvelope,
    repo_root: Path,
) -> Finding | None:
    """Verify `certify` step is reachable from the production dispatch map.

    Walks the AST of ``executor.py``, locates the ``_build_steps`` function,
    enumerates every ``Step(id=<literal>, ...)`` constructor argument value,
    and asserts ``"certify"`` is among them (the literal-string id at
    ``executor.py:build_certify_step`` L2098).

    The walker is intentionally conservative -- only Constant string literals
    in keyword ``id=`` arguments to ``Step`` calls are counted. Dynamic ids
    like ``id=f"generate-{agent_a.id}"`` are normalized to their string
    prefix (``"generate-"``); ``"certify"`` is a static literal so this
    edge case never affects it.

    Returns
    -------
    Finding | None
        ``None`` on PASS (certify is in the dispatch map).
        A HIGH-severity ``Finding`` on FAIL with location pointing at
        ``executor.py:_build_steps`` and remediation guidance referencing
        master:§Flaw 1 / Contract #2.
    """
    executor_path = repo_root / "src" / "superclaude" / "cli" / "roadmap" / "executor.py"
    if not executor_path.is_file():
        return Finding(
            id="CA-DISPATCH-001",
            severity="HIGH",
            description=(
                f"assert_step_reachable: executor.py not found at "
                f"{executor_path} (repo_root resolution failed)"
            ),
            location=str(executor_path),
            fix_guidance="Verify repo_root passed to gate_passed is correct.",
        )

    tree = ast.parse(executor_path.read_text(encoding="utf-8"))
    step_ids = _extract_step_ids_from_build_steps(tree)

    if "certify" not in step_ids:
        return Finding(
            id="CA-DISPATCH-002",
            severity="HIGH",
            description=(
                "CERTIFY_GATE dispatch-reachability: step 'certify' not found "
                "in _build_steps dispatch map (Contract #2 / master:§Flaw 1). "
                f"Observed step ids: {sorted(step_ids)!r}. "
                "build_certify_step() defines the step but no production "
                "caller invokes it."
            ),
            location=f"{executor_path}:_build_steps",
            fix_guidance=(
                "Wire build_certify_step() into the production dispatch path "
                "(roadmap_run_step post-remediate, see executor.py L2366 "
                "comment) and re-run the gate."
            ),
        )

    return None


def _extract_step_ids_from_build_steps(tree: ast.Module) -> set[str]:
    """Return the set of literal string ``id=`` values used in Step(...)
    constructor calls inside the ``_build_steps`` function body.

    Two-pass walk:
      1. Locate the FunctionDef named ``_build_steps``.
      2. Walk its body; collect every ``Call`` whose ``.func`` is
         ``Name("Step")`` and whose keyword ``id=`` is a ``Constant`` str.

    Dynamic ids (f-strings, name lookups) are normalized to their static
    prefix when feasible; for ``f"generate-{agent_a.id}"`` we record
    ``"generate-"``. For ``id=some_var`` we record the Name node id with a
    ``<dynamic:>`` prefix so the test can see them but does not match
    static lookups.
    """
    ids: set[str] = set()
    for node in ast.walk(tree):
        if not (isinstance(node, ast.FunctionDef) and node.name == "_build_steps"):
            continue
        for inner in ast.walk(node):
            if not (
                isinstance(inner, ast.Call)
                and isinstance(inner.func, ast.Name)
                and inner.func.id == "Step"
            ):
                continue
            for kw in inner.keywords:
                if kw.arg != "id":
                    continue
                value = kw.value
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    ids.add(value.value)
                elif isinstance(value, ast.JoinedStr):
                    prefix_parts: list[str] = []
                    for part in value.values:
                        if isinstance(part, ast.Constant) and isinstance(part.value, str):
                            prefix_parts.append(part.value)
                        else:
                            break
                    if prefix_parts:
                        ids.add("".join(prefix_parts))
    return ids
```

**Design notes.**

- **No external dependencies.** `ast` is stdlib; `Path` already in scope.
  Satisfies the Step 8.1 spec "the AST walker uses Python's `ast` module
  (no external dependencies)".
- **Idempotent and side-effect-free.** Reads the file, parses once, walks
  the tree. No writes, no imports of the module under test (avoids the
  meta-recursion trap where importing `executor.py` to inspect it
  re-runs decorators).
- **Robust to f-string ids.** The two parallel `generate-A`/`generate-B`
  Step constructors at `executor.py:2192`/`L2210` use
  `id=f"generate-{agent_a.id}"`. The walker records the literal prefix
  `"generate-"` for these. The certify assertion looks for the literal
  `"certify"` which is a `Constant` string at L2098, so f-string handling
  does not affect the certify case but is documented so future code
  assertions (R1.5) inherit the convention.
- **No false PASS via overload.** Bare `Step(...)` calls outside
  `_build_steps` (e.g., the certify Step constructor at
  `build_certify_step` L2097) are intentionally NOT counted. The walker
  scopes to the `_build_steps` function body, so a Step defined in
  `build_certify_step` does NOT auto-satisfy the assertion just because
  it exists in the file. This is the load-bearing semantic that
  distinguishes "step defined" (L2098) from "step reachable" (L2108+
  dispatch map) and is what makes the assertion catch master:§Flaw 1.

### 6.3 Wiring into `CERTIFY_GATE`

```python
# src/superclaude/cli/roadmap/gates.py — CERTIFY_GATE at L1430-1457

from superclaude.cli.pipeline.models import CodeAssertion, GateCriteria, SemanticCheck
from superclaude.cli.roadmap.code_assertions import assert_step_reachable

CERTIFY_GATE = GateCriteria(
    required_frontmatter_fields=[...],   # unchanged
    min_lines=15,                         # unchanged
    enforcement_tier="STRICT",            # unchanged
    semantic_checks=[                     # unchanged (3 existing)
        SemanticCheck(name="frontmatter_values_non_empty", ...),
        SemanticCheck(name="per_finding_table_present", ...),
        SemanticCheck(name="certified_is_true", ...),
    ],
    code_assertions=[                     # NEW (R1.3)
        CodeAssertion(
            name="step_reachable",
            check_fn=assert_step_reachable,
            failure_message=(
                "Contract #2: certify step must be reachable from the "
                "production _build_steps dispatch map "
                "(master:§Flaw 1 evidence chain)."
            ),
        ),
    ],
)
```

The other 13 entries in `ALL_GATES` (L1532-1547) are unchanged in R1.3 —
they continue to use `semantic_checks` only with `code_assertions=None`
defaulted. R1.5's `verify-implementation` terminal step will introduce
the second batch of CodeAssertions (FR→AST link), at which point Step 8.4's
`test_all_gates_have_assertions` becomes more interesting; for R1.3 it
documents the boundary.

## 7. Step-Count Budget Resolution — Wiring `build_certify_step`

### 7.1 Problem statement

Acceptance gate #6 (Task L102): "Final pipeline step count ≤ current (14)."

Current state at HEAD daa10416:

- `_build_steps` (executor.py:2108-2369) produces 13 Step constructions:
  extract, generate-A, generate-B, diff, debate, score, merge,
  anti-instinct, test-strategy, spec-fidelity, wiring-verification,
  deviation-analysis, remediate.
- `ALL_GATES` (gates.py:1532-1547) lists 14: the above 13 plus
  `("certify", CERTIFY_GATE)`.
- `build_certify_step` (executor.py:2060) is defined but
  `grep -rn build_certify_step src/ tests/` returns ZERO production
  callers — only `tests/roadmap/test_pipeline_integration.py:565`
  invokes it inside a unit test.
- L2366 comment: "Step 12 (certify) constructed dynamically by
  roadmap_run_step after remediate" — declares intent but is NOT
  implemented in production code. This is the master:§Flaw 1 / Contract
  #2 evidence at its purest: a step that exists, has a gate registered,
  yet ships unwired.

If Step 8.3 wires `build_certify_step` as a NEW entry inside the
`_build_steps` return list, the count grows to 14 (treating
generate-A/generate-B as one parallel slot) or 15 (treating them as
separate slots, which `ALL_GATES` does). Either way the new entry pushes
the structural budget closer to or past 14. R1.5 will also add
`verify-implementation`, which would push the count to 15 or 16 — over
budget.

### 7.2 Resolution — Option (a): dynamic post-remediate construction

**Decision: Wire `build_certify_step` inside `roadmap_run_step` (or its
sibling pipeline driver) post-remediate. `_build_steps` is NOT
modified. Step count stays at 14 (per `ALL_GATES`).**

Rationale:

1. **Matches existing intent.** The L2366 comment ("Step 12 (certify)
   constructed dynamically by roadmap_run_step after remediate")
   explicitly declares this design — it is implementation that lags the
   declaration, not a design change.
2. **Matches existing precedent.** `roadmap_run_step` already special-
   cases two step ids that are NOT plain LLM-prompt steps:
   `deviation-analysis` (L1075-1076) and `remediate` (L1079-1080) and
   `wiring-verification` (L1085-1102). Adding a fourth branch for
   `certify` is structurally identical to those three.
3. **Doesn't grow `_build_steps`.** Step count remains ≤14 throughout
   R1.3, R1.4 (which only rewrites *how* steps emit content, not the
   step set), R1.5 (which then absorbs `wiring-verification` per R1.6
   §Cleanup to make room for `verify-implementation`).
4. **Preserves PRESERVED invariants.** `commands.py` (CLI surface,
   PRESERVE), `structural_checkers.py` (v3.05 layer, PRESERVE), and
   `convergence.py` (public API, PRESERVE) are untouched.
5. **Minimal risk.** R1.3 ships the substrate (slot + first assertion
   + dispatch wiring) without touching the step set. R1.5 owns the step
   set evolution. Smallest-blast-radius staging.

### 7.3 Where the dynamic construction actually lands (Step 8.3 detail)

`roadmap_run_step` (`_roadmap_run_step_impl` at L1021) is per-step
dispatch — it receives ONE Step at a time. A "post-remediate" hook
properly lives in the pipeline DRIVER (`execute_roadmap` at L3146 /
`execute_pipeline` in the generic pipeline executor), not inside
`roadmap_run_step` itself.

Two viable wiring points; Step 8.3 picks (B):

| Point | Location | Pros | Cons |
| --- | --- | --- | --- |
| (A) Inside `roadmap_run_step` post-remediate branch | `executor.py:1079-1080` extension | Co-located with other step-id branches | Each step call would re-test "am I certify?" — couples per-step dispatch to pipeline-level sequencing |
| (B) After `execute_pipeline` returns, before `_save_state` | `execute_roadmap` at `executor.py:~3294` | Pipeline-level placement matches "terminal step" semantics; no per-step coupling | Slightly more code in `execute_roadmap` |

**Step 8.3 implementation sketch (option B):**

```python
# In execute_roadmap, after execute_pipeline returns (~L3286-L3292):

results = execute_pipeline(
    steps=steps,
    config=config,
    run_step=roadmap_run_step,
    on_step_start=_print_step_start,
    on_step_complete=_print_step_complete,
)

# R1.3: dynamically construct + execute the certify step after remediate
# passed. Counts against ALL_GATES (14), NOT against _build_steps.
remediate_result = next(
    (r for r in results if r.step and r.step.id == "remediate"),
    None,
)
if remediate_result is not None and remediate_result.status == StepStatus.PASS:
    certify_step = build_certify_step(
        config,
        findings=_collect_findings_from_results(results),
        context_sections=_extract_context_sections(results),
        remediation_summary=_remediation_summary(results),
    )
    certify_result = roadmap_run_step(certify_step, config)
    results.append(certify_result)

_save_state(config, results)
```

Helper functions (`_collect_findings_from_results`,
`_extract_context_sections`, `_remediation_summary`) extract from the
existing `results` list of `StepResult` objects + the envelope sidecar.
These are pure Python helpers; their detailed signatures land in Step 8.3.

**Why this stays under budget.** `_build_steps` continues to return 13
Steps (or 14 counting the parallel generate pair). The certify Step is
constructed at runtime exactly once per pipeline invocation, appended to
`results` after the fact. The user-visible pipeline-step count (which is
what Acceptance gate #6 measures via `ALL_GATES`) stays at 14.

### 7.4 Test budget assertion (Step 8.4)

`tests/roadmap/test_dispatch_reachability.py::test_step_count_within_budget`
asserts `len(ALL_GATES) <= 14` so any future addition that violates the
budget fails CI. This complements `test_certify_step_reachable` which
asserts the certify CodeAssertion actually catches the unwired case.

## 8. Dispatch-Reachability Coverage Caveats

Per sc:reflect UC-1 M3, the dispatch-reachability AST walker is
intentionally scoped to ONE entry-point shape in R1.3:

**In R1.3 scope:** `Step(id=<literal>)` constructors inside
`executor.py:_build_steps`.

**Deferred (per M3):** Click commands (`cli/roadmap/commands.py`) and
skill invocations (`/sc:roadmap`, `/sc:tasklist`) as production entry
points. The walker SHOULD be extensible to those shapes in R1.5+, but
R1.3 ships the proof-of-concept for the dispatch-map case only. M3 is
re-surfaced in Phase Findings during Step 8.3 so PG8.1 doesn't flag the
omission as drift.

## 9. Acceptance Criteria for Step 8.1 Design Doc Completion

The Step 8.1 spec at task L508 requires:

1. ✅ `CodeAssertion` dataclass shape `(name: str, check_fn: Callable[[PipelineEnvelope, Path], Finding | None], failure_message: str)` — defined in §3.
2. ✅ How `GateCriteria.code_assertions` wires into `pipeline/gates.py:gate_passed` dispatch — specified in §5 with the NEW branch alongside `semantic_checks`.
3. ✅ First `CodeAssertion` for `CERTIFY_GATE` that walks AST to confirm `step.id == "certify"` appears in `_build_steps` dispatch map — specified in §6.2 with `assert_step_reachable`.
4. ✅ Backward compatibility — `code_assertions=None` defaults so existing gates unchanged — specified in §4.
5. ✅ Design matches §MVR §2 verbatim — §3 dataclass shape mirrors L107-112 of BUILD-REQUEST §MVR §2.
6. ✅ AST walker uses Python's `ast` module (no external dependencies) — §6.2 implementation uses stdlib only.
7. ✅ Design preserves all existing GateCriteria consumers (no API break) — §4 invariants + §5 keyword-only optional kwargs.
8. ✅ Step-count budget choice documented — §7 selects option (a) dynamic post-remediate construction inside `execute_roadmap`.

## 10. Downstream Step Dependencies

- **Step 8.2** (models.py extension) reads §3, §4 and implements the
  dataclass + slot exactly per the shapes above.
- **Step 8.3** (CodeAssertion impl + CERTIFY_GATE wiring + dispatch fix)
  reads §5, §6, §7 and implements:
  - `src/superclaude/cli/roadmap/code_assertions.py` per §6.2
  - `gates.py:CERTIFY_GATE` extension per §6.3
  - `pipeline/gates.py:gate_passed` kwargs extension per §5
  - `executor.py:execute_roadmap` post-remediate certify construction per §7.3
- **Step 8.4** (test_dispatch_reachability.py) reads §6, §7 and tests:
  - `test_certify_step_reachable` — assert PASS for current `_build_steps`
  - `test_unwired_step_caught` — synthetic envelope expecting a missing step → HIGH Finding
  - `test_all_gates_have_assertions` — walks `ALL_GATES`, asserts each gate has `semantic_checks` OR `code_assertions` (R1.3 expects only CERTIFY_GATE has the new slot populated; rest pass via semantic_checks)
  - `test_codeassertion_signature_invariant` — introspect `CodeAssertion.check_fn` annotations
  - `test_step_count_within_budget` — `len(ALL_GATES) <= 14` (R1.3 substrate test for §7.4)
- **PG8.1** (rf-qa task-integrity) verifies all of the above against the
  acceptance criteria in §9 + the task's PG8.1 verdict-criteria list at
  L526.

## 11. Open Questions & Deferrals

1. **OQ-A** — Should `gate_passed`'s `envelope=None` skip-path log a
   WARNING when a gate with `code_assertions` is evaluated without an
   envelope? Decision: **No** for R1.3 (silent skip). R1.6 deletes the
   skip-path entirely; warning would be noise during the transition.
2. **OQ-B** — Should `assert_step_reachable` cache the parsed AST across
   gate invocations? Decision: **No** for R1.3 (parse-per-call). The
   certify gate is evaluated once per pipeline run; the parse cost is
   ~10ms. Caching adds invalidation complexity for negligible savings.
3. **OQ-C** — Should the `_extract_step_ids_from_build_steps` walker
   live in `code_assertions.py` (module-private) or in a shared utility?
   Decision: **module-private for R1.3**, promote to a shared utility
   in R1.5 when `verify-implementation` needs a similar AST helper.
4. **Deferred — M3 (sc:reflect UC-1):** Walker coverage for Click
   commands and skill invocations as production entry points. R1.3
   scope is `_build_steps` only; M3 is logged to Phase Findings during
   Step 8.3 for PG8.1 awareness.

## 12. Status

DESIGN COMPLETE — ready for Step 8.2 (models.py extension) to consume.
