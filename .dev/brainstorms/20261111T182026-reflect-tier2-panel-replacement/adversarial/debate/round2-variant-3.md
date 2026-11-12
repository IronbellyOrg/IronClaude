# Round 2 — Variant 3, backend advocate

## Responses to criticisms

Source citations below identify inspected checkout files relative to `src/superclaude/`; they are evidence, not installed lookup instructions. Debate references identify the supplied statements. New interfaces remain PROPOSED. No experiment was run. Fable and Tier 0 remain forbidden, including fallbacks, calibration and judging; Opus requires an explicit independent-calibration or adjudication justification.

1. **“The exact key barely dedupes” (V1 R1/R2; V2 R1/R2, C-005).** Concede under-merging, not the proposed cure. Exact identity is for lossless storage; V3 separately proposes related groups and adjudicated issue IDs (V3, Finding format). The finalizer still matches paraphrases, so no debate-token saving is established. V1's primary-citation repair removes its shared-spec mistake but does not prove distinct defects cannot merge. Nearby locations are evidence of relatedness, not identity; see new evidence 2. Keep members separate until adjudication and count adjudicated issues once.

2. **“A new envelope needs a second parser; V1's superset is simpler” (V1 R1/R2, C-004).** Concede the adapter and engineering cost. Keeping the legacy parser unchanged plus normalizing its parsed records does not require a second markdown parser, but V3 has not specified the conversion sufficiently to call it lossless, especially for line-only citations. Award the finding-core specification to V1. Retain submission-level completion, coverage observations and calibration provenance around that core; optional finding fields alone cannot establish whether an entire assignment finished.

3. **“No concrete template, commands or multi-input merge interface” (both advocates, S-007/C-009/C-023/X-001).** Conceded. V3 names the required boundaries but leaves executable interfaces undesigned. Adopt V1's one-fixed-anchor template shape, separate calibration selection and role-qualified input design. Those remain proposals, not verified available options. V1's normal template also needs V3's eligible-anchor replacement and fallback-policy checks. Installed instructions must use installed/project lookup surfaces, never checkout-only source paths.

4. **“This becomes a platform with uncosted machinery” (both advocates).** Concede missing implementation-effort estimates. V3 explicitly excludes a scheduler, daemon, database and automatic revision engine (V3, Risks); its intended addition is bounded state in the existing output directory. Neither V1's four layers nor V3's envelope has an engineering estimate. Keep only snapshot identity, attempt replacement, completion and committed-result visibility needed by this migration; assess implementation effort before approval. These requirements do not establish a multi-file transaction: legacy readers need an explicit readiness bridge and crash-point tests before publication can be called atomic.

5. **“The 96-run study is expensive, has no T1 arm, and leaves debate usefulness untested” (both advocates).** Fully concede the first-measurement design weakness. Adopt V2's T1 control and natural-case ledger, V1's scripted seeds, and V3's blinded grading/repeats. Start with an approved small exploratory sample, not an automatic 4.824M-token spend. Shared-card comparisons isolate finalizer effects; end-to-end legacy/shared comparisons require independently generated outputs to detect changed prompts or dispatch. Do not reuse identical cards and then claim to have tested the entire infrastructure. Debate removal remains a separately identified ablation. V2's 15-point rule is proposed, not empirically calibrated.

6. **“The version is wrong” (both advocates, X-003).** Conceded. The universal unchanged-1.8.0 table was false; preserve existing engine-specific serialization initially. The inspected builder emits post mode and references its own version constant (`cli/reflect/ensemble.py:788,797`); the reported literal `1.0` is established by the supplied diff analysis, not re-read here. The post-only scope narrows the error but is not permission to promise pre/headless parity. No new merge meaning is needed for initial pre adoption.

7. **“Pre reviewer support already exists” (both advocates, X-011).** Concede the overly broad wording. The supplied recorded-card evidence demonstrates pre use; V3's actual remaining proposal is formalizing pre brief/schema support in the restricted definition. I did not re-read that card this round and claim no new run evidence. V2 deserves credit for the correction.

8. **“There is no deterministic check, so headless citation-drop accounting has no mechanism” (V1 R1/R2; V2 R2, C-022).** Concede that V3 specifies a final validator outcome but not its headless invocation/serialization implementation. Neither proposal closes the whole gap as written: V1's location precheck cannot detect a located citation that fails semantic support. A post migration must execute the evidence gate, serialize its actual drops and run drift verification, with unavailable validation remaining visibly partial. Until that exists, keep headless migration gated; do not replace literal zero with an invented measurement.

9. **“Gateway dispatch is unresolved” (V2 R1/R2, X-010).** Concede. V3 does propose immutable swarm binding, so it did not ignore swarm, but its transport-factory mapping is explicitly UNVERIFIED. V2's null/non-null `launch` routing is useful; V2 R2 correctly concedes that routing to an unspecified pre swarm adapter is not proof it works. Award no complete implementation here. Apply overrides before freeze, verify restricted transport behavior, and require actual-identity conformance.

10. **“Lower-tier-first calibration changes policy; two-class quorum tightens the floor” (both advocates).** Conceded, as in R1. The rule selects the highest-capability disjoint calibrator, with a degraded fallback when none exists (`skills/sc-reflect-protocol/SKILL.md:1178-1185`). Preserve it initially; independent calibration is a concrete justification for Opus when it is the applicable choice, not permission for routine Opus reviewers. Do not claim measured cost reduction from moving its role. Preserve N=2 as the hard count floor rather than introducing an additional distinct-class floor (`SKILL.md:600,610`).

11. **“SHOULD/degraded telemetry rules out refusing executor collisions” (V1 R2 new evidence 4; V2 R2 new evidence 3).** Reject that generalization. The same inspected policy separately says executor exclusion **MUST** hold when identity is resolved, removes that class and falls to T1 below N=2 (`SKILL.md:600,610`). The three-way SHOULD explicitly refers back to this enforcement and retains the grader assertion (`SKILL.md:1190`). Unknown executor is fail-open (`SKILL.md:602`); a known executor collision is not licensed by generic diversity degradation. Replace the anchor, seek eligible replacements, then degrade to N=2/T1 as specified. Do not dispatch a known excluded reviewer merely to keep T2 alive.

12. **“37–53k versus 37–56k is inconsistent” (X-014).** Concede confusing headline labeling. V3 explains target versus allowance in its cost section, but the candidate table should use the broader planning band consistently. Neither range is measured. Also reject the other rebuttals' new phrase that 65.6k is a ceiling for “any lane budget”: the calculation is in profile Claude-token units, not a conversion into output-only lane limits. The central unit distinction must survive adoption.

## Updated assessment of other variants

**V1, steelman first.** Its strongest contribution is a usable implementation skeleton: explicit layer ownership, one-fixed-slot template, typed multi-file finding core, compatibility fixtures and staged rollback. Its R2 retains the real debate, fixes calibration transport, accepts pre-freeze overrides and replaces the ineligible anchor. Those are substantial corrections; the initial objection that it inevitably ships premature debate removal no longer describes its revised position.

Award V1 more implementation-detail points, including the template and role-qualified multi-input design. Do not award proximity matching the status of proven semantic identity. Its pre-merge validator also cannot validate claims newly introduced by later synthesis, so V3's final gate remains necessary. Its claim that three-way degradation permits known executor collisions misreads the more specific MUST. “One merge” now means shared mechanics plus an adversarial authority, not elimination of interpretive adjudication.

**V2, steelman first.** Its strongest contribution remains asking whether T2 is worth using at all. R2 now repairs the calibrator slot, synthetic-document identity, override precedence and version classification; it also adopts honest failure handling. Its final measurement synthesis is the best starting experiment, provided shared-card pairing is not mistaken for an end-to-end substitution test.

V2 now offers a sensible gate rather than a competing complete architecture. Its numeric stop rule needs calibration and owner approval, and failure to beat T1 by a proposed margin does not itself prove two reviewers are adequate. Its gateway-dispatch concession is more accurate than declaring the launch rule a complete solution. Both other advocates now support V3's first-shipment policy; V1 supplies stronger schema/interface detail, not a reason to weaken those invariants.

## New evidence

1. **Known and unknown executors have different failure rules.** The specific MUST/removal/N=2 rule and separate unknown-identity fail-open rule appear together (`skills/sc-reflect-protocol/SKILL.md:600-610`). This distinction was absent from the earlier rebuttals' SHOULD-based argument. It prevents a false consensus that any collision can merely be reported and dispatched.

2. **Primary-only matching still has a chain-merging counterexample.** The actual cluster algorithm unions every pair accepted by `same_defect` (`cli/review/findings.py:393-398`). The matcher accepts intersecting refs and spans within three lines (`findings.py:373-378`). Consider three different claims with intersecting refs, distinct fingerprints and single-line primary spans at 10, 13 and 16: A matches B, B matches C, A does not match C, yet all enter one cluster. This is a deductive example from inspected code, not an executed test. V1's primary-only repair does not remove this transitive bridge. Grouping is acceptable if it preserves every member; automatic issue collapse is not justified.

3. **Headless input-drift telemetry is another literal default.** Beyond the already discussed citation zeros, the same builder sets `input_drift_detected: False` (`cli/reflect/ensemble.py:817-819`). That is a serialization fact, not proof that no caller checks drift. It means a new shared path must connect an observed drift result before claiming parity; fixing citation accounting alone cannot establish it. The verification skip reason is explicitly `no-verification-stage` (`ensemble.py:808-809`), so reviewers remaining read-only and coordinator-owned verification are compatible requirements.

## Final shared assumption responses

These cover every promoted assumption, including those with differing labels or reasons so far.

- **A-001 — QUALIFY.** T2's incremental value remains unmeasured; include T1 before expanding migration or reviewer count.
- **A-002 — REJECT.** Stand-in equivalence to gateway quality is unsupported. Mechanics can be tested locally, but require a separate gateway validation before transferring quality claims.
- **A-003 — REJECT.** Line-only recorded evidence has no established lossless short-quote conversion. Permit validated ranges without invented quotes.
- **A-004 — REJECT.** A findings-only reduction loses dimensions, reasons and notes. Preserve full calibrated cards and provenance.
- **A-005 — REJECT.** Turn-budget, provider output, retrieval and artifact-size figures are not interchangeable.
- **A-006 — REJECT** (from R1 QUALIFY). The stated straightforward mapping is false. Require V1's explicit class registry plus actual-identity/fallback checks; classes, tiers and transport slots remain distinct.
- **A-008 — QUALIFY.** Keep post debate for current safety/compatibility; deterministic classification is not proved impossible, nor its replacement validated.
- **A-009 — REJECT.** Consumer completeness is not established. Adopt V1's hard inventory gate; inspect runtime/tests, not only the documented map.
- **A-010 — REJECT.** Location failure is not universally semantic invalidity; location success is not claim support. Prechecks annotate, final validation decides support.
- **A-012 — QUALIFY.** Scripted/authored defects need independently graded natural cases. V3 already includes real plans and warns against generalization; V2's union ledger strengthens that, rather than correcting a claim that authored cases alone suffice.
- **A-014 — QUALIFY.** Non-interference must be demonstrated. Adopt V1's byte-identical legacy fixtures, with new paths dormant by default.

## Per-point positions

Votes judge the stated point, crediting explicit repairs. A winner does not certify implementation. All 68 requested points are included; unique U rows and unpromoted A rows are outside the requested ballot.

| Point | Winner | Changed from R1? | Reason |
|---|---|---|---|
| S-001 | NONE | Yes | Shared ordering; sentence styling is not decisive. |
| S-002 | V1 | No | Candidate blocks and matrix expose alternatives. |
| S-003 | V2 | No | Clearest provenance/uncertainty convention. |
| S-004 | NONE | Yes | Heading punctuation is not a design advantage. |
| S-005 | V3 | No | Answers are available in place. |
| S-006 | V1 | No | Field ownership table specifies trust boundaries. |
| S-007 | V1 | Yes | More concrete adapter interfaces; state credited separately. |
| S-008 | V3 | No | Completion, retry and resume obligations are explicit. |
| S-009 | V1 | No | Explicit shipped scope and rollback. |
| S-010 | V1 | Yes | Strongest consumer-level mapping. |
| S-011 | V3 | No | Separates estimates and incompatible units. |
| S-012 | V1 | No | Proposed-name inventory prevents invented APIs. |
| C-001 | V1 | No | Widest useful separation of adoption choices. |
| C-002 | V3 | No | Share mechanics without changing verdict authority. |
| C-003 | V3 | No | Includes execution identity and incomplete outcomes. |
| C-004 | V1 | Yes | Better specified finding core; retain V3 submission metadata. |
| C-005 | V3 | No | Exact storage plus related groups avoids destructive collapse. |
| C-006 | V2 | Yes | Explicit measurement gate before debate removal. |
| C-007 | NONE | Yes | Revised variants all retain post adjudication. |
| C-008 | V3 | No | Immutable identity must govern both transports. |
| C-009 | V1 | Yes | Concrete legal template beats V3's abstract slots. |
| C-010 | V3 | No | Final validation, drift and readiness complete the flow. |
| C-011 | V3 | No | Attempts cannot add votes or clear findings. |
| C-012 | V3 | No | Honest units; hypothetical savings remain hypothetical. |
| C-013 | V3 | No | Preserve rubric; no unsupported automatic panel expansion. |
| C-014 | V2 | No | Resolution-only first minimizes initial mutation. |
| C-015 | V3 | Yes | Corrected engine-specific preservation needs no initial new meaning. |
| C-016 | V3 | No | Genuine child score preserves convergence semantics. |
| C-017 | V3 | No | Anchor replacement and all-fallback identity enforcement. |
| C-018 | V1 | Yes | Repaired calibration transport preserves current selection policy. |
| C-019 | V3 | No | Final gate checks synthesized claims, not just inputs. |
| C-020 | V2 | No | T1 control and explicit stop question. |
| C-021 | V3 | No | Actual judge identity and collision accounting. |
| C-022 | NONE | Yes | Neither proposal fully specifies headless semantic-gate integration. |
| C-023 | V1 | Yes | More concrete role-qualified multi-input proposal. |
| C-024 | V3 | No | Complete-empty differs from failed/truncated output. |
| C-025 | NONE | No | Names do not establish behavior. |
| X-001 | V1 | Yes | Concrete one-fixed-slot repair; calibration outside template. |
| X-002 | V3 | No | Replace anchor; preserve known-executor exclusion and N=2 floor. |
| X-003 | NONE | No | Original universal-version claims were wrong. |
| X-004 | V1 | No | Semantic enum/gate changes require major migration. |
| X-005 | V3 | No | Real adversarial finalization avoids own-merge violation. |
| X-006 | V2 | Yes | Keep until measured; agreement is not recall. |
| X-007 | V3 | No | Original contradiction correctly rejects synthetic identity. |
| X-008 | V3 | Yes | Repaired calibrated view preserves embedded record. |
| X-009 | V3 | No | Full calibration reaches finalizer inputs. |
| X-010 | NONE | Yes | Routing intent does not prove pre gateway dispatch works. |
| X-011 | V2 | Yes | Recorded pre use rebuts V3's broad wording. |
| X-012 | V3 | No | Turn budget is not measured output-only usage. |
| X-013 | V3 | No | Correct arithmetic without converting units. |
| X-014 | V3 | No | Target/allowance distinction exists; headline needs tightening. |
| X-015 | V3 | No | Reconciled planning arithmetic versus withdrawn inconsistent nets. |
| X-016 | V1 | Yes | Current independent-calibrator policy justifies conditional Opus. |
| X-017 | V3 | No | Revision decision must not become reflect authority. |
| X-018 | V2 | Yes | Citation-accuracy point, not member-preservation point. |
| X-019 | V1 | No | Correct fallback locations established by supplied analysis. |
| X-020 | V2 | No | Explicit forbidden-alias filter. |
| A-001 | V2 | No | T1 comparison tests the foundational premise. |
| A-002 | NONE | Yes | No complete gateway transfer study proposed. |
| A-003 | NONE | No | Lossless line-only conversion remains undesigned. |
| A-004 | V3 | No | Preserve full cards and calibration provenance. |
| A-005 | V3 | No | Separate measurement bases. |
| A-006 | V1 | Yes | Explicit registry is the concrete missing precondition. |
| A-008 | V3 | No | Separate post replacement trial, not impossibility claim. |
| A-009 | V1 | Yes | Hard consumer-inventory gate beats informal recheck. |
| A-010 | V3 | No | No automatic quote-mismatch rejection layer. |
| A-012 | V2 | Yes | Controlled seeds plus natural-case union ledger. |
| A-014 | V1 | No | Explicit byte-identical legacy compatibility tests. |

Tally: V1 18, V2 10, V3 31, NONE 9. Changed from Round 1: 23.

## Remaining disagreements

- **C-002/C-003/C-010:** V1's useful skeleton does not supersede V3's verdict, completion and final-publication policy. Prefer that policy as the base, importing V1's interfaces.
- **C-005:** Both advocates prefer primary proximity matching; transitive bridges still preclude treating clusters as single issues without adjudication.
- **C-008/X-010:** V1 credits V2's routing as a solution. Immutable binding is the stronger design property; actual pre gateway conformance remains unproved.
- **C-013:** A proposed 15-point threshold does not establish a universal reviewer-count policy; preserve the existing rubric pending study.
- **C-014:** Resolution-only adoption is smaller than building every kernel layer before shadowing, despite V1's stronger compatibility fixtures.
- **C-019/C-022:** A pre-merge location check does not validate post-synthesis semantics or fully close headless accounting; neither design supplies the complete latter implementation.
- **C-007/A-008:** Revised post-debate retention is substantively shared, but replacement still needs a post-specific study; the lone unread datapoint is not enough to rank its necessity.
- **X-002/C-017 policy rationale:** Winner labels now agree, but their SHOULD-based permission for known executor collisions conflicts with the specific MUST and grader assertion.
- **X-007/C-023:** V3 wins the original identity objection; V1 wins concrete interface detail. These are different ballot questions.
- **X-014:** A labeling defect deserves correction, not erasure of an explicitly explained target/allowance distinction.
- **A-002/A-010:** Transfer and automatic rejection remain unsupported even when mechanics work. I retain REJECT for the assumptions as stated, not rejection of useful local tests or advisory checks.

No implementation, tests or paid model runs were authorized or performed; remaining interfaces and publication guarantees require implementation-time verification.
