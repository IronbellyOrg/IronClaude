# Phase 1 — Load-Bearing Anchor Map (re-grepped 2026-06-12)

All anchors below were re-grepped against current source at task start. None are
missing; line numbers WILL drift as Phase 2-6 edits land — re-grep each at edit time.

| Anchor Description | Current File:Line | Grep Match Text |
|---|---|---|
| Optimistic INV-001 increment (to be RELOCATED) | `src/superclaude/pr_submit/fsm.py:793` | `result.round_counter += 1` |
| Optimistic increment comment (to be REMOVED) | `src/superclaude/pr_submit/fsm.py:792` | `# Re-review attributed to our push: tick the monotonic round counter (INV-001).` |
| EventType count docstring (33→37) — models | `src/superclaude/pr_submit/models.py:20` | `"""Closed enum of run-log event types — EXACTLY 33 members.` |
| EventType count prose (33→37) — run_log append docstring | `src/superclaude/pr_submit/run_log.py:103` | `... is not one of the 33 closed` |
| EventType count prose (33→37) — run_log ValueError | `src/superclaude/pr_submit/run_log.py:109` | `f"unknown event_type: {event_type!r} (not one of the 33 §11.3 events)"` |
| IDEMPOTENCY_SETS tuple decl (5→6) | `src/superclaude/pr_submit/run_log.py:27` | `IDEMPOTENCY_SETS = (` |
| IDEMPOTENCY_SETS state seed (generic consumer) | `src/superclaude/pr_submit/run_log.py:159` | `**{s: [] for s in IDEMPOTENCY_SETS},` |
| IDEMPOTENCY_SETS working-set ctor (generic consumer) | `src/superclaude/pr_submit/run_log.py:161` | `sets = {s: set() for s in IDEMPOTENCY_SETS}` |
| IDEMPOTENCY_SETS serialization (generic consumer) | `src/superclaude/pr_submit/run_log.py:188` | `for s in IDEMPOTENCY_SETS:` |
| IDEMPOTENCY_SETS validation (generic consumer) | `src/superclaude/pr_submit/run_log.py:207` | `if set_name not in IDEMPOTENCY_SETS:` |
| EventType class decl | `src/superclaude/pr_submit/models.py:19` | `class EventType(str, Enum):` |
| MonitorState class decl | `src/superclaude/pr_submit/models.py:83` | `class MonitorState(str, Enum):` |
| TERMINAL_STATES frozenset | `src/superclaude/pr_submit/models.py:117` | `TERMINAL_STATES = frozenset(` |
| SkillResult dataclass decl | `src/superclaude/pr_submit/models.py:166` | `class SkillResult:` |
| transition() RESOLVING/"resolved" edge (to retarget RHS) | `src/superclaude/pr_submit/fsm.py:611` | `if edge == (MonitorState.RESOLVING, "resolved"):` |
| transition() INV-001 edge (PRESERVE byte-identical) | `src/superclaude/pr_submit/fsm.py:613` | `if edge == (MonitorState.S5_AWAITING_REREVIEW, "rereview_attributed"):` |
| transition() S5/"timeout" sibling edge | `src/superclaude/pr_submit/fsm.py:615` | `if edge == (MonitorState.S5_AWAITING_REREVIEW, "timeout"):` |
| transition() full `if edge ==` chain | `src/superclaude/pr_submit/fsm.py:579-615` | 15 flat `if edge == (state, event):` guards (NOT a dict) |

## Notes / Flags

- **No missing anchors.** Every expected anchor from Step 1.4 matched.
- The optimistic increment is confirmed present at `fsm.py:793` (the ONLY
  `round_counter += 1` in the file) — Step 5.4 will relocate it.
- The INV-001 edge is at `fsm.py:613` — preserve byte-for-byte (Step 5.3 adds the
  `"declined"` sibling alongside, never replacing it).
- run_log.py has 2 "33"-count prose sites (`:103`, `:109`); models.py has 1 (`:20`)
  plus a module-docstring "33" to be confirmed during Step 2.2.
- IDEMPOTENCY_SETS has 4 generic consumers (`:159`, `:161`, `:188`, `:207`) that
  auto-wire the 6th set — do NOT duplicate them (Step 4.1).
