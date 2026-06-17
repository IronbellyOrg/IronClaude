# QA Report — Backend-Neutrality (Phase 6)

**Topic:** TFEP incident-reporting + escalation-budget block backend-neutrality
**Target:** `src/superclaude/skills/sc-task-protocol/SKILL.md` §4.5 (lines ~247-271, with §4.5 header context 133-245)
**Date:** 2026-06-16
**Phase:** doc-qualitative (backend-neutrality lens)
**Fix authorization:** false (REPORT ONLY)
**Stance:** ADVERSARIAL — assumed >=5 backend-leaky phrasings survive; hunted for them.

---

## Overall Verdict: FAIL

Two RESIDUAL backend-specific PIPELINE-SHAPE leaks survive in the reporting block. These are
distinct from the permitted invocation/artifact binding (`/sc:troubleshoot`, `report_path`,
`audit_log_path`, REPORT.md/audit.log filenames, `--depth standard|deep`), which are correct and
NOT flagged per the spawn instructions.

Bright-line residual-forensic tokens are ALL CLEAN (grep-verified, file-wide): no `forensic`,
no `rca-verdict.md`, no `solution-verdict.md`, no `--tier`, no `--intent`. The budget block
(267-271) is clean. The leaks are subtler: prose that bakes in the troubleshoot backend's
INTERNAL report structure and INTERNAL wave shape.

## Items Reviewed
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | No `forensic` token | PASS | grep file-wide: 0 hits |
| 2 | No `rca-verdict.md` / `solution-verdict.md` | PASS | grep file-wide: 0 hits |
| 3 | No `--tier` / `--intent` flags | PASS | grep file-wide: 0 hits |
| 4 | Budget describes depths (standard/deep) cleanly | PASS | L267-271: depths + invocation strings only; no pipeline-shape baked in |
| 5 | Invocation/artifact binding is the only backend-specific surface | FAIL | L257-258 bake in backend report SECTION layout; L260 bakes in backend WAVE shape |
| 6 | Reporting prose names no backend-specific pipeline shape | FAIL | L260 "Tier-2 hypothesis cards", "adversarial artifacts" |

## Summary
- Checks passed: 4 / 6
- Checks failed: 2
- Critical issues: 0
- Important issues: 2
- Issues fixed in-place: 0 (report-only)

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | SKILL.md:257-258 | Bakes in the troubleshoot REPORT.md INTERNAL section layout: `root_cause_summary` "sourced from the **Diagnosis** section" and `solution_summary` "sourced from the **Proposed Fix** / **Next Steps** section". The artifact-field binding (`root_cause_summary`/`solution_summary` from the return contract) is permitted, but naming the backend report's internal heading structure is a pipeline-shape leak — a swapped backend need not emit "Diagnosis" / "Proposed Fix" / "Next Steps" sections. | Drop the "sourced from the **X** section of troubleshoot REPORT.md" clauses. The fields already come from the return contract (the neutral binding surface); the backend's internal report headings should not be asserted. E.g. `{`root_cause_summary` from the return contract}` with no section-layout claim. |
| 2 | IMPORTANT | SKILL.md:260 | `**Diagnostic artifacts**: ... Tier-2 hypothesis cards, and any adversarial artifacts` names troubleshoot's INTERNAL wave shape. "Tier-2", "hypothesis cards", and "adversarial artifacts" are the troubleshoot protocol's specific multi-wave pipeline (Tier-2 = parallel hypothesis agents + adversarial fix debate) — NOT artifact-field bindings like `report_path`/`audit_log_path`. A swapped backend may have no tiers, no hypothesis cards, and no adversarial stage. | Replace the backend-specific enumeration with a neutral artifact reference. E.g. `troubleshoot `report_path` (REPORT.md), `audit_log_path` (audit.log), and any additional diagnostic artifacts emitted by the backend`. Keep the two blessed field names; drop "Tier-2 hypothesis cards" and "adversarial artifacts". |

## Adversarial note (5+ leak hunt)
The stance assumed >=5 surviving leaks. After exhaustive grep + line-by-line read of 247-271 and
the full §4.5 frame (133-245), only TWO genuine pipeline-shape leaks survive; the rest of the
candidate surface is permitted invocation/artifact binding:
- `report_path` / `audit_log_path` field names + `(REPORT.md)` / `(audit.log)` filenames — PERMITTED (artifact binding).
- `/sc:troubleshoot --caller task-unified --depth standard|deep` invocation strings (L268-269, L215) — PERMITTED (invocation binding + the declared change-point at L137).
- `**Diagnostic backend:**` declaration (L137) — PERMITTED single change-point; correctly labels the neutrality contract.
- "adversarial" usages at L144/L153/L178/L179 are GENERIC TFEP/test-debate vocabulary in the prohibition+gradient prose, NOT backend pipeline references — NOT flagged.
Reporting honestly: the "expect 5" framing did not materialize into 5 real leaks; inflating to
hit a quota would be a false-positive. Two real IMPORTANT leaks, both in the reporting block.

## Self-Audit
1. Factual claims verified against source: 6 (all grep tokens + both leak locations read in full context).
2. Files read: SKILL.md lines 133-300 (full §4.5 + budget + adjacent §5), grep across entire file.
3. Why trust the check: every PASS is grep-backed (0-hit proofs) or line-read; every FAIL cites exact line + quoted text; did NOT inflate to the assumed count of 5.
4. Web research: none required (purely local-file neutrality assessment); Tavily-first N/A.

**Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: 4 | Grep(bash): 2 | Glob: 0

## Recommendations
Resolve both IMPORTANT leaks (257-258 report-section-layout bake-in; 260 Tier-2/adversarial
wave-shape bake-in) before Phase 6 sign-off. Both are surgical prose edits that preserve the
permitted invocation/artifact binding while removing the backend pipeline-shape assertions.

## QA Complete
