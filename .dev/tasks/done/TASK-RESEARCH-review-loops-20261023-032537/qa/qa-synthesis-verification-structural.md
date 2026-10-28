# QA Report: Phase 5 Synthesis Verification, Structural (Step 5.25)

**Topic:** Independent structural check of the Step 5.24 corrections to synthesis components 01-06 and hypothesis cards 01-05, against the 33 consolidated findings P5-01..P5-33 and the frozen cycle-0 PASS identities
**Date:** 2026-10-24
**Phase:** synthesis-gate verification (Task Step 5.25)
**Lens:** structural synthesis verification (rf-qa, fresh context, report-only)
**Fix cycle:** 1 (of at most 2)
**Fix authorization:** false
**Governing format:** Standard QA Report Output Format (`/config/.claude/skills/task/SKILL.md:466-506`), with the Synthesis QA Agent Prompt's 12-item checklist (`/config/.claude/skills/tech-research/SKILL.md:900-942`) applied to the corrected state.
**Intended output:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-synthesis-verification-structural.md`

**Delivery limitation:** My higher-priority instructions do not allow me to write report files, so this text is the complete report for the parent to persist at the path above. I edited no package file. I did not use Git, staging, tests, agents, archive, move, delete or publication. The only file I created and then removed was my own private directory, `/tmp/ironclaude-verify.BBS4miwJ` (removal confirmed with `CLEANUP_OK`). It held in-memory reconstructions of the pre-fix files.

All relative paths below resolve under `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`. `ADV/` means `reviews/adversarial/adversarial/`.

---

## Overall Verdict: FAIL

- **Original PASS now FAIL:** 1 of 70 frozen protected identities. This is a regression, and it is listed first below.
- **Unresolved original findings:** 1 of 33 (P5-18, partly resolved).
- **New findings introduced by or exposed after the fixes:** 8. One of them is the regressed item.
- **Deduplicated failure set after cycle 1:** |F1| = 9 (1 unresolved + 8 new), against |F0| = 33.
- **Comparison contract:** regression is checked first. A regression was detected, so Step 5.27 must apply the regression halt before the monotonicity check. The literal message is under Recommendations.

## Original PASS now FAIL

| # | Frozen identity (report, file, row) | Cycle-0 basis | Corrected-state evidence | Result |
|---|---|---|---|---|
| R1 | `qa/qa-synthesis-content-2.md` row 10, "Content rules (tables over prose, no code reproduction, cited evidence, uncertainty markers)", applied to synth-04 | Cycle-0 PASS: "All three files present multi-item data in tables." Pre-fix synth-04:311 was a single sentence. | `synthesis/synth-04-options-recommendation.md:309` (§7.7), added at Step 5.24 for P5-18, is one prose paragraph that maps six screened controls to their placements, deck anchors (`:650-655`) and exclusion reasons. The rule is "Tables over prose whenever presenting multi-item data" (`tech-research/SKILL.md:1598`). The consolidation itself treated the same pattern as a verified defect (P5-15: "synth-01:69 lists seven or more distinct controls in one paragraph"). | **FAIL (regression, MINOR).** Recorded as new finding S25-N2. |

The other 69 protected identities still PASS. The table is under "Protected PASS identity re-check".

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Inputs read in full | PASS | Read Step 5.25 and neighbours (task file :255-371) and Phase 5 Findings (:641-659). Read in full: `qa/qa-consolidated-findings-phase5.md` (302 lines), `qa/qa-synthesis-fix-log.md` (all tables, Preservation Checks and the Parent Application Record; the JSON patch array was parsed by script), all six components, the chapter-1 and 10.5 regions of all five cards, and `reviews/adversarial/run-evidence.md`. Also read the task Standard QA format and the tech-research Synthesis QA prompt. |
| 2 | Application identity, checked independently of the fix log | PASS | Current SHA-256 of all 11 targets equals the fix log's "After all patches" column. I parsed the 102 literal patches and reversed them. Five deletion patches (`repl="\n"`) were not invertible directly, so I brute-forced their positions: exactly one candidate per file reproduced each consolidation-bound cycle-0 prefix (`fcbaedde…`, `f7fd5451…`, `4a352d1e…`, `e3a8900b…`, `d5cdf596…`, `8ac285ee…`, `4f324b28…`, `765fcc04…`, `64eb89ad…`, `b09d2dea…`, `9f14883c…`). A forward replay from those bytes matched every needle exactly once and reproduced the current bytes. Pre-fix byte sizes (38,294 / 25,247 / 11,546 / 53,087 / 22,943 / 49,470) equal the values quoted in the Delivery Receipts and in intake rows `:25,39,41,42,52`. |
| 3 | Every group P5-01..P5-33 checked against its cited sources | FAIL | 32 resolved. P5-18 is partly unresolved. See the register below. |
| 4 | Every frozen cycle-0 protected PASS identity re-checked | FAIL | 70 protected rows re-checked: 69 PASS, 1 regression (R1). |
| 5 | All expected sections and files exist | PASS | Sections 1-2 (synth-01), 3-4 (synth-02), 5 with 5.1-5.5 (synth-03), 6-7 (synth-04), 8 (synth-05) and 9-10 (synth-06) are all present. Each card has `## 1.`-`## 10.` plus a Table of Contents. Debate artifacts: 4 top-level and 13 in `ADV/`. Superseding package counts re-derived now: research 23, synthesis 11, qa 204, reviews 17, phase-outputs 9, resume-analysis 4, root 4, `.claude` 1, total 273. |
| 6 | No active placeholders | PASS | A grep for `{{RF_PLACEHOLDER`, `TODO`, `TBD`, `FIXME` and `[placeholder]` across `synthesis/*.md` returned nothing. |
| 7 | Five card identities preserved | PASS | Every non-heading line of `ADV/variant-N-original.md` was compared with `hypothesis-0N.md` by whole-line counts (35/37/36/36/34 substantive lines). Each substantive line appears exactly once. The generic separator `\|---\|---\|---\|` appears twice in every card both before and after Step 5.24 (checked on the reconstructed pre-fix bytes). It is markdown syntax, not identity text, and the patch did not change it. All five variant hashes still equal `input-manifest.json`. The only card change is the chapter-1 presentation note at line 29. |
| 8 | Ranks and displayed order unchanged | PASS | The 7.1 rank numbers and candidates, the 7.2 advocate orders and pair tallies, and the comparison-table "Final rank" row are unchanged by the diff. `V1 > V3 > V2 > V5 > V4` appears 3 times in synth-04 both before and after the fix. The rank-3 and rank-5 rows changed only in wording and citations. |
| 9 | No new probability | PASS | Added lines were grepped for `%`, "percent", "probabilit" and "likelihood". The only hits are negations (synth-02:42, synth-03:82). synth-04 contains 0 `%`. |
| 10 | Added Section 8 rows are UNEXECUTED | PASS | synth-05:75 (order 4), :91 (consent/scope) and :92 (checkpoint guard) each carry **UNEXECUTED** and approval or scope-decision wording. The extension to row :70 is inside an existing proposed row under the header "All proposed follow-up checks are **UNEXECUTED**" (:4). |
| 11 | Provenance blocks excluded from assembly | PASS | Each component has exactly one `## Provenance and Delivery Record (not for assembly)` at its end (lines 191/96/84/331/136/269) and one `NOT-ASSEMBLED` comment. Every `\| DONE \|`, `\| NEXT \|` and "pending" handoff line sits below that heading. No receipt claims a gate verdict. |
| 12 | Debate artifact coverage and provenance | PASS | `run-evidence.md:8-31` matches the files on disk. These anchors were re-read: transcript :49, 128-129, 167-168, 264-273 (S-002 :269, C-001 :270, C-003 :272), 343, 378-386, 425-426; refactor-plan :30-33; plan-review-evidence :4, 16; merge-log :161-163; variant-2 :10, 37. |
| 13 | 12-item synthesis checklist re-applied to the corrected state | FAIL | 8 new findings (S25-N1..N8) are listed below. |

## Summary

- Checks passed: 10 / 13
- Checks failed: 3 (items 3, 4, 13)
- Critical issues: 0
- Original groups: resolved 32, unresolved 1 (P5-18)
- New findings: 8 (all MINOR), one of them the regression R1
- Regressed protected identities: 1 of 70
- |F1| = 9, which shrinks from |F0| = 33. The regression halt still takes precedence.
- Issues fixed in place: 0 (report-only)

## Verification Register: P5-01..P5-33 (checked against sources, not the fix log alone)

| ID | Status | Evidence in the corrected text and its sources |
|---|---|---|
| P5-01 | Resolved | Handoff lines and DONE/NEXT tables moved below the non-assembled block in all six files; synth-05's Component-review row moved (:134 is now N/A). Receipts bind the intake at `qa/synthesis-component-intake.md:25` (03), `:39` (01), `:41` (05), `:42` (06), `:52` (02); `:5` reads "Status: Complete"; `:59-63` record 5 persisted, 0 pending. Bytes and hashes in the receipts equal the reconstructed pre-fix files. No receipt states a verdict. (Moved-copy fidelity defect in synth-04: S25-N6.) |
| P5-02 | Resolved | synth-03:72 `### 5.5 Evidence and Limits`, an option the consolidation allowed ("keeping 5.4 as the summary"). |
| P5-03 | Resolved | synth-02:48-59 are all `Important` (12 of 12). Rows 57-59 Notes begin "Inference limit." The preamble at :42 states why none is Critical or Minor. Template values are at `tech-research/SKILL.md:1370-1372`. |
| P5-04 | Resolved as specified; residual is new S25-N1 | synth-01:74 now reads "1215/1230 → first FINAL issues (dispatch 1916; nested record 135; parent 1932) → 1938". The range is `06-session:131-266`. Dispatch 1916 is at `research/06-session-0690ee9f.md:137` and record 135 at `:139`. The figure 1932 appears only at `research/evidence-deck.md:350`, which synth-01 does not cite (grep of 06-session for "1932" returns 0). |
| P5-05 | Resolved | synth-01:15 cites `BUILD-REQUEST.md:12`, which reads "…in sc:workflow and sc:implement…". |
| P5-06 | Resolved | synth-01:12 `**Trigger:**` repeats `BUILD-REQUEST.md:14` word for word. Method and deliverable are split to :13. |
| P5-07 | Resolved | synth-01:59 cites `evidence-deck.md:105,662`. Both lines say what is claimed: not a failure rate; clustered, modification-time selection. |
| P5-08 | Resolved | synth-03:82 cites task file :68 ("…publish externally…"). A grep of web-01 for `publica\|publish` returned no match. |
| P5-09 | Resolved | synth-01:72 (CI row) and :166 (coverage), synth-02:54 (gap row) and :87 (coverage). `04-session:102` (791), `:103` (801), `:104` (810/821), `:114-118` (Key takeaways), `:240` (mechanism 3) and `:244` (mechanism 5), plus `evidence-deck.md:280`, all say what is claimed. |
| P5-10 | Resolved | synth-02:48 cites `:505` ("Half-edited advisory meaning passes") and `:312` ("structural checks pass. Behavioral/job-wiring tests are deferred to Task 14"). |
| P5-11 | Resolved | synth-02:50 cites deck `:350`, `:558` ("Task 6 softens literal lint criterion"), `:596` ("Criterion knowingly softened") and `06-session:156-175` (1215/1219/1230, ending in the root cause). |
| P5-12 | Resolved | synth-02:53 cites `06-session:381` (`T6: complete verdict=compliant`, no `T6: Ruling:`), deck `:244` and `03-session:173-178` (raw 498/503/506/510). |
| P5-13 | Resolved | synth-02:55 adds the 13/3 summary and the condensed verdict, citing `01-session:81` ("persists a condensed targeted verdict"), `:90-103` and `:253` ("shorter on-disk targeted verdict omits some per-site detail") and deck `:858-859`. synth-02:57 adds deck `:862`. The coverage rows at synth-01:163 and synth-02:84 are updated. All nine deck items (`:855-863`) are placed in Section 4 or 9; item 7 is covered by Q17 at synth-06:29 ("shared ledgers could grow"). |
| P5-14 | Resolved | synth-05:91 binds deck `:244,:564-569`, case 06 `:381` and 03 `:173-178`. synth-05:92 binds deck `:631,:709,:729` (each line verified). The coverage rows at :116 and :119 point to them. |
| P5-15 | Resolved | synth-01:48-51 (boundary table), synth-01:78-87 (8 controls) and synth-02:69-74 (4 controls). Every control in the old prose survives; the columns follow deck `:645-658`. |
| P5-16 | Resolved | synth-03:20-21 split the row. `05-session:292-293` hold the runner and timeout unknowns. A grep of the CI case for cancel or timeout returned 0. |
| P5-17 | Resolved; new S25-N3 | synth-05:70 adds the monitor input (record 585, deck `:312`, monitor case §§2 and 4, which exist at `05-session:52,113`). synth-05:75 adds the order-4 row, citing C-001 at `ADV/debate-transcript.md:270`. synth-04:284 states the grouping, that 7.6 governs order, and the Q1 mapping (synth-06:13). |
| P5-18 | **Unresolved (partial)** | Option A (synth-04:56), D (:137), synth-05:87 and the per-control note at :309 are done. The transcript grep for these sessions returned 0, which supports "advocates did not weigh them". **Gap:** the consolidation required "each relevant control, with its deck anchor **and the limit stated there**". Option B (:83) and Option E (:161) add Session 10 Task 4 and Session 17 Task 8 without their deck limits ("Original implementation package absent from searched locations; logs/Edit survive"; "Later PR reviews are separate development work", `evidence-deck.md:650-651`). Option A states them. The §7.7 note (:309) also introduced the regression R1. |
| P5-19 | Resolved | synth-04:213 now says "one credential work family plus one documentation-baseline context". Transcript :381 ("Credential packages remain one work family"), :384 and `ADV/refactor-plan.md:33` (V4 row: "concentrated in credential/documentation work") were verified. |
| P5-20 | Resolved | synth-04:238 cites `refactor-plan.md:32` for the continuation (V5 row) and transcript `:384-385` for the reversal. `plan-review-evidence.md:16` holds the independent plan review's PASS. |
| P5-21 | Resolved | synth-04:56 cites deck `:389` ("Delivery already met the lint criterion") and `:595` ("Delivery criterion held"). |
| P5-22 | Resolved | synth-04:88 and :211 add `:168` (V4 Round 1, block 148-190) and `:379,385` (V4 Round 2, block 364-404). |
| P5-23 | Resolved | synth-04:62 removes 943/944 from the semantic list and states that v4 was never semantically reviewed, citing `01-session:85-86` (943/944 structural pass; 946 "NOT CHECKED"). |
| P5-24 | Resolved | synth-04:65 matches `01-session:323` ("first two … match … final … matches the live plan"). |
| P5-25 | Resolved; new S25-N4 | Superseding rows are added to 10.1 (:76-84), 10.4 (:151-153, :159), 10.6 (:185, :222-226) and 10.8 (:262-265). Checked now: qa has 204 files, of which exactly 13 are newer than 2026-10-23 22:14:30 plus the re-modified intake (191 + 13); total 273. "debate pending" sits at `hypothesis-04.md:187` and `hypothesis-05.md:185`, as cited. `RESEARCH-REPORT-review-loops.md:5` reads "In Progress". `qa/synthesis-gate-intake.md:5` reads "In Progress". The 22:14:30Z rows are kept. |
| P5-26 | Resolved | synth-06:176: `plan-review-evidence.md:4` (normalized hash "previously mislabeled as raw"), `:9-17` (PASS) and `:28` (source-directory guard), with 0 matches for `aba0ed57` or `a815d047`. synth-06:177 cites `merge-log.md:161-163` (FAIL record 79; PASS record 38). |
| P5-27 | Resolved | synth-06:40-56 have `### Codebase Research` (File/Topic/Agent Type), `### Web Research` (File/Topic, with web-01) and `### Gaps Log`. These match the template at `tech-research/SKILL.md:1474-1487`. The header (:5) states the adaptation. |
| P5-28 | Resolved; new S25-N7 | Each card has a presentation note at :29 between `## 1.` (:27) and `### Original Hypothesis` (:31). The only card diff is that note. |
| P5-29 | Resolved | synth-04:62, 116, 143, 167, 275 and 277 name `/config/workspace/IronClaude/src/superclaude/skills/...`. A `diff` of the checkout and installed `qa.md:82` and `quality-gates.md:24-39` is empty. Checkout managed-workspace `:42` and installed `:43` have identical text. `research/scope-rules.md:30-45` read the `src/superclaude` layer, as :280 says. |
| P5-30 | Resolved | synth-06:34 cites transcript `:49` ("task size is an observed amplifier, not an isolated cause"). |
| P5-31 | Resolved | synth-04:72, 84, 85, 179 and 211 align with `ADV/variant-2-original.md:10` ("…or leave a sibling failure intact") and `:37` ("Two outcomes must remain separate"), and with transcript S-002 `:269` and C-003 `:272`. No card or variant was edited (hashes checked). |
| P5-32 | Resolved | synth-04:67, :202 and :288 now say "only unanimous exact rank position". |
| P5-33 | Resolved | synth-04:146 restores "under the recorded Coder worktree" (card `hypothesis-04.md:153`). `ls` shows `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t10-markdownlint.log` exists at 1006 bytes. Its identity is stated as not hash-verified. |

## Protected PASS identity re-check (frozen cycle-0 set)

| Report | Protected rows re-checked | Result |
|---|---|---|
| accuracy-1 | synth-01 #2, #3; synth-02 #3; synth-03 #2, #10 | 5/5 PASS. The new tables carry Evidence lines (synth-01:55, :89; synth-02:76). New content traces to sources. 5.3-5.4 are unchanged. |
| accuracy-2 | synth-04 #1, #2, #5, S3; synth-05 #1, #2, #3, #4, #6, #10; synth-06 #2, S4 | 12/12 PASS. New synth-05 rows have 4 cells (awk check of :69-75 and :87-92). New anchors verified (585/`:312`, 2028, 498/503/506, `:244`, `:564-569`, `:381`, `:173-178`, `:631`, `:709`, `:729`, transcript `:270`). The synth-06 Web Research table uses the template's File/Topic columns. |
| tracing-1 | synth-01 #7, #8, #9, B; synth-02 #3, #8, B; synth-03 #7, #8, #9, #10, B | 12/12 PASS. Cross-file consistency holds: synth-01:163 matches synth-02:55, and synth-01:72 matches synth-02:54. §2.3 is unchanged. The monitor and CI windows stay separate (synth-01:48-51). |
| tracing-2 | synth-04 #8, #9, T3; synth-05 #6, #8, #9, #10, T4, T3; synth-06 T3 | 10/10 PASS. Current-rule statements are layer-named and source-read only. The drift is still surfaced (synth-04:62, :280). Every new synth-05 check traces to a real gap (synth-02 rows 53, 56, 59). |
| structure-1 | #5, #6 | 2/2 PASS. synth-01..03 still hold no options, ranking or Step/Action/Files/Details tables. |
| structure-2 | #3, #6, #10, #11 | 4/4 PASS. 4 + 13 debate artifacts are present. The five variant hashes equal the manifest. |
| content-1 | #8, #12 | 2/2 PASS. Every newly cited file exists and every cited range is within file length. |
| content-2 | #8, #10, S3, S4, S5 | 4/5 PASS. **#10 FAIL (R1, synth-04:309).** |
| qualitative-1 | #1, #3, #5, #6, #7, #9, #10, #11, #12, #13 | 10/10 PASS. The control tables keep every control that was in the old prose (synth-01: 09/10/17/19 plus case controls; synth-02: the same four as before). |
| qualitative-2 | #1, #5, #6, #8, #9, #12, #14, #16 | 8/8 PASS. The card preservation claims still hold, because the note adds no original-identity line. |

## Issues Found

### Unresolved original findings

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| P5-18 | IMPORTANT group, residual MINOR | synth-04:83 (Option B Opposition), :161 (Option E Opposition) | Session 10 Task 4 and Session 17 Task 8 are added without the limits the deck states, which the consolidation's correction required. | Append the limits with `research/evidence-deck.md:650-651`: "Session 10's original implementation package was absent from searched locations (logs and Edit survive); Session 17's later PR reviews are separate work". No re-ranking. |

### New findings (introduced by or exposed after the cycle-1 fixes)

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| S25-N1 | MINOR | synth-01:74 (credential row, Evidence cell) | The inserted "parent 1932" is anchored in no cited range. Its only source is `research/evidence-deck.md:350`. synth-01 cites the deck only at :14-64, 10-164, 47-164, 105, 662, 117-143, 280, 643-668, 608-668, 791-890 and 814-890, and 06-session never mentions 1932. | Add `research/evidence-deck.md:350` to that row's evidence cell. |
| S25-N2 | MINOR (regression R1) | synth-04:309 (§7.7 "Excluded with rationale") | Six controls with their anchors, placements and exclusion reasons are written as prose, against `tech-research/SKILL.md:1598`. | Convert to a table (Control / Deck anchor / Placement / Reason or limit) and keep the sentence saying the debate did not weigh these controls. |
| S25-N3 | MINOR | synth-05:11, :120 versus :75, :91, :92; and :25, :77 | (a) The text still says "the existing five discriminating checks" (:11) and "All five comparisons" (:120), but Phase 2 now has six rows and Phase 3 adds two checks. (b) :25 says every input was directly read and listed, and :77 says the bindings "are the exact existing inputs listed above", yet :75 cites `ADV/debate-transcript.md:270`, which the input table at :27-39 does not list. | Reword the counts, for example "five candidate comparisons, one scope-decision row and two Phase 3 authority/checkpoint checks". Either add the debate transcript to the input table or qualify :25 and :77. |
| S25-N4 | MINOR | synth-06:64 versus :176-177 and 10.2 | :64 says every row "not marked 'Superseding' … is kept unchanged as historical". But the P5-26 rows at :176-177 were rewritten in place without that label, and the P5-27 move took the web-01 row out of 10.2. | Change :64 to disclose these in-place Step 5.24 corrections, or mark :176-177 "Corrected at Task Step 5.24" and note the 10.2 relocation. |
| S25-N5 | MINOR | synth-04:324 (§7.8 Sources read) versus :284 (§7.6) | §7.8 still says synth-05 was read at "Lines 1-40 only; referenced by path, not by step identifiers". The corrected §7.6 now states synth-05's row grouping and its order-4 row, and nothing records the Step 5.24 reads. | Add a row or note to §7.8 saying the Step 5.24 corrections relied on a full read of synth-05 (and deck `:650-655`), attributed to the fix cycle. |
| S25-N6 | MINOR | synth-04:335-337 | The block says "The producer's original header lines, moved here unchanged". The moved `**Status:**` line drops its last sentence ("The ranking below inherits the adversarial return status `partial`…"), which stayed at :4. Nothing discloses this, whereas synth-05:140 does disclose the same kind of split. | Add the same parenthetical disclosure used at synth-05:140. |
| S25-N7 | MINOR | `synthesis/hypothesis-01.md`..`-05.md`, 10.5 Parent Persistence Record | Each record states "Saved body before this record: N bytes, SHA-256 X". X matches the pre-fix bytes (verified for all five) but not the current ones, because the 441-byte chapter-1 note was inserted above the record. Example: card 01 records 22,587 bytes and `cd72eab0…`, while the current body is 23,026 bytes. No card has an in-file Step 5.24 amendment record, unlike the components' Delivery Receipts. | Append a dated amendment receipt to each card: the Step 5.24 P5-28 note, the new pre-record body hash, and the re-run exact-once check. Do not edit the original record. |
| S25-N8 | MINOR (process record) | `qa/qa-synthesis-fix-log.md:71` | The Summary's per-file patch counts (15, 22, 5, 32, 13, 15, plus 5 cards) add up to 107, not the 102 stated at :70. Parsing the patch array gives synth-01 15, synth-02 21, synth-03 5, synth-04 31, synth-05 11, synth-06 14 and cards 1 each, which is 102. | Correct the counts in the fix log. If the original return is kept immutable, add a corrected-count note. |

### Observations, not findings

- The generic separator line appears twice in each card, both before and after Step 5.24. It is markdown syntax, so it is not an identity change.
- Out of scope: `reviews/adversarial/run-evidence.md:18` still places the canonical-identity re-review in `plan-review-evidence.md`. That file holds the identity correction, not the FAIL and re-review verdicts. `run-evidence.md` is a historical, off-limits artifact, and synth-06:176-177 is now accurate.
- Out of scope: `qa/synthesis-component-intake.md:9` keeps a stale "one pending (02)" line above its later passes. That is administrative text, not a synthesis target.

## Actions Taken

- Report-only. No target was edited.
- Reconstructed the cycle-0 bytes of all 11 targets in a private `/tmp` directory by inverting the fix-log patches. Each reconstruction matched its bound hash, and the forward replay reproduced the current bytes. The directory was removed afterwards.
- Re-read every cited source range used above in its source file, using direct Reads and bounded read-only batch scripts.

## Recommendations

- **Step 5.27 must apply the regression guard first.** The filled-in message is: `Regression detected on Item content-2.10 — previously PASS at cycle 0, now FAIL. Halt overrides monotonicity check.` The halt overrides the monotonicity result (|F1| = 9 < |F0| = 33) and the cycle cap.
- If the user authorizes continuing, cycle 2 should send P5-18 (residual) and S25-N1..N8 to one fixer, with no re-ranking and no card or variant edits beyond the S25-N7 receipt.

## QA Complete

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. Limit: all changed text and every protected-row claim were traced to sources. Unchanged text outside those claims was not re-traced sentence by sentence.
- **Tool engagement:** Read: 17 | Grep: 0 (greps ran inside Bash) | Glob: 0 | Bash: 42 (bounded read-only batches, hash, diff and reconstruction scripts, one private-directory cleanup). No web research; tavily_search 0 | tavily_extract 0 | web_search_fallback 0 | web_fetch_fallback 0.
- **Self-Audit:** Every finding above is backed by a specific tool output: hash equality, reversed and replayed patches, line-specific source reads, file counts by modification time, and awk cell counts.

| Status | Result |
|---|---|
| DONE | Verified all 33 groups against their sources: 32 resolved, P5-18 partly unresolved. |
| DONE | Re-checked all 70 frozen protected PASS identities: 1 regression (content-2 #10, at synth-04:309). |
| DONE | Found 8 new MINOR findings. Card identities, ranks and order, no new probability, UNEXECUTED rows and assembly exclusion all PASS. |
| NEXT | The parent persists this report at `qa/qa-synthesis-verification-structural.md`. Step 5.27 then applies the regression halt before any monotonicity or cap decision. |