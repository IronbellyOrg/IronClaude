# QA Report — Domain Lens: no-orphaned-forensic-refs

**Topic:** TFEP forensic→troubleshoot backend rename (Phase 2 migration)
**Date:** 2026-06-16
**Phase:** task-integrity (domain QA lens)
**Fix authorization:** false (REPORT ONLY)
**Stance:** ADVERSARIAL — assumed >=5 forensic terms survived; hunted for them.

---

## Overall Verdict: PASS

All Phase-2-targeted bare-`forensic` terms have been renamed. The only remaining
`forensic` / `/sc:forensic` hits are the four intentionally-deferred invocation-string
and return-contract references. `task.md` contains zero `forensic` hits.

---

## Raw rg Output (verbatim)

Command:
`rg -n "/sc:forensic|\bforensic\b" .../sc-task-protocol/SKILL.md .../commands/task.md`

```
.../sc-task-protocol/SKILL.md:214:6. Invoke: `/sc:forensic --tier {tier} --intent triage --caller task-unified --context {context_path} --output {output_dir} --depth quick`
.../sc-task-protocol/SKILL.md:218:8. Read the forensic return contract from `{output_dir}/return-contract.yaml`.
.../sc-task-protocol/SKILL.md:260:1st TFEP trigger  → /sc:forensic --tier light --intent triage    (~5-8K tokens)
.../sc-task-protocol/SKILL.md:261:2nd TFEP trigger  → /sc:forensic --tier standard                 (~15-20K tokens)
```

`task.md`: NO forensic hits.
Case-insensitive sweep (`rg -ni "forensic"`): same 4 lines only — no `Forensic`-cased survivors.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Line 214 `/sc:forensic --tier {tier} ...` invocation (Step 3) | PASS | Matches deferred allow-list item (invocation string at ~line 212). Verbatim at SKILL.md:214. |
| 2 | Line 218 `Read the forensic return contract from ...` (Step 4) | PASS | Matches deferred allow-list item (~line 216). Verbatim at SKILL.md:218. |
| 3 | Lines 260-261 Escalation Budget `/sc:forensic --tier light/standard` | PASS | Both match deferred allow-list (Escalation Budget lines). Verbatim at SKILL.md:260-261. |
| 4 | `{summary from rca-verdict.md}` / `{summary from solution-verdict.md}` incident-template sources | PASS | Present at SKILL.md:249-250; allow-listed, no bare `forensic` token. |
| 5 | "for future forensic integration" gradient header GONE | PASS | Line 174 now reads "Escalation gradient (within-TFEP, for diagnostic-backend escalation)". `rg -ni "future forensic integration"` → empty. |
| 6 | "forensic tier" GONE | PASS | `rg -ni "forensic tier"` → empty. |
| 7 | "forensic pipeline" GONE | PASS | `rg -ni "forensic pipeline"` → empty. |
| 8 | "Invoke forensic" heading GONE | PASS | `rg -ni "Invoke forensic"` → empty. Replaced: SKILL.md:207 "Step 3: Invoke diagnostic escalation". |
| 9 | "Consume forensic results" heading GONE | PASS | `rg -ni "Consume forensic"` → empty. Replaced: SKILL.md:217 "Step 4: Consume diagnostic results". |
| 10 | "Forensic artifacts" label GONE | PASS | `rg -ni "Forensic artifacts"` → empty. Replaced: SKILL.md:252 "Diagnostic artifacts:". |
| 11 | "alongside other forensic artifacts" GONE | PASS | `rg -ni "alongside other forensic"` → empty. Replaced: SKILL.md:255 "committed to git alongside other diagnostic artifacts". |
| 12 | task.md "structured forensic analysis" GONE | PASS | `rg -ni "structured forensic analysis"` over both files → empty. task.md has zero forensic hits. |
| 13 | No additional `Forensic`-cased survivors | PASS | Case-insensitive `rg -ni "forensic"` returns exactly the 4 deferred lines. |

## Summary

- Checks passed: 13 / 13
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found

None. All 8 named Phase-2 bare-term targets are GONE; all 4 surviving hits are
intentionally deferred and verified against the allow-list.

## Confidence

Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%

**Tool engagement:** Read: 1 | Grep: 5 (via rg in Bash) | Glob: 0 | Bash: 4

## Recommendations

- Green light from this domain lens. The deferred `/sc:forensic` invocation strings
  (lines 214, 218, 260-261) remain by design for later-phase migration; no action
  needed in Phase 2.

## QA Complete
