# Reflect deviation patterns — IronClaude

## reflect-post-config-error-20260707060955 (UC-2, B2/C2/D2 reflect-CLI observability)
- Verdict: PASS (tier 2, convergence 0.94, calibrated 0.91). 0 regression, 0 gating deviation.
- Recurring pattern: **completed work delivered as UNCOMMITTED working-tree state** — `--diff origin/master..HEAD` was empty because HEAD==branch==origin/master. Reflect correctly audited the working-tree diff instead of reporting a vacuous empty-diff success. (Watch for this on skill-mode POST runs invoked before the executor commits.)
- Recurring pattern: `--spec` path (a REPORT.md) absent because it equals the tasklist's own `spec_path` frontmatter, which pointed at a troubleshoot dir containing only `audit.log`. Gold-standard fell back to `research/06-gap-fill-*-contract.md` canonical per-edit contract.
- Deviation profile: 2 LOW non-gating **test-adequacy Drift** (weak frontmatter-leak assertion; missing exact git-call-count). No implementation drift. A "5→7 construction sites" comment initially flagged LOW-drift by one reviewer was refuted by another reviewer's independent enumeration → resolved to none. Lesson: accurate comments are not drift; require independent verification before classifying a comment as drift.
- Promotion correctly withheld (gate-failed): the reflect gate IS the step that unblocks task finalization; frontmatter was still "🟠 Doing", work uncommitted.

## pre-mergedOutput-20261024165806 (UC-1, sc:implement severity plan)
- Recurring pattern: specs labelled FR-/NFR-/AC- yield 0 Pass-1 ids (reflect regex is R-/REQ-/SPEC-/T- only) -> coverage_degraded parsed-sparse forces T2 every time. Lexical containment then undercounts paraphrase (189/322); a qa reviewer walking the unmapped rows is what finds the real drops.
- Recurring plan-defect classes for protocol edits: (1) plan requires `make verify-sync` but never runs `make sync-dev`; (2) spec rule text carries `SKILL.md:NNN` pointers that test_protocol_prose_has_no_cross_file_line_pointers rejects; (3) rules placed in a ref file that is not loaded on the path that needs them (retry.md loads only on A2 failure/resume); (4) bare line citations drift once earlier tasks edit the same file.
- Lesson: label-only FR->task self-audits falsely report coverage; require content-level disposition of unmapped rows.
