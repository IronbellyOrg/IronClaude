# Merge Execution Log

## Metadata
- Base: Variant B (sonnet:refactorer)
- Executor: merge-executor agent
- Changes applied: 41 of 41
- Status: success
- Timestamp: 2026-11-08T16:00:16Z

Output: `merged-output.md` (one directory above this log). Base copied first, then each change applied in plan order by in-place edits. Provenance tags use " - " in place of the template's dash.

## Changes Applied

### Change 1: Remove the copied `src/superclaude` example-template read
- **Status**: Applied
- **Source**: Variant C (haiku:qa), Section 8 "Command text to add or replace"
- **Target**: Base 8.1 (new item 7, opening sentence), 8.3 drift-guard row
- **Before**: "Every other line is byte-identical to the original"; six numbered edits; drift guard with no `## Tool Coordination` exemption.
- **After**: "byte-identical ... except the edits listed here"; new item 7 deletes the `src/superclaude/examples/release-spec-template.md` line with no replacement; drift guard compares `## Tool Coordination` after that one deletion.
- **Provenance tag**: `<!-- Source: Variant C (haiku:qa), Section 8 "Command text to add or replace" - merged per Change #1 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 2: Add the variant to `_POST_REFRESH_ADDITIONS`
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 8.6 second bullet
- **Target**: Base 8.3 (new row and "must keep passing without edit" paragraph), 8.4 bullet, 10 Build cost row
- **Before**: No routing-test edit; 8.4 "No edit to ... the routing tests"; Build cost "one 3-line test edit".
- **After**: New 8.3 row for `tests/recommend/test_routing_refresh.py` (line 33 set literal with `spec-panel-diffgate`); paragraph names the two edited tests; 8.4 "No edit to `HOW-WE-WORK.md` or the level-table test; one line in `test_routing_refresh.py` (8.3)"; Build cost "two small edits to existing tests (8.3)" (removes wording that implied only one test edit, per the plan's "remove any wording" instruction).
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 8.6 - merged per Change #2 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 3: Register the variant through `UNATTENDED_VARIANTS`
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 8.6 first bullet
- **Target**: Base 8.3 row `tests/skills/test_worker_contract.py`
- **Before**: `VARIANT_COMMANDS` frozenset subtracted from `have`.
- **After**: `UNATTENDED_VARIANTS = {"spec-panel-diffgate": "spec-panel"}`, set-union assertion in `_check_no_unattended_sections`, parametrized `test_variant_unattended_section_matches_parent` using `_unattended_section(name: str) -> str` (line 853); `UNATTENDED_COMMANDS` and line 1564 untouched. B's negative-test note kept as B wrote it (lines 1118-1126; the Fact check gives 1116-1126, the plan says to keep B's note).
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 8.6 - merged per Change #3 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 4: Correct factual slips and two terminology defects
- **Status**: Applied
- **Source**: `diff-analysis.md` Fact check; `base-selection.md`; X-018
- **Target**: Base 1, 5.2, 5.4, 5.5, 7, 8.1, 8.2, 8.3, 11
- **Before**: "Title line 11"; plugin copy "drifts ... by one word at line 219"; `test_spec_panel_review_loop.py:14`; "the gate would have allowed 13" and the 13/12 split in section 1; "cause 3"; unnumbered cause table; fix-map rules F1 to F3.
- **After**: (a) "Title line 10". (b) Section 11 plugin text replaced with the verified list of differences. (c) `:15`. (d) 5.4 and section 1 row 2 state the replay qualitatively ("the gate removes the minor-only and citation lines and keeps every line that carries a blocking id"). (e) "cause 2" in 5.2 and 5.5; section 1 table gains a `#` column numbered 1 to 5. (f) M1 to M3 in 5.2, the section 7 reviser row and the 8.2 outline comment.
- **Provenance tag**: `<!-- Source: Base (original, modified) - adjusted per Changes #4 and #28 -->` (section 1) and section-level "Base (original, modified)" tags for 5, 7, 8.1, 8.2, 8.3, 11
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 5: Name the host skill `sc-diffgate`, called by path
- **Status**: Applied
- **Source**: Variant A (opus:architect), Sections 3.2 and 8.2
- **Target**: Base 2 notation, 3 host skill, 8.1 `## Diffgate` items 1 and 4, 8.2, 8.5, 12 question 1
- **Before**: `sc-diffgate-protocol` (13 occurrences), frontmatter `name: sc:diffgate-protocol`.
- **After**: `sc-diffgate` everywhere; SKILL.md frontmatter `name: sc-diffgate`, delegate-only description, `allowed-tools: Read, Bash`; home path then project `.claude/` path; `E-DIFFGATE-MISSING` stop with no plain-review fallback (section 2 notation, section 3, `## Diffgate` item 1); installer naming reason (`install_skills.py` lines 40-62) stated in section 3.
- **Provenance tag**: section-level `<!-- Source: Base (original, modified) - adjusted per Changes #5, ... -->` on sections 2, 3, 8.1, 8.2, 8.5
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 6: `begin` re-runs the fix gate authoritatively
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 2 step R2.a and Section 3.3
- **Target**: Base 2 step 7, 3 `begin` row
- **Before**: `begin` checked only that a fixcheck was recorded.
- **After**: Step 7 "refuses (exit 5) unless fixcheck N-1 is accepted ..., and re-runs that check (exit 1 on an unmapped hunk)"; `begin` row recomputes the fix-map check for N of 2 or more and opens nothing on an unmapped hunk.
- **Provenance tag**: section-level tags on sections 2 and 3 ("adjusted per Changes #5, #6, ...")
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 7: One JSON object on stdout with separate verdict and execution fields
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 3.3; Variant C (haiku:qa), Section 3
- **Target**: Base 3 output sentence, subcommand Stdout column, exit-code table; section 2 steps 2 and 7; section 6 count wording
- **Before**: "Output is plain `key: value` lines"; key:value stdout per subcommand; exit 0 "done".
- **After**: One JSON object with `ok`, `exit`, `message`, `review` plus the plan's per-subcommand fields; exit-0 row adds "includes an accepted review whose verdict is FAIL; read `verdict`, never the exit code"; exit-5 row reads the `next` field; steps 2 and 7 and section 6's count describe JSON fields instead of `key: value` lines (found in the contradiction re-scan, aligned under this change).
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 3.3 and Variant C (haiku:qa), Section 3 - merged per Change #7 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 8: Hunk ids `H<k>.<n>`
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 3.5 step 5
- **Target**: Base 2 files table, 3 diff steps 5 and 6, surface example, ledger sketch, 4 report example and rules C6/C7, 5.2, 6, 8.1 `## Diffgate` item 3, 8.2 outline
- **Before**: `H<i>`, `H1`, `H2` ids.
- **After**: "Number surviving hunks `H<k>.<n>` in document order, where k is the review the surface feeds; ids never repeat across reviews"; examples renumbered (`H2.2`, `H2.3`, ...). Finding ids stay `R<k>.<j>`.
- **Provenance tag**: section-level tags on sections 2, 3, 4, 5, 6, 8.1, 8.2
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 9: Token-level eligibility inside changed lines; block-level ids for ownership
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 3.5 steps 3-4; Variant C (haiku:qa), Section 3; debate round2-B.md
- **Target**: Base 3 diff steps 3 to 5, rule C6
- **Before**: Line-level hunks; `MERGE_GAP` merged lines into eligible hunks; deletion range was the lines before and after.
- **After**: Second token-level `SequenceMatcher` pass defines the changed and removed spans; `MERGE_GAP = 2` groups lines for the fix map and display only; gap and context lines never eligible; renumbered list is one block hunk with one owner; 1-based inclusive ranges; step 5's deletion range now display context with `side=old` anchoring (kept consistent with the new step 4); C6 requires overlap with a changed or removed token.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 3.5 steps 3-4 - merged per Change #9 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 10: Finding grammar with JSON-string quoted values
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 4.1
- **Target**: Base 3 surface example, 4 report block and key list, 6 deferred example, 8.1 `## Diffgate` items 3 and 4
- **Before**: `[[...]]` delimiters; `PRIOR <id> resolved` with no `by=`; reviewer `verdict:` line in the example.
- **After**: Block under `## Diffgate findings`; line forms `PRIOR ... resolved by=`, `open quote=`, `regressed by= quote=`, `withdrawn quote= reason=`, `FINDING ... anchor="..." outcome="..."` with optional `via`, `via_quote`, `cites`, `fr`, `side=old`, and `FINDINGS none`; values are JSON strings; no `verdict:` line. Example findings keep B's keys (R2.3 via-only, R2.4 cites-only), so one clause states that a `via=` or `cites=` finding omits `hunk=` as rule C11 allows. No `[[` remains anywhere.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 4.1 - merged per Change #10 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 11: Anchor check by token overlap at the cited line, every anchor validated
- **Status**: Applied
- **Source**: Variant A (opus:architect), rule C5; Variant C (haiku:qa), Section 4 step 4
- **Target**: Base 4 rules C5 and C6
- **Before**: C5 substring on the `at` lines; C6 hunk range membership.
- **After**: C5: 12 to 200 characters, no shorter waiver, occurs on the `at=` lines on the side `side` names; every anchor and `via_quote` checked, one failure fails the line. C6: from review 2 that occurrence overlaps a changed (or removed) token of the cited hunk; `via_quote` overlaps a changed token of the `via` hunk.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), rule C5 and Variant C (haiku:qa), Section 4 step 4 - merged per Change #11 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 12: The reviewer writes no verdict; the script prints the verdict line
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 8.1 bullets 3 and 8; Variant C (haiku:qa), Section 4 step 8
- **Target**: Base 4 rule C1, rule C13, 8.1 bullet 3, `## Diffgate` item 5; section 2 step 3
- **Before**: C1 required a reviewer verdict line; C13 rejected a mismatch; bullet 3 got an appended clause; step 3 "ends with `verdict:`".
- **After**: C1 without the verdict clause; C13 deleted and replaced by a paragraph: derived verdict printed as `verdict_line`, the command removes any reviewer `verdict:` line and appends it last; bullet 3 text per the plan; item 5 appends `verdict_line`; step 3 "writes no verdict line"; tier 2 rule range no longer names C13.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 8.1 bullets 3 and 8 and Variant C (haiku:qa), Section 4 step 8 - merged per Change #12 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 13: A MAJOR blocks when an outcome is present, no length constant
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 4.1
- **Target**: Base 4 rule C12, 8.2 constants, 10 R3; section 4 "What the checker proves" and section 7 residual wording
- **Before**: `outcome` of at least 25 characters; `OUTCOME_MIN = 25`; R3 "or pad `outcome` to 25 characters"; "present and long enough".
- **After**: "`sev=major` with an `outcome` other than `-`"; constant removed; R3 padding clause removed, residual kept; "present" only.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 4.1 - merged per Change #13 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 14: Reject handling: repair once, degrade finding-level failures, stop on structure, scoped acceptance
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 4.3; debate round2-A.md, round2-B.md; Variant C (haiku:qa), Section 6
- **Target**: Base 4 tier 3, 3 `check` stdout, 6 "Surfaced once"
- **Before**: Tier 3 degraded everything and the derived verdict replaced the report's.
- **After**: Finding-level failures degrade; a structural failure ends the run with no verdict; new "Scoped acceptance" paragraph (`acceptance: scoped|clean`, the scoped-PASS line above the Reviser brief and verdict, verdict line stays exact, only `clean` earns clean-PASS credit); `check` prints `acceptance`; section 6 shows the scoped-PASS line with the deferred list.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 4.3 and Variant C (haiku:qa), Section 6 - merged per Change #14 -->` and `<!-- Source: Variant C (haiku:qa), Section 6 and debate round2-B.md A-W3 and C-W3 - merged per Change #14 (resolves INV-028) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 15: Ledger state after a structural stop
- **Status**: Applied
- **Source**: Invariant probe INV-001 (adopted, not debated)
- **Target**: Base 3 ledger sketch and paragraph, `status` states, exit-code table; 4 tier 3
- **Before**: No retry state and no `invalid` state.
- **After**: Round stays `open` with `attempts: 1`; one more `begin` for the same N reuses `doc-r<N>.md` and `surface-r<N>.md`; a second structural stop sets `invalid`; every later subcommand exits 4 with `halt: invalid`; coordinator escalates; recorder counts a failed attempt. Ledger sketch carries `state` and `attempts`; `status` lists `invalid`; exit-4 row names `halt: invalid`.
- **Provenance tag**: `<!-- Source: Invariant probe INV-001 - merged per Change #15 (adopted, not debated) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 16: `resolved by=<hunk>` replaces the forced-open rule; carried severity pinned
- **Status**: Applied
- **Source**: Variant A (opus:architect), rules C8 and V4
- **Target**: Base 4 rule C10, 3 surface example, 7 prior-findings row; section 4 "What the checker proves", tier 2 range
- **Before**: Soft C10 forcing `open` on an untouched anchor; `anchor_untouched:` fields in the surface.
- **After**: Hard C10: `resolved` carries `by=H<k>.<n>` of this surface, nothing resolves on an empty surface, `PRIOR` lines carry no severity, priors keep their recorded severity. Surface keeps `fix hunks:` only (both `anchor_untouched` fields removed). Section 7 row and "What the checker proves" updated; tier 2 hard range becomes C1 to C10.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), rules C8 and V4 - merged per Change #16 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 17: Remove the byte budget; report bytes and hunks per id
- **Status**: Applied
- **Source**: Variant A (opus:architect), Sections 5 and 3.3; debate round2-B.md A-W5
- **Target**: Base 5.2 budget paragraph, 5.4 item 2, 8.2 constants and outline comment, 8.3 test, 10 R5, 12 question 4, 3 ledger sketch
- **Before**: `FIX_BUDGET_BYTES = 1500`, `over_budget`, `added_bytes`, "blocking ids x budget", over-budget test.
- **After**: `bytes_by_id` and `hunks_by_id` as figures only; next surface header prints the largest fix; flg-r1 R2-2/R2-3 reason stated; `new_section: H<k>.<n>` warning kept; every budget item deleted; 5.4 item 2 reads "the hunks mapped to blocking ids".
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 5 and Section 3.3 - merged per Change #17 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 18: A `withdrawn` status for a declined false positive
- **Status**: Applied
- **Source**: Invariant probe INV-004 (adopted, not debated)
- **Target**: Base 4 grammar (with Change 10) and rule C9, 5.2 rule M2, 9 counting rules
- **Before**: No exit from the open set for a declined id.
- **After**: `PRIOR <id> withdrawn quote="..." reason="..."`, legal only after a `declined` line in `fixmap-r<N-1>.txt`; leaves the open blocking set, counts in `R3-proxy-all` at its recorded label, sets `acceptance: scoped`.
- **Provenance tag**: `<!-- Source: Invariant probe INV-004 - merged per Change #18 (adopted, not debated) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 19: Fix-map hardening
- **Status**: Applied
- **Source**: debate round2-B.md; invariant probe INV-024, INV-003, INV-009
- **Target**: Base 5.2 (heading, intro, M1, M3), 2 step 5 and files table, 3 `fixcheck` row
- **Before**: One id per hunk; no document binding; "at most 3 runs, then stops and says so".
- **After**: Pre-fill from inline `R<N>.<j>` tags with the file as authority; `H<k>.<n> R<N>.<j>[,R<N>.<m>...]`; first line `doc_sha: <sha>`, mismatch exits 1; third failing `fixcheck` records `fix-rejected`, reviser stops, coordinator escalates, no review consumed. 5.2 heading reads "every hunk owned by a blocking id".
- **Provenance tag**: `<!-- Source: Base (original, modified) - adjusted per Change #19 (debate round2-B.md; invariant probe INV-024, INV-003, INV-009) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 20: Word-identical changes that alter Markdown structure are surfaced
- **Status**: Applied
- **Source**: Invariant probe INV-025; debate round2-C.md New evidence 2
- **Target**: Base 3 diff step 3 (reflow filter)
- **Before**: Any word-identical block dropped.
- **After**: Dropped only when the counts of list-marker, heading and table-pipe lines match; otherwise kept as `structural: yes`, owned in the fix map and eligible next review.
- **Provenance tag**: `<!-- Source: Invariant probe INV-025 and debate round2-C.md New evidence 2 - merged per Change #20 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 21: Ledger replay, exclusive-create lock and input limits
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 4.4; Variant C (haiku:qa), Sections 3 and 10
- **Target**: Base 3 ledger paragraph and exit-code rows 2 and 6, 10 R11, 2 skip list
- **Before**: Atomic replace only; R11 "two workers ... are not locked".
- **After**: "Replay, lock and limits" paragraph (replay exits 6; exclusive-create lock; symlink refusal; 2 MiB, 100,000 lines, 1,000 machine lines exit 2); new skip-list bullet for hand edits; R11 "Hand edits are detected by replay; concurrent writers are refused by the lock."; exit rows 2 and 6 name the limits and replay.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 4.4 and Variant C (haiku:qa), Sections 3 and 10 - merged per Change #21 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 22: The verdict line is always the last line
- **Status**: Applied
- **Source**: Invariant probe INV-027 (adopted, not debated)
- **Target**: Base 2 step 12 and "Early exit", 6 "Surfaced once", 8.1 `## Diffgate` item 6, 8.3 command test row
- **Before**: `deferred.md` printed "as the last block of its output".
- **After**: Order: findings block, `## Deferred (pre-existing, not looped on)`, scoped-PASS line if any, Reviser brief (reviews 1 and 2 only), verdict line last; command test asserts the last non-blank line is exactly `verdict: PASS` or `verdict: FAIL`.
- **Provenance tag**: `<!-- Source: Invariant probe INV-027 - merged per Change #22 (adopted, not debated) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 23: Deferred list: scoped-PASS disclosure and a safer dedup key
- **Status**: Applied
- **Source**: Variant C (haiku:qa), Section 6
- **Target**: Base 6 "Format" and "Surfaced once"
- **Before**: Dedup by quote ("The same quote deferred in two rounds is one entry").
- **After**: Header sentence "PASS in this loop is scoped to the reviewed surfaces; deferred severity labels are the reviewer's, unvalidated."; key = anchor text plus whitespace-collapsed `::` text; the R3 proxy never reads the deduplicated list.
- **Provenance tag**: `<!-- Source: Variant C (haiku:qa), Section 6 - merged per Change #23 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 24: Command bullets written out verbatim for the merged design
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 8.1; Variant C (haiku:qa), Section 8
- **Target**: Base 8.1 item 3 bullets 1, 3, 5, 6 and `## Diffgate` items 2 to 6
- **Before**: Bullet 3 as an appended clause outside the block; bullet 5 without `by=`, `withdrawn` or the read-only-context rule; bullet 6 "map every changed hunk to one blocking id".
- **After**: Bullet 1 as B's text; bullet 3 written in full inside the block; bullet 5 adds `resolved by=`, `open quote=`, `regressed by= quote=`, `withdrawn`, token-overlap anchoring and "context is read-only and cannot widen eligibility", keeps the empty-surface clause; bullet 6 adds the `doc_sha` line, multi-id mapping, `declined` lines and "the next review refuses to open while any hunk maps to no listed finding". Each bullet is one physical line (checked: 6 bullets in the Review Loop block, 6 items in the `## Diffgate` block). Pinned literals present: canonical cap text, HALT clause, `resolved|open|regressed`, `origin=changed|unchanged`, `verdict: PASS`, `verdict: FAIL`, `review: N of 3`, `Reviser brief`, `byte size before and after`, rf-qa lookup order.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 8.1 and Variant C (haiku:qa), Section 8 - merged per Change #24 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 25: Key the comparison table to 427's seven bullets
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 7
- **Target**: Base 7 table
- **Before**: 12 rows without a bullet column; "Blocking and verdict" row cited C13.
- **After**: First column "427 bullet" (1 Mode, 2 Grading and 3 Verdict, 4 Cap, 5 Re-review output, 6 Reviser contract, or "none" for findings-point-at-text and order of steps); "Blocking and verdict" row says the script prints the verdict line; "Prior-findings table" row updated by Change 16.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 7 - merged per Change #25 (427 bullet column; rows changed by Changes #12 and #16) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 26: Label every new name as PROPOSED
- **Status**: Applied
- **Source**: Variant C (haiku:qa), Sections 1 and 8
- **Target**: Base 8 opening
- **Before**: No PROPOSED sentence.
- **After**: "Every file, subcommand, flag, constant and test named in sections 2 to 8 and 13 is PROPOSED and does not exist yet; existing files are cited with line numbers."
- **Provenance tag**: `<!-- Source: Variant C (haiku:qa), Sections 1 and 8 - merged per Change #26 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 27: Script outline with A's signatures, the profile seam and the merged constants
- **Status**: Applied
- **Source**: Variant A (opus:architect), Sections 8.3 and 3.6
- **Target**: Base 8.2 outline, size lines; 10 Build cost
- **Before**: `MAX_ROUNDS = 3; MERGE_GAP = 2; VIA_CAP = 2` (after Changes 13 and 17); `build_hunks`; about 350 lines.
- **After**: `CAP_REVIEWS = 3; MERGE_GAP = 2; VIA_CAP = 2; FORMAT = "diffgate/1"` and the `PROFILES` dict; exit constants unchanged; adds `tokens`, `quote_spans`, `replay`, `derive`; `build_hunks` renamed to A's `diff(old_lines, new_lines, review)` covering both passes; rules C1-C12; about 420 lines; cut order kept.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Sections 8.3 and 3.6 - merged per Change #27 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 28: Replace the forecast with the Round 2 consensus and state the theme's limit
- **Status**: Applied
- **Source**: debate round2-A.md, round2-B.md, round2-C.md; debate/evidence-flg-r1.md
- **Target**: Base 9 predictions and probability lines, 1 "What stays unfixed" and retrofit paragraph, 5.5
- **Before**: R3 "3.5 mean (replicates about 5 and 2)", growth "23% mean (range 17 to 30%)", P(both at 3 or fewer) about 0.25, `flg-r1` composition UNVERIFIED.
- **After**: R3 about 3.0 to 3.5 (flg-r1-like about 4 to 5, flg-r2-like about 1 to 2); growth about 20% to 27% with P about 0.9; P(both at 3 or fewer) about 0.2 to 0.25; P(F1 in at least one) about 0.5 to 0.55; clean PASS about 10%; verbatim theme-limit paragraph; most likely product and "escalate with an interpretable record"; early PASS carried forward for growth; section 1 retrofit paragraph now cites `debate/evidence-flg-r1.md`.
- **Provenance tag**: `<!-- Source: Debate round2-A.md, round2-B.md and round2-C.md, ... and debate/evidence-flg-r1.md - merged per Change #28 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 29: Merged failure conditions
- **Status**: Applied
- **Source**: Variant B Section 9; debate round2-B.md; Variant A (opus:architect), Section 9 conditions 3 to 5
- **Target**: Base 9 failure conditions
- **Before**: F1 "R3-proxy-all of 5 or more"; F3 blind-audit comparison; four conditions.
- **After**: F1 re-based (proxy above 3 and at least 70% of review-3 critical+major on blocking-fix hunks by ledger ancestry); F2 and F4 unchanged; F3 is A's blindness condition; two added conditions numbered 5 and 6 and labelled F5 (demotion or gate failures) and F6 (stall); label proxy and 427-blocking reported side by side; success sentence now "F1 to F6".
- **Provenance tag**: `<!-- Source: Base (original, modified) - F1 re-based and F3 replaced per Change #29 (...) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 30: F1 share over all-discovered findings by ancestry
- **Status**: Applied
- **Source**: Invariant probe INV-016 (adopted, not debated)
- **Target**: Base 9 F1 and "Extra recordings"
- **Before**: "share of review-3 blockers sitting on mapped fix hunks".
- **After**: "F1 share (pre-registered)" paragraph with the three ancestry classes, the 100%-by-construction sentence, and the control/Arm B method via `disposition*.md`; extra recordings name the same share.
- **Provenance tag**: `<!-- Source: Invariant probe INV-016 - merged per Change #30 (adopted, not debated) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 31: One R3 proxy function for every arm
- **Status**: Applied
- **Source**: Invariant probe INV-015 (adopted, not debated)
- **Target**: Base 9 primary metric
- **Before**: Proxy counted from the review-3 report with deferred findings.
- **After**: One function over every arm's review-3 report and ledger (new findings incl. deferred and demoted; open or regressed priors at recorded label; each id once); withdrawn priors counted; control (8, 4) and Arm B (6, 1) recomputed and published beside the historical values before scoring.
- **Provenance tag**: `<!-- Source: Invariant probe INV-015 - merged per Change #31 (adopted, not debated) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 32: Three pre-registered result classes and the reachable spread check
- **Status**: Applied
- **Source**: Invariant probe INV-036 (adopted, not debated); debate round2-B.md
- **Target**: Base 9 (new paragraph), 8 Stage C; 11 `/sc:spec-panel` row
- **Before**: Stage C "only if the S1 bar is met"; no result classes.
- **After**: "Result classes (pre-registered)" paragraph (three classes; spread check reported, defined from the INV-036 row, reachable only below a treatment mean of 2.0; proven-effect claim needs a pre-fixed replicate count); Stage C "decided on the result class of section 9, never on the bar alone"; section 11 order "after the S1 result class (section 9)".
- **Provenance tag**: `<!-- Source: Invariant probe INV-036 - merged per Change #32 (adopted, not debated) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 33: Claim the combined treatment; name the briefs-only arm
- **Status**: Applied
- **Source**: Invariant probe INV-034 (adopted, not debated)
- **Target**: Base 9 Design, 8.5 brief substitution
- **Before**: No treatment definition; brief substitution only recorded.
- **After**: "The treatment is the script plus the brief diff published in 8.5. A pass does not support 'mechanical over prose'; that claim needs a briefs-only arm ..."; 8.5 publishes the exact before and after text of every changed brief line.
- **Provenance tag**: `<!-- Source: Invariant probe INV-034 - merged per Change #33 (adopted, not debated) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 34: Mandatory blindness audit classified by ledger history
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 9 "Blindness audit"
- **Target**: Base 9 "Blind audit"; references in 6 and 10 (R1, R2)
- **Before**: Optional "if budget allows" blind audit.
- **After**: Mandatory fresh review 1 per replicate for every arm, classified by ledger history, compared with control and Arm B, density recorded; "blind audit" references renamed "blindness audit".
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 9 "Blindness audit" - merged per Change #34 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 35: Validity rules for recovery compliance and review-1 comparability
- **Status**: Applied
- **Source**: Invariant probe INV-038, INV-039, INV-033, INV-019; debate round2-C.md New evidence 5
- **Target**: Base 9 validity gate
- **Before**: "An invalid replicate is rerun, not scored."
- **After**: Fixed attempt slots (two per arm); void conditions; void replicate reported with cost, never scored or silently replaced; review-1 13 to 17 comparability label; completion rate per arm.
- **Provenance tag**: `<!-- Source: Invariant probe INV-038, INV-039, INV-033, INV-019 and debate round2-C.md New evidence 5 - merged per Change #35 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 36: Pre-run gate, install hashes and invocation evidence
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 8.9; Variant C (haiku:qa), Section 8; base question 12.1; invariant probe INV-010, INV-006
- **Target**: Base 8.5, 9 Design, 12 question 1
- **Before**: Permissions an open question; no `spec-panel.md` hash check.
- **After**: "Pre-run gate" paragraph (three checks, `spec-panel.md` hash before and after each step, hashes of the new files, no `--force`, transcript step order); 8.5 adds the `sha256sum ~/.claude/commands/sc/spec-panel.md` line (one physical line) and a pointer to the gate; question 1 marked as moved into the gate.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 8.9, Variant C (haiku:qa), Section 8, base question 12.1, invariant probe INV-010 and INV-006 - merged per Change #36 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 37: Full cost envelope
- **Status**: Applied
- **Source**: Variant C (haiku:qa), Section 10 "Cost envelope"
- **Target**: Base 10 cost table, 9 extra recordings
- **Before**: Wall time "about 3 to 5 extra minutes per loop".
- **After**: Rows for correction turns, `fixcheck` failures, the blindness-audit session, void or `invalid` attempts, coordinator dispatch time; wall time is a range that grows with correction turns, marked UNVERIFIED (no new numbers invented); extra recordings list the same items.
- **Provenance tag**: `<!-- Source: Variant C (haiku:qa), Section 10 "Cost envelope" - merged per Change #37 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 38: Later adopters keep the profile seam and C's limits
- **Status**: Applied
- **Source**: Variant A (opus:architect), Section 11; Variant C (haiku:qa), Section 11
- **Target**: Base 11 rows rf-qa and `/sc:implement`
- **Before**: rf-qa row without profile or guard clause; `/sc:implement` row "Nothing to replace".
- **After**: rf-qa adds an `rf-qa` profile (CRITICAL and IMPORTANT blocking, MINOR a note) and must not weaken its guards; `/sc:implement` "do not replace the final review; at most a checked delta surface ... with a fresh full final review kept for archive acceptance".
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 11 and Variant C (haiku:qa), Section 11 - merged per Change #38 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 39: New section 13 "Test plan"
- **Status**: Applied
- **Source**: Variant C (haiku:qa), Section 13; Variant A (opus:architect), Section 8.4; base 8.3 case list; debate round2-B.md, round2-C.md
- **Target**: Base, new section 13; 8.3 rows point to it
- **Before**: [Section did not exist]; cases inline in the 8.3 row.
- **After**: P0 script cases (B's list minus the budget and verdict-mismatch cases, plus every case the plan lists, including the flg-r1-shaped fixture with its expected values); P1 command, the two existing-test edits, the isolated temporary-HOME install test, and a one-line `uv run pytest` command. B's case "`resolved` on an untouched anchor becomes `open`" tested a rule Change 16 removed, so it is replaced by "`resolved` without `by=` exits 1 `E-PRIOR`" (the merged C10). 8.3 script row now says "Cases: section 13, P0".
- **Provenance tag**: `<!-- Source: Variant C (haiku:qa), Section 13, with Variant A (opus:architect), Section 8.4 cases and the base 8.3 case list - merged per Change #39 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 40: New section 14 "Acceptance criteria"
- **Status**: Applied
- **Source**: Variant C (haiku:qa), Section 14
- **Target**: Base, new section 14
- **Before**: [Section did not exist]
- **After**: Criteria 1 to 14 adapted to the merged design in the plan's order; C's criterion 15 moved to section 9's result classes.
- **Provenance tag**: `<!-- Source: Variant C (haiku:qa), Section 14, adapted to the merged design - merged per Change #40 -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

### Change 41: Give every open question a default and close the answered ones
- **Status**: Applied
- **Source**: Variant C (haiku:qa), Section 12
- **Target**: Base 12 (all items)
- **Before**: Twelve open questions, several answered elsewhere by the plan.
- **After**: Intro sentence on defaults; 1 moved to the pre-run gate (Change 36); 4, 5, 7 closed; 12 answered by `debate/evidence-flg-r1.md`; 2, 3, 6, 8, 9, 10, 11 each state the default used in S1, taken from the merged text.
- **Provenance tag**: `<!-- Source: Base (original, modified) - every question given a default or closed per Change #41 (Variant C (haiku:qa), Section 12) -->`
- **Validation**: Structural integrity ✅ | References ✅ | Contradictions ✅

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: ✅ One H1 title; H2 sections 1 to 14; H3 8.1 to 8.5 under section 8; H3 P0 and P1 under section 13. Headings inside fenced examples (`## Diffgate`, `## Diffgate findings`, surface `#` lines) are code, not document headings.
- Section ordering: ✅ 1, 2, ..., 12 (B's numbering kept), then 13 Test plan and 14 Acceptance criteria.
- Document flow: ✅ Every section carries a provenance tag; provenance header (Provenance, Base, Merge date) at the top; title names the merged design (diffgate for /sc:spec-panel, variant command `spec-panel-diffgate`).

### Internal References
- Total references: 158 (65 section references, 62 rule references C1 to C12, C2b, M1 to M3, F1 to F6, 6 risk references R2, R9, R10, R11, and 25 "Change N" references carried from the plan's integration text)
- Resolved: 158 (every cited section 1 to 13, 5.1, 5.2, 8.3, 8.5 exists; every cited rule and risk is defined; "Change N" references resolve to `adversarial/refactor-plan.md` and this log)
- Broken: 0

### Contradiction Re-Scan
- New contradictions introduced: 0
- Details: Scanned for leftover pre-merge items with zero hits each: old forecasts ("3.5 mean" as a point forecast, "replicates about 5 and 2", "23% mean", "about 40%", the 13/12 line split, "the gate would have allowed 13"); the old byte budget (`1500`, `FIX_BUDGET_BYTES`, `over_budget`, `added_bytes`, "blocking ids x budget"); `OUTCOME_MIN` and "25 characters"; the old skill name `sc-diffgate-protocol` and `sc:diffgate-protocol`; `--ledger` (0 hits; the plan keeps B's `--diffgate-dir <dir>` and ledger file naming, so flag and ledger naming are consistent); `[[...]]` quotes; rule C13 and `E-VERDICT`; `anchor_untouched`; `H<i>`; `MAX_ROUNDS` and `build_hunks`; "Title line 11"; `review_loop.py:14`; "cause 3"; fix-map rules named F1 to F3. Five leftovers found during the scan were aligned under the change that caused them before this log was written: section 2 step 3 reviewer verdict (Change 12), steps 2 and 7 and the section 6 count in `key: value` form (Change 7), Build cost "one 3-line test edit" (Change 2), section 11 "after the S1 bar" (Change 32), and "blind audit" naming (Change 34). Em dashes in the merged file: 0. Pre-existing base wording not changed by the plan and not a new contradiction: exit-code row 1 "reruns, at most twice" covers both one `check` repair and up to three `fixcheck` runs.

## Summary
- Total changes planned: 41
- Successfully applied: 41
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
