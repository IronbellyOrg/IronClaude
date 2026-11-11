# Merge Execution Log

## Metadata
- Base: Variant B (sonnet:analyzer), `variant-2-sonnet-analyzer.md`
- Executor: merge-executor agent
- Plan: `refactor-plan.md` (36 changes), corrected by `refactor-plan-review.md` (PR-B1..PR-B7 binding; minor notes PR-M1..PR-M10 applied where one-line)
- Output: `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/brainstorms/346-minfix/nested/adversarial-1/merged-output.md` (528 lines, 8 H2 sections kept, 22 `<!-- Source: -->` tags)
- Changes applied: 36 of 36 (22 as planned, 14 as corrected by a PR-B item) plus 1 review-mandated insertion (PR-B7); 0 skipped
- Status: success
- Timestamp: 2026-11-08T16:25:36Z
- Method: base copied with `cp`; edits made with Edit in place. Changes 3-36 were placed into B's text; Change 2 and Change 1 were then realised by the same section-level edits (old Step 1 items 2-3 and old Step 5 moved into a new Step 3; old Step 4 folded into Step 2; section 4 regrouped). Citation key as in the plan: `B:n` = unmodified base line.

## Changes Applied

### Change 1: Mechanism steps grouped by actor and phase
- **Status**: applied
- **Source**: Variant A, Section 2.1-2.3 (A:35-119)
- **Target**: Base, section 2 (B:100-214)
- **Before**: Step 0, Step 1 (review, with re-review items 2-3), block, Step 2 reviser, Step 3 checker computes, budget, report, exits, Step 4 `enforce`, Step 5 next review.
- **After**: Step 0 (owner); Step 1 Review N, reviewer (items 1-2 + block); Step 2 Reviser (items 1-7, `check --enforce` as item 6); Step 3 Review N+1, re-review (old items 2-3 and old Step 5, rewritten); then reference H3s without step numbers: What the checker computes, Budget table, Checker report, Exit codes. "Back to step 1" became "Then step 1 item 2 with `review: N+1 of 3`"; Step 2 item 5 points to "step 3"; reference to the brief now "section 4.2".
- **Provenance tag**: `<!-- Source: Base (original, modified) — ... steps regrouped by actor per Change #1 (Variant A, Section 2.1-2.3) -->` and per-H3 tags
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 2: Exact-changes section as file table plus one H3 per artifact
- **Status**: applied
- **Source**: Variant A, Section 4 (A:138-262)
- **Target**: Base, section 4 (B:235-342)
- **Before**: 4.1 file list, 4.2 bullet 8, 4.3 `## Fix Budget`, 4.4 script, 4.5 tests, 4.6 adopters.
- **After**: 4.1 file list; 4.2 `spec-panel-minfix.md` (six regions incl. the `## Fix Budget` literal); 4.3 script outline; 4.4 `sc-fixcheck/SKILL.md` (body moved from the B:242 row, row now says "section 4.4"); 4.5 tests; 4.6 adopters. "section 4.5" in B:244-245 still resolves (tests stayed 4.5).
- **Provenance tag**: `<!-- Source: Base (original, modified) — section regrouped as file table plus one H3 per artifact per Change #2 (Variant A, Section 4) ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 3: Zero edits for non-blocking findings; proxy and blocking counts reported separately
- **Status**: applied (with PR-M4)
- **Source**: Variant A, Section 2.1 item 3 and 2.4 (A:50, A:75)
- **Target**: B:98 (PR-M4), B:133, B:176, B:178, B:188 (PR-M4), B:223, B:233, B:275, B:277, B:284, B:298, B:300, B:315, B:327 test 4, B:383, B:448, B:454, B:471, B:476; 6.1 metrics
- **Before**: minor budget 12 words / net 0 / 1 entry, 36-word minor cycle total, `MINOR_CYCLE_GROSS`, open question 6.
- **After**: minor row 0 in every column (both tables and `BUDGETS`), minor edit = policy failure exit 1, brief "change nothing for it", test 4 = 1-word minor edit exits 1, cause row 2 "zero edits", F22 paragraph one sentence, risk 9 residual per plan, Q1 without "12/0", Q6 placeholder (PR-M5), 1.6 sentence "Minor budget 0: all 17 non-blocking fixes are refused", report row `MINOR-EDIT (minor budget 0)`. 6.1 gained the review-3 line (proxy and blocking count as two numbers), merged with Change 27(c) into one bullet.
- **Provenance tag**: section tags in 1, 2, 3, 4.2, 4.3, 4.5, 6, 7, 8
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (sweep: no "12 words", "36", `MINOR_CYCLE`)

### Change 4: One `check` invocation with B's revert folded in
- **Status**: applied-as-corrected-by-PR-B1 and PR-B2
- **Source**: Variant A, Section 2.2 (A:48, A:62)
- **Target**: B:131, B:160, B:210-211, B:267, B:285, B:288, B:303, B:316-318, tests
- **Before**: five subcommands `hash snapshot check enforce verify`; reviser "On 2, 3 or 4 ... `enforce --in-place`".
- **After**: subcommands `hash`, `snapshot` (fallback kept per PR-B2) and `check` (`check --enforce` replaces `enforce --in-place`, same behaviour). Reviser sequence uses PR-B1's single text in Step 2 item 5, the exit table and brief step 4: exit 1 -> one cut-down or missing entry / `## deferred` line, re-run; second exit 1 -> `check --enforce`; exit 2 -> correct the call; 3/4/5/70 at any run -> stop and paste. Tests restated on `check --enforce`.
- **Provenance tag**: `<!-- Source: Base (original, modified) — ... check sequence per Changes #4, #21 as corrected by PR-B1 ... -->`
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 5: Override owned by the reviewer, one per report
- **Status**: applied-as-corrected-by-PR-B4 (all `large` sites swept)
- **Source**: Variant A, A:50, A:78
- **Target**: B:123 (example row), B:128, B:145, B:152, B:159, B:178, B:190, B:206, B:277, B:281, B:300, B:314, B:327 tests 10-11, B:391, B:446, B:447, B:472
- **Before**: ledger `override:` field with three codes, 2 per cycle, exit 4 "override refused", reviewer `large` flag with 25% rule.
- **After**: `budget` column `std | override | gap:<n> | -`; `override-reason: <id> <reason>` line in the block; one per report; second / reasonless / minor override = exit 3; "never on an `origin=changed` finding" in Step 1 prose, `## Fix Budget` and 7.3. Ledger `override:` lines, codes, `large`, `MAX_OVERRIDES=2`, `LARGE_SHARE` and old test 11 deleted (`MAX_OVERRIDES = 1` kept as the one limit constant). Risk rows 1-2 and Q2 restated.
- **Provenance tag**: tags in Step 1 block, budget table, 4.2, 4.3, 7, 8
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS

### Change 6: Seven Review Loop bullets, bullet 6 amended; bullet 8 dropped
- **Status**: applied-as-corrected-by-PR-B5 (with PR-M2, PR-M3)
- **Source**: Variant A, Section 4.1 item 5 and bullet 6 (A:163, A:177-180)
- **Target**: B:241 row, B:252-260, B:331 (M2, per PR-B5), B:332 (M3), B:336 (M7), B:362, B:480
- **Before**: bullet 8 appended; bullets 1-7 byte-identical; M2 excluded bullet 8.
- **After**: 4.2 region 5: seven bullets, 1-5 and 7 byte-identical, bullet 6 = 427 text minus the finding-id clause plus the appended clause "; the Reviser brief carries the `## Fix Budget` steps, and a blocking finding the reviser cannot fix within budget is listed `escalated` with what it needs, never expanded." (PR-M3 wording). One sentence says why bullets 2 and 5 are not amended (PR-M2). M3 pins seven bullets and the bullet-6 literals. M2 per PR-B5 (one sentence, all exclusions). Q10 says "merging bullet 6". M7 mentions the amended bullet and the `## Fix Budget` numbers.
- **Provenance tag**: 4.2 tag
- **Validation**: Structural integrity PASS | References PASS | Contradictions PASS (no "bullet 8" left)

### Change 7: Finding ids kept out of the spec text
- **Status**: applied
- **Source**: Variant A, A:55, A:118, A:130, A:238
- **Target**: B:165, B:269, B:286, B:309, test 13
- **Before**: tags such as `(F10)` excluded from word counts.
- **After**: a finding-id tag in the spec is a new id, policy failure; `path:line` still excluded from words, counted in bytes; brief step 2 "no finding id in the spec"; `words()` drops no tags; test (now 12) "`(F3)` exits 1 with reason `id`". Q9 tokenisation list drops "tags".
- **Provenance tag**: "What the checker computes" tag
- **Validation**: PASS | PASS | PASS

### Change 8: The re-review's own read-only checker run is authoritative
- **Status**: applied-as-corrected-by-PR-B4
- **Source**: Variant A, Section 2.3 (A:64-68)
- **Target**: B:110-111, B:281, B:318, test 17, B:230, B:451, B:456, B:461-462, plus PR-B4 sites B:338, B:455, B:477
- **Before**: `verify` on the receipt; `fixcheck: OK|STALE|MISSING`; data copied from the receipt.
- **After**: Step 3 item 1 runs `check` without `--enforce` with the plan's call shape, stdout only, header `fixcheck: <exit> ...`, authoritative; item 2 copies only numbers and ids from that run (`open (over budget)`, `open (escalated: budget)`, `attacks:` from the run's hunks). `verify` and its test deleted; cause row 9, risk rows 6, 10, 11, 7.3 and Q7 restated on the re-review's run.
- **Provenance tag**: `<!-- Source: ... checker run from Variant A (opus:architect), Section 2.3 — merged per Change #8 ... -->`
- **Validation**: PASS | PASS | PASS

### Change 9: No new coordinator duty
- **Status**: applied-as-corrected-by-PR-B4 (B:102 receipt sentence removed, not only appended to)
- **Source**: Variant A, A:37
- **Target**: B:102, B:104
- **Before**: intro ended "The script leaves a receipt; the next review verifies the receipt ..."; Step 0 "(coordinator or owner)".
- **After**: intro drops "snapshots the spec" and the receipt sentence, says "The next review runs the same check itself", appends A:37's sentence; Step 0 "(owner, before the experiment)". No exit-table row names the coordinator. Q3 "letting the run escalate".
- **Provenance tag**: `<!-- Source: ... coordinator sentence from Variant A (opus:architect), Section 2 (A:37) — merged per Change #9 -->`
- **Validation**: PASS | PASS | PASS

### Change 10: Fail line at the seed bar with causal falsifiers
- **Status**: applied-as-corrected-by-PR-B3
- **Source**: Variant A, Section 6 (A:324-330)
- **Target**: 6.4 (B:417-428), 7.4 (B:465-467)
- **Before**: six-row table incl. "promising" band and the 100/60 retry row.
- **After**: A's four falsifiers (sites read as cycle-2 hunks; carried count from 6.1); "Not a test of the idea" line in PR-B3's exact form (V1-V7, exits 3/4/5/70, section 6.2 bound 14.7% / 21.3%, exit 0). A's V-M1 to V-M3 are not carried (none of their inputs exist in the merged design). Cost sentence kept ("read the checker output", PR-B4). 7.4 is one sentence pointing to 6.4. Risk row 1 mitigation lost its "pre-registered retry" reference accordingly.
- **Provenance tag**: section 6 tag naming Variant A Section 6 (A:324-330)
- **Validation**: PASS | PASS | PASS

### Change 11: One short fit assessment per later adopter
- **Status**: applied
- **Source**: Variant A, Section 4.5 (A:256-261)
- **Target**: 4.6 (B:340-342)
- **Before**: paragraph with `--class-map` and `--unit line` options.
- **After**: three one-line assessments (rf-qa good, `/sc:reflect` weak, `/sc:implement` out of scope) plus B's last sentence. A's promotion paragraph not taken.
- **Provenance tag**: `<!-- Source: Variant A (opus:architect), Section 4.5 (A:256-261) — merged per Change #11; last sentence Base (original) -->`
- **Validation**: PASS | PASS | PASS

### Change 12: Fixed cycle cap of gross words and bytes, overrides included
- **Status**: applied-as-corrected-by-PR-B4 (all `ten percent` / `CYCLE-GROWTH` sites) with PR-M8
- **Source**: Variant C, Step 2 (C:62), section 6 (C:317)
- **Target**: B:178, B:184, B:204, B:211, B:227, B:228, B:277, B:300, B:315, test 18, 6.2 (B:391-393)
- **Before**: 10% growth cap, `CYCLE-GROWTH`, `CYCLE_GROWTH_PCT`, 16.1% bound, range 8-17%.
- **After**: cycle cap 600 gross words and 6,144 gross bytes, overrides included, bytes on raw added text; constants `CYCLE_GROSS_WORDS, CYCLE_GROSS_BYTES`; report line `cycle_words=512/600 cycle_bytes=3790/6144` placed on the second report line (B:184; PR-M8: B:183 is the `FIXCHECK` header). Example totals changed from gross 912 to 512 so the example does not breach the new cap (executor adjustment needed for consistency). 6.2: 13% replay kept; bound "1,200 gross words (14.7% of 8,148) and 12,288 gross bytes (21.3% of 57,763)"; prediction 13% (8% to 14.7%). Cause rows 6-7 cite the new bound.
- **Provenance tag**: budget-table and section-6 tags naming Variant C, C:62 / C:317
- **Validation**: PASS | PASS | PASS (arithmetic: 1,200/8,148 = 14.7%; 12,288/57,763 = 21.3%)

### Change 13: Exit-code layout
- **Status**: applied-as-corrected-by-PR-B1 (exit-1 action includes "add the missing entry or `## deferred` line")
- **Source**: Variant C, exit table (C:259-267)
- **Target**: B:198-208, B:203, B:279, B:301, B:316, test expectations
- **Before**: 0 OK, 1 input, 2 over, 3 ledger, 4 override; order "1, 3, 4, 2".
- **After**: 0 accept; 1 policy failure (incl. ledger incomplete, minor edit, finding-id tag); 2 argparse; 3 bad input; 4 hash conflict (`STALE-BASE`); 5 cannot write safely; 70 internal. Attribution reasons before size reasons inside exit 1. `EXIT` constant, `## Fix Budget` exit line and tests follow (2-9 exit 1; override errors exit 3; no-ledger `--enforce` exit 3; stale baseline exit 4).
- **Provenance tag**: `<!-- Source: Variant C (haiku:backend), exit table (C:259-267) — merged per Change #13; action column per Change #21 as corrected by PR-B1 -->`
- **Validation**: PASS | PASS | PASS

### Change 14: Detect a hard-gate or CRITICAL finding graded minor
- **Status**: applied
- **Source**: Variant C, Step 2 (C:53)
- **Target**: B:128, B:305, B:453
- **Before**: severity column took plain severities only.
- **After**: severity may read `MAJOR/FR-8` or `MAJOR/FR-9`; checker flags `CRITICAL`, `MAJOR/FR-8`, `MAJOR/FR-9` with grade `minor` (`parse_fixbudget` comment, risk row 8 detection).
- **Provenance tag**: Step 1 tag
- **Validation**: PASS | PASS | PASS

### Change 15: Fail closed on a missing or stale input
- **Status**: applied
- **Source**: Variant C, Step 6 (C:126)
- **Target**: B:110, B:451
- **Before**: STALE and MISSING did not stop the review.
- **After**: Step 3 item 1: missing or malformed saved copy, block or ledger, or `check` exit 3/4/5/70 -> stop with the named input error, never fall back to a first review; risk row 6 detection restated. `E-FIXCHECK-MISSING` (Step 0) kept.
- **Provenance tag**: `<!-- Source: ... fail-closed from Variant C (haiku:backend), Step 6 — merged per Change #15 ... -->`
- **Validation**: PASS | PASS | PASS

### Change 16: Fresh-worker valid/invalid probe as proof of delivery
- **Status**: applied
- **Source**: Variant C, Section 5 (C:289)
- **Target**: B:360
- **Before**: pre-flight `hash --file README.md` must print a hash.
- **After**: a fresh worker loads `/sc:spec-panel-minfix` and runs the installed checker on a tiny valid and invalid fixture (exit 0 and exit 1); reading the command file is not proof. `E-FIXCHECK-MISSING` sentence kept.
- **Provenance tag**: section 5 tag
- **Validation**: PASS | PASS | PASS

### Change 17: Spelled-out class labels where a person reads them
- **Status**: applied
- **Source**: forced L1 round (A + C)
- **Target**: B:172-176, B:185-188, B:223, B:271-275, B:128, B:481
- **Before**: `C`, `M`, `m`, "class M", "class `m`".
- **After**: `CRITICAL`, `blocking MAJOR`, `minor`, `override` in tables, report and prose; script keys stay terse, M4 maps them; chain classes A-E of 1.4 untouched.
- **Provenance tag**: budget-table and report tags
- **Validation**: PASS | PASS | PASS (no "class M" / "class `m`" left)

### Change 18: INV-001 — baseline without a reviser-authored file
- **Status**: applied-as-corrected-by-PR-B2 and PR-B4
- **Source**: invariant probe (IP:50); B:131
- **Target**: B:111, B:131, B:160, B:196, B:211, B:285, B:288, B:303, B:319, test 16, B:436, B:439, B:440, B:452, B:456, B:381-383, plus PR-B4 sites B:102, B:214, B:316, B:322, B:338, B:428, B:449, B:455, B:462, B:477
- **Before**: `snapshot` always, receipt JSON, `receipt_json`, `.fixcheck/receipt-<N>.json`.
- **After**: Step 2 item 1 uses PR-B2's wording: the saved copy when the review brief supplies its path (not true of T05/T07/T09 today), otherwise `snapshot`, which writes only `<report dir>/.fixcheck/base-<N>.md` and refuses a changed spec (exit 4). The unconditional "the Reviser brief names its path" was not written. Receipt, receipt keys, `receipt_json` removed. Paste rule (Step 2 item 7, brief step 5) per PR-B4: `result:`, `escalated:` and last `FIXCHECK` lines of the final run, and of the first run when not exit 0; report example line renamed `escalated:` to match. Escalation list sourced from `## deferred` lines and pasted `--enforce` output (PR-B4). V7 restated; metric sources = pasted lines, re-review runs, history copies. 7.1 row "new files" restored to B:440 wording; reviser calls `snapshot` 0 or 1. Risk row 7 residual: INV-001 mitigated, not closed, until the pilot; a failed pilot ends as a justified escalation (PR-B2). Test 16 (now 15): `snapshot` and `check` both refuse a hash mismatch (exit 4). Plan Risk for Change 18 is High per PR-B2 (plan-level; recorded here, the plan file was not edited).
- **Provenance tag**: Step 2 tag "baseline per Change #18 as corrected by PR-B2"
- **Validation**: PASS | PASS | PASS (sweep: `receipt`, `verify` = 0 hits in body; `snapshot` / `.fixcheck` only as the fallback)

### Change 19: INV-002 — carried prior blocking findings get a budget
- **Status**: applied
- **Source**: IP:51
- **Target**: B:114, B:281
- **After**: "one line per finding of this review, plus one line per prior blocking id still open, with its prior severity and grade" in Step 1 and the `## Fix Budget` report paragraph. Completeness rule unchanged.
- **Provenance tag**: Step 1 tag
- **Validation**: PASS | PASS | PASS

### Change 20: INV-005 — a hard gate graded minor warns instead of stopping
- **Status**: applied (with PR-M10)
- **Source**: IP:52 (reduced)
- **Target**: B:128, B:180-194, B:214, B:481
- **After**: not an input error; checker prints `GRADE-CONFLICT <id>`, keeps the grade's budget, exit unaffected (Step 1 rules); report example gains `GRADE-CONFLICT F16 (MAJOR/FR-8 graded minor)` (PR-M10); review-3 escalation lists grade conflicts (Step 3 item 3); Q11 notes the warning. Probe's reclassification not taken (plan reason).
- **Provenance tag**: Step 1 and report tags
- **Validation**: PASS | PASS | PASS

### Change 21: INV-006 — one exit-code table for every actor
- **Status**: applied-as-corrected-by-PR-B1
- **Source**: IP:53; C:259-267; A:105-110 column shape
- **Target**: B:200-206, B:160, B:288, B:211
- **After**: one column "reviser / reviewer action"; 0 reviser stops / reviewer records; 1 PR-B1 sequence / reviewer `open (over budget)`; 2 correct once, nothing counted; 3, 4, 5, 70 reviser edits nothing further and pastes, reviewer stops and escalates. `--enforce` reverts findings with an exit-1 reason and unattributed hunks and runs only after a second exit 1. No row names the coordinator.
- **Provenance tag**: exit-codes tag
- **Validation**: PASS | PASS | PASS

### Change 22: INV-007 — every early stop is a justified escalation
- **Status**: applied-as-corrected-by-PR-B4 (B:214 "from the receipts" rewritten) with PR-M9
- **Source**: IP:54
- **Target**: B:213-214 -> Step 3 item 4
- **After**: the plan's sentence in substance, plus PR-M9: "A stop with `E-FIXCHECK-MISSING` (step 0) is an install error reported to the owner, not a loop state."
- **Provenance tag**: Step 3 tag
- **Validation**: PASS | PASS | PASS

### Change 23: INV-012 — deterministic revert order for the cycle cap
- **Status**: applied
- **Source**: IP:55 (order adjusted)
- **Target**: B:211, test 18
- **After**: Step 2 item 6: within 600 words and 6,144 bytes; blocking MAJOR before CRITICAL; within a class largest gross first, then finding id; each reverted finding `escalated` with its gross. Test 16 (renumbered) checks the order; `check` outline comment states it.
- **Provenance tag**: Step 2 tag
- **Validation**: PASS | PASS | PASS

### Change 24: INV-023 — gap fills get condition words for the guard rows they name
- **Status**: applied
- **Source**: IP:56
- **Target**: B:128, budget tables, B:306
- **After**: `gap:<n>` budget value for blocking `MAJOR/FR-8`/`MAJOR/FR-9` gap fills; condition limit n; exclusive with `override`; `classify` comment; brief step 2.
- **Provenance tag**: Step 1 and budget-table tags
- **Validation**: PASS | PASS | PASS

### Change 25: INV-026 — convergence prediction stated as conditional
- **Status**: applied (with PR-M1)
- **Source**: IP:57; C-024 band
- **Target**: 6.3 (B:409), 6.1 chain-data metric
- **Before**: "Prediction: mean review-3 proxy 3.0, band 2.1 to 4.0" with three probabilities.
- **After**: "band 1.1 to 5.6 (A's estimate, about 4.1, lies inside it); central 3.3 (judgment)"; "If the two assumed rows hold ..., the mean is 2.1 to 4.0, about 3.0 at R1 = 12"; "The budget alone is not claimed to reach 3 or fewer (section 1.5)". Probabilities deleted. 6.1 chain bullet gains the within-budget-parents metric, reported before the bar.
- **Provenance tag**: section 6 tag
- **Validation**: PASS | PASS | PASS

### Change 26: INV-027 — condition-word counter with guard words
- **Status**: applied
- **Source**: A:80; IP:58 (`where`)
- **Target**: B:167, budget tables (one column), B:286, B:296-298, B:313, test 5
- **After**: `new_cond` (`if unless when whenever where except otherwise`), limits CRITICAL 2, blocking MAJOR 1, minor 0, `gap:<n>` n; risk row 5 names `when`/`where` false positives and the replay measurement; Q9 measures them.
- **Provenance tag**: checker-computes and budget-table tags
- **Validation**: PASS | PASS | PASS

### Change 27: INV-028 — cut-down success rate and carried/new split
- **Status**: applied
- **Source**: IP:59; A:305 (M9); B:479
- **Target**: B:383, B:412, B:479
- **After**: (a) Q9: harness reports the over-cap-at-first-check denominator (and why the rate is not from the harness); (b) 6.1 per-cycle bullet: cut-down success rate; (c) 6.1 review-3 bullet: carried vs new, before the bar. B:412 conditional on the unmeasured rate.
- **Provenance tag**: section 6 and section 8 tags
- **Validation**: PASS | PASS | PASS

### Change 28: B defect 1 — installed variant cites no `src/superclaude/` path
- **Status**: applied-as-corrected-by-PR-B5 (M2 exclusion merged into one sentence). PR-M6 (limit to repository file) not applied: it is advisory ("consider"), and the plan's form applies the edit to both files.
- **Source**: Variant C, C:160
- **Target**: B:241, 4.2 region 4, B:331, B:250
- **After**: region 4 replaces the lookup with C's wording in both files, with the install-watcher note (UNVERIFIED whether S1 exercises it); M2 excludes the line; B:250's claim now true; M5 unchanged. B:362 lists the template-lookup line as part of the change.
- **Provenance tag**: 4.2 tag naming Variant C (haiku:backend), C:160
- **Validation**: PASS | PASS | PASS

### Change 29: B defect 2 — repository file drops `## Unattended mode`
- **Status**: applied-as-corrected-by-PR-B5
- **Source**: Variant A, A:161-162
- **Target**: B:241, B:246/B:248 test lists, B:331, B:336, B:362
- **After**: regions 2-3 (Usage flags and section removed, repository file only); M2 excludes both; `tests/skills/test_worker_contract.py` added to M7 and to the 4.1 "run unchanged" row (placed in the B:246 row, which is the run-unchanged list; the B:248 row is the UNVERIFIED-enumeration list); B:362 notes the removed section.
- **Provenance tag**: 4.1 and 4.2 tags
- **Validation**: PASS | PASS | PASS

### Change 30: B defect 3 — one minor budget everywhere
- **Status**: applied (sweep, with PR-M4)
- **Source**: Change 3
- **Target**: all minor-allowance sites incl. B:98, B:188
- **After**: post-merge check: no text gives the minor budget as 12 or a cycle total of 36; `deferred (minor, fixcheck budget 0)` is literally true.
- **Provenance tag**: as Change 3
- **Validation**: PASS | PASS | PASS

### Change 31: One owning finding per edit
- **Status**: applied
- **Source**: C-008 amendment (C:62 single owner)
- **Target**: B:159
- **After**: "`finding` names one id, and an edit that also answers another finding is charged to its owner only"; brief step 3 "`finding` (one id)".
- **Provenance tag**: Step 2 tag
- **Validation**: PASS | PASS | PASS

### Change 32: Coupled revert
- **Status**: applied-as-corrected-by-PR-B6
- **Source**: r2B:156 amendment
- **Target**: B:159, B:211, test 14, B:447
- **After**: ledger entry may carry `depends: L<n>`; `--enforce` "also reverts, whole, every finding that owns an entry that `depends:` on one of the reverted finding's entries", each listed `escalated` with its gross (the shared sentence in Step 2 item 6); test 13 (renumbered) asserts the owning finding's other entries are reverted too; risk row 2 residual names undeclared dependencies.
- **Provenance tag**: Step 2 tag "(PR-B6)"
- **Validation**: PASS | PASS | PASS (no single-entry revert; matches "reverted whole")

### Change 33: INV-009 — brief ids cross-checked against the block
- **Status**: applied
- **Source**: IP:16
- **Target**: B:453, exit 3 meaning
- **After**: risk row 8 detection and exit-3 row: a Reviser brief id that is not a blocking id of the block is exit 3; `parse_fixbudget` comment.
- **Provenance tag**: exit-codes and section 7 tags
- **Validation**: PASS | PASS | PASS

### Change 34: INV-015 — rename counts as one entry
- **Status**: applied
- **Source**: Variant A, A:80
- **Target**: B:167
- **After**: "An identical single-token substitution repeated across units for one finding counts as one entry." appended to item 4.
- **Provenance tag**: checker-computes tag naming A:80
- **Validation**: PASS | PASS | PASS

### Change 35: Define experiment terms on first use
- **Status**: applied (with PR-M7)
- **Source**: glosses A:298, B:346, B:374, B:378
- **Target**: after B:3
- **After**: one "Terms:" line glossing D5, D9, D10/D11, V1-V6, D12 (UNVERIFIED, no gloss in any source), FR-8/FR-9. PR-M7: the spec carries no IP citation, so the wrong `IP:20` cite does not appear; the correct sources are IP:12 and IP:30.
- **Provenance tag**: `<!-- Source: Base (original, modified) — definitions line added per Change #35 -->`
- **Validation**: PASS | PASS | PASS

### Change 36: MEDIUM invariants recorded as open questions
- **Status**: applied
- **Source**: invariant probe INV-014..031
- **Target**: section 8, risk residuals
- **After**: INV-014 new Q12 (moved text); INV-015 appended to Q4; INV-016 appended to Q9 (ceiling from harness output); INV-019 appended to Q3 and "letting the run escalate"; INV-020 appended to risk row 3 residual; INV-021 via Change 32 in risk row 2; INV-029 appended to Q11; INV-030 and INV-031 no new text (already stated). PR-M5: Q6 kept as "(Removed: the minor budget is 0.)" so Q7-Q11 keep their numbers and "(question 9)" in Q1 still resolves.
- **Provenance tag**: section 8 tag
- **Validation**: PASS | PASS | PASS

### PR-B7 (review-mandated insertion, no plan change number): likelihood / impact per risk
- **Status**: applied (correction of the plan's rejected "Risk 1" row)
- **Source**: base-selection must-fix (BS:289), corrected by PR-B7
- **Target**: 7.2 risk table
- **After**: one column "likelihood / impact (judgment, UNVERIFIED)" with low/medium/high values and one reason phrase taken from each row's "why" cell. Values are the executor's reading of the existing evidence; the owner should review them.
- **Provenance tag**: section 7 tag "likelihood / impact column per PR-B7"
- **Validation**: PASS | PASS | PASS

## Review minor notes
- PR-M1 applied (Change 25). PR-M2, PR-M3 applied (Change 6). PR-M4 applied (Changes 3/30). PR-M5 applied (placeholder Q6). PR-M6 not applied (advisory; plan form kept). PR-M7 applied (no wrong cite in spec). PR-M8 applied (line placement). PR-M9 applied (Change 22). PR-M10 applied (Change 20).

## Post-Merge Validation

### Structural Integrity
- Heading hierarchy: PASS. One H1, eight H2 (1-8, seed order), H3 only below H2, no H4, no level gaps. The `#` lines at merged lines 129 and 149 are inside code fences. Code fences balanced (18 fence lines).
- Section ordering: PASS. Section 2: Step 0 -> Step 1 reviewer -> Step 2 reviser -> Step 3 re-review -> reference H3s. Section 4: 4.1-4.6.
- Document flow: PASS. Old Step 4/Step 5 headings removed; no dangling "Step 4"/"Step 5" in body text (remaining "step 4"/"step 5" hits are evidence about the S1 spec's own steps, sections 1.3/1.4/7.2).

### Internal References
- Section references (1.2-1.6, 4.2, 4.4, 4.5, 4.6, 6, 6.1, 6.2, 6.4, 7.2 row 2), step references (step 0, step 1 item 2, step 3), open-question numbers (2, 3, 4, 9, 12), 427 bullet numbers, test ids (M3, M4), validity ids (V1-V7): all resolve. Broken: 0.
- Change ids, INV ids, PR ids, debate citations (DT/IP/r2): appear only inside provenance comments; 0 in body text. All comment ids resolve to Changes 1-36 and PR-B1..B7 / PR-M items of the plan and review.
- Repository paths named as existing, verified in the worktree: `src/superclaude/commands/spec-panel.md` (bullet 6 at line 263 starts `6. **Reviser contract**`; template lookup at line 220; `## Unattended mode` at line 451), `src/superclaude/agents/rf-qa.md`, `tests/skills/test_worker_contract.py`, `tests/skills/test_spec_panel_review_loop.py`, `tests/skills/test_review_severity_rule.py`. Other paths carried unchanged from the base (the B:248 test list, `install_commands.py`, `install_skills.py`) were not re-verified.

### Contradiction Re-Scan
- One exit-code table, used consistently: PASS. The section 2 table, the `## Fix Budget` exit line, `EXIT`, Step 2, Step 3, brief step 4, tests, risk rows 5/7/8, V7 and 6.4 all use 0/1/2/3/4/5/70 with the same meanings.
- One budget table: PASS. Section 2 table, `## Fix Budget` table, `BUDGETS` and brief step 2 carry identical numbers (M4 pins them).
- No leftover removed mechanism: PASS. 0 body hits for `receipt`, `verify`, `large`, `CYCLE-GROWTH`, `ten percent`, 10% cycle cap, `MINOR_CYCLE`, `LARGE_SHARE`, 12-word or 36-word minor budget, `gap-fill`/`multi-site` codes, `--in-place`, bare `enforce`. `snapshot` and `.fixcheck/` remain only as the PR-B2 fallback (by design). Remaining "10%" hits are the cost row (10% to 23%) and the replay-deviation threshold, not the cap.
- No `src/superclaude/` path inside text to be installed: PASS. The `## Fix Budget` literal and the bullet-6 literal contain none; every remaining hit is design text, file-table rows, install commands or the description of the line being removed.
- Convergence prediction conditional (INV-026/INV-028): PASS. 6.3 states a band and a condition; "The budget alone is not claimed to reach 3 or fewer"; escalation forecast conditional on the unmeasured cut-down rate.
- New contradictions introduced: 0.
- Noted, not introduced by the merge: the reviewer's call count in 7.1 ("one call") follows the plan's "hash or check, one each"; whether a re-review also needs `hash` to fill `reviewed_sha256` for the next cycle was equally unstated in the base. `json` stays in the stdlib lists although no JSON file is written (harmless).

## Summary
- Total changes planned: 36
- Successfully applied: 36 (22 as planned, 14 applied-as-corrected-by-PR-B: 4, 5, 6, 8, 9, 10, 12, 13, 18, 21, 22, 28, 29, 32), plus the PR-B7 insertion
- Failed: 0
- Skipped: 0
- Post-merge validation: PASS
- Open for the owner: plan Review Status note should say INV-001 is mitigated, not closed, until the pilot (PR-B2; plan file not edited by this executor); PR-B7 likelihood / impact values are executor judgment; PR-M6 left as planned.
