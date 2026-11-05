909e1d562fe164c74387e9e81ef63ebec00e4db8
family=docs-claims-installer-reports-residuals
defect form: user-guide text that says the installer "reports" a residual (a kept or untouched registration) when the code reports it only for some names or not at all
search: git grep -n -E -e 'reported' -e 'kept and' -e 'never removed' -- docs/user-guide/mcp-installation.md docs/reference/mcp-server-guide.md CHANGELOG.md README.md
before:
CHANGELOG.md:141:- `/sc:pr-submit` with no `--monitor` now runs level 3 (`DEFAULT_MONITOR = 3` in `superclaude.pr_submit.fsm`). A bare `/sc:pr-submit` now fixes the confirmed review findings of Medium severity or higher (lower ones are only reported) and faili
docs/user-guide/mcp-installation.md:54:In the first `superclaude install` where codegraph is registered and usable (`Ready for Serena retirement: yes` in `install --list`), the cleanup step also removes every user-scope MCP entry other than `serena-local` that
docs/user-guide/mcp-installation.md:56:Kept by policy: `~/.serena`, project `.serena/` folders, `~/.cache/codebase-memory-mcp`, the uv cache and, outside Coder, a `serena-agent` uv tool you installed (the removal command is printed). Local-scope (`projects.*.m
coupled sites: docs/user-guide/mcp-installation.md lines 54 and 56 (the two paragraphs of the Serena section); CHANGELOG.md line 13 (the retire bullet says Serena launchers are removed, which is true) is not coupled
after:
CHANGELOG.md:118:- `ccsession ... --claude-args <claude args>`: everything after `--claude-args` goes to Claude Code exactly as given, after any label, and is never read as a label or a ccsession opti
CHANGELOG.md:135:- The `--yes` flag of `/sc:pr-submit`. It was accepted but never read.
CHANGELOG.md:141:- `/sc:pr-submit` with no `--monitor` now runs level 3 (`DEFAULT_MONITOR = 3` in `superclaude.pr_submit.fsm`). A bare `/sc:pr-submit` now fixes the confirmed review findings of Medium
docs/user-guide/mcp-installation.md:54:In the first `superclaude install` where codegraph is registered and usable (`Ready for Serena retirement: yes` in `install --list`), the cleanup step also remov
docs/user-guide/mcp-installation.md:56:Kept by policy: `~/.serena`, project `.serena/` folders, `~/.cache/codebase-memory-mcp`, the uv cache and, outside Coder, a `serena-agent` uv tool you installed 
