# Diff Analysis: REFACTOR-PROPOSAL Cross-Environment Comparison

## Metadata

- Generated: 2026-05-26T (Agent B, pr86 substrate)
- Variants compared: 2
  - Variant 1: `calibration-failure/REFACTOR-PROPOSAL.md` (pr86-substrate run, this environment, 30.7 KB)
  - Variant 2: `Calibration-Refactor-pr86-B/REFACTOR-PROPOSAL.md` (other environment with original T4 artifacts, 27.0 KB)
- Total differences found: 23
- Categories: structural (5), content (8), contradictions (3), unique (5), shared assumptions (2)

## Structural Differences

| #     | Area                          | Variant 1 (pr86-substrate)                                                                                   | Variant 2 (T4-environment)                                                                              | Severity |
| ----- | ----------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- | -------- |
| S-001 | Top-level organization        | Per-change deep-dives (Change A-E) with embedded diff sketches, then coverage matrix, then counter-arguments | Numbered sections: (1) Smallest closing set, (2) Schema change, (3) Hard-fail rules, (4) Out of scope, (5) Verification plan | Medium   |
| S-002 | Change count                  | 5 changes (A-E)                                                                                              | 6 changes (1-6)                                                                                          | Low      |
| S-003 | File-path convention          | `src/superclaude/...` (correctly targets source of truth)                                                    | `/config/.claude/skills/...` (targets sync-dev output — **VIOLATION of repo SoT rule**)                  | High     |
| S-004 | Diff representation           | Embedded ``` diff fenced blocks with +/- markers                                                              | Embedded markdown blocks showing new content (no -/+ diff markers)                                       | Low      |
| S-005 | Verification plan format      | Property tests P1-P5 + 6 fixtures (Change E)                                                                 | V1-V5 replay tests using original T4 cards (H1, H2, H3)                                                  | Medium   |

## Content Differences

| #     | Topic                              | Variant 1 Approach                                                                                                                                                                | Variant 2 Approach                                                                                                                                                                                          | Severity |
| ----- | ---------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- |
| C-001 | New rubric dimension               | "**Runtime check**" 6th dimension; gated-minimum formula `min(mean, evidence_grounding+0.30, runtime_check+0.30)` with verdict-direction modifier capping REFUTE@0.70, AFFIRM@0.84 | "**Claim/evidence alignment**" 6th dimension; hard cap 0.65 when alignment=0.0 (overrides arithmetic mean entirely)                                                                                          | High     |
| C-002 | Frontmatter additions              | `claim_class: static_defect \| runtime_behavior \| environment_dependent` + `verdict_direction: AFFIRM \| REFUTE \| REJECT`                                                       | `claim_class: runtime_behavior \| static_defect \| config_value \| doc_contract \| mixed` + `evidence_class: runtime_repro \| runtime_trace \| log_evidence \| source_static \| doc_static \| none`         | High     |
| C-003 | Evidence taxonomy granularity      | Evidence quality captured via `Runtime check` dimension score (0.0/0.5/1.0) referencing executed reproducer / test assertion                                                      | Evidence captured as typed `evidence_class` taxonomy + cross-tabulated with `claim_class` to score alignment dimension                                                                                       | High     |
| C-004 | Cap mechanism                      | Soft-cap via gated-minimum (M1+M2) AND verdict-direction modifier (M3a); composite still arithmetic-mean-based with caps                                                          | Hard-cap that overrides arithmetic mean entirely when alignment=0.0; multiple named caps (0.65, 0.70, 0.75) by rule number                                                                                   | High     |
| C-005 | Audit-layer enforcement            | **No equivalent change** — relies on calibrator self-application                                                                                                                  | **Change 4** adds Tier 2 calibration-completeness gate in `sc-troubleshoot-protocol/SKILL.md`; orchestrator MUST refuse to publish REPORT.md without sibling calibration artifacts; force-degrade on failure | High     |
| C-006 | Code-level enforcement             | Markdown-only proposal; no code change                                                                                                                                            | **Change 6** modifies `confidence.ts::assess()` to add Check 6 + `Math.min(score, 0.65)` cap                                                                                                                 | High     |
| C-007 | confidence-check SKILL.md          | Change D: scope-correct the "1.000/1.000" cultural-prior claim (5-line annotation) — kills rhetorical recursion                                                                   | Change 5: add 6th check "Runtime-vs-static evidence alignment" (15% weight); rebalance weights of original 5 checks                                                                                          | High     |
| C-008 | REFUTE asymmetry treatment         | Verdict-direction modifier caps REFUTE on runtime claims at 0.70 (universal rubric rule)                                                                                          | Hard-fail rule 2 + 5: REFUTE > sibling CONFIRM smell → cap 0.75; negative-existential REFUTE → cap 0.70                                                                                                       | Medium   |

## Contradictions

| #     | Point of Conflict                          | Variant 1 Position                                                                                          | Variant 2 Position                                                                                       | Impact |
| ----- | ------------------------------------------ | ----------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------ |
| X-001 | File path target                           | `src/superclaude/skills/...` and `src/superclaude/agents/...` (source of truth per CLAUDE.md project rules) | `/config/.claude/skills/...` and `/config/.claude/agents/...` (sync-dev output — should never be edited) | High   |
| X-002 | Should arithmetic mean be overridden?       | NO — keep arithmetic mean as base; impose caps via min() of gates                                            | YES — when alignment=0.0, hard-cap at 0.65 OVERRIDES mean entirely                                       | Medium |
| X-003 | Is confidence.ts a target file?            | NOT mentioned — Markdown-only proposal                                                                      | YES — Change 6 modifies `confidence.ts::assess()` directly                                                | Medium |

## Unique Contributions

| #     | Variant   | Contribution                                                                                                                                                              | Value Assessment |
| ----- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- |
| U-001 | Variant 1 | Change E: `calibrator-eval-cases.md` pin-test corpus (6 fixtures + 5 properties) gating future changes to A-C                                                              | High             |
| U-002 | Variant 1 | Migration / backward-compat table explaining v1.5 → v2.0 path with v1.0 card fail-safe defaults                                                                            | High             |
| U-003 | Variant 2 | Change 4: Tier 2 calibration-completeness audit gate — orchestrator MUST verify sibling calibration artifacts exist before publishing REPORT.md; force-degrade on failure | **High** — addresses Cause #1 (calibrator non-execution) which Variant 1 entirely omits |
| U-004 | Variant 2 | Hard-fail rule 4 (GitHub WebFetch URLs in evidence) → mark "unverifiable by spot-check"                                                                                    | Medium           |
| U-005 | Variant 2 | Verification plan replays actual H1/H2/H3 cards from the original T4 run (V1-V5)                                                                                           | High             |

## Shared Assumptions

| #     | Assumption                                                                                                                                                                              | Source Agreement                                                                                                                          | Classification | Promoted |
| ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | -------------- | -------- |
| A-001 | Calibrator should remain Read-only (no Bash); runtime evidence must be supplied by the orchestrator or referenced from the card                                                          | Both reject "give calibrator Bash" (Variant 1 explicit in Counter-args, Variant 2 implicit via Change 4 routing runtime to orchestrator)  | STATED         | No       |
| A-002 | A 6th dimension on the rubric is the right place for the runtime-vs-static gate (both agree; differ only on its name and aggregation mechanic)                                          | Both add a 6th dimension to escalation-rubric.md                                                                                          | STATED         | No       |

## Summary

- Total structural differences: 5
- Total content differences: 8
- Total contradictions: 3
- Total unique contributions: 5
- Total shared assumptions surfaced: 2 (UNSTATED: 0, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: S-003, C-001, C-002, C-003, C-004, C-005, C-006, C-007, X-001, U-003, U-005

## Key cross-environment finding

**Convergence on the 6th-dimension solution is STRONG** — both environments independently identified that adding a runtime-vs-static dimension to the rubric closes the failure mode. **Divergence is on enforcement architecture**: V1 (pr86 substrate) treats it as a calibration-formula refinement (gated-minimum), while V2 (T4 environment with original artifacts) adds an audit-layer gate (Change 4) that catches the original Cause #1 (calibrator non-execution) which V1 missed entirely.
