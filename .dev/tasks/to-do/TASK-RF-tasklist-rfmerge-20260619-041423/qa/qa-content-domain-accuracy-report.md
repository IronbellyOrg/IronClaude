# QA Report — task-qualitative (lens: domain-accuracy) — P2 Bounded Patch Loop

**Topic:** P2 Bounded Patch Loop (FR-RFMERGE.2) edits to `sc-tasklist-protocol/SKILL.md` — do they faithfully represent spec FR-RFMERGE.2 / §5.3, the recorded P2 decision, R-8, and adversarial-validation.md:141?
**Date:** 2026-06-19
**Phase:** task-qualitative (content domain-accuracy lens)
**Fix cycle:** N/A (report-only; fix_authorization: false — modified NOTHING)
**Stance:** ADVERSARIAL — assumed the P2 edits misrepresent spec FR-RFMERGE.2 / the recorded decision / R-8; hunted for ≥5 discrepancies.

> NOTE: This file previously held the P3 DNSP domain-accuracy report (06:56). It is the designated
> output path for THIS P2 review and has been overwritten with the P2 findings (same overwrite-with-note
> convention the prior occupant used).

---

## Overall Verdict: PASS

All five mandated domain-accuracy claims hold against their cited authority. The adversarial pass
surfaced five candidate discrepancies (monotonicity index off-by-one, residual "does NOT loop" gate,
stray `3-cap` token, `sc:task-unified` stale delegate, R-8 anchor drift) — every one resolved to
CORRECT on verification. The negative results are documented as evidence the edits were checked, not
waved through. No spec requirement dropped; no behavior beyond spec; matches the recorded
`retain-with-full-set-revalidation-and-guards` decision.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Full-set re-validation (not subset) | none | PASS | SKILL.md:1540 |
| 2 | Monotonicity + regression guards present | none | PASS | SKILL.md:1542-1543 |
| 3 | 2-total cap per adversarial-validation.md:141 | none | PASS | SKILL.md:1536,1544 |
| 4 | Non-overlap fence per R-8 | none | PASS | SKILL.md:1552,1554 |
| 5 | No requirement dropped / no behavior beyond spec / matches recorded decision | none | PASS | SKILL.md:1536,1546; spec:215-251 |

---

## Claim-by-Claim Verification (each cites authority + actual edit)

### CLAIM 1 — Full-set re-validation (NOT subset): PASS

**Authority.**
- Spec FR-RFMERGE.2:232-233 (Retained contract / Compared data): *"each pass re-runs the **full** Stage-7 validation set over the bundle (not a sampled or unresolved-only subset) and records the failing-finding set `F_k`."*
- §5.3 P2_bounded_patch_loop:605 — `revalidation: "full-set (NOT subset-only)"`.
- Recorded decision token: `retain-with-full-set-revalidation-and-guards` (spec:223, 248).

**Actual edit.** SKILL.md:1540 step 1: *"Compute `F_k` by re-running the FULL Stage-7 2N validation set
(reuse the Stage-7 fan-out primitive — a complete re-validation of every phase, NOT a subset re-read of
only the previously-failing items), so regressions in previously-PASS items are detectable."* The gate at
:1536 names the decision `RETAINED: full-set-revalidation-and-guards`.

**Verdict.** MATCH. The edit re-runs the entire Stage-7 2N fan-out per pass, explicitly forbids the
subset/unresolved-only re-read, and ties it to regression detectability — exactly the spec's "full set"
semantics, and the literal mechanism the recorded decision token names. PASS.

### CLAIM 2 — Monotonicity + regression guards present: PASS

**Authority.**
- Spec FR-RFMERGE.2:236 (Monotonicity predicate): *"`|F_{k}| < |F_{k-1}|` must hold to continue; if
  `|F_k| >= |F_{k-1}|` the loop halts."*
- Spec FR-RFMERGE.2:238-240 (Regression predicate): *"any finding that was PASS at pass `k-1` and is FAIL
  at pass `k` halts the loop immediately (regression takes precedence over monotonicity), reusing the
  existing PR-02 regression semantics in `task-builder/SKILL.md:1290-1305`."*
- §5.3:606 — `guards: ["monotonicity_guard", "regression_detection", "1_extra_pass_cap_2_total"]`.
- Reuse source verbatim: task-builder PR-02 4-step ordering + API-004 wire strings
  (`task-builder/SKILL.md:1283,1294-1303`).

**Actual edit.**
- Monotonicity — SKILL.md:1543: *"if `|F_k| > 0` AND `|F_{k+1}| >= |F_k|` (the patchable failing set did
  NOT strictly shrink), HALT and emit the byte-exact halt string `[HALT-MONOTONICITY] |F|=<n>` (with `<n>`
  = `|F_{k+1}|`)."*
- Regression — SKILL.md:1542: *"if any patchable item that PASSED at pass `k` is FAILing at pass `k+1`,
  HALT immediately and emit the byte-exact halt string `Regression detected on Item X.Y — previously PASS
  at cycle N, now FAIL. Halt overrides monotonicity check.`"* with "Regression ALWAYS runs and exits
  BEFORE the monotonicity check."
- Ordering — SKILL.md:1541: *"Apply the PR-02 4-step ordering ... in this exact order, EXIT on the first
  match — `regression → monotonicity → hard-cap → proceed`."*

**Byte-exactness cross-check against PR-02 source.** task-builder/SKILL.md:1283 (API-004 wire-ABI table)
gives the regression string `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt
overrides monotonicity check.` and the monotonicity string `[HALT-MONOTONICITY] |F|=<n>`. Both are
reproduced character-for-character in the edit, em-dash (`—`, NOT hyphen) preserved in the regression
string. The 4-step ordering at :1541 matches task-builder/SKILL.md:1296 verbatim
(`regression → monotonicity → hard-cap → proceed`, exit-on-first-match).

**Index-alignment check (adversarial — the most likely off-by-one trap).** Spec indexes the predicate as
`|F_k| < |F_{k-1}|`; the edit indexes on the transition `k → k+1` with halt `|F_{k+1}| >= |F_k|`. Mapping:
spec's continue-condition `|F_k| < |F_{k-1}|` at spec-k=2 ⇔ edit's continue-condition `|F_{k+1}| < |F_k|` at
edit-k=1 (k+1=2). They are the SAME inequality under the relabeling (spec counts the predicate AT the new
pass; the edit counts it ON the transition into the new pass). No off-by-one. The regression-precedence
ordering (regression evaluated and exited BEFORE monotonicity) matches spec:238-240 and PR-02:1270/1298.

**Verdict.** MATCH. Both guards present, regression-over-monotonicity precedence honored, halt strings
byte-exact to the reused PR-02 contract, no index drift. PASS.

### CLAIM 3 — 2-total cap per adversarial-validation.md:141: PASS

**Authority (the pin, read directly).** adversarial-validation.md:141: *"**Cap at 2 total passes** (1
original + 1 retry) — RF experience shows diminishing returns beyond first retry."* Spec
FR-RFMERGE.2:241 (Cap counting): *"at most 1 re-patch pass (`k` ∈ {2}); pass 2 is the last permitted pass
(2 total passes; adversarially-adopted cap, `artifacts/adversarial-validation.md:141`)."* §5.3:606 token
`1_extra_pass_cap_2_total`. Spec:219-221 explicitly marks the "3 total passes" value as the **rejected**
Variant-B cap, historical-only.

**Actual edit.**
- SKILL.md:1536: *"capped at **at most ONE re-patch pass (2 TOTAL passes, `k ∈ {2}` — NOT task-builder's
  3-cap)**."*
- SKILL.md:1544 (hard-cap step): *"if `k+1 > 2` (i.e. one re-patch pass already ran), STOP — the cap is 2
  TOTAL passes."*
- SKILL.md:1545 (proceed step): loop-back gated on `k < 2`.
- SKILL.md:1538: `k = 1` is the initial Stage 7→10 pass (anchors the count so 2 total = original + 1).

**Verdict.** MATCH. Cap is exactly 2 TOTAL passes (`k ∈ {2}`, one re-patch), reachable hard-cap at
`k+1 > 2`, with the rejected 3-cap explicitly negated (`NOT task-builder's 3-cap`). The arithmetic is
internally consistent: initial k=1 + one re-patch k=2 = 2 total, no path continues past k=2 (proceed
requires `k < 2`; hard-cap fires at `k+1 > 2`). Matches the pin at :141 and spec:241 exactly, and correctly
diverges from task-builder's own per-gate caps. PASS.

### CLAIM 4 — Non-overlap fence per R-8: PASS

**Authority (research/08 R-8:55-57, read directly).**
- R-8 predicate: *"`set(P2_loop_findings) ∩ set(stage_10_5_reflect_pre_findings) == ∅`."*
- R-8 three independent disjointness levers: (1) different STAGE (loop confined to 7→10, fenced before
  10.5 at `SKILL.md:1462`); (2) different FINDING-SOURCE (QA-gate validation findings vs reflect
  spec-coverage gaps); (3) different REMEDIATION OWNERSHIP (P2 re-patches via `sc:task`; Stage 10.5 reflect
  only AUTHORS/offers remediation, never auto-mutates phase files).
- Spec FR-RFMERGE.2:242-244 (Stage-10.5 non-overlap / exclusion proof obligation) + NFR-RFMERGE.2:628
  ("Zero double-remediation of the same finding") + §5.3:607 `must_not: "overlap Stage 10.5 reflect
  remediation"`.

**Actual edit.**
- Predicate — SKILL.md:1554: *"**Non-overlap invariant (P2 ⟂ Stage-10.5, R-8):** `set(P2_loop_findings) ∩
  set(stage_10_5_reflect_pre_findings) == ∅`."* — byte-identical to the R-8 predicate.
- Three levers — SKILL.md:1554 enumerates (1) distinct stage, (2) distinct finding-source, (3) distinct
  remediation-ownership — matching R-8's three levers one-for-one (P2 mutates via `sc:task --compliance
  strict`; Stage 10.5 reflect-pre authors advisory findings, does not execute the loop).
- Fence — SKILL.md:1552: Stage 10.5 is *"fenced after the Stage 8-10 patch chain **including any P2
  bounded loop-back iterations**"*; *"The P2 bounded patch loop (Stage 10 gate) MUST fully
  converge/terminate ... BEFORE Stage 10.5 fans out."* This realizes R-8 lever (1) "fenced before 10.5"
  and supplies the temporal guarantee that no finding is in-flight in both surfaces.

**Verdict.** MATCH. The writable disjointness predicate is reproduced verbatim from R-8, all three levers
are present and correctly mapped, and the convergence fence forces P2 to terminate before the 10.5 fan-out
— satisfying both R-8 and the spec NFR-RFMERGE.2 zero-double-remediation target. PASS.

### CLAIM 5 — No requirement dropped / no behavior beyond spec / matches recorded decision: PASS

**Authority.** Recorded P2 human decision `retain-with-full-set-revalidation-and-guards` (spec:223,248;
§5.2 Human-decision gate:575; §5.3:603; phase-5 summary:5). The decision's full meaning is fixed by the
"Retained contract" (spec:229-244) and the four Acceptance Criteria (spec:248-251). Delegate remap
`sc:task-unified → sc:task` (spec:226-227, §5.3:608).

**Requirement-by-requirement coverage of the recorded contract:**

| Spec-required element | Anchor | Present in edit? |
|---|---|---|
| Full-set re-validation | spec:232, §5.3:605 | YES — SKILL.md:1540 (Claim 1) |
| Monotonicity guard | spec:236 | YES — SKILL.md:1543 (Claim 2) |
| Regression detection (PR-02 semantics, precedence) | spec:238-240 | YES — SKILL.md:1542 (Claim 2) |
| 2-total-pass cap | spec:241, pin:141 | YES — SKILL.md:1536,1544,1545 (Claim 3) |
| Non-overlap with Stage 10.5 | spec:242-244 | YES — SKILL.md:1552,1554 (Claim 4) |
| State model `(k, F_k, F_{k-1})`, k starts at 1, adds k=2 | spec:234-235 | YES — SKILL.md:1538 (k=1 initial), :1526-1534 per-iteration state table |
| Delegate remap `sc:task-unified → sc:task` | spec:226-227 | YES — SKILL.md:1545 (`sc:task --compliance strict`); grep: 0 `sc:task-unified` hits |
| Loop is advisory, bundle still ships | NFR/Stage-10.5 model; spec §5.3:618 | YES — SKILL.md:1546 ("the bundle still ships; the loop is an advisory remediation, not a hard blocker") |

**No behavior beyond spec.** The edit adds nothing the spec did not authorize: it reuses the EXISTING
task-builder PR-02 protocol verbatim (no new retry loop, no new stage), the synthetic-dnsp `F_k` exclusion
folds in the documented OQ-PRE-1 resolution (consistent with the DM-003 cross-cycle dedup rule the spec
references), and the loop-back wiring (Stage 10 → Stage 9 → Stage 10) reuses the existing Stage-9
`sc:task` delegate. The orchestrator-never-patches separation-of-concerns is preserved (SKILL.md:1497,
1545).

**Matches the recorded decision.** The recorded value is `retain-with-full-set-revalidation-and-guards`
(NOT `defer`, NOT auto-defaulted). The edit at :1536 names the gate
`RETAINED: full-set-revalidation-and-guards` and implements every guard the retain decision entails. The
rejected Variant-B 3-cap is explicitly negated, not shipped.

**Verdict.** MATCH. Every element of the recorded retain contract is present; no spec requirement dropped;
no unauthorized behavior added; the implementation is the literal `retain-with-full-set-revalidation-and-guards`
decision. PASS.

---

## Adversarial Discrepancy Hunt (target ≥5; all NEGATIVE — documented as proof of checking)

| # | Hypothesized discrepancy | Test performed | Result |
|---|--------------------------|----------------|--------|
| H1 | Monotonicity index off-by-one: edit uses `\|F_{k+1}\| >= \|F_k\|` while spec uses `\|F_k\| >= \|F_{k-1}\|` | Relabeled both onto the same transition (spec-k=2 ⇔ edit-k+1=2); compared continue/halt conditions | NO DISCREPANCY — identical inequality under k-relabeling; spec counts AT new pass, edit counts ON transition into it |
| H2 | Stale "the skill does NOT loop" gate left in place, contradicting the new loop | `grep -n "does NOT loop\|if a future re-validation"` | NO DISCREPANCY — 0 hits; old no-loop gate fully replaced (phase-5 summary:16 "count is now 0" confirmed) |
| H3 | Rejected 3-total-pass cap surfaced as operative text | `grep -n "3 total\|3-cap\|k ∈ {3}\|original + 2"` | NO DISCREPANCY — only hit is the correct negation "NOT task-builder's 3-cap" at :1536; no operative 3-cap |
| H4 | Stale `sc:task-unified` delegate not remapped | `grep -n "sc:task-unified"` | NO DISCREPANCY — 0 hits repo-side; Stage-9 delegate is `sc:task --compliance strict` (:1545) |
| H5 | Halt strings drifted from PR-02 (hyphen vs em-dash, wrong token) | Char-for-char diff of :1542-1543 against task-builder/SKILL.md:1283 API-004 wire-ABI table | NO DISCREPANCY — both strings byte-exact, em-dash `—` preserved in regression string |
| H6 | R-8 predicate paraphrased/weakened rather than reproduced | Diff SKILL.md:1554 predicate against research/08 R-8:56 | NO DISCREPANCY — `set(P2_loop_findings) ∩ set(stage_10_5_reflect_pre_findings) == ∅` byte-identical |
| H7 | Synthetic-dnsp wrongly counted in `F_k` (would spuriously trip monotonicity halt) | Read :1540 + :1349 cross-cycle-dedup rule | NO DISCREPANCY — `F_k` EXCLUDES `source: "synthetic-dnsp"`; persistent synthetic is DEDUP not regression (OQ-PRE-1 fold-in correct) |

Seven adversarial hypotheses raised, all falsified by direct tool evidence. The edit withstands the
adversarial domain-accuracy lens.

---

## Summary
- Checks passed: 5 / 5 (mandated domain-accuracy claims)
- Checks failed: 0
- Critical issues: 0 | Important: 0 | Minor: 0
- Issues fixed in-place: 0 (report-only; fix_authorization: false)
- Adversarial hypotheses raised: 7 | falsified: 7
- Axis lens status: drift-axis-inactive — no BUILD_REQUEST.GOAL verbatim was supplied in the spawn
  prompt or reproduced in the phase-5 summary; AX-1 Drift disabled for this review. AX-2..AX-5 applied
  (no axis-attributable finding fired; all rows annotated `none` per closed-set vocabulary).

## Issues Found
None. (No CRITICAL / IMPORTANT / MINOR findings at the domain-accuracy lens.)

## Actions Taken
None (report-only). Nothing in `SKILL.md` or any other file was modified.

## Self-Audit
**(a) Reliance list — structural items NOT re-verified here (out of this lens):** This is a content
domain-accuracy review, not a structural pass. I did NOT re-verify section numbering, template
conformance, or cross-reference existence (covered by the structural QA agents:
qa-structural-internal-consistency / -template-conformance / -evidence-quality). No
`## Inherited Structural Verdict` block was supplied in the spawn prompt; standalone behavior applied.

**(b) Independent semantic checks (≥1 required) — performed with own tool engagement:**
- Read the actual pin adversarial-validation.md:141 (not a report's restatement) and confirmed "Cap at 2
  total passes (1 original + 1 retry)" — verifies Claim 3 at source.
- Read research/08 R-8:55-57 directly and diffed its predicate against SKILL.md:1554 — byte-identical
  (Claim 4).
- Diffed the two halt strings in SKILL.md:1542-1543 char-for-char against the task-builder API-004
  wire-ABI table at task-builder/SKILL.md:1283 — em-dash preservation confirmed (Claim 2).
- Performed the monotonicity index-relabeling proof (spec `|F_k|<|F_{k-1}|` ⇔ edit `|F_{k+1}|<|F_k|`) by
  hand rather than trusting the summary's "PR-02 reuse fidelity" assertion (Claim 2 / H1).
- Ran grep sweeps for the four stale/forbidden tokens (does-NOT-loop, 3-cap, sc:task-unified) against
  live source (H2-H4).

## Confidence Gate
- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 7 | Grep: 1 (multi-pattern bash sweep covering 4 token classes) | Glob: 0 | Bash: 2
- Every checklist item maps to a specific Read/grep against the cited spec line, pin line, R-8 line, or
  SKILL.md edit line. No item marked VERIFIED by relying on another report.
- UNCHECKED items: none. UNVERIFIABLE items: none.
- **Web research:** none performed (all authorities are local files); Tavily-first rule not triggered.

## Recommendations
- None blocking. The P2 edits faithfully implement spec FR-RFMERGE.2 / §5.3, the recorded
  `retain-with-full-set-revalidation-and-guards` decision, R-8, and adversarial-validation.md:141.
- Green light to proceed from the domain-accuracy lens.

## QA Complete
