# Wave 1 Partition Report — A1a: Roadmap Core (v1.x–v3) — older

**Partition scope:** Evolution of the first three generations of the sc:roadmap generator (v1.4 → v2.0 → v2.02). Focus on top-level findings, post-mortems, and retrospectives.

**Methodology:** Focused-budget retry. The earlier exhaustive partition agent stalled, so this pass reads only README-class, FINDINGS-class, COMMIT-LOG-class, and one phase-class file per directory, with a hard ceiling of 25 files total.

---

## Findings

### F-A1a-001: v1.4 generator written for the wrong framework entirely

- **Type:** FAILURE
- **Pipeline step:** OTHER (spec authorship — pre-extract)
- **Symptom:** The v1.4 release directory contains a complete, fully formed roadmap-generator spec, prompt, extraction, test strategy, and a 6-milestone tasklist that were authored against IBOpenCode (`/rf:roadmap-gen`, `.opencode/command/`, `gpt-5.2`, `crossLLM`, `@rf-*` agents) instead of SuperClaude / Claude Code (`/sc:`, `.claude/skills/`, wave orchestration, Task tool). 13 of 16 files in the directory had to be archived as outdated source material, and only 5 translation-analysis files survived as canonical.
- **Root cause (claimed):** Spec was generated/imported from a sibling project and then attempted to be used in SuperClaude without a port. The retrospective file `FILE-STATUS-ANALYSIS.md` documents this explicitly via two indicator tables (IBOpenCode indicators → OUTDATED; SuperClaude indicators → CURRENT) — INFERENTIAL inference that the indicator-table framing was needed *at all* implies the project ingested a foreign spec without a gating check.
- **Remediation applied:** A separate translation workstream produced `claude-code-proposals-opencode.md` and `claude-code-proposals-framework.md` (10 + 11 translation proposals) plus `workflow-superclaude-refactoring.md` as an execution guide. The v1.4 directory itself was reorganised: 13 files moved to `archive/ibopencode-source/`, 5 SuperClaude-applicable files kept at top level.
- **Outcome:** v1.4 never shipped a working SuperClaude generator. The reorganisation prevented future contributors from accidentally implementing IBOpenCode behaviour, but the effort cost was substantial — a full spec, prompt, and 6-milestone tasklist had to be discarded.
- **Still possible today (Auggie check):** NOT CHECKED — this is a historical authorship error, not a live code path.
- **Source artifacts:** `v1.4-roadmap-gen/FILE-STATUS-ANALYSIS.md` (whole file), `v1.4-roadmap-gen/SPEC-IMPROVEMENT-PROPOSALS.md` header.

### F-A1a-002: v1.4 spec used fixed-count milestone heuristics that conflicted with observed reality

- **Type:** REMEDIATION
- **Pipeline step:** generate-opus-architect / generate-sonnet-architect (template/milestone count step)
- **Symptom:** v1.4's Proposal P2 (Inline Template Algorithm) initially proposed fixed milestone counts of 3 / 5 / 7 keyed off complexity tiers. Adversarial debate flagged "Real-world evidence shows flexibility needed (6 milestones observed for complexity 0.85)" and "Missing multi-domain resolution: No handling for co-primary domains." Original proposal also omitted required milestone sections (Type, Priority, Files Affected, Risk Level).
- **Root cause (claimed):** The initial template algorithm treated complexity as a discrete bucketing problem instead of an interpolation problem; it also assumed a single primary domain.
- **Remediation applied:** P2 was approved with MODIFY verdict (82% confidence). Fixed counts replaced by range + interpolation formula (`base_count + floor((requirement_count - 5) / 5) + (1 if domain_spread > 2 else 0)` clamped to range bounds). Multi-primary domain resolution rule added (>= 40% threshold, max 2 domain-specific milestones). Required-section list expanded.
- **Outcome:** Algorithm landed in spec but was never executed in v1.4 (see F-A1a-001). The interpolation pattern survived conceptually into v2.0's `ceil(FR_count / 4) + ceil(NFR_count / 6) + (risk_count > 5 ? 1 : 0)` formula in `refs/templates.md`.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `v1.4-roadmap-gen/SPEC-IMPROVEMENT-PROPOSALS.md` Proposal P2 (lines 71–155).

### F-A1a-003: v1.4 spec violated framework "Parallel Everything" rule

- **Type:** REMEDIATION
- **Pipeline step:** generate-opus-architect / generate-sonnet-architect (wave-step authoring)
- **Symptom:** v1.4 Section 3.4 (Wave 3 Generation) listed steps sequentially with zero parallelisation guidance. RULES.md "Parallel Everything" was the violated principle.
- **Root cause (claimed):** Author defaulted to sequential pseudocode rather than declaring dependencies.
- **Remediation applied:** Proposals P1 (declarative `concurrent_with` markers per step) and P3 (Section 3.7 consolidating wave-level parallel/sequential strategy) approved with MODIFY (81–82% confidence). Original P3 claimed 40–60% reduction; debate downgraded to realistic 30–45%. P3 also caught a real architectural constraint: Wave 4 cannot be parallel because the Task tool's AWAIT semantics force sequential agent calls.
- **Outcome:** Pattern adopted in spec but, again, never executed in v1.4. The "wave-level concurrent_with markers" idea reappeared in v2.0's "5-wave architecture" with on-demand ref loading.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `v1.4-roadmap-gen/SPEC-IMPROVEMENT-PROPOSALS.md` Proposals P1 (lines 22–69) and P3 (lines 157–235).

### F-A1a-004: v2.0 frontmatter schema contradicted itself on day one

- **Type:** FAILURE
- **Pipeline step:** wiring-verification / spec-fidelity
- **Symptom:** v2.0's `SC-ROADMAP-V2-SPEC.md` (FR-002) declared frontmatter fields `generator` and `generated`, but the v2.0 `roadmap.md` actually generated from that spec emitted `generated_by` and `generated_at`. NFR-003 simultaneously declared "Fields may be added but not removed or renamed after initial release" — meaning the spec was in conflict with its own forward-compatibility invariant the moment it was finalised. Two undocumented fields (`depth: standard`, `template: inline`) also appeared in the generated artifact with no spec backing.
- **Root cause (claimed):** Spec was written after the first roadmap had already been generated by a precursor implementation, but the spec author did not reconcile naming against the existing output. Naming convention drift between author and generator.
- **Remediation applied:** Spec Panel review flagged as C1 (CRITICAL, P0). Recommendation: pick one convention and apply everywhere. No evidence in COMMIT-LOG.md of which option was chosen, but Phase 6 (Session Persistence) work mentions a 12-field `roadmap_session` schema, suggesting the schema was rationalised during v2.0 execution.
- **Outcome:** Caught pre-implementation by the panel, so it didn't ship as a runtime bug. But it exposed the deeper pattern: spec and reference implementation evolved on different tracks and only spec-panel review forced reconciliation.
- **Still possible today (Auggie check):** NOT CHECKED — would require live grep of current `refs/templates.md` against current sc:roadmap output frontmatter. Flag for Auggie sweep in cross-cutting wave.
- **Source artifacts:** `v2.0-roadmap-v2/spec-panel-roadmap-v2-review.md` finding C1 (lines 23–52); `v2.0-roadmap-v2/COMMIT-LOG.md` File Inventory section.

### F-A1a-005: v2.0 spec declared three flags with zero behavioral contracts

- **Type:** FAILURE
- **Pipeline step:** generate-opus-architect / generate-sonnet-architect (flag-table authoring) + spec-fidelity
- **Symptom:** Three flags appeared in v2.0 spec without functional requirements: `--dry-run` was in the M7 deliverables but missing from both the formal flags table (6.2) and from any FR; `--compliance` had a description but no FR defining what compliance tiers mean for a generator (vs sc:task-unified); `--template` was partially covered in Wave 2 prose but the 4-tier discovery algorithm lived only in `refs/templates.md`, not as a testable FR.
- **Root cause (claimed):** Spec author moved algorithmic detail into refs/ (the deliberate architecture decision) but didn't backfill the spec with testable behavioural contracts for every flag. Refs document HOW; spec is supposed to document WHAT, and the WHAT was incomplete.
- **Remediation applied:** Spec Panel flagged C2 (CRITICAL, P0). FR-018 (dry-run), FR-019 (compliance, or remove), and an elevated template-discovery FR were prescribed. Phase 7 task T07.03 in `COMMIT-LOG.md` confirms `--dry-run` was wired to flags table + Wave 2 exit criteria + explicit Wave 3/4 skip conditions during execution.
- **Outcome:** Fixed during Phase 7 polish. But three flags slipping past the spec author into the deliverables-without-contracts state is a recurring class of bug — the test-fixture-driven gates in v2.02 (see F-A1a-008) are a direct response.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `v2.0-roadmap-v2/spec-panel-roadmap-v2-review.md` finding C2 (lines 56–79); `v2.0-roadmap-v2/COMMIT-LOG.md` Phase 7 section (lines 130–144).

### F-A1a-006: v2.0 Wave numbering (Wave 1A / 1B) deviated from documented framework pattern

- **Type:** REMEDIATION
- **Pipeline step:** OTHER (architecture convention)
- **Symptom:** Framework developer guide standardised on Wave 0–4. v2.0 introduced Wave 1A and Wave 1B as conditional subwaves, producing a 6-step pipeline (0, 1A, 1B, 2, 3, 4) that broke pattern conformance.
- **Root cause (claimed):** Wave 1A handles adversarial consolidation (conditional on `--specs`), Wave 1B handles extraction (always). Author preserved both as numbered subwaves rather than collapsing into "Wave 1 with two phases."
- **Remediation applied:** Spec Panel finding M1 (P2, cosmetic). Three options were debated: keep 1A/1B with documented rationale, promote to a 6-wave structure, or simplify to "Wave 1 with phases." Fowler recommended Option C (simplify). COMMIT-LOG.md however shows execution kept the 1A/1B naming — Phase 4 work explicitly says "Updated SKILL.md Wave 1A with explicit section references" and "Fixed step numbering in Wave 1A (duplicate step 3 → step 4)." Recommendation was not followed.
- **Outcome:** Deviation persisted into shipped artifact. This is a small example of a recurring class: spec-panel recommendations marked P2/P3 cosmetic often get dropped in execution-phase prioritisation.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `v2.0-roadmap-v2/spec-panel-roadmap-v2-review.md` finding M1 (lines 103–119); `v2.0-roadmap-v2/COMMIT-LOG.md` Phase 4 entry (lines 73–90).

### F-A1a-007: v2.0 quality gates caught 4 defects during execution

- **Type:** SUCCESS
- **Pipeline step:** validation (quality-engineer sub-agent runs)
- **Symptom:** Across 7 phases, three quality-engineer sub-agent runs (T04.04, T06.03-04, T07.01) caught four real defects: (1) duplicate step numbering in Wave 1A (Phase 4), (2) sc:save only triggered at completion rather than per-wave (Phase 6), (3) hash-mismatch path missing collision protocol reference (Phase 6), (4) duplicate step numbering in Wave 2 (Phase 7). All four passed after remediation.
- **Root cause (claimed):** N/A — this is the gate working as intended.
- **Remediation applied:** N/A — defects were fixed in-phase per quality-engineer feedback.
- **Outcome:** Defects 1 and 4 (duplicate step numbering) are noteworthy because the same bug recurred between Phase 4 and Phase 7. INFERENTIAL: a structural lint for "monotonic step numbering" was never added; each detection was manual-review-based. The pattern survived into v2.02 (which then needed its own structural audit tests — see T06.02 "Wave 2 Step 3 Structural Audit").
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `v2.0-roadmap-v2/COMMIT-LOG.md` Defects section (lines 205–209).

### F-A1a-008: v2.02 needed a dedicated QA remediation sprint to reach 79% QA score

- **Type:** FAILURE
- **Pipeline step:** wiring-verification + spec-fidelity (post-execution audit)
- **Symptom:** v2.02 shipped at 21/28 (75%) on the post-execution QA scorecard, below the 22/28 (79%) threshold. A whole separate remediation sprint (`fix-tasklist.md`, 12 tasks across two fix families) was required to lift the score to 28/28. Root issues were two clusters: (1) observability gaps — no `pipeline_diagnostics` block in extraction.md frontmatter to surface prereq checks, contract validation results, or fallback activation; (2) failure-injection testing — no `--resume-from` flag to feed pre-built return-contract fixtures into the pipeline, meaning consumer-defaults, missing-file-guard, YAML-parse-error, and fallback-mode warning paths were untested.
- **Root cause (claimed):** Original v2.02 sprint focused on functional correctness of the adversarial integration (skill-tool wiring, return-contract consumption, fallback protocol). It did not include observability scaffolding nor a deterministic harness for fault injection. The spec-panel critique caught the omissions only after execution.
- **Remediation applied:** `fix-tasklist.md` defined 12 tasks (T-FIX1.1–1.4 for observability, T-FIX2.1–2.8 for failure injection), creating: `pipeline_diagnostics` YAML schema (~15 lines added to refs/templates.md); two SKILL.md logging directives (Wave 1B exit + Wave 3 Step 3); `--resume-from` flag with Wave 0 validation and Wave 1A/Wave 2 skip conditions; 5 DC fixture directories (DC-1 missing fields, DC-2 null values, DC-3 missing referenced file, DC-4 malformed YAML, DC-5 fallback mode); failure-injection test prompt; manual procedures doc for the 3 cascade paths (F1, F2/F3, F4/F5) that can't be automated.
- **Outcome:** All 12 tasks marked EXECUTED COMPLETE. Net score impact projected as +7 (21 → 28). The `--resume-from` mechanism is itself a notable structural pattern — it converts the unreproducible "adversarial pipeline went sideways" failure into a deterministic test by externalising the return contract.
- **Still possible today (Auggie check):** NOT CHECKED (would benefit from Auggie sweep to verify `--resume-from` and `pipeline_diagnostics` still present in current SKILL.md / templates.md — flagging as one of the two Auggie-worthy items).
- **Source artifacts:** `v2.02-Roadmap-v3/fix-tasklist.md` (whole file, esp. lines 1–35 origin/score, 100–215 fix bodies).

### F-A1a-009: v2.02 sprint executor halted on Phase 2 with exit code -9

- **Type:** FAILURE
- **Pipeline step:** OTHER (sprint executor / orchestration)
- **Symptom:** `execution-log.md` records the v2.02 sprint started Phase 2 at 2026-02-26T05:26:23, errored 2m 39s later, exit code -9, outcome `halted`. Resume command given for `--start 2 --end 6`.
- **Root cause (claimed):** UNDOCUMENTED — the log shows only "error" status, exit -9 (typically SIGKILL on Unix, suggesting OOM kill or external termination), and no symptom text. No accompanying RCA file in the directory.
- **Remediation applied:** NONE recorded. Subsequent phase tasklists (phase-3 through phase-6) exist as fully-formed files dated May 21 (vs. April 7 for execution-log.md), suggesting the sprint was eventually completed manually outside the executor, after phase content was re-authored or migrated.
- **Outcome:** Phases 2–6 did eventually land (phase tasklist files all present and sizeable). But the original orchestrated execution failed silently; only a manual cross-check of phase-vs-execution-log timestamps reveals it.
- **Still possible today (Auggie check):** NOT CHECKED — would need Auggie sweep of sprint-executor exit handling to confirm whether exit -9 still produces a diagnostic-free log. Flagging as second Auggie-worthy item.
- **Source artifacts:** `v2.02-Roadmap-v3/execution-log.md` (whole 17 lines); directory listing showing phase-*-tasklist.md dated May 21 vs execution-log dated April 7.

### F-A1a-010: v2.02 prereq + probe gates worked as designed

- **Type:** SUCCESS
- **Pipeline step:** generate-* (Wave 0 prerequisites + probe)
- **Symptom:** Before the v2.02 sprint executed any remediation, two scoped probe tasks (T01.01 cross-skill invocation, T01.02 constraint semantics) and one prereq-validation task (T01.03 with 6 dependency checks) ran read-only and produced clean PASS results. The `SAME_NAME_BLOCKED` semantic was correctly identified — invoking a skill of the same name as the running skill is blocked, but `sc:roadmap-protocol` invoking `sc:adversarial-protocol` (different names) is permitted. This is the constraint the `-protocol` suffix naming convention was designed to dodge.
- **Root cause (claimed):** N/A — gates working as intended.
- **Remediation applied:** N/A.
- **Outcome:** The probe pattern (do a low-cost runtime check before committing to a remediation strategy) is reusable architecture. Three evidence sources were triangulated: tool description verbatim, command/skill architecture policy doc, and the live probe result.
- **Still possible today (Auggie check):** NOT CHECKED.
- **Source artifacts:** `v2.02-Roadmap-v3/probe-results.md`; `v2.02-Roadmap-v3/prereq-validation.md`.

---

## Cross-cutting patterns within this partition

- **Spec/implementation drift caught only by spec-panel-style review, not by mechanical gates.** F-A1a-004 (frontmatter naming), F-A1a-005 (flags without FRs), and F-A1a-006 (Wave 1A/1B deviation) all required a multi-expert critique to surface. None would have been caught by lint, sync-check, or test-runner. The pattern: SKILL.md/refs split is a great architecture for token economy but creates a new failure mode where spec contracts and refs algorithms can diverge silently.
- **Cosmetic / structural recommendations get dropped in execution-phase prioritisation.** F-A1a-006 (Wave 1A/1B simplification) and F-A1a-007 (recurring duplicate-step-numbering bug detected twice without a structural lint being added) both show P2/P3 recommendations losing to P0/P1 work. The bug recurrence in F-A1a-007 is the highest-cost expression — same defect appeared in Phase 4 and Phase 7.
- **First-release flag contracts are systematically under-specified.** F-A1a-005 (three v2.0 flags) and F-A1a-008 (v2.02 needed `--resume-from` invented retroactively for testability) both show flags being added to deliverables/intent before their behavioural contracts exist. The remediation pattern that worked in v2.02 — invent a fixture-driven failure-injection flag and pair it with a `pipeline_diagnostics` observability block — is generalisable.
- **Translation/portability errors are catastrophic.** F-A1a-001 (entire v1.4 spec authored for wrong framework) shows the failure mode where a precursor spec is ingested without a gating check. The cost was a discarded 6-milestone spec + tasklist. The remediation (indicator tables in `FILE-STATUS-ANALYSIS.md` distinguishing IBOpenCode vs SuperClaude markers) is post-hoc, not preventive.
- **Sprint-executor failures can land silently.** F-A1a-009 shows an exit -9 with no diagnostic text and no RCA file in the release directory; the only evidence the sprint failed mid-execution is a timestamp diff between execution-log and phase tasklists. Operationally this means "sprint completed" is not a reliable signal — manual cross-check is required.
- **Cross-skill invocation requires deliberate name-collision avoidance.** F-A1a-010 documents the `-protocol` suffix convention. This is one of the only mechanical-gate-style enforcement points in the partition — and it works because it's name-based and observable.

## Brittleness drivers identified

- **No structural lint for SKILL.md / refs/ files.** Duplicate step numbering (caught manually in Phase 4 and Phase 7 of v2.0) and Wave-numbering deviation (caught only by spec-panel) both stem from absence of automated structural checks. The lint surface is small (monotonic step numbers within a wave, wave numbering matches framework pattern, every flag in flags table has a corresponding FR section) but no such linter exists in the artefacts read.
- **Two-track evolution of spec and refs.** The SKILL.md (WHAT/WHEN) + refs/ (HOW) split is architecturally sound for token economy but creates a drift surface. Frontmatter schemas, flag contracts, and step-by-step algorithms can diverge between spec, SKILL.md, refs, and generated output. The remediation that v2.02 reached for — observability block + fixture-driven failure injection — is heavy. A lighter contract-verification gate is missing.
- **Reliance on spec-panel critique as the primary spec-quality gate.** Spec-panel review caught all the v2.0 CRITICAL findings. But spec-panel is human-effort-heavy and runs at most once per spec generation. Recurring defect classes (flag-without-FR, frontmatter-naming-drift, duplicate-step-numbering) keep slipping through because no automated rule encodes them.
- **Sprint-executor diagnostic poverty.** Exit -9 with no symptom text and no auto-generated RCA is a brittleness driver of its own — failures don't leave evidence trails, so post-mortem requires manual reconstruction from timestamps and side artifacts.
- **No prevention layer for foreign-spec ingestion.** F-A1a-001's IBOpenCode-spec-in-SuperClaude-repo error has only a post-hoc detection mechanism (indicator tables). Nothing gates a new spec at ingestion time to refuse `/rf:` or `.opencode/` markers.

## Budget note

- Files Read: 8 (v2.0/COMMIT-LOG.md, v2.0/spec-panel-roadmap-v2-review.md, v1.4/SPEC-IMPROVEMENT-PROPOSALS.md, v1.4/FILE-STATUS-ANALYSIS.md, v2.02/fix-tasklist.md, v2.02/execution-log.md, v2.02/probe-results.md, v2.02/prereq-validation.md, plus 80-line head of v2.02/phase-6-tasklist.md and a directory-listing of rollback-analysis/). Counting the partial phase-6 read as 1 file: 9 reads + 1 dir listing.
- Files Skipped (over budget, deliberately): ~50 across the three directories — including all phase-1-tasklist.md through phase-5-tasklist.md in v2.02, the SC-ROADMAP-V2-SPEC.md and SC-ROADMAP-FEATURE-SPEC.md full bodies, both extraction.md files, both test-strategy.md files, the artifacts/ checkpoints/ results/ SpecDev/ test-runs/ test-fixtures/ test-prompts/ rollback-analysis/* subtrees in v2.02, and tasklist-p1.md through tasklist-p7.md plus tasklist-overview.md in v2.0.
- Auggie lookups: 0. The two candidate items (F-A1a-008 still-present check on `--resume-from` + `pipeline_diagnostics`; F-A1a-009 sprint-executor exit-handling diagnostic poverty) were flagged in the relevant findings as NOT CHECKED but were not run because neither rose to the "must verify in this partition" bar — both are better answered in the cross-cutting Wave 2 sweep with current src/ as the search target rather than from historical release artifacts.
