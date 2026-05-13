# TASKLIST INDEX -- Roadmap Pipeline Downstream Fix (deviation-analysis + certify)

## Metadata & Artifact Paths

| Field | Value |
|---|---|
| Sprint Name | Roadmap Pipeline Downstream Fix |
| Source | Handoff from AI-1 + adversarial debate (Solution B winner) |
| Generated | 2026-04-05T00:00:00Z |
| TASKLIST_ROOT | .dev/releases/current/v3.66-tdd-skill-refactor-v2/tasklist-pipeline-fix/ |
| Total Phases | 3 |
| Total Tasks | 8 |
| Complexity Class | MEDIUM |
| Primary Persona | backend |
| Consulting Personas | qa, architect |
| Branch | feat/v3.65-prd-tdd-Refactor |

**Artifact Paths**

| Asset | Path |
|---|---|
| This file | TASKLIST_ROOT/tasklist-index.md |
| Phase 1 Tasklist | TASKLIST_ROOT/phase-1-deviation-analysis.md |
| Phase 2 Tasklist | TASKLIST_ROOT/phase-2-certify-wiring.md |
| Phase 3 Tasklist | TASKLIST_ROOT/phase-3-hardening-verification.md |

## Phase Files

| Phase | File | Phase Name | Task IDs | Tier Distribution |
|---|---|---|---|---|
| 1 | phase-1-deviation-analysis.md | Deviation Analysis Classification Fix | T01.01-T01.03 | STRICT: 2, STANDARD: 1 |
| 2 | phase-2-certify-wiring.md | Certify Step Wiring (Mode-Aware Gate) | T02.01-T02.03 | STRICT: 3 |
| 3 | phase-3-hardening-verification.md | Hardening + End-to-End Verification | T03.01-T03.02 | STRICT: 1, STANDARD: 1 |

## Dependency Graph

```
T01.01 (classify records) ──┐
T01.02 (DEV-N IDs)         ─┤──> T01.03 (test deviation-analysis)
                             │
T02.01 (certify step)      ─┤
T02.02 (mode-aware gate)   ─┤──> T02.03 (test certify)
T02.03 depends on T01.03    │
                             │
T03.01 (convergence fix)   ─┤──> T03.02 (E2E pipeline run)
T03.02 depends on T01.03, T02.03
```

## Source Snapshot

- Pipeline passes spec-fidelity and wiring-verification after AI-1 fixes
- deviation-analysis crashes fixed (dict-vs-list) but analysis is semantically hollow (0 classifications)
- certify step never wired into pipeline (build + handler both missing)
- Adversarial debate selected Solution B (pipeline-mode-aware gate) over deferred-resolution and escalation alternatives
- DeviationRegistry.load_or_create has latent dict-vs-list crash on legacy data
