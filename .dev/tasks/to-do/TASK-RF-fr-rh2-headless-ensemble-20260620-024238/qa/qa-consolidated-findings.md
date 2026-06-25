# FINAL QA Gate — Consolidated Findings (cycle 1)

Date: 2026-06-20
6-agent lens verdicts: **3 PASS** (no-nesting/isolation, backward-compat-floor,
M-N-divergence-verdict-correctness) + **3 FAIL** (spec-acceptance-traceability,
ensemble-formation-correctness, OI-1-mapping-fidelity).

Consolidated verdict: **FAIL** (any agent reported issues → FAIL). Each finding
below is triaged against the acceptance oracle (spec), the validated OI-1 table
(Phase 0.1b), and the resolved Phase-0 decisions. Duplicates merged.

## ACCEPTED — fixes to apply (serialized, one writer)

### A. [CRITICAL] reflect-review lens brief not wired into the worker prompt
- Lenses: spec-traceability #2, ensemble-formation #1.
- Evidence: `ensemble.py` passed `prompt=self._build_prompt()` (the `/sc:reflect`
  slash command) verbatim to `dispatch_wave1`, so proxy workers receive a
  Claude-Code slash command, not the `reflect-review` lens brief. FR-RH2.2 / spec
  §2.2 require `ensemble.py` to build per-reviewer briefs from the lens.
- Fix: `run_tier2_ensemble` builds the worker prompt from
  `REFLECT_REVIEW_LENS.system_prompt_fragment` + `user_template` with the review
  target content (the tasklist under audit + base ref header), mirroring swarm
  `commands._assemble_prompt`. The stub tests are content-agnostic; this fixes the
  live openai_compat path.

### B. [IMPORTANT] t2_vendor_diversity not vendor-classified
- Lenses: OI-1 #3, spec-traceability (FR-RH2.4 partial).
- Evidence: `compute_vendor_diversity` returned "multi" for any ≥2 distinct
  `model_id`s; two distinct SAME-vendor models would wrongly read "multi" and
  suppress the FR-11 single-vendor degrade. The validated OI-1 table marks
  `t2_vendor_diversity` DERIVED "from vendor/classification of each succeeded
  worker model_id."
- Fix: restore `_vendor_from_model_id` vendor classification; "single" when all
  succeeded reviewers share a vendor, "multi" when ≥2 vendors, `None` when <2
  succeeded (single-reviewer-fallback owns the slug). Update the stub integration
  PASS-case model_ids to span ≥2 vendors (realistic — real T2 pools are
  multi-vendor) so model-class AND vendor diversity are genuinely satisfied.

### C. [IMPORTANT] production `_audit_once` → ensemble route is untested
- Lenses: spec-traceability #5, ensemble-formation (production stub).
- Evidence: the integration tests call `run_tier2_ensemble` directly; no test
  proves the production `_audit_once` (with the real `ClaudeProcess` identity
  seam) actually routes Tier-2 to the ensemble and not a single ClaudeProcess.
- Fix: add a test that, with the real `ClaudeProcess`, spies `run_tier2_ensemble`
  and asserts it is called for `expected_tier == 2` while no audit `ClaudeProcess`
  is constructed; and that Tier-1 (`depth=quick`) does NOT call the ensemble.

### D. [MINOR] DoD matrix NFR-RH2.6 wording imprecise
- Lens: spec-traceability #12.
- Evidence: the matrix said "git diff of existing test files empty," but
  `test_no_nesting_guard.py` was intentionally EXTENDED per Step 7.1 (FR-RH2.8).
- Fix: correct the DoD/Phase-8 wording to scope NFR-RH2.6 to the B1/B2/B3 +
  fix_loop + marker_suppression floor (unchanged), with `test_no_nesting_guard.py`
  intentionally extended.

## REJECTED — with rationale (not defects against THIS task's oracle/scope)

- **R1. "Tier-2 skips the Tier-1 ClaudeProcess pass" (spec #1, CRITICAL claimed).**
  Misreads FR-RH2.1: "the Tier-1 grounded pass via ClaudeProcess is unchanged"
  means the `depth=quick` Tier-1 path is byte-unchanged — NOT that a Tier-2 run
  must ALSO run a Tier-1 ClaudeProcess first. Tier-2 never did. The no-nesting,
  backward-compat, and M-N lenses all PASS consistent with this.
- **R2. M==0 slug must be `ensemble-empty` (spec #8).** Resolved by the Q6
  decision (Option B → `contract-missing`) to preserve FR-RH2.7's "derive_verdict
  unchanged"; the spec mn_guard_table's `ensemble-empty` is [CODE-VERIFIED] absent
  from contract.py. The M-N-divergence lens (which read Q6) PASSED on this exact
  point.
- **R3. adversarial_unavailable not set True on scorer failure (OI-1 #4).**
  Governed by the adversarial-seam decision: "fallback = option (c) null-
  convergence DEGRADE on adversarial-child failure" — i.e. failure → score=None →
  null-convergence (NOT adversarial-unavailable). Current behavior matches the
  resolved decision. Both route degraded/exit 11.
- **R4. status="success" / merge_method="adversarial" / tier_reached=2 are not
  failure-derived (OI-1 #1,#2,#5).** The M-N-divergence lens PASSED, proving every
  (M,N) row resolves to the spec-correct verdict/exit/slug. `tier_reached=2` for
  M≥2 is REQUIRED for the spec mn_guard_table to emit `degraded-model-diversity`
  (not `degraded-tier1`) on the duplicate case; setting it to 1 would produce the
  WRONG spec slug. `status="success"` and `merge_method="adversarial"` never
  produce a wrong verdict (the (M,N) degrades own the routing). These are the
  canonical pass.yaml field values.
- **R5. report_path uses swarm merged_path (OI-1 #6, spec #3).** The validated
  OI-1 table EXPLICITLY allows "a derived path from swarm reduce artifacts such as
  ResultContract.merged_path / succeeded WorkerResult.final_path." Table-faithful.
- **R6. deviation_count_by_class hard-coded zero (spec #3).** SYNTHESIZED per the
  validated table ("zero-equivalent inert default ... No swarm equivalent").
- **R7. verification_ran=True (OI-1 #7).** Verdict-inert (True is not False → the
  verification-skipped trigger does not fire either way); matches the canonical
  pass.yaml shape. Logged as a low nit, not changed.
- **R8. extra top-level fields beyond the 20-row table (OI-1 #8).** Intentional:
  the contract mirrors the 21-key canonical `pass.yaml` shape (I7 requires the same
  downstream-consumed field set); contract.py tolerates them (NFR-8). The 20-row
  table enumerates the verdict-DRIVER fields, not the full contract.
- **R9. NFR-RH2.2 raw subprocess in config.py/commands.py (spec #9).** Pre-existing
  reflect-package git/tmux subprocess use, explicitly out of the guard's scope by
  design (the existing `test_apply_remediation` docstring documents this); NOT
  added by FR-RH2.
- **R10. NFR-RH2.4 production stub still launches the adversarial ClaudeProcess
  (spec #6).** `--transport stub` is the WORKER-fan-out credit-free lane (no proxy
  credits). The adversarial scorer is a separate Claude child (local binary, not
  proxy credits); CI injects the score via the production `adversarial_score_fn`
  seam. Noted as a rollout follow-up (optional stub for the scorer), not a blocker.
- **R11. NFR-RH2.7 detached/tmux/--tui pollability (spec #10).** Task Step 6.9
  scopes NFR-RH2.7 to the `done.json` DM-017 sentinel (proven by I9). Full tmux/TUI
  observability is broader swarm functionality out of this task's scope.
- **R12. NFR-RH2.8 proxy URL contract not enforced at the transport boundary
  (spec #11).** Task Step 7.3/U9 scopes NFR-RH2.8 to "no forbidden literal in
  ensemble.py executable code" (proven). Transport-boundary URL enforcement is the
  pre-existing openai_compat transport's job.
- **R13. lens user_template not asserted in tests / _const_score ignores paths
  (ensemble-formation #3,#4).** Addressed by fix A (the lens now drives the prompt)
  + a new assertion. The `final_path`-not-merged.md contract is already enforced in
  code (`succeeded_final_paths` from normalized workers); a stronger assertion is a
  follow-up.

## Follow-Ups (deferred, logged — not blockers)
- Live-proxy + `claude -p` regression smoke (spec §8.3) — manual rollout.
- Optional credit-free stub for the adversarial scorer under `--transport stub`.
- Full diff materialization as the per-reviewer target (currently tasklist+base).
- Q7 private-symbol coupling contract test.
- Repo-wide pre-existing ruff/format sweep (102 files, none this task's).
