# Adversarial Debate Transcript: K-arm lead-in (DD-14)

## Metadata
- Depth: standard (Round 1, Round 2, Round 2.5; no Round 3)
- Rounds completed: 2 plus the invariant probe
- Convergence achieved: 100% (13 of 13 points agree on the blocking classification)
- Convergence threshold: 80%
- Advocates: V1 haiku defender, V2 sonnet prosecutor, V3 sonnet architect; Round 2.5 fault-finder: one sonnet agent. No Opus.
- Full statements are on disk, not copied here: Round 1 in `variant-1-haiku-defender.md`, `variant-2-sonnet-prosecutor.md`, `variant-3-sonnet-architect.md`; Round 2 in `debate/round2-V1.md`, `round2-V2.md`, `round2-V3.md`; Round 2.5 in `debate/invariant-probe.md`; the orchestrator's briefs in `debate/orchestrator-note-round2.md` and `work/corrections.md`.

## Round 1 (parallel): where each advocate stood
- V1 (defender): PASS. Strongest case against itself: "your own review" against CB-5 blurs the attention boundary. No defect conceded.
- V2 (prosecutor): looked for a blocking defect, found none, offered no replacement. Seven notes.
- V3 (architect): the draft is inside the acceptable range; offered its own 140-character design and a draft-against-design table; five notes.
- Orchestrator reading: unanimity this early is a risk. The prosecutor did not flip after a correction (unlike debate 2); it started on NO.

## Round 2 (sequential: V1, then V2, then V3; each read the earlier rebuttals)
- Orchestrator corrections before Round 2: CORR-1 to CORR-6 (work/corrections.md); CORR-7 was added after V1 found that `analysis/analyze.py` never reads `no_source` (confirmed by grep).
- V1: PASS held. Rejected V3's "time is not an input" and V2's unsupported 0.01-0.02. Added notes on no-source reporting and on extension documentation.
- V2: NO held. Withdrew its own size guess. Tested the cheapest fixes ("Apply each one to the plan"; dropping "in your own review of") and found neither evidence-backed.
- V3: NO held. Dropped "established direction" for the apply verb, withdrew its design as a recommendation, corrected its table on time, and wrote the reading sentences for the owner.
- The routes R-A to R-G of the orchestrator note were each ruled NOTE or NOT BLOCKING by all three advocates.

## Round 2.5 (invariant probe, one fault-finder, six categories)
14 findings, 0 HIGH. 9 UNADDRESSED (7 MEDIUM, 2 LOW), 5 ADDRESSED. The orchestrator verified on disk: the file hash and size, that `briefs/` and `cards/` are untracked, that `analysis/analyze.py` has zero reads of the brief or freeze fields, that RL holds identical card definitions and an identical lead-in, and that D7 uses no interval.

## Scoring Matrix
| Diff point | Winner | Confidence | Evidence summary |
|---|---|---|---|
| Q1 fair, strong control | Default (approve) | 75% | The draft is the owner's K (MR 1035); soft in two places, direction not established |
| Q2 leak | Default | 90% | The lead-in holds only the number "eight"; definitions are class-level card text |
| Q3 length and tone | Default | 80% | The difference is the treatment; REQ-40 reports K minus Z0 apart |
| Q4 "may have none" | Default | 75% | base.txt and CB-2 push the other way; SS carries "Most items are fine" |
| Q5 equivalence of information | Default | 90% | Not equivalent by design; K lists all eight definitions, SS prints none |
| R-A direction and size of bias | Default (NOTE) | 70% | D7 flips only if K minus Z0 is above about 0.08 (derived); no neutral wording exists |
| R-B overstrong K | Default (NOTE) | 70% | An apply verb moves K toward SS-lite; MR 1035 asks for plain words |
| R-C no-source definition | Default (NOTE) | 70% | A reporting gap for all arms; harm bounded to seconds or one vacuous finding; hold-out sources UNVERIFIED |
| R-D "your own review" and CB-5 | Default (NOTE) | 65% | Two opposite readings; CB-5 is verbatim (REQ-05) |
| R-E what is approved | Default (NOT BLOCKING) | 85% | Line 2 only; REQ-33 order holds |
| R-F action cost | Default (NOT BLOCKING) | 85% | The rule judges the default; an edit would split the RL copy |
| R-G "Eight" and the closing position | Default (NOTE) | 80% | `len(cs) == 8` test guard; the ending is the treatment |
| Overall: any blocking defect? | No | 80% | Three advocates, one fault-finder, zero HIGH |

## Convergence Assessment
- Points resolved: 13 of 13. Alignment: 100%. Threshold: 80%. Status: CONVERGED, with the caveats below.
- Caveat 1: all three advocates share one untested premise, that no real-model run of a K brief exists (A-001). Agreement cannot test it.
- Caveat 2: the labels differ inside the non-blocking class (NOTE against NOT BLOCKING). That is not a disagreement on the blocking question.
- Caveat 3: the Round 2 advocates were fresh agents. The Round 1 agents could not be resumed ("No transcript found"), so each Round 2 advocate re-read its own Round 1 file and the others; no private reasoning carried over.
- Unresolved points: none on the verdict. Open for the owner, not for the verdict: the hold-out `source: null` question and the optional K check run.
