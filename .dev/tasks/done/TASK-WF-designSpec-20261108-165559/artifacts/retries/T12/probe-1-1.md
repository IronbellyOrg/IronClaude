acb70ba1d033199da22be7d9eeeffabeac8d5799
# Task 12 family probes

## incomplete-ir7-regression-coverage

- Defect: FR-103's True/owned launch success case is missing; existing parameterization covers only absent hooks.
- Command: `grep -n -E 'IR7_REFUSE|test_ir7|l2_status\(wt\)' tests/skills/test_issue_l2_install.py src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py`
- before (test hits): `594:def test_ir7_absent_l2_switch(`; `605:monkeypatch.setattr(module, "IR7_REFUSE", refuse)`; `606:assert module.l2_status(wt)[0] == "absent"`; `624:def test_ir7_shipped_switch_is_off():`; `625:assert _load().IR7_REFUSE is False`. Source hits: 53,810,813,821,822,1374,1412,1696,1699,1701 (the shipped-False constant, remedy, status calls and refusal guard). No True/owned test hit.
- Coupled sites: absent-hook warning/remedy assertion; True/absent enforcement_hook assertion; True/owned success branch and no-warning assertion; shipped-False assertion.
- after: test hits now 594 (`test_ir7_l2_switch`), 605 (patch), 616 (`owned` or `absent` assertion), 639-640 (shipped-False assertion). Source hits unchanged. The three parameter pairs include True/owned with an actual installed hook. Focused result: 4 passed. First owned-case verification failed because the reused launch fixture's uv is a no-op; the owned case now removes that temporary stub, uses the real selector and passes. The False/absent remedy and True/absent installed-enforcement assertions are pinned too.

## history-ac-mismatch

- Defect: the literal five-entry history AC omits A after the owner-ordered separate stat-fix commit. No history rewrite is authorized.
- Command: `grep -n -E 'SD-3|six|five|stat-fix|git log --oneline' .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md .dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md`
- before: spec-deviations.md:25 `## SD-3: Task 12 history check includes the owner-ordered stat-fix commit`; :27 five-commit plan rule; :28 `The implementation therefore has six commits: A, B, stat fix, C, D, E.`; :29 `Use git log --oneline -6` and compare the protected test against `e28a71719^`; plan:168 still requires `git log --oneline -5` showing A,B,C,D,E.
- Coupled sites: pinned T12.AC3; SD-3 equivalent check; commit E body. Owner-provenance acceptance requested via Orca message 645344fb-670c-4680-92cc-b3912466deea; not assumed.
- after: spec-deviations.md:25,27-30 and plan:168 are the grep hits. SD-3:30 records explicit owner approval on 2026-11-09 (msg_9b527074031c) for the history-count mismatch only, preserving A,B,stat-fix,C,D,E and the full comparison from A's parent. The literal five-entry AC stays unmet; it is not rewritten. The executor will record the scoped Ruling after the fresh review's blocked line, with all other requirements still enforced.
