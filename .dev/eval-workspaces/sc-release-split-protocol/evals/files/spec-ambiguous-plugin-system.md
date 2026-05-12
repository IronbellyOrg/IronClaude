---
title: "v5.0 — Plugin System Architecture"
version: "5.0.0"
status: draft
date: 2026-03-18
complexity_class: HIGH
domain_distribution:
  backend: 40
  frontend: 30
  devops: 20
  security: 10
estimated_scope: 3000-4000 lines production code
priority: P1
---

# v5.0 Release Spec: Plugin System Architecture

## 1. Executive Summary

SuperClaude currently distributes extensions as markdown skill files copied into `~/.claude/skills/`. This works for simple behavioral instructions but cannot support:
- Executable code (TypeScript/Python plugins that run at build time or runtime)
- Dependency management (plugins that need npm packages or Python libraries)
- Versioning and updates (no mechanism to check for or apply updates)
- Marketplace discovery (users must manually find and install skills)

This release implements a full plugin system: a plugin registry, installation/update CLI, sandboxed execution environment, and a marketplace web UI.

## 2. Requirements

### R1: Plugin Package Format (P0)
Define the `.claude-plugin` package format.
- Must be a zip archive with manifest.json at root
- manifest.json schema: name, version, description, author, entrypoint, dependencies, permissions
- Support for multiple entrypoint types: `skill` (markdown), `hook` (TypeScript), `transform` (Python)
- Content-addressable storage: packages identified by SHA-256 hash
- Signature verification: packages must be signed with author's GPG key or registry-issued certificate

### R2: Plugin Registry (P0)
Server-side registry for publishing and discovering plugins.
- RESTful API: publish, search, download, version listing
- Scoped namespaces: `@org/plugin-name` format
- Semantic versioning with dependency resolution
- Rate limiting and abuse prevention
- Storage backend: S3-compatible object store for packages, PostgreSQL for metadata

### R3: CLI Plugin Manager (P0)
Extend the `superclaude` CLI with plugin management commands.
- `superclaude plugin install <name>[@version]` — download, verify, install
- `superclaude plugin update [name]` — check and apply updates
- `superclaude plugin remove <name>` — uninstall and cleanup
- `superclaude plugin list` — show installed plugins with versions
- `superclaude plugin publish` — package and upload to registry
- Lockfile generation (`plugin-lock.json`) for reproducible installs
- Offline mode: install from local `.claude-plugin` files

### R4: Sandboxed Execution Environment (P0)
Plugins must execute in an isolated environment.
- TypeScript plugins: V8 isolate with limited API surface
- Python plugins: subprocess with restricted imports and filesystem access
- Permission model: plugins declare required permissions in manifest
- User must approve permissions on first install
- Resource limits: CPU time, memory, filesystem write quota
- Audit logging: all plugin actions recorded with identity

### R5: Plugin Lifecycle Hooks (P1)
Integration points where plugins can extend SuperClaude behavior.
- `pre-command`: runs before any `/sc:*` command executes
- `post-command`: runs after command completes (receives output)
- `on-error`: runs when a command fails
- `transform-output`: modifies command output before display
- `custom-command`: registers new `/sc:*` commands
- Hook ordering: plugins declare priority; conflicts resolved by install order

### R6: Marketplace Web UI (P1)
Web interface for browsing and installing plugins.
- Search with filtering by category, author, rating
- Plugin detail pages with README, screenshots, install stats
- One-click install (launches CLI via protocol handler)
- User ratings and reviews
- Featured/curated collections
- Author verification badges

### R7: Migration from Skills to Plugins (P1)
Convert existing skill packages to plugin format.
- `superclaude plugin migrate <skill-dir>` — auto-converts skill to plugin
- Backward compatibility: `.claude/skills/` still works, loaded as implicit plugins
- Deprecation timeline: skills format supported for 2 major versions
- Migration guide documentation

### R8: Plugin Development Kit (P2)
Tooling for plugin authors.
- `superclaude plugin init` — scaffold a new plugin project
- `superclaude plugin dev` — local development mode with hot reload
- `superclaude plugin test` — run plugin's test suite in sandbox
- TypeScript type definitions for hook APIs
- Python stub packages for sandbox API
- Example plugins: custom command, output transformer, MCP bridge

### R9: Plugin Analytics (P2)
Telemetry for plugin health and usage.
- Install/uninstall counts per plugin
- Error rates and crash reports (opt-in)
- Performance impact metrics (command latency with/without plugin)
- Author dashboard: usage stats, error reports, user feedback

### R10: Enterprise Plugin Policies (P2)
Organization-level plugin governance.
- Approved plugin allowlist per org
- Private registries for internal plugins
- Plugin audit trail for compliance
- Automatic security scanning of published plugins
- Policy enforcement: block unsigned or unreviewed plugins

## 3. Architecture

### 3.1 Component Overview

```
┌──────────────────────────────────────────────────────┐
│                  Marketplace Web UI                    │
└──────────────┬───────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────┐
│              Plugin Registry (Server)                  │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐ │
│  │ API      │  │ Storage  │  │ Security Scanner   │ │
│  │ Server   │  │ (S3+PG)  │  │ (async pipeline)   │ │
│  └──────────┘  └──────────┘  └────────────────────┘ │
└──────────────────────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────┐
│              CLI Plugin Manager                        │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐ │
│  │ Install  │  │ Lockfile │  │ Signature Verify   │ │
│  │ Engine   │  │ Manager  │  │                    │ │
│  └──────────┘  └──────────┘  └────────────────────┘ │
└──────────────────────────────────────────────────────┘
               │
┌──────────────▼───────────────────────────────────────┐
│              Sandboxed Runtime                         │
│  ┌──────────┐  ┌──────────┐  ┌────────────────────┐ │
│  │ V8       │  │ Python   │  │ Permission         │ │
│  │ Isolate  │  │ Sandbox  │  │ Manager            │ │
│  └──────────┘  └──────────┘  └────────────────────┘ │
└──────────────────────────────────────────────────────┘
```

### 3.2 Data Flow

1. Author develops plugin locally with PDK
2. Author publishes to registry via CLI
3. Registry scans, validates, stores
4. User discovers via marketplace or direct link
5. CLI downloads, verifies signature, installs
6. Runtime loads plugin in sandbox, enforces permissions
7. Plugin hooks execute at lifecycle points

## 4. Dependencies

- Node.js >= 18 (V8 isolate for TypeScript plugins)
- Python >= 3.10 (subprocess sandbox)
- PostgreSQL >= 15 (registry metadata)
- S3-compatible storage (plugin packages)
- Web framework (marketplace UI — React + Next.js)

## 5. Testing Strategy

- Unit tests for package format parsing, signature verification
- Integration tests for install/update/remove lifecycle
- Sandbox escape testing (security audit)
- Load testing for registry under high download volume
- E2E: publish → discover → install → execute → update → remove

## 6. Rollout Plan

1. Alpha: Plugin format + CLI install from local files (internal team)
2. Beta: Registry + marketplace (invited authors)
3. GA: Public marketplace with migration tooling
4. Post-GA: Enterprise features, analytics

## 7. Success Criteria

- Existing skills can be migrated to plugin format with `plugin migrate`
- Plugin install-to-working takes < 30 seconds
- Sandbox prevents filesystem access outside declared scope
- Registry handles 1000 concurrent downloads
- Migration guide enables authors to self-serve conversion
