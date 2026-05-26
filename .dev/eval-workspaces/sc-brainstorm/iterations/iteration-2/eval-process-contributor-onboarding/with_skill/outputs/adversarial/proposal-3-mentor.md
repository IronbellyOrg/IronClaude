---
proposal_id: 3
persona: mentor
model: haiku
lens: contributor experience, learning curves, sustained engagement, community health
---

# Proposal 3 — Mentor: Sustained Engagement Needs a Path Past PR #1

## Position

Both prior proposals improve the *first PR* experience — scribe via clearer docs, PM via faster review. Both are necessary. But the goal isn't first PRs; it's **second PRs**. Hitting 40%-second-PR-rate from 25% requires something neither prior proposal addresses: **a deliberate path from PR #1 to PR #2**, and a way for the contributor to feel they're becoming part of something rather than transacting a one-off.

## The intervention: the "second issue" handoff

When a first PR merges, the shepherd-of-the-week (borrowing PM's rotation) leaves a templated comment:

> "Thanks for landing this! If you'd like to keep contributing, here are two issues that build on what you just learned: [link 1] and [link 2]. Or, you've now seen the X subsystem — issues tagged `area:X` are good candidates. Either way, ping `@maintainer-on-call` and we'll help you get started."

That's it. Three lines. The cost is ~2 minutes per merged first PR for the shepherd. The behavioral mechanism is:

1. **Reduces "what next?" friction.** The biggest drop-off cause after PR #1 isn't dissatisfaction — it's a returning contributor opening the issue tracker, seeing 400 issues, and not knowing which to take. Two curated suggestions cut that cliff.
2. **Creates a "you belong here" signal.** The hand-off comment treats the contributor as continuing, not departing. Small social cue, large effect.
3. **Builds maintainer-contributor familiarity.** By PR #3, the shepherd remembers the contributor. By PR #5, the contributor knows which maintainer to ping. This is the soil aspiring maintainers grow in.

## Why this complements (doesn't compete with) the others

- **Without the scribe's spine**: the "two issues that build on what you just learned" links land in a 2,400-line README contributor and get lost.
- **Without the PM's shepherd**: there's no consistent person to write the handoff comment; it becomes "someone might do it sometimes."
- **Without this proposal**: the spine + shepherd make first PRs faster and cleaner, but second-PR-rate improves modestly because the existing 400-issue cliff hasn't moved.

The three proposals are **layered**, not competing. Scribe = clarity for the first 30 minutes. PM = speed through the first 7 days. Mentor = path through the first 60 days.

## Tone calibration (subordinate but important)

The PM proposal's "review rubric" matters, but rubrics calibrate the *what*; tone calibration handles the *how*. Add to the rubric:

- **The "first PR" review opens with appreciation, ends with next-action.** Not a template, a habit. "Thanks for picking this up — one small thing on line 23 and we're good to merge."
- **Avoid the "harsh accidental" patterns**: "this is wrong" → "I'd suggest"; "you didn't" → "we usually"; one-word "nit" comments → either drop the nit or explain it in a sentence.
- **In-line examples in the rubric**: 3 before/after examples of comments. Reviewers read it once, internalize, move on.

## Discord question recurrence (open Q5 partial answer)

The seed brief flags recurring Discord questions. Two-track:

1. **Self-serve the questions that repeat 3+ times/quarter**: those go into `START_HERE.md` or `CONTRIBUTING.md`'s FAQ — sole owner is the next shepherd-of-the-week who noticed them.
2. **GitHub Discussions as the primary Q&A surface**: shift the "where to ask" pointer in the docs from "Discord" to "GitHub Discussions for technical questions, Discord for chat." Discussions are searchable, indexed, and don't require a third-party account. Honors the seed brief's "GitHub-only path" constraint.

## Aspiring-maintainer pipeline

Out of scope per seed brief Q7, but a downstream consequence of this proposal: contributors who hit PR #3-5 with the same shepherd are exactly the pipeline. No additional intervention needed; the soil grows them.

## Where I diverge

- **From scribe**: the spine is good but it ends at "filed the PR." Sustained engagement is a 60-day arc; documentation alone doesn't carry it.
- **From PM**: the shepherd rotation is the right *mechanism*, but its *measure* must include second-PR-rate, not just time-to-decision. Otherwise the shepherd is incentivized to ship fast and not to cultivate.

## Cost

- ~30 minutes to draft the "second issue" handoff template (one shepherd, one time).
- ~2 minutes per merged first PR for the shepherd to personalize and post (~20-30 first PRs/month × 2 min = ~1 hour/month).
- Tone calibration additions to the rubric: subsumed in the rubric work (scribe + PM cost).
- Shift docs pointer from Discord to Discussions: ~15 minutes.

Total marginal cost: trivial. The leverage is all in the design, not the labor.
