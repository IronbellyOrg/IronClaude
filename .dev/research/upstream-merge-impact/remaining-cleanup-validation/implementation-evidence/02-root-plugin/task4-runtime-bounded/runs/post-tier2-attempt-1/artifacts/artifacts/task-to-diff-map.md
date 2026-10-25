# Wave 1B — UC-2 task/spec-to-work map (orchestrator, inline)

Audit root: fixtures/project (paths below are repo-relative).

## Diff hunks (changes.patch)

| Hunk | Ref | Content |
|------|-----|---------|
| H1 | changes.patch:5-9 → src/greeting.py:1-4 | new file `greet(name)`: `if not name: raise ValueError("name required")`; `return f"Hello, {name}!"` |

Total hunks: 1. The patch contains NO hunk for tests/test_greeting.py.

## Task → spec → work mapping

| Task | Spec req | Claimed (completed.md) | Work evidence | Diff-backed? | Map status |
|------|----------|------------------------|---------------|--------------|------------|
| T-101 | R-001 (spec.md:5-6) | completed.md:6 | src/greeting.py:4 `return f"Hello, {name}!"` → "Hello, Ada!" for "Ada" | yes (H1, changes.patch:9) | mapped |
| T-102 | R-002 (spec.md:8-9) | completed.md:7 | src/greeting.py:2-3 `if not name: raise ValueError(...)` | yes (H1, changes.patch:7-8) | mapped |
| T-103 | R-003 (spec.md:11-12) | completed.md:8 | tests/test_greeting.py:4-5 (ordinary), :8-13 (empty) — file exists on disk, untracked | **no** — not in changes.patch, outside --scope src | mapped to on-disk evidence only; not executed |

## Structural signals

- S_scope = 1 (touched files in diff)
- S_domains = 1 (code) — tests/ is not in the diff
- S_dev_density = 0 unmapped hunks / 1 total = 0.00
- tasklist_completion_pct (claimed) = 3/3; independently grounded by Read = 3/3 for presence; R-003 "exercise" (execution) unverified
- Frontmatter: completed.md:2 `status: done`

## Verification triangle (§6.1 step 5.5)

Not run: Serena `execute_shell_command` not exposed (verification_skip_reason: tool-unavailable).
Regression detection degrades to the task-log claim; no task log was supplied (`--task-log` absent),
so no test-state claim exists → Grounding Gap required.

## Other Wave-1A chain steps

- Serena symbolic chain (2, 2a, 3, 3b, 4, 4.5, 5, 7, 7'): skipped — Serena unavailable; native Read/Grep used (degraded: serena).
- 4b'/4b runtime-surface: `greet` is a plain undecorated function (src/greeting.py:1) — not on the refs/runtime-surface.md §1 Python allowlist → runtime_surface_requirements: [], runtime_surface_sweep_ran: false.
- 5.6 / 5.6a reachability: spec has no side-effect / durable-sink requirement and no in-scope enabled-by-config capability → reachability_skip_reason: no-side-effect-requirements.
- 1B.3 cross-task interaction scan: tasklist has 3 tasks, but symbol derivation requires Serena find_symbol; native fallback: T-101 and T-102 both touch symbol `greet` (src/greeting.py:1); T-103 references it (tests/test_greeting.py:1). T-101/T-102 jointly implement one 4-line function; no un-cited conflicting edit observed. 1 LOW interaction entry (1 call-site group).
