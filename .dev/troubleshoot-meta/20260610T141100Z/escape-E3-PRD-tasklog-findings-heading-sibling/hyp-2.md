# Why-It-Escaped Hypothesis Card: E3 PRD Task-Log Findings Heading Sibling

## Escape

- **ID:** E3-PRD-tasklog-findings-heading-sibling
- **Lens:** verification-artifact / off-path review
- **Symptom:** After PR #154, the same STRICT `parallel_instructions` gate halted again because loose phase-heading matching consumed Task-Log placeholder headings such as `### Phase 2 - Codebase Research Findings` and failed on empty placeholder content.
- **Fix reference:** PR #155 / `eb9a2633bfc49b96f2a677fd907a68976f2a5fd9`

## Independent hypothesis

This escaped review because the PR #154 verification artifacts were optimized around the observed final-phase false positive, not around the broader parser boundary implied by the failure class. The off-path review confirmed that a final completion phase should be exempted and preserved enforcement for real work phases, but it did not force the parser to ingest full generated MDTM task files with non-executable sibling sections such as Task Log placeholders. As a result, review validated the corrected phase-range semantics while leaving the heading-discovery surface effectively unchallenged.

The second escape was therefore not primarily a missing patch detail; it was a review-scope failure. Review treated the defect as "which executable phases should the hard gate inspect?" rather than "which headings can the hard gate accidentally classify as executable phases?" That framing allowed Task Log headings to remain outside the adversarial fixture set even though they use the same `Phase N` vocabulary as executable plan headings.

## Evidence chain

1. The defect table records PRD-E06 as a repeat false positive after PR #154: the STRICT gate matched Task-Log placeholders like `### Phase 2 - Codebase Research Findings`, then failed on empty placeholder content. It also states that PR #154 fixed only the observed final-phase case and did not sweep the parser over all generated task sections. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` lines 12-13.
2. The PR #154 summary shows the verification focus: the bug was framed as checking every phase >=2 despite a `phases 2-5` docstring, with live ground truth centered on Phase 7 being a sequential completion/presentation phase. The chosen fix exempted the final phase only when its heading looked like completion, while preserving enforcement for short real-work tasks. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 60-70.
3. The PR #155 summary states that the same heuristic check had false-positived twice, and the second false positive was specifically caused by the regex matching Task-Log `### Phase N - … Findings` placeholder headings. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 81-86.
4. The broader PR summary confirms the cost asymmetry recognized only after the repeat: a hard failure halted long heavyweight runs even though the guarded failure mode was only slower serial execution, not incorrect output. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 97-112.
5. The timeline shows this was a direct sequence: PR #154 at 02:46 fixed the final completion-phase false positive; PR #155 at 05:13 addressed the subsequent Task-Log placeholder false positive by changing the check to advisory. Source: `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` lines 21-22.

## Why review missed it

- **Observed-case anchoring:** PR #154's artifacts centered on the live Phase 7 failure. The reviewed invariant became "setup and completion bookends are exempt; middle work phases are enforced," not "the parser must distinguish executable phase-plan headings from every other generated `Phase N` heading."
- **Fixture shape was too narrow:** The tested/reviewed cases described in the PR #154 summary covered a live 7-phase repro, a short completion-phase exemption, and a final work-phase enforcement case. Those fixtures exercise phase semantics, but not sibling generated sections such as Task Log findings placeholders.
- **The off-path lens reviewed the decision, not the artifact topology:** The adversarial comparison in PR #154 debated clamp-to-2-5 versus completion-heading exemption. That is useful for phase-range correctness, but it does not prove the heading enumerator is scoped to the executable task plan.
- **Hard-gate severity raised the cost of parser ambiguity:** Because `parallel_instructions` was STRICT, any parser false positive became a run-halting defect. The advisory severity analysis appears only in PR #155, after the second false positive made the cost asymmetry explicit.

## Counterfactual catch point

A verification artifact that fed the gate a full generated MDTM task file, including Task Log sections and empty `### Phase N - … Findings` placeholders, should have caught this before PR #154 merged. The expected assertion would not be about patching PRD behavior; it would be about classification: only executable phase-plan headings are eligible for `parallel_instructions` enforcement, while Task Log/findings headings are non-executable review artifacts and must not be evaluated as phases.

## Confidence

High. The artifacts independently agree on the sequence, the narrowness of the PR #154 verification focus, the exact sibling-heading false positive in PR #155, and the later recognition that hard severity made heuristic parser false positives disproportionately expensive.
