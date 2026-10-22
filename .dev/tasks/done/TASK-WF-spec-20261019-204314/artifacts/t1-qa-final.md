# Task 1 final Q5 spec-compliance verdict

Final independent reviewer verdict: **missing** after the single permitted fix pass. Product source/tests were unchanged during Q5. No Task 2–7 work has begun.

Six of seven acceptance bullets are met; the literal direct-argv/full-bootstrap AC4 mechanics are also met. The unmet requirement is the associated mandatory task-body lifecycle guarantee: termination/reaping of the installer and its descendants on timeout. The reviewer assigns that instruction gap to T1.AC4 rather than falsely claiming argv execution is defective.

| AC | Final status | Produced-file evidence |
|---|---|---|
| T1.AC1 | met | `src/superclaude/cli/install_codebase_memory.py:187-204`; `tests/cli/test_install_codebase_memory.py:45-75` |
| T1.AC2 | met | `src/superclaude/cli/install_codebase_memory.py:138-177`, `:206-219`; `tests/cli/test_install_codebase_memory.py:78-181` |
| T1.AC3 | met | `src/superclaude/cli/install_codebase_memory.py:180-185`, `:206-229`; `tests/cli/test_install_codebase_memory.py:88-98`, `:184-196` |
| T1.AC4 plus lifecycle instruction | unmet | `src/superclaude/cli/install_codebase_memory.py:63-86`, `:235-275`; actual implementation reaps only its direct child. |
| T1.AC5 | met | `src/superclaude/cli/install_codebase_memory.py:24`, `:120-135`, `:282-298`; `tests/cli/test_install_codebase_memory.py:242-259` |
| T1.AC6 | met for enumerated acquisition/failure/cleanup coverage | `tests/cli/test_install_codebase_memory.py:14-24`, `:45-310`, `:316-394`; no arbitrary orphan-reaping proof. |
| T1.AC7 | met | `src/superclaude/cli/install_codebase_memory.py:112-135`, `:176-177`, `:276-307` |

No extra scope or misunderstood requirement was independently established.

## Blocking distinction

The helper terminates remaining members of its new POSIX process group using TERM/KILL and reaps the directly launched Popen child via communicate. It does not adopt/reap arbitrary orphaned grandchildren. The current real child fixture uses a cooperative parent waiting for its child; the leader-first exit fixture tests signalling through mocks.

POSIX wait/waitpid restrict collection to immediate children. Process-group selection does not change parenthood. A Linux subreaper extension is not portable to macOS and was not introduced. The portability explanation does not waive the frozen task requirement.

Source evidence and authoritative OS references are recorded in `./t1-q5-blocker.txt`. The coordinator independently re-fetched https://pubs.opengroup.org/onlinepubs/9799919799/functions/wait.html and verified child-only wait semantics and ECHILD for nonchildren.

## Final extras and disposition

Coordinator checks: 53 tests passed, Ruff passed, mypy failed with one str-to-Path assignment typing error at helper line 166. Exact commands/results are in `./t1-extras-final.txt`. Passing tests and lint do not override the missing spec requirement.

Disposition: **E-HALT-QA**. Task 1 stays blocked and its Q0 snapshot pin stays available. The coordinator must obtain an operator ruling before completing a non-compliant task or starting Task 2. No native installation/removal, developer configuration mutation, commit, push or live smoke was performed.
