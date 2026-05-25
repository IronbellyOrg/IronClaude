---
debate_round: 1
proposals: [proposal-1-scribe, proposal-2-pm, proposal-3-mentor]
convergence_score: 0.86
---

# Adversarial Debate Transcript

Three proposals against `seed-brief.md` (STANDARD / AGILE tier, 3 proposals as configured). Convergence is **high (0.86)** because the proposals turn out to be **layered, not competing** — each addresses a distinct phase of the contributor journey (first 30 minutes / first 7 days / first 60 days). The debate clarified ordering and budget allocation, not direction.

## Tension 1 — Which lever is primary? (Scribe vs PM)

**Scribe**: documentation is the primary lever; every other intervention is downstream.

**PM**: review latency is the primary lever; even perfect docs don't convert past a 14-day review wait.

**Resolution**: **PM's framing is more defensible on the conversion-rate goal (25% → 40% second-PR)**, but scribe's work doesn't have to be deferred — the two streams run in parallel. Merged sequencing:

- **Weeks 1-2**: Shepherd rotation stands up (PM). `SHEPHERD_RUNBOOK.md` written. `CONTRIBUTING.md` updated with the 24h/7d SLA.
- **Weeks 3-8**: Documentation spine rewrite in parallel (scribe). Shepherd rotation produces ~6 weeks of signal.
- **Weeks 9-10**: Measure both before the conference talk.

This way both proposals' interventions are live by the deadline, but the higher-leverage one (latency) starts producing signal first.

## Tension 2 — Is the rubric a scribe-deliverable or a PM-deliverable?

Both proposals mention the review rubric. Scribe owns the *content* (tone examples, must-fix vs should-fix, two-comment rule); PM owns the *enforcement* (shepherd links to rubric in first review comment).

**Resolution**: No tension — scribe writes the rubric document, PM's shepherd integrates it into the workflow, mentor adds the tone-calibration examples. Single artifact, three contributors, clear handoff.

## Tension 3 — One-time audit vs continuous triage on "good first issue" (carries seed Q5)

Scribe: one-time audit + written definition for ongoing discipline. Mentor: didn't address. PM: didn't address.

**Resolution**: **Scribe's position adopted unchallenged.** One-time audit, then the written definition in `CONTRIBUTING.md` governs ongoing triage. Mislabel rate ≤10% measured by sampling.

## Tension 4 — Second-PR motion (Mentor vs Scribe + PM)

Mentor adds the "second-issue handoff" template. Neither scribe nor PM addressed sustained engagement past PR #1.

**Resolution**: **Mentor's proposal is adopted as an additive layer.** Scribe + PM accept that their work optimizes the *first* PR; mentor's template moves the dial on the *second*. The handoff template lives in the shepherd's runbook (PM's deliverable) and references the recurated `good first issue` set (scribe's deliverable). All three proposals compose cleanly.

## Tension 5 — Discord vs GitHub Discussions for Q&A

Mentor proposes shifting the primary Q&A pointer from Discord to GitHub Discussions (honoring the seed brief's "GitHub-only path" constraint and producing searchable Q&A). Scribe didn't address; PM didn't address.

**Resolution**: **Adopted.** Update `START_HERE.md` and `CONTRIBUTING.md` pointers. Discord stays for chat; technical questions land in Discussions. Cost is trivial.

## Tension 6 — Measurement vs metric-gaming

PM's shepherd-week scorecard is described as "a visibility instrument, not a performance metric." Mentor pushes back: a shepherd optimized for *time-to-decision* without *second-PR-rate* in the same view will ship fast and not cultivate.

**Resolution**: **Add second-PR-rate (60-day lookback) to the scorecard.** Two metrics, not one. Quarterly retro discusses both. Both proposals agree.

## Convergence rationale

Three proposals, six tensions, all resolved with explicit positions. No proposal was rejected; all three are layered into the final spec. Convergence **0.86** — high; the proposals were genuinely complementary, and the debate's job was sequencing and integration rather than choosing winners. The shared model: scribe = first 30 min, PM = first 7 days, mentor = first 60 days.
