# Round 2.5 invariant probe (fault-finder): slot X-13, process-redesign-modules

Agent: independent fault-finder (not an advocate). Code state: HEAD 50d4d2b9d plus working tree, read 2026-11-14.
Read first, in full: diff-analysis.md, round1-advocate-A.md, round1-advocate-B.md, round2-advocate-A.md, round2-advocate-B.md, variant-1-original.md, variant-2-original.md. Sibling results read: core-shape-and-finding-contract, ledger-clearing-and-verdict-authority, merge-verdict-policy-and-quorum (ADJUDICATION-RESULT.md).
Code and tests re-read for this probe (read-only): `cli/review/findings.py:26-27, 38-196, 272`; `findings_v2.py:51-81, 84-304`; `verify_cmd.py` (all); `cluster_cmd.py:20-190`; `cluster.py:184-232, 380-424`; `merge_cmd.py:55-119`; `ledger.py:80-300, 440-490`; `panel.py:46, 189-216, 595-707`; `manifest.py:9-13, 97-130, 275-325`; `telemetry.py:1-120, 196-281`; `reflect/panel_lint.py:170-340`; `skills/sc-reflect-protocol/SKILL.md:300-349`; `refs/reviewer-spec.md:25-84`; `rules/prompts/document_review_loop_prompts.md:10-75`; tests `tests/review/test_review_rules_text.py`, `tests/skills/test_review_brief_placement.py`, `tests/skills/test_review_prompt_overrides.py:100-230`, `tests/cli/reflect/test_shadow_skill_contract.py:38-175`.
Own measurement (jq over the 23 `coverage.json` files under `.dev/`, `.dev/tasks/` excluded): 69 reviewer entries; largest `assigned` list 48 (comboE-r2 reviewer-2), 21 of 69 entries above 12 rows; 2 entries whose `observed` is not a subset of `assigned`; id shapes are 667 `INF-N`, 23 `FR-N`, plus free slugs (`verification-honesty`, `PRN/N-evolution`) and one range token (`INF-N..INF-N`).
Rule applied: ADDRESSED only when the consensus text itself handles the point; an advocate listing it as open is UNADDRESSED.

## Category 1: state variables

ID: INV-001
CATEGORY: state_variables
ASSUMPTION: The consensus says `observed` is "computed only from parsed rows" by the new entry point, so the sidecar has one writer. The reflect skill still tells the orchestrator to write `panel/coverage.json` itself, with `observed` as "the rows its card reports", and D-7 names only a step 5 edit. Two writers exist in the prose; the orchestrator is a model following that prose, so the older instruction can win and the "clean report is valid only if every assigned row is observed" floor then rests on whatever it wrote.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: SKILL.md:345 (step 6: "first write `<output>/panel/coverage.json` ... the rows its card reports"); round2-advocate-B section 4.1 (iii) and D-7 (edit named: step 5 only); round2-advocate-A section 5 item 2 says the writer "fills `assigned` only" while B's component 3 also computes `observed` (the two Round 2 lists disagree and the lead summary takes B's form without saying so). `findings_v2.py:196-212, 291-298` (observed is whatever the caller supplies). Recorded orchestrator-written sidecars are already inconsistent: 2 of 69 entries have `observed` outside `assigned` (comboA-r2 reviewer-2: 17 assigned, 18 observed; shadow13 reviewer-1: 3 assigned, 2 observed, both outside). Edit is permitted by `tests/cli/reflect/test_shadow_skill_contract.py:52-75` (steps 4-6 sit under section 4.3a), so it is possible but is not in any component list.

ID: INV-002
CATEGORY: state_variables
ASSUMPTION: The rows the entry point parses are the reviewer's own words. In reflect the file it would read is `panel/cards/reviewer-<N>.md`, which the orchestrator assembles (header lines, the card's Findings block, a yaml calibration block); getting the row block there needs the D-7 "verbatim copy" prose edit. The copy is made by a model, so a dropped, merged or invented row changes `observed`. The raw reviewer card is a different file with a different stem.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: SKILL.md:343-344 (step 4 "orchestrator never edits ... a reviewer's findings"; step 5 "write `panel/cards/reviewer-<N>.md` ... that card's `## Findings block`, then a fenced yaml block"); `panel_lint.py:188, 273` (legacy cards are `reviewer-cards/reviewer-<N>-card.(yaml|yml|md)`, a fourth reviewer-id space beside `t1b-1` (`panel.py:668`), `reviewer-<N>` (`cluster_cmd.py:146`) and any `--report` id (`merge_cmd.py:86-94`)). round2-advocate-B section 4.1 (iii) names the copy as a prose edit but not the fidelity risk; round2-advocate-A did not price it. Fix that fits the consensus: the entry point parses the raw card path, never the copy.

ID: INV-003
CATEGORY: state_variables
ASSUMPTION: (Advocate-listed: A R2 section 8 item 2, B R2 section 9 item 2.) Three reviewer-id spaces and a missing sidecar entry: a mismatch gives `assigned = None`, which makes every clean block invalid and makes `verify-citations` stop while `cluster` degrades silently.
STATUS: ADDRESSED
SEVERITY: HIGH
EVIDENCE: Consensus component 3 text: "one entry per card including `{}`, with an id map between resolution ids, card stems and --report ids". Re-read: `verify_cmd.py:124-128` (stops when the entry is missing), `findings_v2.py:202-203` (`(None, [])` for no entry), `findings_v2.py:292` (`not rows` makes a clean block invalid), `cluster_cmd.py:146-151` (silent degrade). The text covers the three spaces it names; the fourth (legacy `-card` stem) is INV-002.

ID: INV-004
CATEGORY: state_variables
ASSUMPTION: A clean report becomes valid once its rows are observed, and a reviewer whose block is invalid gets "one bounded re-ask for the block only". Step 4 parses the card (and decides the re-ask and the first-pass `findings_block_compliance_rate`) before any coverage sidecar exists; step 6 is the first place the sidecar is written. The consensus does not say the new entry point runs before step 4, so a compliant clean reviewer is judged invalid, re-asked and counted as a first-pass failure while the sidecar is still empty.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: SKILL.md:343 (step 4: parse, record `findings_block_compliance_rate` "on this first parse ... before any re-ask") vs SKILL.md:345 (step 6 writes the sidecar); `findings_v2.py:291-298` (empty block needs assigned non-empty and all observed); `cluster_cmd.py:117` help ("Without it a card with no findings ... is listed invalid"). Same ordering gap exists at HEAD for clean cards; the consensus claims to make that path valid and does not move the writer.

ID: INV-005
CATEGORY: state_variables
ASSUMPTION: Rows and the second file are a first-review mechanism ("apply the process to the first review only"). The entry point writes fixed paths `panel/coverage.json` and `panel/rowcheck.json` with no round or review-kind argument, so a coordinator that runs it again after a re-review overwrites the round 1 evidence and, with uniform binding, assigns rows to a re-review reviewer who was never asked for them (`rows_missing` for every row).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `panel.py:600-605` (re-review expands no slots; `review_kind` not in `apply_to` gives one fixed reviewer), `panel.py:697` (the resolution records `review_kind`); `merge_cmd.py:71` (round is an input to merge, none to the new writer); `cluster_cmd.py:180` / `verify_cmd.py:174` (existing outputs also overwrite in place, so this is a pattern, but those carry no round-1-only duty). Neither Round 2 file gives the entry point a `--kind` guard; the G-2 and G-3 measurements read these files, so an overwrite also destroys measurement input.

## Category 2: guard conditions

ID: INV-006
CATEGORY: guard_conditions
ASSUMPTION: Row ids are short copyable strings that the row parser, the sidecar and `coverage_rows` all accept. The consensus defines no row-id grammar or type rule. Recorded ids are not uniform, and the one hard guard downstream aborts a whole command on a bad type.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Own jq over 23 sidecars: 667 `INF-N`, 23 `FR-N`, slug ids `verification-honesty` (20 chars) and `PRN/N-evolution` (contains `/`), and a range token `INF-N..INF-N`. `findings.py:26` finding-id grammar allows 16 characters and no `/` (not applied to rows today, so a row grammar must be chosen). `findings_v2.py:206-211`: a non-string in `assigned` or `observed` raises ValueError, which `cluster_cmd.py:148-150` and `verify_cmd.py:130-132` turn into a ClickException for the whole run, not one card. `findings_v2.py:262` maps assigned ids with `str` but `:292` compares them with `set(observed_rows)` unmapped, so an int row id (`{"row": 1}`) and an assigned `"1"` never match. Advocate lists name range tokens and duplicates (A R1 S1) but the consensus text states no rule.

ID: INV-007
CATEGORY: guard_conditions
ASSUMPTION: The check rules are implementable from the row fields. The consensus row has `row id, class, verdict, quote_plan, quote_other, problem, ran`, yet the rules say `quote_other` is checked "only against snapshot paths" and that "tool-line quotes" and "out-of-snapshot paths" are `check_skipped`. No row field carries the path or the quote kind, so the checker cannot decide snapshot membership or skip the right rows without inventing a field or scanning every snapshot file (which passes any quote that appears anywhere). `ran` has no bound or type, and nothing says whether the row parser accepts unknown keys, although C-01 left them open for findings.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: round2-advocate-B section 6 components 2 and 4 (field list and rules); `verify_cmd.py:42-48` (a citation needs a `path` to be tested against the snapshot; no path gives no verdict); `findings.py:79-87` (`_check_flat` bounds exist for findings text, none stated for `ran`); core-shape-and-finding-contract ADJUDICATION-RESULT (unknown keys open in both finding parsers; says nothing of a third parser). Recorded data: 472 of 510 flags are `not-in-snapshot`, so for `quote_other` the skipped branch is the common branch.

ID: INV-008
CATEGORY: guard_conditions
ASSUMPTION: (Advocate-listed: B R2 D-6 and section 9 item 7.) UNSURE counts as observed. The guard compares ids only, so an all-UNSURE clean report passes. The consensus leaves D-6 open.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: `findings_v2.py:291-298` consults the presence of ids only. An all-OK block with no quotes passes equally and has nothing for `rowcheck` to test (quotes are optional), and both advocates already concede rubber-stamping (A R2 section 8 item 1), so UNSURE-as-observed adds no bypass beyond that one; the cost is only that `rows_unsure` is visible in telemetry alone. LOW because the decision changes a counter, not a verdict.

## Category 3: count divergence

ID: INV-009
CATEGORY: count_divergence
ASSUMPTION: `assigned`, `observed`, `rows_total`, the module row cap and the "12" of E2 describe one consistent quantity. They do not. The row cap is "set by the module" (B component 2) and E2's 12 is [UNVERIFIED]; recorded per-reviewer slices are much larger; the empty-block rule needs every assigned row observed, so any cap below the assigned count makes a clean report unsatisfiable. `observed` computed from parsed rows can also exceed or fall outside `assigned`, and uniform binding replicates every card row across all reviewers.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Own jq: 69 reviewer entries, 21 with more than 12 assigned rows, maximum 48 (comboE-r2 reviewer-2, 48 observed of 48), 43 in comboD-r2; 2 entries with `observed` not a subset of `assigned`. `findings_v2.py:292` (`rows <= set(observed_rows)`: extras are ignored by the guard but a length-based `rows_missing = assigned - observed` goes negative for comboA-r2 reviewer-2, 17 vs 18). Uniform binding (consensus item 6) gives N reviewers the same rows, so telemetry "items assigned" is N times the unique count unless the unit is stated (A R1 D1, B R1 invariant 6: both listed, neither resolved). Needed rules: observed is the intersection with assigned, extras are counted separately, the loader rejects a module whose assigned count exceeds the cap, rows_total names its unit.

ID: INV-010
CATEGORY: count_divergence
ASSUMPTION: A row quote of 12 to 200 flattened characters is checked the way a citation quote is. Three boundaries disagree. (1) `quote_plan` needs 12 flattened characters, but the classes with a mechanical test (C4, C8) quote short literals, so those rows are invalid and unobserved. (2) The rule tests `quote_plan` against the whole candidate, while the 5.5 percent and 9.9 percent failure figures were measured with a line window; a 12-character fragment found anywhere in a long spec passes, so the check mostly detects fabricated text, not misplaced evidence. (3) `quote_other` is "at most 200 and checked only when 12 or more", so a short one is silently unchecked while a short `quote_plan` is an error.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `findings.py:79-87` (`_check_flat`: flattened length, minimum and maximum inclusive); `findings_v2.py:79-80` (citation quote 12 to 200); `verify_cmd.py:68-72` (quote tested against `lines[line_start-1:line_end]`, not the whole file); round2-advocate-A section 3 point 9 and round2-advocate-B section 2 item d (the 5.5 and 9.9 percent figures; both note the transfer to rows is an assumption, neither notes the window difference); round2-advocate-B section 6 component 2 (limits) and component 4 (whole-candidate rule). A and B R2 invariant lists name the 12-character minimum (A item 6, B item 11); the consensus fixes it only for `quote_other`.

ID: INV-011
CATEGORY: count_divergence
ASSUMPTION: (Advocate-listed: A R2 section 8 item 8, B R2 section 3.1 row 7.) Compliance feeds quorum arithmetic only through the empty-block rule. The consensus does not state that this is the intended and only hard consequence, and the paths differ by engine. v1: rows never reach `block_ok`, except that a row block placed before the findings block lengthens the report in front of the one block the merge needs, so truncation raises the chance of the zero-valid-block refusal and of C-03's `min(2, requested)` floor. v2: a clean reviewer without rows is `invalid`, drops out of `complete_reviewers`, and `cluster_agreement` becomes None below two complete reviewers. The first-pass `findings_block_compliance_rate` also changes meaning against the recorded shadow baseline.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `ledger.py:128-157` (`fnd.parse_block` only; refusal when no reviewer has a valid block); `findings.py:151-158` (unclosed findings fence is not ok); `cluster.py:218-221, 386, 405-406` (valid only when state is complete; fewer than 2 complete gives None); SKILL.md:343 (first-parse metric); merge-verdict-policy-and-quorum ADJUDICATION-RESULT (floor `min(2, requested)`, INV-006 union over invalid-block reviewers). Size of the added text: 48 rows at the minimum row size is a few KB in front of the block (v1 placement), far above the 12-row figure the advocates used.

ID: INV-012
CATEGORY: count_divergence
ASSUMPTION: (Advocate-listed: A R2 section 8 item 13, A R1 D3.) Line bases differ between engines (0-based half-open in v1, 1-based inclusive in v2) and script-attached spans must use the checking engine's base.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: Not triggered by the built-now set: script extractors are reserved with no schema key (consensus "Reserved"), and the only built-now text test is a whole-file substring with no line numbers. `findings.py:276-278` (`locate` 0-based half-open) vs `findings_v2.py:76-78` (citation lines 1-based). The length bounds do agree across engines (`findings.py:79-87`, `findings_v2.py:79-80`).

## Category 4: collection boundaries

ID: INV-013
CATEGORY: collection_boundaries
ASSUMPTION: Zero cards, a reviewer with no card, and the `{}` entry behave as today. The consensus handles these: no cards declared means no sidecar and today's run by hash; the writer emits one entry per card including `{}`; G-0 fixtures cover 0, 1 and N rows.
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Consensus items (1), (3) and the G-0 list; `cluster_cmd.py:138-140` and `verify_cmd.py:115-117` iterate only existing cards, so a lost reviewer has no card and no entry; `verify_cmd.py:125-128` and `findings_v2.py:202-203` (the entry rule). Residual that stays as at HEAD: a carded reviewer with no bound cards gets `{}`, so a clean report is invalid (`findings_v2.py:292`, `not rows`).

ID: INV-014
CATEGORY: collection_boundaries
ASSUMPTION: A card yields a definite list of row ids, the loader has a defined outcome for a bad card, and a row block holds each id at most once. None of the three is specified. The consensus card fields (id, name, version, definition, recipe text, question template, route, applies_to, instances, known weakness, `requires_tools`, `search_forms`) contain no step or row list, so what `assigned` holds per card (one row per class, one per step) is undefined; both Round 2 files say "assigned from bound cards" without the rule. A loader that skips an invalid card silently shrinks `assigned`; one that fails aborts the review. Two rows with the same id and different verdicts have no stated winner, while both finding parsers reject duplicate ids.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: round2-advocate-B section 6 components 1 and 3; round2-advocate-A section 5 item 1 (card fields "as MR2 3.0.3", [UNVERIFIED] text); `findings.py:94-95` and `findings_v2.py:101-102` (duplicate id rejected for findings); `verify_cmd.py:125-128` (a missing entry stops the run, so an inconsistent writer is loud for one command and silent for the other). Fixtures for zero, one and N rows (B R2 component 2) do not cover duplicates or an invalid card.

## Category 5: interaction effects

ID: INV-015
CATEGORY: interaction_effects
ASSUMPTION: Wiring the v1 loop is "one new prose step in `document_review_loop_prompts.md` and `commands/spec-panel.md`" (A R2 item 18; the INV-N mirror pins were marked [UNVERIFIED] by both advocates). The pins exist and they contradict the file list. The command file may not carry prompt text or procedure; the plugin bundles a byte copy of the rules file; the insertion order and the "last section" sentence are pinned.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `tests/skills/test_review_brief_placement.py:73-103` (the `/sc:spec-panel` gate paragraph must be one sentence that restates nothing; forbidden words include "evidence" and "Step 1"), `:129-138` (`plugins/superclaude/rules/prompts/document_review_loop_prompts.md` must equal the source file byte for byte); `tests/review/test_review_rules_text.py:34-43` (the line after the First-review brief must be exactly the findings-block line), `:65-73` (pins "The last section of every review report is `## Findings block`"); `tests/skills/test_review_prompt_overrides.py:110-113` (shipped briefs must pass `lint_brief`). So the v1 edit is the rules file plus its plugin twin, not `spec-panel.md`; a row block before the findings block is compatible with the pinned sentence only if the added instruction says the findings block stays last.

ID: INV-016
CATEGORY: interaction_effects
ASSUMPTION: "No verdict changes" and "no cards declared equals today's run by hash". (a) In shadow mode dispatch is the legacy dispatch with the legacy brief plus one line, and the card body still reaches the legacy debate; a per-row duty added to that brief changes the output of the reviewers whose reports are authoritative, so non-interference holds for code but not for the behaviour being measured. (b) The manifest freezes the sha256 of `refs/reviewer-spec.md` as a policy input, so any edit to that file changes `policy_sha256` for runs that declare no cards, and a resumed frozen run conflicts. (c) The reviewer brief already says to end the card with the Findings heading and then add a `reviewer_model_self_report` line; a row block "after the block" has no stated order against that line.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: SKILL.md:338 (shadow adds no verdict), :342 ("Briefs are the legacy briefs plus the one findings-block instruction line ... Dispatch is the legacy dispatch"), :343 (card body reaches the debate), :340 (`--brief-template-sha256 <sha256 of refs/reviewer-spec.md>`); `manifest.py:97-104, 231` (policy hash includes the brief template hash and is checked); reviewer-spec.md:39 (end-of-card wording and the self-report line); `tests/cli/reflect/test_shadow_skill_contract.py:146-165` (the excerpt must keep the findings-v2 text and the self-report phrase; three sections only). B R2 D-7 cites `panel_lint` and the 36-test matrix as the gate; those tests do not pin SKILL.md or reviewer-spec.md text.

ID: INV-017
CATEGORY: interaction_effects
ASSUMPTION: "Counts-only telemetry plus a leak test" has a place to land. `review-telemetry/1` reviewer records are closed: every group has a fixed key list and an unknown key is a validation error that makes `append_record` raise. New counters (`rows_missing`, `rows_unsure`, item-linked findings) fit only in `context` as short numeric values or in a new schema version. Reflect's contract allows nested keys under its `telemetry:` mapping but fixes top-level keys.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `telemetry.py:30-81` (fixed group keys), `:204-225` (unknown key errors), `:243-251` (`context` values restricted to short labels or numbers; the leak guard exists only there), `:287-291` (`append_record` raises on any error); `panel_lint.py:316-325` (top-level keys fixed; `telemetry` must be a mapping, contents free). `tests/cli/reflect/test_shadow_skill_contract.py:65` allows changes under section 9.2, so reflect side is open; the review-telemetry side is not. The T-B6 leak test is trivially true if the counters go nowhere; the consensus names no schema or version.

ID: INV-018
CATEGORY: interaction_effects
ASSUMPTION: The row block, the second file and the sidecar writer do not disturb the adjudicated C-01, C-02 and C-03 outcomes (unknown keys open, typed `blocking` authority, `prior` quorum, `min(2, requested)` floor and refusal, union over parsable findings).
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: `ledger.py:128` parses with the v1 `parse_block` only; `findings.py:73` keeps only fences whose info string equals the requested one and `:143-150` counts only findings-v1 fences, so a `rows-v1` fence leaves `findings`, `priors` and `ok` unchanged (`findings_v2.py:233` likewise); no demotion or promotion is built, so `blocking` stays typed (C-02 result); `apply_to: ["first"]` keeps rows out of the `prior` quorum (`panel.py:600`). The only residual path is truncation, recorded in INV-011.

## Category 6: sufficiency challenge

ID: INV-019
CATEGORY: sufficiency_challenge
ASSUMPTION: The built-now set alone makes process-catchable defects get examined. It cannot, by branch trace, and the consensus's own no-cards invariant says so: with no cards declared the run is byte-identical to today's run, and no module declares cards until G-2 and G-3 pass. The set is a loader, a validator, a sidecar writer, a row parser with a check file, counters and tests. None of it puts a card in front of a reviewer. Gate trace for a target input (a Medium process defect such as a C4 criterion command that cannot match the text its task orders):
  - G-a, a module declares cards: not before G-2/G-3 (B R2 section 6 item 18; the lead summary: "wiring gated on G-2/G-3"). FAILS for built-now.
  - G-b, card text and the row instruction reach the reviewer: briefs are prose built by the orchestrator, no brief renderer exists in code, and `_SLOT_KEYS` stays closed (consensus item 6), so the resolution carries no card list either. Only prose edits (the rules file, reviewer-spec.md) reach a reviewer, and those are module wiring, not built-now code. FAILS.
  - G-c, the reviewer writes the rows: compliance is unmeasured (G-2 not run); a model may write OK rows without doing the step.
  - G-d, the row parses: undefined id grammar and a 12-character quote minimum (INV-006, INV-010). Not shown.
  - G-e, a consequence follows: v1 none; v2 only the empty-report case (`findings_v2.py:291-298`). Not shown for a report with any finding.
  - G-f, the output is read: INV-020. Not shown.
  Falsifier: G-2 fails or arm K matches arm RL (both accepted outcomes of the consensus) and the built-now code stays dormant with zero effect on what is examined.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Consensus "Built now" list and "no cards declared = today's run by hash"; round2-advocate-B section 6 items 13-18 and section 7 D-5 ("the carrier costs nothing until then"); round1-advocate-B concession 1 (no renderer; I re-ran the search: `def .*brief` in `src/superclaude` Python finds only `ledger._brief_ids` and an unrelated `_check_brief`); SKILL.md:342 (briefs are legacy briefs plus one line), `document_review_loop_prompts.md:32, :70` (brief text and "same brief" are prose); `panel.py:46, 214-216, 666-680` (slot key list and the fixed reviewer entry keys). The consensus should either label the stated outcome as conditional on G-2/G-3 plus the prose wiring, or move wiring into the built-now list.

ID: INV-020
CATEGORY: sufficiency_challenge
ASSUMPTION: "Advisory checks add safe value" and "`observed` becomes trustworthy". Safe, yes: nothing in the set changes a flag, status or verdict. Value requires a reader and a route to the fix, and the code shows neither. (1) v1: the merged report prints only ledger rows (blocking findings and "Other findings" from findings-block lines); reviewer prose, follow-up candidates and the row block never enter the ledger, so a Medium defect confirmed through a PROBLEM row stays in a raw report and CB-2 is not adopted. (2) v2 host: the only reflect host is opt-in shadow mode (default engine never calls the panel), where `cluster` and `verify-citations` "neither drop anything nor feed the debate" and `cluster_agreement` "never routes anything", so the empty-report floor changes only a listing label and `valid_blocks`. (3) `rows_missing` and the PROBLEM-without-finding list have no named reader; both advocates left this open as HIGH (A R2 item 1, B R2 item 1). (4) `observed` is typed by the reviewer, so "trustworthy" means "typed", and the one input that could verify it (`ran`) stays unverified until C-08 (INV-010 adds that quote checks mostly detect fabricated text only).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `ledger.py:442-474` (report built from ledger rows only), `merge_cmd.py:99-117` (reviewer text goes to `merge_round`, which keeps parsed findings and hashes); SKILL.md:311 (legacy default never calls the panel), :345 ("Neither drops anything and neither feeds the debate", "`cluster_agreement` ... never routes anything"); `cluster.py:386-419` (what the floor actually moves); rules file line 31 (Medium goes under follow-up candidates); round2-advocate-A section 8 item 1 and round2-advocate-B section 9 item 1. Target-input trace for a Medium C4 defect: assigned (after G-a) -> row PROBLEM -> graded Medium -> either (i) left under follow-up candidates, which the merge never reads, or (ii) written as a non-blocking findings line, which reaches only "Other findings" (`ledger.py:467-474`) and never the Reviser brief (`_brief_ids` takes blocking rows only, `ledger.py:99-104`). Either way it is examined and not repaired by the loop; a blocking-graded defect (a contradiction, an unpassable check) does pass.

## Summary

Total findings: 20
ADDRESSED: 4 (INV-003, INV-012, INV-013, INV-018)
UNADDRESSED: 16
UNADDRESSED by severity: HIGH 2 (INV-001, INV-019), MEDIUM 13 (INV-002, INV-004, INV-005, INV-006, INV-007, INV-009, INV-010, INV-011, INV-014, INV-015, INV-016, INV-017, INV-020), LOW 1 (INV-008)
Per category (total / unaddressed): state_variables 5 / 4, guard_conditions 3 / 3, count_divergence 4 / 3, collection_boundaries 2 / 1, interaction_effects 4 / 3, sufficiency_challenge 2 / 2.

Advocate-listed invariants re-checked against the consensus text: three reviewer-id spaces ADDRESSED (INV-003); line bases ADDRESSED by deferral (INV-012); zero cards and `{}` entry ADDRESSED (INV-013); C-01/C-02/C-03 non-interference ADDRESSED (INV-018). Still only named, not handled: who writes `observed` (INV-001), row-quote limits (INV-010), quorum arithmetic and compliance coupling (INV-011), UNSURE (INV-008), row-block placement and truncation (INV-011, INV-015), loop edit control (INV-015), and the reader of `rows_missing` (INV-020).

Facts the advocates marked [UNVERIFIED] that this probe verified: the INV-N mirror pins on the loop prompt exist (`tests/review/test_review_rules_text.py:34-43, 65-73`; `tests/skills/test_review_brief_placement.py:73-103, 129-138`) and they exclude `commands/spec-panel.md` from prompt edits; the 12-row figure is far below recorded slice sizes (21 of 69 entries above 12, maximum 48).

Status: Complete
