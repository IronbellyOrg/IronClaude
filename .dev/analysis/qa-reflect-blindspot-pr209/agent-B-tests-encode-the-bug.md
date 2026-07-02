# Agent B — "The Tests Encoded the Bug": Why the RF QA + Tier-2 Reflect Audit Missed F2 & F4 (PR #209)

**Date:** 2026-07-02
**Angle:** Test-vs-code circularity behind F2 (app-slug override) and F4 (all-None `_path_resolves`), and how the Phase-4 test-QA gate amplified it.
**Verdict:** Both bugs were *inside the test oracle*, so every reviewer that checked "tests-vs-code consistency" ratified them. The RF heterogeneous-reviewer design was supposed to break shared-blindspot circularity but didn't — because no reviewer validated tests-vs-external-truth (the spec / a differential property).

Commits: `dc507305` (feat, pre-fix) → `f6a32e9a` (F2 fix + F4 test correction) → `21d4b8e0` (F4 code fix).

---

## 1. F4 — THE SMOKING GUN: the test author SAW the quirk, wrote a comment explaining it, and encoded it as *expected behavior*

### 1a. The buggy resolution helper (pre-fix)

`git show dc507305:src/superclaude/pr_submit/contract_setup/candidate.py`, `_path_resolves` (starts L356):

```python
def _path_resolves(payload: dict[str, Any], path: str | None) -> bool:
    if not path:
        return False
    normalized = path.replace("[]", "")
    current: Any = payload
    for part in normalized.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list):
            current = [item.get(part) for item in current if isinstance(item, dict)]
        else:
            return False
        if current in (None, []):   # <-- [None, None] is neither None nor [] → passes
            return False
    return True
```

When `severity` is missing on **every** element of a non-empty `reviews` list, the comprehension yields `[None, None]`. `[None, None] in (None, [])` is `False`, so the guard does **not** fire and the function returns `True` = "resolved". A findings/severity path is thus falsely marked **observed**, which flows into `FieldProvenance(observed=True)` and affects **lockability** (a MUST_OBSERVE field is satisfied by a surface that carries no data).

### 1b. The test that PINNED the bug — and its self-incriminating comments

`git show dc507305:tests/pr_submit/test_contract_setup_validation.py`:

`test_severity_path_null_is_allowed_but_recorded_not_field_backed` (L130) documents the quirk in its own API note (L131–136):

> ```python
> # API note: _observed_severity_path probes reviews[].severity, comments[].severity,
> # then check_runs[].conclusion, and _path_resolves treats a non-empty list of
> # all-None as "resolved" (a list of None != []). So ANY present review OR comment
> # makes a severity path "resolve". A genuinely-null (not field-backed) severity path
> # ... the field is None and its provenance is recorded as NOT observed.
> ```

Then `test_severity_path_present_is_field_backed_and_distinct_from_null` (L156) **asserts the buggy result** and rationalizes it in the comment (L157–161):

> ```python
> # A present Augment review makes the observed severity path resolve and be
> # field-backed. API note: reviews[].severity is checked first and "resolves" for a
> # non-empty reviews list, so the derived path is reviews[].severity (NOT
> # comments[].severity) ...
> ...
> assert candidate.contract.severity_field_path == "reviews[].severity"   # WRONG
> assert severity_prov.observed is True
> assert severity_prov.evidence_ref == "payload.severity"
> ```

The fixture supplies a review with **no** `severity` and an inline comment that **does** carry `severity: high`. The honest answer is `comments[].severity`. The test asserted `reviews[].severity` — the *bug's* output — and its comment explicitly explained *why* the all-None list "resolves". The author encountered surprising behavior, reverse-engineered it from the code, wrote it down as an "API note," and froze it as the expected value.

### 1c. The fix confirms it was a bug, not a spec choice

`21d4b8e0` rewrote `_path_resolves` to drop None values (`if isinstance(item, dict) and (value := item.get(part)) is not None`) so an all-None list collapses to `[]` = unresolved, corrected the assertion to `severity_field_path == "comments[].severity"`, and **added** `test_severity_path_all_none_does_not_resolve` whose docstring reads: *"Regression (PR #209 finding F4): _path_resolves treated an all-None list as resolved..."*. The corrected comment now says the OLD one was wrong: *"_path_resolves no longer treats an all-None list as 'resolved'."*

**This is the definition of "the test encoded the bug": the assertion and the code produced the same wrong answer because they were written from the same (flawed) mental model, in the same sitting, from the same source doc.**

---

## 2. The Phase-4 adversarial QA lenses reviewed the bug-pinning tests and PASSED — because they checked "asserts a concrete behavior / coverage present", not "is the asserted behavior CORRECT"

All three Phase-4 test lenses returned **VERDICT: PASS** over exactly the files containing the pinned bug.

### 2a. test-structure lens (`phase-4-qa-test-structure.md`) — "assume test-smells" but the smell it hunts is the wrong one

Checklist item 1 is *"Tests assert BEHAVIOR, not identity/type (no `is not None`-only, no tautologies)"*. Its PASS evidence (L26):

> "Assertions test state outcomes (`d.state is ContractState.X`), derived values (`d.next_command == "<exact string>"`), provenance flags (`prov.observed is False`) ... — a real invariant, not a tautology."

The lens' definition of a good assertion is **"asserts a concrete derived value / state outcome."** `assert candidate.contract.severity_field_path == "reviews[].severity"` **passes that bar perfectly** — it is a concrete derived-value assertion. The lens has no rule "is the concrete value the SPEC-correct one?", so a precisely-wrong assertion is indistinguishable from a precisely-right one. Final line (L69–71): *"Green light. The Phase 4 test suite is structurally sound: real symbols ... behavioral assertions throughout."*

### 2b. acceptance-traceability lens (`phase-4-qa-acceptance-traceability.md`) — counted EXISTENCE, not answer-flow correctness

VERDICT PASS, "28/28 ... Confidence: 100.0%" (L11, L19). The Q10 row (L44) lists **both** severity tests — *including the one asserting the bug* — as coverage and stamps it "existence + behavioral":

> `| 10 | severity_field_path | test_severity_path_null_is_allowed... + test_severity_path_present_is_field_backed_and_distinct_from_null (validation) | existence + behavioral |`

The lens verified *a dedicated test exists and asserts something*, not *the asserted value is right*. Its own methodology statement (L21) — verifying against `LockGate.CHECK_IDS` and `merged-requirements.md §6` — checks that a **check-ID/predicate is named**, which is satisfiable by any test that touches the predicate regardless of the assertion's truth value.

Most damning: **Finding 1 (L95) walked right up to F4 and looked away.** It flagged the `paths_resolve` predicate as having *"asymmetrically weaker"* coverage on the completion-signal half vs the findings-locus half, and recommended *"add one positive test asserting `review_completeness_signal` resolves."* It was auditing the exact resolution machinery that was broken — but framed the gap as *missing a positive test*, never asking whether the *existing* positive resolution was itself lying. It treated `_path_resolves` as a trustworthy oracle instead of the thing under test.

The `final-qa-qualitative-domain-accuracy.md` lens did the same (its item 2 PASS): *"severity_field_path observed only if a path resolved (candidate.py:88-91)"* — it trusted "a path resolved" as ground truth rather than auditing whether `_path_resolves` resolves *correctly*.

### 2c. edge-case-completeness lens (`phase-4-qa-qualitative-edge-case-completeness.md`) — 8/8 edge cases, but the all-None edge case was not in its list

VERDICT PASS, "8/8 edge cases verified = 100%". Its edge-case matrix covers empty-payload, non-Augment, repo-mismatch, cross-PR-shape-only, etc. — none of which is *"a surface present but the specific key absent on every element."* The all-None case is precisely the edge case a resolution helper most needs, and it never made the list, because the list was derived from the same requirements doc the code was written from. The edge cases the author *thought of* are the edge cases the tests *cover* — a closed loop.

---

## 3. Root cause: single mental model authored code + tests + (in-context) QA — a shared-blindspot circularity the RF design was meant to break but didn't

### 3a. Shared provenance

Per `BUILD-REQUEST.md` (L3, L41), both the implementation and the test scope were derived from the **same two source docs**: `design.md` and `merged-requirements.md §4` (the 16 questions). The Phase-4 tests were authored by rf-analyst subagents against those same docs. So:

- **Code** encodes model M's understanding of "resolve a path."
- **Tests** encode model M's understanding of "resolve a path" — and were even *reverse-engineered from the code's behavior* (the "API note" comments are literal descriptions of what the code does, not what the spec requires).
- **QA lenses** run in-context against code+tests, checking they *agree with each other*.

When code and test share the bug, "code ⇔ test consistency" is **maximally green** precisely when the bug is present. Every RF reviewer measured consistency; none measured correctness against an external oracle (the spec's intent, or an independent property like "resolution requires ≥1 element to actually carry the key").

### 3b. Why heterogeneous reviewers didn't help

RF's heterogeneous-reviewer / blind-calibration machinery neutralizes **representational bias in judging a given artifact**. It does not help when *the reference the reviewers judge against is itself the corrupted artifact.* Different model classes all reading "the test asserts `reviews[].severity` and the code produces `reviews[].severity`" will all conclude CONSISTENT. Diversity of judge doesn't rescue a shared, wrong ground-truth.

The Tier-2 `/sc:reflect` post-audit (`reflect/post/156f28292b4d/t2-adversarial/reflect-review-consolidated.md`) confirms this vividly: its **entire** finding set is process/state-fidelity (frontmatter drift, unchecked completion gate, empty `reflect_post`) — Findings #1–#4 are all "gate not ticked" / "state drift." It **never inspected a single test assertion for correctness**, never mentioned `app_slug`, `all-None`, `_path_resolves`, or `severity_field_path`, and actually cited *"its changed-file test set passes"* as evidence **in favor** of the work. Reflect audited work-vs-protocol, not tests-vs-truth — the identical blind spot, one level up.

### 3c. Grounding the F2 gap — "16 IDs present" is satisfiable with zero behavioral answer-flow

F2: the app-slug operator override was read from `answers.decline_detection_fields.get("augment_app_slug")` (`dc507305:candidate.py:167`, inside `_selected_app_slug`) — a `dict` bucket semantically meant for *decline-detection evidence*, not identity override. Pre-fix `SetupAnswers` (`dc507305:questions.py:15`) had **no** `augment_app_slug` field at all (the full field list ends at `next_step`; `f6a32e9a` added `augment_app_slug: str | None` at L28). No test in `test_contract_setup_questions.py` exercised the override branch — the pre-fix test list is: `..._contains_all_16_questions_in_order`, `..._defaults_are_suggestions...`, `..._multiple_augment_identity_candidates...` (login identity, *not* app-slug), `..._unobserved_emission_shape...`, `..._polling_expected_result...`, `..._missing_decline_evidence...`. No override-flow test.

The acceptance-traceability lens still scored 16/16 because **`app_slug` is not one of the 16 question IDs** — it's a derived contract field. Its coverage test of record is `test_setup_question_sequence_contains_all_16_questions_in_order`, which asserts `[q.id for q in SETUP_QUESTIONS] == EXPECTED_QUESTION_IDS` — pure *existence + order* of ID strings. **An ID being present in an ordered list is fully satisfiable with zero test that any answer actually flows through to the derived contract.** So the operator-override path — where the answer is read from the wrong bucket — has no traceability obligation at all under "16 IDs present," and slid through untested. The QA measured the *presence of the question*, never the *fate of the answer*.

---

## 4. Recommended RF changes (2–3 concrete)

1. **Mandatory property/differential test for every resolution/predicate helper.**
   Any helper that returns a boolean/path used as a *lockability or observed-provenance gate* (`_path_resolves`, `_observed_*`, `required_unobserved`) must ship a **property test** asserting the *negative*: "a surface present but the target key absent on every element does NOT resolve." This is the exact test `21d4b8e0` added post-hoc (`test_severity_path_all_none_does_not_resolve`). Make the RF test-authoring lens FAIL if a gate helper has only positive-resolution tests and no all-absent / all-None negative. Positive-only coverage of a gate is a structural smell, not "green."

2. **"Assertions justified against the SPEC, not the code" QA rule (external-oracle gate).**
   Add a Phase-4 lens check: for each concrete-value assertion on a *derived* field, the reviewer must cite the **spec/requirements line** that mandates that value — not the source function that produces it. If the only justification available is "this is what the code returns" (as every "API note" comment here was), the assertion is UNVERIFIED-against-truth and the item cannot be marked covered. This directly breaks the code⇔test consistency loop by forcing an external reference.

3. **A test comment that rationalizes surprising/quirky behavior is a MANDATORY ESCALATION, not an accepted API note.**
   Introduce a lint/lens rule: any test comment containing "quirk", "API note", "treats ... as", "surprising", "resolves for ... even though", or otherwise *explaining why an assertion holds despite being counter-intuitive* is a **HALT-and-flag** signal. The author has, by writing the explanation, demonstrated they saw non-obvious behavior — that is exactly the moment to ask "is this a bug?" not "let me pin it." Route such comments to an independent reviewer with the framing "confirm this behavior is spec-required, not spec-accidental."

**(Bonus, for F2 specifically):** acceptance-traceability must trace *answer-flow*, not *ID existence*. For every question whose answer feeds a derived contract field, require a behavioral test that sets the answer and asserts the derived field changes — and FAIL if an operator-override branch (a distinct code path reading the answer) has no test. "16 IDs present" must be downgraded from "covered" to "declared" until answer-flow is demonstrated.
