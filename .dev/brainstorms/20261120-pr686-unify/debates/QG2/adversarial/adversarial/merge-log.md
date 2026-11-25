# Merge Log: QG2 position (Base Variant A, OURS)

## Metadata
- Base: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/adversarial/variant-1-original.md` (Variant A, Position OURS)
- Incorporated from: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/adversarial/variant-2-original.md` (Variant B, Position CLAY)
- Refactoring plan: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/adversarial/refactor-plan.md`
- Merged output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/QG2/adversarial/merged-qg2-position.md`
- Merge date: 2026-11-20
- Approval: auto (per plan)
- Note: all D:nnn line citations and the INV and ruling references were taken from the base, Variant B and the plan. This merge did not open `docs/designs/orchestrator.md` or the D15 files, so none of them was re-verified here.

## Changes Applied

### Change 1: Visible mask marker and fenced paths
- Status: Applied
- Source: Variant B, "Cited facts" 4 and "What it risks"; Variant A advocate steelman (via plan)
- Target: Base "Claim" (OD-4 sentence) and "What it risks" (first bullet)
- Before (Claim, OD-4): "OD-4: fail open on delivery (the escalation is always written, the matched span masked, the refusal logged)."
- After (Claim, OD-4): "... the matched span masked with a visible marker such as "[name removed by naming rule]", the original match kept in the log, the refusal logged; the escalation template fences paths, shas and numbers so the scan skips them, which is UNVERIFIED against the real template)."
- Before (risks): the bullet ended with "...written unmasked and logged. Whether the escalation template fences paths is UNVERIFIED (INV-013)."
- After (risks): one sentence inserted before the UNVERIFIED sentence: the mask is a visible marker, the original match stays in the log, paths such as `.claude/settings.json` hit the deny list (INV-013), so the template should fence paths, shas and numbers. The base UNVERIFIED sentence is kept.
- Provenance tag: `<!-- Source: Variant B (Cited fact 4, What it risks; Variant A advocate steelman), merged per Change #1 -->` (Claim) and `<!-- Source: Variant B (Cited fact 4, What it risks), merged per Change #1 -->` (risks); section tags say "Base (original, modified)".
- Validation: marker text is the plan's example, not an invented fact. Template fencing is written as UNVERIFIED in both places. The base "Mechanism" OD-4 bullet ("Mask the matched span") is still true and was left unchanged.

### Change 2: Offline template and fixture scan, scope-independent
- Status: Applied
- Source: Variant B, "Mechanism" (OD-3/OD-4 bullet) and "Cited facts" 8; D:847
- Target: Base "Mechanism", OD-3 bullet (append)
- Before: bullet ended "...only a prompt line stands behind it."
- After: appended "The offline scan does not depend on the scope: a test over every template, fixture and `gh`/`orca` body the end-to-end tests produce, and a fake `launch.effective` test, stay in place for either scope (D:847)."
- Provenance tag: `<!-- Source: Variant B (Mechanism, Cited fact 8; D:847), merged per Change #2 -->`; section tag "Base (original, modified)".
- Validation: scope B for the live writers is untouched. The test wording comes from Variant B's Mechanism bullet.

### Change 3: Escalation shape rules
- Status: Applied
- Source: Variant B, "Mechanism" OD-5 and "What it gets right"; D:825 item 2, D:686
- Target: Base "Claim", OD-5 sentence (append)
- Before: "OD-5: audit escalations go as entry lines only, until the owner rules on the nine-row list and the daily notice cap."
- After: same sentence plus "Rules of the entry-lines channel: one escalation per pull request, never one per finding; warnings never reach the person; the entry is always written; a cap never drops an entry (D:825 item 2, D:686)."
- Provenance tag: `<!-- Source: Variant B (Mechanism OD-5, What it gets right, Cited fact 7), merged per Change #3 -->`
- Validation: each rule appears in Variant B (one per PR, warnings never reach the person, entry always written, a cap never drops an entry, D:686). No cap number is stated.

### Change 4: Reserved notice for AU4a, AU4c, AU5
- Status: Applied (Medium risk per plan; trigger text UNVERIFIED)
- Source: Variant B, OD-5 claim; both advocates' C-004 hybrid (via plan)
- Target: Base "What it risks" (second bullet) and "What it gets right"
- Before (risks): "...Mitigation: the entry is the "waiting on a person" item that the sweep lists; add the notice step when a delivery path is tested."
- After (risks): the "add the notice step" clause is replaced by: entry lines suffice for held items but not for a post-merge hit (INV-014); a notice for AU4a, AU4c and AU5 is reserved, not built; proposed triggers, all UNVERIFIED because no notice sender exists in master, pr-a or pr-p: the owner says in chat that a push is wanted and gives the cap number; a notice sender is tested; row 8 can be used without a ruling on the other eight rows.
- Before (gets right): last sentence "Each deferred piece has a named trigger: ... a tested notice sender."
- After (gets right): same sentence kept; added "The reserved notice for AU4a, AU4c and AU5 has its proposed triggers listed under "What it risks"."
- Provenance tag: `<!-- Source: Variant B (OD-5 claim; both advocates' C-004 hybrid), merged per Change #4 -->` (risks) and `<!-- Source: Variant B (OD-5 claim), merged per Change #4 -->` (gets right).
- Validation: the plan does not say whether the triggers are all required or any one, so the text calls them "proposed triggers" and does not say which. The plan does not describe what row 8 is, so the text does not either. The base Claim still says entry lines only "until the owner rules on the nine-row list and the daily notice cap"; that was not changed (see contradiction re-scan).

### Change 5: Correct the cap and ruling-source statements
- Status: Applied
- Source: Orchestrator check of D:686, D:877, D:1170, D:1177; A-002 (via plan)
- Target: Base "Cited facts" 8 and 3
- Before (8): "The cap is not settled: D:1177 says "not ruled on; open", D:686 and D:877 say "settled as recommended" (ruling 39); ..."
- After (8): "The cap is settled only by Clay's ruling 39, which is not an owner ruling (design default 5, D:877; parser default 0, `pr-a/src/superclaude/cli/issue_watch/repos.py:262-269`): D:1177 says "not ruled on; open", D:686 and D:877 say "settled as recommended" (ruling 39); ..." The rest of fact 8 is unchanged.
- Before (3): "...(ruling 39) but not a "generated with" line..."
- After (3): "...(ruling 39, which is Clay's ruling, not an owner ruling) but not a "generated with" line..."
- Provenance tag: `<!-- Source: Base (original, modified) - ... (Change #5) -->` on facts 3 and 8, plus the section tag.
- Validation: defaults 5 and 0 and the file range come from the plan and fact 7 of the base. D:1170 is named in the plan but not needed in the restated text, so it is not cited. The parser default 0 matches fact 7.

## Post-Merge Validation

### Heading hierarchy
- One H1 (title), then H2 sections in the base order: Claim, Mechanism, Cited facts, What it costs, What it risks, What it gets right. No heading added, removed or re-levelled. Pass.

### Internal references
- "listed under "What it risks"" (What it gets right) resolves to the existing H2 "What it risks". Pass.
- Fact numbers 1 to 9 are still in order and none is renumbered. Pass.
- All three header provenance comment lines are present (Base: Variant A; Incorporated: Variant B; merge date 2026-11-20). Every section and every merged block carries a tag. Pass.

### Contradiction re-scan
- Minor wording mismatch, left as is: the base "What it costs" bullet says a masked name appears as "[removed]", while Change 1 gives the marker "[name removed by naming rule]". Same behavior described loosely; the rule to keep every other base sentence unchanged took precedence. Orchestrator may want to align the "[removed]" text.
- Open tension, left as is: base OD-5 says entry lines only until the owner rules on the nine-row list and the cap; Change 4 lists "row 8 can be used without a ruling on the other eight rows" as an UNVERIFIED trigger. It is written as a proposed trigger for reserving the notice, so it does not change the OD-5 claim, but the orchestrator should confirm the intent.
- Fact 7 (cap key default 0 means no cap) and revised fact 8 (parser default 0, design default 5) agree. Fact 8 and OD-5 agree that the cap is not an owner ruling. No other contradiction found.

## Summary
- Planned: 5
- Applied: 5
- Failed: 0
- Skipped: 0
- UNVERIFIED items carried: template fencing (Change 1), notice trigger text and row 8 (Change 4)
