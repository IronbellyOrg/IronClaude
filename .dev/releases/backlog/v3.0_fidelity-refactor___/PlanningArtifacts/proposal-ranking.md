# Fidelity Refactor -- Proposal Ranking

**Date**: 2026-03-17
**Pipeline**: 4-phase systemic refactoring proposal pipeline
**Input**: cli-portify executor no-op forensic report
**Method**: 5-agent brainstorm -> scoring framework -> 5-agent adversarial debate -> ranking

---

## 1. Ranked Proposal Table

| Rank | Proposal | Source | Fidelity Link | Weighted Score | Success | Complexity | FP Risk | Maintain | Compose |
|------|----------|--------|---------------|----------------|---------|------------|---------|----------|---------|
| 1 | Two-Pass Validation (Programmatic Sweep + LLM Deep Dive) | brainstorm-01 A3 | Link 1: Spec->Roadmap | **6.80** | 7.0 | 7.0 | 6.0 | 6.0 | 8.0 |
| 2 | Test Requirement ID Extraction & Cross-Reference Gate | brainstorm-03 A1 | Link 1: Spec->Roadmap | **6.75** | 6.5 | 7.5 | 6.0 | 6.0 | 8.0 |
| 3 | Wiring Verification Gate (Static Import-Chain Analysis) | brainstorm-05 A2 | Link 3: Tasklist->Code | **6.75** | 8.0 | 5.5 | 5.5 | 6.0 | 8.5 |
| 4 | Deviation Count Reconciliation Gate | brainstorm-04 A3 | Link 1: Spec->Roadmap | **6.40** | 4.0 | 8.5 | 7.0 | 7.0 | 7.5 |
| 5 | End-to-End Call Path Task Verification | brainstorm-02 B5 | Link 2: Roadmap->Tasklist | **5.13** | 6.0 | 3.5 | 4.5 | 4.5 | 8.0 |

### Score Distribution Analysis

- **Top 3 cluster (6.75-6.80)**: Proposals 1-3 are effectively tied. Tiebreaker: Proposal 3 (Wiring Verification) has the highest Likelihood to Succeed (8.0) and would definitively catch the cli-portify bug at Link 3.
- **Middle tier (6.40)**: Proposal 4 (Deviation Count Reconciliation) scores highest on Implementation Complexity (8.5 = trivial to implement) but lowest on Likelihood to Succeed (4.0) because it catches a secondary failure mode (LLM arithmetic errors), not the primary cli-portify failure.
- **Lower tier (5.13)**: Proposal 5 (Call Path Verification) has strong composability but suffers from the chicken-and-egg problem: it validates against the roadmap, which was already lossy in the cli-portify case.

---

## 2. Recommended Implementation Order

### Wave 1: Immediate (Next Release)

**Proposal 4: Deviation Count Reconciliation Gate**
- **Why first**: Trivial to implement (35-55 lines, 1 file), zero pipeline changes, fits existing `SemanticCheck` signature perfectly. Provides a self-consistency layer that catches LLM arithmetic errors in fidelity reports.
- **Effort**: 1-2 hours. Add `_deviation_counts_reconciled` to `roadmap/gates.py`.
- **Prerequisite for**: Proposal 1 (shares DEV-NNN parsing utility with A4 severity spot-check).

**Proposal 3: Wiring Verification Gate (narrow initial scope)**
- **Why early**: Highest Likelihood to Succeed (8.0). Directly catches the cli-portify no-op bug pattern. Start with narrow scope: `Optional[Callable] = None` call-site analysis + `REGISTRY`/`DISPATCH` dictionary checks only.
- **Effort**: 2-3 days. New module `audit/wiring_gate.py` (~200-300 lines for narrow scope).
- **Deploy in shadow mode** per B4 rollout strategy to collect false positive data before enforcement.

### Wave 2: Foundation Building (Next Release +1)

**Proposal 1: Two-Pass Validation (Programmatic Sweep + LLM Deep Dive)**
- **Why second wave**: Requires upstream prerequisite -- extraction prompt must mandate exhaustive FR-NNN/NFR-NNN/SC-NNN assignment. Wave 1 gives time to implement this co-requisite.
- **Effort**: 3-5 days. `pre_checks` extension to `GateCriteria` (~60 lines infra), ID extraction function (~40 lines), prompt modification (~15 lines).
- **Key decision**: Use Option B (`pre_checks` on `GateCriteria`) for maximum composability. Add override mechanism for intentional deferrals.

**Proposal 2: Test Requirement ID Extraction & Cross-Reference Gate**
- **Why alongside Proposal 1**: Shares the `pre_checks` infrastructure from Proposal 1. Test requirements are a subset of the ID extraction Proposal 1 builds.
- **Effort**: 2-3 days (incremental on Proposal 1). Add `test_requirements` to extraction frontmatter, add cross-reference semantic check.
- **Pair with B3** (Bidirectional Traceability ID Enforcement from brainstorm-03) for end-to-end deterministic coverage.

### Wave 3: Full Coverage (When Justified by Data)

**Proposal 5: End-to-End Call Path Task Verification**
- **Why deferred**: Highest complexity (500+ lines), lowest score (5.13). The chicken-and-egg dependency on roadmap completeness limits its value until upstream gates (Waves 1-2) are in place.
- **Trigger**: Implement only if Waves 1-2 prove insufficient at catching incomplete task decomposition from correct roadmaps.
- **Effort**: 5-7 days. New pipeline step, new prompt, new gate.

---

## 3. Proposal Combinations (Reinforcement Map)

```
                     Link 1               Link 2                Link 3
                  Spec->Roadmap      Roadmap->Tasklist      Tasklist->Code
                  ============       ==================     ==============

Wave 1:           [4] DevCount                              [3] WiringGate
                  Reconciliation                            (shadow mode)
                       |
                       v
Wave 2:           [1] Two-Pass -------> enables B1/B3 -----> feeds into [3]
                  Validation          (from brainstorm       (wiring gate
                       |               01/03, not debated    enforcement)
                       |               but recommended)
                  [2] Test Req -------> enables B3
                  ID Cross-Ref       (bidirectional
                                      traceability)

Wave 3:                              [5] Call Path
                                     Verification
                                     (if needed)
```

### Strongest Combinations

| Combination | Links Covered | Reinforcement Effect |
|-------------|---------------|---------------------|
| [1] + [2] | Link 1 (dual) | Two-Pass provides deterministic floor for all IDs; Test Req adds focused test coverage. Shared `pre_checks` infra. |
| [1] + [3] | Link 1 + Link 3 | Two-Pass catches spec->roadmap drops; Wiring Gate catches code-level no-ops. Defense in depth across the full chain. |
| [3] + [4] | Link 1 + Link 3 | DevCount catches LLM inconsistency in fidelity reports; Wiring Gate catches code integration failures. Covers both document and code validation. |
| [1] + [2] + [3] + [4] | Links 1 + 3 | **Recommended full deployment.** Four gates covering upstream requirements (1, 2), LLM consistency (4), and code integration (3). |

### Weakest Combinations (Avoid)

| Combination | Issue |
|-------------|-------|
| [4] alone | Catches only LLM arithmetic errors, not the primary failure modes |
| [5] alone | Chicken-and-egg problem: validates against potentially lossy roadmap |
| [2] without [1] | Test-specific gate without general ID cross-referencing misses functional requirement drops |

---

## 4. Estimated Total Implementation Scope

| Wave | Proposals | New Code (est.) | Files Modified | Files Created | Calendar Estimate |
|------|-----------|-----------------|----------------|---------------|-------------------|
| Wave 1 | [4] + [3] narrow | ~300-350 lines | 2 (gates.py, prompts.py) | 1 (wiring_gate.py) | 3-4 days |
| Wave 2 | [1] + [2] | ~200-250 lines | 3 (models.py, gates.py, prompts.py) | 0 | 4-6 days |
| Wave 3 | [5] if needed | ~500-600 lines | 2 (tasklist/gates.py, tasklist/prompts.py) | 1 (call_path.py) | 5-7 days |
| **Total** | **All 5** | **~1000-1200 lines** | **5 unique files** | **2 new modules** | **~2-3 weeks** |

### Shared Infrastructure Requirements

All proposals except [4] require extending the `SemanticCheck` interface to accept cross-file context:

```python
# Current (gates.py)
check_fn: Callable[[str], bool]

# Required for [1], [2], [3], [5]
check_fn: Callable[[str], bool]  # backward compatible
# Plus new pre_checks on GateCriteria:
pre_checks: list[Callable[[Path, Path], tuple[bool, str | None]]] | None = None
```

This is a ~15-line change to `pipeline/models.py` and `pipeline/gates.py` that enables all proposals. **Implement in Wave 1 alongside Proposal 4.**

---

## 5. Recommended Next Step

**Proposal 3 (Wiring Verification Gate) should become the next release spec.**

### Rationale

1. **Highest Likelihood to Succeed** (8.0): The only proposal that would definitively catch the cli-portify no-op bug through deterministic analysis, without depending on upstream prerequisites.
2. **Addresses the missing link**: Link 3 (Tasklist->Code) has zero coverage today. All other proposals strengthen Links 1-2 which already have gates (even if imperfect). Proposal 3 creates an entirely new defense layer.
3. **Composability**: Scores 8.5 on composability. Its check functions integrate directly into the unified-audit-gating v1.2.1 task-scope gate (B1) and serve as the executor for tasklist-emitted audit metadata (B5).
4. **Shadow mode rollout**: Can be deployed non-blocking to collect data while Wave 2 prerequisites (ID assignment, `pre_checks` infra) are built.

### Spec Scope for Next Release

```
Title: Wiring Verification Gate v1.0
Link:  Link 3 (Tasklist->Code)
Scope: Narrow initial scope
  - Optional[Callable] = None call-site analysis
  - REGISTRY/DISPATCH/RUNNERS dictionary import verification
  - Orphan module detection (steps/ directories)
  - No-op fallback detection (deferred to v1.1 pending shadow data)
Deploy: Shadow mode -> soft mode -> full enforcement
Integration: GateCriteria/SemanticCheck pattern, STRICT tier
Output: YAML report (unwired_count, orphan_module_count)
```

**Pair with Proposal 4 (Deviation Count Reconciliation)** as a quick-win companion that ships in the same release with minimal effort.

---

## Appendix: Debate Score Summary

| Debate | Proposal | Advocate Score | Skeptic Score | Final Score | Key Dispute |
|--------|----------|---------------|---------------|-------------|-------------|
| 01 | Two-Pass Validation | ~7.20 (est.) | ~5.80 (est.) | 6.80 | ID prerequisite dependency; veto power false positives |
| 02 | Call Path Verification | 6.20 | 4.40 | 5.13 | Chicken-and-egg: validates lossy roadmap |
| 03 | Test Req ID Cross-Ref | ~7.10 (est.) | ~6.10 (est.) | 6.75 | Narrow scope; satisfiable without substance |
| 04 | Deviation Count Recon | ~6.90 (est.) | ~5.80 (est.) | 6.40 | Secondary failure mode; no evidence it caused cli-portify |
| 05 | Wiring Verification | 7.50 | 5.40 | 6.75 | Dynamic dispatch blind spots; pattern heuristic maintenance |

### Cross-Debate Themes

1. **LLM-only gates are insufficient**: All 5 debates confirmed that deterministic enforcement is necessary alongside LLM analysis. The forensic report's finding is validated.
2. **Upstream prerequisites matter**: Proposals 1, 2, and 5 depend on upstream document quality (formal IDs, roadmap completeness). Proposal 3 is the only one that catches bugs regardless of upstream quality.
3. **The `SemanticCheck` interface needs extension**: All agents independently identified that `check_fn(content: str) -> bool` is too narrow for cross-file validation. The `pre_checks` extension is a consensus infrastructure requirement.
4. **Shadow mode rollout is essential**: Both Proposals 3 and 5 carry false positive risk. Shadow mode (from brainstorm-05 B4) is the consensus deployment strategy.
