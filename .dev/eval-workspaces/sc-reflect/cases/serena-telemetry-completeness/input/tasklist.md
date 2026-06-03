# Tasklist (fixture) — serena-telemetry-completeness (NFR-2, holistic)

# A multi-FR run that exercises all four medium adoptions so the telemetry sweep can assert,
# in ONE pass over audit.log + the return contract, that every new FR emits its
# <tool>_invoked/_ran field AND its degraded/skip-reason field on BOTH paths.
- Task 1: touches a type (FR-1), a verifiable module (FR-4), runs --onboard (FR-2), and --remediate (FR-3)
- Task 2: a degraded-path variant where each tool is unavailable (skip reasons emitted)
