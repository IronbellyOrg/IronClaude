# Diff Analysis: Tier-2 Reflect-Review Comparison

## Metadata
- Generated: 2026-07-07 (session-context ts)
- Variants compared: 2 (`variant-1-qwen3.6-plus`, `variant-2-glm-5.2`)
- Both flagged `--suspect-source` → every finding verified against ground truth (task file + git) before scoring
- Total differences found: 14 (structural 3, content 6, contradictions 2, unique 3) + 2 shared assumptions
- **Critical context:** kimi-k2.7-code (reviewer 0) returned `proxy_error` (0 bytes); glm-5.2's review is itself **truncated mid-sentence at M1** (ends `- *"`), yet its meta claims `status: success`. Only 1.5 usable reviews reached this comparison.

---

## Structural Differences

| # | Area | Variant 1 (qwen3.6-plus) | Variant 2 (glm-5.2) | Severity |
|---|------|--------------------------|---------------------|----------|
| S-001 | Severity vocabulary | 🔴/🟠/🟡 graded tiers + `CONDITIONAL FAIL` verdict | CRITICAL/IMPORTANT/MINOR + hard `FAIL` verdict | Medium — glm hammers harder; qwen calibrates finer |
| S-002 | Structure completeness | Complete: Exec-summary → findings → **suspect-source table** → missing-verification → **scoring recommendations** | **Truncated**: verdict → CRITICAL (C1–C3) → IMPORTANT (I1–I5) → MINOR (M1, cut off) | High — glm loses all MINOR content + any closing synthesis |
| S-003 | Actionability surface | Adds a downstream **adversarial-scoring weights** section (ensemble 1.5×, fallback 1.3×) | No downstream scoring guidance | Medium — qwen-only scaffold |

## Content Differences

| # | Topic | Variant 1 (qwen) approach | Variant 2 (glm) approach | Severity |
|---|-------|---------------------------|--------------------------|----------|
| C-001 | Terminal-gate/Done state | Finding 1 🔴 "Terminal State Mismatch & Unexecuted POST Gate" — task formally incomplete, POST reflect wrapper "has not run" | C1 CRITICAL "Terminal POST-reflect gate NEVER ran… self-certification regression" | Low — same conclusion, **both share a falsified premise** (see A-001) |
| C-002 | `make sync-dev` / verify-sync | Finding 2 🟠 "**Procedural Constraint Violation**" — running sync-dev violates isolation | I5 WARN "verify-sync green achieved by **mutation**, not by change set being in-sync" | **High — materially different severity; qwen's framing is a misread** |
| C-003 | Test-file count drift | Finding 3 🟡 — captures full **6/7/8 three-way oscillation** | I2 IMPORTANT — "**8 vs spec-pinned 7**" + flags `test_cli_smoke.py` extension too | Medium — complementary; each catches an axis the other misses |
| C-004 | `_vendor_from_model_id` F401 guard | Suspect-source row + missing-verification #2 — mechanism unspecified | I3 IMPORTANT — mechanism unspecified, blast-radius analysis of the two mitigation paths | Low — genuine agreement (both correct) |
| C-005 | Additive-only (`contract.py`/`models.py`) | Finding 4 🟡 "**cannot independently verify**" (no diff in provided data) | Implicit in additive-only concern; not a standalone finding | Low — qwen more explicit; **now VERIFIED 0-diff → resolves in executor's favor** |
| C-006 | `coverage_pct 1.0 / tcs 0` | Not raised | C3 CRITICAL "**numeric contradiction… coverage number is fabricated**" | Medium — glm-only, but **over-reaches** (PRE-reflect provenance field, note explains 46/46) |

## Contradictions

| # | Point of Conflict | Variant 1 position | Variant 2 position | Impact |
|---|-------------------|--------------------|--------------------|--------|
| X-001 | Severity of the `make sync-dev` action | 🟠 constraint **violation** ("even if nothing staged, it risks propagating drift") | WARN only ("whether or not staged… ambiguity") | Medium — qwen asserts a violation the constraint text does not support; glm's non-committal WARN is closer to correct |
| X-002 | Overall verdict weight | `CONDITIONAL FAIL` — return to executor, then run POST gate | `FAIL — internally contradictory` (harder, no conditional) | Medium — both inflated by the shared A-001 premise; neither is "return to executor," because the POST gate is running now |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | glm-5.2 | **C2 — final verification round (6.G11) skipped, replaced by "inline" pytest, logged as "None material."** | **HIGH — CONFIRMED: `qa-final-verification-{structural,content}.md` absent while all 5 prior phases have theirs. Highest-value catch in either review.** |
| U-002 | glm-5.2 | **I1 — `sprint/aienv.py` edited outside §10 change map.** | HIGH — CONFIRMED modified vs start_commit (1-line docstring xref); real scope drift, low risk. |
| U-003 | glm-5.2 | I4 — `1 xpassed` reported as clean headline, uninvestigated. | Medium — legitimate stale-xfail signal; qwen missed it. |
| U-004 | qwen3.6-plus | Suspect-source **table** (ensemble.py / fallback.py / openai_compat.py / test_ensemble_unit.py) + **adversarial-scoring weights** + explicit missing-verification checklist. | Medium-High — actionable downstream scaffold; aligns with the executor's own self-caught eager/lazy `TransportEnvError` bug. |

---

## Shared Assumptions (AD-2)

The "agreement = no scrutiny" blind spot. Both reviewers converge on a FAIL headline built on preconditions neither states — and the load-bearing one is **falsified by the runtime context**.

| A-NNN | Assumption | Source Agreement | Impact | Status |
|-------|------------|------------------|--------|--------|
| **A-001** | *The POST reflect wrapper gate has NOT run / is being bypassed, so a populated completion narrative = self-certification without the independent audit.* | C-001 / X-002 (both headline verdicts) | **HIGH** | **CONTRADICTED** — path `reflect/post/d8f84f71a397/` + return-contract `recommended_next_command` prove **this adversarial run is a sub-step of the POST gate, which is executing now.** Status "🟠 Doing" + unchecked terminal items are the **correct in-progress state**, not a regression. |
| **A-002** | *A completed-tone Task Summary at this point is premature self-certification.* | C-001 | MEDIUM | **CONTRADICTED (partial)** — the task's own checklist orders *populate Task Summary* (L482) **before** the POST gate (L484). A populated summary here is **required**. Only the literal `Completion Date: 2026-07-07` field (L492) is genuinely premature vs frontmatter `completion_date: ""`. |

**Promotion:** A-001 and A-002 are promoted to `[SHARED-ASSUMPTION]` diff points. They are the primary adversarial correction: both reviewers' CRITICAL/🔴 headline **must be downgraded** to a MINOR tonal-reconciliation note, because the premise that inflated it is false.

---

## Summary
- Structural differences: 3 (S-002 truncation is High)
- Content differences: 6 (C-002 severity split is High)
- Contradictions: 2 (both severity-calibration, both inflated by A-001)
- Unique contributions: 4 (U-001 glm C2 and U-002 glm I1 both CONFIRMED high-value)
- Shared assumptions surfaced: 2 (UNSTATED/CONTRADICTED: 2, STATED: 0) — **both CONTRADICTED**
- Highest-severity items: S-002, C-002, U-001, A-001
- Similarity: **~40%** — above the 10% floor; full debate proceeds.
