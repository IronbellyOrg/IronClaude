<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant B (Proposal B, default model, default persona) -->
<!-- Merge date: 2026-11-14T17:03:26Z -->

# Proposal B - slot C-06 (limits-repair-policy), merged

<!-- Source: Base (original, modified) - status, position and tag lines updated for the merged position (Changes 1, 7, 15) -->
Status: Complete (merged by /sc:adversarial; four unresolved conflicts and 20 UNADDRESSED Round 2.5 findings are listed in section 10 and are not closed by this document)
Position: the three location fields (`anchor`, `anchor2`, citation `quote`) are cut in code behind a keyword and the cut is recorded; every line that is still dropped is itemised; one bounded re-ask is made only for what remains invalid after the cut; a round whose only blocking evidence was dropped is refused (fail-closed). Whether the claim is cut and which eligibility rule decides clearing and quorum are unresolved (section 10).
Code state: HEAD 50d4d2b9d on branch ironbelly/shadow-runs (`git rev-parse --short HEAD`). E2 data read only through `git show` / `git ls-tree` / `git cat-file` at `6c0984326cbb8fb06c4a36065de58b171d3f8175`.
Tags: [CODE-VERIFIED] re-read or executed in the session that wrote the statement; [CODE-CONTRADICTED]; [UNVERIFIED]; [RECOMPUTED] arithmetic on figures already in this document; [DEBATE-ESTABLISHED] rests on a check the Round 2 advocates executed (the P273 replay, or the code checks N1-N9), cited to the round file and section, not re-run by the merge. "Replay" means a read-only execution that wrote no file. `round2-advocate-A.md` and `round2-advocate-B.md` are in the `adversarial/` folder beside this document.

## 1. The position in one paragraph

<!-- Source: Base (original, modified) - headline position reversed from "never edits reviewer text" to the code cut of the three location fields; the itemise, re-ask and fail-closed parts of the base are kept -->
<!-- Source: Variant A (Proposal A), Section 1 and Section 2 items 1-2 - merged per Change 1 -->
The core cuts the three location fields in code, records every cut, and in the part both positions share edits nothing else. A finding line whose `anchor`, `anchor2` or citation `quote` is longer than 200 flattened characters is shortened to its first 200 characters by one pure function inside both parsers, behind a keyword that is off at the parser and on at the three production call sites (section 3.6); the reviewer's report file is never edited. A line that is still invalid after the cut (bad severity, bad refs, bad JSON, a non-boolean `blocking`) is dropped as today, but every drop is itemised (line number, finding id, rule, field, original and kept length, and whether the line said `blocking: true`, `false` or something unreadable) and is never counted as zero. A reviewer who still has a dropped blocking-or-unknown line does not count toward clearing or toward the quorum floor (section 3.3), and a round whose only blocking evidence was dropped is refused instead of stored as PASS. One bounded re-ask, built only from that reviewer's own block and the parser's per-line errors, is made only for what remains invalid after the cut (E1 protocol text, `SKILL.md:343`; section 3.2). Over-limit incidence is also cut at the source by briefs generated from the parser constants (already decided, synth-06 CO-8); a claim-only raise of the constants is a separate owner decision and never part of the default policy (section 3.5). No field other than the three location fields is cut by the part of the policy both positions share. The claim is not decided here: it carries the wrong outcome (`document_review_loop_prompts.md:60`) and 34 claims over 300 characters in the committed E2 reports would lose 3 to 135 characters; the two positions on it are unresolved (C-001 claim part and C-009; sections 3.6 and 10). The cut replaces the base proposal's earlier default of never editing reviewer text for these three fields; the reasons are in section 3.6 and the evidence in sections 4.2 and 4.3.

## 2. How this position relates to the adjudicated slots C-01, C-02 and C-03

<!-- Source: Base (original, modified) - table kept; the C-02 row, the C-01 rows for the placement outcome, INV-003, INV-004, INV-014, INV-022 and INV-024, the C-03 row wording and the last row are modified; the other cells are original -->
<!-- Source: Variant A (Proposal A), Section 2 item 2 and Section 4.1 - merged per Change 16 (the INV-003 answer by the `repair=False` keyword, the INV-004 and INV-022 answers) -->
<!-- Source: Debate (round2-advocate-A.md section 6 bullet 6; round2-advocate-B.md section 6 bullet 5) - merged per Change 6 (the C-02 row states the eligibility question as unresolved) -->
The ids in the first column (INV-003, INV-004 and so on) are those of the C-01 adjudication's invariant table. They are a separate numbering from INV-A..INV-N (section 5) and from the Round 2.5 probe ids INV-001..INV-026 (section 10).

| Adjudicated outcome | Source | What the merged policy does with it |
|---|---|---|
| One limits-constants module imported by both parsers; one function "called from inside both `parse_block` functions" that must not invent an anchor; "the policy is C-06" | C-01 `ADJUDICATION-RESULT.md` (Winner, shared-now list); `merged-core-shape-and-finding-contract.md:17,27` | It uses the same placement and fills the policy: one repair step runs on each line before the check (`repair_line` before `_check_finding` and `check_finding`, section 3.6) and the failing rule of every remaining drop is recorded where the check fails; both happen inside both parsers. It reads the merged text "normalise-or-itemise" (`:27`) as both: the location fields are cut and everything else is itemised. The step sits inside both parsers, not in callers. |
| INV-003 (HIGH): a rescuing repair inside `parse_block` and "T1: every existing pin unmodified" cannot both hold (`test_review_findings.py:113,117`) | C-01 invariant table | Answered by the `repair=False` keyword. A direct parse keeps `ok` False for a 201-character anchor and a 301-character claim, `errors` keeps its shape, and `repairs` and `dropped` are additive keys, so every direct-parser pin (`test_review_findings.py:113,117`; `test_review_findings_v2.py:200,241`) stays unmodified. A claim-only raise of the constants (sections 3.5 and 5) would be a plain test rewrite, not a conflict. |
| INV-004, INV-010, INV-014, INV-022, INV-024 | C-01 invariant table | INV-004 holds because the cut sits in `findings_v2.parse_block` and the re-ask covers the non-length residual; the loss unit in v2 is the reviewer (`cluster.py:256-257`) and the cut removes it only for the length share (section 3.4). INV-010: `card_convert.py:85-86,199-201` must import the same constants under either policy. INV-014: a single reviewer whose only lines are dropped still gets today's refusal (`ledger.py:150-157`); the re-ask then runs from that refusal (section 3.2), not before the merge. INV-022 is satisfied because a repaired line locates and clusters like any other for verbatim anchors (sections 4.2 and 4.3); the unlocated and ambiguous cases are carried open in section 10 (Round 2.5 INV-016, INV-017). INV-024: the policy reaches both `parse_block` functions and, through the same constants, `card_convert.py:226`. |
| C-02: clearing needs a quorum of distinct `block_ok`-true reviewers typing `prior ... resolved`; a valid `prior open` vetoes; an invalid-block reviewer's priors are collected but not counted (INV-009 of C-02, `findings.py:186-190`, `ledger.py:139-140`) | C-02 `ADJUDICATION-RESULT.md` | The policy depends on it. After the cut a length-only fault on a location field no longer makes the block invalid, so what counts as a clearing-eligible reviewer is unresolved (C-002). The two alternatives are stated side by side in section 3.3 and listed in section 10; both keep `ok` and `state` as the parser's verdict on the cut lines and record `repaired` and `dropped` counts beside `block_ok`. The policy adds one thing to C-02's picture: a `prior` line with a bad status is itemised too (`findings.py:175-186`), not only finding lines. |
| C-03: union default, quorum as a merge-time refusal in `degrade` profiles with exit 12 and a `refusal` object, completion states recorded, reflect keeps `shortfall: visible` | C-03 `ADJUDICATION-RESULT.md`; `merged-output.md:9,61,123-127` | It depends on the refusal object and exit 12 and adds one refusal reason (`dropped_blocking`, section 3.3). No new exit value, no change to exit 0/10/11 (INV-D). It does not touch the reflect profile's `derive_verdict` (INV-B). C-03 INV-006 and INV-007 (merge unions findings of invalid-block reviewers; `requested` can collapse to 1) are unaddressed and the policy does not claim to close them: its refusal reason reads the per-reviewer `dropped` record, so it does not use `requested`. |
| C-01 states one repair step is shared; the policy is left to this slot | task prompt, C-01 result | The shared step is one pure cut function for the three location fields plus a classifier and a record. A change to any other field is not part of the shared step; the claim cut is unresolved (section 10). |

Where the policy disagrees with an adjudicated outcome: none. Where it is conditional on one: C-03's refusal object (without it the fail-closed rule has no vehicle and falls back to a warning), and C-02's quorum gate over `block_ok`, whose eligibility rule is unresolved (section 3.3 and section 10).

## 3. Design consequence for the shared core and the named modules

### 3.1 What the shared core holds

<!-- Source: Base (original, modified) - table kept; the rows "Limits constants", "Line classifier and drop record", "Result shape" and "Re-ask request" are modified, the row "Brief text" is original -->
<!-- Source: Base (original, modified) - "Limits constants" row: explicit exception for the third copy added per Change 13 -->
<!-- Source: Debate (round2-advocate-B.md section 6 bullet 12) - merged per Change 13 -->
<!-- Source: Variant A (Proposal A), Section 2 item 3 (`repairs`) merged with the base's classifier - merged per Change 2 (rows "Line classifier and drop record" and "Result shape") -->
<!-- Source: Variant A (Proposal A), Section 2 items 1-2 - merged per Change 1 (row "Repair step") -->
<!-- Source: Variant A (Proposal A), Section 2 item 8 and Debate (round2-advocate-A.md section 3 N6) - merged per Change 3 (row "First-pass carrier") -->
<!-- Source: Variant A (Proposal A), Section 2 item 6 and Debate (round2-advocate-A.md section 6 bullet 4; round2-advocate-B.md section 6 bullet 4) - merged per Change 4 (row "Re-ask request") -->
| Piece | Content | Where it sits |
|---|---|---|
| Limits constants | anchor and anchor2 12..200, citation quote 12..200, claim at most 300, refs at most 8, id at most 16 characters, citations 1..8, in one module imported by `findings.py` (`:104,108,114,118`), `findings_v2.py` (`:111,114-120,126,128,132,136`) and `card_convert.py` (`MAX_CLAIM = 300`, `MAX_REF_TEXT = 200`, `:85-86`). `card_convert.py` imports the shared constants and keeps its marked claim cut (`text[: MAX_CLAIM - 3] + "..."`, `:200-201`) as a legacy conversion measure, named here as an explicit exception that is reconsidered if the claim switch of section 3.6 is turned on. | the C-01 constants module (not a new decision) |
| Repair step | one pure `repair_line(obj)` that cuts `anchor`, `anchor2` and a citation `quote` to the first 200 characters of their whitespace-flattened form, before `_check_finding` and `check_finding`; it touches no `prior` line (details and the keyword in section 3.6) | the C-01 limits module, called from inside both `parse_block` functions |
| Line classifier and drop record | the existing checks return an error string today; each cut and each failing check also yields a structured record: one record per cut and per residual drop, `{line, finding_id, blocking_state (true, false, unknown), rule, field, original_chars, kept_chars, original_sha256}`, where `blocking_state` is `true`, `false` or `unknown` (absent or non-boolean `blocking`). The record carries lengths, ids and a hash, never reviewer text (INV-H). `refs_changed` is recorded when `refs_norm(original) != refs_norm(repaired)`; tail-only reference tokens are not copied into `refs`. | inside both `parse_block` functions (`findings.py:124-196`, `findings_v2.py:215-304`) |
| Result shape | `ok`, `state`, `findings`, `priors`, `errors` unchanged (errors stay `{line, msg}`); additive keys `repairs` and `dropped` (and `first_pass_state`, next row). Conservation holds per block: every non-blank line of the last findings block is exactly one of kept finding, prior line, or dropped record (non-blank lines = kept + priors + dropped). The merged report's `### Lx` block prints "shortened from N" next to the anchor status; there is no new table column. | both parsers; the merged-report render of C-01 |
| First-pass carrier | the parse result gains `first_pass_state`: `state` unless it is `complete`, else `invalid` when `repairs` is non-empty. `cluster_cmd.py:155-163` and `verify_cmd.py:136-138` emit `first_pass_state` and `repairs` beside the unchanged `state`. `findings_block_compliance_rate` is the share of cards whose `first_pass_state` is `complete`; `repaired_lines_rate` and `dropped_lines_rate` per model are reported next to it. The derivation is exact because the cut fires only on a field the unrepaired parse rejects [DEBATE-ESTABLISHED: `round2-advocate-A.md` section 3 N6]; a differential test checks it (section 6.2). The shadow-mode safety argument (debate point A-005) holds only while shadow lasts unless `first_pass_state` is carried. | both parsers; the two listings above |
| Brief text | the limits sentence in every brief is generated from the constants (synth-06 CO-8, decided). Today the v1 loop brief states only the anchor limit and the reflect brief omits the quote limit (`document_review_loop_prompts.md:60`; `reviewer-spec.md:39` per research/02:135). | the skill and prompt sources, one generator |
| Re-ask request | a function that builds one stateless message from one reviewer's own data: the original brief, the reviewer's own block and the parser's per-line errors (limits read from the constants), asking for the whole block back. It carries no other reviewer's content and no candidate change, and it grants no new tool (INV-G). | review package; the transport that sends it is per environment |

### 3.2 The re-ask (what is decided and what is a transport fact)

<!-- Source: Base (original, modified) - bullet 1 now reads first-pass validity from `first_pass_state` and applies the re-ask to what remains after the cut (Changes 3 and 4) -->
- One re-ask per reviewer per round, for what remains invalid after the cut. First-pass validity is recorded before the re-ask and is read from `first_pass_state` (section 3.1), so `findings_block_compliance_rate` keeps its E1 definition: valid on the first parse, over reviewers dispatched, before any re-ask (`SKILL.md:343,988` [CODE-VERIFIED]).

<!-- Source: Variant A (Proposal A), Section 2 item 6 and Debate (round2-advocate-A.md section 3 N1; round2-advocate-B.md section 1.2 N1) - merged per Change 4 (trigger; replaces the base's pre-merge trigger) -->
- Trigger. Re-ask only for what is still invalid after the cut. v1 (spec loop): the trigger is a refusal, either the dropped-blocking refusal of section 3.3 or the C-03 quorum refusal. A re-ask before the merge has no vehicle: no registered command parses a v1 block without merging, `merge_round` refuses a second merge of the same round (`ledger.py:114-118`), and a refused merge writes nothing (`merge_cmd.py:99-118`) [DEBATE-ESTABLISHED: `round2-advocate-A.md` section 3 N1, confirmed in `round2-advocate-B.md` section 1.2 N1]. After a refusal the coordinator re-asks the named reviewer and re-runs `merge` with the replacement report, whose `report_sha256` is in that round's entry. Dropped lines that said `blocking: false` are itemised and not re-asked in v1. Reflect: the E1 rule (an invalid block gets one bounded re-ask, `SKILL.md:343`) plus an amendment: an invalid block that carries a `prior` line is re-asked too.

<!-- Source: Base (original, modified) - transport bullet: stateless prompt by default, `--resume` an optimisation only, fallback for a transport that cannot re-ask restated (Change 4) -->
<!-- Source: Variant A (Proposal A), Section 2 item 6 - merged per Change 4 (the stateless prompt) -->
- Transport. The prompt is stateless by default: the original brief, the reviewer's own block and the parser's per-line errors, the whole block returned; no other reviewer's content and no new tool grant; `--resume` is an optimisation only. What each path offers: the Agent path continues the same agent (the E1 shadow runs did exactly this, section 4.4); the swarm HTTP path sends a second prompt that carries the reviewer's own first answer (workers get one user message and no session, `openai_compat.py:384-388`, synth-05 6.3 option 2 [CODE-VERIFIED as text of synth-05]); headless `claude -p` needs session persistence and `--resume` for the optimisation, which the E2 r2 spike S2 passed for ember, luna, sonnet and haiku and which is [UNVERIFIED] for other gateway ids (synth-05 6.3 option 2). A transport that cannot re-ask degrades to itemise plus the refusal of section 3.3.

<!-- Source: Base (original, modified) - record bullet: attempt-2 timing and the v1 record added (Change 4) -->
- Record. Reflect: attempt 2 is recorded before the `collected` commit and only while the earlier attempt is not `complete` (`manifest.py:371-383`: `OutOfOrder` once the stage is committed, `Conflict` when the earlier attempt `complete`d). In E1 run A2 the re-ask "could not be recorded in the manifest (stage 'collected' already committed; OutOfOrder refused)" (`.../comboA-r2/panel/notes.md:9-10` [CODE-VERIFIED]). v1 has no manifest: its record is the replacement report and the `report_sha256` of that report in the round's entry. The shape of the record belongs to slot C-08; this policy only requires that one exists. Whether the reflect step order allows the attempt-2 record to be driven from the carrier, and that a refusal-driven v1 re-ask leaves no ledger trace, are open (section 10: Round 2.5 INV-018, INV-003).
- Recovery evidence. Four of the five re-asks recorded in E1 are confirmed (Agent path, one length cause); no recovery rate exists for gateway models (debate point X-002). M2 (section 6.1) is the missing measurement.

### 3.3 Fail-closed in the v1 merge (spec loop)

<!-- Source: Base (original, modified) - bullet 1: keys `repaired` and `dropped` beside `block_ok` (Change 2) -->
- `merge_round` adds to each reviewer entry (`ledger.py:141-149`) the additive keys `repaired` and `dropped` beside `block_ok`: the counts of cuts and of dropped lines by `blocking_state` and by rule, and the dropped finding ids. `review-ledger/1` stays the schema string (`ledger.py:47-48` per C-03 merged text, INV-D additive keys only).

<!-- Source: Base (original, modified) - the base's single eligibility sentence in this bullet is replaced by two stated alternatives; no choice is made (Change 6) -->
<!-- Source: Debate (round2-advocate-B.md section 6 bullet 5; round2-advocate-A.md section 6 bullet 6) - merged per Change 6 -->
- Eligibility for clearing (C-02 B2) and for the C-03 floor. The debate did not settle this (C-002; section 10). Both positions agree that `ok` (v1) and `state` (v2) stay the parser's verdict on the cut lines, that `repaired` and `dropped` counts are recorded beside `block_ok`, and that the bare parser bit has a cost: on P273, 10 of 273 merges fall below the C-03 floor (`complete >= min(2, requested)`) when today's `ok` is the completeness test (Variant A counts at least 7 of 264 audit-D merges, three-reviewer panels only) [DEBATE-ESTABLISHED: `round2-advocate-B.md` section 1.1 W1 and section 3 E4; `round2-advocate-A.md` section 3 N4]. The two alternatives:
  - Alternative B (Variant B, final bullet 5; the advocate's final position on C-002 is Hybrid, 74 percent): a reviewer counts for clearing (C-02 B2) and for the floor (C-03) iff it has no block-level fault, no non-length drop on a `true` or `unknown` line, and no unresolved dropped line with `blocking_state` `true` or `unknown`. Dropped `blocking: false` lines do not disqualify. There is no `repaired == 0` knob.
  - Alternative A (Variant A, final bullet 6; the advocate's final position on C-002 is Variant 1, 80 percent): `block_ok` is the real parser verdict on the repaired lines (a length-only block is `ok` and `complete`; any residual fault makes it False), with `repaired` and `dropped` recorded, and C-03 may count only `repaired == 0` blocks for its floor as a recorded parameter, default off.

  The merged text does not choose between them. Round 2.5 INV-005 and INV-007 bear on the `blocking_state` inputs of either alternative (section 10).

<!-- Source: Base (original, modified) - the refusal bullet: firing statement replaced, implementation constraints added (Change 5) -->
<!-- Source: Debate (round2-advocate-A.md section 3 N2 and N5; round2-advocate-B.md section 1.2 N2 and N5, section 3 E3-E4) - merged per Change 5 -->
- Dropped-blocking refusal (reason `dropped_blocking`). It fires when the derived verdict would be PASS and an unacknowledged dropped line has `blocking_state` `true` or `unknown`. This is the "PASS by loss" case and only that case. The check runs at the end of `merge_round`, after the quorum check, on a working copy swapped in place on success (pins `test_review_ledger.py:352-361,373`); it reuses C-03's refusal subtype and exit 12 with `{"refusal": "dropped_blocking", reviewers, dropped}`, and the ledger file is unchanged [DEBATE-ESTABLISHED: `round2-advocate-A.md` section 3 N5, confirmed in `round2-advocate-B.md` section 1.2 N5]. Fire counts: 3 of 264 merges without the cut, 0 with it. The 0 of 264 is derived from the `flags.tsv` reason text (all four rows end "blocking finding dropped by merge (anchor>200)"; `round2-advocate-A.md` section 3 N2) and was not re-executed against the ledgers; the 0 of 273 was executed on P273 (`round2-advocate-B.md` section 3 E3 and E4). After the cut it is therefore insurance for what the cut cannot reach (bad severity, bad refs, bad JSON, a non-boolean `blocking`), not a rule justified by a measured fire rate.
- The human exit from that refusal, so that it cannot deadlock when a re-ask is impossible or fails: an owner-and-reason acknowledgement option on `merge`, the same shape as the `defer` that C-02 requires (owner and reason, terminal, counted). It lifts the refusal, is recorded in the round entry, and the acknowledged ids are listed in the merged report.
- When a blocking row survives, nothing is refused and the verdict is unchanged; the dropped ids are only printed. The audit-D data say this is 45 of the 49 dropped blocking lines (section 4.2). The recorded price (Variant B, Round 2 N1): in v1 a lost blocking line is never recovered in a merge that succeeds with another blocking row standing (36 of the 39 merges that carry a dropped blocking line on P273); it is itemised and printed only, and the cut of the location fields is what removes most of that cause [DEBATE-ESTABLISHED: `round2-advocate-B.md` section 1.2 N1 and section 3 E4].

<!-- Source: Base (original) - bullet kept -->
- `merge` keeps exit 0 for every merge that is not refused (INV-D). The merged report gains a per-reviewer "dropped lines" table (id, rule, blocking state). Today the warning keeps only the error count and the first message (`ledger.py:130-134`).
- Open and not closed here: the refusal sees only this round's drops (Round 2.5 INV-001), the acknowledgement is not bound to item ids (INV-006), two refusals can occur in sequence (INV-020), and a measured fire rate of zero does not exercise the code path (INV-026). See section 10.

### 3.4 Module by module

<!-- Source: Base (original, modified) - table kept; the rows "Spec review loop", "Reflect UC-1 and UC-2", "PR code review" and "rf-qa replacement" are modified, the row "Tasklist and workflow" is original -->
<!-- Source: Variant A (Proposal A), Section 7 point 1 and Debate (round2-advocate-A.md section 3 N7, section 6 bullet 12; round2-advocate-B.md section 1.1 W6, section 6 bullet 11) - merged per Change 12 (the `SKILL.md:343` sentence in the Reflect row) -->
<!-- Source: Variant A (Proposal A), Section 2 item 7 and Section 6 - merged per Change 16 (v2 loss unit in the Reflect row; quote and re-ask in the PR row) -->
| Module | Under the merged policy |
|---|---|
| Spec review loop (v1 engine, C-01) | Constants, `repair_line` (`ledger.py:128` passes `repair=True`), classifier, the `repairs` and `dropped` keys, the refusal-driven re-ask (section 3.2), the `dropped_blocking` refusal, and in the merged report the dropped-lines table and the "shortened from N" note. No pin changes: the direct-parser pins use the default `repair=False`. |
| Reflect UC-1 and UC-2 (v2 kernel, shadow mode) | The same classifier, keys and cut inside `findings_v2.parse_block`; `cluster_cmd.py:151` and `verify_cmd.py:133` pass `repair=True`, subject to the owner reading below. The listings (`cluster_cmd.py:155-163`, `verify_cmd.py:136-138`) emit the additive keys `first_pass_state` and `repairs` beside the unchanged `state`, `block_state` and `errors`, so `clusters.json` and the card listing are byte-equal on the existing v2 fixtures except for those two keys. `derive_verdict` and contract 1.8.0 are untouched. **The `SKILL.md:343` sentence.** It is step 4 of the reflect shadow procedure only (no match in the v1 prompt or spec-panel texts) and it is pinned (`tests/cli/reflect/test_shadow_skill_contract.py:229-232`) [DEBATE-ESTABLISHED: `round2-advocate-A.md` section 3 N7]. The Normalize sentences stay byte-identical; one sentence is added after them: the package's parser step shortens location fields in code and records every shortening, the orchestrator still never edits a finding, and the first-parse compliance rate reads `first_pass_state`. The owner confirms that package code is not "the orchestrator"; if not, the v2 call sites stay at `repair=False` (itemise and re-ask only) and the v1 `merge` keeps the cut, because no text rule binds it. **The v2 loss unit.** One over-limit location field no longer invalidates the whole reviewer (`cluster.py:255-257` skipped it before). The cut removes the loss unit only for the length share: a claim fault or any non-length fault (reflect's residual is non-length for both policies: coverage rows, citation line numbers; debate point X-003) still costs the reviewer unless the re-ask works. The "4 of 92" figure is a v1 floor and does not size the v2 residual. Open: the unchanged Normalize text and the additive sentence use "invalid" for two different states (Round 2.5 INV-019), and the loss unit is removed only for the length share (INV-024); section 10. |
| Tasklist and workflow | Reached through reflect UC-1 (C-05); same as reflect. |
| PR code review (later) | The panel emits citations; the limit that bites there is the optional citation `quote` (12..200, `findings_v2.py:80`), which E2's own requirement does not name (synth-05 6.3 option 4). A `quote` prefix passes the `verify_cmd.py:68-72` substring test [CODE-VERIFIED], so the quote is cut like the other location fields; the quote limit is a per-profile parameter; the re-ask is the stateless in-session form. Neither variant measured PR code, so a code corpus is required before a PR module relies on this (section 7). |
| rf-qa replacement (later) | Reviewers stay mechanically read-only (INV-G); the re-ask is a stateless second prompt, not a new tool grant; the `dropped` record is the conservation check a replay oracle needs. Section 7. |

### 3.5 The raise-the-limits lever, narrowed to claims

<!-- Source: Base (original, modified) - the raise lever is narrowed from anchor, anchor2 and claim to a claim-only raise and made a separate owner decision (Change 8) -->
<!-- Source: Variant A (Proposal A), Round 2 N8 and Debate (round2-advocate-B.md section 1.1 W3, section 3 E1, section 6 bullet 8) - merged per Change 8 -->
The lever is a claim-only raise of the claim limit to 450. It is a separate owner decision and never part of the default policy. The cut covers the anchors, so the merged text does not propose raising `anchor` or `anchor2`; any fixed limit has a tail, and a raise needs an admission curve and an owner decision (debate points C-011 and U-011). On P273 a claim limit of 450 admits 12 of 12 claim-dependent lines and 400 admits 11 of 12 (the exception is 401) [DEBATE-ESTABLISHED: `round2-advocate-B.md` section 3 E1 and section 6 bullet 8]. A claim-only raise is a widening of the findings-v1 line grammar (every line valid today stays valid), so it touches INV-C (section 5), which is why it is an owner decision, as the slot row says. The CO-8 brief change (limits stated from the constants) is common ground and is not a limit change.

Pin cost, per site: a claim-only raise rewrites 2 assertion sites (`tests/review/test_review_findings.py:117`, `tests/review/test_review_findings_v2.py:241`), and 3 if `card_convert.py` imports the shared claim constant (`tests/review/test_review_card_convert.py:500`); the quote pin (`tests/review/test_review_findings_v2.py:200`) changes only if the quote limit is also raised [DEBATE-ESTABLISHED: `round2-advocate-A.md` section 3 N8, confirmed in `round2-advocate-B.md` section 1.1 W3].

The replay of section 4.3 (anchors and claims raised together; 120 of the 124 length-failing lines pass at 300/300/450) stays there as the evidence of what a raise admits on the 1,215-report corpus; it is no longer the lever.

### 3.6 What the policy does and does not do

<!-- Source: Variant A (Proposal A), Section 1 and Section 2 items 1-2; Debate (round2-advocate-A.md section 6 bullet 1; round2-advocate-B.md section 6 bullet 1, section 0) - merged per Change 1 (replaces the base's list of what the policy does not do) -->
**The cut.**

- `parse_block(text, *, repair=False)` in both parsers. The production call sites `ledger.py:128`, `cluster_cmd.py:151` and `verify_cmd.py:133` pass `repair=True`; the v2 sites (`cluster_cmd.py`, `verify_cmd.py`) are subject to the owner reading of `SKILL.md:343` (section 3.4). A test asserts that every production call site passes the keyword explicitly and that the default stays `False`. The three production call sites rewrite no pin.
- One pure `repair_line(obj)` in the C-01 limits module cuts `anchor`, `anchor2` and a citation `quote` to the first 200 characters of their whitespace-flattened form, before `_check_finding` and `check_finding`. It touches no `prior` line. The report file is never edited. The direct-parser pins (`test_review_findings.py:113,117`, `test_review_findings_v2.py:200,241`) stay unmodified.
- The position: the three location fields are cut in code and recorded; no field other than these three is cut by the part of the policy both positions share (the claim is unresolved, see below); everything that is dropped is itemised.
- Why. Both advocates' final bullet 1 is identical for the three location fields, and Variant B's advocate moved from "no edit by default" to the cut for three reasons: the replay and the second-population run (all 70 over-limit `anchor` and `anchor2` fields on P273 that occur verbatim keep a unique same-span prefix; the 1,215-report replay gives 89 of 89, section 4.3), no v1 vehicle for a re-ask before the merge (`merge_cmd.py:99-118`), and 10 of 273 merges below the C-03 floor under a no-edit rule [DEBATE-ESTABLISHED: `round2-advocate-B.md` section 0, section 1.2 N1 and section 3 E2 and E4].
- Evidence limit. The 70 of 70 and 89 of 89 results cover `anchor` and `anchor2` on single-line tasklist rows only. The `quote` cut has no location measurement; it rests on the substring test at `verify_cmd.py:68-72`. No PR-code or multi-line corpus exists. Round 2.5 INV-017 (HIGH: a shorter prefix that matches more than one place) is not closed by this text and is carried open (section 10).

<!-- Source: Base (original, modified) - the base's single "what B does not do" sentence is replaced by the statements below (Change 1); the `card_convert.py` sentence is modified per Change 13 -->
**What the policy does not do.**

- It does not change a reviewer's `blocking`, `severity`, `category` or `refs`, and it has no calibrator or debate. The claim is the one other field in question and is stated below.
- `card_convert.py:199-201` keeps its marked claim cut (297 characters plus `...`), a measurement converter for legacy cards, not a production path. It imports the shared constants (section 3.1) and is named here as an explicit exception, so that the package carries no silent split; it is reconsidered if the claim switch below is turned on. Round 2.5 INV-022 (two implementations of the same claim-cut arithmetic if a claim cut is adopted) is carried open (section 10).

<!-- Source: Debate (round2-advocate-A.md section 1.3 and section 6 bullets 1 and 11; round2-advocate-B.md section 1.3 and section 6 bullets 2 and 10) - merged per Change 7; both positions recorded, neither chosen -->
<!-- Source: Variant A (Proposal A), Section 2 item 7 and Section 7 point 3 - merged per Change 7 (Proposal A's claim cut) -->
**The claim field (unresolved: C-001 claim part and C-009).** Both positions are stated; this document does not choose.

- Variant A's position (its final position on C-009 is Hybrid, 62 percent): cut the claim to 297 characters plus `...` with a visible marker, a "shortened from N" row note and `original_sha256`, kept unless the blind two-judge test K2 fails. Evidence on this side, from Variant B's P273 runs [DEBATE-ESTABLISHED: `round2-advocate-B.md` section 1.3 (i)-(ii), section 3 E3 and E4]: with an anchors-only cut, 2 merges sit below the C-03 floor and 15 merges have a bad block, against 4 with the claim cut; 12 dropped lines (8 blocking) have a claim over 300.
- Variant B's position (its final position on C-009 is Variant 2, 76 percent): no claim cut by default, because anchors-only and cut-all give identical verdicts on all 273 merges, a claim limit of 450 with no claim cut reproduces cut-all, and the meaning of a cut claim is unmeasured by anyone; the claim carries "X is wrong because Y" (`document_review_loop_prompts.md:60`) [DEBATE-ESTABLISHED: `round2-advocate-B.md` section 1.3 (ii)-(iii)].
- K2 in both forms. Variant A (final bullet 11): the claim cut stands unless more than 20 percent of blocking claims are judged by both judges to lose a decision-relevant clause (the falsifier of the cut). Variant B (final bullet 10): a claim cut is allowed only if both judges mark at most 20 percent of blocking claims as losing a decision-relevant clause (the precondition for the cut). The test population is the 34 claims of the replay in section 4.3 (22 blocking).
- The default is the owner's decision. What both agree on is implemented first: `repair_line` covers the three location fields; the claim cut is a separate switch.

## 4. Evidence

### 4.1 Code facts at HEAD

<!-- Source: Base (original) - table kept; two cells carry an added clause marking the state at HEAD against the merged policy (rows "Both parsers drop..." and "`cluster_cmd.py` writes a fixed key set") -->
| Fact | Evidence | Tag |
|---|---|---|
| Both parsers drop the whole line on any violation and set the block not-ok / `invalid`; at HEAD there is no repair step (the cut of section 3.6 is the proposed change) | v1 `findings.py:188-195`; v2 `findings_v2.py:284-287,299-303` | [CODE-VERIFIED] |
| Limits: v1 anchor 12..200 required, anchor2 12..200, refs at most 8, claim at most 300; v2 repeats them and adds citation quote 12..200 | `findings.py:104,108,111-118`; `findings_v2.py:80,111,114-120,126,132,136` | [CODE-VERIFIED] |
| Length is counted after whitespace flattening, in characters | `findings.py:79-87`, `flat` at `:272-273` | [CODE-VERIFIED] |
| The loss unit is one finding in the v1 ledger and one reviewer in v2 clustering | `ledger.py:112,135-138,150-157`; `cluster.py:218-222,256-257`; `cluster_cmd.py:157-161` | [CODE-VERIFIED] |
| The only merge-time visibility of a drop is one string per reviewer with the error count and the first message | `ledger.py:130-134` | [CODE-VERIFIED] |
| Pins that fix the limits: 201-character anchor and 301-character claim give `ok` False; v2 quote 200 ok / 201 not; v2 claim 300 / 301 | `tests/review/test_review_findings.py:113,117`; `tests/review/test_review_findings_v2.py:199-200,241` | [CODE-VERIFIED] |
| A row clears to `resolved_check` only when a hunk touches its `span` or `span2`, and spans come from `locate` of the anchor (first occurrence wins, `anchor_ambiguous` is only a flag) | `ledger.py:301-337`; `findings.py:276-304,346-352` | [CODE-VERIFIED] |
| The v1 brief states the anchor limit (12 to 200) and gives the claim as "one sentence naming the wrong outcome" with no claim limit; blocking needs a sentence "X is wrong because Y" | `rules/prompts/document_review_loop_prompts.md:31,60` | [CODE-VERIFIED] |
| E1 protocol: the first-parse compliance rate is recorded before any re-ask; "The orchestrator never edits, remaps or normalizes a reviewer's findings itself"; one bounded re-ask | `src/superclaude/skills/sc-reflect-protocol/SKILL.md:343,988` | [CODE-VERIFIED] |
| `card_convert.py` is a third copy of the limits and the only production-tree truncation: claim cut to 297 characters plus a visible `...` | `card_convert.py:85-86,199-201` | [CODE-VERIFIED] |
| `contract.py` contains no limit or anchor constant (grep for `anchor\|MAX_\|limit\|1.8.0` returns only the 1.8.0 comment at `:127`) | `src/superclaude/cli/reflect/contract.py` | [CODE-VERIFIED] |
| `cluster_cmd.py` writes a fixed key set per card (`card`, `reviewer_id`, `state`, `block_state`, `errors`); the merged policy adds `first_pass_state` and `repairs` to this set (section 3.1) | `cluster_cmd.py:155-162` | [CODE-VERIFIED] |

### 4.2 The audit-D drop data (E2, `6c0984326`, read through `git show`) and the second population P273

<!-- Source: Base (original) - audit-D files line and table kept -->
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

<!-- Source: Base (original, modified) - the base paragraph after the audit-D table is rewritten: fire counts stated as 3 of 264 without the cut and 0 with it, the count of merges where a blocking row survived corrected, the pre-merge re-ask count removed (Change 9) -->
<!-- Source: Debate (round2-advocate-A.md section 3 N2) - merged per Change 9 (the 0 of 264 labelled as derived from the `flags.tsv` reason text) -->
What this gives: without the cut, the refusal of section 3.3 would have fired on 3 of 264 merges (1.1 percent), the same 3 where the stored PASS was wrong. 42 merges carry a dropped blocking line and 3 of them have no blocking row left, so on 39 a blocking row survived and the refusal does not fire [RECOMPUTED: 42 minus 3; derived from the `flags.tsv` wording, not re-executed against the ledgers]. With the cut the refusal fires on 0 of 264: all four rows with no surviving blocking row end "blocking finding dropped by merge (anchor>200)" [DEBATE-ESTABLISHED: `round2-advocate-A.md` section 3 N2; derived from the `flags.tsv` reason text, not re-executed against the ledgers].

<!-- Source: Debate (round2-advocate-B.md section 3 E1-E5, section 1.1 W1 and W2, section 1.2 N2 and N3, section 4 rows A-001 and A-003; round2-advocate-A.md section 4 rows A-001 and A-003) - merged per Change 9 (second population added, labelled) -->
#### Second population P273 (Round 2 replay by Variant B's advocate)

Every figure in this block is [DEBATE-ESTABLISHED: `round2-advocate-B.md` section 3 E1-E5, section 1.1 W1-W2 and section 1.2 N2-N3]; the merge did not re-run it.

Method (read-only): `git ls-tree -r` and `git cat-file --batch` at `6c0984326` under `.dev/eval-workspaces/tasklist-review-panel/20261111-a1`; `combos/<row>/<package>/ledger.json` for the three packages `TASK-WF-designSpec-20261107-075614`, `TASK-WF-makeTheAliasOnly-20261105-051649` and `TASK-WF-design-20261108-041415`; rows filtered with audit-D's own exclusion pattern (`contaminated|superseded|quarantine|^i1-|^i2-`); reports taken from the last round's `report` paths; 279 merges found, 6 skipped because a report blob is absent from the commit, 273 analysed (855 reviewer-runs); HEAD `findings.parse_block`, `findings.locate`, `findings._check_finding` and `ledger.merge_round` imported read-only; every dropped line gets all its faults (audit-D's check returns the first only).

| Count | audit-D | P273 |
|---|---|---|
| merges | 264 | 273 |
| dropped lines | 92 | 90 |
| blocking dropped lines | 49 | 46 |
| reviewer-runs with `ok` False | 80 | 79 (of 855) |

The net difference of 9 merges (273 against 264) is reported by Variant B as a 15-merge difference that it did not reconcile (audit-D's `exclude-list.txt` has 54 reviewer-level entries that were not applied); it is not reconciled here. Variant B states that the order of magnitude and every ranking below do not depend on it. The 90 P273 lines are 57 anchor first-fault, 18 anchor2, 11 claim, 3 severity and 1 refs.

- Baseline. Re-merging with HEAD `ledger.merge_round` reproduces the stored verdict in 273 of 273. A stored PASS with a dropped `blocking: true|unknown` line occurs in exactly 3 merges (g3-sonnet-luna-ember-r3 and g5-ember2-luna-r2 on makeTheAlias, n5-sonnet-ember on design); the four lines have anchors of 215, 218, 240 and 240 characters, claims of 79 to 166 characters and no second fault. The `unknown` class (bad JSON, non-boolean `blocking`) has 0 members.
- Where the 79 `ok` False runs come from. 75 are length-only (40 with at least one dropped `blocking: true|unknown` line, 35 with only `blocking: false` drops), 2 carry a non-length line fault and 2 are block-level faults (missing, unclosed or multiple block).
- Prefix location. 75 over-limit anchor and anchor2 fields: 70 occur verbatim after flattening, and for all 70 the 200-character prefix occurs exactly once with the same first span as the full anchor (blocking 34 of 37, non-blocking 36 of 38); 5 are not verbatim (3 blocking) and are missing under any policy. This reproduces section 4.3's 89 of 89 on a second population. Single-line tasklist rows only.
- Verdict simulation. Cut all (anchor, anchor2 and claim): 3 verdicts change PASS to FAIL (exactly the three wrong PASSes), 16 merges gain 16 blocking rows (21 rows in total), 13 of those 16 were already FAIL, no FAIL becomes PASS, and 4 merges still have a bad block. Cut anchors only: the same 3 flips, 15 merges with a bad block, and verdicts identical to cut-all on all 273 merges. Cut anchors with the claim limit at 450: identical to cut-all. Not measured: whether the 16 added blocking rows are true or false blockers.
- Floor (C-03 floor `min(2, requested)`; panel sizes across the 273 merges: 3: 144, 2: 51, 4: 45, 5: 27, 1: 6). Merges below the floor: 10 with today's `ok` as the completeness test; 5 with an eligibility that tolerates dropped `blocking: false` lines; 0 with a perfect re-ask on every length-only run; 0 with the cut; 2 with the anchors-only cut. 39 merges (40 runs, 14 percent of merges) carry at least one dropped blocking line.
- Recovery by policy (lines and blocking lines recovered, of 90 and 46). Cut anchor, anchor2 and claim: 86 and 45. Cut anchors only: 74 and 37. Cut anchors plus claim limit 450: 86 and 45. Claim limit 450 alone: 11 and 8. Raise anchors and anchor2 to 300 and claim to 450: 82 and 44. Raise to 250 and 350: 70 and 38. Four lines are unreachable by any length policy (3 bad severity, 1 refs). Claim-dependent lines: 12 (8 blocking), lengths 303 to 401, median 339.

What the two populations support (debate points A-001 and A-003, both advocates: Neither). Audit-D and P273 are adequate for ordering the policies but cannot give a recovery percentage; a single population must be frozen before any percentage is stated. Reviewer behaviour is not stationary (CO-8 changes the claim rate), so the policy is written to hold in both directions.

### 4.3 Replay of the committed E2 reports

<!-- Source: Base (original) - method paragraph and table kept -->
Method (read-only, no file written): `git ls-tree -r` of `.dev/eval-workspaces/tasklist-review-panel/20261111-a1` at `6c0984326`; 1,222 unique report blobs under `TASK-WF-*/reviews*`; the last `findings-v1` block of each of the 1,215 reports that has one (5,270 lines); the three `TASK-WF-*/candidate.md` documents; `findings.locate`, `flat`, `_check_finding` and `refs_norm` imported from HEAD. Population caveat: this includes stale, superseded and failed-launch report folders, so it is not the 92 of audit-D. First failing rule over today's v1 rules: anchor 64, anchor2 29, claim 31, category 26, severity 3, refs 1 = 154 invalid lines (90 blocking) of 5,270. [CODE-VERIFIED by execution]

| Measurement | Result |
|---|---|
| Over-limit fields | anchor 64 (28 blocking), median 218 non-blocking / 240 blocking, max 680 / 355; anchor2 30 (22 blocking), max 253 / 279; claim 34 (22 blocking), min 303, max 435 / 403 |
| Lines that would pass unedited, anchor and anchor2 limit / claim limit | 250 / 350: 103 (59 blocking); 300 / 450: 120 (69 blocking); 400 / 500: 122 (70 blocking); 300 / 300: 87 (48 blocking); 200 / 450: 31 (20 blocking). The denominator is the 124 lines whose first failing rule is a length rule. |
| Does a 200-character prefix of an over-limit anchor still locate? (this answers GQ-017 for these documents) | Of 94 over-limit anchor and anchor2 fields, 89 occur verbatim in the candidate after flattening; for all 89 the prefix occurs exactly once and gives the same first span. 5 are not verbatim and are missing under any policy. |
| Does truncation change the extracted requirement refs (`refs_norm`)? | 0 of 125 lines with an over-limit field |
| What a claim cut at 300 removes | 34 claims; 3 to 135 characters cut, median 37.5, 9 cut more than 60. Sample tails: "the Task 6 check that existing parse tests pass cannot hold.", "Medium: the implementer must invent the sources.", "deletion of the `gh api user` mention." |

<!-- Source: Base (original, modified) - the reading paragraph is restated for the merged policy: the location evidence now supports the cut, the claim evidence stays open (Changes 1 and 7) -->
Reading of these results: on these tasklist documents a 200-character prefix of an over-limit anchor keeps the location and the refs, which is the evidence for the cut of the three location fields (section 3.6); section 4.2 reproduces it on a second population (70 of 70). They leave open whether a claim cut changes the finding's meaning (the tails above are consequence clauses; whether a cut changes the meaning was not judged, so that is [UNVERIFIED]; K2 in section 3.6 is the test), the compliance and provenance arguments of 4.5, and what a raise admits (120 of 124 lines at 300/300/450; section 3.5 narrows the lever to claims). They do not transfer to multi-line anchors or code hunks (single-line table rows dominate this corpus) [UNVERIFIED for PR code].

### 4.4 What E1 recorded about the one bounded re-ask (tracked files under `.dev/eval-workspaces/shadow-model-combos/`)

<!-- Source: Base (original) - table kept -->
| Run | First-pass compliance | Re-asks | Cause | After the re-ask |
|---|---|---|---|---|
| A1 | 0.6667 | 1 | reviewer-3 claims F6 and F10 over 300 characters (a limit failure) | 3 of 3 valid (`runs/...comboA-r1/panel/notes.md:2`) |
| A2 | 0.6667 | 1 | `coverage_rows` outside the reviewer's slice | 3 of 3 valid; before the re-ask the invalid block's 2 findings were out of clustering (11 of 11 against 13 of 13) (`...comboA-r2/panel/notes.md:4-14`) |
| A3 | 0.667 | 0 | one citation-path typo "fixed same run"; who fixed it is not stated [UNVERIFIED] | (`...comboA-r3/panel/notes.md:10`) |
| E2 | 0.6667 | 1 | citation line numbers counted inside the brief | valid (`...comboE-r2/panel/notes.md:2-3`) |
| E3 | 0.3333 | 2 | citation line numbers counted inside the briefs | reviewer 3 fully fixed; reviewer 2 still had two bad citations; "3 of 3 (to be confirmed by `review cluster`)" (`...comboE-r3/panel/notes.md:2-3`) |
| the other 10 runs | 1.0 | 0 | | |

<!-- Source: Base (original, modified) - the totals paragraph: the count of re-asked blocks recorded valid corrected to four confirmed and one unconfirmed (Change 9) -->
Totals read from `results.md` and the notes: 15 runs, 45 reviewer cards, 6 first-pass misses, 5 re-asks, of which four are confirmed valid afterwards and one is unconfirmed (orchestrator-reported); only 1 of the 5 was a limit failure. The mean first-pass compliance is 0.867 (13.001 / 15), which matches the combo mean that research/07 reports. This is not the E2 Spike 5 measurement: the reviewers are Agent-path subagents, the failure causes are mixed and n is 5. It is the first recorded recovery evidence in this repository, and it contradicts the word "unmeasured" in research/02 gap 5 (those values were "not read" there) without establishing a rate (debate point X-002: no recovery rate exists for gateway models). The working-tree memory file `docs/memory/reflect/deviation-patterns-brainstorm-reflect-panel.md:29,71` (untracked) adds "4 claims >300 chars needed re-asks" and "the bounded re-ask fixes them. Briefs should state the 300-char claim cap and the 200-char quote cap explicitly" [CODE-VERIFIED as text].

### 4.5 Evidence for the principle and for the provenance argument

<!-- Source: Base (original) - bullets 1, 2, 4 and 5 kept -->
- E2's own design review of the harness normaliser: blocking finding 2, "seal writes raw `p1.md` but combiner compares normalised lines", fixed by a `normalise(sealed line)` rule; blocking finding 4, a re-ask command lacked `--model`, `--permission-mode` and `--disallowedTools` so it could run on the default model; blocking finding 7, with session persistence on a reviewer can read peer transcripts (`research/scope/08-collab-r3-r4-r5.md:187-197`) [CODE-VERIFIED as research text]. Normalisation created a second form of every line that every later check had to know about; the re-ask created a new session surface.
- E2 note D10: the normaliser imports `parse_block` from the worktree and the launcher refuses when the worktree and installed `findings.py` differ, "the same parser-drift hazard r4 hit" (`research/scope/08-collab-r3-r4-r5.md:374`) [CODE-VERIFIED as research text]. Placing the repair inside the parser (C-01) removes the drift for any policy; it does not remove the second form of each line.
<!-- Source: Base (original, modified) - provenance bullet: restated for the cut of the location fields; the byte-copy objection is kept only for a claim cut (Change 14) -->
<!-- Source: Debate (round2-advocate-B.md section 4 row C-012; round2-advocate-A.md section 4 row C-012) - merged per Change 14 -->
- The ledger stores `report_sha256` of the reviewer's text (`ledger.py:146`) and the members come from that text. Under the cut the stored `anchor`, `anchor2` and `quote` remain a flattened-form substring of the reported line, and each `repairs` item carries `original_sha256` of the flattened original field, so `original_sha256` and the existing `report_sha256` keep provenance. The stored finding is a recorded derived value, not a byte copy of a line in the hashed report; the byte-copy objection is kept only for a claim cut (C-012, unresolved; sections 8 and 10). [CODE-VERIFIED for the hash; the provenance consequence is a design inference.]
- E1 text against E2 text: `SKILL.md:343` forbids any normalisation by the orchestrator; E2 R-02 truncates anchors and claims, then re-asks once (`merged-requirements.md:1006` via research/02:129). Both allow one re-ask; only E2 edits. [CODE-VERIFIED as text of both documents.]
- An agent that persists reviewer text can corrupt it: in A2 the orchestrator "introduced 3 transcription corruptions" while persisting a card (`...comboA-r2/panel/notes.md:40-44`). This applies to an agent-run normaliser; a code normaliser would be deterministic, so it bears on where a repair may live, not on a repair written in code. [CODE-VERIFIED as text]

### 4.6 Status of the doc-sourced claims used in the conflict row

<!-- Source: Base (original, modified) - table kept; the rows on the prefix of a verbatim quote and on re-ask recovery are modified (Change 9); the other rows are original -->
| Claim | Status |
|---|---|
| "Truncation addresses at most 88 of 92 lines and 48 of 49 blocking" (synth-05 6.3 option 1; research/02:109-111) | [CODE-VERIFIED] as arithmetic on the audit-D reasons (56+18+14 = 88; 24+14+10 = 48; unrecoverable 3 bad severity and 1 bad refs). It is an upper bound on lines parsed, not on lines located or lines whose meaning is kept. |
| "A prefix of a verbatim quote is a verbatim substring, so `locate` finds it" | [CODE-VERIFIED] (`findings.py:276-304`; replay 89 of 89; 70 of 70 on the second population P273, section 4.2 [DEBATE-ESTABLISHED: `round2-advocate-B.md` section 3 E2]) |
| "Re-ask recovery is unmeasured (Spike 5 not run)" | The Spike 5 part is unchanged. The word "unmeasured" is [CODE-CONTRADICTED] in part by 4.4 (four of the five re-asked blocks confirmed valid, one unconfirmed, n small). |
| "E1 first-pass compliance: pilot mean 0.704, combo mean 0.867" (synth-05 6.3 related levers) | the combo mean [CODE-VERIFIED] by arithmetic from `results.md`; the pilot mean [UNVERIFIED] here |
| "`--resume` for gateway ids is only partly evidenced" | [UNVERIFIED] beyond the S2 spike (ember, luna, sonnet, haiku); not re-tested here |
| "Raising the anchor limit has not been tested" (research/08 section 7 point 9) | [CODE-VERIFIED] as to behaviour in this repository; 4.3 gives the first replay of what it would admit, not a test of reviewer behaviour under the new numbers |

## 5. Invariants

<!-- Source: Base (original, modified) - the 14-row table is kept (debate point S-005: the base table is wider); the columns are renamed for the merged policy and the cells of INV-A, INV-B, INV-C, INV-D, INV-G, INV-H, INV-I, INV-J, INV-K and INV-L are modified; the rows INV-E, INV-F, INV-M and INV-N are original -->
<!-- Source: Variant A (Proposal A), Section 4 - merged per Change 11 (INV-C "partly endangered", INV-D additive keys, INV-G, INV-I) -->
<!-- Source: Variant A (Proposal A), Section 2 item 8 and Debate (round2-advocate-A.md section 3 N6) - merged per Change 3 (INV-A and INV-L) -->
INV-A..INV-N are those of synth-06 6.12.0 (`synthesis/synth-06-conflict-log.md:54-67`). The conflict row lists INV-C and INV-I (HIGH) and INV-G (MEDIUM).

| Invariant | The policy (cut of the location fields, itemise, re-ask, refusal on PASS-by-loss) | Claim-only raise (owner lever, section 3.5) |
|---|---|---|
| INV-A contract 1.8.0 names and the `merge_method` pair, byte-identical | Kept for the contract names. No change to `contract.py` (it holds no limit constant, section 4.1) or to any reflect field name. `findings_block_compliance_rate` keeps its definition and is read from `first_pass_state`. The listings (`cluster_cmd.py:155-163`, `verify_cmd.py:136-138`) gain the additive keys `first_pass_state` and `repairs`; they do not emit `dropped`. | Kept for names. Brief text in `reviewer-spec.md` changes (a skill file, not the contract). |
| INV-B `derive_verdict` map, exit codes 0/10/11/2, the 36-test matrix | Kept. Nothing in `derive_verdict` or the reflect profile is touched; the `dropped_blocking` refusal lives in the v1 merge. | Kept. |
| INV-C findings-v1 line grammar and `review merge` unchanged; unknown keys accepted | Partly endangered for the cut. The validators are unchanged and `repair` is off at the parser by default, so the direct-parser pins stay literal; every line valid today passes through the step unchanged (the no-op property, section 6.2). What changes is `review merge` output for inputs that were dropped before: a consumer that relied on the drop would see a change, and none was found in `tests/review`. `errors` keeps its shape, unknown keys stay accepted, and `merge` keeps exit 0 except C-03's exit 12. | Endangered as worded: a widening of the claim limit. No line valid today becomes invalid. Pin rewrites: 2 assertion sites for a claim-only raise (`test_review_findings.py:117`; `test_review_findings_v2.py:241`), 3 with `card_convert.py` (`test_review_card_convert.py:500`); the quote pin (`test_review_findings_v2.py:200`) only if the quote limit is also raised. |
| INV-D `review-ledger/1`, the `ledger` group, exit 0/10/11, `merge` exit 0 | Kept with additive keys: `repairs`, `dropped`, `first_pass_state` and `repaired` (a `repaired` and a `dropped` object per reviewer entry) and an acknowledgement option on `merge` (owner and reason). Older readers ignore the keys (`ledger.load` checks the schema string alone, as the C-03 merged text records). Not closed here: the entry carries no policy tag (Round 2.5 INV-004, section 10). | Kept. |
| INV-E `pr_submit` types and FSM | Untouched. | Untouched. |
| INV-F installed-path rule | Endangered only by how the brief generator and the re-ask text are delivered: both must land as installed text, never as an instruction to read `src/superclaude/...`. This policy requires that. | Same. |
| INV-G reviewers mutually blind and mechanically read-only | Kept on the Agent path and the swarm path: the re-ask prompt holds only that reviewer's own block and its own errors and grants no new tool (T-B5). `--resume` is an optimisation only; the headless `claude -p --resume` path, where session persistence lets a reviewer read peer transcripts (E2 design-review finding 7, section 4.5), is not used until isolation exists, and the stateless prompt does not need it. | Kept. |
| INV-H telemetry carries no document text | Kept by construction: `repairs` and `dropped` entries hold ids, rule names, lengths, a hash and a blocking state, never text. This is still a convention (research/15:48-56 per the invariant table). | Kept. |
| INV-I fail-closed: a review that did not happen never certifies PASS | Strengthened at one point: a PASS that rests on dropped blocking-or-unknown lines is refused. It does not close the partial-panel case, which is C-03's. Under Alternative A of section 3.3 `block_ok` becomes True for a reviewer whose only fault was length, and the eligibility rule is as stated in section 3.3 (C-002 unresolved). Not closed here: Round 2.5 INV-001, INV-017 and INV-023 (section 10). | Kept. |
| INV-J repo review rule S1-S5 and the pinned caps | Kept. A re-ask is a second prompt to the same reviewer inside one round, not a review and not a fix cycle. Whether `test_f` (no other numbers in primitives) objects to "one re-ask" in a new primitive text is [UNVERIFIED]; `SKILL.md:343` already says "one bounded re-ask". | Kept. |
| INV-K sync and layout gates | Endangered by the brief generator: it edits skill and prompt sources, so `make sync-dev`, `make verify-sync` and the reflect skill edit fence apply; the additive `SKILL.md:343` sentence (section 3.4) is a skill edit too. Which tests pin the text of `reviewer-spec.md:39` is [UNVERIFIED]. | Same. |
| INV-L shadow mode changes no verdict | Kept while shadow lasts: no verdict reads the listings (`repairs` and `first_pass_state` are emitted there; `dropped` goes to the notes only). The shadow-mode safety argument (debate point A-005) holds only while shadow lasts unless `first_pass_state` is carried (section 3.1). | Kept. |
| INV-M `reflect_status` enum and headless output directories | Untouched. | Untouched. |
| INV-N plugin mirror parity | Endangered when the loop prompt text changes (the limits sentence); the plugin copies move with it. [UNVERIFIED] which parity pins cover `document_review_loop_prompts.md`. | Same. |

Repository rules: no `.claude/` path is touched by this position; the generator output belongs in `src/superclaude/`; the fork-only PR rule is out of scope.

## 6. The test or measurement that would show the policy right or wrong

### 6.1 Measurements

<!-- Source: Base (original, modified) - the base measurement rows M1, M2 and M3 are modified (M1: fire counts "3 without the cut, 0 with it"; M2: re-ask on the residual lines only; M3: the claim-only admission curve) per Change 10; the opening sentence is original -->
<!-- Source: Variant A (Proposal A), Section 5 (M1-M4) and Debate (round2-advocate-A.md section 6 bullet 10; round2-advocate-B.md section 6 bullet 9) - merged per Change 10 (the cut replay folded into M1, the re-ask on the residual folded into M2, the cost-side re-merge added as M4, the two-judge claim test added as M5) -->
Rules for each measurement are written to a file before the first run, as C-02's replay does; the owner may change the numbers before then.

| Id | What | Shows the policy right | Shows the policy wrong |
|---|---|---|---|
| M1 | Conservation, fire-set and cut replay, no model call. Run both parsers with the classifier and the cut over every reviewer report of the 264 audit-D merges and over the 1,215-report corpus (two frozen populations). Report: conservation per report, lines passing the parser, fields locating uniquely over fields whose full anchor locates, `refs_changed`, the residual by rule, and the fire count of the `dropped_blocking` refusal. | For every report, non-blank lines equal kept plus priors plus dropped; with the cut off the dropped rows reproduce 56/18/14/3/1 by rule and 49 with `blocking_state` true; the refusal fires on exactly the 3 merges of 4.2 without the cut and on none with it. It also explains the 17-19 lines audit-D could not (research/08:79, 111 against 92). | Conservation fails for any report, or the refusal fires where a blocking row survived, or misses one of the 3 without the cut, or K1 fails (section 6.3). |
| M2 | Re-ask recovery on the residual lines only, the missing Spike 5. For the lines that remain invalid after the cut (bad severity, bad refs and any new E1 residuals), send each reviewer its own block and the parser's per-line errors once as the stateless prompt, per transport (the Agent path, and the gateway path where `--resume` exists). Score per line: valid on re-parse; anchor verbatim in the candidate; claim meaning kept (blind judge); whether the model repeats the same violation; whether the re-ask changes a line that was not listed. | One re-ask recovers the residual lines at a share that meets K4 and changes no unlisted line. | K4 fails: recovery under 60 percent over at least 20 residual lines, or any re-ask changes an unlisted line. |
| M3 | The claim-only admission curve and the incidence levers. First-pass compliance over a set of runs with the generated-brief change alone, then with a claim-only raise. Extend the P273 claim curve (12 claim-dependent lines: 12 of 12 at 450, 11 of 12 at 400) to the 264 merges and to later runs (lines admitted, blocking lines admitted, row text length in the merged report). | The brief change alone lowers the over-limit rate (the E1 notes and memory say claims over 300 were the repeat cause and the brief did not state the cap); a claim-only raise admits the claim-dependent lines at the stated curve. | The brief change does nothing to the claim rate, or the claim-only raise does not admit the claim-dependent lines at the stated curve. |
| M4 | Cost-side re-merge (the only measurement in either proposal that can show the policy harmful; debate point U-003). Re-merge the merges of both frozen populations with repair on and off. Report the PASS-to-FAIL flips (first run on P273: 3, exactly the three wrong PASSes), the added blocking rows (first run: 16) and whether a blind judge rates each added blocking row true or false. | The added blocking rows are judged false no more than K3 allows. | K3 fails (section 6.3). |
| M5 | Two-judge claim-meaning test (K2). On the 34 claims of section 4.3 (22 blocking), two blind judges mark whether a cut to 297 characters plus `...` loses a decision-relevant clause. | At most 20 percent of blocking claims lose a decision-relevant clause (both judges). | More than 20 percent do (both judges): in Variant A's form claims move to re-ask-first; in Variant B's form the claim cut is not allowed (section 3.6). |

### 6.2 Tests

<!-- Source: Base (original, modified) - T-B1 to T-B5 kept; T-B2, T-B3 and T-B4 are modified (default `repair=False`; `dropped_blocking`; byte-equal except the additive keys) per Change 10 -->
<!-- Source: Variant A (Proposal A), Section 5 (unit tests) and Debate (round2-advocate-A.md section 6 bullet 10; round2-advocate-B.md section 6 bullet 9) - merged per Change 10 (T-A1 to T-A6) -->
| Id | What | Holds | Fails |
|---|---|---|---|
| T-B1 | Property test on both parsers: for generated blocks, non-blank lines equal findings plus priors plus dropped. | holds | any counterexample |
| T-B2 | All existing pins pass unmodified with the default `repair=False` (`test_review_findings.py:113,117` among them). | holds | any pin fails |
| T-B3 | Merge matrix: one reviewer with only dropped blocking lines (today's refusal at `ledger.py:150-157` stays); two reviewers, one with a dropped blocking line and one with an empty valid block (refusal `dropped_blocking`); a surviving blocking row (no refusal, ids printed); only `blocking: false` drops (no refusal, no re-ask); acknowledged drops (merge proceeds, ids listed); panels of 1 to 5. | as listed | any other outcome |
| T-B4 | `review cluster` output byte-equal on the existing v2 fixtures with the classifier and the cut in place, except for the additive keys `first_pass_state` and `repairs` (the C-01 INV-020 differential that C-01 found missing). | equal | any other difference |
| T-B5 | The re-ask message contains no text from another reviewer's report and grants no tool. | holds | any leak |
| T-A1 | No-op property: for every valid line in the existing fixtures (`tests/review/test_review_findings.py`, `test_review_findings_v2.py`), `repair_line(obj) == (obj, [])`. | holds | any valid line changes |
| T-A2 | Boundaries 200/201 and 300/301 with and without repair (the 300/301 claim case applies with the claim switch of section 3.6 on): 201 and 301 fail with `repair=False` and, where the field is cut, pass with `repair=True` with one `repairs` item each; 200 and 300 pass both ways. A raw 205-character anchor that flattens to 190 is not repaired, because the limit is measured after `flat()` (`findings.py:79-87`). | as listed | any other outcome |
| T-A3 | Idempotence and non-invention: `repair_line(repair_line(x)) == repair_line(x)`; a citation-only line gets no `anchor`; `quote` is cut only when present; a line that is still invalid after repair is reported in `dropped`, not changed further. | holds | any counterexample |
| T-A4 | Call sites: every production call site passes `repair` explicitly, and the default stays `False`. | holds | a call site omits it, or the default changes |
| T-A5 | Differential first-pass: `first_pass_state` against a `repair=False` parse shows zero mismatches, and `findings_block_compliance_rate` read from it equals the rate from a `repair=False` parse. | zero mismatches | any mismatch |
| T-A6 | The v2 loss unit: one block with one over-limit location field and one valid line is `complete` with `repairs`, and both findings reach `cluster`; a claim fault stays `invalid` unless the claim switch of section 3.6 is on. | as listed | any other outcome |

### 6.3 Kill lines

<!-- Source: Debate (round2-advocate-A.md section 6 bullet 11; round2-advocate-B.md section 6 bullet 10) - merged per Change 10 (kill lines K1-K5 as in both advocates' final bullets) -->
Written to a file before the first run; the owner may change the numbers.

- K1: if fewer than 90 percent of the over-limit location fields that occur verbatim in the document keep a unique same-span prefix (75 percent on a code or multi-line corpus once one exists), that field class is demoted to itemise plus re-ask. K1 is computed over fields that occur verbatim in the document: on P273 the blocking fields are 34 of 37 (91.9 percent) over all fields, and the 3 misses do not occur verbatim, so the unrestricted figure would test reviewer fidelity and not the cut [DEBATE-ESTABLISHED: `round2-advocate-B.md` section 2]; over the verbatim fields it is 70 of 70.
- K2: the claim-meaning test, in both forms (section 3.6).
- K3: the cut is wrong if the added blocking rows are judged false more than 10 percentage points above the base rate of kept blocking rows, or if any merge flips PASS to FAIL through a false repaired row the cap of 3 reviews cannot clear.
- K4: the re-ask half is wrong if recovery is under 60 percent over at least 20 residual lines, or if any re-ask changes a line it was not asked about.
- K5: the refusal is wrong if it fires on more than 5 merges of the frozen population after the cut (the advocates' texts say 5 of 264 and 5 of 273), or if any refusal has no re-ask or acknowledgement exit.

## 7. Effect on future PR code review and on the rf-qa replacement

<!-- Source: Base (original, modified) - PR bullets 1 and 2 and the rf-qa bullet 1 are modified (stateless re-ask; quote prefix; the base's quote wording replaced; the base's over-limit-quote-as-re-ask design removed because the quote is now cut) per Change 16; the other bullets are original -->
<!-- Source: Variant A (Proposal A), Section 6 - merged per Change 16 (quote prefix, per-profile limit, code corpus required) -->
PR code review.
- pr-submit must run in the main session (research/13:183, P8 [CODE-VERIFIED as research text]), so a headless `--resume` re-ask is not the PR path; the re-ask there is the stateless in-session form (a second prompt carrying the original brief, the reviewer's own block and the parser's per-line errors), or an in-session continuation of an Agent reviewer [UNVERIFIED for this module].
- The limit that bites in PR review is the optional citation `quote` (12..200) on code lines, which are not whitespace-flat and often exceed 200 characters (research/scope/03:534 [CODE-VERIFIED as research text]; luna, ember and wonder lost 30, 33 and 14 findings in E2). The 4.3 numbers come from tasklist documents and do not transfer. A `quote` prefix passes the `verify_cmd.py:68-72` substring test, so the quote is cut like the other location fields; the quote limit is a per-profile parameter (CO-9, decided: spec-shaped hard-codings become module extension points); the re-ask is the stateless in-session form. Neither variant measured PR code, so a code corpus is required before a PR module relies on the cut (K1 carries its 75 percent line for code, section 6.3).
- A dropped record with a blocking state maps onto the PR flow's "no file:line, no finding" rule (research/13:103) without any change to `Finding`, `Severity` or the FSM, because the record stays inside the review package and the adapter (C-10) sees only kept findings.

rf-qa replacement (first step at the `/task` gate).
- The reviewers are mechanically read-only (INV-G); the re-ask is a stateless second prompt that grants nothing, so the "lens agents on `bypassPermissions`" question in C-11 is not made worse.
- rf-qa has no behavioural oracle (C-11 row). The `dropped` record gives a replay oracle its first cheap check, conservation of lines, and the `dropped_blocking` refusal gives the confidence gate a rule for the case where the evidence for a block was lost.
- A ledger-based rf-qa replacement cannot take citation-only findings until `annotate` and ledger rows stop requiring `anchor` (synth-05 6.2 status text); that is C-01's deferral and is independent of this slot.

## 8. The strongest objections and the answers

<!-- Source: Base (original, modified) - the base objection and its answers 1 to 4 are replaced by the merged pair below; base answer 5 is kept with its numbers corrected; base answer 1 is withdrawn and replaced by the corrected statement (Changes 9 and 14) -->
<!-- Source: Variant A (Proposal A), Section 7 (objection and answers 1, 2 and 3) - merged per Change 14 (answer to Objection 1, for the location fields) -->
<!-- Source: Debate (round2-advocate-B.md section 4 row C-012 and section 1.1 W1; round2-advocate-A.md section 1.1 W3) - merged per Change 14 -->
Two objections remain open in the debate's own record after the merge. Each is stated in its strongest form, then answered.

**Objection 1: provenance and the principle (C-012).** A repaired line is not the reviewer's finding. The stored finding is not a byte copy of a line in the hashed report; `SKILL.md:343` says the orchestrator "never edits, remaps or normalizes a reviewer's findings itself"; a cut anchor can bind to an earlier occurrence; and the recovery figure is a derivation from a count of reasons, not a measurement.

Answer 1 (kept from Proposal A's section 7 for the location fields):
1. The report file is never edited and its `report_sha256` is recorded per reviewer (`ledger.py:146`). The repaired object is a derived copy that carries `original_sha256` and a per-field record of the original and kept lengths. `SKILL.md:343` is step 4 of the reflect shadow procedure, addressed to "the orchestrator", and is pinned; its sentences stay byte-identical and one sentence is added (section 3.4). Whether package code counts as "the orchestrator" is an owner reading, and the fallback if it does is stated in section 3.4.
2. Dropping is also an edit, and a larger one: the drop removed 49 blocking lines in audit-D and flipped 3 verdicts to PASS (research/02:100-101).
3. The evidence for the location fields: 70 of 70 and 89 of 89 prefixes locate once with the same first span, and `refs_norm` changed on 0 of 125 lines (sections 4.2 and 4.3). It covers single-line tasklist rows only, and a prefix that matches more than one place is open (Round 2.5 INV-017, section 10).
4. Where the objection stays: for a claim cut. The stored claim would end in `...` and so would not be a substring of the reported line, and what the cut changes in meaning is unmeasured (K2, section 3.6). Variant A accepts that the stored member is a recorded derived value; Variant B's advocate would allow a claim cut only if K2 passes. Variant B's advocate moved C-012 to Variant 1 for the cut anchor and kept the byte-copy objection only for the claim cut; the two final positions differ (section 10).

**Objection 2: the eligibility cost (C-002).** Under the bare parser verdict a repaired block votes to clear and counts toward quorum although the reviewer broke a limit (Variant B's Round 1 weakness 3; Variant A's W3 answer). Under a derived eligibility some length-fault runs stay ineligible and cost clearing power and quorum.

Answer 2: the cost is now quantified on P273 (section 4.2): today's bare `ok` puts 10 of 273 merges below the C-03 floor, a tolerant eligibility 5, the cut 0, and an anchors-only cut 2; Variant A counts at least 7 of 264 audit-D merges (three-reviewer panels only). The INV-I refusal (`ledger.py:150-157`) is untouched. Under Alternative A of section 3.3 `ok` after the cut is still the real parser verdict on the repaired lines and any residual fault leaves it False; Alternative B does not use the bare bit at all. Which applies is unresolved (section 3.3 and section 10).

**Other answers.**
3. Stall exposure. The base's earlier answer on stall exposure is withdrawn. On P273, 79 of 855 reviewer-runs have `ok` False and 10 of 273 merges fall below the C-03 floor under today's `ok` (section 4.2). The refusal itself fires on 3 of 264 merges without the cut and on 0 with it (section 3.3).
4. A transport that cannot re-ask degrades to itemise plus the refusal on PASS-by-loss. That is strictly better than today, which drops silently and stored three wrong PASSes. The acknowledgement option removes the deadlock.
5. What the policy does not have is a measured recovery rate for the re-ask on gateway models: that is M2, and until it is run the recovery claim rests on four confirmed re-asks of five in E1 (Agent path, one length cause, n small) and the E2 S2 resume spike. If long-anchor models repeat the violation after being told the limit, the re-ask recovers little for the residual lines; K4 (section 6.3) states when the re-ask half is wrong.

## 9. Open facts this proposal does not settle

<!-- Source: Base (original, modified) - the base list is kept; items 2, 3, 6 and 8 are modified for the merged policy and the last item is appended per Change 15 -->
- Re-ask recovery on gateway ids and on the PR path ([UNVERIFIED]; M2).
- Whether a claim cut at 300 changes the finding's meaning (judge not run; 4.3; M5 and K2).
- Whether a 200-character prefix stays unique for multi-line anchors and code hunks, and whether a `quote` prefix locates (4.3 and 4.2 cover single-line tasklist rows only).
- The 17 to 19 dropped lines audit-D could not explain (research/08:79 [UNVERIFIED cause]); M1 would classify them.
- The A3 "typo fixed same run" and who made the fix (`...comboA-r3/panel/notes.md:10`).
- The exact form of C-03's refusal object and of the acknowledgement option; the policy needs both and does not define either beyond what is stated in 3.3.
- Which static tests pin the text of the briefs and the loop prompt (INV-K, INV-N).
- Whether the owner accepts a claim-only raise of the limit, which widens the findings-v1 grammar (an owner decision, as the slot row says; 3.5).
- The unresolved conflicts, the owner decisions and the 20 UNADDRESSED Round 2.5 findings of section 10 are open facts too; this document does not close them.

## 10. Open invariants and unresolved conflicts

<!-- Source: Debate (the Convergence Assessment of debate-transcript.md as recorded in refactor-plan.md Change 15; invariant-probe.md; round2.5-fault-finder-raw.md) - merged per Change 15 (new section; transparency only) -->
The debate ended with convergence BLOCKED_BY_INVARIANTS at 85.7 percent (24 of 28 points): the Round 2.5 probe left 4 HIGH findings UNADDRESSED (INV-001, INV-017, INV-018, INV-023), together with 12 MEDIUM and 4 LOW. Standard depth has no Round 3, so none was resolved in the debate. This section lists them so that they travel with the merged text. Nothing in this section is closed by this document, and the document adds no fix for any of them. The probe ids INV-001 to INV-026 are the Round 2.5 numbering and are separate from the C-01 ids of section 2 and from INV-A to INV-N of section 5; `adversarial/round2.5-fault-finder-raw.md` is authoritative for the evidence behind each.

### 10.1 Unresolved conflicts: both positions

Four debate points ended with the advocates' final positions apart. The merged text states both positions and does not choose.

- C-001 (claim part) and C-009: whether the claim is cut. Final positions: on C-001 Variant A's advocate says Variant 1 (72) and Variant B's says Hybrid (76), by field; on C-009 Variant A's advocate says Hybrid (62) and Variant B's says Variant 2 (76).
  - Position A: cut the claim to 297 characters plus `...` with a marker, a "shortened from N" row note and `original_sha256`, kept unless K2 (in Variant A's form) fails.
  - Position B: no claim cut by default, because no verdict or floor outcome on P273 needs it, a claim limit of 450 reproduces cut-all, and the meaning of a cut claim is unmeasured; a claim cut only if K2 (in Variant B's form) passes.
  - The evidence and both forms of K2 are in section 3.6. Not settled.
- C-002: which eligibility rule decides clearing and the quorum floor. Final positions: Variant A's advocate Variant 1 (80), Variant B's advocate Hybrid (74).
  - Position A: `ok` and `complete` are the parser's verdict on the repaired lines, so a length-only block is `ok`, any residual fault is False, and C-03 may count only `repaired == 0` blocks for its floor as a recorded parameter, default off.
  - Position B: a derived eligibility: a reviewer counts iff it has no block-level fault, no non-length drop on a `true` or `unknown` line, and no unresolved dropped line with `blocking_state` `true` or `unknown`; dropped `blocking: false` lines do not disqualify; no `repaired == 0` knob.
  - Both quantify the same cost of the bare `ok` (10 of 273 merges below the floor on P273; at least 7 of 264 on audit-D). The alternatives are stated in section 3.3. Not settled.
- C-012: the provenance of a stored member that is not a byte copy of a line in the hashed report. Final positions: Variant A's advocate Hybrid (70), Variant B's advocate Variant 1 (68).
  - Position A: a derived copy with `original_sha256` of the flattened field plus the existing `report_sha256`; the member is accepted as not a byte copy.
  - Position B: for a cut anchor the stored value is a flattened-form substring of the reported line, so `original_sha256` and `report_sha256` keep provenance; the byte-copy objection applies to a claim cut, which Position B leaves uncut by default.
  - The two positions agree for the location fields and differ for a claim cut (section 8, Answer 1 point 4). Not settled for the claim cut.

### 10.2 Owner decisions the text depends on

- The default for the claim: cut or not (section 3.6), and the numbers of K2.
- Whether package code is "the orchestrator" in `SKILL.md:343` (section 3.4); if it is, the v2 call sites stay at `repair=False` and the v1 `merge` keeps the cut.
- Whether to raise the claim limit to 450 (section 3.5; a widening of the findings-v1 grammar, INV-C).
- The numbers of the kill lines K1 to K5, which the owner may change before the first run (section 6.3).

### 10.3 Round 2.5 findings left UNADDRESSED

20 findings: 4 HIGH, 12 MEDIUM, 4 LOW. One sentence each, taken from `invariant-probe.md` and `round2.5-fault-finder-raw.md`. Not closed by this document.

| ID | Severity | Category | What is open |
|---|---|---|---|
| INV-001 | HIGH | state_variables | The dropped-blocking refusal sees only the current round's drops, so a blocking line lost in a FAIL round can be forgotten when a later round passes, because the ledger keeps no cross-round list of unresolved dropped lines. |
| INV-017 | HIGH | interaction_effects | A 200-character prefix can locate at more than one place while the full anchor locates once; `annotate` takes the first and `anchor_ambiguous` is read nowhere in `src`, so a new blocking defect can be matched to a deferred row and pass with nothing dropped (shown by the probe on a synthetic two-row document). |
| INV-018 | HIGH | interaction_effects | In reflect, `cluster_cmd` and `verify_cmd` run at step 6 after the `collected` commit of steps 3 and 4, so the re-ask and the attempt-2 record cannot be driven from the first-pass carrier as written and the compliance rate stays the orchestrator's own count. |
| INV-023 | HIGH | sufficiency_challenge | The cut plus itemise plus refusal does not by itself close the PASS-by-loss defect and the v2 loss unit: a lost blocking line forgotten across rounds (INV-001), a cut line absorbed by a deferred or resolved row (INV-017) and a truncated block with no line to drop (INV-025) each falsify it alone. |
| INV-002 | MEDIUM | state_variables | The manifest `completion` value is a third carrier of first-pass state that the debate text does not name, and `reviewers_complete` and `valid_blocks` can disagree on the same card unless one value is chosen and tested. |
| INV-003 | MEDIUM | state_variables | A refused v1 merge writes nothing, so after a refusal-driven re-ask succeeds, attempt 1's report, its `repairs` and `dropped` lists and the re-ask itself are nowhere in the ledger, and K4 and K5 cannot be measured on live ledgers. |
| INV-005 | MEDIUM | guard_conditions | `blocking_state` taken from the line's own `blocking` field is not a sound proxy for "this lost line would have blocked": both checkers accept CRITICAL with `blocking: false`, which would get `blocking_state` false and no refusal. |
| INV-006 | MEDIUM | guard_conditions | The acknowledgement is not bound to the dropped item ids or hashes, and the coordinator agent that is told to re-run on exit 12 can pass its own owner and reason. |
| INV-007 | MEDIUM | guard_conditions | `blocking_state` is defined only for finding lines, so a dropped `prior` line (a lost veto) has no stated `blocking_state` and may leave a reviewer eligible under Alternative B. |
| INV-008 | MEDIUM | guard_conditions | Both checkers return the first fault only, so a line with two faults is fixed in one respect and dropped again after the single re-ask, and the itemised `rule` and the "residual by rule" count undercount. |
| INV-010 | MEDIUM | count_divergence | A cut can invent a reference token (the probe cut `FR-12` to `FR-1`) and change `refs_norm`, `fp` and `same_defect`; recording `refs_changed` does not prevent it, and the 0 of 125 measure did not cover claims. |
| INV-016 | MEDIUM | collection_boundaries | A rescued line whose prefix does not locate becomes a kept row with `anchor_status: missing` and no span, which no fix can touch, so the spec loop can spend its reviews on an unfixable row (C-01 INV-015 is the same defect). |
| INV-019 | MEDIUM | interaction_effects | The unchanged Normalize text and the additive sentence use "invalid" for two different states (the unrepaired first parse and the re-ask trigger on the repaired state), and an orchestrator that follows the unchanged text re-asks every length-faulted block. |
| INV-024 | MEDIUM | sufficiency_challenge | The cut removes the v2 loss unit only for the length share: any non-length fault still discards all of a reviewer's findings, so recovery rests on the single re-ask, which has no recorded success rate on gateway models. |
| INV-025 | MEDIUM | sufficiency_challenge | A truncated block loses its tail with no line to itemise, so nothing can trigger the refusal for the lost findings; truncation stays outside the guard. |
| INV-026 | MEDIUM | sufficiency_challenge | After the cut the refusal fires on 0 of 264 in the study data, so K5 passes trivially and no measurement exercises the code path or the residual classes it exists for. |
| INV-004 | LOW | state_variables | Additive keys do not tell a later reader which meaning of `block_ok` applies, because the entries carry no parser or policy version and `ledger.load` checks only the schema string; shadow telemetry has no policy tag either. |
| INV-011 | LOW | count_divergence | `original_chars`, `kept_chars` and `repaired_lines_rate` have no single unit (stored length against retained source for a claim cut; per field against per line; a cut on a line that is later dropped inflates `repairs`). |
| INV-020 | LOW | interaction_effects | Two refusals can occur in sequence (the quorum refusal, then `dropped_blocking`, both exit 12), each recording nothing, so the loop prompt must branch on the `refusal` key and not on the exit code alone. |
| INV-022 | LOW | interaction_effects | `card_convert.py:226` validates through `check_finding` and has its own claim cut, so a claim cut adopted in the repair would leave two implementations of the same arithmetic. |

The probe's 6 ADDRESSED findings (INV-009, INV-012, INV-013, INV-014, INV-015, INV-021) were handled in the debate text and are not restated here.

Status: Complete
