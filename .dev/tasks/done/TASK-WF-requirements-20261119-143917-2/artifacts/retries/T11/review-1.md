d0fceb99a82a5553b5fc8c6ac7776ae1930b4cf4
# T11 review 1

Earlier blocking findings: none given (first review), so no status lines.

## ACs
- T11.AC1 met. Claim-time approval before the plan reply gives `label-before-plan` (T11.AC1@tests/issue_pipeline/test_stage_predicates.py:516, tests/issue_pipeline/test_stage_status.py:579; reason produced at src/superclaude/cli/issue_pipeline/stage_predicates.py:166). After the plan reply it is accepted (test_stage_predicates.py:525, test_stage_status.py:592). `record_create` refusals and the required `--plan-hash` are tested (tests/issue_pipeline/test_approval_record.py:431, :439, :447; option is `required=True` at src/superclaude/cli/issue_pipeline/cli.py:52). Duties text "only when the worker's `ask` carries the plan hash and `stage-status` reports the approval as accepted" is in src/superclaude/core/WORKER-CONTRACT.md:295 and asserted at tests/skills/test_worker_contract.py:3456.
- T11.AC2 met. T11.AC2@tests/issue_pipeline/test_brief.py:67 (one row per Status), :81 (Debug without `--fix`), :168 (bad Status refused with closed reason `bad-stage`); bad issue and nonce are refused in the same file (:200, :319).
- T11.AC3 met (weakly). T11.AC3@tests/issue_pipeline/test_brief.py:88 (design row vs brainstorm row with `--handoff design`) and :97 (reason recorded in issue-summary: template and refs/claim.md carry the `spec-route:` line; src/superclaude/skills/sc-issue-protocol/templates/issue-summary.md, refs/claim.md). The judgment is text-checked only, which matches the design that no code judges it.
- T11.AC4 met. T11.AC4@tests/skills/test_worker_contract.py:3404 asserts the new push sentence and that no Pipeline-and-push sentence grants the coordinator a push; the sentence is at src/superclaude/core/WORKER-CONTRACT.md:245. I ran the five touched test files: 957 passed. I did not run the whole of `tests/skills tests/issue_pipeline`.
- T11.AC5 met as far as I checked: `git status` shows no staged `.claude/` path. I did not run `make verify-sync`.

## Findings
No blocking findings.

F1.1 ac=T11.AC3 at=tests/issue_pipeline/test_brief.py:97 anchor="a well-defined issue yields the `/sc:design` row, an issue that is not yields the `/sc:brainstorm` row" chk=n,n,n,n family=spec-judgment fix=none required; optionally add a fixture issue-summary.md with a `spec-route:` line parsed end to end: the judgment is only checked as template and ref text, not as a produced summary. Non-blocking.

Other checks, clean: no remaining caller uses the old `build(issue, type, complexity)` signature (grep of tests/ and src/); line 242 reworded as the task asks (WORKER-CONTRACT.md:242); duties name `stage-status --repo` twice (WORKER-CONTRACT.md:295, :299) and cover every level; the dispatch.json fixture field names (`approver_id`, `approval_event_id`, `approved_at`) match src/superclaude/cli/issue_watch/audit.py:193-195; `approval_record.py` and `stage_predicates.py` are unchanged in the diff.
