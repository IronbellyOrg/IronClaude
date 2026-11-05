# Base Selection Report

**Status:** Complete, actual scoring assembled and arithmetic verified; downstream merge validation remains separate
**Governing sources:** sc-adversarial-protocol/refs/artifact-templates.md Section3 and scoring-protocol.md; the current six-dimension, thirty-criterion rubric overrides the older five-dimension template example.
**Scope:** Selection of the writing base only. Scores and agreement are not causal likelihood, probabilities, or independent empirical observations.

## Quantitative Scoring (50% weight)
The completed quantitative evaluator froze lexical rules before execution and evaluated them twice with identical results. Counts are retained below. These are bounded writing proxies, not independently certified semantic facts.

| Metric | Weight | Actual operational definition |
|---|---:|---|
| Requirement coverage (RC) |0.30|Heading matches against13 named topic aliases; no formal source requirement IDs were present.|
| Internal consistency (IC)|0.25|One minus exact positive/negative lexical opposing pairs divided by lexical claim candidates. This does not prove absence of semantic contradictions.|
| Specificity ratio (SR)|0.15|Concrete statements divided by substantive statements after the recorded paragraph, fence and boilerplate rules. Residual nonconcrete statements are not necessarily vague.|
| Dependency completeness (DC)|0.15|Resolved internal references divided by internal references; zero references receives the evaluator's neutral value1. External document links are excluded.|
| Section coverage (SC)|0.15|Second-level heading count divided by maximum observed count11.|

| Count or metric | Variant1 | Variant2 | Variant3 | Variant4 | Variant5 |
|---|---:|---:|---:|---:|---:|
|Heading-topic matches|13/13|13/13|13/13|12/13|12/13|
|Concrete / substantive statements|7/24|10/26|7/26|10/16|5/14|
|Nonconcrete statements|17|16|19|6|9|
|Lexical claim candidates|7|10|7|10|5|
|Opposing literal pairs|0|0|0|0|0|
|Internal references resolved / total|0/0|0/0|0/0|0/0|0/0|
|Second-level headings|11|11|11|11|11|
|RC|1.000000000|1.000000000|1.000000000|0.923076923|0.923076923|
|IC|1.000000000|1.000000000|1.000000000|1.000000000|1.000000000|
|SR|0.291666667|0.384615385|0.269230769|0.625000000|0.357142857|
|DC|1.000000000 (neutral 0/0)|1.000000000 (neutral 0/0)|1.000000000 (neutral 0/0)|1.000000000 (neutral 0/0)|1.000000000 (neutral 0/0)|
|SC|1.000000000 (11/11)|1.000000000 (11/11)|1.000000000 (11/11)|1.000000000 (11/11)|1.000000000 (11/11)|
|Recorded quantitative score|**0.893750000**|**0.907692308**|**0.890384615**|**0.920673077**|**0.880494505**|

Formula: `0.30RC + 0.25IC + 0.15SR + 0.15DC + 0.15SC`. Variants4/5 match12/13 topics because they lack the recorded next-steps heading alias; inline takeaways do not count. The evaluator reports `TWO_RUN_EQUAL=True`. The exact executed rule script is retained at scoring source lines84-166; its limitations are at lines71-73. The published nine-decimal quantitative scores agree with direct fraction arithmetic within0.00000000051. Combined values below use those published scores, matching the actual mechanical comparison; retaining full fractions changes only sub-billionth rounding, not selection.

## Qualitative Scoring (50% weight): Thirty-Criterion Binary Rubric

### Completeness
The criterion labels and binary decisions below are the actual independent evaluations. Full Claim-Evidence-Verdict records for every cell, including distinct evidence wording in each pass, are preserved unchanged in Complete Forward Evaluation and Complete Reverse Evaluation. `F/R` means forward/reverse; both gave the displayed decision.

| Criterion | Variant1 F/R | Variant2 F/R | Variant3 F/R | Variant4 F/R | Variant5 F/R |
|---|---|---|---|---|---|
|`COMP1`: Covers all explicit requirements from source input|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`COMP2`: Addresses edge cases and failure scenarios|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`COMP3`: Includes dependencies and prerequisites|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`COMP4`: Defines success/completion criteria|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`COMP5`: Specifies what is explicitly out of scope|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|Subtotal per pass|5/5|5/5|5/5|5/5|5/5|

### Correctness
The criterion labels and binary decisions below are the actual independent evaluations. Full Claim-Evidence-Verdict records for every cell, including distinct evidence wording in each pass, are preserved unchanged in Complete Forward Evaluation and Complete Reverse Evaluation. `F/R` means forward/reverse; both gave the displayed decision.

| Criterion | Variant1 F/R | Variant2 F/R | Variant3 F/R | Variant4 F/R | Variant5 F/R |
|---|---|---|---|---|---|
|`COR1`: No factual errors or hallucinated claims|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`COR2`: Technical approaches are feasible with stated constraints|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`COR3`: Terminology used consistently and accurately throughout|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`COR4`: No internal contradictions (cross-validated with quantitative IC metric)|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`COR5`: Claims supported by evidence or rationale within the document|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|Subtotal per pass|5/5|5/5|5/5|5/5|5/5|

### Structure
The criterion labels and binary decisions below are the actual independent evaluations. Full Claim-Evidence-Verdict records for every cell, including distinct evidence wording in each pass, are preserved unchanged in Complete Forward Evaluation and Complete Reverse Evaluation. `F/R` means forward/reverse; both gave the displayed decision.

| Criterion | Variant1 F/R | Variant2 F/R | Variant3 F/R | Variant4 F/R | Variant5 F/R |
|---|---|---|---|---|---|
|`STR1`: Logical section ordering (prerequisites before dependents)|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`STR2`: Consistent hierarchy depth (no orphaned subsections)|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`STR3`: Clear separation of concerns between sections|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`STR4`: Navigation aids present (table of contents, cross-references, or index)|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`STR5`: Follows conventions of the artifact type|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|Subtotal per pass|5/5|5/5|5/5|5/5|5/5|

### Clarity
The criterion labels and binary decisions below are the actual independent evaluations. Full Claim-Evidence-Verdict records for every cell, including distinct evidence wording in each pass, are preserved unchanged in Complete Forward Evaluation and Complete Reverse Evaluation. `F/R` means forward/reverse; both gave the displayed decision.

| Criterion | Variant1 F/R | Variant2 F/R | Variant3 F/R | Variant4 F/R | Variant5 F/R |
|---|---|---|---|---|---|
|`CLR1`: Unambiguous language (no "should consider", "might", "as appropriate")|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`CLR2`: Concrete rather than abstract (specific actions, not general principles)|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`CLR3`: Each section has a clear purpose statement or can be summarized in one sentence|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`CLR4`: Acronyms and domain terms defined on first use|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|
|`CLR5`: Actionable next steps or decision points clearly identified|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|Subtotal per pass|4/5|4/5|4/5|4/5|4/5|

### Risk Coverage
The criterion labels and binary decisions below are the actual independent evaluations. Full Claim-Evidence-Verdict records for every cell, including distinct evidence wording in each pass, are preserved unchanged in Complete Forward Evaluation and Complete Reverse Evaluation. `F/R` means forward/reverse; both gave the displayed decision.

| Criterion | Variant1 F/R | Variant2 F/R | Variant3 F/R | Variant4 F/R | Variant5 F/R |
|---|---|---|---|---|---|
|`RISK1`: Identifies at least 3 risks with probability and impact assessment|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|
|`RISK2`: Provides mitigation strategy for each identified risk|NOT MET / NOT MET|MET / MET|MET / MET|NOT MET / NOT MET|MET / MET|
|`RISK3`: Addresses failure modes and recovery procedures|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|MET / MET|MET / MET|
|`RISK4`: Considers external dependencies and their failure scenarios|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`RISK5`: Includes monitoring or validation mechanism for risk detection|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|Subtotal per pass|2/5|3/5|3/5|3/5|4/5|

### Invariant and Edge Case Coverage
The criterion labels and binary decisions below are the actual independent evaluations. Full Claim-Evidence-Verdict records for every cell, including distinct evidence wording in each pass, are preserved unchanged in Complete Forward Evaluation and Complete Reverse Evaluation. `F/R` means forward/reverse; both gave the displayed decision.

| Criterion | Variant1 F/R | Variant2 F/R | Variant3 F/R | Variant4 F/R | Variant5 F/R |
|---|---|---|---|---|---|
|`EDGE1`: Addresses boundary conditions for collections (empty, single-element, maximum size)|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|
|`EDGE2`: Handles state variable interactions across component boundaries|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`EDGE3`: Identifies guard condition gaps (missing validation, unguarded type assumptions)|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|`EDGE4`: Covers count divergence scenarios (off-by-one, inclusive/exclusive ranges)|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|NOT MET / NOT MET|
|`EDGE5`: Considers interaction effects when features or components combine|MET / MET|MET / MET|MET / MET|MET / MET|MET / MET|
|Subtotal per pass|3/5|3/5|3/5|3/5|3/5|

### Qualitative Summary and Eligibility
| Dimension | Variant1 | Variant2 | Variant3 | Variant4 | Variant5 |
|---|---:|---:|---:|---:|---:|
|Completeness|5/5|5/5|5/5|5/5|5/5|
|Correctness|5/5|5/5|5/5|5/5|5/5|
|Structure|5/5|5/5|5/5|5/5|5/5|
|Clarity|4/5|4/5|4/5|4/5|4/5|
|Risk|2/5|3/5|3/5|3/5|4/5|
|Edge|3/5|3/5|3/5|3/5|3/5|
|Total criteria MET|24/30|25/30|25/30|25/30|26/30|
|Qualitative score|0.800000000|0.833333333|0.833333333|0.833333333|0.866666667|
|Invariant/edge eligibility|ELIGIBLE (3/5)|ELIGIBLE (3/5)|ELIGIBLE (3/5)|ELIGIBLE (3/5)|ELIGIBLE (3/5)|

Every candidate meets the minimum1/5 invariant/edge criterion, so no floor is suspended. Both passes give5/5 Correctness on supplied card evidence; this means no error was identified within those inputs, not an independent replay or recertification of every historical primary record. The qualitative scorers were not given the quantitative IC result; their COR4 decisions use qualitative consistency and say so explicitly. Probability/impact requirements not evidenced in the cards remain NOT MET; no probabilities were invented to improve scores.

## Position-Bias Mitigation
Actual independent forward evaluation reads1→2→3→4→5. The separate reverse evaluator reads5→4→3→2→1 and explicitly states no other scorer results were used. Each gives30 binary decisions per candidate,150 per pass. A mechanical key-by-key comparison found150 matching criterion/candidate pairs out of150 and zero disagreements. Therefore zero disagreement adjudications and zero verdict changes were required. This is agreement on writing criteria, not causal-order convergence.

| Candidate | Compared criterion pairs | Agreed | Disagreed | Re-adjudicated | Changed verdicts |
|---|---:|---:|---:|---:|---:|
|Variant1|30|30|0|0|0|
|Variant2|30|30|0|0|0|
|Variant3|30|30|0|0|0|
|Variant4|30|30|0|0|0|
|Variant5|30|30|0|0|0|
|Total|150|150|0|0|0|

The six dimension tables above display every forward/reverse binary pair. The unchanged raw pass blocks below retain all300 Claim-Evidence-Verdict records, rather than replacing the reverse pass with the forward evidence merely because their decisions agree.

## Combined Scoring
Formula: `combined = 0.50 × recorded quantitative score + 0.50 × (criteria MET / 30)`. Values are writing-quality arithmetic only.

| Candidate | Quantitative ×0.50 | Qualitative ×0.50 | Combined score | Writing-point wins | Correctness MET |
|---|---:|---:|---:|---:|---:|
|Variant1|0.446875000000|0.400000000000|**0.846875000000**|1|5/5|
|Variant2|0.453846154000|0.416666666667|**0.870512820667**|1|5/5|
|Variant3|0.445192307500|0.416666666667|**0.861858974167**|1|5/5|
|Variant4|0.460336538500|0.416666666667|**0.877003205167**|1|5/5|
|Variant5|0.440247252500|0.433333333333|**0.873580585833**|1|5/5|

Numeric writing-score order: Variant4, Variant5, Variant2, Variant3, Variant1. Top-two score gap: `0.003422619333333`, below0.05. Apply the protocol tiebreak: writing-point wins1:1; Correctness5:5; input order4 before5 selects Variant4. The actual manager records one win each for C-004→Variant1, C-003→Variant2, C-002→Variant3, C-007→Variant4 and C-005→Variant5; shared synthesis points award no individual win. No causal order is used to break the writing tie.

## Selected Writing Base
**Selected writing base: Variant4, brittle evidence and provenance handoffs.** This identifies the document to merge into, not the most likely cause. The actual mode used existing artifacts and current-model-default advocates; no model version is inferred.

The highest combined scores are Variant4 and Variant5, separated by0.003422619333 on the0-1 writing-score scale. That is below the protocol's0.05 tiebreak threshold. The actual manager's recorded point matrix gives each variant one writing-point win; shared synthesis points award no individual win. Variant4 and Variant5 therefore tie at level1 (one win each), and at level2 (all five Correctness criteria MET). Level3 selects the earlier input, Variant4 before Variant5. This is an explicit deterministic tiebreak, not an empirical causal preference.

### Strengths to Preserve from the Writing Base
- Separate durable-proof loss, incorrect evidence pointers, false change attribution from a reconstructed dirty baseline, and missing-checkpoint halt classification.
- Preserve unchanged-delivery controls while distinguishing evidence artifacts and policy, which delivery digests do not cover.
- Retain valid historical proof requirements, actual literal lint failure, policy/proof confounding, and missing present-day archive availability as counterevidence and limits.

### Strengths to Incorporate from All Non-Base Variants
| Source | Distinct contribution to retain | Integration boundary |
|---|---|---|
|Variant1|Checks can genuinely pass while proving less than behavior: fixture meaning, timing, integration, deferred tests and ineffective stubs.|Explains old-defect escape, not every repair introduction or unchanged authorized blocker.|
|Variant2|Successful repairs can introduce connected ordering, data-source or diagnostic/data-stream faults, demonstrated by immediate before/after evidence.|Keep introduced defects distinct from untouched sibling failures; plan nonconformance is not automatically runtime disorder.|
|Variant3|Original criteria, applied interpretations and actually loaded policies can differ; live migration can add review entry.|Policy change does not create preexisting code defects; final policy/proof effects remain confounded.|
|Variant5|A known frozen-input or unavailable-capability blocker can remain unchanged through useful partial repair review.|Original requirements were feasible; accepted unverified rendering is not a repaired render.|

### Separate Causal Comparison
The plan's provisional causal order is Variant1, Variant3, Variant2, Variant5, Variant4. This is an evidence-weighted synthesis judgment, not the numeric writing-score order and not full advocate consensus. Actual Round2 orders: advocates1/2 retain1>2>3>4>5; advocate3 retains1>3>2>4>5; advocates4/5 give1>3>2>5>4. The middle pair and bottom pair remain disputed; neither reaches four-of-five agreement. All five mechanisms remain potentially coexisting. No probability, population prevalence, model/version effect or universal cure is established.

## Complete Forward Evaluation
Source: retained scoring record lines168-358, original scorer `agent-a503f9bd5b0246156.jsonl`, final physical record41, UUID `f88e2e39-fc06-44cc-87c8-c8a2e2f672fd`. The following complete evaluator body is copied unchanged.

```text
FORWARD qualitative pass1. Five consecutive 30-row blocks follow INPUTORDER 1→5. COMP1 assesses each assigned single-cause card; deferred ranking is allowed at this prerequisite stage, while the final synthesis still requires all five distinct merits and a selected-sample ranking. Historical claims are assessed against card evidence and supplied R2 context, not independently rerun or recertified. Scores assess writing quality, not causal rank.
COMP1 — Covers all explicit requirements from source input
COMP2 — Addresses edge cases and failure scenarios
COMP3 — Includes dependencies and prerequisites
COMP4 — Defines success/completion criteria
COMP5 — Specifies what is explicitly out of scope
COR1 — No factual errors or hallucinated claims
COR2 — Technical approaches are feasible with stated constraints
COR3 — Terminology used consistently and accurately throughout
COR4 — No internal contradictions (cross-validated with quantitative IC metric)
COR5 — Claims supported by evidence or rationale within the document
STR1 — Logical section ordering (prerequisites before dependents)
STR2 — Consistent hierarchy depth (no orphaned subsections)
STR3 — Clear separation of concerns between sections
STR4 — Navigation aids present (table of contents, cross-references, or index)
STR5 — Follows conventions of the artifact type
CLR1 — Unambiguous language (no "should consider", "might", "as appropriate")
CLR2 — Concrete rather than abstract (specific actions, not general principles)
CLR3 — Each section has a clear purpose statement or can be summarized in one sentence
CLR4 — Acronyms and domain terms defined on first use
CLR5 — Actionable next steps or decision points clearly identified
RISK1 — Identifies at least 3 risks with probability and impact assessment
RISK2 — Provides mitigation strategy for each identified risk
RISK3 — Addresses failure modes and recovery procedures
RISK4 — Considers external dependencies and their failure scenarios
RISK5 — Includes monitoring or validation mechanism for risk detection
EDGE1 — Addresses boundary conditions for collections (empty, single-element, maximum size)
EDGE2 — Handles state variable interactions across component boundaries
EDGE3 — Identifies guard condition gaps (missing validation, unguarded type assumptions)
EDGE4 — Covers count divergence scenarios (off-by-one, inclusive/exclusive ranges)
EDGE5 — Considers interaction effects when features or components combine
V1 — Checks Prove Less Than the Requirement
COMP1|claim met|Hypothesis, incidents, counterevidence and limits develop the assigned weak-check mechanism; Summary explicitly defers relative likelihood to debate.|MET
COMP2|claim met|Counterevidence distinguishes frozen remainder, successful smaller-task repairs and actual repair introductions.|MET
COMP3|claim met|Discriminating Test requires "preserved historical versions" and fixed original acceptance criteria/review policy.|MET
COMP4|claim met|Discriminating Test specifies support when examples pass weak checks but fail a criterion-derived behavioral check, and weakening when actual original checks reject them.|MET
COMP5|claim met|Scope excludes frozen fixtures, unavailable rendering and defective pointers from automatic inclusion in this hypothesis.|MET
COR1|claim met|Incidents and Counterevidence distinguish initial escape from later persistence; Limits denies causal rates, while Gaps states tests were not rerun. No error established by supplied evidence.|MET
COR2|claim met|Discriminating Test proposes bounded counterexamples on preserved versions, explicitly not production execution or relaxed criteria.|MET
COR3|claim met|Exact Mechanism, Counterevidence and Summary consistently distinguish weaker verification, old defects and repair-created defects.|MET
COR4|claim met|Counterevidence qualifies the broad hypothesis: three repairs worked; task size is only an amplifier. No internal contradiction found; quantitative IC result was not supplied.|MET
COR5|claim met|Supporting Incidents links four case reports and historical review/plan anchors; Limits explains the observational task-size inference.|MET
STR1|claim met|Hypothesis → Exact Mechanism → Supporting Incidents → Counterevidence → Scope → Discriminating Test → Limits.|MET
STR2|claim met|All substantive sections use the same heading level; the incident table and mechanism list remain subordinate content.|MET
STR3|claim met|Supporting Incidents supplies observations; Counterevidence limits attribution; Discriminating Test separates proposed investigation from historical evidence.|MET
STR4|claim met|Supporting Incidents and Counterevidence contain linked case reports plus named sections and historical anchors.|MET
STR5|claim met|Metadata, causal mechanism, supporting evidence, competing explanations, falsification and gaps fit a research hypothesis card.|MET
CLR1|claim met|Hypothesis says "partly caused"; Limits explicitly labels task-size evidence observational and denies universal attribution. These are clear evidentiary qualifications.|MET
CLR2|claim met|Incidents name counts/labels, validation after fetch, ineffective search filters and contradictory advisory wording rather than merely urging better checking.|MET
CLR3|claim met|Each named section has one identifiable function: explanation, evidence, limitation, test or conclusion.|MET
CLR4|claim notmet|No first-use definitions for JSONL, CI or PR; searched metadata, Exact Mechanism and Supporting Incidents.|NOT MET
CLR5|claim met|Discriminating Test directs construction of each minimal counterexample and comparison of existing versus criterion-derived checks.|MET
RISK1|claim notmet|Several failure risks and impacts appear, but probability assessments do not; searched Mechanism, Incidents, Counterevidence and Limits. Evidence strength is not probability.|NOT MET
RISK2|claim notmet|The proposed behavioral comparison addresses weak checks, but no explicit mitigation covers the separately identified large-unit/deferred-lasting-test amplifier; searched Test, Takeaways and Summary.|NOT MET
RISK3|claim notmet|Failure modes are detailed, but the proposed test diagnoses attribution rather than providing a repair/recovery procedure; searched Mechanism, Counterevidence, Test and Summary.|NOT MET
RISK4|claim met|Scope explicitly identifies "unavailable render tools" and frozen fixtures as competing immediate blockers rather than silently assuming those dependencies work.|MET
RISK5|claim met|Discriminating Test compares passing weak checks against criterion-derived behavioral checks and checks whether relevant tests were absent or deferred.|MET
EDGE1|claim notmet|No concrete empty/single-element/maximum collection boundary is developed; searched Incidents, Test and Limits. Generic "range, summary and size defects" is insufficient.|NOT MET
EDGE2|claim met|Planning incident places validation after the fetch consuming its input; Exact Mechanism explicitly identifies execution order and cross-component use.|MET
EDGE3|claim met|Oracle labels/counts omit required semantic validation; planning validation exists too late to guard the input-consuming fetch.|MET
EDGE4|claim notmet|No concrete off-by-one or inclusive/exclusive count divergence is explained; searched Incidents and Test. Passing family counts despite wrong semantics is not count divergence.|NOT MET
EDGE5|claim met|Scope permits weak checks to coexist with connected repair defects, while Counterevidence separates frozen-input persistence and task-size/deferred-test amplification.|MET
V2 — Local Repairs Miss Connected Effects
COMP1|claim met|Hypothesis, five connected-effect examples, counterevidence and scope develop the assigned local-repair cause; metadata explicitly defers final ranking.|MET
COMP2|claim met|Counterevidence covers accepted repairs, preexisting monitor defects, exposed output limits and proof-only credential repairs.|MET
COMP3|claim met|Discriminating Test requires confirmed successful edits, preserved immediate pre-fix state and fixed original criterion/policy.|MET
COMP4|claim met|Test requires an absent-before/present-after counterexample; existing-before failures must instead be classified retained or previously missed.|MET
COMP5|claim met|Scope separates introduction from incomplete sibling coverage and excludes reviewer cognition; Limits rejects universal repair/model-ability claims.|MET
COR1|claim met|Incidents distinguish plan nonconformance from runtime disorder; Counterevidence rejects treating twenty later items as twenty regressions. No error established by supplied evidence.|MET
COR2|claim met|Test uses preserved immediate states and confirmed edits; it explicitly labels replay proposed and disclaims production execution.|MET
COR3|claim met|Scope and Takeaways consistently reserve "introduced" for demonstrated new defects and "retained" for untouched existing failures.|MET
COR4|claim met|CI's sequential-execution safeguard consistently limits the claimed graph defect's runtime impact; no contradiction found. Quantitative IC result was not supplied.|MET
COR5|claim met|Each incident provides a before/after conclusion and case/transcript anchors; Counterevidence identifies successful amendments and preexisting defects.|MET
STR1|claim met|Mechanism and historical evidence precede counterevidence, attribution boundaries and proposed replay.|MET
STR2|claim met|Uniform section headings contain a numbered mechanism, evidence table and subordinate test bullets without orphaned subsections.|MET
STR3|claim met|Incidents distinguish actual amendments; Scope defines attribution categories; Test specifies how to distinguish those categories.|MET
STR4|claim met|Incident rows and Counterevidence link planning, monitor and CI case reports with sections and historical anchors.|MET
STR5|claim met|The card supplies hypothesis, mechanism, before/after evidence, counterevidence, falsification, limitations and summary.|MET
CLR1|claim met|"This is demonstrated in selected changes, not inferred from every later failure" clearly bounds the assertion rather than obscuring uncertainty.|MET
CLR2|claim met|Examples specify Task13 before Task14 registration, deployed-package versus recipe provenance and trap annotations captured as stdout data.|MET
CLR3|claim met|Each section can be summarized as mechanism, examples, objections, boundaries, test, evidentiary strength or unresolved questions.|MET
CLR4|claim notmet|No first-use definitions for CI, JSONL or stdout; searched metadata, Mechanism and Supporting Incidents.|NOT MET
CLR5|claim met|Test requires immediate before/after counterexamples and directs reclassification when the failure predates the edit.|MET
RISK1|claim notmet|Multiple concrete risks and impacts are given, but no probability assessments; searched Incidents, Counterevidence, Scope and Limits.|NOT MET
RISK2|claim met|Test identifies each affected producer/consumer/sibling/dependency edge and checks the remedy against unchanged constraints and neighboring paths before broader review.|MET
RISK3|claim notmet|Failure modes and diagnostic reclassification are explicit, but rollback or operational repair/recovery procedures are absent; searched Test, Takeaways, Gaps and Summary.|NOT MET
RISK4|claim met|The four-asset incident distinguishes release existence from pin-writer eligibility and explains how an inappropriate dependency predicate changes which job rejects the release.|MET
RISK5|claim met|Test demands confirmed successful edits plus an explicit data-flow/order explanation and an absent-before/present-after counterexample.|MET
EDGE1|claim notmet|No empty/single-element/maximum collection case is developed; searched all incident rows and Test. The four-asset predicate is not presented as those boundaries.|NOT MET
EDGE2|claim met|Inventory comparison precedes registration; inherited trap diagnostics cross command-substitution boundaries into captured data.|MET
EDGE3|claim met|The early four-asset predicate applies the wrong stage contract; trap output is accepted as captured data without preserving the diagnostic/data boundary.|MET
EDGE4|claim notmet|No explicit off-by-one/inclusive/exclusive divergence; searched Incidents, Counterevidence and Test. Amendment/finding-count cautions are attribution cautions, not count-boundary cases.|NOT MET
EDGE5|claim met|Exact Mechanism and five incidents directly trace repairs interacting with neighboring jobs, data sources, dependency edges and unchanged constraints.|MET
V3 — Review Contracts Change During the Loop
COMP1|claim met|The assigned contract-change cause includes distinct submechanisms, evidence, counterexamples and limits; Summary leaves relative importance for debate.|MET
COMP2|claim met|Counterevidence preserves stable oracle/render criteria and genuine preexisting monitor defects despite changed review entry rules.|MET
COMP3|claim met|Test requires original text, accepted exceptions, exact loaded rubric bytes and artifact state for every reviewed attempt.|MET
COMP4|claim met|Test specifies support when changing only the contract changes a verdict/review requirement, and weakening when fixed criteria reproduce substantive failures.|MET
COMP5|claim met|Scope rejects universal invented-requirement claims and distinguishes source contradictions, unauthorized interpretations, operator decisions and migrations.|MET
COR1|claim met|Migration is explicitly separated from original defect creation; credential convergence remains policy/proof-confounded. No error established by supplied evidence.|MET
COR2|claim met|Proposed paired adjudication holds artifact state fixed and varies preserved contracts; the card explicitly states no historical replay occurred.|MET
COR3|claim met|Mechanism, Scope and Test consistently distinguish original requirements, actually applied rules, authorized acceptance and added hardening.|MET
COR4|claim met|The hypothesis permits unchanged delivery with changed review while Counterevidence acknowledges genuine old defects; no contradiction found. Quantitative IC result was not supplied.|MET
COR5|claim met|Incident rows cite nested reviewer records, captured historical-rule text and migration records; Limits names the unknown actor and unresolved isolated policy effect.|MET
STR1|claim met|The card defines contract inconsistency before presenting mechanisms, stable-contract counterexamples and the controlled comparison.|MET
STR2|claim met|Uniform major headings, a five-row evidence table and subordinate test bullets form a consistent hierarchy.|MET
STR3|claim met|Evidence, competing causes, proposed adjudication and unknown attribution are separated into named sections.|MET
STR4|claim met|Links point to case reports, historical-review-rules.json and scope-rules.md, with historical record references.|MET
STR5|claim met|Hypothesis-card conventions are satisfied through mechanism, primary anchors, counterevidence, falsification and explicit limitations.|MET
CLR1|claim met|"Their separate effects cannot be isolated" clearly states confounding; "not clearly required" identifies a documented scope dispute rather than an ambiguous instruction.|MET
CLR2|claim met|Examples specify the changed-line lint clause, stale-evidence rubric difference and mandatory fresh review on migration.|MET
CLR3|claim met|Each section has a distinct one-sentence purpose, from defining the mechanism through proposing a discriminating comparison.|MET
CLR4|claim notmet|QA, FINAL, CI and JSONL appear without first-use definitions; searched metadata, Mechanism and Supporting Incidents.|NOT MET
CLR5|claim met|Test tells reviewers to adjudicate under original versus actual contracts and classify original violations, exceptions, hardening, contradictions or version effects.|MET
RISK1|claim notmet|At least three contract risks and consequences are identified, but no probability assessments; searched Mechanism, Incidents, Scope and Limits.|NOT MET
RISK2|claim met|Preserving original requirements, exceptions, exact rubric bytes and artifact state, then paired classification, directly addresses the identified contract-consistency risks.|MET
RISK3|claim notmet|The card explains reversals and how to classify them, but supplies no procedure to resolve conflicting contracts or recover execution after migration; searched Test, Takeaways and Summary.|NOT MET
RISK4|claim met|Installed review-policy contents can change between reviewers; Stale Documentation explicitly refuses to substitute current rules for historically loaded versions.|MET
RISK5|claim met|Paired adjudication under fixed original versus changed rules detects verdict/re-entry changes attributable to contract differences.|MET
EDGE1|claim notmet|No collection empty/single-element/maximum boundary is analyzed; searched Incidents, Test and Gaps. Uncapped fields are not developed as collection-boundary cases.|NOT MET
EDGE2|claim met|Test tracks artifact state, accepted exceptions and loaded rubric bytes across review attempts, isolating rule-state changes from delivery changes.|MET
EDGE3|claim met|The literal no-finding-on-changed-line condition is weakened to no-new-findings; the migration introduces a completion prerequisite absent from earlier acceptance.|MET
EDGE4|claim notmet|No off-by-one or inclusive/exclusive count divergence is explained; searched Incidents, Test and Gaps. Reviewer-count attribution is not that scenario.|NOT MET
EDGE5|claim met|Credential convergence explicitly combines evidence corrections with changed policy; monitor migration combines new review entry with genuine preexisting omissions.|MET
V4 — Brittle evidence and provenance handoffs
COMP1|claim met|The assigned proof/provenance cause develops distinct mechanisms, evidence-only intervals, counterevidence and limits; metadata explicitly leaves ranking pending.|MET
COMP2|claim met|Counterevidence preserves genuine lint failure, valid evidence rejection and policy confounding; Scope limits the missing checkpoint to a halt mechanism.|MET
COMP3|claim met|Falsification requires the true pre-task state, retained original proof, fixed rubric and unchanged delivered requirements.|MET
COMP4|claim met|Falsification states weakening conditions: repeats despite valid proof/baseline, or a purported proof-only interval requiring delivery correction.|MET
COMP5|claim met|Hypothesis excludes explanation of every semantic defect; Scope denies that checkpoint absence proves repository movement or caused rendering failure.|MET
COR1|claim met|The card distinguishes delivery digests from evidence/policy and unavailable live archives from preserved transcript contents. No error established by supplied evidence.|MET
COR2|claim met|Proposed reconstruction uses recorded baselines and original proof; missing live logs are explicitly disclosed rather than assumed available.|MET
COR3|claim met|Claim-to-proof linkage, baseline provenance, checkpoint halt and delivery change remain distinct throughout Mechanism, Scope and Summary.|MET
COR4|claim met|An initial proof-only pass coexists consistently with a follow-up genuine lint violation and later confounding; no contradiction found. Quantitative IC result was not supplied.|MET
COR5|claim met|Supporting Incidents provides transcript/nested-review anchors and discriminating observations; Limits identifies unchanged delivery digests and recovered Git trees.|MET
STR1|claim met|Hypothesis and mechanism precede incident evidence, objections, scope, competing explanations and falsification.|MET
STR2|claim met|Consistent main headings contain subordinate bullets, one evidence table and clearly associated takeaway paragraphs.|MET
STR3|claim met|Mechanism separates proof loss/baseline substitution; Counterevidence limits causal claims; Gaps separately records archive availability.|MET
STR4|claim met|Case-report links, physical transcript anchors and historical-rule evidence links provide navigation beyond headings.|MET
STR5|claim met|The adapted hypothesis card includes metadata, causal explanation, traceable incidents, counterevidence, falsification and unresolved questions.|MET
CLR1|claim met|"That label does not itself prove HEAD changed" and "digests exclude evidence artifacts and policy" clearly delimit conclusions.|MET
CLR2|claim met|Concrete examples include a README separator citation, blank log line10, post-edit HEAD substitution and an absent start-HEAD file.|MET
CLR3|claim met|Named sections and repeated key takeaways make each section's purpose directly identifiable.|MET
CLR4|claim notmet|QA, HEAD, JSONL and FINAL are not defined on first use; searched metadata, Mechanism and Supporting Incidents.|NOT MET
CLR5|claim met|Falsification directs reconstruction of the true baseline, retention of original proof and checking every cited range under a fixed rubric.|MET
RISK1|claim notmet|Proof loss, incomplete evidence, false attribution and checkpoint halt have impacts, but no probability assessments; searched Mechanism, Incidents and Limits.|NOT MET
RISK2|claim notmet|Durable proof, citation checks and true-baseline reconstruction mitigate several risks, but no mitigation is supplied for the separately identified missing-checkpoint halt; searched Falsification and Summary.|NOT MET
RISK3|claim met|Supporting Incidents records proof/pointer correction and recovery of the truthful Git tree; Falsification specifies reconstructing the true pre-task state and validating cited ranges.|MET
RISK4|claim met|Gaps records an archived log returning "file does not exist" and distinguishes that failed dependency from the surviving nested transcript body.|MET
RISK5|claim met|Checking every cited range under a fixed rubric and comparing delivery digests against historical-before/after evidence detect proof/provenance failures.|MET
EDGE1|claim notmet|No collection empty/single-element/maximum boundary is developed; searched Mechanism, Incidents and Falsification. A blank cited line is not an empty collection.|NOT MET
EDGE2|claim met|Post-edit HEAD substitution replaces a baseline containing preexisting dirty work, changing downstream attribution without establishing new task-created changes.|MET
EDGE3|claim met|Falsification says not to waive semantic support merely because a cited line exists; Mechanism rejects equating a missing-checkpoint guard label with actual HEAD movement.|MET
EDGE4|claim notmet|No explicit off-by-one/inclusive/exclusive divergence; searched Mechanism, Incidents and Stale Documentation. A missed row or moved pointer alone does not establish count divergence.|NOT MET
EDGE5|claim met|Counterevidence and Competing Explanations identify evidence repair combined with changed rubric text, preventing isolated attribution of the final pass.|MET
V5 — Late feasibility and repair-authority checks
COMP1|claim met|The assigned retained-blocker cause distinguishes authority from capability, supplies both incidents and limits broader attribution; final ranking is explicitly pending.|MET
COMP2|claim met|Counterevidence preserves feasible original requirements, successful permitted repairs and legitimate partial re-review; no malformed manual page is inferred.|MET
COMP3|claim met|Falsification requires the unmet property, actual evidence-producing capability and permitted correction before resubmission.|MET
COMP4|claim met|Test requires a changed blocker or scoped decision; Summary distinguishes authorized fixture correction/PASS from accepted unverified rendering.|MET
COMP5|claim met|Hypothesis excludes universal impossibility; Falsification explicitly excludes installs, freeze bypass, altered criteria and new task execution.|MET
COR1|claim met|The card distinguishes accepted inability to verify from successful rendering and feasible original requirements from constrained repair. No error established by supplied evidence.|MET
COR2|claim met|The proposed comparison examines documented authority/capability without installing tools or bypassing the freeze; missing live evidence is disclosed.|MET
COR3|claim met|Unchanged blocker, repair authority, rendering capability, authorized correction and accepted cannot-verify retain distinct meanings.|MET
COR4|claim met|The scope restriction and later authorized fixture correction are consistent; rendering remains unverified throughout. Quantitative IC result was not supplied.|MET
COR5|claim met|Both incident rows provide physical transcript anchors and specific repeated conditions; Gaps identifies captured historical evidence when an archived log is absent.|MET
STR1|claim met|Hypothesis and mechanism precede incidents, counterevidence, scope, competing explanations and the proposed test.|MET
STR2|claim met|Uniform major headings consistently contain subordinate mechanism bullets, one evidence table and takeaway paragraphs.|MET
STR3|claim met|Authority and capability are distinct mechanisms; Counterevidence handles legitimate controls, while Gaps handles absent render proof/archive availability.|MET
STR4|claim met|Case-report links, a directly reread review-artifact reference and absolute historical transcript paths support navigation.|MET
STR5|claim met|The card follows research-hypothesis conventions through mechanism, primary evidence, counterevidence, falsification and limitations.|MET
CLR1|claim met|"Late blocker handling under the observed constraints" explicitly rejects impossible-specification and pointless-review interpretations.|MET
CLR2|claim met|Examples identify default_path=false, three successful repairs, the excluded fourth defect and a nominal rc0 notice that did not render.|MET
CLR3|claim met|Each section has a distinct purpose, reinforced by takeaways separating unchanged acceptance state from new repair damage.|MET
CLR4|claim notmet|JSONL and rc0 are not defined on first use; searched metadata, Supporting Incidents and Gaps.|NOT MET
CLR5|claim met|Before resubmission, identify the failed property, actual capability and permitted correction; require a changed blocker or scoped decision.|MET
RISK1|claim notmet|Freeze, capability, misleading availability/exit evidence and repeated unchanged rejection are covered, but probability assessments are absent; searched Mechanism, Incidents and Limits.|NOT MET
RISK2|claim met|The pre-resubmission property/capability/authority check covers both identified blocker classes and requires either relevant correction or the required scoped decision.|MET
RISK3|claim met|The fixture recovers through explicit authorization and one-field correction/PASS; rendering instead takes a scoped acceptance path retaining cannot-verify, not falsely claiming repair.|MET
RISK4|claim met|The available manual-page command prints a notice rather than rendering; missing archived proof is disclosed with surviving transcript evidence identified.|MET
RISK5|claim met|Falsification checks whether the next attempt actually changes the blocker or obtains its required decision, rather than relying on successful unrelated repairs.|MET
EDGE1|claim notmet|No collection empty/single-element/maximum boundary is analyzed; searched Mechanism, Incidents and Falsification. Three repairs plus one blocker are outcome counts, not collection boundaries.|NOT MET
EDGE2|claim met|The frozen fixture's semantic state interacts with executor repair permission and reviewer acceptance; rendering capability interacts with the availability-guarded evidence requirement.|MET
EDGE3|claim met|Stale Documentation identifies the inadequate availability guard; Supporting Incidents explains why nominal rc0 did not establish rendering capability.|MET
EDGE4|claim notmet|No explicit off-by-one/inclusive/exclusive count divergence; searched Mechanism, Incidents and Counterevidence. Three corrected findings and one retained finding do not alone satisfy this criterion.|NOT MET
EDGE5|claim met|Scope combines weak semantic assertions with fixture freezing and weak availability checks with renderer limitation, while preserving their distinct immediate blockers.|MET
V1 TOTAL — COMP5 COR5 STR5 CLR4 RISK2 EDGE3 = 24/30 (80.00%); correctness 5/5, card-evidence limited; edge eligibility YES (3/5). Source: /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/variant-1-original.md
V2 TOTAL — COMP5 COR5 STR5 CLR4 RISK3 EDGE3 = 25/30 (83.33%); correctness 5/5, card-evidence limited; edge eligibility YES (3/5). Source: /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/variant-2-original.md
V3 TOTAL — COMP5 COR5 STR5 CLR4 RISK3 EDGE3 = 25/30 (83.33%); correctness 5/5, card-evidence limited; edge eligibility YES (3/5). Source: /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/variant-3-original.md
V4 TOTAL — COMP5 COR5 STR5 CLR4 RISK3 EDGE3 = 25/30 (83.33%); correctness 5/5, card-evidence limited; edge eligibility YES (3/5). Source: /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/variant-4-original.md
V5 TOTAL — COMP5 COR5 STR5 CLR4 RISK4 EDGE3 = 26/30 (86.67%); correctness 5/5, card-evidence limited; edge eligibility YES (3/5). Source: /config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/variant-5-original.md
```

## Complete Reverse Evaluation
Source: retained scoring record lines360-547, original scorer `agent-a5a65d90e0b48891c.jsonl`, final physical record46, UUID `25b4ad1b-aea4-4faa-9540-2b8e2e4cbf79`. The following complete evaluator body is copied unchanged.

```text
Reverse pass 2: cards read 5→4→3→2→1 in `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/`; exact supplied Round 2 context read; no other scorer results used.
Operationalization: COMP1 assesses each assigned single-cause card; all-five merits and selected-sample ranking remain final-synthesis requirements, not missing individual-card requirements. Historical correctness is assessed from supplied card evidence, not independently replayed primary records.
Criterion dictionary follows verbatim; Vn denotes variant-n-original.md. Writing/base quality is not causal likelihood. No writing, delegation or publication performed.
COMP1|Covers all explicit requirements from source input
COMP2|Addresses edge cases and failure scenarios
COMP3|Includes dependencies and prerequisites
COMP4|Defines success/completion criteria
COMP5|Specifies what is explicitly out of scope
COR1|No factual errors or hallucinated claims
COR2|Technical approaches are feasible with stated constraints
COR3|Terminology used consistently and accurately throughout
COR4|No internal contradictions (cross-validated with quantitative IC metric)
COR5|Claims supported by evidence or rationale within the document
STR1|Logical section ordering (prerequisites before dependents)
STR2|Consistent hierarchy depth (no orphaned subsections)
STR3|Clear separation of concerns between sections
STR4|Navigation aids present (table of contents, cross-references, or index)
STR5|Follows conventions of the artifact type
CLR1|Unambiguous language (no "should consider", "might", "as appropriate")
CLR2|Concrete rather than abstract (specific actions, not general principles)
CLR3|Each section has a clear purpose statement or can be summarized in one sentence
CLR4|Acronyms and domain terms defined on first use
CLR5|Actionable next steps or decision points clearly identified
RISK1|Identifies at least 3 risks with probability and impact assessment
RISK2|Provides mitigation strategy for each identified risk
RISK3|Addresses failure modes and recovery procedures
RISK4|Considers external dependencies and their failure scenarios
RISK5|Includes monitoring or validation mechanism for risk detection
EDGE1|Addresses boundary conditions for collections (empty, single-element, maximum size)
EDGE2|Handles state variable interactions across component boundaries
EDGE3|Identifies guard condition gaps (missing validation, unguarded type assumptions)
EDGE4|Covers count divergence scenarios (off-by-one, inclusive/exclusive ranges)
EDGE5|Considers interaction effects when features or components combine
COMP1|V5 met|Hypothesis, Exact Mechanism, Supporting Incidents, Counterevidence and Falsification Test complete the assigned retained-blocker account; Rank explicitly pending.|MET
COMP2|V5 met|Counterevidence distinguishes feasible original requirements, three successful repairs, legitimate partial re-review and absence of demonstrated malformed output.|MET
COMP3|V5 met|Falsification Test requires “unmet property, actual evidence-producing capability and permitted correction” before resubmission.|MET
COMP4|V5 met|Falsification Test requires changed blocker or scoped decision; Summary distinguishes fixture correction/PASS from accepted unverified rendering.|MET
COMP5|V5 met|Hypothesis explicitly excludes “a universal inability to implement the original requirement”; Scope limits direct support to two incidents.|MET
COR1|V5 met|Supporting Incidents supplies anchored observations; Counterevidence and Gaps explicitly deny demonstrated malformed output, fresh rendering and current archive availability; no error identified within supplied evidence.|MET
COR2|V5 met|Falsification Test checks permitted changes and capability; explicitly records “no installs, freeze bypass, altered acceptance criteria or new task execution.”|MET
COR3|V5 met|Exact Mechanism and Summary consistently separate correction authority, rendering capability, unchanged blocker and scoped acceptance.|MET
COR4|V5 met|Counterevidence’s feasible originals agree internally with observed later constraints; Summary never converts accepted inability to verify into successful rendering; no quantitative IC result supplied.|MET
COR5|V5 met|Supporting Incidents contrasts exclusion→three repairs→unchanged fourth finding and static-only retry→same render clause, with primary anchors.|MET
STR1|V5 met|Hypothesis→Exact Mechanism→Supporting Incidents→Counterevidence precede Falsification Test and final limits/summary.|MET
STR2|V5 met|One document title and consistently parallel second-level sections; no orphaned subsection.|MET
STR3|V5 met|Exact Mechanism explains causation; Supporting Incidents supplies observations; Counterevidence bounds inference; Gaps records unavailable evidence.|MET
STR4|V5 met|Supporting Incidents links oracle and documentation case reports and names their sections.|MET
STR5|V5 met|Metadata labels an adapted hypothesis card; mechanism, evidence, counterevidence, falsification, limits and summary match that artifact type.|MET
CLR1|V5 met|“not an impossible specification or a rule against all resubmission” precisely bounds the claim; uncertainty concerns evidence, not vague instructions.|MET
CLR2|V5 met|Supporting Incidents identifies excluded default_path=false correction, a one-field correction, static-only retry and unchanged rendering clause.|MET
CLR3|V5 met|Each section has a distinct stated function; Hypothesis, Mechanism, Incidents and Counterevidence also give explicit Key takeaways.|MET
CLR4|V5 not met|No first-use definitions for JSONL and rc0; searched Supporting Incidents, Exact Mechanism and remaining sections.|NOT MET
CLR5|V5 met|Falsification Test explicitly says identify property/capability/authority and check whether the next attempt changes the blocker or obtains a scoped decision.|MET
RISK1|V5 not met|Provisional Evidence Strength gives strong/moderate evidentiary support, not probability-and-impact assessments for at least three risks; searched Mechanism, Counterevidence, Limits and Gaps.|NOT MET
RISK2|V5 met|Falsification Test supplies a shared mitigation for both blocker types: verify capability and permitted correction, then change the blocker or obtain the required scoped decision.|MET
RISK3|V5 met|Supporting Incidents documents authorized fixture correction followed by PASS; Summary separately preserves accepted unverified rendering rather than claiming recovery of rendering.|MET
RISK4|V5 met|Exact Mechanism identifies the available command returning a notice instead of rendering; Gaps handles missing archived evidence through captured transcript findings.|MET
RISK5|V5 met|Falsification Test compares the identified unmet property with the next attempted change and tests unsupported repeated objections.|MET
EDGE1|V5 not met|No empty, singleton or maximum-size collection cases; searched Exact Mechanism, Supporting Incidents, Counterevidence and Falsification Test.|NOT MET
EDGE2|V5 met|Exact Mechanism connects frozen fixture state and permitted repair actions to reviewer acceptance; separately connects executable availability to real rendering capability.|MET
EDGE3|V5 met|Stale Documentation explicitly calls the rendering “availability guard” inadequate; Supporting Incidents says nominal rc0 did not prove rendering.|MET
EDGE4|V5 not met|Three repaired findings versus one retained finding describes repair scope, not an off-by-one or divergent counting/range rule; searched Incidents, Mechanism and Test.|NOT MET
EDGE5|V5 met|Competing Explanations examines anti-overfitting freeze combined with permitted repairs; Counterevidence examines partial repair verification alongside retained rejection.|MET
COMP1|V4 met|Hypothesis through Falsification Test develops the assigned evidence/provenance cause, with scope, counterevidence and limits; Summary explicitly defers ranking.|MET
COMP2|V4 met|Counterevidence includes valid proof rejection, genuine lint failure and policy-confounded convergence; Scope separates checkpoint halt from rendering failure.|MET
COMP3|V4 met|Falsification Test requires true pre-task state, original proof, every cited range and a fixed rubric.|MET
COMP4|V4 met|Falsification Test specifies weakening conditions: valid complete proof/correct baseline with continued failures, or a necessary delivery correction in a supposed proof-only interval.|MET
COMP5|V4 met|Hypothesis says it “does not explain every semantic defect”; Limits excludes fleet frequency, numerical probability and version-effect claims.|MET
COR1|V4 met|Supporting Incidents anchors ledger changes and baseline reconstruction; Counterevidence denies isolated proof causation for the final pass; no error identified within supplied evidence.|MET
COR2|V4 met|Falsification Test proposes historical reconstruction and fixed-rubric citation checking, explicitly not an executed comparison or waiver of semantic support.|MET
COR3|V4 met|Mechanism and Scope consistently distinguish delivery, proof, baseline provenance and checkpoint classification.|MET
COR4|V4 met|Evidence-only intervals coexist without contradiction with the follow-up’s genuine lint violation; checkpoint label is explicitly not proof of HEAD movement; no quantitative IC result supplied.|MET
COR5|V4 met|Supporting Incidents supplies temporary-proof substitution, preexisting blank pointer and recovered earlier baseline; Limits explains what delivery digests exclude.|MET
STR1|V4 met|Hypothesis and mechanism precede incident evidence; counterevidence and competing explanations precede proposed falsification and summary.|MET
STR2|V4 met|Document title and parallel second-level sections maintain one consistent hierarchy.|MET
STR3|V4 met|Incidents hold observations; Counterevidence qualifies attribution; Scope separates contexts; Gaps distinguishes unavailable archives from preserved contents.|MET
STR4|V4 met|Supporting Incidents links documentation and credential reports; Stale Documentation links historical rule evidence.|MET
STR5|V4 met|Explicit adapted hypothesis-card metadata and mechanism/evidence/counterevidence/falsification/limits sections follow research-card conventions.|MET
CLR1|V4 met|“that label does not itself prove HEAD changed” and “digests exclude evidence artifacts and policy” make evidentiary limits precise.|MET
CLR2|V4 met|Exact Mechanism names unrelated citation, incomplete evidence range, post-edit HEAD substitution and missing checkpoint.|MET
CLR3|V4 met|Each section has a distinct purpose; Mechanism, Incidents and Counterevidence include concise Key takeaways.|MET
CLR4|V4 not met|QA, HEAD, JSONL and FINAL appear without first-use definitions; searched Hypothesis, Mechanism, Incidents and Counterevidence.|NOT MET
CLR5|V4 met|Falsification Test gives concrete reconstruction, proof retention and cited-range checks under a fixed rubric.|MET
RISK1|V4 not met|Several risks and consequences are described, but none receives a probability-and-impact assessment; searched Mechanism, Counterevidence, Limits and Gaps.|NOT MET
RISK2|V4 not met|Summary mitigates baseline/proof/citation failures, but no explicit mitigation preserves or restores the missing start checkpoint; searched Mechanism, Test, Gaps and Summary.|NOT MET
RISK3|V4 met|Incidents documents durable-proof/pointer correction producing a pass and investigation recovering the truthful earlier Git tree.|MET
RISK4|V4 met|Counterevidence addresses changed loaded policy; Gaps records unavailable archived proof and preserved nested transcript content.|MET
RISK5|V4 met|Falsification Test checks every cited range under a fixed rubric and rejects mere line existence as semantic support.|MET
EDGE1|V4 not met|Blank lines and incomplete citations do not establish empty/singleton/maximum collection handling; searched Mechanism, Incidents and Test.|NOT MET
EDGE2|V4 met|Mechanism connects dirty working-tree state, reconstructed baseline and later task attribution; proof conversion separately changes the reviewable ledger state.|MET
EDGE3|V4 met|Mechanism identifies an incomplete evidence range surviving audit; Test explicitly forbids accepting semantic support merely because a cited line exists.|MET
EDGE4|V4 not met|Blank pointer and later line shift show citation defects, but no explicit divergent counting/range rule or off-by-one scenario; searched Incidents, Test and Stale Documentation.|NOT MET
EDGE5|V4 met|Counterevidence explains pointer correction plus changed rubric confounding the final pass; Scope separates checkpoint and rendering mechanisms.|MET
COMP1|V3 met|Hypothesis, five mechanism-specific incidents, stable-contract counterexamples and Discriminating Test complete the assigned contract-change card; final ranking is explicitly deferred.|MET
COMP2|V3 met|Counterevidence covers stable oracle/render criteria and genuine defects predating migration; Gaps rejects unsupported assumptions about all broad review demands.|MET
COMP3|V3 met|Discriminating Test requires original requirements, accepted exceptions, exact loaded rubric bytes and artifact state for every attempt.|MET
COMP4|V3 met|Discriminating Test defines support as verdict/re-entry changing solely with contract; unchanged substantive failure under identical conditions weakens the hypothesis.|MET
COMP5|V3 met|Scope excludes universal defect causation and blanket invented requirements; Counterevidence excludes stable-contract retained blockers.|MET
COR1|V3 met|Incidents anchors differing rubric versions and migration; Limits explicitly leaves actor and policy-only pass effect unknown; no error identified within supplied evidence.|MET
COR2|V3 met|Paired independent adjudication under original and changed contracts is a feasible proposed comparison; no historical replay is claimed.|MET
COR3|V3 met|Scope consistently distinguishes source contradiction, unauthorized interpretation, authorized acceptance, added hardening and policy migration.|MET
COR4|V3 met|Migration can reopen review while genuine defects predate it; final convergence is explicitly confounded by evidence repair; no quantitative IC result supplied.|MET
COR5|V3 met|Supporting Incidents supplies separate anchored evidence for lint relaxation, rubric versions, migration, broader checking and source conflicts.|MET
STR1|V3 met|Hypothesis→mechanism→evidence→counterevidence/scope precedes controlled comparison, limits and summary.|MET
STR2|V3 met|One title and consistent parallel second-level sections; numbered mechanism and table remain within their parent sections.|MET
STR3|V3 met|Evidence table separates contract mechanisms; Counterevidence isolates stable contracts; Test defines comparison rather than asserting its outcome.|MET
STR4|V3 met|Evidence table links credential, monitor and planning cases plus captured rule texts; Stale Documentation links current-rule map separately.|MET
STR5|V3 met|Research metadata, causal hypothesis, anchored incidents, alternatives, discriminating test and limits follow hypothesis-card conventions.|MET
CLR1|V3 met|“not a claim that all reviewers invent requirements” and the five explicit finding classifications remove attribution ambiguity; warranted uncertainty is bounded.|MET
CLR2|V3 met|Incidents specifies no-new-findings versus no-finding-on-changed-line, differing rubric text and mandatory fresh operator review.|MET
CLR3|V3 met|Each section can be summarized distinctly: proposed cause, transition mechanism, evidence, exceptions, comparison, limits or conclusion.|MET
CLR4|V3 not met|QA, FINAL, CI and JSONL appear without first-use definitions; searched Hypothesis, Mechanism and Supporting Incidents.|NOT MET
CLR5|V3 met|Discriminating Test explicitly directs preservation, paired adjudication and classification of differences.|MET
RISK1|V3 not met|Five contract mechanisms are described, but probability-and-impact assessments are absent; searched Incidents, Scope, Limits and Gaps.|NOT MET
RISK2|V3 met|Preserving original requirements/exceptions/exact rules and separately adjudicating/classifying differences mitigates conflation across the identified contract-change mechanisms.|MET
RISK3|V3 not met|Failure modes and detection are explicit, but no procedure resolves conflicting instructions or restores one operative contract after detection; searched Scope, Test, Takeaways and Summary.|NOT MET
RISK4|V3 met|Migration and changing installed rubric are external review-policy dependencies; source contradictions are separately identified rather than silently normalized.|MET
RISK5|V3 met|Paired fixed-versus-changed-contract adjudication detects verdict/re-entry effects while holding artifact state constant.|MET
EDGE1|V3 not met|Uncapped fields are mentioned, but no empty/singleton/maximum-size collection cases are developed; searched Incidents, Counterevidence and Test.|NOT MET
EDGE2|V3 met|Mechanism tracks original criterion, early interpretation, later loaded rule and artifact state across successive reviewers.|MET
EDGE3|V3 met|Literal lint incident identifies acceptance under no-new-findings despite a no-finding-on-changed-line requirement: a missing original-condition validation.|MET
EDGE4|V3 not met|Counting cautions and unsupported minimum-reviewer-count attribution are not divergent counting/range scenarios; searched Counting, Limits and Gaps.|NOT MET
EDGE5|V3 met|Rubric change plus evidence correction explicitly confound the final pass; migration adds review without creating preexisting defects.|MET
COMP1|V2 met|Assigned connected-impact cause has mechanism, successful-change evidence, counterevidence, scope and discriminating comparison; metadata explicitly defers final ranking.|MET
COMP2|V2 met|Counterevidence distinguishes successful repairs, preexisting monitor faults, evidence-only changes and the CI sequential-order safeguard.|MET
COMP3|V2 met|Discriminating Test requires successful edits, immediate pre-fix state, original criterion/policy and identified producer/consumer/sibling/dependency edge.|MET
COMP4|V2 met|Test requires a counterexample absent before and present after; already-present failures must be reclassified as retained or missed.|MET
COMP5|V2 met|Limits excludes most later monitor findings, frozen/environmental blockers and general model-ability claims.|MET
COR1|V2 met|Evidence table distinguishes plan nonconformance from reproduced runtime regression; Counterevidence rejects treating later-item totals as repair regressions; no supplied-evidence error identified.|MET
COR2|V2 met|Successful-edit-only historical replay and before/after counterexamples respect stated scope; no production execution is claimed.|MET
COR3|V2 met|Scope and Takeaways consistently separate introduced connected defects from unchanged sibling failures.|MET
COR4|V2 met|CI graph nonconformance and sequential runtime safeguard are compatible; accepted monitor defects are not described as repaired; no quantitative IC result supplied.|MET
COR5|V2 met|Evidence table provides successful write/edit anchors and concrete ordering, predicate, provenance, stdout and graph mechanisms.|MET
STR1|V2 met|Hypothesis and mechanism precede evidence; counterevidence/scope precede replay method and limits.|MET
STR2|V2 met|One title, parallel second-level sections and contained numbered mechanism/table maintain consistent hierarchy.|MET
STR3|V2 met|Before/after table holds case evidence; Counterevidence bounds attribution; Test specifies standards; Gaps records unperformed or unresolved work.|MET
STR4|V2 met|Supporting Incidents cross-references planning, monitor and CI case reports with named sections and supplements.|MET
STR5|V2 met|Research-card metadata, causal mechanism, anchored comparisons, competing explanations, test and limits match artifact conventions.|MET
CLR1|V2 met|“Evidence for the latter alone does not prove a regression” states the critical distinction plainly; conditional trap behavior is warranted, not vague advice.|MET
CLR2|V2 met|Incidents specifies Task13 before Task14 registration, four-asset predicate reuse and inherited trap output captured as data.|MET
CLR3|V2 met|Every section has a distinct, readily summarized purpose from causal proposal through evidence, exclusions and test.|MET
CLR4|V2 not met|CI and shell-specific terms such as inherited traps/command substitution are not defined on first use; searched Hypothesis, Mechanism and Incidents.|NOT MET
CLR5|V2 met|Discriminating Test gives explicit replay, fixed-contract, before/after and neighbor-check steps plus a reclassification decision.|MET
RISK1|V2 not met|Multiple connected-effect risks have consequences, but no probability-and-impact assessments; searched Incidents, Counterevidence, Limits and Gaps.|NOT MET
RISK2|V2 met|Test applies producer/consumer/sibling/dependency analysis to each alleged regression and requires checking remedies against unchanged constraints and neighbors before review.|MET
RISK3|V2 not met|Failures and attribution recovery are covered, but no concrete artifact-recovery procedure repairs the demonstrated trap or plan defects; Gaps says the regression was accepted, not shown repaired.|NOT MET
RISK4|V2 met|Four-asset predicate incident considers release-asset eligibility and incorrect rejection stage; digest incident considers deployed-package provenance versus companion recipe contract.|MET
RISK5|V2 met|Absent-before/present-after counterexample and explicit data-flow/ordering explanation form a concrete regression-validation mechanism.|MET
EDGE1|V2 not met|Four-asset predicate and size-limit mentions do not develop empty/singleton/maximum collection boundary cases; searched Incidents, Counterevidence and Test.|NOT MET
EDGE2|V2 met|Inherited error-trap status/output crosses command-substitution data capture; release detection and pin-writer eligibility use different stage contracts.|MET
EDGE3|V2 met|Predicate reuse changes which stage rejects a release; acceptance lacks neighbor/invariant validation, and stdout diagnostics enter an unprotected data stream.|MET
EDGE4|V2 not met|Four assets and fourteen/two repair totals do not establish divergent counting rules or off-by-one/range behavior; searched Incidents and Counterevidence.|NOT MET
EDGE5|V2 met|Inherited traps combined with command substitution create captured diagnostic data; inventory comparison combined with later registration creates impossible intermediate acceptance.|MET
COMP1|V1 met|Assigned weak-verification cause includes mechanism, four incident contexts, counterevidence, scope, discriminating test and limits; final debate/ranking remains deferred.|MET
COMP2|V1 met|Counterevidence separates frozen authority, successful smaller-task repairs and genuinely introduced faults from old-defect escape.|MET
COMP3|V1 met|Discriminating Test requires preserved historical versions, original criteria/policy and minimal counterexamples on the first-passing version.|MET
COMP4|V1 met|Test defines support as weak checks accepting wrong behavior that criterion-derived checks reject; actually used checks rejecting it weaken the mechanism.|MET
COMP5|V1 met|Scope excludes frozen fixtures, unavailable render tools and defective pointers as automatic instances; Limits rejects probability/model-comparison claims.|MET
COR1|V1 met|Anchored incident observations are bounded by explicit “historical tests were inspected, not rerun here” and observational size limits; no error identified within supplied evidence.|MET
COR2|V1 met|Bounded historical counterexample checking is feasible under stated preserved-version constraints; the card explicitly labels it proposed, not performed.|MET
COR3|V1 met|Mechanism and Counterevidence consistently distinguish old-defect discovery, introduced regression, semantic checking and repair authority.|MET
COR4|V1 met|Initial weak-check escape and later frozen-blocker persistence are explicitly different events; smaller-task convergence limits task-size inference; no quantitative IC result supplied.|MET
COR5|V1 met|Incidents supplies wrong oracle semantics, structural-only monitor checks, mistimed validation and search/advisory stub weaknesses with case/primary anchors.|MET
STR1|V1 met|Hypothesis→mechanism→supporting incidents→counterevidence/scope precedes test, limits and conclusion.|MET
STR2|V1 met|One title and parallel second-level sections maintain consistent hierarchy without orphaned subsections.|MET
STR3|V1 met|Mechanism explains escape; table supplies observations; Counterevidence separates alternatives; Gaps records causal unknowns and lack of rerun.|MET
STR4|V1 met|Supporting Incidents links oracle, monitor, planning and CI case reports with section references.|MET
STR5|V1 met|Research metadata, hypothesis, anchored evidence, competing explanations, proposed test and limitations fit the assigned research-card artifact.|MET
CLR1|V1 met|“not independently proven universal causes” and “not evidence that the preceding repair introduced it” precisely delimit causal claims.|MET
CLR2|V1 met|Incidents names known/unknown author semantics, default-path meanings, Task14 deferral, validation after fetch and ignored search filters.|MET
CLR3|V1 met|Every section can be summarized in one sentence with distinct hypothesis, mechanism, evidence, exception, test or limit purpose.|MET
CLR4|V1 not met|CI, PR and JSONL are not defined at first use; searched Supporting Incidents and the surrounding sections.|NOT MET
CLR5|V1 met|Discriminating Test directs constructing a minimal counterexample, running the described check and checking absent/deferred behavioral tests.|MET
RISK1|V1 not met|Several risks and impacts are identified, but probability assessments are expressly unestablished; searched Incidents, Limits and Gaps.|NOT MET
RISK2|V1 not met|Test diagnoses weaker checks but gives no explicit per-risk mitigation for deferred test timing, validation placement and ineffective search filtering; searched Test, Takeaways and Summary.|NOT MET
RISK3|V1 not met|Failure mechanisms are detailed, but no recovery procedure repairs or revalidates an affected artifact after detecting weak verification; searched Counterevidence, Test and Summary.|NOT MET
RISK4|V1 met|Planning validation occurs after the fetch consuming its input; CI search stub ignores filters, exposing failures at input/search dependency boundaries.|MET
RISK5|V1 met|Proposed weak-check-versus-criterion-derived-counterexample comparison explicitly detects the claimed verification gap.|MET
EDGE1|V1 not met|Family counts and mentions of range/size defects do not specify empty/singleton/maximum collection scenarios; searched Mechanism, Incidents and Test.|NOT MET
EDGE2|V1 met|Mechanism identifies cross-component use and execution order; planning incident connects input validation state to an earlier consuming fetch.|MET
EDGE3|V1 met|Oracle labels/counts omit semantic validation; planning validation follows consumption; CI stub ignores effective search filters.|MET
EDGE4|V1 not met|Unspecified range defects, test totals and counting cautions do not describe divergent counting rules or inclusive/exclusive boundaries; searched Incidents, Counting and Test.|NOT MET
EDGE5|V1 met|Monitor incident combines three jobs/many behaviors with structural acceptance and deferred lasting tests; Mechanism explicitly includes cross-component and exceptional paths.|MET
V5 totals|COMP 5/5; COR 5/5; STR 5/5; CLR 4/5; RISK 4/5; EDGE 3/5|26/30 = 86.67%|Correctness: all five met on stated evidence basis; edge eligibility: ELIGIBLE.
V4 totals|COMP 5/5; COR 5/5; STR 5/5; CLR 4/5; RISK 3/5; EDGE 3/5|25/30 = 83.33%|Correctness: all five met on stated evidence basis; edge eligibility: ELIGIBLE.
V3 totals|COMP 5/5; COR 5/5; STR 5/5; CLR 4/5; RISK 3/5; EDGE 3/5|25/30 = 83.33%|Correctness: all five met on stated evidence basis; edge eligibility: ELIGIBLE.
V2 totals|COMP 5/5; COR 5/5; STR 5/5; CLR 4/5; RISK 3/5; EDGE 3/5|25/30 = 83.33%|Correctness: all five met on stated evidence basis; edge eligibility: ELIGIBLE.
V1 totals|COMP 5/5; COR 5/5; STR 5/5; CLR 4/5; RISK 2/5; EDGE 3/5|24/30 = 80.00%|Correctness: all five met on stated evidence basis; edge eligibility: ELIGIBLE.
```

## Source Provenance and Limits
The source aggregate is `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/tool-results/bybsrxops.txt`:

| Actual source | Retained location | What is preserved |
|---|---|---|
|Quantitative evaluator `agent-a5d2062843ae2b975.jsonl`, final record44|Aggregate56-166|Counts, exact executed evaluator rules, hashes and repeatability statement|
|Forward evaluator `agent-a503f9bd5b0246156.jsonl`, final record41|Aggregate167-358|Thirty-criterion dictionary and all150 decisions with evidence|
|Reverse evaluator `agent-a5a65d90e0b48891c.jsonl`, final record46|Aggregate359-547|Independent reverse order and all150 decisions with evidence|
|Actual mechanical comparison|Aggregate548-553|150/150 decision agreement and published-score combined arithmetic|
|Manager `agent-acausal-debate-manager-7197cc83cce2bf57.jsonl`, SendMessage at physical178,2026-10-23T05:26:04.949Z|Captured in score-source-manifest.json|Actual point matrix, one writing win each, tiebreak and dissent metadata|

All named raw agent transcripts reside under the original investigation session's `/subagents/` directory. The full source paths, byte hashes, card hashes, parsed decisions, metric counts and rounding checks are recorded in score-source-manifest.json. Main-source transport restrictions are explicit: workers returned text rather than authoring canonical report files. This artifact assembles their actual results; it is not a fresh scoring pass.

Lexical metrics are reproducible proxies, sensitive to topic aliases, paragraphs, boilerplate and citation digits. IC detects narrow literal opposition rather than all semantic inconsistency; DC's empty denominator is neutral by evaluator choice. Qualitative MET means supported within supplied cards/context, not that primary history was rerun. Full agreement between two evaluations neither establishes unbiased causal truth nor erases disputed causal ordering. No production source, candidate card, debate transcript, invariant probe or merge plan was changed by this assembly.
