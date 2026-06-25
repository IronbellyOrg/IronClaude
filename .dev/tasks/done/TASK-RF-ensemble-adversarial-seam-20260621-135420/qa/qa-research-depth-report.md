# QA Report — research-depth (Lens: research-depth)

**Topic:** Wire adversarial seam in ensemble.py → build_reflect_contract; add regression test asserting derive_verdict != PASS
**Date:** 2026-06-21
**Phase:** research-depth
**Stance:** ADVERSARIAL — assume research is superficial until proven otherwise.

---

## Scope
Assigned research files:
- 01-ensemble-seam-inventory.md
- 02-adversarial-child-output-schema.md
- 03-contract-consumer-constraints.md
- 04-test-patterns.md
- 05-template-and-citations.md

Lens focus: Is the research DEEP ENOUGH to build a correct task file without re-reading source?

---

## Findings

### Lens-Focus Question 1 — R2: HOW does the adversarial child produce output (threshold-derive vs producer-extend)? — PASS (DEEP)

R2 does NOT merely list the return-contract keys. It (a) traces the invocation path
(`run_adversarial_scorer` → `ClaudeProcess` headless `claude --print` running the literal
`/sc:adversarial` slash command, not a subprocess module), (b) enumerates the COMPLETE
producer schema with a typed field table (10 fields: merged_output_path, convergence_score,
artifacts_dir, status, base_variant, unresolved_conflicts, fallback_mode, failure_stage,
invocation_method, unaddressed_invariants), and (c) renders the DECISIVE finding: the five
target deviation/regression fields are emitted NOWHERE by the child (grep → ZERO hits over
the adversarial skill dir).

**Independently verified:** I read `src/superclaude/skills/sc-adversarial-protocol/SKILL.md`
L425-460 — the return-contract schema matches R2's field table EXACTLY (all 10 fields, types,
null-on-abort semantics). I re-ran the grep over `sc-adversarial-protocol/` for the four
deviation tokens → **0 hits**, confirming R2's "SCORE-ONLY" decisive finding. R2 then lays
out three concrete design options (threshold-derive from convergence | extend the producer |
parse the merged-report body) with their feasibility trade-offs. This is exactly the
threshold-derive-vs-producer-extend decision the lens asks for, and it is grounded, not
hand-waved. **The builder can choose between the approaches from this research alone.**

### Lens-Focus Question 2 — R3: Does it trace the derive_verdict ladder end-to-end incl. the bool-type trap? — PASS (DEEP)

R3 traces the full first-match-wins ladder (blocked → degraded → halted → pass) with a
per-condition table giving the EXACT line number and verdict/slug for every stage. Stage-3
HALTED (the stage real findings must trip) is given truth-condition-by-truth-condition
(contract.py:311 status-failed, :313 status-partial, :315 regression_present is True, :317
unauthorized, :319 needs-human-decision, :321 user-decision, :324 count.regression>0, :326
count.drift>0). It explicitly calls out the strict-identity `is True` checks AND the
`_LOAD_BEARING_BOOL_FIELDS` F2 guard (contract.py:47-57, 200-209) that routes a non-bool
truthy value to BLOCKED/malformed-contract-boolean — i.e. the bool-type trap — with the
correct remediation ("emit genuine Python bool, never `'true'`/`1`").

**Independently verified:** I read `contract.py:307-328` (the `_halted_reason` ladder) and
`contract.py:40,47-57` (`_DEVIATION_KEYS`, `_LOAD_BEARING_BOOL_FIELDS`). Every line anchor
and every truth condition in R3's tables matches the source EXACTLY. The bool-type trap is
real and correctly described. This is the single most important depth requirement for a
correct task and R3 nails it.

### Lens-Focus Question 3 — R4: Does it give a concrete replicable test design? — PASS (DEEP)

R4 names the EXACT home (`test_ensemble_stub_integration.py`, new I12 after L452), the EXACT
model test (I4 DEGRADED negative-witness, L222-228), the EXACT injection seam (`_const_score`
at L39-41, the `_run` driver at L88-102), the EXACT fixtures (`temp_tasklist`, `patch_git`
from conftest L46-55/58-80), a near-complete code sketch with the precise assertions
(`result.verdict is not Verdict.PASS` sharpened to `Verdict.HALTED` / `exit_code == 10` /
`reason == "regression"`), the red-then-green expectation (FAILS today seeing PASS — the
intended red proof), and the verified pytest invocation. It also flags the NFR-7 no-nesting
guard tokens the new code/test must avoid.

**Independently verified:** I read `test_ensemble_stub_integration.py:34-102` — `_const_score`,
`_FailingTransport`, `_distinct_stub`, `_config`, and `_run` all match R4's quotes verbatim.
I re-ran `uv run pytest tests/cli/reflect/test_ensemble_stub_integration.py -q` → **12 passed
in 0.21s** (R4 claimed 12). I confirmed `fixtures/halted_regression.yaml` has `regression: 1`
and `regression_present: true` (R4's claimed reference shape). A builder can write I12 from
this alone.

### Lens-Focus Question 4 — R1: Precise widen points + every backward-compat call site? — PASS (DEEP)

R1 §8 enumerates all six surfaces that change in lockstep when `AdversarialScoreFn` is
widened (the alias L72; the seam branch L229-232; `run_adversarial_scorer` sig L244-249 +
body L271; the `build_reflect_contract` call L234-239 + its sig/body L360-407; the 3 stub
test sites). It correctly identifies that production is insulated because `runner.py:425`
calls `run_tier2_ensemble(config)` positional-only with no score-fn kwarg.

**Independently verified:** read `ensemble.py:60-150, 215-407` — every line anchor (L72,
L136-145, L221-239, L244-271, L274-301, L336-357, L360-407) is EXACT, including the
field-by-field dict body (L377-407) matching R1's HARD-CODED-vs-COMPUTED table cell for cell.
Confirmed `runner.py:425` → `run_tier2_ensemble(config)` positional-only, and
`grep AdversarialScoreFn` → only `ensemble.py` (no external consumer). R1 also CORRECTLY
flags that the user's brief named a `_parse_convergence_score` helper that **does not exist**
— the real helpers are `parse_adversarial_contract` (L274) + `extract_convergence_score`
(L336). I confirmed `_parse_convergence_score` returns no matches. This is exactly the kind
of brief-vs-reality correction that prevents a builder from writing an item against a
phantom symbol.

### Lens-Focus Question 5 — Is the threshold-derive (convergence ≥0.75) approach grounded or hand-wavy? — PASS (GROUNDED, with an honest caveat)

R2 §7 option 1 grounds the threshold-derive approach in TWO real citations: reflect SKILL.md
documents convergence routing (≥0.75 PASS / ≥0.60 PARTIAL / <0.60 FAIL) and
`grader-extensions.md:300` uses `convergence_score < 0.75 OR verdict == regression_present`.
Critically, R2 is HONEST that threshold-derive yields only a COARSE `regression_present`-ish
gate and does NOT recover per-class `deviation_count_by_class` / `unauthorized_deviation` /
`needs_human_decision` — those require option 2 (extend the producer). R3 §6 confirms the
minimal correct fix for the TRACK GOAL test needs only `regression_present=True` and/or
`deviation_count_by_class.regression >= 1`, so threshold-derive IS sufficient for the stated
goal (a regression test asserting derive_verdict != PASS) while R2 correctly scopes its
limits for the fuller mapping. This is grounded, not hand-wavy — the approach is bounded by
explicit citations and the researcher states what it cannot do.

### Lens-Focus Question 6 — Could a builder write per-file checklist items from this research alone? — MOSTLY (one path defect would force a guess/error)

R5 supplies the template ruleset (B2/A3/M3/I17/I18/I19/I22 with verbatim quotes + line
anchors), the frontmatter convention fields, the verbatim POST-reflect-wrapper item, and the
four load-bearing citation anchors — all independently verified as existing and verbatim.
R1-R4 give per-edit-point and per-test detail. The cross-task tension (R6 was "REJECTED" in
the prior task's scope vs flagged CRITICAL in per-lens QA) is explicitly framed so the builder
knows this is a deliberate scope-expansion follow-up, not re-litigation. This is genuinely
buildable.

**The one defect (see Issues Found #1):** R5 cites the prior task FILE at a path that does
not resolve to an existing file. A builder copying that path literally into a Read/cite would
hit a missing-file error and would have to GUESS the correct nested location.

---

## Self-Audit

**(a) Reliance list — items I relied on upstream verdicts for:** None. This is a
research-depth lens with no inherited structural verdict in the spawn prompt; I performed
all verification independently.

**(b) Independent semantic checks (tool-backed):**
- Verified R1 ensemble.py anchors L72/L136-145/L221-239/L244-271/L274-301/L336-357/L360-407
  by Read of `src/superclaude/cli/reflect/ensemble.py` — all exact incl. the L377-407 dict body.
- Verified R3 derive_verdict ladder by Read of `contract.py:307-328` + `:40,47-57` — exact.
- Verified R2 producer schema by Read of `sc-adversarial-protocol/SKILL.md:425-460` (10 fields
  match) + re-ran grep for deviation tokens → 0 hits (confirms SCORE-ONLY).
- Verified R2 `--suspect-source` flag claim by grep of `commands/adversarial.md` flag table →
  flag absent (confirmed inert).
- Verified R4 test scaffolding by Read of `test_ensemble_stub_integration.py:34-102` + re-ran
  `uv run pytest …test_ensemble_stub_integration.py -q` → 12 passed.
- Verified R5 citation anchors: prior-task frontmatter (lines 2/15/18/19/20/31/59/60), line
  148, line 483, OI-1 rows 35/38/39/40, QA CRITICAL #2 line 39, consolidated R6 lines 84-85,
  spec.md:303, template-02 existence — all verbatim/existing.
- Verified R1 backward-compat: `runner.py:425` positional-only call + `AdversarialScoreFn`
  single-consumer grep.

**Why the user should trust this:** I made 9 Read calls + 6 Bash/grep calls mapping to
specific claims, re-ran the test suite the research cites, and found exactly ONE defect (a
path that does not resolve) — surfaced below. A clean pass on a 5-file research set this dense
would be suspicious; the path defect is the real finding adversarial review is meant to catch.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | R2 explains HOW child produces output (derive vs extend) | PASS | SKILL.md:425-460 verified; grep deviation tokens → 0; 3 design options grounded |
| 2 | R3 traces derive_verdict ladder + bool-type trap | PASS | contract.py:307-328, :40,47-57 verified exact; F2 guard correctly described |
| 3 | R4 concrete replicable test design | PASS | test file L34-102 verified verbatim; 12 tests re-run green; halted_regression.yaml shape confirmed |
| 4 | R1 widen points + backward-compat sites | PASS | ensemble.py anchors all exact; runner.py:425 positional-only; _parse_convergence_score phantom correctly flagged |
| 5 | Threshold-derive grounding | PASS | grader-extensions.md:300 + SKILL convergence routing cited; honest about coarse-only scope |
| 6 | Buildable per-file from research alone | MOSTLY | All content anchors verbatim; ONE unresolvable path (Issue #1) |

## Summary
- Checks passed: 5 / 6 fully PASS; 1 MOSTLY (single defect)
- Checks failed: 0 fully; 1 carries a MINOR defect
- Critical issues: 0
- Important issues: 0
- Minor issues: 1
- Confidence: Verified 6/6 lens questions with tool evidence | Unverifiable 0 | Unchecked 0 | Confidence 100%
- Tool engagement: Read: 9 | Grep/Bash: 6 | Glob: 0

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | research/05-template-and-citations.md:88, 89, 101, 104 (and §4 summary anchor list) | R5 cites the prior task file as `TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md`. That path resolves to `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md`, which **does NOT exist**. The file actually lives one directory deeper at `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md`. All line anchors R5 quotes from it (frontmatter L2/15/18/19/20, L148, L483) are verbatim-correct against the REAL file — only the path string is wrong. A builder copying the path literally into a Read or into a task-item Context field would hit a missing-file error and have to guess the nested location. (The OI-1 / QA-report / consolidated-findings paths R5 cites ARE correct — they include the full nested dir; only the top-level task-FILE path drops the directory level.) | In R5, correct every reference to the prior task file to the full nested path `.dev/tasks/to-do/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/TASK-RF-fr-rh2-headless-ensemble-20260620-024238.md` (the `<dir>/<same-name>.md` MDTM layout). Severity is MINOR not CRITICAL because the content is all verbatim-correct and the correct sibling-artifact paths in the same file make the right layout inferable — but it WILL cause a guess if copied literally, which this lens is charged with flagging. |

## Note on R2's `--suspect-source` finding (NOT a research-depth defect — informational)
R2 surfaces that `build_adversarial_prompt` (ensemble.py:299) emits `--suspect-source`, a flag
the `/sc:adversarial` command does not define (verified: absent from commands/adversarial.md
flag table). R2 correctly labels this "Unverified impact" and out of its own scope. This is a
PRE-EXISTING product bug in the seam, not a gap in the research — and R2 surfacing it is a sign
of DEPTH, not shallowness. It is NOT counted against the research. (It may warrant a separate
task-item note, but that is a builder/scope decision, not a research-depth FAIL.)

## Recommendations
- Fix Issue #1 (the prior-task-file path) in R5 before the builder consumes it — a 4-occurrence
  string correction. Everything else is build-ready.
- Optional: the builder may want to carry R2's `--suspect-source` observation into the task as
  an informational note, since the seam being wired emits a non-existent flag.

VERDICT: FAIL (one MINOR issue — research-depth lens treats any builder-would-guess defect as a FAIL per the no-leniency rule; the issue is a single string correction and the research is otherwise exceptionally deep and fully verified).

## QA Complete
