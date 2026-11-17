review: 2 of 3 must be the first line of your report.

You are the re-reviewer of a /sc:spec-panel critique-mode review loop. Read-only: do not edit, write or create any file and do not start another review. Return your whole report as your final message.

Roles are fixed:
| ROLE | FILE | MEANING |
|---|---|---|
| CANDIDATE | docs/designs/surgical-remediation.md | the revised text under review |
| BASELINE | .dev/spec-panel/surgical-remediation/baseline-r1.md | the text as it was before the revision |
| PRIOR | .dev/spec-panel/surgical-remediation/round-2/prior.md | the previous review report (review 1 of 3) |

Review the revised candidate docs/designs/surgical-remediation.md (sha256 1333d41ed0abcd621d1c1e1ccca93b086327b475c48342c961ba89171e2ddb76) against .dev/spec-panel/surgical-remediation/baseline-r1.md, the spec as it was before the revision (sha256 fb26244a2f37a20f9d179383ebb0dc27b54ebe66b641e6acfff0043adc084a64), using prior report .dev/spec-panel/surgical-remediation/round-2/prior.md (sha256 cab342ea1bfc22b75ab20edc06996b3fbceead5362e44dddd24d12cb196ba8a4), review 2 of 3, where N is the prior report's review number plus 1. Do Step 1, the evidence block, before any finding: the changed lines are in /tmp/sr-rev1/diff-r1.txt (diff -w BASELINE CANDIDATE); copy them verbatim under BEFORE (baseline) (lines starting <) and AFTER (candidate) (lines starting >). Re-check each prior blocking finding (only L4 was blocking) as resolved, open or regressed against the revised candidate, comparing its defect with the AFTER text only. Inspect changed behavior and the dependencies it touches; for inherited text, cite the changed line it depends on. Report concrete wrong outcomes, not a minimum number of findings. Minor findings are notes and never fail the review; list Medium and minor findings under follow-up candidates. Record a severe defect you newly discover even if it is older, and say where it came from. If an input is missing or unreadable, return incomplete. Self-check before the verdict: use Grep to confirm each quoted AFTER line is in CANDIDATE and each quoted BEFORE line is in BASELINE; if not, you swapped roles, redo Step 1. Do not edit the candidate and do not start another review. State what you covered.

Context: besides the fix for L4, the revision applies four owner decisions of 2026-11-17 (D1 all three counts under their limits; D2 archive the original before the re-review, fix cycles repeat the five steps on the placed package, a failed repair keeps review_verdict FAIL and /sc:implement refuses it; D3 H counts the label HIGH and M the grade Medium; D4 default on). These are owner orders, not findings: check that the text implements them consistently, do not argue them.

Grading check, for each finding before you mark it blocking: write the sentence "An implementer who follows the stated text as written builds X, and X is wrong because Y." Blocking needs a sentence that holds with no further assumption: two stated texts that contradict each other, a stated text that causes data loss or breaks a security or safety boundary, or a stated text that an acceptance criterion cannot pass. Grade it Medium when the sentence needs a guess that the implementer picks the worse of two readings the text allows, or when the finding is a requirement the document never states. A finding on unchanged text is a minor note unless it quotes the changed line it depends on.

End the report with:
1. "## Findings block": one fenced code block with info string findings-v1, one JSON object per line: one line per finding you report ({"id": "F1", "severity": "CRITICAL|MAJOR|MINOR", "blocking": true|false, "category": "contradiction|unpassable-check|data-loss|safety|missing-requirement|other", "anchor": "<12 to 200 characters copied exactly from the candidate>", "anchor2": "<optional>", "refs": ["<sections>"], "claim": "<one sentence, at most 300 characters>"}) and one prior line per prior blocking finding: {"prior": "L4", "status": "resolved|open|regressed"}.
2. If no blocking finding is open, the line: scoped PASS: changed lines + prior blockers
3. The last line: verdict: PASS or verdict: FAIL.
