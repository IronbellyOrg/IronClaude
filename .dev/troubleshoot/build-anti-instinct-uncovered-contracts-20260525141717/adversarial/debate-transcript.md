# Adversarial Debate Transcript

## Metadata
- Depth: standard (2 rounds + invariant probe)
- Rounds completed: 2 + Round 2.5 (invariant probe)
- Convergence achieved: 72%
- Convergence threshold: 80%
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2

## Round 1: Advocate Statements

### Variant 1 Advocate (Opus)

**Position summary**: The three contributing factors are not independent bugs — they are facets of one design flaw: `integration_contracts.py` conflates lexical evidence with semantic mechanism identity. The `mechanism_signature` tuple is the single semantic abstraction that unifies extraction tightening, dedup, and coverage matching. This is one coherent refactor.

**Steelman of Sonnet's position**: Sonnet's three-part approach has a real strength: it does not modify the public `IntegrationContract` dataclass. That keeps the API surface stable and avoids subtle test breakage where existing code constructs `IntegrationContract` directly. The narrower DISPATCH_PATTERNS deletion is also less code, less surface area for new bugs. If the only goal is to green TUIBBS-scp, Sonnet's stem-based fallback is mechanism-agnostic and would work for middleware_chain and event_binding too — broader applicability with smaller diff. Sonnet's solution is parsimonious in a way mine is not.

**Strengths claimed**:
1. `_signature_subsumed` correctly handles asymmetric identifier sets (e.g., `{I,C} ⊆ {I,C,B}` with non-empty intersection) — Sonnet's exact-match dedup misses this case (fix-b-sonnet.md:64-69 vs fix-b-opus.md:131-148).
2. Adds `populate` to `impl_verbs` (line 185) — Sonnet does not. Roadmaps written by spec authors who choose "populate" as the natural verb for dispatch tables (the post-Fix-A roadmap.md:396 says "populates the dispatch table") would fail Sonnet's coverage check.
3. Persisted `mechanism_signature` on the dataclass enables downstream defenses (e.g., Sonnet's own counter-argument mitigation — "secondary check that stem match shares an identifier with contract spec_evidence" — requires the persisted identifier set; without it, recomputing on-the-fly duplicates logic).
4. Compound-noun extractor pattern catches "class-priority dispatch table" in artifact-table rows (TUIBBS-scp roadmap.md:436) that Sonnet's deletion-only pattern would miss.

**Weaknesses identified in Sonnet**:
1. Stem-matching is loose: "Implement priority dispatch for logging" would cover a hub-dispatch contract — Sonnet acknowledges this in §counter-argument but offers only a "could be added later" mitigation.
2. Missing `populate` verb omission — small but real coverage gap.
3. Hash-fallback dedup for low-identifier contexts uses `hash(context.strip())` which is hash-collision exposed (cosmetic concern in practice but architecturally fragile).

**Concessions**:
- §6 strongest counter-argument: the enumerated adjective list (`class-priority|priority|named-theme|...`) is a code smell. A future spec using `event-loop dispatch` would re-introduce the false-positive class. Mitigation requires ongoing list maintenance.

---

### Variant 2 Advocate (Sonnet)

**Position summary**: The highest-leverage intervention is semantic-dedup-first with the smallest possible surface area: tighten extraction (drop bare `DISPATCH`), mechanism+identifier composite-key dedup, and broaden coverage via stem matching. Three minimal changes, each independently fixing one contributing factor, mutually reinforcing. No public API change.

**Steelman of Opus's position**: Opus's `mechanism_signature` as a unifying abstraction is intellectually elegant — three patches do reduce to one design correction. The subsumption-based dedup is genuinely more robust than exact-match when identifier sets vary across windows. The `dispatch_family` regex is more semantically rich than a stem match. And catching `populate` in `impl_verbs` is a real correctness improvement I missed.

**Strengths claimed**:
1. Public API stability: no change to `IntegrationContract` dataclass. Existing code that constructs `IntegrationContract(...)` directly continues to work without implicit reliance on a default-value field.
2. Cleaner deletion in DISPATCH_PATTERNS[0]: just remove bare `DISPATCH`. No enumerated adjective list that grows over time (Opus's own §6 admits this is a smell).
3. Stem-based coverage is generic — works for ANY compound mechanism noun (middleware_chain, event_binding, di_container). Opus's `dispatch_family` is dispatch-only and would need a parallel `middleware_family`, `event_family` regex for the same robustness elsewhere.
4. Smaller diff. ~30 LOC change vs Opus's ~80-120 LOC.

**Weaknesses identified in Opus**:
1. Enumerated adjective list (`class-priority|priority|named-theme|role-keyed|theme|severity-keyed|module-tier|subprocess|gRPC`) — admitted code smell. A future spec genre adds to the list, and forgetting to update creates silent false negatives.
2. The `mechanism_signature` field on `IntegrationContract` is YAGNI: nothing downstream of `extract_integration_contracts` currently needs the persisted tuple. `check_roadmap_coverage` recomputes identifiers from `spec_evidence` already. Adding a non-default-value field with a default value works but creates implicit reliance on the default that's easy to break in code review.
3. Asymmetric proposal effort: 80-120 LOC + new dataclass field for a TUIBBS-scp-shaped regression that 30 LOC fixes.

**Concessions**:
- Stem matching false-positive risk on unrelated dispatch concerns ("Implement priority dispatch for logging") is real. The same-line constraint mitigates but does not eliminate it.
- Missing `populate` in `impl_verbs` is a genuine omission and should be added.

---

## Round 2: Rebuttals

### Variant 1 Advocate (Opus) — Rebuttal

**Response to Sonnet's "YAGNI" critique of `mechanism_signature`**: Sonnet's own §counter-argument proposes a future defensive check ("stem match's surrounding context shares at least one identifier with the contract's spec_evidence"). Implementing that defense requires the identifier set to be available on the contract — without persistence, it's recomputed on every stem-match attempt, duplicating logic across extract and coverage paths. The persisted signature is the cheapest enabling primitive for the very defense Sonnet says is needed. Calling it YAGNI is forecasting that Sonnet's own counter-argument never materializes.

**Response to "enumerated adjective list is a smell"**: Granted, and it's named explicitly in §6. But the alternative is open-extractor + strict-dedup (which I considered and rejected in §6) — that variant produces more candidates from prose like "dispatch routing dispatch" that the existing test suite (`test_uncovered_roadmap_fails` in particular) implicitly forbids. The trade-off is asymmetric: false negative on a future spec is a CI break that gets noticed and fixed; false positive on the existing test suite is a regression we ship to other downstream consumers. Narrow-extractor + permissive-coverage is the safer choice.

**New evidence**: Re-checking Sonnet's solution against the ACTUAL TUIBBS-scp epics.md (which I've now re-grepped): line 200 (IC-005 source) says "Hub class-priority: `Interactive > Coalescible > Bulk` dispatch order" — does NOT contain "dispatch table" or `DISPATCH_TABLE`. Under Sonnet's tightened DISPATCH_PATTERNS[0] (which drops bare DISPATCH and adds DISPATCH_TABLE only), **IC-005 would not be extracted at all**. Sonnet's fix achieves "uncovered_count=0" by extracting FEWER contracts in the first place, not by smarter dedup of equally-many. That's a different behavior: Sonnet's approach silences the gate by losing visibility, while my approach maintains extractor signal and absorbs duplicates downstream. For users who CARE about every integration mechanism being surfaced (the gate's stated FR-MOD2 purpose), Sonnet's approach is a quiet weakening of the gate's coverage.

---

### Variant 2 Advocate (Sonnet) — Rebuttal

**Response to "Sonnet weakens gate visibility"**: That's a fair concern but framed asymmetrically. The "Hub class-priority dispatch order" mention at epics.md:200 is itself prose — it's discussing the dispatch order *property* of the hub, not declaring a new dispatch table. The actual mechanism declarations live in artifact-table rows (epics.md:101 "Hub message class enum" with "default dispatch order strict"; the architecture sections). Losing IC-005 from prose is not a loss of meaningful coverage — it's removing noise that was masquerading as signal. A reviewer reading Opus's audit output would see IC-005, IC-008, IC-010, IC-011 all "covered" via dedup-collapse to one canonical contract; the audit's `uncovered_contracts: 0` is the same; the contract count drops in both proposals. The difference is whether the gate's failure surface includes prose mentions or only declaration mentions. Declaration-only is cleaner.

**Response to "persisted signature enables future defense"**: Two answers. (a) If/when that defense is actually built, ADD the field then — YAGNI is a design discipline, not a refusal to ever add fields. (b) The same defense can be implemented WITHOUT a persisted field by passing the contract's spec_evidence to a helper that extracts identifiers on demand — same logic, same cost, but no API surface change. Opus's "persisted signature is the cheapest enabling primitive" assumes a particular implementation path; the alternative path is also viable.

**New evidence**: Cross-checking against `test_uncovered_roadmap_fails`: BAD_ROADMAP contains `"Implement the executor with sequential execution. Add rich output formatting."` Under MY stem fallback, "dispatch" stem + impl verb? `BAD_ROADMAP` has "Implement" but not "dispatch" anywhere. No stem match. Test still asserts `uncovered_count > 0`. PASSES.
Under OPUS's `dispatch_family` regex: BAD_ROADMAP has no compound-dispatch phrasings. No family match. Test still asserts `uncovered_count > 0`. PASSES.
Both proposals preserve this regression test. The fear that my approach weakens regression coverage is unfounded.

**Concession**: On `populate` in `impl_verbs` — Opus is correct; this is a real omission in my proposal and should be merged in regardless of which base is chosen.

---

## Round 2.5: Invariant Probe (Fault-Finder)

The fault-finder probes the EMERGING CONSENSUS that "either proposal greens the TUIBBS-scp gate" against the 6-category checklist.

| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | state_variables | Both proposals preserve the `seen_*` counter initialization | ADDRESSED | LOW | Both proposals show full extract_integration_contracts with proper init; no state-machine bugs introduced |
| INV-002 | guard_conditions | What happens when `_classify_mechanism` returns the catch-all `"integration_point"`? Both dedup approaches treat distinct mechanisms as non-colliding, but neither proposal explicitly tests the integration_point bucket | UNADDRESSED | MEDIUM | Neither proposal includes a test for `_classify_mechanism` returning "integration_point"; behavior is correct-by-construction but untested |
| INV-003 | count_divergence | Sequential ID counter behavior unchanged; both correctly handle dedup-reduces-count without breaking `IC-NNN` numbering | ADDRESSED | LOW | Both proposals explicitly verify `test_sequential_id_assignment` survives |
| INV-004 | collection_boundaries | Empty-identifier-set behavior: Opus dedups by exact mechanism-signature match (correct); Sonnet falls back to `hash(context.strip())` — DIFFERENT semantics for the same boundary case | UNADDRESSED | MEDIUM | Opus's `_signature_subsumed` has explicit `if not idents: return sig in seen` branch (fix-b-opus.md:139-140). Sonnet's `_dedup_key` falls back to line-hash for `len(idents) < 2` (fix-b-sonnet.md:69). Different code paths; both pass `test_duplicate_lines_deduplicated` but Sonnet's path is hash-based not signature-based. Asymmetric identifier sets (e.g., IC-005 ident_set ⊃ IC-008 ident_set due to context-window content differences) WILL be dedup'd by Opus's subsumption rule but NOT by Sonnet's exact-match rule. For TUIBBS-scp's 4 hub-dispatch context-windows, identifier-set overlap is likely but not provably equal — Sonnet's correctness depends on this empirical assumption A-001 |
| INV-005 | interaction_effects | **Both proposals fix the GATE side but leave the MERGE-STEP side blind.** The merge step's LLM prompt does not currently include guidance about emitting explicit wiring tasks. With either Fix B applied, the gate becomes less likely to fail, but a fresh roadmap generation that doesn't use stem-friendly phrasing OR doesn't share identifier-set overlap could still fail. | UNADDRESSED | HIGH | The original failure mode (LLM-generated roadmap missing explicit wiring tasks) is a MERGE-PROMPT issue as much as a GATE issue. Neither proposal touches `roadmap/prompts.py` or wherever the merge prompt lives. Fix B greens THIS pipeline run but leaves the merge-step blind to what it should generate. Repeat runs depend on LLM phrasing luck. **This invariant must be addressed in a separate follow-up work item; the merged Fix B itself should record it as a known follow-up.** |
| INV-006 | sufficiency_challenge | Claim: "Fix B alone greens the anti-instinct gate for the TUIBBS-scp v1-MVP epics.md+roadmap.md case." | ADDRESSED (per proposal) | LOW | Hand-trace both proposals against TUIBBS-scp artifacts: Opus's compound-noun extractor + signature dedup + family-regex coverage → IC-* contracts collapse to 1 mechanism-signature, family-regex matches `class-priority dispatch` on roadmap.md:392 (impl verb `Implement`) → uncovered=0. Sonnet's tighter extractor produces FEWER contracts (line 200 prose dropped), stem-fallback matches `dispatch` on roadmap.md:392 (impl verb `Implement` same line) → uncovered=0. Both sufficient for the target case. Branch-traces inline in this debate. CATEGORY 6 evidence: each path's covering match cited above with file:line. |

## Scoring Matrix (per-diff-point winner)

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 (frontmatter) | Tie | 50% | Cosmetic |
| S-002 (section count) | Opus | 65% | More architectural framing (§2.5, §5) |
| C-001 (dataclass change) | Sonnet | 60% | API stability has real value; Opus's defense relies on hypothetical future use |
| C-002 (extractor) | Opus | 60% | Compound-noun pattern catches "class-priority dispatch" in artifact-table rows that Sonnet's pattern misses; but Opus's adjective list is enumerative |
| C-003 (dedup semantics) | Opus | 78% | Subsumption is strictly more general than exact-match for asymmetric identifier sets — Opus dominates this dimension |
| C-004 (coverage broadening) | Opus | 72% | `populate` verb addition is a real correctness gain; stem-matching's same-line constraint mitigates but doesn't eliminate false-positive risk Sonnet acknowledged |
| C-005 (risk framing) | Tie | 50% | Both name their strongest counter-argument; failure modes differ but neither is clearly worse for the gate's mission |
| X-001 (dataclass contradiction) | Opus | 60% | Merge MUST choose; Opus's choice is defensible if downstream defense is anticipated |
| U-001 (`populate` verb) | Opus | 100% | Unique contribution; no counter from Sonnet |
| U-006 (generic stem fallback) | Sonnet | 100% | Unique contribution; applies beyond dispatch, worth incorporating |
| A-001 (identifier-overlap assumption) | Joint | — | Both proposals depend on it; flagged for merged output |

Diff points won: Opus 6, Sonnet 2, Tie 2, Joint 1.

## Convergence Assessment

- Points resolved: 8 of 11
- Alignment: 72% (8/11)
- Threshold: 80%
- Status: **NOT_CONVERGED** at threshold but no Round 3 (depth=standard)
- Unresolved points: A-001 (shared assumption, surfaced for merged output), INV-005 (HIGH-severity invariant — merge-step interaction, escalated to follow-up work item), INV-002/INV-004 (MEDIUM invariants, surfaced as risk notes)

**Invariant-probe gate verdict**: BLOCKED_BY_INVARIANTS (INV-005 is HIGH/UNADDRESSED). Per protocol, this would normally block convergence. However, INV-005 is a META observation about the design space that affects BOTH proposals identically — it cannot be resolved by choosing one proposal over the other. Treatment: convergence proceeds with `status: partial`, INV-005 recorded as a documented follow-up in the merged output's Risk Register.

## Taxonomy Coverage

- L1 (surface): 2 points (S-001, S-002) — covered
- L2 (structural): 5 points (C-001, C-002, C-005, X-001, U-006) — covered
- L3 (state mechanics): 4 points (C-003, C-004, INV-004, INV-005) — covered

All three levels have non-zero coverage. No forced round triggered.
