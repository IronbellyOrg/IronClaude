# QA Report - Gate 5 Anti-Omission Verification (structural, fix cycle 1)

**Status:** Complete
**Date:** 2026-11-08
**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Fix authorization:** false

Scope: report `RESEARCH-REPORT-bmad-first-use.md` (headings run through line 1795, last heading `Quality Gates and User-Accepted Exceptions`), consolidated findings (BLOCKING_COUNT 4: rows 5, 7, 65, 66; 4 JUSTIFIED rows: 52, 86, 88, 92), fix log. Line numbers below are as of this pass (the fix log's numbers are pre-edit). Checks are by meaning, not by ID. Only the 4 blocking RECOVER rows and the 4 JUSTIFIED rows were checked for (a) and (b); the 91 MINOR rows are notes and were not rechecked, per the prompt.

---

## Part A - blocking RECOVER rows represented in the report (check a)

| # | Row | Result | Evidence |
|---|-----|--------|----------|
| A1 | Row 5 (A1 O-5): flagless `--yes` takes the default branch and seeds five keys; any one of four flags selects the partial-seed branch | PASS | Report l.121 (flagless paragraph) and step 3.1 at l.1464 ("Alternative flag set, not the plan default"), Section 9 row 20(a) at l.1718, pointers at l.292, l.568, l.674, l.1021. Reproduced against source: `/opt/nvm/versions/node/v24.22.2/lib/node_modules/bmad-method/tools/installer/ui.js:807` (the four-flag test), `:838-861` (default branch: capitalised `os.userInfo().username`, `path.basename(directory)`, `English`, `English`, `_bmad-output`), `:843` (only when existing core config is empty). Text is tagged `[UNVERIFIED - never run]`; plan default unchanged; no owner decision invented. |
| A2 | Row 7 (A1 O-8a): `bmad-os-*` always preserved, re-install and ownership rules, condition 3 of FIRST_USE(P) | PASS | Report l.95 (created-path row), l.292 (definition), l.294-300 (new paragraph and 3-row table), l.529, l.578, l.612 (SC-07), l.651 (F-02), l.1022, l.1396, l.1465 (step 3.2), l.1542 (step 5.3 case d with a `bmad-os-x` fixture), l.1624 (step 7.8), l.1718 (row 20b). Reproduced against source: `ide/_config-driven.js:445-448` (existing skill dir removed before copy), `:499-516` (removal set = previous set + removals.txt), `:789-790` (`bmad-os-` skipped in cleanup), `ide/shared/installed-skills.js:45` (`isBmadOwnedEntry` false for `bmad-os-`), `core/installer.js:97-101` and `:406-425` (`_cleanupSkillDirs` after the IDE step). All cited lines say what the report says. Every statement of condition 3 I found (grep for `bmad-\*` near FIRST_USE, "untracked", "on disk") carries the `bmad-os-*` exception, except l.1408 (README wording for the manual command, left on purpose per the fix log: it describes the manual command, not the predicate). |
| A3 | Row 65 (A3 OM-1): managed-settings source ranking and default `first-wins` | PASS | W01-17 at l.860 (ranking, `first-wins`, `managedSourcesBehavior: "merge"`, D2 drop-in ignored when a higher source delivers a policy key, `ANTHROPIC_BASE_URL` rule, `[UNVERIFIED - doc-only]`); Option D row 7 l.1141, D2 Risk R6 l.1146, D2 Cons l.1150, G-03 at l.670, Section 5.3 l.974, Rationale row 5 l.1320, Q-reading row 5 l.1355, step 4D.6 l.1528, Section 9 row 15 l.1713, register G-03 l.1728. Matches `research/web-01-claude-code-user-skills-hooks-and-live-reload.md:143` (read lines 125-158). |
| A4 | Row 66 (A3 OM-2): skill-frontmatter hooks register on invocation incl. `-p` untrusted folders; "no hook-based option escapes it" was wrong | PASS | W01-18 relationship line l.867 now reads "no settings-file hook option escapes it" plus a correction, the frontmatter-hook variant, the project-skill caveat (user-level stub UNVERIFIED) and the web-01 self-disagreement; step 4D.4 l.1526 separates settings-file hooks from frontmatter hooks and cites W01-18. Grep for "no hook-based option" returns nothing; the only remaining "no hook option escapes the hold-back" is l.1526 inside "would be wrong". Matches `web-01:127`, `:156`, `:157`. |

## Part B - JUSTIFIED rows (check b)

| # | Row | Result | Evidence |
|---|-----|--------|----------|
| B1 | Row 52 (A2 Row 29, web provenance of file 03) | PASS | Cited item exists: Section 5 intro l.777 states `provider=WebSearch/WebFetch reason=tavily-unavailable` and that WebFetch returns small-model summaries. Not a pinned test, document to change, UNVERIFIED item, Feasibility or owner question. |
| B2 | Row 86 (A3 OM-22, npm dist-tags, gitHead, bins) | PASS | K-07 (l.635, pin stays 6.9.0) and W02-1 (l.884, latest 6.12.4 and 6.9.0 publish dates) exist and carry the substance that matters. Grep for `dist-tag\|gitHead\|rollback` finds no plan use of dist-tags or gitHead (hits are rollback phases). K-07 is a constraint row, not an excluded category. |
| B3 | Row 88 (A3 OM-24, 6.9.0 interactive directory prompt) | PASS | Step 3.1 (l.1464) always passes `--yes --directory "$P"`; W02-6 (l.907) carries the post-6.9.0 install-affecting changes and the `--directory` prompt remark. Justification rests on a plan step and a finding, both present. |
| B4 | Row 92 (A3 OM-28, v7 main-branch page details) | PASS | W02-11 (l.930: "does not apply to v6.12"), W02-12 (l.937: offer-and-ask pattern) and K-07 (l.635) exist and say what the justification claims. Not an excluded category. |

## Part C - new blocking issues introduced by the recoveries (check c)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| C1 | Duplicated content | PASS | The flagless alternative is stated in full at l.121 and l.1464 and as a decision at l.1718; other places are one-clause pointers (l.292, l.568, l.674, l.1021). The `bmad-os-*` rules are in full at l.294 and l.1465, pointers elsewhere. This repeats facts across sections as the report already does for other topics; no copy-paste block duplicated within one section. |
| C2 | Table of Contents / headings | PASS | `^##`/`^###` grep: every ToC entry still has its heading; the recoveries added no heading (new `bmad-os-*` content is a paragraph and a table inside 2.3, l.294-300; Section 9 gained row 20 inside the existing table, l.1718; intro at l.1695 says "Rows 15 to 20"). |
| C3 | Broken tables | PASS | New table l.296-300 has blank lines before and after and 3 cells per row. Edited rows checked cell by cell: l.1141 (3 cells), l.1146 and l.1150 (4 cells), l.670 (5), l.974 (4), l.1320 (3), l.1355 (7), l.1464/1465 (4 with escaped `\|\|` preserved), l.1718 (4), l.1728 (5). No unescaped `\|` introduced. |
| C4 | Contradiction between sections | FAIL | See finding N-1 (IMPORTANT, blocking). Concept-targeted greps for `bmad-os-`, `first-wins`/managed ranking, hook hold-back and `--output-folder` found one cluster of unqualified absolutes that the new flagless alternative contradicts. Contradictions elsewhere in the report were not hunted line by line (see Self-Audit limits). |
| C5 | Placeholders | PASS | Grep for TODO/TBD/FIXME/PLACEHOLDER/XXX/lorem/??? : only two hits, both the legitimate phrase "placeholder trees" (l.612, l.653). |

---

## Findings

### N-1 (IMPORTANT, blocking) - recovery of row 5 left three unqualified "must keep `--output-folder`" statements that the new flagless alternative contradicts

Row 5's recovery makes a command with none of `--user-name`, `--communication-language`, `--document-output-language`, `--output-folder` a presented alternative (l.121, step 3.1 at l.1464, row 20(a) at l.1718). The fix log says the old absolute "`--output-folder` must stay in every first-use command" was qualified to "that passes `--user-name`" in all places. It was qualified at l.121, l.568, l.1021 and l.1438, but not at these three:

| Location | Text still unqualified | Why it now conflicts |
|---|---|---|
| `RESEARCH-REPORT-bmad-first-use.md:406` (Section 2.5 documents table, row for `slug-configuration.md` line 53) | "Every first-use command must keep `--output-folder _bmad-output`" | The flagless alternative at l.1464 is a first-use command with no `--output-folder` (and the same document's row at l.1438 now says "in every first-use command that passes `--user-name`"). Two sections give different rules for the same file line. |
| `:681` (Section 4.2, G-14 row, Target State) | "SC-04: `--output-folder _bmad-output` kept in every command" | Target state is false for the flagless alternative, which satisfies SC-04 through the default branch seeding `output_folder` (`ui.js:858`) rather than through the flag. |
| `:910` (W02-6 relationship line) | "`--output-folder _bmad-output` stays in every command" | Same absolute, attributed to R01 s3.2; reads as a rule for all commands. |

Required fix (not applied, fix authorization is false): change each to "in every first-use command that passes `--user-name`" (or add "the flagless alternative of step 3.1 seeds `output_folder` itself, `ui.js:858`"), matching l.121/l.568/l.1021/l.1438.

### Notes (MINOR, not blocking)

- N-2 (MINOR). Step 5.3 at l.1542: case (d) now has a second fixture (untracked `.claude/skills/bmad-os-x`, no `_bmad/`) that the plan default treats as first use, yet the "Asserted" sentence in the same item still says "(c), (d), (e) leave P byte-identical". The (d) parenthetical says the assertion follows whichever glob row 20 settles, so a reader can reconcile it, but the byte-identical sentence should split the two (d) fixtures.
- N-3 (MINOR). The fix log says the new `bmad-os-*` paragraph and table went into "Section 2.1"; they are in Section 2.3 (l.294-300, directly after the FIRST_USE(P) definition). The report's own cross-references still resolve (l.95 "table below"; l.578 cites Section 2.1 where l.95 states the rule), so this is a log inaccuracy only.
- N-4 (MINOR). The report body now carries pipeline labels "audit recovery, O-5" (l.121), "audit recovery, O-8a" (l.294), "audit recovery, OM-2" (l.867), "audit recovery O-5, O-8a" (l.1718). The report already uses "fix cycle" labels in the same way; reader-facing noise only.

---

## Self-Audit

What I actively checked (every item below was a tool call in this session, not a reading of another report):

- Read in full: the task file's embedded prompt (line 457), `qa-anti-omission-consolidated-findings.md` (154 lines) and `qa-anti-omission-fix-log-cycle1.md` (51 lines).
- Read from the report: lines 1-330 (Sections 1, 2.1-2.3), 400-409 and 470-530 (Section 2.5 documents table, current-state diagram, summary table), 560-690 (Sections 3.1-4.2), 770-948 (Sections 5.1-5.2), 960-1000 (5.3), 1134-1157 (Option D), 1244-1250 (comparison table), 1308-1367 (Section 7), 1455-1544 (Phase 3, Phase 4, Phase 5 start), 1690-1740 (Section 9 and register). Not read line by line: lines 330-400, 410-470, 690-770, 1000-1134, 1157-1244, 1250-1308, 1367-1455, 1544-1690, 1740-1804.
- Reproduced against installer source (read-only, `/opt/nvm/...`): `ui.js:796-870`, `ide/_config-driven.js:440-520` and a Grep of `bmad-os-`/`isBmadOwnedEntry` over `tools/installer` (hits at `_config-driven.js:789-790`, `installed-skills.js:43-45`), `core/installer.js:92-105` and `:404-426`. All line cites in the recoveries for rows 5 and 7 held.
- Reproduced against research: `research/web-01-...md:125-158` for rows 65 and 66 (ranking text at :143, frontmatter-hook text at :127, :156, :157).
- Searches run on the report: `bmad-os-` (all 20 hits), `first-wins`, `flagless`, `no hook-based option`, `hold-back`, `FIRST_USE(P)`, `untracked|on disk`, `--output-folder` (all hits), "every command / must keep / must stay", `dist-tag|gitHead|rollback`, placeholders, pipeline labels, all headings, "row 20" references.

Why I believe the finding count (1 blocking, 3 minor) is credible: the four recoveries were reproduced end to end against source and web-01, which is why Part A passes. The one blocking issue came from searching for every statement of the rule the recovery changed (`--output-folder` in every command), not from the places the fix log said it touched; the fix log claims full propagation and the grep shows three misses. Zero would not have been credible given that the fix log asserts propagation across about 15 locations per row.

Limits (marked UNVERIFIED, not claimed as checked):
- Contradictions were hunted by concept (the four recovered topics), not by reading every line of the 1804-line report; roughly 800 lines were not read. A contradiction involving a fifth topic is not excluded.
- The 91 MINOR RECOVER rows and the "Recovery text for pinned-test rows" were not rechecked (prompt: MINOR findings are notes).
- Claims about Claude Code documentation (rows 65, 66) were checked against the research file web-01 only; the live documentation was not re-fetched, so they stay `[UNVERIFIED - doc-only]` as the report itself tags them.
- No test or installer was run.

## Summary

- Checks: 13 total (A 4, B 4, C 5). Passed 12, failed 1 (C4).
- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (scope of C4 limited to the four recovered topics, see Limits)
- **Tool engagement:** Read: 21 | Grep: 19 | Glob: 0 | Bash: 0 (every call mapped to a check above)
- Unrecovered blocking rows: 0 of 4. Wrongly justified rows: 0 of 4. Newly introduced blocking issues: 1.
- Severity counts: CRITICAL 0, IMPORTANT 1 (N-1), MINOR 3 (N-2, N-3, N-4).
- Edits to the report or any product file: none. Only this file was created.

## VERDICT: FAIL

Blocking issue to fix before the gate can pass: N-1 (three unqualified "`--output-folder` must stay in every command" statements at `RESEARCH-REPORT-bmad-first-use.md:406`, `:681`, `:910` that the row 5 recovery contradicts).

## QA Complete
