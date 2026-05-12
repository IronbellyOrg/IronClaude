# Dependency Analysis: v5.0 Plugin System

## Requirement Dependency Graph

```
R1 (Package Format)
 └──> R3 (CLI Plugin Manager) — needs format to install/publish
 └──> R4 (Sandboxed Runtime) — needs manifest for permissions
 └──> R7 (Migration) — needs format as target

R2 (Registry)
 └──> R6 (Marketplace UI) — web frontend for registry API
 └──> R9 (Analytics) — telemetry layered on registry data
 └──> R10 (Enterprise Policies) — governance layered on registry

R3 (CLI Plugin Manager)
 └──> R5 (Lifecycle Hooks) — hooks loaded/triggered via CLI runtime
 └──> R7 (Migration) — `plugin migrate` is a CLI command
 └──> R8 (PDK) — `plugin init/dev/test` are CLI commands

R4 (Sandboxed Runtime)
 └──> R5 (Lifecycle Hooks) — hooks execute inside sandbox

R5 (Lifecycle Hooks)
 └──> R8 (PDK) — PDK provides types/stubs for hook APIs
```

## Coupling Matrix

| Req | Tightly Coupled With | Loosely Coupled With |
|-----|---------------------|---------------------|
| R1 (Package Format) | R3 (CLI), R4 (Sandbox) | R7 (Migration) |
| R2 (Registry) | — | R6 (Marketplace), R9, R10 |
| R3 (CLI Manager) | R1 (Format) | R5, R7, R8 |
| R4 (Sandbox) | R1 (Format), R5 (Hooks) | — |
| R5 (Hooks) | R4 (Sandbox) | R3 (CLI), R8 (PDK) |
| R6 (Marketplace) | R2 (Registry) | — |
| R7 (Migration) | R1 (Format), R3 (CLI) | — |
| R8 (PDK) | R3 (CLI), R5 (Hooks) | — |
| R9 (Analytics) | R2 (Registry) | — |
| R10 (Enterprise) | R2 (Registry) | — |

## Natural Seam Identification

The dependency graph reveals two distinct clusters with a clean boundary between them:

### Cluster A: Client-Side Foundation (R1, R3, R4, R5)
- Package format definition
- CLI install/remove/update from local files
- Sandboxed execution environment
- Lifecycle hooks
- **No server-side dependencies. Fully functional with local .claude-plugin files.**

### Cluster B: Server-Side Ecosystem (R2, R6, R9, R10)
- Plugin registry server
- Marketplace web UI
- Analytics dashboard
- Enterprise policies
- **Requires Cluster A to be stable (format must be frozen).**

### Bridge Requirements (R7, R8)
- R7 (Migration): Needs format from A, CLI from A. No server dependency. Fits in A.
- R8 (PDK): Needs CLI from A, hook types from A. Can work offline. Fits in A or as its own phase.

## Cross-Cluster Dependencies

The ONLY dependency from Cluster B to Cluster A is:
- **R1 (Package Format)** — the registry must understand the manifest.json schema

This is a clean contract boundary (a JSON schema). Once R1 is defined and frozen, Cluster B can be built independently.

There are ZERO dependencies from Cluster A to Cluster B. Local plugin install works without any registry.
