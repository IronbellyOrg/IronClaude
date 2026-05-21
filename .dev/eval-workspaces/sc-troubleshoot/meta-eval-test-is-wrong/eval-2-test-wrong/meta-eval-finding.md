# Meta-Eval Finding — eval-2-test-wrong

## Did v2 correctly identify the test as the bug?

**Yes — emphatically, at every tier.** The Tier 1 hypothesis card opens with the cause-class explicitly labelled "Test
infrastructure (stale test against new requirement) — NOT a code bug". All three Tier 2 agents independently converged on
the same diagnosis (the test is wrong, the code is right) at calibrated confidence 0.90 each. The final report's Summary
leads with "**The TEST is the bug, not the code.**" in bold. The Proposed Fix section has a dedicated "Files that MUST
NOT change (asymmetric-cost guard)" subsection naming `api/session.py`. The Alternative Fixes Considered section
explicitly names the "fix the code" direction as "the DANGEROUS wrong answer".

## Where in final-report.md / hypothesis cards is the "test is wrong" insight stated?

Multiple places, in unambiguous prose:

1. **final-report.md Summary**, sentence 1: "**The TEST is the bug, not the code.**" (bolded in source)
2. **final-report.md Summary**, sentence 4: "**The fix is to rewrite the test assertions to match the per-device contract.
   Do NOT modify `api/session.py` — doing so would regress the shipped feature.**" (bolded in source)
3. **final-report.md Diagnosis → Cause class**: "Test infrastructure — stale test against intentionally-changed production
   contract."
4. **final-report.md Proposed Fix**: explicit "Files to change: `tests/api/test_user_session.py`" vs. "Files that MUST NOT
   change (asymmetric-cost guard): `api/session.py`".
5. **final-report.md Alternative Fixes Considered → Fix A**: "Rejected because: directly contradicts the shipped spec...
   This is the DANGEROUS wrong answer and is the entire reason this report explicitly flags the asymmetric-cost risk".
6. **final-report.md Risk + Rollback → first bullet**: "Asymmetric-cost risk (PRIMARY): the largest risk in this
   diagnosis is that a downstream agent... treats the failing test as evidence the code is broken and 'fixes' the code."
7. **final-report.md Next Steps**: "When you do, the task brief MUST forbid edits to `api/session.py`."
8. **tier1-hypothesis.md Cause class**: "Test infrastructure (stale test against new requirement) — NOT a code bug"
9. **tier1-hypothesis.md Proposed Fix**: "**Do NOT change `api/session.py`.** Changing it to make the current test pass
   (e.g. dedup by user_id) would re-introduce the old single-session behaviour and regress the shipped feature."
10. **tier2-quality-engineer-hypothesis.md Risks**: "the dominant risk is the asymmetric-cost failure mode... The fix
    MUST be flagged as 'update test, not code' in any handoff."
11. **tier2-root-cause-analyst-hypothesis.md Risks**: "**The fix is in `tests/`, never in `api/session.py`.**"
12. **candidate-fixes.md**: the only consensus fix is "Rewrite test assertions to validate per-device contract; do NOT
    change api/session.py" — the title of the section literally names the constraint.

The "test is wrong" insight is structurally bracketed at every read-position in the report. It is not buried, not hedged,
and not contingent on the reader pulling a thread.

## How would the proposed `test_is_wrong: true` flag in the output contract have changed this run?

**Answer: it would have been set, but the prose already covers the same ground.** Here is the careful breakdown:

### Where the flag would have been set automatically

A `test_is_wrong: true` flag would have been emitted, based on these structural signals already produced by Tier 2:
- The chosen cause class is "Test infrastructure".
- The "Files that MUST NOT change" list contains a production-code file (`api/session.py`).
- The "Files to change" list contains ONLY test files.
- Three independent agents converged on this asymmetry.

The skill could deterministically detect this combination and set the flag. There is no ambiguity in this eval.

### What the flag would and would not improve

What the flag WOULD improve:
- **Machine-readable signal for Tier 3 task-builder**: an automated remediation chain that consumes the output dict
  would not need to parse prose to discover the constraint. A boolean is harder to misread than English.
- **Defensive coding for downstream agents**: a future "auto-fix" wrapper script that calls `/sc:troubleshoot` then
  immediately invokes a code-edit agent would be able to gate behaviour on a single field rather than NLP over the
  Risk section.
- **Auditability across many runs**: at scale, a `test_is_wrong: true` field could be indexed and reviewed in
  aggregate — a quality signal for engineering productivity.

What the flag WOULD NOT improve (in THIS run):
- **The diagnosis itself.** The prose already names the test as the bug seven times across the report and ten+ times
  across the hypothesis cards. A human reader who misses all of those will not be saved by a frontmatter boolean.
- **The immediate user's understanding.** The user who invoked `/sc:troubleshoot` reads final-report.md, not the output
  dict. They will see the bolded "The TEST is the bug, not the code" within the first 100 words.

### The load-bearing question

The flag is load-bearing **only in the context of an automated downstream chain** (Tier 3 task-builder, or any
auto-apply-fix wrapper). For a human reader of the report, it is form, not substance. **But the asymmetric-cost danger
DOES naturally surface in any automated chain** — task-builder will read the "Files to change" list literally and produce
a task that targets only the test. The Risk section is also passed forward. So even the automation case is mostly
covered by existing structure.

The remaining gap the flag would close: a downstream agent that, despite the report, "tries to be helpful" by reasoning
about whether the named test fix is really the right one and decides to look at the production code anyway. A boolean
flag named `test_is_wrong` short-circuits that reasoning. **That is a real but narrow defensive value.**

## Verdict on the INCORPORATE recommendation

**(b) USEFUL** — v2's prose diagnosis already names the test as the bug clearly and repeatedly. The flag is NOT
load-bearing for the human-reader case (the answer is on the first line of the Summary, in bold, and repeated at every
section). However, a structured `test_is_wrong: true` flag in the output contract WOULD provide non-trivial defensive
value for the automated-downstream-chain case (Tier 3 task-builder, auto-apply wrappers, fleet-level aggregation /
auditability). It is a small, cheap addition that closes a narrow but real gap. It is NOT essential — v2's diagnosis is
correct and clear without it — but it is genuinely useful.

The recommendation should be INCORPORATE-AS-FORTIFICATION (not INCORPORATE-AS-FIX): document it as a machine-readable
mirror of what the prose already establishes, set automatically when the structural signals (cause class = Test
infrastructure + "MUST NOT change" list contains non-test files) match. Do not treat it as the primary mechanism for
conveying the asymmetric-cost danger — the prose Risk section and the dual Files-to-change / Files-that-MUST-NOT-change
sections in the report template do that job already.

## Tier reached + confidence

- **Tier reached**: 2 (escalation_reason: `intermittent` — fired on the "passes locally but fails 4 out of 5 runs in CI"
  phrase, NOT on low confidence; Tier 1 confidence was 0.90)
- **Tier 2 calibrated confidence**: 0.90 across all three cards
- **Adversarial debate**: skipped (consensus on single fix; per Wave 3 exit criteria, debate would have wasted tokens)
- **Final report status**: partial (because of inline-vs-disk grounding gap; not because of diagnostic uncertainty)
- **Diagnostic confidence in "test is wrong"**: very high (3 independent agents + Tier 1 all converged; the test's own
  inline comment self-documents the gap)

## Token / wall-clock cost (rough)

- Wave 0–1: ~2 min, ~4k Claude tokens
- Wave 2 escalation gate: ~30 sec, ~0.5k tokens
- Wave 3 (3 parallel hypothesis agents + per-card calibration): ~4 min, ~12-15k tokens
- Wave 4: skipped (consensus)
- Wave 5 (synthesis + evidence-validation inline): ~3 min, ~5k tokens
- **Total**: ~7-10 min wall-clock, ~22-25k Claude tokens

This is at the lower end of the Tier-2-no-adversarial band in the skill's token cost profile (target 15-30k), reflecting
that the grounding was thin (inline only) so agents didn't burn extra tokens on disk reads.
