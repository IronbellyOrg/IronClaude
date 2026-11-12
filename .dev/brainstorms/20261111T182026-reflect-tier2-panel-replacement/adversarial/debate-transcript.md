# Adversarial Debate Transcript

## Metadata

- Depth: standard. Rounds completed: 2 (invariant probe pending).
- Convergence: R1 56/68 = 0.824 (82.4%); R2 60/68 = 0.882 (88.2%). Threshold 0.75. Focus: All. Advocates: 3 (V1 opus:architect, V2 sonnet:analyzer, V3 haiku:backend).
- Points debated: 68 = structural 12, content 25, contradictions 20, promoted shared assumptions 11 (of 15 A rows; unpromoted: A-007, A-011, A-013, A-015). U rows are not debated points.
- R2 stable-majority check: 51 of 68 points have the same majority winner in R1 and R2.
- Method: agreed = at least 2 of 3 advocates give the same variant as Winner in their per-point table; a NONE majority counts as unresolved. Confidence: unanimous 90 (+4 if R1 was also unanimous on that variant, +4 if no advocate changed vote), max 98; 2 of 3 = 65 (+10 if R1 majority matched, +5 if the third advocate abstained with NONE), max 89; unresolved = 50. No losing-side R2 row concedes its point, so no concession bonus was applied.
- Full round texts are kept in `debate/round1-variant-N.md` and `debate/round2-variant-N.md` (N = 1..3) and are referenced here, not copied.

## Round 1: Advocate Statements

### Variant 1 advocate (`debate/round1-variant-1.md`)

- Position: the layered Review Kernel (K1 resolution, K2 dispatch, K3 findings, K4 merge) with a validator-legal template and consumer-level contract plan is the best long-term base; V3's failure model and V2's T1 arm are to be grafted on.
- Concessions (11): executor exclusion must degrade not raise (X-002, C-017), headless contract constant is "1.0" (X-003), sidecar drops calibration (X-009, A-004, X-008), cost units and the 65.6k hard kill (X-012, X-013), debate-removal claim overstated (X-006), no T1 arm (A-001), ESCALATE in the cap-1 ledger (X-017), pre-check could drop valid citations (A-010), gateway alias dispatch fails (X-010), failure states missing (C-024).
- R1 votes over 68 points: V1 32, V2 11, V3 22, NONE 3.

### Variant 2 advocate (`debate/round1-variant-2.md`)

- Position: stage-gated panel-fed Tier 2: take resolution and clustering first, keep debate, calibration and evidence gate, and remove the debate only after a measurement that includes a T1-only arm.
- Concessions (10): V2's Q4 template is invalid, the sidecar claim and token units are wrong (X-001, X-008, X-012, A-005), version misread (X-003), stage 5 labelled additive (X-004), off-by-one cites (X-019), concatenation blurs identity (X-007), thin failure handling, unread files, and the A-006 class mapping gap.
- R1 votes over 68 points: V1 22, V2 12, V3 22, NONE 12.

### Variant 3 advocate (`debate/round1-variant-3.md`)

- Position: the strongest first migration shares infrastructure without changing what a successful audit means: real adversarial finalization stays authoritative, incomplete work cannot read as clean, retries add no votes.
- Concessions (7): headless version is "1.0" not 1.8.0 (X-003), cheaper-calibrator preference changes existing policy (C-018, X-016), quorum claim overstated, manifest is not a multi-file transaction, exact key under-merges (C-005), measurement is costly and lacks T1, pre-support wording too broad, headline cost labelling.
- R1 votes over 68 points: V1 9, V2 6, V3 46, NONE 7.

## Round 2: Rebuttals

### Variant 1 advocate (`debate/round2-variant-1.md`)

- Stays with V1's skeleton and template as the base, adopts V3's policy for stages 0-4 (debate kept, adversarial merge method) and V2's T1 arm. Withdrew the sidecar and moved to REJECT on A-004, A-006, A-009. New evidence: the "1.0" headless builder is post-only (ensemble.py:797), so a pre-only contract change never touches it.
- R2 votes: V1 28, V2 11, V3 23, NONE 6. Votes changed from R1: 4.
- Remaining disagreements are listed in its `## Remaining disagreements` section.

### Variant 2 advocate (`debate/round2-variant-2.md`)

- Concedes V1 adopted the stage gate, so V1's template is the only one that runs as written; keeps a T1 arm as a hard entry criterion; moved to REJECT on A-004, A-009, A-010. Remaining disputes: C-005 key, C-018/X-016 calibrator tier, C-022 mechanism, X-010 gateway dispatch (voted NONE).
- R2 votes: V1 25, V2 11, V3 22, NONE 10. Votes changed from R1: 15.
- Remaining disagreements are listed in its `## Remaining disagreements` section.

### Variant 3 advocate (`debate/round2-variant-3.md`)

- Concedes under-merging, adapter cost, and the finding-core spec to V1, but holds that V3's verdict, completion and final-publication policy should be the base with V1's interfaces imported. Rejects the 15-point panel gate (C-013), the resolution-only-first stage (C-014 votes V2), and treats A-002/A-003 as unestablished.
- R2 votes: V1 18, V2 10, V3 31, NONE 9. Votes changed from R1: 23.
- Remaining disagreements are listed in its `## Remaining disagreements` section.

## Scoring Matrix

| Diff Point | Level | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|
| S-001 | L2 | UNRESOLVED | 50 | Same order in all three. V3: Shared ordering; sentence styling is not decisive. |
| S-002 | L2 | V1 | 98 | Five candidates with verdicts plus a matrix; all three advocates agree. |
| S-003 | L1 | V2 | 75 | Path abbreviation and PROPOSED/UNVERIFIED markers keep citations auditable; Dissent V1 (votes V1): Separates enrichment provenance from lines read. |
| S-004 | L1 | UNRESOLVED | 50 | Heading style only; V3: Heading punctuation is not a design advantage. |
| S-005 | L2 | V3 | 90 | Answers are available in place. |
| S-006 | L2 | V1 | 98 | "v1?" and "Set by" columns expose field ownership. |
| S-007 | L2 | V1 | 90 | Command-level steps; V3's execution contract is credited under S-008. |
| S-008 | L3 | V3 | 98 | Completion, retry and resume obligations are explicit. |
| S-009 | L2 | V1 | 98 | "What ships" plus entry, exit and rollback per stage. |
| S-010 | L2 | V1 | 90 | Consumer-level change list with the verified wrapper guards (contract.py:299-300, 317-318, R1 read). |
| S-011 | L2 | V3 | 98 | Separates estimates and incompatible units. |
| S-012 | L2 | V1 | 98 | Full PROPOSED-name inventory. |
| C-001 | L2 | V1 | 90 | Widest candidate set; D and E are named stages and rollbacks. |
| C-002 | L2 | V1 | 65 | Kernel skeleton as the base, with V3's policy for Stages 0-4 (debate kept, adversarial merge method); Dissent V3 (votes V3): Share mechanics without changing verdict authority. |
| C-003 | L2 | V1 | 75 | Most complete take, lack and stay map; Dissent V3 (votes V3): Includes execution identity and incomplete outcomes. |
| C-004 | L2 | V1 | 90 | Superset keeps one parser for spec-panel; add V3's completion state and `channel` as optional v2 fields. |
| C-005 | L3 | V1 | 75 | With the primary-citation fix it equals v1 on the reviewed file and clusters paraphrases; Dissent V3 (votes V3): Exact storage plus related groups avoids destructive collapse. |
| C-006 | L2 | V2 | 90 | Keep the pre debate until a T1-armed measurement; V1 R2 and V3 now agree. |
| C-007 | L2 | UNRESOLVED | 50 | V1 (V1): Pre-cluster plus a kept debate, with calibrated cards (fixed per X-009). V2 (NONE): All three keep the post debate with cluster pre-processing, so the differences are not decision-relevant. |
| C-008 | L2 | V2 | 75 | The `launch` null/non-null rule fits the tool enum; add V3's override-before-freeze rule. Dissent V3 (votes V3): Immutable identity must govern both transports. |
| C-009 | L2 | V1 | 90 | Only concrete template that passes panel.py:140-141 (R1 read). |
| C-010 | L2 | V1 | 75 | Most executable pre flow; add V3's input-drift recheck. Dissent V3 (votes V3): Final validation, drift and readiness complete the flow. |
| C-011 | L3 | V3 | 98 | Attempts cannot add votes or clear findings. |
| C-012 | L2 | V3 | 98 | Honest units; hypothetical savings remain hypothetical. |
| C-013 | L2 | V2 | 75 | Numeric 15-point gate for a larger panel. Dissent V3 (votes V3): Preserve rubric; no unsupported automatic panel expansion. |
| C-014 | L2 | V1 | 75 | Shadow stage and byte-identity exit test; Dissent V3 (votes V2): Resolution-only first minimizes initial mutation. |
| C-015 | L2 | V3 | 90 | Corrected engine-specific preservation needs no initial new meaning. |
| C-016 | L2 | V3 | 98 | Genuine child score preserves convergence semantics. |
| C-017 | L3 | V3 | 90 | Anchor replacement and all-fallback identity enforcement. |
| C-018 | L3 | V1 | 90 | Opus calibrator is today's rule (SKILL.md:1181); embedded-calibration fix adopted. |
| C-019 | L3 | V1 | 75 | Pre-check drops only a missing file or range, then the unchanged validator. Dissent V3 (votes V3): Final gate checks synthesized claims, not just inputs. |
| C-020 | L2 | V2 | 98 | Only V2 has a T1 arm and a stop rule; V1's shared cards go inside it. |
| C-021 | L3 | V3 | 98 | Actual judge identity and collision accounting. |
| C-022 | L2 | V1 | 80 | A concrete mechanism for the verified constant 0 (ensemble.py:817). Dissent V3 (votes NONE): Neither proposal fully specifies headless semantic-gate integration. |
| C-023 | L2 | V1 | 90 | Role-qualified documents keep identity, the same idea as V3 but concrete. |
| C-024 | L3 | V3 | 98 | Complete-empty differs from failed/truncated output. |
| C-025 | L1 | UNRESOLVED | 50 | Names have no intrinsic merit; V3: Names do not establish behavior. |
| X-001 | L3 | V1 | 90 | One fixed slot; V3 offers no template to test. |
| X-002 | L3 | V3 | 90 | Replace anchor; preserve known-executor exclusion and N=2 floor. |
| X-003 | L2 | UNRESOLVED | 50 | All misstated; damage limited to headless post (ensemble.py:797). V3: Original universal-version claims were wrong. |
| X-004 | L2 | V1 | 98 | A widened legal set is a major change; all advocates agree. |
| X-005 | L2 | V3 | 98 | Real adversarial finalization avoids own-merge violation. |
| X-006 | L2 | V2 | 90 | Agreement is not recall; keep until measured. |
| X-007 | L2 | V3 | 75 | Single `--doc` plus identity loss rules out concatenation as an identity store. Dissent V1 (votes V1): Separate documents via role-qualified `--doc`; concatenation loses identity. |
| X-008 | L2 | V3 | 90 | Repaired calibrated view preserves embedded record. |
| X-009 | L2 | V3 | 98 | Full calibration reaches finalizer inputs. |
| X-010 | L2 | UNRESOLVED | 50 | V1 (V2): Its dispatch rule avoids the enum limit. V2 (NONE): The model enum rejects gateway aliases; my launch rule only defers gateway dispatch to a swarm path that is not shown for reflect pre. |
| X-011 | L2 | V2 | 90 | The recorded pre card shows pre use exists; the agent text is post-only. |
| X-012 | L2 | V3 | 98 | Turn budget is not measured output-only usage. |
| X-013 | L3 | V3 | 98 | Correct arithmetic without converting units. |
| X-014 | L2 | V3 | 80 | Arithmetic right; target vs allowance explained. Dissent V2 (votes NONE): A minor text gap in V3 between target and allowance. |
| X-015 | L2 | V3 | 90 | Reconciled planning arithmetic versus withdrawn inconsistent nets. |
| X-016 | L2 | V1 | 90 | Opus as calibrator follows SKILL.md:1181 and is less Opus than today. |
| X-017 | L3 | V3 | 90 | Revision decision must not become reflect authority. |
| X-018 | L1 | V2 | 90 | V1 itself agrees V2's ledger cites are the correct ones and its own are wrong (as cited by V1 R1, R2). |
| X-019 | L1 | V1 | 98 | 405 and 408 are correct. |
| X-020 | L1 | V2 | 98 | Names the Fable entry and a resolve-time filter. |
| A-001 | L2 | V2 | 98 | Only V2 states and tests the assumption. |
| A-002 | L2 | UNRESOLVED | 50 | No variant plans a gateway run. V3: No complete gateway transfer study proposed. |
| A-003 | L2 | UNRESOLVED | 50 | All three still carry a quote field; none establishes lossless conversion of line-only evidence. V3: Lossless line-only conversion remains undesigned. |
| A-004 | L2 | V3 | 98 | Preserve full cards and calibration provenance. |
| A-005 | L2 | V3 | 98 | Separate measurement bases. |
| A-006 | L3 | V1 | 90 | The explicit per-model `class` map is the concrete fix. |
| A-008 | L2 | V3 | 80 | Requires an independent post trial before narrowing. Dissent V2 (votes NONE): The only post datapoint is an unread snippet. |
| A-009 | L2 | V1 | 90 | The only variant that makes the consumer grep a hard stage-entry gate. |
| A-010 | L3 | V3 | 98 | No automatic quote-mismatch rejection layer. |
| A-012 | L2 | V2 | 90 | Seeded defects paired with a union ledger of natural findings; V1 R2 and V3 R1 both ask for that pairing. |
| A-014 | L3 | V1 | 98 | The only explicit byte-identical spec-panel test. |

## Shared assumption outcomes

- A-001: V1 QUALIFY, V2 QUALIFY, V3 QUALIFY. Handling: QUALIFY: pre T2 value is unmeasured; a T1-only arm is a hard entry criterion for any pre change beyond resolution-only adoption. Scored point: V2/V2/V2 -> V2.
- A-002: V1 QUALIFY, V2 QUALIFY, V3 REJECT. Handling: QUALIFY (2 of 3): Haiku stand-in runs certify mechanics and anthropic-only behaviour only; a gateway default needs its own run (none planned). V3's REJECT applies to quality claims. Scored point: NONE/NONE/NONE -> UNRESOLVED.
- A-003: V1 REJECT, V2 REJECT, V3 REJECT. Handling: REJECT: the recorded card cites line refs only; `quote` must be optional when path and line range exist, and lossless conversion is undesigned. Scored point: NONE/NONE/NONE -> UNRESOLVED.
- A-004: V1 REJECT, V2 REJECT, V3 REJECT. Handling: REJECT: a findings-only reduction loses dimensions, reasons and notes; keep the full calibrated card embedded (any sidecar is an index). Scored point: V3/V3/V3 -> V3.
- A-005: V1 REJECT, V2 REJECT, V3 REJECT. Handling: REJECT: turn-budget, output-token and artifact-size figures are not comparable; keep units separate per lane. Scored point: V3/V3/V3 -> V3.
- A-006: V1 REJECT, V2 REJECT, V3 REJECT. Handling: REJECT: SKILL.md:1180 classes do not match the gateway tier models; an explicit per-model class map and actual-identity check are preconditions for exclusion and the disjoint rule. Scored point: V1/V1/V1 -> V1.
- A-008: V1 QUALIFY, V2 QUALIFY, V3 QUALIFY. Handling: QUALIFY: keep the post debate; the only post datapoint is an unread snippet, so a separate post trial is needed before any narrowing. Scored point: V3/NONE/V3 -> V3.
- A-009: V1 REJECT, V2 REJECT, V3 REJECT. Handling: REJECT: the consumer map is not complete (the "1.0" headless builder was missed); a repo-wide grep is a hard stage entry gate. Scored point: V1/V1/V1 -> V1.
- A-010: V1 REJECT, V2 REJECT, V3 REJECT. Handling: REJECT: a failed locate is not proof of an unfounded citation; the pre-check may drop only a missing file or out-of-range line, the validator decides the rest. Scored point: V3/V3/V3 -> V3.
- A-012: V1 QUALIFY, V2 QUALIFY, V3 QUALIFY. Handling: QUALIFY: seeded or authored defects need pairing with a union ledger of natural findings and blinded grading. Scored point: V2/V2/V2 -> V2.
- A-014: V1 QUALIFY, V2 QUALIFY, V3 QUALIFY. Handling: QUALIFY: non-interference is a property to test; new flags default off and a byte-identical v1 spec-panel merge test is the acceptance criterion. Scored point: V1/V1/V1 -> V1.

## Convergence Assessment

- Points resolved: 60 of 68; alignment 88.2% (R1 82.4%). Threshold 75%. Unanimous in R2: 47; 2 of 3: 13.
- Status: CONVERGED.
- Unresolved ids (8): S-001, S-004, C-007, C-025, X-003, X-010, A-002, A-003. S-001, S-004, C-025, X-003, A-002, A-003 are all-NONE (no variant wins); C-007 and X-010 have a single variant vote against two NONE.
- Variant tally (points won in R2): V1 25, V2 11, V3 24, unresolved 8.

| Level | Points | Agreed | Addressed |
|---|---|---|---|
| L1 | 6 | 4 | yes |
| L2 | 47 | 41 | yes |
| L3 | 15 | 15 | yes |
| Total | 68 | 60 | |

## Emerging consensus

- Architecture shape: V1 (2 of 3 on C-002, with V3's policy grafted on and V2's stage gate); layered kernel skeleton with candidate set, finding superset and mapping (C-001, C-003, C-004, S-002, S-006, S-009, S-010, S-012 all V1). Contested: V3 holds its verdict/completion policy should be the base.
- Debate fate, pre-execution: V2 (3 of 3, C-006): keep the pre debate until a measurement that includes a T1 arm; X-006 V2, A-001 V2 QUALIFY.
- Debate fate, post-execution: all three keep the post debate; C-007 is unresolved only because V2 and V3 vote NONE (V1 votes V1 for pre-cluster input); A-008 V3 (2 of 3) QUALIFY, X-005 V3 keeps the adversarial merge method.
- Contract version policy: V3 (3 of 3 on C-015, C-016): no contract change for the first pre shipment, version stays 1.8.0, `merge_method: adversarial` with the real child score in pre mode, deterministic agreement is internal telemetry; X-004 V1: any widened legal set is a major change; X-003 NONE (all misread the "1.0" headless builder, which is post-only).
- Engine: V2 (2 of 3, C-008; V3 dissents for immutable binding): per-reviewer `launch` null/non-null rule with V3's pin-before-freeze added; X-010 unresolved (gateway dispatch for pre is unproven).
- Calibrator placement and model tier: V1 (3 of 3, C-018, X-016): per-card blind calibration, disjoint class, Opus by today's SKILL.md:1181 rule; embedded calibration kept (X-008, X-009 V3; A-004 REJECT).
- Evidence-gate placement: V1 (2 of 3, C-019): deterministic pre-check dropping only a missing file or range, then the unchanged validator; A-010 REJECT; C-022 V1 (2 of 3) closes the headless citations_dropped gap.
- Executor-class exclusion mechanism: V3 (3 of 3, C-017, X-002): filter candidates before dispatch, check actual identity, replace an ineligible anchor before resolution (degrade, do not raise); A-006 V1 REJECT requires an explicit class map; C-021 V3 records judge collisions.
- Finding format and dedupe key: V1 superset (3 of 3, C-004) with V3's completion state as optional fields; C-005 V1 (2 of 3) with the primary-citation fix; V3 dissents for the exact key; C-023 V1, X-007 V3 (2 of 3, separate documents, no concatenation).
- Rounds, ledger, revise: V3 (3 of 3, C-011): single pass, retries are attempts not votes, no automatic clearing; X-017 V3 avoids a misleading ESCALATE; C-024 V3 five completion states; S-008 V3 state machine, idempotency and atomic publish.
- Cost model and not-worth-calling rule: V3 (3 of 3, C-012, X-012, X-013, X-014 2 of 3, X-015, A-005) keeps units separate and respects the 65.6k hard kill; C-013 V2 (2 of 3) numeric 15-point gate for a larger panel, V3 dissents.
- Staged migration: V1 (2 of 3, C-014) shadow stage and byte-identity exit, with Stage 3 gated on V2's measurement; V3 dissents for resolution-only first; A-014 V1 QUALIFY.
- First measurement: V2 (3 of 3, C-020): three arms including T1, seeded defects plus a union ledger (A-012 V2 QUALIFY); X-011 V2, A-001 V2.

## Open disputes

- C-002 (V1 2, V3 1, impact High): V1 - kernel skeleton and template are the only version that runs as written, graft V3 policy; V3 - mechanics may be shared without changing verdict authority, V3's policy should be the base.
- C-005 (V1 2, V3 1, impact High, L3): V1/V2 - primary-citation proximity key clusters paraphrases without cross-task merging; V3 - exact storage plus related groups avoids destructive collapse.
- C-007 with A-008 (unresolved, impact High): V1 - pre-cluster input to a kept post debate is worth keeping; V2/V3 - all variants keep the post debate, so the difference is not decision-relevant and replacement needs its own post study.
- X-010 with C-008 (unresolved, impact High): V1/V2 - the launch null/non-null rule avoids the model-enum limit; V3/V2 - gateway dispatch for pre remains unproven, so immutable binding and no claim of conformance.
- C-014 (V1 2, V2 1, impact Medium): V1 - shadow stage plus byte-identity exit is equally small at runtime; V3 - resolution-only first minimises initial mutation.
