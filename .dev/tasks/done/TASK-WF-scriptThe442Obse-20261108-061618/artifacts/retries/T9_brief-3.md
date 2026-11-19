pick: advice-3-a.md; runner-up: none; reason: only passing answer

## Task 9: Update the runbook and its handoff for the scripted path

Acceptance criteria:
- The old wording is gone: `grep -n 'not representative' .dev/issues/442/observation-runbook.md` prints nothing (it also prints nothing before the edit, so the real check follows), `grep -n 'must be.*typed by a person' .dev/issues/442/observation-runbook.md` prints nothing, and `grep -c 'orca terminal send' .dev/issues/442/observation-runbook.md` is at least 1; the last two fail before the edit, so the check cannot pass vacuously. Section 6 names every script file that exists in `.dev/issues/442/scripts/` (a self-test case compares the two lists). (T9.AC1)
- `bash .dev/issues/442/scripts/selftest.sh` still prints `SELFTEST_OK` after the edit, because the prompt and filter diffs read the edited runbook. (T9.AC2)

Steps:
1. Restore the attempt-2 handoff paragraph and the 4.2 / section 6 structure, but drop every sentence that summarises script behaviour. Leave out: the `/tmp/ob` and `OB` sentence; the general meaning of `PENDING`; "the answer is logged"; "the scripts save the screens"; anything about tests, stubs or the secret scan; "only when that branch is the T4 worktree's branch"; the clause about refusing while ob-logs is missing.
2. 4.2 "Starting the sessions": quote the authorization scope from the plan, constraint line 19 of the plan file, naming T1 to T4 only. Cite the plan by path and line, and make no claim about the scripts.
3. 4.2 "The prompts themselves": the statement is the plan's (constraint line 24) together with design V6. Prompts sent with `orca terminal send` reach the hooks as the same payload as typed ones, so injected prompts are representative. Cite the send at `orca terminal send --terminal "$h" --text "$text"` (driver.sh:61). Write "may be sent with `driver.sh send`" and no wording about a person typing.
4. 4.2 O-10 edit: replace the web UI wording with the literal `gh_fork api repos/IronbellyOrg/IronClaude/contents/ob-442/T4.txt` (session-gov.sh:356) and `-X PUT` (session-gov.sh:354). Write "not in the GitHub web UI" and nothing more.
5. 4.2 release: write "The LL-TAMPER block applies only to a governed session, so the claim's release `rm` is run from the driving agent's own shell". Cite `rm -f -- "${p1:?}" "${p2:?}"` (session-gov.sh:170) and `refusing an odd session id` (session-gov.sh:161). Keep the `refs/claim.md` line 119 pointer the runbook already has.
6. 4.2 retries and readings: cite `usage: evidence.sh --reading <u20|retry-f7-f8|ac7>` (evidence.sh:42) and say nothing else about what evidence.sh does.
7. Section 6, run-order table. Columns: Order, Command, Source. Source is a literal copied from the script's own header comment, with its citation: `runbook §1.1-§1.3` (setup.sh:2), `runbook §2.1 session A` (session-a.sh:2), session-a2.sh:2, `runbook §1.4` (setup-github.sh:2), `runbook §2.2 governed sessions B to E` (session-gov.sh:2), `drafts .dev/issues/442/observation-results.md` (evidence.sh:4), `runbook section 5.2 steps 1 to 8` (cleanup.sh:2). For session-a2.sh, copy its own line-2 fragment after reading it. Keep the attempt's order.
8. Section 6, the `--apply` rule: two cited literals and no paraphrase. `Default: print the plan and delete nothing.` (cleanup.sh:3), and `REFUSED apply` (cleanup.sh:21).
9. Section 6, stops table. Columns: Literal printed, Printed at, What to do. Rows:
   - `NEEDS_INPUT` (driver.sh:57, driver-helpers.sh:35)
   - `PENDING step=` with `screen=` (session-a.sh:48, session-a.sh:59, session-a2.sh:41)
   - `reason=needs-input` (session-gov.sh:82)
   - `NEEDS_INPUT claim` (setup-github.sh:55)
   - `BLOCKED login-isolated-home` (setup.sh:169), with `exit 3` (setup.sh:170)

   "What to do" is an instruction only, for example: "Read the screen file named on the line. Answer only a dialog about this run's disposable targets, with `driver.sh answer <name> <key> <reason>` (driver.sh:75). Do not resend the prompt." For BLOCKED: "Stop; the owner decides. Do not copy credential files."
10. Section 6 file list: one line beginning `Files not in the run order:` that lists by name every other `.sh` in the folder (lib.sh, driver.sh, driver-helpers.sh, every `*-selftest.sh`, selftest.sh, runbook-selftest.sh). Say nothing about what they do. The folder-against-section check from the attempt stays.
11. In `runbook-selftest.sh`, drop the phrase-blacklist cases and the case that required the PENDING wording. Add two cases:
    - (a) For every match of `` `X` (f.sh:N) `` in section 6 and in 4.2 (several citations in one parenthesis, comma-separated, each checked), `sed -n "${N}p" "$here/f.sh"` must contain X as a fixed string. A citation to a `*selftest.sh` file fails.
    - (b) Every line of section 6 that is not blank, a heading, a table separator, the table header, or the `Files not in the run order:` line must contain at least one `[a-z0-9-]+\.sh:[0-9]+`.

    Keep the old-wording, authorization, stop-count, `--apply` and line-anchor cases.
12. Handoff: keep the paragraph. Change "five sections" to "six sections" (review-2.md:6). State only that the scripts exist in `.dev/issues/442/scripts/` (runbook section 6) and that the live run is this plan's Task 10.
13. Run `bash .dev/issues/442/scripts/selftest.sh` and confirm the last line is `SELFTEST_OK`. Before handing off, check every new 4.2 and section 6 sentence: it is either a cited literal or an instruction. Delete any sentence that is neither.

differs-by: The runbook text stops describing what the scripts do. Every factual statement about a script is a backticked literal copied from an unchanged script line, with its `file.sh:N` citation. A self-test case greps each literal on its cited line, and any line of section 6 without such a citation fails, apart from blank lines, headings, table separators and one list line.
