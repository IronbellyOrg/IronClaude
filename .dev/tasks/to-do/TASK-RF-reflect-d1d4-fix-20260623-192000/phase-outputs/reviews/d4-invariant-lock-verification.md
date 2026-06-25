# D4 — TST-4 finding-parity falsifier-EXEMPT label verification (NON-BLOCKING)

**Classification:** LOW, AUTHORIZED (audit reclassified from Drift → Authorized). NON-BLOCKING. NO change to the test.

## EXEMPT-label text found (verbatim, `tests/cli/reflect/test_reviewer_finding_parity.py:13-17`)

> "This test is falsifier-EXEMPT in the fail-before/pass-after sense (it is a
> reachability INVARIANT over the seeded fixtures, not a layer-landing guard); it
> is labeled as such per the task's falsifier-discipline rule."

## Verdict: **PASS**

- The label is **present and correct**. The test is genuinely a reachability invariant
  over the seeded eval fixtures (it asserts every seeded defect is statically reachable
  via the restricted `{Read, Grep, Glob}` tool set, i.e. none requires Bash/execution to
  detect), NOT a layer-landing guard — so it legitimately passes on the current tree.
- The parent task's Key Constraint explicitly authorizes this: "any invariant lock that
  passes on the current tree is falsifier-EXEMPT and MUST be labeled as such." The test
  complies exactly.
- The /sc:reflect audit reclassified the original Reviewer-1 "Drift" finding to
  **Authorized** on this basis.

## No change made or required

`tests/cli/reflect/test_reviewer_finding_parity.py` is **NOT modified** by this task.
The EXEMPT label is sanctioned; touching the test would be a spurious change.

## Follow-Up (OPTIONAL future enhancement — NOT this task)

A heavier **live restricted-vs-all-tools recall comparison** test (two real reflect runs:
one with the restricted `reflect-reviewer` agent, one with an all-tools persona, asserting
identical seeded-defect recall) would upgrade TST-4 from a static-reachability proxy to a
live parity check. `research/05 §4` deferred this as more expensive than the static proxy.
Recorded here as an OPTIONAL Follow-Up only — out of scope for this remediation task.
