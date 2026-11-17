# Qualitative Score Pass 2 (reverse order: Variant B then Variant A), slot C-05 consumer-entry-effect-and-delivery, 30-criterion binary rubric with CEV

Variant B = adversarial/variant-2-original.md. Variant A = adversarial/variant-1-original.md. Source input for CMP1 = conflict row C-05 (entry, effect, delivery; INV-M, INV-B, INV-N, INV-K, INV-J; consistency with C-01..C-03; effect on PR review and rf-qa; test or measurement; strongest objection). Debate evidence used: debate-transcript.md (intra-variant contradictions, concessions), invariant-probe.md, round1/round2 advocate files, round2.5-fault-finder-raw.md.

## Variant B

CMP1 | Variant B | MET | CLAIM: covers every element of the C-05 row; EVIDENCE: Section 1 (entry, effect, delivery), Section 2 (C-01, C-02, C-03 table), Section 5 (INV-M, INV-B, INV-N, INV-K, INV-J rows), Section 6 (test or measurement), Section 7 (PR review and rf-qa), Section 8 (strongest objection and answer).
CMP2 | Variant B | MET | CLAIM: edge cases and failure scenarios are addressed; EVIDENCE: Section 8 third objection "where the CLI is absent the skill's hard gate returns `skipped` with a null path"; Section 2 C-03 row "INV-007 (`requested` can collapse to 1 when `panel.resolve` drops skipped slots)"; Section 3 B-replace "`skipped` ... degrade the readers".
CMP3 | Variant B | MET | CLAIM: dependencies and prerequisites are stated; EVIDENCE: Section 2 "Dependence on the adjudicated slots C-01, C-02, C-03" table with a "Dependence or disagreement" column; "B does not depend on C-04".
CMP4 | Variant B | MET | CLAIM: success and failure criteria are defined; EVIDENCE: Section 6 item 3 "B is shown wrong if arm D's wrong blockers drive a majority of packages to ESCALATE or to a patch on a non-defect, or if arm D's real-blocking catch is below arm R's. B is shown right on effect if ...".
CMP5 | Variant B | MET | CLAIM: out-of-scope items are stated; EVIDENCE: Section 2 "The post-execution gate T5 ... is outside B"; Section 3 "B does not decide X-15"; "whether to add [the tasklist skill to the plugin] is a separate product question that B does not need to answer".
COR1 | Variant B | NOT MET | CLAIM: contains factual errors that the debate proved; EVIDENCE: Section 3 "workflow contract 1.1 becomes 1.2" is wrong in code (B Round 1 concession 1: `eval_workflow_vs_task_builder.py:1140` and `archive_workspace.py:327-333` require "1.1"; a bump makes /sc:implement refuse); E6 "binds A's route and not B's" overstated and E7 weak (B concessions 2 and 3, debate-transcript.md).
COR2 | Variant B | NOT MET | CLAIM: parts of the approach are not feasible under the stated constraints; EVIDENCE: Section 3 version bump 1.1 to 1.2 breaks the archive and eval readers; Section 3 tasklist-review/plan-review modules and `effect` have no code home (B Round 2: no `tasklist` or `effect` match in `cli/review`; `findings_v2.py:36`); blocking effect placed at Stage 10.5, which is fenced as non-executing (B concession 4).
COR3 | Variant B | MET | CLAIM: terms are used consistently; EVIDENCE: `effect: advisory | blocking`, B-add and B-replace, and the [CODE-VERIFIED]/[UNVERIFIED] tags are used the same way in Sections 1 to 9; E2 names Stage 10.5 advisory while citing its one blocking edge ("needs_human_decision item").
COR4 | Variant B | NOT MET | CLAIM: internal contradictions exist (three listed in debate-transcript.md); EVIDENCE: Section 1 "A tasklist review is allowed to fail at generation time" versus Section 8 answer 1 "B does not add generation-time blocking"; E7 (v2 kernel has no tasklist lens) versus Section 2 (tasklist runs on the v1 engine); Section 3 contract 1.2 versus the pinned "1.1".
COR5 | Variant B | MET | CLAIM: claims carry evidence or rationale; EVIDENCE: Section 4 E1 to E13 each cite file and line (e.g. E1 `sc-workflow-protocol/SKILL.md:89,93,107`; E8 `return-contract.md:16-21`), and unverified items are tagged rather than asserted.
STR1 | Variant B | MET | CLAIM: ordering is logical; EVIDENCE: Sections 1 position, 2 slot dependence, 3 design consequence, 4 evidence, 5 invariants, 6 test, 7 future effect, 8 objection, 9 undecided; forward cross-references (Section 3 to "section 4, item E8") are minor.
STR2 | Variant B | MET | CLAIM: hierarchy depth is consistent; EVIDENCE: nine numbered `##` sections, no uneven sub-heading levels; content is tables and lists throughout.
STR3 | Variant B | MET | CLAIM: sections separate concerns; EVIDENCE: Section 5 holds only invariant verdicts, Section 6 only tests, Section 8 item 4 "Which part carries which argument" separates entry, effect and delivery.
STR4 | Variant B | MET | CLAIM: cross-references are present; EVIDENCE: "see section 4, item E8"; "section 8 says which part carries which argument"; evidence ids E1 to E13 referenced from Sections 3, 5, 8. No table of contents.
STR5 | Variant B | MET | CLAIM: follows the position-paper convention; EVIDENCE: Section 1 position, Section 4 evidence, Section 5 invariants, Section 6 test, Section 8 objection and answer.
CLA1 | Variant B | MET | CLAIM: language is unambiguous with concrete decision rules; EVIDENCE: Section 6 item 3 "a majority of packages", "below arm R's"; no "should consider", "might" or "as appropriate"; unknowns are tagged [UNVERIFIED] rather than hedged. One loose phrase: item 1 "a small share".
CLA2 | Variant B | MET | CLAIM: concrete rather than abstract; EVIDENCE: "`tests/commands/test_workflow_command.py:251-261`", "`scripts/eval_workflow_vs_task_builder.py:1163`", "`set(CONTRACT_KEYS) <= set(contract)`".
CLA3 | Variant B | MET | CLAIM: each section has one purpose; EVIDENCE: Section 2 "how B uses C-01 to C-03", Section 7 "effect on PR review and rf-qa", Section 9 "what the evidence does not decide".
CLA4 | Variant B | NOT MET | CLAIM: many terms are not defined on first use; EVIDENCE: "C-S7", "CO-25", "CO-35", "FX-1", "FX-5", "X-15", "OQ-24", "DO4", "E2" (the study), "P2 loop", "synth-05 6.8.b" appear with no gloss; searched Sections 1, 2, 4, 5 and found no definition list.
CLA5 | Variant B | MET | CLAIM: next steps and decision points are clear; EVIDENCE: Section 6 items 1 to 4 (free checks, two-arm replay, cost) and Section 9 "owner product decisions (DO4 and plugin delivery)".
RSK1 | Variant B | NOT MET | CLAIM: risks are named but not rated for probability and impact; EVIDENCE: No evidence found, searched Sections 5, 7, 8: Section 7 "Risk B puts on them" and the "Endangers" rows (INV-J, INV-G) carry no probability or impact rating.
RSK2 | Variant B | NOT MET | CLAIM: some named risks have no mitigation; EVIDENCE: Section 5 INV-J "Endangers ... Medium handling is X-15, not decided here" (deferred, not mitigated); Section 2 C-02 "INV-001 `need` can be 0, INV-002 ..." listed as open with no mitigation; mitigations do exist for others (Section 7 "`effect` is module data ... a one-field change").
RSK3 | Variant B | MET | CLAIM: failure modes and recovery are covered; EVIDENCE: Section 8 third objection (CLI absent returns `skipped`, "cannot make it worse"); Section 8 answer 3 (`defer` path for a rejected row, B-add advisory as safe starting form); Section 2 "tasklist reviser must read `next` instead of trusting the exit code".
RSK4 | Variant B | MET | CLAIM: external dependencies and failure scenarios are considered; EVIDENCE: Section 8 third objection (whether a marketplace plugin install has the `superclaude` CLI); E13 (shadow runs 13 of 20, EV-1 failures); E9 (plugin copy lags, spec-panel copy 25-line diff).
RSK5 | Variant B | MET | CLAIM: a validation mechanism exists; EVIDENCE: Section 6 "rule registered before the first run" with free checks and the two-arm replay (arm R versus arm D) with loop and cost columns.
INV1 | Variant B | MET | CLAIM: collection boundaries are addressed; EVIDENCE: Section 3 "runs for every phase with `n_tasks > 0`"; Section 2 `need = min(Q, requested)` and INV-007 "`requested` can collapse to 1"; quorum floor `min(2, requested)`.
INV2 | Variant B | MET | CLAIM: state interactions across components are addressed; EVIDENCE: Section 3 `reflect_status`/`reflect_report_path` kept versus `skipped` and null path in B-replace, read by troubleshoot, auggie-review and reflect hand-off (E8); validator tolerance of extra keys at `:1163`.
INV3 | Variant B | MET | CLAIM: guard-condition gaps are identified; EVIDENCE: Section 2 "INV-001 `need` can be 0, INV-002 a regressed non-blocking row in no brief list, INV-003 exit-code-only callers"; E8 closed enum with `skipped` requiring a null path.
INV4 | Variant B | MET | CLAIM: count-divergence is covered; EVIDENCE: Section 5 INV-J "'2 TOTAL passes' ... whether that equals 2 fix cycles is the open OQ-24"; E4 `COMPLEXITY_SCORE` 0-3 range; E12 "five #346 plans" with differing reflect results.
INV5 | Variant B | MET | CLAIM: feature interaction effects are considered; EVIDENCE: Section 8 second objection "B-add reviews each plan or phase twice, and B-replace degrades the readers of `reflect_status`"; Section 4 E9 workflow skill edit forces both trees via the byte-parity pin.

### Variant B subtotals
- Completeness: 5/5
- Correctness: 2/5 (COR3 and COR5 met)
- Structure: 5/5
- Clarity: 4/5 (CLA4 not met)
- Risk Coverage: 3/5 (RSK3, RSK4, RSK5 met)
- Invariant & Edge Case Coverage: 5/5
- TOTAL Variant B: 24/30

## Variant A

CMP1 | Variant A | MET | CLAIM: covers every element of the C-05 row; EVIDENCE: Section 1 and 2 (entry, effect, delivery: "no plugin copy"), Section 4 (C-01, C-02, C-03), Section 5 (invariants incl. INV-M, INV-B, INV-N, INV-K, INV-J), Section 6 (test), Section 7 (PR review, rf-qa), Section 8 (strongest objection).
CMP2 | Variant A | MET | CLAIM: edge cases and failure scenarios are addressed; EVIDENCE: Section 8 objection 2 (quick-depth phases and `--no-reflect` never reach the panel); Section 4 C-03 "A partial panel inside reflect becomes `status: partial`"; Section 3 item 9 plugin-only install ends `skipped|failed`.
CMP3 | Variant A | MET | CLAIM: dependencies are stated; EVIDENCE: Section 4 "Dependency:" line for each of C-01, C-02, C-03 and "Not adjudicated yet and relevant: C-04".
CMP4 | Variant A | MET | CLAIM: success criteria are defined; EVIDENCE: Section 6 item 1 "A is wrong on outcomes if (ii) finds materially more blocking GT items per cost ..."; item 3 contract-compat test; item 4 "A predicts zero pin changes".
CMP5 | Variant A | MET | CLAIM: out-of-scope items are stated; EVIDENCE: Section 2 table "Tasklist Stages 6-10 ... Out of scope"; "rf-qa, PR review: Not affected"; "Which engine feeds T5 is slot C-04, not this slot"; Section 9 open items.
COR1 | Variant A | NOT MET | CLAIM: contains claims the debate disproved; EVIDENCE: Section 3 item 8 "this test must be changed" (withdrawn in A Round 2, the fence diffs against HEAD); Section 3 item 1 "zero edits to their call sites" versus D1 reach (debate-transcript.md); Section 3 item 3 "four" readers of `reflect_status` undercounted (INV-008); "zero pin changes" shown to be a prediction.
COR2 | Variant A | NOT MET | CLAIM: the activation route is not feasible as specified; EVIDENCE: Section 2 "panel's verdict is mapped onto the existing `status`, `coverage_pct`, `tier_reached`" while `coverage_pct` and `tier_reached` are fixed before the engine is read (INV-007); no engine selector for a consumer call (INV-010); no panel-to-status map ever exercised (INV-011).
COR3 | Variant A | MET | CLAIM: terms are used consistently; EVIDENCE: "Tier-2 engine", "`legacy`/`shadow`/`panel`", "advisory at generation time, blocking at the execution gate" are used the same way in Sections 1, 2, 5 and 8; tag legend defined in the header.
COR4 | Variant A | NOT MET | CLAIM: an internal contradiction exists (listed in debate-transcript.md); EVIDENCE: Section 3 item 1 "the panel can be switched on for both consumers with zero edits to their call sites" versus Section 8 objection 2 and item 7 (rule D1: quick-depth phases never reach the panel under any engine).
COR5 | Variant A | MET | CLAIM: claims carry evidence; EVIDENCE: Section 3 items 1 to 10 cite file, line and test (e.g. item 6 `runner.py:540-545`, `:573-580`; item 5 "36 `def test_`"), with [UNVERIFIED] tags where not read.
STR1 | Variant A | MET | CLAIM: ordering is logical; EVIDENCE: Sections 1 position, 2 consequence table, 3 evidence, 4 slot consistency, 5 invariants, 6 test, 7 future effect, 8 objections, 9 open items.
STR2 | Variant A | MET | CLAIM: hierarchy depth is consistent; EVIDENCE: nine numbered `##` sections, numbered item lists and tables, no uneven nesting.
STR3 | Variant A | MET | CLAIM: sections separate concerns; EVIDENCE: Section 2 (design consequence), Section 3 (evidence), Section 4 (slot consistency), Section 9 (open items "not decided here").
STR4 | Variant A | MET | CLAIM: cross-references are present; EVIDENCE: "section 8 objection 2", "item 8", "item 7", the `r11`/`r12`/`r18` research-file shorthand defined in the header. No table of contents.
STR5 | Variant A | MET | CLAIM: follows the position-paper convention; EVIDENCE: Section 1 position, Section 3 evidence, Section 5 invariants, Section 6 test, Section 8 objection and answer.
CLA1 | Variant A | NOT MET | CLAIM: decision rules use vague quantifiers; EVIDENCE: Section 6 item 1 "materially more blocking GT items per cost"; item 2 "If that share is high"; no numeric threshold for either (B asked for one in Round 2, A did not supply it).
CLA2 | Variant A | MET | CLAIM: concrete rather than abstract; EVIDENCE: "`tests/commands/test_workflow_command.py:243-261`", "`contract.py:287-288`", "`--t2-engine panel` is rejected until Stage 3 (`:87`)".
CLA3 | Variant A | MET | CLAIM: each section has one purpose; EVIDENCE: Section 1 "The position in one paragraph", Section 4 "Consistency with the adjudicated slots", Section 9 "Open items this position does not settle".
CLA4 | Variant A | NOT MET | CLAIM: domain terms are not defined on first use; EVIDENCE: "UC-1", "UC-2", "T5" (only partly glossed), "D1", "DO4", "U11", "X-14", "C-15", "INV-020", "E2 study" appear without a gloss; searched Sections 1, 3, 4, 6; only the research-file shorthand is defined.
CLA5 | Variant A | MET | CLAIM: next steps and decision points are clear; EVIDENCE: Section 6 items 1 to 4; Section 8 objection 3 "one controlled change at reflect's default, gated by the section 6.1 and 6.3 measurements"; Section 9 open items.
RSK1 | Variant A | NOT MET | CLAIM: risks are not rated for probability and impact; EVIDENCE: No evidence found, searched Sections 5 and 8: Section 5 "Endangered by A: (a) ... (b) ... (c)" lists three items with no probability or impact rating.
RSK2 | Variant A | MET | CLAIM: each named risk has a stated mitigation; EVIDENCE: Section 5 "Endangered by A" (a) reach is measured by 6.2, (b) INV-L "must happen only after the measurement in section 6", (c) fence test updated "in the same change"; Section 8 objections 1 to 4 each carry an answer.
RSK3 | Variant A | MET | CLAIM: failure modes and fail-open recovery are covered; EVIDENCE: Section 4 C-03 "a refusal ... would map to `failed` with a null path ... an acceptable fail-open outcome for an advisory step"; Section 5 INV-I "advisory steps already fail open (`skipped|failed` and proceed)"; T5 stays fail-closed.
RSK4 | Variant A | MET | CLAIM: external dependencies and failure scenarios are considered; EVIDENCE: Section 4 C-04 dependency ("the 'blocking at the execution gate' half of A is only as strong as the engine C-04 selects"); Section 3 item 9 plugin-only install; Section 7 plugin gap for a future rf-qa.
RSK5 | Variant A | MET | CLAIM: a validation mechanism exists; EVIDENCE: Section 6 items 1 to 4 (entry-effect replay, routing coverage, contract-compat test, call-site non-regression run).
INV1 | Variant A | MET | CLAIM: collection boundaries are addressed; EVIDENCE: Section 3 item 5 `contract.py:287-288` degrades on a single vendor, `:317-326` degrades convergence below 0.80; Section 4 "A partial panel inside reflect becomes `status: partial`"; item 7 depth 0-3 band.
INV2 | Variant A | MET | CLAIM: state interactions across components are addressed; EVIDENCE: Section 3 item 6 "'the panel behind reflect' has two sub-paths" (UC-1 skill and T5 wrapper); item 3 closed enum read by four skills, a test and a validator.
INV3 | Variant A | MET | CLAIM: guard-condition gaps are identified; EVIDENCE: Section 4 C-03 "workflow Wave 4 would see a refusal where its contract only knows `skipped|failed`"; Section 3 item 7 "quick-depth ... never reach a panel" (rule D1 guard).
INV4 | Variant A | NOT MET | CLAIM: no count-divergence scenario is analysed, and its own reader count diverged; EVIDENCE: No evidence found, searched Sections 3, 5, 6, 8: Section 3 item 3 states "four" readers of `reflect_status`, which the fault-finder shows undercounts (INV-008); Section 8 only mentions "the 3-review cap" and "2 passes" without examining the mismatch.
INV5 | Variant A | MET | CLAIM: feature interaction effects are considered; EVIDENCE: Section 5 INV-L and INV-K "(b) INV-L at the engine switch; (c) the edit-fence test at the engine switch"; Section 4 C-03 quorum refusal applied to the reflect profile.

### Variant A subtotals
- Completeness: 5/5
- Correctness: 2/5 (COR3 and COR5 met)
- Structure: 5/5
- Clarity: 3/5 (CLA1 and CLA4 not met)
- Risk Coverage: 4/5 (RSK1 not met)
- Invariant & Edge Case Coverage: 4/5 (INV4 not met)
- TOTAL Variant A: 23/30

## Summary
Variant B 24/30, Variant A 23/30. The only criteria on which the two differ are CLA1 (B met on the concrete decision rules in Section 6 item 3), RSK2 (A met because each of its three endangered items has a stated precondition; B defers INV-J and leaves C-02 INV-001/002 without mitigation) and INV4 (B met via the OQ-24 cap-count mismatch; A not met). Both fail COR1, COR2, COR4, CLA4 and RSK1.
