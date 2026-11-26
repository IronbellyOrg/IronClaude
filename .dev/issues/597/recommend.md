# /sc:recommend output for #597

- Recorded: 2026-11-23T22:27:00Z
- Goal sent: Pick the next-step chain for GitHub issue https://github.com/IronbellyOrg/IronClaude/issues/597. Type: bug. Complexity: simple. Summary: .dev/issues/597/issue-summary.md. Default row "Bug, simple"; stage debug, --pipeline none.

The block below is the skill's output, copied verbatim.

````text
Goal: Diagnose issue 597 (research questions skip the Context7 and Tavily tools and get delegated to agents that lack them), at stage debug, with no fix applied.

Level: not on the six-level scale (a supporting task) - guide section 3.4, row `bug`

Changes files: step 1 writes a report folder under .dev/troubleshoot/. It changes no source file.

Run these in order:

1. /sc:troubleshoot "Research questions skip the Context7 and Tavily MCP tools: the orchestrator delegates to an agent without them (claude-code-guide) instead of doing the lookup itself; expected Context7 for docs, Tavily for web, or a delegate that has those tools" --type bug --depth quick --context .dev/issues/597/issue-summary.md --scope src/superclaude/core
2. Read .dev/troubleshoot/<name>-<timestamp>/REPORT.md (the path step 1 prints) and keep its status and blockers.
3b. Only if the report confirms a supported fix: /sc:workflow "<the supported fix from REPORT.md, with a reproducing test>", read the printed plan, then /sc:implement <printed plan path>.

Notes:
- No --fix: the claim is --pipeline none, and --depth quick with --fix is refused by the command.
- Diagnosis alone stops after step 2. Do not fix an unconfirmed, failed or blocked result.
- Default row not used for step 2: the guide's bug row plans with /sc:workflow before /sc:implement.

Sources verified:
- src/superclaude/core/HOW-WE-WORK.md (routing table, row `bug`)
- src/superclaude/commands/troubleshoot.md, workflow.md, implement.md (Read; same as the installed copies)
- auggie semantic rank: skipped (matched row)
````
