# Reflection Rubric Reference

Authoritative reference for the calibrated confidence score `C`, the three structural signals, and the calibrator-model selection algorithm. Consumed by **Wave 1D** (T1 self-card calibration) and **Wave 3C** (T2 per-reviewer-card calibration).

Spec source: `.dev/brainstorms/sc-reflect-rebuild/merged-requirements.md` §5.2 (lines 327-338) and §11.3 (lines 882-904).

---

## 5-dimension scoring

`C` is the **calibrated confidence** in the range `0.00-1.00`, computed as the **arithmetic mean across all five dimensions** below (spec §5.2 line 330). Each dimension is scored `0.00-1.00` on the criteria in this section, then averaged. The calibrator emits both the per-dimension scores and the mean `C` into `reflection-card.yaml`.

The five dimensions (spec §5.2 line 331) are:

### 1. Citation grounding

**Measures:** Whether every claim in the reflection card is anchored to a concrete artifact (file:line, symbol path, diff hunk, or spec section). Speculation without a citation is not citation grounding.

**Scoring guidance:**

- `1.00` — every claim has a verifiable artifact reference; no orphaned assertions
- `0.70-0.99` — most claims grounded; a small minority of supporting context lacks citations
- `0.40-0.69` — material findings carry citations but minor claims drift into speculation
- `< 0.40` — load-bearing claims lack any artifact reference

### 2. Coverage completeness

**Measures:** Whether the reflection touched every artifact in scope (every diff hunk for UC-2; every tasklist item / spec requirement for UC-1).

**Scoring guidance:**

- `1.00` — `coverage_pct == 1.00` and no `coverage_undefined` flag
- `0.85-0.99` — coverage meets or exceeds the §5.3 `<coverage-floor>` (default 0.90)
- `0.60-0.84` — partial coverage with explicit gap registry
- `< 0.60` — significant unmapped artifacts; reflection cannot stand alone

### 3. Deviation-classification clarity

**Measures:** Whether each deviation from spec is classified unambiguously as one of `{Aligned, Refinement, Drift, Regression}` with a single defensible category — not split-categorized or hedged.

**Scoring guidance:**

- `1.00` — every deviation has exactly one category and a one-line rationale
- `0.70-0.99` — categories assigned; a small minority hedge between two adjacent categories
- `0.40-0.69` — categories assigned but the rationale is weak or category drift is common
- `< 0.40` — categories missing, contradictory, or hedged across the majority of deviations

### 4. Risk surface coverage

**Measures:** Whether the reflection surfaces the load-bearing risks (regression candidates, blast-radius extensions, untested invariants) — not just the friendly findings.

**Scoring guidance:**

- `1.00` — risk register includes regression candidates AND structural risks (blast radius, untested invariants)
- `0.70-0.99` — primary risks covered; some secondary risks missed
- `0.40-0.69` — risks listed but shallow (no blast-radius reasoning)
- `< 0.40` — reflection only reports successes; risk surface is absent

### 5. Recommendation actionability

**Measures:** Whether the reflection's recommendations name a concrete next action with an artifact target (file, command, or task) rather than abstract guidance.

**Scoring guidance:**

- `1.00` — every recommendation cites a file/command/task and a verifiable success criterion
- `0.70-0.99` — most recommendations actionable; a minority are advisory
- `0.40-0.69` — recommendations are directional but lack concrete targets
- `< 0.40` — recommendations are platitudes; an executor cannot act on them

**Threshold guidance.** Per spec §5.3, `C ≥ 0.90` is the strict T1 ceiling and `C ≥ 0.85` is the medium-confidence floor inherited from sc-troubleshoot. `C < 0.85` is an automatic ESCALATE.

---

## 3 structural signals

Structural signals come from **Wave 1B** (not the calibrator) and feed §5.3 alongside `C`. They are spec §5.2 lines 335-337.

### S_scope

**Definition.** For UC-2: touched-file count from the diff. For UC-1: tasklist-item count.

**Range.** Non-negative integer.

**Threshold semantics (from §5.3):**

- `≤ 5` files — narrow scope, eligible for the strict T1 STOP rule when other conditions hold
- `≤ 10` files — medium scope, eligible for the §5.3 rule-2 path with WARN on `S_dev_density > 0.05`
- `> 10` files — exits the T1 STOP path

### S_domains

**Definition.** Count of **distinct domains** touched, where domains are counted from file paths against the set `{code, infra, docs, tests, config}`.

**Range.** Integer `1-5`.

**Threshold semantics (from §5.3):**

- `== 1` — single-domain, eligible for the strict T1 STOP rule
- `≤ 2` — eligible for the §5.3 rule-2 path
- `≥ 3` — automatic ESCALATE (rule 4): "multi-domain reflection cannot be reliably done by a single reviewer card"

### S_dev_density

**Definition.** For UC-2: `unmapped_diff_hunks / total_hunks`. For UC-1: `unmapped_spec_requirements / total_requirements`.

**Range.** Float `0.00-1.00`.

**Threshold semantics (from §5.3 / §5.5):**

- `≤ 0.05` — near-zero ambiguity, eligible for the strict T1 STOP rule
- `≤ 0.10` — eligible for the §5.3 rule-2 path (WARN above 0.05)
- `> 0.20` — automatic ESCALATE (rule 5): "at one in five unmapped artifacts, a single reviewer cannot adjudicate without ensemble pressure"

**S_dev_density sub-terms (V3 Serena adoptions).** The threshold semantics above are unchanged — the following are **additive weighting inputs** (not threshold changes) layered onto the computed value (the numerator arithmetic lives in `coverage-mapping.md`):

- **FR-6 onboarding-status weight.** Keyed on `onboarding_status` (Wave 0.7): `not_bootstrapped` down-weights grounding confidence (the project has no bootstrapped memory to ground against, so unmapped artifacts are more likely genuine ambiguity). Per **FR-6.4**, `unknown` is **NO signal** — it does NOT down-weight (absence of an onboarding marker is not evidence of a missing bootstrap). `bootstrapped` is neutral.
- **FR-7 context-exclusion up-weight.** When the Wave-0 `get_current_config` probe finds the active Serena context excludes a chain-critical tool (e.g. `get_diagnostics_for_file`), S_dev_density is **up-weighted** (the grounding chain ran with a known capability gap, so its unmapped-artifact ratio under-states true ambiguity) and `"serena:context-excluded"` is appended to `degraded_components`. The `serena:context-excluded` degrade token is an **intentional new colon-namespaced convention** (flagged in this task's Open Questions) — do not normalize it back to a hyphenated slug.
- **FR-1 missing-implementor count.** For UC-1, abstract symbols whose implementors are unaccounted (the `missing_implementations` count from §6.1 step 3b `find_implementations`) feed the **unmapped-artifact numerator** — an interface added with no wired implementor is an unmapped requirement for coverage purposes. The numerator arithmetic is in `coverage-mapping.md`; the degenerate no-op (no eligible symbol of kind ∈ {Interface, AbstractMethod, Protocol, Trait, Class}) emits `implementation_coverage_pct: null` (C5) and contributes nothing to the numerator.
- **FR-4 verification-failure weight (lint/type channel).** Keyed on `verification_failures` from the §6.1 step 5.5 verification triangle, **restricted to the `ruff`/`mypy` lint/type-finding channel** (exit 1 on those tools — explicitly NOT the §10.4 Regression channel, which is `pytest` exit 1 → `regression_present`). A verified lint/type finding on a hunk the tasklist claimed clean raises structural ambiguity, so it **up-weights** S_dev_density. This is an additive weighting input, not a numerator/threshold change; it is `null`-safe — when verification did not run (`verification_ran: false`) it contributes nothing.
- **FR-RV3-MED.1 hierarchy-gap weight.** Keyed on `hierarchy_gaps_found` / `hierarchy_coverage_pct` from the §6.1 step 4.5 `type_hierarchy` retrieval: a type whose transitive subtype family is under-registered (low `hierarchy_coverage_pct` / nonzero `hierarchy_gaps_found`) raises structural ambiguity and **up-weights** S_dev_density. Additive weighting input, not a threshold change; `null`-safe — when the backend is unavailable / `--with-hierarchy` is unset (`type_hierarchy_invoked: false`, `hierarchy_coverage_pct: null`) it contributes nothing. The numerator/formula side lives in `coverage-mapping.md`.

---

## Calibrator selection

The `confidence-calibrator` agent is **stripped of formation context** (spec §11.3 line 886). The card itself is its only input. The calibrator's **model class** is selected per the disjoint-set rule below, sourced from ICLR 2025 MAD evidence (spec §11.3 line 888).

### Pseudocode (verbatim from spec lines 889-898)

```text
LET reviewer_model_classes = union(reviewer 1..N model class)
LET calibrator_model_class ∈ {opus, sonnet, haiku, qwen, kimi, deepseek} \ reviewer_model_classes
IF disjoint set is non-empty: pick the highest-capability calibrator class from the disjoint set
                              AND emit `calibrator_diversity: full`.
IF disjoint set is empty (all available classes are reviewers):
    use the class with the highest available capability tier NOT used by the most reviewers
    AND emit `calibrator_diversity: degraded`.
```

### Telemetry

The field `calibrator_diversity: full | degraded` is emitted into `reflection-card.yaml`. The §12 eval rubric dimension "calibration discipline" asserts: `calibrator_model_class NOT IN reviewer_model_classes` (spec §11.3 line 900).

### Worked examples (disjoint-set resolution)

**Example A — full diversity.** Reviewers are `{sonnet, haiku}`. The disjoint set is `{opus, qwen, kimi, deepseek}`. Pick `opus` (highest capability in the disjoint set). Emit `calibrator_diversity: full`.

**Example B — full diversity, mixed-vendor.** Reviewers are `{opus, sonnet, haiku}`. The disjoint set is `{qwen, kimi, deepseek}`. Pick the highest-capability available among those three (resolved by deployment tier table; see Open Question below). Emit `calibrator_diversity: full`.

**Example C — degraded.** Only Anthropic aliases available and reviewers are `{opus, sonnet, haiku}`. Disjoint set is empty. Apply the fallback: pick the class with the highest capability tier **not used by the most reviewers**. If each class has exactly one reviewer, fall back to highest capability available (`opus`). Emit `calibrator_diversity: degraded`.

### Three-way partition (executor / reviewers / calibrator)

Per spec §11.3 line 902, the disjoint-set principle extends from "calibrator ≠ reviewers" to a **three-way partition**:

- `executor_class`, `reviewer_classes`, and `calibrator_class` SHOULD be **pairwise disjoint**.
- §7.1's executor-class exclusion rule enforces `executor_class ∉ reviewer_classes` at Wave 3A reviewer composition.
- §11.3 enforces `calibrator_class ∉ reviewer_classes` at Wave 1D / Wave 3C.

**Degradation behavior.** When all three pools cannot be made pairwise disjoint (e.g., only Anthropic aliases available AND executor was sonnet), the affected pool emits its `*_diversity: degraded` telemetry.

**Grader assertion.** The grader assertion is extended: `executor_model_class NOT IN reviewer_model_classes` is asserted whenever `executor_class_resolved == true`.

**Wave 3C parallelism.** For Tier 2, *every* reviewer card is calibrated by an **independent calibrator instance in parallel** (spec §11.3 line 904). Calibrated scores — not self-reported — feed the §5.3 rubric and the sc-adversarial-protocol debate weighting in Wave 4.

---

## Open Question

The spec specifies "highest-capability calibrator class from the disjoint set" but does not publish the **capability ordering** across the six classes `{opus, sonnet, haiku, qwen, kimi, deepseek}`. For deterministic resolution of Example B and similar mixed-vendor cases, an explicit capability-tier table is required. This is under-specified in the spec sections cited (§5.2, §11.3) and should be resolved either by a separate `refs/model-capability-tiers.md` reference or by an explicit ordering line added to §11.3 of the merged requirements.
