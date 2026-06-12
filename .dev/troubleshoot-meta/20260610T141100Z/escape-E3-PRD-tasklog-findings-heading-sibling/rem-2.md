# Remediation: whole-artifact validator contract rule

## Scope

This is an issue-agnostic pipeline remediation for parser/gate/validator escapes where a fix handles the observed failing section but does not prove that the validator's runtime input domain, classification boundary, and halt severity are correct. It is not a PRD-specific patch and must be applied to any pipeline component that validates generated artifacts, generated task files, CLI outputs, persisted state, or other structured-by-convention text.

## High-catch-power system rule

When a pipeline defect involves a gate, parser, scanner, validator, recovery lookup, or artifact consumer, the fixing workflow must prove the contract at the live runtime entrypoint before merge:

1. **Runtime-entrypoint verification:** exercise or model the same production boundary that failed, including the real command shape, subprocess/file handoff, artifact path, generated full artifact, and gate invocation. Reduced unit fixtures are allowed only after the runtime input surface has been captured.
2. **Contract-implementation enumeration:** enumerate every producer, consumer, and severity decision for the contract being validated. For a generated artifact validator, this means listing all generated sections/headings/fields that can match the parser, not only the intended executable subset.
3. **Unmask-and-sweep:** treat the first fixed symptom as an anchor for a family sweep across sibling surfaces. Search for adjacent headings, fields, filename patterns, status enums, persisted keys, CLI flags, recovery paths, and mock/runtime divergences that satisfy the same matcher or contract assumption.
4. **False-positive and false-negative adversarial suite:** add representative full-artifact cases that include both intended matches and off-path sibling content. Assertions must be classification-oriented: what is eligible for enforcement, what is ignored, and what failure mode is acceptable.
5. **Severity review:** if the validator is heuristic or convention-based, explicitly compare false-positive cost against false-negative cost. A check that guards performance, style, or execution efficiency should not hard-halt long runs unless a missed failure produces incorrect or unsafe output.
6. **Heterogeneous off-path review when evidence supports it:** route the changed contract through a reviewer or lens that did not author the fix, and require that review to inspect the artifact topology/runtime boundary, not just the local code diff or the observed symptom.

## Required remediation gate

Before closing any follow-up fix in this class, the pipeline owner must attach a short validation card with these fields:

- **Runtime entrypoint:** exact live command/function boundary and the artifact bytes or generated file shape consumed by the validator.
- **Contract ledger:** declared contract, all producers, all consumers, severity, and the owner of each assumption.
- **Matcher/enforcement domain:** every syntactic surface the parser can consume, including non-executable or placeholder sections.
- **Sibling sweep result:** evidence that analogous surfaces were tested or intentionally excluded.
- **Adversarial fixtures:** at least one full generated artifact with valid intended content plus off-path sibling content that resembles the matcher.
- **Severity decision:** STRICT, advisory, or disabled, with false-positive/false-negative cost rationale.

A fix that only adds another special-case exclusion for the latest observed heading, field, or status is incomplete unless this card proves the full matcher domain has been swept.

## Why this would have caught E3

The escaped failure was not that one Task Log heading needed a local exclusion. The runtime gate scanned a whole generated MDTM task file with a loose phase-heading matcher, so headings outside the executable phase plan were part of the live enforcement domain. A runtime-entrypoint fixture using the full generated task file would have exposed that `### Phase 2 - Codebase Research Findings` was classified like a work phase. Contract enumeration would have forced the Task Log headings into the ledger. Unmask-and-sweep would have followed the #154 completion-phase fix into all other generated `Phase N` heading surfaces. The severity review would have challenged a hard halt for a parallelism heuristic whose false positive cost was a stopped long run while a miss usually only causes slower execution.

## Generalized implementation guidance

- Prefer structured producer output or explicit section markers over regex inference from whole documents.
- If regex inference remains, constrain it to the smallest semantically valid region and test every sibling region that can syntactically match.
- Keep hard gates for correctness, safety, data loss, or contract impossibility. Use advisory warnings for brittle heuristics, style/performance hints, and checks whose false positives are more damaging than misses.
- Regression tests must include the production-sized artifact shape, not only minimal strings that reproduce the visible symptom.
- Reviews must ask, "What else can this matcher consume?" and "What happens if this check is wrong?" before accepting a parser/gate fix.

## Evidence basis

- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/escape-E3-PRD-tasklog-findings-heading-sibling/root-cause.md` identifies the root cause as whole-artifact scan scope, broad `Phase N` discovery, and hard severity.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/defect-escape-table.md` row `PRD-E06` records the missed unmask-and-sweep over all generated task sections and the required parser-focused full MDTM sweep.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-targets-summary.txt` records that PR #155 followed two hard-halt false positives and changed only `parallel_instructions` to advisory.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/pr-broader-summary.txt` states the cost asymmetry: false positives halted long runs while the protected failure mode was slower serial execution.
- `/config/workspace/IronClaude/.dev/troubleshoot-meta/20260610T141100Z/timeline.md` places PR #154 and PR #155 as sequential escapes on the same gate, proving that observed-case patching did not sweep the family.
