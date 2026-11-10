# Codebase context: 346-diffgate

Source tier: fallback_1 (auggie codebase-retrieval tool not available in this session; native Grep/Glob/Read and sed on this worktree at origin/master, 2026-11-08). Every fact below was read in this worktree.

## The current contract (PR 427)
- `src/superclaude/commands/spec-panel.md` (486 lines): Usage line 22 carries `[--re-review <prior-findings-file> --baseline <saved-copy>]`; `## Review Loop` at line 256 has 7 single-line bullets (Mode, Grading, Verdict, Cap, Re-review output, Reviser contract, Precedence); `## Unattended mode` at line 451 (`--report-dir` only; `report_path` = `--output` file or `<report-dir>/spec-panel-report.md`; Improve step only with `--improve`).
- Bullet 5 asks the reviewer to find "lines changed against the baseline, ignoring whitespace-only changes" and self-tag `origin=changed|unchanged`. Nothing computes the diff; nothing checks the tags. The Arm B R3 reviewer ran `git diff --no-index -w` itself (flg-r2 `spec-panel-round3.md` Self-Audit).
- Design doc `docs/designs/spec-panel-review-loop.md` section 12: "Prose only: a coordinator that drops the flags or the saved copy starts a fresh first review, and nothing enforces the count." Section 9: "The tests prove the text is present and in the right order, not that a reviewer obeys it."
- Plugin mirror `plugins/superclaude/commands/spec-panel.md` exists (edited in place for 427; one-word drift at line 219).

## Tests that pin the area
- `tests/skills/test_spec_panel_review_loop.py` (T1-T10 text presence, parametrised over src and plugin spec-panel copies).
- `tests/skills/test_review_severity_rule.py` (canonical cap text `CANONICAL_CAP_TEXT`, `AT_CAP_CLAUSES`; bans a cap number above 2 outside `sc-implement-protocol`; scans `src/`, `plugins/`, `commands/`, `agents/`). A new command file is scanned too.
- `tests/skills/test_worker_contract.py`: `P2_COMMANDS` and `UNATTENDED_EXPECT` list `spec-panel`; a new variant command is not in those lists (additive; no test enumerates every command's Unattended section from the list side, UNVERIFIED beyond lines 415-440 and 915-935).

## Prior art for a mechanical re-review
- `/sc:implement` QA (`src/superclaude/skills/sc-implement-protocol/refs/qa.md`): reviewer writes structured finding lines with `at=`, `anchor=`, `origin=<inherited|late|fix-induced|new|unknown>`; the PARENT Reads each anchor back and derives the verdict ("nobody rewrites a recorded verdict", line 97); inherited text is "capped at note, mechanically from the `git diff "$start"` hunk headers" (line 166); "later reviews cannot re-open accepted text with a lower-severity finding" (line 186); each prior blocking finding gets `resolved|open|regressed` (line 143). This is the nearest existing mechanical model: reviewer proposes, parent computes.
- Python stdlib `difflib` is already used in `src/superclaude/cli/eval/expect.py`; no new dependency needed for unified diffs.

## How primitives ship and call scripts
- Scripts ship inside skills: `src/superclaude/skills/<skill>/scripts/*.py` (e.g. `sc-implement-protocol/scripts/archive_workspace.py`, `sc-issue-protocol/scripts/origin_repo.py`). They are called as `uv run --no-project python "<skill base>/scripts/<name>.py" ...` (`refs/managed-workspace.md:54`, `sc-issue-protocol/SKILL.md:72`) and unit-tested (`tests/skills/test_workflow_archive.py`).
- `install_skills.py:167-170` installs a skill directory only if it holds `SKILL.md`; so a script needs a host skill (new `sc-spec-panel-diffgate-protocol` or similar) to reach `~/.claude/skills/`.
- Commands are single `.md` files copied by `install_commands.py` (existing files kept unless `--force`); a new command name is additive and does not overwrite `spec-panel.md`.
- Installed primitives may not name `src/superclaude/` paths (project CLAUDE.md); a command that runs a skill script names `~/.claude/skills/<skill>/scripts/...` and the project `.claude/skills/<skill>/scripts/...` copy (dual surface).

## Machine fact for testing
- A worker loads `/sc:<name>` from `~/.claude/commands/sc/<name>.md` before the project copy (DECISIONS.md D9). An experiment arm therefore installs `spec-panel-diffgate.md` (and the host skill folder) next to the original, and substitutes the command name in its briefs.
