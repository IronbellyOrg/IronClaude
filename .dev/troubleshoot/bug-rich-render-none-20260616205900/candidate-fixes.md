# Candidate Fixes Index

| Fix | Proposed by | Verdict | Confidence |
|-----|-------------|---------|------------|
| Replace `preexec_fn=os.setpgrp` with `start_new_session=True` (process.py:189-190) | root-cause-analyst (`afe966873b7470410`) AND python-expert (`a8821c2d8fa598ac9`) | **CONSENSUS** | 0.74 / 0.88 |
| Defensive `str()` coercion in TUI rendering | (raised as alternative, not primary) | rejected as primary; OK only as belt-and-suspenders alongside the fork fix | — |
| Pause/stop Live display during spawn | (raised as alternative) | rejected — doesn't address root cause | — |

**Why no Wave-4 adversarial debate:** both viable agents independently converged on the *identical* root fix. Per the protocol, `sc:adversarial` is invoked only when ≥2 *competing* strong fixes exist; on consensus it is skipped (debating one proposal against itself wastes tokens). This is a spec-correct skip, not an omission.

## Root-cause hypotheses weighed (the "debate")

The debate was over **root cause**, conducted independently inside each agent (not as a Wave-4 transcript):

| Hypothesis | Claim | Disposition | Who rejected it & why |
|-----------|-------|-------------|------------------------|
| **H-A** unsafe-fork corruption | `preexec_fn=os.setpgrp` runs Python between fork/exec in a multithreaded proc → heap/lock corruption; the None is a corrupted str seen by the Rich thread | **ACCEPTED** | both agents, + orchestrator code audit |
| **H-B** genuine None-leak in TUI | some TUI value reaches a Rich segment as None | **REJECTED** | both agents: every `tui.py` helper + `MonitorState` property returns `str` on every branch (verified file:line) — no path emits None |
| **H-C** plain Rich threading race | `live.update()` vs refresh thread race, no corruption | **REJECTED** | both agents: Rich serializes update/refresh internally; a benign race yields a stale frame, not a NoneType inside `_render_buffer`; cannot explain the co-occurring `stalled >300s` fork-deadlock signature |

**Discriminator that would falsify H-A in favor of H-C:** run `repro/boundary_fork_repro.py` — if `MODE=fixed` (start_new_session) still throws the TypeError, the cause is Rich concurrency, not fork safety. Not yet executed (offered as next step).
