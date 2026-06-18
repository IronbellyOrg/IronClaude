# Why-it-escaped hypothesis card: E2 PRD completion-phase false positive

## Lens

Verification-artifact / off-path-review lens.

## Escape under analysis

- **Escape id:** `E2-PRD-completion-phase-false-positive`
- **Observed symptom:** A STRICT `parallel_instructions` gate halted a live heavyweight PRD `build-task-file` run because the final sequential completion/presentation phase lacked parallel keywords.
- **Fixed by:** PR #154, merge `e97aa4fd2a9d317abdc19f6ce2b5ccd35497df0e`.

## Hypothesis

This escaped review because the verification artifacts validated the gate as a local keyword-enforcement rule, not as a contract between the heavyweight PRD task-file template and the parser scope. Off-path review evidence was present in the broader workflow, but it was aimed at the immediate fix choice after the live failure rather than at a generated-artifact invariant: setup and completion are sequential bookends, while only middle executable work phases must carry parallel-execution instructions.

In other words, the review surface appears to have asked, "Does the phase checker catch missing parallel language?" and later, "Which exemption is safest for this observed final-phase failure?" It did not ask, "Does a full live/generated seven-phase PRD task file contain intentionally sequential non-work phases, and does the checker restrict itself to the executable work-phase subset?" That missing artifact-level question let the implementation's broad `phase >= 2` scope survive despite the documented or intended narrower middle-phase semantics.

## Evidence chain

1. The defect table records the escaped contract mismatch directly: PRD-E05 was a false positive on the final sequential Phase 7, and the stated miss was the template-phase contract that work phases are parallel while setup/completion bookends are intentionally sequential. It also notes that the docstring said phases 2-5 while the implementation checked every phase >=2. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row PRD-E05.

2. The target PR summary shows the runtime failure was not a marginal case: it halted a live heavyweight PRD run at `build-task-file` with `Phase 7 missing parallel execution instructions`. The same summary establishes the generated task's real phase semantics: Phases 2 through 6 were parallel work phases and passed; only Phase 7, `Present to User & Complete Task`, was sequential by anti-orphaning convention. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 60-70.

3. The broader PR summary repeats the same boundary condition and shows the fix decision centered on exempting a final completion-heading phase while preserving enforcement for true work phases. That supports the hypothesis that the original review did not have a full generated-task fixture encoding the bookend-vs-work distinction before the escape; the distinction only became explicit after the live failure. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 81-96.

4. The timeline places PR #154 in a sequence of meta-pipeline escapes, immediately after a reflect/off-path-review wiring escape (#153) and before a second strict parallel-gate false positive (#155). The timeline's meta-implication explicitly says #154 fixed one false-positive mode but did not sweep the phase-heading parser, unmasking #155 hours later. This supports the off-path-review hypothesis: review artifacts were too narrow around the observed failure and did not perform a full generated-artifact parser sweep. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` lines 20-28.

## Why review missed it

- **Artifact granularity mismatch:** The check was reviewed as a parser/gate rule, but the bug lived at the boundary between parser scope and full generated PRD task-file semantics.
- **Missing representative fixture:** The pipeline apparently lacked a live/generated seven-phase PRD task-file fixture where the final phase is intentionally sequential. Without that artifact, a broad `phase >= 2` rule can look correct because it enforces the local keyword invariant everywhere it scans.
- **Docstring was not treated as an executable invariant:** The evidence says the docstring described a narrower phase range while implementation scanned all phases from 2 onward. Review did not convert that docstring/template contract into a test that fails when parser scope drifts.
- **Off-path review was present but not aimed at this artifact contract:** The PR #154 summary mentions adversarial option artifacts, but those artifacts appear to adjudicate the fix after the escape (`clamp-to-2-5` vs `exempt-final-phase`) rather than pre-escape validation of the heavyweight template's phase semantics.
- **Symptom-local remediation pattern:** The timeline shows #154 was followed by #155, another strict parallel-gate false positive. That sequence suggests the review pattern addressed the immediate final-phase symptom without sweeping all non-executable `Phase N` surfaces in generated task files.

## Confidence

High. Multiple independent artifacts agree on the same missed contract: the gate enforced parallel keywords outside the intended executable work-phase subset, and the missing test was a full generated PRD task-file fixture or invariant tying parser scope to heavyweight template semantics.

## Prevention signal for future reviews

For generated workflow artifacts, off-path review should include at least one fixture at the final rendered-artifact level and should assert parser scope against artifact semantics, not just local parser behavior. In this case, the review artifact should have been a generated seven-phase PRD task file with sequential setup/completion bookends and parallel middle work phases, plus an invariant that only executable work phases are subject to the strict `parallel_instructions` requirement.
