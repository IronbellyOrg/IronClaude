# D-0077 — DOC-OQ3 `--no-pty` exclusion set in real.yaml

| Field          | Value                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------ |
| Deliverable    | D-0077                                                                                     |
| Roadmap ID     | R-077                                                                                      |
| Task           | T04.16                                                                                     |
| Tier           | EXEMPT                                                                                     |
| Owner          | architect                                                                                  |
| Closure venue  | `decisions.md` §"DOC-OQ3 Closure" (lines 1196-1203)                                         |
| Cross-refs     | OQ-3 (roadmap row 111); DOC-OQ3 (roadmap row 254); FR-CLI1; T04.10; T01.22                  |

## 1. Scope

Resolve OQ-3 ("Which eval categories are excluded by `--no-pty`") by
expressing the exclusion set declaratively on the suite manifest rather
than as a hardcoded category list in the runner.

The contract has three load-bearing surfaces:

1. **Manifest tag** — every PTY-required eval in
   `src/superclaude/cli/eval/suites/real.yaml` carries the literal
   `no_pty: skip` field.
2. **Describe projection** — `superclaude eval describe --suite real
   --eval <id>` surfaces the `no_pty:` line so operators can inspect
   the exclusion set without parsing YAML by hand.
3. **Runner short-circuit** — `superclaude eval run --no-pty` returns
   `EvalOutcome(status="SKIPPED", skip_reason="--no-pty",
   skip_flag_triggered="--no-pty")` for every tagged spec **before**
   `HomeIsolation.setup()` is called, so PTY-required evals never
   allocate a scratch HOME on hosts that cannot drive a real TTY.

## 2. Exclusion set (M4 close)

The "real" suite is, by design, exclusively PTY-driven (design-spec
§3 / §6). The M4 exclusion set is therefore the complete E1-E15 roster.
Future logic-only evals (no PTY dependency) may omit the tag and
continue to run under `--no-pty` without code changes — the exclusion
set is data-driven, not hardcoded.

| ID  | Title                                                | `no_pty` |
| --- | ---------------------------------------------------- | -------- |
| E1  | auggie-first sticky lifecycle — set then clear       | skip     |
| E2.1| MCP allowlist enforcement (auggie allowed)           | skip     |
| E2.2| MCP allowlist enforcement (denied server)            | skip     |
| E2.3| MCP allowlist enforcement (no allowlist)             | skip     |
| E3  | SessionStart hook fire                                | skip     |
| E4  | SessionStart on resumed session                       | skip     |
| E5  | UserPromptSubmit hook fire                            | skip     |
| E6  | PreToolUse Read matcher                               | skip     |
| E7  | PreToolUse Write matcher                              | skip     |
| E8  | PostToolUse Read matcher                              | skip     |
| E9  | PostToolUse Edit matcher                              | skip     |
| E10 | SubagentStart counter increment                        | skip     |
| E11 | SubagentStop counter decrement                         | skip     |
| E12 | Hook deploy idempotency                                | skip     |
| E13 | Hook stderr error fails open                           | skip     |
| E14 | Concurrent SessionStart bursts                          | skip     |
| E15 | hook timeout fails open with telemetry                  | skip     |

## 3. Schema contract (`suite.schema.json`)

`no_pty` is an optional `evalEntry` property with `enum: ["skip"]`. The
schema rejects any other shape (e.g. `"soft-skip"`, `true`,
omitted-but-typo'd `nopty`). See test
`test_schema_rejects_unknown_no_pty_values` for the rejection pin.

## 4. Runtime contract (`commands.py`)

Closure body in `eval_run` (commands.py:1832-1850):

```python
def run_one(spec: EvalSpec) -> EvalOutcome:
    if no_pty and spec.no_pty == "skip":
        return EvalOutcome(
            eval_id=spec.id,
            title=spec.title,
            status="SKIPPED",
            duration_sec=0.0,
            expects=(),
            skip_reason="--no-pty",
            skip_flag_triggered="--no-pty",
            artifacts={},
            error_class=None,
        )
    return _run_one_spec(...)
```

The short-circuit runs **before** `HomeIsolation.setup()`, so:

- no scratch HOME is allocated;
- no hook deployment occurs;
- no PTY spawn is attempted;
- `duration_sec=0.0` accurately reflects zero work.

Reporting matches the disk-budget skip shape (T04.10) so `RunCounts`
accounting and the Reporter render the two skip causes uniformly.

## 5. Describe contract (`commands.py:_evalspec_to_dict`)

`_evalspec_to_dict` (commands.py:1031-1063) projects `no_pty` onto the
describe payload when set, and omits the key when absent. The CLI YAML
emitter at `superclaude eval describe --suite real --eval E1` includes
the `no_pty: skip` line verbatim.

## 6. Acceptance evidence

See `evidence/T04.16/`:

- `pytest-output.txt` — `uv run pytest tests/cli/eval/test_no_pty_exclusion.py -v` (14 PASSED).
- `describe-E1.yaml` — `superclaude eval describe --suite real --eval E1` output with the `no_pty: skip` line.
- `summary.md` — closure summary mapping the four ACs to verifying tests/artefacts.

## 7. Cross-references

- `decisions.md` §"DOC-OQ3 Closure" (lines 1196-1203) — closure narrative.
- `roadmap.md` row 254 — DOC-OQ3 deliverable row.
- `roadmap.md` row 111 — OQ-3 origin row.
- `src/superclaude/cli/eval/suites/real.yaml` — exclusion-set manifest.
- `src/superclaude/cli/eval/commands.py:1832-1850` — runner short-circuit.
- `src/superclaude/cli/eval/commands.py:1031-1063` — describe projection.
- `src/superclaude/cli/eval/suites/suite.schema.json` — `no_pty` enum constraint.
- `tests/cli/eval/test_no_pty_exclusion.py` — 14 acceptance tests.
