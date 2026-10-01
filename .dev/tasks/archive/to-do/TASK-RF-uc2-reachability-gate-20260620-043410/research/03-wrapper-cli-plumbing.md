# Research 03 — Wrapper CLI Plumbing

Status: Complete

## Summary

Wrapper plumbing is a required FR-RH1 implementation surface: `superclaude reflect run` must carry a default-enabled reachability setting from Click, through `resolve_config()` / `ReflectConfig`, through tmux forwarding, and into `ReflectRunner._build_prompt()` as `--no-reachability` exactly once when disabled. The docs parity and help tests must be updated in lockstep so the CLI surface and guide cannot drift.

## Gaps and Questions

None blocking. The wrapper research intentionally covers Python CLI plumbing only; slash-command documentation is covered separately by `06-slash-command-reflect-source.md`.

Scope: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py`, `config.py`, `models.py`, `runner.py`; `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/docs/guides/reflect-cli-tools-guide.md`; `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_docs_cli_parity.py` and nearby wrapper tests.

## Findings

### Current CLI flag plumbing shape

- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:76` defines the `reflect run` Click command and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:81` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:147` list the current option decorators. There is no `--reachability` / `--no-reachability` option in that option block.
- Existing default-enabled boolean precedent: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:90` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:94` use a Click flag-pair (`--promote/--no-promote`) with `default=True` and a named parameter `promote`.
- The `run()` signature currently receives all Click option values at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:148` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:162`, then forwards them to `resolve_config()` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:175` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:189`. A reachability flag must be added in all three places: Click decorator, function parameter, and `resolve_config(..., reachability=reachability)` call.
- Tmux is a second wrapper-to-wrapper forwarding path: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:279` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:308` build the inner foreground `superclaude reflect run` command. It already forwards default-sensitive booleans explicitly for `promote` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:295` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:299`. Because reachability is default-enabled, an outer `--tmux --no-reachability` call must also forward `--no-reachability` explicitly; otherwise the inner command will revert to enabled.

### Config/model integration points

- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/models.py:57` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/models.py:86` define `ReflectConfig`. New wrapper state belongs here as a `bool` field, consumed by `ReflectRunner`.
- `resolve_config()` is defined at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/config.py:123` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/config.py:142`. It currently has wrapper-side boolean defaults for `promote`, `allow_single_vendor`, `tmux`, `dry_run`, `print_command`, `resume`, and `fix` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/config.py:132` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/config.py:141`.
- `resolve_config()` returns `ReflectConfig(...)` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/config.py:220` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/config.py:240`. A reachability parameter must be assigned into this constructor.
- Default caution: Click `promote` defaults to enabled in `commands.py` (`default=True` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:90` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py:94`), but `resolve_config()` still defaults `promote=False` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/config.py:132`. Do not copy that mismatch for reachability: direct wrapper tests call `resolve_config()` via helpers, so a default-enabled reachability setting should use `reachability: bool = True` in `resolve_config()` as well as `default=True` in Click.

### Prompt forwarding point

- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/runner.py:341` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/runner.py:366` compose the `/sc:reflect` prompt. This is the exact place to forward `--no-reachability` to the skill when disabled.
- Existing negative-only prompt precedent: `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/runner.py:345` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/runner.py:347` append `--no-promote` only when `config.promote` is false. Reachability should mirror this shape: append `--no-reachability` only when `not config.reachability`; do not append a positive `--reachability` to the `/sc:reflect` prompt.
- `_audit_once()` passes exactly the prompt produced by `_build_prompt()` to the child `ClaudeProcess` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/runner.py:405` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/runner.py:417`. Therefore a `_build_prompt()` unit test is sufficient to prove slash-prompt forwarding; an E2E launch test can additionally assert the child prompt if desired.

### Docs parity constraints

- The guide's Key options block starts at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/docs/guides/reflect-cli-tools-guide.md:105`; it claims the exact option set and defaults are read from `commands.py` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/docs/guides/reflect-cli-tools-guide.md:107` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/docs/guides/reflect-cli-tools-guide.md:108`.
- Current documented option bullets run from `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/docs/guides/reflect-cli-tools-guide.md:110` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/docs/guides/reflect-cli-tools-guide.md:137`. There is no reachability bullet in that block.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_docs_cli_parity.py:59` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_docs_cli_parity.py:66` extract only the `### Key options` section, and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_docs_cli_parity.py:69` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_docs_cli_parity.py:80` count only option-definition bullet lines starting with ``- `--``. The reachability documentation must therefore be a Key options bullet beginning with ``- `--reachability` / `--no-reachability` `` (or equivalent that starts with ``- `--``), not only prose elsewhere.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_docs_cli_parity.py:83` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_docs_cli_parity.py:92` require the documented long flag set to equal the Click long flag set. Adding a Click flag-pair without adding both long flags to the Key options bullet will fail this test.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_docs_cli_parity.py:95` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_docs_cli_parity.py:120` currently check documented defaults only for boolean pairs `fix` and `promote`, and value options `max_fix_iterations` and `depth`. Add `reachability` to the boolean-pair loop so the guide must state `Default: --reachability` if Click default is true.

### Nearby wrapper tests to extend

- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_cli_smoke.py:15` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_cli_smoke.py:31` define `_SPEC9_FLAGS`, and `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_cli_smoke.py:40` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_cli_smoke.py:44` assert every listed flag appears in `reflect run --help`. Add `--reachability` and `--no-reachability` here if Click exposes both sides of the flag-pair.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_promote_plumbing.py:16` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_promote_plumbing.py:19` define the common direct `resolve_config()` helper. This file already tests negative-only prompt forwarding: default/on omits `--no-promote` at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_promote_plumbing.py:22` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_promote_plumbing.py:27`, disabled includes it at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_promote_plumbing.py:30` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_promote_plumbing.py:35`, and bare CLI print-command omits it at `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_promote_plumbing.py:38` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_promote_plumbing.py:52`. Add a sibling reachability plumbing test file or extend this one with the same pattern plus an exact-once assertion for `--no-reachability`.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_base_precedence.py:74` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_base_precedence.py:82` show the current prompt-token assertion style (`prompt.split()`, locate a flag, inspect value). Use `prompt.split().count("--no-reachability") == 1` for the disabled case.
- `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_runner_e2e.py:39` through `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_runner_e2e.py:51` already inspects the patched `ClaudeProcess` call in an E2E run. If a launch-level assertion is added, inspect `mock_cls.call_args.kwargs["prompt"]` there or in a focused new test.

## Recommended MDTM task-item breakdown

1. **Add ReflectConfig reachability state**
   - Add `reachability: bool` to `ReflectConfig` in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/models.py`.
   - Add `reachability: bool = True` to `resolve_config()` in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/config.py`.
   - Pass `reachability=reachability` into the `ReflectConfig(...)` constructor.

2. **Add Click surface and wrapper-to-wrapper forwarding**
   - Add a default-enabled Click flag-pair in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/commands.py`, preferably `@click.option("--reachability/--no-reachability", "reachability", default=True, help="...")`.
   - Add `reachability: bool` to `run()` and forward it to `resolve_config()`.
   - In `_build_inner_command(config)`, forward disabled reachability explicitly with `if not config.reachability: cmd.append("--no-reachability")` so `--tmux --no-reachability` does not re-enable reachability in the inner run. Forwarding the positive side is optional for behavior, but forwarding only the negative side matches the requested default-enabled contract.

3. **Forward to `/sc:reflect` exactly once when disabled**
   - In `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/src/superclaude/cli/reflect/runner.py`, add one branch in `_build_prompt()` after the `--no-promote` branch or near other boolean reflect flags: `if not config.reachability: parts.append("--no-reachability")`.
   - Do not add `--reachability` to the slash prompt when enabled.
   - Do not append `--no-reachability` in both `_build_prompt()` and another child-launch path; `_audit_once()` already uses `_build_prompt()` as the single source of the child prompt.

4. **Update docs parity surface**
   - Add a Key options bullet in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/docs/guides/reflect-cli-tools-guide.md` documenting `--reachability` / `--no-reachability`, stating `Default: --reachability`, and describing that `--no-reachability` disables the contracted-sink reachability/oracle-admissibility gate.
   - Update any examples only if the contracted tasklist needs to show explicit disablement; otherwise leave examples default-enabled.

5. **Add/extend tests**
   - Add `--reachability` and `--no-reachability` to `_SPEC9_FLAGS` in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_cli_smoke.py`.
   - Add `reachability` to the boolean default loop in `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_docs_cli_parity.py` so docs must state `Default: --reachability`.
   - Add prompt plumbing tests, preferably beside `/config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_promote_plumbing.py`:
     - direct `resolve_config()` default produces `config.reachability is True` and `_build_prompt()` omits `--no-reachability`;
     - direct `resolve_config(..., reachability=False)` produces `config.reachability is False` and `_build_prompt().split().count("--no-reachability") == 1`;
     - CLI `reflect run <tasklist> --print-command` omits `--no-reachability` by default;
     - CLI `reflect run <tasklist> --no-reachability --print-command` prints `--no-reachability` exactly once in the prompt output.
   - Add a tmux inner-command unit assertion if reachable in existing tests: disabled config should include `--no-reachability` in `_build_inner_command(config)`.

6. **Targeted verification commands**
   - `uv run pytest /config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_cli_smoke.py /config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_docs_cli_parity.py /config/workspace/IronClaude/.dev/worktrees/ReflectHardening-3/tests/cli/reflect/test_promote_plumbing.py -q`
   - If adding a new test file, include its absolute path in the command above.
