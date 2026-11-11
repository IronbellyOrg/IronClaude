# Refactoring Plan: Merge into Base (Variant B)

## Overview
- Base: Variant B (sonnet:refactorer), `variant-2-sonnet-refactorer.md`, selected by the debate-performance tiebreaker (C 0.8648, B 0.8527, A 0.8265; see `base-selection.md`)
- Incorporating strengths from: Variant A (opus:architect), Variant C (haiku:qa), the Round 2 consensus, and the invariant probe
- Planned changes: 41
- Risk level: Medium (overall). Most changes are additive or replace one rule; the eligibility, grammar, checker and reject-handling changes (9 to 16) touch several sections each and must be applied together.

How to read the changes:
- "Diff point" cites the Scoring Matrix of `debate-transcript.md` (winner, confidence) and the Round 2 statement that carries the agreed detail. Round 2 is the deciding round for every point (Round 3 skipped at depth standard).
- Changes marked **adopted from invariant probe (not debated)** take the stated Resolution line of `invariant-probe.md` as written. They are not debate outcomes.
- Changes marked **required by the Fact check** fix a verified repository error listed in `diff-analysis.md`.
- Section references to the base use B's numbering (sections 1 to 12, subsections 8.1 to 8.5). Two new top-level sections are added: 13 Test plan and 14 Acceptance criteria.
- Every changed command bullet stays one physical line, and the canonical cap text `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` and the at-cap clause stay verbatim (seed brief constraint; `tests/skills/test_review_severity_rule.py`).

## Planned Changes

### Part 1: Repository correctness (Fact check)

### Change 1: Remove the copied `src/superclaude` example-template read (from Variant C)
- **Source**: Variant C, section 8 "Command text to add or replace" ("In `## Tool Coordination`, remove the copied repository-only example-template read ... Do not replace it with an invented installed example path").
- **Target**: Base 8.1 (insert a new numbered edit after item 6) and 8.3 drift-guard row (amend).
- **Rationale**: Required by the Fact check: `src/superclaude/commands/spec-panel.md:220` reads `src/superclaude/examples/release-spec-template.md`, so B's "Every other line is byte-identical" ships a `src/superclaude` path into an installed primitive and fails B's own grep (X-016, winner C at 75%; X-015, C at 95%; S-004, A+C at 95%; U-016 High). B conceded in Round 2 (`round2-B.md` A-W1).
- **Integration point**: 8.1 item 7 (new): "`## Tool Coordination`: delete the line that reads `src/superclaude/examples/release-spec-template.md`; add no replacement path." Change 8.1's opening sentence from "Every other line is byte-identical" to "Every other line is byte-identical except the edits listed here." In 8.3, the drift guard compares `## Tool Coordination` after that one deletion; the grep check in 8.5 then prints nothing.
- **Risk**: Low. One deleted line; the drift guard and the grep both pin it.

### Change 2: Add the variant to `_POST_REFRESH_ADDITIONS` (from Variant A)
- **Source**: Variant A, 8.6 second bullet.
- **Target**: Base 8.3 (new table row) and 8.3 paragraph "Existing tests that scan the new files and must keep passing without edit" (amend).
- **Rationale**: Required by the Fact check: `tests/recommend/test_routing_refresh.py` line 33 is `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` and line 648 asserts shipped commands minus that set equal the active set, so a new command file fails it (X-012, A at 95%; C-030, A+B+C at 95%). B conceded (`round2-B.md` A-W2).
- **Integration point**: New 8.3 row: `tests/recommend/test_routing_refresh.py` | edit, 1 line | `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue", "spec-panel-diffgate"}`. Remove any wording that implies no routing test needs an edit; 8.4's "No edit to ... the routing tests" becomes "No edit to `HOW-WE-WORK.md` or the level-table test; one line in `test_routing_refresh.py` (8.3)".
- **Risk**: Low. One set literal.

### Change 3: Register the variant in `test_worker_contract.py` through `UNATTENDED_VARIANTS` (from Variant A)
- **Source**: Variant A, 8.6 first bullet (code block with `UNATTENDED_VARIANTS = {"spec-panel-diffgate": "spec-panel"}` and `test_variant_unattended_section_matches_parent`).
- **Target**: Base 8.3, row `tests/skills/test_worker_contract.py` (replace).
- **Rationale**: Required by the Fact check: `_check_no_unattended_sections` (line 831) asserts set equality at line 837, so the copied `## Unattended mode` heading fails it without a variant exception (X-017, A at 75%; C-031, A+B at 75%; C-030). A's map keeps `UNATTENDED_COMMANDS` and the `assert len(expect) == 31` at line 1564 untouched and adds a parent-equality test; B's `VARIANT_COMMANDS` subtraction drops the variant from the check without pinning its text. `_unattended_section(name: str) -> str` exists at line 853 (Fact check).
- **Integration point**: Replace B's row text with: add `UNATTENDED_VARIANTS = {"spec-panel-diffgate": "spec-panel"}`; in `_check_no_unattended_sections` assert `set(have) == set(UNATTENDED_COMMANDS) | set(UNATTENDED_VARIANTS)`; add the parametrized `test_variant_unattended_section_matches_parent` comparing the variant's section with the parent's after the name swap. Keep B's note that the negative test at lines 1116-1126 still fails as before. Base 8.1 item 5 (verbatim `## Unattended mode`) stays.
- **Risk**: Low. Additive test code; the existing count assertion is untouched.

### Change 4: Correct factual slips and two terminology defects in the base (Fact check and scoring)
- **Source**: `diff-analysis.md` Fact check "Wrong or overstated"; `base-selection.md` Correctness 3 and DC computation; X-018 (tie at 95%, B conceded in `round2-B.md` A-W6).
- **Target**: Base 1, 5.2, 5.4, 5.5, 8.1, 8.3, 11 (replace phrases).
- **Rationale**: These are verified errors; the merged spec must be correct against the repository.
- **Integration point**: (a) 8.1 item 1: "Title line 11" becomes "Title line 10". (b) 11 and anywhere the plugin copy is described: replace "drifts from `src/` by one word at line 219" with "differs from `src/`: it lacks the second Usage line, the `--target-release` paragraph and the whole `## Unattended mode` section, and line 219 reads `Native reasoning` where `src/` line 221 reads `Sequential`". (c) 8.3: `test_spec_panel_review_loop.py:14` becomes `:15`. (d) 1 and 5.4: drop "the gate would have allowed 13" and state the replay qualitatively ("the gate removes the minor-only and citation lines and keeps every line that carries a blocking id"), as B proposed. (e) 5.2 and 5.5: "cause 3" becomes "cause 2" (the "Revisers add work" row); number the section 1 table rows 1 to 5 so the references resolve. (f) Rename the fix-map rules F1 to F3 in 5.2 to M1 to M3 so F1 to F4 name only the failure conditions of section 9.
- **Risk**: Low. Text corrections only.

### Part 2: Script, grammar and checker

### Change 5: Name the host skill `sc-diffgate`, called by path (from Variant A)
- **Source**: Variant A, 3.2 "Name check" (installer analysis) and 8.2.
- **Target**: Base 2 notation, 3 "Host skill", 8.1 `## Diffgate` item 1, 8.2, 8.5 (replace every `sc-diffgate-protocol`).
- **Rationale**: C-002, A at 95%; X-014, A+B at 95%. A's naming rests on the verified `install_skills.py` lines 40-62 analysis (a skill named after the command would be skipped); `sc-diffgate` also matches a delegate-only infrastructure skill like `sc-bare-review`. Round 2 positions add C's transcript check of the by-path call (Change 36).
- **Integration point**: Folder `src/superclaude/skills/sc-diffgate/` with `SKILL.md` (frontmatter `name: sc-diffgate`, description "Infrastructure skill ... Delegate-only, no slash command", `allowed-tools: Read, Bash`) and `scripts/diffgate.py`. Script path in the command: `~/.claude/skills/sc-diffgate/scripts/diffgate.py`, else the project `.claude/skills/sc-diffgate/scripts/diffgate.py`; if neither exists stop with `E-DIFFGATE-MISSING` and never fall back to a plain review (A 3.2).
- **Risk**: Low. Rename only; the installer facts are verified.

### Change 6: `begin` re-runs the fix gate authoritatively (from Variant A)
- **Source**: Variant A, 2 step R2.a and 3.3 (`open` "run the fix gate"); `round2-A.md` C-003.
- **Target**: Base 2 step 7 and 3 subcommand table, row `begin` (amend).
- **Rationale**: C-003, A+B at 95%: keep B's four subcommands (`begin`, `check`, `fixcheck`, `status`) and A's rule that the next review's open step re-runs the gate, so a skipped or forged `fixcheck` record cannot open a review. B's `begin` only checks that a `fixcheck` was recorded for the current sha.
- **Integration point**: 3 `begin` row Writes/Effect: "for N of 2 or more, recompute the fix-map check against `doc-r<N-1>.md` and the current spec; any unmapped hunk exits 1 with the unmapped list and opens nothing". 2 step 7: "refuses (exit 5) unless fixcheck N-1 is accepted for the current doc sha, and re-runs that check (exit 1 on an unmapped hunk)".
- **Risk**: Low. Same code path as `fixcheck`.

### Change 7: One JSON object on stdout with separate verdict and execution fields (from Variants A and C)
- **Source**: Variant A, 3.3 ("Every subcommand prints exactly one JSON object on stdout"); Variant C, 3 ("Verdict and execution success are separate fields. Never interpret exit 0 alone as review PASS").
- **Target**: Base 3 "Output is plain `key: value` lines" (replace), subcommand table Stdout column (replace), exit-code table (amend).
- **Rationale**: C-004, A+C at 95% (B withdrew the key:value preference in `round2-B.md` C-004); C-005, B+C at 95% (B's one-meaning-per-code table plus C's rule that a valid FAIL exits 0); S-006, A+B at 95% (one shared exit table with "Who acts", which B has).
- **Integration point**: Every subcommand prints one JSON object with `ok`, `exit`, `message`, `review`, plus per-subcommand fields (`begin`: `surface`, `hunks`, `ignored`, `coverage`, `priors`; `check`: `accepted`, `verdict`, `verdict_line`, `acceptance` (Change 14), `blocking`, `deferred`, `degraded`, `halt`; `fixcheck`: `hunks`, `mapped`, `declined`, `withdrawn` candidates, `bytes_by_id`, `hunks_by_id`, `unmapped`; `status`: `state`, `next`). Keep B's exit codes 0 to 6; add to the exit-0 row: "includes an accepted review whose verdict is FAIL; read `verdict`, never the exit code, for the review result".
- **Risk**: Low. Format change contained in section 3 and the tests.

### Change 8: Hunk ids `H<k>.<n>` that never repeat across reviews (from Variant A)
- **Source**: Variant A, 3.5 step 5.
- **Target**: Base 3 diff step 5 and 6, surface example, ledger sketch, 4 report block example, 5.2, 5.3 (replace `H<i>`).
- **Rationale**: C-009, A at 75% (`round2-A.md`: "`H<k>.<n>` never repeats and is shared by the gate and the next surface").
- **Integration point**: Diff step 5: "Number surviving hunks `H<k>.<n>` in document order, where k is the review the surface feeds"; step 6 keeps B's point that the fix map of cycle k-1 and the surface of review k use the same ids. Finding ids stay `R<k>.<j>`.
- **Risk**: Low. Naming only; one regex in the parser.

### Change 9: Token-level eligibility inside changed lines; block-level ids for ownership (common core of unresolved C-008; from Variant A)
- **Source**: Variant A, 3.5 steps 3-4 (second `SequenceMatcher` on tokens inside changed blocks); Variant C, 3 "Context lines do not become eligible merely by sharing a hunk"; `round2-B.md` response to round2-A item 1.
- **Target**: Base 3 diff steps 3 to 5 (amend) and 4 rule C6 (amend).
- **Rationale**: C-008 is the one unresolved point (50%: A+C, A+B, A+B+C), but every Round 2 position contains A's token-level eligibility, and B conceded C's point that `MERGE_GAP` must not make unchanged gap lines eligible (`round2-B.md` C-W2). C-022 (A+B at 75%) keeps the reflow filter and `coverage:` warning. Also resolves INV-017 (MEDIUM): one segmentation must serve eligibility, ownership and the next surface.
- **Integration point**: Diff step 3 (new second pass): inside each non-equal block, split old and new into whitespace tokens with line and offset, run a second `SequenceMatcher`; inserted and replaced new-side tokens are the changed span, deleted and replaced old-side tokens the removed span. Step 4: `MERGE_GAP = 2` groups adjacent changed lines into one hunk id for the fix map and display only; gap lines and display context are never eligible. Rule C6: the anchor must overlap a changed token of the cited hunk (or a removed token with `side=old`). Line ranges are 1-based and inclusive everywhere (also closes INV-018, LOW). The renumber case stays as B decided: a renumbered list merges into one block hunk with one owner; no separate `renumber` line (see Changes NOT Being Made).
- **Risk**: Medium. New diff pass; covered by the token-level tests of Change 39.

### Change 10: Finding grammar with JSON-string quoted values (from Variant A)
- **Source**: Variant A, 4.1 ("Quotes and outcomes are JSON strings, so any character can be quoted and parsing is unambiguous (`json.loads` on the token)").
- **Target**: Base 4 "Report block" example and key list (replace `[[...]]` delimiters).
- **Rationale**: C-006, A+B at 75% (`round2-B.md` C-006: "A's JSON-quoted values (no `[[ ]]` limit) carrying B's `via=`, `cites=`, `declined` fields"; B conceded `[[...]]` breaks on `]]`). INV-007 (ADDRESSED) requires the zero-finding sentinel, which B already has.
- **Integration point**: The block sits under `## Diffgate findings`. Lines: `PRIOR <id> resolved by=H<k>.<n>`, `PRIOR <id> open quote="..."`, `PRIOR <id> regressed by=H<k>.<n> quote="..."`, `PRIOR <id> withdrawn quote="..." reason="..."` (Change 18), `FINDING <id> sev=<s> at=<line or a-b> hunk=H<k>.<n> anchor="..." outcome="..." :: text`, with optional `via=H<k>.<n> via_quote="..."`, `cites=<id>`, `fr=8|9|10`, `side=old`, and the single line `FINDINGS none`. Values in quotes are JSON strings. No `verdict:` line (Change 12).
- **Risk**: Medium. Touches every report example and the parser; the old `[[...]]` form must be removed everywhere (sections 3, 4, 6, 8.1).

### Change 11: Anchor check by token overlap at the cited line, every anchor validated (from Variants A and C)
- **Source**: Variant A, rule C5 (quote overlaps a changed token of the cited hunk); Variant C, 4 step 4 ("Validate every claimed surface anchor, not just the first good one").
- **Target**: Base 4 rules C5 and C6 (replace).
- **Rationale**: C-010, A+C at 95% (`round2-A.md`: "A's rules without C13, plus C's validation of every claimed anchor"; `round2-C.md`: "including repeated-text occurrences and old/new side"). Resolves INV-022 (MEDIUM): a quote that also occurs in unchanged text could smuggle a pre-existing defect into blocking scope, so the occurrence that counts is the one on the `at=` lines. B's 12-character minimum has no whole-span waiver, which also closes INV-023 (LOW).
- **Integration point**: C5 (hard): the whitespace-collapsed `anchor` (12 to 200 characters) occurs on the lines `at=` names, in the snapshot side named by `side`. C6 (hard): from review 2, that occurrence overlaps at least one changed token (or removed token for `side=old`) of the cited hunk; `via_quote` must overlap a changed token of the `via` hunk. Every `anchor` and `via_quote` in a line is checked; one failing anchor fails the line.
- **Risk**: Medium. Stricter than both parents; may raise first-try rejects (measured by F4).

### Change 12: The reviewer writes no verdict; the script prints the verdict line (from Variants A and C)
- **Source**: Variant A, bullet 3 and 8 (8.1: "write the report with a `## Diffgate findings` section ... and no verdict line"); Variant C, 4 step 8 ("The reviewer writes no authoritative verdict").
- **Target**: Base 4 rule C1 (amend), rule C13 (delete), 8.1 bullet 3 clause (replace), `## Diffgate` item 5 (amend).
- **Rationale**: C-018 and X-006, A+C at 95%. B conceded (`round2-B.md` A-W4: "Rule C1's verdict clause and C13 are deleted, which removes a reject path").
- **Integration point**: C1 keeps the `review: N of 3` check and the "FINDING lines or `FINDINGS none`" check, without the verdict clause. Delete C13. `check` prints `verdict_line`; the command appends it as the report's last non-blank line (placement in Change 22). Any `verdict:` line the reviewer wrote is removed by the command before appending. Bullet 3: "a critique-mode report's last line is `verdict: PASS` (minor notes allowed) or `verdict: FAIL` (a blocking finding is open), copied from the `verdict_line` that `check` prints; the reviewer never composes its own."
- **Risk**: Low. Removes a reject path.

### Change 13: A MAJOR blocks when an outcome is present, with no length constant (from Variant A)
- **Source**: Variant A, 4.1 ("`sev=major` with an `outcome` that is not `-`").
- **Target**: Base 4 rule C12 (replace), 8.2 constants (delete `OUTCOME_MIN = 25`), 10 R3 (amend).
- **Rationale**: C-019, A at 95%. B conceded (`round2-B.md` A-W5: "`OUTCOME_MIN = 25` is replaced by A's rule ... same checkability and no padding threshold").
- **Integration point**: C12: "an in-scope finding is blocking iff `sev=critical`, or `fr` is 8 or 9, or `sev=major` with an `outcome` other than `-`". R3: drop "or pad `outcome` to 25 characters"; keep "Residual: semantic fit of the finding to the anchor is not checked".
- **Risk**: Low.

### Change 14: Reject handling: repair once, then degrade finding-level failures, stop only on structural failure, never a clean PASS from degraded output (from Variants A, B and C)
- **Source**: Variant A, 4.3 (demote, stop on non-demotable rules); `round2-A.md` B-2 and C-1; `round2-B.md` A-W3 and C-W3; Variant C, 6 ("The final summary explicitly states that PASS is scoped").
- **Target**: Base 4 "What happens on a reject (one answer, three tiers)", tier 3 (replace); 3 `check` stdout (amend); 6 (amend).
- **Rationale**: C-011 and X-002, A+B+C at 95%; C-013 and X-005, B at 75% (over-cap `via` deferred, counted, and forcing the scoped wording). Also resolves INV-028 (MEDIUM): a `PASS (scoped; ...)` verdict line would break 427's exact-line readers, so the scope goes in a separate machine-readable field and the verdict line stays exact.
- **Integration point**: Tier 3 becomes: "Still hard violations on the rerun: a finding-level violation (C2, C4 to C8) moves that finding to `deferred: unanchored`; a missing `PRIOR` row counts as `open`; `degraded: yes` is recorded. A structural failure (no parseable `## Diffgate findings` block, no `FINDING` lines and no `FINDINGS none`, an `R<k>.<j>` id in the prose missing from the block (C2b), or a `review:` line that disagrees with the ledger) ends the run with no verdict (state handling in Change 15)." Add: "`check` sets `acceptance: scoped` and prints the line `scoped PASS: <n> deferred, degraded or withdrawn blocking-grade findings are listed below` above the Reviser brief and verdict whenever the derived verdict is PASS and any finding labelled critical or major, or blocking-grade under the profile, was deferred, degraded, demoted, over the `via` cap (`reason=via-cap`), or withdrawn (Change 18); otherwise `acceptance: clean`. The verdict line is exactly `verdict: PASS` in both cases. Only `acceptance: clean` can earn the bar's clean-PASS alternative."
- **Risk**: Medium. Changes the run's terminal behaviour; Change 15 must land with it.

### Change 15: Ledger state after a structural stop (adopted from invariant probe (not debated))
- **Source**: `invariant-probe.md` INV-001 (HIGH, UNADDRESSED), Resolution line.
- **Target**: Base 3 ledger sketch and `status` states (amend), 3 exit-code table (amend), 4 tier 3 (amend with Change 14).
- **Rationale**: Adopted from invariant probe (not debated). Resolution (verbatim): "A structural stop leaves the ledger in `reviewing` with an attempt counter; `open` from `reviewing` is allowed once for the same review number, reusing the same snapshot and surface; a second structural stop sets a terminal `invalid` state that every later call refuses, escalates to the user, and is recorded as a failed attempt that is never replaced."
- **Integration point**: In B's vocabulary: a structural stop leaves round N in state `open` with `attempts: 1`; one more `begin` for the same N is allowed and reuses `doc-r<N>.md` and `surface-r<N>.md` unchanged; a second structural stop sets the terminal state `invalid`; every later subcommand exits 4 with `halt: invalid`; the coordinator escalates to the user; the recorder counts the replicate as a failed attempt (Change 35).
- **Risk**: Medium. New state; covered by state-machine tests (Change 39).

### Change 16: `resolved by=<hunk>` replaces the forced-open rule; carried severity is pinned (from Variant A)
- **Source**: Variant A, rule C8 ("`resolved` carries `by=<hunk of this surface>`") and V4 ("Severity is pinned once recorded").
- **Target**: Base 4 rule C10 (replace), 3 surface example line `anchor_untouched: yes (... cannot be marked resolved)` (replace), 7 table row "Prior-findings table" (amend).
- **Rationale**: C-020, A at 75%. Also resolves INV-005 (ADDRESSED, with a merge instruction): B's C10 would make an FR-8/FR-9 gap finding fixed by an insertion elsewhere unresolvable; the probe says "the C-010 merge (A+C) does not say B's C10 is dropped; it must be."
- **Integration point**: New C10 (hard): `PRIOR <id> resolved` carries `by=H<k>.<n>`, a hunk of this surface; with an empty surface nothing can be resolved. `PRIOR` lines carry no severity field; a prior keeps the severity and blocking status recorded when it was raised; `regressed` re-opens an earlier id at its recorded severity. The surface keeps `fix hunks:` per prior as information, without the "cannot be marked resolved" clause.
- **Risk**: Low. One rule replaced.

### Change 17: Remove the byte budget; report bytes and hunks per id (from Variants A and B)
- **Source**: Variant A, 5 "Rejected alternatives" (byte budget) and 3.3 `gate` output `bytes_by_id`; `round2-B.md` A-W5.
- **Target**: Base 5.2 (delete the `FIX_BUDGET_BYTES` paragraph's budget part), 8.2 constants, 10 R5, 12 question 4, 8.3 test "over-budget printed" (delete).
- **Rationale**: C-015 and X-013, A+B at 95%. flg-r1: R2-2 and R2-3 changed three lines each and each produced a review-3 blocker (`round2-A.md` New evidence 2), so a size gate would not have fired where it mattered.
- **Integration point**: `fixcheck` records and prints `bytes_by_id` and `hunks_by_id` as figures only; the next surface header prints the largest fix. Keep the `new_section: H<k>.<n>` warning (427 bullet 6). Delete `FIX_BUDGET_BYTES` and `over_budget` everywhere.
- **Risk**: Low.

### Change 18: A `withdrawn` status for a declined false positive (adopted from invariant probe (not debated))
- **Source**: `invariant-probe.md` INV-004 (HIGH, UNADDRESSED), Resolution line.
- **Target**: Base 4 report grammar and rule C9 (amend), 5.2 rule M2 (amend), 9 counting rules (amend).
- **Rationale**: Adopted from invariant probe (not debated). Resolution (verbatim): "Add `DG-STATUS <id> withdrawn quote=... reason=...`, legal only for an id the reviser declined in the preceding fix map; a withdrawn id leaves the open blocking set but stays in the R3 proxy at its recorded label, and any withdrawal turns the verdict into a scoped PASS that cannot earn clean-PASS credit."
- **Integration point**: In B's grammar the line is `PRIOR <id> withdrawn quote="..." reason="..."`. C9 allows `withdrawn` only for an id with a `declined` line in `fixmap-r<N-1>.txt`. A withdrawn id leaves the open blocking set, stays in `R3-proxy-all` at its recorded label (Change 31), and sets `acceptance: scoped` (Change 14).
- **Risk**: Medium. A new exit from the open set; bounded by the declined-only rule and by proxy counting.

### Change 19: Fix-map hardening: pre-fill, several owners per hunk, bound to the document hash, bounded retries (from Variant B Round 2 and the invariant probe)
- **Source**: `round2-B.md` response to round2-A item 4 (pre-fill from inline tags); `invariant-probe.md` INV-024, INV-003, INV-009; base 2 step 5 ("at most 3 runs, then stops and says so").
- **Target**: Base 5.2 rules M1 to M3 (amend), 2 step 5 (amend), 3 `fixcheck` row (amend).
- **Rationale**: C-014, B at 95% (explicit map with `declined` is the base; Round 2 added pre-fill). INV-024 (ADDRESSED with a merge instruction): R3-4 sits on text from R2-1 and R2-4, so "B's map line format `H<i> R<N>.<j>` must allow several ids". INV-003 (MEDIUM): positional hunk ids shift if the spec is edited after the map is written. INV-009 (MEDIUM): no cap on gate retries per fix cycle.
- **Integration point**: (a) `fixcheck` pre-fills `fixmap-r<N>.txt` candidates from inline `R<N>.<j>` tags in added text; the reviser confirms or writes `declined`; the file stays the authority. (b) Map line `H<k>.<n> R<N>.<j>[,R<N>.<m>...]`: one hunk may name several blocking ids. (c) First line of the map is `doc_sha: <sha>` as printed by the last `fixcheck`; a mismatch with the current spec exits 1 ("the map was written against another document"). (d) After the third failing `fixcheck` in one cycle the ledger records `fix-rejected` for that cycle, the reviser stops, the coordinator escalates to the user, and no review is consumed.
- **Risk**: Low. Each item is a small rule with a test.

### Change 20: Word-identical changes that alter Markdown structure are surfaced (from the invariant probe, MEDIUM item)
- **Source**: `invariant-probe.md` INV-025; `round2-C.md` New evidence 2 (`1. First\n2. Second\n` to `1. First 2. Second\n`).
- **Target**: Base 3 diff step 3 (amend, the reflow filter).
- **Rationale**: INV-025 (MEDIUM, UNADDRESSED): A's and B's reflow filter (kept by X-003 and C-022, A+B at 75%) drops a token-identical block that merges two list items, leaving an unreviewed, unowned structural edit.
- **Integration point**: Drop a word-identical block only when the count of lines that start with a Markdown list marker, heading marker or table pipe is the same on both sides; otherwise keep it as a hunk with `structural: yes` that needs an owner in the fix map and is eligible in the next review.
- **Risk**: Low. Narrows an exclusion; one fixture.

### Change 21: Ledger replay, exclusive-create lock and input limits (from Variants A and C)
- **Source**: Variant A, 4.4 (`open` replays `check` on the recorded report); Variant C, 3 ("short exclusive-create lock", "Refuse symlink state paths") and 10 ("at most 2 MiB per document, 100,000 physical lines and 1,000 finding/status entries per draft").
- **Target**: Base 3 ledger paragraph (amend), 10 R11 (replace), 2 skip list (amend).
- **Rationale**: C-035, A+C at 95% (`round2-A.md`: "Ledger replay plus C's lock and size limits"). B adopted the replay and lock in Round 2 (`round2-B.md` A-W7); the winning merge keeps C's limits as well.
- **Integration point**: `begin` re-runs `check` on the recorded report (its `report_sha` must still match) against the recorded surface and recomputes verdict and blocking ids; any difference with `ledger.json` exits 6. All writes take an exclusive-create lock file in `<dir>`; symlinked state paths are refused; inputs over 2 MiB, 100,000 lines or 1,000 machine lines exit 2 before the diff. R11 then reads "Hand edits are detected by replay; concurrent writers are refused by the lock."
- **Risk**: Low.

### Change 22: The verdict line is always the last line (adopted from invariant probe (not debated))
- **Source**: `invariant-probe.md` INV-027 (HIGH, UNADDRESSED), Resolution line.
- **Target**: Base 2 step 12 and "Early exit" (amend), 6 "Surfaced once" (amend), 8.1 `## Diffgate` item 6 (amend), 8.3 command test row (amend).
- **Rationale**: Adopted from invariant probe (not debated). Resolution (verbatim): "The last non-blank line of every report is the verdict line; the deferred appendix and any scoped-acceptance note are written above the Reviser brief and the verdict, and a test asserts the last line is exactly `verdict: PASS` or `verdict: FAIL`."
- **Integration point**: Report order at a closing review: findings block, `## Deferred (pre-existing, not looped on)` with the contents of `deferred.md`, the scoped-PASS line if any (Change 14), the Reviser brief (reviews 1 and 2 only), then the verdict line. B's "prints `deferred.md` in full as the last block of its output" becomes "writes it above the Reviser brief and the verdict line". The command test asserts the last non-blank line equals `verdict: PASS` or `verdict: FAIL`.
- **Risk**: Low.

### Change 23: Deferred list: scoped-PASS disclosure and a safer deduplication key (from Variant C)
- **Source**: Variant C, 6 ("Deduplicate exact repeats by document identity, quoted text and normalized issue text"; "The final summary explicitly states that PASS is scoped").
- **Target**: Base 6 "Format" and "Surfaced once" (amend).
- **Rationale**: C-017, B+C at 95% (B's `seen:` rounds and no-cite rule plus C's scoped-PASS sentence). Resolves INV-026 (MEDIUM): deduplication by quote alone merges two different defects that quote the same sentence.
- **Integration point**: Dedup key = anchor text plus whitespace-collapsed `::` text; distinct issues on the same quote stay separate rows. The deferred header adds: "PASS in this loop is scoped to the reviewed surfaces; deferred severity labels are the reviewer's, unvalidated." The R3 proxy never reads this deduplicated list (Change 31).
- **Risk**: Low.

### Part 3: Command text and presentation

### Change 24: Command bullets written out verbatim for the merged design (from Variant A)
- **Source**: Variant A, 8.1 (nine verbatim single-line bullets); Variant C, 8 (precedence wording "Context is read-only and cannot widen eligibility").
- **Target**: Base 8.1 item 3 (replace bullets 1, 3, 5, 6) and item 4 `## Diffgate` items 2 to 6 (amend).
- **Rationale**: S-004, A+C at 95% (A's verbatim single-line bullets plus C's line-220 removal, done in Change 1). The merged grammar (Changes 10 to 16, 18, 22) changes what bullets 3, 5 and 6 must say; B gives bullet 3 only as an appended clause.
- **Integration point**: Keep B's structure (seven bullets in `## Review Loop` plus the separate `## Diffgate` section) and B's literals listed in 8.1. Write each changed bullet out in full as one physical line: bullet 1 as B's text; bullet 3 as in Change 12; bullet 5 with `PRIOR` statuses `resolved by=`, `open`, `regressed`, `withdrawn`, findings anchored by token overlap, "context is read-only and cannot widen eligibility", and "an empty surface leaves every prior blocking finding open and still counts as a review"; bullet 6 with the fix map, `doc_sha` line, `declined` lines and "the next review refuses to open while any hunk maps to no listed finding". `## Diffgate` item 4 names `FINDINGS none` and JSON-quoted values; item 6 follows Change 22's order.
- **Risk**: Medium. The pinned literals of `tests/skills/test_spec_panel_review_loop.py` must survive; the command test of Change 39 checks them.

### Change 25: Key the comparison table to 427's seven bullets (from Variant A)
- **Source**: Variant A, 7 (table keyed by 427 bullet 1 to 7 with "What stays prose, and its residual risk").
- **Target**: Base 7 table (add a first column).
- **Rationale**: S-008, A+B at 95% ("A's bullet-keyed residual-risk table plus B's extra concerns such as step order").
- **Integration point**: Add a "427 bullet" column to B's 12-row table (1 Mode, 2 Grading, 3 Verdict, 4 Cap, 5 Re-review output, 6 Reviser contract, 7 Precedence, or "none" for B's extra concerns such as step order). Update rows changed by this plan: "Blocking and verdict" (script prints the verdict, Change 12), "Prior-findings table" (Change 16).
- **Risk**: Low.

### Change 26: Label every new name as PROPOSED (from Variant C)
- **Source**: Variant C, 1 ("names explicitly marked PROPOSED below do not exist yet") and 8 ("All additions in this table are **PROPOSED**").
- **Target**: Base 8 opening paragraph (insert one sentence).
- **Rationale**: S-007, B+C at 95% (B's UNVERIFIED tags and replay plus C's PROPOSED labels).
- **Integration point**: "Every file, subcommand, flag, constant and test named in sections 2 to 8 and 13 is PROPOSED and does not exist yet; existing files are cited with line numbers."
- **Risk**: Low.

### Change 27: Script outline with A's signatures, the profile seam and the merged constants (from Variant A)
- **Source**: Variant A, 8.3 (typed function list) and 3.6 (`PROFILES` dict, `CAP_REVIEWS = 3` as a module constant).
- **Target**: Base 8.2 script outline (replace the constants line and add functions).
- **Rationale**: S-005, A+B at 95% (A's signatures fix the interfaces; B's named constants and line budget bound the size); C-034, A+C at 95% (the `PROFILES` seam is the extension point for later adopters).
- **Integration point**: Constants: `CAP_REVIEWS = 3; MERGE_GAP = 2; VIA_CAP = 2; FORMAT = "diffgate/1"; PROFILES = {"spec-panel": {"sev": ("critical", "major", "minor"), "blocking": _spec_panel_blocking}}`; exit constants unchanged. Add `tokens(lines)`, `quote_spans(doc, quote)`, `replay(ledger)`, `derive(parsed, profile, prior)` to B's list, and rename `build_hunks` to cover both diff passes. Keep B's per-part line budget, raised by the token pass and replay to about 420 lines; the cut order stays (`status`, then the `new_section` warning).
- **Risk**: Low.

### Part 4: Measurement, forecast and falsification

### Change 28: Replace the forecast with the Round 2 consensus and state the theme's limit (from the Round 2 debate)
- **Source**: `round2-A.md`, `round2-B.md`, `round2-C.md`, each section "flg-r1 evidence: revised prediction and any in-theme lever"; `debate-transcript.md` Convergence Assessment; `debate/evidence-flg-r1.md`.
- **Target**: Base 9 predictions table and probability lines (replace); 1 "What stays unfixed" (amend); 5.5 (amend).
- **Rationale**: C-023 and X-007, B at 95%; C-024 tie at 75% (growth). Round 2 consensus: "no mechanism inside the diffgate theme lowers blocking-fix-induced blockers without relabelling or hiding them; forecast R3 proxy mean about 3.0 to 3.5, P(both replicates at 3 or fewer) about 0.2 to 0.25, growth about 20% to 27% (bar 44.4%)". Also INV-037 (ADDRESSED): the summary claim "converge or escalate justifiably" must read "escalate with an interpretable record". U-020 (C): growth for an early PASS is carried forward.
- **Integration point**: Predictions table: R3-proxy-all mean about 3.0 to 3.5 (a flg-r1-like replicate about 4 to 5: four blockers on blocking-fix text plus R3-8's MAJOR label, R3-7 removed; a flg-r2-like replicate about 1 to 2); P(both replicates at 3 or fewer) about 0.2 to 0.25; P(F1 fires in at least one replicate) about 0.5 to 0.55; growth after two fix cycles about 20% to 27% (P about 0.9 for the 44.4% bar); clean PASS by review 3 about 10% per replicate. Add verbatim: "No mechanism inside the diffgate theme (computed surface, anchor checker, fix gate, ledger) lowers the count of blocking-fix-induced blockers without relabelling or hiding them. In flg-r1 all 4 review-3 blockers sit on text written by blocking fixes, and a blocking-only gate removes only R3-7." State that the experiment's most likely product is a measured per-blocking-fix defect rate under scope control, and that the design's claim is "escalate with an interpretable record", not convergence. Early PASS: carry the terminal document forward to the scheduled endpoint for growth.
- **Risk**: Low. Text; it lowers the stated expectation to match the evidence.

### Change 29: Merged failure conditions (from Variants A, B and C)
- **Source**: Variant B, 9 F1 to F4; `round2-B.md` "Two edits to B that follow" (F1 re-based on the bar); Variant A, 9 conditions 3 to 5 (blindness audit, demotion share, stall); Variant C, 9 spread check.
- **Target**: Base 9 "What result would mean the idea failed" (replace F1; add conditions).
- **Rationale**: C-025, A+B+C at 95% ("B's F1 as the primary diagnosis, A's blindness and demotion conditions, C's spread check"). The detailed F1 share computation is Change 30; the spread check's role is fixed by Change 32.
- **Integration point**: F1 (re-based): "the R3 proxy is above 3 in a replicate and at least 70% of that replicate's review-3 critical+major findings sit on blocking-fix hunks by ledger ancestry (Change 30)". F2 and F4 as in the base. F3 replaced by A's blindness condition: "the blindness audit finds 2 or more blockers in fix-written text the loop closed, in either replicate" (Change 34). Add A's "more than a quarter of new findings in reviews 2 and 3 are demoted or degraded, or the gate fails more than once per fix cycle on average" and "a replicate stalls (no review 3 delivered)". Report the label proxy and the 427-blocking count side by side (`round2-B.md`).
- **Risk**: Low.

### Change 30: F1 share computed over all-discovered findings by ancestry (adopted from invariant probe (not debated))
- **Source**: `invariant-probe.md` INV-016 (HIGH, UNADDRESSED), Resolution line.
- **Target**: Base 9 F1 and "Extra recordings" ("share of review-3 blockers sitting on mapped fix hunks", replace).
- **Rationale**: Adopted from invariant probe (not debated). Resolution (verbatim): "Compute the F1 share over all-discovered review-3 critical+major findings (blocking, deferred and demoted), each classified by ledger ancestry as on a blocking-fix hunk, on a minor or unmapped edit, or on unchanged text, and state in the pre-registration that the blocking-only share is 100% by construction."
- **Integration point**: Add a pre-registration sentence: "In the treatment arm every blocking new finding sits on a mapped fix hunk by construction (the gate admits no unmapped hunk), so the blocking-only share is 100% and is not a diagnostic." The ancestry classification uses the ledger's per-hunk owners; for control and Arm B it uses `disposition*.md` changed-line lists, as in `debate/evidence-flg-r1.md`.
- **Risk**: Low.

### Change 31: One R3 proxy function for every arm (adopted from invariant probe (not debated))
- **Source**: `invariant-probe.md` INV-015 (HIGH, UNADDRESSED), Resolution line.
- **Target**: Base 9 "Counting rules fixed before the run", primary metric `R3-proxy-all` (replace the definition).
- **Rationale**: Adopted from invariant probe (not debated). Resolution (verbatim): "Define the R3 proxy as one function applied to every arm's review-3 report and ledger: CRITICAL or MAJOR labels on (a) findings first raised in review 3, deferred and demoted included, and (b) prior blocking findings marked open or regressed in review 3, at their recorded label, each id counted once within review 3 only; recompute the control and Arm B with the same function before comparing." C-026 and X-008 (A+B at 95%) already put deferred findings in the bar metric; this fixes how.
- **Integration point**: `R3-proxy-all` = that function. Withdrawn priors (Change 18) count at their recorded label. Recompute control (8, 4) and Arm B (6, 1) with it and publish the recomputed values beside the historical ones before any treatment replicate is scored.
- **Risk**: Low. Historical values may move; that is the point.

### Change 32: Three pre-registered result classes and the reachable form of the spread check (adopted from invariant probe (not debated))
- **Source**: `invariant-probe.md` INV-036 (HIGH, UNADDRESSED), Resolution line; `round2-B.md` "gate Stage C ... on the pre-registered result classes".
- **Target**: Base 9 (new paragraph after the failure conditions); 8 Stage C (amend).
- **Rationale**: Adopted from invariant probe (not debated). Resolution (verbatim): "Pre-register before any replicate that S1 at n=2 returns only one of three result classes (bar met; bar missed with F1; bar missed without F1), that the spread check is reported but cannot be met unless the treatment mean is below 2.0, and that any claim of a proven effect needs a replicate count fixed in advance." C-025 keeps C's spread check; with control mean 6.0 and spread 4, the forecast effect of 2.5 to 3.0 cannot exceed it.
- **Integration point**: Paragraph "Result classes (pre-registered)": the three classes as quoted; "the spread check (C 9) is reported; it can be met only if the treatment mean is below 2.0"; "a claim that diffgate has a proven effect requires a replicate count fixed before the first run". Stage C: "only if the S1 bar is met" becomes "decided on the result class, never on the bar alone".
- **Risk**: Low.

### Change 33: Claim the combined treatment; name the briefs-only arm (adopted from invariant probe (not debated))
- **Source**: `invariant-probe.md` INV-034 (HIGH, UNADDRESSED), Resolution line.
- **Target**: Base 9 "Design" paragraph (amend); 8.5 brief substitution (amend).
- **Rationale**: Adopted from invariant probe (not debated). Resolution (verbatim): "Pre-register the S1 claim as the combined treatment (script plus a published brief diff) and state that a pass does not support 'mechanical over prose' until a briefs-only arm with the same brief lines and no script is run." All three advocates rejected shared assumption A-004 in Round 2.
- **Integration point**: 9 Design: "The treatment is the script plus the brief diff published in 8.5. A pass does not support 'mechanical over prose'; that claim needs a briefs-only arm with the same brief lines and no script." 8.5: publish the exact before and after text of every changed brief line in the run log.
- **Risk**: Low.

### Change 34: Mandatory blindness audit classified by ledger history (from Variant A)
- **Source**: Variant A, 9 "Blindness audit (out of loop, not counted in the bar)".
- **Target**: Base 9 "Blind audit (report only, not a bar)" (replace).
- **Rationale**: C-033, A at 95% (all three agree in Round 2). Also resolves INV-040 (MEDIUM): A's audit counts only misses in fix-written text, so a lower proxy that comes from the reviewer no longer raising pre-existing defects would go unseen; the probe notes A-002 was qualified or rejected by all three.
- **Integration point**: After the loop, one fresh `/sc:spec-panel --mode critique` review 1 of the final document per replicate, in a new session with no ledger, for every arm, not "if budget allows". Classify each blocker by ledger history: fix-written text the loop closed (what diffgate hides; feeds F3 in Change 29) or text present since the original. Report the second class beside the deferred count and compare it with the same audit on the control and Arm B final documents, so a drop in raised pre-existing defects is visible. Record findings per changed token per review (density).
- **Risk**: Low. Adds one review session per replicate (Change 37 counts it).

### Change 35: Validity rules for recovery compliance and review-1 comparability (from the invariant probe, MEDIUM items)
- **Source**: `invariant-probe.md` INV-038, INV-039, INV-033 (ADDRESSED), INV-019 (ADDRESSED); `round2-C.md` New evidence 5 (frozen attempt slots).
- **Target**: Base 9 "Validity gate (new)" (replace "An invalid replicate is rerun, not scored").
- **Rationale**: INV-038 (MEDIUM): all three qualify A-001 as a validity input but none says what a non-compliant replicate does. INV-039 (MEDIUM): the review-1 comparability check (13 to 17 blockers, as in Arm B) has no stated consequence. INV-033 requires the recorder to void, not count, a replicate whose checks disagree. INV-019 and C's evidence: quietly rerunning invalid slots changes the compared population.
- **Integration point**: Attempt slots are fixed before the run (two per arm). A replicate is void when the transcript and the ledger disagree, the state directory or run changes mid-loop, a state file was hand-edited (replay exit 6), plain `/sc:spec-panel` ran, or the run ended `invalid` (Change 15). A void replicate is reported with its cost as a failed attempt, never scored and never silently replaced; any rerun is a separately declared decision. If a valid replicate's review-1 blocker count falls outside 13 to 17, the result is still scored but labelled "review 1 not comparable" and cannot be credited as evidence for the mechanism. Report completion rate per arm.
- **Risk**: Low.

### Change 36: Pre-run gate, install hashes and invocation evidence (from Variants A, B and C)
- **Source**: Variant A, 8.9 ("`sha256sum ~/.claude/commands/sc/spec-panel.md` # must equal the value recorded before the run"; "Never `superclaude install --force`"); Variant C, 8 ("Verify that call order in the transcript"); base 12 question 1; `invariant-probe.md` INV-010 (ADDRESSED, HIGH) and INV-006 (MEDIUM).
- **Target**: Base 8.5 (amend), 9 Design (insert "Pre-run gate"), 12 question 1 (move into the gate).
- **Rationale**: C-028, A+B+C at 95% ("A's hash of the untouched `spec-panel.md` and no `--force`, B's `--expect-round`, C's installed-file hashes and transcript check"). INV-010: worker permission for `uv run` "must be a pre-run gate in the merged plan, not an open question". INV-006: if reviewer and reviser run in different checkouts, the recorded document path fails every later `begin`.
- **Integration point**: Pre-run gate, before any replicate: (1) one worker in the experiment's permission mode runs `status` through the installed path without a prompt; (2) the reviewer and reviser workers of a replicate run in one checkout and pass the same `--doc` real path, checked by a dry `begin` and `status`; (3) a worker resolves `/sc:spec-panel-diffgate` after restart. Record `sha256sum` of `~/.claude/commands/sc/spec-panel.md` before the run and check it after each step; record hashes of the new command and `diffgate.py`; never `superclaude install --force`. Per replicate, the transcript must show the variant command and each `diffgate.py` call in step order.
- **Risk**: Low.

### Change 37: Full cost envelope (from Variant C)
- **Source**: Variant C, 10 "Cost envelope" ("For 20 findings with multiple anchors, parent Read-back can cost more than the helper itself. Do not call this free or count only Python runtime").
- **Target**: Base 10 cost table (add rows), 9 "Extra recordings" (amend).
- **Rationale**: C-027, C at 95% (A: "A's estimate omitted correction turns"); S-009, A+C at 95% (A's residual column plus C's separate cost envelope; B's risks already carry residuals).
- **Integration point**: Add rows: correction turns per rejected report (1 extra reviewer response and 1 `check` each), `fixcheck` failures per cycle and their reviser turns, the blindness-audit session per replicate (Change 34), void or `invalid` attempts and their cost, and the coordinator's dispatch time. Wall-time estimate becomes a range including correction turns, marked UNVERIFIED until the step times are recorded.
- **Risk**: Low.

### Part 5: Structure, tests and remaining sections

### Change 38: Later adopters keep the profile seam and C's limits (from Variants A and C)
- **Source**: Variant A, 11 (`PROFILES` entry per adopter); Variant C, 11 ("`/sc:implement` final review: do not replace it with this scoped gate"; rf-qa "must not weaken or silently duplicate" its monotonicity guards).
- **Target**: Base 11 table (amend rows rf-qa and `/sc:implement`).
- **Rationale**: C-034, A+C at 95%.
- **Integration point**: rf-qa row: "adds an `rf-qa` profile (CRITICAL and IMPORTANT blocking, MINOR a note); must not weaken rf-qa's regression and monotonicity guards". `/sc:implement` row: "do not replace the final review; at most a checked delta surface for a narrowly authorized repair after it, with a fresh full final review kept for archive acceptance".
- **Risk**: Low.

### Change 39: New section 13 "Test plan" in tiers (from Variant C, with A's and B's cases)
- **Source**: Variant C, 13 (P0 eligibility, P0 reviser authorization, P0 state machine, P1 command and install); Variant A, 8.4 (16 cases); base 8.3 test row; `round2-B.md` New evidence 7 (flg-r1 fixture); `round2-C.md` New evidence 2 and 3.
- **Target**: Base, new top-level section 13 after section 12; base 8.3 keeps the file list and points to section 13 for cases.
- **Rationale**: S-001 and S-002, C at 95%; C-030, A+B+C at 95% ("A's two existing-test edits, B's drift guard with a `## Tool Coordination` exemption, C's isolated-HOME install test").
- **Integration point**: P0 script cases: B's list minus the removed budget and verdict-mismatch cases, plus A's token-level cases (one changed word in a 300-character line yields one hunk whose changed span is that word), a `side=old` deletion anchor, a quote occurring in both changed and unchanged text (Change 11), the structural list-merge fixture (Change 20), a two-owner hunk (Change 19), `withdrawn` legal only after `declined` (Change 18), the structural-stop sequence ending `invalid` (Change 15), replay detecting a hand-edited ledger (Change 21), and the flg-r1-shaped fixture (four mapped blocking fixes, four new blockers on them, one MAJOR graded minor on a shared line, one minor-only line; expected: all four fix hunks allowed, minor-only line rejected, chains of length 3, F1 fires, label proxy 5, blocking 4). P1: command text test (literals, both script paths with home first, no `src/superclaude`, last non-blank line exactly a verdict line per Change 22, drift guard with the `## Tool Coordination` exemption); the two existing-test edits (Changes 2 and 3); an isolated temporary-HOME install test that installs the command and `sc-diffgate`, runs the script's `--help` outside the repository, and asserts a sentinel `spec-panel.md` is byte-unchanged. Run with `uv run pytest`.
- **Risk**: Low. Tests only.

### Change 40: New section 14 "Acceptance criteria", separate from experiment success (from Variant C)
- **Source**: Variant C, 14 (15 numbered criteria; "Implementation acceptance is separate from experimental success").
- **Target**: Base, new top-level section 14 after section 13.
- **Rationale**: S-003, C at 95% (`round2-A.md`: "with C's criterion 15 moved to the experiment gate as C concedes").
- **Integration point**: Adapt C's criteria 1 to 14 to the merged design: additive delivery without plugin mirrors (C-032); portable invocation through the installed `sc-diffgate` path; deterministic surface; strict scope with deferral, not report rejection, for unanchored findings (C-012); deletion correctness; report integrity including `FINDINGS none`; script-derived verdict as the last line; fix ownership by explicit map with `declined`, without footprints; one-look rule; bounded execution including `invalid` and `fix-rejected`; safe state (lock, replay, limits); deferred disclosure with the scoped-PASS sentence; unattended compatibility with the verbatim section; regression evidence including both existing-test edits. C's criterion 15 (S1 screen) moves to section 9 as the result classes of Change 32.
- **Risk**: Low.

### Change 41: Give every open question a default and close the answered ones (from Variant C)
- **Source**: Variant C, 12 ("These questions do not leave the initial interface undefined. Defaults above govern the first experiment").
- **Target**: Base 12 (amend every item).
- **Rationale**: S-010, B+C at 95% (B flags experiment blockers; C gives each question a default). Several base questions are answered by this plan or by Round 2.
- **Integration point**: Question 1 moves into the pre-run gate (Change 36). Question 4 is closed (budget removed, Change 17; `VIA_CAP = 2` kept and its use recorded). Question 5 is closed (script owns the verdict, Change 12). Question 7 is closed (degrade finding-level failures, stop on structure, Change 14). Question 12 is answered by `debate/evidence-flg-r1.md` (flg-r1 does not share flg-r2's composition). Each remaining question states the default used in S1.
- **Risk**: Low.

### Invariant coverage

HIGH UNADDRESSED (each adopted from invariant probe, not debated):

| Invariant | Change |
|---|---|
| INV-001 ledger state after a structural stop | 15 |
| INV-004 no way to retire a declined false-positive blocker | 18 |
| INV-015 proxy counted differently across arms | 31 |
| INV-016 F1 is 100% by construction in the treatment arm | 30 |
| INV-027 deferred appendix displaces the last-line verdict | 22 |
| INV-034 brief prose confound | 33 |
| INV-036 spread check makes a positive S1 result unreachable | 32 |

MEDIUM UNADDRESSED (one line each):

| Invariant | Disposition |
|---|---|
| INV-003 hunk ids in the fix map shift after a later edit | Change 19 (map carries `doc_sha`; mismatch exits 1) |
| INV-006 reviewer and reviser at different real paths | Change 36 (pre-run gate checks one checkout and one `--doc` path) |
| INV-009 failing fix gate has no time bound | Change 19 (third failing `fixcheck` in a cycle records `fix-rejected` and escalates) |
| INV-017 one segmentation for eligibility, ownership and the next surface | Change 9 (token eligibility inside block-level ids; `MERGE_GAP` groups only) |
| INV-022 a quote also present in unchanged text | Change 11 (the occurrence on the `at=` lines must overlap a changed token) |
| INV-025 word-identical change that merges list items | Change 20 (structural blocks surfaced and owned) |
| INV-026 deferred dedup merges distinct findings | Change 23 (key = quote plus issue text; proxy never uses the dedup) |
| INV-028 scoped PASS ambiguous to readers | Change 14 (`acceptance: scoped` field; verdict line stays exact) |
| INV-038 recovery-path compliance has no defined effect | Change 35 (void, reported, never silently replaced) |
| INV-039 review-1 comparability gate has no consequence | Change 35 (scored but labelled "review 1 not comparable", not credited) |
| INV-040 lower proxy from less attention to unchanged text | Change 34 (audit reports original-text misses against control and Arm B) |

LOW UNADDRESSED: INV-018 (range base) is closed by Change 9 (1-based, inclusive); INV-023 (one-character quotes) is closed by Change 11 (12-character minimum, no waiver).

ADDRESSED items that carried a merge instruction: INV-005 (Change 16 drops C10), INV-007 (`FINDINGS none` kept, Change 10), INV-010 (Change 36 makes it a pre-run gate), INV-024 (Change 19 allows several owners), INV-033 and INV-019 (Change 35), INV-037 (Change 28 rewording). INV-002 needs no change: base rule C3 already rejects a spec whose sha differs from the one `begin` recorded.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| C-001, X-001 | C: the coordinator runs every subcommand; the reviewer's own check is only early feedback | A+B at 95%: worker-owned steps locked to each other; "an Orca coordinator or a human is also a prose follower" (B 3); C's confirmation "checks presence, not truth, by C's own account" (`round2-A.md`). |
| C-014 | C: repair footprints approved before any edit, single owner per edit group | B at 95%: flg-r1's R2-2 and R2-3 were three-line, mapped, legitimate fixes and each produced a review-3 blocker, so footprints would have stopped neither chain (`round2-A.md` C-2, `round2-B.md` C-W4). Hardening trigger kept as a recorded condition: add footprints if the `bytes_by_id` audit finds mapped edits with no word overlap with the finding's quote. |
| C-019 | C: a MAJOR blocks only with a coordinator-confirmed wrong outcome | A at 95%; C's confirmation file is presence-only by C's own words and adds a coordinator step per finding (`round2-C.md`: "Give confirmation zero forecast benefit unless separately tested"). |
| C-011, X-002 (part) | C: a second rejected report marks the run invalid | A+B+C at 95% on the merged rule (Change 14): anchoring mistakes degrade; only structural failure stops, and then Change 15's one retry applies. With n=2, invalidating on a mistyped anchor discards a replicate (`round2-B.md`). |
| C-012, X-004 | C: an unanchored finding left in `findings` rejects the whole report | A+B at 95%: an unanchored observation is an ordinary deferral and must not spend the one repair (base rule C11 kept). |
| C-006 | C: strict JSON draft file plus coordinator confirmation file | A+B at 75%: the largest change to review 1 (shared assumption A-005); JSON-quoted line values (Change 10) give the parsing safety without it. |
| C-009 | C: digest ids `r<round>-<ordinal>-<digest>` | A at 75%: "a digest adds nothing the ledger hash lacks"; Change 8 uses `H<k>.<n>`. |
| C-022, X-003 | C: reflow and moves are real deltas, no reflow filter | A+B at 75%: a word-identical reflow carries nothing to review; base filter kept, narrowed only for structural Markdown changes (Change 20). |
| X-009 | C: every whitespace edit must have a blocking owner | A+B at 75%: whitespace-only edits are not hunks and need no owner. |
| C-032, X-011 | C: plugin mirrors of command and skill; annex appended to `docs/designs/spec-panel-review-loop.md` | A+B at 95%: `tests/commands/test_routing_plugin_parity.py` lines 42-48 pin mirrors only for README-listed commands; a separate `docs/designs/spec-panel-diffgate.md` keeps 427's design doc historical. |
| C-029, X-010 | A: ignore `--re-review`/`--baseline` with a note; C: verify them against the ledger | B at 95%: drop the flags from the variant's Usage (base 8.1 item 2). |
| C-013, X-005 | A: no unchanged-line route; anchor on the changed words only | B at 75%: quote-checked `via=` kept; flg-r1 needed it for 0 of 10 findings, so it is a narrow escape (`round2-B.md` C-W3). |
| C-008 (part) | A: a `renumber H<k>.<n>` map line accepted when only digit runs change | Unresolved point (50%). B's position kept: block-level ownership ids merge a renumbered list into one hunk with one owner, so no digit-parsing rule is added (`round2-B.md` response to round2-A item 1). Recorded under INV-017 (Change 9). |
| (A 4.2 C13) | A: `DG-COVER` line naming every hunk | A conceded in Round 2 (`round2-A.md` B-4): "costs tokens and proves nothing". |
| C-003 (part) | A: separate `final` subcommand | A+B at 95%: B's four subcommands; the end-of-loop output belongs to `check` at the closing review. |
| C-007 | A: flat files; C: per-round folders | Tie at 95%: file layout does not change behaviour; base flat files kept. |
| C-016 | Severity ceiling at review 3 | Tie at 95%: all three reject it; flg-r1 makes it "the obvious relabelling trap". |
| C-021 | Minor findings reaching the reviser | Tie at 95%: all three already keep minors away from the reviser; no change. |
| (round2-A in-theme candidate) | A: reviser cross-reference closure aid printed by the gate | All three: unmeasured, prose-dependent action; B measured no clean hit on flg-r1's four blockers. It needs its own ablation arm and must not count toward the diffgate result. |
| (base 5.3, Round 2) | B: halt or "revise by hand" rule on a length-3 chain | B withdrew any halt (`round2-B.md` response to round2-A item 3); the base already makes the chain a report line only, so no change. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | Low | Installed command names a `src/superclaude` path; grep and drift guard fail | Restore the line in 8.1 and the drift-guard text |
| 2 | Low | `test_routing_refresh.py` fails on the new command | Revert the set literal |
| 3 | Low | `test_worker_contract.py` fails or the variant's section is unpinned | Revert to base 8.3 row |
| 4 | Low | Residual wrong citations or label collisions | Revert the phrase edits |
| 5 | Low | Skill not installed or wrong path in the command | Revert to `sc-diffgate-protocol` throughout |
| 6 | Low | `begin` and `fixcheck` disagree on the gate | Revert to the recorded-acceptance check |
| 7 | Low | Model misreads exit 0 as PASS | Revert section 3 output description |
| 8 | Low | Id regex mismatch between gate and surface | Revert to `H<i>` |
| 9 | Medium | Token pass mis-segments hunks; anchors wrongly rejected or accepted | Revert to B's line-level hunks with `MERGE_GAP` eligibility |
| 10 | Medium | Report parser and examples inconsistent | Revert to `[[...]]` grammar in all sections together |
| 11 | Medium | First-try reject rate rises (F4) | Revert C5 and C6 to base text |
| 12 | Low | Report without verdict line if the command skips the append | Revert C1 and C13 |
| 13 | Low | Thin outcomes make a MAJOR block | Restore `OUTCOME_MIN` |
| 14 | Medium | Runs stop without verdict more often, or scoped PASS misread | Revert to base tier 3 (degrade everything) |
| 15 | Medium | Ledger stuck in `open` or `invalid` | Revert state additions with Change 14 |
| 16 | Low | A `resolved` claim on an unrelated hunk is accepted | Restore base C10 |
| 17 | Low | Large fixes go unflagged | Restore the advisory budget |
| 18 | Medium | `withdrawn` used to exit genuine blockers | Remove the status; scoped PASS and proxy counting bound the harm meanwhile |
| 19 | Low | Map rejected for a stale `doc_sha` after a benign edit | Revert map header and retry cap |
| 20 | Low | Extra structural hunks need owners | Revert to the plain reflow filter |
| 21 | Low | Lock left behind after a crash blocks the next step | Revert lock and limits; keep replay |
| 22 | Low | Deferred list order wrong in some path | Revert section 6 ordering text |
| 23 | Low | Duplicate deferred rows | Revert dedup key |
| 24 | Medium | A pinned 427 literal lost from a bullet | Revert to base bullets; re-apply Changes 12 and 16 as clauses |
| 25 | Low | None (presentation) | Remove the column |
| 26 | Low | None (presentation) | Remove the sentence |
| 27 | Low | Outline and rules disagree | Revert 8.2 outline |
| 28 | Low | Forecast misquoted from Round 2 | Revert section 9 table |
| 29 | Low | Overlapping failure conditions | Revert to base F1 to F4 |
| 30 | Low | Ancestry classification ambiguous for control arms | Revert to blocking-only share with the 100% caveat |
| 31 | Low | Historical values recomputed incorrectly | Publish both historical and recomputed values |
| 32 | Low | None beyond expectation setting | Revert paragraph |
| 33 | Low | None beyond claim wording | Revert paragraph |
| 34 | Low | Added session cost | Return to "if budget allows" |
| 35 | Low | Fewer scored replicates | Revert to base validity gate |
| 36 | Low | Setup delay before the first replicate | Remove gate items individually |
| 37 | Low | None (accounting) | Remove rows |
| 38 | Low | None (adopter guidance) | Revert rows |
| 39 | Low | Tests missing for merged rules | Not applicable (additive) |
| 40 | Low | None (new section) | Remove section 14 |
| 41 | Low | Open questions stale | Revert section 12 |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-08T15:36:46Z
- Note: the debate gate is BLOCKED_BY_INVARIANTS; Changes 15, 18, 22, 30, 31, 32 and 33 adopt the seven HIGH Resolutions as written and are recorded as adopted from the invariant probe, not as debated outcomes.
