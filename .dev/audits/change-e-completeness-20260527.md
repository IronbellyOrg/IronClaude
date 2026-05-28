# Change E Completeness Audit — `calibrator-eval-cases.md`

**Date:** 2026-05-27
**Auditor:** Claude (read-only, no code changes)
**File audited:** `/config/workspace/IronClaude/src/superclaude/skills/sc-troubleshoot-protocol/refs/calibrator-eval-cases.md` (81 lines, 4915 bytes, mtime 2026-05-27 15:51)
**Spec source:** `/config/workspace/IronClaude/.dev/brainstorms/calibration-refactor-pr86/cross-env-compare/CROSS-ENV-PROPOSAL-MERGED.md` lines 290-370 (Change E section)

## Verdict: **DONE** (with two minor evidence-traceability nits)

The file as it stands on `fix/integration-contracts-mechanism-signature` is a faithful copy of the Change E content block from `CROSS-ENV-PROPOSAL-MERGED.md`. A line-by-line diff of the file against the spec's embedded markdown block shows only **cosmetic differences** (markdown-lint blank-line insertions after section headings, and the absence of the surrounding ` ```markdown ` code-fence — which is correct, since the spec's fence delimits the embedded sample, not the file itself).

There is **no functional gap**. The two nits called out below are about *evidence retrievability for replay fixtures*, not about anything the spec explicitly required.

## Count verification

| Spec requirement | Spec citation | Actual in file | Status |
|---|---|---|---|
| 9 fixtures total | line 34 of spec ("9 fixtures + 5 properties; 6 synthetic + 3 real-T4-replay") | Fixtures 1-9 (file lines 7, 13, 19, 24, 29, 35, 42, 47, 52) | DONE |
| 5 property tests | line 34 of spec | P1-P5 (file lines 61-65) | DONE |
| 6 synthetic | section "Synthetic fixtures (V1 base)" (spec line 303) | Fixtures 1-6 under "Synthetic fixtures (V1 base)" (file line 5) | DONE |
| 3 real-T4-replay | section "Real-card replay fixtures (V2 merged)" (spec line 332) | Fixtures 7-9 under "Real-card replay fixtures (V2 merged)" (file line 40) | DONE |

## Per-fixture shape audit

Required shape per task brief: `claim_class` + `evidence_class` + `verdict_direction` (frontmatter) + expected calibrated score + asserts which of M1/M2/M3a it closes.

| # | claim_class | evidence_class | verdict_direction | Expected calibrated | M1/M2/M3a assertion | Verdict |
|---|---|---|---|---|---|---|
| 1 | `runtime_behavior` | `source_static` | `REFUTE` | ≤ 0.70 (M3a cap) | M1 + M2 + M3a all closed | DONE |
| 2 | `runtime_behavior` | `source_static` | `AFFIRM` | ≤ 0.80 (gate_M2) | M1 + M2 closure below 0.85 STOP | DONE |
| 3 | `static_defect` | `source_static` | (omitted — but `static_defect` makes verdict_direction non-load-bearing for caps) | 1.0 | refactor does NOT over-correct | DONE-with-nit-1 |
| 4 | `static_defect` | (omitted — only claim_class + evidence_grounding=0.5) | (omitted) | ≤ 0.80 (gate_M1) | M1 gate fires | DONE-with-nit-2 |
| 5 | (intentionally omitted — this fixture's *purpose* is the missing-frontmatter migration case) | (intentionally omitted) | (intentionally omitted) | calibrator fail-safe defaults | backward-compat | DONE (omission is the test) |
| 6 | `runtime_behavior` | `runtime_repro` | `REFUTE` | 1.0 | M3a cap does NOT fire when runtime_check=1.0 | DONE |
| 7 | `runtime_behavior` | `source_static` | `REFUTE` | ≤ 0.65 (V2 rule 1) or ≤ 0.70 (V1 M3a) | failing T4-H3 card cannot slip through | DONE |
| 8 | `runtime_behavior` | `source_static` (WebFetch GitHub URLs) | `REFUTE` | ≤ 0.70 + WebFetch unverifiability note | source-only REFUTE on runtime claim is structurally caught (implicit M3a) | DONE |
| 9 | `runtime_behavior` | `log_evidence` | `AFFIRM` | 0.70-0.85 range; NO hard cap fires | legitimate CONFIRM cards with log evidence NOT downgraded | DONE |

**Nit-1 (Fixture 3):** `verdict_direction` is omitted in the description. Spec text at line 316 of the proposal *also* omits it, so the file matches the spec exactly. This is not a defect against the spec, but the cap behavior would benefit from explicit `verdict_direction: AFFIRM` for a clean-import success-case fixture.

**Nit-2 (Fixture 4):** Same as above — `evidence_class` and `verdict_direction` are omitted, matching the spec line 320 exactly. The fixture's load-bearing assertion is gate_M1 (`evidence_grounding=0.5 → calibrated ≤ 0.80`), which only requires `claim_class` + `evidence_grounding`. Acceptable, but a strict reading of the task's "required shape" criterion would flag both fields as missing.

## Real-T4-replay status (the critical evidence-traceability check)

The task brief asks: **"do the T4 H1/H2/H3 cards exist as fixtures with their original 0.82/0.85/0.95 self-reports?"**

| T4 card | Fixture | Self-report stated in file? | Self-report stated in spec? | Verdict |
|---|---|---|---|---|
| H1 (AFFIRM, log+source) | Fixture 9 (`fixture-t4-h1-no-overcorrect.md`) | YES — "0.82 self-reported CONFIRM" (file line 54) | YES (spec line 343) | DONE |
| H2 (REFUTE, WebFetch source) | Fixture 8 (`fixture-t4-h2-replay.md`) | NO — file line 49 names the H2 card and its frontmatter retrofit but does not echo the 0.85 self-report | NO — spec line 339 also omits it | DONE-against-spec, missing-from-file |
| H3 (REFUTE, options-subcommand) | Fixture 7 (`fixture-t4-h3-replay.md`) | NO — file line 44 names `tier2-h3-options-subcommand.md` from `t4-pane-title-20260526-101500` but does not echo the 0.95 self-report | NO — spec line 335 also omits it | DONE-against-spec, missing-from-file |

**Key finding:** Only H1's self-report (0.82) is preserved in the prose. H2 (0.85) and H3 (0.95) self-reports — the two scores explicitly called out in the proposal's own root-cause analysis at line 398 ("the 0.95 / 0.85 self-reports passed through unguarded") — are **not echoed in the fixture descriptions** in either the spec or the file.

This is **not a Change E spec violation** (the file matches the spec text exactly) but **is** an evidence-traceability gap relative to the task brief's verification criterion. The replay-fixture content will need those self-reports to assert "calibrator catches what the unguarded self-report missed", and the source artifacts at `t4-pane-title-20260526-101500/` are not present in this working copy (search returned no matches), so future implementation of the replay fixtures will need to retrieve them from the original T4 environment or from git history.

## Property test coverage

| ID | Property | Spec | File | Status |
|---|---|---|---|---|
| P1 | M1 gate (`evidence_grounding ≤ 0.5 ⟹ calibrated ≤ 0.80`) | spec line 350 | file line 61 | DONE |
| P2 | M2 gate (`runtime_check ≤ 0.5 AND claim_class ∈ {runtime_behavior, environment_dependent} ⟹ calibrated ≤ 0.80`) | spec line 351 | file line 62 | DONE |
| P3 | M3a cap (`verdict_direction == REFUTE AND claim_class == runtime_behavior AND runtime_check < 1.0 ⟹ calibrated ≤ 0.70`) | spec line 352 | file line 63 | DONE |
| P4 | Determinism (±0.0 across N=5 runs) | spec line 353 | file line 64 | DONE |
| P5 | Anchoring soft assertion (±0.05 across self-reported 0.30→0.99) | spec line 354 | file line 65 | DONE |

## Suite-integrity block

File lines 67-77 list the five PR-trigger paths:
- `escalation-rubric.md`
- `confidence-calibrator.md`
- `hypothesis-card-template.md`
- `confidence-check/SKILL.md`
- `sc-troubleshoot-protocol/SKILL.md` (V2-merged Change F)

Matches spec lines 359-363 exactly. The "hard-property (P1-P4) blocks merge; P5 warnings surface for triage" rule is preserved at file line 77. DONE.

## Implementation-hook deferral

File lines 79-81 mark the pytest harness as out of scope, pointing to `tests/troubleshoot/test_calibrator_eval_cases.py` as the expected landing path. Matches spec lines 367-369. DONE.

## Punch list

The following items would tighten the corpus but are **not** required by the Change E spec as written. Flagging for follow-up commit (the same one that lands the pytest harness):

1. **(Optional, evidence-traceability)** Echo the H2 and H3 self-reports inline in Fixtures 7-8 descriptions:
   - Fixture 7 description should mention "(0.95 self-reported REFUTE)".
   - Fixture 8 description should mention "(0.85 self-reported REFUTE with WebFetch evidence)".
   This makes the punchline ("calibrator catches what the unguarded self-report missed") legible without cross-referencing the T4 artifacts.

2. **(Optional, shape-uniformity)** Add explicit `verdict_direction: AFFIRM` to Fixture 3 and `evidence_class: source_static, verdict_direction: AFFIRM` to Fixture 4. Both are currently spec-faithful omissions; making them explicit would let a pytest harness consume the fixture metadata uniformly without per-fixture defaulting logic (though fixture 5 *requires* the omission as its test condition, so defaulting logic is already needed regardless).

3. **(Blocking for the implementation commit, not for Change E)** Source artifacts at `.dev/troubleshoot/t4-pane-title-20260526-101500/` (referenced by Fixtures 7-9) are not present in this working copy. The implementation commit landing `tests/troubleshoot/test_calibrator_eval_cases.py` will need to either:
   - retrieve them from the original T4 environment, or
   - create the actual fixture files (`fixture-t4-h{1,2,3}-replay.md`) by hand using the spec's frontmatter retrofit + the recorded self-report values from line 398 of the spec.

## Conclusion

**Verdict: DONE.**

Change E is complete with respect to the merged proposal:
- 9 fixtures (6 synthetic + 3 real-T4-replay): present
- 5 property tests (P1-P5): present
- Synthetic-vs-replay split: correct
- Per-fixture frontmatter triad + expected score + assertion: present where the spec requires it (Fixtures 1, 2, 5, 6, 7, 8, 9 in full; Fixtures 3 and 4 match spec omissions exactly)
- Suite-integrity trigger list: matches spec
- Pytest-harness deferral: present

The only audit-grade gap is the H2/H3 self-report (0.85/0.95) traceability — which is a spec-level omission inherited by the file, not a file-level regression against the spec. Recommend folding the punch-list items into the same follow-up commit that lands the pytest harness; do not block Change E on them.
