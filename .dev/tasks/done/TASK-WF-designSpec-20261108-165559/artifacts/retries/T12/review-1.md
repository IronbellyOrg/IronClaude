# Review 1: T12 (start acb70ba1d033199da22be7d9eeeffabeac8d5799)

The independent reviewer returned this review in chat because their instructions prohibit report-file writes. The executor transcribed the review below without changing its findings.

## Earlier blocking findings

None supplied.

## AC marks

- T12.AC1 met. Both absent-hook switch positions and the shipped-off assertion are covered at tests/skills/test_issue_l2_install.py:593-625. The separate requirement to complete FR-103 has finding F12.1 below.
- T12.AC2 met. Saved results show 819 passed and 3 skipped at .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t12-ac10.log:833. My independent rerun of all eight required files also produced 819 passed, 3 skipped.
- T12.AC3 unmet, F12.2. The five-entry history omits commit A because a separate stat-fix commit was inserted. The six-commit sequence and substituted check are recorded at .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md:27-29.

## Findings

F12.1 ac=scope at=tests/skills/test_issue_l2_install.py:606 anchor="Add FR-103 to `tests/skills/test_issue_l2_install.py` in both switch positions" chk=n,n,n,y family=incomplete-ir7-regression-coverage sev=blocking first=A1 origin=new fix=Add a monkeypatched-True test with an owned hook that asserts launched and no W-L2-ABSENT: The task explicitly requires FR-103, which includes the True/owned success case. The new parameterized test always establishes an absent hook, and searching the tests for IR7_REFUSE found no owned-hook test with the switch enabled. The required case is specified at .dev/brainstorms/20261108-094705-l2-pre-push-guard/merged-requirements.md:340.

F12.2 ac=T12.AC3 at=.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md:28 anchor="`git log --oneline -5` shows commits A, B, C, D, E in that order with E on top" chk=y,n,n,n family=history-ac-mismatch sev=blocking first=A1 origin=new fix=Obtain an explicit acceptance-criterion amendment for the owner-required six-commit sequence rather than deleting or rewriting the stat-fix commit: The actual top five commits are E, D, C, stat fix, B. The deviation records a sensible replacement check, but the live acceptance criterion still requires the five-entry sequence at .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:168.

## Self-Audit

- Independently reran all eight required regression files: 819 passed, 3 skipped. make verify-sync also passed.
- Checked that refusal precedes pending-record publication, both remedy lookups use the helper, the shipped constant remains false, and the final commit lists the required activation preconditions.
- Confirmed the prescribed comparison of the protected test is empty. Local remote-tracking refs contain no final refusal commit; no network check or push was performed.
- A direct plugin-script comparison failed because that path does not exist. A subsequent search found no orca_worktree.py under plugins; no equivalence is claimed for a nonexistent mirror.
- No source files or tests were edited. The live owner-run observations remain outside this review.
