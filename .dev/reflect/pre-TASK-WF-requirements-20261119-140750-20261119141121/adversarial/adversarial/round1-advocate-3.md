# Round 1: Advocate for Variant 3 (reviewer-3 card, refactorer, opus)

Plan under review: `.dev/tasks/to-do/TASK-WF-requirements-20261119-140750/TASK-WF-requirements-20261119-140750.md` (`plan:N`). Severity rule used: Blocking only for Decision, Missing or Safety; otherwise Medium or Note. Every file:line below was read in this round.

<!-- sections appended below -->

## 1. Steelman of the other cards

**Card 1 (analyzer).** Its best finding is M-3 (C-009). `check-config` (`src/superclaude/cli/issue_watch/cli.py:185-198`) is offline. `self.account_id` is set only during a live cycle from `gh api user` (`cycle.py:767`), so the warning Task 9 asks for has no input unless the code reads `config.owner_account_id`, which is optional (`cycle.py:768`). That is a real wiring gap in a decided owner behaviour (warn-only self-approval), and card 1 grades it more correctly than my card did (I had it as a Note). Its M-1 (C-008) and M-2 (C-007) are also sound. Task 5 needs "the one live item" before the Task 7 helper exists. `status_report` rebuilds the retry prompt from `build_claim_prompt(n)` alone (`cycle.py:1313`), with no stored Status or Pipeline. Its N-1 is better than it looks: the guard test also asserts `len(set(GRID_CLASSES)) == 16` (`tests/hooks/test_launch_level_guard.py:3391`), so adding `ISSUE` breaks a third pin that the plan never names.

**Card 2 (qa).** Its strongest point is QA-1 (C-005). Task 27 (`plan:356`) is the only carrier of R6 and R9 into the Coder repo, and its content list has no lifecycle rules: install cron, start it on every boot from `startup.sh`, keep exactly one entry (`source.md:36`); check coordinator parts at boot and on every watcher run, and restart a stopped session (`source.md:40`). QA-2 (C-003) is also a sharp catch. `record_create` (`src/superclaude/cli/issue_pipeline/approval_record.py:313-359`) takes a plan hash, channel, evidence id and actor, and nothing in it tells a claim-time event from a plan-stage one. So the Task 11 test "a claim-time event is refused as plan approval" (`plan:176`) cannot be written against that module as it stands.

## 2. Strengths of card 3, and critique of cards 1 and 2

Card 3's strengths:
- Only card 3 traced the coordinator's approval read end to end (C-001 / U-001). Cards 1 and 2 read the cycle path, where Task 16 threads `cfg.repo`. They did not read the `stage-status` path, which Task 15 deliberately leaves on the `REPO` default (`plan:227`).
- Only card 3 put Task 3's parse rules and Task 5's void rule side by side (C-002 / U-002). Under the closed ship gate this edge decides whether the one live level works at all.
- Card 3 alone checked the Task 6 decision on which session runs the command (`plan:102`) against the Task 11 brief acceptance (`plan:177`) (C-006). It also alone found the same-file ordering gaps (C-010), the `pr-submit`/GHWRITE conflict (C-011) and the false Goal sentence (C-012).
- Card 3 gives every Blocking item its category and the affected action, which the merge needs for grading (S-002).

Critique point by point:
- **C-001, C-002:** cards 1 and 2 both say "not found". Card 1 states that its `github.py` cites match and that the `cycle.py` ordering holds, but it never opened `issue_pipeline/cli.py:279` or `reads.py:142,148`. Its "No Blocking finding" verdict is therefore unsupported.
- **C-003 (card 2):** the finding is true but overstated. An enforcement point does exist, just not in `approval_record.py`. `stage_predicates._label_channel` accepts only a label applied after the plan reply and otherwise returns `label-before-plan` (`src/superclaude/cli/issue_pipeline/stage_predicates.py:161-170`). A claim-time label always comes before the plan reply. The defect is that Task 11 places the test in `test_approval_record.py`, which has no such rule. That is Medium, not Blocking.
- **C-004 (card 2, QA-3):** the reading is too literal. The coordinator-only case matches on the whole command text `$T` (guard:444). A real command that runs `p.complete.run()` must import the module first, for example `python -c "from superclaude.cli import issue_pipeline as p; p.complete.run()"`. That text contains `issue_pipeline` and `complete.run`, so it matches `*issue_pipeline*complete.run*`. The real Task 13 conflict is the one card 3 found (M-4): the hyphen pattern refuses `plan-hash` with a path containing "completed", which `plan:207` requires to stay allowed. Card 1's M-5 (git, sed and ruff on the pattern's files are refused) is a valid addition.
- **C-005 (card 2):** true, but Medium rather than Blocking. Acceptance `plan:361` already requires each of R6 and R9 to be listed "with ... the value or text the template must use". The owner's R9 decisions are also already posted on Coder issue 516 (`source.md:40`). So the deliverable is under-specified, not absent.
- **C-007 (card 1 M-2):** I agree; card 3 has the same finding as M-2.
- **C-009:** card 1 is right to call it Medium, and I withdraw card 3's Note grade.
- **C-013 (card 1 M-4):** true but Low. The Pipeline value is known only after `project_items` (`cycle.py:957`), the last read in `_examine`, so the gate cannot be applied before the reads without reordering them. This is a Note.
- **C-014 (card 2 QA-4):** true, and card 3 missed it. Task 24 says "exactly one (Task 19 rule)" (`plan:323`), but Task 19 allows several Projects when a defaults-map entry exists (`plan:268`). A repo generated through the map would then be skipped on every sweep.
- **Card 2, "same-file order sound" (C-010):** wrong. `plan:30` lists `WORKER-CONTRACT.md` only for Tasks 11 and 14, but Task 10 edits it too (`plan:161`). Tasks 2 and 10 both edit `docs/designs/issue-watcher.md` and `issue-watcher-setup.md` with no dependency edge between them (`plan:48`, `:50`, `:159`, `:161`).
- **Card 2 S-002:** card 2 labels items Blocking while its own severity column says Medium, so its verdict cannot be used without re-grading.

## 3. Shared assumptions

| ID | Answer | Reason | Conf. |
|---|---|---|---|
| A-001 | QUALIFY | Every line I re-read holds: `cycle.py:949-961, 1007-1016, 1054-1058`, `predicates.py:257-271`, `github.py:37, 74, 88-103, 764-775`, guard `:10, :70-71, :444, :652-654, :764, :786, :798`, `issue_pipeline/cli.py:279, :347`, `reads.py:142, :148`, `WORKER-CONTRACT.md:242, 245, 293, 298, 300`. One semantic cite is wrong: `plan:84` says "one-second resolution, line 257", but `unchanged_since` compares raw datetimes (`predicates.py:257`). In practice `parse_utc` only accepts whole seconds (`predicates.py:24`), so the outcome is the same. | 0.85 |
| A-002 | QUALIFY | Task 4 tells the executor to ask the owner in chat and wait (`plan:73`). That is consistent with the owner's chat-approval rule, but it stalls an unattended `/sc:implement` run. The plan should mark Task 4 as a planned halt. I did not read the `/sc:implement` interrupt list this round. | 0.6 |
| A-003 | ACCEPT | Stated by the plan itself (`plan:24`: "a script or another HTTP client is not seen"). | 0.95 |
| A-004 | ACCEPT | `plan:25` names the `--pipeline none` claim session as ungoverned. | 0.9 |
| A-005 | ACCEPT | All tests use faked runners (`plan:22`). The only repo-threading test is Task 16's, for the cycle (`plan:241`), and no task tests `stage-status` or `reads.py` with a second repo. C-001 would therefore ship green. | 0.9 |

## 4. C-001 to C-014 against the real files

**C-001: cross-repo approval read. TRUE. Blocking (Safety).** Confidence 0.8.
- `_stage_status` calls `gh.reread(runner, budget, issue, _timeout)` with no repo (`issue_pipeline/cli.py:279`) and `reads.read_stage_evidence` (`:282`). That function calls `gh.events` and `gh.edits` with no repo (`reads.py:142, :148`), and builds comments through `_argv_rest_page` (`reads.py:67`).
- All of these use `REPO = "IronbellyOrg/IronClaude"` (`github.py:37`) or the literal `repository(owner: "IronbellyOrg", name: "IronClaude")` in `EDITS_QUERY` (`github.py:75`).
- Task 15 keeps `REPO` as the default "so reads.py and its tests keep working unchanged" (`plan:227`). Task 16 threads `cfg.repo` only through the cycle (`plan:238`).
- `stage-status` takes no `--repo`. Its `--config` defaults to the IronClaude file (`cli.py:347`), while Task 19 writes per-repo configs to `issue-watch.d/<name>.json` (`plan:268`).
- The coordinator duty is "read GitHub through `stage-status` at each gate" (`WORKER-CONTRACT.md:298`), and Task 23 serves every allowed-owner repo (`plan:313`). This path is live with the gate closed, because level None starts plan workers (`WORKER-CONTRACT.md:293-298`).

Failure modes, from `stage_predicates.evaluate` (`stage_predicates.py:262-279`):
- **Usual case, fails closed.** IronClaude#N has no plan reply from the host login, so the result is `no-plan-reply` and repo X's issue can never be approved. That alone breaks a required behaviour.
- **Fail-open case.** If the coordinator omits `--plan-dir` (the duty at `:298` does not require it), `plan_hash_now` is taken from IronClaude#N's own latest plan reply (`cli.py:293-294`), so `changed` is False. An approver's label on IronClaude#N applied after that reply then reports X#N as `approved` (`:279`). Issue numbers collide across repos, and the host login is shared (`plan:110`).

A wrong approval decision on a gate the plan keeps as the control (`plan:26`) is a safety boundary. `WORKER-CONTRACT.md:242` ("Every such action targets `IronbellyOrg/IronClaude`") also contradicts `complete --repo` for other repos, and no task edits that line. My one qualification: the fail-open path needs an issue-number collision plus a plan reply and a label on the IronClaude issue, so it is narrow. The fail-closed outcome alone still meets the Decision rule.

**C-002: empty Pipeline against the unreadable-time rule. TRUE, as an undefined required behaviour. Blocking (Decision).** Confidence 0.65.
- `PROJECT_ITEMS_QUERY` reads `fieldValueByName` per field (`github.py:95-97`), and `_project_item` maps a null value to None (`github.py:770-774`). For an empty Pipeline the field object is null, so `pipeline_changed_at` is None as well as the name.
- Task 3 routes a malformed time to `non_json`/`unreadable` at parse level, before any predicate runs (`plan:65`). So the only way Task 5's predicate can ever see an "unreadable time" (`plan:84`) is a None time, which is exactly the empty-Pipeline case.
- "The later of the Status value time and the Pipeline value time" (`plan:84`) is undefined when one of them is None. The acceptance list (`plan:87-88`) has no empty-Pipeline case.
- An empty Pipeline is a decided launch path ("None or empty = `--pipeline none`", `plan:95`; "an empty Pipeline means None", `source.md:51`). Under the closed gate (`plan:27`) None is the only level that launches.

A literal implementation therefore refuses every empty-Pipeline issue with `edited_after_approval`. I qualify the confidence because a careful implementer might still tell "absent" from "unreadable". The fix is three test rows plus one sentence.

**C-003: claim-time event refused as plan approval. TRUE in part. Medium.** Confidence 0.65.
- `record_create` (`approval_record.py:313-359`) has no claim-versus-plan discriminator, so a test at `plan:176` in `test_approval_record.py` has nothing to assert against.
- The behaviour itself is enforced elsewhere: `_label_channel` accepts only `labeled` after the plan reply (`stage_predicates.py:161-170`).
- The fix is to point the test at `stage_predicates.evaluate`, or add a store check. This does not change a decision.

**C-004: Task 13 guard pattern. TRUE as a cluster. Medium.** Confidence 0.75.
- M-4 (card 3) is true: `superclaude issue-pipeline plan-hash <dir>/completed/...` matches `*issue-pipeline*complete*` and would be refused, but `plan:207` requires it to stay allowed. Only the anchored option at `plan:202` can pass.
- M-5 (card 1) is true: `git add docs/designs/issue-pipeline-fu1.md && git commit -m "... complete ..."`, and any command naming `issue_pipeline/complete.py`, become TAMPER.
- N-4 (card 3) is true: the H3 case runs on any word whose basename is `gh` (guard:626). The plan intends this (`plan:202`), but does not list it as an accepted over-match.
- N-1 (card 1) is true, and wider than it says: `GRID_CLASSES` (test:775), the import-time assert (test:843) and `len(set(GRID_CLASSES)) == 16` (test:3391) all need changing.
- QA-3 (card 2) is mostly false (see section 2).

It is not Blocking, because the plan calls the pattern best effort and not a control (`plan:202`), and the acceptance list decides the anchor.

**C-005: Task 27 lacks R6 and R9 lifecycle content. TRUE. Medium.** Confidence 0.65. The content list at `plan:356` has no boot or daemon rules and no restart-a-stopped-session rule (`source.md:36, :40`). It is not Missing: acceptance `plan:361` already requires an R6 and R9 row with the text the template must use, and the owner's decisions are on Coder issue 516.

**C-006: Task 11 brief test at the wrong levels. TRUE. Blocking (Decision).** Confidence 0.6.
- Task 6 records the decision: the brief is used only at `none`, and at the other levels the launched agent runs the command from its prompt (`plan:102`).
- Task 11's acceptance tests brief rows for `/sc:troubleshoot` at Worktree, Full and Full Submit and has no None row (`plan:177`).
- Today the brief is a plan-writing template whose rows "stop before /sc:implement and /task" (`worker-brief.txt:5`).
- Debug at None (troubleshoot with or without `--fix`, which means code edits before plan approval) is the live path under the closed gate, and it is untested.

The acceptance check contradicts a decision the plan names, so this meets the Decision rule. I concede the merge could reasonably grade it Medium, because a test could be written for rows that are never used.

**C-007: `status` retry has no stored Status or Pipeline. TRUE. Medium.** Confidence 0.85. `status_report` reads `dispatch.json` only (`cycle.py:1279-1281`) and calls `build_claim_prompt(n)` (`cycle.py:1313`). The `plan:131` check ("valid for each Status") can be met by a valid but wrong command, so it is weak rather than impossible.

**C-008: Task 5 needs the live item; the helper arrives in Task 7. TRUE. Medium.** Confidence 0.8. The predicate at `plan:84` needs one item's times. The helper is added at `plan:123`, which runs after Task 5 (`plan:121`). In `_examine` the items are read at `cycle.py:957`.

**C-009: `self.account_id` cited for an offline check. TRUE. Medium** (I withdraw card 3's Note). Confidence 0.85. Evidence: `cli.py:185-198`, `cycle.py:767-768`.

**C-010: same-file edits not ordered. TRUE. Medium.** Confidence 0.85. Evidence: `plan:30` against `plan:48`, `:50`, `:159` and `:161`.

**C-011: `/sc:pr-submit --monitor 3` against the GHWRITE refusal at Full Submit. TRUE but partly pre-existing and uncertain. Medium.** Confidence 0.55.
- GHWRITE is denied at FS today (guard:798), and `graphql` is never a safe read (guard:579).
- The `gh api` writes of pr-submit live inside scripts (`review-retrigger.md:14`, `reply-resolve-thread.sh:73, :131, :141`). Because the guard checks command text only (`plan:24`), it may never see them.
- So card 3 overstated certainty. The real point is that the plan drops a residual risk the remediation had recorded. It is not new breakage.

**C-012: Goal sentence "can never write ... at any level". TRUE. Note** (downgraded from card 3's Medium). Confidence 0.6. `plan:15` contradicts `plan:24-25`, but the Constraints govern and no task follows the Goal sentence. Fix the wording only.

**C-013: gated issues re-examined every cycle. TRUE, inferred. Note.** Confidence 0.6. The Pipeline is known only after the last read (`cycle.py:957`). Against the 35-call cap (`github.py:46-49`) this costs budget, but it fails closed.

**C-014: Task 24 against Task 19 on the Project count, and the missing acceptance case. TRUE. Medium.** Confidence 0.75. R14 says "report ... several Projects" (`source.md:34`). Task 19 allows several with a map entry (`plan:268`). Task 24 requires exactly one and cites Task 19 for it (`plan:323`). This fails closed (the repo is skipped), and the R14 checks are missing from the acceptance at `plan:328`.

### Contradiction rulings
- **X-001 (Q-1):** FIXED, with Medium residues under C-004. Card 2's PARTIAL rests on the mis-read in QA-3. Confidence 0.7.
- **X-002 (Q-6):** I concede it is FIXED. `MARKER_JQ` flags a comment only if its body contains `CLAIM_MARKER` (`github.py:61-63`), and `plan:191` already tests that the result marker does not contain the claim marker. That is enough to prove `marker_comments` ignores a result comment. Card 3's PARTIAL drops to a Note. Confidence 0.75.
- **X-003 (Q-10):** PARTIAL, confirmed by C-010. Confidence 0.85.

## 5. Net position

- **Blocking:** C-001 (Safety, 0.8), C-002 (Decision, 0.65), C-006 (Decision, 0.6).
- **Medium:** C-003, C-004, C-005, C-007, C-008, C-009, C-010, C-011, C-014.
- **Note:** C-012, C-013.
- **Concessions:** C-009's grade goes to card 1. C-014 is card 2's find, missed by card 3. Q-6 is FIXED. C-011's certainty is lowered. C-012 is downgraded.
