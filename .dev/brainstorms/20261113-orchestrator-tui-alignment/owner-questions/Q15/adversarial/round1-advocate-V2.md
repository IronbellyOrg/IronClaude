# Round 1 advocate statement: Variant 2 (report only for v2; wider delivery is a later, separate decision)

Advocate persona: architect (structure, dependencies, long-term impact). Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless they start with F (the Q15 folder). "ADJ" means `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`; "MR" means `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`. All line citations below were re-read on 2026-11-14 unless marked UNVERIFIED or attributed to question.md.

## Position summary

Variant 2 answers the decision the plan actually needs now (what v2 does) with the already-adjudicated text, keeps v2 free of any dependency on unbuilt trust work, and leaves the irreversible "never" or "yes" call to a later owner decision that will have evidence the owner does not have today. It is the cheapest answer to reverse in either direction, and it is the one every existing source already agrees with.

## Steelman

**Variant 1 (never, as a standing rule).** The strongest case for Variant 1 is that boundaries that are "open for later" tend to erode one feature at a time, and a security boundary is cheapest to defend when it is absolute. Today the contract already says person-started sessions "are never messaged" (`src/superclaude/core/WORKER-CONTRACT.md:288`), no inbound channel into a non-worker session is known to exist (F/question.md fact 10), and signing does not stop poisoned content ("encryption alone is not enough", ADJ line 295). A standing rule removes a whole attack surface for good, means nothing ever has to be signed, audited or defended on that path, and gives every future designer one clear sentence to build against. Variant 1 also answers the literal question ("Must v2 ever...") directly, where Variant 2 answers "not now".

**Variant 3 (yes eventually, behind the #339 trust layer).** The strongest case for Variant 3 is fidelity to purpose: #423's current acceptance criteria ask v2 to "relay them to affected agents" (`.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/round2-rebuttal-V4.md:68`, D-8), and a knowledge layer that can only write reports leaves the sessions most in need of correction, unattended watcher-launched ones, waiting on a person (F/adversarial/variant-3-original.md:17). Planning the delivery path in the design now, while the first release still reports only, avoids a second redesign later, and it gives the #339 trust layer (comment 2's signed narrow grants, `.dev/issues/339/issue-summary.md:10`) a concrete consumer, which is a real input to designing that layer well.

## Strengths claimed

1. **It is the adjudicated answer and the stated default, so it creates no new conflicts.** MR:542 records "Report only (advisory)" as the recommended answer and "PLAN INFERENCE: report only" as the default. ADJ line 785 gives "Report only (advisory); no delivery to non-worker sessions". ADJ line 714 already supplies the per-class acceptance text Variant 2 adopts verbatim: "a coordinator follow-up (WC-12) for workers, a report to the person for the rest". Variant 2 changes nothing that V2-01 (MR:398) or V2-03 (MR:400) has to rewrite; Variants 1 and 3 each require new #423 text beyond ADJ's proposal (variant-1-original.md:10, "now or later"; variant-3-original.md:10, the delivery clause).

2. **It keeps v2's dependency graph short and free of unbuilt prerequisites.** ADJ line 699 says the other #339 phases, including the trust layer, "are not prerequisites, unless the brainstorm decides that v2 relays to agents and not only to the person; then the trust decisions in #339 are." MR:401 (V2-04) lists "SW-12 (only if Q14 says v2 relays to agents)" as a conditional dependency. Variant 2 resolves that condition to false for v2, so SW-12 and Q16 stay off v2's critical path (variant-2-original.md:12). Variant 3 resolves it to true and pulls SW-12 and Q16 in front of the delivery release (variant-3-original.md:11). From an architecture view, coupling one planned, unbuilt layer (v2) to a second unbuilt layer (the trust layer), whose threat model ADJ line 295 says differs from the other consumers', is the larger structural risk.

3. **It matches the contract as written, with no edit needed.** Workers pull follow-ups (WC-12, `WORKER-CONTRACT.md:61`); a worker never fans out (WC-13, line 62); person-started sessions "are never messaged" (line 288). Variant 2 needs no contract change now or later to stay consistent. Variant 3 introduces a channel into sessions the contract says are never messaged.

4. **It respects the advisory split.** `/sc:sweep` "recommends nothing" (`WORKER-CONTRACT.md:288`), and v2's correction is a recommendation, so v2 is a separate command or skill (round2-rebuttal-V4.md:118; ADJ line 294). A report-only v2 keeps that split clean: the sweep observes, v2 advises, the coordinator or person acts. Delivery into a session moves v2 from advisor toward actor.

5. **It is the most reversible answer, which matters because the key fact is unknown.** No channel into a person-started or watcher-launched session is known today, and that was not searched beyond the contract (F/question.md fact 10; UNVERIFIED whether Orca has a usable terminal-input verb). Deciding "never" (Variant 1) or "yes, design it now" (Variant 3) both commit before that fact is known. Variant 2 decides only what the v2 package needs and names the open question explicitly (variant-2-original.md:28), so the later decision can be made with the channel research and the Q16 answer in hand.

6. **It scopes the decision to the question asked.** The spec row asks about v2 (MR:542). Variant 1 binds "v2 (and any later automated program)" (variant-1-original.md:5), which reaches into designs nobody has researched, such as the orchestrator of orchestrators (variant-1-original.md:24 concedes this). Variant 2 does not legislate for programs outside its scope.

## Weaknesses identified in others

**Variant 1.**
- Overreach in scope: it rules on "any later automated program", not only v2 (variant-1-original.md:5), which pre-decides part of #339's own v2 vision (ADJ line 294 lists "an orchestrator of orchestrators" as one meaning of v2) before it is researched.
- Asymmetric reversal cost: reopening needs "a new owner decision that overrides a stated standing rule" (variant-1-original.md:22). A standing rule tends to be cited as settled policy; Variant 2's open item reverses with an ordinary decision.
- Its main benefit (no trust layer on v2's path, variant-1-original.md:16) is already delivered by Variant 2 for every release actually planned (V2-04 is the first release and is deferred, MR:401). The extra "forever" buys nothing for any package in the plan.
- It forecloses, without evidence, the one case all three variants admit is unsolved: unattended watcher-launched sessions (variant-1-original.md:23).

**Variant 3.**
- It designs for a channel that does not exist and has not been searched for (F/question.md fact 10). V2-03 would have to "name the delivery channel for each non-worker class; none exists today" (variant-3-original.md:12), which is design work that may be discarded (variant-3-original.md:25 concedes this).
- It reverses the adjudicated recommendation (ADJ line 785) and the default (MR:542), and sets as a goal a channel into sessions the contract says "are never messaged" (`WORKER-CONTRACT.md:288`).
- It lengthens the critical path: SW-12 (the trust layer, unbuilt; MR:201 per F/question.md fact 7, not re-read) and Q16 move in front of the delivery release (variant-3-original.md:11), and the Q14 gate widens (diff-analysis C-005).
- Its near-term behaviour is identical to Variant 2 (first release reports only, variant-3-original.md:5), so its extra cost now buys only a planning commitment, not a capability.
- Its own unresolved item, "Whether a person must approve each delivered correction" (variant-3-original.md:29), suggests the safe form of delivery may collapse back into "report to a person", which is Variant 2.

## Concessions

- Variant 2 does not answer the literal word "ever". It answers "not in v2 as decided" and defers the rest (variant-2-original.md:5, 24). An owner who wants this question closed permanently gets less from Variant 2 than from Variant 1.
- "Later, separate decision" can become a standing invitation to reopen (variant-2-original.md:24); without a trigger condition it may be re-argued in every v2 design pass. A fair improvement would be to name the trigger, for example "reopen only when a channel is found and Q16 is answered".
- Variant 2, like the others, leaves unattended watcher-launched sessions without automatic correction (variant-2-original.md:23). Variant 3 is the only variant that offers a path for them.
- Variant 2 gives the #339 trust layer no concrete consumer, which Variant 3 does (diff-analysis U-002). Trust-layer design may be weaker for lack of one.
- Variant 1's idea of writing the rule beside the contract sentence (variant-1-original.md:12, U-001) makes the boundary more visible than Variant 2 does. Variant 2 could adopt a narrower version of it ("v2 does not message non-worker sessions") but does not propose it.

## Shared assumptions

- **A-001 (corrections to workers through WC-12 pulled follow-ups are acceptable for v2): QUALIFY.** Acceptable only if v2 hands its correction to the coordinator, which decides whether to send a follow-up; v2 itself never sends one, because relay "passes through the coordinator" (ADJ line 715) and WC-12 describes coordinator messages (`WORKER-CONTRACT.md:61`), not v2 messages.
- **A-002 (a person reads and acts on v2's reports in reasonable time): QUALIFY.** It holds for person-started sessions, where a person is present by definition, but not for unattended watcher-launched sessions; all three variants list this as a cost or unresolved (variant-1-original.md:28, variant-2-original.md:23), and V2-03 should state a check for it rather than assume it.

## Per-point verdicts

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | tie | 95% | All three use the same five sections. |
| C-001 | 2 | 65% | An open direction is the only choice that does not commit before the channel fact (question.md fact 10) is known. |
| C-002 | tie | 95% | All three make the first release report only. |
| C-003 | 2 | 60% | Keeps the trust layer off v2's path like Variant 1, without forbidding a future consumer the trust work might want. |
| C-004 | 2 | 70% | Uses ADJ's already-proposed #423 text (ADJ lines 707, 714); no new wording to review. |
| C-005 | tie (1 and 2) | 70% | Neither touches Q14 or Q16 now; Variant 3 widens Q14 and puts Q16 first. |
| X-001 | 2 | 55% | "Undecided" fits the evidence; "No" is also defensible given "never messaged" (`WORKER-CONTRACT.md:288`). |
| X-002 | 2 | 65% | A v2 answer should not bind unresearched designs such as the orchestrator of orchestrators (ADJ line 294). |
| X-003 | tie (1 and 2) | 75% | Designing a delivery path with no known channel risks wasted work, which Variant 3 itself concedes. |
| U-001 | 1 | 55% | Writing the rule beside the contract sentence makes the boundary visible; Variant 2 could adopt a narrower form. |
| U-002 | 2 | 55% | Variant 2 records the Q16 link (variant-2-original.md:28) without making it a gate; Variant 3's concrete consumer is real but premature. |
| U-003 | 3 | 60% | Variant 3 is the only one to name the unattended watcher-launched case as the strongest reason for delivery. |

## Overall ranking and unassigned pick

Ranking, best first: **Variant 2, Variant 1, Variant 3.**

Variant 2 is the adjudicated answer, the plan default and the contract-consistent choice, and it is the cheapest to reverse in either direction. Variant 1 gives the same v2 behaviour with a firmer boundary but overreaches in scope and is costlier to reverse. Variant 3 matches #423's original intent but commits design work and critical-path dependencies to a channel that is not known to exist.

Unassigned pick: I would still pick Variant 2, with one change borrowed from the concessions: name the trigger for reopening (a channel found and Q16 answered). If the owner's priority is a fixed security boundary over flexibility, Variant 1 is a close second and a reasonable choice.
