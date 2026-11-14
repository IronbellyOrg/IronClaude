# Round 1 advocate statement: Variant 3 (architect persona)

Paths below are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/` unless stated. Every line number cited here was re-read in this round.

## Position summary

Variant 3 says the program's person-opened coordinator session creates the `issue-watch` worktree with an agent, owns that agent, and lists watcher sessions in its recurring checks, while closing them stays a person's action. Its architectural case is that ownership should sit with a session that already runs a recurring check, not with a person who must remember to look, and that this points toward the deferred watcher-to-orchestrator handoff (WA-07).

As the architect, I argue that case below. But reading the sources I also found that the coordinator's own contract scopes its loop to its Run, and the watcher has no end date. That mismatch is structural, not cosmetic. So I argue my variant's strengths honestly and still judge Variant 2 the better answer for the owner today.

## Steelman of Variant 1

Strongest version: the real missing decision is not "who owns" but "who closes". The source debate states plainly that "nothing closes or reaps those sessions" (`.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/round2-rebuttal-V2.md` line 91). Naming an owner without a closing rule just names the person who will be blamed for a growing pile of open sessions. Variant 1 refuses to start a live test (FU-1) whose sessions nobody is required to close, and pairs the two decisions (U-001). It also costs nothing irreversible: the default is already written (`.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md` line 547), and the #450 edit set still posts once without edit 4 (line 304, item 7).

What it gets right: it is the only variant that treats cleanup as a precondition rather than a follow-up, and it does not invent new duties for anyone.

Critique: FU-1 is one test issue, not a schedule. WA-04 runs one real launch and records the result (merged-requirements.md line 306); the schedule (WA-05, line 307) waits for that record. Holding FU-1 therefore blocks the very evidence (D-A: does a launch create a Run; D-B: what the session rows hold) that any cleanup or labelling rule would need. Q21 also waits on FU-1 (line 548). A hold with no trigger has no exit. The risk Variant 1 avoids (a worktree filling up) cannot occur during a one-issue test.

## Steelman of Variant 2

Strongest version: it is the spec's own recommended answer (merged-requirements.md line 547) and the source debate's recommended action: name the person and state that watcher sessions are never coordinator-owned (round2-rebuttal-V2.md line 93). It matches the watcher's design at every layer:

- The poller is "a plain process, never an Orca worker" (`docs/designs/issue-watcher.md` line 68), so no coordinator, Run or WC-16 loop is in its model.
- The day cap exists because it "bounds sessions the owner must review" (`docs/designs/issue-watcher.md` line 817). The design already assumes a reviewing person.
- The runbook already tells that person: "Expect sessions to stay open ... look at the open sessions now and then" (`docs/designs/issue-watcher-setup.md` line 571).
- The project rule lets a person own a worktree's agent: "A worktree a human creates needs an agent too" (`CLAUDE.md` line 312).

What it gets right: it keeps the coordinator contract unchanged, unblocks FU-1 and WA-05, and adds the concrete runbook note about `.dev/issues/<N>/` making the worktree show as uncommitted (U-002).

Critique: it leaves closing to "by hand" with no cadence, and it depends on a person who, if inattentive, leaves open sessions running in whatever permission mode the host uses (Variant 2's own risk line). "Never coordinator-owned" also closes a door that WA-07 (line 309) may later want open; that is a reversible ledger line, though, not a design commitment.

## Strengths claimed

1. **One accountable, already-running observer.** The coordinator is required to run `/sc:sweep` on every wake and read its report, and "Person-started sessions appear in the report, observed from transcripts and ccsession files" (`src/superclaude/core/WORKER-CONTRACT.md` line 288, WC-16). So the coordinator already sees watcher sessions as transcript rows. Variant 3 turns an observation the coordinator already makes into a named duty to report them, instead of relying on a person's memory.
2. **It is permitted by the project rule.** "The eligible session that creates a worktree owns its agent(s). An Orca coordinator is person-opened" (`CLAUDE.md` line 312). A coordinator session is eligible; a supervised worker is not (WC-13, `WORKER-CONTRACT.md` line 62). Variant 3 names the right kind of session.
3. **It keeps closing with a person.** Variant 3 does not let the coordinator stop or close anything, which matches WC-16's rule that `/sc:sweep` "recommends nothing: no stop, retry, release, merge or removal" and that person-started sessions "are never messaged" (line 288).
4. **Direction of travel.** The plan's deferred WA-07 hands approved issues from the watcher to an orchestrator (merged-requirements.md line 309). A coordinator that already lists watcher sessions is a smaller step toward that than a person-only model.
5. **It unblocks the same work as Variant 2.** WA-03, edit 4 and WA-04 all proceed (C-003).

## Weaknesses identified in others

- **Variant 1:** blocks the only evidence-gathering step (FU-1) for a risk that a one-issue test cannot produce; no trigger to revisit; Q21 and WA-05 stall with it (merged-requirements.md lines 306 to 307, 548).
- **Variant 2:** reliance on one person with no cadence; the review duty is real but nothing schedules it. Its "never coordinator-owned" wording is stronger than it needs to be to unblock FU-1.

## Concessions

These are real weaknesses of Variant 3, found by reading the sources:

1. **Lifetime mismatch (the decisive one).** WC-16 says "The coordinator keeps watching its Run until every Task it created is settled" (`WORKER-CONTRACT.md` line 288). Its loop is scoped to its own Run and ends when that Run settles. The watcher is a scheduled process with no end date (WA-05 enables a cron schedule, merged-requirements.md line 307). Tying an indefinite duty to a session whose contract ends with its Run is an ownership boundary error. Variant 3's own risk line ("A coordinator session ends and is resumed") understates this.
2. **Ownership by creation covers one agent, not the stream.** The creator rule (`CLAUDE.md` line 312) gives the creator the agent made by `worktree create --agent`. Watcher sessions are started later by the watcher process in that worktree (round2-rebuttal-V2.md line 91), not by the coordinator. So "the coordinator owns watcher sessions" does not follow from the rule Variant 3 cites; it is a new duty. (This gap applies to a person under Variant 2 as well, but Variant 2 frames it as review, not ownership.)
3. **It contradicts both written recommendations.** The spec (merged-requirements.md line 547) and the source debate (round2-rebuttal-V2.md line 93) both say "never coordinator-owned". Whether a coordinator may adopt watcher sessions is UNVERIFIED there.
4. **Review is mostly listing.** Sessions with no Run are "not observable" by the observer and appear in the sweep only as transcript rows, "could not determine" today (`.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md` line 242). The coordinator's review adds little over a person running `status` (`docs/designs/issue-watcher-setup.md` line 572).
5. **Which program's coordinator?** The watcher serves issue #331 and rollout #450 beyond this program; the variant does not say what happens when this program's coordinator finishes. UNVERIFIED whether any later coordinator would inherit the duty.
6. **It edits the coordinator contract.** WC-16 lists the coordinator's duties and escalation triggers; adding watcher review means a contract change that none of WA-01 to WA-07 schedules.

## Shared assumptions

- **A-001 (the day cap of 6 is fixed by design): QUALIFY.** It is fixed in code, not configurable: "The timeouts, the day cap of 6 launches in 24 hours ... are fixed in the code, not in the configuration file ... If one of them has to change, that is a code change, not a configuration edit" (`docs/designs/issue-watcher-setup.md` line 238). The same line says the design lists them "as proposals for you to confirm after the shadow run", so the owner may still choose a lower cap, but only through a code change and PR, which makes it a slower control than the diff analysis suggests. The design names the cap's purpose as bounding "sessions the owner must review" (`docs/designs/issue-watcher.md` line 817), which supports a person-review model.
- **A-002 (one shared configured worktree whatever Q2 answers): QUALIFY.** True for the first session: the watcher always starts in one configured worktree via `--worktree path:<wt>` (round2-rebuttal-V2.md line 91). Not true for the whole tree of sessions: at the default claim level the claim script starts a second agent in a worktree it created or reused (line 92). Under Q2's recommended `--pipeline none` the assumption holds; under the default it does not, and the second agent's ownership is a separate question none of the three variants answers.

## Per-point verdicts (table)

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 | Tie (all three) | 95% | Same five sections. |
| C-001 | Variant 2 | 70% | A person outlives any one Run; WC-16 scopes the coordinator to its Run (`WORKER-CONTRACT.md` line 288). |
| C-002 | Variant 2 | 65% | The cap exists to bound "sessions the owner must review" (`issue-watcher.md` line 817); accepting it with a named reviewer matches the design. |
| C-003 | Variant 2 | 70% | Unblocks WA-03, edit 4 and FU-1 without a contract change; Variant 3 unblocks the same but needs an unscheduled WC-16 change. |
| C-004 | Variant 3 | 55% | Only Variant 3 attaches a recurring check to open sessions; but closing is still by a person in both 2 and 3, and neither sets a cadence. |
| C-005 | Variant 3 | 60% | States the visibility limit as its own main weakness, the more honest framing; the limit itself is identical for 2 and 3. |
| X-001 | Variant 2 | 70% | "Never coordinator-owned" matches the design (`issue-watcher.md` line 68) and both written recommendations; can be revisited at WA-07. |
| X-002 | Variant 2 | 65% | Both are allowed by `CLAUDE.md` line 312; a person fits an open-ended duty, a session fits a bounded Run. |
| X-003 | Variant 2 | 70% | FU-1 is one test issue; waiting for a cleanup rule blocks the evidence that rule needs. |
| U-001 | Variant 1 | 60% | Pairing ownership with a closing rule is the right instinct; it should become a follow-up, not a gate. |
| U-002 | Variant 2 | 75% | Concrete, cheap runbook note grounded in review finding W-07. |
| U-003 | Variant 3 | 55% | Real value as a reporting aid, weakened by the Run-scoped loop. |
| A-001 | Variant 2 | 60% | QUALIFY: cap fixed in code (`issue-watcher-setup.md` line 238); its stated purpose is person review. |
| A-002 | None fully (Variant 2 closest) | 50% | QUALIFY: holds only under `--pipeline none`; no variant owns the claim script's second agent. |

## Overall

Variant 3's best idea, a recurring observer that reports open watcher sessions, can be added later as a reporting duty without making the coordinator their owner. Its core claim, that a Run-scoped coordinator session owns an open-ended watcher, conflicts with WC-16 and with both written recommendations. A good final answer would be Variant 2 plus two small additions: a review cadence for the named person, and a follow-up (from Variant 1) to decide who closes or reaps watcher sessions after FU-1 reports.

Overall: the variant I judge best for the owner is Variant 2, confidence 70%
