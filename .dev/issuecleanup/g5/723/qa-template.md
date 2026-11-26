# Issue 723 independent-review template

This is the governing QA template for the review requested in the dispatch brief. The reviewer did not write findings.md and must verify each load-bearing claim independently against the live issue and current source. A blocker changes verdict, complexity, size, priority, a next step, a dependency or a safety claim. At least one unresolved blocker means FAIL. Record every blocker with evidence and its consequence; zero findings is valid only with the checked scope and reasoning.

Use this report skeleton, stubbing the report before gathering findings and replacing every placeholder before completion:

```text
VERDICT: FAIL

## Scope checked
<!-- TODO: Claim groups, source, live GitHub reads and limits. -->

## Blocking defects
<!-- TODO: Each blocking defect, evidence and consequence, or None with reasoning. -->

## Non-blocking notes
<!-- TODO: Minor concerns or None. -->

## Verification conclusion
<!-- TODO: Final rationale for PASS or FAIL; mark unavailable evidence UNVERIFIED. -->
```

Change the first line to `VERDICT: PASS` only when no blocking defect remains. Do not edit findings.md or other deliverables; report corrections for the producing worker to make. Read files in pieces of at most 80 lines. All writes must stay under `/home/coder/workspaces/worktrees/IronClaude/Issuecleanup/.dev/issuecleanup/g5/723/`.
