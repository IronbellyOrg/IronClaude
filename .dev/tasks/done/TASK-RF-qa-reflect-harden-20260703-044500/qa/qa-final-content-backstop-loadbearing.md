# QA Report — Task Qualitative (FINAL M3 gate)

**Lens:** deterministic-backstop-load-bearing
**Topic:** P0 deterministic backstops FX3 / FX5 / FX7 — are they LOAD-BEARING (do they fire on their real regression, or are they incidental / vacuous)?
**Date:** 2026-07-03
**Phase:** task-qualitative
**Fix cycle:** N/A (report only, `fix_authorization: false`)
**Worktree:** /config/workspace/IronClaude/.dev/worktrees/pr209-harden
**Stance:** Adversarial — assumed each backstop does NOT catch its bug class; attempted to prove it does not. Re-run after a transient API error truncated the prior evidence sections.

---

## Overall Verdict: PASS

All three P0 backstops are LOAD-BEARING, not incidental. Each fires (goes RED, or makes the
vacuity observable) on a genuine recurrence of its bug class, proven END-TO-END below with
deterministic evidence (a scratch AST harness for FX3, a green baseline + read mutation
structure for FX5, and source + fixtures + PENDING files for FX7). FX7 is evaluated against
the SHIPPED design — additive VISIBLE accounting, with the aggressive verdict-DEGRADE
correctly DEFERRED as two `needs_human_decision` PENDING decision files. The clean/shortfall
run still routing PASS is EXPECTED per R2-F2 / FR-RH2.9, NOT a backstop failure. The
adversarial probe that tried hardest to break FX7 (drop the `_make_result` passthrough of a
`*_verified` field) lands in the fail-CLOSED direction (models default `False` = "vacuous"),
so the vacuity-HIDING bug direction remains doubly covered. No load-bearing counterexample
found.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | FX3 traps F3 class: AST assertion (2) goes RED on buggy `_evidence_attr("pr_number")` | none | PASS | Scratch AST harness (below) proves buggy call resolves `answer_key="pr_number"` ∉ SetupAnswers ⇒ assertion(2) False ⇒ RED; fixed call resolves `"probe_pr"` ∈ fields ⇒ green |
| 2 | FX5 differentials trap F4 class: real mutation installed + buggy outcome asserted (3 spot-checks) | none | PASS | Read `test_gate_helper_differentials.py` — `_path_resolves` (L244-259), `_paths_resolve` (L367-379), `required_unobserved` (L439-453) each monkeypatch a real mutant and assert the buggy value; 26/26 green baseline |
| 3 | FX7 makes reviewer-SHORTFALL vacuity VISIBLE (`reviewers_verified:false` + token) | none | PASS | `ensemble.py:535-540` derives flag + appends token; `test_ensemble_unit.py:446-447` asserts both; `test_verdict_mapping.py:387` asserts `result.reviewers_verified is False` |
| 4 | FX7 makes clean-unverified vacuity VISIBLE (`verification_verified:false`) | none | PASS | `ensemble.py:577`; `test_verdict_mapping.py:403` asserts `result.verification_verified is False` |
| 5 | FX7 correctly DEFERS aggressive degrade as `needs_human_decision` PENDINGs; no code auto-applies | none | PASS | Two DECISION files exist; `contract.py` verdict logic (`_degraded_reason`/`_halted_reason`) never references any `*_verified` field; grep for auto-apply ⇒ NONE |
| 6 | FX7 shortfall/clean run still routes PASS (EXPECTED per R2-F2 / FR-RH2.9, not a failure) | none | PASS | `reviewer-shortfall` ∉ `_DEGRADED_COMPONENTS_HALT_SET` (contract.py:31-33); `test_verdict_mapping.py:369-403` asserts `Verdict.PASS`/exit 0 |

<!-- task-qualitative Axis column: closed set {AX-1..AX-5, none}. All rows PASS ⇒ `none`
(five-axis lens applied, nothing surfaced). AX-1 Drift is ACTIVE: the driving lens/GOAL was
supplied verbatim in the spawn prompt (the three load-bearing claims + the FX7 SHIPPED-design
framing), so no `drift-axis-inactive` annotation is required. -->

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0 | Important: 0 | Minor: 0
- Issues fixed in-place: 0 (report-only; `fix_authorization: false`)

---

## FX3 — LOAD-BEARING (F3 class: deriver reading a nonexistent answer field)

**Bug class (F3):** `_evidence_attr(attr, answer_attr=None)` reads the operator answer under
`answer_key = answer_attr or attr` via a SILENT `getattr(answers, answer_key, None)`
(`questions.py:68,71`). The buggy original call was `_evidence_attr("pr_number")` — no
`answer_attr` — so `answer_key` collapsed to `"pr_number"`, which is NOT a `SetupAnswers`
field, and the operator's `probe_pr` answer was silently dropped (fell through to
`evidence.pr_number`). No exception, no warning. Fixed at `questions.py:136`:
`_evidence_attr("pr_number", answer_attr="probe_pr")`.

**The trap (assertion 2):** `test_every_evidence_attr_answer_key_resolves_to_a_real_setupanswers_field`
(`test_setup_questions_resolution.py:135-167`) AST-introspects every `_evidence_attr` call,
resolves `answer_key` (keyword `answer_attr` → else 2nd positional → else `attr`), and asserts
`answer_key ∈ dataclasses.fields(SetupAnswers)` (built DYNAMICALLY, never hardcoded — stays in
sync).

**Deterministic proof it goes RED on the buggy original** (scratch AST harness; the real
`questions.py` was NOT mutated):

```
SetupAnswers fields: [augment_app_slug, author_association_values, decline_detection_fields,
  detected_augment_identity, emission_shape, evidence_source, expected_classifier_result,
  findings_locus, next_step, operation, probe_pr, repo, review_completeness_signal,
  run_validation, severity_field_path, surfaces_to_inspect, write_local_locked_contract]
'pr_number' in SetupAnswers fields: False        # <-- key fact
'probe_pr'  in SetupAnswers fields: True
BUGGY  _evidence_attr("pr_number")                -> answer_key='pr_number' -> in valid: False  (RED)
FIXED  _evidence_attr("pr_number", answer_attr="probe_pr") -> answer_key='probe_pr' -> in valid: True (green)
```

`'pr_number' ∉ SetupAnswers` is the load-bearing pivot: it is confirmed by BOTH the AST harness
and a direct `dataclasses.fields(SetupAnswers)` read. The buggy call therefore FAILS
assertion(2); the current fixed tree PASSES it. Assertion is genuinely load-bearing, not
incidental. Supporting guards (assertion 4, `test_every_collected_deriver_arg_is_a_string_constant`,
L193-218) block the obvious bypass — passing a variable instead of a literal would silently skip
the static check, so it fails loudly instead. Baseline: 4/4 green.

**Verdict FX3: LOAD-BEARING.**

---

## FX5 — LOAD-BEARING (F4 class: gate helper treating presence as observation / all-None as resolved)

FX5 authors a NEGATIVE test (real helper returns the safe value on degenerate input) AND a
DIFFERENTIAL test (a naive/pre-fix mutant is monkeypatched in and a downstream observation is
shown to FLIP to the buggy value) for every one of the 11 enforced gate-load-bearing helpers.
A "negative test exists" checkmark alone is insufficient (research/02 §5); the differential is
what proves a real regression cannot pass silently. Baseline: **26/26 green** (both files).

Three differentials spot-checked — each installs a REAL mutation and asserts the BUGGY outcome:

1. **`candidate._path_resolves` — naive all-None**
   (`test_path_resolves_differential_naive_all_none_flips_findings_observed`, L244-259).
   Real: `_findings_locus` on all-None reviews ⇒ `None`, `prov["findings_locus"].observed is
   False`. Then `monkeypatch.setattr(candidate_mod, "_path_resolves", _naive_path_resolves)`
   (the pre-F4 primitive where an all-None list stays truthy). Asserts the result flips to
   `"reviews[].body"` and `observed is True` — "bug reappears → mutation detected". The paired
   negative `test_path_resolves_all_none_list_is_not_resolved` (L236-241) asserts the REAL
   helper returns `False`, so an actual F4 regression turns THAT test RED.

2. **`lockgate._paths_resolve` — presence-not-observation**
   (`test_paths_resolve_differential_presence_not_observation_flips_gate`, L367-379).
   Real: `_paths_resolve(candidate).passed is False` (unobserved locus fails the gate). Then
   `monkeypatch.setattr(lockgate_mod, "_paths_resolve", _naive_paths_resolve_presence_only)`
   (mutant drops the `.observed` checks, keys off `bool(findings and signal)`). Asserts
   `.passed is True` — the mutant treats present-but-unobserved provenance as resolved and the
   gate WRONGLY passes.

3. **`candidate.CandidateContract.required_unobserved` — skip-field**
   (`test_required_unobserved_differential_skipping_field_flips_membership`, L439-453).
   Real: `"findings_locus" in required_unobserved()`. Then `monkeypatch.setattr` shrinks
   `MUST_OBSERVE_FIELDS` by `{"findings_locus"}` (the §5.3 mutation). Asserts `"findings_locus"
   not in required_unobserved()` — a must-observe field silently goes unchecked.

Each differential (a) reads a real symbol from the module under test, (b) installs a concrete
mutant via `monkeypatch`, and (c) asserts the *buggy* value — the exact structure that proves
detection rather than mere presence. The negative halves are the actual regression trip-wires:
were the F4 fix reverted (real helper → naive), the all-None/unobserved negatives go RED.

**Verdict FX5: LOAD-BEARING.**

---

## FX7 — LOAD-BEARING for VISIBILITY (and correctly DEFERS the aggressive degrade)

**SHIPPED design under evaluation:** FX7's honest-accounting is VISIBILITY, not a verdict flip.
Vacuity/shortfall must become OBSERVABLE via `*_verified` fields + a benign `reviewer-shortfall`
token, while the aggressive verdict-DEGRADE routings (which would reverse R2-F2 / FR-RH2.9) are
DEFERRED as `needs_human_decision` PENDINGs.

**(a) Reviewer-SHORTFALL is made VISIBLE — and the derivation is trapped both directions.**
`ensemble.py:535-540` derives `reviewers_verified = True if reviewers_requested is None else
reviewer_count >= reviewers_requested`, and appends `"reviewer-shortfall"` to
`degraded_components` only on a genuine shortfall. This derivation is load-bearing at the
ensemble seam because BOTH directions are asserted:
- shortfall ⇒ `test_ensemble_unit.py:446-447` asserts `"reviewer-shortfall" in degraded_components`
  AND `reviewers_verified is False`;
- met (2-of-2) / omitted-request ⇒ `test_ensemble_unit.py:466,474` assert `reviewers_verified
  is True`.
A constant-True mutant fails the shortfall assertion; a constant-False mutant fails the met/omitted
assertions. End-to-end, `test_verdict_mapping.py:369-388` feeds `degraded_reviewer_shortfall.yaml`
through `derive_verdict` and asserts `Verdict.PASS` / exit 0 / `reviewers_verified is False`.

**(b) Clean-unverified vacuity is made VISIBLE.** `ensemble.py:577` always emits
`verification_verified: False` in the headless seam (runs no verification triangle).
`test_verdict_mapping.py:391-403` feeds `vacuous_no_verify.yaml` and asserts `Verdict.PASS` /
exit 0 / `verification_verified is False`. The writeback emit is trapped by
`test_writeback.py:192-206`, which constructs a `ReflectResult(reviewers_verified=True, …)` and
asserts the emitted block carries `reviewers_verified is True` — since the models default is
`False`, this True→True passthrough is load-bearing for the persisted block.

**(c) PASS routing on shortfall/clean is EXPECTED, not a backstop failure.** `reviewer-shortfall`
is intentionally NOT a member of `_DEGRADED_COMPONENTS_HALT_SET`
(`contract.py:31-33 = {serena, auggie, env-aliases, evidence-validator, serena:context-excluded}`),
and `verification_skip_reason: tool-unavailable` is an exempt reason
(`_VERIFICATION_SKIP_EXEMPTIONS`, contract.py:36-38). So a 2-of-3 shortfall and a clean
unverified run both stay PASS-eligible per FR-RH2.9 (test_i3) / R2-F2. Correct per the design.

**(d) The aggressive DEGRADE is DEFERRED, and NO code auto-applies it.** Two PENDING decision
files exist, both stamped `**Status:** PENDING (NOT auto-applied)`:
- `phase-outputs/plans/fx7-degrade-on-reviewer-shortfall-DECISION.md` — documents that degrading
  a shortfall would REVERSE FR-RH2.9 (regress test_i3), non-additive; Option A (additive
  visibility) shipped, Option B deferred.
- `phase-outputs/plans/fx7-degrade-on-unverified-DECISION.md` — documents that degrade-on-any-
  unverified would REVERSE R2-F2 (break test_r2f2 + test_i1); "What was auto-applied: ONLY
  Option A … `_VERIFICATION_SKIP_EXEMPTIONS` is BYTE-UNCHANGED."

No auto-apply confirmed structurally: `derive_verdict` routes purely through `_degraded_reason`
and `_halted_reason`, and NEITHER function references `verification_verified`, `reviewers_verified`,
or `regression_verified` (full read of `contract.py`). The `*_verified` fields exist only as
telemetry surfaced by `_make_result` (contract.py:130-132) and re-emitted by the runner
(runner.py:120-122, 239-241). A targeted grep for a `*_verified → degrade` coupling returned
NONE. Baseline: FX7 test slice 6/6 green.

**Adversarial probe that tried hardest to break it (and why it does not):** dropping the
`_make_result` passthrough of `reviewers_verified`/`verification_verified` (contract.py:130-131)
is NOT independently caught by a `derive_verdict` fixture asserting the field `True` (the one
`true`-carrying fixture, `vacuous_no_verify.yaml`, asserts only `verification_verified is False`,
not `reviewers_verified is True`). However this is the fail-CLOSED direction: the models default
is `False` = "unverified/vacuous", so the vacuity-HIDING bug direction (a real shortfall reported
as verified) can never arise from dropping the passthrough — it would only ever under-report
verified as unverified (a false-alarm direction, never a silence direction). The actual bug class
FX7 guards (a shortfall/vacuity going SILENT) is doubly covered: the ensemble derivation
(True-vs-False differential) and the writeback emit (True asserted vs False default). Therefore
this coverage micro-observation does NOT weaken FX7's load-bearingness and is NOT a defect.

**Verdict FX7: LOAD-BEARING for VISIBILITY; aggressive degrade correctly DEFERRED (no auto-apply).**

---

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was supplied in the spawn prompt; this review ran in
  standalone mode (fell back to independent verification per Critical Rule #11). No structural
  PASS was relied upon — every claim below was independently tool-verified.

**(b) Independent semantic checks (≥1 required, INV-019):**
- FX3 load-bearingness — verified by a scratch `uv run python` AST harness that reconstructed
  assertion(2)'s `answer_key` resolution against both the buggy and fixed source strings, plus a
  live `dataclasses.fields(SetupAnswers)` read proving `'pr_number' ∉ fields`. (Not a structural
  check — it exercises the trap's actual predicate.)
- FX5 mutation-detection reality — verified by Reading all three differential bodies
  (`test_gate_helper_differentials.py:244-259, 367-379, 439-453`) and confirming each installs a
  concrete `monkeypatch` mutant and asserts the buggy value, plus a 26/26 green baseline run.
- FX7 non-gating guarantee — verified by a full Read of `contract.py` confirming
  `_degraded_reason`/`_halted_reason` never reference any `*_verified` field, and by reading the
  two PENDING DECISION files confirming `Status: PENDING (NOT auto-applied)` +
  `_VERIFICATION_SKIP_EXEMPTIONS` byte-unchanged.

**Verified:** 6/6 | **Unverifiable:** 0 | **Unchecked:** 0 | **Confidence:** 100.0%
**Tool engagement:** Read: 8 | Grep/Bash-grep: 6 | Bash(pytest/python): 4 | Glob: 0
(Tool calls ≥ checklist items — not padded; each maps to a specific claim above.)
**Web research:** none required (all evidence local-file / source-bound); Tavily not invoked.

## Recommendations
- None blocking. All three P0 deterministic backstops are load-bearing; ship as-is.
- Optional (non-blocking, MINOR-adjacent hardening, NOT a defect): add one `derive_verdict`
  fixture asserting `result.reviewers_verified is True` to independently pin the contract.py:131
  positive passthrough. The current gap is fail-closed-safe (models default `False`), so this is
  belt-and-suspenders only.

## QA Complete
