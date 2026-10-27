# T04.16 — DOC-OQ3 `--no-pty` exclusion set — evidence summary

| Field        | Value                                                  |
| ------------ | ------------------------------------------------------ |
| Task ID      | T04.16                                                 |
| Deliverable  | D-0077                                                 |
| Roadmap ID   | R-077                                                  |
| Tier         | EXEMPT                                                 |
| Date         | 2026-05-21                                             |
| Outcome      | PASSED — all four acceptance criteria satisfied         |

## Acceptance criteria → evidence map

| AC | Statement | Verifying artefact |
| -- | --------- | ------------------ |
| AC1 | `no_pty: skip` annotation appears on each PTY-required eval in `suites/real.yaml` | `pytest-output.txt` — `test_real_suite_marks_every_eval_no_pty_skip` PASSED (E1, E2.1, E2.2, E2.3, E3..E15 all carry the tag). |
| AC2 | `EvalSpec` round-trip preserves the tag via schema + loader | `pytest-output.txt` — `test_schema_accepts_no_pty_skip_on_eval_entry`, `test_schema_rejects_unknown_no_pty_values`, `test_validate_manifest_round_trips_no_pty`, `test_real_suite_loads_through_full_pipeline` all PASSED. |
| AC3 | `superclaude eval describe --suite real --eval <id>` surfaces the `no_pty` tag | `describe-E1.yaml` — final line reads `no_pty: skip`. Tests `test_evalspec_to_dict_emits_no_pty_when_set`, `test_evalspec_to_dict_omits_no_pty_when_absent`, `test_describe_suite_surfaces_no_pty_for_real_e1`, `test_cli_describe_yaml_surfaces_no_pty` all PASSED. |
| AC4 | `--no-pty` short-circuits every tagged spec to `SKIPPED` with `skip_reason="--no-pty"` BEFORE HomeIsolation | `pytest-output.txt` — `test_run_one_short_circuits_tagged_spec_with_no_pty_flag`, `test_run_one_does_not_short_circuit_untagged_spec`, `test_run_one_runs_tagged_spec_when_no_pty_flag_absent`, `test_eval_run_no_pty_skips_real_suite_end_to_end` all PASSED. The end-to-end pin patches `_run_one_spec` to raise and the suite still runs cleanly because the closure short-circuits before any worker invocation. |

## Test run

`uv run pytest tests/cli/eval/test_no_pty_exclusion.py -v`

```
============================== 14 passed in 0.38s ==============================
```

See `pytest-output.txt` for the full report.

## Code surfaces verified

| Surface | Location | Role |
| ------- | -------- | ---- |
| Schema enum | `src/superclaude/cli/eval/suites/suite.schema.json` | `no_pty` accepts only `"skip"`. |
| Manifest tags | `src/superclaude/cli/eval/suites/real.yaml` | Every E1-E15 entry carries `no_pty: skip`. |
| Dataclass field | `src/superclaude/cli/eval/models.py:EvalSpec.no_pty` | `Optional[Literal["skip"]]`. |
| Describe projection | `src/superclaude/cli/eval/commands.py:1031-1063` (`_evalspec_to_dict`) | Emits `no_pty` when set. |
| Runner short-circuit | `src/superclaude/cli/eval/commands.py:1832-1850` (`run_one` closure inside `eval_run`) | Returns `SKIPPED` with `skip_reason="--no-pty"` before `_run_one_spec` is called. |

## Cross-references

- Closure narrative: `decisions.md` §"DOC-OQ3 Closure" (lines 1196-1203).
- Deliverable spec: `artifacts/D-0077/spec.md`.
- Roadmap rows: 111 (OQ-3 origin), 254 (DOC-OQ3 deliverable).
