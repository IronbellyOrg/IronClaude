# Split Recommendation: v5.0 Plugin System Architecture

## Verdict: SPLIT — into 3 releases

The spec should be split. The evidence is strong:

1. **3,600-5,000 estimated lines** — 2-3x normal release size
2. **Clean dependency seam** between client-side and server-side clusters
3. **The spec's own rollout plan already phases it** (Alpha/Beta/GA/Post-GA)
4. **4 distinct technology domains** — Python CLI, V8/sandbox runtime, PostgreSQL/S3 server, React/Next.js frontend
5. **Security-critical component (sandbox)** needs dedicated focus and audit time

---

## Proposed Split

### Release v5.0: Plugin Runtime Foundation
**Requirements**: R1 (Package Format), R3 (CLI — local install only), R4 (Sandbox), R5 (Lifecycle Hooks)
**Estimated scope**: 1,600-2,200 lines
**Priority**: All P0 + one P1
**Domain**: Backend + Security (focused)

**What ships**:
- `.claude-plugin` package format with manifest.json schema
- `superclaude plugin install/remove/list` working with local `.claude-plugin` files
- V8 isolate for TypeScript plugins, subprocess sandbox for Python plugins
- Permission model with user approval flow
- Lifecycle hooks (pre-command, post-command, on-error, transform-output, custom-command)
- Signature verification (GPG/certificate)

**Why this is the right first cut**:
- Delivers immediate user value: people can build, share (via file), and run plugins
- Freezes the package format contract that everything else depends on
- Gets the hardest security work (sandbox) done with full attention
- Zero infrastructure requirements — no server, no database, no new frontend stack
- Directly matches the spec's "Alpha" rollout phase

**Exit criteria before moving to v5.1**:
- Package format schema is frozen and documented
- Sandbox escape test suite passes
- At least 3 internal plugins successfully installed and running
- CLI commands are stable (no breaking changes expected)

---

### Release v5.1: Registry and Marketplace
**Requirements**: R2 (Registry), R6 (Marketplace UI), R7 (Migration), R8 (PDK)
**Estimated scope**: 1,600-2,200 lines
**Priority**: P0 (R2) + P1s + P2
**Domain**: Backend/DevOps + Frontend

**What ships**:
- Plugin registry server (REST API, S3 storage, PostgreSQL metadata)
- `superclaude plugin publish/update` commands (CLI talks to registry)
- Marketplace web UI with search, plugin pages, one-click install
- `superclaude plugin migrate` for converting skills to plugins
- Plugin Development Kit: `plugin init`, `plugin dev`, `plugin test`
- TypeScript type definitions and Python stubs for hook APIs

**Why this is the right second cut**:
- Registry is a new service with its own infrastructure — deploying it separately reduces blast radius
- Marketplace UI is an entirely new frontend codebase (React/Next.js) — deserves its own release cycle
- Migration tooling (R7) benefits from v5.0 field experience — real plugin usage reveals edge cases
- PDK (R8) benefits from real authors having tried to build plugins in v5.0

**Depends on v5.0**: Package format (R1) must be frozen. CLI plugin infrastructure must be stable.

---

### Release v5.2: Enterprise and Analytics
**Requirements**: R9 (Analytics), R10 (Enterprise Policies)
**Estimated scope**: 400-600 lines
**Priority**: P2
**Domain**: Backend + Frontend (dashboards)

**What ships**:
- Install/uninstall telemetry, error rates, performance metrics
- Author dashboard with usage stats
- Org-level plugin allowlists
- Private registries for internal plugins
- Plugin audit trail and compliance logging
- Automatic security scanning pipeline

**Why separate**:
- Pure additive — zero impact on v5.0 or v5.1 functionality
- Enterprise features need real marketplace usage data to design correctly
- Analytics requires opt-in consent flows that deserve dedicated UX attention
- Smallest release; can be accelerated or deferred based on demand

---

## Summary Table

| Release | Requirements | Est. Lines | New Infra | Key Risk |
|---------|-------------|-----------|-----------|----------|
| v5.0 | R1, R3, R4, R5 | 1,600-2,200 | None | Sandbox security |
| v5.1 | R2, R6, R7, R8 | 1,600-2,200 | PostgreSQL, S3, React/Next.js | New server stack |
| v5.2 | R9, R10 | 400-600 | Analytics pipeline | Low |

## Alternative Considered: 2-Way Split

A 2-way split (v5.0 = R1+R3+R4+R5+R7, v5.1 = R2+R6+R8+R9+R10) is also viable. The 3-way split is preferred because:
- v5.2 requirements are all P2 and truly independent
- Keeps each release under 2,200 lines
- Matches the spec's 4-phase rollout plan almost exactly

## Alternative Considered: No Split

Not recommended. A single 3,600-5,000 line release spanning Python CLI, V8 runtime, server infrastructure, React frontend, and security auditing would be the riskiest release in the project's history. The dependency graph has a clean seam — use it.
