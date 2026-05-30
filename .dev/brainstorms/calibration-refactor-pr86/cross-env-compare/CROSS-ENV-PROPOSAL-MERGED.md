<!-- Provenance: Cross-environment adversarial merge of two REFACTOR-PROPOSAL.md files -->
<!-- Base: V1 (pr86-substrate, this environment) — won debate at 0.876 vs V2's 0.845 -->
<!-- Merged in: V2 (T4-environment with original artifacts) — Change 4 (audit gate) + evidence_class taxonomy + WebFetch URL detection + real-card replay fixtures -->
<!-- Merge date: 2026-05-26 -->
<!-- Convergence: 1.00 — STRONG cross-environment agreement on root cause and 6th-dimension solution shape -->

# Cross-Environment Calibration Refactor Proposal — Merged

**Substrates compared**:

- V1 (base): `pr86-integration-contracts-20260526100600` (structurally analogous to H3 0.95-REFUTE miss; this environment)
- V2 (merged-in): original T4 artifacts (`t4-pane-title-20260526-101500`; other environment)

**Root-cause documents**:

- V1: `.dev/troubleshoot/pr86-integration-contracts-20260526100600/calibration-failure/FINAL-MERGED-CAUSES.md`
- V2: original T4 FINAL-MERGED-CAUSES (referenced indirectly via the V2 proposal)

**Failure mode under repair (merged)**:

1. Confidence calibrator can score a hypothesis card at ≥0.85 calibrated on source-only evidence for runtime-behavior claims (V1 framing — calibration-formula defect).
2. The calibrator may not be dispatched at all, causing self-reported confidence to pass through unguarded (V2 framing — audit-layer defect surfaced by missing `tier2-h*-calibration.md` artifacts in the original T4 run).

Both framings are now addressed.

## Scope

Markdown-only proposal. **6 in-scope changes** targeting `src/superclaude/` source-of-truth (NEVER `.claude/` — that is sync-dev output):

1. `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` — rubric formula + 6th dimension + verdict-direction modifier + claim_class × evidence_class cross-tab
2. `src/superclaude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` — `Claim class` + `Verdict direction` + `Evidence class` frontmatter; `Runtime check` self-assessment; `Falsification standard` required section
3. `src/superclaude/agents/confidence-calibrator.md` — Responsibilities updated to apply the new formula + modifier + claim-class handling + WebFetch URL spot-check note
4. `src/superclaude/skills/confidence-check/SKILL.md` — scope-correct the "Test Results 1.000/1.000" cultural-prior claim (5-line annotation)
5. NEW FILE: `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` — pin-test corpus (9 fixtures + 5 properties; 6 synthetic + 3 real-T4-replay) that gates future changes to files 1-3
6. **NEW** `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` — Tier 2 calibration-completeness gate (audit-layer; merged from V2) that catches calibrator non-execution

### File-path discipline note (V2 cross-environment finding)

V2's original proposal targeted `/config/.claude/skills/...` paths throughout. **Those paths are sync-dev output of `src/superclaude/` per CLAUDE.md ABSOLUTE RULE: Never Stage or Commit `.claude/` Contents.** All V2 contributions in this merged document have been migrated to the correct `src/superclaude/...` paths. This is a paste-error class fix at the file-path layer; V2's semantic content is sound.

---

## Change A — `src/superclaude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md`

[Provenance: V1 base; cross-tab table merged from V2]

**Section affected**: `## Confidence calibration (Wave 1.7)` — dimension table at lines 11-17 + formula at line 19. Add new subsection `### Verdict-direction modifier (M3a)` between calibration and escalation decision. Add new subsection `### Claim-class × evidence-class cross-tab` (merged from V2). Add one new rule under `## Escalation decision` § 3.

**Shape**: insert (6th dimension row, modifier subsection, cross-tab subsection, escalation rule) + replace (Evidence grounding 1.0 anchor, formula line).

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

+### Claim-class × evidence-class cross-tab [V2 merged]
+
+The Runtime check dimension score is derived from the (claim_class, evidence_class) pair declared in the card frontmatter:
+
+| claim_class \ evidence_class | runtime_repro | runtime_trace | log_evidence | source_static | doc_static | none |
+|------------------------------|---------------|---------------|--------------|---------------|------------|------|
+| `runtime_behavior`           | 1.0           | 1.0           | 0.5          | **0.0**       | **0.0**    | **0.0** |
+| `environment_dependent`      | 1.0           | 1.0           | 0.5          | **0.0**       | **0.0**    | **0.0** |
+| `static_defect`              | 1.0           | 1.0           | 1.0          | inherits EG   | inherits EG | 0.0  |
+| `doc_contract`               | 1.0           | 1.0           | 1.0          | 0.5           | 1.0        | 0.0  |
+| `config_value`               | 1.0           | 1.0           | 1.0          | inherits EG   | inherits EG | 0.0  |
+| `mixed`                      | min of the two component classes' scores                                                          |
+
+The bolded cells (0.0) trigger the verdict-direction modifier when the card's verdict is REFUTE/REJECT.

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

[Provenance: V1 base; `evidence_class` frontmatter field merged from V2 Change 1]

**Sections affected**: frontmatter block (lines 12-16), per-dimension self-assessment (lines 48-53), and append two new required sections after `## If I'm wrong, it's probably because…`.

**Shape**: insert (frontmatter fields, dimension row, Falsification section, Evidence-classification section, Runtime check section) — additive only; no replacement of existing required fields.

**Diff sketch — frontmatter** (merged: V1's claim_class + verdict_direction + V2's evidence_class):

```diff
 **Cause class**: <from triage-checklist.md, e.g. "Missing/wrong import">
+**Claim class**: `static_defect` | `runtime_behavior` | `environment_dependent` | `config_value` | `doc_contract` | `mixed`
+  — `static_defect`: source-reading alone is sufficient evidence (typos, missing imports, regex literals, syntax errors)
+  — `runtime_behavior`: claim depends on dynamic control flow, side effects, executed semantics, or library call dispatch
+  — `environment_dependent`: claim depends on OS / runtime / feature-flag / network / data state
+  — `config_value`: claim depends on configuration / settings / env vars
+  — `doc_contract`: claim depends on a documented contract (RFC, spec, README)
+  — `mixed`: spans more than one class
+**Evidence class**: `runtime_repro` | `runtime_trace` | `log_evidence` | `source_static` | `doc_static` | `none`
+  — `runtime_repro`: executed reproducer with captured stdout/stderr
+  — `runtime_trace`: live execution trace, debugger output, instrumentation log
+  — `log_evidence`: post-hoc log excerpt from the failing run
+  — `source_static`: source file Read + cited line (no execution)
+  — `doc_static`: documentation citation (no execution, no source)
+  — `none`: prose only / no evidence
+**Verdict direction**: `AFFIRM` | `REFUTE` | `REJECT`
+  — REFUTE/REJECT verdicts on `runtime_behavior` claims face a higher calibration bar (see escalation-rubric § Verdict-direction modifier).
 **Consistency with docs**: <aligned | conflicts | not_applicable | no_docs_found>
```

**Diff sketch — per-dimension self-assessment**:

```diff
 Per-dimension self-assessment:
 - Evidence grounding: <0.0|0.5|1.0> — <one-line reason>
+- Runtime check: <0.0|0.5|1.0> — <derived from (claim_class, evidence_class) cross-tab; cite the executed-reproducer command + captured output, OR cite a runtime-asserting test by name + its execution state. For claim_class=static_defect, mark "inherits Evidence grounding" with no further evidence required.>
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

+## Evidence classification [V2 merged]
+
+- **Claim class**: <one of the seven above> — <one-line reason>
+- **Evidence class**: <one of the six above> — <one-line reason>
+- **Runtime check performed?**: yes | no — <if no, one-line reason why not>
+- **If REFUTE verdict, coverage statement**: <which paths/files/conditions were inspected; explicitly name anything not inspected that could flip the verdict>
+
+Filling rule: an empty or "Not applicable" value on `evidence_class` is a defect; cards with `claim_class: runtime_behavior` AND `evidence_class ∈ {source_static, doc_static, none}` MUST self-cap their confidence at 0.65 in the per-dimension self-assessment and state the cap in the rationale.
```

**New optional section** (V1 base — typed evidence table, presented as recommended shape):

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

[Provenance: V1 base; WebFetch URL spot-check note merged from V2 hard-fail rule 4]

**Sections affected**: `## Independence Instruction` (lines 23-27); `## Responsibilities` (lines 48-54); `## Output Format` (lines 58-93). Insert new subsection `## Claim-class handling` between Independence Instruction and Inputs.

**Diff sketch — Responsibilities**:

```diff
 ## Responsibilities

-1. **Read the rubric** at `rubric_path`. Note the 5 dimensions: Evidence grounding, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
+1. **Read the rubric** at `rubric_path`. Note the 6 dimensions: Evidence grounding, Runtime check, Symptom coverage, Reproducibility fit, Fix directness, Domain coherence.
 2. **Read the card** at `card_path`.
+2a. **Resolve `claim_class`, `evidence_class`, and `verdict_direction` from frontmatter.** If `claim_class` is absent, default to `runtime_behavior` (fail-safe). If `evidence_class` is absent, default to `none`. If `verdict_direction` is absent, default to `AFFIRM`. Record all defaults in Notes (preserves backward-compat with v1.0 cards; v2.0 will require explicit declaration).
 3. **Spot-check the evidence**: for each `file:line` cited in the card, Read the file at that range and verify the snippet matches. This is essential to scoring "Evidence grounding" honestly. If a citation does not match, mark it in the Notes section and let that drive the Evidence grounding score.
+3a. **WebFetch URL detection** [V2 merged]: For any evidence citation that is a remote URL (e.g., `https?://(raw\.)?github(?:usercontent)?\.com/...`), mark `spot_check_unverifiable: <url>` in Notes per citation. Do NOT cap on this alone; surface the unverifiability so the user can act on it. This forces unverifiable cites into the calibration report rather than silently treating them as verified.
-4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. Cite the specific card content (or absence thereof) that drove the score.
-5. **Compute the arithmetic mean**, rounded to 2 decimals.
+4. **Score each dimension** 0.0 / 0.5 / 1.0 per the rubric's anchor language. For **Runtime check**: use the cross-tab table in the rubric to derive the score from (claim_class, evidence_class). 0.5 requires a runnable command in the card without captured output (overrides cross-tab when evidence_class=source_static + a command is present). For `claim_class: static_defect`, Runtime check inherits the Evidence grounding score.
+5. **Compute calibrated confidence** using the rubric's gated-minimum formula: `min(arithmetic_mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)`. Round to 2 decimals. Emit a **Stage-2 trace** in your report (see Output Format) showing each gate's value so the formula application is auditable.
+5a. **Apply the verdict-direction modifier** per the rubric: when `claim_class: runtime_behavior` and `runtime_check < 1.0`, cap calibrated at 0.70 (REFUTE/REJECT) or 0.84 (AFFIRM). Record whether the cap was binding in the Stage-2 trace.
 6. **Apply the escalation decision rules** (rubric § Escalation Decision, in order) using the score and the `flags_context`. Return the verdict (`STOP` or `ESCALATE`) and the matching `escalation_reason`. Note: the allowed-value set for `escalation_reason` is extended with `source_only_dynamic_claim`.
```

**Diff sketch — new subsection `## Claim-class handling`** (insert after Independence Instruction):

```diff
+## Claim-class handling
+
+The card declares `claim_class` and `evidence_class` in frontmatter. You read them but you do not redetermine them from scratch (that invites anchoring on whether you *can* verify the claim with Read alone). Trust the card's declaration with ONE exception: if `claim_class: static_defect` is declared but the card's claim references dynamic control flow ("falls through to", "the runtime would", "after the side effect", "dispatched via", "the helper actually returns"), flag the misdeclaration in Notes and score the card AS IF `claim_class: runtime_behavior`. Surface the discrepancy explicitly so the orchestrator can act on it.
+
+Why this matters: the failure mode under repair (Cause #2) is calibrators scoring runtime-behavior claims at 0.85+ on source-only evidence because the rubric's Evidence-grounding OR-clause permitted it. The `claim_class` + `evidence_class` fields + the Runtime check dimension cross-tab make the structural inadequacy of source-only evidence visible at the dimension level rather than hidden inside Evidence grounding's old OR-clause. Your job is to enforce the visibility, not to relitigate the claim_class declaration.
```

**Diff sketch — Output Format additions** (V1 base; unchanged):

```diff
 | Dimension | Score | Justification (cite card content) |
 |-----------|-------|-----------------------------------|
 | Evidence grounding | 1.0 / 0.5 / 0.0 | <one-line citing what in the card supports this> |
+| Runtime check | 1.0 / 0.5 / 0.0 | <derived from (claim_class, evidence_class) cross-tab; cite the executed-reproducer block or named test, or its absence; for claim_class=static_defect, note "inherits Evidence grounding"> |
 | Symptom coverage | ... |

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
+| spot_check_unverifiable | <list of URLs> | V2-merged WebFetch detection |

 ## Confidence
-- **Self-reported (in card)**: <X.XX>
+- **Self-reported (in card)**: <X.XX> — read but NOT used as input to your score (independence instruction)
 - **Calibrated (this report)**: <Y.YY>
+- **Formula applied**: `min(mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)` then verdict-direction cap if applicable
 - **Delta**: <signed difference, and a one-line read on why it differs>
```

---

## Change D — `src/superclaude/skills/confidence-check/SKILL.md` (cultural-prior correction)

[Provenance: V1 base only — V2's Change 5 rejected per refactor-plan; V1's narrower edit is the load-bearing fix]

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

**Rationale**: the unqualified "1.000 / 1.000" claim was the rhetorical engine of the cultural prior (Cross-mechanism implications ¶5 of FINAL-MERGED-CAUSES.md). Scoping the claim to its actual coverage kills the recursion of anti-pattern without changing any behavioral logic. 5 lines.

---

## Change E — NEW FILE: `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`

[Provenance: V1 base (Fixtures 1-6 + Properties P1-P5); V2 merged (Fixtures 7-9 replay real T4 cards)]

**Shape**: create. Pin-test corpus + property tests that gate any future change to Changes A-C + F.

**Content** (V1 base; new Fixtures 7-9 appended):

```markdown
# Calibrator Eval Cases

Golden hypothesis cards + expected calibrated scores. Run before any change to `escalation-rubric.md`, `confidence-calibrator.md`, `hypothesis-card-template.md`, or `sc-troubleshoot-protocol/SKILL.md` ships. A regression on any fixture or property test blocks merge.

## Synthetic fixtures (V1 base)

### Fixture 1 — `fixture-h3-style.md` (source-only runtime REFUTE)
Hypothesis card with `claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: REFUTE`, evidence_grounding=1.0, runtime_check=0.0 (cross-tab derived), four other dims=1.0.
**Expected calibrated**: ≤ 0.70 (M3a cap fires).
**Asserts**: M1 + M2 + M3a all closed in combination.

### Fixture 2 — `fixture-pr86-rca-style.md` (AFFIRM with structural truncation)
`claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: AFFIRM`, evidence_grounding=1.0, runtime_check=0.5 (runnable command in card without captured output), four other dims=1.0.
**Expected calibrated**: ≤ 0.80 (gate_M2 = 0.80).
**Asserts**: M1 + M2 closure below the 0.85 STOP gate.

### Fixture 3 — `fixture-static-defect-clean.md` (eval_run.py Path import case)
`claim_class: static_defect`, `evidence_class: source_static`, evidence_grounding=1.0, runtime_check inherits 1.0, four other dims=1.0.
**Expected calibrated**: 1.0. **Asserts**: refactor does NOT over-correct.

### Fixture 4 — `fixture-sha-pinned.md` (structurally unverifiable predicate)
Card cites `commit-sha-5a65c62:file:line`. `claim_class: static_defect`, evidence_grounding=0.5, runtime_check inherits 0.5.
**Expected calibrated**: ≤ 0.80 (gate_M1 = 0.80).

### Fixture 5 — `fixture-v1-legacy-card.md` (missing claim_class — migration)
v1.0 frontmatter with no `Claim class`, `Evidence class`, or `Verdict direction` fields.
**Expected behavior**: calibrator defaults claim_class to `runtime_behavior`, evidence_class to `none`, verdict_direction to `AFFIRM` (fail-safe), records in Notes, proceeds.
**Asserts**: backward-compat — v1.0 cards do not break the calibrator.

### Fixture 6 — `fixture-refute-runtime-verified.md` (legitimate REFUTE with strong runtime check)
`claim_class: runtime_behavior`, `evidence_class: runtime_repro`, `verdict_direction: REFUTE`, evidence_grounding=1.0, runtime_check=1.0, four other dims=1.0.
**Expected calibrated**: 1.0. **Asserts**: M3a cap does NOT fire when runtime_check=1.0.

## Real-card replay fixtures (V2 merged)

### Fixture 7 — `fixture-t4-h3-replay.md` [V2 merged]
Replays actual `tier2-h3-options-subcommand.md` from `t4-pane-title-20260526-101500`. Frontmatter retrofitted: `claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: REFUTE`.
**Expected calibrated**: ≤ 0.65 (per V2 rule 1) or ≤ 0.70 (per V1 M3a). Either is below 0.85. **Asserts**: the actual failing card cannot slip through after the refactor.

### Fixture 8 — `fixture-t4-h2-replay.md` [V2 merged]
Replays actual H2 card from T4. `claim_class: runtime_behavior`, `evidence_class: source_static` (WebFetch GitHub URLs), `verdict_direction: REFUTE`.
**Expected calibrated**: ≤ 0.70. Also triggers WebFetch unverifiability note. **Asserts**: source-only REFUTE on runtime claim is structurally caught.

### Fixture 9 — `fixture-t4-h1-no-overcorrect.md` [V2 merged]
Replays actual H1 card from T4 (0.82 self-reported CONFIRM with mixed source + log evidence). `claim_class: runtime_behavior`, `evidence_class: log_evidence`, `verdict_direction: AFFIRM`.
**Expected calibrated**: 0.70-0.85 range; NO hard cap fires. **Asserts**: legitimate CONFIRM cards with log evidence are NOT downgraded by the refactor.

## Property tests

| ID | Property | Assertion |
|----|----------|-----------|
| P1 | M1 gate | `evidence_grounding ≤ 0.5` ⟹ `calibrated ≤ 0.80` |
| P2 | M2 gate | `runtime_check ≤ 0.5 AND claim_class ∈ {runtime_behavior, environment_dependent}` ⟹ `calibrated ≤ 0.80` |
| P3 | M3a cap | `verdict_direction == REFUTE AND claim_class == runtime_behavior AND runtime_check < 1.0` ⟹ `calibrated ≤ 0.70` |
| P4 | Determinism | running calibrator on same card produces same calibrated score (±0.0) across N=5 runs |
| P5 | Anchoring (soft) | varying `Self-reported confidence:` from 0.30 to 0.99 must not change calibrated by more than ±0.05. **Soft assertion** (warn-only in CI). |

## Suite integrity

Run on every PR that touches:
- `escalation-rubric.md`
- `confidence-calibrator.md`
- `hypothesis-card-template.md`
- `confidence-check/SKILL.md`
- `sc-troubleshoot-protocol/SKILL.md` (V2-merged Change F)

A regression on any fixture or hard property (P1-P4) blocks merge. P5 warnings surface for triage.

## Implementation hook (deferred to follow-up commit)

Pytest harness invoking this corpus is OUT OF SCOPE for this brainstorm proposal. Expected landing path: `tests/troubleshoot/test_calibrator_eval_cases.py`.
```

---

## Change F — `src/superclaude/skills/sc-troubleshoot-protocol/SKILL.md` (Tier 2 audit-layer gate) [V2 MERGED — closes Cause #1]

[Provenance: V2 Change 4 — migrated from V2's wrong `/config/.claude/skills/...` path to the correct `src/superclaude/skills/...` SoT path]

**Section affected**: Wave 3 / Tier 2 fan-out section, after the calibrator dispatch step.

**Shape**: insert — new "Tier 2 calibration completeness gate" subsection.

**Diff sketch**:

```diff
+## Tier 2 calibration completeness gate (hard precondition for report publishing)
+
+After all Tier 2 hypothesis cards are written and the calibrator subagents have been dispatched, the orchestrator MUST verify on disk:
+
+- For every `tier2-h<N>-*.md` card written in this run's output directory, a sibling `tier2-h<N>-*-calibration.md` artifact MUST exist and parse as a Calibration Report (per the agent's Output Format).
+- If any sibling calibration artifact is missing or malformed, the orchestrator MUST NOT publish `REPORT.md` with the un-calibrated card's confidence. Instead:
+  - Log `calibration: missing` for each missing sibling in `audit.log` with the absolute card path.
+  - Re-dispatch the calibrator subagent for the missing card with the same inputs and a 2-minute extended timeout (one retry only).
+  - If retry still fails, write the card into `REPORT.md` with confidence force-degraded to `min(self_reported, 0.65)` and a `calibration_status: failed_to_calibrate` annotation on the card's REPORT.md entry. Self-reported confidence is NEVER passed through unmodified.
+
+Verification command (run before publishing): for each `tier2-h*.md` (excluding `*-calibration.md`), assert a matching `*-calibration.md` exists or apply the force-degrade path.
```

**Rationale**: The empirical fact from the original T4 run is that `tier2-*-calibration.md` artifacts were absent — the calibrator did not execute and the 0.95 / 0.85 self-reports passed through unguarded. **No formula refinement closes this; only an audit gate does.** This is the most-load-bearing V2 contribution and the largest cross-environment finding: pr86 substrate could not surface this defect because pr86's substrate was a structural analogue, not the original artifact set.

---

## Cause → Fix coverage matrix (merged)

| Cause | Change A (rubric) | Change B (card) | Change C (calibrator) | Change D (SKILL.md) | Change E (eval cases) | Change F (audit gate) | Closes? |
|-------|-------------------|-----------------|-----------------------|---------------------|-----------------------|----------------------|---------|
| **Cause #1** — Calibrator non-execution (T4 dominant) | — | — | — | — | — | **direct closure** | **closes (V2-merged)** |
| **M1/Cause #2 dilution** — arithmetic-mean (0.89) | gated-min formula | — | applies formula | — | P1 fixture+property | — | **closes + prevents regression** |
| **M2/Cause #2 evidence** — source-vs-runtime conflation (0.85) | 6th dim + cross-tab + tightened anchor | claim_class + evidence_class + Runtime check self-assessment + Falsification standard | scores Runtime check via cross-tab; claim-class handling; WebFetch URL note | scopes cultural-prior "1.000/1.000" claim | P2 fixture+property | — | **closes + prevents regression** |
| **M3a/Cause #3** — Verdict-direction asymmetry (0.78) | verdict-direction modifier | verdict_direction frontmatter | applies modifier | — | P3 fixture+property | — | **closes + prevents regression** |
| **M3b** — Falsification standard (0.65) | — | Falsification standard required section | reads it via Runtime check evidence | — | (implicit — fixtures 1, 2, 6 exercise it) | — | **partially closes** |
| **M3c** — Residual anchoring (0.45) | — | — | Independence Instruction tightened | — | P5 anchoring property test (soft) | — | **partially closes** |
| **M4/Cause #4** — Eval-suite silent-green (0.68) | — | — | — | scopes the "1.000/1.000" claim | **direct closure — Change E IS the deliverable** | — | **closes + prevents regression** |

---

## Minimal-change subset

**The minimum subset closing M1 + M2 + M3a + Cause #1**: **Changes A + B + C + F**.

- Change A alone closes M1 mathematically but the card has no slot for runtime_check / evidence_class; calibrator has no instruction to score it.
- Change B alone exposes claim_class + evidence_class + Runtime check field but the rubric still averages it into the old mean; verdict-direction modifier still absent.
- Change C alone cannot apply a formula that isn't in the rubric and cannot read fields that don't exist on the card.
- **Change F alone closes Cause #1 (the dominant defect from the T4 original)** but does nothing about source-only runtime REFUTEs that DO get calibrated.

These four are **compositional, not exchangeable** — applying any subset alone underfits the failure mode. **Both environments converged on A + B + C as the calibration-formula minimum subset; V2's T4-original framing added F as the audit-layer requirement.**

**Changes D + E** are defense-in-depth:
- **D** kills the cultural-prior recursion (~5 lines)
- **E** prevents silent regression of A-D + F (recursion-of-anti-pattern prevention)

**Recommended PR shape**: Ship A + B + C + E + F in one PR. Ship D in the same PR or as a one-line follow-up.

---

## Cross-environment refactor synthesis

This section surfaces what the merge revealed about the relative strengths of the two substrate environments.

### File-edit convergence (STRONG)

Both environments independently proposed edits to:

- `escalation-rubric.md` (Change A / Change 2): add 6th dimension. **Both agreed structurally** — disagree only on the dimension's name and aggregation mechanic.
- `hypothesis-card-template.md` (Change B / Change 1): add typed frontmatter for claim/evidence classification. **Both agreed structurally** — V1 used 3 enums (claim_class + verdict_direction), V2 used 2 enums (claim_class + evidence_class). Merged: all three enums.
- `confidence-calibrator.md` (Change C / Change 3): teach the calibrator to apply the new rule. **Both agreed structurally** — differ on rule shape (V1's gated-minimum vs V2's three named caps).
- `confidence-check/SKILL.md` (Change D / Change 5): touch this file. **Differ on intent** — V1 corrects the cultural-prior claim; V2 adds a 6th check. Merged kept V1's narrower edit (rejected V2's Change 5 per debate scoring).

### Minimum-subset convergence (MODERATE-to-STRONG)

- Both environments converged on the **A + B + C** triple as the calibration-formula minimum.
- V1's substrate **could not see** Cause #1 (calibrator non-execution) because pr86's substrate was a structural analogue with calibrator artifacts; V2's T4 original substrate **did see** Cause #1 because the artifacts were missing.
- This is the largest substrate-driven divergence: V1's minimum is 3 changes (A+B+C); V2's minimum is 4 changes (1+2+3+4). Merged: 4 changes (A+B+C+F).

### Edits unique to each environment

| Edit                                                            | Source | Why unique to this environment                                                                                                                                                           |
| --------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Change E (pin-test corpus + 6 synthetic fixtures + 5 properties) | V1     | Pr86 substrate's structural-analogue framing made the regression-prevention need visible; V2 used one-off replay tests instead of building a permanent corpus.                              |
| Change F (Tier 2 audit gate)                                    | V2     | Only T4's original artifacts surfaced the missing-calibration-artifact pattern. V1's substrate had calibrator artifacts present, so the gate-need was invisible.                            |
| Migration / backward-compat table                                | V1     | V1's substrate had downstream consumers in mind (pr86's existing calibration reports); V2's framing was forward-only.                                                                       |
| Hard-fail rule 4 (WebFetch URL detection)                        | V2     | T4's H2 card had GitHub WebFetch URLs as evidence; V1's pr86 substrate's evidence was local file:line citations only.                                                                       |
| Real-card replay tests (V1-V5)                                   | V2     | T4 environment had the cards; pr86 substrate didn't.                                                                                                                                       |

### Counter-arguments agreement

Both environments **rejected**:

- Giving the calibrator Bash (RCE risk; both agreed Read-only).
- Hard-veto on a single dimension (too strong; both preferred composite caps).

Both environments **silently agreed** (no contradictory counter-arg) on:

- 6th dimension is the right place for the runtime-vs-static enforcement.
- The frontmatter must expose claim_class as a typed field.

### Test/eval-suite additions comparison

| Test artifact            | V1                              | V2                                                       | Merged                                |
| ------------------------ | ------------------------------- | -------------------------------------------------------- | ------------------------------------- |
| Synthetic fixtures       | 6 (Change E)                    | 0                                                        | 6 (kept from V1)                      |
| Property tests           | 5 (P1-P5)                       | 0                                                        | 5 (kept from V1)                      |
| Real-card replay         | 0                               | 5 (V1-V5: H1, H2, H3, audit-gate test, confidence-check) | 3 fixtures (7-9) + audit-gate in Ch F |
| Permanent eval corpus    | YES (calibrator-eval-cases.md)  | NO                                                       | YES (kept from V1, extended)          |
| Audit-gate verification  | NO                              | YES (V4 test in V2)                                      | YES (covered by Change F's verification command) |

### Implementation order

Both environments sequence the edits compatibly:

1. **First**: rubric (Change A / Change 2) — defines the contract.
2. **Second**: card template (Change B / Change 1) — provides the fields the rubric reads.
3. **Third**: calibrator (Change C / Change 3) — applies the rubric.
4. **Fourth (V2 only)**: audit gate (Change F) — protects against calibrator non-execution.
5. **Last**: eval corpus (Change E, V1 only) — locks in the above.

The merged order is identical to V1 with Change F inserted between calibrator and eval-corpus.

### Convergence verdict: **STRONG**

Both environments independently identified the same failure-mode shape (runtime-vs-static evidence conflation on REFUTE-direction hypothesis cards), proposed the same enforcement point (6th dimension on the escalation rubric), and arrived at largely compatible solutions. The divergence is entirely substrate-driven:

- V1 (pr86 structural analogue) optimized for calibration-formula correctness + regression prevention.
- V2 (T4 original) optimized for audit-layer enforcement + real-card validation.

Neither environment was complete alone. The merged proposal is strictly stronger than either input.

---

## Counter-arguments considered (merged from both environments)

### Rejected: making evidence_grounding (or runtime_check) a hard veto (any 0.5 → ESCALATE / reject) [V1]

Too strong. The calibrator legitimately cannot always execute reproducers; vetoing on 0.5 would block every Tier 1 calibration. The gated-minimum + 0.30 buffer preserves Tier 1 utility while killing the 0.90 dilution. Caps at 0.80 — below the 0.85 STOP gate — which is exactly the behavior we want.

### Rejected: giving the calibrator Bash to close the structural blindness [V1 + V2 implicit agreement]

Symptom-solver. Granting Bash to a Read-only-by-design agent is RCE-equivalent risk (the calibrator would execute commands cited in untrusted hypothesis cards). Cleaner separation: calibrator scores the runtime gap honestly via Runtime check; the Wave-0 orchestrator already runs reproducer commands.

### Rejected: V2's mandatory `verdict_direction` + reject-malformed v1.0 cards [V1]

Migration cost too high for the marginal safety gain. Every in-flight pr86-style card would invalidate. V1.5's safe-default approach (calibrator defaults to AFFIRM / runtime_behavior with explicit Notes) preserves backward-compat. Mandatory schema ships in v2.0.

### Rejected: V2's hard-cap "override the arithmetic mean entirely" [merged decision]

V1's gated-minimum (`min(mean, gate1, gate2)`) preserves the mean's information content; V2's "if alignment=0.0, cap=0.65 regardless of mean" discards it. Both approaches cap H3 below 0.85; V1's is more auditable. **Choice is on auditability grounds, not correctness.**

### Rejected: V2's Change 6 (modify confidence.ts code) [merged decision]

Brainstorm proposal is Markdown-only per V1's stated scope. The code change is implementation; it should land in a follow-up commit alongside V1's deferred pytest harness for Change E. V2's intent is sound; the timing is wrong for a brainstorm deliverable.

### Rejected: V2's hard-fail rule 2 (REFUTE > sibling CONFIRM wave-relative smell) [merged decision]

V1's verdict-direction modifier (M3a) achieves the same outcome (caps REFUTE on runtime claims at 0.70) without needing wave-sibling context. V2 itself acknowledged the fallback path when `wave_siblings` is unavailable. V1's rule is structurally self-contained.

### Rejected: V2's hard-fail rule 5 (negative-existential REFUTE regex detection) [merged decision]

Regex on natural-language phrasing is fragile. V1's verdict-direction modifier achieves the equivalent cap structurally. If V2's specialized detection proves necessary, it can be added as a follow-up.

### Rejected: V2's Change 5 (add 6th check to confidence-check SKILL.md with weight rebalance) [merged decision]

V1's Change D (scope-correct the "1.000/1.000" cultural-prior claim) is the load-bearing fix for the confidence-check skill. V2's 6th check duplicates the rubric's Runtime check dimension and would create maintenance drift between two enforcement points covering the same predicate. V1's narrower edit kills the rhetorical recursion at the source.

### Rejected: dual-calibrator-instance dispatch (take-the-minimum for M3c) [V1]

~2× token cost for a 0.45-likelihood cause. P5 anchoring property test detects drift in CI at a fraction of the cost.

### Rejected: V3's Change 6 (pytest harness invocation) [V1]

Brainstorm deliverable is markdown-only. The pytest harness lives in `tests/troubleshoot/` and is the implementation commit's responsibility. Marked as "Implementation hook (deferred to follow-up commit)" in Change E.

---

## Migration / backward-compat note (V1 base; extended with V2 audit-gate)

| Concern | v1.5 Behavior |
|---------|---------------|
| In-flight cards without `Claim class` frontmatter | Calibrator defaults to `runtime_behavior` (fail-safe). Recorded in Notes. |
| In-flight cards without `Evidence class` frontmatter [V2 merged] | Calibrator defaults to `none`. Recorded in Notes. |
| In-flight cards without `Verdict direction` | Calibrator defaults to `AFFIRM`. Recorded in Notes. |
| In-flight cards without `Runtime check` self-assessment | Calibrator derives from (claim_class, evidence_class) cross-tab. No fallback to old mean. |
| Old calibration reports (e.g., `tier2-root-cause-analyst-calibration.md`) | Schema additions are additive; new rows don't break downstream parsers. |
| pr86 / T4's already-shipped calibration results | Optionally re-run with v1.5 rubric (yields lower scores for source-only runtime claims — intentional). Otherwise annotate old reports with `[calibrated under pre-M1+M2+M3a rubric]`. |
| `confidence-check/SKILL.md`'s "Test Results 1.000/1.000" claim | Scoped via Change D — no behavioral impact. |
| The optional typed evidence table in Change B | Card authors may opt in or stay on the bulleted-list form in v1.5. v2.0 will require it. |
| Existing troubleshoot runs without calibration artifacts [V2 merged] | Change F's audit gate force-degrades to min(self_reported, 0.65) on first run after v1.5 lands. Existing reports unchanged. |

---

## Provenance (per-section sources)

- §Scope — V1 base; Change F added per V2 Change 4
- §Change A — V1 §"Change A"; cross-tab table merged from V2 §"How the calibrator must use it"
- §Change B — V1 §"Change B"; `evidence_class` frontmatter + Evidence-classification section merged from V2 §"Change 1"
- §Change C — V1 §"Change C"; WebFetch URL note merged from V2 §"Hard-fail rule 4"
- §Change D — V1 §"Change D" only (V2's Change 5 rejected per refactor-plan §"Rejected: V2's Change 5")
- §Change E — V1 §"Change E"; Fixtures 7-9 (real-T4-card replays) merged from V2 §"V1 / V2 / V3 verification tests"
- §Change F — V2 §"Change 4" (migrated from `.claude/` to `src/superclaude/` path per CLAUDE.md SoT rule)
- §Cause → Fix matrix — synthesized from V1 + V2 matrices; Cause #1 row added
- §Minimal-change subset — V1 base augmented with Change F per V2's T4-original framing
- §Cross-environment refactor synthesis — net-new merge-time analysis
- §Counter-arguments — union of V1, V2 rejections with merged decisions where applicable
- §Migration — V1 base augmented with V2 evidence_class + audit-gate rows
