# Round 1 Advocate Statement: Variant 3 (Proposal C, "Yes, read-only, for this program's coordinator")

## Position

Variant 3 is the best answer to the question as asked. Q31 asks whether the 2026-11-05 order "appl[ies] to this program's coordinator" (question.md, line 7). Variant 3 answers exactly that: yes, as a read-only check, scoped to this program, with the mechanism limits (7-day cron expiry, session-only life) and the later reporting order (2026-11-09) folded in. It follows the owner's standing order without widening the question into a change to an installed core file, and it closes INV-010 with an owner answer rather than a silent pick, which is why the question exists (question.md, fact 3).

Facts I re-checked read-only for this statement:

- The memory note (modified 2026-11-05) says: "Keep a recurring CronCreate sweep (every ~10 minutes, off-minute) that re-checks the Orca run, ListAgents, open PRs on IronClaude and Coder, and re-subscribes `notify_when_idle` on busy peers", and gives the reason "Peer sessions (interactive, not Orca workers) do not appear in the Orca message queue at all."
- `src/superclaude/core/WORKER-CONTRACT.md:288` (WC-16) says "The coordinator keeps that pass scheduled while work remains. Phase 1 adds this duty, not a scheduler." The same paragraph also says "Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged."
- `merged-requirements.md` line 579: "Q31 does not authorize `/sc:sweep` above WC-16's cap or any write." The cadence record's last row (line 1026) reads "status is Q31's answer; never runs `/sc:sweep` more often than WC-16 allows and never writes".

## Steelman of Variant 1

Strongest version: the coordinator's behaviour should be auditable from checked-in files alone. WC-16 is the contract every coordinator signs; it already says "It never stops watching on its own. When a wait on Orca expires, the coordinator re-arms it", which directly fixes the failure that caused the 2026-11-05 order (a lapsed wait). The spec already reads each PR "at coordinator wakes with `gh pr view <N> --repo IronbellyOrg/IronClaude`" (line 1025). Once SWEEP-RUNNABLE holds, `/sc:sweep` reports "Person-started sessions ... observed from transcripts and ccsession files" (WC-16), which covers much of what the timer was for. So a second clock adds load, an unverified "is a cron fire a wake" question, and a 7-day expiry hazard, for coverage the contract mostly already gives. Variant 1 is also honest about its cost: it names that it "overrides a standing owner order that exists because of a real failure".

What it gets right: one clock family, no expiry management, and no ambiguity about whether a fire triggers the sweep pass (Variant 1, "What it unlocks"). It is the only variant with zero mechanism risk.

## Steelman of Variant 2

Strongest version: the real defect INV-010 found is that the order lived only in memory, "so two of three debate drafts wrote 'no extra scheduler' without it" (Variant 2, citing `invariant-probe.md:18`). Answering "yes" for one program leaves the next coordinator in the same trap. Writing the rule into WC-16 fixes it at the source, settles the "Phase 1 adds this duty, not a scheduler" ambiguity in the contract text, and lets the contract say once whether a cron fire is a "coordinator wake". Variant 2 keeps an immediate "yes" for this program, so nothing is lost while the PR is in flight.

What it gets right: it is the only variant that removes the root cause, and it correctly warns that a contract rule naming a 10-minute cron "must also say what happens on expiry and on resume, or it writes a promise the tool cannot keep".

## Key strengths claimed

1. **Answers the question at the scope asked.** Q31 is about "this program's coordinator" (question.md line 7) and gates only "the status of the last row of the 6.6 cadence record" (question.md, "What it gates"). Variant 3 sets that row to "in force" and stops. It does not turn a W0 intake question into a change to an installed core file.
2. **Follows the owner's order and its reason.** The order exists because non-worker peers "do not appear in the Orca message queue at all" (memory note). This program has such peers: the PR sessions of Q25 and the #539 author of Q33 (Variant 3, "What it unlocks"; Variant 1 concedes the same in its costs).
3. **Handles the mechanism limit concretely.** Only Variant 3 says what to do about the 7-day expiry and session-only life: "records the job id and its expiry in the ledger and re-creates it on expiry or after a resume" (diff-analysis U-002, rated High). Variant 2 only says a future rule "must also say what happens".
4. **Reconciles the two owner orders.** Variant 3 makes routine runs silent and reports only decisions, matching the 2026-11-09 order (memory `orchestration-decision-ledger-only.md`, question.md fact 5). Variant 2 leaves this "unresolved".
5. **Keeps the spec's hard limits.** "No `/sc:sweep` above WC-16's 5-minute cap, no write of any kind, no grant implied" (Variant 3), matching line 579 and line 1026 word for word in substance.
6. **Honest about the open reading.** It names the "is a cron fire a coordinator wake" question as UNVERIFIED and shows the outcome stays inside the cap either way.

## Weaknesses identified in Variant 1

- It overrides a standing owner order on the strength of a contract sentence that probe INV-010 says is "not a ban on that cron" (question.md fact 3). Answering "no" here is the silent-pick-in-reverse the question was raised to avoid.
- Its coverage argument leans on `/sc:sweep`, but `/sc:sweep` is "not runnable" until SWEEP-RUNNABLE holds (line 1031 note; question.md fact 7). During W0 and until PR #539 merges and Q29's route runs, nothing in WC-16 watches non-worker peers. Variant 1 itself lists "How non-worker peers ... are supervised between their own reports" as unresolved.
- Its PR reads happen "at coordinator wakes"; a coordinator waiting on a quiet Orca Run may not wake for a long time (its own words: "on a quiet day that could be long").
- It says nothing about IronbellyOrg/Coder PRs, which the order names; the existing GitHub row reads only `IronbellyOrg/IronClaude`.

## Weaknesses identified in Variant 2

- Scope growth beyond the question. It changes `~/.claude/WORKER-CONTRACT.md`, "an installed core file ... that every project using IronClaude receives", through "a question that was framed for one program" (Variant 2's own costs). Q31 gates no work item (dependency edge 101: "Recorded only; they gate no item"); Variant 2 creates one.
- Adds a PR during a program whose stated bottleneck is owner latency (Variant 2 quotes section 3: "Owner latency is the real schedule").
- Writing a 10-minute cron into the contract for every project hard-codes the IronClaude and Coder repo scope, which Variant 2 admits "may be wider than every coordinator needs".
- Leaves reporting style unresolved, so until the contract PR lands the check could produce routine notices the 2026-11-09 order forbids.
- Its immediate "yes" half is the same as Variant 3 but without the expiry and re-creation step, so in practice its interim behaviour is weaker than Variant 3's.

## Concessions

- **Memory-only rule.** Variant 3's own costs admit the rule "stays in a memory note and a ledger row ... so the next coordinator outside this program may again miss it." Variant 2 fixes this; Variant 3 does not. That is the strongest case against my variant.
- **Silent failure risk.** If the re-creation step is missed after 7 days or a resume, the check "can silently stop" (Variant 3's own costs). A ledger row is a reminder, not a guarantee.
- **Overstated claim.** Variant 3 says "only a timer-driven check sees them go idle". That is too strong: once SWEEP-RUNNABLE holds, WC-16's `/sc:sweep` report includes person-started sessions "observed from transcripts and ccsession files" (WORKER-CONTRACT.md:288). The claim is true only until the sweep is runnable, and only for idle detection by subscription.
- **Ledger write wording.** Line 579 says Q31 authorizes no "write". Variant 3's recording of the job id in the ledger is the coordinator's own local record, not an action of the check, but the text should say so to avoid a reading that it conflicts with line 579.
- **"Never messaged" tension.** WC-16 says person-started sessions "are never messaged". A `notify_when_idle` subscription with no message sends nothing to the peer (SendMessage tool description: "a pure subscription that costs that session nothing"), so I read it as compatible, but the text should state that only message-less subscriptions are used.
- **Idle-only firing (A-002).** Variant 3 does not mention that a session cron fires only while the coordinator is idle, so "about every 10 minutes" is a ceiling on frequency while the coordinator works, not a guarantee.
- **Load.** About 144 read cycles a day, rate limits unmeasured (Variant 3 marks this UNVERIFIED).

## Shared assumption responses

- **A-001 (the 2026-11-05 order is still current): QUALIFY.** No later source I found withdraws it: the memory index still lists it ("Coordinator never stops polling ... owner order 2026-11-05"). The 2026-11-09 order speaks of "automated orchestration checks", which presupposes such checks exist, so it adjusts reporting rather than cancelling the check. But memory is the lowest source tier and the note is 9 days old, which is exactly why Q31 asks the owner. The owner's answer to Q31 is itself the freshness check, so the assumption is acceptable only because the owner is being asked.
- **A-002 (a session cron fires only while the coordinator is idle): ACCEPT.** The CronCreate description says "Jobs only fire while the REPL is idle (not mid-query)". A busy coordinator delays the check. This mostly matters little: when the coordinator is busy it is already acting and reading state; when it is idle (waiting on Orca), which is when peers go unwatched, the cron fires. Variant 3 should still say it, so nobody treats "about every 10 minutes" as a guarantee.

## Per-point verdicts

| Point | Superior variant | Reason |
|---|---|---|
| S-001 | tie | All three use the same five sections. |
| S-002 | 3 | Its operational sub-list (cron, expiry, reporting, limits) is what the coordinator needs to act at W0; Variant 2's second phase is out of scope for this question. |
| C-001 | 3 | "Yes, read-only" (shared with Variant 2) follows the owner order and covers non-worker peers that WC-16 cannot see while `/sc:sweep` is not runnable. |
| C-002 | 3 | Memory plus ledger for this program matches the question's scope; Variant 2's contract change is a broader decision the question was not framed to make, though it fixes the root cause. |
| C-003 | 3 | Timer-renewed subscriptions (shared with Variant 2) are the only listed way to see non-worker peers go idle before SWEEP-RUNNABLE; Variant 1 leaves this unresolved. |
| C-004 | 3 | 10-minute reads cover IronbellyOrg/Coder as the order names and catch PR events between wakes; Variant 1 reads only at wakes and gates. |
| C-005 | 3 | Only Variant 3 gives a concrete expiry and resume procedure; Variant 1 avoids the issue by dropping the check, Variant 2 defers it. |
| C-006 | 3 | Only Variant 3 reconciles the check with the 2026-11-09 reporting order. |
| C-007 | 3 | Names the open reading as UNVERIFIED and shows it stays within the 5-minute cap either way; Variant 2's contract fix would be better long term but is not part of this answer. |
| X-001 | 3 | "In force" (shared with Variant 2) is the status that follows the owner's order; "not in force" overrides it without a newer source. |
| X-002 | 3 | Binding this program only matches "this program's coordinator" in the question. |
| X-003 | 3 | WC-16's sentence describes the `/sc:sweep` duty; probe INV-010 reads it as "not a ban on that cron", and Variant 3 follows that reading. |
| A-001 | 3 | Only Variant 3 engages the later 2026-11-09 order, which is the best evidence that automated checks are still expected; none states the freshness assumption outright. |
| A-002 | tie | None of the three states the idle-only firing limit; Variant 1 sidesteps it only by having no cron. |

## Overall

Variant 3 gives the owner a direct, in-scope "yes" that follows the standing order, handles the cron's expiry and the later reporting order, and keeps every spec limit; its real weakness is that the rule stays outside the checked-in contract, which the owner can address later with a separate decision, and its text should drop "only a timer-driven check" and state the idle-only firing and message-less subscriptions.

Overall best answer for the owner: Variant 3, confidence 70%
