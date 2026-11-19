model: opus family: claude rung: top
family-fallback: no GPT T1 model reachable on this install; strongest reachable model used
# advice-3-b.md (T5) — escalation 1, adviser B (other family; family-fallback)
# STATUS: COMPLETE, delivered 2026-11-09 ~15:40Z. Parent check (procedure step 4):
# outcome line OK, one row per T5.AC1-3, differs-by non-empty, citations within
# attempt-2.diff / review-5.md — PASSED.

outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T5.AC1 | This was fine. The reviewer marked it met (review-5.md:2). Four creates are checked with --repo and --body-file (attempt-2.diff:114-115, :118), and the rerun adds no creates (attempt-2.diff:121-124). | No code change. Do not touch setup-github.sh or selftest.sh. |
| T5.AC2 | This was fine. The reviewer marked it met (review-5.md:3). The generated file is compared with the line-197 generator (attempt-2.diff:137-144), and the refusal to overwrite is tested (attempt-2.diff:146-162). | No code change. |
| T5.AC3 | The AC itself was met (review-5.md:4): the screen is scripted and the worktree paths are recorded (attempt-2.diff:68-70, :129-132). The run fails only on F5.1, the stale-comment scope finding. Attempt 2 corrected only the lines the first review named (review-5.md:5 cited lines 31 and 17-18). It left a second copy of the same false claim at attempt-2.diff:71 ("terminal wait releases one screen-queue line into screen.txt"). The stub's wait arm only checks idle-on (attempt-2.diff:81-84), and the send arm pops the queue (attempt-2.diff:90-95). The reviewer reopened it there (review-5.md:9). Two more comments in the same block are false and could become the next round's finding. attempt-2.diff:107-108 says "exporting PATH", but lines 109, 122 and 158 set PATH only for that one command. attempt-2.diff:104 exports STUB_ORCA, which no script in .dev/issues/442/scripts reads (a grep finds only this line). | Delete the line-71 comment, since lines 62-64 already describe the rotation correctly. Reword the PATH comment. Delete the unused STUB_ORCA export. |

differs-by: Earlier attempts rewrote only the comment lines the reviewer cited. This attempt checks every comment in setup-github-selftest.sh against the stub code that comment describes, then deletes the duplicate rather than rewording it.

steps:
1. In .dev/issues/442/scripts/setup-github-selftest.sh, delete the comment line "# extend the stub: terminal wait releases one screen-queue line into screen.txt". It is currently live line 26, just above `mkdir -p "$L/bin2"`. Do not replace it: the comment above the `for t in T1 T2 T3 T4; do mkdir` loop already says the send arm pops the queue.
2. In the same file, replace the two-line comment "# the driver calls `orca` from PATH; selftest.sh already put a stub first, so / # we shadow it for this case by exporting PATH with bin2 in front" with one line: "# the driver calls `orca` from PATH; each run below puts bin2 first in PATH for that command only, so it shadows selftest.sh's stub".
3. Delete the line `export STUB_ORCA="$L/bin2/orca"`. No script reads STUB_ORCA.
4. Read every remaining `#` comment in the file and check each one against the code it describes. Check the wait arm and the send arm of the heredoc in particular. Make no other edits. Leave setup-github.sh and selftest.sh unchanged.
5. Run `timeout 300 bash .dev/issues/442/scripts/selftest.sh` and confirm the setup-github cases still pass. Record the result, then send it back to reviewer round r5-3 with F5.1 marked as fixed at the old line 26.

One check was left out: I did not run the self-test myself, because this role is read-only.
