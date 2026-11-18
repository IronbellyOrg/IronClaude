# Round 2: Advocate B (rebuttal)

Model: opus. Persona: architect + qa. Focus: correctness, risk, test-coverage. Code checked read-only at HEAD 50d4d2b9d. No file under the forbidden run-1 paths was read. Inputs read: round1-advocate-A.md, round2-advocate-A.md, my round1-advocate-B.md.

## Response to criticisms

A's criticisms of B (Round 1 "Weaknesses identified in Variant B" and Round 2 "Updated assessment of Variant B"), answered one by one.

1. **"B's 2.3 guard can never run" (A R1 weakness 1).** CONCEDED, as in my Round 1 concession 1. `findings.py:104` with `:80-81` rejects a line without an anchor, and `ledger.py:135-136` annotates only parsed findings. The guard is withdrawn.
2. **"B's 5.2 is specified wrongly" (A R1 weakness 2).** CONCEDED. With other valid lines, the citation-only line is dropped with a warning (`ledger.py:130-134`). As the only line, the existing refusal raises (`ledger.py:150-157`), and its message lists warnings, not the finding id. I accept A's merged rewrite of T4 and 5.2 (see the position below).
3. **"B guards a hole that does not exist and misses the one that does" (A R1 weakness 3).** PARTLY CONCEDED, PARTLY COUNTERED.
   - Conceded: B did not name the clearing-ignores-block-validity behaviour.
   - Countered: A's own Round 2 (N2) agrees it is the single-valid-block defect that both proposals already route to C-02 and C-03 (A R1 section 5 item 6; my E-10). It is pinned as intended by `test_review_ledger.py:376-385` [VERIFIED by me in code]. It is not a C-01 defect.
   - Countered: A R1 claimed "A's typed locator path at least moves the finding into the ledger". A withdrew that path in Round 2, so it no longer separates the variants.
4. **"B leaves the verified stuck row untouched" (A R1 weakness 4, A R2 "remaining gap").** CONCEDED that B proposed nothing. COUNTERED on severity: the stuck row fails closed, not open. A row with `span None` stays `open` and blocking (`test_review_ledger.py:408-417`). `_brief_ids` keeps every blocking `open` or `regressed` row (`ledger.py:99-104`), and `_decision` returns `ESCALATE` at the cap (`ledger.py:93-96`); the escalation report says "do not start another fix cycle" (`test_review_ledger.py:476-490`) [VERIFIED by me in code]. So the cost is one wasted fix cycle and a human escalation, never a wrong PASS. It is a liveness defect, not an INV-I (fail-closed) breach. That argues for a cheap, visible fix in C-01, not a new configurable policy.
5. **"The projection view has no consumer" (A R1 weakness 5, A R2).** CONCEDED. Withdrawn until a consumer exists.
6. **"Trigger thresholds are unmeasured" (A R1 weakness 6, A R2).** CONCEDED. I accept A's T-c as the replacement for my 5.4 item 2.
7. **"Closed at the PR adapter has no evidence" (A R2).** CONCEDED. Unknown keys stay open in the core; adapter strictness goes to C-10.

## Updated assessment of Variant A

- A's Round 2 hybrid is B's core shape plus a small v1-local locator change. On the shape (thin contract now, per-module engines, convergence on a trigger) we now agree.
- A's Round 2 self-corrections are all correct and I re-verified the ones that matter: the crash is unreachable, `cluster_v2` cannot join anchor-only findings (`cluster.py:126-154,161-181`; `test_review_cluster.py:279-293`), `prior` lines are inert (`ledger.py:259-272`), and the new ledger state had no consumer.
- A's best remaining contribution is the stuck-row analysis (N3) and the observation that `anchor_status` and `anchor_ambiguous` are thrown away (N4). Both are verified (below).
- A's remaining overreach is small and specific: it still wants the locator policy expressed "as data" with two knobs, and it asks the next round to "say it is gone", which has no effect today. Details in the position section.

## New evidence

Verification of the three claims the orchestrator asked about, then new facts.

### (a) A's N2: a re-find dropped for format reasons cannot hold its row open. AGREE, with one bound.

- `merge_round` keeps the parsed findings of every reviewer, valid block or not (`ledger.py:135-138`); a line rejected by `_check_finding` never reaches `parsed["findings"]` (`findings.py:188-192`).
- `members_by_lid` is filled only from clustered findings (`ledger.py:239`).
- The clearing loop clears a row when `status == "resolved_check"` and the row id is not in `members_by_lid` (`ledger.py:254-258`); it never reads `block_ok`, which is read only at `ledger.py:129,147,150,295,423` and `telemetry.py:67` [VERIFIED by me, Grep].
- So a re-find dropped for an over-limit anchor or claim, or for having no anchor, cannot hold its row open, and that row clears in that round.
- The bound: only rows already in `resolved_check` clear this way, that is, rows a reviser named as applied and whose span a change touched (`ledger.py:330-336`). A dropped re-find of an `open` row leaves it `open`. The defect is real but narrower than "any row can clear".
- Ownership: C-02 and C-03 (clearing rule), with the C-01 constraint A states (the repair step runs before validity is decided). I agree with that routing.

### (b) A's N4: `anchor_status` and `anchor_ambiguous` are read only by tests. AGREE.

- Grep over the repo excluding `.dev/tasks/`: written only at `findings.py:350-351`; read only at `tests/review/test_review_findings.py:219,223,230` (the test function at `:227`). Other hits are a vendored copy under `.dev/research/346-review-loop-experiments/p18/ab5/vendor/`, an older `ledger_lite.py` under `.dev/research/`, plans, and `.dev/brainstorms/` notes; none is product code [VERIFIED by me, Grep].
- The ledger row does not store them (`ledger.py:184-202`), and `render_merged_report` prints only claim and anchor for each blocking finding (`ledger.py:447-466`) [VERIFIED by me in code].

### (c) A's claim that the stuck row has no v1-local safe release independent of C-02. AGREE for automatic release; QUALIFY because a manual release exists.

- Automatic release paths in v1 today:
  - Re-anchoring needs a re-find with a locatable anchor (`ledger.py:226-231`). After a successful fix nobody re-finds it.
  - `apply_revision` cannot move a `span None` row to `resolved_check`, because `hunks_touch(None, ...)` is False (`findings.py:446-447`, `ledger.py:331-339`).
  - A reviewer's `prior` line saying "resolved" is only logged (`ledger.py:259-272`); making it count is C-02.
  - Letting a `span None` row reach `resolved_check` on a fix map entry alone would clear it by silence, which is C-02's rule.
- So I agree: every automatic release depends on a C-02 decision.
- Qualification: a v1-local manual release already exists and is independent of C-02. `ledger defer` (`ledger_cmd.py:83-87` calling `ledger.defer`, `ledger.py:350-360`) parks the row and recomputes the last decision to PASS when no other blocking id remains [VERIFIED by me in code]. It is a human accepted-risk release, not a verified-fix release. Together with point 4 above (the row escalates, fail-closed), this means the stuck row already has a safe, if manual, exit today.

### New facts

- **N-B1. The merged report is pinned in a way that constrains where anchor status may be shown.** `test_rendered_merged_report` asserts that the text between `## Reviser brief` and `Rules for` contains no non-blocking id, with the comment "the reviser brief id parser of the Stage 2 harness reads these ids" (`test_review_ledger.py:459-467`) [VERIFIED by me in code]. So anchor status must be printed in the per-row `### Lx` block of `## Blocking findings` (`ledger.py:439-466`), not in the reviser brief id line, or a harness parser and this pin can break.
- **N-B2. Surfacing needs no prompt-file change.** `render_merged_report` is code in `ledger.py:408`, and its docstring says it is "the merged report the reviser and the next reviewer read" (`ledger.py:411`) [VERIFIED by me in code]. Printing anchor status there reaches both the reviser and the next reviewer without editing `document_review_loop_prompts.md` or its plugin mirror (INV-N).
- **N-B3. There are two `parse_block` functions and many callers.** `findings.py:124` and `findings_v2.py:215` [VERIFIED by me, Grep]; A's Round 1 E10 counts 15 callers of the v1 one, mostly tests [from the proposal, not re-checked]. A repair step placed in callers (for example inside `merge_round`) would miss the other callers and the v2 path. It must be called from inside both `parse_block` functions, on each block line before the check.
- **N-B4. The stuck row escalates, fail-closed.** See response 4: `ledger.py:93-104`, `test_review_ledger.py:476-490` [VERIFIED by me in code].

## Concrete position you stand behind

**C-01 decision:** a thin shared contract now, per-module engines, convergence to one engine only on a mechanical trigger. Concretely:

1. **Shared contract now.** The id grammar `_ID` (already shared); one limits constants module imported by both parsers (names checked against INV-K, by running `make lint-architecture`); one repair function called from inside both `parse_block` functions on each line before the check (policy: C-06); the shared `refs_norm` token list with `T<PP>.<TT>` added once; hash and identity helpers.
2. **Engines.** The spec loop stays on v1 `findings.py`, `ledger.py`, `review-ledger/1` and v1 clustering. Reflect stays on the v2 kernel. No `cli/reflect` change (INV-A).
3. **Stuck row (FX-2), fixed inside v1 with no new configuration.** In `render_merged_report`, print for each blocking row whether its anchor was found, missing or ambiguous, inside its `### Lx` block (N-B1). Optionally store the status on the row additively. No knobs.
4. **Unknown keys** stay open in both parsers. No ledger passthrough keys yet.
5. **Prior lines** unchanged.
6. **Convergence trigger:** A's T-a, T-b and T-c, with the precondition A records (give `same_defect_v2` an anchor-span branch, or derive a `spec`-role citation from the located span, before any loop moves).
7. **Routed out:** clearing that ignores block validity (N2) and how an unlocated row may clear go to C-02 and C-03.

Comparison with A's Round 2 hybrid, point by point.

| Item in A's hybrid | My position | Why |
|---|---|---|
| Thin contract now, per-module engines, convergence on a trigger | AGREE | Same decision. |
| Locator policy as data in v1 (`on_missing`, `on_ambiguous`) | DISAGREE | A's own `spec-loop` default is "keep the row, as today", so each knob has one used value. A configuration value that never changes is an abstraction with no consumer, the same rule A used to drop my projection view. The other values A named in Round 1 (block, warn, fall back to a citation) either drop a blocking finding (block), add nothing over surfacing (warn), or need citations in v1 (convergence work). Hard-code "keep and surface" now; make it data when the engines converge. |
| Surface `anchor_status` and `anchor_ambiguous` in the merged report and reviser brief | AGREE, WITH A PLACEMENT CONDITION | Verified cheap and useful (N4, N-B2). It must go in the per-row `### Lx` block, not in the reviser brief id line that a harness parses and `test_review_ledger.py:459-467` pins (N-B1). It must be generated by `render_merged_report`, not added to the prompt file, so INV-N is untouched. |
| "The next round is asked to locate it or say it is gone" | DISAGREE ON THE SECOND HALF | "Say it is gone" can only be a `prior` line, which is inert (`ledger.py:259-272`). Asking reviewers for output that changes nothing is the same cost A conceded for the typed re-review line. Ask only that the row be re-located (that does re-anchor, `ledger.py:226-231`); route "say it is gone" to C-02. |
| How an unlocated row may clear goes to C-02 | AGREE | Verified in (c). Note for C-02: the row already fails closed (escalates) and `ledger defer` is a manual exit, so this is a liveness item, not an INV-I item. |
| T-c replaces my 5.4 item 2 | AGREE | It can be checked on the diff of a fix; my "two in one quarter" had no basis. |
| Projection view withdrawn | AGREE | Conceded in Round 1 and above. |
| Shared repair step placement ("before the parser decides validity") | AGREE, WITH A REFINEMENT | The step must be called inside both `parse_block` functions (`findings.py:124`, `findings_v2.py:215`), not in their callers (N-B3). It can rescue over-limit lines only; it must not invent an anchor for a citation-only line, so it narrows but does not close N2. |
| Ledger passthrough keys deferred | AGREE | No consumer reads provenance from the ledger. |
| Unknown keys open; adapter strictness to C-10 | AGREE | N5 verified by A; my "closed at the adapter" is withdrawn. |
| Prior lines unchanged, semantics to C-02 | AGREE | Verified inert. |
| T1 survives with `test_review_cluster.py:279-293` added | AGREE | Also add `test_rendered_merged_report` (`test_review_ledger.py:442-473`) to the named pins, because the surfacing change touches that function. |
| T2 + 5.1 merged, projection check dropped | AGREE | Byte-equal parser output on already-valid lines is the right gate for the repair step. |
| T3 + 5.3 merged, run after the snapshot fix and after A-002 is stated | AGREE | Keep my pre-registered decision rule. |
| T4 + 5.2 rewritten as one (pin today's rejection, one and several reviewers) | AGREE | Matches the verified behaviour (`ledger.py:130-157`). Add one assertion: in the several-reviewer case, the same reviewer's other valid lines are still merged (`ledger.py:135-138`). |
| T5 rewritten (span None row, status surfaced, `named_not_touched`, clearing left to C-02) | AGREE, WITH ONE ADDITION | Add an assertion that at the cap such a row gives `ESCALATE`, not PASS. That pins the fail-closed property the C-02 change must keep. |
| Convergence precondition (anchor-span branch or derived `spec` citation) | AGREE | Follows from N1. |

## Updated per-point table

| Point | Superior | Confidence | Reason |
|---|---|---|---|
| S-001 | A | 65% | CHANGED (70% to 65%). A's per-row table is easier to check; it matters less now that both sides agree on most rows. |
| S-002 | B | 75% | CHANGED (70% to 75%). The trigger, sharpened by A's T-c, is now accepted by both sides. |
| S-003 | NEITHER | 55% | Grouping the evidence differently changes no conclusion. |
| S-004 | A | 55% | CHANGED (60% to 55%). A rates each invariant's level; coverage is otherwise similar. |
| S-005 | HYBRID | 80% | CHANGED (75% to 80%). The merged test set in the position table, with the ESCALATE assertion added to T5 and the merged-report pin added to T1. |
| C-001 | B | 80% | CHANGED (75% to 80%). A's Round 2 adopts the thin contract now; the kernel cannot host the anchor loop. |
| C-002 | B | 70% | CHANGED (65% to 70%). Both sides now defer the locator-agnostic `annotate` and pin today's parser rejection; my guard is withdrawn too. |
| C-003 | B | 70% | CHANGED (65% to 70%). `prior` is inert and A withdrew the typed line kind. |
| C-004 | B | 90% | CHANGED (85% to 90%). `cluster_v2` cannot join anchor-only findings, now conceded by A. |
| C-005 | HYBRID | 60% | Open unknown keys in the core; adapter strictness to C-10. |
| C-006 | HYBRID | 55% | The ledger drops passthrough keys, but no consumer reads them; both sides defer. |
| C-007 | B | 70% | CHANGED (65% to 70%). The constants module and one repair step inside both parsers remove the copied literals without merging parsers. |
| C-008 | HYBRID | 70% | CHANGED (A 70% to HYBRID 70%). A's verified stuck row, fixed inside v1 by surfacing anchor status (B's engine-local route), without configuration knobs; clearing to C-02. |
| C-009 | HYBRID | 60% | PR review needs no ledger; both designs need vocabularies as data (`findings_v2.py:109-110`). |
| C-010 | HYBRID | 60% | CHANGED (B to HYBRID). Both sides read citations as untested, not disproved; measure under the merged T3/5.3. |
| X-001 | B | 80% | CHANGED (75% to 80%). A now agrees to converge on a trigger. |
| X-002 | B | 65% | Duplication sits in helpers and literals the contract removes; no cost paid twice yet. |
| X-003 | B | 80% | CHANGED (75% to 80%). The rewrite would break the anchor-only clustering pin and reviewer overlap; A concedes. |
| X-004 | HYBRID | 60% | Same as C-005. |
| X-005 | NEITHER | 85% | Neither original fix closes a reachable path; the real items are the stuck row (C-01, surfacing) and dropped re-finds that cannot hold a row open (C-02, C-03). |
| A-001 | NEITHER | 90% | Contradicted by `findings.py:104` and `ledger.py:135-136`. |
| A-002 | NEITHER | 65% | Neither variant states how line numbers reach reviewers; state it before the merged T3/5.3 runs. |
| A-003 | B | 75% | CHANGED (70% to 75%). The kernel is one commit old, shadow-only, enforces v1 categories and cannot cluster anchors; fit to share helpers with, not to host the loop. |

Not checked: the E1 and E2 run counts; how line numbers reach reviewers (A-002); whether `make lint-architecture` Check 11 would flag a constants-module name (not run); A's count of 15 `parse_block` callers.
