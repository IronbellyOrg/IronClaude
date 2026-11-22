# Merge Log

## Metadata
- Base variant: Variant A (keep Task sub-agents), `variant-1-original.md`
- Other variant: Variant B (Orca orchestrator), `variant-2-original.md`
- Plan: `refactor-plan.md` (5 planned changes, auto-approved 2026-11-11T21:20:00Z)
- Merge date: 2026-11-11
- Output: `../merged-output.md` (79 lines)
- Executor: merge-executor

## Change Log

### Change 1: Layering rule replaces base Case point 3
- **Status**: Applied
- **Source**: Debate A-004, C-003; `~/.claude/WORKER-CONTRACT.md` WC-7, WC-8, WC-13 (as quoted in debate-transcript.md and diff-analysis.md)
- **Target**: Base "Claim" and "Case" point 3 (portability and "two dispatch paths forever")
- **Before**: "Orca may be absent there. Every Orca path therefore needs a Task fallback, so we maintain two dispatch paths forever."
- **After**: New section "The layering rule" opens the substance of the document: Task fan-out stays in the command, Orca fan-out belongs to a coordinator, with WC-7, WC-8, WC-13 and the fan-in rule. States that "two dispatch paths forever" does not apply because the skill would hold no Orca code. The Claim now appears as the Verdict.
- **Provenance tag**: `Variant B / debate A-004, C-003 (Change 1)`; Verdict tagged `Base (original, modified)`
- **Validation**: PASS. All WC citations are quoted in the debate transcript or diff analysis. The 90% figure matches the scoring matrix.

### Change 2: Coordinator-level path for B's goals
- **Status**: Applied
- **Source**: Variant B points 2, 3, 4; debate A-001 (agreed 80%), A-002, C-006/C-007/C-008
- **Target**: New section "Where Variant B's benefits are available without refactoring", after the Case list
- **Before**: No such section; base was silent on observability and resume.
- **After**: One `/sc:brainstorm --unattended` worker per Task under a coordinator. Four bullets: isolation, observability, retry and resume (new Task per WC-6, no `--retry-of`), and status of the `--unattended` section. UNVERIFIED label kept: installed `~/.claude` copy has the section (7 matches), `src/` copy on branch `docs/409-orca-dashboard-designs` has 0 matches, master unverified.
- **Provenance tag**: `Variant B points 2, 3, 4 and debate A-001 (agreed 80%), Change 2`
- **Validation**: PASS. Added the A-002 caveat (the adversarial skill runs in-session) so the isolation bullet does not repeat B's X-002 error.

### Change 3: Cross-family diversity, two routes
- **Status**: Applied
- **Source**: Variant A point 6; Variant B point 1; debate C-004 (unresolved, lean A)
- **Target**: Base point 6
- **Before**: "Real gap is narrower than it looks... fixed without Orca (see `sc-bare-review`...)"
- **After**: Section "Cross-family model diversity: two routes" with Route 1 (`sc-bare-review`; proposal generation UNVERIFIED) and Route 2 (coordinator, one worker per model family, then `/sc:adversarial --compare`; non-Claude worker running `/sc:` commands UNVERIFIED). States C-004 stayed open.
- **Provenance tag**: `Base point 6 replaced with Variant A point 6, Variant B point 1 and debate C-004 (Change 3)`
- **Validation**: PASS. Both UNVERIFIED labels present and unchanged in meaning.

### Change 4: Cost-measurement gate
- **Status**: Applied
- **Source**: Debate A-003 (agreed 80%)
- **Target**: Base "What to do instead", last bullet
- **Before**: Two bullets plus the spec-issue bullet; no measurement step.
- **After**: Last bullet: measure worker cold-start time and cost before any decision to use workers for brainstorm; neither variant has numbers. No hours or dollar figures given. Point 4 of the case links to it.
- **Provenance tag**: `Change 4 appends the measurement gate (debate A-003, agreed 80%)`
- **Validation**: PASS

### Change 5: Claims rejected table
- **Status**: Applied
- **Source**: Debate X-001, X-002, A-004, C-005; Variant A U-001; plan "Changes NOT Being Made"
- **Target**: New table at the end of the document
- **Before**: None.
- **After**: Eight rows: `--runtime orca` and in-skill `worker-start`; X-001; X-002; `--retry-of`; `--resume-from`; transcript-size token accounting; merging enrichment into the proposer; base's own "two dispatch paths forever". Open points C-002, C-004, C-008, C-009 listed below the table. Spec defects (U-001) kept in "What to do instead".
- **Provenance tag**: `Debate X-001, X-002, A-004, C-005; Variant A U-001; Variant B points 4, 5, 6 and mitigation (Change 5)`
- **Validation**: PASS. Each row traces to the plan or the debate transcript.

### Other base edits (not separate plan changes)
- Base points 1, 2, 4, 5 kept as "Why the skills keep Task sub-agents" (renumbered 1 to 4). Skill names were added to the file:line cites because the opportunity map shows `SKILL.md:1021-1028` and `:2211-2218` belong to `sc-adversarial-protocol` and `:240` to `sc-brainstorm-protocol`. Point 2 gained rough size labels (Large, Medium, Small) taken from the opportunity map. Point 4 now links to the measurement gate.
- The base "What to do instead" bullet on bare-review was reworded to point to Route 1.

## Post-Merge Validation

### Heading hierarchy
PASS. H1 once, then H2 sections; the two H3 headings (Route 1, Route 2) sit under an H2. No levels skipped.

### Internal references
- Total: 4
- Resolved: 4
- Broken: 0
- Detail: Verdict to "Where Variant B's benefits are available without refactoring"; layering rule to "Claims rejected"; Why-keep point 4 to "What to do instead" (measurement gate); "What to do instead" to Route 1.

### Contradiction re-scan
- New contradictions introduced: 0
- Checked: no claim that skills call Orca; every `--retry-of` and `--resume-from` mention is in the rejected table or states it is not used; UNVERIFIED labels (bare-review proposals, non-Claude worker with `/sc:` commands, master `## Unattended mode`) match the plan; no em dashes; no hours or dollar estimates (size labels only, marked rough).

### Style checks
- Length: 79 lines (limit 120).
- Provenance: header comments plus one `<!-- Source: ... -->` comment per H2 section.

## Summary
- Changes planned: 5. Applied: 5. Failed: 0. Skipped: 0.
- Post-merge validation: PASS.
- Note: the debate and base selection were done by one evaluator that also wrote both variants (stated in debate-transcript.md), so the merge inherits that limit.
