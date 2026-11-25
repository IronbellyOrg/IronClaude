### Variant 2 Advocate (opus:analyzer) for CLAY

## Position summary
Under the owner's rule, CLAY should not win on where the facts come from: the sweep stays the one source of session facts. CLAY does show five benefits that are evidenced, can be separated from that question, and that OURS lacks: per-issue plain-English text with GitHub and ClickUp reads, a script check that stops a bad report and never drops an item silently, a living page rebuilt without a model call, the nine-row reason table, and the cap of 5 notices. Each should be adopted as a HYBRID on top of OURS's base.

## Steelman of Variant 1
At its strongest, OURS argues three things.

1. Every extra collector adds another place where two readers can disagree about the same session. Master already has two collectors that do not talk to each other (`observe/` has no reference to `sweep`, variant-1 line 20). A third makes the problem worse.
2. The sweep is a script with no model. It reads Orca only through a fixed list of commands (M:src/superclaude/cli/sweep/probes.py:49-56) and has eight classes backed by proof rules, including "could not determine" (M:src/superclaude/cli/sweep/models.py:50-59). It is the only piece cheap enough to run every 5 minutes.
3. The owner's surfaces forbid recommendations (M:src/superclaude/skills/sc-sweep-protocol/SKILL.md:61). CLAY's report sends DMs and makes commits.

All three points are correct. The cap and the table are also spec only: no `escalate` verb exists yet (variant-1 line 26).

## Strengths claimed
1. **A capability OURS lacks: per-issue plain-English summaries with GitHub and ClickUp data.** The sweep allows only Orca and worktree commands (probes.py:49-56). Issue 409's own "Alignment decisions" item 3 says the sweep "has no per-session summary text". The report already writes per-item Done, Still to do, Needs you and links, and `check.py` enforces that layout (M:src/superclaude/skills/agent-work-report/SKILL.md:10). OURS admits the gap may stay "unmet for months" (variant-1 line 38). **HYBRID:** keep these parts as the work-item source.
2. **A verified check against silent loss.** Every item open in the previous report must be listed again or closed with a reason the source confirmed. A failed read carries items forward and never closes them. Every source not read is listed under "Not checked". Delivery is blocked until `check.py` passes (SKILL.md:21-24). Neither the sweep nor the observer has a check that compares one run with the previous one (UNVERIFIED beyond the two papers; neither paper claims one). This rule can be separated from the question of which collector is used.
3. **The living page costs no model call.** `run.py refresh` rebuilds the page from the last daily report plus the entry files "with no model call" (SKILL.md:16). The merged design already sends escalations into each issue's own entry on that page (M:docs/designs/orchestrator.md:666, 682). OURS does not address this at all (diff C-009).
4. **The nine-row table fills a gap in the sweep.** The sweep separates people-waiting rows only by kind "a" or "b" (M:src/superclaude/cli/sweep/report.py:230-236, 282-286). It has no list of reasons. The table rule "When in doubt, a case does not reach Clay" (orchestrator.md:668) is pinned at "exactly nine rows" by a test the design plans (orchestrator.md:1116). It is policy and can be separated.
5. **The cap is settled and never loses an entry.** "The cap never drops an entry. Recommended value: 5 ... ruling 39" (orchestrator.md:686; AD-B4 at line 1177). It also fits the owner's rule that automated reports show outstanding decisions only, which OURS itself cites (variant-1 line 27).

## Weaknesses identified in Variant 1
1. **Its fix is not written.** The contract note `docs/designs/observe-sweep-contract.md` does not exist, and OURS lists that as its first risk (variant-1 lines 31, 37). Putting the report on hold behind it would remove the only working answer to issue 409.
2. **It is silent on the living report and on naming** (diff C-009, C-010). The merged design already routes escalations into that report (orchestrator.md:682). So an unbuilt Decision Desk would end up duplicating a channel that the design has already chosen.
3. **"Additive change" understates the cost.** The v1 key set of the sweep JSON is pinned by a golden test (M:docs/designs/orchestrator-mode.md:605). Every new field needs a reviewed edit to that test.

## Concessions
- The report reads Orca sessions a third way (`sessions.py`). Its six status words can disagree with the sweep's eight classes. One source for session facts is better.
- The DM and commit steps are writes that the sweep and observer rules forbid. Entries also carry a Recommendation, which the sweep's "recommend nothing" rule forbids.
- It is set up for one person (`config.json`: `clayphi`, America/Chicago, one ClickUp token). It costs tokens on every daily run (SKILL.md:10).
- It is not zero-setup: without `$AWR_ROOT` or `orchestrator_repo` set, it exits (M:src/superclaude/skills/agent-work-report/scripts/common.py:35-50).
- It still says `/sc:orchestrator` and `.dev/coordinator/` (singular) (SKILL.md:12, 14), against the owner's naming.
- Nothing enforces the cap or the table yet.

## Shared assumptions
- **A-001: QUALIFY.** No join key is defined. The report maps a terminal to its transcript through the Orca hook file (SKILL.md:38), and the sweep uses Run and worker rows. The contract note must name the key. Whether sweep rows carry a Claude session id is UNVERIFIED.
- **A-002: QUALIFY.** The reasons are general, but the wording names one person ("his own identity", orchestrator.md:672). The column for Clay's reasons is tied to his ruling 16. Adopt the rows with "the person" in place of Clay.
- **A-003: QUALIFY.** Adding fields is possible but not cheap. NFR-009 pins the v1 keys (orchestrator-mode.md:605), so each addition needs a reviewed test edit.
- **A-004: ACCEPT.** common.py:42-50 exits without the orchestrator repo path, so the skill is not zero-setup today. That is a cost on CLAY's side.

## Per-point positions

| Point | Superior | Confidence | Evidence |
|---|---|---|---|
| S-001 | CLAY | 60% | Everything CLAY describes is on master; part of OURS's design is unwritten (variant-1 line 31) |
| S-002 | Tie, so OURS | 50% | Both evidence sets hold; the rule gives ties to OURS |
| C-001 | OURS | 75% | Three readers can disagree; the sweep is a no-model script with proof-based classes (models.py:50-59) |
| C-002 | CLAY (HYBRID) | 65% | The sweep is Orca-only (probes.py:49-56); the report's GitHub and ClickUp code already exists |
| C-003 | CLAY | 80% | Decision Desk is not built; OURS concedes this (variant-1 line 38) |
| C-004 | OURS | 80% | The sweep rule is "Will Not: Recommend anything" (sc-sweep-protocol/SKILL.md:61); the report sends DMs and commits |
| C-005 | OURS | 65% | The sweep costs no tokens; `refresh` only offsets part of the daily model cost |
| C-006 | CLAY (HYBRID) | 70% | The sweep has kinds a and b only (report.py:230-286); nine rows decided (orchestrator.md:668-680) |
| C-007 | CLAY (HYBRID) | 60% | Settled by ruling 39 and never drops an entry (orchestrator.md:686); not enforced yet |
| C-008 | OURS | 75% | Eight classes including "could not determine" beat the report's six status words |
| C-009 | CLAY | 70% | No-model refresh (SKILL.md:16); the design sends escalations into entries (orchestrator.md:682) |
| C-010 | OURS | 70% | CLAY's naming conflicts with the owner's (SKILL.md:12, 14) |
| X-001 | OURS for session facts, HYBRID for work items | 65% | One source of session facts; GitHub and ClickUp text stays in the report layer |
| X-002 | CLAY | 60% | OURS itself says "the report keeps working meanwhile" (variant-1 line 33) |

All citations were re-read in /home/coder/.cache/ic-snap-20261120/master during this round. Two things were not checked: whether sweep rows carry a Claude session id, and whether the sweep or observer has any check that compares one run with the previous one.
