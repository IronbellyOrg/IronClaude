# Position B — DD-5 with parameter-source detection

## Claim
- Keep `--fresh` canonical + `--restart` alias and the `--no-resume`-avoidance rationale
  (all of that is sound).
- REPLACE the value-comparison explicit-window detector with Click parameter-source
  detection:
  `position_explicit = ctx.get_parameter_source("start_phase") == ParameterSource.COMMANDLINE
   or ctx.get_parameter_source("end_phase") == ParameterSource.COMMANDLINE`
  (requires `@click.pass_context` on `run()`).
- Equivalent alternative: change `--start`/`--end` defaults to a sentinel (`default=None`)
  and detect `is not None`; then map None→(1, last) downstream. This mirrors what
  `rerun-tasks` already does (`--phase`/`--tasks` default=None).

## Strengths
- Correctly distinguishes explicit `--start 1` from no-flag, satisfying FR-4.4 / AC-7 for
  EVERY window value including the boundary value 1.
- `get_parameter_source` is a stable Click 8.x API; also returns `ENVIRONMENT` / `DEFAULT_MAP`,
  so env-var or config-file supplied windows are correctly treated as explicit too.
- Sentinel-default variant additionally unifies `run()` with the `rerun-tasks` convention
  (None == "not supplied"), reducing the asymmetry between the two subcommands.

## Cost
- `run()` must take `ctx` (add `@click.pass_context`) — a one-line, well-trodden change; OR
  the default sentinel approach touches the two option declarations + the None→value mapping
  at the `load_sprint_config` boundary.
