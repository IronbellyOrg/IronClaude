# Round 2 rebuttal, Advocate for Variant A (slot C-02, ledger clearing and verdict authority)

Date: 2026-11-14. Cited lines were re-read this session: `ledger.py` 1-80 and 80-494, `merge_cmd.py` whole, `ledger_cmd.py` whole, `findings.py` 90-196, `document_review_loop_prompts.md` 26-75, `spec-panel.md` 254-265, `tests/review/test_review_ledger.py` 316-339, `panel.py` (grep of `apply_to`). Not re-read: synth-06 (so I do not quote VM-3's exact wording), `stoprule.py`, research files.

## 1. Replies to the criticisms of A in round1-B.md

| B's criticism of A | Reply |
|---|---|
| W1 / strength 1: in the one-reviewer default, A's gate is "a free JSON line"; a rubber-stamp yes is untestable | Concede the residue. Two things stay true. Without a quote, A's gate still removes the three reproduced non-dishonest paths (unrelated empty block clears; invalid-block reviewer clears; absent reviewer counts). And B's quote does not remove the rubber stamp either: B conceded it proves reading, not fixing (B Concession 1). B's own narrowing ("when the span is None accept any quote from the changed region") makes the check vacuous exactly where `map_span` returns None for a deletion (`ledger.py:345-346`). |
| Strength 2: the shipped brief already makes the reviewer produce quotes, so a gate on them is free | Partly wrong. The quotes at `prompts.md:44, 46` are diff lines copied into the report's BEFORE/AFTER block for a role-swap self-check. The prior line at `prompts.md:61` carries no quote, and `findings.py:186` keeps only `prior` and `status`. A per-row quote is new reviewer work, not an existing one turned into a gate. |
| W2 / strength 4: dissent bookkeeping, `apply_revision` skips non-open rows (`ledger.py:328`) | Concede. Confirmed: `if row["status"] not in ("open", "regressed"): continue`. A held row left in `resolved_check` would swallow the next fix silently. Fixed in section 4 (C-001). |
| W3: `expires_round` is nearly inert under the cap | Concede with a stronger reason than B gave (section 3, new evidence 5). |
| W4: re-find reopening overrides a human park | Concede. Row stays `deferred` (C-007). |
| W5 / strength 3 and 8: text binding left open; stored fields removed | Concede text binding (C-003). Concede the file-shape point in part (C-009). |
| W6 / strength 6: CRITICAL with `blocking: false` passes | Concede. A's own round 1 said it would not touch it; `spec-panel.md:259` says "CRITICAL is blocking". Floor adopted (C-004). |
| Strength 7: deterministic negative tests exist for B's guard but not for a lazy yes | True and not answerable: no test separates a lazy yes from an examined yes. A's guard has its own deterministic negatives (dissent, invalid-block answerer, absent reviewer, re-find in same round), so it is testable, only weaker. |

## 2. Updated assessment of B

B is better than A on: text-hash binding; the state a dissent row takes; not reopening a human park; the free M2 pre-count; additive file shape; the fail-closed stance that the answer must gate, not warn. B is not better on the quote as a gate and not better on the category predicate. B has now conceded both in its own round 1 (Concessions 1 and 2), so the two papers differ in the merged design only on whether the `evidence` key is recorded. I accept from B: B2 (only valid-block answers count), B4 (hash binding), B5's three lists, B7 (terminal deferral), U-007 as a stated principle, M2, M3.

## 3. New evidence not yet presented (all re-read this session)

1. **Priors from invalid-block reviewers are collected.** `parse_block` appends a valid prior line to `res["priors"]` (`findings.py:186`) even when other lines make `ok` false (`:190`). `merge_round` collects every prior with no `block_ok` test (`ledger.py:139-140`). So any prior-driven gate must filter by `block_ok[reviewer_id]`; B2 is necessary, not optional.
2. **Priors are not de-duplicated.** `seen` guards only finding ids (`findings.py:159, 193`), so one reviewer can type `resolved` and `open` for one lid. Rule needed: any `open|regressed` from a valid reviewer beats any `resolved`.
3. **Order of operations.** The clearing loop (`ledger.py:254-258`) runs before the prior loop (`:259-272`). A prior-gated clear needs the prior map built first; this is a reorder, not an addition.
4. **A same-round re-find already beats a `resolved` answer.** A re-found `resolved_check` row becomes `regressed` at `ledger.py:235-238`, before the clearing loop tests `status == "resolved_check"`. B's "re-find wins" clause needs no new code.
5. **Expiry is inert for a stronger reason.** Deferred rows are already outside `_brief_ids` (`ledger.py:99-104`), and when only deferred rows remain both papers return ESCALATE, after which VM-6 refuses further rounds. A deferral therefore never meets a later round in which an expiry could fire.
6. **The module docstring states the pinned rule too** (`ledger.py:3-4`: "a reviewer's own prior lines are recorded as notes and never change one"). Any dissent routing that moves a row changes that sentence, not only a test name.
7. **A's round-1 claim about `--resolution` was overstated.** `merge_cmd.py:73-83` reads `reviewers` only to build a `models` map; requested ids are not counted anywhere. Counting requested-but-absent reviewers is new code in `merge_cmd.py`.
8. **A quorum deadlock if C-03 sets Q above the re-review panel size.** Re-review resolves one reviewer by default (`panel.py:600`, `apply_to` validated at `:189-196`; all 8 templates `["first"]` per both papers). A fixed Q of 2 would make a one-reviewer re-review unable to clear any row, so every loop ends at the cap.
9. **The empty-diff trap for a verify-only retry.** `prompts.md:44` and `spec-panel.md:262` say an empty diff leaves every prior blocker open. A retry that asks only for missing prior lines must therefore reuse the same BASELINE and CANDIDATE (non-empty diff), not a second `revise` with an empty fix map.
10. **No existing review test pairs CRITICAL with `blocking: false`** (grep of `tests/review` found none, a pattern-limited check), so a CRITICAL floor breaks no pin by that search.
11. **A parser-side CRITICAL floor would be wrong.** A parser error sets `ok` false and drops the line (`findings.py:188-192`); that is the C-06 whole-line-drop cost A named. The floor belongs in `merge_round`.
12. **Only `defer` and `verdict()` read round-record `verdict`/`decision`/`brief_ids`** inside `cli/review` (grep: `ledger.py:358-370`, `ledger_cmd.py:109`).

## 4. Final positions (the exact rule for the merged design)

**C-001 Clearing gate and dissent state.** A `resolved_check` row becomes `resolved` in `merge_round` only if (a) the count of `block_ok`-true reviewers that typed `prior <lid> resolved` is at least `need = min(Q, number of reviewers requested this round)`, (b) no `block_ok`-true reviewer typed `open` or `regressed` for it, and (c) it is not re-found this round. Build the prior map before the clearing loop. A `block_ok`-true `open|regressed` prior moves a `resolved_check` row to `regressed` (history event `dissent`), the route a re-find already takes, so `apply_revision` accepts it (`ledger.py:328`) and `brief_ids` picks it up (`:103`). `open` and `regressed` are one signal to the ledger. A row failing the gate without dissent stays `resolved_check` and is listed in `verify_ids`. Silence never clears. Priors never move a row that is not `resolved_check`.

**C-002 The `evidence` quote.** Recorded only, never gating, optional. The parser keeps an optional string `evidence` on a prior line (one-line change at `findings.py:186`); the ledger puts it in the `prior_note` event with a boolean `quote_in_doc`. It does not gate because the deletion fix, which the revise brief prefers (`prompts.md:53`), leaves nothing in the new text to quote, so a gate would hold correct deletions and feed cap escalations; and a lazy reviewer can quote any line. The recorded flag is the data M1 needs to show whether a gate would add power. If B's measurement later shows it does, promote it to a gate only with a deletion carve-out (a quote from BASELINE absent from CANDIDATE).

**C-003 Text-hash binding.** Adopt B4. `apply_revision` stores `pending_new_sha256 = sha256_text(new_text)` as a top-level ledger key; `merge_round` refuses (LedgerError, ledger unchanged) when it is set and `sha256_text(doc_text)` differs, then clears it. `load` accepts extra top-level keys (`ledger.py:47-48`), so this is additive. If `revise` was never run, no check applies; that gap cannot be closed in the ledger.

**C-004 Blocking authority.** Typed `blocking` stays the authority, plus a CRITICAL floor applied in `merge_round` (not the parser): `blocking = typed or severity == "CRITICAL"`; member records keep `blocking_typed`; each flip adds a warning (`CRITICAL typed non-blocking, floor applied`). No category predicate, no grader in the core, `verdict:` line stays parser-neutral. Declared risk: `prompts.md:31, 60` tell reviewers to type `blocking` only after the grading check, while `spec-panel.md:259` says CRITICAL is blocking; the floor chooses the second. The warning count is M3's data. A lens that wants a stricter rule may add one later.

**C-005 / X-001 The pinned test.** The module docstring (`ledger.py:3-4`), the test name and the rule are restated: "A prior line never changes the status of a row that is not `resolved_check`. On a `resolved_check` row it is the only reviewer input accepted as an examination answer: `resolved` is a precondition of the merge-loop clear, `open|regressed` routes to `regressed`." `test_prior_lines_never_change_a_status` (`test_review_ledger.py:318-338`) keeps passing unchanged, because L4 and L2 are `open` rows; it should be renamed, and new tests added for the `resolved_check` cases. I concede the name read literally is too broad.

**C-006 Defer.** `defer` requires `--owner` and `--reason`; allowed only on a blocking row in `open`, `regressed` or `resolved_check`; touches no round record; row is terminal for the machine and counts open. No expiry field in the core: nothing would read it (evidence 5). A lens with a wall-clock policy may add metadata.

**C-007 Re-find of a deferred row.** Stays `deferred`; the existing `refound` history entry (`ledger.py:232`) stays and the merge result lists `refound_deferred`; the Escalation text lists it.

**C-008 Outputs and the empty-brief REVISE.** `brief_ids` = blocking `open|regressed`; `verify_ids` = blocking `resolved_check`; `held_ids` = blocking `deferred`. PASS only when all three are empty; else FAIL, REVISE below the cap, ESCALATE at the cap or when only `held_ids` remain. Exit codes stay 0/10/11 (`ledger_cmd.py:13`). When `brief_ids` is empty and `verify_ids` is not, the decision stays REVISE (no new exit code) but the Reviser-brief section prints "no revision needed; re-review the same candidate against the same baseline to answer: L1, L3" and `ledger verdict` adds an additive `next` field (`re-review` or `revise`). The retry uses the same BASELINE and CANDIDATE (evidence 9). It costs one review of the cap; that is accepted and bounded.

**C-009 File shape.** Additive. Round records keep writing `verdict`, `decision`, `brief_ids` as a merge-time snapshot that nothing reads (only `verdict()` and `defer` read them, evidence 12); `verdict()` computes from rows; `defer` stops writing them. New fields: `verify_ids`, `held_ids`, `pending_new_sha256`, `blocking_typed`, `owner`. Schema string kept. Conditional: if synth-06 VM-3 literally says "never stored", drop the three snapshot keys instead and keep readers tolerant of old files (A's round-1 form). Whether `review-ledger/2` is needed stays open (LG-2).

**`render_merged_report` gap (`ledger.py:438-466`, `:482`).** Both papers need it. The detailed section prints claim and anchor for every row in `brief_ids + verify_ids + held_ids` under three headings, and the Escalation paragraph lists all three lists (today it lists `brief` only). Open point: whether PRIOR in the re-review brief is this merged report or a single reviewer report; I did not verify it, and if it is a single report the verify rows must be restated in the re-review brief instead.

**A-005 and C-03.** Independent except for one parameter: C-02 owns `need = min(Q, requested)`, C-03 owns Q and the round-1 partial-panel rule. The `min` prevents the deadlock in evidence 8. Counting requested reviewers needs `merge_cmd` to pass the `--resolution` reviewer ids into `merge_round` (evidence 7); without `--resolution`, requested is the reports passed.

## 5. Positions changed since Round 1

| ID | Old (round 1) | New | Why |
|---|---|---|---|
| C-001 | HYBRID: A's gate; dissent withholds at `resolved_check` | Dissent routes to `regressed`; gate uses `need = min(Q, requested)` | `ledger.py:328` skips non-open rows; deadlock risk (evidence 8) |
| C-002 | HYBRID: non-gating key with an occurrence flag | Unchanged in substance, now specified: parser keeps key, `quote_in_doc` flag, promotion rule with deletion carve-out | `prompts.md:53` deletion problem; B conceded the same limit |
| C-004 | HYBRID: typed plus CRITICAL floor | Floor lives in `merge_round`, not the parser | `findings.py:188-192` drops the line and invalidates the block |
| C-005 / X-001 | A: pinned rule "stays true" | Rule narrowed to rows not in `resolved_check`; test renamed; docstring edited | `ledger.py:3-4`; dissent now writes a status |
| C-006 | A: `expires_round` that reopens the row | No expiry in the core | evidence 5 |
| C-007 | B (kept my earlier concession) | B: stays `deferred`, `refound_deferred` surfaced | unchanged from round 1 table, now with the Escalation-text requirement |
| C-009 | B (additive) | Additive snapshot kept, with a VM-3 conditional | evidence 12; synth-06 not re-read |
| A-005 | B | Independent except `need = min(Q, requested)` | evidence 8 |
| C-003 | B | B, specified as a top-level `pending_new_sha256` | `ledger.py:47-48` tolerates new keys |
| Round-1 claim | `--resolution` "already carries" requested ids for counting | Corrected: counting is new code | `merge_cmd.py:73-83` |
