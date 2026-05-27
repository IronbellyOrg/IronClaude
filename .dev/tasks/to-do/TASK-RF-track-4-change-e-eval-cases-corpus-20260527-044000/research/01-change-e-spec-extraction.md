# Research 01 — Change E Spec Extraction (Source Spec)

**Track:** 4 of 4 (Change E — NEW FILE: calibrator eval cases corpus)
**Researcher:** spec-extraction
**Status:** In Progress
**Date:** 2026-05-27
**Source:** `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` (main checkout)
**Scope:** L290-372 (Change E section); the full new-file content lives inline at L298-370 inside a markdown code fence.

---

## 1. Change E section header (proposal L290-296)

Quoted verbatim (proposal L290-296):

```
## Change E — NEW FILE: `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`

[Provenance: V1 base (Fixtures 1-6 + Properties P1-P5); V2 merged (Fixtures 7-9 replay real T4 cards)]

**Shape**: create. Pin-test corpus + property tests that gate any future change to Changes A-C + F.

**Content** (V1 base; new Fixtures 7-9 appended):
```

**Target path:** `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`
**Shape:** `create` (new file)
**Provenance:** V1 base for Fixtures 1-6 + Properties P1-P5; V2 merged appends Fixtures 7-9 (real-T4-card replays).
**Purpose (per proposal L294):** "Pin-test corpus + property tests that gate any future change to Changes A-C + F."

---

## 2. File header (proposal L298-301)

The file's H1 + intro paragraph. Verbatim from proposal L299-301:

```markdown
# Calibrator Eval Cases

Golden hypothesis cards + expected calibrated scores. Run before any change to `escalation-rubric.md`, `confidence-calibrator.md`, `hypothesis-card-template.md`, or `sc-troubleshoot-protocol/SKILL.md` ships. A regression on any fixture or property test blocks merge.
```

**Notes for executor:**
- Single H1 title.
- Single intro paragraph spelling out (a) what the file holds, (b) which downstream files' changes trigger the suite, (c) regression-blocks-merge rule.
- The intro lists FOUR trigger files; the later "Suite integrity" section repeats them and adds a fifth (`confidence-check/SKILL.md`). Both must land verbatim.

---

## 3. Synthetic fixtures (V1 base) — Section H2 + Fixtures 1-6

Section header verbatim (proposal L303):

```markdown
## Synthetic fixtures (V1 base)
```

Six fixtures follow. For each: H3 heading, one descriptive paragraph naming the card's frontmatter fields (`claim_class`, `evidence_class`, `verdict_direction`, plus dimension scores), then `**Expected calibrated**:` and `**Asserts**:` lines.

### Fixture 1 — `fixture-h3-style.md` (source-only runtime REFUTE)

Verbatim from proposal L305-308:

```markdown
### Fixture 1 — `fixture-h3-style.md` (source-only runtime REFUTE)
Hypothesis card with `claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: REFUTE`, evidence_grounding=1.0, runtime_check=0.0 (cross-tab derived), four other dims=1.0.
**Expected calibrated**: ≤ 0.70 (M3a cap fires).
**Asserts**: M1 + M2 + M3a all closed in combination.
```

**Structured fields:**
- `claim_class`: `runtime_behavior`
- `evidence_class`: `source_static`
- `verdict_direction`: `REFUTE`
- `evidence_grounding`: `1.0`
- `runtime_check`: `0.0` (cross-tab derived from claim_class × evidence_class intersection)
- four other dims: `1.0`
- **Expected calibrated:** ≤ 0.70 (M3a cap fires)
- **Asserts:** M1 + M2 + M3a all closed in combination

### Fixture 2 — `fixture-pr86-rca-style.md` (AFFIRM with structural truncation)

Verbatim from proposal L310-313:

```markdown
### Fixture 2 — `fixture-pr86-rca-style.md` (AFFIRM with structural truncation)
`claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: AFFIRM`, evidence_grounding=1.0, runtime_check=0.5 (runnable command in card without captured output), four other dims=1.0.
**Expected calibrated**: ≤ 0.80 (gate_M2 = 0.80).
**Asserts**: M1 + M2 closure below the 0.85 STOP gate.
```

**Structured fields:**
- `claim_class`: `runtime_behavior`
- `evidence_class`: `source_static`
- `verdict_direction`: `AFFIRM`
- `evidence_grounding`: `1.0`
- `runtime_check`: `0.5` (runnable command in card without captured output)
- four other dims: `1.0`
- **Expected calibrated:** ≤ 0.80 (gate_M2 = 0.80)
- **Asserts:** M1 + M2 closure below the 0.85 STOP gate

### Fixture 3 — `fixture-static-defect-clean.md` (eval_run.py Path import case)

Verbatim from proposal L315-317:

```markdown
### Fixture 3 — `fixture-static-defect-clean.md` (eval_run.py Path import case)
`claim_class: static_defect`, `evidence_class: source_static`, evidence_grounding=1.0, runtime_check inherits 1.0, four other dims=1.0.
**Expected calibrated**: 1.0. **Asserts**: refactor does NOT over-correct.
```

**Structured fields:**
- `claim_class`: `static_defect`
- `evidence_class`: `source_static`
- `verdict_direction`: not specified (implicitly AFFIRM-class — static defect citation)
- `evidence_grounding`: `1.0`
- `runtime_check`: inherits `1.0` (cross-tab: static_defect × source_static → 1.0)
- four other dims: `1.0`
- **Expected calibrated:** `1.0`
- **Asserts:** refactor does NOT over-correct (negative-control: keep legitimate full-confidence static defects at 1.0)

### Fixture 4 — `fixture-sha-pinned.md` (structurally unverifiable predicate)

Verbatim from proposal L319-321:

```markdown
### Fixture 4 — `fixture-sha-pinned.md` (structurally unverifiable predicate)
Card cites `commit-sha-5a65c62:file:line`. `claim_class: static_defect`, evidence_grounding=0.5, runtime_check inherits 0.5.
**Expected calibrated**: ≤ 0.80 (gate_M1 = 0.80).
```

**Structured fields:**
- citation form: `commit-sha-5a65c62:file:line` (cites a SHA-pinned location not in the current working tree)
- `claim_class`: `static_defect`
- `evidence_class`: not specified explicitly (inherits from claim_class semantics)
- `evidence_grounding`: `0.5` (low: cannot verify against current tree)
- `runtime_check`: inherits `0.5`
- **Expected calibrated:** ≤ 0.80 (gate_M1 = 0.80)
- **Asserts:** (implicit) M1 gate closure when evidence_grounding ≤ 0.5

### Fixture 5 — `fixture-v1-legacy-card.md` (missing claim_class — migration)

Verbatim from proposal L323-326:

```markdown
### Fixture 5 — `fixture-v1-legacy-card.md` (missing claim_class — migration)
v1.0 frontmatter with no `Claim class`, `Evidence class`, or `Verdict direction` fields.
**Expected behavior**: calibrator defaults claim_class to `runtime_behavior`, evidence_class to `none`, verdict_direction to `AFFIRM` (fail-safe), records in Notes, proceeds.
**Asserts**: backward-compat — v1.0 cards do not break the calibrator.
```

**Structured fields:**
- frontmatter: v1.0 style, MISSING `Claim class`, `Evidence class`, `Verdict direction`
- **Expected behavior** (not a score — a behavior assertion): calibrator defaults missing fields to `claim_class: runtime_behavior`, `evidence_class: none`, `verdict_direction: AFFIRM` (fail-safe), records the defaulting in Notes, proceeds without erroring.
- **Asserts:** backward-compat — v1.0 cards do not break the calibrator.
- **Note:** this fixture differs from the others — it does not assert a calibrated score range; it asserts a behavioral path (default + proceed).

### Fixture 6 — `fixture-refute-runtime-verified.md` (legitimate REFUTE with strong runtime check)

Verbatim from proposal L328-330:

```markdown
### Fixture 6 — `fixture-refute-runtime-verified.md` (legitimate REFUTE with strong runtime check)
`claim_class: runtime_behavior`, `evidence_class: runtime_repro`, `verdict_direction: REFUTE`, evidence_grounding=1.0, runtime_check=1.0, four other dims=1.0.
**Expected calibrated**: 1.0. **Asserts**: M3a cap does NOT fire when runtime_check=1.0.
```

**Structured fields:**
- `claim_class`: `runtime_behavior`
- `evidence_class`: `runtime_repro`
- `verdict_direction`: `REFUTE`
- `evidence_grounding`: `1.0`
- `runtime_check`: `1.0`
- four other dims: `1.0`
- **Expected calibrated:** `1.0`
- **Asserts:** M3a cap does NOT fire when runtime_check=1.0 (negative-control for the M3a cap; ensures REFUTE-on-runtime claims that DO have strong runtime evidence are not downgraded).

---

## 4. Real-card replay fixtures (V2 merged) — Section H2 + Fixtures 7-9

Section header verbatim (proposal L332):

```markdown
## Real-card replay fixtures (V2 merged)
```

Three fixtures follow. Each is marked `[V2 merged]` in the H3 heading. Each replays an actual hypothesis card from the T4 troubleshoot run at directory `t4-pane-title-20260526-101500`.

> **Locator note:** Resolving the `t4-pane-title-20260526-101500` directory content is the responsibility of the parallel researcher (`t4-real-cards-and-template`). This spec-extraction researcher captures only what the proposal asserts about each fixture.

### Fixture 7 — `fixture-t4-h3-replay.md` [V2 merged]

Verbatim from proposal L334-336:

```markdown
### Fixture 7 — `fixture-t4-h3-replay.md` [V2 merged]
Replays actual `tier2-h3-options-subcommand.md` from `t4-pane-title-20260526-101500`. Frontmatter retrofitted: `claim_class: runtime_behavior`, `evidence_class: source_static`, `verdict_direction: REFUTE`.
**Expected calibrated**: ≤ 0.65 (per V2 rule 1) or ≤ 0.70 (per V1 M3a). Either is below 0.85. **Asserts**: the actual failing card cannot slip through after the refactor.
```

**Structured fields:**
- replays: `tier2-h3-options-subcommand.md` from `t4-pane-title-20260526-101500`
- frontmatter retrofitted to v1.5 schema:
  - `claim_class`: `runtime_behavior`
  - `evidence_class`: `source_static`
  - `verdict_direction`: `REFUTE`
- **Expected calibrated:** ≤ 0.65 (per V2 rule 1) OR ≤ 0.70 (per V1 M3a) — either bound is below the 0.85 STOP gate.
- **Asserts:** the actual failing card from the T4 run cannot slip through after the refactor (regression pin for the original Cross-Env defect).
- **Provenance marker:** `[V2 merged]` (preserved verbatim in H3 heading).

### Fixture 8 — `fixture-t4-h2-replay.md` [V2 merged]

Verbatim from proposal L338-340:

```markdown
### Fixture 8 — `fixture-t4-h2-replay.md` [V2 merged]
Replays actual H2 card from T4. `claim_class: runtime_behavior`, `evidence_class: source_static` (WebFetch GitHub URLs), `verdict_direction: REFUTE`.
**Expected calibrated**: ≤ 0.70. Also triggers WebFetch unverifiability note. **Asserts**: source-only REFUTE on runtime claim is structurally caught.
```

**Structured fields:**
- replays: actual H2 card from T4 (sibling of Fixture 7's H3 card; located in same `t4-pane-title-20260526-101500` directory)
- `claim_class`: `runtime_behavior`
- `evidence_class`: `source_static` (specifically, WebFetch against GitHub URLs)
- `verdict_direction`: `REFUTE`
- **Expected calibrated:** ≤ 0.70 (M3a cap)
- **Side effect:** also triggers a "WebFetch unverifiability" note (WebFetch against GitHub URLs is source-static, not runtime).
- **Asserts:** source-only REFUTE on a runtime claim is structurally caught.
- **Provenance marker:** `[V2 merged]`.

### Fixture 9 — `fixture-t4-h1-no-overcorrect.md` [V2 merged]

Verbatim from proposal L342-344:

```markdown
### Fixture 9 — `fixture-t4-h1-no-overcorrect.md` [V2 merged]
Replays actual H1 card from T4 (0.82 self-reported CONFIRM with mixed source + log evidence). `claim_class: runtime_behavior`, `evidence_class: log_evidence`, `verdict_direction: AFFIRM`.
**Expected calibrated**: 0.70-0.85 range; NO hard cap fires. **Asserts**: legitimate CONFIRM cards with log evidence are NOT downgraded by the refactor.
```

**Structured fields:**
- replays: actual H1 card from T4 (self-reported 0.82 CONFIRM, mixed source + log evidence)
- `claim_class`: `runtime_behavior`
- `evidence_class`: `log_evidence`
- `verdict_direction`: `AFFIRM`
- **Expected calibrated:** in range `0.70-0.85`; NO hard cap fires
- **Asserts:** legitimate CONFIRM cards with log evidence are NOT downgraded by the refactor (negative-control against over-correction).
- **Provenance marker:** `[V2 merged]`.

---

## 5. Property tests (proposal L346-354)

Section header + table verbatim (proposal L346-354):

```markdown
## Property tests

| ID | Property | Assertion |
|----|----------|-----------|
| P1 | M1 gate | `evidence_grounding ≤ 0.5` ⟹ `calibrated ≤ 0.80` |
| P2 | M2 gate | `runtime_check ≤ 0.5 AND claim_class ∈ {runtime_behavior, environment_dependent}` ⟹ `calibrated ≤ 0.80` |
| P3 | M3a cap | `verdict_direction == REFUTE AND claim_class == runtime_behavior AND runtime_check < 1.0` ⟹ `calibrated ≤ 0.70` |
| P4 | Determinism | running calibrator on same card produces same calibrated score (±0.0) across N=5 runs |
| P5 | Anchoring (soft) | varying `Self-reported confidence:` from 0.30 to 0.99 must not change calibrated by more than ±0.05. **Soft assertion** (warn-only in CI). |
```

**Structured per-row:**

| ID | Property name | Full assertion (verbatim from table) | Hard / Soft |
|----|---------------|---------------------------------------|-------------|
| P1 | M1 gate | `evidence_grounding ≤ 0.5` ⟹ `calibrated ≤ 0.80` | **Hard** |
| P2 | M2 gate | `runtime_check ≤ 0.5 AND claim_class ∈ {runtime_behavior, environment_dependent}` ⟹ `calibrated ≤ 0.80` | **Hard** |
| P3 | M3a cap | `verdict_direction == REFUTE AND claim_class == runtime_behavior AND runtime_check < 1.0` ⟹ `calibrated ≤ 0.70` | **Hard** |
| P4 | Determinism | running calibrator on same card produces same calibrated score (±0.0) across N=5 runs | **Hard** |
| P5 | Anchoring (soft) | varying `Self-reported confidence:` from 0.30 to 0.99 must not change calibrated by more than ±0.05 | **Soft** (warn-only in CI; explicit `**Soft assertion**` annotation in the row text) |

**Cross-reference to fixtures:**
- P1 ↔ Fixture 4 (`fixture-sha-pinned.md`, evidence_grounding=0.5).
- P2 ↔ Fixture 2 (`fixture-pr86-rca-style.md`, runtime_check=0.5 on runtime_behavior claim).
- P3 ↔ Fixture 1 + Fixture 7 + Fixture 8 (REFUTE on runtime_behavior with runtime_check<1.0).
- P4 ↔ no specific fixture — applies as a global property to every fixture.
- P5 ↔ no specific fixture — applies as a perturbation property.

---

## 6. Suite integrity (proposal L356-365)

Verbatim from proposal L356-365:

```markdown
## Suite integrity

Run on every PR that touches:
- `escalation-rubric.md`
- `confidence-calibrator.md`
- `hypothesis-card-template.md`
- `confidence-check/SKILL.md`
- `sc-troubleshoot-protocol/SKILL.md` (V2-merged Change F)

A regression on any fixture or hard property (P1-P4) blocks merge. P5 warnings surface for triage.
```

**Structured:**

**Suite trigger files** (any PR touching ANY of these MUST run the corpus):
1. `escalation-rubric.md` — the rubric whose formula the expected scores are computed against (Change A target).
2. `confidence-calibrator.md` — the agent under test (Change C target).
3. `hypothesis-card-template.md` — the card schema the fixtures conform to (Change B / PR #89 target).
4. `confidence-check/SKILL.md` — the consumer skill (not a Change-A/C target, but a downstream consumer).
5. `sc-troubleshoot-protocol/SKILL.md` — the dispatcher (Change F target; annotated `(V2-merged Change F)` in the proposal).

**Merge-blocking rule:**
- Regression on **any fixture** (Fixtures 1-9) → blocks merge.
- Regression on **any hard property** (P1-P4) → blocks merge.
- Failure of **P5 (soft / anchoring)** → surfaces as a warning for triage; does NOT block.

---

## 7. Implementation hook (deferred to follow-up commit) (proposal L367-370)

Verbatim from proposal L367-370:

```markdown
## Implementation hook (deferred to follow-up commit)

Pytest harness invoking this corpus is OUT OF SCOPE for this brainstorm proposal. Expected landing path: `tests/troubleshoot/test_calibrator_eval_cases.py`.
```

**Structured:**
- The pytest harness that actually executes the corpus (loads each fixture, computes calibrated, asserts thresholds, runs P1-P5 properties) is **explicitly deferred to a follow-up commit**.
- Expected future landing path: `tests/troubleshoot/test_calibrator_eval_cases.py`.
- **Scope rule for THIS task:** Track 4 (Change E) creates ONLY the markdown corpus file. The pytest harness is a separate downstream task and MUST NOT be in scope here.

---

## 8. Code-fence terminator (proposal L370)

The new file's content ends at proposal L370 with the closing triple-backtick of the outer code fence:

```
```
```

Everything between proposal L298 (opening ```markdown) and L370 (closing ```) is the verbatim content of the new file.

---

## 9. Dependency on Changes A and C — HARD prerequisite

This is the most critical operational fact for the task file. The expected scores in this corpus are **computed against Change A's gated-min formula plus Change A's M3a verdict-direction modifier, plus Change C's calibrator updates that implement them.**

**Evidence from the proposal:**

- **Change A** (proposal L43-95) adds two artifacts the corpus expected-scores depend on:
  - the `gated-minimum` formula `min(arithmetic_mean(all_six), evidence_grounding + 0.30, runtime_check + 0.30)` — L210 references this verbatim, and the corpus's per-fixture "gate_M1 = 0.80", "gate_M2 = 0.80" annotations directly cite the formula's gate names.
  - the verdict-direction modifier (M3a), proposal L71-73: "After computing the gated-minimum confidence, apply this modifier when the card's frontmatter declares `claim_class: runtime_behavior` AND `runtime_check < 1.0`". The cap values (0.70 REFUTE / 0.84 AFFIRM) are exactly the values Fixture 1 / Fixture 6 / Fixture 7 / P3 reference.
- **Change C** (proposal L190+) teaches the calibrator to apply both pieces. L210-211 show the new procedural steps; L239-242 show the Stage-2 trace fields (`gate_M1`, `gate_M2`, `verdict_cap`) the corpus's "**Asserts**: M1 + M2 + M3a all closed in combination" (Fixture 1) presumes.
- The "minimum subset closing M1+M2+M3a + Cause #1" (proposal L418) is **Changes A + B + C + F**. Change E (this corpus) is the regression pin — without A and C, the calibrator produces legacy scores that DO NOT match the expected ranges in this corpus.

**Operational consequence for the task file:**

- The corpus file (the markdown deliverable) **CAN be created in parallel** with Changes A, B, C, F — no merge-order conflict at the file-creation level.
- The corpus's **expected behavior is only valid AFTER Changes A and C land.** If a pytest harness is wired up before A and C, every Fixture 1/2/4/7/8 expected-score assertion will FAIL (legacy calibrator produces ~0.89-1.0 for these cards).
- The task file should encode this as: "Can be created in parallel with A/B/C/F. Cannot be **executed** until A and C land. The pytest harness is deferred per Section 7 above, so this temporal sequencing only becomes a hard constraint once the follow-up commit wires the harness."

**Cross-reference to the proposal's Implementation order:** The proposal's Implementation order (referenced in research-notes.md L32 as L488-495) places Change E LAST, after A → B → C → F. This is consistent with the dependency analysis above.

---

## 10. Provenance markers summary

| Item | Provenance per proposal | Verbatim marker in file content |
|------|-------------------------|----------------------------------|
| File overall | V1 base (Fixtures 1-6 + P1-P5); V2 merged (Fixtures 7-9) | header line L292: `[Provenance: V1 base (Fixtures 1-6 + Properties P1-P5); V2 merged (Fixtures 7-9 replay real T4 cards)]` |
| Section "## Synthetic fixtures (V1 base)" | V1 base | `(V1 base)` literally in the H2 heading |
| Section "## Real-card replay fixtures (V2 merged)" | V2 merged | `(V2 merged)` literally in the H2 heading |
| Fixture 7 H3 heading | V2 merged | `[V2 merged]` literal suffix in H3 |
| Fixture 8 H3 heading | V2 merged | `[V2 merged]` literal suffix in H3 |
| Fixture 9 H3 heading | V2 merged | `[V2 merged]` literal suffix in H3 |
| Suite integrity bullet 5 (`sc-troubleshoot-protocol/SKILL.md`) | V2 merged | parenthetical `(V2-merged Change F)` in the bullet |

All seven provenance markers MUST land verbatim in the created file.

---

## 11. Acceptance checklist for the executor

The task file's validation phase must confirm ALL of:

- [ ] File exists at `src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` (NOT in `.claude/` — sync-dev mirrors there).
- [ ] H1 = `# Calibrator Eval Cases`.
- [ ] Intro paragraph verbatim per Section 2 above.
- [ ] H2 `## Synthetic fixtures (V1 base)` present.
- [ ] Fixtures 1-6 present, each as H3 with the exact heading text from Sections 3.1-3.6 above.
- [ ] Each Fixture 1-6 includes the descriptive paragraph + `**Expected calibrated**:` line + `**Asserts**:` line (Fixture 5 uses `**Expected behavior**:` instead — preserve that variant).
- [ ] H2 `## Real-card replay fixtures (V2 merged)` present.
- [ ] Fixtures 7-9 present, each H3 with the `[V2 merged]` suffix.
- [ ] Each Fixture 7-9 includes its descriptive paragraph + `**Expected calibrated**:` + `**Asserts**:`.
- [ ] H2 `## Property tests` present with the 5-row table (columns: ID, Property, Assertion).
- [ ] All five property-test rows P1-P5 verbatim per Section 5 above.
- [ ] P5's `**Soft assertion**` annotation preserved.
- [ ] H2 `## Suite integrity` present with the 5-bullet trigger-file list + the merge-blocking rule.
- [ ] H2 `## Implementation hook (deferred to follow-up commit)` present with the verbatim text (does NOT create the pytest file).
- [ ] Pytest harness (`tests/troubleshoot/test_calibrator_eval_cases.py`) is NOT created — out of scope per Section 7.
- [ ] `make sync-dev` mirrors the file into `.claude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md`.
- [ ] `make verify-sync` returns 0.
- [ ] Markdownlint passes on the new file.

---

## Status: Complete

## Summary

**Spec extraction for Track 4 / Change E complete.** All Change E content (proposal L290-372) extracted verbatim and structured:

- **File header + intro** (Section 2): H1 `# Calibrator Eval Cases` + intro paragraph naming the four trigger files and the regression-blocks-merge rule.
- **Synthetic fixtures 1-6** (Section 3): full structured field tables for each — claim_class, evidence_class, verdict_direction, dimension scores, Expected calibrated, Asserts. Fixture 5 is the only fixture asserting a behavior (defaulting) rather than a score.
- **Real-card replay fixtures 7-9** (Section 4): each marked `[V2 merged]`, each replaying a specific T4 card from `t4-pane-title-20260526-101500` (resolution delegated to the parallel `t4-real-cards-and-template` researcher).
- **Property tests P1-P5** (Section 5): full 5-row table verbatim; P1-P4 hard, P5 soft (warn-only).
- **Suite integrity** (Section 6): the 5 trigger files + the "regression on any fixture or hard property blocks merge; P5 warns" rule.
- **Implementation hook** (Section 7): pytest harness explicitly deferred; expected future path `tests/troubleshoot/test_calibrator_eval_cases.py` is OUT OF SCOPE for THIS task.
- **HARD prerequisite on Changes A and C** (Section 9): the file can be CREATED in parallel with A/B/C/F, but its expected scores are only producible AFTER Changes A (gated-min formula + M3a modifier) and C (calibrator updates that apply them) land. Without A and C, every Fixture 1/2/4/7/8 expected-score check would fail against the legacy calibrator. This is the most important sequencing constraint the task file must encode.
- **Provenance markers** (Section 10): seven markers (file header, two H2 section labels, three Fixture H3 `[V2 merged]` suffixes, one Suite integrity bullet annotation) must land verbatim.
- **Acceptance checklist** (Section 11): 16 items for the executor's validation phase.

**Output file:** `/config/workspace/IronClaude/.claude/worktrees/calibration-source-runtime-gap/.dev/tasks/to-do/TASK-RF-track-4-change-e-eval-cases-corpus-20260527-044000/research/01-change-e-spec-extraction.md`
