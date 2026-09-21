# QA Report — Phase 4 Consolidated Findings

**Date:** 2026-09-19
**Phase:** Phase 4 gate consolidation
**Fix cycle:** N/A
**Scope:** Consolidation only; no source/task edits or phase execution. Worktree source is authoritative; peer findings are inputs, not verified facts.

## Overall Verdict: FAIL

All six confirmed findings must be resolved before Phase 4 release. This is an initial consolidated failure set, not a fix-cycle transition.

## Report inventory and origin map

All eight reports and `phase-4-gate-input.md` were read completely. Report paths below are relative to `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/qa/`.

| Report | Verdict | Submitted findings | Consolidated disposition |
|---|---|---:|---|
| qa-phase-4-structural-template.md | FAIL | 3 | ST-01 → P4-F04; ST-02 → P4-F05; ST-03 → P4-F06 |
| qa-phase-4-structural-consistency.md | FAIL | 1 | SC-01 → P4-F03 |
| qa-phase-4-structural-evidence.md | FAIL | 1 | SE-01 → P4-F01 |
| qa-phase-4-structural-completeness.md | FAIL | 2 | SC-01 and SC-02 → P4-F01 |
| qa-phase-4-content-actionability.md | FAIL | 2 | CA-01 → P4-F03; CA-02 → P4-F01 |
| qa-phase-4-content-metrics.md | FAIL | 1 | P4-CM-01 → P4-F03; its rejection of ST-02 is adjudicated below |
| qa-phase-4-content-chain.md | FAIL | 2 | CC-01 → P4-F02; CC-02 → P4-F01 |
| qa-phase-4-content-domain.md | FAIL | 1 | CD-01 → P4-F01 |

**13 submitted finding records → 6 unique confirmed findings: 2 CRITICAL, 2 IMPORTANT, 2 MINOR.** Seven duplicate records collapse; none is silently discarded. No synthetic findings. Highest submitted severity is retained within each deduplicated group. Origin-qualified IDs distinguish the two reports that independently use SC-01.

## Source and authority key

Every source coordinate below is rooted at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-generalize/src/superclaude/`, never the main checkout.

- CAL: `agents/confidence-calibrator.md` (complete Read).
- VAL: `agents/evidence-validator.md` (complete Read).
- CMD: `commands/troubleshoot.md` (complete Read).
- SKILL: `skills/sc-troubleshoot-protocol/SKILL.md` (Read 294–535 plus targeted full-file consequence search).
- AA: `skills/sc-troubleshoot-protocol/refs/agent-assertions.md` (complete Read).
- RUB: `skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (complete Read).
- Task authority: `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-troubleshoot-generalize-20260919-015257/TASK-RF-troubleshoot-generalize-20260919-015257.md`, Read 988–1081 and 2149–2238. The correction authorization and ledgers supersede incompatible historical strings; they do not authorize unrelated cleanup or early future-phase implementation.

## Issues Found

| Stable ID | Severity | Exact correction scope | Confirmed defect | Origins |
|---|---|---|---|---|
| P4-F01 | CRITICAL | SKILL Wave 5 common epilogue and step 3/inline fallback, before final report/footer/TFEP; VAL responsibility 2b is the producer contract | Structural table consequences are returned but have no explicit shared receiving step. Suggested-status/citation consumption cannot enforce structural FAIL or status-neutral removals. | structural-evidence SE-01; structural-completeness SC-01/SC-02; content-actionability CA-02; content-chain CC-02; content-domain CD-01 |
| P4-F02 | CRITICAL | SKILL Wave 1.7 fallback/exit, Wave 3 step 3.5 and Tier 2 calibration-completeness failure ladder; downstream disk calibration inputs | Audit-only inline calibration can be replaced by min(self_reported, 0.65), increasing a C6-capped 0.30 to 0.65 and leaving no normal calibration artifact for later consumers. | content-chain CC-01 |
| P4-F03 | IMPORTANT | VAL Status Decision success/partial bullets, aligned with responsibility 2b | Zero dropped citations still independently defines success despite structural partial/blocked/FAIL. | structural-consistency SC-01 (MINOR); content-actionability CA-01 (IMPORTANT); content-metrics P4-CM-01 (IMPORTANT) |
| P4-F04 | MINOR | CAL fenced Output Format, conditional Structural assertions section | Required canonical per-rule table is absent from the declared report template, although step 5b requires it. | structural-template ST-01 |
| P4-F05 | MINOR | CAL Confidence → Formula applied output description only | Displayed derivation stops at verdict modifier and omits structural caps/adjusted-dimension provenance. Scoring procedure itself is correct. | structural-template ST-02; content-metrics rejection explicitly adjudicated below |
| P4-F06 | IMPORTANT | CAL Escalation recommendation → Rubric rule fired provenance slot and restriction note | C1-forced ESCALATE cannot honestly be attributed solely to the first matching rubric rule when that rule is a hard STOP. | structural-template ST-03 |

### P4-F01 — Consume structural consequences, not just their table

**Verified chain:** VAL:64–65 evaluates rules and returns recommendations without editing inputs; VAL:102–108 serializes them. SKILL:479–481 materializes inputs, dispatches, persists the result, merges its three-value status and removes dropped citations. SKILL:484–515 then finalizes footer/return/publication. Full-file Grep for structural/revalidation paths found no shared post-return structural disposition. Earlier composition at SKILL:465/478 is not consumption of an independent validator's newly discovered result.

**Witnesses:** (a) All citations verify; a later-run unquoted reference `a or b` fires A6, structural FAIL plus suggested partial. Zero drops still permits ordinary partial publication along the enumerated caller steps. (b) A7: producer row exists while RUN-SITE remains pending-producers; same failure. (c) Invalid non-citation timestamp fires A3 with zero drops: citation removal does not remove the line. (d) Actual reference-arm mismatch fires A9 without a status contribution: the returned suspect/outcome-table suppression needs application. (e) A8's blocked suggestion alone does not render its required CI-unobserved Diagnosis.

**Required correction:** One shared post-validation step for agent and inline results, inspecting every fired consequence before publication. A6/A7 require repair plus revalidation or explicitly failed diagnostic disposition with invalid causal claims suppressed; do not simply ship a normal partial/blocked diagnostic. Apply A3 line removals, A8 Diagnosis and A9 suspect/Grounding Gap/outcome-table suppression independently of citation count. Consume all other contributed outcomes as well. Then derive report/footer/TFEP from the same monotone status. Retain validator success/partial/blocked; FAIL remains a separate structural result and the orchestrator owns failed. Test combined A6/A7+A8 and prior failed/blocked cases, including inline fallback. All these are one missing receiving-stage defect, not separately counted symptoms.

### P4-F02 — Preserve calibration through the Tier 2 failure ladder

**Verified chain:** CAL:68 and AA:25 require final confidence ≤0.30 when C6 fires. SKILL:303/305 explicitly permits inline audit output instead of a calibration file. SKILL:368 inherits that fallback per Tier 2 card. SKILL:376–380 requires a sibling report and, after one failed retry, explicitly replaces confidence with min(self_reported, 0.65). SKILL:480 supplies calibration artifact paths to validation; SKILL:482 says calibration reports are consumed from disk.

**Witness:** Self-report 0.95; supplied tasklist location resolves a bracket artifact lacking required bracket evidence; C6 fires and inline calibration computes 0.30. Inline audit-only completion leaves the sibling absent. Retry fails. The prescribed terminal assignment is min(0.95, 0.65)=0.65, which violates the active cap and can also lose a final-score C1 recommendation for a definite enum headline. This is a reachable source-contract path, not a claim of observed agent execution. The existing failure ladder becomes in-scope because it overwrites a newly required structural result.

**Required correction:** Persist inline calibration at the normal per-card calibration output path using the agent report schema, structural rows, final score and recommendation. Both tiers and later validation consume that artifact. Align completeness/retry handling so no degradation branch increases a known calibrated score or discards fired caps/C1. If valid calibration cannot be produced, retain explicit failure/provenance and use a conservative disposition that cannot bypass the applicable structural constraints; do not claim successful calibration from a self-report. Keep the one-retry policy unless a separately verified necessity requires alteration. Witness successful-agent C6, inline C6, retry exhaustion, C7/C8 stricter score preservation, and C1 with quick/no-escalate suppression.

### P4-F03 — Status Decision has overlapping success/non-success predicates

**Evidence:** VAL:119 says success means zero dropped citations; VAL:120 also allows structural partial, while VAL:65 prohibits success on structural FAIL and specifies A8 precedence. The safe rule exists, but the dedicated decision summary is inconsistent. Highest origin severity IMPORTANT retained; this is contradictory guidance, not proof of an actual false-success run.

**Correction and witnesses:** Qualify success as zero drops AND no structural partial/blocked/FAIL contribution. Explicitly carry responsibility 2b's FAIL mapping into Status Decision: blocked if A8, otherwise partial, with the separate repair/failed disposition consumed under P4-F01. Zero drops + A1 → partial; + A6 → partial with structural FAIL; + A6+A8 → blocked with structural FAIL; legacy zero drops without assertions → success. No fourth validator status value.

### P4-F04 — Calibrator report template omits its required rule table

**Evidence:** CAL:68 requires the canonical Structural assertions table; CAL:73–124's fenced template contains none. AA:31–33 requires the same five-column shape for both agents. Surrounding instructions establish evaluation, so this is a template completeness defect, not missing C-rule logic.

**Correction and witnesses:** Add a conditional Structural assertions section to the existing fence, generic placeholder row and canonical reference, covering C1–C8 with C3b after C3, including skipped rows. Do not duplicate trigger definitions. With assertions supplied, nine C-rule rows must be representable; without assertions, retain explicit skipped/default behavior and legacy optional compatibility.

### P4-F05 — Displayed derivation is incomplete, not a broken formula

**Dispute adjudication:** Content-metrics explicitly rejects a separate defect because CAL:103's structural_flags row explains caps. That observation is correct and prevents classifying this as a scoring failure. Nevertheless CAL:109 labels a formula as the applied derivation while stopping after the verdict modifier; it does not identify itself as the base formula or refer to the final structural minimum. The template's display remains incomplete relative to the newly required final value. Retain structural-template ST-02 as MINOR, not a second cap-enforcement issue.

**Witness:** Adjusted dimensions all 1.0, no verdict modifier, C6 fires. The displayed line evaluates to 1.00; actual required reported confidence is 0.30. CAL:68 and the trace remain correct.

**Correction:** Change only surrounding output explanation: the formula uses assertion-adjusted dimensions, then verdict modifier, then minimum with all fired structural caps. Alternatively explicitly label this line as the base derivation and point to the structural finalization. Preserve RUB's formula verbatim. Verify the displayed derivation explains both uncapped 1.00 and capped 0.30 without suggesting caps raise lower scores.

### P4-F06 — Forced recommendation needs honest provenance

**Evidence and witness:** CAL:68 makes final-score C1 ESCALATE non-overwritable. CAL:116 permits only a quote from RUB's Escalation Decision as the fired-rule source. RUB:54–58 first matches STOP for no-escalate/quick. For a definite headline at 0.30 with no-escalate, the recommendation is forced ESCALATE while actual fan-out remains suppressed. A hard-STOP quote cannot honestly be its forcing source; a later low-confidence rubric quote is not the first matching rule.

**Correction:** Preserve the existing output marker if needed for compatibility, but permit canonical C1 as recommendation provenance and separately state the matching rubric restriction that suppresses actual escalation. Do not change protected Will Not text, add a CLI flag, weaken user restrictions, or invent a new reason enum to solve a provenance-only defect. Verify C1 with no-escalate, quick and unrestricted standard, plus an ordinary no-C1 rubric decision.

## Overlap and scope decisions

| Dispute or candidate | Resolution |
|---|---|
| Several lenses PASS caller-interface existence while others FAIL publication enforcement | Both describe different depths. Inputs and table-producing instructions exist; source trace confirms missing explicit consumption. P4-F01 prevails for behavioral liveness, not an allegation of absent evaluation. |
| A6/A7 FAIL and A3/A9 edits split across reports | One missing post-validation consequence consumer; merge as P4-F01, preserve every witness and highest CRITICAL severity. Fixing only the FAIL branch does not close it. |
| Structural-consistency rates status summary MINOR; actionability/metrics IMPORTANT | Keep IMPORTANT in P4-F03 under highest-severity merge. Explicit safe rule is acknowledged. |
| ST-02 versus metrics rejection | Retain only the bounded MINOR display defect P4-F05; reject any claim that the scoring algorithm lacks cap/recompute logic. |
| Tier 2 ladder predates Phase 4 | Do not reopen its unrelated historical weaknesses. The new C6 result being increased and structural output lost is a directly demonstrated integration defect, P4-F02. |
| CAL missing table versus table instruction | Instruction exists; template incompleteness remains P4-F04. Not a claim that all emitted reports necessarily omit rows. |
| Baseline Wave 1/five-dimension prose, old verdict_cap table escaping, unrelated rubric or E4 issues | Excluded. No correction authorization inferred for unrelated baseline cleanup. |
| Historical input/reason counts and exact-string tests | Superseding ledgers govern: no finding for twelve VAL input bullets, nine reasons, or approved semantic replacements. |
| Pending Phase 7 harness | Not missing Phase 4 work. Recommend future acceptance additions, do not execute now. |

## Downstream override recommendations

These are recommendations for the authorized serialized correction/ledger pass, NOT task edits or newly executed phases. Preserve original checklist history and historical research; record supersession rather than restoring obsolete strings.

| Finding | Existing task/consumer surface | Recommended acceptance override |
|---|---|---|
| P4-F01 | 4.6–4.10 plus existing SKILL Wave 5 receiving seam; scheduled 7.2, 7.8, 7.10, 7.11, 7.33, 7.43, 7.46 | Table production/parity alone is insufficient. Add agent/inline consumer witnesses for zero-drop FAIL, non-citation line removal, reference mismatch suppression, CI Diagnosis and final report/footer/TFEP agreement. No normal publication before structural disposition. |
| P4-F02 | 4.4–4.5 and existing SKILL calibration/failure consumers; scheduled 7.2 and 7.46 | Inline calibration must materialize the normal artifact and survive completeness/retry/validator consumption. Supersede any min(self_reported, 0.65)-only expectation that raises a stricter computed score. Add failure-path witnesses, not just evaluator flag equality. |
| P4-F03 | 4.6–4.10; scheduled 7.33/7.43/7.46 | Replace unqualified zero-drop success predicate with contribution-aware decision matrix; retain suggested enum and monotone final status. |
| P4-F04/F05/F06 | 4.1–4.5; scheduled 7.2/7.44/7.46 where applicable | Complete report shape, derivation and forced-recommendation provenance override stale exact-template expectations. Keep canonical cite-not-copy discipline, immutable base formula, optional inputs and hard execution restrictions. |

Minimum correction footprint is CAL, VAL and the existing SKILL consumer/fallback seams. No command change is justified by this merged finding set. Do not add new frameworks, command flags, unrelated source fixes or early Phase 7 files. Any subsequent fixer must verify actual test-item content before implementing these recommendations; this consolidation verifies their headings and relevant ledger mappings, not future test implementation.

## Items Reviewed

This is a consolidation-specific checklist, not a claim to have re-run all 80 peer lens checks.

| # | Check | Result | Direct evidence |
|---|---|---|---|
| 1 | Complete report inventory and authority | PASS [x] VERIFIED | Glob returned exactly the eight requested peer reports before output creation; all eight and gate input fully Read; task Phase 4/ledgers Read. |
| 2 | Deduplication and origin/severity preservation | PASS [x] VERIFIED | Full peer Reads yield 13 records; origin map preserves all in six groups with max severity. |
| 3 | Validator-to-caller consequence liveness | FAIL [x] VERIFIED | VAL full Read; SKILL 294–535 Read and full-file consequence Grep; P4-F01. |
| 4 | Calibration fallback/completeness/cap preservation | FAIL [x] VERIFIED | CAL/AA full Reads; SKILL 303–305, 368, 372–382 and 480–482; P4-F02 numeric witness. |
| 5 | Status decision coherence | FAIL [x] VERIFIED | VAL full Read plus fresh 117–122 Read versus responsibility 2b; P4-F03. |
| 6 | Calibrator output shape, derivation and provenance | FAIL [x] VERIFIED | CAL full/focused Reads; AA and RUB full Reads; P4-F04–F06. |
| 7 | Disputed overlaps and scope boundary | PASS [x] VERIFIED | Peer disagreement read directly; all three outputs and source seams checked against gate/ledger scope. No unrelated baseline promoted. |
| 8 | Downstream recommendation linkage and report persistence | PASS [x] VERIFIED | Task Phase 4/ledgers Read, planned-test heading Grep; incremental Write/Edit and final report readback. |

## Summary and confidence

- Checks passed: 4 / 8; checks failed: 4 / 8.
- Confirmed findings: 6 (CRITICAL 2; IMPORTANT 2; MINOR 2).
- Issues fixed in-place: 0. No source/task edits, phase execution, runtime tests, sync, staging or commits.
- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 22 | Grep: 2 | Glob: 1 | Bash: 0.
- Counts include report initialization/incremental/final readbacks; source/report verification alone exceeds the eight-check engagement minimum. No web lookup needed or performed.
- UNCHECKED items: none in the consolidation checklist. UNVERIFIABLE items: none in this static contract review.
- Confidence measures checklist coverage, not likelihood that runtime agents obey Markdown instructions. Witnesses are source-level execution simulations, not executed agent incidents. Peer PASS counts were not inherited as independent verification.

## Actions Taken

Created only this requested report with a header, appended inventory/findings and adjudication incrementally, then read it back. Read all eight inputs, gate authority, current worktree outputs and actual callee/caller/fallback contracts. Preserved origin identities, retained highest severities, bounded contested minor findings and excluded unrelated baseline. No corrections were applied outside this report.

## Recommendations

Resolve P4-F01–P4-F06 through the authorized serialized correction process, recording any necessary acceptance supersessions without rewriting history. Re-review all listed witnesses and retain these stable IDs across cycles. The initial failure set has cardinality 6; future regression/monotonicity decisions must compare verified stable-ID dispositions, not the raw 13 peer records. No Phase 4 release is warranted yet.

## QA Complete
