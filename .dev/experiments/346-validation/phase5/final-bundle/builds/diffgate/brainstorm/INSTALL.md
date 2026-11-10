# Install note: `/sc:spec-panel-diffgate` for the S1 experiment (issue #346)

This note tells the coordinator how to install the diffgate variant into `~/.claude` for the S1 runs. Nothing here has been installed yet; the worktree build wrote nothing under `~/.claude`.

## What was built, and where each file goes

| Repo path | Destination under `~/.claude/` |
|---|---|
| `src/superclaude/commands/spec-panel-diffgate.md` | `~/.claude/commands/sc/spec-panel-diffgate.md` |
| `src/superclaude/skills/sc-diffgate/SKILL.md` | `~/.claude/skills/sc-diffgate/SKILL.md` |
| `src/superclaude/skills/sc-diffgate/scripts/diffgate.py` | `~/.claude/skills/sc-diffgate/scripts/diffgate.py` |
| `tests/skills/test_diffgate_script.py` | not installed |
| `tests/skills/test_spec_panel_diffgate_command.py` | not installed |
| `tests/skills/fixtures/diffgate/` (every file, including `spec-panel-base-c8d80346a96c.md` and `flg-r1/`) | not installed |
| `docs/designs/spec-panel-diffgate.md` | not installed |
| `tests/recommend/test_routing_refresh.py` (edited: `spec-panel-diffgate` added to `_POST_REFRESH_ADDITIONS`) | not installed |
| `.dev/brainstorms/346-diffgate/briefs/` (every file: the templates, `source/`, `README.md`) | not installed |

`src/superclaude/commands/spec-panel.md` is NOT changed. `make sync-dev` also copied the command and the skill folder into the worktree's `.claude/` (gitignored dev copies); they are not an install.

## Owner rulings this build follows

- **Base file.** The variant is a copy of the 472-line Arm B command file `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/inputs/tool-text/spec-panel-post427-95f2c6e4.md` (sha256 first 12 characters `c8d80346a96c`), byte for byte apart from this team's change (frontmatter name and description, title, the Usage token `--diffgate-dir <dir> [--expect-round N]`, the seven Review Loop bullets, the new `## Diffgate` section, and `/sc:spec-panel` renamed to `/sc:spec-panel-diffgate`). It is NOT a copy of the current `src/superclaude/commands/spec-panel.md`, which minus its Unattended section is 474 lines, with two extra lines about `--unattended` and `--target-release`. The drift tests compare against the in-repo byte copy `tests/skills/fixtures/diffgate/spec-panel-base-c8d80346a96c.md`.
- **No Unattended section.** The variant deliberately has no `## Unattended mode` section, so a brief never passes `--unattended` to it.
- **Inherited `src/superclaude` line kept.** The base's `**Read**` bullet in `## Tool Coordination` names `src/superclaude/examples/release-spec-template.md`; it is kept byte for byte on purpose. The test asserts the variant adds no `src/superclaude` occurrence beyond the base's one. Removing it from the base is a separate follow-up.
- **Routing test.** The variant is added to `_POST_REFRESH_ADDITIONS` in `tests/recommend/test_routing_refresh.py`; `tests/skills/test_worker_contract.py` is unedited.
- **Who runs the script (design A).** The review and revision sessions run only read-only script calls (`status`, `check --dry-run`, `fixcheck --dry-run`), which write no file. Every writing call is a coordinator step inserted between the brief tasks, with its own brief template: `S-begin` (`begin`), `S-check` (`check`, then append `close-r<N>.md` to the report) and `S-fixcheck` (`fixcheck --map <disposition file>`). Order per replicate: `S-begin` r1, T05, `S-check` r1, T06, `S-fixcheck` r1, `S-begin` r2, T07, `S-check` r2, T08, `S-fixcheck` r2, `S-begin` r3, T09, `S-check` r3, then T11 (blindness audit). Details: `.dev/brainstorms/346-diffgate/briefs/README.md`.

## Install (adds two things, edits nothing)

Never run `superclaude install --force`: it rewrites every command file, `spec-panel.md` included.

Run from this worktree's root (`/home/coder/workspaces/worktrees/IronClaude/bs346-diffgate`):

```bash
sha256sum ~/.claude/commands/sc/spec-panel.md              # record; must be unchanged after every step
cp src/superclaude/commands/spec-panel-diffgate.md ~/.claude/commands/sc/spec-panel-diffgate.md
mkdir -p ~/.claude/skills/sc-diffgate && cp -R src/superclaude/skills/sc-diffgate/. ~/.claude/skills/sc-diffgate/
sha256sum ~/.claude/commands/sc/spec-panel-diffgate.md ~/.claude/skills/sc-diffgate/scripts/diffgate.py   # record in the run log
```

Re-run the first `sha256sum` after each step and confirm it has not changed. `superclaude install-skill sc-diffgate` also exists, but `cp` is preferred: it is explicit and cannot touch `spec-panel.md`. Workers load commands from `~/.claude/commands/sc/`, so a worktree-only copy is inert.

## Pre-run gate (before any replicate)

1. A worker in the experiment's permission mode runs `uv run --no-project python ~/.claude/skills/sc-diffgate/scripts/diffgate.py status --dir <a scratch dir>` through the installed path with no permission prompt.
2. The reviewer and reviser of a replicate run in one checkout and pass the same `--doc` real path, checked by a dry `begin` and `status` on a scratch directory.
3. A worker resolves `/sc:spec-panel-diffgate` after a restart.
4. The hashes above are recorded as in the install block.

## Brief changes

The one-line substitution in every review brief (reviews 1, 2 and 3):

```text
/sc:spec-panel <args>   ->   /sc:spec-panel-diffgate <args> --diffgate-dir <one directory per replicate> --expect-round <N>
```

Any `--re-review ... --baseline ...` in a brief is removed (the variant refuses them; the S1 originals carry none). The worker must invoke the command through the Skill tool, and its transcript must show the call (rule WC-7 of `~/.claude/WORKER-CONTRACT.md`: reading the command file and following it from memory does not count).

The one line the reviser briefs gain (both fix cycles), amended by design A, inserted immediately before `Finish with worker_done`:

```text
Your task list is <DIR>/reviser-brief-r<N>.md, not the whole report; after editing, run `uv run --no-project python ~/.claude/skills/sc-diffgate/scripts/diffgate.py fixcheck --dir <DIR> --doc .dev/orca-command-refactor/specs/orca-worker-contract-spec.md --map <disposition file> --dry-run` (read-only: it writes no file), put its `doc_sha:` line and one line per changed hunk (confirm or decline each candidate it prints) in a `## Diffgate fixmap` block inside <disposition file>, and repeat until it exits 0.
```

The T10 review-3 reviser brief is unchanged. The filled templates, the step briefs, the blindness audit and the scoring note are under `.dev/brainstorms/346-diffgate/briefs/` (see its `README.md`).
