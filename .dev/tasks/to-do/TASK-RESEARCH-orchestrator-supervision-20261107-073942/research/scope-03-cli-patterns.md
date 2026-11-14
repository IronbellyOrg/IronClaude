# Scope 03: CLI, command and skill patterns
**Scope:** src/superclaude/cli/main.py, cli/recommend, cli/reflect, their tests, commands/reflect.md + skills/sc-reflect-protocol, Makefile, pyproject, registry tests, help.md, docs/designs/sc-issue-command.md
**Status:** Complete
**Date:** 2026-11-07
---

## Files read (path, line count)

| Path | Lines | Read extent |
|---|---|---|
| src/superclaude/cli/main.py | 565 | 1-30, 505-565, grep of all decorators |
| src/superclaude/cli/recommend/__init__.py | 20 | full |
| src/superclaude/cli/recommend/commands.py | 461 | 1-140 |
| src/superclaude/cli/reflect/__init__.py | 30 | full |
| src/superclaude/cli/reflect/config.py | 394 | 55-214 |
| src/superclaude/cli/reflect/{commands,runner,contract}.py | 585 / 834 / 420 | grep for subprocess, which, PURE |
| tests/cli/test_cli_registration.py | 128 (re-verified 2026-11-07) | full |
| tests/recommend/test_cli_registration.py | 39 (re-verified 2026-11-07) | full |
| tests/recommend/conftest.py | 24 (re-verified 2026-11-07) | full |
| tests/cli/reflect/conftest.py | 188 | full |
| tests/cli/reflect/test_contract_status_cli.py | (not counted) | 1-80 |
| tests/recommend/test_routing_refresh.py | (not counted) | 26-67 grep, 620-679 |
| tests/core/test_how_we_work_routing_table.py | (not counted) | 27-40, 285-334, 352-368 |
| tests/commands/test_routing_plugin_parity.py | 47 (re-verified 2026-11-07) | full |
| tests/commands/test_issue_command.py | (not counted) | 1-60 |
| tests/unit/test_cli_install.py | (not counted) | 630-680 |
| src/superclaude/commands/reflect.md | 305 | 1-70, 140-164, heading grep |
| src/superclaude/commands/recommend.md | 138 (re-verified 2026-11-07) | full |
| src/superclaude/commands/issue.md | (not counted) | 1-12, heading grep, 45-52, 87-89 |
| src/superclaude/commands/help.md | 135 | full |
| src/superclaude/commands/README.md | (not counted) | full via cat |
| src/superclaude/skills/sc-reflect-protocol/SKILL.md | 1954 | 1-40 |
| src/superclaude/skills/sc-issue-protocol/SKILL.md | (not counted) | 1-8 |
| src/superclaude/skills/sc-recommend/SKILL.md, sc-swarm-wizard-protocol/SKILL.md | (not counted) | grep for CLI calls |
| src/superclaude/core/HOW-WE-WORK.md | (not counted) | 310-339 |
| Makefile | 560 | 1-70, 105-204, grep of targets |
| pyproject.toml | 216 | 50-54, 173-216 |
| .pre-commit-config.yaml, .github/workflows/test.yml | - | ruff lines only |
| docs/designs/sc-issue-command.md | 477 | 1-12, 346-411, heading grep |
| docs/user-guide/commands.md | - | heading grep |

## CLI group registration pattern (file:line, exact code shape)

- Root group: `src/superclaude/cli/main.py:18-26`, `@click.group()` + `@click.version_option(version=__version__, prog_name="SuperClaude")` on `def main()`. [CODE-VERIFIED]
- Built-in commands (`install`, `mcp`, `update`, `install-skill`, `doctor`, `version`) are defined inline with `@main.command()` (main.py:29, 283, 334, 432, 471, 513). [CODE-VERIFIED]
- Subcommand groups are registered in a deferred-import block at the END of main.py, after `version()` (main.py:519-561), just before `if __name__ == "__main__": main()` (main.py:564-565). Each entry is two lines separated by a blank line, with the exact trailing comment:

```python
from superclaude.cli.reflect.commands import reflect_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports

main.add_command(reflect_group, name="reflect")
```

- Registered groups in order: sprint (519/521), roadmap (523/525), cleanup-audit (527/529), tasklist (531/533), cli-portify (535/537, no `name=`), prd (539/541), eval (543/545), swarm (547/549), recommend (551/553), init-lite (555/557, a single command, not a group), reflect (559/561). [CODE-VERIFIED]
- Two import styles coexist: from the package `__init__` (`superclaude.cli.recommend`, main.py:551) or from the `commands` submodule (`superclaude.cli.reflect.commands`, main.py:559). [CODE-VERIFIED]
- A new `sweep` group would be a new two-line entry after main.py:561 and before :564: `from superclaude.cli.sweep import sweep_group  # noqa: E402,I001  # intentional: ...` then `main.add_command(sweep_group, name="sweep")`. (Recommendation, not existing code.) [CODE-VERIFIED] anchors only: main.py:561 is the last `add_command` line and main.py:564-565 is the `__main__` guard; no `src/superclaude/cli/sweep/` exists yet.
- Lazy package `__init__` pattern (keeps `superclaude --help` fast): `src/superclaude/cli/recommend/__init__.py:12-20` uses a module-level `__getattr__(name)` that imports `recommend_group` from `.commands` only on access, with `__all__ = ["recommend_group"]`. [CODE-VERIFIED]
- Eager package `__init__` pattern: `src/superclaude/cli/reflect/__init__.py:17-30` imports `reflect_group` and pure helpers (`resolve_config`, `derive_verdict`, `parse_contract`, models) at import time. Its module docstring (lines 1-15) lists each submodule's job (`models` types only, `config`, `contract` pure, `runner`, `commands` Click surface). [CODE-VERIFIED]

## Example group layout and test-mocking pattern (file:line)

### Layout

- `src/superclaude/cli/recommend/`: `__init__.py` (20 lines), `commands.py` (461, Click surface), `cache.py` (196), `telemetry.py` (62), `dispatch.py` (137), `best_model.py` (134), `models.py` (40), `prompts.py` (258), `eval_aggregate.py` (90), `eval_grader.py` (93), `eval_pipeline.py` (144), `plugin_eval.py` (149). No `__main__.py`. [CODE-VERIFIED via wc/ls]
- `src/superclaude/cli/reflect/`: `__init__.py` (30), `models.py` (182, dataclasses + `Verdict` enum), `config.py` (394, owns all subprocess/git calls), `contract.py` (420, pure), `runner.py` (834), `commands.py` (585, Click surface), `ensemble.py` (895), `fallback.py` (594), `_diversity.py` (61). No `__main__.py`. [CODE-VERIFIED]
- House split to copy for a pure classifier: types in `models.py`; pure logic in a module documented "PURE: no Click, no subprocess, no I/O" (reflect/contract.py:397; also contract.py:7 "No Click, no subprocess"); every subprocess call isolated in one module (reflect/config.py:158-159: "Lives in config.py (the subprocess-owning module) so runner.py stays free of any raw subprocess import"); Click surface in `commands.py`. [CODE-VERIFIED]

### Click surface conventions (recommend/commands.py)

- `from __future__ import annotations` + `import click` at top (commands.py:18-24). [CODE-VERIFIED]
- `@click.group("recommend")` on `def recommend_group() -> None:` with a docstring that includes an `Examples:` block, body `pass` (commands.py:34-48). The group docstring is what `superclaude --help` shows; tests assert a stable fragment of it (tests/cli/test_cli_registration.py:69 for the eval group). [CODE-VERIFIED]
- Nested groups via `@recommend_group.group("cache")` (commands.py:51) and commands via `@cache_group.command("get")` (commands.py:57). [CODE-VERIFIED]
- Path options: `type=click.Path(path_type=Path)` with a module-constant default (commands.py:26-27, 59-64). [CODE-VERIFIED]
- Heavy imports deferred inside each command body (commands.py:67, 102-104; module docstring commands.py:6-8 cites the `cli/tasklist` precedent). [CODE-VERIFIED]
- JSON output: `click.echo(json.dumps(row, ensure_ascii=False))` (commands.py:75, 461). Errors: `click.echo("[recommend cache get] ...", err=True)` then `sys.exit(1)` (commands.py:73-74, 108-112). The `[group subcommand]` stderr prefix is the house convention. [CODE-VERIFIED]
- Docstring claim "The skill shells to these subcommands via `Bash(uv run python -m superclaude.cli.recommend ...)`" (recommend/commands.py:40-41): [CODE-CONTRADICTED] there is no `src/superclaude/cli/recommend/__main__.py`, so `python -m superclaude.cli.recommend` cannot run the package. A sweep skill should call the installed entry point `superclaude sweep ...`.

### Subprocess / git shape (reflect/config.py)

- One private helper `_git(cwd: Path, *args: str) -> str` (reflect/config.py:64-78):

```python
result = subprocess.run(
    ["git", "-C", str(cwd), *args],
    capture_output=True, check=True, text=True, timeout=10,
)
return result.stdout.strip()
```

  Callers catch `(OSError, subprocess.SubprocessError)` and fail closed (config.py:103-109, 151-152, 182-183). Its docstring says it "Models the drift.py `_git` subprocess shape" (config.py:67). [CODE-VERIFIED]
- Binary presence preflight: `shutil.which("claude") is None` (reflect/runner.py:387) and `shutil.which("tmux") is None` (reflect/commands.py:494). [CODE-VERIFIED]

### Test-mocking pattern

- Tests import the live root group and use Click's `CliRunner` (no subprocess): `from superclaude.cli.main import main`; `runner.invoke(main, ["recommend", "--help"])`; assert `exit_code == 0` and subcommand names in `result.output` (tests/recommend/test_cli_registration.py:1-39). [CODE-VERIFIED]
- Suite folder convention: own `__init__.py` + `conftest.py` with `tmp_path` path fixtures so tests never write the real `.claude/cache/` (tests/recommend/conftest.py:1-24). `tests/cli/reflect/` has `__init__.py`; `tests/cli/` itself has none. [CODE-VERIFIED]
- git mocking replaces the module-level `_git` helper, not `subprocess.run`: fixture `patch_git` does `monkeypatch.setattr(config_mod, "_git", _fake_git)` where `_fake_git(cwd, *args)` dispatches on `args[0]` (tests/cli/reflect/conftest.py:58-80). Also `with patch("superclaude.cli.reflect.config._git", side_effect=_fake_git):` (tests/cli/reflect/test_isolate_reviewers_cli.py:97, 140, 163) and `MagicMock(side_effect=...)` (tests/cli/reflect/test_cli_smoke.py:265-266 (re-verified 2026-11-07: the MagicMock is built at :265 and installed at :266), 287). [CODE-VERIFIED]
- Binary preflight mocking: `monkeypatch.setattr(runner_mod.shutil, "which", lambda name: "/usr/bin/claude")` (tests/cli/reflect/conftest.py:95; test_preflight_phase_complete.py:53). [CODE-VERIFIED]
- Read-only proof pattern: patch forbidden entry points with `side_effect=AssertionError(...)` so a test fails if a read-only subcommand reaches them (tests/cli/reflect/test_contract_status_cli.py:44-66), and run inside `CliRunner.isolated_filesystem()` so cwd-relative probes never touch the real repo (same file, docstring lines 18-22). Reusable to prove `/sc:sweep` makes no local writes beyond its report. [CODE-VERIFIED for the pattern] **Gate fix B-13:** it does not prove that the sweep leaves Orca state unchanged, because an Orca subprocess call can change state with no local write (plain `check` may mark messages read, [UNVERIFIED] per `06-orca-open-questions.md` Gap 1 (`:158`), so it is treated as draining; every `check` is a mutation call, `message-check-handler.js:30`; `check --unread` is destructive on older runtimes, `message-check-handler.js:17`; `worktree ps --agent-wait` may write to terminals, 06 Q3). A second test is therefore required: every Orca call goes through one subprocess seam in the `_git` style of reflect/config.py:64-78 (for example `_orca(*args)`), the test patches that seam and asserts each argv against an allowlist. **Default allowlist (gate fix NB-2; read verbs added by gate fix NB-4):** `worker-list`, `worker-show`, `worker-read`, `worktree ps` without `--agent-wait`, `orchestration task-list` (with `--ready` and `--run <id>`; plain read `orchestration.taskList`, `07-gate-gap-fill.md` B `:43`, `task-handlers.js:32-44`), `orchestration run-list` (plain read `orchestration.runList`, `07` B `:41`, `run-handlers.js:35-48`), `orchestration run-current` (plain read `orchestration.runCurrent`, `07` B `:42`, `run-handlers.js:28-34`) and `orchestration gate-list` (plain read `orchestration.gateList`, `07` B `:44`, `gate-handlers.js:26-37`); these four feed "waiting on a person" kind (b) (`research-notes.md:197`), the Run ids and the Owner column (`scope-04:339`) and the Approval candidate (`scope-04:345`). No `check` call at all, because the design default reads contracts only (`06-orca-open-questions.md:72`, constraints (2) and (3)). **Gated additions:** only after the probe settles constraint (2) (no `legacyCompatibility.ackMessageIds` on `--peek`/`--all` results, Gap 18) and constraint (3) (a runtime probe shows peek is honoured) may the allowlist add `orchestration check --peek` and `orchestration check --all`, as two **separate** argv, never combined: the handler rejects more than one read mode (`message-check-handler.js:18-19`: `if ([flags.has('unread'), peek, flags.has('all')].filter(Boolean).length > 1) throw ... 'Choose at most one message read mode: --unread, --peek, or --all.'`) [CODE-VERIFIED 2026-11-07 by grep]. Forbidden (the test fails if any appears): any `check` while the probe gate is unsettled, plain `check` without `--peek`/`--all`, any argv with two or more of `--unread`/`--peek`/`--all`, `--ack`, `--wait`, `--unread`, `check --format`, `reply`, `ask`, `send`, `inbox` (a plain read on the CLI side, but whether it marks messages read is [UNVERIFIED], so it is not used: `07-gate-gap-fill.md:92`, `06-orca-open-questions.md` Gap 4 `:161`), `worktree ps --agent-wait`, and any verb not on the allowlist. The contract-only fallback (read `return-contract.yaml` files when Orca is unreachable) stays.
- Fixture files live in `tests/cli/reflect/fixtures/`, reached through `FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"` (conftest.py:17). [CODE-VERIFIED]

## Command + skill file pattern (frontmatter, Activation, allowed-tools; file:line)

### Command file (`src/superclaude/commands/<name>.md`, installed as `/sc:<name>`)

- Frontmatter fields, reflect.md:1-11: `name: reflect` (bare, no `sc:` prefix), `description: "..."` (quoted, one line), `category`, `complexity`, `mcp-servers: [..]`, `personas: [..]`, optional `version`, `supersedes`, `argument-hint: "..."`. [CODE-VERIFIED]
- issue.md:1-9 (the newest command, closest template): `name: issue`, `description`, `category: workflow`, `complexity: advanced`, `mcp-servers: [auggie, codegraph]`, `personas: [analyzer]`, `argument-hint`. No `allowed-tools`. [CODE-VERIFIED]
- recommend.md:1-9 same shape (`category: utility`, `complexity: standard`, `personas: []`). [CODE-CONTRADICTED] in one field: recommend.md:2 is `name: sc:recommend` (prefixed), not a bare name like reflect.md:2 and issue.md:2; the other fields match the described shape.
- `allowed-tools` in command frontmatter is optional. 14 of 46 command files set it (re-verified 2026-11-07: 47 `.md` files, one of them README.md) (Grep `^allowed-tools`), for example `validate-tests.md:6` `Read, Glob, Grep, Bash, TodoWrite, Task, Skill`, `init-lite.md:6` `Read, Glob, Grep, Bash, Skill`, `post-release.md:6` `Read, Glob, Grep, Skill`. Scoped Bash patterns are used where the command must stay narrow: `graph.md:9` `Skill, Bash(codegraph init --yes *), Bash(codegraph init -i)` and `help.md:6` `Bash(find:*), Bash(ls:*), ...`. A read-only `/sc:sweep` could pin `Bash(superclaude sweep:*)` and `Bash(uv run superclaude sweep:*)` the same way (both forms, per open question 3, gate fix B-19; NB-3). reflect.md, issue.md and recommend.md set none. [CODE-VERIFIED]
- Section order in issue.md: `## Triggers` (22), `## Usage` (26), `## Options` (33), `## STOP rules (checked before Activation)` (45), `## Examples` (53), `## Outputs` (62), `## Boundaries` (73), `## Activation` (87), `## Related Commands` (95). reflect.md: Triggers 15, Required Input 23, Usage 37, Options 84, Behavioral Summary 127, Activation 146, MCP Integration 153, Tool Coordination 161, Examples 176, Boundaries 256, CRITICAL BOUNDARIES 284, Related Commands 296. [CODE-VERIFIED]
- Activation block, exact shape (reflect.md:146-151; issue.md:87-93 same form; recommend.md:52-58 identical form [CODE-CONTRADICTED]: recommend.md has a blank line between the invoke line (:54) and `> Skill sc-recommend` (:56), its follow-on sentence (:58) reads "Do NOT proceed using only this command file" and names no `~/.claude/skills/...` path):

```markdown
## Activation

**MANDATORY**: Before executing any protocol steps, invoke:
> Skill sc:reflect-protocol

Do NOT proceed with protocol execution using only this command file. The full behavioral specification ... is in the protocol skill at `~/.claude/skills/sc-reflect-protocol/SKILL.md`.
```

  Note the skill is referenced by its frontmatter `name` (`sc:reflect-protocol`) while the folder is `sc-reflect-protocol`; `recommend.md:56` uses `> Skill sc-recommend` (folder name = skill name, no protocol suffix). The installed path `~/.claude/skills/...` is used, never `src/superclaude/...` (CLAUDE.md rule). tests/recommend/test_routing_refresh.py:38-40 parses this block with `^## (?:Activation|Skill Invocation)` and :472 requires the line form `^> Skill (\S+)$`. [CODE-VERIFIED]

### Skill file (`src/superclaude/skills/<dir>/SKILL.md`)

- sc-reflect-protocol/SKILL.md:1-6: `name: sc:reflect-protocol`, `description: "..."`, `version: 1.0.0`, `allowed-tools: Read, Grep, Glob, Bash, TodoWrite, Task, Write, Edit, Skill, mcp__auggie__codebase-retrieval, mcp__codegraph__..., ...`. Then an HTML comment `<!-- Extended metadata (for documentation, not parsed): category / complexity / mcp-servers / personas -->` (lines 16-23). [CODE-VERIFIED]
- sc-issue-protocol/SKILL.md:1-4: `name: sc:issue-protocol`, `description`, `allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task, Skill, AskUserQuestion`, followed by the same Extended-metadata comment. [CODE-VERIFIED]
- Skill layout precedent: `SKILL.md` + `refs/*.md` + `templates/` + `scripts/*.py` (docs/designs/sc-issue-command.md:355-363; the design calls for SKILL.md "Under 500 lines"). A skill-local script is standard library only and is tested directly (design :362-363, :395-396). The sweep leaning puts logic in `src/superclaude/cli/` instead, which the issue design explicitly did not do (":384 No CLI (`src/superclaude/cli/`) code: the only program is the skill's own script"). [CODE-VERIFIED as text of the design]
- Naming convention for a sweep pair would be: command `src/superclaude/commands/sweep.md` (`name: sweep`) + skill `src/superclaude/skills/sc-sweep-protocol/SKILL.md` (`name: sc:sweep-protocol`). (Recommendation, follows the 20+ existing `sc-*-protocol` folders listed under src/superclaude/skills/.) [CODE-VERIFIED] 25 `sc-*-protocol` folders exist; no `commands/sweep.md` exists yet.

## Registries and tests a new command/skill/CLI must be added to (file:line each)

Lists that would fail or need a deliberate update:

1. `src/superclaude/cli/main.py:559-561` pattern: new `from ... import sweep_group  # noqa: E402,I001 ...` + `main.add_command(sweep_group, name="sweep")`. [CODE-VERIFIED]
2. `tests/recommend/test_routing_refresh.py:33` `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` must gain `"sweep"`. Line 647-648 asserts `{p.stem for p in _COMMANDS.glob("*.md") if p.name != "README.md"} - _POST_REFRESH_ADDITIONS == active`; any new command file fails this test otherwise. [CODE-VERIFIED] (The issue design cites "line 32 today", docs/designs/sc-issue-command.md:380; it is line 33 now, minor drift.)
3. `src/superclaude/core/HOW-WE-WORK.md:314-337` "Other commands" table between `<!-- other-commands:v1 -->` (318) and `<!-- /other-commands -->` (337): add a `/sc:sweep` row (commands/README.md step 4 requires a row for every new command). [CODE-VERIFIED]
4. `tests/core/test_how_we_work_routing_table.py:27-40` `_OTHER_COMMANDS` set must gain `"sc:sweep"`; :291-311 asserts the table members equal this set exactly and that each named command file exists. [CODE-VERIFIED]
5. `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` must be a byte copy of the edited guide (tests/commands/test_routing_plugin_parity.py:29-38). [CODE-VERIFIED] If the level table changes, `src/superclaude/core/CLAUDE.md:65-82` (`<!-- level-table:v1 -->` block) must be recopied (commands/README.md step 5); a sweep row in "Other commands" does not touch the level table.
6. `docs/user-guide/commands.md:105` "8. UTILITIES" table (the `/sc:issue` row at :115) plus a detail section (`/sc:issue` at :347). Not test-enforced as far as found. [CODE-VERIFIED for location; enforcement UNVERIFIED]
7. Optional CLI registration test, house style: a new `tests/sweep/test_cli_registration.py` modelled on tests/recommend/test_cli_registration.py:1-39. `tests/cli/test_cli_registration.py:31-49` `EXPECTED_TOP_LEVEL_COMMANDS` is a subset check (it only invokes `--help` on each listed name, :95-106), so adding `sweep` does not break it; it already omits `swarm` and `reflect`. Adding `sweep` there is optional. [CODE-VERIFIED]
8. Static command-file test precedent: tests/commands/test_issue_command.py:1-60 (reads frontmatter by splitting on `\n---\n`, checks the Options table and Activation). A `tests/commands/test_sweep_command.py` would follow it. [CODE-VERIFIED]
9. **`make lint` must pass (gate fix B-27).** `make lint` runs `lint-architecture` (target at Makefile:362, summary :484-489), which exits 1 on any error (Makefile:489). The gates a new `commands/sweep.md` + `skills/sc-sweep-protocol/SKILL.md` pair must pass [CODE-VERIFIED, re-read 2026-11-07]:
   - Check 1 (Makefile:368-383): a command file with `## Activation` needs a skill dir `sc-<name>-protocol` (or a utility skill without the suffix).
   - Check 2 (:385-396): every `sc-*-protocol` skill needs a matching `commands/<name>.md`.
   - Checks 3/4 (:398-411): a command file over 200 lines warns, over 500 lines fails (README.md excluded).
   - Check 6 (:413-427): a command paired with a `sc-*-protocol` skill must contain `## Activation`.
   - Check 8 (:429-439): every `sc-*-protocol/SKILL.md` frontmatter needs `name:`, `description:` and `allowed-tools:`.
   - Check 9 (:441-451): the SKILL.md `name:` must end in `-protocol` (so `sc:sweep-protocol`).
   - Check 11 (:467-476): `superclaude.tools.arch_lint --check-contracts src/superclaude/contracts/__init__.py --scan-paths src/superclaude/cli/` fails on contract constants re-declared under `src/superclaude/cli/`. Today `RETURN_CONTRACTS` holds only `sc:adversarial` (`contracts/__init__.py:204-206`). A `cli/sweep/` module that needs return-contract field names must import them from `superclaude.contracts` (or the module that owns the worker contract), never re-declare them.

Suite-wide scans every new primitive must pass (gate fix B-21; each re-read 2026-11-07) [CODE-VERIFIED]:

- `tests/skills/test_model_alias_policy.py:81-100`: globs every `agents/*.md`, `skills/*/SKILL.md` and `commands/*.md` (:84-86); a frontmatter `model:` must be an alias or `inherit` (`ALIASES`, :97-99). `sweep.md` and `sc-sweep-protocol/SKILL.md` either set no `model:` or an alias.
- `tests/commands/test_graph_command.py:219-225`: globs every `skills/*/SKILL.md`; no skill other than `sc-graph-protocol` may contain `sc:graph-protocol`.
- `tests/skills/test_worker_contract.py`: the AC-0.9 git/gh write-verb audit scans every file under `AUDIT_ROOTS` = skills, commands, agents (:1090-1094, used at :1134); every git or gh write-verb line must be classified. `_check_no_unattended_sections` (:464-472) requires the set of commands with a `## Unattended mode` heading to equal `UNATTENDED_COMMANDS` (:379), and `_ORCA_NAME_RE` (:476-478, asserted at :519) bans naming an Orca command inside such a section. The sweep is read-only and should add no `## Unattended mode` section unless the contract set is extended deliberately.
- `tests/skills/test_primitive_dual_surface_lookup.py`: not a glob scan; it pins named sites only (`_ADV_SITES` :16-21, the persona and rf-qa lookups :38-50). It does not cover a new skill, but the CLAUDE.md dual-surface rule it guards still applies if `sc-sweep-protocol` looks up another installed primitive.

Not registries (no change needed):

- `/sc:help` reads the installed tree live (`find -L "$HOME/.claude/commands/sc" ...`, help.md:30-34) and its Boundaries forbid a hand-written list (help.md:134). [CODE-VERIFIED]
- `tests/unit/test_cli_install.py:638-647` checks only that `agent`, `index-repo`, `recommend`, `research` are present. [CODE-VERIFIED]
- `make sync-dev` and `make verify-sync` glob every `src/superclaude/commands/*.md` and every skill dir with a SKILL.md (Makefile:112-136, verify-sync Commands block); no list to edit. [CODE-VERIFIED]
- Plugin command mirrors are required only for `help`, `recommend`, `workflow`, `implement` (tests/commands/test_routing_plugin_parity.py:41-47). [CODE-VERIFIED]
- ~~No test found that globs every `src/superclaude/skills/*/SKILL.md` for a registry.~~ [CODE-CONTRADICTED, gate fix B-21] Two tests glob every skill: `tests/skills/test_model_alias_policy.py:85` and `tests/commands/test_graph_command.py:222`. They are not registries (no list to edit) but a new skill must pass them; see "Suite-wide scans" under item 9 above.

## Build, lint, format and sync commands (exact commands, ruff version)

- Ruff pinned exactly: `"ruff==0.15.20"` (pyproject.toml:54; comment :50-53 says the pin exists because `ruff format` output is version-sensitive). Pre-commit hook `ruff-pre-commit` `rev: v0.15.20`, `id: ruff-format`, `files: '^(src|tests)/'` (.pre-commit-config.yaml:105-113, comment says rev MUST equal the pyproject pin). [CODE-VERIFIED]
- Ruff config: `line-length = 88`, `target-version = "py310"`, `exclude = ["docs/"]`, `extend-exclude = [".dev/", ...]` (pyproject.toml:173-181); `[tool.ruff.lint] select = ["E", "F", "I", "N", "W", "TID"]`, `ignore = ["E501", "N818"]` (:183-193); banned API `anthropic` imports via `flake8-tidy-imports` (:203-206), so a sweep classifier must not import the anthropic SDK. [CODE-VERIFIED]
- CI gates: `ruff check src/ tests/` and `ruff format --check src/ tests/` (.github/workflows/test.yml:100-106). [CODE-VERIFIED]
- Makefile: `make lint` = `lint-architecture` then `uv run ruff check .` (Makefile:48-50; what lint-architecture enforces is listed in registry item 9 above, and `make lint` must pass); `make format` = `uv run ruff format .` (:53-55); `make test` = `uv run pytest` (:13-15); `make install` = `uv pip install -e ".[dev]"` (:5-7); `make sync-dev` (:109-163) copies skills, agents, commands (to `.claude/commands/sc/`), hooks, templates; `make verify-sync` (:166 onward) exits 1 on drift. No `format-check` make target exists; use `uv run ruff format --check src/ tests/`. [CODE-VERIFIED]
- Per-feature run line used by the issue design: `uv run pytest tests/commands tests/core tests/skills tests/recommend ...`, then `make test` (docs/designs/sc-issue-command.md:402); sync order `make sync-dev`, `make verify-sync`, guide copy, `grep -rn 'src/superclaude' src/superclaude/{commands,skills,agents,core,hooks}` (:404-410). [CODE-VERIFIED as text]

## Design doc house format (docs/designs/sc-issue-command.md heading list)

Header block (lines 1-9): `# Design: <command> and <skill>`, then bold key lines `**Status:**`, `**Issue:**`, `**Branch:**`, `**Source of truth:**`, `**Produced by:**`, then `---`. [CODE-VERIFIED] docs/designs/sc-issue-command.md:1-9 (key lines 3-7, `---` at 9).

Headings in order:

1. `## 1. Purpose and scope` (11)
2. `## 2. Binding decisions (issue body + three comments)` (20)
3. `## 3. Corrections to the issue text` (42)
4. `## 4. Command interface` (57)
5. `## 5. Component architecture` (81)
6. `## 6. Model tiers and how each sub-agent is pinned` (112)
7. `## 7. \`--claim\` flow` (137)
8. `## 8. \`--create\` flow` (182)
9. `## 9. Next-step chains (what \`next-steps.md\` may contain)` (221)
10. `## 10. Output files and templates` (240)
11. `## 11. Label set` (274)
12. `## 12. ClickUp lookup and assignment` (286)
13. `## 13. Repository resolution and GitHub call rules` (318)
14. `## 14. Error handling` (325)
15. `## 15. Files to create or change` (346; Create table + Change table + "Not changed")
16. `## 16. Tests` (386; table "Test file | What it pins" + run line)
17. `## 17. Sync, routing registration and documentation` (404)
18. `## 18. Defaults chosen by this design` (412)
19. `## 19. Flags cited, verified against the real command files` (446)
20. `## 20. Acceptance criteria for the implementation` (467)

Sections 7-13 are feature-specific; the reusable skeleton is 1-6, 14-20. [CODE-VERIFIED] all 20 heading line numbers match the current file.

## Open questions

1. Lazy vs eager package `__init__` for `cli/sweep/`: recommend uses lazy `__getattr__` (recommend/__init__.py:12-20), reflect is eager (reflect/__init__.py:17-30). Lazy keeps `superclaude --help` fast; either works with the main.py registration. [CODE-VERIFIED] both line ranges.
2. Whether `/sc:sweep` belongs in the HOW-WE-WORK "Other commands" table (requires items 3-5 above) or in the excluded set at tests/core/test_how_we_work_routing_table.py:299-309 (which lists commands deliberately kept out of that table, e.g. `sc:help`, `sc:init-lite`). commands/README.md step 4 says every new command gets a row; a decision is still needed. [CODE-VERIFIED] test_how_we_work_routing_table.py:299-309 and commands/README.md:10.
3. How the skill calls the CLI. The recommend docstring's `uv run python -m superclaude.cli.recommend` is CODE-CONTRADICTED (no `__main__.py`). The skills actually use `uv run superclaude <group> ...`: sc-recommend/SKILL.md:77, :309, :324 (`uv run superclaude recommend dispatch|eval plugin|cache put ...`) and sc-swarm-wizard-protocol/SKILL.md:35, :69, :110 (`uv run superclaude swarm ...`). [CODE-VERIFIED] Open: `uv run` assumes a uv project in the cwd; whether that works in a non-IronClaude project where `superclaude` was installed with pipx is UNVERIFIED. **Decision recommendation (gate fix B-19):** the skill calls the installed entry point `superclaude sweep ...` on PATH (the pipx install in CLAUDE.md puts `superclaude` there), as sc-reflect-protocol/SKILL.md:63-64 already does (`superclaude reflect contract-status ...`) [CODE-VERIFIED]; `uv run superclaude sweep ...` is the fallback only inside a dev checkout, used when `command -v superclaude` finds nothing. `allowed-tools` lists both forms (`Bash(superclaude sweep *)`, `Bash(uv run superclaude sweep *)`). Test requirement: a static test pins that the SKILL.md uses the bare form first and lists both in `allowed-tools`; the implementation plan must also run `superclaude sweep --help` once from a project that is not a uv project to prove the PATH form works there. That live run is not done here (read-only research), so the pipx behaviour stays [UNVERIFIED] until the plan runs it.
4. Skill `allowed-tools` precedent for scoping the CLI: sc-swarm-wizard-protocol/SKILL.md:7 `allowed-tools: Read, Grep, Glob, Write, AskUserQuestion, TodoWrite, Task, Monitor, Bash(uv run superclaude swarm *), Bash(ls *), Bash(wc *), Bash(test *), Bash(mkdir *)`. [CODE-VERIFIED] A sweep skill can copy this with both `Bash(superclaude sweep *)` and `Bash(uv run superclaude sweep *)` (the PATH-first form and the dev-checkout fallback decided in open question 3, gate fix B-19; NB-3) plus `Write` for the report. Open: whether the command file should also set `allowed-tools` (graph.md:9 does; reflect.md and issue.md do not) and how Claude Code combines the two is UNVERIFIED.
5. Where the orca/claude-session probes live: following reflect/config.py, every subprocess call (git, orca, tmux) should sit in one module with a `_git`-style helper so tests patch a single seam; the pure classifier stays subprocess-free like reflect/contract.py. [CODE-VERIFIED] for the cited precedent (reflect/config.py:64-78, :158-159; contract.py:7, :397); the sweep placement itself is a recommendation.
6. `docs/user-guide/commands.md` entry: whether any test pins the UTILITIES table is UNVERIFIED. [UNVERIFIED]

## Summary

New top-level CLI groups are registered by a two-line deferred-import block at the end of `src/superclaude/cli/main.py` (main.py:519-561, before the `__main__` guard at :564), with either a lazy `__getattr__` package `__init__` (recommend) or an eager one (reflect), all subprocess calls kept in one `_git`-style module and pure logic in a subprocess-free module. The read-only test proof pattern patches every forbidden entry point with `side_effect=AssertionError(...)` and runs inside `CliRunner.isolated_filesystem()` (tests/cli/reflect/test_contract_status_cli.py:44-66, docstring :18-22), which a `/sc:sweep` test can reuse. A new `/sc:sweep` must join main.py registration, `_POST_REFRESH_ADDITIONS` (test_routing_refresh.py:33), the HOW-WE-WORK "Other commands" table (:318-337), `_OTHER_COMMANDS` (test_how_we_work_routing_table.py:27-40), the plugin byte copy of the guide, and (by convention, not test) the docs/user-guide/commands.md UTILITIES table; sync, help and install need no list edits. Six open questions remain: lazy vs eager `__init__`, whether sweep belongs in "Other commands", how the skill calls the CLI under pipx installs, command vs skill `allowed-tools`, where the orca/claude probes live, and whether the UTILITIES table is test-pinned. Re-verification on 2026-11-07: 58 findings tagged [CODE-VERIFIED] after re-reading every cited file:line, 7 line numbers or counts corrected in place and marked `(re-verified 2026-11-07)`, 3 claims [CODE-CONTRADICTED] (recommend `python -m` docstring, recommend.md `name:` shape, recommend.md Activation "identical form"), and 3 items UNVERIFIED (whether a test pins the UTILITIES table, `uv run` under a pipx install, how command and skill `allowed-tools` combine).
