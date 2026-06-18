# Remediation 1: Runtime effective-input proof gate for generated review handoffs

## Scope

This is an issue-agnostic pipeline remediation, not a PRD-specific patch. It applies to any pipeline stage that generates, delegates, or validates an independent review command over a selected work surface: diff ranges, file lists, artifact paths, tasklists, prompts, or runtime logs.

## Escape addressed

`E5-Reflect-post-diff-wrong-base` escaped because the pipeline verified that a POST-reflect review step existed, but did not verify that the review step audited the same work surface produced by the actual runtime entrypoint. The generated command used a commit range derived from task start state. In normal `/task` execution, work commonly remains as uncommitted working-tree edits, so the range could omit the task work; if unrelated commits landed after task start, it could include foreign work.

## Generalized root cause

The pipeline accepted a handoff artifact based on syntax and presence instead of proving its effective input set.

This failure class appears whenever all of the following hold:

1. A generator emits a selector for downstream review or validation.
2. The selected surface is runtime-dependent rather than purely static.
3. The implementation entrypoint can produce uncommitted, staged, external, partial, or otherwise non-commit-bounded state.
4. Validation checks that the review exists, but not what the review consumed.
5. Tests cover the builder or helper in isolation, but not the production entrypoint that operators actually run.

## Remediation style

Low-cost protocol gate: add a mandatory checklist and fixture requirement to pipeline review, task-builder, and release-validation workflows. Do not add a large new framework. The gate is a small evidence requirement that blocks promotion when a generated review handoff cannot prove its effective input surface.

## Protocol gate

Before accepting any generated independent-review handoff, require an `Effective Input Proof` section in the evidence packet.

The proof must answer four questions:

1. **Runtime entrypoint:** Which command or skill will an operator actually run?
2. **Implementation contract:** What file, diff, artifact, prompt, or log surface can that entrypoint produce at runtime, including dirty working-tree state?
3. **Generated selector:** What selector did the pipeline emit for the reviewer?
4. **Effective input match:** How was it proven that the reviewer consumed the runtime-produced surface and excluded unrelated surface?

A PASS requires evidence, not assertion. Acceptable evidence can be a small e2e, a captured changed-file list, an effective-diff manifest, a generated command plus resolved-file manifest, or a negative fixture that fails before the fix and passes after it.

## Required invariants

### I1. Runtime-entrypoint verification

Every generated review handoff must be exercised through the same entrypoint operators use, or through a faithful harness that preserves the entrypoint's state semantics.

For `/task`-like flows, the harness must permit tracked-file edits without a commit. For headless CLI flows, the harness must execute the real subprocess boundary when the defect class depends on CLI behavior. Builder-only tests are insufficient when the runtime entrypoint mutates or resolves state differently.

### I2. Contract-implementation enumeration

For each generated handoff, enumerate the contract and all implementations that can satisfy or violate it.

Minimum enumeration:

- source generator that emits the handoff;
- runtime entrypoint that performs the work;
- reviewer command or agent that consumes the selector;
- artifact or diff resolver used by the reviewer;
- validation gate that decides PASS/FAIL;
- recovery/resume path, if present.

The gate blocks if the evidence only checks the generator text while skipping the consumer or runtime resolver.

### I3. Effective input proof

The downstream reviewer must prove the exact input surface it audited.

For diff-like reviews, record at least:

- base selection rule;
- whether dirty working-tree changes are included;
- list of included task/work files;
- list or assertion excluding unrelated commits/files;
- command actually run after placeholder resolution.

For artifact-like reviews, record at least:

- canonical path;
- whether stdout/NDJSON was ignored or accepted;
- recovery search behavior;
- malformed/missing artifact behavior;
- exact artifact consumed by the gate.

### I4. Unmask-and-sweep

When a handoff bug is found, do not patch only the observed command. Sweep sibling generators and validators for the same pattern:

- commit-range selectors where runtime work can be uncommitted;
- path selectors where runtime may write canonical artifacts elsewhere;
- prompt selectors where CLI flags or inputs may not survive into the first model prompt;
- parser/gate selectors where non-executable sections can be mistaken for executable work;
- resume/recovery paths that use different selectors than fresh runs.

The sweep result must list checked surfaces and state whether each is affected, unaffected, or needs follow-up.

### I5. Heterogeneous off-path review

When supported by the task criticality or prior escapes, keep off-path review, but require it to be heterogeneous in both reviewer identity and input derivation.

A reviewer running in a different session or model is not enough if it consumes the same wrong selector. The review must either derive the input surface independently or verify the generated selector against a runtime manifest before auditing.

## Minimal regression fixture

Add one dogfood e2e fixture for the class, not one PRD-only fixture.

Fixture shape:

1. Generate a task or pipeline artifact that includes a terminal independent-review handoff.
2. Execute through the real runtime entrypoint or faithful harness.
3. Mutate tracked files without committing them.
4. Optionally create or simulate a foreign commit after the recorded start point.
5. Run the generated review handoff exactly as emitted, after normal placeholder resolution.
6. Assert the review's effective input manifest includes the runtime-touched files.
7. Assert the manifest excludes the foreign commit or unrelated files.
8. Fail if the review only proves command presence, PASS text, or artifact existence.

This fixture is intentionally reusable across PRD, task-builder, tasklist, roadmap, and reflect-style workflows: swap the entrypoint and selector type, keep the effective-input assertion.

## Low-cost implementation plan

1. Add an `Effective Input Proof` subsection to pipeline evidence templates and review checklists.
2. Add a small reusable helper or test assertion that compares expected runtime-touched files with reviewer-consumed files.
3. Add the dogfood dirty-working-tree fixture for generated POST-review handoffs.
4. Add an unmask-and-sweep checklist item to escape remediation: list sibling entrypoints and selector emitters before closing the fix.
5. Treat missing proof as a blocking validation failure for high-impact or terminal gates; allow advisory severity only for explicitly non-blocking review steps.

## Acceptance criteria

- A generated review handoff cannot pass solely because the command exists.
- A review artifact cannot pass without declaring what input surface it consumed.
- At least one regression fixture covers dirty working-tree runtime output.
- The fixture fails on a commit-range-only selector when runtime work is uncommitted.
- The fixture fails when a foreign commit is included in the audited surface.
- The remediation applies to any generated review handoff, not only PRD or POST-reflect.
- The evidence packet includes runtime-entrypoint verification, contract-implementation enumeration, unmask-and-sweep results, and heterogeneous/off-path review input validation when such review is used.

## Non-goals

- Do not redesign the full pipeline.
- Do not require every task to commit before review.
- Do not make POST-reflect PRD-specific.
- Do not replace independent review with inline self-review.
- Do not accept model/session heterogeneity as sufficient without effective-input proof.
