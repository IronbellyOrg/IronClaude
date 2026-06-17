# Phase 8 -- Migration, Test Discipline & Hardening

**Goal:** Migrate `sc-bare-review` to a ~60-line thin caller building `--lens bare-review` job specs, executing the CLI, and relaying the return contract — with A/B parity vs the current bare-review output gating legacy shell deletion. Prove non-Claude caller compatibility via `subprocess.run`, land the enumerated migration deliverables (MIG-001..004: source-first sync, package entry registration, legacy shell retirement, release notes), and ship the per-IMM / per-INV / per-FR acceptance test suite as enumerated TEST-001..008 items. Exit when SKILL.md is migrated, `scripts/*.sh` removed only after A/B parity passes, non-Python caller produces identical contract, and every enumerated TEST item is green.

### T08.01 -- Migrate `sc-bare-review` SKILL.md to ~60-line thin caller

| Field | Value |
|---|---|
| Roadmap | R-135 (FR-029) |
| Deliverables | D-0116 |
| Effort | L |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie, serena |
| Sub-Agent | tech-research (migration design review) |
| Verification | tests: `uv run pytest tests/swarm/test_bare_review_parity.py` |

**Deliverables:**
1. `src/superclaude/skills/sc-bare-review/SKILL.md` rewritten as ~60-line thin caller invoking `swarm run --lens bare-review`.

**Steps:**
1. [PLANNING] Read current SKILL.md and identify orchestration code to remove.
2. [EXECUTION] Rewrite SKILL.md as thin caller building JobSpec → exec CLI → relay return contract.
3. [EXECUTION] Preserve user-facing behavior + flag surface.
4. [VERIFICATION] A/B parity gate (T08.11) must pass before legacy deletion (T08.07).
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- Thin caller ~60 lines; lens: bare-review; contract relayed; parity gate passes before legacy deletion.
- `bare_review_v1` recipe used via `--lens bare-review`.
- No orchestration logic in SKILL.md (delegated to CLI).
- A/B parity assertions deferred to T08.11 / TEST-003.

**Validation:**
- `wc -l src/superclaude/skills/sc-bare-review/SKILL.md` reports ≤80 lines.
- `make verify-sync` exits 0 after sync.

**Dependencies:** T03.08 (swarm run), T05.07 (contract emission), T04.03 (bare_review_v1). **Rollback:** revert SKILL.md to legacy version; restore `scripts/*.sh` reference path.
**Notes:** Gates MIG-003 legacy deletion.

### T08.02 -- Verify FR-030 non-Claude caller compatibility (`subprocess.run`)

| Field | Value |
|---|---|
| Roadmap | R-136 (FR-030) |
| Deliverables | D-0117 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_non_claude_caller.py` |

**Deliverables:**
1. `tests/swarm/test_non_claude_caller.py` invoking CLI via `subprocess.run` from a non-Python wrapper.

**Steps:**
1. [PLANNING] Compose non-Python caller (shell or another language wrapping subprocess).
2. [EXECUTION] Write test invoking `subprocess.run(["superclaude","swarm","run","--detached", spec_path])`.
3. [EXECUTION] Compare returned contract against Claude-invoked contract on identical input.
4. [VERIFICATION] Assert byte/structure equivalence.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Non-Python subprocess produces identical result contract.
- Detached supported via subprocess.run.
- No Claude-specific assumptions in invocation path.
- `tests/swarm/test_non_claude_caller.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_non_claude_caller.py -v` passes.
- Diff of two contracts returns empty (modulo timestamps).

**Dependencies:** T07.11 (detached). **Rollback:** mark test xfail; document deficiency.

### T08.03 -- Land per-IMM + per-INV test coverage matrix (NFR-007)

| Field | Value |
|---|---|
| Roadmap | R-137 (NFR-007) |
| Deliverables | D-0118 |
| Effort | L |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/ -m imm -v` and `-m inv -v` |

**Deliverables:**
1. `tests/swarm/conftest.py` + `pytest.ini` with `imm` and `inv` markers.
2. CI matrix exercising both marker subsets.

**Steps:**
1. [PLANNING] Enumerate IMM-3/4/5/6 + §11.5 + INV-001/002/003/005/007/010/014.
2. [EXECUTION] Mark each existing test with appropriate marker.
3. [EXECUTION] Register markers in pytest.ini.
4. [VERIFICATION] Run `-m imm` and `-m inv` selectors; assert coverage.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Every IMM + INV has a passing dedicated test.
- `pytest -m imm` and `pytest -m inv` run subsets cleanly.
- CI matrix runs both lanes.
- Test count per marker matches enumeration.

**Validation:**
- `uv run pytest tests/swarm/ -m imm -v` lists all IMM tests passing.
- `uv run pytest tests/swarm/ -m inv -v` lists all INV tests passing.

**Dependencies:** T08.09, T08.10. **Rollback:** mark partial coverage; raise issue.

### T08.04 -- MIG-001 source-first sync workflow

| Field | Value |
|---|---|
| Roadmap | R-138 (MIG-001) |
| Deliverables | D-0119 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: `make verify-sync` |

**Deliverables:**
1. `docs/dev/migration-skill.md` documenting src-first edit + sync workflow for the skill migration.

**Steps:**
1. [PLANNING] Confirm src-first rule from CLAUDE.md.
2. [EXECUTION] Author doc detailing migration sync steps.
3. [EXECUTION] Add pre-commit assertion that `.claude/skills/sc-bare-review/` matches src.
4. [VERIFICATION] `make verify-sync` exits 0.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- src updated; `make sync-dev` run; `make verify-sync` clean; no direct `.claude/` edits.
- Doc cites CLAUDE.md source-of-truth rule.
- Pre-commit hook references skill migration paths.
- Doc renders without markdownlint errors.

**Validation:**
- `make verify-sync` exits 0.
- `grep -q "make sync-dev" docs/dev/migration-skill.md`.

**Dependencies:** T08.01. **Rollback:** revert doc.

### T08.05 -- MIG-002 package entry point registration

| Field | Value |
|---|---|
| Roadmap | R-139 (MIG-002) |
| Deliverables | D-0120 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, context7 (pyproject entry points) |
| Sub-Agent | none |
| Verification | tests: `pipx install --force . && superclaude swarm --help` |

**Deliverables:**
1. `pyproject.toml` updated with swarm CLI group registered under console_scripts/entry_points.

**Steps:**
1. [PLANNING] Confirm pyproject `[project.scripts]` includes `superclaude`.
2. [EXECUTION] Ensure swarm CLI group reachable via the existing entry point.
3. [VERIFICATION] `pipx install --force .` succeeds; `superclaude swarm --help` lists subcommands.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- `superclaude swarm --help` lists subcommands.
- Package imports clean post-install.
- Entry point installs cleanly via `pipx install --force`.
- No additional console_script needed (swarm under existing `superclaude`).

**Validation:**
- `pipx install --force .` exits 0.
- `superclaude swarm --help` exits 0 with 8 subcommands.

**Dependencies:** T01.02. **Rollback:** revert pyproject changes.

### T08.06 -- Checkpoint: Phase 8 mid-phase gate (tasks 1-5)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP8-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T08.01..T08.05 marked done in execution-log.
- `phase-8-cp1.md` checkpoint report written.
- SKILL.md migrated; non-Claude caller test; per-IMM/INV matrix; src-first sync; pkg entry registered.
- A/B parity gate not yet run (deferred to T08.11).

**Validation:**
- `pipx install --force .` succeeds; `superclaude swarm --help` works.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T08.01..T08.05.

### T08.07 -- MIG-003 legacy `scripts/*.sh` retirement (after A/B parity passes)

| Field | Value |
|---|---|
| Roadmap | R-140 (MIG-003) |
| Deliverables | D-0121 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash, auggie |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_bare_review_parity.py` (must precede deletion) |

**Deliverables:**
1. Deleted `src/superclaude/skills/sc-bare-review/scripts/*.sh` after TEST-003 (T08.11) passes.

**Steps:**
1. [PLANNING] Confirm T08.11 parity gate green.
2. [EXECUTION] Delete shell scripts only after parity confirmed.
3. [EXECUTION] Remove any references in SKILL.md or docs.
4. [VERIFICATION] `grep` for shell references returns empty.
5. [COMPLETION] `make sync-dev && make verify-sync`.

**Acceptance Criteria:**
- Shell scripts removed; no legacy dispatch refs in skill; legacy code path absent.
- Deletion is sequenced AFTER T08.11 parity gate.
- References purged from SKILL.md.
- Pre-deletion checklist documented in MIG-004 (T08.08).

**Validation:**
- `ls src/superclaude/skills/sc-bare-review/scripts/` returns empty or no .sh files.
- `grep -RnE "scripts/.*\.sh" src/superclaude/skills/sc-bare-review/` empty.

**Dependencies:** T08.11 (TEST-003 parity). **Rollback:** restore deleted scripts from git history.

### T08.08 -- MIG-004 release notes + operator migration note

| Field | Value |
|---|---|
| Roadmap | R-141 (MIG-004) |
| Deliverables | D-0122 |
| Effort | S |
| Risk | LOW |
| Tier | STANDARD |
| Confidence | `[█████████-] 90%` |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | smoke: doc renders |

**Deliverables:**
1. `docs/swarm/release-notes-v1.md` documenting CLI invocation, resume behavior, prompt guard requirement, custom prompt migration path.

**Steps:**
1. [PLANNING] Enumerate migration topics: invocation change, resume, --auto-inject-guard, custom prompt migration.
2. [EXECUTION] Author release notes with examples.
3. [VERIFICATION] Render doc.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Run examples; resume notes; `--auto-inject-guard` migration; custom prompt path documented.
- Examples copy-pasteable.
- Cross-links to OPS-001 runbook (M9).
- Doc passes markdownlint.

**Validation:**
- `markdownlint docs/swarm/release-notes-v1.md` exits 0.
- Examples cite `swarm run --lens bare-review`.

**Dependencies:** T08.01, T08.05. **Rollback:** revert doc.

### T08.09 -- TEST-001 IMM acceptance suite

| Field | Value |
|---|---|
| Roadmap | R-142 (TEST-001) |
| Deliverables | D-0123 |
| Effort | L |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | tech-research (suite design review) |
| Verification | tests: `uv run pytest tests/swarm/test_imm_suite.py` |

**Deliverables:**
1. `tests/swarm/test_imm_suite.py` consolidating IMM-3/4/5/6 + §11.5 acceptance tests.

**Steps:**
1. [PLANNING] Enumerate IMM cases: IMM-3 parallelism, IMM-4 empty-target STOP (49-byte), IMM-5 status matrix, IMM-6 atomic-write mid-write kill, §11.5 end-marker target safety.
2. [EXECUTION] Aggregate existing IMM tests + add suite entry points.
3. [EXECUTION] Mark with `@pytest.mark.imm`.
4. [VERIFICATION] Run suite; assert each IMM case green.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Each IMM case has a dedicated passing test.
- Suite runnable via `pytest -m imm`.
- All 5 cases (IMM-3/4/5/6 + §11.5) listed.
- `tests/swarm/test_imm_suite.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_imm_suite.py -v` passes.
- `pytest -m imm --collect-only` lists ≥5 tests.

**Dependencies:** T03.11, T02.13, T05.03, T03.13, T02.26. **Rollback:** mark missing case xfail.

### T08.10 -- TEST-002 INV remediation suite

| Field | Value |
|---|---|
| Roadmap | R-143 (TEST-002) |
| Deliverables | D-0124 |
| Effort | L |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | tech-research |
| Verification | tests: `uv run pytest tests/swarm/test_inv_suite.py` |

**Deliverables:**
1. `tests/swarm/test_inv_suite.py` consolidating INV-001/002/003/005/007/010/014 remediation tests.

**Steps:**
1. [PLANNING] Enumerate INV cases: INV-001 manifest lens rehydration, INV-002 Python-only dispatch, INV-003 custom-prompt-dir guard, INV-005 worker-vs-pool, INV-007 empty-pool failure, INV-010 resume merge regen, INV-014 escape-hatch isomorphism.
2. [EXECUTION] Aggregate INV tests with `@pytest.mark.inv` marker.
3. [VERIFICATION] Run suite.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Each INV remediation has a dedicated passing test.
- Suite runnable via `pytest -m inv`.
- All 7 INV cases listed.
- `tests/swarm/test_inv_suite.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_inv_suite.py -v` passes.
- `pytest -m inv --collect-only` lists ≥7 tests.

**Dependencies:** T06.01, T03.14, T02.08, T02.10, T02.11, T06.02, T02.09. **Rollback:** mark missing case xfail.

### T08.11 -- TEST-003 bare-review A/B parity test

| Field | Value |
|---|---|
| Roadmap | R-144 (TEST-003) |
| Deliverables | D-0125 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, auggie |
| Sub-Agent | tech-research (A/B harness review) |
| Verification | tests: `uv run pytest tests/swarm/test_bare_review_parity.py` |

**Deliverables:**
1. `tests/swarm/test_bare_review_parity.py` comparing thin-caller output vs legacy bare-review.

**Steps:**
1. [PLANNING] Define A/B corpus (shared targets used in both runs).
2. [EXECUTION] Run legacy bare-review (pre-migration path) capturing output.
3. [EXECUTION] Run thin-caller `swarm run --lens bare-review` capturing output.
4. [EXECUTION] Compare normalized output structure (allow timestamps to differ).
5. [VERIFICATION] Assert equivalence; gate MIG-003 deletion.
6. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Same target → equivalent normalized output; contract relayed; gates MIG-003.
- A/B harness covers ≥3 representative targets.
- Equivalence asserted on findings table structure + content.
- `tests/swarm/test_bare_review_parity.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_bare_review_parity.py -v` passes.
- Output diff (modulo timestamps) returns empty.

**Dependencies:** T08.01, T04.03. **Rollback:** keep legacy path operational; defer MIG-003.
**Notes:** This gate sequences before T08.07.

### T08.12 -- Checkpoint: Phase 8 migration gate (tasks 7-11)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP8-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T08.07..T08.11 marked done in execution-log.
- `phase-8-cp2.md` checkpoint report written.
- Legacy shells retired post-parity; release notes written; IMM/INV suites green; A/B parity confirmed.
- MIG-001..004 + TEST-001..003 all done.

**Validation:**
- `uv run pytest tests/swarm/test_bare_review_parity.py tests/swarm/test_imm_suite.py tests/swarm/test_inv_suite.py -v` passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T08.07..T08.11.

### T08.13 -- TEST-004 bundled lens validation gate

| Field | Value |
|---|---|
| Roadmap | R-145 (TEST-004) |
| Deliverables | D-0126 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[█████████-] 90%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_validate_lenses_ci.py` |

**Deliverables:**
1. `tests/swarm/test_validate_lenses_ci.py` running `swarm validate-lenses` in CI against all non-custom entries.

**Steps:**
1. [PLANNING] Confirm 7 non-custom entries available.
2. [EXECUTION] Write test invoking `swarm validate-lenses` and asserting exit 0.
3. [VERIFICATION] Run test in CI lane.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- 7 non-custom entries pass validator in CI.
- Failure semantics match OQ-010 resolution (exit code, blocking).
- CI lane runs validator on every PR.
- `tests/swarm/test_validate_lenses_ci.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_validate_lenses_ci.py -v` passes.
- `swarm validate-lenses` exits 0.

**Dependencies:** T02.16, T02.20. **Rollback:** convert to warning during triage.

### T08.14 -- TEST-005 non-Claude caller integration test

| Field | Value |
|---|---|
| Roadmap | R-146 (TEST-005) |
| Deliverables | D-0127 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/test_subprocess_caller.py` |

**Deliverables:**
1. `tests/swarm/test_subprocess_caller.py` cross-language subprocess wrapper invoking CLI.

**Steps:**
1. [PLANNING] Compose non-Python caller (bash or other) wrapping subprocess.
2. [EXECUTION] Run swarm via subprocess from wrapper; capture return contract.
3. [VERIFICATION] Compare to Claude-invoked contract; assert identical (modulo timestamps).
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Subprocess invocation succeeds; detached supported; contract identical to Claude invocation.
- Test exercises both inline and detached modes.
- Cross-language caller documented.
- `tests/swarm/test_subprocess_caller.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_subprocess_caller.py -v` passes.
- Contract diff empty modulo timestamps.

**Dependencies:** T08.02, T07.11. **Rollback:** mark xfail.

### T08.15 -- TEST-006 mechanical-merge boundary test (final hardened)

| Field | Value |
|---|---|
| Roadmap | R-147 (TEST-006) |
| Deliverables | D-0128 |
| Effort | M |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | tech-research (final boundary hardening) |
| Verification | tests: `uv run pytest tests/swarm/test_merge_mechanical_only.py` |

**Deliverables:**
1. `tests/swarm/test_merge_mechanical_only.py` final hardened version with CI file-touch rule.

**Steps:**
1. [PLANNING] Audit T05.09 test; add adversarial cases (huge inputs, duplicates, reorder attempts).
2. [EXECUTION] Harden test with extra fixtures.
3. [EXECUTION] Confirm CI rule flags PRs touching test file.
4. [VERIFICATION] Run test; verify CI rule.
5. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- 3 sections in slot order; no transforms beyond header; CI rule active.
- Adversarial fixtures included.
- Test file flagged in PR review checklist.
- `tests/swarm/test_merge_mechanical_only.py` final hardened green.

**Validation:**
- `uv run pytest tests/swarm/test_merge_mechanical_only.py -v` passes.
- `.github/workflows/` references test file in PR-touch check.

**Dependencies:** T05.09. **Rollback:** revert to T05.09 baseline.

### T08.15a -- Checkpoint: Phase 8 test gate (tasks 13-15)

| Field | Value |
|---|---|
| Type | CHECKPOINT (mid-phase) |
| Deliverables | D-CP8-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T08.13..T08.15 marked done in execution-log.
- `phase-8-cp3.md` checkpoint report written.
- TEST-004 + TEST-005 + TEST-006 hardened all green.

**Validation:**
- `uv run pytest tests/swarm/test_validate_lenses_ci.py tests/swarm/test_subprocess_caller.py tests/swarm/test_merge_mechanical_only.py -v` passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T08.13..T08.15.

### T08.16 -- TEST-007 resume crash recovery E2E

| Field | Value |
|---|---|
| Roadmap | R-148 (TEST-007) |
| Deliverables | D-0129 |
| Effort | L |
| Risk | HIGH |
| Tier | STRICT |
| Confidence | `[████████--] 80%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit, Bash |
| Sub-Agent | tech-research |
| Verification | tests: `uv run pytest tests/swarm/test_resume_crash_recovery.py` |

**Deliverables:**
1. `tests/swarm/test_resume_crash_recovery.py` full E2E test.

**Steps:**
1. [PLANNING] Compose E2E scenario: start swarm → SIGKILL mid-Wave-1 → resume → assert terminal.
2. [EXECUTION] Write test orchestrating subprocess kill + resume.
3. [VERIFICATION] Assert succeeded workers skipped, remaining re-dispatched, Wave 2 reruns, merge regenerates.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Kill-then-resume reaches terminal state with no duplicate work; merge regenerated.
- E2E covers the full Wave 1→3 redispatch path.
- Worker skip + merge regen both verified.
- `tests/swarm/test_resume_crash_recovery.py` green.

**Validation:**
- `uv run pytest tests/swarm/test_resume_crash_recovery.py -v` passes.
- `workers_succeeded` count matches expected.

**Dependencies:** T06.04, T06.08. **Rollback:** mark xfail with diagnostics.

### T08.17 -- TEST-008 wire deterministic-fixture transport into integration suite

| Field | Value |
|---|---|
| Roadmap | R-149 (TEST-008) |
| Deliverables | D-0130 |
| Effort | M |
| Risk | MEDIUM |
| Tier | STRICT |
| Confidence | `[████████--] 85%` |
| Critical Path Override | YES |
| MCP Tools | Read, Edit |
| Sub-Agent | none |
| Verification | tests: `uv run pytest tests/swarm/integration/ -v` |

**Deliverables:**
1. `tests/swarm/integration/conftest.py` wiring stub transport into full M3-M5 integration coverage.

**Steps:**
1. [PLANNING] Identify integration tests currently using mocks; plan replacement with stub.
2. [EXECUTION] Refactor integration suite to consume stub transport via fixture.
3. [VERIFICATION] Run integration suite; assert no network calls.
4. [COMPLETION] `make sync-dev`.

**Acceptance Criteria:**
- Integration suite runs end-to-end against wired-in deterministic-fixture transport.
- CI passes without external network.
- Integration test count covers Wave 1→3 paths.
- `tests/swarm/integration/conftest.py` provides shared stub fixture.

**Validation:**
- `uv run pytest tests/swarm/integration/ -v` passes.
- Network isolation: `httpx.AsyncClient` patched to forbid real calls in test.

**Dependencies:** T03.07, T04.01, T05.01. **Rollback:** revert to mock-based integration tests.

### T08.18 -- Checkpoint: Phase 8 exit gate (end-of-phase)

| Field | Value |
|---|---|
| Type | CHECKPOINT (end-of-phase) |
| Deliverables | D-CP8-1 |
| Tier | EXEMPT |

**Acceptance Criteria:**
- All of T08.01..T08.17 marked done in execution-log.
- `phase-8-cp4.md` end-of-phase checkpoint written.
- SKILL.md migrated, A/B parity passed, legacy shells deleted, MIG-001..004 + TEST-001..008 all green.
- Release candidate ready for M9 operational handoff.

**Validation:**
- `uv run pytest tests/swarm/ -v` Phase 8 surface passes.
- Checkpoint file under `tasklist/checkpoints/`.

**Dependencies:** T08.01..T08.17. **Rollback:** none — phase exit gate.
**Notes:** M8 exit unblocks M9 operational handoff.
