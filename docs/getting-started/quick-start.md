# Quick Start

Before you start, you need Python 3.10 or later, git, the Claude Code CLI `claude` on your `PATH` (`claude --version` must work), and network access to GitHub. `superclaude install` exits 1 if its codegraph step cannot find `claude` or cannot get codegraph (it reuses a matching `codegraph` on `PATH` or in `~/.local/bin`, otherwise it downloads one from GitHub).

Already have IronClaude installed? Follow [Upgrading to IronClaude 5.0.0](upgrading.md) instead of step 1.

1. **Install IronClaude.** Follow the [Installation Guide](installation.md). It installs the slash commands, agents, skills, and the How We Work guide into `~/.claude/`. Restart Claude Code after installing so it loads the new files and the codegraph server.
2. **Pick the right tool for your job.** Read [How We Work](../user-guide/how-we-work.md). It tells you how much process a job needs and which commands to run, in order.
3. **Not sure?** Run `/sc:recommend "<what you want to do, and why>"` inside Claude Code. Run `/sc:help` to see every installed command and skill.

For the exact syntax of each command, see the [Commands Reference](../user-guide/commands.md).
