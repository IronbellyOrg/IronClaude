# Merge Log: blocker classification spec

- Base: Variant 2 (sonnet:analyzer), `variant-2-sonnet-analyzer.md`
- Plan: `refactor-plan.md` (PC-01 to PC-33; binding amendments RB-1 to RB-3, RM-1 to RM-15)
- Output: `../merged-output.md`
- Date: 2026-11-15
- Status: complete

## Method

The merged spec was created as a header stub and filled section by section with Edit calls. Section numbers in the "Before" column are the base's (Variant 2); "After" names the merged spec's section. Provenance tags are HTML comments at the top of each merged section. Repository facts added during the merge were verified live and are listed as MC-01 to MC-13 in merged section 17.4. Only two files were written: `../merged-output.md` and this log. No git write, no GitHub action, no Jev or TypeSafe call; Python ran only through `uv run --no-project python -B` (no bytecode written; the existing `__pycache__` in `02-brainstorm/` predates the merge, checked with `stat`).

## Planned changes

| PC | Status | Before (base) | After (merged spec) | Provenance tag | Validation |
|---|---|---|---|---|---|
| PC-01 | applied | 9.1 and D1 recommend `core/REVIEW-SEVERITY.md` | 9.1: delegate-only skill folder `sc-review-severity/` with six files, options table, three surfaces; REQ-29; OD1 | Variant 1, sections 7.3 and 7.4 | pointer never names `src/`; folder absence cited (LC-20) |
| PC-02 | applied | 9.2 "block word for word" of the 4.1 paragraph | 4.1 digest (V2 paragraph plus V3 sentences, cap bullet `pragmatic.md:227` word for word, re-read MC-12) inside a versioned fence; 9.2 fence and pointer line; REQ-01, REQ-04 (brief at line 221) | Variant 1, sections 7.2 and 7.4 | `CANONICAL_CAP_TEXT` text present inside the digest (MC-11) |
| PC-03 | applied | 9.2 manifest bullets; 11 T1 | 9.2 registry rows (logical paths, kinds, surfaces, stage, version, own-scale flag, command path mapping, `installed-only` rows); tests T1, T2, T3, T14; REQ-28; verify-sync not cited for carriers | Variant 1, sections 7.3 and 10.2 | T-ids resolve (section 11.2) |
| PC-04 | applied (as amended by RB-1 and RM-10) | R10 "not solved by this spec"; 12 rollback "restore from git" | 9.4: installer facts, REQ-26 delivery rules 1 to 4, REQ-27 install check; 13.2 revert definition; 12 rollback column | Variant 3, section 7 | item (d) replaced per RB-1 (no immediate brake); install check reads the packaged registry |
| PC-05 | applied | 9.1 "no plugin mirror in version 1" | 9.5 plugin surface; mirror and parity test (T15) at stage 4 | Variant 1, decision D9 | stage 4 consistent with section 12 |
| PC-06 | applied (as amended by RM-11) | none | precedence sentence in the digest (REQ-03); 9.6; stage 3 switches `pragmatic.md` and the rf-qa family together; M10b replaces the M10 claim | invariant probe INV-027 | REQ-03 quoted in Appendix A |
| PC-07 | applied | 4.1 conditions without "required behaviour", "name the affected action", acceptance-check sentence | 4.1 digest conditions 1 to 3 carry the V3 wording; unverified safety claim "is not a Note" | Variant 3, section 3 | wording checked against V3 lines 57 to 72 |
| PC-08 | applied | 4.2 row "could not be established: Medium, tagged consumer-unknown"; GR4 Medium; 4.3 upstream row Medium | REQ-02 digest sentence (RM-6); 4.2 last row keeps the reviewer's label; 4.3; GR4; OD14 with its conditions and recommendation. Consequential edits so the base does not contradict itself: case 7 and case 14 verdicts, the "8 of 10" observation (now 7 of 10), RK2 | Variant 3, section 3 | contradiction scan: no remaining "consumer-unknown ... Medium" outcome |
| PC-09 | applied (with RM-4) | 7.3 sketch v1 counts, "UNSET means send to a person" | 7.3 version 2: states, NA rule (REQ-19), wrong() (REQ-17), table, lift (REQ-18), UNDETERMINED outside the table (REQ-20), three property tests (REQ-21), intended lowering moves (256 of 26,880; 72 of 2,560 to NA), verdict counts; deleted the "send to a person" rule; no "monotone in every input" claim | jev-uses.md version 2 and sketch version 2 | re-run MC-01 matches LC-01 and LC-02 |
| PC-10 | applied | none | GR12 (REQ-25) in 8.1; 6.1 step 5; 6.4 unattended bullet; 7.5 shadow exception; T17 | invariant probe INV-008 | consistent with REQ-22 exception |
| PC-11 | applied | 7.4 critiques the min but keeps it | 7.4 lower bound `max(0, pW + pD - 1)`; union bound reported only; null confidence for SHOW_USER, UNDETERMINED and reviewer-only; overrides `jev-uses.md:195` | Variant 3, section 5.3 | stale line noted in section 7 lead-in and 17.2 |
| PC-12 | applied | none | 7.7 judge request and response contract; bounds as pilot parameters; cache key; secrets | Variant 3, sections 5.2 and 5.4 | budgets stated as pilot parameters, not guarantees |
| PC-13 | applied | 7.5 and D3 "else use the LLM judge only" | REQ-23; judge table "needs" column; OD3; 7.8 privacy | Variant 3, section 5.4 | no remaining "LLM judge only" fallback |
| PC-14 | applied (with RM-5) | 12 stage 4 "any classifier gating"; D4 one-directional gating | REQ-22: no authority in version 1; OD4; evidence from the same judge id and version; GR12 the only exception; absence rule | Variant 3, section 10 | stage table has no classifier stage |
| PC-15 | applied (with RM-15) | 10.4 "location is a plan decision" | REQ-24: classifier reached only through a `superclaude review` subcommand without name clash | Variant 1, section 5.1 | `cli/review/__init__.py:14` cited [V] |
| PC-16 | applied | 6.2 one table plus Notes table | 6.2 data contract: metadata, Items, Notes, Observations, Offers, Filings (on first use), states, escalation, identity, cross-run rule (REQ-09), writing rules (REQ-08). The Offers `answer` values gain `file-each` so offer option 3 has a recorded value | Variant 3, sections 4.1 to 4.3 | V2 fields kept: `rests_on`, tags, Notes table, sort order, five rows |
| PC-17 | applied (with RM-12) | none | REQ-10 entity codec, evidence block with a longer fence, one reader and writer, fixtures including a triple-backtick line; JSON layer not adopted | refactor-plan decision | literal pipe character described in words, never typed inside a table cell |
| PC-18 | applied (with RM-1) | 6.6 five-row table | 6.6 REQ-07 one rule and two exceptions; path fixed before dispatch | Variant 3, section 4.1 | `.gitignore:250` and WC-4 line 34 cited |
| PC-19 | applied (with RM-3) | 6.3 offer only | 6.3 REQ-11 consent binding; needs-your-decision group first and outside the consent set unless selected; failed-verdict first sentence at a halt; one-line form when there are no Medium and no needs-your-decision rows (the zero-follow-up form recorded as addressed in INV-022; Variant 1's 10-note threshold, a Variant 1 owner decision, is not carried because no plan row adopts it) | Variant 3, section 4.5; Variant 1, section 4.3 | cadence stays once per run plus escalation halt |
| PC-20 | applied | 6.7 resolve-now inside the run | 6.7 separately authorized work; mechanical one-location fix may use L2 checks alone | Variant 3, sections 3 and 12 | consistent with offer option 1 |
| PC-21 | applied (as amended by RB-3 and RM-13) | 6.5 Option A recommended; 6.1 step 6 per-row write-back; non-goal | 6.5 facts about `/sc:issue` (LC-10), options table with new verdicts, recommended consent-bound path (OD15), REQ-13 floor, REQ-14 repository `<R>` from `origin_repo.py` plus fork guard, batch states, REQ-15 size bound 60,000 characters with overflow comments, incidents; 6.1 step 7; non-goal in section 3 | Variant 3, section 4.5 | `origin_repo.py` and `sc-issue-protocol/SKILL.md:72` verified (MC-04); no hard-coded repository in a `gh` form |
| PC-22 | applied (with RM-1, RM-9) | 6.4 "one optional key and a count; WC-4 line 35 allows extra keys" | REQ-12 three keys, `incomplete` maps to `partial`, WC-4 edit, coordinator duties, tracked-path and nesting rules, final report line | Round 2 advocates; Variant 3, section 4.6 | worker-contract edit placed at stage 2 |
| PC-23 | applied | L1 "Where": task skill plus [E] task-builder, tech-research; T5 single phrase | REQ-05; 10.3 thirteen lines in ten files with stages; auggie row; remediate_parser out of scope; T5 reverse scan with allow-list; RC2 and OD11 updated | refactor-plan LC-04 | 13 rows counted: 5 at stage 3, 8 at stage 4 |
| PC-24 | applied (as extended by RB-2 and RM-14) | none | L6 (REQ-06); 10.4 frozen Grep (REQ-30) and the known lines; Rule 6 and its template copy; OD16; pinning tests change in the same step; stage 3 row; M12 | invariant probe INV-034 | lines 990 and 333 verified (MC-02); rf-qa lines 221, 316, 333, 334 verified (MC-09) |
| PC-25 | applied | 9.3 seven-row table | 9.3 twelve-row scale map with V1 rows, the auggie row, tasklist on 7 lines, reflect 1540, "adding a row" paragraph, separate adapter approvals; native-label rule in 7.5 | Variant 1, sections 7.5 and 8.3; Variant 3, section 7 | roadmap-validate row carried without Variant 1's stage 3 placement, because the plan's stage list does not include it |
| PC-26 | applied | 11 "Eight test modules" and "nine paths" over an 8-row table | 11.1 eleven modules plus two fixtures, named patterns, pattern-dependence note (MC-10: 16 files with a broader pattern); `S1_S3_FILES` and slice change with the fence | Variant 1, section 10.1; Variant 3, section 9 | module count in text equals rows (11 plus fixtures row) |
| PC-27 | applied | 8.2 pooled Wilson on an oversampled audit; RT1, RT2 | 8.2 rate sample, diagnostic strata, every protected-risk disagreement reviewed, per-stratum intervals with sampling fraction; RT1 single event; RT2 on the random sample only | Round 2 advocate 3 N6; Variants 1 and 3 | RT2 note says oversampled strata never feed it |
| PC-28 | applied (with RM-8, RM-9, RM-14) | 12 five stages (0 measure, 1 shadow, 2 reach points, 3 copies, 4 own-scale) and 15b | 12 stages 0 Measure, 1 Offline scaffold, 2 Shadow beside the old rule, 3 Pilot, 4 Propagate, each with entry, exit and rollback; one stage 3 entry condition; own-scale adapters and authority are decisions, not stages; 16 order of work | Variants 2, 3 and 1 | stage references across sections 6, 9, 10, 11 checked consistent |
| PC-29 | applied | 14 R1 to R13 without likelihood or impact | 14 RK1 to RK18, every row with likelihood and impact; five new rows (INV-001, INV-027, INV-029, INV-036, INV-021) | Variant 1, section 13; Variant 3, section 12 | 18 rows, 6 cells each (table check) |
| PC-30 | applied | 6.4 unattended SHOW_USER rule only | REQ-16 in 6.1 step 5; 7.5 | Variant 2 section 6.4, extended | no text says SHOW_USER is asked at its gate |
| PC-31 | applied | M1 to M10 | M11, M12, M13 added (plus M10b per RM-11) | refactor-plan | metric ids resolve |
| PC-32 | applied | BW-01 to BW-16 defects | see the BW table below | various | all 16 rows applied |
| PC-33 | applied | 16.1 to 16.3 | 17.1 relabelled (item 15 superseded by sketch version 2), 17.2 extended to 13 items, 17.3 updated, 17.4 with LC-01 to LC-22 and MC-01 to MC-13; [E] labels upgraded to [V] where a plan or merge check confirmed them (Makefile sync, installers, plugin twins, worker contract) and corrected where contradicted (WC-4 extra keys) | refactor-plan | live-check totals stated at the top of section 17 |

Totals: 33 applied, 0 partially applied, 0 skipped.

## Base weaknesses (carried by PC-32)

| BW | Status | Where fixed |
|---|---|---|
| BW-01 | applied | 7.3 rewritten for sketch version 2; "UNSET means send to a person" removed (kept only as a listed false claim in 17.2 item 5) |
| BW-02 | applied | 4.2, 4.3, GR4 and section 5 now give one outcome for an unknown consequence (REQ-02) |
| BW-03 | applied | "R2" means only the run-2 folder; risks RK1 to RK18; owner decisions OD1 to OD17; no D-numbered or R-numbered ids remain outside provenance comments |
| BW-04 | applied | 11.1: eleven modules plus two fixtures, patterns named |
| BW-05 | applied | 10.3 withdraws the task-builder and tech-research claim |
| BW-06 | applied | glossary rows for MDTM, WC-2, WC-4, WC-11, SHOW_USER, UNDETERMINED and the answer states |
| BW-07 | applied | section 14 likelihood and impact columns |
| BW-08 | applied | 2.2 last paragraph points at section 4.4 |
| BW-09 | applied | 6.4 states the old claim was wrong and adds the WC-4 edit |
| BW-10 | applied | OD8 covers the classifier filling `qa.md`'s four answers (no in version 1) |
| BW-11 | applied | 9.1 and OD1 |
| BW-12 | applied | L1 and GR5 with RM-2 (`reasked` flag, no `disputed` tag) |
| BW-13 | applied | 2.2 RC6, 9.3, 10.5: tasklist on 7 lines |
| BW-14 | applied | section 10 patterns: 22 files, 120 matching lines, 139 occurrences |
| BW-15 | applied | section 7 lead-in and 7.2, 7.4 override `jev-uses.md` lines 195 and 242 |
| BW-16 | applied | 6.1 step 7 and 6.5 batch states |

## Amendments

| Id | Status | Where applied | Note |
|---|---|---|---|
| RB-1 | applied | 9.4 item 4, GR11, 13.2 revert definition, RT1, RK14, OD17 | the per-run override is described nowhere as a brake. RB-1 makes a no-reinstall brake a new owner decision; it is listed as OD17, beyond the OD1 to OD16 the plan counted, with "no recommendation in the merge plan; default no" because the plan gives none |
| RB-2 | applied | L6, 10.4, 11.1 test row, 12 stage 3, M12, OD16 | Rule 6 at `rf-qa-qualitative.md:990` and `agent_template_qa.md:333` verified (MC-02); the test pin verified (MC-07) |
| RB-3 | applied | 6.5 REQ-14, OD15, Appendix A INV-013 row | `<R>` from `origin_repo.py` (MC-04); fork guard; "limited to this repository in version 1" option with recommendation yes |
| RM-1 | applied | 6.1 step 1, 6.4, 6.6 | path fixed before dispatch; nested ledgers via nested contracts; `artifacts` only for tracked paths |
| RM-2 | applied | L1, GR5, 6.2 tags, 8.2 strata, M8 | no `disputed` tag remains in the spec (Grep: 0 matches) |
| RM-3 | applied | 6.2, 6.3, 6.4 | one `show_user` count for the three tags; not in the consent set unless selected |
| RM-4 | applied | 7.3 REQ-19 and the intended-moves list; T6 | 72 of 2,560 UNSET-to-NA moves re-computed (MC-01) |
| RM-5 | applied | 7.5 REQ-22 | absence rule stated |
| RM-6 | applied | 4.1 digest, REQ-02 | sentence verbatim from the amendment |
| RM-7 | applied | 7.2 option Q | failed lookup reads as UNSET |
| RM-8 | applied | 6.1 step 6, 11.1, 12 stage 2 and 3 | pins at `test_review_severity_mapping.py:72,128` verified (MC-05) |
| RM-9 | applied | GR7, 10.5, 12 stage 2 | |
| RM-10 | applied | 9.4 REQ-27, T13 | `doctor` target verified (MC-06) |
| RM-11 | applied | 9.6, M10b | the M10 claim was not carried |
| RM-12 | applied | 6.2 REQ-10, T7 | |
| RM-13 | applied | 6.5 REQ-15 | 60,000 characters marked as a starting value; GitHub's limit [U] |
| RM-14 | applied | 10.4 REQ-30, 12 stage 0 | lines 494 and 548 kept as [E] (not matched by the three-pattern Grep MC-09) |
| RM-15 | applied | 6.2 relation paragraph, 7.1 REQ-24, 10.6 | `review-ledger/1` verified (MC-03); the `sc-review-ledger` skill has no `src/` copy (MC-08), so its location is marked [U] |

## Additions and edits not named by a plan row

- Consequential edits under PC-08 (cases 7 and 14, observation count) and the `file-each` value under PC-16, both to keep the merged text free of contradictions; logged in their rows above.
- The stage 3 row first named `rf-analyst.md` as a carrier moving to digest v2; it is not one of the 11 carriers, so the row was corrected during writing to list it only among the merge-rule lines.
- No new repository fact was added without a live check; facts first seen during the merge are tagged "[V, this merge]" in the spec and listed as MC-01 to MC-13.

## Post-merge validation

Run with `uv run --no-project python -B` reading the merged file (no file written), plus Grep.

| # | Check | Result |
|---|---|---|
| 1 | Heading hierarchy | 71 headings, 1 H1; no level gaps; no orphan (every H3 sits under an H2) |
| 2 | Internal references | section references: 391 regex matches, 3 false positives (an external file's "section 1.1" and two percentages "3.0" and "2.0"), 388 resolved, 0 broken. Id references (outside comments): 544 total, 544 resolved, 0 broken (REQ 91 of 30 defined, OD 85 of 17, RK 26 of 18, RT 18 of 8, M 35 of 14, GR 45 of 12, T 43 of 17, L 37 of 6, RC 32 of 6, G 9 of 7, INV 54 of 38, LC 50 of 22, MC 19 of 13). PC ids appear only in provenance comments and resolve to the plan |
| 3 | Contradiction re-scan | unknown consequence: one outcome everywhere (REQ-02); UNSET handling: one rule (7.3), the "send to a person" sentence survives only as a listed false claim; offer set: needs-your-decision rows listed first and outside the consent set unless selected (6.2, 6.3, 6.4 agree); ledger location: one rule in 6.6, referenced from 6.1 and 9.1; classifier questions: six decisive everywhere, "ten" appears only as a quote of a stale input line; stage order: 0 Measure, 1 Offline scaffold, 2 Shadow, 3 Pilot, 4 Propagate, and every stage reference in sections 6, 9, 10, 11 and 13 matches; classifier authority: owner decision OD4 only, no stage implies it; repository targeting: `<R>` from `origin` everywhere, `IronbellyOrg/IronClaude` appears only in the fork guard. New contradictions found: 1 (the stage 3 carrier list), fixed |
| 4 | Table cells | 44 tables, 451 body rows, 0 rows with a cell count different from the header; 0 unescaped pipe characters inside table cells (search patterns that contain a pipe are kept in bullet lists, and the ledger codec names the pipe character in words) |
| 5 | Dashes | 0 em dash and 0 en dash characters (Unicode U+2014 and U+2013) in the merged spec and in this log |

Status: complete.

