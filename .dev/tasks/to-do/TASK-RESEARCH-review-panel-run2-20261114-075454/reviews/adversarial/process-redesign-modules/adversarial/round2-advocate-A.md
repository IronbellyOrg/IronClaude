# Round 2 rebuttal by the advocate for Variant A (slot X-13, process-redesign-modules)

Advocate: A (Sweep-Sheet-shaped). Round 2 of 2. Code state: HEAD 50d4d2b9d plus the working tree, read in this worktree on 2026-11-14.
Tags: [VERIFIED] = I read it this session at the cited path:line (or ran the cited command). [UNVERIFIED] = relayed from a variant, a research file or the opponent without my own read. [MY-ARITHMETIC] = a number I computed from verified counts. [DESIGN] = a choice, not a fact.
Files read in full first: round1-advocate-A.md, round1-advocate-B.md, diff-analysis.md, variant-1-original.md, variant-2-original.md. Code re-read this round: `ledger.py:1-30, 80-300, 455-475`; `findings.py:36-77, 88-122`; `findings_v2.py:140-305`; `merge_cmd.py:60-119`; `cluster_cmd.py:105-165`; `verify_cmd.py:1-185`; `panel.py:205-245, 655-700`; `agents/reflect-reviewer.md:1-70`; `rules/prompts/document_review_loop_prompts.md:14-75`; `skills/sc-reflect-protocol/SKILL.md:338-349`; `skills/sc-reflect-protocol/refs/reviewer-spec.md:30-79`. Searches: `verify-citations|review cluster|coverage.json|input-snapshot` over `src/superclaude`; `document_review_loop_prompts|review panel resolve|review merge` over `src/superclaude/**/*.md`; the same words inside `commands/spec-panel.md`; Glob of `cli/swarm/recipes/`. Commands run: one jq over the 29 `precheck.json` files and one jq over the 23 `coverage.json` files found under `.dev/` excluding `.dev/tasks/`.

## 0. Where I stand after Round 2

I keep the Round 1 hybrid and tighten it in four places where B's Round 1 or my own re-read showed a hole in A:

1. I withdraw A's own core part (c), the additive item-evidence flags in `precheck.json`. B is right that `verify_cmd._check` reaches only findings-v2 citations, and the script's own attached evidence has no one to check it. The only checkable object is a reviewer-typed quote, and that belongs in B's separate `review-rowcheck/1` file.
2. I accept B's reviewer-side row block as a record-only carrier, with one narrowing B did not state: at HEAD the "observed" list has a consequence only for an EMPTY findings block (section 2, point 8). A reviewer who writes one finding and zero rows passes. So the carrier gives a hard floor for the clean-report case only.
3. I give up one of my own arguments against demotion (`ledger.py:3-4` is a status rule, not a `blocking` rule) and replace it with stronger ones: `ledger.py:210-213`, the measured quote-failure floor, and the fact that a demoted row never reaches the Reviser brief (section 2, point 6).
4. I hold my ground on four points: no demotion or promotion in the core, no reviewer-side shell, no change to `_SLOT_KEYS` now, and CB-2 outside the core.

## 1. Steelman of B (short, since Round 1 has it)

B's best form: nothing has to be built before the review, `observed` becomes something the core computes from reviewer output, the second output file protects the pinned precheck bytes, and B ships concrete code-level tests. After Round 1 B itself reserves demotion and promotion behind a measurement. What is left between us is small: who produces the assigned items (a script for the mechanical classes, or only cards), and whether the names `apply` and a slot key are reserved in the schema now or in this document only.

## 2. Responses to every criticism B raised

### B section 4, weakness 1: A's "existing mechanism" for a no-finding item does not exist
ACCEPT. Same as my Round 1 concession 1. New evidence that narrows both sides:
- `findings_v2.py:291-298` consults `observed_rows` ONLY inside `if closed and not res["errors"] and not res["findings"]`. With one or more findings, assigned rows that were never observed raise no error (the loop at `:264-290` checks `coverage_rows` against `assigned`, never `observed`). [VERIFIED]
- So B's "hard floor" (B R1 strength 1) exists only for the clean-report case. A reviewer under B who writes one finding and no rows is valid and `rows_missing` is advisory. The same holds for A. The difference between us on C-002 and X-007 is therefore real but smaller than B's Round 1 reads: B supplies a reviewer-side source of `observed`; neither supplies enforcement in the non-empty case. [VERIFIED code, my reading]
- Recorded sidecars: in the 13 sidecars under `.dev/reflect/` that I counted, two (shadow07 and shadow15) have `observed` empty for all three reviewers, and three more have at least one empty entry (shadow03, shadow10, shadow14). The 10 sidecars under `.dev/eval-workspaces/shadow-model-combos/` have `observed` non-empty for every reviewer. [VERIFIED by my jq; this matches research/10 Unit 10's "2 of 13" for the first set; I did not re-check its "11 of 13 with a repeated row id".] The 10 full sidecars are what an orchestrator-written `observed` looks like (G2 of my Round 1): full, and proving nothing about the reviewer.

### Weakness 2: `verify_cmd._check` reaches only findings-v2 citations, so A's check has no v1 host
ACCEPT. `verify_cmd.py:133-143` parses cards with `fv2.parse_block` and loops `f.get("citations")`; its `--cards` help says "findings-v2 block" (`:82`). The spec loop's findings have `anchor`, not citations. Extra evidence B did not have: `verify-citations|review cluster|coverage.json|input-snapshot` appears in exactly 8 files under `src/superclaude`: reflect `SKILL.md`, five `cli/review` modules (`verify_cmd`, `cluster_cmd`, `cluster`, `manifest`, `manifest_cmd`, plus `card_convert`) and `sc-implement-protocol/refs/managed-workspace.md`. None is `commands/spec-panel.md` or `rules/prompts/`. And `review panel resolve|review merge` appears only in the reflect skill, `document_review_loop_prompts.md` and `commands/spec-panel.md`, where `spec-panel.md` has no such match inside it (its hits for "coverage" are unrelated persona text). So the v1 loop has no snapshot, no sidecar, no cluster and no precheck step anywhere. [VERIFIED by absence]
Consequence for A: part (c) is withdrawn. For the v1 loop any row check can compare `quote_plan` to the candidate file only (the candidate is the one file the loop always has); `quote_other` has no snapshot to be checked against in v1, so it is `check_skipped`.

### Weakness 3: A's per-reviewer assignment conflicts with "the same brief"
QUALIFY. `document_review_loop_prompts.md:70` says each reviewer runs "in a fresh context with the same brief" [VERIFIED]. True for the spec loop, and A's replica assignment (an item to 2 of 3 reviewers) cannot be used there. Two corrections to B's reading:
- A can give every reviewer the whole sheet in the loop: `assigned` is then identical for all reviewers, which obeys `:70`. I adopt that as the loop default.
- The reflect brief already breaks "same brief" by design: the persona excerpt is per reviewer (`reviewer-spec.md:37`) and `## Coverage slice` holds "only the rows this reviewer is responsible for" (`:63`) [VERIFIED]. So the rule is loop-specific. B's per-slot `recipes` has the same conflict in the loop whenever two slots carry different cards (B concedes this in its invariant 10). It is a tie, and uniform binding is the default for both.

### Weakness 3b: A's pre-pass reaches into a fenced brief ("exactly three sections")
QUALIFY. `reviewer-spec.md:33` says a reflect brief has exactly three sections and every addition so far sits as an entry inside an existing one (`:53, :55, :57, :59`) [VERIFIED]. For the reflect module A does not need a new section: the C2 item list is the requirement row list, which is what `## Coverage slice` already carries for UC-1 (`:63`). Script evidence for a mechanical class (C4, C8) would enter `## Grounding hunks` as `file:line` entries, which `:55-59` already do. I concede A did not say this. I also note `reflect-reviewer.md:59`: the brief "carries pre-computed evidence only ... MUST NOT instruct you to run anything" [VERIFIED]. Script-made items fit that sentence by construction. A recipe that tells the reviewer to search fits it only through the Read, Grep, Glob carve-out in the same sentence. B concedes the same (B R1 concession 10).

### Weakness 4: M1 is not as model-free as stated; the fallback has no value
ACCEPT in part.
- M1 measures selection recall only. Whether the reviewed text is retained beside each recorded report is still [UNVERIFIED]; I did not open the recorded runs for that.
- A's "degrades by construction" is a claim about harm, not value. If every class fails M1, A's leftover is a loader plus card text in the brief, which is B's arm K (a plain-words checklist) with a loader. I withdraw the wording that this leftover has value. The merged resolution (section 5) makes the leftover B's carrier plus rowcheck, which can be measured.

### Weakness 5: `ledger.py:3-4` is a status rule, not a `blocking` rule
ACCEPT the reading. `ledger.py:3-4`: "Only this module changes a finding's status; a reviewer's own prior lines are recorded as notes and never change one." [VERIFIED] It is about status. B is also right that `verify_cmd.py:10-12` governs the precheck only. My Round 1 use of both was by analogy.
What replaces it, all read this round:
- `ledger.py:210-213`: "The current report's classification decides: a defect a reviewer now keeps only as a warning or note no longer fails the review." The code makes the reviewer's current typed flag the authority over a row's `blocking`. [VERIFIED]
- `SKILL.md:343`: "The orchestrator never edits, remaps or normalizes a reviewer's findings itself." [VERIFIED]
- C-02's adjudicated outcome keeps typed `blocking` as the only authority (C-02 result, relayed in both Round 1 files).
- `findings.py:100-101` and `findings_v2.py:161-162`: both engines tie `blocking` to `severity` (v1: a MINOR finding cannot be blocking; v2 with `reflect_category`: blocking must equal severity not MINOR). [VERIFIED]
So my conclusion on X-003 stands on different grounds and I lower my confidence (section 4).

### Weakness 6: A loses found-at-blocking under CB-2, and nothing in A records an examined-and-clean item
ACCEPT the second half (it is weakness 1). On the first half A stays outside CB-2 in the core; the cost (a Medium defect confirmed through an item stays under follow-up candidates) is real and A reports found-at-any and found-at-blocking separately. A new point on B's route: B says a PROBLEM row without a finding is listed under follow-up candidates "by the report builder (non-blocking rows are already listed, `ledger.py:468`)". `ledger.py:467-474` prints `## Other findings` from `ledger["rows"]` where `not r["blocking"]` [VERIFIED]. A PROBLEM row with no finding is not a ledger row, so that code would not list it. B's route needs a new consumer; it is a module-level listing step, not an existing path. B's R1 does not address this.

### Weakness 7: per-class build and determinism burden
ACCEPT. It is the price; the unit of commitment is one extractor behind M1. This is why the merged resolution builds no extractor now.

### B's per-point positions where B and I differ
- C-002 / X-007 (B): I agree with B on the carrier (section 4), with the narrowing above.
- C-004 (B): agree; A's flags withdrawn.
- X-004 (B): B's `requires_tools` lint test is right and I adopt it. I keep that for C4 the Grep tool's dialect is ripgrep ("Ripgrep, not grep", the Grep tool description); B itself marks the equivalence [UNVERIFIED]. This is a cost B states, not hidden.
- X-005 (B): partly agree; see C-005 and X-005 in section 4.
- X-008 (A for B): B grants that my first gate needs no model. I accept B's limit: it needs extractors and ground truth that do not exist.

## 3. Checks of B's Round 1 claims where B contradicts A

1. "Whether the v1 spec loop has any precheck or sidecar hook." Verified none, see weakness 2. B is right, and A's Round 1 hedged this as [UNVERIFIED]; it is now [VERIFIED by absence] for `src/superclaude`.
2. "Whether an item can be answered through `coverage_rows` alone." No for an item with no defect: `coverage_rows` is a per-finding link (`findings_v2.py:166-176`) and `observed` is supplied by the caller (`findings_v2.py:196-212`). B is right.
3. "Whether A's pre-pass fits the loop's same-brief rule." Only with a uniform sheet (weakness 3). B is right for per-reviewer assignment, wrong that A cannot satisfy it.
4. "Whether B's overlay needs a merge hook." Yes. `merge_cmd.command` takes `ledger_path, doc, round_n, reports, resolution, out, cap` (`merge_cmd.py:71`) and hands raw report text to `led.merge_round` (`:109`), which parses it itself (`ledger.py:128`) [VERIFIED]. An overlay that lowers a typed flag needs a new option and a change inside `ledger.py`, or an edit of the report text, which `SKILL.md:343` forbids for reflect. B concedes this (B R1 concession 3). B's own `rowcheck: off | advisory | apply` has no host in code.
5. "Re-review resurrection" (B R1 concession 4). Verified: on a re-found row, `current = any(m["blocking"] ...)` replaces the row flag unless the row was already re-found in the same round (`ledger.py:213-218`). Extra mechanism that strengthens the point: `_brief_ids` lists only rows with `blocking` and status open or regressed (`ledger.py:99-104`). A row demoted in round 1 is not in the Reviser brief, so it is never repaired; it can return only if a round-2 reviewer happens to flag it again. [VERIFIED] The round-1 demotion of a true blocker is therefore permanent unless a reviewer rediscovers it.
6. "Sidecar key is the card stem" (B R1 concession 6). Verified: `rid = card.stem` (`cluster_cmd.py:146`). Together with `reviewer_id = f"{slot_id}-{i}"` (`panel.py:668`) and `--report REVIEWER_ID=PATH` (`merge_cmd.py:86-90`) there are three id spaces: resolution ids, v2 card stems (`reviewer-<N>`, `SKILL.md:345`) and v1 merge ids. A's Round 1 line "the sidecar already keys by `reviewer-<N>`" is true for v2 only; both designs need a mapping. [VERIFIED]
7. "`recipes` collides with `cli/swarm/recipes/`." Verified the directory exists with 8 modules (`findings_table_v1.py`, `bare_review_v1.py`, `verdict_only_v1.py`, `hypothesis_table_v1.py`, `passthrough.py`, `custom.py`, `_primitives.py`, `__init__.py`). B's quote of the `__init__.py` docstring is [UNVERIFIED by me]. If a slot key is ever built it must not be named `recipes`.
8. "A-004: 472 of 510 flags are not-in-snapshot." I re-ran it. Over the 29 `precheck.json` files outside `.dev/tasks/`: `checked` 1,047, `flagged` 510, by flag `missing-file` 472, `out-of-range` 7, `quote-not-found` 31, and 472 citations carry reason `not-in-snapshot`. [VERIFIED by jq] This confirms research/10 Unit 10 and B's use of it.
9. A new, measured number that bears on B's demotion: `_check` returns at `missing-file` and `out-of-range` before the quote test (`verify_cmd.py:46-67`), so the 31 `quote-not-found` come from at most 1,047 - 472 - 7 = 568 citations that reached it. 31 / 568 = 5.5 percent per quote, as a lower bound (citations without a quote are in the denominator). A row with two quotes would fail an exact test at about 1 - (1 - 0.055)^2 = 10.6 percent or more if the two failures are independent. [MY-ARITHMETIC; transfer from findings-v2 citation quotes of 12 to 200 characters to row quotes and short literal commands is an assumption.] That is a measured floor under the exactness risk B put at 16.5 percent from a planning figure.
10. "Narrowing of my Round 1 weakness 3" (demotion by flag alone invalid in v2). Scope correction: `findings_v2.py:161-162` binds `blocking` to severity only when `reflect_category` is set, which is the reflect case where B already sets `rowcheck: off`. In v1, `findings.py:100-101` rejects only a blocking MINOR; a non-blocking MAJOR line is valid. So in the spec loop, demotion by flag alone is a valid line. My weakness 3 holds for reflect and not for the loop. [VERIFIED]
11. "Placement: the row block after the findings block." The loop prompt says both "end the report with the findings block" (`:33`) and "The last section of every review report is `## Findings block` ... holding one JSON object per line and nothing else" (`:58`) [VERIFIED]. B's concession 2 cites only `:33`; `:58` also blocks an "after" placement in v1. In v2 an "after" placement has precedent: the brief appends a `reviewer_model_self_report` line after the block (`reviewer-spec.md:39`) and the orchestrator writes a fenced `yaml` calibration block after it (`SKILL.md:344`), both without touching the findings parse [VERIFIED]. And `_blocks_after` keeps only fences whose info string equals the requested one (`findings.py:73`) [VERIFIED]. So: before the findings block in v1, after it in v2, with B's T-B3 as the test for both.

## 4. Updated positions on the 29 points

Superior = A, B, Hybrid (named in a phrase) or Neither. CHANGED marks a change since Round 1 (position or confidence), with the reason.

### L1 points

| ID | Round 2 position | Conf. | Changed? | Reason |
|---|---|---|---|---|
| S-001 | Neither | 85 | no | Section order changes no behaviour. |
| S-002 | B | 60 | no | A numbered tag table is easier to audit. |
| S-003 | B | 60 | no | A closing "does not claim" section is a useful scope guard. |
| C-013 | Neither | 70 | CHANGED (75 to 70) | B's `recipes` collides with `cli/swarm/recipes/` (Glob, 8 modules); A's "no block named ledger" is satisfied by both. Name the key anything but `recipes`. |

### Higher-severity points

| ID | Round 2 position | Conf. | Changed? | Reason |
|---|---|---|---|---|
| S-004 | B | 65 | no | A preserved/endangered split with a consistency table is easier to check. |
| C-001 | Hybrid: A's card loader plus a card-to-sidecar writer, B's optional record-only row block and separate rowcheck file; no overlay, no slot key now, no part (c) | 70 | CHANGED (65 to 70, content) | I withdrew part (c); B's overlay is reserved and not built. |
| C-002 | Hybrid: script-made or card-made assigned items, answered through B's row block, `observed` computed from the parsed rows | 70 | no (claim narrowed) | The computed `observed` has a hard consequence only for an empty block (`findings_v2.py:291-298`). |
| C-003 | Hybrid: shared fields, B's `requires_tools` and tool-keyed `search_forms`, `extractor` optional | 70 | no | The lint needs `requires_tools`. |
| C-004 | B | 80 | CHANGED (75 to 80) | A second file keeps `review-precheck/1` byte-identical, and `_check` has no v1 object to check. |
| C-005 | Hybrid: spec loop = uniform cards plus row block, advisory; tasklist via reflect UC-1 = items are the Coverage slice rows plus rows, extractors only where M1 passes; reflect UC-2 = off; PR review and rf-qa = reserved | 60 | CHANGED (55 to 60) | Verified that the v1 loop has no hook (weakness 2); verified the Coverage slice is the existing host. |
| C-006 | Neither | 75 | no | The engine split comes from C-01; computed `observed` exists only where the v2 parser runs. |
| C-007 | Hybrid: B's code tests T-B2, T-B3, T-B5, T-B6 plus A's byte-identity test, A's M1 per class, B's M-B1 and M-B2 arms; M-B3 only if `apply` is ever planned | 75 | CHANGED (70 to 75) | The code tests need no model and no harness; I now rank them first. |
| C-008 | Hybrid: B's carrier plus rowcheck as the leftover, A's per-class gating for extractors | 55 | CHANGED (A, 65 to Hybrid, 55) | B showed that A's leftover is a loader plus card text, which is arm K. The merged leftover is measurable. |
| C-009 | Hybrid: carrier now, per-class extractors only after M1 | 60 | CHANGED (B, 55 to Hybrid, 60) | Without the overlay and the renderer B's build is smaller; extractors are unbuilt either way; line counts are [PLANNING]. |
| C-010 | A | 60 | no (refined) | CB-2 stays out of the core; B's `ledger.py:468` route lists a different set; PROBLEM rows without a finding are listed in the rowcheck file and a module may print them, with no promotion. |
| C-011 | Hybrid: script for reverse-dependency and whole-tree search over untrusted diffs, card text for lens wording | 55 | no | `codegraph_callers` is in the reviewer allowlist (`reflect-reviewer.md:5`), so either place works. |
| C-012 | B | 60 | no | OK, UNSURE, missing to `[x]`, `[?]`, `[ ]` is a usable checklist output; the `rf-qa.md:484-511` lines are [UNVERIFIED by me]. |
| X-001 | Hybrid: script only for the classes a script can decide (C4, C8) and only after M1; cards for the rest | 70 | no | Matches research/10 Unit 7's mechanical column; B also lands here. |
| X-002 | A | 85 | CHANGED (80 to 85) | New grounds: measured floor of 5.5 percent per quote (section 3, point 9), resurrection plus absence from the Reviser brief (point 5), no merge hook (point 4). One Round 1 ground narrowed (point 10). |
| X-003 | A | 70 | CHANGED (80 to 70) | `ledger.py:3-4` is a status rule. Remaining grounds: `ledger.py:210-213`, `SKILL.md:343`, C-02, the fail-closed asymmetry. |
| X-004 | Hybrid: script for mechanical searches, B's tool lint for any card left | 75 | no | Removes the Bash dependency for C4 and C8 and pins it by test. |
| X-005 | Hybrid: uniform card binding per module by default, no `_SLOT_KEYS` change now; a `slot_id`-keyed binding reserved with a golden resolution test, a decision on `review-panel/1`, and a name other than `recipes` | 60 | no (refined) | `_SLOT_KEYS` rejects unknown keys (`panel.py:214-216`); `SKILL.md:340` requires the resolution to be the unmodified output; uniform binding keeps the loop's same-brief sentence. |
| X-006 | A | 60 | no | CB-2 outside the core; see C-010. |
| X-007 | Hybrid: B's record-only row block over A's items | 60 | CHANGED (65 to 60) | Its hard consequence is only the empty-report case; `ran` is unverified until C-08. |
| X-008 | A (conditional) | 55 | CHANGED (65 to 55) | A's offline gate needs extractors (0 code) and ground truth (none built); B's first gate needs a model. Neither is runnable today. |
| X-009 | Neither | 60 | no | Both size figures are [PLANNING]; no measurement settles it. |
| A-001 | Neither | 80 | no | Both need X-14's harness. |
| A-003 | Neither | 80 | CHANGED (75 to 80) | Verified: the v1 loop host has no precheck or sidecar step (section 2, weakness 2). |
| A-004 | Hybrid: script evidence restricted to snapshot paths by test; reviewer-typed `quote_other` is `check_skipped` when outside the snapshot | 70 | CHANGED (A, 60 to Hybrid, 70) | I re-ran the counts (472 of 510); B's `check_skipped` rule is needed and A's by-construction rule covers script evidence. |

## 5. The merged resolution I can defend

Numbered so that agreement and disagreement are explicit.

### Built now (all optional; with nothing declared the run equals today's run by hash)
1. Card file format and loader with a validator. Module data only; fields as MR2 3.0.3 relayed by research/10 Unit 5, plus `requires_tools` and tool-keyed `search_forms`; `extractor` optional. No class constant in core; the `findings_v2.py:36-48` vocabularies stay untouched. Both advocates agree.
2. A card-to-sidecar writer: one CLI entry point that writes `<output>/panel/coverage.json` `{assigned, observed}` entries from the module's cards, with one entry per card including `{}`, and with a mapping between resolution ids, card stems and v1 merge ids (section 3, point 6). It fills `assigned` only. Agreement.
3. The row block, record-only: a fenced block with its own info string (name subject to the collision rule), one row per assigned item: id, verdict OK, PROBLEM or UNSURE, optional `quote_plan`, `quote_other`, `problem`, `ran`. `observed` is computed by parsing it and is never declared by an orchestrator. Placement: before the findings block in v1 (loop `:33, :58`), after it in v2 (`reviewer-spec.md:39`, `SKILL.md:344`). A truncated row block never invalidates a complete findings block. Agreement on the carrier; the placement split is mine.
4. The row check as a separate output file `review-rowcheck/1`, advisory only. It reuses `verify_cmd._norm` and the `in` test through one shared function, not a copy. `review-precheck/1` and `reread_set` stay byte-identical. `check_skipped` for a quote that is a printed tool line, a path outside the snapshot, or any `quote_other` in the v1 loop (no snapshot). In v1 only `quote_plan` against the candidate is checked. It changes no flag, status or verdict. Agreement.
5. Counts-only telemetry (ids and counts: items assigned, items observed, rows problem, rows unsure, rows missing, item-linked findings) and a test that no telemetry record serialises quote or `problem` text. Agreement.
6. Binding: uniform per module by default. Every slot gets the same cards, so the loop's "same brief" sentence (`:70`) and `_SLOT_KEYS` hold. The sheet for the loop is the whole sheet for every reviewer. Reflect assigns per reviewer through the Coverage slice, which already does this.
7. Tool wall: no card may require a tool outside the bound agent's allowlist (`reflect-reviewer.md:5`); a test fails otherwise (B's T-B5). A class whose only form needs a shell is not bound to a read-only agent.

### Reserved (named in this document only, not built, no schema key)
8. A `slot_id`-keyed card binding, with a name that is not `recipes`, built only when a module needs different cards per slot, with a golden test of the resolution output and an explicit decision on the `review-panel/1` hash.
9. Script extractors per class (C4 and C8 first, listers for C2 and C5): built one at a time, each behind its own M1 pass; C1, C3, C7 stay card text.
10. A cross-check of `ran` against transcript tool calls (the C-08 adapter).
11. The `rowcheck: apply` profile value, i.e. demotion and promotion. I would not even reserve a schema key: nothing would read it and it has no host in `merge_cmd` or `ledger.merge_round`. B reserves the name; this is the one place where we still differ on mechanics (section 6, D-3).

### Not built
12. Demotion and promotion in the core. CB-2 inside the core. Any change to findings-v1 or v2, `review-ledger/1`, `derive_verdict`, reflect contract 1.8.0 or its 36-test matrix. Any reviewer-side shell. Any class constant in core.

### Gates
13. G-0, code level, no model, no harness: slot-key rejection unchanged (T-B2); a row fence leaves `findings.parse_block` and `findings_v2.parse_block` results identical, including `ok` and `state` (T-B3); card-to-tool lint (T-B5); telemetry test (T-B6); no-cards byte identity by hash of the brief, the loop prompt file and `coverage.json`; `review-precheck` golden bytes unchanged; sidecar writer rejects a duplicate id inside one reviewer and a range token; extractor determinism where one exists. (B's T-B1 as "golden rendered briefs" has nothing to hash, because no brief renderer exists in `cli/review`; B concedes this. It becomes a golden test of the resolution output plus a pin of the loop prompt file.)
14. G-1, per class, offline: recall at a floor frozen before the run and above a random pick (A's M1). Needs ground truth and X-14's rule.
15. G-2: B's compliance spike (rows missing plus invalid rows at or below a pre-registered rate).
16. G-3: B's arms Z0, K, RL, SS on one ground truth; RL must beat K by the pre-registered margin or K wins; SS counts only for classes that passed G-1.
17. G-4: B's M-B3 before any `apply` is built, plus three prerequisites: per-row persistence across rounds (section 3, point 5), a merge hook (section 3, point 4) and a severity rewrite for v2 reflect findings (section 3, point 10).

### What each module does
18. Spec review loop (v1): uniform cards; row block before the findings block; rowcheck advisory on `quote_plan` against the candidate; one new prose step in the loop host (`document_review_loop_prompts.md` and `commands/spec-panel.md`), which is an edit of a primitive, not an engine hook. The item link on a finding is an open key; `review-ledger/1` copies only round, reviewer id, finding id and `blocking` into `members` (`ledger.py:172-179`), so any per-item metric reads raw reports.
19. Tasklist and workflow via reflect UC-1 (v2): the items are the Coverage slice rows; C4 and C8 are the first extractor candidates; row block after the findings block; sidecar `assigned` from the existing requirement rows, `observed` from the parsed rows.
20. Reflect UC-2: no cards in any packaged template; the result is byte-identical.
21. PR review and rf-qa: reserved. Reverse-dependency and whole-tree search run in a script for untrusted diffs; OK, UNSURE and missing map to `[x]`, `[?]`, `[ ]` as a design inference.

## 6. Disagreements that remain, and the evidence that would settle each

- D-1: does the row duty crowd out the free review (A-002)? Settled by G-2 and the Z0 versus RL arms.
- D-2: do script-built items beat card-derived rows on C4 and C8? Settled by G-1 and the SS versus RL arms.
- D-3: reserve `apply` in the schema (B) or in this document only (me)? Nothing can settle it before G-4; the cost of my choice is a later schema decision, the cost of B's is a key with no reader.
- D-4: placement per engine. Settled by T-B3.
- D-5: is a row block in the v1 loop worth its cost when `observed` is not computed there and no snapshot exists? Settled by G-2 on the loop.

## 7. Round 2 responses to A-001, A-003, A-004

- A-001 (a harness, ground truth and the pre-registration rule exist): QUALIFY, unchanged. The code tests of G-0 need none of them; every effect claim needs X-14.
- A-003 (every coordinator can host one more deterministic step without a new engine hook): REJECT as stated, changed from QUALIFY. Advisory steps need no ENGINE hook, but the spec loop has no precheck or sidecar step at all (verified by absence), so each such step is a new prose edit of `document_review_loop_prompts.md` or `commands/spec-panel.md`. The INV-N mirror pins B names are [UNVERIFIED by me]. A step that alters merge input needs a change in `merge_cmd` and `ledger.merge_round` (point 4 of section 3).
- A-004 (cited evidence lies inside the input snapshot): REJECT for reviewer-typed quotes, changed from QUALIFY; ACCEPT for script-attached evidence made true by construction and a unit test. Recorded data: 472 of 510 flags are `not-in-snapshot` (I re-ran it). The v1 loop has no snapshot at all.

## 8. Invariants the consensus still leaves open

1. HIGH. Computed `observed` has a consequence only for an empty findings block (`findings_v2.py:291-298`); one finding plus zero rows is valid. The consensus must not claim that a row block proves examination, and must say who reads `rows_missing`.
2. HIGH. Three reviewer-id spaces (`panel.py:668`, `cluster_cmd.py:146`, `merge_cmd.py:86-90`) with no mapping. A mismatch gives `assigned = None`, which makes every empty block invalid (`findings_v2.py:292`) and makes `verify-citations` stop when an entry is missing (`verify_cmd.py:125-128`).
3. HIGH if `apply` is ever built, otherwise MEDIUM. A demoted row is absent from the Reviser brief (`ledger.py:99-104`) and is recomputed from typed flags on a re-find (`ledger.py:213-218`); a demoted true blocker is never repaired.
4. HIGH. Exactness: at least 5.5 percent per quote fails the normalised substring test on recorded data (section 3, point 9). Any consequence of a failed row quote needs this number measured on row data first; the check stays advisory.
5. MEDIUM. Placement of the row block against the loop prompt's `:33` and `:58`, and the truncation rule (a truncated row block must not invalidate a complete findings block).
6. MEDIUM. Row quote length: findings-v2 citation quotes are 12 to 200 flattened characters (`findings_v2.py:79-80`, relayed from my Round 1 read); a short literal pattern is below 12, so rows need their own limit and a rule for over-length.
7. MEDIUM. Who writes `observed`. The 10 combo-run sidecars all have full `observed`; it must come only from parsed rows.
8. MEDIUM. Compliance feeds the quorum arithmetic through the empty-block rule: a clean reviewer who skips rows is counted lost by C-03's floor, while `merge_round` refuses only when no reviewer has a valid block (`ledger.py:150-157`). State that this is the intended and only hard consequence.
9. MEDIUM. The v1 loop needs a new prose step; edits to `document_review_loop_prompts.md` and `commands/spec-panel.md` need change control (the pins are [UNVERIFIED]).
10. MEDIUM. The slot-key name must not be `recipes`; a binding key changes the template hash and the resolution that `SKILL.md:340` requires to be unmodified.
11. MEDIUM. Extractor determinism (directory order, locale, `git grep` order) pinned by tests, or G-1 is meaningless.
12. LOW. Zero items, one item and the cap (12 in E2, [UNVERIFIED]) each need a fixture.
13. LOW. Line bases differ by engine (C-01 INV-009); script-attached spans must use the checking engine's base.
14. LOW. Telemetry cleanliness is a convention (`telemetry.py:3`) and needs T-B6 to hold.
15. LOW. rf-qa mark mapping is a design inference, not a tested equivalence.

Not re-read, relied on as relayed [UNVERIFIED]: MR2 text, research/05, 06, 13, 16, slice 06, synth-05 and synth-06 rows, `rf-qa.md:484-511`, the `cli/swarm/recipes/__init__.py` docstring, INV-N mirror pins, `telemetry.py:243-251`, the "11 of 13 sidecars with a repeated row id" count, all [PLANNING] numbers.

Status: Complete
