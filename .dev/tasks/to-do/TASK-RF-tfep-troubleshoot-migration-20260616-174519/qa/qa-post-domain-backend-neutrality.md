# QA Report — Post-Completion Domain Lens: Backend-Neutrality

**Topic:** TFEP forensic→troubleshoot backend migration (SKILL.md §4.5)
**Date:** 2026-06-16
**Phase:** report-validation (post-completion domain QA, backend-neutrality lens)
**Fix authorization:** false (REPORT ONLY)
**Stance:** Adversarial — assume residual backend leakage exists; find it.

---

## Overall Verdict: FAIL

The forensic→troubleshoot migration is functionally complete and the residual
`forensic` sweep is clean (zero live hits). HOWEVER, the stated neutrality contract —
"a future backend swap would touch ONLY the `**Diagnostic backend:**` declaration
(line ~137) and the invocation/budget strings" — is **NOT** met. Three surfaces
outside the declared change-points name the `troubleshoot` backend or bind to its
internal wave-shape / artifact-filename layout. A backend swap would have to edit
these too, which violates the single-change-point invariant this migration was meant
to establish.

---

## Residual `forensic` Sweep (REQUIRED OUTPUT)

Command:

```
rg -n "/sc:forensic|\bforensic\b" \
  src/superclaude/skills/sc-task-protocol/SKILL.md \
  src/superclaude/commands/task.md
```

Output: (no matches; rg exit code 1)

```
EXIT=1
```

**Result: ZERO live hits. PASS on the residual-sweep sub-check.**

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Bare-term prose neutral (gradient header, Step 3/4 headings, "diagnostic depth", "Diagnostic artifacts" label, declaration) | PASS | L174 "Escalation gradient (within-TFEP, for diagnostic-backend escalation)"; L207 "Step 3: Invoke diagnostic escalation"; L208 "diagnostic depth"; L218 "Step 4: Consume diagnostic results"; L260 label "**Diagnostic artifacts:**" — all backend-neutral wording |
| 2 | Incident template binds to neutral contract fields, not backend report layout | PARTIAL/FAIL | L257-258 bind to `root_cause_summary`/`solution_summary` (neutral ✓); but L260 hard-codes backend artifact FILENAMES `REPORT.md` and `audit.log` in parentheticals (leak) |
| 3 | Only backend-named surfaces are the declaration + invocation/budget strings | FAIL | L219, L239, L260 name `troubleshoot` / `Wave 5` / `REPORT.md`+`audit.log` OUTSIDE the declared change-points |
| 4 | Declaration line is the single backend authority (L137) | PASS | L137 `**Diagnostic backend:** \`troubleshoot\`` present and correctly scoped |
| 5 | Invocation strings (expected change-points) | PASS | L215, L228, L229, L268-270 are `/sc:troubleshoot` invocation/budget strings — expected change-points, neutral by contract |
| 6 | Residual `forensic` sweep zero live hits | PASS | rg exit 1, no matches (see above) |
| 7 | task.md free of forensic refs | PASS | included in sweep — zero hits |

## Summary

- Checks passed: 4 / 7
- Checks failed: 2 (items 2, 3); 1 partial folded into FAIL
- Critical issues (neutrality-contract violations): 3
- Issues fixed in-place: 0 (report-only)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | SKILL.md:219 | "`see \`sc:troubleshoot-protocol\` **Wave 5** emission`" leaks the troubleshoot backend NAME *and* its internal **wave-shape** ("Wave 5"). The neutrality contract explicitly forbids binding to backend wave-shape. A backend without a "Wave 5" concept (e.g. a phase-based or single-pass backend) would force an edit here. This is neither the declaration nor an invocation/budget string. | Replace with a backend-neutral pointer, e.g. "see the Diagnostic backend's return-contract emission" and drop "Wave 5". Defer the backend-specific cross-reference to the L137 declaration. |
| 2 | IMPORTANT | SKILL.md:260 | Incident template hard-codes the troubleshoot backend's ARTIFACT FILENAMES: "`report_path` (REPORT.md), `audit_log_path` (audit.log)". The contract-field names (`report_path`/`audit_log_path`) are correctly neutral, but the parenthetical filenames are backend-specific report layout — exactly what item-2 of the lens forbids. A backend emitting `diagnosis.md`/`trace.log` would force an edit here. | Drop the `(REPORT.md)`/`(audit.log)` parentheticals; cite only the neutral contract fields `report_path`/`audit_log_path`. The filenames belong (if anywhere) behind the L137 declaration. |
| 3 | MINOR | SKILL.md:239 | Parenthetical ownership note names the backend in prose: "(Remediation ownership: **troubleshoot** diagnoses and emits the contract …)". Not the declaration, not an invocation string. A swap forces a prose edit here. | Replace bare "troubleshoot" with "the Diagnostic backend" (the note already ends "see the Diagnostic backend declaration" — make the subject match). |

### Borderline / Accepted (documented for completeness — NOT counted as leaks)

| Location | Term | Disposition |
|----------|------|-------------|
| SKILL.md:215, 228, 229 | bare word "troubleshoot" / `/sc:troubleshoot` | ACCEPTED — these are the literal invocation strings the contract designates as expected change-points. |
| SKILL.md:219 | `return-contract.yaml`, field names `status`/`test_is_wrong`/… | ACCEPTED — these are the TFEP **adapter contract** field names (backend-neutral interface), not backend-internal layout. Only the co-located "Wave 5" (Issue 1) is the leak. |
| SKILL.md:227, 235, 237 | "adjudicated" / "Adjudicated" | ACCEPTED — TFEP's own remediation-plan vocabulary, not a backend-shape term. |

## Why this is FAIL, not PASS

The migration's whole point is the single-change-point invariant stated in the
declaration itself (L137): "swapping the backend changes only this declaration and
the invocation string." Three surfaces (L219 "Wave 5", L260 filenames, L239 prose
"troubleshoot") falsify that sentence: a real backend swap would require editing them.
Because the declaration makes a literal promise the body does not keep, the section
is internally inconsistent and fails the neutrality lens. Severity is IMPORTANT (not
CRITICAL) because nothing here is a functional/runtime defect — the protocol executes
correctly today; the defect is in the swap-resilience guarantee.

## Recommendations (for the fix owner — NOT applied here)

1. SKILL.md:219 — strike "Wave 5"; make the cross-ref backend-neutral.
2. SKILL.md:260 — strike the `(REPORT.md)` / `(audit.log)` parentheticals; keep only the neutral field names.
3. SKILL.md:239 — change bare "troubleshoot" → "the Diagnostic backend".
4. Re-run this lens after the fix; target is exactly TWO backend-named surface classes remaining (the L137 declaration + the `/sc:troubleshoot` invocation/budget strings).

---

## Confidence

- **Confidence:** Verified: 7/7 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 3 | Glob: 0 | Bash: 3 (rg sweeps + region greps)
- No web research performed (no external claims in scope).
- Tool calls ≥ checklist items: 10 tool calls ≥ 7 checks — engagement sufficient.

## QA Complete
