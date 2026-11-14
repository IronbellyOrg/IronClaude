# Round 1 advocate statement: Variant 1 (no routing entry for now)

Advocate: Variant 1 (proposal A). Persona: qa (edge cases, failure scenarios). Paths are relative to the worktree root `/home/coder/workspaces/worktrees/IronClaude/issue-339-orchestrator-mode` unless they start with F (the Q12 folder).

## Position summary

Variant 1 is the lowest-risk answer: it changes no file, needs no test edit, cannot collide with PR #539, and does not freeze a routing entry for a tool whose usage text will change when its guard flips and its scope sentence (Q6) is written. OB-07 is a sink that nothing waits on (merged-requirements.md:779), so deferring it blocks nothing, and the question is asked again once the observer's final shape is known.

## Steelman

**Variant 2 (one prose bullet in "Orca coordination").** Its best case: the observer is built and merged (PRs #503, #514) yet invisible; a single bullet in the prose section fixes that for people reading the guide, sits next to the `/sc:sweep` bullet it complements (`src/superclaude/core/HOW-WE-WORK.md:406`, re-read), and gives the INV-013 "person only" sentence a home next to the existing "Some commands are never workers" bullet (`HOW-WE-WORK.md:405`, re-read). The section starts at line 398, after the routing-table end marker at line 396 (re-read), so the two table tests that parse marked blocks (`tests/core/test_how_we_work_routing_table.py:22-24`, re-read) do not see it. That is the cheapest way to get partial discoverability with no test edit. This is a strong, well-grounded proposal.

**Variant 3 (one routing-table row, own PR after #539).** Its best case: it is the spec's own recommended answer (merged-requirements.md:539) and the source review's verdict (V5 D8). A table row is the only shape `/sc:recommend` actually routes from: its parse rule reads the routing-table and other-commands blocks only (`src/superclaude/skills/sc-recommend/SKILL.md:53-56`, re-read). The change is one row plus named test edits, reversible by one PR, and OB-07 already lists the exact acceptance checks (merged-requirements.md:255). If the goal is "an agent asking how to watch workers is pointed at the observer", only Variant 3 delivers it.

## Strengths claimed

1. **Zero blast radius.** No edit to `HOW-WE-WORK.md`, its byte-for-byte plugin mirror, the sc-recommend table, or any of the 13 test files that read the guide (grep of `tests/` for "HOW-WE-WORK", 13 files, including `tests/commands/test_routing_plugin_parity.py` and `tests/recommend/test_routing_refresh.py`). Nothing can fail in CI because nothing changed.
2. **No collision with #539.** PR #539 edits the guide, its mirror, `tests/core/test_how_we_work_routing_table.py` (which now lists `sc:sweep` at line 34) and `tests/recommend/test_routing_refresh.py:33` (`_POST_REFRESH_ADDITIONS` includes `sweep`, re-read). Variants 2 and 3 must both wait and rebase; Variant 1 has no rebase risk at all.
3. **Avoids a stale entry.** The observer's usage is still moving. Its `--questions` read is gated by `QUESTION_GATE_PASSED = False` (`src/superclaude/cli/observe/commands.py:63-67`, re-read), and OB-06, the guard-flip PR, must add an owner scope sentence ("this Run only" or "any Run my terminal holds") that the code enforces (merged-requirements.md:254). Any routing text written now either omits `--questions` (incomplete) or describes a flag that fails with exit 1 (`commands.py:185-186`). Edge case: a person told by the guide to run `superclaude observe --questions` today gets a refusal message. Waiting removes that failure mode.
4. **Keeps the two machine-read tables honest.** INV-029 (MEDIUM) says a CLI-only entry fits neither table without a test edit (`test_how_we_work_routing_table.py:193-205` needs 8 cells; `:297-298` asserts `members == _OTHER_COMMANDS` from the first backticked slash token, re-read). Variant 1 does not set a precedent of loosening a test to admit a non-slash entry.
5. **Blocks nothing.** OB-07 is a sink (merged-requirements.md:779); its only inputs are SW-05, K-ROUTE and Q12 (merged-requirements.md:807, per question.md). Deferring costs no downstream work item.
6. **Coherent revisit trigger.** The trigger (guard flipped and the observer-sweep contract note written) lines up with work already planned: OB-06 and XC-05 (merged-requirements.md:254, :135). At that point a routing entry can describe the finished tool in one edit instead of two.

## Weaknesses identified in others

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

## Concessions

- **Discoverability stays at zero.** No guide, user guide or command file names `superclaude observe` today (question.md fact 2; variant-1-original.md:21). A person asking "how do I see my workers" gets no pointer. This is Variant 1's main cost and it is real.
- **INV-013 stays unwritten.** The never-as-worker list names slash commands only (question.md fact 4), so nothing tells an agent not to run the observer as a worker. INV-013 is LOW and the observer makes no questions call while the guard is False (`commands.py:66`), but an unscoped listing across all Runs is still possible.
- **The guard argument is narrower than Variant 1's text implies.** The guard gates only the opt-in `--questions` flag (`commands.py:169-170`); the rest of the dashboard works today. "Advertising a dashboard whose question panel is off" is a reason to word the entry carefully, not proof the tool is unfit to route to.
- **Variant 1 equals the default.** The default if Q12 is unanswered is "OB-07 does not start" (merged-requirements.md:539). Variant 1 adds only a dated ledger entry and a revisit trigger. The trigger has no date: XC-05 and OB-06 depend on Q6, Q23 and live tests (OB-03, OB-04), so "later" may be long.
- **The "words do not match the sweep's" claim** (variant-1-original.md:17) rests on the contract note being unwritten (XC-05); I did not verify a specific wording mismatch between the observer and `/sc:sweep`. UNVERIFIED.

## Shared assumptions

- **A-001 (any guide edit must wait for #539): QUALIFY.** True for the table blocks and the test files #539 edits; for a prose bullet it is a merge-conflict courtesy, not a test guard, but #539 adds its `/sc:sweep` bullet in the same section (`HOW-WE-WORK.md:406`) and the mirror must stay byte-identical, so waiting is still the safe order.
- **A-002 (the observer is stable enough to route people to): REJECT (for now).** Its `--questions` behaviour and scope rule change in OB-06 (merged-requirements.md:254; `commands.py:63-67`), so routing text written today is likely to need a second edit; this is Variant 1's core reason to wait.

## Per-point verdicts

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

## Overall ranking and unassigned pick

Ranking as advocate (best first): **Variant 1, Variant 2, Variant 3.** Variant 1 is the only answer with no failure scenarios to manage now (no test edit, no rebase, no entry that goes stale at OB-06); Variant 2 is a cheap, safe middle path; Variant 3 carries the most edge cases (test loosening, table choice left open, worker-routing exposure).

Unassigned pick: **Variant 2.** Weighing the evidence honestly, the zero-discoverability cost of Variant 1 is real, and Variant 2 removes most of it for a one-bullet PR with no test edits and a natural home for INV-013. I would pair it with one wording rule taken from Variant 1: the bullet says `--questions` is off until the guard-flip PR, so when OB-06 lands the only edit is removing that clause.
