# QA Report — Task Integrity (Structural: cap-arithmetic / internal-consistency)

**Topic:** P2 bounded patch loop — cap-arithmetic & internal-consistency lens
**Date:** 2026-06-19
**Phase:** task-integrity (structural lens, REPORT-ONLY — fix_authorization: false)
**Fix cycle:** N/A
**Lens:** cap-arithmetic / internal-consistency
**Stance:** Adversarial — assume the cap / full-set re-validation is wrong; hunt for ≥5 errors.

> NOTE: This path previously held a P3 branch-logic report (which itself overwrote a P1 mirror-sync
> report). The Phase 5 spawn prompt directs the P2 cap-arithmetic lens report to this exact path; it
> has been overwritten with the P2 report below, per the same precedent the prior passes set.

---

## Overall Verdict: PASS

All five lens criteria are satisfied with citable source text. Cap = exactly 2 TOTAL passes
(`k ∈ {2}`, one re-patch), distinct from task-builder's 3-cap; the loop re-runs the FULL Stage-7
2N validation set (not a subset re-read); the Stage 10 → Stage 9 → Stage 10 wiring is internally
consistent with the residual PatchChecklist scoped to `F_k`; the per-iteration state recorded is
sufficient for the monotonicity/regression guards; and the loop is nested under the non-short-circuit
branch only. The adversarial probes surfaced consistency nits (documented in Issues Found) — none
defeats the cap or the guards, so the verdict stands at PASS.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Cap = exactly 2 TOTAL passes (`k ∈ {2}`, one re-patch), NOT 3-cap | PASS | SKILL.md:1536 — "capped at **at most ONE re-patch pass (2 TOTAL passes, `k ∈ {2}` — NOT task-builder's 3-cap)**". Reinforced by hard-cap `if k+1 > 2 ... STOP — the cap is 2 TOTAL passes` (1544) and proceed-guard `AND k < 2` (1545). No `k ∈ {3}` / `k < 3` / `> 3` token anywhere (grep). |
| 2 | Loop re-runs FULL Stage-7 2N set (not subset re-read) | PASS | SKILL.md:1540 step 1 — "Compute `F_k` by re-running the FULL Stage-7 2N validation set (reuse the Stage-7 fan-out primitive — a complete re-validation of every phase, NOT a subset re-read of only the previously-failing items), so regressions in previously-PASS items are detectable." Acceptance-criterion #2 in phase-5 summary echoes "full Stage-7 2N re-run (not subset)". |
| 3 | Loop-back wiring (Stage 10 → Stage 9 → Stage 10) consistent; residual PatchChecklist scoped to `F_k` | PASS | Stage 9 is the named loop-back target — SKILL.md:1497 "**P2 loop-back target:** Stage 9 is the loop-back target re-entered by the P2 bounded patch loop … residual `PatchChecklist.md` scoped to `F_k`". Proceed clause (1545): "loop back to **Stage 9** — re-delegate `sc:task --compliance strict` against a **residual PatchChecklist scoped to `F_k`** — then re-run Stage 10." Round-trip closed. |
| 4 | Per-iteration state sufficient for monotonicity/regression guards | PASS | SKILL.md:1526 records per pass `k`: `k`, `\|F_{k-1}\|`, `\|F_k\|`, PASS-set, regression set — "sufficient to evaluate the regression-then-monotonicity-then-hard-cap ordering on each `k → k+1` transition." Regression guard needs PASS-set + regression-set (1542); monotonicity needs `\|F_k\|`+`\|F_{k-1}\|` (1543); hard-cap needs `k` (1544). All five recorded columns map to a guard input. |
| 5 | Loop nested under non-short-circuit branch only (does not fire on Stage-8 zero-finding short-circuit) | PASS | Stage 8 short-circuit (SKILL.md:1379-1388) "skip Stages 9 and 10. The skill is complete." The P2 loop lives in the **Stage 10 gate** (1536), which is unreachable when Stages 9-10 are skipped. Synthetic-present guard (1390) prevents a synthetic from taking the short-circuit, so the loop only runs when Stage 10 actually executed. |

---

## Adversarial Deep-Dive: Cap Arithmetic

I attacked the cap from every off-by-one angle. The arithmetic is consistent across all four
expressions of the bound:

| Expression | Location | Reading | Consistent? |
|---|---|---|---|
| `k ∈ {2}` ("2 TOTAL passes", "at most ONE re-patch pass") | 1536 | Total passes capped at 2; pass 1 = initial, pass 2 = the single re-patch | yes |
| Hard-cap `if k+1 > 2 ... STOP` | 1544 | When `k=2`, `k+1=3 > 2` → STOP before a 3rd pass ever launches | yes |
| Proceed guard `... AND k < 2` | 1545 | Loops only from `k=1` (`1<2` true) to `k=2`; at `k=2` (`2<2` false) it does NOT loop | yes |
| `capped at k=2` (STOP outcome) | 1546, 1552 | Termination label matches | yes |

**Probe — could the loop run a 3rd pass?** No. Two independent guards forbid it: the proceed
clause requires `k < 2` (fails at k=2), and the hard-cap fires at `k+1 > 2` (fires at k=2). Either
alone caps at 2; together they are redundant-safe.

**Probe — the worked iteration table (1529-1534).** Row 1: `k=1`, `|F_{k-1}|`=—, `|F_k|`=2,
initial pass. Row 2: `k=2`, `|F_{k-1}|`=2, `|F_k|`=1, "shrank 2→1, no regression → finalize
(cap k=2)". This is arithmetically correct: 1 < 2 satisfies strict-shrink, no regression, and
`k=2` hits the cap → finalize. The table terminates at the cap exactly as the gate prescribes.
Note the table shows the **clean-cap** path (residual `|F_2|`=1 still nonzero but capped) — i.e.
it correctly depicts that hitting the cap with residual findings finalizes-with-UNRESOLVED rather
than looping, matching 1546 ("Findings that remain UNRESOLVED at termination are logged for human
review; the bundle still ships").

**Probe — is `k ∈ {2}` notation itself sound?** Mildly loose (see Issue 1) but unambiguous in
context: every prose gloss ("2 TOTAL passes", "at most ONE re-patch pass") and every operative
guard pins the bound to 2. The set-membership notation does not drive any branch; the `k+1 > 2`
and `k < 2` integer comparisons do.

---

## Adversarial Deep-Dive: Full-Set Re-Validation & Guard Sufficiency

**Probe — does the per-iteration state actually feed the guards, or is it decorative?** Each of the
5 recorded columns maps to a live guard input:
- PASS-set + regression-set → regression check (1542): "any patchable item that PASSED at pass `k`
  is FAILing at pass `k+1`" requires the prior PASS-set to compare against.
- `|F_k|` + `|F_{k-1}|` → monotonicity check (1543): `|F_{k+1}| >= |F_k|`.
- `k` → hard-cap (1544): `k+1 > 2`.
No recorded column is unused, and no guard input is missing from the recorded state. Sufficient.

**Probe — full-set vs subset confusion.** The residual PatchChecklist that Stage 9 re-patches is
scoped to `F_k` (a subset — only the failing items get re-patched), BUT the `F_k` *computation* at
Stage 10 re-runs the FULL 2N set (1540). These are two distinct scopes and the SKILL keeps them
distinct: patch-scope = `F_k` subset; validation-scope = full 2N. This is exactly what makes
regressions in previously-PASS items detectable, and it is internally consistent (a subset re-read
could not detect a regression in an item outside `F_k`). No contradiction.

**Probe — synthetic-dnsp exclusion vs monotonicity (OQ-PRE-1).** `F_k` excludes
`source: "synthetic-dnsp"` (1540, 1349). A persistent synthetic with the same `dedup_key` is a
DEDUP case, not a regression, so it cannot spuriously inflate `|F_k|` and trip the monotonicity
halt. Consistent with the cross-cycle DM-003 rule reused at 1349. The synthetic still forces human
review via Stage 8 (1390). Self-consistent.

---

## Issues Found

All five lens criteria PASS. The adversarial sweep nonetheless surfaced the following MINOR
internal-consistency nits. None alters the cap, the guards, or any branch outcome; none is a FAIL.
REPORT-ONLY — nothing modified.

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | SKILL.md:1536 | `k ∈ {2}` is loose set-membership notation for what is really "the cap on the pass index is 2 / k ≤ 2". A literal reading of "k is the singleton set {2}" would exclude pass 1 (`k=1`), yet pass 1 is explicitly the initial pass (1538). The prose glosses ("2 TOTAL passes", "at most ONE re-patch pass") and the integer guards (`k+1 > 2`, `k < 2`) all resolve the intent correctly, so this is cosmetic. | Optionally rephrase to `k ≤ 2` or "k caps at 2" for notational precision. No behavioral change. |
| 2 | MINOR | SKILL.md:1532-1533 (iteration table) | The worked example shows only the strict-shrink→cap path. It does not illustrate the monotonicity-halt row (e.g. `|F_k|` non-shrinking) or the regression-halt row, so a reader cannot see the halt-string emission modeled in the same table. Sufficiency for the guards is met by the column schema (1526), not by the example rows, so this is presentational completeness only. | Optionally add a 2nd example table or a halt-row to demonstrate `[HALT-MONOTONICITY]` / regression emission. Not required for correctness. |
| 3 | MINOR | SKILL.md:1544-1545 | Redundant double-guard: the hard-cap (`k+1 > 2`) and the proceed clause (`k < 2`) both independently prevent a 3rd pass. This is defensive-redundant (safe), but a reader could mistake one for dead code. The 4-step ordering ("EXIT on first match") means the proceed clause is only reached when hard-cap did NOT fire, so both are live on different transitions. | None required — redundancy is intentional belt-and-suspenders. Optionally add a one-line note that both guards are deliberately retained. |
| 4 | MINOR | SKILL.md:1546 / 1533 | Terminology: the table row 2 says "finalize (cap k=2)" while `|F_2|`=1 (nonzero residual). The STOP-outcome prose (1546) lists "capped at `k=2`" as distinct from "clean: `F_k` empty". The example therefore depicts a *capped-with-residual* finalize, which is correct, but the single word "finalize" could read as "clean". | Optionally annotate the example row as "cap-with-residual finalize (1 UNRESOLVED logged)" to distinguish from a clean finalize. Cosmetic. |
| 5 | MINOR (cross-file note) | phase-5-output-summary.md:14 vs SKILL.md:1529 | The summary says the iteration table is "appended to the Stage-10 `## Verification Results` section". The SKILL places the `## P2 Bounded-Loop Iterations` table at 1529 — physically *before* the `## Verification Results` example block? No: 1526 explicitly says "append a per-iteration loop-state table to this `## Verification Results` section", and 1529's heading is a sub-block under it. Verified consistent; flagging only because the summary's "appended to" wording could be read as a sibling section rather than a nested append. | None — verified consistent on re-read. Documented for traceability. |

**Internal-consistency claims independently re-verified (no defect):**
- "`does NOT loop` count is now 0" (summary:16) — `grep "does NOT loop"` over SKILL.md returns **zero** matches. Confirmed: the stale no-loop gate was fully removed and merge-step-1a (1349) now references the real P2 loop's `F_k` synthetic exclusion. Consistent.
- Stage 10.5 fence (1552, 1554) names the P2 loop convergence ("clean | capped at `k=2` | monotonicity-or-regression halt") with the same three terminal labels as the Stage-10 gate (1546). Cross-referenced labels match exactly.

---

## Summary

- Checks passed: 5 / 5 (all five lens criteria)
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 5 (cosmetic/presentational; none alters cap, guards, wiring, or branch outcomes)
- Issues fixed in-place: 0 (REPORT-ONLY — fix_authorization: false)

## Actions Taken

None. fix_authorization: false — nothing in the SKILL was modified. All findings are advisory.

## Confidence Gate

- **Confidence:** Verified: 5/5 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 3 | Grep: 0 | Glob: 0 | Bash: 2 (grep-via-bash for cap/loop/short-circuit tokens + test refs); tavily/web: 0 (no external claim — purely local source verification per Principle 6)
- Tool-call-to-check ratio: 5 tool calls for 5 checks (≥ 1:1) — not suspect.
- Every VERIFIED item cites specific SKILL.md line numbers and quoted text confirmed by Read + grep.

## Recommendations

- Verdict is PASS — green light for the P2 cap-arithmetic / internal-consistency lens.
- The 5 MINOR nits are optional polish (notation tightening at 1536; richer iteration-table
  examples at 1532-1533; a one-line note on the deliberate double-guard at 1544-1545). None blocks
  proceeding. They may be batched into a future cosmetic pass or left as-is.

## QA Complete
