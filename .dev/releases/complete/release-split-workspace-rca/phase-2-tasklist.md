# Phase 2 -- Detection Gate (Priority-0)

**Phase Goal:** Convert the existing-but-dormant misplacement detection logic into an enforcing CI gate. Closes INV-002 HIGH-severity unaddressed invariant. Sequencing within phase: D2.1 -> D2.2 -> D2.3 -- the CI gate flips on last so the first PR-blocking failure exhibits the correct message and blocklist.

### T02.01 -- Replace Makefile verify-sync error message with context-aware variant

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004 |
| Why | Replace the misleading `Makefile:179-187` error `"MISSING in src/superclaude/skills/: <name> (not distributable!)"` with a context-aware variant that, when the missing entry has no SKILL.md, emits: *"<name> has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/<name>/."* Sourced from FR-L2.1. |
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
| Deliverable IDs | D-0004 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0004/spec.md`
- `TASKLIST_ROOT/artifacts/D-0004/notes.md`
- `TASKLIST_ROOT/artifacts/D-0004/evidence.md`

**Deliverables:**
- Edited `Makefile` lines 179-187 (verify-sync target) with context-aware messaging: branch on whether the missing entry has `SKILL.md` and emit the appropriate redirect.
- A short test fixture (synthetic directory) that exercises both branches.

**Steps:**
1. **[PLANNING]** Read `Makefile:179-187` to capture the current verify-sync logic and message format.
2. **[PLANNING]** Confirm that `.dev/README.md` (output of T01.01) is in place so the redirect destination can be cited authoritatively.
3. **[EXECUTION]** Update the verify-sync target to detect "missing entry without SKILL.md" and emit the new message: *"<name> has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/<name>/."*
4. **[EXECUTION]** Preserve the original message for the legitimate case (entry has SKILL.md but is missing from `src/superclaude/skills/`).
5. **[VERIFICATION]** Create a throwaway `.claude/skills/_probe-workspace/` (no SKILL.md), run `make verify-sync`, and confirm the new message appears verbatim; exit status non-zero.
6. **[VERIFICATION]** Create a throwaway `.claude/skills/_probe/SKILL.md` and confirm the original "MISSING in src/superclaude/skills/" message still triggers for the legitimate case.
7. **[COMPLETION]** Remove probe directories; capture both `make verify-sync` outputs in `TASKLIST_ROOT/artifacts/D-0004/evidence.md`.

**Acceptance Criteria:**
- `make verify-sync` against a probe `.claude/skills/_probe-workspace/` without SKILL.md emits the verbatim message `<name> has no SKILL.md — not a skill, must not live in .claude/skills/. Move to .dev/eval-workspaces/<name>/.` (em-dash exact) and exits non-zero.
- `make verify-sync` against a probe `.claude/skills/_probe/` WITH a SKILL.md still emits the original `MISSING in src/superclaude/skills/` message for that case (no regression).
- Makefile edit is scoped to the verify-sync target (lines 179-187); no unrelated targets modified.
- Probe outputs (both cases) captured in `TASKLIST_ROOT/artifacts/D-0004/evidence.md`.

**Validation:**
- Manual check: reviewer runs `make verify-sync` against both probe scenarios.
- Evidence: linkable artifact produced (`evidence.md` containing the two captured outputs).

**Dependencies:** T01.01 (DEP-001: error message must cite `.dev/README.md` convention).
**Rollback:** Revert the Makefile change via `git checkout -- Makefile`.
**Notes:** Tier set to STANDARD per operational override; pattern logic in Makefile warrants test execution rather than sanity check alone.

---

### T02.02 -- Add `*-workspace` suffix blocklist to verify-sync (or lint-architecture)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-005 |
| Why | Add an explicit blocklist for directories suffixed `-workspace` under `.claude/skills/` with the message *"Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`."* Either `verify-sync` or `lint-architecture` is acceptable per roadmap; deterministic choice below. Sourced from FR-L2.3. |
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
| Deliverable IDs | D-0005 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0005/spec.md`
- `TASKLIST_ROOT/artifacts/D-0005/notes.md`
- `TASKLIST_ROOT/artifacts/D-0005/evidence.md`

**Deliverables:**
- A blocklist rule in `Makefile` (target: `lint-architecture` by Section 4.9 tie-breaker rule 4 -- reversible and changes fewest existing interfaces) that fails when any directory matches `.claude/skills/*-workspace/` regardless of its SKILL.md presence.
- Explicit error message text containing the verbatim string from FR-L2.3.

**Steps:**
1. **[PLANNING]** Inspect existing `lint-architecture` target (if present) or `verify-sync` target to choose insertion site per the deterministic tie-breaker.
2. **[PLANNING]** Confirm the new check does not duplicate the T02.01 logic (T02.01 fires only for missing-SKILL.md cases; this check fires unconditionally on `*-workspace/` suffix).
3. **[EXECUTION]** Add the blocklist rule emitting verbatim: *"Workspace directories belong under `.dev/eval-workspaces/`, not `.claude/skills/`."*
4. **[EXECUTION]** Ensure the rule exits non-zero so CI (Phase 2 T02.03) will block the PR.
5. **[VERIFICATION]** Run `make lint-architecture` (or whichever target was chosen) with a probe `.claude/skills/_probe-workspace/` directory and confirm the new message appears verbatim; exit status non-zero.
6. **[VERIFICATION]** Run the same target on a clean tree and confirm exit status 0 (no false positives).
7. **[COMPLETION]** Remove probe; capture outputs in `TASKLIST_ROOT/artifacts/D-0005/evidence.md`.

**Acceptance Criteria:**
- `make lint-architecture` (or chosen target) with a probe `*-workspace/` directory emits the verbatim message `Workspace directories belong under \`.dev/eval-workspaces/\`, not \`.claude/skills/\`.` and exits non-zero.
- Clean-tree run exits 0 with no `*-workspace` references.
- Choice of target (verify-sync vs lint-architecture) documented in `TASKLIST_ROOT/artifacts/D-0005/notes.md` with the Section 4.9 tie-breaker rationale.
- Probe outputs (both passing and failing cases) captured in `TASKLIST_ROOT/artifacts/D-0005/evidence.md`.

**Validation:**
- Manual check: reviewer runs the chosen target against both probe scenarios.
- Evidence: linkable artifact produced (`evidence.md` containing the two captured outputs).

**Dependencies:** T02.01 (sequencing within M2: D2.1 -> D2.2 -> D2.3).
**Rollback:** Remove the blocklist rule from the Makefile target.
**Notes:** Section 4.9 tie-breaker applied: lint-architecture chosen over verify-sync to avoid coupling architectural linting with sync verification (rule 4: fewest interface changes). Recorded per protocol. Tie-breaker rationale inline: `lint-architecture` is the dedicated architectural-rules target while `verify-sync` is sync-verification. Coupling architectural linting with sync verification would change two interfaces; using `lint-architecture` changes one.

---

### T02.03 -- Wire `make verify-sync` + `make lint-architecture` into `.github/workflows/quick-check.yml`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-006 |
| Why | Convert detection from opt-in to enforcing. Closes INV-002 HIGH-severity unaddressed invariant. PRs must fail on drift before merge. Sourced from FR-L2.2. |
| Effort | M |
| Risk | Low |
| Risk Drivers | ci (cross-cutting via the `ci` keyword) |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0006 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0006/spec.md`
- `TASKLIST_ROOT/artifacts/D-0006/notes.md`
- `TASKLIST_ROOT/artifacts/D-0006/evidence.md`

**Deliverables:**
- Edits to `.github/workflows/quick-check.yml` invoking `make verify-sync` and `make lint-architecture` as required jobs, configured to fail the workflow on non-zero exit.
- A synthetic test PR (or local act run / scripted simulation) demonstrating the gate fails on a `.claude/skills/<X>-workspace/` directory without SKILL.md.

**Steps:**
1. **[PLANNING]** Read `.github/workflows/quick-check.yml` to identify the insertion point and confirm the existing structure (steps, runs-on, matrix).
2. **[PLANNING]** Confirm T02.01 and T02.02 have landed (otherwise the gate would emit the OLD misleading message).
3. **[EXECUTION]** Add a step (or job) running `make verify-sync && make lint-architecture` with explicit `if: always()` semantics consistent with the rest of the workflow.
4. **[EXECUTION]** Note (out of task scope): branch-protection / required-check configuration is repo-admin scoped. If it is not already configured for this workflow, record a follow-up request in `notes.md` for repo admins; the workflow's non-zero-exit behaviour is the in-scope deliverable.
5. **[VERIFICATION]** Open a synthetic PR introducing `.claude/skills/_probe-workspace/` (no SKILL.md) and confirm the workflow fails with the verbatim message from T02.01 or T02.02.
6. **[VERIFICATION]** Confirm a clean PR (no `*-workspace/` directories) passes the workflow.
7. **[COMPLETION]** Capture workflow log URLs (or local act outputs) in `TASKLIST_ROOT/artifacts/D-0006/evidence.md`.

**Acceptance Criteria:**
- `.github/workflows/quick-check.yml` invokes `make verify-sync` and `make lint-architecture` in a job that fails the workflow on non-zero exit.
- A synthetic PR with `.claude/skills/_probe-workspace/` (no SKILL.md) shows the workflow failing with the message from T02.01 or T02.02.
- A clean PR passes the workflow.
- A failing required workflow status equates to a blocked merge under this repo's standard merge policy (evidence: workflow run + PR `mergeable=false` in the GitHub API), OR a repo-admin follow-up note recorded in `notes.md` if branch protection is not yet configured.
- Workflow run URLs (or local-act log paths) captured in `TASKLIST_ROOT/artifacts/D-0006/evidence.md`.

**Validation:**
- Manual check: reviewer opens the synthetic PR and confirms workflow failure message matches T02.01/T02.02 verbatim outputs.
- Evidence: linkable artifact produced (`evidence.md` containing workflow run URLs or local-act logs).

**Dependencies:** T02.01, T02.02 (sequencing within M2: D2.1 -> D2.2 -> D2.3).
**Rollback:** Revert `.github/workflows/quick-check.yml` to its prior version.
**Notes:** R-02 (CI runtime impact) is Low/Low -- `make verify-sync` and `make lint-architecture` run in seconds and can run concurrently with existing checks. Branch protection requirement (required-check) is repo-admin scoped; if blocked, evidence.md should record the request.

---

### T02.04 -- Checkpoint: End of Phase 2

| Field | Value |
|---|---|
| Roadmap Item IDs | R-004, R-005, R-006 |
| Why | Gate: verify the detection chain (D2.1 + D2.2 + D2.3) is enforcing before Phase 3 begins. M3 hook + addendum carry less risk only after this CI gate is detecting bypass cases (DEP-002). |
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
| Deliverable IDs | D-CP02 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-END.md`

**Purpose:** Confirm the Makefile messaging and CI wiring are in place and demonstrably block a drift PR; closes INV-002.

**Verification:** (exactly 3 bullets)
- Makefile verify-sync emits the new context-aware message when SKILL.md is absent (output of T02.01).
- Makefile lint-architecture (or chosen target) emits the `*-workspace` blocklist message (output of T02.02).
- `.github/workflows/quick-check.yml` invokes both Makefile targets and fails the synthetic probe PR (output of T02.03).

**Exit Criteria:** (exactly 3 bullets)
- D-0004, D-0005, D-0006 have evidence files captured under `TASKLIST_ROOT/artifacts/`.
- INV-002 marked closed in the checkpoint report (synthetic PR demonstrably blocked).
- Phase 3 may begin: hooks + CLAUDE.md addendum can rely on CI catching any bypass.

**Steps:**
1. **[VERIFICATION]** Confirm each Verification bullet artifact is present.
2. **[VERIFICATION]** Re-run `make verify-sync` and `make lint-architecture` on a clean tree (expect exit 0) and against the workspace probe (expect exit non-zero).
3. **[VERIFICATION]** Write the checkpoint report to `TASKLIST_ROOT/checkpoints/CP-P02-END.md` including the synthetic PR URL or local-act evidence.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P02-END.md` exists and contains `Overall: Pass` and an explicit `INV-002: CLOSED` line.
- All 3 Verification bullets confirmed.
- All 3 Exit Criteria bullets met.
- Checkpoint report enumerates task IDs T02.01, T02.02, T02.03.

**Validation:**
- Manual check: reviewer confirms the report at `TASKLIST_ROOT/checkpoints/CP-P02-END.md` and the cited synthetic-PR/log evidence.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.01, T02.02, T02.03
**Rollback:** N/A (checkpoints are read-only verifications)
