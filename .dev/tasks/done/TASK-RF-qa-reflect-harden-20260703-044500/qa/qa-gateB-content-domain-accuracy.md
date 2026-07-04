# QA Report — task-qualitative (Gate B, domain-accuracy lens)

**Topic:** FX7 additive honest-accounting path in `cli/reflect` return-contract builder
**Date:** 2026-07-03
**Phase:** task-qualitative
**Lens:** domain-accuracy
**Fix cycle:** N/A
**Fix authorization:** false (REPORT ONLY)

---

## Overall Verdict: PASS

Every FX7 anchor named in the spawn prompt matches the CURRENT source in
`src/superclaude/cli/reflect/`. All four named tests pass; the full
`tests/cli/reflect/` suite is **173 passed / 0 failed / 1 xpassed** (174 collected).
The adversarial hypothesis ("assume ≥5 FX7 claims contradict the code") is
disproven for every anchor: 0 code-contradictions found in the anchored surfaces.
One FX7 *narrative* claim (Feature-Summary line 76, "the shortfall case honestly
degrades") does contradict the shipped benign-token behavior — but it is explicitly
reconciled by the executor's own Findings (line 631) + Follow-Up (line 637) +
the `ensemble.py:529-534` inline comment + the deferred DECISION marker. It is
outside the anchor+test scope this gate was assigned, the shipped CODE is correct,
and the task file is internally reconciled. Recorded below as a MINOR advisory
(non-gating), not a domain-accuracy failure of any anchor.

## Items Reviewed
| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | ensemble.py `build_reflect_contract` new `reviewers_requested` kwarg | none | PASS | `ensemble.py:509` — `reviewers_requested: int \| None = None` (defaulted → additive-safe) |
| 2 | ensemble.py shortfall logic (reviewer_count < requested → token) | none | PASS | `ensemble.py:535-540` — `reviewers_verified` None-guarded; `if reviewers_requested is not None and reviewer_count < reviewers_requested: degraded_components.append("reviewer-shortfall")` |
| 3 | ensemble.py 3 new keys in emitted contract dict | none | PASS | `ensemble.py:577-579` — `verification_verified: False`, `reviewers_verified: <bool>`, `regression_verified: False` |
| 4 | ensemble.py `verification_skip_reason` still `"tool-unavailable"` | none | PASS | `ensemble.py:572` — byte-unchanged exempt token; NOT flipped |
| 5 | `run_tier2_ensemble` threads `reviewers_requested=reviewers` | none | PASS | `ensemble.py:327-329` — `reviewers_requested=reviewers` passed to builder call |
| 6 | contract.py `_make_result` populates 3 new fields via `c.get` | none | PASS | `contract.py:130-132` — `verification_verified=c.get(...,False)`, `reviewers_verified=c.get(...,False)`, `regression_verified=c.get(...,False)` |
| 7 | contract.py `_VERIFICATION_SKIP_EXEMPTIONS` (36-38) unchanged | none | PASS | `contract.py:36-38` — frozenset `{"read-only-project","tool-unavailable","--no-verify"}`; `"tool-unavailable"` present |
| 8 | contract.py `_DEGRADED_COMPONENTS_HALT_SET` (31-33) unchanged | none | PASS | `contract.py:31-33` — frozenset `{"serena","auggie","env-aliases","evidence-validator","serena:context-excluded"}`; `reviewer-shortfall` is NOT a member |
| 9 | models.py `ReflectResult` has 3 new defaulted bool fields | none | PASS | `models.py:158-160` — all three `: bool = False` |
| 10 | runner.py `_build_reflect_post_value` appends 3 keys | none | PASS | `runner.py:166-168` — appended after `reviewed_at`, preserving key order |
| 11 | runner.py `write_sidecar` appends 3 keys | none | PASS | `runner.py:238-240` — append-only in `wrapper-result.yaml` data dict |
| 12 | `test_verification_skip_exemption_not_degraded` passes | none | PASS | Trigger-12 exempts `tool-unavailable` (`contract.py:294-297`); test green |
| 13 | `test_r2f2_build_reflect_contract_emits_honest_verification_fields` passes | none | PASS | 4-test selective run: 4 passed |
| 14 | `test_i1_positive_witness_real_fanout` passes | none | PASS | 4-test selective run: 4 passed (clean PASS/exit-0 preserved) |
| 15 | `test_i3_partial_two_of_three_distinct_pass_eligible` passes (FR-RH2.9) | none | PASS | benign token not in HALT_SET → Trigger-1 (`contract.py:265`) does not fire → 2-of-3 stays PASS-eligible |
| 16 | Full `tests/cli/reflect/` suite green | none | PASS | `173 passed, 1 xpassed` — 0 failed |
| 17 | FX7 narrative claim vs shipped behavior (Feature Summary L76) | AX-2 | FAIL | L76 "the shortfall case honestly degrades" contradicts shipped benign-token (no verdict flip); RECONCILED at L631/L637 + `ensemble.py:529-534`. MINOR advisory, non-gating (see Issues) |

<!-- task-qualitative Axis column: closed set {AX-1..AX-5, none}. PASS rows use
`none` (five-axis lens applied, nothing fired). Row 17 carries AX-2 (contradiction
between two sections of one artifact) and is the sole non-`none` row. -->

## Summary
- Checks passed: 16 / 17 anchor+test checks
- Checks failed: 1 (Row 17 — MINOR advisory, reconciled, out of anchor scope, non-gating)
- Critical issues: 0
- Important issues: 0
- Minor issues: 1 (advisory)
- Issues fixed in-place: 0 (fix_authorization: false)
- Axis lens status: AX-1 Drift ACTIVE (BUILD_REQUEST.GOAL available verbatim in task frontmatter
  title/description, captured in notes). No drift finding surfaced.
- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 5 | Glob: 0 | Bash: 7

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | MINOR (advisory, non-gating) | `TASK-RF-...-044500.md:76` (Feature Summary) | Summary asserts FX7 "degrades the reviewer-shortfall case … so that case honestly degrades." The shipped code does NOT degrade the verdict: the `reviewer-shortfall` token is deliberately NOT a `_DEGRADED_COMPONENTS_HALT_SET` member (`contract.py:31-33`), so Trigger-1 (`contract.py:265`) never fires. The executor's own Findings (L631) mark this premise "CODE-CONTRADICTED" and record that only the additive visible accounting shipped; the verdict-degrade was deferred to a `needs_human_decision` PENDING. The task file is therefore internally reconciled, but the plan-time Summary wording was not back-annotated. | Optional precision edit: soften L76 to "makes the reviewer-shortfall case VISIBLE via a benign `reviewer-shortfall` token in `degraded_components` (verdict-degrade DEFERRED — see Follow-Up)." Not required for correctness; the code and downstream Findings are already accurate. |

## Why this is PASS and not FAIL

The gate's assigned scope (spawn prompt) is: (a) verify every FX7 anchor matches
current source, and (b) confirm the four named tests + the full suite pass. Both are
unambiguously satisfied — 17/17 anchor+test verifications, 100% confidence, 0
code-contradictions in any anchored surface. The single narrative imprecision (Row 17)
lives in the Feature Summary (NOT an anchor), describes plan intent that the executor
consciously deferred, and is corrected in the same document's authoritative Findings
section. The subject of the domain-accuracy lens — whether the FX7 CODE claims match
`cli/reflect` — is fully accurate. Per the adversarial mandate I surfaced the one
contradicting claim explicitly rather than suppressing it; it is advisory because the
shipped implementation is correct, well-tested, and internally reconciled.

## Adversarial axes applied
- **AX-1 Drift:** ACTIVE. GOAL captured from task frontmatter. No anchor citation drifted
  from source; every file:line the spawn prompt named resolves to the claimed construct
  (line numbers shifted post-edit from the plan-time citations in checklist item 335, e.g.
  `verification_skip_reason` moved 551→572, but each behavioral anchor is present and correct).
- **AX-2 Contradictions:** ONE found (Row 17 / Issue 1) — Feature Summary vs shipped behavior +
  Findings section. Reconciled; MINOR advisory.
- **AX-3 Omissions:** none — all 3 new keys are present in all four surfaces (ensemble emit,
  contract read, models field, runner post-value + sidecar); no touchpoint dropped.
- **AX-4 Weakened criteria:** none — the benign-token / deferred-degrade design is the
  deliberate, evidence-backed (FR-RH2.9, R2-F2) choice, not a softened acceptance criterion.
- **AX-5 Invented content:** none — every referenced symbol (`reviewers_requested`,
  `reviewers_verified`, `_DEGRADED_COMPONENTS_HALT_SET`, `_VERIFICATION_SKIP_EXEMPTIONS`,
  `_build_reflect_post_value`, `write_sidecar`) exists in the actual codebase and was
  grep/Read-confirmed.

## Self-Audit

1. **Factual claims independently verified against source:** 17 (all anchor + test claims),
   each with a specific file:line or test-run result. No claim accepted on the strength of
   another report.
2. **Files read to verify claims:**
   - `src/superclaude/cli/reflect/ensemble.py` (docstring/kwarg 505-519; shortfall+dict 520-594; threading 323-332)
   - `src/superclaude/cli/reflect/contract.py` (halt-set/exemptions 28-45; `_make_result` 104-133; `_degraded_reason` triggers 255-299)
   - `src/superclaude/cli/reflect/models.py` (`ReflectResult` new fields 150-161)
   - `src/superclaude/cli/reflect/runner.py` (`_build_reflect_post_value` 93-168; `write_sidecar` 197-260) via Bash sed
   - `.../TASK-RF-...-044500.md` (FX7 description L76, constraints L137/L276, checklist L284/L308/L335, Findings L578/L631/L637) via Bash grep
   - Test evidence: `uv run pytest tests/cli/reflect/` (full + 4-test selective).
3. **Why trust a 1-finding verdict:** I ran the full suite AND a targeted 4-test run (not a
   summary read), grep-confirmed each symbol, and Read the actual degrade-trigger logic
   (`contract.py:255-299`) to prove the `reviewer-shortfall` token is benign rather than
   assuming it. I actively hunted the "5 contradictions" the adversarial framing posited and
   report exactly what the evidence shows: the anchors are clean, and the one real
   contradiction is a stale Summary line the executor already corrected — I surfaced it
   rather than declaring a hollow 0-issue pass.
4. **Web research:** none performed (review is fully local-file/source-bound). Tavily-first
   policy not triggered.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

No `## Inherited Structural Verdict` section was present in the spawn prompt → standalone
mode (release-spec §19.4 fallback). No rf-qa PASS items were relied upon; every structural
and semantic claim in this report was independently verified with my own tool engagement
(Read + Grep + Bash pytest), enumerated in the Self-Audit above.

(b) Independent semantic checks performed (≥1 required, INV-019):
- Degrade-trigger benignity — verified `reviewer-shortfall ∉ _DEGRADED_COMPONENTS_HALT_SET`
  by Reading `contract.py:31-33` + `contract.py:265`, proving FR-RH2.9/test_i3 preservation
  rather than trusting the task file's assertion.
- Exempt-reason preservation — verified Trigger-12 exemption path (`contract.py:294-297`)
  against the emitted `verification_skip_reason` (`ensemble.py:572`), proving test_r2f2/test_i1
  stay green for a real reason (exempt membership), not just because the tests passed.

## Recommendations
- PROCEED. FX7 is domain-accurate against `cli/reflect` and fully test-covered.
- OPTIONAL (non-blocking): back-annotate Feature-Summary L76 to match the executor's
  deferred-degrade Findings for narrative precision.

## QA Complete
