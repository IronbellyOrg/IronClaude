# Calibration Report (reviewer 2 card)

(Returned by the confidence-calibrator agent, sonnet class; persisted by the parent on receipt at 2026-11-08T02:08Z.)

**Card**: reviewer-cards/reviewer-2-card.md   **Rubric**: reflection-rubric.md (5 dimensions, C = arithmetic mean)   **Tier**: 2   **Mode**: pre   **Timestamp**: 2026-11-08T02:06:28Z

## Per-dimension scores

| Dimension | Score | Justification |
|---|---|---|
| Citation grounding | 0.90 | 16 citations checked, all matched. Unverified: claude --help not read and the done and blocked packages not read (the card flags both itself as [INFERRED] or ungrounded); Q-4's claim about F2.4 in review-2.md not read |
| Coverage completeness | 0.90 | INF 10 of 10; the INF-006 refutation of the lexical miss confirmed (plan:29 "exit-status ledger", plan:31 "exit code or signal"); run-budget arithmetic checked against plan:22; findings cluster on Tasks 1, 3, 5, 8; Task 7 gets only N-10 and Task 2 only Q-8 and N-9 |
| Deviation-classification clarity | 0.65 | no {Aligned, Refinement, Drift, Regression} labels in pre mode; severity and confirm/refute labels scored instead; hedged severities in 5 of 22 rows (Q-5 "Low-Medium", Q-6 "Low-Medium", N-2 "Medium-Low", N-9 "Low-Medium", N-13 "Info/Low"); N-8 ("partly refute then extend") and N-14 ("confirm and strengthen") carry no severity; no Q row has a severity rationale; several confirmed Lows (N-5, N-11) have no stated reason; strengths: Medium calls on N-1, N-3, N-12, Q-1..Q-4 have stated consequences |
| Risk surface coverage | 0.88 | blast radius: cleanup killing the old child (N-3), setsid supervisor (N-7), a daemon escaping the cwd sweep (Q-6), a budget cap that does not bound the pty run (N-4); untested invariants Q-4, Q-5, Q-3, PASS unreachable (N-14); does not explain why the unobserved pty /clear identity matters beyond Q-1 |
| Recommendation actionability | 0.85 | Q rows name a plan line and a concrete edit (Q-1 ordering, Q-8 pid file with a cap); Q-2 and Q-3 offer alternatives joined by "or"; N judgements mostly "confirm" with no action; Q-5 gives only "for example" |

## Confidence

Self-reported 0.80; **calibrated 0.84** (mean 0.836 rounded). Delta +0.04. Sensitivity: dimension 3 is the only dimension below 0.85; at 0.70 the mean would be 0.846, on the threshold.

## Escalation recommendation

ESCALATE, reason low_confidence (C = 0.84 < 0.85; rubric rule: C < 0.85 is an automatic ESCALATE). The gap is 0.01 and comes from label hedging, not weak evidence; removing the hedged and missing severities would lift C to about 0.88. No structural signals supplied. This is a Tier 2 card, so the verdict means "tidy the severity labels", not "the card is wrong".

## Notes

Spot-check (all verified against the worktree): Q-4 (helper:238-241 `governed(root, value['session_id'])` raising FileNotFoundError returns `{'status': 'ordinary', 'reason': 'released'}`; design:526; design:557; plan:79 and :120 show Task 5 is the only release task and is controlled; caveat: the proposed real release observation works only if Task 3's child survives the kill, which plan:55 treats as unproven; the "closes part of F2.4" claim depends on review-2.md, unread); Q-7 (helper:435-437 `if not os.path.lexists(path): return 0`, so a new session id with no record is ordinary; that a fork or /clear gets a new session id is [INFERRED], as the card says); helper :219-223, :234, :253, :292, :428; live_probe.py :129, :237-240, :252-253, :280; design:504; plan :22, :29, :31, :44, :55, :66, :71, :79, :90, :114, :117, :120.
Not checked: actor-context-probe.sh:11, review-2.md, test_launch_job_identity.py:1288-1357, and the Tier 1 card for N-1..N-14 (the N rows were judged from the card's one-line summaries). Rubric has no Runtime-check dimension and no structural assertions (no assertions_path; C1-C8 skipped).
