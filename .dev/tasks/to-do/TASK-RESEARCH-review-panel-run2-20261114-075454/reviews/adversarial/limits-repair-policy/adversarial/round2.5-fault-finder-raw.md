# Round 2.5 invariant probe: slot C-06 limits-repair-policy (independent fault-finder)

Role: independent fault-finder, not an advocate. Target: the emerging consensus of `round2-advocate-A.md` and `round2-advocate-B.md` (the "Proposed resolution text" bullets 1-12 of each; below "bullet N" means that numbered bullet in section 6 of both files, which converge, and "A bullet" / "B bullet" where they differ).
Code state: HEAD 50d4d2b9d, branch `ironbelly/shadow-runs`, read-only. No file was written except this one.
Tags: [READ] I read the file or lines this session; [RAN] I executed a read-only, in-memory check this session (`uv run --offline --no-sync python -B` with `PYTHONPATH=src`, `PYTHONDONTWRITEBYTECODE=1`, nothing written to disk); [DOC] taken from an adjudicated result or an advocate file whose source I did not re-open.
Inputs read: round1-advocate-A/B, round2-advocate-A/B, diff-analysis, the C-01, C-02 and C-03 ADJUDICATION-RESULT files, the C-03 merged-output (sections around lines 28-40, 74-87), the C-01 merged text (grep), and the code and tests named in the brief. `branch-trace.md` does not exist for this task; the inline source enumeration of gates is INV-023.

Format per entry: ID, CATEGORY, ASSUMPTION, STATUS, SEVERITY, EVIDENCE (and a short consequence or failing input where verified).

---

## state_variables

### INV-001
- CATEGORY: state_variables
- ASSUMPTION: the dropped-blocking refusal (bullet 8) makes a PASS that rests on a lost blocking-or-unknown line impossible. It is stated only for "the derived verdict would be PASS and an unacknowledged residual dropped line has `blocking_state` true or unknown"; the scope of "dropped line" (this round or every round of the ledger) is not stated, and the recorded unit is a per-round reviewer entry.
- STATUS: UNADDRESSED
- SEVERITY: HIGH
- EVIDENCE: Concrete failing input (a stated sequence, derived from code, not executed end to end). Round 1, three reviewers: reviewer A writes a valid blocking finding F1 and a blocking line F2 with `"severity": "HIGH"` (a residual fault the cut cannot reach, `findings.py:96-97`; `blocking_state` true). The merge FAILs on L1, so the rule "no refusal when a blocking row survives" (bullet 8) fires nothing; F2 is only itemised in round 1's reviewer entry. The Reviser fixes L1. Round 2 is the standard one-reviewer re-review (C-02 E2, all 8 packaged templates `apply_to: ["first"]` [DOC]); that reviewer writes no finding and `prior L1 resolved`. `merge_round` computes `verdict = "FAIL" if brief else "PASS"` from rows only (`ledger.py:273-275`, `_brief_ids` `:99-104`); the round-2 entry holds no dropped line, so the refusal has nothing to test. PASS, with F2's defect never re-found by construction (a second look at the whole document by one reviewer is not a guarantee). The ledger keeps no cross-round list of unresolved dropped lines and no rule says a later PASS must consult earlier rounds' `dropped` items. Round 1's `dropped` item can only be resolved by a matching row, and a dropped line has no row (`ledger.py:135-138` builds rows only from parsed findings). Sources: `round2-advocate-A.md` section 6 bullet 8; `round2-advocate-B.md` section 6 bullet 7; `ledger.py:99-104, 254-258, 273-275` [READ]; `merge_cmd.py:99-118` [READ].
- Needed: persist `dropped` items with `blocking_state` in each round entry, evaluate the refusal over every round's unacknowledged true/unknown items, and define when an item is closed (re-found as a row, re-asked and replaced, or acknowledged by id).

### INV-002
- CATEGORY: state_variables
- ASSUMPTION: carrying `first_pass_state` beside the repaired `state` keeps both the compliance metric and the manifest honest (bullet 7; A N6).
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: the manifest has a third carrier the consensus does not name. `record_attempt` stores a caller-supplied `completion` (`manifest.py:331-347`, values `complete, truncated, invalid, failed, timed_out` at `:52`), `_recount` sets `reviewers_complete` from the latest `collected` attempt equal to `complete` (`manifest.py:269-274`), and the exit script counts a "2-of-3 shortfall" when `reviewers_resolved == 3 and reviewers_complete == 2` (`reflect_shadow_exit.py:244-245`, aggregate at `:349`) [READ]. Nobody says which completion the orchestrator records for a block that the cut rescued: `complete` (the manifest then hides every first-pass length fault and the shortfall count falls) or `invalid` (the manifest then says the reviewer was incomplete although `cluster` treats the block as valid, `cluster.py:219-221`, so `reviewers_complete` and `valid_blocks` disagree on the same card). One value must be chosen and tested; today there are three counters (`first_pass_state`, repaired `state`, manifest `completion`) and the consensus defines two.

### INV-003
- CATEGORY: state_variables
- ASSUMPTION: a refusal-driven re-ask in v1 (bullets 3-5) is measurable and its record "is the replacement report and its `report_sha256` in that round's entry".
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: a refused merge writes nothing by construction (`merge_cmd.py:109-116`: `led.save` is last; `ledger.py:114-118` refuses a second merge of the same round) [READ]. When the re-ask succeeds, the replacement text is what `merge_round` parses and hashes (`ledger.py:128, 146`), so attempt 1's report, its `repairs`, its `dropped` list and the fact that a re-ask happened are nowhere in the ledger. K4 (re-ask recovery over at least 20 residual lines), K5 (refusal fire rate), M3 and `dropped_lines_rate` in v1 cannot be computed from production ledgers; only the offline re-merge (M2) exists. Round2-A N5 concedes "a refusal leaves no stored trace" and C-03 INV-001 (MEDIUM, unaddressed [DOC]) is the same gap. The kill lines K4 and K5 are therefore falsifiable only on frozen corpora, never in live use.

### INV-004
- CATEGORY: state_variables
- ASSUMPTION: additive keys (`repaired`, `dropped`, `repairs`, `first_pass_state`) are enough for later readers to interpret old and new rounds.
- STATUS: UNADDRESSED
- SEVERITY: LOW
- EVIDENCE: `block_ok` changes meaning with this policy (a length-only block was False, becomes True), and `entries[]` in `merge_round` carries no parser or policy version (`ledger.py:141-149` [READ]); `ledger.load` checks only the schema string (`ledger.py:47-48` [READ]; C-03 merged text line 33 says the same [DOC]). A ledger whose round 1 predates the change and round 2 follows it mixes both meanings, and an absent `repaired` key reads as "unknown", not 0. The same applies to shadow telemetry: `clusters.json` content, `cluster_agreement` and `calibrated_findings n/m` change when previously dropped lines now cluster (C-01 INV-020 [DOC]), and `reflect_shadow_exit.py:353-362` averages compliance across runs with no policy tag. Record a `policy` key (limits and repair on/off) next to `block_ok` and in telemetry.

---

## guard_conditions

### INV-005
- CATEGORY: guard_conditions
- ASSUMPTION: `blocking_state` (true, false, unknown) taken from the line's own `blocking` field is a sound proxy for "this lost line would have blocked".
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: [RAN] `_check_finding` and `check_finding` both accept `{"severity":"CRITICAL","blocking":false,...}` (printed `None, None`); [READ] `findings.py:96-101` rejects only MINOR with `blocking: true`. C-02 adopted a CRITICAL floor in `merge_round` precisely because typed `blocking` is untrusted [DOC: ADJUDICATION C-004]. A dropped line that is CRITICAL with `blocking: false` gets `blocking_state` false under bullet 2, is not refused (bullet 8 tests true/unknown) and, under B's derived eligibility (B bullet 5, "dropped `blocking: false` lines do not disqualify"), the reviewer still counts for clearing and the floor. In the reflect lens the opposite mislabel (MAJOR with `blocking: false`) is itself a rule fault that drops the line (`findings_v2.py:161-162` [RAN: message printed]), and again `blocking_state` is false. The state must be derived with the severity floor applied: true when severity is CRITICAL or MAJOR-in-reflect regardless of the typed flag, unknown when the line cannot be read.

### INV-006
- CATEGORY: guard_conditions
- ASSUMPTION: the owner-and-reason acknowledgement lets a human lift the refusal "so it cannot deadlock" (bullet 8) without making the guard decorative.
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: the option is specified as owner plus reason on `merge`, "mirrors C-02 `defer`" (A N5; bullet 8). C-02 left open that `--owner ""` satisfies "required" (C-02 INV-008, MEDIUM [DOC: ADJUDICATION table]). The spec loop is run by a coordinator agent that is told by exit 12 to "re-run the review" (C-03 merged text line 77 [READ]); after one failed re-ask the same agent can pass its own owner and reason. Nothing binds the acknowledgement to the dropped item ids or line hashes (bullet 2 records `original_sha256` per item, so binding is possible), so one acknowledgement can lift lines the acknowledger never saw, and a `merge` invocation that carries the flag from the start turns the guard off for the run. K5's "any refusal lacks a re-ask or acknowledgement exit" tests that an exit exists, not that it is used by a person.

### INV-007
- CATEGORY: guard_conditions
- ASSUMPTION: the conservation property and `blocking_state` "cover bad `prior` lines" (A section 4 U-009 row; B bullet 2).
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: a `prior` line has no `blocking` key; `blocking_state` is defined only for finding lines (bullet 2: bad JSON or non-boolean `blocking` is unknown). [READ] `findings.py:175-187`: a bad prior line sets `ok` False and is dropped before any finding check; a good one is appended to `priors` even if the block later fails. [RAN] `{"prior":"L2","status":"open "}` (trailing space in the status) gives `ok False`, no prior, one error. A dropped `prior open` is a lost veto (C-02 B2 and INV-009 [DOC]); under A's bare `ok` the reviewer becomes ineligible, under B's derived eligibility (no non-length drop on a true or unknown line) a malformed prior line may leave the reviewer eligible, because no `blocking_state` applies. The consensus must say what `blocking_state` a dropped prior line has (unknown, or a separate `prior` class) and whether it triggers the refusal or the re-ask.

### INV-008
- CATEGORY: guard_conditions
- ASSUMPTION: the first-fault ordering of the checks cannot hide a second fault from the re-ask or the itemised `rule`.
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: both checkers return the first fault only: v1 order `findings.py:90-121` (id, duplicate, severity, blocking, MINOR-blocking, category, anchor, anchor2, refs, claim); v2 `findings_v2.py:84-187` (claim at `:111` before refs, citations, anchor, anchor2, then lens, deviation, coverage_rows, confidence, channel) [READ]. [RAN] a line with a claim of 301 characters and `coverage_rows: ["R-9"]` outside the slice reports only the claim fault; with the claim at 300 it reports the coverage fault. Bullet 4 hands the reviewer "the parser's per-line errors", i.e. one message per line, and bullet 3 allows exactly one bounded re-ask. A line with two residual faults is therefore fixed in one respect and dropped again after the single re-ask; B's own E1 table says reviewer 2 "still had two bad citations" after its re-ask (diff-analysis X-002 [DOC]). Likewise the itemised `rule` records the first fault only, so M1's "residual by rule" undercounts. P273's all-fault replay found 4 of 90 lines with a non-length fault (round2-B N3 [DOC]); in v2 the population has 4 of 5 re-asks for non-length causes, so this is not marginal. Collect every fault per line (a list, not a first message) for both the record and the re-ask prompt.

### INV-009
- CATEGORY: guard_conditions
- ASSUMPTION: "the cut fires only on a field the unrepaired parse would reject, so the first-pass state is exact" (A N6; bullet 7) also holds for v2 where several faults coexist.
- STATUS: ADDRESSED
- SEVERITY: LOW
- EVIDENCE: derivation checked against `findings_v2.py:215-304` [READ]. The state precedence is `truncated` if the block is unclosed, else `invalid` if any error, else `complete` (`:299-303`), identical for repaired and unrepaired parses whenever any other fault remains; a cut line that is also dropped keeps `errors` non-empty so `state != complete` and the derivation returns `state` unchanged; a cut line with no other fault turns an `invalid` into `complete`, which is exactly the `repairs` non-empty case. The derivation is exact only if the repair trigger equals the check predicate: `len(flat(value)) > 200` for anchor, anchor2 and quote and `> 300` for claim (`findings.py:79-87`, `findings_v2.py:79-80`), applied only to `str` values that the check would also read (`anchor2` and `quote` not null, citations only when a dict, `anchor` only when the checker reaches it). The consensus requires a differential test (bullet 7) and M5 "no-op on every valid fixture line", which covers this; add a type-guard case (anchor an integer or a list, `citations` not a list, quote not a string): without the `isinstance` guard that `_check_flat` has at `findings.py:80-81`, `flat(None)` or `flat(5)` would raise in the parser instead of producing an error line. Residual side effect, see INV-011: a cut recorded on a line that is then dropped inflates `repairs`.

---

## count_divergence

### INV-010
- CATEGORY: count_divergence
- ASSUMPTION: recording `refs_changed` is enough for the cut's effect on `refs_norm`, `fp` and `same_defect` (C-008, A W5, B bullet "record only").
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: the cut can invent a token, not only lose one. [RAN] a claim whose flattened text has `FR-12` straddling character 297 becomes `...FR-1...` after `flat(claim)[:297] + "..."`: `refs_norm` goes from `['FR-12']` to `['FR-1']` (the `_REF_TOKEN` regex `\b[A-Z]{1,4}-[0-9]+(?:\.[0-9]+)*\b` matches `FR-1` before the dots, `findings.py:29`). `annotate` builds `fp = fingerprint(section, refs_norm)` and `same_defect` returns True on `fp` equality with non-empty `refs_norm` (`findings.py:340-343, 371-372`), so a cut claim or anchor that cites `FR-12` can cluster with an unrelated finding that cites `FR-1` in the same section, and rows store the invented token in `refs` (`ledger.py:183`). The planned mitigation (copy tail-only tokens into `refs`, kept only if M1 fires) addresses lost tokens, and M1 only counts `refs_norm(original) != refs_norm(repaired)` on the replay corpus, which measured 0 of 125 for anchors on single-line tasklist rows; claims were not part of that measurement. Needed: cut at a token boundary (back off to the previous whitespace) whenever the cut lands inside a `_REF_TOKEN` match, or drop claim cutting, and test it with the straddling input above.

### INV-011
- CATEGORY: count_divergence
- ASSUMPTION: `original_chars`, `kept_chars`, `repairs` item counts and `repaired_lines_rate` mean the same thing wherever they are read.
- STATUS: UNADDRESSED
- SEVERITY: LOW
- EVIDENCE: the claim keeps 297 source characters plus a 3-character marker (`card_convert.py:200-201` [READ]); a row note "shortened: claim 412 to 300" (A W2) therefore mixes stored length (300) with retained source (297), and "lose 3 to 135 characters" (diff-analysis C-009 [DOC]) depends on which one is meant. `repairs` is per field (bullet 2) but `repaired_lines_rate` (bullet 7) is per line; a line with `anchor` and `anchor2` cut is two items, one line. A line that was cut and then dropped for another fault (INV-008) is recorded as a repair although its cut text was never kept, so `repaired_lines_rate` can exceed the share of kept lines that were cut, and the conservation sum "non-blank lines = kept + priors + dropped" does not count the repair at all. Define the unit (line), count only kept lines, and name `kept_chars` as stored length.

### INV-012
- CATEGORY: count_divergence
- ASSUMPTION: the 200/201, 297+3/300, exact-300 and idempotence boundaries are handled.
- STATUS: ADDRESSED
- SEVERITY: LOW
- EVIDENCE: bullet 10 M5 lists boundaries 200/201 and 300/301 with and without repair, idempotence and no-op on valid lines; [READ] the checks use `len(flat(value))` (`findings.py:83-85`), and the pins that stay literal are `test_review_findings.py:113, 117` and `test_review_findings_v2.py:200, 241` [READ grep]. [RAN] a cut ending on a space leaves a stored value of length 200 whose flattened length is 199: it passes the check and locates. The anchor minimum of 12 cannot be reached by a cut (the cut value has length 200). A claim of exactly 300 is untouched, so cut and uncut claims of 300 characters are indistinguishable without the `repairs` record. Residual: the repair must measure flattened length, not raw length; an anchor of 250 raw characters with runs of whitespace that flattens to 190 passes today and must stay untouched (covered by the "no-op on valid" test).

### INV-013
- CATEGORY: count_divergence
- ASSUMPTION: a cut at a surrogate pair or a combining sequence cannot corrupt a stored field.
- STATUS: ADDRESSED
- SEVERITY: LOW
- EVIDENCE: [RAN] `json.loads('"\\ud83d\\ude00abc"')` gives length 4 (the pair is one code point), and a Python slice cuts by code point, so the cut cannot split a pair. A lone surrogate (`"\\ud800"`, length 1) survives parsing and then fails `json.dumps(..., ensure_ascii=False).encode("utf-8")` with `UnicodeEncodeError` [RAN]; `ledger.save` writes with `ensure_ascii=False` and `encoding="utf-8"` (`ledger.py:58-59` [READ]). That crash is pre-existing and independent of the cut (the cut neither creates nor removes a lone surrogate); noted only so M5 does not blame the repair for it. A cut may split a combining sequence (cosmetic).

---

## collection_boundaries

### INV-014
- CATEGORY: collection_boundaries
- ASSUMPTION: panel of 1, or every reviewer invalid, behaves sensibly with the new refusal and the existing zero-valid refusal.
- STATUS: ADDRESSED
- SEVERITY: LOW
- EVIDENCE: the zero-valid check is the first guard (`ledger.py:150-157`: `not any(block_ok.values())` raises before any mutation); the quorum check of C-03 sits in the same place (merged-output.md line 36 [READ]); the dropped-blocking check runs at the end of `merge_round` (bullet 8). So a panel of 1 whose only block still has a residual drop is refused as "no valid block" and never reaches the dropped-blocking test; the existing pins `test_review_ledger.py:345-373` use `_broken` (no block, or `not json`, or an unclosed empty block) and are not flipped by a length repair (A N4 [DOC]). Residual (LOW): that refusal text does not name the dropped lines, so the coordinator re-runs the whole review instead of a targeted re-ask; harmless, and the C-03 INV-010 note that the pin asserts message text still applies.

### INV-015
- CATEGORY: collection_boundaries
- ASSUMPTION: zero findings, a block with only `prior` lines, and an empty closed block are unaffected.
- STATUS: ADDRESSED
- SEVERITY: LOW
- EVIDENCE: v1 `parse_block` returns `ok` True with `findings == []` for a closed empty block or a priors-only block (`findings.py:159-196`); the repair has nothing to cut; conservation is trivially satisfied; the dropped-blocking refusal needs a dropped line. The v2 empty-block rule (`findings_v2.py:291-298`) is untouched because the repair never removes a line.

### INV-016
- CATEGORY: collection_boundaries
- ASSUMPTION: a rescued line whose prefix does not locate is "a visible row where today there is none" and that is acceptable (A N9; B N9).
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: B's replay found 5 of 94 over-limit fields not verbatim (3 of 37 blocking in P273) [DOC]; after the cut these become kept rows with `anchor_status: missing`, `span None`, `section "none"` (`findings.py:346-360` [READ]). Such a row can never be cleared by the loop: `same_defect` needs an `fp` with non-empty `refs_norm` or overlapping spans (`findings.py:367-379`), so with empty refs each round's re-find opens a new span-less row; `apply_revision` calls `hunks_touch(None, ops)` which is False (`findings.py:446-447`; `ledger.py:331-339`), so every "applied" fix map entry is `named_not_touched`. The result is FAIL, REVISE twice, then ESCALATE at the cap, each time with a row that no fix can touch. C-01 INV-015 (unaddressed [DOC]) is this same defect; the consensus text offers no rule (for example, surface it and let `defer` clear, or refuse to keep an unlocated rescued blocking line and re-ask instead). Before the cut that line was dropped; after it the spec loop spends reviews on an unfixable row.

---

## interaction_effects

### INV-017
- CATEGORY: interaction_effects
- ASSUMPTION: a cut anchor still locates "uniquely with the same first span" (K1, C-007, A-002) and that this can be verified offline on tasklist rows is enough; the runtime flag `anchor_ambiguous` can stay unread.
- STATUS: UNADDRESSED
- SEVERITY: HIGH
- EVIDENCE: [RAN] end-to-end with `ledger.merge_round` on a synthetic tasklist in which two rows share their first 200 flattened characters (a repeated boilerplate acceptance clause) and differ only at the end (the row id). The reviewer's full 262-character anchor locates uniquely at line 62; its 200-character prefix (what bullet 1 stores) locates at lines 1 and 62, and `annotate` takes the first (`findings.py:349-352`); `refs_norm` of both is empty because `_REF_TOKEN` does not match `T09.07` (`findings.py:29`). Round 1 recorded a blocking L1 at line 1; `defer` parked it; round 2, a reviewer reports a new blocking defect at line 62 with the cut anchor: result `verdict PASS, decision PASS, brief []`, rows `[L1 deferred]` and no row for the new defect (it was matched to the deferred L1 by `same_defect` with both refs empty and overlapping spans, `ledger.py:165-170, 207-209`; `deferred` is neither reset nor in the brief, `ledger.py:99-104, 235-238`). Today the same round is refused as "no valid findings block" (`LedgerError`, printed in the run) because the over-limit line is dropped and the only reviewer is invalid (`ledger.py:150-157`). So the cut turns a fail-closed refusal into a silent PASS for the standard one-reviewer re-review, and because nothing is dropped, the dropped-blocking refusal (bullet 8) has no line to fire on. `anchor_ambiguous` is written at `findings.py:351` and read nowhere in `src` (grep: one hit) [READ]. K1 measures this offline ("unique same-span prefix") on single-line tasklist rows (70 of 70, 89 of 89 [DOC]); the production populations for spec review (documents, tables with repeated clauses) and PR code are unmeasured, and A already moves the code threshold to 75 percent. Needed at runtime: a cut anchor whose prefix has more than one occurrence while the full flattened anchor has fewer is itemised as `ambiguous`, not matched to a `deferred` or `resolved` row, and for a blocking line counts as `blocking_state` true for the refusal (or is re-asked).

### INV-018
- CATEGORY: interaction_effects
- ASSUMPTION: in reflect the re-ask can be triggered from the repaired parse state, recorded as attempt 2 "before the `collected` commit", and the first-pass rate read from `first_pass_state` in the cluster listing (bullets 3, 5, 7, 12).
- STATUS: UNADDRESSED
- SEVERITY: HIGH
- EVIDENCE: the sequence in the skill makes this impossible as written. [READ] `SKILL.md:342` (step 3): "when the cards are back, record each attempt's completion the same way with `--stage collected`, then advance `collected`"; `SKILL.md:343` (step 4, Normalize): parse the block, record the compliance rate, re-ask an invalid block. `manifest.py:371-372` raises `OutOfOrder` once the stage is committed and `:378-381` raises `Conflict` when the earlier attempt is `complete` [READ]; diff-analysis A-006 [DOC] says E1 run A2 hit exactly that refusal. The carrier `first_pass_state` comes from `cluster_cmd.py:155-163` and `verify_cmd.py:136-138`, which run at step 6 over `panel/cards/` that step 5 writes after calibration [READ SKILL.md:344-345]; the registered review commands are `merge`, `ledger`, `manifest`, `panel`, `telemetry`, `cluster`, `verify-citations` (grep of registrations, `ledger_cmd.py`, `cluster_cmd.py`, `verify_cmd.py`, `manifest_cmd.py`, `panel_cmd.py`, `telemetry_cmd.py`, `merge_cmd.py`), and none parses a v2 block before step 6. So at step 3 and 4 nothing machine-readable says whether a card is valid before or after the cut: the attempt `completion` and the compliance rate are the orchestrator's own judgement, which is the very thing bullets 7 and 12 say the code now owns. Bullet 12 adds one sentence after the pinned Normalize sentences and moves no step. Either a parse-only command (usable at step 3, before the `collected` advance) plus a reorder of steps 3 and 4 is part of the consensus, or the reflect re-ask and attempt-2 record cannot run and the metric stays the orchestrator's count. The v1 side has the same hole and the consensus already answers it with the refusal-driven re-ask (A N1); reflect has no such substitute because its re-ask trigger is the invalid block itself.

### INV-019
- CATEGORY: interaction_effects
- ASSUMPTION: one additive sentence after the pinned Normalize sentences is enough (bullet 12) and does not contradict them.
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: [READ] `SKILL.md:343` keeps, unchanged, "the cards whose block is valid on this first parse, over the reviewers dispatched, before any re-ask. An invalid block gets one bounded re-ask for the block only... a block that still fails after the one re-ask stays invalid", and the test pins three of its substrings (`test_shadow_skill_contract.py:229-232` [READ]). Under the consensus "first parse" validity is the unrepaired state (a length-faulted block is not compliant) while the re-ask trigger is the repaired state (a length-faulted block is complete and is not re-asked). The same word "invalid" now carries both meanings inside one paragraph, and the additive sentence must override the second without editing the first. An orchestrator that follows the unchanged text re-asks every length-faulted block (the metric reads it as invalid), which wastes the re-ask and, for a block the cut already made complete, runs into `manifest.py:378-381`. The additive sentence has to say in plain words that the re-ask trigger and the compliance numerator use different states, and the skill copies (`.claude/skills`, `plugins/superclaude/skills/sc-reflect-protocol`) must be synced in the same change (`make sync-dev`, `make verify-sync` does not cover the loop prompts per C-03 INV-013 [DOC]).

### INV-020
- CATEGORY: interaction_effects
- ASSUMPTION: the dropped-blocking refusal "reuses the C-03 object" (A N5; bullet 8) and the coordinator has "one re-run signal".
- STATUS: UNADDRESSED
- SEVERITY: LOW
- EVIDENCE: when both apply, the quorum refusal wins by code position (it sits with the zero-valid check at `ledger.py:150-157`; the dropped-blocking check is at the end of `merge_round`), and C-03's object is `{"refusal": "quorum_shortfall", requested, complete, invalid}` with no `dropped` information and no `decision` key (merged-output.md line 77 [READ]). The coordinator fixes the missing reviewer, re-runs, and then meets a second refusal, `dropped_blocking`, with the same exit 12 (C-03 line 77: "Exit 12 ... unused inside `cli/review`"). Each refused attempt records nothing and costs reviewer spend outside `cap_reviews` (C-03 INV-001, INV-002 [DOC]). One refusal that carries every cause (invalid reviewers with their dropped items) avoids the second cycle. The loop prompt must branch on the `refusal` key, not on the exit code alone; the prompt copies skew until reinstall (C-03 INV-013 [DOC]).

### INV-021
- CATEGORY: interaction_effects
- ASSUMPTION: a refusal at the end of `merge_round`, on a working copy swapped in on success, keeps the existing pins and the "refusal changes nothing" property.
- STATUS: ADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: [READ] `merge_round` appends rows at `ledger.py:204`, mutates existing rows at `:209-238, 255-257, 265-272` and appends the round at `:276`, all on the dict the caller passed in; the pins are `test_review_ledger.py:352-361` (the ledger JSON byte-identical after the zero-valid refusal) and `:373` (`led["rounds"] == [] and led["rows"] == []`), and `merge_cmd.py:109-116` saves only after success. Bullets 8 (both advocates) name the working copy and the pins. The remaining implementation constraint is identity: callers (24 test call sites, `merge_cmd`) hold the original dict, so the swap must replace its contents in place (`clear` then `update`), and every helper that takes `ledger` (`_row(ledger, ...)`, `_brief_ids(ledger)`, `_decision(ledger, ...)`) must receive the copy. `result["_members"]` holds annotated finding copies, not ledger rows, so it is safe.

### INV-022
- CATEGORY: interaction_effects
- ASSUMPTION: the third validation path (`card_convert.py:226`, which calls `findings_v2.check_finding` directly) and its own claim cut do not diverge from the repair.
- STATUS: UNADDRESSED
- SEVERITY: LOW
- EVIDENCE: [READ] `card_convert.py:85-86` declares `MAX_REF_TEXT = 200` and `MAX_CLAIM = 300`, cuts claims with `text[: MAX_CLAIM - 3] + "..."` (`:200-201`) and validates through `check_finding` (`:226`), not through `parse_block`, so the repair never runs there; pin `test_review_card_convert.py:490-501` asserts `len == 300` and a trailing `...`. If A's claim cut is adopted, the repair and the converter hold two implementations of the same arithmetic and any later change to the marker or the 297 breaks one pin silently; if B's no-claim-cut is adopted, B bullet 12 documents the converter as the one exception. Under the unresolved C-009 both texts need the same sentence: one function owns the claim cut (the converter calling it, or the repair importing it), and `MAX_REF_TEXT` (a citation `ref`, not a quote) stays a separate constant (C-01 INV-008 [DOC]).

---

## sufficiency_challenge

### INV-023
- CATEGORY: sufficiency_challenge
- ASSUMPTION: "cutting the three location fields plus itemise plus a refusal closes the PASS-by-loss defect and the v2 loss unit". Name a downstream condition that falsifies it alone.
- STATUS: UNADDRESSED
- SEVERITY: HIGH
- EVIDENCE: inline enumeration of the gates between the cut site and the verdict (source read this session):
  1. G1, block level, `findings.py:124-158` / `findings_v2.py:233-262`: missing heading, no fence, several blocks, unclosed block set `ok` False; the cut does not touch them.
  2. G2, line level, `findings.py:90-121, 160-195` / `findings_v2.py:84-187, 264-290`: JSON, severity, blocking, category, refs, coverage_rows, lens, deviation class stay as rejection causes after the cut (first fault only, INV-008).
  3. G3, locate, `findings.py:276-304, 346-360`: a line with an unlocated anchor is kept with `span None`; a prefix with several occurrences gets the first (INV-016, INV-017); `anchor_ambiguous` is read by nothing.
  4. G4, same defect, `findings.py:340-343, 367-379`: `fp` plus non-empty refs, or shared refs or both empty plus spans within 3 lines (INV-010, INV-017).
  5. G5, row matching, `ledger.py:165-239`: first matching existing row wins, including `deferred` and `resolved` rows; a deferred row stays deferred.
  6. G6, silence clears, `ledger.py:254-258`: a `resolved_check` row with no member this round becomes `resolved`; a re-find lost to a drop or a truncation is silence.
  7. G7, `ledger.py:259-272`: `prior` lines only add history notes in the current code.
  8. G8, verdict, `ledger.py:99-104, 273-275`: FAIL only when a blocking row is `open` or `regressed`; the refusal sees only this round's drops.
  9. G9, to be added by C-02 and C-03: quorum floor over `block_ok`, the CRITICAL floor, derived eligibility.
  10. G10, `merge_cmd.py:99-118`: refusal writes nothing; the coordinator prompt decides what exit 12 means.
  11. G11, `ledger.py:328-339`: `hunks_touch` on the stored span moves a row to `resolved_check`, after which G6 clears it.
  The consensus is sufficient only if G3 to G6 and G8 behave as if the repaired line were a trustworthy, correctly located row. Three conditions that each falsify the central claim without the others: (a) a dropped blocking line in a FAIL round is forgotten when a later round passes (INV-001, G8 per round); (b) a cut line that matches a different place and is absorbed by a `deferred` or `resolved` row passes with nothing dropped, so the refusal is silent, [RAN] verdict PASS with the new blocking defect unrecorded (INV-017, G3 and G5); (c) a truncated block loses its tail with no line to drop (INV-025). In addition the "v2 loss unit" half fails alone for any non-length fault (INV-024). Each condition has a one-line unit test that can be written before code: the cross-round sequence, the two-row prefix document used in INV-017, an unclosed block with a blocking line missing.

### INV-024
- CATEGORY: sufficiency_challenge
- ASSUMPTION: the cut removes the v2 loss unit (A's C-003 win: "`cluster.py:255-257` skips the whole reviewer when its block is not valid; the cut removes that").
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: [READ] `findings_v2.py:298-303` sets `state` to `invalid` on any error; `cluster.py:219-221` takes `valid` from `state == "complete"` and `cluster.py:255-257` skips every record that is not valid, so one residual line fault still discards all of a reviewer's findings. The residual faults in v2 are non-length: `coverage_rows` outside the assigned slice (`findings_v2.py:166-176`), the lens and `deviation_class` rules (`:140-164`), citation path and line-range rules (`:59-81`), bad JSON. The consensus's own data says so: in E1 four of five re-asks were for non-length causes (`coverage_rows`, citation line numbers) [DOC: diff-analysis X-003]. After the cut, the unit of loss in v2 is still a whole reviewer, for every cause except length, and the recovery depends on one stateless re-ask that has no recorded success rate on gateway models (X-002: no recovery rate exists). Salvaging the valid lines of an otherwise invalid v2 block (itemise the bad line, keep the others, mark the reviewer `invalid` for the floor but union its valid lines as v1 does at `ledger.py:135-138`) is not in the consensus; without it the claim should read "removes the length share of the v2 loss unit".

### INV-025
- CATEGORY: sufficiency_challenge
- ASSUMPTION: a lost blocking finding always leaves a dropped line that can be itemised and refused on.
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: a truncated block (the report ends inside the fence) loses its tail; no line exists for the missing findings, so there is nothing to itemise, no `blocking_state`, no refusal. [READ] `findings.py:151-158` sets `ok` False for an unclosed block but keeps every finding parsed before the cut (`:160-195`), and `ledger.py:135-138` unions them; with two other valid reviewers the C-03 floor `complete >= min(2, requested)` is met (merged-output.md line 36 [READ]) and the verdict can be PASS although the third reviewer was cut off while listing findings. The last line of a truncated block, a partial JSON object, is itemised as `unknown` and can trigger the refusal; every full line after it cannot. Audit-D has 80 `block ok false` runs and 44 are length-driven (diff-analysis C-002 [DOC]); the share that is truncation is not measured by either advocate. The consensus should state that truncation is outside the guard and keep it as a recorded shortfall (the state `truncated` is already visible, `findings_v2.py:299-300`), or require a re-ask for every `truncated` reviewer before a PASS.

### INV-026
- CATEGORY: sufficiency_challenge
- ASSUMPTION: the kill lines can show that the refusal is wrong or right (K5: wrong if it fires on more than 5 of 264 merges after the cut).
- STATUS: UNADDRESSED
- SEVERITY: MEDIUM
- EVIDENCE: after the cut the refusal fires on 0 of 264 in the study data (A N2; B E4 [DOC]), so K5 passes trivially and no measurement exercises the code path that bullet 8 adds, or the residual classes it exists for (bad severity, refs, JSON; 4 of 90 lines in P273, and `unknown` has 0 members). K5 also has no live signal (INV-003). The path will first run in production. It needs a synthetic fixture matrix before it ships (the matrix in B bullet 9: one reviewer all dropped; one dropped blocking plus one empty block; surviving blocking row; `blocking: false` drops only; acknowledged drops; panels of 1 to 5) and the cross-round and ambiguity cases from INV-001 and INV-017; a measured fire rate of zero is not evidence that the guard works.

---

## Summary

- Total findings: 26
- ADDRESSED: 6 (INV-009, INV-012, INV-013, INV-014, INV-015, INV-021)
- UNADDRESSED: 20
- UNADDRESSED by severity: HIGH 4 (INV-001, INV-017, INV-018, INV-023), MEDIUM 12 (INV-002, INV-003, INV-005, INV-006, INV-007, INV-008, INV-010, INV-016, INV-019, INV-024, INV-025, INV-026), LOW 4 (INV-004, INV-011, INV-020, INV-022)
- By category: state_variables 4 (all UNADDRESSED), guard_conditions 5 (4 UNADDRESSED, 1 ADDRESSED), count_divergence 4 (2 UNADDRESSED, 2 ADDRESSED), collection_boundaries 3 (1 UNADDRESSED, 2 ADDRESSED), interaction_effects 6 (4 UNADDRESSED, 1 ADDRESSED with residual, 1 UNADDRESSED LOW), sufficiency_challenge 4 (all UNADDRESSED)

Checks run by me (all in memory, nothing written): mid-token cut and `refs_norm` (INV-010), trailing-space cut and surrogate behaviour (INV-012, INV-013), CRITICAL with `blocking: false` accepted by both checkers and the v2 reflect rule message (INV-005), prefix ambiguity with `annotate` and a full `merge_round` and `defer` sequence (INV-017), prior-line typo (INV-007), over-limit claim hiding a coverage fault (INV-008).
Not checked: any population-level rate (I did not re-run audit-D or P273), the real Reviser and coordinator prompts' reaction to exit 12, the live reviewer behaviour under a changed brief, PR-code corpora.

END-OF-ADVOCATE-FILE
