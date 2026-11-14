# Round 1 advocate statement: Variant 2 (analyzer persona)

Source short names used below (all line numbers confirmed by reading, 2026-11-14):

- MR: `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`
- ADJ: `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`
- R01: `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/variant-1-original.md` (review 01)
- R05: `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/variant-5-original.md` (review 05)
- WC: `src/superclaude/core/WORKER-CONTRACT.md`

## Position summary

Variant 2 says: do not name a first ask now; leave OB-09 unstarted and ask Q19 again when QUESTION-LINK, the questions-read switch-on (OB-06) and the owner's AC-S record (OB-02) are all recorded.

The evidence case for it is that every release 3 prerequisite is open today. MR line 72: release 3 is "behind QUESTION-LINK (not established)". ADJ line 187: the questions read "is dark on master" and "the dated selection record (AC-S) does not exist". R05 line 252: "summary, issue/PR links, named steps and open-session have no source in either program", and no release row covers Fleet Quilt, Loop Detector or Mission Pulse. No source read records what data Fleet Quilt needs (question.md fact 4). A choice made now is a choice among asks whose inputs are unknown or missing.

As an analyzer I must also say plainly where this argument is thin: it is the spec's own default ("PLAN INFERENCE: OB-09 does not start", MR line 546) dressed as an answer, and it ties the choice to gates that only Decision Desk needs. Those weaknesses are set out under Concessions, and they lead me to judge Variant 3 better for the owner.

## Steelman of Variant 1

Strongest version: the only ask with a known, deterministic, already-reachable data source is the plain-English summary plus named steps, so build that first, in the program that already reads the inputs. R01 line 84 (F-08) confirms the sweep already reads the Orca Task spec text and that the brief carries the `Command:` lines; the deterministic option is a bounded `task_title` plus the `Command:` list. R01 line 86 (F-10) confirms workers write `<report-dir>/handoff/<n>-<command>.md` with `worker_status`, and WC line 64 (WC-15) confirms that file layout. This path waits on no release 3 gate, needs no language model ("Anything richer needs an LLM, which #409's AC forbids", R01 line 84), and gives the reviewer something real soon.

What it gets right: it is the only variant that is grounded in a concrete data source, and it correctly separates links out because they need a GitHub read the sweep does not make (R01 line 85, F-09). Its claim on X-003 is also right on the text: WC line 286 (WC-16) defines "recommends nothing" as "no stop, retry, release, merge or removal"; a task title and step states are observations, not recommendations.

Critique with counter-evidence:

1. Review 01 itself, the source Variant 1 leans on, recommends the opposite order. R01 line 167, item 9 "Order of work": "choose the direction first among Fleet Quilt, Decision Desk, Signal Bridge, then add only the fields those need." Variant 1 adds the fields before the direction is chosen.
2. Review 01 also puts the fleet view and links on the observer side, not the sweep: R01 line 162 (links are "observer-side `gh` reads, not the sweep, so Phase 1 stays GitHub-free") and line 163 ("observer merges per-Run reports").
3. The reviewer was looking at the observer dashboard. Q17's recommended answer is "No, not now" for showing sweep facts on the observer screen (MR line 544), so a summary in the sweep report stays invisible where the reviewer looked. Variant 1 admits this in its own costs section.
4. Whether the sweep's read rules allow reading `<report-dir>/handoff/` files is UNVERIFIED; R01 line 86 says only that the sweep reads none today ("no `handoff` in sweep/"). R05 line 214 describes the sweep side as having an "exact-token allow-list", so a new file read is a reviewed change, not free.
5. Citation slip: Variant 1 quotes "in the order the reviewer values" as R05 line 252. The phrase is on R05 line 254; line 252 is the Facts line. Minor, but it is the line the owner would check.

## Steelman of Variant 3

Strongest version: the spec (MR line 546; ADJ line 789) and review 05 (R05 line 254) both say Fleet Quilt or Decision Desk first, in the observer, and review 01 independently agrees on direction-first among the same names (R01 line 167). Naming the program and the candidate now satisfies OB-09 condition (2) (MR line 257: "Q19 names the first ask and its program") while the start date still waits for the contract note (XC-05, XC-07) and the shared capture (XC-03), exactly as graph row 60 lists them (MR line 707). It keeps the asks in the program the reviewer looked at and does not reopen the sweep's Phase 1 scope. It also does what D7 says the first step is: "the owner picks the first ask" (R05 line 254).

What it gets right: it separates choosing from starting. That gives the owner's direction now and the confirmed field meanings later, which is the main benefit Variant 2 claims, without Variant 2's cost of leaving the reviewer unanswered.

Critique with counter-evidence:

1. It does not fully answer the question. It returns a choice between two asks to the owner (its own "What stays unresolved"), so Q19 is half-closed.
2. Fleet Quilt has no recorded data source (question.md fact 4; R05 line 67 records only that it is unbuilt and in no release row). Picking it first means the first work is discovery, not delivery.
3. Decision Desk is blocked on QUESTION-LINK, "Not established" (R05 line 66), plus OB-06 and OB-02 (MR line 706). Picking it means nothing moves until those open, which in practice is Variant 2's timing.
4. Its priority argument rests on review 05's reading of the reviewer's order. R01 line 34 (C-06) re-read the comment, and R01 line 82 lists the reviewer's picks differently ("Fleet Quilt, Decision Desk, Loop Detector or Mission Pulse, Signal Bridge"), with the summary and links as a separate item. No source read shows the reviewer stating a ranking; "the order the reviewer values" is review 05's inference (see A-001).
5. Same citation slip as Variant 1 (cites R05 line 252 for the line 254 quote).

## Strengths claimed

1. Honest about unknowns. Variant 2 is the only variant that commits no work to an ask whose input is unknown (Fleet Quilt) or missing (links), matching R05 line 252 and question.md fact 4.
2. Least exposed to A-001. It does not depend on any reading of the reviewer's priority order, so if review 05's "Fleet Quilt and Decision Desk first" reading is wrong, Variant 2 loses nothing.
3. Accurate on release 3 state. Each fact it cites checks out: QUESTION-LINK "Not established" (R05 line 66), questions read dark and AC-S missing (ADJ line 187), and the BC-15 replacement text already says "decide where the reviewer's four asks are built" (ADJ line 557), so no #409 correction is needed. (One slip in Variant 2 itself: it cites R05 line 65 for "Not established"; that row is on line 66.)
4. Zero change cost. Nothing is added to `release-gates.md`, no sweep change, no new allow-list entry.

## Weaknesses identified in others

- Variant 1: contradicts review 01's own order-of-work recommendation (R01 line 167) and its placement of links and fleet view on the observer side (R01 lines 162, 163); lands output where Q17's default keeps it off the dashboard (MR line 544); relies on an UNVERIFIED allow-list change for handoff reads; departs from the spec and review 05 (MR line 546, R05 line 254).
- Variant 3: leaves the final pick to the owner; Fleet Quilt's data needs are unrecorded; Decision Desk carries every release 3 gate; its priority claim depends on an inference about the reviewer's order (A-001).
- Both: cite R05 line 252 for a quote that is on line 254.

## Concessions

1. Variant 2 is functionally identical to the default. MR line 546 already says that if Q19 is unanswered, OB-09 does not start. Picking Variant 2 gives the owner nothing that silence would not.
2. Its gate set is wrong for most of the asks. QUESTION-LINK, OB-06 and OB-02 gate release 3, which is Decision Desk (MR lines 257, 706). Fleet Quilt, Loop Detector, Mission Pulse and the summary are in no release row (R05 lines 67 to 69), so tying their choice to Decision Desk's gates is not supported by any source.
3. It goes against the first step D7 names: "the owner picks the first ask" (R05 line 254), and against review 01's item 9 (R01 line 167), which asks for the direction to be chosen first.
4. Its claimed benefit (deciding with XC-03 and XC-05/XC-07 in view) is also delivered by Variant 3, which waits for the same note and capture before starting (MR line 707).
5. It leaves the reviewer's 2026-11-11 comment without any answer on priority, which it admits.

## Shared assumptions

- A-001: QUALIFY. The diff analysis says nobody re-read the comment; that is not quite right. R01 line 34 (C-06) records the comment as verified (id 6798967760, created 2026-11-11T14:47:52Z). But the two reviews describe the asks differently: R01 line 82 lists the reviewer's picks as Fleet Quilt, Decision Desk, Loop Detector or Mission Pulse, Signal Bridge, with summary and links as a separate item (R01 lines 84 to 87), while R05 lines 66 to 69 and ADJ line 789 list summary and links as the fourth ask. No source read shows the reviewer stating an order; "the order the reviewer values" (R05 line 254) is review 05's reading. Whether list order means priority is UNVERIFIED.
- A-002: ACCEPT. MR line 130 says #423 (Orchestrator v2) is not started, is advisory only, "reads only what named collectors publish", and "neither collector carries command, objective, branch, changed paths, issue or PR today". So even a v2 home would first need the observer or the sweep to publish the data; the "which program" choice cannot bypass these two programs.

## Per-point verdicts (table)

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (no difference) | 90% | Same five sections in all three. |
| C-001 | Variant 3 | 55% | Spec, review 05 and review 01 item 9 all put Fleet Quilt or Decision Desk ahead; weakened by V3 naming two. |
| C-002 | Variant 3 | 65% | Reviewer looked at the observer; R01 lines 162, 163 put links and fleet view observer-side; Q17 default keeps sweep facts off the screen (MR line 544). |
| C-003 | Variant 1 | 70% | Only V1 needs no release 3 gate; V2 needlessly waits on all of them. |
| C-004 | Variant 1 | 80% | Only V1 names a confirmed deterministic source (R01 lines 84, 86; WC line 64). |
| C-005 | Variant 3 | 70% | Matches the spec and R05 line 254; capped by A-001. |
| X-001 | Variant 3 | 65% | Same evidence as C-002. |
| X-002 | Variant 3 | 60% | D7's first step is "the owner picks the first ask" (R05 line 254); deferral is already the default. |
| X-003 | Variant 1 | 60% | Only V1 addresses it, and WC line 286 defines "recommends nothing" as no stop, retry, release, merge or removal; the handoff-read allow-list is UNVERIFIED. |
| U-001 | Variant 1 | 75% | The deterministic-source finding is real and unique. |
| U-002 | Variant 2 | 50% | Unique framing, but V3 already waits for XC-03 and XC-07 before starting. |
| U-003 | Variant 3 | 70% | Meets OB-09 condition (2) (MR line 257) and follows D7. |
| A-001 | Variant 2 | 60% | Least dependent on the unverified priority reading. |
| A-002 | Tie | 70% | Accepted assumption; no variant is harmed by it. |

## Overall

Variant 3 best fits the evidence for the owner: it follows the spec, review 05 and review 01's direction-first order, meets OB-09 condition (2), and waits for the same note and capture that Variant 2 claims as its benefit. Variant 1's deterministic summary deserves to come right after, as a second release-gates row or a #534 item, because it is the only ask with a confirmed source. My own Variant 2 adds nothing beyond the default. The owner should know that Variant 3 still leaves a choice between Fleet Quilt and Decision Desk; of the two, Fleet Quilt avoids the QUESTION-LINK gate but has no recorded data source.

Overall: the variant I judge best for the owner is Variant 3, confidence 60%
