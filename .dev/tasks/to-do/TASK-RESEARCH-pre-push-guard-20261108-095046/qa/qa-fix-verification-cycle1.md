# QA Report: Fix Verification (Gate 3, report validation, cycle 1)

**Topic:** git pre-push hook semantics for the L2 launch-level guard
**Date:** 2026-11-08
**Phase:** report-validation (fix verification)
**Fix cycle:** 1 (third Gate 3 review; the fix-cycle cap is reached)
**Fix authorization:** false (no file other than this report was edited)
**Inputs:** `qa/qa-consolidated-findings-phase6-cycle1.md` (2 blocking findings), `qa/qa-fix-log.md` (Cycle 1 section), `RESEARCH-REPORT-pre-push-guard.md` (1472 lines)

---

## Overall Verdict: FAIL

Both blocking findings are fixed as written. The fix for #1 adds a new IMPORTANT issue (NEW-1): the accepted-limit text it adds says the same-user binary rewrite "does not arise here", but on this host `uv` runs a Python interpreter that the user owns, which no check covers.

## Fix verification table

| # | Original finding | Fixed yes/no | Evidence | New issue |
|---|---|---|---|---|
| 1 | IMPORTANT: `<hooks-dir>/pre-push.uv-dir` is an unchecked trust input (it goes first on PATH before `identify`); no step checks its owner, mode or content, or its directory and `uv`; SC-24 has no implementing `l2_status` step; the file is missing from the §7 bypass table and the 5.1 token rationale | **yes** | Report line 1121 (step 2.5(b)): `O_NOFOLLOW` regular file, owned by the user, not group/other-writable, content equal to the directory of `shutil.which("uv")` at the check, directory and `uv` owned by the user or root and not group/other-writable; failures map to `uv-dir-missing` / `not-owned`; runs at install and at every pre-launch recheck. Line 1117 (2.1) points to 2.5(b). Line 1143 (4.1) names the uv-dir change. Line 1144 (4.2) says `present-owned` requires 2.5(b) "run on every call", so SC-24 now has an implementing step. SC-18 (line 589), SC-24(b) (line 595), the SC-25 `Write` case (line 596) and SC-31 (line 602) map the same failures to the same reasons. Step 6.4 (line 1173) adds the cases. Step 5.1 (line 1156) states the tokens match the file. §7 rows at lines 1049-1050 and §9 row 41 (line 1339) were added. The content-equality check (3) is what stops the fake-`uv` redirect: a user-owned `/tmp/x/uv` passes the owner and mode checks but fails (3). Host facts re-observed this session: `command -v uv` printed `/usr/local/bin/uv`; `ls -ld` printed `drwxr-xr-x root root /usr/local/bin` and `-rwxr-xr-x root root /usr/local/bin/uv` (matches the fix-log line 57 observation) | **NEW-1 (IMPORTANT)**; NEW-3, NEW-4, NEW-5 (MINOR) |
| 2 | IMPORTANT: G-44 rated Important though its `--no-verify` form passes L1 and removes L2, which meets the line-649 Critical rule (L1-5, same class, is Critical) | **yes** | Line 698: G-44 severity is `Critical` with a reworded parenthesis. Line 649: the severity-rule paragraph says G-44 is Critical and G-45 Important. Line 1245 (§8.8) and line 1270 (§8.9) state the Critical rating. Grep for `G-44` in the report gives lines 649, 698, 728, 1046, 1158, 1245, 1270, 1325; none rates it Important. Supporting evidence re-read: guard line 549 (the wrapper skip list has no `chrt`, `taskset`, `find` or `uv`) and line 557 (`LL_CP=$i`); `research/02-l1-guard-push-bypass-coverage.md` line 251 (the wrapper becomes command position, lines 549, 557, 637) and line 248 (the `--no-verify` form passes at every level) | NEW-2, NEW-6 (MINOR) |

Blocking findings confirmed fixed: 2 of 2.

## New issues

| # | Severity | Location | Issue | Evidence | Required fix |
|---|---|---|---|---|---|
| NEW-1 | **IMPORTANT** | §7 bypass row at line 1050; §9 row 41 (line 1339); step 2.5(b) limit sentence (line 1121) | The new accepted-limit text frames the same-user trust gap as "a same-user rewrite of a user-owned `uv`" and states "On this host ... `uv` is `/usr/local/bin/uv`, owned by root, mode 0755, so the case does not arise here". That claim is false in substance. `uv run --no-project python` (the selector's line-566 entry) runs a uv-managed interpreter, and on this host that interpreter is owned by the user. A same-user rewrite of it (or a wrapper that prints `{"status": "ordinary"}`) passes every 2.5(b) check, because 2.5(b) checks only the file, the directory and `uv`. No L1 tamper token at guard line 706 names `.local/share/uv`. Row 41's second remedy ("require `uv` and its directory be root-owned") would not close it, so the owner decision in row 41 rests on a wrong premise | Recorded read-only commands, this session: `uv python find --no-project` (run from `/tmp`) printed `/home/coder/.local/share/uv/python/cpython-3.11-linux-x86_64-gnu/bin/python3.11`; `ls -ld` on its resolved target printed `-rwxr-xr-x 1 coder coder ... cpython-3.11.15-linux-x86_64-gnu/bin/python3.11` and its directory `drwxr-xr-x 2 coder coder`. Guard line 706 re-read: tokens are the store path, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config`, `.config/git` | Widen the limit in line 1050, row 41 and the 2.5(b) sentence to the whole selector chain run under the hook's PATH: `uv`, the interpreter `uv` selects (uv-managed, user-owned on this host), and the selector script. Drop "does not arise here", or say it does arise here through the interpreter. In row 41, add the option of pinning a root-owned interpreter (for example `--python /usr/bin/python3` with `UV_PYTHON_PREFERENCE=only-system` in the hook) or of choosing A-iii. Cite the commands above |
| NEW-2 | MINOR | G-44 parenthesis (line 698) | The new parenthesis says "the example carries `--no-verify` ... so a governed push to main succeeds". The example is `chrt 0 git ...`, and `chrt 0` does not run its command. The Critical rating still holds through `taskset 1`, `find -exec` and `uv run`. This repeats note N7, but the new wording now leans on it | `chrt 0 true` printed `chrt: unsupported priority value for the policy: 0`, rc 1; `taskset 1 true` gave rc 0 (this session) | Use `taskset 1 git $'\x70ush' --no-verify origin main` as the example in G-44 (and in §7 line 1046 and SC-28, per N7) |
| NEW-3 | MINOR | Step 5.1 (line 1156); §7 line 1049; §9 row 41 | "rewriting it ... is refused by L1" overstates what the tokens do: they match only a contiguous `.git/hooks` or `hooks/pre-push` spelling (`cd <common-dir>/.git && cd hooks && printf /x > pre-push.uv-dir` matches neither). The launch-time recheck catches the change only at the next launch, not within the session that made it. Same class as the existing `.git/hooks/pre-push` row (line 1048) and covered by the design disclaimer (line 520) | Guard line 706 (substring tokens on the command text) | Say "contiguous spellings are refused by L1", and state that an in-session rewrite is caught only at the next launch |
| NEW-4 | MINOR | Steps 2.1 and 2.5(b) (lines 1117, 1121) | Check (3) compares the file with the launcher's `shutil.which("uv")` at each check, and the file is never rewritten. If uv moves, or a later launch runs under a PATH that resolves another `uv`, every later launch gets `uv-dir-missing`, and no step says how to recover. This is fail-closed (a warning while `L2_REFUSAL_ENABLED` is False) | Lines 1117 ("never replaced", "not rewritten") and 1121 ("never rewritten here") | Name the recovery (who removes or rewrites the file, under which check), or record it in §9 |
| NEW-5 | MINOR | §9 row 41 placement (line 1339) | Row 41 is placed in the 9.1 decision table, before row 40 (line 1363, in 9.2). The fix log explains the numbering; the position looks out of order | Lines 1339, 1363 | None needed beyond an optional note |
| NEW-6 | MINOR | §8.9 L1-5 row (line 1270) | "Covered by G-13; the unlisted-wrapper form ... is G-44 (both Critical)" can be read as G-13 being Critical; G-13 is Important at line 667 (G-1 to G-43 keep the `gaps-and-questions.md` ratings, line 649) | Lines 649, 667, 1270 | Write "(L1-5 and G-44 are both Critical)" |

Notes N1-N9 from the consolidated findings are not rechecked (MINOR).

## Confidence

- **Checks:** (1) fix #1 present, (2) fix #1 correct and consistent across 2.1/2.5/4.1/4.2/5.1/SC-18/24/25/31/6.4/§7/§9, (3) fix #2 present, (4) fix #2 consistent across 649/698/1245/1270 and every other `G-44` hit, (5) evidence quality of the new text, (6) template conformance of the changed tables, (7) new issues from the fixes.
- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 10 | Grep: 2 | Glob: 0 | Bash: 4 (read-only: `chrt`/`taskset`/`uv` location checks, `uv python find`, two line prints). No web research. No git experiment was needed; none was run.
- Limit: NEW-1 rests on `uv python find` choosing the managed interpreter; the hook's fixed PATH (`<dir>:/usr/bin:/bin`) does not change uv's managed-first choice, but the selector was not run under that exact PATH in a sandbox.

## Recommendation

This is the third Gate 3 review, so the fix-cycle cap is reached. The open blocking count went from 2 to 1 (NEW-1), so it shrank, but no fourth review may run. Escalate NEW-1 to the user: either accept a corrected limit statement (fix as above) or pin a root-owned interpreter in the A-i design.

## QA Complete
