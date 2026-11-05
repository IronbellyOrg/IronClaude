a343d047bad737918e4654f319b571e1413c50f4
family=uncited-observed-output
defect form: expected result quotes exact codegraph CLI output whose only source is a local observation, not code/--help/transcript, and is not marked UNVERIFIED
command: grep -n -i -e "observed" -e "UNVERIFIED" -- docs/testing/v5.0.0/user/D03-codegraph-graph-impact.md
before:
11:- codegraph 1.6.2 installed by `superclaude install` and `~/.local/bin` on your `PATH`, so a bare `codegraph` resolves. `/sc:graph init` may only call bare `
118:**Expected result:** `pgrep` prints nothing (no init is running), then `CodeGraph Status`, `Project: /tmp/d03/repo`, `⚠ Not initialized` and `ℹ Run "cod
149:**Expected result:** `exit=0 stdout=[]` (the hook returns at once and prints nothing). `.codegraph/` holds `.gitignore` and `codegraph.db`. The log `/tmp/d0
183:**Expected result:** Claude loads the `sc:graph-protocol` skill and prints the 8-line report in this order: `codegraph 1.6.2 (pin 1.6.2: match)`; `index: no
268:**Expected result:** The contract has `input.tests: true`, `tests: [{path: tests/test_config.py, source: both}]` and `selection_source: advisory` (`codegrap
334:| `[LOCAL-WRITE]` In `/tmp/d03/hooked`, append a line to `pkg/cli.py`, then `pgrep -f 'codegraph\.js (init\|index)' \|\| codegraph status` with no Claude se
336:| `[CLAUDE-SESSION]` Delete `/tmp/d03/clone2/.codegraph`, then resume with `claude --continue` in `/tmp/d03/clone2` | No new index: the hook is registered f
coupled sites: plan Constraints line 26 (UNVERIFIED rule); steps 5, 7, 13, 15 and the Pending Changes edge row
after:
11:- codegraph 1.6.2 installed by `superclaude install` and `~/.local/bin` on your `PATH`, so a bare `codegraph` resolves. `/sc:graph init` may only call bare `
118:**Expected result:** `pgrep` prints nothing (no init is running), then `CodeGraph Status`, `Project: /tmp/d03/repo`, `⚠ Not initialized` and `ℹ Run "cod
149:**Expected result:** `exit=0 stdout=[]` (the hook returns at once and prints nothing). `.codegraph/` holds `.gitignore` and `codegraph.db`. The log `/tmp/d0
183:**Expected result:** Claude loads the `sc:graph-protocol` skill and prints the 8-line report in this order: `codegraph 1.6.2 (pin 1.6.2: match)`; `index: no
237:`impact.md` starts with YAML front matter, then these headings in order: `## Summary`, `## How to read this`, `## Readiness`, `## Input`, `## Definitions`, 
268:**Expected result:** The contract has `input.tests: true`, `tests: [{path: tests/test_config.py, source: both}]` and `selection_source: advisory` (`codegrap
334:| `[LOCAL-WRITE]` In `/tmp/d03/hooked`, append a line to `pkg/cli.py`, then `pgrep -f 'codegraph\.js (init\|index)' \|\| codegraph status` with no Claude se
336:| `[CLAUDE-SESSION]` Delete `/tmp/d03/clone2/.codegraph`, then resume with `claude --continue` in `/tmp/d03/clone2` | No new index: the hook is registered f
