# Recommendation — Refactor `src/utils/timefmt.py` (~40 lines)

**Recommendation kind:** `native_tooling`

No skill / command / agent delegation adds net value here. Use native tools.

## Native-tool sequence

1. `Read` `src/utils/timefmt.py` to load the full ~40 lines into context.
2. `Edit` (or `Write` for a full rewrite) to apply the refactor in place.
3. Optional: `Bash` to run the file's tests (e.g. `uv run pytest tests/utils/test_timefmt.py -v`) to confirm behavior is preserved.

## Reason (Phase 1 net-value evaluation)

All four "default to native" conditions in `refs/delegation-vs-native-heuristics.md` are satisfied:

- Task fits in 1 read + 1-2 edits.
- Model can hold ~40 lines of context without loss.
- No specialized capability required (no multi-agent debate, no semantic ranking across the repo, no structured template, no browser automation).
- No structured artifact (PRD / TDD / tasklist / roadmap) requested.

The rubric's table is explicit: **"Single-file refactor of a small util → Read + Edit → NO, native wins"** and **"'Refactoring this small util' — unless the util is genuinely tangled, native wins."**

Invoking `/sc:improve`, `/sc:cleanup`, or `/sc:cli-portify` here would load a multi-phase protocol whose loading cost dwarfs the ~40 lines of actual work. That is the exact anti-pattern Phase 1 exists to block.

## Escalation triggers (when this answer changes)

Recommend delegation **only if** one of these surfaces during the Read:

- The util is genuinely tangled (deep nesting, hidden state, > 3 responsibilities) → consider `/sc:improve --quality`.
- The refactor turns out to span > 3 files once call sites are inspected → re-run `/sc:recommend` with the broader scope.
- The user wants an audit-trail artifact (before/after diff with reasoning) → consider `/sc:cleanup-audit`.

Absent those, stop after `Read` + `Edit`.

## Sources verified

- `.claude/skills/sc-recommend/SKILL.md` — Phase 1 net-value gate (Read)
- `.claude/skills/sc-recommend/refs/delegation-vs-native-heuristics.md` — explicit "single-file refactor of small util" → native, and "'Refactoring this small util' — native, always" (Read)
- Auggie semantic ranking: skipped intentionally. Phase 0 Step B exists to rank candidates when delegation is plausible; the rubric pre-resolves this case to native, so spending an Auggie query on it would itself be the bloat the skill is designed to prevent.
