---
source: codebase
quality_tier: fallback_1
reason: auggie codebase-retrieval tool not available in this session; codegraph (fresh, 2321 files) plus Read, Grep, Glob used
created: 2026-11-07
---

# Codebase context: orchestrator mode (#339)

## 1. Coordinator/worker contract (what already exists)

Source: `src/superclaude/core/WORKER-CONTRACT.md` (installed to `~/.claude/WORKER-CONTRACT.md`).

- Section 1 "Terms" (line 9): person-mode flags are refused under `--unattended` (line 14); brief guard with case 3 = never-as-worker list (lines 16-20).
- Section 2 "Command-side rules" (line 26): WC-4 `return-contract.yaml` with `worker_status`; WC-9 no outward action by a worker; WC-10 (line 45): a missing heartbeat is absence, never death; the coordinator acts only on Orca's stall proofs.
- Section 3 "Worker-session duties" (line 48).
- Section 4 "Coordinator rules" (line 64): WC-6 every retry is a new Task (line 68); what the coordinator owes each worker (line 77); brief layout (line 91); feature and child worktrees (line 101, with a cleanup refusal list: unmerged commits, open PR, uncommitted changes, unfinished `/sc:implement` ledger, unread report); git and GitHub ownership (line 110); reading a result (line 120); after an `/sc:implement` stop (line 131); fan-in (line 154); worked example (line 158).
- Section 5 brief template (line 166).
- Gap: no shipped rule tells the coordinator to keep polling until every Task settles or to re-arm the wait after an expiry. That rule lives only in a private memory file (analysis F3). Orca's own guide has the keep-waiting duty (`orca-capabilities.md:113`).
- Tests: `tests/skills/test_worker_contract.py` (41 static tests pinning contract text).
- Routing: `src/superclaude/core/HOW-WE-WORK.md` "Orca coordination" (lines 396-405), copied byte-for-byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`.

## 2. Orca state the sweep can read

Source: `.dev/orca-command-refactor/inventory/orca-capabilities.md` (verified against the installed Orca guides and CLI help).

- Liveness has three verdicts: `live`, `unverifiable`, `exited` (lines 37, 122). `worker-list`'s `projection.liveness` is the fleet verdict and wins over `worker-show`, which reports terminal liveness only (line 123).
- `unverifiable` reasons `missing_status`, `stale_status`, `restored_unconfirmed`, `host_unavailable` are all absence; absence never authorizes stop, retry or release (line 125).
- Stall proof is one of: `exited`, the worker's own process-exit observation, or a final transcript turn without `worker_done` (line 126).
- Each row carries `projection.attention.requiresAction` and a literal `projection.nextAction` argv (line 127).
- Paging: at most 100 rows per page, continued with `page.nextCursor` (line 127). Remote workers need `--include-remote` (line 128).
- Terminal states (process accounting, separate from Task status) and the rule that the coordinator turn cannot end while `worker-list --terminal-state reclaimable` returns rows (line 113).
- Orca not running: `runtime_unavailable` (lines 39, 147).
- Heartbeats prove liveness, not progress (line 130).

## 3. Existing read-only sweep: sc-crash-recovery

Source: `src/superclaude/skills/sc-crash-recovery/` (`SKILL.md`, `refs/investigators.md`, `refs/pipelines.md`, `refs/report-template.md`, `scripts/bootstrap_scan.sh`, `scripts/parse_session_log.py`).

- Read-only, enforced by `allowed-tools` (`SKILL.md:4`): Read, Glob, Grep, a fixed list of read-only Bash forms, its own scripts and Task. No Edit, no Write (`SKILL.md:13`).
- Default `--since` is 72 hours. Five investigators. Every suggested command is marked SAFE or REVIEW; gaps go into a "What I could not determine" section. It proposes commands and never runs them.
- Reuse value: session-log parsing, the SAFE/REVIEW labelling and the "could not determine" honesty section. It does not read Orca state and does not write a report file.

## 4. Sessions outside Orca: ccsession

Source: `src/superclaude/skills/ccsession-tag/ccsession` (bash).

- `ccsession --list` lists labeled sessions (usage at line 26, handler at line 1787).
- Sessions started this way are ordinary Claude Code sessions: no Orca preamble, so they cannot send lifecycle messages (analysis F2). In phase 1 they can only be listed, never messaged.

## 5. Report layout source: #409 observer design package

Source: unmerged branch `docs/409-orca-dashboard-designs`, commit `495eb96d`, folder `.dev/design/orca-observer-20261106/`. Not on this branch; read with `git show 495eb96d:<path>`.

- Offline terminal-design prototypes (Python/Pillow renderer, widths 160, 116 and 80 columns), 20 designs in two sets. Set 2 (`agent-focus/`) includes **Attention Ledger** (open human questions with age, requester, acting owner and affected session IDs; "seen is not resolved"; "retain context") and **Shift Brief**, the closest matches to the #339 periodic report.
- Header convention: scope counts (`N owners / N sessions / N mapped trees`), then clock and per-source freshness (`08:00 UTC | msgs partial | workers 4s | checks 14m`), and a `SYNTHETIC . READ ONLY` marker.
- Data dictionary keeps state dimensions independent: lifecycle, phase, health, approval, freshness, result, admission, evidence, policy, tests/review. Entities: Orchestrator, Session, Worktree, Request, Dependency, Event, Source.
- Required semantics: dirty is not dangerous; stale is not failed; overlap is not conflict; a worker result is not admission; unknown stays unknown and null cost is never zero; no approve, dispatch, retry or merge actions shown, even greyed; narrow views keep the first human decision, owner and scope/freshness; show omission counts when output is limited.
- The fixture schema is proposed, not an Orca API schema. A static Markdown report can follow the Attention Ledger order and the header/freshness/omission rules without the renderer.

## 6. Where new code would live

- CLI: Click groups under `src/superclaude/cli/<name>/`, registered in `src/superclaude/cli/main.py` with deferred imports (`main.add_command(<group>, name=...)`, lines 519-561, `# noqa: E402,I001`). Examples: `recommend/`, `reflect/`, `swarm/`.
- Commands: `src/superclaude/commands/<name>.md` (no `sweep.md` or `close.md` today). Skills: `src/superclaude/skills/<name>/SKILL.md`. Primitives reference installed paths, never `src/superclaude/...`.
- Tests: `tests/` with pytest; Orca and git calls mocked.
- Sync: `make sync-dev`, `make verify-sync`; `.claude/` mirrors never staged.

## 7. Conflicts and gaps (from analysis F1-F12)

Source: `.dev/issues/339/analysis/analyze-worker-contract.md`.

- F1: extend the coordinator contract, do not build a parallel protocol.
- F2: sessions started outside Orca cannot send lifecycle messages.
- F3: "keep polling" is not a shipped rule.
- F4: `/sc:close` overlaps the contract's cleanup refusal list and must never treat `.dev/tasks/` as disposable.
- F5: `/sc:sweep` overlaps `worker-list` and crash-recovery; window 6h (issue) vs 72h (crash-recovery); a resume must be a new Task (WC-6).
- F6: "new worktree first" conflicts with the child-worktree trigger rule (CR-01).
- F7: the report overlaps #409.
- F8, F9: bypass permission mode versus default; typed messages exist for Orca only.
- F10-F12: no signed-grant code; "management server" undefined; the sweep has two names in the issue.
