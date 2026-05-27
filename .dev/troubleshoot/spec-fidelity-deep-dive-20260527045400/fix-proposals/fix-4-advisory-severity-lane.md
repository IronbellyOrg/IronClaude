# Fix Proposal #4 — New ADVISORY severity tier + CLI lane (Tier 2 / system-architect)

## Problem statement

The spec-fidelity gate is a binary closed-world classifier wired to an open-world finding stream. (1) Deterministic checkers emit findings from an open set (anything spec/roadmap can disagree about). (2) LLM remediation is structurally too weak to bridge them when disagreement is non-additive. (3) Convergence orchestrator's ONLY pass predicate is `active_high_count == 0` (`convergence.py:539`). Every prior remediation hardened orchestration WITHIN the closed-world assumption. The cosmetic-remediation lane (`--allow-cosmetic-remediation`, `SKILL.md:148-155`) is the ONE place where a non-binary terminal state (`remediated`) was introduced — and it works. The S5 fix (`_classify_nfr_severity` at `structural_checkers.py:309-327`) is the in-module precedent for severity-demotion as gate bypass. Extending these two patterns to `id_schema_drift`-class findings is the architectural completion of an existing project pattern.

## Proposed change

THREE files (architectural lane + checker + CLI flag).

**Part A — `src/superclaude/cli/roadmap/structural_checkers.py`** (~35 LOC):

1. Add `_canonicalize_requirement_id(pid: str) -> str` next to `_classify_nfr_severity` at line ~309.
2. Add new `mismatch_type` literal: `"id_schema_drift"`. Add entry to `SEVERITY_RULES` (`structural_checkers.py:42-67`): `("signatures", "id_schema_drift") -> "ADVISORY"`.
3. Modify the phantom_id block at lines 372-391 to emit `id_schema_drift` (ADVISORY) for canonical-match-but-form-differs cases; emit current HIGH `phantom_id` for genuine phantoms.

**Part B — `src/superclaude/cli/roadmap/convergence.py` and registry** (ZERO source change; one semantic change via the new severity tier):

The registry's `get_active_high_count` at line 242 already filters by `severity == "HIGH"`. Findings emitted with new tier `ADVISORY` (slotting beneath MEDIUM) are AUTOMATICALLY excluded from the gate predicate WITHOUT any `convergence.py` edit. Architectural payoff: pass condition stays binary; vocabulary becomes a deliberate three-state ladder (`HIGH=gating, MEDIUM=informational, ADVISORY=deferred-by-design`).

**Part C — `src/superclaude/cli/roadmap/commands.py`** (~20 LOC, mirrors `--allow-cosmetic-remediation` lines 153-170):

Add `--allow-advisory-drift / --no-allow-advisory-drift` (default: enabled) and `--strict-no-advisory` alias. When `--strict-no-advisory`, checker emits `id_schema_drift` at HIGH (restoring current gating behavior for high-stakes runs).

**Part D — `sprint/models.py`** (~2 LOC): add `"ADVISORY"` to `Finding.severity` allowed-values list.

## Evidence

- `src/superclaude/cli/roadmap/convergence.py:539` — sole pass branch (binary)
- `src/superclaude/cli/roadmap/convergence.py:242-244` — `get_active_high_count` filters HIGH; vocabulary slot for ADVISORY exists by construction
- `src/superclaude/cli/roadmap/remediate_executor.py:309-362` — 30% per-patch guard (the second architectural primitive)
- `src/superclaude/skills/sc-roadmap-protocol/SKILL.md:148-155` — cosmetic-remediation lane (working precedent for non-binary terminal state)
- `src/superclaude/cli/roadmap/structural_checkers.py:309-327` — `_classify_nfr_severity` (in-module precedent for severity-demotion-as-gate-bypass; S5 fix)
- `src/superclaude/cli/roadmap/integration_contracts.py:445` — canonicalization precedent

## Risks

- **`ADVISORY` is a new severity tier**: downstream consumers that switch-case on `Finding.severity` need updates. Mitigation: grep `severity\s*==` across `src/superclaude/cli/roadmap/`; registry filter is whitelist (HIGH-only) → safe by default.
- **Quietly hides real schema drift**: ADVISORY hides legitimately-distinct ID divergence. Mitigation: `--strict-no-advisory` opt-out + ADVISORY findings remain in the report (just non-gating).
- **Doesn't address next rule_id**: if next release fails on `function_missing` with similar "structurally unfixable additively" pattern, this lane only generalizes if extended (one-line SEVERITY_RULES update per rule_id).
- **Doesn't address LLM attention drift** (Pattern 1) — semantic-fluctuation failures remain possible.

## Test plan

- New: `test_phantom_id_drift_emits_advisory_not_high`
- New: `test_genuine_phantom_id_still_emits_high`
- New: `test_advisory_findings_do_not_block_pass`
- New: `test_strict_no_advisory_flag_restores_high_severity`
- Regression: existing `phantom_id` HIGHs from genuine missing IDs still pass

## Documented constraints to honor

### Restrictions
1. Module ownership — checker + severity in `structural_checkers.py`; CLI flag in `commands.py` (which already owns gate-lane flags). [COMPLIES]
2. Pure-function contract — `_canonicalize_requirement_id` pure; mirrors `_classify_nfr_severity` exactly. [COMPLIES]
3. 30% per-patch guard — ~35 LOC in 700-line file = ~5%. [COMPLIES]
4. Binary pass condition `active_highs == 0` — **NOT MODIFIED**. New severity tier slots beneath the predicate's filter automatically. Vocabulary change, not predicate change. [COMPLIES IN SPIRIT]
5. Spec is input. [COMPLIES]
6. `max_runs=3`. [COMPLIES]
7. Canonicalization precedent. [LEVERAGED — fix is architectural completion of three existing precedents: cosmetic-remediation lane + `_classify_nfr_severity` MEDIUM-demotion + `_canonicalize_identifiers`]

### Re-frame signals
1. No shipped fix has touched the comparator — this fix does AND introduces the missing terminal-state vocabulary. [ADDRESSES BOTH]
2. Failure shape has shifted — generalizable to next rule_id with one-line SEVERITY_RULES additions. [ADDRESSES]
3. Chosen remediation surface is `structural_checkers.py` — primary checker code is there; CLI flag is in `commands.py` (the right place per project pattern). [ALIGNED]
