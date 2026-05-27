# Round 2 — Rebuttal Advocate for Variant 3

## Responses to R1 Criticisms

### Response to V1 Advocate: "Two-ref minimalism hides load-bearing logic"

V1's advocate (R1-A1, W-V3-1, lines 131-136) argues that V3's Kill List item 1 ("Extract only if eval shows Wave 1 inline logic is fragile") is an anti-pattern -- "we'll know it when we see it." This misreads V3's intent. The Kill List does not say "we will discover fragility magically." It says: *the eval harness will produce evidence*. If Wave 1's inline coverage mapping misclassifies >25% of requirements (per V3 eval rubric dimension 2, threshold >=75% precision), that is a measurable failure signal that triggers extraction. V3's position is not "defer the decision" but "let empirical data make the decision." V1's alternative -- pre-committing to 6-7 ref files before any eval data exists -- optimizes for a failure mode (inline fragility) that may not materialize, at the cost of 4-5 additional files that must be authored, reviewed, and kept consistent during the iteration cycle where they are most likely to change.

V1's own advocate concedes (R1-A1, concession 6, lines 210-212) that V1's dual-source-of-truth on thresholds (Wave 2.5 table AND Section 6 restatement) creates drift risk. V3 has no such duplication because the rubric exists in one place (Section 4). The fewer-files discipline prevents the specific failure mode V1 already admits to.

### Response to V1 Advocate: "0.85 is rubber-stamping"

R1-A1 (W-V3-2, lines 138-144) calls V3's >=0.85 T1 stop threshold "rubber-stamping" because "15% of spec requirements can be unmapped." This argument ignores V3's compound stop condition. Per V3 Section 5 Wave 2 (line 229): T1 STOP requires *all three* of `coverage_pct >= 0.85` AND `deviations_found == 0` AND `scope <= 3 files`. The 0.85 floor applies only when the work is deviation-free AND narrow-scope. A 15% coverage gap with zero deviations in a <=3-file change means the unmapped items are spec requirements the diff legitimately does not touch (e.g., requirements for features not included in the PR). V1's 0.95 threshold would force T2 escalation on a clean 3-file change because one requirement in a 20-item spec is for a future feature. That is not "rigor" -- it is false escalation.

However, the field converges on 0.90 (V2, V5). R1-A1's argument that 0.90 aligns with CLAUDE.md global rule 3 (>=90% confidence) is persuasive. V3 should adopt 0.90 for the default T1 stop and retain 0.85 as the `--depth quick` floor, as V3's own R1 advocate already proposed (R1-A3, X-001 position, line 157). This is a genuine concession, not a retreat.

### Response to V2 Advocate: "4-signal rubric drops multi-domain detection"

R1-A2 (W-V3-1, lines 259-265) identifies that V3's tier rubric (Section 4) has no explicit multi-domain trigger. V2's rule 4 ("S_domains >= 3 -> ESCALATE") catches cross-domain changes. This is a valid critique. V3's table covers coverage_pct, scope breadth, spec complexity, and --depth override -- but a 3-file change touching code + infra + docs could pass all four checks and stop at T1 incorrectly.

V3 should add a 5th signal: `domain_span > 1` triggers T2. This is a single row addition to the rubric table (Section 4), not a structural change. It does not require V2's full 5-dimension priority logic or V5's composite scoring -- it is a boolean escalation trigger. V3's framework supports this addition without inflation: the Kill List already excludes T1 multi-model fan-out (Kill List item 5), which is consistent with escalating multi-domain work to T2 where heterogeneous review applies.

### Response to V2 Advocate: "Eliminating think_about_* loses 200-token nudge benefit"

R1-A2 (W-V3-2, lines 267-274) argues that V3's elimination of think_about_* "throws away the cheap 200-token scripted-nudge benefit." The word "cheap" is doing all the work in this argument. The cost is not 200 tokens -- it is:

1. Three additional tool invocations per reflection (each consuming a tool-call round trip).
2. Audit-log entries that must be parsed, stored, and ignored by every downstream consumer.
3. A protocol dependency on a tool surface whose behavior is non-deterministic (the "nudge" output varies per invocation).

None of the advocates provides empirical evidence that these nudges improve any measurable outcome. V2's advocate cites "Topic 1 research" but that research characterizes the tools as "current but under-leveraged" -- not "proven to improve classification accuracy." V1's advocate (R1-A1, line 233) positions them as "optional scripted checkpoints, never load-bearing" -- which means they do not gate any decision. A non-gating, non-load-bearing, non-deterministic tool invocation is not "cheap" -- it is dead weight with a token cost.

V3's position (eliminate entirely) is the correct default for v1. If eval evidence shows that adding scripted nudges improves deviation classification precision (dimension 2) or reduces false positives (dimension 5), they can be restored in v1.1 with a single protocol addition. The reverse path -- removing them from a protocol that has grown dependent on their audit-log entries -- is harder. V3's elimination is the safer direction of reversibility.

### Response to V4 Advocate: "V3 under-specifies gatekeeper rigor"

R1-A4 (lines 167-173) argues that V3's 2-ref architecture and 70% ship threshold provide "less protection against fake citations, bad recommendations, and artifact contract drift" than V4's 7-dimension rubric and Testability Map.

This conflates two different things: the number of eval dimensions and the rigor of the gatekeeping. V3's 5 eval dimensions include Citation accuracy (>=90% threshold) and Recommendation actionability (>=80% threshold). V3 also has an explicit evidence re-validation step (Wave 4 step 3) that spawns evidence-validator to re-Read every file:line citation. These are the same mechanisms V4 relies on for citation protection. V4's additional 2 dimensions (Tier-routing correctness, Artifact contract compliance) test protocol mechanics, not reflection quality -- a point V4's own advocate implicitly concedes by describing them as "deterministic" (R1-A4, X-011 position).

V3 should adopt V4's Testability Map *principle* (every protocol decision maps to an eval assertion) without adopting V4's 7-dimension structure. The principle is valuable; the extra dimensions are not. V3's R1 advocate already proposed this (R1-A3, concession C3 and S7 discussion).

### Response to V5 Advocate: "No F1/F2/F3 fallback for sc-adversarial failures"

R1-A5 (lines 118-119) identifies a genuine gap: V3 delegates to sc-adversarial in Wave 3 step 3 (lines 277-284) but has no documented recovery path if sc-adversarial returns empty, times out, or produces a partial response. V5's three-level fallback (F1 retry with --depth quick, F2 highest-calibrated single review, F3 write reflect-failed.md with partial state) is a concrete operational discipline V3 lacks.

This is V3's most significant structural gap. The Error Handling Matrix (V3 Section 11, lines 470-487) has a row for "sc:adversarial-protocol fails" with fallback "use highest-confidence agent output" and flag "adversarial_unavailable" -- but this is a single-level fallback, not a graduated response. V3 should adopt V1's three-tier guard sequence (R1-A1, Strength 8, lines 100-104): empty-response guard, partial-parse guard, and missing-file guard, each with distinct fallback behavior. This addition is 3-4 lines in the Error Handling Matrix and does not inflate the wave count.

### Response to V5 Advocate: "Calibrator-as-reviewer anti-pattern"

R1-A5 (line 119) and R1-A1 (lines 183-189) both flag V3's placement of confidence-calibrator in the reviewer table (V3 Section 5 Wave 3, lines 244-258) as conflating the calibrator's role. V1's advocate (R1-A1, line 235) argues the calibrator should grade *other* reviewers' cards, not produce its own first-pass card.

This is a valid structural critique. V3's current design has the calibrator re-grading the Wave 1 coverage map -- which is a reviewer-like task (producing a card with scores). The calibrator's comparative advantage is *independent assessment of others' work*, not independent generation of primary analysis. V3 should restructure: confidence-calibrator runs per-card after the root-cause-analyst produces its deviation investigation, grading the analyst's output rather than producing a parallel coverage re-grade. The coverage re-grade moves inline into Wave 2 (the confidence gate), which is where coverage assessment logically belongs. This is a role restructuring, not a new agent or new wave.

## Updated Assessment

V3's core thesis -- minimalism as a discipline -- survives R1 criticism intact but requires four targeted repairs:

1. Raise T1 coverage floor to 0.90 (default) / 0.85 (--depth quick).
2. Add a 5th tier-rubric signal for multi-domain detection.
3. Add a three-tier fallback protocol for sc-adversarial failures.
4. Restructure calibrator role from reviewer to post-card grader.

None of these repairs changes V3's wave count (6), ref count (2), return contract field count (~14), or Kill List. They are additive refinements within V3's existing frame.

## New Evidence

### NE-1. V1 and V5 both concede V3's Kill List discipline

R1-A1 (concession 9, lines 216-217): "The merge should add a Kill List subsection inside V1 Section 15." R1-A5 (steelman of V3, lines 31-33): "The Kill List is the only variant that treats scope-exclusion as a first-class design decision." V3's Kill List is now the consensus position -- every advocate agrees it should be in the merged output. This validates V3's approach as a structural contribution, not just a stylistic preference.

### NE-2. V2 and V5 converge on V3's convergence threshold direction

V2 uses 0.75 PASS; V3 and V5 use 0.65. But R1-A3's own R1 advocate (line 169) proposed a two-tier approach: >=0.75 = PASS, 0.65-0.74 = PARTIAL. V5 (R1-A5, X-003 position, lines 181-185) argues 0.65 is correct for classification tasks. V3's 0.65 is not an outlier -- it is one end of a legitimate spectrum where the other end (0.75) applies to creative-merge tasks, not classification tasks. The merged output should adopt V3's two-tier structure (PASS >= 0.75, PARTIAL >= 0.65) as the compromise that respects both positions.

### NE-3. Field converges on 0.90 coverage floor

V2 (0.90), V5 (0.90), and V3's revised position (0.90 default, 0.85 --depth quick) all land at the same number. V1 (0.95) is the outlier. V4 (1.00) is the extreme. The field has spoken: 0.90 is the T1 coverage floor. V3 should adopt this and move forward.

### NE-4. V3's wave count is defensible against V1/V4's 9-wave alternatives

R1-A1 (line 240) argues 9 waves "buys observability" via per-wave audit-log emits. But observability does not require separate waves. V3 can emit per-step timing within a single wave (Wave 4 step 3 "evidence re-validation complete: <ms>") without splitting into distinct waves. The audit-log granularity comes from step-level emits, not wave-level boundaries. V3's 6 waves provide sufficient checkpoint density; V1/V4's 9 waves provide redundant checkpoint density at the cost of 3 additional wave-entry/exit boundary pairs that must each be tested.

## Concessions

### Concession 1: Classification Precedence Rule (confirmed from R1)

V3 lacks a classification precedence rule. V2's "Regression > Drift > Necessary > Authorized" (R1-A2, S2-4) is the correct mechanism. V3's default-to-Drift rule is the right fallback but not the right primary rule. V3 should adopt V2's precedence as the primary rule and retain default-to-Drift as the fallback when no signals match. This was conceded in R1-A3 (concession C1) and remains valid.

### Concession 2: [INFERRED] Tag (confirmed from R1)

V3 drops ungrounded claims silently without tagging the inference/evidence distinction. V2's Grounded/[INFERRED] binary (R1-A2, S2-3) provides auditability that V3 lacks. V3 should adopt the binary tag and surface `citations_inferred: N` in the report header. V3 should not adopt V2's "drop everything that fits neither bucket" rule (per R1-A1's critique, lines 118-121, which is correct). This was conceded in R1-A3 (concession C3).

### Concession 3: sc-adversarial Fallback Protocol (new in R2)

R1-A5 identifies that V3 has no graduated fallback when sc-adversarial fails. V3's Error Handling Matrix has a single-row fallback. V1's three-tier guard sequence (R1-A1, Strength 8) and V5's F1/F2/F3 protocol (R1-A5) are both superior. V3 should adopt a three-level fallback: (1) retry with --depth quick, (2) use highest-confidence agent output, (3) write reflect-failed.md with partial state. This adds 3-4 lines to the Error Handling Matrix.

### Concession 4: Env-Var Model-Alias Awareness (confirmed from R1)

V3 assumes model aliases are available. V5's Wave 0 step 6 (R1-A5, S2) checks env vars and degrades gracefully. V3 should add a Wave 0 env-var check. This was conceded in R1-A3 (concession C5).

### Concession 5: Multi-Domain Detection (new in R2)

V3's tier rubric lacks a multi-domain escalation trigger. V2's rule 4 (S_domains >= 3) and V1's binary multi-domain rule both address this gap. V3 should add a 5th rubric signal: `domain_span > 1` triggers T2. This is a single row addition to Section 4.

## Updated Per-Point Positions

### X-001 (T1 coverage floor)

**REVISED from R1.** V3 now proposes 0.90 (default) / 0.85 (--depth quick). Rationale: the field converges on 0.90 (V2, V5). CLAUDE.md global rule 3 aligns at 0.90. V3's compound stop condition (0.90 AND deviations==0 AND scope<=3) provides equivalent safety to V1's single-signal 0.95. The `--depth quick` floor at 0.85 preserves V3's quick-pass economics for low-stakes work. This is a genuine concession that strengthens V3's position by aligning with the consensus while preserving the depth-stratified threshold structure that only V3 offers.

### X-003 (convergence PASS)

**HELD from R1.** V3 proposes >=0.75 = PASS, 0.65-0.74 = PARTIAL, <0.65 = unresolved_conflict. This is a two-tier compromise that respects V1/V2's stricter bar (0.75) while preserving V3/V5's tolerance for partial resolution (0.65). The R1 debate revealed that the convergence threshold is task-dependent: creative merge (brainstorm) needs 0.75, classification merge (reflect) tolerates 0.65. V3's two-tier structure accommodates both. R1-A3's advocate (line 169) already proposed this; it remains the correct position.

### X-005 (think_about_* status)

**HELD from R1.** V3 eliminates entirely. No R1 advocate provided empirical evidence that these tools improve any measurable outcome. V1's "optional scripted checkpoints" and V2's "scripted nudges, not load-bearing" both admit the tools are non-gating. V4's "mandatory checkpoint gates" and V5's "mandatory scripted checkpoints" add audit-log overhead without evidence of value. V3's elimination is the correct v1 default. The merged output should adopt V3's position with a design note in the Boundaries section stating that scripted nudges can be restored if eval evidence supports it.

### X-009 (deviation taxonomy categories)

**HELD from R1.** V3 maintains 4 categories with conservative default-to-Drift. V4's 5th `unknown` class is an escape hatch that reduces classification precision (R1-A2, W-V4-2). V5 agrees with V3 (R1-A5, X-009 position: "4 categories is correct... the gap is in the evidence, not the taxonomy"). V3 should adopt V2's precedence rule (Regression > Drift > Necessary > Authorized) as the primary classification mechanism, with default-to-Drift as the fallback for ambiguous cases.

### A-001 (SKILL.md length)

V3 is 569 lines -- the shortest variant. R1-A5 concedes that V5's 864 lines "crosses into compress or split" (R1-A5, A-001 response). R1-A1 argues that "the wave count is not a quality dimension" (R1-A1, X-007 position) but acknowledges V5's length is problematic. V3's 569 lines is comfortably within the 400-700 line band. The merged output should target 550-650 lines, using V3's frame and adding the accepted concessions (precedence rule, inference tag, env-var check, multi-domain signal, fallback protocol) which total ~40-60 additional lines, bringing the merged result to ~610-630 lines.

### A-002 (env-var aliases)

**REVISED.** V3 now accepts the critique. Wave 0 should check ANTHROPIC_DEFAULT_* env vars. If any are missing: WARN and adjust reviewer topology (drop optional quality-engineer if haiku alias unavailable; use opus+sonnet duo if haiku is missing; use sonnet-only if only sonnet is available). If no aliases are available: WARN and restrict to T1-only execution (T2 requires heterogeneous models). This matches V5's degraded-mode handling (R1-A5, S2).

### A-003 (workspace path)

**HELD.** V3 uses `.dev/eval-workspaces/sc-reflect/` per V1-V4 convention. V5's `sc-reflect-protocol` is the outlier. R1-A5 concedes this (lines 240-243): "V1-V4 are correct." V3's convention should prevail.

### A-004 (60/40 train/test split)

**HELD with qualification.** 60/40 is the Anthropic default and appropriate for iteration 2+. For iteration 1 (3 pilot cases), the split is statistically meaningless. V3 should use all-train for iteration 1 and 60/40 for iteration 2+. This matches R1-A1's position (R1-A1, A-004 response).

### A-005 (single-repo scope)

**HELD.** All variants agree. V3's memory key convention (`reflection-last-pass-{project-slug}`) is scoped per-project. Multi-repo reflection is out of v1 scope.

## Summary Judgment

V3 enters R2 with four targeted repairs that address every substantive criticism from R1:

| Criticism from R1 | V3 Response | Mechanism |
|---|---|---|
| Coverage floor too low (V1, V2) | Adopt 0.90 default, 0.85 --depth quick | Compound stop condition preserved |
| Missing multi-domain trigger (V2) | Add 5th rubric signal | Single row in Section 4 |
| No classification precedence (V2, V4) | Adopt V2's Regression > Drift > Necessary > Authorized | One paragraph in Wave 1 step 5 |
| No inference/evidence tagging (V2) | Adopt Grounded/[INFERRED] binary without drop rule | 2-3 lines in Wave 4 step 3 |
| No adversarial fallback (V5) | Adopt three-tier fallback protocol | 3-4 lines in Error Handling Matrix |
| Calibrator-as-reviewer (V1, V5) | Restructure calibrator to post-card grader | Role change, no new agents |
| No env-var check (V5) | Add Wave 0 degraded-mode check | 2 lines in Wave 0 |
| Ref minimalism hides logic (V1) | Eval-data-driven extraction trigger | Kill List unchanged |

These repairs add ~50 lines to V3's 569-line frame, producing a ~620-line merged candidate that remains the shortest variant, retains the 6-wave architecture, keeps 2 refs, and preserves the Kill List. V3 remains the correct skeletal structure for the merged output.

The path forward: V3's frame, V2's hallucination discipline (precedence rule + inference tagging), V1's fallback guard sequence, V5's env-var handling, and V4's Testability Map principle (without the 7-dimension bloat). Every addition must earn its lines against V3's Kill List standard: if it cannot map to an eval assertion, it does not belong in v1.
