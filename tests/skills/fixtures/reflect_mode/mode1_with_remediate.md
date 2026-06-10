---
id: "FIXTURE-mode1-remediate"
title: "fixture mode 1 with --remediate (AT-VALIDATION-1)"
status: "🟡 To Do"
created_date: "2026-06-09"
type: "Feature"
reflect_post_mode: "1"
reflect_post: ""
---

## Fixture — Mode 1 with --remediate (must fail V9)

## Phase 1: Final

- [ ] **1.1 — Inline post-execution reflect audit (same session, audit-only, HALT)**
  - **Context**: All implementation/test/QA items above are complete.
  - **Action**: Run `/sc:reflect --mode post --depth standard --remediate --diff {BASE}..HEAD --tasklist {TASK_FILE} --executor-model {EXECUTOR_CLASS}` as a top-level skill invocation.
  - **Output**: Frontmatter reflect_post written; reflect_post_mode: 1.
  - **Verification**: verdict recorded.
  - **Completion gate**: reflect_post.verdict == pass → proceed; else HALT.

- [ ] **1.2 — Update task status to Done**
  - **Context**: All phases complete.
  - **Action**: Update frontmatter: status to Done, set completion_date.
  - **Output**: Task file updated.
  - **Verification**: Frontmatter shows Done.
  - **Completion gate**: Task marked complete.
