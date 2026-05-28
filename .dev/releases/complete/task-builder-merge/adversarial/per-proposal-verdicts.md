# Per-Proposal Verdicts (Phase 4 G3 supplementary artifact)

One section per proposal with case, scores, verdict, strengths/weaknesses, invariant findings, rationale.

---

## PR-01: execution-context-header

- **CASE**: D
- **quant_score**: 0.890
- **qual_score**: 0.933
- **combined_score**: 0.912
- **verdict**: REVISE
- **debate-derived strengths**:
  - Unique value: no other proposal addresses task-level executor readability (U-001, debate-transcript per-point matrix 88% confidence)
  - Scope-confinement design preserves evidence-bound-item invariant (proposal line 34; PR-01 Round-1 strength #2)
  - Optional behavior degrades gracefully when BUILD_REQUEST minimal (proposal failure-mode #2)
  - Cross-validation via rf-qa task-integrity check (proposal line 54) closes header-drift gap
- **debate-derived weaknesses**:
  - rf-qa task-integrity cross-validation check structurally overlaps PR-06's TB-Add catalogue (Round-2 PR-01 rebuttal concession)
  - Does not acknowledge sync-discipline (A-001 UNSTATED shared assumption); D5.4 NOT MET in qualitative scoring
  - No structural test that proves "no specific paths" rule is confined to header (INV-015 MEDIUM)
- **invariant-probe findings affecting this proposal**: INV-008 ADDRESSED (LOW), INV-011 ADDRESSED (LOW), INV-014 ADDRESSED (LOW), **INV-015 UNADDRESSED MEDIUM** (scope-confinement structural test missing)
- **rationale**: Score (0.912) clears the 0.75 ADOPT threshold, but INV-015 MEDIUM invariant concern requires a new acceptance criterion (TB-Add-8: "Every per-item Context field referencing a code surface includes file:line citation or justified absence comment") before adoption. With that criterion in the refactor plan, PR-01 is effectively ADOPT-with-revision. Cross-validation check (PR-01 failure-mode #4) is absorbed into PR-06 as TB-Add-7.

---

## PR-02: retry-monotonicity-guards

- **CASE**: D
- **quant_score**: 0.929
- **qual_score**: 1.000
- **combined_score**: 0.965
- **verdict**: ADOPT
- **debate-derived strengths**:
  - Highest combined score in portfolio (0.965)
  - Perfect qualitative score (30/30) — only PR-02 and PR-06 reach this
  - Addresses documented oscillation defect (FINAL-REPORT §6.2 F2: 21 retry files / 18 batches empirical pattern; U-002 90% confidence)
  - Conservative thresholds preserve legitimate multi-cycle correction (proposal line 38)
  - Independent counters preserved (proposal line 53)
  - Strengthens zero-trust QA strictly (proposal line 41; debate-transcript Round-1 strength #2)
- **debate-derived weaknesses**:
  - Race-between-guards case was underspecified in original proposal (concession line 49); resolved in Round-2 rebuttal (regression > monotonicity precedence rule)
  - Composition with PR-03 (synthetic findings as failure-count input to monotonicity) was unaddressed in original proposal (INV-012 MEDIUM)
- **invariant-probe findings affecting this proposal**: INV-001 ADDRESSED (LOW, independent counters), INV-005 ADDRESSED (LOW, strict `>=` comparison correct), **INV-012 UNADDRESSED MEDIUM** (PR-02 + PR-03 composition)
- **rationale**: Highest score in portfolio. Surgical, additive design; addresses a specific documented defect with conservative thresholds. INV-012 MEDIUM is addressed in refactor plan acceptance criterion #5 specifying synthetic-finding dedup-key behavior under monotonicity.

---

## PR-03: dnsp-synthetic-finding (BASE)

- **CASE**: B
- **quant_score**: 0.951
- **qual_score**: 0.967
- **combined_score**: 0.959
- **verdict**: ADOPT (BASE)
- **debate-derived strengths**:
  - **Strongest external evidence in portfolio**: P3 39/50 — the ONLY proposal across 5 RF→SC ports to win without revision (proposal line 8; U-003 92% confidence; debate Round-1 by 6/7 advocates as steelman point)
  - CASE-B no-conflict classification: lowest portfolio-integration friction (frontmatter line 12)
  - Reinforces TWO invariants simultaneously (zero-trust QA + evidence-bound-item per proposal lines 43-44; C-001 88% confidence)
  - Parallel-research invariant explicitly load-bearing (proposal line 47)
  - All-agents-fail guard preserves existing escalation (proposal line 35; INV-004 ADDRESSED)
- **debate-derived weaknesses**:
  - Dedup specification was one sentence in original proposal (failure-mode #4); resolved in Round-2 rebuttal (`(assigned_files_range, escalation_ladder_exhaust_point)` key)
  - "Synthetic finding masks a real issue" risk acknowledged (failure-mode #3); mitigation via HIGH severity + zero-trust gate behavior
- **invariant-probe findings affecting this proposal**: INV-004 ADDRESSED (LOW), INV-007 ADDRESSED (LOW), INV-016 ADDRESSED (LOW), INV-021 ADDRESSED (LOW). Composition concern INV-012 MEDIUM is attributed to PR-02 (this proposal's role is passive — emits the synthetic; PR-02 consumes it in monotonicity logic).
- **rationale**: Selected as BASE by combined score + Level-1 tiebreaker (debate-performance: 4 high-confidence per-point wins, highest in portfolio). Paradigm-neutral pattern transplants cleanly. Lowest portfolio-integration friction.

---

## PR-04: gate-results-passthrough

- **CASE**: B
- **quant_score**: 0.901
- **qual_score**: 0.967
- **combined_score**: 0.934
- **verdict**: ADOPT
- **debate-derived strengths**:
  - Operationalises existing stated rule (rf-qa-qualitative.md:794 — proposal lines 9-10; U-004 78% confidence)
  - Lowest implementation risk among CASE-B proposals (frontmatter line 14)
  - Token savings + sharper semantic focus (proposal line 14)
  - Anti-inflation rule strengthened with specific prompt language (proposal line 50)
- **debate-derived weaknesses**:
  - X-002: anti-inflation rule "reliance ≠ verification" requires careful prompt engineering with no test (Round-2 rebuttal concession)
  - Coupled to PR-06 sequencing (INV-010 MEDIUM): inherited verdict richens only when PR-06's TB-Add items are live
  - INV-002 MEDIUM: verdict re-injection on subsequent fix cycles not explicitly specified
- **invariant-probe findings affecting this proposal**: **INV-002 UNADDRESSED MEDIUM** (verdict re-injection), **INV-010 UNADDRESSED MEDIUM** (sequencing with PR-06), INV-013 ADDRESSED (LOW, axis-overlay composition), INV-019 ADDRESSED (LOW, anti-inflation preserved)
- **rationale**: Score (0.934) clears the 0.75 ADOPT threshold; 2 MEDIUM invariant concerns addressed via refactor plan acceptance criteria (#3 INV-002 re-injection mandate; #3 INV-010 dynamic checklist enumeration; #3 INV-019 Self-Audit acceptance criterion). Lands third in sequencing order.

---

## PR-05: tier-history-advisory

- **CASE**: D
- **quant_score**: 0.857
- **qual_score**: 0.867
- **combined_score**: 0.862
- **verdict**: REVISE (Phase-2 deferral)
- **debate-derived strengths**:
  - Most comprehensive failure-mode analysis (6 modes; S-003 60% confidence)
  - Frontmatter-only reading avoids privacy/leakage (proposal line 60)
  - Honest Phase-2 framing acknowledges premature adoption risk (proposal lines 12, 61)
  - Advisory MUST cite specific historical task file paths — itself evidence-bound (proposal line 49)
- **debate-derived weaknesses**:
  - X-004: Disclaimer presence ≠ disclaimer obeyed; LLM agents weight recent framing (Round-2 rebuttal concession)
  - Volume-dependency: "LOW immediate value until 10+ done tasks exist" (proposal line 61)
  - D4.1, D4.2 NOT MET in qualitative scoring (Phase-2 hedge introduces conditional language inherent to proposal nature)
  - D6.2 NOT MET (advisory state vs rule-based state interaction not formally modeled)
  - Lowest combined score in portfolio
- **invariant-probe findings affecting this proposal**: **INV-003 UNADDRESSED MEDIUM** (advisory operational obedience cannot be structurally enforced), INV-009 ADDRESSED (LOW, empty `.dev/tasks/done/` handled), INV-017 UNADDRESSED LOW (historical file staleness), INV-020 ADDRESSED (LOW, advisory-only rule documented)
- **rationale**: Score (0.862) clears 0.75 ADOPT threshold numerically, BUT INV-003 MEDIUM concern (advisory obedience) is structurally unaddressable in agent-exploratory paradigm — author's own Phase-2 framing is the strongest evidence the proposal should defer. Re-evaluation trigger explicit: `.dev/tasks/done/` ≥10 completed tasks of ≥3 distinct task_types. Verdict REVISE = defer to Phase-2; do NOT land in Phase-1 portfolio.

---

## PR-06: structural-gate-additions

- **CASE**: D
- **quant_score**: 0.926
- **qual_score**: 1.000
- **combined_score**: 0.963
- **verdict**: ADOPT
- **debate-derived strengths**:
  - Second-highest combined score (0.963; differs from PR-02 by 0.002)
  - Perfect qualitative score (30/30)
  - CB-3 per-check classification (proposal line 41) — traceable to source check IDs (sc:tasklist checks 11/13/14/15/16/17)
  - Additive, never subtractive (proposal line 49); zero-trust QA strengthened
  - Self-contained-item reinforcement: TB-Add-1 placeholder scan enforces 5-field schema (proposal line 50)
  - Migration path documented (failure-mode #2)
  - Most numeric thresholds in portfolio (D4 SR=0.90)
- **debate-derived weaknesses**:
  - TB-Add-2 bounds (≥3, ≤40, ≤50) are speculative without `.dev/tasks/done/` calibration (failure-mode #4; INV-006 LOW)
  - Check-overlap with rf-qa-qualitative for TB-Add-1 and TB-Add-6 (proposal line 59); mitigated by PR-04 Inherited Structural Verdict
- **invariant-probe findings affecting this proposal**: **INV-006 UNADDRESSED LOW** (TB-Add-2 calibration), INV-011 ADDRESSED (LOW, sequencing with PR-01 correct)
- **rationale**: Score (0.963) clears 0.75 ADOPT threshold strongly. Only LOW invariant concern (TB-Add-2) and proposal already mitigates via ADVISORY-fail-until-calibrated. Central role in portfolio: lands first in sequencing, absorbs PR-01 cross-validation as TB-Add-7, sets the structural verdict that PR-04 propagates.

---

## PR-07: adversarial-category-naming

- **CASE**: D
- **quant_score**: 0.892
- **qual_score**: 0.933
- **combined_score**: 0.913
- **verdict**: ADOPT
- **debate-derived strengths**:
  - Lowest over-engineering risk of all 7 (proposal line 13)
  - Pure intent-port: no new code path, no new stage, no new agent file (proposal line 13)
  - Axes ARE evidence-bound: "invented content" axis cross-checks against research/*.md (proposal line 51)
  - Anti-inflation alignment: "weakened" only if BUILD_REQUEST/research demands stronger phrasing (proposal line 60)
  - Severity floor preserved (proposal line 58, ref rf-qa-qualitative.md:789)
- **debate-derived weaknesses**:
  - D5.4 NOT MET in qualitative scoring (no sync-discipline mention)
  - Failure-mode #3: drift baseline requirement underspecified (Round-2 rebuttal resolved with `drift-axis-inactive` annotation when GOAL-baseline absent)
  - Touches the qualitative-gate area along with PR-04 and PR-06; sequencing must be explicit
- **invariant-probe findings affecting this proposal**: INV-013 ADDRESSED (LOW, clean composition with PR-04 verdict)
- **rationale**: Score (0.913) clears 0.75 ADOPT threshold. No HIGH or MEDIUM invariant concerns directly tied to this proposal. Lands fourth in sequencing order (after PR-04 establishes inherited-verdict context).

---

## Verdict Summary

| Proposal | Verdict | Combined Score |
|----------|---------|----------------|
| PR-01 | REVISE | 0.912 |
| PR-02 | ADOPT | 0.965 |
| **PR-03** | **ADOPT (BASE)** | **0.959** |
| PR-04 | ADOPT | 0.934 |
| PR-05 | REVISE | 0.862 |
| PR-06 | ADOPT | 0.963 |
| PR-07 | ADOPT | 0.913 |

**Counts**: ADOPT 5 (PR-02, PR-03, PR-04, PR-06, PR-07) + REVISE 2 (PR-01, PR-05) + REJECT 0.
