# Agent D — F4: The Known Quirk That Was Rationalized and Shipped

**Scope:** Reconstruct the "noted but dismissed" decision chain for bug F4 (`candidate.py::_path_resolves()` treating an all-None list as "resolved"), fixed in `21d4b8e0`.
**Method:** Pre-fix git blobs (`dc507305`), Phase-4 + final QA reports, reflect post artifacts, auggie confirmation of live behavior.
**Date:** 2026-07-02

---

## 0. The bug, confirmed against source

Pre-fix `_path_resolves` (git `dc507305:src/superclaude/pr_submit/contract_setup/candidate.py:356-370`):

```python
def _path_resolves(payload: dict[str, Any], path: str | None) -> bool:
    ...
    for part in normalized.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        elif isinstance(current, list):
            current = [item.get(part) for item in current if isinstance(item, dict)]
        else:
            return False
        if current in (None, []):   # <-- [None, None] is NOT in (None, []) → passes
            return False
    return True
```

When a list element is a dict but the key is missing on **every** element, the comprehension yields `[None, None, ...]` — a non-empty list of Nones. The guard `if current in (None, []):` does not catch it, so the loop continues and the function returns `True` = "resolved" = `observed=True`.

**Why this affects lockability (auggie-confirmed, current tree):**
- `_path_resolves` sets `FieldProvenance.observed` for `findings_locus` (`candidate.py:259, 268`) and `review_completeness_signal` (`candidate.py:299, 311`).
- `findings_locus` **is in `MUST_OBSERVE_FIELDS`** (`candidate.py:18-25`), so `required_unobserved()` blocks lock when it is not observed (`candidate.py:47-60`).
- `lockgate.py:_paths_resolve` (`lockgate.py:119-125`) gates on `findings.observed AND signal.observed`.
- Net: a payload whose findings/severity key is absent on every element could be falsely marked `observed=True` and pass the lock gate. This is a real correctness/lockability defect, not cosmetic.

The fix (`21d4b8e0`) drops None entries so an all-None list collapses to `[]` (unresolved).

---

## 1. Chain of custody — WHO saw it, WHAT they wrote, WHICH rule downgraded it

### Touchpoint A — Phase-4 test author (rf-analyst) LAUNDERED the bug into a spec

The author who wrote `tests/pr_submit/test_contract_setup_validation.py` did not miss the quirk — they **discovered it, understood it precisely, and wrote a comment describing it as the API's design.** Verbatim, `git show dc507305:tests/pr_submit/test_contract_setup_validation.py:131-135` (test `test_severity_path_null_is_allowed_but_recorded_not_field_backed`):

> ```
> # API note: _observed_severity_path probes reviews[].severity, comments[].severity,
> # then check_runs[].conclusion, and _path_resolves treats a non-empty list of
> # all-None as "resolved" (a list of None != []). So ANY present review OR comment
> # makes a severity path "resolve". A genuinely-null (not field-backed) severity path
> # is therefore only reachable when reviews AND comments are both empty. That is the
> # honest null case: the field is None and its provenance is recorded as NOT observed.
> ```

And in `test_severity_path_present_is_field_backed_and_distinct_from_null` (`dc507305:...:157-161`):

> ```
> # A present Augment review makes the observed severity path resolve and be
> # field-backed. API note: reviews[].severity is checked first and "resolves" for a
> # non-empty reviews list, so the derived path is reviews[].severity (NOT
> # comments[].severity) — the point of this test is field-backed (observed=True) vs
> # the null case above ...
> ```

The author literally wrote the sentence `a list of None != []` — the exact mechanism of the bug — and then **wrote a test that asserts the buggy output** (`assert candidate.contract.severity_field_path == "reviews[].severity"` for a review with no `severity` field). The label "API note" converted a surprising behavior into a documented contract. This is the origin event: the quirk was pinned as expected, not flagged as suspicious.

### Touchpoint B — Phase-4 edge-case QA never named it; it graded adjacent INFOs

`phase-4-qa-qualitative-edge-case-completeness.md` (VERDICT: PASS) does **not** mention `_path_resolves`, all-None, or the severity quirk at all. Its Findings section (lines 27-30) is INFO-only, e.g.:

> `F-2 (INFO): item 4 tests hash-absence (bool(evidence.sha256) presence gate) — the honest implemented behavior; no separate wrong-but-present-hash path exists.`

The edge-case lens catalogued which edge cases have *a* test, saw the two severity tests in its matrix row (indirectly, via acceptance-traceability), and treated presence-of-a-passing-test as coverage. It never asked whether the pinned behavior was *correct*. The word "honest" recurs here and in the test comment — the same rationalization vocabulary.

### Touchpoint C — Phase-4 acceptance-traceability QA rubber-stamped the tests as behavioral coverage

`phase-4-qa-acceptance-traceability.md:44`:

> `| 10 | severity_field_path | test_severity_path_null_is_allowed_but_recorded_not_field_backed + test_severity_path_present_is_field_backed_and_distinct_from_null (validation) | existence + behavioral |`

The traceability lens confirmed the field *has* behavioral tests and moved on. Mapping a field to a test that pins the wrong behavior scores as "covered."

### Touchpoint D — the DEEPEST miss: adversarial domain-accuracy QA read `_path_resolves` and blessed it

`final-qa-qualitative-domain-accuracy.md` opened with an explicit adversarial stance (line 10): *"Stance: Adversarial — assumed a state/provenance/lockability rule was wrong; verified every rule against actual source."* Its overall verdict was **PASS**. Row 2 (line 23) is the only place in the entire QA/reflect corpus that cites `_path_resolves` by name — and it uses it as **evidence of correctness**:

> `findings_locus user answer → observed = _path_resolves(...) (L255). severity_field_path observed only if a path resolved (L88-91). required_unobserved() (L47-60) blocks lock when any MUST_OBSERVE field lacks observed provenance. Confirmed no field is hardcoded observed=True without a payload-resolution predicate ...`

The adversarial reviewer confirmed the *shape* of the invariant ("observed is gated by a resolution predicate") without testing the *predicate itself* against an all-None input. It trusted `_path_resolves` as the arbiter of truth instead of adversarially probing it. The one lens designed to catch this looked directly at the buggy helper and validated it.

### Touchpoint E — consolidation: zero-tolerance rule defeated by pre-classification

`phase-4-qa-consolidated.md:18-20` states the decision rule:

> `FAIL because at least one report contains an issue of any severity.`

The rule is genuinely zero-tolerance — Phase 4 did FAIL (on an unrelated CRITICAL redaction test-guard, P4-QA-001, plus a MINOR). But the F4 quirk **never entered the issue ledger**: no lens filed it as an issue. It was pre-classified as an accepted "API note" (Touchpoint A) and as passing coverage (B, C) or a correct invariant (D). "FAIL on any issue" cannot fire on an item that no lens ever labeled an issue. The quirk rode through a FAIL-and-fix cycle untouched, because the fix agent was scoped to the two filed findings.

### Touchpoint F — Reflect: silent

Across the full reflect post tree (`.dev/tasks/.../reflect/post/156f28292b4d/`) — the adversarial `invariant-probe.md`, the t2-swarm reviewers, and `reflect-review-consolidated.md` — there is **zero mention** of `_path_resolves`, `severity_field_path`, all-None, or severity resolution (grep-confirmed: no match in any reflect artifact). The adversarial invariant-probe's only surfaced item (INV-002) concerns sprint step 5.6/5.7 gate sufficiency, not the contract helper. Reflect audited plan-vs-execution deviations and never descended into the resolution predicate. The bug survived to `21d4b8e0`, where Augment's round-2 PR review finally caught it.

---

## 2. Root cause

RF has **no rule that "behavior a reviewer felt compelled to explain in a comment must be escalated to a correctness question."** The failure is not a missed edge case — it is an *inverted* one: an adversarial author **understood the quirk well enough to document it precisely** and, in the act of documenting it, laundered it from "surprising behavior" into "accepted API property." Every downstream gate then read that laundered classification as ground truth:

- The test comment turned the bug into a spec ("API note", "honest null case").
- Coverage/traceability lenses scored presence-of-a-test, not correctness-of-the-pinned-value.
- The adversarial domain-accuracy lens trusted the buggy helper as its own oracle instead of probing it.
- Zero-tolerance consolidation ("FAIL on any issue") is structurally defeated because the issue was pre-classified INFO/accepted **by the author**, so it never became an issue to consolidate.

The system's strongest control (a FAIL-if-any-issue gate + an explicitly adversarial reviewer) is exactly the control that a well-written rationalizing comment neutralizes: the comment lowers everyone's prior that anything is wrong.

---

## 3. Concrete RF changes

1. **Rationalization-comment escalation rule (highest value).** Any test/source comment that *explains or justifies a non-obvious behavior* — trigger phrases like "API note", "quirk", "treats X as Y", "honest ... case", "note: ... != ..." — MUST auto-create a `needs_human_decision` correctness ticket that HALTS the phase gate until a human (or a second, isolated lens) confirms the behavior is intended, not merely observed. A comment that says *why the weird thing is fine* is the single strongest signal that the weird thing is a bug; RF currently treats it as documentation. The author who can articulate `a list of None != []` has already done the hard diagnostic work — the framework must not let them also render the verdict.

2. **A lens cannot self-close a finding about a helper it validated by trusting that helper.** When a QA lens cites a predicate function (e.g. `_path_resolves`) as the *reason* an invariant holds, it MUST be required to attach an adversarial input probe for that predicate (all-None list, empty list, missing key, wrong type) rather than asserting "observed is gated by a resolution predicate" from the call-site shape. INFO/PASS findings about resolution/validation/lockability logic cannot be self-closed by the authoring or reviewing lens; they escalate to a second isolated reviewer with a mandate to break the predicate.

3. **Lockability-deciding helpers require an adversarial property test, not a narrative acceptance test.** Any helper whose return feeds `MUST_OBSERVE_FIELDS` / `required_unobserved` / a lock gate (`_path_resolves`, `_paths_resolve`, `required_unobserved`) must ship with a property/parametrized test enumerating the falsy-but-truthy boundary cases (`[None]`, `[None, None]`, `[]`, `[{}]`, missing key) — asserting `observed is False` for each. A test whose comment *narrates* why an odd output is acceptable is disqualified as the coverage-of-record for that helper.

---

## Summary

Bug F4 was not missed — it was **diagnosed, documented, and pinned as intended** by the Phase-4 test author, who wrote (verbatim, `dc507305:test_contract_setup_validation.py:131-135`) that `_path_resolves` "treats a non-empty list of all-None as 'resolved' (a list of None != [])" and labeled it an "API note ... the honest null case," then wrote a test asserting that buggy output. Downstream, the edge-case lens filed only adjacent INFO notes (F-1..F-4) and never named the quirk; acceptance-traceability scored the field as "behavioral covered" (line 44); and the **adversarial** domain-accuracy lens — the one control designed to catch this — read `_path_resolves` directly (line 23), cited it as *proof* that "no field is hardcoded observed=True without a payload-resolution predicate," and returned PASS. Consolidation's zero-tolerance rule ("FAIL on any issue," `phase-4-qa-consolidated.md:20`) did fire Phase-4 to FAIL, but on an unrelated redaction guard — the F4 quirk never entered the issue ledger because it was pre-classified as an accepted API property by its own author. No reflect artifact (invariant-probe, swarm, consolidated) mentions it at all. Augment's round-2 PR review finally caught it (`21d4b8e0`). Root cause: RF has no rule forcing a *rationalized* behavior to be re-litigated as a correctness question — a reviewer who writes the comment explaining why the weird thing is fine has laundered a bug into a spec, and zero-tolerance consolidation is powerless against an issue the author pre-closed.

**Single most important recommendation:** Add a rationalization-comment escalation rule — any test/source comment that explains or justifies non-obvious behavior ("API note", "quirk", "treats X as Y", "honest case", "X != Y") auto-creates a `needs_human_decision` correctness ticket that HALTS the phase gate until an isolated second lens confirms the behavior is intended, not merely observed. The ability to articulate the quirk must never grant the authority to accept it.
