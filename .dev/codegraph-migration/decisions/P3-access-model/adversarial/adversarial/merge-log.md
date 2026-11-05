# Merge Log: P3 access model

## Metadata

- Base: Variant C (`option-c.md`; copy `variant-3-original.md`, 24 lines)
- Plan: `refactor-plan.md` (20 changes, auto-approved 2026-10-29T18:25:00Z)
- Executor: merge-executor (sc:adversarial Step 5)
- Output: `../P3-access-model-merged.md` (229 lines)
- Changes applied: 20 of 20 (failed 0, skipped 0)
- Status: COMPLETE. Debate status carried into the document: BLOCKED_BY_INVARIANTS (INV-002, INV-003, INV-011 as accepted risks with closure rules)
- Timestamp: 2026-10-29T18:30:00Z
- Ground truth re-checked before writing: BR FR-01..FR-08, FR-10, FR-11, FR-19, FR-21..FR-24, NFR-06, NFR-07, NFR-09, K-1 fields, §2.1 line 69, D-01, D-08, D-10, D-11, D-17, D-18, D-28, E-1, E-3, OQ-3, OQ-9; EVAL §3 (tool table, `tools.ts:2926-2929`, `projectPath`), §6.2 (Serena map), §7 steps 5-6

## Changes Applied

| # | Status | Source | Target | Before → After (brief) | Provenance tag | Validation |
|---|---|---|---|---|---|---|
| 1 | Applied | Base Proposal, Strengths, Weaknesses | whole document | Pro/con list → 13-section decision record; base bullets became rules in sections 2-8, strengths the "why" lines of section 1, weaknesses mapped in section 11 | Base (original, modified), sections 1, 3, 4, 11 | 13 H2 sections in plan order |
| 2 | Applied | Variant B; A-002 | section 2 | 8-tool string with explore → 7-tool string, explore omitted; stated as the only Phase 2 edit | Variant B, section 2 | String matches plan exactly; no `explore,node` string remains |
| 3 | Applied | Variant B; INV-009, INV-010 | section 9.1 | none → measurement, 2K threshold (labelled proposed, user confirms), failure branch `status` only | Variant B + probe, section 9.1 | Threshold label present in sections 9.1 and 12 |
| 4 | Applied | X-004; A-001; INV-012 | section 6.4 | "removes most of INV-001" → path-independent freshness, run-time MCP detection, BR INV-001 for no-MCP sessions | Variant B + probe, section 6.4 | Vague phrase removed |
| 5 | Applied | Variant B; BR FR-01..FR-08, K-1; INV-008, INV-013 | section 6.1 | "one readiness check per run" → full contract, 7 states, `access: mcp\|cli\|none`, `graph:unlisted`, E-1 MCP capture | Variant B over base transport, section 6.1 | 7 `index_state` values match BR K-1 line 224 |
| 6 | Applied | B condition (b); A-003; INV-005 | sections 3, 7 | none → exact MCP names in `tools:`/`allowed-tools`; wildcard only in settings | Variant B/A, sections 3, 7 | Consistent in both sections |
| 7 | Applied | C Round 2; INV-014; BR FR-04, FR-06, E-3 | section 5 | 2-3 verbs → 6-verb table per orchestrator class; N-001 flagged | Base (original, modified), section 5 | Verb list identical in sections 1, 3, 5, 7 |
| 8 | Applied | B evidence 2; C Round 2; EVAL §6.2; BR D-10, FR-19 | section 7 | none → node file mode only with `symbolsOnly:true`; FR-23 extended; N-002 flagged | Variant B + C Round 2, section 7 | Agent citations match invariant-probe re-read |
| 9 | Applied | INV-002; BR FR-03, NFR-09 | section 6.2 | none → `Bash(codegraph --version)` for closed-Bash; `graph:provenance_unproven` until E-3 | Invariant probe, section 6.2 | Also listed in sections 3, 5, 11 |
| 10 | Applied | INV-003; EVAL §3 | section 4 | none → brief fields, citation-contract Read, fresh-only calls, rows are leads | Invariant probe, section 4 | Replaces "rarely need to call" |
| 11 | Applied | INV-011; OQ-9; `SKILL.md:86` | section 9.2 | "one live smoke test" → spawn-mode matrix, version re-run, roster pins | Invariant probe, section 9.2 | Referenced from sections 1, 3, 4, 10, 11 |
| 12 | Applied | A U-001; INV-006, INV-007; EVAL §6.2 | section 4 | none → per-agent table; auggie-reviewer search, node, callers as a Bash agent | Variant A corrected by probe, section 4 | Subsets match plan; evidence-validator unchanged |
| 13 | Applied | B evidence 3; INV-004 | section 6.3 | none → `projectPath` = realpath of own toplevel; snapshot and nested children `foreign_index` | Variant B + probe, section 6.3 | Reflect citation `SKILL.md:283-288` kept |
| 14 | Applied | Base bullet 1; U-007; BR FR-02, NFR-07 | section 8 | one fallback sentence → 8-row token table | Base (original, modified), section 8 | Every token is in the BR FR-02 vocabulary; two rows say "none" per FR-02 |
| 15 | Applied | INV-001; EVAL §5.4, §5.8; BR B2 | section 11 | none → ten gates, sibling worktree default, Markdown sparse, first live check | Invariant probe, section 11 | Ten gates counted against the probe text |
| 16 | Applied | INV-008, INV-010; BR items | section 10 | none → superseded-items table plus kept list | Probe + BR, section 10 | All 7 superseded items and 8 kept items from the plan present |
| 17 | Applied | B conditions (a), (d); BR FR-22, FR-23; B9 | section 7 | grep test sentence → FR-23 scope and exception, telemetry handoff, no env prefixes | Variant B, section 7 | `init` exception named once |
| 18 | Applied | A Strength 1; C-012; A-005 | sections 1, 3 | none → name swap in place; new machinery limited to K-1, `affected`, brief fields | Variant A, sections 1, 3 | Matches section 13 C-012 row |
| 19 | Applied | Clarity-1, Correctness-5 NOT MET | all sections | vague phrases → rules from Changes 4 and 10; EVAL/BR/CTX citations on every number | Tags on sections 1, 4, 6.4 | No "rarely" or "removes most" remains |
| 20 | Applied | Debate leftovers; INV-010, INV-012, INV-015; OQ-3, OQ-9 | sections 11, 12 | base weaknesses → accepted-risk table and 8 open points | Probe + debate, sections 11, 12 | All plan items present |

Executor notes (no plan deviation):

- The title is placed directly after the provenance comments, and the metadata block follows it, so the file opens with its H1.
- Two ID spaces both use INV-0NN. The metadata block defines bare INV-0NN as probe findings and BR INV-0NN as brainstorm invariants (BR INV-001, INV-020, INV-025).
- The Change 3 failure branch moves lookups to Variant B's CLI transport. To avoid a contradiction with the 6-verb list, sections 5 and 9.1 state that the 6-verb table describes the pass branch only. This is scoping, not new content.
- Fallback rows for "agent MCP unavailable" and "NFR-06 failure" have no `graph:*` token in the plan; the table says "none" and cites FR-02 (consumers invent no tokens) instead of inventing one.

## Post-Merge Validation

### Structural integrity

- Heading hierarchy: one H1; 13 H2 (sections 1-13, plan order); H3 only under section 6 (6.1-6.4) and section 9 (9.1, 9.2). No level gaps.
- Provenance: 3 header comments; 18 `<!-- Source: ... -->` tags; every Change #1-#20 is cited in at least one tag.
- Tables present where the plan asks: access per class (section 3), agents (section 4), CLI verbs per orchestrator class (section 5), fallbacks (section 8), superseded items (section 10), plus risks (section 11) and not adopted (section 13).
- Length: 229 lines (target 150-230). No emojis.

### Internal references

- Section references: 52 total, 16 distinct targets (1, 2, 3, 4, 5, 6, 6.1, 6.2, 6.3, 6.4, 7, 8, 9.1, 9.2, 10, 11). Resolved 52, broken 0.
- Change references: 16 tags carry `Change #N`, covering 20 distinct changes, all within the plan's #1-#20. Resolved 20, broken 0.
- External IDs (BR FR/NFR/D/E/OQ/K-1, EVAL §n) spot-checked against the ground-truth files; no unknown ID found.

### Contradiction re-scan

- CLI verb list: identical in sections 1, 3, 5 and 7 (`--version`, `status` no-MCP only, `telemetry status`, `query --json` unrestricted-Bash only, `affected`, user-typed `init`). Closed-Bash patterns (`--version`, `affected` in pr-submit) identical in sections 3, 5, 6.2.
- Phase 2: "exactly one env key" holds in sections 1, 2 and 9.1; the failure branch changes only the key's value.
- Agent subsets: section 4 table matches sections 13 (INV-006 row) and 1.
- Freshness: no remaining claim that the access path gives freshness (section 6.4 only).
- Explore: described as blocked everywhere (sections 2, 7, 10); no allowance remains.
- UNVERIFIED markers: 13 kept (alwaysLoad deferral, `allowed-tools` restriction, MCP warning form, `serverInfo` version, MCP spans, foreground access, watcher on init, no-MCP runs, explore instructions).
- New contradictions introduced: 0.

## Summary

All 20 planned changes were applied to Variant C with provenance tags; none failed or were skipped. The merged document follows the plan's 13-section structure, keeps every UNVERIFIED marker, labels the 2K-token threshold as proposed for user confirmation, and carries INV-002, INV-003 and INV-011 as accepted risks with closure rules. Validation found no heading gaps, no broken references and no new contradictions. N-001 and N-002 remain flagged for user review as orchestrator decisions.
