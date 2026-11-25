# QA Report - Gate 3 Structural Verification of Fixes (cycle 1, review 2)

**Status:** Complete
**Topic:** Observer / Sweep / Dashboard technical reference
**Phase:** fix-cycle (structural verification, report-only, fix_authorization: false)
**Fix cycle:** 1
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md
**Inputs read:** qa-consolidated-findings.md, qa-fix-log-c1.md (same qa/ folder), the whole document (all 1,392 lines, read in 7 chunks), the cited snapshot files (/home/coder/.cache/ic-snap-20261120/master/...) and the design-package files (checkout).

---

## Overall Verdict: PASS

`|F_1|` = 9 blocking findings (GD-1 to GD-9). `|F_2|` = 0 open blocking findings. Regression check (run first): no item that passed review 1 fails now (C8 wording, neutrality, 16-section order, TOC, frontmatter, and the PASS lenses spot-checked; see Part 2). No new blocking issue was introduced by the fixes. Four minor notes (not rechecked, never fail the review).

## Part 1. Status of each blocking finding

| ID | Status | Evidence (what I read myself) |
|----|--------|-------------------------------|
| GD-1 (length) | RESOLVED | `wc -l` = 1,392 (was 1,698); the finding's blocking threshold is more than 1,400 and the stated target is at most 1,400. Protected parts still present: 2.5 comparison matrix (document L244-249 and overlaps table L253-258), 8.1 Orca verb inventory (L943-976), 14.4 A contradictions list and B UNVERIFIED list (L1263-1297), five 13.1 scenarios A-E plus new F (L1164-1169), every DEFECT-CANDIDATE row with full wording (14.1 L1225 and L1228, 14.5 L1321-1322). Section 14.4 C is now one pointer line (L1299). Note m-1: 1,392 is still 192 lines above the 800-1,200 Standard ceiling; the Document History row discloses it. Not blocking under the rule the finding set. |
| GD-2 (14.2 columns) | RESOLVED | L1235 header is `Item / Severity / Description / Effort to Fix` (the template columns named in the lens report); every row (L1237-1244) reads "not rated" in both columns, with the research label and evidence in Description; no data invented. Lead-in sentence at L1233 matches. |
| GD-3 (C8 wording) | RESOLVED | Grep for "flagged for the owner" returns L556, 636, 1225, 1228, 1295, 1308, 1314-1322, 1324. I read each: the full text "Remediation task not created (read-only brief); flagged for the owner" is on 14.1 D-1 (L1225), 14.1 C8-8 (L1228), 14.5 C8-4 (L1317), C8-5 (L1318), C8-7 (L1320), and also on C8-1, C8-2, C8-3, C8-6, C8-8, C8-9 (L1314-1316, 1319, 1321-1322), 5.3 (L636) and 5.2 D-1 (L556, lower-case lead-in, full words). Rule 4 at L1308 states it. |
| GD-4 (12.3 cross-reference) | RESOLVED | L1145 Do-This-Instead now reads "Observer: follow the 5.1 Conventions (template constants, `assert_allowed`, pinned tests); sweep: 13.1 B; never shrink the forbidden set". The first 5.1 Conventions bullet (L477) says exactly: change the template constants, `assert_allowed` and the pinned tests; never remove a forbidden prefix. The only other "13.1 B" references (L727, 5.4 Conventions; L1145 sweep half) are about the sweep and are correct. |
| GD-5 (13.1 row D) | RESOLVED | Row D (L1167) now has: step 1 field set in `Collector.run_once` (collector.py:248); step 6 `KeySource._take` / `_take_escape` (keys.py:176, 217), escape decoder maps only finals A and B, help-line constants `QUESTIONS_KEYS_LINE`, `QUESTIONS_LINK_KEYS_LINE`, `KEYS_LINE` (view.py:91-118); pitfall names `test_session.py:339-353` and `:359-393`. Code facts read in the snapshot: keys.py:176 `_take`, :217 `_take_escape`, :227 and :233 map only `A` and `B`; view.py:30 `KEY_NAMES`, :91, :93-95, :118 constants; collector.py:248 `run_once` builds each `CycleResult`; test_session.py:339-353 loops over `r`, `x`, `Z`, `1`, space, Backspace and asserts no change; :359-393 asserts `e` is the only export key and `q` / Ctrl-C the only quit keys. 5.2 convention line (L568) names the `keys.py` edit. |
| GD-6 (L313 reference) | RESOLVED | Section 3 tree line (L308) now says "artifact list in 5.5"; 5.5 holds the 15-row step and artifact table (L762-776). |
| GD-7 (design-package chain) | RESOLVED | New rows: 10.2 (L1068), 13.1 scenario F (L1169), 13.2 (L1202). Facts checked in `/home/coder/workspaces/IronClaude/.dev/design/orca-observer-20261106/`: render.py:20-24 `designs(batch)` builds the dict from the layout modules (set 1 `group_a` + `group_b`, set 2 `agent_focus`); render.py:128-130 `--show` indexes `designs(args.batch)[args.show]` (a slug of the other batch gives `KeyError`) and `--width` is `type=int` with no check; DESIGNS entries carry `name, render, question, omits, tradeoff, data, missing` (group_a.py:225, agent_focus.py:183); tests/test_designs.py: `Semantics` 10, `SafeText` 5, `Layouts` 4 test methods (19), `test_all_scenarios_widths` asserts `len(ds) == 20` and widths 160/144/116/80 with `SYNTHETIC` (L80-87), `test_export_manifest` asserts 10 concepts for both `ROOT` and `ROOT/agent-focus` (L104-108); tests/test_gallery.cjs exists. |
| GD-8 (page.py usage) | RESOLVED | L829 reads `page.py <run>;  page.py --open;`. Snapshot page.py:381-387: `sys.argv[1:] == ["--open"]` or `len(sys.argv) == 2`, else usage exit. L774 and the other `page.py --open` mentions agree. |
| GD-9 (skeleton A) | RESOLVED | L1179-1180 now say `RULES` and `CLASSES` are tuples, insert `Rule("example", _rule_example)` before `Rule("fallback", ...)`, add "example" inside `CLASSES`, add a ninth name `C_EXAMPLE` in the unpack, add `NEXT_INSPECTION["example"]`. Snapshot: classify.py:42-51 unpacks eight `C_*` names from `CLASSES`; :345-355 `RULES` is a tuple with `fallback` last; :130-136 `_classification(class_name, rule, evidence, waiting_kind=None, notes=())`; models.py:50-59 `CLASSES` is a tuple of 8; report.py:54-68 `NEXT_INSPECTION` dict. No `+=` and no undefined `C_EXAMPLE` remain. Skeletons B, C, E are dropped with a one-line description (L1171), as the fix log says. |

`|F_1|` = 9; resolved 9; open 0.

## Part 2. New issues introduced by the fixes (adversarial pass)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| N1 | Template structure intact, 16 sections in order | PASS | Heading list (grep `^#{1,3} `): sections 1-16 at L161, 183, 264, 329, 391, 916, 931, 937, 1004, 1043, 1080, 1115, 1156, 1208, 1332, 1351, in order; Appendix A (L1372) and Document History (L1386) follow; subsections 2.1-2.5, 3.1, 4.1-4.3, 5.1-5.6, 8.1-8.3, 9.1-9.3, 10.1-10.3, 11.1-11.3, 12.1-12.3, 13.1-13.2, 14.1-14.6, 15.1-15.2 all present. Every 5.x has Purpose, Key Files, How It Works, Public Interface, Dependencies, Consumers, Conventions. Frontmatter (L1-48) intact. |
| N2 | Table of Contents up to date | PASS | L138-155 list 16 sections plus Appendix A and Document History; each title matches its heading text. No heading was added, removed or renamed (fix log, confirmed by the heading list). |
| N3 | Placeholders | PASS | Grep (case-insensitive) for TBD, TODO, FIXME, XXX, lorem, placeholder: only legitimate uses (the gate check "placeholders" at L791, the entry field `todo` at L805, the allowlist word "placeholders" at L1165). |
| N4 | Fabricated or uncited facts in the new or edited text | PASS | Every code fact in the edits of GD-4, 5, 6, 7, 8, 9 was re-read at source (Part 1). Nothing new was found that has no source. |
| N5 | Broken tables | PASS (with minor note m-2) | awk column check over all 456 table rows: only two rows differ from their header (L959 and L974, in 8.1). Both carry unescaped `|` inside code spans (`tab list|close|switch|create`, `reference add|find`, `automations list|show|runs`). Both strings also appear in the synthesis file `synthesis/synth-06-integration-config-perf.md` (L56, L71) and in research 05 L527, so they are not introduced by the fixes. All tables the fixes touched (14.1, 14.2, 14.5, 12.3, 10.2, 13.1, 13.2) have matching column counts. 26 code-fence lines (even). |
| N6 | Lost C8 wording | PASS | See GD-3: the full sentence is on every DEFECT-CANDIDATE row and every KNOWN LIMIT row (14.5 L1314-1322); rule 4 at L1308. No DEFECT-CANDIDATE was relabelled (C8-8 and C8-9 still bold DEFECT-CANDIDATE; C8-1 to C8-7 still KNOWN LIMIT (cited)). |
| N7 | Unification recommendation | PASS | Grep for unif / should merge / should consolidate / recommend: hits are only the neutrality statements (L53, 56, 130, 1374) and the entry field `recommend` (L805). The L1186 "Unification touch points" paragraph states facts and says "facts only; no recommendation". Nothing recommends unifying. |
| N8 | Dangling cross-references after the cuts | PASS | Checked every reference to cut material: "14.5" for C8 pointers (L260, 636), "8.1" for the Orca allowlist table (L680), "10.1" for error codes (L451), "4.1 (a)" for the observer flow (L416), "2.5 overlaps" for sanitizers and status sets (L696, 1138), "5.6" for the render pipeline (L361), "5.5" for run artifacts (L308, 359). All targets exist. The only "14.4 C" mention outside the heading is in the Document History as a record of the cut. `gaps-and-questions.md` exists in the task folder. |
| N9 | Line count and structure | PASS (note m-1) | 1,392 lines, at or under the 1,400 limit set by GD-1; Document History states the cycle-1 cut honestly (L1390). |
| N10 | Regression check (runs first) | PASS | No review-1 passing item fails now: C8 wording (N6), neutrality (N7), the PASS lens items on evidence and domain accuracy were spot-checked on the edited rows (14.1, 14.5, 5.3, 5.5); cuts left Completeness Status and 15.1 consistent (15.1 row lists the files re-read this cycle, matching the fix log). |

## Part 3. Minor notes (not rechecked, never fail the review)

| # | Location | Note |
|---|----------|------|
| m-1 | Whole document | 1,392 lines is within the 1,400 limit the finding set but 192 above the 800-1,200 Standard ceiling. Disclosed in the Document History row. |
| m-2 | L959, L974 (8.1) | Unescaped `|` inside code spans split cells in GFM renderers (3 extra cells in each row). Pre-existing from the synthesis file. Escape as `\|` if the file is rendered. |
| m-3 | L1167 (13.1 row D, step 6) | "the only places a `Key` is built" is slightly too strong: keys.py also builds `Key("escape")` at :165 (lone-ESC timeout in the read loop) and `Key("text", ...)` at :214 (`_take_utf8`, called from `_take`). Still true that keys.py is the only file. |
| m-4 | L478 vs L1166 | 5.1 says "exporting a new row field is a four-place edit (13.1 C)"; 13.1 C lists five steps. Appendix A (L1381) credits GF-5 only for 5.6, 14.4, 14.5 though 10.2, 13.1 F and 13.2 now also use it. |

## Summary
- Blocking findings from review 1 (`|F_1|`): 9. Open now (`|F_2|`): 0. Strictly fewer (0 < 9).
- New blocking issues introduced by the fixes: 0.
- Checks passed: 19 / 19 (9 findings + 10 new-issue checks). Checks failed: 0.
- Critical issues: 0. Issues fixed in place: 0 (fix authorization false; the document was not modified).

## Confidence
- **Confidence:** Verified: 19/19 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 22 | Grep: 11 | Glob: 2 | Bash: 1 (awk table check; read-only)
- No web research performed; no Tavily or fallback calls.
- Limits: tests were not run (read-only brief); facts about files that exist only on origin/master under `.dev/` were not re-read because the fixes did not touch them.

## Verdict line
PASS: 9 of 9 blocking findings resolved, 0 introduced, `|F_2|` = 0 versus `|F_1|` = 9.

## QA Complete
