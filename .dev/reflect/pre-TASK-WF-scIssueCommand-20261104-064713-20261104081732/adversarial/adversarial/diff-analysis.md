# Diff Analysis: Reviewer-Card Comparison (sc:reflect Tier-2, pre-execution, round 2)

## Metadata
- Generated: 2026-11-04T08:46:00Z
- Variants compared: 3
  - V1 = reviewer-1 card (analyzer, sonnet), verdict FAIL, 1 blocking + 5 minor (A-1..A-6)
  - V2 = reviewer-2 card (qa, haiku -> glm-5.3), verdict PASS, 4 minor (Q-1..Q-4)
  - V3 = reviewer-3 card (refactorer, opus), verdict FAIL, 2 blocking + 10 minor (S-1..S-12)
- Input-type warning: all three inputs are YAML, not markdown. "Sections" are top-level YAML keys; "claims" are the finding claims, the verdict and the self-audit.
- Target under review: plan `.dev/tasks/to-do/TASK-WF-scIssueCommand-20261104-064713/TASK-WF-scIssueCommand-20261104-064713.md` (version 2, revised after round 1) against `source.md` in the same folder.
- Total differences found: 38
- Categories: structural (2), content (7), contradictions (2), unique (19), shared assumptions (8)
- Convergence denominator (S + C + X + A): 19

## Structural Differences

| # | Area | V1 | V2 | V3 | Severity |
|---|------|----|----|----|----------|
| S-001 | Card schema and keys | 7 top-level keys plus `round1_fix_check` (only V1 reports on the round-1 fixes); block-style findings with `recommendation` | 8 keys (adds `resolved_model`, `attempt`); every finding is an inline flow map | 7 keys; block style for the two blocking findings, flow maps for the ten minor ones | Low |
| S-002 | Finding granularity and verdict basis | 6 findings; FAIL rests on one safety finding (A-1) | 4 findings, all minor, all "keep / acceptable"; PASS | 12 findings; FAIL rests on S-1 and S-2 (self_audit says so) | Medium |

## Content Differences

| # | Topic | V1 Approach | V2 Approach | V3 Approach | Severity |
|---|-------|-------------|-------------|-------------|----------|
| C-001 | Task 17 live item-4 run (`/sc:issue --claim https://github.com/octocat/Hello-World/issues/1`, "may run without asking", plan:26, plan:254) | A-1 blocking (safety-risk): only guard is the code under test; escape posts on a third-party repo; fix: non-existent foreign repo URL, read SKILL.md first, ask the user | Silent on item 4; Q-4 accepts pending ACs and asks for one pre-approved scratch issue for items 1, 2, 3, 6, 8 | Silent | High |
| C-002 | Task 15 "stop, start a new session, re-run, it resumes at this task" (plan:233, plan:236) | A-2 minor (ambiguous-ac): two incompatible exits (stop vs pending); prerequisite should say after Task 14 | Silent | S-2 blocking (executor-semantics): /sc:implement has no pause state; resume cannot work, or the executor writes pending and the spawn never happens | High |
| C-003 | Fork-safety scan (Task 7, plan:131) vs SKILL.md prose required by Task 6 (plan:111; section 14 table, section 13 write list) | A-5 minor (test-design): line-level scan false-positives on prose; scope the scan to command lines and state the api rule as `repos/<R>/...` | Silent | S-1 blocking (cross-task-contradiction): Task 6 content contradicts Task 7's test; require `--repo <R>` on every mention and define "line that runs gh" | High |
| C-004 | Task 16 ClickUp smoke: key-path comparison and safe variable checks (plan:243, plan:246) | A-3 minor: no method; ban `curl -v/-i/--trace`; accept `already_assigned` on first run | Silent (self_audit: "ClickUp posture satisfies section 12") | S-6 minor: no method; accept the two status results as the shape check; `test -n "${CLICKUP_API_TOKEN:-}"` | Low |
| C-005 | ClickUp environment hygiene in tests and checks (plan:23, plan:45, plan:50) | A-4 minor: tests clear only two of four CLICKUP_* variables | Silent | S-4 minor: Constraints ban `env` on the token, Task 2 uses `env -u` | Low |
| C-006 | Pending section-20 ACs posture (plan:15, plan:254) | Accepts pending for 1, 2, 3, 6, 8; challenges only the item-4 carve-out | Q-4 minor: core end-to-end behaviour may ship unverified; ask the user to pre-approve one scratch issue | Accepts; S-3 asks Task 17 to depend on Tasks 15 and 16 | Medium |
| C-007 | Dependency metadata of Tasks 15 and 17 (plan:231, plan:233, plan:252, plan:254) | A-2 second half: prerequisite text "after Task 13" though the task depends on Task 14 | Silent | S-3 minor: Task 17 depends on Task 14 only but cites Task 15 and 16 evidence | Low |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | V3 Position | Impact |
|---|-------------------|-------------|-------------|-------------|--------|
| X-001 | Overall verdict on plan version 2 | FAIL ("blocking A-1 introduced by the revision") | PASS ("ACs observable; ClickUp posture satisfies section 12") | FAIL ("FAIL rests on S-1 and S-2") | High |
| X-002 | Can /sc:implement stop at Task 15 and resume there after a new session? | Yes, implied: A-2 recommends "Executor stops without writing the artifact and asks the user to restart" | No position | No: "/sc:implement has no pause-for-new-session state ... 'it resumes at this task' cannot work" | High |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|-------------|-----------------|
| U-001 | V1 | `round1_fix_check: {F-01: fixed, F-02: fixed}`: only card that checks the round-1 blocking fixes | Medium |
| U-002 | V1 | A-4: `CLICKUP_MAX_PAGES` / `CLICKUP_LIST_IDS` exported in the shell still reach the page-cap and URL tests | Medium |
| U-003 | V1 | A-6: invalid `CLICKUP_MAX_PAGES` behaviour unbounded; fix it as fallback-to-20 or an error status with exit 0 | Low |
| U-004 | V1 | A-5 recommendation: scope the scan to fenced/inline command lines; never write the `{owner}/{repo}` placeholder even in prose | Medium |
| U-005 | V2 | Q-1: section 17 item 5 (PR via /sc:pr-submit) deferred; name the exact command as the next action | Low |
| U-006 | V2 | Q-2: `--limit 200` added to the spec's merged-PR query is a disclosed addition | Low |
| U-007 | V2 | Q-3: Task 7's source-only flag check narrows section 16's "installed-or-source" | Low |
| U-008 | V2 | Q-4 recommendation: ask the user to pre-approve one scratch test issue so ACs 1, 2, 3, 6, 8 can run live | Medium |
| U-009 | V3 | S-4: Constraints forbid `env` on the token while Task 2's AC uses `env -u` | Low |
| U-010 | V3 | S-5: copying `evidence-validator.md` frontmatter carries `permissionMode: plan`, blocking worker writes | Medium |
| U-011 | V3 | S-6: safe presence check `test -n "${CLICKUP_API_TOKEN:-}"` | Low |
| U-012 | V3 | S-7: the tier proxy rewrites the alias, so served-model evidence may show a tier member model, not the picker ID | Medium |
| U-013 | V3 | S-8: "every file in scripts/" inventory can trip on `scripts/__pycache__` | Low |
| U-014 | V3 | S-9: interim red tests between Task 6/8 and Task 9 are unexplained | Low |
| U-015 | V3 | S-10: the D26 sentence has no fixed wording shared by Tasks 6 and 8 | Low |
| U-016 | V3 | S-11: no per-task lint before Task 14 | Low |
| U-017 | V3 | S-12: Task 12 heading lacks backticks around the command | Low |
| U-018 | V3 | S-3: Task 17 `Depends on` omits Tasks 15 and 16 (also part of C-007) | Low |
| U-019 | V1 | A-1 recommendation: read the implemented SKILL.md and confirm E-FOREIGN-REPO precedes the first gh call before the live run | Medium |

## Shared Assumptions

Sources: the three blind calibrations (`reviewer-N-calibration.yaml`, `missed_by_card`) name items no card raised; each is an agreement point whose precondition no variant states. All eight are UNSTATED and promoted to `[SHARED-ASSUMPTION]` diff points.

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | No card questions Task 7's spawn-rule test (plan:126) | A phrase-presence test satisfies section 20 AC 7 "the skill never passes `model` on an Agent call (static test)" (source.md:473). Round 1 ruled it adequate because source.md:391 defines the static test as phrase presence (round-1 rejected_findings `A-003-ac7-phrase-test`) | UNSTATED | Yes |
| A-002 | No card checks AC 5's first half | Task 17's row plan for item 5 covers "with CLICKUP_API_TOKEN unset the claim completes and the comment says ClickUp was skipped" (source.md:471); plan:254 assigns only item 5's ClickUp half (Task 2, Task 16) and lists items 1, 2, 3, 6, 8 as pending | UNSTATED | Yes |
| A-003 | No card checks AC 8 | AC 8's offline half (next-steps.md starts with the `/model` tier line, source.md:474) is pinned; plan:77 defines the template but no test or AC asserts its first line | UNSTATED | Yes |
| A-004 | All cards accept Task 7's fork-safety scan scope | Checking `--repo` on `gh issue|pr|label` lines plus banning `{owner}/{repo}` (plan:131) covers section 13's "every `gh api` path spells `repos/<R>/...`" (source.md:319) | UNSTATED | Yes |
| A-005 | V1 A-1 relies on "the code under test"; no card asks for a test | The Wave 0 URL-vs-origin comparison that yields E-FOREIGN-REPO (source.md:143) needs no deterministic test; Task 1 tests only origin parsing (plan:32-38) | UNSTATED | Yes |
| A-006 | All cards treat Task 16 as approved by scheduling | Task 16's live ClickUp PUT (plan:243) needs no explicit user-approval rule; plan:26's approval rule names GitHub writes only | UNSTATED | Yes |
| A-007 | No card applies the Task 15 fresh-session logic to Task 17 | Task 17's item-4 run (plan:254, "a session that has the skill loaded (after Task 13)") needs no restart instruction like Task 15's | UNSTATED | Yes |
| A-008 | No card checks Task 14's master comparison | A fresh Orca worktree on origin/master (plan:220) can run the failing test with no environment setup | UNSTATED | Yes |

## Summary
- Total structural differences: 2
- Total content differences: 7
- Total contradictions: 2
- Total unique contributions: 19
- Total shared assumptions surfaced: 8 (UNSTATED: 8, STATED: 0, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, X-001, X-002
- Similarity check: 38 differences across 22 findings; variants are not substantially identical; debate proceeds.

## Taxonomy tags (AD-5)

| Point | Level | Signal |
|-------|-------|--------|
| S-001 | L1 | formatting / style choice |
| S-002 | L2 | organization of the verdict basis |
| C-001 | L3 | guard (Wave 0 E-FOREIGN-REPO guard) |
| C-002 | L3 | state / transition (executor pause and resume) |
| C-003 | L3 | validation rule (fork-safety scan) |
| C-004 | L2 | interface (live response shape comparison) |
| C-005 | L3 | state (environment variables leaking into tests) |
| C-006 | L2 | organization (acceptance posture) |
| C-007 | L2 | dependency |
| X-001 | L2 | organization (verdict) |
| X-002 | L3 | state / transition |
| A-001 | L3 | validation rule |
| A-002 | L2 | dependency (AC-to-task mapping) |
| A-003 | L3 | validation rule |
| A-004 | L3 | validation rule |
| A-005 | L3 | guard |
| A-006 | L3 | guard (approval) |
| A-007 | L3 | state (session state) |
| A-008 | L2 | dependency |

Coverage: L1 = 1, L2 = 7, L3 = 11. All three levels covered.
