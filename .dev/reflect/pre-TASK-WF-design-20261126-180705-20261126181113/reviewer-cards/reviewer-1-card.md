# Re-review findings (reviewer 1, analyzer, sonnet class)

`PLAN` = `.dev/tasks/to-do/TASK-WF-design-20261126-180705/TASK-WF-design-20261126-180705.md`. The reviewer ran out of turns and reported from what it had read; items it did not reach are marked UNVERIFIED.

## Prior blockers

| id | status | evidence |
|---|---|---|
| M-01 | resolved | PLAN:30 bans only commands and argv the code or a primitive tells an agent to run; deny-list, refusal text, tests of refusals and forbidding sentences may name the tokens. |
| M-02 | resolved | PLAN:234 moves the S23 edit and the routing-test run out of Task 19; PLAN:244 and PLAN:247 put them in Task 20, after the skill file exists. `test_routing_refresh.py:101-107` resolves `sc:git-protocol` to `skills/sc-git-protocol/SKILL.md`; `make lint-architecture` Check 9 needs a name ending in `-protocol`, which `sc:git-protocol` satisfies. |
| M-03 | resolved | PLAN:284 and PLAN:288 scan only files this work adds; unchanged files are compared against the recorded base commit. |
| M-04 | resolved | PLAN:297 checks `test ! -e commands/sc-git.md` and a work-tree count; 21 files under `commands/` including `sc-git.md` were counted, so 20 after the delete; no file links to `sc-git.md`. |
| M-05 | resolved | Tasks 26 to 32 each copy their plugin twin (PLAN:306, 316, 326, 336, 346, 356, 366); Task 38 only verifies (PLAN:428). Byte-parity tests: `test_workflow_command.py`, `test_routing_plugin_parity.py`. |
| M-06 | resolved | PLAN:316 and PLAN:356 keep both new transient reasons in `refs/commit-step.md` only, in agreement with the `_TRANSIENT` pin at `test_task_workspace_lifecycle.py:611,682-688`. |
| M-07 | resolved | PLAN:306 and PLAN:366 add `_ALLOW` entries in the same task and record the T-16 override in PLAN:20; `test_implement_severity_static.py:296-434` is an exact one-entry-per-line match; step 1 of the gate (`managed-workspace.md` line 52) does not match `_SITE` today and a new `E-ARCHIVE-BLOCKED` mention in it would. |
| M-08 | resolved | PLAN:38 and PLAN:128 copy all nine patterns; `archive_workspace.py:44-67,181-208` confirms the nine; PLAN:20 records the DD-8 override. |
| M-09 | resolved | `record-skipped` is in PLAN:158, 161, 216; skipped settlement in PLAN:336; one ambiguity is row 5. |
| M-10 | resolved for T-04 and T-21; a residual remains | T-04 and T-21 cases are in PLAN:195, 225, 329 with the pins in Task 34 at PLAN:386; the remaining FR-109 cases are row 4. |
| M-11 | resolved | `.dev/implement/` is the first path rule in PLAN:170 with cases at PLAN:173 and PLAN:185; see row 7 for a wrong claim inside that text. |

## Prior medium findings (M-12 to M-24)

M-12 resolved (Task 4 from-scratch environment with `GIT_TERMINAL_PROMPT=0`, PLAN:72, 75; stop rule PLAN:254, 336). M-13 resolved (PLAN:366). M-14 resolved in intent (PLAN:62), but row 3 is a new defect. M-15 resolved (PLAN:386). M-16 resolved (PLAN:310, 350). M-17 resolved (PLAN:185). M-18 resolved (only the recording command remains, PLAN:31, 38). M-19 resolved (Task 24, PLAN:284, 287). M-20 still present as a contradiction (row 2). M-21 resolved (Task 30 covers `retry.md:437`; `SKILL.md:129`, `ledger.md:157`, `wc9-allowed` rows at `test_worker_contract.py:2341,2413` confirmed). M-22 resolved (PLAN:62, 83). M-23 resolved (PLAN:346, 408, 412). M-24 resolved (PLAN:432).

## Deviations (new or still open)

| # | Category | Location | What diverged | Evidence | Severity |
|---|---|---|---|---|---|
| 1 | Drift | Task 28, PLAN:326 | Medium: Task 28 says "a reply that carries no key is not a resolution and the STOP is shown again"; design FR-122 says "a reply naming no key counts only when exactly one key was displayed". Task 28's rule is stricter than the design with no recorded override; the static pin in Task 34 (PLAN:386, "no-key rule") would pin the stricter text. Under the design a single-key STOP answered with a bare "abandon" resolves; under the plan it never resolves. Not a safety failure (it fails closed). Affected action: Task 28 and Task 34's no-key pin. | `source.md:387`; PLAN:326, 329, 386 | MEDIUM |
| 2 | Drift | Constraints PLAN:28 vs Phases 6 and 7 | Medium: the Constraint says tests are written first in each task that adds behavior, but Tasks 19 to 23 and 26 to 33 add text behavior whose static pins arrive only in Task 24 and Task 34 at the end of each phase; Tasks 28 and 29 acceptance cite "pinned in Task 34" (PLAN:329, 339). The test-first rule cannot be followed for those tasks and no override is recorded. | PLAN:28, 284, 329, 339, 386 | MEDIUM |
| 3 | Drift | Task 3, PLAN:62, 65 | Medium: `validate_argv(argv)` takes only argv, yet its acceptance must reject `add` without a private `GIT_INDEX_FILE`, accept `add -A` with one, and reject `-A` printed in an agent argv; nothing says where the index or the agent-versus-runner mode comes from. Tasks 13 to 15 depend on this interface, so Task 3 and Task 15 can disagree. | PLAN:62, 65, 174 | MEDIUM |
| 4 | Missing | Task 17 acceptance, PLAN:215-216 | Medium: the FR-109 and T-19 cases still missing from the acceptance: revocation, a stale installed copy's later `start` (`out-of-protocol`), a changed managed plan (`plan-changed` before prepare), `git gc --prune=now` between crash and resume for boundary pins, an unflagged completion followed by a flagged re-review, a resumed batch, and "a halt gives no commit". Task 38 AC-16 and AC-19 depend on them (PLAN:433); the task body says only "segment and eligibility cases of T-19", so a wrong implementation could pass. | `merged-requirements.md:580,682`; PLAN:215-216 | MEDIUM |
| 5 | Drift | Task 12, PLAN:158, 161 | Medium: `record-skipped` is not tied to the flag. Design rows 290 and 291 sit under a "Run with flag" table; the plan says an unflagged due boundary "stops unsettled" and also that a mixed or empty boundary gives `record-skipped` (PLAN:216); Task 27 says an unflagged run writes only one `off` line (PLAN:316). Which action an unflagged run gets for a mixed or empty boundary is undefined. | `source.md:289-291`; PLAN:158, 216, 316 | MEDIUM |
| 6 | Drift | Task 3, PLAN:62 | Medium: `version` is described as "the `--version` form, no other option"; the runner builds `<verb> <options>`, so the exact argv form is undefined and Task 5 acceptance does not test it. UNVERIFIED whether `git -c ... --version` works with the runner prefix (believed to). | PLAN:62, 83 | MEDIUM |
| 7 | Drift | Task 13, PLAN:170 | Medium: it says to skip a `.dev/implement/` path "with the `why` the design names for it"; the design names none (`source.md:228` lists "under `.dev/implement/`" with no token, `merged-requirements.md:475` says only "listed in `skipped` with its reason"). The acceptance (PLAN:173) tests only "skipped", so nothing fails, but the stated anchor is false and the token is invented. | `source.md:228`; `merged-requirements.md:475` | MEDIUM |
| 8 | Drift | Task 30 acceptance, PLAN:349 | Note: `git diff -- .../archive_workspace.py` is empty compares the work tree with the index; Constraint PLAN:31 says to use the recorded base commit. | PLAN:31, 349 | LOW |
| 9 | Drift | Task 26, PLAN:306 | Note: the 15-line net growth budget across Tasks 26 and 30 is tight (about 12 or more lines needed for 5b, 6b, `q0-branch`, Q8a, the load rule, two STOP rows, the revised sentence, the flag and the Done line); both tasks fail if it cannot be met, with no fallback stated. UNVERIFIED (existing text not counted). | PLAN:306, 310, 350 | LOW |

## Adherence summary

- Prior blockers M-01 to M-11: 11 resolved, 0 open, 0 regressed (M-10 has a residual in row 4). Prior mediums M-12 to M-24: 12 resolved, 1 still present (M-20, row 2).
- New or still-open rows: 9, with 0 Blocking, 7 Medium and 2 Note. No Blocking defect found in the 38 tasks it could check.

## Notes

- UNVERIFIED: the exact FR-126 case list against Task 18's acceptance; Tasks 7, 8, 10, 11, 21 to 23, 37 line by line; whether `make verify-sync` and `make lint-architecture` pass at baseline; the +15 budget (row 9); whether tests pin the new loop line, the STOP-table sentence or the `Q8a` wording; `tests/skills/test_review_severity_rule.py` banned-wording scans against the new text.
- Verified and true: `WRITE_VERB_RE` (`test_worker_contract.py:1894`) matches `/sc:git add`, `/sc:git commit`, `gh pr`, `gh api`; Makefile lint-architecture Checks 1, 2, 3/4, 6, 8, 9; `test_task_workspace_lifecycle.py:221` pins "Join every delegated writer" which Task 32 keeps; `WORKER-CONTRACT.md:42` has "wait for issue #326 (K3)" and no test pins it, no plugin copy exists; `tests/unit/test_cli_install.py` checks only that listed files are present; no test-module basename collisions for the planned `tests/vcs` names; HOW-WE-WORK line 293 still has the old `/sc:git` row and the routing tests pass with it until Task 35.
