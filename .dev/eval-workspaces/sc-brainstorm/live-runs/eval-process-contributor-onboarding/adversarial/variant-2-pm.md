---
variant: 2
agent: sonnet:pm
focus: sprint-shippable process changes
created: 2026-05-27T00:00:00Z
---

# Variant 2 — Process / Sprint-Cadence Onboarding (PM / Sonnet)

## Premise

Documentation alone doesn't move retention — process does. New contributors need a visible "queue" of work, a feedback channel that fits async-first, and tight sprint cycles so they can see their work land quickly. Apply lean agile rituals to the contributor pipeline itself.

## Proposed Improvements

### 1. Curated `good-first-issue` queue with rotating maintainer-of-the-week

- Maintain a backlog of 10-15 issues labeled `good-first-issue`, each with:
  - Estimated effort (S/M/L, capped at S for first-timers)
  - Pointer to relevant docs section
  - Named "shepherd" maintainer who commits to <48h first response
- Maintainer-of-the-week rotation (volunteer signup in `MAINTAINERS.md`) ensures coverage without burning out any single person.

### 2. Two-week "onboarding cohort" sprint cadence

- Every two weeks, open a "cohort" GitHub Discussion thread: introductions, pick-an-issue, share-a-question.
- Async-friendly: no calendar invites, no synchronous calls. Thread is the unit of cohort interaction.
- At end of sprint: post a public "cohort summary" with PRs merged, contributors highlighted.

### 3. PR template with "first PR" checkbox

- If contributor checks "this is my first PR to this project":
  - Auto-comment from a GitHub Action with the 3-doc reading list + shepherd ping.
  - Maintainer SLA: first review within 72h.
  - Gentler review tone — explanatory, not just blocking.

### 4. Confidence-check lite for newcomer PRs

- Lightweight checklist in PR template: "Did you (a) `make dev`, (b) `uv run pytest`, (c) `make verify-sync`?"
- Not enforced by CI (avoid the gate), but visible. Helps maintainer triage and teaches the rhythm.

### 5. Sprint retro on contributor experience

- Every 4 weeks, maintainers post a brief retro: where did newcomers get stuck, what 1-2 fixes shipped, what's queued next sprint.
- Closes the feedback loop without requiring a heavyweight survey.

## Success Metrics

- Median time-to-first-response on newcomer PRs drops below 48h.
- Contributor return rate (second PR within 90 days of first) increases by 25%.
- `good-first-issue` queue depth stays in 8-15 range (not depleted, not stale).
- Each 2-week cohort produces ≥2 merged newcomer PRs.

## Sprint Plan (one 2-week sprint)

- Week 1: curate `good-first-issue` backlog, draft MAINTAINERS.md rotation, write PR template auto-comment Action.
- Week 2: open first cohort thread, run a retro at sprint end, iterate based on signal.

## Risks

- Maintainer burnout if rotation lacks enough volunteers. Mitigation: minimum 4 volunteers before launching; clear opt-out path.
- Cohort threads can feel performative if traffic is low. Mitigation: don't force them — only open a thread if there's an active newcomer that fortnight.
- Auto-comment can feel spammy. Mitigation: keep it short (3 lines, 3 links), only on flagged first-PRs.

## Out-of-Scope Acknowledged

- No paid programs, no scheduled office hours, no in-depth mentorship pairing. Purely lightweight process scaffolding.
