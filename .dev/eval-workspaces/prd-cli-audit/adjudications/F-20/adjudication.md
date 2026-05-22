# Adjudication: F-20 -- Stall timeout semantic shift

**Mode**: /sc:adversarial Mode B (3 personas -> convergence)
**Status**: READ-ONLY adjudication
**Preliminary severity**: MEDIUM
**Source finding**: `.dev/eval-workspaces/prd-cli-audit/findings/F-20-stall-timeout-semantic-shift.md`

---

## Re-verification

### V1. `src/superclaude/cli/prd/executor.py:499`

```python
499:            timeout_seconds=self._config.stall_timeout * 30,
```

Confirmed verbatim. `PrdClaudeProcess` is instantiated with `timeout_seconds` derived as `stall_timeout * 30`. The kwarg name in `PrdClaudeProcess.__init__` (`process.py:140`) is `timeout_seconds: int = 3600` -- i.e. the receiving parameter is a **wall-clock** subprocess timeout, not a stall-detection cadence.

Numeric coincidence: default `stall_timeout=120` * 30 = 3600s, which is the *exact* default value of the `timeout_seconds` parameter at `process.py:140`. This is strong evidence the `* 30` multiplier was reverse-engineered to preserve a 1-hour wall-clock budget while reusing the misnamed config field, rather than being any kind of intentional scaling.

### V2. `src/superclaude/cli/prd/models.py:190-191`

```python
189:    max_turns: int = 300
190:    stall_timeout: int = 120
191:    stall_action: str = "warn"
```

No docstring, no inline comment. The field name `stall_timeout` and the adjacent `stall_action: str = "warn"` collectively imply "kill or warn when subprocess stalls for N seconds with no output" -- standard stall-watchdog semantics consistent with `cli/sprint/` and `cli/cli_portify/` usage of identically named fields:

- `sprint/executor.py:1407-1408`: `config.stall_timeout > 0 and ms.stall_seconds > config.stall_timeout` -- true stall semantics.
- `cli_portify/config.py:76`: `"stall_timeout: Seconds before stall detection triggers."` -- documented as stall.
- `cleanup_audit/executor.py:102-103`: `config.stall_timeout and state.stall_seconds > config.stall_timeout` -- true stall semantics.

The PRD module is the **only** consumer in the repo that repurposes `stall_timeout` as a wall-clock multiplier base.

### V3. CLI help text

```
grep -n "stall\|timeout" src/superclaude/cli/prd/commands.py  -> (no output)
```

There is **no PRD CLI flag** exposing `stall_timeout`. The field is only settable via the dataclass default or programmatic construction. User-visible documentation surface is limited to the field name itself (and any downstream docs that reference it).

### V4. Cross-reference with F-11

F-11 (HIGH, confidence 0.98) establishes that `PrdMonitor` is instantiated at `executor.py:334` and never invoked again. Specifically:

- `parse_line`, `check_stall`, `reset`, `get_state` -> zero call sites.
- No stall detection path runs at all.
- `stall_action` (warn|halt) is dead.

Combined user-facing reality: the only behavior `stall_timeout` actually drives is the 30x-scaled wall-clock kill in `executor.py:499`. Stall detection -- the behavior the name advertises -- does not exist. F-20 is the *naming* defect; F-11 is the *missing behavior* defect. They are coupled.

---

## Persona 1: Analyzer -- Reproducibility

**Scenario**: User reads `models.py:190`, sees `stall_timeout: int = 120`, and infers "subprocess gets killed if it produces no output for 120 seconds." User sets `stall_timeout=30` to tighten stall detection.

**What actually happens**:
1. `PrdMonitor` is created (executor.py:334) but never consulted -- per F-11.
2. `PrdClaudeProcess` is launched with `timeout_seconds = 30 * 30 = 900` (executor.py:499).
3. The underlying `ClaudeProcess` watchdog (inherited from `pipeline/process.py`) fires SIGTERM at 900s wall-clock, regardless of whether output is flowing.
4. A subprocess streaming output continuously for 16 minutes is killed despite never stalling.
5. A subprocess silent for 5 minutes is **not** killed, despite massively exceeding the user's 30s threshold.

**Symmetric case**: User raises `stall_timeout=600` thinking "tolerate up to 10 minutes of quiet" -> every step's wall-clock cap silently becomes 5 hours. A genuinely hung subprocess sits unkilled for 5 hours.

**Reproducibility verdict**: **Fully reproducible** by inspection. Behavior is deterministic and the semantic divergence is observable in unit-test scope (mock `PrdClaudeProcess`, assert `timeout_seconds == config.stall_timeout * 30`). No flakiness, no environmental dependencies.

**Analyzer score**: Confirmed. Both directions of the misconfiguration (tighten -> over-kill; loosen -> under-kill) reproduce trivially.

---

## Persona 2: Refactorer -- Blast radius

**Same-shape findings in this audit**:

- **F-11** (monitor unused): same field, opposite end of the wire. Fix for F-11 either (a) wires the monitor properly so `stall_timeout` means what it says, or (b) deletes monitor + renames `stall_timeout` -> `subprocess_timeout`. Either way **the fix must traverse F-20**. Bundling is not just convenient, it is required for coherence.

**Other repurposed knobs in PRD module** (grep audit):

- `stall_action: str = "warn"` (models.py:191) -- read by nothing. Pure dead config (P2). Should be removed in the same change.
- `max_turns: int = 300` (models.py:189) -- correctly threaded to `process.py:155`. Not repurposed.
- `max_research_fix_cycles`, `max_synthesis_fix_cycles`, `research_partition_threshold`, `synthesis_partition_threshold` -- need separate verification but out of F-20 scope.

**Cross-module consistency**: `sprint/`, `cli_portify/`, `cleanup_audit/` all use `stall_timeout` with true stall semantics. PRD is the **only** outlier. Fixing PRD aligns it with the rest of the codebase rather than introducing divergence.

**Bundle recommendation**: F-20 + F-11 + `stall_action` removal -> single PR. The three are inseparable: monitor (F-11) is the *behavior*, `stall_timeout` (F-20) is the *name*, `stall_action` is the *vestigial policy knob*. Splitting them yields incoherent intermediate states (e.g., wire the monitor but keep the 30x multiplier; or rename the field but leave the dead monitor).

**Blast radius**: Low. Two files (`executor.py`, `models.py`), one config schema field rename/replace, one constructor-call change. No public API surface (no CLI flag) so no user-facing migration is required beyond changelog mention.

**Refactorer score**: Bundle for fix. Blast radius small. Blocks F-11 resolution.

---

## Persona 3: Architect -- Severity calibration

**Preliminary**: MEDIUM. Argument for calibration:

**Arguments to hold MEDIUM**:
- User-facing config field whose name actively misleads (P7: misleading naming).
- Magic multiplier (`* 30`) with no documentation, no constant name (P4).
- Coupled with F-11 (HIGH), the actual user impact is "stall protection silently absent" -- but that impact is already attributed to F-11.
- No CLI flag exposes the knob, so the misleading-naming blast radius is bounded to developers reading source / docs, not end users tuning flags.
- Reproducible misconfiguration in both directions, but the *consequences* are bounded by either pipeline budget (over-kill) or wall-clock (under-kill at 5h ceiling). No data corruption, no security implication, no cost amplification beyond the 30x factor itself.

**Arguments to escalate to HIGH**:
- Naming is "actively misleading" not merely "ambiguous." A maintainer touching the file would reasonably assume stall semantics -- a non-trivial cognitive trap.
- The 30x multiplier is undocumented anywhere -- not in models.py, not in executor.py, not in process.py. A reader would need to trace three files to discover it.
- Sets a P8 anti-pattern precedent (silent semantic reuse of a typed field) which, if propagated, compounds.

**Arguments to de-escalate to LOW**:
- No CLI surface -> no immediate user-facing knob to misconfigure today.
- Fix is mechanical (rename + drop multiplier or wire monitor) once F-11 is resolved.
- Behavior is "wrong label" rather than "wrong action" in the narrow sense -- the wall-clock kill itself works.

**Architect verdict**: **Hold MEDIUM**. The de-escalation arguments are weakened by F-11 coupling (the *combination* is what bites users), and the escalation arguments are weakened by the absence of a CLI flag. MEDIUM correctly captures "UX defect, fix bundled with HIGH F-11, no independent emergency."

---

## Convergence

| Dimension | Result |
|---|---|
| **Verdict** | CONFIRMED -- defect is real, reproducible, and correctly characterized. |
| **Convergence score** | 0.95 (Analyzer: confirmed; Refactorer: bundle confirmed; Architect: severity confirmed at MEDIUM with explicit calibration argument). |
| **Final severity** | **MEDIUM** (unchanged from preliminary). |
| **Fix difficulty** | **LOW**. Single PR. ~5-10 LOC across `executor.py:499`, `models.py:190-191`. Coupled to F-11 fix but does not extend it materially. |
| **Pattern tags** | P2 (dead config: `stall_action`), P4 (magic multiplier `* 30`), P7 (misleading naming), P8 (silent semantic reuse). |
| **Bundle with** | F-11. The two findings are operationally inseparable. |

## Synthesis

F-20 is a genuine UX/maintainability defect with a clean reproduction path and a small fix. The misnamed field (`stall_timeout` used as `wall_clock_base * 30`) combines with F-11 (monitor unwired) to silently strip stall-detection behavior from the PRD pipeline while preserving the appearance of a stall knob. Either resolution path is acceptable:

- **Path A (preserve behavior, fix name)**: Rename `stall_timeout` -> `subprocess_timeout_seconds`, drop the `* 30` multiplier, set default to `3600`, delete `stall_action`. F-11 then becomes a separate decision about whether to add stall detection at all.
- **Path B (preserve name, fix behavior)**: Wire `PrdMonitor` (per F-11), make `stall_timeout` mean true stall-detection cadence, add a *new* `subprocess_timeout_seconds` field for the wall-clock cap. This re-aligns PRD with `sprint/` / `cli_portify/` / `cleanup_audit/`.

Path B is the architecturally consistent option (aligns with the rest of the repo) and addresses F-11 directly. Path A is the minimal-change option if the team decides PRD genuinely doesn't need stall detection.

Either way: **F-20 and F-11 ship in one PR**.

## Citations

- `src/superclaude/cli/prd/executor.py:499` -- `timeout_seconds=self._config.stall_timeout * 30`
- `src/superclaude/cli/prd/executor.py:334` -- `self._monitor = PrdMonitor()` (only PrdMonitor reference; per F-11)
- `src/superclaude/cli/prd/models.py:189-191` -- `max_turns`, `stall_timeout`, `stall_action` defaults
- `src/superclaude/cli/prd/process.py:140` -- `timeout_seconds: int = 3600` (kwarg name confirms wall-clock semantics; default equals 120 * 30)
- `src/superclaude/cli/prd/process.py:158` -- `timeout_seconds=timeout_seconds` (propagated to base `ClaudeProcess`)
- `src/superclaude/cli/sprint/executor.py:1407-1408` -- true stall semantics in sprint module
- `src/superclaude/cli/cli_portify/config.py:76` -- documented stall semantics (`"Seconds before stall detection triggers."`)
- `src/superclaude/cli/cleanup_audit/executor.py:102-103` -- true stall semantics in cleanup_audit module
- `src/superclaude/cli/prd/commands.py` -- grep `stall|timeout` returns no matches (no CLI flag exposure)
