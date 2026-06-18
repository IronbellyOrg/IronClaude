# Remediation: effective-input proof for generated review gates

## Remediation rule

Any pipeline step that generates, schedules, or delegates an independent review must prove that the reviewer consumed the same work surface produced by the runtime entrypoint it is reviewing. A review gate is not valid merely because it exists, is off-path, invokes the intended command, or returns a PASS artifact.

For every generated review handoff that accepts a VCS selector, path selector, artifact selector, or other input indirection, the pipeline must require an **effective-input proof**:

1. Enumerate the concrete files, commits, artifacts, or records changed by the real runtime entrypoint.
2. Enumerate the concrete files, commits, artifacts, or records consumed by the generated review command.
3. Block unless the review input includes the runtime-produced work and excludes known foreign work.
4. Preserve the proof as an artifact that a later audit can inspect without trusting command text.

## Why this catches E5 and adjacent escapes

E5 was not caused by missing reflect wiring. The generated POST-reflect item existed and invoked `/sc:reflect`, but its diff selector was commit-centric while `/task` commonly leaves work as uncommitted working-tree edits. The generated range could therefore review no task work, or review unrelated commits. The missing invariant was: **the reflect artifact must prove the effective diff matched the task's actual runtime changes.**

This rule generalizes beyond POST-reflect and beyond PRD. The same failure class exists whenever a generator emits a downstream gate that references work indirectly: commit ranges, merge bases, globs, canonical output paths, stream captures, cached artifacts, resume metadata, or model-produced filenames.

## Required pipeline controls

### 1. Runtime-entrypoint verification

Tests and release gates must exercise the entrypoint operators actually use, not only prompt builders, source helpers, or command-string construction.

For generated task review gates, at least one blocking dogfood test must:

- generate the task or handoff through the real builder path;
- execute or faithfully harness the real runtime entrypoint that mutates disk state;
- leave representative work uncommitted when that is allowed by the runtime;
- run the generated review item exactly as emitted; and
- assert the review's effective input set, not just command presence or verdict text.

If the runtime supports dirty working trees, staged-only changes, resumed runs, or interleaved commits, those states must be explicit fixtures. A commit-only fixture is insufficient unless the runtime contract requires commits.

### 2. Contract-implementation enumeration

For each pipeline contract, enumerate every implementation and consumption surface before declaring the contract covered.

For review gates, the enumeration must include:

- the generator that emits the review item;
- the runtime entrypoint that produces the work;
- metadata captured at start/resume time;
- the command or skill invoked by the review item;
- the review tool's actual diff/artifact resolution behavior;
- artifacts used as proof after the review; and
- scanner or validation surfaces that may inspect generated output rather than source text.

Coverage is incomplete if it verifies only one of these surfaces. In E5 terms, checking that task-builder emitted `/sc:reflect` was not enough; the contract also needed to verify how `/task` leaves changes and how `/sc:reflect` resolves the supplied diff.

### 3. Effective-input invariant

Every off-path review artifact must include a machine-checkable effective-input summary. For diff-based reviews, this should include at minimum:

- requested selector or command input;
- resolved base and head or resolved working-tree basis;
- changed-file list consumed by the reviewer;
- whether staged and unstaged changes were included;
- excluded commits or files when a foreign-work fixture is present; and
- enough metadata to reproduce the selector resolution.

The gate must fail closed when the effective-input summary is absent, empty despite known runtime changes, or includes known foreign work.

### 4. Unmask-and-sweep after any escape

A fix for a wrong selector, wrong base, wrong path, wrong output stream, or wrong artifact reader must trigger a sweep for sibling selectors across the pipeline. The sweep should search for the same assumption expressed in other forms, not only the exact broken token.

For E5-class failures, sweep for:

- commit ranges emitted by generated task or review text;
- references to task-start `HEAD` as an audit boundary;
- review gates that accept `--diff`, path globs, or cached artifacts without proving effective input;
- tests that assert command construction but do not run the runtime entrypoint; and
- PASS artifacts that do not record what was actually reviewed.

The remediation is not complete until the sweep either adds coverage or records why each sibling surface is not susceptible.

### 5. Heterogeneous off-path review, with input proof

Off-path review remains valuable only when it is both executor-disjoint and input-correct. When supported by the pipeline, use a heterogeneous reviewer path: different session, different agent/reviewer identity, and where available a different model class or review mechanism. However, heterogeneity must not substitute for input proof.

A heterogeneous reviewer that points at the wrong diff is still a false audit. The release gate must therefore require both:

- reviewer independence from the executor that produced the work; and
- effective-input proof that the reviewer audited the runtime-produced work surface.

## Minimal blocking regression for this escape class

Add a dogfood regression that creates a generated review gate and verifies these cases:

1. **Dirty work included:** runtime edits tracked files without committing; generated review effective diff includes those files.
2. **Foreign commit excluded:** an unrelated commit exists after task start; generated review effective diff excludes files touched only by that commit.
3. **Empty-diff fail closed:** if known runtime changes exist but the review resolves an empty diff, the gate fails with a typed reason.
4. **Artifact proof required:** deleting or corrupting the review effective-input summary fails validation even if the review verdict says PASS.

This regression should be issue-agnostic: the changed files can be synthetic fixtures, but the producer and review handoff must use the same runtime semantics as production.

## Acceptance criteria

- Generated review gates cannot pass without an effective-input summary.
- Runtime-entrypoint e2e coverage exists for dirty working-tree review semantics.
- Contract enumeration maps generator, runtime producer, selector resolver, reviewer, and artifact validator for the review gate.
- A negative fixture proves foreign work is excluded.
- A negative fixture proves empty or missing effective input fails closed.
- The remediation sweep records sibling review selectors and whether each is covered or not applicable.

## Non-goals

- Do not patch only the PRD or POST-reflect instance.
- Do not rely on commit discipline unless the runtime contract requires commits.
- Do not accept command-string assertions as proof that review coverage is correct.
- Do not treat a PASS verdict from an independent reviewer as sufficient when the reviewed input set is unproven.
