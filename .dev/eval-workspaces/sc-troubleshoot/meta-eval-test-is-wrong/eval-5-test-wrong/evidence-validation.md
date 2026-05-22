# Evidence Validation — Wave 5

**Validator**: evidence-validator (inline simulation)
**Report draft**: `REPORT.md.draft`
**Allow command re-exec**: false
**Method**: Read each cited `file:line`, confirm the quoted snippet exists at the cited location, drop mismatches.

## Citations validated

| # | Citation | Verified? | Notes |
|---|----------|-----------|-------|
| 1 | `docs/eval/scratch-roots.md:11-21` — three allowed roots table | ✓ | Read; matches. Table lists `/tmp/eval-runs/`, `<repo>/.dev/eval-runs/`, `--output-dir <path>`. |
| 2 | `docs/eval/scratch-roots.md:28-38` — "Why an allowlist (and not a denylist)" | ✓ | Read; matches. |
| 3 | `src/superclaude/cli/eval/config.py:63-67` — `_default_allowed_scratch_roots()` returns tuple | ✓ | Read via grep; lines 63-67 contain the function body returning `(Path("/tmp/eval-runs"), Path(".dev/eval-runs"))`. |
| 4 | `src/superclaude/cli/eval/config.py:40-50` — `SCRATCH_ROOT_POLICY` constant | ✓ | Read via grep; constant defined on line 40, includes the three roots. |
| 5 | `tests/cli/eval/test_scratch_root_policy.py:170-182` — `test_doctor_accepts_allowlisted_output_dir` | ✓ | Read; positive test exists, asserts exit code 0 for `/tmp/eval-runs/sub`. |
| 6 | `tests/cli/eval/test_scratch_root_policy.py:146-156` — `test_doctor_rejects_non_allowlisted_output_dir` | ✓ | Read; negative test exists, asserts exit code 2 + policy block in stderr. |
| 7 | `src/superclaude/cli/eval/commands.py:845-850` — doctor calls `resolve_scratch_root` and renders violation | ✓ | Read via grep; doctor function calls `resolve_scratch_root(output_dir)` and catches `ScratchRootViolation`. |
| 8 | Commit reference: `5a65c62 fix(cliEval): close scratch-root allowlist tautology in eval_run (PR #66 review)` | ✓ | Verified via `git log` in working tree. |
| 9 | `CLAUDE.md` — "Plugin Override — Skill-Creator Workspace Destination" naming `.dev/eval-workspaces/<skill-name>/` | ✓ | Read in CLAUDE.md context window — present. |

## Citations dropped

None. All citations were verifiable.

## Suggested report status

**success** — all evidence grounded; no `partial` downgrade needed.

## Notes

The only "fact" not strictly verifiable in this session is the runtime behavior of the synthetic test (the test file itself does not exist on disk at `tests/cli/eval/test_scratch_root_policy.py` — only the *real* test suite of the same name exists; the synthetic test was provided inline by the user). This is correctly framed in the REPORT.md: the diagnosis stands regardless of whether the synthetic test runs (the test is wrong as written either way), and the Grounding Gaps section notes this.
