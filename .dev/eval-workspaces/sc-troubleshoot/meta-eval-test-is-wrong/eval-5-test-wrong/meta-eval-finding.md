# Meta-Eval Finding — eval-5-test-wrong

## Did v2 correctly identify the test as the bug?

**Yes — clearly and decisively.** Evidence:

- REPORT.md Summary opens with: "**The test is the bug, not the code.**" (first sentence, bold).
- REPORT.md Diagnosis -> "Root cause": "A regression test was added that encodes an inverted/invented policy."
- REPORT.md Proposed Fix: "**Delete** `test_doctor_rejects_workspace_default`" plus explicit "**Files that MUST NOT change**" listing the three production files that a careless remediation would touch.

**Crucially, v2 read the OPS-002 policy doc BEFORE forming its hypothesis.** The Wave 1 grounding step (audit.log) explicitly Reads `docs/eval/scratch-roots.md` and `src/superclaude/cli/eval/config.py` as the first action. This is the load-bearing step: trusting the test's claim ("any path containing .dev/eval-workspaces/ should be rejected") without verifying it against the canonical policy would have produced the catastrophic "tighten the code" diagnosis. The v2 protocol's "Hallucination contract" + Wave 1's "Ground the symptom in real code" step are exactly the structural defenses that forced policy-doc grounding before hypothesis formation.

## Where in REPORT.md / hypothesis cards is the "test is wrong" insight stated?

Quoted lines:

- REPORT.md, Summary (line 1): "**The test is the bug, not the code.**"
- REPORT.md, Diagnosis Root cause: "A regression test was added that encodes an inverted/invented policy. It asserts the rejection of a path family (.dev/eval-workspaces/) that the OPS-002 allowlist never claimed jurisdiction over."
- REPORT.md, Proposed Fix: "Delete test_doctor_rejects_workspace_default... Files that MUST NOT change: src/superclaude/cli/eval/config.py..."
- tier1-hypothesis.md, Claim: "the **test is wrong as written** because the assertion's *rationale* confuses the allowlist (eval-runs) with the unrelated dev-workspace directory (eval-workspaces)"
- tier2-security-engineer-hypothesis.md, Claim: "The danger is not the test failure itself — it's the remediation path a less-careful diagnosis would propose." (then enumerates the three anti-fixes)
- candidate-fixes.md: explicit "**Anti-fixes**" section enumerating A1-A4 with rejection reasons, recorded so "a downstream remediation chain cannot resurrect them."

## How would the proposed `test_is_wrong: true` flag in the output contract have changed this run?

**Almost no operational difference for this case.** The flag would have been set automatically (the prose diagnosis trivially supports a yes/no extraction). But the prose diagnosis is already crystal clear: the Summary leads with the conclusion in bold, the "Files that MUST NOT change" section enumerates the production files to leave alone, and the candidate-fixes.md anti-fixes section catalogs the four bad code-side remediations a less-careful chain might choose.

Where the flag *might* help: a **downstream automated remediation chain** (Tier 3 task-builder + `/task` execution) that parses the structured output dictionary rather than reading REPORT.md prose. With `test_is_wrong: true` in the contract, the task-builder skill could gate on the flag and refuse to generate a task that touches production code, forcing the operator to acknowledge the diagnosis before any automated change. Without the flag, the chain would have to parse "Files to change" vs "Files that MUST NOT change" from prose — feasible but more fragile.

So: not load-bearing for *this run*. Possibly load-bearing for the *downstream automation contract*.

## Verdict on the INCORPORATE recommendation

**(b) USEFUL — but not essential.**

Rationale:
- v2 got the diagnosis right in prose, with full asymmetric-cost reasoning, with the "Files that MUST NOT change" sentinel, and with an explicit anti-fixes catalog. A human reading REPORT.md cannot miss the conclusion.
- The flag's value is at the *machine-readable contract* boundary: downstream skills (task-builder, /sc:reflect) that gate behavior on the output dictionary benefit from a structured signal rather than parsing prose for "test is wrong" or "do not modify production code."
- The flag is also small (one bool in the dict), low-cost to set (already implied by the prose), and forward-compatible with the Tier 3 chain's evolution.
- NOT essential because the prose already does the load-bearing work for any human reader, and the anti-fixes catalog already addresses the worst failure mode (automated remediation choosing a code-side fix).
- The flag would shift it from "needs careful prose-reading" to "single boolean gate" — a small but real improvement in automation safety, not a load-bearing fix.

## Tier reached + confidence

- **Tier reached**: 2 (escalated from Tier 1 due to multi_domain — test correctness + security-adjacent allowlist policy)
- **Wave 4 (adversarial debate)**: SKIPPED per "all agents converge with high confidence" rule
- **Final confidence**: 0.94 (consensus among 3 independent Tier 2 cards, calibrated 0.90-0.92 each)
- **Status**: success
- **Escalation reason**: multi_domain

## Token / wall-clock cost (rough)

- Auggie tokens (offloaded): ~12k (two Wave 1 queries + three Wave 3 queries)
- Claude tokens (orchestration + simulated agents): ~22k (Wave 0 parse + Wave 1 hypothesis + Wave 1 calibration + 3 x Tier 2 hypothesis + 3 x Tier 2 calibration + candidate-fixes + evidence-validation + REPORT)
- Wall clock (simulated): ~8 minutes for Tier 2 without adversarial. Real-world would land at the 4-7 min "Tier 2 no adversarial" target in SKILL.md's cost profile.
