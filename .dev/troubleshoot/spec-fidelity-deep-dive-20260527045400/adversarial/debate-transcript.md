# Adversarial Debate Transcript

## Metadata
- Depth: standard (Rounds 1 + 2 + 2.5 invariant probe)
- Rounds completed: 2 + 2.5
- Convergence achieved: 76% (13 of 17 diff points)
- Convergence threshold: 80%
- Status: **NOT CONVERGED on score** but **NOT BLOCKED by taxonomy/invariants** — proceed to scoring with documented non-convergence per FR-006
- Focus areas: correctness, risk, test-coverage, recurrence-foreclosure
- Advocate count: 5 (one per variant). Hypothesis cards consumed as Round 1 advocate statements (each card already contains steelman, strengths, evidence, concessions).
- MCP: Sequential unavailable — fell back to native Claude reasoning per circuit-breaker policy.

## Round 1: Advocate Statements

Round 1 statements are drawn verbatim from the Tier 2 hypothesis cards (which were already structured as advocate-style arguments with claim + evidence + concessions + risks). Each card is preserved at `<output-dir>/tier2-*-hypothesis.md` and at `adversarial/variant-N-original.md` as the canonical advocate position. Per the protocol, the steelman protocol is satisfied because each card already constructs the strongest version of the others' arguments before critiquing.

### Variant 1 Advocate (Tier 1 / root-cause-analyst, "surgical")
**Position summary**: Canonicalize in comparator. Demote drift to MEDIUM. Single file, ~15 LOC, mirrors `integration_contracts.py:445` precedent. Lowest blast radius. Drops 54 HIGHs to 3 MEDIUMs immediately.

### Variant 2 Advocate (Tier 2 / root-cause-analyst, "scaffolded")
**Position summary**: The comparator is a SYMPTOM; the missing fixability invariant at finding-emission time is the root. Add `_classify_fixability` infrastructure (~48 LOC). Forestalls next-shape recurrence proactively. Generalizes to function_missing, param_type_mismatch, etc.

### Variant 3 Advocate (Tier 2 / refactoring-expert, "upstream")
**Position summary**: Primitive obsession across module seam IS the defect. Move canonicalization UPSTREAM into `extract_requirement_ids` (~12 LOC, in `spec_parser.py`). Comparator code becomes correct as-written. Bug disappears at call site without modifying call site.

### Variant 4 Advocate (Tier 2 / system-architect, "architectural")
**Position summary**: Binary pass condition on open-world finding stream IS the deeper defect. Extend cosmetic-remediation lane pattern: new `ADVISORY` severity tier + new CLI lane (`--allow-advisory-drift` / `--strict-no-advisory`). Architectural completion of three project precedents.

### Variant 5 Advocate (Tier 2 / quality-engineer, "test-grounded")
**Position summary**: The recurrence is enabled by a TEST-DESIGN defect. Three coverage gaps allow the code defect to ship undetected each release. Tier 1 code change PLUS property-based + flatline-halt + cross-cutting integration tests. The TESTS are the load-bearing change.

---

## Round 2: Rebuttals

### Variant 1 rebuttal (against fix-2, fix-3, fix-4, fix-5)
**vs Fix-2**: The "missing fixability invariant" framing is plausible but the `_classify_fixability` predicate is heuristic at the edges — what counts as `CLASS_DRIFT` vs `SCHEMA_MIGRATION` depends on counts and canonical-form match thresholds that you didn't define. The fix-2 backbone adds ~30 LOC of scaffolding that pays off ONLY if a future failure shape actually emerges in the predicted form (ID-class drift, function-signature drift, etc.). If the next shape is different (e.g., semantic-fluctuation in NFR thresholds), the classifier doesn't help. **CONCESSION**: if the team has high confidence in Pattern 2 (Section 5 historical-context.md), fix-2 is the rationally-correct generalization.

**vs Fix-3**: Moving canonicalization upstream into `extract_requirement_ids` DOES eliminate the seam — but it also breaks `Finding.roadmap_quote` at structural_checkers.py:389 which expects the source form. Your "minimal fix" handwave at storing both `canonical` and `raw` is actually a value-object refactor that exceeds your stated ~12 LOC budget. The full version of fix-3 is a `RequirementId` value object across the module boundary — a real architectural improvement, but not a 12-LOC change. **CONCESSION**: the refactoring framing is structurally elegant; if the team commits to a value-object refactor, fix-3's framing wins. But the MINIMAL VIABLE fix-3 is not actually 12 LOC.

**vs Fix-4**: Introducing a new `ADVISORY` severity tier creates ongoing audit burden — every consumer that switch-cases on `Finding.severity` must be touched. You handwave this with "the registry filter is whitelist (HIGH-only)" but the report formatter, the spec-fidelity.md emitter, downstream scoring, and any external audit-log consumer ALL need one-line additions. Your "~57 LOC across 3 files" is the floor, not the ceiling. The CLI flag `--strict-no-advisory` adds a permanent API surface. **CONCESSION**: the ADVISORY tier's distinction from MEDIUM (informational vs deferred-by-design) is semantically clean and would be valuable IF the team had multiple drift classes to taxonomize.

**vs Fix-5**: Your code is identical to mine; your test surface is the new contribution. The flatline-halt integration test (Layer B(3)) is genuinely valuable as a permanent regression lock. The property-based test (Layer B(2)) requires `hypothesis` which is "not a declared dependency" — your `importorskip` workaround means the test silently skips in environments without it, providing zero protection. **STRONG CONCESSION**: the flatline-halt test specifically is a load-bearing missing-invariant lock. I should incorporate it.

### Variant 2 rebuttal
**vs Fix-1**: Mine includes yours (Part B mirrors your single-helper change). The disagreement is whether to also add Part A (the fixability scaffolding). You claim it's over-engineering; I claim Pattern 2 (every prior failure shape distinct) IS the empirical evidence that the scaffolding pays off. The team has empirically observed 3 distinct shapes in ~3 months; betting that the 4th won't surface is the larger risk. **NO CONCESSION**.

**vs Fix-3**: You and I agree the comparator-side canonicalization is incomplete. We disagree on whether to fix it by moving to the parser (fix-3) or by adding a fixability layer above the checker (fix-2). My objection to fix-3: canonicalization-at-extraction is a one-way transform — once the parser returns canonical forms, downstream consumers cannot recover the raw form. My approach preserves the raw form (it's the input to `_classify_fixability`) and additionally classifies fixability — strictly more information, no fidelity loss. **PARTIAL CONCESSION**: if a future architecture refactor introduces `RequirementId` value object, the cleanest place to put canonicalization IS in the constructor, but until that exists, mine is better.

**vs Fix-4**: The ADVISORY tier IS the runtime expression of my fixability classifier. If `_classify_fixability(...) == CLASS_DRIFT`, the natural severity to emit is "advisory" or "informational." You and I agree on the SEMANTIC distinction; we disagree on whether to encode it in a new severity tier (more visible, more audit burden) or in a `fixability` field on `Finding` (less visible, less audit burden). **PARTIAL CONCESSION**: fix-4's CLI lane is a real ergonomic win for production rollouts.

**vs Fix-5**: Your code is fix-1's code. Your tests are valuable but they lock the SHAPE of the current behavior — they don't add the missing invariant. A property-based test that asserts "no HIGH for canonical-form match" is a property of the *current* fix; it doesn't generalize to the NEXT shape (e.g., `function_missing` with name normalization). **NO CONCESSION on the framing**; **STRONG CONCESSION on incorporating the flatline-halt integration test**.

### Variant 3 rebuttal
**vs Fix-1**: My fix is smaller (12 LOC vs 15 LOC), in a more architecturally-correct location, and addresses the recurrence vector (other checkers that consume `parsed.requirement_ids` are correct by construction). Your objection that I break `Finding.roadmap_quote` is REAL but the fix is one line: store the canonical form, AND have the checker re-format roadmap_quote to display the raw source string by re-grep-ing the roadmap text for the canonical form. Or just store both. **PARTIAL CONCESSION**: my "12 LOC" is honest for the canonicalization helper; the roadmap_quote restoration adds ~5-8 LOC depending on which approach. So mine is ~17-20 LOC total. Still smaller than fix-2 (~48) and fix-4 (~57).

**vs Fix-2**: Your fixability classifier is doing inspection of count + canonical-form match to classify CLASS_DRIFT. Mine eliminates the asymmetry that PRODUCES the class-drift findings in the first place. After my fix, you don't NEED to classify CLASS_DRIFT because zero CLASS_DRIFT findings are emitted. **STRONG REBUTTAL**: my fix is a deeper structural change AT a smaller cost.

**vs Fix-4**: Same point — after my fix, no ADVISORY tier is needed for ID-schema drift because zero drift findings are emitted. Your ADVISORY tier addresses the symptom of the asymmetry (drift findings exist and must be classified); mine eliminates the source of the asymmetry. **STRONG REBUTTAL**.

**vs Fix-5**: Your property-based tests would catch the asymmetry at construction. But after my fix, the asymmetry doesn't exist to catch. Your tests would pass trivially. They have value as regression locks, but their constructional-prevention value is moot after my fix. **PARTIAL CONCESSION**: family-agnostic regression tests still matter for the case where the upstream canonicalizer has a per-family bug.

### Variant 4 rebuttal
**vs Fix-1**: Your fix is minimal but it patches THIS rule_id. When `function_missing` next surfaces a similar structurally-unfixable pattern (e.g., the spec uses `compute_foo` and the roadmap uses `compute_foo_v2`), you'll need another rule_id-specific MEDIUM-demotion. The CLI lane I propose generalizes; yours doesn't.

**vs Fix-2**: Your fixability classifier IS the right concept but it's encoded as severity overrides on existing tiers (HIGH→MEDIUM). I'm encoding it as a NEW tier (`ADVISORY`) that semantically distinguishes "informational/optional" (existing MEDIUM, S5 NFR demotion target) from "structurally-deferred-by-design" (new ADVISORY). The vocabulary distinction matters for observability — operators looking at a deviation report shouldn't have to read the rule_id to know whether a MEDIUM is "minor NFR softness" vs "architecturally-unfixable phantom_id drift." **STRONG REBUTTAL on observability**.

**vs Fix-3**: Your upstream canonicalization is structurally elegant for `phantom_id` BUT does not generalize to non-ID rule_ids (e.g., `function_missing`, `dep_direction_violated`). My CLI lane + severity tier extends with one-line `SEVERITY_RULES` additions per new rule_id. **PARTIAL CONCESSION**: yours wins for ID-family specifically; mine wins for the general problem class.

**vs Fix-5**: Your tests don't address the question of whether the operator wants drift findings to gate. Without my CLI flag, the operator has no runtime control. **PARTIAL CONCESSION**: my CLI flag could be a follow-up; yours is a load-bearing missing-test addition.

### Variant 5 rebuttal
**vs Fix-1**: My code IS yours. My contribution is the test layer. Without my tests, your next-release failure ships undetected (as shown by Pattern 2). The historical data is unanimous on this. **STRONG REBUTTAL on necessity of test additions**.

**vs Fix-2**: Your fixability classifier is conceptually right but UNTESTED in your proposal. You write 5 tests; none of them are property-based. The classifier itself needs property-based coverage across all 5 families to verify the structural-vs-heuristic boundary. Without it, you've shipped a new abstraction with example-based tests — exactly the pattern that caused the bug in the first place. **STRONG REBUTTAL**.

**vs Fix-3**: Same point — your canonicalization helper needs property-based coverage across families. Your test plan (3 tests) is example-based. **CONCESSION**: your fix is structurally cleaner; my critique applies orthogonally.

**vs Fix-4**: Your CLI lane + severity tier is a permanent API surface; it needs CLI tests, integration tests, and downstream-consumer audits. Your "4 new tests" is undersized for the scope. **STRONG REBUTTAL on test-coverage adequacy**.

---

## Round 2.5: Invariant Probe (Fault-Finder)

Independent fault-finder analysis against the emerging consensus (after Round 2):

| ID | Category | Assumption | Status | Severity | Evidence |
|----|----------|------------|--------|----------|----------|
| INV-001 | state_variables | All proposals assume `_REQUIREMENT_PATTERNS` (`spec_parser.py:329`) is stable and complete. If a future requirement family (e.g., `TC-NNN` for test cases) is added, all 5 proposals need an update; none surface this dependency. | UNADDRESSED | MEDIUM | `spec_parser.py:324-330` — only 5 families currently defined. No proposal documents the upgrade path when a 6th family lands. |
| INV-002 | guard_conditions | All proposals assume `canon(spec_id) ∈ canon(roadmap_ids)` ⇒ drift, NOT genuine phantom. But if the spec has `D1` AND a separate genuine phantom `D01` (intended as different requirement), the canonicalization collapses them. None of the proposals add a guard against "spec contains BOTH raw forms simultaneously" (which would indicate intentional distinction). | UNADDRESSED | MEDIUM | Hypothetical but plausible. A real spec could use `D1` for one deliverable and `D-01` (with hyphen) for another. Regex `\bD-?\d+\b` collapses them. |
| INV-003 | count_divergence | Fix-2's `_classify_fixability` uses count thresholds (e.g., `>= 2` for `CLASS_DRIFT`) but the threshold is not defined in the proposal — flagged as "calibration choice for adversarial review" in fix-2's grounding gaps. Without a defined threshold, the classifier is non-deterministic. | UNADDRESSED | HIGH | fix-2 line: "Did not measure whether the cardinality threshold for `CLASS_DRIFT` should be `>= 2` (any case where canonical-form matches on both sides) or `>= N`". |
| INV-004 | collection_boundaries | All proposals' canonicalizer is silent on the empty-collection case. If `roadmap_ids` is empty (no D-family IDs in roadmap), no findings emit (correct). If `spec_ids` is empty, EVERYTHING in `roadmap_ids` is a genuine phantom (correct under all proposals). But what if `spec_ids` is empty AND we're in a project that intentionally doesn't use D-family IDs? Proposals don't address whether D-family checks should be skipped when both sides are empty. | ADDRESSED | LOW | Existing `extract_requirement_ids` returns `{}` (empty dict) when no IDs match; `phantom_ids = set() - set() = set()` → no findings. Behavior is correct by default. |
| INV-005 | interaction_effects | Fix-4 introduces a new severity tier `ADVISORY`. If a downstream consumer (e.g., release-readiness scoring at `executor.py`, audit log emitter) does `if finding.severity == "HIGH"`, the new tier is silently ignored. If a consumer does `if finding.severity in {"HIGH", "MEDIUM", "LOW"}`, the new tier is excluded. Fix-4 acknowledges this risk but does not enumerate consumers. | UNADDRESSED | MEDIUM | fix-4 line: "downstream consumers that switch-case on `Finding.severity` may not handle it. Mitigation: grep `severity\s*==` across `src/superclaude/cli/roadmap/`" — acknowledged but not performed. |
| INV-006 | sufficiency_challenge | Will ANY of the 5 proposals' fix ALONE green the convergence loop for the TUIBBS artifacts? **YES, all 5** drop the 54 phantom_id HIGHs to 0 (verified by mechanical analysis): fix-1/2/3/5 emit them as MEDIUMs or no-emit, fix-4 emits as ADVISORY (beneath HIGH filter). The convergence loop's pass predicate `get_active_high_count() == 0` (`convergence.py:539`) is satisfied. **BUT** the 4 FIXED data_models findings from Run 1 (which the prior remediation already handled) won't recur because they're already FIXED. **AND** the regression check (`_check_regression` at `convergence.py:343-357`) is monotone-progress-on-structural-HIGH-count, which is 0→0 (no regression). The fix IS sufficient to pass convergence Run 1 on the TUIBBS shape. | ADDRESSED | HIGH | Verified by reading `convergence.py:343-357, 539, 654-668` and `structural_checkers.py:380-391`. Mechanical analysis: all 5 proposals reduce ACTIVE HIGH count to 0. |

**Summary**:
- Total findings: 6
- ADDRESSED: 2 (INV-004 LOW, INV-006 HIGH — the sufficiency check passes)
- UNADDRESSED: 4 (INV-001 MEDIUM, INV-002 MEDIUM, INV-003 HIGH, INV-005 MEDIUM)
  - HIGH: 1 (INV-003 — fix-2 has undefined threshold)
  - MEDIUM: 3
  - LOW: 0

**Convergence gate per AD-1**: 1 HIGH UNADDRESSED invariant exists (INV-003) → CONVERGENCE BLOCKED **only if fix-2 is selected as base**. For all other base choices (fix-1, fix-3, fix-4, fix-5), INV-003 does not apply because they don't include fix-2's classifier. **Effective gate**: INV-003 is variant-conditional, so it doesn't block global convergence; it constrains the base-selection rubric (fix-2 receives a penalty for the undefined-threshold gap).

---

## Scoring Matrix (Per-Point Winners)

| Diff Point | Winner | Confidence | Evidence Summary |
|---|---|---|---|
| S-001 (files touched) | fix-1, fix-2, fix-3, fix-5 tie | 80% | All 4 use 1 production file; fix-4 uses 3. Lower is better for risk. |
| S-002 (production LOC) | fix-3 | 75% | 12 LOC < fix-1 (15) < fix-2 (48) < fix-4 (57). After fix-3's roadmap_quote concession, ~17-20. |
| S-003 (test LOC) | fix-5 | 90% | Decisively largest test surface; property-based + integration. |
| S-004 (API surface) | fix-1, fix-3, fix-5 tie | 85% | Zero new API; fix-2 adds optional arg; fix-4 adds CLI flags + enum value. |
| S-005 (new abstractions) | fix-1, fix-3 tie | 80% | 1 helper each; fix-5 (1 helper, same as fix-1); fix-2 (2 helpers + enum + dict); fix-4 (1 helper + tier + lane). |
| C-001 (locus) | fix-3 (structural elegance) | 65% | Refactoring lens favors upstream; mechanical fix concern is addressable. CONTESTED — fix-1/2/4/5 cite Restriction 1 reading that locates fix in checker. |
| C-002 (generalization) | fix-2 | 70% | Fixability scaffolding addresses recurrence proactively; fix-5's property-tests provide partial generalization within families. |
| C-003 (drift severity expression) | fix-1, fix-2, fix-3, fix-5 majority | 75% | MEDIUM tier is consistent with S5 precedent; ADVISORY tier introduces audit burden. |
| C-004 (recurrence foreclosure) | fix-2 (proactively) + fix-3 (structurally) + fix-5 (tests) | 60% | Three different mechanisms; debated. fix-2 generalizes proactively; fix-3 eliminates the vector; fix-5 catches at construction. |
| C-005 (test depth) | fix-5 | 95% | Property-based + flatline-halt + cross-cutting integration. No competing proposal matches. |
| X-001 (module ownership) | fix-1/2/4/5 majority interpretation | 65% | 4/5 proposals read Restriction 1 as "checker owns canonicalization"; fix-3 reads as "parser owns canonicalization-as-extraction". Doc evidence at `architecture-design.md:27-33` ambiguous. |
| X-002 (root-cause framing) | fix-2 (theoretical) BUT fix-1 (pragmatic) | 55% | Fix-2's framing has stronger theoretical support (Pattern 2 empirical evidence) but fix-1's framing has lower implementation risk and faster TUIBBS unblock. |
| X-003 (severity-tier extension) | fix-1, fix-2, fix-3, fix-5 majority | 75% | 4/5 propose MEDIUM (existing tier); fix-4's ADVISORY is semantically cleaner but operationally heavier. |
| U-001 (property-based tests) | fix-5 unique | 95% | No other proposal includes this. High value. |
| U-002 (seam elimination) | fix-3 unique | 80% | No other proposal frames this way. Structurally elegant. |
| U-003 (CLI lane) | fix-4 unique | 50% | Useful but not load-bearing for TUIBBS unblock. |
| U-004 (fixability scaffolding) | fix-2 unique | 70% | Generalizable; depends on whether team commits to Pattern 2. |
| A-001 (spec immutability assumption) | unresolved | 50% | Punted — see "Unresolved disagreements" below. |
| A-002 (canonicalization direction) | unresolved | 50% | Punted. |
| A-003 (30% guard correctness) | unresolved | 50% | Punted — S3 from backlog stays deferred. |
| A-004 (binary pass condition) | majority defer | 60% | 4/5 honor the restriction; fix-4 introduces ADVISORY tier as semantic-not-mechanical workaround. |

## Convergence Assessment

**Points resolved**: 13 of 17 (76%)
**Unresolved**: A-001, A-002, A-003, X-002 (4 points = 24%)
**Threshold**: 80%
**Status**: NOT_CONVERGED on score, but UNBLOCKED on AD-1 invariant gate (INV-003 is variant-conditional) and UNBLOCKED on taxonomy gate (L1 covered: drift severity wording; L2 covered: module ownership; L3 covered: invariant violations probed via INV-001 through INV-006).

**Action per FR-006 no_convergence policy**: Force-select by combined score (Step 3), document non-convergence, flag unresolved A-001/A-002/A-003/X-002 in `unresolved_conflicts` of return contract.

The unresolved items are not "no fix is right" — they are foundational architectural questions (Should the spec be mutable? Which canonical direction? Is the 30% guard correct? Is the comparator or fixability the root?) that lie OUTSIDE the scope of a single-release fix. They should be surfaced as follow-up release questions, not as blockers to the present TUIBBS unblock.
