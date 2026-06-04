# Phase 1 Baseline — Regression Subset + start_commit

**Captured:** 2026-06-04 (pre-edit, Step 1.3)

## start_commit

```text
2ea470c15ec110719fe6636cd184fa4defecce75
```

Written to frontmatter `start_commit:`. This is the `<BASE>` for the POST reflect diff.

## Baseline regression-subset result

Command:

```text
uv run pytest tests/audit/ tests/skills/test_task_builder_merge.py tests/sprint/test_checkpoints.py tests/audit/test_checkpoint.py -q
```

**Result: 26 failed, 1233 passed, 1 skipped, 37 errors (exit 1)** — recorded verbatim in
`phase-outputs/test-results/phase1-baseline-pytest.txt`.

### IMPORTANT — baseline is NOT clean; failures are pre-existing

The 63 failing/erroring tests are **dominated by mirror-parity / byte-identity / mirror-line-number
assertions** in `tests/audit/`:

- `test_*_byte_identical` / `test_source_and_mirror_byte_identical` / `test_files_byte_identical`
- `test_*_in_mirror` / `test_*_mirror_exists` / `test_header_at_same_line_number`
- `test_self_audit_heading_at_or_after_line_794_mirror`, `test_header_line_number_matches`

These compare `src/superclaude/...` against the `.claude/...` mirror. They are failing because **the
`.claude/` mirror is STALE in this worktree** (sync-dev has not been run here). Running `make sync-dev`
(Steps 2.14 / 3.15) regenerates the mirror, which is expected to RESOLVE most of these mirror-parity
failures (an improvement, not a regression).

### Phase 4 triage rule (consequence of the above)

Because the baseline is stale-mirror-polluted, Phase 4 must NOT treat "fewer failures than baseline" as a
problem. The regression test is: **does any test that was GREEN in this baseline turn RED after the edits?**
The most likely true-regression signature from additive markdown edits is a *mirror line-number assertion*
that shifts because new content displaced a byte-exact anchor (e.g.
`test_self_audit_heading_at_or_after_line_794_mirror`, `test_header_at_same_line_number`,
`test_inherited_verdict ... header_at_same_line_number`). Those are the ones to watch after sync-dev.

Full failing/erroring test name list: see the raw `phase1-baseline-pytest.txt` (FAILED/ERROR lines).
