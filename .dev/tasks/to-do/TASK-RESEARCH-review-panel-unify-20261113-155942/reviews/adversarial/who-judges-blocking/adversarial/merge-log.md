# Merge Log

## Metadata
- Merge executor: merge-executor agent (Step 5 of /sc:adversarial, Mode A). It makes no strategic decision and does not override the plan.
- Base: Variant B (`adversarial/variant-2-original.md`, Option D blind grader, normalized copy)
- Non-base: Variant A (`adversarial/variant-1-original.md`, Option A hardened veto)
- Plan executed: `adversarial/refactor-plan.md` (20 changes, independently reviewed, auto-approved)
- Evidence consulted: `debate-transcript.md`, `invariant-probe.md`, `base-selection.md`, `diff-analysis.md`
- Output: `proposal-merged.md` (parent folder of `adversarial/`)
- Merge date: 2026-11-14T01:18:57Z (UTC, `date -u`)
- Method: the merged file was written incrementally, header and Decision summary first, then one section at a time. The log entries below are in change order (1 to 20); the document was built in section order, with the Rollout subsection (Change 15) inserted into Design when Change 15 was applied.

## Plan-versus-source conflicts found (recorded once here; handling stated in each entry)
1. The plan's Change 10 gives Advocate A's panel-size subset as "1.33, 1.21, 1.50 and 1.00". Advocate A's own table lists n=5 as two rows, 1.75 and 0.25; the figure 1.00 is the mean of those rows as computed by Advocate B (Round 2, G4). Handling: the merged text prints A's two n=5 rows and says the mean 1.00 is B's computation. Both tables are tagged advocate-computed, not re-aggregated.
2. The plan's Overview says "five High changes"; the plan's own change list and Risk Summary rate six changes High (1, 3, 5, 6, 8, 15; Change 7 is Medium-High). Handling: no effect on the merged text; recorded here for the orchestrator.
3. The plan's Change 17 asks for the invariant evidence "exactly as in invariant-probe.md". The INV-019 evidence cell says "see the citation note above", which points at the probe's header, not at a note in the merged table. Handling: the cell text is kept and the pointer reads "see the note below the table"; the note below the table states that `research/05-blocking-calibration.md:311` was not borne out by the orchestrator's spot check and that the control-package fact stands on Variant B R1 and `research/11` section 5.
4. The plan's Change 1 integration point suggests the sentence "the existing, unhardened veto decides today". The merged text says "what runs today is the existing, unhardened veto" instead, so that no sentence can be read as the hardened veto deciding today (rule R-1). Same meaning, no loss.

## Change Entries

### Change 1: Staged-decider position and decision summary
- **Status**: Applied
- **Source**: Variant A Design "The decision"; Variant B Design "Position"; transcript rows C-001, C-004, C-013; plan Overview decision list (PR-001, PR-002)
- **Target**: Base Design "Position" (restructured); new "Decision summary" H2 before the template sections, with a "Terms used in this document" H3 (also serves Change 19)
- **Before**: Position said "Reviewers propose, a blind grader decides, code counts" and that the reviewer flag "stops being the decision".
- **After**: Position states four stages (today: the unhardened veto runs; interim target: the hardened veto; shadow grader; per-lens live grader after the replay). The Decision summary prints the seven agreed items, each with the INV IDs that qualify it, labels the cap "cost cap only; precision effect open (C-005)", lists the three agreed-open points and the 11 HIGH invariants, and has a "Not decided here" paragraph.
- **Provenance tags**: `Base (original, modified) - Change 1`; `Debate record - Decision summary, merged per Change 1`
- **Validation**: structure OK (Decision summary H2 precedes the seven template H2s; glossary is H3 under it). References: every INV ID printed exists in the probe. Contradictions: no sentence says the hardened veto runs or decides today (checked by grep at the end). Plan conflict 4 (wording of "decides today") recorded above.

### Change 2: Interim rule, the hardened veto
- **Status**: Applied
- **Source**: Variant A Design (veto rule, four input fixes); Round 2 A concessions 2 and 7; facts F1, F6; plan Change 2
- **Target**: New Design subsection "Interim rule: the hardened veto (a target; the unhardened veto is what runs today)", placed before the grader subsection
- **Before**: Variant A's Design presented the rule as "what `ledger.py:187,213-218,274` and `cluster.py:375` already do", with four fixes "decided elsewhere".
- **After**: The rule plus a four-row prerequisite table with the debate's corrections: named resolver (C-007), D2 as a code change at `ledger.py:254-257` that inverts the pin at `test_review_ledger.py:376-385` (INV-013), complete-link as a C12 dependency, per-lens predicate (C16, INV-016). `ledger.py:187` (v1) and `cluster.py:375` (v2) are stated as two copies. A's FAIL-set-bounds-every-decider claim is dropped (X-001) without restating it; the cap is kept only as a cost cap.
- **Provenance tags**: `Variant A, Design "The decision" ... merged per Change 2`
- **Validation**: structure OK (H3 under Design). References: INV-005, 006, 009, 011, 013, 014, 016, 025 exist; C-005, C-007, C-015, A-007, X-001 exist. No restated subset claim.

### Change 3: Certification rule and verdict vocabulary
- **Status**: Applied
- **Source**: Variant A Design "Asymmetric verdict"; Variant B verdict logic and CLI table; transcript rows C-002 (HYBRID 73%), C-010, X-005 (HYBRID 69%); Round 2 A concession 5, F7, `defer()`; Round 2 B G2
- **Target**: New Design subsection "Certification and verdict vocabulary" (the edits to the base "Verdict logic" and "CLI surface" are in Changes 9 and in How it works)
- **Before**: Base had no reviewer-count guard (one reviewer plus an approving grader yields PASS) and `defer()` bypassed PENDING; Variant A's degrade rule was unscoped.
- **After**: (a) first review with fewer than two valid blocks returns PASS with `degraded: true`, set at round 1 and inherited; exits 0/10/11 unchanged; flag in the round record and a report line before `verdict:`; `verdict()` key set unchanged. (b) `defer()` recomputes `degraded` and, under `--decide grader`, PENDING. (c) PENDING and exit 12 only under `--decide grader`, with an `EXIT_BY_DECISION` entry (KeyError otherwise). Open points kept visible: INV-004, INV-007, INV-024 (and INV-009); INV-003 stated as addressed.
- **Provenance tags**: `Variant A, Design "Asymmetric verdict" (U-001) combined with Base ... merged per Change 3`
- **Validation**: structure OK. References: `ledger.py:356-360`, `ledger_cmd.py:13,109`, `test_review_ledger.py:299-304` and `:468-472` are the plan's citations. INV-004, 007, 009, 024, 003 exist. No claim that the open points are fixed.

### Change 4: Candidate rule, promotion and singleton handling
- **Status**: Applied
- **Source**: Variant B "What the core does" step 1; Variant A "Record who and how many"; transcript C-003 (HYBRID 68%), C-004 (HYBRID 64%), X-001
- **Target**: "Candidates, promotion and singletons" (H3 with H4s: Candidate rule, Evidence gate and named resolver, Promotion and `singleton_blockers`, Recording)
- **Before**: Candidate rule v2-only; `promoted` could in principle block; no `singleton_blockers`; shadow counts said to make the choice "checkable after rollout".
- **After**: B's candidate rule kept for v2, v1 form added (`blocking or severity in {MAJOR, CRITICAL}`, no channel test); `singleton_blockers` added to cluster output and telemetry, read by no decision; in shadow `promoted` cannot raise a FAIL; A's subset claim stated as dropped (X-001) and not restated either way; the "checkable after rollout" sentences are qualified: the counts measure disagreement, not who is right (INV-023). The base sentence in P4 is handled in Change 11.
- **Provenance tags**: `Base (original, modified) - ... Change 4`
- **Validation**: structure OK. References: C-003, C-004, X-001, INV-023 exist. Rule R-7: the subset property is not stated in either direction.

### Change 5: Grader reply contract and rubric versioning
- **Status**: Applied
- **Source**: Variant B "The grader and its rubric" and "Reply, validation and failure handling"; transcript X-006 (HYBRID 78%), Round 2 B concession 4; INV-008, INV-021
- **Target**: "The grader and its rubric" with an H4 "Reply contract: what was agreed, what is proposed, what is open"; the mechanical reply handling stays in How it works (Change 8/9 area)
- **Before**: P4 "fail-closed by construction"; the rubric `spec-v1` copied verbatim; the reply was boolean.
- **After**: "Fail-closed on procedure only" is stated; the demotion rule is presented as the agreed outcome and the tri-state reply as Advocate B's proposal; the probe findings are printed: schema change at `stoprule.py:808-830` (INV-008), selector for `undecidable` not agreed, named criterion checked by format only (`why` of at most 25 words, `stoprule.py:813`; INV-021), claim-shape precondition conceded by B but not in the consensus list. `spec-v2` is the new rubric version; `spec-v1` stays the live stoprule rubric.
- **Provenance tags**: `Base (original, modified) - ... Change 5; rubric inventory per Change 7`
- **Validation**: structure OK. References: X-006, INV-008, INV-021, INV-015 exist. The base phrase "fail-closed by construction" appears only inside quotes describing the dropped claim (grep at the end).

### Change 6: Evidence gate, named resolver and seal rule
- **Status**: Applied
- **Source**: Variant A Design item 1; Variant B step 2 and "What the grader sees"; transcript C-007 (HYBRID 66%), A-003 (QUALIFY 58%); Round 2 B G5
- **Target**: H4 "Evidence gate and named resolver" under "Candidates, promotion and singletons"; the grader-input table in How it works carries the matching `unverified` rule
- **Before**: `unverified` evidence was graded as true-but-noted; stoprule's seal rule was not ported; no resolver was named.
- **After**: The agreed rule, the A-003 condition verbatim, the resolver named per path (v2: `verify-citations` and the evidence-validator; v1: `anchor_status`/`span is None`, no re-read resolver today), the stoprule behaviour (`stoprule.py:264-265,283-284,541-553,590`) and why porting it to v1 means suppression without a resolver (PR-010). The seal rule is presented as B's proposal. Open: INV-005, INV-006, INV-025, INV-014; the 13 null-span blocking rows are tagged `[VIA audit-D]`.
- **Provenance tags**: `Base (original, modified) + Variant A Design item 1 ... merged per Change 6`
- **Validation**: structure OK. References: C-007, A-003, INV-005, 006, 014, 025 exist. Nothing is described as safe.

### Change 7: Reflect-post predicate and reflect integration
- **Status**: Applied
- **Source**: Variant A per-lens predicate and reflect consumer row; Variant B `reflect-post-v1` and "Reflect Tier 2"; transcript C-008 (HYBRID 70%), C-011 (EQUAL 70%), A-001 (QUALIFY 60%)
- **Target**: Base lens table and "What each consumer does" (this entry); the full predicate subsection is "Reflect-post: code predicate" in How it works, written with Change 9
- **Before**: `reflect-post-v1` grader class assignment; `reflect-pre-v1` as a new rubric.
- **After**: Rubric inventory table: only `spec-v2` ships; `reflect-post-v1` dropped (code predicate); `reflect-pre` not decided and listed under Owner decisions. Consumer bullets: debate and contract 1.8.0 kept; grade stage for the spec and tasklist lens writes only to nested `telemetry:`; authority only via a contract bump after a paired run (G-57); A-001 stated.
- **Provenance tags**: `Base (original, modified) - ... Change 7`
- **Validation**: structure OK. References: C11, C17, G-57, A-001 exist. The two predicate rules are named in the How-it-works subsection (both cited lines come from the plan).

### Change 8: Document-loop adapter and the two-copy rule
- **Status**: Applied
- **Source**: Variant B "How it works" data flow and "Reflect-post"; Variant A Design step 6; transcript Round 2 A F1 and B G1; C-015 (A at 80%); INV-011, INV-017
- **Target**: Base "How it works" data flow (now two variants) and a new subsection "Adapters and the two copies of the rule"
- **Before**: Base presented the v2 flow as the one flow and said `merge --decide grader` "clusters through `merge_round`"; K1 treated v2 fields as available on the document loop.
- **After**: A v2 flow and a v1 flow; v1 candidate rule, pre-check and renderer stated; the v1 renderer must be blind (PR-018); the parity test spans both copies (`ledger.py:187`, `cluster.py:375`); `diffgate.py:796` and `stoprule.py:1179-1191` named as further copies with scope undecided (INV-017); INV-011 kept visible (representative claim per cluster, frozen; "tighten `same_defect`" has no mechanism or test). The 50-100 lines are tagged `[estimate; Advocate B, not measured]`.
- **Provenance tags**: `Base (original, modified) - ... Change 8`; `Variant A Design step 6 ... merged per Change 8`
- **Validation**: structure OK (H3 under How it works). References: C-015, A-007, INV-011, INV-017 exist; all line references come from the plan, transcript or probe. No new line numbers invented. The grader-input table keeps B's content; the `unverified` rule was added there for Change 6 consistency.

### Change 9: Contract fields and CLI surface
- **Status**: Applied
- **Source**: Variant A contract-fields table; Variant B `review-decisions/1` and CLI table; transcript C-010 (HYBRID 65%); PR-021
- **Target**: Base "Contract fields" and "CLI surface"; base "Reply, validation and failure handling" and "Verdict logic" were carried through the same renames
- **Before**: Two separate field tables; `decision: blocking/not_blocking/unconfirmed` inside the grader record and `decision REVISE` in the verdict block (the K3 collision); exit 12 without the `EXIT_BY_DECISION` entry named.
- **After**: Two merged field tables (B's `lens`, `rubric_id`, `rubric_sha256`, `grader`, `batches[]`, `clusters{}`, `summary`; A's `blocking_effective`, `anchor_status`, `rejected_lines[]`, `partial`, `degraded`, `singleton_blockers`); exits 0/10/11 kept; the CLI table names both places that change for PENDING (`ledger_cmd.py:13` and `:109`) and lists `degraded` and `PENDING` as the new values; INV-002 and INV-018 are flagged as open; the verdict pseudo-code uses `grade` and keeps `decision` for REVISE/ESCALATE; the reflect-post subsection (Change 7) was written here as "Reflect-post: code predicate" with both rules named.
- **Provenance tags**: `Base (original, modified) - ... Change 8` (the How it works header) and per-subsection comments where a block was rewritten
- **Validation**: structure OK. The old collision terms were replaced everywhere in this section (grep at the end). References: INV-002, 007, 016, 018 exist; C-006 narrowing cites `ledger.py:235` from the transcript.

### Change 10: Evidence corrections
- **Status**: Applied
- **Source**: Variant B V7 and P1; Variant A E-3, E-5, E-7; transcript Round 2 A concessions 2-4, B concessions 1-2 and G4; S-003 (EQUAL), X-002, X-003, X-004, C-005, C-012
- **Target**: Base Evidence tables A-E, a "Counter-reading" column on EVERY table, and a new "Evidence corrections" subsection (EC1-EC6)
- **Before**: B's source-column tables only; V7 omitted D1; P1 claimed E2 measured the size effect; no counter-reading column; A's reasoning sat inline in E-1 to E-17.
- **After**: Counter-reading column added to tables A, B, C, D and E; A's E-1 to E-17 moved into it as matching rows (E-1 to V1, E-2/E-6 to V3, E-3 to V2, E-4 to V5, E-5 to V7 and V11, E-8 to V8, E-9 to V6/X5/X11, E-10 to F4/X8, E-11 to G1/G2/G6/X2, E-12 to F5/X3, E-13 to F1/V9, E-14 to V10, E-15 to X1/X4, E-16 to F2, E-17 to the test table in Test coverage); A-only items added as V10, V11 and X11. Tags `[READ]`, `[VIA ...]`, `[E2 4a22d74]`, `[external]` kept, plus `[advocate-computed, not re-aggregated]` and `[estimate]`. EC1-EC6 apply the corrections; the control-by-size table prints B's full-table figures (n=1 1.00, n=2 1.27, n=3 1.05, n=4 1.33, n=5 0.89), B's audit-clean subset and A's selected rows, all tagged advocate-computed (plan conflict 1: A's n=5 "1.00" is B's mean of A's two rows, stated as such). `ember + sonnet` 0.25 (defect-rich) versus 1.25 (control) stated. E-5's contamination excuse and E-7's cap-as-precision are dropped; E-14 is carried as `[VIA research/09 and 13]`. The 13 null-span rows are tagged `[VIA audit-D]`.
- **Provenance tags**: `Base (original, modified) - ... Change 10 (S-003, EQUAL)`
- **Validation**: structure OK (H2 Evidence with H3 A-E and "Evidence corrections"). References: V/G/K/F/X IDs in the Correctness argument and Risks resolve to rows (checked at the end). X-002, X-003, X-004, C-005, C-006, C-012 exist.

### Change 11: Correctness argument rewrite
- **Status**: Applied
- **Source**: Variant B Correctness P1-P5 and "Weakest point"; Variant A Correctness steps 1-8; transcript C-006 (B at 63%), C-013 (B at 71%)
- **Target**: Base "Correctness argument"
- **Before**: P1 "E2 measured that direction"; P4 "fail-closed ... by construction"; A's step 1 (subset claim) and step 2 ("FAIL is the right verdict" snapshot argument).
- **After**: P1 rewritten per EC2 (per-candidate false-block rate; E2 neither supports nor refutes a size effect; falsifier necessary, not sufficient, INV-019); P2-P3 kept with the recall-floor caveat; P4 rewritten per Change 5 (fail-closed on procedure only; frozen grade only after the flip and only for unchanged cited text; veto record shows disagreement); P5 narrowed (INV-016); P6 added from A's step 4 with its limit (the re-find rate is unmeasured); "Properties of the interim rule" from A steps 3 and 5 (within-round monotonicity limited by INV-001); "Why a staged grader over the other deciders" table; "What this argument does not establish" for both options (A's step 8) listing INV-001, INV-006, INV-019, INV-020 plus INV-011, INV-021, INV-023. A's steps 1 and 2 are deleted, not restated; A's steps 6 and 7 are not carried (their claims were conceded: contamination direction, "only option that leaves every pin alone").
- **Provenance tags**: `Base (original, modified) - ... Change 11`
- **Validation**: structure OK. References: EC2, EC4, EC1, V/G/X/F row IDs and INV IDs resolve. No "measured that direction" claim remains (grep at the end). The subset property is not stated in either direction.

### Change 12: Risk table merge with likelihood bases
- **Status**: Applied
- **Source**: Variant B R1-R11 (base table); Variant A Risks 1-8; the re-evaluated R1 standard in `base-selection.md`; S-004 (B)
- **Target**: Base "Risks and mitigations" table, with new columns "Likelihood basis" and "Consequence" (the Residual column is kept)
- **Before**: R1-R11 with Risk, Mitigation and Residual; residuals in modal words; no likelihood basis.
- **After**: 22 rows. R1-R11 kept and updated (R1 now points to the Rollout gate; R2 and R5 reflect the code predicate and the demotion rule; R8 no longer cites "the D9 conflict" and says what it means); A's Risks 1-8 carried as R12 (self-grading, 27 over-graded), R13 (one reviewer clears a row, INV-001), R14 (promotion into reflect, now the reflect-authority bump), R15 (correlated reviewers), R16 (thin evidence: 3 packages, 16 defects, n of 4-6), R17 (degraded outcomes: 80 invalid-block cases, INV-009), R18 (chained clusters); A's Risk 1 (weakest point) is carried in "What this argument does not establish" and R1/R12/R22. Debate risks added: R19 (v1 adapter uncosted, `[estimate]`), R20 (`defer()` and PENDING), R21 (grader pins `model: sonnet`, non-Anthropic unverified), R22 (replay passable by an always-demoting grader, INV-019). Every row has a likelihood basis or "no basis recorded".
- **Provenance tags**: `Base (original, modified) - ... Change 12 (S-004)`
- **Validation**: structure OK (one table, six columns on every row). References: V8, X-series, G7, INV-001/004/007/008/009/011/017/019/020/021/022/023/024 and C-003, C-005, C-011, C13, C20, G-03, G-04, G-05, G-57, G-59 all exist. No row claims a rate that no source gives.

### Change 13: Test plan merge with corrected accounting
- **Status**: Applied
- **Source**: Variant B 16 new-test groups and existing-tests table; Variant A items 1-9; transcript C-014 (HYBRID 65%), S-006 (HYBRID 63%); Round 2 A F2
- **Target**: Base "Test coverage needed"
- **Before**: B's table omitted the one-reviewer PASS pins, `defer`, the exit-code pins and the exact-dict pin; A's list kept `:279-300` green while changing `:296-298` and claimed "only option that leaves every pin alone".
- **After**: One existing-tests table with the plan's accounting (`:128-129` and `:518-544` stay green under `--decide flag`; `:376-385` and `:408-417` change under the prerequisites; `:299-304` breaks only if `verdict()` gains a key, so `degraded` goes elsewhere; `:296-298`, `:307-315`, `:396-403`, `:468-472` gain a `degraded` assertion and the last pins the last report line; `test_review_cli.py:328-348` exit 0 and PASS). New tests 1-16 from B with the two adjustments (v1 and v2 renderer blindness; reflect-post group now tests the code predicate; selection and data files cover `spec-v2` only), additions 17-23 from A and the debate (rule parity across both copies, monotonicity, effective flag, `singleton_blockers`, `defer` recomputation, `EXIT_BY_DECISION` with PENDING, reflect isolation), and probe-derived tests 24-27 marked "not agreed in the debate" (INV-020, 019, 008/010, 014).
- **Provenance tags**: `Base (original, modified) - ... Change 13 (C-014 and S-006, HYBRID)`
- **Validation**: structure OK. All test line numbers are the ones given by the plan, the variants or the transcript; none invented. Test 10 is worded conditionally because the owner has not chosen between the two reflect-post rules.

### Change 14: Cost merge
- **Status**: Applied
- **Source**: Variant A Cost; Variant B Cost; transcript C-015 (A at 80%); INV-010; PR-007, PR-015
- **Target**: Base "Cost"
- **Before**: One cost story at effort L; "a full batch is 25% canary overhead"; three rubrics and three canary files; the owner-decision list sat in Cost; A's Cost carried a separate "cost of being wrong".
- **After**: Two cost lines (interim: effort S, zero extra model calls, D2 about three lines `[estimate; Advocate A]`; destination: effort L with `grade.py` 300-400, `grade_cmd.py` about 150, `ledger.py` 40-60, all `[estimate]`, plus the v1 adapter 50-100 lines `[estimate; Advocate B, not measured]`); one rubric (`spec-v2`) and its canary file in the first build; benchmark cost about 380,000 REVIEWER OUTPUT tokens for six replicates (6 x 63,644, `CR:331`) tagged `[advocate-computed, not re-aggregated]`, judge passes and judge re-run not costed; canary overhead as one formula (canaries / (claims + canaries) per batch, two canaries per batch, 25% only for a six-claim batch, 67% of items or 200% relative to the one real claim for a 1-claim batch, INV-010); A's "cost of being wrong" (U-008) carried; the owner-decision paragraph moved to the "Owner decisions" section (Change 18) with a pointer left in Cost. During the build one sentence in "Cost of keeping the veto alone" that said E2 measured more wrong blockers as reviewers were added was corrected to match EC2 (it contradicted the agreed X-004 outcome).
- **Provenance tags**: `Base (original, modified) - ... Change 14 (C-015, A at 80%)`
- **Validation**: structure OK. References: C-015, INV-010, G4, G7, V1, V3, V5, V7, V8, EC1, EC2 resolve.

### Change 15: Replay and acceptance gate
- **Status**: Applied (inserted into Design as the last subsection "Rollout", replacing the placeholder left when Change 7 was applied)
- **Source**: Variant B R1 and "Rollout"; Variant A Test item 9 and Risk 1; transcript C-013 (B at 71%), C-012 (OPEN at 71%); Round 2 B concession 7
- **Target**: Base "Rollout" and R1 (R1 was rewritten in Change 12 to point here)
- **Before**: Four rollout steps; the pass condition in R1; no numeric threshold and no statement of what the gate cannot show.
- **After**: Step 0 (prerequisites: D1, D5, D6 fixed first and "D1 fixed" defined as an open point, INV-014; claim-shape fix and `spec-v2` before shadow, INV-015, INV-021), steps 1-4 as staged, then the gate: paired and pre-registered, same candidate sets, both arms scored against `blocking_in_implement`, known E2 wrong blockers as a leniency probe, true-negative rate reported, canary and benchmark sets disjoint, inconclusive result keeps the grader in shadow; B's qualitative pass criterion kept; "pooled" for the 71 valid-era rows; the D1 candidate-set break noted. A six-item "What the gate does not settle" list: no numeric threshold and an always-demoting grader meets the criterion (INV-019), low power (INV-022), no rounds 2-3 (INV-020), shadow counts measure disagreement (INV-023), pre-`spec-v2` shadow data (INV-015), v1 anchors unverified and the judge re-run uncosted.
- **Provenance tags**: `Base (original, modified) - Rollout ... Change 15 (C-013, B at 71%; C-012, OPEN at 71%; S-005, B)`
- **Validation**: structure OK (H3 under Design, last in Design; the placeholder comment no longer exists, checked by grep). Contradictions: the replay is not called sufficient anywhere; "inconclusive keeps the veto live" is stated.

### Change 16: "Unresolved conflicts" section
- **Status**: Applied
- **Source**: transcript Convergence Assessment; Round 2 tracking rows C-005, C-012, X-002 and A-001, A-003, A-007; scoring-matrix confidences (OPEN 73%, 71%, 69%; QUALIFY 60%, 58%, 60%)
- **Target**: New H2 "Unresolved conflicts" after "Cost"
- **Before**: Absent (the base carried open points only as scattered "not decided" phrases).
- **After**: A three-row table (C-005, C-012, X-002), each with the agreed-open position, "the measurement the debate named; it may not decide" and the limits (INV-019, 020, 022; per-panel n of 4 to 6; D1 pushes counted wrong blockers down while D5 and D6 may push either way, direction not agreed); then a three-row QUALIFY table with the condition and the agreed confidence written as in the plan: A-001 (60%), A-003 (58%, INV-006 and INV-025 attached), A-007 (60%, INV-011 attached).
- **Provenance tags**: `Debate record - Unresolved conflicts ... Change 16`
- **Validation**: structure OK (H2 after Cost; H3s under it). Count: 3 agreed-open rows, 3 QUALIFY rows. No row says the replay decides.

### Change 17: "Unaddressed invariants" section
- **Status**: Applied
- **Source**: `invariant-probe.md` (25 findings)
- **Target**: New H2 "Unaddressed invariants" after "Unresolved conflicts"
- **Before**: Absent.
- **After**: A heading paragraph stating this is the debate's list of what it did not resolve and not a completed to-do list; a 25-row table (ID, category, assumption, status, severity, one-line evidence, where used in this document with the plan change numbers), ordered 11 HIGH UNADDRESSED (INV-001, 004, 005, 011, 014, 019, 020, 021, 023, 024, 025), then 10 MEDIUM UNADDRESSED (002, 006, 007, 008, 009, 010, 015, 016, 017, 022), then 2 LOW UNADDRESSED (013, 018), then the 2 ADDRESSED (003, 012). Severities and statuses are as the probe set them; evidence cells are the probe's table cells verbatim apart from the INV-019 pointer (plan conflict 3). A notes block defines M1-M12 (the probe's labels), carries the INV-019 citation note and the counts.
- **Provenance tags**: `Debate record - Unaddressed invariants ... Change 17`
- **Validation**: structure OK. Count: 25 rows (checked by grep at the end). No item is rewritten as resolved; no severity or status softened.

### Change 18: Owner decisions merge
- **Status**: Applied
- **Source**: Variant A Cost "Owner decisions"; Variant B Cost "Decisions this proposal needs from the owner"; transcript
- **Target**: New H2 "Owner decisions" after "Unaddressed invariants" (the lists were removed from Cost; Cost keeps a pointer)
- **Before**: A: one new number (the control-package tolerance) plus two reflect-post questions; B: MINOR drift, the producer of `unauthorized_deviation_present`, static unreachability, the environment (C03, O-2), the benchmark-port owner, who authors the rubrics.
- **After**: One merged table of 16 decisions with the invariant each is attached to (the first draft of the table had 22 entries; entries 17-22 were not in the plan's list and were removed, so no content was added beyond the plan; as a consequence INV-004, INV-007, INV-009 and INV-020 have no owner-decision entry, which the section says); includes the plan's list (tolerance and numeric pass threshold, reflect-post predicate, reflect-pre rubric, MINOR drift G-03, `unauthorized_deviation_present` G-04, static unreachability G-05, C03/O-2, benchmark-port owner G-59, who authors the rubrics, degraded-PASS vocabulary C19, diffgate/stoprule scope, `undecidable` selector, claim-shape fix, ledger schema bump) and the open phrases the plan told me to replace (lines of cited text and cap on citations per item; "owner-set tolerance"; how `same_defect` is tightened).
- **Provenance tags**: `Base (original, modified) / Variant A ... Change 18`
- **Validation**: structure OK. References resolve (INV IDs, G-numbers, C-numbers). No decision is presented as taken.

### Change 19: Terminology and clarity fixes
- **Status**: Applied (a whole-text change; applied while each section was written and then by a scan-and-fix pass after the last section)
- **Source**: re-evaluated K3 for B; L1 and L4 for both variants in `base-selection.md`
- **Target**: whole merged text
- **Before**: "decision" meant both the grader outcome (`decision == blocking`) and the ledger routing word; "class" meant model class and deviation class; E2, D1-D6, C-numbers, UC-1/UC-2, B1-B3, veto, candidate and shadow were used before definition; open phrases "(names proposed)", "design parameters to fix at build time", "owner-set tolerance", "to be tightened".
- **After**: The grader outcome is `grade` (`blocking`, `not_blocking`, `undecidable`, `unconfirmed`); `decision` stays the ledger routing word (PASS, REVISE, ESCALATE; PENDING under `--decide grader`); the model class is `model_class` and `deviation_class` keeps its name. A "Terms used in this document" block under the Decision summary defines E2, D1-D6 (D4 stated as unused), UC-1/UC-2, B1-B3, veto, candidate, shadow, `grade`, `decision`, `model_class`, INV, U-nnn and S4, gives one line for each of the 14 synthesis conflicts cited (C02, C03, C04, C05, C07, C11, C12, C13, C14, C15, C16, C17, C19, C20), the open items G-03, G-04, G-05, G-57, G-59, O-2, and a pointer row for the debate point IDs (all 33 are defined by topic in the Debate record table). Open phrases were replaced: "names proposed" was dropped in favour of the concrete command names; "design parameters to fix at build time" became Owner decision 15; "owner-set tolerance" became Owner decision 1; "to be tightened" became Owner decision 16. The file and schema names `panel/decisions.json` and `review-decisions/1` keep the base's word; the text says each entry carries a `grade`.
- **Provenance tags**: terminology edits sit inside blocks already tagged; the glossary block is tagged `Base (original, modified) - glossary added ..., Change 19`
- **Validation**: scan results are in "Post-Merge Validation" below (old-term grep: each remaining hit is a quotation of a replaced claim, the real `decision == "PASS"` assertion of `test_review_cli.py`, or a probe row kept verbatim).

### Change 20: Debate record, provenance and status banner
- **Status**: Applied
- **Source**: transcript; `base-selection.md`; Step 5 provenance rules
- **Target**: top banner (written with the first block) and the closing H2 "Debate record and provenance"
- **Before**: No banner; the base carried no debate record.
- **After**: Banner: status PARTIAL; alignment 90.9% (30 of 33 points with a determinate agreed outcome); convergence NOT achieved, blocked by invariants (11 HIGH UNADDRESSED); 3 agreed-open points. Closing section: status paragraph with the same qualifiers, points won (B 6, A 2, HYBRID 13, EQUAL 6, OPEN 3, QUALIFY 3), a 33-row table (ID, level, topic, agreed outcome) copied from the Round 2 tracking table, a "Where each contribution went" list (U-001 to U-017), and an artifact table with pointers. Provenance comments precede each section.
- **Provenance tags**: `Debate record - status banner, Change 20`; `Debate record - Debate record and provenance ... Change 20`
- **Validation**: 33 rows counted (see below). "Convergence" appears only with the qualifier or in unrelated senses (a reflect convergence score; stoprule's convergence result).

## Summary
- Changes applied: 20 of 20 (Applied 20, Skipped 0, Failed 0).
- Output: `proposal-merged.md`, 823 lines, 23,489 words (final count after all fixes below), 51 provenance comments plus the three header comments.
- Plan-versus-source conflicts: 4 (listed at the top; none blocked a change).
- Content added beyond the plan: none. One draft addition (Owner decisions 17-22) was removed during validation because it was not in the plan's list.

## Post-Merge Validation

### 1. Structural integrity
- Heading hierarchy: checked with a fence-aware scan of every heading. Levels are H1 (title), H2, H3 and H4 under "Candidates, promotion and singletons"; no level gap (PASS).
- H2 order: Decision summary; then the seven template sections in template order (Design, How it works, Evidence, Correctness argument, Risks and mitigations, Test coverage needed, Cost); then the four new H2 sections after Cost (Unresolved conflicts, Unaddressed invariants, Owner decisions, Debate record and provenance) (PASS).
- Provenance: the first scan found 25 headings with no `<!-- Source: -->` comment (the Terms block, the H4s under Candidates, the How it works subsections, Evidence tables A-E and corrections, Correctness subsections, test subsections, the Unresolved and Debate record subsections). Comments were added; the re-scan lists none. Initial result FAIL, after fix PASS.
- Tables: every table row has the same number of columns as its header (fence-aware awk, escaped pipes handled) (PASS).
- The Rollout placeholder comment was replaced when Change 15 was applied; grep finds 0 (PASS).

### 2. Internal references
Scan of ID, change, INV, EC, debate-point, row and "see" references, counted on the final text (counts include the defining rows and tables):

| Reference family | Occurrences | Resolved | Broken |
|---|---|---|---|
| `INV-nnn` (25 defined rows) | 185 | 185 | 0 |
| `EC1`-`EC6` | 25 | 25 | 0 |
| debate points S/C/X/A-nnn (33 defined rows) | 173 | 173 | 0 |
| synthesis conflicts Cnn (14 glossary rows) | 55 | 55 | 0 |
| evidence-row tokens V/G/K/F/X + number (V1-V11, G1-G8, K1-K6, F1-F5, X1-X11) | 149 | 149 | 0 |
| tokens of the form Rnn (risk rows R1-R22 and research-file tags R02, R05, R07, R11, R12) | 86 | 86 | 0 |
| test references ("test 24", "tests 17-23", ...; 27 numbered tests exist) | 9 | 9 | 0 |
| quoted section cross-references ("see ...") | 42 | 42 | 0 |
| plan change numbers in comments and the invariant table (1 to 20) | 20 distinct | 20 | 0 |
| **Total** | **744** | **744** | **0** |

Two reference ambiguities were found and fixed: in R20 and R21 the labels "G2" and "G5" could be read as the Evidence rows G2 and G5 instead of the Round 2 facts of the transcript; they now read "Round 2 B fact G2" and "Round 2 B fact G5". The research-file tags R02 to R12 and the risk rows R1 to R22 share a letter; the Evidence key now says they are different.

### 3. Contradiction re-scan (grep of the merged text)

| Pattern | Hits | Resolution |
|---|---|---|
| "decides today" | 0 | none needed; the text says "what runs today is the existing, unhardened veto" (see plan conflict 4) |
| "is live today" | 0 | none needed |
| "can only remove" / "no decider can add" / "none can add" | 0 | none needed; Variant A's subset claim is described as "dropped (X-001)" and never restated |
| "subset" | 1 (the table column "audit-clean subset") | not the rejected claim |
| "fail-closed by construction" | 2 | both are quotations of the replaced base claim ("the base's claim, is replaced by fail-closed on procedure only"; "P4 ('fail-closed by construction')" in the list of rewritten claims) |
| "measured that direction" | 1 | quotation of the replaced P1 claim in EC2 |
| "measured more wrong blockers as reviewers were added" | 1 at first | a sentence in "Cost of keeping the veto alone" contradicted the agreed X-004 outcome; rewritten to match EC2 (FAIL, fixed, PASS) |
| "only option that leaves every pin" | 0 | the claim appears only as the topic label of X-007 in the debate table ("Is A the only option that leaves pins and contract alone", outcome: B's side) |
| "converged" | 0 | none |
| "convergence" | 11 | banner, Decision summary, invariant section and Debate record carry the qualifier ("blocked by invariants", "NOT achieved"); the other hits mean the reflect convergence score (`contract.py:317-326`) or stoprule's "repeated convergence result" |
| "decision ==" | 1 | the real assertion of `test_review_cli.py:348` (`decision == "PASS"`); `decision` there is the ledger routing word, which is correct |
| "class" meaning model class | 0 left unqualified | remaining hits are `deviation_class`, `model_class`, the CLI option `--hard-exclude-class`, a quoted base row, or probe rows kept verbatim (a note under the invariant table says the probe's "decision" means `grade` and its "class" means `deviation_class`) |
| "names proposed" | 0 | replaced |
| "design parameters to fix at build time" | 2 | quotations of the replaced phrase (Owner decisions) |
| "owner-set tolerance" | 1 | quotation of the replaced phrase (Owner decisions) |
| "Resolved:" label on INV-003 | 1 at first | reworded to "Addressed in the debate: INV-003 (ADDRESSED, LOW)" so that no invariant reads as resolved by this document |

### 4. Open-item count check
- Agreed-open conflicts: 3 in "Unresolved conflicts" (C-005, C-012, X-002) and 3 OPEN rows in the debate table (PASS).
- QUALIFY assumptions: 3 in "Unresolved conflicts" (A-001 60%, A-003 58%, A-007 60%) and 3 QUALIFY rows in the debate table (PASS).
- Invariant rows: 25 (11 HIGH UNADDRESSED, 10 MEDIUM UNADDRESSED, 2 LOW UNADDRESSED, 2 ADDRESSED), in that order (PASS).
- Debate points: 33 rows (8 S, 15 C, 7 X, 3 A) (PASS).

### 5. Rule check
| Rule | Result | Basis |
|---|---|---|
| R-1 no "hardened veto decides or is live today" | PASS | Position, Decision summary and banner say what runs today is the unhardened veto; the hardened veto is a target with four unbuilt prerequisites |
| R-2 unaddressed invariants all listed, none softened or resolved | PASS | 25 rows in the required order with the probe's severity and status; the section says the debate did not resolve them; INV IDs are printed next to the items in the body (Decision summary, Certification, Evidence gate, Grader and rubric, Adapters, Contract fields, Reflect-post, Correctness, Rollout, Risks, Tests, Owner decisions) |
| R-3 no implied grader accuracy, replay sufficiency, understood false-block rate, or shadow counts proving a winner | PASS | "Not claimed" paragraph in Position; "Not decided here" in the Decision summary; Rollout "What the gate does not settle"; INV-023 attached wherever the shadow record is mentioned |
| R-4 "converged" only with the blocking qualifier | PASS | banner and Debate record state 90.9% (30 of 33), status partial, 11 HIGH unaddressed, 3 agreed-open; no use of "converged" |
| R-5 tags on advocate-computed numbers and unread facts | PASS | control-by-size tables, the 50-100 line adapter estimate, 380,000 reviewer output tokens, the 300-400/150/40-60 line estimates and "about three lines" for D2 carry `[advocate-computed, not re-aggregated]` or `[estimate]`; the 13 null-span rows carry `[VIA audit-D]` (one occurrence inside the verbatim INV-025 row was added after the first scan found it untagged) |
| R-6 terminology fixes | PASS | `grade`/`decision`, `model_class`/`deviation_class`, glossary for E2, D1-D6, UC-1/UC-2, B1-B3, veto, candidate, shadow, 14 synthesis conflicts and a row for the debate-point IDs; open phrases replaced by values or Owner decisions 1, 15, 16 |
| R-7 subset property not stated in either direction | PASS | only "dropped (X-001)" appears |
| R-8 no invented line numbers or counts | PASS | every file:line is one the plan, transcript, probe or a variant gives; the one new count (744 references) is a validation figure, not a code claim |
| R-9 unresolved-conflicts section | PASS | C-005, C-012, X-002 with agreed-open position, "the measurement the debate named; it may not decide" and limits; A-001, A-003, A-007 with conditions and confidences |
| R-10 debate record | PASS | 33-row table (ID, level, topic, agreed outcome) plus artifact pointers |

### 6. Fixes made during validation (each re-checked after the fix)
1. 25 headings without provenance comments: comments added (re-scan clean).
2. Owner decisions table: six entries (17-22) that were not in the plan's list were removed; the section now says which probe items have no owner-decision entry (INV-004, INV-007, INV-009, INV-020). Re-read: 16 entries.
3. "Cost of keeping the veto alone" sentence corrected to match EC2.
4. INV-003 label reworded; INV-025 evidence cell tagged `[VIA audit-D]`.
5. Ambiguous G2/G5 labels in R20/R21 disambiguated; research-file tag versus risk-row note added to the Evidence key.
6. Terminology pass: "read by no decision" became "read by no verdict rule"; "class diversity" became "`model_class` diversity"; "two-word class labels" became "two-word deviation-class labels"; a note on the file name `panel/decisions.json`; a note on the probe's wording.
7. The banner and Terms block gained one-line glosses for C-005, C-012, X-002 and the debate points used in the Decision summary.

### 7. Not done and why
- The merge executor did not re-read any code, test or E2 file; all `[READ]`-style tags are inherited from the variant authors, as the Evidence key says.
- The return contract (`adversarial/return-contract.yaml`) was not edited, per the instructions.
