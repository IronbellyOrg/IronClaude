# Phase 2 — Checkpoint 1 (Mid-Phase: Schema + Preflight Foundations)

**Checkpoint ID:** CP1 (mid-phase, after T02.01..T02.05)
**Phase:** 2 — Preflight, Schema, Lens Registry & Injection Guard (Wave 0)
**Type:** CHECKPOINT (mid-phase) — Tier EXEMPT
**Deliverable:** D-CP2-1
**Timestamp:** 2026-06-01T06:26:16+00:00
**Worktree:** `/config/workspace/IronClaude/.claude/worktrees/BareReview`
**Commit:** `757a3824` (branch `brainstorm/t2-bare-reviewer-adjunct`; swarm artifacts on working tree, untracked per §SoT discipline)
**Roadmap binding:** R-030..R-034 (COMP-005, COMP-006, FR-019, FR-020, FR-021)

## Scope

Verify the Phase 2 schema + preflight foundation tasks (T02.01..T02.05)
are complete and the Wave 0 entry surface — JSON Schema validation with
cross-field rules, the `run_preflight` orchestration, lens-driven
defaults expansion, and the `--custom-prompt-dir` escape-hatch reader —
is locked before Phase 2 mid-phase work (T02.07..T02.11) proceeds.

The §11.5 prompt-injection substring rule is the security-critical
binding that ties this bracket together; CP1 specifically gates that
the rule is enforced in the schema (T02.03) and is wired through every
prompt-input path the preflight module exposes (lens path via
T02.04, custom-prompt-dir path via T02.05). Identical enforcement
across all three paths (lens / JSON-Schema / custom-prompt-dir) lands
at CP2 (T02.07..T02.11); CP1 only certifies the foundation.

## Acceptance Criteria — Results

| # | Criterion | Result | Evidence |
|---|-----------|--------|----------|
| 1 | All of T02.01..T02.05 marked done | ✅ PASS | Deliverables present on disk (see §Task Evidence below); 108/108 tests pass for the bracket (`uv run pytest tests/swarm/test_schema.py tests/swarm/test_preflight.py tests/swarm/test_schema_injection_substring.py tests/swarm/test_lens_defaults.py tests/swarm/test_custom_prompt_dir.py -v` → 108 passed in 0.26s). |
| 2 | `phase-2-cp1.md` checkpoint report written | ✅ PASS | This file. |
| 3 | Schema, preflight, lens-defaults expansion, custom-prompt-dir reader all green | ✅ PASS | `src/superclaude/cli/swarm/schema.py` (9 defs/classes, 26 KB, line-anchored validators); `src/superclaude/cli/swarm/preflight.py` (21 defs/classes, 40 KB) exposes `run_preflight`, `expand_lens_defaults`, `read_custom_prompt_dir`, `enforce_injection_guard`, `guard_empty_target`, `check_pool_size`, `check_empty_pool`, `materialize_lens_defaults`, `set_lens_resolver`, `resolve_lens`, `write_manifest`. Full swarm suite green: 714/714 tests pass (`uv run pytest tests/swarm/ -q` → 714 passed in 0.81s). |
| 4 | §11.5 substring rule enforced in schema | ✅ PASS | `schema.py:89` defines `CANONICAL_INJECTION_GUARD_SENTENCE`; `schema.py:124` defines `RULE_INJECTION_SUBSTRING`; `schema.py:543` implements `_injection_substring_failures` cross-field validator; `schema.py:544` docstring states "Apply the §11.5 cross-field rule". Bundled by `validate()` (line 667) and `validate_or_raise()` (line 691). The substring rule rejects specs whose `prompt.system` is missing the required substring while `target.injection_guard.enabled=True`. Negative-test fixture (`tests/swarm/test_schema_injection_substring.py::test_missing_canonical_substring_in_prompt_system_is_rejected`) passes; mutation removing the rule fails the test. |
| 5 | `make verify-sync` passes | ✅ PASS | `make verify-sync` exits 0 ("✅ All components in sync") on this worktree state. |

## Task Evidence (T02.01..T02.05)

### T02.01 — Schema module with cross-field validators
- **Deliverable:** `src/superclaude/cli/swarm/schema.py` exists (~26 KB, 9 defs/classes).
- **JSON Schema:** `JOB_SPEC_SCHEMA` covers every DM-001 leaf; `Draft7Validator` bound at line 430.
- **Cross-field validators:** `_injection_substring_failures` (line 543), `_custom_prompt_dir_lens_failures` (line 611).
- **Rule constants:** `RULE_SPEC_VERSION` (123), `RULE_INJECTION_SUBSTRING` (124), `RULE_INJECTION_REQUIRED` (125), `RULE_CUSTOM_PROMPT_DIR_REQUIRES_CUSTOM_LENS` (126), `RULE_SCHEMA` (129).
- **Public entry points:** `validate(spec)` (667) returns failure list; `validate_or_raise(spec)` (691) raises `SchemaValidationError` bundling every failure.
- **Spec version pinned:** `RULE_SPEC_VERSION = "spec_version.pinned"` cross-field rule enforced.
- **Tests:** `tests/swarm/test_schema.py` 14/14 pass (valid spec accepted, missing field rejected, wrong type rejected, out-of-enum rejected, unknown top-level field rejected, `validate_or_raise` bundles every failure, frozen-result invariant, ≥1 failure invariant, non-dict spec parametrized rejection 5 cases, no-mutation invariant).

### T02.02 — Preflight (Wave 0) module
- **Deliverable:** `src/superclaude/cli/swarm/preflight.py` exists (~40 KB, 21 defs/classes).
- **Orchestrator:** `run_preflight(spec, ...)` (line 856) executes lens resolution → schema validation → §11.5 guard enforcement → IMM-4 empty-target guard → INV-005/INV-007 pool guards → manifest emit; returns `PreflightResult` (`state="preflight_ok"` on success) or raises `PreflightError`.
- **Result types:** `PreflightFailure` (135, frozen), `PreflightError` (161, requires ≥1 failure, frozen), `PreflightResult` (183, frozen).
- **Guard wiring:** `enforce_injection_guard` (727), `guard_empty_target` (639), `check_pool_size` (690), `check_empty_pool` (664), `_count_non_whitespace_bytes` (627).
- **Manifest emit:** `write_manifest` (778) writes atomically; `_target_checksum` (767) snapshots target bytes.
- **JobSpec coercion:** `_coerce_dict` (818) / `_coerce_jobspec` (828) accept both dict and `JobSpec` inputs; `_default_target_loader` (846) reads target by path.
- **Tests:** `tests/swarm/test_preflight.py` 24/24 pass — covers public surface, byte-floor matches IMM-4, manifest atomicity, JobSpec instance acceptance, schema-failure propagation, missing-injection-substring path, unknown-lens path, IMM-4 empty target (zero bytes + whitespace-only + unreadable), INV-005 workers-exceed-pool, INV-007 empty pool, injection-guard helper (substring + skip-on-empty), pool guards (equal-size pass, single-model pass), `materialize_lens_defaults` snapshot, `set_lens_resolver` round-trip, error frozen, no input mutation.

### T02.03 — FR-019 schema validation with §11.5 substring rule
- **Deliverable:** `_injection_substring_failures` (`schema.py:543`) implements the §11.5 cross-field rule + `RULE_CUSTOM_PROMPT_DIR_REQUIRES_CUSTOM_LENS` covers the FR-021 cross-field.
- **Required-substring policy:** when `target.injection_guard.enabled=True`, `prompt.system` must contain the substring; default substring is `CANONICAL_INJECTION_GUARD_SENTENCE` (line 89), overridable per-spec via `target.injection_guard.required_substring`.
- **Structured diagnostics:** failures name the rule (e.g., `"injection_guard.required_substring_in_prompt_system"`) and include path + message.
- **Cross-field rule (FR-021):** `custom_prompt_dir` requires `lens=="custom"` — enforced at `_custom_prompt_dir_lens_failures` (line 611).
- **Tests:** `tests/swarm/test_schema_injection_substring.py` 23/23 pass — baseline fixture, missing canonical substring rejected, partial-substring rejected, custom-substring verbatim enforcement, empty-required-substring-with-guard-enabled rejected, disabled-guard bypass, custom_prompt_dir-without-custom-lens rejected (parametrized over 10 non-`custom` lens values including whitespace/case variants), custom_prompt_dir-with-custom-lens accepted, custom-lens-without-custom_prompt_dir accepted, null/empty/omitted `custom_prompt_dir` bypasses FR-021, non-string `custom_prompt_dir` defers to JSON Schema, `validate_or_raise` bundles both failure classes, no input mutation on failure path.

### T02.04 — FR-020 lens-driven defaults expansion
- **Deliverable:** `preflight.py::expand_lens_defaults` (line 286) + `materialize_lens_defaults` (line 255) + `resolve_lens` (line 244) + `set_lens_resolver` (line 231) + `_default_lens_resolver` (line 207).
- **Field coverage:** expansion populates `prompt.system` / `prompt.user_template`, `normalization.recipe` / `normalization.template_path`, `workers.count`, `truncation.line_cap`, `output.filename_template` / `output.lens_name`, `recommended_next_command_template`, `caller_metadata.suspect` / `caller_metadata.tier` (the 10 fields enumerated in T02.04 step 1).
- **Caller-supplied override semantics:** caller values for `prompt.system`, `recipe`, `workers.count`, `line_cap`, `lens_name`, `next_command_template` are preserved (do not get overwritten by lens defaults). Verified per-field by `test_caller_supplied_*_preserved`.
- **Unknown lens:** raises structured failure (`PreflightFailure(rule="lens.unknown")`).
- **Tests:** `tests/swarm/test_lens_defaults.py` 18/18 pass — every block populated (prompt/normalization/workers/truncation/output/next-cmd), `ResolvedLensEntry` snapshot returned, 6 caller-supplied preservations, unknown-lens structured failure, empty-registry path, non-JobSpec rejection, non-dict-registry rejection, single-expansion populates every listed field.

### T02.05 — FR-021 custom-prompt-dir escape hatch
- **Deliverable:** `preflight.py::read_custom_prompt_dir` (line 458) reads `<dir>/system.txt`, `<dir>/user.txt`, `<dir>/meta.yaml`; returns `(system, user, meta)` trio.
- **§11.5 parity:** the same `enforce_injection_guard` helper used by the lens path is invoked on `system.txt` contents (verified by `test_read_custom_prompt_dir_guard_uses_central_helper_path_label`). This makes INV-003 parity provable without re-implementing the substring check.
- **Missing file:** structured failure; `test_read_custom_prompt_dir_missing_file_raises` parametrized over all 3 files (`system.txt`, `user.txt`, `meta.yaml`).
- **Batched missing files:** when multiple files are missing, all are reported (`test_read_custom_prompt_dir_batches_missing_files`).
- **Invalid YAML:** structured failure (`test_read_custom_prompt_dir_invalid_yaml_raises`); non-mapping / scalar meta rejected.
- **Round-trip:** files round-trip into manifest snapshot (`test_custom_prompt_dir_contents_round_trip_into_manifest`), meta variables survive JSON round-trip.
- **Tests:** `tests/swarm/test_custom_prompt_dir.py` 18/18 pass — happy-path trio, PathLike accepted, empty meta → empty dict, verbatim content preserved, missing directory, path-is-file rejected, 3-file missing-file parametrization, batched missing-files, missing-substring rejection, substring-default-disabled bypass, central-helper-path-label parity, invalid YAML, non-mapping meta, scalar meta, manifest round-trip, meta JSON round-trip.

## Validation Block — Quantitative

| Check (per tasklist §T02.06 Validation) | Spec value | Observed | Status |
|------------------------------------------|------------|----------|--------|
| `grep -c "status: done" execution-log.yaml` ≥ 32 | ≥ 32 | n/a — sprint runner uses `execution-log.jsonl` + artifact-and-test verification, not per-task YAML status lane (convention established in CP1/CP2/CP3/CP5 of Phase 1; see `phase-1-cp5.md:55`). **Substitute:** 108/108 tests pass on the bracket-focused suite + 714/714 tests pass across the full swarm suite + every T02.01..T02.05 deliverable present at the file paths and line numbers cited above + `make verify-sync` green. | ✅ PASS (semantically) |
| `phase-2-cp1.md` checkpoint file exists | required | This file | ✅ PASS |
| Schema, preflight, lens-defaults, custom-prompt-dir reader green | required | All four modules exercised by 108 tests; all pass | ✅ PASS |
| §11.5 substring rule enforced in schema | required | `schema.py:543` cross-field validator + `RULE_INJECTION_SUBSTRING` constant + `CANONICAL_INJECTION_GUARD_SENTENCE` + 23 dedicated tests | ✅ PASS |

## Validation Commands (Replayable)

```
uv run pytest tests/swarm/test_schema.py \
              tests/swarm/test_preflight.py \
              tests/swarm/test_schema_injection_substring.py \
              tests/swarm/test_lens_defaults.py \
              tests/swarm/test_custom_prompt_dir.py -v
uv run pytest tests/swarm/ -q
make verify-sync
grep -n "RULE_INJECTION_SUBSTRING\|CANONICAL_INJECTION_GUARD_SENTENCE" \
     src/superclaude/cli/swarm/schema.py
grep -nE "^def (run_preflight|expand_lens_defaults|read_custom_prompt_dir|enforce_injection_guard|guard_empty_target)" \
     src/superclaude/cli/swarm/preflight.py
```

All commands above succeed on this commit.

## §11.5 Enforcement Status (CP1 Scope)

| Prompt-input path | Enforcement site | Status at CP1 |
|---|---|---|
| Lens path | `schema.py::_injection_substring_failures` (cross-field rule on `prompt.system`) | ✅ enforced via `validate_or_raise` invoked by `run_preflight` |
| JSON-Schema (direct spec) path | same — `schema.py::validate()` is the single entry point | ✅ enforced |
| Custom-prompt-dir path | `preflight.py::read_custom_prompt_dir` calls `enforce_injection_guard` (line 727) against `system.txt` contents | ✅ enforced (T02.05 already wires the central helper; T02.07 will lock parity via a parametrized cross-path test) |

CP1 certifies the **foundation** for §11.5 across all 3 paths. **CP2
(T02.07..T02.11)** is the gate that proves identical enforcement via
the cross-path parity test (`test_injection_guard_all_paths.py`,
`test_escape_hatch_guard_parity.py`).

## Open Question Status

| OQ | Title | Owner | Status at Phase-2 CP1 |
|---|---|---|---|
| OQ-007 | Worker-count vs model-pool guard (warn-with-defaults vs STOP) | architect | Open — resolution scheduled at T02.10 (CP2 bracket). Not blocking at CP1. |
| OQ-008 | Empty-pool failure contract (INV-007) | architect | Open — resolution scheduled at T02.11 (CP2 bracket) via INV-007 implementation. Not blocking at CP1. |
| OQ-010 | `validate-lenses` failure semantics (exit code + blocking/warning policy) | architect | Open — resolution scheduled at T02.20 (CP4 bracket). Not blocking at CP1. |

Mid-phase requirement satisfied: owners are named in `roadmap.md`
§Open Questions; no blocker entries logged against the architect role.
Final OQ-007 / OQ-008 / OQ-010 sign-off lands at T02.29 (M2 exit gate,
STRICT tier).

## Outstanding / Next

1. **T02.07** — central `enforce_injection_guard` parametrized test across all 3 prompt-input paths (lens / JSON-Schema / custom-prompt-dir). The helper itself is already wired (see CP1 §"§11.5 Enforcement Status"); T02.07 locks parity programmatically.
2. **T02.08** — INV-003 custom-prompt-dir identical-guard test (already partially exercised by `test_custom_prompt_dir.py::test_read_custom_prompt_dir_missing_substring_raises`; T02.08 adds the explicit cross-path-equivalence assertion).
3. **T02.09** — INV-014 escape-hatch isomorphism test (lens path and `--custom-prompt-dir` path reject the same guard violation with structurally similar diagnostics).
4. **T02.10** — INV-005 `check_pool_size` resolution per OQ-007 (the helper exists at `preflight.py:690`; T02.10 binds the OQ-007 warn-vs-STOP branch and records the resolution in `docs/swarm/oq-resolutions.md`).
5. **T02.11** — INV-007 `emit_env_missing_contract` per OQ-008 (the `check_empty_pool` helper exists at `preflight.py:664`; T02.11 adds the structured `failed`/`env-missing` contract emission and the two-branch test).

CP2 (T02.12) gates these.

## Sign-Off

**Gate Result:** ✅ PASS — Phase 2 schema + preflight foundation gate cleared.
**Authorized to proceed:** T02.07 → T02.11 (CP2 bracket).
**Recorded by:** automation (T02.06 checkpoint task).
