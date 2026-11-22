# Reflect report (UC-1, pre-execution)

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.76
citations_total: 142
citations_revalidated: 70
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 70` - size of the re-Read sample (the finding citations in full, plus a sample of the inferred-requirement rows; every inferred row was also checked verbatim by `artifacts/coverage_match.py`).
> - `citations_dropped: 1` - drops observed in the sample only.
> - The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined.

**Verdict: FAIL** (advisory). The plan `TASK-WF-specWorktreeClea-20261120-173546.md` is checked against `source.md` (the issue 687 spec). Why `status: partial`: convergence of the debate is blocked by four HIGH invariants, one grade dispute is open, and both reviewer cards were cut off by a transport limit. Reflect never edits the plan.

Run facts: Tier 2 (forced by the parse-density guard: 0 labeled requirements, 82 inferred rows); reviewers opus class (analyzer) and haiku class (qa), executor class sonnet excluded, calibrator sonnet class; Tier 1 card calibrated 0.65, reviewer cards 0.75 and 0.76; adversarial convergence 0.9231 over 13 diff points; base variant 2; codegraph index fresh (checked 2026-11-20T17:38:06Z); no verification run (UC-1).

## Coverage

- Parsed requirements: 0 (`coverage_pct` null, `coverage_undefined` false). Inferred requirements: 82. `coverage_pct_union`: 0.9024. `S_dev_density`: 0.0976.
- Unmapped by the lexical containment rule (union): INF-026, INF-028, INF-035, INF-042, INF-045, INF-048, INF-058, INF-079. The rule is lexical, so the Tier 1 calibrator also found wrong-task matches (for example INF-082, INF-002, INF-057); the matrix is a lead, not a proof.

## Findings

### Finding M-1 (BLOCKING, ground: Decision)

- **Claim:** Acceptance checks of Tasks 3, 4, 7, 11 and 12 cannot be met when their task ends, because they need fixtures or tests that later tasks create. Separately, no task owns tests for the fact-gathering code (Orca parsers, /proc scan, four-place issue collection, landed-check lookup chain).
- **Evidence:**
  - PLAN:62 "accepts the recorded shape saved under `tests/worktree_cleanup/fixtures/` by Task 7" (Task 3 needs Task 7, which comes later)
  - PLAN:73 "On a throwaway repository built by Task 7" (Task 4 needs Task 7)
  - PLAN:106 Task 7 "Depends on: Task 6" and PLAN:108 "the script's removal reports 'kept' not an error" (Task 7 own check needs the removal pipeline of Task 11 at PLAN:158; verb bodies stay stubs until Tasks 11 and 12 at PLAN:45)
  - PLAN:161 "The order of recorded commands in a test run is: archive commands, `orca terminal close`" (Task 11 check, no test exists until Task 13 at PLAN:178-188)
  - PLAN:174 "Two runs started against the same repo cannot both remove the same worktree" (Task 12 check, tested only in Task 13)
  - PLAN:99 Task 8 tests "A pure function (no process started)" with hand-built facts, so it does not exercise the collectors of Tasks 3 to 5
  - PLAN:108 and PLAN:114 Task 7 owns only test_git_facts.py (the three git facts); PLAN:74 and PLAN:86-88 (fake /proc, squash, four places, fallback) name no test module
  - Declared deferrals, not blocking: PLAN:49, PLAN:63, PLAN:76, PLAN:85 each say the assertion is made in Task 13
- **Consequence:** An executor that checks each task when it ends (the per-task model of /sc:implement, shown by the per-task Acceptance criteria and Depends on lines and by the plan own deferral wording) cannot pass these checks. It must mark them unverified or build fixtures out of order. The parsers and collectors can ship with no regression test that fails if they break.
- **Suggested fix:** Move Task 7 support work (conftest, fixtures, throwaway-repo builder, fake /proc) to just after Task 2 and split Task 7: the "removal reports kept" check moves to after Task 11. Add a test module for Tasks 3 to 5 (for example tests/worktree_cleanup/test_facts.py) that exercises the real collectors. Rewrite the checks of Tasks 2, 11 and 12 so each can be met when its task ends, or move them into Task 13. Renumber the "by Task 7" and "Task 13" references (see INV-008 below).
- **Provenance:** Variant 1 F1 (scope, six tasks, collector-test gap U-003) plus variant 2 F1 (Task 7 self-reference); debate points C-001 and X-002; verdict C-001 92 percent; both advocates agree. Declared deferrals separated from hard cases per debate A-001 QUALIFY.

### Finding M-2 (BLOCKING, ground: Missing)

- **Claim:** No task opens the pull request. The spec ends its acceptance list with the pull request step, and the plan ends at the dry run report and regression gate.
- **Evidence:**
  - source.md:276 "Finish with `/sc:pr-submit --monitor 3`"
  - source.md:379 "Pull request with `/sc:pr-submit --monitor 3`" (step 7 of the plan of work)
  - PLAN:263-274 Task 20 ends with the dry run report and the regression gate; no task names the pull request
- **Consequence:** A checkbox of the spec own acceptance list has no owning task, so a plan run to the end leaves the change without its required finish step.
- **Suggested fix:** Add the pull request step as a final handoff note for the person (not an executing task). Reason (INV-006): the plan Constraints say "no other repo is pushed to" (PLAN:24), the pull request may be opened only through /sc:pr-submit --monitor 3 against the fork, and the pull request body needs a "Generator-Constraint Considered" section if a gate or validator file is touched (UNVERIFIED whether this change touches one). A note keeps those decisions with the person.
- **Provenance:** Variant 2 F4 (headline only survived the cut; evidence taken from the spec) plus invariant INV-006 caveat; debate point C-004, 90 percent; both advocates accept.

### Finding M-3 (BLOCKING, ground: Decision)

- **Claim:** The spec section 12 table has 15 rows, not 14, and its labels are not limited to the three words the plan requires. Task 19 acceptance check uses the wrong number.
- **Evidence:**
  - PLAN:253 "one row for each of the 14 rows of the table in source section 12"
  - PLAN:256 "has 14 rows in its changed-table, each labelled with one of the three words"
  - source.md:314-328 holds 15 data rows (11 from retire.py at 314-324, branch-landed.sh at 325, lane-map.md at 326, two disk-janitor.sh rows at 327-328)
  - Labels outside "kept as is, changed or dropped": "Replaced" at source.md:321, "Reused" at source.md:325, "Not adopted" at source.md:327, "Adopted in spirit" at source.md:328
  - source.md:275 and source.md:332 require the adapted files to say what was changed
- **Consequence:** To meet "14 rows" the executor must drop one of the spec rows from the provenance record without saying so (probably branch-landed.sh), or fail the check. That weakens the Apache-2.0 "say what was changed" record the spec requires.
- **Suggested fix:** Change both numbers to 15. Either allow the spec own labels or state in the plan how each label maps to kept as is, changed or dropped.
- **Provenance:** Variant 1 F2; debate point C-005, 99 percent; variant 2 advocate had no counter.

### Finding M-4 (BLOCKING, ground: Decision)

- **Claim:** Task 1 gives the fallback of item 2 to item 1 and settles a conflict between two spec fallbacks without saying so. The "deregister from Orca" half of item 1 fallback has no verb in any task.
- **Evidence:**
  - PLAN:33 "copy the fallback of source section 11" then "items 1 and 2: remove an Orca-listed worktree with `orca worktree rm` without `--force` and read back"
  - source.md:297 item 1 fallback "Use only `git worktree remove` (its refusal is tested) and deregister from Orca if Orca still lists the worktree"
  - source.md:298 item 2 fallback "Remove through Orca for the worktrees it lists"
  - PLAN:37 items 1 and 2 are both NOT PROVEN by design, so both fallbacks apply at once and conflict
  - source.md:374 "If a proof in step 1 fails, use the fallback named in section 11 for that item; any other change goes back to Clay"
  - PLAN:158 Task 11 still runs `orca worktree rm` for Orca-listed worktrees; no task has a step that deregisters a worktree from Orca after `git worktree remove`
- **Consequence:** Correcting the text either changes the removal path Task 11 builds for Orca-listed worktrees or sends the conflict to the owner. Either way a required behaviour changes. The plan chosen path (orca worktree rm for Orca-listed worktrees) matches the spec default design, so the defect is the unflagged choice, not an unsafe path.
- **Suggested fix:** Record each item own fallback in Task 1 (item 1 per source.md:297, item 2 per source.md:298). State how the plan resolves the conflict when both stay NOT PROVEN, or send it to the owner as source.md:374 requires. Either add a deregister step and verb for the item 1 fallback or state that it does not exist and ask the owner.
- **Provenance:** Variant 1 F3 (cut off after the evidence; consequence and fix completed from the debate) plus invariant INV-002; debate point C-006, 95 percent.

### Finding M-5 (BLOCKING, ground: Decision)

- **Claim:** Spec section 11 item 3 asks for the landed check to be run on a merged and an OPEN pull request. Task 1 runs it on pull request 700 and on a number that does not exist (MERGED and NONE), so the OPEN answer is never proved. Neither card raised this.
- **Evidence:**
  - source.md:299 "run the check on a merged and an open pull request"
  - PLAN:33 "once on pull request 700 and once on a number that does not exist, to see `MERGED` and `NONE`"
  - PLAN:37 acceptance "the `MERGED` line for pull request 700 and the `NONE` line for the missing number appear verbatim"
  - PLAN:120 Task 8 does exercise an open pull request case, from fixtures
- **Consequence:** Correcting the text changes an acceptance check (OPEN in place of, or beside, NONE), so it blocks under the literal acceptance-check clause. Practical effect is small because the OPEN branch is still exercised from fixtures in Task 8.
- **Suggested fix:** Change the Task 1 proof and its acceptance check to MERGED and OPEN (a real open pull request), keeping NONE as an extra if wanted.
- **Provenance:** Debate Round 2 (round-2-advocate-1.md section 3.3; raised in Round 1 concession 5); both advocates accept; plan change 5.

### Finding M-6 (MEDIUM, ground: none)

- **Claim:** The manual archive save of tracked edits and later commits as a patch and a bundle is dropped by the plan on its own authority. GRADE UNRESOLVED (variant 2 holds BLOCKING; see unresolved_conflicts C-003).
- **Evidence:**
  - source.md:214 "`archive` by hand can still save them as a patch and a bundle"
  - PLAN:25 "It gives no step, format or folder for it, so it is not built; Task 12 records that in the verb's help text"
  - PLAN:170 help text states the patch-and-bundle save "is not built"
  - source.md:83 verb definition: archive "Runs only the evidence step of section 7 on one worktree: copy, push, check against GitHub" (no patch or bundle)
  - source.md:374 "any other change goes back to Clay" (scope: changes to the decided design and to proof fallbacks)
  - No acceptance case or build-list entry for it at source.md:246-276 or source.md:375
- **Consequence:** A capability named in the spec is not built and the owner has not approved the drop. Nothing is lost by leaving it out (a worktree with tracked edits or later commits is always kept, source.md:229 and source.md:212), and no decision or acceptance check rests on it.
- **Suggested fix:** Ask the owner whether to build a bounded patch-and-bundle save or accept the drop. Keep the help text note. Keep such worktrees during prune either way.
- **Provenance:** Variant 2 F3 regraded to MEDIUM by orchestrator tie-break (plan change 7); debate point C-003, 55 percent on grade; follow-up candidate for the owner.

### Finding M-7 (MEDIUM, ground: none)

- **Claim:** The landed-check helper writes (a git fetch, a temporary file), while Task 1 says to prove "only what needs no write", and the recording runner answers the helper from canned replies, so its safety test cannot see the helper child commands.
- **Evidence:**
  - PLAN:33 "Prove only what needs no write to a real worktree" but runs branch-landed.sh on pull request 700
  - PLAN:82 Task 5 runs branch-landed.sh from the repo main checkout and "needs `jq` and one `git fetch`"
  - LANDED:182 "git fetch --quiet origin \"$base\" \"refs/pull/$PR/head\""
  - LANDED:99 "ERRFILE=$(mktemp)" and LANDED:40 "rm -f -- \"$ERRFILE\"" (the helper own temporary file, not a file in any worktree)
  - LANDED:32-33 header "The only write is git fetch of the base branch and refs/pull/<N>/head, which touches objects and FETCH_HEAD only"
  - LANDED:107-108 and LANDED:120-128 (cited in round-2-advocate-1.md) OPEN, CLOSED and NONE exit before the fetch, so it runs only on the MERGED path
  - source.md:299 "run the check on a merged and an open pull request" and source.md:256 "changes nothing (the recorded commands contain no removal)"
  - PLAN:45 and PLAN:108 the recorder answers branch-landed.sh from canned replies
- **Consequence:** The "needs no write" sentence in Task 1 is untrue for one call, and the safety test that records every command (source.md:255) never sees the helper own child commands. No data is lost or exposed and the spec requires the call, so no named decision rests on it. A throwaway repository cannot replace the real run, because Task 1 needs the MERGED line for pull request 700 (PLAN:37).
- **Suggested fix:** Document the helper fetch in Task 1 and in the dry run report. Add a note that the recorder cannot observe the helper children and test the helper integration separately. Do not move the proof to a throwaway repository.
- **Provenance:** Variant 2 F2 regraded from BLOCKING to MEDIUM (plan change 6), evidence lines kept; debate points C-002 and X-001, 88 and 85 percent; variant 2 advocate conceded to MEDIUM in Round 2.

### Finding M-8 (BLOCKING, ground: Decision)

- **Claim:** Task 20 requires "the recorded command list in the .json output", but no task writes a command list into the JSON. Tasks 6 and 12 write the JSON of "the same rows" only.
- **Evidence:**
  - PLAN:270 "the recorded command list in the `.json` output contains no removal, no terminal close, no archive and no push"
  - PLAN:96 Task 6 "Add the table renderers (markdown and the same rows as JSON)"
  - PLAN:170 Task 12 writes "the `.json` of the same rows"
- **Consequence:** The Task 20 acceptance check cannot be met as written: the output it inspects does not exist. The executor must invent the output or fail the check.
- **Suggested fix:** Either add to Task 6 or Task 12 a step that writes the recorded command list into the JSON (or a sibling file) and a test for it, or reword the Task 20 check to read the commands from a place a task actually writes.
- **Provenance:** Invariant probe INV-001 (HIGH, verified by the orchestrator against the plan text); plan change 8. The merge executor chose the ground Missing; the orchestrator changed it to Decision (an acceptance check that cannot be met); the plan fixed only the BLOCKING severity.

### Finding M-9 (BLOCKING, ground: Safety)

- **Claim:** Task 2 builds the command runner as a denylist (it lists banned shapes), but the spec adopts an allowlist runner. Unlisted mutating commands (for example git reset, mv, find -delete) would pass the runner.
- **Evidence:**
  - PLAN:45 check_allowed "refuses before any process starts: `--force` or `-f` on `orca worktree rm` or `git worktree remove`, `git branch -D`, `rm`, `git worktree prune`, `git push` with a delete flag ..." (banned shapes only)
  - source.md:323 "Adopted: the script runs commands only through one runner with an allowlist, and a test records every command (section 9)"
  - PLAN:19 safety constraint: no task removes, moves or clears any real worktree or file
- **Consequence:** The runner is the safety boundary of the whole script. A denylist lets any mutating command that nobody thought to ban run, which breaks the safety boundary the spec adopted and the plan own constraint relies on.
- **Suggested fix:** Rewrite Task 2 so the runner holds a positive list of allowed command shapes (read verbs of git, gh and orca, plus the named write verbs of the pipeline) and refuses everything else, and keep the banned shapes as extra refusals. Add a test that an unlisted command such as git reset is refused.
- **Provenance:** Invariant probe INV-003 (HIGH, verified by the orchestrator); plan change 8. The grade ground (Safety) was chosen by the merge executor; the plan fixed only the BLOCKING severity.

### Finding INV-004 (MEDIUM, ground: none)

- **Claim:** Task 1 marks item 7 NOT PROVEN with a write-based reason although item 7 is read-only, and marks item 4 PROVEN by "write the definition" while the spec says to test with a fake /proc.
- **Evidence:**
  - PLAN:33 "Mark items 1, 2, 5, 6, 7, 8 and 10 NOT PROVEN, because proving them needs a real Orca removal, a real push, an automation or a terminal close"
  - source.md:303 item 7 is proved by "Compare with `gh` on every worktree Orca lists" (read-only)
  - PLAN:33 item 4 "write the definition" against source.md:300 "Test with a fake `/proc`"
- **Consequence:** The proofs record gives an untrue reason for item 7 and weaker proof than the spec for item 4. Nothing named rests on it (item 7 is never used as authority at source.md:303).
- **Suggested fix:** Prove item 7 read-only against gh, or give its real reason; record item 4 as proved only once the fake /proc test exists.
- **Provenance:** Invariant probe INV-004 (probe severity HIGH; placed in the MEDIUM and NOTE bucket by refactor-plan.md change 9, so graded MEDIUM here).

### Finding INV-005 (MEDIUM, ground: none)

- **Claim:** Tasks 14 and 16 may fail an existing test because the plan never mentions the WRITE_VERB_CLASSIFICATION table that classifies every git or gh write verb in command files.
- **Evidence:**
  - WCTEST:1893-1896 WRITE_VERB_RE matches `git push`, `git worktree remove`, `gh pr` and similar on any line under the audit roots
  - WCTEST:1950-1957 _check_all_classified fails on "unclassified git/gh write-verb hits"
  - (dropped by the evidence gate: 1)
- **Consequence:** Task 16 acceptance check "uv run pytest tests/skills/test_worker_contract.py -v passes" (PLAN:221) can fail on unclassified hits from the new command file.
- **Suggested fix:** Add to Task 14 or Task 16 a step to classify any new hit in WRITE_VERB_CLASSIFICATION, or word the command file so it has no matching line.
- **Provenance:** Invariant probe INV-005 (MEDIUM, re-checked by the orchestrator against WCTEST:1893-1957).

### Finding INV-007 (MEDIUM, ground: none)

- **Claim:** The .dev save-state window is not fully covered: Task 6 shows removable at save state needed while rule 5 allows .dev files only at verified; the order of save and decision under --apply is unstated; no test adds a new ignored .dev file between save and removal.
- **Evidence:**
  - PLAN:96 "`.dev` files allowed only when the save state is `verified`" and the dry run "shows `removable` with the saved-copy cell `needed`"
  - PLAN:158 Task 11 re-reads the untracked and ignored lists after the terminal close (so a check exists)
  - PLAN:182 Task 13 and source.md:248 test a new commit, a tracked edit and an untracked file outside .dev, not a new ignored .dev file
- **Consequence:** Coverage gap and unstated order only, not a missing check (the orchestrator refinement of the probe). A change in the .dev window could pass untested.
- **Suggested fix:** State the order of save and decision under --apply in Task 6 or Task 11, and add a test for a new ignored file under .dev appearing between the save and the removal.
- **Provenance:** Invariant probe INV-007 as refined by the orchestrator (MEDIUM).

### Finding INV-008 (MEDIUM, ground: none)

- **Claim:** Moving Task 7 after Task 2 (the fix for M-1) is not a plain reorder: Task 7 must be split, the check_allowed registration arrives in Task 11, and "by Task 7" and "Task 13" references need renumbering.
- **Evidence:**
  - PLAN:108 Task 7 "removal reports 'kept'" check needs Task 11 (PLAN:158)
  - PLAN:45 and PLAN:158 the registration of saved paths with the Runner is added in Task 11
  - PLAN:62, PLAN:73 ("by Task 7"); PLAN:49, PLAN:63, PLAN:76, PLAN:85 ("Task 13"); PLAN:143 "Depends on: Task 9, Task 7"; PLAN:180 "Depends on: Task 12, Task 8"; PLAN:259 "Task 2" pointer
- **Consequence:** An executor that applies the M-1 fix as a simple move breaks dependency lines and cross-references.
- **Suggested fix:** Apply the M-1 fix as a split and renumber every cross-reference listed above in one pass.
- **Provenance:** Invariant probe INV-008 (ADDRESSED partial, MEDIUM).

### Finding INV-009 (NOTE, ground: none)

- **Claim:** Task 20 lists only Tasks 12 and 19 as dependencies, but its criteria record the full suite, lint and sync results, so Tasks 13 and 15 to 18 are missing from its dependencies.
- **Evidence:**
  - PLAN:265 "Depends on: Task 12, Task 19"
  - PLAN:274 the report records "the full test suite (`uv run pytest`), `make lint`, `make verify-sync`, and a scan of every new file for em and en dashes"
- **Consequence:** A dependency line is incomplete. The task order already puts Task 20 last, so no outcome changes.
- **Suggested fix:** Add Tasks 13 and 15 to 18 to the Task 20 dependency line.
- **Provenance:** Invariant probe INV-009 (LOW), listed as a note by plan change 9.

## Unresolved conflicts

- C-003: Grade of the dropped patch-and-bundle save for manual archive (finding M-6). Variant 2: BLOCKING: source.md:214 says archive by hand "can still save them as a patch and a bundle", the plan drops it on its own authority, and source.md:374 sends any other change back to the owner. Variant 1 and the calibrator: MEDIUM: it is an aside in "What is not saved" with no step, format, folder or test case, the verb definition at source.md:83 omits it, and the plan discloses the drop at PLAN:25 and PLAN:170. Used: Orchestrator tie-break to MEDIUM, as written in refactor-plan.md change 7. The finding stays listed as UNRESOLVED and as a follow-up candidate for the owner.

## Checked and found sound

- Dry run safety wording: PLAN:19 bans removal, moving, clearing, terminal close, automation and push to the evidence repo, not a fetch; source.md:256 defines "changes nothing" as no removal in the recorded commands. The helper fetch is therefore MEDIUM (M-7), not a safety break.
- The helper temporary file and rm -f (LANDED:99, LANDED:40) concern its own mktemp file, not a file in any worktree, and PLAN:21 scopes "never rm" to the script itself.
- The plan removal path for Orca-listed worktrees (PLAN:158) is the spec default design; M-4 is about the unflagged fallback choice, not an unsafe path.
- Patch-and-bundle drop is disclosed in the plan (PLAN:25, PLAN:170) and does not lose data (tracked edits and later commits keep the worktree), so it is not a safety finding.
- Rejected claim, variant 1 F1 wording that Task 2 cannot pass: overstated, since most Task 2 checks pass when it ends; only the refusal assertion at PLAN:49 looks ahead, and that is a declared deferral.
- Rejected attribution, variant 1 citing PLAN:99 as an ordering defect of Task 8: that line belongs to Task 6 and describes a pure function with hand-built facts; used only for the collector-test gap in M-1.
- Rejected grade, variant 2 F2 as BLOCKING: the spec requires the helper call (source.md:299) and defines "changes nothing" as no removal (source.md:256).
- Rejected figure, variant 2 self-reported confidence 0.95: two of its four BLOCKING grades (F2, F3) did not hold under the grade rule.
- Truncation of both cards is a transport limit, not evidence of a plan defect; the FAIL verdict does not depend on the cut-off text, because M-1, M-2, M-3, M-4, M-5, M-8 and M-9 each block on their own.

## Coverage gaps

- Both input cards were cut off by the transport: variant 2 after the start of F4 ("The plan ends with recording"), variant 1 after the evidence of F3 ("source.md:374 says"). The consequence and fix of variant 1 F3 and the evidence of variant 2 F4 were completed from the spec and the debate, not from the cards.
- No coverage matrix: neither visible card covers C-007 (spec section to task coverage), so unreviewed spec sections are not shown clean.
- Tasks 9, 10, 14 to 19 were reviewed by neither card in the visible text; they appear here only through INV-005, INV-008 and INV-009.
- UNVERIFIED: a plain git fetch origin <branch> may also update the remote-tracking ref refs/remotes/origin/<branch> (round-2-advocate-1.md); it changes no grade.
- UNVERIFIED: whether this change touches a gate or validator file, which decides whether the pull request body needs a "Generator-Constraint Considered" section (M-2).
- The /sc:implement protocol file was not opened by the advocates; the per-task checking model is taken from the plan own Acceptance criteria and Depends on lines and from the skill description.
- Advocate 2 wrote no report files; its positions come from the returned summaries recorded in debate-transcript.md.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | It never uses `--force` on a worktree removal, never `git branch -D`, never `rm`, never pushes to a source repo and never deletes a remote branch. | source.md:16 | Task 11 (containment 0.769) |
| INF-002 | Its only push goes to the evidence repo. | source.md:16 | Task 1 (containment 0.75) |
| INF-003 | Tracked edits and commits made after the pull request always keep the worktree. | source.md:16 | Task 8 (containment 0.8) |
| INF-004 | Dry run is the default for every verb that could remove something; `--apply` is the only way to remove. | source.md:78 | Task 2 (containment 0.8) |
| INF-005 | Prints a table of every git worktree of every repo of ours, one decision (keep or removable) and one reason per row. | source.md:82 | Task 6 (containment 0.833) |
| INF-006 | Runs only the evidence step of section 7 on one worktree: copy, push, check against GitHub. | source.md:83 | Task 9 (containment 0.909) |
| INF-007 | Removes one worktree whose work is safe, run from outside it, usually right after its pull request merges. | source.md:84 | Task 15 (containment 0.615) |
| INF-008 | Runs the same decision on all worktrees and removes the removable ones. | source.md:85 | Task 12 (containment 1.0) |
| INF-009 | One row per worktree: repo, folder, branch, in Orca (yes or no), pull request and state, issue(s) and state, idle days, size, saved copy (none needed, saved and checked, or failed), decision and reason. | source.md:87 | Task 6 (containment 0.87) |
| INF-010 | Each step fails closed: if any step cannot be completed or read back, the worktree is kept and the reason is shown. | source.md:89 | Task 11 (containment 0.727) |
| INF-011 | Without a `VERIFIED` result the worktree is kept and nothing below happens. | source.md:91 | Task 13 (containment 0.625) |
| INF-012 | An `unverifiable` or failed close keeps the worktree. | source.md:92 | Task 11 (containment 1.0) |
| INF-013 | Any change since the save and any process still inside the worktree keeps it. | source.md:93 | Task 11 (containment 1.0) |
| INF-014 | Never a path that is not in the manifest, never `-d` on a folder as a whole, never a tracked file (decision 2). | source.md:94 | Task 11 (containment 0.778) |
| INF-015 | For a worktree Orca lists: `orca worktree rm --worktree id:<id>` without `--force`. | source.md:95 | Task 11 (containment 1.0) |
| INF-016 | For a worktree Orca does not list (the 13 removable ones today): `git worktree remove <path>` without `--force`. | source.md:95 | Task 13 (containment 0.833) |
| INF-017 | **Remove the local branch with `git branch -d`, never `-D`.** | source.md:96 | Task 2 (containment 1.0) |
| INF-018 | Confirm the folder is gone, `git worktree list` no longer shows it and `orca worktree list` no longer shows it. | source.md:97 | Task 11 (containment 0.778) |
| INF-019 | In a dry run (no `--apply`) steps 1 to 7 are not run | source.md:99 | Task 11 (containment 1.0) |
| INF-020 | a repo whose `origin` belongs to IronbellyOrg or IronbellyGroup, found from `orca repo list` plus `git worktree list` in each repo (so worktrees Orca does not list are covered), wherever they sit | source.md:102 | Task 4 (containment 0.824) |
| INF-021 | As a second guard the script skips any worktree whose folder name starts with `orca-port-`, `orca-recipe-` or `orca-pristine-`, or is `orca-old-patched`, even if git lists it. | source.md:105 | Task 2 (containment 0.778) |
| INF-022 | One Orca automation per Coder workspace, once a day at 2:00 AM Central (08:00 UTC), switched on by that workspace's owner. | source.md:112 | Task 18 (containment 0.733) |
| INF-023 | The name must not start with `coordinator-`. | source.md:112 | Task 18 (containment 1.0) |
| INF-024 | The cron string is `0 8 * * *` (UTC). | source.md:116 | Task 18 (containment 0.6) |
| INF-025 | Python standard library only, no model call anywhere. | source.md:124 | Task 2 (containment 0.667) |
| INF-026 | It is a command, not a skill: a skill installs for everyone and would break the opt-in schedule. | source.md:125 | none (0.375) |
| INF-027 | The automation definition, written and switched off, modelled on `scripts/merged_pr_log_orca_automation.md`. | source.md:126 | Task 18 (containment 1.0) |
| INF-028 | a precheck command that exits non-zero makes Orca skip the run and start no agent session. | source.md:131 | none (0.417) |
| INF-029 | Name: `worktree-cleanup-daily`. Trigger: `0 8 * * *` (UTC; 2:00 AM Central in winter, decision 11). Status: written, not switched on. | source.md:137 | Task 18 (containment 0.944) |
| INF-030 | `GH_TOKEN` (never read from a file by the script; it is passed to `gh` and to `git push` through the environment). | source.md:144 | Task 13 (containment 1.0) |
| INF-031 | One lock file per repo in the output folder, so two runs cannot remove the same worktree twice; a second run after a removal finds nothing more to do. | source.md:146 | Task 12 (containment 0.944) |
| INF-032 | Each run writes `<out dir>/prune-<UTC timestamp>.md` (the table) and a `.json` of the same rows | source.md:148 | Task 12 (containment 1.0) |
| INF-033 | Exit codes follow Jay's: 0 means the run completed (some worktrees may be kept; read the table), 64 means a usage error or a `retire` of a worktree that is not removable, 69 means a lookup or a removal failed (the table still shows what happened). | source.md:148 | Task 12 (containment 0.821) |
| INF-034 | No output names an agent or a model. | source.md:148 | Task 12 (containment 1.0) |
| INF-035 | Clay switches it on in his workspace and for the first week it only writes the table (no `--apply`) | source.md:150 | none (0.556) |
| INF-036 | A worktree is removed only when ALL eight rules hold. | source.md:154 | Task 6 (containment 0.667) |
| INF-037 | Every rule fails closed: if the script cannot tell, it keeps the worktree. | source.md:154 | Task 1 (containment 0.889) |
| INF-038 | It is a linked worktree of one of our repos that this run may touch. | source.md:158 | Task 12 (containment 0.667) |
| INF-039 | Its own pull request is MERGED. | source.md:159 | Task 5 (containment 1.0) |
| INF-040 | Nothing was added after the pull request. | source.md:160 | Task 9 (containment 0.8) |
| INF-041 | The issue it was for is CLOSED. | source.md:161 | Task 6 (containment 1.0) |
| INF-042 | Nothing unsaved is in it. | source.md:162 | none (0.5) |
| INF-043 | Nothing but its own Orca terminals is using it. | source.md:163 | Task 13 (containment 0.6) |
| INF-044 | It has been idle for at least 7 days and was not created in the last 7 days. | source.md:164 | Task 8 (containment 1.0) |
| INF-045 | It is not pinned and nobody asked to keep it. | source.md:165 | none (0.5) |
| INF-046 | Decision 1 allows `git clean -f -x` for the exact paths saved and verified in the evidence repo and for nothing else | source.md:170 | Task 11 (containment 0.867) |
| INF-047 | Close an Orca terminal of a worktree that has not passed every other rule and whose save is not verified. | source.md:171 | Task 11 (containment 0.909) |
| INF-048 | Run `git worktree prune`, because a missing folder can mean a disk is not mounted (Jay's guard); it reports such a worktree and leaves it. | source.md:173 | none (0.562) |
| INF-049 | Create, move or change a file inside a worktree it keeps (the archive step reads and copies; it never edits). | source.md:175 | Task 11 (containment 0.75) |
| INF-050 | Read a credential from a file, print a credential, or name an agent or a model in any output. | source.md:176 | Task 12 (containment 0.75) |
| INF-051 | Needs the merged pull request of rule 2. Without one it refuses (nothing is saved for unmerged work). | source.md:186 | Task 9 (containment 0.833) |
| INF-052 | Pack the ignored files under `.dev/` (not `__pycache__`) into `ignored.tar.gz`, split into parts of 85 MB when larger | source.md:188 | Task 9 (containment 0.929) |
| INF-053 | Write `saved-paths.txt`, one exact path per line | source.md:188 | Task 9 (containment 0.857) |
| INF-054 | Write `MANIFEST.md`: source repo, branch, pull request link and title, merge date, worktree head and pull request head, worktree folder, time saved, count of files, and a SHA-256 of each archive file and of `saved-paths.txt`. | source.md:188 | Task 9 (containment 0.96) |
| INF-055 | Commit in the evidence repo with the message `archive(<repo>): <date> pr<N> <subject>`. | source.md:189 | Task 9 (containment 0.889) |
| INF-056 | If the push is refused, repeat from the fetch up to 3 times | source.md:190 | Task 9 (containment 1.0) |
| INF-057 | Print `VERIFIED <folder> files=<n>`. | source.md:191 | Task 6 (containment 0.8) |
| INF-058 | It never overwrites a folder. | source.md:192 | none (0.5) |
| INF-059 | `<source-repo>/<pr-author>/<YYYY-MM-DD>_pr<number>_<subject>/`. | source.md:194 | Task 9 (containment 1.0) |
| INF-060 | after the save is pushed and verified against GitHub, do whatever is needed to make the worktree removable, for the saved untracked and ignored files only. | source.md:212 | Task 6 (containment 0.667) |
| INF-061 | YES: a names-only secret check before pushing. | source.md:235 | Task 9 (containment 0.667) |
| INF-062 | They never touch a real worktree. Each case must fail if its rule is removed. | source.md:244 | Task 8 (containment 0.625) |
| INF-063 | Decision 3: a worktree that passes every rule and has Orca terminals open and a process inside is removed in `--apply` only after `orca terminal close --worktree id:<id> --all` is confirmed | source.md:249 | Task 13 (containment 1.0) |
| INF-064 | A squash-merged pull request whose commits are not on the base is judged landed from pull request state, not ancestry. | source.md:251 | Task 5 (containment 0.909) |
| INF-065 | A pull request that is merged but whose branch was later reused for new commits keeps the worktree. | source.md:252 | Task 8 (containment 1.0) |
| INF-066 | A test records every command the script runs, in every verb and every branch | source.md:255 | Task 2 (containment 1.0) |
| INF-067 | A second run after a removal finds nothing more to do; two runs at once do not both remove the same worktree (one lock per repo). | source.md:257 | Task 12 (containment 0.933) |
| INF-068 | No output names an agent or a model (a test greps the table, the summary and the log). | source.md:259 | Task 13 (containment 1.0) |
| INF-069 | An ignored archive larger than 85 MB is split into parts that join back to the same bytes. | source.md:264 | Task 9 (containment 1.0) |
| INF-070 | Two clones pushing different folders at the same time both end up on `origin/main` after the rebase and retry. | source.md:266 | Task 10 (containment 1.0) |
| INF-071 | Decision 1: exactly the paths in `saved-paths.txt` are cleared (including a name with a space) and nothing else | source.md:268 | Task 13 (containment 0.917) |
| INF-072 | Decision 2: a merged worktree with a tracked edit or a commit after the pull request is kept, nothing is cleared, no terminal is closed and nothing is archived by `prune`. | source.md:269 | Task 11 (containment 0.941) |
| INF-073 | `git worktree remove` without force refuses a worktree with an untracked file and one with a modified tracked file, and removes one that holds only ignored files | source.md:271 | Task 7 (containment 1.0) |
| INF-074 | A dry run in Clay's workspace prints a table whose counts match `git worktree list` | source.md:274 | Task 20 (containment 0.846) |
| INF-075 | Jay's files that are adapted keep his Apache-2.0 notice and say what was changed | source.md:275 | Task 19 (containment 0.769) |
| INF-076 | The regression gate passes: the full test suite, `make lint` and the sync checks that `/sc:pr-submit` runs. | source.md:276 | Task 20 (containment 0.643) |
| INF-077 | No em or en dashes in new files. | source.md:276 | Task 17 (containment 0.8) |
| INF-078 | on throwaway worktrees only, and write the findings to `.dev/research/worktree-cleanup-proofs.md`. | source.md:373 | Task 1 (containment 0.7) |
| INF-079 | registered where the repo lists commands. Reuse the landed check of #668. | source.md:375 | none (0.556) |
| INF-080 | A provenance block with Jay's Apache-2.0 notice at the top of the script. | source.md:376 | Task 2 (containment 1.0) |
| INF-081 | **Retire the manual tool** in the evidence repo (its `tools/archive-workspace.sh` becomes a pointer to the script) | source.md:377 | Task 19 (containment 0.667) |
| INF-082 | **Pull request** with `/sc:pr-submit --monitor 3`. | source.md:379 | Task 1 (containment 0.714) |

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 142` = 0.00

## Recommendations

### Recommendation R-001: Move Task 7 support work (conftest, fixtures, throwaway-repo builder, fake /proc) to just after Task 2 and spl

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md), Tasks 2 to 13
- **Change:** Move Task 7 support work (conftest, fixtures, throwaway-repo builder, fake /proc) to just after Task 2 and split Task 7: the "removal reports kept" check moves to after Task 11. Add a test module for Tasks 3 to 5 (for example tests/worktree_cleanup/test_facts.py) that exercises the real collectors. Rewrite the checks of Tasks 2, 11 and 12 so each can be met when its task ends, or move them into Task 13. Renumber the "by Task 7" and "Task 13" references (see INV-008 below).
- **Verifier:** Re-read every acceptance bullet of Tasks 2 to 13: none may name a file or test that a later task creates; the mechanical gate still passes.
- **Linked finding:** M-1
- **Priority:** P0

### Recommendation R-002: Add the pull request step as a final handoff note for the person (not an executing task)

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md), last task or a closing note
- **Change:** Add the pull request step as a final handoff note for the person (not an executing task). Reason (INV-006): the plan Constraints say "no other repo is pushed to" (PLAN:24), the pull request may be opened only through /sc:pr-submit --monitor 3 against the fork, and the pull request body needs a "Generator-Constraint Considered" section if a gate or validator file is touched (UNVERIFIED whether this change touches one). A note keeps those decisions with the person.
- **Verifier:** Read the plan end: either a task or an explicit note names `/sc:pr-submit --monitor 3` as the finish, matching source.md lines 276 and 379.
- **Linked finding:** M-2
- **Priority:** P0

### Recommendation R-003: Change both numbers to 15

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md), Task 19
- **Change:** Change both numbers to 15. Either allow the spec own labels or state in the plan how each label maps to kept as is, changed or dropped.
- **Verifier:** Count the rows of source.md section 12 (lines 314 to 328) and compare with the number written in Task 19.
- **Linked finding:** M-3
- **Priority:** P0

### Recommendation R-004: Record each item own fallback in Task 1 (item 1 per source

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md), Task 1 and Task 11
- **Change:** Record each item own fallback in Task 1 (item 1 per source.md:297, item 2 per source.md:298). State how the plan resolves the conflict when both stay NOT PROVEN, or send it to the owner as source.md:374 requires. Either add a deregister step and verb for the item 1 fallback or state that it does not exist and ask the owner.
- **Verifier:** Read Task 1: item 1 carries its own spec fallback (source.md:297) and Task 11 has a step for deregistering from Orca.
- **Linked finding:** M-4
- **Priority:** P0

### Recommendation R-005: Change the Task 1 proof and its acceptance check to MERGED and OPEN (a real open pull request), keeping NONE a

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md), Task 1
- **Change:** Change the Task 1 proof and its acceptance check to MERGED and OPEN (a real open pull request), keeping NONE as an extra if wanted.
- **Verifier:** Task 1 asks for the `OPEN` token on an open pull request (source.md:299) as well as `MERGED`.
- **Linked finding:** M-5
- **Priority:** P0

### Recommendation R-006: Either add to Task 6 or Task 12 a step that writes the recorded command list into the JSON (or a sibling file)

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md), Task 6, Task 12 and Task 20
- **Change:** Either add to Task 6 or Task 12 a step that writes the recorded command list into the JSON (or a sibling file) and a test for it, or reword the Task 20 check to read the commands from a place a task actually writes.
- **Verifier:** A task writes the recorded command list into the JSON (or a sibling file) and Task 20 reads it from there.
- **Linked finding:** M-8
- **Priority:** P0

### Recommendation R-007: Rewrite Task 2 so the runner holds a positive list of allowed command shapes (read verbs of git, gh and orca, 

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md), Task 2
- **Change:** Rewrite Task 2 so the runner holds a positive list of allowed command shapes (read verbs of git, gh and orca, plus the named write verbs of the pipeline) and refuses everything else, and keep the banned shapes as extra refusals. Add a test that an unlisted command such as git reset is refused.
- **Verifier:** Task 2 holds a positive list of allowed command shapes and a test that `git reset` is refused.
- **Linked finding:** M-9
- **Priority:** P0

### Recommendation R-008: Ask the owner whether to build a bounded patch-and-bundle save or accept the drop

- **File:** source.md lines 83 and 214 (owner decision)
- **Change:** Ask the owner whether to build a bounded patch-and-bundle save or accept the drop. Keep the help text note. Keep such worktrees during prune either way.
- **Verifier:** The owner states whether a patch-and-bundle save of tracked edits is in version 1; the plan then matches.
- **Linked finding:** M-6
- **Priority:** P1

### Recommendation R-009: Document the helper fetch in Task 1 and in the dry run report

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md), Task 1 and Task 13
- **Change:** Document the helper fetch in Task 1 and in the dry run report. Add a note that the recorder cannot observe the helper children and test the helper integration separately. Do not move the proof to a throwaway repository.
- **Verifier:** Task 1 states that `branch-landed.sh` fetches; Task 13 tests the helper integration apart from canned replies.
- **Linked finding:** M-7
- **Priority:** P1

### Recommendation R-010: Prove item 7 read-only against gh, or give its real reason; record item 4 as proved only once the fake /proc t

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md)
- **Change:** Prove item 7 read-only against gh, or give its real reason; record item 4 as proved only once the fake /proc test exists.
- **Verifier:** Re-read the cited lines after the change and confirm the finding no longer applies.
- **Linked finding:** INV-004
- **Priority:** P1

### Recommendation R-011: Add to Task 14 or Task 16 a step to classify any new hit in WRITE_VERB_CLASSIFICATION, or word the command fil

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md)
- **Change:** Add to Task 14 or Task 16 a step to classify any new hit in WRITE_VERB_CLASSIFICATION, or word the command file so it has no matching line.
- **Verifier:** Re-read the cited lines after the change and confirm the finding no longer applies.
- **Linked finding:** INV-005
- **Priority:** P1

### Recommendation R-012: State the order of save and decision under --apply in Task 6 or Task 11, and add a test for a new ignored file

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md)
- **Change:** State the order of save and decision under --apply in Task 6 or Task 11, and add a test for a new ignored file under .dev appearing between the save and the removal.
- **Verifier:** Re-read the cited lines after the change and confirm the finding no longer applies.
- **Linked finding:** INV-007
- **Priority:** P1

### Recommendation R-013: Apply the M-1 fix as a split and renumber every cross-reference listed above in one pass

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md)
- **Change:** Apply the M-1 fix as a split and renumber every cross-reference listed above in one pass.
- **Verifier:** Re-read the cited lines after the change and confirm the finding no longer applies.
- **Linked finding:** INV-008
- **Priority:** P1

### Recommendation R-014: Add Tasks 13 and 15 to 18 to the Task 20 dependency line

- **File:** the plan file in the workflow package (TASK-WF-specWorktreeClea-20261120-173546.md)
- **Change:** Add Tasks 13 and 15 to 18 to the Task 20 dependency line.
- **Verifier:** Re-read the cited lines after the change and confirm the finding no longer applies.
- **Linked finding:** INV-009
- **Priority:** P2

