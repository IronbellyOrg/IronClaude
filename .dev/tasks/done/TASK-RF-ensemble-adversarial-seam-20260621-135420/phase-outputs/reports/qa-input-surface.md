# QA Input Surface — consolidated change surface (Step QG.1)

**Date:** 2026-06-22

## What the change does (one paragraph)

R6 widens the FR-RH2 Tier-2 adversarial seam in `src/superclaude/cli/reflect/ensemble.py` from a bare convergence float to an `AdversarialResult` dataclass carrying `{convergence_score, regression_present, unauthorized_deviation_present, needs_human_decision, deviation_count_by_class, report_path}`. The seam alias `AdversarialScoreFn` and the default scorer `run_adversarial_scorer` are widened in lockstep (only `convergence_score` + `report_path` are LIVE; the 3 booleans + counts default clean). `build_reflect_contract` gains keyword-only params and threads those fields in place of the previously hard-coded clean literals; `_select_report_path` prefers an adversarial report path when present. A red-then-green I12 integration test injects `AdversarialResult(regression_present=True)` and asserts `derive_verdict(...)` routes HALTED/exit-10/reason=regression (NOT PASS); a U11 unit companion checks the builder threading. `contract.py`/`models.py` are byte-unchanged (FR-RH2.7).

## FR-RH2.7 diff-proof verdict

PASS — `git diff -- contract.py models.py` is EMPTY (see `phase-outputs/test-results/fr-rh2.7-diff-proof.md`).

## Phase-3 result / proof files

- `phase-outputs/test-results/pytest-summary.md` — 2353 passed, 0 failed; I12 + U11 + U10 + I1 + U6 all PASSED
- `phase-outputs/test-results/fr-rh2.7-diff-proof.md` — empty frozen-file diff (PASS)
- `phase-outputs/test-results/nfr7-nesting-guard.md` — no-nesting guard PASS
- `phase-outputs/test-results/make-lint.md` — ruff clean on scope files; 1 pre-existing OUT-OF-SCOPE error on recommend.md
- `phase-outputs/test-results/ruff-format-check.md` — scope files formatted (PASS); repo-wide noise is version-mismatch
- `phase-outputs/test-results/pytest-full-output.txt` — raw suite output

## git diff --stat

```
 src/superclaude/cli/reflect/ensemble.py            | 163 ++++++++++++++++++---
 .../cli/reflect/test_ensemble_stub_integration.py  |  86 ++++++++++-
 tests/cli/reflect/test_ensemble_unit.py            |  43 ++++++
 3 files changed, 271 insertions(+), 21 deletions(-)
```

## Full git diff (ensemble.py + both test files)

```diff
diff --git a/src/superclaude/cli/reflect/ensemble.py b/src/superclaude/cli/reflect/ensemble.py
index 102b804f..8f8b45f9 100644
--- a/src/superclaude/cli/reflect/ensemble.py
+++ b/src/superclaude/cli/reflect/ensemble.py
@@ -68,8 +68,39 @@ ADVERSARIAL_SUBRUN_DIR = "t2-adversarial"
 CONTRACT_FILENAME = "return-contract.yaml"
 MZERO_CONTRACT_MISSING_SLUG = "contract-missing"
 
+
+@dataclasses.dataclass
+class AdversarialResult:
+    """Result object returned by the Tier-2 adversarial seam.
+
+    Widens the seam beyond a bare convergence float so real deviation/regression
+    signal can flow into ``build_reflect_contract``. Today only
+    ``convergence_score`` + ``report_path`` are LIVE (sourced from the score-only
+    ``/sc:adversarial`` Mode-A child); the three deviation booleans + per-class
+    counts default CLEAN until a producer-extension emits them (OQ-PRODUCER).
+
+    Load-bearing booleans (``regression_present``, ``unauthorized_deviation_present``,
+    ``needs_human_decision``) MUST be genuine Python ``bool`` — a non-bool routes
+    BLOCKED ``malformed-contract-boolean`` in ``contract.py``.
+    """
+
+    convergence_score: float | None
+    regression_present: bool = False
+    unauthorized_deviation_present: bool = False
+    needs_human_decision: bool = False
+    deviation_count_by_class: dict[str, int] = dataclasses.field(
+        default_factory=lambda: {
+            "authorized": 0,
+            "necessary": 0,
+            "drift": 0,
+            "regression": 0,
+        }
+    )
+    report_path: str | None = None
+
+
 TransportFactory = Callable[[int], Transport]
-AdversarialScoreFn = Callable[[list[str], Path], float | None]
+AdversarialScoreFn = Callable[[list[str], Path], AdversarialResult | None]
 
 # Vendor-distinct stub model pool so a credit-free ``--transport stub`` run is
 # genuinely PASS-eligible: each slot binds a DISTINCT model_id from a DISTINCT
@@ -218,24 +249,63 @@ def run_tier2_ensemble(
     swarm_contract_path = swarm_output_dir / CONTRACT_FILENAME
     emit_done_sentinel(swarm_contract.status, swarm_contract_path)
 
+    adversarial_result: AdversarialResult | None = None
     if adversarial_convergence_score is None and len(succeeded_final_paths) >= 2:
         if adversarial_score_fn is None:
-            adversarial_convergence_score = run_adversarial_scorer(
+            adversarial_result = run_adversarial_scorer(
                 succeeded_final_paths,
                 output_dir / ADVERSARIAL_SUBRUN_DIR,
                 config=config,
             )
         else:
-            adversarial_convergence_score = adversarial_score_fn(
+            adversarial_result = adversarial_score_fn(
                 succeeded_final_paths,
                 output_dir / ADVERSARIAL_SUBRUN_DIR,
             )
+        # A ``None`` result (child failure) leaves ``adversarial_convergence_score``
+        # at ``None`` so the null-convergence DEGRADE fallback is preserved; a
+        # pre-supplied score short-circuits the seam (this branch never runs).
+        if adversarial_result is not None:
+            adversarial_convergence_score = adversarial_result.convergence_score
+
+    # Destructure the seam result into contract-bound locals. Clean defaults apply
+    # when no seam ran (pre-supplied score / <2 survivors) OR the child failed
+    # (``adversarial_result is None``) — so a genuinely clean Tier-2 run still
+    # routes PASS (NFR-RH2.6 backward-compat).
+    regression_present = (
+        adversarial_result.regression_present
+        if adversarial_result is not None
+        else False
+    )
+    unauthorized_deviation_present = (
+        adversarial_result.unauthorized_deviation_present
+        if adversarial_result is not None
+        else False
+    )
+    needs_human_decision = (
+        adversarial_result.needs_human_decision
+        if adversarial_result is not None
+        else False
+    )
+    deviation_count_by_class = (
+        adversarial_result.deviation_count_by_class
+        if adversarial_result is not None
+        else None
+    )
+    adversarial_report_path = (
+        adversarial_result.report_path if adversarial_result is not None else None
+    )
 
     contract = build_reflect_contract(
         normalized_workers,
         swarm_merged_path=swarm_contract.merged_path,
         adversarial_convergence_score=adversarial_convergence_score,
         adversarial_unavailable=adversarial_unavailable,
+        regression_present=regression_present,
+        unauthorized_deviation_present=unauthorized_deviation_present,
+        needs_human_decision=needs_human_decision,
+        deviation_count_by_class=deviation_count_by_class,
+        adversarial_report_path=adversarial_report_path,
     )
     _emit_reflect_contract(config.contract_path, contract)
     return contract
@@ -246,13 +316,21 @@ def run_adversarial_scorer(
     output_dir: Path,
     *,
     config: ReflectConfig,
-) -> float | None:
-    """Launch the selected Mode-A scorer and parse its convergence score.
+) -> AdversarialResult | None:
+    """Launch the selected Mode-A scorer and wrap its output in an ``AdversarialResult``.
 
     The downstream merge step consumes swarm's per-reviewer ``final_path``
     artifacts (suspect-aware). No scoring, ranking, or dedup logic is added to
     ``swarm/merge.py``. The adversarial merge produces a convergence score
     recorded on the reflect contract.
+
+    Only ``convergence_score`` + ``report_path`` are populated LIVE here (the
+    score-only Mode-A child cannot supply reviewer-deviation signal); the three
+    deviation booleans + per-class counts default CLEAN on ``AdversarialResult``
+    (GAP-2 scope fork). A child-launch/parse failure still returns ``None`` so the
+    null-convergence DEGRADE fallback is preserved. ``regression_present`` is
+    NEVER auto-derived from a low/None convergence score (GAP-4 non-conflation:
+    low convergence is reviewer DISAGREEMENT → DEGRADE, not a regression).
     """
     output_dir.mkdir(parents=True, exist_ok=True)
     prompt = build_adversarial_prompt(final_paths, output_dir)
@@ -268,7 +346,11 @@ def run_adversarial_scorer(
     proc.start()
     if proc.wait() != 0:
         return None
-    return extract_convergence_score(parse_adversarial_contract(output_dir))
+    parsed = parse_adversarial_contract(output_dir)
+    return AdversarialResult(
+        convergence_score=extract_convergence_score(parsed),
+        report_path=_extract_adversarial_report_path(parsed),
+    )
 
 
 def parse_adversarial_contract(output_dir: Path) -> dict[str, Any] | None:
@@ -357,14 +439,45 @@ def extract_convergence_score(contract: dict[str, Any] | None) -> float | None:
     return None
 
 
+def _extract_adversarial_report_path(contract: dict[str, Any] | None) -> str | None:
+    """Extract the merged report path from the adversarial return contract.
+
+    Mirrors ``extract_convergence_score``'s ``return_contract:`` unwrap. The
+    Mode-A child emits ``merged_output_path`` (string|null, schema research 02
+    §3); surface it as the adversarial ``report_path`` so the contract can prefer
+    it over the swarm ``merged.md`` subrun fallback. Returns ``None`` when absent
+    or non-string.
+    """
+    if not contract:
+        return None
+    inner = contract.get("return_contract")
+    if isinstance(inner, dict):
+        contract = inner
+    value = contract.get("merged_output_path")
+    return value if isinstance(value, str) and value else None
+
+
 def build_reflect_contract(
     workers: list[WorkerResult],
     *,
     swarm_merged_path: str | None = None,
     adversarial_convergence_score: float | None = None,
     adversarial_unavailable: bool = False,
+    regression_present: bool = False,
+    unauthorized_deviation_present: bool = False,
+    needs_human_decision: bool = False,
+    deviation_count_by_class: dict[str, int] | None = None,
+    adversarial_report_path: str | None = None,
 ) -> dict[str, Any] | None:
-    """Map swarm worker facts onto the reflect return-contract namespace."""
+    """Map swarm worker facts onto the reflect return-contract namespace.
+
+    The deviation/regression signal (``regression_present``,
+    ``unauthorized_deviation_present``, ``needs_human_decision``,
+    ``deviation_count_by_class``) is threaded from the adversarial seam result;
+    all four default CLEAN so a direct call or a seam-less Tier-2 run still emits
+    an all-zero, regression-free contract that routes PASS. Load-bearing booleans
+    are forwarded as genuine Python ``bool`` (never ``"true"``/``1``).
+    """
     succeeded = [worker for worker in workers if worker.status == "success"]
     reviewer_count = len(succeeded)
     if reviewer_count == 0:
@@ -372,7 +485,18 @@ def build_reflect_contract(
 
     tier_reached = 2 if reviewer_count >= 2 else 1
     merge_method = "adversarial" if reviewer_count >= 2 else "single-reviewer-fallback"
-    report_path = _select_report_path(succeeded, swarm_merged_path)
+    report_path = _select_report_path(
+        succeeded,
+        swarm_merged_path,
+        adversarial_report_path=adversarial_report_path,
+    )
+    if deviation_count_by_class is None:
+        deviation_count_by_class = {
+            "authorized": 0,
+            "necessary": 0,
+            "drift": 0,
+            "regression": 0,
+        }
 
     return {
         "contract_version": REFLECT_CONTRACT_VERSION,
@@ -382,12 +506,7 @@ def build_reflect_contract(
         "reviewer_count": reviewer_count,
         "report_path": report_path,
         "audit_log_path": None,
-        "deviation_count_by_class": {
-            "authorized": 0,
-            "necessary": 0,
-            "drift": 0,
-            "regression": 0,
-        },
+        "deviation_count_by_class": deviation_count_by_class,
         "t2_model_class_diversity": compute_model_class_diversity(succeeded),
         "t2_vendor_diversity": compute_vendor_diversity(succeeded),
         "adversarial_unavailable": adversarial_unavailable,
@@ -398,10 +517,10 @@ def build_reflect_contract(
         "citations_dropped": 0,
         "citations_dropped_extrapolated": 0,
         "input_drift_detected": False,
-        "regression_present": False,
-        "unauthorized_deviation_present": False,
-        "needs_human_decision": False,
-        "user_decision_required": False,
+        "regression_present": regression_present,
+        "unauthorized_deviation_present": unauthorized_deviation_present,
+        "needs_human_decision": needs_human_decision,
+        "user_decision_required": needs_human_decision,
         "serena_summary_corroboration": "unavailable",
         "degraded_components": [],
     }
@@ -488,7 +607,15 @@ def _slugify_model(value: str, index: int) -> str:
 def _select_report_path(
     succeeded: list[WorkerResult],
     swarm_merged_path: str | None,
+    *,
+    adversarial_report_path: str | None = None,
 ) -> str | None:
+    # Prefer the adversarial merged report when present (QA CRITICAL #2: keep the
+    # swarm ``merged.md`` only as a subrun-artifact fallback). When no adversarial
+    # report path is available the existing chain (swarm → worker final_path →
+    # None) is preserved unchanged, so current swarm-path assertions stay green.
+    if adversarial_report_path:
+        return adversarial_report_path
     if swarm_merged_path:
         return swarm_merged_path
     for worker in succeeded:
diff --git a/tests/cli/reflect/test_ensemble_stub_integration.py b/tests/cli/reflect/test_ensemble_stub_integration.py
index bd20a83f..f72b360c 100644
--- a/tests/cli/reflect/test_ensemble_stub_integration.py
+++ b/tests/cli/reflect/test_ensemble_stub_integration.py
@@ -26,7 +26,11 @@ from unittest.mock import patch
 from superclaude.cli.reflect import ensemble as ensemble_mod
 from superclaude.cli.reflect.config import resolve_config
 from superclaude.cli.reflect.contract import derive_verdict, parse_contract
-from superclaude.cli.reflect.ensemble import run_tier2_ensemble, stub_model_id
+from superclaude.cli.reflect.ensemble import (
+    AdversarialResult,
+    run_tier2_ensemble,
+    stub_model_id,
+)
 from superclaude.cli.reflect.models import Verdict
 from superclaude.cli.swarm.models import WorkerResult
 from superclaude.cli.swarm.transports.stub import StubTransport
@@ -36,8 +40,24 @@ from superclaude.cli.swarm.transports.stub import StubTransport
 _FIXED_SCORE = 0.86
 
 
-def _const_score(_paths: list[str], _out: Path) -> float:
-    return _FIXED_SCORE
+def _const_score(_paths: list[str], _out: Path) -> AdversarialResult:
+    # Clean-default result object (the widened seam shape): a non-None convergence
+    # score with no deviation/regression signal, so the existing PASS/DEGRADED
+    # tests that inject this stub keep their current verdicts. Booleans are genuine
+    # Python ``False``. Covers all three injection sites transitively.
+    return AdversarialResult(
+        convergence_score=_FIXED_SCORE,
+        regression_present=False,
+        unauthorized_deviation_present=False,
+        needs_human_decision=False,
+        deviation_count_by_class={
+            "authorized": 0,
+            "necessary": 0,
+            "drift": 0,
+            "regression": 0,
+        },
+        report_path=None,
+    )
 
 
 class _FailingTransport:
@@ -449,3 +469,63 @@ def test_i11b_tier1_audit_once_does_not_call_ensemble(temp_tasklist, patch_git)
         ReflectRunner(tier1_config)._audit_once()
     spy_ensemble.assert_not_called()
     spy_proc.assert_called_once()
+
+
+def test_i12_seam_regression_does_not_pass(temp_tasklist, patch_git) -> None:
+    """I12 (FR-RH2 R6): a seam-reported regression MUST NOT route PASS.
+
+    Red-then-green acceptance: against the pre-R6 code (``build_reflect_contract``
+    hard-coded ``regression_present: False``) this asserted ``Verdict.PASS`` and
+    FAILED; after the seam widening the regression signal threads through to the
+    contract and ``derive_verdict`` routes HALTED (exit 10, reason
+    ``"regression"``) via ``_halted_reason``.
+
+    The ensemble is kept HEALTHY (distinct vendor-survivors → ``full`` diversity)
+    and ``convergence_score`` is NON-None (0.86) so the ``null-convergence``
+    DEGRADE trigger does NOT fire and mask the HALT (GAP-4 non-conflation).
+    """
+
+    def _regression_score(_paths: list[str], _out: Path) -> AdversarialResult:
+        # Genuine Python ``True``/``1`` (never "true") so the strict-identity
+        # ``is True`` halt trigger fires instead of self-BLOCKing on a non-bool.
+        return AdversarialResult(
+            convergence_score=_FIXED_SCORE,
+            regression_present=True,
+            unauthorized_deviation_present=False,
+            needs_human_decision=False,
+            deviation_count_by_class={
+                "authorized": 0,
+                "necessary": 0,
+                "drift": 0,
+                "regression": 1,
+            },
+            report_path=None,
+        )
+
+    config = _config(temp_tasklist, reviewers=3)
+    run_tier2_ensemble(
+        config,
+        transport_for_slot=_distinct_stub,
+        adversarial_score_fn=_regression_score,
+    )
+    contract = parse_contract(config.contract_path)
+    result = derive_verdict(
+        contract,
+        expected_tier=2,
+        allow_single_vendor=config.allow_single_vendor,
+        child_rc=0,
+    )
+
+    # HEADLINE acceptance: a reported regression does not route PASS.
+    assert result.verdict is not Verdict.PASS
+    # Sharpened: it routes the HALTED regression rung specifically.
+    assert result.verdict is Verdict.HALTED
+    assert result.verdict.exit_code == 10
+    assert result.reason == "regression"
+    # Provenance: the seam signal actually reached the contract (was hard-coded
+    # ``False`` before R6).
+    assert contract is not None
+    assert contract["regression_present"] is True
+    # Healthy-ensemble guard: a DEGRADE is not masking the HALT.
+    assert contract["t2_model_class_diversity"] == "full"
+    assert result.verdict is not Verdict.DEGRADED
diff --git a/tests/cli/reflect/test_ensemble_unit.py b/tests/cli/reflect/test_ensemble_unit.py
index 70950a95..9b2e3ab2 100644
--- a/tests/cli/reflect/test_ensemble_unit.py
+++ b/tests/cli/reflect/test_ensemble_unit.py
@@ -289,3 +289,46 @@ def test_u10_adversarial_contract_parse_real_shape(tmp_path) -> None:
     # Wrong-path / missing contract → None (graceful null-convergence fallback).
     assert parse_adversarial_contract(tmp_path / "nope") is None
     assert extract_convergence_score(None) is None
+
+
+def test_u11_build_reflect_contract_threads_regression_fields() -> None:
+    """U11 (R6): the widened builder threads the deviation/regression kwargs.
+
+    Isolates the contract-builder change from the full fan-out path: a direct call
+    with the new kwargs surfaces the regression signal, while a call WITHOUT them
+    keeps the clean defaults (so the clean Tier-2 path still PASSes).
+    """
+    workers = [
+        WorkerResult(index=0, status="success", model_id="model-a"),
+        WorkerResult(index=1, status="success", model_id="model-b"),
+    ]
+
+    # With the deviation kwargs: the signal threads through as genuine bool/int.
+    flagged = build_reflect_contract(
+        workers,
+        adversarial_convergence_score=0.86,
+        regression_present=True,
+        deviation_count_by_class={
+            "authorized": 0,
+            "necessary": 0,
+            "drift": 0,
+            "regression": 1,
+        },
+    )
+    assert flagged is not None
+    assert flagged["regression_present"] is True
+    assert flagged["deviation_count_by_class"]["regression"] == 1
+
+    # Clean default (no deviation kwargs): regression-free, all-zero counts.
+    clean = build_reflect_contract(workers, adversarial_convergence_score=0.86)
+    assert clean is not None
+    assert clean["regression_present"] is False
+    assert clean["unauthorized_deviation_present"] is False
+    assert clean["needs_human_decision"] is False
+    assert clean["user_decision_required"] is False
+    assert clean["deviation_count_by_class"] == {
+        "authorized": 0,
+        "necessary": 0,
+        "drift": 0,
+        "regression": 0,
+    }
```
