# QA Report - Gate 3 Lens: Internal Consistency

**Topic:** Observer, sweep and dashboard technical reference
**Date:** 2026-11-20
**Phase:** lens-internal-consistency
**Fix cycle:** N/A (fix_authorization: false, report only)
**Document:** /home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/techref/OBSERVER-SWEEP-DASHBOARD-TECHNICAL-REFERENCE.md
**Status:** Complete

---

## Overall Verdict: FAIL (2 blocking findings: F-01, F-02; 12 minor notes M-01 to M-12)

L<n> below = line number in the assembled document (1,698 lines, read in full in 8 chunks).

## 1. Repeated-facts table (54 rows)

| # | Fact | Locations (doc line numbers) | Consistent |
|---|------|------------------------------|-----------|
| 1 | Observer: 13 `.py` + `snapshot.schema.json` (158 L), 6,011 L | L175, L216-218 (module lines sum to 6,010 + `__init__`), L608 (13 vs 14 with `fixtures/__init__.py`, explained), L1039 | yes |
| 2 | Observer module line counts (adapter 512, parse 835, collector 361, commands 524, view 1,300) | L216-218, L1584 | yes |
| 3 | Observer fixtures: 19 JSON (10 variants incl. base, 8 golden, `question-cap-100`) | L175, L282 (base + 9), L323, L425, L1343, L1584 | yes |
| 4 | `tests/observe`: 26 `test_*.py` of 36 entries; `test_session.py` 27 tests | L175, L406, L648, L1584 | yes |
| 5 | Observer Orca argv shapes = 3 | L190, L246, L273, L381, L441-447, L1147, L1360 | yes |
| 6 | Forbidden prefixes = 13 (13 named at L451 and L1360) | L451, L1147, L1360 | yes |
| 7 | worker-list calls per cycle 5; 4 + 1 with questions; 500 / 400 rows | L246, L343-345, L433-434, L459, L1330, L1380, L1488 | yes |
| 8 | Poll 15 s, cycle budget 15 s, backoff 15 -> 30 -> 60 s | L460, L1129, L1276, L1329, L1377 | yes |
| 9 | STALE at 45 s on the monotonic clock | L348, L422, L462, L1130, L1303, L1331 | yes |
| 10 | Question window 100 rows, retention 1,000 | L422, L461, L1119, L1331, L1487 | yes |
| 11 | Per call 10 s, 8 MiB, 2 KiB stderr, 2 s kill grace | L343, L458, L1276, L1330 | yes |
| 12 | 31 row attributes read / 20 exported / 11 dropped (7 resource + 2 workspace + 2 stage) | L246, L419, L466, L490, L1052, L1211, L1421, L1490 | yes |
| 13 | Snapshot: schemaVersion 1, closed, 0600, fixed name, replaced each cycle | L193, L246, L424, L495, L1211, L1367 | yes |
| 14 | Observer state dir `$XDG_STATE_HOME/superclaude/observe` else `~/.local/state/...` | L310, L495, L1249 | yes |
| 15 | `QUESTION_GATE_PASSED` / `QUESTION_LINK_PASSED` True at commands.py:67, 70 | L246, L353, L539, L596, L1153, L1262, L1368 | yes |
| 16 | Observer flags = 7 (`Options` seven fields) | L217, L533, L549-559, L625, L1261 | yes |
| 17 | Observer exit codes 0 / 1 / 2 / 129 / 143; gate False exits 1 | L567-570, L1262, L1280 | yes |
| 18 | Release stages R0-R3 built, R4 not established; dates 2026-11-12 / 11-16 / 11-17 | L229, L602-606, L1081, L1651 | yes |
| 19 | Observer PR list #503, #514, #577, #592, #598, #673 | L175, L610-619, L1087 | yes |
| 20 | D-1: `--questions` + `--fixture` refused, exit 2, commands.py:77-78, 183-188, 414 | L246, L353, L568-569, L622, L1083, L1491, L1608 | yes (ids differ, see M-03) |
| 21 | Sweep 9 ordered rules, 8 classes | L218, L289, L658, L681-704, L1375, L1389 | yes |
| 22 | Sweep Orca allowlist 10 templates / 7 verbs / 6 called | L247, L381, L797-808, L1147, L1361, L1420 | yes |
| 23 | Sweep git 4 argv shapes; 2 to 4 calls per worktree | L195-196, L359, L812, L1224, L1334, L1361 | yes |
| 24 | Sweep budget 50 shows / 90 s / 10 s per call | L359, L823, L858, L1332, L1380 | yes |
| 25 | Sweep byte limits 8 MiB, 1 MiB, 256 KiB tail, 512 KiB ledger search | L247, L816-823, L1333 | yes |
| 26 | Sweep report names `<stem>.md`, `-2` to `-99` | L324, L825, L1212, L1283, L1294, L1333, L1379 | yes |
| 27 | Sweep report 12 sections; JSON v1 12 top-level keys | L219, L247, L290, L833-835, L1212-1213 | yes |
| 28 | Sweep exit codes 0 / 1 / 2 | L247, L827-831, L1283 | yes |
| 29 | WC-16 at WORKER-CONTRACT.md:287-289; WC-10 :46, :157; never-as-worker :23; "The sweep." :110 | L219, L293, L785, L845-848, L1188, L1645-1647 | yes |
| 30 | `.gitignore:255-256` for `.dev/sweeps/` | L247, L311, L785, L1189, L1240, L1545 | yes |
| 31 | DESIGN line cites for stalled / fenced (493, 636, 841, 877) | L262, L731 (stalled), L732 (fenced: 493, 841 only), L1600, L1601 | NO, minor (M-02) |
| 32 | DESIGN line cites for `agent_wait_since` (493, 494, 649, 1003) | L262, L733 (omits 649), L1602 | NO, minor (M-02) |
| 33 | ORCH line cites for the entry writer (3, 510, 791, 1020, 1021, 1041) | L262 (omits 1021), L1605 | NO, minor (M-02) |
| 34 | Live sweep outcomes 180 of 180 (2026-11-12); 263 of 264 (issue #590) | L247, L1293, L1321, L1486 | yes |
| 35 | `CHECKED_ORCA_VERSION = "1.4.245"`, `JOIN_PATH = "B"` | L239, L713, L1264 | yes |
| 36 | AWR: 16 scripts, 15 steps, 7 templates | L177, L296-299, L898, L904, L1193 | yes |
| 37 | AWR scripts 5,777 L; 5,971 with SKILL.md (194 L) | L177, L220, L900, L904, L1584 | yes |
| 38 | AWR tests 4,005 L / 142 defs | L177, L912, L1468 | yes |
| 39 | `config.json` 14 keys (14 named at L1235); lock budget daily 120 / hourly 10 | L384, L911, L954, L1235, L1322 | yes |
| 40 | AWR gate: 7 checks + sha256 chain; run.py:204-368; `close` weaker (CC-04) | L395, L954, L1193, L1284, L1382, L1553 | yes |
| 41 | AWR six session statuses | L248, L941-950, L1390 | yes |
| 42 | AWR page server 127.0.0.1:8765 | L199, L964, L1013, L1204, L1225, L1514 | yes |
| 43 | PR chain: design #681, D #682, closeout #683, C #684 merged; A #686, P #690 open; B none | L179, L898, L984-986, L1087, L1656 | yes |
| 44 | Package 406 files, 20 designs, 360 exports, 18 scenarios + base (405 flagged as stale at L1557) | L178, L1031, L1045, L1323, L1346, L1557 | yes |
| 45 | Package 180 exports per batch; 570 gallery frame pairs | L249, L1337 | yes |
| 46 | Package 19 `unittest` + 1 Node test, results not run | L178, L249, L1037, L1572 | yes |
| 47 | Observer / package share 8 palette colours | L227, L1054, L1196 | yes |
| 48 | Observer fixtures sharing names with the package: "9 of 9" vs "all 10" | L249 ("9 of 9 fixture names ... 0 of 10 fixture contents") vs L1054, L1196, L1453 ("all 10 / all ten") | NO, minor (M-01) |
| 49 | Observer implements 3 of 20 designs (views A, B, C) | L249, L1029, L1061, L1104, L1196 | yes |
| 50 | PR #503 = 545 files, #673 = 2,831 files | L178, L614, L619, L1029, L1580 | yes |
| 51 | Orchestrator FR-9: 8 states | L255, L1391, L1570 | yes |
| 52 | Sweep: 6 of 8 classes can print; stalled and fenced cannot | L247, L698-704, L1482 | yes |
| 53 | Count of subjects: "Four subjects" vs "Three live + Two designed only" | L52, L64, L163 vs L174-180 (five table rows) | NO, minor (M-05) |
| 54 | Overlap counts: 3 meanings of "waits on a person", 2 joins, 4 sanitizers, 3 Orca wrappers | L228, L246-258, L1585 | yes |

## 2. Items Reviewed (lens checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Repeated-facts table of at least 40 rows, every occurrence compared | PASS | 54 rows above, read from the document in 8 chunks; 4 rows differ (31-33, 48, 53), all minor |
| 2 | Key numbers in Section 1 agree with the rest | PASS | L173-179 against L216-221, L296-299, L610-619, L900, L1031, L1087: files, lines, tests, PR lists all agree (rows 1-4, 19, 36-38, 43-44, 50) |
| 3 | Section 2.2 subsystem map matches 5.x | PASS | L214-221 rows 5.1-5.6 against headings L410, L531, L656, L772, L896, L1027; file line counts equal those in 5.x (L664-665, L780-782, L900-911) |
| 4 | 2.5 matrix and overlaps table agree with Sections 5, 8 and 14 | PASS with notes | L246-258 against 5.1-5.6, L1147-1215, L1482-1494; sanitizer, join, vocabulary and "waits on a person" facts agree; minor items M-01, M-02 |
| 5 | Section 8 Orca verb inventory vs 5.x and Section 4 diagrams | PASS | 8.1 L1151-1165 against L441-447, L797-808, L1161-1165 (AWR verbs) and 4.1 (a), (b), (e) L340-375: same argv, same counts (3 / 10 / 7 / 6 called) |
| 6 | Section 9 settings vs Section 5 and Section 11 | PASS | 9.1-9.3 L1233-1266 against 5.2 L549-569, 5.4 L856, 5.5 L954, 11.2 L1329-1336; values (window, budgets, gates, lock budgets) agree |
| 7 | Live-versus-designed labels agree | PASS | observer, sweep, AWR daily pipeline = built; writer, orchestrator, `/sc:orchestrator` = designed; package = prototype: L163, L190-206, L246-249, L366, L984-988, L1194, L1492, L1653 |
| 8 | C8 candidates labelled identically in Sections 2, 5, 14 | PASS with notes | KNOWN LIMIT (cited) for C8-1 to C8-7 and DEFECT-CANDIDATE for C8-8, C8-9 in every section (L262-263, L731-735, L990, L1482-1494, L1600-1608); only id aliases and "(cited)" abbreviation differ (M-03, M-04) |
| 9 | Words "remediation task not created (read-only brief); flagged for the owner" wherever no cited on-record decision exists | FAIL | F-01: missing at L1491, L1494 (14.1 DEFECT-CANDIDATE rows), L1603, L1604 (14.5 C8-4, C8-5; rule 4 at L1594 requires them), and L1606 (C8-7; GF-1 prints them) while 5.3 L734-735 prints them for the same two limits |
| 10 | Cross-references resolve and say what is claimed | FAIL | F-02: L1399 "(13.1 B)" points at a sweep-only procedure; all other references checked resolve (L229, L366, L368, L381, L392, L622, L990, L1079, L1083, L1087, L1261, L1297, L1348, L1448) |
| 11 | Table of Contents matches headers | PASS | ToC L138-155 vs headers L161, L183, L269, L336, L402, L1112, L1137, L1143, L1229, L1270, L1309, L1354, L1411, L1474, L1618, L1639, L1665, L1692; anchors follow the GitHub slug rule |
| 12 | Completeness Status checklist matches actual state | PASS with notes | L105-122: sections 6 and 7 N/A as stated (Section 6 does hold a runtime-state table, as L110 says); "links verified" and "QA review" left open, true at this point; minor M-06, M-09 |
| 13 | No unresolved `[CONTRADICTION: ...]` marker | PASS | Grep for CONTRADICTION, TBD, TODO, FIXME, placeholder tokens returned only `[[` in a code signature (L742); the one prose "Contradiction" (L497) states its resolution |
| 14 | No contradiction inside the document | PASS with notes | no two sections give different values for one fact except the minor items below; F-01 and F-02 are blocking |

## 3. Findings

### Blocking

**F-01 (IMPORTANT, blocking). Required C8 wording missing where no cited scope decision exists, and 14.5 contradicts its own rule 4 and Section 5.3.**
- Locations: rule 4 at L1594 says "Remediation task not created (read-only brief); flagged for the owner" is printed on every DEFECT-CANDIDATE and on every KNOWN LIMIT whose cited text names no tracked owner for its "until" condition.
  - 14.5 L1603 (C8-4 Safe to close) ends "Flagged for the owner" only; L1604 (C8-5 Removable) ends "No later work named. Flagged for the owner" only; L1606 (C8-7) ends "Flagged for the owner" only.
  - 14.1 L1491 (D-1, DEFECT-CANDIDATE) and L1494 (C8-8, DEFECT-CANDIDATE) say only "Flagged for the owner" in the Planned Fix column.
- Evidence: the same two limits in Section 5.3 carry the full words (L734 "remediation task not created (read-only brief); flagged for the owner", L735 "Remediation task not created ... flagged for the owner"). The authority file GF-1 prints the full words for C8-4, C8-5 and C8-7 (gapfill file lines under "### C8-4", "### C8-5", "### C8-7" in `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/gaps-and-questions.md` L201, L210, L228, and the register rows DC-01 L100 and DC-02 L101 for the two defect candidates). C8-5 states "No later work named" at L1604, so by rule 4 it has no tracked owner and needs the words.
- Required fix: in 14.5 rows C8-4, C8-5, C8-7 and in 14.1 rows L1491 and L1494, replace "Flagged for the owner" by "Remediation task not created (read-only brief); flagged for the owner" (the exact wording used at L1600-1602, L1605, L1607, L1608).

**F-02 (IMPORTANT, blocking). Broken cross-reference: 12.3 points to a section that does not cover the claim.**
- Location: L1399 (12.3 anti-pattern "Adding an Orca argv outside the allowlist, or `--ack` / `--wait` / `--peek` to the observer", fix column "Add a template deliberately with its tests (13.1 B); never shrink the forbidden set").
- Evidence: 13.1 B (L1420) is "Add a sweep probe or allowlist entry" (sweep `ALLOWED_ORCA`, `ALLOWED_GIT`); it has no observer step and does not mention the observer forbidden set. The observer procedure is in 5.1 Conventions (L524) and no 13.1 row covers it (rows A to E at L1419-1423: sweep rule, sweep probe, snapshot field, observer view/key, AWR source).
- Required fix: change the reference to "5.1 Conventions (observer argv) and 13.1 B (sweep)" or add the observer argv steps to 13.1.

### Minor (notes only; not rechecked in later rounds)

- **M-01.** L249 says the observer "inherits 9 of 9 fixture names ... 0 of 10 fixture contents"; L1054, L1196 and L1453 say all 10 (9 variants plus base) share names. Use "10 of 10 names" in L249.
- **M-02.** Line-cite lists for the same C8 evidence differ: L732 (fenced) lists DESIGN 493, 841 while L262 and L1601 list 493, 636, 841, 877; L733 omits DESIGN:649 that L262 and L1602 list; L262 omits ORCH:1021 that L1605 lists. Subsets, no contradiction.
- **M-03.** Three ids for the same candidates: D-1 / C8-9 / DC-02 and C8-8 / DC-01. DC-01 and DC-02 appear only at L382, L1110, L1297 (and are defined only in the register rows DC-01, DC-02), never in Section 14, although L1476 says DC- ids are register ids. Add a one-line crosswalk in 14.5.
- **M-04.** The label "KNOWN LIMIT" appears without "(cited)" at L366, L990 (C8-7), L1194, L1195, L1482, where L1600-1606 and L262 print "KNOWN LIMIT (cited)". Abbreviation only; same label.
- **M-05.** "Four subjects" (L52, L64, L163) against "Three are live ... Two are designed only" (L163) and a five-row Section 1 table (L174-180, which adds the orchestrator design). Say "four subjects plus the orchestrator design as context".
- **M-06.** L1624 says all 134 tracked items are in 14.4 and 14.5; register ids G-13, G-38 and G-40 are not printed anywhere in the document (G-13 and G-40 substance is at L1542 and L1504; G-38 "public wording corrections not made" has no counterpart).
- **M-07.** "A / B / C" means two things: question-panel layouts A, B, C (L588-592, L1422) and observer views A, B, C for Signal Bridge, Attention Ledger, Decision Desk (L249, L1058-1060, L1491). Different nouns are used, so no contradiction, but a reader can conflate them.
- **M-08.** L1533 says nine "STALE DOC rows" are also CODE-CONTRADICTED (SD-01, 06, 07, 21-24, 26, 27) while the table tags SD-01, 06, 07, 21-24 CODE-CONTRADICTED (L1539-1556) and SD-25 to SD-29 STALE DOC (L1557).
- **M-09.** L89 points to "Section 1 and Section 14" for "Active Development / Stable by subject"; neither section uses those words (Grep: only L89 and an unrelated L823).
- **M-10.** 5.1 says the observer allow-list is not applied to the `skills list --json` probe (L512) while the allowed-argv table (L445) and 8.1 L1151 say it is "allowed by exact match". Both can be true (the template is in the allowed set but `_find_orca` builds its own argv); one sentence would remove the doubt.
- **M-11.** 15.2 items 3 and 4 (L1633-1634) say there is no client-state section, yet Section 6 (L1112-1133) documents `Session` and `CycleResult`.
- **M-12.** PR #682 is "plan-gate retirement" at L984 and "plan-approval retirement" at L1656 (wording only).

## 4. Self-audit

- Checks that found nothing were still verified by reading all 1,698 lines and comparing every occurrence in the table above; the two blocking findings were each confirmed against the authority file (gaps-and-questions.md C8 blocks and register rows) and by Grep counts of the required words (the full phrase appears at L260, L622, L731-735, L990, L1083, L1594, L1600-1602, L1605, L1607, L1608, L1610; only the short form at L1491, L1494, L1603, L1604, L1606).
- Code facts were not re-verified (out of lens); the only code reads were `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/cli/observe/parse.py` L745-835 and `commands.py` L464-478 to check one doubt (fixture loading), which produced no finding.

## 5. Summary

- Checks passed: 12 / 14 (items 4, 8, 12, 14 passed with minor notes only)
- Checks failed: 2 (item 9 -> F-01, item 10 -> F-02)
- Critical issues: 0; blocking (IMPORTANT) issues: 2; minor notes: 12
- Issues fixed in-place: 0 (fix_authorization: false; the document was not modified)

## 6. Recommendations

- Fix F-01 (restore the full required words in 14.5 C8-4, C8-5, C8-7 and 14.1 L1491, L1494) and F-02 (re-point the L1399 cross-reference), then re-review only those two items.
- Minor notes M-01 to M-12 need no fix pass; M-03 (id crosswalk) and M-01 are the cheapest to correct while editing.

## 7. Confidence Gate

- **Confidence:** Verified: 14/14 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 15 | Grep: 20 | Glob: 0 | Bash: 1 (Read + Grep + Glob = 35, at least the 14 checklist items)
- Unchecked items: none. Unverifiable items: none.
- Limits: code behaviour was out of lens and was not re-verified; the document was compared with itself and with the register `gaps-and-questions.md` only where a finding needed an authority.

## QA Complete
