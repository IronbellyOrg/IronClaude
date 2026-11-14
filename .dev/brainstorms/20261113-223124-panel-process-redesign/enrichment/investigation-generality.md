# Generality of the defect classes behind the ten never-found issues

Date: 2026-11-14. Read-only investigation. Question: do the defect classes behind the ten issues that cheap reviewer panels never found recur in other plans and documents, or are they artefacts of the three evaluation packages?

Conventions
- All paths are relative to `/home/coder/workspaces/worktrees/IronClaude/eval-tasklist-review-panel/.dev/` unless absolute. `R` = `reflect/`, `D` = `tasks/done/`, `E346` = `experiments/346-validation/`, `X346` = `research/346-review-loop-experiments/`.
- The three evaluation packages are excluded everywhere: designSpec-20261107-075614, makeTheAliasOnly-20261105-051649 (and its reflect folder `pre-TASK-WF-makeTheAliasOnly-...`), design-20261108-041415 (and `R/pre-design-20261108041729`). `D/TASK-WF-designSpec-20261108-165559` (issue #441) and `R/pre-design-20261104164711` are different packages and are counted.
- Instance kinds: P = a plan or spec finding (a reviewer found the defect in text before build); I = an implementation-time finding (a blocked task, retry review or post-run audit found the defect in a delivered text or check). Only recorded findings are counted; a phrase hit with no finding behind it is not.
- Method limit: the search is phrase-based (Grep over REPORT.md, merged-*.md, reviewer cards, merged-verdict.yaml, retry reviews, notes.md, progress.md). Counts are lower bounds. The reflect reviewers were Tier-2 panels (sonnet/haiku/opus), stronger than the cheap panels, so an instance shows the class exists; it does not show cheap panels would miss it.

## 1. The ten issues abstracted into eight defect classes

Ground truth read from `eval-workspaces/tasklist-review-panel/20261111-a1/<pkg>/ground-truth.json`; the needed review move for each comes from the prior investigations in `brainstorms/20261113-223124-panel-process-redesign/enrichment/reused/` (investigation-designspec.md section 4, investigation-alias-control.md B7/B8/I6/I7).

| id | defect class (no package, task or file names) | issues covered | review move that finds it |
|---|---|---|---|
| C1 | A criterion asks for a complete or exhaustive result over a set that has no bounded method, stopping rule or scope list, or the criterion's scope differs from the scope of the instruction it checks, so every review can find one more item. | designSpec GT1, GT2 | Ask of each "every/all/found for X" criterion: what finite check proves it, and does its scope equal the instruction's scope? |
| C2 | A rule stated in the source is not carried into the plan's task text or criterion, so the artefact built from the plan breaks that rule. | designSpec GT5 | Walk the source rule by rule (and trace each failure path) against the plan. |
| C3 | A value, field or state is read, mapped or required by one component and no row, task or step writes it (or writes it for that case). | designSpec GT6 | Tabulate every value the reader keys on against the rows that write it. |
| C4 | A criterion embeds a command, pattern or test selector whose literal form cannot match (or cannot pass) the text or state the same plan orders. | designSpec GT9 | Run each criterion's literal command against the text the task tells the implementer to write. |
| C5 | After a change, a count, claim or copy in a second location is left stale because no task enumerates that location. | designSpec GT10 | Search the whole tree (root docs, changelogs, mirrors) for the claim the change falsifies. |
| C6 | A sentence the plan dictates asserts "all", "only", "never" or "outside X nothing" while the repository inventory, the plan's own other tasks or the scope of the test said to enforce it contradict it. | alias GT1, GT3 | Test each universal claim against an inventory count, the plan's later tasks and the enforcing test's scope. |
| C7 | Verbatim text the plan dictates omits a clause of a constraint the plan states elsewhere (or contradicts the plan's own criterion or constraint). | alias GT4 | Sweep each constraint, clause by clause, across every piece of dictated text. |
| C8 | A plan edits files or behaviour that a test elsewhere pins, and has no task to update or run that test. | control GT1 | Reverse-dependency sweep: for each edited file, grep the tree (especially tests) and compare with the plan's gate. |

Mapping check: 2 + 1 + 1 + 1 + 1 + 2 + 1 + 1 = 10 issues. Note on fit: C7's broad form (dictated text contradicts the plan's own constraint or criterion) is well supported below; the narrow form that alias GT4 is (one clause of a two-clause constraint dropped) has little support.

## 2. Instances in other material (per class)

Material searched: all 48 `D/` packages (progress.md ledgers for blocked/retry/halt lines, `artifacts/retries/*/review-*.md`, `notes.md`, final reviews), all 143 `R/` folders (REPORT.md, adversarial merges, reviewer cards), `E346/phase1/REPORT.md` (five recorded review-loop incidents), and `X346/p13/catalog` plus `X346/p17/ledger.json` (a validated 44-defect ledger of one spec). Ledger scan result: only 5 non-eval packages have `blocked` lines (designSpec-20261108-165559 T12, implementTheDesi-20261031 T2/T13/T15, diagnosticRefres T2, fixIronbellyOrgI T5, implementFrOnb2T T1); the richer record is the retry review files, which carry `sev=blocking` findings with a `family=` tag (24 packages have at least one).

Summary table (distinct documents other than the three eval packages):

| class | other documents with a recorded instance | of which plan/spec (P) | strength |
|---|---|---|---|
| C1 unbounded completeness | 3 (+1 borderline) | 3 | moderate; symptom-level evidence |
| C2 source rule not carried | 6 | 6 | strong |
| C3 read, never written | 3 | 3 | weak (1 blocking, 1 INFERRED, 1 LOW) |
| C4 check cannot match or pass | 9 | 8 | strong |
| C5 stale second location | 9 | 3 | strong |
| C6 overbroad claim | 12 | 4 | strong (mostly delivered docs) |
| C7 text vs plan's own constraint | 5 broad (the 5th is also the only narrow case) | 5 | broad: supported; narrow: weak |
| C8 pinned by a test nobody updates | 6 | 5 | strong |

### C1 Unbounded completeness criterion (3 documents, +1 borderline)
1. A "list every site" plan (review-severity-rule, package `D/TASK-WF-removeTheAnyIssu-20261102-053741`). Three pre-reviews each found new missed sites (11, 7, 10 blocking; never clean; cap hit). `E346/phase1/REPORT.md:124-132`: "the findings are mainly newly discovered missed sites in a 'list every site' plan". Target: plan.
2. Launch-level hook plan, issue 394. Three adversarial reviews 8 -> 8 -> 10 blocking, owner stopped the loop. `E346/phase1/REPORT.md:172-178`: B-4 "closed only for listed spellings"; the parent's words at review 2: "Each patch exposes another route". A closed list was used against an open set. Target: plan (design).
3. Worker-contract spec (the #346 spec). Ledger defect D23 (`X346/p17/ledger.json`): "The AC-C1 pattern covers only orchestration, worktree, terminal and agent, so a file running 'orca status' ... violates SA-2 yet passes" (a finite list standing for an open ban); loop symptom 24 -> 13 -> 14 findings, `E346/phase1/REPORT.md:80,82`. Target: spec.
4. Borderline: P0 live-check plan: an acceptance check that git status shows nothing outside the package, over an open set of untracked paths, so "no fix pass can make the AC true" (`R/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/adversarial/merged-verdict.yaml:21`). This is more a C4/baseline problem (see X5).
Caveat: instances 1-3 record the symptom (new items every round) and attribute it to enumeration. None quotes an AC worded like "provably complete inventory", so the exact wording defect is not independently shown.

### C2 Source rule not carried into the plan (6 documents, all P)
- `R/pre-phase3CodegraphA-20261029205359/REPORT.md:110` (M-17): "plan:37 sends G1-G4 failures to H1 and silently drops source.md:30's rule that T1-T10 may continue while G3 fails ... A G5 failure has no route."
- `R/pre-TASK-WF-scIssueClaimPipe-20261107-063237-20261107063558/REPORT.md:203-204`: "Task 6 drops the `hand_command` note that a hand-started agent is not governed by the hook (source.md:211)"; "drops 'The pending record stays' (source.md:212)".
- `R/pre-design-20261104164711/REPORT.md:215` (D-13): "Task 2 drops the clause that source section 6.5 adds to both models.py docstrings: 'plus the two conflict-cycle events sync_started and sync_concluded'".
- `R/pre-TASK-WF-fixTheScIssueWor-20261104-162205-20261104162416/REPORT.md:51` (D-M03): "the Rules bullet (plan:29) omits E-WORKER-NO-OUTPUT and the harness-note clause that source.md:1 puts in the Rules-section rule."
- `R/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329/REPORT.md:87` (D-006): "Task 8 does not carry the AC-0.6 `--source terminal` fallback into step 5".
- `R/pre-workflowSource-20261102234109/reviewer-cards/reviewer-1-card.yaml:37`: "Plan omits the Tier A/B/C grouping and template header fields ... required by the Test guide plan."

### C3 Value read, written by nothing (3 documents, weak)
- Worker-contract spec, ledger D11 (blocking): "AC-0.4 requires 7.2 step 3 (contract path and contract status) in P0, before any WC-4 contract exists" (`X346/p17/ledger.json`; same defect in the audit finding `X346/p17/findings.jsonl:20`: "The WC-4 contract ... is required by one text and built by none"; catalogue row `X346/p13/catalog/catalog.md:25`). Target: spec.
- `R/pre-TASK-WF-brainstormFixBri-20261106-113538-20261106113956/REPORT.md:106` (M-10, [INFERRED]): a clause is judged from chat text, "a checker that misses it requires a folder that was never written".
- `R/pre-task-rf-194013-20260609103200/REPORT.md:57` (S2, LOW): Step 3.2 reads `spec_path` from frontmatter; "No step writes or asserts the `spec_path` frontmatter field for the Mode-2 path".
None found: a mapping table whose input value is written by no row of a source table (the exact GT6 shape) in any other document.

### C4 Check that cannot match or pass (9 documents, 8 P)
- `R/pre-workflowSource-20261102234109/REPORT.md:51` (D-002) and `.../reviewer-cards/reviewer-1-card.yaml:13`: "Task 39 AC (grep --custom-prompt-dir returns nothing) contradicts item B-W15.3, which tells the writer to state the flag is planned, not shipped" (the GT9 shape: the check fails on the text the plan orders).
- `R/pre-refactorIronClau-20261102175540/adversarial/merged-findings.md:36`: "Plan line 19: the hit set is the output of `git grep -n -E '\.dev/worktrees|git worktree add'`, which cannot match a list-argument call."
- `R/pre-TASK-WF-writeTheP1Static-20261105-033458-20261105034258/adversarial/merged-review-card.md:99`: "The regex uses `[[:space:]]` ... Python `re` reads it as an ordinary character set, so the Orca check ... never matches and passes vacuously."
- `R/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105172548/adversarial/merged-review-card.md:17` (C-001): `cmp` of "every file under src/superclaude/commands/" includes files the installer never copies, "so the install line can never pass".
- `R/pre-implementGitHubI-20261105171020/reviewer-cards/reviewer-1-card.yaml:15`: "the sentinel never matches" (awk pattern).
- `R/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/REPORT.md:38` (M-7): "Task 1 acceptance criterion 3 is vacuous: the write-verb scan covers only skills, commands and agents".
- `E346/phase1/REPORT.md:127` (removeTheAnyIssu plan): "P2-B3 'CAP_PATTERN cannot detect 11 IN lines'".
- Worker-contract spec, `X346/p13/catalog/catalog.md:10,22` (D4 "scans core/, where P0 itself adds Orca text, so the check cannot pass"; D16 "grep cannot detect a deleted markdown bullet") and ledger D20-D22.
- I: `D/TASK-WF-scIssueClaimPipe-20261107-063237/artifacts/retries/T5/review-1.md:3` (blocking, family ac-selector): "the `-k prompt` command run as written selects only test_arg1_prompt_bad_arguments_exit_2, so PR-1 to PR-4 never run under it."
- I: `D/TASK-WF-writeTheP1Static-20261105-033458/artifacts/retries/T5/review-1.md:6` (blocking, family ac-grep-visibility): the criterion's grep cannot show the flag named in the sentence it checks; fix is to name the flag literally.

### C5 Stale count, claim or copy in a second location (9 documents, 3 P)
- P: `R/pre-TASK-WF-scIssueClaimPipe-20261107-063237-20261107063558/REPORT.md:249` (M-3): the frontmatter description and `issue.md:71`, `:100` "still say the claim then stops"; Tasks 4 and 7 leave them out.
- P: `R/pre-TASK-WF-writeTheP1Static-20261105-033458-20261105034258/adversarial/merged-review-card.md:116-118,174` and `reviewer-cards/reviewer-2-card.yaml:118-121`: plugin command copies left stale by P1; the pre-existing file count in Task 15 is off.
- P: `R/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/REPORT.md:30,39` (M-4, M-8): "The plan's search for other WC-4 copies skips the design spec the brief names"; "build.md:104 still restates parts of WC-4 after Task 3".
- I: `R/post-reuse-audit-20260607/REPORT.md:13,29`: "an incomplete `contract_version` bump that left two stale `1.2.0` references behind" (SKILL.md:1624, :1755).
- I: `R/post-perworker-models-20260609/REPORT.md:17-18`: docstring "still says per-slot model differentiation is 'intentionally out of scope' ... Now false."
- I: `R/post-pr-submit-defaults-20260616-prbranch/REPORT.md:69`: stale comment still citing the old `1800` default.
- I: `R/post-cleanup-audit-scope-defaults-20260530031952/REPORT.md:48`: task-log table says `155 -> 170`, disk is `155 -> 171`.
- I: `R/post-phase11-r16-20260602/REPORT.md:44`: `validation.md:67` "still maps spec-fidelity to SPEC_FIDELITY_GATE with stale line numbers".
- I: `D/TASK-WF-phase3CodegraphA-20261029-204913/artifacts/retries/T12/review-1.md:8` (blocking, family mirror-root-copy): root `commands/sc-*.md` copies not given the same edit.
Near-GT10 shape (a changelog line that restates a number the change alters): none found other than GT10 itself; the I-class changelog findings below are claim-vs-code mismatches (C6), not stale numbers.

### C6 Overbroad or false universal claim (12 documents, 4 P)
- P: `R/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/REPORT.md:28` (M-3): the new sentence "the report names where those files were written" "is false for workflow".
- P: `R/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/REPORT.md:307`: brainstorm text says the handoff is skipped because its skill does "not accept the flag at this phase"; "after P2 that reason is false".
- P: `R/pre-TASK-WF-brainstormFixBri-20261106-021737/reviewer-cards/reviewer-1-card.yaml:44`: Task 7 "writes only" is "false because sync-dev writes .claude/".
- P: worker-contract spec, ledger D03, D04, D28, D41 (e.g. D04 "'only changes are the small fixes' and 'every changed command' leave them unedited and in no phase, yet AC-1.1 requires their section").
- I (delivered docs, all `sev=blocking` retry reviews): `D/TASK-WF-phase1RemovalSpe-20261029-185100/artifacts/retries/T16/review-1.md:3-4` ("doc and CHANGELOG say the step prints the exact remove command for each kept entry; code prints only the kept reason"); `D/TASK-WF-removeTheAnyIssu-20261102-053741/artifacts/retries/T21/review-1.md:3` and `T16/review-1.md:4` ("`--max-convergence` can raise it" when the value never reaches the engine); `D/TASK-WF-closeIronbellyOr-20261104-124207/artifacts/retries/T4/review-1.md:6`; `D/TASK-WF-launcherFollowup-20261105-131531/artifacts/retries/T5/review-1.md:4`; `D/TASK-WF-implementTheDesi-20261031-182028/artifacts/retries/T15/review-1.md:4` and `review-2.md:6` ("After a push, one re-trigger comment per present reviewer" has no exception for a CI-fix push); `D/TASK-WF-phase2CodegraphI-20261029-192001/artifacts/retries/T11/review-1.md:3-4`; `D/TASK-WF-implementGitHubI-20261105-184607/artifacts/retries/T6/review-1.md:4`; `D/TASK-WF-designSpec-20261108-165559/artifacts/retries/T8/review-1.md:5`.
Caveat: the 8 delivered-doc cases are defects in written text, mostly changelog and user-guide sentences, not in plan wording; they show the class is common in docs, not that plans dictate such sentences as often.

### C7 Dictated text vs the plan's own constraint or criterion (5 documents broad; 1 narrow)
- `R/pre-TASK-WF-implementIronbel-20261104-130647-20261104130837/REPORT.md:48` (B-2): "Task 2's own criterion cannot be met" (requires `;` in an allowed case; the plan's allowed list has none).
- `R/pre-implementGitHubI-20261105171020/REPORT.md:67` (M-F2, blocking): "Task 1's red-run criterion contradicts its own test" (PLAN:36 vs PLAN:39).
- `R/pre-workflowSource-20261102234109/REPORT.md:51` (D-002): AC contradicts its own item.
- `R/pre-TASK-WF-p1LivePlanBrief-20261105-164506-20261105172548/adversarial/merged-review-card.md:17` (C-001): the install check "contradicts the plan's own definition of failure".
- Narrow form (text drops one clause of a stated constraint): `R/pre-TASK-WF-brainstormFixBri-20261106-021737/reviewer-cards/reviewer-2-card.yaml:10`: "Correction F-16's verifier is literally unsatisfied ... The mandated Constraints line is '... this plan does not commit.'; the plan carries 'only after they are committed'".

### C8 Plan edits what a test elsewhere pins, no task updates or runs it (6 documents, 5 P)
- `R/pre-phase3CodegraphA-20261029205359/adversarial/merged-reviewer-findings.md:22` (M-03, important): new rows "fail tests/core/test_how_we_work_routing_table.py, which asserts members == _OTHER_COMMANDS ... no task edits it."
- `R/pre-TASK-WF-implementIronbel-20261104-130647-20261104130837/REPORT.md:44-46` (B-1, blocking): "Task 3 breaks an existing test that no task runs" (`tests/hooks/test_freshness_subagent_start_policy.py:102-105`).
- `R/pre-implementTheLaun-20261107093251/REPORT.md:36-38` (D-001, HIGH): "12 tests assert `launched` ... a plan step that would break currently passing tests, with no task that migrates the fixture."
- `R/pre-refactorIronClau-20261102175540/reviewer-cards/reviewer-3-card.yaml:57-59` (R3-F4, low): "Task 6 skips the test that pins the text of the files it edits".
- `R/pre-fixGitHubIssue31-20261105031639/reviewer-cards/reviewer-3-card.yaml:48` (sequencing variant): "Tasks 1-4 change behaviour that existing tests pin and those tests are updated only in Task 5".
- I: `D/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md:17-22` (SD-2): the planned TAMPER tokens change messages that a read-only test pins, "16 failures across 4 levels"; resolved by an owner decision.
- Counter-example showing the move is cheap when the source states it: `R/pre-TASK-WF-writeTheP2Static-20261107-011441-20261107013500/REPORT.md:66` (INF-026 matched plan Task 21, "the pre-existing tests that read the edited files").

## 3. Defect classes that recur in the other material but are NOT among the ten

These show the ten are not a special set: the same material holds at least as many other recurring classes. Counts are distinct other documents.

| id | class | docs | evidence |
|---|---|---|---|
| X1 | A test or check passes on the old code or old text, so it pins nothing (non-discriminating, vacuous). | 4 | `R/pre-TASK-WF-brainstormFixBri-20261106-001016/reviewer-cards/reviewer-1-card.yaml:10` ("The new `fallback_1` assertion ... passes on the OLD text") and `reviewer-2-card.yaml:20`; `R/pre-implementGitHubI-20261105171020/REPORT.md:67` (M-F2, "red-run criterion contradicts its own test"); `R/pre-revisedPlanRefac-20261102214256/REPORT.md:123` ("A test that pins the current exit code would pass before the change too"); `R/pre-TASK-WF-writeTheP1Static-20261105-033458-20261105034258/adversarial/merged-review-card.md:99` (regex that never matches passes vacuously). |
| X2 | A cited line, symbol or premise about the repository is wrong or has aged. | 4 | `R/pre-design-20261104164711/reviewer-cards/reviewer-2-card.yaml:42` ("cites loop-guard.md:86-99 while the list ends at :103"); `R/post-reuse-audit-20260607/REPORT.md:32` (the spec cites a function pair that "does not exist in the tree"); `R/post-perPhaseturnBudget-20260619/REPORT.md:95` (residual line refs); `R/pre-sprint-cli-arch-20260603002500/REPORT.md:31` ("never set anywhere" judged IMPRECISE). |
| X3 | Two statements in the source conflict, so one requirement cannot be met as written. | 3 | `D/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md:5-15` (SD-1: FR-001 forbids what FR-020 needs); worker-contract spec ledger D34, D41, D42 (`X346/p17/ledger.json`); `R/pre-TASK-WF-orcaWorkerContra-20261103-012232-20261103055307/reviewer-cards/reviewer-1-card.yaml:54` ("The spec records D3 as option (a), so a 'P4' label would be false"). |
| X4 | Task ordering: a task needs a later task to go green, or a gate has no consumer. | 3 | `R/pre-fixGitHubIssue31-20261105031639/reviewer-cards/reviewer-3-card.yaml:48`; `R/pre-implementTheLaun-20261107093251/adversarial/merged-review.md:17` (row 2: "Task 1 gate has no consumer ... a STOP would not stop Tasks 2-22"); worker-contract spec ledger D01, D02 and `X346/p13/catalog/catalog.md:9` (D3: flag shipped before the gates it must disable). |
| X5 | A criterion depends on a baseline state the plan never captured (dirty tree, another worker's edit, untracked files). | 3 | `R/pre-TASK-WF-writeTheP0LivePl-20261103-215902-20261103220351/adversarial/merged-verdict.yaml:21`; `D/TASK-WF-diagnosticRefres-20261109-144413/progress.md:6-7` (T2.AC2 `make verify-sync` unmet because of another worker's uncommitted edit, plan forbids `make sync-dev`; owner ruling); worker-contract spec ledger D17 ("git-status check has no pre-dispatch baseline"). |
| X6 | A failure or edge path has no route or no allocation (cap never allocated, failure with no handler, empty result unspecified). | 3 | `R/pre-phase3CodegraphA-20261029205359/REPORT.md:110` ("A G5 failure has no route"); `R/pre-TASK-WF-planTheRealBound-20261107-080351-20261107080543/adversarial/merged-verdict.yaml:135` ("The cap of twelve real Claude runs is never allocated"); worker-contract spec ledger D29, D30. |
| X7 | A count-bearing criterion is broken by a step another requirement forces. | 2 (weak) | `D/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md:25` (SD-3: five-commit history check vs the owner-ordered extra commit; owner accepted the literal mismatch); `R/pre-TASK-WF-writeTheP1Static-20261105-033458-20261105034258/adversarial/merged-review-card.md:116` ("pre-existing file count is off"). |
| X8 | An acceptance criterion cannot be met because of environment flake, accepted by ruling as a carried gap. | 1 (I only) | `D/TASK-WF-fixIronbellyOrgI-20261108-110741/progress.md:12-13` (T5.AC2 unmet, parallel-run flake). Not counted as general. |

Observation: C4, C5, C6, C8 each have more distinct documents than X3, X4, X5, X6, so the ten issues were not chosen from an unusual corner of the defect space; they are among the most frequent classes in the material.

## 4. Hold-out validation material (up to six, none from the three eval packages)

Common cautions for all six: (a) remove `.dev/reflect/` (and the package's `artifacts/` and `progress.md`) from the review sandbox, as the control-package analysis required (investigation-alias-control.md line 155), or the reflect findings leak; (b) ground truth derived from reflect reports is capped at what Tier-2 reviewers found, so "never found by cheap panels" must be measured by running the cheap panels, not assumed; (c) the plan in `D/` should equal the plan reviewed: the reflect headers say the plan was not edited from these findings (H2, H4, H5), but I did not compare sha256 against the ledger `PLAN:` line (UNVERIFIED).

| # | material | recorded defects (evidence file) | classes it exercises | how to derive ground truth | work |
|---|---|---|---|---|---|
| H1 | Worker-contract spec, `X346/p17/spec-original.md` | `X346/p17/ledger.json`: 44 defects (20 blocking, 19 medium, 5 minor), each with quote, spec lines, what_goes_wrong, is_fixed_when; validated by 20 agents, Sonnet/Opus agreement 96.2% (`X346/p17/LEDGER-RESULTS.md`); blind form `X346/p17/score/ledger-blind.json` | C1, C3, C4, C6, X3, X4, X5, X6 | Already derived. Use the 20 blocking rows as GT; spot-check 5 quotes against the spec. | Low (about 1 hour). Caveat: one document, a spec not a plan package, and the whole #346 series was tuned on it, so it is a hold-out for the three eval packages but not for earlier #346 designs. |
| H2 | Plan `D/TASK-WF-implementIronbel-20261104-130647/TASK-WF-implementIronbel-20261104-130647.md` (134 lines, with `source.md`) | `R/pre-TASK-WF-implementIronbel-20261104-130647-20261104130837/REPORT.md:42-60`: 4 blocking findings B-1..B-4 with plan lines (B-1 C8: plan:73 vs the hooks test; B-2 C7: plan:58, :64), plus R1-F3..F8 | C7, C8, C4 | Each B-n already cites plan line and evidence; write a ground-truth.json item per B-n with the quoted plan lines (plan_quote) and mark blocking_in_implement from `D/.../progress.md`. | Low (4 to 8 items, about 1 hour) |
| H3 | Plan `D/TASK-WF-phase3CodegraphA-20261029-204913/` (236 lines, with `source.md`) | `R/pre-phase3CodegraphA-20261029205359/adversarial/merged-reviewer-findings.md`: 19 findings (9 important, 10 minor) with plan:line and source.md:line; includes M-03 (C8), M-17 (C2), M-06; implement-time blocking history: 22 `sev=blocking` findings in `D/.../artifacts/retries/*/review-*.md` | C2, C8, X6, C1 | Take the 9 important findings; use the implement-time blocking findings (outcome evidence) to set blocking_in_implement. Several rows are tagged `inherited-from-spec`; decide per row. | Medium (about half a day) |
| H4 | Plan `D/TASK-WF-scIssueClaimPipe-20261107-063237/` (163 lines, with `source.md`) | `R/pre-TASK-WF-scIssueClaimPipe-20261107-063237-20261107063558/REPORT.md:17,93,203-204,249`: 6 blocking (B-1..B-6) and 6 medium Drift; plan "stays as written" (`REPORT.md:17`); implement-time record in `D/.../artifacts/retries/T5/review-1.md:3` (C4) | C2, C5, C4 | One GT item per B-n and M-n using the report's plan:line and source.md:line; add the T5 `-k prompt` finding as an implementation-confirmed item. | Low to medium (12 items, 1 to 2 hours) |
| H5 | Plan `D/TASK-WF-workerContractFo-20261106-214402/` (89 lines, docs-only, with `source.md`) | `R/pre-TASK-WF-workerContractFo-20261106-214402-20261106214804/REPORT.md:18-48`: M-1..M-11 (M-3 C6, M-4 and M-8 C5, M-7 C4); advisory, plan not edited (`REPORT.md:6`); 73 citations checked, 72 founded | C4, C5, C6 | One GT item per M-n from the report; plan lines are cited as `plan :30` etc. | Low (about 1 hour); cheapest and smallest to run |
| H6 | Spec/plan `D/TASK-WF-designSpec-20261108-165559/` (issue #441; with `source.md`) | `.../artifacts/spec-deviations.md`: SD-1 (X3), SD-2 (C8-type: read-only test pins messages), SD-3 (X7); implementation code defects in `final-review.md` (FIFO open, ledger placement) are not plan defects and should be excluded | C8, X3, X7 | Three plan-level items; plan_quote from the plan's T9 (SD-2), T1/FR-001 (SD-1) and T12.AC3 (SD-3), using the lines cited in spec-deviations.md. Defects were found by building, so they are findable-by-execution, not by reviewer capability. | Low (3 items), but weak statistical power; same pipeline and period as the eval designSpec package, so style is not independent. No reflect review exists for it. |

Spares: `R/pre-TASK-WF-writeTheP1Static-20261105-033458-20261105034258` (8 blocking MF-01..08; C4 regex, C5; package `D/TASK-WF-writeTheP1Static-20261105-033458`, but "post-fix-rechecks.md" suggests the plan was changed after the review, so verify first) and `R/pre-refactorIronClau-20261102175540` (14 deviations; C4, C8; its plan is in `to-do`, not `done`, UNVERIFIED location).

Suggested set: H5 + H2 + H4 as the fast trio (about 25 items, 3 to 4 hours of ground-truth work), H3 for volume, H1 for depth on spec-type targets, H6 only as a sanity check.

## 5. Conclusion

Thresholds: general = recorded instances in at least 3 other documents; weak = 1 to 2, or 3 where most are low-grade or inferred; unsupported = none.

| class | verdict | basis |
|---|---|---|
| C2 source rule not carried | demonstrably general | 6 other plans (all P, Tier-2 findings with source.md:line vs plan:line) |
| C4 check cannot match or pass | demonstrably general | 9 other documents (8 P, incl. a regex that never matches, a grep returning nothing on the ordered text, a `-k` selector that skips tests) |
| C5 stale second location | demonstrably general | 9 other documents (3 P, 6 I) |
| C6 overbroad claim | demonstrably general | 12 other documents (4 P, 8 I; the I cases are delivered changelog and guide sentences) |
| C8 pinned by a test nobody updates | demonstrably general | 6 other documents (5 P, 1 I), incl. a HIGH and a blocking plan finding |
| C7 text vs plan's own constraint or criterion (broad) | general in the broad form | 5 other plans |
| C1 unbounded completeness criterion | supported, with a caveat | 3 other documents, but all show the symptom (new items every round, closed list against an open set); no other document records an AC worded like "provably complete" |
| C3 read but never written | weakly supported | 3 other documents: 1 blocking (spec ledger D11, an ordering variant), 1 [INFERRED], 1 LOW. The exact GT6 shape (mapping input never written by any source row) was not found elsewhere |
| C7 narrow form (one clause of a constraint dropped) | weakly supported | 1 other document (`reviewer-2-card.yaml:10` of the brainstormFixBri review) |
| any class | unsupported | none; every class has at least one other recorded instance |

What this means for a claim of broad applicability
1. Process changes aimed at C2, C4, C5, C6, C8 (and the broad form of C7) can be claimed as broadly applicable: each recurs in 5 to 12 documents the eval never used, across plans, specs, changelogs and user guides.
2. A change aimed at C1 can claim applicability to "list-every-site or closed-list-for-open-set" plans (3 documents), not to the exact "provably complete inventory" wording. A change aimed at C3 should be claimed only as plausible; test it on H1 (spec ledger D11) before claiming more.
3. The ten issues are not special: the other material contains at least eight more recurring classes (X1 to X7), several as frequent as the ten.
4. Limits of this evidence: (a) every document comes from one repository, one owner and one plan-generation pipeline (`/sc:workflow` markdown and prompt plans), so breadth across domains, authors or code-heavy plans is not shown; (b) the search was phrase-based, so counts are lower bounds and some classes (C3, C1) may be under-counted because their wording varies; (c) reflect reviewers were stronger than the cheap panels, so these records prove the class exists, not that cheap panels miss it in other documents; that needs the hold-out run in section 4; (d) the 8 delivered-document cases in C6 and the 6 in C5 are implementation-time findings in written text, not plan wording defects.
UNVERIFIED: whether each `D/` plan equals the plan reflect reviewed (no sha comparison); `X346/p11-p16` and `E346/phase2/S2-S5` specs were not read beyond the catalog, ledger and phase-1 report; `R/` folders from before 2026-10 (mms-phase-*, uc2-*, r0/r1 validations) were only phrase-searched, not read.
