# D-0071 — Implementation notes

## Why this task was documentation-only

By the time T04.09 was reached the surface it pins was already
in place:

* `eval_group` itself shipped at T01.26 / FR-G3 alongside the
  top-level `main.add_command(eval_group, name="eval")` line.
* `doctor`, `list`, and `describe` shipped at T01.13, T01.21, and
  T01.22 respectively, each bolting onto `eval_group` via
  `@eval_group.command(...)`.
* `run` shipped at T04.10 with its 12 flags. The T04.09 acceptance
  bullets only require `run` to be **reachable** (its `--help`
  resolves); the body verification is T04.10's responsibility.

So at T04.09 there was nothing to add to `commands.py` and nothing to
add to `main.py`. The deliverable for this task is the test harness
in `tests/cli/eval/test_eval_group.py` that pins the four-subcommand
surface against future regressions, plus the artifacts under
`D-0071/`.

## Decisions

1. **Assert on the sorted set, not registration order.** Click
   `--help` rendering sorts subcommands lexicographically, so
   asserting `set(eval_group.commands) == {"describe", "doctor",
   "list", "run"}` keeps the test resilient to source-file
   reorderings. Source-order changes are routine (e.g. inserting a
   new helper between two `@eval_group.command(...)` blocks); the
   surface contract is what callers depend on.

2. **Pin the entry-point reachability with a second test path.**
   `test_top_level_main_lists_eval_group` invokes `main, ["--help"]`
   and asserts the word `eval` appears. This is the FR-G3 /
   T01.26 surface — distinct from the group's own `--help` — and is
   what regresses when somebody drops the `main.add_command(...)`
   line. `test_eval_invoked_through_main_lists_subcommands` then
   asserts dispatch through the entry point reaches the group
   surface (i.e. `superclaude eval --help` shows all four
   subcommands), which catches the case where `add_command` is
   present but the group object is replaced with something missing
   subcommands.

3. **Defer `run` body verification to T04.10.** T04.09 only asserts
   `eval run --help` resolves (exit 0) and the word `run` appears in
   the output. The 12-flag surface, exit-code mapping, and
   RunOrchestrator wiring are all T04.10 / D-0072 territory.

## Deferred follow-ups

* None. The registration is final; future subcommands (if any) would
  ship under their own roadmap items and append to this test file.

## Risk notes

* **Click version drift.** Click 8.x is the only supported series for
  the CLI. The tests use `click.testing.CliRunner` which has been
  stable across 7.x → 8.x; no version pin is required at the test
  level beyond the project-wide `pyproject.toml` dependency.

* **Entry-point regression surface.** The single line
  `main.add_command(eval_group, name="eval")` is the only thing
  separating "eval is reachable" from "eval is unreachable". The two
  entry-point tests (`test_top_level_main_lists_eval_group` and
  `test_eval_invoked_through_main_lists_subcommands`) catch deletions
  of that line and any future refactor that replaces it.
