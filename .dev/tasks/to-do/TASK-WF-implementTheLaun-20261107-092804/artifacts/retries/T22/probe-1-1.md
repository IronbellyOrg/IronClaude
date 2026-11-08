c3ed6e792050896f66c62b4b57c965eb7909edf1
family docs-stale-claim
defect form: a documentation sentence that still states the pre-change behaviour (warning only, not implemented, enforcement_status, enforces the level) or misattributes the ship gate
command: grep -rnE 'enforcement_status|nothing implemented|Design only|does not implement this proposed|enforces the level|U1 ship gate' docs/designs/sc-issue-claim-pipeline-flag.md docs/designs/sc-issue-launch-level-hook.md docs/user-guide/commands.md src/superclaude/commands/issue.md src/superclaude/skills/sc-issue-protocol/SKILL.md src/superclaude/skills/sc-issue-protocol/refs/claim.md
before-output:
the review listed pipeline-flag design lines 3, 30, 115, 133, 204, 210, 295 and the user guide line 381
coupled sites: docs/designs/sc-issue-command.md and docs/designs/spec-panel-review-loop.md also say Design only (nothing implemented) but describe other features (left alone)
after:
docs/designs/sc-issue-launch-level-hook.md:23:One script, `launch-level-guard.sh`, enforces the level that `/sc:issue --claim --pipeline <level>` gives a launched agent. Only sessions the claim script
