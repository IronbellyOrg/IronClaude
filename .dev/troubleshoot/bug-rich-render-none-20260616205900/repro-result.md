# Empirical repro result — INCONCLUSIVE (did not reproduce)

**Command:** `MODE={unsafe,fixed} ITERS=20000 uv run python repro/boundary_fork_repro.py`
**Date:** 2026-06-17

| Mode | Code path | Predicted (by both cards) | **Actual** | Exit |
|------|-----------|---------------------------|-----------|------|
| `unsafe` | `preexec_fn=os.setpgrp` | SIGSEGV / TypeError / deadlock | **SURVIVED 20000 spawns / 67k summarizer forks in 42.6s** | **0** |
| `fixed` | `start_new_session=True` | SURVIVED | SURVIVED 20000 spawns in 22.6s | 0 |

## Honest interpretation

**The repro failed to reproduce the bug — and critically, the UNSAFE mode did NOT crash.** This is the falsification criterion both hypothesis cards named, and it came back **negative for their prediction**. Consequences:

1. The empirical test **does NOT confirm** the unsafe-fork root cause (H-A). It is **not** the "strongest validation" I billed it as — it is a non-result.
2. It does **not** cleanly **refute** H-A either: the harness is a weak model of the real failure —
   - child is `/bin/true` (instant exit, ~zero allocation) vs. the real `claude` subprocess (runs minutes, heavy malloc);
   - renderable is a 2-row table vs. the real nested Panel/Table whose buffer reached **index 139**;
   - real crash appeared after a **~27-minute** run, not 42s;
   - environment/timing (glibc arena count, core count, load) differ.
   Non-reproduction in a simplified harness is weak evidence, but it removes the empirical leg the diagnosis was leaning on.
3. **Net effect on confidence:** the diagnosis drops from "high (0.86)" to **"plausible but unconfirmed."** `preexec_fn=os.setpgrp` remains a genuine, documented latent hazard worth fixing regardless — but I can no longer claim it is *proven* to be the cause of THIS specific Thread-1 `TypeError`.

## What a faithful repro would need (to actually settle it)
- A child that allocates/holds the arena lock for a non-trivial window (not `/bin/true`).
- A renderable large enough to produce a multi-hundred-segment buffer (match the index-139 scale).
- Longer runtime / more iterations, ideally on the same host class as the original crash.
- Or: capture a `faulthandler`/core dump from the REAL runner when it next crashes (add `faulthandler.enable()` + `PYTHONFAULTHANDLER=1` to the sprint entrypoint) — direct evidence beats any synthetic repro.
