# Round 1 advocate statement: Variant 3 (no recurring chat report yet; park the clause)

Advocate persona: qa (edge cases, failure scenarios). Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`.

## Position summary

Variant 3 is the only answer that promises nothing the system cannot deliver today: there is no coordinator loop to print anything every 3 to 5 minutes, and the only text allowed to skip the DONE / NEXT table is the reply of an actual, person-assigned `/sc:sweep` run. Parking the clause keeps the coordinator's automated output equal to the decision ledger (section 6.7's first sentence) and defers the "which report" choice to the moment the loop and the contract note make it testable.

## Steelman

**Variant 1 (both reports, now).** Its strongest case: #339 literally asks for a static report "taking inspiration" from #409 (variant-5-original.md:221), the observer that renders #409's view is built and merged (ADJ glossary line 77), and `observe --once` writes no file, so it is the only status text that can run between sweeps without breaking NFR-001 (debate-transcript.md:904, X-004: "the only no-write static status is `observe --once`"). It is also the only variant that addresses the 3-minute end of "3 to 5 minutes", which the sweep's 5-minute cap (WORKER-CONTRACT.md:109) cannot reach. And it has the strongest support from the owner's own earlier choice: the seed brief records that "the first PR delivers only a read-only `/sc:sweep` plus the static orchestrator status report on the #409 layout" (.dev/brainstorms/20261107-073115-orchestrator-mode/seed-brief.md:17). Variant 1 is also honest about its risks (Q-1 UNVERIFIED, word-list clash, unmeasured load).

**Variant 2 (sweep summary only, until the contract note).** Its strongest case: it is the spec's recommended answer and its default (merged-requirements.md:538), it is already written into section 6.7 (merged-requirements.md:1040), and it matches V5's D2 advice word for word ("keep the sweep reply as the WC-16 output until D1 is settled; do not name `observe` in WC-16 or the skill's `allowed-tools` yet", variant-5-original.md:222). It needs zero edits anywhere, keeps one source of truth in chat while the two programs use different word lists, and the sweep reply is already the only exempt reply in the output style (pragmatic.md:22-23; sc-sweep-protocol/SKILL.md:31-43). It is the cheapest correct-looking answer.

## Strengths claimed

1. **It does not promise a cadence that nothing runs.** WC-16 is "a cap, not a schedule" (ADJ glossary line 81) and the transcript records "Phase 1 adds this duty, not a scheduler" (debate-transcript.md:625). WORKER-CONTRACT.md:109 says the sweep runs "after every wake or timeout, at most once every 5 minutes". The question itself states "The coordinator loop that would print a recurring report is unbuilt" (question.md fact 10). Variants 1 and 2 both answer "what goes in the recurring report" when there is no recurring report; Variant 3 is the only one that says so in its answer (variant-3-original.md:15).

2. **It matches the exact scope of the one exempt reply.** The sweep exception applies only when "the session is executing the loaded `sc-sweep-protocol` skill for an actual `/sc:sweep` invocation" and only to "the final successful reply of that skill" (pragmatic.md:23; SKILL.md:38, :43). It also says "There is no general exemption for coordinators, for other skills or for file output" (pragmatic.md:25). Variant 3's wording, "the sweep reply appears only when someone actually runs `/sc:sweep`" (variant-3-original.md:5), is a direct restatement of that rule. Calling that reply "the every-3-to-5-minute static report" (Variant 2) stretches a per-invocation reply into a periodic one the style does not describe.

3. **It keeps automated status equal to the owner's stated preference.** Section 6.7's first sentence limits automated status to "the decision ledger's outstanding owner decisions and held items with their reasons" (merged-requirements.md:1040, quoting SEED Batch 2 item 8). The last sentence of the same paragraph then allows an in-chat sweep summary. Variant 3 removes that internal tension; Variant 2 keeps it; Variant 1 widens it.

4. **It avoids naming a format before the word list exists.** The contract note must fix "one word list (stale, unknown, unavailable, could not determine, historical, frozen, settled, ...)" (variant-5-original.md:216). Choosing either report as the periodic chat report before that note binds the chat to one program's vocabulary. Variant 3 defers the choice until both inputs to it exist.

5. **Failure-scenario coverage is strongest.** QA view of each answer when the loop is later built:
   - Variant 1: the coordinator runs `observe --once` from its own terminal; Q-1 already failed for an unbound terminal (ADJ glossary line 87) and the coordinator-terminal case is UNVERIFIED (question.md fact 7). The chat could show an empty or wrong Run every cycle. Load with observer plus sweep plus watcher was never measured (INV-032, merged-requirements.md:502, as cited by question.md fact 8; not re-read here).
   - Variant 2: "until the note exists" has no date (variant-2-original.md:24), so the interim becomes the permanent answer by default, while the recorded answer claims a 3-to-5-minute report that the cap cannot meet at 3 minutes (variant-2-original.md:23).
   - Variant 3: no new failure path. Nothing new runs; the only risk is unmet scope, which is visible and tracked.

6. **It is cheap to reverse, and reversal is explicit.** No code, contract or skill edit (variant-3-original.md:11). The clause is tracked as a deferred row (variant-3-original.md:9), so it cannot silently drop out, which is the failure mode of Variant 2's undated trigger.

## Weaknesses identified in others

1. **Variant 1 needs edits nobody has scheduled and one the style forbids by default.** It requires WC-16 and the skill's tool list to name `observe` (variant-1-original.md:11), which is the exact step V5 D2 says not to take yet (variant-5-original.md:222). Its observe block cannot use the sweep exception, since the exception covers only the sweep skill's final reply (pragmatic.md:25 "There is no general exemption for coordinators, for other skills"). So the "static report replacing the end-of-message table" (#339's intent, .dev/issues/339/issue-summary.md) would still carry a DONE / NEXT table for half its content, or need a new style exception to an output style whose current exception already runs to five conditions.

2. **Variant 1 rests on an unverified binding.** Its whole 3-minute advantage depends on `observe --once` showing the coordinator's own Run. Q-1 failed for the unbound case (ADJ line 87) and Variant 1 itself marks the coordinator case UNVERIFIED (variant-1-original.md:21). Recording "both, now" as an owner decision on an unverified premise is the riskiest of the three.

3. **Variant 1 shows two vocabularies side by side.** Before the contract note, "stale", "unknown" and "historical" can mean different things in the two outputs (variant-5-original.md:216; variant-1-original.md:22). A person reading both in one chat block cannot tell which wins.

4. **Variant 2 labels an on-demand reply as a periodic report.** The sweep reply is "counts and report path only" (question.md fact 2), produced only on an actual `/sc:sweep` invocation by an assigned coordinator (pragmatic.md:23). Nothing invokes it periodically today. Recording it as "the static report every 3 to 5 minutes" records a capability the system lacks, and Variant 2 concedes the 3-minute end is not met (variant-2-original.md:23).

5. **Variant 2's trigger may never fire.** "Until the note exists" waits on XC-05 and Q5 (variant-2-original.md:24); the note is unbuilt (question.md fact 6). An undated interim answer recorded in the decision ledger tends to become the final answer without a second owner look.

6. **Variant 2 is a narrow reading of #339.** Counts plus a path is "narrower than #339's 'taking inspiration from #409' wording" (variant-2-original.md:22). It satisfies neither the letter (#409-style picture) nor the cadence, yet records itself as the answer.

## Concessions

1. **Variant 3 conflicts with a recorded owner scope choice.** The seed brief says the owner chose on 2026-11-07 that the first PR delivers "a read-only `/sc:sweep` plus the static orchestrator status report on the #409 layout" (seed-brief.md:17). Parking the clause defers something the owner put in scope. My best answer is that the first-PR static report may be the sweep's report file rather than an in-chat periodic block, but whether the owner meant the chat block is UNVERIFIED, and this is the strongest argument against Variant 3.
2. **#339's explicit ask is met in no form for now** (variant-3-original.md:21). The person must run a command or open a file to see the fleet.
3. **It edits spec text that already applies the recommended answer.** Dropping section 6.7's last sentence (variant-3-original.md:10) is a change, where Variant 2 needs none.
4. **It adds a deferred item to track** and leaves the sweep exception without a stated role in a loop (variant-3-original.md:22-23).
5. **It contradicts the spec's recommendation and default** (merged-requirements.md:538) and V5 D2, both of which keep the sweep reply as the WC-16 output.

## Shared assumptions

- **A-001 (no work item, so a wrong answer is cheap to reverse): QUALIFY.** True for code (merged-requirements.md:538, :748 "Recorded only"), but the answer is copied into section 6.7 and the decision ledger, and a recorded owner answer is read as binding by later work, so reversal still costs an owner touch.
- **A-002 (the contract note XC-05 will eventually be written): QUALIFY.** V5 recommends it as the first step (variant-5-original.md:215-217), but it is unbuilt and undated; Variant 3 hedges this by also requiring the loop and by tracking the clause as a deferred row rather than relying on the note alone.

## Per-point verdicts

| Point | Winner | Confidence | One-line reason |
|---|---|---|---|
| S-001 | Tie (nominal 3) | 50% | All three use the same five sections; no structural edge. |
| C-001 | 3 | 60% | Only Variant 3 matches what exists: no loop, and the sweep reply is per-invocation only (pragmatic.md:23, :25). |
| C-002 | 3 | 60% | Waiting for both the loop and the note avoids an undated interim (V2) and a premature commitment (V1). |
| C-003 | 2 | 75% | Variant 2 needs no edit at all; Variant 3 drops one sentence; Variant 1 needs contract, skill and style edits. |
| C-004 | 3 | 65% | WC-16 is a cap, not a schedule (ADJ line 81; debate-transcript.md:625); not promising a cadence is the honest treatment. |
| C-005 | 1 | 85% | Variant 1 is closest to "taking inspiration from #409" and to the seed-brief scope (seed-brief.md:17). |
| X-001 | 2 | 70% | Variants 2 and 3 agree; Variant 2 states it as a positive rule matching V5 D2 word for word (variant-5-original.md:222). |
| X-002 | 3 | 65% | The sweep reply is exempt only for an actual `/sc:sweep` run (SKILL.md:38, :43), so it is an on-demand reply, not a periodic report. |
| X-003 | 3 | 55% | Removing the last sentence resolves the tension with 6.7's own first sentence (merged-requirements.md:1040). |
| U-001 | 1 | 80% | Correct and useful: `observe --once` is the only no-write static status (debate-transcript.md:904). |
| U-002 | 1 | 85% | Flagging Q-1 as UNVERIFIED (ADJ line 87) is the key risk fact any later choice must test. |
| U-003 | 3 | 75% | The unbuilt loop (question.md fact 10) is the fact the other two answers skip. |

## Overall ranking and unassigned pick

Ranking (best first): Variant 3, Variant 2, Variant 1.

Variant 3 ranks first on failure-scenario grounds: it is the only answer that records no capability the system lacks. Variant 2 is close behind because it costs nothing and matches the spec, V5 D2 and section 6.7 as written; its flaw is labelling an on-demand reply as a periodic report under an undated trigger. Variant 1 ranks last because it depends on an UNVERIFIED binding (Q-1), needs unscheduled edits including a new style exception, and mixes two vocabularies.

Unassigned pick: honestly, Variant 2. It is the spec's recommendation and default, requires no edit, and the gap between it and Variant 3 is mostly labelling, since neither causes anything to run periodically today. The seed-brief owner choice (seed-brief.md:17) also weighs against parking the clause outright. I would pick Variant 2 with one amendment taken from Variant 3: record in the ledger that no loop exists yet, so the "every 3 to 5 minutes" cadence is not claimed as met.
