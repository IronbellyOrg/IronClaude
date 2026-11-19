# advice-3-a.md (T5) — escalation 1, adviser A (executor family, top rung: opus)
# STATUS: COMPLETE, delivered 2026-11-09 ~15:40Z. Parent check (procedure step 4):
# outcome line OK, one row per T5.AC1-3, differs-by non-empty, citations within
# attempt-2.diff / review-5.md / extras-5.log — PASSED. Pick: winner (tie with -b
# on 1 blocking finding cited; ties go to -a).

outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T5.AC1 | Fine. The review marks it met (review-5.md:2). The four creates with --repo and --body-file are checked at attempt-2.diff:114-115, and the rerun guard at attempt-2.diff:121-125. The failure was the scope finding F5.1 (review-5.md:5, review-5.md:9), not this AC. | None. |
| T5.AC2 | Fine. The review marks it met (review-5.md:3). The generator-equality check is at attempt-2.diff:137-143 and the EXISTS refusal case at attempt-2.diff:146-162. | None. |
| T5.AC3 | Fine. The review marks it met (review-5.md:4). The scripted screen is popped in the send arm (attempt-2.diff:90-95), the path is read from the saved screen (attempt-2.diff:228-232), and the check is WT_T1 (attempt-2.diff:131-132). F5.1 sits in this case's narration. Attempt 2 fixed the 16-19 block (attempt-2.diff:61-64) but left the next stub comment, which still says "terminal wait releases one screen-queue line into screen.txt" (attempt-2.diff:71). The wait arm only checks idle-on (attempt-2.diff:81-84); the send arm does the pop (attempt-2.diff:90-95). review-5.md:9 records this. | Rewrite that one comment so it names the send arm. |

differs-by: earlier fixes edited only the cited lines (review-5.md:5 named 31 and 55-60; attempt 2 fixed 16-19 and the ghstub, per review-5.md:9). This attempt checks every comment in setup-github-selftest.sh against the code it describes before handing back, so a third comment of the same kind cannot come up in the next review.

steps:
1. In .dev/issues/442/scripts/setup-github-selftest.sh, replace line 26 (attempt-2.diff:71) with: `# extend the stub: each terminal send pops one screen-queue line into screen.txt; terminal wait only checks idle-on`. Leave code lines unchanged.
2. Check every other `#` comment in that file against the code below it, and fix any that claim behaviour the code does not have. The one known candidate is lines 71-72 (attempt-2.diff:116-117). They say the template fill is checked ("our sed filled all four sections"), but line 73 only counts `issue create` calls. Reword them to say this case checks only the create count and that the template content is not inspected by the stub. Do not add a new check (that is scope creep).
3. Do not touch setup-github.sh or selftest.sh: their ACs are met (review-5.md:2-4).
4. Run `bash -n .dev/issues/442/scripts/setup-github-selftest.sh`. Then run `timeout 300 bash .dev/issues/442/scripts/selftest.sh` and confirm it ends with `SELFTEST_OK`. The last extras log recorded `test:skip` (extras-5.log:1), so this would be the first observed run.
5. In approach notes, list every comment line checked in step 2 and its result (kept or rewritten), so the re-review can confirm the sweep.

Not checked: delta-5-2.txt is a reverse diff that deletes every script, so treated as noise. The self-test was not run (read-only role).
