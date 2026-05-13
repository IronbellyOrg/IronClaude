# Phase 3 -- Occurrence Prevention

**Phase Goal:** Stop the misplacement at write time without depending on Claude obedience. Hook + project rule + convenience target make the correct destination the path of least resistance and the wrong destination unwritable. Pattern precision (R-01) is the central risk: hook must match `*-workspace/` directory suffix only, never legitimate skill files.

### T03.01 -- Add PreToolUse hook rejecting writes to `.claude/skills/*-workspace/**`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007 |
| Why | Block Write/Edit to `.claude/skills/*-workspace/**` at tool-dispatch time and emit a deny-decision message naming the correct destination `.dev/eval-workspaces/<skill-name>/<remainder>`. Pre-decision (resolves self-review Q3): semantics are *reject-with-redirect*, not transparent path rewrite -- Claude Code hooks emit deny + explanatory message and Claude retries with corrected path. Sourced from FR-L1.1. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [█████████-] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0007 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0007/spec.md`
- `TASKLIST_ROOT/artifacts/D-0007/notes.md`
- `TASKLIST_ROOT/artifacts/D-0007/evidence.md`

**Deliverables:**
- Edit to `.claude/settings.json` adding a PreToolUse hook on `Write`/`Edit` that matches the pattern `.claude/skills/*-workspace/**` and emits a deny decision with a message of the form: *"Workspace path rejected: write to `.claude/skills/<X>-workspace/<remainder>` blocked. Use `.dev/eval-workspaces/<X>/<remainder>` instead."*
- Positive AND negative test cases per merged-thesis Risk Register: confirm the hook fires on `.claude/skills/foo-workspace/file.md` but NOT on `.claude/skills/foo/file.md` and NOT on `.claude/skills/foo/workspace.md`.

**Steps:**
1. **[PLANNING]** Read existing `.claude/settings.json` and locate the `hooks` section (or schema if absent).
2. **[PLANNING]** Confirm hook syntax for PreToolUse rejection matches Claude Code's current contract (deny decision + message; no transparent path mutation).
3. **[EXECUTION]** Add the PreToolUse hook with the matcher `.claude/skills/*-workspace/**` and the redirect message naming the corrected destination.
4. **[EXECUTION]** Document the hook's *reject-with-redirect* semantics inline in `.claude/settings.json` (comment field or `description` per schema).
5. **[VERIFICATION]** Positive case: attempt `Write` to `.claude/skills/_probe-workspace/file.md`; confirm the hook rejects with the redirect message and the file is not created.
6. **[VERIFICATION]** Negative case 1: attempt `Edit` on `.claude/skills/sc-tasklist-protocol/SKILL.md`; confirm the hook does NOT fire.
7. **[VERIFICATION]** Negative case 2: attempt `Write` to `.claude/skills/_probe/workspace.md` (single-file `workspace.md`, NOT a `-workspace/` directory); confirm the hook does NOT fire.
8. **[COMPLETION]** Capture all three test outputs in `TASKLIST_ROOT/artifacts/D-0007/evidence.md`.

**Acceptance Criteria:**
- `.claude/settings.json` contains a PreToolUse hook matching `.claude/skills/*-workspace/**` for `Write` and `Edit` operations.
- Positive case: an attempted write to `.claude/skills/_probe-workspace/file.md` is rejected with a message containing the substring `.dev/eval-workspaces/`.
- Negative case 1: a write/edit to `.claude/skills/<existing-skill>/SKILL.md` proceeds without the hook firing.
- Negative case 2: a write to `.claude/skills/<X>/workspace.md` (single file, not a directory match) proceeds without the hook firing.

**Validation:**
- Manual check: reviewer runs the three probes (one positive, two negative) and confirms hook behaviour against acceptance criteria.
- Evidence: linkable artifact produced (`evidence.md` containing all three probe outputs and exit statuses).

**Dependencies:** None directly; benefits from M2 CI gate (DEP-002) so any hook bypass is detected.
**Rollback:** Remove the PreToolUse hook entry from `.claude/settings.json`.
**Notes:** R-01 (pattern precision) mitigation: both positive and negative tests are mandatory per merged-thesis Risk Register. Thesis L1.1 wording "rewrites the path" is interpreted as "names the correct path in the error message" (Claude Code hooks do not transparently mutate tool arguments).

---

### T03.02 -- Append CLAUDE.md addendum overriding skill-creator's "sibling to skill directory" convention

| Field | Value |
|---|---|
| Roadmap Item IDs | R-008 |
| Why | Provide a project-level instruction explicitly overriding skill-creator's behavior of writing eval workspaces as siblings to the skill directory. Cite behavior (not file path) to mitigate R-04: skill-creator plugin updates could rename L167, but the *convention* survives. Names the override and the destination. Sourced from FR-L1.2. |
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
| Deliverable IDs | D-0008 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0008/spec.md`
- `TASKLIST_ROOT/artifacts/D-0008/notes.md`
- `TASKLIST_ROOT/artifacts/D-0008/evidence.md`

**Deliverables:**
- Edited `/config/workspace/IronClaude/CLAUDE.md` with an explicit addendum stating: when invoking skill-creator (or any plugin that uses a sibling-workspace convention), the eval workspace MUST go to `.dev/eval-workspaces/<skill-name>/` rather than `.claude/skills/<skill-name>-workspace/`. Addendum cites *behavior* not file path so it survives skill-creator upgrades.

**Steps:**
1. **[PLANNING]** Open `/config/workspace/IronClaude/CLAUDE.md` and select an insertion site (preferably near an existing Workflow or Conventions section, or a new "Plugin Override" section).
2. **[PLANNING]** Draft the addendum prose: name the override (skill-creator's sibling-workspace convention), name the destination (`.dev/eval-workspaces/<skill-name>/`), and cite behavior rather than file paths or line numbers.
3. **[EXECUTION]** Insert the addendum with a heading such as `## Plugin Override -- Skill-Creator Workspace Destination` and exactly the destination rule.
4. **[EXECUTION]** Cross-reference `.dev/README.md` (output of T01.01) as the authoritative source for the convention.
5. **[VERIFICATION]** Re-read the addendum aloud and confirm it (a) names the override, (b) names the destination, and (c) does NOT cite a file-path or line number of the skill-creator plugin.
6. **[COMPLETION]** Capture the diff and the rendered addendum text in `TASKLIST_ROOT/artifacts/D-0008/evidence.md`.

**Acceptance Criteria:**
- `/config/workspace/IronClaude/CLAUDE.md` contains an addendum naming both the skill-creator sibling-workspace convention AND the `.dev/eval-workspaces/<skill-name>/` destination.
- Addendum does not reference `SKILL.md L167` or any other transient skill-creator file path (R-04 mitigation).
- Addendum cross-references `.dev/README.md` as the published convention.
- Diff captured in `TASKLIST_ROOT/artifacts/D-0008/evidence.md`.

**Validation:**
- Manual check: reviewer confirms the addendum mentions the override behavior and the destination, and does not embed a transient plugin file-path.
- Evidence: linkable artifact produced (`evidence.md` with the diff and rendered prose).

**Dependencies:** T01.01 (the addendum cites `.dev/README.md` as published convention).
**Rollback:** Revert the CLAUDE.md addition via `git checkout -- CLAUDE.md` or remove the inserted section.
**Notes:** R-04 mitigation -- cite behavior ("skill-creator's sibling-workspace convention") not file path. Addendum is project-level (this CLAUDE.md), not global.

---

### T03.03 -- Add `make eval-skill SKILL=<name>` target

| Field | Value |
|---|---|
| Roadmap Item IDs | R-009 |
| Why | Provide a convenience target so the correct destination is the path of least resistance: `make eval-skill SKILL=<name>` creates `.dev/eval-workspaces/<name>/` and prints the absolute path for downstream use as workspace root. Sourced from FR-L1.3. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0009 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0009/spec.md`
- `TASKLIST_ROOT/artifacts/D-0009/notes.md`
- `TASKLIST_ROOT/artifacts/D-0009/evidence.md`

**Deliverables:**
- A new `eval-skill` target in `Makefile` accepting `SKILL=<name>` that:
  1. Creates `.dev/eval-workspaces/<name>/` (idempotent: no-op if exists).
  2. Prints the absolute path of the created directory to stdout.
  3. Fails with a clear error if `SKILL` is unset.

**Steps:**
1. **[PLANNING]** Open `Makefile` and identify the section where similar convenience targets live; reserve an insertion site.
2. **[PLANNING]** Confirm `.dev/eval-workspaces/` already exists as a directory in the repo (it should, from the prior physical relocation at commit `86d2749`).
3. **[EXECUTION]** Add the `eval-skill` target with an `if [ -z "$(SKILL)" ]; then ...; fi` guard that fails when `SKILL` is unset.
4. **[EXECUTION]** Implement the target as `mkdir -p .dev/eval-workspaces/$(SKILL) && realpath .dev/eval-workspaces/$(SKILL)`.
5. **[VERIFICATION]** Run `make eval-skill SKILL=__probe__` and confirm the directory is created and the absolute path is printed to stdout.
6. **[VERIFICATION]** Run `make eval-skill` (no SKILL) and confirm a non-zero exit with a clear error message.
7. **[COMPLETION]** Remove the probe directory and capture both runs' outputs in `TASKLIST_ROOT/artifacts/D-0009/evidence.md`.

**Acceptance Criteria:**
- `make eval-skill SKILL=__probe__` creates `.dev/eval-workspaces/__probe__/` and prints the absolute path on stdout; exit status 0.
- `make eval-skill` (without `SKILL`) exits non-zero with a clear error.
- Target is idempotent: running `make eval-skill SKILL=__probe__` twice does not error.
- Both outputs captured in `TASKLIST_ROOT/artifacts/D-0009/evidence.md`.

**Validation:**
- Manual check: reviewer runs both invocations and confirms expected behavior.
- Evidence: linkable artifact produced (`evidence.md` with stdout/exit-status of both runs).

**Dependencies:** None directly; conceptually complements T03.01 (hook) by making the correct destination trivially available.
**Rollback:** Remove the `eval-skill` target from the Makefile.
**Notes:** Operational tier STANDARD per the override; behaviour test (target invocation) is the appropriate verification. Note: the unset-SKILL error case (Deliverable item 3, AC bullet 2) is operational hardening beyond roadmap D3.3's literal scope -- retained because the alternative (silent no-op) would create a confusing failure mode.

---

### T03.04 -- Checkpoint: End of Phase 3

| Field | Value |
|---|---|
| Roadmap Item IDs | R-007, R-008, R-009 |
| Why | Gate: verify L1 (occurrence-prevention) is in place before M5 entry. M5 ENTRY GATE requires no CP-M3-END CRITICAL severity findings open. |
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
| Deliverable IDs | D-CP03 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P03-END.md`

**Purpose:** Confirm hook + CLAUDE.md addendum + eval-skill convenience target are in place and demonstrably steer writes to `.dev/eval-workspaces/`.

**Verification:** (exactly 3 bullets)
- PreToolUse hook rejects `.claude/skills/*-workspace/` writes and passes negative-case probes (output of T03.01).
- CLAUDE.md addendum names the override and destination without citing transient plugin paths (output of T03.02).
- `make eval-skill SKILL=<name>` creates the correct destination and prints the absolute path (output of T03.03).

**Exit Criteria:** (exactly 3 bullets)
- D-0007, D-0008, D-0009 have evidence files captured under `TASKLIST_ROOT/artifacts/`.
- No CP-M3-END CRITICAL severity findings are open (M5 ENTRY GATE precondition).
- Phase 5 (Acceptance Validation) may proceed once Phase 4 also reaches its end-of-phase checkpoint.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present on disk.
2. **[VERIFICATION]** Re-run the three Phase 3 probes (positive hook reject, both negatives; CLAUDE.md grep; eval-skill invocation).
3. **[VERIFICATION]** Write the checkpoint report to `TASKLIST_ROOT/checkpoints/CP-P03-END.md` and explicitly assert `M5 ENTRY GATE precondition: MET`.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P03-END.md` exists and contains `Overall: Pass` and an explicit `M5 ENTRY GATE precondition: MET` line.
- All 3 Verification bullets confirmed.
- All 3 Exit Criteria bullets met.
- Checkpoint report enumerates task IDs T03.01, T03.02, T03.03.

**Validation:**
- Manual check: reviewer confirms the report at `TASKLIST_ROOT/checkpoints/CP-P03-END.md`.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T03.01, T03.02, T03.03
**Rollback:** N/A (checkpoints are read-only verifications)
