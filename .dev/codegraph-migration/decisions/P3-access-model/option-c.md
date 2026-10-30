# Option C: hybrid (MCP for interactive lookups, CLI only for CLI-only jobs)

Read `context.md` in this folder first.

## Proposal

- Phase 2 lists the seven small tools plus explore: `CODEGRAPH_MCP_TOOLS=explore,node,search,callers,callees,impact,files,status` (one line in its JSON). If that is not done, primitives fall back to Grep/Read, exactly like "codegraph absent".
- Main sessions and unrestricted orchestrators use MCP for symbol, caller and impact lookups (fast, structured, keeps the watcher alive).
- Read-only agents that already carried Serena symbol tools get the matching codegraph MCP names (they did the same job with Serena); the orchestrator still passes precomputed artifacts where a brief already works that way (troubleshoot producers, reflect hunks), so agents rarely need to call.
- CLI only for what MCP cannot do: `codegraph affected` (test selection), `codegraph status` in scripts and the new commands' file outputs, and `codegraph init` in one user-typed command. Allowlists name exact read subcommands only; a grep test forbids mutating verbs in every primitive.
- One readiness check per run (`codegraph_status`, or `codegraph status` where MCP is not available) labels answers; stale or foreign-index answers are leads only.

## Strengths

- Keeps the small 1:1 replacement for existing primitives (MCP names where Serena names were).
- Freshness: an MCP session keeps the daemon and watcher running, which removes most of INV-001 for interactive sessions; CLI-only jobs carry the readiness label.
- Agents keep follow-up ability without needing Bash.
- CLI used only where it is the only path, so allowlist risk is limited to 2-3 subcommands.

## Weaknesses

- Two access paths to document (one shared guide covers both).
- Still depends on the one-line Phase 2 env change for full value; schema overhead of 8 listed tools unmeasured.
- Foreground agent MCP availability UNVERIFIED (one live smoke test needed).
