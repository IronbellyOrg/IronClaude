# HC1 — Runtime entrypoint card

- Production boundary: the real `src/superclaude/skills/ccsession-tag/ccsession --shim` launch (setup_shim, ccsession:752-830) starting the real `local-gateway-alias-proxy.py`, followed by the event that killed the field shims: a terminal kill that SIGTERMs then SIGKILLs every descendant of the terminal's root (Orca pty sweep, behaviour-definitions.md row 1).
- Replay 1 (live check): live-check/orca_close_repro.py — real ccsession, fake `claude` (`exec sleep 300`), own session, free port, stand-in gateway with a paused stream, sweep of the root's descendants.
- Replay 2 (regression test, to be added): tests/unit/test_ccsession_tiers.py, same shape with the existing StandInGateway and `pause-stream`.
- Forbidden interpretations and their negative witnesses:
  1. "The shim survives because it was started directly by a test" — forbidden: the replay must go through `ccsession` (not the `shim` fixture).
  2. "The shim survives because the sweep missed it by accident" — the replay asserts the shim pid is NOT among the terminal root's descendants after launch, and that its session differs from the terminal's.
  3. "The stream finished because the gateway finished early" — the stream must still be paused when the sweep runs (sweep at 1.5 s, pause 5 s) and must end with `message_stop`.
- Negative witness (fix reverted = HEAD f90877be): observed FAIL — live-check/before.txt: `shim is a descendant of the terminal: True`, `stream finished: False`, port refused.
- Positive witness: pending implementation (live-check/after.txt and the regression test result).
- Positive witness, observed after implementation (2026-11-02T04:39Z): PASS.
  - live-check/after.txt (replay 1 through the real changed ccsession): `shim is a descendant of the terminal: False`, `stream finished: True`, `port after close: answers`.
  - Replay 2 is `tests/unit/test_ccsession_tiers.py::test_shim_outlives_the_terminal_that_started_it`. It asserts the shim is not a descendant, that its session differs from the terminal's (`os.getsid`), that the reply ends with `message_stop`, and that the pid is unchanged. It fails at HEAD and passes with the fix (`.dev/tasks/<to-do|done>/TASK-WF-detachTheCcsessi-20261102-034618/artifacts/t1-before.log` and `t4-tests.log`).
  - Replay 2 adapts forbidden interpretation 3: it sweeps at 1 s against a 4 s pause, so the stream is still paused when the sweep runs.
