# Protocol Targets Research

Status: Complete

## Scope

Assigned source files reviewed:

- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md`
- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md`
- `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`

## Findings by requested protocol target

### 1. Context anchor extraction

**Current evidence**

- Wave 1 classifies domain and strategy, then moves directly into dialogue and seed brief synthesis; there is no explicit context-anchor extraction step in the Wave 1 behavior list (`SKILL.md:122-167`).
- The domain taxonomy already treats file paths, language extensions, functions/classes/modules/endpoints, and dev verbs paired with code entities as code-domain signals (`refs/socratic-templates.md:11-16`). This is the closest existing anchor-related logic, but it is classification-only.
- Codebase enrichment currently tells Auggie to query using raw `{topic}` and `{topic_domain_area}` (`refs/handoff-routing.md:18-20`), but no normalized anchor set is produced before enrichment.

**Exact change targets**

1. Add a Wave 1 step in `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` between current steps 3 and 4 (`SKILL.md:124-129`) or immediately before seed brief synthesis (`SKILL.md:136`) to extract and cache `context_anchors` from:
   - `@file` references
   - absolute/relative paths
   - function/class/module/endpoint names
   - project/component names
   - explicit constraints or user-named systems
2. Add a new section to `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md` after `§Synthesis-Rules` (`refs/socratic-templates.md:212-222`) named `§Context-Anchor-Extraction`.
3. Update `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` codebase enrichment queries (`refs/handoff-routing.md:18-20`) to use the normalized `context_anchors` first, with raw topic as fallback only.

**Recommended contract addition**

`context_anchors` should be a deterministic list of objects, not free prose:

```yaml
context_anchors:
  - type: file|symbol|endpoint|component|concept|constraint
    value: <verbatim extracted anchor>
    source: topic|dialogue|enrichment
    confidence: high|medium|low
```

[UNVERIFIED] Runtime implementation behavior beyond the assigned source-of-truth protocol Markdown files was not inspected; this is not a tasklist-generation blocker because the requested remediation targets are the protocol docs and eval artifacts listed in the scope map.

### 2. Seed brief schema

**Current evidence**

- The seed brief schema is embedded directly in Wave 1 and currently includes frontmatter fields `topic`, `domain`, `strategy`, `depth`, `proposals_target`, `handoff_target`, and `created` (`SKILL.md:136-147`).
- The body currently requires `Problem Statement`, `Known Context`, `Constraints`, `Success Criteria`, and `Open Questions` (`SKILL.md:149-165`).
- The synthesis rules define how to populate those sections, with a 1500-token max and guidance to reference enrichment artifacts by path rather than inline (`refs/socratic-templates.md:214-222`).
- Enrichment appends an `## Enrichment Context` section later (`SKILL.md:198`).

**Exact change targets**

1. Extend the seed brief YAML block in `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` at `SKILL.md:138-147` with stable schema fields:
   - `schema_version: "1.0"`
   - `intent_summary: <one sentence>`
   - `context_anchors: [...]`
   - `must_preserve: [...]`
   - `out_of_scope: [...]`
   - `source_confidence: high|medium|low`
2. Extend the body template at `SKILL.md:149-165` with dedicated sections:
   - `## Intent Summary`
   - `## Context Anchors`
   - `## Must Preserve`
   - `## Out of Scope`
3. Extend `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md` synthesis rules (`refs/socratic-templates.md:214-222`) to define how dialogue answers map into the new fields.

**Reason this is a target**

The current schema captures problem/context/constraints but does not provide a stable, machine-checkable seed brief schema for preserving user intent through adversarial merge and handoff. The additions above are protocol-doc changes, not implementation-specific changes.

### 3. Merged-requirements contract

**Current evidence**

- Wave 3 currently copies adversarial `merged_output_path` to `<output>/merged-requirements.md` when convergence passes or partially passes (`SKILL.md:286-289`).
- There is no required internal schema for `merged-requirements.md` before Wave 4 consumes it.
- Wave 4 validates only that `merged-requirements.md` has at least three enumerated requirements before tasklist/task handoff (`SKILL.md:312-327`; `refs/handoff-routing.md:183-225`).
- The return contract exposes `merged_output_path`, `convergence_score`, `unresolved_conflicts`, and handoff fields, but not a merged-requirements schema version or fit-to-intent result (`SKILL.md:337-351`).

**Exact change targets**

1. Add a normalization step to `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` immediately after PASS/PARTIAL copy logic in Wave 3 (`SKILL.md:286-289`) and before Wave 3 exit criteria (`SKILL.md:296`).
2. Add the same contract details to `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` after the 3-status routing table (`refs/handoff-routing.md:128-134`) or before Wave 4 handoff routing (`refs/handoff-routing.md:144-147`).
3. Update Wave 4 pre-invoke validation in both files (`SKILL.md:312-327`; `refs/handoff-routing.md:183-225`) to validate this contract, not only count enumerated requirements.

**Recommended merged-requirements minimum contract**

```yaml
---
schema_version: "1.0"
source_seed_brief_path: <path>
domain: code|architecture|product|process|incident|research
strategy: systematic|agile|enterprise
adversarial_status: pass|partial
convergence_score: <float>
fit_to_intent: pass|partial|fail
unresolved_conflicts: []
---

# Merged Requirements

## Intent Preservation
## Requirements
## Acceptance Criteria
## Constraints
## Out of Scope
## Open Questions
## Handoff Notes
```

This should be described as a brainstorm-owned normalization layer over adversarial output, not as a change to adversarial merge internals, to avoid duplicating the adversarial-merge research scope.

### 4. Final fit-to-intent gate

**Current evidence**

- The current status gate is convergence-only: `>=0.65` PASS, `>=0.50` PARTIAL, `<0.50` FAIL (`SKILL.md:286-289`; `refs/handoff-routing.md:128-134`).
- Wave 4 may proceed on PASS or PARTIAL if the requirement-count check passes; there is no explicit comparison between `seed-brief.md` and `merged-requirements.md` (`SKILL.md:312-327`).
- The stable return contract has no field for fit-to-intent status or fit-to-intent issues (`SKILL.md:337-351`).

**Exact change targets**

1. Add a new Wave 3.5 or pre-Wave-4 gate in `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` between Wave 3 exit criteria (`SKILL.md:296`) and Wave 4 start (`SKILL.md:298-304`).
2. Mirror this gate in `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` before `§Handoff-Routing` (`refs/handoff-routing.md:144-147`), because that file controls downstream consumption behavior.
3. Extend the stable return contract in `SKILL.md:337-351` with:
   - `fit_to_intent: pass | partial | failed | null`
   - `fit_to_intent_issues: [<strings>]`

**Recommended gate criteria**

The gate should compare `seed-brief.md` against `merged-requirements.md` and require:

- problem statement preserved or intentionally refined
- all `must_preserve` items retained
- no `out_of_scope` item promoted into requirements
- constraints represented
- success criteria represented as acceptance criteria or measurable outcomes
- unresolved conflicts surfaced, not hidden

Suggested routing:

- `pass`: Wave 4 may proceed normally.
- `partial`: Wave 4 may proceed only with caution metadata and visible warning.
- `failed`: skip handoff; return artifacts for review.

### 5. Return contract

**Current evidence**

- The protocol already defines a stable contract with `contract_version: "1.0"`, status, paths, convergence, domain, proposal count, enrichment, handoff, and unresolved conflicts (`SKILL.md:331-352`).
- The telemetry block includes wave durations, token usage, agent spec, and enrichment sizes (`SKILL.md:354-375`).
- Dry-run exits with a partial return contract (`SKILL.md:246-252`), but the stable schema does not explicitly document which fields are null in dry-run beyond `merged_output_path` comments (`SKILL.md:337-351`).

**Exact change targets**

1. Update `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` Return Contract section (`SKILL.md:331-375`) to include the new seed/merge/fit fields.
2. Add return-contract consumption notes to `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` near expected adversarial response fields (`refs/handoff-routing.md:110-119`) and downstream handoff return consumption (`refs/handoff-routing.md:196-225`).

**Recommended stable additions**

```yaml
seed_schema_version: "1.0"
merged_requirements_schema_version: "1.0" | null
context_anchors_count: <int>
fit_to_intent: pass | partial | failed | null
fit_to_intent_issues: [<strings>]
source_of_truth_paths:
  skill: src/superclaude/skills/sc-brainstorm-protocol/SKILL.md
  refs:
    - src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md
    - src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md
    - src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md
```

Recommended dry-run clarification: explicitly state `merged_requirements_schema_version: null`, `fit_to_intent: null`, `handoff_output_path: null`, and `status: dry-run`.

### 6. Source-of-truth sync discipline

**Current evidence**

- All assigned files are under the source-of-truth tree `/src/superclaude/skills/sc-brainstorm-protocol/`.
- The protocol metadata points to the full spec at `.dev/eval-workspaces/sc-brainstorm/SPEC.md` (`SKILL.md:18`; `SKILL.md:419-421`), but the protocol does not state the repo-level sync requirement for dev mirrors.
- The handoff routing ref has an update-protocol note requiring its Domain-Template-Mapping table and SKILL.md Wave 4 mapping to stay in sync (`refs/handoff-routing.md:229-242`). This is a local precedent for explicit sync discipline.
- The assigned files do not mention `.claude/` dev mirrors or `make sync-dev` / `make verify-sync`.

**Exact change targets**

1. Add a short `## Source-of-Truth / Sync Discipline` section near the end of `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`, before `## 7. Spec Reference` (`SKILL.md:419-421`) or immediately after it.
2. Add a cross-file update note to `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md` near the existing update protocol (`refs/handoff-routing.md:242`).
3. If the seed schema and context-anchor rules are split between `SKILL.md` and `refs/socratic-templates.md`, add a local sync note in `/config/workspace/IronClaude/.claude/worktrees/sc-brainstorm-v2/src/superclaude/skills/sc-brainstorm-protocol/refs/socratic-templates.md` after synthesis rules (`refs/socratic-templates.md:212-222`) stating that seed schema fields in SKILL.md and synthesis rules must be updated together.

**Recommended source-of-truth wording**

- Edit `src/superclaude/skills/sc-brainstorm-protocol/` first.
- Regenerate `.claude/` mirrors with `make sync-dev`.
- Verify with `make verify-sync` before commit.
- Do not stage generated `.claude/skills/...` mirrors.

This target is protocol-maintenance guidance only; it does not affect runtime behavior.

## Cross-file consistency notes

- `SKILL.md` currently embeds the Wave 4 domain-to-template mapping (`SKILL.md:319-326`), while `refs/handoff-routing.md` has an authoritative mapping and update-protocol note (`refs/handoff-routing.md:229-242`). Any change to template mapping must touch both.
- `agent-spec-builder.md` already has a robust validation and sanitization section (`refs/agent-spec-builder.md:97-109`) and does not need direct changes for the requested six targets unless context anchors are later used to influence persona selection. No such use is currently specified.
- `agent-spec-builder.md` explicitly forbids raw topic references in instruction templates (`refs/agent-spec-builder.md:50-76`), which supports the proposed context-anchor extraction being used for enrichment and seed/merge contracts, not for agent-spec custom instructions.

## Summary

Primary protocol changes should land in `SKILL.md` Wave 1, Wave 3/Wave 3.5, Wave 4 validation, and Return Contract sections. Supporting reference changes should land in `refs/socratic-templates.md` for anchor extraction and seed synthesis, and `refs/handoff-routing.md` for enrichment query inputs, merged-requirements validation, fit-to-intent gating, and handoff consumption. `refs/agent-spec-builder.md` appears mostly unaffected except as a constraint: do not inject raw topic or anchors into agent instructions without the existing sanitization and validation path.
