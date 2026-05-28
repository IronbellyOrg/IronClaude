=== Phase 4 source diffs ===
 src/superclaude/cli/eval/commands.py   | 145 ++++++++++++++++++++++-----------
 src/superclaude/cli/eval/isolation.py  |  81 ++++++++++++++----
 src/superclaude/cli/eval/reporter.py   |  77 ++++++-----------
 src/superclaude/cli/eval/run_report.py | 104 ++++++++++++++++++-----
 4 files changed, 269 insertions(+), 138 deletions(-)

=== Phase 4 test additions ===
 tests/cli/eval/test_atomic_setup.py              | 123 +++++++++++++++-------
 tests/cli/eval/test_containment.py               |  63 ++++++++++++
 tests/cli/eval/test_coverage_gate.py             |  29 +++++-
 tests/cli/eval/test_coverage_gate_integration.py |  15 ++-
 tests/cli/eval/test_hard_guard_real_home.py      |  42 +++-----
 tests/cli/eval/test_home_isolation_extend.py     | 114 +++++++++++++++++++++
 tests/cli/eval/test_path_containment.py          |  29 ++++--
 tests/cli/eval/test_run_report.py                |  11 +-
 tests/cli/eval/test_run_summary.py               |  41 ++++++++
 tests/cli/eval/test_scratch_root_allowlist.py    |  30 +++++-
 tests/cli/eval/test_single_command.py            |  22 +++-
 tests/cli/eval/test_symlink_attacks.py           | 124 +++++++++++++----------
 12 files changed, 503 insertions(+), 140 deletions(-)

=== Phase 4 pytest ===
tests/cli/eval/test_symlink_attacks.py::TestScratchSymlinkToHome::test_scratch_root_symlink_to_non_allowlisted_target_is_refused PASSED [ 97%]
tests/cli/eval/test_symlink_attacks.py::TestScratchSymlinkToHome::test_scratch_root_symlink_chain_to_outside_is_refused PASSED [ 97%]
tests/cli/eval/test_symlink_attacks.py::TestScratchSymlinkToHome::test_scratch_symlink_refusal_runs_before_mkdtemp PASSED [ 97%]
tests/cli/eval/test_symlink_attacks.py::TestNestedSymlinkEscape::test_mkdtemp_returns_symlink_escape_refused PASSED [ 97%]
tests/cli/eval/test_symlink_attacks.py::TestNestedSymlinkEscape::test_nested_symlink_chain_refused PASSED [ 97%]
tests/cli/eval/test_symlink_attacks.py::TestNestedSymlinkEscape::test_symlink_escape_refusal_observes_post_mkdtemp_path PASSED [ 97%]
tests/cli/eval/test_symlink_attacks.py::TestPartialHomePreservedOnSymlinkAttack::test_no_partial_home_after_scratch_symlink_refusal PASSED [ 97%]
tests/cli/eval/test_symlink_attacks.py::TestPartialHomePreservedOnSymlinkAttack::test_partial_home_preserved_after_symlink_escape_refusal PASSED [ 97%]
tests/cli/eval/test_symlink_attacks.py::TestSetupFailedTagUnderSymlinkAttack::test_scratch_symlink_violation_does_not_write_tag PASSED [ 97%]
tests/cli/eval/test_symlink_attacks.py::TestSetupFailedTagUnderSymlinkAttack::test_symlink_escape_violation_does_not_write_tag PASSED [ 98%]
tests/cli/eval/test_symlink_attacks.py::TestSetupFailedTagUnderSymlinkAttack::test_non_containment_exception_in_symlink_context_writes_tag PASSED [ 98%]
tests/cli/eval/test_symlink_attacks.py::TestOrderingAfterMkdtempBeforeHookDeploy::test_hook_deploy_not_called_when_scratch_symlink_refused PASSED [ 98%]
tests/cli/eval/test_symlink_attacks.py::TestOrderingAfterMkdtempBeforeHookDeploy::test_hook_deploy_not_called_when_symlink_escape_refused PASSED [ 98%]
tests/cli/eval/test_symlink_attacks.py::TestOrderingAfterMkdtempBeforeHookDeploy::test_containment_guard_runs_after_mkdtemp PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_exists_at_canonical_path PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_references_each_command[01-targeted-pytest] PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_references_each_command[02-make-verify-sync] PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_references_each_command[03-eval-doctor] PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_references_each_command[04-eval-run-E1] PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_lists_commands_in_canonical_order PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_links_evidence_log[01-targeted-pytest] PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_links_evidence_log[02-make-verify-sync] PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_links_evidence_log[03-eval-doctor] PASSED [ 98%]
tests/cli/eval/test_validation_commands.py::test_doc_links_evidence_log[04-eval-run-E1] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 1. Contract] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 2. Command details + evidence locations] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 3. Execution order and idempotency] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 4. Acceptance map (T06.11)] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 5. Known blockers] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 6. Reproducibility] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_carries_required_section[## 7. Cross-references] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_evidence_root_directory_exists PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[01-targeted-pytest] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[02-make-verify-sync] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[03-eval-doctor] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_evidence_log_present_with_exit_code[04-eval-run-E1] PASSED [ 99%]
tests/cli/eval/test_validation_commands.py::test_doc_records_known_blockers_section PASSED [100%]

=============================== warnings summary ===============================
tests/cli/eval/test_pty_lifecycle.py::test_real_claude_help_spawn_and_transcript
tests/cli/eval/test_pty_lifecycle.py::test_lifecycle_prompt_ready_and_input_injection
tests/cli/eval/test_pty_lifecycle.py::test_lifecycle_timeout_reaps_child
tests/cli/eval/test_pty_lifecycle.py::test_lifecycle_transcript_persisted_end_to_end
tests/cli/eval/test_signal_handling.py::test_pty_driver_terminate_kills_real_subprocess
  /config/.local/share/uv/python/cpython-3.12.12-linux-x86_64-gnu/lib/python3.12/pty.py:95: DeprecationWarning: This process (pid=1753860) is multi-threaded, use of forkpty() may lead to deadlocks in the child.
    pid, fd = os.forkpty()

-- Docs: <https://docs.pytest.org/en/stable/how-to/capture-warnings.html>
================= 1368 passed, 4 skipped, 5 warnings in 19.42s =================
EXIT_CODE=0

=== Phase 4 ruff ===
All checks passed!
EXIT_CODE=0

=== Phase 4 verify-sync ===
  ✅ hooks.json matcher and auggie-flag-clear.sh case body agree on auggie prefixes

✅ All components in sync.
EXIT_CODE=0

=== H1 grep gate ===
(0 hits — PASS)

=== H5 grep ordering ===
1763:    # ``home_root.mkdir`` below so the path is in the allowlist at the
1766:    runtime_allowed = tuple(base_config.allowed_scratch_roots) + (
1774:        allowed_scratch_roots=runtime_allowed,
1781:    home_root.mkdir(parents=True, exist_ok=True)
