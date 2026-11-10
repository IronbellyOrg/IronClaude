# Revise 1: orca-worker-contract-spec.md (blocking findings F-1 to F-4)

- candidate (edited in place): `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`
- input report: `.dev/orca-command-refactor/review/round1.md` (review 1 of 3, verdict FAIL; Reviser brief at `round1.md:181-183`)
- ids repaired: F-1, F-2, F-3, F-4 only. Medium (M-1 to M-10) and minor (m-1 to m-3) findings are not touched.
- no spec-panel run, no review run, no PASS awarded. This file is a revision record, not a review.

## Byte accounting

Convention: per Edit call, bytes added = length of the new text, bytes deleted = length of the old text it replaced.

| Point | Value |
|---|---|
| size before | 57763 bytes; sha256 `d3cdbe573e57303b9ce6c93d1fe98ba18fb7cb1a15773d926bf6a0c31425200d` (matches the candidate hash in `round1.md:5`) |
| size after | 59286 bytes; sha256 `24081c933a7fbedd6b461f8f09d06fe7d90105a4b5e12f7221ed9cf63dc4b40e` |
| total added | 2047 bytes |
| total deleted | 524 bytes |
| net | +1523 bytes (57763 + 1523 = 59286) |

| Finding | Added | Deleted | Net |
|---|---|---|---|
| F-1 | 188 | 91 | +97 |
| F-2 | 410 | 105 | +305 |
| F-3 | 372 | 172 | +200 |
| F-4 | 1077 | 156 | +921 |

## Rows

| Finding | Disposition | Applied where (post-edit line) |
|---|---|---|
| F-1 | Applied. The section 2.3 brief rule said every brief carries `--unattended`, but the P0 smoke runs (`SPEC:158`, AC-0.4) run before any command accepts the flag (flag introduced in P1, `SPEC:159`). The rule now applies `--unattended` from P1 on and states that P0 briefs omit it. | `SPEC` line 73 (section 2.3) |
| F-2 | Applied. AC-0.4 step 3 needs the P1 contract (`status` and WC-4 path), which does not exist in P0. Step 3 gets a P0 variant that applies WC-5 to the command's existing report and checks that `--report-path` names it. Steps 1, 2, 5-7 are unchanged; step 4 keeps its existing exemption. | `SPEC` line 194 (AC-0.4, section 7.3) |
| F-3 | Applied by exclusion, as the review's first option allows. WC-4 gets an exception for `/sc:load`, which writes no contract under its own Decisions row. AC-1.1 excludes `/sc:load` from the `## Unattended mode` assertion. The Decisions row is unchanged. | `SPEC` line 62 (WC-4); `SPEC` line 195 (AC-1.1) |
| F-4 | Applied. The tasklist row's "no change" claim is withdrawn. The row now states that reflect's fan-out is two layers below the worker (`INV-B:210`), that Claude Code allows three layers and withholds `Agent` at the limit (`INV-A:14`), and that adversarial Mode A depth is UNVERIFIED (`INV-B:111`). WC-7 gets a rule that a gate firing inside a subagent resolves as blocked, because a subagent cannot send `ask`. AC-2.6 (P2) is added to check that the Tier 2 fan-out survives a tasklist run under `--unattended`. | `SPEC` line 122 (section 3.2, tasklist row); `SPEC` line 65 (WC-7); `SPEC` line 204 (new AC-2.6) |

## Notes on the evidence

- Every inventory citation added here was checked by reading the file in this sandbox: `INV-B:210` (`commands-b.md` line 210, Stage 10.5 subagents running `/sc:reflect`), `INV-B:111` (`commands-b.md` line 111, Tier 2 merged by `sc:adversarial-protocol`), `INV-A:14` (`commands-a.md` line 14, three-layer nesting and withheld `Agent` tool).
- WC-2 (c) and WC-7 are cited by their in-spec anchors only.
- The tasklist row stays in section 3.2 (needs a change). Only its "Other required change" cell moved from "none" to the F-4 text, so the section 3 counts (10 / 27 / 6) are unchanged.
- Nothing outside the four findings was changed. The Decisions table, section 9 and the UNVERIFIED list are untouched.
