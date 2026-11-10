2d22cdca7e49b3ce5d37a021214388b8ce3fd056
## family uv-host-scope
defect form: a host requirement narrower than the plan instruction
command: grep -n -e "uv" .dev/brainstorms/346-ledger/INSTALL.md
before:
25:Record the three `sha256sum` lines in the install watcher. Nothing else in `~/.claude/` changes: `~/.claude/commands/sc/spec-panel.md` stays as it is, and no `superclaude install` runs. Every worker host that runs the ledger steps needs `uv` (every call is `uv run --no-project python "<skill base>/scripts/review_ledger.py" ...`, with `<skill base>` = `~/.claude/skills/sc-review-ledger`).
coupled sites: none
after:
25:Record the three `sha256sum` lines in the install watcher. Nothing else in `~/.claude/` changes: `~/.claude/commands/sc/spec-panel.md` stays as it is, and no `superclaude install` runs. Every worke
