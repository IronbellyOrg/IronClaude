# Round 2.5 invariant probe, raw findings: slot C-03 merge-verdict-policy-and-quorum

Agent: fault-finder (not an advocate). Inputs read: diff-analysis.md, round1-advocate-A.md, round1-advocate-B.md, round2-advocate-A.md, round2-advocate-B.md. Code read this session: `src/superclaude/cli/review/{ledger,merge_cmd,ledger_cmd,panel,panel_cmd,manifest,findings}.py` (parts), `src/superclaude/cli/reflect/models.py:25-65`, `src/superclaude/rules/prompts/document_review_loop_prompts.md:55-75`, `tests/review/test_review_ledger.py`, `tests/review/test_review_cli.py`, `tests/skills/test_review_brief_placement.py`, `Makefile` (verify-sync block). Transcript tags: A-R1/A-R2 = round1/round2-advocate-A.md, B-R1/B-R2 = round1/round2-advocate-B.md. Nothing under the forbidden task folders was read. Research files under `research/` were not opened; claims that rest only on a transcript are marked "(transcript)".

---

ID: INV-001
CATEGORY: state_variables
ASSUMPTION: A refusal that "records nothing" is free: the cap is not consumed, the ledger is untouched, and the measurement plan (consensus item 7: reviews-to-cap, escalate-at-cap rate, floor falsifier) can still be computed.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `merge_cmd.py:109-116` writes the merged report and calls `led.save` only after `merge_round` and `render_merged_report` succeed; `test_review_cli.py:447-449` pins `not ledger.exists() and not out.exists()` for the zero-valid refusal; `test_review_ledger.py:345-361` pins an unchanged ledger. So a quorum refusal leaves no durable trace anywhere except stdout and the exit code. Consequences: (a) the refusal rate, the number of retries per round and the share of rounds that needed a retry cannot be measured from stored ledgers, yet item 7 needs "the floor falsifier" and the A-R2 bullet 11 measure "reviews-to-cap"; (b) the retry bound is prose only, which B-R2 (bullet 5 and New evidence 6) admits, but nobody notes that the bound is also unobservable after the fact; (c) the dispatch cost of refused rounds sits outside `cap_reviews` (`ledger.py:93-96` uses only `n`), so the cap no longer bounds reviewer spend. Transcripts cover the unbounded-retry prose (B-R2) but not the loss of evidence.

---

ID: INV-002
CATEGORY: state_variables
ASSUMPTION: After exit 12 the coordinator state is unambiguous: "stop, re-run the missing reviewers once, then escalate"; no other artifact says otherwise.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: (1) `ledger.verdict()` returns the stored last round (`ledger.py:363-372`) and `apply_revision` never rewrites that stored verdict or its `brief_ids` (`ledger.py:301-347`). After a refusal at round k+1, `ledger verdict` therefore prints round k's REVISE and exits 10 (`ledger_cmd.py:94-109`) although the rows have already moved to `resolved_check`. (2) At the cap this is wrong in a worse way: if the cap-th review (n = cap) is refused, the stored decision is the previous round's REVISE (`_decision`, `ledger.py:93-96`), never ESCALATE, so a reader of `ledger verdict` sees "another fix cycle" where the loop prose says escalate. (3) In round 1 a refusal saves no ledger (`merge_cmd.py:100-116`), so `ledger verdict` fails in click's `exists=True` check (`ledger_cmd.py:95-100`), a different failure from round 2. (4) `--out` is written only on success (`merge_cmd.py:113-116`); a coordinator that reuses one output path across rounds (the tests use per-round names, `test_review_cli.py:210, 276`, but the prompt at `document_review_loop_prompts.md:70` fixes no names) reads a stale merged report ending in `verdict: FAIL`. The prompt says the merged report and the ledger "give the verdict and the Reviser brief ids" (`:70`); after a refusal neither is current. B-R2 (bullet 5) avoided a `decision` key because `ledger verdict` would show the previous decision, which shows the hazard was seen, but the consensus adds only "exit 12, prose" and no rule telling the coordinator not to consult `ledger verdict` after a refusal. The `revise` sha check (`ledger.py:308-314`) incidentally stops a blind second fix cycle with exit 1, which is luck, not design.

---

ID: INV-003
CATEGORY: state_variables
ASSUMPTION: "In a `degrade` profile `complete >= min(2, requested)`" has a defined initialization: the profile, `min_complete` and `requested` reach `merge_round` from somewhere stable.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `merge_cmd.py:21-70` has no profile, quorum or min-complete option; the only persisted policy value is `cap_reviews`, fixed at round-1 creation (`ledger.py:37-38`, `merge_cmd.py:64-70`, "Review cap used when round 1 creates the ledger"). `merge_round(ledger, doc_text, n, reviewers)` (`ledger.py:107`) has no parameter for `requested` or a profile, yet the consensus puts the gate inside `merge_round` (item 2) while computing `requested` from `--resolution` in the CLI. Open points: (a) if the profile is a per-call CLI flag it can differ between rounds of one ledger and, unlike `cap`, is not persisted; if it is hard-coded to `degrade`, then "profile" is vestigial because reflect never calls `review merge` (it uses `derive_verdict`), so `visible` is selectable by nobody in this command; (b) the default of a new `requested` parameter is unspecified: `requested=None` meaning "gate off" leaves the 24 direct `merge_round(` call sites in `tests/review/test_review_ledger.py` (grep count 24) and any library caller ungated, while `None` meaning `len(reviewers)` would make `test_review_ledger.py:382` a refusal (the rewrite item 6 expects) and nothing else. Transcripts name the profile field (A-R2 bullet 3) and the CLI source (B-R2 bullet 3) but never say which layer owns the default.

---

ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: A present `--resolution` file is accurate and current, so `requested = max(len(resolution.reviewers), len(--report))` measures the panel that was dispatched for this round.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `merge_cmd.py:73-83` reads only `reviewer_id` and `model` from the file; it does not look at `review_kind`, `run_id` or `template_sha256`, all of which `panel.resolve` writes (`panel.py:688-699`). The kind decides the size: a re-review resolves only the fixed slots (`panel.py:600-605`, `count = ... else 1` at `:616`), and the loop prompt tells the coordinator to resolve with `--kind first|re-review` (`document_review_loop_prompts.md:70`). Two failures: (a) a first-kind resolution passed with the one report of a by-design single-reviewer re-review inflates `requested` to the first-panel size, so `complete 1 < 2` refuses every retry (fail-closed livelock; the cap is not consumed, so only prose ends it); (b) a smaller or unrelated resolution (or only one `--report` with a stale resolution) deflates `requested` and bypasses the gate. The existing round-trip test passes a first-kind resolution in round 1 and none in round 2 (`test_review_cli.py:204-228, 277-290`), so no test exercises the wrong-kind pairing. The consensus makes "always pass `--resolution`" mandatory (item 2) and so makes this input load-bearing, but no transcript proposes binding it to the ledger or to the round (for example round 1 must carry kind `first`, later rounds kind `re-review`, run_id stable across rounds).

---

ID: INV-005
CATEGORY: guard_conditions
ASSUMPTION: Counting `complete` reviewers counts distinct, genuine reviewers of the panel (the consensus checks "reviewer ids unique" only).
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The only uniqueness guard is on ids in one call (`ledger.py:119-121`, raises `LedgerError("duplicate reviewer id in one round")`). Not checked: (a) `--report` ids absent from the resolution (`models.get(rid)` just yields `None`, `merge_cmd.py:94`; a typo or an id from another run counts as a complete reviewer); (b) two ids pointing at the same file or identical text (`report_sha256` is computed, `ledger.py:146`, and never compared), so one valid empty report under two ids satisfies a floor of 2; (c) duplicate ids inside the resolution, which collapse silently in the `models` dict (`merge_cmd.py:76-79`) while `len(resolution.reviewers)` would still count them; (d) a report written for an earlier round or another document version: the header line `review: n of cap` is not parsed (`parse_block` reads only the findings block, `findings.py:124-196`; the test helper writes a constant `review: 1 of 3`, `test_review_ledger.py:45-50`), and the "pass all reports again plus the replacement" retry advice (A-R2 bullet 5, B-R2 bullet 5) makes reuse of report files across attempts the normal path. A-001 (transcripts) asks whether `complete` means examined; this finding is narrower: it asks whether `complete` means distinct and current. Not addressed in either round.

---

ID: INV-006
CATEGORY: guard_conditions
ASSUMPTION: Consensus item 1 states the union as "any complete reviewer's blocking flag on an open/regressed row fails the round", and that statement matches what `merge_round` does.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: `ledger.py:127-138` appends every finding that `parse_block` could parse to `all_findings` whether or not that reviewer's block was `ok`; the docstring says so ("A reviewer with an invalid block is skipped for clearing but its parsable findings are kept", `:112-113`). A reviewer with one malformed JSON line among ten valid findings is `ok=False` (`findings.py:163-170`) yet its blocking findings create rows and fail the round (`:184-187`, `:273-275`) and its refound rows are not cleared (`:254-258`). So the shipped union is "any parsable blocking finding", wider than "any complete reviewer". Three risks: (1) fail-open if an implementer follows the consensus text and filters findings by `block_ok`: a partial panel's invalid reviewer would stop failing rounds; (2) no test pins the kept-findings behaviour (the only mixed-validity test, `test_review_ledger.py:376-385`, asserts `block_ok`, warnings and `L1 resolved`, not that an invalid reviewer's finding is kept; it is also the test the consensus rewrites, so the behaviour loses its only incidental coverage); (3) the measurement arms (item 7: "union", "union minus span-null rows") replayed from stored E2 data will be computed from whichever definition the replay script uses, and the consensus text and the code disagree. Also, with refuse-then-retry, a replacement reviewer id that does not re-pass the old broken report drops that report's parsable blocking finding, which the pre-change merge would have kept. No transcript mentions invalid reviewers' findings under the union (A-R1 and B-R1 discuss only quorum counts).

---

ID: INV-007
CATEGORY: count_divergence
ASSUMPTION: `len(resolution.reviewers)` is the dispatched panel size, so `requested` can only be understated by a caller that omits reports.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: `panel.resolve` skips a non-fixed slot that has no model left (`panel.py:636-656`, `continue` without appending to `reviewers`) and records it only in `skipped_slots`, which is written only when an exclusion flag was used (`panel.py:700-706`). Those flags are shipped (`panel_cmd.py:53-63`: `--hard-exclude-class`, `--strict-distinct`; passed at `:93-103`). A template with a fixed anchor plus three other slots, resolved with `--strict-distinct` or a hard-excluded class, can yield `reviewers` of length 1 (a fixed slot failure is fatal, `:647-649`, so at least the fixed ones remain). Then `requested = max(1, len(--report)) = 1`, `min(2, 1) = 1`, and one valid empty block certifies PASS for a first review that the template meant as a panel: the D-2 shape, with no caller mistake. The manifest already models the difference: `reviewers_requested` >= `reviewers_resolved` (`manifest.py:307-316`), and the consensus's `requested` equals the manifest's `resolved`. A-R2 (New evidence 4) lists `skipped_slots` as a source and flags "whether `reviewers` equals the dispatched count" as UNVERIFIED; the consensus text (item 2) drops `skipped_slots` from the formula. Related numerator divergence: ledger `complete` = parse-ok per file; manifest `reviewers_complete` counts the caller-declared `completion == "complete"` of the latest `collected` attempt (`manifest.py:269-274`); the two can disagree (manifest says 3, merge says 1) and nothing reconciles them (A-R2 bullet 4 calls the manifest "a cross-check", the consensus does not).

---

ID: INV-008
CATEGORY: count_divergence
ASSUMPTION: `min(2, requested)` behaves sensibly at requested = 1, 2, 3, 4 and the floor is inclusive.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: Enumeration from the formula `complete >= min(2, requested)`: requested 1 gives floor 1 (single reviewer, includes by-design re-review); requested 2 gives floor 2 (zero failures tolerated); requested 3 gives floor 2 (one failure tolerated, matches the pinned 2-of-3 reflect behaviour, `test_ensemble_stub_integration.py:199-221` per A-R1/B-R1); requested 4 gives floor 2 (two failures tolerated). So tolerance is not monotone in panel size (a 2-reviewer panel is stricter than a 3-reviewer panel) and the `max(...)` in `requested` changes the result only at the 1-versus-2 boundary, because every value above 2 gives the same floor. The comparison is inclusive in the consensus text and the test matrix (item 6) covers N=1..5. Transcripts address this: A-R1 K4 (floor 2 makes the reflect carve-out mostly moot), A-R2 bullet 3 and consensus item 7 (floor declared unmeasured, with a floor falsifier). Residual only: the matrix should assert the non-monotone tolerance explicitly so a later change to a proportional floor is a visible test failure.

---

ID: INV-009
CATEGORY: count_divergence
ASSUMPTION: A round that meets the floor but not `requested` (for example 2 complete of 4 requested) is acceptable as an ordinary PASS because "no new row columns or render change" keeps the artifact stable.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `render_merged_report` prints `panel of {len(rnd['reviewers'])} reviewers` and lists only the reports that were passed (`ledger.py:415-424`). A 4-requested, 2-complete, 2-absent round is rendered as "panel of 2 reviewers", with `verdict: PASS` (`:493`); `requested`/`complete`/`quorum` exist only as new JSON keys in the round entry (consensus item 3) and in no artifact the Reviser, the next reviewer or the user reads. The union loses the only visible shortfall signal in exactly the case where the consensus chose not to refuse. The original A design said "DEGRADED, never PASS" for `complete < requested`; the consensus narrowed that to a floor, so everything between the floor and `requested` is silent. The advocate who wanted no render change (B-R2 bullet 2 point 3) argued against flag columns; the transcripts do not weigh a one-line header showing `complete` of `requested`. If a header change is rejected because the table header is pinned (`test_review_ledger.py:451`), the header line at `:417` is a separate pin (`:447`, "panel of 2 reviewers") that would also have to be rewritten, which is a cost to state, not a reason to hide the shortfall.

---

ID: INV-010
CATEGORY: collection_boundaries
ASSUMPTION: The test matrix "N=1..5 x five completion states" (consensus item 6) can be run against the code that is being changed.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `merge_round` receives only `{reviewer_id, model, report_path, text}` and derives one boolean per reviewer from `parse_block` (`ledger.py:127-130`); `truncated` and `invalid` both become `block_ok=False`, and `failed`/`timed_out` have no input at all (`COMPLETION_STATES` has five values but `parse_block` yields three and the rest "are for callers", per A-R1 K3 citing `findings_v2.py:39-40`). At the CLI, a reviewer with no file cannot even be passed: `_read` raises `ClickException` (exit 1) for an unreadable path (`merge_cmd.py:13-18, 96`), so the same operational condition "a reviewer produced nothing" yields exit 1 when its path is passed and nothing at all when it is omitted, while "invalid" yields 12. The matrix can therefore only distinguish valid / invalid-file / absent-from-`--report`. B-R2 (bullet 3) notes that failed and timed_out "collapse into absent"; the consensus item 6 still states five states and nobody says whether `--report` gains a state suffix or the matrix is restricted to three input states. Also relevant for boundaries: an empty `--report` list cannot occur (click `required=True, multiple=True`, `merge_cmd.py:43-49`); all-invalid (zero valid) is already a refusal (`ledger.py:150-157`, `test_review_cli.py:425-449`) and the consensus moves it to exit 12 while the pin at `:448` asserts the message text "no reviewer produced a valid findings block", which the new refusal JSON (`{"refusal":"quorum_shortfall",...}`) does not contain, so the message must stay in the output or the pin is rewritten (B-R2 bullet 6(a) assumed it stays).

---

ID: INV-011
CATEGORY: interaction_effects
ASSUMPTION: The union is on the cheap-error side once precondition item 5 is stated ("to the cap, then a human decision").
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Verified trace: a Reviser `rejected` fix-map item only appends `rejected_by_reviser` and leaves status `open` (`ledger.py:340-342`); `apply_revision` skips non-open/regressed rows (`:328-329`); only `resolved_check` rows clear at merge (`:254-258`); an open row not refound is re-presented every round (`:457-466`) and stays in `_brief_ids` (`:99-104`); the only exit is the human `defer` (`:350-360`). Addressed in A-R2 (R1, bullet 8) and B-R1 (Strength 5), B-R2 (bullet 8, noting `prior` notes cannot clear, `ledger.py:259-272`). Residual that the consensus wording does not carry: the cost now stacks with INV-001, because refusals do not consume the cap while false-blocker fix cycles do; and the precondition is a stated dependency on slot C-02, not a gate: nothing in code or tests fails if the union default ships before C-02 does.

---

ID: INV-012
CATEGORY: interaction_effects
ASSUMPTION: Under refuse-and-record-nothing, `defer` has nothing to lift for the quorum dimension (A-R2 R7), so the stored-verdict pin and the quorum gate do not interact.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: `defer` rewrites the last stored round to PASS/PASS when its `brief_ids` empties (`ledger.py:356-360`), pinned by `test_review_ledger.py:396-405`. After a revision and a refused re-review, the last stored round still lists the blockers the Reviser already fixed (`apply_revision` does not edit `brief_ids`, `ledger.py:301-347`). The consensus escalation path for a persistently failing reviewer is "escalate to the user"; the user's only command that produces a stored PASS without a quorate review of the revised document is `defer` on the stale brief ids. So `defer` is the single non-quorate route to PASS, reachable exactly when quorum keeps failing. It is a recorded human act (`reason` goes to history, `:355`), so this is visible, not silent; the transcripts discuss `defer` only for derive-on-read and `pending` (A-R2 R7, B-R2 W2), not as the escalation exit of the quorum gate. Kept LOW because the pin and the human decision are existing behaviour; the consensus should state it.

---

ID: INV-013
CATEGORY: interaction_effects
ASSUMPTION: Updating "both copies" of the loop prompt keeps the mirror in sync and `make verify-sync` will catch drift; the prompt change reaches every caller.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: The two copies are byte-identical today (`diff -q` exit 0). `make verify-sync` compares only Skills, Agents, Commands, Hooks and Templates (the five `echo "=== ... ==="` sections of the target at `Makefile:166` onward); it does not compare `rules/prompts` or anything under `plugins/`. The drift guard is a pytest, `test_plugin_bundles_the_rules_file_and_the_gate_falls_back_to_it`, which asserts `bundled.read_bytes() == RULES_FILE.read_bytes()` (`tests/skills/test_review_brief_placement.py:128-134`). So drift is caught by the test suite, not by `verify-sync`, which matters only to anyone who relies on `verify-sync` alone. Larger gap: the prompt is read from the installed `~/.claude/rules/prompts/document_review_loop_prompts.md` (`test_review_brief_placement.py:21-22`), refreshed only by `superclaude install`. A new CLI with exit 12 plus an old installed prompt (no `--resolution`, no exit-12 sentence) is the normal state until reinstall, and the whole D-2 closure beyond `len(--report)` depends on the prose reaching those installs. A-R2 and B-R2 name both copies but neither mentions install skew. Exit vocabularies: reflect uses 0/10/11/2 for pass/halted/degraded/blocked (`cli/reflect/models.py:44-49`), `ledger verdict` uses 0/10/11 for pass/revise/escalate (`ledger_cmd.py:13`), and `merge` adds 12; avoiding a clash with reflect's 10/11 is covered in A-R1 (strength 4) and A-R2 (bullet 6), but a consumer that handles both products must still map 11 to two meanings.

---

ID: INV-014
CATEGORY: sufficiency_challenge
ASSUMPTION: The merge-time refusal ALONE closes the reproduced D-2 defect (one valid empty block of N PASSes).
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Inline source enumeration of every gate between `merge` input and a PASS verdict, with whether the consensus refusal stops the D-2 shape at that gate:
1. `merge_cmd.py:43-49` `--report`: required, repeatable; one `ID=PATH` per reviewer. No state, no completeness. Not a gate for D-2.
2. `merge_cmd.py:50-56, 73-83` `--resolution`: optional; supplies models only today. Under the consensus it supplies `requested` (INV-004, INV-007 show it can be wrong).
3. `merge_cmd.py:84-98` + `:13-18` report reading: a missing path aborts with exit 1, so failed/timed_out reviewers can never appear as reports (INV-010).
4. `ledger.py:114-121`: round-number and duplicate-id guards only (INV-005).
5. `ledger.py:127-138` `parse_block` validity: `ok=True` for any closed `findings-v1` block whose lines parse, including an empty one (`findings.py:134-196`; the loop prompt says "A report with no finding has an empty block", `document_review_loop_prompts.md:58`). Validity is format, not examination.
6. `ledger.py:150-157` zero-valid refusal: stops only complete = 0. The consensus quorum extends this to `complete < min(2, requested)`.
7. `ledger.py:165-257` clustering, matching, and `resolved_check` clearing (`:254-258`): a row clears when no reviewer in the round refound it. Two valid empty blocks (floor 2) clear every `resolved_check` row.
8. `ledger.py:273-275` verdict: `PASS` iff `_brief_ids` is empty (`:99-104`).
9. `ledger.py:276-285` round recorded; `merge_cmd.py:113-118` report written, ledger saved, JSON printed, process exits 0 whatever the verdict.
10. Consumers of `decision`: `ledger_cmd.py:109` and the loop prose (`:70`); nothing else in `src`, `plugins`, `scripts`, `docs` (A-R2 grep, transcript).
Result: the refusal closes exactly "complete < floor". The same defect class survives at complete = floor: 2 valid empty blocks of 4 requested clear `resolved_check` rows and give PASS. That is shared assumption A-001, which both R1 papers answered QUALIFY ("necessary, not sufficient", A-R1, B-R1) and the consensus defers to a seeded-defect control (slot X-14). So ADDRESSED as a limit, but the consensus sentence "closes the reproduced D-2 defect" should say "closes it for exactly one valid block of two or more requested; a floor-sized set of empty blocks still passes".

---

ID: INV-015
CATEGORY: sufficiency_challenge
ASSUMPTION: "An old caller fails closed on exit 12."
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Enumeration of old-caller behaviours after a refusal: (a) a caller that checks exit status treats 12 as a failure, so it never proceeds on PASS: holds. (b) A caller that ignores `merge` status and then runs `ledger verdict`: round 1 gives click usage error because no ledger file exists (`ledger_cmd.py:95-100`); round 2+ gives the previous round's stored REVISE, exit 10 (INV-002), so it is non-PASS but stale; a blind second fix cycle is then stopped by the `--old` sha check at `ledger.py:308-314`. (c) A script that parses the stdout JSON for `decision` finds the refusal object has no `decision`, `verdict` or `brief_ids` keys (consensus item 2); no such script exists in `src`, `plugins`, `scripts` or `docs` (A-R2 R6, transcript; coordinators that are models are not testable here). (d) A caller on an installed old prompt never sees the exit-12 sentence (INV-013). Fail-closed with respect to PASS holds on every enumerated path; fail-closed with respect to a correct next step does not (INV-002). A-R2 (R6, bullet 6) and B-R2 (bullet 6) address "any non-zero code is non-PASS", and the unverified part (how a model coordinator treats an unknown code) is acknowledged by A-R2 R6. Status ADDRESSED for the PASS claim only.

---

ID: INV-016
CATEGORY: sufficiency_challenge
ASSUMPTION: No LLM stage is needed because the union is deterministic (consensus item 1), so the verdict is a pure function of the rows.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: `merge_round` is deterministic given its inputs, but "deterministic" is not "correct": the rows it unions over come from two unmeasured steps. (1) Reviewer-typed `blocking` (slot C-02, acknowledged). (2) Defect identity: a new cluster matches an existing row when `fnd.same_defect(m, _view(row))` holds (`ledger.py:165-170`), using mapped spans, fingerprints and refs. A match to a row with status `deferred` adds members and sets `row["blocking"]` but leaves `status` `deferred` (`ledger.py:207-238`: only `resolved_check`/`resolved` become `regressed`), and `_brief_ids` selects only `open`/`regressed` (`:99-104`). So a new, genuinely distinct blocking defect that `same_defect` mis-matches to a deferred row never fails the round, and no quorum, floor or union rule sees it. The same function decides when a refound `resolved` row becomes `regressed` versus a new row. The transcripts treat the union as the fully specified policy (A-R1 strength 1: "pure function ... exhaustively testable") and test only quorum and monotonicity; neither examines false merges or false splits of clusters, and neither measures `same_defect` precision. This does not argue for an LLM in the merge; it limits the claim: the default is deterministic and fail-closed over rows that may already have absorbed a mistake, and the consensus claims discipline (item 9) should say so.

---

ID: INV-017
CATEGORY: sufficiency_challenge
ASSUMPTION: "`requested` falling back to `len(--report)` closes D-2 for existing callers."
STATUS: ADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Falsifiers by completion state: the fallback sees only reviewers whose report file is passed. `truncated` and `invalid` reviewers have files (counted); `failed` and `timed_out` reviewers have none and, because `_read` raises on a missing path (`merge_cmd.py:13-18, 96`), a coordinator must omit them (not counted). So the four-reports-one-valid-three-broken case closes, the one-report-three-dispatched case does not, and a single `--report` always gives `requested = 1`. Existing callers pass no resolution: `document_review_loop_prompts.md:70` never mentions it (B-R2 New evidence 2; I re-read the line), and the round-trip test passes none in round 2 (`test_review_cli.py:277-290`). Addressed in B-R2 (bullet 4, bullet 12 caveat: "closed for callers that supply reports for every dispatched reviewer; the variant where a reviewer wrote no file is closed only when the coordinator passes `--resolution`") and in consensus item 2 ("must always pass --resolution"). Not carried into the consensus claims item 9: the caveat sentence is missing there. Closure for that variant depends on prose reaching installs (INV-013) and on the resolution being current (INV-004), which is why ADDRESSED applies to the stated caveat only.

---

## Summary

Total findings: 17. Categories: state_variables 3, guard_conditions 3, count_divergence 3, collection_boundaries 1, interaction_effects 3, sufficiency_challenge 4 (the collection_boundaries empty-list, zero-valid and duplicate-id cases are folded into INV-005 and INV-010 and found already covered or pinned).

By status: ADDRESSED 5 (INV-008, INV-011, INV-014, INV-015, INV-017); UNADDRESSED 12.

By severity: HIGH 2 (INV-006, INV-007); MEDIUM 12; LOW 3 (INV-008, INV-012, INV-013).

HIGH + UNADDRESSED: 2 (INV-006: union text says "complete reviewer", code unions every parsable finding, unpinned; INV-007: `requested` taken from `resolution.reviewers` excludes skipped slots, so shipped exclusion flags can collapse a panel to one reviewer and one valid empty block passes).

UNADDRESSED by severity: HIGH 2, MEDIUM 8 (INV-001, INV-002, INV-003, INV-004, INV-005, INV-009, INV-010, INV-016), LOW 2 (INV-012, INV-013).

Not verified by me: research-sourced figures; `cluster.py` and `findings_v2.py` line citations repeated from the transcripts (marked "transcript"); whether a model coordinator treats an unknown exit code as failure.
