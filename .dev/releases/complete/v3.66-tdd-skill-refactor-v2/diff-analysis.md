---
total_diff_points: 12
shared_assumptions_count: 11
---

## 1. Shared Assumptions and Agreements

Both roadmaps agree on:

1. **Complexity**: LOW (0.25), zero external dependencies, pure Markdown refactoring
2. **Spec source**: `tdd-command-layer-spec.md` as the governing specification
3. **Gold-standard template**: `commands/sc/adversarial.md` as the structural pattern
4. **Migration scope**: Same line ranges (48-63 prompt examples, 82-88 tier table) — ~23 lines relocated
5. **Success criteria**: Identical SC-1 through SC-12 validation matrix
6. **Risk identification**: Same 5 risks (content loss, protocol leakage, scope creep, sync failure, example context degradation) with matching severity ratings
7. **FR/NFR coverage**: Both reference the same requirement IDs from the spec
8. **Zero behavioral change**: Both treat protocol sections as immutable
9. **Canonical-first editing**: All changes to `src/superclaude/` before sync
10. **Sync pipeline**: Both require `make sync-dev` + `make verify-sync` as release gate
11. **Core phase sequencing**: Read references → Create command → Migrate content → Verify → Sync (same logical flow)

---

## 2. Divergence Points

### D-1: Phase Granularity — Dedicated Baseline Phase
- **Opus**: Folds baseline capture into Phase 1 ("Preparation & Template Study") alongside reference reading
- **Haiku**: Introduces a standalone Phase 0 ("Baseline & Control Setup") with checksums and behavioral section snapshots
- **Impact**: Haiku's approach provides stronger audit trail and makes Phase 3 verification trivially comparable against frozen snapshots. Opus's approach is more pragmatic and avoids an extra phase boundary for what is fundamentally 15 minutes of reading.

### D-2: Timeline Estimates — Order-of-Magnitude Gap
- **Opus**: ~85 minutes total (single implementer, minutes-level granularity)
- **Haiku**: ~2.0 working days (day-level granularity, assumes multiple roles)
- **Impact**: Opus's estimate reflects a single skilled developer executing continuously. Haiku's estimate accounts for handoffs, review cycles, and calendar overhead. For automated/single-session execution, Opus is realistic. For team-based delivery, Haiku is more conservative but arguably inflated for a 0.25-complexity task.

### D-3: Dev Copy Creation Timing
- **Opus**: Creates only canonical source in Phase 2; dev copy produced exclusively via `make sync-dev` in Phase 5
- **Haiku**: Phase 1 Task 1 states "Create `src/superclaude/commands/tdd.md` and sync copy `.claude/commands/sc/tdd.md`" — implying direct creation of both
- **Impact**: Opus strictly follows the documented workflow (canonical-first, sync-derived). Haiku's wording risks violating Architectural Constraint #2 by creating the dev copy manually rather than through the sync pipeline.

### D-4: Team Model
- **Opus**: Assumes single implementer throughout; no role separation
- **Haiku**: Explicitly defines three roles (Architect/maintainer, Reviewer, CI/automation)
- **Impact**: Haiku's multi-role model adds review checkpoints but introduces coordination overhead disproportionate to a 0.25-complexity task. Opus's single-implementer model is leaner and matches the actual execution context (one Claude session).

### D-5: Formal Traceability Rule
- **Opus**: Integrates verification into each phase implicitly; no formal traceability mandate
- **Haiku**: Adds explicit traceability rule: "Every phase closes with explicit FR/NFR/SC mapping before progressing"
- **Impact**: Haiku's approach produces auditable compliance evidence at each boundary. Opus achieves the same coverage but embeds it in task descriptions rather than enforcing a process gate.

### D-6: Evidence Report Artifact
- **Opus**: No formal evidence report; verification results are ephemeral (terminal output)
- **Haiku**: Phase 4 includes "Produce short evidence report mapping SC and FR/NFR to checks"
- **Impact**: Haiku creates a persistent compliance artifact useful for future audits or onboarding. Opus treats verification as pass/fail gates with no documentation overhead.

### D-7: Open Questions Handling
- **Opus**: No dedicated section; implicitly assumes spec is complete
- **Haiku**: Section 8 explicitly addresses open questions with a change-request escalation process
- **Impact**: Haiku's approach provides a documented escape valve if ambiguity surfaces mid-implementation. Low practical impact here (spec is complete), but establishes good process hygiene.

### D-8: Commit Strategy
- **Opus**: Explicitly recommends single atomic commit with rationale (clean `git revert` path)
- **Haiku**: Does not specify commit strategy
- **Impact**: Opus's guidance prevents a common mistake (splitting an atomic refactor into multiple commits that are individually broken). This is actionable and important.

### D-9: Baseline Depth
- **Opus**: Captures `wc -l` and `git diff --stat` baseline
- **Haiku**: Captures behavioral section snapshots AND checksums of refs/ files
- **Impact**: Haiku's checksum approach is more tamper-evident. Opus's approach is sufficient for the actual verification needs (diff-based checks in Phase 4).

### D-10: Parallelization Guidance
- **Opus**: Explicitly notes that Phase 4's 26 verification checks can be batched into parallel invocations
- **Haiku**: No parallelization discussion
- **Impact**: Minor but practical — parallel grep/diff calls can halve Phase 4 duration.

### D-11: Architect Recommendations Section
- **Opus**: Dedicated Section 8 with 5 specific, actionable recommendations (follow template exactly, edit canonical only, snapshot before migration, Phase 4 as hard gate, single commit)
- **Haiku**: No equivalent section; guidance is distributed across phase descriptions
- **Impact**: Opus's consolidated recommendations serve as a quick-reference checklist for the implementer. Particularly valuable for the "Phase 4 as hard gate" and "single commit" guidance.

### D-12: Integration Points Detail
- **Opus**: 4 integration points in a structured table with owning phase, wired components, and consuming phases; also embeds integration notes within phase descriptions
- **Haiku**: 3 named artifacts with cross-references but less granular wiring detail
- **Impact**: Opus's dual presentation (in-phase + summary table) makes it harder to miss a handoff. Haiku omits the SKILL.md Input section as a named integration point.

---

## 3. Areas Where One Variant Is Clearly Stronger

### Opus is stronger in:
- **Actionable implementer guidance**: The Architect Recommendations section (D-11) and single-commit guidance (D-8) directly prevent common mistakes
- **Timeline realism**: 85-minute estimate (D-2) is calibrated to the actual execution context; 2 days is excessive for 0.25 complexity
- **Integration point coverage**: 4 integration points vs 3, with richer wiring detail (D-12)
- **Parallelization awareness**: Explicit batching guidance for verification checks (D-10)
- **Sync discipline**: Correctly defers dev copy creation to `make sync-dev` (D-3)

### Haiku is stronger in:
- **Audit trail**: Formal traceability rule (D-5) and evidence report artifact (D-6) create persistent compliance records
- **Process hygiene**: Dedicated baseline phase (D-1) and open questions handling (D-7) add defensive structure
- **Baseline rigor**: Checksum-based verification of refs/ files (D-9) is more tamper-evident

---

## 4. Areas Requiring Debate to Resolve

1. **Evidence report (D-6)**: Is a persistent compliance artifact worth the overhead for a 0.25-complexity task? If this refactor pattern will repeat for other skills (PRD, design, etc.), the evidence template pays off. If one-shot, it's overhead.

2. **Dev copy creation (D-3)**: Haiku's wording may be ambiguous rather than intentionally wrong — needs clarification on whether it means "create via sync" or "create manually." If the latter, it should be corrected.

3. **Timeline calibration (D-2)**: The right estimate depends on execution context. For a Claude Code session, Opus's 85 minutes is correct. For a human team with review cycles, something between the two (half a day) is more realistic. Neither variant acknowledges this distinction.

4. **Phase 0 as separate phase (D-1)**: Marginal value. The baseline activities take ~15 minutes regardless of whether they're Phase 0 or Phase 1. The debate is purely about organizational clarity vs. phase count inflation.
