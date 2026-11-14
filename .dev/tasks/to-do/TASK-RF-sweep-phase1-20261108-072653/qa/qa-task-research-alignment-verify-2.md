# QA Verify: Task-Research Alignment (after fix cycle 1 of the A.10.25 re-run)

**QA mode:** task-integrity (verify pass, adversarial)
**Lens:** task-research-alignment
**Date:** 2026-11-08
**Task file:** .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md (2895 lines)
**Findings under review:** qa/qa-task-research-alignment-report-2.md (B-1 to B-4, m-1 to m-4)
**Fix log:** qa/qa-task-research-alignment-fix-log-2.md
**Ground truth:** phase-outputs/plans/OQ-1-agent-wait-decision.md (42 lines, read in full)
**DESIGN at HEAD:** docs/designs/orchestrator-mode.md (7.3 block lines 514 to 551, section 11 line 738, section 13 lines 801 to 836 read; grep for agent-wait, eight, 8 templates, worktree ps, Total, headings)

Verifier did not produce the fixes. Only this report was written.

---

## Check 1: are B-1 to B-4 closed in the task file?

| Finding | Task file evidence now | Status |
|---|---|---|
| B-1 (template position) | 6.3 step (1), line 998: "after `("worktree", "current", "--json"),` (the last template, before the closing `)`) add ... so they are templates 9 and 10". DESIGN 522 to 529 order (run-current, worker-list, worker-show, task-list --ready, task-list, ps --json, list, current) matches the 7.16 list 1 to 8 (lines 1251 to 1258). 6.3 step (4) "templates 1 to 8", 7.24 (1316), 1780 "templates 9 and 10", 10.3 (1793) and OQ-16 (2881) all agree. The 6.3 Verification `grep -c '("worktree", "ps"'` = 3 is right (DESIGN has one today, line 527). | CLOSED |
| B-2 (branch (b) prompts in Phase 6) | 7.24 lens (1316) now checks `FORBIDDEN_TOKENS` is exactly `{"--include-remote"}`, ten templates, 9 and 10 the `--agent-wait` forms, and that 1.0a ran none. 6.5 (1012), 6.9 (1040), 6.11 (1054) and 6.12 (1061) are reworded. All 13 Phase 6 Contexts list "sections 7.3, 11, 12 (NFR-014 row), 13 (D10) and 15.1, the GQ-109 row, and the `### Fix cycle 3` table". The 6.15 (1082) and 6.19 (1110) fix-agent scope names the 6.3 edit places. No hit for "never sends", "keeps --agent-wait", "FORBIDDEN_TOKENS is unchanged", "R5 sentence" or "section 8 WC-16 block". | CLOSED for Phase 6. The same leftover survives in Phase 7 (N-2) |
| B-3 (8.10 count) | Line 1485: "a count of `ALLOWED_ORCA` entries is 10"; Context 1482 says 10. | CLOSED |
| B-4 (DESIGN eight-templates sentences) | 6.3 step (8) (998) names DESIGN 548, 794 and 829 with replacement text. At HEAD, 548 says "seven verbs and eight templates", 794 "`ALLOWED_ORCA` eight templates (7.3)", 829 "Only the eight allowlisted templates". The other `eight` or `8 templates` DESIGN hits (530, 738, 873) are covered by 6.3 steps (1), (3) and (4). The 6.3 Verification (1000) and the 6.4 Action and pass rule (1005) add `grep -n 'eight\|8 templates'`. | CLOSED |
| m-1 | The D10 row now cites "SPEC lines 310, 500, 504, 562 and 619" (998). | CLOSED |
| m-2 | Line 163 now says ten templates and that 1.0a uses templates 1 to 8. | CLOSED (wording note in m-D) |
| m-3 | OQ-16 added (2881). | CLOSED |
| m-4 | Line 594 still quotes `'join completed'` with single quotes. | OPEN, minor, skipped by instruction |

## Check 2: whole-file sweep for leftovers after item 6.3

Grep counts in the task file: `agent-wait` 47 lines; `eight` 27 hits; `8 templates` 3; `9 deviations` 26; `10 deviations` 10; `FORBIDDEN_TOKENS` 14; `section 8 sentence` 1; `option (b)` 4; `branch (b)` 2; `R5 edit in DESIGN sections 8 and 18` 12.

- `9 deviations`: every hit is in Phases 2 to 5 (287 to 950), the 6.3 Context and "change from" text (997, 998), or OQ-15 (2880, "until item 6.3 adds D10"). Correct.
- `eight`: 351 is Phase 3 (before 6.3, eight is right). 998, 1000, 1005, 1082, 1110 are the new B-4 checks. 1262 ("one of the eight templates") refers to the eight commands listed in 7.16 itself. 1294 to 1422 count decision records or reports, not templates. 1781 and 1782 count captured templates 1 to 8 and the eight synthetic names. No leftover.
- `FORBIDDEN_TOKENS`: every hit after 6.3 says `--include-remote` only (998, 1005, 1040, 1047, 1316, 1482, 1525, 2532). 980 names it only as the branch (b) that does not apply.
- `section 8 sentence` (789) and every `section 8` hit in lines 766 to 894 and 2103 to 2330 concern WC-14/WC-16 (R4 and Phase 12), not R5. No `never` sentence about `--agent-wait`, Orca templates or the allowlist in those regions. 2163 (Phase 12 lens) reflects the allow decision.
- `option (b)` 1167, 1209, 1223 belong to OQ-3, OQ-6 and OQ-7; 2866 says option (b) does not apply. `branch (b)` 980 and 2828 say it does not apply.
- Leftovers found: Phase 7 (N-1, N-2), described below.

## Findings

### N-1 (blocking): Phase 7 decision checks still expect OQ-1 to be a PENDING-style record

- **Evidence:** item 7.20 (line 1288) runs `grep -c 'does NOT authorize adoption' .../OQ-*-decision.md` and expects "at least 1 for each of the OQ-1 to OQ-7 files". The same expectation is repeated in the 7.30 re-check (line 1358) and the 7.34 re-check (line 1386). The record `OQ-1-agent-wait-decision.md` has no such line: `grep -c` prints 0 (run during this verify). Item 7.22 record-form lens (line 1302) requires every `OQ-*-decision.md` to have `needs_human_decision: true`, a recommendation line ending "This recommendation does NOT authorize adoption." and the blocked steps, with exceptions only for GQ-63 and OQ-8, and says "Each missing part is BLOCKING". The OQ-1 record has `needs_human_decision: false` (record line 4), no recommendation line and an `## Applied by` section instead of blocked steps. Item 7.27 (line 1337) follows "each decision record's Blocks line"; OQ-1 has none.
- **What is wrong:** these checks fail by construction against the build-time RESOLVED record. 7.20 says "On a FAIL, return to the owning item", which is 6.1, and 6.1 says "Do not rewrite it". The executor either loops or HALTs, or the 7.30 fix agent ("may correct the decision records") adds a fake recommendation to a resolved owner record. This is a leftover of the R5 rewrite: the record form changed at build time but the Phase 7 checks did not.
- **Smallest fix:** in 7.20, 7.30 and 7.34 say "at least 1 for each of the OQ-2 to OQ-7 files, 0 for the OQ-1 file (resolved at build time, no recommendation) and 0 for the OQ-8 file". In 7.22 add "(OQ-1: resolved at build time, so `needs_human_decision: false`, `status: RESOLVED`, no recommendation line, and `## Applied by` in place of the blocked steps)". In 7.27 say OQ-1 links through its `## Applied by` line (items 6.1 to 6.4).

### N-2 (blocking): Phase 7 still locates the R5 edit in DESIGN section 8 and scopes its fix agent to "the R5 DESIGN sentence"

- **Evidence:** every Phase 7 gate Context, 12 places (lines 1294, 1301, 1308, 1315, 1322, 1329, 1336, 1343, 1364, 1371, 1392 and 1399), lists "the R5 edit in DESIGN sections 8 and 18 (item 6.3)". The 7.30 (line 1358) and 7.34 (line 1386) fix agent "may correct ... the R5 DESIGN sentence".
- **What is wrong:** item 6.3 edits DESIGN 7.3, the GQ-109 row (section 2), 11, 12, 13 and 15.1 plus the `### Fix cycle 3` R5 row; it writes nothing in section 8 and there is no single "R5 DESIGN sentence". The Context is a false claim about item 6.3. The 7.24 lens (1316) checks `ALLOWED_ORCA` and `FORBIDDEN_TOKENS` in 7.3, so any breach it finds is outside the fix agent's named scope. This is the same defect as B-2, fixed in Phase 6 but not in Phase 7.
- **Smallest fix:** replace "the R5 edit in DESIGN sections 8 and 18 (item 6.3)" with "the R5 edit in DESIGN sections 7.3, 11, 12 (NFR-014 row), 13 (D10) and 15.1, the GQ-109 row and the `### Fix cycle 3` R5 row (item 6.3)" in all 12 places, and replace "the R5 DESIGN sentence" in 7.30 and 7.34 with "the item 6.3 R5 edit places in DESIGN (as listed in Context)".

### m-A (minor): items 5.1 and 5.3 still put DESIGN line 835 in section 14

Check 4 passes: item 5.12 (line 845) says "section 13" for the historical-name hits, and DESIGN line 835 (the `1.17` row "The REPORT's WC-14 draft") is in section 13 (section 13 starts at 801, section 14 at 837). But item 5.1 (line 770) and item 5.3 (lines 781 and 782) still say "section 14 row 1.17 near line 835". The edit is anchored by quoted text, so behaviour is unaffected; the hit-list file may carry "section 14" labels that 5.12 then describes as section 13. Change "section 14" to "section 13" in those three places.

### m-B (minor): the 6.15 and 6.19 re-checks omit the new template-count grep

Both say "re-run the item 6.4 commands" and then list six commands; the `grep -n 'eight\|8 templates'` command that item 6.4 now runs (line 1005) is not in the list (lines 1082, 1110). A fix agent could reintroduce an eight-templates sentence unseen until the gate verifiers. Add it to both lists.

### m-C (minor): line 1142 cites "the item 6.2 procedure" for the HALT branches

Item 6.2 is now "Log the OQ-1 decision (L3, no HALT)" and has no Branch 1 or Branch 2. Each HALT item (for example 7.4 at line 1167) restates both branches in full, so no behaviour changes. Rephrase to "the procedure below" or name a Phase 7 HALT item.

### m-D (minor): line 163 says "eight called in Phase 1"

DESIGN 528 and 529 mark `worktree list` and `worktree current` "pinned, not called in Phase 1" (by the sweep code), while step 1.0a does call them (7.16 step (3)). "Eight called in Phase 1" mixes the two. Say "eight run by step 1.0a".

### m-E (minor): D10 and Fix cycle 3 section lists are narrower than the edit

The D10 row's Section cell is "7.3, 11, 15.1" and the R5 Fix cycle 3 row ends "(7.3, 11, 13, 15.1)" (line 998), while 6.3 also edits section 12 (NFR-014 row) and the GQ-109 row. The D10 SPEC-text cell ("`worktree ps` never carries `--agent-wait`") and the R5 row ("INV-005 condition 1 forbade it") are `agent-wait` hits that quote the old SPEC rule; the 6.4 pass rule "no `agent-wait` hit forbids it" should say that these two quoting cells are expected.

### m-F (minor): no test pins "not called in Phase 1" for templates 9 and 10

The 10.3 row (line 1793) keeps "zero argv for `worktree list` and `worktree current`" but does not extend the zero-argv assertion to the two `--agent-wait` templates that 6.3 comments as "not called in Phase 1" and OQ-16 records. Scoping choice, not required by the decision record.

## Check 3: did the fixes add new defects?

| Check | Evidence | Result |
|---|---|---|
| Item numbering | Phase 6 headers 6.1 to 6.22 in order (982 to 1129); Phase 7 headers 7.20 to 7.37 in order; Open Questions OQ-1 to OQ-16 in order (2866 to 2881) | PASS |
| Invented file or line | DESIGN 548, 794, 829 (6.3 step 8), 527 to 532, 738, 873 and the 835 row exist and say what the task claims; SPEC 562 was already confirmed by report-2; OQ-16 cites no new file | PASS |
| YAML frontmatter | Parsed lines 1 to 71 with `yaml.safe_load`: 35 keys, `status: 🟡 To Do` | PASS |
| New em dashes | Em dash count is 0 on lines 163, 998, 1004, 1011, 1040, 1054, 1061, 1316, 1485 and 2881. Lines 1000, 1005, 1082 and 1110 each hold one, inside the existing `grep -c '—'` command only | PASS |
| New text stays within the record | Ten templates, seven verbs, `{"--include-remote"}`, D10 and `Total: 10 deviations.` match the record (lines 19 to 30). "Not called in Phase 1" is a builder decision now recorded as OQ-16 | PASS |

## Verdict

Blocking: N-1 (Phase 7 checks 7.20, 7.22, 7.27, 7.30 and 7.34 expect OQ-1 to have a PENDING-style recommendation line, `needs_human_decision: true` and a Blocks line, so they fail by construction against the RESOLVED record), N-2 (12 Phase 7 Contexts place the R5 edit in DESIGN section 8, and the 7.30 and 7.34 fix agents are scoped to a nonexistent "R5 DESIGN sentence").

Minor: m-A to m-F, plus m-4 carried.

B-1, B-3 and B-4 are closed. B-2 is closed in Phase 6 but its root cause survives in Phase 7 as N-2. Both new blocking findings are text edits to Phase 7 items and need no owner decision.

VERDICT: FAIL
