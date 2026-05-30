<!-- Variant 1: opus:analyzer — minimal surgical fix; emphasize what NOT to change -->

# Variant 1 — Surgical-Minimum Refactor (opus:analyzer)

## Stance

Apply the smallest set of edits to three files (rubric, card template, calibrator) that mechanically closes M1+M2+M3a. Resist temptations to redesign the calibrator's invocation surface, add new agents, fork the card schema, or rewrite confidence-check SKILL.md. Every change must point at a specific named cause; everything else stays.

## Proposal

### Change 1 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`

**Section affected**: `## Confidence calibration (Wave 1.7)` — the dimension table at line 11-17 and the formula at line 19.

**Shape**: Add a 6th row to the table; replace line 19's formula; add a new subsection between `## Confidence calibration` and `## Escalation decision`.

**Diff sketch** (replace):

```diff
 | Dimension | 1.0 (strong) | 0.5 (partial) | 0.0 (weak) |
 |-----------|--------------|---------------|------------|
-| **Evidence grounding** | Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |
+| **Evidence grounding** | Cited `file:line` matches a real code path that exhibits the symptom (snippet match verified) | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |
 | **Symptom coverage** | ... | ... | ... |
 | **Reproducibility fit** | ... | ... | ... |
 | **Fix directness** | ... | ... | ... |
 | **Domain coherence** | ... | ... | ... |
+| **Runtime check** | Hypothesis includes an executed reproducer with captured stdout/stderr that reproduces the symptom; OR an asserted-by-test runtime invariant | Hypothesis includes a runnable command but no captured output; OR cites a test that exists but was not exercised at hypothesis time | Hypothesis is source-only — no executed reproducer, no test assertion. |

-**Confidence** = arithmetic mean of the five dimension scores.
+**Confidence** = `min(mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30 when claim_class=runtime_behavior)`.
+
+The first two terms apply unconditionally. The third term applies when the hypothesis card's frontmatter declares `claim_class: runtime_behavior`. The gated-minimum prevents a single 0.5 on either Evidence grounding (M1) or Runtime check (M2) from being averaged away by four prose-readable 1.0s.

+### Verdict-direction modifier (M3a)
+
+After computing the gated-minimum confidence, apply the verdict-direction modifier:
+
+| Verdict | `claim_class` | `runtime_check` | Cap |
+|---------|---------------|-----------------|-----|
+| REFUTE / REJECT | runtime_behavior | < 1.0 | calibrated ≤ 0.70 |
+| AFFIRM | runtime_behavior | < 1.0 | calibrated ≤ 0.84 |
+| (any) | static_defect | (any) | no cap |
+
+Rationale: a wrong REFUTE on runtime behavior closes the investigation door (the H3 case); a wrong AFFIRM gets caught by CI. Source-only REFUTEs of runtime claims are precisely the failure mode under repair and must not clear the 0.85 STOP gate.
```

**Escalation Decision section** — add one rule before "Default":

```diff
 3. **Signal-driven escalation** (any one triggers escalation)
    - `confidence < 0.85` → ESCALATE (`escalation_reason: low_confidence`).
    ...
+   - `claim_class == runtime_behavior` AND `runtime_check < 0.5` → ESCALATE (`escalation_reason: source_only_runtime_claim`).
```

### Change 2 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md`

**Section affected**: frontmatter list (lines 12-16) and "Per-dimension self-assessment" block (lines 48-53).

**Shape**: Add `Cause class → Claim class`-adjacent `claim_class` field to frontmatter (DO NOT rename Cause class; keep it). Add `Runtime check` to per-dimension self-assessment. Append a `Falsification standard` section (M3b — cheap, ships in the same edit).

**Diff sketch**:

```diff
 **Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">
+**Claim class**: `static_defect` | `runtime_behavior` | `environment_dependent`
+  — `static_defect`: source-reading alone is sufficient evidence (typos, missing imports, regex literals)
+  — `runtime_behavior`: claim depends on dynamic control flow, side effects, or executed semantics
+  — `environment_dependent`: claim depends on OS/runtime/feature-flag/network state
 **Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>
```

```diff
 Per-dimension self-assessment:
 - Evidence grounding: <0.0|0.5|1.0> — <one-line reason>
+- Runtime check: <0.0|0.5|1.0> — <one-line reason; cite reproducer command + captured output, OR mark as N/A only if claim_class=static_defect>
 - Symptom coverage: <0.0|0.5|1.0> — <one-line reason>
 - Reproducibility fit: <0.0|0.5|1.0> — <one-line reason>
 - Fix directness: <0.0|0.5|1.0> — <one-line reason>
 - Domain coherence: <0.0|0.5|1.0> — <one-line reason>
```

Append new section after "If I'm wrong, it's probably because…":

```diff
+## Falsification standard
+
+One sentence: what concrete evidence (executed command, captured output, test result, log line, log absence) would prove this hypothesis wrong? If the answer is "nothing concrete — only re-reading the source differently", the claim_class is runtime_behavior and runtime_check should self-score ≤ 0.5.
```

### Change 3 — `src/superclaude/agents/confidence-calibrator.md`

**Sections affected**: `## Responsibilities` (lines 48-54) — reflect the 6th dimension and new formula. `## Output Format` table — add Runtime check row, and a `## Claim-class handling` subsection between Independence Instruction and Inputs.

**Shape**: Replace step-1 and step-5 in Responsibilities; insert claim-class handling subsection; extend the per-dimension table in Output Format.

**Diff sketch**:

```diff
 ## Responsibilities

-1. **Read the rubric** at `rubric_path`. Note the 5 dimensions: Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
+1. **Read the rubric** at `rubric_path`. Note the 6 dimensions: Evidence grounding, Runtime check, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
 2. **Read the card** at `card_path`.
+2a. **Read the card's `claim_class` frontmatter field.** If absent, default to `runtime_behavior` (fail-safe: assume runtime semantics matter until proven otherwise). Record the resolved value in your report's Notes section.
 3. **Spot-check the evidence** ...
-4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. Cite the specific card content (or absence thereof) that drove the score.
-5. **Compute the arithmetic mean**, rounded to 2 decimals.
+4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. For Runtime check: score honestly even though you have only `tools: Read`. If the card cites no executed reproducer and no asserted-by-test invariant, Runtime check = 0.0 (no leniency for "I read the code carefully"). 0.5 requires a runnable command in the card without captured output. 1.0 requires captured stdout/stderr OR a green test asserting the runtime invariant.
+5. **Compute calibrated confidence** using the rubric's gated-minimum formula: `min(mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30 when claim_class=runtime_behavior)`. Round to 2 decimals.
+5a. **Apply the verdict-direction modifier** per the rubric: source-only REFUTEs of runtime claims cap at 0.70; source-only AFFIRMs cap at 0.84.
 6. **Apply the escalation decision rules** ...
```

Append new subsection after `## Independence Instruction`:

```diff
+## Claim-class handling
+
+The card declares its `claim_class` in frontmatter. You do not redetermine it (that would invite anchoring on whether you *can* verify it with Read alone). Trust the card's declaration, with one exception: if `claim_class: static_defect` is declared but the card's claim references dynamic control flow ("falls through to", "the runtime would", "after the side effect"), flag this in Notes and treat the card as `claim_class: runtime_behavior` for scoring. Surface the discrepancy.
+
+Why this matters: the failure mode under repair is calibrators scoring runtime-behavior claims at 0.85+ on source-only evidence (`tools: Read` cannot execute). The claim_class declaration + Runtime check dimension makes the structural inadequacy of source-only evidence visible at the dimension level rather than hidden inside Evidence grounding's old OR-clause.
```

Extend the per-dimension table in `## Output Format`:

```diff
 | Dimension | Score | Justification (cite card content) |
 |-----------|-------|-----------------------------------|
 | Evidence grounding | 1.0 / 0.5 / 0.0 | <one-line citing what in the card supports this> |
+| Runtime check | 1.0 / 0.5 / 0.0 | <cite the executed-reproducer block in the card, or its absence> |
 | Symptom coverage | ... | ... |
 | Reproducibility fit | ... | ... |
 | Fix directness | ... | ... |
 | Domain coherence | ... | ... |

+## Confidence

+- **Self-reported (in card)**: <X.XX>
+- **Calibrated (this report)**: <Y.YY>
+- **Formula applied**: `min(mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30 if runtime_behavior)`
+- **Verdict-direction cap**: <"none" | "REFUTE+runtime cap 0.70" | "AFFIRM+runtime cap 0.84">
+- **Delta**: <signed difference, and a one-line read on why it differs>
```

## What I am explicitly NOT changing

- `src/superclaude/skills/confidence-check/SKILL.md` — this skill is the *pre-implementation* confidence skill, separate from the troubleshoot calibrator chain. M2's evidence cites it as a *cultural* prior, but the H3/pr86 calibration miss runs entirely through the escalation-rubric + calibrator agent. Touching confidence-check expands surface area without closing a unanimous cause. Leave it for a follow-up if M4 pin tests surface drift.
- Calibrator's `tools: Read` constraint — the structural blindness IS real, but giving the calibrator Bash invites a different failure mode (calibrator executes user code in untrusted contexts). The Runtime check dimension and the gated-minimum together force the calibrator to *score* the runtime gap honestly; they do not require the calibrator to *close* it. The orchestrator/Wave 0 verifier is the right layer for execution.
- Card template's "Cause class" field — orthogonal to claim_class. Keep both.
- The 5-criterion confidence-check (pre-implementation) percentages — unrelated.

## Coverage matrix

| Cause | Change 1 (rubric) | Change 2 (card) | Change 3 (calibrator) | Closes? |
|-------|-------------------|-----------------|------------------------|---------|
| M1 (mean dilution) | gated-min formula | — | applies formula | **closes** |
| M2 (source-vs-runtime conflation) | 6th dim Runtime check + tightened Evidence grounding anchor | claim_class + Runtime check self-assessment | scores Runtime check; treats claim_class as input | **closes** |
| M3a (verdict-direction) | verdict-direction modifier table | — | applies modifier | **closes** |
| M3b (falsification standard) | — | Falsification standard field added | — (calibrator reads it indirectly via Runtime check evidence) | **partially closes** (field exists; calibrator doesn't yet *score* it directly) |
| M3c (anchoring) | — | — | — | **n/a** (rejected — dual-instance dispatch is too expensive for the marginal 0.45 likelihood) |
| M4 (silent-green eval) | — | — | — | **n/a** (rejected from this minimal set; pin tests are a separate eval-suite change) |

## Minimal-change subset closing M1+M2+M3a

**All three changes are required and minimal**:
- Change 1 alone (rubric): closes M1 mathematically but the card has no slot for runtime_check; calibrator has no instruction to score it.
- Change 2 alone (card): exposes claim_class + Runtime check field but rubric still averages it into the old mean; verdict-direction modifier still absent.
- Change 3 alone (calibrator): can't apply a formula that isn't in the rubric and can't read a field that doesn't exist on the card.

These three files are **compositional, not exchangeable**.

## Counter-arguments considered

- **Rejected: "Make evidence_grounding a veto (any 0.5 → reject hypothesis)."** Too strong. The calibrator legitimately can't always verify; vetoing on 0.5 would block every Tier 1 calibration where the calibrator lacks Bash. The gated-minimum + 0.30 buffer preserves Tier 1 utility while killing the 0.90 dilution.
- **Rejected: "Give the calibrator Bash and remove the structural blindness."** Solves the symptom but introduces RCE-equivalent risk inside a Read-only agent. Cleaner separation: calibrator scores honestly; Wave-0 orchestrator (which already runs `git show` per `REPORT.md:114-116`) handles execution.
- **Rejected: "Spawn two calibrator instances per card, take the min (M3c fix)."** ~2× token cost for a 0.45-likelihood cause. Defer unless M4 pin tests show the placebo risk materializing.
- **Rejected: "Rewrite confidence-check/SKILL.md to add a runtime-verification check."** Wrong layer. confidence-check is pre-implementation; the calibration miss is mid-investigation. Touching SKILL.md without touching the calibration chain doesn't close M1/M2/M3a.

## Regression tests / eval-suite additions

Add to calibrator eval suite (a single new ref file, e.g. `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` or a directory of fixture cards):

1. **Pin test "source-only runtime claim"**: hypothesis card with claim_class=runtime_behavior, runtime_check=0.0, four other dims=1.0. Expected calibrated ≤ 0.30+0.30 = 0.60. Assertion: `calibrated < 0.85` always.
2. **Pin test "static_defect with strong evidence"**: claim_class=static_defect (e.g., the eval_run.py `Path` import), evidence_grounding=1.0, runtime_check=0.5 (no reproducer but the static analysis IS the runtime here). Expected calibrated ≥ 0.85.
3. **Pin test "REFUTE+runtime cap"**: verdict=REFUTE, claim_class=runtime_behavior, runtime_check=0.5, mean=0.85 → expect calibrated capped at 0.70.
4. **Pin test "sha-pinned citation"**: card cites `commit-sha:file:line`. Expected: calibrator flags in Notes that the citation is structurally unverifiable from current HEAD and Runtime check ≤ 0.5.
5. **Property test**: `evidence_grounding ≤ 0.5` → calibrated ≤ 0.85 for any combination of other scores and any claim_class.

These are M4's deliverable but they're cheap to ship in the same commit as Changes 1-3.

## Migration / backward-compat note

- **In-flight cards without `claim_class`**: calibrator defaults to `runtime_behavior` (fail-safe). Old cards will score lower than they did under the 5-dim mean — that is the intended correction.
- **Old cards without `Runtime check` self-assessment**: calibrator scores Runtime check = 0.0 (no evidence is no evidence). Same direction of safety.
- **Old calibration reports**: schema is *additive* — `Runtime check` row + verdict-direction cap line are new but parseable downstream. No breaking change for /sc:troubleshoot's report-template.
- **Eval-suite Test Results claim** (`confidence-check/SKILL.md:14-18` "Precision 1.000 / Recall 1.000"): out of scope for this minimal-change subset. Mark as "stale claim — pending re-eval against M1+M2+M3a fixtures" in a follow-up commit.
