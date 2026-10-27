---
spec_source: "release-spec-accept-spec-change.md"
complexity_score: 0.65
adversarial: true
---

# Roadmap: v2.24.2 Accept-Spec-Change (Merged)

## Executive Summary

This release adds a `accept-spec-change` CLI command and an auto-resume cycle to the roadmap executor. When a spec file changes mid-pipeline (e.g., patched by a subprocess), the system detects accepted deviation evidence, updates the spec hash atomically, and resumes from spec-fidelity — firing at most once per invocation.

**Scope**: 1 new module (`spec_patch.py`), modifications to `commands.py` and `executor.py`, 1 new dependency (PyYAML ≥6.0), 18 functional requirements across 4 domains (backend, CLI, state-management, filesystem), 5 NFRs, 15 success criteria.

**Key architectural properties**: leaf-module isolation (no internal imports), atomic writes via `os.replace()`, mandatory disk-reread before resume decisions, single-cycle recursion guard.

**Design philosophy**: This is a reliability-focused change to the roadmap control plane. The implementation must preserve four safety invariants at all times — any weakening during implementation should trigger a pause-for-redesign rather than a workaround.

---

## Phase 1: Foundation — `spec_patch.py` Leaf Module

**Goal**: Implement the standalone `accept-spec-change` logic as an isolated leaf module with zero internal imports.

**Duration**: ~2 days

**Milestone**: `spec_patch.py` passes all unit tests independently.

### Phase 1 Preconditions

Before writing code, resolve these design questions inline (not as a separate phase — these are preconditions, not deliverables):

1. **`DeviationRecord` convention**: Confirm whether the existing codebase uses frozen dataclasses, TypedDicts, or NamedTuples for similar records. Adopt the prevailing convention. Target: frozen dataclass with 7 fields and strict type invariants unless codebase convention differs.
2. **Absent `id` handling**: Decide whether a deviation file missing the `id` field is a parse failure (skip with warning) or an error. Document the decision in a code comment.
3. **mtime comparison semantics**: The spec mandates strict `>`. If implementation requires `>=` (e.g., filesystem granularity), document the rationale in code and tests.

### Tasks

1. **Add PyYAML dependency** — Add `pyyaml>=6.0` to `pyproject.toml` dependencies.
2. **Create `DeviationRecord` dataclass** — Frozen dataclass with fields for id, severity, affected sections, rationale, disposition, spec_update_required, and source file. Strict type invariants: `spec_update_required` must be YAML boolean, not string (FR-2.24.2.4c).
3. **Implement state file loading** (FR-2.24.2.1) — Read `.roadmap-state.json` from `output_dir`; exit 1 if absent/unreadable.
4. **Implement spec hash computation** (FR-2.24.2.2) — `sha256(spec_file.read_bytes())`; exit 1 if spec file missing.
5. **Implement hash comparison** (FR-2.24.2.3, FR-2.24.2.3a, FR-2.24.2.3b) — Byte-exact hex digest equality; absent/null/empty hash treated as mismatch.
6. **Implement deviation file scanning** (FR-2.24.2.4, FR-2.24.2.4a–FR-2.24.2.4f) — Glob `dev-*-accepted-deviation.md`, parse YAML frontmatter, filter by `disposition: ACCEPTED` (case-insensitive) + `spec_update_required: true` (boolean). Warn-and-skip on parse errors (FR-2.24.2.4d). Exit 1 on zero matches (FR-2.24.2.4f).
7. **Implement interactive prompt** (FR-2.24.2.5, FR-2.24.2.5a–FR-2.24.2.5c) — Display evidence summary (ID, severity, affected sections, rationale), `[y/N]` prompt. Only `y`/`Y` confirms. Non-interactive detection via `sys.stdin.isatty()`.
8. **Implement atomic state update** (FR-2.24.2.6) — Write `.roadmap-state.json.tmp` then `os.replace()`. Modify only `spec_hash`; preserve all other keys verbatim.
9. **Implement confirmation output** (FR-2.24.2.7) — Print old/new hashes (12-char truncation), accepted deviation IDs, guidance to run `roadmap run --resume`.

### Validation

- Unit tests for each requirement: missing state file, missing spec, hash match/mismatch, absent hash in state, YAML boolean vs string distinction, invalid YAML warning, non-interactive detection, atomic write preservation of keys, idempotency (NFR-3).
- Verify NFR-4: no `ClaudeProcess` or subprocess import in `spec_patch.py`.
- Verify NFR-2: state file mtime unchanged after abort.

### Risks

- **PyYAML boolean coercion** (Low severity): YAML 1.1 accepts `yes`/`on`/`1` as true — intentional per spec. Document in code comments.
- **Invalid YAML in deviation files** (Low severity, Medium probability): FR-2.24.2.4d handles via warn-and-skip.
- **False-positive deviation matching**: Quoted `"true"` or malformed YAML could cause unintended acceptance. Strict boolean check for `spec_update_required` plus explicit warning-and-skip parse behavior. Tests for absent fields and invalid types.

---

## Phase 2: CLI Wiring — `commands.py` Integration

**Goal**: Wire `accept-spec-change` as a Click command with zero optional arguments.

**Duration**: ~0.5 days (parallelizable with Phase 3)

**Milestone**: `superclaude roadmap accept-spec-change <output_dir>` works end-to-end.

### Tasks

1. **Add Click command** in `commands.py` — `accept-spec-change` with single `output_dir` argument (`click.Path(exists=True)`). Zero optional arguments per architectural constraint.
2. **Import and call `spec_patch.py`** — Dependency direction: `commands.py → spec_patch.py` only.
3. **Document exclusive access constraint** — Add help text or docstring noting that `accept-spec-change` must not run concurrently with `roadmap run`.
4. **Integration test**: Run command against fixture directories (missing state, matching hash, deviation records present/absent, interactive and non-interactive modes).

### Validation

- SC-1: exits 1 when no deviation records found.
- SC-3: idempotent — second run exits 0.
- SC-4: state untouched on abort.
- SC-12: hashes truncated to 12 chars.

---

## Phase 3: Auto-Resume Cycle — `executor.py` Integration

**Goal**: Add post-spec-fidelity-FAIL detection and single-cycle auto-resume to `execute_roadmap()`.

**Duration**: ~2 days (parallelizable with Phase 2)

**Milestone**: Spec-patch → auto-resume → spec-fidelity re-run works end-to-end.

### Tasks

1. **Add `auto_accept` parameter** (FR-2.24.2.8) — `auto_accept: bool = False` on `execute_roadmap()`. Thread through call chain. Backward-compatible (SC-10). No public CLI flag exists for this parameter.
2. **Capture `initial_spec_hash`** (FR-2.24.2.9b) — Local variable at top of `execute_roadmap()` via `hashlib.sha256(config.spec_file.read_bytes()).hexdigest()`.
3. **Initialize recursion guard** (FR-2.24.2.11) — `_spec_patch_cycle_count = 0` as local variable in `execute_roadmap()`. Per-invocation scope; two successive calls get independent counters.
4. **Implement 3-condition detection** (FR-2.24.2.9) — After `execute_pipeline()` returns with spec-fidelity FAIL, check all three conditions:
   - Condition 1: `_spec_patch_cycle_count < 1`
   - Condition 2: deviation files with `mtime > datetime.fromisoformat(state["steps"]["spec-fidelity"]["started_at"]).timestamp()` (FR-2.24.2.9a: strict `>`). Absent `started_at` → condition not met (fail-closed).
   - Condition 3: `sha256(spec_file) != initial_spec_hash` (compared against local var, not `state["spec_hash"]`)
5. **Implement 6-step disk-reread sequence** (FR-2.24.2.10, FR-2.24.2.10a):
   1. Re-read state from disk
   2. Recompute spec hash
   3. Atomically write `spec_hash` via `.tmp` + `os.replace()`
   4. Re-read state again (post-write verification)
   5. Rebuild steps from fresh state
   6. Call `_apply_resume(post_write_state, steps)`
   - Atomic write failure → abort cycle with stderr message (SC-14).
6. **Implement cycle logging** (FR-2.24.2.12) — Entry, completion, and suppression messages (SC-15).
7. **Implement cycle exhaustion fallback** (FR-2.24.2.13) — Fall through to `_format_halt_output` + `sys.exit(1)` with second-run results only.

### Validation

- SC-5a: updated hash matches `_apply_resume()` comparison value.
- SC-5b: `roadmap run --resume` after accept skips upstream steps.
- SC-6: auto-resume fires at most once per invocation.
- SC-7: disk-reread — no in-memory state reuse.
- SC-8: exits 1 on cycle exhaustion.
- SC-9: `auto_accept=True` skips prompt.
- SC-10: existing callers unaffected by new parameter.
- SC-11: non-interactive + `auto_accept=False` → abort.
- SC-13: all three conditions required.
- SC-14: atomic write failure aborts gracefully.
- SC-15: all three log message types emitted.

### Risks

- **TOCTOU window** (Medium severity, Low probability): NFR-5 documents exclusive access. No concurrent `roadmap run` supported. *Why the mitigation is sufficient*: The `accept-spec-change` command and `roadmap run` operate on the same state file serially. The exclusive access constraint eliminates the concurrent-write scenario entirely — the TOCTOU window only exists if an operator violates the documented constraint, which is an operator error, not a system defect.
- **Filesystem mtime resolution** (Medium severity, Low probability): HFS+/network mounts may have 1-second granularity. Documented limitation; `>=` allowed with rationale.
- **Accidental `auto_accept=True`** (High severity, Low probability): Parameter is internal-only with no CLI flag. *Why the mitigation is sufficient*: The only call site for `auto_accept=True` is inside `executor.py` after all three trigger conditions are met. There is no path from CLI input to this parameter. Code review of any new `execute_roadmap()` call site must verify the `auto_accept` value — this is a review checklist item, not a runtime guard.

---

## Phase 4: Integration Testing, Hardening, and Documentation

**Goal**: End-to-end validation of the full cycle plus operator documentation as a release gate.

**Duration**: ~1.5 days

**Milestone**: All 15 success criteria pass; NFR-5 documentation reviewed and approved.

### Testing Tasks

1. **End-to-end test: happy path** — Spec patched by subprocess, deviation record created, `accept-spec-change` run, `roadmap run --resume` completes from spec-fidelity.
2. **End-to-end test: cycle exhaustion** — Spec-fidelity fails after resume → pipeline exits 1 normally (SC-8).
3. **End-to-end test: no deviation evidence** — Auto-resume cycle does not fire when conditions unmet (SC-13).
4. **Edge case tests**:
   - Absent `started_at` in state → Condition 2 not met (fail-closed).
   - ISO 8601 → timestamp float type conversion correctness.
   - YAML boolean `true` vs string `"true"` distinction.
   - Multiple deviation files, some with parse errors.
   - Two successive `execute_roadmap()` calls get independent counters.
5. **NFR verification**:
   - NFR-1: Atomic write — no partial state on simulated crash.
   - NFR-4: No subprocess invocation in `spec_patch.py`.
6. **Regression**: No regressions in existing roadmap pipeline tests.

### Documentation Tasks (NFR-5 — Release-Blocking Gate)

Documentation is part of the safety model because file locking is intentionally out of scope. NFR-5 verification is a release-blocking gate item, not optional polish.

1. **Command usage documentation**: When to run `accept-spec-change`, requirement for evidence-backed deviation files, expected follow-up `roadmap run --resume`.
2. **Exclusive access constraint**: No concurrent `accept-spec-change` with `roadmap run`. Documented in command help, docstrings, and operator guide.
3. **Internal-only `auto_accept`**: Document that this parameter has no CLI exposure and must not be added without safety review.
4. **mtime resolution limitation**: Document the known filesystem granularity issue and rationale if `>=` is used instead of strict `>`.

### Validation

- All 15 success criteria (SC-1 through SC-15) pass.
- NFR-5 documentation reviewed as a separate gate item during release review.
- No regressions in existing roadmap pipeline tests.

---

## Release Gate Invariants

The implementation is known safe if and only if these four invariants hold. If any is weakened during implementation, **pause for redesign** rather than patching around it.

| # | Invariant | Validates | How to Verify |
|---|-----------|-----------|---------------|
| 1 | `spec_patch.py` stays isolated and subprocess-free | NFR-4, architectural constraint | `grep -r "import subprocess\|ClaudeProcess" spec_patch.py` returns empty |
| 2 | Every state write uses atomic replace semantics | NFR-1, FR-2.24.2.6, FR-2.24.2.10 | All `.roadmap-state.json` writes go through `.tmp` + `os.replace()` |
| 3 | The executor resume cycle fires at most once per invocation | FR-2.24.2.11, FR-2.24.2.13 | `_spec_patch_cycle_count` incremented before cycle entry; SC-6 test passes |
| 4 | Resume decisions use disk-reloaded state, never stale in-memory state | FR-2.24.2.10, FR-2.24.2.10a, SC-7 | 6-step disk-reread sequence executed; no reference to pre-cycle state object after reread |

These invariants complement the SC validation matrix: the matrix validates *features*; this list validates *safety properties*. Both must pass for release.

---

## Success Criteria Validation Matrix

| SC | Criterion | Validated In |
|---|---|---|
| SC-1 | Exit 1 on no deviation records | Phase 1, Phase 4 |
| SC-2 | Only `spec_hash` modified | Phase 1 |
| SC-3 | Idempotent execution | Phase 1, Phase 2 |
| SC-4 | State untouched on abort | Phase 1 |
| SC-5a | Hash matches `_apply_resume()` value | Phase 3 |
| SC-5b | Resume skips upstream steps | Phase 4 |
| SC-6 | Single cycle per invocation | Phase 3 |
| SC-7 | Disk-reread, no in-memory reuse | Phase 3 |
| SC-8 | Exit 1 on cycle exhaustion | Phase 3, Phase 4 |
| SC-9 | `auto_accept=True` skips prompt | Phase 3 |
| SC-10 | Backward-compatible signature | Phase 3 |
| SC-11 | Non-interactive + no auto-accept → abort | Phase 3 |
| SC-12 | 12-char hash truncation | Phase 2 |
| SC-13 | All three conditions required | Phase 3, Phase 4 |
| SC-14 | Atomic write failure → graceful abort | Phase 3 |
| SC-15 | All log messages emitted | Phase 3 |

---

## Resource Requirements and Dependencies

### External Dependencies

| Dependency | Action Required |
|---|---|
| PyYAML ≥6.0 | Add to `pyproject.toml`, `uv pip install` |
| Python ≥3.10 | Already satisfied |
| Click ≥8.0.0 | Already satisfied |

### Internal Dependencies

| Module | Relationship |
|---|---|
| `spec_patch.py` (new) | Leaf module — no internal imports |
| `commands.py` | Imports `spec_patch.py` |
| `executor.py` | Imports `spec_patch.py`; uses existing `_apply_resume`, `_build_steps`, `_format_halt_output`, `execute_pipeline`, `read_state` |

### Phase Dependencies

```
Phase 1 ──→ Phase 2 (CLI needs spec_patch.py)
Phase 1 ──→ Phase 3 (executor needs spec_patch.py)
Phase 2 ──┐
Phase 3 ──┴→ Phase 4 (integration tests need both)
```

Phases 2 and 3 can run in parallel after Phase 1 completes.

### Engineering Roles

1. **Primary implementer** — Owns `spec_patch.py`, `executor.py` integration, and state integrity invariants.
2. **QA/reliability engineer** — Owns regression and integration test matrix; validates abort/no-write/idempotency behavior.
3. **Reviewer** — Verifies architectural constraints, no subprocess usage, backward compatibility.

### Environmental Assumptions

- POSIX is primary target for atomic write guarantee (`os.replace()` is atomic on POSIX).
- Exclusive access is assumed during command execution — no file locking in this release.

---

## Risk Assessment Summary

| Risk | Severity | Probability | Phase | Mitigation |
|---|---|---|---|---|
| TOCTOU window / state corruption | Medium | Low | 3 | NFR-5: exclusive access documented [1] |
| Filesystem mtime resolution | Medium | Low | 3 | Documented limitation; `>=` allowed with rationale |
| PyYAML boolean coercion | Low | Low | 1 | Intentional design; documented |
| Invalid YAML in deviation files | Low | Medium | 1 | Warn-and-skip (FR-2.24.2.4d) |
| Accidental `auto_accept=True` | High | Low | 3 | Internal-only parameter; code review gate [2] |

**[1] TOCTOU detail**: The exclusive access constraint eliminates concurrent writes. The TOCTOU window only exists under operator violation of the documented constraint. The atomic write path (`.tmp` + `os.replace()`) further ensures no partial state is observable even in crash scenarios. Three mitigations enforce this: atomic replace everywhere, preserve all non-`spec_hash` keys verbatim, and tests diffing pre/post state.

**[2] `auto_accept` detail**: The only call site is inside `executor.py` after all three trigger conditions are met. No CLI-to-parameter path exists. Any new `execute_roadmap()` call site adding `auto_accept=True` must be flagged during code review.

---

## Timeline Summary

| Phase | Duration | Parallelizable |
|---|---|---|
| Phase 1: Foundation | ~2 days | — |
| Phase 2: CLI Wiring | ~0.5 days | Yes (with Phase 3) |
| Phase 3: Auto-Resume Cycle | ~2 days | Yes (with Phase 2) |
| Phase 4: Testing & Documentation | ~1.5 days | — |
| **Total (with parallelism)** | **~4.5 days** | Phases 2+3 overlap |
| **Total (single implementer)** | **~6 days** | Sequential execution |

The 4.5-day estimate assumes two engineers can work Phases 2 and 3 concurrently after Phase 1 completes. A single implementer working sequentially should plan for ~6 days.

---

## Requirement Coverage Map

### Manual Acceptance Path (Phase 1 + Phase 2)
FR-2.24.2.1, FR-2.24.2.2, FR-2.24.2.3, FR-2.24.2.3a, FR-2.24.2.3b, FR-2.24.2.4, FR-2.24.2.4a, FR-2.24.2.4b, FR-2.24.2.4c, FR-2.24.2.4d, FR-2.24.2.4e, FR-2.24.2.4f, FR-2.24.2.5, FR-2.24.2.5a, FR-2.24.2.5b, FR-2.24.2.5c, FR-2.24.2.6, FR-2.24.2.7

### Executor Auto-Resume Path (Phase 3)
FR-2.24.2.8, FR-2.24.2.9, FR-2.24.2.9a, FR-2.24.2.9b, FR-2.24.2.10, FR-2.24.2.10a, FR-2.24.2.10b, FR-2.24.2.11, FR-2.24.2.12, FR-2.24.2.13

### Non-Functional Controls (All Phases)
NFR-1, NFR-2, NFR-3, NFR-4, NFR-5
