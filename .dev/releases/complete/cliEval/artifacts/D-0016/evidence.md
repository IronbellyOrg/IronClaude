# D-0016 — Evidence

## Test results

`uv run pytest tests/cli/eval/test_scratch_root_allowlist.py -v`

Result: **19 passed in 0.15s** (full log at
`evidence/T01.19/pytest.log`).

Coverage breakdown:

| Bucket | Tests | Notes |
|---|---|---|
| Exit-code mapping | 1 | `test_scratch_root_violation_exit_code_is_two` confirms the constant matches the loader trio (= 2). |
| Positive — canonical prefixes | 3 | `/tmp/eval-runs` (root + sub-path) and `.dev/eval-runs` sub-path. |
| Positive — `--output-dir` override | 2 | Accepts under user-supplied output dir; verifies override is call-scoped (not persistent). |
| Negative — non-allowlisted prefixes | 6 | Parametrised across `/home/user/foo`, `/var/lib/eval-runs`, `/etc/passwd`, `/root/.claude`, `/usr/local/share`, `/tmp/other-runs`. |
| Negative — message forensics | 1 | Exception message must surface the offending path and the AC12 anchor. |
| Allowlist source of truth | 2 | Narrowed `EvalConfig` flips which paths pass; default `EvalConfig()` retains the canonical pair. |
| Ergonomics + traversal hardening | 4 | `str` input accepted; `..` traversal collapsed; `~` expanded; internal prefix resolver handles relative + absolute inputs. |

Cross-suite: `uv run pytest tests/cli/eval/ -q` exits **255 passed in
0.52s** — no regressions in the sibling eval CLI tests.

## Files touched

| Path | Kind | Change |
|---|---|---|
| `src/superclaude/cli/eval/config.py` | source | Added `ScratchRootViolation`, `SCRATCH_ROOT_VIOLATION_EXIT_CODE`, `resolve_scratch_root`, `_resolve_prefix`, and `__all__` listing. |
| `src/superclaude/cli/eval/__init__.py` | source | Re-exported the three new public symbols + the constant. |
| `tests/cli/eval/test_scratch_root_allowlist.py` | test | New 19-assertion module. |
| `.dev/releases/current/cliEval/artifacts/D-0016/spec.md` | doc | Policy + acceptance map (this deliverable). |
| `.dev/releases/current/cliEval/artifacts/D-0016/notes.md` | doc | Implementation decisions + follow-ups. |
| `.dev/releases/current/cliEval/artifacts/D-0016/evidence.md` | doc | This file. |
| `.dev/releases/current/cliEval/evidence/T01.19/pytest.log` | log | Captured pytest output. |

## Acceptance criteria → evidence map

| AC (from phase-1-tasklist T01.19) | Evidence |
|---|---|
| `resolve_scratch_root` raises `ScratchRootViolation` for `/home/user/foo`, `/var/lib/eval-runs`, and any non-allowlisted prefix. | `test_rejects_non_allowlisted_paths` parametrised across 6 prefixes including the two named in the AC. |
| Resolved paths under `/tmp/eval-runs/`, repo `.dev/eval-runs/`, or `--output-dir` pass. | `test_accepts_path_under_tmp_eval_runs`, `test_accepts_tmp_eval_runs_root_itself`, `test_accepts_path_under_dev_eval_runs`, `test_accepts_path_under_output_dir`. |
| Allowlist source is `EvalConfig.allowed_scratch_roots`; no other module embeds a hard-coded copy. | `test_allowlist_source_is_evalconfig` proves narrowing the config flips behaviour; the helper accepts a `config` kwarg, defaults to `EvalConfig()`, and reads only `config.allowed_scratch_roots` (plus the per-call `output_dir`). |
| `TASKLIST_ROOT/artifacts/D-0016/spec.md` documents the allowlist policy. | `spec.md` in this directory. |
