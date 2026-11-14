# Adversarial Debate Transcript: Q12

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2, Round 2.5 invariant probe and Round 3 skipped: depth=quick)
- Convergence achieved: 100% (11 of 11 scored points have a majority)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 3, each a spawned general-purpose sub-agent (Variant 1 persona qa, Variant 2 persona analyzer, Variant 3 persona architect). No agent failures.
- Protocol: sc-adversarial-protocol, loaded by Skill call at Q11 in this session and applied as written here.
- Variant map: Variant 1 = proposal-A (no entry for now); Variant 2 = proposal-B (prose bullet in "Orca coordination"); Variant 3 = proposal-C (one routing table row after #539)

## Unassigned picks
- Advocate V1: Variant 2, with a wording rule from Variant 1 (say the questions panel is off until the guard-flip PR).
- Advocate V2: Variant 3, with the "person only" sentence in the row's notes cell and as a bullet beside the never-as-worker text.
- Advocate V3: Variant 3, amended: name the routing table, cite a numbered section, "person only" in the notes cell, describe only what works on master, run the tests before naming any test edit.
- Result: 2 of 3 pick Variant 3; 1 of 3 picks Variant 2; none picks Variant 1.

## Orchestrator spot-checks of new evidence raised in Round 1
- `src/superclaude/skills/sc-recommend/SKILL.md:50-54` (and its plugin copy): re-read. The recommender extracts only three marker blocks (level table, routing table, other commands), "never by line number or heading text". A bullet in "Orca coordination" is outside all three, so it is not routable. Confirmed; this resolves Variant 2's own UNVERIFIED cost against it.
- `tests/core/test_how_we_work_routing_table.py:105`: `_TOKEN_RE` matches only a backtick followed by a slash, so `` `superclaude observe` `` yields no command token to resolve. `:109` and `:336-340`: every routing row's section cell must name a numbered heading. Confirmed.
- `HOW-WE-WORK.md:376`: the `resume` row already has a terminal step "named conversation: terminal `ccsession <name>`". Confirmed precedent for a non-slash step.
- `HOW-WE-WORK.md:335`: the `/sc:sweep` other-commands entry says "Coordinator or person only, never a worker." Confirmed pattern for the INV-013 sentence.
- Consequence: INV-029 (an invariant-probe finding that a CLI-only entry fits neither table without a test edit) is confirmed for the other-commands table and appears overstated for the routing table. Not run; UNVERIFIED until the routing tests run on the PR branch.

## Scoring Matrix

| Diff Point | Level | V1 adv | V2 adv | V3 adv | Winner | Confidence | Evidence Summary |
|---|---|---|---|---|---|---|---|
| S-001 | L1 | tie | tie | tie | tie (agreed) | 95% | Same five sections. |
| C-001 | L2 | 2,3 | 2,3 | 3 (tie 2) | Variants 2 and 3 over 1 | 85% | A merged tool with no guide mention should be findable; even Variant 1's advocate conceded. |
| C-002 | L2 | 2 | 3 | 3 | Variant 3 | 75% | Only marker blocks are read by `/sc:recommend` (SKILL.md:50-54). |
| C-003 | L3 | 1,2 | 2 | 3 (tie 2) | Variant 2 | 65% | Verified zero test edits for a prose bullet; Variant 3 may also need none (UNVERIFIED). |
| C-004 | L2 | 1 | 2,3 | 3,2 | Variants 2 and 3 | 70% | "After #539" is a scheduled trigger; Variant 1's trigger is undated. |
| C-005 | L2 | 3 | 3 | 3 | Variant 3 | 92% | Unanimous: only a table row is routed. |
| X-001 | L2 | 1 | 3 | 3 | Variant 3 | 65% | Name the off panel and describe only what works; hiding the tool costs more. |
| X-002 | L3 | 1,2 | 2 | 3 | Variant 2 | 55% | Avoiding a test-edit precedent is cheaper; weakened by the finding that the routing table may need no edit. |
| X-003 | L1 | 1 | 3 | 3 | Variant 3 | 65% | Keeping OB-07 as written avoids spec churn. |
| A-001 | L3 | QUALIFY | QUALIFY | ACCEPT | agreed: QUALIFY | 75% | Waiting for #539 is right; for prose the reason is text conflict, not tests. |
| A-002 | L2 | REJECT | QUALIFY | QUALIFY | agreed: QUALIFY | 70% | Name the command and current purpose only; no flags or panels that will change. |
| U-001 | n/a | 1 | 3 | 1 | Variant 1 (as a wording rule) | 60% | Adopted as "describe only what is on", not as a delay. |
| U-002 | n/a | 2 | 2 | 2 | Variant 2 (valid) | 88% | Tests read only marker blocks. |
| U-003 | n/a | 2 | 2 | 2 | Variant 2 (valid) | 72% | "Person only" belongs beside the never-as-worker text. |
| U-004 | n/a | 3 | 3 | 3 | Variant 3 (valid) | 75% | The table is what people and `/sc:recommend` read. |

## Convergence Assessment
- Points resolved: 11 of 11 (S, C, X and A points)
- Alignment: 100%
- Threshold: 80%
- Taxonomy coverage: L1 2, L2 6, L3 3; all levels covered
- Invariant gate: not applied (Round 2.5 skipped at depth quick)
- Status: CONVERGED
- Unresolved points: none on scored points; the overall pick is 2 of 3 for Variant 3

## Round 1: Advocate Statements

The three statements follow verbatim.


---

### Round 1 advocate statement: Variant 1 (no routing entry for now)

Advocate: Variant 1 (proposal A). Persona: qa (edge cases, failure scenarios). Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless they start with F (the Q12 folder).

#### Position summary

Variant 1 is the lowest-risk answer: it changes no file, needs no test edit, cannot collide with PR #539, and does not freeze a routing entry for a tool whose usage text will change when its guard flips and its scope sentence (Q6) is written. OB-07 is a sink that nothing waits on (merged-requirements.md:779), so deferring it blocks nothing, and the question is asked again once the observer's final shape is known.

#### Steelman

**Variant 2 (one prose bullet in "Orca coordination").** Its best case: the observer is built and merged (PRs #503, #514) yet invisible; a single bullet in the prose section fixes that for people reading the guide, sits next to the `/sc:sweep` bullet it complements (`src/superclaude/core/HOW-WE-WORK.md:406`, re-read), and gives the INV-013 "person only" sentence a home next to the existing "Some commands are never workers" bullet (`HOW-WE-WORK.md:405`, re-read). The section starts at line 398, after the routing-table end marker at line 396 (re-read), so the two table tests that parse marked blocks (`tests/core/test_how_we_work_routing_table.py:22-24`, re-read) do not see it. That is the cheapest way to get partial discoverability with no test edit. This is a strong, well-grounded proposal.

**Variant 3 (one routing-table row, own PR after #539).** Its best case: it is the spec's own recommended answer (merged-requirements.md:539) and the source review's verdict (V5 D8). A table row is the only shape `/sc:recommend` actually routes from: its parse rule reads the routing-table and other-commands blocks only (`src/superclaude/skills/sc-recommend/SKILL.md:53-56`, re-read). The change is one row plus named test edits, reversible by one PR, and OB-07 already lists the exact acceptance checks (merged-requirements.md:255). If the goal is "an agent asking how to watch workers is pointed at the observer", only Variant 3 delivers it.

#### Strengths claimed

1. **Zero blast radius.** No edit to `HOW-WE-WORK.md`, its byte-for-byte plugin mirror, the sc-recommend table, or any of the 13 test files that read the guide (grep of `tests/` for "HOW-WE-WORK", 13 files, including `tests/commands/test_routing_plugin_parity.py` and `tests/recommend/test_routing_refresh.py`). Nothing can fail in CI because nothing changed.
2. **No collision with #539.** PR #539 edits the guide, its mirror, `tests/core/test_how_we_work_routing_table.py` (which now lists `sc:sweep` at line 34) and `tests/recommend/test_routing_refresh.py:33` (`_POST_REFRESH_ADDITIONS` includes `sweep`, re-read). Variants 2 and 3 must both wait and rebase; Variant 1 has no rebase risk at all.
3. **Avoids a stale entry.** The observer's usage is still moving. Its `--questions` read is gated by `QUESTION_GATE_PASSED = False` (`src/superclaude/cli/observe/commands.py:63-67`, re-read), and OB-06, the guard-flip PR, must add an owner scope sentence ("this Run only" or "any Run my terminal holds") that the code enforces (merged-requirements.md:254). Any routing text written now either omits `--questions` (incomplete) or describes a flag that fails with exit 1 (`commands.py:185-186`). Edge case: a person told by the guide to run `superclaude observe --questions` today gets a refusal message. Waiting removes that failure mode.
4. **Keeps the two machine-read tables honest.** INV-029 (MEDIUM) says a CLI-only entry fits neither table without a test edit (`test_how_we_work_routing_table.py:193-205` needs 8 cells; `:297-298` asserts `members == _OTHER_COMMANDS` from the first backticked slash token, re-read). Variant 1 does not set a precedent of loosening a test to admit a non-slash entry.
5. **Blocks nothing.** OB-07 is a sink (merged-requirements.md:779); its only inputs are SW-05, K-ROUTE and Q12 (merged-requirements.md:807, per question.md). Deferring costs no downstream work item.
6. **Coherent revisit trigger.** The trigger (guard flipped and the observer-sweep contract note written) lines up with work already planned: OB-06 and XC-05 (merged-requirements.md:254, :135). At that point a routing entry can describe the finished tool in one edit instead of two.

#### Weaknesses identified in others

**Variant 2.**
- Its stated risk "UNVERIFIED how `/sc:recommend` weighs prose" can now be answered: `/sc:recommend` routes from the routing-table block and, on `no_match`, the other-commands block only (`sc-recommend/SKILL.md:53-54`). A prose bullet is not routed. So Variant 2 pays a full PR cycle (worker, mirror copy, `/sc:pr-submit --monitor 3`, review wait) for discoverability by human readers only, while the main machine route stays as dark as in Variant 1.
- It rewrites the spec's OB-07 row from "row" to "bullet" and drops its test acceptance items (variant-2-original.md:10), which is spec churn for a partial result, and it leaves open whether a row is still wanted later (variant-2-original.md:27). A later row would then be a second PR on the same lines.
- It does not address the guard edge case (X-001 is "Not addressed" in diff-analysis.md:30): the bullet would advertise the observer with no word on `--questions` refusing until OB-06.
- Its "no test edits" claim holds for the two table tests, but the guide is read by 13 test files; I found no test that pins the Orca section text (grep for "Orca coordination" in `tests/`: no hit), so this risk is small, not zero.

**Variant 3.**
- It requires at least one test edit to admit a CLI-only entry (variant-3-original.md:22), and it defers the choice of table into the PR (variant-3-original.md:28). That leaves the hardest part of the change undecided at approval time: the owner approves a row without knowing whether the 8-cell routing table or the slash-only other-commands table is bent.
- The routing table needs resolvable steps (question.md fact 3, citing `test_how_we_work_routing_table.py:193-205`), and `/sc:recommend` hands steps off as labelled steps (`sc-recommend/SKILL.md:53`). A CLI the person starts in a terminal is not a step an agent should run, so a row may route agents toward a tool INV-013 says they must not run. Edge case: `/sc:recommend "watch my workers"` from a worker session returns the observer row; the "person only" note is the only guard.
- It accepts advertising the observer while its question panel is off (variant-3-original.md:24) and does not say how the row is updated when OB-06 changes usage, so a second edit to the same row is likely.
- It waits on #539 like Variant 2, so it delivers nothing sooner than Variant 1's revisit in practice if OB-06 follows soon after.

#### Concessions

- **Discoverability stays at zero.** No guide, user guide or command file names `superclaude observe` today (question.md fact 2; variant-1-original.md:21). A person asking "how do I see my workers" gets no pointer. This is Variant 1's main cost and it is real.
- **INV-013 stays unwritten.** The never-as-worker list names slash commands only (question.md fact 4), so nothing tells an agent not to run the observer as a worker. INV-013 is LOW and the observer makes no questions call while the guard is False (`commands.py:66`), but an unscoped listing across all Runs is still possible.
- **The guard argument is narrower than Variant 1's text implies.** The guard gates only the opt-in `--questions` flag (`commands.py:169-170`); the rest of the dashboard works today. "Advertising a dashboard whose question panel is off" is a reason to word the entry carefully, not proof the tool is unfit to route to.
- **Variant 1 equals the default.** The default if Q12 is unanswered is "OB-07 does not start" (merged-requirements.md:539). Variant 1 adds only a dated ledger entry and a revisit trigger. The trigger has no date: XC-05 and OB-06 depend on Q6, Q23 and live tests (OB-03, OB-04), so "later" may be long.
- **The "words do not match the sweep's" claim** (variant-1-original.md:17) rests on the contract note being unwritten (XC-05); I did not verify a specific wording mismatch between the observer and `/sc:sweep`. UNVERIFIED.

#### Shared assumptions

- **A-001 (any guide edit must wait for #539): QUALIFY.** True for the table blocks and the test files #539 edits; for a prose bullet it is a merge-conflict courtesy, not a test guard, but #539 adds its `/sc:sweep` bullet in the same section (`HOW-WE-WORK.md:406`) and the mirror must stay byte-identical, so waiting is still the safe order.
- **A-002 (the observer is stable enough to route people to): REJECT (for now).** Its `--questions` behaviour and scope rule change in OB-06 (merged-requirements.md:254; `commands.py:63-67`), so routing text written today is likely to need a second edit; this is Variant 1's core reason to wait.

#### Per-point verdicts

| Point | Winner | Confidence | One-line reason |
|---|---|---|---|
| S-001 | tie | 95% | All three use the same five sections. |
| C-001 | 2 and 3 (tie) | 65% | Making a built tool findable has real value; Variant 1 only buys time. |
| C-002 | 2 | 60% | A prose bullet fits a CLI without bending a machine-read table, though `/sc:recommend` does not route it. |
| C-003 | 1 and 2 (tie) | 75% | Neither needs a test edit; Variant 3 needs at least one (INV-029). |
| C-004 | 1 | 55% | Waiting for the guard flip avoids writing the entry twice; the trigger is undated, which costs confidence. |
| C-005 | 3 | 80% | Only a table row is routed (`sc-recommend/SKILL.md:53-56`); Variants 1 and 2 are both not routed. |
| X-001 | 1 | 55% | Only Variant 1 treats the off guard as a reason; weakened because the guard gates one opt-in flag. |
| X-002 | 1 and 2 (tie) | 70% | Avoiding a test edit for one CLI entry keeps the tables' slash-only contract intact. |
| X-003 | 1 | 55% | Variant 1 leaves the OB-07 row intact and marked deferred; Variant 2 rewrites it, Variant 3 keeps it but leaves the table choice open. |
| U-001 | 1 | 60% | Tying discoverability to the finished tool prevents a stale entry; value limited by the undated trigger. |
| U-002 | 2 | 85% | Verified: the tests read only the marked blocks and the Orca section is outside them (lines 396, 398). |
| U-003 | 2 | 80% | The never-workers bullet at `HOW-WE-WORK.md:405` is the natural home for "person only". |
| U-004 | 3 | 70% | The table is what `/sc:recommend` reads; it also follows V5 D8 and the spec. |

#### Overall ranking and unassigned pick

Ranking as advocate (best first): **Variant 1, Variant 2, Variant 3.** Variant 1 is the only answer with no failure scenarios to manage now (no test edit, no rebase, no entry that goes stale at OB-06); Variant 2 is a cheap, safe middle path; Variant 3 carries the most edge cases (test loosening, table choice left open, worker-routing exposure).

Unassigned pick: **Variant 2.** Weighing the evidence honestly, the zero-discoverability cost of Variant 1 is real, and Variant 2 removes most of it for a one-bullet PR with no test edits and a natural home for INV-013. I would pair it with one wording rule taken from Variant 1: the bullet says `--questions` is off until the guard-flip PR, so when OB-06 lands the only edit is removing that clause.

---

### Round 1 advocate statement: Variant 2 (one prose bullet, no table row)

Paths below are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless they start with `F/`. Every file:line was re-read on 2026-11-14 unless marked UNVERIFIED.

#### Position summary

Variant 2 makes the merged observer findable now, puts the "person only" rule (INV-013) right beside the guide's existing never-as-worker text, and touches no machine-read block, so no routing test changes. Its real weakness, which I confirmed and concede below, is that `/sc:recommend` does not read the "Orca coordination" section, so the bullet helps people and agents who read the guide but is not routable; the fix is to move the same sentence into a place the recommender does read, not to fall back to deferral.

#### Steelman

**Variant 1 (no entry for now), strongest form.** The observer is not finished as a coordination tool: its coordinator-questions panel is off on master (owner question Q6) and the contract note that aligns its words with the sweep's is unwritten. Advertising it in the guide that agents route from invites use before the two tools agree, and every guide edit collides with PR #539, which edits the same guide, its mirror and both routing tests (question.md fact 3). OB-07 is a sink that nothing waits on (merged-requirements.md:779, as cited in question.md), so deferring costs nothing downstream and keeps the guide stable until the tool is complete. Asking again later is cheap and avoids writing something twice.

**Variant 3 (one routing table row), strongest form.** The owner's question is literally "a routing row?", and the spec, the adjudication and the source debate all recommend yes (merged-requirements.md:539, re-read; variant-5-original.md:258-259 as cited in question.md). The routing table is the one surface `/sc:recommend` matches against: its Step 0 extracts only the level table, the routing table and the other-commands block by their markers (`src/superclaude/skills/sc-recommend/SKILL.md:50-54`). A row there is the only form that both people and the recommender use. The test cost may be smaller than INV-029 says: from my reading, the routing-table tests that loop over every row (`tests/core/test_how_we_work_routing_table.py:193-340`) check slash tokens only (`_TOKEN_RE` at `:105` matches spans that start with a backtick and a slash), so a step written as `` `superclaude observe` `` is not looked up as a command. Small, reversible, matches the planned OB-07 shape with no spec churn.

#### Strengths claimed

1. **No machine-read block is touched, so no test edit is needed (verified).** The test file defines exactly three marker pairs (`tests/core/test_how_we_work_routing_table.py:22-24`) and reads blocks only through `_block(text, begin, end)` (`:116-118`). In the guide, the routing table ends at `src/superclaude/core/HOW-WE-WORK.md:396` (`<!-- /routing-table -->`) and "## Orca coordination" starts at `:398`, outside every block. INV-029 therefore cannot fire, and `_OTHER_COMMANDS` (`:27` onward) and the membership assertion (`:297-298`) stay untouched. The only whole-guide check that applies is ASCII (`:343-348`), which one plain sentence meets.
2. **The person-only rule lands next to its sibling text.** The Orca section already holds "**Some commands are never workers.**" (`HOW-WE-WORK.md:405`) and the `/sc:sweep` "itself never a worker" bullet (`:406`). The never-as-worker list in `src/superclaude/core/WORKER-CONTRACT.md:23` names slash commands only, which is exactly the gap INV-013 describes; a bullet beside `:405` closes it in the one section about who may run what.
3. **It fixes the real present-day problem.** The guide has no mention of `superclaude observe` (my grep of `HOW-WE-WORK.md` for "observe" hit only unrelated words such as "observed" at `:16`, `:356`, `:390`), while the code exists (`src/superclaude/cli/observe/` holds `commands.py`, `collector.py`, `questions.py` and others). Variant 2 makes it findable; Variant 1 does not.
4. **Lowest exposure to change in the observer itself.** A one-sentence bullet naming only `superclaude observe`, with no flags, carries no flag or step contract that can go stale (relevant to A-002), and it has no `section`, `level` or `mandatory_flags` cells for tests to validate.
5. **Same merge order as Variant 3, smaller diff.** It waits for #539 like Variant 3, but its diff is one guide line plus the byte-for-byte mirror (project CLAUDE.md, "Key Documentation Files"); review and rebase cost is minimal.

#### Weaknesses identified in others

**Variant 1.**
- It leaves the INV-013 "person only" sentence written nowhere, while the never-as-worker list stays slash-command only (`WORKER-CONTRACT.md:23`). The risk it names (an agent running the observer as a worker) persists for the whole deferral.
- It has no trigger date or owner: "asked again then" depends on Q6 and on an unwritten contract note, two other open items. A built and merged tool (PRs #503 and #514, question.md fact 1) stays invisible indefinitely.
- The "panel is off" argument is about one panel, not the tool. The rest of the observer works today (UNVERIFIED in a live run; I only confirmed the code exists), and a guide line can describe what the tool shows now.

**Variant 3.**
- It leaves the key design choice open: "The PR decides which table carries the row." The other-commands table is the wrong fit by construction: the first cell of every row must yield a slash token (`:297`, `_TOKEN_RE` at `:105`), so a CLI-only row there breaks `members == _OTHER_COMMANDS` (`:298`) or needs a test change.
- A routing row's `section` cell must name a numbered heading (`test_every_section_reference_is_a_heading`, `:336-340`; `_HEADING_RE` at `:109` matches only headings that start with a number). "Orca coordination" has no number, so the row cannot point at the section that holds the who-may-run-what rules unless it cites an unrelated numbered section or the guide gains a new numbered heading. That is guide-structure churn Variant 2 avoids.
- Matched mode in `/sc:recommend` runs Step C on the row's "selected commands/skills" (`SKILL.md:62`). Whether Step C accepts a step that is a shell CLI rather than a command or skill is UNVERIFIED; precedent exists for non-command steps ("or a plain edit" in the `small-change` row, `HOW-WE-WORK.md:356`), so this is a risk, not a proven defect.
- It accepts a test edit (X-002) and sets a precedent for non-slash entries in machine-read blocks, if INV-029 is right for whichever table it picks.

#### Concessions

1. **Variant 2 as written is not routable by `/sc:recommend` (verified; the proposal marked it UNVERIFIED).** Step 0 extracts three blocks "by their markers, never by line number or heading text" (`src/superclaude/skills/sc-recommend/SKILL.md:50-54`). The Orca section is outside all three. A no-match then goes to the cache or to Phase 0 live enumeration of commands, skills, agents and templates (`SKILL.md:108`, `:138`), which would not list a CLI subcommand. So C-005 goes against Variant 2. The agent does Read the whole guide in Step 0, so the bullet is in its context, but no rule tells it to route from prose.
2. **INV-029 may be overstated for the routing table.** From the tests I read (`:193-340`), a routing row whose steps hold `` `superclaude observe` `` with `mandatory_flags` set to `-` seems to pass, provided its `section` cell names a numbered heading. I did not read every row-looping test after `:1090`, so this is partly UNVERIFIED. If true, Variant 2's "no test edit" edge over Variant 3 shrinks to "no guide-structure decision".
3. **A better version of Variant 2 exists and I would adopt it.** The other-commands block already carries a prose line after its table: "One more user-facing skill: `/confidence-check` checks readiness before implementation." It sits inside `<!-- other-commands:v1 -->`, just before `<!-- /other-commands -->` (`HOW-WE-WORK.md`, between `:319` and `:339`). Tests count only lines that start with `|` as table rows (`_table_rows`, `:125-126`), and the live-reference loop checks only slash tokens (`:311-312`). One prose sentence there about `superclaude observe`, person only, would sit inside a block `/sc:recommend` extracts (`SKILL.md:54`) with no test edit. Whether the recommender's no-match path then proposes a CLI that is not a command is UNVERIFIED (`SKILL.md:54` speaks of "a command it names").
4. Variant 2 rewrites the OB-07 spec row and drops its test-edit acceptance items; that is spec churn Variant 3 avoids (X-003).

#### Shared assumptions

- **A-001 (any guide edit waits for #539): QUALIFY.** For a prose bullet the reason is not the tests (they never read `:398` onward) but plain textual conflict: #539 edits the same guide, its mirror and the same Orca section (question.md facts 3 and 5); waiting is cheap because OB-07 is a sink.
- **A-002 (the observer is stable enough to route to): QUALIFY.** The code is present (`src/superclaude/cli/observe/`), but flag stability is UNVERIFIED; this favors an entry that names only `superclaude observe` with no flags, which Variant 2's bullet does and a Variant 3 row can also do.

#### Per-point verdicts

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

#### Overall ranking and unassigned pick

Ranking, best first: **Variant 2 (with the sentence placed as a prose line inside the other-commands block, next to the `/confidence-check` line), then Variant 3, then Variant 1.** Variant 2 exactly as written (Orca section) ties Variant 3 at best, because it fixes discoverability for readers and the INV-013 gap but not routing.

Unassigned pick: **Variant 3.** The owner asked about a routing row, and verified evidence (`SKILL.md:50-54`) shows only a marker-block entry is routable; a routing-table row is the documented, reliably matched form, and its test cost may be smaller than INV-029 claims. I would add Variant 2's one contribution to it: write the "person only" sentence in the row's notes cell and also as a bullet beside `HOW-WE-WORK.md:405`, which costs one more guide line and no test edit.

---

### Round 1 advocate statement: Variant 3 (one routing row, own small PR after #539)

Persona: architect. Depth: quick. Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode`. Every line number below was re-read in this session unless marked UNVERIFIED.

#### Position summary

Variant 3 is the best answer because the routing table is the only part of `HOW-WE-WORK.md` that `/sc:recommend` actually reads for routing, so it is the only placement that makes the observer findable by both people and the recommender. Reading the tests shows the cost Variant 3 names for itself (INV-029) is smaller than stated: a routing-table row whose step is a plain terminal command already has a precedent and appears to pass the current tests with no test edit (by reading, not run).

#### Steelman

**Variant 1 (no entry for now).** The strongest form: do not advertise a tool before it is complete. The observer's coordinator-questions panel is off on master (owner question Q6), and the contract note that aligns its words with `/sc:sweep` is unwritten. A routing entry written now would describe a half-switched-on tool and would have to be rewritten when the panel turns on, so waiting means one edit instead of two, no rebase against #539, and zero risk to the two machine-read test tables (`tests/core/test_how_we_work_routing_table.py:193-205`, `:297-298`). OB-07 is a sink (nothing waits on it, merged-requirements.md:779 per question.md), so deferring it blocks nothing.

**Variant 2 (one bullet in "Orca coordination").** The strongest form: put the observer exactly where its sibling already lives. The "Orca coordination" section (`src/superclaude/core/HOW-WE-WORK.md:398-408`) already carries the `/sc:sweep` bullet (`:406`) and the never-as-worker rule (`:405`), so "person only, never as a worker" sits next to the rule it extends. The two table tests read only the marked blocks (markers defined at `tests/core/test_how_we_work_routing_table.py:22-24`), so a prose bullet needs no test edit at all and cannot destabilise the routing contract. It is the smallest change that still makes the tool discoverable to a human reading the guide.

#### Strengths claimed

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

#### Weaknesses identified in others

**Variant 1.**
- Leaves a merged, shipped tool (`src/superclaude/cli/observe/` exists with 12 modules, Glob this session) undiscoverable: no guide, user guide or command file names it (question.md fact 2).
- Writes the INV-013 "person only" sentence nowhere, so an agent has no text telling it not to run the observer as a worker; Variant 1 lists this itself.
- Ties discoverability to two future events (the Q6 guard flip and the contract note) with no date, so the default becomes "never". The panel being off is a reason to describe what the tool does today, not to hide what already works.

**Variant 2.**
- Its main benefit (no test edit) is also available to a routing-table row, per strength 2, so it trades away recommender routing for a saving that may not exist.
- The prose section is not read by `/sc:recommend` for routing (`SKILL.md:50-54`, `:403`), so the observer stays invisible to the tool the core CLAUDE.md tells people to use when unsure ("Unsure which tool fits? Run `/sc:recommend`").
- It forces a spec change: OB-07 reworded from row to bullet and its acceptance items dropped (Variant 2 lists this itself), which is churn on a settled row for a smaller result.
- The "Orca coordination" section describes coordinator mechanics (Tasks, workers, `--unattended`, `:400-408`); a person-facing terminal dashboard is a looser fit there than a routing row whose intent column names the person's goal.

#### Concessions

- Variant 3 as written overstates its own cost ("At least one routing test must change") and names `test_routing_refresh.py:33` as an edit. My reading suggests neither may be needed. If the owner picks Variant 3, the PR should try the routing table first and run the tests before naming any edit.
- Variant 3 leaves "which table" to the PR. That is a real weakness: the other-commands block cannot take it without changing `_OTHER_COMMANDS` (`:297-298`), so the answer should state "routing table" now.
- Variant 3 advertises a dashboard whose question panel is off on master (Q6). I did not confirm the guard in code (a grep of `src/superclaude/cli/observe/` showed a `questions: bool = False` parameter at `collector.py:154`, which is suggestive but not the guard itself): UNVERIFIED. The row text must describe only what is on.
- Variant 2's placement next to the never-as-worker rule (`:405`) is a genuinely good home for the person-only sentence. A combined answer (routing row plus a one-line pointer in "Orca coordination") would capture it at the cost of one more edit.
- Any routing row adds one more row a recommender run must match against; a loose intent phrase could mis-route a "show me status" request that `/sc:sweep` should own.

#### Shared assumptions

| Id | Response | Reason |
|---|---|---|
| A-001 | ACCEPT | The routing table, its mirror and the routing tests are all edited by #539 (question.md fact 3), so waiting avoids a rebase; for a prose-only bullet the guard is weaker but the byte-for-byte mirror copy still conflicts. |
| A-002 | QUALIFY | The observer is merged (PRs #503, #514) and its CLI entry point is stable enough to name, but its question panel is off (Q6), so the row should name the command and its current purpose only, not flags or panels that may change. |

#### Per-point verdicts

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

#### Overall ranking and unassigned pick

Ranking: Variant 3, then Variant 2, then Variant 1.

If I were not assigned a variant I would still pick Variant 3, amended: name the routing table (not "either table"), cite section `3.13`, put "person only, never a worker" in the notes cell, describe only what the observer does on master today, and run the routing tests before naming any test edit. If the owner values zero risk to the machine-read tables above recommender routing, Variant 2 is a close and acceptable second.
