<!-- Provenance: This document was produced by /sc:adversarial via sc:brainstorm-protocol Wave 3 -->
<!-- Base: V1 (opus:analyzer) — surgical-minimum refactor -->
<!-- Incorporated: V3 (haiku:qa) Changes 4 + 5 + property test P5; V2 (sonnet:architect) U-001 as optional -->
<!-- Merge date: 2026-05-26T20:50:00Z -->
<!-- Convergence: 1.00 — CONVERGED (above 0.65 threshold). Direction convergence unanimous; per-point confidences range 0.70-0.95. -->

# Calibration Refactor Proposal — pr86-integration-contracts substrate

**Substrate**: pr86-integration-contracts-20260526100600 (structurally analogous to H3 0.95-REFUTE miss)
**Root-cause document**: `.dev/troubleshoot/pr86-integration-contracts-20260526100600/calibration-failure/FINAL-MERGED-CAUSES.md`
**Failure mode under repair**: Confidence calibrator can score a hypothesis card at ≥0.85 calibrated on source-only evidence for runtime-behavior claims.

## Scope

Markdown-only proposal. 5 in-scope changes targeting `src/superclaude/` source-of-truth (NEVER `.claude/` — that is sync-dev output):

1. `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` — rubric formula + 6th dimension + verdict-direction modifier
2. `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` — `Claim class` frontmatter + `Runtime check` self-assessment + `Falsification standard` field
3. `src/superclaude/agents/confidence-calibrator.md` — Responsibilities updated to apply the new formula + modifier + claim-class handling
4. `src/superclaude/skills/confidence-check/SKILL.md` — scope-correct the "Test Results 1.000/1.000" cultural-prior claim (5-line annotation)
5. NEW FILE: `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` — pin-test corpus (6 fixtures + 5 properties) that gates future changes to files 1-3

---

## Change A — `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`

**Section affected**: `## Confidence calibration (Wave 1.7)` — dimension table at lines 11-17 + formula at line 19. Add new subsection `### Verdict-direction modifier (M3a)` between calibration and escalation decision. Add one new rule under `## Escalation decision` § 3.

**Shape**: insert (6th dimension row, modifier subsection, escalation rule) + replace (Evidence grounding 1.0 anchor, formula line).

**Diff sketch**:

```diff
 | Dimension | 1.0 (strong) | 0.5 (partial) | 0.0 (weak) |
 |-----------|--------------|---------------|------------|
-| **Evidence grounding** | Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |
+| **Evidence grounding** | Cited `file:line` matches a real code path that exhibits the symptom (snippet match verified by calibrator's spot-check) | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |
 | **Symptom coverage** | ... |
 | **Reproducibility fit** | ... |
 | **Fix directness** | ... |
 | **Domain coherence** | ... |
+| **Runtime check** | Hypothesis includes an executed reproducer with captured stdout/stderr that reproduces the symptom; OR an asserted-by-test runtime invariant (test cited by name AND its execution-state declared) | Hypothesis includes a runnable command but no captured output; OR cites a test that exists but was not exercised at hypothesis time | Hypothesis is source-only — no executed reproducer, no test assertion. For `claim_class: static_defect`, this dimension inherits the Evidence grounding score (static defects' source IS their runtime). For `claim_class: runtime_behavior` or `environment_dependent`, source-only cards mandatorily score 0.0. |

-**Confidence** = arithmetic mean of the five dimension scores.
+**Confidence** = `min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)`.
+
+The +0.30 buffer means a 0.5 dimension caps the composite at 0.80, *below* the 0.85 STOP gate. A 0.0 dimension hard-caps the composite at 0.30. The gates apply unconditionally (no claim_class exemption); for `static_defect` claims, Runtime check auto-inherits Evidence grounding so the gate is satisfied whenever the citation is.

 Round to two decimals.

+### Verdict-direction modifier (M3a)
+
+After computing the gated-minimum confidence, apply this modifier when the card's frontmatter declares `claim_class: runtime_behavior` AND `runtime_check < 1.0`:
+
+| Verdict direction | Cap on calibrated confidence |
+|-------------------|------------------------------|
+| REFUTE / REJECT   | 0.70 |
+| AFFIRM            | 0.84 |
+
+Rationale: a wrong REFUTE on runtime behavior closes the investigation door (the H3 0.95-REFUTE case); a wrong AFFIRM is caught by CI. Source-only REFUTEs of runtime claims are the precise failure mode under repair and must not clear the 0.85 STOP gate. The 0.84 AFFIRM cap means source-only AFFIRMs of runtime claims still ESCALATE to Tier 2 (below the 0.85 STOP).

 ## Escalation decision (Wave 2)
 ...
 3. **Signal-driven escalation** (any one triggers escalation)
    - `confidence < 0.85` → ESCALATE (`escalation_reason: low_confidence`).
    - Multi-domain symptom ...
    - Symptom described as intermittent ...
    - Reproducibility dimension scored 0.0 ...
    - `--type security` AND confidence < 0.95 → ESCALATE (`escalation_reason: security_caution`).
+   - `claim_class ∈ {runtime_behavior, environment_dependent}` AND `runtime_check < 0.5` → ESCALATE (`escalation_reason: source_only_dynamic_claim`).
```

---

## Change B — `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`

**Sections affected**: frontmatter block (lines 12-16), per-dimension self-assessment (lines 48-53), and append two new required sections after `## If I'm wrong, it's probably because…`.

**Shape**: insert (frontmatter field, dimension row, Falsification section, Runtime check section) — additive only; no replacement of existing required fields.

**Diff sketch — frontmatter**:

```diff
 **Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">
+**Claim class**: `static_defect` | `runtime_behavior` | `environment_dependent`
+  — `static_defect`: source-reading alone is sufficient evidence (typos, missing imports, regex literals, syntax errors)
+  — `runtime_behavior`: claim depends on dynamic control flow, side effects, executed semantics, or library call dispatch
+  — `environment_dependent`: claim depends on OS / runtime / feature-flag / network / data state
+**Verdict direction**: `AFFIRM` | `REFUTE` | `REJECT`
+  — REFUTE/REJECT verdicts on `runtime_behavior` claims face a higher calibration bar (see escalation-rubric § Verdict-direction modifier).
 **Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>
```

**Diff sketch — per-dimension self-assessment**:

```diff
 Per-dimension self-assessment:
 - Evidence grounding: <0.0|0.5|1.0> — <one-line reason>
+- Runtime check: <0.0|0.5|1.0> — <cite the executed-reproducer command + captured output, OR cite a runtime-asserting test by name + its execution state. For claim_class=static_defect, mark "inherits Evidence grounding" with no further evidence required.>
 - Symptom coverage: <0.0|0.5|1.0> — <one-line reason>
 - Reproducibility fit: <0.0|0.5|1.0> — <one-line reason>
 - Fix directness: <0.0|0.5|1.0> — <one-line reason>
 - Domain coherence: <0.0|0.5|1.0> — <one-line reason>
```

**New required section** (append after "If I'm wrong, it's probably because…"):

```diff
+## Falsification standard
+
+One sentence. What concrete evidence — an executable command and expected output, a named test outcome, a log assertion, or a measurable observation — would prove this hypothesis WRONG? "Re-reading the source differently" is NOT a falsification standard. If you cannot name a falsification standard, the claim_class is `runtime_behavior` and Runtime check self-scores ≤ 0.5.
```

**New optional section** (from V2's typed evidence table, presented as recommended shape):

```diff
+## Recommended evidence shape (v2.0 preview)
+
+For new cards, the recommended evidence shape is a typed table that makes each item's evidence kind explicit:
+
+| # | Kind | Source | Content |
+|---|------|--------|---------|
+| E1 | `source_citation` | `path/to/file.py:142` | (verified snippet) |
+| E2 | `executed_reproducer` | `uv run python -c "..."` | (captured stdout/stderr) |
+| E3 | `test_assertion` | `tests/.../test_x::test_y` | (execution state: fails / passes / not-run) |
+
+Kinds: `source_citation`, `executed_reproducer`, `test_assertion`, `documentation`, `log_artifact`.
+
+This shape is **OPTIONAL in v1.5** — the existing bulleted-list evidence shape remains valid. The typed table will become **MANDATORY in v2.0** (target: follow-up commit after pin-test corpus in `calibrator-eval-cases.md` confirms v1.5 stability).
```

---

## Change C — `src/superclaude/agents/confidence-calibrator.md`

**Sections affected**: `## Independence Instruction` (lines 23-27) — note about self-reported confidence anchoring; `## Responsibilities` (lines 48-54) — full revision to reflect 6 dimensions + new formula + modifier; `## Output Format` (lines 58-93) — add Runtime check row, add `## Confidence` block elaboration. Insert new subsection `## Claim-class handling` between Independence Instruction and Inputs.

**Shape**: replace (Responsibilities steps 1, 4-6); insert (Claim-class handling subsection, Stage-2 trace rows in Output Format); append (escalation-reason allowed-value `source_only_dynamic_claim`).

**Diff sketch — Responsibilities**:

```diff
 ## Responsibilities

-1. **Read the rubric** at `rubric_path`. Note the 5 dimensions: Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
+1. **Read the rubric** at `rubric_path`. Note the 6 dimensions: Evidence grounding, Runtime check, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
 2. **Read the card** at `card_path`.
+2a. **Resolve `claim_class` and `verdict_direction` from frontmatter.** If `claim_class` is absent, default to `runtime_behavior` (fail-safe: assume runtime semantics matter until proven otherwise) and record the default in your Notes. If `verdict_direction` is absent, default to `AFFIRM` and record similarly (this preserves backward-compat with v1.0 cards; future schema v2.0 will require both fields explicitly).
 3. **Spot-check the evidence**: for each `file:line` cited in the card, Read the file at that range and verify the snippet matches. This is essential to scoring "Evidence grounding" honestly. If a citation does not match, mark it in the Notes section and let that drive the Evidence grounding score.
-4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. Cite the specific card content (or absence thereof) that drove the score.
-5. **Compute the arithmetic mean**, rounded to 2 decimals.
+4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. For **Runtime check**: score honestly even though your tools are `Read`-only. If the card cites no executed reproducer with captured output and no named test asserting the runtime invariant, Runtime check = 0.0 — there is no leniency for "I read the code carefully." 0.5 requires a runnable command in the card without captured output. 1.0 requires captured stdout/stderr OR a named test with declared execution-state. For `claim_class: static_defect`, Runtime check inherits the Evidence grounding score (do not re-derive).
+5. **Compute calibrated confidence** using the rubric's gated-minimum formula: `min(arithmetic_mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)`. Round to 2 decimals. Emit a **Stage-2 trace** in your report (see Output Format) showing each gate's value so the formula application is auditable.
+5a. **Apply the verdict-direction modifier** per the rubric: when `claim_class: runtime_behavior` and `runtime_check < 1.0`, cap calibrated at 0.70 (REFUTE/REJECT) or 0.84 (AFFIRM). Record whether the cap was binding in the Stage-2 trace.
 6. **Apply the escalation decision rules** (rubric § Escalation Decision, in order) using the score and the `flags_context`. Return the verdict (`STOP` or `ESCALATE`) and the matching `escalation_reason`. Note: the allowed-value set for `escalation_reason` is extended with `source_only_dynamic_claim`.
```

**Diff sketch — new subsection `## Claim-class handling`** (insert after Independence Instruction):

```diff
+## Claim-class handling
+
+The card declares `claim_class` in frontmatter. You read it but you do not redetermine it from scratch (that invites anchoring on whether you *can* verify the claim with Read alone). Trust the card's declaration with ONE exception: if `claim_class: static_defect` is declared but the card's claim references dynamic control flow ("falls through to", "the runtime would", "after the side effect", "dispatched via", "the helper actually returns"), flag the misdeclaration in Notes and score the card AS IF `claim_class: runtime_behavior`. Surface the discrepancy explicitly so the orchestrator can act on it.
+
+Why this matters: the failure mode under repair (M2) is calibrators scoring runtime-behavior claims at 0.85+ on source-only evidence because the rubric's Evidence-grounding OR-clause permitted it. The `claim_class` field + the Runtime check dimension makes the structural inadequacy of source-only evidence visible at the dimension level rather than hidden inside Evidence grounding's old OR-clause. Your job is to enforce the visibility, not to relitigate the claim_class declaration.
```

**Diff sketch — Output Format additions**:

```diff
 | Dimension | Score | Justification (cite card content) |
 |-----------|-------|-----------------------------------|
 | Evidence grounding | 1.0 / 0.5 / 0.0 | <one-line citing what in the card supports this> |
+| Runtime check | 1.0 / 0.5 / 0.0 | <cite the executed-reproducer block or named test in the card, or its absence; for claim_class=static_defect, note "inherits Evidence grounding"> |
 | Symptom coverage | ... |
 | Reproducibility fit | ... |
 | Fix directness | ... |
 | Domain coherence | ... |

+## Stage-2 trace (REQUIRED)
+
+| Step | Value | Notes |
+|------|-------|-------|
+| arithmetic_mean(all_six) | <X.XX> | raw mean |
+| gate_M1: evidence_grounding + 0.30 | <X.XX> | always applies |
+| gate_M2: runtime_check + 0.30 | <X.XX> | always applies |
+| gated_min | <X.XX> | min of the three above |
+| verdict_cap | <none | 0.70 | 0.84> | M3a; binding only if claim_class=runtime_behavior AND runtime_check<1.0 |
+| **calibrated** | <X.XX> | final |

 ## Confidence
-- **Self-reported (in card)**: <X.XX>
+- **Self-reported (in card)**: <X.XX> — read but NOT used as input to your score (independence instruction)
 - **Calibrated (this report)**: <Y.YY>
+- **Formula applied**: `min(mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)` then verdict-direction cap if applicable
 - **Delta**: <signed difference, and a one-line read on why it differs>
```

---

## Change D — `src/superclaude/skills/confidence-check/SKILL.md` (cultural-prior correction)

**Section affected**: lines 14-18, the "Test Results (2025-10-21): Precision 1.000, Recall 1.000, 8/8 test cases passed" block.

**Shape**: replace — scope the unqualified claim to the 5 pre-implementation checks it actually covers.

**Diff sketch**:

```diff
 **Requirement**: ≥90% confidence to proceed with implementation.

-**Test Results** (2025-10-21):
-
-- Precision: 1.000 (no false positives)
-- Recall: 1.000 (no false negatives)
-- 8/8 test cases passed
+**Test Results** (2025-10-21, scope: the five pre-implementation checks below — duplicate / architecture / docs / OSS / root-cause):
+
+- Precision 1.000 / Recall 1.000 on 8 fixtures covering the five pre-implementation checks
+
+**Out of scope for these test results**:
+- Runtime-behavior calibration (see `sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`)
+- Sha-pinned PR-diff citations (see same)
+- Structurally-unverifiable predicates of any kind
+
+The 5-check confidence assessment ratchets are a pre-implementation gate, not a general epistemology for code claims. Runtime-vs-static evidence is the calibrator's responsibility (escalation-rubric § Runtime check), not this skill's.
```

**Rationale**: the unqualified "1.000 / 1.000" claim was the rhetorical engine of the M2 cultural prior. Scoping the claim to its actual coverage kills the recursion of anti-pattern (Cross-mechanism implications ¶5 of FINAL-MERGED-CAUSES.md) without changing any behavioral logic. 5 lines.

---

## Change E — NEW FILE: `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`

**Shape**: create. This is the M4 deliverable — pin-test corpus + property tests that gate any future change to Changes A-C.

**Content**:

```markdown
# Calibrator Eval Cases

Golden hypothesis cards + expected calibrated scores. Run before any change to `escalation-rubric.md`, `confidence-calibrator.md`, or `hypothesis-card-template.md` ships. A regression on any fixture or property test blocks merge of the rubric/calibrator/card change.

## Fixtures

### Fixture 1 — `fixture-h3-style.md` (source-only runtime REFUTE)

Hypothesis card with `claim_class: runtime_behavior`, `verdict_direction: REFUTE`, evidence_grounding=1.0, runtime_check=0.0 (source-only), four other dims=1.0.

**Expected calibrated**: ≤ 0.70 (M3a cap fires).
**Asserts**: M1 + M2 + M3a all closed in combination.

### Fixture 2 — `fixture-pr86-rca-style.md` (AFFIRM with structural truncation)

`claim_class: runtime_behavior`, `verdict_direction: AFFIRM`, evidence_grounding=1.0, runtime_check=0.5 (runnable command in card, no captured output), four other dims=1.0.

**Expected calibrated**: ≤ 0.80 (gate_M2: runtime_check + 0.30 = 0.80; AFFIRM cap 0.84 not binding here).
**Asserts**: M1 + M2 closure; below the 0.85 STOP gate.

### Fixture 3 — `fixture-static-defect-clean.md` (the eval_run.py Path import case)

`claim_class: static_defect`, evidence_grounding=1.0, runtime_check inherits 1.0, four other dims=1.0.

**Expected calibrated**: 1.0.
**Asserts**: refactor does NOT over-correct; legitimate static defects pass cleanly.

### Fixture 4 — `fixture-sha-pinned.md` (structurally unverifiable predicate)

Card cites `commit-sha-5a65c62:file:line`. `claim_class: static_defect`, evidence_grounding=0.5 (calibrator cannot verify against current HEAD), runtime_check inherits 0.5.

**Expected calibrated**: ≤ 0.80 (gate_M1: 0.5 + 0.30 = 0.80).
**Asserts**: sha-pinned cites cannot score 0.85+ even when self-classed as static_defect.

### Fixture 5 — `fixture-v1-legacy-card.md` (missing claim_class — migration)

v1.0 frontmatter with no `Claim class` or `Verdict direction` fields.

**Expected behavior**: calibrator defaults claim_class to `runtime_behavior` and verdict_direction to `AFFIRM` (fail-safe), records the defaults in Notes, proceeds with calibration.
**Asserts**: migration backward-compat — v1.0 cards do not break the calibrator; defaults err on the side of caution.

### Fixture 6 — `fixture-refute-runtime-verified.md` (legitimate REFUTE with strong runtime check)

`claim_class: runtime_behavior`, `verdict_direction: REFUTE`, evidence_grounding=1.0, runtime_check=1.0 (captured stdout from executed reproducer that contradicts the rejected claim), four other dims=1.0.

**Expected calibrated**: 1.0.
**Asserts**: M3a cap does NOT fire when runtime_check=1.0; legitimate runtime-verified REFUTEs are not over-penalized.

## Property tests

| ID | Property | Assertion |
|----|----------|-----------|
| P1 | M1 gate | `evidence_grounding ≤ 0.5` ⟹ `calibrated ≤ 0.80` for any other-dim combination |
| P2 | M2 gate | `runtime_check ≤ 0.5 AND claim_class ∈ {runtime_behavior, environment_dependent}` ⟹ `calibrated ≤ 0.80` |
| P3 | M3a cap | `verdict_direction == REFUTE AND claim_class == runtime_behavior AND runtime_check < 1.0` ⟹ `calibrated ≤ 0.70` |
| P4 | Determinism | running calibrator on same card produces same calibrated score (±0.0) across N=5 runs |
| P5 | Anchoring (soft) | varying the card's `Self-reported confidence:` field from 0.30 to 0.99 must not change calibrated by more than ±0.05. **Soft assertion** (warn-only in CI; LLM-as-judge has natural variance). Tighten over time. |

## Forward-compat note

Fixtures 1-6 + properties P1-P5 cover v1.5 closure (Changes A-D). Add fixtures for v2.0 evidence-kind validation (`source_citation` | `executed_reproducer` | `test_assertion` typed table mandatory) when the v2.0 schema ships.

## Suite integrity

Run on every PR that touches:
- `escalation-rubric.md`
- `confidence-calibrator.md`
- `hypothesis-card-template.md`
- `confidence-check/SKILL.md`

A regression on any fixture or hard property (P1-P4) blocks merge. P5 warnings are surfaced for triage.

## Implementation hook (deferred to follow-up commit)

The pytest harness invoking this corpus is OUT OF SCOPE for this brainstorm proposal. Expected landing path: `tests/troubleshoot/test_calibrator_eval_cases.py`. It should load each fixture, dispatch the calibrator (or its inline-fallback), and assert on the returned calibrated value.
```

---

## Cause → Fix coverage matrix

| Cause | Change A (rubric) | Change B (card) | Change C (calibrator) | Change D (SKILL.md) | Change E (eval cases) | Closes? |
|-------|---------------------|--------------------|------------------------|----------------------|------------------------|---------|
| **M1** — arithmetic-mean dilution (0.89) | gated-min formula | — | applies formula | — | P1 fixture+property | **closes + prevents regression** |
| **M2** — source-vs-runtime evidence conflation (0.85) | 6th dim Runtime check + tightened Evidence grounding anchor | claim_class frontmatter + Runtime check self-assessment + Falsification standard | scores Runtime check honestly under Read-only; claim_class handling | scopes cultural-prior "1.000/1.000" claim | P2 fixture+property | **closes + prevents regression** |
| **M3a** — verdict-direction asymmetry (0.78) | verdict-direction modifier table | verdict_direction frontmatter | applies modifier | — | P3 fixture+property | **closes + prevents regression** |
| **M3b** — falsification standard / doubt-channel (0.65) | — | Falsification standard required section | reads it indirectly via Runtime check evidence | — | (implicit — fixtures 1, 2, 6 exercise it) | **partially closes** (field exists; calibrator does not yet *score* it as its own dimension) |
| **M3c** — residual anchoring (0.45) | — | — | Independence Instruction tightened (read but don't use self-reported confidence) | — | P5 anchoring property test (soft) | **partially closes** (prompt-level + CI prevention; no structural input-filter — that ships in v2.0) |
| **M4** — eval-suite silent-green (0.68) | — | — | — | scopes the "1.000/1.000" claim to its actual coverage | **direct closure — Change E IS M4's deliverable** | **closes + prevents regression** |

---

## Minimal-change subset closing M1 + M2 + M3a

**Changes A + B + C alone** mathematically close M1 + M2 + M3a.

- Change A alone closes M1 mathematically but the card has no slot for runtime_check; calibrator has no instruction to score it.
- Change B alone exposes claim_class + Runtime check field but the rubric still averages it into the old mean; verdict-direction modifier still absent.
- Change C alone cannot apply a formula that isn't in the rubric and cannot read a field that doesn't exist on the card.

These three are **compositional, not exchangeable** — applying any subset of {A, B, C} alone underfits the failure mode.

**Changes D + E** are defense-in-depth:
- **D** kills the cultural-prior recursion (~5 lines)
- **E** prevents silent regression of A-D (recursion-of-anti-pattern prevention per Cross-mechanism implications ¶4-5 of FINAL-MERGED-CAUSES.md)

Ship A + B + C + E in one PR (the rubric/card/calibrator triple + the pin-test corpus that locks them in). Ship D in the same PR or a one-line follow-up.

---

## Counter-arguments considered

### Rejected: making evidence_grounding (or runtime_check) a hard veto (any 0.5 → ESCALATE / reject)

Too strong. The calibrator legitimately cannot always execute reproducers; vetoing on 0.5 would block every Tier 1 calibration. The gated-minimum + 0.30 buffer preserves Tier 1 utility while killing the 0.90 dilution. Caps at 0.80 — below the 0.85 STOP gate — which is exactly the behavior we want.

### Rejected: giving the calibrator Bash to close the structural blindness

Symptom-solver. Granting Bash to a Read-only-by-design agent is RCE-equivalent risk (the calibrator would execute commands cited in untrusted hypothesis cards). Cleaner separation: calibrator scores the runtime gap honestly via Runtime check; the Wave-0 orchestrator already runs `git show` / reproducer commands per `REPORT.md:114-116`. The proposal makes that out-of-band workaround in-band by giving the orchestrator's executed reproducers a place to land (as `executed_reproducer` evidence items that the calibrator scores).

### Rejected: V2's mandatory `verdict_direction` + reject-malformed v1.0 cards

Migration cost too high for the marginal safety gain. Every in-flight pr86-style card would invalidate. V1.5's safe-default approach (calibrator defaults to AFFIRM / runtime_behavior with explicit Notes) preserves backward-compat. Mandatory schema ships in v2.0 once v1.5 has been live long enough that no v1.0 cards remain.

### Rejected: V2's schema v2.0 redesign (typed evidence-kind table as MANDATORY) in this commit

Same migration-cost reason. The typed table ships as an *optional recommended shape* in v1.5 (Change B's "Recommended evidence shape (v2.0 preview)" subsection). Mandatory in v2.0.

### Rejected: V2's structural input-filter for self-reported confidence (M3c full closure)

Requires orchestrator-side byte-preprocessing of the calibrator's Read input. V2 itself flags this as out-of-scope. Prompt-level Independence Instruction (Change C) + P5 anchoring property test (Change E) is the v1.5 prevention; structural masking is a v2.0 follow-up.

### Rejected: dual-calibrator-instance dispatch (take-the-minimum for M3c)

~2× token cost for a 0.45-likelihood cause. P5 anchoring property test detects drift in CI at a fraction of the cost. Defer until P5 shows the placebo risk materializing.

### Rejected: V3's Change 6 (pytest harness invocation)

Brainstorm deliverable is markdown-only. The pytest harness invoking the calibrator-eval-cases lives in `tests/troubleshoot/` and is the implementation commit's responsibility. Marked as "Implementation hook (deferred to follow-up commit)" in Change E.

---

## Regression tests / eval-suite additions

**Change E IS the eval-suite addition.** Specifically:

- 6 fixture hypothesis cards (`fixture-h3-style.md`, `fixture-pr86-rca-style.md`, `fixture-static-defect-clean.md`, `fixture-sha-pinned.md`, `fixture-v1-legacy-card.md`, `fixture-refute-runtime-verified.md`) with expected calibrated scores
- 5 property tests (P1 M1 gate, P2 M2 gate, P3 M3a cap, P4 determinism, P5 anchoring-variance)
- Suite-integrity rule: run on every PR touching `escalation-rubric.md`, `confidence-calibrator.md`, `hypothesis-card-template.md`, or `confidence-check/SKILL.md`

**Implementation hook (deferred)**: `tests/troubleshoot/test_calibrator_eval_cases.py` (pytest module). Out of scope for this markdown proposal; ships in the implementation commit.

**Forward-compat extension**: add fixtures for v2.0 evidence-kind validation (`source_citation` / `executed_reproducer` / `test_assertion` typed table mandatory) when the v2.0 schema ships.

---

## Migration / backward-compat note

| Concern | v1.5 Behavior |
|---------|---------------|
| In-flight cards without `Claim class` frontmatter | Calibrator defaults to `runtime_behavior` (fail-safe). Recorded in Notes. Old cards may score lower than they did under the 5-dim mean — this is the intended correction. |
| In-flight cards without `Verdict direction` | Calibrator defaults to `AFFIRM`. Recorded in Notes. Preserves backward-compat; v2.0 will require explicit declaration. |
| In-flight cards without `Runtime check` self-assessment | Calibrator scores Runtime check = 0.0 (no evidence is no evidence). For `claim_class: static_defect` (default upon missing or explicit), Runtime check inherits Evidence grounding — so cards with strong source citations still pass. |
| Old calibration reports (e.g., `tier2-root-cause-analyst-calibration.md` in the pr86 substrate) | Schema additions are additive — the new `Runtime check` row + verdict-direction cap line + Stage-2 trace are new but do not break downstream parsers. Old reports remain readable; new reports carry strictly more information. |
| pr86's already-shipped calibration results | Optionally re-run with v1.5 rubric (yields lower scores for source-only runtime claims — intentional). Otherwise annotate old reports with `[calibrated under pre-M1+M2+M3a rubric; see new rubric for current scoring]`. |
| `confidence-check/SKILL.md`'s "Test Results 1.000/1.000" claim | Scoped via Change D — no behavioral impact. The claim still holds for its actual coverage (5 pre-implementation checks). |
| The optional typed evidence table in Change B | Card authors may opt in or stay on the bulleted-list form in v1.5. No calibrator-side validation of the typed table in v1.5. v2.0 will require it. |

---

## Provenance

Per-section sources (per V2's input-bias requirement that the merge be auditable):

- §Scope — V1 base; pin-test corpus added per V3 Change 5
- §Change A — V1 §"Change 1"
- §Change B — V1 §"Change 2" + V2 §"Recommended evidence shape" as optional subsection
- §Change C — V1 §"Change 3"
- §Change D — V3 §"Change 4"
- §Change E — V3 §"Change 5" + V2's Round 3 forward-compat note
- §Coverage matrix — synthesized from V1 + V3 matrices
- §Minimal-change subset — V1 §"Minimal-change subset" augmented with V3's Changes D+E as defense-in-depth
- §Counter-arguments — union of V1, V2, V3 rejections
- §Regression tests — V3 §"Change 5" with implementation-hook scope deferred per V3 Round 2 concession
- §Migration / backward-compat — V1 §"Migration" augmented with V2's v1.5 → v2.0 migration path
