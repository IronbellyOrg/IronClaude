---
name: reflect
description: "Tiered reflection (UC-1 pre-execution / UC-2 post-execution) grounded in real code and citations, using Serena + Auggie"
category: special
complexity: advanced
mcp-servers: [serena, auggie, context7, tavily, sequential]
personas: [analyzer, qa, refactorer, architect]
---

# /sc:reflect - Tiered Reflection (UC-1 / UC-2)

## Triggers

- Pre-execution (UC-1): audit a proposed tasklist/strategy against its driving spec/PRD for coverage and best-practice compliance before token spend
- Post-execution (UC-2): audit completed work (diff, artifacts, task log) for 100% adherence and classify every divergence under the 4-category deviation taxonomy
- Reviewer-side, structurally-independent validation — not single-agent self-review
- Auto-triggered by `/sc:troubleshoot` Wave 6 (Phase B pre-exec, Phase D post-exec)

## Usage

```bash
/sc:reflect [--mode pre|post] [--spec <path>] [--tasklist <path>] [--diff <ref>] \
  [--depth quick|standard|deep] [--tier 1|2|auto] [--reviewers N] [--remediate]
```

Legacy grammar (preserved for `/sc:troubleshoot` Wave 6 and other v1 callers):

```bash
/sc:reflect --type task --analyze    # maps to --mode pre
/sc:reflect --type task --validate   # maps to --mode post
```

## Required Input

- **UC-1 (pre)**: `--spec <path>` is required. `--tasklist <path>` is strongly recommended.
- **UC-2 (post)**: at least one of `--diff <ref-or-path>` or `--task-log <path>` is required. `--tasklist <path>` is strongly recommended.

## Behavioral Flow

1. **Resolve mode**: explicit `--mode pre|post` (or legacy mapping), else auto-detect from inputs
2. **Tier 1**: fast single-agent grounded reflection (auggie + serena symbol chain), blind-calibrated
3. **Tier decision**: rubric routes to Tier 2 on low confidence, multi-domain, or regression candidacy
4. **Tier 2 (conditional)**: heterogeneous reviewer ensemble + adversarial merge via `sc-adversarial-protocol`
5. **Evidence-validator gate**: every `file:line` citation re-Read; unfounded citations dropped, not downgraded
6. **Report + contract**: coverage matrix (UC-1) or deviation register (UC-2) + versioned return contract
7. **Tier 3 (opt-in `--remediate`)**: hand off to `task-builder` for a corrective MDTM task

## MCP Integration

- **Auggie** (primary, free retrieval): codebase grounding via `mcp__auggie__codebase-retrieval`
- **Serena**: symbol-level navigation (`find_symbol`, `find_referencing_symbols`, `get_symbols_overview`, `find_declaration`, `find_implementations`, `type_hierarchy`), the UC-2 verification triangle (`get_diagnostics_for_file` / `execute_shell_command` / `summarize_changes`; `--no-verify` disables), opt-in `onboarding` cold-start (`--onboard`), and cross-session memory
- **Context7 / Tavily / Sequential**: Tier 2 only (framework docs, external-symptom lookups, synthesis)

## Tool Coordination

- **modern Serena symbolic chain** replaces the load-bearing role of `think_about_*` (which remain as scripted, non-gating checkpoints captured to the audit log)
- **confidence-calibrator**: blind re-grade of each reviewer card (calibrator class disjoint from reviewer classes)
- **evidence-validator**: non-negotiable final gate — a zero-drop pass is treated as suspect, not clean
- **sc-adversarial-protocol**: Tier 2 debate/scoring/merge (never re-implemented here)

## Key Patterns

- **UC-1 coverage**: spec → tasklist coverage map → unmapped-requirement gap registry → best-practice grade
- **UC-2 deviation**: tasklist-vs-diff map → 4-category taxonomy (Authorized / Necessary / Drift / Regression) → remediation posture
- **Tier escalation**: quick-first Tier 1, escalate only when the rubric or `--tier 2`/`--depth deep` demands
- **Promotion (UC-2)**: on a strict gate pass, move the validated work-unit to its `done` destination (`--no-promote` to suppress)

## Examples

### UC-1 pre-execution coverage/gap audit

```bash
/sc:reflect --mode pre --spec docs/spec.md --tasklist .dev/tasklists/feat.md
# Coverage matrix + unmapped requirements before execution
```

### UC-2 post-execution deviation audit

```bash
/sc:reflect --mode post --diff HEAD~1..HEAD --tasklist .dev/tasklists/feat.md
# 100% adherence audit + per-item deviation classification
```

### Legacy (preserved for `/sc:troubleshoot` Wave 6)

```bash
/sc:reflect --type task --validate   # maps to --mode post (needs --diff or --task-log)
```

## Boundaries

**Will:**

- Run reviewer-side, structurally-independent reflection grounded in real code and real citations
- Classify every UC-2 deviation under the 4-category taxonomy with detection signals and gold-standard references
- Delegate Tier 2 debate/scoring/merge to `sc-adversarial-protocol`; gate every report through evidence-validator

**Will Not:**

- Confirm its own conclusions — a zero-drop evidence-validator pass on a non-trivial report is an audit flag
- Auto-execute a Tier 3 remediation task (produces a file; the user runs `/task`)
- Treat `think_about_*` as the load-bearing signal, or the executor's commit message as the gold-standard reference
