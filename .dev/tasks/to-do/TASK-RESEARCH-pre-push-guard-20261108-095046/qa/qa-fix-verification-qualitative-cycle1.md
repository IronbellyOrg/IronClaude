# QA Report: Fix Cycle (report-qualitative lenses), Gate 3 cycle 1

**Topic:** git pre-push hook semantics for the L2 launch-level guard
**Date:** 2026-11-08
**Phase:** fix-cycle (report-validation, content lenses)
**Fix cycle:** 1 (last allowed cycle)
**Fix authorization:** false (no file other than this report was changed)
**Inputs:** `qa/qa-consolidated-findings-phase6-cycle1.md`, `qa/qa-fix-log.md` (Cycle 1), `RESEARCH-REPORT-pre-push-guard.md`

---

## Overall Verdict: PASS (with notes)

Both cycle 1 blocking findings are fixed. The fixed text is still actionable, accurate to the domain, reproducible and cross-referenced, and no fix introduced a contradiction. The fixes raised four new issues, all MINOR. They are notes and do not block.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Fix #1 applied: `pre-push.uv-dir` is checked on every launch | PASS | Step 2.5(b) (l.1121) requires (1) a regular file opened with `O_NOFOLLOW`; (2) owner = current user, not g/o-writable; (3) content = one absolute path equal to the directory of `shutil.which("uv")`; (4) the directory and `uv` owned by the user or root, not g/o-writable, `uv` executable. Runs "on every run of this step (install and each pre-launch recheck, step 4.1)". Step 4.2 (l.1144) returns `present-owned` only after the 2.5(b) checks "run on every call". |
| 2 | Fix #1: each failure maps to a closed reason | PASS | l.1121: missing, symlink, unreadable, malformed, mismatch or no `uv` give `uv-dir-missing`; wrong owner or a g/o-writable file, directory or `uv` give `not-owned`. Both are in the SC-18 list (l.589) and the 4.2 closed set (l.1144). |
| 3 | Fix #1: SC-24 now has an implementing step | PASS | SC-24 (l.595) parts (a) and (b) cite Phase 1.2, 1.4, 2.1, 2.5(b), 4.2. Each (b) case (symlink, other directory with a stub `uv`, g/o-writable) matches a 2.5(b) clause and its reason. The earlier finding (no step checks the file) is closed. |
| 4 | Fix #1: bypass table and accepted limit | PASS | §7 l.1049: Edit/Write on the file is caught by the 5.1 tokens plus the launch recheck. l.1050: a same-user rewrite of a user-owned `uv` is stated as an accepted limit, pointing to §9 row 41 (l.1339), which gives three owner options. Host fact re-observed: `stat` gives `root 755 /usr/local/bin/uv` and `root 755 /usr/local/bin`; `type -a uv` lists only `/usr/local/bin/uv`. |
| 5 | Fix #1: no contradiction with step 2.1 | PASS | Step 2.1 (l.1117) writes the file from `shutil.which("uv")` and never replaces it; 2.5(b)(3) compares with the same rule ("so no second record is kept"). The SC-18 title (l.589) now covers 2.5(b) failures at install and at a later launch. |
| 6 | Fix #1 is actionable | PASS | Each 2.5(b) clause maps to one file-system check and one reason string. A developer can write the 6.x test cases from SC-24 (a)/(b) and SC-31 (l.602) without more research. The remaining gaps are new MINOR notes 1 and 3. |
| 7 | Fix #2 applied: G-44 is Critical | PASS | l.698 is rated Critical, with the reason given under the l.649 rule (`--no-verify` removes L2, L1 lets it through). The l.649 paragraph now says G-44 and G-45 were added at Gate 3 and how they are rated. |
| 8 | Fix #2 domain accuracy | PASS | Guard l.549 (read now) lists `env`, `sudo`, `nohup`, `exec`, `command`, `builtin`, `timeout`, `xargs`, `setsid`, `time`, `nice`, `stdbuf`, `ionice`, `doas`, `unbuffer`, `eval` and shell keywords. `chrt`, `taskset`, `find` and `uv` are absent, as G-44 says. |
| 9 | Fix #2 cross-references agree | PASS | §8.9 l.1270 (L1-5) names G-44 as the unlisted-wrapper form and rates it Critical. §8.8 (l.1245) agrees. L1-5 is Critical at l.728. G-13 stays Important (l.667) because the l.649 rule keeps G-1 to G-43 at their recorded severity. The report states this, so it is not a contradiction (see MINOR note 4 on wording). |
| 10 | No fix introduced a contradiction (whole-report scan of the touched terms) | PASS | `uv-dir-missing` appears at l.589, 595, 602, 1101, 1103, 1117, 1121, 1144 and 1173, always with the same meaning. `Critical` appears at l.649, 698, 707-733, 1245 and 1270; none rates G-44 differently. |

## Summary

- Previously blocking items now passing: 2 of 2 (#1 uv-dir trust input, #2 G-44 severity)
- Previously blocking items still failing: 0
- New issues from the fixes: 0 CRITICAL, 0 IMPORTANT, 4 MINOR (notes)
- Issue count trend: cycle 0 had 20 blocking, cycle 1 had 2, this cycle has 0. It is falling.
- The MINOR notes N1-N9 of the consolidated file were not rechecked (rule). In passing, N8 is still open: SC-25 (l.596) still says "lines 135-138", while `ll_deny` runs from line 135 to line 139 (read now).

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|---|---|---|---|
| 1 | MINOR | Step 2.5(b)(3) (l.1121) with step 2.1 (l.1117) | The fix compares the file with the directory of `shutil.which("uv")` found by the launcher at each check. The consolidated proposal said "the value recorded at install". So if uv is legitimately moved, or the launcher runs with a different PATH, every later launch reports `uv-dir-missing`. Step 2.1 never rewrites the file, and no step or SC gives a way to recover. The failure is fail-closed: a named `W-L2-ABSENT` warning appears, and at push time a missing `uv` becomes `unknown`, so main is refused. It is not a security gap. The never-rewrite rule was already in the plan before this cycle, so I rate this MINOR, not IMPORTANT. Step 2.8 shows the plan does add a recovery path for the same kind of problem on `pre-push` itself. | Add a sentence to 2.1 or 2.5(b) that handles a mismatch whose new `uv` passes clause (4). Either republish through the 2.8 replace path, or name the manual recovery (delete the file and reinstall) in the `W-L2-ABSENT` detail. Add the case to SC-24. |
| 2 | MINOR | §7 l.1050, §9 row 41 (l.1339) | The accepted limit names only a same-user rewrite of `uv`. But step 1.2 puts the named directory first on PATH for every command the hook runs, and uv finds `python` through PATH. So any user-owned executable placed in a user-owned uv directory is the same hole. The limit is understated. It does not arise on this host: the directory is `/usr/local/bin`, owned by root, mode 755. | Widen row 41 and l.1050 to say "any executable in the named directory when that directory is user-owned". The existing option "require root-owned `uv` and directory" already covers it. |
| 3 | MINOR | SC-18 (l.589), steps 2.5 and 4.2 | SC-18 requires "exactly one" reason. No order is set between the hook checks (2.5) and the uv-dir checks (2.5(b)), or between `not-owned` and `uv-dir-missing` when the uv-dir file fails both. Two implementations could report different reasons for the same state. | State the order of evaluation: 2.5 before 2.5(b), and within 2.5(b) clauses in the order (1) to (4), with the first failure winning. |
| 4 | MINOR | §8.9 L1-5 row (l.1270) | "Covered by G-13; the unlisted-wrapper form of the same bypass is G-44 (both Critical)" can be read as "G-13 and G-44 are both Critical". G-13 is Important (l.667). The meant reading (L1-5 and G-44) agrees with l.649, so this is a wording ambiguity, not a contradiction. | Write "(L1-5 and G-44 both Critical; G-13 keeps its recorded Important)". |

## Actions Taken

None. Fix authorization is false. This report is the only file written.

## Self-Audit

**(a) Reliance list: rf-qa PASS items skipped for structural re-check:**
- No `## Inherited Structural Verdict` block was given. I relied on the consolidated file's statement that cycle 0 findings #1-#20 are closed, and on the fix log's statement that §8.8 (l.1245) was edited. I did not re-verify every §8.8 row structurally.
- I relied on the fix log for the earlier observation of `/usr/local/bin/uv`, and re-observed it myself (below).

**(b) Independent semantic checks (≥1 required, INV-019):**
- G-44's factual basis: I read guard line 549 of `src/superclaude/hooks/scripts/launch-level-guard.sh` with Bash `sed`. `chrt`, `taskset`, `find` and `uv` are not in the wrapper list.
- The host claim in §7 l.1050 and row 41: I ran `stat` and `type -a uv`. Result: root, 755, a single `uv` at `/usr/local/bin/uv`.
- The line-706 tamper-token claim in §7 l.1049 and l.1050: I read guard line 706. It has `.claude/hooks*` and `.git/config*` but no `.git/hooks` token and no `uv` path, which matches "allowed today".
- The N8 location: I read guard lines 135-139. `ll_deny` ends at line 139.
- Consistency across sections: I grepped the report for `Critical` and `uv-dir-missing` and re-read l.589, 595, 596, 649, 667, 698, 1049, 1050, 1117, 1121, 1124, 1144, 1270 and 1339 in this turn. I found no contradictions. That reading produced new notes 1-4.

## Confidence

- **Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: 2 | Glob: 0 | Bash: 5 (all read-only: `sed`, `grep`, `stat`, `type`, `ls`)
- Web research: none needed; Tavily not used and no fallback taken.
- Unchecked items: none. Unverifiable items: none.

## Recommendations

- Proceed. No blocking findings are open, so no escalation is needed.
- Optionally apply MINOR notes 1-4 and the still-open N8 when the report is next edited. Note 1 (recovery after a legitimate move of uv) is the most useful one for the implementer.

## QA Complete
