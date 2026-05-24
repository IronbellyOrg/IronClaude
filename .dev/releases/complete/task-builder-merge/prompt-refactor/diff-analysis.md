# Diff Analysis — Task-Builder Convergence Orchestration Prompt

## Metadata
- Generated: 2026-05-14T06:55:00Z
- Variants compared: 3 (architect, analyzer, qa)
- Source artifact: source-prompt.md
- Total differences found: 19 (S-006, C-005, X-003, U-005, A-skipped per depth=quick)
- Depth: quick (Round 1 only; AD-2/AD-1 probes skipped)

## Structural Differences

| # | Area | Source | V1 (Architect) | V2 (Analyzer) | V3 (QA) | Severity |
|---|------|--------|----------------|---------------|---------|----------|
| S-001 | Phase 3→4 handoff | Implicit "write proposals" | Explicit Step 3.2 + `proposals/INDEX.md` manifest | Explicit `proposals/PR-NN-<slug>.md` with header | Explicit `NN-<slug>.md` + cap rule | High |
| S-002 | Precedence enforcement surface | Slogan, 5 prose mentions | `conflict-register.md` file-mediated ledger appended phase-by-phase | Citation gate G1-G5 with binary halt | State/ dir + four-case rule per proposal | High |
| S-003 | Phase 2/3 separation | Two distinct phases | Two distinct + matrices in `analysis/*.md` | Folded into one `analysis.md` | Two distinct (preserved 8-phase shape) | Medium |
| S-004 | Output subdirectories | Implicit | Explicit Phase 1 Step 1.0 creates 5 subdirs | Not explicitly enumerated | `state/` dir explicit; others implicit | Medium |
| S-005 | Invariants block | "Global Constraints" at end | Hoisted to "Precondition 0" (I0–I3) at top | Verified-only flag rule preamble | "Global Failure-Mode Contract" (G1-G7) at top | Medium |
| S-006 | Pass-batching for >10 proposals | Phrased ("batch in passes") with no merge logic | Defined: pass-N subdirs + second --compare merge | Hard cap at 10 with deterministic pair-merge | (V2 also defers to V3-style cap) | High |

## Content Differences

| # | Topic | Source | V1 | V2 | V3 | Severity |
|---|-------|--------|----|----|----|----------|
| C-001 | "task-builder wins" rule semantics | Blanket, one-sided | Operationalized via register; same blanket scope | Conditional: 5 named invariants only; rest open | Four-case rule (A authoritative, B additive, C deferred, D partial) | High |
| C-002 | Sequential thought count | "15-25 minimum" | Preserved | "outcome-bounded; stop when each row has citation" | Preserved | Medium |
| C-003 | Proposal count target | "5-8" | Preserved | "one per FINAL-REPORT mechanism + cited extras" | "5-8 with hard cap 10" | Medium |
| C-004 | /sc:reflect semantics | "verify outcomes respect rule" | Scoped prompt referencing merge-log + register | Replaced with G1-G5 citation gate (reflect optional) | Retained with retry → `--type completion` → DEGRADED | Medium |
| C-005 | Phase 7 --downstream flag | `--downstream roadmap` set | OMITTED with rationale (downstream is PRD, not roadmap) | Preserved | Preserved | High |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|---|---|---|---|---|
| X-001 | /sc:adversarial --depth | `deep` (matches source) | `standard` with conditional `deep` escalation (FINAL-REPORT §6.1 found quick + 0.81 convergence sufficient) | `deep` (matches source) | Medium — quant outcome differs |
| X-002 | /sc:adversarial --convergence | `0.80` (matches source) | OMIT (defer to protocol default) | `0.80` (matches source) + branch for sub-threshold | Medium — affects pass/fail surface |
| X-003 | /sc:adversarial --interactive | Preserved (`--interactive`) | OMITTED (batch replayable) | Preserved (`--interactive`) | Medium — affects automation contract |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---------|--------------|-------|
| U-001 | V1 | `conflict-register.md` as file-mediated precedence ledger; appended in Phase 3, consulted in Phases 5–7, cited in Phase 6 exclusions, used to filter Phase 7 revisions | High — operationalizes the slogan |
| U-002 | V1 | `SUPPORTING_INPUTS` field passed to prd skill (conflict-register + merge-log + reflect output) for traceability | Medium — improves PRD provenance |
| U-003 | V2 | Required proposal-header fields `final_report_citation` + `direction_inversion_basis` enforced as halt conditions; addresses the user-direction evidence gap | High — closes inversion-symmetry assumption |
| U-004 | V2 | Glob-and-report-absent rule for Bucket D (rf-* agents) and Bucket F (sample release specs); confirmed Bucket F is empty in this repo | Medium — prevents agent fabrication |
| U-005 | V3 | INPUT_SPEC routing fix — append release-spec path to WHAT/WHERE (fields the prd skill documents at SKILL.md:33-43); INPUT_SPEC kept as forward-compatibility | High — prevents silent ignore by prd skill |
| U-006 | V3 | Observable `## Acceptance Criteria` section per proposal (observable behavior + verification + negative criterion) propagated to Phase 7 review and Phase 8 PRD mirror-check | High — makes test plan post-hoc verifiable |
| U-007 | V3 | Global Failure-Mode Contract G1-G7 (retry budgets, halt-or-degrade artifacts, decision gates, freshness hook discipline, no-invented-flags rule, four-case conflict completion, pipeline-log tracking) | High — covers all silent-failure paths |
| U-008 | V3 | Phase 7 five-step defense process (Classify → Identify invariant → Cite FINAL-REPORT → Decide → Escalate) for expert revisions contradicting the conflict rule + rejection-rate threshold | High — defends "task-builder precedence" rule against panel drift |
| U-009 | V3 | Phase 4 explicit branch for convergence < 0.80 (exclude → retry-at-lower-depth → DEGRADED) | High — catches H-1 silent-pass failure |

## Summary
- Total structural differences: 6
- Total content differences: 5
- Total contradictions: 3
- Total unique contributions: 9
- Highest-severity items: S-001, S-002, S-006, C-001, C-005, U-001, U-003, U-005, U-006, U-007, U-008, U-009
- Variants substantially similar? NO — 19 differences across 5 categories; debate proceeds.
