BLOCKING_COUNT: 3

# Gate 5 consolidated findings, fix cycle 2 (the last allowed cycle)

Sources: `qa/qa-anti-omission-verification-structural-cycle1.md` (FAIL, Important 1) and `qa/qa-anti-omission-verification-content-cycle1.md` (FAIL, Important 3). Both agents confirm the 4 cycle-1 blocking omissions (O-5, O-8a, OM-1, OM-2) were recovered into the report and the 4 JUSTIFIED rows are valid, so none carries over. Report: `RESEARCH-REPORT-bmad-first-use.md` (1804 lines). Not SYSTEMIC: 3 blocking findings now versus 4 in cycle 1.

| # | Reporter severity | Final severity | Reason for any change | Blocking | Finding | Originating report | Target report section | Proposed fix |
|---|---|---|---|---|---|---|---|---|
| 1 | IMPORTANT (I-1) | IMPORTANT | | yes | Section 8 step 5.3 (l.1542): the new `bmad-os-x` fixture of case (d) counts as a first use, so the install runs; the same step still says "(c), (d), (e) leave P byte-identical", so the test fails on its own fixture. | content verification | 8 (step 5.3) | Make case (d) assert what it now means (a `bmad-os-*` entry alone does not block first use, so P is changed by the install) and keep "byte-identical" only for the cases where it holds. |
| 2 | IMPORTANT (I-2); structural: IMPORTANT | IMPORTANT | | yes | Sections 2.5 (l.406), 4.2 (l.681) and 5.2 (l.910) still say `--output-folder` must be kept in "every first-use command"; the rule is qualified to commands that pass `--user-name` at l.121, 568, 1021 and 1438, and the new flagless `--yes` alternative needs no `--output-folder`. The fix log says it was qualified everywhere. | structural verification; content verification | 2.5, 4.2, 5.2 | Qualify l.406, l.681 and l.910 the same way; Grep the report for any other "every command" / "every first-use command" wording about `--output-folder`. |
| 3 | IMPORTANT (I-3) | IMPORTANT | | yes | Section 5.1 W01-18 (l.867) and step 4D.4 (l.1526): the row-66 recovery concludes that skill-frontmatter hooks are not held back until the folder is trusted, drawn from a `-p` quote; `-p` runs treat every folder as trusted anyway (web-01:155), and the conclusion is an unlabelled inference. | content verification | 5.1 (W01-18), 8 (step 4D.4) | State only what web-01 says (skill-frontmatter hooks run in untrusted `-p` folders, where `-p` already trusts the folder); label any further step `[synthesis inference: ...]` and UNVERIFIED - doc-only; say it is unverified for a user-level stub. |

## Severity changes

none. No finding was downgraded; each keeps the reporting agent's IMPORTANT grade.

## Notes (MINOR, not acted on, never rechecked)

- M-1: the fix log has a section mislabel (structural).
- M-2: the report says `ANTHROPIC_BASE_URL` is "not established" but `llm-env.tf:24-28` sets it to the LiteLLM gateway for every agent process (content).
- Pipeline labels left in the report body (structural).
- The other Minor items of both cycle-1 verification reports and the 91 MINOR rows of `qa/qa-anti-omission-consolidated-findings.md` (including the pinned-test notes: the `coder_script` count pins `test-5-coder-app-allowlist`, `test-70`, `test-74-orca-clean-stop`, `test-1-tool-floor`).

review 2 of 3 complete; if the next verification fails the gate HALTS
