# Diff Analysis: task-builder-merge Proposal Portfolio Comparison

## Metadata

- Generated: 2026-05-14
- Mode: Mode A (compare)
- Variants compared: 7 (PR-01 through PR-07 — distinct proposals to import qualities of /sc:tasklist into task-builder)
- Focus areas: structure, completeness
- Total differences found: 25 (S: 5, C: 7, X: 5, U: 5, A: 3)

**Context note**: These 7 inputs are NOT competing variants of the same artifact — they are 7 distinct proposals that together compose a portfolio. The "diff" is therefore a cross-cutting analysis of structural overlap, integration-point collisions, mechanism contradictions, and unique mechanism contributions, NOT a synonymy comparison.

**Invariant axis (load-bearing across diff)**: All 7 proposals MUST be evaluated against the 5 task-builder invariants:
1. self-contained-item (5-field schema per checklist item)
2. evidence-bound-item (file:line citation mandatory)
3. persistent-.dev/tasks/-artifact (research/qa/ persist)
4. zero-trust QA (any gap = FAIL)
5. parallel-research (rf-analyst / rf-qa partitioning)

---

## Structural Differences

| ID | Area | PR-01 | PR-02 | PR-03 | PR-04 | PR-05 | PR-06 | PR-07 | Severity |
|----|------|-------|-------|-------|-------|-------|-------|-------|----------|
| S-001 | Frontmatter shape | Standard 8-field | Standard 8-field | Standard 8-field (CASE-B "n/a-for-case-B-or-C") | Standard 8-field (CASE-B) | Standard 8-field | Standard 8-field | Standard 8-field | Low |
| S-002 | Section order | Mechanism → Adaptation → Why-not-1:1 → Invariant → Failure-modes → Sketch | Same | Same | Same | Same | Same | Same | Low |
| S-003 | Failure-modes count | 4 | 4 | 4 | 4 | 6 (highest) | 4 | 4 | Low |
| S-004 | Concrete-change sketch granularity | 2 edits, 1 check | 4 edits, 1 protocol | 5 edits | 4 edits | 5 edits | 4 edits | 3 edits | Low |
| S-005 | Length / line-count | ~55 lines | ~58 lines | ~62 lines | ~57 lines | ~67 lines (longest) | ~65 lines | ~64 lines | Low |

**Assessment**: Structural convergence is extremely high. All 7 follow the same authoring template. No structural High-severity findings — the portfolio reads as a coherent set.

---

## Content Differences (cross-cutting tensions, not redundancy)

| ID | Topic | PR-01 | PR-02 | PR-03 | PR-04 | PR-05 | PR-06 | PR-07 | Severity |
|----|-------|-------|-------|-------|-------|-------|-------|-------|----------|
| C-001 | Primary invariant claimed | evidence-bound-item | zero-trust QA | n/a (B) — reinforces zero-trust QA | n/a (B) — reinforces zero-trust QA | evidence-bound-item | zero-trust QA | zero-trust QA | Medium — invariant coverage skew |
| C-002 | Integration point in SKILL.md | :228-238, :1409-1485 (template area) | :651, :859/865/870, :1550 (retry counters) | :574-654, :872-916 (research gate, integrity gate) | :923-1000 (qualitative gate spawn) | :88-101 (tier selection) | :898-906, :1491-1507 (integrity + 15-item validation) | :961 (qualitative gate) | Medium — collision between PR-04, PR-06, PR-07 on qualitative-gate area |
| C-003 | rf-qa.md edits required | No | Yes (~310-313, monotonicity) | Yes (~50-77, partition + DNSP emission) | No (rf-qa output is INPUT to PR-04) | Yes (task-integrity check addition) | Yes (~264-287, 6 new checklist items) | No | Medium — PR-02/PR-03/PR-06 stack edits in same agent file |
| C-004 | rf-qa-qualitative.md edits | No | No | Maybe (if partitioning enabled there) | Yes (~794, passthrough) | No | No (additions live in rf-qa not rf-qa-qualitative) | Yes (~527-583, 5-axis overlay) | Medium — PR-04 and PR-07 both edit rf-qa-qualitative |
| C-005 | rf-task-builder.md edits | Edits A.9 section (~SKILL.md:719) | Yes (~336-359, per-gate fix-cycle) | No | No | No | No | No | Low |
| C-006 | New agent files | No | No | No | No | No | No | No | Low — all proposals are agent-edits, no new agents |
| C-007 | Maturity / readiness | Phase-1 quick-win (medium gain) | Phase-1 (medium-high gain, removes documented oscillation) | Phase-1 (HIGH gain — DNSP was P3 39/50 win) | Phase-1 quick-win (lowest-risk per author claim) | **Phase-2** (highest over-engineering risk; low value until 10+ done tasks) | Phase-1 (medium gain, additive) | Phase-1 quick-win (LOWEST over-engineering risk per author) | High — PR-05 is the only Phase-2 proposal in the bunch |

---

## Contradictions (cross-cutting conflicts between proposals or with task-builder invariants)

| ID | Point of Conflict | Position A (proposal) | Position B (other proposal / invariant) | Impact |
|----|---|---|---|---|
| X-001 | PR-01 "no specific file paths in task-level Execution Context header" vs evidence-bound-item invariant requiring file:line citations | PR-01: "Source areas: named modules or packages ... NEVER specific path.py:NN references at this level" (line 27) | task-builder invariant evidence-bound-item per SKILL.md:1530 rule #2 requires file:line in research/*.md and per-item Context | Medium — PR-01 confines the rule to header scope only (mitigates); but cross-validation needs rf-qa task-integrity to enforce header source-area mentions appear in per-item Context fields. Risk: header drift from body. |
| X-002 | PR-04 "inject rf-qa structural verdict into rf-qa-qualitative prompt" vs rf-qa-qualitative.md:766-775 anti-inflation rule "never mark VERIFIED from another report" | PR-04: skip mechanical re-verification of items rf-qa already PASSed (line 32) | rf-qa-qualitative existing rule: "reliance ≠ verification" | Medium — PR-04 acknowledges this (line 50) and proposes mitigation prompt language. But the operational distinction between "skip re-verification of structural facts" and "rely on another agent's verdict" is subtle and depends on careful prompt engineering. |
| X-003 | PR-02 "Halt if F_{n+1} >= F_n" monotonicity vs rf-task-builder's tolerance for legitimate slow convergence | PR-02: "monotonicity guard only fires when count does NOT shrink (not when shrinking slowly)" (line 38) | task-builder norm: multi-cycle correction tolerated when forward progress (Bucket C SKILL.md:651, 859, 865) | Low — PR-02 mitigates by saying "strictly shrink" is the trigger, which permits any forward motion. Resolution is correct but underspecified for the edge case |F_{n+1}| = |F_n| - 1 with new regression. |
| X-004 | PR-05 "advisory only" vs the practical reality that LLM-driven agents will tend to weight recent advisory framing more heavily than rule-based selection it precedes | PR-05: "rule-based tier selection in SKILL.md:96-101 always wins" (line 67) | Inversion of FINAL-REPORT §6.2 F4 hidden-input concern: in agent-exploratory paradigm, advisories influence behavior even when labeled non-binding | Medium — PR-05 acknowledges this risk (own line 60 §6.2 F4 mitigation) but offers no enforcement other than rf-qa task-integrity verifying the disclaimer text exists. Disclaimer presence != disclaimer obeyed. |
| X-005 | PR-06 TB-Add-2 "Track has >=3 and <=40 checklist items" vs PR-01 task-level Execution Context implying tasks may include compact source-area summaries that could increase total items | PR-06 (line 35): bound at 40 | PR-01 implication: source-areas + constraint summary blocks may push item count by adding "verify the constraint X" items per the rule-#16/17/18 expansion | Low — bounds are at 40 (track) and 50 (single-track), generous enough that PR-01's effect is small; the conflict is theoretical at best. Note for merge: bounds should be calibrated using current `.dev/tasks/done/` empirical data (PR-06 line 60 already notes this). |

---

## Unique Contributions

| ID | Variant | Contribution | Value Assessment |
|----|---------|--------------|------------------|
| U-001 | PR-01 | Task-level executor-readability layer for large MDTM tasks (Execution Context block with source-areas + key constraints) — does NOT exist anywhere else in task-builder | High — closes a documented "executor confusion on large tasks" gap; no other proposal addresses task-level readability |
| U-002 | PR-02 | Monotonicity guard + regression detection stop conditions (vs existing simple cap-based retry termination) | High — directly addresses documented oscillation defect (§6.2 F2: 21 retry files across 18 batches). No other proposal touches retry-loop convergence. |
| U-003 | PR-03 | Synthetic HIGH-severity finding emission on partition-agent failure (DNSP) — was the ONLY ADOPT proposal in FINAL-REPORT across 5 RF→SC ports (P3 39/50) | High — paradigm-neutral pattern transplants cleanly; turns silent failure into citable evidence. No other proposal touches partition-failure handling. |
| U-004 | PR-04 | Operational bridge between rf-qa structural verdict and rf-qa-qualitative prompt (delivers the inherited verdict that rf-qa-qualitative.md:794 already commits to consume) | Medium — makes existing rhetorical rule operational; token savings + sharper focus. Lower-novelty because the rule already exists; PR-04 is the wiring. |
| U-005 | PR-05 | Cross-task tier consistency via historical pattern reading (reads `.dev/tasks/done/` frontmatter) — no other proposal reads completed tasks at all | Low to Medium — value emerges only after `.dev/tasks/done/` accumulates ≥10 completed tasks of varied types. High latent value, low immediate value. Author explicitly marks as Phase-2. |

(PR-06 and PR-07 are intentionally not in the unique-contributions table — both are additive overlays on existing checklists rather than novel mechanisms. They strengthen but do not introduce new behavior categories.)

---

## Shared Assumptions

UNSTATED preconditions promoted as [SHARED-ASSUMPTION] diff points (per AD-2):

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| A-001 | All 7 proposals assume that `src/superclaude/skills/task-builder/SKILL.md` and `src/superclaude/agents/rf-*.md` are the correct edit surfaces — none consider whether the changes should live in `.claude/` first and be back-synced, nor address the `make sync-dev` workflow | All 7 cite SKILL.md line ranges as integration points | Medium — non-blocking for these proposals (sync-discipline applies regardless), but the merge plan must include sync-discipline in execution guidance | UNSTATED — promoted as [SHARED-ASSUMPTION] |
| A-002 | All proposals affecting QA gates (PR-02, PR-03, PR-04, PR-06, PR-07) assume rf-qa's existing "any gap regardless of severity = FAIL" stance (Bucket D rf-qa.md:140-142) continues to govern. None propose loosening this. | PR-02 line 39, PR-03 line 43-45, PR-04 line 39-40, PR-06 line 47, PR-07 line 46 | Low — assumption is congruent with zero-trust QA invariant; documenting strengthens the invariant story | UNSTATED — promoted |
| A-003 | All proposals assume the conflict-register's CASE classification (A/B/C/D per G6 four-case rule) is canonical and binding for prioritization, but none explicitly state what happens when downstream evidence contradicts a CASE classification (e.g., what if PR-05's "Phase-2" deferral becomes a Phase-1 need after evidence?) | All frontmatter uses `case:` field as if static | Low — but worth documenting for portfolio adaptability | UNSTATED — promoted |

**Classified-but-not-promoted (STATED)**:
- All proposals state and adhere to the FINAL-REPORT §6.3 "adapt intent, not implementation" lesson (stated in 7/7 frontmatter `direction_inversion_basis`).
- All proposals classify themselves as additive (no proposal removes existing behavior).

**CONTRADICTED**: None identified.

---

## Summary

- **Total structural differences**: 5 (all Low severity)
- **Total content differences**: 7 (2 High, 4 Medium, 1 Low)
- **Total contradictions**: 5 (4 Medium, 1 Low)
- **Total unique contributions**: 5 (3 High, 1 Medium, 1 Low-to-Medium)
- **Total shared assumptions surfaced**: 3 (1 Medium impact, 2 Low impact; all UNSTATED → promoted)
- **Highest-severity items**: C-001 (invariant coverage skew across portfolio), C-007 (PR-05 is the singleton Phase-2 outlier)

**Diff coverage by taxonomy level**:
- L1 (surface): S-001 through S-005 (all Low)
- L2 (structural): C-001, C-002, C-003, C-004, C-005, C-006 — primary debate axis
- L3 (state-mechanics): X-001, X-002, X-003 (retry-loop, prompt-injection, monotonicity); A-002 (zero-trust gate semantics)

L3 coverage is non-trivial (3 contradictions + 1 shared assumption), satisfying the taxonomy coverage gate without forced rounds.
