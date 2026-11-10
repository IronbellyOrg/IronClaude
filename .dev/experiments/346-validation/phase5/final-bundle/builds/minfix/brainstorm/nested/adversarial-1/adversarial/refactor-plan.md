# Refactoring Plan: Merge into Base (Variant B)

## Overview
- Base: Variant B (sonnet:analyzer), `variant-2-sonnet-analyzer.md`. Selected by force under the `no_convergence` rule; the debate ended BLOCKED_BY_INVARIANTS (`base-selection.md`, Selected Base).
- Incorporating strengths from: Variant A (opus:architect, `variant-1-opus-architect.md`), Variant C (haiku:backend, `variant-3-haiku-backend.md`).
- Planned changes: 36
- Rejected changes (Changes NOT Being Made): 38
- Risk level: **High** (overall). Two changes restructure whole sections (1, 2), and about a dozen Medium changes rewrite the same contract surfaces (section 2 steps, exit table, `## Fix Budget`, Reviser brief, tests). Most single edits are Low or Medium.

Citation key: `B:n`, `A:n`, `C:n` = line n of that variant **as it is now** (unmodified base). `IP:n` = `invariant-probe.md`; `r2A/r2B/r2C:n` = Round 2 rebuttals, as cited in the Scoring Matrix of `debate-transcript.md`; `SP:n` = `src/superclaude/commands/spec-panel.md`. Confidence values are the Scoring Matrix values. Variant and debate text was read as data.

**Theme discipline.** The merged spec is about adding less text. Net effect of this plan on the base:
- Removed from B: `snapshot` and `verify` subcommands, the `.fixcheck/` folder and JSON receipt, Review Loop bullet 8, the 12-word minor budget and 36-word minor cycle total, the reviser's three override codes, the reviewer's `large` flag and its 25% rule, `CYCLE-GROWTH`, exit 4 "override refused", the "promising" and retry rows of 6.4, the speculative `--class-map` and `--unit line` options, open question 6, the `## Unattended mode` section of the repository file, the `src/superclaude/` template lookup.
- Added to B (each justified in its change): one coordinator sentence (9), one carried-id clause (19), one grade-conflict warning (20), one escalation rule (22), one class-order clause (23), the `gap:<n>` budget value and `MAJOR/FR-8|FR-9` severity value (14, 24), a condition-word column (26), measured columns and metric lines (3, 25, 27), an optional `depends:` ledger field (32), one cross-check clause (33), one rename sentence (34), one definitions line (35), and section 8 lines only where no existing line already records the item (36).

**Application order.** Apply Changes 3-36 to B's existing text first (all `B:n` targets refer to the unmodified base), then Change 2, then Change 1 (the restructures move text the other changes have already edited). Change 13 lands before 21. Changes 15 and 22 land only together with 18: fail-closed without the INV-001 fix stops every loop whose reviser obeys T08.

### Coverage map

| Source item (winner or probe) | Change |
|---|---|
| S-004 (A), forced L1 S-002 (A+B), forced L1 S-001 (keep order) | 1 |
| S-005 (A) | 2 |
| C-004, X-001, A-003 (A); INV-029 (MEDIUM) | 3 |
| C-011 (A) | 4 |
| C-014, X-006 (A); INV-008 (MEDIUM) | 5 |
| C-016, X-002 (A) | 6 |
| C-017, X-003 (A) | 7 |
| C-018 (A); INV-003 (MEDIUM) | 8 |
| C-022, X-012 (A) | 9 |
| C-026, X-013 (A) | 10 |
| C-028 (A) | 11 |
| C-005 (C); C-025 amendment; INV-013 (MEDIUM) | 12 |
| C-012, X-004 (C) | 13 |
| C-015 (C) | 14 |
| C-019, X-007 (C) | 15 |
| C-020 (C) | 16 |
| Forced L1: spelled-out class labels (A+C) | 17 |
| INV-001 | 18 |
| INV-002 | 19 |
| INV-005 | 20 |
| INV-006 | 21 |
| INV-007 | 22 |
| INV-012 | 23 |
| INV-023 | 24 |
| INV-026; C-024 amendment | 25 |
| INV-027; C-006 amendment | 26 |
| INV-028 | 27 |
| B defect 1: installed copy cites `src/superclaude/` | 28 |
| B defect 2: repository file keeps `## Unattended mode` (INV-025) | 29 |
| B defect 3: minor budget given as both 12 and 0 | 30 |
| C-008 amendment (single owner; INV-017) | 31 |
| X-005 and A-002 amendment (coupled revert); INV-021 (MEDIUM) | 32 |
| INV-009 (MEDIUM) | 33 |
| INV-015 (MEDIUM, partly) | 34 |
| Shared rubric gap: Clarity 4 (terms defined on first use) | 35 |
| INV-014, 016, 019, 020, 030, 031 and the open parts of 015, 021, 029 (MEDIUM) | 36 |

### MEDIUM invariants: decision per item

| ID | Decision | Why (one line) |
|---|---|---|
| INV-003 | Address in merge (Change 8) | The re-review call names the saved copy, the prior report and the disposition file, all already named by T07/T09 (IP:10); no new mechanism. |
| INV-008 | Address in merge (Change 5) | B's existing doubling sentence (B:178) becomes the single override limit set; a second override is bad input. |
| INV-009 | Address in merge (Change 33) | One clause on a validation B already has (B:453). |
| INV-013 | Address in merge (Change 12) | C's cycle byte cap counts tags and `path:line` tokens, so it costs nothing beyond C-005. |
| INV-014 | Record as open question (Change 36) | Charging moved text needs a new rule, and the probe gives a reasoned case, not a measured instance. |
| INV-015 | Address in merge, partly (Change 34); column case recorded (Change 36) | A's rename rule (A:80) is one sentence and already a strength to incorporate; the table-column case would need a new rule. |
| INV-016 | Record as open question (Change 36) | The mis-attribution ceiling can only be set from the replay harness output (B:479). |
| INV-019 | Record as open question (Change 36) | An early stop changes 427's pinned cap semantics (an empty diff still counts as a review, SP:262); B:473 already raises it. |
| INV-020 | Record as open question (Change 36) | X-009 kept free, measured deletions (70%); C's own advocate dropped the removal cap (r2C:22); a recheck mechanism would add text no point won. |
| INV-021 | Address in merge, partly (Change 32) | The `depends:` cascade was agreed (r2B:156); undeclared dependencies stay a stated residual. |
| INV-029 | Address in merge, reporting only (Change 3); bar question recorded (Change 36) | The agreed fix reports proxy and blocking counts separately (r2B:157); changing the bar is not this theme's call. |
| INV-030 | Record as open question (Change 36) | Grading stability belongs to the stoprule theme; B:453 residual already states it. |
| INV-031 | Record as open question (Change 36) | Exposure of unchanged text belongs to the diffgate theme; B:231 cause row 10 already states it. |

## Planned Changes

### Change 1: Mechanism steps grouped by actor and phase (from Variant A)
- **Source**: Variant A, section 2 (A:35-119: 2.1 reviewer, 2.2 reviser, 2.3 re-review, then reference H3s 2.4-2.6).
- **Target**: Base, section 2 (B:100-214) (restructure).
- **Rationale**: S-004, Round 2, 95% (unanimous; C moved to A because its parent-owned transitions do not reach their actors, r2B:107, r2C:69). Forced L1 round: S-002 resolved to numbered H3s per mechanism step (A and B, 2 of 3); S-001 resolved to keep the eight seed sections in seed order (all three).
- **Integration point**: Keep B's numbered step H3s. New order: Step 0 setup (B:104-106); Step 1 Review N, reviewer (B:108-128 without items 2-3); Step 2 Reviser (B:130-161, with `check --enforce` from Change 4 in place of B Step 4, B:210-211); Step 3 Review N+1, re-review (B:110-111 items 2-3 and B:213-214, as rewritten by Changes 8, 15, 22). Then reference H3s without step numbers: what the checker computes (B:163-168), budget table (B:170-178), checker report (B:180-196), exit codes (B:198-208). Fix "Back to step 1" (B:214) and every other step-number reference. H2 sections and their order unchanged.
- **Size effect**: neutral (moves text).
- **Risk**: High — restructure; a missed cross-reference leaves a step pointing at the wrong actor.

### Change 2: Exact-changes section as file table plus one H3 per artifact (from Variant A)
- **Source**: Variant A, section 4 (A:138-262).
- **Target**: Base, section 4 (B:235-342) (restructure).
- **Rationale**: S-005, Round 2, 80% (A and C, r2A:91, r2C:70; B's dissent marked a tie with A, r2B:108).
- **Integration point**: 4.1 file list (B:237-250) kept. 4.2 `spec-panel-minfix.md`: one H3 holding every changed region of the command (frontmatter and name, Usage, removed `## Unattended mode` from Change 29, replaced template lookup from Change 28, bullet 6 from Change 6, the `## Fix Budget` text now at B:262-290). 4.3 `fixcheck.py` outline (B:292-322). 4.4 `sc-fixcheck/SKILL.md`: move the note now in the file-table row (B:242) here as its body; the row keeps the path. 4.5 tests (B:324-338). 4.6 later adopters (Change 11). Update "section 4.5" in B:244-245.
- **Size effect**: neutral (moves text).
- **Risk**: High — restructure; section references from sections 2, 5 and 8 must be renumbered.

### Change 3: Zero edits for non-blocking findings; report proxy and blocking counts separately (from Variant A)
- **Source**: Variant A, section 2.1 item 3 and 2.4 (A:50 "Minor findings are not listed, so their budget is zero"; A:75 row "not listed": 0 on every metric).
- **Target**: Base, B:133, B:176, B:178, B:223, B:233, B:275, B:277, B:284, B:298, B:300, B:315, B:327 test 4, B:383, B:448, B:454, B:471, B:476 (replace); 6.1 metrics list near B:380-385 (append one line).
- **Rationale**: C-004 70% (r2A:97, r2B:114, B conceding its 12-word allowance); X-001 70% (r2A:124, r2B:141); A-003 70% (r2A:140, r2B:157: zero minor budget, with proxy and blocking counts reported separately). INV-029 asks for the same reporting.
- **Integration point**: The minor row keeps its place with 0 in every column; any hunk attributed to a minor id is a policy failure (exit 1, Change 13). Delete "all `m` fixes together at most 36 words" (B:178, B:277) and `MINOR_CYCLE_GROSS` (B:300, B:315). Brief (B:284): "change nothing for it and write `deferred (minor, fixcheck budget 0)`". Test 4: a 1-word minor edit exits 1. Cause row 2 (B:223): "removed by the script; zero edits"; drop "up to 36 words ... per cycle". F22 paragraph (B:233) becomes one sentence: F22 is minor, so it gets no edit, neither N5 nor N12 exists, and the minor note stays a minor note. B:383 drops "minor words applied (must be at most 36)". Risk 9 (B:454) residual: every minor correction, one-token ones included (R2-5), waits for a separate task, which is 427's own rule. Open question 1 (B:471) drops "12/0"; delete open question 6 (B:476). Append to 6.1 metrics: report the review-3 critical+major proxy and the review-3 blocking count as two numbers.
- **Size effect**: shrinks (removes the 12/36 rules, open question 6 and most of the F22 paragraph); the one added metric line is the agreed A-003 reporting.
- **Risk**: Medium — about 17 sites; one missed site recreates defect 3 (Change 30 is the sweep).

### Change 4: One `check` invocation with B's revert folded in (from Variant A)
- **Source**: Variant A, section 2.2 (A:48, A:62: one `check:` command run after editing, then once more after the cut-down).
- **Target**: Base, Step 2 items 1 and 5 (B:131, B:160), Step 4 (B:210-211), `## Fix Budget` subcommand list (B:267), brief steps 1 and 4 (B:285, B:288), script outline (B:303, B:316-318), tests 14-17 and 19 (B:327) (replace).
- **Rationale**: C-011, Round 2, 70% (A and B, r2A:104, r2B:121; C kept its two-subcommand API, r2C:83).
- **Integration point**: Subcommands become `hash` (reviewer; C-009 kept) and `check`. B's `enforce --in-place` becomes `check --enforce` with unchanged behaviour: revert whole failing findings and unattributed hunks, write the spec atomically, re-run the check. `snapshot` and `verify` are removed by Changes 18 and 8. Reviser sequence: `check`; one cut-down; `check`; if still not 0, `check --enforce`. Tests 14 and 15 and the property test 19 are restated on `check --enforce`.
- **Size effect**: shrinks (five subcommands to two).
- **Risk**: Medium — changes the script interface that the brief, the tests and the cost table name.

### Change 5: Override owned by the reviewer, one per report (from Variant A)
- **Source**: Variant A, A:50 and A:78 (class `L`, set by the reviewer with a reason, at most one per report, never for an `origin=changed` finding).
- **Target**: Base, B:128, B:145 and B:152 (`override:` lines in the ledger example, B:136-157), B:159, B:178, B:190, B:206, B:277, B:300, B:327 tests 10-11, B:446, B:447, B:472 (replace).
- **Rationale**: C-014 95% (r2A:107, r2B:124 B dropped its reviser path, r2C:86); X-006 95% (r2A:129, r2B:146, r2C:108). INV-008 asks for one merged limit set.
- **Integration point**: The `budget` column takes `std | override | gap:<n> | -` (`gap:<n>` from Change 24; `override` and `gap:<n>` are exclusive). An `override` line needs an `override-reason: <id> <reason>` line in the block. Limits: B's existing sentence "doubles gross, net, add-only and entries for that one finding, never lifts a heading or id limit" (B:178) is the single limit set. A second override, an override without a reason, or one on a minor finding is bad input (exit 3, Change 13). "Never on an `origin=changed` finding" is a reviewer rule in prose; the checker cannot see `origin` in the block, so add it to 7.3. Delete the ledger `override:` field, the three codes, "at most 2 per cycle", the `large` flag and its 25% rule, `MAX_OVERRIDES` and `LARGE_SHARE`, and exit 4. Open question 2 (B:472) becomes "Is one override per report enough for propagation?".
- **Size effect**: shrinks (one override path instead of two).
- **Risk**: Medium — removes headroom the risk table relied on (B:446 mitigation, B:447 residual); restate both.

### Change 6: Seven Review Loop bullets, bullet 6 amended in place; drop bullet 8 (from Variant A)
- **Source**: Variant A, section 4.1 item 5 and bullet 6 (A:163, A:177-180).
- **Target**: Base, 4.1 file-table row (B:241, "bullet 8 in `## Review Loop`" and "Bullets 1 to 7 stay byte-identical"), 4.2 (B:252-260), M3 (B:332), open question 10 (B:480) (replace).
- **Rationale**: C-016 95% (r2A:109, r2B:126, r2C:88; B and C moved to A on delivery grounds); X-002 95% (B conceded bullet 8, r2B:142; seed: "keep its 7 bullets").
- **Integration point**: Delete bullet 8. Bullet 6 = 427's bullet-6 text from the base file, minus its clause that each added paragraph or table cites its finding id (Change 7), plus one appended clause: the reviser follows `## Fix Budget`, and a blocking finding it cannot fix within budget is listed `escalated` with what it needs, never expanded. Re-review duties stay in `## Fix Budget` (B:281), not in a bullet. Bullets 1-5 and 7 stay byte-identical. M3: exactly seven bullets; bullets 1-5 and 7 equal the original; bullet 6 is one line starting `6. **Reviser contract**` that contains `Reviser brief`, `byte size before and after` and `## Fix Budget`. B:480: "merging bullet 6 and `## Fix Budget`".
- **Size effect**: shrinks (B's bullet 8 is about 130 words; the appended clause about 30).
- **Risk**: Medium — `test_review_severity_rule.py` scans every command file (A:252), so M7 must be re-run on the new bullet.

### Change 7: Finding ids kept out of the spec text (from Variant A)
- **Source**: Variant A, A:55, A:118, A:130, A:238.
- **Target**: Base, B:165, B:269, B:286, B:309, B:327 test 13 (replace).
- **Rationale**: C-017 70% (r2A:110, r2B:127, B conceding); X-003 70% (r2A:126, r2B:143). A:118 and A:130: ids written into the spec are added text the next review citation-checks (25-61 tags per cycle).
- **Integration point**: A finding-id tag written into the spec (`(F10)`, `(N3, N4)`) counts as a new id: forbidden, policy failure. `path:line` tokens stay excluded from word counts (B:165) and count toward bytes (Change 12). Drop "so a fix that cites its evidence as the README demands is not penalised" as it applies to ids. `words()` comment (B:309) drops the tag clause. Test 13: a `path:line` token adds zero words; a `(F3)` tag exits 1 with reason `id`.
- **Size effect**: shrinks.
- **Risk**: Medium — changes a counting rule the replay harness (B:479) must re-check.

### Change 8: The re-review's own read-only checker run is authoritative (from Variant A)
- **Source**: Variant A, section 2.3 (A:64-68).
- **Target**: Base, Step 1 items 2-3 (B:110-111), `## Fix Budget` report paragraph (B:281), `verify` (B:318), test 17 (B:327), cause row 9 (B:230), risk rows 6 and 11 (B:451, B:456), 7.3 second bullet (B:461) (replace).
- **Rationale**: C-018, Round 2, 95% (r2A:111, r2B:128, r2C:90; C moved to A). INV-003 (MEDIUM) asks for the call shape.
- **Integration point**: Before the prior-blocking table the re-review runs `check` without `--enforce`: `--baseline <the saved copy passed as --baseline> --revised <spec> --report <prior report> --ledger <disposition file>`. It prints to stdout and writes no file (INV-022 stays ADDRESSED). Its summary goes in the header as `fixcheck: <exit> ...`. The run counts whether or not the reviser ran the checker. A prior blocking id the run reports over budget is `open (over budget)` (A:67); an id under `## deferred` as escalated is `open (escalated: budget)` with its need (B:111 (a) kept); `attacks:` is computed from this run's hunks instead of a receipt (B:111 (b) kept). Copy only numbers and ids (X-008 kept). Delete `verify` and test 17. INV-003 is answered by this call shape.
- **Size effect**: shrinks (removes `verify` and the receipt-reading path).
- **Risk**: Medium — V7, cause row 9 and risk rows 6 and 11 depended on the receipt; Change 18 restates V7.

### Change 9: No new coordinator duty (from Variant A)
- **Source**: Variant A, A:37 ("The coordinator gets no new duty, so the S1 briefs change only by the command name").
- **Target**: Base, section 2 intro (B:102) (append one sentence); Step 0 heading (B:104) (replace).
- **Rationale**: C-022 80% (r2A:115, r2C:94; B's dissent marked a tie, r2B:132); X-012 80% (r2A:135, r2C:114).
- **Integration point**: Append A:37's sentence to B:102. Step 0 heading "(coordinator or owner)" becomes "(owner, before the experiment)". Every action in the exit table names the reviser or the reviewer (Change 21). B:131's "saved copy the coordinator needs" goes with Change 18; B:473's "letting the coordinator stop" goes with Change 36.
- **Size effect**: grows by one sentence. Justified: it is the rule INV-006 and Change 21 are checked against.
- **Risk**: Low — additive.

### Change 10: Fail line at the seed bar with causal falsifiers (from Variant A)
- **Source**: Variant A, section 6, "What would mean the idea failed" (A:324-330).
- **Target**: Base, 6.4 (B:417-428) and 7.4 (B:465-467) (replace).
- **Rationale**: C-026 70% (r2A:119, r2B:136); X-013 70% (r2A:136, r2B:153, rejecting B's "promising" band as a pass).
- **Integration point**: Replace B's six-row table with A's four falsifiers (minimality not enough; budget turns fix-induced findings into unfixed ones, read from Change 27's carried count; surface not the driver, with A's "cycle-2 sites" read as cycle-2 hunks; only growth improves against Arm B's 3.5) and A's "Not a test of the idea (re-run instead)" line, with A's 16% ceiling replaced by Change 12's bound. Drop the "promising" row and the 100/60 retry row (A: no retune inside this run). Keep B's measurement-cost sentence (B:428). 7.4 becomes one sentence pointing to 6.4.
- **Size effect**: neutral to shrinking.
- **Risk**: Medium — removes B's pre-registered retry setting (U-015, Low value).

### Change 11: One short fit assessment per later adopter (from Variant A)
- **Source**: Variant A, section 4.5 (A:256-261).
- **Target**: Base, 4.6 (B:340-342) (replace).
- **Rationale**: C-028, Round 2, 70% (A and B, B as a tie, r2A:121, r2B:138).
- **Integration point**: Replace the paragraph with A's three one-line assessments (rf-qa Fix Cycle good fit; `/sc:reflect` weak fit, no reviser step; `/sc:implement` needs a code unitiser, out of scope). Keep B's last sentence ("Each adopter runs its own S1-style measurement first; I claim nothing for them"). Drop the `--class-map` and `--unit line` options, which do not exist. Do not take A's promotion paragraph (A:262); B open question 10 covers promotion.
- **Size effect**: neutral; removes two speculative options.
- **Risk**: Low.

### Change 12: Fixed cycle cap of gross words and bytes, overrides included (from Variant C)
- **Source**: Variant C, Step 2 (C:62: 600 gross added words and 6,144 gross added bytes per cycle, including overrides) and section 6 (C:317: 21.3% byte bound).
- **Target**: Base, B:178, B:184, B:204, B:211 (cycle clause; order in Change 23), B:227, B:228, B:277, B:300, B:315, B:327 test 18, 6.2 (B:392-393) (replace).
- **Rationale**: C-005 95% (r2A:98, r2B:115, r2C:77; A and B moved because B's relative cap reverts CRITICAL fixes first). C-025 70% (r2A:118, r2B:135): B's replay growth with C's byte bound stated beside it. INV-013 (MEDIUM).
- **Integration point**: Cycle cap = 600 gross added words and 6,144 gross added bytes, overrides included. Bytes are counted on the raw added text, tags and `path:line` included, so a citation-heavy fix is bounded at cycle level (INV-013). Per-finding caps stay B's word caps; no per-finding byte caps (C's 512/1,024 belong to C's 60-word cap). Delete `CYCLE-GROWTH` and `CYCLE_GROWTH_PCT`; the report header (B:184) shows `cycle_words=<n>/600 cycle_bytes=<n>/6144`. 6.2: keep the 13% replay estimate; replace the 16.1% bound with "two cycles add at most 1,200 gross words (14.7% of 8,148) and 12,288 gross bytes (21.3% of 57,763), so net growth cannot exceed these"; cap the prediction range at the word bound: 13% (8% to 14.7%). Cause rows 6-7 (B:227-228) cite the new bound.
- **Size effect**: neutral (one cap rule replaces two).
- **Risk**: Medium — the 6.2 derivation and the B:228 bound must be recomputed, not edited in place.

### Change 13: Exit-code layout (from Variant C)
- **Source**: Variant C, exit table (C:259-267).
- **Target**: Base, exit-code H3 (B:198-208), B:203, B:279, B:301, B:316, test exit expectations (B:327) (replace).
- **Rationale**: C-012 95% (r2A:105, r2B:122, r2C:84); X-004 95% (r2A:127, r2B:144, r2C:106: the only layout that keeps argparse's exit 2 free).
- **Integration point**: For `hash` and `check`: 0 accept (may carry declared escalations); 1 policy failure (over budget, forbidden element, cycle cap, unattributed hunk, ledger incomplete, mislabelled `op`, edit on a minor id, finding-id tag); 2 argparse usage; 3 bad input (missing or empty file, no `fixbudget` block, malformed or extra override, ledger missing for `--enforce`); 4 hash conflict (`STALE-BASE`); 5 `--enforce` cannot write the spec safely; 70 internal error. B's order "1, 3, 4, 2" (B:208) becomes the order of reasons inside exit 1: attribution before size. `EXIT` constant and M4 follow. Tests: 2-9 expect exit 1 with their reason; second override exit 3; test 15 exit 3; the stale-baseline test exit 4. The action column is Change 21.
- **Size effect**: neutral (seven rows, but B's three policy codes collapse into one).
- **Risk**: Medium — every test expectation and the brief's exit references change.

### Change 14: Detect a hard-gate or CRITICAL finding graded minor (from Variant C)
- **Source**: Variant C, Step 2 (C:53); the hard-gate check adopted as the C-001 amendment (r2A:44, r2B:57, r2B:125).
- **Target**: Base, block rules (B:128), `parse_fixbudget` (B:305), risk 8 detection (B:453) (insert).
- **Rationale**: C-015, Round 2, 95% (r2A:108, r2B:125, r2C:87; A and B moved to C). The response to the detection is changed by Change 20 (INV-005).
- **Integration point**: The block's `severity` column may read `MAJOR/FR-8` or `MAJOR/FR-9`, so the checker can see a hard gate. The checker flags any line whose severity is `CRITICAL`, `MAJOR/FR-8` or `MAJOR/FR-9` with grade `minor`.
- **Size effect**: grows by one value form in an existing column. Justified: C-015 (95%) and INV-005 (HIGH) both need the checker to see a hard gate.
- **Risk**: Low — additive.

### Change 15: Fail closed on a missing or stale input (from Variant C)
- **Source**: Variant C, Step 6 (C:126: "If any physical input is missing, malformed or stale, stop with an input error, never fall back to a first review").
- **Target**: Base, Step 1 item 2 (B:110, "STALE ... and MISSING do not stop the review"), risk 6 detection (B:451) (replace). B:106 `E-FIXCHECK-MISSING` kept.
- **Rationale**: C-019 95% (r2A:112, r2B:129, r2C:91; A and B moved to C; same rule as 427 bullet 1); X-007 95% (r2A:130, r2B:147, r2C:109).
- **Integration point**: If the saved copy, the prior report's block or the disposition file's ledger is missing or malformed, or the re-review's `check` exits 3, 4, 5 or 70, the re-review stops with the named input error and never falls back to a first review. Its terminal state is Change 22.
- **Size effect**: neutral.
- **Risk**: Medium — without Change 18 this stop fires on every loop whose reviser obeys T08 (INV-001).

### Change 16: Fresh-worker valid/invalid probe as proof of delivery (from Variant C)
- **Source**: Variant C, section 5 (C:289).
- **Target**: Base, section 5, pre-flight sentence in B:360 (replace).
- **Rationale**: C-020, Round 2, 95% (r2A:113, r2B:130, r2C:92; B moved to C).
- **Integration point**: Replace "Pre-flight before dispatch ... `hash --file README.md` must print a 64-hex hash and exit 0" with: before a measured loop, a fresh worker loads `/sc:spec-panel-minfix` and runs the installed checker on a tiny valid and a tiny invalid fixture (exit 0 and exit 1); reading the command file is not proof of invocation. Keep the `E-FIXCHECK-MISSING` sentence.
- **Size effect**: neutral.
- **Risk**: Low.

### Change 17: Spelled-out class labels where a person reads them (forced L1, from Variants A and C)
- **Source**: Forced L1 round, L1-A2 and L1-C3 (`CRITICAL`, `blocking MAJOR`, `minor`, `override`).
- **Target**: Base, budget table class column (B:172-176), `## Fix Budget` table (B:271-275), checker report `cls` column (B:185-188), "class M" (B:128), "class `m`" (B:223) (replace).
- **Rationale**: Forced L1 round, 2 of 3 (A and C; B preferred terse labels).
- **Integration point**: Replace `C`, `M`, `m` with `CRITICAL`, `blocking MAJOR`, `minor`, and the override value with `override`, in text and tables a person reads. Script keys (B:295-299) may stay terse; M4 maps them. Do not rename the chain classes A-E of section 1.4.
- **Size effect**: neutral.
- **Risk**: Low.

### Change 18: INV-001 — the reviser writes no `.fixcheck/` file (invariant probe)
- **Source**: `invariant-probe.md` suggested resolution (IP:50); B's own statement that "a coordinator copy with the same hash is equivalent" (B:131).
- **Target**: Base, B:111 (receipt references), B:131, B:160, B:196, B:211 ("writes the receipt"), B:285, B:288, B:303 (`snapshot`), B:319 (`receipt_json`), test 16, 7.1 cost rows (B:436, B:440), risk 7 (B:452), risk 11 (B:456), V7 (B:381), B:382-383 (metric sources) (replace).
- **Rationale**: INV-001 HIGH (IP:8): T08 lets the reviser write only the spec and the disposition file, the real S1 reviser refused to write a baseline copy (D2:61), and fail-closed (Change 15) then stops the re-review.
- **Integration point**: The baseline is the saved copy 427 already keeps for the next `--baseline` (SP:261); the Reviser brief names its path. `check` compares that file's sha256 with `reviewed_sha256` (exit 4 on mismatch; C-009 kept). No `.fixcheck/` folder and no receipt: `check` prints to stdout, and the reviser pastes the last `FIXCHECK` line into the disposition file, which B:161 already requires. Delete `snapshot`, the receipt-key paragraph (B:196) and `receipt_json`. Test 16 becomes "`check` refuses a baseline whose hash differs (exit 4)". V7: the disposition ends with a `FIXCHECK exit=0` line (or the ids `--enforce` reverted) and the re-review's own run does not exit 3, 4, 5 or 70. 7.1: reviser calls drop `snapshot`; reviewer calls are `hash` or `check`, one each; "new files: none". Metric sources (B:382-383): the re-review's run and the history copies. Not taken: the probe's "receipt data inside the disposition file" beyond the pasted line, because Change 8 makes the re-review's own run the authoritative record.
- **Size effect**: shrinks (removes a subcommand, a folder, a JSON schema and a test).
- **Risk**: Medium — residual: if the reviewer cannot know the saved-copy path when it writes the brief, the brief cannot name it; the one-replicate pilot (B:451) must check this. The advocates disagreed on whether a pilot settles INV-001 (r2B:91 against r2C:44,56).

### Change 19: INV-002 — carried prior blocking findings get a budget (invariant probe)
- **Source**: IP:51.
- **Target**: Base, block description (B:114) and `## Fix Budget` block description (B:281) (replace one clause); completeness rule (B:159) unchanged.
- **Rationale**: INV-002 HIGH (IP:9): an id not in the block gets budget 0, so a carried F-id (F7, escalated for budget, B:155) cannot be fixed in cycle 2 and counts at review 3.
- **Integration point**: "one line per finding of this review, plus one line per prior blocking id still open, with its prior severity and grade". The completeness rule (B:159) then covers carried ids with no new text.
- **Size effect**: grows by one clause. Justified: HIGH, and the smallest text that closes the gap.
- **Risk**: Low — additive.

### Change 20: INV-005 — a hard gate graded minor warns instead of stopping (invariant probe, smaller form)
- **Source**: IP:52, reduced.
- **Target**: Base, B:128 (FR-8/FR-9 sentence), checker report (B:180-194), escalation text in Step 5 (B:214), open question 11 (B:481) (replace and append).
- **Rationale**: INV-005 HIGH (IP:12): the real S1 review 1 grades F22 and F16 "MAJOR (FR-8 GAP minimum), non-blocking" (R1:63, R1:121), so an input-error rule stops cycle 1 and no actor can repair the report.
- **Integration point**: A line flagged by Change 14 is not an input error. The checker prints `GRADE-CONFLICT <id>`, keeps the budget the grade gives (zero for `minor`), and the exit code is unaffected. The review-3 escalation lists each grade conflict. Open question 11 stays an owner question. **Deviation from the probe**: the probe reclassifies the finding as class M. Not taken: F22, the only review-3 blocking chain of flg-r2, is exactly such a finding, and its 66-word fix produced N5 and then N12 (B:44-50, B:233; S-003 and C-029, 95%). An 80-word budget would reopen the chain that Change 3 closes, and the grade stays with the reviewer (AP-01).
- **Size effect**: grows by one sentence; smaller than the probe's reclassification path.
- **Risk**: Low — hard-gate findings graded minor stay unfixed, as B:481 already states.

### Change 21: INV-006 — one exit-code table for every actor (invariant probe)
- **Source**: IP:53; meanings from C:259-267 (Change 13); the "who acts" column shape of A:105-110.
- **Target**: Base, exit-table action column (B:200-206), Step 2 item 5 (B:160, "On 2, 3 or 4"), brief step 4 (B:288), `--enforce` triggers (B:211, "exit 2 or 4 reasons") (replace).
- **Rationale**: INV-006 HIGH (IP:13): under C's codes, B's reviser steps would treat an argparse error or a hash conflict as a reason to cut down or revert, and C's table gives the actions to the coordinator, which C-022 rejects.
- **Integration point**: One column "reviser / reviewer action". 0: reviser stops; reviewer records it. 1: reviser cuts the named entries once and re-runs, then `check --enforce`; reviewer marks the named findings `open (over budget)`. 2: correct the call once; nothing is counted. 3, 4, 5, 70: reviser edits nothing further and pastes the output; reviewer stops (Change 15) and escalates (Change 22). `--enforce` reverts every finding with an exit-1 reason and every unattributed hunk. No row names the coordinator.
- **Size effect**: neutral.
- **Risk**: Medium — touches the brief's literal steps.

### Change 22: INV-007 — every early stop is a justified escalation (invariant probe)
- **Source**: IP:54.
- **Target**: Base, Step 5 (B:213-214); after Change 1, Step 3 re-review (append one sentence).
- **Rationale**: INV-007 HIGH (IP:14): a stop at review 1 or 2 is neither a PASS nor a justified escalation, and no rule turns it into one.
- **Integration point**: "If the re-review stops on an input (Change 15), or the disposition's last `FIXCHECK` line shows exit 3, 4, 5 or 70, the run ends as an escalation to the user that lists the open blocking findings and the named input error." The reviewer is the actor, so no coordinator duty is added.
- **Size effect**: grows by one sentence. Justified: HIGH; it is the only terminal state otherwise missing.
- **Risk**: Low — additive.

### Change 23: INV-012 — deterministic revert order for the cycle cap (invariant probe, order adjusted)
- **Source**: IP:55, adjusted.
- **Target**: Base, `--enforce` cycle clause (B:211, "the findings with the highest gross are reverted first"), test 18 (B:327) (replace).
- **Rationale**: INV-012 HIGH (IP:19): 13 blocking ids can reach 1,120 words against the 600-word cap, and B's order was conceded wrong (r2B:35) because it reverts CRITICAL fixes first.
- **Integration point**: When the cycle cap is exceeded, `--enforce` reverts whole findings until the cycle is within 600 words and 6,144 bytes: blocking MAJOR before CRITICAL; within a class, largest gross first, then by finding id. Each reverted finding is listed `escalated` with its gross as the need. Test 18 checks this order. **Deviation from the probe**: the probe says smallest gross first. Not taken: reverting the smallest fixes first reverts more findings for the same words, and each reverted finding is a carried open blocker at review 3 (INV-028; A's falsifier 2). Only B's class order was conceded, not its within-class order.
- **Size effect**: neutral (one clause replaces one).
- **Risk**: Medium — changes which fixes survive.

### Change 24: INV-023 — gap fills get condition words for the guard rows they name (invariant probe)
- **Source**: IP:56.
- **Target**: Base, B:128 (budget values), budget tables (B:172-178, B:271-277), `classify` (B:306) (insert).
- **Rationale**: INV-023 HIGH (IP:30): an FR-8/FR-9 gap fill must specify the guard-table rows, but the blocking MAJOR class allows one condition word, so a two-branch fill breaches and escalates.
- **Integration point**: For a blocking `MAJOR/FR-8` or `MAJOR/FR-9` gap fill (Change 14), the reviewer writes `gap:<n>` in the budget column, n = the guard rows the finding names. That finding's condition-word limit is n instead of 1 (Change 26); every other limit is its class limit. `gap:<n>` and `override` are exclusive.
- **Size effect**: grows by one budget value and one sentence. Justified: HIGH; smaller than a new class.
- **Risk**: Low — additive.

### Change 25: INV-026 — convergence prediction stated as conditional (invariant probe; claim, no mechanism)
- **Source**: IP:57; the restated forecast band agreed in C-024 (A about 4.1, B 1.1-5.6); B's own B:87 and B:218.
- **Target**: Base, 6.3 (B:395-415) (replace); 6.1 chain-data metric (B:384) (append one measured column).
- **Rationale**: INV-026 HIGH (IP:33): F1 and F12 were within budget and still had blocking children; B's own data show size does not separate the groups (B:87). C-024 (95%) kept B's derived forecast with a wider band.
- **Integration point**: Band becomes 1.1 to 5.6, with A's estimate (about 4.1) beside it. Restate B:409: "If the two assumed rows hold (removal 0.49; replacement 25% to 75%), the mean is about 3.0. The budget alone is not claimed to reach 3 or fewer (section 1.5)." Delete the three probability figures, which came from the narrower 2.1-4.0 band. Pre-register in 6.1, reported before the bar: within-budget parents with blocking children, from `attacks:`, as the count and share of within-budget ledger entries whose finding has a blocking `origin=changed` child. No new mechanism.
- **Size effect**: neutral (the column line replaces the probability sentence).
- **Risk**: Low.

### Change 26: INV-027 — condition-word counter with guard words (invariant probe; C-006 amendment from Variant A)
- **Source**: A:80 (condition words `if unless when whenever except otherwise`); IP:58 adds `where`.
- **Target**: Base, Step 3 item 4 (B:167), budget tables (B:172-176, B:271-275: one column), brief step 2 (B:286), `BUDGETS` (B:296-298), `element_counts` (B:313), test 5 (B:327) (insert).
- **Rationale**: INV-027 HIGH (IP:34): 5 of 6 trt-r1 review-3 blockers are guard GAPs from short revisions, and R3-3 comes from "none where the location is fixed". C-006 (95%) adopted A's counter as an amendment (r2B:116).
- **Integration point**: Per finding, `new_cond` = net new `if`, `unless`, `when`, `whenever`, `where`, `except`, `otherwise` (`only when` is caught by `when`; `only` stays in the universal list). Limits: CRITICAL 2, blocking MAJOR 1, minor 0, `gap:<n>` n. Each counted word is a new guard charged to its finding.
- **Size effect**: grows by one column and one word list. Justified: HIGH, and adopted by all three advocates.
- **Risk**: Medium — `when` and `where` are common in prose, so false positives are likely; add them to risk row 5 (B:450) and measure them in the replay harness (B:479).

### Change 27: INV-028 — cut-down success rate and carried/new split, pre-registered (invariant probe; claim, no mechanism)
- **Source**: IP:59; A's metric M9 (A:305); B open question 9 (B:479).
- **Target**: Base, 6.1 per-cycle metrics (B:383), escalation prediction (B:412), open question 9 (B:479) (append and replace).
- **Rationale**: INV-028 HIGH (IP:35): 11 of 17 flg-r2 MAJOR fixes exceed the cap (B:94, B:98), no variant measured a cut-down success rate (r2C:46), and 4 or more carried blockers fail the review-3 bar with no new findings.
- **Integration point**: (a) The replay harness reports, per recorded loop, the blocking fixes over cap at the first check, which is the cut-down denominator. (b) The pilot and each replicate report the cut-down success rate: findings over budget at the first `check` that pass at the second. (c) The review-3 count is reported as carried (open from review 2: unfixed, escalated or reverted) and new (on cycle-2 hunks) before the bar is applied (A's M9). B:412's "1 to 3 escalated" becomes conditional on the unmeasured rate. **Deviation from the probe**: the probe puts the rate in the replay harness; recorded loops contain no cut-down attempts, so the harness can give only the denominator.
- **Size effect**: grows by three metric lines. Justified: HIGH; measurement only.
- **Risk**: Low — additive.

### Change 28: B defect 1 — the installed variant cites no `src/superclaude/` path (from Variant C)
- **Source**: Variant C, C:160.
- **Target**: Base, 4.1 file-table row (B:241), command regions (4.2 after Change 2), M2 (B:331), B:250 (replace); M5 (B:334) unchanged.
- **Rationale**: Base-selection Completeness 1 NOT MET (re-evaluation 2): the copy carries `src/superclaude/examples/release-spec-template.md` (`spec-panel.md:220`; plugins copy at line 218), which breaks the constraint "Installed primitives never cite `src/superclaude/` paths", and B's M2 pin forbids the fix while M5 forbids the path. Only C met this criterion.
- **Integration point**: In the variant only, replace that lookup with C's wording: "use a caller-supplied release template; if none is supplied, use the inline output schema". Apply it to the repository file and the experiment file, because both are installed. M2 excludes that line from its line-for-line comparison, M5 then passes, and B:250's claim becomes true. Record in the install watcher that the experiment file differs from Arm B's text on this one line too (UNVERIFIED whether S1 exercises it).
- **Size effect**: neutral.
- **Risk**: Low.

### Change 29: B defect 2 — the repository file drops `## Unattended mode` (from Variant A)
- **Source**: Variant A, A:161-162.
- **Target**: Base, 4.1 file-table row (B:241, "a 12-line `## Unattended mode` section"), test list (B:248), M2 (B:331), M7 (B:336), base-text paragraph (B:362) (replace and append).
- **Rationale**: Base-selection Correctness 2 NOT MET (re-evaluation 3): `tests/skills/test_worker_contract.py:831-839` asserts the exact set of commands with `^## Unattended mode`. All three advocates agreed to drop it (r2A:49, r2B:39 and 133, r2C:26; INV-025); B's own advocate voted against B on C-023 for this reason.
- **Integration point**: The repository file removes the section and drops `[--unattended] [--report-dir <dir>]` from Usage line 2 (A:161). M2 excludes both. Add `tests/skills/test_worker_contract.py` to M7's keep-green list. B:362: the two variant files differ only where the two bases differ, except the removed section. The experiment file (472-line base) has no such section and is unchanged.
- **Size effect**: shrinks.
- **Risk**: Low.

### Change 30: B defect 3 — one minor budget everywhere
- **Source**: Change 3 (Variant A, C-004).
- **Target**: Base, every site that states a minor allowance: B:133, B:176, B:223, B:233, B:259 (removed with bullet 8 by Change 6), B:275, B:277, B:284, B:298, B:300, B:327 test 4, B:383, B:454, B:471, B:476 (replace).
- **Rationale**: Base-selection Correctness 4 NOT MET: "12 words, net 0" (B:133, B:223, B:233) against "fixcheck budget 0" and "minor budget 0" (B:133, B:226).
- **Integration point**: Apply Change 3 at every listed site. Check after the merge: no text gives the minor budget as 12 or a minor cycle total of 36, and `deferred (minor, fixcheck budget 0)` (B:133, M6 at B:335) is now literally true. The other Correctness 4 contradiction (M2 against M5) goes with Change 28.
- **Size effect**: shrinks.
- **Risk**: Low.

### Change 31: One owning finding per edit (C-008 amendment)
- **Source**: Single-owner rule adopted by all three advocates (r2A:27, r2B:44, C:62; INV-017 ADDRESSED).
- **Target**: Base, ledger rules (B:159, "`finding` may list two ids (the words are split equally)") (replace).
- **Rationale**: C-008 70% (B's lookahead splitter, amended to one owner per hunk); A-001 70% (splitter gated by the replay harness, already B:479).
- **Integration point**: "`finding` names one id; an edit that also answers another finding is charged to its owner only." No new field.
- **Size effect**: shrinks.
- **Risk**: Low.

### Change 32: Coupled revert (X-005 and A-002 amendment; INV-021)
- **Source**: The `depends:` cascade agreed in Round 2 (r2B:156); base-selection strength to preserve 9.
- **Target**: Base, ledger rules (B:159), `--enforce` (B:211), test 14 (B:327), risk 2 residual (B:447) (insert).
- **Rationale**: X-005 70% and A-002 70%: whole-finding revert "with a coupled revert added". INV-021 (MEDIUM): N3 came from an F2+F11 interaction (B:48).
- **Integration point**: A ledger entry may carry `depends: L<n>`. When `--enforce` reverts a finding, it also reverts every entry that depends on one of that finding's entries. Test 14 adds one dependent entry. Risk 2 residual: undeclared dependencies remain (r2C:21, r2C:32).
- **Size effect**: grows by one optional field and one clause. Justified: the agreed amendment on two points B won.
- **Risk**: Low — additive and optional.

### Change 33: INV-009 — brief ids cross-checked against the block
- **Source**: IP:16.
- **Target**: Base, risk 8 detection (B:453) and the matching validation in Step 3 (insert one clause).
- **Rationale**: INV-009 (MEDIUM): an id in the brief (SP:263) but missing from the block silently gets budget 0, and its fix is then reverted with no input error.
- **Integration point**: Extend the existing check ("every id of the block appears in the report body") in the other direction: every id in the Reviser brief's id list must be a blocking id of the block, else exit 3.
- **Size effect**: grows by one clause, on a validation B already has.
- **Risk**: Low.

### Change 34: INV-015 — rename counts as one entry (from Variant A)
- **Source**: Variant A, A:80 ("an identical single-token substitution repeated across sites for one finding (a rename) counts as one site").
- **Target**: Base, Step 3 item 4 (B:167) (insert one sentence).
- **Rationale**: INV-015 (MEDIUM); base-selection strength to incorporate A12 (the rename rule was lost when C-006 went to B).
- **Integration point**: "An identical single-token substitution repeated across units for one finding counts as one entry." The table-column case (F2's "Contract path" column) is recorded as open in Change 36.
- **Size effect**: grows by one sentence.
- **Risk**: Low.

### Change 35: Define experiment terms on first use (shared rubric gap)
- **Source**: Glosses in the variants: D5 = metrics M1-M5 (A:298); D9 = parallel arms need different command names (B:346); D10/D11 = the earlier A/B experiment designs whose bar and validity checks V1-V6 this arm reuses (B:374, B:378); FR-8/FR-9 = spec-panel's hard gates for guard-table rows and blank behaviour (IP:20, IP:30).
- **Target**: Base, after B:3 (insert one line).
- **Rationale**: Base-selection Clarity 4 NOT MET in all three variants (B:9 uses D10/D11/D12; B:378 uses V1-V6 without definitions).
- **Integration point**: One line glossing D5, D9, D10, D11, V1-V6, FR-8 and FR-9 as above. D12 has no gloss in any variant: name its source record and mark it UNVERIFIED rather than invent one.
- **Size effect**: grows by one line. Justified: a rubric criterion no variant met; a reader cannot apply the bar without it.
- **Risk**: Low.

### Change 36: MEDIUM invariants recorded as open questions
- **Source**: `invariant-probe.md` INV-014, 015, 016, 019, 020, 021, 029, 030, 031.
- **Target**: Base, section 8 (B:469-481) and existing residual cells (append only where no line exists).
- **Rationale**: The 13 MEDIUM items do not block selection (base-selection, "Required Changes"); the decisions are in the Overview table.
- **Integration point**: Add to an existing line where one fits; add a new line only where none does:
  - INV-014 (moved text charged 0): new one-line question in section 8.
  - INV-015 (table-column fix needs more than 4 entries): append to open question 4 (B:474).
  - INV-016 (mis-attribution ceiling): append to open question 9 (B:479): set the ceiling from the harness output.
  - INV-019 (all-reverted cycle still spends a review): append to open question 3 (B:473), and change "letting the coordinator stop" to "letting the run escalate" (Change 9).
  - INV-020 (free deletions may remove required behaviour): append to risk row 3 residual (B:448).
  - INV-021 (undeclared dependencies): carried by Change 32 in risk row 2.
  - INV-029 (should the bar count blocking grade instead of severity): append to open question 11 (B:481).
  - INV-030 and INV-031: already stated (B:453 residual; B:231 cause row 10); no new text.
- **Size effect**: grows by about one new line plus short appends to existing lines.
- **Risk**: Low — additive.

## Changes NOT Being Made (with rationale)

Diff points B won (all 28), then other alternatives considered and rejected.

| Diff Point | Non-Base Approach | Rationale for Keeping Base |
|------------|-------------------|---------------------------|
| S-003 | A: prose, one table, chain bullets; C: one evidence table | B's six evidence tables, replicated by A and B; 95% (r2A:89, r2B:106, r2C:68). |
| S-006 | A and C: measurement section without derivation tables | B's derivation tables let a reader recompute the forecast; 95% (r2A:92, r2B:109, r2C:71). |
| S-007 | A: numbered failure modes; C: two-column table | B's detection, mitigation and residual columns per risk; 95% (r2A:93, r2B:110, r2C:72). |
| C-001 | A: `fix-budget:` line for blocking ids only; C: `minfix-v1` JSON block | B's all-findings block with a derived class; 95% (r2A:94, r2B:111, r2C:73). Amended only by Changes 14, 19, 24. |
| C-002 | A: 40 added / 30 net; C: 60 words / 512 bytes | B's 80/50 fits the measured blocking fixes; A withdrew its 40-word cap; 95% (r2A:95, r2B:112, r2C:74). |
| C-003 | A: 80/60; C: 120 words / 1,024 bytes | B's 120 gross with net and add-only caps; 90% (r2A:96, r2C:75; B tie r2B:113). |
| C-006 | A: sites, sentences, condition words; C: bytes, removed words | B's universal and exec-recipe gates; 95% (r2A:99, r2B:116, r2C:78). Only the agreed amendments are added (Changes 12, 26). |
| C-007 | A: separate JSONL ledger; C: `cycle-1/ledger.json` | Ledger inside the disposition file fits T08's single write target; 95% (r2A:100, r2B:117, r2C:79). |
| C-008 | C: byte-offset reconstruction inside reviewer quotes, no splitter | B's lookahead splitter, amended to one owner (Change 31); 70% (r2A:101, r2B:118). |
| C-009 | A: unhashed `cp -p` copy by the reviewer; C: coordinator `freeze` with state pins | Reviewer hash plus `STALE-BASE` with no coordinator duty; 95% (r2A:102, r2B:119, r2C:81). |
| C-010 | A: folder `fix-budget` (install sweep concern); C: `sc-spec-panel-minfix-protocol` | `sc-fixcheck`: 70% (r2A:103, r2B:120) and unanimous in the forced L1 round; the sweep looks for `commands/fixcheck.md`, which does not exist (B:242). |
| C-013 | A: reviser restores `revert_to` by hand; C: admit nothing, never rewrite | Script-side revert of whole findings guarantees termination without model compliance; 70% (r2A:106, r2B:123). Kept as `check --enforce` (Change 4). |
| C-021 | A: `sed` on every brief; C: prose instruction | B's `@`-anchored substitution hits exactly the review briefs; 95% (r2A:114, r2B:131, r2C:93). |
| C-023 | A and C: current master text for the variant | 472-line 427 text for the experiment file; 80% (r2A:116, r2C:95). The repository file still drops `## Unattended mode` (Change 29). |
| C-024 | A: 2.5; C: 1/1 with no derivation | B's derived forecast, widened to 1.1-5.6 and made conditional (Change 25); 95% (r2A:117, r2B:134, r2C:96; C withdrew 1/1). |
| C-025 | A: 7% (4-12%); C: 12%/18% | B's replay-derived 13% with C's byte bound beside it (Change 12); 70% (r2A:118, r2B:135). |
| C-027 | A and C: coarser cost estimates | B's itemised cost table; 95% (r2A:120, r2B:137, r2C:99). Rows edited only by Change 18. |
| C-029 | A: sentence-level medians; C: no per-finding measurement | B's chain taxonomy and cap replay, replicated twice; 95% (r2A:122, r2B:139, r2C:101). |
| C-030 | A: derivation-pin test; C: seven files with `plugins/` mirrors and a design doc | B's behaviour tests plus the `enforce` property test; 90% (r2A:123, r2C:102; B tie r2B:140). No plugin mirror unless a parity test requires one. |
| X-005 | A: reviser reverts; C: nobody rewrites the candidate | Script reverts whole findings with a coupled revert (Change 32); 70% (r2A:128, r2B:145). |
| X-008 | A: reads the checker report; C: reads the ledger | Numbers and ids only, never reviser prose; 95% (r2A:131, r2B:148, r2C:110). |
| X-009 | C: removal cap of 120/240 words | Free in-scope deletions, measured; 70% (r2B:149, r2C:111). INV-020 recorded (Change 36). |
| X-010 | A: median 38 words, 62-79% under 40 | B's whole-fix measurement (mean 108, min 58); A withdrew its calibration; 95% (r2A:133, r2B:150, r2C:112). |
| X-011 | A: sites drive next-round findings | Fix size alone does not separate parents with blocking children; 95% (r2A:134, r2B:151, r2C:113). This is why Change 25 makes the claim conditional. |
| X-014 | A and C: current master for the experiment file | Exact 472-line 427 text, so only one thing changes; 95% (r2A:137, r2B:154, r2C:116). |
| A-001 | C: exact quotes instead of a splitter | Splitter gated by the replay harness; 70% (r2A:138, r2B:155). |
| A-002 | C: reject partial admission outright | Whole-finding revert with a coupled revert; 70% (r2A:139, r2B:156). |
| A-004 | C: bounded retries without partial salvage | One-retry success rejected as a prediction; `--enforce` kept as the termination mechanism; 70% (r2A:141, r2B:158). The rate is measured instead (Change 27). |
| Forced L1 (L1-C4) | C: section named `## Minimal fix gate` | `## Fix Budget`, B and C (2 of 3). |
| Forced L1 (S-002) | C: lighter subdivision of section 2 | Numbered H3 per mechanism step, A and B (2 of 3); kept in Change 1. |
| L1-A3 (single advocate) | Keep 427's bullet-6 wording word for word and append | Not voted. Change 6 keeps 427's wording except the finding-id clause, which C-017 (70%) removes. |
| L1-A4 (single advocate) | Budget numbers only in the checker constants; the command points to preflight output | Not voted. B's table plus the M4 sync test keep prose and script equal, and the Reviser brief needs the numbers (B:286). |
| L1-B4 (single advocate) | One `fix*` artifact name family | Not voted; already true after the merge (`fixbudget`, `fixledger`, `fixcheck`; `.fixcheck/` is removed by Change 18). No change. |
| L1-C2 (single advocate) | Ledger field named `finding_id` | Not voted; renaming B's `finding:` adds churn and fixes no point. |
| INV-005 probe form | Reclassify a minor-graded hard gate as class M | Reopens the F22 to N5 to N12 chain (B:44-50, B:233); Change 20 warns instead, which is smaller. |
| INV-012 probe form | Within a class, revert the smallest gross first | Reverts more findings and so creates more carried blockers (INV-028); Change 23 keeps B's within-class order. |
| INV-028 probe form | Measure the cut-down success rate in the replay harness | Recorded loops contain no cut-down attempts; the harness gives the denominator and live runs give the rate (Change 27). |
| Risk 1 (shared rubric gap) | Add a probability column to the risk table | No measured probabilities exist; invented values would add unsupported text against the theme. The residual column stays the honest field. |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|----------|------|------------------|----------|
| 1 | High | Steps out of actor order or stale step references; readers route actions to the wrong actor | Revert to base section 2 (B:100-214) and reapply the content changes in place |
| 2 | High | Broken section-4 references from sections 2, 5 and 8 | Revert to base section 4 headings (B:235-342) |
| 3 | Medium | A missed site restates a 12-word budget (defect 3 returns) | Revert listed sites; Change 30 re-sweeps |
| 4 | Medium | Brief, tests and outline name removed subcommands | Restore B's `enforce` subcommand (B:210-211) |
| 5 | Medium | Override rules from both paths coexist | Revert B:128, B:178, B:277 |
| 6 | Medium | Eight bullets remain, or pinned literals of bullet 6 are lost; severity-rule test may fail | Revert 4.2 (B:252-260) and M3 |
| 7 | Medium | Citations counted as ids, false breaches | Revert B:165 word rule |
| 8 | Medium | Re-review has no authoritative record; V7 undefined | Restore `verify` (B:110-111, B:318) |
| 9 | Low | None beyond one sentence | Remove the sentence |
| 10 | Medium | Fail lines refer to metrics that do not exist yet | Revert to base 6.4 table (B:417-428) |
| 11 | Low | None material | Restore base 4.6 paragraph |
| 12 | Medium | Wrong growth bound or prediction range above the cap | Revert 6.2 (B:387-393) and B:178 |
| 13 | Medium | Test expectations and exit references disagree | Revert exit H3 (B:198-208) |
| 14 | Low | Severity value not parsed | Remove the `MAJOR/FR-x` value form |
| 15 | Medium | Every obedient loop stops at review 2 if Change 18 is missing | Revert B:110 text; land with Change 18 only |
| 16 | Low | Probe step missing | Restore B:360 pre-flight sentence |
| 17 | Low | Mixed terse and spelled labels | Revert label edits |
| 18 | Medium | Reviser cannot find the saved-copy path; pilot needed | Restore `snapshot` and receipt (B:131, B:196) |
| 19 | Low | Carried ids still budget 0 | Remove the clause |
| 20 | Low | Hard-gate grade conflicts invisible | Remove the warning sentence |
| 21 | Medium | Actors act on wrong codes | Revert action column |
| 22 | Low | Early stops unclassified | Remove the sentence |
| 23 | Medium | Non-deterministic or wrong survivors under the cycle cap | Revert B:211 clause and test 18 |
| 24 | Low | Gap fills breach and escalate | Remove `gap:<n>` |
| 25 | Low | None material | Restore base 6.3 text |
| 26 | Medium | False positives on `when`/`where`, more reverts | Remove the column; keep the replay measurement |
| 27 | Low | None material | Remove the metric lines |
| 28 | Low | M2 still pins the source-path line | Revert row and M2 |
| 29 | Low | `test_worker_contract.py` fails | Revert row and M2/M7 |
| 30 | Low | Residual 12-word text | Re-sweep |
| 31 | Low | Shared edits ambiguous | Restore B:159 split rule |
| 32 | Low | Dependent fixes left half-reverted | Remove `depends:` |
| 33 | Low | Brief/block mismatch unnoticed | Remove the clause |
| 34 | Low | Renames over-counted | Remove the sentence |
| 35 | Low | Terms still undefined | Remove the line |
| 36 | Low | MEDIUM items unrecorded | Remove the appends |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-08T15:59:13Z
- Note: the base was force-selected under `no_convergence` (BLOCKED_BY_INVARIANTS). This plan carries all 10 HIGH UNADDRESSED invariants as Changes 18-27. The merged result still needs user review before it counts as converged.
- Analytical review (`refactor-plan-review.md`, 2026-11-08): verdict FAIL, 7 blocking issues (PR-B1 to PR-B7). The plan text above was not edited; the merge executor applied each PR-B correction in place of the affected change (14 changes applied in corrected form, see `merge-log.md`). Residual from PR-B2: the `snapshot` fallback stays unproven until a one-replicate pilot shows that the reviser runs it, or that a saved-copy path can be named in the Reviser brief.
