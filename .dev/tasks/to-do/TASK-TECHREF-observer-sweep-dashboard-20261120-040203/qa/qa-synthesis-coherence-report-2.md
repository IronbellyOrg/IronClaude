# QA Report - Synthesis Coherence (Partition B)

**Topic:** Observer, sweep and dashboard family technical reference
**Date:** 2026-11-20
**Phase:** doc-qualitative (synthesis-coherence lens), partition B of the synthesis files
**Fix cycle:** N/A
**Status:** Complete
**Assigned files:** synth-05-subsystem-work-report-dashboard.md, synth-06-integration-config-perf.md, synth-07-conventions-extension-debt.md

---

## Overall Verdict: FAIL

One blocking finding (F-1, Check 4: UNVERIFIED items tagged in the synthesis files but absent from Section 14). Checks 1, 2, 3, 5, 6, 7, 8 and 9 pass; minor notes N-1 to N-12 are recorded and never fail the gate.

Inherited Structural Verdict: none was supplied in the spawn prompt, so this review ran standalone (no rf-qa PASS items were relied on).
Drift axis: not applicable (doc-qualitative phase, no Axis column).

Scope of reads (all paths absolute):
- Partition B files: `/home/coder/workspaces/IronClaude/.dev/tasks/to-do/TASK-TECHREF-observer-sweep-dashboard-20261120-040203/synthesis/synth-05-subsystem-work-report-dashboard.md`, `.../synth-06-integration-config-perf.md`, `.../synth-07-conventions-extension-debt.md`.
- Cross-check files (read in full): `.../synthesis/synth-01-overview-architecture.md`, `synth-02-directory-dataflow.md`, `synth-03-subsystem-observer.md`, `synth-04-subsystem-sweep.md`; register `.../gaps-and-questions.md` (134 rows plus the C8 section); `.../research/06-dashboard-design-vs-observer-gaps.md` section 7 (contradictions C1 to C8).
- Code spot checks in the snapshot `/home/coder/.cache/ic-snap-20261120/master` (see the Self-Audit section).

---

## Items Reviewed

### Check 1. Cross-file consistency of the same fact

| Fact | Locations compared | Result |
|---|---|---|
| Observer files, lines, fixtures | synth-01:16, synth-03:24, synth-05:147, synth-06:247 | Identical (13 `.py`, 6,011 + 158 lines; 19 JSON fixtures, 20 directory entries). Verified by `wc -l` and `ls`: 1+512+361+524+274+235+835+142+1461+48+192+126+1300 = 6,011; `fixtures/` = 20 entries. |
| Sweep files and lines | synth-01:17, synth-04:15-22 | Identical (3,759 = 12+1009+288+278+1477+695, verified). |
| AWR scripts, templates, tests, config keys | synth-01:18, synth-02:36-37, synth-05:9-21, synth-06:127 | Identical (16 scripts = 5,777 lines verified; SKILL.md 194 verified; 7 templates; 14 config keys verified in `config.json`). |
| Design package counts | synth-01:19, synth-02, synth-05:139, synth-06:224, 238, 250 | Identical (406 files; 180 exports per batch, 360 total; 19 scenarios; renderer 130+122+122+637 = 1,011 verified). |
| Allowlists | synth-03:42-50, synth-04:154-169, synth-06:38, synth-07:14-15 | Identical (observer 3 shapes and 13 prefixes, verified in `adapter.py:29-50`; sweep 10 templates, 7 verbs, 4 git shapes, verified in `probes.py:49-81`). |
| Caps and intervals (5 calls, 10 s, 8 MiB, 2 KiB, 15 s, 45 s, 1,000, 100) | synth-03:52-61, synth-06:230-232, synth-07:34 | Identical. |
| PR chain and dates | synth-01:20, synth-03:211-220, synth-05:7, 207, synth-06:73, synth-07:225, 331 | Identical. `d7d645ddd` is an ancestor of `61ac2c2e6` and was committed 2026-11-19 20:01:06 -06:00 (= 02:01:06Z on 11-20), matching the stated merge time. |
| Backoff sequence | synth-03:59, synth-06:24, synth-06:169, synth-07:130 | Wording mismatch: see N-4 (minor). |
| Discovery probe versus the allowlist | synth-02:138, synth-03:111, synth-06:42 | Wording mismatch: see N-5 (minor). |
| AWR config values | synth-06:127 versus `config.json:7, 9` | Two values shortened: see N-6 (minor). |
| Citation `test_cli_contract.py` | synth-07:71 (":956, 1032, 1077") versus synth-07:125 (":956, 1032, 1070") | Not a mismatch: line 1070 is `def test_zero_counts_are_present_for_every_class` and line 1077 is its `assert list(counts) == list(CLASSES)` (read in the snapshot). |

Verdict: PASS (no blocking mismatch; N-4, N-5, N-6, N-7 are minor).

### Check 2. Section 8 against Sections 5.1 to 5.6 and the data-flow diagrams in synth-02

| Item | Evidence | Result |
|---|---|---|
| Observer verbs | synth-06:42-44 versus synth-03:44-46 and synth-02:81-82: same three argv shapes, same line cites (`adapter.py:29, 30, 32, 173-190`); question shape is 8 tokens (orchestration, check, --all, --types, question, --run, id, --json) | OK |
| Sweep verbs | synth-06:45-51 versus synth-04:156-165: six called templates with the same call-site lines (399, 1150, 1281, 1165, 1178, 1335), four pinned (56-59), `test_probes_allowlist.py:624-638`; the 9-argv full sweep (1+2+5+1) matches synth-07:72 | OK |
| AWR verbs | synth-06:52-56 versus synth-05:69-72 and synth-02:146: same terminal, worktree, automations, tab, eval verbs; the same two write paths (`waker.py` terminal send and create, unread mark; `page.py` tab) | OK |
| Orchestrator design verbs | synth-06:58-73 versus synth-01:111, synth-02:151, synth-04:212, synth-05:205, synth-07:114: "about 30 verb forms, 4 equal a sweep template, none equals the observer's 3" is identical in all five files, and the four matches named at synth-04:212 and synth-06:73 are the same four | OK |
| Who reads and writes what | synth-06:91-99 versus synth-02:48-52 and synth-03:94: same paths (`snapshot.json`, `observe-<ts>.txt`, `.dev/sweeps/<UTC>-sweep.md`, run folder, `report.html`, `wakes/`, `settings.json`) | OK |
| Schemas | synth-06:105-109 versus synth-03:88-91, synth-04:190-192: snapshot v1 (20 of 31 attributes), sweep JSON v1 (the same 12 keys listed in synth-04:190), sweep Markdown (12 sections, two without `##`) | OK |
| Data-flow diagrams | synth-02:79-130: step order in diagram (c) equals the step table at synth-05:34-48; sweep diagram (b) equals the budget numbers at synth-06:233 | OK |
| Orchestrator automation | synth-02:127 names `orchestrator-poll` UNVERIFIED; synth-06:58-73 does not repeat it (design only) | consistent, but see F-1 for Section 14 |

Verdict: PASS (N-5 is the only wording issue).

### Check 3. Sections 9 to 11 against the subsystem sections

| Item | Evidence | Result |
|---|---|---|
| Observer flags (7) | synth-06:153-157 lists all seven that synth-03:152-160 lists; exit codes at synth-06:173 equal synth-03:166-171 | OK |
| Gate constants | synth-06:157 and synth-07:22 versus `commands.py:67, 70` (both `True`, read) | OK |
| Sweep flags and window | synth-06:158 versus synth-04:217 (`--run`, `--window`, `--root`, `--output`; 720 h) | OK |
| Constants `JOIN_PATH`, `CHECKED_ORCA_VERSION`, `JSON_SCHEMA_VERSION` | synth-06:159 versus synth-01:86 and synth-04:66 | OK |
| Caps and budgets | synth-06:230-237 versus synth-03:52-61, synth-04:180, synth-05:63 (`time_budget_minutes` 120 / 10, lock exit 3, wake retries 15 x 120 s = 30 min) | OK |
| Env vars | synth-06:140-147 versus synth-02:50, 140, 147 and synth-05:108 (`AWR_ROOT`, `AWR_HOOK_FILE`, `XDG_STATE_HOME`, `ORCA_CLI_COMMAND`) | OK |
| Config values | synth-06:127 versus `config.json` | two values shortened (N-6, minor) |
| State transitions | synth-06:19-26 versus `collector.py:306, 321` and `test_collector.py:149` | first-failure wait is written ambiguously (N-4, minor) |

Verdict: PASS.

### Check 4. Section 14 carries every contradiction, stale document, UNVERIFIED item and C8 candidate

Method: matched all 134 register rows of `gaps-and-questions.md` against synth-07 sections 14.1 to 14.6, then harvested every `[UNVERIFIED]`, `[CODE-CONTRADICTED]`, `[STALE DOC]`, "contradict" and C8 mention in synth-01 to synth-06 (Grep over the synthesis folder) and looked each up in synth-07.

| Class | Evidence | Result |
|---|---|---|
| Register rows (UNVERIFIED 40, CODE-CONTRADICTED 5, STALE DOC 35, DEFECT-CANDIDATE 2, GAP 52) | Every ID is in synth-07 14.4 B (U-01 to U-40, counted 3+6+5+6+3+7+5+5 = 40), 14.4 A (CC-01 to CC-05, SD-01 to SD-35), 14.5 (DC-01 = C8-8, DC-02 = C8-9) or 14.4 C (G-01 to G-52, with G-13, G-35, G-36, G-37, G-38, G-40, G-45 carried in 14.1, 14.4 A, 14.5 or 14.6). 15.1 states the same totals (40+5+35+2+52 = 134). | OK |
| C8 candidates | Nine in synth-07:268-276: C8-1 to C8-5 KNOWN LIMIT (cited), C8-6 and C8-7 KNOWN LIMIT sequenced to PR B / PR A, C8-8 and C8-9 DEFECT-CANDIDATE. Labels agree with synth-01:115-116, synth-02:104, 115, synth-04:80-88, synth-05:100, 198, synth-06:3, 189-190, 194-195. No file relabels a DEFECT-CANDIDATE as a plain gap; the three files that changed a label (file 04 for C8-1 to C8-3, file 05 for C8-6, C8-7) are listed as superseded at synth-07:278. | OK |
| Exact words on every DEFECT-CANDIDATE | "Remediation task not created (read-only brief); flagged for the owner" is present for C8-8 and C8-9 at synth-07:275-276, in 5.5 at synth-05:100 and in 5.6 at synth-05:198 (8 occurrences in synth-07). | OK (see N-3 for the shorter wording in 14.1 and for C8-4, C8-5) |
| Contradictions among research files (synth-02:179; synth-06:254) | Carried: stalled/fenced labels (synth-07:278), scope of "no DEFECT-CANDIDATE" (14.4 C row G-01), commands.md claim (SD-08, SD-09 and the GF-2 paragraph at synth-07:227), 6,321 and test counts (14.4 C count row). | OK |
| Contradictions C1 to C8 of synth-05:189-194 | C1, C2 (SD-21 to SD-24), C3 (SD-25), C5 (SD-27), C6 (SD-22), C8 (SD-26) carried. C4 is carried as the open question at synth-07:194 (alignment items 1-10 include the recommendation-text question) and synth-07:190 (write-back); research 06:202 itself says C4 is "not a contradiction inside shipped behaviour", so I do not count it missing. C7 is "consistent". | OK |
| Stale documents in synth-01 to synth-06 | Every doc statement they call stale or contradicted (SD-01 to SD-35, CC-01 to CC-05) is in 14.4 A. | OK |
| UNVERIFIED tags in synth-01 to synth-06 | 3 of the tagged items are not in 14.4 B and have no register id (details in F-1): (a) Orca automation `orchestrator-poll` and orchestrator repo `IronOrchestrator` (synth-02:127, synth-05:97; synth-07:238 names only `coordinator-morning-wake` and `coordinator-missed-check`); (b) "Reason for three wrappers not stated [UNVERIFIED]" (synth-01:74; synth-07 holds only the fact row at 113 and G-52 at 253); (c) the issue #590 result tagged [UNVERIFIED] at synth-01:98 and synth-04:90 but untagged and unlisted at synth-06:192, 221 and synth-07:150. | FAIL (F-1) |

Verdict: FAIL (F-1 blocking).

### Check 5. Section 13 Extension Guide

| Item | Evidence | Result |
|---|---|---|
| Scenario A (sweep class or rule) | Files and lines exist in the subsystem sections: `models.py:50-59` (synth-04:18), `classify.py:42-51, 345-355` (synth-04:17, 121), `report.py:26-27, 54-68, 545-558` (synth-04:115, 139, 192), tests `test_classify.py:277, 351, 378-379` and `test_report.py:1091` (synth-04:121). The same unpack constraint is in synth-04:121 and synth-07:55. | OK |
| Scenario B (sweep probe) | `ALLOWED_ORCA` 49-60, `ALLOWED_GIT` 68-81 (read in `probes.py`); the 9-argv recording equals synth-04 and synth-06:220; pinned zero-argv test equals synth-04:167 | OK |
| Scenario C (snapshot field) | `_FIELDS` 58-90, `_TEXT_FIELDS`, schema `definitions.row.properties`, golden-bytes pitfall equal synth-03:65, 89, 125 | OK |
| Scenario D (observer view or key) | `KEY_NAMES` `view.py:30`, `build_view`, `_columns` `render.py:480-568`, the three width classes and layouts A/B/C equal synth-03:173-193, 246-248 | OK |
| Scenario E (AWR source) | `main(run)` shape, `REQUIRED_CHECKS`, `run.py` argv-length branches, `common.run_cmd`; SKILL.md step table lines equal synth-05:9, 48 | OK |
| Entry points (signatures) | `collect`, `classify`, `classify_all`, `render`, `to_json`, `build_view`, `Collector.__init__`, `LiveSource.read_pages` equal synth-03:101-103 and synth-04:95-99, 218-222 (same line numbers) | OK |
| "Unification touch points" (synth-07:102-119) | 14 rows, every one is a fact with a cite; searched the file for recommend, should, prefer, better, unif: the only hits are "no recommendation" disclaimers (synth-07:102, 351) and the sweep property "recommends nothing" | OK |

Verdict: PASS.

### Check 6. Live versus designed across Sections 5.5, 5.6, 8 and 14

| Item | Evidence | Result |
|---|---|---|
| Entry writer `superclaude orchestrator report-entry` | "designed; absent" in synth-05:95, synth-06:85, 58, synth-07:111, 156, 273. Snapshot check: `grep orchestrat cli/main.py` has 0 hits; the only entry-file writer is `move_to_closed` (`run.py:466`; line 483 sets `closed_at` and `close_reason`, 487 replaces the file). | OK |
| `orchestrator_repo` | master rejects it: `cycle.py:58` defines `_TOP_KEYS`, `cycle.py:216` rejects unknown keys (read); `common.py` reads it; PR A open. synth-05:96, synth-06:86, 128, synth-07:110, 157, 274 agree. | OK |
| Reader side of the living report | "built (PR #684), fake-tested" in synth-05:93 and synth-06:85, 195; commit `d7d645ddd` is an ancestor of `61ac2c2e6` | OK |
| `prefs.py answer` for a session url | `prefs.py:20` `URL = re.compile(r"^https://(github\.com\|app\.clickup\.com)/\S+$")` and `check_url` at 30-32 exit "not an item URL" (read); DEFECT-CANDIDATE everywhere | OK |
| D-1 fixture replay | `collector.py:129` `SourceResult("FAILED", code="no-question-fixture")`; `commands.py:77, 188` refuse `--questions` with `--fixture` (grep); live R2/R3 wired with both gates `True` | OK |
| Observer 3 of 20 designs, package "not a production integration" | synth-05:137, 164-169, synth-01:100, synth-07:320-321 agree | OK |
| Orchestrator design, `/sc:orchestrator`, verbs | marked designed in synth-05:95, 202-207, synth-06:58, synth-07:119, 326; none is described as built | OK |
| Sweep Phase 1 limits | printed limits and KNOWN LIMIT labels agree in 5.3 (synth-04:80-88), 8 (synth-06:189-190) and 14 | OK |

Verdict: PASS.

### Check 7. Neutrality

Searched the three assigned files (and the others) for recommend / should / prefer / better / best / unif / consolidat. Hits are only the disclaimers "facts only; no unification recommendation" (synth-05:3, synth-06:3, synth-07:3, 102, 351), the field name `recommend` (synth-05:80), the sweep's own "recommends nothing" (synth-07:59, 311), and "recommendation text" as an open owner question (synth-07:194). No sentence recommends unifying the tools or preferring one. Writing rules such as synth-05:222 ("Write '20 designs, 3 partly implemented'") govern wording, not the tools.

Verdict: PASS.

### Check 8. Single source of truth and key numbers against Section 1

Key numbers in synth-01:14-20 re-derived by `wc -l`, `ls` and `git show`: observer 13 files / 6,011 + 158 lines, sweep 3,759, AWR scripts 5,777 + SKILL 194, SPEC 653 lines (synth-07:333), `docs/designs/orchestrator.md` 1,412 (synth-01:20), renderer 1,011. All match. Totals in 15.1 (134 = 40+5+35+2+52) equal the register. Facts that are stated in two places agree (exit codes in 5.2 and 10.1; sweep exits in 5.4 and 10.1; lock and gate in 5.5 and 10.1). Mismatches found are only those logged as N-4, N-5, N-6, N-7.

Verdict: PASS.

### Check 9. Sections 6 and 7

Section 6 (synth-06:9) says "N/A as a client-side store" and gives the reason (CLI and file based tools; the package is a static renderer), then lists the runtime state that exists (observer `Session` and `CycleResult`, AWR `run.lock`). That agrees with 5.2 ("keys change the Session only", synth-03:173) and 5.5 (lock, synth-05:63). Section 7 (synth-06:32) says "N/A: these tools have no component tree. The subsystem tables in Section 5 are the inventory", which agrees with 15.2 item 4 (synth-07:301). One wording clash is logged as N-11.

Verdict: PASS.

---

## Summary

- Checks passed: 8 / 9 (Checks 1, 2, 3, 5, 6, 7, 8, 9); Check 4 failed.
- Checks failed: 1
- Blocking issues: 1 (F-1, graded IMPORTANT)
- Minor notes: 12 (N-1 to N-12), recorded only; they never fail the gate and need no re-check.
- Issues fixed in place: 0 (fix authorization was false; no synthesis file was modified)

## Issues Found

### Blocking

| ID | Severity | Locations | Issue | Required Fix |
|---|---|---|---|---|
| F-1 | IMPORTANT (blocking) | Missing from synth-07 14.4 B (lines 229-240). Tagged at: synth-02:127 and synth-05:97 (`orchestrator-poll` automation, `IronOrchestrator` repo, `waker.py` triggers: "outside the repo: [UNVERIFIED]"); synth-01:74 ("Reason for three wrappers not stated [UNVERIFIED]"); synth-01:98 and synth-04:90 (issue #590 result "[UNVERIFIED]"). Compare synth-07:238 (names only `coordinator-morning-wake` and `coordinator-missed-check`), synth-07:113 and 253 (wrappers appear only as a fact and as G-52), synth-07:150, synth-06:192, 221 (the #590 figures appear with no UNVERIFIED tag). | The brief requires Section 14 to carry EVERY UNVERIFIED item from synth-01 to synth-06. Three items tagged UNVERIFIED in Sections 2, 4 and 5 are in neither the register `gaps-and-questions.md` (grep for `orchestrator-poll`, `IronOrchestrator`, "three wrappers" and "#590" in the register finds no U-row) nor Section 14.4 B. A reader who uses 14.4 B as the complete list of open uncertainties would miss them, and the issue #590 numbers are UNVERIFIED in two files and untagged in three others. | Add three rows to 14.4 B (a note that they carry no register id is enough): (1) the Orca automations and orchestrator repo outside the checkout, adding `orchestrator-poll` (`*/5`), `IronOrchestrator` and the `waker.py` triggers to the U-17 to U-23 row; (2) "why the observer, sweep and report skill have three separate Orca wrappers is not stated"; (3) "issue #590 result (264 sessions, 263 `could not determine`) is a recorded report, not re-run". Then add the same "recorded, not re-run (UNVERIFIED)" wording at synth-06:192, 221 and synth-07:150. |

### Minor notes (do not fail the gate)

| ID | Locations | Note |
|---|---|---|
| N-1 | synth-06:3, 186, 194 use DC-01 and DC-02; synth-07:155, 158, 275-276 and synth-03:225, synth-05:198 use D-1, C8-8 and C8-9 | Same two DEFECT-CANDIDATEs carry three ids; the mapping (DC-01 = C8-8, DC-02 = C8-9 = D-1) exists only in the register. Add one alias line in 14.5. |
| N-2 | synth-05:189-194 ("C1" to "C8" contradictions; "C8 names only") and synth-06:107 ("C7") versus synth-07:255, 334 ("C8" = the scope rule) | The letter C8 means two things. Rename the contradiction labels (for example K1 to K8) when the document is assembled. |
| N-3 | synth-07:271-272 (C8-4, C8-5) and 155, 158 (14.1 pointers for D-1 and C8-8) | These print only "Flagged for the owner"; the document's own rule at synth-07:262 and the register print "Remediation task not created (read-only brief); flagged for the owner" for a KNOWN LIMIT with no tracked owner, and the exact words are present for every DEFECT-CANDIDATE in 14.5. Add the words to C8-4 and C8-5. |
| N-4 | synth-06:24 ("wait 15 -> 30 -> 60 -> 60 s") versus `collector.py:306` (`_wait = min(_wait * 2, max)`, starting at 15), `test_collector.py:149` (`[30.0, 60.0, 60.0, 60.0]`), synth-07:130 | After the first failed first page the wait is 30 s, not 15 s; write "30, 60, 60, 60 s after consecutive failures; 15 s after any parsed page". |
| N-5 | synth-06:42 ("allowed by exact match"), synth-02:138 ("not allow-listed by adapter"), synth-03:111 | In code `DISCOVERY_TEMPLATE` is accepted by `assert_allowed` (`adapter.py:148-149`) but `_find_orca` spawns its own argv (`install_user_setup.py:258-264`) without calling it. Use synth-03's wording in all three places. |
| N-6 | synth-06:127 ("daily_run_local 07, missed_run_dm_local 09") versus `config.json:7, 9` | Values are the strings "07:00" and "09:00". |
| N-7 | synth-01:100 ("9 of 9 fixture names ... 0 of 10 contents", "inherits") versus synth-05:162 ("all 9 variant names plus base ... 0 of 10") | Denominators differ (partition A file); "inherits" conflicts with "no shared code or data". Use "10 of 10 names". |
| N-8 | synth-07:200 says nine STALE DOC rows are also CODE-CONTRADICTED; the 14.4 A rows for SD-25 to SD-29 do not mark SD-26 and SD-27 | Mark them in the rows. |
| N-9 | synth-07:280 ("heartbeat classification" not adopted) has no counterpart in 5.6 (synth-05:178); synth-05:171 settles a research 06 internal disagreement (S1, S2, S4 grouping) that Section 14 does not list | Add "heartbeat classification" to the 5.6 NOT BUILT row or drop it from 14.5; optional one-line note in 14.4 C. |
| N-10 | synth-07:252 (G-32: `refresh` body untraced) versus synth-05:85 (seven stages of `run.py refresh`) | Say the stages come from research 05 and were not re-traced by the entry-point pass. |
| N-11 | synth-07:300 ("the document carries no client-state section") versus synth-06:13-14 (observer `Session` and `CycleResult` listed in Section 6) | Reword 15.2 item 3: "Section 6 lists in-memory state; compare it with `Session` and `CycleResult`". |
| N-12 | synth-07:4 (line-budget note), synth-07:140 (ids "of `gaps-and-questions.md`") | Meta text should be dropped on assembly, and the U-, SD-, G- ids need that register (or an equivalent key) shipped or described, because the deliverable does not include it. |

## Actions Taken

None. Fix authorization was false; no synthesis file, source file or design file was modified. The only file written is this report.

## Inherited Structural Verdict - Reliance Audit (PR-04, INV-019)

No `## Inherited Structural Verdict` section was in the spawn prompt, so there are no rf-qa PASS items to rely on; this run used the standalone fallback.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited verdict was supplied. I treated the Gate 1 and Gate 2 reports as unread input and re-read the cited code and the register myself.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Section 14 completeness against the register: matched all 134 register ids against synth-07 by reading `gaps-and-questions.md` (lines 1-290) and synth-07 14.1 to 14.6, then Grep over synth-01 to synth-06 for every `[UNVERIFIED]` tag; this found F-1.
- Key counts re-derived from the code snapshot with `wc -l`, `ls` and `git show`: observer 6,011 + 158, sweep 3,759, AWR scripts 5,777, SKILL.md 194, renderer 1,011, SPEC 653 lines, orchestrator design 1,412 lines, 20 observer fixture entries, 16 AWR scripts.
- Allowlist and gate claims against source: `adapter.py:26-62, 125-190` (13 prefixes, 3 shapes, `MAX_CALLS_PER_CYCLE = 5`, 8 MiB, 2 KiB, `PER_CALL_TIMEOUT`), `probes.py:44-83` (10 templates, 4 git shapes, `ORCA_VERSION_FILE`), `commands.py:67, 70` (both gates True).
- Behaviour claims against source: `collector.py:306, 321` and `test_collector.py:140-149` (backoff), `install_user_setup.py:247-270` (discovery, `topics` iteration outside the `try`), `prefs.py:20, 30-32` (URL regex), `run.py:466-488` (`move_to_closed`), `cycle.py:58, 216` (`_TOP_KEYS`), `collector.py:129` and `commands.py:77, 188` (D-1), `common.py:22-48` (`orchestrator_repo`, `AWR_ROOT`), `cli/main.py` (no `orchestrat` match), `config.json` (14 keys and values).
- Git fact: `d7d645ddd` (PR #684) is an ancestor of `61ac2c2e6`, committed 2026-11-19 20:01:06 -06:00.

1. Factual claims independently verified: about 45 (counts, constants, line-cited behaviour, config values, one git ancestry).
2. Files read to verify: the three assigned files, four cross-check synth files, `gaps-and-questions.md`, `research/06-dashboard-design-vs-observer-gaps.md` (section 7), `adapter.py`, `probes.py`, `install_user_setup.py`, `test_cli_contract.py`, `prefs.py`, `run.py`, `common.py`, `config.json`, `collector.py`, `test_collector.py`, `commands.py`.
3. If I had found 0 issues, the evidence above (counts, ids matched one by one, tags harvested by Grep) is what I would show; I found one blocking and twelve minor items.
4. Web research: none performed; Tavily was not needed (all evidence is local). Tool-engagement summary: Tavily 0 attempts, no fallback.

Not re-checked (reported as the research states them, not by me): PR merge states other than #684, `gh` issue and PR body wording (#534, #590, #539), the `.dev/issues/409/` records, and most line numbers inside files I did not open (`classify.py`, `report.py`, `view.py`, `render.py`, `export.py`). A mismatch there would be a line-number drift, which is a minor finding.

## Recommendations

1. Fix F-1 (three rows in 14.4 B plus consistent tagging of the issue #590 figures), then request the cycle-1 re-review; only F-1 needs re-verification.
2. Apply N-1 to N-12 when the document is assembled; none needs a re-review.

## Confidence Gate

- **Confidence:** Verified: 9/9 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (every check was run with tool evidence; "verified" here means checked, not passed)
- **Tool engagement:** Read: 26 | Grep: 19 | Glob: 2 | Bash: 4
- Tool calls (47) exceed the 9 checks.
- Unchecked items: none. Unverifiable items: none (limits of scope are listed under "Not re-checked" above).

## QA Complete

