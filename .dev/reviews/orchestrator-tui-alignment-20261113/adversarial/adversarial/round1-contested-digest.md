# Round 1 digest: contested points (X and A rows where fewer than 2/3 of advocates name the same winner)

Points: 36; agreed (>=2/3 same winner): 23; contested: 13; convergence over X and A rows: 0.639

Agreed points (winner is stable across advocates; see each round1-advocate-VN.md section 7 for evidence): A-001, A-003, A-006, A-010, A-012, A-014, A-015, A-016, X-001, X-002, X-003, X-004, X-005, X-007, X-010, X-011, X-012, X-013, X-014, X-015, X-016, X-017, X-018

## A-002  (winner tally {'V5': 3, 'V2': 1, 'V3': 1})

- V1 advocate: V5; V1 for the sweep | 80% | Section 6 | State the unit in the contract.
- V2 advocate: V2 | 75% | W-04 | State the unit explicitly and mark Run-less sessions as out of both programs
- V3 advocate: V3 (F4), V5 | 70% | `report.py:619-695`; `startup.tf:57` | Add an identity envelope (workspace id, owner, `gh` login, host) before any cross-workspace read
- V4 advocate: V5, V4 (F3) | 80% | `probes.py:1203-1214`; observer paging | v2 states its unit.
- V5 advocate: V5 | 80% | `adapter.py` templates; SC-10 | State both scopes in the relationship note.

## A-004  (winner tally {'V1': 3, 'V5': 2})

- V1 advocate: V1/V5 | 75% | GraphQL: 2 unresolved threads; `ROW_KEYS` pin | Resolve the two threads; do not add keys inside #539.
- V2 advocate: V1 | 80% | SC-2; PR re-queried | Keep V2 items independent of #539
- V3 advocate: V5, V3 | 70% | two open threads | Log in #534; do not widen #539
- V4 advocate: V5 (D4) | 75% | design `:599`; SC-2 | Do not edit #539 for these; log in #534/#339.
- V5 advocate: V1 | 85% | my GraphQL read; SC-1 | Settle the two threads before any alignment edit touches #539.

## A-005  (winner tally {'V1': 1, 'V2': 1, 'V3': 1, 'V4': 1, 'V5': 1})

- V1 advocate: V1 (V5 agrees for R3/R4) | 85% | Only `PHASE2-preflight-input.md` exists | Give each deferred item a #534 line and an owner.
- V2 advocate: V2 | 65% | #534, PHASE2 reading list | File the machine-started-session label as a #534 row after FU-1
- V3 advocate: V3 (concedes its own), V1, V5 | 75% | `PHASE2-preflight-input.md` is a reading list only | Owner names a tracker per deferred item
- V4 advocate: V4 | 70% | tech ref `:1829`; #444 open | Give each deferred item an issue and owner.
- V5 advocate: V5 | 85% | V5 S10; V1 C-10 | Name one owner per deferred item or label each "unowned".

## A-007  (winner tally {'other': 1, 'V3': 2, 'V4': 1, 'V5': 1})

- V1 advocate: All (unstated) | 85% | V5 S8; sweep reads one user's data | Write it down as a constraint for v2 and #477.
- V2 advocate: V3 (weak) | 65% | `issue-watcher.md:15` | None now; revisit for multi-owner use
- V3 advocate: V3 | 65% | heartbeat `workspace_id`, `owner` | Add a single-owner or multi-owner statement to #477 (owner answers)
- V4 advocate: V4 (F17) | 80% | `probes.py:1344-1350`; V3 F4 | Add the read-permission AC (V4 AC 2).
- V5 advocate: V5 | 75% | pass record; Q-1 FAIL (V5 S8) | Write it down as a stated limit in both designs.

## A-008  (winner tally {'V1': 1, 'V2': 3, 'V5': 1})

- V1 advocate: V1 (sweep); V5 (observer) | 85% | `sweep.md` triggers; `collector.py` | State per program in the contract.
- V2 advocate: V2 | 80% | W-04, W-06 | Name Run-less sessions as a separate blind spot
- V3 advocate: V2, V3 | 80% | V2 W-04; V3 F7 | State in #477 that "orchestrator" is not an address (Edit 8, Q6)
- V4 advocate: V2, V5 | 75% | V2 fact 4; V5 O-09 | v2 says whether Run-less sessions are catalogued.
- V5 advocate: V5 and V2 | 80% | `adapter.py` (`--run` optional); `classify.py:748-767` | Put "machine-started and person-started sessions are not visible to the observer" in the observer HELP or doc.

## A-009  (winner tally {'other': 1, 'V2': 1, 'V3': 1, 'none': 2})

- V1 advocate: All (stated) | 70% | Observer records no Orca version; sweep locks 1.4.245 | Record the Orca version in both golden captures.
- V2 advocate: V2 | 85% | #450 item 1; four `_assumed_shape` fixtures | FU-1 replaces them; record the Orca version in the live-test record
- V3 advocate: V3 | 60% | `main.tf:104-107`; upstream monitor workflow | Include version fields in the envelope
- V4 advocate: none | 60% | tech ref `:446`; V5 | Record Orca and collector version in every v2 fact.
- V5 advocate: none | 60% | V5 O-01, dependency table | Record the Orca version in the observer's golden capture and in the D3 capture.

## A-011  (winner tally {'other': 2, 'V5': 2, 'none': 1})

- V1 advocate: All; none proposes it | 92% | S-006, X-002 | One owner-approved edit pass per issue.
- V2 advocate: V5 | 90% | S-006, X-002 | Apply the #409 edits as one merged pass
- V3 advocate: V5 | 85% | S-006, X-002 | Owner answers the shared questions once; apply edits in dependency order (section 8)
- V4 advocate: diff S-006 | 90% | three rewrites of decision 8 | One ordered edit set (section 8).
- V5 advocate: none | 90% | X-002 | One editor, one merged edit set per issue.

## A-013  (winner tally {'V5': 2, 'V2': 1, 'V3': 1, 'none': 1})

- V1 advocate: V5 | 65% | #409 L66 UNVERIFIED; `projection.attention` unread | Capture live `projection.attention` values (V5 D3) before choosing a source.
- V2 advocate: V2 | 70% | `adapter.py:29-32`; W-04 | Capture `worktree ps` agent rows in FU-1; evaluate an event feed separately
- V3 advocate: V3 | 55% | Claude Code docs "Channels"; V5 O-13 | Note as a possible later alternative; do not research now
- V4 advocate: V5 | 70% | V5 O-13; #423 body | Keep a push or child-report path open in v2's design.
- V5 advocate: none | 62% | `orca-ide orchestration --help` has no stream verb; V3 cites a local WebSocket | Add one read-only check of Orca's event surface to the D3 capture list.

## X-006  (winner tally {'V5': 1, 'none': 2, 'V4': 2})

- V1 advocate: V5 | 75% | `snapshot.schema.json` (observer) vs `report.py:619-695` (sweep); join key `dispatchId` = `row_id` minus `orca:` (`classify.py:891`, re-verified) | Record one relationship note naming both contracts; decide sweep JSON keys in #534 after #539 merges.
- V2 advocate: neither | 60% | O-08, SC-15; V5 D1 | Decide once in #339 after the D1 relationship note; do not edit PR #539 for it
- V3 advocate: V4 (venue), V5 (scope) | 65% | O-08; `test_cli_contract` golden keys | Decide once in #339 via V5's relationship note; V3 Edits 5 and 12 point there, not at #409 item 1
- V4 advocate: V4 (venue), V5 (two contracts) | 65% | design `:599`; `snapshot.schema.json`; V5 O-08 | Write the relationship note first; decide additive keys vs schema v2 in #339 when v2 names its keys.
- V5 advocate: none (V5 reframes) | 68% | V1 W-1; V4 F13; A-014 evidence; PR #539 golden test (SC-1) | Decide sweep-JSON key additions in one place (#339, where the golden test lives) and put the observer-snapshot relationship in the D1 note.

## X-008  (winner tally {'V5': 2, 'V1': 2, 'none': 1})

- V1 advocate: V5 | 90% | V1 verdict vs C-02/F-02; observer shows none of the ten names (V5 RT-F02) | Drop the sentence; replace with the mapping table (observer / sweep / Orca words).
- V2 advocate: V5 | 90% | X-008, RT-F02 | Ignore the V1 verdict sentence
- V3 advocate: V1 (detail) | 90% | same file | Ignore the V1 verdict line; no effect on V3
- V4 advocate: none | 85% | V1 verdict vs C-02, F-02; V5 RT-F02 | Ignore the sentence; use V5's word-mapping table (O-07).
- V5 advocate: V1's tables, not its verdict line | 88% | V1 C-02, F-02; V5 RT-F02 | Ignore the verdict sentence and use F-02 plus V5's three-vocabulary mapping table (O-07).

## X-009  (winner tally {'V1': 1, 'none': 4})

- V1 advocate: V1 is wrong (low impact) | 95% | V1 header: 3 UNVERIFIED listed under "2"; C-08 double-counted | Correct the tally; no decision depends on it.
- V2 advocate: neither | 95% | X-009 | None
- V3 advocate: none | 90% | arithmetic in the tally | None
- V4 advocate: none | 95% | by inspection | None.
- V5 advocate: none | 95% | X-009 text | None needed.

## X-019  (winner tally {'V2': 1, 'V5': 2, 'V3': 1, 'none': 1})

- V1 advocate: V2/V3 on that point | 85% | V2 and V3 make no "observer unbuilt" claim (diff analysis X-019; V3 text: "the observer stays read-only") | None needed beyond not repeating the sentence.
- V2 advocate: V5 (qualified) | 80% | X-019; V2 W-10 text | Reword V2 W-10 as "no watcher panel in `observe` before FU-1"
- V3 advocate: V3 on the claim, V5 on the fact | 75% | V3 text is generic | None; Concession 2 stands
- V4 advocate: V5 (partly) | 85% | V2 W-10; V3 generic text | None; do not repeat the claim.
- V5 advocate: none (V5 slightly overstated) | 85% | X-019 text | Say "V1 stated it; V2 W-10 and V4 F13 assumed it" when citing.

## X-020  (winner tally {'V1': 1, 'none': 3, 'V5': 1})

- V1 advocate: V1 | 90% | No "fleet mode / 50 worker-show / one sweep covers" text in the live body (re-verified, SC-19) | Read it as "do not add V1's W-3"; no body edit.
- V2 advocate: neither | 95% | SC-19 | Read as "do not add V1's W-3"
- V3 advocate: V5 error | 95% | SC-19 | Read as "do not add V1's W-3"
- V4 advocate: none | 90% | SC-19 | None.
- V5 advocate: none (V5 slip) | 90% | SC-19 | Read it as "do not add V1's W-3".

