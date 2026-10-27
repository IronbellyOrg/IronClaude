# D-0043 — Evidence

**Task**: T02.25 (Phase 2 — cliEval harness)
**Deliverable**: OPS-002 scratch-root policy enforcement (R-043)
**Module**: `tests/cli/eval/test_scratch_root_policy.py`

## Verification command (T02.25 Steps[5])

```
uv run pytest tests/cli/eval/test_scratch_root_policy.py -v
```

## Result

**16 passed in 0.14s** — every OPS-002 surface green; policy/code/doc agree.

Full log: `TASKLIST_ROOT/evidence/T02.25/pytest-T02.25.log`

### Per-section tally (matches the matrix in `spec.md`)

| Section                                  | Cases | Status |
|------------------------------------------|-------|--------|
| Policy constant                          | 3     | PASS   |
| Renderer (`format_scratch_root_violation`) | 3   | PASS   |
| Doctor CLI (`--output-dir` integration)  | 4     | PASS   |
| Single source of truth                   | 2     | PASS   |
| Doc anti-drift                           | 3     | PASS   |
| Doctor / default-`EvalConfig` wiring     | 1     | PASS   |
| **Total**                                | **16**| **PASS** |

## Sibling-regression check

Re-ran the full policy/config/doctor family to confirm D-0043 did not
break adjacent deliverables:

```
uv run pytest tests/cli/eval/test_doctor.py \
              tests/cli/eval/test_config.py \
              tests/cli/eval/test_scratch_root_allowlist.py \
              tests/cli/eval/test_scratch_root_policy.py -v
```

**69 passed in 0.18s** — no drift in `test_doctor.py` (FR-CLI4),
`test_config.py` (D-0001), or `test_scratch_root_allowlist.py` (D-0016).

Log: `TASKLIST_ROOT/evidence/T02.25/pytest-policy-family.log`

## Acceptance-criteria coverage

| AC | Status | Evidence |
|----|--------|----------|
| AC1 — `docs/eval/scratch-roots.md` exists and documents the 3 allowed roots | PASS | `test_scratch_roots_doc_exists`, `test_scratch_roots_doc_names_three_allowed_roots` |
| AC2 — Doctor failure messages quote the policy text exactly | PASS | `test_doctor_rejects_non_allowlisted_output_dir`, `test_doctor_rejects_real_home_output_dir`, `test_doctor_uses_default_evalconfig_allowlist` |
| AC3 — `EvalConfig.allowed_scratch_roots` (T01.01) remains the single source of truth | PASS | `test_default_allowlist_matches_policy_constant`, `test_narrowing_config_changes_what_resolve_accepts` |
| AC4 — `D-0043/spec.md` records the cross-module policy | PASS | `.dev/releases/current/cliEval/artifacts/D-0043/spec.md` (cross-module contract table + the-three-allowed-roots table) |
| AC5 — pytest exits 0 on `tests/cli/eval/test_scratch_root_policy.py` | PASS | 16 passed in 0.14s |

## Files produced

- `docs/eval/scratch-roots.md` — operator-facing policy doc (R-043 authoritative reference)
- `src/superclaude/cli/eval/config.py` — added `SCRATCH_ROOT_POLICY` constant + `format_scratch_root_violation()` renderer
- `src/superclaude/cli/eval/commands.py` — added `eval doctor --output-dir <path>` Click option; doctor now catches `ScratchRootViolation` and exits via `SCRATCH_ROOT_VIOLATION_EXIT_CODE` before HARD probes
- `src/superclaude/cli/eval/__init__.py` — re-exports `SCRATCH_ROOT_POLICY` + `format_scratch_root_violation`
- `tests/cli/eval/test_scratch_root_policy.py` — 16-test module covering 6 surfaces
- `.dev/releases/current/cliEval/artifacts/D-0043/spec.md` — deliverable contract + test matrix
- `.dev/releases/current/cliEval/artifacts/D-0043/notes.md` — design notes ("why this approach")
- `.dev/releases/current/cliEval/artifacts/D-0043/evidence.md` — this file
- `.dev/releases/current/cliEval/evidence/T02.25/pytest-T02.25.log` — primary verification log
- `.dev/releases/current/cliEval/evidence/T02.25/pytest-policy-family.log` — sibling-regression log

## Cross-module assertion sanity

Beyond the per-test PASS table, the following invariants are now
machine-checked by every CI run that includes this module:

* Policy text agreement: `SCRATCH_ROOT_POLICY` constant ≡ doc table ≡ default allowlist tuple. Drift in any one surface fails a named test.
* Single ingress: `resolve_scratch_root(config=…, output_dir=…)` is the only path-validation function the doctor calls. Bypass attempts (e.g., an inlined `if path.is_relative_to(...)` check) would fail `test_doctor_uses_default_evalconfig_allowlist`.
* Renderer coverage: every doctor CLI path that catches `ScratchRootViolation` funnels through `format_scratch_root_violation()`; the test asserts the rendered stderr contains both forensic detail AND the policy block.

## Pending follow-up

Sub-agent quality-engineer review (STRICT-tier policy for cross-module
changes) is the remaining T02.25 checklist item. It is **not** an
acceptance criterion — every AC is independently green per the table
above — but the tasklist's "Sub-Agent Delegation: Recommended" calls
for an adversarial sweep before declaring the deliverable closed.
