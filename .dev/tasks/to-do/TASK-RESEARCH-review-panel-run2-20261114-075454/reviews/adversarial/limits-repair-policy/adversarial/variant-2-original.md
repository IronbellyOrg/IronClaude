# Proposal B - slot C-06 (limits-repair-policy)

Status: Complete
Position: B (never edit reviewer text; reject with per-line errors, one re-ask, itemised drop report, fail-closed on a dropped blocking line; or raise the limits)
Code state: HEAD 50d4d2b9d on branch ironbelly/shadow-runs (`git rev-parse --short HEAD`). E2 data read only through `git show` / `git ls-tree` / `git cat-file` at `6c0984326cbb8fb06c4a36065de58b171d3f8175`.
Tags: [CODE-VERIFIED] re-read or executed in this session; [CODE-CONTRADICTED]; [UNVERIFIED]. "Replay" means a read-only execution that wrote no file.

## 1. The position in one paragraph

The core never edits reviewer text. A finding line that breaks a parser limit is dropped from the findings exactly as today, but the drop is itemised (line number, finding id, rule, field, actual length, limit, and whether the line said `blocking: true`, `false` or something unreadable), it is never counted as zero, a reviewer who still has a dropped blocking-or-unknown line after the re-ask is not a `complete` reviewer, and a round whose only blocking evidence was dropped is refused instead of stored as PASS. The reviewer, not the orchestrator, repairs its own lines: one bounded re-ask built only from that reviewer's own rejected lines and the parser's per-line messages (E1 protocol text, `SKILL.md:343`). Over-limit incidence is cut at the source by two levers that B-core does not depend on: briefs generated from the parser constants (already decided, synth-06 CO-8), and, if the owner accepts a widening of the findings-v1 line grammar, raising the constants in the shared limits module that slot C-01 already requires. B rejects truncation as a default policy because it is the one option that changes what a reviewer said (34 claims over 300 characters in the committed E2 reports lose 3 to 135 characters, and the claim is the field that carries the wrong outcome, `document_review_loop_prompts.md:60`) and because it turns a recorded non-compliance into a pass.

## 2. How this position relates to the adjudicated slots C-01, C-02 and C-03

| Adjudicated outcome | Source | What B does with it |
|---|---|---|
| One limits-constants module imported by both parsers; one function "called from inside both `parse_block` functions" that must not invent an anchor; "the policy is C-06" | C-01 `ADJUDICATION-RESULT.md` (Winner, shared-now list); `merged-core-shape-and-finding-contract.md:17,27` | B uses the same placement and fills the policy with itemise, not normalise. B reads the merged text "normalise-or-itemise" (`:27`) as the itemise branch. It does not need the call "on each line before the check": B records the failing rule at the point where the check fails, which is still inside both parsers, so a repair placed in callers is not needed (debate N-B3 stays satisfied). |
| INV-003 (HIGH): a rescuing repair inside `parse_block` and "T1: every existing pin unmodified" cannot both hold (`test_review_findings.py:113,117`) | C-01 invariant table | For B-core INV-003 does not arise: `ok` stays False for a 201-character anchor and a 301-character claim, `errors` keeps its shape, and `dropped` is an additive key. For the raise-the-limits lever INV-003 becomes a plain test rewrite (section 5), not a conflict. |
| INV-004, INV-010, INV-014, INV-022, INV-024 | C-01 invariant table | INV-004: B's effect is the same in v2 because the loss unit there is the reviewer (`cluster.py:256-257`); B answers it with the re-ask and the `complete` rule, not a repair. INV-010: `card_convert.py:85-86,199-201` must import the same constants under either policy. INV-014: a single reviewer whose only lines are dropped still gets today's refusal (`ledger.py:150-157`); B's remedy is the re-ask before the merge, not a repair. INV-022 (truncated claim can drop ref tokens; truncated anchor prefix can match several places): measured in section 4.3; it is not what B rests on. INV-024: B-core reaches both `parse_block` functions and, through the same constants and a per-line record, `card_convert.py:226`. |
| C-02: clearing needs a quorum of distinct `block_ok`-true reviewers typing `prior ... resolved`; a valid `prior open` vetoes; an invalid-block reviewer's priors are collected but not counted (INV-009 of C-02, `findings.py:186-190`, `ledger.py:139-140`) | C-02 `ADJUDICATION-RESULT.md` | B depends on it. Under B an over-limit finding line makes the reviewer `block_ok` False, so its `prior` lines do not count until the re-ask returns a valid block. That is a stated cost of B (section 8). B adds one thing to C-02's picture: a `prior` line with a bad status is itemised too (`findings.py:175-186`), not only finding lines. |
| C-03: union default, quorum as a merge-time refusal in `degrade` profiles with exit 12 and a `refusal` object, completion states recorded, reflect keeps `shortfall: visible` | C-03 `ADJUDICATION-RESULT.md`; `merged-output.md:9,61,123-127` | B depends on the refusal object and exit 12 and adds one refusal reason (`dropped-blocking`, section 3.3). No new exit value, no change to exit 0/10/11 (INV-D). B does not touch the reflect profile's `derive_verdict` (INV-B). C-03 INV-006 and INV-007 (merge unions findings of invalid-block reviewers; `requested` can collapse to 1) are unaddressed and B does not claim to close them: B's refusal reason reads the per-reviewer `dropped` record, so it does not use `requested`. |
| C-01 states one repair step is shared; the policy is left to this slot | task prompt, C-01 result | B's position is that the shared step is a classifier plus a record, and that any text change belongs to the reviewer. |

Where B disagrees with an adjudicated outcome: none. Where B is conditional on one: C-03's refusal object (without it B's fail-closed rule has no vehicle and falls back to a warning), and C-02's `block_ok` filter on clearing.

## 3. Design consequence for the shared core and the named modules

### 3.1 What the shared core holds

| Piece | Content | Where it sits |
|---|---|---|
| Limits constants | anchor and anchor2 12..200, citation quote 12..200, claim at most 300, refs at most 8, id at most 16 characters, citations 1..8, in one module imported by `findings.py` (`:104,108,114,118`), `findings_v2.py` (`:111,114-120,126,128,132,136`) and `card_convert.py` (`MAX_CLAIM = 300`, `MAX_REF_TEXT = 200`, `:85-86`) | the C-01 constants module (not a new decision) |
| Line classifier and drop record | the existing checks return an error string today; B makes each failing check also yield a structured record `{line, id, rule, field, actual, limit, blocking_state}` where `blocking_state` is `true`, `false` or `unknown` (absent or non-boolean `blocking`). The record carries lengths and ids, never reviewer text (INV-H). | inside both `parse_block` functions (`findings.py:124-196`, `findings_v2.py:215-304`) |
| Result shape | `ok`, `state`, `findings`, `priors`, `errors` unchanged (errors stay `{line, msg}`); one additive key `dropped`. Conservation holds per block: every non-blank line of the last findings block is exactly one of kept finding, prior line, or dropped record. | both parsers |
| Brief text | the limits sentence in every brief is generated from the constants (synth-06 CO-8, decided). Today the v1 loop brief states only the anchor limit and the reflect brief omits the quote limit (`document_review_loop_prompts.md:60`; `reviewer-spec.md:39` per research/02:135). | the skill and prompt sources, one generator |
| Re-ask request | a function that builds one message from one reviewer's own rejected lines plus the rule messages (limits read from the constants) and asks for the complete corrected block. It carries no other reviewer's content and no candidate change (INV-G). | review package; the transport that sends it is per environment |

### 3.2 The re-ask (what is decided and what is a transport fact)

- One re-ask per reviewer per round. First-pass validity is recorded before the re-ask, so `findings_block_compliance_rate` keeps its E1 definition: valid on the first parse, over reviewers dispatched, before any re-ask (`SKILL.md:343,988` [CODE-VERIFIED]).
- Trigger is a module setting. Reflect keeps its E1 rule (any invalid block gets the one bounded re-ask, `SKILL.md:343`). The spec loop triggers only when a reviewer has a dropped line whose `blocking_state` is `true` or `unknown`, or a block-level failure; dropped lines that said `blocking: false` are itemised and not re-asked. On the audit-D data that is 44 reviewer runs instead of 80 (section 4.2).
- The transport is a capability, `continue(reviewer, message)`: the Agent path continues the same agent (the E1 shadow runs did exactly this, section 4.4); the swarm HTTP path sends a second prompt that carries the reviewer's own first answer (workers get one user message and no session, `openai_compat.py:384-388`, synth-05 6.3 option 2 [CODE-VERIFIED as text of synth-05]); headless `claude -p` needs session persistence and `--resume`, which the E2 r2 spike S2 passed for ember, luna, sonnet and haiku and which is [UNVERIFIED] for other gateway ids (synth-05 6.3 option 2). A transport without the capability gets itemise-only plus the fail-closed rule of 3.3, never a truncation.
- The attempt needs a record. In E1 run A2 the re-ask "could not be recorded in the manifest (stage 'collected' already committed; OutOfOrder refused)" (`.../comboA-r2/panel/notes.md:9-10` [CODE-VERIFIED]). The shape of that record belongs to slot C-08; B only requires that one exists.

### 3.3 Fail-closed in the v1 merge (spec loop)

- `merge_round` adds to each reviewer entry (`ledger.py:141-149`) one additive key: dropped counts by `blocking_state` and by rule, and the dropped finding ids. `review-ledger/1` stays the schema string (`ledger.py:47-48` per C-03 merged text, INV-D additive keys only).
- A reviewer with one or more unresolved `true` or `unknown` dropped lines is not `complete` for C-03's quorum and, because its `block_ok` is False, it does not count toward clearing (C-02).
- New refusal reason `dropped-blocking`, carried by C-03's refusal object and exit 12, nothing recorded: the round has no blocking-open row after the union and at least one reviewer has an unresolved `true` or `unknown` dropped line. This is the "PASS by loss" case and only that case.
- The human exit from that refusal, so that it cannot deadlock when a re-ask is impossible or fails: an acknowledgement with owner and reason, the same shape as the `defer` that C-02 requires (owner and reason, terminal, counted). The acknowledged ids are listed in the merged report.
- When a blocking row survives, nothing is refused and the verdict is unchanged; the dropped ids are only printed. The audit-D data say this is 45 of the 49 dropped blocking lines (section 4.2).
- `merge` keeps exit 0 for every merge that is not refused (INV-D). The merged report gains a per-reviewer "dropped lines" table (id, rule, blocking state). Today the warning keeps only the error count and the first message (`ledger.py:130-134`).

### 3.4 Module by module

| Module | Under B |
|---|---|
| Spec review loop (v1 engine, C-01) | Constants, classifier, `dropped` key, re-ask on blocking-or-unknown drops, the `dropped-blocking` refusal, the dropped table in the merged report. No pin changes in B-core. |
| Reflect UC-1 and UC-2 (v2 kernel, shadow mode) | Same classifier and `dropped` key inside `findings_v2.parse_block`. `cluster_cmd.py:155-162` lists only `card`, `reviewer_id`, `state`, `block_state` and `errors`, so `clusters.json` and the card listing are byte-equal until someone chooses to emit `dropped`. The skill's E1 re-ask rule and compliance metric stay as written. `derive_verdict` and contract 1.8.0 are untouched. |
| Tasklist and workflow | Reached through reflect UC-1 (C-05); same as reflect. |
| PR code review (later) | The panel emits citations; the limit that bites there is the optional citation `quote` (12..200, `findings_v2.py:80`), which E2's own requirement does not name (synth-05 6.3 option 4). B handles it with the same re-ask or with the raise lever; section 7. |
| rf-qa replacement (later) | Reviewers stay mechanically read-only (INV-G); the re-ask is a continuation, not a new tool grant; the `dropped` record is the conservation check a replay oracle needs. Section 7. |

### 3.5 The raise-the-limits lever (B-raise), separate from B-core

The constants module makes the numbers a one-line change. The replay in section 4.3 gives the evidence for choosing them: with anchor and anchor2 at 300 and claim at 450, 120 of the 124 lines that fail today on a length rule pass unedited (69 of them blocking); with 250/250/350 it is 103 (59 blocking). B-raise is a widening of the findings-v1 line grammar (every line valid today stays valid), so it touches INV-C and rewrites four boundary assertions (section 5). B-core does not need it and B-raise does not need B-core, but together they leave about 4 lines in 124 for the re-ask.

### 3.6 What B does not do

No truncation step, no normaliser in front of the parser, no repair-aware parse, no change to a reviewer's `blocking`, `severity` or any other field, no calibrator or debate. `card_convert.py:199-201` keeps its marked truncation (297 characters plus `...`), which is a measurement converter for legacy cards, not a production path.

## 4. Evidence

### 4.1 Code facts at HEAD

| Fact | Evidence | Tag |
|---|---|---|
| Both parsers drop the whole line on any violation and set the block not-ok / `invalid`; there is no repair step | v1 `findings.py:188-195`; v2 `findings_v2.py:284-287,299-303` | [CODE-VERIFIED] |
| Limits: v1 anchor 12..200 required, anchor2 12..200, refs at most 8, claim at most 300; v2 repeats them and adds citation quote 12..200 | `findings.py:104,108,111-118`; `findings_v2.py:80,111,114-120,126,132,136` | [CODE-VERIFIED] |
| Length is counted after whitespace flattening, in characters | `findings.py:79-87`, `flat` at `:272-273` | [CODE-VERIFIED] |
| The loss unit is one finding in the v1 ledger and one reviewer in v2 clustering | `ledger.py:112,135-138,150-157`; `cluster.py:218-222,256-257`; `cluster_cmd.py:157-161` | [CODE-VERIFIED] |
| The only merge-time visibility of a drop is one string per reviewer with the error count and the first message | `ledger.py:130-134` | [CODE-VERIFIED] |
| Pins that fix the limits: 201-character anchor and 301-character claim give `ok` False; v2 quote 200 ok / 201 not; v2 claim 300 / 301 | `tests/review/test_review_findings.py:113,117`; `tests/review/test_review_findings_v2.py:199-200,241` | [CODE-VERIFIED] |
| A row clears to `resolved_check` only when a hunk touches its `span` or `span2`, and spans come from `locate` of the anchor (first occurrence wins, `anchor_ambiguous` is only a flag) | `ledger.py:301-337`; `findings.py:276-304,346-352` | [CODE-VERIFIED] |
| The v1 brief states the anchor limit (12 to 200) and gives the claim as "one sentence naming the wrong outcome" with no claim limit; blocking needs a sentence "X is wrong because Y" | `rules/prompts/document_review_loop_prompts.md:31,60` | [CODE-VERIFIED] |
| E1 protocol: the first-parse compliance rate is recorded before any re-ask; "The orchestrator never edits, remaps or normalizes a reviewer's findings itself"; one bounded re-ask | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:343,988` | [CODE-VERIFIED] |
| `card_convert.py` is a third copy of the limits and the only production-tree truncation: claim cut to 297 characters plus a visible `...` | `card_convert.py:85-86,199-201` | [CODE-VERIFIED] |
| `contract.py` contains no limit or anchor constant (grep for `anchor|MAX_|limit|1.8.0` returns only the 1.8.0 comment at `:127`) | `src/superclaude/cli/reflect/contract.py` | [CODE-VERIFIED] |
| `cluster_cmd.py` writes a fixed key set per card (`card`, `reviewer_id`, `state`, `block_state`, `errors`), so an extra key in the parse result is not emitted | `cluster_cmd.py:155-162` | [CODE-VERIFIED] |

### 4.2 The audit-D drop data (E2, `6c0984326`, read through `git show`)

Files: `.dev/eval-workspaces/tasklist-review-panel/20261111-a1/analysis/audits/audit-D/summary.md` and `flags.tsv`.

| Fact | Value | Tag |
|---|---|---|
| Reasons for the 92 dropped lines | anchor over 200: 56; anchor2 over 200: 18; claim over 300: 14; bad severity: 3; refs bad: 1 | [CODE-VERIFIED] (`summary.md` reasons line; sum checked) |
| Blocking drops | 49 `3-dropped-blocking` rows in `flags.tsv`, in 44 distinct (row, package, reviewer) triples and 42 distinct (row, package) merges | [CODE-VERIFIED] (executed counts) |
| Blocking drops where the verdict stayed FAIL | 45 of 49 rows end "ledger still FAIL via other rows" | [CODE-VERIFIED] (executed count) |
| Blocking drops where no blocking row was left | 4 rows in 3 merges end "ledger then has NO blocking row, so verdict PASS can be wrong": g3-sonnet-luna-ember-r3 (alias, F1), g5-ember2-luna-r2 (alias, F1), n5-sonnet-ember (design, F1 and F2) | [CODE-VERIFIED] |
| Reviewers that lose every line | total-loss merges at 6 of 6 and 8 of 8 lines for g7-haiku-luna2 and n4-sonnet-ember; the three long-anchor models are luna (27 of 30 drops are anchors), ember (24 of 33) and wonder; glm-5.3's 7 drops are all claims over 300 | [CODE-VERIFIED] as `summary.md` text |
| 80 reviewer runs with `block ok` false hold 335 raw findings and 229 ledger members | research/08:77 | [CODE-VERIFIED] as research text (recomputed there; not recomputed here) |
| "Four verdicts flipped" | three flips plus five total-loss merges that did not flip | [CODE-CONTRADICTED] as "4" (research/02:101; the three flips are re-confirmed above) |

What this gives B: the rule "refuse a PASS that rests on dropped blocking lines" would have fired on 3 of 264 merges (1.1 percent), the same 3 where the stored PASS was wrong, and on none of the 42 merges where a blocking row survived [derived from the `flags.tsv` wording, not re-executed against the ledgers]. The re-ask would be requested for 44 reviewer runs under the spec-loop trigger of 3.2, not 80.

### 4.3 Replay of the committed E2 reports (new in this proposal)

Method (read-only, no file written): `git ls-tree -r` of `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` at `6c0984326`; 1,222 unique report blobs under `TASK-WF-*/reviews*`; the last `findings-v1` block of each of the 1,215 reports that has one (5,270 lines); the three `TASK-WF-*/candidate.md` documents; `findings.locate`, `flat`, `_check_finding` and `refs_norm` imported from HEAD. Population caveat: this includes stale, superseded and failed-launch report folders, so it is not the 92 of audit-D. First failing rule over today's v1 rules: anchor 64, anchor2 29, claim 31, category 26, severity 3, refs 1 = 154 invalid lines (90 blocking) of 5,270. [CODE-VERIFIED by execution]

| Measurement | Result |
|---|---|
| Over-limit fields | anchor 64 (28 blocking), median 218 non-blocking / 240 blocking, max 680 / 355; anchor2 30 (22 blocking), max 253 / 279; claim 34 (22 blocking), min 303, max 435 / 403 |
| Lines that would pass unedited, anchor and anchor2 limit / claim limit | 250 / 350: 103 (59 blocking); 300 / 450: 120 (69 blocking); 400 / 500: 122 (70 blocking); 300 / 300: 87 (48 blocking); 200 / 450: 31 (20 blocking). The denominator is the 124 lines whose first failing rule is a length rule. |
| Does a 200-character prefix of an over-limit anchor still locate? (this answers GQ-017 for these documents) | Of 94 over-limit anchor and anchor2 fields, 89 occur verbatim in the candidate after flattening; for all 89 the prefix occurs exactly once and gives the same first span. 5 are not verbatim and are missing under any policy. |
| Does truncation change the extracted requirement refs (`refs_norm`)? | 0 of 125 lines with an over-limit field |
| What a claim cut at 300 removes | 34 claims; 3 to 135 characters cut, median 37.5, 9 cut more than 60. Sample tails: "the Task 6 check that existing parse tests pass cannot hold.", "Medium: the implementer must invent the sources.", "deletion of the `gh api user` mention." |

Reading of these results: they narrow every argument for B that rests on location or on lost reference tokens, because on these tasklist documents truncation of anchors keeps the location and the refs. They leave standing the claim cut (the tails above are consequence clauses; whether a cut changes the finding's meaning was not judged, so that is [UNVERIFIED]), the compliance and provenance arguments of 4.5, and the raise lever, which admits 120 of 124 lines without any edit. They do not transfer to multi-line anchors or code hunks (single-line table rows dominate this corpus) [UNVERIFIED for PR code].

### 4.4 What E1 recorded about the one bounded re-ask (tracked files under `.dev/eval-workspaces/shadow-model-combos/`)

| Run | First-pass compliance | Re-asks | Cause | After the re-ask |
|---|---|---|---|---|
| A1 | 0.6667 | 1 | reviewer-3 claims F6 and F10 over 300 characters (a limit failure) | 3 of 3 valid (`runs/...comboA-r1/panel/notes.md:2`) |
| A2 | 0.6667 | 1 | `coverage_rows` outside the reviewer's slice | 3 of 3 valid; before the re-ask the invalid block's 2 findings were out of clustering (11 of 11 against 13 of 13) (`...comboA-r2/panel/notes.md:4-14`) |
| A3 | 0.667 | 0 | one citation-path typo "fixed same run"; who fixed it is not stated [UNVERIFIED] | (`...comboA-r3/panel/notes.md:10`) |
| E2 | 0.6667 | 1 | citation line numbers counted inside the brief | valid (`...comboE-r2/panel/notes.md:2-3`) |
| E3 | 0.3333 | 2 | citation line numbers counted inside the briefs | reviewer 3 fully fixed; reviewer 2 still had two bad citations; "3 of 3 (to be confirmed by `review cluster`)" (`...comboE-r3/panel/notes.md:2-3`) |
| the other 10 runs | 1.0 | 0 | | |

Totals read from `results.md` and the notes: 15 runs, 45 reviewer cards, 6 first-pass misses, 5 re-asks, and all 5 re-asked blocks recorded valid afterwards; only 1 of the 5 was a limit failure. The mean first-pass compliance is 0.867 (13.001 / 15), which matches the combo mean that research/07 reports. This is not the E2 Spike 5 measurement: the reviewers are Agent-path subagents, the failure causes are mixed and n is 5. It is the first recorded recovery evidence in this repository, and it contradicts the word "unmeasured" in research/02 gap 5 (those values were "not read" there) without establishing a rate. The working-tree memory file `docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md:29,71` (untracked) adds "4 claims >300 chars needed re-asks" and "the bounded re-ask fixes them. Briefs should state the 300-char claim cap and the 200-char quote cap explicitly" [CODE-VERIFIED as text].

### 4.5 Evidence for the principle and for the provenance argument

- E2's own design review of the harness normaliser: blocking finding 2, "seal writes raw `p1.md` but combiner compares normalised lines", fixed by a `normalise(sealed line)` rule; blocking finding 4, a re-ask command lacked `--model`, `--permission-mode` and `--disallowedTools` so it could run on the default model; blocking finding 7, with session persistence on a reviewer can read peer transcripts (`research/scope/08-collab-r3-r4-r5.md:187-197`) [CODE-VERIFIED as research text]. Normalisation created a second form of every line that every later check had to know about; the re-ask created a new session surface.
- E2 note D10: the normaliser imports `parse_block` from the worktree and the launcher refuses when the worktree and installed `findings.py` differ, "the same parser-drift hazard r4 hit" (`research/scope/08-collab-r3-r4-r5.md:374`) [CODE-VERIFIED as research text]. Placing the repair inside the parser (C-01) removes the drift for any policy; it does not remove the second form of each line.
- The ledger stores `report_sha256` of the reviewer's text (`ledger.py:146`) and the members come from that text; under truncation the stored finding is no longer a byte copy of a line in the hashed report. [CODE-VERIFIED for the hash; the provenance consequence is a design inference.]
- E1 text against E2 text: `SKILL.md:343` forbids any normalisation by the orchestrator; E2 R-02 truncates anchors and claims, then re-asks once (`merged-requirements.md:1006` via research/02:129). Both allow one re-ask; only E2 edits. [CODE-VERIFIED as text of both documents.]
- An agent that persists reviewer text can corrupt it: in A2 the orchestrator "introduced 3 transcription corruptions" while persisting a card (`...comboA-r2/panel/notes.md:40-44`). This applies to an agent-run normaliser; a code normaliser would be deterministic, so it bears on where a repair may live, not on a repair written in code. [CODE-VERIFIED as text]

### 4.6 Status of the doc-sourced claims used in the conflict row

| Claim | Status |
|---|---|
| "Truncation addresses at most 88 of 92 lines and 48 of 49 blocking" (synth-05 6.3 option 1; research/02:109-111) | [CODE-VERIFIED] as arithmetic on the audit-D reasons (56+18+14 = 88; 24+14+10 = 48; unrecoverable 3 bad severity and 1 bad refs). It is an upper bound on lines parsed, not on lines located or lines whose meaning is kept. |
| "A prefix of a verbatim quote is a verbatim substring, so `locate` finds it" | [CODE-VERIFIED] (`findings.py:276-304`; replay 89 of 89) |
| "Re-ask recovery is unmeasured (Spike 5 not run)" | The Spike 5 part is unchanged. The word "unmeasured" is [CODE-CONTRADICTED] in part by 4.4 (5 of 5 re-asked blocks recorded valid, n small). |
| "E1 first-pass compliance: pilot mean 0.704, combo mean 0.867" (synth-05 6.3 related levers) | the combo mean [CODE-VERIFIED] by arithmetic from `results.md`; the pilot mean [UNVERIFIED] here |
| "`--resume` for gateway ids is only partly evidenced" | [UNVERIFIED] beyond the S2 spike (ember, luna, sonnet, haiku); not re-tested here |
| "Raising the anchor limit has not been tested" (research/08 section 7 point 9) | [CODE-VERIFIED] as to behaviour in this repository; 4.3 gives the first replay of what it would admit, not a test of reviewer behaviour under the new numbers |

## 5. Invariants

INV-A..INV-N are those of synth-06 6.12.0 (`synthesis/synth-06-conflict-log.md:54-67`). The conflict row lists INV-C and INV-I (HIGH) and INV-G (MEDIUM).

| Invariant | B-core (no edit, itemise, re-ask, refusal on PASS-by-loss) | B-raise (constants raised) |
|---|---|---|
| INV-A contract 1.8.0 names and the `merge_method` pair, byte-identical | Kept. No change to `contract.py` (it holds no limit constant, section 4.1) or to any reflect field name. `findings_block_compliance_rate` keeps its definition. `dropped` is not emitted by `cluster_cmd.py:155-162`. | Kept for names. Brief text in `reviewer-spec.md` changes (a skill file, not the contract). |
| INV-B `derive_verdict` map, exit codes 0/10/11/2, the 36-test matrix | Kept. Nothing in `derive_verdict` or the reflect profile is touched; the `dropped-blocking` refusal lives in the v1 merge. | Kept. |
| INV-C findings-v1 line grammar and `review merge` unchanged; unknown keys accepted | Kept. The accepted and rejected sets of lines are identical, `errors` keeps its shape, unknown keys stay accepted, `merge` keeps exit 0 except C-03's exit 12. | Endangered as worded: a widening. No line valid today becomes invalid, so every E2 tool that produces lines still works, and the harness truncation to 200/300 stays valid but no longer fires. Four boundary assertions are rewritten against the constants (`test_review_findings.py:113,117`; `test_review_findings_v2.py:199-200,241`). |
| INV-D `review-ledger/1`, the `ledger` group, exit 0/10/11, `merge` exit 0 | Kept with additive keys: a `dropped` object per reviewer entry and an acknowledgement option on `merge` (owner and reason). Older readers ignore the key (`ledger.load` checks the schema string alone, as the C-03 merged text records). | Kept. |
| INV-E `pr_submit` types and FSM | Untouched. | Untouched. |
| INV-F installed-path rule | Endangered only by how the brief generator and the re-ask text are delivered: both must land as installed text, never as an instruction to read `src/superclaude/...`. B requires that. | Same. |
| INV-G reviewers mutually blind and mechanically read-only | Kept on the Agent path and the swarm path: the re-ask carries only that reviewer's own rejected lines and no tool is granted. Endangered on the headless `claude -p --resume` path, where session persistence lets a reviewer read peer transcripts (E2 design-review finding 7, section 4.5); B excludes that path until isolation exists, which means itemise-only there. | Kept. |
| INV-H telemetry carries no document text | Kept by construction: `dropped` entries hold ids, rule names, lengths and a blocking state, never text. This is still a convention (research/15:48-56 per the invariant table). | Kept. |
| INV-I fail-closed: a review that did not happen never certifies PASS | Strengthened at one point: a PASS that rests on dropped blocking-or-unknown lines is refused. It does not close the partial-panel case, which is C-03's. | Kept. |
| INV-J repo review rule S1-S5 and the pinned caps | Kept. A re-ask is a continuation inside one round, not a review and not a fix cycle. Whether `test_f` (no other numbers in primitives) objects to "one re-ask" in a new primitive text is [UNVERIFIED]; `SKILL.md:343` already says "one bounded re-ask". | Kept. |
| INV-K sync and layout gates | Endangered by the brief generator: it edits skill and prompt sources, so `make sync-dev`, `make verify-sync` and the reflect skill edit fence apply. Which tests pin the text of `reviewer-spec.md:39` is [UNVERIFIED]. | Same. |
| INV-L shadow mode changes no verdict | Kept: in shadow mode `dropped` goes to the notes only. | Kept. |
| INV-M `reflect_status` enum and headless output directories | Untouched. | Untouched. |
| INV-N plugin mirror parity | Endangered when the loop prompt text changes (the limits sentence); the plugin copies move with it. [UNVERIFIED] which parity pins cover `document_review_loop_prompts.md`. | Same. |

Repository rules: no `.claude/` path is touched by this position; the generator output belongs in `src/superclaude/`; the fork-only PR rule is out of scope.

## 6. The test or measurement that would show B right or wrong

Rules for each measurement are written to a file before the first run, as C-02's replay does.

| Id | What | Shows B right | Shows B wrong |
|---|---|---|---|
| M1 | Conservation and fire-set replay. Run both parsers with the classifier over every reviewer report of the 264 audit-D merges (no model call). | For every report, non-blank lines equal kept plus priors plus dropped; the dropped rows reproduce 56/18/14/3/1 by rule and 49 with `blocking_state` true; the `dropped-blocking` refusal fires on exactly the 3 merges of 4.2 and on none of the other 261. It also explains the 17-19 lines audit-D could not (research/08:79, 111 against 92). | Conservation fails for any report, or the refusal fires where a blocking row survived, or misses one of the 3. |
| M2 | Re-ask recovery, the missing Spike 5 for B. For the 44 reviewer runs that held a dropped blocking line, send each reviewer its own rejected lines and rule messages once, on the Agent path and on the gateway path where `--resume` exists. Score per line: valid on re-parse; anchor verbatim in the candidate; claim meaning kept (blind judge); whether the model repeats the same violation. Run the same lines through the truncation upper bound (48 of 49) and through B-raise. | One re-ask recovers dropped blocking lines at a share close to the other two policies and keeps meaning; repeat offenders (luna 27 of 30 drops are anchors, ember 24 of 33) comply once the message names the limit. | The recovered share is below the other two by a margin fixed before the run, or the long-anchor models repeat the violation. Then B-core's cost shows up as refusals and B stands only through B-raise and the `unknown`/`true` refusal rule. |
| M3 | Separate the two incidence levers. First-pass compliance over a set of runs with the generated-brief change alone, then with the raised constants. Extend 4.3 to the 264 merges (lines admitted, blocking lines admitted, anchors that locate, row text length in the merged report). | The brief change alone lowers the over-limit rate (E1 notes and memory say claims over 300 were the repeat cause and the brief did not state the cap); raised constants admit about 120 of 124 lines with no new missing or ambiguous anchors. | The brief change does nothing and the raised limits admit lines that locate worse than the 89 of 94 verbatim rate measured in 4.3. |
| T-B1 | Property test on both parsers: for generated blocks, non-blank lines equal findings plus priors plus dropped. | holds | any counterexample |
| T-B2 | All existing pins pass unmodified in B-core (`test_review_findings.py:113,117` among them). | holds | any pin fails |
| T-B3 | Merge matrix: one reviewer with only dropped blocking lines (today's refusal at `ledger.py:150-157` stays); two reviewers, one with a dropped blocking line and one with an empty valid block (refusal `dropped-blocking`); a surviving blocking row (no refusal, ids printed); only `blocking: false` drops (no refusal, no re-ask); acknowledged drops (merge proceeds, ids listed). | as listed | any other outcome |
| T-B4 | `review cluster` output byte-equal on the existing v2 fixtures with the classifier in place (the INV-020 differential that C-01 found missing). | equal | any difference |
| T-B5 | The re-ask message contains no text from another reviewer's report and grants no tool. | holds | any leak |

## 7. Effect on future PR code review and on the rf-qa replacement

PR code review.
- pr-submit must run in the main session (research/13:183, P8 [CODE-VERIFIED as research text]), so a headless `--resume` re-ask is not the PR path; the re-ask there is an in-session continuation of an Agent reviewer or a second prompt carrying the reviewer's own first answer [UNVERIFIED for this module].
- The limit that bites in PR review is the optional citation `quote` (12..200) on code lines, which are not whitespace-flat and often exceed 200 characters (research/scope/03:534 [CODE-VERIFIED as research text]; luna, ember and wonder lost 30, 33 and 14 findings in E2). The 4.3 numbers come from tasklist documents and do not transfer. B's answers there are the re-ask or a higher quote limit (B-raise), not a cut quote. Because `quote` is optional and location is carried by `path:line`, one further B-compatible design is to treat an over-limit quote as the reason for a re-ask of that line only; that is not decided here.
- A dropped record with a blocking state maps onto the PR flow's "no file:line, no finding" rule (research/13:103) without any change to `Finding`, `Severity` or the FSM, because the record stays inside the review package and the adapter (C-10) sees only kept findings.

rf-qa replacement (first step at the `/task` gate).
- The reviewers are mechanically read-only (INV-G); the re-ask is a continuation that grants nothing, so the "lens agents on `bypassPermissions`" question in C-11 is not made worse.
- rf-qa has no behavioural oracle (C-11 row). The `dropped` record gives a replay oracle its first cheap check, conservation of lines, and the `dropped-blocking` refusal gives the confidence gate a rule for the case where the evidence for a block was lost.
- A ledger-based rf-qa replacement cannot take citation-only findings until `annotate` and ledger rows stop requiring `anchor` (synth-05 6.2 status text); that is C-01's deferral and is independent of this slot.

## 8. The strongest objection and the answer

Objection. B spends a model call and a round trip on a defect code can fix instantly, and the cost lands where the loop is most fragile. An over-limit line makes the reviewer's block invalid, so under C-02 its `prior` lines stop counting and under C-03 it leaves the quorum; if the transport cannot re-ask, or the model repeats the violation, the loop refuses or escalates over a cosmetic length error. Truncation has none of that, and the replay in 4.3 shows it keeps the location and the refs on every verbatim anchor in the corpus.

Answer.
1. The stall exposure is small and sits where the damage is. The refusal fires only when the round has no blocking row and a blocking-or-unknown line was lost: 3 of 264 merges in the audit-D data, the same 3 where a wrong PASS was stored. In 45 of the 49 blocking drops a blocking row survived and the verdict did not change. The re-ask under the spec-loop trigger covers 44 reviewer runs, not 80.
2. Incidence is reduced before any call is spent. The brief change is decided (CO-8) and targets the claims, which the v1 brief never limited (`document_review_loop_prompts.md:60`). Raising the constants admits 120 of the 124 length-failing lines unedited (96.8 percent, replay population), a share comparable to truncation's by-reason 88 of 92 (95.7 percent, audit-D population; the two populations differ), without producing a second form of the line.
3. Where truncation costs nothing measurable (anchors in these tasklist documents) B-raise gives the same recovery without an edit. Where truncation loses text (the 34 claims) the lost text is a consequence clause in the sampled tails, and E1 recorded claims over 300 as fixed by the reviewer's re-ask, not by a cut (`.../comboA-r1/panel/notes.md:2`; memory `:29,71`).
4. A transport that cannot re-ask degrades to itemise plus refusal-on-PASS-by-loss. That is strictly better than today, which drops silently and stored three wrong PASSes, and it needs no trust in an edited line. The acknowledgement option removes the deadlock.
5. What B does not have is a measured recovery rate for the re-ask on gateway models: that is M2, and until it is run the recovery claim rests on 5 of 5 in E1 (Agent path, n small) and the E2 S2 resume spike. If the objection's second half is true, that long-anchor models repeat the violation after being told the limit, B's cost becomes refusals and B-core alone is not enough; B-raise and the brief change then carry the weight.

## 9. Open facts this proposal does not settle

- Re-ask recovery on gateway ids and on the PR path ([UNVERIFIED]; M2).
- Whether a claim cut at 300 changes the finding's meaning (judge not run; 4.3).
- Whether a 200-character prefix stays unique for multi-line anchors and code hunks (4.3 covers single-line tasklist rows only).
- The 17 to 19 dropped lines audit-D could not explain (research/08:79 [UNVERIFIED cause]); M1 would classify them.
- The A3 "typo fixed same run" and who made the fix (`...comboA-r3/panel/notes.md:10`).
- The exact form of C-03's refusal object and of the acknowledgement option; B needs both and does not define either beyond what is stated in 3.3.
- Which static tests pin the text of the briefs and the loop prompt (INV-K, INV-N).
- Whether the owner accepts a widening of the findings-v1 grammar (B-raise); that is an owner decision, as the slot row says.

Status: Complete
