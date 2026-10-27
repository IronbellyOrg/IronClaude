# Phase 2 -- Isolation Process Vendored Ptytest

**Phase Goal:** Land HomeIsolation with defense-in-depth path containment, vendored ptytest fork (with attribution complete), PtyDriver, and the ANSI-aware stream layer. Every component that touches the per-eval HOME or the real `claude` subprocess merges in this phase.

### T02.01 -- Vendor ptytest fork under cli/eval/pty/ (NFR-MAINT1)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-023 |
| Why | NFR-MAINT1 requires forking ptytest under `cli/eval/pty/` with upstream LICENSE retained, PROVENANCE.md documenting fork SHA + changes, and `pexpect>=4.9` pinned. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0023 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0023/spec.md`
- `TASKLIST_ROOT/artifacts/D-0023/notes.md`
- `TASKLIST_ROOT/artifacts/D-0023/evidence.md`

**Deliverables:**
- Vendored ptytest sources under `src/superclaude/cli/eval/pty/` with LICENSE and PROVENANCE.md.

**Steps:**
1. **[PLANNING]** Confirm DOC-OQ4 (T02.02) is complete (M2 entry blocker).
2. **[PLANNING]** Identify upstream ptytest SHA to vendor and capture changes list.
3. **[EXECUTION]** Copy ptytest sources into `src/superclaude/cli/eval/pty/` retaining LICENSE.
4. **[EXECUTION]** Pin `pexpect>=4.9` via vendored module imports; add PROVENANCE.md with fork SHA + changes.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_pty_vendor.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.01/`.

**Acceptance Criteria:**
- Directory `src/superclaude/cli/eval/pty/` contains ptytest sources with upstream LICENSE file present.
- File `PROVENANCE.md` exists at the same path and records fork SHA, vendoring date, and changes list.
- `pexpect>=4.9` is reachable via `from superclaude.cli.eval.pty import pexpect` (or equivalent vendored import path).
- `TASKLIST_ROOT/artifacts/D-0023/spec.md` records the vendoring plan and SHA pin.

**Validation:**
- Manual check: import the vendored module and verify `pexpect.__version__ >= 4.9`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.02
**Rollback:** TBD (if not specified in roadmap)
**Notes:** M2 entry blocked until OQ-4 closed; DOC-OQ4 (T02.02) must land first.

### T02.02 -- DOC-OQ4 NOTICE/LICENSE attribution for ptytest

| Field | Value |
|---|---|
| Roadmap Item IDs | R-024 |
| Why | DOC-OQ4 is the M2 entry blocker per debate convergence: NOTICE at repo root must reference ptytest LICENSE before vendored sources land. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0024 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0024/spec.md`
- `TASKLIST_ROOT/artifacts/D-0024/notes.md`
- `TASKLIST_ROOT/artifacts/D-0024/evidence.md`

**Deliverables:**
- `NOTICE` file at repo root referencing ptytest LICENSE; decisions.md ADR entry recording the decision.

**Steps:**
1. **[PLANNING]** Inspect existing repo NOTICE state (likely absent).
2. **[PLANNING]** Read ptytest upstream LICENSE for attribution text.
3. **[EXECUTION]** Add `NOTICE` at repo root with ptytest attribution clause.
4. **[EXECUTION]** Record decision in `.dev/releases/current/cliEval/decisions.md` with D-? entry.
5. **[VERIFICATION]** Manual review by maintainer.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.02/`.

**Acceptance Criteria:**
- File `NOTICE` exists at repo root and references ptytest LICENSE.
- `.dev/releases/current/cliEval/decisions.md` contains a D-? entry recording OQ-4 closure.
- DOC-OQ4 status changes from "open" to "resolved" in decisions.md.
- `TASKLIST_ROOT/artifacts/D-0024/spec.md` records the attribution clause.

**Validation:**
- Manual check: confirm `NOTICE` exists and `grep -c ptytest NOTICE` returns >=1.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** M2 entry blocker; vendoring (T02.01) cannot land first.

### T02.03 -- AC10 ptytest fork SHA pin + drift policy

| Field | Value |
|---|---|
| Roadmap Item IDs | R-025 |
| Why | AC10 documents fork SHA freeze with quarterly review cadence and resync procedure; CHECKLIST.md in `cli/eval/pty/` records review owner. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0025 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0025/spec.md`
- `TASKLIST_ROOT/artifacts/D-0025/notes.md`
- `TASKLIST_ROOT/artifacts/D-0025/evidence.md`

**Deliverables:**
- `PROVENANCE.md` entry under `src/superclaude/cli/eval/pty/` recording SHA + review cadence, plus `CHECKLIST.md` with review steps.

**Steps:**
1. **[PLANNING]** Confirm NFR-MAINT1 (T02.01) has the SHA recorded.
2. **[PLANNING]** Define quarterly review owner (RyanW per roadmap risk register).
3. **[EXECUTION]** Append SHA + review-date + cadence section to `PROVENANCE.md`.
4. **[EXECUTION]** Author `CHECKLIST.md` with the 5-step review procedure.
5. **[VERIFICATION]** Manual review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.03/`.

**Acceptance Criteria:**
- File `src/superclaude/cli/eval/pty/PROVENANCE.md` records fork SHA, vendoring date, and "review cadence: quarterly".
- File `src/superclaude/cli/eval/pty/CHECKLIST.md` exists with the review-procedure steps.
- Review owner is named explicitly (RyanW).
- `TASKLIST_ROOT/artifacts/D-0025/spec.md` records the drift policy.

**Validation:**
- Manual check: read PROVENANCE.md + CHECKLIST.md and confirm fields present.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Quarterly cadence carries into R5-mit (T02.26).

### T02.04 -- Add DM-006 HomeIsolation frozen dataclass

| Field | Value |
|---|---|
| Roadmap Item IDs | R-026 |
| Why | DM-006 captures isolation state per-eval: eval_id, home_root, session_id, time_offset_sec. Frozen dataclass enables safe sharing across threads. |
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
| Deliverable IDs | D-0026 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0026/spec.md`
- `TASKLIST_ROOT/artifacts/D-0026/notes.md`
- `TASKLIST_ROOT/artifacts/D-0026/evidence.md`

**Deliverables:**
- `HomeIsolation` frozen dataclass in `src/superclaude/cli/eval/isolation.py` with the 4 fields from DM-006.

**Steps:**
1. **[PLANNING]** Confirm field semantics: eval_id:str, home_root:Path, session_id:str, time_offset_sec:int=0.
2. **[PLANNING]** Identify consumer site (COMP-006 T02.11).
3. **[EXECUTION]** Add `HomeIsolation` frozen dataclass with the 4 fields.
4. **[EXECUTION]** Provide `__post_init__` validating eval_id via `validate_eval_id` (T01.05).
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_isolation_dataclass.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.04/`.

**Acceptance Criteria:**
- Class `HomeIsolation` in `src/superclaude/cli/eval/isolation.py` is a frozen dataclass with fields `eval_id`,`home_root`,`session_id`,`time_offset_sec`.
- Construction with an unsafe `eval_id` raises `InvalidEvalId` (delegated to `validate_eval_id`).
- Default `time_offset_sec=0` matches DM-006 spec.
- `TASKLIST_ROOT/artifacts/D-0026/spec.md` documents the 4-field contract.

**Validation:**
- Manual check: build a `HomeIsolation` and assert mutation raises FrozenInstanceError.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.05
**Rollback:** TBD (if not specified in roadmap)
**Notes:** time_offset_sec semantics gated on OQ-8 resolution (DOC-OQ8 T06.03).

### T02.05 -- Pin IsolationLayers API surface via COMP-012 probe

| Field | Value |
|---|---|
| Roadmap Item IDs | R-027 |
| Why | COMP-012 read-only smoke test pins the API of `cli/sprint/executor.py:107-182` so HomeIsolation extension fails fast on upstream shape changes. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0027 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0027/spec.md`
- `TASKLIST_ROOT/artifacts/D-0027/notes.md`
- `TASKLIST_ROOT/artifacts/D-0027/evidence.md`

**Deliverables:**
- Probe test `tests/cli/eval/test_isolation_layers_probe.py` pinning the IsolationLayers API surface.

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/sprint/executor.py` lines 107-182 to inventory IsolationLayers API.
2. **[PLANNING]** Decide which method signatures need pinning.
3. **[EXECUTION]** Author probe test asserting method names, parameter names, and return types via inspection.
4. **[EXECUTION]** Add docstring explaining failure means upstream refactor occurred.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_isolation_layers_probe.py -v` and confirm pass on current tree.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.05/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_isolation_layers_probe.py` exists and asserts the IsolationLayers API surface against `cli/sprint/executor.py:107-182`.
- Test passes against the current tree and fails on a synthetic mutation of a pinned method signature.
- Test is read-only (no IsolationLayers instances are constructed; uses `inspect`).
- `TASKLIST_ROOT/artifacts/D-0027/spec.md` records the pinned surface.

**Validation:**
- Manual check: mutate an IsolationLayers method name temporarily and confirm test fails.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** None
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Probe is read-only; no IsolationLayers state is touched.

### T02.06 -- Checkpoint: Phase 2 / Tasks T02.01-T02.05

| Field | Value |
|---|---|
| Roadmap Item IDs | R-023,R-024,R-025,R-026,R-027 |
| Why | Gate: verify vendored ptytest, NOTICE attribution, SHA pin, HomeIsolation record, and IsolationLayers probe before HomeIsolation extension and containment guard land. |
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
| Deliverable IDs | D-CP02-MID-T01-T05 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md`

**Purpose:** Confirm vendoring, attribution, and isolation data model before HomeIsolation extension.

**Verification:**
- Vendored ptytest sources at `src/superclaude/cli/eval/pty/` include LICENSE and PROVENANCE.md.
- NOTICE at repo root references ptytest LICENSE.
- IsolationLayers probe test passes on current tree.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_pty_vendor.py tests/cli/eval/test_isolation_dataclass.py tests/cli/eval/test_isolation_layers_probe.py -v` exits 0.
- `grep -q ptytest NOTICE` returns 0.
- Checkpoint report `CP-P02-T01-T05.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P02-T01-T05.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T02.01-T02.05).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.01..T02.05
**Rollback:** N/A (checkpoints are read-only verifications)

### T02.07 -- Extend IsolationLayers with HomeIsolation (FR-ISO1)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-028 |
| Why | FR-ISO1 adds HOME override + CLAUDE_SESSION_ID stamp + optional CLAUDE_FAKE_TIME_OFFSET while preserving the 4 existing isolation guarantees (cwd, git ceiling, plugin dir, settings dir). |
| Effort | L |
| Risk | Medium |
| Risk Drivers | scope (cross-cutting per-eval isolation) |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0028 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0028/spec.md`
- `TASKLIST_ROOT/artifacts/D-0028/notes.md`
- `TASKLIST_ROOT/artifacts/D-0028/evidence.md`

**Deliverables:**
- `HomeIsolation` class in `src/superclaude/cli/eval/isolation.py` exposing `setup()`, `env() -> dict[str,str]`, `teardown(keep: bool)`, `state_path(suffix: str) -> Path`, extending IsolationLayers.

**Steps:**
1. **[PLANNING]** Confirm DM-006 record (T02.04) and probe (T02.05) are landed.
2. **[PLANNING]** Inventory the 4 existing IsolationLayers guarantees (cwd, git ceiling, plugin dir, settings dir).
3. **[EXECUTION]** Implement `HomeIsolation.setup()` mkdtemp under `home_root` and stamp CLAUDE_SESSION_ID.
4. **[EXECUTION]** Implement `env()`, `teardown(keep)`, `state_path(suffix)` per spec; honor `CLAUDE_FAKE_TIME_OFFSET` if OQ-8 resolution permits.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_home_isolation_extend.py -v` and quality-engineer review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.07/`.

**Acceptance Criteria:**
- Class `HomeIsolation` exposes `setup`, `env`, `teardown(keep)`, `state_path(suffix)` and preserves the 4 existing isolation guarantees (verified by re-running the IsolationLayers probe).
- `env()` returns a dict containing `HOME`, `CLAUDE_SESSION_ID`, optional `CLAUDE_FAKE_TIME_OFFSET`.
- Per-eval HOMEs are sibling directories under `home_root`; mutating one HOME does not affect siblings (concurrency-safe).
- `TASKLIST_ROOT/artifacts/D-0028/spec.md` records the method contract.

**Validation:**
- Manual check: build a `HomeIsolation` and confirm `setup()` creates a sibling HOME under home_root.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.04, T02.05
**Rollback:** TBD (if not specified in roadmap)
**Notes:** time_offset behavior conditional on OQ-8 resolution (DOC-OQ8 T06.03).

### T02.08 -- Implement FR-ISO2 path containment guard (security-critical)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-029 |
| Why | FR-ISO2 is security-critical: re-check eval_id regex, verify `home_path.is_relative_to(scratch_root)`, and resolve symlinks AFTER creation BEFORE hook deploy. Raises HomeContainmentViolation. |
| Effort | L |
| Risk | High |
| Risk Drivers | security, scope |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0029 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0029/spec.md`
- `TASKLIST_ROOT/artifacts/D-0029/notes.md`
- `TASKLIST_ROOT/artifacts/D-0029/evidence.md`

**Deliverables:**
- `containment_guard(home_path, scratch_root, eval_id)` raising `HomeContainmentViolation` when any of the three checks fails; integrated into `HomeIsolation.setup()`.

**Steps:**
1. **[PLANNING]** Confirm AC12 allowlist (T01.19) and FR-ISO1 (T02.07) are landed.
2. **[PLANNING]** Enumerate failure cases: bad eval_id, home outside scratch_root, symlink escape post-creation.
3. **[EXECUTION]** Implement `containment_guard` chaining the 3 checks; resolve symlinks via `Path.resolve(strict=True)`.
4. **[EXECUTION]** Call `containment_guard` inside `HomeIsolation.setup()` AFTER mkdtemp and BEFORE hook deploy.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_path_containment.py -v` + sub-agent review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.08/`.

**Acceptance Criteria:**
- Function `containment_guard()` raises `HomeContainmentViolation` for: unsafe eval_id, home_path outside scratch_root prefix, scratch root symlinked to a non-allowlisted target.
- Symlink resolution runs AFTER mkdtemp creation and BEFORE hook deployment (verified by an integration test sequence).
- Allowed prefixes are sourced from `EvalConfig.allowed_scratch_roots` (T01.01), not hard-coded.
- `TASKLIST_ROOT/artifacts/D-0029/spec.md` records the 3-check sequence.

**Validation:**
- Manual check: create scratch dir as symlink to /home/user, invoke setup, confirm `HomeContainmentViolation`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.05, T01.19, T02.07
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Sub-agent delegation Required because STRICT tier + High risk per Section 5.6.

### T02.09 -- Layered defense-in-depth tests (NFR-SEC2)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-030 |
| Why | NFR-SEC2 requires tests covering scratch-is-symlink-to-HOME attack, scratch-outside-allowlist, eval_id mutation post-construction, and loader-bypass attempts. |
| Effort | M |
| Risk | High |
| Risk Drivers | security |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0030 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0030/spec.md`
- `TASKLIST_ROOT/artifacts/D-0030/notes.md`
- `TASKLIST_ROOT/artifacts/D-0030/evidence.md`

**Deliverables:**
- Pytest module `tests/cli/eval/test_defense_in_depth.py` covering 4 attack vectors with positive containment-rejection assertions.

**Steps:**
1. **[PLANNING]** Inventory the 4 attack vectors from NFR-SEC2 roadmap text.
2. **[PLANNING]** Confirm containment_guard (T02.08) is importable.
3. **[EXECUTION]** Author tests for: scratch-symlink-to-HOME, scratch-outside-allowlist, eval_id mutation post-construction, loader-bypass.
4. **[EXECUTION]** Assert each vector raises `HomeContainmentViolation`.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_defense_in_depth.py -v` + sub-agent review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.09/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_defense_in_depth.py` contains 4 tests covering the 4 NFR-SEC2 attack vectors, each asserting `HomeContainmentViolation`.
- `uv run pytest tests/cli/eval/test_defense_in_depth.py -v` exits 0 with all 4 tests passing.
- Loader-bypass test verifies that constructing `HomeIsolation` without going through SuiteLoader still fails containment.
- `TASKLIST_ROOT/artifacts/D-0030/spec.md` records the attack matrix.

**Validation:**
- Manual check: run the targeted pytest module.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Test set is independent from FR-SCH2 path-traversal tests (T01.08); these target HomeIsolation, not loader.

### T02.10 -- Hard-guard tests for real ~/.claude/ (NFR-SEC3)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-031 |
| Why | NFR-SEC3 requires HomeIsolation.setup() refuses HOME outside known scratch dirs; integration test attempts to escape into real `~/.claude/` and confirms refusal. |
| Effort | M |
| Risk | High |
| Risk Drivers | security |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0031 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0031/spec.md`
- `TASKLIST_ROOT/artifacts/D-0031/notes.md`
- `TASKLIST_ROOT/artifacts/D-0031/evidence.md`

**Deliverables:**
- Integration test `tests/cli/eval/test_hard_guard_real_home.py` asserting `HomeIsolation.setup()` refuses any HOME path resolving to the real `~/.claude/`.

**Steps:**
1. **[PLANNING]** Confirm containment_guard (T02.08) and NFR-SEC2 tests (T02.09) are landed.
2. **[PLANNING]** Design test that attempts to set `home_root` to `~/.claude/` and asserts refusal.
3. **[EXECUTION]** Author integration test asserting `HomeContainmentViolation` when HOME resolves to real `~/.claude/`.
4. **[EXECUTION]** Add a test for "scratch root somehow contains `~/.claude/`" via symlink escape.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_hard_guard_real_home.py -v` + sub-agent review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.10/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_hard_guard_real_home.py` exists and contains at least 2 tests proving HomeIsolation.setup() refuses to operate on real `~/.claude/`.
- Tests pass on a host where `~/.claude/` exists (skipped with explicit reason on hosts where it does not).
- Refusal occurs before any FS write under the rejected HOME (verified by mtime snapshot fixture).
- `TASKLIST_ROOT/artifacts/D-0031/spec.md` records the hard-guard contract.

**Validation:**
- Manual check: run the targeted pytest module.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.08, T02.09
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Mitigates R7 (maintainer runs harness against real ~/.claude/).

### T02.11 -- Implement COMP-006 HomeIsolation full component

| Field | Value |
|---|---|
| Roadmap Item IDs | R-032 |
| Why | COMP-006 is the full HomeIsolation implementation: setup/env/teardown/state_path methods backed by install_hooks adapter and containment guard. |
| Effort | L |
| Risk | Medium |
| Risk Drivers | scope |
| Tier | STRICT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0032 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0032/spec.md`
- `TASKLIST_ROOT/artifacts/D-0032/notes.md`
- `TASKLIST_ROOT/artifacts/D-0032/evidence.md`

**Deliverables:**
- Full `HomeIsolation` implementation module integrating FR-ISO1, FR-ISO2, and the install_hooks adapter.

**Steps:**
1. **[PLANNING]** Confirm FR-ISO1 (T02.07), FR-ISO2 (T02.08), NFR-SEC2 (T02.09), NFR-SEC3 (T02.10) all green.
2. **[PLANNING]** Identify install_hooks adapter entry (T02.14).
3. **[EXECUTION]** Wire setup/env/teardown/state_path methods on `HomeIsolation` per DM-006 record.
4. **[EXECUTION]** Call containment_guard inside setup and route teardown through the keep-flag.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_home_isolation.py -v` + sub-agent review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.11/`.

**Acceptance Criteria:**
- Class `HomeIsolation` exposes the 4 methods named in COMP-006 (setup, env, teardown(keep), state_path(suffix)).
- `state_path(suffix)` returns paths exclusively under the per-eval HOME (verified by `is_relative_to(home_root)` assertion).
- `teardown(keep=True)` preserves the HOME directory; `teardown(keep=False)` removes it.
- `TASKLIST_ROOT/artifacts/D-0032/spec.md` records the integrated component contract.

**Validation:**
- Manual check: build HomeIsolation, run setup -> env -> state_path -> teardown(keep=False) and verify state.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.07, T02.08, T02.09, T02.10
**Rollback:** TBD (if not specified in roadmap)
**Notes:** install_hooks adapter (T02.14) provides the hook deploy callback.

### T02.12 -- Checkpoint: Phase 2 / Tasks T02.07-T02.11

| Field | Value |
|---|---|
| Roadmap Item IDs | R-028,R-029,R-030,R-031,R-032 |
| Why | Gate: verify HomeIsolation extension, path containment guard, defense-in-depth tests, hard-guard tests, and COMP-006 full impl before atomic setup and PtyDriver land. |
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
| Deliverable IDs | D-CP02-MID-T07-T11 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T07-T11.md`

**Purpose:** Confirm HomeIsolation extension + path containment + defense-in-depth + hard-guard tests before COMP-006 finalization downstream consumers.

**Verification:**
- All 4 STRICT-tier tasks (T02.07..T02.10) pass sub-agent quality-engineer review.
- `containment_guard` rejects all 4 NFR-SEC2 attack vectors and the NFR-SEC3 real-HOME case.
- `HomeIsolation` preserves the 4 existing IsolationLayers guarantees (probe T02.05 re-runs green).

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_home_isolation_extend.py tests/cli/eval/test_path_containment.py tests/cli/eval/test_defense_in_depth.py tests/cli/eval/test_hard_guard_real_home.py tests/cli/eval/test_home_isolation.py -v` exits 0.
- IsolationLayers probe test passes after HomeIsolation extension.
- Checkpoint report `CP-P02-T07-T11.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P02-T07-T11.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T02.07-T02.11).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.07..T02.11
**Rollback:** N/A (checkpoints are read-only verifications)

### T02.13 -- Wrap HomeIsolation.setup() with atomic try/except contract (NFR-ISO2)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-033 |
| Why | NFR-ISO2 requires try/except wrap: on exception after mkdtemp, partial HOME is preserved with `keep=True` forced and `setup_failed` artifact tag written. Distinguishes harness bugs from eval failures. |
| Effort | M |
| Risk | Medium |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0033 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0033/spec.md`
- `TASKLIST_ROOT/artifacts/D-0033/notes.md`
- `TASKLIST_ROOT/artifacts/D-0033/evidence.md`

**Deliverables:**
- Atomic setup wrapper inside `HomeIsolation.setup()` writing `setup_failed` artifact tag on any post-mkdtemp exception.

**Steps:**
1. **[PLANNING]** Confirm COMP-006 (T02.11) landed.
2. **[PLANNING]** Define artifact tag location (`<home>/.eval-meta/setup_failed`).
3. **[EXECUTION]** Wrap `HomeIsolation.setup()` body in try/except after mkdtemp.
4. **[EXECUTION]** On exception, force `keep=True` and write `setup_failed` tag with exception class + traceback.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_atomic_setup.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.13/`.

**Acceptance Criteria:**
- Inducing an exception inside `HomeIsolation.setup()` after mkdtemp results in the per-eval HOME being preserved on disk.
- The preserved HOME contains a `setup_failed` artifact tag file with the exception class name.
- Eval status is set to `ERRORED` (not `FAIL`) on setup exception (verified by mock EvalRunner).
- `TASKLIST_ROOT/artifacts/D-0033/spec.md` records the failure-preservation contract.

**Validation:**
- Manual check: monkeypatch an internal call to raise, run setup, inspect preserved HOME.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.11
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Distinguishes harness bugs from eval failures per NFR-ISO2.

### T02.14 -- Adapt install_hooks for per-eval HOME (COMP-014)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-034 |
| Why | COMP-014 reuses existing `src/superclaude/cli/install_hooks.py:install_hooks` and deploys `src/superclaude/hooks/hooks.json` verbatim into the per-eval HOME; signature matches install_hooks; idempotent. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0034 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0034/spec.md`
- `TASKLIST_ROOT/artifacts/D-0034/notes.md`
- `TASKLIST_ROOT/artifacts/D-0034/evidence.md`

**Deliverables:**
- Adapter `deploy_hooks_to(home_path: Path)` in `src/superclaude/cli/eval/hook_adapter.py` invoking `install_hooks` with `home_path` as target.

**Steps:**
1. **[PLANNING]** Read existing `install_hooks` signature at `src/superclaude/cli/install_hooks.py`.
2. **[PLANNING]** Confirm `src/superclaude/hooks/hooks.json` is the source artifact.
3. **[EXECUTION]** Implement `deploy_hooks_to(home_path)` matching `install_hooks` signature.
4. **[EXECUTION]** Ensure idempotency: re-deploy on existing HOME produces identical state.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_hook_adapter.py tests/cli/test_install_hooks.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.14/`.

**Acceptance Criteria:**
- Function `deploy_hooks_to(home_path)` exists in `src/superclaude/cli/eval/hook_adapter.py` and calls `install_hooks` with `target_dir=home_path`; adapter raises `HookDeployFailed` with an `error_tag` propagated to `EvalRunner.outcome.artifacts` on `install_hooks` failure.
- Re-invocation on the same `home_path` produces identical filesystem state (idempotent); `<home_path>/.claude/hooks.json` is byte-identical to `src/superclaude/hooks/hooks.json` (SHA256 equality assertion in adapter test).
- The adapter never writes to the real `~/.claude/` (verified by mtime fixture on real HOME).
- `TASKLIST_ROOT/artifacts/D-0034/spec.md` documents the adapter contract, error tagging, and verbatim-deploy verification.

**Validation:**
- Manual check: deploy hooks twice to a scratch HOME and confirm identical state.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.11
**Rollback:** TBD (if not specified in roadmap)
**Notes:** `tests/cli/test_install_hooks.py` must remain green when adapter targets per-eval HOME.

### T02.15 -- Measure NFR-PERF1 HOME setup performance baseline

| Field | Value |
|---|---|
| Roadmap Item IDs | R-035 |
| Why | NFR-PERF1 records p50 <=2s/eval at 15-eval parallel with ~1.4s/eval target; benchmark captured in test report for adoption budget tracking. |
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
| Deliverable IDs | D-0035 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0035/spec.md`
- `TASKLIST_ROOT/artifacts/D-0035/notes.md`
- `TASKLIST_ROOT/artifacts/D-0035/evidence.md`

**Deliverables:**
- Benchmark `tests/cli/eval/test_perf_home_setup.py` running 15 parallel HomeIsolation setups and recording p50/p95.

**Steps:**
1. **[PLANNING]** Confirm COMP-006 (T02.11) and adapter (T02.14) are landed.
2. **[PLANNING]** Identify reasonable iteration count (>=30 for statistical signal).
3. **[EXECUTION]** Author benchmark spinning up 15 parallel HomeIsolation setups using ThreadPoolExecutor.
4. **[EXECUTION]** Record p50 and p95 to a JSON report at `TASKLIST_ROOT/evidence/T02.15/perf.json`.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_perf_home_setup.py -v --benchmark-only` (or equivalent).
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.15/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_perf_home_setup.py` exists and produces a JSON report with p50, p95, and per-iteration durations.
- p50 setup time is <= 2.0s at 15-eval parallel on the dev host (or test marked xfail with documented host limitation).
- Report file `perf.json` is written to `TASKLIST_ROOT/evidence/T02.15/` for trend tracking.
- `TASKLIST_ROOT/artifacts/D-0035/spec.md` documents the budget and methodology.

**Validation:**
- Manual check: run the benchmark and inspect `perf.json`.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.11, T02.14
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Baseline informs NFR-PERF3 suite-runtime tracking (T03.21).

### T02.16 -- Implement COMP-007 PtyDriver wrapping pexpect.spawn

| Field | Value |
|---|---|
| Roadmap Item IDs | R-036 |
| Why | COMP-007 wraps pexpect.spawn exposing expect_prompt_ready, inject_prompt, stdin/stdout, exit capture; satisfies FR-G1 by spawning real `claude` via PTY (no in-process SDK). |
| Effort | L |
| Risk | Medium |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 80% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None | Preferred: Sequential, Context7 |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0036 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0036/spec.md`
- `TASKLIST_ROOT/artifacts/D-0036/notes.md`
- `TASKLIST_ROOT/artifacts/D-0036/evidence.md`

**Deliverables:**
- `PtyDriver` class in `src/superclaude/cli/eval/pty_driver.py` exposing `expect_prompt_ready(timeout=)`, `inject_prompt(text)`, `write_stdin`, `read_stdout`, `wait_exit`.

**Steps:**
1. **[PLANNING]** Confirm vendored pexpect (T02.01) and ClaudeProcess adapter (T02.19) interfaces.
2. **[PLANNING]** Identify prompt-ready string the real claude binary emits.
3. **[EXECUTION]** Implement `PtyDriver` class wrapping `pexpect.spawn` with the 5 method names.
4. **[EXECUTION]** Add timeout handling and exit-code capture aligned with FR-G1.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_pty_driver.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.16/`.

**Acceptance Criteria:**
- Class `PtyDriver` in `src/superclaude/cli/eval/pty_driver.py` exposes the 5 methods named in COMP-007.
- A unit test spawns a real `claude --help` (or test-stub) subprocess via PTY and `expect_prompt_ready()` returns within the timeout.
- `wait_exit()` captures and returns the subprocess exit code accurately.
- `TASKLIST_ROOT/artifacts/D-0036/spec.md` documents the method contract and FR-G1 satisfaction.

**Validation:**
- Manual check: drive a real claude subprocess interactively via PtyDriver, capture transcript.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.01
**Rollback:** TBD (if not specified in roadmap)
**Notes:** FR-G1 (real subprocess discipline) satisfied here.

### T02.17 -- Implement COMP-011 PtyStream ANSI/buffer layer

| Field | Value |
|---|---|
| Roadmap Item IDs | R-037 |
| Why | COMP-011 strips ANSI escape sequences, provides line-buffered iterator, and raises PtyTimeout on stalled read for downstream Expect.stdout/stderr assertions. |
| Effort | M |
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
| Deliverable IDs | D-0037 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0037/spec.md`
- `TASKLIST_ROOT/artifacts/D-0037/notes.md`
- `TASKLIST_ROOT/artifacts/D-0037/evidence.md`

**Deliverables:**
- `PtyStream` class in `src/superclaude/cli/eval/pty_stream.py` providing ANSI-stripped, line-buffered iteration with timeout.

**Steps:**
1. **[PLANNING]** Confirm PtyDriver (T02.16) emits raw byte chunks.
2. **[PLANNING]** Select an ANSI strip library or implement local regex.
3. **[EXECUTION]** Implement `PtyStream` with line-buffered iterator and `PtyTimeout` exception.
4. **[EXECUTION]** Add unit tests covering ANSI-laden output, partial-line buffering, and timeout.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_pty_stream.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.17/`.

**Acceptance Criteria:**
- Class `PtyStream` strips ANSI escape sequences from byte chunks and yields line-buffered output.
- `PtyTimeout` is raised when no new line arrives within the configured timeout.
- ANSI test fixture is normalized to identical plain-text output across runs.
- `TASKLIST_ROOT/artifacts/D-0037/spec.md` documents the API.

**Validation:**
- Manual check: feed an ANSI-laden byte stream and confirm clean line output.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.16
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Consumed by Expect.stderr/stdout primitives (T04.07).

### T02.18 -- Checkpoint: Phase 2 / Tasks T02.13-T02.17

| Field | Value |
|---|---|
| Roadmap Item IDs | R-033,R-034,R-035,R-036,R-037 |
| Why | Gate: verify atomic setup, hook adapter, perf baseline, PtyDriver, and PtyStream before ClaudeProcess adapter and capability gate tests land. |
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
| Deliverable IDs | D-CP02-MID-T13-T17 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T13-T17.md`

**Purpose:** Confirm atomic setup, hook adapter, perf baseline, PtyDriver, PtyStream before ClaudeProcess wiring.

**Verification:**
- Atomic setup preserves partial HOME on exception with `setup_failed` tag.
- `deploy_hooks_to` is idempotent on a scratch HOME.
- `PtyDriver` spawns a real `claude` test-stub via PTY and captures exit code.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_atomic_setup.py tests/cli/eval/test_hook_adapter.py tests/cli/eval/test_perf_home_setup.py tests/cli/eval/test_pty_driver.py tests/cli/eval/test_pty_stream.py -v` exits 0.
- Performance report `TASKLIST_ROOT/evidence/T02.15/perf.json` exists.
- Checkpoint report `CP-P02-T13-T17.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P02-T13-T17.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T02.13-T02.17).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.13..T02.17
**Rollback:** N/A (checkpoints are read-only verifications)

### T02.19 -- Implement COMP-013 ClaudeProcess reuse adapter (no in-process SDK)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-038 |
| Why | COMP-013 wraps existing `cli/pipeline/process.py:24-150` to spawn the real claude binary with HomeIsolation.env(); preserves stdout/stderr separation; ban-import lint rule rejects `anthropic` SDK imports under `cli/eval/`. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0038 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0038/spec.md`
- `TASKLIST_ROOT/artifacts/D-0038/notes.md`
- `TASKLIST_ROOT/artifacts/D-0038/evidence.md`

**Deliverables:**
- `ClaudeProcessAdapter` in `src/superclaude/cli/eval/claude_process.py` wrapping `cli/pipeline/process.py` for real claude spawn; ruff/lint rule banning `anthropic` SDK imports under `src/superclaude/cli/eval/`.

**Steps:**
1. **[PLANNING]** Read `src/superclaude/cli/pipeline/process.py` lines 24-150 to inventory ClaudeProcess interface.
2. **[PLANNING]** Confirm PtyDriver (T02.16) and HomeIsolation.env() (T02.11) interfaces.
3. **[EXECUTION]** Implement `ClaudeProcessAdapter` invoking real claude via PtyDriver with HomeIsolation.env().
4. **[EXECUTION]** Add a ruff lint rule banning `import anthropic` under `src/superclaude/cli/eval/`.
5. **[VERIFICATION]** Run `uv run ruff check src/superclaude/cli/eval/ && uv run pytest tests/cli/eval/test_claude_process_adapter.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.19/`.

**Acceptance Criteria:**
- Class `ClaudeProcessAdapter` spawns real claude with `cwd` pinned, `HomeIsolation.env()` injected, and stdout/stderr separated.
- `uv run ruff check src/superclaude/cli/eval/` flags any `anthropic` SDK import under that subtree.
- No `from anthropic` or `import anthropic` import exists anywhere under `src/superclaude/cli/eval/`.
- `TASKLIST_ROOT/artifacts/D-0038/spec.md` documents the adapter and lint rule.

**Validation:**
- Manual check: add a synthetic `import anthropic` line and confirm `ruff check` flags it.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.11, T02.16
**Rollback:** TBD (if not specified in roadmap)
**Notes:** FR-G1 (real subprocess discipline) reinforced by ban-import rule.

### T02.20 -- Pin claude version range in eval doctor (R1-mit)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-039 |
| Why | R1-mit pins supported claude version range and enforces in doctor: min_version 0.5.0, max_version recorded; doctor fails closed on out-of-range. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0039 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0039/spec.md`
- `TASKLIST_ROOT/artifacts/D-0039/notes.md`
- `TASKLIST_ROOT/artifacts/D-0039/evidence.md`

**Deliverables:**
- `_check_claude_version()` helper inside `eval doctor` parsing `claude --version` and rejecting out-of-range; min_version 0.5.0 recorded.

**Steps:**
1. **[PLANNING]** Confirm eval doctor (T01.13) command implementation.
2. **[PLANNING]** Determine claude version-output parse regex.
3. **[EXECUTION]** Add `_check_claude_version()` invoked at doctor preflight; record min 0.5.0.
4. **[EXECUTION]** Wire doctor to exit 2 when version is below the floor.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_doctor_version.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.20/`.

**Acceptance Criteria:**
- Function `_check_claude_version()` rejects claude installations below 0.5.0 with exit 2.
- A reference fixture stubbing `claude --version` at 0.4.0 fails the doctor check.
- Version floor is sourced from `EvalConfig` (not hard-coded in doctor).
- `TASKLIST_ROOT/artifacts/D-0039/spec.md` records the version policy.

**Validation:**
- Manual check: stub claude binary at 0.4.0 and run doctor; confirm exit 2.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.13
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Mitigates R1 (Claude Code TTY behavior change).

### T02.21 -- TEST-002 containment unit tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-040 |
| Why | TEST-002 is a first-class test deliverable proving allowed roots accepted, non-allowlisted roots rejected, loader-bypass defense at HomeIsolation, and exit-code-2 path covered. |
| Effort | M |
| Risk | High |
| Risk Drivers | security |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0040 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0040/spec.md`
- `TASKLIST_ROOT/artifacts/D-0040/notes.md`
- `TASKLIST_ROOT/artifacts/D-0040/evidence.md`

**Deliverables:**
- Pytest module `tests/cli/eval/test_containment.py` covering allowed roots, rejected roots, loader-bypass, and exit-2 path.

**Steps:**
1. **[PLANNING]** Confirm FR-ISO2 (T02.08), AC12 (T01.19), NFR-SEC2 (T02.09) are landed.
2. **[PLANNING]** Enumerate test cases per TEST-002 AC.
3. **[EXECUTION]** Author `tests/cli/eval/test_containment.py` with one test per case.
4. **[EXECUTION]** Add an exit-code assertion confirming exit 2 on each rejection.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_containment.py -v` + sub-agent review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.21/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_containment.py` contains tests for: repo `.dev` accepted, `/tmp` accepted, non-allowlisted root rejected, loader-bypass rejected, exit-2 path covered.
- `uv run pytest tests/cli/eval/test_containment.py -v` exits 0 with all assertions passing.
- Loader-bypass test constructs HomeIsolation directly (without SuiteLoader) and confirms containment still applies.
- `TASKLIST_ROOT/artifacts/D-0040/spec.md` documents the test matrix.

**Validation:**
- Manual check: run the targeted pytest module.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.19, T02.08, T02.09
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Cross-links AC12 + FR-ISO2 + NFR-SEC2.

### T02.22 -- TEST-003 symlink attack tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-041 |
| Why | TEST-003 is a first-class test deliverable proving symlink resolution catches scratch and HOME escape attempts AFTER creation BEFORE hook deploy; partial HOME preserved; setup_failed tag asserted. |
| Effort | M |
| Risk | High |
| Risk Drivers | security |
| Tier | STRICT |
| Confidence | [█████████-] 95% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Required |
| Deliverable IDs | D-0041 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0041/spec.md`
- `TASKLIST_ROOT/artifacts/D-0041/notes.md`
- `TASKLIST_ROOT/artifacts/D-0041/evidence.md`

**Deliverables:**
- Pytest module `tests/cli/eval/test_symlink_attacks.py` covering scratch->HOME symlink, nested symlink escape, partial-HOME preservation, and setup_failed tag.

**Steps:**
1. **[PLANNING]** Confirm FR-ISO2 (T02.08), NFR-SEC3 (T02.10), atomic setup (T02.13) are landed.
2. **[PLANNING]** Enumerate symlink attack scenarios.
3. **[EXECUTION]** Author tests building filesystem fixtures with symlink traps.
4. **[EXECUTION]** Assert containment rejection + partial HOME preservation + setup_failed tag.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_symlink_attacks.py -v` + sub-agent review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.22/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_symlink_attacks.py` contains tests for: scratch symlink to real HOME rejected, nested symlink escape rejected, partial HOME preserved, setup_failed tag asserted.
- `uv run pytest tests/cli/eval/test_symlink_attacks.py -v` exits 0 with all 4+ tests passing.
- Tests assert the rejection occurs AFTER mkdtemp creation AND BEFORE hook deploy.
- `TASKLIST_ROOT/artifacts/D-0041/spec.md` documents the attack matrix.

**Validation:**
- Manual check: run the targeted pytest module.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.08, T02.10, T02.13
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Mitigates the scratch-symlink-to-$HOME attack vector explicitly.

### T02.23 -- TEST-004 capability gate tests

| Field | Value |
|---|---|
| Roadmap Item IDs | R-042 |
| Why | TEST-004 validates HARD, SOFT-SKIP, and SOFT-XFAIL capability classifications including `--no-mcp` behavior; doctor renders statuses. |
| Effort | M |
| Risk | Low |
| Risk Drivers | None |
| Tier | STANDARD |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Direct test execution |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0042 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0042/spec.md`
- `TASKLIST_ROOT/artifacts/D-0042/notes.md`
- `TASKLIST_ROOT/artifacts/D-0042/evidence.md`

**Deliverables:**
- Pytest module `tests/cli/eval/test_capability_classifications.py` covering HARD/SOFT-SKIP/XFAIL classifications and `--no-mcp` flag behavior.

**Steps:**
1. **[PLANNING]** Confirm COMP-009 (T01.11) and FR-CLI4 doctor (T01.13) interfaces.
2. **[PLANNING]** Enumerate classification cases: missing claude (HARD), missing MCP (SOFT-SKIP), XFAIL fixture.
3. **[EXECUTION]** Author tests stubbing `shutil.which` to simulate missing binaries.
4. **[EXECUTION]** Add `--no-mcp` flag test confirming MCP evals are SKIPPED.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_capability_classifications.py -v`.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.23/`.

**Acceptance Criteria:**
- File `tests/cli/eval/test_capability_classifications.py` contains tests for: missing claude fails HARD, `--no-mcp` soft-skips MCP evals, XFAIL classification supported.
- `uv run pytest tests/cli/eval/test_capability_classifications.py -v` exits 0 with all 3+ tests passing.
- Doctor command output renders the correct status string per classification.
- `TASKLIST_ROOT/artifacts/D-0042/spec.md` documents the classification matrix.

**Validation:**
- Manual check: run doctor with PATH excluding jq and confirm HARD message.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.11, T01.13
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Validates COMP-009 + FR-CLI4 contract together.

### T02.24 -- Checkpoint: Phase 2 / Tasks T02.19-T02.23

| Field | Value |
|---|---|
| Roadmap Item IDs | R-038,R-039,R-040,R-041,R-042 |
| Why | Gate: verify ClaudeProcess adapter, version pin, containment tests, symlink attack tests, capability gate tests before scratch root policy and drift checklist close M2. |
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
| Deliverable IDs | D-CP02-MID-T19-T23 |

**Checkpoint Report Path:** `TASKLIST_ROOT/checkpoints/CP-P02-T19-T23.md`

**Purpose:** Confirm ClaudeProcess adapter + version pin + first-class containment/symlink/capability tests before M2 close.

**Verification:**
- `ruff check src/superclaude/cli/eval/` flags any synthetic `anthropic` import.
- `_check_claude_version` rejects 0.4.0 stub binaries.
- TEST-002, TEST-003, TEST-004 modules pass green.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/test_claude_process_adapter.py tests/cli/eval/test_doctor_version.py tests/cli/eval/test_containment.py tests/cli/eval/test_symlink_attacks.py tests/cli/eval/test_capability_classifications.py -v` exits 0.
- `uv run ruff check src/superclaude/cli/eval/` exits 0.
- Checkpoint report `CP-P02-T19-T23.md` records pass/fail per upstream task.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P02-T19-T23.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T02.19-T02.23).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.19..T02.23
**Rollback:** N/A (checkpoints are read-only verifications)

### T02.25 -- Enforce scratch root policy across config/isolation/CLI (OPS-002)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-043 |
| Why | OPS-002 documents and enforces allowed scratch roots across config, isolation, and `--output-dir`; policy appears in doctor failures. |
| Effort | S |
| Risk | Medium |
| Risk Drivers | scope (cross-cutting policy) |
| Tier | STRICT |
| Confidence | [████████--] 85% |
| Requires Confirmation | No |
| Critical Path Override | Yes |
| Verification Method | Sub-agent (quality-engineer) |
| MCP Requirements | Required: Sequential, Serena | Preferred: Context7 |
| Fallback Allowed | No |
| Sub-Agent Delegation | Recommended |
| Deliverable IDs | D-0043 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0043/spec.md`
- `TASKLIST_ROOT/artifacts/D-0043/notes.md`
- `TASKLIST_ROOT/artifacts/D-0043/evidence.md`

**Deliverables:**
- Policy documentation in `docs/eval/scratch-roots.md` plus consistent doctor failure messages naming the policy.

**Steps:**
1. **[PLANNING]** Confirm AC12 allowlist (T01.19) and FR-ISO2 guard (T02.08) are landed.
2. **[PLANNING]** Identify doctor failure-message format.
3. **[EXECUTION]** Author `docs/eval/scratch-roots.md` documenting the 3 allowed roots.
4. **[EXECUTION]** Update doctor + CLI run failure messages to name the policy verbatim.
5. **[VERIFICATION]** Run `uv run pytest tests/cli/eval/test_scratch_root_policy.py -v` + sub-agent review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.25/`.

**Acceptance Criteria:**
- File `docs/eval/scratch-roots.md` exists and documents `/tmp/eval-runs/`, repo `.dev/eval-runs/`, and `--output-dir` as the 3 allowed roots.
- Doctor failure messages quote the policy text exactly when a non-allowlisted root is supplied.
- `EvalConfig.allowed_scratch_roots` (T01.01) remains the single source of truth.
- `TASKLIST_ROOT/artifacts/D-0043/spec.md` records the cross-module policy.

**Validation:**
- Manual check: invoke doctor with `--output-dir /etc/foo` and confirm the failure message names the policy.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T01.01, T01.19, T02.08
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Policy crystallizes the FR-ISO2 + AC12 contract for users.

### T02.26 -- Document quarterly ptytest drift review checklist (R5-mit)

| Field | Value |
|---|---|
| Roadmap Item IDs | R-044 |
| Why | R5-mit documents review steps and target dates; CHECKLIST.md in `cli/eval/pty/` names review owner and quarterly cadence. |
| Effort | S |
| Risk | Low |
| Risk Drivers | None |
| Tier | EXEMPT |
| Confidence | [█████████-] 90% |
| Requires Confirmation | No |
| Critical Path Override | No |
| Verification Method | Skip verification |
| MCP Requirements | None |
| Fallback Allowed | Yes |
| Sub-Agent Delegation | None |
| Deliverable IDs | D-0044 |

**Artifacts (Intended Paths):**
- `TASKLIST_ROOT/artifacts/D-0044/spec.md`
- `TASKLIST_ROOT/artifacts/D-0044/notes.md`
- `TASKLIST_ROOT/artifacts/D-0044/evidence.md`

**Deliverables:**
- Updated `src/superclaude/cli/eval/pty/CHECKLIST.md` with quarterly review steps, owner, and target dates.

**Steps:**
1. **[PLANNING]** Confirm AC10 PROVENANCE (T02.03) is landed.
2. **[PLANNING]** Identify review owner from roadmap (RyanW).
3. **[EXECUTION]** Author CHECKLIST.md with the 5-step quarterly procedure.
4. **[EXECUTION]** Add target review dates aligned with calendar quarters.
5. **[VERIFICATION]** Manual review.
6. **[COMPLETION]** Save evidence under `TASKLIST_ROOT/evidence/T02.26/`.

**Acceptance Criteria:**
- File `src/superclaude/cli/eval/pty/CHECKLIST.md` lists the 5-step review procedure with owner = RyanW.
- File records quarterly cadence with at least the next 2 target review dates.
- AC10 cross-reference is recorded in CHECKLIST.md.
- `TASKLIST_ROOT/artifacts/D-0044/spec.md` records the checklist content.

**Validation:**
- Manual check: read CHECKLIST.md and confirm fields are present.
- Evidence: linkable artifact produced (spec/test log/screenshot/doc).

**Dependencies:** T02.03
**Rollback:** TBD (if not specified in roadmap)
**Notes:** Mitigates R5 (ptytest fork drift).

### T02.27 -- Checkpoint: End of Phase 2

| Field | Value |
|---|---|
| Roadmap Item IDs | R-023..R-044 |
| Why | M2 exit gate: HomeIsolation refuses any HOME outside allowed scratch roots, PtyDriver spawns real claude against a 1-eval suite end-to-end, symlink attack negative case covered, PROVENANCE records vendored ptytest SHA. |
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

**Purpose:** M2 exit gate: isolation + process + vendored ptytest land; security guards green; doctor recognizes pinned claude version.

**Verification:**
- HomeIsolation refuses any HOME outside `EvalConfig.allowed_scratch_roots` (verified by T02.21 + T02.10 tests).
- PtyDriver spawns real claude against a 1-eval suite and captures exit code via ClaudeProcessAdapter.
- PROVENANCE.md records the vendored ptytest SHA and quarterly review cadence.

**Exit Criteria:**
- `uv run pytest tests/cli/eval/ -v` passes for M2 modules.
- `uv run ruff check src/superclaude/cli/eval/` exits 0.
- Checkpoint report `CP-P02-END.md` records pass/fail per task in Phase 2.

**Steps:**
1. **[VERIFICATION]** Confirm each artifact listed in Verification is present.
2. **[VERIFICATION]** Re-run the tier-proportional checks for the covered tasks.
3. **[VERIFICATION]** Write the checkpoint report to the Checkpoint Report Path above.

**Acceptance Criteria:**
- File `TASKLIST_ROOT/checkpoints/CP-P02-END.md` exists and contains `status: PASS`.
- All 3 Verification bullets are confirmed.
- All 3 Exit Criteria bullets are met.
- Checkpoint report includes the task IDs it covers (T02.01-T02.26).

**Validation:**
- Manual check: reviewer confirms the report at the Checkpoint Report Path.
- Evidence: the generated checkpoint markdown file.

**Dependencies:** T02.01..T02.26
**Rollback:** N/A (checkpoints are read-only verifications)
