# Round 1 advocate: Variant 1 (Proposal A, label from the watcher's own record)

Persona: analyzer (evidence quality, logical consistency). Sources were read on 2026-11-14 in this checkout. "ADJ" = `.dev/reviews/orchestrator-tui-alignment-20261113/adversarial/alignment-findings-adjudicated.md`; "MR" = `.dev/brainstorms/20261113-orchestrator-tui-alignment/merged-requirements.md`.

## Position summary

A "machine-started" label should rest on a record the watcher writes on purpose, matched positively, not on Orca free-form fields that were empty or not a slash command on all 27 live rows seen (ADJ line 162). The watcher already keeps a schema-versioned per-issue record in `dispatch.json` with `operation_id` and `launch_cwd` (`record.py:69-95`), so V1's evidence base is stronger than V2's. However, V1's first-named input, `status --json`, does not carry those fields for launched sessions, and V1 departs from the SW-10 done-when the spec already wrote. So V1 wins on signal quality and loses on cost and fit with the spec.

## Steelman

**Variant 2 (Phase 2, Orca rows after FU-1).** At its strongest, V2 is the spec's own answer, written into SW-10's done-when (MR line 199, item 2: "the label reads `worktree ps` agent rows (`prompt`, `paneKey`) only in the shape FU-1 recorded"). It needs no new input and no new owner signature: `("worktree", "ps", "--json")` is already one of the pinned templates (`src/superclaude/cli/sweep/probes.py:55`, closing comment "10 templates, 7 verbs (NFR-014)"). The watcher's prompt is fixed and narrow, `PROMPT_PATTERN = ^/sc:issue --claim [1-9][0-9]{0,8}$` (`src/superclaude/cli/issue_watch/launch.py:33`). If Orca stores the launch prompt in `prompt`, that field is close to a fingerprint. Its stop rule (U-002, "records 'no reliable signal' and stops") is the best failure discipline in the set: nothing is built on an unusable signal. Its error direction, a false negative, is the safe one, because person sessions are never messaged (WC-16).

**Variant 3 (not now, name the blind spot).** At its strongest, V3 is the most honest about the evidence: D-B is open (ADJ line 493), the firm mislabel claim was withdrawn (ADJ line 162), and L1 is NOT BUILT (MR line 93). It also observes correctly that WA-07 item (3) accepts either route: "visible to the sweep as a labelled row (SW-10) or bound to a Run" (MR line 309). So if D-A shows that `agent launch` creates a Run, the label is unnecessary. V3 costs nothing, keeps FU-1 item (e) as evidence, and puts in place now the documentation sentence ADJ already asks for (ADJ lines 227, 242).

## Strengths claimed

1. **The watcher already writes the record V1 needs, with a version.** Each `dispatch.json` entry carries `operation_id` and `launch_cwd` (`src/superclaude/cli/issue_watch/record.py:69-88`). `mark_launched` refuses an invalid `operation_id` (`record.py:580-593`). `launch_cwd` is set from the configured worktree before the launch (`cycle.py:1082-1091`) and must be absolute (`record.py:548-549`). The store document has a `schema_version` that the loader checks (`record.py:95`, `record.py:220-237`). So the drift risk V1 itself names, "`status --json` has no `schema_version`" (MR line 453), applies to the status output, not to the store. MR line 453 already lists "`dispatch.json` v1" in the contract registry.
2. **Positive match, so a false "machine-started" label is unlikely (U-001).** The label fires only on a match with a watcher entry. V2's label fires on an Orca field shape that is unverified (D-B, ADJ line 493) and that the only live evidence contradicts: 27 of 27 rows empty or not a slash command (ADJ line 162).
3. **The deciding signal survives Orca drift.** A-009 records two builds of Orca 1.4.245 (cited in V2's own risks). V1's deciding input is owned by this repo's code (`launch.py:33`, `record.py`). An Orca change to `prompt` or `paneKey` cannot flip the label, because in V1 those fields are only supporting notes.
4. **FU-1 still decides, so V1 does not guess the key.** V1 step 1 keeps FU-1 items (e) and (f). Item (f) is "the real launch-reply operation-id path, compared with `OPERATION_ID_PATHS`" (MR line 306; `launch.py:42-44`). FU-1 chooses the join key. V1 does not assume it.
5. **Better reader correctness than V3.** V3 accepts that the sweep may show a watcher session as `person_active` until SW-13. That label comes from `_person_origin` returning `True` with only the note "origin not proved" (`classify.py:748-767`), which feeds `_rule_person_active` (`classify.py:302-315`). For watcher sessions, V1 replaces that unproven `True` with a proven positive.

## Weaknesses identified in other variants

1. **V2 builds on a signal that the only evidence contradicts.** On 27 live agent rows, `prompt` was empty or not a slash command (ADJ line 162). V2 waits for one FU-1 row (MR line 306, item e) to show the shape, which is a sample of one. V2 concedes this ("one FU-1 row may not represent every launch"). SW-10's done-when (MR line 199) has no rule for re-checking after an Orca build change (A-009).
2. **V2's "no new input" advantage is narrower than it looks.** `worktree ps --json` is allowed (`probes.py:55`). But what decides the label is the content of `prompt`/`paneKey`, and no contract pins it. The contract registry lists the observe snapshot, the sweep report JSON, watcher `status --json`, `dispatch.json` v1 and future records (MR line 453), but no Orca `worktree ps` row schema. V2 adds an unversioned dependency too, just in a different place.
3. **V2's `paneKey` route brings in a third source that nobody has audited.** Item (e) asks "does `paneKey` equal a tab-map name" (MR line 306). That ties the label to the ccsession tab map (item h), which neither the sweep allow-list nor the contract note covers. Whether the sweep may read the tab map is UNVERIFIED.
4. **V3 defers onto a design that does not exist.** SW-13 and WA-07 are DEFERRED, and L1 is NOT BUILT (MR lines 93, 128). Until they land, a person reading the report can be misled about who started a session (V3 states this cost itself). The reopen trigger also loses context (V3 concedes this too).
5. **V3's "the label may be unnecessary" rests on D-A, which is open.** Whether `agent launch` creates a Run is unknown (MR line 128). If it does not, WA-07 item (3) still needs either the label or a new binding mechanism. V3 assumes, without evidence, that the label can be avoided.

## Concessions

1. **V1 names the wrong input first.** `status --json` (`cycle.py:1277-1334`) returns `healthy`, `counts`, `stale` (issue, state, last_reason, updated_at), `retry` and a few scalars. `operation_id` and `cwd` appear only in `retry`, and only for entries in state `unknown` (`cycle.py:1308-1323`). The operation id and launch directory of a successfully launched session are **not** in `status --json`. The only workable V1 input is the store file `dispatch.json`, which needs an approved file-read path (V1 step 3, second option). V1 leaves the choice open and lists `status --json` first. That is a factual error in V1.
2. **The join key may not exist.** Nothing read here shows that an Orca operation id appears in a `worktree ps` agent row or in a transcript. This is D-A/item (f) territory and is UNVERIFIED. V1's fallback is worktree-path matching, which is coarse: every person session opened in the watcher worktree (`launch_cwd=str(cfg.worktree)`, `cycle.py:1086`) would be labelled machine-started. **That is the unsafe error direction:** it turns a person session into a "machine" session. V1 lacks V2's stop rule (U-002) for this case and should adopt it: if no exact key exists, record "no reliable signal" and do not fall back.
3. **V1 rewrites a spec work item and adds owner work.** SW-10's done-when (MR line 199, item 2) names Orca rows. V1 requires rewriting it, plus a contract-note entry and either a widened NFR-014 list or an approved file path. NFR-014 lists Orca and git *commands* (ADJ line 84). Whether a plain file read needs an owner signature is UNVERIFIED; V1 assumes it does, to be safe.
4. **Host and user scope is assumed.** The store lives in the watcher's state directory. That the sweep can always read it rests on "single owner, single OS user, single host" (MR line 453), which is not verified for this pair of programs.
5. **V1 does not state that FU-1 waits on Q2 and Q20.** V2 states it; V1 omits it (diff-analysis A-001).

## Shared assumption responses

**A-001: QUALIFY.** All three variants rely on FU-1, and FU-1 waits on Q2 and Q20 (V2 states this; V1 omits it, as conceded above). The dependence is not equal, though. V1's main input, the watcher store, exists and is versioned today (`record.py:69-95`, `record.py:220-237`), so FU-1 is needed only to pick the join key (item f), not to learn whether a signal exists. V2 needs FU-1 to learn whether its signal exists at all (D-B). V3 needs FU-1 only for evidence it will not act on yet. If FU-1 never runs, all three end at V3's outcome, as the diff says.

## Per-point verdicts

| Point | Superior | One-line reason |
|---|---|---|
| S-001 | tie | All three use the same five-section layout. |
| C-001 | V1 | The deciding signal is a versioned record this repo writes (`record.py:69-95`), not Orca free text that was empty or non-slash on 27 of 27 rows (ADJ 162). |
| C-002 | V2 | `worktree ps --json` is already allowed (`probes.py:55`). V1 needs a new file-read path, because `status --json` lacks the op ids of launched sessions (`cycle.py:1308`). |
| C-003 | V2 | Same timing as V1 and matches the spec row (MR 548). V3's trigger, SW-13, is DEFERRED with no date (MR 93). |
| C-004 | tie (V1, V2) | Both feed WA-07 item (3) through a labelled row. V3 leaves only the Run-binding route (MR 309). |
| C-005 | V2 | Its stop rule refuses to guess. V1's worktree-path fallback errs in the unsafe direction (a person session labelled machine). |
| X-001 | V1 | The only evidence on Orca rows (ADJ 162) argues against trusting them for the decision. V3 shares the distrust but builds nothing. |
| X-002 | V2 | No new cross-program input or contract entry. V1's added input is a real cost: status JSON is not enough, and the store needs a new read path. |
| X-003 | V2 | The label is needed while D-A is open (MR 128). V3's "may be unnecessary" depends on a Run binding nobody has verified. |
| A-001 | V1 (narrowly) | V1's input exists and is versioned today, so FU-1 only picks the key. V2 needs FU-1 to learn whether any signal exists. Against V1: it did not state the Q2/Q20 wait. |

Honest net: V1 has the stronger signal (C-001, X-001). V2 wins on cost, spec fit and failure discipline (C-002, C-005, X-002). The best synthesis is V2's process and stop rule with V1's deciding signal, read from `dispatch.json` (not `status --json`), and with no worktree-path fallback.
