daf091791b274de69e219a80819834369813228d
family=hint-flag-definition-scope
defect form: blanket claim that no installed file defines a section's flags, while CLAUDE.md lists --c7/--tavily/--play
command: grep -n -E -e "no installed file defines|not in the MCP table|defines the hint flags" docs/user-guide/flags.md
before:
9:Since 5.0.0 no installed file defines the hint flags in this section or in Advanced Control Flags: `FLAGS.md` and `MODES.md` are no longer shipped, and old copies left in `~/.claude/` are not loaded. Claude knows these flags only if you explain them in your request.
29:`--morph` is not in the MCP table of the shipped `~/.claude/CLAUDE.md`; Morphllm is an optional server you install with `superclaude mcp --servers morphllm-fast-apply` (needs `MORPH_API_KEY`).
coupled sites: src/superclaude/core/CLAUDE.md:22-24 (advisory MCP flags); flags.md MCP Server Flags table
after:
9:Since 5.0.0 `FLAGS.md` and `MODES.md` are no longer shipped, and old copies left in `~/.claude/` are not loaded. The only hint flags an installed file still names are `--c7`, `--tavily` and `--play`, listed as advisory flags in the MCP table of the shipped `~/.claude/CLAUDE.md`. No installed file defines the other hint flags in this section or in Advanced Control Flags; Claude knows them only if you explain them in your request.
29:`--morph` is not in the MCP table of the shipped `~/.claude/CLAUDE.md`; Morphllm is an optional server you install with `superclaude mcp --servers morphllm-fast-apply` (needs `MORPH_API_KEY`).
