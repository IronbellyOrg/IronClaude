# Qualitative Scoring Brief (Step 3, A.2 rubric, CEV protocol)

You are an independent evaluator. You are not an advocate and have not
seen the debate. Do not read any file under `.work/` except this brief.
Do not edit any file except your own assigned output file.

ART = /home/coder/workspaces/IronClaude/.dev/research/orca-dashboard-20261105/snapshot-brainstorm/adversarial/adversarial/

Inputs (read each in full from disk):
- Source all variants answer: /home/coder/workspaces/IronClaude/.dev/research/orca-dashboard-20261105/snapshot-brainstorm/seed-brief.md
- V1: ART/variant-1-opus-architect.md
- V2: ART/variant-2-sonnet-analyzer.md
- V3: ART/variant-3-haiku-backend.md

Context: each variant is a design-only spec for static ASCII five-minute
chat snapshots of an Orca multi-agent dashboard (five whole-report
concepts plus a recommended default). Judge each against the seed brief.

## Criteria (30 binary, 6 dimensions)

Completeness: CO1 covers all explicit requirements from the seed brief
(Constraints + Success Criteria); CO2 edge cases and failure scenarios;
CO3 dependencies and prerequisites; CO4 success/completion criteria;
CO5 explicit out-of-scope.
Correctness: CR1 no factual errors or hallucinated claims (relative to
the seed brief's Known Context); CR2 approaches feasible within stated
constraints; CR3 terminology consistent; CR4 no internal contradictions;
CR5 claims supported by rationale/evidence in the document.
Structure: ST1 logical ordering; ST2 consistent hierarchy, no orphaned
subsections; ST3 clear separation of concerns; ST4 navigation aids (TOC,
cross-references or index); ST5 follows conventions of a design spec.
Clarity: CL1 unambiguous language; CL2 concrete not abstract; CL3 each
section has a clear purpose; CL4 acronyms/domain terms defined on first
use; CL5 actionable next steps or decision points identified.
Risk Coverage: RK1 at least 3 risks with probability AND impact; RK2
mitigation for each identified risk; RK3 failure modes and recovery;
RK4 external dependencies and their failure scenarios; RK5 monitoring or
validation mechanism for risk detection.
Invariant & Edge Case Coverage: IE1 collection boundaries (empty,
single, maximum/overflow); IE2 state variable interactions across
component boundaries; IE3 guard condition gaps; IE4 count divergence
(off-by-one, inclusive/exclusive, observed vs total); IE5 interaction
effects when features combine.

## CEV rules

For every criterion and every variant:
CLAIM: "<criterion> is met/not met in Vn"
EVIDENCE: direct short quote with section reference, OR "No evidence
found - searched sections [list]"
VERDICT: MET (1) | NOT MET (0)
No partial credit. If you cannot cite specific evidence, the verdict is
NOT MET. Start adversarially: assume defects exist.

## Output format

Your assigned output file (named in your task prompt). Stub-first: write
the headings with `<!-- TODO -->` placeholders, then fill in place.

```
# Qualitative Pass <N> (order: <order>)

## Variant <first in your order>
| Criterion | Claim | Evidence | Verdict |
|-----------|-------|----------|---------|
| CO1 | ... | ... | MET |
... (all 30 rows CO1..IE5 in the order listed above)

## Variant <second> ...
## Variant <third> ...

## Summary
| Variant | Completeness | Correctness | Structure | Clarity | Risk | Invariant | Total /30 |
```

Evaluate variants strictly in the order given in your task prompt,
completing all 30 criteria for one variant before starting the next.
Verdict cells contain exactly `MET` or `NOT MET`. Final file has no
`<!-- TODO -->` markers. Your final message: just the output path and one
line confirming 90 rows plus the summary are present.
