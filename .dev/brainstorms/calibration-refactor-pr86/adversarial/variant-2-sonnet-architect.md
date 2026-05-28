<!-- Variant 2: sonnet:architect — schema-redesign perspective; cleanest end-state -->

# Variant 2 — Schema-Redesign Refactor (sonnet:architect)

## Stance

A surgical patch closes the immediate failure, but the rubric's underlying schema has structural debt that will keep generating analogous misses. Treat the calibration apparatus as a contract between three artifacts (card schema, rubric scoring function, calibrator agent execution model) and redesign the contract with explicit typing of *claims* and explicit typing of *verdict cost*. Migration cost is higher; the end-state is cleaner and prevents not only M1/M2/M3a but the family of failures structurally similar to them.

## Proposal

### Change 1 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` (schema-level)

**Strategy**: Promote `claim_class` to a first-class frontmatter field with a closed vocabulary, AND restructure the evidence section to carry per-evidence-item *kind* tagging. Then per-dimension self-assessment becomes a derived view, not the source of truth.

**Shape**: Replace the frontmatter block (lines 12-16) and the `## Evidence` and `## Confidence` sections wholesale. Append `Falsification standard` (M3b) and `Runtime verification` (M2) as required sections.

**Diff sketch — frontmatter**:

```diff
 **Agent**: <agent-name>
 **Tier**: <1|2>
 **Timestamp**: <ISO 8601>
 **Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">
+**Claim class**: <static_defect | runtime_behavior | environment_dependent | composite>
+**Verdict direction**: <AFFIRM | REFUTE | REJECT>
+  — REFUTE/REJECT verdicts on `runtime_behavior` claims face a higher calibration bar (see escalation-rubric §Verdict-direction modifier).
+**Schema version**: 2.0
 **Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>
```

**Diff sketch — Evidence section**:

Replace the prose-bulleted evidence with a typed table:

```diff
-List 1–4 evidence items. **Each item must be either a `file:line` citation with a quoted snippet, or a command + actual output.** Speculation is not evidence.
-
-- `path/to/file.py:142` — `result = Path(scratch_root) / "foo"` (uses `Path` but no `from pathlib import Path` in the file's imports — verified by reading lines 1–20)
-- Command: `uv run python -c "from src.module import target"` → `NameError: name 'Path' is not defined`
-- `path/to/test_file.py:88` — the failing test that exercises this code path

+List 1-6 evidence items in the table below. Each item declares its kind so the calibrator can score Source-citation vs Runtime-verification independently. **Speculation, "I read it carefully", and re-statement of the symptom are not evidence — they are commentary.**
+
+| # | Kind | Source | Content |
+|---|------|--------|---------|
+| E1 | `source_citation` | `path/to/file.py:142` | `result = Path(scratch_root) / "foo"` — no `Path` import in lines 1-20 |
+| E2 | `executed_reproducer` | `uv run python -c "from src.module import target"` | `NameError: name 'Path' is not defined` (captured stdout/stderr) |
+| E3 | `test_assertion` | `tests/path/to/test_file.py::test_eval_run` | currently fails with the same NameError — green after fix |
+| E4 | `documentation` | `docs/python/pathlib.html#path` | `Path` requires `from pathlib import Path` |
+
+**Allowed kinds**:
+- `source_citation`: file:line + verified snippet. Sufficient evidence only for `static_defect` claims.
+- `executed_reproducer`: a runnable command with captured stdout/stderr. Required for `runtime_behavior` 1.0 scoring.
+- `test_assertion`: a named test (passing OR failing) that asserts the relevant invariant. Acceptable substitute for executed_reproducer when the test was actually run.
+- `documentation`: an authoritative doc / spec section. Supports `static_defect` and `environment_dependent` claims.
+- `log_artifact`: captured log lines or an output dump. Acceptable for `environment_dependent` claims with timestamps.
```

**Diff sketch — Confidence section**:

```diff
-Self-reported confidence: <0.0–1.0>
-
-The skill will re-grade this against the rubric. The agent's score is a signal, not the final number.
-
-Per-dimension self-assessment:
-- Evidence grounding: <0.0|0.5|1.0> — <one-line reason>
-- Symptom coverage: <0.0|0.5|1.0> — <one-line reason>
-- Reproducibility fit: <0.0|0.5|1.0> — <one-line reason>
-- Fix directness: <0.0|0.5|1.0> — <one-line reason>
-- Domain coherence: <0.0|0.5|1.0> — <one-line reason>

+Self-reported confidence: <0.0-1.0>
+
+The skill re-grades this against the rubric. **The agent's score is a signal that the calibrator is instructed NOT to read** (the calibrator agent's input filter masks this field — see confidence-calibrator.md §Anchoring defense). The dimension scores below are the only carriers.
+
+Per-dimension self-assessment:
+- Source citation: <0.0|0.5|1.0> — <which evidence items E? support this>
+- Runtime verification: <0.0|0.5|1.0> — <which executed_reproducer or test_assertion E? supports this; if claim_class=static_defect, may score N/A>
+- Symptom coverage: <0.0|0.5|1.0> — <one-line reason>
+- Reproducibility fit: <0.0|0.5|1.0> — <one-line reason>
+- Fix directness: <0.0|0.5|1.0> — <one-line reason>
+- Domain coherence: <0.0|0.5|1.0> — <one-line reason>
```

Append two required new sections:

```diff
+## Falsification standard
+
+The single most diagnostic piece of evidence that would prove this hypothesis wrong, in the form of a runnable command, expected output assertion, or named test outcome. "Re-reading the source" is not a falsification standard. If you cannot name a falsification standard, the claim_class is `runtime_behavior` and Runtime verification self-scores 0.0.

+## Runtime verification

+If `claim_class != static_defect`, this section is REQUIRED. State explicitly:
+- The command/test that was executed
+- The captured output (stdout/stderr/log) demonstrating the runtime behavior under the hypothesis
+- OR a one-sentence justification for why runtime verification is structurally impossible at hypothesis time (e.g. "requires production traffic")
+
+The calibrator scores Runtime verification 0.0 if this section is absent or contains only commentary.
```

### Change 2 — `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (rewrite of §Confidence calibration)

**Strategy**: Replace the 5-dim arithmetic-mean with a two-stage scoring function. Stage 1 produces a per-dimension vector; Stage 2 applies *guards* (gated-min for M1, claim-class gate for M2) and a *modifier* (verdict-direction for M3a).

**Diff sketch — Confidence calibration section**:

```diff
 ## Confidence calibration (Wave 1.7)

-The `root-cause-analyst` returns a self-reported confidence. The skill **re-grades** it against this rubric — agent confidence is not trusted directly.
-
-Score each dimension 0.0–1.0 and average.
-
-| Dimension | 1.0 (strong) | 0.5 (partial) | 0.0 (weak) |
-|-----------|--------------|---------------|------------|
-| **Evidence grounding** | Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |
-...
-
-**Confidence** = arithmetic mean of the five dimension scores.

+The `root-cause-analyst` returns a self-reported confidence. The skill **re-grades** it against this rubric using a two-stage scoring function that explicitly types the claim and the verdict cost.
+
+### Stage 1 — Dimension vector
+
+Score each of six dimensions 0.0 / 0.5 / 1.0. Source citation and Runtime verification are *independent* dimensions (Schema v2.0); they replace the v1.0 single "Evidence grounding" row.
+
+| Dimension | 1.0 (strong) | 0.5 (partial) | 0.0 (weak) |
+|-----------|--------------|---------------|------------|
+| **Source citation** | `source_citation` evidence item with verified snippet match (calibrator re-Read the cited file:line and confirms the snippet) | Cited file exists but the specific line/snippet is inferred, not verified | No real citation; pattern-matching prior bugs |
+| **Runtime verification** | `executed_reproducer` OR `test_assertion` evidence item with captured output reproducing the symptom under the hypothesis | Runnable command in card but no captured output; OR cited test exists but was not run at hypothesis time | Source-only — no executed reproducer, no test assertion. For `claim_class: static_defect` this dimension is auto-set to the value of Source citation (static defects' source IS their runtime). For `claim_class: runtime_behavior` and `environment_dependent`, source-only mandatorily scores 0.0. |
+| **Symptom coverage** | (unchanged from v1.0) |
+| **Reproducibility fit** | (unchanged from v1.0) |
+| **Fix directness** | (unchanged from v1.0) |
+| **Domain coherence** | (unchanged from v1.0) |
+
+### Stage 2 — Scoring function with guards and modifiers
+
+```
+raw_mean = mean(source_citation, runtime_verification, symptom_coverage, reproducibility_fit, fix_directness, domain_coherence)
+
+gated_min = min(
+    raw_mean,
+    source_citation + 0.30,                          # M1 gate
+    runtime_verification + 0.30,                     # M2 gate (always applies — no claim_class exemption)
+)
+
+if claim_class == "runtime_behavior" and runtime_verification < 1.0:
+    if verdict_direction in ("REFUTE", "REJECT"):
+        calibrated = min(gated_min, 0.70)            # M3a cap — REFUTE-wrong closes the door
+    elif verdict_direction == "AFFIRM":
+        calibrated = min(gated_min, 0.84)            # M3a cap — AFFIRM-wrong gets caught by CI
+else:
+    calibrated = gated_min
+```
+
+Round to two decimals.
+
+### Why these guards specifically
+
+- **+0.30 buffer**: lets a 0.5 dimension still average upward when the other five are 1.0, but caps it at 0.80 — *below* the 0.85 STOP gate, by design. A 0.0 dimension is hard-capped at 0.30.
+- **M2 gate has no claim_class exemption**: even `static_defect` claims see the Runtime verification gate. For static defects, runtime_verification auto-inherits source_citation, so the gate is satisfied iff the source citation was. This preserves the "source IS runtime" identity for static defects without requiring a separate code path.
+- **M3a cap asymmetry (0.70 vs 0.84)**: REFUTE/REJECT is the destructive verdict (the H3 0.95-REFUTE case); AFFIRM at 0.84 still triggers ESCALATE per the 0.85 threshold, which is the desired behavior — wrong-AFFIRM gets a second opinion via Tier 2, wrong-REFUTE structurally cannot close the door.
```

**Add Escalation Decision rule**:

```diff
 3. **Signal-driven escalation** (any one triggers escalation)
+   - `claim_class ∈ {runtime_behavior, environment_dependent}` AND `runtime_verification < 0.5` → ESCALATE (`escalation_reason: source_only_dynamic_claim`).
+   - `verdict_direction == REFUTE` AND `claim_class == runtime_behavior` AND `runtime_verification < 1.0` → ESCALATE (`escalation_reason: refute_runtime_unverified`).
    - `confidence < 0.85` → ESCALATE (`escalation_reason: low_confidence`).
    ...
```

### Change 3 — `src/superclaude/agents/confidence-calibrator.md`

**Strategy**: Make the calibrator schema-v2-aware. Add an explicit input filter that masks the card's self-reported confidence (M3c, cheap to ship in same edit). Add per-evidence-item kind validation. Add the two-stage scoring function as the canonical Responsibilities sequence.

**Diff sketch — Role & Independence (lines 21-25)**:

```diff
 ## Independence Instruction

-**Self-reported confidence on the card is a signal, not a number.** Treat it as part of the card's narrative, not as input to your score. If the card says "Confidence: 0.92" and the evidence chain is two cited lines and an unverified command, the dimension scores tell the truth and the average wins.
+**Self-reported confidence on the card is structurally masked from your input.** When you Read the card, treat the line beginning `Self-reported confidence:` as if it were `Self-reported confidence: [REDACTED]`. Do not reason about its value, do not let it influence your dimension scores. This is a defense against M3c residual anchoring; the dimension scores are the only signal you score.
+
+**Self-reported per-dimension scores are inputs to your judgment but not to your output.** Read them, then score independently. If you disagree, score what the evidence supports.
```

**Diff sketch — Responsibilities (lines 48-54)**:

```diff
 ## Responsibilities

-1. **Read the rubric** at `rubric_path`. Note the 5 dimensions ...
-2. **Read the card** at `card_path`.
-3. **Spot-check the evidence**: for each `file:line` cited in the card, Read the file ...
-4. **Score each dimension** 0.0 / 0.5 / 1.0 ...
-5. **Compute the arithmetic mean**, rounded to 2 decimals.
-6. **Apply the escalation decision rules** ...

+1. **Read the rubric** at `rubric_path`. Note Schema v2.0 dimensions: Source citation, Runtime verification, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
+2. **Read the card** at `card_path`. **Apply input filter**: treat the `Self-reported confidence:` line as REDACTED.
+3. **Resolve `claim_class` and `verdict_direction`** from frontmatter. If `claim_class` is absent → default to `runtime_behavior` (fail-safe). If `verdict_direction` is absent → reject the card with `status: malformed` (this field is now mandatory).
+4. **Spot-check the evidence**: for each evidence item, Read the cited file:line OR confirm the captured-output block is present. Validate the declared `kind` against the content (a `source_citation` row with no file:line → kind mismatch; an `executed_reproducer` row with no captured stdout/stderr → kind mismatch). Flag mismatches in Notes.
+5. **Score each dimension** per Stage 1 of the rubric. For Runtime verification under `claim_class: static_defect`, inherit the Source citation score (do not re-derive).
+6. **Compute calibrated confidence** per Stage 2 of the rubric: raw_mean, gated_min (M1+M2 gates), then verdict-direction cap (M3a) if applicable.
+7. **Apply the escalation decision rules** per the rubric § Escalation decision.
```

**Diff sketch — Output Format additions**:

```diff
+## Stage 2 trace (REQUIRED in calibration report)
+
+| Step | Value | Notes |
+|------|-------|-------|
+| raw_mean | <X.XX> | arithmetic mean of all six dimensions |
+| gate_M1 (source_citation + 0.30) | <X.XX> | applies always |
+| gate_M2 (runtime_verification + 0.30) | <X.XX> | applies always |
+| gated_min | <X.XX> | min of raw_mean and both gates |
+| verdict_cap_applied | <none | 0.70 (REFUTE+runtime) | 0.84 (AFFIRM+runtime)> | M3a |
+| **calibrated** | <X.XX> | final |
```

## Coverage matrix

| Cause | Card schema v2.0 | Rubric v2.0 (two-stage) | Calibrator v2.0 | Closes? |
|-------|------------------|--------------------------|------------------|---------|
| M1 (mean dilution) | typed evidence enables clean source vs runtime split | gated_min via Stage 2 | applies Stage 2 | **closes** |
| M2 (source-vs-runtime) | claim_class + typed evidence kinds + Runtime verification section | independent Runtime verification dim with no OR-clause | enforces kind validation; auto-derivation for static_defect | **closes** |
| M3a (verdict-direction) | verdict_direction in frontmatter | verdict-cap modifier in Stage 2 | applies cap | **closes** |
| M3b (falsification standard) | required section | (implicit — Runtime verification dim) | reads & validates the section exists | **closes** |
| M3c (anchoring) | self-reported confidence is a separate field | — | input filter masks the field at Read time | **closes** (low confidence — masking is best-effort; LLM might still notice) |
| M4 (silent-green eval) | — | — | — | **n/a** (eval-suite layer — see test additions below) |

## Counter-arguments considered

- **Rejected: "Stay surgical (Variant 1's three-edit shape)."** Acknowledged as the minimum; rejected as the *right* end-state. Variant 1's `claim_class` addition without typing the evidence items means the calibrator still has to *infer* whether each citation is source-only or runtime — exactly the inference the calibrator is bad at. Schema v2.0 makes the kind explicit at the data layer.
- **Rejected: "Add a fifth `claim_class` value `unknown` for messy real-world cards."** Tempting but creates a soft-default that swallows the failure mode. Mandatory frontmatter + calibrator rejects malformed cards is strictly safer.
- **Rejected: "Compute calibrated as raw_mean × evidence_grounding."** Mathematically elegant; rejected because the multiplicative form punishes static_defect cards (which legitimately have runtime_verification ≈ source_citation) too harshly. Gated-min with +0.30 buffer is the surgical scalpel.
- **Rejected: "Make Wave 0 orchestrator the source of truth for runtime verification, calibrator inherits."** This is what /sc:troubleshoot already does via `git show` (REPORT.md:114-116) — but it's an *out-of-band workaround*, not encoded in the rubric. Schema v2.0 brings it in-band: the orchestrator's executed reproducers become `executed_reproducer` evidence items the calibrator scores honestly.

## Regression tests / eval-suite additions

New file: `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` containing 5+ golden hypothesis cards with expected calibrated scores. Pin tests:

1. **`fixture-h3-style.md`** — REFUTE on a runtime claim, source-only. Expected calibrated ≤ 0.70 (M3a cap).
2. **`fixture-pr86-rca-style.md`** — AFFIRM on a runtime claim (the "F1→F3→F5 chain") with source_citation=1.0 and runtime_verification=0.5. Expected calibrated ≤ 0.80 (M2 gate + M3a cap).
3. **`fixture-static-defect-clean.md`** — missing import case. claim_class=static_defect, source_citation=1.0, runtime_verification auto-inherits 1.0. Expected calibrated ≥ 0.85.
4. **`fixture-malformed.md`** — verdict_direction missing. Expected: calibrator returns `status: malformed`.
5. **Property test**: for any input, `runtime_verification == 0.0 AND claim_class == runtime_behavior` → `calibrated ≤ 0.30 + 0.30 = 0.60` (gate_M2).
6. **Property test**: under verdict_direction=REFUTE+claim_class=runtime_behavior+runtime_verification<1.0, calibrated ≤ 0.70 always.

## Migration / backward-compat note

- **Schema v1.0 cards (legacy)**: calibrator detects absence of `Claim class` and `Verdict direction` frontmatter and rejects with `status: schema_v1_unsupported`. Orchestrator catches this and runs a one-time migration: infer `claim_class` from the card's Evidence section content (any `source_citation`-only evidence → `runtime_behavior` fail-safe; any `executed_reproducer` → `runtime_behavior` with the reproducer as evidence; pure-source claim about an import/regex/typo → `static_defect`). Migration produces a v2.0 card; the v1.0 calibration report is invalidated.
- **In-flight pr86 calibration cards**: `tier2-root-cause-analyst-calibration.md` and siblings will fail v2.0 schema validation. Orchestrator's options: (a) re-run calibration with migrated cards; (b) accept v1.0 results with a top-of-report annotation `[schema-v1 — calibrated under pre-M2-fix rubric; treat with caution]`. Choose (b) for already-shipped investigations, (a) for new ones.
- **Old eval-suite "Precision 1.000 / Recall 1.000" claim**: explicitly invalidated. Replace SKILL.md:14-18 with `Test Results: pending re-eval under Schema v2.0 (see refs/calibrator-eval-cases.md)`.
- **Self-reported confidence masking (M3c)**: best-effort; the calibrator's prompt instruction to treat the field as REDACTED is enforceable but not bulletproof. Schedule a follow-up that strips the field from the input bytes before the calibrator's Read returns (requires orchestrator-side preprocessing — out of scope here but flagged).
