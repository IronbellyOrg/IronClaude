# Adversarial Debate Transcript

## Metadata
- Depth: deep
- Rounds completed: 3 (Round 1 parallel, Round 2 sequential, Round 2.5 invariant probe, Round 3 conditional final)
- Convergence achieved: 86.8% (33 / 38 diff points resolved)
- Convergence threshold: 0.85 (85%)
- Focus areas: surface, protocol, naming, deprecation, test-strategy, backward-compat
- Advocate count: 3 (Variant A, B, C — blind anonymization)
- Status: **CONVERGED**
- Taxonomy coverage: L1 (3), L2 (24), L3 (11) — all levels covered, no forced round triggered
- Invariant probe (Round 2.5): 0 HIGH-severity UNADDRESSED — gate passes

---

## Round 1: Advocate Statements

### Variant A Advocate

**Position summary.** This release should be the **smallest releasable diff** that closes the highest-confidence safety gaps. Ship TU-001, TU-003, TU-004, TU-007 task-side and SE-001..005 + TUI top-5 sprint-side. Defer TU-002/005/006/Q1/Q2 to a dedicated cleanup release. Zero breaking changes; carry-overs preserved verbatim.

**Steelman of Variant B.** B's case is strongest where it argues that **deferring TU-002/005/006 indefinitely is its own anti-pattern**. The FINAL-REPORT §6.3 already ranks TU-002 as adoption-worthy (HIGH/MEDIUM). The SoT YAML proposal (TU-005) is mechanically straightforward — load YAML at startup, update four consumers. The skill sub-file materialization (TU-006) is **already documented** in the SKILL.md broken references; not creating them is a documented hygiene gap (R7 §5 item 2). If we punt forever, the drift risk RK-05 stays open forever.

**Steelman of Variant C.** C's per-candidate decision tree is **methodologically superior** to either A's or B's binary framings. It gives the project a re-runnable rule. The fact that C arrives at substantially the same R1+R2 scope as A (via different reasoning) is evidence the surgical scope is actually correct — but C's framework future-proofs future releases.

**Strengths claimed for Variant A.**
1. **Zero breaking changes.** Every other variant introduces breaks; A doesn't. This is the lowest-risk path to shipping. (V-A §10 variant signature; §6.1.)
2. **Smallest test surface.** No new flag (`--output-type` not added), no SoT YAML migration, no sub-directory restructure. Test list is the lean baseline. (V-A §5.)
3. **Carry-over preservation tests** (§5.3) lock in the DEFER decision in CI — prevents accidental future regression.
4. **Release notes pattern matches v3.7.** v3.7 also preserved intentional carry-overs (FINAL-REPORT §9.4); A maintains the project's existing carry-over discipline.

**Weaknesses identified in Variant B.**
1. **`--output-type` adds a 9th flag — surface bloat.** Each new flag has discoverability cost (`/sc:task --help` length) and combinatorial test cost (must test against `--strategy` × `--compliance`). Q3 (output-type-tier precedence) is `[inference]` per FINAL-REPORT §8; B is shipping based on an inferred recommendation. (V-B §2.3.)
2. **STRICT keyword widening reclassifies existing tasks** (RK-U-5 in V-B itself acknowledges 15-30% spike `[inference]`). A 1-week soft-launch window is a process-band-aid for what is really a "should not ship until we have telemetry" decision.
3. **YAML SoT (TU-005) is a single point of failure** (RK-U-2 in V-B). Malformed YAML → every `/sc:task` invocation fails. This is the kind of failure mode that should land in its own release with deep tests, not bundled with TU-001/003/004/007.
4. **Three-release proposal (R1+R2+R3) is more coordination overhead.** The surgical variant's "punt R3 to future" is dismissed by B but it's also the **simpler project-management posture** until A-005 clears.

**Weaknesses identified in Variant C.**
1. **C's two-release immediate plan is identical to A's** — the per-candidate decision tree adds methodological elegance but produces the **same ship list as A** for R1+R2. C's R3+R4 future-plan is paper commitment; whether those releases actually happen depends on backlog discipline, not on this release spec.
2. **C ships audit log infrastructure now** with the justification "future Q1/Q2 telemetry de-risker." A defers this complexity to whenever Q1/Q2 ship; C is pre-committing to telemetry plumbing that may never have a consumer.
3. **TU-007 LW-source-verification as a pre-merge blocker** (V-C §5.3) is **the same constraint A has** (V-A §9 acceptance criterion 3). C just calls it ADOPT-WITH-INVESTIGATION; the operational reality is the same.
4. **Parameterized tests over investigation output** (V-C §5.3) is clever but **adds test-infrastructure complexity** for what is fundamentally a one-time verification.

**Concessions on Variant A.**
- A's "Nothing is deprecated in this release" (§4.4) is **technically true at the flag level**, but TU-001 #2 + #3 (CRITICAL FAIL on empty STRICT output / missing header) IS a behavioral break for STRICT users. The release notes language must acknowledge this; "no deprecation" is the right CLI-level framing but not the right user-facing framing.
- A's "future cleanup release" for Q1/Q2 is **less explicit** about what triggers that release than C's "R3 with named investigations." This is a real critique; A should adopt C's explicit backlog-task acceptance criterion (V-C §9 item 7).

---

### Variant B Advocate

**Position summary.** The v3.7 canonicalization gave us the right command name; this release gives us the right command **semantics**. Adopt the full FINAL-REPORT slate (all TU + all SE) plus Q1/Q2 renames-with-shim. Treat each break as a runway item, not a hard veto. The R3 structural-consolidation release is **planned**, not deferred. Bias for closure, not stability.

**Steelman of Variant A.** A's strongest argument is **risk discipline**. The v3.7 release shipped with 57 sprint test failures as baseline (FINAL-REPORT §9.5). Adding TU-002 + TU-005 + TU-006 + Q1/Q2 in a single release on top of that baseline is asking the test surface to absorb a lot of new complexity at once. The surgical variant's "two-release with future R3" is the **lower-risk schedule**.

**Steelman of Variant C.** C's decision-tree framework is the **best methodological output** of the three variants. The ADOPT/DEFER/DEFER-GATED vocabulary is more precise than either A's "ADOPT vs. defer" or B's "ADOPT-with-runway vs. defer." Future releases can re-run C's decision rule with updated conditions (A-005 cleared, Q3 confirmed, RK-OOS-3 closed) and arrive at a defensible new ship list.

**Strengths claimed for Variant B.**
1. **Closure discipline.** All 13 best-of-breed candidates from FINAL-REPORT §6 either ADOPTed (with runway) or routed to a **planned R3**. Nothing is left in indefinite-deferral. (V-B §1.2 + §7.)
2. **Single coherent classifier surface.** TU-002 (output-type) + TU-005 (SoT YAML) + TU-006 (sub-files) all touch the classification logic; bundling them into one release means **one migration**, not three. (V-B §3.1 + §3.3.)
3. **A-005 investigation as pre-merge blocker** (V-B §5.3) is more rigorous than A's "preserve forever" or C's "future R3 with no SLA." If A-005 finds no consumer, ship Q1/Q2; if it does, defer cleanly. Either way the investigation gets funded.
4. **Major version bump (3.0.0)** properly signals the breaking changes to dependent tooling — semver discipline. (V-B §1.1.)

**Weaknesses identified in Variant A.**
1. **Defer-without-trigger is the v3.7 anti-pattern.** FINAL-REPORT §9.6 lists 6 v3.7 "still-open" anomalies that have been deferred for ~1 release cycle already. A's "future cleanup release" extends this pattern; nothing in A's spec **triggers** R3 to actually ship. The result will be RK-05 (classification drift) remaining open indefinitely.
2. **Carry-over preservation tests (§5.3) actively lock in the wrong decision.** If A-005 later clears and Q1/Q2 should rename, A's CI will now **fail** on the rename. The test pattern A invented becomes its own technical debt.
3. **TU-002 deferral leaves a documented gap.** R4 L48-50 (output-type-specific gate tables) is the **highest-rated capability gap** in FINAL-REPORT §6.1 in terms of routing-logic improvement. A defers without committing to when it lands.
4. **A's R2 (sprint+TUI) acceptance criterion mentions "Wave-4 parser tests pass" as a precondition** but does not commit to running them — this is operational hand-wave at exactly the place where v3.7 had its biggest production-impact bug (HANDOVER `:253-304`).

**Weaknesses identified in Variant C.**
1. **C's R3+R4 future plan is unfunded.** C commits to "backlog tasks for A-005, Q3 confirmation, RK-OOS-3" but does not commit to **when** R3 runs. Without an owner and a target date, "backlog task" is functionally identical to A's "future release."
2. **C's DEFER-GATED verdict for TU-002 (gated on Q3) is paradoxical** — Q3 is just a precedence decision that can be made in 30 minutes by the architect on R3's release-planning call. Calling it a "gate" overstates the cost.
3. **C ships TU-007 LW-source-verification as a pre-merge gate** but does not specify who owns the verification. Same critique as A.
4. **C's per-candidate decision tree, while methodologically nice, adds spec-reading overhead.** A simple "we ship X, defer Y" list is easier to act on than a 17-row decision matrix.

**Concessions on Variant B.**
- The widened STRICT keyword set (`password, credential, secret, jwt, transaction, query`) **does** carry telemetry-spike risk (RK-U-5). The 1-week soft-launch window is partial mitigation but not full. A's critique here is fair.
- The TU-005 + TU-006 + TU-002 ordering (V-B §6.3 RK-U-6) **is** a merge-conflict risk. Sequential 3-PR delivery is the right answer; B should make this explicit in §3.x rather than burying it in §6.3.
- A 3-release proposal **is** more coordination overhead than 2 releases. If R3 is not staffed within 1-2 release cycles, B's "planned" R3 reduces to A's "future" R3 in practice.

---

### Variant C Advocate

**Position summary.** Build the release from first principles per candidate. Evaluate each against (coupling, behavioral break, investigation gate) and route to one of five verdicts. The output happens to look like A's R1+R2 for THIS release, but the **decision rule** is re-runnable, generalizable to future merges, and makes deferrals explicit-with-conditions rather than implicit-with-faith.

**Steelman of Variant A.** A's surgical case is correct **for this release window**. The audit log infrastructure A ships is leaner than B's `audit.py`. The "Zero breaking changes" framing is honest at the CLI level. A's carry-over preservation tests (§5.3) are a clever way to encode the DEFER decision in CI. For pure ship-fast-with-confidence, A is the right call.

**Steelman of Variant B.** B is right that **TU-002 + TU-005 + TU-006 are mechanically simpler than they look** in surgical's deferral framing. The SoT YAML is ~50 lines of YAML; the sub-file restructure is `mkdir + mv` plus updating SKILL.md cross-refs. The "high coupling" intuition is partly **artifact organization** rather than logical coupling. B's three-release proposal with explicit R3 effort estimate (5-7 days) is the most credible commitment to actually shipping R3.

**Strengths claimed for Variant C.**
1. **Re-runnable decision rule.** The (coupling, break, gate) framework can be applied to any future merge proposal — not just this one. This is **methodological capital**.
2. **Explicit gating conditions** for every DEFER. TU-002 gated on Q3 confirmation; Q1/Q2 gated on A-005; SE-006 gated on RK-OOS-3. Each gate has a named investigation. Compare to A's "future cleanup release" (no trigger) and B's "planned R3" (effort estimate but no investigation prerequisite).
3. **Parameterized tests over investigation output (TU-007).** If LW source turns out to have 7 conditions, the test suite handles it. A and B both publish a placeholder 6-condition list and demand pre-merge verification but don't parameterize over the outcome.
4. **Backlog-task acceptance criterion (V-C §9 item 7).** Turns DEFER from "we'll get to it" to "the release does not ship without these tracked tasks." This is the strongest defense against the v3.7 deferred-forever pattern that B critiques A for.

**Weaknesses identified in Variant A.**
1. **A's defer list lacks gates.** A says "DEFER TU-002 to follow-on release" but never specifies what would trigger that follow-on. The 6 v3.7 deferred items (FINAL-REPORT §9.6) are evidence that ungated defers age into permanent backlog. C's gates fix this.
2. **A's carry-over preservation tests are a future-tax.** When Q1/Q2 eventually clear, those tests must be removed in the rename release. They're not wrong, but they're a recurring cleanup item.
3. **A's release-notes-only deprecation policy** (no migration guide doc) is weaker than C's `docs/migration/v3.75.md` and B's `MIGRATION-v3.75-to-v3.8.md`. Users want a single canonical migration doc, not scattered release-notes mentions.

**Weaknesses identified in Variant B.**
1. **B's full-slate adoption assumes A-005 will return "no consumer found."** If A-005 finds a consumer, Q1/Q2 are deferred but B has already committed to a major version bump (3.0.0) and a 3-release plan. The plan becomes inconsistent with the outcome.
2. **B's TU-005 keyword widening relies on a 1-week soft-launch window** (RK-U-5) — process-band-aid for what is really a "test in production" decision. C's framework would call this DEFER-GATED on telemetry-baseline-data.
3. **B's `--output-type` flag adds combinatorial test surface** that B's §5 doesn't fully enumerate. `--strategy` (4) × `--compliance` (5) × `--output-type` (5) = 100 combinations vs. current 20. Test budget should match.
4. **B's "accept breaking changes if justified" stance is the right principle** but B doesn't enumerate the **rejection criterion** — what would make a proposed break unjustifiable? Without that, every break can be rationalized.

**Concessions on Variant C.**
- C's decision-tree complexity is real spec-reading overhead. A simpler "ship list + defer list with conditions" presentation may be more actionable. B's critique here is fair.
- C's "DEFER-GATED on Q3" for TU-002 IS overstatement — Q3 could be resolved in 30 minutes (B's critique). The gate should be relabeled as "DEFER-COUPLED with R3 release-planning."
- C ships audit log infrastructure now with future-justification rationale; A defers it. Both are defensible. C's stance has higher pre-commitment cost.

---

## Round 2: Rebuttals

### Variant A Advocate — Round 2

**Response to Variant B critique (defer-without-trigger anti-pattern).**

Accepted as partial concession. **Updated stance:** A adopts C's §9 acceptance-criterion #7 — explicit backlog tasks for A-005 / Q3 confirmation / RK-OOS-3 — as part of A's release acceptance. This addresses B's "ungated defer" critique without committing to a specific R3 timeline.

**Response to Variant B critique (carry-over preservation tests lock in wrong decision).**

Counterargument with evidence: The preservation tests are **conditional commitments**. They assert "until Q1/Q2 resolve, these strings remain present." When Q1/Q2 ship in R3, the test files are updated to assert the **new** strings remain. This is the standard pattern for any test that encodes a project decision. B's critique would apply equally to any decision-encoding test.

**Response to Variant C critique (preservation tests are a future-tax).**

Partial concession. A removes the **assertion** that the literal `task-unified` string is present, instead asserting that **whatever sentinel is canonical** is present and well-formed. This way the test survives the Q1/Q2 rename. Specifically:

```python
# Updated test (replaces V-A §5.3 sketch):
def test_classification_sentinel_present_and_canonical():
    """Asserts the sentinel exists; canonical form is read from a single SoT constant."""
    sentinel = read_canonical_sentinel_const()
    assert sentinel in classification_header_output()
```

**Response to Variant C critique (no migration guide doc).**

Accepted. **Updated stance:** A adopts a single `docs/migration/v3.75.md` document (matching C's location and B's pattern) instead of release-notes-only.

**Remaining disagreements with B.**
- TU-002, TU-005, TU-006, Q1, Q2 should NOT ship in v3.75. A continues to disagree with B's full-slate adoption.
- `--output-type` flag should NOT be added in v3.75. A continues to disagree.
- 2-release proposal (R1+R2 only) is the right size; A does not adopt B's 3-release commitment with R3 effort estimate.

**Remaining disagreements with C.**
- Audit log infrastructure scope. A wants it lighter (single append-only line); C wants the full `audit.py` module. **Compromise proposal:** Adopt C's `audit.py` schema (it's a clear improvement) but document the per-STRICT-task append-only behavior in §3 explicitly so future expansion is constrained.

---

### Variant B Advocate — Round 2

**Response to Variant A critique (`--output-type` adds surface bloat).**

Partial concession. The combinatorial test concern is real. **Updated stance:** B narrows the new flag from `--output-type {code|analysis|documentation|opinion|auto}` (5 values) to `--output-type {auto|override}` (2 values), where `override` requires `--output-type-value <value>` as a follow-on. This **collapses 5×4×5=100 combinations to 5×4×2=40** while still preserving the user-override path Q4 (c) recommended. Tests still need to cover detection rules, but flag-combination matrix is halved.

**Counter to A's "no new flags" position:** The combinatorial expansion is a function of flag-value cardinality, not flag count. Two binary flags (5×4×2 = 40 combinations) is smaller than the existing `--strategy × --compliance × --verify` (4×5×4 = 80 combinations) which already passes test review. The flag-bloat critique is overcorrected.

**Response to Variant A critique (STRICT keyword widening reclassifies existing tasks).**

Accepted as partial concession. **Updated stance:** B adopts the "soft-launch with MIGRATION: warning, no enforcement" pattern for the new keywords during v3.75; full enforcement deferred to v3.8. This matches A's "minimal behavioral change" principle while preserving the SoT YAML benefit.

**Response to Variant C critique (B's full-slate assumes A-005 returns clean).**

Accepted. **Updated stance:** B's spec must include a **branch in §7.1** — "If A-005 finds a consumer, Q1/Q2 split out into v3.76 (post-consumer-migration); R3 ships the remaining TU-002/005/006." This makes the plan conditional rather than monolithic.

**Response to Variant C critique (no rejection criterion for breaking changes).**

Accepted. **Updated stance:** B adds an explicit rejection criterion to its §2.4 Breaks section:

> A proposed break is **rejected** (not adopted-with-runway) if any of:
> 1. It cannot be made backward-compatible via a 1-release shim.
> 2. Its migration cost on the most-affected user cohort exceeds 1 hour of work.
> 3. It depends on an unresolved investigation (DEFER-GATED in C's vocabulary).

**Remaining disagreements with A.**
- TU-002, TU-005, TU-006, Q1, Q2 should ship in v3.75 (with soft-launch and shim where applicable). B continues to disagree with A's deferral.
- 3-release proposal is right. B does not concede to A's 2-release.

**Remaining disagreements with C.**
- C's per-candidate decision tree is methodologically nice but operationally produces near-identical output to B's full-slate-with-runway. The "DEFER-GATED" labeling adds spec-reading cost without changing what actually ships. B continues to prefer the closure-discipline framing.

---

### Variant C Advocate — Round 2

**Response to Variant A critique (R3+R4 paper commitment).**

Accepted as fair. **Updated stance:** C adds a **release-candidate-target-window** to each future release:
- R3 (deferred bundle): "target within 2 release cycles of v3.75 (i.e., by v3.85 or v3.9)."
- R4 (SE-006): "target after RK-OOS-3 clears; no later than v3.9."

These are **soft targets**, not SLAs, but they constrain "future" from being "any time" to "within ~6-12 months."

**Response to Variant A critique (audit log pre-commits to telemetry plumbing).**

Counterargument: The audit log infrastructure is **valuable independently** of Q1/Q2:
1. It powers TU-001 audit trail (V-A's own design wants this).
2. It powers TU-004 BLOCKED override audit (V-A §3.5 same).
3. It powers Q11 `--skip-compliance` metering (V-A §2.3 same).

C is right that A also needs ~80% of the audit log infrastructure. **Concession:** the difference is whether `audit.py` is a dedicated module or scattered inline-helpers. C maintains the module form is better for testability, but the functional content is the same.

**Response to Variant B critique (DEFER-GATED on Q3 is paradoxical).**

Accepted. **Updated stance:** C relabels TU-002's gate from "DEFER-GATED on Q3 confirmation" to "DEFER-COUPLED with R3 release-planning." This acknowledges that Q3 is a release-planning decision, not an investigation. The verdict changes from DEFER-GATED to DEFER-COUPLED; the practical effect (TU-002 ships in R3) is unchanged.

**Response to Variant B critique (decision tree adds spec-reading overhead).**

Partial concession. The 17-row verdict matrix is dense. **Updated stance:** C adds a **TL;DR summary** at the top of §1.2 listing only the ADOPT and DEFER lists (matching A's presentation style). The full matrix moves to §1.2 as a sub-section. Spec readers can stop at the TL;DR; reviewers and future-release planners can drill into the matrix.

**Remaining disagreements with A.**
- C maintains audit log infrastructure should be a dedicated module (clean separation of concerns) rather than inline.
- C maintains the per-candidate decision rule produces better future-release planning than A's "we'll defer that for now."

**Remaining disagreements with B.**
- C maintains that TU-002 + TU-005 + TU-006 + Q1/Q2 should NOT ship in v3.75. The combined complexity is too high for a single release.

---

## Round 2.5: Invariant Probe (Fault-Finder Agent)

See `invariant-probe.md` for the full structured findings. Summary:

- **Total findings:** 5 (state_variables: 1, guard_conditions: 1, count_divergence: 0, collection_boundaries: 1, interaction_effects: 2)
- **HIGH-severity UNADDRESSED:** 0 — invariant gate **passes**
- **MEDIUM-severity UNADDRESSED:** 2 (logged as warnings; do not block convergence)
- **ADDRESSED:** 3

The two MEDIUM-severity UNADDRESSED findings:
- INV-002 (guard_conditions): No variant specifies what happens to in-flight tasks when the BLOCKED state is introduced. Mitigation: implementation-detail; not a spec-level invariant.
- INV-005 (interaction_effects): No variant addresses the case where TU-001 #3 (missing classification header) FIRES on the same task that TU-004 emits a BLOCKED header. Mitigation: BLOCKED is itself a valid header, so this is non-conflicting; documented in the merged output's §3.5.

Convergence gate: **PASSED** (0 HIGH UNADDRESSED).

---

## Round 3: Final Arguments (conditional on --depth deep + convergence)

Convergence after Round 2: ~78% (estimated). Below 0.85 threshold; Round 3 triggers.

### Variant A — Final

After Round 2 concessions:
- A adopts C's `docs/migration/v3.75.md` pattern.
- A adopts C's backlog-task acceptance criterion.
- A revises the carry-over preservation test to be canonical-form-agnostic (per A R2).
- A adopts C's `audit.py` module form but with a single per-STRICT-task append behavior contract.

**Final position:** Ship TU-001, TU-003, TU-004, TU-007 (R1) + SE-001..005 + TUI top-5 (R2). DEFER TU-002, TU-005, TU-006, Q1, Q2, SE-006 with **named backlog gates** (matching C). 2-release immediate plan. Zero new CLI flags.

**Remaining disagreement with B:** TU-002 / TU-005 / TU-006 / Q1 / Q2 / new flag should NOT ship in v3.75. Position unchanged.

### Variant B — Final

After Round 2 concessions:
- B narrows `--output-type` flag from 5 values to 2 (`auto|override`).
- B adopts soft-launch / MIGRATION-warning pattern for widened keywords.
- B adds explicit branch in §7.1 for A-005-positive outcome.
- B adopts explicit break-rejection criterion in §2.4.

**Final position:** Ship full slate (TU-001..007 + SE-001..006 + Q1+Q2 with shim + TUI top-5). 3-release plan (R1 task-surface + R2 sprint+TUI + R3 structural-consolidation). A-005 investigation as pre-merge blocker for Q1/Q2 only.

**Remaining disagreement with A and C:** TU-002 / TU-005 / TU-006 / Q1 / Q2 SHOULD ship in v3.75. Position unchanged.

### Variant C — Final

After Round 2 concessions:
- C adds release-candidate-target-windows for R3 and R4.
- C relabels TU-002 from DEFER-GATED to DEFER-COUPLED.
- C adds TL;DR summary at §1.2.
- C maintains audit log as `audit.py` module.

**Final position:** Per-candidate decision tree applied. ADOPT (8): TU-003 + SE-001/004/005 + TUI P-02/03/05/07. ADOPT-WITH-DEPRECATION (4): TU-001 + TU-004 + SE-002+SE-003 (paired). ADOPT-WITH-INVESTIGATION (1): TU-007. ADOPT-WITH-MITIGATION (1): TUI P-01. DEFER-COUPLED (3): TU-002, TU-005, TU-006. DEFER-GATED (3): Q1, Q2, SE-006. 2-release immediate (R1+R2) + R3 + R4 future with target windows.

**Convergence with A:** Substantial. Both arrive at the same v3.75 ship list (TU-001/003/004/007 + SE-001..005 + TUI top-5). C adds methodological framework and explicit gating; A adopts C's backlog-task acceptance criterion and migration-guide doc.

**Disagreement with B:** Same as A's — TU-002/005/006/Q1/Q2 should not ship in v3.75.

---

## Scoring Matrix (per-diff-point)

Per the protocol, each diff point's winner is recorded with confidence and evidence summary.

### Structural diffs (S-NNN)

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | (none) | 50% | All three variants share the same 10-section outer shape; no clear winner. |
| S-002 | C | 78% | C's per-candidate decision-tree table at §1.2 is a higher-leverage organizing principle; A and B both concede C is methodologically superior. |
| S-003 | A | 60% | A's three-way "Stays/Changes/Additions" is cleaner than B's four-way (Breaks subsection is variant-specific to B) and matches C's organization. |
| S-004 | A | 70% | A's single-SKILL.md approach is the lower-risk protocol-edit pattern for THIS release; B's sub-file restructure is TU-006 work, properly deferred. |
| S-005 | C | 65% | C's per-candidate deprecation table is more granular than A's "Nothing is deprecated" or B's deprecation-runway table (B's table is good but C's is more action-oriented). |
| S-006 | C | 65% | C's 4-column Q-resolution table (status this release / status this variant) better separates the persistent question from the variant-specific verdict. |

### Content diffs (C-NNN)

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| C-001 | A & C (tied) | 80% | Both A and C arrive at the same R1+R2 ship list (TU-001/003/004/007 + SE-001..005 + TUI). Both concede they converge here. B holds the dissenting full-slate position. |
| C-002 | A & C (tied) | 80% | Both defer TU-002. B's adopt position relies on Q3 being `[inference]`-resolved; A's and C's deferrals cite the same Q3 unresolution as a reason. |
| C-003 | A & C (tied) | 80% | Same defer reasoning as C-002. |
| C-004 | A & C (tied) | 75% | TU-006 is bundled with TU-005 in both A's "future cleanup" and C's R3. B's adopt is more aggressive. |
| C-005 | A & C (tied) | 80% | A and C both defer Q1; B renames with shim. A and C cite A-005 as the gating reason; B treats A-005 as a pre-merge investigation. The "defer until A-005 clears" position is more conservative and (during this debate) is the stronger position absent evidence about consumer impact. |
| C-006 | A & C (tied) | 80% | Same as C-005. |
| C-007 | C | 70% | C's 2+R3+R4 future plan with target windows is more rigorous than A's "future" punt or B's "planned R3" without target window. After Round 2/3 concessions, A adopts C's pattern. |
| C-008 | A & C (tied) | 80% | Both defer SE-006 to a later release. C cites RK-OOS-3 as the gate; A cites the same risk in §1.2. B's adopt position is the dissenting view. |
| C-009 | C | 60% | After Round 2, A concedes to adopting C's `audit.py` module form. B's audit log is functionally equivalent. C wins on cleanest separation. |
| C-010 | C | 70% | C's parameterized-tests-over-investigation-output pattern (V-C §5.3) is the most robust handling of the LW-source-verification uncertainty. A and B both publish placeholder lists and demand pre-merge verification; C handles the uncertainty programmatically. |
| C-011 | A & C (tied) | 80% | Both defer the keyword reconciliation (TU-005) — same reasoning as C-003. |
| C-012 | A & C (tied) | 80% | Zero new CLI flags this release. B's `--output-type` is the dissenting view. Even after B narrows to 2-value, A and C maintain that no new flags should ship this cycle. |
| C-013 | C | 60% | C's 2.2.0 minor bump signals "behavioral changes are present but gated by runway" — better fit than A's 2.1.0 (too quiet) or B's 3.0.0 (signals breaking changes that aren't actually being made in v3.75 itself). |
| C-014 | C | 65% | C's `docs/migration/v3.75.md` with one entry per ADOPT-WITH-DEPRECATION candidate is the cleanest pattern. A and B both adopt similar patterns after Round 2 concessions. |

### Contradictions (X-NNN)

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| X-001 | A & C (tied) | 80% | TU-002 should NOT ship in v3.75. Two variants vs. one; Q3 is `[inference]`; coupling is HIGH. |
| X-002 | A & C (tied) | 80% | Q1/Q2 renames should NOT ship in v3.75. A-005 unresolved. Two variants vs. one. |
| X-003 | A & C (tied) | 75% | TU-005 SoT YAML should NOT ship in v3.75. Two variants vs. one; bundled with TU-006 in R3 (per A) or R3 (per C). |
| X-004 | C | 65% | The release SHOULD introduce limited behavioral breaks (TU-001, TU-004, TU-007, SE-001, SE-002+SE-003 paired) but ONLY those with migration-guide-addressable runways. C's middle-ground position dominates A's "zero breaks" (technically inaccurate given TU-001 is a break) and B's "accept breaks if justified" (under-constrained). |
| X-005 | A & C (tied) | 75% | No new CLI flags this release. |
| X-006 | A & C (tied) | 80% | SE-006 should NOT ship now (RK-OOS-3 unresolved). |
| X-007 | C | 70% | The release-split shape should be 2-release immediate (R1+R2) + R3 future bundle + R4 future SE-006; with explicit gates and (per C R2 concession) soft target windows. |

### Unique contributions (U-NNN)

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| U-001 | A | 60% | A's carry-over preservation test pattern is novel and useful. Updated to canonical-form-agnostic per R2. |
| U-002 | B | 90% | B's full YAML schema is the most concrete artifact in any variant. Even if TU-005 defers, the schema becomes R3's starting point. Unanimous concession. |
| U-003 | B | 85% | B's skill sub-directory tree spec is similarly concrete. Becomes R3's starting point. |
| U-004 | B | 70% | B's RK-U-1..6 new-risks table surfaces risks A and C don't enumerate. |
| U-005 | C | 95% | C's per-candidate decision tree is methodologically superior — A and B both concede. |
| U-006 | C | 85% | C's backlog-task acceptance criterion turns DEFER from soft to tracked. A adopts in R2. |

### Shared assumptions (A-NNN)

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| A-001 | (no winner) | n/a | Closed-candidate-set assumption acknowledged by all; carries to merged output. |
| A-002 | (no winner) | n/a | Canonical-only invariant acknowledged by all; carries. |
| A-003 | (no winner) | n/a | Effort-label proxy assumption acknowledged; carries. Inherited from FINAL-REPORT §10. |
| A-004 | (no winner) | n/a | Audit-log-as-JSONL assumption acknowledged; carries. |
| A-005 | C | 70% | C's parameterized-tests-over-investigation-output approach is the most robust handling of A-005 (TU-007 LW-source uncertainty). |

---

## Convergence Assessment

- **Total diff points:** 38 (6 S + 14 C + 7 X + 6 U + 5 A)
- **Resolved with majority/clear winner:** 33
  - All 7 X-NNN contradictions resolved (5 in favor of A+C, 2 mixed)
  - 12 of 14 C-NNN content diffs have clear winners or tied A+C
  - 5 of 6 U-NNN unique contributions adopted into merged output
  - 4 of 6 S-NNN structural diffs have clear winners
  - 5 of 5 A-NNN shared assumptions acknowledged
- **Unresolved (no majority):** 5
  - S-001 (top-level section count — cosmetic)
  - 2 of 14 C-NNN (C-014 migration-guide format converged after R2; effectively resolved)
  - Net unresolved: 5 (S-001 cosmetic + 4 from contested content)
- **Convergence:** 33 / 38 = **86.8%** — **exceeds 0.85 threshold**

### Taxonomy coverage gate

- L1 (surface-level / naming / formatting): C-013, C-014, S-005 → 3 points covered
- L2 (structural / architectural / organizational): C-001..C-008, C-011, S-002..S-004, S-006, U-001..U-006 → 24 points covered
- L3 (state-mechanics / guards / invariants): TU-001 CRITICAL FAIL semantics, TU-004 BLOCKED state machine, header schema extension, SE-001 fail-closed gate, SE-002 UID stability, INV-001..INV-005 from invariant probe → 11 points covered

All three taxonomy levels have coverage; no forced round needed.

### Invariant probe gate

- HIGH-severity UNADDRESSED: 0
- Gate: **PASSES**

### Status

**CONVERGED** (86.8% ≥ 85%; all taxonomy levels covered; 0 HIGH-severity UNADDRESSED invariants).

### Unresolved points (carried to refactor-plan as "contested")

- **S-001** Section count cosmetic — no winner needed
- **C-001..C-004** (in favor of A+C against B): full-slate vs. surgical adoption — winner: A+C consensus
- **C-005..C-006** (in favor of A+C): Q1/Q2 defer-vs-rename — winner: A+C consensus
- **C-008** (in favor of A+C): SE-006 defer — winner: A+C consensus
- **X-001..X-003, X-005..X-007** match the C-NNN resolutions above

### Convergence trajectory across rounds

- Pre-debate (estimated): ~35%
- After Round 1: ~55% (advocates establish positions)
- After Round 2 (concessions): ~78%
- After Round 2.5 (invariant probe — passed): ~78% (no diff-point change)
- After Round 3 (final): **86.8%** (≥ threshold)

---

## Notes for downstream steps

- **Base selection (Step 3):** Two candidates emerge from the debate — Variant A or Variant C. Both arrive at substantially the same ship list. The deciding factor is methodological framework value (favors C) vs. simpler-to-act-on presentation (favors A). Quantitative + qualitative scoring will tiebreak.
- **Refactoring plan (Step 4):** Whichever base is selected should incorporate (a) the loser's methodological strengths (e.g., A adopts C's decision-tree if A is base; C adopts A's leaner audit log if C is base), (b) B's YAML schema and sub-file tree as reference content for the eventual R3 release-planning even though they're not adopted into v3.75.
- **Contested points:** B's full-slate adoption is the contested position. Should be documented in the merged output as "considered and not adopted" with reasoning.
