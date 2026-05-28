---
title: "agent-spec-builder.md — Phase 2 Scope Note"
task: TASK-RF-20260526-183300
phase: 2
step: 2.4
decision: no-edit
created: 2026-05-26
---

# agent-spec-builder.md — No-Edit Scope Note

## Decision

`src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md` was NOT edited in Phase 2 Step 2.4. The existing file already contains every sanitization and injection guard required by the context-anchor remediation design. Adding additional anchor-handling rules to this file would broaden the remediation beyond its declared scope (context retention and return-contract traceability) and risks introducing new runtime behavior that was not researched in `01-protocol-targets.md`.

## Evidence

Three guards already present in `agent-spec-builder.md` cover the anchor-injection risk surface:

1. **Raw-topic prohibition** (`§Instruction-Templates`, line 52): explicitly states "NEVER reference the raw user topic — injection risk." This same rule applies transitively to `context_anchors` values, which are themselves extracted verbatim from the topic and dialogue. The raw-topic prohibition therefore already forbids raw anchor injection by extension.

2. **Parameter sanitization rule** (`§Instruction-Templates`, lines 70-74): for every `{X}` placeholder substitution, strip `,`, `:`, `'`, `"`, newline, tab, and control characters before substitution; if the sanitized value becomes empty, fall back to the placeholder literal. The current templates use only `{domain}` and `{strategy}` — both fixed-vocabulary, classification-derived values. No `{anchor}` or `{topic}` placeholder exists or is being added.

3. **Round-trip validation** (`§Validation`, lines 97-109): every serialized agent-spec is parsed back through the adversarial parser; segments must match recognized model aliases and persona names, with single-quote boundary handling. Any malformed instruction string is a STOP, preventing downstream injection.

## Why the Phase 2 context-anchor design respects this boundary

The context-anchor remediation in Phase 2 routes anchors into THREE places, all of which keep them away from agent-spec custom instructions:

- **Wave 1 seed-brief synthesis** (SKILL.md Wave 1 step 5/6 + `refs/socratic-templates.md §Context-Anchor-Extraction`): anchors are written into `seed-brief.md` body sections (`## Context Anchors`, `## Must Preserve`, `## Out of Scope`). These are markdown documents consumed by humans and downstream skills — not shell-style serialized instruction strings.

- **Wave 2A codebase enrichment** (`refs/handoff-routing.md §Enrichment-Sources` Codebase Tier 1): anchors are interpolated into Auggie query strings. The handoff-routing edit explicitly added a sanitization rule (strip commas, colons, quotes from anchor values before joining) and restated that "raw anchors are NEVER injected into agent-spec custom instructions — that path remains governed by `refs/agent-spec-builder.md`."

- **Wave 3 merged-requirements normalization + fit-to-intent gate** (SKILL.md Wave 3 steps 5-6 + `refs/handoff-routing.md §Merged-Requirements-Normalization, §Fit-to-Intent-Gate`): anchors are compared against the merged-requirements document. Comparison is internal logic; no anchor value ever reaches the agent-spec string.

`refs/agent-spec-builder.md` continues to govern ONLY the model/persona alias requirements and instruction-template parameter substitution. Persona selection is driven by the `--personas` flag, the `--strategy enterprise` override, or the domain-aware default matrix — none of which consume `context_anchors`. Model aliases come from `--models` or the `opus,sonnet,haiku` default. Neither requires any anchor-aware logic.

## What this scope note does NOT do

- Does NOT add new runtime behavior to `agent-spec-builder.md`.
- Does NOT modify the persona matrix, model rotation, instruction templates, sanitization rule, serialization, validation, token-budget estimation, or round-trip test vectors.
- Does NOT bring context anchors into persona selection. If a future remediation explicitly opts to use anchors for persona influence, that work is out of scope for TASK-RF-20260526-183300 and would require a fresh research+gate cycle.
- Does NOT modify any generated `.claude/skills/...` mirror file.

## Verification

- `src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md` mtime unchanged after Step 2.4.
- No edits applied to that file during this step.
- `git status` for this file shows no modifications attributable to Step 2.4.
