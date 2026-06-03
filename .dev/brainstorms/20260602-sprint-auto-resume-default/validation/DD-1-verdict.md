---
dd: DD-1
verdict: REFACTOR
confidence: 0.82
---

## Adversarial findings

DD-1's **decision** — derive the resume cursor from on-disk artifacts, add no new
heavyweight state store — is sound and should stand. DD-1's **written rationale** is
wrong on two verifiable facts and rests on a durability claim that the code does not
support. The fix is to correct the rationale and harden one algorithm clause; not to
add the breadcrumb file the alternative proposed (that is redundant — see below).

1. **"phase_start is written before a phase executes" is false for the single-process
   path.** `proc_manager.start()` spawns the subprocess at `executor.py:1331`, and
   `write_phase_start` runs only afterward at `executor.py:1335`. (It IS written before
   `execute_phase_tasks` on the per-task path: `executor.py:1267` precedes `:1270`.) So
   the ledger event does not strictly precede execution.

2. **"phase number always survives a crash" is false.** The JSONL writer
   (`logging_.py:265-267`) is a bare `open(..., "a"); f.write(json + "\n")` with NO
   `fsync`, NO `flush`, NO atomic rename, NO lock (grep of `logging_.py` + `executor.py`
   returns the lone `os.replace` at `executor.py:2072`, which belongs to result.json, not
   the ledger). A SIGKILL / OOM / power-loss between the `write()` and the kernel page
   flush can leave the last `phase_start` line absent or torn (non-JSON). The design's own
   §3 says the reader skips malformed lines — which means a torn `phase_start` is silently
   dropped, not recovered.

3. **The decision survives anyway — but for a reason the design does not state.** Phase
   recoverability does NOT actually depend on the torn-prone ledger line. `result.json` is
   written with atomic tmp+rename (`executor.py:2070-2072`, comment at `:2056-2057`
   explicitly: "so a crash mid-write never leaves a truncated phase-N-result.json"). The
   real durability anchor is result.json presence, which the planner already consults
   (§3 lines 110, 113, 116, 122). The breadcrumb alternative is therefore **redundant**:
   it duplicates a guarantee result.json already provides. This is why the verdict is
   REFACTOR (fix the story), not REJECT (the decision is fine) and not adopt-breadcrumb.

4. **Latent bug exposed (must-fix): a torn `phase_complete` line forces a needless re-run
   of an already-completed, non-idempotent phase.** §3 line 110 gates COMPLETED on
   `phase_complete` event AND result.json. If phase 2 finished (result.json written
   atomically) but its `phase_complete` ledger line is torn/lost, line 110 fails, the phase
   falls through to `else → PENDING` (line 114), and line 116 elects it as the interrupted
   phase to re-run. Because phases are non-idempotent (NG2), re-running a completed phase is
   exactly the hazard the whole feature exists to prevent. COMPLETED must key off the atomic
   result.json, with the ledger event as corroboration only.

5. **Concurrency caveat (medium, shared by both options):** `_resolve_release_dir`
   (`config.py:242-278`) derives the release dir deterministically from `index_path` with no
   PID/timestamp/lock. Two concurrent `sprint run <same index>` invocations append to the
   SAME `execution-log.jsonl` with no writer lock, interleaving `phase_start` events. The
   derive-only pairing loop ("starts where phase==p" / "closed where phase==p") can
   mis-associate interleaved events. FR-5 ambiguity detection must explicitly cover this, or
   the planner must tolerate duplicate/interleaved starts. A breadcrumb would not fix this
   either (last-write-wins races too), so it is not a point for the alternative — but it must
   be named in the design.

## Code verification (file:line)

- `logging_.py:59-69` `write_phase_start` — emits `phase_start` with `phase.number`. Confirmed.
- `logging_.py:71-87` `write_phase_interrupt` — balancing close event. Confirmed.
- `logging_.py:89-107` `write_phase_result` — emits `phase_complete`. Confirmed.
- `logging_.py:265-267` `_jsonl` — `open(..., "a"); f.write(json.dumps(...) + "\n")`. No
  fsync / flush / rename / lock. **This is the load-bearing refutation of "always survives."**
- `executor.py:1264-1267` per-task path: `write_phase_start` precedes `execute_phase_tasks`
  (:1270). Claim TRUE here.
- `executor.py:1330-1335` single-process path: `proc_manager.start()` (:1331) PRECEDES
  `write_phase_start` (:1335). Claim FALSE here.
- `executor.py:1488` `write_phase_interrupt` — only on `signal_handler.shutdown_requested`
  (graceful). Hard crash bypasses it → dangling `phase_start`. Confirmed.
- `executor.py:2070-2072` result.json `tmp.write_text(...)`; `tmp.replace(out)` — atomic.
  Confirmed; only `os.replace` in the module.
- `config.py:242-278` `_resolve_release_dir` — deterministic from index_path, no lock.
- design §3 lines 110/113/116/122 — COMPLETED requires `phase_complete` event; result.json
  used for boundary disposition. Gap in line 110 confirmed (torn-`phase_complete` → PENDING).

## Proposed spec changes

### Change 1 — DD-1 table cell (design.md line 23). Replace the EXACT existing text:

`| **DD-1** | Resume cursor: derive vs. new breadcrumb | **Derive-only. No new state file.** The JSONL log is already a *balanced-event ledger*: `phase_start` is written **before** a phase executes (`executor.py:1267,1335`), closed by either `phase_complete` (`logging_.py:89-107`) or `phase_interrupt` (`logging_.py:71-87`, emitted at `executor.py:1488`). A `phase_start` with **no** closing event = hard crash, and the phase number is still known. R2 downgrades from "unknown phase" to "known phase, unknown intra-phase progress" — handled by the integrity gate. | `logging_.py:59-107`, `executor.py:1267,1335,1488` |`

with:

`| **DD-1** | Resume cursor: derive vs. new breadcrumb | **Derive-only. No new state file.** Recovery rests on **two** on-disk signals, not the ledger alone: (a) `results/phase-N-result.json`, written **atomically** via tmp+rename (`executor.py:2070-2072`) so a crash never truncates it; (b) the `execution-log.jsonl` ledger (`phase_start` at phase entry — `executor.py:1267` per-task, and just after subprocess spawn at `:1335` single-process — closed by `phase_complete` `logging_.py:89-107` or `phase_interrupt` `logging_.py:71-87`@`executor.py:1488`). NOTE the ledger append (`logging_.py:265-267`) is non-atomic/non-durable (no fsync/rename), so a hard crash MAY torn or drop the last line; the planner therefore treats **result.json presence as the authoritative phase-completion signal** and the ledger as corroboration. A breadcrumb file is unnecessary because result.json already provides the atomic anchor. R2 downgrades to "known phase (from result.json), unknown intra-phase progress" — handled by the integrity gate. | `logging_.py:59-107,265-267`, `executor.py:1267,1335,1488,2070-2072` |`

### Change 2 — §3 COMPLETED classification (design.md line 110). Replace the EXACT existing text:

`     if phase_complete with PASS-family status AND results_dir/phase-p-result.json exists → COMPLETED`

with:

`     if results_dir/phase-p-result.json exists with PASS-family status → COMPLETED  (phase_complete event is corroboration, NOT required — a torn/dropped phase_complete line must not demote a phase whose atomic result.json proves completion)`

### Change 3 — §12 R2 line (design.md lines 321-322). Replace the EXACT existing text:

`- R2 (crash blind spot) **largely closed** by DD-1 — phase identity always survives; only
  intra-phase progress is unknown, which the gate handles.`

with:

`- R2 (crash blind spot) **largely closed** by DD-1 — phase identity is recovered from the
  atomically-written result.json (executor.py:2070-2072), NOT from the non-durable ledger
  append (logging_.py:265-267 has no fsync/rename, so the last phase_start may be torn/dropped
  on hard crash). Only intra-phase progress is unknown, which the gate handles. Residual
  concurrency caveat: `_resolve_release_dir` (config.py:242) is deterministic from index_path
  with no lock, so concurrent `sprint run <same index>` share one ledger; the planner's
  event-pairing must tolerate interleaved phase_start events or FR-5 must flag it as ambiguous.`
