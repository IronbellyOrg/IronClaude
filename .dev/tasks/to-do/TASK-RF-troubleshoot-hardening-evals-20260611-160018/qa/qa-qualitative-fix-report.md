# QA Report — task-qualitative (consolidated-fix)

**Topic:** Differential Backtest/Eval Harness (E1-E5 OLD=MISS vs NEW=CATCH)
**Date:** 2026-06-11
**Phase:** task-qualitative / consolidated-fix (MDTM I20 single serialized fix agent)
**Fix cycle:** 1
**fix_authorization:** true
**Team context:** NONE (escalation override — no SendMessage/TaskCreate/TaskUpdate/TaskList used)

---

## Overall Verdict: FIXES APPLIED (all 5)

All 5 consolidated findings applied IN-PLACE to the task file via surgical Edit. All three
post-fix grep constraints pass (zero `evalIdString`, zero `{UPPER}` placeholders, zero
parent-sha-with-caret). All preserved-clean content verified intact.

---

## Pre-fix verification (claims checked against source before editing)

| Claim | Tool evidence | Result |
|-------|---------------|--------|
| `summary.schema.json` has NO `evalIdString` $def / no escape-id pattern | `grep -n` → only `evalStatus` enum at L73, `$ref #/$defs/evalStatus` at L171 | CONFIRMED — FIX-1 valid |
| E1 `_build_file_args` is class-bound (`PrdClaudeProcess`) | `git show 94d5baa0:.../process.py` → `class PrdClaudeProcess` L129, `self._build_file_args(...)` L155, `def _build_file_args(config, step_id)` L170 (`@staticmethod` shape) | CONFIRMED — bound to class; signature varies at parent → "read first" guidance justified |
| E4 `_evaluate_gate` is class-bound (`PrdExecutor`) | `grep -n` executor.py → `class PrdExecutor` L480, `def _evaluate_gate(` L823 (indented, inside class) | CONFIRMED |
| E2 `_check_parallel_instructions` is module-level | `grep -n` prd/gates.py → `def _check_parallel_instructions(content)` L200 (col 0) | CONFIRMED — direct call OK |
| E3 `gate_passed` is module-level | `grep -n` pipeline/gates.py → `def gate_passed(` L23 (col 0) | CONFIRMED — direct call OK |
| `_pollution_snapshot` line | `grep -n` tests/conftest.py → `def _pollution_snapshot():` L29 | CONFIRMED — task said 30-93, actual is 29 → FIX-3 valid |

---

## Fixes Applied

### FIX-1 (IMPORTANT) — Fabricated `evalIdString` provenance removed (Step 3.4 + echo in Step 3.5)

- **Location:** Step 3.4 (schema item, L266) + Step 3.5 (fidelity-test enum-pin clause, L270).
- **Before (3.4):** "...whose `escape_id` reuses the `evalIdString` regex `^[A-Z][A-Za-z0-9]*([0-9]+(\.[0-9]+)?)?$`..."
- **After (3.4):** Declares a NEW `$defs.escapeId` string `$def` with literal pattern `^E[0-9]+$`
  (sufficient for E1..E5), and an explicit directive to declare it FRESH and NOT attempt to reuse
  any escape-id/eval-id `$def` from `summary.schema.json` (which has none — only an unrelated
  `evalStatus` enum), so the executor will not grep for a non-existent symbol. `escape_id` now
  `{"$ref":"#/$defs/escapeId"}`.
- **After (3.5):** Added assertion clause — fidelity test pins
  `schema["$defs"]["escapeId"]["pattern"] == "^E[0-9]+$"` sourced from the schema's OWN $def, NOT
  from `summary.schema.json`.
- **Step 3.2 (model):** No edit required — `escape_id` there is a Python dataclass field, not a
  schema-pattern echo; it never referenced `evalIdString`.
- **Verify:** `grep -c "evalIdString"` → **0** (the literal symbol no longer appears anywhere,
  including in the warning text, which was reworded to avoid naming it).

### FIX-2 (IMPORTANT) — E1/E4 bound-method vs E2/E3 module-function invocation guidance

- **Location:** Step 3.1 (generic ReplayExecutor in-process-invocation contract, L254), Step 4.3
  (E1 runner, L332), Step 4.6 (E4 runner, L344).
- **Before:** Items said "invoke the real pre-fix callable in-process" with no distinction between
  class-bound and module-level callables; a naive import-and-call of E1/E4 would raise.
- **After (3.1):** Added CRITICAL invocation-contract caveat — E1 `_build_file_args`
  (`PrdClaudeProcess`, process.py) and E4 `_evaluate_gate` (`PrdExecutor`, executor.py) are
  CLASS-BOUND; E2 `_check_parallel_instructions` (prd/gates.py) and E3 `gate_passed`
  (pipeline/gates.py) are MODULE-LEVEL and callable directly. Executor must obtain a class instance
  (instantiate / `SimpleNamespace` self) for the bound pair, direct-call the module pair, and
  **read the actual pre-fix-parent signature FIRST** (do NOT hardcode — a method may be
  `@staticmethod`/`@classmethod` at the parent commit). Owning-class names are instantiation
  guidance only.
- **After (4.3):** E1-specific note — `_build_file_args` is class-bound to `PrdClaudeProcess`;
  naive module import-and-call fails; read the `94d5baa0` signature first (may be `@staticmethod`
  taking `(config, step_id)` with no `self`); class name is instantiation guidance, not a hardcoded
  signature.
- **After (4.6):** E4-specific note — `_evaluate_gate` is class-bound to `PrdExecutor` (unlike
  module-level E2/E3); obtain a `PrdExecutor` instance; read the `1b0264f1` signature first; do not
  hardcode.
- **Verify:** signature-read-first guidance present; E4 `1b0264f1` pin preserved (7 refs);
  no signature hardcoded.

### FIX-3 (MINOR) — `_pollution_snapshot` citation corrected (Step 5.1)

- **Location:** Step 5.1 (L402).
- **Before:** "the root `_pollution_snapshot` autouse guard at lines 30-93..."
- **After:** "the root `_pollution_snapshot` autouse guard at `tests/conftest.py:29` —
  `def _pollution_snapshot` —..."
- **Verify:** behavioral claim (fails session on `docs/` writes) preserved; only the line citation
  corrected to the verified `tests/conftest.py:29`.

### FIX-4 (MINOR) — E2/E3 shared-H3-ref distinct-facet clarity (Steps 4.4, 4.5)

- **Location:** Step 4.4 (E2 runner, L336) + Step 4.5 (E3 runner, L340).
- **Before:** No note that E2 and E3 both proxy the same `unmask-and-sweep.md` ref under wave H3.
- **After (4.4):** One-line NOTE — E2 and E3 both map to H3 and both proxy `unmask-and-sweep.md`,
  but assert DISTINCT facets: E2 = word-boundary `complete` ⊄ `incomplete` classifier (this item);
  E3 = sibling-heading unmask/sweep `K_swept == K_true` + WARN/CONTINUE. Do not collapse.
- **After (4.5):** Mirror NOTE from E3's perspective (E3 facet = sibling-heading sweep
  `K_swept == K_true` + WARN/CONTINUE; E2 facet = word-boundary classifier).
- **Verify:** one-liner each, no structural change; wave-H3 mapping and `requires_impl_ref`
  decorators preserved.

### FIX-5 (MINOR) — Key Constraints "3 agents" inert contradiction reworded (L124)

- **Location:** `## Execution Context` → Key Constraints (L124).
- **Before:** "QA intensity = standard (per I22): intermediate/phase gates = 3 agents;
  final/phase-gate lens QA = 7 agents..."
- **After:** "QA intensity = standard (per I22): phase QA gates use 7 lens agents (3 rf-qa
  structural + 3 rf-qa-qualitative content + 1 domain lens) per the standard PER_PHASE band; no
  intermediate research/synthesis gates are encoded; fidelity gate = 2 agents; max 2 fix cycles per
  gate; 2 verification agents."
- **Verify:** the misleading "3 agents" intermediate-gate claim removed; reality (7 lens phase
  gates, no intermediate gates) stated; matches the 4 actual Phase 2-5 QA-gate headers.

---

## Post-fix constraint verification (grep evidence)

| Constraint | Command | Result |
|-----------|---------|--------|
| Zero `evalIdString` | `grep -c "evalIdString"` | **0** ✓ |
| Zero `{UPPER}` placeholders | `grep -coE '\{[A-Z]+\}'` | **0** ✓ |
| Zero parent-sha + caret | `grep -coE "(94d5baa0\|10723863\|e97aa4fd\|1b0264f1\|d878bc6d)\^"` | **0** ✓ |

## Preserved-clean content verification (NOT touched / still intact)

| Item | Evidence |
|------|----------|
| G1 no-caret parent SHAs | all 5 present (E1=94d5baa0 ×10, E2=10723863 ×12, E3=e97aa4fd ×12, E4=1b0264f1 ×25, E5=d878bc6d ×10), zero with `^` |
| E4 `1b0264f1` pin (NOT HEAD) | 7 "pinned to `1b0264f1`" refs preserved |
| skipif / no-xfail / no-importorskip | `skipif` present (12); `xfail` (6) and `importorskip` (5) all in NEVER/NO prohibition contexts |
| anti-vacuity backtest_status derivation | 2 "ANTI-VACUITY" refs (all-5-CATCH ∧ non-null negative_witness ∧ non-null card_path → complete) preserved |
| SELF-RUN POST-reflect form | 2 "POST-reflect" refs preserved (no human-handoff conversion) |
| ≥7-agent QA gates | 4 "7 lens agents + serialized fix + 2-agent verify" gate headers (Phases 2-5) preserved; none weakened |
| `parents[3]` path resolution | 8 `parents[3]` refs; 3 `parents[2]` refs all prohibition ("NOT `parents[2]`") |
| collision boundary | unchanged (only files under `tests/troubleshoot/backtest/` targeted by items) |

---

## Self-Audit

**(a) Reliance list — structural items NOT re-checked (delegated to rf-qa structural gates):**
- Relied on prior structural QA for section numbering, frontmatter shape, and template conformance
  (no `## Inherited Structural Verdict` block was supplied; this is the consolidated-fix lens, not
  a fresh structural pass).

**(b) Independent semantic checks (tool-verified):**
- `evalIdString` absence in `summary.schema.json` — verified via `grep -n` (only `evalStatus`
  enum exists) → confirms FIX-1's fabricated-provenance finding before editing.
- E1/E4 class-bound vs E2/E3 module-level callable shapes — verified via `grep -n` on the four
  source files AND `git show 94d5baa0:...process.py` (E1 is `@staticmethod`-shaped at the parent,
  justifying the "read signature first" wording) → confirms FIX-2 is accurate, not speculative.
- `_pollution_snapshot` at `tests/conftest.py:29` — verified via `grep -n` → confirms FIX-3's
  off-by-N citation correction.
- Post-fix invariants (parent SHAs, E4 pin, anti-vacuity, POST-reflect, 7-agent gates) re-grepped
  to prove no preserved content regressed during the edits.

---

## Summary
- Fixes applied: 5 / 5 (FIX-1, FIX-2, FIX-3, FIX-4, FIX-5)
- Edits made: 8 surgical Edits across L124, L254, L266, L270, L332, L336, L340, L344, L402
- Constraint greps: 3/3 pass (evalIdString=0, {UPPER}=0, sha+caret=0)
- Preserved content: 8/8 verified intact
- Tool engagement: Read: 4 | Grep/Bash: 6 | Edit: 8 | Write: 1
- Out-of-scope findings: none (all 5 findings target the task file, which IS the edit target)

FIXES_APPLIED: 5, REMAINING: 0
