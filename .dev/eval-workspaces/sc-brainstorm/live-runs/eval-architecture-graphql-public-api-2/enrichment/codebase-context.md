# Codebase Context: explore GraphQL for public API

**Quality tier**: primary (Auggie MCP)
**Scope**: full repo (`/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2`)
**Date**: 2026-05-25

## Material finding — the host project has no public API surface today

The SuperClaude repo is a **Python CLI + pytest plugin**, distributed via `pipx install superclaude`. There is no HTTP server, no REST endpoints, no GraphQL schema, and no socket-listening process maintained in `src/`. The only `GraphQL` references in the repo are inside a test fixture YAML (`src/superclaude/cli/eval/suites/adversarial_merge_consistency.yaml`) that uses GraphQL as an example data-model — they are not implementation references.

**Implication for the brainstorm**: "Explore GraphQL for public API" is a **greenfield exercise for this codebase**. The merged requirements should not assume an existing REST API to coexist with or replace within this repo. If the brainstorm is being run *against* this codebase, the framing is "what would it take for SuperClaude itself to expose a public GraphQL API" — which is a substantial scope expansion. If the brainstorm is being run **in this codebase but about a hypothetical/other-project public API**, that should be made explicit in the seed brief, and the requirements should remain stack-agnostic.

## Relevant existing surfaces

| File | What it is | Relevance |
|------|-----------|-----------|
| `src/superclaude/cli/main.py:20` | Click-based CLI entry point | Closest thing to a "public interface" — but it's a local CLI, not network-exposed |
| `src/superclaude/cli/main.py:400-426` | Subcommand registration (sprint, roadmap, cleanup-audit, tasklist, cli-portify, prd, eval) | Pattern for adding new command groups — a future `superclaude api` group would slot here |
| `src/superclaude/cli/install_mcp.py:516-635` | MCP server install logic (HTTP/SSE to localhost:9400) | Only network code in the project — outbound client calls to MCP, no server |
| `pyproject.toml` | Build system (hatchling, `superclaude` entry point, pytest plugin) | Would need new server dep (fastapi/strawberry/ariadne) if exposing GraphQL |
| `src/superclaude/cli/eval/suites/adversarial_merge_consistency.yaml:199` | Test fixture mentioning REST/GraphQL | Test artifact only — no live code |

## Architectural patterns in use

- **Click command groups** with `.add_command()` registration in `src/superclaude/cli/main.py`. New surfaces follow this pattern (see `prd_group`, `eval_group`, `tasklist_group`).
- **No persistent server / no state machine** — every CLI invocation is short-lived. Adding a public API would introduce a long-running process model that does not exist today.
- **Python ≥3.10**, hatchling build, UV-managed deps. Any new server stack must be compatible.
- **MCP servers are external** — SuperClaude consumes MCP via airis-mcp-gateway at `http://localhost:9400/sse`, but does not host one.

## Constraints introduced by current code

- **No existing HTTP framework dependency** — adding GraphQL means picking and adding a server framework (FastAPI + Strawberry, or Ariadne, or pure ASGI), which is a significant net-new dependency surface.
- **Distribution model is `pipx install`** — a CLI-installable package is not a natural host for a long-running public API. If the brainstorm targets SuperClaude itself, expect a deployment-model decision (separate `superclaude-server` package? container image? cloud-hosted service?).
- **No authentication code in the repo** — any public API requires auth infrastructure built from scratch (or via gateway/proxy).
- **No persistence layer** — the repo has no DB, no migrations, no ORM. A public API that does anything non-trivial will need a state-bearing backend chosen and bolted on.

## Open architecture questions surfaced from codebase scan

- **Target project clarification**: is this brainstorm about adding a public API to SuperClaude itself, or about a separate product? The codebase only constrains the answer if the former.
- **If for SuperClaude itself**: which capability is being exposed publicly? CLI introspection? Task/skill execution as a service? Eval results? A registry of skills? The "what is the API for" question is open.
- **Stack-agnostic vs. opinionated**: the brainstorm output should declare whether it commits to a specific server stack (Python-aligned: Strawberry / Ariadne / Graphene), or remains a portable requirements doc.
