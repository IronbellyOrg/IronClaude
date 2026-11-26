# /sc:analyze report: src/superclaude/cli/observe/ (focus architecture, depth quick)

Codegraph: index_state=fresh, checked_at=2026-11-24T20:50:02Z; degraded: none

Scope: structure only, checked against checkout a7ae3dd30 (branch ironbelly/Issuecleanup). Quick depth: no deep call tracing.

## Findings

1. **Info.** The package has 14 modules: adapter, collector, commands, export, keys, parse, questions, render, sanitize, snapshot.schema.json, terminal, theme, view. `adapter.py` is the only edge to the Orca CLI (module docstring line 1: "The one read-only edge to the Orca CLI").
2. **Info (boundary that matters for #781).** `adapter.py:32-48` defines a forbidden-verb set that includes `send`, `ask`, `reply`, `dispatch`, `run-use`. The observer therefore cannot carry a person's message. A relay must live outside this package. This agrees with the issue's step 2.
3. **Info.** `export.py:101-102,158-159` keeps question text out of stored output (ids, times, counts only). A stored feed built from export.py cannot answer content questions about a pending question. This is the "feed coverage" unknown in the issue.
4. **Info.** `docs/user-guide/observer.md:154,156` state local-host-only counts and that the observer never messages. Matches the issue's quotes.
5. **Info.** No file under src, docs or tests mentions "contact agent". Nothing of #781 is built.

## Recommendation

Keep the observer unchanged. Specify any contact agent and relay as a new component outside `src/superclaude/cli/observe/`.
