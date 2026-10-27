# Phase 4 -- Defense in Depth

**Phase Goal:** Skill-level guard for the unlikely case that a future workflow routes a `.claude/skills/...` value through `sc-release-split-protocol --output` directly, bypassing both L1 (hook) and L2 (CI gate). M4 is parallel-eligible per DEP-004 and has a SOFT dependency on M2 (DEP-005): authoring may begin before M2 lands but completion must wait for `make verify-sync` to emit correct messages.

### T04.01 -- Add output-path policy guard in sc-release-split-protocol SKILL.md

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010 |
| Why | Refuse `--output` paths under `.claude/skills/`, `.claude/agents/`, `.claude/commands/` at the skill's Prerequisites step (before any artifacts are written). Document the policy in the command Options table. Sourced from FR-L3.1. |
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
| Deliverable IDs | D-0010 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0010/spec.md`
- `TASKLIST_ROOT/artifacts/D-0010/notes.md`
- `TASKLIST_ROOT/artifacts/D-0010/evidence.md`

**Deliverables:**
- Edit to `src/superclaude/skills/sc-release-split-protocol/SKILL.md` Prerequisites (step 2a): a refusal clause for `--output` paths under `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` that aborts before any write.
- Edit to `src/superclaude/commands/release-split.md` Options table: documented policy entry naming the three forbidden prefixes and the redirect destination (`.dev/`).
- `make sync-dev` run so `.claude/skills/sc-release-split-protocol/` copy stays in sync with `src/superclaude/`.

**Steps:**
1. **[PLANNING]** Read `src/superclaude/skills/sc-release-split-protocol/SKILL.md` and locate Prerequisites step 2a (or insert one if absent).
2. **[PLANNING]** Read `src/superclaude/commands/release-split.md` Options table format.
3. **[EXECUTION]** Add the guard clause to Prerequisites step 2a: refuse `--output` paths matching `.claude/skills/`, `.claude/agents/`, or `.claude/commands/` and abort with an explanatory error citing `.dev/` as the correct destination.
4. **[EXECUTION]** Update the command Options table in `src/superclaude/commands/release-split.md` with the policy entry.
5. **[EXECUTION]** Run `make sync-dev` to update `.claude/skills/sc-release-split-protocol/SKILL.md`.
6. **[EXECUTION]** Run `make verify-sync` to confirm src/ and .claude/ are in sync (this also exercises the new M2 message if M2 has already landed -- see DEP-005 SOFT dependency).
7. **[VERIFICATION]** Invoke `sc-release-split-protocol --output .claude/skills/foo/` (dry-run if available); confirm the skill refuses BEFORE writing any artifact and emits an error naming `.dev/`.
8. **[VERIFICATION]** Invoke `sc-release-split-protocol --output .dev/releases/current/test-output/` (or equivalent legitimate path); confirm the skill proceeds normally.
9. **[COMPLETION]** Capture both invocations' outputs and the `make sync-dev` / `make verify-sync` outputs in `TASKLIST_ROOT/artifacts/D-0010/evidence.md`.

**Acceptance Criteria:**
- `src/superclaude/skills/sc-release-split-protocol/SKILL.md` Prerequisites step 2a refuses `--output` paths under `.claude/skills/`, `.claude/agents/`, `.claude/commands/`.
- `src/superclaude/commands/release-split.md` Options table contains the policy entry naming all three forbidden prefixes.
- Invoking `sc-release-split-protocol --output .claude/skills/foo/` aborts BEFORE writing any artifact and emits an error mentioning `.dev/`.
- `make verify-sync` exits 0 after `make sync-dev`.

**Validation:**
- Manual check: reviewer runs both invocations (one forbidden path, one legitimate) and confirms behavior.
- Evidence: linkable artifact produced (`evidence.md` containing both invocations plus sync-dev/verify-sync outputs).

**Dependencies:** None hard; SOFT dependency on M2 (DEP-005) -- `make verify-sync` only emits the correct error messages after D2.1 + D2.2 land. T04.01 may begin authoring before M2 completes but cannot be marked done until M2 verify-sync output is correct.
**Rollback:** Revert the SKILL.md and command-doc edits via `git checkout --`; re-run `make sync-dev`.
**Notes:** Operational tier STANDARD per override; the guard is policy logic that warrants invocation tests, not a sanity check. R-04 mitigation (cite behavior over file paths) does not apply here -- the policy lists prefixes, which is the appropriate level of specificity for an output-path guard.

---

### T04.02 -- Apply output-path policy guard to sibling skills (optional)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-011 |
| Why | Apply the same guard pattern to `sc-adversarial-protocol` and `sc-cleanup-audit-protocol` SKILL.md files for consistency. Defense-in-depth generalization. Defer until M1-M5 ship; if not done, release still ships. Sourced from FR-L3.2. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [███████---] 75% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0011 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0011/spec.md`
- `TASKLIST_ROOT/artifacts/D-0011/notes.md`
- `TASKLIST_ROOT/artifacts/D-0011/evidence.md`

**Deliverables:**
- Edits to `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` Prerequisites: the same refusal clause as T04.01.
- Edits to `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md` Prerequisites: the same refusal clause as T04.01.
- `make sync-dev` run to propagate to `.claude/skills/`.

**Steps:**
1. **[PLANNING]** Read `src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and `src/superclaude/skills/sc-cleanup-audit-protocol/SKILL.md` to locate Prerequisites sections.
2. **[PLANNING]** Confirm each skill takes an `--output` (or equivalent) argument; if a skill does not, document the skip in `TASKLIST_ROOT/artifacts/D-0011/notes.md`.
3. **[EXECUTION]** Add the same refusal clause as T04.01 (refuse `--output` paths under `.claude/skills/`, `.claude/agents/`, `.claude/commands/`) to each skill's Prerequisites.
4. **[EXECUTION]** Run `make sync-dev` and `make verify-sync`.
5. **[VERIFICATION]** Invoke each sibling skill with a forbidden `--output` (dry-run if available) and confirm refusal.
6. **[VERIFICATION]** Invoke each sibling skill with a legitimate `--output` and confirm normal operation.
7. **[COMPLETION]** Capture all invocations in `TASKLIST_ROOT/artifacts/D-0011/evidence.md`.

**Acceptance Criteria:**
- Both sibling SKILL.md files contain the refusal clause (or `notes.md` documents why a skill is exempt).
- Invocation of each sibling skill with a forbidden `--output` aborts pre-write.
- `make verify-sync` exits 0 after `make sync-dev`.
- All invocation outputs captured in `TASKLIST_ROOT/artifacts/D-0011/evidence.md`.

**Validation:**
- Manual check: reviewer runs forbidden and legitimate invocations for each sibling skill and confirms behavior.
- Evidence: linkable artifact produced (`evidence.md` with all invocations).

**Dependencies:** T04.01 (this task copies T04.01's clause); SOFT dependency on M2 (DEP-005).
**Rollback:** Revert SKILL.md edits via `git checkout --`; re-run `make sync-dev`.
**Notes:** Optional: Yes. Per roadmap (merged-thesis L3.2), this task is defer-pending-capacity. Excluded from sprint critical path; if not done, release still ships. M5 entry gate is NOT blocked by this task. Confidence reduced to 75% (vs T04.01's 80%) due to the conditional skip path when a sibling skill does not accept `--output`.

---

### T04.03 -- Checkpoint: End of Phase 4

| Field | Value |
|---|---|
| Roadmap Item IDs | R-010, R-011 |
| Why | Gate: verify L3 (skill-level guard) is in place. Confirm T04.01 is complete and document T04.02's optional status. |
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
| Deliverable IDs | D-CP04 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P04-END.md`

**Purpose:** Confirm the skill-level output-path guard is in place in sc-release-split-protocol and record T04.02's completion status (done or deferred).

**Verification:** (exactly 3 bullets)
- `sc-release-split-protocol --output .claude/skills/foo/` refuses pre-write and emits the correct error (output of T04.01).
- `make sync-dev` + `make verify-sync` exit cleanly with the M4 edits applied (output of T04.01) AND emit the M2 D2.1/D2.2 messages on the probe inputs per DEP-005 SOFT dep (or record an explicit M4 waiver if M2 has not merged).
- T04.02 status recorded: either completed (with evidence) or explicitly deferred with reason `defer-pending-capacity` (per roadmap optional flag).

**Exit Criteria:** (exactly 3 bullets)
- D-0010 has evidence captured under `TASKLIST_ROOT/artifacts/D-0010/`.
- D-0011 has evidence OR a deferral note recorded under `TASKLIST_ROOT/artifacts/D-0011/notes.md`.
- M5 entry is not blocked by D-0011 status (consistent with roadmap optional flag).

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present on disk (or `notes.md` deferral for D-0011).
2. **[VERIFICATION]** Re-run `sc-release-split-protocol` against a forbidden and a legitimate path; re-run `make verify-sync`.
3. **[VERIFICATION]** Write the checkpoint report to `TASKLIST_ROOT/checkpoints/CP-P04-END.md` and explicitly record T04.02 status (done or deferred).

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P04-END.md` exists and contains `Overall: Pass` and an explicit `T04.02 status: <done|deferred>` line.
- All 3 Verification bullets confirmed.
- All 3 Exit Criteria bullets met.
- Checkpoint report enumerates task IDs T04.01, T04.02.

**Validation:**
- Manual check: reviewer confirms the report at `TASKLIST_ROOT/checkpoints/CP-P04-END.md` and the recorded T04.02 status.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T04.01, T04.02 (T04.02 may be marked deferred)
**Rollback:** N/A (checkpoints are read-only verifications)
