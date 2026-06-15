# QA Report — task-qualitative (operational-correctness, scoped graft re-verify)

**Topic:** Differential Backtest/Eval Harness — surgical graft of Step 4.4 (E2 digit-heading caveat), Step 4.7b (Waiver re-green runner), Step 4.8 / OQ-3 (waiver excluded from catch_rate denominator)
**Date:** 2026-06-11
**Phase:** task-qualitative
**Lens:** operational-correctness (CHANGED/grafted items ONLY)
**Fix cycle:** N/A (report-only; fix_authorization: false)

---

## Overall Verdict: PASS

The graft is operationally correct. Every load-bearing claim in the three grafted surfaces was
verified against live source (`git show 10723863:...gates.py`), the parent-commit chain
(`git rev-parse`), and the RELEASE-SPEC at the named section/line level. No fabricated enum
tokens, no internal contradictions, no fixture trap, and the "no OLD=MISS by design" framing is
sound. One MINOR observation (non-blocking, advisory) is recorded.

---

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | E2 digit-heading caveat accurate vs live source | none | PASS | `git show 10723863:src/superclaude/cli/prd/gates.py` L197-228: regex `r"(?:^\|\n)\s*#{1,4}\s+.*Phase\s+(\d+)"` (digit-only capture) + `int(m.group(1)) >= 2`. Caveat is ACCURATE, not fabricated. |
| 2 | OLD=MISS fixture prescription would go GREEN (not RED) | none | PASS | Traced control flow: empty `later_phases` → `return True` (no halt) → OLD=MISS test RED. Caveat's "concrete digit ≥2 completion heading, no parallel kw in its body" forces the failure-string return. Correct. |
| 3 | E2 mechanism matches fix-commit semantics | none | PASS | `e97aa4fd` msg: "exempt sequential completion phase from parallel-instructions gate (#154)". Pre-fix over-strict HALT on sequential final phase = exactly the OLD=MISS observable. |
| 4 | Waiver spec grounding (FR-12, NFR-4, §4.5, §5.4, §8.3) | none | PASS | All exist: FR-12 L225; NFR-4 L526; `waiver_status` enum none\|latched one-way L315/L432; §5.4 truth table L392-411; §8.3 "Waiver re-green attempt" row L580. |
| 5 | No fabricated enum tokens | none | PASS | `success_with_hardening_blocker` / `success_with_hardening_advisory` appear VERBATIM in §5.4 L411. Step 4.7b's assertion is faithful, not invented. |
| 6 | Step 4.7b assertion (latched → {blocked,advisory}; no upgrade) matches §5.4 | none | PASS | §5.4 rows 3 & 5 (L396, L398): `waiver_status=latched` → `blocked` or `advisory`; all rows "Downstream Override Allowed? = No"; L411 forbids upgrade to pass/success. |
| 7 | Impl-ref target = correct §4.7 validator surface | none | PASS | §4.7 L340 names `refs/hardening-output-contract.md` as the "Verdict aggregation contract" surface (truth table + waiver latch). NOT pipeline-hardening-closure.md (L270/L324 = protocol-mode ref, distinct surface). Target is correct. |
| 8 | catch_rate coherence — total_escapes==5 with waiver excluded | none | PASS | §3.1 matrix L253-257 = exactly E1-E5 (5 escapes). Waiver is a cross-cutting FR-12/NFR-4 invariant, NOT a 6th escape. Excluding it keeps `total_escapes==5` coherent. |
| 9 | No contradiction across 4.7b / 4.8 / 3.2 / OQ-3 | none | PASS | All four say identically: waiver backs NFR-4 (not NFR-1), excluded from `CatchRateReport`, denominator stays 5, single `requires_impl_ref`-guarded test, read-as-COMPLETE. Self-consistent. |
| 10 | "No OLD=MISS by design" soundness | none | PASS | Waiver is a forward verdict-state-machine invariant of the impl's aggregator (impl-only surface), not a regression of pre-fix code. No commit to replay → no unguarded OLD=MISS half is correct. |
| 11 | Replay-table SHA parent chain internal consistency | none | PASS | `git rev-parse e97aa4fd^`=`10723863` (E2 parent); `eb9a2633^`=`e97aa4fd` (E3 parent). All 7 SHAs resolve. Note: E2 fix `e97aa4fd` IS E3's parent `e97aa4fd` — chained but distinct roles, correctly labeled. |
| 12 | Skip-guard discipline for waiver test | none | PASS | Step 4.7b mandates `requires_impl_ref(...)` (NOT importorskip/xfail/try-except) — matches Key Constraint "NEVER importorskip / NEVER xfail" and repo convention. |
| 13 | Distinct nodeid vs impl suite | none | PASS | `test_waiver_latch_one_way_blocks_downstream_regreen` is distinct from impl's `test_waiver_latch_one_way` (§8.1 L557) — collision-boundary-safe. |

(axis column: this review is operationally scoped to grafted items; all checks PASSED so `none`
is the correct sentinel per task-qualitative canonical annotation rules. No AX-1..AX-5 finding
fired. AX-1 Drift is ACTIVE — BUILD_REQUEST.GOAL verbatim is reproduced at task R-001 L109.)

## Summary
- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (advisory, non-blocking — see below)
- Issues fixed in-place: 0 (fix_authorization: false — report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | MINOR | Step 4.4 caveat clause "preceded by at least one earlier phase whose body DOES contain a parallel keyword" | This clause is OPERATIONALLY CORRECT but slightly STRONGER than strictly necessary for OLD=MISS to fire. The pre-fix gate returns the failure string on the FIRST digit-≥2 phase whose body lacks a parallel keyword, regardless of whether an earlier parallel-keyword phase exists. The earlier-parallel-phase requirement makes the fixture a more realistic/representative artifact (it proves the gate's discrimination, not just absence) and prevents the fixture from reading as a degenerate all-empty case — so it is a defensible tightening, not a defect. No change required; recorded so a fix agent does NOT mistake the extra clause for a contradiction. | None required. Optionally annotate the clause as "representativeness, not a hard precondition for the HALT" if future readers question it. |

## Detailed Verification Notes

### Step 4.4 — E2 digit-heading caveat (the most falsifiable claim)
Live source at parent `10723863` (`git show 10723863:src/superclaude/cli/prd/gates.py`, function
`_check_parallel_instructions` L197-228):
- Regex: `r"(?:^|\n)\s*#{1,4}\s+.*Phase\s+(\d+)"` with `re.IGNORECASE` — captures DIGITS ONLY via
  `(\d+)`.
- `later_phases = [m for m in phase_sections if int(m.group(1)) >= 2]` — the exact `int(group)` +
  `>= 2` the caveat names.
- `if not later_phases: return True` — a literal "Phase N: …" heading never matches → no later
  phases → returns True (no halt) → an OLD=MISS test asserting a halt would go RED. This is the
  EXACT trap the caveat warns about. CONFIRMED ACCURATE — not a fabricated hazard.
- The HALT path returns `f"Phase {phase_num} missing parallel execution instructions ..."` only
  when a collected digit-≥2 phase's body has none of `parallel|concurrent|simultaneously|batch`.
  The caveat's prescription (concrete digit ≥2 completion heading, no parallel keyword in its
  body) is precisely what produces this return. CONFIRMED.
- Fix commit `e97aa4fd` ("exempt sequential completion phase from parallel-instructions gate")
  corroborates the pre-fix over-strict-HALT mechanism. CONFIRMED.

### Step 4.7b — Waiver re-green runner
- FR-12 (L225-231): one-way `waiver_status` latch none→latched forcing verdict ∈ {blocked,
  advisory}; no downstream task-builder/sc:reflect/adversarial may upgrade to pass/success.
- §5.4 truth table (L392-411): rows 3 (latched + waived mandatory → blocked) and 5 (latched +
  substituted + no FAIL → advisory). All rows "Override Allowed? = No". L411 renders downstream
  success as `success_with_hardening_blocker` / `success_with_hardening_advisory`, never plain
  `success`. The enum tokens in Step 4.7b are VERBATIM from the spec — no fabrication.
- §8.3 (L580): "Waiver re-green attempt | Waive H1, then run downstream reflect/adversarial |
  Verdict stays blocked/advisory; never pass" — the 6th-row scenario the runner maps to.
- Impl-ref `hardening-output-contract.md`: §4.7 L340 names it as the verdict-aggregation-contract
  validator surface. CORRECT target (not pipeline-hardening-closure.md, which is the protocol-mode
  ref per L270/L324).
- "No OLD=MISS by design": SOUND. The waiver invariant is a forward state-machine property of the
  impl's aggregator (which only exists on the impl surface), not a pre-fix-parent regression.
  There is no historical commit where the aggregator re-greened a latched verdict to replay
  against. A single `requires_impl_ref`-guarded test is the correct and complete shape.

### Step 4.8 / OQ-3 — Waiver excluded from the 5-escape denominator
- §3.1 escape matrix (L253-257) enumerates EXACTLY E1-E5. The waiver scenario is a cross-cutting
  FR-12/NFR-4 invariant, categorically not a 6th product escape. Excluding it from
  `catch_rate`/`backtest_status` (NFR-1) and keeping `total_escapes==5` is COHERENT.
- Cross-item consistency: Step 4.7b, Step 4.8, Step 3.2 (report model `total_escapes`), and OQ-3
  all state the SAME exclusion rationale (backs NFR-4 not NFR-1; not fed to CatchRateReport;
  denominator stays 5). No operational contradiction.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- This was a SCOPED operational re-verify of grafted items only; no inherited structural verdict
  block was provided in the spawn prompt. No structural re-checks were skipped on the basis of
  reliance — all claims were independently re-verified.

**(b) Independent semantic checks (≥1 required, INV-019):**
- E2 digit-only regex + `int(group)>=2` — verified by `git show 10723863:src/superclaude/cli/prd/gates.py` L197-228 (read the actual pre-fix function body, traced control flow).
- E2 fixture-would-go-GREEN — verified by manual control-flow trace of the `if not later_phases: return True` branch vs the failure-string return branch.
- E2 mechanism — verified by `git log --oneline -1 e97aa4fd` fix-commit message.
- Enum-token non-fabrication — verified by `grep success_with_hardening` → §5.4 L411 (verbatim match).
- §5.4 latch→verdict mapping — verified by `sed -n 390,412p` of the spec truth table.
- Impl-ref target correctness — verified by `grep hardening-output-contract / §4.7` → L340 vs L270/L324 disambiguation.
- total_escapes==5 coherence — verified by `sed -n 249,258p` of §3.1 (exactly E1-E5).
- SHA chain — verified by `git rev-parse e97aa4fd^ eb9a2633^` (parent-of relations hold).

**Confidence-Gate fields:**
- Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 4 (task file pages) | Grep: 4 (task + spec) | Glob: 0 | Bash: 5 (git show / rev-parse / log / spec sed). Total tool calls (Read+Grep+Bash) = 13 ≥ 13 checks. Adequate.
- Self-audit answers: (1) 8 distinct factual claims independently verified against live source/spec. (2) Files read: task file, `gates.py@10723863`, RELEASE-SPEC §3.1/§4.7/§5.4/§8.3/FR-12/NFR-4. (3) 0 issues at CRITICAL/IMPORTANT is trustworthy because each grafted claim was re-derived from primary source, not the task's own prose — the one most-falsifiable claim (digit-only regex) was confirmed at the byte level. (4) No web research performed; all sources local.

## Recommendations
- PROCEED. The graft is operationally sound. No blocking issues.
- The single MINOR (item #1) is advisory only — the "earlier parallel phase" clause is a
  representativeness tightening, not a hard precondition; no fix agent action is needed unless a
  future reviewer flags it as over-specified.

## QA Complete
