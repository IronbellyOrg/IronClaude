# D-0001 — Author Notes

- Counted 9 subdirectories on disk at authoring time; the FR-L2.4 extraction text mentions "11 subdirectories" but only 9 exist (`benchmarks/`, `evals/`, `eval-workspaces/`, `releases/`, `research/`, `resurrection-contracts/`, `tasks/`, `test-fixtures/`, `test-sprints/`). Enumerated what is actually present per phase-1 acceptance criterion ("Every existing subdirectory of `.dev/` is enumerated").
- Rule is quoted verbatim inside a top-level blockquote so it is the first concrete sentence a reader sees after the heading.
- Decision guide table added (not required by acceptance criteria) to make the convention actionable — keeps the file useful as the M2 error message and M3 hook will reference it.
- Did not list nested children (e.g. `releases/archive/`, `releases/current/`) inline; called them out parenthetically in the `releases/` row to keep the table flat.
- No pre-existing `.dev/README.md` was present; this is a clean create (no merge needed).
