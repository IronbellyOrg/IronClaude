---
dd: DD-5
verdict: REFACTOR
confidence: 0.95
---

## Adversarial findings

DD-5's **flag-name decision is sound and upheld**: `--fresh` canonical + `--restart` alias
is collision-free, the alias-to-one-dest pattern is natively expressible in Click (verified),
and the rationale for avoiding `--no-resume` as canonical is valid. `--yes` +
`SUPERCLAUDE_SPRINT_ASSUME_YES` is fine.

The **explicit-window detection mechanism is buggy** and must be refactored. The debate
resolved unanimously (Position B) on the single contested point, blocked by one HIGH-severity
invariant against Position A:

- **INV-001 / guard_conditions / HIGH / UNADDRESSED (kills Position A):** The guard
  `position_explicit = (start_phase != 1) or (end_phase != 0)` cannot distinguish an explicit
  `--start 1` from no flag at all — both produce `start_phase == 1`, so `start_phase != 1` is
  False and **auto-resume wrongly fires on an explicit `--start 1`**. This is a silent breach
  of FR-4.4 ("explicit `--start` disables auto-detect") and AC-7 ("Explicit `--start 4` ⇒
  auto-detect bypassed; behaves exactly as today" — the AC is written against `--start`, and
  `--start 1` is the most natural explicit "run from the top, don't resume" value a script
  passes). For a non-idempotent pipeline, a silent false-negative on the bypass guard is the
  worst failure mode (it layers new work instead of erroring). Telling users to "pass
  `--fresh` instead" does not satisfy an AC phrased against `--start`.

- **INV-002 / count_divergence / MEDIUM (Position A):** The `end_phase != 0` arm is a *safe*
  explicit signal in isolation (0 is out-of-range as a phase number, so no legitimate
  `--end 0` exists). But it only catches windows where the END was customized; bare
  `--start 1` or `--start 1 --end <last>` still slip through. The `or` does not rescue the
  `--start` arm.

- **INV-004 / sufficiency_challenge / HIGH / ADDRESSED (Position B):** Parameter-source
  detection greens AC-7 for the full input domain *only if* `run()` gains access to `ctx`.
  Verified: `run()` does not currently take `ctx`, so the fix MUST add `@click.pass_context`
  (one line, empirically verified working). The sentinel-default variant
  (`--start/--end default=None`) is an equally sufficient alternative needing no `ctx` and
  additionally unifies `run()` with the `rerun-tasks` convention (which already uses
  `default=None` for `--phase`/`--tasks`).

- **INV-003 / interaction_effects / LOW / ADDRESSED:** `--fresh`/`--restart` alias verified
  clean; no collision with the stale `--resume <task>`/`--budget` hint at `models.py:877`
  (that hint references options that do not exist on `run()` and is orthogonal to this
  decision — worth a separate cleanup but not blocking DD-5).

- **rerun-tasks side is already correct:** `--phase`/`--tasks` default to `None`
  (`commands.py:424,430`), so "absence" is detectable there. The asymmetry is the bug — only
  the `run()` side uses in-range value-comparison. Aligning `run()` to a sentinel/`None`
  convention removes the asymmetry.

Convergence: Position A carries one HIGH+UNADDRESSED invariant ⇒ convergence BLOCKED for A.
Position B has zero HIGH-UNADDRESSED items ⇒ base = Position B. Not REJECT (the decision's
core is sound); REFACTOR (fix the one buggy line + note the `ctx` requirement).

## Code verification (file:line)

- `src/superclaude/cli/sprint/commands.py:74-80` — `run()` `--start` option, `default=1`.
- `src/superclaude/cli/sprint/commands.py:81-87` — `run()` `--end` option, `default=0`.
- `src/superclaude/cli/sprint/commands.py:190-208` — `run()` signature; it does **NOT** take
  `ctx`/`@click.pass_context` today, so a parameter-source fix requires adding it.
- `src/superclaude/cli/sprint/commands.py:421-426` — `rerun-tasks` `--phase`, `default=None`.
- `src/superclaude/cli/sprint/commands.py:427-432` — `rerun-tasks` `--tasks`, `default=None`.
- `src/superclaude/cli/sprint/models.py:877` — stale `--resume <task_id> --budget` hint
  string referencing options absent from `run()` (orthogonal; flag for separate cleanup).
- Click 8.4.1 empirical check (`ctx.get_parameter_source`): no-flag ⇒ `DEFAULT`;
  `--start 1` ⇒ `COMMANDLINE`; `--start 4` ⇒ `COMMANDLINE`. `--fresh`/`--restart`
  alias-to-one-dest: both set the flag and both appear in `--help`. Confirms Position B is
  implementable and Position A's value-comparison is provably defective at value 1.

## Proposed spec changes

EXACT existing design.md text to replace (line 206):

```
position_explicit = (start_phase != 1) or (end_phase != 0)        # user supplied a window
```

EXACT replacement text:

```
# explicit-window detection MUST use Click parameter source, NOT value comparison:
# `--start 1` is a valid EXPLICIT window and must NOT be misread as "no flag" (FR-4.4/AC-7).
# `run()` therefore takes @click.pass_context; the value-comparison form is a known bug
# because `--start` default=1 (commands.py:78) makes `start_phase != 1` indistinguishable
# from an explicit `--start 1`.
src = ctx.get_parameter_source
position_explicit = src("start_phase") == ParameterSource.COMMANDLINE \
                 or src("end_phase")   == ParameterSource.COMMANDLINE   # user supplied a window
# Alt (no ctx): set --start/--end default=None (mirrors rerun-tasks --phase/--tasks),
# detect `is not None`, then map None→(1, last) at the load_sprint_config boundary.
```

Additionally, in the §0 DD-5 row, the clause "Explicit `--start/--end` (run) ... remain the
*positional* bypass" should be annotated so it does not get implemented as value-comparison.

EXACT existing design.md text to replace (line 27, within the DD-5 row):

```
Explicit `--start/--end` (run) and `--phase/--tasks` (rerun-tasks) remain the *positional* bypass.
```

EXACT replacement text:

```
Explicit `--start/--end` (run) and `--phase/--tasks` (rerun-tasks) remain the *positional* bypass — detected via Click `ParameterSource.COMMANDLINE` (run() takes `@click.pass_context`) or a `None` sentinel default, **never** by value comparison such as `start_phase != 1` (an explicit `--start 1` must still bypass auto-resume; FR-4.4/AC-7).
```
