# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 invariant probe
- Convergence achieved: 100% of diff points agreed (18 of 18); gate status BLOCKED_BY_INVARIANTS (2 HIGH UNADDRESSED, see invariant-probe.md)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant 1 = OURS, opus:architect; Variant 2 = CLAY, opus:analyzer)
- Round 2 order: Variant 1 first, then Variant 2 (who read Variant 1's rebuttal)
- Verified facts the orchestrator injected between Round 1 and Round 2: the sweep JSON v1 row has no session_id, terminal handle or worktree_path (`src/superclaude/cli/sweep/report.py:612-695`).
- Omission check (A-001 to A-004): no omissions; both advocates answered all four in both rounds.
- Taxonomy coverage (AD-5): L1 (C-010), L2 (S-001, S-002, C-001 to C-003, C-005 to C-007, C-009, X-001, X-002, A-002, A-004) and L3 (C-004, C-008, A-001, A-003) all debated; no forced round needed.

## Round 1: Advocate Statements

### Variant 1 Advocate (opus:architect) for OURS

## Position summary

The sweep JSON should be the single fact source, and the observer should be the single screen that reads it. Clay's work report should stay, but as the plain-English work-item layer on top of the sweep, not as a third collector. We adopt the nine-row table and the notice cap as policy now, because nothing built depends on them yet. The living report is adopted as a HYBRID, once it reads session facts from the sweep.

## Steelman of Variant 2

Clay's strongest argument is that his report is the only piece that already gives a person, per issue, a plain-English summary, what is done, what is left, whether it needs them, and a link. Issue 409 asks for exactly that. The sweep records its own gap here: issue 409 item 3 says "the sweep has no per-session summary text", and its Orca allowlist contains no GitHub call (M:src/superclaude/cli/sweep/probes.py:49-56). The report also has three solid safety properties:

- A script gate: `check.py` must pass before anything is delivered (M:src/superclaude/skills/agent-work-report/SKILL.md:24).
- No silent loss: "a failed read carries items, never closes them" (SKILL.md:21).
- A living page that is rebuilt "with no model call" (SKILL.md:16).

Our own paper concedes that the observer-sweep contract note does not exist. So Clay is right that waiting on paper would delay a tool that works today, and right that the nine-row table fills a gap. Our sweep only splits "waiting" by kind, with no list of reasons.

## Strengths claimed

1. **One fact layer with a fixed, read-only surface.** The sweep may call Orca only through a fixed list of command templates (M:src/superclaude/cli/sweep/probes.py:49-58). It uses no model, so it is the only one of the three that can run on the 5-minute cadence of rule WC-16 (M:src/superclaude/core/WORKER-CONTRACT.md:287). Two readers of the same sessions can disagree about a session's state, a risk that Clay's own paper names (variant 2, line 36). One reader removes that risk at its root.
2. **The keys needed to join a session already exist in the sweep.** The sweep's models carry `worktree_path`, a `session_id` on the transcript record, and a `TabMapEntry` linking `session_id` to `terminal_handle` (M:src/superclaude/cli/sweep/models.py:103, 131, 146-148). The report can therefore join on sweep rows instead of re-reading Orca. That makes "sit on top of" a real, buildable dependency direction, not a wish.
3. **The owner's rules are encoded where they matter.** The sweep "will not recommend anything, propose an action, or add advice" (M:src/superclaude/skills/sc-sweep-protocol/SKILL.md:61). The observer's questions panel turns on only against a recorded owner pass (M:src/superclaude/cli/observe/commands.py:63-67). Building the base on these keeps the owner's decided order of watcher, then orchestrator, then dashboard.
4. **The dependency direction fits the owner's own issue.** Issue 409's alignment item 1 says to read "the sweep's JSON, not a second collector" (variant 1, line 14). Clay's direction, where "the sweep and observer feed or read it" (variant 2, line 9), would make a skill tied to one person, which needs a model and writes to outside services, an upstream dependency of zero-token, read-only tools. That reverses the stability gradient: the most stable layer should sit at the bottom.
5. **The notice policy agrees with the owner's standing rule.** "When in doubt, a case does not reach Clay" (M:docs/designs/orchestrator.md:668) and "the cap never drops an entry" (orchestrator.md:686) match the owner's rule to show outstanding decisions only. So both can be adopted without conflict.

## Weaknesses identified in Variant 2

1. **A third collector.** `sessions.py` lists terminals and reads transcripts itself (scripts/sessions.py:1-28, cited in variant 1 line 21). This is a third Orca reader with its own six status words, beside the sweep's eight classes. Variant 2 admits the disagreement risk at line 36.
2. **Tied to one person and not zero-setup.**
   - `config.json` sets `"person": "clayphi"`, `"timezone": "America/Chicago"` and `"session_tag": "coordinator"` (M:src/superclaude/skills/agent-work-report/config.json:2, 6, 11).
   - The skill stops unless `AWR_ROOT` or `orchestrator_repo` is set (M:src/superclaude/skills/agent-work-report/scripts/common.py:35-45).
   - As a base layer for every user, this is a cost the sweep does not have.
3. **Writes and recommendations.** The report's notice is a ClickUp direct message (M:docs/designs/orchestrator.md:666), and its entries carry a "recommendation and why" (orchestrator.md:690). Clay's paper concedes these are "writes the sweep and observer rules forbid" (variant 2, line 37).
4. **Naming drift.** The skill text still says `/sc:orchestrator` and `.dev/coordinator/` (SKILL.md:12, 14). Clay's paper concedes these conflict with the owner's decisions on naming and folder layout (variant 2, line 32).
5. **The cap is not enforced by anything built.** The cap is enforced through the `escalate` verb and the file `asks.json` (orchestrator.md:684-686). Our paper verified that neither exists in master, pr-a or pr-p (variant 1, line 26). So the "settled" cap is text, not code.

## Concessions

- Our unification has not been delivered. `observe/` never reads the sweep, and the contract note has not been written since 2026-11-13 (variant 1, lines 20 and 37).
- Clay's report meets the issue 409 asks today. Ours meets them only after the Decision Desk is built, and it is "NOT BUILT".
- The sweep has no GitHub, ClickUp or summary text. That layer has to come from Clay's code (`collect.py`, `clickup.py`), and it is right to reuse that code rather than rewrite it.
- Clay's script gate and "carry, never close" rules are real strengths the sweep's report could learn from.
- Our paper said nothing about the living report (C-009) or about naming (C-010).

## Shared assumptions

- **A-001: QUALIFY.** A join key exists on our side: `session_id`, `terminal_handle` and `worktree_path` (M:src/superclaude/cli/sweep/models.py:103, 146-148). Neither paper fixes which key is the contract, so the contract note must name it.
- **A-002: QUALIFY.** We adopt the table's structure. Row 1 ("his own identity", M:docs/designs/orchestrator.md:672) and the other rows' "Clay" wording must be made about any user before the table applies stack-wide.
- **A-003: ACCEPT, with the cost stated.** The v1 key set is pinned by a golden test (M:docs/designs/orchestrator-mode.md:605), so adding fields needs a reviewed test edit, which is cheap but not free. The same file shows that additive v1 keys were planned from the start.
- **A-004: ACCEPT** that the assumption is false. `common.py:35-45` exits without `AWR_ROOT` or `orchestrator_repo`. The report is not zero-setup, which is one more reason it should not be the base layer.

## Per-point positions

| Point | Superior | Confidence | Evidence |
|---|---|---|---|
| S-001 | Variant 2 | 65% | Clay describes built code; ours is a partly unbuilt target (the contract note is missing). |
| S-002 | Tie | 50% | Both cite well: Clay on capability, ours on structural cost. |
| C-001 | OURS | 75% | One Orca reader removes the status disagreement; join keys exist (sweep models.py:146-148). The full-transcript read can stay as an enrichment step keyed on sweep rows. |
| C-002 | HYBRID | 70% | Keep Clay's GitHub and ClickUp code, but join it through the contract note, not a parallel stack. |
| C-003 | Variant 2 | 75% | Only the report meets the issue 409 asks today; the Decision Desk is not built. |
| C-004 | OURS | 80% | The sweep refuses to recommend (sc-sweep-protocol SKILL.md:61); the DM and recommendation are confined to the report surface. |
| C-005 | OURS | 70% | Person-specific config (config.json:2, 6); the sweep costs zero tokens. Clay's no-model `refresh` narrows the gap. |
| C-006 | Variant 2, adopted as HYBRID | 70% | Nothing in the sweep gives a reason list; the table gets generic wording before stack-wide use. |
| C-007 | OURS, on enforcement facts | 60% | The cap is written down (orchestrator.md:686), but `escalate` and `asks.json` are unbuilt. Adopt the value of 5 as policy. |
| C-008 | OURS | 70% | Eight proof-based classes with "could not determine" are the stable base; the report's six words should be mapped onto them. |
| C-009 | Variant 2, adopted as HYBRID | 70% | Entry files plus a no-model refresh (SKILL.md:16) are a real capability; feed them sweep facts. |
| C-010 | Variant 2, for honesty | 60% | Clay names the naming drift (SKILL.md:12, 14); the fix follows the owner's naming. |
| X-001 | OURS | 75% | The stable, zero-token, read-only layer belongs at the bottom; the reverse makes the base depend on a single-user skill that writes to outside services. |
| X-002 | Variant 2, in part | 55% | Do not freeze the working report; ship the contract note next, and let the report move to the sweep data afterwards. |

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

## Round 2: Rebuttals

### Variant 1 Rebuttal (OURS, opus:architect)

#### The join-key correction first

In Round 1 I said the join keys "already exist" in the sweep. That is true of the code and false of the JSON the observer would read. Each JSON row carries only `row_id`, `class`, `waiting_kind`, `rule`, `evidence`, `notes`, `policy`, `person_started` and `safe_to_close` (M:src/superclaude/cli/sweep/report.py:642-661).

One part of the key does survive. Rows built only from a transcript get `row_id = "transcript:<session id>"` (M:src/superclaude/cli/sweep/classify.py:933). When the record has no session id, that falls back to the file name (classify.py:923). Rows built from Orca get `"orca:<dispatch>"` with no session id (classify.py:903), even when a transcript was joined to them. So parsing `row_id` would be a fragile habit, not a contract.

The fix is one additive `session_id` field per row, plus a reviewed edit to the golden test `sweep/test_cli_contract.py` (M:docs/designs/orchestrator-mode.md:817). There is a precedent: five keys were already added under NFR-009's additive-only rule (orchestrator-mode.md:850). The dependency direction still stands, but it now waits on that field, so my confidence on C-001 drops.

#### CLAY's five strengths

1. **Per-issue plain-English text with GitHub and ClickUp: CONCEDE.** The sweep's allowlist has no GitHub call (probes.py:49-56). Under the HYBRID, `collect.py` and `clickup.py` stay as the work-item source.
2. **Check against silent loss: CONCEDE. It is clear and separable.** I searched `src/superclaude/cli/sweep/` for any comparison with a previous run and found nothing. The report's rules (carry items forward, never close them on a failed read, list what was not checked, block delivery until `check.py` passes) are at SKILL.md:21-24. How to merge it: put the rule in the work-item and report layer. The sweep stays a snapshot with no saved state, which keeps it zero-token and its output deterministic.
3. **Living page rebuilt with no model call: CONCEDE the capability, partly rebut where it lives.** `run.py refresh` uses no model (SKILL.md:16). But its state is in `.dev/coordinator/` inside an orchestrator repo that must be configured, or the skill exits (SKILL.md:14; common.py:35-50). HYBRID: keep the entry files, feed them sweep facts, and make the path configurable for any user.
4. **Nine-row table: PARTLY CONCEDE.** The gap is real: the sweep sorts people-waiting rows only into lists `a` and `b` (report.py:682-685). However: the rows come from Clay's ruling 16 and name one person ("his own identity", M:docs/designs/orchestrator.md:668-672); choosing a row is a judgment call and the sweep "will not recommend anything" (sc-sweep-protocol SKILL.md:61), so the table belongs in the notice-policy layer, not in the sweep classes. Adopt it with "the person" in place of Clay.
5. **Cap of 5: PARTLY CONCEDE, and rebut "settled".** Ruling 39 settled it "as recommended" (orchestrator.md:1170), and that was Clay's ruling, not the owner's. Nothing enforces it: the `escalate` verb and `asks.json` (orchestrator.md:684-686) are unbuilt, as already verified (U-004). The value does fit the owner's "decisions only" rule. Adopt 5 as the default, pending the owner's word.

#### CLAY's three weaknesses of OURS

1. **The fix is not written: CONCEDE the fact, rebut the consequence.** Nobody proposes holding the report back. My Round 1 position on X-002 already said "do not freeze the working report".
2. **Silent on the living report and on naming: CONCEDE, and change my position.** The merged design already sends escalations into each issue's entry in the living report (orchestrator.md:682). The observer's Decision Desk should therefore read those entries, not build a second channel for the same thing. That splits X-001 in two: session facts flow from the sweep into the report, and work items flow from the report into the observer.
3. **"Additive change" understates the cost: CONCEDE.** The orchestrator's check after Round 1 makes the point stronger than CLAY did: the join itself depends on a new field and a test edit.

#### Points where my position changed

- C-001: still OURS, but at 65%, because the join needs the `session_id` field first.
- C-007: HYBRID. "Settled" is Clay's ruling, not the owner's.
- C-010: OURS. The real question is whose naming wins, and the owner's does (SKILL.md:12, 14).
- X-001: HYBRID, split by kind of data as above.
- X-002: HYBRID. The report keeps running. The contract note and the `session_id` field come next, then the report switches its session reads to sweep data.
- New point, the silent-loss check (U-005): CLAY, adopted as HYBRID.

#### Shared assumptions, updated

- A-001: QUALIFY. No stable key is in the JSON contract. `row_id` holds the session id only for transcript rows. The report links terminals to transcripts through Orca's hook file (SKILL.md:38), so the session id is the natural shared key. The contract note must name it and add it to every row. UNVERIFIED: that a transcript's file name always equals its session id.
- A-002: QUALIFY, unchanged: use generic wording before the table applies to everyone.
- A-003: QUALIFY (was ACCEPT). The change is cheap but not free, and the join needs it.
- A-004: ACCEPT that the assumption is false (common.py:35-50).

#### Updated per-point table

| Point | Superior variant | Confidence |
|---|---|---|
| S-001 | CLAY | 65% |
| S-002 | Tie, so OURS | 50% |
| C-001 | OURS (after the `session_id` field is added) | 65% |
| C-002 | HYBRID | 75% |
| C-003 | CLAY | 80% |
| C-004 | OURS | 80% |
| C-005 | OURS | 70% |
| C-006 | HYBRID (generic wording, notice layer) | 75% |
| C-007 | HYBRID (5 as default, pending owner, unenforced) | 60% |
| C-008 | OURS (map six words onto eight classes) | 75% |
| C-009 | HYBRID | 70% |
| C-010 | OURS | 70% |
| X-001 | HYBRID (sweep to report for session facts; report to observer for work items) | 70% |
| X-002 | HYBRID | 65% |
| U-005 silent-loss check | CLAY, adopted as HYBRID | 80% |

Not checked by this advocate: whether Claude transcript file names always equal the session id, and a full reread of `common.py`.

### Variant 2 Rebuttal (CLAY, opus:analyzer)

#### Where OURS's concessions already give a HYBRID
I accept OURS's Round 2 positions on C-002, C-006, C-009, X-001, X-002 and the silent-loss check (U-005), and I won't argue them again. That leaves C-001, C-004, C-005, C-007, C-008 and C-010.

#### C-001: replace part of `sessions.py`, not all of it
OURS says the report should "switch its session reads to sweep data". It should switch only half of them.

- **Finding sessions and judging their state: move to the sweep.** `sessions.py` says "status is decided by the model from these facts" (M:src/superclaude/skills/agent-work-report/scripts/sessions.py:5-6). That is weaker than the sweep's classes, which follow written proof rules. OURS wins this half.
- **Reading what each session did: keep it in the report.** `sessions.py` reads the transcript bytes after the previous report's saved position, and up to 30 MB on the first run (sessions.py:14-17, 142, 170, 346). It pulls out prompts, files written, git commands and item URLs. The sweep reads only the last 256 KiB (M:src/superclaude/cli/sweep/probes.py:865-867), so it cannot say what a session did since yesterday. That benefit is clear, evidenced and separable, so the result is a HYBRID.
- **A new risk.** The two tools match terminals to sessions from different files. The sweep reads `ccsession/orca-tabs` (probes.py:870-871). The report reads Orca's agent-hook file `last-status.json` and falls back to the ccsession tag (sessions.py:9-13). Before switching, someone must check that the sweep finds every session the report finds today. Which file covers more sessions is UNVERIFIED.

#### C-004: concede to OURS
Only report entries may carry Options and a Recommendation, because Clay's design requires them there (orchestrator.md:690). The sweep keeps its "Will Not: Recommend anything" rule (M:src/superclaude/skills/sc-sweep-protocol/SKILL.md:61). The DM and the commit are made only by the report or orchestrator session, never by the sweep or the observer. Whether the observer may show an entry's text word for word, labelled as coming from the report, needs the owner's word (UNVERIFIED).

#### C-005: concede to OURS, with one change
Person-specific values (`clayphi`, America/Chicago, the ClickUp token) move into the user's own config. The shipped `config.json` should name no person.

#### C-007: concede that "settled" was overstated
OURS is right that ruling 39 is Clay's, though the design implies it rather than saying it in that line:
- Line 3 says the design was "approved by the owner (Clay)" under ruling 37, so the numbered rulings are Clay's rulings.
- Line 1170 lists "Clay's rulings 23 to 35" and then "ruling 39" without naming who made ruling 39.
- Lines 688 and 877 say the cap changes "only on Clay's recorded word".

All lines are in M:docs/designs/orchestrator.md. It is also worse than OURS said:
- The same design calls AD-B4 "not ruled on; open" (orchestrator.md:1177).
- It says an absent key means 0, which is no cap (orchestrator.md:686).
- The built parser returns 0 for an absent or bad value (A:src/superclaude/cli/issue_watch/repos.py:262-269).

So the cap is unenforced, and the code gives "no cap" by default. Only the owner can settle this. My proposal: when the config file is generated, write 5 into it, and add a test that pins it.

#### C-008, C-010: concede to OURS
The report's six words describe work items only. The session state it shows is the sweep's class, word for word. On naming, the owner's naming wins.

#### Is OURS right about where the nine rows belong?
Yes. The table decides whether to notify someone: "The orchestrator decides everything that is not in this table ... When in doubt, a case does not reach Clay" (orchestrator.md:668). Choosing a row is a judgment, and the sweep refuses to make judgments (SKILL.md:61). The table belongs to the notice step. The observer may show the row number that the entry already records, but it never picks one.

#### Final recommended merge (testable statements for the spec)
**(a) One data source.**
- Sweep JSON v1 gains `session_id` and `worktree_path` on every row, with a reviewed edit to the golden test.
- `sessions.py` stops calling `orca terminal list` and its status logic. It reads transcripts only for session ids found in sweep rows, still from its saved position.
- A test fails if any session the old map found is missing from the sweep.

**(b) One report.**
- The work report is the only plain-English report. It gets session facts from the sweep and work items from GitHub and ClickUp (`collect.py`, `clickup.py`).
- `check.py` gates delivery.

**(c) One dashboard.**
- The observer reads the sweep JSON for sessions and the living-report entry files for work items.
- It adds no recommendation and makes no write.

**(d) Clay's features.**

| Feature | Verdict | What changes |
|---|---|---|
| Living report | Adopt with change | The state path becomes configurable per user, and the entry files take sweep facts. `refresh` stays model-free. |
| Nine rows | Adopt with change | Use "the person" in place of Clay. The table lives in the notice step only. Keep the planned "exactly nine rows" test. |
| Cap of 5 | Adopt with change | 5 becomes the default written into the config, pending the owner's ruling. It stays unenforced until `escalate` and `asks.json` exist. It never drops an entry. |
| Silent-loss check | Adopt as is | It stays in the report layer, so the sweep keeps no saved state. |
| Plain-English item template | Adopt with change | Use generic wording for the person. The observer's Decision Desk shows the same fields. |

#### Shared assumptions
- **A-001: QUALIFY.** The JSON has no shared key yet. Add `session_id` to every row, and reconcile the two terminal-to-session maps first.
- **A-002: QUALIFY.** Use generic wording before the table applies to everyone (orchestrator.md:672).
- **A-003: QUALIFY.** Adding fields is cheap but not free: the golden test pins the v1 keys (M:docs/designs/orchestrator-mode.md:605).
- **A-004: ACCEPT that it is false.** The skill exits unless `$AWR_ROOT` or `orchestrator_repo` is set (M:src/superclaude/skills/agent-work-report/scripts/common.py:35-50).

#### Updated per-point table

| Point | Superior variant | Confidence |
|---|---|---|
| S-001 | CLAY | 65% |
| S-002 | Tie, so OURS | 50% |
| C-001 | HYBRID (sweep finds sessions and judges state; report reads the transcript from its saved position) | 75% |
| C-002 | HYBRID | 75% |
| C-003 | CLAY | 80% |
| C-004 | OURS | 85% |
| C-005 | OURS | 75% |
| C-006 | HYBRID (notice step, generic wording) | 75% |
| C-007 | HYBRID leaning OURS (owner ruling needed; default is 0 today) | 65% |
| C-008 | OURS | 80% |
| C-009 | HYBRID | 75% |
| C-010 | OURS | 75% |
| X-001 | HYBRID | 75% |
| X-002 | HYBRID | 70% |
| U-005 silent-loss check | CLAY, adopted as HYBRID | 80% |

Not checked by this advocate: whether the sweep's `orca-tabs` map covers every session that Orca's hook file covers, and whether a transcript's file name always equals its session id.

## Round 2.5: Invariant Probe

Full table in `invariant-probe.md` (12 findings; 2 HIGH UNADDRESSED: INV-001 report would lose sessions of removed worktrees, INV-002 the agreed coverage test cannot run live once the old session map is removed).

## Scoring Matrix

Winner is taken from the two final per-point tables (Round 2). Confidence is the mean of the two advocates' final confidence; a point both call a HYBRID is a HYBRID.

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Variant 2 (CLAY) | 65% | CLAY describes built code; OURS describes a partly unwritten target (no contract note). |
| S-002 | Variant 1 (OURS), by the tie rule | 50% | Both evidence sets hold; ties go to OURS under the owner's rule. |
| C-001 | HYBRID | 70% | Sweep finds sessions and judges state (written proof rules); the report keeps a transcript reader from its saved position (sweep reads a 256 KiB tail, `probes.py:865-867`). |
| C-002 | HYBRID | 75% | Report keeps GitHub, ClickUp and plain-English code; joined through a written contract note. Sweep has no GitHub call (`probes.py:49-56`). |
| C-003 | Variant 2 (CLAY) | 80% | Only the report meets Clay's issue 409 asks today; Decision Desk NOT BUILT; OURS conceded. |
| C-004 | Variant 1 (OURS) | 83% | Sweep "Will Not: recommend anything" (`sc-sweep-protocol/SKILL.md:61`); Options, Recommendation, DM and commit only on report entries; CLAY conceded. |
| C-005 | Variant 1 (OURS) | 73% | Person-specific `config.json` moves to per-user config; sweep is zero-token. |
| C-006 | HYBRID | 75% | Nine rows adopted with "the person" for Clay, living in the notice step only; the sweep never picks a row. |
| C-007 | HYBRID (leaning OURS) | 63% | Cap of 5 adopted as a proposed default pending the owner's ruling; unenforced; the parser returns 0 (no cap) for absent keys (`pr-a issue_watch/repos.py:262-269`); ruling 39 is Clay's. |
| C-008 | Variant 1 (OURS) | 78% | Eight proof-based classes; the report's six words describe work items; session state shown is the sweep class. |
| C-009 | HYBRID | 72% | Living report adopted; per-user state path; entry files hold only the session id and take the class live (INV-008). |
| C-010 | Variant 1 (OURS) | 73% | Owner's naming (coordinator) and layout win; CLAY conceded. |
| X-001 | HYBRID | 73% | Session facts flow sweep to report; work items flow report to observer. |
| X-002 | HYBRID | 68% | Report keeps running; contract note and `session_id` field first, then the report switches session reads. |
| A-001 | QUALIFY (both) | n/a | No shared key in JSON v1; add `session_id` per row (`row_id` holds it only for transcript rows, `classify.py:933`). |
| A-002 | QUALIFY (both) | n/a | Rows adopted with generic wording. |
| A-003 | QUALIFY (both) | n/a | Adding fields needs a reviewed golden-test edit (NFR-009, `orchestrator-mode.md:605`); precedent exists (five keys added, `:850`). |
| A-004 | ACCEPT that it is false (both) | n/a | The report exits without `$AWR_ROOT` or `orchestrator_repo` (`common.py:35-50`). |

Tally: OURS 5 points (S-002, C-004, C-005, C-008, C-010), CLAY 2 (S-001, C-003), HYBRID 7 (C-001, C-002, C-006, C-007, C-009, X-001, X-002), shared assumptions 4 resolved.

## Convergence Assessment
- Points resolved: 18 of 18 (all four shared assumptions answered)
- Alignment: 100%
- Threshold: 80%
- Status: CONVERGED on diff points, BLOCKED_BY_INVARIANTS (INV-001, INV-002 HIGH UNADDRESSED). Treated as converged after the two items are written into the refactoring plan as required statements (no advocate disputes them).
- Unresolved points: none among diff points; open for the owner: C-007 (cap value and who rules), and the MEDIUM invariants INV-003 to INV-007, INV-009, INV-010 carried as requirements.
