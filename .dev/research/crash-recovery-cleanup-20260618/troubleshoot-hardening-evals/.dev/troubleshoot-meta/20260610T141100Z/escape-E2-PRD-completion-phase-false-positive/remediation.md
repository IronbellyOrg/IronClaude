# Remediation: semantic-topology contract gate for generated-workflow validators

## Escape covered

- **Escape id:** `E2-PRD-completion-phase-false-positive`
- **Symptom:** a strict generated-workflow gate halted a live PRD task-file run because it applied a parallel-instruction requirement to the final sequential completion/presentation bookend.
- **Fix reference:** PR #154 / `e97aa4fd2a9d317abdc19f6ce2b5ccd35497df0e`
- **Root-cause artifact:** `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E2-PRD-completion-phase-false-positive/root-cause.md`

## Generalized problem class

A validator escaped because it enforced a syntactic shortcut against every matching section instead of proving that its implementation scope matched the semantic topology of the generated artifact and the runtime entrypoint that consumes it.

The durable failure mode is issue-agnostic:

> A pipeline gate, parser, scanner, or semantic check is attached to generated artifacts without proving that its runtime scope, parser boundary, severity, and tests match the generator's artifact topology and consumer contract.

This applies to generated workflow artifacts with setup/work/completion sections, dynamic file names, declared-but-unused fields, subprocess arguments, persisted state, monitor contracts, advisory-versus-strict severity, resume/run asymmetry, or parser regexes that can match off-plan headings, placeholders, examples, logs, or guard prose.

## High-catch-power rule

Any pipeline gate, scanner, parser, or validator that can block a live generated workflow MUST be verified as a runtime contract between the generator, the persisted artifact, the parser scope, the gate severity, and every implementation surface that consumes or emits the same contract.

It is not sufficient to test the helper rule in isolation, patch only the observed failing example, or encode positional assumptions such as phase numbers when the real invariant is semantic role.

## Mandatory semantic-topology gate card

Before closing any fix that changes or relies on a generated-artifact validator, complete this card with concrete names. It is intentionally small enough to fit in a PR description, task file, or troubleshooting report.

A fix is in scope when it touches any of these surfaces:

- gate criteria or semantic checks;
- parsers/scanners over generated markdown, JSON, YAML, stdout, logs, or task files;
- prompt/template sections consumed by code;
- declared file naming, artifact resolution, persisted state, monitors, or resume/run behavior;
- CLI/subprocess command assembly or environment-dependent runtime entrypoints;
- severity changes such as strict halt, advisory warning, or asynchronous trailing gate behavior.

```text
Semantic-topology gate card

1. Runtime entrypoint replay
   - Production command or entrypoint:
   - Process boundary crossed, if any:
   - Required/forbidden environment assumptions:
   - Artifact producer:
   - Persisted artifact path or shape:
   - Artifact consumer/gate registry:
   - Gate severity outcome asserted: continue/warn/halt
   - Does the test/mock cross the same boundary as production? yes/no; if no, why sufficient:

2. Contract-implementation enumeration
   - Semantic contract in role terms:
   - Declared contract items: <flags, fields, filenames, sections, predicates, severity bits, persisted keys, monitor events>
   - Live implementation consumers for each item:
   - Producers/transformers/recovery paths for each item:
   - Dead/unused items intentionally retained:
   - Docstring/spec/template claims that constrain implementation scope:
   - Disagreements converted to executable assertions or documented exceptions:

3. Semantic topology fixture
   - Representative generated artifact shape:
   - Sections/records included:
     - setup or prelude bookend, if applicable;
     - at least one true executable/work item that should fail when violating the validator;
     - at least one true executable/work item that should pass;
     - completion/summary/bookend section, if applicable;
     - off-plan headings, placeholders, examples, comments, logs, emitted guard prose, malformed variants, or parser decoys that must be ignored or handled.
   - Expected pass/fail matrix:
   - Negative control that fails for the intended reason:

4. Unmask-and-sweep
   - Anchor bug pattern:
   - Sibling parser/gate/template/pipeline surfaces searched:
   - Similar regex/static-map/unused-field/severity/stdout-vs-disk/resume-vs-run/mock-vs-runtime assumptions checked:
   - False-positive cases added:
   - False-negative cases added:
   - Severity re-evaluation result:

5. Off-path review decision
   - Required if the bug crosses CLI, subprocess, filesystem, persisted state, generated artifacts, cross-pipeline contracts, parser scope, or strict-halt severity.
   - Reviewer/probe used:
   - Plausible false positive identified:
   - Plausible false negative identified:
   - Fixture faithfulness to live generator checked:
   - If skipped, explicit reason local contract tests are sufficient:
```

## Required invariants

1. **Runtime-entrypoint verification:** At least one verification step must exercise the same command/entrypoint, gate registry, parser, persisted artifact, and severity mapping used by production or dogfood runs. Source-level helper tests are not enough when behavior depends on subprocess semantics, environment, filesystem artifacts, persisted state, or generated disk output.

2. **Contract-implementation enumeration:** Every declared contract item must be mapped to a live producer, transformer, recovery path, and consumer. This includes flags, prompt sections, filename patterns, artifact paths, semantic-check fields, severity bits, parser scope, persisted state, monitor events, and documentation/template claims. Any mismatch is a failing signal unless explicitly documented as an owned exception with rationale.

3. **Semantic topology over positional shortcuts:** Validators must key on artifact role or declared structure when role matters. Positional or regex shortcuts are allowed only after a representative generated-artifact fixture proves they do not include setup/completion bookends, logs, placeholders, examples, comments, or other off-plan sections.

4. **Full-artifact false-positive and false-negative proof:** The fixture must represent the full generated artifact shape, not a trimmed snippet. It must prove both that valid non-target sections are not blocked and that invalid executable/work sections are still caught for the intended reason.

5. **Unmask-and-sweep after anchor bug:** A discovered false positive or false negative must trigger a sibling sweep before closure. The sweep must look for adjacent parser matches, static maps, unused fields, severity mismatches, stdout-vs-disk confusion, resume/run divergence, mock-vs-runtime gaps, artifact lookup assumptions, malformed variants, and sibling pipeline contracts.

6. **Severity cost re-evaluation:** If a heuristic's false-positive cost is higher than the behavior it prevents, downgrade to advisory or require stronger evidence before HALT. Strict validators must explicitly prove halt/warn/continue behavior.

7. **Heterogeneous off-path review for high-risk gates:** If a strict gate can halt a live run, or if the bug crosses generated artifacts plus runtime state, require an adversarial/off-path reviewer or invariant probe targeted at the contract boundary. The reviewer must identify at least one plausible false positive and one plausible false negative and check whether the fixture is produced by, or faithful to, the live generator.

## Acceptance checklist for future fixes

A generated-workflow validator fix is not complete until the PR/task/troubleshooting evidence answers yes to all of these:

1. Is the semantic-topology gate card present?
2. Did verification run the same runtime entrypoint and gate registry that production/dogfood runs use, or justify an equivalent narrower test?
3. Does the fixture represent a full generated artifact, including setup, work, completion, logs/placeholders/examples, and other non-target sections the parser may see?
4. Are pass and fail cases tied to semantic roles rather than brittle positions?
5. Does at least one negative control fail for the intended reason?
6. Are all producers, transformers, recovery paths, parser boundaries, templates, docs, tests, severity mappings, and consumers enumerated?
7. Were disagreements converted to executable assertions or explicit documented exceptions?
8. Did the fix sweep adjacent parser matches and unmasked failure modes after the immediate anchor bug?
9. Were both false-positive resistance and false-negative enforcement added to tests or equivalent verification?
10. Was gate severity re-evaluated for cost asymmetry, with halt/warn/continue behavior asserted explicitly?
11. Did an off-path reviewer or invariant probe inspect the contract boundary when the change involved strict HALT behavior, runtime artifacts, parser scope, or cross-pipeline contracts?

If any answer is no, the remediation is incomplete and should not be accepted as issue-agnostic.

## Minimal implementation path

1. Add the semantic-topology gate card template to the troubleshooting/task-builder protocol used for pipeline escapes.
2. Require the card only for generated-artifact validator changes and runtime-bound pipeline fixes; do not burden pure typo, documentation-only, or low-risk local edits.
3. Establish a repository test/helper convention: generated-artifact validator tests must include a pass/fail matrix covering bookends, real work items, and parser decoys.
4. For blocking gates, require one runtime-entrypoint replay that asserts continue/warn/halt outcome through the real gate registry.
5. During review, reject fixes whose proof is only local to the observed case. The proof must generalize to the declared contract and sibling surfaces.

## Evidence basis

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E2-PRD-completion-phase-false-positive/root-cause.md` identifies the generalized root cause as validators not being tested against the semantic topology of generated artifacts.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row `PRD-E05` / `PRD-E05-final-phase-false-positive` records the missed template-phase contract and implementation-scope gap.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 60-70 record the live halt, generated work phases, sequential completion bookend, and rejection of a purely positional fix.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 81-96 confirm the generated-artifact boundary and role-sensitive exemption.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` lines 86-91 recommends runtime-entrypoint replay cards, contract ledgers, unmask sweeps, and targeted off-path review.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` lines 21-28 identify the broader meta-pipeline principles: runtime-entrypoint verification, contract-implementation enumeration, and unmask-and-sweep.

## Cost posture

This remediation intentionally favors a lightweight card plus targeted fixtures over mandatory heavy end-to-end testing for every parser change. Cost scales with risk:

- **Low risk:** local contract tests plus completed card may be enough.
- **Generated artifact or runtime boundary:** require representative full-artifact fixture and entrypoint replay or explicit equivalence proof.
- **Strict HALT, persisted state, subprocess, filesystem, resume/run, or cross-pipeline contract:** require off-path review/invariant probe and explicit severity cost analysis.

The goal is maximum defect-catch power per unit cost: force role-aware fixtures, real runtime boundaries, and sibling sweeps where false positives or false negatives can halt live work, while avoiding heavyweight process for purely local or non-blocking changes.

## Non-goals

- Do not hard-code PRD-specific phase numbers.
- Do not define completion phases as universally exempt.
- Do not require all validators to become advisory.
- Do not mandate heavyweight end-to-end runs for every small parser edit.
- Do not require heterogeneous review for low-risk, non-runtime, non-strict changes when the card explains why local contract tests are sufficient.
