# Task-supplied report templates

Source: this dispatch's TASK block for issue #672. These local templates preserve its explicitly required output structure; they do not alter any product template.

## Findings template

The findings document must contain exactly these headings in this order, with every placeholder populated before completion:

```markdown
## Verdict
<!-- TODO: close, not-planned, in-progress or still-relevant, with source/live evidence and limitations -->

## Complexity and size
<!-- TODO: simple/medium/complex and XS/S/M/L/XL with one-line reason -->

## Priority
<!-- TODO: P0/P1/P2/P3 with impact and blockers, one-line reason -->

## Concrete next steps
<!-- TODO: remaining work, if any; no speculation presented as implementation-ready -->

## Dependencies
<!-- TODO: verified needs/blocks or explicitly unknown -->

## Related issues
<!-- TODO: verified issue relationships, not inferred dependencies -->

## Related PRs
<!-- TODO: linked/mentioned PRs, their verified state and relevance, or bounded negative evidence -->
```

## Independent review template

The reviewer must create qa.md themselves as a stub before collecting evidence, then populate it section by section. The first line must be `VERDICT: PASS` or `VERDICT: FAIL`; initial FAIL may mean verification incomplete and must be explained. Final PASS means no blocking defect remains; final FAIL means at least one blocking defect or required unverified input remains.

```markdown
VERDICT: FAIL

## Scope and evidence
<!-- TODO: independent checks against live GitHub and source -->

## Blocking defects
<!-- TODO: each defect, evidence and consequence, or verified zero with reasons -->

## Notes and limits
<!-- TODO: minor findings, unverified incident inputs, tests not run -->
```

Blocking defect: correcting it changes the verdict, complexity, size, priority, a next step, a dependency or a safety claim. Report concrete consequences; do not invent findings or treat a producer summary as evidence. Reviewer reads the findings and rechecks the live issue and source; it does not edit findings.md. At most two producer fix cycles, with a fresh reviewer each time.
