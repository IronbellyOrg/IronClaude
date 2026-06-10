---
id: "FIXTURE-mode1-wrapper"
title: "fixture mode 1 carrying mode-2 wrapper shape (AT-VALIDATION-1 / AT-MISMATCH-1)"
status: "🟡 To Do"
created_date: "2026-06-09"
type: "Feature"
reflect_post_mode: "1"
reflect_post: ""
---

## Fixture — Mode 1 with wrapper shape (must fail V6)

## Phase 1: Final

- [ ] **1.1 — Independent post-execution reflect gate (wrapper subprocess, HALT)**
  - **Context**: All implementation/test/QA items above are complete.
  - **Action**: Run, as a Bash shell-out: `superclaude reflect run {TASK_FILE}`. The wrapper derives the depth and runs reflect with --remediate.
  - **Output**: Frontmatter reflect_post written by the wrapper; reflect_post_mode: 1.
  - **Verification**: The wrapper exited 0.
  - **Completion gate**: reflect_post.verdict == pass → proceed; else HALT.

- [ ] **1.2 — Update task status to Done**
  - **Context**: All phases complete.
  - **Action**: Update frontmatter: status to Done, set completion_date.
  - **Output**: Task file updated.
  - **Verification**: Frontmatter shows Done.
  - **Completion gate**: Task marked complete.
