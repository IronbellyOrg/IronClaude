# BUILD_REQUEST — Remediation for TASK-RF-20260608-150011 (sprint-recovery reflect findings)

## Source
Post-execution `/sc:reflect --mode post --depth deep` audit of commit `c0d56f18` (diff `b05e0fe1..HEAD`).
- Reflect report: `.dev/reflect/post-sprint-recovery-stranded-20260608175221/REPORT.md`
- Deviation ledger: `.dev/reflect/post-sprint-recovery-stranded-20260608175221/deviation-ledger.yaml`
- Original task: `.dev/tasks/to-do/TASK-RF-20260608-150011/TASK-RF-20260608-150011.md`

## Goal
Fix the 2 confirmed Regressions + 2 Drift the reflect ensemble independently reproduced in the sprint-recovery fix, and add the regression tests that would have caught them. All four findings are grounded with re-Read + executable PoC evidence.

## Branch
Continue on `fix/sprint-recovery-stranded-deliverables-stale-checkpoint` (the branch under audit). Do NOT branch off master fresh — these fixes amend the same work-unit. Never stage `.claude/`. PR target is the fork `IronbellyOrg/IronClaude` only.

## Scope — exactly these fixes (in priority order)

### FIX-1 (Regression, HIGH) — PRIMARY checkpoint re-run omits required INDEX_PATH
- **Site:** `src/superclaude/cli/sprint/rerun_tasks.py:1616-1630` (the PRIMARY `subprocess.run([... "rerun-tasks", "--phase", str(phase), "--tasks", checkpoint_tid, "--no-verify-checkpoints"])` argv).
- **Defect:** `rerun-tasks` requires a positional `INDEX_PATH` (`commands.py:721` `@click.argument("index_path", type=click.Path(exists=True))`). The argv has no positional ⇒ `Error: Missing argument 'INDEX_PATH'`, exit 2, swallowed by `check=False`. PRIMARY re-runs nothing.
- **Fix:** insert `str(config.index_path)` as the first positional (immediately after `"rerun-tasks"`, before `"--phase"`). Confirm `config.index_path` is the absolute resolved index (it is — `load_sprint_config`). Consider inspecting the subprocess return code and echoing a warning on non-zero (the FALLBACK keeps `check=False`, but PRIMARY should at least log a failed re-run so it is not silent).
- **Test:** add an integration test (new fixture) seeding a phase tasklist with a real `### T<PP>.<NN> -- Checkpoint:` task whose `Checkpoint Report Path:` ends in `CP-Pxx-END.md`; assert the PRIMARY branch is taken and the nested argv parses (exit 0) and a fresh verdict lands at `release_dir/checkpoints/CP-Pxx-END.md`. This closes the acknowledged "PRIMARY has no automated coverage" gap.

### FIX-2 (Regression, MED) — never-auto-PASS violable via verbatim verification_block
- **Site:** `src/superclaude/cli/sprint/checkpoints.py` `_render_recovered_checkpoint` (the "## Verification Criteria (copied from tasklist)" interpolation of `verification_section`, and the `entry.name` / `evidence_lines` interpolations). Gate reader: `executor.py:2518-2519` (`"STATUS: PASS" in content.upper() or "**RESULT**: PASS" in content.upper()`).
- **Defect:** the gate substrings can be injected verbatim from the tasklist verification prose into the rendered "UNKNOWN" report. PoC: `verification_block="...confirm **RESULT**: PASS..."` ⇒ `_check_checkpoint_pass` returns True on an UNKNOWN report.
- **Fix:** after rendering, neutralize the gate tokens in the interpolated fields — e.g. case-insensitively replace/escape `STATUS: PASS` and `**RESULT**: PASS` within `verification_section`, `entry.name`, and `evidence_lines` before assembly (or assert their absence post-render and fall back to a minimal safe body). Do NOT alter the hard-coded `## Result` UNKNOWN line.
- **Test:** per-field injection test — put each gate token in `entry.name`, the verification block, and an evidence path; assert the rendered report (uppercased) contains neither `STATUS: PASS` nor `**RESULT**: PASS`.

### FIX-3 (Drift, MED) — deliverable landing-verify OR-clause masks stranding
- **Site:** `src/superclaude/cli/sprint/recovery.py:581-585` (`landed = (canonical_dest...) or (declared.is_file() and ...)`).
- **Defect:** the cwd-resolved `declared.is_file()` clause can satisfy `landed` even when relocation never reached `canonical_dest` (clearest: empty `bundle.artifacts_produced` skips relocation at ~:537 yet verify passes). Contradicts spec item-2.1(c) and the builder's own Phase-2 note.
- **Fix:** verify the canonical mirror only — drop the `or (declared.is_file() ...)` clause, OR gate it on `declared.resolve() == canonical_dest.resolve()`.
- **Test:** strengthen `tests/sprint/test_recovery.py::test_merge_relocates_deliverable_trees_or_partials` to use production `<bundle>/results/` geometry and **non-canonical** declared paths; add a case with empty `artifacts_produced` + a stale cwd file asserting PARTIAL with a `deliverable-not-landed:` entry.

### FIX-4 (test hardening, MED) — missing checkpoint regression tests
- Add to `tests/sprint/test_checkpoints.py::TestRecoverMissingCheckpoints`: (a) a **BLOCKED**-verdict re-stamp test (branch is `in ("FAIL","BLOCKED")` but only FAIL is tested); (b) a **body-only** stale verdict test (no `status:` frontmatter, only `## Result` body — the parse path the current 5.1 never exercises because it seeds both); (c) an **idempotent re-fire** test (a re-stamped UNKNOWN report must not re-fire the re-stamp on a second `reevaluate_stale=True` call); (d) a **default-off-with-evidence** test (`reevaluate_stale=False` leaves an existing FAIL untouched even when fresh evidence is present).

## Out of scope (do NOT touch)
- DEV-4 (evidence-present proxy) and the `_mirror` mtime same-second race — advisory only; note as follow-ups, do not change behavior.
- The pre-existing `lint-architecture` failure in `recommend.md`.
- Any `.claude/` paths; any `make sync-dev` (CLI Python, not synced Markdown).

## Validation requirements
- `uv run pytest tests/sprint/ -v` fully green including all new tests.
- The two new positive tests (PRIMARY integration, injection) must FAIL against the current `c0d56f18` code and PASS after the fix (prove they catch the regressions).
- Scoped `uv run ruff check src/superclaude/cli/sprint/ tests/sprint/` clean; `ruff format` idempotent.
- POST gate: after commit, re-run `/sc:reflect --mode post --diff <new-base>..HEAD --tasklist .dev/tasks/to-do/TASK-RF-20260608-150011/TASK-RF-20260608-150011.md --depth standard` and confirm regression count is 0 before the original task's Step 8.4 marks Done.

## Template
Use the complex MDTM template (`02_mdtm_template_complex_task.md`) — multi-fix, multi-file, with a final QA + POST-reflect gate phase.
