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
