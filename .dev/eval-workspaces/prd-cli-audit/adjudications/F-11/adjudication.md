# F-11 Adjudication — PrdMonitor entirely dead code

**Mode**: /sc:adversarial Mode B (three personas → convergence)
**Source finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-11-prdmonitor-entirely-dead-code.md`
**Preliminary severity (Stage 2)**: HIGH
**Pattern tags**: P2 (knob defined, never consumed), P4 (dead code), P8

---

## Re-verification (read-only, cited)

### Public API of `PrdMonitor` (`src/superclaude/cli/prd/monitor.py:56-201`)

- `__init__` — `monitor.py:66-67` (constructs `PrdMonitorState`)
- `parse_line(line: str) -> None` — `monitor.py:69-98`
- `check_stall(threshold_seconds: float) -> bool` — `monitor.py:100-112`
- `get_state() -> PrdMonitorState` — `monitor.py:114-116`
- `reset() -> None` — `monitor.py:118-120`
- Private helpers `_extract_from_event` / `_extract_from_text` — `monitor.py:126-201`

### Call-site inventory (grep across `src/` + `tests/`)

- Only import: `executor.py:54` (`from .monitor import PrdMonitor`).
- Only instantiation: `executor.py:334` (`self._monitor = PrdMonitor()` inside `PrdExecutor.__init__`).
- Zero method calls on `self._monitor` anywhere in `src/superclaude/cli/prd/`. Verified by:
  - `grep -rn "PrdMonitor\|monitor\." src/superclaude/cli/prd/` returns only the import, the class definition, and the bare instantiation; no `self._monitor.parse_line`, `self._monitor.check_stall`, `self._monitor.get_state`, or `self._monitor.reset` anywhere.
  - `grep -rn "parse_line\|check_stall\b" src/ tests/` returns hits only inside `monitor.py` itself.
  - `grep -rn "PrdMonitor\b" tests/` returns **zero** results. No unit tests, no integration tests, no mocks cover this class. (The hits in `tests/sprint/test_monitor.py` and `tests/cli_portify/test_monitor.py` are for unrelated `sprint` / `cli_portify` monitors with different APIs — `start`, `stop`, `output_bytes` — not `parse_line`/`check_stall`.)
  - `tests/cli/prd/` directory contains 12 test files; none reference `PrdMonitor` (verified via `grep -n "PrdMonitor" tests/cli/prd/*.py` → empty).

### `executor.py:334` instance — is it ever exercised?

It is **constructed and then abandoned**. The subprocess loop in `_run_subprocess_step` (`executor.py:469-509`) takes the synchronous path:

1. Build `PrdClaudeProcess` with `timeout_seconds=self._config.stall_timeout * 30` (`executor.py:493-500`).
2. `proc.start_with_retry()` then `proc.wait()` (`executor.py:503-504`).
3. After `wait()` returns, `output_file.read_text(...)` (`executor.py:514`) reads the *complete* stdout dump.

No `for line in proc.stdout` loop. No threaded reader feeding `parse_line`. The instance held in `self._monitor` is referenced exactly once after construction: never.

### `stall_timeout` / `stall_action` consumers

- `grep -rn "stall_timeout\|stall_action" src/superclaude/cli/prd/` returns three lines:
  - `models.py:190` — definition `stall_timeout: int = 120`
  - `models.py:191` — definition `stall_action: str = "warn"`
  - `executor.py:499` — `timeout_seconds=self._config.stall_timeout * 30`
- `stall_action` has **zero** consumers anywhere — it is a pure dead knob.
- `stall_timeout` is consumed in exactly one place, and **not as a stall threshold**: `executor.py:499` multiplies it by 30 to derive the wall-clock subprocess kill timeout (120 × 30 = 3600 s = 1 hour). This is the semantic shift documented in `F-20-stall-timeout-semantic-shift.md` (cross-confirmed by file presence at `.dev/eval-workspaces/prd-cli-audit/findings/F-20-stall-timeout-semantic-shift.md:1`). There is **no** path that treats `stall_timeout` as the "max gap between events" threshold its name implies — because the only thing that could compute such a gap is `PrdMonitor.check_stall`, which is never called.

### Conclusion of re-verification

The finding's three core claims hold without qualification:

1. `PrdMonitor` is instantiated and never invoked (`executor.py:334` is the sole reference after `__init__`).
2. `stall_timeout` is misused as a wall-clock multiplier, not a stall threshold.
3. `stall_action` is entirely unwired.

Stdout streams to `{step_id}-output.txt` via Popen redirection (confirmed via `process.py:159` `output_format="stream-json"` plus `executor.py:504` blocking `proc.wait()` then `executor.py:514` post-mortem `read_text`). Nothing reads bytes line-by-line in real time.

---

## Persona 1 — Analyzer (reproducibility & user-visible behavior)

**Q: If the monitor is dead, how does the executor detect stalls?**

It does not detect stalls. The only safety net is the Popen watchdog inside `PrdClaudeProcess` (`process.py:140` `timeout_seconds: int = 3600`, enforced via the SIGTERM → 5 s → SIGKILL pattern documented at `process.py:10`). That watchdog fires only on **total elapsed wall-clock time**, not on output silence.

**Q: What happens during a long, slow-progress step?**

Two sub-cases:

- **Slow-but-progressing** (steady NDJSON, e.g., a long research step writing one line every 30 s): nothing bad, but the user gets zero mid-stream TUI updates — `tui.update_step` is called only on completion at `executor.py:455-459`. `PrdMonitorState` fields (`research_files_completed`, `current_artifact`, `events_received`, `output_bytes`) remain at their default zero values because `parse_line` is never invoked, so even if `tui.update_monitor_state` (`tui.py:189`) were wired, it would receive the empty initial state. The TUI is functionally a coarse-grained step-pass/fail indicator.

- **Hung subprocess** (Claude wedged, zero further output for hours): the documented `stall_timeout=120` config knob is the user's expectation per the finding's reproduction sketch. Actual behavior: silence until 3600 s, at which point the watchdog kills the process. That is **30× the user-expected stall ceiling** and 30× the documented default.

**Reproducibility verdict**: Trivially reproducible by static inspection — no subprocess required. The reproduction sketch in the finding (`F-11.md:32`) describes the observable symptom and the executor + process source code corroborate it without further evidence.

**User-visible symptoms**:

1. TUI has no mid-step liveness indicators (no byte counts, no current artifact, no research/synthesis file progress).
2. A genuinely hung step burns up to 1 hour of wall-clock before being killed, vs. the 2-minute expectation set by `stall_timeout=120`.
3. `stall_action="warn"` never produces a warning. The "warn" / "abort" / etc. semantic surface is documentation-only.
4. PRD-specific signals (`qa_verdict`, `fix_cycle_count`, `research_files_completed`) declared in `PrdMonitorState` (`models.py:291+`) are inert — the TUI cannot show progress on a 6-file research fan-out because the counter is never incremented.

---

## Persona 2 — Refactorer (blast radius)

**Shape match**: Identical pattern to F-03 (`_tier_min_lines` unwired), F-07 (`--where` stored, never consumed), F-22 (EXEMPT/LIGHT tiers not recognized). Each is "knob/code declared, no execution path reads it." F-11 is the *largest* instance by line count.

**Dead-code quantification**:

| Surface | Lines | Test coverage |
|---|---|---|
| `monitor.py` (whole module) | 201 (`wc -l src/superclaude/cli/prd/monitor.py`) | 0 tests reference `PrdMonitor` |
| `PrdMonitorState` consumers in `tui.py` | `tui.py:125, 189` (state field + setter `update_monitor_state`) — setter is also never called from `executor.py` | 0 |
| Config fields | `models.py:190-191` (`stall_timeout`, `stall_action`) | Field exists in `test_config.py` constructors but no behavioral test |
| Regex constants | `monitor.py:27-48` (8 compiled patterns) | 0 |

**Total dead lines attributable to F-11**: 201 (monitor.py) + ~5 (TUI integration stubs in `tui.py:125, 189-*`) + 2 config fields = **~208 lines of unreachable code plus the entire `PrdMonitorState` schema (`models.py:291+`) as an unused data model**.

**Compounding with F-20**: The `stall_timeout * 30` wall-clock derivation in `executor.py:499` is the *only* live consumer of the knob, and F-20 already classifies that as a semantic shift. The two findings are tightly coupled: fixing F-11 (wire the monitor) is the prerequisite for fixing F-20 (treat `stall_timeout` as a stall threshold rather than a wall-clock divisor).

**Blast radius assessment**: Large by code volume, contained by isolation. The dead code does not corrupt other systems — it simply does not run. Removing or wiring it is a localized change inside `prd/`. No cross-package import contamination (`monitor.py:8-10` explicitly forbids imports from `sprint`, `roadmap`, `executor`, `tui`).

---

## Persona 3 — Architect (severity calibration)

**Preliminary HIGH — challenge stance**: Is "stall detection apparatus is dead" *operationally* significant, or *theoretical*?

**Arguments for downgrading to MEDIUM**:

- The wall-clock watchdog (`process.py:140`, default 3600 s) does eventually bound runaway processes. A user is never *permanently* stuck.
- No evidence in the repo (no incident logs, no escalation notes) that production stalls have actually occurred at the 2-minute boundary.
- The TUI is a cosmetic surface, not a correctness surface. Lack of mid-stream updates is a UX degradation, not a data-integrity bug.
- `PrdMonitorState` is consumed by `tui.py` (`tui.py:125, 189`) but the TUI's contract for that state is "informational only" — there is no decision logic gated on monitor state.

**Arguments for sustaining HIGH**:

- **User-promised behavior**: the config field `stall_timeout: int = 120` (`models.py:190`) and `stall_action: str = "warn"` (`models.py:191`) are part of the public CLI surface (assuming they are user-tunable). They lie about what the system does. Users who set `--stall-timeout 60` to enforce a tight stall ceiling will get a 1800-s wall-clock watchdog and no stall detection. That is a **silent contract violation**, not a missing convenience.
- **Failure-mode coverage**: PRD pipelines invoke a long-running Claude subprocess per step (15 steps × up to 1 h each). A wedged Claude is a realistic failure mode (auth flap, network stall, model-side hang). Burning 1 h on a hung step before any signal vs. 120 s with the advertised behavior is a **30× MTTR regression** for that failure class.
- **Magnitude of dead surface**: 201 lines + entire state model + 8 regexes + config knobs is the largest single dead-code finding in this audit. Even if no single behavior is critical, the aggregate signals systemic decay of the "monitor → TUI → executor" feedback loop, which is what the PRD framework's NFR-PRD.5 ("Stall detection") promised.
- **Hides downstream signal extraction**: `qa_verdict` / `fix_cycle_count` / research/synthesis file counters are not just TUI sugar — they are the signals a future operator-control or auto-abort loop would need. With them dead, any future enhancement that wants to act on QA verdicts mid-pipeline has to rebuild this layer from scratch.

**Calibrated severity**: **HIGH sustained**. The "30× MTTR regression on hung-subprocess failures" + "config knobs lie to users about what they control" combination is more than cosmetic. It is not CRITICAL because the wall-clock watchdog prevents unbounded hangs and no data is lost or corrupted, but it is meaningfully worse than MEDIUM (cf. F-03 tier thresholds, also HIGH).

**Operational significance summary**: Theoretical risk in steady state, real risk on the worst-case-per-step failure mode that the system was explicitly designed to guard against (NFR-PRD.5).

---

## Convergence

**Verdict**: **CONFIRMED**. All three personas converge on the factual claim that `PrdMonitor` is dead code and `stall_timeout` / `stall_action` are unwired knobs. Re-verification shows zero counter-evidence; `executor.py:334` instantiation is the sole reference and no method on the instance is ever called.

**Convergence score**: **0.97**. The only minor divergence is severity calibration (Architect entertained MEDIUM); on full inspection, all three personas land on HIGH. No persona disputed reproducibility, blast radius, or the factual mapping.

**Final severity**: **HIGH** (sustained from Stage 2 preliminary).

Justification:
- Silent contract violation on a user-facing config knob (`stall_timeout`, `stall_action`).
- 30× MTTR regression on the failure mode the monitor was designed to catch.
- Largest dead-code surface in the audit (~208 lines + state schema + regex bank).
- Tightly coupled with F-20 (the only live consumer is itself a misuse).
- Not CRITICAL because the wall-clock watchdog at `process.py:140` provides a hard upper bound and there is no data-corruption path.

**Fix difficulty**: **MEDIUM**.

The fix has two viable shapes:

1. **Wire it** (preferred, restores promised behavior): Replace the blocking `proc.wait()` at `executor.py:504` with a line-iterating reader thread (or direct `for line in proc.stdout` loop after switching `PrdClaudeProcess` to expose a line iterator). Feed each line to `self._monitor.parse_line`. Add a periodic `self._monitor.check_stall(self._config.stall_timeout)` poll, and on True, dispatch by `self._config.stall_action` ("warn" / "abort"). Push `self._monitor.get_state()` into `self._tui.update_monitor_state` on a timer.
   - Effort: ~1 day. Touches `executor.py` (subprocess loop), `process.py` (expose stdout iterator), `tui.py` (timer thread), and `models.py` (validate `stall_action` enum).
   - Risk: introduces a reader thread / async edge in a module that explicitly forbids `async def` (`monitor.py:8` NFR-PRD.1); must be done with a plain `threading.Thread` or a `select`-based loop.

2. **Delete it** (faster, accepts the regression): Remove `monitor.py`, the `_monitor` field at `executor.py:334`, and the `stall_timeout` / `stall_action` config fields. Rename or repurpose the `stall_timeout * 30` derivation at `executor.py:499` to a properly named `subprocess_timeout_seconds` config field. Resolves F-11 + F-20 together by elimination.
   - Effort: ~2 hours. Pure deletion plus one rename.
   - Risk: locks in the "no mid-stream signal" UX as the long-term design. Any future TUI liveness work will have to rebuild.

The choice between (1) and (2) is a product decision, not a technical one. Either eliminates the silent-lie surface that drives the HIGH severity. (2) also closes F-20 as a side effect. Recommended for triage: bundle F-11 + F-20 as a single workstream.

**Synthesis**:

`PrdMonitor` is the canonical example of "code shipped before its integration." The class is internally well-formed (sensible API, defensive regex extraction, NFR-PRD.5-aligned `check_stall`), but the executor never calls into it. The instantiation at `executor.py:334` reads as an incomplete plumbing exercise — the constructor call is in place where one would expect to find a reader thread or callback registration, but neither was wired. The downstream consequence is a **30× drift between documented and actual stall behavior** (`stall_timeout=120` advertised, ~3600 s wall-clock enforced), plus a fully cosmetic TUI for the longest-running steps in the pipeline. Severity HIGH is sustained because the gap between documented and observed behavior is large and the failure mode (wedged subprocess) is realistic for the workload. Fix difficulty is MEDIUM because either wiring (~1 day, moderate cross-module surgery) or deletion (~2 hours, closes F-20 too) is tractable; neither requires architecture-level rework. The finding should be remediated in tandem with F-20.
