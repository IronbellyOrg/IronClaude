e94872ee0ce7ba5d7715e716e1094ebac6844616
family: test-assert-scope
defect form: a test asserts a path or line against the whole message where the task text names a block
command: grep -n -E "in message" tests/cli/test_install_keep.py
before: lines 397-399 assert str(baks[0]) in message and the failure line in message, then only the block order
coupled sites: tests/cli/test_install_keep.py TR-001 (saved line), TR-006 (failure line) assert whole-message membership by design
after: 397:    before_failed, failed_block = message.split("❌ Failed", 1);398:    assert "💾 Saved" in before_failed  # the saved block comes before the failed block;399:    assert str(baks[0]) in before_failed.split("💾 Saved", 1)[1];
