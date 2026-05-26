# External Skill & Agent Registry — Requirements Specification

**Source:** `/sc:brainstorm` session 2026-05-24
**Status:** Draft requirements — pending `/sc:design` for architecture and `/sc:workflow` for implementation planning
**Owner:** RyanW

---

## 1. User Goal

Incorporate curated skill/agent/command sets from external GitHub repositories
into IronClaude such that:

1. They activate **only on projects where they apply** (e.g. `samber/cc-skills-golang`
   on Go projects like TUIBBS; never on Python projects like IronClaude).
2. Project applicability is determined by **scanning the project itself**, not by
   user declaration (with optional user override).
3. External resources **stay current** with upstream changes, with safe rollback
   when upstream breaks the integration.
4. The mechanism is **generic**: adding a new source is a config edit, not new code.

Seed sources for v1:

- `samber/cc-skills-golang` — 42 Go-specific skills (cobra, viper, testify, grpc,
  samber-* libs, error-handling, concurrency, etc.).
- `davila7/claude-code-templates`-style project analyzer — port the
  framework-detection behavior, not the npm distribution model.

## 2. Confirmed Design Decisions (Locked in Brainstorm)

| # | Decision | Choice |
|---|----------|--------|
| D1 | Vendor model | Vendored namespace under `src/superclaude/external/<source>/` |
| D2 | Activation gate | Project-local `<project>/.claude/skills/` override (not `~/.claude/skills/`) |
| D3 | v1 scope | Generic registry, seeded with 2 sources |
| D4 | Update policy | Floating HEAD with last-known-good rollback |
| D5 | Detector signals | Marker files (`go.mod`, `package.json`, `pyproject.toml`, `Cargo.toml`, …) |
| D6 | Registry scope | Skills **+ agents + commands** (full breadth) |
| D7 | Rollback gate | Schema validation **+** smoke skill-load test |
| D8 | Selection grain | All-or-nothing per source |

## 3. Functional Requirements

### FR-1 — External Source Registry

- **FR-1.1** A YAML manifest at `src/superclaude/external/registry.yaml` declares
  every external source.
- **FR-1.2** Each registry entry MUST specify:
  - `source` — git URL
  - `kind` — `skills`, `agents`, `commands`, or any combination
  - `pin` — last-known-good commit SHA (updated by sync)
  - `match` — list of marker-file patterns that activate this source
  - `namespace` — prefix applied to externally-sourced commands to avoid `/sc:` collisions (per D6 + the `.claude/` SoT rules)
  - `paths` — sub-path(s) within upstream repo containing the skills/agents/commands
- **FR-1.3** Registry is the single source of truth for "what's available"; the
  vendored payload under `src/superclaude/external/<source>/` is the fetched
  artifact.

### FR-2 — Project Detection

- **FR-2.1** A `superclaude detect-project` CLI subcommand reports the detected
  project type(s) for the current working directory.
- **FR-2.2** Detection uses marker files only (D5):
  - `go.mod` → Go
  - `package.json` → Node/JS-TS (with `tsconfig.json` upgrading to TypeScript)
  - `pyproject.toml` / `setup.py` → Python
  - `Cargo.toml` → Rust
  - (extensible via registry entries that declare their own marker patterns)
- **FR-2.3** Detection is deterministic and fast (<200 ms typical) — no AST
  parsing, no dependency-graph walking, no LLM calls.
- **FR-2.4** A project MAY match multiple types (polyglot repos); all matching
  sources activate.
- **FR-2.5** Out of v1 scope (deferred): file-extension census, framework
  probes, user `.claude/project-profile.yaml` declarations.

### FR-3 — External Sync

- **FR-3.1** `superclaude external sync` fetches the floating HEAD of every
  registered source into `src/superclaude/external/<source>/`.
- **FR-3.2** Sync is **read-from-internet, write-to-vendor-tree** — no
  modification of `~/.claude/` or any target project's `.claude/`.
- **FR-3.3** After sync, the registry's `pin:` field is updated **only if** the
  rollback gate (FR-5) passes.
- **FR-3.4** Sync produces a structured report:
  - Sources fetched, their old/new SHAs
  - Files added/modified/removed per source
  - Rollback gate result per source
- **FR-3.5** Sync MUST NOT touch sources whose upstream HEAD == current pin.

### FR-4 — Per-Project Install

- **FR-4.1** `superclaude external install` (run inside a target project) is the
  per-project activation command:
  1. Run project detection (FR-2)
  2. Resolve matching sources from registry
  3. Copy their skills/agents/commands to `<project>/.claude/skills/`,
     `<project>/.claude/agents/`, `<project>/.claude/commands/<namespace>/`
  4. Write `<project>/.claude/external.lock` recording: source, pinned SHA,
     install timestamp, matched markers
- **FR-4.2** Install MUST NOT touch `~/.claude/skills/` — global skills
  remain IronClaude-internal only.
- **FR-4.3** Re-running install is idempotent: identical lock → no file writes.
  Lock-file SHA drift triggers refresh.
- **FR-4.4** `superclaude external uninstall` removes all externally-installed
  files from the current project's `.claude/` tree, leaving internal IronClaude
  components untouched.
- **FR-4.5** External commands installed to `<project>/.claude/commands/<namespace>/`
  MUST use the namespace prefix declared in registry (`ext-golang:` etc.) so they
  cannot collide with `/sc:` namespace.

### FR-5 — Last-Known-Good Rollback Gate (D7)

- **FR-5.1** Before promoting a new upstream SHA to `pin:`, run:
  - **Schema validation**: every `SKILL.md` / agent `.md` / command `.md`
    parses, has required frontmatter fields (`name`, `description`), no
    malformed YAML.
  - **Smoke load test**: spawn a sandboxed Claude Code-equivalent skill loader
    that enumerates and parses every new skill without error.
- **FR-5.2** Gate failure → revert `src/superclaude/external/<source>/` to last
  known good SHA, leave `pin:` unchanged, surface failure in sync report.
- **FR-5.3** Gate failure on one source MUST NOT block other sources from
  promoting.
- **FR-5.4** Per-source allow-override: `--force <source>` bypasses the gate for
  that source only, with explicit warning logged.

### FR-6 — Source Vendoring & SoT Discipline

- **FR-6.1** Vendored payload lives at `src/superclaude/external/<source-slug>/`
  and IS committed to IronClaude's git history.
- **FR-6.2** Each commit that bumps `pin:` SHOULD include the corresponding
  vendor-tree changes in the same commit ("registry bump + payload" is one
  atomic unit).
- **FR-6.3** `make verify-sync` MUST cover `src/superclaude/external/` ↔ any
  IronClaude-local `.claude/` mirror (note: IronClaude itself is a Python
  project, so most external sources will NOT install here; verify-sync just
  ensures nothing leaked).

### FR-7 — Update Visibility

- **FR-7.1** `superclaude external status` lists every registered source with:
  current pin, upstream HEAD (if reachable), commits-behind count, last sync
  timestamp, last-known-good gate result.
- **FR-7.2** Optional: SessionStart hook displays a one-line advisory when any
  source is >N commits behind upstream (configurable, default off).

## 4. Non-Functional Requirements

| ID | Requirement |
|----|-------------|
| NFR-1 | `superclaude detect-project` returns in <200 ms on TUIBBS-sized repos |
| NFR-2 | `superclaude external sync` produces no permanent state changes on rollback-gate failure (atomic) |
| NFR-3 | `superclaude external install` is idempotent — re-running with identical lock is a no-op |
| NFR-4 | Per-project install MUST NOT write outside `<project>/.claude/`; never touches `~/.claude/` |
| NFR-5 | Sync MUST work offline if no source needs updating (uses cached vendor tree) |
| NFR-6 | External skill payload is auditable via standard git diff (consequence of D1 + FR-6) |
| NFR-7 | No execution of upstream code at sync time — only file copy + YAML parse |
| NFR-8 | Sync respects HTTP proxy env vars; no hardcoded transport |
| NFR-9 | Adding a new source requires editing only `registry.yaml` + running sync — no Python changes |

## 5. User Stories / Acceptance Criteria

### US-1 — Go developer in TUIBBS gets Go skills automatically

> As a developer working in TUIBBS (Go), when I run `superclaude external install`
> in the project root, the 42 samber/cc-skills-golang skills appear in
> `<TUIBBS>/.claude/skills/` and become available to Claude Code, while no Go
> skills appear in any non-Go project on the same machine.

**Acceptance:**

- Detector identifies TUIBBS as Go via `go.mod`.
- Registry's `samber/cc-skills-golang` entry has `match: [go.mod]`.
- Post-install, `<TUIBBS>/.claude/skills/golang-*/` exists; `<TUIBBS>/.claude/external.lock` records the pinned SHA.
- Running the same command in IronClaude (Python) installs zero Go skills.

### US-2 — Upstream pushes a breaking SKILL.md

> As IronClaude maintainer, when I run `superclaude external sync` and upstream
> `samber/cc-skills-golang` pushed a commit with a malformed `SKILL.md`, the
> sync rolls back that source, leaves the previous pin intact, and surfaces the
> failure clearly — without affecting other sources.

**Acceptance:**

- Schema validation flags the malformed SKILL.md.
- `src/superclaude/external/cc-skills-golang/` reverts to last-good SHA.
- `registry.yaml`'s `pin:` for that source is unchanged.
- Sync report shows the specific file + parse error.
- Other registered sources sync normally if they pass.

### US-3 — Generic source addition

> As IronClaude maintainer, when I want to add a third source (say,
> `someone/rust-skills`), I edit `registry.yaml` with the source URL, kind,
> match patterns, namespace, and an initial pin, then run sync. No Python
> changes needed.

**Acceptance:**

- Registry entry alone is sufficient.
- First sync fetches the source, runs the rollback gate, sets `pin:`.
- Cargo-marker projects pick up the new source on next `external install`.

### US-4 — Upstream silently changes everything

> As IronClaude maintainer, the rollback gate catches structural breakage
> (schema, load test) but not policy issues (upstream rewrote a skill's intent).
> I want visibility, not auto-prevention, for this case.

**Acceptance:**

- Sync report shows file-change counts per source.
- `superclaude external status` shows commits-behind and a diff summary on
  request.
- (Policy-level review remains a human responsibility; out of v1 scope to
  automate.)

### US-5 — Per-project uninstall

> As a developer, if I added external skills to my Go project and want to
> remove them, `superclaude external uninstall` cleans up `<project>/.claude/`
> without affecting IronClaude's internal skills.

**Acceptance:**

- Only files recorded in `<project>/.claude/external.lock` are removed.
- IronClaude-internal `.claude/skills/` content (if any) is untouched.
- Lock file is removed after successful uninstall.

## 6. Open Questions (For `/sc:design` Phase)

| ID | Question |
|----|----------|
| OQ-1 | Lock-file format: JSON vs YAML? Schema for forward-compat? |
| OQ-2 | Where exactly does the smoke-load test run — subprocess `claude --check-skills`, or in-process loader? |
| OQ-3 | Should `superclaude external install` register itself as a SessionStart hook so it auto-runs on first session per project, or is it always explicit? |
| OQ-4 | Namespace prefix scheme for external commands: `ext-golang:cobra-init` vs `golang:cobra-init` vs `samber:cobra-init`? |
| OQ-5 | Trust boundary for upstream scripts (SKILL.md `scripts/` subdir often contains executable code) — do we sandbox, allowlist, or just document the risk? |
| OQ-6 | Floating HEAD against which branch? Default branch only, or configurable per source? |
| OQ-7 | Handling of binary assets in upstream skills (icons, fixtures) — copy verbatim, or skip non-text by default? |
| OQ-8 | If two sources install skills with the same name (e.g. both define `golang-testing`), how is collision resolved? Source-priority order in registry? |
| OQ-9 | Does the per-project install need to migrate gracefully when a source is dropped from the registry — auto-uninstall, warn, or leave orphans? |
| OQ-10 | Should `superclaude detect-project` be exposed as a library function (for use by `/sc:recommend`, `/sc:brainstorm` Phase 0, etc.) in addition to a CLI subcommand? |
| OQ-11 | CI integration: should there be a periodic GitHub Actions job that runs `superclaude external sync` and opens PRs on pin bumps? (Hybrid of D4 with manual review.) |
| OQ-12 | Per-source allow-list of file kinds: do we only sync `*.md` + `*.yaml`, or also `scripts/`? Trust posture leak. |

## 7. Out of Scope for v1

- **NPM-style runtime distribution** (no `npx superclaude external@latest`).
- **Framework-tier sub-source profiles** (e.g. only Cobra+Viper for Go-CLI). D8
  locked all-or-nothing per source.
- **Per-skill activation rules** within a source.
- **GPG/sigstore signature verification** of upstream commits.
- **External MCP server registration**. Out of scope; MCP servers are managed
  by `superclaude mcp`.
- **External hook registration**. Hooks have privileged execution and project-
  local hook installation needs a separate trust model — defer.

## 8. Next-Step Handoff

This requirements spec is complete. The next sensible commands are:

```text
/sc:design "external skill registry — architect the CLI subcommands, registry.yaml schema, vendor layout, rollback gate, and project-local install flow per .dev/eval-proposals/external-skill-registry-REQUIREMENTS.md"
```

or, if you want to skip directly to a roadmap:

```text
/sc:roadmap .dev/eval-proposals/external-skill-registry-REQUIREMENTS.md
```

For implementation planning after architecture is settled:

```text
/sc:workflow .dev/eval-proposals/external-skill-registry-REQUIREMENTS.md
```
