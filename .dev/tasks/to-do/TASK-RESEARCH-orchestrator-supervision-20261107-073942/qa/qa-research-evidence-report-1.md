# QA Report -- Research Gate (Partition 1 of 2)

**Topic:** Orchestrator mode Phase 1 (issue #339): read-only `/sc:sweep` and coordinator-loop rules
**Date:** 2026-11-07
**Phase:** research-gate
**Fix cycle:** N/A
**Fix authorization:** false (no research file edited)
**Assigned files:** `research/scope-01-contract.md`, `research/scope-02-orca-recovery.md`, `research/05-orca-row-schema.md`
**Checklist items applied:** 1 (file inventory), 2 (evidence density), 3 (scope coverage), 4 (documentation cross-validation)

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

Research-file checksums at start (md5): scope-01 `5b7ed79ec06aabec2fc0b92712e5a38e`, scope-02 `409347852d9deffce43d0638421f3441`, 05 `33cdc5ebf1fa63990af7a49e9f898a9d`.

---

## Verification log

(Filled in section by section below.)

### File 1: `research/scope-01-contract.md` (152 lines)

**Item 1 (inventory):** `**Status:** Complete` at line 2; `## Summary` at line 150. PASS.

**Item 2 / item 4 (evidence and every CODE-VERIFIED claim), checked by Read of every cited source:**

| Claim group (scope-01 line) | Source re-read | Result |
|---|---|---|
| Section headings and term/rule lines (30-48): headings 9, 26, 48, 64, 68, 77, 91, 101, 110, 120, 131, 154, 158, 166; terms 11-24; intro 66; brief contents 79-89; guard 95-97; 103-108; 160-164; template 170-179; slot rules 181-186; flag table 188-203 | `WORKER-CONTRACT.md:1-203` (Read whole file) plus `awk` line dump of 7, 11-24, 66, 79, 89, 95-97, 103, 126, 127, 134, 160, 164, 170, 179, 181, 186, 188, 190, 203 | Hold. Flag table has exactly 12 command rows (grep count 12 between 188-203). |
| Rule IDs WC-2..WC-13, no WC-1 / WC-14+ (50, 143) | `grep -nE 'WC-1\b|WC-1[4-9]'` | No match: holds. |
| Decision lines D1 :12, D2 :56,:131, D3 :23, D4 :40, D5 :129 (50) | Contract Read | Hold. Omits D3 also at :115 and D4 also at :84, :184 (MINOR, see issue 6). |
| 15 quoted rules (56-70): :11, :20, :23, :39, :40, :43, :45, :54-57, :60, :61, :70, :73, :74, :105, :107, :108, :112, :114, :117, :122-129, :133-136, :156 | Contract Read | Every quote is verbatim at the cited line. |
| Gap table G1-G7 insertion points and triggers (78-86): :46, :57, :126, :127, :129, :131, :134, :156, :158 | Contract Read + line dump | Hold (:126 "reports the failure to the person", :127 guard refusal, :134 frozen plan). |
| Absence grep for poll/re-arm/cron/sweep/expir (74) | Same grep over both files | Only `WORKER-CONTRACT.md:45` matches: holds. No `sweep`/`close` command file exists. |
| `install_core.py:27` (26) | `sed -n 26,28p` | `"WORKER-CONTRACT.md",` at 27: holds. |
| Test anchors (92-102): :19, :20, :22, :25-237, :86-92, :125-128, :163, :164-172, :181-190, :207-213, :227-228, :239-243, :245-254 (8 entries), :381, :384-385, :388-395, :398-404, :413-421, :446, :540-542, :545 ("all seven"), :581-584, :587-594, :597-621 (16 ungated lines), :624-633, :1090-1094, :1098, :1166, last test :2249, EOF :2265, 41 `def test_` | Read `test_worker_contract.py` 17-256, 379-448, 536-635, 1086-1101, 2190-2204; `grep -c '^def test_'` = 41; `wc -l` = 2265 | All hold. `WRITE_VERB_CLASSIFICATION` closes at :2196 (scope says "~2198"; approximate, true). |
| Copies table (108-119): plugin byte copy, `test_routing_plugin_parity.py:38`, `core/CLAUDE.md:45,65,82`, `HOW-WE-WORK.md:11,28,318,337,396-405,403,405`, `test_claude_md_routing_block.py:28-32`, `test_orca_session_launch_guidance.py:10-31,14-16`, `test_how_we_work_routing_table.py:27-40,56-97,213-217,291-311,342-347` (1202 lines), `test_help_command.py:32-33,41`, root `CLAUDE.md:164-165` | `cmp` (identical, exit 0); `wc -l`; Read of each test range; `sed` of CLAUDE.md and HOW-WE-WORK lines | All hold. |
| No test names "Orca coordination" (102) | `grep -rln 'Orca coordination' tests/` | No hit: holds. |
| CODE-CONTRADICTED cross-refs (100, 111, 127-138): `issue-summary.md:18` is the HOW-WE-WORK row; `analyze-worker-contract.md` is 72 lines, F1-F14 at :32-45, S1-S5 at :51-55, :46 blank, :54 is S4, :14 plugin copy note, #409 only at :23 and :60, F9 at :40, F11 at :42, F12 at :43, F14 at :45, S1 :51, S2 :52, S3 :53, Phase 3 :62, capabilities cited :120-131 at :16 and :125-126 at :34 | Read both files in full | Every relocation holds. The 12 CODE-CONTRADICTED tags are accurate and none contradicts a contract rule. |
| Tag counts in Summary (152): 54 / 12 / 4 | `grep -o '\[TAG[^]]*\]' \| wc -l` | 55 / 13 / 5 raw, each including the one mention inside the Summary sentence itself, so 54 / 12 / 4: holds. |

**Item 3 (scope coverage):** S1 key files examined: contract, HOW-WE-WORK and plugin copy, core `CLAUDE.md`, `install_core.py`, all five test files, issue summary, analysis. Not examined: `.dev/orca-command-refactor/decisions/APPROVED.md` (EXISTING_FILES lists it; scope-01:50 leaves the decision texts UNVERIFIED with "no `D1`..`D5` heading found by grep there"). QA grep shows D1-D5 are table rows at `APPROVED.md:8-12`, so the texts were one Read away. `grep -rln APPROVED.md research/` finds only scope-01 and research-notes, so no other research file covers it (issue 5).

**Item 4 (tagging):** Every doc-sourced claim carries a tag. Four places keep stale "not read / UNVERIFIED" prose beside a later [CODE-VERIFIED] re-check of the same thing (lines 99, 118, 119, 146): wording only (issue 7).

**Evidence density for scope-01:** Dense (every claim carries a file:line; every cited line checked holds).

### File 2: `research/scope-02-orca-recovery.md` (236 lines)

**Item 1 (inventory):** `**Status:** Complete` at line 3; `## Summary` at line 227. PASS.

**Item 2 / item 4, checked by re-reading every cited source (awk line dumps with line numbers, live `--help` only):**

| Claim group (scope-02 line) | Source re-read | Result |
|---|---|---|
| Version 1.4.245, inventory written against 1.4.237 (9) | `orca-ide --version`; `orca-capabilities.md:8` | Hold. |
| Line counts table (13-32) | `wc -l` of all 8 repo files + captures | Hold (157, 171, 222, 169, 170, 128, 1975, 203, 56, 188, 212, 219, 219, 47). |
| Command-name CODE-CONTRADICTED note (16, 229) | `orca-ide orchestration worker-list --help` prints usage `orca orchestration worker-list` | Consistent; top-level "Unknown command" not re-run. |
| worker-list envelope (40-49) | `lc01-step7.txt:22-47` dump | `workers: []` :28, `counts` :29-31, `page` :32-37, `scope` :38-41, `_meta.runtimeId` :43-45: hold. |
| worker-list help lines 3, 10-11, 19, 20, 21, 22 (45-48, 91, 95, 113-115) | `orca-ide orchestration worker-list --help \| cat -n` (22 lines) | Every quoted line is at the cited number. |
| worker-show help line 16 (70, 88); worker-read line 20 (117); status line 14 (112) | live `--help \| cat -n` | Hold. |
| Per-worker field table (53-72) against lc16/lc17/lc01 | dumps of lc16 :4-212, lc17 :127-193, lc01 :127-193 | Every range holds: stage :128-133, outcome :134, liveness :135-139, evidence :140-144, resource :145-151 (`state` :146), nextAction lc16 :152-155 / lc17 :153, attention lc16 :156-159 / lc17 :162-165, terminal :167-175, agentWait :180, :185, observation :183-184, retainedReason :191, block :187. |
| `activity` "working" after settlement (74) | lc17 :132, lc01 :132 | Hold (`detail` "settled" at :131 in both). |
| Enum tally and "none found" list (76, 203-211) | grep tally over `lc*-show-*.json`; artifacts grep (batch run before this section) | Hold. |
| orca-capabilities citations (36, 64, 82-94, 109, 112, 115, 116, 219) | Read whole `orca-capabilities.md` | :36, :39, :111-114, :122-130, :127 (quoting `[G]` 136-142), :128, :149, :151, :184 all say what is claimed. |
| orchestration SKILL.md :37-39, :46-47, :64-66 (110, 111, 118) | dump | Hold. |
| sc-crash-recovery SKILL.md :4 (both script paths incl. `~/workspace/IronClaude/...`), :13, :25-27, :31-37, :53, :75-81, :91, :93-97, :134, :137, :139-150, :155 (124-133) | dump of every cited line | Hold. `Bash(git stash *)` is in :4, so the CODE-CONTRADICTED read-only note holds. |
| investigators.md :9-41, :47-70, :76-95, :101-126, :115, :132-151, :171 (129) | boundary dump | Hold. |
| report-template.md :71-118, :120-125, :127-129; pipelines.md :19, :52-68, :102-116, :161-168, :177-201 (130-133, 184-189) | dump | Hold. |
| bootstrap_scan.sh :21-24, :31, :65-69, :73, :82, :136, :143-169 (137-143) | dump | Hold. The 18 output keys at :145-162 match the list. |
| parse_session_log.py :21-29, :31-40, :45-55, :81-84, :85-102, :91, :111-119 (147-150) | dump | Hold (error JSON printed to stdout at :28; prefix drop only for `role == "user"` at :81). |
| ccsession :144, :162-165, :175-222, :224, :285-287, :344-361 (`%25`/`%2F`/`%2E` at :346-358), :453-455, :524, :558-605, :564, :566-572, :590, :1297-1327, :1301-1302, :1324, :1408-1411, :1482-1581, :1524-1548, :1566, :1572, :1577-1579, :1787-1788, :1792-1797, :1920-1927 (155-160) | dump + grep | Hold. `list_sessions` range is given as :1482-1580 in prose and :1482-1581 in the tag (citation nit, issue 11). |
| WORKER-CONTRACT.md :14, :15, :30-38, :52-58, :161 (166-174) | Read earlier in this session (File 1) | Hold. |
| Five command files `worker_status: failed` (174) | `grep -n worker_status` | brainstorm.md:155, test.md:104, business-panel.md:100, explain.md:104, adversarial.md:160: hold. |
| return-contract.md :3-19, :33, :45-56, :49 (178-179) | dump of :1-56 | Hold (:49 has no `blocked`). |
| sc-brainstorm-protocol :385, sc-graph-protocol :112, sc-impact-protocol :100 (180) | dump | Hold. |
| Summary counts (235): "Contradicted: 8", "Unverified: 30 lines" | `grep -o` counts: 11 / 32 raw | Hold once the legend line 7 and the Summary line itself are excluded. |

**Errors found in scope-02:**

- Summary line 234 swaps the bootstrap_scan.sh citations: it gives "`.git` is a file, :31, :73" and "encodes paths differently ... (:136)". The dump shows the encoding is at :31, the `.git` test at :73, and :136 is the hand-built JSON array (escaping), as the body says at lines 140-142 (issue 2).
- Line 140 says Claude Code's every-non-alphanumeric encoding is "confirmed by this session's own log dir `-home-coder-workspaces-worktrees-IronClaude-issue-339-orchestrator-mode`". That path contains no `.` or `_`, so it cannot confirm the `.`/`_` difference the bug rests on. The claim itself holds (ccsession:1301-1302 comment) (issue 3).

**Item 3 (scope coverage):** S2 data-source rows in research-notes EXISTING_FILES (`research-notes.md:48-67`, plus `orchestration/SKILL.md` :45 and `orca-ide` :46) are all examined by scope-02, except `src/superclaude/skills/ccsession-tag/README.md` (766 lines, row :59), which no research file read. scope-02 took the same facts from the ccsession source, and README:359 only restates the `orca-tabs` path from ccsession:564, so nothing is lost (issue 10).

**Item 4 (tagging):** Every doc-sourced claim carries a tag; every table row has a Tag column or a block tag. Every [CODE-VERIFIED] claim checked above holds.

**Evidence density for scope-02:** Dense.

### File 3: `research/05-orca-row-schema.md` (201 lines)

**Item 1 (inventory):** `**Status:** Complete` at line 5; `## Summary` at line 199. PASS.

**Item 2 / item 4, checked against live help and the captures:**

| Claim group (05 line) | Source re-read | Result |
|---|---|---|
| `[H:worker-list]` 22 lines; lines 3, 5, 13-16, 19, 20, 21, 22 (14-22) | live `--help \| cat -n` | Hold. Help names no row field, `projection`, `liveness`, `attention` or `agentWait`: holds. |
| `[H:worker-show]` 16 lines; lines 3, 5, 15, 16 (24-29) | live `--help \| cat -n` | Hold. |
| Inventory citations `orca-capabilities.md:8, :10-21, :12, :113, :122-130, :97-102` (40-51, 71, 194-197) | Read whole inventory | Hold. |
| STALE DOC: inventory has no `page.hasMore` and no `scope.source` (195, 196) | `grep -n 'scope.source\|hasMore\|bound Run'` on the inventory | NO_MATCH: holds. |
| lc16 block ranges (120): dispatch :5-30, worker :31-108, projection :109-160, terminal :161-181, observation :182-186, terminalResource :187-207; runtime id :210 (116) | dump | Hold. |
| 16 projection fields (122, 148) | awk of the top-level keys at :110-156 | 16 keys: holds. All quoted values at :128-159 hold. |
| `agentWait` only at lc16 :180, :185 (124); lastHeartbeatAt :29, lastOutputAt :174, preview :175 (126) | dump | Hold. |
| lc17 :128-136, :150, :152-160, :161-166, :182, :187, :190, :192 (130-133) | dump | Hold. |
| lc01-show :128-136, :150, :153-159, :161-166, :187, :192 (137-138) | dump | Hold. |
| lc01-step7 :23-47, :28, :29-31, :32-37, :33, :35, :38-41 (142-144, 163, 186-187) | dump | Hold. |
| `--pairing-code` / `--environment` "(`[H:worker-list]` 3, 9-14)" (163) | live help | They are at :10-11, not in usage line 3; inside the cited range, so a citation nit (issue 11). |
| `[G]`, `[G:recovery]`, `[CLI]` line numbers and the 215 / 289 output-line counts (59-108, 157-161, 165, 174, 194, 197) | not re-run: this gate allows `--help` text and captures only | UNVERIFIABLE by QA. 05 tags these UNVERIFIED (or STALE DOC), which is correct; see issue 8. |

**Errors found in 05:**

- Lines 43, 44, 45, 46 and 48 restate guide-sourced claims from the inventory (`orca-capabilities.md:123-126, :128`: fleet vs PTY layers, outranking, the `unverifiable` reasons, stall proof, remote `unverifiable`) with no tag. The neighbouring lines 42, 47, 49, 51 are tagged, and the same content is tagged UNVERIFIED later in Source 3b, but these five lines are untagged doc claims (issue 1).
- Line 70 tags a guide claim (`worker-list ... --terminal-state reclaimable` enumerates terminals owing a release decision) `[CODE-VERIFIED: flags exist in [H:worker-list] line 3]`; the evidence proves only that the flags exist, not the purpose (issue 4).

**Item 3 (scope coverage):** 05's EXISTING_FILES targets (the inventory, both help texts, the four captures) are all examined. PASS.

**Item 4 (tagging):** Fails on lines 43-46 and 48 (issue 1). Every [CODE-VERIFIED] claim (all help-text or capture based) was checked and holds.

**Evidence density for 05:** Dense for help and capture claims; the guide-derived part (Sources 3, 3b, 3c) is tagged UNVERIFIED and could not be re-checked under this gate.

**Cross-file within this partition (scope-02 vs 05):** scope-02:9 says `orca skills get` was not run under its brief, and scope-02:82-86 still cite the inventory's `[G]` 58-60 and 143-145 line numbers; 05:194 says those numbers moved in the current 215-line guide (for example 58-60 -> 59-61). Both files tag the guide claims UNVERIFIED, so no fact conflicts, but synthesis gets two line-number bases for the same guide text (issue 8).

---

## Items Reviewed

| # | Check | scope-01 | scope-02 | 05 | Evidence |
|---|-------|----------|----------|----|----------|
| 1 | File inventory | PASS | PASS | PASS | Status Complete at scope-01:2, scope-02:3, 05:5; Summary at :150, :227, :199 (Read). |
| 2 | Evidence density | PASS (Dense) | PASS (Dense) | PASS (Dense) | Every cited source re-read by Read or numbered awk dump; tables above. Line nits are MINOR. |
| 3 | Scope coverage | PASS (gap noted) | PASS (gap noted) | PASS | research-notes.md:15-84 EXISTING_FILES checked row by row; APPROVED.md and ccsession-tag README unread (MINOR, issues 5 and 10). |
| 4 | Documentation cross-validation | PASS | PASS | **FAIL** | Untagged doc claims at 05:43-46, :48 (issue 1); every [CODE-VERIFIED] claim re-checked and holds. |

## Summary

- Checks passed: 11 / 12 (4 checks x 3 files)
- Checks failed: 1 (item 4 on `05-orca-row-schema.md`)
- Critical issues: 0
- Important (blocking) issues: 1
- Minor issues (notes): 10
- Issues fixed in-place: 0 (fix authorization false)
- No fabricated path, line or quote was found; every [CODE-VERIFIED] claim that QA could check holds.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | `05-orca-row-schema.md` lines 43, 44, 45, 46, 48 (Source 2) | Doc-sourced claims (guide text via `orca-capabilities.md:123-126, :128`) carry no tag; item 4 says any untagged doc claim fails. | Add `[UNVERIFIED: guide text via orca-capabilities.md:<line>]` to each of the five lines (or CODE-VERIFIED with a capture citation where one exists). |
| 2 | MINOR | `scope-02-orca-recovery.md` line 234 (Summary) | bootstrap_scan.sh citations swapped: `.git` paired with :31, :73 and encoding with :136. | Change to "encoding :31; `.git` test :73; unescaped JSON :136", matching body lines 140-142. |
| 3 | MINOR | `scope-02-orca-recovery.md` line 140 | The "confirmed by this session's log dir" evidence contains no `.` or `_`, so it cannot confirm the encoding difference. | Cite a log dir whose path has `.` or `_`, or drop the clause and keep ccsession:1301-1302. |
| 4 | MINOR | `05-orca-row-schema.md` line 70 | `[CODE-VERIFIED]` covers only flag existence, not the guide's purpose claim it is attached to. | Split: `[CODE-VERIFIED: flags exist, [H:worker-list] 3]` plus `[UNVERIFIED: purpose, guide]`. |
| 5 | MINOR | `scope-01-contract.md` (D1-D5 citations) | `APPROVED.md` was not read; D1-D5 sit at `APPROVED.md:8-12`. | Read APPROVED.md and cite :8-12 for D1-D5. |
| 6 | MINOR | `scope-01-contract.md` line 50 | Omits the other D3 (:115) and D4 (:84, :184) occurrences. | Add the extra line anchors. |
| 7 | MINOR | `scope-01-contract.md` lines 99, 118, 119, 146 | Stale "not read / UNVERIFIED" prose sits beside later [CODE-VERIFIED] re-checks of the same claim. | Remove or update the stale prose so each claim has one tag. |
| 8 | MINOR | `scope-02-orca-recovery.md` line 17; scope-02:82-86 vs 05:194 | Line 17 "no `references/` dir exists" is untagged; scope-02 uses the inventory's `[G]` line numbers while 05 says they moved in the 215-line guide. | Tag line 17 [CODE-VERIFIED] with the ls evidence; at synthesis pick one guide line-number base. |
| 9 | MINOR | `05-orca-row-schema.md` lines 71, 189, 197 (cross-file note) | Nested-worker claim (`[G]` 130-131) against depth 1 at `orca-capabilities.md:97-102` is unresolved and design-relevant. | Resolve in a separate check before synthesis relies on worker depth. |
| 10 | MINOR | research-notes EXISTING_FILES row `src/superclaude/skills/ccsession-tag/README.md` | No research file read the README (orca launches at :228, worker-start note :236, orca-tabs :359); scope-01:112 mentions it only in passing. | Read README:228-236 and :359, or cite them where used. |
| 11 | MINOR | scope-02:155-160 (`list_sessions` :1482-1580 vs :1482-1581); 05:163 (`[H:worker-list]` 3) | Citation nits: inconsistent end line; flags are at help lines 10-11, not usage line 3. | Use one end line; cite help lines 10-11. |

## Actions Taken

- None. Report only; fix authorization false. No research file was edited (md5s of scope-01, scope-02, 05 and research-notes unchanged at the end of the review).

## Recommendations

- Fix issue 1 (tag the five lines in 05), then re-run this gate for 05 item 4 only.
- Fold the MINOR notes into the gap-fill pass if one runs; they do not block synthesis.
- At merge, check issue 9 against the other partition's findings before synthesis states nested-worker behaviour.

## Confidence

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 26 | Grep: 7 | Glob: 0 | Bash: 13 (counts across both context windows of this review; no web research)
- **UNCHECKED items:** none.
- **UNVERIFIABLE sub-claims (inside verified checks, blocker: this gate allows only `--help` text and existing captures):** every `[G]`, `[G:recovery]` and `[CLI]` line number and line count in 05 (Sources 3, 3b, 3c; lines 59-108, 157-161, 165, 174, 194, 197) and the guide-quoted lines in scope-02:82-86. Both files tag these UNVERIFIED or STALE DOC, which is the correct handling; QA did not run `orca skills get` or any non-help Orca command.

## QA Complete

## Verdict: FAIL
