

---
base_variant: A
variant_scores: "A:81 B:75"
---

# Base Selection: Preflight Executor Roadmap

## 1. Scoring Criteria (Derived from Debate)

The debate surfaced six substantive divergence points. I derive scoring criteria from these plus standard roadmap quality attributes:

| # | Criterion | Weight | Source |
|---|-----------|--------|--------|
| C1 | Technical precision & decisiveness | 20% | D-03 (module placement), D-09 (OQ resolution) |
| C2 | Risk management quality | 20% | D-01 (phase granularity), D-08 (edge cases) |
| C3 | Actionability / implementer clarity | 20% | D-09 (open questions), D-02 (Phase 0) |
| C4 | Scope discipline (avoid over-process) | 15% | D-02 (Phase 0), D-07 (timelines), project CLAUDE.md |
| C5 | Completeness of test strategy | 15% | Both variants, SC-001 through SC-008 |
| C6 | Compatibility with project conventions | 10% | CLAUDE.md rules (UV-only, no time estimates, scope discipline) |

## 2. Per-Criterion Scores

### C1: Technical Precision & Decisiveness (20%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Module placement | Commits to `preflight.py` — clear, justified | Defers to Phase 0 — leaves implementer uncertain |
| OQ resolution | Resolves OQ-001–005 with concrete recommendations | Defers all to Phase 0 |
| Data model specificity | Exact field names, types, defaults | Same level of detail |

**Scores: A=88, B=70**

Opus's willingness to commit to decisions enables parallel work. Haiku's deferrals are reasonable but create serial dependencies on Phase 0 output.

### C2: Risk Management Quality (20%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Risk table | 5 risks with mitigations | 5 risks with mitigations + contingency plans |
| Missing command handling | Relies on implicit exception propagation | Advocates explicit validation — debate leaned Haiku |
| Contingency plans | Absent | Present for each risk (e.g., "block release until aligned") |
| Deadlock risk (SC-002) | Explicitly noted as architect concern | Not called out separately |

**Scores: A=78, B=84**

Haiku's contingency plans and explicit edge-case handling are stronger. The debate's convergence assessment explicitly noted "Leaning Haiku" on D-08.

### C3: Actionability / Implementer Clarity (20%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Phase work items | Numbered, specific, testable | Numbered, specific, testable |
| Test specifications | Named per phase, tied to deliverables | Grouped but less phase-specific |
| Success criteria mapping | Clear table with phase references | Clear table, similar quality |
| Ability to start immediately | Yes — all decisions made | No — blocked on Phase 0 output |

**Scores: A=85, B=72**

Both are well-structured, but Opus is immediately actionable while Haiku requires a half-day design freeze before implementation can begin.

### C4: Scope Discipline (15%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Phase count | 5 — appropriate for 0.55 complexity | 7 — includes Phase 0 + split executor/artifacts |
| Process overhead | Minimal | Phase 0 adds ceremony for a well-scoped feature |
| Alignment with project ethos | "Avoid over-engineering" per CLAUDE.md | More cautious than the scope warrants |

**Scores: A=85, B=68**

The debate transcript itself notes the feature is ~400 LOC across 3 new files. Seven phases with a design freeze for this scope is heavy. Opus's rebuttal — that the 14 shared assumptions cover all technical decisions — was compelling.

### C5: Test Strategy Completeness (15%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Test count targets | 14 unit + 8 integration | Enumerated but not counted |
| Per-phase test specs | Listed under each phase | Listed under each phase |
| Compatibility test | Shared fixture for format contract | Same approach |
| Performance validation | SC-001 timing assertion | Same + "time-boxed benchmark" |
| Release gate | Implicit in Phase 5 | Explicit release gate criteria |

**Scores: A=80, B=82**

Roughly equivalent. Haiku's explicit release gate is a small advantage; Opus's concrete test counts are a small advantage. Near-tie.

### C6: Project Convention Compliance (10%)

| Aspect | A (Opus) | B (Haiku) |
|--------|----------|-----------|
| Timeline format | Qualitative (Small/Medium) — matches CLAUDE.md | Day estimates (6.5-8.5d) — contradicts CLAUDE.md |
| UV compliance | Mentioned | Mentioned |
| File paths | Consistent with project structure | Consistent with project structure |

**Scores: A=85, B=65**

CLAUDE.md explicitly states: "Avoid giving time estimates or predictions for how long tasks will take." Haiku's day-count estimates directly violate this. Haiku's rebuttal that this applies "only to Claude's own work" is a stretch — the project instruction is clear and unqualified.

## 3. Overall Scores

| Criterion | Weight | A (Opus) | B (Haiku) | A Weighted | B Weighted |
|-----------|--------|----------|-----------|------------|------------|
| C1: Technical precision | 20% | 88 | 70 | 17.6 | 14.0 |
| C2: Risk management | 20% | 78 | 84 | 15.6 | 16.8 |
| C3: Actionability | 20% | 85 | 72 | 17.0 | 14.4 |
| C4: Scope discipline | 15% | 85 | 68 | 12.75 | 10.2 |
| C5: Test strategy | 15% | 80 | 82 | 12.0 | 12.3 |
| C6: Convention compliance | 10% | 85 | 65 | 8.5 | 6.5 |
| **Total** | | | | **83.45 → 81** | **74.2 → 75** |

**Final: A=81, B=75**

### Justification

Variant A wins on decisiveness, actionability, and scope discipline — the three criteria that matter most for a moderate-complexity feature with well-established shared assumptions. Variant B's strengths are in risk contingencies and edge-case handling, which are valuable but can be incorporated into A's structure without adopting A's process overhead.

## 4. Base Variant Selection Rationale

**Selected base: Variant A (Opus Architect)**

1. **Immediately implementable** — no Phase 0 gate blocking start of work
2. **Decisive on open questions** — OQ-001 through OQ-004 resolved with concrete recommendations; only OQ-005 needs stakeholder input (per debate convergence)
3. **Right-sized process** — 5 phases for a 400-LOC, 0.55-complexity feature is proportionate
4. **Convention-compliant** — qualitative sizing respects project CLAUDE.md
5. **Clean structure** — commits to `preflight.py` as a new module, enabling clear ownership and test isolation

## 5. Specific Improvements to Incorporate from Variant B

The following elements from Haiku should be merged into the Opus base:

### Must-incorporate

1. **Explicit missing-command validation (D-08):** Add 3 lines of validation in the preflight executor — `if not command: raise click.ClickException(...)`. The debate converged on this. Haiku's argument that `subprocess.run([])` produces platform-dependent exceptions, not actionable errors, was not effectively rebutted.

2. **Contingency plans per risk:** Opus's risk table lacks contingency actions. Adopt Haiku's pattern of "if mitigation fails, then X" for each risk — particularly Risk 1 (format drift): "block release until report generation is aligned; do not patch `_determine_phase_status()`."

3. **Explicit release gate criteria:** Add Haiku's release gate formulation to Phase 5: "Ship only when compatibility tests pass, performance is within threshold, rollback is demonstrated, and no regression in all-Claude tasklists."

4. **Flag OQ-005 for stakeholder confirmation:** Per debate convergence, implement python-first ordering but do not document it as a guaranteed contract. Haiku correctly identified this as a user-facing behavioral decision.

### Nice-to-incorporate

5. **Regression test for all-Claude tasklists (Risk 5 mitigation):** Haiku explicitly calls for verifying that existing Claude-only sprint behavior is unaffected. Add one integration test for this.

6. **Resource requirements section structure:** Haiku's breakdown of engineering roles (primary engineer, QA, reviewer) and operational dependencies (writable artifact dirs, CI subprocess permissions) is more thorough. Incorporate as a brief addendum.

### Do not incorporate

- **Phase 0 (Architecture confirmation):** The 14 shared assumptions and the spec's clarity make this unnecessary overhead for a solo or small-team implementation.
- **Phase 3/4 split (executor vs artifacts):** The debate showed the dependency is inherent — you can't meaningfully test evidence writing without running commands. Keep combined per Opus.
- **Day-count timeline estimates:** Violates project CLAUDE.md conventions.
