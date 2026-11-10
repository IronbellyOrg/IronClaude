# QA Report — Research Gate

**Topic:** git pre-push hook semantics for the L2 launch-level guard (issue #441)
**Date:** 2026-11-08
**Phase:** research-gate
**Lens:** evidence-quality
**Depth tier:** Standard
**Fix cycle:** N/A
**Fix authorization:** false (report only)

---

## Analyst report

`qa/analyst-completeness-report.md` does not exist (directory listing of `qa/` on 2026-11-08 shows no such file). Full independent verification was performed.

## Verification log (written incrementally)

### File 01 (identity selector ancestry)

- Status: Complete; Summary present (302 lines). Section order 1, 2, 3, 7, 4, 5, 6, 8 shows iterative writing.
- Read `src/superclaude/hooks/scripts/launch-job-identity.sh` in full (566 lines). Every cited line checked matches: 4, 7-8, 20-24, 25-53, 55, 81-84, 87-99, 102-122, 109, 125-137, 140-161, 164-174, 169, 171, 177-186, 202-207, 210-212, 215-248, 251-265, 291-301 (setsid 292), 341-359, 365, 392, 525-556, 536, 566.
- External citations checked: `src/superclaude/hooks/hooks.json` line 130 (identity command, Bash matcher at 126), plugin `hooks.json` line 100, `install_hooks.py` line 90, `orca_worktree.py` lines 803 and 1025-1028, design lines 493, 495-502, 512, 514, 518, 547-565, 557, 559, and seed brief lines 22-25, 73. All match.
- `cmp` of the source and plugin `launch-job-identity.sh` shows no difference, so the "byte-identical plugin mirror" claim holds.
- MINOR: the line 55 quote omits `IFS=` (the source line is `IFS= read -r -d '' launch_identity_code <<'PY'`).
- MINOR (evidence-quality): section 7 reports experiments in `/tmp/l2-ident.XXXXXXXX` and `/tmp/l2-ident2` as prose and tables, without the exact commands and verbatim output. The exact-command rule in the gate brief names file 04 only, and the conclusions agree with the code (session id from `/proc/<pid>/stat` field 6, no PPID walk), so this is a note.

### File 02 (L1 guard push bypass coverage)

- Status: Complete; Summary present (284 lines).
- Checked against `src/superclaude/hooks/scripts/launch-level-guard.sh` (747 lines; read 1-200 and 250-747). Every cited line and every quoted regex checked matches: 36-133, 50-57, 59-61, 78-81, 94-97, 135-139, 147-163, 168-173, 195, 257-273, 394, 417, 421-437, 440-441, 446, 450, 486-494, 495-524, 525-534 (528 push/send-pack/http-push), 535-558 (549 list), 559-566, 611-654, 659-669 (661 canonical push regex), 672-680, 706, 710-714, 716-718, 722-743.
- The static evasions in section 9 (including `A_B=1 git $'\x70ush' ...`) follow from the T/G/W normalisation and the command-position-only subcommand table.
- MINOR: section 5 states "cd persists between Bash calls" as fact, but Gap 7 tags the same point [UNVERIFIED], and design line 559 says an internal `cd` does not persist under the governed adapter. The file is internally inconsistent on this point. It does not change any coverage verdict.

### File 03 (design and claim code cross-validation)

- Status: Complete; Summary present (325 lines). 83 claims D19-1 to D19-83, each tagged.
- `orca_worktree.py` (1452 lines) read at 45-52, 770-810, 841-845, 925-940, 998-1084, 1195-1389. Every ow citation checked matches: 772, 789-799, 803, 1012-1029, 1032-1068, 1053-1060, 1061-1063, 1071, 1282-1304, 1307-1312, 1315, 1330-1334, 1337, 1376-1385.
- The two [CODE-CONTRADICTED] claims are confirmed:
  - D19-16: a foreign executable hook gives `present-unverified` and no warning. See the test parametrisation at `tests/skills/test_issue_orca_worktree.py:1691`, the assertion at 1727, and ow:1312.
  - D19-18: the launch continues after `l2_status` (ow:1311-1388); REMEDY at ow:789-792.
- Design lines 487, 506, 510, 512, 514, 518, 520, 526, 534, 538-545, 549-565, 574 and 578 match the claims made about them.
- `hooks.json` lines 116, 120, 126 and 130 match. In the plugin `hooks.json`, lines 90 and 100 match.
- `SKILL.md:150` matches, as do `tests/skills/test_issue_orca_worktree.py` 1554 and 1686-1729, and the test policy in `tests/hooks/test_launch_job_identity.py` 1175-1232 (it uses `line.split()` with 4-way unpacking and reads stdin for every actor).
- `.dev/tasks/done/TASK-WF-authorizedNarrow-20261106-214325/artifacts/live-harness-events.jsonl` exists (4881 bytes).
- The `.dev/brainstorms/20261106-l2-prepush-decisions/` tree is absent (`ls .dev/brainstorms/`), which confirms D19-10 and section 19.6 as stale.
- **IMPORTANT (false claim):** file 03 line 22 says Glob `.dev/brainstorms/2026110[56]*` "returned no files, so the historical corpus `.dev/brainstorms/20261105-170229-launch-level-hook/` named at design line 487 ... is also absent".
  - That is false. The directory exists and is git-tracked (last commit `4f7e3e7e`, 2026-11-06).
  - Every file design line 487 names is present: `merged-requirements.md`, `enrichment/research-light.md`, `adversarial/adversarial/plan-review.md`, `plan-review-2.md`, `plan-review-3.md` and `adversarial/adversarial/refactor-plan.md` (Glob results).
  - `.dev/brainstorms/20261105-024132-issue-claim-orca-worktree-flag` also matches the same pattern.
  - The error spreads to three places: the [STALE DOC] entry for design line 487 (file 03 line 316), the open question at line 299, and the Summary.
- MINOR: section 4 heading says `install_hooks.py` has 612 lines; `wc -l` gives 611.
- Re-checked at gate close: Glob `.dev/brainstorms/20261105-170229-launch-level-hook/**/*.md` returns 25 files, so the IMPORTANT finding stands. The wrong absence claim appears at file 03 lines 22, 299 and 316.
- File 03 line 46 is correct: `/home/coder/workspaces/IronClaude/.git/hooks/pre-push` does not exist (`ls`), and `git rev-parse --git-path hooks/pre-push` from this worktree resolves to that path.
- All 14 `UNVERIFIED-GIT` lines of file 03 (lines 277-290) are covered by the Step 2.5 table in file 04.

### File 04 (empirical git pre-push experiments)

- Status: Complete. Summary present (lines 2257-2261). Results table at 1714-1771, Step 2.5 at 1773-2231, Gaps at 2233-2250, Stale Documentation at 2252-2255. The file has 2261 lines and was read in full.
- **Evidence:** every experiment has an exact command block and verbatim output. That covers E0-E31 in the first sandbox and F0-F4 in the follow-up sandbox. Each push shows the remote refs before and after (or the runner's `REMOTE-REFS-CHANGED` line) and the hook log. Where output is filtered or reduced, the file says so; examples are E19, E23, E24-E29 and E28b/c.
- **Safety record, first sandbox `/tmp/prepush-research.ERbSguv9`:**
  - Created with `mktemp -d /tmp/prepush-research.XXXXXXXX` (E0).
  - `remote -v` at lines 47-49 shows only `/tmp/prepush-research.ERbSguv9/remote.git`. The SHA-256 clone's `remote -v` at lines 1168-1169 shows only `.../remote256.git`.
  - `--mirror` (E11, line 559/641) targets `$S/remote2.git`. `send-pack` (E17, lines 907-909, 915, 923, 933) targets `$S/remote.git`. `clone2` (E23) is cloned from `$R`.
  - Removed at lines 1701-1711: `rm exit=0`, then `ls` reports "No such file or directory".
  - Compliant.
- **Safety record, follow-up sandbox `/tmp/prepush-followup.0OZWoyIi`:**
  - Created with `mktemp -d /tmp/prepush-followup.XXXXXXXX` (line 1801).
  - `remote -v` at lines 1872-1874 shows only the local bare `.../remote.git`. Every F-push targets `origin` = that sandbox remote.
  - Removed at lines 2217-2228: `rm rc=0`, then `ls` reports "No such file or directory".
  - Compliant.
- Grep of file 04 for `https?://`, `ssh://`, `git@` and `github.com` found no hits outside the sandbox paths. No push went to a URL that is not a local bare repo inside a recorded sandbox.
- **Independent reproduction:** I ran my own `mktemp -d /tmp/qa-prepush.XXXXXXXX` sandbox. Its only remote was the local bare `r.git`, and it was removed afterwards (trap; `ls` reports "No such file or directory"). On git 2.47.3 it reproduced six results:
  - E30a: `--git-path` from a linked worktree resolves to the common-dir hook.
  - E6/E13: `--dry-run HEAD:main` runs the hook with field 1 `HEAD` and field 3 `refs/heads/main`, and the remote is unchanged.
  - E1: create gives a 40-zero field 4.
  - E12: an up-to-date push runs the hook with EMPTY stdin.
  - E14/E15: `--no-verify` and `-c core.hooksPath=/dev/null` skip the hook.
  - E3a: delete gives `(delete) <zero-oid>`.
  - E29c: a non-executable hook fails open, and the push succeeds.
- Arithmetic checks hold:
  - Step 2.5 has 17 rows.
  - 15 rows are CONFIRMED, and the 15 IDs listed match the table.
  - 6 rows were settled by F1-F4: D19-21, 27, 29, 33, 35 and 42.
  - 16 claims = 14 `UNVERIFIED-GIT` + D19-27 + D19-29.
- MINOR (internal inconsistency): Gaps lines 2241 (`refs/heads/ma` not pushed) and 2242 (worktree removal not exercised) are stale. F3a and F2 resolved them, and line 2248 says so, but the two bullets were not updated.
- MINOR (tag consistency): Stale Documentation line 2254 says "None contradicted", while the Step 2.5 table (line 1791) and Gaps (line 2247) tag D19-47 as [CODE-CONTRADICTED]. Line 2247 explains that the sentence is "incomplete rather than wrong", so the meaning is recoverable, but the tag and the heading disagree.
- MINOR: E0 runs `chmod +x $S/x.sh $S/hook-logging.sh` but does not show the commands that wrote those files. Their full contents are shown, and the F0 block does show its `cat > ... <<'EOF'` creation.

---

## Overall Verdict: FAIL

One blocking finding (IMPORTANT, a false claim in file 03) is open. Every other finding is MINOR and recorded as a note.

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory | PASS | 4 research files plus `research-notes.md`. All 4 have Status: Complete and a Summary: 01 (302 lines), 02 (284), 03 (325), 04 (2261, Summary at 2257). |
| 2 | Evidence density | FAIL | All four files are Dense: nearly every claim cites a file:line, and every cited line I checked matches (see the per-file logs). File 04 gives an exact command and verbatim output for every experiment, and I reproduced 7 of its results in my own sandbox. Fails on one false claim: file 03 line 22, which says the line-487 corpus is absent (Glob finds 25 files). |
| 3 | Scope coverage | PASS | `research-notes.md` EXISTING_FILES (lines 24-30) lists 5 entries. `launch-level-guard.sh` is covered by file 02. `launch-job-identity.sh` by file 01. Design §19 by files 03 and 04. `orca_worktree.py` by file 03 (sections 2-3). `install_hooks.py` by file 03 (section 4). |
| 4 | Documentation cross-validation | PASS | Every design claim in file 03 (D19-1 to D19-83) is tagged. The [CODE-VERIFIED] claims I checked in files 01, 03 and 04 match the code or the measured output. Both [CODE-CONTRADICTED] claims (D19-16, D19-18) are confirmed. |
| 5 | Contradiction resolution | PASS (notes) | File 03 left D19-47 UNVERIFIED-GIT, and file 04 resolves it as CONTRADICTED in part (E23a). Within single files there are inconsistencies: file 02 on cd persistence, and file 04 Gaps 2241/2242 against F2/F3 and line 2254 against line 1791. These are MINOR. No cross-file contradiction is left unresolved. |
| 6 | Gap severity | FAIL | The open question at file 03 line 299 and the [STALE DOC] entry at line 316 rest on the false absence claim. Synthesis would report design line 487 as stale and ask the owner about artifacts that exist. That is IMPORTANT. Every other gap is MINOR or is routed (web-01). |
| 7 | Depth (Standard) | PASS | There is file-level coverage of every EXISTING_FILES entry. File 03 also traces `l2_status` data flow (line 37). |
| 8 | Integration points | PASS | Hook to identify: file 01, with `identify` at jid:215 and the CLI entry. Installer: file 03 section 4 (`install_hooks.py` has no git-hook path) and `hooks.json` 116-130. `l2_status` read: file 03 at ow:1012-1029 and the call at ow:1311. Hook lookup: file 04 E30/E31. |
| 9 | Pattern documentation | PASS | O_EXCL + fchmod + link no-replace: file 01, jid:164-174. Session-id actor selection: file 01, jid:202-215 and setsid at 292. `rev-parse --git-path`: file 03 at ow:1021 and file 04 at E30a. Each one was checked against the source. |
| 10 | Incremental writing | PASS | File 01's section order (1, 2, 3, 7, 4, ...) shows it was written in stages. File 04 has an appended Step 2.5 and a follow-up sandbox section. Files 02 and 03 have their gap lists added after the main sections. |

## Summary

- Checks passed: 8 / 10
- Checks failed: 2 (items 2 and 6, from the same root finding)
- Critical issues: 0
- Important issues: 1
- Minor issues: 8
- Issues fixed in-place: 0 (fix authorization false)

## Issues Found

| # | Severity | File | Finding | Required fix |
|---|----------|------|---------|-------------|
| 1 | IMPORTANT | `research/03-design-and-claim-code-crossvalidation.md` lines 22, 299, 316 and Summary | False claim. It says Glob `.dev/brainstorms/2026110[56]*` returned no files and that `.dev/brainstorms/20261105-170229-launch-level-hook/` (design line 487) is absent. The directory exists and is git-tracked (commit `4f7e3e7e`). It holds `merged-requirements.md`, `enrichment/research-light.md`, `adversarial/adversarial/plan-review{,-2,-3}.md` and `refactor-plan.md` (25 `.md` files in total). `20261105-024132-issue-claim-orca-worktree-flag` also matches the glob. | Correct line 22 to say the line-487 corpus exists. Remove it from the [STALE DOC] entry at line 316, which should then cite only the absent `20261106-l2-prepush-decisions/` files. Remove it from the open question at line 299. Fix the Summary to match. Then re-check whether any design §19 statement attributed to that corpus can now be tagged. |
| 2 | MINOR | `research/01-identity-selector-ancestry.md` line 55 quote | The quote omits `IFS=` (the source is `IFS= read -r -d '' launch_identity_code <<'PY'`). | Quote the line exactly. |
| 3 | MINOR | `research/01-identity-selector-ancestry.md` section 7 | The `/tmp/l2-ident*` experiments are given as prose and tables, without exact commands and verbatim output. | Add the command blocks and verbatim output, or mark them as summarised. |
| 4 | MINOR | `research/02-l1-guard-push-bypass-coverage.md` section 5 | It states "cd persists between Bash calls" as fact, while its own Gap 7 tags it [UNVERIFIED] and design line 559 says it does not persist under the governed adapter. | Make section 5 agree with Gap 7 by tagging it [UNVERIFIED]. |
| 5 | MINOR | `research/03-design-and-claim-code-crossvalidation.md` section 4 heading | It says `install_hooks.py` has 612 lines; `wc -l` gives 611. | Change to 611. |
| 6 | MINOR | `research/04-empirical-git-prepush-experiments.md` Gaps lines 2241-2242 | The bullets say `refs/heads/ma` was not pushed and worktree removal was not exercised. F3a and F2 later did both (line 2248). | Update or strike the two bullets. |
| 7 | MINOR | `research/04-empirical-git-prepush-experiments.md` line 2254 | Stale Documentation says "None contradicted", while lines 1791 and 2247 tag D19-47 [CODE-CONTRADICTED]. | Pick one tag for D19-47 and make all three places use it. |
| 8 | MINOR | `research/04-empirical-git-prepush-experiments.md` E0 | `x.sh` and `hook-logging.sh` are made executable without showing the commands that created them. Their contents are shown. | Show the `cat > ... <<'EOF'` creation lines, as F0 does. |
| 9 | MINOR | scope note | RECOMMENDED_OUTPUTS lists `web-01` and `web-02` (`research-notes.md` lines 56-57). They are outside this four-file gate and were not reviewed. D19-30 (API part) is routed to web-01. | Gate web-01 and web-02 separately before synthesis. |

## Actions Taken

None. Fix authorization was false. The only files written were this report and a temporary `/tmp/qa-prepush.*` sandbox, which was removed.

## Recommendations

- Fix issue 1 in file 03, then re-run this gate as fix cycle 1. Only issue 1 needs re-verification.
- The file 04 safety record is compliant for both sandboxes. I found no push to a non-sandbox URL.

## Confidence

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 22 | Grep: 8 | Glob: 3 | Bash: 5 (approximate running totals across the session). No web research was done, so tavily_search, tavily_extract, web_search_fallback and web_fetch_fallback are all 0.
- Unchecked items: none. Unverifiable items: none.

## QA Complete
