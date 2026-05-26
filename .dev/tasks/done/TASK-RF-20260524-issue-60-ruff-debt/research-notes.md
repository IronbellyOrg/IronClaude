# Research Notes: GitHub Issue #60 — Ruff Debt Cleanup

**Date:** 2026-05-24
**Scenario:** A (Explicit — Issue #60 + BUILD_REQUEST inline are highly specific)
**Depth Tier:** Standard (scope spans multiple rule categories but is well-bounded tech debt)
**Track Count:** 1

---

## EXISTING_FILES

**Configuration files:**
- `pyproject.toml` lines ~50-90: `[tool.ruff]` block with `select = ["E", "F", "I", "N", "W", "TID"]`, `ignore = ["E501", "N818"]`, `exclude = ["docs/"]`, `extend-exclude = ["tests/audit/fixtures/syntax_error.py"]`, and banned-api `anthropic` entries (FR-G1 protection — DO NOT remove).
- `Makefile` lines for `lint:` target: `uv run ruff check .` (no `--config` override; no path scoping).
- `.pre-commit-config.yaml` exists; uses `detect-secrets`, `pre-commit-hooks` repos. Ruff is NOT currently a pre-commit hook (Makefile only).

**Reference data (frozen snapshot from Issue #60 filing, 2026-05-19):**
- `.dev/tasks/done/TASK-RF-track-2-20260518-231708/phase-outputs/test-results/ruff-summary.md` — original 35-error breakdown
- `.dev/tasks/done/TASK-RF-track-2-20260518-231708/phase-outputs/test-results/ruff-output.txt` — raw ruff output

**Current state (verified 2026-05-24 by `uv run ruff check . --output-format=concise`):**
- Total: **442 errors** (vs 35 at Issue filing). Discrepancy is due to:
  - New cliEval CLI module (PR #66) added ~125 errors in `src/superclaude/cli/eval/` and `tests/cli/eval/`
  - `.dev/releases/` archived release artifacts: 182 errors (NEVER linted before; should be excluded)
  - `.dev/eval-workspaces/` and `.dev/research/`: 32 errors (eval outputs, should be excluded)
  - `scripts/` analysis tools: 5 errors

**Full current breakdown (verified via `awk -F': ' '{print $NF}' | awk '{print $1}'`):**

| Rule | Count | Description |
|------|------:|-------------|
| TID252 | 101 | Prefer absolute imports over relative imports (all in src/superclaude/) |
| I001 | 94 | Import block un-sorted or un-formatted |
| N802 | 81 | Function name should be lowercase |
| F401 | 49 | Imported but unused |
| E402 | 38 | Module-level import not at top of file |
| F541 | 29 | f-string without placeholders |
| F821 | 18 | Undefined name |
| N801 | 9 | Class name should use CapWords |
| F841 | 6 | Local variable assigned but never used |
| N999 | 4 | Invalid module name |
| E741 | 3 | Ambiguous variable name (e.g., `l`) |
| E731 | 3 | Lambda expression assigned (use def) |
| N806 | 2 | Variable in function should be lowercase |
| **Total** | **442** | |

**Top contributing directories (verified via `awk -F'/' '{print $1"/"$2}'`):**

| Directory | Errors | Notes |
|-----------|-------:|-------|
| `.dev/releases/` | 182 | Archived release artifacts — should be excluded |
| `src/superclaude/` | 125 | Real code; needs proper fixes (TID252=101 + E402=21 + F821=3) |
| `tests/cli/` | 60 | New cliEval test suite (mostly I001=58) |
| `.dev/eval-workspaces/` | 29 | Eval scratch outputs — should be excluded |
| `tests/audit/` | 13 | Pre-existing Issue #60 scope (N801, N999, F841) |
| `tests/sprint/` | 11 | Pre-existing Issue #60 scope (E402, E731, F821) |
| `tests/pipeline/` | 7 | Pre-existing Issue #60 scope (E402) |
| `scripts/` | 5 | Analysis tools (F401, E741, I001) |
| `tests/roadmap/` | 3 | Pre-existing Issue #60 scope (E402) |
| `.dev/research/` | 3 | Research scratch outputs — should be excluded |
| `tests/cli_portify/` | 1 | Pre-existing Issue #60 scope (E402) |
| `.dev/eval-roadmap/` | 1 | Eval outputs — should be excluded |

## PATTERNS_AND_CONVENTIONS

**From `pyproject.toml`:**
- `line-length = 88`, `target-version = "py310"`
- Selected rule families: `E` (pycodestyle errors), `F` (pyflakes), `I` (isort), `N` (pep8-naming), `W` (pycodestyle warnings), `TID` (tidy-imports)
- Intentional ignores: `E501` (line-length handled by black), `N818` (existing exception classes without Error suffix are part of public API)
- Banned-api: `anthropic` imports forbidden under FR-G1 (cliEval harness must use subprocess) — **DO NOT modify or weaken**

**From `.dev/README.md` and project convention (per CLAUDE.md):**
- `.dev/` is for non-distributable artifacts (eval outputs, release archives, research notes, sprint state)
- `docs/` is already excluded from ruff
- Same logical reasoning applies to `.dev/`: it's NOT shippable code

**E402 fix patterns (from Issue #60 ruff-output.txt analysis):**
- Most E402 in `tests/sprint/diagnostic/test_*.py` are because `pytestmark = [...]` appears before imports. Fix: move pytestmark AFTER imports, OR add `# noqa: E402` if pytestmark placement is intentional.
- `tests/pipeline/test_full_flow.py:343,345` and `tests/cli_portify/test_failures.py:377` likely have late imports inside test bodies that got hoisted.

**N801 fix pattern (test class names):**
- `TestInvariant1_SelfContainedItem`, `TestPartA_OneLowFindingFailsGate` etc. — these use underscore-separated test phase identifiers intentionally. **Safe to `# noqa: N801`** with rationale comment, since renaming would lose semantic meaning.

**N999 (invalid module name):**
- `test_invariant_preservation_NFR_6_through_10.py`, `test_monotonicity_halt_F_5_5_5.py`, `test_sequencing_PR06_before_PR04.py`, `v2.09-adversarial-v2-tests` — these contain capital letters and/or dots that ruff rejects. Test files use these names for cross-reference clarity with FR/INV/PR identifiers. **Two paths**: (a) rename to lowercase (breaks cross-references) OR (b) add `# noqa: N999` at the top of each file with rationale. **(b) is preferred** per Issue #60 scope guidance ("rare — F821 should never be # noqa'd").

**E731 (lambda):**
- `tests/sprint/diagnostic/test_instrumentation.py:45` — rewrite `foo = lambda x: ...` as `def foo(x): ...`. Trivial.

**F841 (unused local var):**
- `tests/audit/test_evidence_bound_tb_add_8.py:97` — `current_item_line` assigned but never used. Either delete the assignment or rename to `_current_item_line` to mark intentional.

**F821 (undefined name):**
- `tests/sprint/test_preflight.py:483, 914` — `"SprintConfig"` used in forward references. The actual import happens inside the function body. Fix: add `from __future__ import annotations` at top OR import at module level.
- `src/superclaude/.../*.py:3 errors` — REAL bugs; cannot `# noqa` per Issue #60 ("F821 should never be # noqa'd"). Must investigate and fix.

**TID252 (relative imports):**
- 101 errors all in src/superclaude/. Pattern: `from . import foo` or `from .module import bar`. Fix: rewrite as `from superclaude.module import foo` (absolute). `ruff check --fix` does NOT auto-fix TID252; manual rewriting required. **Significant scope** — but mechanical and safe.

## GAPS_AND_QUESTIONS

**RESOLVED during scope discovery:**
- ~~How many errors actually exist?~~ → 442 (current) vs 35 (at filing).
- ~~Why the growth?~~ → cliEval feature landed (PR #66) + `.dev/` paths never excluded.
- ~~Are F821 in src/ real bugs?~~ → Yes, 3 errors in src/superclaude need investigation.

**GENUINE UNKNOWNS (need investigation during execution):**
- The exact location of the 3 `F821` errors in `src/superclaude/` — need to read each one before deciding fix vs noqa.
- The exact location of `N802` (81) and `F541` (29) errors — likely concentrated in cliEval, but per-instance review needed for N802 (function naming).
- Whether `N802` violations are in test methods (where camelCase is sometimes deliberate) or in production code (where snake_case must be enforced).
- Whether `I001` (94) is safe to fix via `ruff --fix` everywhere or whether some manual review is warranted.

## RECOMMENDED_OUTPUTS

**Deliverables when task completes:**
1. Updated `pyproject.toml` with `.dev/` and `.dev/releases/`, `.dev/eval-workspaces/`, etc. in `extend-exclude`
2. All ruff errors in `src/superclaude/`, `tests/`, `scripts/` reduced to zero
3. Per-file fixes: imports moved/sorted, lambdas rewritten, unused vars removed, undefined names fixed, class names noqa'd with rationale
4. `make lint` returns exit 0
5. `uv run pytest` baseline preserved (record baseline pre-task, verify post-task)
6. PR opened against `master` branch closing Issue #60

**Branch:** `fix/issue-60-ruff-debt` off `master` (NOT off `feat/agents-tavily`)

## SUGGESTED_PHASES

Use **Template 02 (complex multi-phase)**. The task needs discovery before remediation (per-file inspection), parallel per-rule fix execution, regression sweep, and PR creation.

**Phase 1: Setup & Baseline (P1)**
- Verify branch state (off master, not feat/agents-tavily)
- Create phase-outputs directories
- Capture pre-fix baselines: ruff output, pytest output
- Discover exact locations of all 442 errors per rule

**Phase 2: Configuration Fix — Exclude .dev/ (P2)**
- Add `.dev/` to `pyproject.toml` extend-exclude
- Verify error count drops from 442 to ~226 (removing 216 .dev/ errors)
- Verify no `.dev/` errors remain in ruff output

**Phase 3: Auto-fixable Rules — I001 + F401 + F541 (P3)**
- Run `uv run ruff check . --fix` (handles I001, F401, F541 safely)
- Re-verify ruff output; commit auto-fixes separately for clean PR history
- Re-run pytest to ensure import sorting did not break anything

**Phase 4: Manual Fixes — E402 + E731 + F841 + E741 + N806 (P4)**
- Per-file E402 remediation: move imports to top OR add justified noqa
- Per-file E731: rewrite lambdas as def
- Per-file F841: remove or underscore-prefix unused vars
- Per-file E741: rename ambiguous variables
- Per-file N806: lowercase function-local variables

**Phase 5: Manual Fixes — N801 + N802 + N999 (P5)**
- Per-file N801: noqa with rationale for test classes; rename otherwise
- Per-file N802: review each — production code rename, test methods may noqa
- Per-file N999: noqa with rationale for FR/INV/PR cross-reference filenames

**Phase 6: F821 Investigation & Fix (P6)**
- For each F821 in src/superclaude/: read context, identify root cause, fix properly (NEVER noqa per Issue #60)
- For F821 in tests/sprint/test_preflight.py: add `from __future__ import annotations` OR move imports

**Phase 7: TID252 — Relative-to-Absolute Imports (P7)**
- 101 instances in src/superclaude/ requiring manual rewrite
- Run tests after each module's conversion to detect breakage
- Most are simple `from .module` → `from superclaude.full.path.module`

**Phase 8: Regression Sweep & Validation (P8)**
- Final `uv run ruff check .` → must exit 0
- Final `make lint` → must exit 0
- Final `uv run pytest` → must match baseline (no new failures)
- QA gate (rf-qa) verifying all phase outputs

**Phase 9: PR Creation & Issue Closure (P9)**
- Create PR against master with summary, evidence, Issue #60 closure
- Mark task Done

## TEMPLATE_NOTES

**Template selection: 02 (Complex Task)** — confirmed per BUILD_REQUEST. Justification:
- Discovery before building (per-rule per-file investigation)
- Conditional flows (pytest regression, fix vs noqa decisions)
- Phase gates (after each rule category, re-verify ruff state)
- Final QA validation phase

**QA Gate strategy: PER_PHASE** for major phases (3, 4, 5, 6, 7) since each rule category is independent. FINAL_ONLY QA gate before PR creation.

**Tier: Standard.** Scope is medium (442 errors across 6 rule families + config change). Not Quick (>5 files; multiple subsystems) and not Deep (well-bounded tech debt, no novel architecture).

**Key MDTM rules to honor:**
- B2 self-contained items (every item has context + action + output + verification + completion gate + error-handling clause)
- A3 granularity: per-file items where possible (avoid "fix all E402" in one item)
- L1-L6 handoff patterns: use L3 (test/execute) for ruff/pytest runs, L5 (conditional) for fix-vs-noqa branches, L6 (aggregation) for final regression sweep
- A1: TaskCreate spawning agent items use Agent tool with bypassPermissions

## AMBIGUITIES_FOR_USER

None — intent is clear from Issue #60 + BUILD_REQUEST. The "discrepancy" between the original 35 errors and current 442 is fully explained by:
1. New code landings (cliEval PR #66 = ~125 errors)
2. `.dev/` paths never being excluded from ruff (216 errors)
3. Scripts/ tools never linted (5 errors)
4. ~78 additional errors from other minor PRs since 2026-05-19

The BUILD_REQUEST's instruction "DO preserve test semantics — any rename / refactor must keep tests collecting + passing" combined with "DO NOT bypass via `# noqa` blanket suppressions unless the rule violation is intentional" gives clear guidance for fix-vs-noqa decisions per-instance.

**Implicit user decision (documented as task assumption, not asked):** `.dev/` will be added to ruff `extend-exclude`. Rationale: `.dev/` already gitignored partially (`.dev/eval-runs/`, `.dev/sprint-state/`); the entire directory is non-distributable artifact storage per CLAUDE.md ("docs/generated/ is a roadmap pipeline artifact directory, not a general output sink" — same logic applies to all .dev/ artifacts). Excluding `.dev/` from ruff aligns with existing `docs/` exclusion. If the user disagrees, they can remove this change before PR merge.
