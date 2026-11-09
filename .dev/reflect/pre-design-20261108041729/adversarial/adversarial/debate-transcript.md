# Adversarial Debate Transcript

Note: the sections below are the orchestrator's faithful condensation of each advocate's returned text (the full returns are in the background-task output files of the three advocate runs). Citations and verdicts are kept; prose is shortened.

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 100% (15 of 15 points settled by at least 2 of 3 advocates; 4 settled by all 3 with no qualification)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3 (variant 1 sonnet, variant 2 haiku, variant 3 opus; all run as the read-only `reflect-reviewer` agent type)
- Advocates verified claims by reading the repo files; none ran commands.

## Round 1: Advocate Statements

### Variant 1 Advocate (sonnet)
- Position: V1 found the one defect that breaks CI deterministically (the exact-text classification table in `tests/skills/test_worker_contract.py`). V3 is the more complete reviewer; V2 is deeper on test strength but overstates severity.
- Steelman of V2: a plan whose tests only check that words appear gives false assurance; Task 8 says "exact line formats" but lists three prefixes (plan:122) while Task 1 needs full formats (plan:39). Also correct that the Will / Will Not test reads only `SKILL` (`test_issue_protocol.py:527-541`).
- Steelman of V3: broadest repo grounding; names `docs/designs/sc-issue-command.md:34,330,331`, the spaces in `orgs/<owner of R>/issue-fields` that defeat an `orgs/\S+` scanner, and the unowned `Issue type` row.
- Strengths claimed: C-001 cited ranges all verified (:1948-1951, :2005-2012, :3006-3013, :3022-3037, :3086-3093, :3133-3138, :3150-3156); C-003 command/worker test files unrun; C-004 plan names `complexity-field` zero times; C-005 mode label as well as comment.
- Concessions: R1-F6 overstated for Task 4 (Task 8 test 5 asserts the scout headings); R1-F4's proposed regex is incomplete (spaces); ok-check row inside findings is noise; the OK credit on the Will / Will Not test was unearned.
- Shared assumptions: A-002 QUALIFY (the classification keys must be rebuilt from post-edit text); A-003 ACCEPT (`make lint` = lint-architecture + ruff, none read the wording).

### Variant 2 Advocate (haiku)
- Position: V2 is strongest on whether the proposed tests protect the behaviour; V1 and V3 found the most concrete failure (C-001) and V2 missed it.
- Steelman of V1: local protocol-test success hides failures elsewhere; classification keys are whole source lines (`test_worker_contract.py:3006`). Steelman of V3: instruction surface must agree across files (`docs/designs/sc-issue-command.md:330-331`).
- Strengths claimed: R2-F1 exact formats (design:65-67 vs plan:122); R2-F2 Q7 precedence and Q8 pairs not pinned by name-only checks; R2-F3 Will / Will Not test reads only SKILL; R2-F4 constraint contradiction.
- Concessions: missed C-001, C-003, C-004; "blocking" too strong for R2-F1/F2 (material verification drift, not demonstrated failure); R2-F4 incomplete (mode label).
- Weaknesses found in others: V1's Task 4 revert claim wrong as stated; V3's R3-F4 and R3-F5 partly covered by Tasks 2 and 10.
- Shared assumptions: A-002 REJECT (plan line 25 requires re-reading before each edit); A-003 QUALIFY (not a lint result until Task 12 runs).

### Variant 3 Advocate (opus)
- Position: V3's blocking finding is correct and the most important; most minor findings hold; R3-F5 is unique to V3. V3 missed the test-strength gaps (C-002), the "exactly two things" contradiction (C-005), and C-009.
- Steelman of V1/V2 as above; verified R3-F1 at every cited point and CI runs the full suite (`.github/workflows/test.yml:47`).
- Concessions: R3-F4's `create.md:34` half already in Task 2; R3-F7 describes a pre-existing inconsistency (`SKILL.md:107` vs `:121`); R3-F5 partly covered by Task 10's acceptance; R3-F6 overlaps R1-F4.
- Weaknesses found in others: V2 missed C-001 and overstated severities (design test 6 itself is names-only, so this is an inherited design weakness, Medium); V1's ok-check on the Will / Will Not test is wrong; V1's R1-F6 should cite Task 3, not Task 4, as the unprotected change.
- Shared assumptions: A-002 QUALIFY; A-003 ACCEPT.

## Scoring Matrix

| Diff point | Winner / validity | Confidence | Evidence summary |
|---|---|---|---|
| S-001 | No substantive winner (V3 cleaner) | 60% | Card shape does not affect correctness; V1 includes a noise ok-check finding |
| S-002 | V1 and V3 | 65% | Repo-level file:line citations verified directly |
| C-001 | Finding valid (V1, V3) | 95% | `test_worker_contract.py:3006-3093` keys equal lines Tasks 2, 3, 5 rewrite; CI runs the full suite |
| C-002 | V2, at Medium not blocking | 75% | Plan:122 checks prefixes and names; design tests 4 and 6 are equally loose; `orgs/` regex needs spaces (V3) and a prose guard (V1) |
| C-003 | Finding valid, minor (V3 most concrete) | 80% | `test_issue_command.py:98-123`, `test_issue_worker_agents.py:93-105` unrun |
| C-004 | Finding valid (V1, V3) | 85% | `SKILL.md:52`, `create.md:7`, `commands/issue.md:78`; plan never names the file |
| C-005 | V1 | 85% | Plan:23 vs mode label and pushback comment (plan:47) |
| C-006 | Valid in part (V1, V3) | 65% | `create.md:36` "relabelled" unowned; `create.md:34` already in Task 2 |
| C-007 | Valid (V3 only) | 80% | `docs/designs/sc-issue-command.md:34,330,331` missing from Task 10's list; 331 clearly |
| C-008 | Valid, Low (V3) | 65% | `SKILL.md:107` and the `labels_*` narrowing; ambiguity pre-dates the change |
| C-009 | V2 | 90% | `test_issue_protocol.py:527-541` reads only SKILL |
| C-010 | V1 principle; not actionable | 60% | Matrix task ids are word matches, not coverage proof |
| X-001 | V1, narrowed to Task 3 | 65% | Task 4 revert is caught by test 5; Task 3's additions are pinned by no new Task 8 test |
| A-002 | QUALIFY (2 of 3) | 70% | Cited lines hold today; keys must be rebuilt from post-edit text |
| A-003 | ACCEPT (2 of 3) | 70% | Lint checks do not read the wording; Task 12 gates on `make lint` |

## Convergence Assessment
- Points resolved: 15 of 15 (taxonomy: L1 5 points, L2 7 points, L3 3 points; all three levels covered)
- Alignment: 100%
- Threshold: 80%
- Status: CONVERGED
- Unresolved points: none. Residual disagreement is about severity only: V2 labelled C-002 blocking; V1 and V3 advocates place it at Medium, and V2's advocate conceded the label was too strong.
- Caveat: agreement is on validity of findings, each re-read against the repo by at least two advocates; it is not agreement on an unchecked answer.
