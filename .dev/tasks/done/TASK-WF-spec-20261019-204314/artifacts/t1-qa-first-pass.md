# Task 1 independent spec-compliance review: first pass

Reviewer: independent quality-engineer; read-only inspection of the actual native helper, tests, source snapshot, task brief, change patch and upstream-contract artifact. Reviewer did not execute commands/tests or modify files. Q0 tree: `ddd1f9a31dceab5b73187dcdb68de1d1bbec6424`.

Verdict: **missing**. Exactly one Q5 fix pass was requested; no Task 2 work is authorized by this verdict.

| AC | Result | Reviewer evidence |
|---|---|---|
| T1.AC1 | met | `src/superclaude/cli/install_codebase_memory.py:187-204`; `tests/cli/test_install_codebase_memory.py:45-75` |
| T1.AC2 | met | `src/superclaude/cli/install_codebase_memory.py:138-177`, `:206-219`; `tests/cli/test_install_codebase_memory.py:78-137`, `:170-181` |
| T1.AC3 | met | `src/superclaude/cli/install_codebase_memory.py:180-185`, `:206-229`; `tests/cli/test_install_codebase_memory.py:88-98`, `:184-196` |
| T1.AC4 | unmet overall | Direct argv/private completed download/full configuration mechanics exist at `src/superclaude/cli/install_codebase_memory.py:63-72`, `:235-275`, but the task's associated mandatory installer-tree reaping requirement is not established by `:74-87`. |
| T1.AC5 | met | `src/superclaude/cli/install_codebase_memory.py:24`, `:120-135`, `:282-298`; `tests/cli/test_install_codebase_memory.py:242-259` |
| T1.AC6 | met for enumerated coverage | `tests/cli/test_install_codebase_memory.py:14-24`, `:45-310`, `:316-394`; the orphaned-descendant guarantee remains a separate gap. |
| T1.AC7 | met | `src/superclaude/cli/install_codebase_memory.py:112-135`, `:176-177`, `:276-307`; `artifacts/t1-upstream-contract.md` documents source-only verification and pending live gate. |

## Verified gap

The timeout runner signals the whole POSIX process group with TERM and KILL, but `communicate()` reaps the directly launched Popen child only. A group leader that exits while a grandchild ignores TERM can leave an orphan whose reaping is delegated to the surrounding environment rather than ensured by this helper. The task text expressly requires termination/reaping of installer descendants.

The existing real parent/child test uses a cooperative parent waiting for its child (`tests/cli/test_install_codebase_memory.py:320-325`). The leader-exits-first test mocks signalling (`:341-367`); the real TERM-ignoring test has no child (`:370-383`). Thus the current tests do not prove arbitrary orphaned-descendant reaping.

No extra scope or misunderstood requirement was independently established. Task 2 registration and Task 3 uninstall are not assessed by this review.

## Single fix-pass instruction

Add a real benign orphaned-descendant regression and the smallest compatible correction. Do not weaken tests, claim unproven descendant-reaping behavior, change the source spec, introduce a generic supervision framework, mutate host-global subreaper state, or implement unsupported platform-specific lifecycle behavior silently. If the literal guarantee cannot be met portably within scope, return a concrete blocker for the final re-review and operator ruling rather than invent compliance.
