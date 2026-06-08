---
artifact: REPORT
skill: sc-reflect
mode: post (UC-2)
tier_reached: 2
status: partial
target: "Phase 8 / R1.3 — GateCriteria.code_assertions + first CodeAssertion"
task: TASK-RF-20260531-042405
parent_commit: 90a8fa67
created_date: 2026-06-02
reviewers: [sonnet, haiku]
calibrator: opus (inline, disjoint from reviewer classes)
merge_judge: opus (distinct class from both debaters)
---

# sc:reflect UC-2 Post-Execution Audit — R1.3

## Verdict: PARTIAL — ship-blocking finding surfaced (needs human decision)

The R1.3 **substrate** (the `GateCriteria.code_assertions` slot, the `CodeAssertion`
dataclass, the first `assert_step_reachable` predicate, the `test_dispatch_reachability.py`
CI enforcement, and the `models.py` changes) is **sound and its stated Contract #2
deliverable is genuinely CI-enforced**. PRESERVE invariants (`commands.py`,
`structural_checkers.py`, `convergence.py`) are byte-unchanged. 184/184 targeted
regression + ruff clean were independently reconfirmed by PG8.1.

**However**, the heterogeneous ensemble surfaced one HIGH finding that PG8.1's inline
rf-qa missed — a genuine anti-bias catch:

## DEV-R13-001 (HIGH, Drift / regression-risk) — the dynamic certify step is never gated

`build_certify_step` was given a production caller (`_run_certify_after_remediate`,
`executor.py:3409`), which satisfies the dispatch-reachability assertion's premise and
the CI test. **But it runs certify via a bare `roadmap_run_step(certify_step, config,
lambda: False)` (`executor.py:2170`) — OUTSIDE `execute_pipeline`.** Gate evaluation
(`gate_passed`) happens *only* inside `execute_pipeline` (`pipeline/executor.py:267,329`);
`_roadmap_run_step_impl` contains zero `gate_passed` calls (grep-verified; its own comment
at L1083-84 says "Returns PASS unconditionally; gate evaluation is handled separately").

**Consequence:** CERTIFY_GATE — all 3 semantic_checks (`certified_is_true`,
`per_finding_table_present`, `frontmatter_values_non_empty`) **and** the new
`code_assertion` — is **never evaluated** on the produced `certification-report.md`.
The headline R1.3 CodeAssertion is therefore runtime-inert in production; and certify now
emits an **unvalidated** certification artifact.

Compounding (grounded):
- **Not persisted:** `_save_state` runs at L3369, *before* the certify append at L3409 → certify is absent from `.roadmap-state.json`.
- **Non-halting:** the failures `sys.exit` at L3399 runs *before* certify → a certify FAIL only prints a line (`executor.py:2175-2178`).
- **Resume-asymmetric (DEV-R13-006):** the `--resume` path (`executor.py:3593`) has *no* `_run_certify_after_remediate` call — certify runs on fresh runs but not resumed ones.

So the dynamic certify is, as wired, ungated + unpersisted + non-halting. For R1.3's
narrow Contract #2 purpose (production caller exists; CI test enforces reachability) it
technically works. As a *certification* mechanism it is inert.

### Why this matters / why it's not a false alarm
A properly-wired terminal step flows through `execute_pipeline` so its gate is evaluated.
This implementation runs the step beside the gated executor, so the gate that gives the
step meaning never fires. PG8.1 verified "has a caller" and "CI test passes" — both true —
but did not check whether the production path evaluates the gate. The sonnet reviewer
(different model class than the executor) caught it; the haiku reviewer and the Tier-1
pass did not. This is the representational-diversity catch the protocol exists for.

## Recommended remediation (small, high-value)

**Option B (recommended):** inside `_run_certify_after_remediate`, after `roadmap_run_step`
returns, explicitly call
`gate_passed(certify_step.output_file, CERTIFY_GATE, envelope=<envelope>, repo_root=<repo_root>)`
and act on the verdict (set `certify_result.status`, persist, optionally halt). This closes
**both** DEV-R13-001 (gate bypass) **and** DEV-R13-002 (runtime-dormant code_assertion) in
one local change — and it would make R1.3 the first place the code_assertion actually fires
at runtime.

**Option A:** route certify through `execute_pipeline` so it is gated like every other step.

Either is a small, local change. The alternative is an explicit, eyes-open decision to defer
to R1.6 with DEV-R13-001 logged as a known gate-bypass (not just "runtime-dormant assertion").

## Full deviation ledger (6 findings)

| ID | Severity | Class | Finding |
|----|----------|-------|---------|
| DEV-R13-001 | **HIGH** | Drift (regression-risk) | Dynamic certify bypasses execute_pipeline → CERTIFY_GATE never evaluated |
| DEV-R13-002 | MEDIUM | Necessary | code_assertion runtime-dormant via envelope-None fail-open shim (documented R1.6 carry-forward) |
| DEV-R13-003 | LOW | Necessary | Assertion generalized vs design-doc §6.2 — *more* faithful to spec; sound |
| DEV-R13-004 | LOW | Authorized | `assert_envelope_artifacts_present` task-required (L516) but wired into zero gates (dead-but-tested) |
| DEV-R13-005 | LOW | Authorized | Live step count 13→14 (certify now runs); "budget unaffected" wording imprecise but 14≤14 holds |
| DEV-R13-006 | LOW | Drift | certify runs on fresh run but not on --resume path |

Tally: Authorized 2 · Necessary 2 · Drift 2 (1 regression-risk) · Regression 0.

## Adversarial-point dispositions (the 5 you asked about)

1. **Assertion generalization** → **Necessary/Compliant** (DEV-003). More faithful to §MVR §2 "reachable" than the design doc. Sound.
2. **envelope-None shim → runtime-dormant** → **Necessary staging** (DEV-002), BUT subsumed for certify by the bigger DEV-001 gate-bypass. Fail-open-introduction tension with Contract #5 is real and worth the explicit flag.
3. **assert_envelope_artifacts_present** → **Authorized** (task L516), not expansion. Note: no production consumer yet (DEV-004).
4. **Step-count budget** → **Genuinely satisfied** (14 ≤ 14), *not* sleight-of-hand. Precision note: live count 13→14 (DEV-005).
5. **certify executing in production** → **Authorized by §MVR §2** ("wire as the final step"). Behavioral-change magnitude (new LLM call every run) is real; and per DEV-001 the call is currently ungated.

## Reviewer ensemble

- **sonnet** (BLOCK): surfaced DEV-R13-001 (gate bypass). Grounded and correct.
- **haiku** (SHIP-WITH-NOTES): saw only the envelope-None shim (DEV-002), missed the full gate-bypass.
- **Calibration (opus, blind):** the gate-bypass is independently grounded (gate_passed never called in roadmap_run_step), so sonnet's finding carries high calibrated confidence; haiku's "ship" rests on an incomplete Q2 view. Merge weights the grounded finding.

## Evidence integrity (§11.2 gate)
- Citations total: 9 (gates.py:93-98; executor.py:2170, 3360-3409, 1083-84; pipeline/executor.py:267,329; task L516; ALL_GATES; design §6.2/§7.3). All independently re-Read this session.
- Citations dropped: 0. Citations inferred: 0.
- (Per §11.2 a zero-drop pass is treated as a flag, not a clean signal — each citation here was genuinely re-Read against current file state.)

## Bottom line
R1.3's substrate is correct and CI-enforces Contract #2. The certify *wiring* introduced an
ungated/unpersisted/non-halting execution path (DEV-R13-001) that makes the headline
assertion runtime-inert and emits an unvalidated certification artifact. Recommend the
Option-B local fix (closes DEV-001 + DEV-002 together) before treating Phase 8 as fully
closed — or an explicit decision to defer with the gate-bypass logged, not just the
"runtime-dormant assertion."
