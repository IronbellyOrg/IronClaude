# Reflect report: pre-execution check of the /sc:issue plan

```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.75
citations_total: 98
citations_revalidated: 98
citations_dropped: 0
citations_inferred: 2
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

- Spec: `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md` (476 lines)
- Plan: `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md` (6 phases, 16 tasks)
- Citation legend: `plan:N` is a line of the plan; `source.md:N` is a line of the spec; other paths are relative to the repo root.
- Merged verdict (adversarial, 3 heterogeneous reviewers): **FAIL**, 2 blocking and 16 minor findings, convergence 1.0, adversarial status partial (3 HIGH invariant-probe items folded into F-01 and F-02).

## Coverage

- Pass 1 (labelled IDs): 0 rows; the spec labels decisions B1-B15 and D1-D27, which the ID pattern does not match. `coverage_pct: null`.
- Pass 2 (quote-pinned inference): 67 rows, all quotes verified verbatim on their cited lines; 61 matched by the deterministic containment rule. `coverage_pct_union: 0.9104`; `unmapped_requirements_union: [INF-013, INF-023, INF-054, INF-058, INF-059, INF-062]`; `S_dev_density: 0.0896`.
- `coverage_degraded: parsed-sparse` forced Tier 2 (Step 1B.2b).
- Semantic disposition of the unmapped rows: INF-013 is covered by plan:92; INF-054 is an authorized exclusion at plan:24; INF-023 is finding F-05; INF-058, INF-059 and INF-062 are finding F-03.
- Reviewer 2 spot-checked spec regions outside the 67 rows (source.md:76-77, source.md:148-159, source.md:192-210, source.md:327-342) and found each carried by a task.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | Exactly one of `--claim` / `--create` is required; both or neither -> STOP with the usage block. | source.md:74 | containment (Task 8, 0.8571) |
| INF-002 | `--depth`, `--mode` or `--type` with `--claim` -> STOP (`E-CREATE-ONLY-FLAG`). | source.md:75 | containment (Task 8, 1.0) |
| INF-003 | There is no `--repo` flag (B10), no dry-run flag and no preview flag (B1). | source.md:79 | containment (Task 8, 0.75) |
| INF-004 | Each worker agent file sets `model: claude-gw-tier<N>` (one agent file per tier, because frontmatter is the only place a picker ID can be pinned). | source.md:131 | containment (Task 14, 0.75) |
| INF-005 | `SKILL.md` and every ref state: spawn workers with `subagent_type: issue-worker-t<N>` and **never pass the `model` parameter**. | source.md:132 | containment (Task 6, 0.9333) |
| INF-006 | the skill STOPs with `E-TIER-UNAVAILABLE`, naming the agent file and picker ID. It does not fall back to an alias (default D4). | source.md:134 | containment (Task 5, 0.7333) |
| INF-007 | The T1/T2 tier for the next-step chains is written into `next-steps.md` as a `/model claude-gw-tier1a` or `/model claude-gw-tier2` line before the chain | source.md:135 | containment (Task 4, 0.6471) |
| INF-008 | `gh issue edit <N> --repo <R> --add-assignee @me`. Failure -> STOP `E-ASSIGN-FAILED` (ClickUp is not touched). | source.md:162 | containment (Task 6, 0.6875) |
| INF-009 | If an earlier one exists, edit it with `gh api -X PATCH repos/<R>/issues/comments/<id> -F body=@<D>/accuracy-check.md` | source.md:178 | containment (Task 5, 0.8889) |
| INF-010 | Print the `next-steps.md` path and STOP. | source.md:180 | containment (Task 6, 0.8333) |
| INF-011 | Files are written to `<D>` = `.dev/issues/draft-<YYYYMMDD-HHMMSS>-<slug>/` until the issue exists, then the directory is renamed to `.dev/issues/<N>/` (default D10). | source.md:184 | containment (Task 5, 0.8824) |
| INF-012 | If it lists nothing, the issue is posted without any prompt. | source.md:212 | containment (Task 5, 0.6667) |
| INF-013 | Missing ones are listed in the final output, never created (B7). | source.md:215 | none (Task 2, 0.5) |
| INF-014 | No ClickUp call (B6). No self-assignment. | source.md:219 | containment (Task 5, 1.0) |
| INF-015 | Every posted template ends with its hidden marker line | source.md:270 | containment (Task 4, 0.8333) |
| INF-016 | holds the one-time `gh label create | source.md:282 | containment (Task 5, 0.6) |
| INF-017 | --issue-url <url> --issue-number <N> --repo <owner/repo> | source.md:289 | containment (Task 2, 1.0) |
| INF-018 | Never printed, logged or written to disk | source.md:296 | containment (Task 2, 1.0) |
| INF-019 | Exit 0 for every outcome above; exit 2 only for bad arguments. | source.md:310 | containment (Task 2, 1.0) |
| INF-020 | the unit tests pin them with recorded fixtures, and the implementation plan includes one manual smoke claim against a test task. | source.md:314 | containment (Task 15, 0.6) |
| INF-021 | Nothing else is consulted: not `gh repo set-default`, not `gh`'s fork-parent default, not a `--repo` flag (B10). | source.md:318 | containment (Task 5, 0.6667) |
| INF-022 | Every `gh issue`, `gh pr` and `gh label` call passes `--repo <R>` | source.md:319 | containment (Task 5, 0.75) |
| INF-023 | `git fetch origin` is the only fetch; no other remote is added or fetched. | source.md:321 | none (Task 1, 0.5714) |
| INF-024 | `src/superclaude/commands/issue.md` / Thin command (~100-150 lines) | source.md:352 | containment (Task 8, 1.0) |
| INF-025 | `name: sc:issue-protocol`; `allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion` | source.md:353 | containment (Task 6, 1.0) |
| INF-026 | Claim waves in detail; effort and complexity rubric (default D5); marker handling | source.md:354 | containment (Task 5, 1.0) |
| INF-027 | Create waves; flag-settling table; depth-to-worker table; contradiction prompt rule | source.md:355 | containment (Task 5, 1.0) |
| INF-028 | The six default chains of section 9 and the `/sc:recommend` goal format | source.md:356 | containment (Task 5, 1.0) |
| INF-029 | The fixed label set and the maintainer's one-time `gh label create` lines | source.md:357 | containment (Task 5, 0.8889) |
| INF-030 | Tier map, the pinning rule and its verified reason, `E-TIER-UNAVAILABLE` | source.md:358 | containment (Task 5, 0.875) |
| INF-031 | `issue-feature-simple.md`, `issue-feature-complex.md`, `issue-bug-simple.md`, `issue-bug-complex.md`, `summary.md` | source.md:359 | containment (Task 4, 1.0) |
| INF-032 | Section 12; standard library only; no secrets in output | source.md:360 | containment (Task 2, 0.8333) |
| INF-033 | runs `git remote get-url origin` and prints `owner/repo`; standard library only; exits non-zero with `E-NO-ORIGIN` otherwise. | source.md:361 | containment (Task 1, 0.9375) |
| INF-034 | `model: claude-gw-tier3`; `tools: Read, Grep, Glob, Write, Bash`; read-only on GitHub and code; writes only under `.dev/issues/`; returns its file path | source.md:362 | containment (Task 3, 1.0) |
| INF-035 | `src/superclaude/agents/issue-worker-t2.md` / Same shape, `model: claude-gw-tier2` | source.md:363 | containment (Task 3, 0.9231) |
| INF-036 | `src/superclaude/agents/issue-worker-t1.md` / Same shape, `model: claude-gw-tier1a` | source.md:364 | containment (Task 3, 0.9231) |
| INF-037 | No `src/superclaude/...` path appears in them | source.md:366 | containment (Task 5, 0.8) |
| INF-038 | One row in the "Other commands" table | source.md:372 | containment (Task 8, 1.0) |
| INF-039 | Byte-for-byte copy of the edited guide (required by `tests/commands/test_routing_plugin_parity.py`) | source.md:373 | containment (Task 10, 1.0) |
| INF-040 | Section 4.1: the optional `model:` field also takes a full model ID or picker ID | source.md:374 | containment (Task 11, 1.0) |
| INF-041 | One row in "8. UTILITIES" | source.md:375 | containment (Task 12, 1.0) |
| INF-042 | Replace `test_no_issue_skill_or_command_added` (section 16) | source.md:376 | containment (Task 9, 1.0) |
| INF-043 | Add `"sc:issue"` to `_OTHER_COMMANDS` | source.md:377 | containment (Task 10, 1.0) |
| INF-044 | Add `"issue"` to `_POST_REFRESH_ADDITIONS` | source.md:378 | containment (Task 9, 1.0) |
| INF-045 | `tests/commands/test_issue_command.py` (new) | source.md:390 | containment (Task 8, 0.8) |
| INF-046 | `tests/skills/test_issue_protocol.py` (new) | source.md:391 | containment (Task 7, 0.8) |
| INF-047 | `tests/skills/test_issue_worker_agents.py` (new) | source.md:392 | containment (Task 3, 0.8) |
| INF-048 | `tests/skills/test_clickup_claim.py` (new) | source.md:393 | containment (Task 2, 0.8) |
| INF-049 | `tests/skills/test_issue_repo_resolution.py` (new) | source.md:394 | containment (Task 1, 0.8) |
| INF-050 | `test_no_issue_skill_or_command_added` becomes `test_issue_command_and_skill_are_the_only_issue_primitives` | source.md:395 | containment (Task 9, 0.6667) |
| INF-051 | Run before commit: `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py`, then `make test`. | source.md:400 | containment (Task 16, 0.8667) |
| INF-052 | `make sync-dev`, then `make verify-sync`. | source.md:405 | containment (Task 13, 1.0) |
| INF-053 | Run `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` and justify any new hit | source.md:407 | containment (Task 13, 0.8462) |
| INF-054 | Open the PR only with `/sc:pr-submit --monitor 3 | source.md:408 | none (Task 3, 0.3333) |
| INF-055 | The plan's smoke step confirms one spawn per worker | source.md:434 | containment (Task 14, 0.75) |
| INF-056 | The command file and `SKILL.md` each state in one line that | source.md:441 | containment (Task 5, 0.8333) |
| INF-057 | `/sc:issue --claim <N>` on an open, unassigned issue of the origin repo: the T3 worker runs first | source.md:467 | containment (Task 4, 0.6667) |
| INF-058 | Running the same claim again edits both comments; the comment count on the issue does not grow. | source.md:468 | none (Task 5, 0.5) |
| INF-059 | A closed issue, or one assigned to someone else, stops with the stated message and makes no GitHub or ClickUp write. | source.md:469 | none (Task 5, 0.5833) |
| INF-060 | A claim URL for any repo other than origin stops with `E-FOREIGN-REPO` | source.md:470 | containment (Task 6, 0.75) |
| INF-061 | With `CLICKUP_API_TOKEN` unset the claim completes and the comment says ClickUp was skipped | source.md:471 | containment (Task 2, 0.625) |
| INF-062 | at `standard`/`deep` a disagreement produces one marked pushback comment; no ClickUp call is made. | source.md:472 | none (Task 5, 0.4) |
| INF-063 | one manual smoke run per worker shows it was served by the pinned tier. | source.md:473 | containment (Task 14, 0.8889) |
| INF-064 | `next-steps.md` contains only commands and flags listed in section 19 | source.md:474 | containment (Task 4, 0.8889) |
| INF-065 | `make verify-sync` passes; the tests of section 16 pass | source.md:475 | containment (Task 16, 0.875) |
| INF-066 | Every brainstorm row passes `--models opus,sonnet` | source.md:237 | containment (Task 7, 1.0) |
| INF-067 | Not changed: `src/superclaude/core/CLAUDE.md` (rule 10 stays; no level-table change) | source.md:380 | containment (Task 6, 0.6667) |

Postscript: 0 inferred rows dropped by quote verification.

## Findings

### Finding F-01 (blocking, ordering): the final suite/lint/staging task sits behind two tasks that may block

- **Location:** plan:228
- **Evidence:** Task 16 `Depends on: Task 13, Task 14, Task 15` (plan:228); Task 14 and Task 15 acceptance criteria require "reported as blocked rather than passed" (plan:213, plan:223); `/sc:implement` stops on a task that is not complete until the user confirms a Ruling (src/superclaude/skills/sc-implement-protocol/SKILL.md:135; src/superclaude/skills/sc-implement-protocol/refs/ledger.md:155).
- **Classification rationale:** wrong behaviour: the only task that runs the full suite, `make lint` and `git add .dev/tasks` (plan:230-236) can be stranded by an environment fact.
- **Default remediation:** run the suite task before the smoke checks, rewrite the smoke checks' criteria as truthful-evidence criteria, re-sync and re-test after any Task 15 edit, and stage after each smoke task.

### Finding F-02 (blocking, security): Task 15 routes the ClickUp token through the session

- **Location:** plan:219
- **Evidence:** Task 15 says "ask the user for them" and runs the script "with those variables set in the environment" (plan:219); the spec forbids printing, logging or writing the token (source.md:296).
- **Classification rationale:** security risk: a token typed into the conversation or inlined in a command is persisted in the session record.
- **Default remediation:** the user exports the variables in their own shell before the session; the executor never asks for, echoes or inlines the value; Task 2's no-token check runs with `env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID` and the tests clear both variables; the live-shape comparison compares key paths only and never copies live values into fixtures.

### Minor findings (F-03 to F-18)

- F-03: no task runs or records section 20 acceptance criteria 1, 2, 3, 4 and 6 (source.md:465-472; plan:25).
- F-04: no static test that every `gh issue|pr|label` line carries `--repo` and no `{owner}/{repo}` placeholder appears (source.md:319; plan:121).
- F-05: the origin-only `git fetch origin` rule is not assigned to claim.md or the worker body, and conflicts with "read-only gh and git calls" (source.md:149; plan:55; plan:91).
- F-06: Task 11's `git diff --stat` criterion cannot hold after Tasks 9-10 (plan:178).
- F-07: Task 10 does not state the ASCII and live-reference rules for the new row (plan:159; tests/core/test_how_we_work_routing_table.py:341).
- F-08: Task 2's no-token check does not unset the variables (plan:49).
- F-09: the never-pass-`model` rule must be in every ref, not only tiers.md (source.md:132; plan:95).
- F-10: Task 14 needs a fresh session and names no checkable served-model evidence (plan:209).
- F-11: Task 7's flag test reads the installed command copy first, making it machine-dependent (plan:121; tests/core/test_how_we_work_routing_table.py:141).
- F-12: Task 13 compares against local `master` rather than `origin/master` (plan:198).
- F-13: `.dev/issues/smoke/` and the Orca worktree are outside the Constraints' edit scope; the worktree is never removed (plan:20; plan:230).
- F-14: coverage-matrix best-task notes for five rows are string matches, not task satisfaction (no plan change).
- F-15: the spec's merged-PR query has no `--limit` (gh default 30) (source.md:149).
- F-16: first page number and invalid `CLICKUP_MAX_PAGES` behaviour are undefined (source.md:304).
- F-17: [INFERRED] tests that load scripts by path may write `__pycache__` files that the path greps then match.
- F-18: [INFERRED] `wc -l` and a Python line count differ by one on a file with no final newline (plan:112).

## Recommendations

### Recommendation R-001: Reorder the end of the plan and rewrite the smoke-check criteria

- **File:** .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md
- **Change:** make the full-suite/lint/sync/staging task depend on Task 13 only and run before the smoke checks; replace "reported as blocked" with truthful-evidence criteria; re-sync and re-test after any ClickUp fixture edit; stage after each smoke task.
- **Verifier:** re-run `/sc:reflect --mode pre` on the edited plan; no `Depends on` names a smoke task from the suite task.
- **Linked finding(s):** F-01
- **Priority:** P0

### Recommendation R-002: Keep the ClickUp token out of the session

- **File:** same plan file, Task 2 and the ClickUp smoke task
- **Change:** user pre-exports the variables; executor never asks for or prints them; `env -u` on the no-token check; tests clear both variables; key-path-only shape comparison.
- **Verifier:** re-run `/sc:reflect --mode pre`; grep the plan for "ask the user for them" returns nothing.
- **Linked finding(s):** F-02, F-08
- **Priority:** P0

### Recommendation R-003: Fold the minor findings into the tasks they name

- **File:** same plan file
- **Change:** apply F-03 to F-13 and F-15 to F-18 recommendations from `adversarial/merged-verdict.yaml`.
- **Verifier:** each finding's cited plan line carries the change.
- **Linked finding(s):** F-03 to F-18
- **Priority:** P1

## Inferred-claim audit

- `citations_inferred: 2`
- Inferred-fraction: `2 / 98` = 0.02
- Evidence validator: full re-read of 98 citations, 0 dropped (`zero-drop-flag: true` recorded in audit.log for meta-eval spot-check).
