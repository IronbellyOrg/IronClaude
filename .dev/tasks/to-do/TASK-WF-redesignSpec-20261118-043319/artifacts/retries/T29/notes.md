4fd9e9b6096d2b22766ba4a17c01ef38206a4340
minor F1.1 (make-test-red): after the owner synced the dev mirror and installed ruff, make test gives 1 failed, 28414 passed, 153 skipped, 2 xpassed (log /tmp/t29_test2.log). The one failure is tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files; neither it nor src/superclaude/cli/install_keep.py is touched by this work, and it fails on its own rerun. The criterion "make test passes" is therefore met except for this one failure outside the change.
minor F1.2 (missing-evidence): per-width scorecards written as reviewer-outputs/width-160.scores.md, width-116.scores.md and width-80.scores.md (29 rows each).
minor F1.3 (zellij-note): owner ruling 2026-11-18: record the check as a note, not as a decline; the check was not run because an agent cannot drive a live Zellij session. zellij-note.md says so and lists the steps for a person.
minor F1.4 (staging): git add .dev/tasks run again after the review files were written.
note: make lint exit 0; tests/observe 1176 passed; export.py diff empty; no .claude path staged.
