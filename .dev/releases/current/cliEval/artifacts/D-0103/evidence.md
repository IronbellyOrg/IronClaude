# D-0103 — evidence index (T05.26)

| Artifact | Path | Purpose |
|---|---|---|
| Test module | `tests/cli/eval/test_no_mcp_skip.py` | TEST-014 pytest pin (12 tests, 11 passing, 1 gated-skip). |
| Spec | `.dev/releases/current/cliEval/artifacts/D-0103/spec.md` | Skip semantics + AC traceability. |
| Author notes | `.dev/releases/current/cliEval/artifacts/D-0103/notes.md` | Discovery, design decisions, scope. |
| Run log | `.dev/releases/current/cliEval/evidence/T05.26/pytest.log` | `uv run pytest -v` output. |
| Manifest extract | `.dev/releases/current/cliEval/evidence/T05.26/real-yaml-extract.md` | Manifest lines establishing optional_capabilities ↔ requires coupling. |

## AC traceability

| AC bullet | Pin |
|---|---|
| MCP evals classify SKIPPED with non-empty `skip_reason` under `--no-mcp` | `test_run_one_short_circuits_mcp_spec_with_no_mcp_flag` (parametrised over E1 / E2.1 / E2.2 / E2.3). |
| `counts.kept_plus_skipped_equals_n_prime` is True | `test_run_summary_counts_kept_plus_skipped_equals_n_prime_under_no_mcp`. |
| Each SKIPPED entry includes a populated `skip_reason` | Asserted in both the closure pin and the RunSummary pin; reverse-pinned by `test_run_summary_rejects_inconsistent_kept_plus_skipped_flag`. |
| `spec.md` records skip semantics | `D-0103/spec.md` (this directory). |

## Result

```
======================== 11 passed, 1 skipped in 0.36s =========================
```

The one skip is the end-to-end CliRunner test, gated on the T04.10
forward-deps and the `--no-mcp` closure branch in `commands.py`. Both
gates emit a `pytest.skip(...)` with a remediation pointer; the
end-to-end pin auto-clears once the wiring lands. Per-branch contract
tests above pin the FR-G4 / TEST-014 surface in the interim.
