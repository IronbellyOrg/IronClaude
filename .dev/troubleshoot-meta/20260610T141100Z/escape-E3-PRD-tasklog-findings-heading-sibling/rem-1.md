# Remediation 1: Low-cost generated-artifact parser boundary gate

## Scope

This is an issue-agnostic remediation for pipeline escapes where a runtime gate, parser, scanner, or generated-output validator is fixed for one observed symptom but not validated against the full artifact surface it actually consumes.

It is not a PRD-only patch. The same protocol applies to PRD, roadmap, tasklist, reflect, sprint, validate, and any future pipeline that consumes generated artifacts, emitted command text, logs, frontmatter, JSON, markdown task files, or subprocess output.

## Escape class

A fix is unsafe when it proves only that the reported example no longer fails, while leaving the runtime classifier's full input domain unexamined.

For E3, the live `build-task-file` gate scanned the whole generated MDTM task file with loose phase-heading matching. PR #154 fixed the visible final-phase false positive, but did not sweep sibling headings in the same generated artifact. The next run then halted on Task Log placeholder headings such as `### Phase 2 - Codebase Research Findings`.

Generalized failure pattern:

1. A gate/parser consumes a larger runtime surface than the fix analysis modeled.
2. The test fixture contains only the observed failing case, not all same-token/same-shape sibling surfaces.
3. The gate is hard-fatal even though the protected failure mode is lower cost than a false positive.
4. Review is performed in the same frame as the patch and does not independently enumerate off-path runtime consumers.

## Required protocol gate

Before merging any remediation to a pipeline parser, semantic gate, generated-output scanner, or runtime artifact reader, require a short `classification-boundary sweep` note in the task output or PR evidence.

The note must answer four questions.

### 1. Runtime-entrypoint verification

Identify the live entrypoint and the exact runtime input it consumes.

Required evidence:

- the command, executor step, gate, scanner, subprocess call, or generated-artifact reader that failed or could fail;
- whether tests exercise that live entrypoint or only helper functions / command construction;
- one fixture or smoke path using the same artifact shape the live pipeline produces.

Acceptance rule:

- If the fix changes behavior observed at runtime, at least one verification must run through the same runtime boundary or explicitly justify why a narrower seam is equivalent.

This prevents fixes that validate helper logic while missing subprocess semantics, full markdown artifacts, uncommitted working-tree diffs, emitted task text, or recovery-path inputs.

### 2. Contract-implementation enumeration

List every implementation of the relevant contract, not just the implementation that failed.

Examples of contracts:

- local input delivery contract: inline content vs cloud-only file references;
- document-producing step contract: canonical output path, recovery search roots, gate input source;
- generated task contract: executable phase headings vs Task Log / findings / review / appendix headings;
- reflect/audit contract: effective diff must include the task's actual changes and exclude foreign work;
- semantic gate contract: strict checks halt only for correctness/safety violations, advisory checks warn for efficiency/style concerns.

Required evidence:

- an enumeration source such as grep, codebase search, template list, pipeline step list, generated fixture inventory, or a table of producer/consumer pairs;
- an explicit statement of which implementations were changed, which were verified unchanged, and which are out of scope.

Acceptance rule:

- If only one implementation is patched, the evidence must show it is the only implementation of that contract or that sibling implementations already satisfy it.

This prevents one-pipeline fixes when sibling pipelines already encode the correct contract or when templates, prompts, gates, and recovery logic drift independently.

### 3. Unmask-and-sweep

After fixing the observed failure, deliberately search for the next failure of the same class that the first failure may have hidden.

Required evidence:

- at least one adversarial fixture containing the original failing token or shape in non-target locations;
- at least one positive fixture proving the intended target is still detected;
- at least one negative fixture proving sibling / placeholder / appendix / log / emitted-output surfaces are ignored or downgraded appropriately.

For markdown or generated text parsers, the sweep must cover the full generated artifact, not an isolated snippet. Include executable sections and non-executable siblings in the same fixture.

For JSON/frontmatter/artifact readers, the sweep must cover missing, malformed, stale, corrupt, and wrong-but-present artifacts where applicable.

For command/diff/subprocess contracts, the sweep must cover the live invocation shape, not only string construction.

Acceptance rule:

- A patch that fixes only the original repro without at least one same-class false-positive and one same-class false-negative check is incomplete unless the maintainer explicitly downgrades the change to advisory-only and records the cost rationale.

This prevents symptom patches such as excluding one final phase while leaving other `Phase N` headings in the parser's enforcement domain.

### 4. Severity and cost-asymmetry review

Classify the gate's failure cost against the defect it prevents.

Required evidence:

- whether a false positive halts, blocks merge, fails CI, discards work, or merely warns;
- whether a false negative causes incorrect output, unsafe behavior, data loss, security exposure, or only slower/less efficient execution;
- whether the check is deterministic or heuristic;
- whether the parser operates on structured data or loose generated prose.

Acceptance rule:

- Heuristic checks over generated prose must not be hard-fatal unless the protected failure mode is correctness-, safety-, or data-integrity-critical and the classifier boundary is covered by adversarial false-positive fixtures.
- If the protected failure mode is efficiency, style, completeness preference, or operator guidance, default to advisory warning plus telemetry/evidence capture.

This prevents a brittle parser from halting long runs when the underlying issue is merely reduced parallelism or slower execution.

## Heterogeneous off-path review trigger

Use an independent review path when any of these are true:

- the fix touches generated-output parsing, command emission, semantic gates, recovery paths, or reflection/audit wiring;
- the first failure was discovered only in a live pipeline run;
- the proposed fix narrows or broadens a parser regex, heading classifier, artifact search pattern, file discovery rule, or severity policy;
- the patch changes which evidence is considered authoritative.

The off-path reviewer must not only inspect the diff. They must enumerate the runtime entrypoint and at least one off-path surface where the same token/shape can appear.

Minimum prompt for the review:

```text
Review this pipeline remediation issue-agnostically. Identify the live runtime entrypoint, enumerate all implementations of the affected contract, and look for same-token/same-shape false positives in non-target generated surfaces. Do not limit the review to the reported repro.
```

When an off-path review is not available, the patch author must include the four-question classification-boundary sweep note directly in the evidence.

## Low-cost checklist

Use this checklist before merge:

- [ ] Runtime entrypoint named and exercised, or narrower seam equivalence justified.
- [ ] All implementations of the affected contract enumerated.
- [ ] Full generated artifact or live invocation shape included in at least one fixture.
- [ ] Positive fixture proves intended detection still works.
- [ ] Negative fixture proves sibling/off-path same-token surfaces do not hard-fail.
- [ ] One unmask-and-sweep case added for the next likely failure after the observed symptom.
- [ ] Gate severity reviewed against false-positive and false-negative costs.
- [ ] Heuristic generated-prose checks are advisory unless correctness/safety-critical.
- [ ] Independent/off-path review performed for parser/gate/recovery/audit changes, or explicitly waived with rationale.

## Evidence standard

The evidence does not need a large new test harness. A low-cost remediation is acceptable if it adds one compact generated-artifact fixture or smoke test and one short classification-boundary note.

For a markdown task-file parser, a sufficient fixture contains:

- executable phase-plan headings that should be classified;
- setup/completion/bookend headings that should be ignored or exempted;
- Task Log, findings, review, appendix, or placeholder headings that reuse phase-like tokens but are not executable work phases;
- assertions that hard-fatal checks apply only to the executable plan or that heuristic checks are advisory.

For a CLI/subprocess contract, a sufficient fixture invokes the same command path the operator uses and asserts the real subprocess arguments, stdin/file delivery, output artifact, status enum, and halt reason.

For a recovery/artifact contract, a sufficient fixture injects malformed, missing, stale, and wrong-location artifacts and asserts typed graceful outcomes instead of incidental crashes or passing for the wrong reason.

## Application to E3

Had this protocol been applied to PR #154, the remediation would have required:

1. naming `build-task-file` and `_check_parallel_instructions` as the runtime gate over the full generated MDTM task file;
2. enumerating all generated headings containing `Phase N`, including executable plan headings and Task Log findings placeholders;
3. adding a full-artifact fixture with both the sequential final completion phase and empty Task Log findings headings;
4. reviewing whether `parallel_instructions` deserved hard-fatal severity despite guarding against slower serial execution rather than incorrect output.

That would have exposed the Task Log false positive before merge, or would have led directly to the advisory-severity fix that PR #155 ultimately applied.

## Owner guidance

Adopt this as a protocol gate for pipeline remediations, not as a one-off test requirement for PRD. The durable invariant is:

> Fix the classifier boundary and severity model for the runtime surface, not just the observed token that tripped it.

When the team is under time pressure, do the smallest safe version: one full-artifact fixture, one contract enumeration paragraph, and an advisory-vs-strict decision. That is enough to catch the E3 class without turning every fix into a broad redesign.
