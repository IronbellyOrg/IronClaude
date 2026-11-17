# Variant 3 (haiku, analyzer): evidence-first cut list

Saved by the orchestrating session from the agent's returned text; evidence condensed, verdicts unchanged. Confidences as reported (94 to 99 percent on nearly every row; see the scoring note about calibration).

Stance: cut current questions-panel decision work, not safety checks or merged features. Only C16 survives as a CUT; several claimed savings are unverified; two supposedly redundant controls protect different boundaries.

Claims checked (all against master `8c21ac41f`):
- (a) TRUE for default production discovery: acceptance needs exit 0 and an `orca-cli` topic (`install_user_setup.py:268`); but the candidate executable is already run for the discovery probe at line 259, so a wrong executable is run once.
- (b) TRUE for `src/` (only the definition at `cycle.py:1359`); FALSE as "no useful caller": the operator script at `docs/designs/issue-watcher-setup.md:470` calls it, with a seven-day review at line 680.
- (c) TRUE: `probes.py:59` has the exact tuple (allowed, not called); `worker-show` at line 52. Allow-list membership does not show the captures replace the other tests.
- (d) TRUE: `launch-level-guard.sh:347` matches the leading implementation command; line 353 matches the whole prompt `approved` (optionally `.` or `!`). Both release only the governed worktree level.
- (e) TRUE, narrower than the proposed deletion: `observe/commands.py:64` requires an owner-written pass record before live question reads; `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode/.dev/issues/409/bmad/spec-orca-observer/release-gates.md` lines 22 and 50 forbid agents from writing the owner's evidence. Original authorship UNVERIFIED.
- (f) `questions.py` is 151 lines; 56 test functions with "question" in the name; the 2,500-line deletion is UNVERIFIED.
- (g) FALSE for "another identifiable reader" within the searched scope; external readers and dynamic paths UNVERIFIED.

| ID | Verdict | Risk if cut | Reward if cut | Conf |
|---|---|---|---|---|
| C01 | MODIFY | Backup does not establish owner approval | Preserve endangered records promptly | 96 |
| C02 | KEEP | Loses comparison and message-safety evidence | Fewer live checks | 97 |
| C03 | KEEP | Mistakes plan wording for owner confirmation | One card fewer | 98 |
| C04 | KEEP | Hides executable-selection differences | One risk question fewer | 98 |
| C05 | KEEP | Removes an unresolved non-worker messaging boundary | One future question fewer | 97 |
| C06 | DEFER | Changes sequencing without checking its source | Shorter start gate | 94 |
| C07 | DEFER | Acceptance-record gap remains | Avoid premature paperwork | 95 |
| C08 | DEFER | Future reader still needs staleness rules | No unsupported threshold | 97 |
| C09 | DEFER | Panel cannot ship during deferral | Avoid an unused live-test decision | 98 |
| C10 | KEEP | First manual launch lacks an accountable owner | Avoid a full rota now | 97 |
| C11 | DEFER | Installation remains a prerequisite to use | Avoid interrupting sessions | 93 |
| C12 | KEEP | Removes explicitly approved GitHub inputs; reversal needs an owner decision | Potentially less unbuilt code | 99 |
| C13 | KEEP | Reverses the explicit "remove now" answer | Fewer immediate edits | 99 |
| C14 | DEFER | Could bypass live-test prerequisites | Real launch and reply evidence | 95 |
| C15 | KEEP | Breaks the documented operator measurement | Removes helper and tests | 99 |
| C16 | CUT | Questions-panel progress pauses | Stops panel decision work | 97 |
| C17 | DEFER | Broad deletion damages shared behaviour | Potential large deletion | 98 |
| C18 | DEFER | Breaks the export default or external consumers | Avoid repeated writes | 97 |
| C19 | MODIFY: add the caveat, no blanket freeze | Blanket freeze blocks the requested summaries | Honest report without new probes | 97 |
| C20 | DEFER | Invents a new incident-only start condition | Avoid speculative design | 94 |
| C21 | KEEP | Enables an unpassed live read; weakens approval provenance | Removes gate code | 99 |
| C22 | KEEP | Merges different discovery policies | Less apparent duplication | 98 |

Final list: C16.
