# FINAL QA Gate — Fix Record (cycle 1, serialized single writer)

Date: 2026-06-20
Consolidated verdict was FAIL. Per the consolidated findings triage
(`qa-consolidated-findings.md`), the ACCEPTED fixes A-D were applied by the
orchestrator as the single serialized writer (I20). REJECTED findings R1-R13 were
not changed — each is documented with rationale in the consolidated findings
(scope over-reach, decision-governed, table-allowed, or verdict-provably-correct).

## Fixes applied

### A. [CRITICAL] reflect-review lens brief now drives the worker prompt
- `src/superclaude/cli/reflect/ensemble.py`: added `build_worker_prompt(config)` +
  `_load_review_target(config)`; `run_tier2_ensemble` now sends the lens
  `system_prompt_fragment` + `user_template` (over the tasklist target) to each
  worker instead of the `/sc:reflect` slash command. Imported the lens entry
  (`_REFLECT_REVIEW_LENS_ENTRY`).
- `src/superclaude/cli/reflect/runner.py`: `_audit_once` now calls
  `run_tier2_ensemble(config)` (no slash-command prompt passed).
- New test `test_i10_lens_brief_drives_worker_prompt` asserts the worker prompt is
  the lens brief (contains the Tier-2 reflection framing + `<<<TARGET>>>`, no
  `{target_content}` placeholder, no `/sc:reflect`).

### B. [IMPORTANT] t2_vendor_diversity is now vendor-classified
- `src/superclaude/cli/reflect/ensemble.py`: restored `_vendor_from_model_id`;
  `compute_vendor_diversity` returns "single" when all succeeded reviewers share a
  vendor, "multi" for ≥2 vendors, None for <2 survivors. Distinct same-vendor
  models now correctly read "single" (smoke-verified: gpt-4/gpt-3.5 → "single").
- Production stub factory now binds vendor-distinct `stub_model_id`s
  (`qwen-stub-00`, `deepseek-stub-01`, …) so a credit-free `--transport stub` run
  is genuinely PASS-eligible on BOTH model-class and vendor diversity. Updated U3
  and the integration `_distinct_stub` to the new scheme.

### C. [IMPORTANT] production `_audit_once` → ensemble route now tested
- New test `test_i11_production_audit_once_routes_tier2_to_ensemble`: with the real
  `ClaudeProcess` identity seam, a `depth=deep` `_audit_once` calls
  `run_tier2_ensemble` (spied) — proving the production route hits the ensemble,
  not a single audit ClaudeProcess.

### D. [MINOR] DoD/Phase-8 NFR-RH2.6 wording
- Recorded in the Phase 8 finding that `test_no_nesting_guard.py` was intentionally
  EXTENDED (Step 7.1/FR-RH2.8); NFR-RH2.6's "unchanged" scope is the B1/B2/B3 +
  fix_loop + marker_suppression floor (confirmed `git diff` empty by the
  backward-compat lens). Reflected in this record.

## Verification (post-fix)
- `uv run pytest tests/cli/reflect -q` → 103 passed, 1 xpassed (was 101+1; +I10, +I11).
- Forbidden NFR-7 tokens in `ensemble.py`: NONE.
- Touched-surface `ruff check` + `ruff format --check`: CLEAN (6 files).
- `tests/cli/reflect/test_no_nesting_guard.py` → 5 passed, 1 xpassed (ensemble.py
  still has `ClaudeProcess`, no raw subprocess).
- Re-captured evidence: `phase6-integration-full-output.txt` (11 passed),
  `phase3-u3u4u5u6u8-output.txt` (13 passed), `phase7-u7u9-guard-output.txt`.

Every ACCEPTED consolidated finding of every severity is addressed. No fix
introduced a forbidden NFR-7 token or broke the backward-compat floor.

## Cycle 2 (verification-round findings addressed)

The cycle-1 verification round (2 agents) returned FAIL with three IMPORTANT
findings; triage + fixes:

- **[ACCEPTED] I10 `/sc:reflect` exclusion was fixture-dependent (content lens).**
  The real tasklist target legitimately contains `/sc:reflect` references; the
  worker prompt may quote them inside `<<<TARGET>>>` but must never be the worker
  INSTRUCTION. Strengthened I10: it now appends a `/sc:reflect` line to the
  tasklist body, partitions the prompt at `<<<TARGET>>>`, asserts the instruction
  prefix starts with the lens fragment and contains NO `/sc:reflect`, and asserts
  the `/sc:reflect` body reference survives ONLY inside the target block. Now
  fixture-independent.
- **[ACCEPTED] Fix C missing the Tier-1 negative (structural lens).** Added
  `test_i11b_tier1_audit_once_does_not_call_ensemble`: a `depth="quick"` (Tier-1)
  config (built via `dataclasses.replace`, since resolve_config floors quick→
  standard) drives `_audit_once` with `ClaudeProcess` patched and
  `run_tier2_ensemble` spied — asserts the ensemble spy is NOT called and the
  Tier-1 `ClaudeProcess` IS constructed.
- **[REJECTED] Fix D "edit the task-instruction prose" (structural lens).** Steps
  4.2/8.1's "NO existing test modified" are IMMUTABLE checklist items (executor
  rule F4 forbids rewriting checklist items). Their "existing tests" scope is the
  B1/B2/B3 + fix_loop + marker_suppression floor; Step 7.1 separately and
  explicitly authorizes extending `test_no_nesting_guard.py` (FR-RH2.8). The
  scoping clarification is recorded in the editable DoD matrix (NFR-RH2.6 row) and
  the Phase 8 finding — the substance of D is captured without violating F4.

### Cycle 2 verification
- `uv run pytest tests/cli/reflect -q` → 104 passed, 1 xpassed (+I11b).
- `uv run pytest tests/cli/reflect/test_ensemble_stub_integration.py -v` → 12 passed.
- Protected floor `git diff --stat` (verdict_mapping/runner_e2e/writeback/fix_loop/
  marker_suppression) → empty.
- Touched-surface ruff check + format → clean.
