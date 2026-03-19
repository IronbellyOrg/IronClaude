---
release: 1
parent-spec: /config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/evals/files/spec-ambiguous-plugin-system.md
split-proposal: /config/workspace/IronClaude/.claude/skills/sc-release-split-protocol-workspace/iteration-1/ambiguous-large-plugin-system/with_skill/outputs/split-proposal-final.md
scope: "Local plugin runtime — package format, CLI (offline), sandbox, basic hooks, migration"
status: draft
validation-gate: null
---

# Release 1 — Local Plugin Runtime

## Objective

Deliver a complete local plugin system that enables users to create, install, execute, and manage plugins on their local machine without requiring any server-side infrastructure. This validates the package format, sandbox security model, and permission system through real-world usage before distribution infrastructure is built.

## Scope

### Included

1. **R1: Plugin Package Format** (full scope)
   - `.claude-plugin` zip archive with manifest.json at root
   - Manifest schema: name, version, description, author, entrypoint, dependencies, permissions
   - Multiple entrypoint types: `skill` (markdown), `hook` (TypeScript), `transform` (Python)
   - Content-addressable storage: packages identified by SHA-256 hash
   - Signature verification: packages must be signed with author's GPG key or registry-issued certificate
   - Forward-compatibility: manifest includes reserved fields for registry metadata (categories, screenshots, author-org mapping) marked "reserved for v5.0-R2"
   - From: [original-spec] Section 2, R1

2. **R3: CLI Plugin Manager — Offline Operations** (partial scope)
   - `superclaude plugin install <path>` — install from local `.claude-plugin` files
   - `superclaude plugin remove <name>` — uninstall and cleanup
   - `superclaude plugin list` — show installed plugins with versions
   - Lockfile generation (`plugin-lock.json`) for reproducible installs
   - Offline mode: install from local `.claude-plugin` files
   - Install engine includes explicit registry source stubs (interface shaped by R2's known API design)
   - From: [original-spec] Section 2, R3 (offline subset)

3. **R4: Sandboxed Execution Environment** (full scope)
   - TypeScript plugins: V8 isolate with limited API surface
   - Python plugins: subprocess with restricted imports and filesystem access
   - Permission model: plugins declare required permissions in manifest
   - User must approve permissions on first install
   - Resource limits: CPU time, memory, filesystem write quota
   - Audit logging: all plugin actions recorded with identity
   - From: [original-spec] Section 2, R4

4. **R5: Plugin Lifecycle Hooks — Basic Hooks** (partial scope)
   - `pre-command`: runs before any `/sc:*` command executes
   - `post-command`: runs after command completes (receives output)
   - Hook ordering: plugins declare priority; conflicts resolved by install order
   - From: [original-spec] Section 2, R5 (pre-command and post-command only)

5. **R7: Migration from Skills to Plugins** (full scope)
   - `superclaude plugin migrate <skill-dir>` — auto-converts skill to plugin
   - Backward compatibility: `.claude/skills/` still works, loaded as implicit plugins
   - Deprecation timeline: skills format supported for 2 major versions
   - Migration guide documentation
   - From: [original-spec] Section 2, R7

### Excluded (assigned to Release 2)

1. **R2: Plugin Registry** — Server-side infrastructure. Deferred to: Release 2, full scope.
2. **R3: CLI Plugin Manager — Registry Operations** — `plugin install <name>[@version]` (from registry), `plugin update`, `plugin publish`. Deferred to: Release 2.
3. **R5: Lifecycle Hooks — Advanced Hooks** — `on-error`, `transform-output`, `custom-command`. Deferred to: Release 2 (ships with PDK for proper documentation).
4. **R6: Marketplace Web UI** — Deferred to: Release 2, full scope.
5. **R8: Plugin Development Kit** — Deferred to: Release 2, full scope.
6. **R9: Plugin Analytics** — Deferred to: Release 2, full scope.
7. **R10: Enterprise Plugin Policies** — Deferred to: Release 2, full scope.

## Dependencies

### Prerequisites
None — Release 1 has no dependencies on other releases.

### External Dependencies
- Node.js >= 18 (V8 isolate for TypeScript plugin sandbox)
- Python >= 3.10 (subprocess sandbox for Python plugins)
- GPG toolchain (signature verification)
- From: [original-spec] Section 4

## Real-World Validation Requirements

These scenarios must be executed with actual functionality in production-like conditions. No mocks, no simulated tests.

1. **Plugin creation end-to-end**: A real user (not the developer) creates a `.claude-plugin` from scratch using only the manifest documentation. Measures: time to working plugin, errors encountered, questions asked. Success: user creates a working plugin within 30 minutes.

2. **Install-execute-remove lifecycle**: Install 3 different plugins (skill-type, TypeScript hook, Python transform) from local files. Execute each in a real SuperClaude session. Remove each. Verify no artifacts remain. Success: all 3 plugins install, execute, and remove cleanly.

3. **Sandbox escape testing**: Install a deliberately malicious plugin that attempts: (a) filesystem access outside declared scope, (b) network access without permission, (c) excessive CPU consumption, (d) excessive memory allocation. Verify all 4 attempts are blocked. Success: zero escape vectors succeed.

4. **Permission model usability**: Present 5 users with plugins requesting various permission sets. Measure whether users understand what they're approving. Success: >= 4/5 users correctly identify what each permission grants.

5. **Hook execution verification**: Install a plugin with a `pre-command` hook. Run 10 different `/sc:*` commands. Verify the hook fires correctly each time with correct timing (before command execution). Install a `post-command` hook. Verify it receives actual command output.

6. **Migration fidelity**: Take 5 existing skills from `~/.claude/skills/` and run `superclaude plugin migrate` on each. Install the resulting plugins. Execute them in real SuperClaude sessions. Verify behavior matches the original skill. Success: all 5 migrated plugins behave identically to their skill originals.

7. **Lockfile reproducibility**: Install 3 plugins, generating `plugin-lock.json`. Delete all installed plugins. Reinstall from lockfile. Verify identical plugin state. Success: byte-identical plugin installations.

## Success Criteria

- All 7 real-world validation scenarios pass
- Existing skills can be migrated to plugin format with `plugin migrate`
- Plugin install-to-working takes < 30 seconds (from local file)
- Sandbox prevents filesystem access outside declared scope
- No breaking changes to the existing skill loading system (backward compatibility)

## Traceability

| Release 1 Item | Original Spec Source |
|----------------|---------------------|
| Plugin Package Format (full) | R1 — Section 2 |
| CLI Manager — offline ops | R3 — Section 2 (install from local, remove, list, lockfile, offline) |
| Sandboxed Execution (full) | R4 — Section 2 |
| Basic Lifecycle Hooks | R5 — Section 2 (pre-command, post-command, hook ordering) |
| Migration (full) | R7 — Section 2 |
| V8/Python runtime deps | Section 4 (Node.js >= 18, Python >= 3.10) |
