# Tasklist (fixture) — serena-handoff (FR-3)

# Drives the Tier-3 handoff-bridge variants. A regression in the work forces a Tier-3
# --remediate path; reflect writes reflect/handoff-{slug}-{ts} BEFORE the task-builder spawn.
- Task 1: --remediate accepted, prepare_for_new_conversation present → handoff written before task-builder
- Task 2: --remediate accepted, tool context-excluded → write_memory fallback
- Task 3: both tool + write_memory fail → handoff_persist_failed, report still ships
- Task 4: no --remediate → no-op (handoff_memory_key: null)
- Task 5: FR-3.7 retention — N>20 handoff entries trigger a sweep down to the 20-entry cap
