# Reflect REPORT — TASK-WF-scriptThe442Obse-20261108-061618 (UC-1 pre-execution)

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.61
citations_total: 39
citations_revalidated: 38
citations_dropped: 1
citations_inferred: 6
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

- Run: `.dev/reflect/pre-TASK-WF-scriptThe442Obse-20261108-061618-20261108062130/`
- Spec: `.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/source.md` (1 line, sha 2cccf326)
- Tasklist: `.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md` (266 lines, 6 phases, 11 tasks, sha 6858a121)
- Tier: 2 (rule 4: S_domains=4; parsed-sparse pre-filter forbids STOP; C=0.61)
- Reviewers: 1 = sonnet/analyzer (card C=0.75), 2 = haiku/qa (card C=0.67); merge via sc-adversarial-protocol Mode A, convergence 1.00
- Input drift: none — all 7 input-file hashes identical to the Wave-0 snapshot (tasklist and spec unchanged).

## Inferred requirements (Pass 2)

Parsed requirements: 0 (spec is one sentence). All rows below are Pass-2 inferences, quote-pinned to source.md:1, validated by the evidence-validator (each quote matches the cited line).

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | "Script the #442 observation runbook (.dev/issues/442/observation-runbook.md): setup" | source.md:1 | verified |
| INF-002 | "Orca terminal driver" | source.md:1 | verified |
| INF-003 | "evidence" | source.md:1 | verified |
| INF-004 | "cleanup" | source.md:1 | verified |
| INF-005 | "The owner has authorized an agent to start Claude sessions and run governed claims on the four disposable issues." | source.md:1 | verified |
| INF-006 | "Investigate whether the /orchestration skill (~/.claude/skills/orchestration/SKILL.md) is appropriate to use in this plan, and include it only if it fits." | source.md:1 | verified |

Union coverage 6/6 = 1.0; S_dev_density 0.0 over the union. coverage_pct (parsed-only) is null: 0 parsed requirements exist.

## Findings (merged, calibrated)

Merged verdict: **FAIL for execution-readiness** — the plan covers its spec completely (union coverage 1.0) but is not executable as written. 12 blocking + 5 minor confirmed findings; 1 dropped; full per-finding rows with corrected citations in `adversarial/merged-verdict.yaml`.

### Blocking (execution would break or is unsafe)

1. **Driver `Blocked:` baseline (R1-F01, plan:70-75; runbook:216).** `send` stops on "the screen shows a Blocked: line", but an earlier block stays visible on screen; the second send would report blocked immediately and type the next prompt mid-turn. Fix: count `Blocked:` lines before sending; only an increase is a block; self-test two blocked prompts in a row.
2. **Background-notice wait (QA-1, plan:70-75; runbook:302-324).** The driver's stop conditions (first new Stop, Blocked line, tui-idle) include no wait for background-completion notices and Claude's answer; a turn can end before its background task does. Fix: a separate bounded notice-wait per prompt that needs one; missing completion evidence leaves the item pending.
3. **Sessions A/A2 working directory (R1-F05, plan:64,96-98; runbook:163,452).** The driver's `start` takes an Orca worktree selector and passes it to `orca terminal create --worktree`; `/tmp/ob/repo-a` is a plain git repository, not an Orca worktree. As written the terminal opens elsewhere or create fails. Fix: confirm the `--help` form for a working directory (Task 3 already captures `--help` into `artifacts/t3-orca-help.txt`); state the supported form and self-test it.
4. **Permission-dialog mechanism (R1-F07, plan:63-75,81,243).** No `driver.sh` subcommand can answer a dialog, and the "only for a command the runbook prompt itself asked for" rule is unanswerable in the claim session (every dialog there is for a command the skill chose). Fix: add a `driver.sh answer <name> <key> <reason>` subcommand sharing the marker refusal and logging to the run log; define the claim-session rule explicitly.
5. **Cleanup steps 1/3/8 unspecified (R1-F02, plan:199,204-208; runbook:789-794,806,835).** Task 8 claims "steps 1 to 8" but scripts only 2, 4, 5, 6, 7. Step 3 (undo push URL and `extensions.worktreeConfig`) is the safety net when session e dies between set and restore; no task records whether the run set that key. Fix: add the three bullets plus a state key written before session e sets the flag.
6. **Store-diff placement (R1-F03, plan:263,208; runbook:796-804).** The Task 11 acceptance criterion requires the sessions-store diff before step 7 deletes `/tmp/ob`, but no script runs or prints it, and the runbook's second diff (pending, runbook:800) is absent. Fix: `cleanup.sh` runs both diffs after step 2 and again before step 7, prints the result, and refuses step 7 on any `>` line.
7. **Session b step 4 incompleteness (R1-F04, plan:141,153; runbook:635-641).** The runbook releases mid-step and runs a post-release `identify` expecting "ordinary with reason released"; the plan puts release only "at the end", so OB-CTX can never reach PASS. Fix: move the guarded release and line-638 identify into step 4 in runbook order; make release idempotent.
8. **O-10 window and cycle end (R1-F06, plan:149-150; runbook:659-665,28-30).** No observable trigger for when to fire the O-10 edit or that the pr-submit cycle has ended; the push URL guard is the only barrier to the unprotected fork master. Fix: edit fires when the PR URL appears in the governed screen or log; cycle ends on a Stop event after the final report; inline push-URL check immediately before `send`, not only in self-test.
9. **Gated-skip vs acceptance conflict (QA-3, plan:252,257,264; runbook:726).** When item 1 is not PASS the gates correctly skip sessions D/E, but Task 10's PR-URL criterion and Task 11's PR-CLOSED criterion then cannot be met, and cleanup is unreachable. Fix: make PR assertions conditional on creation; require cleanup after a gated or aborted run; add a cleanup test with issues+worktrees but no PR.
10. **Evidence classification untested (QA-4, plan:187-191).** No acceptance criterion asserts that present-but-failing evidence is classified FAIL; a script that marks every existing log PASS would pass its self-test while feeding the gates that authorize governed launches. Fix: expected-result assertions over positive, failing and incomplete synthetic evidence.
11. **Secret-scan breadth (R1-F12, raised to blocking, plan:185,74-75,259; runbook:779).** Screens capture everything the observed agent printed; the scan covers four token patterns; staging is unconditional. Fix: widen patterns (`Bearer `, `Authorization:`, `-----BEGIN`, `_TOKEN=`, `_KEY=`); Task 11 states the owner reviews ob-logs before any commit.
12. **Authorization wording (R1-F13, minor kept, plan:19,114,148-149; source.md:1).** The owner line names sessions and governed claims; creating the four issues and the PR are outward writes on the fork the line does not name in words. The source's phrasing implies they exist already. Fix: state in Constraints that creating the four issues and the one disposable PR on IronbellyOrg/IronClaude is within the authorization, or confirm with the owner before Task 10.

### Minor

- R1-F08 (plan:137,123; runbook:541,563): no task writes the `/tmp/ob/t1-local.json` backup that session b restores from, and the restore conflicts with Task 5's "never overwrites".
- R1-F09 (plan:138; orca_worktree.py:49,1031-1046,1289,1313): the governed-handle field is verifiable now (`terminal` key; recursive `handle` search); the UNVERIFIED label can be replaced.
- R1-F10 (plan:224,231; runbook:765,767-769): Task 9 cites the wrong runbook lines, its grep is vacuous today, and lines 767-769 become partly false after the scripted path lands.
- R1-F11 (plan:185,208,214): `./artifacts/` is ambiguous between the package artifacts folder and the never-staged project-root `artifacts/`; define `PKG_ART` in `lib.sh`.
- QA-2 (plan:156,159-161; runbook:720-726): stop rules gate b, d and e but not c when invoked independently; require item 5 PASS at entry to every governed subcommand.

Dropped: R1-F14 (needs-reading dependency of item 5) — the plan's own needs-reading list (plan:183) excludes item 5; the card's cited lines did not support the claim.

## Unreviewed surface (advisory)

The merge's invariant probe INV-010: the destructive cleanup paths (plan:205 `--force` heuristic, plan:199 + plan:206 `--delete-branch` ordering and PR-close step, runbook:823 `git branch -D`) were examined by neither card. Review them before any corrective execution.

Citation note: the evidence-validator dropped one citation in this section's first draft (plan:206 cited alone for `--delete-branch`; that sentence is plan:199). The citation above is the corrected form; the drop is recorded in the header (`citations_dropped: 1`) and forced `status: partial`.

## Inferred-claim audit

- `citations_inferred: 6` (the six INF rows above; each quote-pinned and validator-verified)
- Inferred-fraction: 6 / 18 = 0.33

## Recommendations

Priority order P0 first. Files: `plan` = `.dev/tasks/to-do/TASK-WF-scriptThe442Obse-20261108-061618/TASK-WF-scriptThe442Obse-20261108-061618.md`.

- R-001 (P0): driver fixes to Task 3 (`plan:70-75`): Blocked-count baseline (F01), background-notice wait (QA-1). Verifier: self-test cases for two consecutive blocked prompts and a Stop-before-notice ordering.
- R-002 (P0): session-start working directory for A/A2 (`plan:96-98`) from `orca terminal create --help` (F05). Verifier: Task 3 self-test opens a terminal whose `pwd` is `/tmp/ob/repo-a`.
- R-003 (P0): `driver.sh answer` subcommand and an explicit claim-session dialog rule (`plan:63-75,243`) (F07). Verifier: self-test shows the marker refusal shared and the answer logged.
- R-004 (P0): cleanup completeness (`plan:199-215`): steps 1/3/8 bullets, the set-flag state key, and the two store diffs run and printed by `cleanup.sh` with a step-7 refusal (F02, F03). Verifier: self-test covers an unspecified step and a `>`-line refusal.
- R-005 (P0): session b step 4 order (`plan:141,153`): mid-step guarded release plus the line-638 identify (F04). Verifier: self-test shows the post-release identify expecting "ordinary with reason released".
- R-006 (P0): session e triggers (`plan:149-150`): PR-URL-triggered O-10 edit, cycle-end condition, inline push-URL check before `send` (F06). Verifier: self-test with a scripted cycle timeline.
- R-007 (P0): gated-skip coherence (`plan:240-266`): PR assertions conditional on creation; cleanup required after gated/aborted runs (QA-3). Verifier: self-test cleanup with no PR.
- R-008 (P0): evidence classification tests (`plan:187-191`): FAIL and incomplete synthetic-evidence cases (QA-4). Verifier: self-test asserts a wrong-parent-session fixture cannot PASS.
- R-009 (P1): widen the secret scan and add the owner-review line to Task 11 (`plan:185,259`) (F12). Verifier: planted `Bearer` and `-----BEGIN` lines stop the copy.
- R-010 (P1): Constraints wording for issue/PR creation authorization (`plan:19`) (F13). Verifier: the Constraints block names issue and PR creation in words.
- R-011 (P2): the five minor findings (F08, F09, F10, F11, QA-2) as one editing pass. Verifier: self-test still prints `SELFTEST_OK`; grep proves the new Task 9 check fails before the edit.

Advisory per the workflow protocol: the plan was NOT edited from these findings.
