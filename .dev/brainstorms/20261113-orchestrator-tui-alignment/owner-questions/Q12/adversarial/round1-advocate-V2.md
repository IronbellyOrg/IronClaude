# Round 1 advocate statement: Variant 2 (one prose bullet, no table row)

Paths below are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless they start with `F/`. Every file:line was re-read on 2026-11-14 unless marked UNVERIFIED.

## Position summary

Variant 2 makes the merged observer findable now, puts the "person only" rule (INV-013) right beside the guide's existing never-as-worker text, and touches no machine-read block, so no routing test changes. Its real weakness, which I confirmed and concede below, is that `/sc:recommend` does not read the "Orca coordination" section, so the bullet helps people and agents who read the guide but is not routable; the fix is to move the same sentence into a place the recommender does read, not to fall back to deferral.

## Steelman

**Variant 1 (no entry for now), strongest form.** The observer is not finished as a coordination tool: its coordinator-questions panel is off on master (owner question Q6) and the contract note that aligns its words with the sweep's is unwritten. Advertising it in the guide that agents route from invites use before the two tools agree, and every guide edit collides with PR #539, which edits the same guide, its mirror and both routing tests (question.md fact 3). OB-07 is a sink that nothing waits on (merged-requirements.md:779, as cited in question.md), so deferring costs nothing downstream and keeps the guide stable until the tool is complete. Asking again later is cheap and avoids writing something twice.

**Variant 3 (one routing table row), strongest form.** The owner's question is literally "a routing row?", and the spec, the adjudication and the source debate all recommend yes (merged-requirements.md:539, re-read; variant-5-original.md:258-259 as cited in question.md). The routing table is the one surface `/sc:recommend` matches against: its Step 0 extracts only the level table, the routing table and the other-commands block by their markers (`src/superclaude/skills/sc-recommend/SKILL.md:50-54`). A row there is the only form that both people and the recommender use. The test cost may be smaller than INV-029 says: from my reading, the routing-table tests that loop over every row (`tests/core/test_how_we_work_routing_table.py:193-340`) check slash tokens only (`_TOKEN_RE` at `:105` matches spans that start with a backtick and a slash), so a step written as `` `superclaude observe` `` is not looked up as a command. Small, reversible, matches the planned OB-07 shape with no spec churn.

## Strengths claimed

1. **No machine-read block is touched, so no test edit is needed (verified).** The test file defines exactly three marker pairs (`tests/core/test_how_we_work_routing_table.py:22-24`) and reads blocks only through `_block(text, begin, end)` (`:116-118`). In the guide, the routing table ends at `src/superclaude/core/HOW-WE-WORK.md:396` (`<!-- /routing-table -->`) and "## Orca coordination" starts at `:398`, outside every block. INV-029 therefore cannot fire, and `_OTHER_COMMANDS` (`:27` onward) and the membership assertion (`:297-298`) stay untouched. The only whole-guide check that applies is ASCII (`:343-348`), which one plain sentence meets.
2. **The person-only rule lands next to its sibling text.** The Orca section already holds "**Some commands are never workers.**" (`HOW-WE-WORK.md:405`) and the `/sc:sweep` "itself never a worker" bullet (`:406`). The never-as-worker list in `src/superclaude/core/WORKER-CONTRACT.md:23` names slash commands only, which is exactly the gap INV-013 describes; a bullet beside `:405` closes it in the one section about who may run what.
3. **It fixes the real present-day problem.** The guide has no mention of `superclaude observe` (my grep of `HOW-WE-WORK.md` for "observe" hit only unrelated words such as "observed" at `:16`, `:356`, `:390`), while the code exists (`src/superclaude/cli/observe/` holds `commands.py`, `collector.py`, `questions.py` and others). Variant 2 makes it findable; Variant 1 does not.
4. **Lowest exposure to change in the observer itself.** A one-sentence bullet naming only `superclaude observe`, with no flags, carries no flag or step contract that can go stale (relevant to A-002), and it has no `section`, `level` or `mandatory_flags` cells for tests to validate.
5. **Same merge order as Variant 3, smaller diff.** It waits for #539 like Variant 3, but its diff is one guide line plus the byte-for-byte mirror (project CLAUDE.md, "Key Documentation Files"); review and rebase cost is minimal.

## Weaknesses identified in others

**Variant 1.**
- It leaves the INV-013 "person only" sentence written nowhere, while the never-as-worker list stays slash-command only (`WORKER-CONTRACT.md:23`). The risk it names (an agent running the observer as a worker) persists for the whole deferral.
- It has no trigger date or owner: "asked again then" depends on Q6 and on an unwritten contract note, two other open items. A built and merged tool (PRs #503 and #514, question.md fact 1) stays invisible indefinitely.
- The "panel is off" argument is about one panel, not the tool. The rest of the observer works today (UNVERIFIED in a live run; I only confirmed the code exists), and a guide line can describe what the tool shows now.

**Variant 3.**
- It leaves the key design choice open: "The PR decides which table carries the row." The other-commands table is the wrong fit by construction: the first cell of every row must yield a slash token (`:297`, `_TOKEN_RE` at `:105`), so a CLI-only row there breaks `members == _OTHER_COMMANDS` (`:298`) or needs a test change.
- A routing row's `section` cell must name a numbered heading (`test_every_section_reference_is_a_heading`, `:336-340`; `_HEADING_RE` at `:109` matches only headings that start with a number). "Orca coordination" has no number, so the row cannot point at the section that holds the who-may-run-what rules unless it cites an unrelated numbered section or the guide gains a new numbered heading. That is guide-structure churn Variant 2 avoids.
- Matched mode in `/sc:recommend` runs Step C on the row's "selected commands/skills" (`SKILL.md:62`). Whether Step C accepts a step that is a shell CLI rather than a command or skill is UNVERIFIED; precedent exists for non-command steps ("or a plain edit" in the `small-change` row, `HOW-WE-WORK.md:356`), so this is a risk, not a proven defect.
- It accepts a test edit (X-002) and sets a precedent for non-slash entries in machine-read blocks, if INV-029 is right for whichever table it picks.

## Concessions

1. **Variant 2 as written is not routable by `/sc:recommend` (verified; the proposal marked it UNVERIFIED).** Step 0 extracts three blocks "by their markers, never by line number or heading text" (`src/superclaude/skills/sc-recommend/SKILL.md:50-54`). The Orca section is outside all three. A no-match then goes to the cache or to Phase 0 live enumeration of commands, skills, agents and templates (`SKILL.md:108`, `:138`), which would not list a CLI subcommand. So C-005 goes against Variant 2. The agent does Read the whole guide in Step 0, so the bullet is in its context, but no rule tells it to route from prose.
2. **INV-029 may be overstated for the routing table.** From the tests I read (`:193-340`), a routing row whose steps hold `` `superclaude observe` `` with `mandatory_flags` set to `-` seems to pass, provided its `section` cell names a numbered heading. I did not read every row-looping test after `:1090`, so this is partly UNVERIFIED. If true, Variant 2's "no test edit" edge over Variant 3 shrinks to "no guide-structure decision".
3. **A better version of Variant 2 exists and I would adopt it.** The other-commands block already carries a prose line after its table: "One more user-facing skill: `/confidence-check` checks readiness before implementation." It sits inside `<!-- other-commands:v1 -->`, just before `<!-- /other-commands -->` (`HOW-WE-WORK.md`, between `:319` and `:339`). Tests count only lines that start with `|` as table rows (`_table_rows`, `:125-126`), and the live-reference loop checks only slash tokens (`:311-312`). One prose sentence there about `superclaude observe`, person only, would sit inside a block `/sc:recommend` extracts (`SKILL.md:54`) with no test edit. Whether the recommender's no-match path then proposes a CLI that is not a command is UNVERIFIED (`SKILL.md:54` speaks of "a command it names").
4. Variant 2 rewrites the OB-07 spec row and drops its test-edit acceptance items; that is spec churn Variant 3 avoids (X-003).

## Shared assumptions

- **A-001 (any guide edit waits for #539): QUALIFY.** For a prose bullet the reason is not the tests (they never read `:398` onward) but plain textual conflict: #539 edits the same guide, its mirror and the same Orca section (question.md facts 3 and 5); waiting is cheap because OB-07 is a sink.
- **A-002 (the observer is stable enough to route to): QUALIFY.** The code is present (`src/superclaude/cli/observe/`), but flag stability is UNVERIFIED; this favors an entry that names only `superclaude observe` with no flags, which Variant 2's bullet does and a Variant 3 row can also do.

## Per-point verdicts

| Point | Winner | Confidence | One-line reason |
|---|---|---|---|
| S-001 | tie | 95% | All three use the same five sections. |
| C-001 | tie (2 and 3) | 80% | A merged tool with zero guide mentions should be findable now; deferral has no trigger date. |
| C-002 | 3 | 60% | The Orca section is outside every block `/sc:recommend` extracts (`SKILL.md:50-54`); a table row is read, a prose bullet there is not. Variant 2 moved to the other-commands prose line would beat both. |
| C-003 | 2 | 70% | Verified zero test edits (section at `:398` is outside the markers at test `:22-24`); Variant 3 needs a heading or test decision, though INV-029 may be partly overstated. |
| C-004 | tie (2 and 3) | 70% | Both wait for #539 to avoid textual conflict; Variant 1's wait depends on two other open items. |
| C-005 | 3 | 85% | Verified: the recommender extracts only marker blocks, so the Orca bullet is not routable. |
| X-001 | 3 | 55% | Naming the off panel as a cost and shipping anyway beats hiding a working tool; Variant 2 should have addressed it. |
| X-002 | 2 | 65% | Avoiding a precedent for non-slash entries in pinned machine-read tables is cheaper, if discoverability is still met. |
| X-003 | 3 | 60% | Keeping OB-07 unchanged avoids spec churn and re-review of its acceptance items. |
| U-001 | 3 | 55% | Tying discoverability to the guard flip and the note blocks a usable tool on unrelated work. |
| U-002 | 2 | 90% | Correct and verified: the tests read only the three marker blocks (`:22-24`, `:116-118`). |
| U-003 | 2 | 70% | `HOW-WE-WORK.md:405` already holds the never-workers bullet; INV-013 belongs beside it. |
| U-004 | 3 | 75% | The routing table is the surface both people and `/sc:recommend` use (`SKILL.md:53`). |

## Overall ranking and unassigned pick

Ranking, best first: **Variant 2 (with the sentence placed as a prose line inside the other-commands block, next to the `/confidence-check` line), then Variant 3, then Variant 1.** Variant 2 exactly as written (Orca section) ties Variant 3 at best, because it fixes discoverability for readers and the INV-013 gap but not routing.

Unassigned pick: **Variant 3.** The owner asked about a routing row, and verified evidence (`SKILL.md:50-54`) shows only a marker-block entry is routable; a routing-table row is the documented, reliably matched form, and its test cost may be smaller than INV-029 claims. I would add Variant 2's one contribution to it: write the "person only" sentence in the row's notes cell and also as a bullet beside `HOW-WE-WORK.md:405`, which costs one more guide line and no test edit.
