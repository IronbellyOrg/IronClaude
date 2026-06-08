# Position A — DD-5 as written in design.md

## Claim
- Opt-out flag: `--fresh` canonical, `--restart` alias. Defined as "ignore prior on-disk
  state; run from phase 1 with auto-detect disabled."
- Explicit-window bypass detection (design.md §6, line 206):
  `position_explicit = (start_phase != 1) or (end_phase != 0)`
- Avoid `--no-resume` as canonical because Click would imply a `--resume` toggle that does
  not fit a default-on feature.
- `--yes` non-interactive assent, also honored via `SUPERCLAUDE_SPRINT_ASSUME_YES=1`.

## Strengths
- `--fresh`/`--restart` naming is clean, collision-free in the sprint surface, and the
  alias-to-one-dest pattern is natively expressible in Click.
- Value-comparison is zero-dependency: no need to thread `ctx` into `run()`.
- Matches today's existing defaults (`--start` default=1, `--end` default=0) without
  changing any option signatures.

## Known weak point (conceded)
- The value comparison `start_phase != 1` cannot distinguish a user who typed `--start 1`
  explicitly from a user who passed nothing. Both yield `start_phase == 1`.
