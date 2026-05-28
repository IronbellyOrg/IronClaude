# Round 2 — Rebuttal Advocate for Variant 4

## Responses

### 1. Response to the `think_about_*` allowed-tools critique

1. R1 critics are right that V4 is uniquely exposed on the literal
   `think_about_*` surface: diff-analysis marks V4 as the only variant that
   lists the tools in frontmatter (X-006 / C-007), and several R1 reports call
   that a brittle dependency.
2. I accept the frontmatter critique. The three
   `mcp__serena__think_about_*` names should not be part of the minimal
   declared permission surface unless the final harness proves they must be.
3. The R1 critique goes too far when it treats this as a reason to discard V4's
   checkpoint model. V4's load-bearing idea is not the tool name; it is the
   auditable checkpoint outcome.
4. The merged protocol should require three checkpoint rows: evidence
   completeness, task adherence, and final done-ness. Each row should include
   `checkpoint`, `result`, `routing_decision`, and
   `mechanism=serena|inline-fallback|skipped`.
5. If the Serena tools exist, they may implement those checkpoints. If they are
   unavailable, an inline checklist must produce the same audit row and routing
   behavior.
6. This repairs the R1 "deprecated-risk surface" objection while retaining the
   part V4 makes uniquely testable: `checkpoint_logged` assertions against
   observable routing decisions.
7. The V5-side R1 criticism that V4's Testability Map asserts audit rows rather
   than literal tool invocation is therefore a strength, not a weakness. Evals
   should test behavior that affects correctness, not incidental mechanism.
8. V1/V2 optional nudges are less testable because an optional checkpoint cannot
   be relied on during eval triage. V3's total elimination is cleaner but loses
   the chance to measure whether explicit self-scrutiny catches gaps before
   final evidence validation.
9. Updated V4 position: remove the literal tools from frontmatter; keep
   mandatory checkpoint semantics; require fallback parity; assert the audit
   row, not the tool call.

### 2. Response to the `unknown` deviation-class critique

10. R1 critics argue that V4's fifth `unknown` class is an escape hatch that
    defeats deterministic deviation classification.
11. I concede the draft under-specifies `unknown` and lacks V2's precedence
    rule. That is a real defect.
12. I reject the stronger claim that a fifth state is inherently unsound. The
    four substantive classes answer: with enough evidence, is this authorized
    expansion, necessary deviation, drift, or regression?
13. `unknown` answers a prior question: is there enough evidence to classify
    without fabricating certainty?
14. Forcing every insufficient-evidence item into `drift` can create a false
    accusation when the missing artifact may be an approval, task-log entry, or
    external constraint the input did not include.
15. The repair is a two-stage rule: first decide evidence sufficiency; if
    sufficient, apply V2's precedence rule, Regression > Drift > Necessary >
    Authorized; if insufficient, use `unknown` with a `needs-human-decision`
    verdict path.
16. `unknown` must be more expensive than normal classes, not easier. Required
    fields: `evidence_missing`, `why_not_classifiable`,
    `next_evidence_needed`, `owner`, and `decision_needed_by_user`.
17. The Testability Map should add an assertion that no `unknown` row is allowed
    when all required evidence fields are present.
18. V5's R1 position says evidence insufficiency should be only a grounding gap.
    V4 can do both: the ledger row records `unknown`; the report aggregates all
    such rows into Grounding Gaps and blocks clean success for high-stakes rows.
19. Updated V4 position: retain `unknown` only as an evidence-insufficiency
    terminal state; import V2 precedence for all evidence-sufficient cases.

### 3. Response to the T1 `coverage_gap_rate=0` critique

20. R1 critics describe V4's T1 floor as impossible or wasteful. That critique
    lands against V4's wording, not against the underlying safety rule.
21. V4 should distinguish matrix statuses: `mapped`, `not_applicable`,
    `human_decision`, and `gap`.
22. `coverage_gap_rate=0` should count true gaps only. A justified
    `not_applicable` row is not a gap. A surfaced `human_decision` row is not a
    hidden miss.
23. Clean T1 success should still require zero true gaps, low stakes, low
    conflict, and calibrated confidence >=0.85.
24. Caveated T1 should be allowed when non-mapped rows are explicitly justified
    as `not_applicable` or `human_decision` with evidence and owner.
25. Any actual `gap` should route to T2 unless the user explicitly requested a
    quick, non-authoritative scan.
26. This preserves V4's safety while answering the R1 claim that a 1.00 floor is
    unrealistic for normal work.

### 4. Response to the adversarial convergence critique

27. R1 critics correctly identify V4's missing numeric convergence threshold as
    inconsistent with V4's assertion-heavy philosophy.
28. I accept the critique. V4 should import explicit bands: PASS >=0.75,
    PARTIAL >=0.60 and <0.75, FAIL / unresolved below 0.60.
29. The return contract should surface `convergence_score`, `merge_status`, and
    `fallback_reason` when status is not PASS.
30. The Testability Map should assert those fields. This makes V4's delegation
    to `sc-adversarial` measurable without re-implementing debate or scoring.
31. V5's lower 0.65 PASS may be worth future domain calibration, but v1 of a
    gatekeeper should use the stricter default.

### 5. Response to internal-inconsistency and over-engineering critiques

32. One R1 critique says V4 lists `think_about_*` tools while its Testability
    Map checks checkpoint rows rather than tool invocation. I agree with the
    diagnosis and reverse the implication.
33. The fix is not to add tool-invocation assertions; that would make the
    brittleness worse. The fix is to remove the tool names from frontmatter and
    keep the behavior-level assertion.
34. R1 minimalist critiques also treat V4's seven dimensions, semantic
    assertions, and nine waves as excessive.
35. V4's defense is that most of its extra surface is eval-bound machinery, not
    free-form protocol prose: Testability Map, `citation_resolves`, assertion
    types, seeded hardening traps, recommendation scrutiny, and return-contract
    observability.
36. V4's own pruning rule controls bloat: a step that cannot map to a
    deterministic or qualitative assertion should be simplified or removed.
37. That is a better merge discipline than line count alone because it separates
    long-but-testable from short-but-implicit.

## Updated Assessment

38. Variant 4 remains the best base, but only after three explicit repairs:
    remove `think_about_*` from frontmatter, import numeric convergence bands,
    and constrain `unknown` with evidence-sufficiency rules.
39. V4's core advantage remains systemic: it is the only variant organized
    around making protocol decisions fail visibly in eval.
40. V1 contributes convergence bands, richer downstream flags, and useful
    fallback guards.
41. V2 contributes hallucination guardrails, `[INFERRED]` tagging, zero-drop
    audit, and classification precedence.
42. V3 contributes Kill List discipline and a warning against unnecessary
    dependencies.
43. V5 contributes ops integration, env-var degraded-mode handling, and build
    pipeline realism.
44. V4 can absorb these imports through the Testability Map: every imported
    feature must add or strengthen an assertion, stable contract field, STOP
    condition, or explicit boundary.
45. The reverse is harder. A non-V4 base can copy the Testability Map, but it
    was not built around assertion coverage from the start.
46. Therefore the lowest-risk merge is V4 as spine plus targeted imports and
    repairs.

## New Evidence

47. Diff-analysis identifies V4 as the only variant with a dedicated
    Testability Map and marks it high-value under U-007.
48. Diff-analysis also marks V4's `citation_resolves` implementation sketch as
    high-value under U-008 and its assertion types under U-009.
49. These are not aesthetic differences; they are build-path accelerants. A
    grader can be implemented from V4's assertion vocabulary without inventing
    the testing language from scratch.
50. Multiple R1 opposing reports concede this exact point: even advocates for
    other bases name V4's Testability Map as a merge-worthy or uniquely strong
    contribution.
51. By contrast, the strongest criticisms against V4 cluster around local
    decisions: frontmatter allowed-tools, `unknown`, convergence threshold, and
    strict coverage wording.
52. In base-selection terms, systemic testability with local defects is easier
    to repair than local testability grafted onto a non-testability spine.
53. New synthesis rule: judge V4 by whether its mechanisms are observable enough
    to fail during eval. On that criterion it still leads.

## Concessions

54. Concession 1: The three `think_about_*` entries should be removed from
    frontmatter unless the final harness requires explicit enumeration of every
    optional MCP mechanism.
55. Concession 2: Literal Serena checkpoint calls should not be required for
    correctness; inline checklist fallback must be first-class and tested.
56. Concession 3: V4 must import V2's deviation precedence rule; without it,
    `unknown` can be abused and multi-signal cases remain under-specified.
57. Concession 4: `unknown` needs mandatory detection/remediation fields and
    must be forbidden for evidence-sufficient rows.
58. Concession 5: V4 must import explicit adversarial convergence bands,
    preferably PASS >=0.75 and PARTIAL >=0.60.
59. Concession 6: V4's T1 zero-gap wording should be clarified so justified
    `not_applicable` and `human_decision` rows are not treated as gaps.
60. Concession 7: V4 should import V5's env-var degraded-mode handling and a
    compressed ops path, preferably in refs or SPEC content when not runtime
    behavior.
61. Concession 8: V4 should import V3's Kill List discipline, including an
    exclusion for unconstrained new agents and tool-name-dependent checkpoint
    logic.

## Updated Per-Point Positions

### X-001 — T1 coverage floor: `coverage_gap_rate=0`

62. Position: QUALIFY and retain for clean T1 success.
63. `coverage_gap_rate=0` should mean zero true unmapped gaps, not perfect
    fulfillment of every source sentence.
64. Matrix rows must support `mapped`, `not_applicable`, `human_decision`, and
    `gap`.
65. Clean T1 requires zero `gap` rows, low stakes, low conflict, and calibrated
    confidence >=0.85.
66. Caveated T1 may be allowed when every non-mapped row is explicitly justified
    and surfaced.
67. Any real `gap` routes to T2 unless `--depth quick` is explicitly
    non-authoritative.
68. This repair preserves V4's safety while answering R1's false-escalation
    concern.

### X-003 — Adversarial convergence threshold

69. Position: ACCEPT critique and import bands.
70. Use PASS >=0.75, PARTIAL >=0.60 and <0.75, FAIL / unresolved below 0.60.
71. Surface `convergence_score`, `merge_status`, and `fallback_reason` in the
    return contract.
72. Add Testability Map assertions for these fields.
73. Keep `sc-adversarial` as the owner of debate/scoring/merge; V4 only routes
    on the returned metadata.

### X-005 — `think_about_*` in allowed-tools / checkpoint status

74. Position: QUALIFY.
75. Remove literal `mcp__serena__think_about_*` tools from frontmatter.
76. Retain mandatory checkpoint outcomes for collected information, task
    adherence, and final done-ness.
77. Assert `checkpoint_logged` with `checkpoint`, `result`, `routing_decision`,
    and `mechanism`.
78. Serena calls may implement the checkpoint when available; inline checklist
    parity must preserve behavior when unavailable.
79. This reconciles R1's brittleness critique with V4's eval value.

### X-009 — Fifth `unknown` deviation class

80. Position: RETAIN with constraints.
81. `unknown` is not a fifth substantive deviation type; it is an
    evidence-insufficiency state.
82. It is forbidden when the four-class precedence rule can be applied.
83. Required fields: `evidence_missing`, `why_not_classifiable`,
    `next_evidence_needed`, `owner`, and `decision_needed_by_user`.
84. Final reports aggregate unknown rows into Grounding Gaps and block clean
    success for high-stakes unknowns.
85. This avoids fabricated certainty while preventing `unknown` from becoming
    an easy escape.

### A-001 — User can read a 400-700 line SKILL.md

86. Position: QUALIFY.
87. V4 is within the band, but readability still matters.
88. The mitigation is navigability plus testability: keep the Testability Map,
    compress repeated prose, and move non-runtime ops detail to refs/SPEC.
89. User-facing output should be a concise report and return contract, not an
    expectation that the user reads the whole SKILL.md.

### A-002 — `ANTHROPIC_DEFAULT_*` env-var aliases remain set

90. Position: ACCEPT as a V4 gap.
91. Import V5's Wave 0 degraded-mode alias check.
92. Missing aliases should warn, record degraded model topology, and reduce T2
    diversity rather than abort.
93. If no usable reviewer aliases exist, run T1 only, mark degraded confidence,
    and recommend rerun after environment repair.
94. V4's telemetry block is the right place to record this.

### A-003 — `.dev/eval-workspaces/sc-reflect/` and output conventions

95. Position: ACCEPT workspace name; qualify output shape.
96. Use `.dev/eval-workspaces/sc-reflect/`, matching the majority and project
    override.
97. Change V4's default output shape to
    `.dev/reflect/<mode>-<slug>-<timestamp>/` unless a concrete sorting or
    collision reason is documented.
98. Keep the load-bearing rule: never write eval workspaces or generated mirrors
    under `.claude/`.
99. Add output-path assertions for forbidden `.claude/` paths and canonical
    `.dev/` destinations.

### A-004 — `sc-adversarial` Mode A is the right merge mechanism

100. Position: ACCEPT.
101. V4 is strong because it refuses to implement debate, scoring, base
     selection, or merge inline.
102. Add numeric convergence routing around the delegated output; do not
     reinterpret the debate.
103. Require the standard artifacts: diff analysis, debate transcript, base
     selection, refactor plan, merge log, and merged output.
104. Missing or malformed adversarial output should fail closed to PARTIAL with
     a visible fallback reason.

### A-005 — Low confidence / ambiguity should STOP or ask

105. Position: ACCEPT.
106. V4 already supports this through missing-source STOPs, ambiguous-mode STOPs,
     high-stakes blockers, partial downgrades, and recommendation scrutiny.
107. Borrow V1's asymmetric-flag idea where useful so downstream consumers do
     not parse prose for blocker reasons.
108. HIGH-stakes unknown preconditions must block the recommendation.
109. Tier 3 remediation must remain opt-in and must not auto-run `/task`.

## Final Round 2 Position

110. V4 should remain the merge base because it gives the final protocol a
     falsifiable spine.
111. The R1 criticisms identify real local defects, but each has a direct repair
     compatible with V4's philosophy.
112. Remove brittle tool-name commitments; keep checkpoint assertions.
113. Import V2 precedence/guardrails, V1/V2 convergence bands, V5 ops/env
     handling, and V3's Kill List under V4's assertion-map enforcement rule.
114. After those repairs, V4 remains the only candidate that can say every major
     protocol decision is evaluated, logged, or deleted.
