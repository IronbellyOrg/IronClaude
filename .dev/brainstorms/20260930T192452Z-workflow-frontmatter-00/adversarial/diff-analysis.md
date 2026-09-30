# Diff Analysis: spec Comparison

## Metadata
- Generated: 2026-09-30T19:36:00Z
- Variants compared: 2 — V1 `variant-1-opus-architect.md` (225 lines), V2 `variant-2-sonnet-refactorer.md` (222 lines)
- Total differences found: 16
- Categories: structural (2), content (8), contradictions (1), unique (4), shared assumptions (3; 2 promoted)
- Note: model aliases are spec identities only; the Agent tool exposed no model selector, so both variants ran on the session model with persona-specific subagent types.

Core agreement (not debated): both switch Wave 2 from 03 headings to template 00; both bump `schema` to `workflow-plan/1.1`; both require the 3 new keys at schema-min; `created_date` = UTC run date; `priority` = explicit source value else `Medium`, no new flag; `return-contract.yaml` unchanged; command `workflow.md` unchanged; gate bans checkbox and numbered-list lines; 03 kept for `rf-team-lead.md:463`; plugin mirror updated byte-for-byte.

## Structural Differences

| # | Area | V1 (architect) | V2 (refactorer) | Severity |
|---|------|----------------|-----------------|----------|
| S-001 | Fill-rule placement in `quality-gates.md` | New `## Fill rules` section with 3 bullets (V1:89-93) | One `Fill:` sentence under the yaml block (V2:88) | Low |
| S-002 | Gate check distribution | AC-per-Task + placeholder literals at schema-min; Phase→Task grouping + contiguous ids at full (V1:109-142) | Unique Task ids at schema-min; AC-per-Task at full (V2:92-117) | Low |

## Content Differences

| # | Topic | V1 Approach | V2 Approach | Severity |
|---|-------|-------------|-------------|----------|
| C-001 | `version` fill rule | `"1"`, or previous integer + 1 when the same slug is overwritten (V1:15,92) | Constant `"1"` because same-slug runs overwrite with no resume (V2:16,88) | Medium |
| C-002 | `version` validation | Regex `^[1-9]\d*$` (V1:111) | "non-empty" (V2:94) | Low |
| C-003 | Phase field → Task mapping | Inputs → files/sections in task body; Outputs + Checkpoint → that phase's task AC bullets; deps → `Depends on: Task K` (V1:48) | deps/Inputs → `Depends on` on the phase's first task; Outputs → task body; Checkpoint → last task's AC (V2:43) | Medium |
| C-004 | Placeholder-residue check | Enumerated literals: `<!--`, `[High \| Medium \| Low]`, `YYYY-MM-DD`, `version: ""`, `[`-bracketed line (V1:112) | "template comment and `[...]` placeholders removed" (V2:97) | Low |
| C-005 | AC-per-Task check depth | schema-min (quick) (V1:113) | full only (V2:112) | Medium |
| C-006 | Plugin mirror drift control | Manual `diff -r` step; test pins `src/` only (V1:148,214) | Byte-equality assert for SKILL.md + quality-gates.md inside the new test (V2:135-137) | Medium |
| C-007 | `created_date` quoting | Quoted `"YYYY-MM-DD"` string (V1:84,185) | Unquoted `YYYY-MM-DD` (V2:85,166) | Low |
| C-008 | Full-gate phase grouping | "every `## Phase N:` is followed by ≥1 Task before the next Phase" (V1:137) | "≥1 `## Phase N:` and ≥1 `## Task N:`" at schema-min, no per-phase rule (V2:95) | Medium |

## Contradictions

| # | Point of Conflict | V1 Position | V2 Position | Impact |
|---|-------------------|-------------|-------------|--------|
| X-001 | Meaning of `version` across runs | "previous `<run>/plan.md` `version` + 1 when the same slug is overwritten" (V1:186) | "constant (overwrite-in-place, `input-parse.md:13`)"; out of scope: "a version counter across runs (no resume exists)" (V2:164,216) | Medium |

## Unique Contributions

| # | Variant | Contribution | Value Assessment |
|---|---------|--------------|------------------|
| U-001 | V1 | Risk 1: `## Phase N` and `## Task N` are both H2 in template 00, so "has enumerable children" (`sc-implement-protocol/SKILL.md:65`) is ambiguous; mitigation via empty Phase body + full gate forcing ≥1 Task per Phase (V1:210) | High |
| U-002 | V2 | Byte-equality assert for plugin mirror because no make target syncs `plugins/superclaude/` (V2:135-142) | High |
| U-003 | V1 | Explicit placeholder-literal list the gate greps for (V1:112) | Medium |
| U-004 | V2 | "Never guess priority from tone" tied to template 00 "DO NOT invent" rule (V2:168) | Low |

## Shared Assumptions

| # | Agreement Source | Assumption | Classification | Promoted |
|---|------------------|------------|----------------|----------|
| A-001 | Both ban numbered-list lines "anywhere in the body" | The ban excludes fenced code blocks inside Task bodies (a task may quote a snippet with `1.` lines) | UNSTATED | Yes |
| A-002 | Both set `created_date` = UTC run date | The Wave 2 writer has a date source; `refs/input-parse.md:30` limits Bash to "mkdir of output dir only", so `date -u` is not permitted — the value must come from session context | UNSTATED | Yes |
| A-003 | Both read `src/superclaude/templates/...` at runtime | Installed users may lack `src/`; same convention as current `SKILL.md:42` | STATED (V1:211, V2:207) | No |

### Promoted [SHARED-ASSUMPTION] points

| # | Assumption | Impact | Status |
|---|------------|--------|--------|
| A-001 | Numbered/checkbox ban scope excludes fenced code | False `E-GATE` on plans that quote code; conversely `/sc:implement` SKILL.md:64 has no fence exemption either | Open |
| A-002 | Date source for `created_date` under the Bash=mkdir-only rule | Writer may fabricate a date (violates template 00 "DO NOT invent") or break the Bash rule | Open |

## Taxonomy tags
- L1 surface: S-001, C-004, C-007
- L2 structural: S-002, C-003, C-006, C-008, U-002
- L3 state-mechanics: C-001, C-002, C-005, X-001, A-001, A-002, U-001

## Summary
- Total structural differences: 2
- Total content differences: 8
- Total contradictions: 1
- Total unique contributions: 4
- Total shared assumptions surfaced: 3 (UNSTATED: 2, STATED: 1, CONTRADICTED: 0)
- Highest-severity items: none High; Medium: C-001, C-003, C-005, C-006, C-008, X-001
- Similarity: core decision identical; differences are refinements (debate still run; 13 debatable points = S 2 + C 8 + X 1 + A 2)
