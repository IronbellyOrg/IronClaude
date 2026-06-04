# Tasklist (fixture) — serena-onboarding (FR-2)

# Drives the FR-2 onboarding-bootstrap variants. Reflect runs UC-2 over this tasklist; the
# onboarding bootstrap is a Wave-0 0.7b concern gated on --onboard + empty project memory.
- Task 1: cold start, --onboard set, project memory empty, onboarding tool available → bootstrap runs
- Task 2: silent-fail variant — onboarding completes but list_memories delta ≤ 0
- Task 3: context-excluded variant — --onboard set but onboarding tool not in active context
- Task 4: warm-start variant — list_memories non-empty
- Task 5: no-flag variant — --onboard NOT set
- Task 6: NFR-7 budget variant — oversized project exceeds the T1 context budget
