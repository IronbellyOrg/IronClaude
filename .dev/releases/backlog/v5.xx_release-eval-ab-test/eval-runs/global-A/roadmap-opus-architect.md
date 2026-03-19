Roadmap written to `.dev/releases/current/v3.0_unified-audit-gating/eval-runs/global-A/roadmap.md`.

Key highlights:
- **5 phases, 25 tasks**, single-sprint scope matching the 0.45 complexity score
- **Critical path**: data models → executor wiring → extended metadata → integration tests
- **1 blocking prerequisite** (GAP-002: deviation sub-entry schema) gates Phase 4.2 but doesn't block other work
- **3 contradiction resolutions** proposed: `--resume` vs overwrite, "significant findings" threshold, certification→remediation reference mechanism
- **Architectural invariant enforced**: `commands.py → executor.py → progress.py → models.py/gates.py` — no circular dependencies, no changes to gate enforcement logic
- All 6 explicit FRs, 6 implicit FRs, and 5 NFRs mapped to specific phases with acceptance criteria
