# Dependency Analysis: v3.2 Unified Auth System

## Requirement Dependency Map

```
R1 (Identity Model)  ──────┐
                            ├──► R4 (Auth Middleware)  ──► R5 (Migration)
R2 (Permission Store) ─────┤                               │
                            │                               ▼
R3 (Token Service) ────────┘                          R6 (Admin Dashboard)
                                                           │
                                                           ▼
                                                      R7 (SDK Updates)
```

## Dependency Details

| Requirement | Depends On | Depended On By | Priority |
|-------------|-----------|----------------|----------|
| R1: Identity Model | None | R2, R3, R4, R5, R6, R7 | P0 |
| R2: Permission Store | R1 | R4, R5, R6 | P0 |
| R3: Token Service | R1 | R4, R5, R7 | P0 |
| R4: Auth Middleware | R1, R2, R3 | R5 | P1 |
| R5: Migration Framework | R1, R2, R3, R4 | R6 (partial) | P1 |
| R6: Admin Dashboard | R1, R2 (R5 for full utility) | None | P2 |
| R7: SDK Updates | R3, R4 | None | P2 |

## Natural Seam Identification

There is a clear dependency boundary between two groups:

**Foundation Group (R1 + R2 + R3 + R4):** These form the core infrastructure. R1, R2, R3 are independent of each other at the model level but all feed into R4. This group is self-contained — once built, the unified auth service exists and can run in shadow mode.

**Adoption Group (R5 + R6 + R7):** These depend on the foundation being in place. They handle migration, management, and external integration. They cannot be meaningfully started until R4 is at least functional.

## Coupling Assessment

- **R1-R2 coupling:** Medium. Permission store references identity IDs, but the schema/model work is independent.
- **R1-R3 coupling:** Medium. Token service issues tokens for identities, but token logic is self-contained.
- **R4 integration coupling:** High with R1/R2/R3 — it's the integration point.
- **R5-R4 coupling:** High. Migration must test against working middleware.
- **R6-R5 coupling:** Low. Dashboard can be built against R1/R2 directly; migration is independent functionality.
- **R7-R3/R4 coupling:** Medium. SDKs call new endpoints but are largely client-side work.

## Split Feasibility

**Verdict: Highly splittable.** The priority markers (P0 vs P1 vs P2) already reveal the natural split. The dependency graph has a clean cut between the foundation layer (R1-R4) and the adoption layer (R5-R7). The rollout plan in the spec even sequences them this way — shadow mode and migration come after the unified service is deployed.
