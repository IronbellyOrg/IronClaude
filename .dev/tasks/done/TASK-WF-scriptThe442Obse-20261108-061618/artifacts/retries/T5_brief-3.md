pick: advice-3-a.md; runner-up: advice-3-b.md; reason: tie, -a

## Task 5: Write the disposable GitHub and claim setup script

Acceptance criteria:
- With the stub `gh`, the self-test shows four `issue create` calls, each carrying `--repo IronbellyOrg/IronClaude` and a `--body-file`, and no second set on a rerun. (T5.AC1)
- The self-test shows the generated `settings.local.json` equal to the output of the runbook's line 197 generator, and the script refusing to overwrite an existing file. (T5.AC2)
- The worktree paths are read from the claim screen, not guessed. A self-test case with a scripted screen records `WT_T1`. (T5.AC3)

Steps:
1. In .dev/issues/442/scripts/setup-github-selftest.sh, replace line 26 (attempt-2.diff:71) with: `# extend the stub: each terminal send pops one screen-queue line into screen.txt; terminal wait only checks idle-on`. Leave code lines unchanged.
2. Check every other `#` comment in that file against the code below it, and fix any that claim behaviour the code does not have. The one known candidate is lines 71-72 (attempt-2.diff:116-117). They say the template fill is checked ("our sed filled all four sections"), but line 73 only counts `issue create` calls. Reword them to say this case checks only the create count and that the template content is not inspected by the stub. Do not add a new check (that is scope creep).
3. Do not touch setup-github.sh or selftest.sh: their ACs are met (review-5.md:2-4).
4. Run `bash -n .dev/issues/442/scripts/setup-github-selftest.sh`. Then run `timeout 300 bash .dev/issues/442/scripts/selftest.sh` and confirm it ends with `SELFTEST_OK`. The last extras log recorded `test:skip` (extras-5.log:1), so this would be the first observed run.
5. In approach notes, list every comment line checked in step 2 and its result (kept or rewritten), so the re-review can confirm the sweep.

differs-by: earlier fixes edited only the cited lines (review-5.md:5 named 31 and 55-60; attempt 2 fixed 16-19 and the ghstub, per review-5.md:9). This attempt checks every comment in setup-github-selftest.sh against the code it describes before handing back, so a third comment of the same kind cannot come up in the next review.
