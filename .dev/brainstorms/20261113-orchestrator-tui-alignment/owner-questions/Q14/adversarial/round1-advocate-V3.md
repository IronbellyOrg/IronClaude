# Round 1 advocate statement: Variant 3 (proposal C)

Persona: analyzer (evidence quality, logical consistency). Depth: quick, Round 1 only. Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. "M" = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`; "ADJ" = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`. Every line cited below was re-read on 2026-11-14.

## Position summary

Variant 3 sets the #423 gate at two checkable records: PR #539 merged and the #534 shared live capture recorded. It is the only variant that already matches the spec's own default (M:541) and the V2-02 check as written (M:399), so it needs no new spec wording, while keeping a code change (SW-14) off a planning gate for an advisory, unbuilt v2.

## Steelman

**Variant 1 (gate = #539 merged; capture gates only live-value fields).** Its best case: v2 is advisory and unbuilt, most catalogue fields come from the sweep report rather than from the uncaptured live values, and the capture depends on an Orca app that was not reachable on 2026-11-13 (M:604) plus an unanswered owner question on who runs it (Q24, ADJ:335). Tying all of v2 to an event outside the team's control can stall design indefinitely. Marking live-value fields "pending" is a standard way to design against an open interface, and V1 is the only variant whose gate cannot be blocked by Orca availability.

**Variant 2 (gate = #539 merged + capture recorded + `working` class restored in code).** Its best case: it is the most literal reading of ADJ, which twice says "the #534 live capture that restores the sweep's `working` class" (ADJ:294, ADJ:699). The `working` class is one of eight sweep classes (docs/designs/orchestrator-mode.md:472), and today `_rule_working` returns None so every working row falls to "could not determine" (src/superclaude/cli/sweep/classify.py:251-257). A v2 designed on a sweep that cannot say "working" is designed on a degraded input. V2 also uniquely notices (U-002) that the capture might show Rule 5 cannot be built from what Orca exposes; requiring the code change forces that risk to surface before v2 commits to a design.

## Strengths claimed

1. **It is already the spec's default, so it costs no rewrite.** M:541 sets the default as "ADJ's recommended gate, read as \"capture recorded\" ... SW-14 is then not needed". V2-02 already says "if Q14 means \"capture recorded\", (2) suffices" (M:399). SW-14 already says it is "Needed only if the owner's Q14 answer means \"`working` class restored\", not \"capture recorded\"" (M:203). Choosing V3 confirms the default; choosing V1 or V2 changes rows.
2. **It resolves weak point W5 in the direction W5 itself points.** W5 says the capture is "a read-only record" and that "restoring the class is a later sweep change. The gate as worded conflates a record with a code change" (M:415). ADJ row A-013 says the capture "unblocks" the `working` class (ADJ:335), which describes a precondition, not the change itself. V3 keeps the gate on the record and the change where A-013 places it, after.
3. **Its gate is checkable by a ledger entry.** V2-02's observe clause is "one dated gate note ... citing the merge and the capture record" (M:399). Both V3 parts are facts a ledger entry can cite (a merge, a recorded capture). V2's third part needs a merged PR with its own review cycle and grant (`GRANT(SW-14,pr-submit)`, M:203).
4. **v2 is designed with real live values, not guesses.** V2-02 part (2) requires the capture to include "`projection.attention` values for one live and one blocked worker" (M:399), and the design's open item 6 lists the missing `worker-show` names for `agentWait`, `liveness.verdict` and `status` (docs/designs/orchestrator-mode.md:997). V3 makes v2's design start after those names exist, which avoids V1's admitted redo risk.
5. **It keeps the scope ADJ chose for the other phases.** Like ADJ:699, V3 keeps `/sc:close`, resume and the trust layer out unless the brainstorm decides v2 relays to agents, which matches SW-12's "only if v2 relays to agents, Q14" (M:201).
6. **Waiting costs little where it matters.** The dedicated v2 research pass V2-05 is ungated (M:400, item 2), and V2-03 waits on V2-02 only for its "implementation-facing parts" (M:400). So V3 delays only implementation-facing design, not research.

## Weaknesses identified in others

**Variant 1.**
- It contradicts V2-02 as written: V2-02 lists "the shared capture recorded (XC-03)" as part (2) for every reading of Q14 (M:399), so V1 must rewrite V2-02, V2-01 and the ADJ text (V1 concedes the last).
- Its "per-feature" gate needs a list of which fields are live-value dependent, which V1 itself leaves unresolved ("the brainstorm must list them"). The gate therefore depends on an output of the activity it gates; a V2-02 check cannot pass or fail mechanically until that list exists.
- It accepts the redo risk it names: the design "may assume field names or meanings that the capture later contradicts". Open item 6 shows those names are genuinely unknown today (orchestrator-mode.md:997).
- The claim that "most catalogue fields ... come from the sweep's report" is reasonable but UNVERIFIED: no v2 field list exists (V2-03 item 3 has not run, M:400).

**Variant 2.**
- It puts a code PR on the critical path of a planning gate for a v2 that is advisory (ADJ:294) and unbuilt. W5 names that exact conflation as the defect (M:415).
- Its own risk (U-002) cuts against it: if the capture shows Rule 5 cannot be built, V2's gate "waits on a sweep redesign", so v2 planning is held hostage to sweep work. Under V3 the same discovery is visible in the recorded capture, and v2 designs around it.
- Its literalism is weaker than it looks: ADJ:699 says the capture "that restores the sweep's `working` class is recorded", so the verb applied to the gate is "recorded"; "restores" describes what the capture enables. A-013's "unblocks" (ADJ:335) supports that reading. V2 reads a relative clause as a third gate condition.
- It requires a grant row and a `/sc:pr-submit --monitor 3` run (M:203), adding owner decisions (Q25) to the v2 path.

## Concessions

- V3 still depends on a live capture, so it inherits the Orca availability risk (M:604) and the open Q24 (ADJ:335). V1 is the only variant immune to that.
- V3 allows a v2 that ships while the sweep still shows working sessions as "could not determine" (classify.py:251-257). The gap is carried, not closed.
- V3 departs from ADJ's literal wording by dropping or rewording "restores"; the #423 rewrite (V2-01) must change ADJ's proposed text slightly.
- V3 leaves "when the `working` class is restored" unresolved; SW-14 has no forcing date once it is off the gate.
- V3's claim that the capture records the `agentWait`, `liveness` and `status` names is what the capture is meant to record (orchestrator-mode.md:997); whether one capture run will actually yield all of them is UNVERIFIED, since XC-03 has not run.

## Shared assumptions

- **A-001 (v2 reads the sweep's report JSON as a main input): ACCEPT.** V2-01 item 4 requires the #423 body to name "sweep report JSON v1" as a collector (M:398) and V2-04 says v2 reads only what named collectors publish (M:401).
- **A-002 (PR #539 merges close to today's form): QUALIFY.** All three variants depend on it equally, so it does not rank them; but if the INV-008 ruling (Q1) changes the class list, the "capture recorded" part still holds while V2's SW-14 part could be invalidated, which slightly favours the record-based gates.

## Per-point verdicts

| Point | Winner | Confidence | Reason |
|-------|--------|------------|--------|
| S-001 | tie | 95% | All three use the same five sections. |
| C-001 | 3 | 70% | Two record parts match V2-02 as written (M:399) without a code PR or a field list the gate cannot yet name. |
| C-002 | 3 | 65% | Whole-gate prerequisite as a record is checkable by a ledger entry; V1's per-feature role needs an unwritten field list. |
| C-003 | 3 (tie with 1) | 70% | SW-14 as a follow-up follows W5 and A-013 ("unblocks", ADJ:335); V1 and V3 agree here. |
| C-004 | 1 | 55% | V1 starts the brainstorm earliest; V3's cost is limited because V2-05 research is ungated (M:400), but V1 is still earlier. |
| C-005 | 2 | 75% | V2 is the most literal match to ADJ:294 and ADJ:699; V3 is close but drops "restores". |
| X-001 | 3 | 60% | Waiting for live values avoids V1's admitted redo risk; waiting also for code (V2) adds a PR for an advisory, unbuilt v2. |
| X-002 | 3 | 55% | A carried gap is acceptable for an advisory v2; V1 accepts it too but adds per-field pending marks with no field list. |
| X-003 | 3 (tie with 1) | 75% | W5 names a code change on the gate as the conflation to fix (M:415). |
| U-001 | 1 | 60% | Per-feature gating is a real idea V3 lacks; useful as a fallback if Orca stays unreachable. |
| U-002 | 2 | 60% | A genuine risk V3 does not name; under V3 it is visible in the capture record but not forced. |
| U-003 | 3 | 70% | A records-only gate is what V2-02's observe clause can check (M:399). |

## Overall ranking and unassigned pick

Ranking: Variant 3 first, Variant 1 second, Variant 2 third.

Variant 1 ranks above Variant 2 because it at least keeps code off the planning gate and has a concrete answer to the Orca outage; Variant 2 adds a code PR, a grant and a sweep-redesign risk to the path of an advisory, document-stage project.

If I were not assigned a variant, I would still pick Variant 3, with one honest qualification: it would be stronger if it borrowed V1's U-001 as a fallback (if the capture cannot run by a dated point, the gate drops to #539 merged with live-value fields marked pending) and V2's U-002 as a named risk (the capture record must state whether Rule 5's four conditions can be built from what it recorded).
