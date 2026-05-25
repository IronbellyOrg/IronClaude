---
proposal_id: 1
persona: scribe
model: sonnet
lens: documentation clarity, information architecture, learning path design
---

# Proposal 1 — Scribe: A Three-Tier "Start Here" Spine That Replaces the 2,400-line README

## Position

The 2,400-line README is the load-bearing failure. Every other intervention (label curation, reviewer rubric, shepherd rotation) is downstream of "the contributor couldn't find what they needed in the first 60 seconds." Replace the README's role as a Swiss-army-knife with a **three-tier documentation spine** that maps to the three contributor moments: 60 seconds (am I in the right place?), 5 minutes (can I make a first change?), 30 minutes (do I understand enough to file a PR?).

## The three-tier spine

- **Tier 1 — `README.md`, ≤200 lines.** Project pitch (3 lines), "is this for you?" decision tree (5 lines), install/quickstart (10 lines), three links: `START_HERE.md`, `CONTRIBUTING.md`, `docs/`. Nothing else.
- **Tier 2 — `START_HERE.md`, ≤400 lines.** New file. The "5-minute" doc. Project mental model in one diagram, "your first 5 minutes" walkthrough (clone → run → observe), one curated "good first issue" link, where to ask questions (GitHub Discussions, then Discord). Written for someone who's never seen the repo.
- **Tier 3 — `CONTRIBUTING.md`, ≤600 lines.** Rewritten. The "30-minute" doc. Dev-env setup, how to file a PR, what reviewers will look for (links to the review rubric — see scribe-proposal §rubric below), how to get reviewers' attention, the project's code style summary (full style lives in `docs/style/`).

The current 2,400-line README's *content* doesn't get deleted — it gets relocated into `docs/` as topical pages (architecture, configuration reference, troubleshooting, FAQ) and discoverable via the README's "links to deeper docs" footer. Existing content survives; the spine becomes navigable.

## The reviewer rubric (subordinate to the spine)

A 1-page `docs/reviews/first-pr-rubric.md` covering:

- **Tone**: "what to assume" (the contributor is doing this on their lunch break, hasn't read the architecture doc, may not know the conventions yet). Three "instead of saying X, say Y" examples.
- **What to require vs suggest**: must-fix (correctness, security, public-API breakage), should-fix (style, test coverage), nice-to-have (naming, doc tightening). First-PR reviewers default to *suggesting* anything below must-fix.
- **The two-comment rule**: a first PR shouldn't get more than two rounds of review feedback before either landing or being explicitly closed with a kind explanation.

Reviewers link to this rubric in the first review comment on every first PR. The link becomes the calibration mechanism.

## "Good first issue" recuration (subordinate to the spine)

One-shot audit (~4 hours of one maintainer) against an explicit definition: ≤30 LOC change, no architecture knowledge required, has a clear "expected behavior" description, has an acceptance criterion stated. Issues failing this definition get re-labeled `help-wanted` or have the label stripped. Then: add the definition to `CONTRIBUTING.md` so future triagers apply it consistently. The continuous-vs-one-time question (open Q5) resolves to **one-time audit, then triage discipline via the written definition**.

## Cost

~2 maintainer-weeks total over 8 calendar weeks:
- ~3 days writing `START_HERE.md` (the hardest doc — needs the project's mental model in one diagram).
- ~2 days rewriting `CONTRIBUTING.md`.
- ~1 day shortening the README and relocating content.
- ~0.5 day writing the reviewer rubric.
- ~0.5 day auditing "good first issue" labels.
- ~3 days of buffer for review cycles among the 4 maintainers.

Inside the 1-maintainer-day/week budget; well inside the 10-week deadline.

## Why this shape

**The README is broken because it's trying to be 3 documents at once.** It's the project pitch, the install guide, the contributor guide, and a partial architecture reference. Split the *audience moments*; let each document serve one. Industry prior art: every well-onboarded OSS project (Kubernetes, React, Rust) has a tier-1 README that hands off to specialized docs.

**The reviewer rubric and label recuration are subordinate, not primary.** They matter — but a great rubric on a project whose README confuses people produces fast harsh reviews of code that never should have been written. The spine must come first.

## What I'd push back on

Anyone who proposes "more documentation" without subtracting from the existing 2,400-line README is making the problem worse. The README is *too much*, not too little. Adding pages without restructuring leaves contributors with more places to get lost.
