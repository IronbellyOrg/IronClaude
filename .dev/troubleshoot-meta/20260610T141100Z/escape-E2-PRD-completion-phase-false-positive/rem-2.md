# Remediation: issue-agnostic pipeline rule for generated-artifact gate escapes

## Escape covered

- **Escape id:** `E2-PRD-completion-phase-false-positive`
- **Symptom:** a STRICT `parallel_instructions` gate halted a live heavyweight PRD `build-task-file` run because the final sequential completion/presentation phase lacked parallel keywords.
- **Fix reference:** PR #154 / `e97aa4fd2a9d317abdc19f6ce2b5ccd35497df0e`
- **Root-cause artifact:** `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E2-PRD-completion-phase-false-positive/root-cause.md`

## High-catch-power system rule

Any pipeline gate, scanner, parser, or validator that can block a live generated workflow MUST be verified as a runtime contract between the generator, the persisted artifact, the parser scope, the gate severity, and every implementation that consumes or emits the same contract. It is not sufficient to test the helper rule in isolation or to patch the observed failing example.

Before a blocking gate change ships, the pipeline must prove all four checks below.

### 1. Runtime-entrypoint verification

Exercise the real entrypoint that operators use, not only the local helper or command-construction layer.

Required proof:

- Generate or load the representative artifact through the live workflow path.
- Feed the persisted artifact into the same gate registry, parser, and severity mapping used at runtime.
- Assert the operational outcome, including whether the workflow continues, warns, or halts.
- Include at least one negative control that should fail for the intended reason, not merely fail somewhere nearby.

For this escape class, the representative artifact must include valid non-target sections that resemble the parser's target syntax. A phase parser, for example, must be tested against a full generated task file, not only a trimmed phase snippet.

### 2. Contract-implementation enumeration

Enumerate the contract across every producer, transformer, parser, recovery path, and gate consumer before declaring the fix complete.

Required proof:

- Name the semantic contract in role terms, not just syntax. Example: enforce parallel instructions on executable work phases; do not enforce them on setup or completion bookends.
- List every implementation surface that depends on the contract.
- Compare documentation, templates, generated artifacts, parser boundaries, and tests for disagreement.
- Convert each discovered disagreement into either an executable assertion or an explicit documented exception with owner and rationale.

This prevents local fixes such as hard-coding a phase range when the durable invariant is actually role-based.

### 3. Unmask-and-sweep after the first fix

When a defect is caused by parser overreach, gate severity, generated-output scanning, artifact lookup, or runtime wiring, the first fix is not complete until adjacent false-positive and false-negative modes have been swept.

Required proof:

- Search for sibling syntactic surfaces that the same parser could accidentally match.
- Add adversarial fixtures for near-miss headings, placeholders, comments, logs, emitted guard prose, malformed artifacts, and short/long generated variants as applicable.
- Test both false positives and false negatives.
- Re-evaluate gate severity after the sweep. If a heuristic's false-positive cost is higher than the behavior it prevents, downgrade to advisory or require stronger evidence before HALT.

The PR #154 to PR #155 sequence is the cautionary pattern: fixing only the observed completion-phase false positive left the same strict parser able to halt on Task-Log placeholder headings hours later.

### 4. Heterogeneous off-path review targeted at the contract

Use off-path review when the change affects generated artifacts, runtime gates, strict HALT behavior, parser scope, or cross-pipeline contracts. The review must be aimed at the contract, not merely at the patch option.

Required proof:

- Give the reviewer the generated artifact topology and ask for contract violations, not style review.
- Require the reviewer to identify at least one plausible false positive and one plausible false negative for the gate.
- Require the reviewer to check whether the test fixture is produced by, or faithful to, the live generator.
- If multiple pipeline families share the contract, require a sibling-pipeline sweep.

Off-path review only has catch power when it reviews the runtime contract end to end. A debate over local fix options can still miss the broader generator/parser/gate mismatch.

## Acceptance checklist for future pipeline fixes

A pipeline fix that touches a blocking gate is not complete until the PR evidence answers yes to all of these:

1. Did we run the same runtime entrypoint and gate registry that production/dogfood runs use?
2. Did the fixture represent a full generated artifact, including setup, work, completion, logs, placeholders, and other non-target sections the parser may see?
3. Did we enumerate all producers and consumers of the contract, including templates, docs, parser code, gate severity, recovery, and sibling pipelines?
4. Did we add both pass and fail fixtures tied to semantic roles rather than brittle positions?
5. Did we sweep adjacent parser matches and unmasked failure modes after the immediate fix?
6. Did an off-path reviewer inspect the contract boundary and cost asymmetry, not only the code diff?
7. Did we verify the halt/warn/continue outcome explicitly?

If any answer is no, the remediation is incomplete and should not be accepted as issue-agnostic.

## Evidence basis

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row `PRD-E05-final-phase-false-positive` identifies the missed template-phase contract and the gap between the documented phase range and implementation scope.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 60-70 records the live HALT, the actual phase topology, and why a pure positional fix was rejected.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 81-96 confirms the same generated-artifact boundary and role-sensitive exemption.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` lines 21-28 show the broader meta-pipeline principles: runtime-entrypoint verification, contract-implementation enumeration, and unmask-and-sweep.

## Non-goals

This remediation is not a PRD-only patch, a rule that completion phases are always exempt, or a hard-coded phase-number policy. The durable rule is broader: blocking validators for generated workflows must be proven against the runtime artifact contract and then swept for adjacent parser and severity failures before release.
