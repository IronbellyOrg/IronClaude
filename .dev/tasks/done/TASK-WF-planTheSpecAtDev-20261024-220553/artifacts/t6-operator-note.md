# Operator note: pragmatic output style severity carve-out

The repo copy `src/superclaude/output-styles/pragmatic.md` now carries the clause "except inside a protocol that defines its own severity model, such as `/sc:implement`" on its "Any issue of ANY severity" line.

`superclaude install` without `--force` skips an existing installed style file, so on other hosts apply the same one-clause edit to `~/.claude/output-styles/pragmatic.md` by hand, or delete that one file and re-run `superclaude install`. Do not run `superclaude install --force`: it overwrites every installed framework file.
