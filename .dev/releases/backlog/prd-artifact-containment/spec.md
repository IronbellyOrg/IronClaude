---
title: "PRD Skill — Artifact Containment in Release Folders"
version: "1.0.0"
status: draft
feature_id: FR-PRD-CONTAIN
parent_feature: null
spec_type: refactoring
complexity_score: 0.55
complexity_class: MEDIUM
target_release: v4.3.0
authors: [user, claude]
created: 2026-05-14
quality_scores:
  clarity: 8.5
  completeness: 8.5
  testability: 9.0
  consistency: 8.5
  overall: 8.6
---

## 1. Problem Statement

> What problem does this work solve? Why does it matter? What fails or is suboptimal today?

The `prd` skill (`src/superclaude/skills/prd/`) currently writes 15 artifact classes to `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/` and the final PRD to `docs/docs-product/tech/[feature-name]/`. The IronClaude project's discipline is that **all development artifacts produced for a release must live inside `.dev/releases/<bucket>/<release-name>/`**. The skill predates this discipline and is unaware of the release tree. As a result:

- Research, synthesis, and QA artifacts that justify a release-scoped PRD live in a separate, timestamp-keyed tree with no binding back to the release.
- The final PRD lands in a global `docs/` location regardless of which release it belongs to.
- Concurrent developers working on different releases can collide on the same `TASK-PRD-YYYYMMDD-HHMMSS/` minute-resolution timestamp.
- The skill cannot be cleanly resumed by another developer because the workspace location is not tied to the release.

### 1.1 Evidence

| Evidence | Source | Impact |
|----------|--------|--------|
| 12 hardcoded `.dev/tasks/to-do/` references in skill | `prd-artifact-index.md` Section A (this release dir) | Single-point rewrite required across SKILL.md + 2 refs files |
| 10 `docs/` references (5 write sites + 5 read/example) | `prd-artifact-index.md` Section B | Final PRD destination + archive step violate containment |
| 17 artifact classes (C1–C17) created outside release folder | `prd-artifact-index.md` Section C | All must be re-rooted; concurrent-dev collision risk |
| 0 references to `.dev/releases/` anywhere in the skill | `grep -rn "\.dev/releases" src/superclaude/skills/prd/` | Skill is entirely unaware of the release tree |
| CLAUDE.md project rule: all artifacts in `.dev/releases/...` | `/config/workspace/IronClaude/CLAUDE.md` "Plugin Override" section + project discipline | Direct violation of stated rule |

### 1.2 Scope Boundary

**In scope**:
- `src/superclaude/skills/prd/SKILL.md` (full rewrite of Output Locations + Stage A.0/A.1)
- `src/superclaude/skills/prd/refs/build-request-template.md` (new variables, new task-file location)
- `src/superclaude/skills/prd/refs/operational-guidance.md` (artifact table, update flow, session mgmt)
- `src/superclaude/skills/prd/refs/validation-checklists.md` (Step 11 archive path, new validation lines)
- `src/superclaude/skills/prd/refs/agent-prompts.md` (placeholder discipline)
- `.claude/skills/prd/**` synced from src via `make sync-dev`
- Test additions for path resolution, containment, publish step, resumability

**Out of scope**:
- Migration utility for legacy in-flight `.dev/tasks/to-do/TASK-PRD-*/` folders (manual / future)
- Changes to `rf-task-builder`, `rf-analyst`, `rf-qa`, `rf-assembler` agent definitions themselves (they consume the new variables verbatim; no agent logic change required)
- Changes to the `/task` skill (it already accepts a task-file path argument)
- Changes to `src/superclaude/examples/prd_template.md` (read-only schema)
- A `/sc:prd` slash-command wrapper (does not exist; not introduced here)
- Cross-skill containment for `tdd`, `tech-research`, `tech-reference`, etc. (separate releases)

## 2. Solution Overview

> High-level description of the approach. What changes, what stays the same.

Introduce a new **Stage A.0 — Release Resolution** that runs before the existing A.1 existing-task probe. A.0 uses a 4-tier resolution algorithm (explicit → session-inferred → slug-matched → user-consented bootstrap) to compute `RELEASE_PATH`, then derives `PRD_WORKSPACE = ${RELEASE_PATH}prd-workspace/${PRD_SLUG}/` and re-points `TASK_DIR` to `${PRD_WORKSPACE}`. Every existing artifact path placeholder (`${RESEARCH_DIR}`, `${SYNTHESIS_DIR}`, `${QA_DIR}`, etc.) is preserved by name but resolves to a new release-internal location.

The final PRD is written to `${PRD_CANONICAL_PATH} = ${PRD_WORKSPACE}PRD_<SLUG>.md` (release-internal, canonical). A new opt-in Phase-7 publish step optionally copies or symlinks the PRD to a user-supplied `${PUBLISH_PATH}` under `docs/`. By default the skill makes zero writes outside the release folder.

Legacy `.dev/tasks/to-do/TASK-PRD-*/` folders remain read-only references: Stage A.1 detects them, informs the user, but never auto-migrates or deletes.

### 2.1 Key Design Decisions

| Decision | Choice | Alternatives Considered | Rationale |
|----------|--------|------------------------|-----------|
| Release-dir resolution strategy | **Hybrid** (explicit → session → slug → bootstrap) | Explicit-only; session-only; slug-only | Hybrid covers the full usage spectrum (CI, dev, first-PRD-in-release) without forcing a separate setup command. |
| PRD subfolder name | **`prd-workspace/<slug>/`** | `prd/`; `prd-<slug>/`; `prd/<slug>/` | Mirrors `.dev/eval-workspaces/<skill-name>/` from the skill-creator override, signals "iteration workspace", supports multiple PRDs per release. |
| Bootstrap UX | **User-consented prompt** with 3 options | Auto-create silently; refuse and require `/sc:release` first | First-PRD-in-release is a common entry point; auto-create is too aggressive, refusal is too high-friction. Explicit consent strikes the balance. |
| Final-PRD home | **Release-canonical + optional docs/ publish** | Keep in `docs/` only; release-only with no publish | Containment is preserved (canonical lives in release); GameFrame `docs/` convention is honoured as an opt-in publish step, not an implicit side effect. |
| Task-file naming | **Flat `task.md`** (drop timestamp) | Keep timestamped `TASK-PRD-YYYYMMDD-HHMMSS.md` | Release+slug already provides global uniqueness; flat naming simplifies resumability probe to a single path check. |
| Backward compat | **Read-only detection only**, no auto-migration | Auto-migrate; ignore legacy folders | Migration is risky and out of scope; ignoring loses in-flight work. Detection + user prompt preserves user agency. |
| Path variable propagation | **Through BUILD_REQUEST verbatim** | Have builder re-derive paths | Single point of truth (orchestrator computes once); builder is a faithful transcriber. |
| `TASK_DIR` alias retention | **Deprecated alias, retained through v4.3.x, scheduled for removal in v4.4.0** | Remove now and rename in all refs/* files; keep forever | Removing now forces simultaneous edits in 4 refs files plus all agent prompts in one release, increasing rollback risk. Keeping the alias temporarily preserves backwards-compat for refs/ templates; deprecation target prevents perpetual ambiguity (Fowler F-C1). |
| Bootstrap default bucket | **`backlog/`** (resolves OQ-1) | `current/` | Backlog is the safer default — does not imply active sprint commitment; matches the existing release-hygiene workflow of promoting backlog → current explicitly. |
| Slug filename casing | **Uppercase with `-` preserved** (e.g., `PRD_WIZARD-SYSTEM.md`) — resolves OQ-5 | Uppercase with `_` substitution; lowercase | Preserves human-readable kebab while signaling "deliverable" via uppercase. Locked pre-implementation to prevent inconsistent filenames between developers. |

### 2.2 Workflow / Data Flow

```
User invokes /prd
        |
        v
Stage A.0 — Release Resolution
  1. Explicit RELEASE_PATH in prompt? -----> use it
  2. CWD under .dev/releases/<b>/<n>/? ----> infer it
  3. Branch matches feat/<name> or fix/<name>? -> map to release
  4. PRD_SLUG matches exactly one .dev/releases/*/*<slug>*/ ? -> use it
  5. Otherwise ask user:
       (a) Bootstrap .dev/releases/backlog/<slug>/   <-- default offered
       (b) Use specified path
       (c) Cancel
  -> RELEASE_PATH, RELEASE_BUCKET, RELEASE_NAME
  -> PRD_WORKSPACE = ${RELEASE_PATH}prd-workspace/${PRD_SLUG}/
  -> TASK_DIR = PRD_WORKSPACE  (alias retained)
  -> Create ${TASK_DIR}{research,synthesis,qa,reviews}/

Stage A.1 — Existing-task probe
  - ${TASK_FILE} exists with unchecked items?  -> resume via /task
  - ${TASK_DIR}research-notes.md exists?       -> continue from its status
  - Legacy .dev/tasks/to-do/TASK-PRD-*/ found? -> notify user (READ-ONLY)
  - Otherwise continue to A.2

Stage A.2 — A.8 (unchanged in shape, all paths re-rooted)

Stage B — /task skill consumes ${TASK_FILE}, runs F1 loop
  Phase 2-6 emit research/synthesis/QA into ${PRD_WORKSPACE}
  Phase 6 Assembler writes canonical PRD to ${PRD_CANONICAL_PATH}
  Phase 7 OPT-IN publish to ${PUBLISH_PATH} if user opts in

Final state:
  - Every artifact under ${PRD_WORKSPACE}
  - ${PRD_CANONICAL_PATH} is authoritative
  - ${PUBLISH_PATH} exists only if user opted in
  - docs/archive/ never touched
```

### 2.3 Actors & Invocation Modes

| Actor | Description | Behaviour at Stage A.0 step 5 (no match found) |
|-------|-------------|------------------------------------------------|
| **Human developer (interactive)** | A developer running `/prd` directly in Claude Code | Skill prompts with 3 options (bootstrap / specify path / cancel); blocks until response |
| **Orchestrator agent (interactive proxy)** | An LLM orchestrator like `/sc:pm` invoking `/prd` while a human supervises | Same as human developer; the orchestrator forwards the prompt to the supervising human |
| **Subagent / CI / non-interactive caller** | Programmatic invocation with no human in the loop (CI pipeline, batch script, automated agent chain) | The skill MUST detect non-interactive mode and require explicit `RELEASE_PATH`; if `RELEASE_PATH` is unset OR resolution falls through to step 5, the skill HALTS with a clear error rather than bootstrapping silently |

**Non-interactive mode detection:** The skill is in non-interactive mode when ANY of the following holds: (a) environment variable `IRONCLAUDE_NON_INTERACTIVE=1`, (b) explicit `--non-interactive` flag in the invocation, (c) stdin is not a TTY, (d) the invocation context indicates a parent agent (e.g., a `subagent_type` was set when this skill loaded).

### 2.4 Worked Example — Variable Resolution

Given the following inputs:
- `PRD_SLUG=wizard-system`
- `RELEASE_BUCKET=current`
- `RELEASE_NAME=q2-redesign`
- Resolution method: `explicit` (RELEASE_PATH provided in prompt)
- `PUBLISH_MODE=copy`
- `PUBLISH_PATH=docs/docs-product/tech/wizard/PRD_WIZARD-SYSTEM.md`

The skill resolves to:

```
RELEASE_PATH          = .dev/releases/current/q2-redesign/
PRD_WORKSPACE         = .dev/releases/current/q2-redesign/prd-workspace/wizard-system/
TASK_DIR              = .dev/releases/current/q2-redesign/prd-workspace/wizard-system/   (alias of PRD_WORKSPACE)
TASK_FILE             = .dev/releases/current/q2-redesign/prd-workspace/wizard-system/task.md
RESEARCH_DIR          = .dev/releases/current/q2-redesign/prd-workspace/wizard-system/research/
SYNTHESIS_DIR         = .dev/releases/current/q2-redesign/prd-workspace/wizard-system/synthesis/
QA_DIR                = .dev/releases/current/q2-redesign/prd-workspace/wizard-system/qa/
REVIEWS_DIR           = .dev/releases/current/q2-redesign/prd-workspace/wizard-system/reviews/
SOURCES_ARCHIVE_DIR   = .dev/releases/current/q2-redesign/prd-workspace/wizard-system/sources-archive/
PRD_CANONICAL_PATH    = .dev/releases/current/q2-redesign/prd-workspace/wizard-system/PRD_WIZARD-SYSTEM.md
```

The single-line bootstrap README stub (when triggered) reads:

```markdown
# Release stub: wizard-system

Created 2026-05-14T12:34:56Z by /prd skill (bootstrap path, Stage A.0 step 5a). Promote to current/ or complete/ when ready.
```

## 3. Functional Requirements

### FR-PRD-CONTAIN.1: Release Resolution (Stage A.0)

**Description**: The skill MUST resolve a `RELEASE_PATH` under `.dev/releases/<backlog|current|complete>/<release-name>/` before any other Stage-A work begins. Resolution uses the 4-tier algorithm: explicit input → session inference (CWD or git branch) → slug-based reverse lookup → user-consented bootstrap.

**Acceptance Criteria**:
- [ ] **(W-H1)** `RELEASE_PATH` exists and matches `.dev/releases/(backlog|current|complete)/[a-z0-9][a-z0-9-]*/` — validated by `test_release_resolution_explicit`
- [ ] **(W-H1)** Resolution method (`explicit | session-cwd | session-branch | slug | bootstrap`) is recorded in `${TASK_DIR}research-notes.md` under a `RELEASE_RESOLUTION` heading AND emitted as a structured log line (see NFR-CONTAIN.7) — validated by `test_resolution_method_logged`
- [ ] **(W-H1)** When multiple slug matches are found, the skill HALTS and prompts the user; it does NOT auto-pick — validated by `test_release_resolution_slug_multi`
- [ ] **(W-H1)** Match priority when multiple resolution tiers could fire simultaneously is: explicit (step 1) > session-cwd (step 2) > session-branch (step 3) > slug-reverse-lookup (step 4) > bootstrap (step 5). Within step 4, an existing `prd-workspace/<slug>/` containment beats a release-name match — validated by `test_match_priority`
- [ ] **(W-H1)** When no match is found in interactive mode, the user is offered exactly 3 options: bootstrap (default — bucket = `backlog/` per §2.1 decision) / specify path / cancel — validated by `test_release_resolution_no_match`
- [ ] **(W-H1)** Cancel option (step 5c) exits the skill cleanly with zero side-effects: no directories created, no files written, no state persisted — validated by `test_release_resolution_cancel`
- [ ] **(W-H1, N-C1, CRITICAL)** **CWD precondition guard:** Before any resolution step runs, the skill MUST verify CWD is inside an IronClaude project by checking for AT LEAST ONE of: (a) `pyproject.toml` with `[tool.superclaude]` table, (b) `.dev/README.md` file, (c) ancestor directory matching one of these conditions. If none found, the skill HALTS with error: `"/prd must be invoked inside an IronClaude project (no pyproject.toml [tool.superclaude] table or .dev/README.md found from CWD upward). Bootstrap will not pollute foreign repositories."` — validated by `test_release_resolution_foreign_repo_halt`
- [ ] **(N-H1, WH-C2, CRITICAL)** **Bootstrap atomicity + re-resolve verification:** Bootstrap uses `mkdir -p` (idempotent). After bootstrap, the skill MUST re-run the resolution algorithm; if step 4 (slug-match) now returns multiple results due to a concurrent bootstrap, HALT and prompt the user. If only a release stub exists (`README.md` present but `prd-workspace/<slug>/` empty or absent), step 4 MUST treat it as the bootstrap-completion path and proceed to create the missing `prd-workspace/<slug>/` subtree rather than reporting it as an existing match — validated by `test_release_resolution_concurrent_bootstrap` and `test_release_resolution_half_bootstrap`
- [ ] **(A-H1)** Branch-match rule (step 3): The skill extracts the suffix from a branch matching `^(feat|fix|chore|refactor)/(?P<slug>[a-z0-9][a-z0-9-]*)$` and matches it against existing release names using **exact equality** (no fuzzy/substring matching). Branch `feat/foo` matches a release named exactly `foo`; it does NOT match `foo-v2`. If two releases share the same name across buckets (e.g., `current/foo` and `backlog/foo`), `current/` wins; if neither wins, HALT and prompt — validated by `test_release_resolution_branch`
- [ ] Bootstrap creates `.dev/releases/backlog/<PRD_SLUG>/README.md` with the literal stub content shown in §2.4 — validated by `test_release_resolution_bootstrap`
- [ ] **(WH-H1)** Empty or whitespace-only `PRD_SLUG` HALTS with error: `"PRD_SLUG cannot be empty; provide a kebab-case product identifier."` — validated by `test_prd_slug_empty`
- [ ] **(C-H1, K-M1)** In non-interactive mode (per §2.3), the skill MUST NOT prompt; if resolution falls through to step 5 OR `PRD_SLUG` is unset, HALT with a clear error directing the caller to set `RELEASE_PATH` and `PRD_SLUG` explicitly — validated by `test_release_resolution_non_interactive_halt`

**Dependencies**: none

### FR-PRD-CONTAIN.2: Workspace Path Derivation

**Description**: All artifact paths MUST resolve from a single derivation chain: `RELEASE_PATH → PRD_WORKSPACE → TASK_DIR → {RESEARCH_DIR, SYNTHESIS_DIR, QA_DIR, REVIEWS_DIR, SOURCES_ARCHIVE_DIR, PRD_CANONICAL_PATH}`.

**Acceptance Criteria**:
- [ ] `PRD_WORKSPACE` = `${RELEASE_PATH}prd-workspace/${PRD_SLUG}/` — validated by `test_paths_containment`
- [ ] `TASK_DIR` is an alias for `PRD_WORKSPACE` (deprecated; removal target v4.4.0 per §2.1) — validated by `test_task_dir_alias`
- [ ] `TASK_FILE` = `${TASK_DIR}task.md` (flat naming, no timestamp) — validated by `test_task_file_naming`
- [ ] `PRD_CANONICAL_PATH` = `${TASK_DIR}PRD_${PRD_SLUG_UPPER}.md` where `PRD_SLUG_UPPER` is `PRD_SLUG.upper()` with `-` preserved (per §2.1 decision) — validated by `test_prd_canonical_path`
- [ ] `${TASK_DIR}{research,synthesis,qa,reviews,sources-archive}/` subfolders created during Stage A.0 — validated by `test_workspace_subdirs_created`
- [ ] `PRD_SLUG` matches `^[a-z0-9][a-z0-9-]*$` with length ≤ 48 characters (validated, error on fail) — validated by `test_prd_slug_regex` and `test_prd_slug_length_bound`
- [ ] **(WH-C1, CRITICAL)** **Reserved slug list:** `PRD_SLUG` MUST NOT match any of the following reserved names (case-sensitive): `prd-workspace`, `research`, `synthesis`, `qa`, `reviews`, `sources-archive`, `task`, `archive`. If a reserved slug is supplied, HALT with error: `"PRD_SLUG '<value>' collides with a reserved workspace directory name. Choose a different slug."` — validated by `test_prd_slug_reserved_words`

**Dependencies**: FR-PRD-CONTAIN.1

### FR-PRD-CONTAIN.3: Artifact Containment Invariant

**Description**: Every artifact produced by the skill — task file, research notes, codebase/web research files, synthesis files, gap log, analyst reports, QA reports, partitioned QA reports, update-research files, canonical PRD, archived consolidation sources — MUST be written under `${PRD_WORKSPACE}`.

**Acceptance Criteria**:
- [ ] All 17 artifact classes (C1–C17 from `prd-artifact-index.md`) write under `${PRD_WORKSPACE}` post-change
- [ ] Static check: `grep -nE "\\.dev/tasks/to-do/" src/superclaude/skills/prd/` returns hits ONLY inside a clearly labelled "Legacy task folders (read-only)" subsection
- [ ] Static check: `grep -nE "docs/docs-product/" src/superclaude/skills/prd/` returns hits ONLY in example/discovery references, never in write-site instructions
- [ ] No agent-prompt instance hardcodes a `.dev/tasks/to-do/` or `docs/docs-product/` path; all use `${...}` placeholders resolved per BUILD_REQUEST
- [ ] Validation Checklist Step 9 has a new line: "Canonical PRD path is under `.dev/releases/<bucket>/<name>/prd-workspace/<slug>/`"

**Dependencies**: FR-PRD-CONTAIN.2

### FR-PRD-CONTAIN.4: Existing-task Probe with Legacy Detection

**Description**: Stage A.1 MUST check for an in-progress workspace at `${TASK_FILE}`, AND scan `.dev/tasks/to-do/TASK-PRD-*/` for legacy folders matching the current `PRD_SLUG`. Legacy folders are read-only — the skill never migrates or deletes them automatically.

**Acceptance Criteria**:
- [ ] When `${TASK_FILE}` exists with unchecked items, skill resumes via the `/task` skill — validated by `test_resume_existing_task_file`
- [ ] **(C-M2, WH-M2)** When a matching legacy task folder is found, the skill notifies the user and offers exactly three options with the following defined behaviour:
  - **Option 1 — "migrate manually":** Skill prints the legacy folder path, lists which artifacts could be ported, and EXITS without further action. User performs the migration outside the skill. Re-invoking `/prd` after manual migration finds the new release-internal workspace and proceeds normally.
  - **Option 2 — "finish in legacy":** Skill EXITS. The legacy folder is the user's responsibility; the new release workspace (if Stage A.0 already created it) remains as an empty stub. Re-invoking with this slug will detect the empty stub via the half-bootstrap rule and rebuild from scratch. The skill does NOT remap `TASK_DIR` back to the legacy path.
  - **Option 3 — "start fresh":** Skill prompts for a slug-suffix (e.g., `wizard-system` → `wizard-system-v2`) to avoid the legacy collision, then proceeds with the new slug. If the user declines a suffix, HALT.
  — validated by `test_legacy_probe_detection`, `test_legacy_option_migrate_manually`, `test_legacy_option_finish_in_legacy`, `test_legacy_option_start_fresh`
- [ ] No auto-deletion of any legacy folder under any circumstance — validated by `test_legacy_no_auto_delete`
- [ ] When all items in `${TASK_FILE}` are checked, skill reports PRD complete and offers update/re-run — validated by `test_task_file_all_complete`

**Dependencies**: FR-PRD-CONTAIN.2

### FR-PRD-CONTAIN.5: Opt-in Docs Publish

**Description**: Phase 7 MUST offer an OPT-IN publish step. By default (`PUBLISH_MODE=none`) no write occurs outside `${PRD_WORKSPACE}`. When the user selects `copy` or `symlink`, the canonical PRD is materialised at user-supplied `${PUBLISH_PATH}`.

**Acceptance Criteria**:
- [ ] **(W-M2)** `PUBLISH_MODE` defaults to `none` when unset; explicit `PUBLISH_MODE=none` is equivalent — validated by `test_publish_default_none`
- [ ] **(WH-M1)** `PUBLISH_MODE` is case-sensitive. Accepted values: `none`, `copy`, `symlink`. Any other value (including case-variants like `NONE`, `Copy`) HALTS with error — validated by `test_publish_mode_case_sensitive`
- [ ] Default behaviour writes ZERO bytes to `docs/` — validated by `test_publish_default_none`
- [ ] `PUBLISH_MODE=copy` produces a byte-identical copy at `${PUBLISH_PATH}`; canonical untouched — validated by `test_publish_optin_copy`
- [ ] `PUBLISH_MODE=symlink` produces a symlink at `${PUBLISH_PATH}` → `${PRD_CANONICAL_PATH}` — validated by `test_publish_symlink`
- [ ] **(N-H3)** **Publish target preconditions:** Before writing, the skill MUST verify (a) parent directory of `${PUBLISH_PATH}` exists, (b) target path does not exist OR `PUBLISH_OVERWRITE=1` is explicitly set. If target exists without overwrite flag, HALT with: `"Publish target '<path>' already exists; set PUBLISH_OVERWRITE=1 to replace, or choose a different path."` — validated by `test_publish_target_exists_halt`
- [ ] **(A-M1)** **Symlink-unsupported failure:** If `PUBLISH_MODE=symlink` and the underlying filesystem does not support symlinks (e.g., some Docker volume mounts, FAT/exFAT, Windows without developer mode), HALT with: `"Symlink creation failed on this filesystem; use PUBLISH_MODE=copy instead."` — validated by `test_publish_symlink_unsupported_filesystem`
- [ ] If `${PUBLISH_PATH}` is unsupplied while `PUBLISH_MODE != none`, skill halts with a clear error — validated by `test_publish_path_missing`
- [ ] **(H-M2)** Publish event is recorded in the task file Task Log AND as a structured JSON line in `${TASK_DIR}publish-log.jsonl` with schema: `{"timestamp": "<ISO-8601>", "mode": "copy|symlink", "source": "<PRD_CANONICAL_PATH>", "target": "<PUBLISH_PATH>", "overwrite": false}` — validated by `test_publish_log_schema`

**Dependencies**: FR-PRD-CONTAIN.3

### FR-PRD-CONTAIN.6: Sources-archive Path Update

**Description**: Step 11 of `validation-checklists.md` MUST archive consolidation source documents to `${SOURCES_ARCHIVE_DIR}` (under the release workspace), not `docs/archive/`.

**Acceptance Criteria**:
- [ ] `docs/archive/` no longer appears as a write site anywhere in the skill
- [ ] `${SOURCES_ARCHIVE_DIR}` is created on-demand during Phase 7 when archiving is approved
- [ ] User is prompted before any source-doc move; nothing auto-archives

**Dependencies**: FR-PRD-CONTAIN.3

### FR-PRD-CONTAIN.7: Variable Propagation through BUILD_REQUEST

**Description**: The BUILD_REQUEST template MUST be extended with the new variables (RELEASE_BUCKET, RELEASE_NAME, RELEASE_PATH, PRD_SLUG, PRD_WORKSPACE, TASK_DIR, TASK_FILE, PRD_CANONICAL_PATH, PUBLISH_MODE, PUBLISH_PATH, RELEASE_RESOLUTION) so the `rf-task-builder` subagent embeds correct paths in every checklist item.

**Acceptance Criteria**:
- [ ] BUILD_REQUEST contains all new variables with explicit values (no `${...}` left unresolved) — validated by `test_build_request_variables_resolved`
- [ ] **(NW-M1)** BUILD_REQUEST contains a top-level `BUILD_REQUEST_VERSION: "1.0"` field. The `rf-task-builder` subagent MUST verify it can parse the declared version and HALT with a clear error if the version is unknown — validated by `test_build_request_version_present` and `test_build_request_version_unknown_halts`
- [ ] Task-file checklist items reference only the variable names, never hardcoded paths — validated by `test_agent_path_discipline`
- [ ] Builder STEP 6 instruction reads: "Create the task file at `${TASK_FILE}` using PART 2 structure" — validated by `test_builder_step_6_uses_variable`
- [ ] If any required variable is missing in the BUILD_REQUEST, the builder fails fast with a clear error — validated by `test_build_request_missing_variable`

**Dependencies**: FR-PRD-CONTAIN.1, FR-PRD-CONTAIN.2

### FR-PRD-CONTAIN.8: Multi-PRD-per-Release Soft Cap

**Description**: A release MAY contain multiple PRD workspaces (e.g., `prd-workspace/wizard-system/`, `prd-workspace/payment-flow/`). To bound resolution latency and surface accidental sprawl, the skill MUST warn when a release accumulates more than a soft cap.

**Acceptance Criteria**:
- [ ] **(WH-H3)** When Stage A.0 step 4 (slug reverse-lookup) scans `prd-workspace/` directories and the candidate release already contains ≥ 5 PRD workspaces, the skill emits a WARNING (not a halt) to stderr: `"Release '<release_name>' has <N> PRD workspaces; consider whether this PRD belongs to a different release."` — validated by `test_multi_prd_soft_cap_warning`
- [ ] Hard cap: above 20 PRD workspaces in a single release, the slug-match algorithm MUST still complete in under the NFR-CONTAIN.2 latency target (skill enumerates with `iterdir()`, not recursive walks) — validated by `test_multi_prd_hard_cap_latency`

**Dependencies**: FR-PRD-CONTAIN.2

## 4. Architecture

### 4.1 New Files

> **(F-H2)** No new files are added inside `src/superclaude/skills/prd/` (this is an in-place refactor of skill content). The only new file produced by this work is the test module, tracked in §4.2 under the `tests/` tree.

| File | Purpose | Dependencies |
|------|---------|-------------|
| (none inside skill package — see §4.2 for test file) | — | — |

### 4.2 Modified Files

| File | Change | Rationale |
|------|--------|-----------|
| `src/superclaude/skills/prd/SKILL.md` | Insert Stage A.0; rewrite L95-131 Output Locations; update L168-180 A.1 probe; update L257 task-folder creation; update L43 / L48 / L54 / L205 example paths; update L410 Stage B handoff example; add Legacy Folders subsection | Core anchor of `TASK_DIR` + `docs/` defaults. |
| `src/superclaude/skills/prd/refs/build-request-template.md` | Add 11 new variable fields; update L9 GOAL line; update L100-106 Phase 1 step list; update L154 TASK FILE LOCATION; update L156-165 STEPS section | Single funnel from orchestrator to builder. |
| `src/superclaude/skills/prd/refs/operational-guidance.md` | Rewrite L72-91 Artifact Locations table; update L88 Final PRD row; update L95-104 Updating-existing-PRD step list; rewrite L108-110 Session Management; add new Legacy Folders subsection | Mirror of SKILL.md table; session mgmt narrative. |
| `src/superclaude/skills/prd/refs/validation-checklists.md` | Replace L88 archive path; add 2 new validation lines to Step 9 | Single docs/ write site; new containment validation. |
| `src/superclaude/skills/prd/refs/agent-prompts.md` | Insert "Path Discipline" block; update L147-149, L183-186, L222-226, L267-269, L309-312, L358-362 output-path placeholders | Agent prompt templates must reference new variables. |
| `src/superclaude/skills/prd/refs/synthesis-mapping.md` | Audit only (read-only reference file) | Verify no embedded `.dev/tasks/to-do/` paths. |
| `.claude/skills/prd/**` | Mirror via `make sync-dev` | Project source-of-truth rule. |
| `tests/skills/test_prd_containment.py` (new) | Add 15 behavioural + 2 static tests (see Section 8) | TDD discipline; regression protection. |

### 4.3 Removed Files

None. This is a refactor of in-place content, not a deletion.

### 4.4 Module Dependency Graph

```
SKILL.md (orchestrator entry)
  | references
  v
build-request-template.md  (BUILD_REQUEST payload — Stage A.7)
  | passed-to
  v
rf-task-builder subagent (unchanged) -- reads -->  agent-prompts.md
                                                    synthesis-mapping.md
                                                    validation-checklists.md
                                                    operational-guidance.md
  | emits
  v
${TASK_FILE} (self-contained MDTM)
  | consumed by
  v
/task skill (unchanged) -- runs F1 loop --> subagents
                                              | emit
                                              v
                                  ${RESEARCH_DIR}, ${SYNTHESIS_DIR},
                                  ${QA_DIR}, ${PRD_CANONICAL_PATH}
                                  (ALL under ${PRD_WORKSPACE})
```

### 4.5 Data Models — Resolved Variable Schema

> **(F-M1, F-H1)** The 11 path/control variables introduced by this refactor form a typed schema. The orchestrator MUST resolve every variable in this table during Stage A.0 before passing the BUILD_REQUEST to the builder.

| Variable | Type | Source | Example | Validation |
|----------|------|--------|---------|------------|
| `BUILD_REQUEST_VERSION` | `str` | constant in template | `"1.0"` | exact match against builder's expected versions |
| `RELEASE_BUCKET` | `enum` | `backlog \| current \| complete` | `current` | regex `^(backlog\|current\|complete)$` |
| `RELEASE_NAME` | `str` (kebab) | release directory basename | `q2-redesign` | regex `^[a-z0-9][a-z0-9-]*$`, length ≤ 64 |
| `RELEASE_PATH` | `str` (POSIX path, trailing slash) | composed: `.dev/releases/${RELEASE_BUCKET}/${RELEASE_NAME}/` | `.dev/releases/current/q2-redesign/` | path exists, matches `.dev/releases/(backlog\|current\|complete)/[a-z0-9][a-z0-9-]*/` |
| `RELEASE_RESOLUTION` | `enum` | resolution method | `explicit \| session-cwd \| session-branch \| slug \| bootstrap` | one of the 5 enum values |
| `PRD_SLUG` | `str` (kebab) | user input or derived from scope | `wizard-system` | regex `^[a-z0-9][a-z0-9-]*$`, length ≤ 48, NOT in reserved list (FR-PRD-CONTAIN.2 AC) |
| `PRD_SLUG_UPPER` | `str` | `PRD_SLUG.upper()` (dashes preserved per §2.1) | `WIZARD-SYSTEM` | derived; never user-input |
| `PRD_WORKSPACE` | `str` (POSIX path, trailing slash) | composed: `${RELEASE_PATH}prd-workspace/${PRD_SLUG}/` | `.dev/releases/current/q2-redesign/prd-workspace/wizard-system/` | path under `${RELEASE_PATH}prd-workspace/`; created during Stage A.0 |
| `TASK_DIR` | `str` (alias) | alias of `PRD_WORKSPACE` (DEPRECATED; removal v4.4.0 per §2.1) | same as `PRD_WORKSPACE` | identity equality with `PRD_WORKSPACE` |
| `TASK_FILE` | `str` (POSIX path) | `${TASK_DIR}task.md` | `.dev/releases/.../task.md` | parent must be `${PRD_WORKSPACE}`; filename exactly `task.md` |
| `PRD_CANONICAL_PATH` | `str` (POSIX path) | `${TASK_DIR}PRD_${PRD_SLUG_UPPER}.md` | `.dev/releases/.../PRD_WIZARD-SYSTEM.md` | filename matches `^PRD_[A-Z0-9][A-Z0-9-]*\.md$` |
| `PUBLISH_MODE` | `enum` | user input or default | `none \| copy \| symlink` (default `none`) | exact case-sensitive match |
| `PUBLISH_PATH` | `str \| null` (POSIX path) | user input | `docs/docs-product/tech/wizard/PRD_WIZARD-SYSTEM.md` | required iff `PUBLISH_MODE != none`; must resolve inside repo working tree |

### 4.6 Implementation Order

```
1. Update src/superclaude/skills/prd/SKILL.md       -- core variable block + Stage A.0 + Output Locations table
2. Update refs/build-request-template.md            -- BUILD_REQUEST payload + STEP 6
   Update refs/operational-guidance.md              -- [parallel with step 2; mirror of artifact table]
3. Update refs/agent-prompts.md                     -- depends on 1, 2 (new variable names)
   Update refs/validation-checklists.md             -- [parallel with step 3]
4. Audit refs/synthesis-mapping.md                  -- verify-only; no edits expected
5. make sync-dev                                    -- propagate to .claude/
6. make verify-sync                                 -- gate
7. Add tests/skills/test_prd_containment.py         -- 15 behavioural + 2 static tests
8. uv run pytest tests/skills/test_prd_containment.py -v   -- gate
9. make lint && make format                          -- gate
10. Manual end-to-end: invoke /prd, exercise resolution + containment + publish paths
```

### 4.7 Variable Schema Sync Discipline

> **(F-H1)** The variable schema in §4.5 is the canonical source of truth. The following surfaces MUST render the variable set identically (same names, same order):
>
> 1. `src/superclaude/skills/prd/SKILL.md` Output Locations section
> 2. `src/superclaude/skills/prd/refs/build-request-template.md` variable header
> 3. `src/superclaude/skills/prd/refs/operational-guidance.md` Artifact Locations table
>
> A static lint check (added to `tests/skills/test_prd_containment.py::test_variable_schema_sync`) parses all three surfaces and asserts the variable set is identical. Drift fails the test.

## 6. Non-Functional Requirements

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-CONTAIN.1 | Zero artifacts outside `${PRD_WORKSPACE}` by default | 100% containment when PUBLISH_MODE=none | `find . -newer <start> -not -path "*/.dev/releases/*" \| wc -l` returns 0 (excluding session memory/log files) |
| NFR-CONTAIN.2 | Resolution algorithm latency | <2s for steps 1-3; user-prompt latency for step 4 | Measure on T-RES-* tests |
| NFR-CONTAIN.3 | Concurrent-developer collisions (defined as: two simultaneous `/prd` invocations writing to the same file path, OR one invocation observing a partially-written file from another, OR two `mkdir` operations racing on the same target) | 0 collisions when releases or slugs differ | T-CONCURRENT-DEV + T-MULTI-PRD-SAME-RELEASE (integration tier) |
| NFR-CONTAIN.4 | Resumability roundtrip | Resume from any phase boundary loses 0 artifacts | T-RESUMABILITY |
| NFR-CONTAIN.5 | Backward compat — legacy folders untouched | 100% of legacy folders detected, 0% auto-modified | T-LEGACY-PROBE |
| NFR-CONTAIN.6 | Documentation parity | SKILL.md table === operational-guidance.md table (byte-equivalent rows) | Spot check + lint rule (`test_variable_schema_sync`) |
| NFR-CONTAIN.7 | Resolution observability | Every Stage A.0 invocation emits a structured log line and persists the resolution method in `${TASK_DIR}research-notes.md` | Log line schema: `{"event": "release_resolution", "method": "<enum>", "release_path": "<path>", "prd_slug": "<slug>", "timestamp": "<ISO-8601>", "non_interactive": <bool>}`; emitted to stderr (visible in transcript) AND appended to `${TASK_DIR}resolution-log.jsonl`. Validated by `test_resolution_method_logged` |

## 7. Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Legacy task folders silently lose work | Medium | High | A.1 step 3 detects legacy folders, prompts user, never auto-migrates/deletes. Documented in operational-guidance.md. |
| Slug collisions across releases | Low | Medium | `PRD_SLUG` validation `^[a-z0-9][a-z0-9-]*$`; release+slug composition is the global key; multiple-match prompt halts skill. |
| Bootstrap creates noise releases | Medium | Low | Bootstrap is user-consented (3C); README stub clearly labels "stub". Cleanup falls to existing release-hygiene workflows. |
| `docs/` publish path validation gaps | Low | Medium | FR-PRD-CONTAIN.5 requires explicit `PUBLISH_PATH`; reject if path outside user git tree; document the limitation. |
| Variable propagation drift between SKILL.md and refs/ | Medium | Medium | Static grep checks (FR-PRD-CONTAIN.3 acceptance criteria); `make verify-sync` after each edit; single variable-reference block in SKILL.md. |
| Builder fails on missing variable | Low | High | Builder STEP 6 includes explicit fail-fast on unresolved `${...}`; tested via T-AGENT-PATH-DISCIPLINE. |
| Skill regressions in existing flows | Medium | High | Full 15-test suite + manual E2E run; staged implementation order. |

## 8. Test Plan

### 8.1 Unit Tests

| Test | File | Validates |
|------|------|-----------|
| `test_release_resolution_explicit` | `tests/skills/test_prd_containment.py` | T-RES-EXPLICIT — explicit RELEASE_PATH wins |
| `test_release_resolution_cwd` | same | T-RES-SESSION-CWD — CWD inference |
| `test_release_resolution_branch` | same | T-RES-SESSION-BRANCH — git branch inference, current/ preferred over backlog/ |
| `test_release_resolution_slug_single` | same | T-RES-SLUG-MATCH — exactly-one slug match |
| `test_release_resolution_slug_multi` | same | T-RES-SLUG-MULTIPLE — halts pending user pick |
| `test_release_resolution_bootstrap` | same | T-RES-BOOTSTRAP — creates backlog/<slug>/README.md stub |
| `test_release_resolution_cancel` | same | T-RES-CANCEL — clean halt, zero writes |
| `test_paths_containment` | same | T-PATHS-CONTAINMENT — every artifact under PRD_WORKSPACE on Lightweight tier |
| `test_publish_optin_copy` | same | T-PUBLISH-OPTIN — PUBLISH_MODE=copy materialises and leaves canonical untouched |
| `test_publish_default_none` | same | T-PUBLISH-DEFAULT-NONE — zero docs/ writes by default |
| `test_legacy_probe_detection` | same | T-LEGACY-PROBE — detects legacy, prompts, no auto-migrate |
| `test_resumability` | same | T-RESUMABILITY — interrupt and resume, no artifact loss |
| `test_agent_path_discipline` | same | T-AGENT-PATH-DISCIPLINE — task-file contents free of hardcoded paths |
| `test_release_resolution_foreign_repo_halt` | same | N-C1 — invoking outside IronClaude project halts |
| `test_release_resolution_concurrent_bootstrap` | same | N-H1 — concurrent bootstrap is safe |
| `test_release_resolution_half_bootstrap` | same | WH-C2 — half-bootstrapped release detected and completed |
| `test_release_resolution_cancel` | same | Cancel exits cleanly with zero side-effects |
| `test_release_resolution_no_match` | same | 3-option prompt offered |
| `test_release_resolution_non_interactive_halt` | same | C-H1/K-M1 — non-interactive mode never prompts |
| `test_prd_slug_empty` | same | WH-H1 — empty slug halts with clear error |
| `test_prd_slug_reserved_words` | same | WH-C1 — reserved slug list enforced |
| `test_prd_slug_length_bound` | same | F-M1 — slug length cap enforced |
| `test_publish_target_exists_halt` | same | N-H3 — publish refuses to overwrite without flag |
| `test_publish_symlink_unsupported_filesystem` | same | A-M1 — symlink failure path |
| `test_publish_path_missing` | same | publish path required when mode != none |
| `test_publish_mode_case_sensitive` | same | WH-M1 — case-sensitivity enforced |
| `test_publish_log_schema` | same | H-M2 — JSONL schema validation |
| `test_match_priority` | same | A-H2 — explicit > cwd > branch > slug > bootstrap |
| `test_multi_prd_soft_cap_warning` | same | WH-H3 — 5+ PRDs in a release emits warning |
| `test_build_request_version_present` / `_unknown_halts` | same | NW-M1 — BUILD_REQUEST version handshake |
| `test_legacy_option_migrate_manually` / `_finish_in_legacy` / `_start_fresh` | same | C-M2/WH-M2 — legacy 3-option subcases |
| `test_variable_schema_sync` | same | F-H1 — schema parity across SKILL.md, build-request-template.md, operational-guidance.md |

### 8.2 Integration Tests

> **(CR-M2)** Static checks use Python `re.search` over `pathlib.Path.read_text()` rather than shell `grep` (BSD/GNU portability).

| Test | Validates |
|------|-----------|
| `test_static_no_tasks_path_in_skill` | Python `re.search(r'\.dev/tasks/to-do/', file_text)` returns 0 hits across `src/superclaude/skills/prd/**/*.md`, EXCEPT inside the explicitly labelled "Legacy task folders (read-only)" subsection (detected by surrounding heading regex) |
| `test_static_no_docs_product_writes` | Python `re.search(r'docs/docs-product/')` returns 0 hits in write-site instructions; example/discovery references allowed and tagged |
| `test_make_verify_sync` | `make verify-sync` passes after edits |
| `test_end_to_end_lightweight_tier` | Full Lightweight-tier run end-to-end; all 17 artifact classes land in PRD_WORKSPACE |
| `test_concurrent_dev_no_collision` | **(CR-H2)** Two parallel `subprocess.Popen` invocations of the skill against distinct release+slug combinations complete without overlap on any file write |
| `test_multi_prd_same_release` | Two PRD slugs in the same release; no collision; soft-cap warning emitted on the 5th PRD |

### 8.3 Manual / E2E Tests

| Scenario | Steps | Expected Outcome |
|----------|-------|-----------------|
| First PRD in a fresh release | `cd` to repo root, invoke `/prd` with a new product and no existing release | Skill prompts for bootstrap; user accepts; `.dev/releases/backlog/<slug>/prd-workspace/<slug>/` is created and populated |
| PRD inside existing release | `cd` to `.dev/releases/current/<name>/`, invoke `/prd` | Skill auto-infers release; no bootstrap prompt |
| Concurrent dev simulation | Two terminal sessions, two distinct releases, invoke `/prd` simultaneously | No file collisions; both runs complete independently |
| Publish opt-in | Complete a PRD with PUBLISH_MODE=copy and PUBLISH_PATH=`docs/docs-product/tech/foo/PRD_FOO.md` | Canonical AND publish copy both exist; task log records publish event |
| Legacy folder detection | Pre-create a `.dev/tasks/to-do/TASK-PRD-20260101-000000/` with matching slug, invoke `/prd` | Skill detects, prompts, does NOT touch the legacy folder |

### 8.4 Test Infrastructure

> **(CR-H1)** Tests for path resolution require a controlled filesystem. The following fixtures are MANDATORY and live in `tests/skills/conftest.py`:

| Fixture | Provides | Used by |
|---------|----------|---------|
| `prd_repo` (factory) | A `tmp_path`-based pytest fixture that materialises a minimal IronClaude repo skeleton: `pyproject.toml` with `[tool.superclaude]`, `.dev/README.md`, `.dev/releases/` empty tree. Returns the repo root `Path`. | All resolution and containment tests |
| `release_factory(prd_repo, bucket, name)` | Creates `.dev/releases/<bucket>/<name>/` under `prd_repo` and returns its absolute `Path`. Optional kwarg `with_prd_workspace=<slug>` materialises `prd-workspace/<slug>/` with empty subdirs. | Tests that need pre-existing releases (multi-match, half-bootstrap, etc.) |
| `legacy_task_factory(prd_repo, slug)` | Creates `.dev/tasks/to-do/TASK-PRD-<timestamp>-<slug>/` with a stub task file. | Legacy probe tests |
| `non_interactive_env(monkeypatch)` | Sets `IRONCLAUDE_NON_INTERACTIVE=1`, redirects stdin to a closed file. | Non-interactive mode tests |
| `mock_user_consent(monkeypatch, answer)` | Patches the consent-prompt input function to return `answer` ('bootstrap' / 'specify' / 'cancel' / etc.). | Interactive prompt tests |

**(CR-L1) Coverage target:** branch coverage ≥ 85% on the resolution module (`src/superclaude/skills/prd/_resolution.py` or wherever the resolver lands); enforced via `--cov-fail-under=85` flag in the test command.

## 9. Migration & Rollout

- **Breaking changes**:
  - **Yes for in-flight task folders.** Any partially-completed PRD under `.dev/tasks/to-do/TASK-PRD-*/` will be detected but not auto-migrated. Users must either (a) finish the in-flight PRD manually using the legacy path, or (b) start a fresh run in the new release-workspace location.
  - **No for completed PRDs.** Previously published PRDs in `docs/docs-product/tech/...` remain valid and discoverable.
- **Backwards compatibility**:
  - `TASK_DIR` name retained as an alias for `PRD_WORKSPACE` so refs templates and agent prompts that reference `${TASK_DIR}` continue working with zero changes to subagent code.
  - Legacy `.dev/tasks/to-do/TASK-PRD-*/` folders are read-only references; SKILL.md adds a "Legacy task folders" subsection explaining the transition.
  - Variable names `${RESEARCH_DIR}`, `${SYNTHESIS_DIR}`, `${QA_DIR}`, `${REVIEWS_DIR}` are unchanged — only their resolved values move.
- **Rollback plan**:
  - All edits are confined to `src/superclaude/skills/prd/` + sync to `.claude/skills/prd/`. A single `git revert` of the merge commit restores the prior behaviour.
  - No data migration is performed, so rollback never strands artifacts.
  - Test fixture artifacts (under `tests/`) can be removed independently if test file conflicts arise.
- **(N-H2) Half-bootstrapped release cleanup**: If Stage A.0 step 5a bootstrapped a release (creating `.dev/releases/<bucket>/<slug>/README.md`) and the user subsequently cancelled before any PRD workspace artifacts were written, the stub release directory remains on disk. The skill MUST NOT auto-delete it (preserves user agency, mirrors legacy-folder discipline). A new validation step in `validation-checklists.md` Step 12 surfaces empty stub releases at PRD completion time so the developer can decide to keep or remove them. A future release-hygiene workflow (out of scope here) MAY add an explicit `superclaude release prune` command.
- **(G-M1) Pre-implementation sign-off**: This refactor touches three implicit interface owners — the orchestrator (SKILL.md), the builder (`rf-task-builder`), and the downstream consumer (`/task` skill). Pre-merge, at least one maintainer from each surface MUST review the spec. Sign-off is recorded in the merge-commit body.

## 10. Downstream Inputs

### For sc:roadmap

This containment change provides a single workstream theme:
- **Theme**: PRD Skill Artifact Containment Refactor
- **Milestone 1**: Path resolution + variable block (FR-PRD-CONTAIN.1, .2) — SKILL.md + build-request-template.md
- **Milestone 2**: Containment invariant + agent path discipline (FR-PRD-CONTAIN.3) — refs/operational-guidance.md, refs/agent-prompts.md, refs/validation-checklists.md
- **Milestone 3**: Resumability + legacy detection (FR-PRD-CONTAIN.4)
- **Milestone 4**: Opt-in publish + sources-archive (FR-PRD-CONTAIN.5, .6)
- **Milestone 5**: Tests + sync + lint (FR-PRD-CONTAIN.7 acceptance evidence)

### For sc:tasklist

Task breakdown guidance (Sprint CLI tier classification):
- **Tier 1 (mechanical edits)**: SKILL.md path/variable edits, refs/* path updates, `make sync-dev`
- **Tier 2 (substantive design)**: Stage A.0 algorithm authoring, Phase-7 publish-step prose, legacy-detection prompt UX
- **Tier 3 (validation)**: Test suite authoring, manual E2E run, lint/sync gates
Estimated total: ~12 sub-tasks across 5 milestones; parallelisable except for milestone 1 (variable block must land first).

## 11. Open Items

| Item | Question | Impact | Resolution Target |
|------|----------|--------|-------------------|
| OQ-1 | Should bootstrap default to `backlog/` or `current/`? | Determines default placement of new releases | **RESOLVED**: `backlog/` (recorded in §2.1 Key Design Decisions) |
| OQ-2 | Should there be a `--strict-containment` flag that forbids the `docs/` publish step entirely? | Strict-mode users want zero `docs/` writes ever | Post-MVP enhancement; not in this release |
| OQ-3 | Should a `scripts/migrate_prd_legacy.py` helper be authored alongside this change? | Improves UX for users mid-flight on legacy paths | Out of scope for this release; track as follow-up |
| OQ-4 | Should we add a pre-edit hook that rejects writes to `.dev/tasks/to-do/TASK-PRD-*/`? | Defensive enforcement; mirrors skill-creator hook in `.claude/settings.json` | Post-MVP; track as follow-up |
| OQ-5 | Slug normalisation rule for `PRD_SLUG_UPPER` | Filename aesthetics | **RESOLVED**: uppercase with `-` preserved (recorded in §2.1) |
| OQ-6 | What is the upper bound on slug-reverse-lookup latency at realistic release counts (N=100, N=1000)? Should NFR-CONTAIN.2 add a measurement-tier breakdown? | Performance scaling under release proliferation | Post-MVP; measure after first 6 months of usage (N-M1) |
| OQ-7 | When should the `TASK_DIR` alias be removed (clean rename in refs/* templates)? | Removes referential ambiguity for good (Fowler F-C1) | Target v4.4.0; track as follow-up release (NW-M2) |
| OQ-8 | Should an `IRONCLAUDE_DEFAULT_BUCKET` env var override the bootstrap default? | Power-user ergonomics for teams that prefer `current/` by default | Post-MVP; not in this release (K-M2) |
| OQ-9 | Empty release stub cleanup: should `superclaude release prune` ship in a follow-up release? | Operational hygiene for cancelled bootstraps | Post-MVP; tracked alongside OQ-3 (K-L1) |

## 12. Brainstorm Gap Analysis

| Gap ID | Description | Severity | Affected Section | Persona |
|--------|-------------|----------|-----------------|---------|
| BG-1 | Brainstorm did not address whether `RELEASE_NAME` validation should be enforced by the skill or assumed correct from existing release tree | Low | FR-PRD-CONTAIN.2 | architect |
| BG-2 | Brainstorm did not specify what happens if the resolved release has `prd-workspace/<slug>/` already populated from a different product (slug collision across products) | Medium | FR-PRD-CONTAIN.2 / OQ-5 | analyzer |
| BG-3 | Brainstorm did not address Windows path separators (skill uses POSIX `/`) | Low | Section 4.6 | devops |
| BG-4 | Brainstorm did not address skill behaviour when `.dev/releases/` itself does not exist OR when CWD is outside an IronClaude project | **Medium** (raised from Low per spec-panel N-C1 CRITICAL finding) | FR-PRD-CONTAIN.1 | qa |

Mitigation summary: BG-1 + BG-2 covered by FR-PRD-CONTAIN.2 acceptance criteria (slug regex + reserved-words list + multi-match prompt + match priority rule). BG-3 deferred — IronClaude is POSIX-first per existing convention. BG-4 mitigated by Stage A.0 step 0 CWD precondition guard (rejects foreign repos) plus bootstrap step 5a using `mkdir -p` (idempotent parent creation) with post-bootstrap re-resolve.

---

## Appendix A: Glossary

| Term | Definition |
|------|-----------|
| Release folder | `.dev/releases/<bucket>/<release-name>/` — the canonical home for all artifacts produced for a release |
| PRD workspace | `${RELEASE_PATH}prd-workspace/<slug>/` — the per-PRD sub-tree inside a release; replaces the legacy `.dev/tasks/to-do/TASK-PRD-*/` |
| Canonical PRD | The release-internal copy of the final PRD at `${PRD_CANONICAL_PATH}` — the authoritative deliverable |
| Publish copy | An optional copy or symlink of the canonical PRD at a user-supplied `${PUBLISH_PATH}` under `docs/` |
| Bucket | One of `backlog \| current \| complete` (the three lifecycle states of a release) |
| Slug | A kebab-case identifier matching `^[a-z0-9][a-z0-9-]*$`; used for both release names and PRD product slugs |
| TASK_DIR | Legacy variable name retained as an alias for `PRD_WORKSPACE` to minimise refs/ template churn |
| Bootstrap | The user-consented creation of a new release folder when no existing release matches the PRD scope |
| Legacy task folder | A `.dev/tasks/to-do/TASK-PRD-YYYYMMDD-HHMMSS/` folder predating this refactor; treated as read-only |

## Appendix B: Reference Documents

| Document | Relevance |
|----------|-----------|
| `.dev/releases/backlog/prd-artifact-containment/prd-artifact-index.md` | Pre-change inventory of all path references and artifact write sites |
| `src/superclaude/skills/prd/SKILL.md` | Primary edit target — orchestrator entry point |
| `src/superclaude/skills/prd/refs/build-request-template.md` | Primary edit target — BUILD_REQUEST payload |
| `src/superclaude/skills/prd/refs/operational-guidance.md` | Secondary edit target — artifact table + session mgmt |
| `src/superclaude/skills/prd/refs/validation-checklists.md` | Secondary edit target — Step 11 archive path |
| `src/superclaude/skills/prd/refs/agent-prompts.md` | Secondary edit target — agent placeholder discipline |
| `/config/workspace/IronClaude/CLAUDE.md` | Project rule: artifact containment + skill-creator override convention (mirrors the `prd-workspace/<slug>/` design) |
| `/config/workspace/IronClaude/.dev/README.md` | Canonical "where things go" convention (referenced in CLAUDE.md Plugin Override) |
| `src/superclaude/examples/prd_template.md` | Read-only PRD schema (untouched by this refactor) |
