model: opus family: claude rung: top
# advice-3-a.md (T9), escalation 1, adviser A (executor family, top rung: opus). Saved verbatim.

outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T9.AC1 | The grep checks and the script-name check passed (review-2.md:2). The task failed on scope: section 6 and the 4.2 bullets described what the scripts do in the writer's own words, and each such description could be wrong. The `/tmp/ob (override with OB)` sentence (attempt-2.diff:40) is contradicted by driver.sh:83 and session-gov.sh:48, which write to `$PKG_ART/t10-run-log.md` (review-2.md:4). setup.sh:156-158 fixes the probe at `/tmp/ob/bin/ob-tree.sh` (the review cited 129-138, but the cited lines do not change the finding). The sentence "A PENDING line means the script stopped" (attempt-2.diff:60) is contradicted by session-gov.sh:212 and :223, which go on after a PENDING step (review-2.md:5). The attempt's self-test only blocked phrases that had already failed (attempt-2.diff:88, :91), so it could not catch the next wrong summary. It also required the false PENDING sentence to be present (attempt-2.diff:90). Smaller issue: the handoff still says the runbook has five sections (review-2.md:6). | Section 6 and the new 4.2 sentences must not describe any script in the writer's own words. Every statement about a script is a backticked literal copied from one line of an unchanged script, followed by `(file.sh:N)`. Anything that cannot be said that way is left out (scratch paths, OB override, what PENDING means in general, tests, stubs, what gets logged, what gets copied). Advice to the operator is written as instructions, not as claims about the scripts. A new self-test case checks every citation against the cited line. Change the handoff to "six sections". |
| T9.AC2 | This passed (extras-2.log:9). The risk is that the new check, or a 4.2 edit that adds lines, breaks it. Prompt extraction reads runbook text by section (session-gov.sh:70, session-a.sh:15), and the attempt's line-anchor checks passed only because all edits came after line 698 (extras-2.log:4-8). | Edit only after the `## 3.` anchor at runbook line 698. Cite only scripts other than the self-tests, which are unchanged, so citations do not move. Add the citation check to `runbook-selftest.sh` and register it in `selftest.sh` as before. Run `bash .dev/issues/442/scripts/selftest.sh` and look for `SELFTEST_OK`. |

differs-by: The runbook text stops describing what the scripts do. Every factual statement about a script is a backticked literal copied from an unchanged script line, with its `file.sh:N` citation. A self-test case greps each literal on its cited line, and any line of section 6 without such a citation fails, apart from blank lines, headings, table separators and one list line.

steps:
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

Relevant files:
- /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/observation-runbook.md
- /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/handoff-runbook.md
- /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/runbook-selftest.sh
- /home/coder/workspaces/worktrees/IronClaude/issue-442-runbook/.dev/issues/442/scripts/selftest.sh

I did not check: session-a2.sh line 2 (step 7 leaves its fragment to the implementer); the runbook's current lines 761-860 after the revert; or whether `refs/claim.md` line 119 is still right. The citation check only proves that each quoted literal is on its cited line, not that the sentence around it is true. Keeping that surrounding sentence to an instruction is what stops the next overclaim.
