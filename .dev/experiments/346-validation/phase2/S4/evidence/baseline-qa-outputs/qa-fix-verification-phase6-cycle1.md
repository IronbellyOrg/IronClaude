# QA Report - Gate 3 Fix Verification (Phase 6, fix cycle 1)

**Status:** Complete
**Date:** 2026-11-08
**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Fix authorization:** false
**Phase:** fix-cycle (Gate 3, report validation), fix cycle 1
**Report under review:** `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md` (1795 lines, read in full)
**Inputs read:** `qa/qa-consolidated-findings-phase6.md` (BLOCKING_COUNT 18), `qa/qa-fix-log-phase6-cycle1.md`

---

## Check (a): each Blocking = yes row re-checked in the cited report section

Report line numbers are lines of the current report. "Re-verified" means I ran the Grep/Read/WebFetch named.

| Row | Finding | Result | Evidence |
|---|---|---|---|
| 1 | Claude Code pin never stated | FIXED | Read `Dockerfile.coder:110` = `npm install -g @anthropic-ai/claude-code@2.1.289`. Report now states the pin with citation at L609 (SC-12), L660 (G-01), L775 (5.1), L832 (W01-12), L964, L984, L1094, L1332, L1517 (4D.3), L1705 (row 15), L1771; 2.1.319 and drift marked UNVERIFIED. Grep for "version is not established" style residuals: none left (L852 "not established" is about `ANTHROPIC_BASE_URL`). |
| 2 | Managed skill path "not established" | FIXED | WebFetch of https://code.claude.com/docs/en/skills returned both quotes (Enterprise row `.claude/skills/<skill-name>/SKILL.md` in the managed settings directory; "Remove a skill" example `/etc/claude-code/.claude/skills/<skill-name>/` on Linux). Report L1208, L1215, L1258, L1345, L1691 now say "documented path, doc-only, not observed". Grep for "path UNVERIFIED / not stated in the text": no match. `Dockerfile.coder:473-475` and `test-73:102-114` read; the claim that test-73 pins the form of the `install -d` RUN is correct (see note N-1 for one imprecision). |
| 3 | B2 risk omits R4 | FIXED | L1088 (B2 = R2, R4, R5 as written; "Still High (R2 and R4) if the zero-layer fold holds"), L1228 (Table 1), L1302 (Not recommended), rubric L1005 R4 definition. Consistent with L1092 Cons and K-09 (L629). |
| 4 | Effort S contradicts Section 8 | NOT FULLY FIXED | B3 (L1087, L1227), D3 (L1137, L1227) and C (L1112, L1227) re-rated M "as planned" and Section 7 Stage 1 Why (L1299) updated. D2 is not: L1137 and L1227 still say "S (4 files)". Section 8 builds D2 (Phase 4 table L1476 "4D with D2"; step 4D.6 L1520), and steps 5.3 (new `test-80` file plus driver-table row in `coder-ci-aidev02-contract.yml`) and 5.4 (second-file check in `test-73`) apply to it. By the rubric (L1004-1005: M = 5 to 7 files or 2 to 3 amended or new tests) D2 as planned is M, the same defect the row names. See finding F-1. |
| 5 | L1356 vs Phase 4 table / Section 9 row 4 | FIXED | L1355 now blocks only (no, named bootstrap skill) and sends (no, session) to 4D with D2; matches Phase 4 table L1474-1476, Limits row 3 L1333, Dependence rows L1345-1347, Section 9 rows 3 and 4 (L1693-1694, "not feasible" now applies only to the "available globally" part). |
| 6 | "Phases 1-3 and 5-7 do not depend on answers" | FIXED | L1357 and L1280 reworded; consistent with Phase 3 Dependencies (L1452), Phase 5 "Which steps apply" (L1526), step 6.7 (L1600), Phase 7 (L1611-1613). |
| 7 | 9.1 and row 16 say no plan step rests on the register | FIXED | L1713 now maps G-01..G-04, G-08, G-09, G-13, G-21, G-19 to steps; row 16 (L1706) names R-1, R-3, R-10 as bounds. Consistent with steps 3.1, 3.2, 3.3, 3.4, 4C.3 read at L1456-1459 and L1507. |
| 8 | Phase 4 gate had no procedure | FIXED (note N-2) | L1478-1488 now give who/where, how, three facts with pass/fail, evidence location and rule. Precedent verified: `coder-ci-orca-proof.yml` lines 1-15 (name "Coder Orca In-Session Proof", boots one `orca` workspace on dind-sidecar, one model call, `incomplete` turns the job red), job `orca_proof` at :225, `claude -p` rows at :557-:598. Section 7 Stage 2 (L1300), checklist L1669 and L1681, row 15 (L1705) point to it. |
| 9 | SC-02/SC-03 had no asserting step | FIXED | Step 3.3 (L1458) checks manifest and `config.toml` after install; step 5.3 case (a) (L1534) asserts both and `P/.claude/skills/bmad-*` count = `<N>`. Grep of `_config-driven.js:479`: `configured: ${count} skills` exists (arrow is a unicode arrow, cosmetic). |
| 10 | R-10/R-11 not produced by any test case | FIXED | Step 5.3 cases (h) and (i) (L1534); checklist L1675 and L1681 list R-10/R-11 by (h),(i) and make R-9 conditional as step 6.7 (L1600) does. |
| 11 | Step 4C.3 plans late-COPY helper but rating is in-place | FIXED | L1507 says so and gives the two ratings; SC-14 (L611), Table 1 Risk and Layers (L1228, L1235) and Section 7 Stage 1 (L1299) agree; heading L1501 renamed. |
| 12 | L416 says OD-1 label is for other matters at `test-57:10` and `startup.sh:1114` | FIXED | Re-ran Grep: `test-57:10` "(bmad excluded, OD-1)", `:992` and `:1034` "owner OD-1 = A"; `startup.sh` has no "OD-1" and `:1114` reads "BMad is an explicit owner-decision exception". L415 of the report now says exactly this and agrees with G-23 (L682), step 5.6 (L1537) and Table 5.1 (L1543). |
| 13 | Step 1.3 told implementer to find the re-derive procedure | FIXED | `.claude/skills/bmad-spec/SKILL.md` read: L46, L54, L56 (derived, single writer) and L66 (memlog is authority, next unused `CAP-N`) support L1385. Residual unobserved part kept UNVERIFIED (Section 9 row 19). |
| 14 | Step 1.1 hand-edited memlog and `updated:` | FIXED | `_bmad/scripts/memlog.py:116-119` (`touch` stamps `updated`) and `:206-211` (`append --workspace --text --type`) read; `SKILL.md:58-61` prescribes the same form; `.memlog.md:31,34` are `(event)` re-derive bullets and `:27` the void decision, as L1383 says. Step 1.1 now uses three `memlog.py append` calls. |
| 15 | Steps 1.2/1.4/1.5 hand-edit derived files | FIXED | `SPEC.md:3-8` lists `fr-audit.md` and `owner-decisions.md` under `companions:`; L1384, L1386, L1387 state derived versus hand-kept per file and draft the OD-4 row; spec-authored status kept UNVERIFIED (row 19). |
| 16 | Stage 0 under the CLI reading had no destination for Phase 3 | FIXED | Phase 3 header (L1452) names the CAP-8 success text plus `(constraint)` memlog bullets as the record; Stage 0 (c) (L1298) and step 1.1 (L1383) carry the same pointer. |
| 17 | Steps 6.3/6.5 named a workflow that cannot gate a PR and "not recorded" notes | FIXED | Re-ran Grep: `upstream-monitor.yml` triggers `schedule` :17, `workflow_dispatch` :20, guard `if: github.ref == 'refs/heads/main'` :40, `health.py` with `expected.txt` :160-163; `coder-ci-aidev02-contract.yml` step "T78: upstream monitor (runner-native)" :822-826 inside `contract_tests` :492; `coder-ci-orca-boot.yml` job `orca_boot` :141, step :253, command :265; `coder-ci-validate.yml` `workflow_call` :5, job `validate` :61, `test-startup-boot` at :276-277, :301, :912, :1085; `coder-template-main.yml` calls it at :392 and :409. Report L1405, L1596-1598, L1680 match. |
| 21 (override) | Scaffolding in the report | FIXED | Grep for `Scope of this file`, `UNVERIFIED here`, `S01..S04`, `plan brief`, `synth-0` in report body: only Section 10 evidence-trail rows (L1777-1780, L1793) remain, which is correct; "the task file" is now in the Evidence Trail (L1760). Remaining "this synthesis" at L684 and L689 is a MINOR wording leftover (note N-3). |

Fixed: 17 of 18 rows fully, 1 row (4) not fully.

## Check (b): new blocking issues introduced by the fixes

| Category | Result | Evidence |
|---|---|---|
| New false claims | None blocking | Every new factual claim in the fix text was re-checked against its source (rows 1, 2, 8, 9, 12, 13, 14, 15, 17 above). One imprecision: N-1. |
| Broken tables | None | New Phase 4 gate table (L1480-1488, two columns), step 5.3 and 1.1-1.5 cells (escaped `\|` only inside code), Section 9 row 19 (L1709) all have the right column count; no stray raw pipe found while reading L1381-1390, L1480-1488, L1534, L1709. |
| Placeholders | None | Grep (case-insensitive) for TODO, TBD, FIXME, XXX over the report: no hit. |
| Stale Table of Contents | None | ToC (L10-55) entries all match headings: Sections 1-10 at L59, L74, L547, L634, L767, L986, L1276, L1351, L1685, L1746; sub-sections 2.1-2.6, 3.1-3.3, 4.1-4.5, 5.1-5.3, 6.0, 7 sub-headings, Phases 1-7, 9.1 present. Fixes added no new `##`/`###` heading. |
| Hallucinated paths | None | Glob confirmed `.github/workflows/{markdownlint,upstream-monitor,coder-ci-orca-proof,coder-ci-orca-boot,coder-ci-validate,coder-template-main}.yml`, `_bmad-output/specs/spec-orca-catalogue-bundle/{SPEC.md,.memlog.md,slug-configuration.md}`, `epics-orca-gap-closure.md`, `ARCHITECTURE-SPINE.md` (gap-closure folder), `_bmad/scripts/memlog.py`, `.claude/skills/bmad-spec/SKILL.md`. |
| Contradictions between sections | One residual (F-1) | Effort rating of D2 versus Section 8 (F-1). Rows 3, 5, 6, 11 cross-checked section by section and now agree (Limits row 3 / Phase 4 table / Section 9 rows 3-4 / L1355; SC-14 / Table 1 / step 4C.3 / Stage 1 / step 6.2). |
| Document-only claim in Sections 2, 6, 7, 8 | None new | New doc-only statements (managed skill path in Option I, Claude Code behaviour in the gate and 4D.3) all carry "[UNVERIFIED - doc-only ...]" or "doc-only" and are not the sole basis of a rating (6.0 tag table L996). Section 2.3 L294 and 2.6 L508 say the Claude Code answers come "from official documentation only, in Section 5". |

## Check (c): 10-section structure

PASS. Headings `## 1.` to `## 10.` present once each, in order (L59, L74, L547, L634, L767, L986, L1276, L1351, L1685, L1746). Section 1 lost the "Scope of this file" bullet and now ends at L72 with the Trigger bullet; no section is empty or placeholder.

## Findings

| # | Severity | Location | Issue | Required fix |
|---|---|---|---|---|
| F-1 | IMPORTANT (blocking; unfixed part of consolidated row 4) | Report L1137 (Option D, D2 Effort), L1227 (Table 1, D2 Effort), L1299 (Section 7 Stage 1 Why: "rated M for B3, D3 and for C") | The fix re-rated B3, D3 and C to M because Section 8 adds new tests, but left D2 at "S (4 files)". Section 8 builds D2 for the (no, session) combination (L1355, L1476, step 4D.6 at L1520) and steps 5.3 (new `test-80-bmad-first-use.sh` plus a driver-table row in `coder-ci-aidev02-contract.yml`) and 5.4 (second-drop-in check in `test-73`) apply to any built Phase 4 branch. Counting the plan's own work, D2 is at least 6 files and 2 new or amended tests; the rubric (L1004-1005) rates that M. The Effort row is cited as a basis of the recommendation (L1299), and L1299 recommends D2 for the session trigger when Q1 is "no". | Re-rate D2 to "M as planned (S on the researched minimum; plan adds the step 5.3 test and the step 5.4 second-file check)" in L1137 and L1227, and add D2 to the L1299 Why sentence. |

Minor notes (not counted as blocking, not required before the next review):

| # | Location | Note |
|---|---|---|
| N-1 | Report L1208 (Option I) | Says the `install -d` RUN at `Dockerfile.coder:473-475` "creates only `/etc/claude-code` and `/etc/claude-code/managed-settings.d`". Read of lines 473-475 shows the same RUN also creates `/var/lib/aidev02` and `/etc/skel/.claude`. The point (no `/etc/claude-code/.claude/skills/...` parents) still holds; say "of the /etc/claude-code tree, creates only ...". |
| N-2 | Report L1478 vs L1482 | The paragraph is headed "Gate before any branch", but fact 1 (stub loaded, hook runs) can only be observed in a candidate template version that already contains the stub or hook (L1482 says so). Checklist L1669, Section 9 row 4 (L1694) and Section 7 Stage 2 say "before B or D is relied on", which is the workable reading. Align the heading wording to "before a branch is relied on or merged". |
| N-3 | Report L684, L689 | "This synthesis uses R01's tag" and "This synthesis uses the corrected reading" are leftover synthesis wording (the same class as row 21, in two cells the fix did not touch). |
| N-4 | Fix log, Row 1 entry | States the `/add-dir` v2.1.257 gate "does not appear in the report"; it does, at W01-4 (report L791). No report defect (2.1.257 is below the 2.1.289 pin); the log sentence is wrong. |
| N-5 | Report L1383 | "`updated:` changed by the script, no existing line changed" reads as a contradiction (line 3 is rewritten by the script); say "no existing bullet changed". |

## Counts

- Blocking rows in the consolidated findings: 18 (rows 1-17 and 21).
- Verified fixed: 17. Not fully fixed: 1 (row 4, D2 part).
- New blocking issues introduced by the fixes: 0 (F-1 is the unfixed part of row 4, counted once).
- CRITICAL 0, IMPORTANT 1 (F-1), MINOR 5 (N-1 to N-5).
- MINOR rows of the consolidated findings (18 to 69 other than 21) were not rechecked, as instructed.

## Confidence Gate

Checklist items: 18 blocking rows + 7 check-(b) categories + 1 check-(c) = 26. Verified with tool evidence: 26. Unverifiable: 0. Unchecked: 0.

- **Confidence:** Verified: 26/26 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 25 | Grep: 22 | Glob: 4 | Bash: 0 | WebFetch: 1 (Read + Grep + Glob = 51 against 26 items).
- Limits that no tool call here lifted (all UNVERIFIED by me): the Section 5 external claims (W01, W02) other than the managed-skill path on the skills page (the WebFetch read only the first 100000 of 118986 characters, and both quotes were inside that part); whether `claude -p` can show the three Phase 4 gate facts (the report itself marks it UNVERIFIED); the exact CAP-8 rendering of a `bmad-spec` run; no test or workflow was run.

## Self-Audit

What I actively checked:

- Read all 1795 lines of the report in 12 reads (L1-130, 131-430, 431-660, 661-780, 781-995, 996-1145, 1145-1279, 1276-1385, 1386-1485, 1486-1560, 1561-1680, 1681-1795) and the full consolidated findings (111 lines) and fix log (90 lines).
- Re-ran sources for every row whose fix cites code or a workflow: `Dockerfile.coder` lines 106-111 and 466-477; `test-73` lines 98-118; Greps of `test-57-catalogue-configure.sh` and `startup.sh` for "OD-1" and "owner-decision exception"; `bmad-spec/SKILL.md` lines 40-71; `_bmad/scripts/memlog.py` (touch, append arguments); `SPEC.md` lines 1-14; `.memlog.md` lines 1-35; `coder-ci-orca-proof.yml` lines 1-30 and Grep of its rows; Greps of five workflow files for job names, triggers and line numbers; `_config-driven.js` for the install count string; WebFetch of the skills page for the managed skill path.
- For check (b) I Grepped the report for placeholders and scaffolding strings (TODO/TBD/FIXME/XXX, `Scope of this file`, `UNVERIFIED here`, `S0n`, `plan brief`, `synth-0`, `this synthesis`, `this file`, `the task file`), checked heading lines against the ToC, and Globbed the new paths.
- I did not simply trust the fix log: it has one wrong sentence (N-4), and its Row 4 entry reasons about D1 but never mentions D2, which is how F-1 was found. I then looked for the same pattern elsewhere (B2 risk, C layers, gate timing) and found only the notes above.

Why I believe the count is right: 17 rows reproduce against source; the one failure (F-1) is a direct read of L1137, L1227, L1299 against the rubric at L1004-1005 and the Section 8 steps 4D.6, 5.3 and 5.4. The notes N-1 to N-5 are accurate wording or log defects that change no rating, plan step or conclusion. A zero-finding result was not plausible: the row 4 fix was selective, and I tested for exactly that. What could still hide issues: wording-level contradictions inside the very long Section 8 cells that I read but did not diff against the pre-fix text (there was no pre-fix copy to diff).

## Verdict

**FAIL** - 1 unfixed blocking issue (F-1, row 4: D2 Effort rating, Section 6 L1137 and L1227, Section 7 L1299). No new blocking issue was introduced. After F-1 is fixed, the other 17 blocking rows need no further change.

Status: Complete

## QA Complete
