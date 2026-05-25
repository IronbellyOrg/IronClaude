---
proposal_id: 2
persona: pm
model: sonnet
lens: workflow design, throughput metrics, ownership, incentives
---

# Proposal 2 — PM: The Bottleneck Is Review Latency, Not Documentation

## Position

The scribe is solving the second-biggest problem. Look at the numbers: median time-to-first-merged-PR is **21 days**. A contributor who pushes a PR on day 0 and gets first review on day 14 has already disengaged emotionally. Even a perfect onboarding doc doesn't fix a 2-week review wait. Fix the **review-throughput bottleneck** first — every other improvement compounds with it; without it, every other improvement underperforms.

## The intervention: First-PR Shepherd rotation

A named role, weekly rotation among the 4 maintainers. The shepherd's only commitment for that week:

1. **Triage every new first-PR within 24 hours** — leave one of three responses: (a) "I'll review this within 3 days, hold tight", (b) "this needs X before review, here's what to do", (c) "this isn't in scope for the project, here's why and a kind redirect."
2. **Drive each first-PR to a decision (merge / changes-requested / decline) within 7 days.** Hand off to another reviewer if they themselves are blocked.
3. **Apply the review rubric** (subordinate proposal — borrow from scribe's spec).

That's it. The shepherd does NOT have to be the *only* reviewer — they're the *accountable* reviewer. Other maintainers can chime in. If the shepherd is on vacation, the prior week's shepherd covers.

## Why this works

**Latency is the conversion-killer.** Open-source product analytics across multiple studies (CHAOSS, Linux Foundation OSS reports) show first-PR-to-second-PR conversion drops off a cliff past 7 days of review wait. The 25%-to-40% second-PR target is *primarily* a latency problem, not a documentation problem.

**Ownership beats process.** Right now, the failure mode is "everyone assumes someone else will get to it." Naming a person for a week breaks that. The week-long rotation is short enough that no maintainer feels permanently on the hook.

**It scales with the team you have.** 4 maintainers × ~5 hours/week shepherd-time = 5 hours/week sustained, dropping into one maintainer's slot. That's inside the 1-maintainer-day/week budget. The other 3 maintainers' weeks are unburdened.

## Metrics & enforcement

- **Shepherd-week scorecard** (visible to all 4 maintainers): how many first-PRs landed in their week, median time-to-first-response, median time-to-decision. *Not* a performance metric — a visibility instrument. Conversations about it happen in the maintainer retro.
- **Public expectation in `CONTRIBUTING.md`**: "your first PR will get a response within 24 hours and a decision within 7 days." This makes the SLA externally visible and creates the right pressure.
- **Quarterly review**: are we hitting the median? If not, increase shepherd-week scope (e.g., 2 maintainers/week) before adding new tooling.

## Where I diverge from scribe

The scribe's three-tier spine is **good work**, but it's a Q2 project, not the Q1 lever. Sequence:

- **Weeks 1-2**: Stand up the shepherd rotation. Write a 1-page `SHEPHERD_RUNBOOK.md`. Update `CONTRIBUTING.md` with the SLA.
- **Weeks 3-8**: While the shepherd rotation is producing signal, the scribe's spine rewrite happens in parallel.
- **Weeks 9-10**: Measure both interventions' effects. By KubeCon, we have data on the shepherd rotation (~6 weeks of signal) *and* a new docs spine.

This way the conference talk has *two* improvements to point to, and the first one (shepherd) is already producing measurable results when the talk happens.

## What I'd push back on

The scribe's claim that "every other intervention is downstream of documentation." False — review latency is upstream of documentation engagement. A contributor who never gets a response on PR #1 doesn't read the docs for PR #2; they leave. Fix latency first, *then* docs compound.

## Cost

- Week 1: ~3 hours to write `SHEPHERD_RUNBOOK.md` and update `CONTRIBUTING.md`.
- Weekly ongoing: ~5 hours of shepherd time per maintainer, rotating.
- Quarterly: ~2 hours retro.
- Total over 10 weeks: ~50 maintainer-hours (well inside budget).
