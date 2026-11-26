# Reflection report: pre-execution review of the plan TASK-WF-scopeCut-20261126-165750 (depth quick, Tier 1)

```yaml
contract_version: 1.9.0
status: partial
mode: pre
tier_reached: 1
confidence_calibrated: 0.65
citations_total: 23
citations_revalidated: 23
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

> **WARN (overridden pre-filter).** `--depth quick` is a hard override of the tier rubric (SKILL.md section 5.1) and outranks the `coverage_degraded: parsed-sparse` pre-filter and the calibrated confidence of 0.65, so this run stops at Tier 1. No Tier 2 reviewers ran. The independent check in this report is the blind calibrator's own review of the plan, on top of its grading of the T1 card. The two earlier plans for the larger design each got a full Tier 2 review.

## Verdict

**FAIL for the plan: 1 Blocking, 8 Medium, 2 Note findings.**

- **What:** the plan (7 tasks, 3 phases) is a small script with a dry run plus an operator page. It covers 11 of 16 spec rows by the containment rule (0.6875); the 5 unmatched rows are carried by the Constraints or are the deliberate dropped parts. One Blocking finding: the plan's `--apply` never prints what it did, although the spec says it prints the written ids, the issue comment line and the rollback commands; with no state file those printed lines are the only rollback record.
- **Why it matters:** an implementer who follows the plan literally builds a script whose `apply_repo` returns the ids but whose command line shows nothing, and Task 6's operator steps ("comment the ids on issue 838") depend on that output.
- **Recommended action:** repair F-1 on a copy of the plan (workflow Wave 4R, surgical route). Medium findings are never repaired by that route; they are listed as follow-up candidates. Verifier: a re-review of the repaired plan finds F-1 resolved.

## Coverage (UC-1)

| Field | Value |
|---|---|
| Parsed requirement IDs | 0 |
| Inferred requirements (Pass 2) | 16 valid of 16 emitted (one per requirement-bearing line; coarse) |
| `coverage_pct` (parsed only) | null |
| `coverage_pct_union` | 0.6875 (11 of 16) |
| `S_dev_density` | 0.3125 |
| `coverage_degraded` | parsed-sparse |
| Unmapped (union) | INF-001, INF-002, INF-004, INF-006, INF-016 |

## Findings

### F-1 [Blocking (Missing)] `--apply` never prints its results
- Claim: the spec says `--apply` prints what was written on a failure, the one-line comment for issue 838 on success, and the manual rollback command for each id it created. The plan's `apply_repo` returns those, but Task 5's `main` is not required to print them and no acceptance check looks at the output.
- Citations: source.md:42 "stop at the first failure and print what was written"; source.md:42 "On success print the one-line comment for issue 838"; source.md:44 "the script prints, and the page lists, the `gh api --method DELETE"; plan:85 "It returns the ids by name and the one-line comment text"; plan:85 "It also returns the manual rollback commands"; plan:106 "with `--apply` it builds a runner that may POST and calls `apply_repo`".
- Consequence if corrected: Task 5 gains a printing step and an acceptance check; Task 6's "comment the ids" step then has an input.
- Recommendation: Task 5: `main` prints the ids, the comment line and one DELETE command per created id; on a failure it prints what was written before stopping. Add the check "a successful fake `--apply` prints the comment line and one DELETE per id; a read-back failure prints the one written id and exits `EXIT_FAILED`". Verifier: `test_cli.py`.

### F-2 [Medium] The dry run does not stop on a refusal reason
- Claim: the spec stops on an archived repo, no admin or no default branch; the plan tests that refusal only in `--apply`, and with no default branch the set of branches to check is undefined.
- Citations: source.md:35 "Archived, no admin, or no default branch: stop with a refusal naming it."; plan:85 "itself calls `read_repo`, `check_push` and `read_existing`".
- Consequence if corrected: one stop and three acceptance checks are added.
- Recommendation: the dry run stops after reading the repo, exits `EXIT_FAILED` and names the reason; add a check per reason in `test_cli.py`.

### F-3 [Medium] An "unknown" protection state passes the apply check
- Claim: `read_existing` records any answer other than 200 or 404 as unknown, but the refusals of `apply_repo` name only classic protection.
- Citations: plan:70 "anything else is recorded as unknown"; source.md:37 "A classic-protection hit refuses `--apply`".
- Consequence if corrected: one refusal and one check are added.
- Recommendation: add "no branch has an unknown protection state" to the refusals of Task 4 and its acceptance. Verifier: `test_apply.py`.

### F-4 [Medium] The timed-out POST check is weaker than the task text
- Claim: the task text says one list call before any other call; the acceptance says only that a list call follows and no second POST. Code that posts the next ruleset before the list still passes, and nothing says what happens when the list shows no match.
- Citations: plan:95 "followed by a list call and never by a second POST"; source.md:42 "a list call before anything else".
- Consequence if corrected: one acceptance line is tightened and one case added.
- Recommendation: require that the call recorded right after the timed-out POST is the list call, and that the run stops as a failure when the list shows no match. Verifier: `test_apply.py`.

### F-5 [Medium] The push-check fallback is half-tested and ambiguous
- Claim: the spec falls back to commits on 403, 404 or a pagination cap; the plan tests only the 403 case and says "a truncated page chain" gives `incomplete` without naming the source.
- Citations: source.md:36 "unavailable (403 or 404) or paginates past a cap, fall back to"; plan:77 "a truncated page chain".
- Consequence if corrected: two cases are added and one phrase reworded.
- Recommendation: add cases where a 404 and an over-the-cap activity feed both fall back; reword to "a truncated commits chain gives `incomplete`". Verifier: `test_checks.py`.

### F-6 [Medium] The private-name test can silently check fewer names
- Claim: the page test reads the 17 names after a marker phrase with no end marker and no count check; two of the names (verified from the pasted list) contain a full stop, so a parser that ends the list at the first full stop checks fewer names and cannot fail for the rest.
- Citations: plan:127 "the comma-separated names after".
- Consequence if corrected: the parse rule and a count check are added.
- Recommendation: end the list at the text ". That list", split on ", ", and assert exactly 17 names before checking. Verifier: `test_page.py`.

### F-7 [Medium] The pull request must not close issue 838, and the plan does not say so
- Claim: the spec says the pull request refers to the issue and does not close it; no Constraint carries it.
- Citations: source.md:7 "refers to issue 838".
- Consequence if corrected: one Constraints line is added.
- Recommendation: add a Constraint: no closing keyword for issue 838; the pull request lists source.md section 5 and the choices of the Constraints.

### F-8 [Medium] Task 7's lint check cannot be decided
- Claim: Task 7 closes with `ruff check .` "reports nothing new" with no baseline, while every other task has the scoped command that must report nothing.
- Citations: plan:140 "`uv run ruff check .` reports nothing new".
- Consequence if corrected: one command changes.
- Recommendation: use the scoped command of the Constraints, or record the `ruff check .` output before Task 1 as the baseline.

### F-9 [Medium] Nothing checks that the dry run gets a read-only runner
- Claim: `main` builds a read-only runner for the dry run, but the test passes its own runner, so the code path where `main` builds the runner is never run, and with a read-only runner "no POST is recorded" is always true because a refused call is not recorded.
- Citations: plan:106 "A runner passed in (tests) is used as given"; source.md:31 "A runner built with `read_only=True` (the dry run) refuses POST".
- Consequence if corrected: one check is added.
- Recommendation: add a check with `runner=None` and a stand-in for `Runner`: `main` uses `read_only=True` without `--apply` and `read_only=False` only with it. Verifier: `test_cli.py`.

### F-10 [Note] The page check disagrees with an org-level command
- Claim: the page must write every command with `OWNER` and `REPO`, yet the acceptance also allows `<org>`, and the existing guide has an org-level command that cannot carry `REPO`.
- Citations: plan:122 "writes every command with the variables `OWNER` and `REPO`"; plan:125 "or the placeholder `<org>`".
- Consequence if corrected: wording only.
- Recommendation: repo-level commands use `$OWNER` and `$REPO`, org-level ones use `$OWNER`; make the two lines agree.

### F-11 [Note] "names" the ruleset ids is stricter than the spec
- Claim: the plan forbids any call that names the ruleset ids 28081842, 28081844 or 28081845; the spec forbids a call that writes to them.
- Citations: source.md:42 "No call ever writes to the ruleset ids"; plan:85 "never makes a call that names the ruleset ids".
- Consequence if corrected: wording only.
- Recommendation: use the spec's wording, "writes to".

## Evidence (citations checked by the evidence validator)

23 citations, every one re-read (full re-read: 23 is the whole population). Locations are `source.md:N` (the spec) and `plan:N` (the plan) in `.dev/tasks/to-do/TASK-WF-scopeCut-20261126-165750/`.

| ID | Finding | Location | Quote | Result |
|---|---|---|---|---|
| E-001 | F-1 | source.md:42 | stop at the first failure and print what was written | verified |
| E-002 | F-1 | source.md:42 | On success print the one-line comment for issue 838 | verified |
| E-003 | F-1 | source.md:44 | the script prints, and the page lists, the `gh api --method DELETE | verified |
| E-004 | F-1 | plan:85 | It returns the ids by name and the one-line comment text | verified |
| E-005 | F-1 | plan:85 | It also returns the manual rollback commands | verified |
| E-006 | F-1 | plan:106 | with `--apply` it builds a runner that may POST and calls `apply_repo` | verified |
| E-007 | F-2 | source.md:35 | Archived, no admin, or no default branch: stop with a refusal naming it. | verified |
| E-008 | F-2 | plan:85 | itself calls `read_repo`, `check_push` and `read_existing` | verified |
| E-009 | F-3 | plan:70 | anything else is recorded as unknown | verified |
| E-010 | F-3 | source.md:37 | A classic-protection hit refuses `--apply` | verified |
| E-011 | F-4 | plan:95 | followed by a list call and never by a second POST | verified |
| E-012 | F-4 | source.md:42 | a list call before anything else | verified |
| E-013 | F-5 | source.md:36 | unavailable (403 or 404) or paginates past a cap, fall back to | verified |
| E-014 | F-5 | plan:77 | a truncated page chain | verified |
| E-015 | F-6 | plan:127 | the comma-separated names after | verified |
| E-016 | F-7 | source.md:7 | refers to issue 838 | verified |
| E-017 | F-8 | plan:140 | `uv run ruff check .` reports nothing new | verified |
| E-018 | F-9 | plan:106 | A runner passed in (tests) is used as given | verified |
| E-019 | F-9 | source.md:31 | A runner built with `read_only=True` (the dry run) refuses POST | verified |
| E-020 | F-10 | plan:122 | writes every command with the variables `OWNER` and `REPO` | verified |
| E-021 | F-10 | plan:125 | or the placeholder `<org>` | verified |
| E-022 | F-11 | source.md:42 | No call ever writes to the ruleset ids | verified |
| E-023 | F-11 | plan:85 | never makes a call that names the ruleset ids | verified |

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 23` = 0.00

## Recommendations

### Recommendation R-001: Print the apply results from `main`

- **File:** .dev/tasks/to-do/TASK-WF-scopeCut-20261126-165750/TASK-WF-scopeCut-20261126-165750.md
- **Change:** Task 5: `main` prints the created ids, the comment line and one DELETE command per created id, and on a failure prints what was written before stopping; add the matching acceptance check.
- **Verifier:** `test_cli.py` asserts the printed comment line and one DELETE per id, and a read-back failure prints the one written id and exits `EXIT_FAILED`.
- **Linked deviation(s):** F-1
- **Priority:** P0

### Recommendation R-002: Medium findings as follow-up candidates

- **File:** .dev/tasks/to-do/TASK-WF-scopeCut-20261126-165750/TASK-WF-scopeCut-20261126-165750.md
- **Change:** F-2 to F-9 are not repaired by the workflow remediation route; they go to the implementation stage as notes and to the pull request as follow-up candidates.
- **Verifier:** the pull request body lists F-2 to F-9.
- **Linked deviation(s):** F-2, F-3, F-4, F-5, F-6, F-7, F-8, F-9
- **Priority:** P1

## How this review was run

- **Tier 1 only.** The T1 card was written by the orchestrator (inline), graded blind by a separate calibrator (C 0.65, scores 0.75, 0.70, 0.35, 0.55, 0.90), and the same calibrator reviewed the plan against the spec independently (the findings above). The card's own candidates C1 and C2 were Notes and are folded into F-9; its C3 was regraded to a Note by the calibrator (the plan follows the spec there) and is carried in the pull request as a choice, not as a finding.
- **Degradations, stated plainly.** No Tier 2 reviewers and no adversarial merge (depth quick). `calibrator_diversity` is not applicable. The calibrator could not send its report by message, so the orchestrator took it from the reply. Pass 2 rows are mechanical (one per requirement-bearing line), so the coverage figure is coarse.
- **Not run:** no code was executed and no live call was made.
