# Round 1 advocate statement: Variant 3 (frontend persona)

Variant 3 = proposal C: "Fleet Quilt or Decision Desk first, in the observer, after the contract note and the shared capture." Persona: user experience, meaning what the reviewer and the person at the dashboard actually see and need.

Short names for sources: MR = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; ADJ = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`; R01 and R05 = `variant-1-original.md` and `variant-5-original.md` in `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/`; WC = `src/superclaude/core/WORKER-CONTRACT.md`. Every line number below was re-read in this session.

## Position summary

The four asks came from a reviewer looking at screens: the twenty design images of the #409 package (ADJ line 93: "Names of designs in the twenty synthetic design images of the #409 package"). The question is what the person at the dashboard gets first. Variant 3 is the only answer that puts the first ask on the screen the reviewer was looking at, the observer, and it is the answer the spec already recommends (MR line 546; ADJ line 789) and the order review 05 recommended (R05 line 254: "in the order the reviewer values (Fleet Quilt and Decision Desk first). First step: the owner picks the first ask.").

The main user-experience point against Variant 1 is where its output lands. The sweep's report is "a dated local file; it is never posted" (WC line 288), and its reader is the coordinator. For the person at the dashboard to see it, the observer would have to show sweep facts, which is Q17, whose recommended answer is "No, not now" (MR line 544). So under the spec's own recommendations, Variant 1 delivers the summary to a file the reviewer never opens. Variant 1 admits this: "The summary appears in the sweep's report, not on the dashboard the reviewer looked at; showing it on the dashboard would need Q17 = yes" (variant-1-original.md line 23).

Variant 3 has a real cost: both of its candidates are slow. Decision Desk is behind QUESTION-LINK, "Not established" (R05 line 66), and Fleet Quilt has no recorded data source. I still argue the owner should choose Variant 3, and should name Fleet Quilt inside it, because the observer is where the asks pay off for a person and Fleet Quilt is in no release row, so it carries none of release 3's gates.

## Steelman of Variant 1

Strongest version: Variant 1 picks the only ask that can be built today from a known, deterministic, already-read source, with no language model. R01 F-08 (R01 line 84) shows the Orca Task brief text is already read by the sweep and that a bounded `task_title` plus the `Command:` list is a deterministic option; F-10 (R01 line 86) shows workers already write `<report-dir>/handoff/<n>-<command>.md` with `worker_status` (WC line 64, WC-15), so `steps: [{name, state}]` can be emitted with state words from `worker_status`, "not from colour or elapsed time". It waits on none of QUESTION-LINK, OB-06 or OB-02. It also builds the data layer a later Loop Detector or Mission Pulse screen would need, since the reviewer described that ask as named steps with green, yellow, red (R05 line 68). And a plain-English summary is an observation, not advice, so it plausibly fits "`/sc:sweep` recommends nothing" (WC line 288).

What it gets right: it is the most concrete and the least blocked. If the question were "what can ship soonest", Variant 1 wins.

Critique with counter-evidence:
1. It serves a different user. The reviewer's asks are dashboard asks; Variant 1's output reaches the coordinator's local report (WC line 288). With Q17 at its recommended "No, not now" (MR line 544), nothing reaches the dashboard, and the reviewer sees no change.
2. The person at the dashboard already has the closest field: Orca's worker-reported `projection.stage.activity` and `.detail`, shown in the observer's inspector (R05 line 69). So the added value of a sweep-only summary, for the dashboard user, is small until Q17 changes.
3. It departs from the spec and from review 05's ordering, which Variant 1 itself concedes (variant-1-original.md line 22).
4. It widens the sweep after Phase 1: a new report field and a new file read, each needing review, and it depends on PR #539 merging (variant-1-original.md lines 24 and 25).
5. It ships only half of the fourth ask: links are left out (variant-1-original.md line 11), because they need a GitHub read the sweep does not make (R01 line 85, F-09).

## Steelman of Variant 2

Strongest version: every release 3 prerequisite is open today. QUESTION-LINK is "Not established" (R05 line 66), the questions read is dark on master and the AC-S record does not exist (ADJ line 187). Choosing now risks committing to a screen whose data does not exist, and the spec's own default is that OB-09 does not start (MR line 546). Deferring until the shared capture (XC-03) and the contract note (XC-05, XC-07) exist means the owner chooses with real field meanings in view, and spends nothing on Fleet Quilt (no known source) or links (no GitHub read). Review 05 itself found that none of the asks has a source in either program today (R05 line 252).

What it gets right: it is honest that nothing on the observer side can move quickly, and it avoids sunk work.

Critique with counter-evidence:
1. It leaves the reviewer's comment of 2026-11-11 with no priority answer, which Variant 2 concedes (variant-2-original.md line 22). To a user, silence reads as "not heard".
2. Without a named first target, release 3 design "may drift toward whatever is easiest rather than what the reviewer valued" (variant-2-original.md line 23). That is a user-experience risk: the screen built may not be the screen asked for.
3. Its main benefit, choosing with the data in view, is already in Variant 3, which also starts work only after XC-07 and XC-03 (variant-3-original.md line 5). Variant 3 gets the same safety while recording the priority now and meeting OB-09 condition (2) (MR line 257).
4. It puts the question back on the critical path as one more owner decision later (variant-2-original.md line 24).
5. Minor citation error: it cites "variant-5-original.md line 65" for "Not established"; on re-read that text is at line 66 (line 65 is the Attention Ledger row). The fact stands; the line is off by one.

## Strengths claimed

1. **Right audience, right surface.** The asks are names of screen designs (ADJ line 93). The observer is the program that renders screens for a person; the sweep writes a local, never-posted file for the coordinator (WC line 288). Variant 3 keeps the first ask where its user is.
2. **Matches the spec and review 05.** MR line 546 and ADJ line 789 recommend exactly this answer. R05 line 254 recommends one `release-gates.md` row per ask with its data gate, Fleet Quilt and Decision Desk first, and says the first step is the owner picking the first ask. Variant 3 is that first step.
3. **Meets OB-09 condition (2) now.** MR line 257 lists "(2) Q19 names the first ask and its program". Variant 3 meets it; Variant 2 does not; Variant 1 takes the first ask out of OB-09 altogether (variant-1-original.md line 12).
4. **Designs against confirmed field meanings.** Starting after XC-07 (the final contract note) and XC-03 (one read-only recorded session against live Orca) means the screen is designed on real values, not guesses (variant-3-original.md line 18). Graph row 60 (MR line 707) records this ordering as Q19's recommendation.
5. **No other program changes scope.** The sweep stays at Phase 1 scope, read-only and recommending nothing (WC line 288); there is no new sweep field to review (variant-3-original.md line 17).
6. **A visible answer to the reviewer.** A dated ledger entry, "Fleet Quilt (or Decision Desk) first, in the observer", is a concrete reply about the screen they asked for, even before code exists.

## Weaknesses identified in others

- **Variant 1:** delivers to a surface the dashboard user does not see (WC line 288; MR line 544); departs from the spec and review 05 (variant-1-original.md line 22); widens the sweep after Phase 1 and depends on PR #539 merging (lines 24 and 25); leaves Fleet Quilt and Decision Desk undated (line 30); and ships only the summary half of the fourth ask (line 11).
- **Variant 2:** gives the reviewer no answer (line 22); invites design drift (line 23); adds a later decision on the critical path (line 24); and is the spec's default outcome (MR line 546), so choosing it is close to not answering Q19.

## Concessions

1. **Variant 3 leaves one more choice.** It says "Fleet Quilt or Decision Desk (you name which)" (variant-3-original.md line 5) and lists this as a cost (line 22). Q19 asks for one first ask, so this is a real weakness. My suggestion inside Variant 3 is Fleet Quilt, because Decision Desk cannot move until QUESTION-LINK is established (R05 line 66; MR line 257), while Fleet Quilt is in no release row (R05 line 67). This suggestion is my argument, not text in Variant 3.
2. **Fleet Quilt's data source is unknown.** No source read records what Fleet Quilt reads (question.md fact 4; variant-3-original.md line 24). Its first step is discovery, so "first" does not mean "soon".
3. **Variant 1 has the better data story.** The summary and named steps have a known, deterministic source (R01 lines 84 and 86). Variant 3 makes them wait (variant-3-original.md line 25).
4. **Variant 3 does not say where the summary and links will live** (line 30). The fourth ask is left without a home.
5. **The ordering rests on review 05's reading of the comment, not a re-read of the comment** (see A-001). R05's status table says only "Reviewer asked for it" for Fleet Quilt (R05 line 67); "in the order the reviewer values" is review 05's recommendation wording (R05 line 254). Whether the reviewer actually ranked the asks is UNVERIFIED.
6. **The wait is long.** "After XC-07 and XC-03" is later than Variant 1's "after PR #539 merges". Nothing visible to the reviewer ships soon under Variant 3.

## Shared assumptions

- **A-001 (review 05 reports the reviewer's asks and priority accurately): QUALIFY.** The list of asks is well attested (R05 lines 66 to 70; ADJ line 789), but the priority comes from review 05's recommendation wording (R05 line 254), and its table records only that the reviewer asked for each (R05 lines 67 and 68). The comment's author is not named in the sources read (question.md fact 1). Before recording Q19, the owner should re-read the 2026-11-11T14:47Z comment on #409; it is cheap and it is the one fact that could flip C-005 and X-001.
- **A-002 (the asks are built in the observer or the sweep, not left to Orchestrator v2 #423 or dropped): ACCEPT.** #423 is not started, is advisory only, and its gate "after #339 is complete" has two readings and cannot be applied (MR line 130). Waiting on v2 for the first ask would be a longer deferral than Variant 2's, and dropping the asks would ignore a reviewer request with no stated reason. The current program set is the realistic home for the first ask.

## Per-point verdicts (table)

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | None (equal) | 95% | All three use the same five sections. |
| C-001 | Variant 3 | 55% | The first ask should be a screen the reviewer can see; Fleet Quilt and Decision Desk are the asks review 05 put first. Low confidence because Variant 1's ask is the one buildable now. |
| C-002 | Variant 3 | 70% | The observer is the person-facing program; the sweep report is a never-posted local file (WC line 288) and Q17's recommendation is no (MR line 544). |
| C-003 | Variant 1 | 75% | It avoids every release 3 gate; Variant 3's Decision Desk option inherits them all. |
| C-004 | Variant 1 | 85% | Known deterministic source (R01 lines 84 and 86); Variant 3's sources are blocked or unrecorded. |
| C-005 | Variant 3 | 70% | Follows review 05's order and the spec (R05 line 254; MR line 546); confidence capped by A-001. |
| X-001 | Variant 3 | 70% | The asks are screen designs (ADJ line 93); the dashboard is where the reviewer looks. |
| X-002 | Variant 1 | 55% | Choosing now is right; Variant 1 names one ask, Variant 3 still leaves a two-way choice. |
| X-003 | Variant 1 | 65% | Variant 1 at least argues that a read-only observation field fits "recommends nothing" (WC line 288); Variant 3 sidesteps the question. |
| U-001 | Variant 1 | 80% | A deterministic, ungated path is the most useful new fact in the debate. |
| U-002 | Variant 2 | 60% | Tying the choice to real data is sound, though Variant 3 captures most of it by starting after XC-07 and XC-03. |
| U-003 | Variant 3 | 65% | One release-gates row per ask with its data gate is the concrete step review 05 asked for, and it meets OB-09 condition (2) (MR line 257). |
| A-001 | Variant 1 | 55% | Its case rests on data availability, not on the reviewer's ranking, so it holds if A-001 is false. |
| A-002 | Variant 2 | 55% | It leaves the program open, so it is least exposed if a wider home (v2) later becomes real. |

## Overall

For the person at the dashboard, the first ask should be something they will see on the dashboard. Only Variant 3 does that, in line with the spec and review 05. Its weaknesses are real: it leaves a two-way choice, and both candidates are slow. Variant 1 is faster, but its output reaches a coordinator's local report that the reviewer never sees unless Q17 changes. I recommend that the owner take Variant 3, name Fleet Quilt, and re-read the reviewer's comment before recording the answer.

Overall: the variant I judge best for the owner is Variant 3, confidence 55%
