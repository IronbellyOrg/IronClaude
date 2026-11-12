# QA Report — Fix-Cycle Verification (report-qualitative, content lenses)

**Topic:** Orchestrator mode Phase 1 research report (issue #339)
**Date:** 2026-11-07
**Phase:** fix-cycle (report-qualitative)
**Fix authorization:** false (report not edited)
**Report under review:** `RESEARCH-REPORT-orchestrator-mode.md`
**Inputs:** `qa/qa-consolidated-findings-phase6.md`, `qa/qa-fix-log.md`

---

_Status: complete. Sections were appended as verification proceeded._

## Overall Verdict: FAIL

Four blocking findings: one original finding left open (P6-07), and three new contradictions introduced or left behind by fixes (N-2 from P6-16, N-3 from P6-46, N-4 from P6-49 and step 1.0b). The global checks pass: Section 8 plans A1 as Section 7 recommends, A4 is rejected only, WC-10 holds everywhere it was checked, and the later phases are recorded, not designed.

## Blocking findings (open)

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| P6-07 (OPEN) | IMPORTANT | S6 A1 Description `:899` | The fix corrected the A1 diagram (`:931-932`), S7 (`:1089`) and step 1.15, but the A1 Description still says "The `/sc:sweep` command and the `sc-sweep-protocol` skill run `superclaude sweep`, read its JSON and write the dated report." This contradicts `:931-932` ("report.py renders and writes the dated static report ... the skill only runs the CLI and reads the result (no Write in its allowed-tools)"), step 1.5 and step 1.15. The rendering-owner conflict that P6-07 named is still in the report. (`:1000` "skill writes the dated report" is in A3, a different option, and is correct for A3.) | At `:899` write: "The `/sc:sweep` command and the `sc-sweep-protocol` skill run `superclaude sweep run`; `report.py` renders and writes the dated report and the skill reads the result." |
| N-2 (new, from the P6-16 fix) | IMPORTANT | Step 1.3 rule 4b-contract (`:1204`); step 1.8 fixtures (`:1214`); S3.1 precedence (`:360-371`); S4.5 GQ-96 (`:560`) | Step 1.3 and S3.1 say each session gets exactly one class and the first matching rule wins. Rule 1 maps any contract with `worker_status: blocked` to waiting (a). The P6-16 fix then defines 4b-contract as "frozen when the latest implement `return-contract.yaml` has `worker_status: blocked`" and step 1.8 adds "a `blocked` implement contract" as a 4b-contract fixture. Under first-match precedence that fixture can never reach rule 4, so the plan's test expects (b) while its own rule 1 gives (a). GQ-96 (`:560`) resolves the same case as "fits kinds (a) and (b) ... the dimensions are independent", which the one-class precedence does not implement. The effect matters: a frozen `/sc:implement` plan (`WORKER-CONTRACT.md:133`, read this pass) would print only under "explicit questions (a)", with its question text, and never under "frozen or blocked by policy (b)" (`:405`), so the coordinator's report would hide a freeze during which the contract forbids any dispatch (`WORKER-CONTRACT.md:134-136`). The same overlap exists in Section C (`research-notes.md:192` vs `:197`); the fix made it concrete without reconciling it. | State in step 1.3 (and S3.1) that the policy dimension ("policy: frozen / not frozen", `data-dictionary.md:27`) is computed for every row independently of the class, so a blocked implement contract gets class waiting (a) from rule 1 **and** policy frozen, listed under (b). Rule 4b then sets the class only for rows with no earlier match (the `failed` + non-`E-RESUME-NEEDED` contract, the ledger and the ready-Task cases). Change the "blocked implement contract" fixture to assert both outputs. |
| N-3 (new, left by the P6-46 fix) | IMPORTANT | S3.2 SC-1 (`:437`) vs step 1.11 (`:1217`) | P6-46 rewrote step 1.11 to "Proof by snapshot diff, not by patching write primitives", but SC-1's "How it is checked" still reads "Patch the forbidden entry points with `side_effect=AssertionError(...)`; run inside `CliRunner.isolated_filesystem()`", citing only the entry-point precedent. The success criterion and the step that proves it now describe different checks; the Integration Checklist (`:1457`) ties SC-1 to step 1.11. | Update SC-1 to: "Snapshot diff of the isolated root (path, size, `st_mtime_ns`, SHA-256) before and after `sweep run`, with `HOME` and `XDG_STATE_HOME` inside it; only the dated report (and a new `--output` directory) may differ; subprocess entry points patched with `side_effect=AssertionError` (step 1.11)". Keep the `test_contract_status_cli.py:44-66` citation for the subprocess half only, and add "snapshot diff: plan decision, no in-repo precedent". |
| N-4 (new, from the P6-49 rollback text vs step 1.0b) | IMPORTANT | Rollback `:1278` vs step 1.0b `:1196` | `:1278` says "WC-14 does not land on the working default alone: step 1.0b records the owner's answer on GQ-11 ... before 1A starts." Step 1.0b says "record the answer or 'working default accepted'" and "unanswered decisions keep the working default and stay in S9". So with GQ-11 unanswered, step 1.0b lets steps 1.17-1.19 change the shared contract on the working default alone, which is what `:1278` says cannot happen. The two sections give opposite answers on whether a shared-contract change needs an owner answer. | Pick one. Either make GQ-11 (and the WC-14 wording) a hard gate in step 1.0b: "steps 1.17-1.19 do not start until the owner's answer on GQ-11 is recorded; 'working default accepted' counts only when the owner says it". Or reword `:1278` to say WC-14 may land on the working default, with the rollback table as the revert plan. |

## Original findings: RESOLVED / OPEN

Content-lens findings (ACT, NM, XR, DA, RF, FR) and the plan-decision items named by the orchestrator. "Verified at" gives the current report line I read or grepped.

| Finding | Lens | Status | Verified at / evidence |
|---|---|---|---|
| P6-01 | content | RESOLVED | S1 read (`:1-80`); fix present as logged |
| P6-02 | content | RESOLVED | S1 read (`:1-80`); fix present as logged |
| P6-03 | EQ/CMP/NM | RESOLVED | `:1711-1715`: "43 files ... (24 + 18 + `qa-nb4-fix-log.md`)", Phase 5 bullet names the 18. Independently re-counted `qa/` with `ls`: 24 Phase 2-3/task files; 4 analyst-synthesis + 2 phase5 consolidated + 12 `qa-synthesis-*` = 18; plus `qa-nb4-fix-log.md` = 43 (excluding `qa-lens-*`, the phase6 consolidated file, the fix log and the fix-verification files) |
| P6-07 | ACT/RF | **OPEN** | `:899` still says the skill writes the report (see above) |
| P6-12 | content | RESOLVED | `:342`, `:1226`: no `command -v` call, no extra allowed-tools entry |
| P6-13 | content | RESOLVED | steps 1.14-1.16 (`:1225-1227`) space-form literals; [CONTRADICTION] marker on colon vs space kept (`:1094-1098`) |
| P6-14 | DA/ACT | RESOLVED | "proved final" no longer appears (grep, 0 hits); rule 2 limited to Orca `exited` or an Orca-observed exit, a transcript final turn is a note (`:366-368`, `:1204`); S9 row 70 (`:1577`) closed to the same rule; "Orca's stall" restored at `:56` |
| P6-15 | ACT | RESOLVED (routed) | Row 81a (`:1589`); step 1.3 rule 3 synthetic only, live -> could not determine "fenced evidence not readable" (`:1204`); SC-4 (`:440`) agrees |
| P6-16 | ACT | RESOLVED as asked (detection per sub-case, rows 81b and 81c, one fixture per sub-case) but the fix **introduced N-2** | `:1204`, `:1214`, `:1590-1591` |
| P6-17 to P6-21 | content | RESOLVED | steps 1.2-1.7 (`:1203-1207`) read: dataclasses and constants, seams, bounds, schema v1, exit codes 0/1/2 |
| P6-22 | ACT | RESOLVED | step 1.4 live acceptance names its artifact; step 1.29 (`:1258`): 30 s, pass = exit 0 and `run` listed, saved to `artifacts/sweep-help-pipx.txt` |
| P6-23 | ACT | RESOLVED | `:1473` live end-to-end item with before/after captures; `:1474` WC-14 vs G1-G7 item |
| P6-24 | NM | RESOLVED | `:831` "only Kubernetes taint ... (D1) contradicts WC-10; ... (D3) is a naming note and ... (D4) an action note"; 4.8 `:616` "Of these three, only D1" |
| P6-25 | NM | RESOLVED | One count: `:36`, `:391`, `:1393` (98a), X-7 `:1430` all say the question's six (with idle) plus fenced = seven, rules 1-7 plus idle |
| P6-26 | content | RESOLVED (routed) | Row 81d (`:1592`); Effort basis `:1050`; step count re-counted from the step tables: 2+7+6+3+4+7+5 = 34, matches |
| P6-27 | XR | RESOLVED | S2.4 "Precedents the options in Section 6 rest on" table (`:247`), pointer at `:893` |
| P6-28 | XR | RESOLVED | "settled by GQ-84" no longer appears (grep, 0 hits); scope-01 `:100` at `:577` (4.6) and `:1347` (8.1) |
| P6-29 | content | RESOLVED | agents-fleet labelled unfetched, context only (`:831`); see minor note M-4 |
| P6-30 | DA | RESOLVED | every `~/workspace` hit (`:157`, `:317`, `:470`, `:569`, `:597`, `:1023-1024`, `:1151`, `:1546`, `:1602`, `:1613`) is narrowed to `--all` plus the dev-fallback allowlist entry, with single-project mode from the cwd |
| P6-31 to P6-37 | content | RESOLVED | S6-S8 read (`:882-1238`); fixes present as logged |
| P6-38 | RF | RESOLVED | SC-7 reworded at `:443` and checklist `:1463` to "stays listed while its source still shows it"; "until answered" left to WC-14 G5 |
| P6-39 | FR | RESOLVED | "WC-1 to WC-13", "override WC-1", "amending WC-1", "not a WC-1 clause": 0 hits; `:1186` "WC-2 to WC-13; WC-1 unused; no WC-14 today"; S9 row 9 (`:1504`) "add WC-14, or reuse the unused WC-1 ID" |
| P6-40 | FR | RESOLVED | "runs `git stash` commands beyond": 0 hits; X-1 `:1424` matches |
| P6-41 | FR | RESOLVED | "Follow the help reading": 0 hits; X-4 `:1083` and 8.4 X-4 `:1427` both apply the split rule and cite Gap 19 `:144` |
| P6-42 | IMPL (plan decision) | RESOLVED | step 1.4 seams `_orca(*args: str) -> str`, `_git(cwd: Path, *args: str) -> str`, matching the `reflect/config.py` precedent; labelled plan decision |
| P6-43 | IMPL (plan decision) | RESOLVED | step 1.3 `classify(...) -> Classification`, `safe_to_close(...) -> SafeToClose`, "(plan decision, new design)" (`:1204`) |
| P6-44 | IMPL (plan decision) | RESOLVED | step 1.5 `render(...) -> str`, `write_report(text, output_dir, now) -> Path`, labelled |
| P6-45 | IMPL (plan decision) | RESOLVED | step 1.2 dataclasses and constants, labelled |
| P6-46 | IMPL (plan decision) | RESOLVED in step 1.11 (labelled, limit stated, lack of precedent admitted) but **SC-1 not updated: N-3** | `:1217` vs `:437` |
| P6-49 | IMPL (plan decision) | RESOLVED as asked (subsection exists, labelled, files and reports covered) but **contradicts step 1.0b: N-4** | `:1262-1278` vs `:1196` |

Plan-decision check (orchestrator request): P6-42 to P6-46, step 1.11 and the rollback table are each marked "plan decision, new design". Each rests on cited research (Section C, `reflect/config.py`, `test_contract_status_cli.py:44-66`, `WORKER-CONTRACT.md:108`, `:133-136`), and none designs a later phase. Step 1.11 states its limit and admits the snapshot diff has no in-repo precedent.

## Minor notes (do not fail the review, not rechecked)

| # | Location | Note |
|---|---|---|
| M-1 | `:888` | Says "K-4 tests prove read-only"; the read-only key is K-5. Wrong key ID on a true claim. |
| M-2 | `:893` | The inserted pointer paragraph splits the key table, so the K-5 and K-6 rows are cut off from the header. Formatting. |
| M-3 | step 1.0a | The cursor check uses a settled worker whose transcript no longer changes, so it shows the cursor reads but not that it advances. Weak check, still a real one. |
| M-4 | `:831` | Says the unfetched agents-fleet source "contradicts" WC-10. The source is labelled unfetched, so "would contradict, if it says what the summary says" is the honest wording. |
| M-5 | rule 4b-Task | Every ready Task, the coordinator's own included, lands under (b). Honest because the row says "creator: could not determine"; noisy only. |
| M-6 | Effort basis `:1050` | "1A 7 (... one new test file ...)" is loose: 1A's steps add more than one test file. The count of 34 steps is correct. |

## Items that PASS

- Original findings RESOLVED (count: 39 of the 40 findings above, P6-07 being the one open; with P6-16, P6-46 and P6-49 resolved as asked but each tied to a new blocking finding): P6-01, 02, 03, 12, 13, 14, 15, 16, 17-21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31-37, 38, 39, 40, 41, 42, 43, 44, 45, 46 (step 1.11), 49 (rollback table).
- G-1 Section 8 plans A1, the option Section 7 recommends (S7 `:1089`, S8 steps 1.0a-1.31).
- G-2 A4 is rejected only (`:1151`) and never recommended.
- G-3 WC-10 intact: rule 2 is Orca-only (`:366-368`, `:1204`), live fenced rows give could not determine (`:1204`, `:440`), a transcript final turn is a note, S9 row 70 (`:1577`) agrees.
- G-4 Later phases recorded, not designed (`:1280-1288`).
- G-5 The plan-decision items (P6-42 to P6-46, step 1.11, the rollback table) are labelled, rest on cited research and stay inside Phase 1.

## Confidence

- **Confidence:** Verified: 45/45 (40 finding rows + 5 global checks) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Confidence measures how fully the checks were made, not whether they passed. The verdict is FAIL because four blocking findings are open.
- **Tool engagement:** Read: 14 | Grep: 6 | Glob: 0 | Bash: 5 (after the context compaction). Counts from before the compaction were not kept; that part read the consolidated findings, the fix log, report `:1-80` and `:882-1238`. Several Read and Grep calls each covered more than one finding row, so the post-compaction total of 20 Read and Grep calls is below the 45 items. The pre-compaction reads cover the rest, but because those counts were not kept, this is flagged as the Tool Engagement Minimum requires.
- Web research: none was needed, so Tavily was not called and no fallback happened.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- The spawn prompt supplied no Inherited Structural Verdict, so I relied on no rf-qa PASS item.
- I took the fix-log descriptions of P6-01, P6-02, P6-17 to P6-21 and P6-31 to P6-37 as pointers only. Each was checked against the report text read before the compaction (`:1-80`, `:882-1238`).

**(b) Independent semantic checks (≥1 required, INV-019):**
- Source count for P6-03: re-counted with `ls` on `qa/`, 24 + 18 + 1 = 43, matching `:1711-1715`.
- Step count for P6-26: re-counted from the S8 step tables, 2+7+6+3+4+7+5 = 34, matching `:1050`.
- N-2: read `src/superclaude/core/WORKER-CONTRACT.md:120-144`. `:133` defines frozen and `:134-136` forbid dispatch while frozen. Read `research/research-notes.md:185-209`, where rule 1 (`:192`) and rule 4(b) (`:197`) overlap. Together these show the hidden freeze is a safety problem, not wording.
- Residual-text greps on the report found 0 hits each for "proved final", "Follow the help reading", "settled by GQ-84", "WC-1 to WC-13", "override WC-1", "amending WC-1" and "runs `git stash` commands beyond".
- N-3 and N-4: read SC-1 `:437` against step 1.11 `:1217`, and rollback `:1278` against step 1.0b `:1196`. Each pair is a direct contradiction between two sections; neither is a fix-log claim.

## Issues Found

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| 1 | IMPORTANT | `:899` | P6-07 open: the A1 Description still says the skill writes the report | See the blocking table, P6-07 |
| 2 | IMPORTANT | `:1204`, `:1214`, `:360-371`, `:560` | N-2: a blocked implement contract gets class (a) from rule 1, which hides the freeze from the (b) list; the 4b-contract fixture cannot be reached | See the blocking table, N-2 |
| 3 | IMPORTANT | `:437` vs `:1217` | N-3: SC-1 describes primitive patching, step 1.11 a snapshot diff | See the blocking table, N-3 |
| 4 | IMPORTANT | `:1278` vs `:1196` | N-4: the rollback says WC-14 needs the owner's answer, step 1.0b lets it land on the working default | See the blocking table, N-4 |
| 5-10 | MINOR | see Minor notes | M-1 to M-6 | Optional |

Totals: CRITICAL 0, IMPORTANT 4, MINOR 6.

## Recommendations

- Fix P6-07, N-2, N-3 and N-4 as given in the blocking table, then run one more fix-verification pass limited to those four. This pass counts as the review after fix cycle 1. Under the two-cycle limit, if any of the four is still open after the next fix, stop and send it to the owner.
- N-2 is the one with a behaviour effect: the plan's step 1.3 and its step 1.8 fixture must agree before the plan is handed to `/sc:workflow` or `/sc:implement`.
- Leave M-1 to M-6 as notes; fix them only while editing the same lines anyway.

## QA Complete

## Verdict: FAIL
