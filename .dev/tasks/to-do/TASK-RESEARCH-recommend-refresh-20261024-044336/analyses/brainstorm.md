# Research: /sc:brainstorm recommendation refresh

- **Topic type:** Command contract and routing research
- **Scope:** Changes from 2026-04-24 through 2026-10-24, current command/protocol, recommendation surfaces, plugin packaging and regression coverage
- **Status:** Research complete; proposed changes not implemented
- **Date:** 2026-10-24
- **Delivery:** Inline findings. Higher-priority worker instructions prohibit writing report Markdown files; no output file was created.

## Evidence paths

Line citations below use these absolute-path aliases.

- **B:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/brainstorm.md`
- **P:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-brainstorm-protocol/SKILL.md`
- **H:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md`
- **A:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-brainstorm-protocol/refs/agent-spec-builder.md`
- **G:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/core/HOW-WE-WORK.md`
- **R:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/skills/sc-recommend/SKILL.md`
- **W:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/workflow.md`
- **PG:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`
- **TC:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/core/test_how_we_work_routing_table.py`
- **TP:** `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/tests/commands/test_routing_plugin_parity.py`

- **Persistence provenance:** Mechanically transcribed by the parent from `../artifacts/worker-returns/brainstorm.txt`, worker `a711c2fb3e6db93b9`. The source journal is `/config/.claude/projects/-config-workspace-IronClaude--dev-worktrees-RecommendUpdate/076ab338-03dd-4322-a0dc-a343e620c69e/subagents/workflows/wf_da8a02a1-53f/journal.jsonl`. Worker claims and proposed changes are not independent verification.
- **Governing template:** `src/superclaude/templates/modularization-template-review/codebase-research_template.md` (Findings, Gaps, Key Takeaways scaffold).

## Findings

### Historical changes

[CODE-VERIFIED] Exact-command history contains six commits in the requested window:

- `89df2c11`, 2026-05-22: blank-line normalization and final newline only. Formatting, not a semantic change.
- `02105108`, 2026-05-25: substantive v2 replacement. Interactive discovery became a thin command delegating to a protocol with seed briefs, parallel proposals, adversarial merging, artifacts, resume, preview and optional handoffs. Depth values changed from `shallow|normal|deep` to `quick|standard|deep`; old examples containing `--parallel` and `--validate` disappeared.
- `a97dfb29`, 2026-06-20: removed automatic security-persona claims from examples, paired with protocol and persona-reference changes requiring explicit security selection.
- `3ae238b1`, 2026-09-30: removed the `sequential` MCP declaration.
- `051f39fe`, 2026-10-14: corrected `/sc:task-builder` references to `/task-builder`.
- `5c6a7d91`, 2026-10-22: replaced the command’s checkout-only protocol path with its installed path.

Evidence: directly inspected `git log` and relevant patches for B; current flag and handoff contracts remain at B:43-71.

[CODE-VERIFIED] Relevant protocol-only changes include `b3ebeab0`, 2026-06-25, assigning research parameters to the research delegates; `4c66adba`, 2026-10-01, allowing unset model environment variables; and `3fcb5417`, 2026-10-22, accepting installed or project adversarial prerequisites with installed-skill precedence. These changes do not establish additional brainstorm flags. P:103-109,183-189; A:27-35.

### Current command contract

[CODE-VERIFIED] Input is a nonempty topic, optionally using a file reference. Defaults are three proposals, standard depth, automatic strategy and no downstream handoff. Useful controls include `--interactive`, `--codebase`, research depth, personas, models, blind scoring, convergence, output directory, preview and saved-seed resume. Quick depth caps proposals at two; enterprise implies deep depth unless explicitly overridden. B:21-29,43-71.

[CODE-VERIFIED] Brainstorm produces requirements artifacts rather than product implementation: a seed brief, merged requirements, enrichment when applicable, adversarial artifacts and a versioned return contract. `--handoff design` prints a recommendation only. `--handoff task` invokes task-builder, not `/task`; it therefore builds a task file rather than executing implementation. P:53-60,301-354.

[CODE-VERIFIED] Preview is not a zero-write inspection: prerequisites create an output directory and dialogue writes a seed brief before the dry-run gate skips adversarial generation and downstream handoff. Resume reads a saved seed brief and skips dialogue; domain mismatch requires `--force-stale`. Noninteractive dialogue can proceed from available context rather than waiting for user replies. P:108,124-134,167,249-254.

[CODE-VERIFIED] Security is excluded from automatic persona selection and restored only through explicit `--personas`. Recommendation text must not advertise security review as an automatic enterprise benefit. A:18-20,29-51.

### Comparison with recommendation surfaces

[CODE-VERIFIED] The guide correctly preserves brainstorm as a dedicated requirements-discovery route. `shape-idea` invokes brainstorm and marks the route report-only; `full-spec` invokes it only when the idea remains vague. This agrees with the command’s requirements-only boundary. G:309-310; P:413-418.

[CODE-CONTRADICTED] The current guide conflicts with the requested new routing policy: sections 3.1 and 3.6 and the `shape-idea` note recommend `--handoff task` merely because no PRD is needed. That condition says nothing about exceptional complexity or long duration. The actual handoff invokes task-builder. G:53,151,310; P:320-330. This is a policy mismatch, not evidence that current execution violates its existing guide.

[CODE-VERIFIED] Correcting only brainstorm discovery descriptions will not fix this route. Recommendation Step 0 lets a matched guide row decide the answer and skips cache lookup, cold-path write-back and semantic ranking. The guide’s conditional note therefore directly influences the resulting recommendation. R:50-61.

[CODE-VERIFIED] A supported alternative already exists without inventing a brainstorm flag: workflow accepts an existing source file and supports standard or deep planning. It can therefore consume the returned merged-requirements artifact in a separate invocation. Brainstorm’s existing handoff enum contains no `workflow` value. W:18-40; B:60.

[CODE-VERIFIED] Plugin recommendations carry the same problematic `shape-idea` note. The parity test requires the plugin guide to remain byte-identical to the canonical guide, and the recommendation skill tree to mirror source plus that guide. Changes must update the shared guide and its required plugin copy, not create a second routing table. PG:309-310; TP:27-36.

### Proposed recommendation changes

[UNVERIFIED] **MUST, desired policy:** Amend G sections 3.1 and 3.6 and row `shape-idea`. Retain brainstorm as the terminal route when users request requirements discovery only. Replace the broad “no PRD needed” task-builder condition with: after requirements are agreed, most implementation planning uses workflow followed by implement; reserve task-builder handoff for explicitly requested MDTM work or the exceptionally complex, long-running workloads identified in the consolidated policy. File count, resume and an existing specification alone must not trigger that escalation. Evidence motivating the change: G:53,151,305-310; P:320-330.

[UNVERIFIED] **SHOULD, capability exposure:** Extend the existing guide explanation with verified optional refinements rather than another keyword table:

- User wants questions before synthesis: `/sc:brainstorm "Clarify onboarding requirements for team administrators" --interactive`
- User wants a bounded preview: `/sc:brainstorm "Compare onboarding approaches" --depth quick --dry-run`
- User wants blinded alternatives: `/sc:brainstorm "Explore worker error-handling requirements" --depth deep --proposals 5 --blind`
- User explicitly wants artifact-only discovery: retain default `--handoff none`.

The flags are verified at B:43-71. Generated prompts should invoke the command, not reproduce its internal waves.

[UNVERIFIED] **MUST, follow-on example:** For a user who subsequently requests ordinary implementation planning, recommend `/sc:workflow <returned merged-requirements path> --depth standard`, review the printed plan, then use the existing implement route. Substitute the actual returned path; do not invent a timestamped file. Do not emit nonexistent `--handoff workflow`. W:18-40; G:305; P:343-344.

### Acceptance/regression scenarios

[UNVERIFIED] Proposed checks:

1. “Explore this vague feature; requirements only” selects `shape-idea`, omits implementation and task-builder, and keeps report-only classification.
2. “Ask me before deciding” preserves `--interactive`.
3. “Preview the brainstorm” preserves `--dry-run` and does not promise merged requirements or no filesystem writes.
4. Ordinary implementation after brainstorming recommends workflow plus implement, including when several files or sessions are involved.
5. Explicit MDTM handoff remains available; missing dependencies are not silently substituted.
6. A cached unrelated recommendation cannot override a matched `shape-idea` row.
7. Plugin and canonical guide changes pass byte-parity checks.
8. Old `--parallel` and `--depth normal` examples do not reappear.

## Gaps

[CODE-VERIFIED] Existing routing tests check row structure, command existence and flag existence, not these semantic distinctions. TC:176-201,243-255,286-304. No recommendation-specific brainstorm cases appeared in the targeted searches.

[UNVERIFIED] Internal handoff compatibility needs separate validation before advertising those paths more strongly: brainstorm invokes tasklist with `--source` and merged requirements, while the public tasklist contract expects a roadmap positional input. This is not proof that direct protocol invocation fails. H:183-194; `/config/workspace/IronClaude/.dev/worktrees/RecommendUpdate/src/superclaude/commands/tasklist.md`:20-38.

[UNVERIFIED] Tracked-file enumeration found a plugin brainstorm command but no tracked plugin brainstorm-protocol subtree. A global installation might supply that dependency; plugin-only executability was not demonstrated. No skills or runtime tests were executed during this research.

## Key Takeaways

[UNVERIFIED] **CHANGE. MUST:** Fix the guide’s broad task-builder handoff condition and its plugin copy while preserving report-only brainstorm routing.

[UNVERIFIED] **SHOULD:** Expose interactive discovery, bounded preview, blinded proposals and saved-seed continuation when user intent warrants them.

[UNVERIFIED] **NONE:** No new fixed keyword table, no new brainstorm flag, no automatic implementation, and no claim that workflow has an undocumented capacity limit.
