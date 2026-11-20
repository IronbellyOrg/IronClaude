FINAL: pass

Package: /home/coder/workspaces/worktrees/IronClaude/claim-handoff-planb/.dev/tasks/to-do/TASK-WF-requirements-20261119-143917-2
Basis: the plan and ledger read whole; every notes, review, repair, probe and prompt file under artifacts/retries read or machine-checked; the delivery files read at the end state.
(An older file at this path, from a different package, was overwritten as instructed.)

Test runs at the end state (my own, read-only): `uv run pytest tests/issue_watch tests/issue_pipeline tests/hooks tests/skills tests/commands tests/docs -q` gave 10677 passed, 15 skipped. `uv run superclaude issue-watch run-all --help` exits 0 and `issue-watch --help` lists run-all. `make verify-sync` printed "All components in sync". `git status` shows no `.claude/` path staged or modified.

Saved prompts: all 37 files `prompt-<k>-<j>.md` under artifacts/retries/ were compared with the closed template of qa.md by script (/tmp/fr1/chk.py): every literal chunk outside the seven slots is present, in order, in every file, and line 1 is the task's start sha from the ledger. No difference, not even a blank-line one. `artifacts/superseded-prompts/` does not exist, so no README or later-prompt check applies. The ledger has no `retry ... step=revert` lines.

Constraints checked at the end state (none violated):
- Scope is IronClaude only (no Coder template change; Task 27 hands it over in docs/designs/issue-watcher-zero-setup-coder-handoff.md:10-15).
- github.py stays read-only: its only POST text is a comment (src/superclaude/cli/issue_watch/github.py:156); no mutation in any query constant (tests/issue_watch/test_security_invariants.py:946-960). The only writers are src/superclaude/cli/issue_pipeline/complete.py (POST at :387, mutation at :124) and src/superclaude/cli/issue_watch/repo_init.py (tests/issue_watch/test_security_invariants.py:1059-1076).
- Ship gate closed: src/superclaude/cli/issue_watch/launch.py:48 `GOVERNED_LEVELS_ALLOWED = False`, enforced at src/superclaude/cli/issue_watch/cycle.py:1038-1043 before `_launch`.
- Guard source and plugin mirror are byte-identical (diff clean); stamp 2 at src/superclaude/hooks/scripts/launch-level-guard.sh:10 and orca_worktree.py:865; `.config/superclaude` token at guard :777; ISSUE class at :665, :802, :815.
- Generated config starts `enabled: false` (src/superclaude/cli/issue_watch/generate.py:248). New home-writing modules take injectable base dirs (generate.Base, used by dispatch.py, first_run.py, cli.py:465-497).
- No added line in a delivery source diff says "orchestrator".

== Per-task marks ==

T1 (status allow-list): AC1 met, AC2 met, AC3 met, AC4 met.
- src/superclaude/cli/issue_watch/predicates.py:333 `ALLOWED_STATUSES = ("Research","Spec","Plan","Debug")`, :336-346 `project_check` returns project_mismatch otherwise. tests/issue_watch/test_predicates.py:488-491 (parametrized Backlog, Ready, In progress, In review, Done, None, Triage); no Backlog-passes case remains. tests/issue_watch and tests/issue_pipeline pass in the full run.

T2 (design and runbook text): AC1 met, AC2 met, AC3 met.
- docs/designs/issue-watcher.md:15 says Backlog, Ready, In progress, In review and Done never act and states the issue 331 reversal; docs/designs/issue-watcher-setup.md:189 names the four statuses. These are the only two Backlog grep hits. tests/docs pass.

T3 (Pipeline field and value times): AC1 met, AC2 met, AC3 met, AC4 met.
- artifacts/t3-single-select-value-fields.txt lists createdAt and updatedAt. src/superclaude/cli/issue_watch/github.py:99-117 (aliased status and pipeline reads), :857-870 `_project_item`, :922-932 `_single_select`; predicates.py:127-129 new fields. tests/issue_watch/test_github.py:1596 (null Pipeline parses to None) with the malformed cases in the same block; fixture tests/issue_watch/fixtures/_assumed_shape/graphql_project_items.json updated. Security scan passes.

T4 (owner observation): AC1 met, AC2 met, AC3 met.
- artifacts/t4-updatedat-observation.md: reads 0, 1c, 2 and 3b (lines 9-46), the throwaway issues named at :3-5, one outcome line at :55 "rule stands (R31 as written)". The executor changed nothing (stated at :55).

T4a (Approved issue field): AC1 met, AC2 met, AC3 met, AC4 met.
- src/superclaude/cli/issue_watch/github.py:123-146 `APPROVAL_EVENTS_QUERY`, :880-919 `_field_event` (labeled/unlabeled, bot actor_id 0, id from createdAt seconds), :1108 `approval_events`, :70-75 reread adds the pseudo label; predicates.py:22 `APPROVAL_FIELD_LABEL`, :195-218 merge and with_approval_field; cycle.py:56, :899-903, :942; reads.py:162-165. tests/issue_watch/test_github.py:1703 (event fixture), tests/issue_watch/test_cycle.py:2779 and predicates tests, tests/issue_pipeline/test_stage_status.py:113 (field nodes), tests/issue_watch/test_security_invariants.py:946-960 (APPROVAL_EVENTS_QUERY read-only).
- notes.md F1.1 and F1.2 answers all `n`: noted.

T5 (void on value change): AC1 met, AC2 met, AC3 met. Per the known fact, owner decision R36 withdraws this rule in a separate pass, so the rule being present is correct at this end state.
- src/superclaude/cli/issue_watch/predicates.py:302-329 `value_changed_after` (Status time; Pipeline time only when it has a value); cycle.py:1025-1031 (examine, after unchanged_since, before project_check), :1103-1109 (revalidate, after the approval reread, before project_check). tests/issue_watch/test_predicates.py:578 (cleared Pipeline passes at None), tests/issue_watch/test_cycle.py:2779 (raised Pipeline ends edited_after_approval).

T6 (design note): AC1 met (note 1), AC2 met, AC3 met.
- docs/designs/issue-watcher-status-pipelines.md:13-27 table has one row per Status (Research, Spec, Plan, Debug, Ready) with command, per-level behaviour, end Status and a worker column with file:line; :31-38 gives the exact prompt for each of the four Pipeline values. Decisions: :50, :55, :59, :63, :67, :71-79, :81, :85. :89-100 lists files per task by path; :102 records the ship-gate note.

T7 (per-status prompt): AC1 met, AC2 met, AC3 met, AC4 met.
- src/superclaude/cli/issue_watch/launch.py:33 `PROMPT_PATTERN`, :112 `build_claim_prompt(n, status, pipeline)`; cycle.py:1062-1119 `_revalidate` in the fixed order (approval reread, value-time rule, project_check, examined-vs-reread compare), :1163-1167 prompt built from the reread item. tests/issue_watch/test_cycle.py:2931 (revalidation_failed with no launch), :2779; test_security_invariants.py `_PROMPT_RE` written out in the test; test_cli.py status_report retry cases. Full tests/issue_watch passes.
- notes.md F1.2 `n,n,n,n`: noted. review-1 blocking F1.1 (status_report retry) was fixed and re-reviewed with a template-exact prompt-2-1; the current code passes its test.

T8 (ship gate): AC1 met, AC2 met, AC3 met, AC4 met.
- launch.py:48; cycle.py:1038-1043; audit.py:84 `"level_gated": ("skip", 0)`; tests/issue_watch/test_cycle.py:2854, :2871, :2881; tests/issue_watch/test_audit.py:84; tests/hooks/test_launch_level_observations.py:98-104 coupling test; docs/designs/issue-watcher-status-pipelines.md:102 records the line 133 / line 201 disagreement.

T9 (self-approval exclusion): AC1 met, AC2 met, AC3 met, AC4 met.
- predicates.py:230, :261 `excluded_ids`; cycle.py:69, :111, :268-273, :306, :950, :1090; cli.py:215-224 prints `warning: approver_is_launch_account`; tests/issue_watch/test_cli.py:387; test_cycle.py and test_predicates.py cases pass.
- notes.md F9.1 and F9.2 all `n`: noted.

T10 (claim surface): AC1 met, AC2 met, AC3 met, AC4 met.
- `grep -rn -- "--pipeline none" src tests docs plugins`: no remaining hit presents it as the only watcher prompt (docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md:265 shows `--pipeline <level> --stage <stage>`; docs/designs/issue-watcher-setup.md:170 says the claim runs at the issue's level). src/superclaude/skills/sc-issue-protocol/templates/launch-prompt.md:20 (only the coordinator writes), :47-51 (troubleshoot without --fix at worktree, with --fix at full), :53-54 result block last; no gh write and no issue-pipeline complete call (only a read `gh pr list` at :33). tests/commands, tests/skills, tests/hooks pass; verify-sync clean.
- notes.md records the three-line result.md amendment (docs/designs/issue-watcher-status-pipelines.md:73); it does not contradict Task 6's "outcome word, artifact paths, pull request number". The notes cite a "Review 3" that has no review-3.md in artifacts/retries/T10/ (note 2); the end state of review-2's two blocking families is correct in the current files.

T11 (coordinator duties, brief, push rule): AC1 met, AC2 met, AC3 met, AC4 met, AC5 met.
- src/superclaude/core/WORKER-CONTRACT.md:242 (repo reworded), :245 (replacement push sentence), :293-299 (duties; stage-status `--repo`; record-create only after stage-status accepts). tests/issue_pipeline/test_stage_predicates.py:281 (label-before-plan), test_approval_record.py:55 (`--plan-hash`), test_brief.py:63 (one brief per allowed Status; Debug without --fix), tests/skills/test_worker_contract.py:3407. approval_record.py and stage_predicates.py are not in the changed set.
- notes.md: minor on the Spec judgment tested as text; all `n`: noted.

T12 (complete.py): AC1 met, AC2 met, AC3 met, AC4 met.
- src/superclaude/cli/issue_pipeline/complete.py:27 (non-atomic docstring), :55-60 END_STATUS table, :342-424 (read before write, own-login marker, ALLOWED_STATUSES imported at :38, status_moved_by_person at :402-403, retry of a failed move). tests/issue_pipeline/test_complete.py (58 tests incl. status_moved_by_person and marker cases); tests/issue_watch/test_security_invariants.py:1059-1082 (NG-2 scope, argv scan).
- notes.md: extra refusal words bad_summary and bad_run; all `n`: noted.

T13 (guard): AC1 met, AC2 met, AC3 met, AC4 met.
- src/superclaude/hooks/scripts/launch-level-guard.sh:10 (stamp 2), :70-76 (SUBMIT reworded, LL-ISSUE three-part text), :455 (anchored complete pattern incl. end-of-text form; no `*issue-pipeline*complete*`), :664-665 (item-list/field-list allowed, ISSUE class), :777 (tamper token), :802, :815. tests/hooks/test_launch_level_guard.py:58, :4649-4714; tests/hooks/test_launch_level_guard_worker.py:293, :335-366 (over-match rows). CHANGELOG.md says hosts run `superclaude install --force`.
- notes.md review-1 minor and review-3 note answered `n`; review-1 F1.1 and review-2 F2.1 (design doc) were resolved per review-2 and review-3 and the doc is correct now.

T14 (complete verb): AC1 met, AC2 met, AC3 met.
- src/superclaude/cli/issue_pipeline/cli.py:223-260 (verb); WORKER-CONTRACT.md:301 (grant row, failed never moves Status, guard best effort); tests/issue_pipeline/test_complete_cli.py:38; tests/skills/test_worker_contract.py updated; verify-sync clean.

T15 (repo through reads): AC1 met, AC2 met, AC3 met, AC4 met.
- github.py takes `repo` on the argv builders (e.g. :335, :342, :345); queries use `$owner: String!, $name: String!` (:99, :123). tests/issue_watch/test_security_invariants.py:946-960 (regex `\$(\w+): String!` == [owner, name], count 2, `$after: String` nullable); tests/issue_pipeline/test_stage_status.py:30, :798; tests/issue_pipeline/test_reads.py.

T16 (repo in config): AC1 met, AC2 met, AC3 met, AC4 met, AC5 met.
- cycle.py:70 (`repo` key), :276 default; launch.py:274 `check_origin(..., repo)`; src/superclaude/cli/issue_pipeline/cli.py:391 `refused:repo-mismatch`; tests/issue_pipeline/test_stage_status.py:775-798; tests/issue_watch/test_origin_parity.py; tests/issue_watch/test_cycle.py.
- notes.md: check_origin has one call site; `n`: noted.

T17 (defaults): AC1 met, AC2 met. src/superclaude/cli/issue_watch/defaults.py; tests/issue_watch/test_defaults.py:19-111; test_module_boundaries passes. review-1 F1.1 fixed, review-2 clean.

T18 (repos): AC1 met, AC2 met. src/superclaude/cli/issue_watch/repos.py; tests/issue_watch/test_repos.py:49-208 (six repos, non-GitHub, foreign owner, failed and timed-out list raise, empty list ok); no-shell and boundary tests pass.

T19 (generate): AC1 met, AC2 met, AC3 met. src/superclaude/cli/issue_watch/generate.py:248 (`enabled: False`); tests/issue_watch/test_generate.py:87-312 (all listed cases; modes :109, launch account :172, state_dirs :251, GET :288); the security scan covers it. notes: Projects query omits `title` (all `n`, noted).

T20 (repo_init): AC1 met, AC2 met, AC3 met. src/superclaude/cli/issue_watch/repo_init.py; tests/issue_watch/test_repo_init.py:41-198; :113 and :127 (names come from defaults, no literals); the security test names repo_init.py as writer.

T21 (first run): AC1 met, AC2 met. src/superclaude/cli/issue_watch/first_run.py:163 (gate state), :188-190 (warning); tests/issue_watch/test_first_run.py:148-341 (all pass, worktree_invalid, dry-run failure, lock, restart, second run, report); no real-home write.

T22 (once prints launched and attempted): AC1 met, AC2 met, AC3 met. cli.py:141-143; cycle.py:484, :1216 (set only in the unknown branch); tests/issue_watch/test_cli.py:594; tests/issue_watch/test_cycle.py:5404; tests/issue_watch/test_no_text.py passes.

T23 (dispatcher core): AC1 met, AC2 met. src/superclaude/cli/issue_watch/dispatch.py; tests/issue_watch/test_dispatch.py:157-401 (rotation, launched stop, attempted stop, 255 s kill with and without pending entry, 270 s cap, generated first, failed orca list errors, exit codes kept). notes F1.1 to F1.3 all `n`: noted.

T24 (rate wait and pre-child checks): AC1 met, AC2 met. tests/issue_watch/test_dispatch.py:461-562 (rate_limited waits, clamped does not write, expired ignored, four distinct skip reasons, nothing created); :586 and :601 (every reason is in the documented table). notes: the F1.1 fix (SKIP_REASONS table) had no second review; it is covered by the table tests at :586-601 (note 6).

T25 (run-all): AC1 met, AC2 met, AC3 met. src/superclaude/cli/issue_watch/cli.py:432-520 (command; `--dry-run` takes no lock at :507-514; exit 75 at :513); tests/issue_watch/test_cli.py:53, :133 and the run-all cases; `run-all --help` exits 0 (my run). notes.md F1.1: no direct `run_sweep(dry_run=True)` test (note 3; answers `n`).

T26 (docs): AC1 met, AC2 met. `grep -c` of run-all, issue-watch.d, Coordinator, Pipeline, In review, level_gated and Research is at least 1 in both docs/designs/issue-watcher.md and docs/designs/issue-watcher-setup.md; docs/designs/issue-watcher.md:944 (section 19) and :991 (rollback per finding); docs/designs/issue-watcher-setup.md:710-718. tests/docs pass. notes: the docs describe R31 as built, which is true at this end state (R36 removal is a later pass).

T27 (Coder handoff): AC1 met, AC2 met, AC3 met. docs/designs/issue-watcher-zero-setup-coder-handoff.md:10-15 (R6, R9, R10, R17, R20, R21 rows; R20 open with reproduction at :14), :22-23 (PATH line, `/usr/bin/flock -n`, log path, `run-all`), :28 (gh auth result), :65 (guard version 2 and `install --force`). notes: issue numbers inferred; F1.1 wording fix had no second review (note 6); all `n`.

T28 (requirements record): AC1 met, AC2 met, AC3 met. .dev/releases/backlog/issue-watcher-zero-setup/requirements.md:23 (status vocabulary); status column: R1-R35 are built or `decided (Coder repo)` except R20 and R21 `open` (Coder rows; listed under Open decisions at :99-103 as the plan says); "Built and tested" has an entry per task (:68-96); `make verify-sync` clean. R36 `decided (not built)` is the owner's later row, outside R1-R34.

== Issues ==

None. No AC is unmet at the end state; no later change contradicts an earlier AC; no Constraints item is violated; no log cited on a latest `complete` line shows a failure at its outcome line; every notes entry has four `n` answers; no saved prompt differs from the template.

== Notes (not issues) ==
1. T6 AC1: the per-Status table in docs/designs/issue-watcher-status-pipelines.md:15-21 has no prompt column; the prompts for all four Pipeline values are in the table at :33-38 (last word swapped per stage). Reviewer F1.1 answered n,n,n,n.
2. T10: notes.md cites a "Review 3" with no review-3.md in artifacts/retries/T10/. The current files meet the AC.
3. T25: no direct `run_sweep(dry_run=True)` test over the World in test_dispatch.py (notes.md T25, open minor).
4. .dev/releases/backlog/issue-watcher-zero-setup/requirements.md R11 row text still names the label `issue-watch:approved` (superseded by the R35 row); T28 does not require rewording it.
5. docs/designs/issue-pipeline-fu1.md:9 and docs/designs/issue-watcher.md:818 describe the watcher claim as `--pipeline none`; both are historical or true while the ship gate is closed, and neither says it is the only prompt.
6. T24 F1.1 fix and T27 F1.1 fix had no second review; both are recorded in notes.md and the end state is correct.
