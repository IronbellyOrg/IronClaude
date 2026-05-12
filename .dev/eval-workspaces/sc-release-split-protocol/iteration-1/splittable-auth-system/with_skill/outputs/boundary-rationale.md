# Split Boundary Rationale

## Split Point

The boundary falls between the **data model and engine layer** (Release 1: R1 Identity Model, R2 Permission Store, R3 Token Service, database schema) and the **integration and consumer layer** (Release 2: R4 Middleware, R5 Migration, R6 Dashboard, R7 SDKs, rollout plan).

This is a foundation-vs-application seam. Release 1 defines "what the unified auth system IS." Release 2 integrates it into "how the system RUNS."

## Why This Boundary

1. **Dependency DAG supports it**: R1 is a prerequisite for all other requirements. R2 and R3 depend on R1. R4 depends on R1+R2+R3. R5 depends on R1+R2+R3. R6 depends on R1+R2+R4. R7 depends on R3+R4. The boundary cleanly separates the foundation tier (no upward dependencies) from the consumer tier (depends on foundation).

2. **Highest-risk work is in Release 1**: The database schema (7 tables), identity model (canonical UUID, multi-credential support), permission semantics (RBAC hierarchy, resource-level scoping), and token lifecycle (issuance, revocation, introspection) are the hardest design decisions. Getting these wrong invalidates everything built on top. Validating them first prevents cascading errors.

3. **The three cited incidents trace to Release 1 scope**: The Feb 28 permission bypass (R2 scope), Mar 1 revocation delay (R3 scope), and Mar 10 audit correlation failure (R1 canonical UUID scope) are all addressable at the model/engine level. Release 1 validation can directly verify these are resolved.

4. **No tightly coupled pairs are bisected**: R1, R2, and R3 are self-contained engines with well-defined interfaces. R4 (middleware) consumes them but does not feed back into them. The boundary does not split any component that requires bidirectional interaction.

## Release 1 Delivers

- **Unified Identity Model**: A single `Identity` model with canonical UUID, multi-credential support, and credential rotation. This is the data model that replaces `WebUser`, `CLIIdentity`, and `OAuthClient`.
- **Centralized Permission Store**: RBAC permission engine with role hierarchy (`viewer < editor < admin < super_admin`), permission scopes, and resource-level permissions.
- **Unified Token Service**: JWT-based token issuance, refresh, revocation (within 1 second), and introspection.
- **Database Schema**: 7 production-ready tables validated at scale.
- **Independently testable**: The identity merge logic, permission mapping, token lifecycle, and schema can all be validated against real production data without deploying any new middleware or changing the running system.

## Release 2 Builds On

- **Auth Middleware** (R4): Replaces three middleware stacks with one. Depends on R1 for identity extraction, R2 for permission checking, R3 for token validation.
- **Migration Framework** (R5): Moves real users and permissions into the unified model. Depends on the Release 1 schema being stable and validated.
- **Admin Dashboard** (R6): Management UI for the unified system. Depends on R1 identity model, R2 permission engine, and R4 middleware being operational.
- **SDK Updates** (R7): Client libraries for the unified auth endpoints. Depends on R3 token service and R4 middleware providing stable APIs.
- **Full Rollout**: Shadow mode, system switchover, kill switches. Depends on all of the above.

## Cross-Release Dependencies

| Release 2 Item | Depends On (Release 1) | Type | Risk if R1 Changes |
|----------------|----------------------|------|---------------------|
| R4 Middleware — identity extraction | R1 Identity model and credential types | Hard | Middleware rewrite if identity model changes |
| R4 Middleware — permission checking | R2 Permission engine RBAC API | Hard | Permission enforcement logic rewrite |
| R4 Middleware — token validation | R3 Token service validation endpoint | Hard | Token validation integration rewrite |
| R5 Migration — target schema | Database schema (7 tables) | Hard | Migration scripts rewrite |
| R5 Migration — identity merging | R1 Identity merge mapping logic | Hard | Merge algorithm rewrite |
| R5 Migration — permission conflicts | R2 RBAC model semantics | Soft | Conflict resolution logic adjustment |
| R6 Dashboard — user search | R1 Identity model query patterns | Soft | Query adjustments |
| R6 Dashboard — role management | R2 Role hierarchy and permission model | Soft | UI adjustments for changed role semantics |
| R6 Dashboard — audit correlation | R1 Canonical UUID | Hard | Audit log viewer rewrite if UUID scheme changes |
| R7 SDK — authenticate() | R3 Token issuance API | Hard | SDK auth methods rewrite |
| R7 SDK — check_permission() | R2 Permission checking API | Hard | SDK permission methods rewrite |
| R7 SDK — backward compat wrappers | R1 Identity model mapping | Soft | Wrapper logic adjustment |

## Integration Points

1. **Identity Model API**: Release 2 components consume the Identity model through a defined API (CRUD operations, lookup by credential, merge resolution). This API must be stable after Release 1.

2. **Permission Engine API**: Release 2 middleware and dashboard consume the RBAC engine through `check_permission(identity, action, resource)` and role management APIs. These must be stable after Release 1.

3. **Token Service API**: Release 2 middleware validates tokens via the introspection endpoint. SDKs issue tokens via the issuance endpoint. These endpoints must be stable after Release 1.

4. **Database Schema**: Release 2 migration writes to the 7-table schema. Dashboard reads from it. Schema must be stable after Release 1 validation.

## Handoff Criteria

Before Release 2 planning begins, Release 1 must demonstrate:

1. Identity merge correctly handles production data from all three systems (zero data loss)
2. Permission mapping resolves the Feb 28 permission bypass scenario
3. Token revocation meets the 1-second propagation requirement (resolves Mar 1 incident)
4. Canonical UUID enables audit correlation (resolves Mar 10 incident)
5. Schema handles production-scale data with acceptable query performance
6. Engineering lead and security lead have reviewed and approved validation results

## Reversal Cost

**Low**. Merging Release 1 and Release 2 back into a single release requires:
- Combining the two specs into one (editorial work)
- No architectural changes — Release 1 deliverables are consumed by Release 2 regardless of whether they ship separately
- No code changes — the same code is written either way; only the shipping schedule changes
- Some validation work from Release 1 would need to be re-planned as part of the integrated release testing strategy

The split is reversible at any point before Release 2 planning begins with minimal overhead.
