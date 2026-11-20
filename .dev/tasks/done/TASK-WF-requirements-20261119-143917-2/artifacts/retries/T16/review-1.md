fe4ba5ed49ff151df1c3ddcf8645953b67bd95b4
# Review of Task 16, attempt 1

Earlier blocking findings: none (first review).

I ran `uv run pytest tests/issue_pipeline tests/issue_watch -q`: 3177 passed.

## AC marks

- T16.AC1 met. T16.AC1@tests/issue_watch/test_cycle.py:5325 runs a cycle with `repo` set to another name. It asserts no gh argv carries `IronClaude` or `IronbellyOrg`, and every argv except the user call carries the other repo. The origin test is at tests/issue_watch/test_cycle.py:5348 and ends with `origin_mismatch`. The source passes `repo=cfg.repo` at src/superclaude/cli/issue_watch/cycle.py:823-830, 891-897, 963-965, 985-987, 1002, 1009, 1020, 1067 and 1096-1098. The origin check is at src/superclaude/cli/issue_watch/cycle.py:704-705.
- T16.AC2 met. T16.AC2@tests/issue_watch/test_origin_parity.py:204 and tests/issue_watch/test_launch.py:1039 are added and pass. `check_origin` takes `repo` at src/superclaude/cli/issue_watch/launch.py:274-284 and compares with `.lower()` on both sides.
- T16.AC3 met. T16.AC3@src/superclaude/cli/issue_watch/cycle.py:276 defaults `repo` to `github.REPO` when the key is absent. tests/issue_watch/test_cycle.py:5389 covers it. All 3177 tests pass, and the diff adds no changes to existing test assertions other than the Task 15 test and the helper in conftest.
- T16.AC4 met. T16.AC4@tests/issue_pipeline/test_stage_status.py:775 (config repo Other/Repo, no `--repo`), :783 (no `repo` key reads the fork), :792 (mismatch refused with `refused:repo-mismatch` and `world.argvs == []`). The source is at src/superclaude/cli/issue_pipeline/cli.py:442-446. The mismatch check runs before `_stage_status`, so it refuses before any call.
- T16.AC5 met. T16.AC5@tests/issue_watch: 3177 passed with issue_pipeline included.

## Findings

No blocking findings.

F1.1 ac=scope at=src/superclaude/cli/issue_watch/launch.py:78 anchor="ORIGIN_REPO = \"ironbellyorg/ironclaude\"" chk=n,n,n,n family=none fix=none: Non-blocking note. The task text says `check_origin` is called from the launch step as well as `_origin_ok`. Only src/superclaude/cli/issue_watch/cycle.py:705 calls it, so there is no other call site to update.
