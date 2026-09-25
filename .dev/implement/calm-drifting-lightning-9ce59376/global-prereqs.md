# Remaining global prerequisites (not done — each needs separate approval)

Repo changes on `fix/pr-submit-attended-ci-monitor` (uncommitted) do **not** arm level-3 CI monitoring
for future PRs. Until every item below is done and a live rehearsal passes, `/sc:pr-submit --monitor >= 1`
will STOP at the CI-wait preflight on this machine, which is the intended fail-closed behaviour.

Observed state (2026-09-25):

| Prerequisite | Current | Needed |
|---|---|---|
| `gh` CLI | `/usr/bin/gh` 2.45.0 (Ubuntu); `gh pr checks --help` has no `--json` | An approved `gh` whose own `gh pr checks --help` lists `--json` |
| Python package | pipx `superclaude` 4.3.5; `import superclaude.pr_submit.ci` → `ModuleNotFoundError` | A package build that includes `pr_submit/ci.py` (fork master or later) |
| Global skill | `~/.claude/skills/sc-pr-submit-protocol/SKILL.md` (2026-09-24 22:23) still says "`Monitor` tool" | Targeted refresh of that skill (and `~/.claude/commands/sc/pr-submit.md`) **after a backup** |
| Skill load | old description still listed in session | Fresh session; confirm the skill description says "attended in-session poll loop" |

Then: a live level-3 rehearsal on a future, safe PR, with a `--timeout` sized to the full CI matrix
(the observed matrix ran longer than the 600 s default).

Not run: `./update.sh`, replacing `/usr/bin/gh`, rebuilding pipx, overwriting `~/.claude/skills/`, commits, pushes.
