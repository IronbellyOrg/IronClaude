## Position summary

Variant 3 is the strongest initial migration because it shares review infrastructure without replacing the meaning of a successful audit: real adversarial finalization remains authoritative, incomplete work cannot become a clean result, and retries cannot add votes. Adopt V2's T1 comparison and V1's explicit compatibility tests, but correct V3's headless-version claim and calibration-policy mismatch before implementation.

Evidence conventions: package-source citations below are relative to `src/superclaude/`; they describe inspected source, not paths proposed for installed primitives. V1/V2/V3 references name sections of the three supplied variant documents. `CARD` denotes the inspected `.dev/research/346-review-loop-experiments/exp346/.dev/experiments/346-validation/phase5/final-bundle/builds/stoprule/brainstorm/workflow-report/nested/reflect-1/reviewer-cards/reviewer-1-card.yaml`. New mechanisms remain proposals. Fable and Tier 0 are forbidden throughout primary selection, fallback, calibration and judging; Opus needs an explicit independence or adjudication justification.

## Steelman

### Variant 1

Its strongest argument is that infrastructure sharing should eventually remove duplicate merge machinery, not merely replace a rotation table. Its four-layer boundary is clear, its proposed major-version migration honestly recognizes semantic changes, and its shared-card experiment isolates merge effects efficiently (V1, “Chosen architecture,” “Return-contract 1.8.0 mapping,” “First measurement”). Its explicit byte-identical legacy merge test is better specified than V3's general compatibility promise. The weakness is not ambition itself: the evidence does not yet justify choosing debate removal as the target default.

### Variant 2

Its strongest argument is that even T2's benefit over T1 is unknown, so the first experiment must test that premise rather than merely compare two expensive T2 implementations (V2, “First measurement”). Resolution-only adoption is an appropriately small first step, and retaining debate avoids pretending that clustering can settle interpretive disputes. Its proposed calibrator slot, however, does not fit the resolver's actual contract, and its later “additive 1.9.0” migration changes existing semantics.

## Strengths claimed

1. **Preserve the public meaning before optimizing it.** The legal merge enum is explicitly exact, and inline synthesis is forbidden outside corroborated fallback (`skills/sc-reflect-protocol/SKILL.md:784-789`). V3 retains a real finalizer rather than substituting overlap for convergence. This also preserves the genuine-verdict requirement of promotion condition 9 (`SKILL.md:1483`). V1 plans a legitimate future major change; V3 avoids needing that change initially.

2. **Make failure a first-class result.** Existing merge logic refuses an all-invalid round but permits parsable findings from invalid blocks (`cli/review/ledger.py:107-157`). That is useful behavior, not proof that transport success means completed coverage. V3's completion states and independent coverage observations distinguish a completed clean review from an empty, truncated or malformed response (V3, “Finding format”). Only complete, valid submissions count toward quorum; incomplete submissions remain diagnostic evidence, not clearing votes.

3. **Bind identity to the execution, including retries.** The current resolver records configuration hashes and launch aliases, but its exclusion list is only previously chosen model IDs; fixed selection ignores it, random/round-robin may fall back to excluded candidates, and fallback lists remain available (`cli/review/panel.py:393-418,479-524`). V3 applies hard policy to primary and fallback candidates, records actual identity, and binds the launch to one resolution. A retry supersedes an attempt rather than becoming another independent reviewer (V3, “Operational execution contract”).

4. **Protect artifact integrity across interruption.** Ledger save uses a same-directory temporary file, fsync and replacement (`cli/review/ledger.py:52-67`), but the merge command writes its report before saving the ledger (`cli/review/merge_cmd.py:113-118`). V3 correctly proposes a committed artifact-set boundary and dependency-hash resume rules instead of calling that pair transactional. Existing readers still need an explicit compatibility bridge, as conceded below.

5. **Prefer visible duplicates to hidden defects.** Current matching can equate findings using section/ref fingerprints or nearby spans; clustering then takes transitive closure (`cli/review/findings.py:367-407`). Ledger rows retain the first claim and category while combining blocking and maximum severity (`cli/review/ledger.py:181-203`). V3 separates exact identity from suggested relationships, preserves all source members and leaves semantic combination to adjudication. Its typed input identities also avoid treating equal quotes from different files as interchangeable.

6. **Keep advisory correctness separate from deviation gates.** The restricted reviewer explicitly forbids treating no-spec correctness gaps as Regression or allowing them to force partial status (`agents/reflect-reviewer.md:30`). V3's channel field preserves that rule through normalization and storage rather than relying on a lossy category mapping.

7. **Use honest accounting.** The cost profile states “claude tokens” and a turn-budget estimate, not measured output-only usage (`skills/sc-reflect-protocol/refs/cost-profile.yaml:46-56`). V3 separates planning estimates, retrieval, provider usage and artifact size. Its pilot names uncertainty and refuses to trade a safety failure for savings (V3, “Cost model,” “First measurement”). V2 nevertheless asks the better first question by including T1.

## Weaknesses identified in other variants

1. **V1 removes semantic adjudication before demonstrating that it is dispensable.** Its strongest case is that high convergence and advisory pre-execution output make the debate an expensive candidate for removal. But agreement does not establish defect recall; even the current deterministic ledger combines blocking claims rather than adjudicating them (`cli/review/ledger.py:187-199`). V3 keeps the debate during infrastructure substitution. A later shared-card ablation can test removal without confounding it with dispatch changes.

2. **V2's calibrator-in-panel design violates two existing boundaries.** Its best idea is mechanically enforced calibrator independence. However, the template validator permits exactly one fixed slot (`cli/review/panel.py:129-141`), and every resolved slot becomes a reviewer entry (`panel.py:498-512`). Adding a second fixed `cal` slot is neither accepted configuration nor a separate calibrator role. Resolve calibration separately; do not count it in reviewer quorum.

3. **V2's environment override creates a second identity authority.** Preserving old `T2ModelNN` overrides is a reasonable compatibility aim (V2, Q4). Letting them override an already recorded resolution nevertheless makes hashes and exclusions describe a different selection from the dispatched one. V3 is better: include explicit transport overrides before freezing the resolution, or reject the mismatch. Legacy routing can preserve old precedence without introducing hidden reselection in shared runs.

4. **V2 calls a semantic migration additive.** Its strongest case is that field names survive. Yet changing the merge enum and promotion's genuine-adversarial-result condition changes existing semantics, not just shape (`skills/sc-reflect-protocol/SKILL.md:789,952-953,1483`). V1's major-version classification is correct; V3 needs no such change for its initial path.

5. **V1's calibration transport is incomplete; V2 misdescribes current storage.** Keeping immutable raw reviewer output is sound. But current policy passes calibrated scores attached to cards (`SKILL.md:1192`), while V1's post adapter compares cards without specifying how its new sidecar reaches that input. V2 says its sidecar exists “as it does now,” although CARD's calibration is embedded at lines 82-103. Preserve raw bytes and materialize a calibrated view carrying the complete calibration record; sidecar placement alone is not compatibility.

6. **Neither single-document reuse nor proximity proves safe multi-file identity.** V2's bundle minimizes parser changes, which is its real advantage. The existing annotator, however, chooses the first occurrence while merely flagging ambiguity (`cli/review/findings.py:346-356`); concatenation does not fix that. V1 improves identity with file/role metadata but can still combine distinct tasks through a common requirement citation. Keep original input identities and source ranges authoritative; any bundle must be a mapped view, not the identity store.

7. **Mechanical prechecks cannot justify an unconditional stronger-grounding claim.** V1/V2 correctly retain the semantic validator. Nevertheless, a missing exact quote may mean format drift or paraphrase, not a false underlying claim; a located quote does not prove support. The inspected locator flattens whitespace (`cli/review/findings.py:276-304`), so ordinary wrapping alone is not a failure example. Mechanical checks should annotate schema/location errors and trigger repair or explicit incompleteness, not automatically equate all failures with semantically unfounded findings.

## Concessions

- **X-003 is a real V3 error.** The headless constant is `"1.0"`, used by its contract builder (`cli/reflect/ensemble.py:74,787-797`), whereas the skill documents v1.8.0 (`skills/sc-reflect-protocol/SKILL.md:847`). “Unchanged constant 1.8.0” cannot describe both. Preserve existing engine-specific serialization initially; converging headless onto the full skill contract needs an explicit compatibility inventory and decision.
- **V3's cheaper-calibrator preference changes existing policy.** Current selection chooses the highest-capability disjoint class (`SKILL.md:1176-1185`). V3's lower-tier-first preference cannot simultaneously be called unchanged. Keep the rule initially and justify any required Opus calibration; a policy change requires explicit approval and evaluation.
- **V3 overstates its quorum constraint.** The current hard floor is reviewer count N=2, with model-class diversity recorded separately (`SKILL.md:600-610`). Requiring two distinct classes as a new hard precondition changes degradation behavior. Preserve the distinction instead of silently tightening it.
- **The manifest is not automatically a multi-file transaction.** Existing consumers do not necessarily read it. V3 must define how existing report/contract readers see readiness, and validate crash points; it cannot assume atomic replacement of several files or universal reader cooperation.
- **Exact identity will under-merge independently worded claims.** Preserve the conservative storage rule, but adjudicated issue IDs must prevent duplicate deviation counting. Neither claim normalization nor semantic issue identity is fully specified yet.
- **V3's measurement is expensive and lacks T1.** The 96-run pilot is explicitly budget-gated, not permission to spend; use a smaller exploratory sample and V2's T1 arm before a larger study. Its five-point margin is not powered proof.
- **V3's pre-support wording is too broad.** The agent definition describes UC-2 (`agents/reflect-reviewer.md:15`), but CARD identifies that agent with plan/spec inputs (lines 4-6). Pre use exists in the record; formalizing its brief/schema support is still proposed.
- **The headline cost target needs clearer labeling.** V3's cost section explains 37k-53k as a target and 37k-56k as allowance, but its candidate table calls the target a planning estimate. Use the broader band consistently; neither is measured savings.

## Shared assumption responses

A-001: QUALIFY - T2 may be useful, but V2's T1 arm is necessary to establish whether its pre-execution cost buys additional recall.
A-002: REJECT - Haiku stand-ins demonstrate that environment's behavior, not equivalence to the gateway's different model pools.
A-003: REJECT - CARD uses line-reference evidence without quote anchors, so a mandatory short-quote format requires tested conversion and cannot be assumed lossless.
A-004: REJECT - CARD includes dimensions, per-finding reasons and notes at lines 85-103, so preserving only calibrated numbers loses information.
A-005: REJECT - Turn-budget Claude-token estimates, artifact bytes and measured output tokens have different measurement bases.
A-006: QUALIFY - Exclusion is feasible only with a verified class registry and actual identity accounting, not a presumed one-to-one mapping between tiers and classes.
A-008: QUALIFY - Retain post debate for current contract compatibility and safety pending evidence, without claiming that deterministic classification is impossible in principle.
A-009: REJECT - A documented consumer map is not proof that no runtime reader or test equality-checks versions or enum values.
A-010: REJECT - A location/format failure is not invariably an invalid substantive citation, and mechanical success does not establish semantic support.
A-012: QUALIFY - Authored defects are useful controlled probes but must be supplemented by blinded natural-case review before broad quality claims.
A-014: QUALIFY - Shared code can change legacy behavior, so V1's explicit byte-identical legacy tests are needed rather than assuming non-interference.

## Per-point positions

| Point | Winner | Reason |
|---|---|---|
| S-001 | V3 | Five direct sentences state ownership and compatibility without hiding the decision. |
| S-002 | V1 | Candidate blocks plus matrix make architectural tradeoffs easiest to audit. |
| S-003 | V2 | Explicit read/unverified conventions are clearer than a borrowed generation timestamp. |
| S-004 | V1 | Direct-answer labels make the requested answers easy to find. |
| S-005 | V3 | In-place operational answers are usable without following forward references. |
| S-006 | V1 | Field ownership columns expose trust boundaries better than an example alone. |
| S-007 | V3 | Adds execution and publication obligations missing from numbered happy paths. |
| S-008 | V3 | Explicit state and retry identity protect against duplicate votes and partial publication. |
| S-009 | V1 | “What ships” and explicit rollback make migration stages concrete. |
| S-010 | V2 | Separate current/later columns make the semantic delta visible, despite its wrong version label. |
| S-011 | V3 | Separates retained-debate costs from hypothetical ablations and reviewer counts. |
| S-012 | V1 | Explicit proposed-name inventory reduces accidental reliance on nonexistent interfaces. |
| C-001 | V1 | Broad candidate set separates dispatcher-only adoption from merge replacement. |
| C-002 | V3 | Shares infrastructure while keeping genuine adversarial authority initially. |
| C-003 | V3 | Includes incomplete states and identity/accounting obligations, not only reuse opportunities. |
| C-004 | V3 | Submission completeness and independent coverage belong in the data contract. |
| C-005 | V3 | Exact identity avoids suppressing distinct claims merely sharing evidence. |
| C-006 | V3 | Keep the real pre debate until a separate ablation supports removal. |
| C-007 | V3 | Post classification retains all evidence and explicit adjudication. |
| C-008 | V3 | Immutable launch binding prevents two engines independently choosing identities. |
| C-009 | V3 | Separates capability tiers, reflect escalation and transport slots. |
| C-010 | V3 | Input drift and artifact readiness remain part of completion. |
| C-011 | V3 | Retries are attempts, not rounds or new clearing votes. |
| C-012 | V3 | Estimates remain estimates and unlike token units remain separate. |
| C-013 | V3 | Preserve T1 stop and avoid default large panels without categorical claims of uselessness. |
| C-014 | V2 | Resolution-only first is the smallest useful initial rollout. |
| C-015 | NONE | All misstate the existing headless version or omit its divergent serializer. |
| C-016 | V3 | Real child score keeps convergence semantics intact. |
| C-017 | V3 | Covers fallbacks and actual completion identity, not only initial candidates. |
| C-018 | NONE | V2's slot is invalid; V1 lacks a fully defined attachment bridge; V3 changes selection policy. |
| C-019 | V3 | Final semantic validation plus drift check protects the published result. |
| C-020 | V2 | T1 control tests whether the expensive mechanism is worthwhile at all. |
| C-021 | V3 | Explicit judge identity/collision handling is stronger than an unverified pass-through. |
| C-022 | V3 | Requires actual validation before emitting citation-drop accounting. |
| C-023 | V3 | Keeps separate document identities and treats ambiguity explicitly. |
| C-024 | V3 | Completion states separate empty-valid findings from failed or incomplete review. |
| C-025 | NONE | Proposed names have no demonstrated intrinsic winner; freeze behavior before naming. |
| X-001 | V3 | Calibration stays outside reviewer slots; avoids the exactly-one-fixed violation. |
| X-002 | V3 | Replace the ineligible anchor before resolution while retaining a valid template and bounded degradation. |
| X-003 | NONE | Headless emits 1.0; no variant's universal 1.8.0 premise is correct. |
| X-004 | V1 | Semantic enum/gate changes require a major version. |
| X-005 | V3 | Genuine adversarial finalization obeys the current no-own-merge rule. |
| X-006 | V3 | Agreement observations do not establish debate-removal recall equivalence. |
| X-007 | V3 | Separate input identity is safer than relying on synthetic-document line coordinates. |
| X-008 | NONE | Embedded calibration is today's fact; new sidecars must be described as migration. |
| X-009 | V3 | Calibrated cards remain finalizer inputs, rather than unattached sidecar numbers. |
| X-010 | V3 | Engine bindings need conformance verification, not unsupported gateway model overrides. |
| X-011 | NONE | Recorded pre use exists while the agent text is post-only; neither broad claim suffices. |
| X-012 | V3 | Profile turn-budget estimates are not established output-only usage. |
| X-013 | V3 | Reads the midpoint hard-kill rule and keeps it distinct from output estimates. |
| X-014 | V3 | The cost section explicitly distinguishes target from allowance; tighten headline wording. |
| X-015 | V3 | Labels savings hypothetical rather than presenting inconsistent net savings as established. |
| X-016 | V3 | Makes Opus conditional on a justified independent role, subject to the calibration-policy concession. |
| X-017 | V3 | Ignores revision authority and separates attempts from rounds instead of using cap as meaning. |
| X-018 | V3 | Preserves classifications and members rather than treating OR/max as adjudication. |
| X-019 | V1 | Its exclusion-fallback references correctly identify lines 405 and 408. |
| X-020 | V2 | Explicitly acknowledges the forbidden alias in tier data and proposes filtering it. |
| A-001 | V2 | Only its first experiment includes T1. |
| A-002 | V3 | Explicit transfer limits and actual-class accounting avoid treating stand-ins as gateway evidence. |
| A-003 | NONE | All require quote content without establishing lossless conversion of recorded line-only evidence. |
| A-004 | V3 | Original card/hash plus calibration provenance best preserve full information. |
| A-005 | V3 | Explicitly separates estimates, retrieval, bytes and provider usage. |
| A-006 | V3 | Distinct namespaces and actual identity checks best expose the missing class-map contract. |
| A-008 | V3 | Makes retention conditional on a later independent replacement trial, not impossibility in principle. |
| A-009 | V3 | Explicitly requires rechecking runtime consumers before implementation. |
| A-010 | V3 | Does not introduce an automatic precheck rejection layer. |
| A-012 | V3 | Varied frozen cases, independent expectations and pilot limits best constrain generalization. |
| A-014 | V1 | Byte-identical legacy tests make non-interference an acceptance criterion. |
