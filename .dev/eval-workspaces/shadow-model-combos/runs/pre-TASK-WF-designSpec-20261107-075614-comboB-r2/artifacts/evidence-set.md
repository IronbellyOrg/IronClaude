# Evidence set for the final gate: 24 of 43 citations (sampled mode)

## C1 (F1, MAJOR, blocking=True, high-stakes)
claim: Task 7 asks a static scan to pass only gh lines with --repo or repos/, but the _RESOLUTION_SCRIPTS tests need the unscoped 'gh repo view --json nameWithOwner' fallback; the fix must reuse _repo_scoped, _command_lines and _GH_CMD and relax the runtime-log clause.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=108-113

## C2 (F1, MAJOR, blocking=True, high-stakes)
claim: Task 7 asks a static scan to pass only gh lines with --repo or repos/, but the _RESOLUTION_SCRIPTS tests need the unscoped 'gh repo view --json nameWithOwner' fallback; the fix must reuse _repo_scoped, _command_lines and _GH_CMD and relax the runtime-log clause.
citation: role=test path=tests/pr_submit/test_static_grep.py lines=545-550

## C3 (F1, MAJOR, blocking=True, high-stakes)
claim: Task 7 asks a static scan to pass only gh lines with --repo or repos/, but the _RESOLUTION_SCRIPTS tests need the unscoped 'gh repo view --json nameWithOwner' fallback; the fix must reuse _repo_scoped, _command_lines and _GH_CMD and relax the runtime-log clause.
citation: role=test path=tests/pr_submit/test_static_grep.py lines=107-132

## C4 (F1, MAJOR, blocking=True, high-stakes)
claim: Task 7 asks a static scan to pass only gh lines with --repo or repos/, but the _RESOLUTION_SCRIPTS tests need the unscoped 'gh repo view --json nameWithOwner' fallback; the fix must reuse _repo_scoped, _command_lines and _GH_CMD and relax the runtime-log clause.
citation: role=spec path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md lines=377-377

## C5 (F2, MAJOR, blocking=True, high-stakes)
claim: resume_decision row 4 re-enters release_decision but has no cycle_id, applied_edits or target_sha and GuardAction has no re-enter value; the Task 4 row-4 criterion cannot be written and could release without a head proof.
citation: role=spec path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md lines=107-109

## C6 (F2, MAJOR, blocking=True, high-stakes)
claim: resume_decision row 4 re-enters release_decision but has no cycle_id, applied_edits or target_sha and GuardAction has no re-enter value; the Task 4 row-4 criterion cannot be written and could release without a head proof.
citation: role=spec path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md lines=166-166

## C7 (F2, MAJOR, blocking=True, high-stakes)
claim: resume_decision row 4 re-enters release_decision but has no cycle_id, applied_edits or target_sha and GuardAction has no re-enter value; the Task 4 row-4 criterion cannot be written and could release without a head proof.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=70-70

## C8 (F2, MAJOR, blocking=True, high-stakes)
claim: resume_decision row 4 re-enters release_decision but has no cycle_id, applied_edits or target_sha and GuardAction has no re-enter value; the Task 4 row-4 criterion cannot be written and could release without a head proof.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=77-77

## C9 (F3, MAJOR, blocking=True, high-stakes)
claim: No fold row sets cycle_id and engage row 7 NOOPs on a held guard, so a later cycle runs under the earlier id; resume row 4 can then release while the later cycle's fixes are unpushed. Adding arguments to resume_decision does not fix it.
citation: role=spec path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md lines=108-108

## C10 (F3, MAJOR, blocking=True, high-stakes)
claim: No fold row sets cycle_id and engage row 7 NOOPs on a held guard, so a later cycle runs under the earlier id; resume row 4 can then release while the later cycle's fixes are unpushed. Adding arguments to resume_decision does not fix it.
citation: role=spec path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md lines=139-139

## C11 (F3, MAJOR, blocking=True, high-stakes)
claim: No fold row sets cycle_id and engage row 7 NOOPs on a held guard, so a later cycle runs under the earlier id; resume row 4 can then release while the later cycle's fixes are unpushed. Adding arguments to resume_decision does not fix it.
citation: role=spec path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md lines=166-166

## C12 (F3, MAJOR, blocking=True, high-stakes)
claim: No fold row sets cycle_id and engage row 7 NOOPs on a held guard, so a later cycle runs under the earlier id; resume row 4 can then release while the later cycle's fixes are unpushed. Adding arguments to resume_decision does not fix it.
citation: role=spec path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md lines=190-206

## C13 (F3, MAJOR, blocking=True, high-stakes)
claim: No fold row sets cycle_id and engage row 7 NOOPs on a held guard, so a later cycle runs under the earlier id; resume row 4 can then release while the later cycle's fixes are unpushed. Adding arguments to resume_decision does not fix it.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=62-62

## C14 (F3, MAJOR, blocking=True, high-stakes)
claim: No fold row sets cycle_id and engage row 7 NOOPs on a held guard, so a later cycle runs under the earlier id; resume row 4 can then release while the later cycle's fixes are unpushed. Adding arguments to resume_decision does not fix it.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=77-77

## C15 (F4, MAJOR, blocking=False, sample-30pct)
claim: A draft_guard_unavailable halt from a failed read or timeline at engage writes no guard record, so guard_status reports released; no task owns or tests the spec's unavailable override.
citation: role=spec path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md lines=112-112

## C18 (F4, MAJOR, blocking=False, sample-30pct)
claim: A draft_guard_unavailable halt from a failed read or timeline at engage writes no guard record, so guard_status reports released; no task owns or tests the spec's unavailable override.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=124-129

## C21 (F5, MAJOR, blocking=False, sample-30pct)
claim: No criterion tests the guard-event producer payload (key format, :a<k> retry suffix, first-request-only fields); matcher fixtures and event-order checks pass with a wrong producer. Add spec 4.2 to Task 8's sources.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=124-124

## C24 (F6, MINOR, blocking=False, sample-30pct)
claim: The fold row for settled(any, skipped, user_override) does not set disabled_cause, yet guard_status keys on it; Task 3 tests only already_draft. Add a settle, fold and status test.
citation: role=spec path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md lines=206-206

## C27 (F7, MINOR, blocking=False, sample-30pct)
claim: Task 1 records the baseline before make sync-dev and Task 13 subtracts it, so a feature-caused mirror failure that is also in a stale baseline is hidden; the two separate sync tests narrow but do not close this.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=199-199

## C30 (F8, MINOR, blocking=False, sample-30pct)
claim: No task owns the mapping from the script JSON keys (isDraft, headRefOid, autoMergeRequest) to the GuardRead fields (is_draft, head_sha, auto_merge_armed), and SKILL.md may carry no new python fence.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=124-124

## C33 (F9, MINOR, blocking=False, sample-30pct)
claim: The Wave 0 bullet must name the L3 and --merge-guard off case, yet its test must fail on L3 or draft gate wording; the test must target the gate wording of the print rule, not the words themselves.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=140-140

## C36 (F10, MINOR, blocking=False, sample-30pct)
claim: Resume row 3 leaves the order of its three reasons open: a live state that mismatches the request settles not_applied without proof that no toggle landed, although the foreign-toggle slack allows one unsettled transition.
citation: role=spec path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md lines=119-124

## C39 (F11, MINOR, blocking=False, sample-30pct)
claim: Tasks 7, 8 and 12 tell the builder to classify only gh pr and gh api lines with one verb key, but WRITE_VERB_RE also hits git write verbs and keys multi-verb lines as a+b; the stale-entry test catches a miss only after a failed run.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=108-108

## C42 (F12, MINOR, blocking=False, sample-30pct)
claim: Task 10 checks the S5a and Wave 6 pre-push sentences as byte-identical using only their recorded start text, which cannot detect a later edit inside the sentence.
citation: role=plan path=.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md lines=33-33

