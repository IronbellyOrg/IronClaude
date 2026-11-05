# Reflect report: pre-execution check round 2 of the /sc:issue plan (version 2)

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.76
citations_total: 236
citations_revalidated: 236
citations_dropped: 2
citations_inferred: 8
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

- Spec: `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/source.md` (475 lines, byte-identical to `docs/designs/sc-issue-command.md`, checked with `cmp`)
- Plan: `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md` (version 2, revised after check round 1; 6 phases, 17 tasks)
- Citation legend: `plan:N` is a line of the plan; `source.md:N` is a line of the spec; other paths are relative to the repo root.
- Merged verdict (adversarial, 3 heterogeneous reviewers: sonnet analyzer, haiku served by glm-5.3 qa, opus refactorer): **PASS with notes**, 0 blocking and 18 minor findings, convergence 1.0 (19 of 19 points), adversarial status partial (BLOCKED_BY_INVARIANTS: 1 HIGH invariant-probe item, INV-001, folded into F-01).
- Round 1 fixes: both round-1 blocking findings are fixed in version 2 (`round1_fix_check: {F-01: fixed, F-02: fixed}`; reviewer-1 card).
- Run history: this round started 08:17 UTC; an API outage interrupted it during the Round 2.5 invariant probe. It was resumed in the same folder after 12:41 UTC: the probe was re-run, base selection was regenerated (the old worker's 12:40:48 copy is kept as `adversarial/adversarial/base-selection.partial-1240.md` and was not used), and the refactor plan, merge and this report were produced. The input tree hash recomputed at 12:44 and again at 13:17 UTC equals the snapshot taken at 08:19-08:20 (`artifacts/input-snapshot.yaml`; audit.log Wave 0 step 0.4), so no input drifted.
- Status is `partial` only because the evidence validator dropped 2 items (see Grounding Gaps); the merged verdict itself is PASS with notes and no finding is blocking.

## Coverage

- Pass 1 (labelled IDs): 0 rows; the spec labels decisions B1-B15 and D1-D27, which the ID pattern does not match. `coverage_pct: null`.
- Pass 2 (quote-pinned inference): 67 rows, 67 of 67 quotes verified verbatim on their cited lines; 60 matched by the deterministic containment rule: `coverage_pct_union: 0.8955`; `unmapped_requirements_union: [INF-013, INF-020, INF-054, INF-058, INF-059, INF-061, INF-062]`; `S_dev_density: 0.1045`.
- `coverage_degraded: parsed-sparse` forced Tier 2 (Step 1B.2b); rule 4 (`S_domains` 4) fired (`artifacts/tier_decision.yaml`).
- Semantic disposition of the seven unmapped rows (string containment fell below 0.6; each was checked by hand against the plan):
  - INF-013 (missing labels never created) is carried by Task 5's create.md (plan:93, "never created (B7)").
  - INF-020 (one manual smoke claim) is Task 16 (plan:243).
  - INF-054 (PR via `/sc:pr-submit`) is an authorized deferral in the Constraints (plan:25).
  - INF-058, INF-059 and INF-062 (section 20 items 2, 3 and 6) are recorded run-or-pending by Task 17 (plan:254); their behaviour is specified in Task 5 (plan:92, plan:93).
  - INF-061 (AC 5 first half) is finding F-08.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | Exactly one of `--claim` / `--create` is required; both or neither -> STOP with the usage block. | source.md:74 | containment (Task 8, 0.8571) |
| INF-002 | `--depth`, `--mode` or `--type` with `--claim` -> STOP (`E-CREATE-ONLY-FLAG`). | source.md:75 | containment (Task 8, 1.0) |
| INF-003 | There is no `--repo` flag (B10), no dry-run flag and no preview flag (B1). | source.md:79 | containment (Task 8, 0.75) |
| INF-004 | Each worker agent file sets `model: claude-gw-tier<N>` (one agent file per tier, because frontmatter is the only place a picker ID can be pinned). | source.md:131 | containment (Task 15, 0.6875) |
| INF-005 | `SKILL.md` and every ref state: spawn workers with `subagent_type: issue-worker-t<N>` and **never pass the `model` parameter**. | source.md:132 | containment (Task 5, 1.0) |
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
| INF-016 | holds the one-time `gh label create | source.md:282 | containment (Task 3, 0.6) |
| INF-017 | --issue-url <url> --issue-number <N> --repo <owner/repo> | source.md:289 | containment (Task 2, 1.0) |
| INF-018 | Never printed, logged or written to disk | source.md:296 | containment (Task 2, 1.0) |
| INF-019 | Exit 0 for every outcome above; exit 2 only for bad arguments. | source.md:310 | containment (Task 2, 1.0) |
| INF-020 | the unit tests pin them with recorded fixtures, and the implementation plan includes one manual smoke claim against a test task. | source.md:314 | none (Task 2, 0.5333) |
| INF-021 | Nothing else is consulted: not `gh repo set-default`, not `gh`'s fork-parent default, not a `--repo` flag (B10). | source.md:318 | containment (Task 5, 0.6667) |
| INF-022 | Every `gh issue`, `gh pr` and `gh label` call passes `--repo <R>` | source.md:319 | containment (Task 5, 1.0) |
| INF-023 | `git fetch origin` is the only fetch; no other remote is added or fetched. | source.md:321 | containment (Task 3, 1.0) |
| INF-024 | `src/superclaude/commands/issue.md` \| Thin command (~100-150 lines) | source.md:352 | containment (Task 8, 1.0) |
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
| INF-035 | `src/superclaude/agents/issue-worker-t2.md` \| Same shape, `model: claude-gw-tier2` | source.md:363 | containment (Task 3, 0.9231) |
| INF-036 | `src/superclaude/agents/issue-worker-t1.md` \| Same shape, `model: claude-gw-tier1a` | source.md:364 | containment (Task 3, 0.9231) |
| INF-037 | No `src/superclaude/...` path appears in them | source.md:366 | containment (Task 2, 0.8) |
| INF-038 | One row in the "Other commands" table | source.md:372 | containment (Task 3, 1.0) |
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
| INF-051 | Run before commit: `uv run pytest tests/commands tests/core tests/skills tests/recommend tests/cli/test_issue_body_templates.py`, then `make test`. | source.md:400 | containment (Task 14, 0.8667) |
| INF-052 | `make sync-dev`, then `make verify-sync`. | source.md:405 | containment (Task 13, 1.0) |
| INF-053 | Run `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` and justify any new hit | source.md:407 | containment (Task 13, 0.7692) |
| INF-054 | Open the PR only with `/sc:pr-submit --monitor 3 | source.md:408 | none (Task 3, 0.5) |
| INF-055 | The plan's smoke step confirms one spawn per worker | source.md:434 | containment (Task 4, 0.625) |
| INF-056 | The command file and `SKILL.md` each state in one line that | source.md:441 | containment (Task 5, 1.0) |
| INF-057 | `/sc:issue --claim <N>` on an open, unassigned issue of the origin repo: the T3 worker runs first | source.md:467 | containment (Task 5, 0.75) |
| INF-058 | Running the same claim again edits both comments; the comment count on the issue does not grow. | source.md:468 | none (Task 5, 0.5) |
| INF-059 | A closed issue, or one assigned to someone else, stops with the stated message and makes no GitHub or ClickUp write. | source.md:469 | none (Task 5, 0.5833) |
| INF-060 | A claim URL for any repo other than origin stops with `E-FOREIGN-REPO` | source.md:470 | containment (Task 5, 0.875) |
| INF-061 | With `CLICKUP_API_TOKEN` unset the claim completes and the comment says ClickUp was skipped | source.md:471 | none (Task 2, 0.5) |
| INF-062 | at `standard`/`deep` a disagreement produces one marked pushback comment; no ClickUp call is made. | source.md:472 | none (Task 5, 0.4) |
| INF-063 | one manual smoke run per worker shows it was served by the pinned tier. | source.md:473 | containment (Task 15, 1.0) |
| INF-064 | `next-steps.md` contains only commands and flags listed in section 19 | source.md:474 | containment (Task 4, 0.8889) |
| INF-065 | `make verify-sync` passes; the tests of section 16 pass | source.md:475 | containment (Task 14, 0.875) |
| INF-066 | Every brainstorm row passes `--models opus,sonnet` | source.md:237 | containment (Task 5, 1.0) |
| INF-067 | Not changed: `src/superclaude/core/CLAUDE.md` (rule 10 stays; no level-table change) | source.md:380 | containment (Task 6, 0.6667) |

Postscript: 67 of 67 quotes verified on their cited lines; 0 inferred rows dropped by quote verification (orchestrator script and the Wave 5 evidence validator, `artifacts/evidence-validator-inf.md`). The "Match result" column is a deterministic string score: its best-task name is wrong or weak for INF-004, INF-016, INF-037, INF-038, INF-055, INF-056 and INF-067 (and partial for INF-008, INF-012, INF-021, INF-060); the validator confirmed each of those requirements is still carried by the plan and named the real carrier tasks in that artifact. Do not cite a task from this column without checking it.

## Findings

No blocking finding. All 18 findings are minor under the binding rule (blocking only for wrong behaviour, a false claim, a missing required deliverable, or a security/data-loss risk). F-01 is the top-priority minor: its fix should be applied before Task 17's live item-4 run.

### Finding F-01 (minor, safety-risk)

- **Claim:** plan:26 exempts the item-4 run from approval because it 'stops before any GitHub or ClickUp write', which is the behaviour under test; plan:254 runs `/sc:issue --claim https://github.com/octocat/Hello-World/issues/1` live; the URL-vs-origin comparison has no deterministic test (Task 1 tests parsing only), so plan:259 is hoped for, not guaranteed. An escape needs a Wave 0 fault plus a missed Wave 2 inference and lands reversibly on the user's own fork (origin #1 is a merged pull request), so it is minor under the binding rule.
- **Evidence:** plan:26, plan:254, plan:259, plan:32-38, plan:111, plan:116, source.md:142-143, source.md:151, source.md:155, source.md:159, source.md:162, source.md:336, source.md:361, source.md:470, .work/evidence-sheet.md E4 and E6, source.md:66, source.md:144, source.md:148, source.md:178, plan:32, plan:258
- **Recommendation:** (1) Item 4 uses a foreign URL whose repo and issue number cannot exist on origin and that has no digits outside the `/issues/<N>` segment, e.g. `https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999` (AC 4 needs only 'any repo other than origin'); the debate's example `.../issue302-no-such-repo/...` is NOT used, because its `302` is the real origin issue (INV-001) (that this repo does not exist is UNVERIFIED; no gh was run). (2) Add a pure URL-vs-origin check (or `--check-url` mode) to `origin_repo.py` that prints `E-FOREIGN-REPO` with an exit code distinct from `E-NO-ORIGIN`, pinned in Task 1 by tests for a same-repo URL, a foreign owner, the same owner with a different repo, a repo-name prefix (`IronClaude` vs `IronClaudeX`), a `/pull/<N>` URL (on origin: rejected, not parsed as an issue number, with a stated code), fragment and trailing `/`, and digits in the owner or repo name never becoming N (INV-001, INV-002); require in Task 6 (text and AC) that Wave 0 calls it; record it as a disclosed addition justified by source.md:361. (3) Rewrite plan:26's carve-out by target ('a run whose URL names a repository and issue that do not exist may run without asking'). (4) Split Task 17's item-4 row: clause 1 (E-FOREIGN-REPO) from the real run; clause 2 ('no `gh` call is made without `--repo <origin repo>`') points at the Task 7 fork-safety test and the F-10 `repos/<R>/` assertion and notes that `gh auth status` and `gh api` carry no `--repo` flag (INV-003). (5) Fallback: if (1) and (2) are not applied, item 4 stays pending (INV-005: the executor cannot ask for approval, refs/qa.md:288, SKILL.md:4; the debate's 'else approval' is replaced).
- **Debate ruling:** C-001 minor, unanimous after Round 2 (V3 conceded from blocking, round2-v3.md:3); winner V1, 95%. A-005 minor, unanimous (new). The minor grade holds only with a URL that has no stray digits (INV-001, INV-012); fallback amended by INV-005.

### Finding F-02 (minor, ambiguous-ac)

- **Claim:** Task 15 offers two exits for a stale session: plan:233 says 'stop here and ask the user to start a new session ... it resumes at this task' while plan:236 accepts a pending row; resume does work (a stop before review leaves only a start line, and Row S re-runs the task), so the defect is the choice of exit, not impossibility.
- **Evidence:** plan:233, plan:236, src/superclaude/skills/sc-implement-protocol/SKILL.md:108-115, src/superclaude/skills/sc-implement-protocol/refs/ledger.md:161, src/superclaude/skills/sc-implement-protocol/SKILL.md:4, src/superclaude/skills/sc-implement-protocol/SKILL.md:97, src/superclaude/skills/sc-implement-protocol/refs/qa.md:288
- **Recommendation:** State one exit, and make it pending: the executor may not stop to ask the user (src/superclaude/skills/sc-implement-protocol/refs/qa.md:288; its allowed-tools at SKILL.md:4 have no AskUserQuestion), and the session that runs Tasks 1-14 in source order started before Task 13, so the rule is that on the first pass Task 15 writes a pending row with the reason. This pending outcome is the rule to follow, not a statement about Claude Code (whether a skill hot-loads mid-session is UNVERIFIED). End Task 17's artifact with a short post-restart runbook in source order (export `CLICKUP_API_TOKEN`, `CLICKUP_WORKSPACE_ID` and `CLICKUP_LIST_IDS` (the test list, F-11) and have the test issue URL and task ID ready, start a new session, run Task 15's spawns, Task 16, item 4) so the scheduled checks are not dropped (INV-005). The runbook results are recorded in a new note next to the archived package under `.dev/tasks/done/`, because the package is archived after Task 17 (src/superclaude/skills/sc-implement-protocol/refs/managed-workspace.md:47-54). plan:233's 'delete it afterwards only with the user's approval' moves into the runbook. Remove 'it resumes at this task'. Keep 'after Task 13' (it is the agent-load condition, not the dependency).
- **Debate ruling:** C-002 and X-002 minor, unanimous; V3 withdrew 'resume cannot work' (round2-v3.md:24-25). Winner V1, 95%. The debate's 'stop and ask the user to restart' exit is replaced by pending per INV-005.

### Finding F-03 (minor, cross-task-contradiction)

- **Claim:** Task 6's mandated error-table rows trip Task 7's fork-safety scan: Task 6 requires SKILL.md to carry the section 14 error table and orchestrator write list, which name gh issue edit/comment/create without --repo; Task 7's fork-safety test requires every line that runs gh issue|pr|label to carry --repo.
- **Evidence:** plan:111, plan:131, plan:136, source.md:336, source.md:340, plan:56, plan:58, source.md:319, source.md:320
- **Recommendation:** Define the scan once and use it in both Task 3's test (plan:58) and Task 7's test (plan:131): every code span or fenced line that starts with `gh issue|pr|label` carries `--repo`, prohibitions included. Tasks 3, 5 and 6 then write every such mention with `--repo <R>`: the section-14 table cells (source.md:336, :340), the orchestrator write list (source.md:320) and the workers' 'never run ...' prohibition (plan:56). They write the placeholder rule of source.md:319 without the literal token (for example 'never a brace placeholder'), so plan:131's ban holds (INV-004). plan:136's negative case writes its `gh issue view` line as a code span or fenced line.
- **Debate ruling:** C-003 minor; V1 handed the better instance to V3 (round2-v1.md:26); winner V3, 95%.

### Finding F-04 (minor, unexecutable)

- **Claim:** Task 16 live comparison has no method or safe presence check: Task 16 key-path comparison names no method; the script prints only status JSON; the secrets rule does not ban curl -v/-i/--trace; first run 'assigned' cannot hold if the test task already lists the user.
- **Evidence:** plan:23, plan:243, plan:246
- **Recommendation:** Name one key-paths-only method (or accept the two status results as the shape check); ban `curl -v/-i/--trace` and header-printing options; check presence with `test -n "${CLICKUP_API_TOKEN:-}"`; accept `already_assigned` on the first run with a note.
- **Debate ruling:** C-004 minor, unanimous; winner V1, 90%.

### Finding F-05 (minor, test-isolation)

- **Claim:** ClickUp environment hygiene: tests clear only the token and workspace variables; an exported CLICKUP_MAX_PAGES or CLICKUP_LIST_IDS still reaches tests that pin page cap, first page and URLs. The secrets constraint forbids env on the token yet Task 2 uses env -u.
- **Evidence:** plan:23, plan:43, plan:45, plan:50
- **Recommendation:** Every test clears all four `CLICKUP_*` variables; plan:23 says 'no command that prints it; `env -u` to unset it is allowed'.
- **Debate ruling:** C-005 minor, unanimous; V3 handed it to V1 (round2-v3.md:106); winner V1, 90%.

### Finding F-06 (minor, acceptance-posture)

- **Claim:** 'Approval at that moment' has no trigger: Section 20 ACs 1, 2, 3, 6, 8 may end pending, so core end-to-end behaviour may ship unverified.
- **Evidence:** plan:15, plan:26, plan:254, src/superclaude/skills/sc-implement-protocol/refs/qa.md:274, src/superclaude/skills/sc-implement-protocol/refs/qa.md:288, src/superclaude/skills/sc-implement-protocol/SKILL.md:4
- **Recommendation:** The executor cannot prompt (refs/qa.md:288; SKILL.md:4), so the debate's 'add one explicit ask' is not available inside `/sc:implement` (INV-005). Instead: items 1, 2, 3, 5 (first half), 6 and 8 are recorded pending, and Task 17's artifact ends with the explicit request to the user, in the runbook of F-02, to pre-approve one scratch test issue so those items can be run by hand; plan:26's and plan:254's 'approval at that moment' clauses are reworded to 'only in a later, user-started session with the user's explicit approval'.
- **Debate ruling:** C-006 minor; winner V2, 90%; mechanism amended by INV-005.

### Finding F-07 (minor, dependency-metadata)

- **Claim:** Task 17 depends on Task 14 only but cites Task 15 and Task 16 evidence.
- **Evidence:** plan:252, plan:254
- **Recommendation:** Depends on: Task 14, Task 15, Task 16.
- **Debate ruling:** C-007 minor; winner V3, 90%. Metadata only for this executor (src/superclaude/skills/sc-implement-protocol/SKILL.md:79, :97).

### Finding F-08 (minor, dependency)

- **Claim:** AC 5's first half is unplaced: 'with CLICKUP_API_TOKEN unset the claim completes and the comment says ClickUp was skipped' (source.md:471) is never marked run or pending; plan:254 assigns only item 5's ClickUp half.
- **Evidence:** source.md:471, plan:50, plan:254
- **Recommendation:** Name it in the Task 17 record as pending (it needs a live claim); do not mark it run on Task 2's script-only `no_token` output.
- **Debate ruling:** A-002: minor, unanimous (new). No card raised it; named by reviewer-2-calibration (missed_by_card).

### Finding F-09 (minor, validation-rule)

- **Claim:** AC 8's `/model` first line is unasserted: AC 8's offline half (next-steps.md starts with the `/model` tier line, source.md:474) is not pinned by any test or AC; plan:77 defines the template but nothing asserts its first line.
- **Evidence:** source.md:474, plan:77, plan:81-85, plan:123-132
- **Recommendation:** Add a Task 4 AC (or Task 7 test) that `templates/next-steps.md` starts with the `/model` tier line; in Task 17, describe this static check as covering the template and default rows only and keep item 8 pending until a live claim, because `/sc:recommend` output can carry other flags (source.md:438; INV-011).
- **Debate ruling:** A-003: minor, unanimous (new). No card raised it; named by reviewer-2-calibration (missed_by_card).

### Finding F-10 (minor, validation-rule)

- **Claim:** No check that `gh api` paths spell `repos/<R>/`: Task 7's fork-safety scan (plan:131) checks `--repo` on `gh issue|pr|label` lines and bans the brace placeholder, but nothing checks section 13's rule that every `gh api` path spells `repos/<R>/...` (source.md:319).
- **Evidence:** source.md:319, plan:131, source.md:148, plan:92
- **Recommendation:** Extend Task 7's fork-safety test: every `gh api` path in the skill and agents other than `user` (the login lookup of source.md:148) starts with `repos/<R>/`; none uses the brace placeholder.
- **Debate ruling:** A-004: minor, unanimous (new). No card raised it; named by reviewer-2-calibration (missed_by_card).

### Finding F-11 (minor, guard)

- **Claim:** Task 16's PUT target is chosen by a workspace-wide match, not the named task, and the PUT happens inside the first run, so comparing the reported `task_id` afterwards cannot prevent a wrong assignment (INV-007).
- **Evidence:** plan:243, plan:246, source.md:298, source.md:304-309
- **Recommendation:** Task 16 runs only when the user has, before the session, exported `CLICKUP_LIST_IDS` set to the test task's list (narrowing the search before the PUT; INV-007) and supplied the test issue URL and task ID up front (the executor cannot ask mid-run, INV-005); otherwise it is pending. Remove plan:243's 'Ask the user only for the test issue URL and task ID'; the user supplies them before the session in `./artifacts/t16-input.md` (or the `/sc:implement` invocation text). After the first run compare the reported `task_id` with the named one; on a mismatch make no second run, record the wrong `task_id`, and tell the user to remove the assignment.
- **Debate ruling:** A-006: minor; winner V2, 90%; amended by INV-005 and INV-007. No card raised it; named by reviewer-1-calibration and reviewer-2-calibration (missed_by_card).

### Finding F-12 (minor, state)

- **Claim:** Task 17 item 4 needs a post-Task-13 session with no check: plan:254 runs item 4 in a session that has the skill loaded (after Task 13), the same fresh-session dependency as Task 15, with no stop-and-restart instruction.
- **Evidence:** plan:233, plan:254, plan:258
- **Recommendation:** State the same session precondition as Task 15; as the rule to follow (not a statement about Claude Code: whether a skill hot-loads mid-session is UNVERIFIED), on the first pass item 4 is pending and goes into the F-02 runbook (INV-005); a read-through or simulated run is not evidence, and the item-4 row quotes the real output when it is run.
- **Debate ruling:** A-007: minor, unanimous after V2 changed (round2-v2.md:72). No card raised it; named by reviewer-3-calibration (missed_by_card).

### Finding F-13 (minor, underspecified)

- **Claim:** Task 2 asks to 'define' invalid CLICKUP_MAX_PAGES behaviour without bounding it; the spec reserves exit 2 for bad arguments and exit 0 for everything else.
- **Evidence:** plan:43, source.md:310
- **Recommendation:** Fix the rule: fall back to 20 (or print an error status) and exit 0, since exit 2 is reserved for bad arguments.
- **Debate ruling:** V1 Round 1 kept it as low-value minor (round1-v1.md:77); carried as an explicit minor finding per INV-008.

### Finding F-14 (minor, executability-trap)

- **Claim:** Copying evidence-validator.md frontmatter would carry permissionMode: plan and block worker writes.
- **Evidence:** plan:56, src/superclaude/agents/evidence-validator.md:8
- **Recommendation:** Task 3 sets no `permissionMode: plan`, and its test asserts that.
- **Debate ruling:** Verified by V1 and V3 Round 1 (round1-v1.md:21, round1-v3.md:13). Carried as an explicit minor finding per INV-008, which ranks it first among F-13 to F-17 because a copied `permissionMode: plan` would leave every worker unable to write its file, so every claim or create ends `E-WORKER-NO-OUTPUT` (source.md:335) [INFERRED].

### Finding F-15 (minor, evidence-definition)

- **Claim:** The tier proxy rewrites the alias, so the transcript may show a tier member model, not the picker ID [INFERRED]; no transcript or log path named.
- **Evidence:** plan:233, plan:236, src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:17-21
- **Recommendation:** Accept the picker ID or a model from that tier's mapping as 'served', and name where the evidence is read.
- **Debate ruling:** Verified by V1 and V3 Round 1 (round1-v1.md:22, round1-v3.md:14); the transcript side stays [INFERRED]. Carried as an explicit minor finding per INV-008.

### Finding F-16 (minor, test-spec-ambiguity)

- **Claim:** Task 7 inventory 'every file in refs/, templates/, scripts/' fails on scripts/__pycache__.
- **Evidence:** plan:125, plan:132
- **Recommendation:** Limit the inventory to `refs/*.md`, `templates/*.md`, `scripts/*.py`.
- **Debate ruling:** Minor (round1-v3.md:18). Carried as an explicit minor finding per INV-008.

### Finding F-17 (minor, unpinned-literal)

- **Claim:** The D26 sentence has no fixed wording, so Tasks 6 and 8 can drift.
- **Evidence:** plan:111, plan:146
- **Recommendation:** State the exact sentence once in Task 6 and reference it from Task 8 and its test.
- **Debate ruling:** Minor (round1-v3.md:18). Carried as an explicit minor finding per INV-008.

### Finding F-18 (minor, state-variables)

- **Claim:** Wave 2 cannot see that a number is a pull request: Wave 2 decides from scout.md alone (source.md:154); the scout claim section the plan defines (plan:78) has no `url` or pull-request field although Wave 1 fetches `url` (source.md:148); an open pull request reports `OPEN`, so a user who types an open PR number reaches the assign and two comments (source.md:162, :178-179) without any fault. `E-NOT-AN-ISSUE` (source.md:159) is only checked for presence (plan:116). [INFERRED: an open PR's `state` reads `OPEN`; `gh issue edit` on a PR number is UNVERIFIED]
- **Evidence:** plan:78, plan:116, source.md:148, source.md:154, source.md:159, source.md:162
- **Recommendation:** Task 4 adds `url` and `is_pull_request` (true when `url` contains `/pull/`) to the scout claim section, with an AC; Task 5's claim.md makes the Wave 2 STOP read that field. Record it as a disclosed addition (the same kind as the 'whether that list was truncated' field at plan:78). Fix before any live claim.
- **Debate ruling:** INV-006 (MEDIUM, UNADDRESSED in the debate): no card raised it; named by the Round 2.5 invariant probe. Minor: no deliverable is missing and no plan statement is false; plan:92 already requires the pull-request STOP.


## Authorized expansions, notes and rejected points

- Authorized expansions (no action): `--limit 200` on the merged-PR query (plan:92, plan:105) and the source-only flag check of Task 7 (plan:129), both directed by check round 1 and disclosed in the plan.
- Notes: interim red tests between Tasks 1/8 and Task 9 are `unrelated-red` and change no verdict (src/superclaude/skills/sc-implement-protocol/SKILL.md:152-154); Task 12's heading lacks backticks (plan:197 vs docs/user-guide/commands.md:236).
- Rejected: S-001, S-002 (format only), A-001 (source.md:391 defines the static test as phrase presence), A-008 (pytest is a main dependency, pyproject.toml:34-43), Q-1 (duplicates plan:25), S-11 (withdrawn), U-019 (superseded by F-01 and F-12).

## Recommendations

### Recommendation R-001: Fix the Task 17 item-4 run before it is executed

- **File:** .dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md (Constraints plan:26, Task 1, Task 6, Task 17)
- **Change:** use a foreign URL with no digits outside `/issues/<N>` (for example `https://github.com/IronbellyOrg/no-such-repo-sc-issue-probe/issues/999999999`), add a tested URL-vs-origin check to `origin_repo.py` that Wave 0 calls, rewrite plan:26's carve-out by target, and split the item-4 row (F-01, F-12).
- **Verifier:** `grep -n 'octocat\|issue302-no-such' <plan>` prints nothing (the Task 14 worktree name `issue302-master-check` is expected to remain); Task 1's AC lists the URL-check tests; Task 6's AC requires the Wave 0 call.
- **Linked finding(s):** F-01, F-12
- **Priority:** P1

### Recommendation R-002: Make pending the single exit for the live checks and add a post-restart runbook

- **File:** same plan file, Tasks 15, 16 and 17
- **Change:** remove the mid-run asks (plan:233, plan:243, plan:254) that `/sc:implement` cannot make (src/superclaude/skills/sc-implement-protocol/refs/qa.md:288), record the live checks as pending on the first pass, and end Task 17's artifact with the runbook and the pre-approval request (F-02, F-06, F-11).
- **Verifier:** `grep -n 'Ask the user\|ask the user\|at that moment' <plan>` prints nothing; Task 17's ACs require the runbook.
- **Linked finding(s):** F-02, F-06, F-11
- **Priority:** P1

### Recommendation R-003: Block the `permissionMode: plan` copy and fold in the other minors

- **File:** same plan file (Tasks 2, 3, 4, 5, 6, 7, 16)
- **Change:** Task 3's test asserts no `permissionMode` key (F-14), then apply F-03 to F-05, F-07 to F-10, F-13 and F-15 to F-18 as written in `adversarial/merged-verdict.yaml`.
- **Verifier:** each finding's cited plan line carries the change.
- **Linked finding(s):** F-03 to F-05, F-07 to F-10, F-13 to F-18
- **Priority:** P2

## Grounding Gaps

Items the Wave 5 evidence validator dropped (`artifacts/evidence-validator-findings.md`). Neither changes a finding's severity or the verdict.

### Gap G-001: F-02 cited ledger Row P as support

- **Dropped citation:** `src/superclaude/skills/sc-implement-protocol/refs/ledger.md:155` in F-02's evidence.
- **Why:** line 155 is Row P (a `blocked` verdict exists), which the debate cites only as the row that does NOT apply to a stop before review; the supporting row is Row S at line 161, which stays cited. Removed from the F-02 evidence list above; it remains in `adversarial/merged-verdict.yaml`, where readers should treat it as "Row P does not apply".
- **Next evidence needed:** none; owner: reviewer; decision needed by user: no.

### Gap G-002: R-001's verifier could never pass

- **Dropped claim:** R-001's original verifier `grep -n 'octocat\|issue302' <plan>` prints nothing.
- **Why:** the plan's Task 14 worktree name `issue302-master-check` (plan:220, plan:226) would always match. The verifier above now greps `octocat\|issue302-no-such` and states the expected remaining hits.
- **Next evidence needed:** none; owner: reviewer; decision needed by user: no.

Other validator notes (kept, wording only): F-03 cites plan:56 as the line that requires the workers' prohibition text, although the "never run ..." wording is the recommendation's, not plan:56's; F-14's ruling in the merged verdict says INV-008 ranks S-5 first, while the probe only calls it "the costly one if it is dropped"; F-14's claim "block worker writes" is itself [INFERRED].

## Inferred-claim audit

- `citations_inferred: 8` (7 tag occurrences covering 8 claims: the UNVERIFIED notes in F-01, F-02 and F-12, the [INFERRED] tags in F-14 and F-15 (twice), and the two sub-claims tagged in F-18)
- Inferred-fraction: `8 / 236` = 0.03
- Evidence validator: full re-read of all 236 line-bearing citations by two parallel validators (169 outside the Pass 2 table, 67 in it), plus 10 path-only references confirmed to exist; 2 items dropped (G-001, G-002).
