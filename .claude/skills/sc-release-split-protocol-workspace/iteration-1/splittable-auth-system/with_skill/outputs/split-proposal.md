# Split Proposal — v3.2 Unified Authentication & Authorization System

## Discovery Analysis

### Spec Summary

The v3.2 release unifies three independent auth systems (web session, CLI API key, OAuth2 plugin) into a single identity and permission system. It contains 7 requirements spanning 3 priority levels:

- **P0 (Core)**: R1 (Unified Identity Model), R2 (Centralized Permission Store), R3 (Unified Token Service)
- **P1 (Integration)**: R4 (Auth Middleware Consolidation), R5 (Migration Framework)
- **P2 (Consumer)**: R6 (Admin Dashboard), R7 (Developer SDK Updates)

Estimated scope: 2000-2500 lines production code across backend (60%), security (25%), frontend (15%).

### Dependency Analysis

```
R1 (Identity Model) ──┬──> R2 (Permissions) ──┬──> R4 (Middleware) ──> R6 (Dashboard)
                       │                        │
                       ├──> R3 (Token Service) ─┘
                       │
                       └──> R5 (Migration) [depends on R1+R2+R3]

R3 (Token Service) + R4 (Middleware) ──> R7 (SDK Updates)
```

R1 is the foundation for everything. R2 and R3 depend on R1 but are largely independent of each other. R4 consumes R1+R2+R3. R5 needs the data model stable. R6 and R7 are consumer layers that depend on the core being complete and integrated.

### Discovery Questions

**Q1: Are there components that deliver standalone value and can be validated through real-world use before the rest ships?**

Yes. R1 (Identity Model) + R2 (Permission Store) + R3 (Token Service) + the database schema constitute the foundational data model and engine layer. These can be deployed, tested with real data, and validated before the integration layers are built on top. The identity model can be populated from existing user data in a non-enforcing mode. The permission engine can be tested against real permission scenarios. The token service can be validated for issuance/revocation behavior.

**Q2: What is the cost of splitting?**

- Two release cycles with coordination overhead
- Schema must be stable before Release 2; changes after Release 1 ships would require migration-on-migration
- Context switching between releases
- Release 1 delivers infrastructure that has no user-visible impact until Release 2 integrates it

**Q3: What is the cost of NOT splitting?**

- Big-bang deployment of a security-critical system with 7 interrelated components
- If the identity model or schema is wrong, everything built on top fails — root-cause isolation is harder
- No feedback on the foundational data model until the entire system ships
- The current system is actively producing security incidents (permission bypass, delayed revocation, audit correlation failure)

**Q4: Is there a natural foundation vs. application boundary?**

Yes — a clear seam exists between:
- **Foundation (data model + engines)**: R1, R2, R3, database schema
- **Application (integration + consumer layers)**: R4, R5, R6, R7

This is not an artificial division. R1+R2+R3 define the data model, permission semantics, and token behavior. R4+R5+R6+R7 integrate those into the running system, migrate data, build UIs, and update SDKs.

**Q5: Could splitting INCREASE risk?**

Low risk of misleading intermediate state. Shipping R1+R2+R3 without R4 means the old auth systems continue running unchanged. No user faces a half-baked auth experience. The new identity model can run in parallel (shadow mode concept from R5) during the validation period. The main risk is schema churn — if Release 1 validation reveals schema problems, Release 2 scope could expand. This is mitigated by focusing Release 1 validation on schema correctness specifically.

**Q6: Does Release 1 create meaningful value for Release 2, not just "the easiest work"?**

Yes. The identity model and permission engine are the hardest design decisions in this release, not the easiest. Getting the schema right — canonical UUID, credential types, role hierarchy, resource-level permissions — is the highest-risk work. Validating it before building 4 more systems on top is the highest-leverage split possible.

### Recommendation: SPLIT

**Confidence: 0.85**

### Proposed Split

**Release 1: Identity & Permission Foundation**
- R1: Unified Identity Model (full scope)
- R2: Centralized Permission Store (full scope)
- R3: Unified Token Service (full scope)
- Database schema (all 7 tables)
- Schema validation and real-world data testing

**Release 2: Integration, Migration & Consumer Layers**
- R4: Auth Middleware Consolidation
- R5: Migration Framework
- R6: Admin Dashboard
- R7: Developer SDK Updates
- Full system integration and switchover

### The Seam

The boundary falls between "defining the unified auth model" and "integrating it into the running system." Release 1 answers the question: "Is our unified identity/permission/token model correct?" Release 2 answers: "Can we migrate to it and expose it to all consumers?"

This is a foundation-vs-application seam. Release 1 delivers the foundation that every Release 2 component depends on.

### Real-World Validation Plan for Release 1

1. **Identity merging test**: Take production user data from all three systems, run the merge logic, verify canonical UUIDs are assigned correctly and no identities are lost or incorrectly merged
2. **Permission mapping test**: Map existing permissions from all three stores into the RBAC model, verify no permission escalation or loss occurs
3. **Token lifecycle test**: Issue tokens via the new service, verify refresh, revocation (within 1 second), and introspection work correctly
4. **Schema stress test**: Load production-scale data into the new schema, verify query performance and constraint integrity
5. **Cross-system correlation**: Verify audit log entries can be correlated via canonical UUID across all three original systems

### Risks of the Split

| Risk | Severity | Mitigation |
|------|----------|------------|
| Schema changes after R1 ships | HIGH | Focus R1 validation specifically on schema correctness; design migration path for schema evolution |
| R1 delivers no user-visible value | MEDIUM | Acceptable — R1's value is de-risking the foundation, not shipping features |
| Coordination overhead of 2 releases | LOW | Clear dependency boundary minimizes coordination; R2 planning gates on R1 validation |
| R1 false confidence (tests pass but integration fails) | MEDIUM | R1 validation must include real data from all 3 existing systems, not synthetic data |

### R1 Scope Bias

Following default `--r1-scope fidelity-schema`: Release 1 focuses on planning fidelity (is the model correct?) and schema hardening (is the data model production-ready?).

### Smoke Gate Placement

Following default `--smoke-gate r2`: Smoke gate placed in Release 2, where the integrated system is tested end-to-end with real auth flows.
