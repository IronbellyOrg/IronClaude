---
round: 2
advocate: Variant 2 (sonnet:analyzer)
generated: 2026-11-11
reads_this_round: diff-analysis.md; round1-variant-1/2/3.md; round2-variant-1.md; skills/sc-reflect-protocol/SKILL.md:1172-1195; cli/reflect/ensemble.py:784-819; cli/review/panel.py (grep of fixed/exclude, lines 35, 97, 132-141, 386-408, 447-453, 479-487). Paths are under src/superclaude/. Any other line number below is quoted from another advocate's statement and is marked "(as cited by ...)".
---

# Round 2, Variant 2 (analyzer): rebuttal

## Responses to criticisms

1. **"V2's template needs two fixed slots; the validator rejects it" (V1 R1, V3 R1, X-001).** Conceded in full, and the grep confirms it again. `panel.py:140-141` rejects any template where the count of fixed slots is not exactly one. The calibrator is also not a slot at all. SKILL.md:1176-1181 (read) makes it a rule: pick the highest-capability class from the set that is disjoint from the reviewer classes. The repair is to delete the `cal` slot. The template keeps one fixed `t1b` anchor plus random slots, and the calibrator is chosen by the section 11.3 rule outside the template. V1's template is the concrete one, and I adopt its shape.

2. **"Concatenating plan and spec loses source identity" (V1, V3, X-007, C-023).** Conceded. Merge takes one `--doc` (as cited by diff-analysis X-007). Concatenation was a workaround for that limit, not a design preference. The repair: the original files stay the identity store, and the concatenated `review-doc.md` is only a mapped view with H3 `path:start-end` headings. If the merge input cannot carry roles, a role-qualified input (V1) has to be built. That input is a PROPOSED change, not an existing option, in V1 and V3 alike.

3. **"Stage 5 is not 'additive 1.9.0'; it is a semantic change" (V1, V3, X-004).** Conceded. SKILL.md:952-953 (as cited by diff-analysis) puts any change to the legal `merge_method` set under a major version. Stage 5 either carries a major bump or does not ship. The staging never needed stage 5 to ship, and that is the point of gating it.

4. **"V2 confuses cost units and contradicts itself on the net" (V1, V3, X-012, X-015, A-005).** Conceded. The 35k-70k figure is a turn-budget figure, not output tokens. I also gave two nets, "-5k to +3k" and "0 to -2k". Retract both. The accurate claim is that stages 1-4 move composition, not cost, and no saving is claimed until a measurement exists. V3's 65.6k hard-kill arithmetic is the correct ceiling for any lane budget (as cited by V3 and V1 R1).

5. **"Calibration sidecar exists 'as it does now'" (V1, V3, X-008).** Conceded. Calibration is an embedded block inside the card (diff-analysis X-008: lines 82-103 of the recorded card). The calibrated card stays authoritative. Any sidecar is an index.

6. **"`T2ModelNN` env overrides applied after resolution create a second identity authority" (V3 R1 weakness 3; V1 R2 agrees).** Conceded. Look at `panel.py:479`: the exclude list is built only from models already chosen in earlier slots, so a late override would make the recorded resolution differ from what was dispatched. The repair is to fold an explicit `T2ModelNN` into the resolution as a pin before it is frozen, or to reject the mismatch. My R1 rule of "env wins" is kept only in that pre-freeze form.

7. **"V2 has no failure model" (V1, V3, S-008, C-024, U-014 to U-017).** Conceded. V2 only counted valid-block reviewers toward N=2. I adopt V3's five completion states, the rule that a retry is an attempt and never a vote, and an atomic publish after the manifest commit, grafted on at stage 2.

8. **"Span overlap on one concatenated document merges cross-task findings" (V1 R2 new evidence 5).** Conceded as to the concatenated view. If anchors are tied to the combined file, two tasks whose anchors sit near a shared requirement line can fall within the 3-line window. On a single reviewed file, today's matcher (as cited by V1 R2: `findings.py:363-378`, which I did not re-read) reads the finding's own anchors, so that is v1 behaviour. V1's primary-citation-only rule is the right fix and it supersedes my concatenation-based rule.

9. **"The quote-locate pre-check can drop valid paraphrased citations" (V3 weakness 7, A-010).** My R1 design added the pre-check as `annotate` plus a path and line check ahead of the validator. I concede that it may only drop a missing file or an out-of-range line. A quote mismatch is flagged and passed to the validator, which remains the authority. This matches what V1 now says.

10. **"Opus on every calibrator breaks the brief's 'sparingly'" (V3, X-016).** Partly rebutted, partly conceded. Verified: SKILL.md:1181 already says "pick the highest-capability calibrator class from the disjoint set". Today, when Opus is not a reviewer, Opus is the calibrator. So V2 does not invent Opus use. The brief's "sparingly" is not quantified, though, and I have not measured Opus output per calibrator re-grade. The concession: Opus as calibrator stays the default only because policy already says so. It needs the U-012 ablation (two reviewers plus an Opus calibrator against three reviewers with two Haiku stand-ins) before it is called justified.

11. **"V2's `contract_version` 1.8.0 is wrong" (V1, V3, X-003).** Partly conceded. `ensemble.py:788` writes `REFLECT_CONTRACT_VERSION` and `ensemble.py:797` hard-codes `"mode": "post"` (both read this round). So the constant I never read belongs to the headless post builder. The "1.8.0 unchanged" statement is still wrong for that builder, and is untested for the pre agent-session path.

12. **"Executor exclusion: 'drop the slot and report' breaks the one-fixed rule" (V1, V3, X-002, C-017).** Conceded. If the only tier1b model is the executor's class, dropping the fixed anchor leaves zero fixed slots and fails `panel.py:140-141`. SKILL.md:1190 (read) says the three pools SHOULD be pairwise disjoint and that they degrade with telemetry when they cannot. V3's rule is consistent with that: replace the anchor before resolution, then degrade with telemetry. I now vote for it.

13. **"The `panel.py:405, 409` cite is off by one" (X-019).** Conceded. The grep shows `or candidates` fallbacks at 405 and 408 and the fixed pick at 402.

14. **"V2 is not the base architecture; it has no concrete composition that runs" (V1 R2).** Accepted for implementation structure, rejected for the decision rule. V1 R2 now keeps the pre debate through stage 4, adds a T1 arm and moves removal behind a measurement. That is the stage gate V2 argued for. What V2 adds beyond V1 R2 is the stop rule, which V1 R2 left implicit.

## Updated assessment of other variants

**Variant 1, steelman.** V1's strongest case: the maintenance unit is the layer, not the command. Reviewer identity, finding shape and merge each become one implementation with a schema id, so a third consumer adds only a template, a brief and a mapping. V1 also has the only validator-legal template, the only superset finding format that leaves spec-panel's parser alone, the only byte-identical v1 merge test, and a consumer-by-consumer contract plan. After R2, V1 has withdrawn its three weakest claims: removal by default, the `panel` merge value shipping early, and the sidecar calibration. It also fixed its dedupe rule to primary citations only, which is the correct repair of the cross-task merge risk V3 found. Remaining weakness: its shadow experiment still has no T1 arm of its own in the shipped plan. It adopts one only in prose. Its 0.10 non-inferiority margin was also conceded as too wide. And the layered kernel is still a large build with no cost estimate for the build itself.

**Variant 3, steelman.** V3's strongest case: share the transport and keep the verdict meaning. A real adversarial finalizer leaves `merge_method`, `adversarial_convergence_score` and gate 9 untouched, so no consumer migrates. V3 alone treats failure honestly: five completion states, a retry identity that adds no votes, and atomic publish. V3's R1 attack on V2 and V1 was accurate on every point I could check. Its concessions in R1 narrowed its weak points: the lower-tier calibrator preference changes current policy (SKILL.md:1181 confirms the rule picks the highest capability), the two-class quorum tightens the N=2 floor, and the exact key under-merges. Remaining weakness: no concrete template, no merge interface design, a 96-run measurement with no T1 arm, and a manifest state machine with no build cost. Its anchor-replacement rule is the right answer to X-002, so I credit it.

**Convergence.** All three advocates now agree on the pre debate staying until measured, a T1 arm, embedded calibration, replacing the anchor before resolution, V3's units, a byte-identical spec-panel test and a hard consumer grep. The open split is which skeleton to build on and how loose the dedupe key is. My view: V1's skeleton and template, V3's failure model and finalizer policy, and V2's measurement design and stop rule.

## New evidence

1. **Resolution exclusion is narrow today.** `panel.py:479` builds the exclude list only from models already chosen in earlier slots, and only when `distinct_across_slots` is true. Nothing in it carries an executor class. `panel.py:402-408` shows fixed returns `candidates[0]` and the two other strategies fall back to the full list when the pool empties. So executor-class exclusion is a net-new input to resolution in every variant. None of them can say it "reuses" the panel for it.
2. **The calibrator is a rule, not a slot.** SKILL.md:1176-1185 (read) defines the calibrator by set subtraction and a capability preference, with `calibrator_diversity` as telemetry. That is why the `cal`-slot design fails twice: the validator forbids it and the policy does not describe it as a slot. A repaired V2 reuses the rule unchanged.
3. **SKILL.md:1190 is a SHOULD with degrade-and-report.** This is the governing text for X-002 and C-017. It rules out V1's original raise and also rules out any design that refuses to run on a class collision.
4. **The headless builder is post-only, and the zero is a constant.** `ensemble.py:797` sets `"mode": "post"`. `ensemble.py:817-818` sets `citations_dropped` and `citations_dropped_extrapolated` to the literal 0, and `ensemble.py:808, 814, 816` sets the verification fields to False. So the headless gap in C-022 is a fixed value, not a measured one. V3's rule "never copy the constant 0" has no mechanism, and V1's stage 5 pre-check has one.
5. **SKILL.md:1192 fixes the calibration transport.** Cards go to Wave 4 "with calibrated scores attached". That is the ground truth against which X-008 and X-009 are decided: a design that moves calibration to a sidecar must also say how the debate reads it. V3's "materialize a calibrated view" is the one that satisfies both lines.
6. **Revised V2 first-measurement gate (a proposal, not a recorded result).** Run three arms: T1, current T2 and panel-fed T2. Take V1's shared-card pairing inside the two T2 arms, V1's scripted seeded defects for ground truth, V2's union ledger for natural findings, and V3's arm-hiding and repeat hygiene. Keep the stop rule: a T2 recall gain under 15 points over T1 shrinks T2 to two reviewers instead of migrating. No cost figure is claimed for the run until the lanes are measured in one unit.

## Final shared assumption responses

Only the promoted assumptions where responses differed across advocates in R1 or R2 are listed. A-003, A-005 and A-008 are close to unanimous (A-008 QUALIFY in every statement), so they stay as stated in my R1.

- **A-001: QUALIFY** (changed from REJECT). Pre T2 may add recall over T1, but nothing recorded shows it, since six runs show agreement and not defect recall. The T1 arm is a hard entry criterion for any pre change beyond resolution-only adoption. REJECT overstated it, and V1 and V3 reasoned with QUALIFY.
- **A-002: QUALIFY.** Haiku stand-in runs show mechanics, cost and compliance in anthropic-only. A gateway default needs its own run, and no variant plans one. V3's REJECT is acceptable for quality claims. My QUALIFY holds because the stand-ins still test the mechanics.
- **A-004: REJECT** (changed from ACCEPT-as-risk). The card carries five dimension scores, per-finding reasons and notes, so a findings-only reduction loses them. SKILL.md:1192 passes calibrated cards on. Embedded calibration stays authoritative.
- **A-006: REJECT.** SKILL.md:1180 lists classes (kimi, deepseek) that the gateway tier lists do not carry (as cited by diff-analysis A-006). An explicit per-model class map and an actual-identity check are both preconditions for exclusion and for the disjoint rule.
- **A-009: REJECT** (changed from ACCEPT-as-risk). The documented consumer map did not name the "1.0" headless post constant, so completeness is disproven. A repo-wide grep for `merge_method`, `contract_version` and convergence readers is a hard stage entry gate, as V1 says.
- **A-010: REJECT** (changed from QUALIFY). A quote mismatch from a paraphrase does not prove an unfounded citation. The pre-check may drop only a missing file or an out-of-range line. The rest is flagged for the validator.
- **A-012: QUALIFY.** Seeded defects give known ground truth but not natural defects. Pair them with a union ledger of natural findings and blinded grading.
- **A-014: QUALIFY** (changed from ACCEPT). Non-interference is a property to test. New flags default off, and a byte-identical v1 merge test is the acceptance criterion for every variant.

## Per-point positions

| Point | Winner | Changed from R1? | Reason |
|---|---|---|---|
| S-001 | NONE | No | Same order in all three. |
| S-002 | V1 | No | Five candidates with verdicts plus a matrix show the staging most clearly. |
| S-003 | V2 | No | Path abbreviation and PROPOSED/UNVERIFIED markers keep citations auditable; V3 copied a timestamp. |
| S-004 | NONE | No | Heading style only. |
| S-005 | V3 | No | Answering Q5 and Q7 in place saves a lookup. |
| S-006 | V1 | No | The "v1?" and "Set by" columns show field ownership. |
| S-007 | V1 | No | Concrete commands and a shadow paragraph make the sketch executable. |
| S-008 | V3 | No | Only V3 designs state, idempotency and resume; graft it on. |
| S-009 | V1 | No | "What ships" plus entry, exit and rollback per stage. |
| S-010 | V1 | No | Versioning plan and consumer-by-consumer change list. |
| S-011 | V3 | No | Keeps output, retrieval and turn-budget units apart. |
| S-012 | V1 | No | Separate assumptions, UNVERIFIED and PROPOSED-name inventory. |
| C-001 | V1 | Yes | V1's set of five includes dispatcher-only and debate-always as named rungs and rollbacks; V2's four plus C2 is a subset in effect. |
| C-002 | V1 | Yes | V1 R2 adopted the stage gate, keeps the debate and adds a T1 arm; with that convergence, V1's layered skeleton and template is the only one that runs as written. |
| C-003 | V1 | No | Most complete takes, lacks and stays map. |
| C-004 | V1 | No | Superset with typed citations keeps one parser; add V3's completion state and channel as optional fields. |
| C-005 | V1 | No | With the primary-citation fix it equals v1 on the reviewed file and clusters paraphrases; V3's exact key under-merges and my span overlap shares the cross-task risk. |
| C-006 | V2 | No | Keep the pre debate until a T1-armed measurement; V1 R2 and V3 now agree. |
| C-007 | NONE | Yes | All three keep the post debate with cluster pre-processing, so the differences are not decision-relevant. |
| C-008 | V2 | No | The `launch` null or non-null rule fits the tool's model enum; add V3's pin-before-freeze rule. |
| C-009 | V1 | No | Only concrete template that passes `panel.py:140-141`. |
| C-010 | V1 | No | Most executable pre flow; add V3's input-drift recheck. |
| C-011 | V3 | No | Retries are attempts, and automatic clearing is off. |
| C-012 | V3 | No | Correct units and tied to the hard kill. |
| C-013 | V2 | No | Numeric 15-point gate before a larger panel. |
| C-014 | V1 | No | Seven stages with shadow, byte-identity exit and rollback. |
| C-015 | V3 | No | No contract change for the first pre shipment. |
| C-016 | V3 | No | A real child score keeps gate 9 meaning. |
| C-017 | V3 | Yes | Replace the ineligible anchor before resolution; SKILL.md:1190 requires degrade and report, not raise. |
| C-018 | V1 | Yes | Opus as calibrator is what SKILL.md:1181 already selects from the disjoint set; calibration stays embedded. Needs the U-012 ablation. |
| C-019 | V1 | No | Deterministic pre-check before the validator, dropping only missing files and out-of-range lines. |
| C-020 | V2 | No | Only V2 has a T1 arm and a stop rule; V1's shared cards go inside it. |
| C-021 | V3 | No | Resolves a disjoint judge and records collisions. |
| C-022 | V1 | No | A concrete mechanism for the verified constant 0 (`ensemble.py:817`). |
| C-023 | V1 | Yes | Both V1 and V3 keep documents separate and need a new multi-input merge; V1 is the concrete one (role-qualified citations). |
| C-024 | V3 | No | Five completion states. |
| C-025 | NONE | No | Names only. |
| X-001 | V1 | No | V1's template has one fixed slot; mine failed `panel.py:140-141`. |
| X-002 | V3 | Yes | Anchor replacement before resolution, consistent with SKILL.md:1190; all three had incompatible behaviours as written. |
| X-003 | NONE | No | All three misread the version; the "1.0" builder is post-only (`ensemble.py:797`). |
| X-004 | V1 | No | A widened legal set is a major change. |
| X-005 | V3 | No | Keeps the adversarial merge, so the no-own-merge rule holds. |
| X-006 | V2 | No | Agreement is not recall; keep until measured. |
| X-007 | V3 | No | Single `--doc` plus identity loss rules out concatenation as an identity store. |
| X-008 | V3 | Yes | Embedded calibration is today's fact; V3's calibrated view keeps it. V1 withdrew its sidecar to an index. |
| X-009 | V3 | No | SKILL.md:1192 passes calibrated cards on; V3's design satisfies it. |
| X-010 | NONE | No | The model enum rejects gateway aliases; my launch rule only defers gateway dispatch to a swarm path that is not shown for reflect pre. |
| X-011 | V2 | No | The recorded pre card shows pre use exists; the agent text is post-only. |
| X-012 | V3 | No | Turn-budget figures are not output tokens. |
| X-013 | V3 | No | Computes the 65.6k hard kill. |
| X-014 | NONE | No | A minor text gap in V3 between target and allowance. |
| X-015 | V3 | Yes | V2's two nets contradict; V3's arithmetic reconciles. |
| X-016 | V1 | Yes | Opus calibrator follows SKILL.md:1181; "sparingly" is unquantified, so require the ablation. |
| X-017 | V3 | Yes | No misleading ESCALATE written to the ledger; V1 conceded and adopted it. |
| X-018 | V2 | Yes | V1 itself agrees V2's ledger cites are the correct ones and its own are wrong (as cited by V1 R1, R2). |
| X-019 | V1 | No | 405 and 408 are right (grep). |
| X-020 | V2 | No | Names the Fable entry and a resolve-time filter. |
| A-001 | V2 | No | Only V2 states and tests the assumption. |
| A-002 | NONE | No | No variant plans a gateway run. |
| A-003 | NONE | No | All three still carry a quote field with no lossless conversion of line-only evidence. |
| A-004 | V3 | No | Keeps the full calibration record on the card. |
| A-005 | V3 | No | Keeps units separate. |
| A-006 | V1 | Yes | The explicit per-model class map is the concrete precondition fix. |
| A-008 | NONE | No | The only post datapoint is an unread snippet. |
| A-009 | V1 | Yes | Only V1 makes the consumer grep a hard entry gate; the missed "1.0" builder shows why. |
| A-010 | V3 | No | Adds no automatic quote-based drop. |
| A-012 | V2 | Yes | Seeded defects paired with a union ledger of natural findings; V1 R2 and V3 R1 both ask for that pairing. |
| A-014 | V1 | No | Only V1 states a byte-identical spec-panel test. |

Tally: V1 25, V2 11, V3 22, NONE 10. Changed from Round 1: 15 (C-001, C-002, C-007, C-017, C-018, C-023, X-002, X-008, X-015, X-016, X-017, X-018, A-006, A-009, A-012).

## Remaining disagreements

- **C-002, C-001:** V3 still votes V3 on C-002, and a split between V1's skeleton and V3's policy is open. I hold V1's template and layers as the base, with V3's policy, failure model and finalizer grafted on.
- **C-005:** V3 favours the exact key. Under the debate-kept design an under-merge is cheap, but only V1's primary-citation rule clusters paraphrases without a cross-task merge.
- **C-018, X-016:** V3 reads "sparingly" as a reason to prefer a lower-tier calibrator. I side with V1 on the policy text (SKILL.md:1181), so V3's reading is a policy change. I do not call the Opus use justified until the ablation runs.
- **C-022:** V3 votes V3 for "validate before reporting". It gives a rule and no mechanism for the verified constant 0.
- **C-023:** V3 votes V3. V1 and V3 are the same idea; V1 is the concrete one.
- **X-001:** V3 votes V3 because it keeps calibration outside the slots. V3 has no template to check, and V1 does.
- **X-007:** V1 votes V1. Both reject concatenation; the contradiction row is V2 against V3's side, which is why I vote V3.
- **X-008, X-009, X-017:** V1 votes V3 after withdrawing its sidecar, so these are now agreed with V1. V3 votes NONE on X-008, because it wants the migration labelled as a change.
- **X-010:** V1 votes V2 and V3 votes V3. I vote NONE: my rule defers gateway dispatch and does not resolve it.
- **X-018:** V3 votes V3 on preserving members. I vote V2 on cite accuracy only.
- **A-006:** V3 votes V3 (distinct namespaces, actual identity). I vote V1 because the class map is the concrete artifact.
- **A-009:** V3 votes V3 for "re-check before implementation". I vote V1 for a hard gate.
- **A-012:** V1 votes V2 and V3 votes V3. V3 holds that varied authored cases are enough. I keep the union ledger of natural findings as the stronger pairing.
- **C-007:** V1 votes V1 and V3 votes V3. I vote NONE because all three keep the post debate and the remaining differences do not change the decision.
