---
spec_source: "release-spec-accept-spec-change.md"
generated: "2026-03-20T00:00:00Z"
generator: "claude-opus-4-6-requirements-extractor"
functional_requirements: 13
nonfunctional_requirements: 5
total_requirements: 18
complexity_score: 0.65
complexity_class: MEDIUM
domains_detected: [backend, cli, state-management, filesystem]
risks_identified: 5
dependencies_identified: 4
success_criteria_count: 15
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 132.0, started_at: "2026-03-20T17:05:27.909343+00:00", finished_at: "2026-03-20T17:07:39.927599+00:00"}
---

## Functional Requirements

### FR-2.24.2.1: Locate state file
**Priority**: High | **Domain**: filesystem, state-management

Read `.roadmap-state.json` from `output_dir`. If absent or unreadable, exit with code 1 and message: "No .roadmap-state.json found in \<output_dir\>. Run `roadmap run` first."

**Acceptance Criteria**:
- AC: Command exits 1 with clear message when state file is missing

**Dependencies**: None

---

### FR-2.24.2.2: Recompute current spec hash
**Priority**: High | **Domain**: backend, filesystem

Load `spec_file` path from the state file. Recompute `sha256(spec_file.read_bytes())`. If the file is missing, exit with error: "Spec file not found: \<path\>".

**Acceptance Criteria**:
- AC: Command exits 1 with clear message when spec file is missing

**Dependencies**: FR-2.24.2.1

---

### FR-2.24.2.3: Check for hash mismatch
**Priority**: High | **Domain**: state-management

If `current_hash == state["spec_hash"]`, print "Spec hash is already current. Nothing to do." and exit 0.

**Sub-requirements**:
- **FR-2.24.2.3a**: If `state["spec_hash"]` is absent, null, or empty string, treat as mismatch (proceed to FR-2.24.2.4, do not exit 0)
- **FR-2.24.2.3b**: Hash comparison uses byte-exact string equality on hex digest — no case folding or normalization

**Acceptance Criteria**:
- AC-3: `accept-spec-change` is idempotent — running twice does not corrupt state

**Dependencies**: FR-2.24.2.1, FR-2.24.2.2

---

### FR-2.24.2.4: Scan for accepted deviation evidence
**Priority**: High | **Domain**: filesystem, backend

Glob `output_dir` for `dev-*-accepted-deviation.md`. Parse YAML frontmatter. Collect records where `disposition: ACCEPTED` (case-insensitive) AND `spec_update_required: true` (YAML boolean, NOT string `"true"`).

**Sub-requirements**:
- **FR-2.24.2.4a**: Absent `disposition` → not-ACCEPTED (no match)
- **FR-2.24.2.4b**: Absent `spec_update_required` → treat as `false` (no match)
- **FR-2.24.2.4c**: `spec_update_required` MUST be YAML boolean (`true`/`false`); quoted string `"true"` does NOT match
- **FR-2.24.2.4d**: YAML parse exceptions → emit warning to stderr (`[roadmap] WARNING: Could not parse frontmatter in <filename>. Skipping.`), continue processing remaining files
- **FR-2.24.2.4e**: If all files fail to parse, effective matching count is zero → zero-records path applies
- **FR-2.24.2.4f**: Zero matching records → exit 1 with message directing user to either run without `--resume` or create a deviation record

**Acceptance Criteria**:
- AC-1: `accept-spec-change` exits 1 with clear message when no accepted deviation records found

**Dependencies**: FR-2.24.2.1, FR-2.24.2.2

---

### FR-2.24.2.5: Display evidence summary and prompt (interactive mode)
**Priority**: High | **Domain**: cli

Print summary of each matching deviation record (ID, severity, affected sections, rationale). Prompt user with `[y/N]`.

**Sub-requirements**:
- **FR-2.24.2.5a**: Only `y` or `Y` (single character) confirms. `yes`, `YES`, empty string, all other input treated as N (abort)
- **FR-2.24.2.5b**: Non-interactive detection via `not sys.stdin.isatty()`. If non-interactive and `auto_accept=False`, treat as N, exit 0 with "Aborted."
- **FR-2.24.2.5c**: User answers N → exit 0 with "Aborted.", state file untouched

**Acceptance Criteria**:
- AC-4: `accept-spec-change` never touches state file if user answers N
- AC-11: Non-interactive + `auto_accept=False` → exits 0 with "Aborted.", no state modification

**Dependencies**: FR-2.24.2.4

---

### FR-2.24.2.6: Update spec_hash atomically
**Priority**: High | **Domain**: state-management, filesystem

On confirmation, write to `.roadmap-state.json.tmp` then `os.replace()`. Only `spec_hash` is modified; all other keys (`steps`, `fidelity_status`, `validation`, `remediate`, `certify`, `agents`, `depth`, `last_run`) preserved verbatim.

**Acceptance Criteria**:
- AC-2: `accept-spec-change` updates only `spec_hash` — all other keys preserved
- AC-5a: Updated `spec_hash` matches value `_apply_resume()` will compare against, allowing upstream step skip

**Dependencies**: FR-2.24.2.5

---

### FR-2.24.2.7: Confirmation output
**Priority**: Medium | **Domain**: cli

Print old hash (truncated to 12 chars), new hash (truncated to 12 chars), list of accepted deviation IDs, and guidance to run `roadmap run --resume`. Exit 0.

**Acceptance Criteria**:
- AC: Both hashes truncated to 12 chars in output
- AC-5b (integration): After `accept-spec-change`, `roadmap run --resume` proceeds from spec-fidelity without re-running upstream steps (extract, generate, diff, debate, score, merge, test-strategy)

**Dependencies**: FR-2.24.2.6

---

### FR-2.24.2.8: auto_accept parameter
**Priority**: High | **Domain**: backend

Add `auto_accept: bool = False` to `execute_roadmap()` signature. When `True`, spec-patch resume cycle skips interactive prompt. When `False` (default), prompts user. Threaded through call chain: `execute_roadmap → _apply_resume_after_spec_patch → prompt_accept_spec_change`. Non-interactive + `auto_accept=False` → falls through to normal failure handling (no prompt, no cycle).

**Acceptance Criteria**:
- AC-9: `auto_accept=True` skips prompt; `auto_accept=False` prompts user
- AC-10: `execute_roadmap()` signature backward-compatible (`auto_accept` defaults to `False`)

**Dependencies**: None (executor-side)

---

### FR-2.24.2.9: Post-spec-fidelity-FAIL detection
**Priority**: High | **Domain**: backend, state-management

After `execute_pipeline()` returns with spec-fidelity FAIL, check three conditions (ALL must be true to trigger cycle):

1. `_spec_patch_cycle_count < 1` (recursion guard not exhausted)
2. `output_dir` contains `dev-*-accepted-deviation.md` files with `disposition: ACCEPTED` AND `spec_update_required: true` with `mtime > datetime.fromisoformat(state["steps"]["spec-fidelity"]["started_at"]).timestamp()`. Absent `started_at` → Condition 2 not met (fail-closed). Type conversion required: ISO 8601 string → `datetime.fromisoformat().timestamp()` before comparing with `os.path.getmtime()` float.
3. `sha256(spec_file) != initial_spec_hash` where `initial_spec_hash` is a local variable captured at `execute_roadmap()` entry. Does NOT use `state["spec_hash"]`.

**Sub-requirements**:
- **FR-2.24.2.9a**: Strict `>` operator for mtime comparison (known limitation on 1-second resolution filesystems; `>=` allowed with documented rationale)
- **FR-2.24.2.9b**: `initial_spec_hash` captured via `hashlib.sha256(config.spec_file.read_bytes()).hexdigest()` at top of `execute_roadmap()` before `execute_pipeline()`

**Acceptance Criteria**:
- AC: All three conditions must be true to trigger cycle
- AC: mtime comparison uses proper type conversion (ISO string → timestamp float)
- AC: `initial_spec_hash` (local var) used for Condition 3, not `state["spec_hash"]`

**Dependencies**: FR-2.24.2.8, FR-2.24.2.11

---

### FR-2.24.2.10: Disk-reread at resume boundary
**Priority**: High | **Domain**: state-management, backend

Before re-running `_apply_resume()`, execute 6 steps in order:

1. Re-read `.roadmap-state.json` from disk → `fresh_state` (do NOT reuse in-memory results)
2. Recompute `new_hash = sha256(spec_file)`
3. Write `new_hash` into `fresh_state["spec_hash"]`, atomic write to disk (`.tmp` + `os.replace()`). On failure: abort cycle, print error to stderr, fall through to normal failure
4. Re-read `.roadmap-state.json` again → `post_write_state` (this is passed to `_apply_resume()`)
5. Rebuild steps via `_build_steps(config)`
6. Call `_apply_resume(post_write_state, steps)`

**Sub-requirements**:
- **FR-2.24.2.10a**: Atomic write failure aborts cycle immediately with stderr message; state file guaranteed unmodified
- **FR-2.24.2.10b**: No concurrent write protection; exclusive access assumed (documented constraint)

**Acceptance Criteria**:
- AC-7: Auto-resume cycle re-reads state from disk — does not reuse in-memory results
- AC: Atomic write failure aborts cycle and falls through to normal failure

**Dependencies**: FR-2.24.2.9

---

### FR-2.24.2.11: Recursion guard
**Priority**: High | **Domain**: backend

`_spec_patch_cycle_count` is a **local variable** inside `execute_roadmap()`, initialized to `0`. Increment before entering cycle; if `>= 1`, skip. Per-invocation scope (not module/class/global). Two successive calls get independent counters.

**Acceptance Criteria**:
- AC-6: Auto-resume cycle fires at most once per `execute_roadmap()` invocation

**Dependencies**: None (executor-side)

---

### FR-2.24.2.12: Cycle outcome logging
**Priority**: Medium | **Domain**: cli, backend

Log messages at three points:
- **Cycle entry**: `[roadmap] Spec patched by subprocess. Found N accepted deviation record(s).` + `[roadmap] Triggering spec-hash sync and resume (cycle 1/1).`
- **Cycle completion**: `[roadmap] Spec-patch resume cycle complete.`
- **Cycle suppressed** (guard fires): `[roadmap] Spec-patch cycle already exhausted (cycle_count=1). Proceeding to normal failure.`

**Acceptance Criteria**:
- AC: Entry, completion, and suppression messages logged correctly

**Dependencies**: FR-2.24.2.11

---

### FR-2.24.2.13: Normal failure on cycle exhaustion
**Priority**: High | **Domain**: backend

If spec-fidelity still fails after patched resume, fall through to normal failure path (`_format_halt_output`, `sys.exit(1)`). No second cycle. `_format_halt_output` receives post-resume (second run) results only; first-run FAIL results excluded.

**Acceptance Criteria**:
- AC-8: If spec-fidelity still fails after patched resume, pipeline exits 1 normally (no loop)

**Dependencies**: FR-2.24.2.10, FR-2.24.2.11

---

## Non-Functional Requirements

### NFR-1: Atomic write integrity
**Category**: Reliability | **Priority**: High

No partial state corruption on power loss mid-write. Uses `os.replace()` which is atomic on POSIX when source and destination are on the same filesystem. Windows support is best-effort.

**Target**: Zero data loss on POSIX systems
**Measurement**: `os.replace()` atomicity; crash simulation testing

---

### NFR-2: Read-only on abort
**Category**: Safety | **Priority**: High

State file never touched if user answers N or operation is aborted.

**Target**: No writes on abort path
**Measurement**: Unit test asserting state file mtime unchanged after N

---

### NFR-3: Idempotency
**Category**: Reliability | **Priority**: High

Running `accept-spec-change` twice with the same spec change is safe. Second run exits 0 cleanly.

**Target**: Second run exits 0, state unchanged after first successful run
**Measurement**: Unit test: run twice, assert state unchanged after first

---

### NFR-4: No pipeline execution
**Category**: Safety | **Priority**: High

`accept-spec-change` command only reads/writes state — zero subprocess invocations. No `ClaudeProcess` usage in `spec_patch.py`.

**Target**: Zero subprocess invocations
**Measurement**: Code review; no `ClaudeProcess` imports in `spec_patch.py`

---

### NFR-5: Exclusive access (documented constraint)
**Category**: Concurrency | **Priority**: Medium

No concurrent write protection via file locking. Operator responsible for preventing concurrent access. Running `accept-spec-change` concurrently with `roadmap run` or another instance is not supported.

**Target**: Documented constraint
**Measurement**: README/docstring warning

---

## Complexity Assessment

**Score**: 0.65 | **Class**: MEDIUM

**Rationale**:
- **Component count (moderate)**: 1 new module (`spec_patch.py`), 2 modified files (`commands.py`, `executor.py`), 2 test files — manageable surface area
- **State management (elevated)**: Atomic write patterns, disk-reread safety property, hash consistency across multiple state transitions require careful implementation
- **Concurrency concerns (low)**: Explicitly punted via NFR-5 (documented exclusive access)
- **Integration surface (moderate)**: Auto-resume cycle in `executor.py` touches the critical path of `execute_roadmap()` with 3-condition gating, recursion guard, and 6-step disk-reread sequence
- **Edge cases (elevated)**: YAML boolean vs string distinction, mtime type conversion (ISO string → timestamp float), absent `started_at` fail-closed behavior, non-interactive detection
- **Backward compatibility (low risk)**: Single keyword argument with default value; no breaking changes
- **Expert panel review**: 21 findings (7 critical) resolved during spec development — indicates the design space has non-obvious failure modes that were caught pre-implementation

---

## Architectural Constraints

1. **Module isolation**: `spec_patch.py` imports only stdlib + PyYAML. No imports from `executor.py` or `commands.py` (prevents circular dependencies)
2. **Dependency direction**: `commands.py → spec_patch.py` and `executor.py → spec_patch.py` only. `spec_patch.py` is a leaf module
3. **Public API surface**: No new public symbols on `executor.py`. Only `execute_roadmap()` is public; all new functions use leading underscore convention
4. **Atomic write pattern**: All state file writes use `.tmp` + `os.replace()` — no direct overwrites
5. **No `_apply_resume()` modification**: All changes are additive. The existing `_apply_resume()` function is not modified
6. **Recursion guard scope**: `_spec_patch_cycle_count` MUST be local to `execute_roadmap()`, not module/class/global level
7. **Technology mandate**: PyYAML for YAML parsing; `pyyaml>=6.0` added to `pyproject.toml`
8. **CLI surface constraint**: Zero optional arguments on `accept-spec-change` command. `auto_accept` is internal-only
9. **Platform target**: POSIX primary (atomic write guarantee). Windows best-effort
10. **Data model**: `DeviationRecord` is a frozen dataclass with 7 fields and explicit type invariants

---

## Risk Inventory

1. **TOCTOU window** — Severity: **Medium** | Probability: Low
   State file modified between read and atomic write. Stale keys could be overwritten.
   *Mitigation*: NFR-5 documents exclusive access constraint; no concurrent `roadmap run` supported.

2. **Filesystem mtime resolution** — Severity: **Medium** | Probability: Low
   Files written in same second as `started_at` not detected by strict `>` comparison (HFS+, network mounts).
   *Mitigation*: FR-2.24.2.9 documents limitation; implementations may use `>=` with documented rationale.

3. **PyYAML boolean coercion** — Severity: **Low** | Probability: Low
   `yes`/`on`/`1` accepted as `true` per YAML 1.1 — broader than some users may expect.
   *Mitigation*: Intentional design; documented in spec. YAML 1.1 boolean forms explicitly accepted.

4. **Invalid YAML in deviation files** — Severity: **Low** | Probability: Medium
   Files matching glob pattern but containing invalid YAML frontmatter.
   *Mitigation*: FR-2.24.2.4d — warn to stderr, skip file, continue processing remaining files.

5. **Accidental `auto_accept=True`** — Severity: **High** | Probability: Low
   Caller accidentally passes `auto_accept=True`, updating spec hash without human review.
   *Mitigation*: Parameter is internal (not CLI flag); only sprint runner uses it. Code review gate.

---

## Dependency Inventory

| Dependency | Type | Version | Purpose |
|---|---|---|---|
| PyYAML | Library (new) | `>=6.0` | YAML frontmatter parsing in `spec_patch.py` |
| Python stdlib (`hashlib`, `os`, `sys`, `json`, `pathlib`, `datetime`) | Library (existing) | Python >=3.10 | SHA-256 hashing, atomic write, path handling, type conversion |
| Click | Library (existing) | `>=8.0.0` | CLI command definition (`click.Path(exists=True)`) |
| `executor.py` (`_apply_resume`, `_build_steps`, `_format_halt_output`, `execute_pipeline`, `read_state`) | Internal module | Current | Auto-resume cycle integration points |

---

## Success Criteria

| ID | Criterion | Threshold | Maps to |
|---|---|---|---|
| SC-1 | `accept-spec-change` exits 1 when no deviation records found | 100% of runs | AC-1 |
| SC-2 | Only `spec_hash` modified in state file on update | Zero other key changes | AC-2 |
| SC-3 | Idempotent execution — second run exits 0 | State unchanged after first | AC-3 |
| SC-4 | State file untouched on user abort (N) | mtime unchanged | AC-4 |
| SC-5a | Updated hash matches `_apply_resume()` comparison value | Hash equality verified | AC-5a |
| SC-5b | `roadmap run --resume` after accept skips upstream steps | Resumes from spec-fidelity only | AC-5b |
| SC-6 | Auto-resume fires at most once per invocation | `_spec_patch_cycle_count` guard | AC-6 |
| SC-7 | Disk-reread — no in-memory state reuse | `post_write_state` from disk | AC-7 |
| SC-8 | Pipeline exits 1 on cycle exhaustion | No infinite loop | AC-8 |
| SC-9 | `auto_accept=True` skips prompt | No stdin interaction | AC-9 |
| SC-10 | Backward-compatible signature | Existing callers unaffected | AC-10 |
| SC-11 | Non-interactive + `auto_accept=False` → abort | Exits 0 with "Aborted." | AC-11 |
| SC-12 | Hashes truncated to 12 chars in output | Visual verification | FR-2.24.2.7 |
| SC-13 | All three conditions required for cycle trigger | Any single false → no cycle | FR-2.24.2.9 |
| SC-14 | Atomic write failure aborts cycle gracefully | Falls through to normal failure | FR-2.24.2.10 |
| SC-15 | Logging messages at cycle entry, completion, suppression | All three message types emitted correctly | FR-2.24.2.12 |

---

## Open Questions

All 7 open items from the spec are marked **Resolved**. No outstanding questions remain.

| Item | Original Question | Resolution |
|---|---|---|
| Verification level | Evidence-based: requires `dev-*-accepted-deviation.md` with `spec_update_required: true` | Resolved — §1.2, FR-2.24.2.4 |
| Manual vs auto invocation | Manual: prompted. Auto: `auto_accept` parameter | Resolved — FR-2.24.2.5, FR-2.24.2.8 |
| Scope of accepted deviations | Only `spec_update_required: true` | Resolved — §1.2 |
| Command name | `accept-spec-change` | Resolved — §5.1 |
| Process architecture | Same-process + disk-reread safety | Resolved — §2.1 |
| CLI flag for non-interactive | No CLI flag — `auto_accept` is internal | Resolved — §2.1 |
| Recursion limit | 1 cycle per `execute_roadmap()` invocation | Resolved — FR-2.24.2.11 |

**Implicit gaps identified during extraction**:

1. **Subprocess contract enforcement**: The spec notes subprocess responsibilities (write deviation record before exit, patch only listed sections, exit 0) but explicitly marks them out of scope. If the subprocess violates these, the auto-resume cycle may fire with incomplete evidence. The spec acknowledges this boundary but no validation is performed.

2. **`DeviationRecord.id` extraction**: The frontmatter schema shows `id: DEV-001` but FR-2.24.2.4 does not specify behavior when `id` is absent. The `DeviationRecord` dataclass requires it — unclear if absent `id` should cause parse failure or use a default.

3. **Hash algorithm hardcoding**: SHA-256 is used throughout but never parameterized. Not a gap per se (the spec is explicit), but a future algorithm change would touch multiple files.
