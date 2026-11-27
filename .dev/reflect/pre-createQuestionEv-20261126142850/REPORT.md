# Reflection report: second pre-execution audit of the regenerated issue 834 plan (UC-1)

```yaml
contract_version: 1.9.0
status: partial                        # one sub-citation dropped by the evidence validator; adversarial merge unavailable (fallback)
mode: pre
tier_reached: 2
confidence_calibrated: 0.64            # Tier 1 card; reviewer cards 0.75 (reviewer 1) and 0.86 (reviewer 2)
citations_total: 142
citations_revalidated: 142
citations_dropped: 1
citations_inferred: 4
citation_budget_policy: full_reread
merge_method: single-reviewer-fallback
adversarial_unavailable: true
coverage_degraded: null
```

Short paths: PLAN = `.dev/tasks/to-do/TASK-WF-createQuestionEv-20261126-142533/TASK-WF-createQuestionEv-20261126-142533.md`; SPEC = the `source.md` beside it.

## Loud notice: the adversarial merge did not complete

The Wave 4 adversarial merge was started for the two reviewer cards. Its orchestrator stopped after spawning the round 1 advocates (the session paused for about two hours); no merged card, debate transcript or return contract was written, only `adversarial/diff-analysis.md` and header stubs. This is the protocol's fallback path F2: the result below is the highest-calibrated single reviewer card (reviewer 2, qa, opus class, calibrated C 0.86), unmerged. `merge_method: single-reviewer-fallback`, `adversarial_unavailable: true`, `status: partial`. The reviewer 1 card (analyzer, haiku class, calibrated 0.75) is not part of this result; its three findings overlap reviewer 2's rows 13 (secret-scan scope), 14 (criterion 6 refresh) and add one point reviewer 2 lacks (R-006: the `kept without approval:` output line is not named in the run checks). Those are recorded as follow-ups, not graded here.

- finding_counts: blocking 4, label_high 4, medium 12, note 6 (the reviewer's own grades by the review severity rule; label_high counts the reviewer's HIGH labels, rows 1 to 4)
- Why Tier 2: S_scope 11 tasks (above 10), at least 3 domains (code, tests, docs, infra paths), and calibrated C 0.64 (below 0.85). Parsed coverage 24 of 24, union 0.8421, `S_dev_density` 0.1579, no `coverage_degraded`.
- Executor class: the orchestrating session (claude-gw-tier1b, the `sonnet` alias class) was excluded from the reviewer pool; the calibrator class is also sonnet, so executor and calibrator are not separated.

## Blocking findings

### Deviation B-1 (Blocking, Safety, open: unverified): the Task 4 dry run happens before any write block exists

- **Location:** PLAN:104 (Task 4), PLAN:114, 116-120 (Task 5)
- **Evidence:** the only model run the plan prescribes before write blocking exists is Task 4's "dry print-mode run" (PLAN:104, excerpt saved at PLAN:109). Neither names a prompt or an environment (validator check 4 confirms). The fake `gh`, the isolated home and the blocked remote are built in Task 5, which depends on Task 4 (PLAN:114-120). If the dry run uses the real home it loads the installed skill, whose rule is the old one (`~/.claude/skills/sc-issue-protocol/refs/create.md:84`), and calls the real authenticated `gh`, so it can file a live issue on the fork, which R-003 and R-012 forbid (SPEC:55, 64). PLAN:22 is a general ban, not a mechanical control for this step.
- **Fix (plan text):** in Task 4, name the dry run's environment and prompt: run it in an isolated home and configuration directory outside the package with `GH_TOKEN`, `GITHUB_TOKEN` and `SSH_AUTH_SOCK` unset, `gh` shadowed by a stub that exits non-zero, the remote push URL invalid, and a probe prompt that makes one question tool call and never invokes `/sc:issue`.
- **Verifier:** Task 4's file records the dry run's command line, its environment and the shadowed `gh`.
- **Not verified:** whether the permission settings would have stopped a real `gh` call anyway.

### Deviation B-2 (Blocking, Decision): the criterion 4 empty-diff check compares with a moving integration tip

- **Location:** PLAN:205, PLAN:212 (Task 9)
- **Evidence:** `git diff origin/integration -- <the three files>` compares the working tree with the integration tip; SPEC:37 says the tip has advanced past 862384852. A later integration commit that touches `SKILL.md`, `refs/claim.md` or `templates/launch-prompt.md` makes the diff non-empty although this work never touched them, so the Task 9 acceptance check "AC4 shows the empty diff" fails or is misreported. The plan used the merge-base form for R-023 (PLAN:234, three-dot) but not here; prohibition 12 (SPEC:80) forbids the working-tree-against-tip comparison.
- **Fix (plan text):** in Task 9 replace the diff with `git diff origin/integration...HEAD -- <the three files>` plus `git diff HEAD -- <the three files>`, and say that the check passes when both are empty.
- **Verifier:** PLAN:205 names both commands.
- **Not verified:** whether integration has advanced over those three files (no fetch was made).

### Deviation B-3 (Blocking, Decision): the preserved-flag test cannot pass as the plan states it

- **Location:** PLAN:76 against PLAN:80-81, acceptance at PLAN:86 (Task 3)
- **Evidence:** the counting rule counts a Contradictions item when its second part is "the user's own words in quotes or the flag as passed" (PLAN:76, validator check 1). The scenario at PLAN:81 says a worker's disagreement with a supplied flag, written "as a Contradictions line without the user's quoted words", gives zero questions. A natural flag-disagreement line carries the flag as passed, so by PLAN:76 it is complete and gives one question, and the zero assertion fails; if the flag is dropped too, it is just the incomplete-line case of PLAN:80. Either way the shipped exception ("a worker's disagreement with a user-supplied flag is not a contradiction when the issue is filed with the user's flag", `templates/draft-notes.md:13`, `refs/create.md:38,86`) is never modelled, so R-001's preserved-flag scenario is not exercised at notes level (SPEC:53).
- **Fix (plan text):** in Task 3 replace the preserved-flag fixtures with two cases that the rule does decide: a worker's disagreement recorded under New material (zero questions), and a Contradictions item of category changed flag that states the flag as passed and that the drafted issue uses a different value (one question); keep the assertion that the Wave 2 sentence exists and that the Wave 5 step 7 pushback still posts a disagreement.
- **Verifier:** Task 3's test ids include one for each of the two cases, and the zero-question case passes with the flag named in the New material line.

### Deviation B-4 (Blocking, Decision): the hold on staging raw run output appears only in Tasks 9 and 11

- **Location:** Constraints PLAN:17-27; Tasks 4 to 8; hold only at PLAN:191 and PLAN:234
- **Evidence:** R-013 requires every run output to be scanned before `git add .dev/tasks` (SPEC:65). The standing rule stages `.dev/tasks` including every package's `artifacts/` (CLAUDE.md:37). The plan states the hold ("before anything in ./artifacts/ is staged") only in Task 9 and as a note in Task 11; the Constraints (PLAN:27 only bars `.claude/` and `.dev/issues/`) and Tasks 4 to 8, which create the dry-run excerpt, the self-test output and the raw event logs, carry none (validator check 3 confirms). An executor following the standing rule stages raw logs before any scan.
- **Fix (plan text):** add a Constraints bullet and a line in Tasks 4, 5, 6, 7 and 8: raw event logs, dry-run excerpts and any other raw run output are written to a scratch folder that is not under `.dev/tasks` (Task 4 names it), scanned by Task 9, and only scanned files are copied into `./artifacts/`; no plan text says "never stage `.dev/tasks`".
- **Verifier:** the Constraints and each of Tasks 4 to 8 name the scratch folder; Task 9 copies from it after a clean scan.

## Medium findings (recorded; the surgical repair leaves them alone)

- M-05 PLAN:118,120,145,150: the before-answer body is not captured, and the body comparison passes when the draft never named the false file; save the draft body when the question appears and the posted body at create time.
- M-06 PLAN:150,195,205,212: R-005's "not evidenced" and R-015's four verdict words are never reconciled; state it.
- M-07 PLAN:160,161,177: no expected `issue comment` count for `standard-contradiction`, `standard-multi-contradiction` and `deep-contradiction` (R-004 says "otherwise recorded as observed"; the validator notes the row paraphrase overstates R-004).
- M-08 PLAN:156,175: Tasks 7 and 8 depend only on Task 5; make 7 depend on 6 and 8 on 7, or state that runs go one at a time.
- M-09 PLAN:98,102: the load list omits the analyze command file and the adversarial skill that deep runs need.
- M-10 PLAN:22,97-102: no model login is established for an isolated home (an unverified premise; the model gateway variables may be inherited).
- M-11 PLAN:23,100,151: no rule attributes fork changes to a run, so another session's activity can stop the matrix.
- M-12 PLAN:120,129,149: skill and worker loads may be visible by name rather than path in the event log; Task 4 should check what the log shows.
- M-13 PLAN:191: the secret scan covers only `./artifacts/runs/`, not the feasibility file, the self-test output or the planted-token folder (also raised by reviewer 1, graded Blocking (Missing) there).
- M-14 PLAN:234,239: criterion 6 is refreshed from `gates.md` only; the pull request half is not (also raised by reviewer 1).
- M-15 PLAN:56,69,76,82: the notes-contract tests link to the rule text only by two phrases and a line format they invent.
- M-16 PLAN:100,127-128: Wave 0 reads the fetch URL (`scripts/origin_repo.py:160`) and stops with `E-NO-ORIGIN` for a non-GitHub origin; a clone of the local worktree has a local-path origin.

## Notes

N-17 PLAN:142-143 quick runs expect 0 comments (supported by create.md:98). N-18 PLAN:23 adds a stop condition for a run that read an installed copy (enforces R-010). N-19 PLAN:234 present-tense "the issue is closed" mirrors R-021. N-20 PLAN:205 omits `refs/claim.md:80` and `SKILL.md:86` from the AC4 reading list. N-21 PLAN:39,41,46 the builder has no template argument for the drift guards. N-22 PLAN:129 the self-test check against the installed copy depends on machine state.

## Evidence validator result

142 citations re-read; every row of the table survives. One dropped sub-citation: `plan:22` in the card's coverage-audit mapping of INF-001/002/003 (secondary; it belongs at plan:20 for the secret-exception row). Unmarked inferences kept with their citations: M-10 ("an isolated home holds no Claude login"), M-11 ("other sessions are active on the fork"), the planted-token folder location. Unverified items the reviewer listed: that the six quoted criteria match the live issue body word for word, whether `origin/integration` has commits touching the three criterion 4 files, and how the event log records skill and agent loads.

## Degraded components and honest limits

`graph:truncated` and `graph:unlisted` (Grep, Glob and Read were the evidence floor); the adversarial merge was unavailable (fallback F2); the Tier 1 card was written by the orchestrator (`hypothesis_source: inline-fallback`); the executor class equals the calibrator class; the reviewer outputs were not isolated from the live tree (read-only agent type); the memory file under `docs/memory/reflect/` was not written (out of scope for this branch).

## Recommendations

### Recommendation R-001: Repair the four blocking findings on a copy of the plan
- **File:** the plan package TASK-WF-createQuestionEv-20261126-142533 (Tasks 3, 4, 5, 6 to 9 and the Constraints)
- **Change:** apply the fixes of B-1 to B-4 above with `/sc:workflow --revise <package> --review <this report> --remediate surgical` (surgical route, at most 2 fix cycles, changed-lines re-review).
- **Verifier:** the re-review reports each of B-1 to B-4 resolved.
- **Linked deviation(s):** B-1, B-2, B-3, B-4. **Priority:** P0

### Recommendation R-002: Carry the medium findings as follow-up candidates
- **File:** the pull request body and `./artifacts/pr-notes.md`
- **Change:** list M-05 to M-16 with their fixes; apply any that the surgical repair touches anyway.
- **Verifier:** the pull request body names each M-id and its status.
- **Linked deviation(s):** M-05 to M-16. **Priority:** P1
