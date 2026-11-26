review: 2 of 3

# Re-review of the revised plan (reflect-reviewer, model opus; read-only)

Candidate: .dev/tasks/to-do/TASK-WF-remediationSourc-20261126-115917/TASK-WF-remediationSourc-20261126-115917.md (sha256 534d58b15c06c3ab20d1854903ea73a13a7e49fb2ec50fea9ed63d1a654d163c). Baseline: .dev/tasks/archive/TASK-WF-remediationSourc-20261126-041454/TASK-WF-remediationSourc-20261126-041454.md (sha256 2bfcf8fe5b2c8426334e91a31b5bcf18fe8bfef0c07041fbc4e61f04f5c27f6b). Diff: rereview-diff.txt. Nothing was run by the reviewer.

Verdict: FAIL on two NEW blocking findings (F1, F2). Prior blocking findings B1 and B2: resolved. Prior mediums: M-a, M-b, M-c, M-d, M-f resolved; M-e and M-g partly open; N1 to N5 resolved.

## Prior findings
B1 resolved (line 79 runs `--rounds 20 --parallel 1`, timed run, skip comparison, 5x4 demoted to an extra). B2 resolved (line 59: Linux semantics checked: two sockets can share a port when both set SO_REUSEADDR and neither listens, so the helper prints True; a plain bind fails, so a helper without SO_REUSEADDR would print False).

## New findings
- F1 Blocking (Safety), CANDIDATE:77, 79: `pgrep -af "local-gateway-alias-proxy.py"` matches the live shared model-alias shim started from `$HOME/.claude/skills/ccsession-tag/` (ccsession:169, 1249-1256), so "print nothing; kill any leftover" would kill the proxy serving every live session on the host; it also misses the detached launcher-test orphans, whose command line is `python3 <tmp>/shim-under-test.py` (TEST:1467, 1476-1478, 2273); `pgrep -f` can also match the calling shell's own command line. Verified by the orchestrator: a live shim, PID 1644, runs from the home-installed path on this host.
- F2 Blocking (Decision), CANDIDATE:79: `--timeout <the larger of 600 and twice the timing run's secs>` is usually a non-integer (secs is rounded to one decimal, load_repro.py:102) while `--timeout` is `type=int` (load_repro.py:154); argparse rejects it before any run starts. Fix: rounded up to a whole number of seconds. Verified by the orchestrator.
- F3 Medium, CANDIDATE:82 vs 79: "does not count against this change" has no stated effect on line 79's all-20-rc-0 rule and widens the earlier rule; the wall-clock tests use the `shim` fixture, whose port comes from the changed `_free_port()` (TEST:850, 1177-1189).
- F4 Medium, CANDIDATE:78-79: 20 loaded serial whole-file runs plus a timing run of up to 1800 s is a long job; no instruction to run the harness detached and poll for the summary; a cut-off foreground call leaves the 16 burners running and writes no summary (load_repro.py:36, 172-173, 175).
- F5 Note, CANDIDATE:32: "names the module already has ... plus `random`" omits `errno` (lines 36 and 39 require it).
- F6 Note, CANDIDATE:36: a single OSError-to-skip guard around the premise could swallow the premise bind's expected EADDRINUSE and always skip; line 41's red-run rule would catch it.
- F7 Note, CANDIDATE:82: the CCSESSION_FIRST_BYTE_TIMEOUT list omits TEST:1543 and TEST:2212.
- M-e partly open: the whole-file bullets (76-82) do not require recording the port and the below-range test, nor forbid rerunning until green.

## Findings block

```findings-v1
{"id": "F1", "severity": "CRITICAL", "blocking": true, "category": "safety", "anchor": "pgrep -af \"local-gateway-alias-proxy.py\"", "refs": ["B1", "M-g"], "claim": "The leftover-process check and kill would kill the live shared model-alias shim and would miss the shim-under-test orphans."}
{"id": "F2", "severity": "CRITICAL", "blocking": true, "category": "unpassable-check", "anchor": "--timeout <the larger of 600 and twice the timing", "refs": ["B1", "M-d"], "claim": "The computed timeout is usually a decimal and the harness only accepts an integer, so the 20-run command fails to start."}
{"id": "F3", "severity": "MAJOR", "blocking": false, "category": "contradiction", "anchor": "one that passes alone, or fails alone too, is reported and does not count against this change", "refs": ["M-f"], "claim": "Line 82 has no stated effect on line 79's all-20-pass rule."}
{"id": "F4", "severity": "MAJOR", "blocking": false, "category": "other", "anchor": "--rounds 20 --parallel 1 --burners 16", "refs": ["B1"], "claim": "A long foreground run can be cut off, leaving burners and no summary."}
{"id": "F5", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "The tests use only names the module already has", "refs": ["M-c"], "claim": "The sentence omits errno."}
{"id": "F6", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "the listener accept and the premise checks all sit inside one guard", "refs": ["M-a"], "claim": "One guard could swallow the expected EADDRINUSE and always skip."}
{"id": "F7", "severity": "MINOR", "blocking": false, "category": "other", "anchor": "(near lines 1204, 1244, 1554 and 1752)", "refs": ["M-f"], "claim": "The list omits lines 1543 and 2212."}
{"prior": "B1", "status": "resolved"}
{"prior": "B2", "status": "resolved"}
```
