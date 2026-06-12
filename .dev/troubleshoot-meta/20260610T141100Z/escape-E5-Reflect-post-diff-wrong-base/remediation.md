# Remediation: Effective-input proof for generated review gates

## Scope

This is an issue-agnostic pipeline remediation for any stage that generates, schedules, delegates, or validates an independent review over an indirectly selected work surface: VCS selectors, file lists, path globs, canonical artifacts, model-produced filenames, prompt inputs, runtime logs, cached metadata, resume state, or stream captures.

It is not a PRD-only or POST-reflect-only patch.

## Escape addressed

`E5-Reflect-post-diff-wrong-base` escaped because the pipeline verified that a POST-reflect review step existed and invoked the intended review command, but did not prove that the reviewer audited the same work surface produced by the real runtime entrypoint.

The generated review selector was commit-centric. The actual `/task` runtime can leave task work as uncommitted working-tree edits. As a result, the generated review could omit the task work entirely. If unrelated commits landed after the recorded task start point, it could also include foreign work. The missing invariant was not “reflect must be present”; it was “the reflect artifact must prove its effective input matched the runtime-produced changes and excluded unrelated changes.”

## Generalized failure class

A generated review handoff is unsafe when all of the following are true:

1. A generator emits a selector for downstream review or validation.
2. The selected surface is runtime-dependent rather than purely static.
3. The implementation entrypoint can produce uncommitted, staged, resumed, external, partial, streamed, cached, or otherwise non-commit-bounded state.
4. Validation checks command presence, syntax, reviewer identity, or PASS text instead of what the reviewer consumed.
5. Tests cover the prompt builder or helper in isolation but not the production entrypoint that operators actually run.

This class applies beyond diffs. The same escape can occur with wrong artifact paths, stale cached metadata, stdout-vs-file mismatches, recovery searches, resume selectors, parser sections mistaken for executable work, or model-produced filenames.

## Remediation rule

Any generated independent-review gate must include an **Effective Input Proof**. A review gate is invalid merely because it exists, is off-path, invokes the intended command, uses a different reviewer, or returns a PASS artifact.

The proof must be preserved as an auditable artifact and must answer four questions:

1. **Runtime entrypoint:** What command, skill, CLI path, or harness will an operator actually run?
2. **Runtime-produced surface:** What files, commits, artifacts, records, prompts, or logs can that entrypoint produce at runtime, including dirty working-tree state and resume behavior?
3. **Generated selector:** What selector or input did the pipeline emit for the reviewer after normal placeholder resolution?
4. **Effective input match:** What concrete files, commits, artifacts, records, or logs did the reviewer consume, and how was it proven to include runtime work while excluding known foreign work?

A PASS requires evidence, not assertion. Acceptable evidence includes a captured changed-file list, an effective-diff manifest, a generated command plus resolved-file manifest, a reviewer-consumed artifact manifest, or a negative fixture that fails before the fix and passes after it.

## Required controls

### 1. Runtime-entrypoint verification

Tests and release gates must exercise the entrypoint operators actually use, or a faithful harness that preserves the entrypoint's state semantics.

For `/task`-like flows, the harness must permit tracked-file edits without a commit. For CLI-driven flows, it must cross the same subprocess boundary when the defect class depends on CLI behavior. For resumed or recovery flows, it must use the same metadata and selector resolution behavior as the real resume path.

Builder-only tests are insufficient when the runtime entrypoint mutates disk state, leaves dirty work, resolves selectors, or writes artifacts differently from the builder.

### 2. Contract-implementation enumeration

For each generated review contract, enumerate every implementation and consumption surface before declaring coverage complete.

Minimum enumeration:

- generator that emits the review item or handoff;
- runtime entrypoint that produces the work;
- metadata captured at start, checkpoint, resume, or recovery time;
- command, skill, agent, or reviewer invoked by the review item;
- selector resolver used by the reviewer, including diff/artifact/path resolution behavior;
- proof artifact generated after review;
- scanner or validation gate that decides PASS/FAIL;
- recovery/resume path, if present.

Coverage is incomplete if it verifies only the generator text while skipping the runtime producer, selector resolver, reviewer-consumed surface, or artifact validator.

### 3. Effective-input invariant

Every generated review artifact must include a machine-checkable effective-input summary.

For diff-based reviews, record at least:

- requested selector or command input;
- resolved base and head, or resolved working-tree basis;
- whether dirty, staged, and unstaged changes were included;
- changed-file list consumed by the reviewer;
- expected runtime-touched files;
- excluded commits or files when a foreign-work fixture is present;
- command actually run after placeholder resolution;
- enough metadata to reproduce selector resolution.

For artifact-based reviews, record at least:

- requested artifact selector;
- canonical resolved path;
- whether stdout, NDJSON, logs, fallback search, or cached metadata was accepted or ignored;
- exact artifact consumed by the gate;
- malformed, missing, stale, or empty artifact behavior;
- enough metadata to reproduce artifact resolution.

The gate must fail closed when the effective-input summary is absent, empty despite known runtime changes, non-reproducible, or includes known foreign work.

### 4. Heterogeneous off-path review with input proof

Off-path review remains valuable, but only when it is both executor-disjoint and input-correct.

When supported by task criticality or prior escapes, the reviewer should be heterogeneous in reviewer identity, session, and where available model or review mechanism. However, heterogeneity must never substitute for effective-input proof. A different reviewer consuming the same wrong selector is still a false audit.

Release gates for high-impact or terminal reviews must require both:

- reviewer independence from the executor that produced the work; and
- effective-input proof that the reviewer audited the runtime-produced surface.

### 5. Unmask-and-sweep after selector escapes

A fix for any wrong selector, wrong base, wrong path, wrong output stream, stale cache, or wrong artifact reader must trigger a sibling-surface sweep. The sweep must search for the same assumption expressed in other forms, not only the exact broken token.

For E5-class failures, sweep for:

- commit ranges emitted by generated task or review text;
- references to task-start `HEAD` as an audit boundary;
- review gates accepting `--diff`, path globs, artifact paths, cached artifacts, or resume metadata without proving effective input;
- prompt selectors where CLI flags or inputs may not survive into the first model prompt;
- parser or gate selectors where non-executable sections can be mistaken for executable work;
- resume or recovery paths that use different selectors than fresh runs;
- tests that assert command construction but do not run the runtime entrypoint;
- PASS artifacts that do not record what was actually reviewed.

The remediation is incomplete until the sweep records each sibling surface as covered, unaffected with rationale, or requiring follow-up.

## Minimal blocking regression

Add one reusable dogfood regression for the escape class, not a PRD-only fixture.

Fixture shape:

1. Generate a task, pipeline artifact, or review handoff through the production builder path.
2. Execute the real runtime entrypoint, or a faithful harness preserving its disk-state semantics.
3. Mutate representative tracked files without committing them when the runtime allows dirty work.
4. Optionally create or simulate a foreign commit after the recorded start point.
5. Run the generated review handoff exactly as emitted after normal placeholder resolution.
6. Capture the review's effective-input manifest.
7. Assert that runtime-touched files are included.
8. Assert that foreign commits or unrelated files are excluded.
9. Assert that an empty effective diff fails closed when known runtime changes exist.
10. Assert that deleting or corrupting the effective-input summary fails validation even if the review verdict says PASS.
11. Fail if validation only proves command presence, PASS text, reviewer identity, or artifact existence.

The fixture should be reusable across PRD, task-builder, tasklist, roadmap, reflect-style, release-validation, and recovery workflows by swapping the entrypoint and selector type while preserving the effective-input assertion.

## Low-cost implementation plan

1. Add an `Effective Input Proof` subsection to review evidence templates, release gates, and troubleshooting remediation checklists.
2. Add a small reusable assertion helper that compares expected runtime-produced surfaces with reviewer-consumed surfaces.
3. Add the dogfood dirty-working-tree regression for generated terminal review handoffs.
4. Add negative cases for foreign work, empty effective input, and missing/corrupt proof artifacts.
5. Add an unmask-and-sweep checklist item to escape remediation closure.
6. Make missing proof a blocking validation failure for high-impact or terminal gates; allow advisory severity only for explicitly non-blocking review steps.

This plan intentionally avoids a large new framework. The highest leverage control is a small, mandatory proof artifact plus one production-semantics regression that prevents command-presence checks from masquerading as review coverage.

## Acceptance criteria

- Generated review gates cannot pass solely because a command exists, invokes the expected reviewer, or returns PASS.
- Every generated review artifact declares the concrete input surface consumed by the reviewer.
- Runtime-entrypoint coverage exists for dirty working-tree review semantics.
- The regression fails when runtime work is uncommitted and the generated selector is commit-range-only.
- The regression fails when known foreign work is included in the audited surface.
- The regression fails when known runtime changes produce an empty effective input.
- The regression fails when the effective-input proof is missing or corrupt even if the verdict says PASS.
- Contract enumeration maps generator, runtime producer, metadata capture, selector resolver, reviewer, proof artifact, validator, and resume/recovery path where applicable.
- The unmask-and-sweep record lists sibling selectors and marks each covered, unaffected with rationale, or requiring follow-up.
- Heterogeneous/off-path review, when used, is accepted only with effective-input proof.
- The remediation applies to generated review handoffs generally, not only PRD or POST-reflect.

## Non-goals

- Do not redesign the full pipeline.
- Do not require every task to commit before review unless the runtime contract already requires commits.
- Do not patch only the observed PRD or POST-reflect instance.
- Do not replace independent review with inline self-review.
- Do not accept command-string assertions as proof that review coverage is correct.
- Do not treat model, session, or reviewer heterogeneity as sufficient without effective-input proof.
