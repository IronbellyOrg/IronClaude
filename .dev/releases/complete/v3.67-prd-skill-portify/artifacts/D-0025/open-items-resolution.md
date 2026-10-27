# D-0025: Open Items Resolution Document

**Sprint**: v4.3.0 -- PRD CLI Pipeline
**Phase**: 5 (Validation + E2E)
**Task**: T05.01
**Date**: 2026-04-12

---

## OI-001: Scope Flag vs Inference

**Question**: Should the CLI pipeline support `--scope product` vs `--scope feature` as explicit flags, or always infer from request parsing?

**Impact**: Affects `config.py` and FR-PRD.2

### Decision: INFER FROM PARSING

**Rationale**:

1. **Consistency with current skill behavior**: The existing PRD skill (`.claude/skills/prd/SKILL.md`) determines scope by analyzing the user's natural-language request, not via an explicit flag. The CLI pipeline should preserve this behavior to avoid divergence between the skill and CLI paths.

2. **Implementation evidence**: The `PrdConfig` dataclass in `models.py:117` already has `prd_scope: str = "feature"` as a field with a default. The `resolve_config()` function in `config.py` does not expose a `--scope` CLI flag -- it leaves scope to be set during the `parse-request` pipeline step, which analyzes the user's request text.

3. **User ergonomics**: Requiring users to explicitly classify their request as "product" vs "feature" adds friction. The parse-request agent already handles this classification with high accuracy by examining request text for product-level indicators (platform-wide language, multiple subsystems, organizational scope).

4. **Escape hatch**: If a user wants to force product scope, they can include explicit scope language in their request (e.g., "Create a full product PRD for..."). No flag needed.

**Impact Analysis**: No code changes required. The current implementation already infers scope. This decision confirms the existing design is correct.

---

## OI-002: Maximum Wall-Clock Time for Heavyweight PRD Run

**Question**: What is the maximum acceptable wall-clock time for a full heavyweight PRD run?

**Impact**: Affects timeout budgets and stall thresholds

### Decision: 45 MINUTES (2700 seconds)

**Rationale**:

1. **Agent count analysis**: A heavyweight PRD run may launch 10+ agents across all phases:
   - Stage A (Research): 5-8 research agents + 2-3 web research agents = 7-11 agents
   - Stage B (Synthesis): 3-5 synthesis agents + 1 assembly agent = 4-6 agents
   - QA: 2-4 QA agents across gates
   - Total: 13-21 agent invocations including fix cycles

2. **Per-agent timeout budget**: The executor uses `stall_timeout * 30` as the subprocess timeout (see `executor.py:379`). With the default `stall_timeout=120`, this gives 3600s (60 minutes) per individual agent. However, most agents complete in 2-5 minutes with a 300-turn budget.

3. **Empirical estimate**: With 15 agents averaging 3 minutes each = 45 minutes. Fix cycles (up to 3 research + 2 synthesis) could add 15 minutes in worst case, but this is offset by parallel execution in partitioned QA.

4. **Budget exhaustion guard**: The `TurnLedger` enforces `--max-turns` (default 300) which provides a separate budget ceiling. The 45-minute wall-clock limit serves as a safety backstop, not the primary budget control.

5. **Recommended configuration**:
   - Default `--max-turns 300`: sufficient for standard and lightweight tiers
   - Heavyweight suggested `--max-turns 500`: accommodates larger agent count
   - Wall-clock alarm at 45 minutes: log warning + suggest increasing budget if still running

**Impact Analysis**: The current `stall_timeout=120` default (per-step) combined with `max_turns=300` already provides adequate time control. The 45-minute overall wall-clock guidance should be documented but does not require a new hard-coded timeout -- it's enforced naturally by the turn budget.

---

## OI-003 through OI-011: Implementation-Time Confirmation

| Item | Status | Confirmation |
|------|--------|--------------|
| OI-003 | During implementation | Correct. QA report file preservation is a filtering.py concern resolved during implementation. |
| OI-004 | During implementation | Correct. TUI agent progress display is a tui.py design decision. |
| OI-005 | During implementation | Correct. Case-insensitive section matching is a gates.py robustness concern. |
| OI-006 | During implementation | Correct. Concurrent QA write safety is a filtering.py/inventory.py concern. |
| OI-007 | During implementation | Correct. Gap deduplication strategy is a filtering.py concern. |
| OI-008 | During implementation | Correct. PrdPipelineResult.outcome typing is a models.py refinement. |
| OI-009 | During implementation | Correct. Placeholder false-positive handling is a gates.py concern. |
| OI-010 | During implementation | Correct. Empty-gaps FAIL handling is an executor.py fix-cycle concern. |
| OI-011 | During implementation | Correct. Verdict field test coverage is a test_gates.py concern. |

All 9 items (OI-003 through OI-011) are confirmed as correctly classified for resolution during implementation. None require pre-implementation decisions.

---

## Summary

| Item | Decision | Code Impact |
|------|----------|-------------|
| OI-001 | Infer scope from parsing (no explicit flag) | None -- confirms existing design |
| OI-002 | 45-minute max wall-clock for heavyweight | Documentation only -- existing timeouts adequate |
| OI-003--OI-011 | Confirmed as implementation-time targets | Deferred to implementation phase |
