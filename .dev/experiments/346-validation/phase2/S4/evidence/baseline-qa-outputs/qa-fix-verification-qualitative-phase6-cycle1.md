# QA Report - Fix Verification (qualitative) - Phase 6, cycle 1

**Topic:** BMAD first-use directory creation in a project that never had BMAD
**Status:** Complete
**Date:** 2026-11-08
**Phase:** fix-cycle (report-qualitative lens), fix_authorization: false
**Fix cycle:** 1
**Inputs:** `qa/qa-consolidated-findings-phase6.md` (BLOCKING_COUNT 18), `qa/qa-fix-log-phase6-cycle1.md`, `RESEARCH-REPORT-bmad-first-use.md` (1795 lines now)

---

## Part A - The 18 blocking rows (check a): resolved by substance or by wording?

Method: for each row I re-read the edited place in the report and, where the fix cites code, a workflow, the docs or the memlog tooling, I re-read that source myself. "PASS" means the original defect is gone in substance. New defects the fixes caused or exposed are in Part B.

| Row | Lens | Result | Evidence (what I read) |
|---|---|---|---|
| 1 | EQ#1 pin | PASS | `Dockerfile.coder:110` Grep: `npm install -g @anthropic-ai/claude-code@2.1.289`. Report states pin with citation at L609 (SC-12), L660 (G-01), L775 (5.1), L832, L964, L984, L1094, L1332, L1517, L1705, L1771. Residual is now "does the documented behaviour hold at the pin"; 2.1.319 and pin drift are marked UNVERIFIED (L775, L1705). Not overstated: L775 still says docs mention versions up to v2.1.314, above the pin. |
| 2 | DA#1 managed path | PASS | WebFetch of https://code.claude.com/docs/en/skills (first 100000 chars): Enterprise row = `.claude/skills/<skill-name>/SKILL.md` in the managed settings directory; "Remove a skill" example = `/etc/claude-code/.claude/skills/<skill-name>/` on Linux. Report L1208, L1215, L1248, L1258, L1345, L1691 now say "documented path, doc-only, not observed in the image". Grep for "path UNVERIFIED" and "not stated in the text": no match left. `Dockerfile.coder:473-475` read: the `install -d` RUN creates only `/etc/claude-code` and `managed-settings.d`, as L1208 says. |
| 3 | IC#1 B2 risk | PASS | L1088 and L1228: B2 = R2, R4, and R5 as written; still High (R2, R4) if the fold holds. L1302 aligned. Matches rubric L1005 (R4 = image-wide, not slug-gated) and B2's own Cons L1092 ("section 6 also runs for `minimal`"). |
| 4 | IC#4 effort | PASS on the original defect; see B-3 and B-4 for what the re-rating exposed | B3, D3, C re-rated M "as planned" (L1087, L1112, L1137, L1227); counts match steps 5.2-5.4 (2, 3 and 2 new tests; rubric L1004: M = 2 to 3 tests). D1 left S with the stated reason (no D1 step in Section 8). |
| 5 | IC#2, CR#4, CR#14 | PASS | L1355 now blocks only (no, named skill) and sends (no, session) to 4D with D2, matching Phase 4 table L1474-1476. One wording ("not supported by code-traced evidence; owner decides") at L1333, L1355 and L1694. Row 4 of Section 9 no longer says "not feasible" for (no, b). |
| 6 | IC#3, CR#3 | PASS | L1357 and L1280 now list which steps wait: Phase 3 needs rows 5 and 6; steps 5.2-5.5, 6.7, 7.3-7.5 follow the chosen branch. Matches L1452, L1526, L1600, L1611-1613. |
| 7 | CR#1 | PASS | L1713 (9.1 intro) now maps G-01 to G-04, G-08, G-09, G-13, G-21, G-19 to steps 3.1, 3.2, 3.3, 3.4, 4B.2-4B.4, 4C.3, 4D.3-4D.4. Row 16 (L1706) names R-1, R-3, R-10 as bounds. Contradiction gone. |
| 8 | CR#2, AC#5 | PASS on "no procedure"; ordering defect remains, see B-1 | Phase 4 gate now has a who/where/how/fact/evidence/rule table (L1480-1488). Precedent verified: `coder-ci-orca-proof.yml` job `orca_proof` (L225), header L1-15 ("a row is `pass` only when observed; anything else is `incomplete` and the job is red"), `claude -p` driver rows at L689-697, red on any incomplete row at L779-795. |
| 9 | CR#6 | PASS | Step 3.3 (L1458) checks manifest and `config.toml`; step 5.3 case (a) (L1534) asserts both files and skill count == installer `<N>`. Installer string verified: `_config-driven.js:479` prints `${this.name} configured: ${count} skills`, and `platform-codes.yaml:53` names claude-code "Claude Code". |
| 10 | CR#7 | PASS | Step 5.3 cases (h) (R-10) and (i) (R-11) at L1534; checklist L1681 lists R-10 and R-11 by case and makes R-9 conditional, as step 6.7 (L1600) does. |
| 11 | CR#8 | PASS | Step 4C.3 (L1507) now says the helper is the late-COPY variant, Medium (R4) only if folded (UNVERIFIED, U19), High (R4, R5) as own COPY; SC-14 (L611) and Table 1 (L1228, L1235) agree; Plan basis (L1353) names the helper. |
| 12 | CR#9, DA#5 | PASS | `test-57-catalogue-configure.sh` Grep: line 10 "(bmad excluded, OD-1)", lines 992 and 1034 "owner OD-1 = A". `startup.sh:1114` read: "BMad is an explicit owner-decision exception", no label. L416 now says exactly this and agrees with G-23 (L682), step 5.6 (L1537) and Table 5.1 (L1543). |
| 13 | AC#1 | PASS | `bmad-spec/SKILL.md` read at 46, 54, 56, 58-61, 66: SPEC.md is derived, memlog is authority on CAP IDs, new capabilities get next unused CAP-N. Step 1.3 (L1385) names this mechanism and keeps the unobserved part UNVERIFIED (Section 9 row 19). |
| 14 | AC#2 | PASS | `memlog.py` read: `touch()` stamps `updated` (L116-119) and `cmd_append` calls it (L174), so the manual bump was wrong; `--type` is free text (L209) so decision, capability, event, constraint, note all work. Existing re-derives are `(event)` at `.memlog.md:31,34`. Step 1.1 (L1383) is now three `memlog.py append` calls and no manual bump. |
| 15 | AC#3 | PASS | `SPEC.md:3-8` read: `fr-audit.md` and `owner-decisions.md` are listed under `companions:`; `SKILL.md:54,56` read. Steps 1.2, 1.4, 1.5 (L1384-1387) state derived versus hand-kept per file and draft the OD-4 row in the `ID | Decision | Consequence` shape of `owner-decisions.md:3-5`. Note `companions:` also lists a PRD and another SPEC, so "listed" does not prove "spec-authored"; the report says so (UNVERIFIED, row 19). |
| 16 | AC#4 | PASS on "no destination"; see B-2 | Phase 3 header (L1452) names the destination under the CLI reading. |
| 17 | AC#6, DA#9 | PASS | Verified myself: `upstream-monitor.yml` `schedule` :17, `workflow_dispatch` :20, `if: github.ref == 'refs/heads/main'` :40; `coder-ci-aidev02-contract.yml` job `contract_tests` :492, step "T78: upstream monitor (runner-native)" :822, command :826, next job :1474; `coder-ci-orca-boot.yml` job `orca_boot` :141, step :253, command :265; `coder-ci-validate.yml` `workflow_call` :5, job `validate` :61, `test-startup-boot.sh` at :276-277, :301, :912, :1085; `coder-template-main.yml` `uses: ./.github/workflows/coder-ci-validate.yml` at :392 and :409. Steps 6.3 and 6.5 (L1596, L1598) match. |
| 21 | TC/IC/CR scaffolding | PASS | Grep for "Scope of this file", "this synthesis", "UNVERIFIED here", "this file frames", "(this file)", "plan brief", S01-S04: no match. Remaining "synthesis" strings are the intended `[synthesis inference]` labels and the Section 10 file table. L294-295 now says the Claude Code questions are answered from documentation in Section 5. Task file is in the Evidence Trail (L1760). |

## Part B - New or remaining defects after the fixes (check b: claims stronger than evidence, recommendation / plan / gap table consistency)

### B-1 IMPORTANT (blocking) - Phase 4 gate cannot be run in the order the report states (exposed by the row 8 fix)

- L1477 (Phase 4): "**Gate before any branch:** ... They must be observed, not assumed." L1463 heading: no branch starts before rows 1 and 2 are answered.
- The new procedure (L1482-1484) observes the facts "in a workspace booted from the candidate template version" of "the chosen branch", and Fact 1 needs the stub (B) or the hook plus the Phase 3 block (D) to exist. A stub or hook cannot be observed before any branch is built.
- Section 7 Stage 2 (L1300) puts the same observation after building ("Only if a Phase 4 branch is built ... Observe the Claude Code facts"); the checklist (L1669) says "observed before B or D is relied on"; step 4D.3 (L1517) says it uses the field only if "the Phase 4 gate confirms it", which is inside branch 4D. Four places, two orders.
- Why it matters: the original finding was that the gate's failure branch was unreachable by following the plan. It is now reachable only by choosing one of the two orders, and the heading picks the one that cannot be done.
- Required fix: reword L1477 to "Gate before relying on any branch: observed on the candidate build of the chosen branch (steps 4B.1-4B.2 or 4D.1-4D.3 drafted, not shipped)"; say in the Rule row that a failed fact 1 discards that draft; make Section 7 Stage 2, L1669 and L1463 use the same words.

### B-2 IMPORTANT (blocking) - the row 16 fix records unanswered owner questions as canonical `(constraint)` memlog bullets (L1452, L1383)

- L1452 says that under the CLI reading the specification is recorded through `(constraint)` bullets for "the broken-install rule and failure ceiling (step 3.3), the git rule (step 3.4) and the prohibitions (step 3.6)", and the CAP-8 success text carries the command and FIRST_USE(P) (L1383).
- But the git rule is open (step 3.4 L1459: "The owner has not decided (G-26, D-10, Section 9 row 5)"), the subfolder rule and bare-`_bmad/` guard are open (Section 9 rows 6 and 10; Stage 0 (c) L1298: "plan defaults, not settled decisions"). Section 9 L1687 says nothing there is answered by the author.
- The memlog is the decision-of-record and append-only (`SKILL.md:54`, `memlog.py:164-177` has no edit or delete; step 7.1 L1609 reverses only by superseding). `constraint` is also the type of settled lines such as `.memlog.md:17-19`. An implementer following L1452 writes the author's defaults into the owner's record as constraints. Phase 1 Dependencies (L1377) forbids this only for the Q1 and Q2 wording.
- Required fix: in L1452 and step 1.1, record the open items as `--type assumption` ("plan default pending owner, Section 9 rows 5, 6, 10") and `--type question` for the owner inputs; keep `--type constraint` only for the fixed prohibitions of step 3.6. State in the CAP-8 success text that the command and predicate are defaults until rows 5, 6 and 10 are answered. (`SKILL.md:61` lists assumption and question as valid types.)

### B-3 IMPORTANT (blocking) - Rationale 4 and Option B Pros call B3 "cheapest" on the Effort row that the row 4 fix now rates worse than B1 (L1311, L1091 versus L1087, L1227)

- After the fix, Effort is B1 S, B3 M ("as planned") in Option B (L1087) and Table 1 (L1227). Rationale 4 (L1311) still says "B3 is cheapest and least exposed" and lists "Effort" first among the comparison rows it rests on; Option B Pros (L1091) says "Cheapest". The Stage 1 "Why" cell (L1299) now says Effort does not separate B3 from B1 ("the Risk and Pinned-tests rows, not Effort, are what separate B3 and D3 from B1 and D1").
- The report therefore both cites and disclaims the Effort row for the same ranking. A contradiction between rows that support the recommendation is never minor.
- Required fix: in L1091 and L1311 replace "cheapest" by "lowest risk (no certain break, 0 layers)" and drop "Effort" from the rows Rationale 4 rests on, or state "S on the researched minimum, equal to B1".

### B-4 IMPORTANT (blocking) - "template push only" for B3 and D3 contradicts the plan's own B3/D3 files and the rubric's L rule (L1083, L1091, L1234, L1311, L1615 versus L1087, L1137, L1499, L1521, L1403, L1610, L1004)

- The row 4 fix now lists `manifest.yaml` and `README.md` as B3 and D3 product files (L1087, L1137); steps 4B.6 (L1499) and 4D.7 (L1521) edit `image/catalogue/bmad/manifest.yaml`. Step 2.5 (L1403) and step 7.2 (L1610) say any edit under `image/catalogue/` changes `catalogue_sha256` (`main.tf:74`), retags the image and needs `coder update`; Option A (L1234) says "rebuild if the welcome text changes".
- Yet Table 1 (L1234) says "Template push only" for B3 and D3, the variant table (L1083) says "template push only", Rationale 4 (L1311) leads with it, and step 7.7 (L1615) calls 4B and 4D (D3) "template-push changes". The rubric (L1004) defines L as "two delivery layers (image and Terraform)"; B3 and D3 as planned touch both, so by the report's own rubric they are L, not M.
- This is the main stated advantage of the recommended option, and the plan does not deliver it as written (the welcome-text sentence is mandatory in 4B.6 and 4D.7).
- Required fix: state in L1083, L1234, L1311 and L1615 that the resource is a template push but the required welcome-text sentence retags the image, or move the welcome-text sentence to a separate image release and say B3 and D3 are template-push-only without it. Then re-rate Effort by the rubric (L) or state that the manifest edit is counted under Stage 0.

### Notes (MINOR, not counted)

- N-1: the fix log (Row 1) says the `/add-dir` v2.1.257 gate "does not appear in the report"; it does, in W01-4 at L791 ("after `/add-dir` (v2.1.257 or later)"). The report text is not wrong (the pin 2.1.289 is above it); only the fix log is inaccurate.
- N-2: step 6.1 (L1594) still quotes `runs-on: [self-hosted, big]`; consolidated row 28 (MINOR) says line 498 is `[self-hosted, "${{ inputs.runner_class || 'big' }}"]`. Not rechecked by design.
- N-3: L1357 says steps 6.1 to 6.6 "do not depend" on the answers; 6.1 (new driver row), 6.2 (layer expectations per branch) and 6.3 (proof for 4B/4C/4D) carry branch-specific text, although each step itself runs under every reading. Wording only.

## Part C - Feasibility statement and the two owner questions (check c)

| Check | Result | Evidence |
|---|---|---|
| Feasibility statement present and unchanged in substance | PASS | Section 7 L1319-1325 still answers "Yes" to both questions with the R01/R03 quotes and "Stop condition: not triggered"; Section 9 row 4 (L1694) restates it. Only the wording for the (no, b) combination was aligned ("not supported by code-traced evidence; owner decides"); that combination was never part of the "Yes" (L1333, L1355, L1694 agree). |
| Q1 and Q2 present, unanswered, correctly worded | PASS | Section 7 L1339 copies Q1 and Q2 "unanswered"; Section 9 rows 1 and 2 (L1691-1692) say "(unanswered)"; Phase 1 step 1.8 (L1390) puts them to the owner; Phase 4 builds nothing before the answers (L1463). No owner decision was invented by the fixes (fix log "Constraints kept" agrees). The task file lines cited for them (L1687 "163 and 164", L1760 "159 to 164") are consistent with the task file Grep (heading at 159, "BMAD slash" wording at 164). |

## Summary

- Part A: 18 of 18 blocking rows resolved in substance (rows 1-17 and 21). No row was closed by wording alone.
- Check (b): FAIL. 4 new or exposed IMPORTANT defects (B-1 to B-4), all in the Section 6 to 8 chain the fixes touched.
- Check (c): PASS.
- Checks passed: 19 / 20 (18 rows + (c); (b) failed). Checks failed: 1.
- Critical issues: 0. IMPORTANT: 4. MINOR notes: 3 (not counted).
- Issues fixed in place: 0 (fix_authorization: false; I edited only this report).
- Trend: 18 blocking in review 1, 4 after cycle 1; the count fell, so no systemic-growth flag.
- Confidence: Verified: 20/20 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% for the 20 scoped checks (the verdict is FAIL regardless, on B-1 to B-4).
- Tool engagement: Read: about 25 | Grep: about 21 | Glob: 0 | Bash: 0 | WebFetch: 1. Reads and Greps exceed the 20 checks.

## Self-Audit

**What I actively checked.**
- Read in full: the consolidated findings (111 lines) and the fix log (90 lines).
- Read in the report (1795 lines): 1-120, 290-298, 405-423, 548-667, 682, 768-778, 995-1797 (Sections 3.1-4.2 start, 5.1 intro, and all of 6 to 10). Not read line by line: 120-290, 423-548, 667-768, 778-995 (2.2-2.5 body, 4.2-4.5 body, Section 5 findings). For those ranges I only ran targeted Greps (pin, enterprise path, scaffolding strings, "not established", `OD-1`, `add-dir`), so a contradiction hidden there is UNVERIFIED.
- Reproduced against sources: `Dockerfile.coder:110` and `:473-475`; `memlog.py:116-119, 164-177, 193-209`; `bmad-spec/SKILL.md:40-79`; `SPEC.md:1-16, 26-82`; `owner-decisions.md`; `.memlog.md:1-34`; `coder-ci-orca-proof.yml` header and driver rows; `upstream-monitor.yml` triggers and guard; `coder-ci-aidev02-contract.yml` job and T78 lines; `coder-ci-orca-boot.yml`; `coder-ci-validate.yml`; `coder-template-main.yml` callers; `test-57` `OD-1` lines; `startup.sh:1110-1118`; installer `_config-driven.js:479`; `platform-codes.yaml:53`; the live docs page for the managed skill path (WebFetch, small-model summary, first 100000 of 118986 characters; the last 18986 were not read).
- About 24 distinct factual claims from the fixes were independently reproduced; none was false except the fix-log aside in N-1.
- Searches that came back empty and prove removal: "Scope of this file", "this synthesis", "UNVERIFIED here", "(this file)", "plan brief", "path UNVERIFIED", "not stated in the text".

**Why the count of 4 is credible.** Every blocking row was traced to the edited line and its source, so a PASS there rests on a reproduced fact, not on the fix log. The four findings are not about whether a fix landed; they are places where a fix made two parts of the report disagree: the gate's order (B-1), what the memlog may hold (B-2), the Effort rows against Rationale 4 (B-3), and "template push only" against the plan's own manifest edit (B-4). Each cites both sides by line. I did not re-run the lenses on MINOR rows 22-69 (out of scope by the prompt), nor any CI job, installer or Claude Code session; whatever depends on those stays UNVERIFIED, as the report itself says.

## Verdict: FAIL

Unresolved or new blocking issues: B-1 (Section 8 Phase 4 gate, L1477 versus L1482-1484 and Section 7 L1300), B-2 (Section 8 Phase 3 header L1452 and step 1.1 L1383), B-3 (Section 7 Rationale 4 L1311 and Section 6 Option B L1091 versus Effort rows L1087, L1227), B-4 (Section 6 L1083, L1234, Section 7 L1311, Section 8 L1615 versus L1087, L1137, L1499, L1521, L1403, L1610 and rubric L1004). CRITICAL 0, IMPORTANT 4, MINOR 0 counted (3 notes).

**Status:** Complete

## QA Complete
