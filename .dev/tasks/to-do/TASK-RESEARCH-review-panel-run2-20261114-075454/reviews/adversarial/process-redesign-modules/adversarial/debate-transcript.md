# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel advocates, Round 2 sequential rebuttals A then B) plus Round 2.5 invariant probe; Round 3 skipped (depth=standard)
- Convergence achieved: 96.55% (28 of 29 diff points agreed; Round 1 alone: 17 of 29 = 58.62%)
- Convergence threshold: 80%
- Focus areas: correctness, risk, test-coverage
- Advocate count: 2 (variant-1 = Proposal A, Sweep-Sheet-shaped, `x13-advocate-A-r1` / `x13-advocate-A-r2`; variant-2 = Proposal B, Recipe-Ledger-shaped, `x13-advocate-B-r1` / `x13-advocate-B-r2`)
- Agents: every advocate and the fault-finder were separate agents dispatched by the orchestrator; the orchestrator did not advocate. Full advocate statements (not shortened) are in `round1-advocate-A.md`, `round1-advocate-B.md`, `round2-advocate-A.md`, `round2-advocate-B.md`; fault-finder text in `round2.5-fault-finder-raw.md`. This transcript records each statement's structure and the content the scoring uses.
- Taxonomy coverage gate: L1 = 4 points (S-001, S-002, S-003, C-013), L2 = 15, L3 = 10; every level was addressed in both rounds by both advocates; no forced round was triggered.
- Shared assumptions: both advocates responded to all of A-001..A-005 in Round 1 and to A-001, A-003, A-004 again in Round 2; no `[OMISSION]` flags.

## Round 1: Advocate Statements

### Variant A Advocate (default model, default persona; file `round1-advocate-A.md`)
**Position**: Keeps A's core (script-first for classes a script can decide, advisory-only checks, no demotion or promotion in the core, no reviewer-side shell, classes as module data) and moves to a named hybrid on one point: "script-built items and advisory-only checks (A), answered through an optional record-only row block (B's carrier without B's overlay)". Takes from B a separate record-only output file (`review-rowcheck/1`), B's code-level tests, and a per-item answer carrier; rejects demotion and promotion even behind a switch.

**Steelman of Variant B**: nothing has to be built before the review, so no extractor to maintain and no second source of false positives; a per-row reviewer answer turns `observed` from a declared number into something computed from reviewer output, with the empty-block rule (`findings_v2.py:291-298`) giving that a consequence; a separate rowcheck file keeps `review-precheck/1` byte-identical; demotion and promotion are contained (off by default, never CRITICAL, own flag only); T-B1..T-B7 tests and a card-to-tool lint; honest first gate (compliance spike) and M-B3.

**Key strengths claimed** (all with file:line re-read):
1. The tool wall is real: `reflect-reviewer` has no Bash and `permissionMode: plan` (`reflect-reviewer.md:5, 8`); E2's R-C4/R-C8 assume a shell; A runs C4 and C8 in the script.
2. Advisory-only is the repository's own rule: `verify_cmd.py:10-12`, reflect `SKILL.md:345`, `ledger.py:3-4`, C-02's outcome keeping typed `blocking` as the only authority.
3. No second container or normaliser: the sidecar is read by `cluster_cmd.py:117, 148-151` and `verify_cmd.py:99-105, 130-135`; `_norm` equals `findings.flat`.
4. No change to the closed slot schema (`panel.py:46, 214-216`); B must say what `recipes` does to `review-panel/1` and `SKILL.md:340`'s "unmodified resolve output".
5. A has a model-free per-class gate once its inputs exist (M1); caveat owed: needs extractors (0 code) and ground truth (none built).
6. Failure degrades small (card loader + sidecar entry point = synth-05 option 4).

**Weaknesses identified in Variant B** (9, with evidence): demotion is a second authority over `blocking` and B concedes the reading; the exactness risk is B's own number (0.835 per row); demotion by flag alone is invalid in v2 when `reflect_category` is set (`findings_v2.py:161-162`); the switch has no host and the brief renderer does not exist (`merge_cmd.py` has no extension point; grep for a renderer returns only `ledger._brief_ids`); B's primary target (the v1 loop) has no precheck to extend (`verify_cmd.py:82, 89, 133-143`); B's CB-2 route cites the wrong list (`ledger.py:467-474` prints ledger rows only); row-format failures couple to the quorum floor through the empty-block rule; row-block placement conflicts with `document_review_loop_prompts.md:33`; the per-row answer is still a self-report (`ran` unverified until C-08).

**Concessions**: A's "existing mechanism" for a no-defect item is hollow (nothing writes `observed` but the orchestrator, `findings_v2.py:6`, `SKILL.md:345`); a clean review can be made invalid by an empty assignment (`findings_v2.py:292`); no extractor exists, the build is large and recall may fail; A's offline gate is conditional (and X-14 was never named); A has no host for spec review on v1; A's additive flags in `precheck.json` endanger the byte-identity pins; A is thinner on tests; GQ-131 answered by omission.

**Shared-assumption responses**: A-001 QUALIFY; A-002 QUALIFY; A-003 QUALIFY; A-004 QUALIFY; A-005 QUALIFY.

### Variant B Advocate (default model, default persona; file `round1-advocate-B.md`)
**Position**: Hybrid built on B's core and cut back where B overreaches: adopt B's reviewer-side row carrier `rows-v1` with `assigned` computed from the bound recipes and `observed` computed from parsed rows; adopt `review-rowcheck/1` as advisory only; build neither demotion nor promotion in the first increment (reserve the name, build `apply` only after M-B3); accept A's script pre-pass as an optional producer admitted class by class after M1; keep class definitions as module data.

**Steelman of Variant A**: determinism where possible (C4, C8 mechanical); advisory by construction with a small core and no change to parsers, ledger or reflect contract; the only first gate that spends no model tokens (M1); keeps the shell out of the reviewer (`reflect-reviewer.md:5, 8, 59`); refuses to let the core write findings the reviewer did not write or lower a flag the reviewer did write (`verify_cmd.py:10-12`; C-03's fail-closed choice); degrades honestly.

**Key strengths claimed** (8): B is the only variant with a reviewer-side carrier (`coverage_context` takes whatever the caller supplies, `findings_v2.py:196-212`; `coverage_rows` is a per-finding link only); B's first increment is isolated from every shipped parser (`_blocks_after`, `findings.py:38-76`; second file keeps precheck byte-identical, tests at `test_review_verify_citations.py:165, 176`); recipes are written for the tools the agent has (`requires_tools`, T-B5); concrete code-level test plan T-B1..T-B7 and a decision rule that kills its own idea; the binding has a consumer in the spec loop (`review panel resolve`, `document_review_loop_prompts.md:70`); containment of demotion (union at `ledger.py:187`); maps onto rf-qa checklist marks (`rf-qa.md:484-511`); no per-class extractor.

**Weaknesses identified in Variant A** (7+1): A's "existing mechanism" for items with no finding does not exist; A's advisory check reaches only findings-v2 citations (`verify_cmd.py:133-143`) so the v1 loop gets nothing; per-reviewer assignment conflicts with the loop's "same brief" rule (`:70`); A's pre-pass reaches into a fenced brief (`reviewer-spec.md:55-59`); M1 is less model-free than stated and the fallback has no value; A reads `ledger.py:3-4` as a rule about `blocking` where it is a status rule; A removes CB-2 by not adopting it, but nothing records an examined-and-clean item; the size and determinism burden is real.

**Concessions** (10): no brief renderer exists in `cli/review`; the row block conflicts with the loop's "end the report with the findings block" (`:33`); the overlay needs a merge hook (`merge_cmd.py:84-109`); demotion cannot be justified from evidence and is unstable across rounds (`ledger.py:210-218`); the name `recipes` collides with `cli/swarm/recipes/`; the sidecar key is the card stem (`cluster_cmd.py:146`) not `<slot_id>-<i>`; compliance is a second unmeasured duty; row quotes need their own limits (12 to 200); one citation off by one (`skills/task/SKILL.md:224` vs 225); for reflect and PR review A's evidence-only brief fits better.

**Shared-assumption responses**: A-001 QUALIFY; A-002 QUALIFY; A-003 REJECT as stated (advisory steps need no hook, merge-altering steps do); A-004 REJECT; A-005 QUALIFY.

## Round 2: Rebuttals

### Variant A Rebuttal (`round2-advocate-A.md`)
Withdraws part (c) (additive item-evidence flags in `precheck.json`); accepts B's reviewer-side row block as a record-only carrier, with the narrowing that `observed` has a consequence only for an EMPTY findings block (`findings_v2.py:264-298`: one finding plus zero rows is valid); gives up one argument against demotion (`ledger.py:3-4` is a status rule) and replaces it with stronger ones (`ledger.py:210-213`; `_brief_ids` hides a demoted row from the Reviser brief, `ledger.py:99-104`; a measured quote-failure floor of 5.5 percent per quote from 31 of 568 citations that reached the quote test); holds four points: no demotion or promotion in the core, no reviewer-side shell, no `_SLOT_KEYS` change now, CB-2 outside the core.
New verified facts: the v1 loop has no snapshot, sidecar, cluster or precheck step anywhere (`verify-citations|review cluster|coverage.json|input-snapshot` appears in 8 files under `src/superclaude`, none a loop host); three reviewer-id spaces (`panel.py:668`, `cluster_cmd.py:146`, `merge_cmd.py:86-90`); `recipes` collides with `cli/swarm/recipes/`; placement before the findings block in v1 (`:33`, `:58`) and after in v2 (`reviewer-spec.md:39`, `SKILL.md:344`); recorded sidecars: 2 of 13 reflect sidecars have empty `observed`.
Merged resolution (its section 5): 21 numbered components (built now / reserved / not built / gates / per-module). Updated positions on all 29 points, 11 marked CHANGED. Remaining disagreements D-1..D-5.
Shared assumptions: A-001 QUALIFY; A-003 REJECT (changed); A-004 REJECT for reviewer-typed quotes, ACCEPT for script evidence (changed).

### Variant B Rebuttal (`round2-advocate-B.md`)
Verified A's seven new claims (a) to (g): all CONFIRMED (the observed-for-empty-block-only narrowing; three id spaces plus the asymmetry that a missing sidecar entry makes `cluster` degrade silently but stops `verify-citations`; `_brief_ids`; quote failures re-measured at 9.9 percent per quote and 18.8 percent per two-quote row, with 2 to 57 percent by run; placement sentences and v2 precedent; v1 loop has no precheck step; `ledger.py:467-474` does not list a PROBLEM row without a finding; B's own R1 citation `ledger.py:468` was wrong). Drops everything that needs a missing host: the `rowcheck: off | advisory | apply` profile value, the overlay, demotion, promotion, the `recipes` slot key; accepts uniform per-module binding, per-engine row-block placement, CB-2 outside the core, extractors reserved behind a per-class offline gate. Holds four things: the reviewer-side row block as the only source of `observed`; the second file; a single writer computing `observed` from parsed rows (recorded orchestrator-written sidecars are partial and sometimes not a subset: comboC-r3, comboA-r3, comboA-r2); wiring of the v1 loop waits for a compliance spike and an RL-versus-K arm.
Decisions (i)-(v): no `apply` key (document only); uniform binding now, slot-keyed binding reserved; v1 row block before the findings block, v2 after; extractors reserved, not built; CB-2 outside the core. Component-by-component answer to A's 21 components: 15 ACCEPT, 6 AMEND (extractor field dropped; same entry point also computes `observed`; G-0 extended; v1 wiring gated on G-2/G-3; class-row namespace and copy for UC-1). Residual disagreements D-5 (is a row block worth wiring on v1), D-6 (does UNSURE count as observed), D-7 (editing reflect step 5 under the frozen contract). D-3 and D-4 closed.
Shared assumptions: A-001 QUALIFY; A-003 REJECT (changed to full REJECT); A-004 REJECT for reviewer-typed quotes, ACCEPT for script evidence (changed).

### Points on which the two advocates agree after Round 2
Classes are module data and the core holds no class constants; the reviewer-side row block exists, is record-only and is the source of `observed`; the row check is advisory and writes a second file (`review-rowcheck/1`), `review-precheck/1` and `reread_set` byte-identical; no demotion, promotion, CB-2, profile value or overlay in the core; uniform per-module binding, no `_SLOT_KEYS` change now; tool wall by lint test; counts-only telemetry with a leak test; gates in order G-0 code tests, G-1 per-class offline gate, G-2 compliance spike, G-3 arms (Z0, K, RL, SS), G-4 demotion safety; A-001 is a precondition for any effect claim; A-004 needs `check_skipped` outside the snapshot.

## Round 3: Final Arguments
Skipped: depth=standard (log: "Round 3 skipped: depth=standard"). Round 2.5 ran (see `invariant-probe.md`).

## Scoring Matrix

Position labels: A = Variant A (Proposal A), B = Variant B (Proposal B), Hybrid = the named hybrid the two advocates converged on, Neither = neither approach's distinguishing feature is needed. Confidence = mean of the two advocates' Round 2 confidences, +10 where the losing advocate conceded the point, never above 95. "R1" = agreement after Round 1 (same label from both).

| Diff Point | Level | A R1 / B R1 | A R2 / B R2 | Agreed | Winner | Confidence | Evidence Summary |
|------------|-------|-------------|-------------|--------|--------|------------|------------------|
| S-001 | L1 | Neither / Neither | Neither 85 / Neither 85 | yes | Neither | 85% | Section order changes no behaviour. |
| S-002 | L1 | B / B | B 60 / B 60 | yes | Variant B | 60% | Numbered tagged evidence table is easier to audit. |
| S-003 | L1 | B / B | B 60 / B 60 | yes | Variant B | 60% | Explicit non-claims section guards scope; A's limits sit inside section 8. |
| S-004 | L2 | B / Neither | B 65 / Neither 60 | NO | Unresolved | 50% | A advocate: B's consistency table reads better; B advocate: neither format is more complete. Split, low severity. |
| C-001 | L2 | Hybrid / Hybrid | Hybrid 70 / Hybrid 75 | yes | Hybrid | 73% | A's card loader and one writer entry point + B's record-only row block and separate rowcheck file; no overlay, no profile value, no slot key, no precheck flags. |
| C-002 | L3 | Hybrid / B | Hybrid 70 / Hybrid 65 | yes (after R2) | Hybrid | 68% | Card-derived (later script-derived) items answered through the row block, `observed` computed from parsed rows; hard consequence only for an empty block (`findings_v2.py:291-298`). |
| C-003 | L2 | Hybrid / B | Hybrid 70 / Hybrid 70 | yes (after R2) | Hybrid | 70% | Shared card fields plus `requires_tools` and tool-keyed `search_forms`; no `extractor` field until one exists. |
| C-004 | L2 | B / B | B 80 / B 80 | yes | Variant B | 90% | Second output file keeps `review-precheck/1` byte-identical; `_check` reaches only v2 citations (`verify_cmd.py:133-143`); A conceded and withdrew its flags. |
| C-005 | L2 | Hybrid / Hybrid | Hybrid 60 / Hybrid 60 | yes | Hybrid | 60% | Per-module list: v1 loop cards + rows (wired after gates), tasklist/workflow via UC-1 v2, reflect UC-2 none, PR review and rf-qa reserved. |
| C-006 | L3 | Neither / B | Neither 75 / Neither 70 | yes (after R2) | Neither | 73% | The engine split is a C-01 outcome; `observed` is computed only where the v2 parser runs. |
| C-007 | L3 | Hybrid / Hybrid | Hybrid 75 / Hybrid 75 | yes | Hybrid | 75% | Code tests first (no model, no harness), A's per-class M1, B's compliance spike and four arms, M-B3 only if `apply` is planned. |
| C-008 | L2 | A / B | Hybrid 55 / Hybrid 55 | yes (after R2) | Hybrid | 55% | The leftover is B's carrier plus rowcheck (measurable), with A's per-class gate for extractors; A's loader-plus-card-text leftover equals arm K. |
| C-009 | L2 | B / Hybrid | Hybrid 60 / Hybrid 60 | yes (after R2) | Hybrid | 60% | Carrier now, extractors only after M1; size figures are planning values. |
| C-010 | L2 | A / A | A 60 / A 65 | yes | Variant A | 73% | CB-2 stays out of the core; `ledger.py:467-474` lists ledger rows only; B conceded its `ledger.py:468` route. |
| C-011 | L2 | Hybrid / Hybrid | Hybrid 55 / Hybrid 55 | yes | Hybrid | 55% | Script for reverse-dependency and whole-tree search over untrusted diffs, card text for lens wording. |
| C-012 | L2 | B / B | B 60 / B 60 | yes | Variant B | 60% | OK/UNSURE/missing to `[x]`/`[?]`/`[ ]` usable; equivalence untested (`rf-qa.md:484-511`). |
| C-013 | L1 | Neither / Neither | Neither 70 / Neither 60 | yes | Neither | 65% | `recipes` collides with `cli/swarm/recipes/`; keep `rows-v1` and `review-rowcheck/1`. |
| X-001 | L2 | Hybrid / Hybrid | Hybrid 70 / Hybrid 65 | yes | Hybrid | 68% | Script only for classes a script can decide (C4, C8) and only after M1; cards for the rest. |
| X-002 | L3 | A / Hybrid(leans A) | A 85 / A 85 | yes (after R2) | Variant A | 95% | No demotion or promotion in the core: measured 9.9 percent per quote failure, `ledger.py:99-104, 210-218`, no merge hook (`merge_cmd.py:71`); B conceded. |
| X-003 | L3 | A / Hybrid | A 70 / A 70 | yes (after R2) | Variant A | 80% | `ledger.py:3-4` is a status rule (both agree), but `ledger.py:210-213`, `SKILL.md:343`, C-02 and C-03's fail-closed choice support A's conclusion; B conceded. |
| X-004 | L2 | Hybrid / B | Hybrid 75 / Hybrid 70 | yes (after R2) | Hybrid | 73% | B's tool lint and tool-keyed forms now; A's script for C4 and C8 reserved. |
| X-005 | L3 | Hybrid / B | Hybrid 60 / Hybrid 65 | yes (after R2) | Hybrid | 63% | Uniform per-module binding now; slot-keyed binding reserved with golden test, `review-panel/1` hash decision and a name other than `recipes`. |
| X-006 | L2 | A / A | A 60 / A 65 | yes | Variant A | 73% | CB-2 outside the core; modules may print PROBLEM-without-finding rows or ask reviewers to copy them into follow-up candidates by brief text. |
| X-007 | L3 | Hybrid / B | Hybrid 60 / Hybrid 60 | yes (after R2) | Hybrid | 60% | B's row block over card- or script-derived items; hard consequence only for the empty report; `ran` unverified until C-08. |
| X-008 | L3 | A / A | A cond. 55 / A cond. 55 | yes | Variant A (conditional) | 55% | A's first gate needs no model but needs extractors (0 code) and ground truth (none built); B's needs a model; neither runs today. |
| X-009 | L2 | Neither / Neither | Neither 60 / Neither 60 | yes | Neither | 60% | Both size figures are planning values; no measurement settles it. |
| A-001 | L3 | Neither / Neither | Neither 80 / Neither 80 | yes | Neither | 80% | Both depend on X-14's harness; code tests need none, every effect claim does. |
| A-003 | L2 | Neither / Neither | Neither 80 / Neither 80 | yes | Neither | 80% | The v1 loop has no precheck/sidecar/cluster step (verified by absence); each is a new prose edit of a primitive. |
| A-004 | L3 | A / Neither | Hybrid 70 / Hybrid 75 | yes (after R2) | Hybrid | 73% | Script evidence restricted to snapshot paths by test; reviewer-typed `quote_other` outside the snapshot is `check_skipped` (472 of 510 flags are `not-in-snapshot`, re-run by both). |

Tally of winners over the 29 points: Variant A 5 (C-010, X-002, X-003, X-006, X-008), Variant B 4 (S-002, S-003, C-004, C-012), Hybrid 13 (C-001, C-002, C-003, C-005, C-007, C-008, C-009, C-011, X-001, X-004, X-005, X-007, A-004), Neither 6 (S-001, C-006, C-013, X-009, A-001, A-003), Unresolved 1 (S-004).

## Convergence Assessment
- Points resolved: 28 of 29 (Round 1: 17 of 29)
- Alignment: 96.55% (28/29)
- Threshold: 80%
- Gate results: diff-point gate PASS (96.55 >= 80); taxonomy gate PASS (L1, L2, L3 all covered); invariant-probe gate FAIL (2 HIGH UNADDRESSED: INV-001, INV-019)
- Status: BLOCKED_BY_INVARIANTS (agreement >= threshold and taxonomy covered, but HIGH-severity UNADDRESSED invariants exist; see `invariant-probe.md`; no Round 3 at depth=standard)
- Unresolved points: S-004 (diff point). Residual advocate disagreements inside the merged resolution that are not diff points: D-5 (row block on the v1 loop), D-6 (UNSURE counts as observed), D-7 (reflect step 5 edit under the frozen contract).
