# D-0103 — author notes (T05.26)

## Discovery notes

* **Closure wiring gap (M2)** — `eval_run.run_one` at
  `src/superclaude/cli/eval/commands.py`:1530-1558 short-circuits
  `--no-pty` but the `CapabilityGates` instance constructed at line
  1512 is immediately `del`'d ("construction is the wiring; instance
  unused at M2"). The `--no-mcp` runtime closure branch is therefore
  the open follow-up T05.26 must accommodate. End-to-end test gates
  itself on the wiring presence so it auto-clears once landed.

* **Test-pattern donor** — `tests/cli/eval/test_no_pty_exclusion.py`
  is the closest analog: schema-layer + closure-branch + RunCounts +
  CliRunner end-to-end with forward-dep gating. T05.26 mirrors the
  structure beat-for-beat, swapping `spec.no_pty == "skip"` for the
  MCP-requirement check `any(r.startswith("mcp_server.") for r in
  spec.requires)`.

* **`skip_reason` format convention** — established by
  `tests/cli/eval/test_reporter_contract.py::_skipped`:
  `"capability_gate:mcp_server.<name>"`. Distinguishable from
  `"--no-pty"` (DOC-OQ3) or future shapes (disk-budget,
  manifest-misconfig).

* **MCP evals confirmed** — E1, E2.1, E2.2, E2.3 in `real.yaml`
  carry `requires:` tuples that name `mcp_server.auggie` /
  `mcp_server.auggie-mcp` / `mcp_server.airis-mcp-gateway`. E8
  additionally requires `mcp_server.serena` but is outside the
  TEST-014 scope per the task description's explicit eval list.

## Design decisions

* Hard-coded the four MCP eval IDs (`MCP_EVAL_IDS`) at module level
  so a future manifest reshuffle breaks TEST-014 loudly rather than
  silently dropping coverage. Counterpoint: tighter coupling to the
  current manifest shape. Accepted because the manifest is the
  authoritative coverage map and the four IDs are roadmap-frozen
  (OQ-2 / D-0082 §3 / D-0084-86).

* `_no_mcp_runtime_wired()` uses source-level introspection
  (`inspect.getsource`) on `eval_run` rather than a sentinel
  constant. Reason: a sentinel requires a second author to remember
  to bump it when the wiring lands; the source probe self-clears.

* Two-layer gate (T04.10 forward-deps + wiring probe) instead of
  `xfail`: the harness contract test board treats xfail as "we
  expect this broken" which would misrepresent the M2 → M3 wiring
  hand-off as a contract violation. Skip-with-remediation-message
  is the right semantic.

* Reverse-pin (`test_run_summary_rejects_inconsistent_kept_plus_skipped_flag`)
  guards against an orchestrator that miscounts under the skip
  scenario but still claims the flag is True. Cheap to write,
  catches a high-impact silent failure mode.

## Out of scope

* MCP-server probe semantics (OQ-5 deferral) — not relevant under
  `--no-mcp` because the gate's override path bypasses the probe.

* Skip-reason format normalisation across all SKIPPED shapes —
  TEST-014 only asserts the `--no-mcp` shape. A cross-cutting
  normalisation test (PTY + MCP + disk-budget skip shapes in one
  matrix) is a future TEST-015 candidate.

* Eval E8 (`mcp_server.serena`) — task description names only
  E1 / E2.1 / E2.2 / E2.3. The CapabilityGates pin
  (`test_capability_gates_no_mcp_flag_skips_every_mcp_capability`)
  covers serena indirectly through `_DEFAULT_CAPABILITY_SPECS`
  iteration so a serena-classification regression still trips
  TEST-014.

## Verification

```
$ uv run pytest tests/cli/eval/test_no_mcp_skip.py -v
...
======================== 11 passed, 1 skipped in 0.36s =========================
```

The single skip is the end-to-end CliRunner test, gated on missing
T04.10 forward-deps. Output captured at
`evidence/T05.26/pytest.log`.
