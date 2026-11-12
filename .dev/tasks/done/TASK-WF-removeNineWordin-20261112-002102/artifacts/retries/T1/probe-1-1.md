55cb1afbedc5de3eadad0ad35adfdd1a97914451
family: plugin-twin-sync
defect form: src/superclaude/core/CODEGRAPH.md changed without the byte-identical plugins/superclaude/core/CODEGRAPH.md twin
command: grep -n 'bounded wait' plugins/superclaude/core/CODEGRAPH.md src/superclaude/core/CODEGRAPH.md
before:
src/superclaude/core/CODEGRAPH.md:74:7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'` (skip it while one runs); the MCP `codegraph_status` takes the bounded wait of section 2 step 3 instead.
coupled sites: tests/core/test_codegraph_guide.py:134 (byte-identity test); no other twin of this guide
after:
plugins/superclaude/core/CODEGRAPH.md:74:7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'` (skip it while one runs); the MCP `codegraph_status` takes the bounded wait of section 2 step 3 instead.
src/superclaude/core/CODEGRAPH.md:74:7. Guard every CLI `status` with `pgrep -f 'codegraph\.js (init|index)'` (skip it while one runs); the MCP `codegraph_status` takes the bounded wait of section 2 step 3 instead.
