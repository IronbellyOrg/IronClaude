---
title: "TDD Artifact Containment — Anchor /sc:tdd Outputs to Release Folders"
version: "1.0.0"
status: draft
feature_id: FR-TDD-CONTAINMENT
parent_feature: null
spec_type: refactoring
complexity_score: 0.45
complexity_class: MEDIUM
target_release: v4.3.0
authors: [user, claude]
created: 2026_05_14
quality_scores:
  clarity: 9.0
  completeness: 9.0
  testability: 9.5
  consistency: 9.0
  overall: 9.1
---

## 1. Problem Statement

The `/sc:tdd` command and `tdd` skill currently write all persistent artifacts (MDTM task file, research notes, PRD extraction, codebase research files, web research files, synthesis files, gap logs, analyst reports, QA reports, qualitative QA review, and the final TDD document) to two flat locations outside the per-release directory tree:

1. **Task tree:** `.dev/tasks/to-do/TASK-TDD-YYYYMMDD-HHMMSS/...` for ~12-35 in-progress files per run.
2. **Docs tree:** `docs/[domain]/TDD_<COMPONENT-NAME>.md` for the final deliverable.

This violates the project-wide discipline that "all development artifacts belong in `.dev/releases/$pathToRelease/`" — the same release folder that holds the release's spec, roadmap, and tasklists. The current layout has four consequences:

- **Discoverability gap:** A reader looking at `.dev/releases/current/<name>/` sees the spec and roadmap but no TDD or research; the TDD is invisible from the release index.
- **Concurrent-developer hazard:** Two developers working on different releases share a single flat `.dev/tasks/to-do/` namespace. Same-minute timestamps collide and unrelated work pollutes one another's task list.
- **Lifecycle fragmentation:** Moving a release between `backlog/`, `current/`, and `complete/` does not move its TDD artifacts. The audit trail is severed.
- **Architectural drift signal:** The skill predates the `.dev/releases/` discipline, and every new TDD reinforces the legacy convention.

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| 28 references to `.dev/tasks/to-do/` across the skill | `tdd-artifact-index.md` Section A | Every TDD run writes there by default |
| 13 references to `docs/...` paths (mostly final-TDD examples and defaults) | `tdd-artifact-index.md` Section B | Deliverable lands outside release folder |
| 14 distinct artifact creation sites currently outside release folder | `tdd-artifact-index.md` Section C | 12-35 files per Standard-tier run misplaced |
| `.dev/README.md` rule: "Release planning / roadmaps / tasklists → `.dev/releases/current/<release-name>/`" | `.dev/README.md` line 36 | Project discipline already established for sibling artifacts |
| TASK_ID format `TASK-TDD-YYYYMMDD-HHMMSS` is timestamp-collision-prone at one-second granularity | `SKILL.md:87` | Two same-second runs would clash |

### 1.2 Scope Boundary

**In scope:**
- Re-anchor every artifact path defined in the `tdd` skill and `/sc:tdd` command from `.dev/tasks/to-do/` / `docs/` to `.dev/releases/<bucket>/<release-name>/`.
- Introduce a 4-step release-resolution algorithm (explicit flag > cwd > PRD path > synthesized fallback).
- Introduce new variables (`RELEASE_DIR`, `COMPONENT_SLUG`) without breaking existing variables (`TASK_ID`, `TASK_DIR`).
- Add `--release` (`-R`) flag to the command surface.
- Update all command examples, artifact tables, and builder-template hand-offs.
- Backwards-compatible resume from legacy `.dev/tasks/to-do/` paths.

**Out of scope:**
- Migrating existing legacy task folders into release folders (separate cleanup pass, future release).
- Modifying the TDD template (`src/superclaude/examples/tdd_template.md`).
- Modifying the `rf-task-builder`, `rf-analyst`, `rf-qa`, `rf-qa-qualitative`, `rf-assembler` agent definitions (they accept paths via prompt embedding — only the BUILD_REQUEST template changes).
- Changing the `prd` skill or `roadmap` skill (separate concern).
- A hook-level enforcement layer (rely on skill-level discipline for this release; consider hooks later if drift recurs).

## 2. Solution Overview

**Primary actor:** developer authoring a TDD interactively. **Secondary actors:** the PM-agent (`/sc:pm`) invoking `/sc:tdd` on behalf of a release-bound task, and CI replay/audit invocations that must complete without user interaction. The resolution algorithm and conflict-handling paths below explicitly account for non-TTY invocation contexts.

Re-anchor every artifact path in the `tdd` skill and `/sc:tdd` command to a per-release directory tree rooted at `.dev/releases/<bucket>/<release-name>/`. Introduce a release-resolution algorithm that picks the release directory in priority order: explicit `--release` flag, then the deepest `.dev/releases/<bucket>/<name>/` ancestor of cwd, then the deepest such ancestor of `--from-prd`, then a synthesized backlog fallback. Redefine `TASK_DIR` to be `${RELEASE_DIR}/tdd/${COMPONENT_SLUG}/${TASK_ID}/` so all 11 downstream artifact paths self-correct without further edits. Move the final TDD default from `docs/[domain]/TDD_<COMPONENT-NAME>.md` to `${RELEASE_DIR}/TDD_<COMPONENT-NAME>.md`. Update one builder-template line (the assembler final-path hand-off) and update the command examples. Add backwards-compatible resume that honors legacy `.dev/tasks/to-do/` paths but never writes there for new runs.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Where does TASK_DIR live? | `${RELEASE_DIR}/tdd/${COMPONENT_SLUG}/${TASK_ID}/` | (a) `${RELEASE_DIR}/${TASK_ID}/` flat, (b) `${RELEASE_DIR}/tdd/${TASK_ID}/` no slug | Slug-scoped layout supports multiple components per release as siblings, and supports re-runs of same component as siblings under one folder. Discoverable. |
| Where does the final TDD live? | `${RELEASE_DIR}/TDD_<COMPONENT-NAME>.md` (sibling to spec.md/roadmap.md) | `${RELEASE_DIR}/tdd/<slug>/TDD.md` (nested) | Flat siblings make the release index human-readable in one ls. Multiple TDDs per release distinguished by component name. |
| How is release directory resolved? | 4-step priority: flag > cwd > PRD > synthesize | (a) Always require flag, (b) Always synthesize, (c) Prompt | Flag for power users, auto-detect for ergonomic flow, synthesize so the invariant "every TDD lives in a release" is always true. |
| Should hooks enforce the rule? | No (skill-level only for this release) | Add PreToolUse hook rejecting writes to `.dev/tasks/to-do/TDD-*` | Defer — start with skill-level discipline; add hook only if drift recurs. Avoids over-engineering for a brand-new convention. |
| Backwards compatibility surface | Resume-only (read legacy paths, never write them) | Auto-migrate legacy folders | Migration is a separate cleanup operation. Read-only compat keeps this release small and reversible. |
| Same-second collision handling | Append 4-char random suffix `-<rand4>` to TASK_ID | Use millisecond precision, use PID, use sequence number | Random suffix is filesystem-agnostic, requires no shared state, statistically safe at expected concurrency (<10 same-second runs). |
| `--release` first-time UX | Require pre-existing release dir EXCEPT for synthesized fallback (step 4 of resolution) | Default to "create if not exists" everywhere; always require explicit pre-creation | Synthesized fallback covers the new-component flow; explicit `--release` should fail loudly if the named release doesn't exist (typo protection). |
| Discovery scan roots in Step A.3 | Search both `.dev/releases/**/PRD_*.md` AND `.dev/releases/**/spec.md`, in addition to `docs/` | Search only one of the two | Both PRDs and release specs are valid input docs for a TDD; scanning both maximizes context capture without ambiguity. |
| Slug derivation for COMPONENT_SLUG | Algorithmic kebab-case: lowercase, replace non-alphanumeric runs with `-`, strip leading/trailing `-`, collapse repeated `-`; empty result errors | Loose "kebab-case identifier" rule | Deterministic derivation makes tests reproducible and prevents per-platform drift. (Was OI-4.) |
| Existing `docs/` TDDs on update | Updates to legacy TDDs stay in `docs/` and add a Document History note; new TDDs go to release folders | Auto-redirect updates to release folders | Avoids surprise relocations and lets legacy TDDs migrate organically. |
| Synthesized release directory marker | Synthesized fallback writes a `README.md` flagging the dir as "synthesized-by-tdd, no spec/roadmap yet" | Leave the dir unmarked; co-locate under a separate `_orphan-tdds/` namespace | Marker preserves a single release namespace AND distinguishes synthesized from real dirs in `ls`; the dir is eligible for later `/sc:roadmap` or `/sc:spec` promotion. |
| Builder embedding of resolved paths | `rf-task-builder` resolves all path variables to **repo-relative literal paths** at task-file-write time | (a) Embed `${RELEASE_DIR}` placeholders, (b) embed absolute paths | Repo-relative literals preserve worktree portability AND make B2 items self-contained without late-bound variables. |

### 2.2 Workflow / Data Flow

```
/sc:tdd <component> [--release <bucket>/<name>] [--from-prd <path>] [--focus ...] [--output ...]
        |
        v
+---------------------------------+
| Skill: Stage A.1b               |
| Resolve RELEASE_DIR             |
|   1. explicit --release         |
|   2. ancestor of cwd            |
|   3. ancestor of --from-prd     |
|   4. synthesize backlog/tdd-... |
+---------------------------------+
        |
        v
+---------------------------------+        +-----------------------------+
| RELEASE_DIR + COMPONENT_SLUG    |        | .dev/releases/<bucket>/     |
| TASK_DIR = RELEASE_DIR/tdd/     | -----> |   <release-name>/           |
|            COMPONENT_SLUG/      |        |   ├─ spec.md (existing)     |
|            TASK_ID/             |        |   ├─ roadmap.md (existing)  |
+---------------------------------+        |   ├─ TDD_<COMPONENT>.md (NEW final)
        |                                  |   └─ tdd/                   |
        v                                  |       └─ <slug>/            |
+---------------------------------+        |           └─ <TASK_ID>/     |
| Spawn rf-task-builder           |        |               ├─ research/  |
| Embed paths in B2 checklist     |        |               ├─ synthesis/ |
| items                           |        |               ├─ qa/        |
+---------------------------------+        |               └─ reviews/   |
        |                                  +-----------------------------+
        v
+---------------------------------+
| /task executes phases 1-7       |
| All writes anchored in TASK_DIR |
| Final TDD written to            |
| RELEASE_DIR/TDD_<COMPONENT>.md  |
+---------------------------------+
```

## 3. Functional Requirements

### FR-TDD-CONTAINMENT.1: Variable Contract

**Description:** Introduce `RELEASE_DIR` and `COMPONENT_SLUG` as first-class variables in `SKILL.md` and redefine `TASK_DIR` to nest under them.

**Acceptance Criteria:**
- [ ] `SKILL.md` defines `RELEASE_DIR`, `COMPONENT_SLUG`, `TASK_ID`, `TASK_DIR` in that order.
- [ ] `TASK_DIR = ${RELEASE_DIR}/tdd/${COMPONENT_SLUG}/${TASK_ID}/`.
- [ ] `RESEARCH`, `SYNTHESIS`, `QA`, `REVIEWS` remain `${TASK_DIR}<subdir>/` (unchanged expansion below TASK_DIR).
- [ ] `${RELEASE_DIR}` always points to a direct child of `.dev/releases/<bucket>/`, where the authoritative list of valid `<bucket>` values is defined in `.dev/README.md`. The skill MUST read `.dev/README.md` (or accept any direct subdirectory of `.dev/releases/`) rather than hard-coding `(backlog|current|complete)`.
- [ ] COMPONENT_SLUG derivation rule: lowercase the input, replace runs of non-alphanumeric characters with a single `-`, strip leading/trailing `-`, collapse repeated `-`. Result must match `^[a-z0-9]+(-[a-z0-9]+)*$`. An empty result (e.g., from input `"!!!"`) is an error.
- [ ] Two component names whose slugs differ only by case (e.g., `Auth` and `auth`) map to the same lowercase slug. A second run for the same slug under the same RELEASE_DIR is treated as a re-run (becomes a sibling `TASK-TDD-*` folder under `tdd/<slug>/`); the user receives a one-line stderr notice that the slug already exists.
- [ ] Release names `tdd` and `archive` are **discouraged** (they produce visually confusing paths like `current/tdd/tdd/` or shadow the per-release `archive/` convention) but NOT rejected; the skill emits a stderr advisory and proceeds.

**Dependencies:** None.

### FR-TDD-CONTAINMENT.2: Release Resolution Algorithm

**Description:** Implement the 4-step release-directory resolution algorithm in Stage A of the skill.

**Acceptance Criteria:**

*Step 1 — explicit `--release`:*
- [ ] An empty-or-whitespace `--release` value (e.g., `--release ""`) is treated as **not provided** and the algorithm falls through to Step 2.
- [ ] Value matching `<bucket>/<name>` form (exactly one `/`): the path `.dev/releases/<bucket>/<name>/` must exist; if not, error "release not found: <path>".
- [ ] Value matching `<name>` form (zero `/`): the skill scans `.dev/releases/*/` for a directory named `<name>`. Unique match → resolved; ambiguous (matches in 2+ buckets) → error "ambiguous release name, specify bucket/name"; not-found → error.
- [ ] Value containing 2+ `/` (e.g., `a/b/c`) → error "invalid release reference; expected `<bucket>/<name>` or `<name>`".

*Step 2 — cwd ancestor walk:*
- [ ] Matcher: longest path-prefix of `pwd` matching `.dev/releases/<bucket>/[^/]+/` where `<bucket>` is a direct child of `.dev/releases/`. The **deepest** (longest-prefix) match wins.
- [ ] When `pwd` is inside `<RELEASE_DIR>/tdd/<slug>/TASK-TDD-*/...`, the matcher returns `<RELEASE_DIR>`, NOT any subdirectory of it.

*Step 3 — PRD ancestor walk:*
- [ ] Same matcher rule as Step 2, applied to `--from-prd` path.

*Step 4 — synthesize fallback:*
- [ ] Resolves to `.dev/releases/backlog/tdd-${COMPONENT_SLUG}/`.
- [ ] If `.dev/releases/` parent does not exist: `mkdir -p` creates it. If `.dev/` itself is missing, error with a message pointing to project setup (greenfield repo case).
- [ ] If the target dir already exists AND contains a `spec.md` or `roadmap.md` (i.e., it is a real release that happens to share the synthesized name), append `-YYYYMMDD-HHMMSS` to the synthesized name and retry.
- [ ] If the target dir already exists AND was previously synthesized (contains a `README.md` whose first line begins with the sentinel `# Synthesized release — tdd skill`), the skill MERGES into it: both runs become siblings under the shared `tdd/` subtree. This makes Step 4 idempotent and race-safe.
- [ ] Synthesized dir creation writes a `README.md` whose content begins with the literal sentinel line `# Synthesized release — tdd skill` so future runs can recognize it.
- [ ] After mkdir, the user receives a single stderr notice: "Synthesized release at .dev/releases/backlog/tdd-<slug>/. Run /sc:spec or /sc:roadmap to promote it."

*Conflict handling:*
- [ ] When both Step 2 (cwd) and Step 3 (PRD) match and produce **different** RELEASE_DIRs, the skill detects the conflict:
  - When stdin is a TTY → prompts the user to choose which to use.
  - When stdin is NOT a TTY → exits with non-zero status, printing both candidates and instructing the user to pass `--release` explicitly. Never silently picks one.
- [ ] When Step 2 and Step 3 match and produce the **same** RELEASE_DIR, no conflict; resolution proceeds.

**Dependencies:** FR-TDD-CONTAINMENT.1.

### FR-TDD-CONTAINMENT.3: Final TDD Default Path

**Description:** The final TDD's default output path changes from `docs/[domain]/TDD_<COMPONENT-NAME>.md` to `${RELEASE_DIR}/TDD_<COMPONENT-NAME>.md`.

**Acceptance Criteria:**
- [ ] `SKILL.md` line 46 reflects new default.
- [ ] `SKILL.md` artifact table (line 107) reflects new default.
- [ ] `operational-guidance.md` artifact table (line 87) reflects new default.
- [ ] `build-request-template.md` line 120 (assembler hand-off) reflects new default.
- [ ] `--output <path>` override remains honored. Two additional acceptance criteria apply to overrides:
  - [ ] If the override path is **outside** RELEASE_DIR, the skill emits a single-line stderr warning (e.g., `WARN: --output path is outside RELEASE_DIR; final TDD will not be discoverable from the release index`) before proceeding. The run is NOT aborted.
  - [ ] The override path's **parent directory must already exist**. The skill does NOT create parent directories for override paths; if the parent is missing, error before any agent work begins.

**Dependencies:** FR-TDD-CONTAINMENT.1.

### FR-TDD-CONTAINMENT.4: Command Surface — `--release` Flag

**Description:** Add `--release` (short `-R`) flag to `/sc:tdd` command.

**Acceptance Criteria:**
- [ ] Options table in `commands/tdd.md` includes `--release` row.
- [ ] Flag grammar:
  - **Exactly one `/`** → parsed as `<bucket>/<name>`.
  - **Zero `/`** → parsed as `<name>` (cross-bucket auto-resolution, per FR-TDD-CONTAINMENT.2).
  - **Two or more `/`** → error with explanatory message.
  - **Empty or whitespace** → treated as not provided (per FR-TDD-CONTAINMENT.2 Step 1 AC).
- [ ] All 7 existing examples in `commands/tdd.md` updated to demonstrate `--release` and release-folder outputs.
- [ ] New "Release Resolution" subsection added.
- [ ] New "Backwards Compatibility" subsection added.

**Dependencies:** FR-TDD-CONTAINMENT.2.

### FR-TDD-CONTAINMENT.5: Builder Template Hand-off

**Description:** `BUILD_REQUEST` template propagates `RELEASE_DIR` and `COMPONENT_SLUG` to the `rf-task-builder` subagent.

**Acceptance Criteria:**
- [ ] `build-request-template.md` adds `RELEASE_DIR:` and `COMPONENT_SLUG:` fields in the header.
- [ ] Line 120 (final TDD path hand-off to `rf-assembler`) uses `${RELEASE_DIR}/TDD_${COMPONENT-NAME}.md`.
- [ ] Lines 133 and 143 (TASK FILE LOCATION) use `${TASK_DIR}` reference instead of literal `.dev/tasks/to-do/...`.
- [ ] **Variable resolution timing (binding contract):** The `rf-task-builder` subagent MUST resolve all path variables (`${RELEASE_DIR}`, `${COMPONENT_SLUG}`, `${TASK_ID}`, `${TASK_DIR}`, derived subdir paths) to **repo-relative literal paths** at the moment it writes the task file. Resolved paths are repo-relative (e.g., `.dev/releases/backlog/foo/tdd/bar/TASK-TDD-.../`), NOT absolute filesystem paths. Rationale: repo-relative literals preserve worktree portability while keeping every B2 item self-contained (no late-bound variable lookups required during /task execution).
- [ ] B2 items in the generated task file contain literal paths, NOT `${VAR}` placeholders. A grep for `\${RELEASE_DIR}` or `\${TASK_DIR}` in any generated task file returns zero hits.

**Dependencies:** FR-TDD-CONTAINMENT.1, FR-TDD-CONTAINMENT.3.

### FR-TDD-CONTAINMENT.6: Backwards-Compatible Resume

**Description:** Resume logic accepts legacy `.dev/tasks/to-do/` paths without migration.

**Acceptance Criteria:**
- [ ] `--resume <legacy-path>` continues to function unchanged.
- [ ] Resume path classification by prefix:
  - Path starting with `.dev/tasks/to-do/` → **legacy** resume.
  - Path matching `.dev/releases/.+/tdd/.+/TASK-TDD-` → **new** resume.
  - Any other path → error with explanatory message ("unrecognized resume path; expected `.dev/tasks/to-do/...` or `.dev/releases/.../tdd/...`").
- [ ] Implicit resume scan covers both `.dev/releases/**/tdd/<slug>/TASK-TDD-*/` (primary) and `.dev/tasks/to-do/TASK-TDD-*/` (legacy, with deprecation notice).
- [ ] When implicit-resume scan finds candidates in BOTH new and legacy trees for the same component, the new-tree task is selected; the legacy hit is logged at INFO level to stderr but not used.
- [ ] When resuming a legacy task, the skill never mid-flight migrates: the final TDD writes to wherever the **legacy task file's metadata or stage-A research notes** already designated (typically `docs/[domain]/TDD_<COMPONENT>.md`); the run notes the deprecation in the final TDD's Document History. No path rewriting occurs.
- [ ] When `--resume` is given alongside `--release`, the resume path's layout takes precedence; `--release` is ignored with a single-line stderr warning ("WARN: --release ignored because --resume specifies the layout").
- [ ] New runs (no resume) never write to `.dev/tasks/to-do/`.

**Dependencies:** FR-TDD-CONTAINMENT.2.

### FR-TDD-CONTAINMENT.7: Concurrent-Developer Safety

**Description:** Same-second collisions in `TASK_ID` are handled deterministically.

**Acceptance Criteria:**
- [ ] When creating `${TASK_DIR}`, if the directory already exists, append a 4-char random suffix to `TASK_ID` and retry.
- [ ] Two parallel runs on different releases never share a parent path.
- [ ] Two parallel runs on different components within the same release land in sibling `tdd/<slugA>/` and `tdd/<slugB>/` folders.

**Dependencies:** FR-TDD-CONTAINMENT.1.

### FR-TDD-CONTAINMENT.8: Discovery Scan Includes Release Tree

**Description:** Discovery logic in Step A.3 (scanning for existing stubs/PRDs) scans `.dev/releases/**/` in addition to `docs/`.

**Acceptance Criteria:**
- [ ] `SKILL.md` line 196 lists both `docs/` and `.dev/releases/**/` as scan roots.
- [ ] PRD discovery and `*_TDD.md` stub detection work from either location.

**Dependencies:** FR-TDD-CONTAINMENT.1.

### FR-TDD-CONTAINMENT.9: Archive Destination is Release-Local

**Description:** `validation-checklists.md` archive instruction relocates from `docs/archive/` to `${RELEASE_DIR}/archive/`.

**Acceptance Criteria:**
- [ ] `validation-checklists.md` line 76 updated.

**Dependencies:** FR-TDD-CONTAINMENT.1.

### FR-TDD-CONTAINMENT.10: Session Management Text Sync

**Description:** Session-management prose in `operational-guidance.md` reflects new layout.

**Acceptance Criteria:**
- [ ] `operational-guidance.md` line 123 updated to reference release tree.
- [ ] Backwards-compat note for legacy paths retained.

**Dependencies:** FR-TDD-CONTAINMENT.6.

## 4. Architecture

### 4.1 New Files

| File | Purpose | Dependencies |
|------|---------|-------------|
| None — refactoring of existing skill text only. | — | — |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/commands/tdd.md` | 11 edits (D1.1-D1.11): add `--release` flag, update 7 examples, add Release Resolution and Backwards Compatibility subsections | Command-surface change for FR-4 |
| `src/superclaude/skills/tdd/SKILL.md` | 13 edits (D2.1-D2.13): variable block, artifact table, lines 29/46/83/107/112/153/157/196/230/383, insert new Step A.1b | Core skill rewiring for FR-1, FR-2, FR-3, FR-6, FR-7, FR-8 |
| `src/superclaude/skills/tdd/refs/build-request-template.md` | 11 edits (D3.1-D3.11): add RELEASE_DIR/COMPONENT_SLUG header fields, update line 120 (assembler hand-off), lines 133/143 (TASK FILE LOCATION) | Builder template for FR-5 |
| `src/superclaude/skills/tdd/refs/operational-guidance.md` | 4 edits (D4.1-D4.4): sync artifact table, update line 123 session-management text | Reference sync for FR-3, FR-10 |
| `src/superclaude/skills/tdd/refs/validation-checklists.md` | 1 edit (D5.1): archive destination | FR-9 |

### 4.3 Removed Files

None.

### 4.4 Module Dependency Graph

```
commands/tdd.md          (surface; documents flag)
       |
       v
skills/tdd/SKILL.md      (orchestrator; resolution algorithm; variable contract)
       |
       v
refs/build-request-template.md   (builder input; carries RELEASE_DIR/COMPONENT_SLUG/TASK_DIR)
       |
       v
rf-task-builder (subagent; reads template, emits task file with embedded paths)
       |
       v
generated task file      (B2 self-contained items with absolute paths embedded)
       |
       v
/task skill (F1 loop)    (executes; spawns subagents; subagents write to embedded paths)
       |
       +-> rf-assembler  (writes final TDD to ${RELEASE_DIR}/TDD_<COMPONENT>.md)
       +-> rf-analyst, rf-qa, rf-qa-qualitative (write reports to ${TASK_DIR}qa/)

refs/operational-guidance.md  (reference doc loaded by builder; defines artifact locations)
refs/validation-checklists.md (reference doc loaded by builder; defines archive path)
refs/synthesis-mapping.md     (unchanged)
refs/agent-prompts.md         (unchanged — uses [output-path] placeholders)
```

### 4.5 Data Models

The release directory tree after this change:

```
.dev/releases/<bucket>/<release-name>/
├── spec.md                          (from /sc:release-split, /sc:cli-portify, etc.)
├── roadmap.md                       (from /sc:roadmap)
├── tasklist*.md                     (from /sc:tasklist)
├── TDD_<COMPONENT-A>.md             ← NEW: final TDD for component A
├── TDD_<COMPONENT-B>.md             ← NEW: final TDD for component B (if multi-component release)
├── archive/                         ← NEW: superseded sources (was docs/archive/)
└── tdd/
    ├── <component-a-slug>/
    │   ├── TASK-TDD-20260514-120000/
    │   │   ├── TASK-TDD-20260514-120000.md   (MDTM task file)
    │   │   ├── research-notes.md             (scope discovery output)
    │   │   ├── gaps-and-questions.md         (interim gaps log)
    │   │   ├── research/
    │   │   │   ├── 00-prd-extraction.md
    │   │   │   ├── 01-architecture.md
    │   │   │   ├── 02-data-model.md
    │   │   │   ├── web-01-frameworks.md
    │   │   │   └── update-2026-06-01-api-changes.md
    │   │   ├── synthesis/
    │   │   │   ├── synth-01-overview.md
    │   │   │   └── synth-02-architecture.md
    │   │   ├── qa/
    │   │   │   ├── analyst-completeness-report.md
    │   │   │   ├── qa-research-gate-report.md
    │   │   │   ├── analyst-synthesis-review.md
    │   │   │   ├── qa-synthesis-gate-report.md
    │   │   │   ├── qa-report-validation.md
    │   │   │   └── qa-qualitative-review.md
    │   │   └── reviews/
    │   └── TASK-TDD-20260601-090000/         (re-run, sibling)
    └── <component-b-slug>/
        └── TASK-TDD-20260514-121500/
```

### 4.6 Implementation Order

```
1. Update SKILL.md variable block + artifact table (D2.1-D2.5, D2.13)   -- foundation
2. Add Step A.1b release resolution to SKILL.md (D2.9)                  -- depends on 1
3. Update SKILL.md discovery/resume references (D2.6-D2.8, D2.11, D2.12) -- depends on 1
4. Update build-request-template.md (D3.1-D3.11)                        -- depends on 1, 2 [parallel with 3]
5. Sync operational-guidance.md (D4.1-D4.4)                             -- depends on 1, 2 [parallel with 3, 4]
6. Update validation-checklists.md (D5.1)                               -- depends on 1 [parallel]
7. Update commands/tdd.md (D1.1-D1.11)                                  -- depends on 1, 2 [parallel with 3-6]
8. Run make sync-dev to propagate src/ to .claude/                      -- depends on 1-7
9. Run make verify-sync                                                 -- depends on 8
10. Execute test plan (Section 8)                                       -- depends on 9
```

## 5. Interface Contracts

### 5.1 CLI Surface

```
/sc:tdd <component> [options]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `<component>` | positional | required | Component name (becomes COMPONENT_SLUG kebab-cased) |
| `--release` / `-R` | string | auto-detect | Release directory: `<bucket>/<name>` or `<name>` (auto-resolved) |
| `--tier` / `-t` | enum | `standard` | `lightweight` / `standard` / `heavyweight` |
| `--from-prd` | path | none | PRD file path; also used as fallback for release auto-detection |
| `--prd` | path | none | Alias for `--from-prd` |
| `--focus` / `-f` | csv | all | Comma-separated focus directories/files |
| `--output` / `-o` | path | `${RELEASE_DIR}/TDD_<COMPONENT-NAME>.md` | Override final TDD destination |
| `--resume` / `-r` | path | none | Resume from MDTM task file (accepts legacy `.dev/tasks/to-do/` paths) |

### 5.2 Resolution Examples

Concrete (cwd, `--release`, `--from-prd`) → expected `RELEASE_DIR` and resolution branch. Examples assume `.dev/releases/backlog/foo/`, `.dev/releases/current/bar/`, and `.dev/releases/current/baz/` exist.

| # | cwd | `--release` | `--from-prd` | Expected RELEASE_DIR | Branch |
|---|-----|------------|--------------|----------------------|--------|
| RE-1 | repo root | `backlog/foo` | (none) | `.dev/releases/backlog/foo/` | Step 1 (explicit bucket/name) |
| RE-2 | repo root | `bar` | (none) | `.dev/releases/current/bar/` | Step 1 (name-only unique) |
| RE-3 | repo root | `foo` | (none) | (error: ambiguous if `foo` also exists in `current/`) | Step 1 (name-only ambiguous) |
| RE-4 | repo root | `""` | (none) | (falls through to Step 2; falls through to 4 if no PRD; synthesizes `.dev/releases/backlog/tdd-<slug>/`) | Step 4 (empty flag ignored) |
| RE-5 | `.dev/releases/current/bar/` | (none) | (none) | `.dev/releases/current/bar/` | Step 2 (cwd ancestor) |
| RE-6 | `.dev/releases/current/bar/tdd/auth/TASK-TDD-.../research/` | (none) | (none) | `.dev/releases/current/bar/` | Step 2 (deepest ancestor match) |
| RE-7 | repo root | (none) | `.dev/releases/backlog/foo/PRD.md` | `.dev/releases/backlog/foo/` | Step 3 (PRD ancestor) |
| RE-8 | `.dev/releases/current/bar/` | (none) | `.dev/releases/backlog/foo/PRD.md` | (conflict — prompts TTY, errors non-TTY) | Conflict handling |
| RE-9 | repo root | (none) | (none) | `.dev/releases/backlog/tdd-<slug>/` (synthesized) | Step 4 (synthesize) |
| RE-10 | repo root | `a/b/c` | (none) | (error: invalid grammar) | Step 1 (2+ slashes) |

### 5.3 Phase Contracts

None changed. Phase loading contract (`SKILL.md` lines 405-419) is unaffected by this refactor — refs files load at the same phases, just contain updated path strings.

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-1 | Backwards compatibility: legacy `.dev/tasks/to-do/` paths remain resumable | 100% of "well-formed" legacy paths resume, where well-formed is defined by the regex `^\.dev/tasks/to-do/TASK-TDD-\d{8}-\d{6}(-[a-f0-9]{4})?/(TASK-TDD-\d{8}-\d{6}(-[a-f0-9]{4})?\.md)?$` | Manual test T18, T19 |
| NFR-2 | Concurrent-developer safety: no path collisions across releases/components/timestamps | 0 collisions in T14, T15; suffix appended in T16 | Tests T14-T17 |
| NFR-3 | Discoverability: every release dir contains its TDD as a sibling of spec.md | `ls .dev/releases/<bucket>/<name>/` shows `TDD_*.md` for every TDD'd component | Manual test M3 (added to §8.3) |
| NFR-4 | Migration cost for in-flight work: zero | No legacy folders are moved by this release | Code inspection |
| NFR-5 | Sync invariant: `make verify-sync` passes after edits | `src/` and `.claude/` byte-equal for tdd skill + command | `make verify-sync` exit 0 |
| NFR-6 | Lifecycle integrity: `mv .dev/releases/current/<name>/ .dev/releases/complete/<name>/` brings all TDD artifacts | Filesystem move preserves audit trail | Manual test M4 (added to §8.3) |
| NFR-7 | Write-failure handling: on any filesystem write error inside RELEASE_DIR (permission denied, disk full, stale NFS), the skill halts with non-zero exit and prints the partial-write path. No implicit retry or silent fallback. | Skill halts on first write error; partial-write path printed; recovery requires user intervention. | Manual test M5 (added to §8.3); negative test in §8.1 (permission-denied case) |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Builder subagent ignores updated `${RELEASE_DIR}` and writes literal `docs/...` because old example was memorized | Low | High | Audit BUILD_REQUEST line 120 carefully; add explicit "REPLACES legacy `docs/[domain]/...` default" comment in builder template |
| Cwd-based detection picks the wrong release when user is inside a deeply nested release subdir | Low | Medium | Algorithm picks the **deepest** matching ancestor; document the rule in Release Resolution section |
| Synthesized backlog name (`tdd-<slug>`) collides with an actual release named `tdd-<slug>` | Very low | Low | Resolution algorithm checks for existence; if synthesized name already exists, append timestamp |
| Users with legacy `.dev/tasks/to-do/` muscle memory keep hitting `--resume` with old paths and never migrate | Medium | Low | Compat layer is intentional; deprecation notice in Document History tracks adoption; future cleanup task moves stragglers |
| Same-second collision suffix `-<rand4>` collides on its own at extreme concurrency | Negligible | Low | 16^4 = 65k namespace; retry on collision |
| `make verify-sync` breaks because edits land in `src/` but not `.claude/` (or vice versa) | Medium | Low | Workflow rule: every commit runs `make sync-dev && make verify-sync` |
| `rf-assembler` agent embeds final-TDD path in its output and the path becomes wrong | Low | Medium | T2 grep ensures no `docs/[domain]/` strings remain post-edit |
| `tdd/<slug>/TASK-TDD-*/` sibling folders accumulate without bound across re-runs over a release lifecycle | Medium | Low | Acknowledged; out of scope for this release. Future cleanup task should add a `--prune-completed` flag or scheduled archival. |
| Cross-platform path handling breaks on Windows or case-insensitive FS | Low | Medium | Slugs are always lowercase (FR-1); skill uses `pathlib` / forward-slash repo-relative paths. Documented; full Windows validation deferred. |

## 8. Test Plan

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_no_legacy_task_writes_in_skill_and_refs` | `tests/skills/test_tdd_paths.py` | grep `\.dev/tasks/to-do/` across SKILL.md AND refs/*.md returns hits only in explicitly-tagged backwards-compat / legacy-resume contexts |
| `test_no_legacy_docs_tdd_writes_in_skill_and_refs` | `tests/skills/test_tdd_paths.py` | grep `docs/\[domain\]/TDD_` across SKILL.md, refs/*.md, commands/tdd.md returns zero hits |
| `test_no_docs_archive_in_validation_checklists` | `tests/skills/test_tdd_paths.py` | grep `docs/archive/` across all refs/*.md returns zero hits |
| `test_release_dir_variable_defined` | `tests/skills/test_tdd_paths.py` | SKILL.md variable block defines RELEASE_DIR, COMPONENT_SLUG, TASK_ID, TASK_DIR |
| `test_builder_assembler_handoff_uses_release_dir` | `tests/skills/test_tdd_paths.py` | `build-request-template.md` line for assembler final-path contains `${RELEASE_DIR}` and does NOT contain `docs/[domain]` |
| `test_operational_guidance_session_text_references_release_tree` | `tests/skills/test_tdd_paths.py` | `operational-guidance.md` line 123 references `${RELEASE_DIR}` or `.dev/releases/` |
| `test_command_options_table_has_release_flag` | `tests/cli/test_tdd_command.py` | `commands/tdd.md` options table includes `--release` row |
| `test_component_slug_derivation_rule` | `tests/skills/test_tdd_paths.py` | Slug derivation: `"Auth/V2 (beta)"` → `auth-v2-beta`; `"Foo___Bar"` → `foo-bar`; `"---x---"` → `x`; `"!!!"` → ValueError; `""` → ValueError; `"Auth"` and `"auth"` produce the same slug `auth` (F-W2, F-F2) |
| `test_no_dangling_g_reflect_refs` | `tests/skills/test_tdd_paths.py` | No "G-REFLECT-" string appears in the spec, test plan, or generated task files (resolves F-CR1) |
| `test_builder_task_file_has_no_unresolved_variables` | `tests/skills/test_tdd_paths.py` | `grep -E '\$\{(RELEASE_DIR|TASK_DIR|TASK_ID|COMPONENT_SLUG)\}'` on a sample generated task file returns zero hits — builder resolves all variables to literals (FR-5) |
| `test_neg_empty_component_name_errors` | `tests/skills/test_tdd_paths.py` | `/sc:tdd ""` errors before any filesystem write |
| `test_neg_release_path_2_slashes_errors` | `tests/skills/test_tdd_paths.py` | `--release a/b/c` errors with grammar message |
| `test_neg_release_empty_value_falls_through` | `tests/skills/test_tdd_paths.py` | `--release ""` is treated as not provided (Step 1 falls through) |
| `test_neg_output_parent_missing_errors` | `tests/skills/test_tdd_paths.py` | `--output /no/such/dir/X.md` errors before agent work begins |
| `test_neg_resume_path_unrecognized_errors` | `tests/skills/test_tdd_paths.py` | `--resume some/random/path.md` errors (not legacy, not new) |
| `test_neg_permission_denied_halts` | `tests/skills/test_tdd_paths.py` | A write inside read-only RELEASE_DIR halts with partial-write path printed (NFR-7) |

### 8.2 Integration Tests

| Test | Validates |
|------|-----------|
| `test_resolve_release_explicit_bucket_name` | T6: `--release current/agent-platform` resolves to `.dev/releases/current/agent-platform` |
| `test_resolve_release_name_only_unique` | T7: `--release foo` resolves to unique-matching bucket |
| `test_resolve_release_name_only_ambiguous_errors` | T8: ambiguous name errors with disambiguation message |
| `test_resolve_release_not_found_errors` | T9 |
| `test_resolve_release_cwd_ancestor` | T10 |
| `test_resolve_release_prd_ancestor` | T11 |
| `test_resolve_release_synthesized_fallback` | T12: synthesized backlog dir created, user notified |
| `test_resolve_release_cwd_prd_conflict_prompts` | T13 |
| `test_concurrent_different_releases_no_collision` | T14 |
| `test_concurrent_same_release_different_components_siblings` | T15 |
| `test_concurrent_same_second_appends_suffix` | T16: second run gets `-<rand4>` suffix |
| `test_resume_finds_existing_unchecked_task` | T17 |
| `test_resume_legacy_path_works` | T18: explicit legacy `--resume` path still functions |
| `test_implicit_resume_dual_scan_with_deprecation` | T19: scan covers both trees, legacy hit prints deprecation |
| `test_new_layout_takes_precedence_over_legacy` | T20: When the implicit-resume scan finds candidates in BOTH the new tree (`.dev/releases/.../tdd/<slug>/TASK-TDD-*/`) and the legacy tree (`.dev/tasks/to-do/TASK-TDD-*/`) for the same component, the new-tree task is selected. The legacy hit is logged to stderr at INFO level but not used. |
| `test_output_override_honored_in_new_layout` | T21: `--output ./custom/path/MY_TDD.md` overrides the default `${RELEASE_DIR}/TDD_*.md`; artifacts still go to `${RELEASE_DIR}/tdd/<slug>/...` but final TDD lands at the override path |
| `test_output_override_with_release_flag` | T22: `--release backlog/foo --output ../external/TDD.md` writes final TDD outside the release dir; emits single-line stderr warning per FR-3 then proceeds; `${TASK_DIR}` still inside RELEASE_DIR |
| `test_resume_and_release_conflict_resume_wins` | T23: `--resume <legacy-path> --release backlog/foo` — the resume layout wins, `--release` is ignored with a warning (FR-6) |
| `test_synthesize_idempotent_concurrent` | T24: Two parallel runs both hitting FR-2 step 4 for the same new component end with one synthesized RELEASE_DIR shared between them; each gets its own `tdd/<slug>/TASK-TDD-*/` sibling. No exception on second mkdir. |
| `test_synthesize_collides_with_real_release_appends_timestamp` | T25: When `.dev/releases/backlog/tdd-<slug>/` already exists with a `spec.md`, step 4 synthesizes `tdd-<slug>-YYYYMMDD-HHMMSS/` instead |
| `test_cwd_inside_nested_tdd_picks_release_root` | T26: cwd is `.dev/releases/current/foo/tdd/bar/TASK-TDD-.../research/`; step 2 returns `.dev/releases/current/foo/`, NOT a subdir of it |
| `test_non_tty_conflict_errors_with_exit_code` | T27: cwd + PRD point to different releases AND stdin is not a TTY → skill exits non-zero, prints both candidates, does NOT prompt |

### 8.3 Manual / E2E Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|-----------------|
| End-to-end run on new release | 1. `mkdir -p .dev/releases/backlog/test-release` 2. `/sc:tdd "test component" --release backlog/test-release` 3. Wait for completion | Final TDD at `.dev/releases/backlog/test-release/TDD_test-component.md`; all research/qa/synthesis files under `.../tdd/test-component/TASK-TDD-*/` |
| Legacy resume | 1. Locate or stage an existing `.dev/tasks/to-do/TASK-TDD-*/...md` 2. `/sc:tdd --resume <legacy-path>` 3. Wait for completion | Run completes under legacy layout; final TDD's Document History notes the deprecation |
| Lifecycle move | After a release completes under new layout, run `git mv .dev/releases/current/<name>/ .dev/releases/complete/<name>/` | All TDD artifacts move with the release; no orphaned references |
| `make verify-sync` | After all edits land, run `make sync-dev && make verify-sync` | Both succeed; exit 0 |
| M3 — NFR-3 discoverability | After an end-to-end run, run `ls .dev/releases/<bucket>/<name>/` | Output shows `TDD_<component>.md` as a sibling of `spec.md`/`roadmap.md` |
| M4 — NFR-6 lifecycle move | After a release completes, run `git mv .dev/releases/current/<name>/ .dev/releases/complete/<name>/` | All TDD artifacts (final TDD + `tdd/<slug>/TASK-TDD-*/` tree) move with the release; no orphan references remain |
| M5 — NFR-7 write-failure halt | Pre-create a RELEASE_DIR, then `chmod -R a-w` on its `tdd/` subtree before triggering a run | Skill halts on first write error with non-zero exit; the failed partial-write path is printed to stderr; no implicit retry |

## 9. Migration & Rollout

- **Breaking changes:** No. The skill still accepts legacy `--resume` paths. New runs default to the new layout, but the layout change is transparent to the command surface (the only new flag is `--release`, which is optional).
- **Backwards compatibility:** Legacy task folders remain readable and resumable via explicit `--resume <legacy-path>`. Implicit resume scan covers both trees with a one-time deprecation notice per discovered legacy task.
- **Rollback plan:** Revert the 5 edited files (commands/tdd.md, SKILL.md, build-request-template.md, operational-guidance.md, validation-checklists.md) from git. No data migration to undo. Any artifacts already written under the new layout remain readable; they just become orphan files relative to the reverted skill.
- **Rollout sequence:** This is a self-contained skill text refactor. Land in one PR. Run `make sync-dev && make verify-sync` as part of the PR. Smoke-test by dogfooding: from inside `.dev/releases/backlog/tdd-artifact-containment/`, run `/sc:tdd "release-resolution-algorithm" --tier lightweight --focus src/superclaude/skills/tdd/SKILL.md`. Expected outcome: a small TDD lands at `.dev/releases/backlog/tdd-artifact-containment/TDD_release-resolution-algorithm.md` with all research/qa artifacts under `tdd/release-resolution-algorithm/TASK-TDD-*/`.

## 10. Downstream Inputs

### For sc:roadmap

This refactor produces a single release with milestones: variable contract, resolution algorithm, command surface, builder hand-off, backwards-compat layer, test suite. Sequential phases (1) skill foundation, (2) refs propagation, (3) command surface, (4) tests. Single-developer release; no parallelization needed beyond intra-step parallel reads.

### For sc:tasklist

Task breakdown follows the Implementation Order in Section 4.6: 10 tasks. Tasks 1-3 are sequential; 4-7 parallel; 8-10 sequential. Each task corresponds to one edit cluster (D1.x, D2.x, etc.) plus its associated tests. Total estimated effort: 2-3 hours for a single developer including test authoring.

## 11. Open Items

> Per the spec-panel critique, Open Items OI-1, OI-2, OI-4, and OI-5 had `Decided` resolutions and have been promoted into §2.1 Key Design Decisions. The remaining open items are listed below.

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| OI-3 | Should a PreToolUse hook reject writes to `.dev/tasks/to-do/TDD-*` to enforce at hook level? | Deferred to a future release | Out of scope here; reconsider if drift observed post-deployment |
| OI-6 | Should the skill emit a structured `resolution-log.json` inside TASK_DIR recording which of the 4 resolution steps fired (and why), to aid future debugging of release-dir drift? | Low — observability only; no behavior change | Deferred to future release; revisit if support burden grows |
| OI-7 | Full Windows compatibility validation (path normalization, case-insensitive FS behavior, `pathlib` round-trips). | Low — current users are POSIX; CI is Linux | Deferred to a future release; tracked in Risk table |

## 12. Brainstorm Gap Analysis

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|-----------------|---------|
| G1 | No formal definition of where COMPONENT_SLUG comes from when user-supplied component name has weird characters | Low | FR-1, OI-4 | architect |
| G2 | Spec does not cover behavior when `.dev/releases/` directory itself does not exist (greenfield repo) | Low | FR-2 step 4 | architect |
| G3 | Spec does not specify whether `make sync-dev` is part of the PR or post-merge | Low | Section 4.6 step 8 | devops |
| G4 | Test plan does not cover the `--output` override path explicitly | Medium | Section 8 | qa |
| G5 | Spec assumes single-developer rollout; multi-developer feature-branch coordination not addressed | Low | Section 9 | devops |

**Summary:** Five low-to-medium gaps identified. G1 and G4 should be resolved before implementation (G1: confirm slug derivation rule explicit; G4: add a test for `--output` override). G2, G3, G5 are minor and can be resolved during implementation.

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| RELEASE_DIR | Absolute path to a release directory: `.dev/releases/<bucket>/<release-name>/` |
| COMPONENT_SLUG | Kebab-case identifier for the component being designed |
| TASK_ID | Timestamp-based MDTM task identifier, optionally suffixed with rand4 |
| TASK_DIR | Per-run artifact root: `${RELEASE_DIR}/tdd/${COMPONENT_SLUG}/${TASK_ID}/` |
| Synthesized release | A release directory created on-demand by step 4 of the resolution algorithm, named `tdd-<slug>` under `backlog/` |
| Legacy layout | The pre-refactor layout writing artifacts to `.dev/tasks/to-do/` and `docs/` |
| MDTM | Markdown-Driven Task Management — the task-file format the skill produces |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `tdd-artifact-index.md` (sibling) | Evidence base — 28 + 13 + 14 references catalogued |
| `.dev/README.md` | Canonical `.dev/` convention; "release planning lives in `.dev/releases/`" rule |
| `CLAUDE.md` (project) | Plugin override section: `.claude/skills/<skill>-workspace/` rejection — same architectural pattern this spec applies to TDD |
| `src/superclaude/skills/tdd/SKILL.md` | Primary edit target |
| `src/superclaude/commands/tdd.md` | Secondary edit target (command surface) |
