# Gate A cycle 2 consolidated findings

Source: cycle-1 verification reports (`qa-verification-structural-report.md`: PASS, all 18 fixed; `qa-verification-content-report.md`: FAIL, 17 of 18 fixed).

## Open blocking findings

| id | originating report | file | evidence |
|---|---|---|---|
| A-7 | qa-verification-content-report.md | src/superclaude/cli/issue_watch/audit.py (lines 4-7 module docstring, comment above `_RULES` near lines 215-217) | The docstring still says free text cannot be written into a line through any key, but `host` and `login` accept any printable bounded string (a probe built a warning line with a 35-character English sentence as `host`). Remedy: reword both statements to say `host` and `login` take any printable bounded token, or restrict them to a charset with rejected-value test rows. |

blocking: 1, minor: 4

## Minor notes carried forward (never rechecked)

- 54 minor notes A-19 to A-72 of `qa-consolidated-findings.md` (unchanged).
- Verification notes: fixture-coverage test only checks fixture names in the test source (structural report); `discover` raises `ValueError` for an unsafe trigger or login, so the Phase 6 cycle and `load_config` must validate both first and reject a comma or leading dash as `config_invalid` (content report); "no assertion weakened" was checked by test-id comparison because the tree is untracked; M-4 comment overstatement (same as A-7).
