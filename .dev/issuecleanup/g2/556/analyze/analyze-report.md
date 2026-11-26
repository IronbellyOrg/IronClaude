# Reflect wrapper architecture analysis

## Scope and grounding
Target: `src/superclaude/cli/reflect`, the command-line wrapper behind `superclaude reflect run`, the area named by issue 556 (the grouped record of three defects in the reflection command). Focus: architecture. Depth: quick. No source was modified.

Codegraph: index_state=fresh, checked_at=2026-11-24T02:50:51Z; degraded: graph:unresolved

The graph covers 3,651 files with 0 added, 0 modified and 0 removed since the index. The package holds 10 Python files and 245 symbols: `ensemble.py` 62, `fallback.py` 41, `runner.py` 40, `panel_lint.py` 26, `commands.py` 23, `config.py` 21, `contract.py` 16, `models.py` 11, `__init__.py` 6, `_diversity.py` 5. One name lookup for `run_cmd` resolved to the swarm command of the same name rather than the reflect command, so that path was read by line range instead. That single miss is the `graph:unresolved` token; the ranges were confirmed by reading the file.

## Architecture and metrics
The wrapper is a thin orchestrator. `commands.py` resolves the configuration, `ReflectRunner.run()` (`runner.py:637`) preflights and then either prints a preview or runs an audit, and `contract.derive_verdict` decides the result. The runner never classifies deviations itself (`runner.py:439-445`).

Two audit routes exist and they do not share a prompt. A tier-2 run, which covers the default depth `standard` and `deep`, calls `run_tier2_ensemble` (`runner.py:536-543`). That dispatches the reviewer slots through the swarm transport and then, when two or more reviewers succeed and no score function is supplied, starts a real headless Claude process as the scorer (`ensemble.py:423-430`, `ensemble.py:537-553`). The tier-1 route builds the `/sc:reflect` prompt (`runner.py:452-481`) and launches it through one `ClaudeProcess` (`runner.py:544-570`), but production code reaches that branch only when the process class has been replaced by a test double (`runner.py:538`).

The preview path (`runner.py:647-662`) prints the `claude` argument list and the `/sc:reflect` prompt, then returns before any launch. The argument list is hand-copied to match `ClaudeProcess.build_command()` (`runner.py:483-507`), so it can drift from the builder it claims to mirror.

Error handling splits in two. A configuration failure is caught before the runner exists, written as a `config-error` sidecar and exits 2 (`commands.py:389-428`). Any exception raised inside `run()` is caught, written as a `blocked` sidecar with reason `runner-error`, and then re-raised (`commands.py:434-469`), so the process exit is Python's exit 1 rather than the verdict's exit code.

The last commit touching `runner.py`, `commands.py` or `ensemble.py` is `2ca022bf7` (pull request 653, the task-file route re-point). The current branch tip is `a7ae3dd30`.

## Severity-rated findings
1. High. The preview describes a route the shipped code does not take. `--print-command` prints the `/sc:reflect` prompt (`runner.py:452-481,647-651`), while a real run at the default depth goes through the ensemble (`runner.py:538-543`) and the scorer is sent the literal `/sc:adversarial` prompt (`ensemble.py:582-598`, the text at 594). An operator trusting the preview audits the wrong plan. This is issue 563.
2. High. An expected configuration failure exits 1 against a documented exit 2. With the default transport and the proxy variables absent, `read_env_for_pool` raises `TransportEnvError` (`src/superclaude/cli/swarm/transports/openai_compat.py:227-228`; the class is at 149). That exception leaves `run()`, the sidecar records `blocked` / `runner-error`, and the bare re-raise at `commands.py:469` leaves the exception uncaught, which Python reports as exit 1. The configuration-stop path exits 2 because `_BLOCKED_EXIT` is 2 (`commands.py:42,428`). The user guide maps `blocked` to exit 2 (`docs/guides/reflect-cli-tools-guide.md:370`). Anything keying off the exit code misreads a known, expected failure as a crash. This is issue 564.
3. Medium. Stub mode is not credit-free. The guide says `--transport stub` is for deterministic, credit-free continuous integration (`docs/guides/reflect-cli-tools-guide.md:137`), but the scorer is launched through the genuine `ClaudeProcess` whenever two reviewers succeed and no score function is given (`ensemble.py:424-430,537-553`). The manual testing guide already records this as observed-as-coded (`docs/testing/v5.0.0/user/D12-reflect.md:15,27`), so the two guides contradict each other. This is issue 565.

## Recommendations and roadmap
Do not start a fix. The owner set this area to lowest priority and backlog on 2026-11-18 because the wrapper runs headless Claude and is not used now. When that hold lifts, the smallest safe changes are: make the preview print the ensemble plan and the scorer prompt it actually sends, without launching; map `TransportEnvError` to exit 2 while still re-raising every other exception; and either score the stub path in-process or correct the guide to say stub still starts one `claude` session. If an in-process scorer is chosen, synthetic scores must never certify real-model convergence, and a model-free integration regression must protect that distinction. A blanket prompt rewrite, or a catch-all that turns every exception into exit 2, would hide real crashes, which the issue itself warns against.

## Verification limits
Read-only. No command was executed, so the exit codes and the scorer dispatch are confirmed from source, not re-run. The original captures from 2026-11-16 were not re-executed. The graph name lookup for `run_cmd` resolved to the wrong module and was discarded in favour of a direct line-range read.
