# Round 1 advocate statement: Variant 3 (one routing row, own small PR after #539)

Persona: architect. Depth: quick. Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. Every line number below was re-read in this session unless marked UNVERIFIED.

## Position summary

Variant 3 is the best answer because the routing table is the only part of `HOW-WE-WORK.md` that `/sc:recommend` actually reads for routing, so it is the only placement that makes the observer findable by both people and the recommender. Reading the tests shows the cost Variant 3 names for itself (INV-029) is smaller than stated: a routing-table row whose step is a plain terminal command already has a precedent and appears to pass the current tests with no test edit (by reading, not run).

## Steelman

**Variant 1 (no entry for now).** The strongest form: do not advertise a tool before it is complete. The observer's coordinator-questions panel is off on master (owner question Q6), and the contract note that aligns its words with `/sc:sweep` is unwritten. A routing entry written now would describe a half-switched-on tool and would have to be rewritten when the panel turns on, so waiting means one edit instead of two, no rebase against #539, and zero risk to the two machine-read test tables (`tests/core/test_how_we_work_routing_table.py:193-205`, `:297-298`). OB-07 is a sink (nothing waits on it, merged-requirements.md:779 per question.md), so deferring it blocks nothing.

**Variant 2 (one bullet in "Orca coordination").** The strongest form: put the observer exactly where its sibling already lives. The "Orca coordination" section (`src/superclaude/core/HOW-WE-WORK.md:398-408`) already carries the `/sc:sweep` bullet (`:406`) and the never-as-worker rule (`:405`), so "person only, never as a worker" sits next to the rule it extends. The two table tests read only the marked blocks (markers defined at `tests/core/test_how_we_work_routing_table.py:22-24`), so a prose bullet needs no test edit at all and cannot destabilise the routing contract. It is the smallest change that still makes the tool discoverable to a human reading the guide.

## Strengths claimed

1. **Only the table reaches `/sc:recommend`.** The sc-recommend skill extracts three blocks "by their markers, never by line number or heading text": the level table, the routing table and the other-commands block (`plugins/superclaude/skills/sc-recommend/SKILL.md:50-54`). Routing is "Match the whole requested outcome to one routing row" (`:58`), and "The guide's routing table, read in Step 0, is the only fixed routing source" (`:403`). A bullet in "Orca coordination" is outside all three markers, so Variant 2's own UNVERIFIED cost ("`/sc:recommend` may not route to a bullet") is in fact confirmed: the recommender does not read that section for routing. Variant 3 is the only option that makes a request like "how do I watch my workers" route to the observer.

2. **A CLI-only routing row has precedent and appears to pass today's tests.** The `resume` row already has a non-slash step: "1c. named conversation: terminal `ccsession <name>`" (`HOW-WE-WORK.md:376`), and the `cleanup` row's step 1 is "establish an authorized checkpoint commit" (`:370`). Reading the routing-table tests:
   - 8 cells, no escaped pipe, ASCII (`test_how_we_work_routing_table.py:193-198`): a normal row meets this.
   - Ids unique, kebab case, and `_EXPECTED_IDS <= set(ids)` (`:201-205`): adding an id is allowed; the comment at `:55-56` says "A row may be added".
   - `level` in `[1-6]|-` and `changes_files` in `{no, yes, asks first}` (`:208-211`): `-` and `no` fit.
   - Command tokens are found only by a backtick followed by `/` (`_TOKEN_RE` at `:105`), so `` `superclaude observe` `` yields no token to resolve (`:214-218`).
   - Each `section` reference must be a numbered heading (`:336-340`); `3.13 Specialist deliverables and operations` exists (`HOW-WE-WORK.md:240`), while "Orca coordination" (`:398`) has no number, so the row would cite `3.13` (the PR may add a short 3.13 sentence).
   - `tests/recommend/test_routing_refresh.py:33` lists command names shipped after the frozen research package; the observer adds no command file, so that line likely needs no edit either.
   So INV-029's "fits neither block without a test edit" is accurate for the other-commands block (`:297-298` pins its member set) but appears wrong for the routing table. This is my reading, not a test run: UNVERIFIED until `uv run pytest tests/core/test_how_we_work_routing_table.py tests/recommend/` runs on the PR branch.

3. **Follows the plan of record with no spec churn.** It is the spec's recommended answer (merged-requirements.md:539, per question.md) and V5 D8's own words, "the routing row only, in its own small PR. A command is not needed" (variant-5-original.md:258-259, per question.md). OB-07's row, acceptance items and graph edge "SW-05, K-ROUTE, Q12 -> OB-07" stay as written (X-003). Variant 2 rewrites OB-07; Variant 1 parks it.

4. **Carries the "person only" guard into a machine-read place.** INV-013 asks for one "person only" sentence. The other-commands entry for `/sc:sweep` already uses that exact pattern in a machine-read cell: "Coordinator or person only, never a worker." (`HOW-WE-WORK.md:335`). A routing row's `notes` cell can carry the same sentence, so `/sc:recommend` repeats it whenever it suggests the observer. A prose bullet carries it only to a human who reads that far.

5. **Small, reversible, correctly sequenced.** One row in a file that #539 also edits, waiting for #539 so there is no rebase conflict (question.md fact 3); reverted by one PR.

## Weaknesses identified in others

**Variant 1.**
- Leaves a merged, shipped tool (`src/superclaude/cli/observe/` exists with 12 modules, Glob this session) undiscoverable: no guide, user guide or command file names it (question.md fact 2).
- Writes the INV-013 "person only" sentence nowhere, so an agent has no text telling it not to run the observer as a worker; Variant 1 lists this itself.
- Ties discoverability to two future events (the Q6 guard flip and the contract note) with no date, so the default becomes "never". The panel being off is a reason to describe what the tool does today, not to hide what already works.

**Variant 2.**
- Its main benefit (no test edit) is also available to a routing-table row, per strength 2, so it trades away recommender routing for a saving that may not exist.
- The prose section is not read by `/sc:recommend` for routing (`SKILL.md:50-54`, `:403`), so the observer stays invisible to the tool the core CLAUDE.md tells people to use when unsure ("Unsure which tool fits? Run `/sc:recommend`").
- It forces a spec change: OB-07 reworded from row to bullet and its acceptance items dropped (Variant 2 lists this itself), which is churn on a settled row for a smaller result.
- The "Orca coordination" section describes coordinator mechanics (Tasks, workers, `--unattended`, `:400-408`); a person-facing terminal dashboard is a looser fit there than a routing row whose intent column names the person's goal.

## Concessions

- Variant 3 as written overstates its own cost ("At least one routing test must change") and names `test_routing_refresh.py:33` as an edit. My reading suggests neither may be needed. If the owner picks Variant 3, the PR should try the routing table first and run the tests before naming any edit.
- Variant 3 leaves "which table" to the PR. That is a real weakness: the other-commands block cannot take it without changing `_OTHER_COMMANDS` (`:297-298`), so the answer should state "routing table" now.
- Variant 3 advertises a dashboard whose question panel is off on master (Q6). I did not confirm the guard in code (a grep of `src/superclaude/cli/observe/` showed a `questions: bool = False` parameter at `collector.py:154`, which is suggestive but not the guard itself): UNVERIFIED. The row text must describe only what is on.
- Variant 2's placement next to the never-as-worker rule (`:405`) is a genuinely good home for the person-only sentence. A combined answer (routing row plus a one-line pointer in "Orca coordination") would capture it at the cost of one more edit.
- Any routing row adds one more row a recommender run must match against; a loose intent phrase could mis-route a "show me status" request that `/sc:sweep` should own.

## Shared assumptions

| Id | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | The routing table, its mirror and the routing tests are all edited by #539 (question.md fact 3), so waiting avoids a rebase; for a prose-only bullet the guard is weaker but the byte-for-byte mirror copy still conflicts. |
| A-002 | QUALIFY | The observer is merged (PRs #503, #514) and its CLI entry point is stable enough to name, but its question panel is off (Q6), so the row should name the command and its current purpose only, not flags or panels that may change. |

## Per-point verdicts

| Point | Winner | Confidence | Reason |
|---|---|---|---|
| S-001 | tie | 95% | All three use the same five sections. |
| C-001 | 3 (tie with 2) | 80% | Make it discoverable now: the tool is merged and nothing names it; deferring has no end date. |
| C-002 | 3 | 75% | Only the routing table is read by `/sc:recommend` for routing (`SKILL.md:50-54`, `:403`). |
| C-003 | 3 (tie with 2) | 60% | By reading, a routing row with a terminal-only step needs no test edit, matching Variant 2's zero-edit benefit; not run. |
| C-004 | 3 (tie with 2) | 75% | "After #539" is a concrete, already-scheduled trigger (wave W3); Variant 1's trigger has no date. |
| C-005 | 3 | 85% | A row routes like any row; a bullet is outside the blocks the recommender extracts. |
| X-001 | 3 | 65% | Name the cost and describe only what is on; hiding a working tool costs more than an honest row. |
| X-002 | 3 | 55% | Accepting a test edit is fine if needed, and reading suggests none is needed for the routing table. |
| X-003 | 3 | 70% | Keeping OB-07 unchanged avoids spec churn; Variant 2 must rewrite it. |
| U-001 | 1 | 60% | Tying the advertised wording to the guard state is a valid point; Variant 3 should adopt it as a wording rule, not a delay. |
| U-002 | 2 | 70% | The marker-only reading of the tests is correct and valuable; it also shows the prose section is invisible to routing. |
| U-003 | 2 | 65% | The person-only sentence beside `:405` is a natural home; Variant 3 matches it in the row's notes cell. |
| U-004 | 3 | 80% | Same table people and `/sc:recommend` read; follows V5 D8 and the spec. |

## Overall ranking and unassigned pick

Ranking: Variant 3, then Variant 2, then Variant 1.

If I were not assigned a variant I would still pick Variant 3, amended: name the routing table (not "either table"), cite section `3.13`, put "person only, never a worker" in the notes cell, describe only what the observer does on master today, and run the routing tests before naming any test edit. If the owner values zero risk to the machine-read tables above recommender routing, Variant 2 is a close and acceptable second.
