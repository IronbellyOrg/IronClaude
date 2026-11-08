# QA Report - Source-Document Fidelity (fidelity-agent-1)

**Topic:** GitHub issue watcher research (issue 331)
**Status:** Complete
**Date:** 2026-11-07
**Phase:** source-fidelity (Gate 4, fidelity agent 1)
**Fix authorization:** false (report only)

---

## Progress log (appended incrementally)

### Step A: sources read in full
issue.md (100 lines), SKILL.md (155), refs/claim.md (90), origin_repo.py (195 by wc -l), clickup_claim.py (270), WORKER-CONTRACT.md (203), core/CLAUDE.md (136), .claude/settings.json (28), docs/designs/sc-issue-launch-level-hook.md (565), launch-job-identity.sh (566), ccsession-tag/README.md (lines 205-289 and 525-544 read; the rest of its 766 lines grepped on demand). Total assigned lines: 3074 by wc -l (README 766 only partly read). Report: 2176 lines (422 KB), read in chunks.

### Step B: report Sections 1, 2.1-2.5 (report lines 100-575) verified against sources
Claims re-checked by reading source lines (all MATCH unless noted):
- issue.md:24, :37, :43, :18, :45-51, :89-93, :15, :71, :79, :83, :68, :8, :29, :35-41, Activation->Related Commands :87-100: MATCH.
- SKILL.md:17, :52-66, :70, :71, :72, :74, :82-88, :85, :88, :101-117, :130, :133, :134, :135, :145, :146, :150, AskUserQuestion only at line 4 (allowed-tools): MATCH.
- refs/claim.md:9, :13-18, :20, :24-31, :26-30, :37, :39-43, :47-50, :54-60, :78-80, :82-90: MATCH.
- origin_repo.py:14, :25-27, :74, :102-110, :114-124, :126-153, :156-174, :177-191: MATCH; exit codes 1/3/4 MATCH; `owner/repo#N`, `0`, `007` correctly mapped to E-NOT-AN-ISSUE.
- clickup_claim.py:8-19, :74, :76, :148-160, :184, :230-231: MATCH.
- WORKER-CONTRACT.md:11, :16-20, :23 (list quoted exactly), :39, :40, :61, :66, :93, :112: MATCH.
- core/CLAUDE.md L45-53 and README.md:211-226, :228-237, :272, :278, :534-535: MATCH.
- design doc :6, :17, :23, :25-30, :32, :34, :40, :41, :52, :57-58, :71, :77, :186-194, :339-350, :355, :359, :450, :491-506, :547-565: MATCH.
- launch-job-identity.sh (566 lines): line 2 text, fast exit 20-24, governed() 177-186, identify() 215-248, supervise() 291-359, run() 362-398, hook() 414-489, execute() 492-522, non-Bash exit 427-428, invalid sid 430-431, missing session file 435-437, updatedInput without permissionDecision 479-482; script never reads a marker: all MATCH.
- .claude/settings.json: l.1-28, Write|Edit l.4-14, Skill l.15-25, description at l.17, no `permissions` key: MATCH.
- Glob `**/launch-level-guard*` over the worktree: no files (report claim CONFIRMED; guard does not exist).
- Section 1, 1.1, 1.2 addendum fidelity: owner decision A/claim-only/integer-only prompt, Coder#477 boundary and the "filed assuming a push design; A makes #477 unnecessary unless B/C is revisited" statement match research-notes lines 99-112.
### Step C: Sections 3, 4, 6, 7, 8 (report lines 575-750, 990-1830) verified; F1/F2 edits checked
- Sections 3-4 (SC-1..SC-17, G1..G30): every assigned-source citation re-read (claim.md:20/26/41/42/47/54-60/80/88/90, issue.md:15/35-41/45-51/79/83, SKILL.md:74/101-117, origin_repo.py:14/74/102-153, WORKER-CONTRACT.md:11/23/61/93, README.md:534, design doc :17/:23/:34/:40/:339-345): MATCH. G16/G17/G27 and 4.2 "unwired capability" rows are faithful: `--claim --pipeline` and `launch-level-guard.sh` are described as design-only/nonexistent everywhere; no aspirational claim presented as current code (checklist item 5 OK).
- Sections 6-7: owner decision labelled "decided by the owner" in 6.1 heading, 7.1; Grep for "pending owner" found no occurrence (the two hits for "pending"/"not decided" are unrelated: line 498 governance items and line 1200 option C location). Coder#477 boundary text in 7.7 and 8 follow-up table matches ADDENDUM 2 exactly. 7.9 keeps the routing rule, approver list, etc. as OPEN, which the addenda do not settle (faithful: ADDENDUM 2 names no routing candidate).
- F2 edit (Phase 3 step 3.4, `resolve_orca`, `which=None` resolved at call time): checked against the cited code. `install_user_setup.py` read: `_ORCA_CLIS = ("orca-ide", "orca")` at l.35, `_find_orca` l.198-221 (docstring text "On Linux a bare `orca` outside Orca's own terminals is usually the GNOME screen reader" quoted exactly), probe `[path,"skills","list","--json"]` with timeout=10 and stdin=DEVNULL, `except (OSError, subprocess.SubprocessError, ValueError, AttributeError): continue` at l.217-218, acceptance test `returncode == 0 and any(t.get("name") == "orca-cli" ...)` l.219, `_orca_timeout` l.224-227, `install_orca_skills` l.230-263: ALL MATCH. Bash `which -a orca-ide` lists /home/coder/.local/bin/orca-ide (and /usr/bin, /bin); `which -a orca` lists /home/coder/.config/orca/linux-orca-cli-shim/orca and /home/coder/.local/bin/orca: MATCH the report's claim. No remaining `which=shutil.which` default-argument text in the report outside the explanatory note at line 1443 (Grep). The F2 reasoning (a default argument bound at import time ignores a later `shutil.which` patch; `lookup = shutil.which if which is None else which` at call time does not) is correct Python semantics, and the test table (test_cli_once, step 6.2, step 3.6) is consistent with it.
- F1 edit (step 5.1 `considered` map, Phase 5 algorithm step 3/4, new test "Unhandled issues cannot monopolize the cap"): internally consistent (sort: never-examined first, then oldest `considered`, ties by ascending number; stamped in step 4 before any filter decides; walkthrough of the 15+1 issue example gives cycle 1 = issues 1-10, cycle 2 = 11-15, 99 and four stamped ones, so 99 is examined by cycle 2). The precedent citations in these steps check out: init_lite.py `_atomic_write` at l.221, poll-augment-review.sh :47 (fail-incomplete comment), :51 (1000 pages), :53-55 (`--method GET -F per_page=100 -F page`), :69-70 (raw `length` tested `-lt 100`), :74 (`completed` check), main.py :559-561 (reflect block) and :564 (`__main__`), test_conflict_e2e.py:178-186 (`assert_no_retrigger_call`).
- Sections 8.1-8.4 / Phases 1-7 citations of `origin_repo.py` (:66-69 patterns, :74, :77-83, :102-153, :135, :156-174, :177-191), `refs/claim.md` (:20, :26, :29, :41-42, :47, :84-88, :88), core/CLAUDE.md L45-53, README.md:216-223/:228-237, WORKER-CONTRACT.md:112: MATCH (see the :112 wording note below).
- MINOR (accuracy of rule characterization): the report (2.1 line 234, step 1.6, G15) says WORKER-CONTRACT.md:112 requires "the user's instruction in the live conversation" for outward git/GitHub actions. The source says the coordinator acts "only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation": the live conversation only waives the at-the-moment confirmation, and the rule binds the coordinator, not a plain-process poller. The report's conclusion (the contract has no category for a standing authorization by an approver's label) still holds. Wording only.
- MINOR: Phase 4 step 4.5 says the write-shaped token list is "modelled on `assert_no_retrigger_call`"; the real helper (test_conflict_e2e.py:185) also treats ANY `--method` as write-shaped, whereas the plan allows `--method GET`. The report states its own rule explicitly (read rule (4)) so this is a stated adaptation, not a distortion.
- MINOR notes (cosmetic): report says origin_repo.py is "196 lines" (wc -l: 195); report cites design front matter `planning_status` at ":9-10" (it is line 10; line 9 is historical_convergence); identify() cited 215-247 (function closes at 248). Cosmetic, not blocking.

### Step D: Sections 5, 9, 10, Appendix A and addendum fidelity
- Section 9.1 (D1-D6) restates ADDENDUM 2 exactly (A, claim-only, integer-only, repo-side deliverable, Coder#477 "filed assuming a push design; option A makes #477 unnecessary unless ... revisited", listener/registration/transport in the Coder repo, B/C and live deployment as follow-up). Section 7.1 and 6.1 heading say "decided by the owner (ADDENDUM 2)"; no "pending owner decision" wording exists anywhere (Grep). Section 1.2 states the boundary and the "spec must record this statement" sentence. Tally in Requirement Scoring (A 2, B 1, C 0, D 2) matches the cell contents (counted cell by cell).
- Section 9.2 Q34/Q35 source cites (`clickup_claim.py:8-19`, `SKILL.md:133`, `claim.md:26,:28,:47`) MATCH. Q21 is labelled inference (SKILL.md:88) honestly.
- Section 2.3 main.py registration list (519-561; sprint 521 ... reflect 561; `__main__` at 564) MATCHES `main.py` (Grep). hooks.json:44-62 (UserPromptSubmit: freshness-user-prompt.sh and ccsession-tag/hooks/session-name.sh) and :96-105 (launch-job-identity.sh, Bash, timeout 5) MATCH; install_hooks.py:87 MATCH; Glob of src/superclaude/hooks/scripts/ returns 14 files (report says 14) MATCH.
- Negative claims re-run with tools: `pipeline` in issue.md = 0 matches; `gh project|projectV2|graphql` under sc-issue-protocol = 0; `AskUserQuestion` appears only at SKILL.md:4 and refs/create.md:59; `--pipeline|sc-launch|launch-level` under src/ matches only adversarial files, HOW-WE-WORK.md and launch-job-identity.sh (store path), never under skills/sc-issue-protocol: all MATCH the report (2.1 and 2.4).
- Sections 5.x (external pages) were skimmed only for statements about repo code (5.9 repeats `cli/pipeline/process.py:134-166`, not in my assigned list); the web pages themselves are outside this assignment (assigned sources are codebase files).

### Detail-preservation omissions (checklist item 2), all MINOR
- STOP code `E-WORKER-NO-OUTPUT` (retry the worker once, then STOP; SKILL.md:64, :131, claim.md:33, :62) is not named in the report; the report covers the consequence generically ("after Wave 3 the issue is assigned even if Waves 4-6 fail", Section 2.1) and names `E-TIER-UNAVAILABLE`, `E-POST-FAILED`, `E-ASSIGN-FAILED`, `E-GH-AUTH`, `E-NO-ORIGIN`, `E-FOREIGN-REPO`, `E-NOT-AN-ISSUE`.
- `clickup_claim.py` `error`/`page_cap` outcome, `CLICKUP_MAX_PAGES` and `CLICKUP_LIST_IDS` are not named (the report keeps "all ClickUp outcomes non-fatal" and "up to 20 pages at 30 s per request", which is correct). Does not change any plan step.
- `E-CREATE-ONLY-FLAG` and the create-mode details are not carried; irrelevant to a claim-only watcher whose prompt carries no flags.
- `launch-job-identity.sh` execution changes (fresh bash per call, cd does not persist, 64 KiB cap, jobs wait for descendants) are not carried; the report treats the adapter as dormant, which the code supports (hook() returns 0 unless `sessions/<sid>` exists, lines 427-437).

## Source-Document Fidelity Report

Report reviewed: `.dev/tasks/to-do/TASK-RESEARCH-issue-watcher-20261107-064950/RESEARCH-REPORT-issue-watcher.md` (2176 lines, includes the F1/F2 edits in Section 8 Phase 3 step 3.4, Phase 5 and the test table)
Source files checked: 12 files assigned and 8 further files opened for edited-section checks; assigned lines 3074 by `wc -l` (README.md 766 lines: only lines 205-289 and 525-544 read in full, the rest located by Grep; every other assigned file read in full). Extra files opened: `cli/install_user_setup.py` (28-37, 195-266), `hooks/hooks.json` (40-110), `cli/install_hooks.py` (Grep), `sc-pr-submit-protocol/scripts/poll-augment-review.sh` (44-79), `cli/init_lite.py` (Grep), `cli/main.py` (Grep), `tests/pr_submit/test_conflict_e2e.py` (Grep), `skills/ccsession-tag/ccsession-orca` (105-125).
Date: 2026-11-07

### Fidelity Findings

| # | Type | Source File | Report Section | Finding | Severity |
|---|---|---|---|---|---|
| 1 | Inaccurate | `src/superclaude/core/WORKER-CONTRACT.md:112` | 2.1 (line 234), Phase 1 step 1.6, gap G15, Q36 | Report says the rule "requires the user's instruction in the live conversation" for outward git/GitHub actions. The source says the coordinator acts "only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation"; the live conversation only waives the at-the-moment confirmation, and the rule binds the coordinator, not a plain-process poller. The report's conclusion (no category for a standing authorization by a label) is still correct | MINOR |
| 2 | Inaccurate | `tests/pr_submit/test_conflict_e2e.py:178-186` | Phase 4 step 4.5 | "token list modelled on `assert_no_retrigger_call`": the helper also treats any `--method` as write-shaped, the plan allows `--method GET`. The plan states its own read rule (4) explicitly, so this is a disclosed adaptation | MINOR |
| 3 | Inaccurate | `origin_repo.py`; design doc front matter; `launch-job-identity.sh` | 2.1 (line 191), 2.4 (line 390), 2.4 (line 397) | Cosmetic count/line drift: "196 lines" (wc -l 195); `planning_status` cited `:9-10` (line 10); `identify()` 215-247 (closes at 248) | MINOR |
| 4 | Missing | `refs/claim.md:33,:62`; `SKILL.md:64,:131` | 2.1 | `E-WORKER-NO-OUTPUT` (worker retried once, then STOP) is not named; the generic "claim can fail after Wave 3" consequence is stated | MINOR |
| 5 | Missing | `scripts/clickup_claim.py:56,:203-206` | 2.1 | `error`/`page_cap` outcome and the `CLICKUP_MAX_PAGES` / `CLICKUP_LIST_IDS` remedy not named (ClickUp stays non-fatal in the report, which is correct) | MINOR |
| 6 | Missing | `launch-job-identity.sh` (comments l.14-19; hook() l.414-489) | 2.4 | Execution-change details (fresh bash, `cd` not persistent, descendants awaited) not carried; irrelevant while the adapter is dormant | MINOR |

No CRITICAL or IMPORTANT finding. No phantom finding. No aspirational claim presented as current code (`--claim --pipeline`, `launch-level-guard.sh`, marker binding, L2 pre-push are consistently labelled design-only / absent; Glob confirms `launch-level-guard*` does not exist). Addendum fidelity (checklist item 6): the owner decision (option A, claim-only, integer-only prompt) and IronbellyOrg/Coder#477 (listener, registration and transport in the Coder repo; filed assuming a push design; unnecessary under A unless B or C is revisited; only a validated integer reaches the session prompt) are stated in Sections 1.1, 1.2, 3 (legend and 3.4), 6.1, 7.1, 7.7, 8 (follow-up), 9.1 exactly as research-notes ADDENDUM and ADDENDUM 2 state them; the Recommendation is labelled "decided by the owner" and never "pending owner decision".

### Summary
- Files checked: 12 assigned (11 in full, ccsession-tag/README.md in part) plus 8 supporting files for the F1/F2 edits
- Claims verified: 120+ individual citations/claims re-read against source (file:line cites in Sections 1-4, 6-9; 8 negative-existence claims re-run by Grep/Glob; F1 and F2 edits; Orca binary resolution via `which -a`)
- Fidelity issues: 0 blocking (0 CRITICAL, 0 IMPORTANT), 6 MINOR
- F1/F2 (unverified by a fourth review): both consistent with the code they cite and internally consistent across step 3.4, step 5.2, Phase 5 algorithm step 3/4/12, test table, Test plan summary and step 6.2; no leftover `which=shutil.which` default argument text.
- Confidence: Verified: 12 of 12 assigned sources (README partially) | Unverifiable: 0 | Unchecked: parts of README.md lines 1-204 and 290-524, 545-766 (not cited by the report beyond the lines verified) | Confidence: high for the cited lines; README remainder not exhaustively read
- Tool engagement: Read: 27 | Grep: 17 | Glob: 3 | Bash: 2 (no web lookups)

Verdict: PASS (6 MINOR notes, no blocking finding)

VERDICT: PASS

