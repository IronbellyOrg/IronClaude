---
total_diff_points: 12
shared_assumptions_count: 14
---

# Comparative Diff Analysis: Haiku-Architect vs Opus-Architect Roadmaps

## 1. Shared Assumptions and Agreements

1. **Spec source and complexity**: Both derive from `portify-release-spec.md` at complexity 0.65 (MEDIUM)
2. **Core deliverable**: 6 input forms resolving to `ResolvedTarget` via a new `resolution.py` module
3. **Backward compatibility as primary risk**: RISK-2 is release-blocking; `resolve_workflow_path()` preserved unchanged
4. **No base-module modification**: `pipeline/` and `sprint/` untouched (NFR-WORKFLOW.2)
5. **Synchronous-only constraint**: No `async def` or `await` (NFR-WORKFLOW.3)
6. **Same 6 risks identified**: RISK-1 through RISK-6 with identical severity ratings
7. **Same 12 success criteria**: SC-1 through SC-12 mapped identically
8. **Same 7 open questions deferred**: OQ-1 through OQ-7 to v2.25
9. **Same dependency graph**: `cli.py → resolution.py → models.py`, no circular deps
10. **Same external dependencies**: Click, pathlib, re, os.path.commonpath, time.monotonic
11. **Same agent extraction approach**: 6 AGENT_PATTERNS, `--include-agent` escape hatch, warnings not errors
12. **Same directory consolidation strategy**: >10 dirs triggers warning, common-parent grouping, top-10 fallback
13. **Same `to_dict()` enrichment**: warnings, command_path, skill_dir, target_type, agent_count
14. **Same manifest behavior**: Write-only in v2.24.1, load deferred

## 2. Divergence Points

### D1: Phase Structure and Granularity

- **Haiku**: 7 phases (0–6), including Phase 0 (architecture confirmation) and Phase 6 (post-release observation)
- **Opus**: 5 phases (1–5), no pre-implementation architecture phase, no post-release phase
- **Impact**: Haiku's Phase 0 adds explicit architectural lock-in before code touches files, reducing mid-implementation rework. Opus assumes architectural alignment is implicit. Haiku's Phase 6 formalizes observation as a deliverable; Opus mentions OQ monitoring but doesn't scope it.

### D2: Model Layer Sequencing

- **Haiku**: Separates resolution (Phase 1) from data model creation (Phase 2), then discovery (Phase 3)
- **Opus**: Combines data model + resolution into a single Phase 1, then discovery in Phase 2
- **Impact**: Haiku enables independent review of the model layer before discovery logic builds on it. Opus reduces phase handoff overhead but couples two concerns.

### D3: CLI Integration Timing

- **Haiku**: CLI wiring is implicit across phases; no dedicated CLI integration phase
- **Opus**: Dedicates Phase 3 explicitly to CLI argument changes, artifact enrichment, and `to_dict()` compliance
- **Impact**: Opus's explicit CLI phase makes the Click argument migration (`WORKFLOW_PATH` → `TARGET`) a first-class deliverable with its own validation. Haiku distributes this across phases, risking late integration issues.

### D4: Timeline Estimates

- **Haiku**: 6.5 days core, 7.0 days total (deterministic single-point estimates)
- **Opus**: 7–9 days total (range estimates per phase)
- **Impact**: Haiku is more optimistic by ~1–2 days. Opus's ranges acknowledge uncertainty more honestly, particularly for Phase 1 (2–3 days vs Haiku's 1.5 days for resolution + 1.0 for models).

### D5: Test Count Specificity

- **Haiku**: References "targeted new test suite" across 5 files but no count
- **Opus**: Explicit ~37 new tests, broken down per phase (~15 + ~12 + ~5 + ~5)
- **Impact**: Opus provides a concrete testing scope that can be tracked; Haiku's test strategy is harder to verify for completeness.

### D6: Milestone Definition Style

- **Haiku**: Milestones named A–D mapped to FR families; exit criteria per phase
- **Opus**: Milestones are prose sentences per phase; no lettered milestone system
- **Impact**: Haiku's lettered milestones enable cleaner status reporting. Opus's inline milestones are more contextual but harder to reference externally.

### D7: Architecture Confirmation as Explicit Deliverable

- **Haiku**: Phase 0 produces an "approved implementation map" covering modified files, new dataclasses, CLI changes, and artifact updates
- **Opus**: No equivalent artifact; jumps directly to implementation
- **Impact**: Haiku's Phase 0 catches boundary violations before they become costly. Opus relies on the roadmap itself serving this purpose.

### D8: Risk Governance Framework

- **Haiku**: Explicit 3-tier governance (release-blocking / release-gating / managed resilience)
- **Opus**: Risk table with severity and mitigation, but no governance tier distinction
- **Impact**: Haiku's tiered governance gives release managers clearer go/no-go criteria. Opus's flat table requires interpretation.

### D9: Post-Release Observation Scope

- **Haiku**: Dedicated Phase 6 with 7 explicit observation items and 0.5-day setup estimate
- **Opus**: "Items requiring monitoring post-launch" listed in a section but no effort estimate or formal phase
- **Impact**: Haiku treats operational learning as a first-class deliverable; Opus treats it as an appendix.

### D10: Module Dependency Visualization

- **Haiku**: Text-based dependency listing in Phase 0 action items
- **Opus**: ASCII dependency graph with arrows showing direction
- **Impact**: Opus's visual graph is more immediately scannable. Minor difference in practice.

### D11: Validation Matrix Format

- **Haiku**: Narrative validation per phase with FR/NFR traceability sections
- **Opus**: Tabular SC × Phase × Method matrix
- **Impact**: Opus's matrix is faster to audit for coverage gaps. Haiku's narrative provides richer context per criterion.

### D12: Complexity Class Framing

- **Haiku**: Explicit "Complexity class: MEDIUM" with domain list and counts (risk: 6, deps: 7, validation: 12)
- **Opus**: "bounded MEDIUM-complexity extension (0.65)" with concrete scope metrics (~37 tests, 6 files, 1 new module)
- **Impact**: Opus's concrete metrics (file counts, test counts) are more actionable for sprint planning. Haiku's counts are more abstract.

## 3. Areas Where One Variant Is Clearly Stronger

### Haiku Strengths
- **Phase 0 architecture lock-in**: Prevents mid-flight boundary violations — critical for a compatibility-sensitive release
- **Risk governance tiers**: Release-blocking vs gating vs managed — actionable for release management
- **Post-release observation formalization**: Ensures OQ items don't become orphaned backlog
- **Exit criteria per phase**: Every phase has explicit "done" conditions

### Opus Strengths
- **Test count specificity**: ~37 tests with per-phase breakdown enables concrete sprint tracking
- **Explicit CLI integration phase**: Isolates the Click argument migration as its own reviewable unit
- **Validation matrix table**: Faster coverage auditing than narrative form
- **Honest timeline ranges**: 7–9 days acknowledges real uncertainty vs Haiku's point estimate of 6.5

## 4. Areas Requiring Debate to Resolve

1. **Phase 0 inclusion**: Is a formal architecture confirmation phase worth 0.5 days, or does the roadmap itself suffice? Haiku's approach is safer for teams with less context; Opus's is leaner for experienced teams.

2. **Model + resolution coupling vs separation**: Should data models land independently (Haiku Phase 1→2 split) or together with resolution (Opus Phase 1)? The answer depends on review workflow — separate PRs favor Haiku, single PR favors Opus.

3. **Timeline realism**: Haiku's 6.5 days vs Opus's 7–9 days. The resolution layer alone (6 input forms, ambiguity handling, root detection) likely warrants Opus's 2–3 day range over Haiku's 1.5 days.

4. **CLI phase isolation**: Should CLI wiring be a dedicated phase (Opus) or distributed (Haiku)? The `WORKFLOW_PATH → TARGET` change is user-facing and deserves focused testing — favors Opus's approach.

5. **Post-release phase**: Is Phase 6 (Haiku) overhead or essential? For a v2.24.1 patch release, formalized observation may be disproportionate — but the OQ items genuinely need tracking.
