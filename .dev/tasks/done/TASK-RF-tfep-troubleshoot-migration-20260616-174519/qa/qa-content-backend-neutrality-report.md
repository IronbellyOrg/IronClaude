# QA Report — Backend-Neutrality Content Lens (TFEP Phase 2)

**Topic:** TFEP forensic→troubleshoot backend rename — Phase 2 bare-term rename neutrality
**Date:** 2026-06-16
**Phase:** doc-qualitative (backend-neutrality content lens)
**Fix cycle:** N/A (REPORT ONLY — fix_authorization: false)
**Target:** `src/superclaude/skills/sc-task-protocol/SKILL.md` §4.5 (lines 133–263)

---

## Overall Verdict: FAIL

The Phase-2-renamed prose does NOT yet read backend-neutrally. The §4.5
declaration at line 137 promises that "swapping the backend changes only this
declaration and the invocation string," but the surrounding renamed prose still
bakes in a **forensic-specific pipeline shape** — specifically an internally
*phased*, *adversarial-debate-driven*, *adjudicated* RCA pipeline. A reader who
swapped in a backend without those internal stages (e.g. a single-pass Tier-1
`/sc:troubleshoot` triage) could NOT honour the prose by editing only the
declaration + invocation string. The neutrality contract is therefore violated
by its own body. 4 distinct leaks + 1 contradiction found (adversarial floor of
5 met).

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Declaration (L137) is internally honest about what a swap touches | FAIL | Promises "only this declaration and the invocation string"; body contradicts (L215, L178–179, L229) |
| 2 | Gradient header (L174) "diagnostic-backend escalation" reads neutral | PASS | Bare term is backend-agnostic |
| 3 | Step 3 heading (L207) "Invoke diagnostic escalation" reads neutral | PASS | No backend assumption |
| 4 | "diagnostic depth" (L208) reads neutral | PASS | "depth" is generic; maps to any tier/depth knob |
| 5 | L215 "runs autonomously through all its phases" reads neutral | FAIL | "through all its phases" asserts an internally phased backend |
| 6 | Step 4 heading (L217) "Consume diagnostic results" reads neutral | PASS | Generic |
| 7 | Escalation-gradient bullets (L178–179) read neutral | FAIL | "adversarial debate" / "adversarial outcome (no winner/tie)" bake in a debate-pipeline shape |
| 8 | Remediation heading label (L229) "(Adjudicated)" reads neutral | FAIL | "Adjudicated" presumes an adjudication/debate stage in the backend |
| 9 | "Diagnostic artifacts" (L252) label reads neutral | PASS | Generic |
| 10 | Prohibition rule (L144) "without adversarial validation" reads neutral | FAIL (IMPORTANT) | Hard-codes that the *only* sanctioned validation path is adversarial — backend-shape leak |

## Summary

- Checks passed: 5 / 10
- Checks failed: 5
- Critical issues: 0
- Important issues: 4
- Minor issues: 1
- Issues fixed in-place: 0 (REPORT ONLY)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | SKILL.md:215 | "The diagnostic escalation backend runs autonomously **through all its phases** and returns a structured return contract." — "through all its phases" asserts the backend is internally multi-phase. A swapped single-pass backend would make this prose false, yet it is neither the declaration nor the invocation string. Forensic-pipeline-shape leak. | Neutralize to e.g. "runs autonomously and returns a structured return contract." Drop "through all its phases." |
| 2 | IMPORTANT | SKILL.md:178–179 | The renamed "Escalation gradient … for diagnostic-backend escalation" block ties TFEP escalation to the backend's *internal adversarial debate*: "Low-confidence root cause from **adversarial debate**" and "Unresolved **adversarial outcome (no winner/tie)**". These presume the backend runs an adversarial-debate stage producing a winner/tie verdict. A backend without debate cannot surface these signals; swapping it would require editing this prose, not just the declaration/invocation. | Re-phrase backend-neutrally: "Low-confidence root cause reported by the backend" and "Backend returns an inconclusive/unresolved diagnosis." Remove the "adversarial debate"/"winner/tie" framing from the neutral prose. |
| 3 | IMPORTANT | SKILL.md:229 | `## Failure Remediation Plan (**Adjudicated**)` heading — "Adjudicated" presumes the backend performed an adjudication (debate-resolution) step. This is prose (a literal output heading the caller writes), not the invocation string, so it is in Phase-2 scope. A non-adjudicating backend makes the label misleading. | Use a backend-neutral label, e.g. `## Failure Remediation Plan (Diagnosed)` or `## Failure Remediation Plan`. |
| 4 | IMPORTANT | SKILL.md:144 | Prohibition rule 2: "MUST NOT modify test expectations … without **adversarial validation**." This is a renamed/standing TFEP rule (not a deferred string). It hard-codes *adversarial* validation as the sole sanctioned gate, baking the forensic backend's debate shape into a VIOLATION-level rule. A troubleshoot backend that validates without an adversarial debate cannot satisfy the literal wording. | Generalize to "without TFEP validation" or "without backend-adjudicated validation," so the rule binds to the protocol, not to a specific backend's debate stage. (Note: L153 "Valid Adversarial Outcome" / "adversarial debate" has the same property; if §4.5 is meant to be backend-neutral, treat L153 consistently with L144.) |
| 5 | IMPORTANT→CONTRADICTION | SKILL.md:137 | The declaration claims a swap "changes only this declaration and the invocation string." Issues #1–#4 prove the body itself carries backend-shape assumptions, so the claim is false as written. Per Critical Rule #6, a self-contradiction between the neutrality promise and the neutral-prose body is at least IMPORTANT. | Either (a) neutralize the body (issues #1–#4) so the promise becomes true, OR (b) soften the declaration to enumerate the additional surfaces that change on a swap. (a) is preferred — the whole point of Phase 2 is to make (a) hold. |

### Borderline / noted, NOT failed (scope-edge — flagged for the orchestrator)

- **L221, L223** — return-contract field-name couplings (`test_is_wrong`,
  `status == "partial"`, `recommended_escalation != "none"`). These assume the
  backend emits these exact contract fields. Arguably part of the
  `return-contract.yaml` read surface the task marked **deferred to Phases 5/6**,
  so NOT counted as a Phase-2 failure — but they are a real residual coupling the
  later phases must resolve, because field names are not "the invocation string."
- **L208 "diagnostic depth"** — accepted as neutral; "depth" is generic. Noted
  only so the orchestrator knows it was consciously evaluated, not skipped.

## Actions Taken

None. `fix_authorization: false` — report only. No files modified.

## Self-Audit

**(a) Reliance list — structural items skipped:**

- Relied on no inherited structural verdict (none supplied in spawn prompt);
  ran standalone per fallback behavior.

**(b) Independent semantic checks (≥1 required, INV-019):**

- Verified the `troubleshoot` backend the declaration names actually exists:
  `ls src/superclaude/skills/` → `sc-troubleshoot-protocol` present, no
  `sc-forensic` dir (confirms the rename target and that the deferred
  `/sc:forensic` strings are genuinely stale-by-design, not typos).
- Verified the deferred-string boundary by grepping `forensic`/`diagnostic`/
  `adversarial`/`verdict` across §4.5 (lines 80–322) and cross-checked each hit
  against the task's explicit deferred list (L214, L218, L249–250, L260–261) so
  no deferred string was miscounted as a Phase-2 failure.
- Verified each flagged line number by re-Reading lines 133–263 in this turn
  (file unmodified since), so every `file:line` citation above is current.

**Confidence:** Verified: 10/10 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100%
**Tool engagement:** Read: 3 | Grep: 2 | Glob: 0 | Bash: 2

## Recommendations

- FAIL the Phase-2 backend-neutrality gate. Resolve issues #1–#5 (all
  IMPORTANT). The cheapest correct fix for #5 is to land #1–#4, after which the
  L137 promise becomes literally true.
- The recurring root cause is one word-family — "adversarial / adjudicated /
  phases / winner-tie" — leaking the forensic backend's *internal* debate-RCA
  shape into prose that is supposed to bind to the protocol, not the backend.
  Sweep §4.5 for that family and neutralize every occurrence that is NOT a
  deferred invocation/contract string.
- Forward to Phases 5/6: the return-contract field-name couplings (L221/L223)
  and the deferred `/sc:forensic` strings must be neutralized there; this lens
  intentionally did not count them as Phase-2 failures.

## QA Complete
