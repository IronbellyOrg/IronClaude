# Split Boundary Rationale

## Split Point

The boundary falls between the **local plugin runtime** (Release 1) and the **distribution infrastructure** (Release 2). Release 1 delivers everything needed to create, install (from local files), execute, and manage plugins on a single machine. Release 2 adds the server-side registry, marketplace, network-based operations, advanced tooling, and enterprise governance.

Two requirements span the boundary:
- **R3 (CLI Manager)**: Offline operations (install from file, remove, list, lockfile) in R1; registry operations (install from registry, update, publish) in R2.
- **R5 (Lifecycle Hooks)**: Basic hooks (pre-command, post-command, hook ordering) in R1; advanced hooks (on-error, transform-output, custom-command) in R2.

## Why This Boundary

1. **Dependency structure demands it.** The dependency graph has two distinct subgraphs that converge at R1 (package format). The local runtime subgraph (R1 → R3-offline, R4, R5-basic, R7) has no server-side dependencies. The distribution subgraph (R2 → R6, R9, R10; R2+R4+R5 → R8) requires infrastructure that doesn't exist yet. Building the foundation first is structurally sound.

2. **Risk concentration in the foundation.** The three highest-risk components are R1 (format design), R4 (sandbox security), and R5 (hook integration contract). These are all in Release 1. Format design errors compound through every downstream requirement. Sandbox vulnerabilities are security-critical. Hook API design affects every future plugin. Validating these before building the distribution layer prevents cascading design flaws.

3. **The spec's own rollout plan suggests it.** Section 6 of the original spec defines: "Alpha: Plugin format + CLI install from local files (internal team)." The proposed Release 1 is an expanded, validated version of this alpha — it aligns with the spec author's own phasing intuition.

4. **Real-world feedback on the foundation maximizes R2 quality.** User feedback on manifest schema usability, permission model clarity, and sandbox behavior directly informs R2 design decisions (registry validation rules, marketplace metadata display, PDK documentation).

## Release 1 Delivers

- **A complete local plugin system**: Users can create `.claude-plugin` packages, install them from local files, execute them in a secure sandbox, and manage their lifecycle (list, remove).
- **Migration path**: Existing skill authors can convert their work to plugin format, ensuring continuity.
- **Validated foundation**: The package format, sandbox security model, and permission system are proven through real-world use before anything is built on top of them.
- **Forward-compatible interfaces**: The manifest schema includes reserved fields for R2 registry metadata. The CLI install engine includes registry source stubs. These prevent rework when R2 ships.

## Release 2 Builds On

- **Registry + marketplace**: The distribution layer that transforms a local tool into an ecosystem. Depends on R1's validated format and signing for package management.
- **CLI registry integration**: Replaces R1's registry source stubs with real registry integration. Depends on R1's install engine architecture.
- **Advanced hooks + PDK**: The full plugin development experience with type definitions, examples, and advanced integration points. Depends on R1's basic hooks and sandbox being stable.
- **Analytics + enterprise**: Operational and governance features that layer on top of the registry. Depend on R2's registry infrastructure.

## Cross-Release Dependencies

| Release 2 Item | Depends On (Release 1) | Type | Risk if R1 Changes |
|----------------|----------------------|------|---------------------|
| R2: Registry package validation | R1: Package format + signing | Hard | Registry validation must be rebuilt if format changes |
| R3-R2: CLI registry source | R3-R1: Install engine stubs | Hard | Medium rework; stubs designed for this purpose |
| R5-R2: Advanced hooks | R5-R1: Basic hook system | Hard | Hook API contract must be stable; changes cascade to all hooks |
| R6: Marketplace metadata display | R1: Manifest schema (reserved fields) | Hard | Marketplace UI built against manifest; schema changes require UI rework |
| R8: PDK type definitions | R4: Sandbox API, R5-R1: Hook API | Hard | Type definitions must match runtime; changes require PDK update |
| R8: PDK migration reference | R7: Migration tooling | Soft | Documentation reference only; low risk |
| R9: Analytics hooks | R2: Registry API | Hard (R2-internal) | No direct R1 dependency |
| R10: Security scanner | R1: Package format | Hard | Scanner must parse package format; format changes require scanner update |

## Integration Points

1. **Package format contract**: R1 defines the `.claude-plugin` format and manifest schema. R2's registry validates against this schema. Any format evolution must be backward-compatible.

2. **CLI install engine interface**: R1's install engine has a source abstraction with local file source and registry source stubs. R2 implements the registry source. The interface contract (source → download → verify → install) is defined in R1.

3. **Hook API contract**: R1 defines the basic hook lifecycle (pre-command, post-command, priority ordering). R2 adds advanced hooks using the same API patterns. The hook registration and execution model must be stable.

4. **Sandbox API surface**: R1 defines what plugins can do inside the sandbox. R2's PDK documents this surface. Any sandbox API changes require PDK documentation updates.

5. **Manifest reserved fields**: R1's manifest includes reserved fields (categories, screenshots, author-org). R2 activates these fields. The schema must be designed in R1 with sufficient knowledge of R2's needs.

## Handoff Criteria

Before Release 2 planning begins:

1. All 7 Release 1 real-world validation scenarios have passed
2. No critical bugs remain in the package format, sandbox, or permission model
3. Manifest schema has been reviewed against R2's known requirements (registry validation, marketplace display, enterprise policies) — no breaking changes anticipated
4. CLI install engine's registry source stubs have been reviewed by the R2 team — the interface is fit for purpose
5. Hook API contract has been documented and reviewed — basic hooks (pre/post-command) are stable
6. Migration tooling has been used by at least 3 external skill authors with no blocking issues

## Reversal Cost

If the split decision proves wrong, merging back into a single release requires:

- **Estimated effort**: 1-2 weeks of integration work
- **What's preserved**: All R1 work (format, sandbox, CLI, hooks, migration) is prerequisite work for R2 regardless. Zero wasted effort on functionality.
- **What's lost**: The release boundary itself — planning, testing, and documentation for two separate releases must be consolidated.
- **Risk**: Low. The merge is additive (add R2 scope to existing R1 codebase). No R1 work needs to be reverted.
