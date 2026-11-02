# Evidence Validation Report (pass 1)

**Report under validation**: .../REPORT.md.draft (version at 2026-11-02T03:33:13Z)
**Timestamp**: 2026-11-02T03:33:21Z
**Source**: evidence-validator agent (persisted by the parent on receipt)
**Total citations**: 24  **Verified**: 19  **Dropped**: 1  **Passed through (command, no reexec)**: 4
**Suggested report status**: partial

## Verified citations

| # | Location | Verdict |
|---|---|---|
| 1 | ccsession-orca:81 | verified |
| 2 | models.py:799 | verified |
| 3 | ccsession:769-770 | verified |
| 4 | ccsession:801-804 | verified |
| 5 | ccsession:1438 | verified (line also carries `--model "$PROFILE_MODEL"`, covered by `...`) |
| 6 | local-gateway-alias-proxy.py:871-872 | verified; grep for signal/setsid/fork/SIGTERM/SIGHUP: 0 hits |
| 7 | daemon.log:680-681 | verified (00:01:42.345Z, release-readiness@@5e7df77c) |
| 8 | daemon.log:750-751 | verified (22:59:18.584Z, IB-CPlus-01@@b846db04) |
| 9 | daemon.log:752-753 | verified (03:08:20.854Z, pid 2257514, serve-46e81c2f); no lines between 751 and 752 |
| 10 | pty-descendant-exit-verification-DKf-exmf.js | verified (SIGTERM loop and SIGKILL present) |
| 11 | local-gateway-alias-proxy.py:687 | verified |
| 12 | local-gateway-alias-proxy.py:112-117 | verified (range slightly wider than the quote) |
| 13 | local-gateway-alias-proxy.py:852-854 | verified (range includes allow_reuse_address) |
| 14 | ccsession:806-824 | verified |
| 15 | ccsession:722 | verified |
| 16 | README.md:415-418 | verified |
| 17 | local-gateway-alias-proxy.py:862 | verified (`errno == 48`; Linux EADDRINUSE is 98) |
| 18 | README.md:504-505 | verified |
| 19 | test_ccsession_tiers.py::test_a_busy_shim_is_never_stopped_by_a_new_launch | verified at 1379; `proc.terminate()` at 612 |

## Dropped citations

| # | Location | Reason | Recommended action |
|---|---|---|---|
| 1 | Diagnosis paragraph 2: "each the only session created shortly before the corresponding 4114 worker and killed at the minute its turn was cut" | snippet-mismatch for incident 2: daemon.log:747 creates serve-c727018a at 22:46:55.929Z, 27 s before worker 2089859, never killed in the log — a closer-in-time candidate than IB-CPlus-01@@b846db04 (22:41:32). Worker-screen times appear only in O7 prose, not in a cited capture. | Reword to a best-fitting-owner claim; keep the attribution as inference under Grounding Gaps; name serve-c727018a as an alternative the log does not exclude. Keep Evidence 9. |

## Passed-through citations

| # | Command | Note |
|---|---|---|
| 1 | Evidence 7 ps listing | matches O1 lines 8-9, O2 lines 16-18 |
| 2 | Evidence 8 SigIgn | matches O4; mask decoded: HUP, INT, QUIT, PIPE, XFSZ; TERM not set |
| 3 | Evidence 10 live reproduction | matches live-check/before.txt:2-4; script read; 53 bytes = one message_start event |
| 4 | Evidence 12 dmesg/journalctl/health | matches O5, O6 |

## Structural assertions

| id | fired | flag | consequence applied | evidence |
|---|---|---|---|---|
| A1 | no | — | — | headline has no enum token; calibrated 0.92 |
| A2 | skipped | — | — | input absent: diff_path |
| A3 | no | — | — | Date 03:32:02Z ≤ draft mtime 03:33:13Z + 5 min |
| A4 | no | — | — | closure verdict `advisory` allowed |
| A5 | no | — | — | clause 1 skipped (no candidate-fixes.md); clause 2: runtime evidence, single proposal |
| A6 | skipped | — | — | no Reference-context values (total-rows=0) |
| A7 | no | — | — | 0 producer rows; RUN-SITE concrete |
| A8 | no | — | — | OBSERVE-VIA same-shell; no CI arm |
| A9 | skipped | — | — | no literal reference cells |
| A10 | no | — | — | capability-verdict n/a |

## Notes (validator)

- Summary/Root cause state in present tense that Orca's close killed the shim; for the 2026-11-01 incidents this is inferred (calibrator Reproducibility 0.5). A1 does not fire (no enum token).
- "4013 shim started by Orca itself at boot" is an inference from O3, not an observation.
- README restart recipe subshell: closing `)` at README.md:497 verified; opening `(` not read by the validator (parent read it at README.md:480).

## Parent disposition (step 3.25)

- Drop 1 applied: the claim was removed from the draft and replaced by new, separately captured evidence (tier1-observation.md O12: Orca terminal scrollback shows serve-c727018a and both workers REUSED an already-running 4114 shim, so serve-c727018a did not own it; serve-c727018a is still alive). The new citations were sent for a second validation pass (evidence-validation-pass2.md). The drop's `partial` contribution stands in the status merge.
- The 4013 "started by Orca" wording was softened to an inference.
