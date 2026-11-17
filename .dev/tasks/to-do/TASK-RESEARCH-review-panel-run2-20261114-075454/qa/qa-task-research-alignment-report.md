# QA Report: task-integrity, lens task-research-alignment

**Task file:** TASK-RESEARCH-review-panel-run2-20261114-075454.md (724 lines, 187 items)
**Date:** 2026-11-14
**Method:** adversarial cross-check of research-notes.md, BUILD-REQUEST.md and slices against task-file items. Read-only. Independence rule respected (run-1 folder and RUN2-QUEUED note never opened).

## Progress log
## Check 1: the 24 Phase 2 assignments, 4 web topics, 10 synthesis files, adjudication step

Method: for each of items 2.01-2.24 I extracted the ASSIGNMENT block (task file lines 171-219) and compared slices-to-read, code anchors, open items and output path with research-notes.md SUGGESTED_PHASES (notes lines 163-188).

| Item | Agent | Slices match | Open items match | Output path match |
|---|---|---|---|---|
| 2.01-2.18 | topic agents 01-18 | yes (all 18) | yes; every notes open item present, several added (e.g. 2.06 reads the unread SKILL.md ranges L508-L621..L1740-L1849, which agree with slice 10 line 576) | yes |
| 2.19-2.24 | value ledgers 19-24 | yes (01+02, 03+04, 05+06, 07+08, 09+10, 11+12) | yes; destination set CORE / MODULE-reflect / MODULE-tasklist / MODULE-spec / EVAL / HARNESS / KNOWLEDGE / DROP+reason, plus MODULE-pr-review and MODULE-rfqa (benign extension of "a named module" in the build request) | yes |
| 4.01-4.04 | W1-W4 | topics match notes SOLUTION_RESEARCH W1-W4 | n/a | yes |
| 5.01-5.10 | synth-01..10 | research-file feeds match notes table (synth-02 from 01,04,06,09,11,12; synth-08 from 19-24 and 17; synth-09 from 18,06,16,13 plus web-03) | n/a | yes; section mapping 1/2.1-2.8, 2.9, 3/4, 5, 6.1-6.11, 6.12, 7, 8.1, 8.2, 9/10 equals notes |
| 5.05 | axes | the 11 decision axes are the 11 axes of notes "Decision axes", same order | | |
| 5.37-5.50 | adjudication | enumeration, 12 slots plus dynamic X-13.., fold with `[PENDING-ADJUDICATION]` replacement, unaddressed-invariant table, open-question rule for HIGH/MEDIUM invariants; `--compare` only, never `--merge`, flags `--depth standard --focus correctness,risk,test-coverage --output <folder>` exactly as the build request | | |

Result: PASS for coverage of assignments. No assignment, web topic, synthesis file or adjudication element is missing.

## Check 2: five deliverables and owner constraints

| Requirement | Encoded where | Status |
|---|---|---|
| (a) overlap matrix | item 5.02 (Section 2.9, 16 capabilities, classification counts) | present |
| (b) value inventory, exactly one destination | items 2.19-2.24, 5.08 (reconciliation rows in = rows out), Gate 1/2/5 checks | present (see F2 for a duplicate-destination risk) |
| (c) conflict log, `--compare` for undecidable only | items 5.06, 5.37-5.50 | present |
| (d) target architecture | item 5.07 (7.1) | present |
| (e) future-use exposure | item 5.07 (7.2, verdict per use) | present |
| report only, no roadmap | repeated in every synthesis and QA prompt; lens 6.07 and 6.15 | present |
| independence from run 1 | embedded in 156 of 187 items; see M1 for the 31 that lack the literal rule | present with minor gap |
| no commit or push, stage `.dev/tasks` only | Phase 7 Steps 7.2, post-completion re-stage; `.claude/` unstaged check | present |
| 20-subagent limit | wave 1 = 18, wave 2 spawned after 6 returns, Gate 1 and 2 = 15, Gate 3 = 13 with instance b only after instance a returned, debates in batches of 3 | present |

## Check 3: slice gaps and questions versus agent prompts

All "Open items it must resolve" cited in notes by slice number are carried: slice 01 G6 (2.01), Q-F (2.04), slice 02 Q-F (2.05), gap 8 (2.04), gap 9 and slice 09 gap 1 (2.03), slice 02 Q-A (2.17), slice 03 gap 6 (2.08), slice 04 Q5 (2.08), slice 07 Q7 and slice 08 gap 5 (2.02), slice 11 G-4 (2.07), slice 12 gaps 1, 2, 5, 9 (2.14, 2.13, 2.12). The slices' remaining gaps and questions (about 150 across the 12 slices, for example slice 05 Q4 rubric change, Q6 H3 base commit, Q9 leak class, Q10 C-18 M7 vs M8; slice 04 Q2, Q3, Q7; slice 03 Q4, Q5; slice 01 G4, G5, G7, Q-C, Q-D) have no named Phase 2 owner. They reach the report only through the value ledgers, which are instructed to enumerate "question ... or open item" rows (items 2.19-2.24). See F3.

## Check 4: fabrication spot-check (35 citations checked against code, git and slices)

Verified correct (read at HEAD `50d4d2b9d` or via `git cat-file`/`git ls-tree` at the E2 tip):
- `findings.py:29` is `_REF_TOKEN`; `findings.py:15-22` is `CATEGORIES` (contains `unpassable-check`, `missing-requirement`); `telemetry.py:23` is `_ID_TOKEN` (so item 2.15/2.02 wording is right and slice 01's mislabel is not copied); `findings_v2.py:15-22` is the import block that pulls in `_check_flat`, `CATEGORIES`, `SEVERITIES`.
- `panel.py:80` starts `validate_reflect_profile`; `panel.py` is 707 lines and `panel_cmd.py` 129; the review package has 16 modules / 5,086 lines and 19 test modules (matches item 2.23).
- `cluster_cmd.py:27-34` holds `_FENCE` / `_BARE` calibration parsing (anchor in item 2.17).
- `.gitignore:13` is `lib/`; `tests/review/test_review_ledger.py:376-385` is `test_one_valid_block_is_enough_and_the_invalid_reviewer_is_reported` (matches).
- `spec-panel.md:256` is `## Review Loop`; `document_review_loop_prompts.md:31, 58, 70` exist; `sc-workflow-protocol/SKILL.md:85` is `## Wave 4 - Reflect`; `sc-tasklist-protocol/SKILL.md:1630` is a `/sc:reflect --mode pre --remediate` line; `sc-reflect-protocol/SKILL.md:87, 338, 349` exist and the file is 2,033 lines; `sc-implement-protocol/refs/qa.md:11` forbids panels.
- `T2bModel01` at `tests/unit/test_ccsession_tiers.py:72-73,239` and `ccsession-models.json:107` (under `src/superclaude/skills/ccsession-tag/`); `muse-ember` has zero hits in `src tests docs scripts` (item 2.04(a) is a real open question with the right expected answer).
- `pr_submit` sizes: `classifier.py` 618, `conflicts.py` 1,659, `merge_guard.py` 605 (item 2.13 exact); `cli/reflect/` has the 9 modules named in item 2.06 and `fallback.py` is 594 lines.
- The four installed variant scripts sum to 7,589 lines (2,668 + 2,050 + 1,740 + 1,131); all 17 installed variant paths exist; E2 tip, hand-off commit and the four post-hand-off commits resolve as `commit`; E2 tree has `20261111-a1`, `20261113-collab/r1..r5`, both 20261113 brainstorms, `HANDOFF-*` files and `snap.py` (5 matches).
- Slice 02 lines 531-595 do start at `C-S1` and end at `FX-22` (item 5.06's range is exact); slice 11 contains the 0/12 tier1b and 1/3 tier3 collapse figures, 4,119,747 tokens, 216 clusters / 7 multi-reviewer, TP 21 FP 4 FN 1 TN 24; slice 10 contains the 36-test `test_verdict_mapping.py` matrix and contract 1.8.0.

One citation is wrong:
- Item 2.13 (task file line 195) says "scope slice 12 reports 185 U2 spawn lines over 7 skills and 44 `subagent_type: rf-*` lines in the tech-research SKILL.md". Slice 12 line 286 says the 44 is a total over all SKILL.md files ("task-builder 23, roadmap 12, task 4, tdd 1, prd 1, tech-reference 1, tech-research 1, operational-guide 1 = 44"); tech-research alone is 1. The 185 figure is right (slice 12 line 300). See F1.

## Check 5: caveats and edge cases in "ensuring" criteria and prompts

| Caveat | Reflected? | Where |
|---|---|---|
| unit confusion 92 / 80 / 49 | yes | 2.02(b) "state the unit of each figure"; 2.08(b); web-01 context |
| `muse-ember-1.0` absence | yes | 2.04(a) |
| E2 `lib/` gitignored, engine absent | yes | 2.09(c), 2.17 anchor `.gitignore:13`, 2.22 evidence note |
| reflect contract 1.8.0 byte-identical, 36-test matrix | yes | 2.06(a), 2.11(c), 2.18(b), proposal prompts 5.38-5.49, synth-03/07/09 |
| git ref rule (`feat/review-panel` vs `.../<name>`) | yes, with a scratch repo needing an initial commit and the exact error text pasted | 2.18(c), 4.03, 5.09 |
| COMBO-REPORT:292 "no error" / "four flips" / "16 empty terra" | yes | 2.08(b)(d) |
| `[CODE-CONTRADICTED]` D14 and "no missing-task category" | yes | 2.11(d), 2.10(d) |
| other 8 of the 13 `[CODE-CONTRADICTED]` rows (#519+#518 attribution, reflect contrast Q4/Q9, alias GT3, `unpassable-ac`, `T2bModel01`, "159 functions", `theory.py` HARD set, memory lesson on fenced yaml) | NOT named in any Phase 2 item; only caught indirectly by ledgers, 3.26, 5.06 and Gate lens (e) | see F4 |
| [UNVERIFIED] numeric disagreements (combos/ 106 vs 96 vs 97 vs 107; RESULT.md 19 vs 29; quarantine 428 vs 417; Qwen 3 vs 4) | NOT assigned to any agent; 3.26 logs them as rows | see F4 |

## Check 6: dependencies and phase ordering

Consistent with the research: ledgers 19-24 depend only on slices (wave 2 may start early); 17 and 18 precede synth-08/09 and web-03 context (4.03 cites item 2.18); Phase 3 gate precedes Phase 4; synthesis precedes its gate; debates run after Gate 2 and before assembly; fold precedes assembly; the `[PENDING-ADJUDICATION]` marker is allowed only in synth-07 and removed by item 5.50; Gate 4 precedes Gate 5; report-size partition (6.02) precedes Gate 3. No ordering defect found.

## Findings

| # | Severity | Blocking | Location (task file) | Finding | Evidence | Proposed fix |
|---|---|---|---|---|---|---|
| F1 | IMPORTANT | Y | line 195 (item 2.13) | Item attributes "44 `subagent_type: rf-*` lines" to the tech-research SKILL.md and to scope slice 12. Slice 12 line 286 gives 44 as the total over ALL SKILL.md files; tech-research alone is 1. Research-notes line 72 says only "in SKILL.md" (ambiguous); the builder narrowed it to a false specific. The agent is told the figure comes from the slice, so a correct recount would look like a slice error. | slice 12 line 286: "task-builder 23, roadmap 12, task 4, tdd 1, prd 1, tech-reference 1, tech-research 1, operational-guide 1 = 44"; line 300: "family column = 185 (U2)" | Change to "44 `subagent_type: rf-*` lines over the SKILL.md files of eight skills (per-skill split in slice 12 line 286; tech-research alone 1)". Keep the [UNVERIFIED] tag and recount instruction. |
| F2 | IMPORTANT | Y | lines 203, 217, 219, 326 (items 2.17, 2.23, 2.24, 5.08) | Deliverable (b) requires every finding mapped to exactly ONE destination, but the same defect is enumerated twice with no reconciliation rule: item 2.17 builds the defect register (`DR-nnn`, with a "fix owner" column) over D-1..D-31, X-1..X-22, D1-D13, B-1..B-7; items 2.23 and 2.24 (parallel wave 2, no access to DR ids) build ledger rows for the same D-1..D-31 and X-1..X-22. Item 5.08 then requires "exactly one inventory row per ledger row AND per DR row", re-validates only ledger destinations, and allows DROP "duplicate of a named ID" only as an option. The two rows for one defect can carry different destinations (for example VL-23 CORE, DR MODULE-x), and 8.1 would show a defect twice. Gate 2 checks (lines 342, 348) only count rows. | item 5.08 text "for EVERY ledger row ... and every defect-register row (DR-nnn) exactly one inventory row"; rule (3) "exactly one destination per row"; no rule linking VL and DR rows; items 2.23/2.24 name D-1..D-31 and X-1..X-22 as ledger content | Add to item 5.08: "where a VL row and a DR row describe the same defect, keep ONE row with the single destination (DR destination wins when the defect register re-verified it) and mark the other `DROP: duplicate of <ID>`; state the number of such pairs in the reconciliation line". Add the same check to the Gate 2 partition C lenses and to Gate 5 agent 4. |
| F3 | IMPORTANT | Y | lines 232-260 (items 3.01-3.15, gate focus (b)); line 288 (item 3.26) | The build request's Gate 1 focus says "every slice gap is resolved or logged". All 15 Gate 1 prompts narrow it to "(b) every open item listed for the file is resolved or logged" (the items notes assign to the agent). Slice-level gaps with no assigned agent (see Check 3: about 150 gaps and questions) are therefore checked by no gate, and the gaps log (item 3.26) reads only the research files' Gaps sections, not the slices'. They are preserved only as ledger rows, which are not turned into Section 9 open questions (synth-10 reads gaps-and-questions.md and research Gaps sections only). | BUILD-REQUEST line 114 and research-notes line 192: "every slice gap is resolved or logged"; no occurrence of "slice gap" in the task file (grep); item 3.10 gate focus (b) | Restore the wording in gate focus (b) of items 3.01-3.15: "every open item of research-notes.md for the file AND every gap or question in the `## Gaps and Questions` section of the scope slice(s) it reads is resolved, logged under Gaps and Questions, or carried as a ledger row". Add to item 3.26: read the `## Gaps and Questions` sections of scope slices 01-12 and give each unresolved slice gap a `GQ` row (or point to its VL row). |
| F4 | IMPORTANT | Y | lines 171-219 (Phase 2 items); line 721 (Builder Notes); line 288 | 8 of the 13 `[CODE-CONTRADICTED]` rows of research-notes AMBIGUITIES_FOR_USER are named in no Phase 2 item: #519+#518 attribution, reflect contrast (Q4/Q9 "no panel/tier code"), alias GT3 vs GT1, `unpassable-ac` vs `unpassable-check`, `T2bModel01` "not referenced", "159 functions" vs 179, `theory.py` HARD set, memory lesson "fenced yaml not parsed" (grep of the task file finds none of these strings in items 2.01-2.24; only D14 (2.11), the three COMBO-REPORT rows (2.08) and the missing-task claim (2.10) are named). The [UNVERIFIED] numeric disagreements (combos/ size 106/96/97/107, RESULT.md 19 vs 29, quarantine 428 vs 417, Qwen 3 vs 4) likewise have no owner. Builder note line 721 states "Phase 2 items 2.04, 2.05, 2.08, 2.10, 2.11 and others name the contradicted claims explicitly", which is false for 2.04 and 2.05 (neither names a contradicted row). Item 5.06 and Gate 2 criterion 9 then expect these rows to be "DECIDED-BY-EVIDENCE" with code evidence that no research file was asked to produce. | research-notes lines 238-254 and 258-265; grep of task file for `#518`, `GT3`, `unpassable-ac`, `T2bModel01`, `159 functions`, `theory.py`, `fenced yaml`: no hit inside lines 171-219 | Add to the open items: 2.01(d) #519+#518 attribution (`git log`/`git show` on the two PRs, excluding `.dev/tasks`), reflect contrast; 2.04(e) `T2bModel01` usage; 2.05(e) `unpassable-ac` vs `CATEGORIES` and the `theory.py` HARD set; 2.08(e) alias GT1 vs GT3 and the combos/RESULT.md/quarantine/Qwen counts; 2.15 or 2.17(e) the "159 functions" vs 179 count and the memory-lesson claim against `cluster_cmd.py:27-34`. Correct builder note line 721 to name only the items that do. |
| M1 | MINOR | N | lines 127 and 156, 264, 272, 276, 284, 288, 370, 378, 382, 390, 396, 450, 510, 518, 522, 530, 546, 554, 558, 566, 580, 588, 592, 600, 617, 625, 629, 631, 633, 635, 639 | The build request says to embed the independence rule "in every checklist item", and Key Constraints (line 127) says it is "repeated in every item". 31 of 187 items lack the literal rule. None of the 31 spawns an agent or searches the repo (they consolidate or read files inside the task folder), so the practical risk is nil. | awk over `^- \[ \]` lines for `RUN2-QUEUED` or `review-panel-unify`: 31 misses | Either add a one-clause "(reads only paths inside this task folder; never the run-1 folder or the RUN2-QUEUED note)" to those 31 items, or soften line 127 to "repeated in every item that spawns an agent or reads outside the task folder". |
| M2 | MINOR | N | line 297 (item 4.01) | The codebase context sentence "both efforts lack a blind judge for E1" is garbled: it says "both efforts" but names one. The research notes do not support it as written (E2 used blind judges, `research-notes` and slice 03 lines 117-133; slice 11 records an adversarial judge in the shadow runs and a never-run seeded-defect quality design, so "E1 has no blind ground-truth judge" is the most the slices support). The web agent receives a muddled premise. | slice 03 lines 117, 125, 133; slice 11 lines 107, 163 | Reword to a sentence the slices support: "E2 scored reviewers with blind judges against a 16-defect ground truth; E1's quality-measurement design (seeded defects) was never run". |
| M3 | MINOR | N | slice 12 line 30 vs slice 09 | Slice 12 says the review package is "15 modules, 5131 lines"; slice 09 and the code say 16 modules / 5,086 lines (verified: `ls` 16, `cat | wc -l` 5086). The task file uses the right figures (item 2.23); no item asks anyone to log the slice-12 discrepancy. | commands run read-only | Optional: add the discrepancy to item 2.23's Gaps note. |
| M4 | MINOR | N | items 2.19-2.24 | Destination set adds MODULE-pr-review and MODULE-rfqa to the notes' MODULE-reflect/tasklist/spec. Consistent with the build request ("a named module"); noted for completeness only. | build request line 12 | none |

## Items checked and found sound (no finding)

Wave structure and concurrency; the 12-slot plus dynamic-slot adjudication design; the fold item's HIGH-invariant rule (matches build request line 132); Gate lens names and counts against the build request (Gate 3 uses 5+5+3, the top of the permitted 3-5 range, recorded in Builder Notes line 720); Gate 4's extra cross-source agent (additive); Gate 5 coverage of research 01-24, web, ledgers, synthesis and debate results; Phase 7 content (summary, stage-only, three next steps in the required order, Done status, NON-BLOCKING suggestion); report path `RESEARCH-REPORT-review-panel-unification-run2.md` and section mapping; report-only language in every synthesis and lens prompt.

VERDICT: FAIL

Blocking issues: F1, F2, F3, F4 (all IMPORTANT; each is a one-paragraph edit to the named items). Minor notes M1-M4 do not block.

