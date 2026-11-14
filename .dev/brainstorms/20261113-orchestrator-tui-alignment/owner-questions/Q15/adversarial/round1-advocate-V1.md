# Round 1 advocate statement: Variant 1 (never, as a standing rule)

Persona: security (vulnerabilities, attack surface, trust boundaries). Depth: quick, Round 1 only.
Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless they start with `Q15/` (the owner-question folder). "ADJ" is `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`.

## Position summary

Variant 1 is the only answer that removes the attack surface instead of postponing or guarding it: no inbound channel into a person-started or watcher-launched session ever exists, so there is nothing to sign, audit or defend against poisoned content. It gives the same first-release behaviour as Variants 2 and 3 (report only), and adds a standing rule so that the "never messaged" boundary in the worker contract cannot be eroded by a later design without an explicit, recorded override.

## Steelman

**Variant 2 (report only for v2; wider delivery is a later, separate decision).** This is the spec's recommended answer and the default if unanswered ("Report only (advisory)", "PLAN INFERENCE: report only", `merged-requirements.md:542`, re-read). It matches ADJ's Q15 row exactly ("Report only (advisory); no delivery to non-worker sessions", ADJ line 785, re-read). Its security posture for v2 is identical to Variant 1: no new channel, no signing scheme, trust layer off v2's path (`Q15/adversarial/variant-2-original.md` lines 12 and 16). It also refuses to decide the long-term question before anyone has researched it, which is good scope discipline: the question asks about v2, and Variant 2 answers about v2.

**Variant 3 (yes, eventually, behind the #339 trust layer).** It keeps #423's stated purpose, "relay them to affected agents" (D-8, `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/round2-rebuttal-V4.md:68`, re-read), and names the real operational gap: watcher-launched sessions may run unattended, and a report that nobody reads corrects nothing (`variant-3-original.md` line 17). It is not reckless: the first release still reports only, delivery waits for the trust layer, and it correctly links that choice to ADJ line 699 (trust decisions become prerequisites if v2 relays to agents, re-read) and to Q16. It gives the trust-layer work a concrete consumer instead of designing it in the abstract.

## Strengths claimed

1. **Smallest attack surface, by elimination rather than mitigation.** ADJ line 295 (re-read) records that "signing does not stop poisoned content (#339 comment 2: 'encryption alone is not enough')". Any delivery channel into a person-started session puts model-readable text into a session that runs with that person's permissions and tools. Variant 1 is the only option under which that threat never has to be modelled, because the channel is never built (`variant-1-original.md` line 17: "no new inbound channel into a person's own session exists to defend, sign or audit").
2. **Matches the contract boundary as written.** `src/superclaude/core/WORKER-CONTRACT.md:288` (re-read 2026-11-14): "Person-started sessions appear in the report, observed from transcripts and ccsession files; they are never messaged." Variant 1 turns that existing sentence into a v2 rule instead of a v2 limit that a later release could relax quietly.
3. **Keeps the one sanctioned worker path narrow.** Workers are reached only through WC-12, which is pulled by the worker and acknowledged per message as `applied|queued|refused` (`WORKER-CONTRACT.md:61`, re-read). The worker controls when it reads; the coordinator is the only sender; WC-13 (`WORKER-CONTRACT.md:62`) forbids fan-out. Relay also passes through the coordinator (ADJ line 715). Variant 1 adds nothing to this path.
4. **Keeps the trust layer off v2's path permanently.** ADJ line 699 makes the #339 trust decisions v2 prerequisites only if v2 relays to agents. Under Variant 1 that condition can never become true, so the Q14 gate stays as ADJ line 294 recommends, and SW-12 Phase 4 (`merged-requirements.md:201`, re-read) stays a v1 orchestrator concern.
5. **Prevents boundary erosion.** A security boundary stated only as "first release" invites a later design to treat it as a placeholder. Variant 1 requires an explicit owner decision that overrides a recorded rule (`variant-1-original.md` line 22), which forces the reasoning for any new channel to be written down. It does not make reopening impossible.
6. **Does not authorize a contract edit.** Copying the rule next to `WORKER-CONTRACT.md:288` is left to a later, separately approved PR (`variant-1-original.md` line 12), so the answer itself has no write side effect.

## Weaknesses identified in others

**Variant 2.**
- "Any wider delivery would be a later, separate owner decision" (`variant-2-original.md` line 5) states no conditions for reopening. A future design (for example the orchestrator of orchestrators that `.dev/issues/339/issue-summary.md` line 6 lists under version 2) can reopen it without first naming a channel, a threat model or an approval rule. The security boundary therefore holds only as long as nobody asks.
- It "narrows" #423's relay goal for non-workers (`variant-2-original.md` line 22) but leaves the goal text alive, so #423 keeps a stated aim that the contract (`WORKER-CONTRACT.md:288`) forbids.

**Variant 3.**
- It commits v2 to a new inbound channel into sessions the contract says are "never messaged" (`variant-3-original.md` line 22 concedes this). That is a reversal of an existing trust boundary, decided before any threat model exists.
- No channel exists today (question.md fact 10; whether Orca has a terminal-input verb that could serve is UNVERIFIED). Planning delivery "now" (`variant-3-original.md` line 5) designs for an unknown mechanism, which is exactly the situation in which injection paths get built by accident (for example, typing into a terminal).
- Its own unresolved list includes "Whether a person must approve each delivered correction" (`variant-3-original.md` line 29). That is the central security control, and it is left open while the goal is fixed.
- Signing does not solve the core risk (ADJ line 295), so even a complete trust layer leaves poisoned content in typed fields or `detail` as residual risk; ADJ line 705 already requires `detail` to be "never acted on", which is hard to guarantee inside a free-running person session.
- It moves SW-12 Phase 4 and Q16 onto v2's path (`variant-3-original.md` line 11), lengthening a path whose first release does not need them.

## Concessions

- **Scope.** Variant 1 rules on "v2 (and any later automated program)" (`variant-1-original.md` line 5). The question asks only about v2. Binding later programs goes beyond the question, and the orchestrator of orchestrators has not been researched; Variant 2 is better on scope discipline.
- **No first-release security gain over Variant 2.** For the release actually being designed, Variants 1 and 2 behave identically (diff C-002). Variant 1's added value is only about the future, and a standing rule is a policy, not a mechanism: an owner can override it, so its protective force is partly procedural.
- **Unattended sessions.** Watcher-launched sessions can never be corrected automatically under Variant 1 (`variant-1-original.md` line 23). If reports are not read quickly (A-002), a stuck unattended session keeps going. Variant 3 names this gap honestly (U-003).
- **Departs from the default.** Variant 2 is the spec's recommendation and the default if unanswered (`merged-requirements.md:542`); Variant 1 needs an active owner decision.
- **Citation note.** question.md fact 5 places ADJ's "The first release delivers to the person or the coordinator only" at ADJ line 707; on re-read that sentence is at ADJ line 705, and line 707 is the "## Acceptance Criteria" heading. The per-class sentence is correctly at line 714.

## Shared assumptions

| ID | Response | Reason |
|----|----------|--------|
| A-001 | QUALIFY | WC-12 is acceptable because the worker pulls, the coordinator is the only sender and each message is acknowledged `applied|queued|refused` (`WORKER-CONTRACT.md:61`), but v2 content on that path must still arrive as typed data with `detail` never acted on (ADJ lines 705 and 715), and no answer states that as an explicit v2 permission. |
| A-002 | QUALIFY | A person acting in reasonable time is not guaranteed for unattended watcher-launched sessions; it is the honest cost of Variants 1 and 2 and should be recorded as a known gap, not assumed. |

## Per-point verdicts

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

## Overall ranking and unassigned pick

Ranking (best first): Variant 1, Variant 2, Variant 3.

If I were not assigned a variant, I would pick Variant 2. For the release being designed its security posture is identical to Variant 1, it is the spec's default and ADJ's recommendation, and it answers only the question asked instead of binding unresearched future programs. I would strengthen it with one element from Variant 1: any later reopening must first name the delivery channel, a threat model for poisoned content and whether a person approves each delivered correction, before the decision is taken. Variant 3 ranks last on security grounds because it commits to reversing an existing trust boundary before any channel or approval control is known.
