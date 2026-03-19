# Prompt 6 Refactor Notes

## Date: 2026-03-19

## Change Applied: Embedded Methodology Preamble Requirement

### What changed
Added a new **item 0 ("Methodology preamble")** to the Step 3 report requirements. This instructs the agent to reproduce the scoring framework's delta formula, threshold values, weighting scheme, and reproducibility definition directly in the eval report, rather than only referencing the external scoring-framework.md file.

Also added inline threshold/weight display requirements to items 2, 3, and 4 so that every table and score in the report is verifiable without cross-referencing.

### Why this improvement was selected
Three improvements were proposed and debated:

1. **Embed methodology summary in report** (self-containment) -- ADOPTED
2. **Make brainstorm invocation string more concrete** -- REJECTED (the current separation of concerns between invocation and validation sub-instructions is intentionally correct)
3. **Structured evidence block for happy-path declaration** -- ADOPTED in debate, but ranked lower impact than #1

Improvement 1 was selected for implementation because it addresses a structural gap affecting the entire report's verifiability. The eval report is the final deliverable of a 6-prompt pipeline; if a reviewer cannot verify its scores without opening a second file, the report fails its purpose as an audit artifact.

### Risks acknowledged
- Increases report length (methodology section adds ~20-40 lines)
- Agent may paraphrase the methodology imprecisely rather than reproducing it faithfully -- mitigated by the instruction to reproduce "verbatim or in a faithful structured summary"
- If scoring-framework.md is modified between Prompt 5 and Prompt 6 execution, the embedded copy could diverge -- low risk in a sequential pipeline

### Improvements NOT applied (available for future iteration)
- **Improvement 3 (structured happy-path evidence block)**: Would strengthen the validation declaration with mandatory worst-case values and explicit negative statements. Low complexity, recommended for next iteration.
