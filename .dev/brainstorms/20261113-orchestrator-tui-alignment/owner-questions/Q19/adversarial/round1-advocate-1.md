# Round 1 advocate statement: Variant 1 (backend persona)

Abbreviations: V5 = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/variant-5-original.md` (review 05); R01 = the same folder's `variant-1-original.md` (review 01); MR = `merged-requirements.md`; ADJ = `alignment-findings-adjudicated.md`; WC = `src/superclaude/core/WORKER-CONTRACT.md`. Every line number below was read in this round.

## Position summary

Variant 1 says: build the plain-English summary and named steps first, as a deterministic Phase 2 addition to the sweep's report, and leave issue and PR links, Fleet Quilt and Decision Desk for later.

From a data-integrity point of view this is the only variant whose first ask has a known source today. Every field it needs is already written by a process the project controls:

- The task title and `Command:` lines come from the Orca Task brief, which the sweep already reads (R01 line 84, F-08: "Orca Task spec text is already read").
- Step names and states come from the worker's handoff files. WC line 64 (WC-15) requires the worker to write `<report-dir>/handoff/<n>-<command>.md` after each `Command:` line, "whatever its outcome", and that file carries `worker_status`.
- R01 line 86 (F-10) calls named steps a "Gap, with a feasible deterministic source" and requires that "State words must come from `worker_status`, not from colour or elapsed time". Variant 1 adopts that rule word for word.

No language model, no new external read, and no release 3 gate stands in the way. The other two variants either have no data source for the first ask (Fleet Quilt) or wait on a gate that is "Not established" (Decision Desk, V5 line 66).

## Steelman of Variant 2

The strongest form of Variant 2: every release 3 input is open today. QUESTION-LINK is "Not established" (V5 line 66), the questions read is dark on master and the AC-S record does not exist (ADJ line 187). The shared capture (XC-03) and the contract note (XC-05, XC-07) would tell us what Orca's fields really mean. Choosing a first ask before those facts exist risks building against guessed field meanings, and any commitment made now may have to be undone. The spec's own default for Q19 is "OB-09 does not start" (MR line 546), so Variant 2 costs nothing in spec terms. It is also the only variant that makes zero scope change to any program.

What it gets right: it correctly reads that the observer's release 3 cannot start yet, and it refuses to spend work on an ask whose data source is unknown (Fleet Quilt). That is sound data discipline.

## Steelman of Variant 3

The strongest form of Variant 3: it follows both the spec's recommendation (MR line 546, ADJ line 789) and review 05's ordering ("in the order the reviewer values (Fleet Quilt and Decision Desk first)", V5 line 254). It keeps the asks in the program the reviewer was actually looking at, the observer dashboard, so no other program's scope grows. Waiting for the contract note and the shared capture means the release is designed against confirmed field meanings. It also meets OB-09 condition (2) ("Q19 names the first ask and its program", MR line 257) cleanly, and it adds review 05's one-row-per-ask discipline with an explicit data gate per row (V5 line 254), which is the right structure for any later ask.

What it gets right: the reviewer's request was about a dashboard, and the observer is the program that owns screens. Variant 3 also honestly lists its own blockers (Decision Desk behind QUESTION-LINK; Fleet Quilt with no recorded data source).

## Strengths claimed

1. **Known, deterministic source (C-004).** Covered above: brief text already read by the sweep (R01 line 84), handoff files mandated by WC-15 (WC line 64), state words from `worker_status` (R01 line 86).
2. **Waits on no release 3 gate (C-003).** QUESTION-LINK, OB-06 and OB-02 gate OB-09 (MR line 257; graph row 59, MR line 706). None of them touches the sweep's report.
3. **Fits the sweep's rules (X-003).** WC line 288 (WC-16) defines "recommends nothing" as "no stop, retry, release, merge or removal". A task title and a list of step names with their reported `worker_status` are observations, not recommendations, so they sit inside that rule.
4. **It is the collector-side prerequisite every consumer needs anyway.** MR line 130 says v2 "must read only what named collectors publish, and neither collector carries command, objective, branch, changed paths, issue or PR today". Whoever eventually displays a summary (observer, v2) needs a collector to publish these fields first. Variant 1 builds that layer first, so later display work does not invent its own source.
5. **Honest about links.** It drops issue and PR links from the first step because they need a GitHub read the sweep does not make and a new allow-list (R01 line 85, F-09), instead of promising them.

## Weaknesses identified in others

**Variant 2.**
- It answers Q19 with "not yet", so OB-09 condition (2) stays unmet (MR line 257) and the reviewer's comment of 2026-11-11 gets no priority answer. Its own costs section admits this.
- The wait buys little for the summary and named steps: their sources (brief text, handoff files) do not depend on QUESTION-LINK, OB-06 or OB-02 at all. Deferring them waits on gates that are irrelevant to their data.
- Citation slip: it cites V5 line 65 for "Not established"; that text is on V5 line 66 (line 65 is the Attention Ledger row). Minor, but the fact itself is correct.

**Variant 3.**
- Neither of its two candidates has a usable data source today. Decision Desk needs QUESTION-LINK, "Not established" (V5 line 66). Fleet Quilt has no recorded data source in the sources read (question.md fact 4; V5 line 67 says the name appears only in issue-body copies). Variant 3 admits "its first step is discovering what it needs". From a backend view that is an ask with no data contract yet.
- It does not pick one ask; it leaves a two-way choice, so Q19 is only half answered.
- Its ordering argument rests on review 05's reading of the comment, which nobody re-read (A-001). R01 line 82 (F-06) lists the reviewer's picks as "Fleet Quilt, Decision Desk, Loop Detector or Mission Pulse, Signal Bridge", which may simply be list order, not a ranking. UNVERIFIED either way.
- Citation slip shared with Variant 1: both cite V5 line 252 for "Fleet Quilt and Decision Desk first"; the quote is on V5 line 254.
- It does not address how the observer would get sweep facts at all; MR line 257 condition (3) says a sweep-facts read needs Q17 = yes and SW-11, and MR line 544 recommends Q17 = "No, not now".

## Concessions

1. **It does not map cleanly onto one of the four asks.** The four asks are (3) Loop Detector or Mission Pulse (named steps with green, yellow, red) and (4) a plain-English summary with issue and PR links (question.md fact 1). Variant 1 takes the named-steps part of ask 3 and the summary part of ask 4, minus links. An owner who wants "one of the four" gets a blend.
2. **Wrong surface for the reviewer.** The summary appears in the sweep's Markdown report, not on the dashboard the reviewer looked at. Showing it on the dashboard needs Q17 = yes, which the spec recommends against for now (MR line 544).
3. **Departs from the spec and review 05.** MR line 546 and V5 line 254 both put Fleet Quilt and Decision Desk first. Review 05 also says to settle D1 and D3 first (V5 line 254); Variant 1 skips that ordering.
4. **Worker-reported, not verified, state.** `worker_status` in a handoff file is what the worker says about itself. It is not an Orca outcome. A crashed worker leaves no handoff file for the step it was in, so the current step's state is absent, not "running". The report must show absence as unknown, never as a colour. Variant 1 does not spell this out.
5. **New reads cost review.** Reading handoff folders is a new file read for the sweep; it must stay bounded (WC-15 caps handoff files at 40 lines, WC line 64) and read-only, and it needs its own PR review after PR #539 merges.
6. **Q19's program question for OB-09.** Variant 1 names the sweep, which leaves OB-09 (an observer release) with no first ask to carry. Whether that satisfies OB-09 condition (2) is a reading question the owner must settle.

## Shared assumptions

- **A-001: QUALIFY.** All three variants take review 05's report of the comment as given, and nobody re-read it. The list of asks is consistent across ADJ line 789, V5 lines 66 to 69 and R01 line 82, so the list itself is likely accurate. The priority is not: R01 line 82 lists the reviewer's picks in a different set (it includes Signal Bridge), and nothing read shows the comment states a ranking. Variant 1 depends least on this assumption, because it is chosen by data availability, not by ranking. Before the owner relies on "the order the reviewer values", someone should re-read the 2026-11-11T14:47Z comment.
- **A-002: QUALIFY.** It is true that all three assume the observer or the sweep builds the asks. But v2 (#423) is "NOT STARTED" (MR line 78) and "must read only what named collectors publish" (MR line 130), so v2 cannot carry a summary until a collector publishes one. The program set is therefore wider for display, but not for the data source: the sweep or the observer must publish the fields first in any case.

## Per-point verdicts

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | None (tie); Variant 1 recorded nominally | 35% | Same five sections in all three |
| C-001 | Variant 1 | 60% | The only first ask with a known source; weakened by blending asks 3 and 4 (Concession 1) |
| C-002 | Variant 1 | 55% | The sweep is the collector that already reads the brief; the observer is the better display home, which keeps this close |
| C-003 | Variant 1 | 80% | Its data needs none of QUESTION-LINK, OB-06, OB-02 (MR lines 257, 706) |
| C-004 | Variant 1 | 85% | R01 lines 84 and 86; WC line 64 |
| C-005 | Variant 3 | 80% | Matches MR line 546 and V5 line 254 |
| X-001 | Variant 1 | 55% | For the data, the sweep; for the screen, the observer; first step is data |
| X-002 | Variant 1 | 65% | Chooses now and picks one; Variant 3 leaves a two-way choice |
| X-003 | Variant 1 | 70% | Only variant that addresses it; WC line 288 limits "recommends nothing" to actions |
| U-001 | Variant 1 | 85% | Deterministic source with no release 3 gate |
| U-002 | Variant 2 | 60% | Real value in deciding with the capture and note in hand |
| U-003 | Variant 3 | 70% | One row per ask with its data gate (V5 line 254) |
| A-001 | Variant 1 | 60% | Least dependent on an unre-read ranking |
| A-002 | Variant 1 | 55% | MR line 130: any later consumer needs a collector to publish the fields first |

## Overall

Variant 1 is the only answer whose first deliverable can be built today from data the project already controls, without waiting on a gate that is not established. Its real costs are that it does not land on the reviewer's dashboard, it blends two asks, and it departs from the spec's recommendation. Variant 3 is the closest competitor and wins on fit with the stated priority, but its two candidates have either no data source or a blocked one.

Overall: the variant I judge best for the owner is Variant 1, confidence 60%
