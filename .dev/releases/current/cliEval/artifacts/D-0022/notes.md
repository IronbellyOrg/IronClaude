# D-0022 — Implementation notes

**Task:** T01.26 (Phase 1, Roadmap FR-G3 / R-022)

## Observation

The `eval` group registration (`main.add_command(eval_group, name="eval")`)
was already present in `src/superclaude/cli/main.py:393-395` because
earlier M1 tasks (T01.13 doctor, T01.21 list, T01.22 describe) needed a
mounted group to expose their subcommands via the CLI for manual smoke
validation. T01.26 therefore *validates* the additive contract rather
than introducing the wire-up from scratch.

## What this task added

- `tests/cli/test_cli_registration.py` — 5 regression tests pinning:
  - top-level help mentions `eval`,
  - top-level command roster is the expected fixed set (snapshot),
  - `eval --help` lists the M1 subcommands,
  - `eval_group` exposes the M1 subcommands at the Click registry level
    (not just in help text),
  - every pre-existing top-level command's `--help` still exits 0.

- This artifact set documents the additive wiring and the AC mapping
  table.

## Why a snapshot test for the top-level roster

FR-G3 says "no impact on existing commands". A literal interpretation
(no renamed/removed pre-existing commands) is captured by the frozen
`EXPECTED_TOP_LEVEL_COMMANDS` set. The test fails loudly on either
direction of drift (missing or unexpected), forcing any future top-level
addition to be a deliberate edit to the expected set rather than a
silent slip. The set lives in the test file (not in `main.py`) so it is
read-only from the CLI's perspective.

## Subcommand floor vs ceiling

The test asserts the *floor* of M1 subcommands (`describe`, `doctor`,
`list`) rather than the exact set under `eval_group`. M4 will add
`run` (FR-CLI1) and later tasks may add helpers; asserting an exact set
would force a churn-only test update each time. Per FR-G3 AC bullet 2,
"additional subcommands land per their milestones".

## Risks / open questions

None. The change is additive at the test layer only; the production
wiring is unchanged from the state at HEAD before T01.26.
