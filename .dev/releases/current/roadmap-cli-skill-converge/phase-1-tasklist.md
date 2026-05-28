# Phase 1 -- Command Surface Alignment

Align the two slash command files with the current CLI surface before deeper skill/reference updates. This phase implements B-1 and B-2 as a command-surface batch; neither task is blocked by the other, but both must complete before Phase 2.

### T01.01 -- Mirror `superclaude roadmap run` flags in `src/superclaude/commands/roadmap.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001 |
| Why | The source documents state that `/sc:roadmap` exposes inference-only flags, omits current CLI flags, and documents a default output directory that diverges from the CLI. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0001 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0001/spec.md`
- `TASKLIST_ROOT/artifacts/D-0001/notes.md`
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md`

**Deliverables:**

- Updated `src/superclaude/commands/roadmap.md` with CLI-faithful `/sc:roadmap` command surface.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0001/evidence.md`.

**Steps:**

1. **[PLANNING]** Load context and identify scope for `src/superclaude/commands/roadmap.md`.
2. **[PLANNING]** Check dependencies and blockers from B-1 flag drift evidence.
3. **[EXECUTION]** Replace inference-only usage and flag rows with the current `superclaude roadmap run --help` surface, including shared flags and CLI-only flags.
4. **[EXECUTION]** Add `--allow-cosmetic-remediation`, `--no-allow-cosmetic-remediation`, and `--strict-no-remediation` to the command surface description.
5. **[VERIFICATION]** Validate `src/superclaude/commands/roadmap.md` against exact CLI-help parity and B-1 release criteria.
6. **[COMPLETION]** Record source-file validation evidence in `TASKLIST_ROOT/artifacts/D-0001/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/commands/roadmap.md` usage, flag table, examples, and output wording mirror current `superclaude roadmap run --help` exactly.
- File `src/superclaude/commands/roadmap.md` removes or explicitly deprecates `--specs`, `--template/-t`, `--multi-roadmap`, `--interactive/-i`, `--compliance/-c`, and `--persona/-p`.
- File `src/superclaude/commands/roadmap.md` documents the parent-directory default output and the cosmetic-remediation flags `--allow-cosmetic-remediation`, `--no-allow-cosmetic-remediation`, and `--strict-no-remediation`.
- Evidence at `TASKLIST_ROOT/artifacts/D-0001/evidence.md` links B-1 to `D-0001` and summarizes the source-file parity check.

**Validation:**

- Manual check: compare `src/superclaude/commands/roadmap.md` against current `superclaude roadmap run --help` and B-1 current-update sweep.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0001/evidence.md`.

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** The source decision selects Option 1 for B-1 and requires a 1:1 command rewrite.

### T01.02 -- Mirror `superclaude roadmap validate` flags in `src/superclaude/commands/validate-roadmap.md`

| Field | Value |
|---|---|
| Roadmap Item IDs | R-002 |
| Why | The source documents identify frontmatter, flag-set, output-dir, adversarial-merge, and NFR-006 documentation drift in `/sc:validate-roadmap`. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | Required: None; Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0002 |

**Artifacts (Intended Paths):**

- `TASKLIST_ROOT/artifacts/D-0002/spec.md`
- `TASKLIST_ROOT/artifacts/D-0002/notes.md`
- `TASKLIST_ROOT/artifacts/D-0002/evidence.md`

**Deliverables:**

- Updated `src/superclaude/commands/validate-roadmap.md` with CLI-faithful `/sc:validate-roadmap` command surface.
- Supporting evidence at `TASKLIST_ROOT/artifacts/D-0002/evidence.md`.

**Steps:**

1. **[PLANNING]** Load context and identify scope for `src/superclaude/commands/validate-roadmap.md`.
2. **[PLANNING]** Check dependencies and blockers from B-2 verification evidence.
3. **[EXECUTION]** Change frontmatter naming to `sc:validate-roadmap`.
4. **[EXECUTION]** Replace inference-only flags with the CLI validate positional output directory and `--agents`, `--model`, `--max-turns`, and `--debug`.
5. **[VERIFICATION]** Validate `src/superclaude/commands/validate-roadmap.md` output wording, N≥2 adversarial-merge condition, and NFR-006 exit-code documentation against B-2.
6. **[COMPLETION]** Record source-file validation evidence in `TASKLIST_ROOT/artifacts/D-0002/evidence.md`.

**Acceptance Criteria:**

- File `src/superclaude/commands/validate-roadmap.md` has frontmatter name `sc:validate-roadmap` and mirrors CLI `validate <OUTPUT_DIR>` usage, flags, and examples.
- File `src/superclaude/commands/validate-roadmap.md` uses `<OUTPUT_DIR>/validate/` for CLI validation output.
- File `src/superclaude/commands/validate-roadmap.md` states that adversarial merge only runs when N≥2 agents and that CLI validation exits 0 per NFR-006.
- Evidence at `TASKLIST_ROOT/artifacts/D-0002/evidence.md` links B-2 to `D-0002` and lists removed inference-only validate flags.

**Validation:**

- Manual check: compare `src/superclaude/commands/validate-roadmap.md` against B-2 flag, output, adversarial-merge, and NFR-006 requirements.
- Evidence: linkable artifact produced at `TASKLIST_ROOT/artifacts/D-0002/evidence.md`.

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** The source decision selects Option 1 for B-2.

### T01.03 -- Checkpoint: End of Phase 01

| Field | Value |
|---|---|
| Roadmap Item IDs | R-001, R-002 |
| Why | Gate: verify outputs of tasks T01.01-T01.02 before continuing. |
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

**Checkpoint Report Path:** TASKLIST_ROOT/checkpoints/CP-P01-END.md

**Purpose:** Confirm both command-surface source edits are ready before skill/reference edits begin.

**Verification:**

- `src/superclaude/commands/roadmap.md` mirrors current `superclaude roadmap run --help`, including cosmetic-remediation flags.
- `src/superclaude/commands/validate-roadmap.md` mirrors CLI validate flags and documents `<OUTPUT_DIR>/validate/`, N≥2 adversarial merge, and NFR-006 exit 0.
- `TASKLIST_ROOT/artifacts/D-0001/evidence.md` and `TASKLIST_ROOT/artifacts/D-0002/evidence.md` summarize direct source-file validation.

**Exit Criteria:**

- B-1 command-surface source edit is represented and evidenced.
- B-2 command-surface source edit is represented and evidenced.
- `TASKLIST_ROOT/checkpoints/CP-P01-END.md` is secondary evidence summarizing direct source-file validation.

**Steps:**

1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**

- File `TASKLIST_ROOT/checkpoints/CP-P01-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes task IDs T01.01 and T01.02 and roadmap IDs R-001 and R-002.

**Validation:**

- Manual check: reviewer confirms the report at the Checkpoint Report Path summarizes direct source-file validation.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T01.01..T01.02
**Rollback:** N/A (checkpoint reports can be regenerated if recorded incorrectly)
