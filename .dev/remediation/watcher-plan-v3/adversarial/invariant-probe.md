# Invariant probe - merged remediation for watcher plan v3

Base: `/home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/`. Folder: `.dev/remediation/watcher-plan-v3/adversarial/`. Companion: `round2-rebuttals.md` (verdicts V-1 to V-8 below mean its points 1 to 8). `guard` = `src/superclaude/hooks/scripts/launch-level-guard.sh`; `plan` = `.dev/tasks/to-do/TASK-WF-requirements-20261119-012839/TASK-WF-requirements-20261119-012839.md`.

Status words: ADDRESSED (the merged text, after Round 1 concessions and Round 2 verdicts, holds the invariant), PARTIAL (holds with a stated limit or a missing piece), UNADDRESSED (no variant covers it). Per-variant cells say what that variant alone gives. Facts marked (read) were checked in this session; (run) were tested with a bash `case` probe; (carried) come from a variant or advocate and were not re-read.

## Summary

| Status | Count | IDs |
|---|---|---|
| ADDRESSED | 9 | I-3, I-4, I-5, I-6, I-12, I-13, I-14, I-16, I-17 |
| PARTIAL | 7 | I-1, I-2, I-7, I-8, I-9, I-11, I-15 |
| UNADDRESSED | 1 | I-10 |

Highest severity open items: I-1 (script route, High, declared limit), I-2 (R31 unverified, High), I-9 (self-approval, High, owner decision), I-10 (config directory not tamper-protected, Medium-High).

## Invariants

### I-1 Only the coordinator writes to GitHub, at every level including Full Submit (High) - PARTIAL
- V1: ADDRESSED for `gh` text: class `ISSUEWRITE` covers issue create/edit/comment/close/reopen/delete/transfer/lock/unlock/pin/unpin/develop plus `label` and `project` writes. V2: PARTIAL, `'issue '*` only, no label/project (guard:653-654 leave those at command-position-only UNKNOWN). V3: PARTIAL, create/edit/comment only. Concessions: A1 and A2 add label/project to V2's catch-all; A3 treats it as optional. Verdict V-6 takes it.
- Verified (read, run): guard:652 allows view/list/status first; a catch-all after it refuses `issue close`, `label create`, `project item-edit`; `gh api` writes are already GHWRITE at every level. Limit: the guard is text-only (guard:774-775); a script, `curl`, or Python that calls `gh` is not seen, and `/sc:pr-submit` itself posts through scripts (`reply-resolve-thread.sh:131`, carried). A-002 stays open by nature.
- Text to address: plan:23 must say "refused at every level, Full Submit included, for `gh` text only; a script or other HTTP client is not seen; the complete control is a token with no issues or projects write for launched agents (a Coder row, owner decision)". Plan:158 tests W, WA, F and FS for `issue edit --add-label`, `issue comment`, `issue close`, `label create`, `project item-edit`, `true && gh issue comment`, and `-R o/r` forms; `gh pr comment` still passes at FS.

### I-2 An approval is void when the Project item changed after it (High) - PARTIAL
- All three implement R31 (Task 4). V1: field times plus item time (V-4 drops the item time). V2: field-value times, Task 3a observation. V3: item time, observation, decision table.
- Open: GitHub's runtime behaviour is unobserved (A-004). Docs show `createdAt` on the single-select value type; `updatedAt` on that type was not seen in the extract (read). Until Task 3/3a runs, the rule can fail open (a field change moves no time) or void everything (a label moves the item time).
- Text to address: Task 3 introspection lists the single-select value fields and fails if `createdAt` or `updatedAt` is absent; Task 3a (owner action) records the four values in `./artifacts/`; Task 4 depends on Task 1, 3 and 3a; the rule voids on an unreadable time and on an equal time (one-second resolution, predicates.py:257, same-second test from V3); both `_examine` and `_revalidate` call it (plan:65); the plan states that a fail-open result returns R31 to the owner for a level-specific label. The coordinator's own move to In review bumps the Status value time and voids the approval by design (Q-10); say so in Task 5.

### I-3 No launch while the ship gate is closed (High) - ADDRESSED
- V1: module `ship_gate.py`, `ship_gate_closed`. V2: constant, `level_gated`. V3: config key, `launch_gate_closed` (rejected, C-2). Concessions: A1, A2, A3 take the code constant. Verdict V-3: single constant plus a coupling test.
- Verified (read): `_launch` has one caller (cycle.py:961), so a check in `_examine` before it covers every route; dry run returns inside `_launch` (cycle.py:1029-1035), so the check must sit before it to keep `would_launch` honest; all 12 observations are `pytest.skip` (test_launch_level_observations.py:79-84). The owner-visible mismatch between `refs/claim.md:133` (item 1 for any governed claim) and design:201 (item 1 only for full/submit) stays an owner note.
- Text to address: the constant is False in code; `_examine` raises `_Skip("level_gated")` for any Pipeline other than None; `level_gated` is one row in `audit.REASON_TABLE` as `("skip", 0)`; a test asserts the four required observation ids are not in `_PENDING` when the constant is True; the Task 17 first-run report prints the gate state; Task 22 documents who flips it (a reviewed commit that also un-skips the observation).

### I-4 Status moves only from the four allowed Statuses (High) - ADDRESSED
- V1: compare-and-set, comment only with `status_moved_by_person` otherwise. V2, V3: select the right item but write unconditionally (UNADDRESSED alone). Concessions: A2 and A3 yield to V1; V2's refusal words (`project_missing`, `project_ambiguous`, `status_option_missing`) and `^PVT_` check merged in (D-09, settled).
- Limit: read-then-write is not atomic (A3), so a person's move in the gap can still be overwritten; the GraphQL mutation has no conditional.
- Text to address: `complete.py` imports the allowed-Status constant that Task 1 names (plan:34 "one module constant") instead of copying the four words, so the two lists cannot drift; a test sets the item to Done and asserts no mutation; the plan notes the residual window.

### I-5 `pytest tests/issue_pipeline/test_complete.py` must not be refused in a launched or bound session (High) - ADDRESSED
- V1, V3: UNADDRESSED, `*issue_pipeline*complete*` refuses it (run: also refuses `test_complete_cli.py`). V2: ADDRESSED. Concessions: A1 and A3 yield to V2. Verdict: V2 patterns plus `*issue_pipeline*complete.run*` (V-5).
- Remaining defect (run): the hyphen alternative `*issue-pipeline*complete*` refuses `superclaude issue-pipeline plan-hash <dir> complete.md` and any `plan-hash` path containing "complete" (a `completed` directory), which G2 says must stay allowed (guard:442-443 comment).
- Text to address: G2 must-allow list adds `uv run pytest tests/issue_pipeline/test_complete.py`, `uv run pytest tests/issue_pipeline/test_complete_cli.py`, and `plan-hash` with a path containing "completed"; either anchor the hyphen alternative on the verb word or record the over-match as accepted and tested.

### I-6 The version stamp bump keeps old hosts refused (High) - ADDRESSED
- V1: UNADDRESSED (omits it). V2: ADDRESSED. V3: UNADDRESSED (said unread). Concessions: A1, A3 yield to V2 (D-03, settled).
- Verified (read): guard:10 and its plugin mirror line 10 say version 1; `GUARD_VERSION_LINE` is the same text at `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py:839`; pins at `tests/hooks/test_launch_level_guard.py:251`, `tests/skills/test_issue_orca_worktree.py:1283` and `:1914-1916`. An installed guard stamped 1 stops matching a required line `...: 2`, so the IR-4 preflight refuses it (the stale case is the one test at :1914-1916).
- Text to address: bump guard:10, the plugin mirror, `GUARD_VERSION_LINE` and the three test pins together in Task 10; edit `src/` and `plugins/superclaude/`, never `.claude/` (repo rule); add a test that a guard stamped 1 is refused after the bump. Release note: hosts must run `superclaude install --force` before the next claim.

### I-7 Every fail-closed path gives an owner-readable message (Medium) - PARTIAL
- Guard messages are three-part (Blocked, Why, You can) in `ll_say` (read). V2 gives full text for `LL-ISSUE`; V1 names `LL-ISSUE-WRITE` and says the message goes in the printer table without text; V3 names `LL-ISSUE` only. A class missing from the `for LL_C in` list at guard:788 is never evaluated, so it silently allows instead of printing `LL-BROKEN` (read).
- Watcher side: `level_gated`, the D-04 warning and the Q-5 refusal words are new closed words; `REASON_TABLE` holds only names and exit kinds (read), so the owner-readable sentence belongs in the `status` output and Task 22 docs; no variant specifies it.
- Text to address: in Task 10, add `ISSUE` to the precedence loop and the four-level case rows, and add one `ll_say` block (Blocked: a GitHub issue, label or project write; Why: only the coordinator writes, a launched session reports through `.dev/issues/<N>/result.md`; You can: write the result file and let the coordinator post). Reword LL-SUBMIT to "pull request" only. A guard test asserts each new code prints a nonempty three-part message. Task 22 lists each new reason word with one plain sentence.

### I-8 The claim session's ungoverned boundary is documented (Medium) - PARTIAL
- All three document it in plan:23 or Task 10 (D-13 convergent). V1 and V3 add a guard test that an unrecorded session is allowed (guard:153-154, 391, read). V2 cites `refs/claim.md:118` (read: Wave 8 runs only when `--pipeline` is not `none`).
- Gap: V1 and V3 mark "the claim session never gets a record" as inference. Nothing in the three variants is a test or a read that shows the watcher-launched `--pipeline none` session has no record.
- Text to address: plan:23 adds "Governed: a session with a record in the launch-level store (agents launched at Worktree, Full, Full Submit; bound workers). Not governed: the watcher-launched `--pipeline none` claim session and the coordinator; the claim session's two marked comments are allowed by design and it reads untrusted issue text under the launch login." Task 10 adds the unbound-session-allowed guard test and labels it "documents, does not endorse".

### I-9 No self-approval under the launch login (High) - PARTIAL
- V1: hard-refuse `excluded_ids`. V2, V3: residual risk only. Concessions: A1 retreats to warn-first; A2 and A3 ask for an owner decision. Verdict V-1: warn-first.
- Verified (read): approvers file holds the launch account 7361222 (source.md:64); `approval_of` has no exclusion (predicates.py:216-223).
- Limit: warn-first leaves the hole open until the owner opts in. Even enforced, GitHub cannot tell the owner from an agent that holds the same token, so only credential separation closes it.
- Text to address: plan:24 gains "approval by the launch account is accepted unless the owner sets `approval_excluded_ids`; `check-config` and the Task 17 first-run report print `approver_is_launch_account`"; the open decision is recorded in Task 24 with both options; the generator never writes the account id into a generated approvers file; a predicate test covers an excluded id.

### I-10 The config and approvers directory is not writable by a launched agent (Medium-High) - UNADDRESSED
- The tamper tokens name the store, `.claude/settings`, `.claude/hooks`, `disableAllHooks`, `.gitconfig`, `.git/config`, `.config/git` and nothing for `~/.config/superclaude` (guard:763-765, read). V1 uses this fact to reject a config key for the gate; no variant adds a control. An agent can edit `issue-watch.json` (project id, `enabled`, worktree) or the approvers file; adding an id already present changes nothing, but changing `project_id` or `enabled` changes where and whether the cron launches.
- Text to address (owner decision, one-token change): add `*.config/superclaude*` to the tamper tokens at guard:764 and the plugin mirror, with a must-refuse test for an Edit and a shell redirect on `issue-watch.json`, or record in plan:23 that the directory is trusted and why. Choosing neither leaves D-04's exclusion list and any future config key exactly as writable as the approvers file.

### I-11 The new coordinator-only `complete` verb is refused for bound workers and launched sessions (High) - PARTIAL
- V1, V2, V3 extend guard:444 (G2). Covered by I-5 for pattern shape. Limit: the pattern is text-only, so spellings outside the glob (`getattr`, `importlib`, a script) run it; the bound-worker rule is by contract (WORKER-CONTRACT.md:241-243, carried) at level None.
- Text to address: G2 tests list the must-refuse spellings (verb, `uv run` verb, `python -m ...issue_pipeline.complete`, `from ... import complete`, `from ....complete import run`, `p.complete.run()`); `stage-status` is left unclassified and the plan says so; plan:152 states that the pattern is best-effort and the grant row rule (WORKER-CONTRACT.md:300) remains the control. V2 residual risk 5 (the verb does not check the issue's grant row) stays an owner-visible limit.

### I-12 The result comment is posted once per run, not once per issue (Medium) - ADDRESSED
- V1: marker with launch op id (partial: `op=none` on an unknown outcome). V2, V3: one static marker (UNADDRESSED: a second run after a fresh approval finds the first run's marker and posts nothing, plan:141; `mark_pending` allows relaunch from `failed`, record.py:545, read). Verdict V-8: per-run marker keyed on the approval event id.
- Text to address: marker `<!-- sc:issue:result issue=<N> run=<approval_event_id> -->`; `complete` suppresses a post only for an exact marker by its own login; tests: another run id does not suppress, another login does not suppress, the same run id and login does.

### I-13 The result marker is never read as a claim marker (Medium) - ADDRESSED
- All three avoid `CLAIM_MARKER` (predicates.py:14, github.py `MARKER_JQ`, carried); A1 and A3 agree it is the real finding.
- Text to address: test that the result marker does not contain `CLAIM_MARKER` and that `marker_comments` evidence ignores a result comment.

### I-14 The coordinator's own comment never voids an approval, and its Status move voids it by design (Medium) - ADDRESSED
- A-006 holds for comments (predicates.py:253-255, read: own-login comments are skipped). The Status move changes the Status value and so the value time; Q-10 in all three says a retry needs a fresh approval.
- Text to address: Task 5 and Task 8 state both facts; one test shows the coordinator's comment leaves `unchanged_since` clean.

### I-15 Fail-closed extra refusals do not block the work launched agents are meant to do (Medium) - PARTIAL
- A-007 is unstated in the variants. After V-5 the over-match with `pytest` is gone; remaining over-matches are the hyphen alternative (I-5), `'project item-list'` and `'project field-list'` (read verbs that a bare `'project '*` refuses, run), and `grep -e complete.run` ordering (run).
- Text to address: allow rows for `project item-list` and `project field-list` ahead of the catch-all; the owner confirms once in chat that these refusals are acceptable (plan Task 24, "Open decisions"); the guard test grid lists each over-match as an expected result so a later glob change shows up in review.

### I-16 The test tree stays green between tasks (Medium) - ADDRESSED
- V1, V3 move one file to Task 6 and leave six red (recount, read: 45 `--pipeline none` lines in 7 files; `launch_argv` rejects an old prompt, launch.py:101; plan:102 changes `build_claim_prompt`). V2 moves all seven. Concessions: A1 leans V2; A3 yields. Verdict V-7: seven files.
- Text to address: Task 6 acceptance is `uv run pytest tests/issue_watch -q`; Task 7's list drops those files; write the new `_PROMPT_RE` in the test (V1 tip).

### I-17 The DF-14 cursor stays nullable and the query is not weakened (Low) - ADDRESSED
- V1: header equality plus `count("String!") == 2`. V2: regex yields exactly {owner, name}. V3: restate, or default value (rejected, C-4, A1 and A3 and A2 agree). Read: today's queries declare `$number: Int!, $after: String` with a hard-coded repository (github.py:84-90); line 919 of `test_security_invariants.py` bans `String!` (carried by A3 with DF-14 text, research/06 line 37).
- Text to address: assert `$after: String` stays nullable, the only `String!` variables are `$owner` and `$name` (regex), no literal repository, no `mutation`; plan:166 says Task 11 reads DF-14 first.

## Items no variant states that the merge executor must carry

1. The new guard class goes into the `for LL_C in ...` list at guard:788 or it is never evaluated (I-7).
2. `project item-list` and `project field-list` need allow rows (I-15).
3. `plan-hash` with a "complete" path is refused by the hyphen alternative (I-5).
4. Every guard change lands in `src/superclaude/hooks/scripts/launch-level-guard.sh` and `plugins/superclaude/hooks/scripts/launch-level-guard.sh`; nothing under `.claude/` is edited or staged (repo rule), and `.dev/tasks/` stays staged.
5. The config directory write path (I-10) is an owner decision; without it the D-04 key and any config switch are as writable as the approvers file.

## Not verified
GitHub's runtime timestamp behaviour (A-004); `refs/review-retrigger.md:27` and `reply-resolve-thread.sh:131`; WORKER-CONTRACT.md:241-245, 298-300; DF-14 text; whether the watcher-launched `--pipeline none` session truly has no store record (inference from claim.md:118).
