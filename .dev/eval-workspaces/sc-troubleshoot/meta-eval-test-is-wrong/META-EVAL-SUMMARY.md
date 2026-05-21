# Meta-Eval Summary: Should v2 incorporate the `test_is_wrong` flag?

**Date**: 2026-05-21
**Method**: Inject synthetic "test is wrong" symptoms into eval-2 (flaky test) and eval-5 (scratch-root policy) variants; re-run the v2 protocol end-to-end on each; observe whether v2 correctly identifies the test (not the code) as the bug, and whether a structured `test_is_wrong: true` flag would change anything.

## Both variants: identical verdict

| Variant | Tier reached | Confidence | Identified test as bug? | Verdict |
|---------|--------------|------------|-------------------------|---------|
| eval-2-test-wrong (stale assertion after per-device feature) | Tier 2 (intermittent rule) | 0.90 (all 3 agents) | **Yes — unambiguously**. Report opens with "The TEST is the bug, not the code" | **USEFUL (b)** — not essential |
| eval-5-test-wrong (inverted policy claim) | Tier 2 (multi_domain) | 0.94 | **Yes — decisively**. "Files that MUST NOT change" sentinel + anti-fixes catalog | **USEFUL (b)** — not essential |

## Why the verdict is USEFUL, not ESSENTIAL

**v2's prose diagnosis already names the test as the bug with high confidence in both variants.** A human reader cannot miss the conclusion:

- Variant A: "The TEST is the bug, not the code" appears 10+ times across REPORT.md + hypothesis cards + Alternative Fixes section ("the DANGEROUS wrong answer")
- Variant B: REPORT.md Summary opens with "The test is the bug, not the code"; candidate-fixes.md catalogs 4 anti-fixes (A1-A4) that downstream remediation must not resurrect

The flag is **load-bearing only for automation chains** that gate on the output contract rather than parsing REPORT.md prose:

- Tier 3 `task-builder` chain
- Auto-apply / fleet remediation wrappers (none currently exist)
- Telemetry / fleet-level audit ("what fraction of /sc:troubleshoot runs identify a test, not code, as the bug?")

## What actually does the load-bearing work in v2

Both variants confirm two existing v2 behaviors carried the diagnosis correctly:

1. **Wave 1 "Ground the symptom in real code"** — variant B's agent Read the OPS-002 policy doc *before* forming a hypothesis, which is what prevented agreeing with the wrong test. This step is in `SKILL.md` Wave 1, step 1.
2. **`confidence-calibrator` independent grounding spot-check** — both variants had calibrators that Read the actual cited code/spec rather than trusting upstream hypothesis cards. This independent verification is what catches inversions like "test claims policy rejects X, but policy actually allows X."

Without these two behaviors, no structured flag would save the diagnosis. With them, the flag is fortification, not foundation.

## Recommendation

**Incorporate as defensive low-cost fortification (~30 min).** Add `test_is_wrong: bool` (and `test_file_path: str | null`) to the output contract at `SKILL.md:37-54`. Update `refs/report-template.md` to set it from the diagnosis. Surface it in the command output.

**Do not pretend the flag is solving the diagnostic problem.** The diagnostic load is carried by Wave 1 grounding and confidence-calibrator spot-check — both already shipped in v2. The flag is automation safety belt-and-braces, valuable only when Tier 3 task-builder is wired to read it (which is a separate follow-up).

**Order of operations**:

1. Add the fields to the output contract (~30 min, additive, near-zero risk)
2. Update `refs/report-template.md` to populate the fields from the diagnosis section
3. Add a single regression eval (a "test is wrong" case) to the iteration-1 eval suite so future skill changes can't silently regress the prose-level detection
4. When Tier 3 task-builder chain ships, have it short-circuit on `test_is_wrong: true` and offer to build a TEST-fix task instead of a CODE-fix task

## Cost / benefit table

| Action | Cost | Benefit | Verdict |
|--------|------|---------|---------|
| Add `test_is_wrong` + `test_file_path` to output contract | 30 min, additive | Automation safety; fleet auditability | **SHIP** |
| Add regression eval ("test is the bug" case) | 1-2 hours | Catches silent regressions in prose-level detection | **SHIP** |
| Wire task-builder to short-circuit on flag | 2-3 hours (part of Tier 3 work) | Closes the "auto-apply fixes the wrong file" loop | **SHIP with Tier 3 follow-up** |
| Rebuild v2 around the flag as a load-bearing primitive | Many hours | Marginal — prose already does the work | **REJECT** |

## Output artifacts

- `.dev/eval-workspaces/sc-troubleshoot/meta-eval-test-is-wrong/eval-2-test-wrong/` (REPORT.md, hypothesis cards, calibration, validation, audit.log, meta-eval-finding.md, timing.json)
- `.dev/eval-workspaces/sc-troubleshoot/meta-eval-test-is-wrong/eval-5-test-wrong/` (same set)
- `.dev/eval-workspaces/sc-troubleshoot/meta-eval-test-is-wrong/META-EVAL-SUMMARY.md` (this file)
