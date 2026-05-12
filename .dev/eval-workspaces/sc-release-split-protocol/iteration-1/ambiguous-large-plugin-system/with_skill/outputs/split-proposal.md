# Split Proposal — v5.0 Plugin System Architecture

## Discovery Analysis

### Spec Overview

v5.0 defines a full plugin system with 10 requirements spanning package format definition, server-side registry, CLI management, sandboxed execution, lifecycle hooks, marketplace web UI, migration tooling, a plugin development kit, analytics, and enterprise policies. Estimated scope is 3000-4000 lines of production code across backend (40%), frontend (30%), devops (20%), and security (10%).

### Dependency Chain Analysis

The requirements form a clear dependency graph:

**Foundation Layer** (no upstream dependencies):
- **R1: Plugin Package Format** — Everything depends on this. Defines the `.claude-plugin` format, manifest schema, content-addressable storage, signature verification. Zero value without consumers, but zero consumers work without it.

**Core Runtime Layer** (depends on R1):
- **R3: CLI Plugin Manager** — Depends on R1 for format parsing. Can operate in offline mode (install from local files) without R2. This is the primary user-facing interface.
- **R4: Sandboxed Execution** — Depends on R1 for permission model (permissions declared in manifest). Required for any plugin to actually run.

**Distribution Layer** (depends on R1, R3):
- **R2: Plugin Registry** — Depends on R1 for package format. Provides the server-side publishing/discovery infrastructure. R3 can function without it (offline mode) but it enables the full install workflow.
- **R5: Lifecycle Hooks** — Depends on R4 for sandbox execution. Defines the integration points (pre-command, post-command, etc.). Bridges the runtime to SuperClaude's command system.

**Application Layer** (depends on foundation + distribution):
- **R6: Marketplace Web UI** — Depends on R2 (registry API). Pure frontend; the rest of the system works without it.
- **R7: Migration** — Depends on R1 (target format). Enables existing skill authors to convert. Could ship with R1+R3.
- **R8: Plugin Development Kit** — Depends on R1, R4, R5. Tooling for authors — requires the runtime to be stable.
- **R9: Analytics** — Depends on R2 for telemetry. Post-GA concern.
- **R10: Enterprise Policies** — Depends on R2 for registry governance. Post-GA concern.

### Discovery Questions

**1. Are there components that deliver standalone value and can be validated through real-world use before the rest ships?**

Yes. R1 (Package Format) + R3 (CLI Manager, offline mode) + R4 (Sandbox) + R7 (Migration) form a coherent local-first plugin system. Users could:
- Define plugins in the `.claude-plugin` format
- Install from local files (`superclaude plugin install ./my-plugin.claude-plugin`)
- Execute plugins in the sandbox with permission enforcement
- Migrate existing skills to the plugin format

This is independently valuable because it validates the package format design, permission model, and sandbox security before building the distribution infrastructure.

**2. What are the dependency chains? Which items are prerequisites for others?**

See dependency chain above. The critical path is: R1 → R3/R4 → R5 → R8. The distribution path is: R1 → R2 → R6/R9/R10. These two paths converge at R3 (which optionally uses R2) and R8 (which needs the full runtime).

**3. What is the cost of splitting?**

- Two release cycles, two test passes, two deployment windows
- R3 must be designed with the registry interface in mind even though R2 ships later — risk of rework if the install engine's registry integration is poorly abstracted
- Users get a plugin system that only works with local files first — could be perceived as incomplete
- Context switching cost for the team between releases

**4. What is the cost of NOT splitting?**

- 3000-4000 lines shipped as a single monolith — harder to isolate failures
- No early feedback on the package format or sandbox design, which are the riskiest components
- If the manifest schema has a fundamental flaw, it's discovered after the entire registry, marketplace, and PDK have been built on top of it
- Big-bang risk: registry + marketplace + sandbox all go live simultaneously

**5. Is there a natural foundation-vs-application boundary?**

Yes. There is a clear **local runtime vs. distribution infrastructure** seam:

- **Foundation (local)**: Package format, CLI (offline), sandbox, lifecycle hooks, migration
- **Application (distributed)**: Registry, marketplace, PDK, analytics, enterprise

The foundation can be validated through real-world use (install local plugins, run them in sandbox, migrate skills) before the distribution layer is built.

**6. Could splitting INCREASE risk?**

Possible concerns:
- The CLI install engine designed for offline-only might need significant rework for registry integration. Mitigation: Design the install engine with a pluggable source interface from the start (local file source + future registry source).
- Users might adopt the local plugin format and then face breaking changes when the registry introduces constraints (e.g., namespace rules, signing requirements). Mitigation: Bake the signing and namespace rules into R1 from the start, even if R2 doesn't exist yet.
- Half a plugin system might confuse users about what SuperClaude's plugin story actually is. Mitigation: Clear documentation that Release 1 is the local-first foundation, with registry/marketplace coming in Release 2.

### Seam Identification

The natural seam is between **local plugin runtime** and **distribution infrastructure**:

| Release 1 (Foundation) | Release 2 (Distribution) |
|------------------------|-------------------------|
| R1: Package Format | R2: Plugin Registry |
| R3: CLI Manager (offline mode) | R3: CLI Manager (registry integration) |
| R4: Sandboxed Execution | R6: Marketplace Web UI |
| R5: Lifecycle Hooks | R8: Plugin Development Kit |
| R7: Migration | R9: Analytics |
| | R10: Enterprise Policies |

Note: R3 is split across releases — offline install/remove/list in R1, registry publish/update in R2. R5 (Lifecycle Hooks) is placed in R1 because it depends on R4 (sandbox) which is in R1, and it's needed for plugins to actually integrate with SuperClaude commands.

### Real-World Test Plan for Release 1

1. **Format validation**: Create 3 real plugins (one skill-type, one TypeScript hook, one Python transform) in `.claude-plugin` format. Verify manifest parsing, signature verification, content-addressable storage.
2. **Install lifecycle**: Use `superclaude plugin install ./plugin.claude-plugin` to install, verify file placement, then `superclaude plugin remove` to clean up. Verify lockfile generation.
3. **Sandbox security**: Install a plugin that attempts filesystem access outside declared scope. Verify it is blocked. Install a plugin that declares correct permissions. Verify it runs.
4. **Hook execution**: Install a plugin with a `pre-command` hook. Run a `/sc:*` command. Verify the hook fires at the correct lifecycle point.
5. **Migration**: Take an existing skill from `~/.claude/skills/` and run `superclaude plugin migrate`. Verify the output is a valid `.claude-plugin` that can be installed and executed.

### Risks of the Split

1. **R3 rework risk**: CLI install engine may need refactoring for registry source. Mitigation: Abstract the source interface in R1.
2. **Format lock-in**: Once R1 ships and users create plugins, the format is hard to change. Mitigation: Version the manifest schema; include format evolution strategy in R1.
3. **Incomplete perception**: Users see "plugin system" but can't discover or publish. Mitigation: Clear messaging; R1 is explicitly the "local plugin runtime."

### Release 1 Value Justification

Release 1 is NOT just "the easiest work." It delivers the riskiest and most architecturally significant components:
- **Package format design** — if this is wrong, everything built on it is wrong
- **Sandbox security model** — must be validated against real escape attempts
- **Permission model** — must be proven usable before building distribution

These are the items where early feedback has the highest leverage. Getting real users to create and install local plugins reveals format design flaws, sandbox gaps, and permission model friction before the distribution layer is built on top.

---

## Recommendation: SPLIT

**Confidence: 0.82**

The dependency graph reveals a clear foundation-vs-distribution seam. Release 1 delivers a complete local plugin runtime that can be validated through real-world use. Release 2 adds distribution infrastructure that builds on validated foundations. The split reduces big-bang risk for the most architecturally critical components (format, sandbox, permissions) while deferring infrastructure that is lower-risk but higher-effort (registry, marketplace).

The confidence is 0.82 rather than higher because:
- R3 spans both releases, creating a partial-delivery concern
- R5 (Lifecycle Hooks) placement in R1 is debatable — it could be deferred to R2 if R1 scope is too large
- The registry's constraints (namespaces, signing) must be anticipated in R1's format design, creating forward-dependency pressure
