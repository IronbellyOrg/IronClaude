# Remediation 1: Low-cost protocol gate for runtime contract escapes

Escape ID: `E1-PRD-cloud-file-misuse`

## Remediation objective

Prevent pipeline fixes from closing on source-level or unit-level proof when the escape class lives at a runtime boundary, shared contract seam, or sibling-pipeline divergence.

This is not a PRD-specific patch. PR #151 already fixed the observed PRD implementation by removing local-path delivery through `claude --file` and inlining specs/refs. The pipeline remediation is a protocol gate that applies to any CLI pipeline, agent pipeline, validation pipeline, or generated-task workflow where an implementation crosses an entrypoint, subprocess, filesystem, persisted-state, or producer/consumer contract boundary.

## Gate name

**Runtime Contract Sweep Gate**

## When the gate is required

Require this gate before marking a remediation, troubleshoot report, reflect report, or task-builder fix complete when any of the following are true:

1. The defect was observed only through a runtime entrypoint, subprocess, CLI invocation, resume path, generated artifact, or persisted state.
2. The fix changes command arguments, file delivery, artifact paths, environment assumptions, generated output contracts, gate criteria, or producer/consumer wiring.
3. A sibling pipeline already implements the same conceptual contract differently.
4. Tests or review primarily inspect helpers, command construction, mocks, markdown output, or local source surfaces rather than the failing runtime seam.
5. A single anchor bug plausibly indicates a family of related defects.

## Required protocol card

Every applicable fix must include a short `Runtime Contract Sweep` card in the task log, review report, or remediation report.

Template:

```markdown
## Runtime Contract Sweep

### 1. Runtime-entrypoint verification
- Production entrypoint:
- Exact command or equivalent replay:
- Boundary crossed: [subprocess | filesystem | persisted state | generated artifact | external CLI | other]
- Environment assumptions included:
- Evidence that the replay reaches the same boundary as production:
- If not replayed, reason and faithful substitute:

### 2. Contract-implementation enumeration
- Contract name:
- Producers:
- Consumers:
- Shared helpers / sibling pipelines checked:
- Forbidden or deprecated mechanisms:
- Guard added or existing guard cited:

### 3. Unmask-and-sweep
- Anchor failure:
- Sibling patterns searched:
- Search method:
- Additional hits:
- Disposition for each hit:

### 4. Off-path review decision
- Does this cross a runtime/process/filesystem/persisted-state boundary?
- If yes, heterogeneous/off-path review or targeted runtime smoke used:
- If no, why Tier 1/local review is sufficient:
```

## Pass criteria

The gate passes only when all four sections are answered with concrete evidence.

### 1. Runtime-entrypoint verification

The fix must execute, or faithfully model, the same boundary that failed in production.

Minimum evidence:

- The named entrypoint is the operator-facing or pipeline-facing entrypoint, not only a helper.
- The replay includes relevant environment absences or presences that affect behavior.
- The replay reaches the process/file/state boundary where the original defect became visible.
- The result has a failure-specific assertion, not only a broad success check.

For this escape class, the missing evidence was a headless pipeline run with no session token reaching the Claude subprocess boundary. Generalized, the missing evidence is any runtime replay that proves the real process contract accepts the implementation's inputs.

### 2. Contract-implementation enumeration

The fix must enumerate the contract across producers, consumers, and sibling implementations.

Minimum evidence:

- List every producer of the contract value: CLI flag, generated file, prompt section, persisted JSON field, subprocess arg, gate criterion, static map entry, monitor, or recovery path.
- List every consumer that interprets the value.
- Identify sibling pipelines or shared helpers that implement the same conceptual contract.
- State whether any mechanism is forbidden, deprecated, cloud-only, local-only, runtime-only, or mock-only.
- Add or cite at least one guard that prevents recurrence across the whole contract family.

For this escape class, the sibling sweep would have found that roadmap/tasklist/validate already forbade local-file delivery through `--file` while PRD still emitted it. Generalized, a fix cannot be accepted until the implementation is compared to sibling contract owners.

### 3. Unmask-and-sweep

The fix must treat the observed bug as an anchor, not a one-off.

Minimum evidence:

- Search for the same pattern outside the immediate file or feature.
- Include both implementation and generated-output surfaces when relevant.
- Include run/resume asymmetries, static-vs-dynamic maps, stdout-vs-disk fallbacks, mock-vs-runtime divergence, declared-but-unused fields, and hard-coded parser assumptions when those pattern families apply.
- Record all hits and dispositions: fixed now, already guarded, irrelevant with reason, or follow-up with owner/path.

For this escape class, the low-cost sweep was a cross-pipeline guard proving no local filesystem path is delivered via a cloud/session-token-only file mechanism. Generalized, a closeout that fixes only the observed command without searching sibling surfaces fails the gate.

### 4. Heterogeneous off-path review

The fix must explicitly decide whether local/Tier 1 review is enough.

Minimum evidence:

- If the bug crosses a subprocess, runtime entrypoint, filesystem, persisted-state, generated-artifact, or external-tool boundary, require either:
  - a targeted runtime smoke/e2e at that boundary, or
  - an off-path reviewer/adversarial review focused on boundary mismatch and contract recurrence.
- If the bug is narrow enough for Tier 1, the report must explain why runtime/off-path review is unnecessary and cite deterministic evidence.

The lesson is not that every fix needs heavyweight review. The lesson is that cheap review is acceptable only when it covers the failing surface. Evidence in the artifact audit shows catches correlated with runtime replay, contract enumeration, unmask sweeps, and off-path/adversarial review; rubber-stamps correlated with local proof, narrow diff mapping, and mocks that bypassed the failing interface.

## Low-cost implementation path

This gate can be implemented without redesigning the pipeline:

1. Add the `Runtime Contract Sweep` card to troubleshoot/remediation/task templates used for pipeline escapes.
2. Add a reviewer checklist item: "Did the evidence execute or faithfully model the runtime boundary that failed?"
3. Add a second checklist item: "Did the fix enumerate sibling implementations of the same contract?"
4. Require one grep/semantic sweep per anchor bug for sibling recurrence.
5. Require an explicit off-path review decision when the failure crosses a runtime/process/filesystem/persisted-state boundary.

## Anti-patterns this gate rejects

- Unit tests that assert command construction while the real subprocess contract is never exercised.
- Review reports that prove the edited helper works but do not prove the production entrypoint uses it correctly.
- Fixes that patch one pipeline without checking sibling pipelines that implement the same contract.
- Mocks that bypass the real interface where the defect surfaced.
- Closeout evidence that says "tests pass" without naming the boundary, contract, and environment assumptions.
- Product-specific remediation that only prevents the PRD `--file` case and does not generalize to other local-vs-runtime contract mismatches.

## Evidence basis

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E1-PRD-cloud-file-misuse/root-cause.md` identifies the merged root cause: verification stopped at PRD's intended local-file abstraction rather than the headless Claude subprocess contract, and no sibling-pipeline sweep exposed PRD as the outlier.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row `PRD-E04-cloud-file-flag` names the missed catchers: headless `--spec` e2e with no session token plus a cross-pipeline guard proving no local path is delivered via `claude --file`.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` lines 1-16 records that PRD was the only pipeline emitting `--file`, while roadmap/tasklist/validate already forbade it.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` lines 49-63 records the same root cause and the implementation fix, supporting this remediation's decision not to propose another product patch.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` lines 14-19 shows the sequence from deterministic `--spec` ingestion to the later cloud-file/session-token crash, supporting the need to verify runtime delivery mechanisms rather than only the intended binding.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pipeline-artifact-audit.md` lines 38-45, 65-72, and 74-84 generalize the pattern as review surface mismatch: artifacts caught bugs when they replayed runtime paths, enumerated contracts, swept recurrence, or used off-path/adversarial review; artifacts rubber-stamped when they stayed on local source/test surfaces.

## Success signal

A future pipeline escape of this class should be caught before merge because the closeout artifact will be unable to answer the four required questions without exposing the mismatch:

1. What runtime boundary actually rejects or consumes this value?
2. Which producers and consumers share the contract?
3. Where else does the same pattern appear?
4. Who or what reviewed the off-path boundary if local tests did not execute it?
