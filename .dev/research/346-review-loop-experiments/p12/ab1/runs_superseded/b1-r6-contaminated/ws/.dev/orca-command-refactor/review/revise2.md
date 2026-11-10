# Revise 2 (REVISE prompt, ids N1, N2)

Candidate: .dev/orca-command-refactor/specs/orca-worker-contract-spec.md (edited in place). Report: .dev/orca-command-refactor/review/round2.md (Reviser brief, round2.md final section, lists N1, N2). No spec-panel run; no PASS claimed.

## Byte accounting
- Before: 58254 bytes (wc -c before edit). After: 58408 bytes. Net +154.
- N1: +60 bytes added, 0 deleted (net; one phrase replaced by a longer one, nothing else touched).
- N2: +94 bytes added, 0 deleted (net).
- Check: 60 + 94 = 154.

## Findings
| id | disposition | where | what |
|---|---|---|---|
| N1 | applied | spec line 194 (AC-0.4, pass column) | "step 4 uses that same file, since the contract arrives in P1 (M2)" became "step 4 is `test -s` on that same file only, and its YAML assertion applies from P1, since the contract arrives in P1 (M2, N1)". The YAML check at line 183 (step 4) is unchanged and no longer applies in P0, where troubleshoot's REPORT.md has no `status`/`command` keys (inventory/commands-b.md:242, 249). Narrowing per round2.md N1 recommendation. |
| N2 | applied | spec line 196 (AC-1.2, check column) | "with `--unattended --output <dir>`" became "with `--unattended` and the command's output flag from section 3 (`--output <dir>`, or `--report-dir <dir>` for `workflow`) (N2)". workflow takes `--report-dir` per spec lines 62 and 92; inventory/commands-b.md:272 names the workflow contract with no `--output`. Matches the fix already made for tdd at line 200. |

Not touched: Medium and minor items (F-1 to F-7, A3). Evidence beyond the spec and inventories (cmd/..., sk/... paths) is UNVERIFIED.
