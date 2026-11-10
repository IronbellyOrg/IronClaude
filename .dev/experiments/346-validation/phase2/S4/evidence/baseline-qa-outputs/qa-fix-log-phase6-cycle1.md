# QA Fix Log - Gate 3 (report validation), fix cycle 1

**Status:** Complete
**Date:** 2026-11-08
**Report:** `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md`
**Input:** `qa/qa-consolidated-findings-phase6.md` (BLOCKING_COUNT 18)

---

## Entries

### Row 3 (IC#1) - FIXED
- Section 6 Option B Risk row (B2 cell) and Table 1 Risk row (B2): added R4 (section 6 not gated by slug or profile; Option B Pros/Cons already said so), dropped "Medium if fold holds"; B2 is High with or without the fold (R2 + R4).
- Section 7 "Not recommended" B2 text aligned (High even if the fold holds).
- Evidence: rubric (Section 6.0, R4 definition) and the report's own Cons cell "section 6 also runs for `minimal`".

### Row 4 (IC#4) - FIXED
- Re-rated Effort to M "as planned in Section 8" (S on the researched minimum) for B3, D3 and C (new command); reason: Section 8 steps 5.2, 5.3, 5.4 add 2-3 new tests, and the rubric makes 2 to 3 new tests M. Edited Option B (B3 cell), Option C Effort row, Option D (D3 cell), Table 1 Effort row, and the Section 7 Stage 1 "Why" column (states that Risk and Pinned-tests rows, not Effort, separate B3/D3 from B1/D1).
- D1 left at S: Section 8 plans no D1 step, so there is no planned-work contradiction for it (the Table 1 cell now says so).

### Row 11 (CR#8) - FIXED
- Step 4C.3 now says the planned helper is the C late-COPY variant, not the rated in-place variant; its rating is Medium (R4) only if it folds into an existing COPY (UNVERIFIED, U19), High (R4, R5) as its own COPY.
- SC-14 and Table 1 (Risk C) updated to match; Section 7 Stage 1 and Section 8 Plan basis name C with the helper per step 4C.3; branch 4C heading renamed.
- Evidence: Table 1 Image layers row for C (late-COPY 0 if folded UNVERIFIED U19, else +1) and the rubric R5.

### Row 1 (EQ#1) - FIXED
- Re-read `templates/VSCode-AIDev02/image/Dockerfile.coder:108-110` myself: `npm install -g @anthropic-ai/claude-code@2.1.289` at line 110 (Grep and Read).
- Section 5.1 intro, G-01 (4.2), SC-12 status (3.2), Option B "Shared points", Section 7 Limits row 2, step 4D.3, Section 9 row 15 and the Section 10 source-URL note now state the pin with its citation; the 2.1.319 workspace observation and any drift between pin and running image are marked UNVERIFIED; the residual is narrowed to "does the doc-described behaviour hold at the pinned version". `reloadSkills` text now says the 2.1.152 figure (user-authored issue) is below the pin. The `/add-dir` v2.1.257 gate does not appear in the report, so nothing to change there.

### Row 2 (DA#1) - FIXED
- Re-fetched https://code.claude.com/docs/en/skills (WebFetch, small-model summary): Enterprise row = `.claude/skills/<skill-name>/SKILL.md` in the managed settings directory; "Remove a skill" example = `/etc/claude-code/.claude/skills/<skill-name>/` on Linux. Both quoted in the fetch result.
- Option I description, Effort-adjacent cost text (own COPY plus parent directories; the `install -d` RUN at `Dockerfile.coder:473-475` read by me creates only `/etc/claude-code` and `managed-settings.d`; `test-73:102-114` pins the RUN form, noted as not run), Files row, Table 2 Risk and snapshot rows, Section 7 Dependence row 3 and Section 9 row 1 now say "documented path (doc-only, not observed in the image)".

### Row 5 (IC#2, CR#4, CR#14) - FIXED
- Section 8 intro "Feasibility and branch": names only (no, named bootstrap skill) as BLOCKED; (no, session) proceeds as 4D with D2 under the doc-only caveat (matches Phase 4 table rows for (no, skill) and (no, session) which I re-read). One wording, "not supported by code-traced evidence; owner decides", now used in Section 7 Limits row 3, Section 8 intro and Section 9 row 4 (which no longer says "not feasible" for row 3 (no, b)).

### Row 6 (IC#3, CR#3) - FIXED
- Section 8 intro "What is not decided" now says: Phases 1 and 2, steps 5.1 and 5.6 and steps 6.1 to 6.6 do not depend on Q1/Q2; Phase 3 needs Section 9 rows 5 and 6 and is a shipped block only if a branch is built; steps 5.2 to 5.5, 6.7 and 7.3 to 7.5 follow the chosen branch. Section 7 "Recommended approach" sentence ("only the last step waits for the owner") replaced with the same facts (Stage 0 item (c) states plan defaults; Stages 1 and 2 follow the owner-selected branch).
- Evidence: re-read Phase 3 Dependencies, Phase 5 "Which steps apply", step 6.7 and Phase 7 steps in the report.

### Row 7 (CR#1) - FIXED
- Section 9.1 intro: replaced "No plan step rests on any item in this table" with the true mapping (G-01 to G-04 and G-08 to steps 4B.2-4B.4, 4D.3-4D.4 and the Phase 4 gate; G-09 to step 3.1 `timeout 120` and 4D.3; G-13 to steps 3.2-3.3; G-21 to step 3.4 Variant H; G-19 to step 4C.3). Section 9 row 16 sentence "None is a basis of a plan step" replaced with the R-1, R-3, R-10 bounds. Evidence: re-read steps 3.1, 3.2, 3.3, 3.4, 4C.3 and row 15.

### Row 8 (CR#2, AC#5) - FIXED
- The Phase 4 gate had no procedure. Read `.github/workflows/coder-ci-orca-proof.yml` (header lines 1-15, driver rows near 660-700): job `orca_proof` boots one `orca` workspace on dind-sidecar and runs one `claude -p` call, rows `pass` only when observed, otherwise `incomplete` (job red). Wrote a procedure table (who, where, how, three facts with pass/fail, evidence location, rule) into the Phase 4 gate; it names the precedent and says that whether `claude -p` can show each fact is UNVERIFIED, with an operator-driven interactive session and saved transcript as the labelled fallback (the trust hold-back is interactive-only per W01-18 and not exercised by `-p`: stated as UNVERIFIED).
- Section 7 Stage 2, the Integration Checklist (gate item and the R-7/R-8 item), Section 9 row 15 and step 6.7 now point to that procedure.

### Row 9 (CR#6) - FIXED
- Step 3.3 now checks `_bmad/_config/manifest.yaml` and `_bmad/config.toml` after the install (SC-02); step 5.3 case (a) now asserts both files and that the count of `P/.claude/skills/bmad-*` equals the `<N>` of the installer's `Claude Code configured: <N> skills` line (SC-03). The format of that line is the report's own CODE-VERIFIED string (`_config-driven.js:477-479`, Section 2.3), not re-read by me.

### Row 10 (CR#7) - FIXED
- Step 5.3 gained observation-only cases (h) (R-10: half-written `_bmad/`, run the step 3.1 command directly and record exit code and tree) and (i) (R-11: documented manual command form of `manifest.yaml:13-14`). The Integration Checklist item now lists R-10 and R-11 (by cases (h), (i)) and makes R-9 conditional as step 6.7 does; checklist case range updated to (a) to (i).

### Row 12 (CR#9, DA#5) - FIXED
- Grep of `.github/contract-tests/test-57-catalogue-configure.sh` for "OD-1": line 10 "(bmad excluded, OD-1)" is the BMad reference; lines 992 and 1034 ("owner OD-1 = A") are other matters. Grep of `templates/VSCode-AIDev02/image/scripts/startup.sh` for "OD-1": no match; I read lines 1112-1117: line 1114 says "BMad is an explicit owner-decision exception" with no label.
- Section 2.5 decision-trail paragraph rewritten to say exactly that, so it now agrees with G-23, step 5.6 and Table 5.1 (which edit `test-57:10`).

### Row 13 (AC#1) - FIXED
- Read `.claude/skills/bmad-spec/SKILL.md:30-89` and `_bmad/scripts/memlog.py:1-150`. Step 1.3 now names the mechanism: run `bmad-spec` on the gap-closure folder in update mode (`SKILL.md:66`: memlog is the authority, next unused CAP-N), SPEC.md derived and never hand-edited (`SKILL.md:46, 54, 56`); UNVERIFIED tag replaced by what was read, and the unobserved part (the run's output) stays UNVERIFIED and goes to Section 9 row 19.

### Row 14 (AC#2) - FIXED
- `memlog.py:116-119` (`touch`) stamps `updated` on every write, so the manual bump was wrong. Step 1.1 rewritten as `uv run _bmad/scripts/memlog.py append --workspace ... --type <decision|capability|event> --text ...` (form from `SKILL.md:58-61`): three appends (decision, capability CAP-8, event after the re-derive); manual `updated:` bump and the "only change" claim removed. Register row, Integration Checklist item 1 updated to match. Earlier re-derives logged as `(event)` confirmed in `.memlog.md:31,34` (read).

### Row 15 (AC#3) - FIXED
- `SPEC.md:3-8` (read) lists `fr-audit.md` and `owner-decisions.md` under `companions:`; `SKILL.md:54, 56` says spec-authored companions are derived on each run and hand edits are overwritten. Steps 1.2, 1.4, 1.5 now state per file whether it is a derived companion (changed via memlog plus a `bmad-spec` run) or a hand-kept record (sprint-status, epics, architecture spine: not derived by bmad-spec), and step 1.2 drafts the exact OD-4 row and the OD-1 pointer. Catalogue-bundle SPEC lines now go through its memlog and a `bmad-spec` update (the folder has a `.memlog.md`, Glob); whether that SPEC was produced by `bmad-spec` and whether the two companions are spec-authored stay UNVERIFIED (Section 9 row 19). Register and checklist rows aligned.

### Row 16 (AC#4) - FIXED
- Phase 3 header now names the destination under the CLI reading: the CAP-8 success text (command of step 3.1, predicate of step 3.2) plus `(constraint)` memlog bullets for steps 3.3, 3.4, 3.6, written through `memlog.py` (step 1.1) and rendered into SPEC.md by the step 1.3 run; no product file. Section 7 Stage 0 (c) and step 1.1 carry the same pointer.

### Row 17 (AC#6, DA#9) - FIXED
- Grep of `.github/workflows/upstream-monitor.yml`: triggers `schedule` (:17) and `workflow_dispatch` (:20) only; job guard `if: github.ref == 'refs/heads/main'` (:40). Read `coder-ci-aidev02-contract.yml:818-826`: step "T78: upstream monitor (runner-native)" runs `test-78-upstream-monitor.sh`; Grep puts it in job `contract_tests` (:492, next job :1474). Grep of `coder-ci-orca-boot.yml`: job `orca_boot` (:141), step "Orca boot gate (test-startup-boot.sh)" (:253, command :265). Grep of `coder-ci-validate.yml`: only trigger `workflow_call` (:5), job `validate` (:61); `coder-template-main.yml` calls it at :392 and :409.
- Steps 6.3 and 6.5 rewritten (6.5 = the T78 step as the PR gate, `upstream-monitor.yml` as post-merge only); both "not recorded [UNVERIFIED]" notes dropped; step 2.7 Files cell and the Integration Checklist "Workflows green" item aligned.

### Row 21 (TC#1, TC#2, TC#6, IC#15, CR#15; orchestrator-raised to IMPORTANT) - FIXED
- Deleted the "Scope of this file" bullet (Section 1); L295 now says the Claude Code questions are answered from official documentation in Section 5; "UNVERIFIED here", "this file frames", "this synthesis's own rubric", "No rating ... in this file" and "this synthesis" rewritten; the S02/S03 labels and the `synthesis/synth-03-...` path in Sections 7 to 9 replaced by section names; "(this file)" and "the plan brief" removed (the (v)(1) to (v)(3) sentence now describes the three checks without naming a source I could not find; BUILD-REQUEST.md has no such list); the task file is now listed in the Evidence Trail "Also read" paragraph (its lines 159 and 164 contain the owner-question section and the "slash skill" wording, checked by Grep). Verified by Grep that no `S01-S04`, `UNVERIFIED here` or "Scope of this file" strings remain.
- Citation-format rows (22, 23) were not touched.

### Section 9 row 19 (added)
- New row listing the plan-level unknowns created by these fixes (spec-authored status of the two companions, outcome of the bmad-spec runs, next free test number, live-boot ledger row, whether `claude -p` can show the gate facts); the Section 9 intro now says rows 15 to 19.

## Constraints kept
- Q1 and Q2 remain unanswered; no owner decision invented. All `[synthesis inference: ...]` labels untouched. Feasibility statement unchanged in Sections 7 and 9 (only the "not feasible" versus "not supported by code-traced evidence" wording for the (no, b) combination was aligned). Only the report and this log were edited. No MINOR row was acted on except where the same sentence was already being corrected for a blocking row (rows 12 and 21 folds, wording only).

## Counts
- Blocking rows in input: 18 (rows 1-17 and 21).
- Fixes applied: 18.
- Findings not fixed: 0.
- Fixed plus not fixed = 18 = BLOCKING_COUNT.
- Unobserved items left UNVERIFIED: whether `claude -p` can show the Phase 4 gate facts; that a `bmad-spec` run renders CAP-8 and the OD-4 row as drafted; whether `owner-decisions.md` and `fr-audit.md` are spec-authored; whether the catalogue-bundle SPEC came from `bmad-spec`; the Claude Code version that actually runs versus the 2.1.289 pin; the managed-skill path in the image (doc-only).
