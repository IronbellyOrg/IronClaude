# Remediation: whole-artifact classifier boundary gate

## Scope

This remediation is issue-agnostic. Apply it to any pipeline fix that touches a gate, parser, scanner, validator, recovery lookup, generated-output check, artifact reader, or severity policy. It is not PRD-specific and is not limited to markdown task files.

The durable rule is:

> Fix and verify the classifier boundary for the live runtime surface, not just the observed token that tripped the gate.

For E3, the escaped failure was a whole-artifact classifier bug: the live `build-task-file` gate scanned the full generated MDTM task file with broad `Phase N` heading discovery. PR #154 fixed the visible final sequential completion phase, but did not sweep sibling headings in the same generated artifact. The next run halted on non-executable Task Log placeholders such as `### Phase 2 - Codebase Research Findings`.

## Escape class

A parser/gate remediation is unsafe when all of these are true:

1. The live runtime input is broader than the patch analysis models.
2. The fix proves only the reported repro no longer fails.
3. Same-token or same-shape sibling surfaces remain in the matcher domain.
4. The gate is hard-fatal even though a false positive is more expensive than the defect it prevents.

Typical examples include:

- markdown heading scanners over generated documents;
- task-file, roadmap, reflect, sprint, validate, or audit gates;
- CLI command and subprocess validators;
- artifact path recovery and state readers;
- frontmatter/JSON/status enum readers;
- generated-output scanners over logs, task text, command text, or persisted state.

## Required remediation gate

Before merging a fix in this class, attach a short validation card to the task output, PR body, or review evidence. The card is intentionally small, but must answer every field below.

### 1. Runtime entrypoint

Name the live command/function boundary and the exact input shape consumed by the validator.

Required evidence:

- command, executor step, gate, scanner, subprocess call, or artifact reader;
- whether verification exercises that live boundary or only a helper seam;
- if a helper seam is used, why it is equivalent to the runtime boundary;
- one smoke path or fixture with the same artifact shape the live pipeline produces.

Acceptance rule: if the production failure occurred at a runtime boundary, at least one verification must run through that boundary or explicitly justify the narrower seam.

### 2. Contract ledger

Enumerate the contract being protected and every implementation that can satisfy or violate it.

For each relevant producer/consumer, record:

- producer of the artifact, command, field, status, or generated text;
- consumer/parser/gate that reads it;
- matcher or classification rule;
- severity decision: STRICT, advisory, or disabled;
- owner of the assumption.

Examples of contracts to ledger:

- generated task contract: executable phase headings vs Task Log, findings, review, appendix, placeholder, setup, and completion headings;
- document artifact contract: canonical output path, recovery roots, gate input source, and fallback behavior;
- command delivery contract: stdin, inline content, local file path, cloud file reference, subprocess argv;
- reflect/audit contract: effective diff includes task changes and excludes foreign work;
- artifact reader contract: missing, malformed, stale, corrupt, wrong-location, and wrong-but-present artifacts produce typed outcomes.

Acceptance rule: if only one implementation is patched, the ledger must show it is the only implementation of that contract or that sibling implementations already satisfy it.

### 3. Matcher/enforcement domain

List every syntactic surface the parser can consume, not only the intended target surface.

Required evidence:

- grep/codebase search, template inventory, generated fixture inventory, step list, or producer/consumer table;
- explicit statement of what is eligible for enforcement and what is ignored or downgraded;
- for generated prose, the full generated artifact region being scanned.

Acceptance rule: a whole-document matcher must either be constrained to the smallest semantically valid region or tested against sibling regions that can syntactically match.

### 4. Unmask-and-sweep

After fixing the observed failure, deliberately search for the next failure of the same class that the first failure may have hidden.

Required evidence:

- one positive fixture proving the intended target is still detected;
- one negative fixture proving off-path sibling content does not hard-fail;
- one adversarial full-artifact fixture containing both intended content and same-token/same-shape non-target content.

For markdown/generated text, the adversarial fixture must include executable sections and non-executable siblings in the same generated artifact. For JSON/frontmatter/artifact readers, cover missing, malformed, stale, corrupt, and wrong-but-present cases where applicable. For subprocess/diff/CLI contracts, cover the live invocation shape, not only string construction.

Acceptance rule: a patch that fixes only the original repro without at least one same-class false-positive and one same-class false-negative check is incomplete unless the severity is explicitly downgraded to advisory with cost rationale.

### 5. Severity and cost asymmetry

Classify the gate's false-positive cost against the defect's false-negative cost.

Required evidence:

- whether a false positive halts, blocks merge, fails CI, discards work, or merely warns;
- whether a false negative causes incorrect output, unsafe behavior, data loss, security exposure, or only slower/less efficient execution;
- whether the check is deterministic or heuristic;
- whether the parser reads structured data or loose generated prose.

Acceptance rule:

- Hard gates are appropriate for correctness, safety, data integrity, contract impossibility, or security-critical defects.
- Heuristic or convention-based checks over generated prose default to advisory unless the protected failure mode is correctness-, safety-, or data-integrity-critical and adversarial false-positive fixtures cover the classifier boundary.
- Checks guarding style, efficiency, completeness preference, or operator guidance should warn and capture evidence rather than halt long runs.

### 6. Heterogeneous off-path review

Use an independent review path when the change touches generated-output parsing, command emission, semantic gates, recovery paths, reflection/audit wiring, artifact discovery, or severity policy.

The reviewer must inspect the runtime topology, not just the local diff. The review prompt should be:

```text
Review this pipeline remediation issue-agnostically. Identify the live runtime entrypoint, enumerate all implementations of the affected contract, and look for same-token/same-shape false positives in non-target generated surfaces. Do not limit the review to the reported repro.
```

If no independent reviewer is available, the patch author must include the five validation-card sections above directly in the evidence and mark the review as waived with rationale.

## Low-cost checklist

Use this checklist before merge:

- [ ] Runtime entrypoint named and exercised, or narrower seam equivalence justified.
- [ ] Contract ledger lists producers, consumers, matcher, severity, and owners.
- [ ] Matcher/enforcement domain includes sibling surfaces, placeholders, appendices, logs, emitted outputs, and recovery paths where relevant.
- [ ] Full generated artifact or live invocation shape appears in at least one fixture.
- [ ] Positive fixture proves intended detection still works.
- [ ] Negative fixture proves same-token/same-shape sibling content does not hard-fail.
- [ ] One unmask-and-sweep case covers the next likely failure after the observed symptom.
- [ ] Severity is justified by false-positive and false-negative cost.
- [ ] Heuristic generated-prose checks are advisory unless correctness/safety/data-integrity critical.
- [ ] Independent/off-path review was performed or explicitly waived with rationale.

## Minimal acceptable evidence

This rule should increase defect-catch power without creating a heavy process. The smallest acceptable package is:

1. one full-artifact or live-boundary fixture;
2. one contract ledger paragraph or table;
3. one positive assertion;
4. one sibling/off-path negative assertion;
5. one severity decision with cost rationale.

For a markdown task-file parser, the compact fixture should contain:

- executable phase-plan headings that should be classified;
- setup/completion/bookend headings that should be ignored, exempted, or advisory;
- Task Log, findings, review, appendix, or placeholder headings that reuse phase-like tokens but are not executable work phases;
- assertions that hard-fatal checks apply only to the executable plan or that heuristic checks are advisory.

For a CLI/subprocess contract, the compact fixture should invoke the same command path the operator uses and assert argv, stdin/file delivery, output artifact, status enum, and halt reason.

For a recovery/artifact contract, the compact fixture should inject malformed, missing, stale, corrupt, and wrong-location artifacts as applicable and assert typed graceful outcomes instead of incidental crashes or passing for the wrong reason.

## Application to E3

Had this gate been applied to PR #154, it would have required:

1. naming `build-task-file` and `_check_parallel_instructions` as the runtime gate over the full generated MDTM task file;
2. recording that `_check_parallel_instructions` classified broad `Phase N` markdown headings across the whole artifact, not only executable phase-plan headings;
3. enumerating sibling headings containing `Phase N`, including Task Log findings placeholders;
4. adding a full-artifact fixture with valid work phases, the sequential completion phase, and empty Task Log findings headings;
5. asserting that only executable work phases are eligible for hard enforcement, or that the `parallel_instructions` heuristic is advisory;
6. reviewing the cost asymmetry: a false positive halted long PRD runs, while a miss usually caused slower serial execution rather than incorrect output.

That would have exposed the Task Log false positive before merge or led directly to the advisory-severity fix later applied by PR #155.

## Evidence basis

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E3-PRD-tasklog-findings-heading-sibling/root-cause.md` identifies the root cause as whole-artifact scan scope, broad `Phase N` discovery, and hard severity.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row `PRD-E06` records that PR #154 missed unmask-and-sweep over all generated task sections and needed a parser-focused full MDTM sweep.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` records the cost asymmetry: false positives halted long runs while the protected failure mode was slower serial execution.

## Owner guidance

Adopt this as a protocol gate for pipeline remediations, not as a one-off PRD test. Prefer structural classifier boundaries over regex inference. When regex inference remains, constrain it to the smallest semantically valid region and test all sibling regions that can match.

Under time pressure, do the smallest safe version: one full-artifact fixture, one contract ledger paragraph, one sibling negative assertion, and one advisory-vs-strict decision. That catches the E3 class without turning every remediation into a broad redesign.
