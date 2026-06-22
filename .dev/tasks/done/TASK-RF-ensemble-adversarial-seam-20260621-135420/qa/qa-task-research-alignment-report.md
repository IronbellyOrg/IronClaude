# QA Report: Task-Research Alignment

**QA_MODE:** task-integrity
**LENS:** task-research-alignment
**Date:** 2026-06-21
**Stance:** ADVERSARIAL (assume builder dropped/misrepresented findings; find ≥3 gaps)

**Task file:** TASK-RF-ensemble-adversarial-seam-20260621-135420.md
**Research files analyzed:** 6 (01-05 + 06-gap-fill)
**Status:** COMPLETE — **VERDICT: PASS** (3 MINOR/INFORMATIONAL findings, none blocking)

---

## Method

Read all 6 research files (01-05 + 06-gap-fill) and the complete task file
(checklist Phases 1-3, Phase Gate QG.1-QG.8, Post-Completion PC.1-PC.5, Open
Questions). Independently re-verified the load-bearing code/path anchors against
live source on the worktree (ensemble.py line numbers, contract.py halted ladder,
the `_const_score` stub + 3 injection sites, the nested parent-task citation
paths). Adversarial stance applied: actively hunted for dropped findings,
misrepresented research, and fabricated anchors.

---

## Part 1 — Per-Research-File Key-Finding → Task-Item Coverage

### Research 01 (ensemble seam inventory)
| Key finding | Task encoding | Status |
|---|---|---|
| Widen `AdversarialScoreFn` alias at `ensemble.py:72` | Step 2.2 | COVERED |
| `run_adversarial_scorer` (`:244-271`) must widen in lockstep | Step 2.3 | COVERED |
| Lossy point `:271` / `extract_convergence_score` (`:336`) — full dict avail via `parse_adversarial_contract` | Step 2.3 (wrap, keep helpers' sigs) | COVERED |
| `build_reflect_contract` (`:360-407`) hard-codes 5 fields + status | Steps 2.5, threaded | COVERED |
| Hard-coded literals at `:385-390` (counts) + `:401-404` (3 bools + mirror) | Steps 2.5 anchors exact | COVERED |
| `_select_report_path` (`:488-497`) never considers adversarial path | Step 2.7 | COVERED |
| Seam call site `:221-239` feeds only float | Steps 2.4, 2.6 | COVERED |
| `_parse_convergence_score` named in brief DOES NOT EXIST | Task uses correct names `parse_adversarial_contract`/`extract_convergence_score` throughout | COVERED (fabrication avoided) |
| Backward-compat: only ensemble internals + 3 stub sites change; `runner.py:425` insulated | Key Constraints + Step 2.8 + research-06 cite | COVERED |

### Research 02 (adversarial-child output schema — SCORE-ONLY)
| Key finding | Task encoding | Status |
|---|---|---|
| Child emits SCORE-ONLY; 4 deviation fields = 0 grep hits in sc-adversarial | Task Overview "decisive scope fact"; OQ-PRODUCER | COVERED |
| R6 is NOT a pure key-rename | Task Overview explicit; Objectives | COVERED |
| `--suspect-source` is an inert/undefined flag (Unverified impact) | NOT mentioned in task | SEE Finding I-1 (minor) |
| `report_path` already sourced from swarm merge, not child | Step 2.7 (swarm as fallback) | COVERED |

### Research 03 (contract consumer constraints / FR-RH2.7)
| Key finding | Task encoding | Status |
|---|---|---|
| Defect is ensemble-side ONLY; `derive_verdict` frozen | Key Constraints FR-RH2.7 | COVERED |
| Stage-3 HALTED: `regression_present is True` → `regression` (`contract.py:315`) | Step 3.1 assertion target | COVERED |
| Load-bearing bool trap: non-bool → BLOCKED `malformed-contract-boolean` (`:200-209`) | Objective 1, Key Constraints, Steps 2.1/2.5/3.1 | COVERED |
| `deviation_count_by_class` = 4-key int dict; `regression>0`/`drift>0` halt | Steps 2.1/2.5 | COVERED |
| Exit map on `Verdict.exit_code` (models.py:38-49) frozen | Key Constraints; models.py READ-ONLY | COVERED |
| Clean path must still PASS (NFR-RH2.6) | Steps 2.6, 3.2 clean-default companion | COVERED |

### Research 04 (test patterns)
| Key finding | Task encoding | Status |
|---|---|---|
| New test = I12 in `test_ensemble_stub_integration.py` after I11 (L452) | Step 3.1 | COVERED |
| Reuse `_config(reviewers=3)`, `_distinct_stub`, `_run` pattern, I4 shape | Step 3.1 | COVERED |
| Keep convergence non-None so null-convergence DEGRADE doesn't mask HALT | Step 3.1 explicit | COVERED |
| Assert `is not Verdict.PASS` → HALTED/exit-10/reason regression | Step 3.1 | COVERED |
| Red-then-green (fails today, green after) | Steps 2.x + 3.1 framing | COVERED |
| NFR-7 banned tokens; keep ClaudeProcess | Key Constraints + Step 3.6 | COVERED |
| Optional unit companion in `test_ensemble_unit.py` (U5 pattern) | Step 3.2 | COVERED |

### Research 05 (template + citations)
| Key finding | Task encoding | Status |
|---|---|---|
| Template-02 B2 self-contained one-paragraph items | All items are single-paragraph w/ ensuring-clause + completion gate | COVERED |
| D3: no checklist items before Phase 1 | Phase 1 is first executable; Prereqs informational | COVERED |
| M3 lens-QA 8-step gate, adversarial framing, serialized fix | Phase Gate QG.1-QG.8 | COVERED |
| I22 standard intensity = 7 agents (3+3+1), 2 fix cycles | QG.2-QG.4 = 7 agents; QG.8 max 2 cycles | COVERED |
| I18 L3 test item (code task) | Step 3.3 | COVERED |
| Frontmatter mirror: start_commit, executor_model_class, parent_task, reflect_post not hand-authored | Frontmatter lines 19-20, 30, 16 | COVERED |
| POST reflect wrapper penultimate, flat form, recursion-breaker | Step PC.4 verbatim | COVERED |
| 4 citation anchors at correct paths | related_docs + References | COVERED |
| Cite BOTH OI-1 conditional AND consolidated R6 rejection (scope-expansion, not re-litigation) | Overview + References + Prereqs | COVERED |

### Research 06 (gap-fill — DECISIVE)
| Key finding | Task encoding | Status |
|---|---|---|
| GAP-2 scope fork: plumbing+test now, producer FOLLOW-ON | Task Overview + OQ-PRODUCER | COVERED |
| Field disposition table: convergence+report_path LIVE; 3 bools+counts default-clean-pending-producer | Task Overview verbatim disposition | COVERED |
| GAP-4 non-conflation: do NOT derive regression from low convergence; preserve null-convergence DEGRADE | Key Constraints "GAP-4 non-conflation" + Steps 2.3/3.1 | COVERED |
| GAP-1 backward-compat: T5/T6 autospec spies (:420/:445) do NOT break; only T1 `_const_score` + U10/U5 considerations | Key Constraints + Step 2.8 | SEE Finding I-2 (partial) |
| GAP-5 FR-RH2.7 proof: empty `git diff -- contract.py models.py`; AdversarialResult in ensemble.py | Steps 1.3/3.5/PC.2 + Objective 1 | COVERED |
| GAP-FIX nested parent-task path (flat MISSING) | related_docs + all citations use nested form (VERIFIED) | COVERED |

---

## Part 2 — CRITICAL Alignment Checks (the 6 spawn-prompt checks)

| # | Critical check | Verdict | Evidence |
|---|---|---|---|
| C1 | Encodes DECISIVE score-only finding (NOT pure key-rename; 3 reviewer-deviation fields default clean pending producer / OQ-PRODUCER) | PASS | Task Overview L74 verbatim "SCORE-ONLY … R6 is NOT a pure key-rename"; disposition split WIRED+LIVE vs WIRED-but-default-clean-pending-producer; OQ-PRODUCER at L319 marks producer emission OUT OF SCOPE |
| C2 | Encodes GAP-4 non-conflation (do NOT derive regression_present from low convergence; preserve null-convergence DEGRADE) | PASS | Key Constraints L129 "GAP-4 non-conflation"; Step 2.3 L189 "do NOT auto-derive regression_present from a low/None convergence score"; Step 3.1 keeps convergence NON-None 0.86 so null-convergence DEGRADE doesn't mask HALT |
| C3 | Encodes FR-RH2.7 proof (empty git diff on contract.py + models.py; AdversarialResult in ensemble.py NOT models.py) | PASS | Objective 1 + Constraints L126 "Place AdversarialResult in ensemble.py (NOT models.py)"; Step 1.3 baseline, Step 3.5 empty-diff proof, Step PC.2 combined gate. Independently verified frozen files clean at baseline (see Part 4) |
| C4 | Encodes load-bearing-bool type trap (genuine Python bool) | PASS | Objective 1 L82; Constraints L127; Steps 2.1/2.5/3.1 all require genuine `bool`, cite `_LOAD_BEARING_BOOL_FIELDS` (`contract.py:47-57`) + `malformed-contract-boolean` (`contract.py:200-209`). Verified those anchors exact in live source (Part 4) |
| C5 | Cites OI-1 table + QA CRITICAL #2 at correct NESTED paths | PASS | related_docs L34/L36 + Prereqs L103/L104 + References L114/L115 all use nested `…/TASK-RF-fr-rh2-headless-ensemble-20260620-024238/<artifact>`. All 4 nested paths VERIFIED to exist (Part 4); flat sibling correctly avoided per GAP-FIX |
| C6 | Backward-compat matches research 06 (autospec spies :420/:445 do NOT break; only _const_score sites + U10 update; runner.py:425 insulated) | PARTIAL PASS | runner.py:425 insulation, U10/U5/U6 green, `_const_score` single-helper-covers-3-sites all encoded (Step 2.8, QG.3 L265). The two autospec spies at :420/:445 are NOT explicitly named as non-breaking. See Finding I-2 |

---

## Part 3 — Fabrication Check (adversarial: anchors NOT present in any research file)

Hunted for task anchors/patterns with no research backing. Independently
re-verified the load-bearing ones against live source.

| Task anchor / claim | In research? | Live-source verified? | Verdict |
|---|---|---|---|
| `ensemble.py:72` alias | R01 §1, R06 GAP-2 | YES (exact) | OK |
| `run_adversarial_scorer` `:244-249` returns `float\|None` | R01 §3, R06 | YES (exact) | OK |
| `build_reflect_contract` `:360-366` sig | R01 §4 | YES (exact) | OK |
| hard-coded `deviation_count_by_class` at `:385-390` | R01/R03/R04 | YES — `:385` exact | OK |
| `regression_present:False` `:401`, `:402`, `:403`, `:404` mirror | R01/R03 | YES — 401/402/403/404 exact | OK |
| `_const_score` stub `:34-41`, injection sites `:93/:331/:356` | R01 §7, R04, R06 T1-T4 | YES (exact) | OK |
| `contract.py:307-328` `_halted_reason`, `:315` regression | R03 §1, R04, R06 GAP-4 | YES (exact) | OK |
| `_LOAD_BEARING_BOOL_FIELDS` `contract.py:47-57` | R03 §3, R05, R06 | YES (exact) | OK |
| `models.py:38-49` Verdict.exit_code | R03 §4 | (cited consistently across research) | OK |
| nested parent-task paths (OI-1, QA-CRIT2, consolidated) | R05 §3, R06 GAP-FIX | YES — all 3 exist | OK |
| I12 test name `test_i12_seam_regression_does_not_pass`, append after L452 | R04 §5 | (test-design anchor from R04) | OK |
| POST reflect flat wrapper + recursion-breaker (Step PC.4) | R05 §2.2 verbatim | — | OK |

**No fabricated anchors found.** Every file:line the task cites is either
verbatim from a research file or independently confirmed accurate against live
source. The task correctly AVOIDS the one fabrication trap research flagged: the
brief's non-existent `_parse_convergence_score` helper (R01 §3 NOTE) — the task
consistently uses the real `parse_adversarial_contract` / `extract_convergence_score`.

---

## Part 4 — Independent Live-Source / Path Verification

Ran during this QA pass (not trusting research transitively):

- `ensemble.py`: alias at L72; seam block L221-239; `run_adversarial_scorer` sig L244-249; `build_reflect_contract` sig L360-366 — all match task anchors byte-for-byte.
- Hard-coded literals: `deviation_count_by_class` at **L385**, `regression_present` **L401**, `unauthorized_deviation_present` **L402**, `needs_human_decision` **L403**, `user_decision_required` **L404** — EXACTLY as the task cites (`:385-390`, `:401-404`).
- `contract.py`: `_LOAD_BEARING_BOOL_FIELDS` L47-57 (contains all 4 mirror bools); `_halted_reason` L307-328 with strict `is True` checks at 315/317/319/321 and count fallbacks — matches.
- `_const_score` stub L34-41 returns bare float; 3 injection sites L93/L331/L356 — matches.
- All 4 nested parent-task citation paths (parent task file, OI-1 table, QA CRITICAL #2, consolidated findings) EXIST; flat sibling correctly not used.
- Task contains NO reference to `--suspect-source` / `deviation-classification` (the inert-flag trap from R02) — neither a fabrication nor a needed item.

---

## Part 5 — Research Caveats → Verification-Criteria Reflection

| Research caveat | Reflected in task verification? | Status |
|---|---|---|
| Non-bool load-bearing field self-inflicts BLOCKED (R03) | Steps 2.1/2.5/3.1 "genuine bool"; QG.3 FR-RH2.7 lens checks bool types | YES |
| Null-convergence DEGRADE must not mask HALT (R04/R06 GAP-4) | Step 3.1 keeps score 0.86 NON-None; QG.4 domain lens traces "DEGRADE rung firing first" | YES |
| FR-RH2.7 empty-diff is the proof (R06 GAP-5) | Step 3.5 + PC.2 combined gate `git diff --quiet`; QG.2 evidence lens re-runs diff independently | YES |
| Clean Tier-2 run must still PASS (NFR-RH2.6, R03/R06) | Step 2.6 + 3.2 clean-default companion; QG.4 "clean defaults still routes PASS" | YES |
| `extract_convergence_score`/`parse_adversarial_contract` keep sigs so U10 green (R06 GAP-1) | Step 2.3 explicit "do not change those two helpers" | YES |
| Producer emission is FOLLOW-ON not defect (R02/R05/R06 OQ-PRODUCER) | Open Questions OQ-PRODUCER + Follow-Up Items | YES |

---

## Findings (severity-rated)

### Finding I-1 — `--suspect-source` inert-flag caveat not surfaced (MINOR / informational)
- **Source:** Research 02 §1 (L30-37) flagged that `build_adversarial_prompt` emits a `--suspect-source` flag that `/sc:adversarial` does NOT define (0 hits), so it runs inert; "Unverified impact."
- **Gap:** The task does not mention this anywhere. Since the task does not edit `build_adversarial_prompt` and the flag mismatch is pre-existing + inert + out-of-scope for R6 (plumbing + test only), this is correctly NOT a checklist item.
- **Why MINOR, not a defect:** R02 itself rated the impact "Unverified" and the flag "inert." It is a latent pre-existing issue on the producer surface, squarely inside the OQ-PRODUCER follow-on territory, not the R6 deliverable. Omitting it from R6 is defensible. Recommend a one-line note under OQ-PRODUCER or Follow-Up Items so the finding is not silently lost.
- **Action:** Optional. Add to Follow-Up Items: "R02 flagged `build_adversarial_prompt` emits an undefined inert `--suspect-source` flag — verify/clean during the OQ-PRODUCER producer work."

### Finding I-2 — autospec-spy non-breakage (:420/:445) not explicitly named (MINOR)
- **Source:** Research 06 GAP-1 T5/T6 (L207-208) + Research 01 §7 establish the two `patch.object(runner_mod, "run_tier2_ensemble", autospec=True)` spies at `test_ensemble_stub_integration.py:420` and `:445` do NOT break under the seam widening (they spy the runner→ensemble boundary, not the score fn).
- **Gap:** The task encodes the conclusion (runner.py:425 insulated; only `_const_score` mechanically breaks; U10/U5/U6 stay green) but never explicitly names the :420/:445 spies as a verified non-breaking surface. An executor reading only the task could be surprised if those tests appear in the suite output.
- **Why MINOR, not a defect:** Step 3.3 runs the FULL `tests/cli/reflect tests/swarm` suite, which exercises i11/i11b; any unexpected breakage would surface there and route to Step 3.4's fix branch. The backward-compat conclusion the task DID encode is correct. This is a documentation-completeness nit, not a correctness gap — no missing checklist item results.
- **Action:** Optional. Add to Step 2.8 or Key Constraints a parenthetical: "(the two autospec `run_tier2_ensemble` spies at `test_ensemble_stub_integration.py:420/:445` are NOT affected — they spy the runner boundary, not the score fn; per research 06 GAP-1 T5/T6)."

### Finding I-3 — `status:"success"` stays hard-coded; QA CRITICAL #2 also named `degraded_components` + `status` (INFORMATIONAL / scope-correct)
- **Source:** QA CRITICAL #2 (R05 §3.4) recommended mapping "regression/unauthorized/human-decision booleans, **degraded_components**, and adversarial report path." Research 01 §4 also flags `status` (L379) is hard-coded `"success"` and "should reflect regression/halt."
- **Gap:** The task deliberately keeps `status:"success"` hard-coded (Step 2.5 "the `status` field stays `"success"`") and does NOT thread `degraded_components`.
- **Why this is CORRECT (not a dropped finding):** Research 03 §1 establishes the verdict ladder routes regression via the Stage-3 `regression_present is True` / `deviation_count_by_class.regression>0` HALT independently of `status` — so the regression-routing GOAL is met without touching `status`. The GOAL explicitly enumerates the 5 fields to thread (deviation_count_by_class, regression_present, unauthorized_deviation_present, needs_human_decision, report_path) and does NOT include `status` or `degraded_components`. Threading those would be scope creep beyond the stated GOAL. The task's scope fence is faithful to the GOAL even though it is narrower than QA CRITICAL #2's full recommendation. This is a deliberate, defensible scope boundary, not a misrepresentation.
- **Action:** None required. Optionally note in OQ-PRODUCER that `status` + `degraded_components` threading is part of the broader QA CRITICAL #2 fix deferred with the producer work, so the narrowing is explicit.

---

## Summary

- **Per-file coverage:** Every key finding across all 6 research files maps to a task item. No research finding was silently dropped.
- **All 6 CRITICAL checks:** 5 PASS, 1 PARTIAL PASS (C6 — autospec-spy detail, Finding I-2).
- **Fabrication:** ZERO fabricated anchors. The one known trap (non-existent `_parse_convergence_score`) was correctly avoided. All load-bearing anchors independently verified exact against live source.
- **Caveats:** All load-bearing research caveats (bool trap, GAP-4 non-conflation, FR-RH2.7 proof, clean-path PASS, helper-sig preservation, OQ-PRODUCER) are reflected in verification criteria.
- **Findings:** 3 total, all MINOR/INFORMATIONAL. None is a dropped or misrepresented research finding that changes the task's correctness; each is either an optional documentation-completeness nit (I-1, I-2) or a deliberate, GOAL-faithful scope narrowing (I-3).

The adversarial stance required finding ≥3 alignment gaps; 3 were found (I-1, I-2,
I-3), but on inspection NONE rises to a CRITICAL or IMPORTANT misalignment: the
task is a faithful, accurately-anchored encoding of the research. The findings are
recorded for completeness, not because they block the task.

---

## VERDICT: PASS

**Rationale:** The task file is a faithful, evidence-grounded encoding of all 6
research files. Every key finding has a corresponding task item; all 6 critical
alignment checks pass (one partially); zero fabricated anchors (the known
`_parse_convergence_score` trap was correctly avoided and independently
confirmed); all load-bearing anchors verified byte-exact against live source; all
research caveats are reflected in verification criteria. The 3 findings are all
MINOR/INFORMATIONAL — two optional documentation-completeness notes (I-1 inert
`--suspect-source` flag, I-2 autospec-spy non-breakage naming) and one deliberate
GOAL-faithful scope narrowing (I-3 `status`/`degraded_components` left to the
producer follow-on). None constitutes a dropped or misrepresented finding that
would cause the executor to build the wrong thing.

**Severity-rated issues (none blocking):**
- I-1 (MINOR): surface R02's inert `--suspect-source` flag under Follow-Up/OQ-PRODUCER — optional.
- I-2 (MINOR): explicitly name the :420/:445 autospec spies as non-breaking — optional.
- I-3 (INFORMATIONAL): note `status`/`degraded_components` deferral under OQ-PRODUCER — optional.
