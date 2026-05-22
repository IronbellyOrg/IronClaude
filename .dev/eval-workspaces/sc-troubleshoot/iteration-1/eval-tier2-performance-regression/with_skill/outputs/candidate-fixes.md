# Candidate Fixes — Wave 3 Distillation

All three Tier 2 agents converge on the diagnosis (N+1 from three lazy relationships in `views/dashboard.py` driven by `models/widget.py` defaults). They diverge on **fix mechanism**, so the proposals are marked `competing` and Wave 4 (`sc:adversarial`) is triggered.

## Fix A — Per-cardinality loader strategy

- **Champion**: performance-engineer
- **Mechanism**: `joinedload(owner)`, `joinedload(last_edit).joinedload(editor)`, `selectinload(tags)`
- **Verdict**: competing
- **One-line rationale**: matches SQLAlchemy idioms — joinedload for single-row, selectinload for collections.

## Fix B — Uniform selectinload

- **Champion**: root-cause-analyst (Tier 2)
- **Mechanism**: `selectinload(...)` for all three relationships
- **Verdict**: competing
- **One-line rationale**: simpler, immune to row explosion, but does extra round-trips on single-row relationships.

## Fix C — Loader options + serializer + per-user cache

- **Champion**: system-architect
- **Mechanism**: Fix A in Phase 1; DTO + `flask_caching` per-user TTL in Phase 2.
- **Verdict**: competing-but-broader-scope
- **One-line rationale**: solves the regression and the structural fragility, but Phase 2 is out-of-scope for a regression hotfix.

## Convergence summary

- Diagnosis: **consensus** — N+1 query storm on lazy relationships.
- Fix: **3 competing mechanisms** — adversarial debate required to settle on one.
