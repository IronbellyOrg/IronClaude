# Round 2.5 invariant probe: fault-finder findings (conflict C13, ledger model)

Scope: the emerging consensus items 1-6 after Round 2. Read-only. Source read this pass (paths relative to `src/superclaude/cli/review/` unless noted): `ledger.py` (all 494 lines), `merge_cmd.py` (all), `ledger_cmd.py` (all), `findings.py` 1-457, `findings_v2.py` 255-304, `panel.py` (grep, `:600`, `:697`), `rules/prompts/document_review_loop_prompts.md:36-75`, `~/.claude/skills/sc-review-ledger/scripts/review_ledger.py:1840-1914`, `tests/review/` (grep). Tool calls used: 13 of 25. Ranked by correctness risk (HIGH first). 20 findings: 18 UNADDRESSED, 2 ADDRESSED in principle.

---

ID: INV-001
CATEGORY: interaction_effects
ASSUMPTION: Once the consensus records a would-be PASS with an uncleared row as FAIL with `unverified`, the stored FAIL stays FAIL until a reviewer re-checks the rows.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: `ledger.py:350-360` `defer()` removes the lid from `last["brief_ids"]` and, if the list is then empty, writes `verdict, decision = "PASS", "PASS"`. It never looks at degraded, unverified, the cap, or whether the lid was in the brief at all. It also does not check that the row is blocking or live (`:352-353`). `_brief_ids` (`:99-104`) lists only blocking rows in `open` or `regressed`, so an `unverified` FAIL has an EMPTY `brief_ids` (its rows are `resolved_check`). So `superclaude review ledger defer --lid <any row>` (`ledger_cmd.py:74-91`) rewrites the stored FAIL into PASS (exit 0 at `:109`). This is a second, ungated path to PASS next to the silence path the consensus closes. Tests only pin that defer sets status `deferred` (`tests/review/test_review_ledger.py:396-405`).
SUGGESTED RESOLUTION: Replace the inline PASS recompute with the same `decide()` function `merge_round` uses, fed from ledger state (live blocking rows, `unverified`, `degraded`, cap), not from the stored list. `defer` should accept only a live blocking row, and a deferred PASS should carry a `deferred_lids` field. Add tests: defer after an `unverified` FAIL stays FAIL; defer of a non-blocking or resolved row is refused.

---

ID: INV-002
CATEGORY: interaction_effects
ASSUMPTION: Consensus item 2 asks for both "atomic refusal, nothing recorded" and "bounded refusal, two refusals then ESCALATE". These are treated as compatible.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: A refusal is a raised `LedgerError` before `led.save` (`merge_cmd.py:109-116`), so by design nothing is written and no counter survives it. The only bound in the transcript is prose for the coordinator (Round 2, A "Fixes A needs" item 4: "prose only and no unit test can pin coordinator behaviour"). `ledger verdict` reads only the stored last round (`ledger.py:363-372`; `ledger_cmd.py:94-109`), so while the loop is refused the ledger still says the previous round's REVISE (exit 10), not ESCALATE (11). The cap check `_decision` (`ledger.py:93-96`) runs only on a recorded round. So "always terminates" holds only for recorded rounds (at most cap); the refuse-and-rerun cycle is unbounded in code. At `n == cap` a refused would-be PASS never reaches `_decision` at all.
SUGGESTED RESOLUTION: Name one permitted write on refusal: append `refusals: [{round, reason, report_sha256s}]` (additive key) and save with rows and rounds untouched. After two refusals for the same round, `merge_round` records an ESCALATE round itself (decision ESCALATE, flag `refused_twice`), so `verdict` exits 11. Test both: rows byte-identical after a refusal, and the third merge call yields ESCALATE.

---

ID: INV-003
CATEGORY: guard_conditions
ASSUMPTION: The clearing gate ("a `resolved_check` row clears only when a valid reviewer gave a `prior` line for it and did not re-report it") treats any prior line as a positive answer.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: `findings.py:23` allows prior statuses `resolved`, `open`, `regressed`; `:175-186` stores `{prior, status}` for all three. The clearing loop (`ledger.py:254-258`) is keyed only on "no cluster re-reported the row" (`members_by_lid`), and priors are consumed only afterwards as history notes (`:259-272`). A reviewer who writes `{"prior":"L3","status":"open"}` and gives no finding line for L3 meets the literal consensus wording and clears L3. The prompt tells the reviewer to record "resolved, open or regressed" (`document_review_loop_prompts.md:44,61`), so this is the normal way to say "still broken". The consensus never says what `open` or `regressed` do to a row.
SUGGESTED RESOLUTION: Say it: only `status == "resolved"` can clear. `open` or `regressed` keeps the row out of `resolved` and moves it to `regressed` (the one case where a prior line may change a status, always toward blocking), with a note. A prior `open` with no matching finding line is recorded as an inconsistency in `warnings`. Pin test: prior `open`, no finding, row stays uncleared and the round is not PASS.

---

ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: "A valid reviewer gave a `prior` line" is well defined: one reviewer, one line per row, from a valid block.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: `ledger.py:127-140` appends a reviewer's priors to `priors` regardless of `parsed["ok"]`. `parse_block` keeps parsing lines inside a truncated or partly invalid block (`findings.py:151-187`), so a reviewer cut off mid-block has already emitted prior lines for the first rows. `findings.py:159-187` dedups finding ids (`seen`) but not prior ids: the same id can appear twice with different statuses. With more than one valid reviewer (explicit multi-reviewer re-review, which consensus item 1 keeps supported) the consensus does not say whether one `resolved` plus one `open` clears, or whether all valid reviewers must answer.
SUGGESTED RESOLUTION: Count priors only from reviewers with `block_ok`. Reject or collapse duplicate prior ids inside one block (the most blocking status wins, and the block is flagged). Across reviewers: a row clears only if every valid reviewer that answered said `resolved` and none re-reported it; any `open` or `regressed` keeps it. Tests for each of the three.

---

ID: INV-005
CATEGORY: interaction_effects
ASSUMPTION: A would-be PASS with an uncleared `resolved_check` row is recorded as FAIL with `unverified: [lids]`, consuming a review number, and the next round can then clear those rows.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Three places read only `brief_ids`. (a) The merged report's `## Blocking findings` and `## Reviser brief` come from `brief` (`ledger.py:438-466`, `:487-493`), so an `unverified` FAIL renders "Blocking finding ids: none". (b) The next reviewer's instruction is "one prior line per prior blocking finding id" taken from PRIOR (`document_review_loop_prompts.md:49,61`), so the unverified ids are not named to it, and a fully compliant reviewer cannot answer rows it was never told about. (c) `_decision` returns REVISE below the cap (`:93-96`), so at review 2 the reviser is sent into a fix cycle with an empty id list. Net: review 3 then ESCALATEs even with a compliant reviewer. This burns one of the two fix cycles for no repair.
SUGGESTED RESOLUTION: Render `unverified` ids in a separate section of the merged report ("Verify these rows; answer each with a prior line and an evidence quote") and add them to the RE-REVIEW instruction. Do not put them in `brief_ids` (the reviser must not edit them). For an `unverified`-only FAIL, set the decision to a distinct `RE-REVIEW` (no reviser step), or say explicitly that REVISE with an empty id list is accepted. Test: round 2 `unverified` FAIL then round 3 with prior lines plus evidence reaches PASS.

---

ID: INV-006
CATEGORY: state_variables
ASSUMPTION: `ledger revise` is called exactly once per fix cycle, with `--new` equal to the next merge's `--doc`.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: `apply_revision` checks only that `--old` hashes to the LAST merged round's document (`ledger.py:305-314`). That value does not change after a revise, so a second run with the same `--old` passes the check. On the second run, rows already `resolved_check` are skipped (`:328-329`), but the span-mapping loop (`:343-346`) runs again over every row and maps spans that are already in new-text coordinates through the old-to-new opcodes a second time. Rows still `open` are then tested with `hunks_touch` against the corrupted span (`:331-333`), so an untouched row can move to `resolved_check` (a wrong clear path once a gate accepts a loose `prior`). If `revise` is skipped, the next merge matches findings against stale old-text spans (`same_defect` span test, `findings.py:367-379`). A reviser re-run (prompt line 70 leaves the call to the coordinator) is a realistic trigger.
SUGGESTED RESOLUTION: Record `revised: {round, old_sha256, new_sha256}` on the round entry. Refuse a second revise for the same round and refuse a merge whose doc hash differs from `revised.new_sha256`. Pin tests: revise twice leaves spans unchanged (second call refused); merge without revise is refused or flagged.

---

ID: INV-007
CATEGORY: guard_conditions
ASSUMPTION: The quorum denominator comes from `--resolution`, and a coordinator will pass the right file.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: `merge_cmd.py:74-83` reads only `reviewers[].reviewer_id` and `model` from the file. The resolution carries `review_kind` (`panel.py:697`) and the reviewers list (`:698`), and neither is checked. Failure cases: (1) the round-1 resolution (3 reviewers) is reused at review 2: panel 3, quorum 2, one anchor reviewer, so every would-be PASS is refused or degraded for ever (feeds INV-002). (2) a resolution with an empty `reviewers` list gives panel size 0 and quorum `min(2, 0) = 0`. (3) report ids absent from the resolution, or more reports than resolution rows, shrink the denominator (`models.get(rid)` silently returns `None`, `:94`). (4) `--resolution` omitted on a 3-report round-1 merge: panel size defaults to the reports passed, so dropping the truncated report gives 2 of 2 valid (transcript A failure 3, called "prose only").
SUGGESTED RESOLUTION: `panel_size = len(resolution.reviewers)`; refuse when a report id is not in it, when `review_kind` does not match the round (`first` for n == 1, `re-review` for n >= 2), or when the list is empty. Record `panel_size`, `quorum`, `valid`, `denominator_source` on the round. For round 1 with more than one report and no `--resolution`, mark the round `degraded` (unknown denominator) so it cannot PASS. Tests for each.

---

ID: INV-008
CATEGORY: collection_boundaries
ASSUMPTION: Rows have a span, and the span points at the defect.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: `annotate` sets `anchor_status` and `anchor_ambiguous` (`findings.py:350-351`), but nothing in `ledger.py` reads them (grep over `src/superclaude/cli/review` finds them only in `findings.py` and the findings tests). (a) A duplicated anchor: `locate` returns every occurrence, `annotate` keeps `spans[0]` (`:352`), and the row's span is the FIRST occurrence even if the defect is the second. A fix at the second occurrence gives `named_not_touched`; an unrelated edit at the first gives `resolved_check` (`ledger.py:331-339`). (b) A missing anchor: span `None`, `hunks_touch(None)` is False (`findings.py:445-447`), so the row can never reach `resolved_check` and ends in ESCALATE at the cap (test `test_missing_anchor_is_kept_without_a_span`, transcript A-006). Consensus item 4 covers only the NEW-ROW anchor at the verify boundary, not `merge_round` or the case where the reviser fixes an unanchored row.
SUGGESTED RESOLUTION: Store `anchor_ambiguous` and `anchor_status` on the row and render them in the merged report. A row with `anchor_ambiguous` may clear only via a prior line whose evidence quote overlaps one of the occurrences touched by a hunk. A spanless blocking row gets `unanchored: true`; the decision text says "needs a human defer or re-anchor" instead of a fix cycle. Tests: duplicate-anchor row and spanless row each, with a revise.

---

ID: INV-009
CATEGORY: interaction_effects
ASSUMPTION: Adding `evidence` to the `prior` line (consensus item 3) gives a mechanical proof of checking, and `findings-v1`, `findings-v2` and the revise path will carry it.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: (a) The v1 parser drops unknown keys: `findings.py:186` stores only `{prior, status}`, so `evidence` is silently discarded until `parse_block` is changed. (b) v2 rejects every prior line (`findings_v2.py:279-283`; consensus item 6 knows). (c) The quote rule "must occur in the new text" is weak as stated. `fnd.locate` (`findings.py:276-304`) matches any occurrence anywhere in the document, there is no minimum length (the finding anchor has 12 to 200, `:104`), and the occurrence need not be near the row or in a changed hunk, so quoting the title proves nothing. (d) Deletion fixes: the reviser rules say "prefer deleting or narrowing" (`ledger.py:22-26`, `document_review_loop_prompts.md:53`). A deletion leaves no new text at the row to quote, and `hunks_touch` works in OLD coordinates (`findings.py:442-457`), so there is no new-side check yet.
SUGGESTED RESOLUTION: Parse `evidence` (string, flat length 12 to 200) for status `resolved`, and make it required there. Script checks: the quote must `locate` in the new text AND overlap `map_span(row.span, ops)` widened by 3 lines, or touch a changed hunk on the new side. For a deletion-only hunk the script checks directly that the row's anchor no longer `locate`s in the new text and accepts a neighbouring-line quote. Missing `evidence` on `resolved` counts as no answer (row stays `resolved_check`). Test: title quote refused; deletion fix accepted.

---

ID: INV-010
CATEGORY: sufficiency_challenge
ASSUMPTION: "This consensus package ALONE yields a loop that cannot certify PASS wrongly, cannot clear a row wrongly and always terminates."
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE (source-file branch enumeration, files and lines read this pass):
PASS is assigned only at `ledger.py:274` (`"FAIL" if brief else "PASS"`) or in `defer` `:358-360`. A row leaves `_brief_ids` (`:99-104`: blocking and status `open` or `regressed`) by these branches only:
 1. Never created: a finding line fails validation and is dropped (`findings.py:163-167`, `:188-192`), and the reviewer's block is `ok == False`, but another reviewer's valid block lets `any(block_ok)` pass (`ledger.py:150`). A quorate 2-of-3 panel therefore certifies PASS with a dropped blocking line. Consensus quorum does not close it (INV-016).
 2. Born non-blocking (`:187`) or un-blocked by a re-find (`:213-218`): closed by sticky blocking (consensus 2) except the partial-reviewer and C05 interactions (INV-011).
 3. To `resolved_check` at `:334` (fix map `applied` plus `hunks_touch`). The fix map can come from the table fallback (`findings.py:199-202`, `:209-223`) and `ledger_cmd.py:64-70` applies `fm["items"]` even when `fm["ok"]` is False. Corrupted spans from a double revise (INV-006) and duplicate anchors (INV-008) feed this branch.
 4. To `resolved` at `:254-258` (silence): closed by the clearing gate, with holes INV-003, INV-004, INV-009.
 5. To `deferred` at `:353`, with the recompute at `:358-360`: not touched by the consensus (INV-001).
 6. Out-of-band: `load` checks only the schema string (`:47-48`); a hand edit or an older binary (INV-014) bypasses every rule.
Termination: recorded rounds are bounded by `expected = len(rounds)+1` (`:114-118`) plus the new cap refusal. Unrecorded steps have no counter: refused merges (`:150-157`, new refusals), `revise` (`:301-347`), `defer`, reviser and reviewer re-runs. Bound exists only as coordinator prose (INV-002).
DOWNSTREAM CONDITIONS THAT FALSIFY THE CLAIM: (F1) `defer` after an `unverified` FAIL gives PASS (INV-001). (F2) A refuse-and-rerun loop never reaches ESCALATE in code (INV-002). (F3) A second `revise` run corrupts spans and can mark an untouched row `resolved_check` (INV-006). (F4) A quorate panel with one reviewer's blocking line dropped as invalid gives PASS (branch 1). (F5) At review 1 every reviewer returns a valid EMPTY block: v1 treats an empty block as valid (`document_review_loop_prompts.md:58`; `parse_block` sets `ok` True with no findings, `findings.py:124-196`), while v2 requires a coverage observation per assigned row (`findings_v2.py:291-297`). Nothing in the consensus supplies that for v1, so a skimming panel can certify round-1 PASS. (F6) Version skew: an older installed `superclaude` continuing a new-key ledger ignores `degraded`, `unverified` and sticky blocking (INV-014).
SUGGESTED RESOLUTION: Restate the claim in the merged proposal as "no PASS and no clear without a positive, script-checked signal on the recorded-round path, given INV-001..009 closed", and list F4 to F6 as accepted residual risks with owners (C01 for F5, C05 hook for F4). Add a path-closure test that enumerates every writer of `status` and `blocking` and asserts each one is gated.

---

ID: INV-011
CATEGORY: interaction_effects
ASSUMPTION: Sticky blocking (`row["blocking"] = row["blocking"] or current`) is safe to apply at the one site where the bit is written today.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The write at `ledger.py:216-218` also takes input from reviewers with an INVALID block: `merge_round` keeps their parsable findings (`:127-139`, docstring `:111-113`). With sticky blocking, one partial reviewer's blocking finding becomes permanent, and the only exits are `defer` or an ESCALATE at the cap. The transcript leaves C05 open ("unless the C05 decider says otherwise"): if the decider hook runs at this site, order matters (sticky first or decider first), and the decider cannot un-block without a rule that overrides sticky.
SUGGESTED RESOLUTION: Make sticky depend on `members` from valid blocks only (a blocking call from an invalid-block reviewer opens the row but marks it `provisional`). State the order: decider output is the input `current`, sticky is applied after it, and an un-block goes through a named, logged action (`unblock` event with reason), never through a re-find. Tests: partial-reviewer blocking line; decider un-block with and without the event.

---

ID: INV-012
CATEGORY: state_variables
ASSUMPTION: "Frozen row identity" (consensus item 3) can sit next to A's re-find path, which rewrites row fields.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: On a re-find `merge_round` rewrites `anchor`, `anchor2`, `span`, `span2` (`ledger.py:224-231`) but not `claim` (`:199` sets it once; `:208-234` never updates it), `fp` (`:186`) or `category`. A 3-line neighbour match (`findings.py:377`) therefore moves the row's span to the neighbour defect, leaves the old claim, and the merged report prints the stale claim under the new anchor (`ledger.py:459-466`, `:473`). Section-number drift after a revision can also break the fp test (`findings.py:371`), since fp is computed on the text at creation. If "frozen" means anchor and span are fixed, the `map_span` updates (`:343-346`) and the re-anchor comment ("a mapped span can point at the start of a longer replacement", `:224-225`) stop working.
SUGGESTED RESOLUTION: Define the field classes: frozen = `lid`, `claim_origin`, `anchor_origin`, `fp`, `category`; mutable = `span`, `span2` (via revise mapping only), `status`. Keep the current claim and anchor in `last_seen: {round, claim, anchor}`. A re-find within the 3-line rule should NOT overwrite `span`; it adds an `adjacent_refind` member. Pin with the characterization test from consensus item 3.

---

ID: INV-013
CATEGORY: interaction_effects
ASSUMPTION: The sweep can be "wired into the decision" with a visible non-PASS on lenses with the sweep off (consensus item 5) without touching the CLI contract.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `ledger_cmd.py:13` defines `EXIT_BY_DECISION = {"PASS": 0, "REVISE": 10, "ESCALATE": 11}` and `:109` does `sys.exit(EXIT_BY_DECISION[v["decision"]])`. Any new decision string (a PENDING or sweep-required value like B's exit 12) is a `KeyError` traceback (exit 1). `_decision` (`ledger.py:93-96`) returns only PASS, REVISE or ESCALATE. The `merge` command exits 0 whatever the decision (`merge_cmd.py:117-118`), so consumers read the JSON. The prompt (`document_review_loop_prompts.md:70`) names no exit codes, so older coordinator text treats an unknown exit as failure.
SUGGESTED RESOLUTION: Add the new decision values and their codes in one table shared by `ledger.py` and `ledger_cmd.py`, with a test that every value `_decision` can return has an exit code. Prefer a non-PASS expressed through ESCALATE with a `reason` field (no new exit code) unless the owner wants PENDING.

---

ID: INV-014
CATEGORY: interaction_effects
ASSUMPTION: Additive keys under an unchanged `review-ledger/1` are safe because old ledgers load and old readers ignore new keys.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `load` accepts any dict whose `schema` equals the string (`ledger.py:47-48`). An older `superclaude` binary (pipx install versus the worktree is a normal skew) reading a new ledger will run the old `merge_round`: it clears on silence (`:254-258`), un-blocks on a re-find (`:213-218`), ignores `degraded` and `unverified`, and writes rounds without the new keys. The new invariants are then silently off while the file still looks valid. B's schema bump would fail closed here; A's additive choice fails open.
SUGGESTED RESOLUTION: Add `min_writer: "<feature id>"` (additive). New code refuses to append a round to a ledger whose `min_writer` it does not know, and writes `min_writer` on every save. Document that old binaries cannot be stopped, so `review merge` prints the writing version into the merged report header and the coordinator prompt compares it. Test: a new-key ledger carries `min_writer`, and an old-shape ledger without it still loads (the HEAD fixture).

---

ID: INV-015
CATEGORY: count_divergence
ASSUMPTION: Cap 3 reviews equals 2 fix cycles, a refused round consumes no review number, and a degraded or `unverified` FAIL consumes one, so numbering stays consistent.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `expected = len(rounds)+1` (`ledger.py:114-118`) and `_decision` `n < cap` (`:93-96`) give the arithmetic. Divergence points: (a) An `unverified` FAIL at review 2 burns the second fix cycle on an empty brief (INV-005). (b) A degraded FAIL at review 1 loses 1 of 3 reviews on a partly seen document, and the re-review then resolves one reviewer (`panel.py:600-616`, `apply_to` is `first`), which may be the very reviewer that truncated. (c) `--cap` default `None`: an explicit `--cap 3` on a ledger already at 3 must NOT be a conflict, and cap 1 or 2 must be tested (cap 1 means round 1 FAIL gives ESCALATE at once, `:96`). (d) `merge_round` accepts a new round after a terminal PASS or ESCALATE, as long as `n == len+1` and `n <= cap`; for instance a round 3 after a PASS at round 2 overwrites the outcome (`:114-118` is the only guard). (e) The header number the reviewer writes comes from PRIOR (`document_review_loop_prompts.md:45`) while `--round` is coordinator-typed; no code compares them.
SUGGESTED RESOLUTION: Specify `--cap` equality as no conflict. Refuse a merge after a recorded PASS or ESCALATE. Compare the reviewer's `review: N of cap` header to `--round` and warn. Add boundary tests for cap 1, 2, 3 with a refusal at `n == cap`.

---

ID: INV-016
CATEGORY: collection_boundaries
ASSUMPTION: Quorum `min(2, panel_size)` behaves for panels of 1, 2 and 3, and "degraded" has one meaning.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Panel 1: quorum 1; fine. Panel 2: quorum 2, so one truncated reviewer means no PASS; consistent. Panel 3: quorum 2, so 2 valid empty blocks plus 1 invalid reviewer is quorate. The invalid reviewer's dropped line can be a BLOCKING finding (`findings.py:188-192` skips it, `ledger.py:130-134` only warns). The transcript says degraded is "recorded" but not whether degraded means `valid < quorum` or `valid < panel_size`; a PASS with 2 of 3 valid is the silent case. Row count: zero rows plus all-valid empty blocks is PASS (see F5 in INV-010).
SUGGESTED RESOLUTION: Define `degraded = valid < panel_size`, `quorate = valid >= quorum`, and record `valid`, `panel_size`, `quorum`, `dropped_lines`. A would-be PASS with `degraded` and `dropped_lines > 0` for any reviewer is refused (re-run that reviewer); a quorate FAIL is accepted. Tests for 1, 2 and 3 with each combination.

---

ID: INV-017
CATEGORY: collection_boundaries
ASSUMPTION: Every `resolved_check` row is one a reviewer was asked to answer, so the gate (a prior line per row) is satisfiable.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `apply_revision` moves any `open` or `regressed` row named `applied` to `resolved_check` and does not check `blocking` (`ledger.py:328-339`). The reviewer is told to answer "one prior line per prior blocking finding id" (`document_review_loop_prompts.md:49,61`), and the reviser's fix map is "one line per blocking id in the brief" (`:66`). A reviser line naming a non-blocking row, or a row that stopped being listed, creates a `resolved_check` row nobody is asked about, so the "any uncleared `resolved_check` row" rule fails every would-be PASS for it. Many prior rows (15 or more): one omitted prior line costs the whole PASS and one of the 3 reviews.
SUGGESTED RESOLUTION: Gate only on rows that were blocking when moved to `resolved_check` (store `blocking_at_fix`). Move non-blocking rows named `applied` straight to `resolved` with a `non_blocking_fix` event, or refuse the line. Clear rows answered, keep only the missing ones in `unverified`, and list them in the next merged report (INV-005).

---

ID: INV-018
CATEGORY: state_variables
ASSUMPTION: Phase ordering and snapshot hashes (consensus item 3) make the merge, revise, merge sequence mechanically checked.
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Consensus item 3 names "snapshot hashes and phase ordering as additive integrity keys". Today only `rounds[-1].doc_sha256` exists (`ledger.py:279`, used at `:308-314`). The consensus names the keys but not the rules, so the pin tests must say what is refused: merge before a revise, a second revise for the round (INV-006), a merge whose doc hash differs from the revised text, a merge after a terminal decision (INV-015).
SUGGESTED RESOLUTION: (ADDRESSED in principle.) The merged proposal should list those four refusals as acceptance tests rather than leave "phase ordering" undefined.

---

ID: INV-019
CATEGORY: state_variables
ASSUMPTION: A refused or retried merge leaves the ledger and the merged report consistent, and a coordinator retry after a lost response is harmless.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: `merge_cmd.py:113-116` writes `--out` BEFORE `led.save`; a failure in `save` leaves a merged report whose verdict the ledger does not contain. The CLI has no lock (a second concurrent merge or revise loads the same file, then last write wins; B had a lock, the consensus does not carry it). A successful merge whose output was lost, then retried, hits "the ledger expects round n+1" (`ledger.py:114-118`), which the coordinator cannot tell from a real refusal and which would count toward the bounded refusal in INV-002.
SUGGESTED RESOLUTION: Save the ledger first, then write `--out` (or write both to temp files and rename). Make a replay of identical inputs (same report hashes, already recorded in `entries[].report_sha256`, `ledger.py:146`) return the stored result instead of an error. A lock is optional; say so.

---

ID: INV-020
CATEGORY: state_variables
ASSUMPTION: Atomic refusal is implemented by checking or copying before mutation (consensus item 2).
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Consensus item 2 and Round 2 A "Fixes A needs" item 1. Mutation points confirmed: `ledger.py:204` (append row), `:209` (extend members), `:232` (history), `:254-258` (clear), verdict at `:273-275`, round appended at `:276`. One implementation trap: `merge_cmd.py:109-110` passes the same `ledger` object to `render_merged_report`, which reads `ledger["rounds"]` with a bare `next(...)` (`ledger.py:412`). If `merge_round` works on a deepcopy and does not hand the copy back or write it into the caller's dict, rendering raises `StopIteration`.
SUGGESTED RESOLUTION: (ADDRESSED in principle.) State that `merge_round` commits by `ledger.clear(); ledger.update(work)` (or returns the new dict and the CLI uses it), and add an in-memory test that calls `merge_round` directly: a refusal leaves `ledger == deepcopy_before`, a success leaves the round in the caller's object.

---

## DONE / NEXT

| Status | Result |
|---|---|
| DONE | 20 findings written; 18 UNADDRESSED (INV-001 to INV-017, INV-019), 2 ADDRESSED in principle (INV-018, INV-020); INV-010 is the always-on sufficiency challenge with a source enumeration. |
| NEXT | The merged proposal should absorb INV-001 to INV-009 before the first step ships; none needs a design change to the consensus, only added rules and tests. |
