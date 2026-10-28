# Synthesis: Options and Recommendation

**Date:** 2026-10-24
**Status and delivery:** Producer handoff status, intended component path and persistence note are kept in the non-assembled Provenance and Delivery Record at the end of this file. The ranking below inherits the adversarial return status `partial`, because the causal order is not a consensus.
**Governing format:** `/config/.claude/skills/tech-research/SKILL.md`, Synthesis Agent Prompt (lines 779-811) and Report Structure sections 6-7 (lines 1393-1431). Two adaptations are made. First, each "option" here is one of five candidate causal explanations, not an implementation choice. Second, the template's Effort, Risk, Reuse, Files, Pros and Cons fields describe only the proposed, unexecuted investigation of each candidate. They are never a measure of how likely a cause is.
**Research question context:** Why was an apparent repair or pass followed by another failed review, or by a required new review, in six selected historical workflow and implementation sessions?

**Path key:** Package-relative paths resolve beneath `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`. `ADV/` means `reviews/adversarial/adversarial/`. Physical JSONL record numbers refer to the original session logs listed in `research/evidence-deck.md:121-128`. They are not line numbers in research files, and they were not replayed for this component.

**Superseded by report (added 2026-10-24 by the Phase 6 /task phase-gate fixer (fix cycle 1 of 3), applied by the parent, consolidated finding G6-08):** the final report's Sections 6-7 govern, and its Section 10.11 holds the producer read record. This component still differs from the report in these places, and the report's text applies: (1) the "7.8 Sources read and limits" reading log below was moved to report Section 10.11; (2) Option D Effort here is "S", while the report re-rates it M; (3) the Options Comparison Effort row here reads "M | M | M | S | S", while the report reads "M | M | M | M | S"; (4) Section 7.2 here says the five orders are repeated at `return-contract.md:24`, while the report says that line repeats only the displayed order; (5) Section 7.6 order 1 here says "V1 loses its lead", while the report says the check alone cannot reorder the ranking; (6) order 3 here says "two incidents each", while the report names one Option D incident and two controls; (7) order 4 here says a broader count "could settle the middle and bottom pairs", while the report says applying it needs a new comparative judgment; (8) the trade-offs paragraph here says steps 1-3 "stay read-only", while the report says steps 1-2 need separately approved execution in a disposable copy; (9) this component omits the shared 2026-10-22T20:29:54Z install that the report uses to qualify V3's reach (report Option C Scope, Sections 7.1 and 7.4, Question 21). Later report corrections to Sections 6-7, including the Phase 6 /task phase-gate additions to Section 7.6, exist only in the report unless the report's Section 10.10 says otherwise.

---

## 6. Options Analysis

### 6.0 What the debate measured, and the comparison rule

The five options are the five debated hypothesis cards. Their immutable debated sources are `ADV/variant-1-original.md` through `ADV/variant-5-original.md`. The formatted presentations are `synthesis/hypothesis-01.md` through `hypothesis-05.md`. Their parent persistence records say every original body line was preserved verbatim.

Options A-E below follow card order (V1-V5), not rank order. The ranking is in Section 7.

| Debate quantity | What it measures | What it does not establish |
|---|---|---|
| Ten-point writing convergence (all ten defined points resolved; contract field `convergence_score: 1.0`) | Agreement on how to classify, cite and report transitions | Agreement on causal order (`reviews/adversarial/return-contract.md:24`; `ADV/debate-transcript.md:468-475`) |
| `unresolved_conflicts: 0` | Count of the ten defined diff points left unresolved | Absence of causal dispute; two causal pairs remain disputed (`return-contract.md:16,24`) |
| Selected writing base: Variant 4 | Which document the merge was built on. The top two combined writing scores fell inside the protocol's tiebreak threshold, so input order decided it | That Variant 4 is the most likely cause (`ADV/base-selection.md:5,150-155`; `merged-root-cause-analysis.md:21`) |
| Five advocates' final Round 2 orders | Evidence-weighted judgments of explanatory support under rule A-001 | Five independent empirical observations, a majority vote on the full order, or any probability (`ADV/invariant-probe.md:39-44`) |
| Round 2.5 invariant probe: PASS, six HIGH assumptions addressed | No unaddressed blocker in the ten-point writing synthesis | Causal-order consensus (`ADV/invariant-probe.md:18-20,72`) |
| Process-confidence label on the scoring matrix | The manager's confidence in each writing choice | Causal probability (`ADV/debate-transcript.md:453`) |
| Post-merge validation: PASS, 13 of 13 checks | Fidelity of the recovered merged artifact to its plan and cards | Replay of historical incidents or causal consensus (count: `qa/adversarial-post-merge-validation.md:41`; scope limit: `:120`) |

**Comparison rule (A-001).**
- The question being compared is why an apparent repair or pass was followed by another failed review or review entry, in this selected and clustered sample.
- Explanatory reach across relevant contexts counts first. Direct evidence for a particular transition counts second.
- Repeated messages, numbered findings and related packages are not independent votes.
- Strong evidence about a specific event overrides the aggregate order for that event.
- The Round 1 responses to this rule were ACCEPT, QUALIFY, ACCEPT, ACCEPT, QUALIFY (`ADV/debate-transcript.md:243`). In Round 2 all five advocates adopted it: V1 ACCEPT, V2-V5 QUALIFY (`:277,316,356,397,438`).

**Sample boundary.**
- Six sessions were selected from a frozen membership of 30 by file modification time. They cluster in a few work families.
- They contain three strict incidents where an operational repair was followed by another unsuccessful review, one unchanged rendering-proof blocker, and two planning loops ending `partial` or not-ready (`research/evidence-deck.md:49-58`; `gaps-and-questions.md:11`).
- Orca planning and Orca monitor share one plan. The two credential packages share one work family. Neither pair is independent (`ADV/diff-analysis.md:33`).

### Option A: Checks prove less than the requirement (Variant 1)

**Description:** A genuine pass establishes format, labels, counts or the presence of a validation step, but not the required behavior. A later reviewer then exercises a different failure path that already existed.

**How it works:**
1. A behavioral requirement is represented by a narrower check.
2. Implementation and early review accept that narrower evidence without establishing ordering, semantics, cross-component use or exceptional paths.
3. The fix closes the demonstrated example only.
4. A later review finds an old counterexample. That is not damage caused by the preceding fix (`synthesis/hypothesis-01.md`, section 2).

| Aspect | Assessment |
|--------|-----------|
| Mechanism | The required behavior is replaced by a weaker predicate (parsing, keyword, count, marker or the presence of a validation step). Later discovery of an old counterexample follows a real but insufficient pass. |
| Support | **Oracle:** family labels, counts and one-field contrasts pass while the known/unknown-author and default-path security meanings are wrong. 67 default and 78 acceptance tests pass despite four valid defects (oracle log 291 is a truncated relay of the review; the full findings 1-4 are at `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/t12-review-1.md:20-35`; `research/02-session-a9b88895.md`, sections 4-5). **Monitor:** a 640-line workflow (record 585) has structural acceptance checks, and lasting behavior tests are deferred to Task 14. Most later findings were already present in it (records 585, 804, 906, 1021; `research/05-session-e002bed2.md`, sections 2 and 4). **Orca planning:** the first coverage matrix credits an up-to-date state that no original task names (first `coverage-matrix.yaml:1749-1757`), and validation runs after the fetch that consumes its input (second `merged-verdict.yaml:39-47`; `research/01-session-ac2cd1fd.md`, section 4). **CI planning:** the creation command's arguments are asserted, but the search stub ignores search filters, and a phrase blacklist still accepts a contradictory half-edited advisory header (`research/04-session-43582de1.md`, section 6.2 and supplement section 5). Cross-case miss mechanisms: `research/evidence-deck.md:585-597`. |
| Opposition | Oracle's three permitted repairs worked. Its repeated fourth finding concerns frozen correction authority, not another weak-check escape. Monitor Tasks 10 and 11 each converged after one repair. The Orca and CI introductions and the monitor error-trap regression need the connected-effects account. The credential proof-only rejection happened while delivery already met the lint criterion (`synthesis/hypothesis-01.md`, section 6; `research/evidence-deck.md:647-648`; credential clause: `research/evidence-deck.md:389,595`). Screened controls Session 10 Task 4 (missing comment corrected, compliant re-review) and Session 17 Task 8 (real deviation corrected, passing re-review) also converged after one repair; limits: Session 10's original implementation package was absent from searched locations, and Session 17's later PR reviews are separate work (`research/evidence-deck.md:650-651`). |
| Alternative explanations | Repair-created interactions (V2), changing review judgments (V3), defective proof pointers (V4), and a frozen fixture or unavailable renderer (V5). These are competing immediate causes that can coexist with weak verification. Task size and deferred lasting tests are observed amplifiers, not isolated causes. |
| Scope | Explains old defects surviving apparently successful verification. It does not explain proven new regressions, frozen repair authority, proof-only rejection, policy-mandated reopening or false baseline attribution (`ADV/debate-transcript.md:49,256-257`). |
| Falsification | **Proposed, unexecuted.** On the preserved version that first passed, build a minimal counterexample for each later finding and separately verify whether the relevant behavior test was deferred or absent (`synthesis/hypothesis-01.md:142`), keeping the original criteria and policy fixed. Support grows if the check actually used accepts wrong behavior that a criterion-derived behavioral check rejects. It weakens if the checks actually used already reject it (`synthesis/hypothesis-01.md`, section 8; `merged-root-cause-analysis.md:64`). |
| Evidence strength | Strong case-specific support across the oracle, monitor and both planning contexts. The size and deferred-test contribution is observational, not a controlled experiment. Why particular reviewers missed particular counterexamples is unknown. |
| Debate record | First in all five final orders (`ADV/debate-transcript.md:477-484`). All five advocates nominated it for the breadth writing point (C-004). Opponents' critiques: "weak checks alone cannot explain restoring a softened criterion or mandatory reopening" (V3 advocate, `:128`); broad escape coverage "is not sufficient explanation of the next failure" (V4 advocate, `:167`); it explains initial fixture escape but not why three permitted fixes could not close the frozen fourth finding (V5 advocate, `:208`). The V1 advocate accepted these limits (`:256-257`). |
| Current rule vs historical observation | **Historical, observed:** Orca plans passed structural checks and still received substantive semantic findings (planning log 499, 843/849; `research/01-session-ac2cd1fd.md`, section 2). Version 4 passed the structural gate at 943/944 but was never semantically reviewed (946: "NOT CHECKED: v4 has had no review since this edit"; `research/01-session-ac2cd1fd.md:85-86`). **Current rule, source-read only (checkout master `2165ae25`, read-only `git show`):** `git show 2165ae25:src/superclaude/skills/sc-workflow-protocol/refs/quality-gates.md`:24-39 (installed copy byte-identical, read 2026-10-24T04:36Z) describes schema and coverage checks performed by an agent, not an executable semantic proof (`research/scope-rules.md:32`); coverage of source requirements is checked only at standard/deep depth (`quality-gates.md`:31-39; installed `sc-workflow-protocol/SKILL.md`:54, read 2026-10-24). That is a current design boundary. It does not show which bytes historical runs loaded, and installed/checkout drift was later observed (`gaps-and-questions.md:56`). |
| Effort (proposed investigation only) | M. Reasoned estimate, not measured: four contexts, one counterexample per later finding on preserved first-passing versions. |
| Risk (proposed investigation only) | Medium. The replay must use preserved historical versions, not mutable current files. It must not relax valid criteria, and it must not be presented as a new authorized review. |
| Reuse of existing code/evidence | Oracle review artifacts and the preserved pre-authorization fixture; the monitor's original workflow embedded at record 585; Orca v1-v4 reconstructable from logged Writes/Edits; the first two reconstructed hashes match their review snapshots and the final (v4) reconstruction matches the live plan, while v3 has no independent comparison target (`research/01-session-ac2cd1fd.md:323`); CI original and regenerated plans. |
| Files/systems affected | Read-only inputs only: the six case reports; the oracle package `/config/workspace/IronClaude/.dev/worktrees/auggie-claim-gate/.dev/tasks/to-do/TASK-WF-designV2-20261020-132032/artifacts/` (historical recorded path); the Orca planning and monitor JSONL logs; the CI plan packages named in case 04. No production system. |
| Pros | Tests the only unanimous exact rank position; the widest reach; preserved inputs exist for all four contexts. |
| Cons | Cannot explain reviewer cognition. Leaves the task-size effect unisolated. Extracting the monitor's first-passing state requires transcript reconstruction. |

### Option B: Local repairs miss connected effects (Variant 2)

**Description:** A repair is checked against the reported symptom without tracing connected execution order, dependencies, data sources or unchanged constraints. It can introduce a new defect or leave a sibling failure in place.

**How it works:**
1. A local remedy (a test, an earlier validation, an error trap, a simpler dependency edge) crosses a boundary.
2. It is accepted without proving that neighbors and invariants still hold.
3. The next review exposes the interaction, or another untouched path (`synthesis/hypothesis-02.md`, section 2).

| Aspect | Assessment |
|--------|-----------|
| Mechanism | A successful amendment crosses an unchecked ordering, dependency, data-source or output-stream boundary. A demonstrably introduced defect must be kept separate from an untouched sibling failure. |
| Support | **Orca inventory test:** the revised plan requires the inventory comparison in Task 13, before Task 14 registers the workflow, so intermediate acceptance cannot be satisfied (successful writes 544-545 and 841; second `merged-verdict.yaml:120-128`). **Four-asset predicate** moved into early detection (`merged-verdict.yaml:75-83`). **Digest source** switched to deployed-package provenance (`:57-65`); case-report and deck qualification, not weighed in the debate: the substitution changed the declared field-9 contract, the requirement itself defines field 9 from recipe state even though rollback can separate recipe and deployed-package state, and provenance might be a defensible source if explicitly approved, but no such approval was declared (`research/01-session-ac2cd1fd.md:208,299`; `research/evidence-deck.md:431`). **Further introductions in the case report, not in the card's table:** renderer test boundary, wrongly named fetch remote, and the v3 unsafe bad-value wording and ill-defined mutation (`research/01-session-ac2cd1fd.md`, sections 3.4-3.5 and 5). A further case-report finding the debate never weighed: v2 added “same result as base” comparisons with no baseline-capture task, an introduced acceptance-executability gap, although a known local-failure comparison already existed in the v2 constraints and no execution is claimed (N-17; `research/01-session-ac2cd1fd.md:222`; `research/evidence-deck.md:446`). **Monitor:** a successful repair enables inherited error traps writing to standard output, and captured values are later contaminated (records 759-762 introduction, 1240 reproduction). **CI:** repointed dependencies lose required ancestors (`research/04-session-43582de1.md`, section 7). |
| Opposition | Fourteen original planning amendments were accepted and two were partial. Twenty later numbered items are not twenty regressions. Most later monitor defects already existed, and the size repair exposed later limits rather than creating them (`research/evidence-deck.md:626,657`). Oracle repairs worked, and credential FINAL repairs changed evidence only. Two of CI's four "new medium" findings were later downgraded (`research/04-session-43582de1.md`, section 1). Screened controls Session 10 Task 4 and Session 17 Task 8 converged after one repair (missing comment; real deviation); limits: Session 10's original implementation package was absent from searched locations, and Session 17's later PR reviews are separate work. Sessions 13/14 made authorized plan corrections without semantic re-review, so not every corrected plan receives a second failed review, although an unreviewed correction is not clean approval either (`research/evidence-deck.md:650-651,655`). |
| Alternative explanations | An incomplete fix of an existing failure family is a different outcome from introduction: within this candidate it is the separately labelled retained-sibling outcome (S-002), never counted as an introduction (C-003). Examples: the CI tooling exemption added to the status check but not the hash check, and the monitor pin trap lacking the detect job's sibling guard. Weak checks (V1) can let the connected problem escape first. Changed criteria (V3) can create apparent conflict without damaged behavior. |
| Scope | Two outcomes kept separate (S-002): an introduction, meaning a failure absent immediately before and present after a confirmed successful amendment under the original contract (C-003); and a retained sibling, an untouched path in the same failure family that a local repair leaves failing, which is never counted as an introduction (`ADV/variant-2-original.md:10,37`; `ADV/debate-transcript.md:269,272`). Plan nonconformance is not observed runtime disorder. The monitor trap was later accepted with known defects, not shown repaired. |
| Falsification | **Proposed, unexecuted.** Replay only confirmed successful edits against their immediately preceding preserved state, keeping criteria and policy fixed. Trace the affected producer, consumer, sibling path or dependency. Require an absent-before/present-after counterexample. If the failure already existed, reclassify it as retained or previously missed (`synthesis/hypothesis-02.md`, section 8). |
| Evidence strength | Strong direct introduction evidence for selected plan interactions and one shell data-flow regression. The CI graph defect is plan nonconformance only, because the sequential executor prevents reordering. It does not explain most later monitor findings. |
| Debate record | Final positions 2, 2, 3, 3, 3 across the five advocates. **For second place:** the V1 and V2 advocates cite reach across planning, implementation data flow and CI graph conformance, with demonstrated change mechanisms (`ADV/debate-transcript.md:264,302`). **Against:** the V3, V4 and V5 advocates say introduction evidence is narrower than finding volume, and V2 cannot claim credit for preexisting monitor faults (`:129,168,343,379,425`). The V2 advocate conceded that most monitor faults preexist and that the CI case shows graph nonconformance only (`:294-295`). Unanimous writing nomination for attribution standard C-003. |
| Current rule vs historical observation | **Historical, observed:** plan-text introductions and one implementation regression. **Current rule, source-read only (installed layer `/config/.claude/skills/sc-implement-protocol/`, read 2026-10-24; the rule map records the same input boundary, `research/scope-rules.md:41`):** a per-task verdict rests on the task brief and the diff (`refs/qa.md`:9,77); the diff is scoped to that task's touched files (`SKILL.md`:118-121, Q1 and Q2); and citations into files outside the touched set are invalid unless the AC required reading them (`refs/qa.md`:31). Per-task review therefore does not trace neighbor impact beyond what the task's AC require. The only end-state contradiction check is the managed FINAL, which returns `issues` when "a later change contradicts" an AC (`refs/qa.md`:82). This is a current design boundary; it does not show which bytes historical runs loaded. |
| Effort (proposed investigation only) | M. Reasoned estimate: replay confirmed edits in three contexts against reconstructed predecessors. |
| Risk (proposed investigation only) | Low-Medium. Plan-level defects must not be reported as runtime failures. Blocked edit attempts must not be counted as applied (records 150/151, 1164-1170). |
| Reuse of existing code/evidence | Logged successful Writes/Edits with reconstructed plan hashes; monitor records 585, 759-762 and 1240; CI original and regenerated plans. |
| Files/systems affected | Read-only: `research/01-session-ac2cd1fd.md`, `research/04-session-43582de1.md`, `research/05-session-e002bed2.md` and their recorded historical plan and log paths. |
| Pros | Its attribution standard was adopted unanimously, and its evidence is the clearest proof of introduction. |
| Cons | Reach is concentrated in one planning cluster plus one shell regression. Cannot resolve the reach-weighting dispute with V3. |

### Option C: Review contracts change during the loop (Variant 3)

**Description:** Review does not keep one operative contract across stages or attempts. Criteria are softened, hardening is treated as required compliance, source conflicts go unresolved, or installed policy changes mid-run. This can cause reversals and extra reviews even when delivery files are unchanged.

**How it works:**
1. The written requirement, the early interpretation and the later loaded rule differ.
2. A fresh reviewer applies another interpretation or a newly loaded policy.
3. The verdict may reflect a real original violation, added scope, migration or a mixture (`synthesis/hypothesis-03.md`, section 2).

| Aspect | Assessment |
|--------|-----------|
| Mechanism | Four separately attributable subtypes: an unresolved source conflict, an interpretation change, added hardening, and policy migration. Each can change a verdict or require another review without creating a delivery defect. |
| Support | **Credential lint relaxation:** Task 6 QA accepts "no new findings" despite the literal no-finding-on-changed-line clause. FINAL reapplies the clause (parent records 1215, 1230, 1935, 1938; nested `agent-a6d8fbaf69a56dd14.jsonl:61`). **Two different rubric texts** were loaded from the same installed path by consecutive FINAL reviewers (`agent-acf0a51e6992c50ee.jsonl:18` and `agent-a4bfff371c63a6c39.jsonl:18`; captured hashes at `research/scope-rules.md:70-71`). The earlier text treats missing, stale or unverifiable evidence as `issues` and forbids an executor-written Ruling; the later text still treats evidence that cannot be found in the current files or logs as `issues`, but takes evidence from current files and artifact logs, says a stale pointer that is only a moved line number is never `issues`, adds stricter `issues` triggers (Section 2.3), and lets the executor record a confirmed, scoped user acceptance (Section 2.3; the debated card states this contrast as stale evidence versus moved line alone and changed acceptance handling, `synthesis/hypothesis-03.md:57`). **Monitor migration** required a fresh review after a compliant verdict (records 42, 58, 849, 874, 893, 902). **Broader monitor hardening** includes uncapped fields absent from the plan (records 906, 1143), and case-insensitive security-keyword matching that the written pattern did not clearly require (`research/05-session-e002bed2.md:156`). The per-review prompts made any defect of any severity noncompliant (`synthesis/hypothesis-03.md:59`; `research/05-session-e002bed2.md:240`). Case-report detail the debate never weighed: the review prompts also told reviewers to judge every Task 12 requirement bullet directly, and the findings mixed requirement violations with exactness problems in commands the requirements suggested (the `git diff --name-only` rename overlap), cosmetic output (punctuation and grammar) and an unused `vhex()` helper that the case classes as a preexisting extra (`research/05-session-e002bed2.md:58,132,135,145-146,242-248`). **Orca source contradictions** (source `:142,285,382,402`) and the **CI boundary-file dispute**, later conceded as optional hardening. |
| Opposition | The oracle review repeats an unchanged default-path requirement. The manual-page reviewer twice asks for the same real render proof. The fresh monitor review finds genuine defects that predate the policy change. Both full Orca reviews used the same driving-source hash, so changed source bytes do not explain their different findings (`research/01-session-ac2cd1fd.md`, section 7). |
| Alternative explanations | Weak checks (V1) and introduced defects (V2) explain the actual artifact state. The final credential pass followed both proof correction (V4) and the rubric change, so neither effect is isolated. |
| Scope | Explains review re-entry, reversals and disagreement, and why final convergence is hard to attribute. It does not explain creation of the underlying defects. The card calls it "a proven amplifier in two runs". |
| Falsification | **Proposed, unexecuted.** Keep the artifact state fixed. Have independent reviewers adjudicate each disputed finding twice: under the preserved original contract and under the actually loaded rules. Classify each difference as original violation, authorized acceptance, added hardening, unresolved contradiction or rule-version effect. The same substantive failure under identical conditions weakens this account (`synthesis/hypothesis-03.md`, section 8). |
| Evidence strength | Direct captured tool results prove two rubric versions. Monitor records prove the migration reopened a compliant check. The lint relaxation and its restoration are explicit. Unknown: who changed the rubric, and whether the policy change alone would have passed the unrepaired package. |
| Debate record | Final positions 3, 3, 2, 2, 2. **For second place:** the target includes review entry and reversal, which this candidate addresses directly, and planning contract conflicts extend its reach (V3 advocate `ADV/debate-transcript.md:343`; V4 `:380`; V5 `:421,425`). **Against:** its decisive migration and rubric evidence is concentrated in two runs (V1 advocate `:264`); including re-entry "materially strengthens V3", but the V2 advocate still did not promote it (`:303`). The V3 advocate conceded migration, credential confounding and the stable-criterion counterexamples (`:333-335`). Unanimous writing nomination for controls point C-002. |
| Current rule vs historical observation | **Historical, observed:** a criterion was softened without owner acceptance (an execution/authority problem, `research/evidence-deck.md:727`); FINAL policy changed between consecutive reviewers (`:730`); a mid-run migration happened. **Current rule, source-read only:** checkout master `git show 2165ae25:src/superclaude/skills/sc-implement-protocol/refs/qa.md`:82 (installed copy byte-identical, read 2026-10-24T04:36Z) says a moved line alone is not an issue (`research/scope-rules.md:43`). The bounded ladder coexists with fresh reviews on operator resume, which is a design boundary (`research/evidence-deck.md:726`). There is no stable finding-resolution registry binding later reviewers, which is a rule-map limitation (`:731`; `research/scope-rules.md:56`). Per-task reviewers are also isolated from earlier reviews: they may not read the retry folders, a citation into them makes the verdict `cannot-verify`, and they never see an adviser answer or a brief; only the managed FINAL reads them (installed `sc-implement-protocol/refs/qa.md`:82,90 and `refs/retry.md`:16, read 2026-10-24). Current text cannot establish which bytes were historically loaded. |
| Effort (proposed investigation only) | M. Reasoned estimate: requires dispatching independent paired adjudications, which needs approval. |
| Risk (proposed investigation only) | Medium. A paired adjudication must not be mistaken for an authorized re-review, must not waive valid findings, and must not treat an accepted gap as compliant. |
| Reuse of existing code/evidence | `research/historical-review-rules.json` (exact before/after loaded texts); nested reviewer transcripts; monitor rule reads 42, 58, 874 and 884. |
| Files/systems affected | Read-only: `research/06-session-0690ee9f.md`, `research/05-session-e002bed2.md`, `research/historical-review-rules.json`, `research/scope-rules.md`, plus the CI and Orca case reports for the source-conflict subtype. |
| Pros | Directly tests the review-entry part of the target. Captured rule bytes already exist. |
| Cons | The credential policy and proof effects stay confounded unless the paired run holds proof fixed. Reviewer-dependent outcomes add variance. |

### Option D: Brittle evidence and provenance handoffs (Variant 4)

**Description:** When verified work is converted into durable proof, it sometimes loses meaning or provenance. A later reviewer then rejects missing, wrong or misleading evidence even though delivery did not regress.

**How it works:** Three distinct forms (`synthesis/hypothesis-04.md`, section 2):
- temporary proof is replaced by an unrelated citation, or a blank or incomplete range survives;
- a baseline reconstructed from post-edit HEAD makes preexisting dirty work look task-created;
- a missing checkpoint is classified as head-moved [correction, Phase 6 /task phase-gate fix: what was missing was the Q0 HEAD file `<retries>/T<id>/q0-head`, not a checkpoint; the task-start snapshot existed (Section 2.5)].

| Aspect | Assessment |
|--------|-----------|
| Mechanism | The link between claim, meaningful proof and historical state breaks. Proof loss or defective pointers, false baseline attribution and a checkpoint-guard halt must stay distinct. A head-moved label does not prove HEAD actually moved [correction, Phase 6 /task phase-gate fix: the guard's missing input was the Q0 HEAD file `<retries>/T<id>/q0-head`; the task-start snapshot existed (Section 2.5)]. |
| Support | **Initial credential package:** genuine temporary lint proof became a README separator citation. Durable proof and a corrected pointer produced a pass with no delivery changes (parent records 332, 390, 411, 435; nested `agent-abd76ef5e5d22848f.jsonl:36`). **Follow-up package:** Task 10's blank-line-10 pointer existed before the first FINAL and was found by the second FINAL. The first proof repair also missed one row (records 1425, 1932, 1968, 2012, 2015, 2036; nested `agent-af349dd52cae648a5.jsonl:16`). **Documentation Task 2:** substituting post-edit HEAD falsely attributed earlier hunks to the task. The earlier truthful tree `f60d2c3…` contains them (records 188, 204, 217, 234; `research/03-session-6f744b87.md`, section 5). |
| Opposition | The initial evidence rejection was valid under the rule loaded at the time. The follow-up also contained a genuine literal lint failure. The third FINAL pass followed both pointer corrections and a changed rubric. The checkpoint halt [correction, Phase 6 /task phase-gate fix: a halt on a missing Q0 HEAD file, Section 2.5] is neither HEAD movement nor the cause of the rendering failure. Screened Session 17 FINAL found a real restore-basename bug plus evidence defects, which were corrected before it passed, so FINAL issues are not only proof defects; limit: that session is not strict fail-fix-fail (`research/evidence-deck.md:652`). |
| Alternative explanations | A strict evidence contract may deliberately demand durable proof for correct delivery. Different review focus explains late detection of the blank pointer, but why the first FINAL missed it is unknown. The changed policy (V3) partly explains the last verdict. |
| Scope | Isolated proof-only rejection and false attribution. Direct support is concentrated in two selected sessions and three package/task contexts. The related credential packages are not independent breadth. |
| Falsification | **Proposed, unexecuted.** Reconstruct the true pre-task state, keep the original proof, and check every cited range for semantic support under a fixed rubric. The account weakens if failures continue despite complete valid proof and a correct baseline, or if a supposedly proof-only interval contained a necessary delivery correction (`synthesis/hypothesis-04.md`, section 8). |
| Evidence strength | Strong within the named historical evidence failures: actual ledger writes, nested tool output, unchanged delivery digests and recovered Git trees. Breadth is limited, and the digests do not cover evidence artifacts or policy. On the policy side, the second and third FINAL judged evidence under different loaded rules: the earlier rubric made missing, stale or unverifiable evidence `issues`; the later one still makes evidence that cannot be found in the current files or logs `issues`, but says a stale pointer that is only a moved line number is never `issues`, and it adds stricter `issues` triggers (Section 2.3; Option C Evidence strength). |
| Debate record | Final positions 4, 4, 4, 5, 5. **For fourth (above V5):** the V1, V2 and V3 advocates cite proof-handoff reach across the credential packages plus documentation provenance, while acknowledging the packages are clustered (`ADV/debate-transcript.md:265,304,344`). **For fifth:** the V4 advocate reversed their own Round 1 order. Their stated reason: the two candidates' reach is "comparably narrow", both V5 incidents directly explain the continuation, and some V4 evidence explains attribution or a halt rather than the repeat itself (`:384-385`). The V5 advocate agreed (`:426`). Unanimous writing nomination for historical-evidence point C-007. Selected as the writing base by tiebreak only (`ADV/base-selection.md:150-155`). |
| Current rule vs historical observation | **Historical, observed:** proof lost at ledger handoff; blank pointer missed; the second failed FINAL is missing from the ledger (a bookkeeping omission, `research/evidence-deck.md:565`); the guard outcome for the missing Q0 HEAD file (`:729`; Section 2.5). **Current rule, source-read only:** checkout master `git show 2165ae25:src/superclaude/skills/sc-implement-protocol/refs/qa.md`:82 (installed copy byte-identical, read 2026-10-24T04:36Z) already says a moved line alone is never an issue (`synthesis/hypothesis-04.md`, section 6). These historical failures cannot prove that rule is absent today. The managed delivery digest excludes task-owned artifacts (`research/scope-rules.md:45`). |
| Effort (proposed investigation only) | S. Reasoned estimate: two sessions, with preserved Git trees and durable logs already identified. |
| Risk (proposed investigation only) | Low. The investigation must not waive semantic support just because a cited line exists, and must not certify that archived files survive today. |
| Reuse of existing code/evidence | Preserved trees `f60d2c3…`, `3c5fdfa…` and `00d8f4a…`; the archived `t3-markdownlint.log` (present at screening on 2026-10-23 at 1,222 bytes, with the ledgers at their recorded lines; the retry-ladder `t8-test.log` was also present at 11,215 bytes; `research/scope-03-recovered.md:156-162`); nested reviewer transcripts. A fresh Read of the formerly archived `t10-markdownlint.log` under the recorded Coder worktree returned "file does not exist"; the nested transcript preserves its contents (`synthesis/hypothesis-04.md`, section 9). Candidate current location observed at `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t10-markdownlint.log` (1,006 bytes, observed 2026-10-24); identity with the historical log not hash-verified; availability to be confirmed before any approved replay. |
| Files/systems affected | Read-only: `research/06-session-0690ee9f.md`, `research/03-session-6f744b87.md` and their recorded package and transcript paths. |
| Pros | Cheap, and the cleanest proof-only control available (unchanged delivery digests). |
| Cons | Narrow reach. Cannot isolate the final credential pass from the policy change. |

### Option E: Late feasibility and repair-authority checks (Variant 5)

**Description:** A task reaches review before anyone establishes that its required evidence can be produced and that its blocking inputs can be corrected within the allowed scope. A resubmission then preserves a known unmet condition, so review correctly fails again (`synthesis/hypothesis-05.md`, section 1).

**How it works:** Correction authority and evidence-producing capability are separate barriers. The resubmission changes neither one, and a scoped human decision is eventually needed.

| Aspect | Assessment |
|--------|-----------|
| Mechanism | An already-identified failed property survives resubmission because it lies outside permitted correction, or because the environment cannot produce the required proof. |
| Support | **Oracle:** first-repair authority explicitly excludes the known `default_path=false` fixture. The second review confirms three repairs and repeats only that defect. Later authorization enables a one-field correction and a PASS (records 291, 383, 398, 450, 521, 573, 668; `t12-review-2.md:20-28`). **Documentation:** `/usr/bin/man` is a notice script, not a renderer, so the nominal zero exit status proved nothing. A static-only retry changed no text, and the second cannot-verify named the same clause (records 413-414, 430, 433-434, 443, 450, 506, 527; `research/03-session-6f744b87.md`, section 2). |
| Opposition | Neither requirement was intrinsically impossible: a correct fixture could have been authored before freezing, and a working renderer could satisfy the clause. Freezing is a legitimate anti-overfitting control. The re-review usefully confirmed three repairs. No malformed manual page was demonstrated. Screened Session 10 Task 4 and Session 17 Task 8 each converged after one repair, which cautions against treating any failed review as predicting a repeat; limits: Session 10's original implementation package was absent from searched locations, and Session 17's later PR reviews are separate work (`research/evidence-deck.md:650-651`). |
| Alternative explanations | Weak semantic assertions (V1) admitted the fixture. A weak availability guard ("when `man` is available") accepted a notice executable. Ordinary incomplete work explains the original omission. Renderer capability is an environmental limitation. |
| Scope | Two documented retained-blocker incidents, with different endpoints: authorized correction ending in PASS, versus accepted, unverified rendering. |
| Falsification | **Proposed, unexecuted.** Before comparing attempts, identify the failed property, the actual evidence-producing capability and the permitted correction. Check whether the next attempt changes the blocker or obtains the scoped decision. An unsupported repeat after a demonstrated permitted resolution would weaken the account. No installs, freeze bypass or altered criteria (`synthesis/hypothesis-05.md`, section 8). |
| Evidence strength | Strong for the two specific unchanged blockers. Moderate as a general explanation. |
| Debate record | Final positions 5, 5, 5, 4, 4. **For fourth:** "both V5 cases directly explain continued failure of an identified condition", while some V4 material explains attribution or a halt (V5 advocate, `ADV/debate-transcript.md:426`; V4 advocate `:384`). **Against:** "more direct for its two retained blockers, but narrower overall" (V1 advocate `:265`; V2 `:304`; V3 `:344`). The V5 advocate conceded its narrow reach, the original feasibility of both requirements, and the legitimate controls (`:414-416`). Unanimous writing nomination for endpoint point C-005. |
| Current rule vs historical observation | **Historical, observed:** the explicit exclusion of fixture changes at oracle record 383, and the weak availability guard in the generated plan. **Current rule, source-read only:** checkout master `git show 2165ae25:src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`:42 (dated observation, read 2026-10-24T04:36Z: the installed copy `/config/.claude/skills/sc-implement-protocol/refs/managed-workspace.md` and branch HEAD `bbbfcc4b`, which contains commit `c6009cd3` (Git-derived, read-only `git show`/`git log`; disclosed in the final report's header Scope line), both have this pin at line 43) pins plan and source after the first task starts (`research/scope-rules.md:45`). That is relevant to frozen-task repair authority, but historical restrictions still require captured evidence (`research/evidence-deck.md:728`). On feasibility, the installed implement text (read 2026-10-24) names infeasibility only through the retry adviser: an adviser returns `dispute` "when the AC is contradictory or infeasible" (`refs/retry.md`:73), a dispute halts `E-HALT-QA` for an operator Ruling (`refs/retry.md`:89), and advisers run only after attempt A2 has failed (`refs/retry.md`:9-13, :57). The AC check before any edit tests only that AC exist and state observable intent (`SKILL.md`:81-91), and the workflow generation gate has no feasibility check (`sc-workflow-protocol/refs/quality-gates.md`:24-41). Under the current text, infeasibility is therefore first named after two failed attempts. The content of the advisory pre-execution reflection was not inspected, and this does not show which bytes historical runs loaded. |
| Effort (proposed investigation only) | S. Reasoned estimate: two incidents, with artifacts located. |
| Risk (proposed investigation only) | Medium. The investigation must not install a renderer, bypass the freeze, alter acceptance criteria or execute the task. |
| Reuse of existing code/evidence | Oracle `t12-held-back-before-authorization.json` and the review artifacts. Documentation artifacts under the verified current root `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-210638/`: three hashes match there, including `artifacts/t6-fix-evidence.log`, while the old worktree path is gone (`research/03-session-6f744b87.md`, Current evidence location). |
| Files/systems affected | Read-only: `research/02-session-a9b88895.md`, `research/03-session-6f744b87.md` and those artifact roots. |
| Pros | Cheap. Two endpoints that are already explicit. |
| Cons | Narrowest reach. The result cannot change the sample-wide picture. |

### Options Comparison

| Criterion | Option A (V1) | Option B (V2) | Option C (V3) | Option D (V4) | Option E (V5) |
|-----------|----------|----------|----------|----------|----------|
| Transition it best explains | Old defect surviving a real pass | Absent-before/present-after introduction; separately, a retained sibling failure (not counted as introduction) | Rule-driven reopening or reversal | Proof-only rejection; false attribution | Unchanged known blocker |
| Direct contexts (not independent) | Oracle, monitor, Orca plan, CI plan | Orca plan cluster, monitor trap, CI graph | Credential, monitor, Orca/CI source conflicts | Credential (one work family), documentation baseline | Oracle fixture, documentation render |
| Strongest single evidence | Wrong oracle semantics pass tests (291, a truncated relay; full review at `t12-review-1.md:20-35` in the oracle artifacts folder) | Trap introduction 759-762 reproduced at 1240 | Two captured rubric loads; migration 874-902 | Proof-only pass with unchanged digest (332-435) | Explicit exclusion 383, repeat at 450 |
| Main counterexample | Oracle repairs 1-3 work | 14 accepted, 2 partial; most monitor defects preexist | Stable oracle/render criteria | Genuine follow-up lint failure; confounded pass | Requirements feasible; freeze legitimate |
| Final rank by advocates V1/V2/V3/V4/V5 | 1/1/1/1/1 | 2/2/3/3/3 | 3/3/2/2/2 | 4/4/4/5/5 | 5/5/5/4/4 |
| Writing-point contribution (not causal) | C-004 breadth | C-003 attribution | C-002 controls | C-007 historical evidence; writing base | C-005 endpoints |
| Effort (investigation) | M | M | M | S | S |
| Risk (investigation) | Medium | Low-Medium | Medium | Low | Medium |
| Maintainability | N/A: research-only; nothing is built or maintained | N/A, same reason | N/A, same reason | N/A, same reason | N/A, same reason |
| Integration complexity (investigation dependencies) | Needs V2's absent-before check to exclude introductions | Needs V1's counterexample to classify retained versus introduced | Must hold V4's proof state fixed to break confounding | Must hold V3's rubric fixed | Needs V1's check record to separate admission from persistence |
| Reuse potential | High: preserved versions in four contexts | High: logged successful edits | High: captured rule bytes | High: preserved trees and logs | High: verified artifact roots |

---

## 7. Recommendation

**Recommended approach:**
- Keep all five candidates as distinct mechanisms that can coexist.
- Present them under the reviewed provisional order **V1 > V3 > V2 > V5 > V4**, labeled non-consensus.
- Run no remediation.
- The next research-only step, if the user approves it, is to execute Option A's discriminating replay first (Section 7.6).

**Rationale:**
- V1 first is the only unanimous exact rank position, and every other conclusion is framed around it. Yet its own falsification test is unexecuted.
- The two disputed placements are disagreements about how to weigh explanatory reach against direct transition evidence. Further replays of the same six incidents cannot by themselves settle that. Section 7.6 states what could.

### 7.1 Provisional comparative ranking (most to least supported within this sample)

| Provisional rank | Candidate | Why at this position (recorded debate argument) | Advocates holding this exact position | Dispute status | Event-specific override |
|---|---|---|---|---|---|
| 1 | Checks prove less than the requirement (V1) | Widest reach: old defects escape across oracle, monitor and planning contexts, without blaming every repair (`ADV/debate-transcript.md:258,297,337,378,419`) | 5 of 5 | Unanimous | Overridden wherever a transition has introduction, contract-change, proof-only or retained-blocker evidence |
| 2 | Review contracts change (V3) | The shared target explicitly includes review entry and reversal, which V3 addresses directly; planning conflicts extend it (`:343,380,421`) | 3 of 5 (V3, V4, V5 advocates) | Disputed; below the four-of-five threshold | Leads for demonstrated rule-driven entry or reversal |
| 3 | Local repairs miss connected effects (V2) | Strongest introduction evidence, but it cannot claim preexisting monitor faults (`:343,379,385,425`) | 3 of 5 (V3, V4, V5 advocates) | Disputed; the V1 and V2 advocates rank it second (`:264,302`) | Leads for absent-before/present-after failures. Retained sibling failures carry V2's separate second-outcome label (S-002), never the introduction label (C-003) |
| 4 | Late feasibility and authority checks (V5) | Both incidents directly explain continuation of an identified failed condition; reach comparable to V4 (`:384,426`) | 2 of 5 (V4, V5 advocates) | Disputed; three of five place V4 above V5 | Leads for documented unchanged blockers |
| 5 | Brittle evidence and provenance handoffs (V4) | Narrow reach: one credential work family plus one documentation-baseline context; some evidence explains attribution or a halt rather than the repeat (`ADV/debate-transcript.md:381,384`; `ADV/refactor-plan.md:33`) | 2 of 5 (V4, V5 advocates) | Disputed; three of five place it fourth | Leads for isolated proof rejection or false attribution |

### 7.2 Recorded dissent and exact pair tallies

| Advocate | Final Round 2 explanatory-support order |
|---|---|
| V1 | V1 > V2 > V3 > V4 > V5 |
| V2 | V1 > V2 > V3 > V4 > V5 |
| V3 | V1 > V3 > V2 > V4 > V5 |
| V4 | V1 > V3 > V2 > V5 > V4 |
| V5 | V1 > V3 > V2 > V5 > V4 |

Source: `ADV/debate-transcript.md:477-484`; repeated at `return-contract.md:24` and `merged-root-cause-analysis.md:37-43`.

| Pairwise placement | Advocates supporting | Count | Reaches four-of-five threshold? |
|---|---|---|---|
| V1 first | All five | 5 of 5 | Yes |
| V3 above V2 (as displayed) | V3, V4, V5 | 3 of 5 | No |
| V2 above V3 (dissent) | V1, V2 | 2 of 5 | No |
| V4 above V5 (dissent from the displayed order) | V1, V2, V3 | 3 of 5 | No |
| V5 above V4 (as displayed) | V4, V5 | 2 of 5 | No |
| V1, V2 and V3 each above both V4 and V5 | All five (derived from the five recorded orders, not stated separately in the debate) | 5 of 5 | Yes |

**Consequences that must stay visible.**
- **Middle pair (V3 above V2).** The displayed placement follows the larger side of a 3-2 split.
- **Bottom pair (V5 above V4).** The displayed placement follows the smaller side. Three of five advocates placed V4 above V5. The reviewed refactor plan still adopted V5 above V4 as a qualified synthesis judgment under A-001's second criterion. It cited the direct continuation evidence (`ADV/refactor-plan.md:32`), and the independent plan review passed it (`ADV/plan-review-evidence.md:16`). The V4 advocate's own reversal is recorded separately in the debate transcript (`ADV/debate-transcript.md:384-385`).
- **No advocate majority holds the full displayed order.** Only the V4 and V5 advocates hold it. The merged analysis states that it "is not the majority's complete order" (`merged-root-cause-analysis.md:43`).
- **Weakest step.** The V5/V4 placement is the least-supported step in the ranking. A reader who weighs the tally would invert it, and neither direction reaches the threshold.
- **Status and Round 3.** The contract status stays `partial` for exactly this dissent (`return-contract.md:14,26`). Round 3 was not run, because the ten writing points converged; that convergence does not cover causal order (`ADV/debate-transcript.md:449-450`).

### 7.3 What the ranking does and does not mean

| Statement | Supported? | Basis |
|---|---|---|
| The order ranks explanatory support for this selected, clustered sample under A-001 | Yes | `ADV/diff-analysis.md:69`; `refactor-plan.md:9` |
| The order is the likelihood ranking the build request asked for ("rank the five by likelihood given this sample", `BUILD-REQUEST.md:34`; "ranked most to least likely", `:12`) | No. The debate adopted A-001's explanatory-reach rule instead, because the cards supplied no shared rule for comparing their likelihood (Section 1). The order ranks explanatory support. On 2026-10-24 the user accepted the explanatory-support order as the delivered answer; there is no re-ranking | `ADV/diff-analysis.md:64,69`; task log entry `[2026-10-24T06:32Z]` |
| The order gives probabilities, prevalence or a fleet-wide rate | No | `return-contract.md:24`; `research/evidence-deck.md:58,823` |
| Variant 4 being the writing base makes it the leading cause | No. V4 is ranked last. V1, unanimously first, had the lowest combined writing score; the numeric writing order was V4, V5, V2, V3, V1 | `ADV/base-selection.md:150,170-171` |
| Ten-of-ten writing convergence means causal agreement | No | `ADV/invariant-probe.md:20` |
| Any candidate is proven as the sole cause of a sequence | No; transitions can carry linked, separately supported labels | `ADV/invariant-probe.md:51-54` |
| Any proposed discriminating comparison was executed | No; all are unexecuted | `merged-root-cause-analysis.md:170,205` |
| The results generalize to models, versions or reviewer counts | No | `research/04-session-43582de1.md`, section 8; `research/evidence-deck.md:662` |

### 7.4 Overlap and dependency cautions

| Interaction | Observed example | Caution |
|---|---|---|
| V1 lets the defect in, V5 keeps it | Oracle: label/count checks admitted the false default-path fixture; the freeze then blocked its correction | Initial escape and later persistence are different transitions; one does not absorb the other |
| V1 precedes V2 | A weak behavioral check lets a connected problem escape (`synthesis/hypothesis-02.md`, section 6) | Do not count a single defect as both "missed" and "introduced" without separate before/after evidence |
| V3 reopens, V1 supplies the findings | Monitor migration forced a fresh review, which found old defects (records 849-906) | Re-entry rules explain why review happened, not why its findings were valid |
| V3 and V4 confounded | Credential third FINAL followed both pointer fixes and a rubric change (`research/06-session-0690ee9f.md`, section 5) | Neither candidate can claim that pass as its isolated effect |
| V2 within a V1-style family | The monitor error-handling family: the first repair introduced the trap regression, while sibling boundaries remained retained misses | An introduction can surface several rounds later; a late discovery does not mean the immediately preceding fix caused it (`research/evidence-deck.md:388,406`) |
| Repair exposes rather than creates | Monitor file-based transport exposed preexisting unbounded output | Not introduction; file transport did not cause oversized bodies (`research/evidence-deck.md:626`) |
| V4 checkpoint halt next to V5 render blocker | Documentation records 485-486 versus 430-450 | The guard halt is not the cause of the rendering failure and does not prove HEAD moved; it was triggered by a missing Q0 HEAD file, not a missing checkpoint (Section 2.5) |
| Shared clusters | Orca planning and monitor share a plan; credential packages share a work family | Multiple examples from one cluster are not independent breadth for any candidate |
| Acceptance endpoints | Monitor accepted four defects; render accepted as cannot-verify; fixture corrected to PASS | Accepted gaps are not repairs, and must not count as success for any mechanism (`merged-root-cause-analysis.md:155-165`) |

### 7.5 Current-rule weakness versus observed historical violation

| Candidate | Observed historical event | Current-rule observation (source-read, not historical proof) | Must not be inferred |
|---|---|---|---|
| V1 | Plans passed structural gates and still received valid semantic findings (planning log 499) | Generation checks are agent-performed schema checks at every depth, with coverage of source requirements checked only at standard/deep depth (installed `sc-workflow-protocol/SKILL.md`:54 and `refs/quality-gates.md`:24-39, read 2026-10-24; `research/scope-rules.md:32`) | That today's gate would miss the same defects |
| V2 | Successful amendments introduced plan defects; record 759-762 introduced the trap | Per-task review is scoped to the brief, the AC and the task's touched-file diff, with no neighbor-impact tracing beyond the AC; only the managed FINAL checks for later contradictions (installed `sc-implement-protocol/refs/qa.md`:9,31,77,82 and `SKILL.md`:118-121, read 2026-10-24; `research/scope-rules.md:41`) | That historical runs loaded this rule, or that it caused a particular introduction |
| V3 | Criterion softened without acceptance; consecutive reviewers loaded different rubric text; migration reopened a compliant check | Moved line alone is not an issue (`git show 2165ae25:src/superclaude/skills/sc-implement-protocol/refs/qa.md`:82; installed copy byte-identical); no stable finding-resolution registry (`research/scope-rules.md:56`); per-task reviewers are barred from the retry folders and never see adviser answers or briefs (installed `refs/qa.md`:90; `refs/retry.md`:16, read 2026-10-24) | Who changed the rubric; that the current rules match the historical loads |
| V4 | Proof lost at handoff; blank pointer missed; second failed FINAL absent from the ledger; post-edit HEAD baseline | Managed digest excludes task-owned artifacts (installed `sc-implement-protocol/refs/managed-workspace.md`:86, read 2026-10-24; `research/scope-rules.md:45`) | That the moved-line rule is absent today; that a ledger's FINAL count captures every review |
| V5 | Fixture changes excluded at record 383; weak "when available" render guard | Plan/source pinned after the first task start (`git show 2165ae25:src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md`:42, via `research/scope-rules.md:45`; installed copy and branch HEAD `bbbfcc4b` (Git-derived, read-only `git show`/`git log`; disclosed in the final report's header Scope line): line 43, read 2026-10-24T04:36Z). Infeasibility is first named only by a retry adviser's `dispute`, after A2 fails (installed `refs/retry.md`:9-13, :57, :73, :89; the AC check before edits tests existence and observability only, `SKILL.md`:81-91) | That historical runs loaded this rule, or that it explains the two V5 incidents |
| Not a card cause | Task 10 credential correction went beyond the named Tasks 7/8/17 authorization (record 2028) | N/A | Retained as an observed authority-boundary event, not ranked as a repeat cause |

Dated layer observation: the recorded seven-pair comparison found three equal and four different source/installed pairs at 2026-10-23T18:22:14Z (`gaps-and-questions.md:56`); that count is not re-measured here and is not a current statement. Any current-rule statement must name the exact layer and commit it read. The current-rule citations in Sections 6-7 use checkout master `2165ae25` in the read-only form `git show 2165ae25:src/superclaude/skills/<path>` (the checkout before the 2026-10-24T03:42:30Z branch switch), not the live working tree. In the installed layer `/config/.claude/skills/` (read 2026-10-24T04:36Z), the cited `qa.md` and `quality-gates.md` text is byte-identical at the same line numbers, and the managed-workspace pin text is at line 43; Section 2.3 lists every installed-layer equivalent.

### 7.6 Research-only next recommendation

All steps below are proposed, unexecuted, and require explicit user approval. They authorize no code change, protocol change, re-run of investigated plans, freeze bypass, renderer install or criterion waiver. Step-level targets are in Section 8 (`synthesis/synth-05-implementation-plan.md`), whose rows are grouped by mechanism rather than listed in this order; this table alone governs the recommended order. Order 4 appears there as a user scope decision and corresponds to Open Question 1 (`synthesis/synth-06-questions-evidence.md`, Question 1).

| Order | Proposed check | Why in this order | What would change the ranking |
|---|---|---|---|
| 1 | Option A replay on the preserved first-passing versions (oracle, monitor, Orca, CI), including a separate check of whether the relevant behavior test was deferred or absent (`synthesis/hypothesis-01.md:142`) | Tests the only unanimous exact rank position. If it weakens, the frame for every other placement changes | If the checks actually used already rejected the counterexamples, V1 loses its lead |
| 2 | Option C paired adjudication (fixed artifact, original versus loaded contract) on the credential and monitor transitions, alongside Option B absent-before/present-after replay on Orca, monitor and CI | These target the middle disputed pair with each side's own falsification test | Contract-only verdict changes strengthen V3; demonstrated additional introductions strengthen V2. Neither replaces the reach-weighting judgment |
| 3 | Option D and E checks on their two incidents each | Cheap, but narrow; cannot alter sample-wide reach | A repeat failure despite valid proof and a correct baseline weakens V4; an unsupported repeat after a permitted resolution weakens V5 |
| 4 (needs user scope decision) | Apply the debate's agreed transition labels (C-001) to additional, independently selected sessions | Only new, less clustered transitions can test reach, which is what the two disputed pairs turn on | A broader count of each transition class could settle the middle and bottom pairs; no outcome is predicted here |

**Trade-offs, and why they are acceptable.** Steps 1-3 reuse preserved evidence and stay read-only, so their risk is mainly misreporting: a replay presented as a review, or a plan defect presented as a runtime failure. That risk is controlled by the unexecuted/approval labels above. Step 4 costs more and changes the study's scope, which is why it is a user decision rather than a default.

### 7.7 Key-finding coverage

| Source | Key takeaway | Where represented |
|---|---|---|
| `research/01-session-ac2cd1fd.md` | Mixed-cause planning loop: correction-induced defects, coverage over-credit, source contradictions; stopped by authorized narrowing; v4 unreviewed | Options A, B, C; 7.4. The authorized narrowing and the authorized unreviewed v4 edit (raw 856, 858, 885, 889) are in Section 2.2 (Orca row) and Section 2.6 (Orca planning row). Section 4 (Key Takeaway Coverage, Orca planning row) records only the narrowed review and the unreviewed final amendment, without their authorization. Neither is in Sections 6-7 |
| `research/02-session-a9b88895.md` | Four valid defects, three repaired; frozen fixture retained; labels are not meaning; no new post-repair defect | Options A, E; 7.4 |
| `research/03-session-6f744b87.md` | Unchanged render blocker; false baseline attribution; head-moved is not proof; acceptance is not rendering | Options D, E; 7.4 |
| `research/04-session-43582de1.md` | Partial repairs across interacting checks; one graph introduction; "new" findings often not introduced; overclaims corrected | Options A, B, C |
| `research/05-session-e002bed2.md` | Progressive discovery of preexisting defects in a large unit; one trap regression; migration reopening; acceptance is not repair | Options A, B, C; 7.4 |
| `research/06-session-0690ee9f.md` | Lost durable proof; knowing relaxation; blank pointer missed; rubric change confounds the pass; second FINAL missing from the ledger | Options C, D; 7.4, 7.5 |
| `research/evidence-deck.md` | No single uniform loop; review claims need validation; human acceptance is a real stopping mechanism; no fleet rate | 6.0, 7.3, 7.4 |
| `research/scope-rules.md` | Current rules are not historical execution; two exact historical rubric loads | 7.5; Option C |
| `gaps-and-questions.md` | Reviewer-miss causes, rubric updater and runtime behavior unknown; clustered selection; protocol drift | 7.3, 7.5, 7.6 |

Excluded with rationale: screening slices `scope-01.md` through `scope-05.md` were not reread for this component. Their control dispositions are taken from the evidence deck's counterexample table (`research/evidence-deck.md:643-662`) and placed per control as shown below. These placements were added at Task Step 5.24 as synthesis-fidelity corrections. They do not change the ranking, and they are not presented as positions the debate advocates weighed.

| Screened control | Deck anchor | Placement | Reason or stated limit |
|---|---|---|---|
| Session 10 Task 4: missing comment corrected, compliant re-review | `research/evidence-deck.md:650` | Opposition rows of Options A, B and E | One-repair convergence. Limit: original implementation package absent from searched locations; logs and Edit survive |
| Session 17 Task 8: real deviation corrected, passing re-review | `research/evidence-deck.md:651` | Opposition rows of Options A, B and E | One-repair convergence. Limit: later PR reviews are separate development work |
| Session 17 FINAL: real restore-basename bug plus evidence defects corrected, then pass | `research/evidence-deck.md:652` | Option D Opposition | A real delivery bug found by FINAL. Limit: not strict fail-fix-fail |
| Sessions 13/14: authorized plan corrections without semantic re-review | `research/evidence-deck.md:655` | Option B Opposition | Not every corrected plan has a second failed review. Limit: an unreviewed correction is not clean approval either; their workflow review reports and the follow-up pre-review were linked from actual events but not fully read at screening (`research/scope-03-recovered.md:171`) |
| Session 09: seven compliant tasks; FINAL never ran | `research/evidence-deck.md:653` | Not placed in an Opposition row | Bounds what counts as an observed failure, not any single candidate's mechanism. Deck limit: overlapping writers are a real operational blocker |
| Session 19: nine compliant task reviews | `research/evidence-deck.md:654` | Not placed in an Opposition row | Bounds a shared-ledger block, not any single candidate's mechanism. Deck limit: later Task 12 belongs to another session |

### 7.8 Sources read and limits

| Source | Read status |
|---|---|
| Task file Step 5.12 and neighbors | Read (lines 250-359) |
| `/config/.claude/skills/tech-research/SKILL.md` | Synthesis Agent Prompt (779-811) and Report Structure through the checklist (1311-1531) read |
| Six case reports, `research/research-notes.md`, `research/scope-rules.md`, `gaps-and-questions.md` | Read in full |
| `research/evidence-deck.md` | Read in full (three reads). The producer recorded 901 lines; corrected to 900 by `wc -l` at Task Step 6.18 (the file ends with a newline and is unchanged since 2026-10-23T16:51Z) |
| `synthesis/hypothesis-01.md` to `-03.md` | Read in full. `-04.md` and `-05.md`: lines 1-170 (all ten sections; Evidence Trail partly) |
| `reviews/adversarial/run-evidence.md`, `return-contract.md`, `merged-root-cause-analysis.md` | Read in full |
| `ADV/diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, `refactor-plan.md`, `merge-log.md`, `plan-review-evidence.md`; `qa/adversarial-post-merge-validation.md` | Read in full |
| `ADV/base-selection.md` | Lines 1-414 and 540-578 read. Lines 415-539 (the middle of the reverse pass's per-criterion records) were not read; the summary of 150 of 150 forward/reverse agreements (125-136) was read |
| `ADV/variant-*-original.md`, `ADV/score-source-manifest.json`, `research/web-01-gap-applicability.md` | Not read directly. The variants' text is preserved verbatim in the formatted cards per their persistence records; the other two are outside this step's inputs |
| `synthesis/synth-05-implementation-plan.md` | Lines 1-40 only; referenced by path, not by step identifiers |
| Task Step 5.24 corrections (synthesis-gate fix cycle 1, 2026-10-24) | The rows above record the producer's Step 5.12 reads and are unchanged. The fixer read all six components in full, including `synthesis/synth-05-implementation-plan.md` (basis for the 7.6 grouping and order-4 note); read `ADV/variant-2-original.md` lines 10 and 37 and `ADV/debate-transcript.md:269,272` (basis for Option B's two outcomes); and re-read every other source range its corrections cite, including `research/evidence-deck.md:650-655` for the 7.7 control placements (`qa/qa-synthesis-fix-log.md`, Items Reviewed and Actions Taken) |

**Limits.**
- Graph coverage was unavailable for package files, so all conclusions come from direct reads.
- Historical JSONL anchors are carried forward from the case reports and cards, not replayed.
- Effort sizes are reasoned estimates.

## Provenance and Delivery Record (not for assembly)

<!-- NOT-ASSEMBLED: everything from this heading to the end of the file is producer handoff and parent delivery provenance, not report content. Do not copy it into the final report. -->

The producer's original header lines, moved here unchanged at Task Step 5.24 (the Status line's remaining sentence, "The ranking below inherits the adversarial return status `partial`, because the causal order is not a consensus.", stays in the header):

**Status:** Component complete as text for Task Step 5.12. Parent persistence and the independent second-partition synthesis gate (Steps 5.14, 5.16, 5.18, 5.20 and 5.22) are still pending.

**Intended component:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-04-options-recommendation.md`

**Persistence:** This worker's higher-priority instructions forbid writing report files, so no stub or file was created. This text is the complete component for the parent to persist. No other file was changed. No debate was re-run or simulated, and no test, agent, Git, staging, archive, move, delete, external query or publication action occurred.

The producer's original DONE/NEXT handoff table, moved here unchanged from the end of section 7.8:

| Status | Result |
|---|---|
| DONE | Wrote sections 6 and 7: five assessment tables, an options comparison, the provisional non-consensus ranking with exact advocate orders and pair tallies, overlap cautions, current-versus-historical separation, and a research-only recommendation. |
| DONE | Recorded that the displayed V5-above-V4 placement is held by only two of five advocates, while V3-above-V2 is held by three of five; neither reaches four of five. |
| NEXT | Parent persists this text at `synthesis/synth-04-options-recommendation.md`; Steps 5.14, 5.16, 5.18, 5.20 and 5.22 then review it independently. |

### Parent Persistence Record (2026-10-24)

The parent persisted this exact restricted return from current session subagents/agent-asynth-04-ranking-*.jsonl (latest text beginning with this title; 336 physical lines, 52,248 UTF-8 bytes before this record). The target did not previously exist. The parent read sections 6.0-7.8 and checked the advocate orders in 7.2 directly against `reviews/adversarial/adversarial/debate-transcript.md:477-486`: they match exactly, including "V3 above V2 has 3/5 support; V4 above V5 has 3/5 support", so the displayed V5-above-V4 step follows the 2-of-5 side as the reviewed refactor plan's qualified judgment. No percentage or probability appears. The worker's "parent persistence pending" status is its original handoff state, resolved here. This record is not an independent synthesis-gate verdict.

### Delivery Receipt (2026-10-24, Task Step 5.24)

The file exists at its intended component path, and its delivery is recorded in the Parent Persistence Record above. The persisted bytes before Task Step 5.24 had SHA-256 `e3a8900b7c6899c3ca149b1052e0fcf8c30208d1c9c79c8c29e1e791442ebf8d` (53,087 bytes), the identity the Phase 5 synthesis-gate reviewers examined (`qa/qa-consolidated-findings-phase5.md`, Targets bound at consolidation). Task Step 5.24 (synthesis-gate fix cycle 1) moved the producer handoff lines here and records its corrections to this file in `qa/qa-synthesis-fix-log.md`. This receipt records delivery only. It states or implies no synthesis-gate verdict.
