# Root cause: E3 PRD Task-Log findings heading sibling

## Verdict

PR #154 escaped because the investigation and verification narrowed the defect to the observed final-phase business rule while leaving the live gate's broader parser boundary untested. The runtime check did not operate on a curated executable phase model; it scanned the full generated MDTM task file with a loose `Phase N` heading regex. That made non-executable sibling sections, especially Task Log findings placeholders such as `### Phase 2 - Codebase Research Findings`, eligible for the same `parallel_instructions` enforcement path as real work phases.

The repeat halt was therefore caused by the combination of three conditions:

1. whole-artifact gate input rather than structured executable-phase input;
2. broad heading discovery that matched any markdown heading containing `Phase <number>`; and
3. STRICT enforcement of a brittle heuristic whose false-positive cost was a pipeline HALT.

PR #154 removed one symptom, the final completion phase false positive, but did not remove or comprehensively test the class: accidental classification of non-work headings as work phases.

## Surviving claims from the two cards

### 1. Runtime-entrypoint scope is the strongest causal explanation

The key technical cause is the live gate entrypoint and scan domain. `_check_parallel_instructions` discovers phases with a broad regex over the entire content:

```python
r"(?:^|\n)\s*#{1,4}\s+.*Phase\s+(\d+)"
```

It then slices from one matched phase heading to the next matched phase heading and requires parallel keywords in each later phase section unless the heading is the max-numbered completion phase. This behavior is sufficient to explain the escape: a Task Log heading with `Phase 2` is indistinguishable from an executable phase heading to the parser, and an empty placeholder body lacks the required keywords.

The `build-task-file` gate is the relevant live surface. It carries STRICT enforcement for the gate as a whole, while PR #155 later changed only `parallel_instructions` to advisory. The PR #155 summaries explicitly state that before the fix this same heuristic false-positived twice and halted long PRD runs.

### 2. Review artifacts were too narrow, but that is a contributing process cause

The verification-artifact card correctly identifies observed-case anchoring: PR #154 validated the final completion-phase exception and preservation of real work-phase enforcement. That was necessary but not general enough. The missing test was not another completion-phase test; it was a full generated MDTM task-file fixture containing non-executable sibling sections with `Phase N` wording.

This is best treated as the review/process reason the defect escaped, not the primary technical mechanism. The primary mechanism remains the runtime whole-file parser plus hard gate.

### 3. Severity amplified the defect into an expensive escape

Both cards correctly identify cost asymmetry. The check guarded against slower serial execution, not incorrect output. Because it was effectively on a hard halt path before PR #155, parser ambiguity became operationally expensive. The advisory change in PR #155 addressed that amplification by preserving warning signal without allowing future parser false positives to halt a good run.

## Refuted or weakened claims

### Refuted: the escape was mainly an off-path review problem

The off-path review framing is incomplete. Review scope explains why the issue was missed, but it does not fully explain why Task Log headings could halt the runtime. The stronger evidence is the runtime parser's scan domain and regex. Without the whole-file heading scanner, the narrow verification would have been less consequential.

### Weakened: PR #154 was merely a missing patch detail

The failure was broader than failing to add one exclusion for Task Log headings. Chasing a specific exclusion would still leave the same class open to other generated sibling headings that contain `Phase N`. The general missed invariant was parser classification: only executable phase-plan headings should be eligible for `parallel_instructions`, or the heuristic should not be hard-fatal.

### Weakened: the issue was only phase-range semantics

The phase-range docstring mismatch and final-phase exemption were real for PR #154, but E3 shows that phase-range semantics were not the whole failure class. The parser boundary, not just the accepted phase numbers, was under-specified.

## Evidence synthesis

- The defect table row PRD-E06 records that after PR #154 the STRICT parallel gate matched Task Log placeholders like `### Phase 2 - Codebase Research Findings` and failed on empty placeholder content.
- The PR #155 target summary states the heuristic had false-positived twice: first on the sequential final completion phase, then on Task Log `### Phase N - ... Findings` placeholders. It also records the cost asymmetry that made hard enforcement inappropriate.
- The broader PR summary repeats the same sequence and states that the failure mode guarded against was only slower serial execution.
- The timeline places PR #154 at 2026-06-10 02:46 for the final completion-phase false positive and PR #155 at 2026-06-10 05:13 for the subsequent Task Log placeholder false positive.
- The current source still shows the broad heading regex in `_check_parallel_instructions`, while the `build-task-file` wiring now marks `parallel_instructions` as advisory. That matches PR #155's stated remediation: reduce severity rather than continuing to chase all detection brittleness.

## Root cause statement

E3 escaped because PR #154's analysis fixed the visible final-phase symptom without generalizing the invariant to the parser's actual runtime input. The live gate scanned the entire generated task artifact for markdown headings containing `Phase N`, so non-executable Task Log placeholder headings were inside the enforcement domain. Because the heuristic was hard-fatal, this parser false positive halted a valid PRD run. The missed validation was a full-artifact, false-positive-oriented parser sweep over all generated heading surfaces, paired with a severity review of whether `parallel_instructions` deserved STRICT enforcement.

## Pipeline catch that would have prevented the escape

The pre-merge verification for PR #154 should have included a full generated MDTM task file with:

- valid executable work phases containing parallel/concurrent/batch instructions;
- a sequential final completion/presentation phase; and
- Task Log or findings sections containing empty `### Phase N - ... Findings` placeholders.

The expected assertion should have been classification-oriented: only executable phase-plan headings are evaluated for `parallel_instructions`, and non-executable Task Log/findings headings must not cause a hard gate failure. A separate severity check should have flagged the hard-gate asymmetry: false positives halt long runs, while missed parallel instructions usually only reduce execution efficiency.
