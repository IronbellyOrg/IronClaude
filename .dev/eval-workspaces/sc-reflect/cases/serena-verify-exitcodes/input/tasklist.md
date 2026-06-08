# Tasklist (fixture) — serena-verify-exitcodes (FR-4.3 / C2)

# Drives each exit code through the exit-code → deviation-class taxonomy.
- Task 1: `pytest` exit 1 (test failed) on a claimed-passing file → Regression
- Task 2: `pytest` exit 2 (collection error) → Grounding Gap
- Task 3: `pytest` exit 5 (no tests collected; claimed-added test absent) → Drift
- Task 4: `ruff` exit 1 (lint finding) → S_dev_density signal (NOT regression)
- Task 5: `mypy` exit 1 (type finding) → S_dev_density signal (NOT regression)
- Task 6: any tool exit 124 (timeout) → Grounding Gap
- Task 7: flaky test (retry flips fail→pass) → Grounding Gap + verify_flaky_suspected
