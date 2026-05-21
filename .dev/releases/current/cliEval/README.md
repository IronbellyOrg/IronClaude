# cliEval — Real-World Eval Suite for IronClaude

**Release ID:** `cliEval`
**Design phase:** drafted 2026-05-18 (this directory)
**Status:** 🟡 DESIGN — pending review
**Target subcommand:** `superclaude eval --suite real`

---

## TL;DR

A new `superclaude eval` subcommand that runs **15 real-world evals** (not mocks, not synthetic) against IronClaude's hook system, installer, and verify-sync detector. Each eval drives a real Claude Code TTY subprocess in an isolated `HOME` directory and asserts on filesystem + JSONL telemetry side-effects.

**Architecture in one sentence:** Fork `ptytest` for the PTY driver, vendor it, extend `cli/sprint`'s existing `IsolationLayers` with a `HOME` override, mirror `cli/prd`'s sub-package layout for the new `cli/eval/` subcommand, borrow `mcp-eval`'s `Expect.tools.*` DSL idea (port only, no dependency), and store run artifacts under `.dev/eval-runs/<ISO>/<run-id>/`.

**Effort estimate:** ~1,190 LOC for the harness scaffolding (2-3 engineering days) + ~150-300 LOC per eval × 15 = ~3,000-4,500 LOC for the eval suite itself. **Total: 4,200-5,700 LOC over ~2 weeks of work.**

---

## Documents in this release

| File | Purpose |
|---|---|
| [`README.md`](./README.md) | This file. Index + TL;DR. |
| [`design-spec.md`](./design-spec.md) | Full architectural design: components, lifecycle, schemas, file-layout. |
| [`decisions.md`](./decisions.md) | Explicit resolution of the 4 open architectural questions raised in the /sc:design intake. |

---

## Inputs to this design

| Source | Path |
|---|---|
| Requirements spec (15 evals + NFRs) | This session's prior `/sc:brainstorm` output |
| Fork-candidate research | [`.dev/eval-runs/research/2026-05-18-fork-candidate-research.md`](../../../eval-runs/research/2026-05-18-fork-candidate-research.md) |
| CLI extensibility analysis | [`.dev/eval-runs/research/2026-05-18-cli-extensibility-analysis.md`](../../../eval-runs/research/2026-05-18-cli-extensibility-analysis.md) |
| Maintainer directives 2026-05-18 | Local-only deployment; output → `.dev/eval-runs/`; subcommand `superclaude eval --suite real`; 5-session baseline for E14 |

---

## Out of scope for this design

- **Eval bodies (E1-E15 implementations).** This design specifies the harness; the eval bodies are a separate workstream.
- **CI integration.** Per the maintainer directive ("locally for now"), CI plumbing is deferred to a future release.
- **MCP-server provisioning.** Evals that need live MCP servers gate on binary presence; setup of the servers themselves is out of scope.
- **Production deployment (e.g., to a SuperClaude_Plugin release).** This is a development-time tool; no end-user surface change beyond the new subcommand.

---

## Next step after design approval

`/sc:workflow` against `design-spec.md` to generate the implementation plan, then `/sc:tasklist` for sprint-runnable bundle, then `superclaude sprint run …` for execution. Alternative: hand-implement against the design spec.
