---
topic: "MVP of the Orca read-only terminal observer (issue #409). Three candidate MVP directions, one per proposal: (A) Signal Bridge, (B) Attention Ledger, (C) Decision Desk. For each: what the first buildable slice is, which verified data sources it needs, what it must show as unknown, what it leaves out. The merged result must recommend ONE MVP direction (or a stated combination with the reason), the build order from MVP to later releases, the production stack decision (issue prefers Go with Bubble Tea v2 / Lip Gloss v2 / Bubbles v2, but this repository is Python: compare, including license and maintenance cost), the smallest read-only data adapter that can be trusted today, acceptance tests for the MVP drawn from the issue's acceptance criteria, and the open owner decisions."
domain: architecture
strategy: agile
depth: deep
proposals_target: 3
handoff_target: none
created: 2026-11-08T13:28:00Z
---

# Seed Brief: orca-observer-mvp

## Problem Statement

One human supervises 5-10 Orca orchestrators and 50-100 worker sessions/worktrees. Decisions that need the human, meaningful changes and supporting evidence are buried in noisy chats. Issue #409 asks for a read-only terminal observer that shows attention items with reasons, the affected scope, changes since the last look, and inspectable evidence, while keeping verified outcomes distinct from activity and disclosing unknown, stale and partial data. The offline design package (`.dev/design/orca-observer-20261106/`) holds twenty synthetic designs; this brainstorm must pick the MVP direction among three of them and define the first buildable slice.

Three candidate directions, one per proposal:

- **A. Signal Bridge**: one human-question panel on top, a source-freshness strip, and a fleet slice (session ledger). Built layout: `layouts/group_a.py` `signal_bridge`.
- **B. Attention Ledger**: an age-ranked list of open human questions with requester/owner and affected IDs, a "seen is not resolved" count, and a retained-context list. Built layout: `layouts/agent_focus.py` `attention`.
- **C. Decision Desk**: the selected request, the evidence ledger of only the affected sessions, and a bounded "other observed questions" panel with an explicit x/y count. Built layout: `layouts/group_a.py` `decision_desk`.

### Proposal assignment

Each proposal argues one direction as the MVP, and must still state honestly where the other two are stronger:

- Proposal by the `architect` persona: **A. Signal Bridge**.
- Proposal by the `analyzer` persona: **B. Attention Ledger**.
- Proposal by the `backend` persona: **C. Decision Desk**.

Every proposal must cover: first buildable slice; verified sources it needs (only those in Known Context); what it shows as unknown; what it leaves out; build order to later releases; stack recommendation with license and maintenance cost; smallest trustworthy read-only adapter; MVP acceptance tests mapped to the issue's acceptance criteria; open owner decisions.

## Known Context

Verified on 2026-11-08 against the installed Orca CLI (version 1.4.245-aidev02.780594c521aa) in this environment:

- `orca orchestration worker-list --json` returns `result.workers[]` with `dispatchId`, `taskId`, `runId`, `workerState`, `dispatchStatus`, `agentTerminalHandle`, `terminalState`, a `resource` block (`id`, `ownershipState`, `releaseState`, `worktreeId`, `ownerDispatchId`, `originDispatchId`, `recoveryAttemptCount`, `terminalHandle`) and a `projection` block (`stage.{worker,dispatch,activity,detail}`, `liveness.{verdict,source,observedAt}`, `evidence.{durable,liveStatus,lastObservedAt}`, `outcome`, `nextAction.kind`, `host.{id,kind}`, `workspace.{id,kind}`, `provider.id`, `role`). Paging: `result.page.{limit,total,hasMore,nextCursor}`, `result.scope.source`, `result.counts.{active,reclaimable,retained,released}`, `result.warnings[]` (e.g. "Showing 2 of 287 Dispatches, newest first"). Limit 1-100. Help: "Terminal state is process accounting and is reported separately from Task status." Note: the package's `integration-gaps.md` says "totalCount"; the live field is `page.total`.
- `orca orchestration check`: `--peek` returns unread messages without marking them read; `--all` returns every message for the handle without marking read; help states "--all and a Run --peek show at most 100 rows". Plain `check` consumes (delivery + `--ack`) and must never be used by an observer. Top-level JSON of an empty peek: `result.{count,dispatchId,runId}`; message row fields were not observed (no unread rows) and are UNVERIFIED.
- `orca orchestration inbox` takes `--limit`, `--terminal`, `--full`; its JSON shape is UNVERIFIED.
- Not established (from `integration-gaps.md`, still true): complete durable non-consuming message history beyond 100 rows; authoritative cross-host mission/owner/task/session/worktree joins; admission and revision-pinned verification feeds and human-owner linkage; cost/usage accounting coverage; durable event replay and ordering; native deep links.
- Design package: synthetic fixtures (`fixtures.py`), character-cell renderer and sanitizer (`canvas.py`), exports at 160/116/80 columns. The fixture schema is PROPOSED, not an Orca API. 19 package tests pass; no independent post-correction review PASS exists.
- Repository: Python, MIT license; dependencies include click and rich>=13 (no Textual, no Go toolchain installed). Rich-based TUIs already exist: `src/superclaude/cli/sprint/tui.py`, `sprint/monitor.py`, `prd/tui.py`, `cleanup_audit/tui.py`.
- Issue prefers Go with Bubble Tea v2 / Lip Gloss v2 / Bubbles v2 (TUIBBS-scp manifest pins 2.0.6 / 2.0.3 / 2.1.0; not claims about latest). Textual and Ratatui were compared. TUIBBS-scp is AGPL: no code may be copied from it.
- Discrepancy: the design PLAN describes Signal Bridge with a SIGNALS panel (running/settled/unknown/stale/policy-frozen counts and bars); the built 160-column layout includes it, but the 116- and 80-column layouts collapse it to one "RUN n SETTLED n UNKNOWN n STALE n" line plus a session ledger.

## Constraints

- Read-only. No approve, retry, terminate, spawn, merge, rebase, delete-worktree or worker instruction. No consuming message check (never plain `check` or `--ack`).
- Deterministic, bounded collection; no LLM polling loop.
- Lifecycle, report status, acceptance, tests and human approval stay separate fields; unknown is never zero or false; missing cost is not zero; a partial subtotal is not total spend; tokens are not progress; policy-frozen stays frozen.
- 160/116/80 columns, stable keyboard selection, NO_COLOR, ASCII/text export, full identifiers in detail, no blinking.
- Sanitize ANSI/OSC/control sequences from untrusted text; truncate by display-cell width; filtered and global counts explicit with denominators.
- Use only confirmed source contracts; label every other field UNVERIFIED or unavailable.
- No AGPL code from TUIBBS-scp. Production stack must be justifiable on license and maintenance cost.
- One-to-one session/worktree mapping is not assumed.

## Success Criteria

- One MVP direction (or an explicit combination with the reason) is recommended with its first buildable slice.
- Each proposal names the verified sources it needs, what it shows as unknown, and what it leaves out.
- A build order from MVP to later releases, gated on source contracts becoming verified.
- A stack decision comparing Go Charm v2 with Python Rich/Textual on license, toolchain, maintenance and fit with this repo.
- The smallest trustworthy read-only adapter, named by exact CLI verbs and fields above.
- MVP acceptance tests mapped to the issue's acceptance criteria, including the 8/80 base and 5/8/10 × 50/80/100 scenarios, duplicates, out-of-order events, stale sources and missing fields.
- A list of owner decisions that only the human can make.

## Open Questions

- Owner's choice of visual direction (the issue requires a human selection before production integration).
- Production stack: Go Charm v2 (issue preference, new toolchain) versus Python Rich (already in repo) or Textual (new dependency, MIT).
- How far to trust non-consuming message reads capped at 100 rows: is a question panel honest if it can only say "latest 100 rows seen"?
- Message row JSON fields from `check --all/--peek` and `inbox --json` are UNVERIFIED; which fields identify a human question, its requester and its owner?
- Signal Bridge intended design (signals panel) versus built narrow layouts: which is the candidate?
- Where the MVP lives: a `superclaude` CLI subcommand in this repo, or a separate binary/repo.
- Whether fixture replay (offline) ships before the live adapter.

## Enrichment Context

Quality tiers: codebase `fallback_1` (codegraph, Glob, Grep, Read; Auggie MCP not available); research-light `fallback_1` (WebFetch/WebSearch; `sc-research-protocol` not installed, Tavily and Context7 not available). Full artifacts: `enrichment/codebase-context.md`, `enrichment/research-light.md`.

### Codebase (what exists to reuse)

- House Rich TUI pattern: `src/superclaude/cli/sprint/tui.py` (`Live(refresh_per_second=2, screen=False)`, `_render() -> Panel`, once-only `_live_failed` guard), also `cleanup_audit/tui.py` and `prd/tui.py` (non-interactive fallback via `sys.stderr.isatty()`). None of these reads keyboard input, handles NO_COLOR explicitly, or truncates by display width (`sprint/tui.py:640` `_truncate` uses `len()`).
- Polling pattern: `sprint/monitor.py` `OutputMonitor` (daemon thread, `threading.Event` wait, 0.5 s default).
- Orca binary discovery: `cli/install_user_setup.py:198-221` `_find_orca()` (tries `orca-ide` then `orca`, validates via `skills list --json` to avoid the GNOME screen reader also named `orca`, 10 s timeout). No code in the repo calls `orca orchestration` or parses its JSON.
- Sanitizer base: `cli/eval/pty_stream.py:94-101` `ANSI_ESCAPE_RE` lacks 8-bit C1, bare control characters, Unicode Cf and unterminated OSC; prototype `canvas.py:10-17` `sanitize` is stricter. No `cell_len`/`wcwidth` use in `src/`; `rich.cells.cell_len` is available through the existing Rich dependency.
- CLI registration: deferred import + `main.add_command(...)` in `cli/main.py:519-561`; groups defined per package (e.g. `cli/sprint/commands.py`).
- Prototype fixtures (`fixtures.py` variants base, uneven, shared-unmapped, historical, long-identifiers, source-loss, missing-fields, duplicate-out-of-order, empty, injection) can seed tests; prototype `requirements.txt` (Pillow, wcwidth) is not a project dependency.
- No Go or Rust code; Textual not a dependency.

### Stack research (2026-11-08, primary sources, nothing run)

| Stack | License | Toolchain cost | Fit for this MVP | Maintenance |
|---|---|---|---|---|
| Bubble Tea v2.1.1 / Lip Gloss v2.0.6 / Bubbles v2.2.1 (Go) | MIT | New Go toolchain + per-platform binary release pipeline | Strong list/focus widgets; NO_COLOR parsed as boolean (`NO_COLOR=yes` ignored, contrary to no-color.org); teatest/v2 untagged under `x/exp`; no built-in plain-text export; wide-char width UNVERIFIED | Low risk, monthly releases |
| Textual 8.2.8 (Python) | MIT | One new pure-Python dependency | Built-in focus/keys, headless `run_test(size=...)`, SVG snapshot plugin; plain-text export UNVERIFIED | Medium: company wound down May 2025, community-maintained, last release June 2026 |
| Rich 15.0.0 (already installed) | MIT | None | Best plain-text/SVG export (`record=True`, `export_text()`), width-fixed test consoles, `rich.cells` width; NO keyboard input (hand-written raw key reading needed) | Medium, same maintainer, very widely used |
| Ratatui 0.30.2 (Rust) | MIT | Rust toolchain + maturin or binary | Strong list, plain-text snapshots | Low-medium, pre-1.0 |
| TUIBBS-scp | AGPL | n/a | No code may be copied | n/a |
