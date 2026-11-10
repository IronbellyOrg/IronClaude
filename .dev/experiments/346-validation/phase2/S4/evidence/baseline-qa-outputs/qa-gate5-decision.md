GATE5_DECISION: FAIL (cycle 1), second fix cycle required

Review count: review 1 (three anti-omission reports) and the cycle-1 verification (review 2) are done; the cycle-2 verification will be review 3. After cycle 2 any open blocking finding means HALT and ask the user (no exception exists for Gate 5).

SEVERITY_DOWNGRADES: 2

From the `## Severity changes` section of `qa/qa-anti-omission-consolidated-findings.md` (the consolidator re-read test-19 and test-49 for both):
- OM-3 (test-19 cases at lines 200, 743-746, 820 missing from Table 5.1): IMPORTANT to MINOR (a comment, a temp-dir fixture and a literal-string self-test; none reads repo state); disposition stays RECOVER.
- OM-4 (test-49 also scans test-startup-boot.sh): IMPORTANT to MINOR (files under `.github/contract-tests/` are allowlisted at test-49:360-366, so step 5.5 cannot trip the scan); disposition stays RECOVER.

## Inputs read

| Report | Verdict | Counts |
|---|---|---|
| qa/qa-anti-omission-report-1-slice1.md (slice of task-file line 447) | FAIL | 2 Important (O-5, O-8a), 21 Minor items; 445 findings enumerated |
| qa/qa-anti-omission-report-2.md (slice of line 449) | PASS | 0 Critical, 0 Important, 35 Minor; 560 enumerated |
| qa/qa-anti-omission-report-3.md (slice of line 451) | FAIL | 4 Important (OM-1 to OM-4), 27 Minor; 630 enumerated |
| qa/qa-anti-omission-consolidated-findings.md | BLOCKING_COUNT: 4 | 95 rows (91 RECOVER, 4 JUSTIFIED) |
| qa/qa-anti-omission-fix-log-cycle1.md | 4 fixed, 0 not fixed | |
| qa/qa-anti-omission-verification-structural-cycle1.md | FAIL | Critical 0, Important 1, Minor 3; all 4 recoveries present and matching sources, all 4 JUSTIFIED rows valid |
| qa/qa-anti-omission-verification-content-cycle1.md | FAIL | Critical 0, Important 3 (I-1, I-2, I-3), Minor 7; rows 5, 7, 65 correct |

## Open blocking findings entering fix cycle 2

| ID | Report location | Finding |
|---|---|---|
| I-1 | Section 8 step 5.3 (l.1542) | The new `bmad-os-x` fixture of case (d) counts as a first use, so the install runs; the same step still says "(c), (d), (e) leave P byte-identical", so the test fails on its own fixture. Fix: make case (d) assert what it now means (a `bmad-os-*` entry alone does not block first use, so P is changed) and keep "byte-identical" only for the cases where it holds. |
| I-2 (same defect as the structural agent's blocking finding) | Sections 2.5 (l.406), 4.2 (l.681), 5.2 (l.910) | "Keep `--output-folder` in every first-use command" is qualified to "commands that pass `--user-name`" at five places (l.121, 568, 1021, 1438) but three places still say "every command", contradicting the new flagless `--yes` alternative. Fix: qualify l.406, l.681 and l.910 the same way and Grep the report for any other "every command" / "every first-use command" wording about `--output-folder`. |
| I-3 | Section 5.1 W01-18 (l.867), step 4D.4 (l.1526) | The row-66 recovery concludes skill-frontmatter hooks are not held back until the folder is trusted, drawn from a `-p` quote, but `-p` runs treat every folder as trusted anyway (web-01:155); the conclusion is an unlabelled inference. Fix: state only what web-01 says (skill-frontmatter hooks run in untrusted `-p` folders, where `-p` already trusts the folder), label any further step `[synthesis inference: ...]` / UNVERIFIED - doc-only, and say it is unverified for a user-level stub. |

Minor notes (not acted on): the fix log section mislabel; pipeline labels left in the report body; `ANTHROPIC_BASE_URL` is called "not established" but `llm-env.tf:24-28` sets it to the LiteLLM gateway for every agent process (M-2); plus the other Minor items of both verification reports and the 91 MINOR rows of the consolidated file.

## Final (after fix cycle 2, review 3 of 3)

Cycle-2 verification reports read: qa/qa-anti-omission-verification-structural-cycle2.md (PASS, Critical 0, Important 0, Minor 1; rows 1 to 3 fixed, cycle-1 recoveries O-5, O-8a, OM-1, OM-2 intact; the agent noted as a Minor note N-1 that the `bmad-os-x` fixture's skill count must exclude `bmad-os-*`) and qa/qa-anti-omission-verification-content-cycle2.md (FAIL, Critical 0, Important 1, Minor 2; I-1, I-2, I-3 fixed).

SEVERITY_DOWNGRADES (total across cycle-1 and cycle-2 consolidated files): 2 (cycle 1: OM-3 and OM-4 Important to Minor; cycle 2: none). No extra downgrade lines.

Open blocking finding (content agent N-1; the structural agent saw the same point and graded it Minor; the executor keeps the content agent's IMPORTANT grade because the test as written fails on its own fixture, the same defect class as I-1):

- N-1 (IMPORTANT): Section 8 step 5.3 case (d), `bmad-os-x` fixture (report l.1542): the fix says to "assert the same creation as in (a) (… the `bmad-*` skill count)". Case (a) asserts that the number of `P/.claude/skills/bmad-*` directories equals the installer's `<N> skills` line. In the `bmad-os-x` fixture the user's own `bmad-os-x` directory also matches `bmad-*`, so the count is N+1 and the test fails on its own fixture. The installer preserves `bmad-os-*` entries (`_config-driven.js:789-790`). Required fix: in case (d) say that the skill count there excludes `bmad-os-*` entries and that the user's `bmad-os-x` entry is still present afterwards.

GATE5_FINAL: FAIL - HALT

## User exception applied (2026-11-07)

The user explicitly accepted this exception to the 3-review limit for Gate 5 only. The executor made the one edit itself (RESEARCH-REPORT-bmad-first-use.md, Section 8 step 5.3 case (d), L1542: the skill count excludes `bmad-os-*` entries and the user's `bmad-os-x` entry is still present afterwards), re-read `_config-driven.js:783-794` and the edited cell, and ran no fourth agent review.

GATE5_FINAL: PASS (user-accepted exception, 3 reviews plus one manual edit; no fourth review)
