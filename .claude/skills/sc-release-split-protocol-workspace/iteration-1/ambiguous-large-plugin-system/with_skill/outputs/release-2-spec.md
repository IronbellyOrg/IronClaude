---
release: 2
parent-spec: /config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/evals/files/spec-ambiguous-plugin-system.md
split-proposal: /config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/iteration-1/ambiguous-large-plugin-system/with_skill/outputs/split-proposal-final.md
scope: "Distribution infrastructure — registry, marketplace, CLI registry ops, advanced hooks, PDK, analytics, enterprise"
status: draft
validation-gate: "blocked until R1 real-world validation passes"
---

# Release 2 — Plugin Distribution Infrastructure

## Objective

Build the server-side distribution infrastructure and advanced tooling that transforms the local plugin runtime (Release 1) into a full ecosystem. This includes the plugin registry, marketplace web UI, CLI registry operations, advanced lifecycle hooks, plugin development kit, analytics, and enterprise governance.

## Scope

### Included

1. **R2: Plugin Registry** (full scope)
   - RESTful API: publish, search, download, version listing
   - Scoped namespaces: `@org/plugin-name` format
   - Semantic versioning with dependency resolution
   - Rate limiting and abuse prevention
   - Storage backend: S3-compatible object store for packages, PostgreSQL for metadata
   - From: [original-spec] Section 2, R2

2. **R3: CLI Plugin Manager — Registry Operations** (remaining scope from R1)
   - `superclaude plugin install <name>[@version]` — download from registry, verify, install
   - `superclaude plugin update [name]` — check registry and apply updates
   - `superclaude plugin publish` — package and upload to registry
   - Registry source integration into install engine (replacing R1's stubs)
   - From: [original-spec] Section 2, R3 (registry subset)

3. **R5: Plugin Lifecycle Hooks — Advanced Hooks** (remaining scope from R1)
   - `on-error`: runs when a command fails
   - `transform-output`: modifies command output before display
   - `custom-command`: registers new `/sc:*` commands
   - From: [original-spec] Section 2, R5 (on-error, transform-output, custom-command)

4. **R6: Marketplace Web UI** (full scope)
   - Search with filtering by category, author, rating
   - Plugin detail pages with README, screenshots, install stats
   - One-click install (launches CLI via protocol handler)
   - User ratings and reviews
   - Featured/curated collections
   - Author verification badges
   - From: [original-spec] Section 2, R6

5. **R8: Plugin Development Kit** (full scope)
   - `superclaude plugin init` — scaffold a new plugin project
   - `superclaude plugin dev` — local development mode with hot reload
   - `superclaude plugin test` — run plugin's test suite in sandbox
   - TypeScript type definitions for hook APIs (including advanced hooks)
   - Python stub packages for sandbox API
   - Example plugins: custom command, output transformer, MCP bridge
   - From: [original-spec] Section 2, R8

6. **R9: Plugin Analytics** (full scope)
   - Install/uninstall counts per plugin
   - Error rates and crash reports (opt-in)
   - Performance impact metrics (command latency with/without plugin)
   - Author dashboard: usage stats, error reports, user feedback
   - From: [original-spec] Section 2, R9

7. **R10: Enterprise Plugin Policies** (full scope)
   - Approved plugin allowlist per org
   - Private registries for internal plugins
   - Plugin audit trail for compliance
   - Automatic security scanning of published plugins
   - Policy enforcement: block unsigned or unreviewed plugins
   - From: [original-spec] Section 2, R10

### Excluded (delivered in Release 1)

1. **R1: Plugin Package Format** — Delivered in Release 1.
2. **R3: CLI Manager — Offline Operations** — Delivered in Release 1.
3. **R4: Sandboxed Execution** — Delivered in Release 1.
4. **R5: Basic Lifecycle Hooks** (pre-command, post-command) — Delivered in Release 1.
5. **R7: Migration** — Delivered in Release 1.

## Dependencies

### Prerequisites (from Release 1)

| Release 1 Deliverable | Release 2 Consumer | Dependency Type |
|----------------------|-------------------|-----------------|
| R1: Package Format (manifest schema, signing) | R2: Registry stores and validates packages | Hard |
| R1: Package Format (manifest schema) | R6: Marketplace displays plugin metadata | Hard |
| R3: CLI install engine (with registry stubs) | R3-R2: Registry source replaces stubs | Hard |
| R4: Sandbox runtime | R8: PDK test command uses sandbox | Hard |
| R5: Basic hooks (pre/post-command) | R5-R2: Advanced hooks extend same system | Hard |
| R7: Migration tooling | R8: PDK references migration path | Soft |

### External Dependencies
- PostgreSQL >= 15 (registry metadata)
- S3-compatible storage (plugin packages)
- Web framework: React + Next.js (marketplace UI)
- From: [original-spec] Section 4

## Real-World Validation Requirements

1. **Publish-discover-install workflow**: Author publishes a plugin via CLI. Another user discovers it via marketplace search. User installs via one-click or CLI. Plugin executes correctly. Success: end-to-end flow completes in < 2 minutes.

2. **Registry under load**: Simulate 1000 concurrent downloads (using real HTTP clients against deployed registry, not mocked). Measure response times and error rates. Success: p99 latency < 5s, error rate < 0.1%.

3. **Advanced hook execution**: Install a plugin with `custom-command` hook that registers `/sc:my-plugin`. Execute the custom command in a real session. Install a `transform-output` hook. Verify output modification works correctly.

4. **PDK author workflow**: A real plugin author (not the developer) uses `plugin init`, `plugin dev` (hot reload), and `plugin test` to develop a plugin from scratch. Measures: time to first working plugin, errors encountered. Success: author creates and publishes a working plugin within 1 hour.

5. **Enterprise policy enforcement**: Configure an org allowlist. Attempt to install a non-allowlisted plugin. Verify it is blocked. Configure a private registry. Publish and install from private registry. Verify isolation from public registry.

6. **Security scanning**: Publish a plugin with known vulnerability patterns. Verify automatic scanner detects and flags the plugin. Verify flagged plugins are not installable without explicit override.

## Success Criteria

- Plugin install-to-working takes < 30 seconds (from registry)
- Registry handles 1000 concurrent downloads
- Marketplace search returns relevant results within 500ms
- Migration guide enables authors to self-serve conversion (from Release 1 foundation)
- PDK enables new plugin creation within 1 hour for experienced developers

## Planning Gate

> **This release's roadmap and tasklist generation may proceed only after Release 1 has passed real-world validation and the results have been reviewed.**
>
> **Validation criteria**: All 7 Release 1 real-world validation scenarios must pass. Specifically:
> - Package format validated by real users creating plugins
> - Sandbox escape testing shows zero successful escapes
> - Migration fidelity confirmed for existing skills
> - Permission model usability confirmed (>= 4/5 users)
>
> **Review process**: Engineering lead and security lead review Release 1 validation results. Focus areas: (1) any manifest schema changes needed based on user feedback, (2) any sandbox security gaps discovered, (3) any permission model usability issues.
>
> **If validation fails**:
> - Minor issues: Fix in a Release 1 patch, re-validate, then proceed to Release 2.
> - Major format/sandbox issues: Revise Release 1 design, re-validate. Release 2 timeline adjusts accordingly.
> - Fundamental design flaw: Re-evaluate whether to merge releases back into a single redesigned release.

## Traceability

| Release 2 Item | Original Spec Source |
|----------------|---------------------|
| Plugin Registry (full) | R2 — Section 2 |
| CLI Manager — registry ops | R3 — Section 2 (install from registry, update, publish) |
| Advanced Lifecycle Hooks | R5 — Section 2 (on-error, transform-output, custom-command) |
| Marketplace Web UI (full) | R6 — Section 2 |
| Plugin Development Kit (full) | R8 — Section 2 |
| Plugin Analytics (full) | R9 — Section 2 |
| Enterprise Policies (full) | R10 — Section 2 |
| PostgreSQL, S3, React/Next.js deps | Section 4 |
