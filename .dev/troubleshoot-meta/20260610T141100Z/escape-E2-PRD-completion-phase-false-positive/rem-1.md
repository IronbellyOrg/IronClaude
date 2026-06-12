# Remediation 1: Semantic-topology gate card

## Scope

This is an issue-agnostic remediation for generated-workflow validators. It is not a PRD patch and does not prescribe a PRD-only phase range or completion-heading heuristic.

## Problem class

A validator escaped because it enforced a syntactic shortcut against every matching section instead of validating the semantic role of the artifact sections it consumed. The immediate failure was a strict parallel-instruction check halting a generated task file whose final bookend phase was intentionally sequential, but the general failure mode is broader:

> A pipeline gate, parser, scanner, or semantic check is attached to generated artifacts without proving that its implementation scope matches the generator's artifact topology and runtime entrypoint.

This class applies to any generated workflow artifact with setup/work/completion sections, dynamic file names, declared-but-unused fields, subprocess arguments, monitor contracts, advisory-vs-strict severity, resume/run asymmetry, or parser regexes that can match off-plan headings.

## Evidence basis

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E2-PRD-completion-phase-false-positive/root-cause.md` identifies the generalized root cause as validators not being tested against the semantic topology of generated artifacts.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row `PRD-E05` records the specific miss: setup/completion bookends were intentionally sequential while the implementation checked every phase `>=2`.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 60-70 records that a live runtime generated work phases 2-6 and a sequential Phase 7 completion bookend.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 81-96 records the live halt and the rejected positional-only fix.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` lines 86-91 recommends runtime-entrypoint replay cards, contract ledgers, unmask sweeps, and targeted off-path review.

## Low-cost protocol gate

Add a mandatory **semantic-topology gate card** before closing any fix that changes or relies on a generated-artifact validator.

A fix is in scope when it touches any of these surfaces:

- gate criteria or semantic checks;
- parsers/scanners over generated markdown, JSON, YAML, stdout, logs, or task files;
- prompt/template sections consumed by code;
- declared file naming, artifact resolution, persisted state, monitors, or resume/run behavior;
- CLI/subprocess command assembly or environment-dependent runtime entrypoints;
- severity changes such as strict halt, advisory warning, or asynchronous trailing gate behavior.

The card is intentionally small enough to fit in a PR description, task file, or troubleshooting report. It should be completed with concrete names, not prose assurance.

```text
Semantic-topology gate card

1. Runtime entrypoint replay
   - Production command or entrypoint:
   - Process boundary crossed, if any:
   - Required/forbidden environment assumptions:
   - Artifact producer:
   - Artifact consumer/gate:
   - Does the test/mock cross the same boundary as production? yes/no; if no, why sufficient:

2. Contract-implementation enumeration
   - Declared contract items: <flags, fields, filenames, sections, predicates, severity bits, persisted keys, monitor events>
   - Live implementation consumers for each item:
   - Dead/unused items intentionally retained:
   - Docstring/spec/template claims that constrain implementation scope:

3. Semantic topology fixture
   - Representative generated artifact shape:
   - Sections/records that must be included:
     - setup or prelude bookend, if applicable;
     - at least one true executable/work item that should fail when violating the validator;
     - at least one true executable/work item that should pass;
     - completion/summary/bookend section, if applicable;
     - off-plan headings/placeholders/log sections that parser must ignore, if applicable.
   - Expected pass/fail matrix:

4. Unmask-and-sweep
   - Anchor bug pattern:
   - Sibling patterns searched:
   - Similar gates/parsers/templates checked:
   - False-positive cases added:
   - False-negative cases added:

5. Off-path review decision
   - Required if the bug crosses CLI, subprocess, filesystem, persisted state, generated artifacts, or strict-halt severity.
   - Reviewer/probe used:
   - If skipped, explicit reason it is unnecessary:
```

## Required invariants

1. **Runtime-entrypoint verification:** At least one verification step must exercise the same command/entrypoint and boundary where the bug manifests, unless the card explicitly proves a narrower test is equivalent. Source-level command construction tests are not enough when production behavior depends on subprocess semantics, environment, persisted state, or generated disk artifacts.

2. **Contract-implementation enumeration:** Every declared contract item must be mapped to a live implementation consumer. This includes flags, prompt sections, filename patterns, artifact paths, semantic-check fields, severity bits, parser scope, persisted state, and monitor events. A mismatch between a docstring/spec/template and code is a failing signal, not a comment to defer.

3. **Semantic topology over positional shortcuts:** Validators must key on artifact role or declared structure when role matters. Positional or regex shortcuts are allowed only after a representative generated-artifact fixture proves they do not include setup/completion bookends, logs, placeholders, examples, or other off-plan sections.

4. **Unmask-and-sweep after anchor bug:** A discovered false positive or false negative must trigger a sibling sweep before closure. The sweep must look for the same parser assumption, static map, unused field, severity mismatch, stdout-vs-disk confusion, resume/run divergence, or mock-vs-runtime gap elsewhere in the pipeline.

5. **Heterogeneous off-path review when risk justifies it:** If a strict gate can halt a live run, or if the bug crosses generated artifacts plus runtime state, require an adversarial/off-path reviewer or invariant probe. The review should test the contract boundary, not merely debate local fix options.

## Acceptance criteria

A remediation or fix for this class is not complete until all of the following are true:

- The semantic-topology gate card is present in the task/PR/troubleshoot artifact.
- The runtime entrypoint and the test entrypoint are named, and any boundary mismatch is justified.
- The contract ledger lists all relevant declared fields, predicates, files, parser scopes, and severity bits with live consumers.
- A representative generated-artifact fixture includes both valid non-work/bookend content and invalid executable-work content.
- The fixture proves both false-positive resistance and false-negative enforcement.
- An unmask sweep records sibling parser/gate/template surfaces searched and the result.
- Strict-halt validators either have off-path review evidence or an explicit downgrade/advisory rationale tied to cost asymmetry.

## Minimal implementation path

1. Add this card template to the troubleshooting or task-builder protocol used for pipeline escapes.
2. Require it only for generated-artifact validator changes and runtime-bound pipeline fixes; do not burden pure typo or documentation-only changes.
3. Add one repository test/helper convention: generated-artifact validator tests must include a pass/fail matrix covering bookends, real work items, and off-plan parser decoys.
4. During review, reject any fix whose proof is only local to the observed case. The proof must generalize to the validator's declared contract and sibling surfaces.

## Non-goals

- Do not hard-code PRD-specific phase numbers.
- Do not require all validators to become advisory.
- Do not mandate heavyweight end-to-end runs for every small parser edit.
- Do not require heterogeneous review for low-risk, non-runtime, non-strict changes when the card explains why local contract tests are sufficient.
