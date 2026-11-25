# Wave 1.5 Branch B (architectural-doc lookup), persisted by the parent

## Preliminary result as received (all verdicts unknown, markers: none found)

Worker returned two documents (summaries condensed by the parent; originals in the worker transcript):

1. /home/coder/workspaces/IronClaude/src/superclaude/skills/ccsession-tag/README.md
   Summary: contract for `--list`, `--here`, `--here --all`, the worktree-following list and the `--ask` question; names are per repo (one list per `origin`). "Time limit" section (README lines 301-311 per worker, unverified) says the question gives up after 30 seconds, Orca fails a supervised worker whose Claude is not ready within 60 seconds, `CCSESSION_ASK_TIMEOUT` changes the limit (0 waits for ever) and the limit lives inside `ccsession --ask`. States no performance expectation, CPU figure or launch-time target for a large list.
   Markers: none found.
2. /home/coder/workspaces/IronClaude/docs/testing/v5.0.0/user/D08-ccsession.md
   Summary: manual test script recording expected behaviour of `--here`, `--here --all`, `--list`, `--ask` (timeout 30 s default; exit 1 on timeout, 130 on Ctrl+C, 3 for text that cannot be a name). Sets no performance or CPU expectation. Its source line citations are tied to an older script revision.
   Markers: none found.

Other ccsession mentions (docs/developer-guide/technical-architecture.md, docs/user-guide/session-management.md, commands.md, CLAUDE.md, SKILL.md, PLANNING.md, KNOWLEDGE.md) hold nothing on the list, `--ask` or the limits (worker grep). Not opened by the worker: docs/reference/model-aliases.md, docs/testing/v5.0.0/sysop/E01-ccsession-tier-policy.md, E02-ccsession-model-data-publishing.md, MODEL-TIERS.md, hooks files (tier policy and model data topics).

## Finalized verdicts (parent, Section 2 procedure)

Collected metadata (2026-11-17, parent): file mtimes of all three files are the checkout time 2026-11-05T20:38:12Z (identical, so mtime cannot separate doc from code); last commit date in this checkout for README.md, D08-ccsession.md and ccsession is 2026-11-05T15:15:37-05:00 for all three; origin/master's newest commit touching ccsession or README is 2026-11-16T12:13:11-06:00.

| Doc | Step 1 | Step 2 | Verdict |
|---|---|---|---|
| src/superclaude/skills/ccsession-tag/README.md | doc not 90+ days behind the code (same commit date; master code is 11 days newer) | no markers | `current` |
| docs/testing/v5.0.0/user/D08-ccsession.md | same | no markers | `current` for the behaviour contract |

CAUTION (parent): the checkout's ccsession is older than origin/master by commit 8c21ac41f and its predecessors (installed copy has 2072 lines vs 1902); D08's source line citations do not match the 2072-line script, so only its behaviour statements, not its line numbers, are usable.
