# Dependency map: the retire step for commands, skills and agents (6.0.0, PR 12)

Measured 2026-11-18 on branch `clayphi/v6-retire-step` at `15d4180b7` (integration after wave 5 plus the master merge). Read-only: codegraph (callers) plus `git ls-tree` against `v5.0.0` plus search. The plan's counts were taken at `d4d1662a8`; the re-measured numbers are below.

## 1. What is retired (generated from `v5.0.0`, verified here)

`git ls-tree --name-only v5.0.0 src/superclaude/{commands,skills,agents}/` against the same folders in this tree:

| Kind | Names present at `v5.0.0` and absent now | Count |
|---|---|---|
| commands | build, cli-portify, improve, index-repo, index, load, review-translation, roadmap, save, spawn, tasklist, validate-roadmap | 12 |
| skills | sc-cli-portify-protocol (6 files), sc-review-translation-protocol (1), sc-roadmap-protocol (7), sc-tasklist-protocol (6), sc-validate-roadmap-protocol (1) | 5 (21 files) |
| agents | none (the diff only adds issue-worker-t1, -t2, -t3) | 0 |

The plan's list matches. No swarm name is in the list (issue 571: swarm stays). No `src/superclaude/{commands,skills,agents}` name from the list exists in `plugins/superclaude/` or in the root `commands/`, `skills/`, `agents/` folders (those hold `sc-`-prefixed legacy copies or `confidence-check`; checked with `git ls-files`).

## 2. How a file reaches `~/.claude/` (proof source)

| Installer | Behavior | Path |
|---|---|---|
| commands | `shutil.copy2` of every `*.md` except `README.md`; no rewriting, no receipt. A forced install saves a differing target as `<name>.bak.<UTC stamp>` first | `src/superclaude/cli/install_commands.py:15-110` (copy at `:77`), `install_keep.py:33-46` |
| skills | `shutil.copytree` of the whole skill folder (so `__init__.py` and `refs/` come too); `--force` deletes the folder first. Also deletes (with `rmtree`, no proof) an installed `sc-<x>` skill whose command `<x>.md` exists and does not activate it | `src/superclaude/cli/install_skills.py:70-135`, `install_skill.py:14-50` |
| agents | `shutil.copy2` of every `*.md` except `README.md`, `__init__.py`; no receipt | `src/superclaude/cli/install_agents.py:15-70` |

Result: an installed 5.0.0 file is byte-identical to the file at the `v5.0.0` tag, so the sha256 of each file at the tag is the proof. Nothing rewrites content and nothing records a receipt. The commands target is the `--target` option (default `~/.claude/commands/sc`), passed to `install_commands` at `main.py:188` and `main.py:372`; skills and agents always use `~/.claude/skills` and `~/.claude/agents`.

## 3. Where the new step plugs in

| Reference | Today | Change |
|---|---|---|
| `src/superclaude/cli/main.py:255-267` | Step 9: MCP retire step, wrapped in `try/except`, never changes the exit code | Add Step 10 right after it (same wrapper) that calls the new file retire step with `target_path`. Placed after, so the MCP step's line numbers do not move |
| `src/superclaude/cli/main.py:269-280` | exit code is decided from the install phases | unchanged logic; the new step is not part of it |
| `src/superclaude/cli/main.py:407-415` | `update` prints the MCP retire notice (read-only) | Add the same file retire step before it, with `target_path` (update calls the installers with `force=True`, `main.py:372-384`) |
| `src/superclaude/cli/main.py:46-59, 340-350` | `install` and `update` docstrings (the `--help` text) | one sentence each. `tests/cli/test_help_examples.py:21` only invokes `update --help`; no text pin |
| `update.sh:7-10` | `pipx install --force ./`, `superclaude install --force` | no change: it reaches the step through `install --force` |
| `src/superclaude/cli/install_retired_mcp.py` | the model: module docstring, `Finding`, `classify_*`, `run_retire_step`, never raises into the caller | Mirror its shape in a new `src/superclaude/cli/install_retired_files.py`; do not import from it (different concerns) |
| NEW `src/superclaude/cli/install_retired_data.py` | -- | generated data: source tag, `{name: sha256}` for commands and agents, `{name: {relative path: sha256}}` for skills |
| NEW `scripts/gen_retired_install_data.py` | -- | the generator (`--tag <prev tag>`, `--check`); lives with the other repo scripts |
| `src/superclaude/cli/doctor.py:230` | doctor warns about retired MCP only | no change (out of scope) |
| `src/superclaude/cli/install_skills.py:70-135` | skills install loop | no change; the new step stays out of `install_*` so the existing "installers never delete" tests (`tests/cli/test_how_we_work_install.py:53-95`) keep their meaning |

Callers (codegraph): `install_commands` is called by `install` and `update` in `main.py` and by tests only; `install_all_skills` and `install_agents` the same. The new step has exactly two production callers, `install` and `update`.

## 4. Launch-level guard (the known follow-up)

| Reference | Change |
|---|---|
| `src/superclaude/hooks/scripts/launch-level-guard.sh:409` | `implement \| task \| improve \| cleanup)` -> `implement \| task \| cleanup)` and drop the trailing comment |
| `plugins/superclaude/hooks/scripts/launch-level-guard.sh:409` | tracked, byte-identical copy: same edit (the `.claude/hooks/` mirror comes from `make sync-dev`) |
| `tests/hooks/test_launch_level_guard.py:918-920` | remove `"sc:improve"` and its comment from `IMPL_SPELLINGS` |
| `tests/hooks/test_launch_level_guard.py:79-85` | `_REMOVED_COMMAND_TEXT` stays: it rewrites the historical design text, which still names `/sc:improve` |
| `tests/hooks/test_launch_level_guard.py:936-940` | add `sc:improve` to the look-alike names that stay NONE (proves the new behavior) |

Decision with evidence (to repeat in the PR body): the guard sees a name only in the `Skill` tool branch (`launch-level-guard.sh:392-414`) and releases only on a first line `/sc:implement` or `/task` (`:344`). The old `improve.md` (`git show v5.0.0:src/superclaude/commands/improve.md`) has no `Skill` activation line and no `allowed-tools`, so running it never produces a `Skill` call named `improve`; no skill named `improve` ever shipped (`git ls-tree v5.0.0 src/superclaude/skills/` has none). A kept, customized copy therefore reaches the guard exactly as it did for `spawn` and `build` (PRs 5 and 7 already removed those names): through no classifier. Keeping `improve` in the list guards nothing, so remove it and keep the guard otherwise unchanged. `spawn` and `build` at `v5.0.0` also never activated a skill named after them (checked below with `git show`).

## 5. Tests

| Reference | Change |
|---|---|
| NEW `tests/cli/test_install_retired_files.py` | static shape checks; generator checks against a throwaway git repo (no dependency on the tag); the upgrade test from the `v5.0.0` tag (skips with a reason when the tag is absent) |
| `tests/unit/test_cli_install.py:471-478` | the `_isolated_home` fixture is the model for a throwaway HOME |
| `tests/cli/test_install_retired_mcp.py:514-534` | `_INSTALLERS` and `_stub_framework` stub the installers and the codegraph phase for CLI-level runs; reuse the idea |
| `tests/hooks/test_launch_level_guard.py` | see section 4 |
| `tests/cli/test_install_keep.py::test_same_content_is_true_only_for_identical_readable_files` | known failing on integration before any edit; not mine |

## 6. Docs that describe the installer (not historical records)

| Reference | Change |
|---|---|
| `docs/getting-started/upgrading.md:225-236` ("Files 5.0.0 no longer ships": "The installer never deletes files") | Add a section for 6.0.0: the retire step, what it removes, what it keeps and prints, the command to remove a kept item. The old sentence stays true for core files only, so qualify it |
| `docs/getting-started/installation.md:54-70, 280-284` | one paragraph on the step and that `--force` and `update` both run it |
| `docs/developer-guide/technical-architecture.md` (installer section) | add the step to the install order |
| `docs/developer-guide/release-procedure.md` (release preparation) | add: regenerate the retire data from the previous tag (`scripts/gen_retired_install_data.py`) |
| `docs/developer-guide/codegraph-integration.md:64-67, 101` | cite `main.py` line numbers; refresh the ones the new step shifts |
| Not edited | `docs/releases/`, `docs/testing/v5.0.0/`, `docs/designs/`, `CHANGELOG.md` (the release PR adds the entry) |

## 7. Generated copies

`src/superclaude/` is the source; `make sync-dev` refreshes `.claude/` (never staged). Hook scripts also exist in `plugins/superclaude/hooks/scripts/` (tracked, edited by hand above). New Python modules need no sync.
