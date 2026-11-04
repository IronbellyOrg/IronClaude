---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: standard
slug: TASK-WF-closeIronbellyOr-20261104-084334
version: "1"
priority: Medium
created_date: "2026-11-04"
---

# Install the Ponytail plugin on every workspace (issue #330)

Source: ./source.md
Goal: `superclaude install`, `superclaude update` and `update.sh` install `ponytail@ponytail` from `DietrichGebert/ponytail` with `PONYTAIL_DEFAULT_MODE=off`, a failed plugin is reported by name, and docs and CHANGELOG describe the behaviour, footprint, opt-out and upgrade step. Design: `.dev/brainstorms/20261104-063430-ponytail-plugin-install/merged-requirements.md` (the "design spec" below).

## Constraints

- Change only these delivery files: `src/superclaude/cli/user_settings_defaults.json`, `src/superclaude/cli/install_user_setup.py` (at most 5 changed lines), `tests/cli/test_install_user_setup.py`, `docs/getting-started/installation.md`, `CHANGELOG.md`. Do not edit `src/superclaude/cli/main.py`, `update.sh`, `src/superclaude/cli/doctor.py`, `src/superclaude/output-styles/`, any skill, command, agent or hook, or anything under `.claude/` (design spec FR-006, FR-008, AC-2).
- A default plugin is added by data only; there is no Ponytail-specific Python. The only Python change is the shared failure-label fix (design spec NFR-003, FR-005).
- Ponytail comes only from `DietrichGebert/ponytail`; no version pin (design spec FR-002, R5).
- Never run `superclaude install`, `superclaude update`, `./update.sh` or any `claude plugin` command against this workspace's `~/.claude`, and never install or enable a plugin in this workspace. Manual evidence uses a throwaway `HOME` under `/tmp`, removed afterwards.
- Plugin failures stay non-fatal: `install_plugins` returns `ok=True` on every path (design spec NFR-001).
- Ledger default: this plan implements design spec 3.1a Outcome 2 (Ponytail's own default, no `pluginConfigs` entry), the recommendation sent to the coordinator. If the coordinator picks "off+ledger-off" before Task 1 runs, Task 1 also adds `"pluginConfigs": {"ponytail@ponytail": {"options": {"ledger": false}}}` with a T1 assertion, and Tasks 3 and 4 use the Outcome 1 ledger sentence instead.
- `.dev/tasks/` is staged with `git add .dev/tasks` (this package and its `artifacts/` included). Staging is not committing.

## Phase 1: Ship Ponytail through the plugin defaults

## Task 1: Add the three Ponytail entries to the defaults and pin them with tests

Edit `src/superclaude/cli/user_settings_defaults.json` (design spec 3.1, FR-001..FR-003):
- In `env`, add `"PONYTAIL_DEFAULT_MODE": "off"` after the two existing entries.
- In `enabledPlugins`, append `"ponytail@ponytail": true` after `"understand-anything@understand-anything": true` (append-last convention only; order is not a budget lever, design spec 3.1 "Order").
- In `extraKnownMarketplaces`, append `"ponytail": {"source": {"source": "github", "repo": "DietrichGebert/ponytail"}}` after `understand-anything`.

Add and extend tests in `tests/cli/test_install_user_setup.py` (design spec "Tests and Acceptance Criteria" T1, T2, T3/T4):
- T1: new `test_defaults_ship_ponytail` that loads `user_settings_defaults.json` (same path the existing install test uses, `Path(setup.__file__).parent / "user_settings_defaults.json"`) and asserts `enabledPlugins["ponytail@ponytail"] is True`, `extraKnownMarketplaces["ponytail"]["source"] == {"source": "github", "repo": "DietrichGebert/ponytail"}`, `env["PONYTAIL_DEFAULT_MODE"] == "off"`, and that for every `enabledPlugins` key the text after `@` names an `extraKnownMarketplaces` entry with a `source.repo`. T1 must not assert key order.
- T2: in `test_plugins_install_missing_enabled_defaults`, assert `["plugin", "marketplace", "add", "DietrichGebert/ponytail"] in calls` and `"ponytail@ponytail" in installs`, next to the existing marketplace and install assertions.
- T3/T4: extend `test_settings_defaults_fill_only_missing_values` (or add sibling tests in the same style) with two legs. Leg 1 (existing user): settings hold the six pre-existing `enabledPlugins` entries and the two pre-existing marketplaces; after `apply_settings_defaults` the three Ponytail keys are present with the default values, the pre-existing entries are unchanged, and a second run returns `(True, "✅ Settings defaults: already present")`. Leg 2 (user choice kept): settings hold `enabledPlugins["ponytail@ponytail"] = False` and `env["PONYTAIL_DEFAULT_MODE"] = "full"`; both are unchanged after `apply_settings_defaults`.

Acceptance criteria:
- `src/superclaude/cli/user_settings_defaults.json` parses as JSON and contains exactly the three new entries above; no other key changes (`git diff` of the file shows only added lines plus the comma changes they need).
- `uv run pytest tests/cli/test_install_user_setup.py -v` passes, including T1, T2 and both T3/T4 legs; output saved to `./artifacts/t1-pytest.log`.
- Reverting only the JSON change makes T1, T2 and T3/T4 leg 1 fail (demonstrated once and noted in `./artifacts/t1-pytest.log`).

## Phase 2: Name failed plugins in the install report

## Task 2: Fix the plugin failure label and test both failure paths and the missing-CLI branch

Depends on: Task 1

In `install_plugins` in `src/superclaude/cli/install_user_setup.py` (design spec 3.2, FR-005): today a failed `plugin install` is appended as `args[3]`, which is `"--scope"`, and a time-limited one as `install <id> --scope (time limit)`. Compute one name per command (the repo for `["plugin", "marketplace", "add", <repo>]`, the plugin id for `["plugin", "install", <id>, "--scope", "user", "-y"]`) and use it on the time-limit path (`f"{name} (time limit)"`), the non-zero-exit path and the exception path. Do not change the return values, the `ok=True` contract, the message prefixes or the retry sentence. At most 5 changed lines in this file.

Tests in `tests/cli/test_install_user_setup.py` (design spec T5, T5c):
- T5: extend `test_plugin_failures_and_time_limit_never_fail_install` (fixture enables only `playwright@claude-plugins-official`). Non-zero-exit leg: `ok is True`, the message contains `anthropics/claude-plugins-official` and `playwright@claude-plugins-official`, and `"--scope" not in message`. `deadline=0` leg: `ok is True`, the message contains `(time limit)` and both names, and `"--scope" not in message`.
- T5c: new test that monkeypatches `setup.shutil.which` to return `None` and asserts `setup.install_plugins(home=tmp_path) == (True, "⏭️  Plugins: claude CLI not found; skipped")`.

Acceptance criteria:
- `git diff src/superclaude/cli/install_user_setup.py` shows at most 5 changed lines, all inside `install_plugins`.
- T5 fails on the pre-fix code (both legs report `--scope`) and passes after the fix; T5c passes; both results recorded in `./artifacts/t2-pytest.log`.
- `uv run pytest tests/cli/test_install_user_setup.py tests/cli/test_update_command.py tests/unit/test_cli_install.py -v` passes (log in `./artifacts/t2-pytest.log`).
- `make lint` and `uv run ruff format --check src/ tests/` pass (output appended to `./artifacts/t2-pytest.log`).

## Phase 3: Document the behaviour

## Task 3: Update the installation guide

Depends on: Task 1

Edit `docs/getting-started/installation.md` at the default-plugins paragraph (currently "six plugins, including `playwright` and `frontend-design`"), following the design spec "Docs and CHANGELOG" installation block:
- Replace the count with a count-free sentence naming `playwright`, `frontend-design` and `ponytail`; keep the existing budget and retry sentences.
- Add the Ponytail paragraph: what it adds (`ponytail-*` skills, `/ponytail`); installed with `PONYTAIL_DEFAULT_MODE=off` unless already set; what `off` stops (ruleset, codebase map, statusline offer, subagent context) and what still runs (band above the prompt, `git grep` at session start, Edit/Write watch, per-turn ledger row under `$XDG_CONFIG_HOME/ponytail/band/` or `~/.config/ponytail/band/`); `/ponytail band off` hides only the band; the Outcome 2 ledger sentence ("The ledger is on by default; set Ponytail's `ledger` option to `false` to stop it."); `/ponytail <level>` applies to every session in that repo and a new session in `off` switches it back; bare `/ponytail` means `full`; `PONYTAIL_DEFAULT_MODE` overrides `/ponytail default <mode>`; opt out with `"ponytail@ponytail": false` in user settings (a project `.claude/settings.json` wins; do not delete the key); existing workspaces need the IronClaude package upgraded first (`git pull` before `./update.sh` for a checkout), then `superclaude update` or `superclaude install`; hooks need `node`; the Orca-budget known limitation sentence from design spec "Known Limitations and Follow-ups".
- Keep the paragraph in the file's existing Markdown style and line wrapping.

Acceptance criteria:
- `grep -rn "six plugins" docs/` returns nothing.
- The paragraph contains every item listed above (checked item by item against the design spec block; checklist saved to `./artifacts/t3-docs-check.md`).
- No placeholder text (`<LEDGER SENTENCE`) remains in the file.
- `make lint` passes.

## Task 4: Add the CHANGELOG entry

Depends on: Task 2

Under `## [Unreleased]` in `CHANGELOG.md`, add the entry from the design spec "Docs and CHANGELOG" CHANGELOG block, in the file's `### <topic>` / `#### <Kind> (<topic>)` style: `### Ponytail plugin installed by default (#330)`, `#### Added (default plugins)` with the install, mode, footprint, Outcome 2 ledger sentence, opt-out, upgrade-step and `node` bullet plus the migration bullet for existing Ponytail users (`PONYTAIL_DEFAULT_MODE=off` wins over their `config.json`, and `/ponytail default <mode>` reports success but has no effect), and `#### Fixed (plugin install report)` for the failure label.

Acceptance criteria:
- `CHANGELOG.md` has the new section directly under `## [Unreleased]`, above `## [5.0.0]`, with no `<LEDGER SENTENCE` placeholder.
- The Fixed bullet describes the Task 2 behaviour exactly (failed plugins named by id or marketplace repo, no `--scope`).
- `make lint` passes.

## Phase 4: Install evidence and PR handoff text

## Task 5: Record install evidence from a throwaway HOME

Depends on: Task 2

In a throwaway directory created with `mktemp -d /tmp/ic330-e2e.XXXXXX`, run the changed user-setup path with `env -i HOME=<tmp>/home PATH=<curated> ...` (no `CLAUDE_CONFIG_DIR`; Orca CLIs shadowed by failing stubs as in `.dev/releases/current/v5.0.0/post-release/scan/C-install-surface.md` "Recommended recipe"), calling `apply_settings_defaults` and `install_plugins` from this checkout via `uv run python`. Never touch `/home/coder/.claude`. Record design spec AC-M1 and AC-M3 results (all non-blocking):
- M1a: `<tmp>/home/.claude/plugins/installed_plugins.json` lists `ponytail@ponytail`; `known_marketplaces.json` has the key `ponytail`; a second `install_plugins` run returns exactly `✅ Plugins: already installed`; no prompt or hang with closed stdin.
- M1c (file part): the `ponytail-*` skill files exist under the installed plugin directory. The session part (skills listed, `/ponytail lite` switches the mode) and M1b (env reaches the hook) only if a Claude session can start in that HOME; otherwise record them as UNVERIFIED with the reason.
- AC-M3: with `claude` absent from `PATH`, `install_plugins` returns the skip line.
- Remove the throwaway directory at the end.

Acceptance criteria:
- `./artifacts/ac-m1-evidence.md` lists M1a, M1b, M1c and AC-M3 with PASS, FAIL or UNVERIFIED, the exact commands run and their key output lines.
- `stat -c %Y /home/coder/.claude/settings.json` and `ls /home/coder/.claude/plugins/` are recorded before and after and are unchanged.
- The throwaway directory no longer exists (recorded).
- A FAIL is recorded as a follow-up in `./artifacts/ac-m1-evidence.md`, not fixed in this plan.

## Task 6: Draft the PR description with the Coder handoff and known limitation

Depends on: Task 4, Task 5

Write `./artifacts/pr-body.md`: a plain-text summary of the change (defaults entries, mode `off`, the band and ledger footprint, failure-label fix, docs, CHANGELOG); `Closes #330`; the known-limitation sentence verbatim from design spec "Known Limitations and Follow-ups"; a one-paragraph Coder handoff summary with the four questions from design spec "Coder Handoff"; the Task 5 evidence summary; the follow-ups list (Orca probe budget, `doctor` plugin report, and any Task 5 FAIL); and the ledger default decision status.

Acceptance criteria:
- `./artifacts/pr-body.md` exists, contains `Closes #330`, the limitation sentence, all four Coder questions and the follow-ups, and ends with the line `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
- It names no upstream repository other than `IronbellyOrg/IronClaude` and `DietrichGebert/ponytail`.
