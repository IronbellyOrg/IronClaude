---
high_severity_count: 0
medium_severity_count: 5
low_severity_count: 3
total_deviations: 8
validation_complete: true
tasklist_ready: true
---

## Deviation Report

### DEV-001
- **ID**: DEV-001
- **Severity**: MEDIUM
- **Deviation**: Roadmap Phase 3 bundles deliverables from spec's Phase 2 (Structural Audit) and Phase 3 (Cross-Reference Synthesis) into a single implementation phase, obscuring the spec's distinct agent boundaries
- **Spec Quote**: "Phase 2: Structural Audit [Source: Set B ss5] Agent: audit-analyzer (Sonnet, parallel instances)" and "Phase 3: Cross-Reference Synthesis [Source: Set B ss5, HYBRID C-10] Agent: audit-comparator (Sonnet)"
- **Roadmap Quote**: "Phase 3: Depth — Evidence, Cross-Reference, and Docs ... 1. Evidence-mandatory KEEP for Tier 1-2 ... 4. 3-tier cross-reference synthesis"
- **Impact**: Implementers may conflate audit-analyzer and audit-comparator agent responsibilities, since the roadmap groups their deliverables together without maintaining the spec's clear agent-to-phase mapping
- **Recommended Correction**: Add explicit notes in Phase 3 deliverables indicating which items map to the spec's execution Phase 2 (audit-analyzer) vs Phase 3 (audit-comparator) to preserve agent boundary clarity

### DEV-002
- **ID**: DEV-002
- **Severity**: MEDIUM
- **Deviation**: Roadmap omits the Phase 1 scanner output files `pass1-summary.json` from deliverables description
- **Spec Quote**: "Outputs per batch: `.claude-audit/run-{timestamp}/phase1/batch-{NN}-{domain}.json` `.claude-audit/run-{timestamp}/phase1/pass1-summary.json`"
- **Roadmap Quote**: "Standardized Phase 1 scanner schema — simplified JSON schema for Haiku scanners (path, risk_tier, classification, evidence_text, credential_scan)"
- **Impact**: The pass1-summary.json artifact is consumed by Phase 2 as an input. Without explicit mention, implementers may only produce per-batch files and miss the aggregation step
- **Recommended Correction**: Add pass1-summary.json (and other per-phase summary files: pass2-summary.json, pass3-summary.json) as explicit deliverables in their respective roadmap phases

### DEV-003
- **ID**: DEV-003
- **Severity**: MEDIUM
- **Deviation**: Roadmap does not mention the Phase 1 credential scanning priority-ordered enumeration sequence
- **Spec Quote**: "Priority-ordered enumeration: `.env.production` -> `.env.prod` -> `.env` -> `.env.local` -> `.env.staging` -> `.env.test` Skip templates: `.env.example`, `.env.template`, `.env.sample`"
- **Roadmap Quote**: "Credential file scanning — priority-ordered `.env*` enumeration, real vs template pattern detection, configurable pattern list, never print credential values, include security-audit disclaimer"
- **Impact**: Low — the roadmap references priority-ordered enumeration but doesn't specify the exact sequence. Implementers would need to consult the spec for the ordering, which is the expected workflow
- **Recommended Correction**: No action required; the roadmap correctly references the behavior and the spec is the authoritative source for implementation detail

### DEV-004
- **ID**: DEV-004
- **Severity**: MEDIUM
- **Deviation**: Roadmap's Phase 4 lists "Subagent failure handling" but the spec places this as a cross-cutting Quality Gate concern (Section 10), not a Phase 4-specific deliverable
- **Spec Quote**: "Subagent Failure Handling [Source: FLAW CS-04] Per-subagent timeout: 120 seconds, Max retries: 2 (with exponential backoff) ... Cascading failure detection: If 3 consecutive batches fail, pause execution"
- **Roadmap Quote**: "Phase 4: Quality, Polish, and Consolidation ... 6. Subagent failure handling — per-subagent timeout (120s), max 2 retries with backoff, cascading failure detection (3 consecutive → pause), minimum viable report (50%+ batches required)"
- **Impact**: Subagent failure handling must be operational from Phase 1 onward (when parallel scanners first run), not deferred to Phase 4. Deferring it means Phases 1-3 have no failure recovery
- **Recommended Correction**: Move subagent failure handling to Phase 1 or Phase 0 as infrastructure that must be in place before parallel scanning begins

### DEV-005
- **ID**: DEV-005
- **Severity**: MEDIUM
- **Deviation**: Roadmap's Phase 4 lists budget controls (AC9) as a quality gate, but budget controls with graceful degradation are specified as a Phase 3 deliverable in the roadmap itself, creating a validation gap for Phases 0-2
- **Spec Quote**: "When budget pressure activates (phase reaches 90% of allocation): First cut: Skip Tier 4 ... Never cut: Phase 0 profiling, Phase 1 Tier 1-2 scanning, Phase 4 consolidation"
- **Roadmap Quote**: "Phase 3: ... 10. Budget controls with graceful degradation" and "Phase 4 Quality Gates: AC9 (budget control)"
- **Impact**: Budget control is validated in Phase 4 but implemented in Phase 3. The `--budget` flag and basic token tracking should be implemented earlier (Phase 0/1) to prevent overruns during development
- **Recommended Correction**: Split budget controls: basic token tracking and `--budget` ceiling enforcement in Phase 0, graceful degradation logic in Phase 3 as currently placed

### DEV-006
- **ID**: DEV-006
- **Severity**: LOW
- **Deviation**: Roadmap omits the "clean report" template for repos with zero significant findings
- **Spec Quote**: "R18 | 'Clean repo' output | LOW | Define a 'clean report' template that positively confirms repo health when there are zero significant findings"
- **Roadmap Quote**: [MISSING]
- **Impact**: Low — this is a LOW-severity risk item in the spec and primarily affects UX for healthy repos
- **Recommended Correction**: Add as a minor deliverable in Phase 4 (consolidation/report generation)

### DEV-007
- **ID**: DEV-007
- **Severity**: LOW
- **Deviation**: Roadmap omits the spec's explicit mention of non-English documentation handling (R11) and non-markdown format support (R12) from deliverables
- **Spec Quote**: "R11 | Non-English documentation | MEDIUM | Acknowledged limitation. UTF-8 handling required." and "R12 | Non-markdown documentation formats | MEDIUM | v2 supports `.md` first-class, `.rst` best-effort."
- **Roadmap Quote**: "Non-English documentation (R11) | Broken reference detection fails | UTF-8 handling required; full multilingual out of scope"
- **Impact**: The roadmap lists these as risks but doesn't assign them as deliverables to any phase. UTF-8 handling should be a Phase 1 correctness concern
- **Recommended Correction**: Add UTF-8 handling and `.rst` best-effort support as minor deliverables in Phase 1

### DEV-008
- **ID**: DEV-008
- **Severity**: LOW
- **Deviation**: Roadmap does not reproduce the spec's detailed output directory structure showing all intermediate artifacts
- **Spec Quote**: Section 9 shows full directory tree including `phase0/static-analysis/`, `phase2/docs-audit/`, `phase4/consolidation-log.json`, `phase4/directory-assessments.json`
- **Roadmap Quote**: [MISSING — roadmap references output files in deliverables but doesn't provide the consolidated directory structure]
- **Impact**: Minor — implementers will refer to the spec's Section 9 for the canonical directory layout
- **Recommended Correction**: No action required; the spec is the authoritative source for directory structure

## Summary

The roadmap is a faithful representation of the specification with **0 HIGH**, **5 MEDIUM**, and **3 LOW** severity deviations. No functional requirements, data models, CLI options, or architectural constraints are missing or contradicted.

The MEDIUM deviations are primarily about **implementation sequencing** rather than missing content:
- **DEV-001**: Spec execution phases 2-3 are merged into a single roadmap phase, blurring agent boundaries
- **DEV-002**: Per-phase summary artifacts not explicitly listed as deliverables
- **DEV-004/DEV-005**: Cross-cutting infrastructure (subagent failure handling, budget tracking) is deferred to later phases when it should be available from the start of parallel execution

The roadmap is **tasklist-ready** — these sequencing concerns can be addressed during tasklist generation without requiring roadmap revision.
