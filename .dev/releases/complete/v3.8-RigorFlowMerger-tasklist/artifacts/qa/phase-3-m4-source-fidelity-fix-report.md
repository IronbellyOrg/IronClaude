# QA Report — Phase 3 M4 Source-Fidelity Fix Cycle

**Topic:** RFMerger refresh — M4 source-fidelity remediation
**Task:** TASK-RF-rfmerger-refresh-20260618-172224
**Date:** 2026-06-18
**Phase:** fix-cycle (M4 source-fidelity)
**Fix authorization:** true (source-fidelity fixes only; PENDING preserved; no P2/P5 defaults)
**Adversarial axes applied:** AX-1 drift, AX-2 contradictions, AX-3 omissions, AX-4 weakened criteria, AX-5 invented content
**Input findings:** `artifacts/qa/phase-3-m4-source-fidelity-consolidated-findings.md` (11 findings: 3 CRITICAL, 8 IMPORTANT)

---

## Controlling P2 Cap Determination (dominant finding F-01/F-02/F-03)

**Adversarially-adopted P2 cap: `2 total passes` (1 original + 1 retry / 1 extra re-patch pass).**

**Primary citation:** `artifacts/adversarial-validation.md:141` —
P2 winner is Variant C (Human Checkpoint, 39/50). The automated-mode amendment, safeguard 4, states:
"**Cap at 2 total passes** (1 original + 1 retry) — RF experience shows diminishing returns beyond first retry."

**Corroborating citations:**
- `FINAL-REPORT.md:236` (R4 Dual-Mode Patch Recovery): "...regression detection (halt if previously-RESOLVED item becomes UNRESOLVED). **Cap at 2 total passes.**"
- `FINAL-REPORT.md:334` (risk K4): "**Cap at 2 total passes** limits blast radius."

**Determination:** The post-adversarial (adopted) cap is **2 total passes = original + 1 retry**. The
"3 total passes (original + 2 re-patch)" value is the **pre-adversarial** design cap (the rejected Variant B
loop, scored 20/50) — it was systematically reintroduced into spec.md, prd.md, tdd.md, and the ledger by a
prior in-task remediation that incorrectly treated the pre-adversarial value as canonical. AX-1 (drift) +
AX-4 (weakened criteria, a larger cap = looser blast-radius bound) + AX-5 (invented value not in the
controlling source) all fire on the "3 total" reintroduction.

---

## Final verdict and per-finding detail follow below (see "Overall Verdict: PASS").

---

## Applied Fixes — spec.md

### F-01 (CRITICAL, AX-1/AX-4/AX-5) — P2 cap drift → FIXED
Corrected every P2 cap reference from "3 total passes (original + 2 re-patch)" to the adversarially-adopted
**2 total passes (original + 1 re-patch)** with citation `artifacts/adversarial-validation.md:141`. Locations:
- L209-217 (FR-RFMERGE.2 Description) — value corrected + pre-adversarial "3 total" explicitly marked
  rejected/historical-only Variant-B (20/50).
- L230 (Cap counting: `k ∈ {2}`, pass 2 last); L227 (State model: loop adds pass `k=2` only); L239 (AC: 2-total cap).
- L96 (§2 summary bullet), L579 (YAML `1_extra_pass_cap_2_total`), L615 (risk row), L642 (test-matrix row).
- Residual "3 total" at L217 is the deliberate historical/rejected annotation (required by the fix directive), not drift.

### F-04 (IMPORTANT, AX-2/AX-4) — P5 determinism overclaim + sample mislabel → FIXED
- §2 summary: replaced blanket "same roadmap → same output" with the precise dual guarantee — "same roadmap →
  same **scored tiers**" (roadmap-only) and "same roadmap + same `feedback-log.md` → same advisory" (advisory
  varies with feedback). Cited `artifacts/adversarial-validation.md:219,246`.
- Exact-markdown sample row: mislabeled `| STANDARD | STRICT | … ⚠ STRICT-downgrade |` (an upgrade tagged as a
  downgrade) corrected to `| STRICT | STANDARD | … ⚠ STRICT-downgrade |`, now consistent with the STRICT-downgrade
  warning semantics ("scored tier is `STRICT` and the feedback suggests a lower tier").

---

## Applied Fixes — prd.md

### F-02 (IMPORTANT, AX-1/AX-4) — P2 cap drift → FIXED
- L505 (PR-2 Acceptance Criteria): "3-total-pass cap (original + at most 2 re-patch)" → **2-total-pass cap
  (original + at most 1 re-patch)**, cited `artifacts/adversarial-validation.md:141` + `FINAL-REPORT.md:236,334`;
  pre-adversarial "3 total" marked rejected/historical-only.
- L656 (risk-analysis row): "2-extra-pass cap (3 total)" mitigation + contingency → **1-extra-pass cap (2 total)**.
- Post-fix grep confirms zero residual "3 total" / "2 re-patch" / "2 extra" cap references in prd.md.

### F-05 (IMPORTANT, AX-1/AX-3) — P5 PENDING lacks historical-departure rationale → FIXED (option b)
PENDING preserved per spawn constraint (no P5 default chosen). Added a cited deliberate-departure note under
PR-5 explaining the refresh intentionally supersedes the historical **REVISE → advisory-only** recommendation
(`artifacts/adversarial-validation.md:227-249`; `FINAL-REPORT.md:240-246`) by elevating P5 to a PENDING
human decision with no default, while constraining **advisory-only as the only permitted retain shape** and
keeping auto-mutation (Variant-B) a non-goal. Also tightened the determinism claim on the AC line from
"same roadmap → same output" to "same roadmap → same **scored tiers**" (consistent with F-04). Did **not**
take option (a) (align to retained-advisory-only) because that would resolve the PENDING disposition, which
the spawn prompt forbids.

---

## Applied Fixes — tdd.md (heaviest concentration: 7 findings)

### F-03 (IMPORTANT, AX-2/AX-5) — P2 cap drift → FIXED
Corrected to the adversarially-adopted **2 total passes (original + 1 re-patch)** at: FR-002 row (§5.1),
§11.2 gated-flow prose + state model (`k ∈ {2}`, pass 2 last), §15 P2 bounded-loop test row, §12.4 retry table
(1 extra cycle), §20 R1 risk row. Pre-adversarial "3 total" marked rejected/historical-only at §11.2.
Post-fix grep: zero residual retained-context cap drift.

### F-06 (CRITICAL, AX-2/AX-3/AX-4) — P3 synthetic-dnsp contract under-specification → FIXED
§7.1 P3 data model expanded from the under-specified 3-field shape (`severity`/`task_range`/`source`, with the
non-canonical `task_range`) to the **full 7-field task-builder DM-003 contract** (`severity` HIGH/R-113,
`source`/R-114, `affected_range` verbatim/R-115, `evidence` never-blank/R-116, fixed `recommendation`/R-117,
2-element `dedup_key`/R-118, `found_n_times`/R-119) plus the all-agents-fail guard precedence (Path A/B/C, R-122),
strictly-additive merge (R-126), and N-1 cohort concurrency (INV-021/R-125). Grounded against
`src/superclaude/skills/task-builder/SKILL.md:873-911` (read in full). Added a narrower-projection note so the
reuse claim is integrity-preserving (no field-dropping projection asserted).

### F-07 (CRITICAL, AX-5) — invented `StageError` / "exactly as today" → FIXED
Grep verified **zero `StageError`** in `src/superclaude/skills/sc-tasklist-protocol/` and
`src/superclaude/cli/tasklist/` (Stage 7 is markdown protocol, not typed code). The token originates in the
historical adversarial doc (`adversarial-validation.md:51`, which itself wrongly called it "current behavior").
Added an authoritative **§7 source-fidelity caveat** globally reframing every `StageError` reference as
release intent / historical-prescribed, NOT a verified current return contract. De-claimed the load-bearing
false-current assertions: FR-003 AC (§5.1), §8.3 ("exactly as today" removed), §12.1 error table, §15 test row
(discovery reframed: raise site is a NEW requirement, not confirm-existing; test renamed
`test_dnsp_all_agents_fail_escalates`), §21 sequencing + §20 R6 ("Restore prior" → "Fall back to the
all-agents-fail escalation path", since nothing prior existed to restore).

### F-08 (IMPORTANT, AX-3) — `--spec` API row under-representation → FIXED
§8.1 `--spec` row expanded from reflect-only to the **four** verified current generator sites: §4.1a
Supplementary TDD Context (`SKILL.md:169-182`), §4.4a Supplementary Task Generation/enrichment
(`SKILL.md:246-271`), Stage-7 Supplementary TDD Validation (`SKILL.md:1297-1308`), Stage 10.5 PRE reflect
threading (`SKILL.md:1466-1471`). All four verified by grep of current source.

### F-09 (IMPORTANT, AX-2/AX-3) — stale `phase-template.md` checkpoint-heading lag undisclosed → FIXED
§10.1 phase-template component row now discloses the lag: the template still uses non-numbered
`### Checkpoint:` headings (`templates/phase-template.md:110,128`) while authoritative `SKILL.md` requires the
numbered `### T<PP>.<NN> -- Checkpoint:` form (`SKILL.md:356,360`; gate check 18 at `:1183`). States the
authoritative shape comes from inline `SKILL.md` until the reference template is updated. Both source facts
verified by grep.

### F-10 (IMPORTANT, AX-5) — `gate-results.txt` framed as existing output → FIXED
§7.1 file-body row reframed: the 20 *checks* exist (`SKILL.md:1132-1194`), but the **emitted artifact + per-line
PASS/FAIL format + trailing-summary contract are NEW (P4 design), with no current emitter**. Added explicit
"FUTURE artifact contract — no current emitter exists". §15 test discovery reframed to "attachment points for
the new emission, not existing emitters".

### F-11 (IMPORTANT, AX-1) — OQ-1 drifts from M3 fix direction → FIXED
§22 OQ-1 rephrased as **upstream-source cleanup only**: the refreshed validation matrix has already correctly
pinned `uv run pytest tests/cli/reflect/ -v` (`artifacts/refresh-validation-matrix.md:61,75,77` — verified), so
the matrix command is NOT blocked. The residual is the stale upstream `BUILD-REQUEST.md:15` / `research/07:137`
references; Target Date reworded off the false "before pinning the matrix command" gate.

---

## Applied Fixes — refresh-requirements-ledger.md (per explicit spawn directive)

### P2 cap harmonization (cross-document consistency) → FIXED
The consolidated report rated the ledger PASS on PENDING-status fidelity, but its **adversarial-revision** and
**test** columns carried the drifted "2-extra-pass cap (3 total passes)" into the *retained-form contract*.
Per the spawn directive to harmonize the cap across all four carriers, corrected both columns to
**1-extra-pass cap (2 total passes)** with `adversarial-validation.md:141` citation. The **Canonical
[HISTORICAL-ONLY]** column's "3 total passes" is left intact (it correctly describes the pre-adversarial
proposal) with an added NOTE distinguishing it from the adopted 2-total revision. PENDING disposition untouched.

---

## Overall Verdict: PASS (all 11 findings remediated; PENDING preserved; no out-of-scope edits)

## Items Reviewed

| # | Finding | Severity | Doc(s) | Result | Evidence |
|---|---------|----------|--------|--------|----------|
| F-01 | P2 cap drift | CRITICAL | spec.md | FIXED | 2-total cap applied at 7 sites; `adversarial-validation.md:141` cited; rejected value annotated. Grep: 0 residual retained-context drift. |
| F-02 | P2 cap drift | IMPORTANT | prd.md | FIXED | L505 AC + L656 risk row corrected; grep clean. |
| F-03 | P2 cap drift | IMPORTANT | tdd.md | FIXED | 6 sites corrected; grep clean (only historical annotation remains). |
| F-04 | P5 determinism overclaim + sample mislabel | IMPORTANT | spec.md | FIXED | Determinism split into scored-tier vs advisory; sample row STRICT→STANDARD now matches warning semantics. |
| F-05 | P5 PENDING lacks departure rationale | IMPORTANT | prd.md | FIXED | Cited deliberate-departure note added under PR-5; PENDING preserved (option b, not a). |
| F-06 | P3 DNSP contract under-spec | CRITICAL | tdd.md | FIXED | Full 7-field DM-003 contract + guard/merge/concurrency semantics; grounded `task-builder/SKILL.md:873-911`. |
| F-07 | invented `StageError` / "as today" | CRITICAL | tdd.md | FIXED | Grep proved 0 `StageError` in current source; §7 caveat + 6 de-claims applied. |
| F-08 | `--spec` API under-representation | IMPORTANT | tdd.md | FIXED | 4 verified `--spec` sites enumerated from `SKILL.md`. |
| F-09 | stale phase-template checkpoint lag | IMPORTANT | tdd.md | FIXED | Lag disclosed; `templates/phase-template.md:110,128` vs `SKILL.md:356,360,1183` verified. |
| F-10 | `gate-results.txt` framed as existing | IMPORTANT | tdd.md | FIXED | Reframed as FUTURE artifact contract; gate exists, emitter does not. |
| F-11 | OQ-1 drift from M3 fix | IMPORTANT | tdd.md | FIXED | OQ-1 = upstream cleanup only; matrix already pinned (`:61,75,77` verified). |
| — | ledger P2 cap (spawn directive) | (was PASS) | ledger | FIXED | Retained-form columns harmonized to 2-total; historical column annotated. |

## Summary

- Findings fixed: **11 / 11** (3 CRITICAL, 8 IMPORTANT) + ledger cap harmonization (spawn directive).
- Adversarially-adopted P2 cap applied: **2 total passes (1 original + 1 retry)**, citation `artifacts/adversarial-validation.md:141` (corroborated `FINAL-REPORT.md:236,334`).
- PENDING preserved for P2 and P5 — no default chosen, no auto-default introduced.
- Out-of-scope respected: did NOT edit `phase-outputs/reviews/` (P2 decision record), source code, or `.claude/` mirrors.
- Documents edited: `spec.md`, `prd.md`, `tdd.md`, `artifacts/refresh-requirements-ledger.md`. (`refresh-validation-matrix.md` needed no fidelity edit — verified clean.)

## Adversarial Axis Coverage

Every finding mapped to its firing axis (per consolidated findings + independent re-verification):
F-01 AX-1/AX-4/AX-5; F-02 AX-1/AX-4; F-03 AX-2/AX-5; F-04 AX-2/AX-4; F-05 AX-1/AX-3; F-06 AX-2/AX-3/AX-4;
F-07 AX-5; F-08 AX-3; F-09 AX-2/AX-3; F-10 AX-5; F-11 AX-1. No PASS-with-`none` rows (all 11 were FAIL→FIXED).

## Unresolved Issues / Residuals for the Executor

1. **P2 decision-record consistency (OUT OF SCOPE — noted per spawn instruction).** Harmonizing the P2
   decision record under `phase-outputs/reviews/p2-human-decision-record.md` was explicitly out of scope.
   If that record references a cap value, the executor should confirm it reads **2 total passes** for
   consistency with the now-corrected spec/prd/tdd/ledger. NOT edited here.
2. **OQ-1 upstream source cleanup (out of TDD edit scope).** `BUILD-REQUEST.md:15` and `research/07:137`
   still pin the stale `tests/reflect/` path. These are upstream sources outside the release dir; correct or
   formally waive before the `/task-builder` handoff. The matrix command itself needs no further action.
3. **`--spec` exact-input-contract inconsistency (pre-existing open risk, §22).** The `sc:tasklist` SKILL body
   is internally inconsistent ("exactly one input: the roadmap" vs `--spec` enrichment/autowire). This is an
   upstream-source reconciliation item already carried as an open risk; not a fidelity defect in the refresh docs.
4. **`StageError` raise-site is a NEW requirement.** Implementation must decide whether the all-agents-fail
   path surfaces as a typed `StageError` or the existing escalation; flagged as a discovery item in §7 + §15.

## Recommendation

Re-run the M4 source-fidelity gate (all six reports) on the corrected documents. All 11 deduplicated findings
are remediated with source-grounded citations; PENDING dispositions preserved; no out-of-scope edits.

## Confidence

**Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%**

Every fix was verified by either (a) grep over current source for the disputed token (`StageError`,
`--spec` sites, phase-template headings, matrix pin), or (b) post-edit grep confirming the corrected value
and zero residual drift, or (c) direct read of the controlling adversarial source for the cap value.

**Tool engagement:** Read: 12 | Grep: 8 | Glob: 0 | Bash: 8 (grep/ls via Bash) | tavily_search: 0 |
tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0 — no external lookup required; all
verification was against local source-of-truth files (Principle 6).

## QA Complete
