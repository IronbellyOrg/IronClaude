# File Inventory Research

Status: Complete

## Scope

Inventory for the PR #167 verdict-regex remediation task. The remediation should be a two-file source/test change, with the troubleshoot report used as read-only grounding.

## Relevant files

| File | Purpose in task | Key symbols / tests | Modify or read? |
|---|---|---|---|
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py` | Source file containing PRD semantic gate checks and the verdict parser that needs remediation. | `_check_verdict_field(content: str) -> bool \| str` is defined at lines 37-67. Its markdown branch currently documents free-form decoration at lines 47-60 and uses the active regex at lines 61-64. `_check_qa_verdict` delegates to `_check_verdict_field` at lines 296-298. `GATE_CRITERIA` wires `_check_verdict_field` into `sufficiency-review` at lines 402-414 and `verify-task-file` at lines 455-466. | Modify only the `_check_verdict_field` markdown regex/comment area. Read surrounding gate wiring to understand blast radius; avoid unrelated gate changes. |
| `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py` | Unit test file for PRD gates; should receive regression coverage for accepted numbered-list and underscore-emphasis verdict shapes while preserving invalid-shape strictness. | Imports `_check_verdict_field` at lines 10-20. `TestCheckVerdictField` starts at lines 91-92. Baseline JSON/markdown acceptance is lines 94-106. Existing valid markdown shapes are parametrized at lines 108-117. Existing invalid-shape rejects are lines 119-135. Decorated valid shapes are parametrized at lines 137-153. Rationale-heading false-positive guard is lines 155-158. | Modify by adding narrowly scoped regression cases under `TestCheckVerdictField`; do not restructure unrelated tests. |
| `/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/REPORT.md` | Read-only diagnosis and acceptance criteria source for the task-builder remediation. | Summary states the Augment finding is valid and identifies the false negative for digit/underscore decoration at lines 17-20. Diagnosis/root cause is lines 37-43. Evidence cites the current regex and failing reproducer at lines 45-51. Proposed fix and exact files to change are lines 53-60. Verification commands are lines 61-63. | Read only. Do not modify. Use as task evidence and verification guidance. |

## Required remediation evidence to carry into the task

- Current implementation accepts JSON verdict fields first, then markdown verdict lines in `_check_verdict_field`; the source of the bug is the markdown branch, not JSON parsing (`/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:37-67`).
- The current markdown regex is line-anchored and intentionally strict about colon and uppercase `PASS|FAIL`, but it models decoration with non-word/non-colon classes: `r"(?:^|\n)[^\w\n:]*(?i:verdict)[^\w\n:]*:[^\w\n:]*(PASS|FAIL)(?!\w)"` at `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py:61-64`.
- The troubleshoot report says the false negative is caused by the current regex's non-word decoration class excluding digits and underscores, so valid markdown such as `1. Verdict: PASS` and `__Verdict__: PASS` fails (`/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/REPORT.md:37-43`).
- The same report requires preserving strictness: colon remains required, `PASS|FAIL` remains uppercase/case-sensitive, `PASSING`/`FAILURE` remain rejected, and `Verdict rationale` without a value remains rejected (`/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/REPORT.md:53-55`).
- Existing tests already cover valid plain/bold markdown verdicts, invalid separators/missing colon/malformed value shapes, decorated emoji/heading/bullet shapes, and the `Verdict rationale` guard (`/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py:94-158`). Add the missing accepted shapes without weakening these guards.

## Suggested task boundaries

- Change exactly these two files:
  - `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/src/superclaude/cli/prd/gates.py`
  - `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473/tests/cli/prd/test_gates.py`
- Treat `/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/REPORT.md` as read-only evidence.
- Avoid unrelated edits to other PRD gate checks, `GATE_CRITERIA`, or non-verdict tests.
- Verification target from the report: `uv run pytest tests/cli/prd/test_gates.py::TestCheckVerdictField -v` from `/config/workspace/IronClaude/.dev/worktrees/troubleshoot-pr167-r3406462473` (`/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/REPORT.md:61-63`).

## Evidence artifact coverage

- `/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/tier1-observation.md` is read-only runtime grounding. It records PR #167 branch/head and the UV reproducer showing `1. Verdict: PASS` and `__Verdict__: PASS` fail while positive controls pass.
- `/config/workspace/IronClaude/.dev/troubleshoot/github-pr-167-discussion-r3406462473-20260612230428/evidence-validation.md` is read-only citation-validation grounding. It records that all local report file:line citations were verified, with the command evidence passed through under `allow_command_reexec=false`.

## Summary

The remediation is a bounded two-file bug fix in the PR #167 worktree. Modify only `_check_verdict_field` in `gates.py` and the `TestCheckVerdictField` coverage in `test_gates.py`; use the troubleshoot report, observation, and evidence-validation artifacts as read-only grounding. The task builder should preserve strict invalid-shape protections and require UV-based targeted validation before completion.
