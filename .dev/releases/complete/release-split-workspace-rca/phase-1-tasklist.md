# Phase 1 -- Pre-flight & Discoverability

**Phase Goal:** Land zero-risk docs/config so subsequent milestones can cite a published convention. These deliverables are pure docs/config edits with no runtime behavior change; their presence is a prerequisite for the M2 error message (DEP-001) and the M3 CLAUDE.md addendum to reference an authoritative source.

### T01.01 -- Create `.dev/README.md` documenting `.dev/` subdirectory conventions

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | Publish the convention that workspaces, fixtures, harness code, and iteration outputs live under `.dev/`, never under `.claude/skills/`; `.dev/eval-workspaces/<skill-name>/` is the canonical workspace location. Sourced from FR-L2.4. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0001/spec.md`
- `TASKLIST_ROOT/artifacts/D-0001/notes.md`
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md`

**Deliverables:**
- `.dev/README.md` enumerating `.dev/` subdirectories (`releases/`, `eval-workspaces/`, etc.) with the explicit rule: *"Workspaces, fixtures, harness code, and iteration outputs go under `.dev/`, never under `.claude/skills/`. Eval workspaces use `.dev/eval-workspaces/<skill-name>/`."*

**Steps:**
1. **[PLANNING]** Load context: read existing top-level `.dev/` directory listing and identify all subdirectories that need to be documented.
2. **[PLANNING]** Confirm there is no pre-existing `.dev/README.md` (or capture current contents to merge).
3. **[EXECUTION]** Author `.dev/README.md` listing each subdirectory and its purpose; include the explicit workspace-location rule verbatim from FR-L2.4.
4. **[EXECUTION]** Cross-reference the convention from the rule into the file's opening summary so the convention is the first thing a reader encounters.
5. **[VERIFICATION]** Sanity check: open `.dev/README.md` and confirm the FR-L2.4 rule appears verbatim and the subdirectory list matches the actual filesystem.
6. **[COMPLETION]** Record evidence path under `TASKLIST_ROOT/artifacts/D-0001/evidence.md` and link the produced file.

**Acceptance Criteria:**
- File `.dev/README.md` exists at repository root and contains the FR-L2.4 workspace-location rule verbatim.
- Every existing subdirectory of `.dev/` is enumerated with a 1-line purpose statement.
- Document is committed in the same change-set that introduces it (no orphan staging).
- A reference link to `.dev/README.md` is recorded in `TASKLIST_ROOT/artifacts/D-0001/evidence.md`.

**Validation:**
- Manual check: reviewer confirms `.dev/README.md` text contains the verbatim FR-L2.4 rule and an enumeration of subdirectories.
- Evidence: linkable artifact produced (the `.dev/README.md` path captured in `evidence.md`).

**Dependencies:** None
**Rollback:** Delete `.dev/README.md` (no other files depend on it until M2 lands).
**Notes:** Tier set to LIGHT per operational override (Generation Notes): docs creation, low risk, sanity-check sufficient. R-03 (prior `.dev/releases/complete/v2.15-cli-portify/` divergence) is *resolved* by this file -- D1.1 publishes the new convention; forward-only.

---

### T01.02 -- Repair broken `PLANNING.md`/`TASK.md` pointers in CLAUDE.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | Remove dangling references to `PLANNING.md` and `TASK.md` in `/config/workspace/IronClaude/CLAUDE.md` (lines 51-53 and 225-227). Per roadmap pre-decision (resolves self-review TOP CONCERN): remove rather than stub. `KNOWLEDGE.md` stays. Sourced from FR-L2.5. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0002/spec.md`
- `TASKLIST_ROOT/artifacts/D-0002/notes.md`
- `TASKLIST_ROOT/artifacts/D-0002/evidence.md`

**Deliverables:**
- Edited `/config/workspace/IronClaude/CLAUDE.md`: the project-structure block's three-line listing replaced with `KNOWLEDGE.md` only; the two corresponding lines in "Key Documentation Files" section removed.

**Steps:**
1. **[PLANNING]** Open `/config/workspace/IronClaude/CLAUDE.md` and locate the project-structure block (lines 51-53) and "Key Documentation Files" section (lines 225-227).
2. **[PLANNING]** Confirm `KNOWLEDGE.md` exists at repository root; confirm `PLANNING.md` and `TASK.md` do not exist.
3. **[EXECUTION]** Delete the `PLANNING.md` and `TASK.md` lines from the project-structure listing, retaining only the `KNOWLEDGE.md` line.
4. **[EXECUTION]** Delete the two corresponding `PLANNING.md` and `TASK.md` rows from the "Key Documentation Files" section.
5. **[VERIFICATION]** Run `grep -E 'PLANNING\.md|TASK\.md' /config/workspace/IronClaude/CLAUDE.md` and confirm no matches.
6. **[COMPLETION]** Record the diff and `grep` exit status in `TASKLIST_ROOT/artifacts/D-0002/evidence.md`.

**Acceptance Criteria:**
- `grep -E 'PLANNING\.md|TASK\.md' /config/workspace/IronClaude/CLAUDE.md` exits with status 1 (no matches).
- `grep 'KNOWLEDGE\.md' /config/workspace/IronClaude/CLAUDE.md` exits with status 0 (preserved reference) and `KNOWLEDGE.md` exists on disk.
- Edits scoped to the two location ranges identified in the roadmap (line refs as of roadmap authoring: 51-53 and 225-227; match by content -- the `PLANNING.md`/`TASK.md` references -- not by line number); no other CLAUDE.md content modified.
- Diff captured in `TASKLIST_ROOT/artifacts/D-0002/evidence.md`.

**Validation:**
- Manual check: reviewer scans CLAUDE.md and confirms the project-structure block lists only `KNOWLEDGE.md` and the "Key Documentation Files" section no longer references `PLANNING.md` or `TASK.md`.
- Evidence: linkable artifact produced (the diff captured in `evidence.md`).

**Dependencies:** None
**Rollback:** Restore previous CLAUDE.md from git history.
**Notes:** Roadmap pre-decision is REMOVE not STUB: rationale -- restoring empty stubs is worse than removing dangling references. Future contributor can re-add at the time `PLANNING.md`/`TASK.md` actually exist.

---

### T01.03 -- Append `.claude/skills/*-workspace/` to `.gitignore`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-003 |
| Why | Defense against the case where every other layer fails: future misplacement under `.claude/skills/<X>-workspace/` should not get committed. Sourced from FR-L2.6. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0003 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0003/spec.md`
- `TASKLIST_ROOT/artifacts/D-0003/notes.md`
- `TASKLIST_ROOT/artifacts/D-0003/evidence.md`

**Deliverables:**
- An appended `.gitignore` entry matching `.claude/skills/*-workspace/` (directory suffix `-workspace`), with a short comment explaining the rationale and linking to `.dev/README.md`.

**Steps:**
1. **[PLANNING]** Open `.gitignore` at repository root and locate an appropriate section (or end of file).
2. **[PLANNING]** Confirm no existing pattern already matches `.claude/skills/*-workspace/` to avoid duplicate entries.
3. **[EXECUTION]** Append a commented pattern line: `# Skill eval workspaces must live in .dev/eval-workspaces/ -- see .dev/README.md` followed by `.claude/skills/*-workspace/`.
4. **[VERIFICATION]** Create a throwaway `.claude/skills/_probe-workspace/` directory locally and confirm `git status` lists it as untracked AND `git check-ignore .claude/skills/_probe-workspace/` exits 0 (ignored).
5. **[VERIFICATION]** Confirm that a legitimate skill directory (e.g., `.claude/skills/sc-tasklist-protocol/`) is NOT matched by the new pattern via `git check-ignore`.
6. **[COMPLETION]** Remove the probe directory and record evidence (commands and exit statuses) in `TASKLIST_ROOT/artifacts/D-0003/evidence.md`.

**Acceptance Criteria:**
- File `.gitignore` contains the literal pattern `.claude/skills/*-workspace/` (or equivalent gitignore syntax).
- `git check-ignore .claude/skills/_probe-workspace/` exits 0 for a workspace-suffixed path.
- `git check-ignore .claude/skills/sc-tasklist-protocol/` does NOT match the new pattern (existing skills remain tracked).
- Probe commands and outputs captured in `TASKLIST_ROOT/artifacts/D-0003/evidence.md`.

**Validation:**
- Manual check: reviewer confirms `.gitignore` diff and the `git check-ignore` probe results.
- Evidence: linkable artifact produced (`evidence.md` with command outputs).

**Dependencies:** None
**Rollback:** Remove the appended pattern from `.gitignore`.
**Notes:** Pattern precision is the same as the M3 hook's matching rule (`*-workspace/` directory suffix, not single-file `workspace.md`).

---

### T01.04 -- Checkpoint: End of Phase 1

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002, R-003 |
| Why | Gate: verify outputs of tasks T01.01-T01.03 before continuing to Phase 2 (Detection Gate), which depends on the convention published by D1.1 (DEP-001). |
| Effort | XS |
| Risk | Low |
| Risk Drivers | None |
| Tier | LIGHT |
| Confidence | [██████████] 100% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Quick sanity check |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-CP01 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P01-END.md`

**Purpose:** Confirm `.dev/README.md`, CLAUDE.md pointer repair, and `.gitignore` entry are all in place so M2 can cite the convention.

**Verification:** (exactly 3 bullets)
- `.dev/README.md` exists and contains the FR-L2.4 rule (output of T01.01).
- CLAUDE.md no longer references `PLANNING.md` or `TASK.md` (output of T01.02).
- `.gitignore` matches `.claude/skills/*-workspace/` directories (output of T01.03).

**Exit Criteria:** (exactly 3 bullets)
- All three Phase 1 deliverables (D-0001, D-0002, D-0003) have evidence files under `TASKLIST_ROOT/artifacts/`.
- No CRITICAL severity findings logged against any Phase 1 task.
- DEP-001 satisfied: Phase 2's D2.1 error-message draft can cite `.dev/README.md` as the source of truth for the redirect destination.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present on disk.
2. **[VERIFICATION]** Re-run the LIGHT-tier sanity checks (file exists; grep returns expected) for T01.01-T01.03.
3. **[VERIFICATION]** Write the checkpoint report to `TASKLIST_ROOT/checkpoints/CP-P01-END.md`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P01-END.md` exists and contains `Overall: Pass`.
- All 3 Verification bullets are confirmed in the report.
- All 3 Exit Criteria bullets are met and documented in the report.
- Checkpoint report enumerates task IDs T01.01, T01.02, T01.03.

**Validation:**
- Manual check: reviewer confirms the report at `TASKLIST_ROOT/checkpoints/CP-P01-END.md`.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.01, T01.02, T01.03
**Rollback:** N/A (checkpoints are read-only verifications)
