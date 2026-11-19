# Refactoring Plan: Merge into Base (Variant 2, opus:architect)

Folder: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/remediation/watcher-plan-v3/adversarial/`. Base: `variant-2-opus-architect.md` (V2). Other inputs: `variant-1-opus-security.md` (V1), `variant-3-sonnet-analyzer.md` (V3), `round2-rebuttals.md` (R2, verdicts V-1 to V-8 are its points 1 to 8), `invariant-probe.md` (probe, I-1 to I-17), `debate-transcript.md`, `base-selection.md`. Repo paths are relative to `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/`. `guard` = `src/superclaude/hooks/scripts/launch-level-guard.sh`; `plan` = `.dev/tasks/to-do/TASK-WF-requirements-20261119-012839/TASK-WF-requirements-20261119-012839.md`.

## Overview
- Base: Variant 2 (opus:architect), score 0.9087, selected by the debate tiebreaker (margin 0.0072 over V1, inside 5%).
- Incorporating strengths from: V1 (opus:security) and V3 (sonnet:analyzer).
- Planned changes: 8 Round 2 verdict rows (V-1 to V-8), 8 Round 1 settled rows (S-1 to S-8), 5 carry items (K-1 to K-5), 3 small V3 additions (T-1 to T-3). 24 rows in total.
- Risk level: Medium overall (the guard edits and the cycle.py reason order are the sensitive parts).
- Edit rule for the merge executor: every guard change lands in `src/superclaude/hooks/scripts/launch-level-guard.sh` and `plugins/superclaude/hooks/scripts/launch-level-guard.sh`; nothing under `.claude/` is edited or staged (repo rule); `.dev/tasks/` stays staged.

## Planned Changes

### A. Round 2 verdicts (one row per verdict)

| # | Decision | Source | Target in base | Rationale (round, point, confidence) | Integration | Risk |
|---|---|---|---|---|---|---|
| V-1 | Self-approval by the launch account: warn-first, owner decision recorded | V1 Q-1 Part B (softened) | New Q-1 Part B in base; base Residual risk 1 reworded | R2 point 1, 0.70, 3/3; diff D-04 L3 | `approval_of` (predicates.py:185) gets `excluded_ids` (default empty); one new closed-set config key (cycle.py:58-69 `_TOP_KEYS`) feeds it at both call sites (cycle.py:883, 998); `check-config` (cli.py:185-198, new warning line) and the Task 17 first-run report print `approver_is_launch_account` when the approvers file holds the launch account; Task 15 generator never writes the account id into a generated approvers file; plan:24, plan:209; open decision recorded in Task 24; predicate test for an excluded id. State in the plan that `~/.config/superclaude` is not in the guard's tamper list (guard:763-765), so Part B limits an honest-but-injected session, not a hostile one | Medium: new config key and warning output; no behaviour change until the owner opts in |
| V-2 | Reason order in `_revalidate`: approval reread, then time rule (`edited_after_approval`), then `project_check` and equality (`revalidation_failed`) | V1 Q-4 | Replace base Q-4 ordering sentence ("time check runs first") | R2 point 2, 0.65, 2/3; diff D-08 / C-1 L3; plan:71 (owner-derived) versus plan:108 | cycle.py:1007-1016: keep approval reread first; time rule after the items reread (cycle.py:1012-1014); equality last. plan:108 fixtures keep every field time before the approval so the equality check is reached; add the overlap case (Pipeline lowered with a late field time ends `edited_after_approval`); neither case makes a launch call | Low to Medium: audit counts of `revalidation_failed` drop |
| V-3 | Ship gate: single constant plus coupling test | V2 Q-2 Option A plus V1 Q-2 coupling test | Base Q-2 (keep Option A, drop Option B as default, add the test) | R2 point 3, 0.75, 3/3; diff D-05 L3 | `GOVERNED_LEVELS_ALLOWED = False` in `launch.py`; gate sits in `_examine` before `_launch` (cycle.py:833-834, 1028) so `would_launch` stays honest; one `level_gated` row in `audit.REASON_TABLE` as `("skip", 0)`; test in `tests/hooks/test_launch_level_observations.py` beside `_PENDING` (lines 79-84): when the constant is True none of `OB-H1 item 1`, `OB-H1 item 5`, `OB-H2`, `OB-H3` is in `_PENDING`; Task 17 report prints the gate state; Task 22 documents who flips it. The A2 per-level split stays an owner option | Low: about 6 lines plus one row and tests |
| V-4 | Updated time: field-value times only, unreadable voids, item time excluded | V2 Q-3 Option C plus V1 Q-3 (unreadable voids) plus V3 Q-3 (same-second test) | Base Q-3 (Option C default; Task 3a kept) | R2 point 4, 0.75, 3/3; diff D-07 L3; github.py:84-100 reads no time today | Task 3 introspection lists the single-select value fields and fails if `createdAt` or `updatedAt` is absent (docs extract confirmed `createdAt` only); rule voids on an unreadable time and on an equal time (one-second resolution, predicates.py:257); `ProjectItem` gets `status_changed_at` and `pipeline_changed_at` (predicates.py:113-118); both `_examine` and `_revalidate` call the rule (plan:65); plan:55, 58, 65, 67 edits as in base; Task 4 depends on Task 1, 3 and 3a | Medium: GitHub runtime behaviour unobserved (A-004) until Task 3a |
| V-5 | Add `*issue_pipeline*complete.run*` to the coordinator-only pattern, as best-effort | A1 proposal (no variant) | Base Q-1 item 4 pattern list | R2 point 5, 0.55, 1/3 strict; diff D-02 extra L3; WEAK ROW | Pattern becomes `*issue-pipeline*complete* \| *issue_pipeline.complete* \| *issue_pipeline/complete.py* \| *issue_pipeline*import*complete* \| *issue_pipeline*complete.run*`; one must-refuse test line for `p.complete.run()`; plan:152 states the pattern is best-effort, not a control (A-002), and the grant-row rule (WORKER-CONTRACT.md:300) remains the control | Low: one more glob alternative; known false positive is an odd `grep -e` order |
| V-6 | Blocked class covers issue, label and project writes | V2 Q-1 catch-all plus V1 Q-1 label/project scope | Base Q-1 items 1 and 2 | R2 point 6, 0.75, 2/3 merged scope; diff D-01 L3; plan:23 (owner decision) | After guard:652 add `'issue '*`, `'label '*`, `'project '*` as one class; allow `'project item-list' \| 'project field-list'` before the catch-all (R2 case run: they do not match `*' list'`); add the class to the `for LL_C in` list at guard:788; four-level case rows `W`, `WA`, `F`, `FS`; message names issue, label and project writes; plan marks this as the one place Q-1 goes beyond issue verbs | Medium: new refusals; reads stay allowed |
| V-7 | Task 6 takes all seven test files | V2 Q-7 plus V1 Q-7 tip | Base Q-7 (kept) | R2 point 7, 0.85, 3/3; diff D-11 L2; recount 45 lines in 7 files; launch.py:101 rejects an old prompt | Move the seven files from Task 7 (plan:114) into Task 6; Task 6 acceptance (plan:109) becomes `uv run pytest tests/issue_watch -q`; write the new `_PROMPT_RE` out in the test, do not import it from `launch.py` | Low: Task 6 grows |
| V-8 | Result marker is per run, keyed on the approval event id | V1 Q-6 idea (key changed) | Replace base Q-6 static marker `<!-- sc:issue:result -->` | R2 point 8, 0.65, 1/3 strict; diff D-10 L2; WEAK ROW; record.py:545-547, plan:141 | Marker `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->`; never contains `CLAIM_MARKER` (predicates.py:14); `complete` suppresses a post only for an exact marker by its own login; tests: another run id does not suppress, another login does not suppress, same run id and login does; plan:87, 141, 146 edits; design note states the login is shared by watcher, coordinator and launched agents | Medium: overrules 2 of 3 advocates; coordinator must pass the run id |

### B. Round 1 settled decisions

| # | Decision | Source | Target in base | Rationale | Integration | Risk |
|---|---|---|---|---|---|---|
| S-1 | Narrow coordinator-only pattern keeps pytest allowed | V2 Q-1 item 4 | Base (kept) | D-02 / C-5 L3, A1 and A3 conceded; R2 section 0 case run | Must-allow list adds `uv run pytest tests/issue_pipeline/test_complete.py` and `test_complete_cli.py` | Low |
| S-2 | Guard version stamp bumped to 2 | V2 Q-1 risk note | Base Q-1 (promote `[SCOPE+, recommended]` to required) | D-03 L3, 3/3; guard:10, orca_worktree.py:839 | Bump guard:10, the plugin mirror line 10, `GUARD_VERSION_LINE` (orca_worktree.py:839) and the pins at tests/hooks/test_launch_level_guard.py:251, tests/skills/test_issue_orca_worktree.py:1283 and :1914-1916 in Task 10; test that a guard stamped 1 is refused; release note: hosts run `superclaude install --force` before the next claim | Low |
| S-3 | Status moves only from the four allowed Statuses; V2 refusal words kept | V1 Q-5 compare-and-set plus V2 Q-5 | Base Q-5 | D-09 L3, 3/3 | Comment only with `status_moved_by_person` when the current Status is not Research, Spec, Plan or Debug; `complete.py` imports the allowed-Status constant Task 1 names (plan:34) instead of copying the four words; keep `^PVT_` check, `project_missing`, `project_ambiguous`, `status_option_missing`, `--project-id`; test: item at Done gets no mutation; plan notes the read-then-write window is not atomic | Medium: one more read per completion |
| S-4 | DF-14 assertion restated without weakening | V1 Q-8 count plus V2 Q-8 regex | Base Q-8 | D-12 L1, 3/3 | `$after: String` stays nullable; regex `\$(\w+): String!` yields exactly {owner, name}; `count("String!") == 2`; no literal repository; no `mutation`; Task 11 reads DF-14 first; reject `$owner: String = "IronbellyOrg"` | Low |
| S-5 | No config key as the gate switch | V1 Q-2 reasoning | Base Q-2 (V3 key not adopted) | C-2 / D-06 L3, 3/3; guard:763-765 | Covered by V-3; plan states why | Low |
| S-6 | Plan:23 wording on scope of the guard | V1 residual risks | Base plan:23 edit and residual risks | A-001, A-002, A-007 | "Refused at every level, Full Submit included, for `gh` text only; a script or other HTTP client is not seen; the complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision)"; Task 24 asks the owner to confirm once that the extra refusals are acceptable (A-007); plan:158 tests W, WA, F, FS | Low |
| S-7 | Governed sessions documented, unbound session test added | V2 Q-9 plus V1/V3 guard test | Base Q-9 | D-13 L1, convergent; guard:153-154, 391 | plan:23 text per probe I-8; Task 10 adds a guard test that an unrecorded session is allowed, labelled "documents, does not endorse" | Low |
| S-8 | Ordering and push sentence | V2 Q-10 Constraints line plus V1 replacement sentence | Base Q-10 | D-14 L1, convergent | Task 4 depends on Task 1 and 3a; Task 15 depends on Task 9; Constraints line for shared files; V1's replacement for WORKER-CONTRACT.md:245; `tests/skills/test_worker_contract.py` asserts the new sentence | Low |

### C. Items the probe says no variant stated (the merge must carry all five)

| # | Item | Where it goes | Risk |
|---|---|---|---|
| K-1 | New guard class goes into the `for LL_C in ...` list at guard:788, or it is never evaluated | Base Q-1 item 2, V-6 row; guard test that each new code prints a nonempty three-part message (probe I-7) | Medium if missed: silent allow |
| K-2 | `project item-list` and `project field-list` get allow rows ahead of the catch-all | V-6 row; guard test grid lists each over-match as an expected result (probe I-15) | Low |
| K-3 | `plan-hash` with a path containing "complete" is refused by the hyphen alternative `*issue-pipeline*complete*` | Anchor the hyphen alternative on the verb word, or record the over-match as accepted and tested; G2 must-allow adds `plan-hash` with a path containing "completed" (probe I-5) | Low |
| K-4 | Every guard change lands in `src/` and `plugins/superclaude/`; nothing under `.claude/`; `.dev/tasks/` stays staged | Overview edit rule; merge-log check | Low |
| K-5 | The config directory write path (`~/.config/superclaude`) is an owner decision; without it the V-1 key and any config switch are as writable as the approvers file | Open owner decisions, OD-4 | Medium |

### D. Small additions from V3

| # | Addition | Source | Target | Integration | Risk |
|---|---|---|---|---|---|
| T-1 | Same-second approval and item-time test case | V3 Q-3 | Task 4 tests | Included in V-4; equal time voids, an item an hour older passes | Low |
| T-2 | Task 3a outcome decision table | V3 Q-3 | Task 3a text | Field moves the time and a label does not: rule as written; field does not move it: fail-open, stop and return the fallback; label moves it: total outage, same stop | Low |
| T-3 | Rollback line per finding, ranked impact table, "Unverified" list | V3 structure | Task 22 docs and the owner summary | Optional text; do not restructure the base | Low |

## Invariants

The probe status is for the merged text after Round 1 concessions and Round 2 verdicts. "Text to address" is what the merged plan must say; the rows are condensed from `invariant-probe.md`.

| ID | Invariant | Status | Text to address in the merged plan |
|---|---|---|---|
| I-1 | Only the coordinator writes to GitHub, at every level including Full Submit (High) | PARTIAL | plan:23 per S-6 (gh text only; token separation is a Coder row). plan:158 tests W, WA, F, FS for `issue edit --add-label`, `issue comment`, `issue close`, `label create`, `project item-edit`, `true && gh issue comment`, and `-R o/r` forms; `gh pr comment` still passes at FS. Limit A-002 stays open by nature |
| I-2 | An approval is void when the Project item changed after it (High) | PARTIAL | Task 3 introspection fails if `createdAt` or `updatedAt` is absent; Task 3a records four values in `./artifacts/`; Task 4 depends on 1, 3, 3a; void on unreadable and on equal time; both `_examine` and `_revalidate` call it; a fail-open result returns R31 to the owner for a level-specific label; Task 5 says the coordinator's own move to In review bumps the Status value time and voids the approval by design |
| I-3 | No launch while the ship gate is closed (High) | ADDRESSED | Constant False in code; `_examine` raises `_Skip("level_gated")` for any Pipeline other than None; one REASON_TABLE row; coupling test; Task 17 report prints the gate state; Task 22 documents who flips it (a reviewed commit that also un-skips the observation) |
| I-4 | Status moves only from the four allowed Statuses (High) | ADDRESSED | `complete.py` imports the allowed-Status constant from Task 1; test sets the item to Done and asserts no mutation; plan notes the residual read-then-write window |
| I-5 | `pytest tests/issue_pipeline/test_complete.py` is not refused in a launched or bound session (High) | ADDRESSED | G2 must-allow adds `uv run pytest tests/issue_pipeline/test_complete.py`, `test_complete_cli.py`, and `plan-hash` with a path containing "completed"; anchor the hyphen alternative on the verb word or record the over-match as accepted and tested (K-3) |
| I-6 | The version stamp bump keeps old hosts refused (High) | ADDRESSED | S-2: bump guard:10, the plugin mirror, `GUARD_VERSION_LINE` and the three test pins together in Task 10; edit `src/` and `plugins/superclaude/`; test a guard stamped 1 is refused; release note on `superclaude install --force` |
| I-7 | Every fail-closed path gives an owner-readable message (Medium) | PARTIAL | Add the class to the precedence loop and four-level case rows (K-1); one `ll_say` block (Blocked: a GitHub issue, label or project write; Why: only the coordinator writes, a launched session reports through `.dev/issues/<N>/result.md`; You can: write the result file and let the coordinator post); reword LL-SUBMIT to "pull request" only; guard test asserts each new code prints a nonempty three-part message; Task 22 lists each new reason word (`level_gated`, `approver_is_launch_account`, the Q-5 refusal words) with one plain sentence |
| I-8 | The claim session's ungoverned boundary is documented (Medium) | PARTIAL | plan:23: "Governed: a session with a record in the launch-level store (agents launched at Worktree, Full, Full Submit; bound workers). Not governed: the watcher-launched `--pipeline none` claim session and the coordinator; the claim session's two marked comments are allowed by design and it reads untrusted issue text under the launch login." Task 10 adds the unbound-session-allowed test (S-7). Gap: "claim session has no record" is an inference from refs/claim.md:118 |
| I-9 | No self-approval under the launch login (High) | PARTIAL | plan:24: "approval by the launch account is accepted unless the owner sets the exclusion key; `check-config` and the Task 17 first-run report print `approver_is_launch_account`"; open decision in Task 24 with both options (OD-3); generator never writes the account id; predicate test for an excluded id (V-1). Limit: warn-first leaves the hole open until the owner opts in |
| I-10 | The config and approvers directory is not writable by a launched agent (Medium-High) | UNADDRESSED | Owner decision OD-4: add `*.config/superclaude*` to the tamper tokens at guard:764 and the plugin mirror with a must-refuse test (Edit and shell redirect on `issue-watch.json`), or record in plan:23 that the directory is trusted and why |
| I-11 | The coordinator-only `complete` verb is refused for bound workers and launched sessions (High) | PARTIAL | G2 tests list must-refuse spellings: the verb, `uv run` verb, `python -m ...issue_pipeline.complete`, `from ... import complete`, `from ....complete import run`, `p.complete.run()`; `stage-status` left unclassified and the plan says so; plan:152 states best-effort (V-5) and the grant-row rule (WORKER-CONTRACT.md:300) remains the control |
| I-12 | The result comment is posted once per run, not once per issue (Medium) | ADDRESSED | V-8: marker with `run=<approval_event_id>`; tests for another run id, another login, same run id and login |
| I-13 | The result marker is never read as a claim marker (Medium) | ADDRESSED | Test that the result marker does not contain `CLAIM_MARKER` and that `marker_comments` evidence ignores a result comment |
| I-14 | The coordinator's own comment never voids an approval; its Status move voids it by design (Medium) | ADDRESSED | Task 5 and Task 8 state both facts; one test shows the coordinator's comment leaves `unchanged_since` clean |
| I-15 | Fail-closed extra refusals do not block the work launched agents do (Medium) | PARTIAL | Allow rows for `project item-list` and `project field-list` (K-2); owner confirms once in chat that these refusals are acceptable (Task 24, A-007); the guard test grid lists each over-match as an expected result |
| I-16 | The test tree stays green between tasks (Medium) | ADDRESSED | V-7: Task 6 acceptance `uv run pytest tests/issue_watch -q`; Task 7's list drops those files; `_PROMPT_RE` written in the test |
| I-17 | The DF-14 cursor stays nullable and the query is not weakened (Low) | ADDRESSED | S-4: `$after: String` nullable, only `$owner` and `$name` are `String!` (regex), no literal repository, no `mutation`; plan:166 says Task 11 reads DF-14 first |

Probe totals: ADDRESSED 9 (I-3, I-4, I-5, I-6, I-12, I-13, I-14, I-16, I-17), PARTIAL 7 (I-1, I-2, I-7, I-8, I-9, I-11, I-15), UNADDRESSED 1 (I-10). The merge should lift I-7 to ADDRESSED with the message text above; I-1, I-2, I-8, I-9, I-11 and I-15 stay limited by declared text-only and unobserved-behaviour limits, and I-10 waits on the owner.

## Changes NOT Being Made (with rationale)

| Diff Point | Non-base approach | Rationale for keeping base or the verdict |
|---|---|---|
| D-05 | V1 module `ship_gate.py` with `REQUIRED`/`PASSED` frozensets and new Task 4b | R2 point 3: A1 calls `REQUIRED - PASSED` overkill for a boolean; the coupling test survives without the module |
| D-04 | V1 `excluded_ids` default-on hard refuse | R2 point 1: total outage for a one-login workspace on the first cycle; warn-first adopted |
| D-07 | V1 item-level `updatedAt` in the default rule | R2 point 4: a label apply may move the item time and void every approval |
| D-10 | V1 marker with the launch op id (`op=none` for unknown outcome) | R2 point 8: two unknown outcomes would suppress each other; approval event id used instead |
| D-10 | V2/V3 single static marker | R2 point 8: second run after a fresh approval finds the first marker and posts nothing (plan:141) |
| D-02 | V1/V3 `*issue_pipeline*complete*` | R2 section 0: refuses `pytest tests/issue_pipeline/test_complete.py` |
| D-01 | V1 enumerated verb list (`ISSUEWRITE`) and V3 narrow `ISSUEW` | Enumeration lets a new `gh issue` verb escape; V3 leaves close/reopen/lock to the command-position-only UNKNOWN row (R2 point 6) |
| D-05 / D-06 | V3 config key `launch_levels_gate` | guard:763-765: `~/.config/superclaude` is not tamper-protected; A3 conceded |
| D-08 | V3 collapse of every `_revalidate` failure to `revalidation_failed` | Changes owner-derived plan:71; the equality check is the backstop for a fail-open time rule (R2 point 2) |
| D-08 | V2 order with the time rule before the approval reread | A2 conceded V1's order is slightly better (A2 section 2, D-08) |
| D-09 | V2/V3 unconditional Status write | Overwrites a person's later move; compare-and-set adopted |
| D-12 | V3 `$owner: String = "IronbellyOrg"` and V1 exact-header equality | Default value reads the fork silently when the variable is missing; exact header breaks on a harmless reorder (A1 section 2, D-12) |
| D-05 | A2 per-level split constants | claim.md:133 and design:201 disagree; one boolean matches the stricter text; split stays an owner option |

## Risk Summary

| Change # | Risk | Impact if failed | Rollback |
|---|---|---|---|
| V-1 | Medium | A new config key and warning with no effect until opted in; wrong wiring could exclude the launch account by default | Remove the key and the warning; `approval_of` default empty is a no-op |
| V-2 | Low to Medium | Wrong reason word in the audit; no store effect (both reasons are `("skip", 0)`) | Revert the ordering sentence and the two fixtures |
| V-3 | Low | A closed gate leaves only Pipeline None launching until the owner flips the constant | Flip the constant in a reviewed commit |
| V-4 | Medium | Fail-open (field change moves no time) or void-all; Task 3a is the detector | Fall back to the level-specific label (OD-2) |
| V-5 | Low | One extra refused spelling | Remove one alternative and one test line |
| V-6 | Medium | Missed `for LL_C` entry silently allows; a missing allow row refuses a read | Revert the class rows; keep the loop and tests |
| V-7 | Low | Task 6 grows; a still-red file shows in Task 6 acceptance | Move the file back to Task 7 |
| V-8 | Medium | Coordinator must pass the run id; a missing id suppresses or duplicates a comment | Fall back to the static marker |
| S-2 | Low | A stale host guard passes preflight and keeps allowing issue writes | Reinstall hooks |
| K-1 to K-5 | Low to Medium | See the rows above | Each is additive |

## Review Status
- [x] Auto-approved (default)
- [ ] User-approved (--interactive)
- Approved by: auto
- Approval timestamp: 2026-11-19 (generated with this plan)

## Open owner decisions (last section)

These stay open after the merge. None is decided by this plan; the agent records each decision in chat per the approvals-through-chat rule and never asks the owner to write a file.

| # | Decision | Options and what the plan does meanwhile | Source |
|---|---|---|---|
| OD-1 | Ship gate: flip or waive | The constant stays False, so only Pipeline None launches. Flip it in a reviewed commit that also un-skips the observation after `OB-H1 item 1`, `OB-H1 item 5`, `OB-H2`, `OB-H3` pass; or waive it in the owner's own words (V2 Option B), which makes the ship-gate sentence in `commands/issue.md`, `sc-issue-protocol/SKILL.md`, `refs/claim.md:133` and the design (:10, :201, :625) false and costs four more files in Task 7. Also owner-visible: `refs/claim.md:133` (item 1 for any governed claim) versus design:201 (item 1 only for full or submit), and the A2 per-level split | R2 point 3; probe I-3 |
| OD-2 | `updatedAt` observation, Task 3a | An owner action on a throwaway issue: change Pipeline, then Status, then apply the approval label, and record the times in `./artifacts/t3a-updatedat-observation.md`. It blocks Task 4. If the result is fail-open or a false void, R31 falls back to a level-specific approval label (Tasks 4, 5, 13, 16 change; Status-by-level labels needed) | R2 point 4; probe I-2 |
| OD-3 | I-9 warn-first enforcement | Switch enforcement on and approve from a second login (or give the watcher a dedicated launch login, a Coder row), or accept the residual. The approvers file holds the launch account 7361222 today (source.md:64) | R2 point 1; probe I-9 |
| OD-4 | I-10 tamper-list for `~/.config/superclaude` | Add `*.config/superclaude*` to the tamper tokens at guard:764 and the plugin mirror with a must-refuse test, or record in plan:23 that the directory is trusted and why. Neither choice leaves the V-1 key and any future config key exactly as writable as the approvers file | probe I-10, K-5 |
| OD-5 | Which pipelines do not end at In review | The owner said "most" (R24, source.md:75); the plan default is that all four end there. The merged plan keeps the default until the owner names the exceptions | source.md:75 |

Also for owner awareness (not blockers): confirm once that the extra fail-closed refusals are acceptable (A-007, I-15); the two weak debate rows D-10 (marker keyed on the approval event id) and D-02 extra (`complete.run`, best-effort) in `debate-transcript.md`; credential separation for launched agents is a Coder row and not part of this plan (A-002).
