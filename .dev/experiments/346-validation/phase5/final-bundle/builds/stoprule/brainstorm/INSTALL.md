# Install note: `/sc:spec-panel-stoprule` (issue #346, stoprule)

Built by the `/sc:implement` run of `.dev/tasks/to-do/TASK-WF-spec-20261108-181616/` (archived to `.dev/tasks/done/` when the run completes). Nothing here is installed by that run; the coordinator installs it. Design: `docs/designs/spec-panel-stoprule.md`.

## 1. Files and where they go

| Repo path | Destination | Installed? |
|---|---|---|
| `src/superclaude/commands/spec-panel-stoprule.md` | `~/.claude/commands/sc/spec-panel-stoprule.md` | yes |
| `src/superclaude/skills/sc-spec-panel-stoprule-protocol/SKILL.md` | `~/.claude/skills/sc-spec-panel-stoprule-protocol/SKILL.md` | yes |
| `src/superclaude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` | `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md` | yes |
| `src/superclaude/skills/sc-spec-panel-stoprule-protocol/refs/canaries.json` | `~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/canaries.json` | yes |
| `src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py` | `~/.claude/skills/sc-spec-panel-stoprule-protocol/scripts/stoprule.py` | yes |
| `src/superclaude/agents/finding-grader.md` | `~/.claude/agents/finding-grader.md` | yes |
| `tests/skills/test_stoprule_script.py` | none | not installed |
| `tests/skills/test_spec_panel_stoprule.py` | none | not installed |
| `tests/skills/fixtures/stoprule/` (`spec-panel-armb-base.md`, `ctl-r1/`) | none | not installed |
| `tests/recommend/test_routing_refresh.py` (one allow-list line) | none | not installed |
| `docs/designs/spec-panel-stoprule.md`, `docs/designs/spec-panel-review-loop.md` (one pointer line) | none | not installed |
| `.dev/brainstorms/346-stoprule/briefs/` (the brief templates of section 7) | none | not installed |

## 2. The command's base (owner ruling)

There is no separate measurement copy: the repo file `src/superclaude/commands/spec-panel-stoprule.md` is the file to install. It is built from the 472-line Arm B base, `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/inputs/tool-text/spec-panel-post427-95f2c6e4.md` (sha256 prefix `c8d80346a96c`; a byte-identical copy is `tests/skills/fixtures/stoprule/spec-panel-armb-base.md`), plus the stoprule edits only. Variant: 481 lines, sha256 `c3f7377b8e422849369f0a1c1c53c5d0b71d1928ca60e45200b3cfd4e3b090ee`. It is the 472 base lines with the stoprule edits plus a `## Activation` heading (and its blank line) above the `> Skill sc:spec-panel-stoprule-protocol` line, added by owner ruling on 2026-11-08 because `make lint` (lint-architecture Check 6) requires that heading in every command paired with an `sc-*-protocol` skill.

The variant deliberately has no `## Unattended mode` section (the base has none) and does not accept `--unattended`: dispatch it without `--unattended`.

Rubric: `refs/rubric.md` sha256 `dbc4926c7421d51337e6963f28116d74dcbebde2deac018857882922bc6d4d61` (prefix `dbc4926c7421`). `begin` refuses a rubric that differs from the loop's review-1 hash.

## 3. Experiment install (three copies, no overwrite, the original verified unchanged; agent and skill before the command)

Run from the repo root of this worktree. The first line removes a bytecode cache a local test run can leave in the skill folder, so `cp -r` copies only the four skill files.

```
rm -rf src/superclaude/skills/sc-spec-panel-stoprule-protocol/scripts/__pycache__
sha256sum ~/.claude/commands/sc/spec-panel.md > /tmp/spec-panel.before
test ! -e ~/.claude/agents/finding-grader.md
test ! -e ~/.claude/skills/sc-spec-panel-stoprule-protocol
test ! -e ~/.claude/commands/sc/spec-panel-stoprule.md
cp src/superclaude/agents/finding-grader.md ~/.claude/agents/finding-grader.md
cp -r src/superclaude/skills/sc-spec-panel-stoprule-protocol ~/.claude/skills/
cp src/superclaude/commands/spec-panel-stoprule.md ~/.claude/commands/sc/spec-panel-stoprule.md
sha256sum -c /tmp/spec-panel.before          # must print OK
```

Stop at the first `test ! -e` that fails: something is already installed under that name. After the copy, record the sha256 of the three installed items in the run log and re-check them before each review dispatch:

```
sha256sum ~/.claude/agents/finding-grader.md ~/.claude/commands/sc/spec-panel-stoprule.md
find ~/.claude/skills/sc-spec-panel-stoprule-protocol -type f | sort | xargs sha256sum
```

**Rollback:** delete the three installed paths (`~/.claude/agents/finding-grader.md`, `~/.claude/skills/sc-spec-panel-stoprule-protocol/`, `~/.claude/commands/sc/spec-panel-stoprule.md`).

## 4. Repo install route

`uv run superclaude install` without `--force` adds the three new items and skips every file that already exists, so `spec-panel.md` is untouched. Never pass `--force` on the experiment machine: it overwrites every installed command, `spec-panel.md` included.

## 5. Brief substitution (Arm B briefs only)

```
perl -pe 's#(/?sc:spec-panel)(?![-\w])#$1-stoprule#g' brief.md > brief.stoprule.md
```

Checks after each substitution:

- `grep -c 'spec-panel-stoprule' brief.stoprule.md` equals `grep -c 'sc:spec-panel' brief.md`.
- The substituted review-3 brief still contains `any finding of any severity is FAIL` verbatim (owner decision: the brief text is not edited): `grep -c 'any finding of any severity is FAIL'` gives the same count in both files.
- `diff brief.md brief.stoprule.md` shows only command-name changes plus, in the review 2 and 3 briefs, the one `--re-review <prior report> --baseline <saved copy>` clause.

Apply it to the Arm B briefs only (reviews 2 and 3 pass `--re-review` and `--baseline`); with briefs that omit those flags the ratchet and hunk coverage are off (`ratchet=off` in the sentinel). The ready-made templates in section 7 already carry the substitution and the clauses.

## 6. Who runs which step (owner ruling)

Reviewer and reviser sessions run only script calls that write no file (`--dry-run`, `grade-prep`, `audit-prep`, `status`, `verdict`, `check`). The coordinator runs every call that writes the report as its own inserted step: `begin` before the reviewer, `seal`, the grader and auditor Agent calls with `apply-grades` and `apply-audit`, and `finalize` after it, then `check` before the reviser. The step table is in `~/.claude/skills/sc-spec-panel-stoprule-protocol/SKILL.md`; the inserted steps are the coordinator templates of section 7.

## 7. Brief templates (`.dev/brainstorms/346-stoprule/briefs/`)

| File | Use |
|---|---|
| `T05-R1-reviewer-L11-699ae853.txt` | review 1 reviewer brief (substituted) |
| `T06-R1-reviser-L10-3bb70411.txt` | fix cycle 1 reviser brief (unchanged text; no command name) |
| `T07-R2-reviewer-L11-aff19d65.txt` | review 2 reviewer brief (substituted, `--re-review`/`--baseline` clause added) |
| `T08-R2-reviser-L10-66468bab.txt` | fix cycle 2 reviser brief |
| `T09-R3-reviewer-L11-1c9a7ec8.txt` | review 3 reviewer brief (substituted, clause added; "any finding of any severity is FAIL" kept) |
| `T10-R3-reviser-L10-458bdc00.txt` | the original's review-3 reviser brief (kept for completeness) |
| `coordinator-before-review.md` | inserted step: save the baseline, run `begin`, dispatch the reviewer |
| `coordinator-fix-cycle.md` | inserted step: seal, grade, audit, finalize, `check`, fill D1-Dk or NONE, `check-disposition` |
| `recorder-after-review.md` | recorder: `verify-transcript`, `count` (the owner's still-open count) |
| `offline-demotion-audit.md` | recorder: the offline demotion audit with `audit-sample` |
| `replay-gate.md` | pre-run replay gate over the six existing review-3 reports |

The originals are read-only under `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/briefs/task-text/`. The templates keep the originals' old repo-root path and per-round counts; the coordinator fills the worktree path, the counts and the reviser finding range at dispatch time.
