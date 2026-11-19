<!-- Provenance: produced by /sc:adversarial Step 5 (merge-executor), 2026-11-19 -->
<!-- Base: Variant 2 (opus:architect), adversarial/variant-2-opus-architect.md -->
<!-- Plan applied: adversarial/refactor-plan.md (V-1..V-8, S-1..S-8, K-1..K-5, T-1..T-3, I-1..I-17) -->

# Remediation proposal: watcher plan v3, findings Q-1 to Q-10

Plan: `.dev/tasks/to-do/TASK-WF-requirements-20261119-012839/TASK-WF-requirements-20261119-012839.md` (written `plan:N`; every plan line below was re-read on 2026-11-19). Guard: `src/superclaude/hooks/scripts/launch-level-guard.sh` (`guard:N`), with its mirror `plugins/superclaude/hooks/scripts/launch-level-guard.sh`. Other repo paths are relative to `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/`.

Edit rule for every change below: edit `src/` and `plugins/superclaude/`; never edit or stage anything under `.claude/`; `.dev/tasks/` stays staged. Nothing here edits the plan package; these are the edits the plan owner applies.

Citation rule: a line number without a mark was read in this session. "(carried)" means a variant or the debate stated it and it was not re-read here.

Owner decisions kept: only the coordinator comments and moves Status to In review (plan:23); an approval is void when the Project item changed after it (R31, plan:65); cron may launch all four levels (plan:25).

Net effect of the merged proposal: one new owner-action task (3a), one new guard class, one new constant, one new config key (warn-first), one new reason word `level_gated`. No new Python module.

## Decisions the owner must make

<!-- Source: Round 2 verdicts V-1, V-3, V-4; probe I-3, I-9, I-10; refactor-plan "Open owner decisions" -->

Take these one at a time. Each answer is given in chat; the agent records it and never asks you to write a file. The plan builds and tests everything with the defaults below, so none of them blocks the build except decision 2, which blocks only Task 4.

### Decision 1. Ship gate: keep it closed, flip it, or waive it

The observations that the design says must pass before any governed launch (`OB-H1` items 1 to 9, `OB-H2`, `OB-H3`) have not been run: every one is a skipped test (`tests/hooks/test_launch_level_observations.py:79-84`).

| Option | What it does |
|---|---|
| A. Keep the constant closed (default) | `GOVERNED_LEVELS_ALLOWED = False` in `launch.py`. Only Pipeline None launches. Everything else is built and tested. You flip it later in a reviewed commit that also un-skips the observations. |
| B. Waive the gate | You say so in chat; the plan records the waiver. Unattended Full Submit launches then happen with subagent identity unverified, and the ship-gate sentence in `commands/issue.md`, `sc-issue-protocol/SKILL.md`, `refs/claim.md:133` and the design becomes false, so four more files change in Task 7. |
| C. Split per level | Two constants: item 5 plus `OB-H2` and `OB-H3` unlock Worktree; item 1 also unlocks Full and Full Submit. Not the default because `refs/claim.md:133` (item 1 for any governed claim) and the design U1 text (`docs/designs/sc-issue-launch-level-hook.md:201`, carried) disagree, and one boolean follows the stricter text. |

Recommendation: A. It keeps both of your decisions true (cron may launch all four levels as a capability; nothing unobserved launches) and costs about 6 lines.

### Decision 2. Run the `updatedAt` observation (Task 3a)

You change Pipeline, then Status, then apply the approval label on a throwaway issue; the agent reads the times after each step and saves them to `./artifacts/t3a-updatedat-observation.md`. This blocks Task 4.

| Option | What it does |
|---|---|
| A. Run the observation (default) | Confirms that a field change moves the field-value time and a label does not. |
| B. Skip it and ship the rule unobserved | The rule may fail open (a change moves no time) or void every approval. The equality check in `_revalidate` is the only backstop. Not recommended. |
| C. Fall back to a level-specific approval label | Needed only if A shows a fail-open or a false void. Tasks 4, 5, 13 and 16 change, and Status-by-level labels are needed because a level label does not cover a Research to Debug move. |

Recommendation: A. If it fails, come back and choose C.

### Decision 3. Self-approval by the launch login (warn-first)

The approvers file holds the launch account 7361222 (`source.md:64`, carried), and `approval_of` accepts any approver id (`predicates.py:216-223`). A launched agent that runs under that login can approve its own plan.

| Option | What it does |
|---|---|
| A. Warn only (default) | The exclusion list stays empty. `check-config` and the Task 17 first-run report print `approver_is_launch_account`. Nothing changes until you opt in. |
| B. Enforce now | The launch account is excluded from approvers. With one login this stops every launch on the first cycle until you approve from a second login. |
| C. Accept the residual | No key, no warning beyond the plan text. |

Recommendation: A now. Move to B when a second login exists or the watcher gets a dedicated launch login (a Coder row). Even B does not stop an agent that holds the same token; only credential separation does.

### Decision 4. Protect `~/.config/superclaude` from launched agents

The guard's tamper tokens do not name the directory (`guard:764`), so an agent can edit `issue-watch.json` (project id, `enabled`) and the approvers file. This is the one invariant no variant covered (I-10).

| Option | What it does |
|---|---|
| A. Add `*.config/superclaude*` to the tamper tokens (guard:764 and the mirror) | Edit and shell-redirect writes to that directory are refused for governed sessions; adds a must-refuse test. Over-match: any governed command whose text mentions that path is refused, reads included. |
| B. Record that the directory is trusted | One sentence in plan:23 saying why. The Decision 3 key and any config key are then exactly as writable as the approvers file. |

Recommendation: A, with the over-match accepted and tested.

### Decision 5. Which pipelines do not end at In review

You said "most" (R24, `source.md:75`, carried). The plan keeps all four ending at In review, held in one table, so an exception is one line. Recommendation: keep the default until you name the exceptions.

### Decision 6. Confirm the extra refusals once (A-007)

The merged guard also refuses `gh label` and `gh project` writes and every `gh issue` verb except view, list and status at every level, Full Submit included. `gh project item-list` and `gh project field-list` stay allowed. Please confirm in chat that you accept these; the plan records your answer in Task 24.

Weak debate rows you may overrule: the per-run result marker keyed on the approval event id (Q-6, convergence 1 of 3) and the best-effort `complete.run` pattern (Q-1 item 4, convergence 1 of 3).

## What changes in the plan task list

<!-- Source: refactor-plan rows V-3, V-4, V-7, V-8, S-2, S-8; Variant 2 Q-3, Q-10 -->

| Task | Change |
|---|---|
| Constraints (plan:17-28) | Reword plan:23 (Q-1, Q-9); add the same-file ordering line (Q-10); state that `~/.config/superclaude` is or is not tamper-protected (Decision 4). |
| Task 3 (plan:53-61) | Reads `createdAt` and `updatedAt` of the Status and Pipeline values, not item `updatedAt`; introspects the single-select value type and fails if either field is absent. |
| **Task 3a (NEW, after Task 3)** | Owner action, no code: the `updatedAt` observation (Decision 2). Blocks Task 4. |
| Task 4 (plan:63-72) | Depends on Task 1, Task 3 and Task 3a (plan:67). Rule voids on an unreadable or equal time; adds the same-second test. |
| Task 5 (plan:76-96) | Notes that the coordinator's Status move voids the approval by design and a relaunch needs a fresh approval. |
| Task 6 (plan:100-110) | Gains: the `level_gated` ship gate, the `_revalidate` reason order, the `excluded_ids` wiring and `check-config` warning (assignment of V-1 to Task 6 is the merge executor's choice, since `cycle.py` is edited there), and all seven `tests/issue_watch` files from Task 7. Acceptance becomes `uv run pytest tests/issue_watch -q`. |
| Task 7 (plan:112-122) | Drops the seven `tests/issue_watch` files from its list (plan:114); keeps commands, skills, WORKER-CONTRACT, docs and the other tests. |
| Task 9 (plan:139-148) | Per-run result marker; `project_id` parameter; compare-and-set on Status; imports the allowed-Status constant; depends on Task 3, 5, 6 (plan:143). |
| Task 10 (plan:150-160) | The guard change in full, the version bump to 2 with its three test pins, the new tests; `--project-id` on the verb. |
| Task 11 (plan:164-173) | DF-14 assertion restated; Task 11 reads DF-14 first. |
| Task 15 (plan:207-216) | Depends on Task 9 (plan:211); never writes the launch account id into a generated approvers file. |
| Task 17 (plan:229-237) | First-run report prints the gate state and `approver_is_launch_account`. |
| Task 22 (plan:285-293) | Documents who flips the gate, each new reason word with one plain sentence, a rollback line per finding. |
| Task 24 (plan:306-316) | Records the open decisions 1 to 6. |

Order: 1, 2, 3, 3a (owner), 4, 5, 6, 7, 8, 9, 10, 11 onward unchanged.

## Q-1 BLOCKING: Full Submit agents can write to issues (Tasks 10, Constraints)

<!-- Source: Base (Variant 2 Q-1), modified by V-6 (scope), V-5 (extra pattern), S-1, S-2, S-6, K-1, K-2, K-3 / Round 2 verdicts 5 and 6 -->

**Decision.** One blocked class, `ISSUE`, covers `gh issue`, `gh label` and `gh project` writes at all four levels, Full Submit included. It goes after the read-allow row, with `project item-list` and `project field-list` allowed first. The guard version stamp goes to 2. The coordinator-only pattern gains the narrow `complete` spellings.

Evidence read: `'issue create' | 'issue edit' | 'issue comment'` share the SUBMIT line with the pr verbs (guard:653), and `SUBMIT:FS` is allowed (guard:790), so plan:23's "keeps refusing issue comments" is false at Full Submit today. Reads are allowed first by `*' view' | *' list' | *' status' ...` (guard:652). The class list that is evaluated is the `for LL_C in` list at guard:786; the case table starts at guard:788 (the debate cited 788 for the `for` list; the file says 786). A class missing from that list is never evaluated.

**Plan edits**
- plan:23 last sentence becomes: "The launch-level guard refuses every `gh issue`, `gh label` and `gh project` write at every level, Full Submit included (Task 10), and every `gh api` write at every level (guard:798). This is a text check on `gh` commands only: a script or another HTTP client is not seen. The complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision). This is the one place Q-1 goes beyond issue verbs."
- plan:23 also adds (Q-9, I-8): "Governed: a session with a record in the launch-level store (agents launched at Worktree, Full, Full Submit; bound workers). Not governed: the watcher-launched `--pipeline none` claim session and the coordinator. The claim session's two marked comments are allowed by design and it reads untrusted issue text under the launch login."
- plan:152 (Task 10 body) adds items 1 to 5 below. plan:158 replaces "still refuse `gh issue comment` at Worktree and Full" with: "refuse `gh issue create`, `gh issue edit 5 --add-label issue-watch:approved`, `gh issue comment 5`, `gh issue close 5`, `gh label create x`, `gh project item-edit`, `true && gh issue comment 5` and the `-R o/r` forms with LL-ISSUE at W, WA, F and FS; `gh issue view 5`, `gh issue list`, `gh project item-list` and `gh project field-list` stay allowed at every level; `gh pr comment 5` still passes at FS." plan:152 also states: "The `complete` pattern is best-effort, not a control (A-002); the grant-row rule (WORKER-CONTRACT.md:300) is the control."

**Code changes (Task 10, guard and mirror)**
1. guard:653: remove the three issue verbs so the line reads `'pr create' | 'pr edit' | 'pr comment' | 'pr ready') LL_CLASSES+='SUBMIT ' ;;`. Insert before it (after guard:652): `'project item-list' | 'project field-list') ;;` then `'issue '* | 'label '* | 'project '*) LL_CLASSES+='ISSUE ' ;;`. It fires whether or not `gh` is in command position, like SUBMIT.
2. guard:786: add `ISSUE` to the `for LL_C in` list after `GHWRITE`. Case table: add `ISSUE:W | ISSUE:WA | ISSUE:F | ISSUE:FS) ll_deny LL-ISSUE ;;` (K-1).
3. `ll_say`: add `LL-ISSUE` with Blocked (a GitHub issue, label or project write), Why (only the coordinator writes; a launched session reports through `.dev/issues/<N>/result.md`), You can (write the result file and let the coordinator post). Reword LL-SUBMIT (guard:71) from "pull request or issue" to "pull request".
4. guard:444 coordinator-only pattern gains: `*issue-pipeline*complete* | *issue_pipeline.complete* | *issue_pipeline/complete.py* | *issue_pipeline*import*complete* | *issue_pipeline*complete.run*`. Never `*issue_pipeline*complete*`: it refuses `uv run pytest tests/issue_pipeline/test_complete.py`. The hyphen alternative also refuses `plan-hash` with a path containing "complete"; either anchor it on the verb word or record the over-match as accepted and tested (K-3).
5. Version stamp: bump guard:10, the mirror line 10, `GUARD_VERSION_LINE` (`src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:839`) and the three pins (`tests/hooks/test_launch_level_guard.py:251`, `tests/skills/test_issue_orca_worktree.py:1283` and `:1914-1916`) to 2 together. Release note: hosts run `superclaude install --force` before the next claim.

**Self-approval, Part B (V-1, warn-first; Decision 3).** `approval_of` (`predicates.py:185`) gets `excluded_ids` (default empty). One new closed-set key is added to `_TOP_KEYS` (`cycle.py:58-69`) and passed at both call sites (`cycle.py:883` and `:998`). `check-config` (`cli.py:185-198`, new warning line) and the Task 17 report print `approver_is_launch_account` when the approvers file holds the launch account. The Task 15 generator never writes the account id into a generated approvers file. plan:24 adds: "approval by the launch account is accepted unless the owner sets the exclusion key." State in the plan that `~/.config/superclaude` is not in the guard's tamper list (guard:763-765), so Part B limits an honest-but-injected session, not a hostile one (Decision 4).

**Tests**
- `tests/hooks/test_launch_level_guard.py`: move the three issue rows out of `GH_ORACLE["SUBMIT"]` (rows at 2743-2745) into a new `"ISSUE"` row with `("LL-ISSUE",) * 4`; remove them from T-GH-5 (2875-2876); add `ISSUE` to the class list near 778 and the expected-result grid at 797 (which today maps `"SUBMIT"` with FS `None`); add every over-match (hyphen alternative, `project item-list`) as an expected result; assert each new code prints a nonempty three-part message; assert a guard stamped 1 is refused; add the unbound-session-allowed test labelled "documents, does not endorse" (S-7).
- `tests/hooks/test_launch_level_guard_worker.py`: must-refuse: `superclaude issue-pipeline complete --repo o/r --issue 5`, the `uv run` form, `python -m superclaude.cli.issue_pipeline.complete`, `from superclaude.cli.issue_pipeline import complete`, `from superclaude.cli.issue_pipeline.complete import run`, `p.complete.run()`. Must-allow: `plan-hash`, `check-approval`, `uv run pytest tests/issue_pipeline/test_complete.py`, `uv run pytest tests/issue_pipeline/test_complete_cli.py`, `plan-hash` with a path containing "completed". `stage-status` stays unclassified and the plan says so.
- Predicate test for an excluded id; `check-config` prints the warning.

**Must pass:** `uv run pytest tests/hooks tests/skills tests/issue_pipeline tests/issue_watch -q`, `make verify-sync`.

**Residual risks.** The guard is text-only (guard:774-775): a script, `getattr` or `importlib` is not seen (A-002, open by nature). Warn-first leaves self-approval open until you opt in. New refusals block more commands (Decision 6). The `complete` verb does not check the grant row itself. At Full Submit, `/sc:pr-submit`'s re-trigger and thread replies use `gh api --method POST` (`refs/review-retrigger.md:27`, carried), which GHWRITE already refuses; out of scope, flagged. Rollback: revert the class rows and keep the loop entry and tests; remove the config key and warning (the empty default is a no-op).

## Q-2 OWNER DECISION: ship gate (Tasks 6, 17, 22)

<!-- Source: Base (Variant 2 Q-2 Option A) plus Variant 1 coupling test / V-3, S-5 -->

**Decision.** Option A of Decision 1. No config key as the switch: the config directory is not tamper-protected (guard:763-765), so a config switch would be as writable as the approvers file.

**Plan edits.** plan:102 (Task 6 body) adds the constant and refusal. plan:108 adds the tests. plan:287 (Task 22) documents who flips the switch. Task 17 report prints the gate state.

**Code and tests.**
- `src/superclaude/cli/issue_watch/launch.py`: `GOVERNED_LEVELS_ALLOWED = False`.
- `cycle.py` `_examine`: before `_launch` (`_launch` at `cycle.py:1026` sets `c.launching` at `:1028`), raise `_Skip("level_gated")` for any Pipeline other than None, so `would_launch` stays honest.
- `audit.py` `REASON_TABLE` (`audit.py:26`): one row `"level_gated": ("skip", 0)`.
- Tests: Full Submit gives `level_gated` and no launch; None launches. Coupling test in `tests/hooks/test_launch_level_observations.py` beside `_PENDING` (line 79): when the constant is True, none of `OB-H1 item 1`, `OB-H1 item 5`, `OB-H2`, `OB-H3` is in `_PENDING`.

**Must pass:** `uv run pytest tests/issue_watch tests/hooks -q`.

**Residual risks.** Until the flip, only None launches. The `refs/claim.md:133` versus design:201 (carried) mismatch stays an owner note. Rollback: flip the constant in a reviewed commit.

## Q-3 OWNER DECISION: what moves when the Pipeline or Status changes (Tasks 3, 3a, 4)

<!-- Source: Base (Variant 2 Q-3 Option C, Task 3a) + Variant 1 (unreadable voids) + Variant 3 (same-second test, outcome table) / V-4, T-1, T-2 -->

**Decision.** Option C: read `createdAt` and `updatedAt` of the Status and Pipeline single-select value objects; item-level time is excluded. An unreadable or equal time voids the approval. Task 3a confirms behaviour once.

Evidence: `PROJECT_ITEMS_QUERY` reads only the Status `name` today (`github.py:88-103`), and `ProjectItem` has no time (`predicates.py:112-118`). Docs show `createdAt` on the single-select value type; `updatedAt` on that type was not seen in the extract (carried from the debate).

**Plan edits**
- plan:55: replace "the Project item's `updatedAt`" with "`createdAt` and `updatedAt` of the Status and Pipeline values"; the schema check also reads `__type(name: "ProjectV2ItemFieldSingleSelectValue")` and the task stops with the R31 fallback if either field is absent. `ProjectItem` gets `status_changed_at` and `pipeline_changed_at` instead of `updated_at`.
- plan:58: acceptance checks both names in the saved artifact.
- plan:65: compare the later of the two times with the approval time; void on an unreadable time and on an equal time (one-second resolution, `predicates.py:257`); both `_examine` and `_revalidate` call it.
- plan:67 becomes "Depends on: Task 1, Task 3, Task 3a".
- plan:70: add a same-second case: equal time voids, a value an hour older passes.
- New Task 3a text: the owner changes Pipeline, then Status, then applies the approval label; between steps the agent runs the read-only query and records four values in `./artifacts/t3a-updatedat-observation.md`. Outcome table: field change moves the time and a label does not: rule as written. Field change does not move it: fail open; stop and return the level-specific label (R31 fallback) to the owner. A label moves it: total outage; same stop.
- Task 5: the coordinator's own move to In review bumps the Status value time and voids the approval by design.

**Tests.** `tests/issue_watch/test_predicates.py` (before, equal, after, unreadable), `tests/issue_watch/test_github.py` (fixtures with value times, null, malformed), `test_cycle.py` (Pipeline raised after approval ends `edited_after_approval`). **Must pass:** `uv run pytest tests/issue_watch -q`.

**Residual risks.** GitHub runtime behaviour is unobserved until Task 3a (A-004) and nothing re-checks it afterwards. Rollback: the level-specific label (Decision 2 option C).

## Q-4 BLOCKING: two reasons for one reread (Tasks 4, 6)

<!-- Source: Variant 1 Q-4 order / V-2 (Round 2 verdict 2, 2 of 3) -->

**Decision.** In `_revalidate` the order is: approval reread (existing, `revalidation_failed`, `cycle.py:1007-1011`), then the time rule (`edited_after_approval`), then `project_check` and examined-versus-reread equality (`revalidation_failed`, `cycle.py:1015-1016`). This replaces the base sentence that put the time check first. It keeps plan:71 (owner-derived) true.

**Plan edits.** plan:102 adds: "In `_revalidate`, after the approval reread and the items reread (cycle.py:1012-1014), the Task 4 time rule runs and raises `edited_after_approval`; only when it passes do `project_check` and the examined-versus-reread comparison run, each raising `revalidation_failed`." plan:108: the existing fixtures keep every field time before the approval so the equality check is reached; add the overlap case (Pipeline lowered with a late field time ends `edited_after_approval`). Neither case makes a launch call.

**Must pass:** `uv run pytest tests/issue_watch/test_cycle.py -q`.

**Residual risks.** Audit counts of `revalidation_failed` drop. Both reasons are `("skip", 0)` (`audit.py:71,80`), so there is no store effect. Rollback: revert the ordering sentence and two fixtures.

## Q-5 MEDIUM: Status move can hit the wrong item (Task 9)

<!-- Source: Variant 1 Q-5 compare-and-set + Variant 2 Q-5 refusal words / S-3, I-4 -->

**Decision.** `complete` selects the one non-archived item of the given Project, then moves Status only when the current Status is one of Research, Spec, Plan or Debug. Otherwise it posts the comment with `status_moved_by_person` and does not write.

**Plan edits.** plan:141: the function also takes `project_id` (validated `^PVT_[A-Za-z0-9_-]+$`); for `succeeded`, before any write (the comment included) it reads the issue's items and selects the item using the helper Task 6 adds next to `project_check`; zero gives `refused:project_missing`, more than one `refused:project_ambiguous`, a Status field without an In review option `refused:status_option_missing`; a current Status outside the four allowed gives the comment plus `status_moved_by_person`. It imports the allowed-Status constant Task 1 names (plan:34) instead of copying the four words. plan:143 becomes "Depends on: Task 3, Task 5, Task 6". plan:146 adds the refusals (zero calls after the read) and a test with the item at Done: no mutation. Task 10's verb takes `--project-id`; the coordinator copies it from the repo's watcher config. The plan notes the read-then-write window is not atomic.

**Must pass:** `uv run pytest tests/issue_pipeline/test_complete.py tests/issue_watch/test_security_invariants.py -q`.

**Residual risks.** One more read per completion; a person's move inside the window can still be overwritten. Rollback: unconditional write is the rejected alternative; revert to it only on owner request.

## Q-6 MEDIUM: the result marker is shared (Task 9, design note)

<!-- Source: Variant 1 Q-6 idea, key changed by the orchestrator / V-8 (Round 2 verdict 8, 1 of 3, WEAK ROW) -->

**Decision.** Per-run marker `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->`, replacing the static marker. The key is the approval event id because each relaunch needs a fresh approval (`mark_pending` allows relaunch from `failed`, `record.py:545-547`), so it is unique per run and known whenever a run exists. It never contains `CLAIM_MARKER` (`predicates.py:14`).

**Plan edits.** plan:87, 141 and 146: `complete` suppresses a post only for an exact marker written by its own login. The design note states the counted login is the workspace's single `gh` login, shared by the watcher, the coordinator and launched agents. Task 8 duties: the coordinator passes the run id.

**Tests.** The marker does not contain `CLAIM_MARKER`; `marker_comments` evidence ignores a result comment; another run id does not suppress; another login does not suppress; same run id and login does. Own-login comments never void an approval (`predicates.py:253-255`); one test shows the coordinator's comment leaves `unchanged_since` clean.

**Residual risks.** Overrules 2 of 3 advocates; the coordinator must pass the run id, and a missing id suppresses or duplicates a comment. Rollback: fall back to the static marker.

## Q-7 MEDIUM: Task 6 cannot pass its own acceptance (Tasks 6, 7)

<!-- Source: Base (Variant 2 Q-7) + Variant 1 tip / V-7 (3 of 3) -->

**Decision.** Move the seven files to Task 6. Recount: 45 `--pipeline none` lines in 7 files (test_cli 3, test_cli_e2e 2, test_crash_injection 1, test_cycle 6, test_launch 14, test_no_text 4, test_security_invariants 15), counts carried from the debate; the reason is real: `launch_argv` rejects a prompt that does not fullmatch `PROMPT_PATTERN` (`launch.py:101`, pattern at `:33`, old prompt built at `:92`).

**Plan edits.** plan:114: remove the seven `tests/issue_watch` files from Task 7's list. plan:109 (Task 6 acceptance) adds `uv run pytest tests/issue_watch -q`. Write the new `_PROMPT_RE` out in the test; do not import it from `launch.py`.

**Residual risks.** Task 6 grows; a still-red file shows in Task 6 acceptance. Rollback: move a file back to Task 7.

## Q-8 NOTE: restating DF-14 (Task 11)

<!-- Source: Variant 1 Q-8 count + Variant 2 Q-8 regex / S-4, I-17 -->

**Decision.** `repository(owner:, name:)` needs non-null variables, so `$owner` and `$name` are `String!`. Line 919 of `tests/issue_watch/test_security_invariants.py` bans `"String!"` (read: `assert "$after: String)" in query and "String!" not in query  # DF-14`). plan:166 becomes: "Line 919 becomes: `$after: String` stays nullable; the regex `\$(\w+): String!` yields exactly {owner, name}; `count("String!") == 2`; no literal repository; no `mutation`." Reject `$owner: String = "IronbellyOrg"` (default value silently reads the fork when a variable is missing). Task 11 reads DF-14 first (research 06, carried) and stops if it forbids non-null variables outright.

**Must pass:** `uv run pytest tests/issue_watch/test_security_invariants.py tests/issue_pipeline -q`. Risk: low.

## Q-9 NOTE: which sessions the guard governs (Task 10, plan:23)

<!-- Source: Variant 2 Q-9, convergent / S-7, I-8 -->

**Decision and edits.** The plan:23 text under Q-1 above. Basis: an unbound session exits 0 (guard:153-154 and :391, read). That the watcher-launched `--pipeline none` session has no store record is an inference from `refs/claim.md:118` (carried) and is not tested. Task 10 adds the unbound-session-allowed guard test, labelled "documents, does not endorse". The guard's store-record lookup at guard:257-268 was not re-read here (carried).

## Q-10 NOTE: dependency edges and ordering (Constraints, Tasks 4, 8, 15)

<!-- Source: Variant 2 Q-10 + Variant 1 replacement sentence / S-8 -->

- plan:67 Task 4: add Task 1 and Task 3a. plan:211 Task 15: add Task 9 (its argv scan, plan:216).
- Constraints, new line: "Tasks that edit the same file run in plan order, never in parallel: `cycle.py` (4, 6, 12, 18), `launch.py` (6, 12), `github.py` (3, 11), `predicates.py` (1, 3, 4, 6), `WORKER-CONTRACT.md` (8, 10), `test_security_invariants.py` (3, 6, 9, 11). Task 1 leaves `cycle.py` unchanged (plan:34)."
- plan:87 and Task 8: after the coordinator mirrors the Status (WORKER-CONTRACT.md:298) or moves it to In review, the Project values have changed, so any relaunch needs a fresh approval label.
- plan:88: the replacement for WORKER-CONTRACT.md:245 (read: the push-needs-the-person's-go rule) keeps "the coordinator never pushes worker commits on the Pipeline setting"; at Full Submit only the launched agent pushes its own feature branch. `tests/skills/test_worker_contract.py` asserts the new sentence.

## Residual risks (whole proposal)

<!-- Source: Base residual risks, reworded by V-1 and S-6; Variant 3 "Unverified" and rollback structure (T-3) -->

1. The guard is text-based: Python or another wrapper that shells out to `gh` or calls `complete.py` in an unusual spelling is not seen. Credential separation (a Coder row) is the real control.
2. Self-approval stays open until Decision 3 is taken.
3. Q-3 rests on GitHub's field-value timestamps; Task 3a confirms once.
4. Without Decision 1 option A, plan:25 and `refs/claim.md:133` contradict each other in production.
5. The `complete` verb does not check the issue's grant row; that stays a rule (WORKER-CONTRACT.md:300, read). A code check is out of scope.

Ranked impact (T-3): Q-1 (silent issue writes at Full Submit), Q-3 (approval provenance), Q-2 (unobserved governed launches), Q-5, Q-6, Q-4, Q-7, Q-8 to Q-10.

## Not verified

- GitHub runtime behaviour of field-value times (A-004); whether `updatedAt` exists on `ProjectV2ItemFieldSingleSelectValue`.
- Carried and not re-read: `source.md:64` and `:75`; `docs/designs/sc-issue-launch-level-hook.md:10, :201, :625`; `refs/review-retrigger.md:27`; `reply-resolve-thread.sh:131`; DF-14 text; guard:257-268; per-file counts of `--pipeline none`; `tests/hooks/test_launch_level_guard.py` lines 2739-2745 beyond what a search showed.
- Whether the watcher-launched `--pipeline none` session truly has no store record.
- No test was run; every test named above is a requirement, not an observed result.
- The debate cited the `for LL_C in` list as guard:788; this merge read it at guard:786.
