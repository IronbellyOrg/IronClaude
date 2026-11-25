# Evidence Validation Report

(Persisted by the parent from the evidence-validator return, condensed; verdicts and tables as returned.)

**Report under validation**: /home/coder/workspaces/IronClaude/.dev/troubleshoot/performance-ccsession-launch-takes-20-seconds-20261117185300/REPORT.md.draft
**Timestamp**: 2026-11-17T19:25:47Z
**Total citations**: 13
**Verified**: 8
**Dropped**: 0
**Passed through (command, no reexec)**: 5
**Suggested report status**: success (the validator contributes nothing above success; the report's own `partial` comes from the Wave 4 self-review and the diagnosability verdict and is kept by the monotonic merge)

## Verified citations

Each line was read in the installed scripts (/home/coder/.claude/skills/ccsession-tag/ccsession and ccsession-orca) and compared with the quoted text.

| # | Type | Location | Verdict |
|---|------|----------|---------|
| 1 | file:line | ccsession:1383 and :1403 (`local ... LC_ALL=C`); the probe printing 0 matches tier1-observation.md | verified |
| 2 | file:line | ccsession:1396 and :1397 (head/tail pipeline, `grep -oE`, `awk '!seen[$0]++'`) | verified |
| 3 | file:line | ccsession:1482 (`ls -t ... \| head -n 1 \|\| true`) and :1599 (`jsonl=$(session_transcript "$uuid")`) | verified |
| 4 | file:line | ccsession:1535 and :1536 (`date -r` then `date -d "@$epoch"`); the `date -r` failure matches tier1-observation.md | verified |
| 5 | file:line | ccsession:1610, :1611, :1616, :1617 (all four `$(...)` calls) | verified |
| 6 | file:line | ccsession:1718 (`sessions=$(LIST_NAME_ON=... \`): the list is captured whole | verified |
| 7 | file:line | ccsession-orca:204 (`answer=$("$CCSESSION" --ask "$hint") \|\| rc=$?`) | verified |
| 8 | file:line | ccsession:1733 and :1735 (the 30 s comment and the 60 s comment) | verified |

Line ranges quoted elsewhere also hold: `list_sessions` 1554-1663, `session_home` 1377-1399, `show_saved` 1715-1731.

## Dropped citations

None. Nearest defect: the PS4 command text in item 10 is not in tier1-observation.md but in diagnosability-tasklist.md Task 1 (the report now cites that; the cited line text was not wrong).

## Passed-through citations (allow_command_reexec=false)

Items 9 (`time ccsession --here` / `--list`), 10 (the `bash -x` trace), 11 (head/tail loop and the two grep pipelines), 12 (six alternating runs, plain vs `env LC_ALL=C`), 13 (one-process prototype): not re-run; numbers match tier1-observation.md and locale-probe.txt.

## Numeric cross-check

No mismatches: 27.069 s, 5.823 s, 13.566 s, 405 lines, 14.473 s, 12.16 s, 5.12 s, 2.68 s, 2.03 s, 1.95 s, 1.22 s and 1.20 s (2.42 s together), 1756 `date`, 972 `head`, 936 `dirname`, 936 `basename`, 878 `stat`, 477 `ls`, 448 `grep`, 1.442 s, 6.460 s, 13.227 s, the six locale-probe times, median gap 6.99 s, 0.75 s, 554 MB, 27.08 s trace wall, 19.4 s CPU / 27.1 s (about 0.7 core, about 2.5% of 28 cores), 13.227/6.460 = 2.05 ("about twice"), calibrated 0.83/0.83/0.83/0.50.

## Structural assertions

| id | fired | flag | consequence applied | evidence (file:line or "input absent") |
|---|---|---|---|---|
| A1 | no | none | none | no enum token in Summary or Diagnosis; max calibrated 0.83; the performance-engineer card's 0.50 is not below 0.50 |
| A2 | skipped | none | none | input absent: diff_path is null (no diff this run) |
| A3 | no | none | none | draft Date 2026-11-17T19:24:55Z is earlier than the draft mtime 19:25:41Z and not T00:00:00Z |
| A4 | no | none | none | Closure verdict `not_applicable` is in the allowed set |
| A5 | no | none | none | shared diagnosis, no "consensus on unobserved" claim; the adversarial debate ran; all cards declare `runtime_trace` |
| A6 | no | none | none | diagnosability-tasklist.md says `discriminator-required: no`; no Reference-context rows |
| A7 | no | none | none | execution-locus.md gives a concrete RUN-SITE; producers.md has zero producer rows |
| A8 | no | none | none | OBSERVE-VIA: same-shell; the failing arm is not a CI job |
| A9 | no | none | none | no literal Reference-context value rendered; nothing certified as a control |
| A10 | no | none | none | diagnosability-tasklist.md has an Emitter search block with usable-capture-routes: 1; no capability-verdict blocked |

## Notes (validator)

Claims about origin/master 10f6ec670 and e3e9d636a and the 1902 vs 2072 line counts depend on git and Bash and were not re-verified by the validator; observation line 3 states the byte-identity (`cmp`). No input pathologies.
