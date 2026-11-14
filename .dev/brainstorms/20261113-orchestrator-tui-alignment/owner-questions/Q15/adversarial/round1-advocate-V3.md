# Round 1 advocate statement: Variant 3 (yes eventually, behind the #339 trust layer)

Advocate: V3. Persona: backend (data integrity, fault tolerance, operational reality). Depth: quick, Round 1.
Paths below are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless they start with `F/` (the Q15 folder).

Sources re-read for this statement (2026-11-14):
- `src/superclaude/core/WORKER-CONTRACT.md:61` (WC-12), `:62` (WC-13), `:288` ("Person-started sessions ... are never messaged").
- `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md` (ADJ) lines 294 to 296, 699, 707, 714, 715, 785.
- `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md` lines 201, 398 to 401, 542.
- `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/adversarial/round2-rebuttal-V4.md:68` (D-8, #423 AC "relay them to affected agents").
- `.dev/issues/339/issue-summary.md:6` and `:10`.

## Position summary

V3 is the only answer that keeps #423's stated purpose ("relay them to affected agents", round2-rebuttal-V4.md:68) while making the first release exactly as safe as V1 and V2 (report only, F/adversarial/variant-3-original.md:5). It turns the open question into an explicit, gated plan: no delivery to a non-worker session until the #339 trust layer and the Q16 vocabulary exist, and a design that records now what that delivery would need, so the first release's data shapes do not have to be rebuilt later.

## Steelman

**Variant 1 (never, standing rule).** The strongest case for V1 is that the safest inbound channel is the one that does not exist. The contract already says person-started sessions "are never messaged" (WORKER-CONTRACT.md:288), signing does not stop poisoned content ("encryption alone is not enough", ADJ line 295), and no delivery channel into a non-worker session is known today (F/question.md fact 10). A standing rule removes a whole attack surface permanently, keeps the trust layer off v2's path for good (ADJ line 699), and gives future designers a clear boundary instead of a recurring debate. From a data-integrity view, "no writer" is the strongest integrity guarantee there is.

**Variant 2 (report only; wider delivery a later separate decision).** The strongest case for V2 is that it decides exactly what must be decided now and nothing more. It is the spec's recommended answer and the default if unanswered (merged-requirements.md:542; ADJ line 785), it matches the contract as written (WC-12 at WORKER-CONTRACT.md:61; :288), it keeps the trust layer off v2's path (ADJ line 699), and it avoids committing design effort to a channel nobody has found. It preserves the option V1 closes without paying V3's planning cost. Under uncertainty, deferring an irreversible commitment is usually the right engineering call.

## Strengths claimed

1. **Same first-release safety as the alternatives.** All three variants make the first release report only (diff-analysis C-002, rated Low severity). V3 states it explicitly: "the first release reports only" (variant-3-original.md:5) and V2-01 gets "first release: report to the person or the coordinator only" (variant-3-original.md:10). So V3 adds no near-term inbound channel and no near-term risk relative to V1 or V2.

2. **Honours the existing #423 acceptance criterion instead of dropping it by implication.** #423's criteria ask v2 to "relay them to affected agents" (round2-rebuttal-V4.md:68, D-8). V1 removes that goal and V2 narrows it (diff-analysis C-004). V3 keeps it as a goal with a gate (variant-3-original.md:10). Keeping a stated requirement with an explicit precondition is better record-keeping than dropping it.

3. **Uses the gate the adjudication already wrote for this exact case.** ADJ line 699 says the other #339 phases are not prerequisites "unless the brainstorm decides that v2 relays to agents and not only to the person; then the trust decisions in #339 are." ADJ line 294 says the same. V3 is the variant that exercises that clause as designed: the delivery release waits on the trust decisions and on Q16 (variant-3-original.md:11). The machinery exists in the spec; V3 connects it.

4. **Plans data shapes once (data-integrity argument).** The first release already must carry relayed knowledge as "fixed typed fields, free text only in one `detail` field that is never acted on", with relay through the coordinator (ADJ lines 707, 715). If delivery to other sessions is a stated later goal, V2-03 can design those fields, the audit record and the grant vocabulary (Q16, ADJ line 295) to serve both report and delivery from the start. Under V2, delivery is a later separate decision that may arrive after the first release's store and field set are fixed, forcing a schema change on a store ADJ already counts as "at least an eighth data store" (ADJ line 296). Designing the contract once is cheaper and less error-prone than migrating it.

5. **Covers the case that most needs correction (U-003).** Watcher-launched sessions are "an ordinary session to the sweep" (#409 decision 9, F/question.md fact 1) and may run without a person watching. Under V1 they can never be corrected automatically (variant-1-original.md:23); under V2 that stays undecided (variant-2-original.md:23 to 24). Operationally, a report nobody reads in time (see A-002) is the failure mode for exactly these sessions. V3 is the only variant that names this gap as something v2 is meant to close.

6. **Gives the trust layer a concrete consumer (U-002).** The trust layer is #339 Phase 4, deferred (SW-12, merged-requirements.md:201), proposed in #339 comment 2 (issue-summary.md:10). A security design without a named consumer tends to be built for an imagined threat model; ADJ itself notes the consumers "have different threat models" (ADJ line 295). V3 names v2 delivery as one consumer, which sharpens Q16.

7. **Puts the per-class question where ADJ's criterion already puts it.** ADJ's proposed acceptance criterion (line 714) already requires the design to state, for each session class, "how a course correction is delivered". V3 asks V2-03 to name the channel for each non-worker class (variant-3-original.md:12); that is the same question, answered honestly rather than pre-empted.

## Weaknesses identified in others

**Variant 1.**
- It makes an irreversible standing rule from today's evidence, which ADJ itself does not ask for: ADJ's recommended answer is "Report only (advisory); no delivery to non-worker sessions" (line 785), not "never". V1 also states the rule binds "any later automated program" (variant-1-original.md:5), which is outside v2's scope.
- It constrains the orchestrator of orchestrators before research (its own cost, variant-1-original.md:24). V1 attributes that idea to "#339 comment 1"; the issue summary attributes comment 1 to "never stop polling" and cleanup ownership (issue-summary.md:10) and lists the orchestrator of orchestrators under version 2 (issue-summary.md:6). The comment-1 attribution is UNVERIFIED from the sources I read.
- Unattended watcher-launched sessions can never be corrected automatically (variant-1-original.md:23), and the only mitigation is A-002, an assumption no variant has shown to hold.
- Reopening is expensive by construction: it "needs a new owner decision that overrides a stated standing rule" (variant-1-original.md:22).

**Variant 2.**
- "Later, separate decision" leaves the long-term direction open, as V2 concedes (variant-2-original.md:24, :28). With the direction open, V2-03 has no reason to design the typed fields, audit record or grant vocabulary for a delivery case, so if the later decision is "yes", the first release's store and field set are likely to need a migration.
- It narrows #423's AC for non-workers (variant-2-original.md:22) without saying whether the purpose is abandoned or postponed; future readers of #423 cannot tell which.
- It leaves the unattended watcher-launched case with no stated path (variant-2-original.md:23).

## Concessions

- **No channel exists.** F/question.md fact 10: no channel delivers a message into a person-started or watcher-launched session (UNVERIFIED whether Orca has a usable terminal-input verb). V3's delivery goal may prove impossible, and the design work in V2-03 could be wasted (variant-3-original.md:24).
- **As a goal it contradicts the contract's current wording.** Person-started sessions "are never messaged" (WORKER-CONTRACT.md:288). V3 plans a future change to that rule, which would need its own approved contract edit.
- **Poisoned content is the main risk and signing does not solve it** ("encryption alone is not enough", ADJ line 295). The trust layer is necessary but not sufficient; V3 does not yet say what is.
- **It lengthens v2's path.** V3 says SW-12 (`/sc:close`, resume, trust layer) moves onto v2's path for the delivery release and Q16 must be answered first (variant-3-original.md:11, :23). That wording is broader than ADJ lines 294 and 699, which name only "the trust decisions in #339"; a merge should narrow it to the trust layer. The first release is not blocked.
- **Person approval is unresolved** (variant-3-original.md:29). Without a decision on whether a person approves each delivered correction, V3's goal is under-specified.
- **It is not the default.** The spec's default if unanswered is report only (merged-requirements.md:542); picking V3 is a deliberate departure that costs owner attention.
- v2, the knowledge layer, the #339 trust layer and any orchestrator that manages work are unbuilt; V3's benefits are planning benefits only.

## Shared assumptions

- **A-001 (WC-12 pulled follow-ups are an acceptable v2 correction route for workers): ACCEPT.** WC-12 is the contract's coordinator-to-worker route (WORKER-CONTRACT.md:61) and ADJ line 714 already names it for workers; v2 should still state it as a permission rather than inherit it silently.
- **A-002 (a person reads and acts on v2's reports in reasonable time): QUALIFY.** It plausibly holds for person-started sessions, whose person is present by definition, but not for unattended watcher-launched sessions; that gap is the main reason V3 keeps delivery as a gated goal, and no variant measures it.

## Per-point verdicts

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

## Overall ranking and unassigned pick

Ranking as V3's advocate: **3, 2, 1.** V3 first because it keeps #423's purpose, connects ADJ line 699's existing clause, and designs data shapes once, at no added first-release risk. V2 second because it shares V3's first release and keeps the option open. V1 last because it makes a permanent rule that goes beyond ADJ's own recommendation (line 785) and forecloses the unattended-session case.

Unassigned pick, honestly: **Variant 2.** With no known delivery channel (fact 10), a contract that says "never messaged" (WORKER-CONTRACT.md:288), poisoned content unsolved by signing (ADJ line 295) and nothing built, the cheapest correct answer is V2, which is also the spec default. I would merge in two V3 elements: name unattended watcher-launched sessions as the open case for the later decision, and ask V2-03 to design the typed fields and audit record so that a later delivery release does not force a store migration.
