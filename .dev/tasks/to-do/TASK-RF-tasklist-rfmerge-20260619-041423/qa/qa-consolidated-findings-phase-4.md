# Phase 4 (P3) — Consolidated QA Findings (Cycle 1)

**Generated:** 2026-06-19 (Step 4.G8). Six lens reports consolidated, deduplicated.
(Several lens agents noted the shared QA report paths held stale prior-phase content and either
overwrote or returned inline; verdicts below are taken from the authoritative agent return messages.)

## Per-lens verdicts

| Lens | Agent | Verdict | Issues |
|------|-------|---------|--------|
| DM-003 contract-reuse fidelity | rf-qa | PASS | 0 (byte-exact em-dash + retry-1 + 7 fields all verified) |
| branch-logic / internal-consistency | rf-qa | **FAIL** | 1 CRITICAL, 1 IMPORTANT, 2 MINOR |
| evidence-quality / test-coverage | rf-qa | **FAIL** | 3 IMPORTANT, 3 MINOR (test-only) |
| silent-pass prevention | rf-qa-qualitative | **FAIL** | 3 CRITICAL, 3 IMPORTANT, 1 MINOR |
| no-fork / map-not-copy | rf-qa-qualitative | PASS | 1 MINOR (same dangling F_k ref) |
| domain-accuracy | rf-qa-qualitative | PASS | 0 (2 observations) |

## CONSOLIDATED VERDICT: **FAIL**

Root cause (flagged by 3 lenses): Phase 4 over-imported task-builder LOOPING/gap-fill prose and
forward-referenced Phase-5 machinery (the P2 bounded loop, `F_k`, "see Stage 10") that does not exist
in this single-pass generator yet — Stage 10 currently says "the skill does NOT loop." Plus the
Stage-7 contract table + Gate Behavior still describe the old binary "zero agent failures" gate, the
some-vs-zero gate is non-exhaustive (no all-succeeded branch), and the non-patchable synthetic is not
excluded from the Stage-9 patch executor.

## Deduplicated issue list

| ID | Severity | Lens(es) | Location | Issue | Required fix |
|----|----------|----------|----------|-------|--------------|
| C4-01 | CRITICAL | branch-logic #1, silent-pass #1, no-fork MINOR, domain obs | SKILL.md merge step 1a (~:1349) | Dangling/self-contradictory forward-reference: cites "the P2 bounded loop, which excludes synthetic-dnsp from its patchable monotonicity failing-set `F_k` (see Stage 10)" — but no P2 loop / `F_k` / monotonicity exists (grep: sole occurrence); Stage 10 says "the skill does NOT loop." | Remove the premature P2/`F_k`/"see Stage 10" reference from Phase 4. Make the synthetic's nature self-contained: non-patchable (records an agent failure, not a fixable defect), treated FAIL-until-manual-review; if a future re-validation pass is added, a persistent synthetic with the same `dedup_key` is a DEDUP case (DM-003 cross-cycle rule), NOT a regression. The concrete P2 `F_k` exclusion is added in Phase 5 (where the loop lands). |
| C4-02 | CRITICAL | silent-pass #2 | SKILL.md contract table (~:1601) + Gate Behavior (~:1609) | Stage-7 contract row still reads "zero agent failures"; Gate Behavior lists agent-completion as a blocking structural gate that would abort the ≥1-failure-with-sibling-success case the new gate is meant to PROCEED through. | Update row :1601 to the some-vs-zero branch ("≥1 success → synthesize synthetic-dnsp + proceed; zero success → escalate"); add a Gate Behavior clause noting Stage 7's agent-completion gate follows the some-vs-zero branch (a single failed-then-synthesized agent does not abort when ≥1 sibling succeeded). |
| C4-03 | CRITICAL | silent-pass #3 | SKILL.md short-circuit guard (~:1389) | Guard cites "the gap-fill / patch cycle MUST NOT auto-resolve it" — no gap-fill cycle exists in this generator (only the closed-vocab tokens). | Reword to drop "gap-fill": the synthetic is recorded for manual review and the Stage-9 patch executor MUST NOT auto-resolve/auto-patch it. |
| C4-04 | IMPORTANT | silent-pass #4/#6 | SKILL.md Stage 8 PatchChecklist (~:1424) / Stage 9 (~:1475-1480) | The non-patchable synthetic (only `recommendation: Manual review required`, no `Exact fix`) would be fed to Stage 9 `sc:task --compliance strict` which "addresses all checklist items" — but it has no actionable edit. | Add a note: synthetic-dnsp findings are recorded in ValidationReport.md under a manual-review section and are EXCLUDED from the actionable PatchChecklist items (Stage 9 does not auto-patch them); they remain a human-review gate. |
| C4-05 | IMPORTANT | silent-pass #5 | SKILL.md zero-success branch (~:1370) | Routes to "a conceptual analogue of R-122 Path A ... not a named path that exists in this generator" — undefined terminal behavior for the worst case. | Point the zero-success branch at the concrete existing terminal behavior: the original gate's "report error" path (the generator reports the validation error / halts rather than returning a clean bundle). Keep the R-122 analogue as an explanatory aside, not the operative instruction. |
| C4-06 | IMPORTANT | branch-logic #2 | SKILL.md some-vs-zero gate (~:1367) | Non-exhaustive: enumerates "≥1 succ AND ≥1 fail" and "ZERO succ" but the reachable all-succeeded (0 failed) outcome has no named branch (SoT R-122 has three mutually-exclusive paths). | Add the all-succeeded branch: all agents succeeded (0 failed) → normal merge, NO synthetic, proceed (the Path C analogue). |
| C4-07 | IMPORTANT | evidence-quality #1 | test_tasklist_cli.py P3 test | `assert "evidence" in text` is vacuous — the token appears ~20× (e.g. `evidence.md`); deleting the DM-003 `evidence` field leaves the test green. | Make it specific: assert the evidence field in its DM-003 context, e.g. assert the `<!-- evidence-absence: spawn-log-unavailable -->` stub string (P3-exclusive). |
| C4-08 | IMPORTANT | evidence-quality #2 | test_tasklist_cli.py P3 test | `found_n_times` value not pinned (only the name). | Assert the default value, e.g. `assert "found_n_times`: `1`" in text` (match the actual authored phrasing). |
| C4-09 | IMPORTANT | evidence-quality #3 | test_tasklist_cli.py P3 tests | Step 4.3 short-circuit guard (SKILL.md:1389) has NO test despite being the silent-pass-prevention mechanism. | Add a test asserting the short-circuit guard markers (synthetic IS a finding; short-circuit MUST NOT fire when synthetic present; FAIL-until-manual-review). |
| C4-10 | MINOR | evidence-quality #4-6, silent-pass #7 | test + SKILL.md | strictly-additive / HIGH-non-overridable / no-sideband unpinned by test; synthesis (step 1a) described before the gate that authorizes it (read-order). | Add light asserts for "strictly additive" / "non-overridable" / "NO sideband"; read-order is cosmetic — optionally add a forward-pointer from step 1a to the gate. |

## Fix scope for Step 4.G9

- SKILL.md C4-01..C4-06: make P3 self-contained for the single-pass generator (drop premature P2/`F_k`/Stage-10
  refs and the "gap-fill" term; update the Stage-7 contract row + Gate Behavior; add the all-succeeded branch;
  concrete zero-success terminal; exclude the non-patchable synthetic from the actionable PatchChecklist). All
  within P3 scope; NO new looping machinery (that is Phase 5). The DM-003 emission contract (fields/values/
  em-dash/retry-1) is already correct (4.G2 PASS) — DO NOT change it.
- Test hardening C4-07..C4-10 in `tests/tasklist/test_tasklist_cli.py` `TestP3DnspSyntheticFindings`
  (de-vacuum the evidence assert; pin found_n_times; add a short-circuit-guard test; light additive/HIGH asserts).
- Phase-5 carry-forward: the concrete P2 `F_k`-excludes-synthetic-dnsp rule + its test land in Phase 5 (OQ-PRE-1).
- After fixes: `make sync-dev` + `make verify-sync` + `uv run pytest tests/tasklist/ tests/skills/test_task_builder_merge.py -v`.
- IMPORTANT: keep test asserts byte-consistent with the post-fix SKILL.md prose (re-read before asserting).
