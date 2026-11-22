# QA Report — Tech Reference Qualitative Review (lens: crossref-chain)

**Topic:** Observer, sweep and dashboard family technical reference
**Date:** 2026-11-20
**Phase:** tech-ref-qualitative (lens: crossref-chain)
**Fix cycle:** N/A
**Status:** Complete
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md (1698 lines)
**Fix authorization:** false (report only)

---

## Method

Read the whole assembled document (lines 1-1698, five Read calls) and traced each chain link by line number. Line numbers below are lines of the document under review as read in this session. Grep was used to confirm absences (a link is "missing" only after a search for the term found nothing in the expected section). Drift axis does not apply (this is a tech-ref-qualitative lens, not task-qualitative), so there is no Axis column. No Inherited Structural Verdict section was in the spawn prompt, so structural checks were done standalone for the cross-reference items only.

## Part 1. Chain tables (checklist item 1)

Link numbering: L1 = 2.2 subsystem map; L2 = Section 3 tree; L3 = Section 4 data-flow diagram; L4 = Section 5.x; L5 = Section 8 verbs and formats; L6 = Section 9 settings; L7 = Section 10 error handling; L8 = Section 11 caps; L9 = Section 13 extension scenario; L10 = Section 14 limitation or debt.

### Chain 1: Observer

| Link | Present | Location |
|---|---|---|
| L1 | yes | 2.2 rows "5.1 Observer data contract" (line 216) and "5.2 Observer interaction layer" (line 217) |
| L2 | yes | Section 3 tree `src/superclaude/cli/observe/` (lines 272-283), output dir line 310 |
| L3 | yes | 4.1(a) diagram (lines 340-353) |
| L4 | yes | 5.1 (lines 410-528), 5.2 (lines 531-648) |
| L5 | yes | 8.1 rows (lines 1151-1153); 8.2 rows (lines 1190-1191, 1196); snapshot format row (line 1211) |
| L6 | yes | 9.1 schema row (1238); 9.2 `XDG_STATE_HOME`, `NO_COLOR` (1249-1250); 9.3 flags and gate constants (1261-1262) |
| L7 | yes | 10.1 rows (1276-1280); 10.2 (1291, 1296); 10.3 (1303) |
| L8 | yes | 11.1 (1317-1319); 11.2 (1329-1331) |
| L9 | yes | 13.1 C and D (1421-1422); 13.2 rows (1463-1467) |
| L10 | yes | 14.1 (1487-1491); 14.2 (1504-1510); 14.5 C8-9 (1608) |

No missing link.

### Chain 2: Sweep

| Link | Present | Location |
|---|---|---|
| L1 | yes | 2.2 rows 5.3 (218) and 5.4 (219) |
| L2 | yes | Section 3 tree (285-294), output dir (311) |
| L3 | yes | 4.1(b) diagram (355-364) |
| L4 | yes | 5.3 (656-768), 5.4 (772-888) |
| L5 | yes | 8.1 rows (1154-1160); 8.2 rows (1188-1189); Markdown and JSON formats (1212-1213) |
| L6 | yes | 9.2 `ORCA_CLI_COMMAND`, `GIT_OPTIONAL_LOCKS` (1248, 1255); 9.3 `sweep run` flags and gate constants (1263-1264); 9.1 `.gitignore` row (1240) |
| L7 | yes | 10.1 rows (1281-1283); 10.2 (1292-1294); 10.3 (1304) |
| L8 | yes | 11.1 (1320-1321); 11.2 (1332-1334) |
| L9 | yes | 13.1 A and B (1419-1420); 13.2 rows (1459-1462) |
| L10 | yes | 14.1 (1482-1486, 1495-1496); 14.5 C8-1 to C8-5 (1600-1604) |

No missing link.

### Chain 3: Agent-work-report (living report)

| Link | Present | Location |
|---|---|---|
| L1 | yes | 2.2 row 5.5 (220) |
| L2 | yes | Section 3 tree (296-300), state locations (312-315) |
| L3 | partial | 4.1(c) (366) is prose with a pointer to 5.5; the only diagrams are in 2.1 (199-202) and 5.5 "How It Works" (916-921). See M-2 |
| L4 | yes | 5.5 (896-1023) |
| L5 | yes | 8.1 rows (1161-1165); 8.2 rows (1193-1195); run-folder format (1214) |
| L6 | yes | 9.1 `config.json`, `issue-watch.json`, `settings.json` (1235-1237); 9.2 `AWR_*`, `CLICKUP_*` (1251-1254); 9.3 run kinds (1265) |
| L7 | yes | 10.1 rows (1284-1285); 10.3 (1305) |
| L8 | yes | 11.1 (1322); 11.2 (1335-1336) |
| L9 | yes | 13.1 E (1423); 13.2 row (1468) |
| L10 | yes | 14.1 (1492-1494); 14.2 (1512-1514); 14.5 C8-6, C8-7, C8-8 (1605-1607) |

No blocking missing link (L3 is a minor presentation gap).

### Chain 4: Dashboard design package (issue 409)

| Link | Present | Location |
|---|---|---|
| L1 | yes | 2.2 row 5.6 (221) |
| L2 | yes | Section 3 `PKG` tree (302-307) |
| L3 | partial | 4.1(d) (368) is prose with a pointer to 5.6; the pipeline sketch is in 5.6 "How It Works" (1043-1049). See M-2 |
| L4 | yes | 5.6 (1027-1106) |
| L5 | yes | 8.1 states "design package = no Orca call" (1147); 8.2 rows (1196, 1205); format row (1215) |
| L6 | yes | 9.1 `requirements.txt` and font path (1239); 9.2 `NO_COLOR` (1250); 9.3 `render.py` flags (1266) |
| L7 | **NO** | Section 10 has no row for the package in 10.1 (1274-1285), 10.2 (1289-1297) or 10.3 (1301-1305). Research GF-5 line 23 records package error behaviour (a slug from the other batch raises `KeyError`; `--width` accepts any int in `--show` mode). Grep for `KeyError` in the document finds only the sweep hit at line 1419. See F-2 |
| L8 | yes | 11.1 (1323); 11.2 (1337); 11.3 (1346) |
| L9 | **NO** | 13.1 has scenarios A-E for sweep, observer and report only; 13.2 has no row for `tests/test_designs.py` or `test_gallery.cjs`; the package appears only in the "Unification touch points" row (1453). See F-2 |
| L10 | yes | 14.4 A SD-21 to SD-29 (1556-1557), 14.4 B U-24 to U-29 (1572), 14.5 C8-9 and the "not raised" paragraph (1610) |

Missing links: L7 and L9.

### Chain 5 (auxiliary, not one of the four named subjects): Orchestrator design

Section 1 lists it as a row of "Key numbers" (line 179) and 4.1(e) diagrams it (370-375), but it has no 2.2 row, no Section 3 entry, no Section 5 subsection (5.5 "Built versus designed" table, lines 979-988, is its only Section 5 home), no Section 9, 10, 11 or 13 row. Present: 2.1 (204), 4.1(e), 8.1 verb tables (1167-1182), 8.2 (1192, 1194-1195), 12.2 (1391), 14.4 A SD-30 to SD-35 (1558), 14.4 B U-34 to U-38 (1570), 14.3 (1528). Graded minor (M-1) because the BUILD-REQUEST names four subjects and the design is explicitly [DESIGNED] with no code.

## Part 2. Section 8 integration points mapped to Section 5 (checklist item 2)

| Section 8 integration (line) | Section 5 home | Result |
|---|---|---|
| 8.1 observer rows (1151-1153) | 5.1 "Allowed argv" table (443-447) | mapped |
| 8.1 sweep rows (1154-1160) | 5.4 Orca allowlist table (799-808) | mapped |
| 8.1 AWR rows (1161-1165) | 5.5 data sources and writes (958-964), `orca_term.py` bullet (977) | mapped |
| 8.1 orchestrator-design verb tables (1167-1182) | none of its own; 5.6 line 1087 points back to 8.1 | no Section 5 subsystem (M-1) |
| 8.2 WC-16 binding (1188) | 5.4 "WC-16 binding" table (841-851) | mapped |
| 8.2 `.dev/sweeps` consumers (1189) | 5.4 Consumers (873-878) | mapped |
| 8.2 observer snapshot consumers (1190) | 5.1 Consumers (515-521) | mapped |
| 8.2 observer and sweep to each other (1191) | 5.6 overlap paragraph (1085); 2.1 (209) | mapped |
| 8.2 orchestrator design to sweep/observer (1192) | 5.5 built-versus-designed (979-988) partly; 5.6 (1087) | partly (M-1) |
| 8.2 AWR to run folders (1193) | 5.5 pipeline table (925-939) | mapped |
| 8.2 entry files (1194) | 5.5 "Living report" (966-977) | mapped |
| 8.2 `orchestrator_repo` route (1195) | 5.5 wording rule (990), Public Interface (998) | mapped |
| 8.2 design package to observer (1196) | 5.6 name parity, design table (1054-1061) | mapped |
| 8.3 Orca, GitHub, ClickUp, git, page server (1221-1225) | 5.1, 5.4, 5.5 | mapped |

Result: every Section 8 row has a Section 5 home except the orchestrator-design verb tables, which are explicitly design-only (minor, M-1).

## Part 3. Section 2.5 "Family at a glance" backing (checklist item 3)

I checked the five subject rows of the matrix (lines 246-249) claim by claim and the overlap table (lines 253-258) row by row against Section 5 and Section 8 tables.

| 2.5 item | Backed by | Result |
|---|---|---|
| Observer data sources, 3 argv shapes, caps (246) | 5.1 allowed-argv and limits tables (443-462); 8.1 (1151-1153) | backed |
| Observer outputs: snapshot 20 of 31, 0600, `$XDG_STATE_HOME`, record `.txt` (246) | 5.1 "Snapshot schema versus code" and "Where it writes" (488-495) | backed |
| Observer R0-R3 built, R4 not (246) | 5.2 release-stage table (598-606) | backed |
| Sweep sources, 12 sections, JSON 12 keys, exit codes (247) | 5.4 (797-837), exit table (827-831) | backed |
| Sweep "6 of 8 classes can print", the five that cannot (247) | 5.3 class table (695-704), limits table (727-735) | backed (the "Rarely" rows for idle and person session are what make it 6) |
| Sweep recorded live runs 180/180 and 263/264 (247) | 10.2 (1293), 11.1 (1321), 14.1 (1486) | backed in Sections 10, 11, 14; not in a Section 5 table (acceptable) |
| AWR sources, outputs, writes (248) | 5.5 pipeline, data-source and writes (925-964); 8.1 (1161-1165) | backed |
| AWR "6 model-judged statuses" (248) | 5.5 status table (943-950) | backed |
| AWR "hook-file join" (248, 257) | 5.5 data-sources "Local" row (962) names the join fields `tabId`, `leafId`; the `<tabId>:<leafId>` key giving `providerSession.id` and `transcriptPath` appears only at line 257 | partly (M-5) |
| AWR "two sanitizer functions" `activity.clean`, `common.safe_title` (248, 258) | grep: both names appear only at line 258 | not backed in Section 5 or 8 (M-5) |
| Package outputs, 180 files per batch, gallery (249) | 5.6 "How It Works" (1043-1049), 8.2 format row (1215) | backed |
| Package "observer shows 3 of 20 designs", name parity, palette (249) | 5.6 design table (1056-1061), parity paragraph (1054) | backed |
| Package "navigation only contract against the sweep's Next inspection text (undecided, issue-409 alignment item 2)" (249) | 5.6 (1085) and 14.3 (1527) cover "alignment items 1-10 undecided"; the specific tension with `Next inspection` text and "item 2" appears only at line 249 | partly (M-5) |
| Overlap table: status vocabularies (255) | 12.2 vocabulary table (1386-1392); 5.3 class table | backed |
| Overlap table: "waits on a person" (256) | 5.2 Decision Desk and questions (572-596); 5.3 rules 1 and 4 (683, 686); 5.5 status table (947) | backed |
| Overlap table: terminal-to-transcript join (257) | 5.3 Joins table (710-717) for the sweep; observer none; AWR partly (see above) | backed except the AWR key detail (M-5) |
| Overlap table: sanitizers (258) | 5.2 key-files row for `sanitize.py` (542); 5.4 "Sanitizer" paragraph (837); 4.3 package canvas row (397); AWR functions not in 5.5 | partly (M-5) |
| C8 pointers (260-263) | 14.5 table (1598-1608) | backed |

## Part 4. Tag coverage: every outside-Section-14 tag matched to Section 14 (checklist item 4)

Method: listed every tag and item id outside Section 14 (lines 1-1472), then looked for each in 14.1 to 14.5. Ranges in 14.4 were expanded and checked for completeness (U-01 to U-40, SD-01 to SD-35, CC-01 to CC-05 all present).

| Tag or id outside 14 (line) | Matching Section 14 entry | Result |
|---|---|---|
| CC-01 (608) | 14.4 A "Observer docs" CC-01 (1550) | matched |
| CC-02 (1195, 5.5 wording rule 990) | 14.4 A CC-02 (1551); 14.5 C8-7 (1606) | matched |
| CC-03 (366) | 14.4 A CC-03 (1552); 14.5 C8-6 (1605) | matched |
| CC-04 (395, 954, 1284) | 14.4 A CC-04 (1553) | matched |
| design DQ13 "Watching" [CODE-CONTRADICTED] (1023) | 14.4 A CC-05 (1554) | matched |
| SD-02 (457), SD-05 (648), SD-14 (311, 1189), SD-21 to SD-25 (227-229), SD-21 to SD-29 (1079), SD-16 (1513) | 14.4 A rows (1539-1558) | matched |
| `rendering-rules.md:3` [STALE DOC] (1054) | SD-25 to SD-29 row (1557) | matched |
| DEFECT-CANDIDATE D-1 / C8-9 (246, 353, 622, 1083, 1491) | 14.5 C8-9 (1608); 14.1 (1491) | matched |
| DEFECT-CANDIDATE C8-8 (990) | 14.5 C8-8 (1607); 14.1 (1494) | matched |
| KNOWN LIMIT C8-1 to C8-7 (262, 731-735, 990) | 14.5 (1600-1606) | matched |
| `DC-02` (382), `DC-01` and `DC-02` (1110, 1297) | not present in Section 14 by id; 14.5 uses C8-8, C8-9, D-1. The ids are defined only in the external `gaps-and-questions.md` rows 100-101 ("see C8-8", "see C8-9") | content matched, id not (M-4) |
| U-01, U-02, U-03, U-05, U-06, U-08, U-11, U-12, U-13, U-14, U-15, U-17, U-24, U-25, U-26, U-27, U-30, U-31, U-32, U-33, U-35, U-40 and untagged [UNVERIFIED] mentions (210, 228, 247, 249, 353, 381, 449, 497, 499, 596, 608, 712-716, 812, 823, 886-888, 1052, 1105, 1235-1236, 1297, 1318, 1332) | 14.4 B (1564-1572) lists U-01 to U-40 with no gap | matched |
| G-04, G-05, G-07, G-08, G-09, G-10, G-22, G-23, G-27, G-48 (469, 490, 596, 614, 1204, 1225, 1529, 1235) | 14.4 C ranges (1578-1585) | matched |
| G-35, G-36, G-37 (366, 1194, 1492, 1605, 1608) | cited inline in 14.1 and 14.5; no 14.4 C row | matched (inline) |
| M-1, M-4, M-7, M-8, M-12, M-14 (3, 406, 323, 900, 911) | 14.4 C "Count corrections" (1584), "Scope" row (1578) | matched |

Result: no tag outside Section 14 lacks a Section 14 entry. Residual: Section 14 never prints G-13, G-38 or G-40 (G-13 and G-38 are "resolved by gap-fill" or a requester step in the register; G-40's content is in 14.2 row `Window.more_text` at line 1504 without the id), although line 1624 says all 134 tracked items are in 14.4 and 14.5 (M-4).

## Part 5. Glossary both directions (checklist item 5)

Glossary terms used in the body (all 15 rows of Section 16, lines 1641-1659):

| Glossary term | Used outside 16 at | Result |
|---|---|---|
| Observer, Sweep, worker-list, Run/Dispatch, Phase 1, Orchestrator, Coordinator, SPEC, C8, KNOWN LIMIT / DEFECT-CANDIDATE | throughout (for example 163, 216-221, 262, 731, 1596) | used |
| WC-16, WC-10, "The sweep." | 845-850 (5.4 table), 1188 | used |
| R0-R3, Decision Desk | 598-606, 594 | used |
| agent-work-report (AWR) | 6 onward (line 1114 defines the abbreviation at first use) | used |
| PR A, B, C, D, P | 163, 898, 985-986, 1087 | used |

Key domain terms used in the body but not defined in Section 16 or at first use:

| Term | Where used | Defined? |
|---|---|---|
| `ccsession` | 198, 247, 257, 358, 383, 819, 870, 964, 1006, 1180, 1202, 1249 | never defined anywhere; central to the sweep's path B join and the AWR wake line |
| `FG-1..14` | 1071 | never defined (only "(R11)") |
| bare `C7` | 1213 | undefined id (research numbering) |
| `ORCH` | first used 1551 (14.4 A); defined 1596 (14.5) | defined after first use, in a later subsection; not in glossary |
| `DESIGN`, `PKG` | defined in section notes (652, 267) and 14.5 (1596) | not in glossary |
| "living report", "entry file", "Needs you", "Safe to close", "Removable" | 163, 896-898, 966 and 5.3 (719-724) | defined in the body where they first matter, no glossary row |

These are minor (M-6): each term is explained or inferable in context except `ccsession` and `FG-1..14`.

## Part 6. Cross-reference resolution table (checklist item 6)

Table of Contents links (lines 138-155), checked against the heading text and GitHub anchor rules:

| ToC link | Heading in document | Resolves |
|---|---|---|
| #1-overview to #7-component-inventory | `## 1. Overview` (161) to `## 7. Component Inventory` (1137) | yes |
| #8-api--integration-points | `## 8. API & Integration Points` (1143) | yes (the `&` drops, leaving a double hyphen) |
| #9-configuration--environment | `## 9. Configuration & Environment` (1229) | yes |
| #10-error-handling--edge-cases | `## 10. Error Handling & Edge Cases` (1270) | yes |
| #11-performance-characteristics, #12-conventions--patterns, #13-extension-guide | lines 1309, 1354, 1411 | yes |
| #14-known-limitations--technical-debt, #15-verification--accuracy, #16-glossary | lines 1474, 1618, 1639 | yes |
| #appendix-a-document-provenance | `### Appendix A: Document Provenance` (1665) | yes |
| #document-history | `## Document History` (1692) | yes |

In-text "Section N", "see N.N" and "in N.N" references (lines 1-1698; research-file references such as "research 06 section 8.3" or "GF-3 section 3" are external and excluded):

| Reference (line) | Target content | Resolves |
|---|---|---|
| "Sections 1, 2 (2.5) and 14", "Section 5" (54) | Overview, 2.5, 14, 5 | yes |
| "See Section 14 for stale statements" (72); "see Section 1 and Section 14" (89) | 14.4 A; 1 and 14 | yes |
| "tabulated in Section 6" (110) | Section 6 tables (1116-1122) | yes |
| "details in Section 14" (260) | 14.5 | yes |
| "pointer in 2.5" (229) | 2.5 line 263 (D-1 pointer) | yes |
| "(artifact list in 4.2)" (313) | 4.2 Data Sources (377-386) | **NO**: 4.2 has no run-folder artifact list (F-1) |
| "see Section 13" (332) | Section 13 | yes |
| "pipeline, run-folder artifacts and gate are in 5.5" (366) | 5.5 pipeline table (925-939) and gate paragraph (953) | yes |
| "render pipeline ... is in 5.6" (368) | 5.6 How It Works (1043-1049) | yes |
| "every verb, binary ... in 8.1; ... in 8.3 and 9.2" (381) | 8.1; 8.3 (1221-1225); 9.2 (1246-1255) | yes |
| "see 5.1, 5.2, 5.3, 5.4 ... sanitizers compared in 2.5" (392) | those subsections; 2.5 sanitizer row (258) | yes |
| "see 5.1" (561) | 5.1 "Where it writes" (495) | yes |
| "Declaring lines ... in 14.5" (622, 990, 1083) | 14.5 table (1598-1608) | yes |
| "settled in 14.4 A (SD-21 to SD-29) and 14.3" (1079) | SD-21 to SD-29 (1556-1557); 14.3 write-back and alignment rows (1523, 1527) | yes |
| "see 2.5, 8.1, 8.2 and 12.2" (1087) | 2.5; 8.1 (1167-1182); 8.2; 12.2 (1384-1392) | yes |
| "defaults, exit codes and rules in 5.2" (1261) | 5.2 command surface (551-561), exit codes (565-570) | yes |
| "(section 10)" (1221) | Section 10 | yes |
| "see 14.1, 14.2 and 14.5" (1297) | 14.1, 14.2, 14.5 | yes |
| "Section 13" (1348) | Section 13 | yes |
| "(13.1 B)" (1399) | 13.1 row B (1420) | yes |
| "in 2.5, 8.1 and 8.2" (1448) | those subsections | yes |
| "(14.5)" (1476, 1658) | R-C8 rule (1589) | yes |
| "Section 2.5; G-52" (1571) | 2.3 wrappers row (228), 2.5 (258) | yes |
| "Impact in 14.1" (1600) | 14.1 rows (1482-1484) | yes |
| "see the assembly notes in the Document History" (1625) | Document History row (1696) | yes |
| 15.2 paths "Sections 12-14", "Section 5", "Section 6", "Section 7", "Section 12" (1631-1635) | those sections | yes |

Result: 1 broken in-text reference (line 313); every ToC link and every other in-text reference resolves.

## Part 7. Test files named in 13.2 versus Section 5 (checklist item 7)

| Test file in 13.2 (line) | Section 5 Key Files or test table | Result |
|---|---|---|
| `tests/sweep/test_classify.py` (1459) | 5.3 Key Files (666) | listed |
| `test_report.py`, `test_cli_contract.py`, `test_probes_allowlist.py`, `test_readonly.py`, `test_git_config_hole.py`, `test_cli_registration.py`, `tests/commands/test_sweep_command.py` (1459-1462) | 5.4 Tests row (786), 5.3 (667) | listed |
| `tests/skills/test_worker_contract.py`, `tests/core/test_how_we_work_routing_table.py` (1462) | 5.4 WC-16 table (848-850) | listed in a table |
| `tests/observe/test_adapter.py` (1463) | 5.1 Key Files row (427) | listed |
| `test_parse.py`, `test_collector.py`, `test_golden_contract.py`, `test_snapshot_schema.py`, `test_export.py` (1464-1465) | 5.1 Key Files row (427) | listed |
| `test_commands.py`, `test_registration.py` (1467) | 5.2 Dependencies (634), Consumers (641) | listed |
| `test_live_screen_pty.py`, `test_keys_spike.py` (1466) | 5.2 Consumers (641) | listed |
| `tests/skills/test_agent_work_report.py` (1468) | 5.5 Key Files (912) | listed |
| `test_render.py` (1465-1466) | prose only: 5.1 Conventions (526) | not in a Key Files or test table |
| `test_session.py` (1466) | prose only: 5.2 notes (406) and Conventions (648) | not in a Key Files or test table |
| `test_view.py` (1466) | grep: appears only at line 1466 | absent from Section 5 |
| `test_height_budget.py` (1466) | grep: appears only at line 1466 | absent from Section 5 |

Four observer test files are not in a Section 5 table (M-3).

## Part 8. Appendix A provenance (checklist item 8)

Every file named in Appendix A (lines 1671-1688) exists in the task directory (checked with `ls`): scope/01-observe.md to 04-dashboard-design.md; research/01 to 06 with the exact names printed; the five `research/gapfill-c1-GF1` to `GF5` files; `gaps-and-questions.md`; `qa/qa-research-consolidated-findings.md`; the seven `synthesis/synth-0N-*.md` files. The header count "11 codebase research files (6 plus 5 gap-fill)" (line 62) matches the 11 research files listed. The Appendix maps each source to the sections it fed; spot checks (GF-1 to 14.5; GF-3 to 8.1; GF-4 to 13.1; GF-5 to 5.6; research 03/04 to 5.3, 5.4 and 14.5) agree with the body. Files the body relies on that the Appendix omits: none found (the body cites only the listed research, gap-fill, register and Gate 1 files plus repo and design-package files, which are outside the task directory). Result: pass. Note the Appendix reads "contradictions C1-C8" (line 1674) while the glossary defines C8 as the brief's rule; the overlap of the label is part of M-6.

## Overall Verdict: FAIL

Two blocking findings (F-1, F-2). Everything else is minor and recorded as notes. No fix was applied (fix authorization false).

## Items Reviewed

| # | Check (lens item) | Result | Evidence |
|---|---|---|---|
| 1 | End-to-end chains for the four subjects | FAIL | Observer and sweep chains complete (Part 1). Agent-work-report complete except a prose-only L3. Design package chain lacks L7 (Section 10) and L9 (Section 13) |
| 2 | Every Section 8 integration maps to a Section 5 subsystem | PASS (note M-1) | Part 2: all rows mapped except design-only orchestrator verb tables |
| 3 | Every 2.5 matrix item backed by a Section 5 or 8 row | PASS (note M-5) | Part 3: three facts live only in 2.5 (lines 249, 257, 258) |
| 4 | Every outside-14 tag matched in Section 14 | PASS (note M-4) | Part 4: all matched by content; `DC-01`, `DC-02` ids and G-13, G-38, G-40 are not printed in Section 14 |
| 5 | Glossary terms used; key terms defined | PASS (note M-6) | Part 5: all 15 glossary terms used; `ccsession`, `FG-1..14`, `C7` undefined |
| 6 | Every "see Section N" and ToC link resolves | FAIL | Part 6: ToC 18 of 18 resolve; one in-text reference (line 313) is broken |
| 7 | 13.2 test files appear in Section 5 | PASS (note M-3) | Part 7: 4 of 24 file names not in a Section 5 table |
| 8 | Appendix lists the files relied on | PASS | Part 8: all named files exist, none omitted |

## Summary
- Checks passed: 6 / 8
- Checks failed: 2
- Critical issues: 0
- Issues fixed in-place: 0 (fix authorization false)

## Issues Found

Numbered findings (ID, severity, location, evidence, required fix). Blocking = CRITICAL or IMPORTANT; minor = MINOR notes that never fail the review.

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| F-1 | IMPORTANT (blocking) | Document line 313, Section 3 state-locations block: `├── runs/<id>/ run folder (artifact list in 4.2)` | Broken cross-reference. Section 4.2 "Data Sources" (lines 377-386) lists inputs (Orca CLI reads, fixtures, sweep disk, "Report state" inputs, package fixture, renderer inputs) and contains no list of run-folder artifacts. The artifact list is in 5.5 (pipeline table, lines 925-939) and 8.2 (run-folder format row, line 1214). Line 366 already points readers to 5.5 for the same list, so the document contradicts itself about where it lives | Change line 313 to "(artifact list in 5.5 and 8.2)" |
| F-2 | IMPORTANT (blocking) | Sections 10 and 13 for the design package (chain 4, L7 and L9); the "Complete" claims at lines 117-118 | The design package is one of the four named subjects but has no error-handling row in 10.1, 10.2 or 10.3 and no extension scenario or test row in 13.1 or 13.2. Research GF-5 (`research/gapfill-c1-GF5-package-pipeline.md` line 23) records facts that belong in Section 10 and are absent from the document: `render.py --show <slug>` with a slug from the other batch raises `KeyError`, and `--width` in `--show` mode is not restricted to 160/116/80 (grep for `KeyError` finds only the sweep hit at line 1419). 5.6 gives only "`--width` is ignored in export mode" (line 1051) and "font path read at import" (1051) | Add a 10.2 row for the package (wrong-batch slug raises `KeyError`; any width accepted with `--show`; missing DejaVu font path read at import is unchecked [UNVERIFIED, U-27]). Add a 13.1 entry F for the package (for example "add a design: add a layout function to `layouts/*.py`, register it in `designs(batch)`, regenerate; `test_designs.py` and `test_gallery.cjs` are the checks") or an explicit statement in 13.1 that the package is a static prototype with no supported extension path, and add the package row (or the same statement) to 13.2. If the owner prefers N/A for the package, the document must say so with a reason, as it does for Sections 6 and 7 |
| M-1 | MINOR | Orchestrator design: lines 179, 370-375, 1167-1182, 1192 | The orchestrator design is a Section 1 "Key numbers" row and has a 4.1(e) diagram and the largest Section 8.1 verb tables, but has no 2.2 row and no Section 5 subsection; 5.6 line 1087 sends the reader to 8.1, 8.2 and 12.2, so Section 5 and Section 8 point at each other. Section 1 line 163 says "Four subjects" | Optional: add one sentence in 2.2 or 5.5 naming where the orchestrator design lives (5.5 built-versus-designed table, 8.1, 8.2, 12.2), or drop the "Orchestrator design" row from the Section 1 table |
| M-2 | MINOR | Lines 366 and 368 (4.1(c), 4.1(d)) | The agent-work-report and design-package data flows in Section 4 are prose pointers with no diagram; the diagrams are in 2.1 and in 5.5 and 5.6 "How It Works" | None required; optionally copy the 5.5 and 5.6 sketches into 4.1 |
| M-3 | MINOR | Line 1466 (13.2 observer view/render/keys row) | `test_view.py` and `test_height_budget.py` appear nowhere in Section 5; `test_render.py` and `test_session.py` appear only in prose (lines 526, 406, 648), not in a Key Files or test table | Add those four names to the 5.2 Consumers "Tests" row (line 641) |
| M-4 | MINOR | Lines 382, 1110, 1297 and Section 14; line 1624 | `DC-01` and `DC-02` are used outside Section 14 but Section 14 prints the same items as C8-8 and C8-9 (D-1); the aliases exist only in the external register (rows 100-101). Line 1624 says all 134 tracked items are in 14.4 and 14.5, yet G-13, G-38 and G-40 are not printed by id (G-40's content is at line 1504 without an id) | Add "(DC-01)" to the C8-8 row and "(DC-02)" to the C8-9 row in 14.5; soften line 1624 to "all unresolved items" or list G-13, G-38, G-40 |
| M-5 | MINOR | Lines 249, 257, 258 | Three 2.5 facts have no Section 5 or 8 row: AWR sanitizer functions `activity.clean` and `common.safe_title`; the hook-file key `<tabId>:<leafId>` giving `providerSession.id` and `transcriptPath`; the tension between the package's "navigation only" contract and the sweep's `Next inspection` text tied to alignment "item 2" | Add one line each to 5.5 (sanitizers, hook-file key) and 5.6 (navigation-only versus `Next inspection`) |
| M-6 | MINOR | Lines 1071, 1213, 1551, 1596, 1674; Section 16 | `ccsession` (12 uses) and `FG-1..14` are never defined; bare `C7` is an undefined id; `ORCH` is used at line 1551 and defined at line 1596; "C1-C8" in the Appendix reuses the label C8 that the glossary defines as the brief's rule; `DESIGN`, `ORCH`, `PKG` and the terms "living report", "Safe to close", "Removable" have no glossary row | Add glossary rows for `ccsession`, `living report`, `Safe to close`, `Removable`, `DESIGN`/`ORCH`/`PKG`; define `FG-1..14` where first used or drop the label; replace `C7` with a section reference |

## Actions Taken

None. Fix authorization was false and the document was not modified.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

The spawn prompt carried no `## Inherited Structural Verdict` section, so this review fell back to standalone behaviour and relied on no rf-qa PASS item.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None. No inherited structural verdict was supplied; every structural item in my lens (cross-references, ToC anchors, test file names, Appendix paths) was checked directly.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Does the run-folder artifact list that line 313 points to actually exist in 4.2? Verified by reading lines 377-386 in full and finding no such list; the list is at 925-939 and 1214. This is F-1.
- Does the design-package chain reach Section 10 and Section 13? Verified by reading 1274-1305 and 1417-1470 and by Grep for `KeyError` (only the sweep hit at 1419), then by Grep of research GF-5 (line 23) for evidence that package error facts exist and were omitted. This is F-2.
- Are the DC-, G- and U- ids used outside Section 14 resolvable in Section 14? Verified by Grep for `DC-0`, `G-13|G-38|G-40|G-35|G-36|G-37` in the document and by reading `gaps-and-questions.md` rows 98-115, which shows DC-01 and DC-02 are aliases of C8-8 and C8-9. This is M-4.
- Self-audit questions: (1) about 150 distinct references, ids and file names were checked against the document, the task directory or the register; no source code was read because this lens covers the document's own cross-references, not code claims (other lenses cover those). (2) Files read: the document (5 reads, all 1698 lines), the task file item, `gaps-and-questions.md` lines 98-115, `BUILD-REQUEST.md` lines 8-17. Grep and `ls` covered research GF-5, synth-07 and the research, scope and synthesis directory listings. (3) This is not a zero-issue review: two blocking findings were found. (4) No web research was performed, so Tavily was not needed.

## Recommendations

- Fix F-1 (one-line edit at line 313) and F-2 (one 10.2 row, one 13.1 entry or explicit N/A statement, one 13.2 row or statement), then re-review only those two items.
- Minor items M-1 to M-6 are notes; they do not need a fix pass.

## Confidence Gate

- **Confidence:** Verified: 8/8 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 8 | Grep: 19 | Glob: 0 | Bash: 2 (both `ls` and `wc -l` only, no mutation)
- Unchecked items: none. Unverifiable items: none.
- Limits of the check: the "Family at a glance" matrix was checked claim by claim at the level of the facts each cell states, not every sub-clause; the document's claims about code (line numbers into source) are out of this lens and were not re-verified here. Tool engagement (29 calls) exceeds the 8 checklist items.

## QA Complete

