MEASURED_NET_LINES: 1311
FINAL_GATE_AGENT_COUNT: 8

# Final Change-Set Manifest (Step PC.3)

Measured vs audit base `46a787dac39c75753a6da4ca483dc6b5d2581bb0`.
- Tracked diff (`git diff --stat 46a787da -- src/superclaude tests`): 420 insertions + 4 deletions = 424 lines.
- Untracked new FX files (`wc -l`): 887 lines.
- **TOTAL net-line delta = 1311** → I19 band 500–1500 → **8 agents (4 rf-qa + 4 rf-qa-qualitative)**.
  (Excludes the task-bookkeeping dir `.dev/tasks/TASK-RF-qa-reflect-harden-.../` and the
  `.dev/analysis/qa-reflect-blindspot-pr209/pipeline/` research/plan artifacts — process outputs, not the FX
  deliverable under review; and the gitignored `.claude/` sync-dev mirrors.)

## Files grouped by FX

### FX3 (field-resolution AST test) — deterministic P0
- `tests/pr_submit/test_setup_questions_resolution.py` (NEW) — AST introspection; 4 assertions + Constant-arg guard.

### FX5 (gate-helper coverage collector) — deterministic P0
- `tests/pr_submit/test_gate_helper_differentials.py` (NEW) — 11 helpers × negative+differential (22 tests) + `HELPER_TEST_MAP`.
- `tests/pr_submit/test_gate_helper_coverage.py` (NEW) — parametrized per-helper coverage test.
- `tests/pr_submit/conftest.py` (+173) — `GATE_LOAD_BEARING_HELPERS`, `GATE_HELPER_DEF_PATTERN`, `pytest_generate_tests`, existence/coverage/drift-alarm, `assert_gate_helper_coverage` fixture. (5 existing fixtures byte-preserved.)

### FX7 (additive honest-accounting) — deterministic P0
- `src/superclaude/cli/reflect/ensemble.py` (+30/-1) — `reviewers_requested` kwarg + threading; `reviewers_verified`; visible benign `reviewer-shortfall` token; `*_verified` keys. Skip reason unchanged.
- `src/superclaude/cli/reflect/models.py` (+8) — 3 defaulted `*_verified` fields on `ReflectResult`.
- `src/superclaude/cli/reflect/contract.py` (+6) — `_make_result` populates the 3 fields via `c.get`.
- `src/superclaude/cli/reflect/runner.py` (+10) — append-only surfacing to `_build_reflect_post_value` + `write_sidecar`.
- `tests/cli/reflect/test_ensemble_unit.py` (+72), `test_verdict_mapping.py` (+40), `test_writeback.py` (+35) — 6 new FX7 tests.
- `tests/cli/reflect/fixtures/degraded_reviewer_shortfall.yaml`, `vacuous_no_verify.yaml` (NEW).

### FX2 (scoped code cross-symbol lens) — P1
- `src/superclaude/agents/rf-qa-qualitative.md` (+4/-) — item 5 augmented with the cross-symbol input-shape invariant (AX-2, cross-module) + Adaptation row.

### FX1 (advisory-only no-spec correctness slot) — P1
- `src/superclaude/agents/reflect-reviewer.md` (+20/-1) — Role advisory note + `no-spec-correctness` persona_lens + `## Correctness gaps` sub-section. `tools:` line unchanged.
- `src/superclaude/skills/sc-reflect-protocol/refs/deviation-taxonomy.md` (+26) — `## Correctness-gap` advisory parallel dimension.

## Excluded-surface confirmation (NO change touched any of these)
- `contract.py:_VERIFICATION_SKIP_EXEMPTIONS` — BYTE-UNCHANGED (Gate B verified).
- `contract.py:_DEGRADED_COMPONENTS_HALT_SET` — BYTE-UNCHANGED (Gate B verified; the deferred shortfall-degrade would edit this).
- A 5th deviation class — NONE (Gate C verified; taxonomy stays 4 classes).
- The "#### Checklist (15 items)" count — UNCHANGED (Gate C verified).
- The reflect-reviewer `tools:` frontmatter line — UNCHANGED (Gate C verified).
- FX4 / FX6 / FX8 / FX9 — NOT shipped (documented non-goals).

## Scaling directive → PC.4
`FINAL_GATE_AGENT_COUNT: 8` → spawn the 6 baseline lens agents PLUS 1 additional `rf-qa`
(`additive-safety-deep-diff`) and 1 additional `rf-qa-qualitative` (`cross-fix-interaction`).
