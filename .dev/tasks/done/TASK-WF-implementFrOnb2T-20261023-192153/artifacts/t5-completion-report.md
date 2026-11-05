# Part B completion report (Task 5)

## Status of the deck

**Not publishable under this plan.** The plan allows three independent accuracy reviews (Task 5); all three returned FAIL:

| Report | Verdict | Findings | Status in the deck |
|---|---|---|---|
| /home/coder/workspaces/IronClaude/.dev/releases/backlog/ironclaude-onboarding-deck/qa/accuracy-review.md | FAIL | 10 (F1-F10) | all fixed (confirmed by rounds 2 and 3; F2 completed after round 3 as R2) |
| /home/coder/workspaces/IronClaude/.dev/releases/backlog/ironclaude-onboarding-deck/qa/accuracy-review-2.md | FAIL | 8 (N1-N8) | all fixed (confirmed by round 3) |
| /home/coder/workspaces/IronClaude/.dev/releases/backlog/ironclaude-onboarding-deck/qa/accuracy-review-3.md | FAIL | 5 (R1-R5), all minor wording; none changes a command or flag | all fixed after the report; not yet re-reviewed |

Spec FR-ONB.5 allows publishing only after a PASS. The deck therefore needs one more independent review before the artifact is published. That review goes beyond this plan's three-round cap, so it is the user's decision.

## What the final deck passes (evidence in ./artifacts)

- Claim test: `./t5-tests.log` (3 passed).
- Secret and host scan: `./t5-secret-scan.log` (no keys, tokens, credentials, IP addresses, or hosts outside fonts.googleapis.com, fonts.gstatic.com and github.com).
- Render re-run on the final deck (sha256 in `./t5-deck-sha.txt`): `./t5-render/summary.json` and `./t5-render/overflow.json`. Results: 15 slides, 6 diagrams, exact keyboard and button navigation, no console errors, no horizontal scroll at 375 px, lowest contrast 5.39:1 (light) and 5.67:1 (dark), no diagram label overflow, no inline code split, a 15-page PDF in light and dark, and network limited to the page and Google Fonts. The Task 4 evidence (`./t4-*`) predates the accuracy fixes; `./t5-render/` is the current evidence.

## Decisions and additions to report

- **Open Item 3 default** (spec Open Items): slides 5 and 10 state only the guide's rule and do not describe what was said in the meeting.
- **Added line:** slide 1 says "Where anything you hear or read differs from the guide, the guide is the authority."

## Footer and publishing follow-up

The footer reads "Built from HOW-WE-WORK.md at commit 070399eb", with a note that the Part A guide changes are not yet committed. Before or when publishing:

- Commit Part A first (the guide and its copies), then update the footer commit to that commit and remove the "not yet committed" note.
- Re-run `uv run pytest tests/docs/test_onboarding_deck.py`.
- Re-check slides 5, 6 and 10 and the level-ladder and two-planner diagrams against the guide as merged. The slide 15 link to section 3.13 works only after Part A is on master.
- Publish the artifact, and re-publish to the same link whenever the deck changes.
