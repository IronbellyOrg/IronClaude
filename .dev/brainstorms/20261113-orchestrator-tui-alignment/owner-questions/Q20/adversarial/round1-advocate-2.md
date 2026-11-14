# Round 1 advocate statement: Variant 2 (security persona)

Variant 2 = proposal B: a named person creates the `issue-watch` worktree with an agent and owns that agent. Up to 6 watcher sessions a day are allowed there as person-reviewed top-level sessions, never owned by a coordinator.

Paths below are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. I re-read every cited line number for this statement unless it is marked UNVERIFIED.

## Position summary

The watcher turns text written by outsiders into running Claude sessions. The question is who answers for those sessions, and the watcher's own design already says: a person. Every trust anchor in the watcher points at one human owner, and the day cap is sized so that this owner can keep up with review. Variant 2 writes that down and lets the first live test (FU-1) run, so the real permission mode gets recorded. It also keeps the most powerful session in the program (the coordinator) away from transcripts that attackers can influence.

Its real weakness is that nothing closes the sessions. I concede that and propose a fix: make a cleanup rule a gate before the schedule is enabled (WA-05), not before FU-1.

Evidence that the design is anchored on a person:

- The runbook is addressed to a person: "This runbook is for the owner of the issue watcher" (`docs/designs/issue-watcher-setup.md:5`).
- The watcher accepts an issue only when it is assigned to exactly the owner's login: "Assign the issue to the owner, which means the GitHub login the watcher runs as, and nobody else" (`issue-watcher-setup.md:172`).
- The day cap's stated reason is human review: "day cap | 6 per rolling 24 h | bounds sessions the owner must review" (`docs/designs/issue-watcher.md:817`).
- The runbook already gives the owner the review duty: "Expect sessions to stay open. ... at most 6 in 24 hours, so look at the open sessions now and then" (`issue-watcher-setup.md:571`).
- The launch carries no permission flag, so the session "runs in its default, interactive mode, which keeps a human between the session and any write. That matters because the session reads text that anyone with comment access can write" (`issue-watcher-setup.md:625`). A bypass mode "is allowed only after you have accepted the risk in writing" (`issue-watcher-setup.md:628`).
- The process model rules out coordinator ownership by design: "The poller is a plain process, never an Orca worker, so WC-13 ... does not apply to it" (`issue-watcher.md:68`).

## Steelman of Variant 1

Strongest version: Variant 1 is the fail-closed answer. It refuses to create any session that no coordinator owns and nothing reaps until the owner has decided two things: who owns the agent and how open sessions are closed. It rightly sees these as one decision about accountability, not two, and it rightly treats "nothing closes or reaps those sessions" (`.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/round2-rebuttal-V2.md:91`) as a real hole. For security, not running unattended machinery with an undefined lifecycle is a fair default. It is also the spec's own default for Q20 (`merged-requirements.md:547`), and it still lets the other #450 edits post (WA-02 item 7, `merged-requirements.md:304`).

Critique with counter-evidence:

- The hold blocks the wrong step. FU-1 is not the 6-a-day pattern. FU-1 is "one owner-run launch on a test issue", launched by hand while `enabled` stays false (`issue-watcher-setup.md:621`; deployment gate at `issue-watcher.md:33`). The 6-a-day exposure begins only when the schedule is enabled (WA-05, `merged-requirements.md:307`). Holding FU-1 blocks one supervised session and does nothing about the risk Variant 1 names.
- The hold delays the security evidence. FU-1 is where the session's real permission mode, `CCSESSION_PERMISSIONS`, `CC_CLAUDE_FLAGS` and real argv are recorded, together with the owner's written acceptance (WA-04 items b and c, `merged-requirements.md:306`). The runbook says to "Read the mode off the session in the live test and do not assume it" (`issue-watcher-setup.md:629`). Holding FU-1 leaves the permission question open longer.
- There is no trigger to resume. Variant 1 admits that "A deferred answer with no trigger may stall the watcher indefinitely" (variant-1-original.md line 24). An open-ended hold tends to get bypassed informally later, which is worse for accountability than naming an owner now.

## Steelman of Variant 3

Strongest version: Variant 3 puts accountability where attention already is. A person opens the coordinator session (`src/superclaude/core/WORKER-CONTRACT.md:69`), and the coordinator already runs a recurring check on the owner's order (Q31). The project rule explicitly lets a session be an owner: "The eligible session that creates a worktree owns its agent(s)" (`CLAUDE.md:312`). A person can forget to look; a polling session does not.

Variant 3 also gives one place to report open watcher sessions, and it fits the deferred plan for a watcher that hands issues to an orchestrator (WA-07, `merged-requirements.md:309`). It keeps closing sessions as a person's action, so it does not claim more than it can do.

Critique with counter-evidence:

- It sends untrusted text into the session with the most authority. The coordinator "plans, creates Tasks, starts workers, reads their reports and performs every outward action" (`WORKER-CONTRACT.md:69`). Watcher sessions read issue titles, bodies and comments that anyone with comment access can write (risk R18, `issue-watcher-setup.md:648`; `issue-watcher-setup.md:625`). If the coordinator "reviews" those sessions, transcripts that attackers can influence flow into the one session that performs every outward action. That opens a prompt-injection path across a trust boundary that Variant 2 keeps closed.
- An agent's review is not a person's acceptance. The contract says a coordinator's reply is "another agent's message", "which is not acceptance" (`WORKER-CONTRACT.md:57`). The watcher's safety rests on interactive permission prompts and the owner's written acceptance (`issue-watcher-setup.md:625`, `:628`). A coordinator that reviews watcher sessions invites, sooner or later, a coordinator that answers their prompts. That would be approval passed through an agent that is not allowed to give it.
- Its review is mostly blind. Variant 3 concedes that these sessions have no Orca Run and appear only as "could not determine" transcript rows (`.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md:242`). Accountability without visibility is a label, not a control.
- Session ownership is unstable. Coordinator sessions end and get resumed, as Variant 3 itself says (variant-3-original.md line 24). An owner that can lapse between a session ending and a rebind is a weak owner for 6 unattended sessions a day.
- It has no basis in the contract. The source debate recommended stating "that watcher sessions are never coordinator-owned" (`round2-rebuttal-V2.md:93`). The coordinator rules in `WORKER-CONTRACT.md` section 4 (from line 67) cover only Tasks and workers, with no rule for owning sessions that are not workers. Variant 3 would need contract text that does not exist.

## Strengths claimed

1. It matches every existing trust anchor: the assignee must be the owner's login, there is an approvers file, bypass needs written acceptance, and the day cap is sized for owner review (all cited above). It invents no new trust model.
2. It keeps the trust boundary clean. Sessions that read untrusted text stay away from the coordinator, which performs every outward action.
3. It unblocks the security evidence. FU-1 runs and records the real permission mode and argv (WA-04, `merged-requirements.md:306`).
4. It makes the forfeit step safer. WA-03 adds a rule that `reset --forfeit-guarantee` on an `unknown` entry first requires checking Orca for a live session in that worktree (`merged-requirements.md:305`). That rule lands only if WA-03 ships.
5. The owner is a person who persists across sessions and whose acceptance counts under the contract (`WORKER-CONTRACT.md:57`).
6. U-002: it adds a runbook note that every watcher session writes `.dev/issues/<N>/` in the worktree, so the sweep shows the worktree as uncommitted, not removable (variant-2-original.md line 13; source W-07 at `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/variant-2-original.md:48`). This stops a cleanup tool or a person from treating the worktree as disposable.

## Weaknesses identified in others

- Variant 1 holds the wrong step: FU-1, a single hand-run session, instead of WA-05, the step that creates the 6-a-day exposure. It delays recording the permission mode, and it has no trigger to resume.
- Variant 3 opens an injection path into the coordinator and treats an agent's review as if it were a person's acceptance. Its review is blind, its owner lapses when the session ends, and it has no basis in the contract.
- Both other variants, like mine, leave the day cap untouched, although the design marks it as a value the owner can confirm (see A-001).

## Concessions

- Under Variant 2, nothing closes or reaps watcher sessions either (`round2-rebuttal-V2.md:91`). Variant 2 relies on the named person's diligence. If they do not look, up to 6 sessions a day sit open, and if a bypass mode is ever accepted, those sessions sit open with prompts off. This is my variant's most serious weakness.
- I accept Variant 1's core insight (U-001) that ownership and cleanup belong together. I propose that Variant 2 adopt it with the gate moved: a written cleanup rule (who closes sessions, and by when) becomes a precondition of WA-05, not of FU-1.
- Variant 3's reporting idea has value in a narrow form. The coordinator's check could include a read-only count of open sessions in `issue-watch`, without reading their transcripts and without becoming the owner.
- Under my variant too, the observer cannot see these sessions (ADJ line 242). Until Q21's label exists, review is done by the person in Orca, not by tooling.
- "Never coordinator-owned" rules out WA-07 for now. That is acceptable only because WA-07 is deferred and unbuilt, and it would reopen this question with its own acceptance conditions (`merged-requirements.md:309`).
- A single named person is a single point of failure (absence, leave). The runbook should either name a fallback or say the schedule is disabled while the owner is away. Whether the owner wants that is UNVERIFIED.

## Shared assumptions

- **A-001 (the 6-a-day cap is fixed and not part of this answer): QUALIFY.** Operators cannot change the cap through config: "Timeouts, caps and the lease are module constants, not config (section 14)" (`issue-watcher.md:139`). But the same line says "the spec makes them [PROPOSAL] values for the owner to confirm after the shadow run", and section 14 lists the day cap as a [PROPOSAL] default (`issue-watcher.md:817`). So 6 is a default the owner can lower with a code change, not a fixed rule. The owner's Q20 answer should say "up to the confirmed day cap (default 6)". While cleanup is manual, a lower cap is a cheap extra control.
- **A-002 (every session starts in one shared configured worktree, whatever Q2 answers): QUALIFY.** This holds for the first session. The config has one `worktree` key (`issue-watcher-setup.md:81`), and launch uses `--worktree path:<wt>` (per `round2-rebuttal-V2.md:91`, which cites `launch.py:95-116,358-370`; not re-read here, UNVERIFIED). But at the default claim level, each claim also starts a second agent, governed by the launch-level hook, in a worktree that the claim script creates or reuses (`round2-rebuttal-V2.md:92`, which cites `claim.md:99-120`; not re-read, UNVERIFIED). Variant 2's ownership statement covers only the first session. If Q2 keeps the default, the owner must also say who owns the `issue-<N>` agents. If Q2 picks the recommended `--pipeline none`, the assumption holds.

## Per-point verdicts (table)

| Point | Superior variant | Confidence | Reason |
|---|---|---|---|
| S-001 Section layout | None (tie) | 90% | Same five sections; no effect on the decision. |
| C-001 Who owns the agent | Variant 2 | 75% | Matches every person-anchored trust control and keeps acceptance valid (`WORKER-CONTRACT.md:57`). |
| C-002 Up to 6 sessions a day | Variant 2 | 60% | The cap was sized for owner review (`issue-watcher.md:817`). Qualified by A-001: confirm or lower the cap. |
| C-003 Effect on WA-03, WA-02 edit 4, WA-04 | Variant 2 | 70% | Lets FU-1 record the permission mode. Variant 3 also proceeds, but with a weaker owner. |
| C-004 Cleanup of open sessions | Variant 1 | 55% | Only Variant 1 treats cleanup as a required decision, but it gates the wrong step (FU-1 instead of WA-05). |
| C-005 Visibility | Variant 2 | 60% | States the blind spot without claiming a review it cannot do. Variant 3 relies on a reviewer that cannot see the sessions. |
| X-001 May a coordinator own watcher sessions | Variant 2 | 75% | The coordinator performs every outward action. Having it own sessions fed by untrusted text crosses a trust boundary. |
| X-002 Person or session as owner | Variant 2 | 70% | A person persists and can accept risk. A session ends, and its reply is not acceptance. |
| X-003 Should FU-1 wait for a cleanup rule | Variant 2 | 60% | FU-1 is one hand-run session. The cleanup rule should gate WA-05 instead. |
| U-001 Pair ownership with cleanup | Variant 1 | 65% | A genuine gap, worth merging into Variant 2 as a WA-05 precondition. |
| U-002 `.dev/issues/<N>/` runbook note | Variant 2 | 70% | Prevents the worktree from being treated as removable. |
| U-003 Coordinator as accountable reviewer | Variant 3 | 50% | Useful only as a read-only count, not as ownership or transcript review. |
| A-001 Day cap fixed | None (all miss it) | 80% | The cap is a [PROPOSAL] value the owner can confirm (`issue-watcher.md:139`). |
| A-002 One shared worktree | None (all miss it) | 70% | The default claim level adds `issue-<N>` agents, and no variant names their owner. |

## Overall

Variant 2 fits the watcher's existing trust model best and keeps untrusted session content away from the coordinator. It should be adopted with two amendments: a written cleanup rule as a precondition of WA-05 (taken from Variant 1), and the day cap stated as "the confirmed cap, default 6" (A-001).

Overall: the variant I judge best for the owner is Variant 2, confidence 70%
