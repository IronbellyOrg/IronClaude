# Risk Assessment: Ship-Together vs. Split

## Risks of Shipping Everything in v3.2

### 1. Blast Radius (CRITICAL)
The spec touches the authentication path for every user across web, CLI, and plugins simultaneously. Shipping identity model changes, permission engine, token service, migration tooling, AND SDK updates in one release means a bug in any component can break auth for everyone. The rollout plan acknowledges this with "kill switches" — but kill switches for 7 interdependent components are hard to operate cleanly.

### 2. Testing Surface (HIGH)
The testing strategy calls for unit tests, integration tests, migration tests, security audits, AND 2-week shadow mode validation. Doing all of this for 7 requirements at once means the test matrix is multiplicative, not additive. Credential type (3) x auth flow (3) x permission model (old vs new) x migration state (pre/during/post) creates a combinatorial explosion.

### 3. Rollback Complexity (HIGH)
If migration (R5) reveals a problem with the permission model (R2), rolling back requires undoing everything — including token changes that SDKs may already depend on. A split release lets you validate the foundation before committing to migration.

### 4. Team Parallelism Bottleneck (MEDIUM)
R6 (Admin Dashboard) and R7 (SDK Updates) require different expertise (frontend, client-side) than R1-R4 (backend, security). Shipping together forces all teams onto the same release train and timeline.

### 5. Shadow Mode Ambiguity (MEDIUM)
The spec calls for 2 weeks of shadow mode. But shadow mode for what? The core auth service? The migration? The SDKs? Splitting makes this concrete: Release 1 ships with shadow mode for the core service. Release 2 starts after shadow mode validates.

## Risks of Splitting

### 1. Partial State Duration (MEDIUM)
Between releases, the system runs both old and new auth. This is already planned (shadow mode), but extending it across releases means maintaining dual systems longer. Mitigation: keep the gap short (2-4 weeks).

### 2. API Surface Churn (LOW-MEDIUM)
If R1-R4 ship first, the API may need adjustments when R5-R7 reveal new requirements. Mitigation: the spec's architecture is already well-defined; the risk of needing API changes for migration or SDK needs is low.

### 3. Coordination Overhead (LOW)
Two releases means two sets of release notes, two deployment windows. This is minor compared to the risk reduction.

## Risk Comparison Summary

| Risk Factor | Ship Together | Split |
|------------|--------------|-------|
| Blast radius | CRITICAL | Reduced to MEDIUM per release |
| Test matrix complexity | HIGH (multiplicative) | MEDIUM (additive per release) |
| Rollback difficulty | HIGH | LOW per release |
| Shadow mode clarity | Ambiguous | Clear scope per release |
| Dual-system maintenance | N/A | SHORT-TERM cost |
| Total risk | HIGH | MEDIUM-LOW |
