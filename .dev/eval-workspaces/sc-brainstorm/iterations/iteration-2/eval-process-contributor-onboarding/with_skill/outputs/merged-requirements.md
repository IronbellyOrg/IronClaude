---
spec_type: requirements
domain: process
strategy: agile
adversarial_status: pass
convergence_score: 0.86
proposal_count: 3
source_proposals: [proposal-1-scribe, proposal-2-pm, proposal-3-mentor]
debate_transcript: ./adversarial/debate-transcript.md
source_seed: ./seed-brief.md
agents: "sonnet:scribe:'documentation clarity and information architecture',sonnet:pm:'workflow design, throughput metrics, and ownership',haiku:mentor:'sustained engagement and contributor experience'"
---

# Merged Requirements: Improve Contributor Onboarding Workflow

## Problem Statement

External OSS contributors to the project (~20-30 first-PRs/month) drop off at a high rate — only ~25% file a second PR within 60 days, and the median time-to-first-merged-PR is ~21 days. The failure surface is layered: a 2,400-line accretion-grown README, a 14-month-stale CONTRIBUTING.md, ~50% mislabeled `good first issue` tickets, ad-hoc reviewer assignment that produces 2-week review limbos, recurring-question rediscovery in Discord, and uncalibrated review tone. A 4-maintainer team must deliver improvements that lift second-PR rate, cut time-to-merge, and don't add tooling burden — with a soft conference deadline ~10 weeks out. The merged plan layers three interventions matched to three phases of the contributor journey: documentation spine (first 30 minutes), shepherd rotation (first 7 days), and second-issue handoff (first 60 days).

## Constraints

- **C1** — No new tooling for maintainers to operate. *(seed Q5)*
- **C2** — No new CLA requirement. *(seed Q5)*
- **C3** — GitHub-only contribution path must exist; Discord is optional. *(seed Q5)*
- **C4** — Maintainer effort budget: ~1 maintainer-day/week sustained, NOT including ongoing PR review. *(seed Q4 + Q9)*
- **C5** — Soft deadline: 10 weeks (conference talk forcing function). *(seed Q9)*
- **C6** — Existing README content is preserved (relocated, not deleted). *(scribe §spine; reduces risk of breaking external links)*

## Functional Requirements

- **FR1** — Three-tier documentation spine: `README.md` (≤200 lines, pitch + entry), `START_HERE.md` (new file, ≤400 lines, first-5-minutes walkthrough), `CONTRIBUTING.md` (rewritten, ≤600 lines, includes the new 24h/7d SLA). Existing README content relocated into `docs/` as topical pages, linked from README footer. *(scribe §spine)*
- **FR2** — First-PR Shepherd rotation: weekly rotation among the 4 maintainers, documented in `SHEPHERD_RUNBOOK.md`. Shepherd commitments: (a) first-response on every new first-PR within 24h, (b) decision (merge / changes-requested / decline) within 7 days, (c) hand-off if blocked, (d) post the second-issue template on every merged first-PR. *(PM §intervention + mentor §handoff)*
- **FR3** — Review rubric at `docs/reviews/first-pr-rubric.md`: must-fix vs should-fix vs nice-to-have taxonomy; the "two-comment rule" for first PRs; three before/after tone examples; appreciation-open + next-action-close pattern. Shepherd links to this rubric in the first review comment on every first PR. *(scribe + mentor; rubric is collaborative deliverable)*
- **FR4** — Second-issue handoff template stored in `SHEPHERD_RUNBOOK.md`. The shepherd-of-the-week posts the templated comment (with two curated issue links *or* an `area:X` pointer) on every merged first PR. Estimated ~2 min/PR. *(mentor §intervention)*
- **FR5** — `good first issue` recuration: one-time audit (~4 hours, single maintainer) against an explicit definition (≤30 LOC, no architecture knowledge required, clear expected behavior, stated acceptance criterion). Definition published in `CONTRIBUTING.md` for ongoing triage discipline. *(scribe §recuration)*
- **FR6** — Q&A surface shift: `START_HERE.md` and `CONTRIBUTING.md` point GitHub Discussions as the primary technical Q&A surface; Discord retained for chat. Honors C3. *(mentor §discord-question-recurrence)*
- **FR7** — Externally-visible SLA: `CONTRIBUTING.md` states "first PRs receive a response within 24 hours and a decision within 7 days." Creates expectation pressure consistent with the shepherd rotation's commitments. *(PM §metrics)*

## Non-Functional Requirements

- **NFR1** — Maintainer effort: total weekly cost ≤ 1 maintainer-day/week (shepherd-week ≈ 5 hours/maintainer/week + scribe spine rewrite ~3 days spread over 8 weeks). Inside C4. *(PM cost + scribe cost)*
- **NFR2** — Externally-visible signal: by week 10, the project has data on (a) time-to-first-merged-PR median, (b) second-PR-within-60-days rate, (c) shepherd SLA hit rate, (d) `good first issue` mislabel rate. Conference talk uses these numbers. *(seed Q9; debate Tension 1)*
- **NFR3** — Content preservation: zero broken external links to existing docs. README content relocated to `docs/` with redirects/anchors maintained. *(C6)*

## Acceptance Criteria

- **AC1** — Time-to-first-merged-PR median ≤ 7 days, measured over the 6 weeks ending at the conference deadline (week 10). Baseline ~21 days. *(seed success criteria)*
- **AC2** — Second-PR-within-60-days rate ≥ 35% (stretch: 40%) measured on the cohort of first-PRs from weeks 1-4 (gives ≥60 days to measure). Baseline ~25%. *(seed success criteria; mentor §sustained-engagement)*
- **AC3** — Shepherd SLA: ≥80% of first PRs receive first-response within 24h and a decision within 7 days, measured over weeks 3-10. *(FR2, FR7)*
- **AC4** — Documentation spine shipped: `README.md` ≤200 lines, `START_HERE.md` exists and is referenced from README, `CONTRIBUTING.md` rewritten with SLA. *(FR1)*
- **AC5** — `good first issue` mislabel rate ≤ 10% in a post-audit sample of 20 issues; written definition exists in `CONTRIBUTING.md`. *(FR5)*
- **AC6** — Review rubric exists and is linked in ≥80% of first-PR shepherd comments over weeks 3-10. *(FR3)*
- **AC7** — Top-5 recurring Discord questions either answered prominently in `START_HERE.md` / `CONTRIBUTING.md` FAQ, or routed to GitHub Discussions. Measured by absence-from-Discord over weeks 6-10. *(FR6)*

## Risks

- **R1** (severity: MEDIUM) — **Shepherd rotation burnout.** 5 hours/week × every 4 weeks across 4 maintainers may be more than estimated for a busy week. *Mitigation*: the prior week's shepherd covers vacation; shepherd's scope is *triage and decision-driving*, NOT being-the-only-reviewer; quarterly retro reviews effort. *(PM §cost; seed Q4 budget)*
- **R2** (severity: MEDIUM) — **Metric gaming.** Shepherds optimize time-to-decision by declining first PRs harshly, hurting second-PR rate. *Mitigation*: scorecard includes BOTH metrics; tone is calibrated by the rubric and the "appreciation-open + next-action-close" pattern; mentor's handoff template requires a kind tone by construction. *(debate Tension 6)*
- **R3** (severity: MEDIUM) — **Spine rewrite stalls.** Writing `START_HERE.md` is the hardest doc (project mental-model-in-one-diagram). If it stalls, the scribe stream slips and the conference talk has only the PM-shepherd story. *Mitigation*: `START_HERE.md` is the FIRST scribe deliverable (weeks 3-4); PM stream is the safety net for the conference talk. *(scribe §cost)*
- **R4** (severity: LOW) — **External-link breakage.** Relocating README content into `docs/` breaks links from blog posts, Stack Overflow, etc. *Mitigation*: anchor-preserving relocation with redirects; one-time link audit of external referrers via search. *(NFR3; C6)*
- **R5** (severity: LOW) — **`good first issue` audit creates a complaint flurry.** Re-labeling 10+ stale issues may surface PR-author frustration. *(seed Q10 — risk shape is "doesn't help" not "actively breaks", but worth noting.)* *Mitigation*: re-labeling comments explain the new definition and link the contributor to the recuration definition.

## Open Questions

- **OQ1** — Shepherd-of-the-week metric scope: should the scorecard also include "% of first-PRs where the shepherd hit BOTH 24h response AND 7-day decision" as a third explicit metric, or treat that as derived? *(debate Tension 6 partial)*
- **OQ2** — Reviewer training: is the written rubric enough, or should we add a 15-min onboarding video for new maintainers joining the rotation? Defer the decision to a quarterly retro once we see how the rubric is being used. *(seed Q open Q3)*
- **OQ3** — Discord vs Discussions shift: should we *deprecate* the Discord technical-question channel entirely, or just deprioritize it in the docs? Tension between not breaking existing contributors and not maintaining two surfaces. Deferred to the first post-deadline retro. *(FR6 + C3)*

## Provenance

| Requirement | Origin |
|---|---|
| FR1 (three-tier spine) | Scribe §spine |
| FR2 (shepherd rotation) | PM §intervention; mentor §handoff layered in |
| FR3 (review rubric) | Scribe + mentor + PM; debate Tension 2 |
| FR4 (second-issue handoff) | Mentor §intervention; debate Tension 4 |
| FR5 (good first issue recuration) | Scribe §recuration; seed Q open Q5 |
| FR6 (Discussions over Discord) | Mentor §discord-question-recurrence; debate Tension 5 |
| FR7 (externally-visible SLA) | PM §metrics |
| NFR1 (maintainer effort budget) | C4 + PM cost + scribe cost |
| NFR2 (measurable signal by week 10) | Seed Q9 forcing function; debate Tension 1 |
| NFR3 (content preservation) | C6 + R4 |
| AC1, AC2 (time-to-merge + second-PR-rate) | Seed brief success criteria |
| AC3 (shepherd SLA) | FR2 + FR7 |
| AC4 (spine shipped) | FR1 |
| AC5 (good first issue mislabel rate) | FR5 |
| AC6 (rubric linked in shepherd comments) | FR3 |
| AC7 (Discord question reduction) | FR6 |
| R1 (shepherd burnout) | Seed Q4 budget; PM cost |
| R2 (metric gaming) | Debate Tension 6; mentor §sustained-engagement |
| R3 (spine rewrite stalls) | Scribe §cost; debate Tension 1 sequencing |
| R4 (external link breakage) | C6 + NFR3 |
| R5 (recuration flurry) | Seed Q10 risk shape |
| OQ1-OQ3 | Debate carry-forwards + seed brief opens |
