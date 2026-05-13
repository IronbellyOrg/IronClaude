# D-0009 — Subagent counter hooks evidence

## Task: T02.06 (STRICT, async:true)

`SubagentStart` / `SubagentStop` counter pair per design §3.6. Feeds the `bg=N`
flag in UserPromptSubmit envelopes.

## Files

- `src/superclaude/hooks/scripts/freshness-subagent-start.sh` (increment)
- `src/superclaude/hooks/scripts/freshness-subagent-stop.sh` (decrement, floored at 0)

Both mode 0755, `bash -n` clean. Mirrored to plugins.

## Linear behaviour

| Sequence | Expected | Got |
|---|---:|---:|
| 3 starts + 2 stops | 1 | 1 ✓ |
| 3 more stops (from 1) | 0 (floored) | 0 ✓ |

## Concurrency tests

**Per-phase parallelism (realistic ordering):**

| Workload | Phase mode | Expected | Got |
|---|---|---:|---:|
| 30 starts sequential, then 20 stops sequential | serial | 10 | 10 ✓ |
| 30 starts parallel (-P 10), then 20 stops parallel (-P 10) | phases sequential, each parallel | 10 | 10 ✓ |
| Pure 30 starts parallel | -P 10 | 30 | 30 ✓ |
| Pure 10 starts parallel | -P 10 | 10 | 10 ✓ |

**Adversarial interleaving (starts AND stops running simultaneously):**

Running 30 starts and 20 stops in two parallel `xargs` pipelines under `&` `wait`
produced a counter value of 15 (rather than 10). This is **expected and correct**:
when stops fire before any start has had a chance to increment, they observe the
counter at 0 and stay there (floor-at-0 guarantee). The 5 "lost stops" reflect
this floor protection working as designed.

**In real Claude Code, every `SubagentStop` event is paired with a preceding
`SubagentStart` for the same subagent**, so this adversarial ordering does not
occur in practice. The realistic concurrency target (per-phase parallelism) is
met exactly.

## Lock-acquisition fix

Initial implementation used `flock -w 1 9 || true`. Under contention, this fell
through to the unlocked critical section when the 1-second timeout fired.

Replaced with `flock 9 2>/dev/null || exit 0`:
- No timeout (blocks until acquired; critical section is microseconds, no
  deadlock risk).
- If flock fundamentally errors (no `flock` binary, etc.), exit subshell
  silently — fail-open per NFR-3.

## Acceptance criteria

| Criterion | Status |
|---|---|
| Both files mode 0755, `bash -n` clean | PASS |
| Linear: 3 starts + 2 stops → counter 1 | PASS |
| Floor: extra stops never go negative | PASS |
| Concurrency (realistic ordering): counter == expected | PASS |
| Concurrency (adversarial ordering): counter ≥ 0 (floor preserved) | PASS |
