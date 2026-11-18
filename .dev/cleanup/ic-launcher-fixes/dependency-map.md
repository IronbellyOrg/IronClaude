# Dependency map: ic launcher fixes (#542, #543, #544)

Measured on `clayphi/v6-ic-launcher-fixes` at 551d5ad38 (= `origin/integration`) on 2026-11-17.
Method: codegraph (the script is bash, so it only indexes `cli/ic.py`), Grep over src, tests, plugins, docs, Makefile, pyproject.toml.

## Files the fixes touch

| Path:line | Change needed |
|---|---|
| `src/superclaude/scripts/ic:13-14` | #542: the header says values are looked up in `$IC_ALIASES`. The code never reads it. Rewrite to the real rule (a lowercase alias variable from `~/.aienv`; anything else passes through). Keep the usage block (lines 2-11) unchanged, since `--help` prints lines 2-15. |
| `src/superclaude/scripts/ic:33-46` (`resolve`) | #542: the indirect lookup accepts any identifier with a non-empty value (`HOME`, `PATH`, `LITELLM_API_KEY`). Restrict to lowercase-initial names; keep literal pass-through. All callers go through this one function: lines 61, 62, 63 (presets), 75, 76, 77 (`-H/-S/-O`), 89 (bare positional). |
| `src/superclaude/scripts/ic:72-77` | #543: `-p/-H/-S/-O` read `$2` unguarded under `set -u` (line 23). Add one shared check before each, so all four options print a clear message and exit 2. |
| `src/superclaude/scripts/ic:25-31` and `:80-82` | #544: `source "$AIENV"` runs before `-h/--help` is handled. Move help handling ahead of the source, using a pre-scan of the arguments that skips option values and stops at `--` (same rules as the main loop). |
| `src/superclaude/cli/sprint/aienv.py:39-40` | Comment only: cites `ic:61-63` and `ic:98`. Update the line numbers if the edit shifts them. No code change. |
| `tests/cli/test_ic_launcher.py` (new) | One failing-before, passing-after test group per issue, plus guards for the behaviour that must not change (valid alias, literal model, valid preset, unknown preset, `--` pass-through). |

## Mirrors and consumers (re-measured, no change needed)

- `.claude/` and `plugins/superclaude/`: no copy of `ic`. `make sync-dev` does not copy `src/superclaude/scripts/ic`; `plugins/superclaude/scripts/` holds only `__init__.py`, `clean_command_names.py`, `session-init.sh`. The plugin build (`scripts/build_superclaude_plugin.py:76`) copies `scripts` into `dist/` only.
- `src/superclaude/cli/ic.py:12-15`: runs `bash <script> "$@"`. Unchanged.
- `pyproject.toml` (`ic = "superclaude.cli.ic:main"`) and `tests/unit/test_cli_install.py:477,938-940`: assert packaging only. Unchanged.
- `src/superclaude/scripts/README.md` lists only the two python/shell utilities and does not name `ic`. Unchanged.
- `src/superclaude/skills/sc-reflect-protocol/refs/runtime-surface.md:45`: names the console-script entry point only. Unchanged.
- Historical records that describe these exact defects (`docs/testing/v5.0.0/user/D16-init-lite-recommend-ic.md:26-30,736-738`, `docs/testing/v5.0.0/post-release-manifest.json`): left as they are (rule from #571).

## Overlap with other wave 3 work

- `git log -- src/superclaude/scripts/ic`: one commit only (74bf717dc, PR #105). No merged PR since has touched the script.
- Open PRs on the fork at the time of writing: #619 (`docs/how-we-work`), #608 (style docs). Neither touches `scripts/ic`, `cli/ic.py` or `aienv.py`.
- PR 8 (`/sc:improve` removal) and small-fix PR A (help-text fixes) run in other worktrees; neither is expected to touch the `ic` script. Shared files such as `PROJECT_INDEX.*` and `docs/developer-guide/technical-architecture.md` are not touched by this PR, so there is nothing to conflict on.
- Two stale remote branches (`ironbelly/eval-severity-rule-test`, `ironbelly/eval-tasklist-review-panel`) show a diff on the script only because they branched before `integration` moved; not open PRs, ignored.

## Count check

Plan counts were taken at d4d1662a8. Re-measured here: 1 script, 1 comment reference file, 1 new test file; 0 mirrors.
