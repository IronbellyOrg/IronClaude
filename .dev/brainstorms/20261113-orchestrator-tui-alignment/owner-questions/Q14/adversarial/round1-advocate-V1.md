# Round 1: Advocate for Variant 1 (gate = PR #539 merged; the capture gates only live-value features)

Persona: architect (structure, dependencies, long-term impact). Paths below are relative to the worktree root unless they start with `F/` (this Q14 folder). "MR" = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`. "ADJ" = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. Every line cited below was re-read on 2026-11-14 unless marked UNVERIFIED.

## Position summary

Variant 1 puts on the whole-v2 gate only the one thing every part of v2 depends on (the merged sweep, PR #539), and moves the live Orca capture to the exact v2 fields that read live values, marked pending until it lands. That keeps an external, currently unreachable dependency (a live Orca session, MR:604) off the critical path of an advisory planning step, and it removes the record-versus-code ambiguity (W5, MR:415) by not tying the whole gate to either.

## Steelman

**Variant 2 (merged + capture recorded + `working` class restored in code).** The strongest case: the gate exists so that v2 is designed against a sweep that tells the truth about sessions. Today `_rule_working` returns None and every working session falls to `could not determine` (`src/superclaude/cli/sweep/classify.py:251-257`; class list at `docs/designs/orchestrator-mode.md:472`). A knowledge layer built on top of a sweep with a blind class inherits that blindness. Variant 2 is also the most literal reading of ADJ, which twice says "the #534 live capture that restores the sweep's `working` class" (ADJ:294, ADJ:699), and it is the only variant that turns the risk "the capture shows Rule 5 cannot be built from what Orca exposes" (variant-2 line 24, U-002) into something discovered before v2 design rather than after.

**Variant 3 (merged + capture recorded).** The strongest case: it is the spec's default (MR:541), it keeps the gate a matter of records that a dated ledger entry can check (V2-02, MR:399, and W5 at MR:415), and it gives the v2 design the real live names (`agentWait`, liveness, status) and the `projection.attention` values for a live and a blocked worker, which V2-02 item (2) already asks for (MR:399). ADJ row A-013 ties the capture not only to the `working` class but also to V5's open items O-13 and O-14 and "the #423 gate" (ADJ:335), so the capture has value for v2 beyond one class. It avoids Variant 2's code PR on the critical path while still not designing blind.

## Strengths claimed

1. **The gate matches the dependency graph, not a proxy for it.** v2's first release must read "only what named collectors publish" (V2-04, MR:401) and the rewrite names two collectors, "sweep report JSON v1" and "observe snapshot v1" (V2-01 item 4, MR:398). The capture is not a collector; it is a read-only record that "unblocks" the `working` class (ADJ:335). Gating all of v2 on it couples v2 to an input that only some of its fields need. Variant 1 gates each consumer on its own producer, which is the standard way to keep a dependency graph honest.
2. **It keeps an unreachable external dependency off the critical path.** The capture needs ORCA-AVAILABLE, and "every live lane needs it: CAP (XC-03) ..."; the app was not reachable on 2026-11-13 (MR:604). It also needs an owner answer on who runs it (Q24, ADJ:335). Variants 2 and 3 both stall the v2 gate on that; Variant 1 does not.
3. **It fits the spec's own design step.** V2-03 item (3) already requires the design to "name every catalogue field and its source ... and which fields need a schema decision" (MR:400). Marking live-value fields "pending capture" is one more column in a table the design must produce anyway, so Variant 1 adds almost no process.
4. **It dissolves W5 instead of picking a side.** W5 says "the gate as worded conflates a record with a code change" (MR:415). Variants 2 and 3 each pick one reading; Variant 1 removes both from the whole-v2 gate, so SW-14 (MR:203) stays a #534 follow-up with no conditional wiring into V2-02.
5. **Proportion.** v2 is advisory, delivers to the person or coordinator only, and marks LLM-derived entries inferred (ADJ:294). A planning gate for an advisory layer should be the lightest gate that prevents real harm; the merged sweep is that gate.

## Weaknesses identified in others

**Variant 2.**
- It puts a code PR (SW-14) on the critical path of a planning gate. SW-14 needs XC-03, then a supervised worker, a test, a PR via `/sc:pr-submit --monitor 3` and a grant row (MR:203). That is four dependencies stacked behind an Orca session that was unreachable (MR:604).
- Its own risk (variant-2 line 24) cuts against it: if Rule 5 cannot be built from what Orca exposes, v2 waits on a sweep redesign. A gate that can turn into an open-ended redesign is a poor gate.
- Literal fidelity to ADJ's phrase is weak support, because ADJ's own A-013 calls the capture something that "unblocks" the class (ADJ:335), which W5 reads as meaning restoring it is a later change (MR:415). The spec has already flagged the literal wording as a conflation.

**Variant 3.**
- It still blocks all of v2 on the live capture (variant-3 line 23), so it shares Variant 2's exposure to MR:604 and Q24 for every field, including those that never touch live values.
- It admits v2 "must carry that gap" of working sessions shown as `could not determine` (variant-3 line 22). Once the gap is accepted, the capture's value to v2 is limited to naming fields, which is exactly what Variant 1's per-field pending marker already handles. Variant 3 pays the waiting cost without buying a working class.
- Its rewording of ADJ's sentence ("that records the values the `working` class needs", variant-3 line 10) is still a departure from ADJ:699, so it is not free of the rewording cost it counts against Variant 1.

## Concessions

- **Rework risk is real.** A design started before the capture may assume field names or meanings the capture contradicts (variant-1 line 22). Variant 3 avoids that.
- **Departure from ADJ and from V2-02 as written.** ADJ:294 and ADJ:699 both put the capture in the gate, and V2-02 item (2) lists "the shared capture recorded (XC-03)" as a gate part independent of the Q14 branch (MR:399). Variant 1 needs V2-02 rewritten, not just a branch chosen.
- **The capture is about more than the `working` class.** A-013 links it to `projection.attention`, V5's O-13 and O-14, and "the #423 gate" (ADJ:335). Variant 1's text names only the `working` class and `projection.attention` (variant-1 line 5) and may under-list what is live-dependent.
- **A fuzzier gate.** "Which v2 fields are live-value dependent" is left to the brainstorm (variant-1 line 28). Until that list exists, a ledger entry cannot check the per-feature part of the gate; Variant 3's gate is checkable today (U-003).
- **The early-start benefit is smaller than it looks.** V2-05 (the research pass) is ungated, and V2-03 waits on V2-02 only "for its implementation-facing parts" (MR:400; question.md fact 6). So under Variant 3 much of the early thinking can already start. Variant 1's unique unlock is mainly the implementation-facing design work.
- **Unverified claim in my own variant.** "Most catalogue fields (sessions, worktrees, packages, git state) come from the sweep's report" (variant-1 line 17) is UNVERIFIED: no catalogue field list exists yet, and V2-01 names a second collector (observe snapshot v1, MR:398).

## Shared assumptions

| ID | Response | Reason |
|----|----------|--------|
| A-001 (v2 reads the sweep report JSON as a main input) | QUALIFY | V2-01 names two collectors, sweep report JSON v1 and observe snapshot v1 (MR:398), so the sweep is a main input but not the only one; how much of v2 rides on sweep classes is UNVERIFIED until V2-03 lists fields. |
| A-002 (PR #539 merges close to today's form) | QUALIFY | All three gates name #539, so a change under Q1 / INV-008 hits all three equally; I did not verify the INV-008 ruling's status (UNVERIFIED), and the gate should name the read-only sweep's contract ("sweep report JSON v1") as well as the PR number so a reshaped merge is still checkable. |

## Per-point verdicts

| Point | Winner | Confidence | Reason |
|-------|--------|-----------|--------|
| S-001 | tie | 95% | Same five sections in all three; no structural edge. |
| C-001 (gate parts) | 3 | 55% | Two records are ledger-checkable today and match V2-02 item (2) and A-013; Variant 1's per-field part is not checkable until the field list exists. |
| C-002 (role of the capture) | 1 | 60% | The capture serves specific fields (A-013, ADJ:335), so gating those fields, not all of v2, matches the real dependency. |
| C-003 (SW-14) | tie (1 and 3) | 80% | Both keep the code change off a planning gate, as W5 (MR:415) and SW-14's conditional wording (MR:203) allow. |
| C-004 (when the brainstorm starts) | 1 | 55% | Starting at #539 merge avoids the MR:604 / Q24 stall, though V2-05 and the non-implementation parts of V2-03 already soften Variant 3's delay. |
| C-005 (fidelity to ADJ wording) | 2 | 85% | Variant 2 is the literal reading of ADJ:294 and ADJ:699; fidelity alone, not correctness. |
| X-001 (should v2 design wait for live values) | 1 | 55% | Design can name live-dependent fields and mark them pending (V2-03 item 3 already requires naming field sources), at a known rework risk. |
| X-002 (v2 showing working sessions as `could not determine`) | tie (1 and 3) | 75% | Both accept the gap for an advisory layer; Variant 2's refusal costs a code PR for a class the sweep already reports honestly as undetermined. |
| X-003 (code change on a planning gate) | tie (1 and 3) | 85% | A planning gate should check records, not code; W5 flags the conflation. |
| U-001 (per-feature gating) | 1 | 70% | It is the one contribution that decouples v2 from Orca availability; worth keeping in any merge. |
| U-002 (capture may show Rule 5 is unbuildable) | 2 | 60% | A real v2 risk only Variant 2 names; it argues for running the capture early, which a per-field pending marker or a capture gate both surface. |
| U-003 (gate of ledger-checkable records) | 3 | 75% | Matches V2-02's "dated ledger entry" design (MR:399) and W5's evidence wording (MR:415). |

## Overall ranking and unassigned pick

**Ranking as the Variant 1 advocate:** Variant 1, then Variant 3, then Variant 2. Variant 1 has the cleanest dependency structure and the smallest critical path; Variant 3 is close behind and better on checkability; Variant 2 puts a code PR and a possible sweep redesign on a planning gate for an advisory layer.

**Honest unassigned pick:** Variant 3, with Variant 1's U-001 grafted in. Variant 3 is the spec's default (MR:541), needs no rewrite of V2-02's capture item (MR:399), keeps the gate checkable by a dated ledger entry, and the capture feeds more than one class (ADJ:335). The graft: if the capture is still blocked by Orca availability (MR:604) or Q24 after a dated deadline the owner sets, V2-03 may proceed with live-value fields marked pending, so the gate cannot stall indefinitely.
