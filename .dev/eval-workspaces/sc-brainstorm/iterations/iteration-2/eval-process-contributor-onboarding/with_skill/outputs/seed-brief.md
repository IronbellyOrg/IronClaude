---
topic: "improve onboarding workflow for new contributors"
domain: process
strategy: agile
depth: standard
proposal_count: 3
handoff_target: none
created: 2026-05-25T00:00:00Z
---

# Seed Brief: improve-contributor-onboarding

## Socratic Dialogue Record

STANDARD tier triggers Clarify + Validate batches — 10 questions targeted at scoping the change and surfacing real blockers.

### Clarify batch

**Q1. Who is "a new contributor" — first-time OSS contributor, returning contributor after a break, or a new hire / new employee on the project?**
A: Mostly external first-time OSS contributors. We get ~20-30/month who file a first PR or issue. Of those, maybe 6-8 stick around past the first PR. Internal new-hires have a separate (better-resourced) onboarding; not in scope here. Returning-after-break contributors are a tiny segment we can ignore.

**Q2. What's the current onboarding path?**
A: README → CONTRIBUTING.md → look at "good first issue" label → file PR. The README has been incrementally rewritten 4 times in 2 years and is now ~2,400 lines. CONTRIBUTING.md exists but hasn't been touched in 14 months. "good first issue" label is stale — half the issues with it are actually intermediate-difficulty.

**Q3. What failure modes do you see?**
A: (a) Drop-off after first read — people clone, look at the README, and never PR. (b) First PR sits in review limbo for >2 weeks because reviewer assignment is ad-hoc. (c) "good first issue" mismatches difficulty, so first-time contributors hit a wall and quit. (d) Recurring questions in Discord that the docs *do* answer but the contributor couldn't find. (e) Tone in code review is sometimes harsh enough that the contributor doesn't return.

**Q4. What does "done" look like?**
A: (i) Time-to-first-merged-PR median ≤7 days (currently ~21 days). (ii) ≥40% of first-PR contributors file a second PR within 60 days (currently ~25%). (iii) "good first issue" label is curated, not free-for-all. (iv) Onboarding docs measurably reduce the top-5 Discord questions. (v) A documented "first review" code-review rubric so reviewers calibrate.

**Q5. Non-negotiable constraints?**
A: (a) No new tooling that we have to maintain (we're 4 maintainers, already stretched). (b) Cannot require contributors to sign a CLA we don't have today (a politics fight we're not taking on). (c) Must not require a Discord account to contribute — GitHub-only path must exist.

### Validate batch

**Q6. Who owns this workflow today?**
A: Distributed and ambiguous. The README is touched by whoever's reviewing PRs that week. CONTRIBUTING.md is "owned" by the project lead but they're the bottleneck. "good first issue" labels are applied by whoever triages. No single throat-to-choke for the onboarding experience.

**Q7. Who's the target audience for the new workflow — first-PR-then-leave contributors, repeat contributors, or aspiring maintainers?**
A: All three but the leverage is in first-PR-then-leave → repeat. If we convert that ~25% → ~40%, the maintainer pool *and* the contributor health both improve. Aspiring-maintainer pipeline is great-to-have but second priority.

**Q8. What's already been tried?**
A: Two relevant things: (i) a hackathon-style "good first issue day" 9 months ago — modest spike, no sustained lift. (ii) a Notion page with "how to set up dev env" written 6 months ago — has 8 page views total, broken. Neither was promoted nor maintained.

**Q9. Forcing function / deadline?**
A: KubeCon-style upstream conference next quarter — project lead is presenting and wants to be able to say "we improved this." Soft deadline ~10 weeks. Not a hard wall, but a real signal.

**Q10. Rollback if a change misbehaves?**
A: Mostly N/A — docs and process don't "roll back" the way code does. But if a labeling-rule change causes a flood of complaints, we revert the label rule and move on. The risk shape is "doesn't help" more than "actively breaks."

## Problem Statement

External OSS contributors to the project (~20-30 first-PRs/month) drop off at a high rate — only ~25% file a second PR within 60 days, and the median time-to-first-merged-PR is ~21 days. Root causes are diffuse: a 2,400-line README that's grown by accretion, a 14-month-stale CONTRIBUTING.md, mislabeled "good first issue" tickets, ad-hoc reviewer assignment that creates 2-week review limbos, recurring-question rediscovery in Discord, and uncalibrated review tone. A 4-maintainer team needs to land improvements that reduce time-to-merge, lift the second-PR rate, and don't introduce new tooling burden — with a soft conference-deadline at ~10 weeks.

## Known Context

- ~20-30 first-PR contributors/month, ~25% file a second PR within 60 days, median time-to-first-merged-PR ~21 days.
- 4 maintainers, already stretched.
- README: 2,400 lines, accretion-grown over 2 years.
- CONTRIBUTING.md: 14 months stale.
- "good first issue" label: ~50% mislabeled (intermediate-difficulty issues tagged).
- Reviewer assignment: ad-hoc (slowest path of all the failure modes).
- Prior attempts: (1) hackathon day 9 months ago — modest spike, no lift; (2) Notion dev-env page — broken, 8 views.
- Soft deadline: ~10 weeks (conference talk).
- Constraints: no new tooling to maintain, no new CLA, GitHub-only path required.

## Constraints

- No new tooling the maintainers have to operate.
- No CLA requirement added.
- GitHub-only contribution path must exist (Discord optional).
- Maintainer effort budget: ~1 maintainer-day/week sustained for the improvements, NOT including ongoing PR review.
- Soft deadline: 10 weeks.

## Success Criteria

- Time-to-first-merged-PR median ≤ 7 days (from ~21).
- Second-PR-within-60-days rate ≥ 40% (from ~25%).
- "good first issue" label has a curated definition + an audit cadence; mislabel rate ≤ 10%.
- A documented "first review" code-review rubric exists and is referenced in ≥80% of first-PR reviews.
- Top-5 recurring Discord questions either answered prominently in updated docs or routed to a self-serve flow.
- All changes implementable inside the constraints (no new tooling, no CLA, GitHub-only path).

## Open Questions

- Should we appoint an explicit "first-PR shepherd" rotation among the 4 maintainers, or distribute via auto-assignment?
- Do we restructure the README (split into smaller docs) or freeze it and add a new "Start here" top doc?
- Is a written code-review rubric enough, or do we need lightweight reviewer training (15-min video / live session)?
- How do we measure "review tone improved" — survey? PR sentiment audit? Or just track second-PR rate as a proxy?
- Should the "good first issue" recuration be a one-time audit, or a continuous part of issue triage?

## Enrichment Context

No enrichment artifacts were generated. This topic is process/people-focused — the codebase and external research are not load-bearing for the proposals. The Socratic dialogue captures all the context the proposals need. Confidence on this skip-decision: high.
