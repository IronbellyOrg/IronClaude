# Research: /sc:validate-roadmap

- **Topic type:** Command history and recommendation-contract research
- **Scope:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate`
- **Status:** Research complete; command/protocol contradiction blocks an unqualified runnable slash-command recommendation
- **Date:** 2026-10-24
- **Persistence:** Returned as text under the analyst's higher-priority instruction prohibiting report-file writes. No source edits, staging, or execution occurred.

All citations below resolve under the absolute worktree root above. Principal source files are `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/validate-roadmap.md` and `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md`.

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/validate-roadmap.txt`, worker `a68ea505e180b40db`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Exact-path history within the inventory window identifies three command changes:

- `89df2c11`, 2026-05-22: formatting only, adding blank lines before boundary lists. No semantic delta.
- `d9901d87`, 2026-05-26: substantive rewrite from roadmap-file plus source-spec validation to CLI-style pipeline-output validation. It replaced `--specs`, depth, exclusions, output controls, and remediation options with `OUTPUT_DIR`, `--agents`, `--model`, `--max-turns`, and `--debug`. It retained mandatory delegation to the existing protocol.
- `3ae238b1`, 2026-09-30: removed `sequential` from MCP metadata. No input, output, or validation-flow change.

Evidence: read-only `git log -p` for `src/superclaude/commands/validate-roadmap.md`; resulting contract at `src/superclaude/commands/validate-roadmap.md:15-43,71-98`.

[CODE-VERIFIED] The delegated skill changed substantively in the same May 26 commit, but in the opposite direction: its new “Relationship to CLI” section explicitly preserved an independent investigative protocol rather than adopting CLI equivalence. `70ef6486`, 2026-05-30, subsequently changed its domain and cross-cutting agents from Haiku to Sonnet. Evidence: inspected commit patches; current text at `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:18-25,365,494-499`.

### Current command contract

[CODE-VERIFIED] The command advertises an output directory containing `roadmap.md`, `test-strategy.md`, and `extraction.md`. Its default is one `opus:architect` agent; two or more agents enable adversarial merging. Optional controls are model override, maximum turns defaulting to 100, and debug logging. Reports go under `<OUTPUT_DIR>/validate/`. Findings do not produce a nonzero validation exit code. Evidence: `src/superclaude/commands/validate-roadmap.md:21-43,62-69`.

[CODE-CONTRADICTED] This advertised contract is incompatible with its activation target. The command passes output-directory arguments verbatim into `sc-validate-roadmap-protocol`, but that skill requires a roadmap **file** and one to ten source specs through `--specs`. Its flags include `--depth`, `--output`, `--exclude`, `--max-agents`, adversarial/remediation skip controls, `--report`, and prior taxonomy. The skill explicitly says it neither wraps nor mirrors the CLI. Evidence on both sides: `src/superclaude/commands/validate-roadmap.md:71-81`; `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:18-25,80-109`.

[CODE-VERIFIED] Preserve the skill's full investigative capability: requirement extraction, domain coverage matrix, cross-cutting review, adversarial challenge, gap registry, remediation planning, and GO/CONDITIONAL_GO/NO_GO reporting. These are document audits, not code-execution checks. It writes report artifacts but never modifies source roadmaps/specs, executes remediation, or automatically triggers downstream work. Its return contract names consolidated and summary reports. No explicit resume flag appears in its flag table. Evidence: `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:90-109,1122-1155`.

[CODE-VERIFIED] The actual CLI independently accepts the command's directory-style input and four advertised options. It calls `execute_validate`, prints finding counts, and does not convert blocking counts into failure exit status. Its tests explicitly assert exit 0 with blocking findings. The skill's “automated CI/CD gating” description therefore must not be interpreted as exit-code gating. Evidence: `src/superclaude/cli/roadmap/commands.py:430-513`; `tests/roadmap/test_validate_cli.py:140-173`; conflicting prose at `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:23,55`.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The guide's only direct recommendation reference says this command is “Part of the separate `/sc:roadmap` release pipeline.” That understates the delegated skill's domain-agnostic support for arbitrary roadmap and spec formats. The plugin-bundled guide repeats the narrow description. Evidence on both sides: `src/superclaude/core/HOW-WE-WORK.md:284`; `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md:284`; `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:70-78`.

[CODE-VERIFIED] Discovery alone cannot fix that narrowing reliably. “Other commands” contributes candidates only when no routing row matches. The existing `check-plan` row routes plan-versus-spec checks to `/sc:reflect`; a matched row prevents semantic reranking and determines the route. There is no dedicated roadmap-fidelity row. Evidence: `src/superclaude/core/HOW-WE-WORK.md:301-325`; `src/superclaude/skills/sc-recommend/SKILL.md:54-60,148-150`.

[CODE-VERIFIED] Recommendation verification currently reads each candidate's source and activation handoff, but does not explicitly require reading and reconciling the delegated protocol. Rule R1 allows only flags in the verified target's flag table or argument hint. Consequently, simply emitting the old `--specs` slash-command example would conflict with the current command's own table, despite matching the delegated skill. Evidence: `src/superclaude/skills/sc-recommend/SKILL.md:128-135,335-350`; incompatible tables cited above.

[CODE-VERIFIED] Cache hits bypass cold-path source enumeration and return stored envelopes. Surface invalidation hashes source paths plus guide content, not every primitive's contents; per-row dispatch checks one `source_path`. A skill-only contract change can therefore escape a command-backed row's content check. Editing the governing guide does invalidate its surface fingerprint. Evidence: `src/superclaude/skills/sc-recommend/SKILL.md:60-86`; `src/superclaude/cli/recommend/cache.py:63-94`; `src/superclaude/cli/recommend/dispatch.py:103-136`.

### Proposed recommendation changes

[CODE-VERIFIED] **MUST, proposed policy:** Reconcile the command and delegated skill before advertising an unqualified deep-audit invocation. Preserve the investigative skill rather than silently reducing it to CLI validation. The minimum recommendation dependency is an accurate slash-command input/flag contract plus a clear distinction from directory-based CLI validation. This directly affects accurate recommendation, not an unrelated cleanup. Evidence: contradictory contracts at `src/superclaude/commands/validate-roadmap.md:15-43,71-81` and `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:18-25,80-101`.

[CODE-VERIFIED] **MUST, proposed policy:** Update the guide's existing “Other commands” description and add a specific roadmap-fidelity situation to its sole governing routing table. Condition: the user wants to audit an existing roadmap against source requirements, including coverage, dependencies, integration wiring, or readiness. Distinguish that from creating a roadmap, checking a general execution plan, or implementing fixes. Use supporting-task level `-` and report-only `changes_files: no`, following the guide's established meaning. Mirror the guide change into the plugin reference. Evidence: `src/superclaude/core/HOW-WE-WORK.md:284,297,321`; protocol boundaries at `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:1122-1140`.

[CODE-VERIFIED] **MUST, proposed verification rule:** Extend existing candidate verification to follow the selected command's mandatory activation target and detect incompatible required inputs and flags. Report contract uncertainty instead of synthesizing a union of both interfaces. Any cached verification should retain the activation dependency's fingerprint or reverify that dependency before reuse. Evidence: current verification at `src/superclaude/skills/sc-recommend/SKILL.md:128-135`; single-source validation at `src/superclaude/cli/recommend/dispatch.py:116-124`.

[CODE-VERIFIED] **Paste-ready example, current independently verified CLI surface:** `superclaude roadmap validate <OUTPUT_DIR> --agents opus:architect,haiku:qa`. Keep the directory placeholder until supplied; explain that report counts, not shell success, determine findings. Do not attach `--specs` or `--depth` to this CLI. A deep slash-command example remains conditional on contract reconciliation; its existing skill documents `/sc:validate-roadmap <roadmap-path> --specs <spec-paths>`, but the command does not currently verify that flag. Evidence: `src/superclaude/cli/roadmap/commands.py:430-479`; `src/superclaude/skills/sc-validate-roadmap-protocol/SKILL.md:80-101`.

### Acceptance/regression scenarios

[CODE-VERIFIED] Proposed regressions should cover:

1. Existing roadmap plus specs and “coverage matrix, report only” selects the dedicated audit, never automatic implementation.
2. Pipeline output directory plus agent list selects the directory validator without deep-skill flags.
3. Command/protocol disagreement produces an explicit contract-gap result.
4. General task-plan review remains distinct from roadmap fidelity.
5. Missing plugin command/protocol never becomes a runnable ghost recommendation.
6. Protocol-only edits invalidate or reverify cached command handoffs.
7. A blocking CLI report is not treated as passed because exit status is 0.
8. Subsequent ordinary remediation defaults to workflow plus implement; explicit MDTM execution remains `/task`.

These extend structural source/flag checks, which currently do not prove semantic routing or activation compatibility. Evidence: `tests/core/test_how_we_work_routing_table.py:275-304`; `tests/roadmap/test_validate_cli.py:140-173`.

## Gaps

[CODE-VERIFIED] Literal searches found no validator-specific references in recommendation refs, cache/classifier prompts, recommendation tests, core routing tests, or commands README. Tracked-path searches found no plugin validator command or matching protocol package. The plugin guide nevertheless names it. This is an availability caveat, not authorization to invent a plugin implementation.

[UNVERIFIED] No command, skill, CLI validation subprocess, or tests were executed. Findings establish source contracts and inspected test assertions, not observed runtime outcomes.

## Key Takeaways

**CHANGE. MUST:** Resolve the activation mismatch, describe full investigative validation, distinguish CLI validation, and test both recommendation routes.

**SHOULD:** Track delegated-source freshness and preserve plugin availability warnings.

**NONE:** No extra keyword table, invented flags, automatic remediation, or forced MDTM escalation. The user's workflow-first preference governs later implementation choices; it must not displace this dedicated report-only audit.
