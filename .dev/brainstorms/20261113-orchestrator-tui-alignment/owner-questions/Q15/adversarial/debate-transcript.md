# Adversarial Debate Transcript: Q15

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 73% (8 of 11 scored points, on assigned positions)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, spawned general-purpose sub-agents (Variant 1 persona security, Variant 2 persona architect, Variant 3 persona backend). No failures.
- Protocol: sc-adversarial-protocol, loaded by Skill call at Q11 in this session and applied as written.
- Variant map: Variant 1 = proposal-A (never, standing rule); Variant 2 = proposal-B (report only; wider delivery a later separate decision); Variant 3 = proposal-C (yes eventually, behind the #339 trust layer)
- Citation correction: Advocate V1 found that ADJ's sentence "The first release delivers to the person or the coordinator only" is at line 705, not 707. Confirmed by grep. question.md and proposal-B.md were corrected after the debate; the variant copies keep the original citation as debated.

## Unassigned picks
- Advocate V1: Variant 2, plus: any reopening must first name the delivery channel, a threat model for poisoned content, and whether a person approves each correction.
- Advocate V2: Variant 2, plus a named reopening trigger (a channel found and Q16 answered).
- Advocate V3: Variant 2, plus: name unattended watcher-launched sessions as the open case, and design the typed fields and audit record so a later delivery release needs no store migration.
- Result: 3 of 3 pick Variant 2.

## Scoring Matrix

| Diff Point | Level | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie (agreed) | 95% | Same sections. |
| C-001 | L3 | 1 | 2 | 3 | unresolved (split) | 50% | Each backed its own long-term direction; all unassigned picks are Variant 2. |
| C-002 | L1 | tie | tie | tie | tie (agreed) | 95% | All report only in the first release. |
| C-003 | L3 | 1 | 2 | 2 | Variant 2 | 68% | Trust layer off v2's path without forbidding a future consumer. |
| C-004 | L2 | 1 | 2 | 3 | unresolved (split) | 50% | Remove, narrow or keep #423's relay goal: each backed its own. |
| C-005 | L2 | 1,2 | 1,2 | 3 | Variants 1 and 2 | 70% | Neither widens the Q14 gate nor forces Q16 first. |
| X-001 | L3 | 1 | 2 | 3 | unresolved (split) | 50% | Split on assigned positions. |
| X-002 | L2 | 2 | 2 | 2 | Variant 2 | 88% | Unanimous: a v2 answer should not bind unresearched future designs. |
| X-003 | L2 | 1,2 | 1,2 | 3 | Variants 1 and 2 | 72% | No known channel; designing delivery now risks waste. |
| A-001 | L3 | QUALIFY | QUALIFY | ACCEPT | agreed: QUALIFY | 70% | WC-12 is acceptable only with v2 handing corrections to the coordinator, which decides; v2 never sends. |
| A-002 | L2 | QUALIFY | QUALIFY | QUALIFY | agreed: QUALIFY | 90% | Holds for person-started sessions, not for unattended watcher-launched ones. |
| U-001 | n/a | 1 | 1 | 1 | Variant 1 (valid) | 60% | Rule beside the contract's "never messaged" sentence, by a separate approved PR. |
| U-002 | n/a | 3 | 2 | 3 | Variant 3 (valid) | 60% | A named consumer sharpens the trust-layer threat model and Q16. |
| U-003 | n/a | 3 | 3 | 3 | Variant 3 (valid) | 65% | Unattended watcher-launched sessions are the real gap. |

Resolved points: S-001, C-002, C-003, C-005, X-002, X-003, A-001, A-002 (8 of 11).

## Convergence Assessment
- Points resolved: 8 of 11
- Alignment: 73%
- Threshold: 80%
- Taxonomy coverage: L1 2, L2 5, L3 4; all covered
- Invariant gate: not applied (quick)
- Status: NOT_CONVERGED on assigned positions (max rounds reached at depth quick); force-selected by score per the skill's no-convergence rule. Every unassigned pick (3 of 3) names Variant 2, so the overall choice is not split.
- Unresolved points: C-001, C-004, X-001

## Round 1: Advocate Statements

The three statements follow verbatim.


---

### Round 1 advocate statement: Variant 1 (never, as a standing rule)

Persona: security (vulnerabilities, attack surface, trust boundaries). Depth: quick, Round 1 only.
Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless they start with `Q15/` (the owner-question folder). "ADJ" is `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`.

#### Position summary

Variant 1 is the only answer that removes the attack surface instead of postponing or guarding it: no inbound channel into a person-started or watcher-launched session ever exists, so there is nothing to sign, audit or defend against poisoned content. It gives the same first-release behaviour as Variants 2 and 3 (report only), and adds a standing rule so that the "never messaged" boundary in the worker contract cannot be eroded by a later design without an explicit, recorded override.

#### Steelman

**Variant 2 (report only for v2; wider delivery is a later, separate decision).** This is the spec's recommended answer and the default if unanswered ("Report only (advisory)", "PLAN INFERENCE: report only", `merged-requirements.md:542`, re-read). It matches ADJ's Q15 row exactly ("Report only (advisory); no delivery to non-worker sessions", ADJ line 785, re-read). Its security posture for v2 is identical to Variant 1: no new channel, no signing scheme, trust layer off v2's path (`Q15/adversarial/variant-2-original.md` lines 12 and 16). It also refuses to decide the long-term question before anyone has researched it, which is good scope discipline: the question asks about v2, and Variant 2 answers about v2.

**Variant 3 (yes, eventually, behind the #339 trust layer).** It keeps #423's stated purpose, "relay them to affected agents" (D-8, `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/round2-rebuttal-V4.md:68`, re-read), and names the real operational gap: watcher-launched sessions may run unattended, and a report that nobody reads corrects nothing (`variant-3-original.md` line 17). It is not reckless: the first release still reports only, delivery waits for the trust layer, and it correctly links that choice to ADJ line 699 (trust decisions become prerequisites if v2 relays to agents, re-read) and to Q16. It gives the trust-layer work a concrete consumer instead of designing it in the abstract.

#### Strengths claimed

1. **Smallest attack surface, by elimination rather than mitigation.** ADJ line 295 (re-read) records that "signing does not stop poisoned content (#339 comment 2: 'encryption alone is not enough')". Any delivery channel into a person-started session puts model-readable text into a session that runs with that person's permissions and tools. Variant 1 is the only option under which that threat never has to be modelled, because the channel is never built (`variant-1-original.md` line 17: "no new inbound channel into a person's own session exists to defend, sign or audit").
2. **Matches the contract boundary as written.** `src/superclaude/core/WORKER-CONTRACT.md:288` (re-read 2026-11-14): "Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged." Variant 1 turns that existing sentence into a v2 rule instead of a v2 limit that a later release could relax quietly.
3. **Keeps the one sanctioned worker path narrow.** Workers are reached only through WC-12, which is pulled by the worker and acknowledged per message as `applied|queued|refused` (`WORKER-CONTRACT.md:61`, re-read). The worker controls when it reads; the coordinator is the only sender; WC-13 (`WORKER-CONTRACT.md:62`) forbids fan-out. Relay also passes through the coordinator (ADJ line 715). Variant 1 adds nothing to this path.
4. **Keeps the trust layer off v2's path permanently.** ADJ line 699 makes the #339 trust decisions v2 prerequisites only if v2 relays to agents. Under Variant 1 that condition can never become true, so the Q14 gate stays as ADJ line 294 recommends, and SW-12 Phase 4 (`merged-requirements.md:201`, re-read) stays a v1 orchestrator concern.
5. **Prevents boundary erosion.** A security boundary stated only as "first release" invites a later design to treat it as a placeholder. Variant 1 requires an explicit owner decision that overrides a recorded rule (`variant-1-original.md` line 22), which forces the reasoning for any new channel to be written down. It does not make reopening impossible.
6. **Does not authorize a contract edit.** Copying the rule next to `WORKER-CONTRACT.md:288` is left to a later, separately approved PR (`variant-1-original.md` line 12), so the answer itself has no write side effect.

#### Weaknesses identified in others

**Variant 2.**
- "Any wider delivery would be a later, separate owner decision" (`variant-2-original.md` line 5) states no conditions for reopening. A future design (for example the orchestrator of orchestrators that `.dev/issues/339/issue-summary.md` line 6 lists under version 2) can reopen it without first naming a channel, a threat model or an approval rule. The security boundary therefore holds only as long as nobody asks.
- It "narrows" #423's relay goal for non-workers (`variant-2-original.md` line 22) but leaves the goal text alive, so #423 keeps a stated aim that the contract (`WORKER-CONTRACT.md:288`) forbids.

**Variant 3.**
- It commits v2 to a new inbound channel into sessions the contract says are "never messaged" (`variant-3-original.md` line 22 concedes this). That is a reversal of an existing trust boundary, decided before any threat model exists.
- No channel exists today (question.md fact 10; whether Orca has a terminal-input verb that could serve is UNVERIFIED). Planning delivery "now" (`variant-3-original.md` line 5) designs for an unknown mechanism, which is exactly the situation in which injection paths get built by accident (for example, typing into a terminal).
- Its own unresolved list includes "Whether a person must approve each delivered correction" (`variant-3-original.md` line 29). That is the central security control, and it is left open while the goal is fixed.
- Signing does not solve the core risk (ADJ line 295), so even a complete trust layer leaves poisoned content in typed fields or `detail` as residual risk; ADJ line 705 already requires `detail` to be "never acted on", which is hard to guarantee inside a free-running person session.
- It moves SW-12 Phase 4 and Q16 onto v2's path (`variant-3-original.md` line 11), lengthening a path whose first release does not need them.

#### Concessions

- **Scope.** Variant 1 rules on "v2 (and any later automated program)" (`variant-1-original.md` line 5). The question asks only about v2. Binding later programs goes beyond the question, and the orchestrator of orchestrators has not been researched; Variant 2 is better on scope discipline.
- **No first-release security gain over Variant 2.** For the release actually being designed, Variants 1 and 2 behave identically (diff C-002). Variant 1's added value is only about the future, and a standing rule is a policy, not a mechanism: an owner can override it, so its protective force is partly procedural.
- **Unattended sessions.** Watcher-launched sessions can never be corrected automatically under Variant 1 (`variant-1-original.md` line 23). If reports are not read quickly (A-002), a stuck unattended session keeps going. Variant 3 names this gap honestly (U-003).
- **Departs from the default.** Variant 2 is the spec's recommendation and the default if unanswered (`merged-requirements.md:542`); Variant 1 needs an active owner decision.
- **Citation note.** question.md fact 5 places ADJ's "The first release delivers to the person or the coordinator only" at ADJ line 707; on re-read that sentence is at ADJ line 705, and line 707 is the "## Acceptance Criteria" heading. The per-class sentence is correctly at line 714.

#### Shared assumptions

| ID | Response | Reason |
|----|----------|--------|
| A-001 | QUALIFY | WC-12 is acceptable because the worker pulls, the coordinator is the only sender and each message is acknowledged `applied|queued|refused` (`WORKER-CONTRACT.md:61`), but v2 content on that path must still arrive as typed data with `detail` never acted on (ADJ lines 705 and 715), and no answer states that as an explicit v2 permission. |
| A-002 | QUALIFY | A person acting in reasonable time is not guaranteed for unattended watcher-launched sessions; it is the honest cost of Variants 1 and 2 and should be recorded as a known gap, not assumed. |

#### Per-point verdicts

| Point | Winner | Confidence | Reason |
|-------|--------|------------|--------|
| S-001 | tie | 95% | All three use the same five sections. |
| C-001 | 1 | 55% | "Never" removes the attack surface for good; Variant 2 is close because it also blocks delivery for v2, only without binding the future. |
| C-002 | tie | 95% | All three report only in the first release. |
| C-003 | 1 | 55% | Variant 1 keeps the trust layer off v2's path permanently; Variant 2 does so for v2 as decided; Variant 3 puts it on the path. |
| C-004 | 1 | 55% | Removing "relay them to affected agents" aligns #423 with `WORKER-CONTRACT.md:288`; narrowing (Variant 2) leaves a goal the contract forbids. |
| C-005 | tie (1 and 2) | 75% | Neither widens Q14 or forces Q16 first; Variant 3 adds prerequisites for an unknown channel. |
| X-001 | 1 | 60% | A channel that never exists cannot be poisoned; "undecided" and "yes, guarded" both leave a future injection path. |
| X-002 | 2 | 55% | Concession: binding unresearched future designs is beyond the question's scope; Variant 2 answers only for v2. |
| X-003 | tie (1 and 2) | 75% | No channel is known (question.md fact 10), so designing delivery now is likely waste and risks an accidental injection path. |
| U-001 | 1 | 60% | Writing the rule beside the "never messaged" sentence, by a separate approved PR, makes the boundary visible without an unapproved edit. |
| U-002 | 3 | 55% | Naming Q16 and the trust layer as prerequisites is useful input to any later reopening, whichever variant is chosen now. |
| U-003 | 3 | 60% | Unattended watcher-launched sessions are the real gap that Variants 1 and 2 leave to the person. |

#### Overall ranking and unassigned pick

Ranking (best first): Variant 1, Variant 2, Variant 3.

If I were not assigned a variant, I would pick Variant 2. For the release being designed its security posture is identical to Variant 1, it is the spec's default and ADJ's recommendation, and it answers only the question asked instead of binding unresearched future programs. I would strengthen it with one element from Variant 1: any later reopening must first name the delivery channel, a threat model for poisoned content and whether a person approves each delivered correction, before the decision is taken. Variant 3 ranks last on security grounds because it commits to reversing an existing trust boundary before any channel or approval control is known.

---

### Round 1 advocate statement: Variant 2 (report only for v2; wider delivery is a later, separate decision)

Advocate persona: architect (structure, dependencies, long-term impact). Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless they start with F (the Q15 folder). "ADJ" means `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`; "MR" means `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`. All line citations below were re-read on 2026-11-14 unless marked UNVERIFIED or attributed to question.md.

#### Position summary

Variant 2 answers the decision the plan actually needs now (what v2 does) with the already-adjudicated text, keeps v2 free of any dependency on unbuilt trust work, and leaves the irreversible "never" or "yes" call to a later owner decision that will have evidence the owner does not have today. It is the cheapest answer to reverse in either direction, and it is the one every existing source already agrees with.

#### Steelman

**Variant 1 (never, as a standing rule).** The strongest case for Variant 1 is that boundaries that are "open for later" tend to erode one feature at a time, and a security boundary is cheapest to defend when it is absolute. Today the contract already says person-started sessions "are never messaged" (`src/superclaude/core/WORKER-CONTRACT.md:288`), no inbound channel into a non-worker session is known to exist (F/question.md fact 10), and signing does not stop poisoned content ("encryption alone is not enough", ADJ line 295). A standing rule removes a whole attack surface for good, means nothing ever has to be signed, audited or defended on that path, and gives every future designer one clear sentence to build against. Variant 1 also answers the literal question ("Must v2 ever...") directly, where Variant 2 answers "not now".

**Variant 3 (yes eventually, behind the #339 trust layer).** The strongest case for Variant 3 is fidelity to purpose: #423's current acceptance criteria ask v2 to "relay them to affected agents" (`.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/round2-rebuttal-V4.md:68`, D-8), and a knowledge layer that can only write reports leaves the sessions most in need of correction, unattended watcher-launched ones, waiting on a person (F/adversarial/variant-3-original.md:17). Planning the delivery path in the design now, while the first release still reports only, avoids a second redesign later, and it gives the #339 trust layer (comment 2's signed narrow grants, `.dev/issues/339/issue-summary.md:10`) a concrete consumer, which is a real input to designing that layer well.

#### Strengths claimed

1. **It is the adjudicated answer and the stated default, so it creates no new conflicts.** MR:542 records "Report only (advisory)" as the recommended answer and "PLAN INFERENCE: report only" as the default. ADJ line 785 gives "Report only (advisory); no delivery to non-worker sessions". ADJ line 714 already supplies the per-class acceptance text Variant 2 adopts verbatim: "a coordinator follow-up (WC-12) for workers, a report to the person for the rest". Variant 2 changes nothing that V2-01 (MR:398) or V2-03 (MR:400) has to rewrite; Variants 1 and 3 each require new #423 text beyond ADJ's proposal (variant-1-original.md:10, "now or later"; variant-3-original.md:10, the delivery clause).

2. **It keeps v2's dependency graph short and free of unbuilt prerequisites.** ADJ line 699 says the other #339 phases, including the trust layer, "are not prerequisites, unless the brainstorm decides that v2 relays to agents and not only to the person; then the trust decisions in #339 are." MR:401 (V2-04) lists "SW-12 (only if Q14 says v2 relays to agents)" as a conditional dependency. Variant 2 resolves that condition to false for v2, so SW-12 and Q16 stay off v2's critical path (variant-2-original.md:12). Variant 3 resolves it to true and pulls SW-12 and Q16 in front of the delivery release (variant-3-original.md:11). From an architecture view, coupling one planned, unbuilt layer (v2) to a second unbuilt layer (the trust layer), whose threat model ADJ line 295 says differs from the other consumers', is the larger structural risk.

3. **It matches the contract as written, with no edit needed.** Workers pull follow-ups (WC-12, `WORKER-CONTRACT.md:61`); a worker never fans out (WC-13, line 62); person-started sessions "are never messaged" (line 288). Variant 2 needs no contract change now or later to stay consistent. Variant 3 introduces a channel into sessions the contract says are never messaged.

4. **It respects the advisory split.** `/sc:sweep` "recommends nothing" (`WORKER-CONTRACT.md:288`), and v2's correction is a recommendation, so v2 is a separate command or skill (round2-rebuttal-V4.md:118; ADJ line 294). A report-only v2 keeps that split clean: the sweep observes, v2 advises, the coordinator or person acts. Delivery into a session moves v2 from advisor toward actor.

5. **It is the most reversible answer, which matters because the key fact is unknown.** No channel into a person-started or watcher-launched session is known today, and that was not searched beyond the contract (F/question.md fact 10; UNVERIFIED whether Orca has a usable terminal-input verb). Deciding "never" (Variant 1) or "yes, design it now" (Variant 3) both commit before that fact is known. Variant 2 decides only what the v2 package needs and names the open question explicitly (variant-2-original.md:28), so the later decision can be made with the channel research and the Q16 answer in hand.

6. **It scopes the decision to the question asked.** The spec row asks about v2 (MR:542). Variant 1 binds "v2 (and any later automated program)" (variant-1-original.md:5), which reaches into designs nobody has researched, such as the orchestrator of orchestrators (variant-1-original.md:24 concedes this). Variant 2 does not legislate for programs outside its scope.

#### Weaknesses identified in others

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

#### Concessions

- Variant 2 does not answer the literal word "ever". It answers "not in v2 as decided" and defers the rest (variant-2-original.md:5, 24). An owner who wants this question closed permanently gets less from Variant 2 than from Variant 1.
- "Later, separate decision" can become a standing invitation to reopen (variant-2-original.md:24); without a trigger condition it may be re-argued in every v2 design pass. A fair improvement would be to name the trigger, for example "reopen only when a channel is found and Q16 is answered".
- Variant 2, like the others, leaves unattended watcher-launched sessions without automatic correction (variant-2-original.md:23). Variant 3 is the only variant that offers a path for them.
- Variant 2 gives the #339 trust layer no concrete consumer, which Variant 3 does (diff-analysis U-002). Trust-layer design may be weaker for lack of one.
- Variant 1's idea of writing the rule beside the contract sentence (variant-1-original.md:12, U-001) makes the boundary more visible than Variant 2 does. Variant 2 could adopt a narrower version of it ("v2 does not message non-worker sessions") but does not propose it.

#### Shared assumptions

- **A-001 (corrections to workers through WC-12 pulled follow-ups are acceptable for v2): QUALIFY.** Acceptable only if v2 hands its correction to the coordinator, which decides whether to send a follow-up; v2 itself never sends one, because relay "passes through the coordinator" (ADJ line 715) and WC-12 describes coordinator messages (`WORKER-CONTRACT.md:61`), not v2 messages.
- **A-002 (a person reads and acts on v2's reports in reasonable time): QUALIFY.** It holds for person-started sessions, where a person is present by definition, but not for unattended watcher-launched sessions; all three variants list this as a cost or unresolved (variant-1-original.md:28, variant-2-original.md:23), and V2-03 should state a check for it rather than assume it.

#### Per-point verdicts

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

#### Overall ranking and unassigned pick

Ranking, best first: **Variant 2, Variant 1, Variant 3.**

Variant 2 is the adjudicated answer, the plan default and the contract-consistent choice, and it is the cheapest to reverse in either direction. Variant 1 gives the same v2 behaviour with a firmer boundary but overreaches in scope and is costlier to reverse. Variant 3 matches #423's original intent but commits design work and critical-path dependencies to a channel that is not known to exist.

Unassigned pick: I would still pick Variant 2, with one change borrowed from the concessions: name the trigger for reopening (a channel found and Q16 answered). If the owner's priority is a fixed security boundary over flexibility, Variant 1 is a close second and a reasonable choice.

---

### Round 1 advocate statement: Variant 3 (yes eventually, behind the #339 trust layer)

Advocate: V3. Persona: backend (data integrity, fault tolerance, operational reality). Depth: quick, Round 1.
Paths below are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless they start with `F/` (the Q15 folder).

Sources re-read for this statement (2026-11-14):
- `src/superclaude/core/WORKER-CONTRACT.md:61` (WC-12), `:62` (WC-13), `:288` ("Person-started sessions ... are never messaged").
- `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md` (ADJ) lines 294 to 296, 699, 707, 714, 715, 785.
- `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md` lines 201, 398 to 401, 542.
- `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/round2-rebuttal-V4.md:68` (D-8, #423 AC "relay them to affected agents").
- `.dev/issues/339/issue-summary.md:6` and `:10`.

#### Position summary

V3 is the only answer that keeps #423's stated purpose ("relay them to affected agents", round2-rebuttal-V4.md:68) while making the first release exactly as safe as V1 and V2 (report only, F/adversarial/variant-3-original.md:5). It turns the open question into an explicit, gated plan: no delivery to a non-worker session until the #339 trust layer and the Q16 vocabulary exist, and a design that records now what that delivery would need, so the first release's data shapes do not have to be rebuilt later.

#### Steelman

**Variant 1 (never, standing rule).** The strongest case for V1 is that the safest inbound channel is the one that does not exist. The contract already says person-started sessions "are never messaged" (WORKER-CONTRACT.md:288), signing does not stop poisoned content ("encryption alone is not enough", ADJ line 295), and no delivery channel into a non-worker session is known today (F/question.md fact 10). A standing rule removes a whole attack surface permanently, keeps the trust layer off v2's path for good (ADJ line 699), and gives future designers a clear boundary instead of a recurring debate. From a data-integrity view, "no writer" is the strongest integrity guarantee there is.

**Variant 2 (report only; wider delivery a later separate decision).** The strongest case for V2 is that it decides exactly what must be decided now and nothing more. It is the spec's recommended answer and the default if unanswered (merged-requirements.md:542; ADJ line 785), it matches the contract as written (WC-12 at WORKER-CONTRACT.md:61; :288), it keeps the trust layer off v2's path (ADJ line 699), and it avoids committing design effort to a channel nobody has found. It preserves the option V1 closes without paying V3's planning cost. Under uncertainty, deferring an irreversible commitment is usually the right engineering call.

#### Strengths claimed

1. **Same first-release safety as the alternatives.** All three variants make the first release report only (diff-analysis C-002, rated Low severity). V3 states it explicitly: "the first release reports only" (variant-3-original.md:5) and V2-01 gets "first release: report to the person or the coordinator only" (variant-3-original.md:10). So V3 adds no near-term inbound channel and no near-term risk relative to V1 or V2.

2. **Honours the existing #423 acceptance criterion instead of dropping it by implication.** #423's criteria ask v2 to "relay them to affected agents" (round2-rebuttal-V4.md:68, D-8). V1 removes that goal and V2 narrows it (diff-analysis C-004). V3 keeps it as a goal with a gate (variant-3-original.md:10). Keeping a stated requirement with an explicit precondition is better record-keeping than dropping it.

3. **Uses the gate the adjudication already wrote for this exact case.** ADJ line 699 says the other #339 phases are not prerequisites "unless the brainstorm decides that v2 relays to agents and not only to the person; then the trust decisions in #339 are." ADJ line 294 says the same. V3 is the variant that exercises that clause as designed: the delivery release waits on the trust decisions and on Q16 (variant-3-original.md:11). The machinery exists in the spec; V3 connects it.

4. **Plans data shapes once (data-integrity argument).** The first release already must carry relayed knowledge as "fixed typed fields, free text only in one `detail` field that is never acted on", with relay through the coordinator (ADJ lines 707, 715). If delivery to other sessions is a stated later goal, V2-03 can design those fields, the audit record and the grant vocabulary (Q16, ADJ line 295) to serve both report and delivery from the start. Under V2, delivery is a later separate decision that may arrive after the first release's store and field set are fixed, forcing a schema change on a store ADJ already counts as "at least an eighth data store" (ADJ line 296). Designing the contract once is cheaper and less error-prone than migrating it.

5. **Covers the case that most needs correction (U-003).** Watcher-launched sessions are "an ordinary session to the sweep" (#409 decision 9, F/question.md fact 1) and may run without a person watching. Under V1 they can never be corrected automatically (variant-1-original.md:23); under V2 that stays undecided (variant-2-original.md:23 to 24). Operationally, a report nobody reads in time (see A-002) is the failure mode for exactly these sessions. V3 is the only variant that names this gap as something v2 is meant to close.

6. **Gives the trust layer a concrete consumer (U-002).** The trust layer is #339 Phase 4, deferred (SW-12, merged-requirements.md:201), proposed in #339 comment 2 (issue-summary.md:10). A security design without a named consumer tends to be built for an imagined threat model; ADJ itself notes the consumers "have different threat models" (ADJ line 295). V3 names v2 delivery as one consumer, which sharpens Q16.

7. **Puts the per-class question where ADJ's criterion already puts it.** ADJ's proposed acceptance criterion (line 714) already requires the design to state, for each session class, "how a course correction is delivered". V3 asks V2-03 to name the channel for each non-worker class (variant-3-original.md:12); that is the same question, answered honestly rather than pre-empted.

#### Weaknesses identified in others

**Variant 1.**
- It makes an irreversible standing rule from today's evidence, which ADJ itself does not ask for: ADJ's recommended answer is "Report only (advisory); no delivery to non-worker sessions" (line 785), not "never". V1 also states the rule binds "any later automated program" (variant-1-original.md:5), which is outside v2's scope.
- It constrains the orchestrator of orchestrators before research (its own cost, variant-1-original.md:24). V1 attributes that idea to "#339 comment 1"; the issue summary attributes comment 1 to "never stop polling" and cleanup ownership (issue-summary.md:10) and lists the orchestrator of orchestrators under version 2 (issue-summary.md:6). The comment-1 attribution is UNVERIFIED from the sources I read.
- Unattended watcher-launched sessions can never be corrected automatically (variant-1-original.md:23), and the only mitigation is A-002, an assumption no variant has shown to hold.
- Reopening is expensive by construction: it "needs a new owner decision that overrides a stated standing rule" (variant-1-original.md:22).

**Variant 2.**
- "Later, separate decision" leaves the long-term direction open, as V2 concedes (variant-2-original.md:24, :28). With the direction open, V2-03 has no reason to design the typed fields, audit record or grant vocabulary for a delivery case, so if the later decision is "yes", the first release's store and field set are likely to need a migration.
- It narrows #423's AC for non-workers (variant-2-original.md:22) without saying whether the purpose is abandoned or postponed; future readers of #423 cannot tell which.
- It leaves the unattended watcher-launched case with no stated path (variant-2-original.md:23).

#### Concessions

- **No channel exists.** F/question.md fact 10: no channel delivers a message into a person-started or watcher-launched session (UNVERIFIED whether Orca has a usable terminal-input verb). V3's delivery goal may prove impossible, and the design work in V2-03 could be wasted (variant-3-original.md:24).
- **As a goal it contradicts the contract's current wording.** Person-started sessions "are never messaged" (WORKER-CONTRACT.md:288). V3 plans a future change to that rule, which would need its own approved contract edit.
- **Poisoned content is the main risk and signing does not solve it** ("encryption alone is not enough", ADJ line 295). The trust layer is necessary but not sufficient; V3 does not yet say what is.
- **It lengthens v2's path.** V3 says SW-12 (`/sc:close`, resume, trust layer) moves onto v2's path for the delivery release and Q16 must be answered first (variant-3-original.md:11, :23). That wording is broader than ADJ lines 294 and 699, which name only "the trust decisions in #339"; a merge should narrow it to the trust layer. The first release is not blocked.
- **Person approval is unresolved** (variant-3-original.md:29). Without a decision on whether a person approves each delivered correction, V3's goal is under-specified.
- **It is not the default.** The spec's default if unanswered is report only (merged-requirements.md:542); picking V3 is a deliberate departure that costs owner attention.
- v2, the knowledge layer, the #339 trust layer and any orchestrator that manages work are unbuilt; V3's benefits are planning benefits only.

#### Shared assumptions

- **A-001 (WC-12 pulled follow-ups are an acceptable v2 correction route for workers): ACCEPT.** WC-12 is the contract's coordinator-to-worker route (WORKER-CONTRACT.md:61) and ADJ line 714 already names it for workers; v2 should still state it as a permission rather than inherit it silently.
- **A-002 (a person reads and acts on v2's reports in reasonable time): QUALIFY.** It plausibly holds for person-started sessions, whose person is present by definition, but not for unattended watcher-launched sessions; that gap is the main reason V3 keeps delivery as a gated goal, and no variant measures it.

#### Per-point verdicts

| Point | Winner | Confidence | One-line reason |
|---|---|---|---|
| S-001 | tie | 95% | All three use the same five sections. |
| C-001 | 3 | 55% | A gated goal keeps #423's purpose without near-term risk; V2 is a close second because "open" costs nothing now. |
| C-002 | tie | 95% | All three make the first release report only. |
| C-003 | 2 | 55% | Keeping the trust layer off v2's path is cheaper; V3 is right only for the delivery release, and its "SW-12 moves onto v2's path" is broader than ADJ line 699. |
| C-004 | 3 | 65% | Keeping the AC with an explicit gate preserves the record; removing (V1) or narrowing (V2) loses the stated purpose. |
| C-005 | 3 | 60% | V3 alone states the dependency ADJ line 699 creates (Q14 widening, Q16 first) instead of leaving it implicit. |
| X-001 | 3 | 50% | "Yes, guarded" is defensible only because the gate is explicit; with no known channel (fact 10), V2's "undecided" is nearly as good. |
| X-002 | 2 | 55% | Not binding future designs is safer under uncertainty; V1 binds against research not yet done, V3 binds toward a goal not yet shown feasible. |
| X-003 | 3 | 55% | Designing the field set and audit record once avoids a later migration; the channel itself can stay an open item. |
| U-001 | 1 | 60% | Writing the rule beside WORKER-CONTRACT.md:288 by a separate PR is a clean consistency practice whatever the answer. |
| U-002 | 3 | 70% | A named consumer sharpens the trust-layer threat model and Q16, which ADJ line 295 says differ by consumer. |
| U-003 | 3 | 70% | Unattended watcher-launched sessions are the real operational gap; only V3 names them as a target. |

#### Overall ranking and unassigned pick

Ranking as V3's advocate: **3, 2, 1.** V3 first because it keeps #423's purpose, connects ADJ line 699's existing clause, and designs data shapes once, at no added first-release risk. V2 second because it shares V3's first release and keeps the option open. V1 last because it makes a permanent rule that goes beyond ADJ's own recommendation (line 785) and forecloses the unattended-session case.

Unassigned pick, honestly: **Variant 2.** With no known delivery channel (fact 10), a contract that says "never messaged" (WORKER-CONTRACT.md:288), poisoned content unsolved by signing (ADJ line 295) and nothing built, the cheapest correct answer is V2, which is also the spec default. I would merge in two V3 elements: name unattended watcher-launched sessions as the open case for the later decision, and ask V2-03 to design the typed fields and audit record so that a later delivery release does not force a store migration.
