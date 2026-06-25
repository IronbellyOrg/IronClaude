# QA Report — Research Gate (Partition P2 — Integration + Meta Cluster)

**Topic:** FR-DRS deterministic runtime-surface sweep + product/eval/SKILL integration
**Date:** 2026-06-22
**Phase:** research-gate
**Lens:** gap-detection
**Fix cycle:** N/A
**Fix authorization:** false (report only)

**Assigned files (P2):**
- 05-eval-path-grader-cases-materializer.md
- 06-skill-prose-demotion-and-refs.md
- 07-test-patterns-and-verification.md
- 08-mdtm-template-and-examples.md

**Also read:** research-notes.md (scope map), TDD §15 / §19 / §23 / §24

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file verification requires merging all partition reports.]

---

## Verification Log

### Scope-map note
`research-notes.md` is at the TASK-DIR root (`.../TASK-RF-.../research-notes.md`), NOT inside `research/`.
Located and read. EXISTING_FILES scope map cross-checked against P2 coverage below.

### Independent re-verification performed (zero-trust, not relying on research CODE-VERIFIED tags)
| Claim re-checked | Tool result | Verdict |
|---|---|---|
| grader.py:440-449 (metadata read + SKIP + C-6 bucketing) | `sed -n 440,449p` — exact match | R5 CODE-VERIFIED holds |
| grader.py:191 `check_yaml_list_len_eq` signature | `sed -n 191,193p` — exact match | R5 holds |
| C-5 materializer absence (no write of eval_metadata.json) | grep `eval_metadata` in workspace `.py` → only grader.py + aggregate_iteration.py, zero write/dump/copytree sites | R5/R7 "NOT LOCATED" CONFIRMED INDEPENDENTLY |
| SKILL.md:489 P1 "never emits a clean PASS…" sentence | `sed -n 489p` grep — exact literal present | R6 P1 holds |
| SKILL.md:465/466 "(UC-2 only)" scoping | `sed -n 465,466p` — both present | R6 P6 holds |
| SKILL.md:672 `contract_version: "1.6.0"` | `sed -n 672p` grep — exact | R6 §3.2 holds |
| ensemble.py:59 `REFLECT_CONTRACT_VERSION = "1.0"` | `sed -n 59p` — exact | R6 holds; usage line re-checked below |
| ensemble.py usage line of the constant | `grep -n` → used at **:502** | R6 says ":501", research-notes ":500", TDD ":378" — all 3 drift (MINOR-1) |
| `runtime_surface.py` greenfield absence | `ls` → No such file | research-notes holds |
| 5 `cases/uc2-*/` dirs exist | `ls -d` → all 5 present (37–41) | R5 holds |

---

## Gap-Detection Findings (7-point checklist + cluster cross-check)

### 1. Coverage gaps — FR-008 (eval), FR-011 (SKILL demotion), FR-013 (hygiene)
- **FR-008 (eval path / determinism):** COVERED. R5 §5.1 quotes FR-008 verbatim (tdd.md:289), maps both wire options (grader-oracle vs upstream materialize), recommends Option B. R7 §2.2 maps the ≥3-run determinism integration test. NO GAP.
- **FR-011 (SKILL §6.1 4b/4b′ demotion):** COVERED. R6 §1 gives current text at 465/466/487/489/491 + a precise demoted replacement + the I6 conditional. Re-anchored against live SKILL.md (489/465/466/672 independently re-verified). NO GAP.
- **FR-013 (verify-sync / UV-only / ruff format --check):** COVERED across R6 §5 (sync workflow) + R7 §3/§3.1 (the `make lint` ≠ `ruff format --check` split, scoped-ruff guidance). NO GAP. Strong: R7 catches the CI-vs-make-lint divergence explicitly.
- **FR-010 (fail-open DEGRADE/NEVER-STOP):** the PRESERVE half is covered by R6 P3 (SKILL:489 NEVER-STOP envelope); the safety-gate half by R7 §2.3 case 40. The *producer-side* FR-010 implementation lives in R1/R2 (out of P2 scope) — correctly deferred. NO GAP within P2.

### 2. C-5 materializer — is the must-build remediation actionable?
ADEQUATE, with one residual scoping ambiguity (see MINOR-2). R5 §4 confirms "NOT LOCATED" (I independently confirmed: zero write sites for eval_metadata.json) and §4 "Where the eval-path hook lands" gives a concrete build target:
- **What:** a small `materialize.py` (or a pre-grade hook in/around grader.py) that (a) flattens `evals.json` ids 37–41 → per-eval `eval_metadata.json`, (b) copies `cases/uc2-*/{expected.yaml,input/}` → `iterations/<iter>/eval-<name>/`, AND (c) runs `run_sweep()` to write `with_skill/outputs/contract.yaml` (6 scalars) + `runtime-surface-ledger.yaml` upstream of grading.
- **Where:** sibling to grader.py in `.dev/eval-workspaces/sc-reflect/`, wired into `make reflect-eval` BEFORE the grader (R5 §4 + §5.1; Makefile:505-516 is grader-only today).
- This is concrete enough for Phase-3 items. The "build Option B materializer" remediation is actionable.

### 3. 3 new test files + §15.4a derivation test + AC-5 safety-regression gate — mapped with enough structure?
WELL COVERED. R7 §2 maps all four surfaces with per-test structure:
- `test_runtime_surface.py` (§2.1): 6 unit fns + N∈{0,1,2} count-invariant + fast-path + §15.4a host (default).
- `test_runtime_surface_eval_determinism.py` (§2.2): 3× run, byte-identity assertion on grading.json — AC-2.
- `test_runtime_surface_safety_regression.py` (§2.3): cases 37/39/40/41 through verdict layer, FAIL on any clean-pass — AC-5. Per-case falsifier table matches TDD §24.2:1415 exactly (independently cross-read).
- §15.4a (§2.4): the 4-row truth table reproduced verbatim from TDD:1074-1079 (I cross-read tdd.md:1070-1081 — matches, including the literal string `"runtime_surface_unreached"` and the degrade-only→null row).
House idioms (no parametrize, `-> None`, enum-identity + exact exit_code, falsifier+control) are captured. NO GAP.

### 4. SKILL demotion PRESERVE list + conditional fallback — concrete enough for a non-destructive edit?
WELL COVERED. R6 §2 gives a verbatim PRESERVE table P1–P11 with current line numbers (P1/P6 independently re-verified at 489/465/466). The conditional fallback (§1.3) gives exact branch wording keyed on `runtime_surface_sweep_ran` PRESENCE — matching TDD §19.1 I6 (tdd.md:1193, cross-read: "field PRESENT (true OR false) → narrate-only; field ABSENT → legacy fallback"). The "RETARGET not delete" treatment of FR-RSR.7 (§3.3) matches TDD §19.2 bullet 3 (tdd.md:1201). A builder can write a surgical, non-destructive Edit item from this. NO GAP.

### 5. Missing mechanisms: ≥3-run determinism, grading.json byte-identity, materializer responsibilities?
- **≥3-run mechanism:** COVERED. R7 §2.2 ("`for _ in range(3):` or 3 explicit iteration dirs"); R5 §5.2 (run grader ≥3×, assert byte-identical). Both cite AC-2 / TDD §15.3:1043.
- **grading.json byte-identity:** COVERED. R7 §2.2 explicitly: "compare the serialized bytes (or json.loads-normalized dicts)… a passing-but-varying result must FAIL this gate." This is the correct identity-not-truthiness discipline.
- **Materializer responsibilities:** COVERED (see finding #2). R5 §4 enumerates the three responsibilities.
NO GAP.

### 6. Q4 ensemble-version reconciliation + OQ ratification as Open Questions?
PARTIALLY COVERED — see IMPORTANT-1.
- **Q4 (ensemble stamp):** R6 §3.2 covers it well: correctly scopes it as a CODE change to ensemble.py, explicitly OUT of the Phase-4 SKILL item, carried as Q4 / product-wire. This is the right call (ensemble.py is R2's seam, not P2's). (Minor line-cite drift — MINOR-1.)
- **OQ-DRS.1/.2/.3:** Only OQ-DRS.3 (no version bump) is addressed (R6 §3.2). OQ-DRS.1 (referrer engine floor) and OQ-DRS.2 (bare-path coverage) are R1/R2 territory and legitimately out of P2 scope — BUT the TDD §24.2:1416 Release Criteria require "OQ-DRS.1/.2/.3 + Q4 ratified … and recorded" as a release gate. No P2 file maps a task item that RECORDS the OQ ratification as an Open Questions block in the generated tasklist. R8 (template) is the natural owner of "where Open Questions / ratification land in the MDTM file" and does NOT mention the OQ-ratification release-criterion. See IMPORTANT-1.

### 7. TDD §24 Release Criteria items not covered (AC-5 gate, OQ ratification)?
- **AC-5 gate (`test_runtime_surface_safety_regression.py`):** COVERED (R7 §2.3, finding #3). Matches TDD §24.2:1415.
- **OQ ratification release-criterion (TDD §24.2:1416):** NOT mapped to a task item by any P2 file. See IMPORTANT-1.
- **Release-checklist item "all four rollout phases complete per exit criteria" + the §23.2 per-phase exit criteria:** R8 §3 maps the 4 phases to build phases but does NOT enumerate the per-phase EXIT CRITERIA (§23.2: e.g. Phase-1 "C-5 materializer located or AC-2 flagged conditional"; Phase-3 "AC-2 green no variance ≥3 runs") as acceptance hooks the gate items must check. See IMPORTANT-2.

---

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | File inventory + Status:Complete (4 files) | PASS | All 4 carry `Status: Complete` + a Summary section (grep'd lines 3 + Summary anchors) |
| 2 | Evidence density (file:line citations) | PASS | All 4 dense (>80% evidenced); R5/R6/R7 carry citation ledgers; independently re-verified 9 anchors |
| 3 | Scope coverage (FR-008/011/013 + AC-5 + materializer) | PASS | Every P2-owned FR + AC mapped (findings 1–7) |
| 4 | Doc cross-validation ([CODE-VERIFIED] tags honest) | PASS | 9/9 spot-checked CODE-VERIFIED tags confirmed against live source |
| 5 | Contradiction resolution (within P2 subset) | PASS w/ note | ensemble usage-line cite differs across R6/notes/TDD — MINOR-1; no semantic contradiction |
| 6 | Gap severity (any gap → FAIL) | FAIL | IMPORTANT-1 (OQ-ratification release-criterion unmapped); IMPORTANT-2 (per-phase exit criteria not surfaced as gate hooks); MINOR-1, MINOR-2 |
| 7 | Depth appropriateness (Deep tier) | PASS | R7 traces test→AC→falsifier end-to-end; R5 traces evals.json→eval_metadata→grader→contract.yaml |
| 8 | Integration point coverage | PASS | eval-wire seam (grader/materializer), SKILL §6.1 producer seam, test seams all documented |
| 9 | Pattern documentation | PASS | R7 §1 (test idioms), R8 §2-§6 (MDTM B2/A3/A4 + POST-reflect-gate shape) |
| 10 | Incremental-writing compliance | PASS | Files show section-growth structure; no one-shot artifacts |

## Summary
- Checks passed: 9 / 10 (item 6 = FAIL on gap presence)
- Checks failed: 1 (gap-severity gate — any gap regardless of severity = FAIL)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization: false — report only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| IMPORTANT-1 | IMPORTANT | R8 (08-mdtm) + R5/R6 cluster | TDD §24.2:1416 makes "OQ-DRS.1/.2/.3 + Q4 ratified and recorded" a RELEASE gate, but no P2 file maps a task item that records the OQ ratification (as an `### Open Questions` block) in the generated tasklist. Only OQ-DRS.3 is touched (R6). OQ-DRS.1/.2 are owned by R1/R2 but the *recording* obligation has no home. | Builder must add a Phase-4 (or Post-Completion) item that records ratification of OQ-DRS.1/.2/.3 + Q4 in an `### Open Questions` block, satisfying §24.2:1416. R8 should note this as a required item; coordinate with R1/R2 partition for OQ-DRS.1/.2 content. (Cross-partition: confirm R1/R2 cover it — partition note applies.) |
| IMPORTANT-2 | IMPORTANT | R8 §3 (08-mdtm phase mapping) | R8 maps the 4 TDD phases to build phases but does NOT surface the §23.2 per-phase EXIT CRITERIA as acceptance hooks for the per-phase verify items (e.g. Phase-1 "C-5 materializer located OR AC-2 flagged conditional"; Phase-2 "§5.3 pre-filter gates on derived surface_unreached"; Phase-3 "AC-2 green, zero variance ≥3 runs"; Phase-4 "AC-1 end-to-end"). A builder writing per-phase verify+sync items has no explicit exit-criteria checklist to bind them to. | R8 should add a per-phase exit-criteria table (lifted from TDD §23.2) so each phase's closing verify item asserts its TDD exit criterion, not just "make verify-sync clean." |
| MINOR-1 | MINOR | R6 §3.2 (06-skill) line cite | R6 states the stale stamp is "used at ensemble.py:501"; actual usage is **ensemble.py:502** (re-verified). research-notes says :500, TDD §19.2 says :378 — all three drift. The constant DEFINITION at :59 is correct everywhere. | Correct R6's ":501" → ":502". Low impact: ensemble.py reconciliation is explicitly carried OUT of the Phase-4 SKILL item (into Q4/product-wire), so the wrong line does not land in a P2-owned edit — but the cite should be accurate. |
| MINOR-2 | MINOR | R5 §4 (05-eval) | The C-5 remediation conflates two responsibilities under one "Option B" landing: (a) the GENERIC flatten+copy materializer, and (b) the FR-DRS-specific `run_sweep` oracle that writes contract.yaml. R5 notes both but does not cleanly separate them into distinct task items — risk a builder writes one over-large item (granularity violation). | R5 should explicitly recommend TWO Phase-3 items: (i) build/locate the generic materializer (flatten+copy), (ii) add the run_sweep oracle hook upstream of grading. Keeps item atomicity (template A3). |

## Actions Taken
None — `fix_authorization: false`. All findings are report-only.

## Recommendations
- Resolve IMPORTANT-1 and IMPORTANT-2 before the rf-task-builder runs: both are about *mapping release-criterion obligations to concrete task items*, which is exactly what the builder consumes. Unmapped → the generated tasklist will silently omit the OQ-ratification gate and per-phase exit-criteria binding.
- MINOR-1 / MINOR-2 are low-risk but cheap to fix in the research files (a one-line cite correction + a one-line item-split note).
- [PARTITION NOTE] IMPORTANT-1 depends on whether the P1 partition (R1/R2) covers OQ-DRS.1/.2 *recording*. The orchestrator must confirm at merge time. If P1 maps it, IMPORTANT-1 may downgrade to "ensure R8 references it."

---

## Confidence Gate
- VERIFIED: 10/10 checklist items checked with tool evidence (Read on all 4 assigned files + research-notes + 4 TDD section reads; Bash/grep re-verification of 9 source anchors).
- UNVERIFIABLE: 0
- UNCHECKED: 0
- **Confidence: Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**
- **Tool engagement:** Read: 9 | Grep: 0 | Glob: 0 | Bash: 5  (Bash calls each targeted a specific verification: grader lines, SKILL/ensemble/module/cases anchors, ensemble usage line, per-file Status/Gaps scan)
- Note: confidence ≥95% and UNCHECKED==0, so eligible for a verdict. The verdict is FAIL not on verification confidence but on the zero-tolerance gap rule (item 6): IMPORTANT gaps exist and ALL gaps regardless of severity = FAIL at a research gate.

---

## VERDICT: FAIL

**Rationale:** Gap-detection found 2 IMPORTANT + 2 MINOR gaps in the integration+meta cluster. Per research-gate zero-tolerance policy, ANY gap regardless of severity = FAIL; all must be resolved before synthesis. The cluster is otherwise strong: FR-008/011/013, the 3 test files, §15.4a, the AC-5 safety gate, the C-5 materializer build target, and the SKILL PRESERVE/conditional-fallback are all well-mapped and independently re-verified. The failures are scoping-of-release-criteria-to-task-items gaps (OQ ratification recording; per-phase exit-criteria binding), not factual errors.

## QA Complete
