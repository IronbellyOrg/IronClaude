# Implementation Handoff Prompt — PR #128 Medium Remediation

Paste the block below to a fresh implementation agent when ready.

---

Implement the two Medium-issue fixes for PR #128 (`feat/init-lite`) specified in
`.dev/brainstorms/20260604-034206-pr128-medium-remediation/merged-remediation.md`.
Read that spec first — it has the exact before/after edits, rationale, and acceptance criteria.

Context:
- Repo: IronbellyOrg/IronClaude (a FORK — any PR uses `--repo IronbellyOrg/IronClaude --base master`).
- Branch: check out `feat/init-lite` (PR #128 head `e55af621`). Work on that branch; do NOT branch off master (the file does not exist on master).
- File: `src/superclaude/cli/init_lite.py`. Use UV for everything (`uv run pytest`, never bare python/pip).
- M1 (atomic write) is ALREADY FIXED in `e55af621` — do not modify `_atomic_write`.

Apply exactly two code fixes + one doc graft + tests:

1. Med-A (fail-fast `--project-root`): change the `--project-root` option type to
   `click.Path(exists=True, file_okay=False, path_type=Path)` and update its help text.
   (Matches repo convention `src/superclaude/cli/sprint/commands.py:179`.)

2. Med-B (anchor relative `--output` to `--project-root`): replace the `out_path` line with:
   ```python
   if output is None:
       out_path = root / REPORT_RELPATH
   else:
       out_path = (output if output.is_absolute() else (root / output)).resolve()
   ```
   Update the `--output` help text to state relative values resolve against `--project-root`,
   and add the same one-line clarification to `src/superclaude/skills/sc-init-lite-protocol/SKILL.md` §4.

3. Tests (`tests/cli/test_init_lite.py`) — add all 6 listed in the spec:
   nonexistent root rejected (no `.dev/superclaude/` created); empty-but-real project still
   succeeds (regression guard for the over-rejection trap); non-dir root rejected; relative
   `--output` lands under `--project-root` not CWD; absolute `--output` unaffected; default-path parity.

Invariants you must NOT regress: `_is_protected_context_path`, `_is_init_lite_owned`, `--dry-run`
writes nothing, `--force` scoped to `.dev/superclaude/`. Keep the empty-but-real-project case
passing (only nonexistent/non-dir roots get rejected).

Gates before declaring done:
- `uv run pytest tests/cli/test_init_lite.py tests/cli/test_cli_registration.py tests/unit/test_cli_install.py`
- `uv run ruff check src/ tests/` and `uv run ruff format --check src/ tests/`
- `make sync-dev && make verify-sync` (because SKILL.md changed; never stage `.claude/` mirrors — only `src/` side).

Out of scope: M1, and review items L1/L2/L4/nit. Do not expand scope.

When green, push `feat/init-lite` to `origin` and report; the PR (#128) already exists. If asked to
update the PR body, note Med-A + Med-B addressed and M1 already fixed.
