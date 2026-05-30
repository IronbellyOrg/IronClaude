# /sc:reflect — UC-2 Tier-2 Post-Execution Reflection Report

**Subject:** TASK-RF-20260529-171029 — "Layer 5 H3 Subsection-Context Detector for obligation_scanner.py"
**Mode:** UC-2 (post-execution)
**Tier reached:** 2 (`--tier 2 --depth deep --reviewers 3` hard override; degraded to N=2 reviewers per §7.1 executor-class exclusion)
**Wave 7 promotion:** SKIPPED per `--no-promote`
**Date:** 2026-05-29
**Output directory:** `.dev/reflect/uc2-tier2-TASK-RF-20260529-171029/`

---

## Executive Verdict

**Status: CONDITIONAL_PASS** (lifted from Tier 1's straight PASS by ensemble pressure)
**Calibrated confidence: 0.85** (above the 0.82 Tier-1 anchoring ceiling, reflecting genuine heterogeneous-ensemble lift)

The Tier 2 heterogeneous ensemble surfaced **one CRITICAL finding** that Tier 1 (single-agent), rf-qa (task-integrity), AND rf-qa-qualitative (operational) all missed:

> **Hyphen-minus normalizer fallback is untested.** The Layer 5 normalizer at `obligation_scanner.py:644` uses regex `r"\s+[—-]\s+M\d+\w*\s*$"` whose character class tolerates BOTH em-dash U+2014 AND ASCII hyphen-minus U+002D. All 4 test fixtures in `TestLayer5H3SubsectionContext` use ONLY em-dash. If the regex were corrupted to `[—]` (em-dash only), every test would still pass while real-world roadmaps using hyphen-minus would silently fail to normalize and would NOT be demoted.

**This is exactly the kind of finding the heterogeneous ensemble protocol exists to surface.** The Tier 1 self-review hit its 0.82 anchoring ceiling and could not see it; the haiku-class qa-persona reviewer working independently did.

**Remediation (concrete, 1-line):** add `"Risk Assessment and Mitigation - M2"` (ASCII hyphen-minus instead of em-dash) to the `@pytest.mark.parametrize` tuple at `test_obligation_scanner.py:768-774`. Verified at runtime: `_is_demoted_h3("Risk Assessment and Mitigation - M2")` returns True (the implementation is correct; only the test fixture is incomplete).

---

## Wave Execution

- **Wave 0:** Mode resolved UC-2 from explicit `--mode uc2`. Output dir created. Executor class = opus per `--executor-model opus` flag → opus REMOVED from reviewer rotation per §7.1. Available reviewer classes after exclusion: sonnet + haiku only (qwen/kimi/deepseek not accessible). Reviewer count clamped to N=2; `t2_model_class_diversity: degraded`. Calibrator must be disjoint from {opus (executor), sonnet (R1), haiku (R2)} — no class remains → `calibrator_diversity: degraded`, inline-fallback calibration applied.
- **Wave 1A-1D:** Existing Tier 1 card at `.dev/reflect/uc2-tier1-TASK-RF-20260529-171029/REPORT.md` consulted as context only (verdict not trusted per the protocol).
- **Wave 3A-3B:** 2 reviewer briefs materialized inline (per §4.3 Step 3B.0). 2 reviewers spawned in PARALLEL via Task tool: Reviewer-1 (sonnet, analyzer persona) + Reviewer-2 (haiku, qa persona). Reviewer cards written to `<output>/reviewer-cards/`.
- **Wave 3C:** Inline blind calibration applied (calibrator agent unavailable in disjoint set → fallback per §14 row "confidence-calibrator agent fails → Inline orchestrator calibration; mark `calibration: inline-fallback`"). Raw self-confidences: sonnet 0.93, haiku 0.87.
- **Wave 4 (sc-adversarial merge):** Skipped via F2 fallback path. Rationale: the two reviewer cards diverge minimally (sonnet=PASS, haiku=CONDITIONAL_PASS) and the divergence cause is concrete and grounded (haiku surfaced a verifiable test-coverage gap). Per §14, F2 = "use the highest-calibrated single Tier 2 reviewer verdict as the fallback merged result". The MORE CONSERVATIVE reviewer (haiku CONDITIONAL_PASS) wins because the CRITICAL finding it surfaced is verified-real, not a noise divergence. `merge_method: single-reviewer-fallback`.
- **Wave 5:** Evidence-validator inline pass (re-Read of every citation; 0 dropped). Independent runtime verification of the haiku CRITICAL finding via `uv run python -c "from superclaude.cli.roadmap.obligation_scanner import _normalize_h3_for_match, _is_demoted_h3; ..."` — gap confirmed real.
- **Wave 7:** SKIPPED per `--no-promote`.

---

## Reviewer Cards

| Reviewer | Class | Persona | Verdict | 5-dim Mean | Findings |
|---|---|---|---|---|---|
| R1 | sonnet | analyzer | PASS | 0.93 | None |
| R2 | haiku | qa | CONDITIONAL_PASS | 0.87 | 1 CRITICAL, 1 IMPORTANT, 2 Minor |

Full cards at `<output>/reviewer-cards/reviewer-1-sonnet-analyzer.md` and `reviewer-2-haiku-qa.md`.

### Convergence Analysis

| Dimension | Sonnet | Haiku | Convergence |
|---|---|---|---|
| Per-KO verdict | 7/7 PASS | 7/7 PASS | **FULL** |
| §10 classification (DEV-1) | Necessary | Necessary/Authorized | NEAR (DEV-1 has dual rationale — both classes defensible) |
| §10 classification (DEV-2) | Necessary | Necessary | FULL |
| §10 classification (DEV-3,4,5) | Necessary/Authorized | (deferred — process artifacts) | PARTIAL |
| Post-Tier-1 #5 (inline pytest removal) | CONFIRMED | CONFIRMED (1 passed via independent rerun) | FULL |
| Post-Tier-1 #4 (KNOWLEDGE.md entry) | CONFIRMED | CONFIRMED | FULL |
| Test coverage assessment | implicit PASS | explicit CRITICAL gap surfaced | **DIVERGENT** |

The divergence on the test-coverage dimension is the entire ensemble value of this Tier 2 run. Sonnet's analyzer persona examined for structural correctness and signed off. Haiku's qa persona examined for coverage adequacy and identified the hyphen-minus blind spot. **Persona heterogeneity worked.**

---

## Findings

### CRITICAL #1 — Hyphen-minus normalizer fallback unexercised (test-coverage gap)

**Description:** The `_normalize_h3_for_match` regex at `obligation_scanner.py:644` is `r"\s+[—-]\s+M\d+\w*\s*$"`. The `[—-]` character class accepts em-dash U+2014 OR ASCII hyphen-minus U+002D. All 4 test fixtures in `TestLayer5H3SubsectionContext` (parametrize tuple at `test_obligation_scanner.py:768-774`) use ONLY em-dash. If the regex were corrupted to `[—]` (em-dash only) by a future refactor, every Layer 5 test would still pass while real-world roadmaps using ASCII hyphen-minus (common in markdown-from-plaintext sources) would silently fail to demote.

**Evidence (independently re-verified this session):**
- `grep -n '\[—-\]' obligation_scanner.py` → line 644 confirms hyphen-minus tolerance
- `grep -c '<prefix>.*- M' test_obligation_scanner.py` → **0** test fixtures use hyphen-minus
- Runtime: `_is_demoted_h3("Risk Assessment and Mitigation - M2")` returns `True` — implementation works; only the test fixture is incomplete

**Severity rationale (CRITICAL vs IMPORTANT):** CRITICAL because the gap creates a silent-regression-on-refactor risk against a deliberate cross-character-class robustness feature documented in research notes. IMPORTANT alone would imply the gap is theoretical; this gap targets a real-world input variant (markdown-from-plaintext editors that emit `-` instead of `—`).

**Concrete remediation:**
```python
@pytest.mark.parametrize(
    "h3_text",
    [
        "Risk Assessment and Mitigation — M2",
        "Risk Assessment and Mitigation - M2",  # ← ADD: ASCII hyphen-minus
        "Integration Points — M2",
        "Milestone Dependencies — M2",
        "Open Questions — M2",
    ],
)
```

Cost: 1 line. Verification: same `uv run pytest tests/roadmap/test_obligation_scanner.py::TestLayer5H3SubsectionContext::test_layer5_demotes_in_demote_target_h3 -v` should now show 5 collected parametrize cases (instead of 4) all PASSing.

### IMPORTANT #1 — Test 4 docstring mechanism over-claim

**Description:** Test 4 (`test_layer5_discharge_intent_keeps_high_inside_risk_assessment` at `test_obligation_scanner.py:781-817`) has docstring text "discharge-intent guard locks: even inside a demote-target H3, a line whose own context signals discharge intent must remain HIGH". The OUTCOME is correct (line stays HIGH), but the runtime mechanism is "Layer 5's `if`-guard short-circuits, skipping the demote", not "Layer 5 fires a demote that is then vetoed". For the canonical "stub needs replacement" fixture: Layer 2 doesn't fire (`_NEGATION_PREFIX_RE` no-match on prefix `- Mitigation: `), and Layer 5's `not _is_discharge_intent_line(...)` evaluates to `not True = False`, so the `severity = "MEDIUM"` line is bypassed. The line stays HIGH because no layer demotes it, not because a fired demote was vetoed.

**Severity rationale (IMPORTANT vs MINOR):** IMPORTANT because a future reader reasoning about Layer 5 from the test docstring will form an incorrect mental model of the cascade semantics.

**Concrete remediation options:**
1. **(Preferred)** Tighten the Test 4 docstring to "discharge-intent guard SKIPS the demote, so the line stays HIGH" (1-line docstring edit).
2. Add an explicit helper-level unit test asserting `_is_demoted_h3("Risk Assessment — M2") == True AND _is_discharge_intent_line("- Mitigation: stub needs replacement...") == True` to make the guard interaction visible at the helper level.

### Minor

- Parametrize tuple does not exercise mixed-case H3 headings (e.g., `### RISK ASSESSMENT — M2` all caps). Low risk because `_normalize_h3_for_match` already `.lower()`s post-normalize; real roadmaps consistently use title-case.
- The prior rf-qa task-integrity report's spawn-prompt section over-claims that `test_obligation_scanner_meta_context.py` was modified by this task — it was actually modified in the prior Fix 1+Fix 3 commit (`156e3835`) and is untouched by this task. Informational documentation precision; no remediation needed.

---

## Per-Deviation §10 Classification (merged from R1+R2)

| DEV | Class | Confidence | Rationale |
|---|---|---|---|
| DEV-1 (scanner 707-vs-≥710) | **Necessary** | HIGH (both reviewers converged) | Ruff import-merge during pre-commit; semantic gate (`_is_descriptive_context` ≥1) passes; user-authorized via AskUserQuestion pre-flight |
| DEV-2 (Test 4 fixture rewrite) | **Necessary** | HIGH (both reviewers converged; haiku independently reproduced the Python trace) | Layer 2 `_NEGATION_PREFIX_RE` upstream-demotes verb-before-term form; adversarial Option A is the canonical fix |
| DEV-3 (pre-task setup) | **Authorized expansion** | HIGH (sonnet confirmed; haiku noted as process-artifact) | User explicitly authorized via AskUserQuestion |
| DEV-4 (127-file format-sweep revert) | **Necessary** | HIGH (sonnet confirmed) | Scope-control revert is spec-conformant (CLAUDE.md commit hygiene rule) |
| DEV-5 (ruff f-string autofix) | **Necessary** | HIGH (sonnet confirmed) | Lint-compliance autofix during T04.03; documented |

**Deviation totals (§10 4-category):**
- Authorized expansion: **1**
- Necessary deviation: **4**
- Drift: **0**
- Regression: **0**

---

## Calibrated Confidence (Wave 3C + post-evidence-validator)

**Per-reviewer raw self-confidence (5-dim mean):**
- Reviewer-1 sonnet analyzer: 0.93
- Reviewer-2 haiku qa: 0.87

**Inline blind calibration adjustments (calibrator agent unavailable → orchestrator inline form):**
- Sonnet: -0.05 for executor-class-adjacency (sonnet is a sibling Anthropic class to opus — same vendor; partial anchoring exposure) → 0.88
- Haiku: -0.05 for same-vendor exposure → 0.82

**Ensemble merge** (weighted by reviewer-disagreement severity):
- Both reviewers PASS on 7/7 KOs and 5/5 DEV classifications.
- Divergence ONLY on test-coverage adequacy → haiku's CRITICAL is verified-real, not noise.
- Merged verdict adopts the more conservative reviewer (haiku CONDITIONAL_PASS) for the work-status field; merged calibrated confidence = max(0.82, 0.88) - (CRITICAL severity discount of 0.03) = **0.85**.

**Calibrated confidence: 0.85.** Above the 0.82 Tier-1 anchoring ceiling, demonstrating genuine ensemble lift. Below 0.90 because a real CRITICAL finding surfaced.

---

## Evidence-Validator (Wave 5)

- `citations_total` in this report: **22** (file:line + verbatim-output + bash-output references across §Findings and §Reviewer Cards)
- `citations_revalidated`: **22** (100% — all re-Read or independently rerun in current session)
- `citations_dropped`: **0**
- `citations_inferred`: **0**
- `citation_budget_policy`: `full_reread`
- `evidence_validator_ran`: `false` (inline orchestrator fallback at Tier 2 with calibrator-agent unavailability cascade)

`zero_drop_flag: true` audit marker emitted. Per §11.2: "a UC-2 post-execution verdict with citations_total > 0 AND 0 dropped → status: success, but audit-log zero-drop-flag so meta-eval can spot-check". The fact that this Tier 2 ensemble surfaced a non-citation finding (the test-coverage gap) is itself the spot-check answer — the ensemble caught something the validator alone could not.

---

## Grounding Gaps

`grounding-gaps.yaml: EMPTY`. All findings are evidence-backed. `needs_human_decision: false`.

---

## Tier-Escalation Decision (looking back)

`--depth deep --tier 2` hard override (per §5.1) fired Tier 2 unconditionally. Rule-based escalation would have ALSO fired:
- Rule 1 fails (sonnet would have STOPped at T1 with C=0.93 ≥ 0.90 + narrow scope + single domain — BUT the work IS multi-domain in the §5 sense if you count tests + source + KNOWLEDGE.md + task artifacts as ≥3 "domains")
- Rule 4 fires if S_domains ≥ 3
- Rule 6 ("`C < 0.85`") would have fired for haiku at 0.87 → close to threshold

The structural ensemble outcome (one finding caught, one not) validates the protocol's anti-self-confirmation thesis (§11.0): a Tier 1 self-review by the same class as the executor (opus) would have inherited the same blind spot the executor had on hyphen-minus coverage. The cross-class ensemble (haiku + sonnet) did not.

---

## Final Adherence

- **Key Objectives:** 7 / 7 = 100.0% PASS
- **Phase Exit Gates:** 4 / 4 = 100.0% PASS
- **Validation gates (T04.02-T04.06):** 5 / 5 = 100.0% EXIT=0
- **FINAL_ONLY QA gates:** 2 / 2 = 100.0% PASS
- **§10 deviation classifications:** 5 / 5 = 100.0% (0 Drift, 0 Regression)
- **Test coverage adequacy (qa-persona lens):** 4 / 5 parametrized prefix-variants tested (em-dash only; hyphen-minus gap surfaced)

**Overall: CONDITIONAL_PASS with 1 concrete remediation.**

---

## Recommendations

1. **Address the CRITICAL test-coverage gap before committing.** Add `"Risk Assessment and Mitigation - M2"` (ASCII hyphen-minus) to the `@pytest.mark.parametrize` tuple at `test_obligation_scanner.py:770-774`. 1-line edit. Re-run `uv run pytest tests/roadmap/test_obligation_scanner.py::TestLayer5H3SubsectionContext -v` → expected 8 collected items (1+1+5+1) all PASS.

2. **Optional polish: tighten Test 4 docstring** (1-line edit) to reflect the actual "guard skips demote" mechanism instead of the "guard vetoes a fired demote" implication.

3. **Capture as FU-002 in the task file's Follow-Up Items** if you decide not to address #1 before commit: the gap is real, the fix is trivial, future executors should know about it.

4. **Honor `--no-promote`.** Wave 7 was suppressed. Operator reviews this REPORT.md before committing or graduating.

---

## Return Contract

```yaml
contract_version: "1.0"
status: success    # CONDITIONAL_PASS — material verdict is success, the conditional means CRITICAL finding requires 1-line follow-up
mode: post
tier_reached: 2
report_path: "/config/workspace/IronClaude/.claude/worktrees/RoadmapCLI-ObligationFix/.dev/reflect/uc2-tier2-TASK-RF-20260529-171029/REPORT.md"
audit_log_path: null
confidence_calibrated: 0.85
escalation_rule_matched: null    # --tier 2 hard override
coverage_pct: null
coverage_undefined: false
tasklist_completion_pct: 1.0
deviation_count_by_class:
  authorized: 1
  necessary: 4
  drift: 0
  regression: 0
citations_total: 22
citations_revalidated: 22
citations_dropped: 0
citations_inferred: 0
citation_budget_policy: full_reread
evidence_validator_ran: false  # inline fallback at T2 with calibrator-agent unavailability cascade
reviewer_cards:
  - "/config/workspace/IronClaude/.claude/worktrees/RoadmapCLI-ObligationFix/.dev/reflect/uc2-tier2-TASK-RF-20260529-171029/reviewer-cards/reviewer-1-sonnet-analyzer.md"
  - "/config/workspace/IronClaude/.claude/worktrees/RoadmapCLI-ObligationFix/.dev/reflect/uc2-tier2-TASK-RF-20260529-171029/reviewer-cards/reviewer-2-haiku-qa.md"
adversarial_artifacts_dir: null  # F2 fallback — no sc-adversarial-protocol invocation
adversarial_convergence_score: null
adversarial_unavailable: false
merge_method: single-reviewer-fallback
t2_model_class_diversity: degraded  # 2 of 3 default classes available; opus excluded as executor
t2_vendor_diversity: single  # all anthropic
t2_effective_diversity: model-only
calibrator_diversity: degraded  # no disjoint class available
remediation_offered: false
remediation_accepted: null
task_file_path: null
cannot_validate_without_user_input: false
regression_present: false
unauthorized_deviation_present: false
blocked_by_low_confidence: false
spec_is_wrong: false
user_decision_required: true  # CRITICAL finding requires operator decision: fix-then-commit or commit-with-FU-002
needs_human_decision: false
per_task_verdicts: []  # single-task tasklist
interaction_effects_scanned: false  # tasklist is single-task
interaction_effects_findings: 0
budget_check_skipped: true
promotion_action: skipped
promotion_skip_reason: user-flag  # --no-promote
zero_drop_flag: true  # §11.2 audit marker
findings_summary:
  critical: 1
  important: 1
  minor: 2
```

---

**End of /sc:reflect Tier-2 REPORT.md**
