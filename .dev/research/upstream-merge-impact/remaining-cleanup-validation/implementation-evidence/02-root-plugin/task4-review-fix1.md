# Research: Final runtime guard fix acceptance

- **Topic type:** Fresh independent spec-compliance review
- **Scope:** Task 4 after one scoped working-directory guard fix pass
- **Status:** FAIL
- **Closed verdict:** `missing`
- **Authoritative reviewer report:** task4-fix1-independent-review.json (single authored source; this Markdown file is its index)
- **Date:** 2026-10-24
- **Template:** src/superclaude/templates/modularization-template-review/codebase-research_template.md

## Findings

[CODE-VERIFIED] The fresh reviewer rejected the resumed proof: actual merge-worker dependency installation violated the no-install boundary, and its final report emitted a bare-Python test recommendation contrary to the standing UV rule. The exact independently authored findings, raw citations and acceptance matrix live only in `task4-fix1-independent-review.json:4-37`; this index does not duplicate or amend that report.

## Gaps

[CODE-VERIFIED] T4.AC1, T4.AC2 and T4.AC5 remain unmet. T4.AC3/T4.AC4 and actual working-directory confinement pass. Cached acquisition was still an installation; no network download or operator-global Python mutation is asserted. See the authoritative report's `gaps` and `acceptance_criteria` fields.

## Key Takeaways

[CODE-VERIFIED] Do not record Task4 compliant. The one fix pass has failed independent review; proceed through the executor's escalating retry protocol without waiving criteria, deleting failed evidence or rewriting native output. Canonical verdict and next-action limits are in `task4-fix1-independent-review.json:21-37`.
