---
source: codebase
quality_tier: fallback_1
reason: reused, not re-gathered. The earlier enrichment (codegraph plus Read, Grep, Glob; auggie unavailable) is still current for Phase 1, and the deep research report re-verified the same anchors on 2026-11-07 and 2026-11-08.
reused_from: .dev/brainstorms/20261107-073115-orchestrator-mode/enrichment/codebase-context.md
created: 2026-11-08
---

# Codebase context: orchestrator mode Phase 1 (#339)

## 1. Reused context (read the source file for detail)

`.dev/brainstorms/20261107-073115-orchestrator-mode/enrichment/codebase-context.md`, sections:

1. Worker contract: `src/superclaude/core/WORKER-CONTRACT.md` (WC-9 no outward action, WC-10 a missing heartbeat is absence, WC-6 a retry is a new Task, cleanup refusal list); no shipped keep-polling rule; 41 static tests in `tests/skills/test_worker_contract.py`; routing in `HOW-WE-WORK.md` "Orca coordination" plus its plugin byte copy.
2. Orca read state: liveness `live` / `unverifiable` / `exited`; `projection.attention.requiresAction`, `projection.nextAction`; 100 rows per page with `page.nextCursor`; `--include-remote`; `runtime_unavailable` when Orca is down.
3. `sc-crash-recovery`: read-only by `allowed-tools`, 72 h default, SAFE/REVIEW labels, "could not determine" section; reads no Orca state and writes no file.
4. ccsession: `ccsession --list`; such sessions cannot send Orca lifecycle messages, so Phase 1 only lists them.
5. #409 layout at `495eb96d` (`.dev/design/orca-observer-20261106/`): header with scope counts and per-source freshness, Attention Ledger, Shift Brief, "unknown stays unknown", omission counts, no action buttons.
6. New code: Click group under `src/superclaude/cli/<name>/`, registered in `cli/main.py` with deferred imports; command `src/superclaude/commands/<name>.md`; skill `src/superclaude/skills/<name>/SKILL.md`; installed paths only.
7. Conflicts F1-F12 from `.dev/issues/339/analysis/analyze-worker-contract.md`.

## 2. What the research added since (pointers only)

- Phase 1 file-by-file plan: REPORT Section 8, Phase 1 (line 1216), steps 1.0a to 1.26.
- Option A1 choice and rejected A4: `TASK/synthesis/phase7-summary.md`.
- Carried design fixes GQ-101 to GQ-110 and stale citations GQ-111 to GQ-113: GAPS lines 124-136; row count at GAPS line 138.
- Safety anchor for GQ-103(1): WC-9 `index.lock` text at `src/superclaude/core/WORKER-CONTRACT.md:44`.

TASK = `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/`; REPORT and GAPS are in it.
