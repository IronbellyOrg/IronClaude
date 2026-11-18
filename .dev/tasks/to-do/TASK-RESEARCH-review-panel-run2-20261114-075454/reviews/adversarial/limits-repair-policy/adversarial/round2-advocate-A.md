# Round 2 rebuttal: Variant 1 (Proposal A), slot C-06 limits-repair-policy

Advocate: A (normalise before the parser). Focus: correctness, risk, test-coverage. Goes first in Round 2.
Code state: HEAD 50d4d2b9d, branch `ironbelly/shadow-runs`, read-only. E2 data read only through `git show` at `6c0984326`.
Tags: [READ] = I read the file or lines in this session before citing; [RAN] = I executed a read-only command this session; [DOC] = taken from a variant, a Round 1 file or an adjudicated merged text that I read but whose source I did not re-open; [UNVERIFIED] = neither.
"A" = Variant 1, "B" = Variant 2. Round 1 files are `round1-advocate-A.md` (mine) and `round1-advocate-B.md`.

## 0. What I moved on, in one paragraph

I keep the core of A (cut first, in code, inside the parsers, recorded) and I now take four things from B as part of the policy, not as additions: the itemised drop record with a three-valued `blocking_state`, the refusal of a PASS that rests on a lost blocking-or-unknown line (with an owner-and-reason acknowledgement), a first-pass state carried next to the repaired state, and B's measurement discipline (rules written before the run, a line-conservation test). I withdraw three statements of mine: "at most 4 residual lines" (it is a floor, section 3 N3), "C-02 INV-009 is unchanged by A" (A actually removes it for length-only faults, N4) and "the SKILL.md:343 sentence needs one sentence changed" (an additive sentence is enough and a test pins the old text, N7). I demote the copy-to-`refs` rule to a recorded flag. New code reading shows that B's re-ask cannot run in the v1 spec loop without a new pre-merge command, and that every one of the 4 audit-D rows where a lost blocking line produced a PASS was an anchor over 200, so cut-first leaves B's refusal almost nothing to fire on in the study data.

## 1. Response to criticisms

Each item states the criticism in its strongest form first, then the answer.

### 1.1 Variant 2's weaknesses 1-8 of Variant 1

**W1. "A's 88 of 92 recovered, at most 4 residual, is a v1 tasklist derivation and does not size the reflect residual; A's re-ask half is as unmeasured as B's."**
Strongest form: `_check_finding` returns the first fault only, so a by-reason count cannot bound second faults; B's replay finds 30 non-length first faults in 154 invalid lines (19.5 percent, 26 of them category), not 4 in 92; and in E1 four of the five re-asks were for causes truncation never touches (coverage rows outside the slice, citation line numbers counted inside the brief).
Answer: conceded in part, and I corrected the claim by reading the order of checks. [READ] `findings.py:96-118`: id, duplicate, severity, blocking, MINOR-with-blocking, category (`:102`), anchor (`:104`), anchor2 (`:107`), refs (`:111-117`), claim (`:118`). A line whose first fault is anchor or anchor2 can hide behind it only a later `refs` fault (the only non-length rule ordered after the length rules; claim is length and is cut in the same pass). So the residual is "4 plus the length-first lines that also carry a refs fault", which is rare (audit-D has one refs-first line in 92) but not measured. The category failures B's replay finds are checked before the anchor, so they were first faults there; they are absent from audit-D's reasons, and why is [UNVERIFIED] (the replay includes stale and superseded folders). Corrected statement: the residual is at least 4 of 92 on the audit-D population and at least 30 of 154 on B's population. What survives: (i) for the length-first lines the cut recovers without a model call, so the re-ask no longer carries all of them; (ii) in the v1 spec loop, which is where all 92 drops happened, the re-ask is needed for roughly the residual instead of 44 reviewer runs (X-003); (iii) in reflect the residual is mostly non-length and the re-ask is load-bearing for both policies equally. I do not claim a recovery rate for the re-ask; Spike 5 is not run.

**W2. "A's 'exact prefix' is 297 characters plus `...` for claims, and cut anchors, anchor2 and quote carry no marker, so a reviser cannot tell."**
Strongest form: the stored claim is no longer a substring of any line of the hashed report, and the only visible trace of a cut anchor is a `repairs` record that nothing renders.
Answer: conceded on both. [READ] `card_convert.py:199-201` cuts to `MAX_CLAIM - 3` plus `...`, so "exact prefix" holds for anchor, anchor2 and quote and not for claim. The fix is in the render slot C-01 already agreed: the per-row `### Lx` block of `## Blocking findings` prints the anchor status (C-01 merged text, section 2.3 [DOC]); it also prints one line "shortened: anchor 335 to 200, claim 412 to 300" from the `repairs` record. No new table column, so the header pins stay (`test_review_ledger.py:451` per C-03 merged text [DOC]).

**W3. "`repair=True` changes what `block_ok` means: a block that broke the contract now votes to clear and counts toward quorum."**
Strongest form: `ledger.py:129` sets `block_ok = parsed["ok"]`; C-02 B2 makes `block_ok` the only reviewer-quality test on the clearing path and C-03 counts `complete` for the floor; A raises both from blocks that were not valid.
Answer: the objection assumes a length fault means the review did not happen. INV-I is about "a review that did not happen" and its refusal (`ledger.py:150-157`, [READ]) is untouched; after the cut `ok` is still the real parser's verdict on the repaired lines, and any residual fault leaves it False. The cost of the literal semantics is concrete, and I did not state it in Round 1 (N4): it deletes dissent (C-02 INV-009), wastes a review of the cap in a one-reviewer re-review (C-02 B5), and lowers C-03 quorum (at least 7 of 264 audit-D merges sit below a 2-of-3 floor today). The legitimate part of the objection is that the quorum analysis must be able to tell a clean block from a repaired one: the round entry records `repaired` beside `block_ok`, and C-03 may choose to count only `repaired == 0` blocks for its floor (a parameter, default off).

**W4. "Two sources of truth for first-parse state; A names no carrier."**
Strongest form: `findings_block_compliance_rate` has no Python in `src`, the only per-card machine state is `block["state"]` in the two card listings, and with `repair=True` that state reads `complete`.
Answer: conceded in Round 1 and now specified from code (N6): the carrier is two additive keys in the listings, derived exactly without a second parse.

**W5. "The copy-to-`refs` rule contradicts 'touches no field the limits do not name'; it may be dead code."**
Answer: conceded and changed. [READ] `refs_norm` reads `anchor`, `anchor2`, `claim` and `refs` (`findings.py:321-337`), so a token that appears only in a cut tail is a real exposure in principle; B's replay changes `refs_norm` on 0 of 125 lines. Under the ladder (no speculative code) the step now only records `refs_changed: true` in the `repairs` item when `refs_norm(original) != refs_norm(repaired)`. The copy rule is added only if M1 shows a nonzero count. The sentence "touches no field the limits do not name" is then true again.

**W6. "A is silent on a lost blocking line."**
Answer: conceded, and adopted (C-004): B's refusal is part of the merged policy for the residual. The new fact is that under cut-first its fire set in the study data is empty (N2), so it is cheap insurance, not a measured necessity.

**W7. "A's re-ask record claim does not apply to the v1 loop: no manifest."**
Answer: conceded (Round 1 concession 5). For v1 the record is the replacement report passed to the re-run `merge` and its `report_sha256` in that round's reviewer entry; a refused merge records nothing by construction (`merge_cmd.py:109-116` [READ]; the in-memory pin at `test_review_ledger.py:373` [READ]).

**W8. "A's 75 percent kill line is its own, and M2 is not run."**
Answer: accepted as stated; symmetric with B's M2 having no margin. Section 6 pre-registers numeric lines for every measurement; the owner may change them before the first run.

### 1.2 B's concessions that bind B, and what I take from them

| B concession (round1-advocate-B.md section 5) | Consequence for the final policy |
|---|---|
| 1. B-core does not fix the v2 loss unit | C-003 goes to A: `cluster.py:255-257` [READ] skips the whole reviewer when its block is not valid; the cut removes that for length faults. |
| 2. "5 of 5" overstated (four confirmed, one unconfirmed, orchestrator-reported) | X-002 is Neither: no recovery rate exists for any policy on gateway models. |
| 3. "3 of 264" derived, `unknown` class unmeasured | I add: its derivation is the `flags.tsv` text, and that text says the cause of all 4 rows was anchor over 200 (N2). |
| 4. About 36 `block ok false` runs have no path in B | B's amendment (re-ask also when an invalid block carries a prior) is adopted for the reflect trigger; in v1 the cut removes most of the cause at the source (W3). |
| 5. "five pins, not four" | The count is more precise than five (N8); the point that B-raise costs pin rewrites and A costs none stands. |
| 6. B's replay population is not audit-D's | M1 runs on both frozen populations; A-001 is Neither. |
| 7. Meaning of the claim cut is [UNVERIFIED] for B | Equally unverified for A: I add a two-judge falsifier (K2). |
| 8. A better on U-001, U-003 and the stateless form | Adopted into the merged policy as written. |
| 9. A-006 is a hole in B too | A-006: narrow form accepted by both. |
| 10. The X-001 textual argument is weaker than B states | X-001: see N7; the sentence is reflect-only and pinned, and an additive sentence is enough. |

### 1.3 B's per-point positions where I still disagree, with the strongest form first

**S-001 and C-001 (B: itemise first, truncation an optional lever behind an owner decision).** Strongest form: any cut is an edit; `SKILL.md:343` forbids normalising; the owner should decide before code does. Answer: the cut is a recorded pure function in the parser path, applied where no text rule forbids it (N7), it recovers the dominant failure class with no model call, no transport and no new command, and it is the only option that works in the v1 loop where no pre-merge step exists (N1). Dropping a line is also an edit, and a larger one: it removed 49 blocking lines and flipped 3 verdicts to PASS in audit-D (R02:100-101 [DOC]). I agree that itemising and the refusal are required under A as well; they are now in the policy.

**C-002 (B: Hybrid, add a re-ask when an invalid block carries a prior).** Strongest form: A's `block_ok` True after repair raises clearing power from broken blocks. Answer: W3 and N4. B's amendment is sound for residual faults and I adopt it as a reflect-path trigger; in the v1 loop an invalid-block reviewer's lost `prior resolved` costs one review of the cap (rows stay `resolved_check`, C-02 B5 [DOC]), not a wrong PASS, so it is a re-ask trigger and not a refusal.

**C-009 and C-012 (B: B wins; claim meaning and byte provenance).** Strongest form: the claim carries "X is wrong because Y" (`document_review_loop_prompts.md:60` per both variants [DOC]), the cut tails in B's sample are consequence clauses, and the stored member is no longer a byte copy of a hashed line. Answer: both stand as risks and neither is measured. I keep the cut for claims only with three safeguards: the visible `...` marker, the "shortened from N" line in the row, and a blind two-judge test on B's 34 claims (22 blocking, corrected from the "10 blocking" I wrote in Round 1: 10 is audit-D's claim-blocking count, 22 is B's replay count); if the judges mark more than 20 percent of the blocking claims as having lost a decision-relevant clause, claims move to re-ask-first and anchors, anchor2 and quote stay cut. For provenance each `repairs` item carries `original_sha256` of the flattened original field, so a cut field can be checked against `report_sha256`; the stored member is a recorded derived value, not a byte copy, and I say so.

**X-001 (B: Variant 2).** Answered in N7: the sentence is in the reflect skill only, is pinned by a test, and an additive sentence keeps both true. The remaining question is an owner call, which I state as a dependency and give a mechanical fallback for.

**X-003 (B: Variant 2, the re-ask is load-bearing in reflect).** Conceded for reflect; contested for v1: see N3 and N1.

## 2. Updated assessment of Variant 2

What B has shown that I did not have: the replay (5,270 lines, prefix locates 89 of 89 verbatim over-limit fields, `refs_norm` unchanged on 0 of 125), the E1 re-ask table, the PASS-by-loss refusal with an acknowledgement exit, the `blocking_state` class, the conservation property, the pre-registration discipline and the E2 design-review counter-evidence about agent-run normalisers and session surfaces. B is right that the compliance metric is honest by construction under B-core, and that the claim cut is the weakest part of A.

What B's defence leaves standing against B-core as a default:
1. **No place to run in v1.** The re-ask for the 44 reviewer runs needs a check that runs before the merge records the round, and none exists (N1). Either a new subcommand or a scratch merge is required, and B names neither.
2. **Deletion of votes.** Under literal `block_ok`, a length fault silently drops that reviewer's `prior open` dissent, wastes a review in a one-reviewer re-review and lowers quorum (N4). B's own amendment (re-ask also for invalid blocks that carry a prior) is the admission.
3. **The v2 loss unit** stays a whole reviewer per bad line unless the re-ask works (B conceded).
4. **B-raise** is untested on reviewer behaviour and an owner decision; it composes with A rather than replacing it, because any fixed limit has a tail.

My overall view: B's policy and A's policy differ on one thing, whether the first response to a length fault is a code cut or a model call. The code cut wins on dispatch independence, on the v1 mechanics and on the effects on C-02 and C-03. B's contributions fix the places where A was silent or unsafe. The merged policy below is A's order with B's record, refusal and carrier.

## 3. New evidence (code checks run now)

**N1. There is no pre-merge check or re-ask step for the v1 loop [READ, plus grep].**
- `merge_cmd.py:99-118` reads the reports, calls `led.merge_round` once (`:109`), renders (`:110`), writes `--out` (`:113-115`) and saves the ledger last (`:116`). A raised `LedgerError` is converted to a `ClickException` (`:111-112`), so a refused merge writes nothing.
- `merge_round` demands `n == len(rounds)+1` (`ledger.py:114-118`), so after a successful merge the same round cannot be merged again.
- The registered commands in `src/superclaude/cli/review` are `merge`, the ledger group (`revise`, `defer`, `verdict`, `capture`), `manifest` (`init`, `advance`, `validate`), `panel` (`resolve`, `validate`), `telemetry`, `cluster` and `verify-citations` (grep of command registrations): none parses a v1 block without merging.
- Consequence: B's re-ask for dropped blocking lines in merges that succeed (45 of 49 blocking drops in audit-D end with a surviving blocking row) needs a new parse-only command or a scratch merge. A re-ask driven by a refusal needs nothing new: the refusal leaves the file unchanged (`merge_cmd.py:109-116`), the docstring already says so for the zero-valid case (`ledger.py:111`), and the re-run passes the replacement report. That is the v1 transport in the merged policy.

**N2. All 4 PASS-by-loss rows in audit-D are anchors over 200 [RAN].**
`git show 6c0984326:.dev/eval-workspaces/tasklist-review-panel/20261111-a1/analysis/audits/audit-D/flags.tsv`, filtered on "NO blocking row": g3-sonnet-luna-ember-r3 (F1), g5-ember2-luna-r2 (F1), n5-sonnet-ember (F1 and F2), each "blocking finding dropped by merge (anchor>200)". So the 3 merges B's refusal would catch are all inside the cut's reach. Under cut-first, B's refusal fires on 0 of 264 merges in this population, provided the repaired lines carry no hidden second fault (the hidden faults can only be `refs`, N3). Derived from the file's reason text, not re-executed against ledgers. The refusal therefore guards the residual (bad JSON, non-boolean `blocking`, bad severity, refs) and keeps `INV-I` closed for them; it is not justified by a measured fire rate.

**N3. The residual is a floor and depends on the population [READ, DOC].** See W1. Audit-D: at least 4 of 92 (3 severity, 1 refs). B's replay: at least 30 of 154 (category 26, severity 3, refs 1). Both from first-fault counts. M1 reports the post-cut residual by rule on both populations.

**N4. What `block_ok` True after repair changes for C-02 and C-03 [READ, RAN, DOC].**
- C-02 INV-009 (merged C-02 text, probe table): the `block_ok` filter drops an invalid reviewer's `prior resolved` and also its `prior open` (collected at `findings.py:186-187` [READ], passed on at `ledger.py:139-140` [READ] with no `block_ok` test), so a valid `resolved` can clear over that dissent. With the cut, a length-faulted reviewer's dissent counts. My Round 1 line "INV-009 is unchanged by this position" was wrong for length-only faults.
- C-02 B5 and E2: the standard re-review is one reviewer (all 8 packaged templates carry `apply_to: ["first"]`, C-02 E2 [DOC]), so a length fault on a new finding by that reviewer leaves every `resolved_check` row unanswered, the decision REVISE with `next = re-review`, and one of the 3 reviews spent. Under B-core only a pre-merge re-ask prevents that, and N1 says none exists.
- C-03 floor (`complete >= min(2, requested)`, merged-output.md:36 [READ]): audit-D has 80 `2-blockok` rows [RAN: awk over `flags.tsv`], in 73 distinct (row, package) merges; 7 merges have two block-ok-false reviewers and none has three. With three reviewers and a floor of 2, at least those 7 of 264 merges (2.7 percent) are below the floor under today's `block_ok`; two-reviewer rows (for example `n5-sonnet-ember`) would be refused on a single fault, and I did not count them. Not all 80 are length faults (a missing block or a truncated block is also False), so repair lowers this number by an unknown amount and cannot raise it.
- The refusal at `ledger.py:150-157` is unchanged, and the one `block_ok` pin I checked (`test_review_ledger.py:376-385`) uses `_broken`, whose text has no findings block at all (`:341-342`), so a length repair does not flip it.

**N5. The dropped-blocking refusal and the C-03 refusal object [READ, DOC].**
- C-03 decided a `LedgerError` subtype, exit 12, and a printed object `{"refusal": "quorum_shortfall", requested, complete, invalid}` with no `decision` key (merged-output.md:36 and :77 [READ]).
- A dropped-blocking check needs the post-union result (is the derived verdict PASS), so it runs at the end of `merge_round`, after the quorum check. It still precedes `led.save` (`merge_cmd.py:116`), so the file on disk is unchanged. But `merge_round` mutates the ledger as it goes, and the existing refusal pin asserts the in-memory ledger is untouched (`test_review_ledger.py:373`: `led["rounds"] == [] and led["rows"] == []`). So the check must run on a deep copy that is swapped in on success, or the pin pattern breaks.
- It reuses the object: `{"refusal": "dropped_blocking", reviewers, dropped: [{reviewer_id, line, finding_id, blocking_state, rule}]}`, same exit 12, so the coordinator has one "re-run the review" signal. The acknowledgement option on `merge` takes owner and reason, mirrors C-02's `defer`, is stored in the round entry and listed in the merged report. C-03's open INV-001 applies unchanged: a refusal leaves no stored trace, so its rate is not measurable from the ledger.
- C-03's open INV-006 (merge unions findings of invalid-block reviewers) shrinks under A because fewer blocks are invalid; it is not closed.

**N6. First-pass state can be carried exactly, without a second parse [READ].**
- The only per-card state carriers in `src` are `cluster_cmd.py:155-163` (`state`, `block_state`, `errors`) and `verify_cmd.py:136-138` (`block_state`); `block_state` appears nowhere else (grep), and `findings_block_compliance_rate` has no Python in `src` (grep over `*.py`: no match); `scripts/reflect_shadow_exit.py:247` only reads it from telemetry.
- With `repair=True`, `errors` in the cluster listing would be empty for a repaired block and the length violations would vanish from the shadow artifact. So the listing must carry `repairs`.
- Exactness: the cut fires only on a field the unrepaired parse would reject, so the first-pass state is `state` if `state != "complete"`, else `invalid` if `repairs` is non-empty, else `complete`. Two additive keys, `first_pass_state` and `repairs`, in both listings; existing consumers read `state` and `errors` (`test_review_cluster_cmd.py:89,99,167` [grep]) and keep working.
- The same fact settles B's weakness 4: no second parse is needed; a differential test against a `repair=False` parse checks it.

**N7. The `SKILL.md:343` sentence is reflect-only and pinned [READ, RAN].**
- The sentence ("The orchestrator never edits, remaps or normalizes a reviewer's findings itself: a block that still fails after the one re-ask stays invalid") is step 4 of the reflect shadow procedure. `document_review_loop_prompts.md` and `spec-panel.md` have zero matches for "never edits", "remaps" and "normaliz" (grep counts: 0 and 0), so no text rule binds the v1 `merge`, where all 92 audit-D drops happened.
- `tests/cli/reflect/test_shadow_skill_contract.py:229-232` asserts three substrings of it ("valid on this first parse", "before any re-ask", "never edits, remaps or normalizes a reviewer's findings itself") and `first parse (before any re-ask)` in the skill text. Changing that sentence means editing a pin; adding one sentence after it does not. So my Round 1 line "needs one sentence changed" is withdrawn in favour of an additive sentence.
- It stays an owner reading whether package code counts as "the orchestrator"; the mechanical fallback is to leave the v2 call sites at `repair=False` (itemise only) and keep the repair in v1 `merge`.

**N8. Pin counts [READ, grep over `tests/`].**
- Over-limit literals in `tests/review`: `test_review_findings.py:113` (anchor 201) and `:117` (claim 301); `test_review_findings_v2.py:200` (quote 201; `:199` is the passing 200) and `:241` (claim 300 / 301); `test_review_card_convert.py:500` (`len == 300`). `parse_block` appears in only three test files (`test_review_findings.py`, `test_review_findings_v2.py` and one hit in `tests/cli/reflect/test_shadow_skill_contract.py:215`). `test_review_card_convert.py:697` uses `cc.MAX_REF_TEXT` and follows a changed constant.
- Under A: `repair=True` at the three production call sites rewrites 0 pins (no ledger or CLI test feeds an over-limit line); the direct-parser pins stay with the default `repair=False`.
- Under B-raise as stated (anchor, anchor2 and claim only): 3 assertion sites (`:113`, `:117`, v2 `:241`), 4 if `card_convert` imports the shared claim constant (`:500`). The quote pin (v2 `:200`) changes only if the quote limit is also raised. B's "four" listed the quote pin B-raise does not touch and omitted `card_convert`; the "five" in the diff analysis and both Round 1 files holds only if the quote limit is raised as well.

**N9. A repaired line that does not locate is still kept [READ].** `annotate` keeps a finding whose anchor is not found with `anchor_status: missing` (C-01 merged text, section 2.3 [DOC]; `findings.py:346-360` as cited in Round 1). B's own replay says 5 of 94 over-limit fields are not verbatim and are missing under any policy; under A the difference is a visible row where today there is none.

What I did not check this session: panel sizes per audit-D row (so the 2-reviewer quorum effect is uncounted), whether the audit-D non-blocking drops hide a second fault, whether any E2 launcher depends on dropped lines, and any PR-code corpus.

## 4. FINAL per-point table

Where I moved from Round 1 the reason column says "moved".

| ID | Final winner | Conf. | One-line reason |
|---|---|---|---|
| S-001 | Hybrid | 76 | A's cut-then-parse, with B's itemised record, PASS-by-loss refusal, and one stateless re-ask driven by the refusal (v1) or the invalid block (reflect); raise lever deferred. |
| S-002 | Hybrid | 80 | A's `repair` keyword (0 pins rewritten) plus B's additive `dropped` record with `blocking_state` and a derived `first_pass_state`. |
| S-003 | Variant 2 | 78 | B's 5,270-line replay and E1 table are the larger evidence base; my `flags.tsv` read adds that all 4 PASS-by-loss rows are anchor over 200. |
| S-004 | Hybrid | 82 | A's numeric kill lines and cost-side replay plus B's pre-registration, conservation test and T-B5; margins fixed before any run. |
| S-005 | Variant 2 | 70 | B's INV-A..N table is wider; keep A's candid "partly endangered" label for INV-C inside it. |
| S-006 | Neither | 60 | Presentation only; adopt B's open-facts section. |
| C-001 | Variant 1 | 72 | Cut anchor, anchor2, quote in code; claim cut visible in the row with a judge falsifier; no text rule binds v1; a drop is itself a larger edit (moved: anchors now visible too). |
| C-002 | Variant 1 | 80 | A length-only fault must not void a block: it deletes dissent (C-02 INV-009), wastes a review (C-02 B5) and lowers C-03 quorum (at least 7 of 264); residual faults stay `ok` False. |
| C-003 | Variant 1 | 76 | `cluster.py:255-257` skips a whole reviewer for one bad line; B conceded; shadow-only today. |
| C-004 | Variant 2 | 78 | Adopt B's refusal and acknowledgement for residual lines; it fires on 0 of 264 audit-D merges once the cut exists (insurance; moved from Hybrid). |
| C-005 | Hybrid | 74 | A's residual-only stateless re-ask with B's `blocking_state` gating; in v1 the trigger is the refusal, in reflect the E1 rule plus B's invalid-block-with-prior amendment. |
| C-006 | Hybrid | 72 | Stateless prompt, no `--resume`; reflect: attempt 2 before the `collected` commit (`manifest.py:371-383`); v1: replacement report plus its sha in the re-run merge; record shape belongs to C-08. |
| C-007 | Hybrid | 80 | B's replay (89 of 89, unique prefix) is the tasklist evidence; A's kill line stays for multi-line and code anchors. |
| C-008 | Hybrid | 70 | Record `refs_changed` only; copy-to-`refs` only if M1 shows firing (B: 0 of 125); fixes A's "touches no other field" sentence (moved). |
| C-009 | Hybrid | 62 | Cut claim with marker and a "shortened from N" row line, two-judge falsifier K2, fall back to re-ask-first for claims if it fails. |
| C-010 | Hybrid | 72 | `repairs` item per cut plus a rendered "shortened" line in the row's `### Lx` block; `...` marker on claims only (moved from Variant 1: unmarked anchors were a real gap). |
| C-011 | Hybrid | 70 | Repair is the default and works at any limit; raising limits is a separate owner decision after the CO-8 measurement; its pin cost is 3 (4 with `card_convert`), not 5. |
| C-012 | Hybrid | 70 | Derived copy plus `original_sha256` of the flattened field and the existing `report_sha256`; accept that the member is not a byte copy. |
| C-013 | Hybrid | 76 | A's repair plus a derived `first_pass_state` and `repairs` in both listings (exact, no second parse) and a differential test; B's by-construction safety replaced by a test (moved from Variant 2). |
| C-014 | Hybrid | 64 | Quote prefix passes the substring test (`verify_cmd.py:68-72`); per-profile limits as a parameter; in-session stateless re-ask; a code corpus is required before a PR module relies on it. |
| X-001 | Variant 1 | 66 | Sentence is reflect step 4 only (0 hits in v1 prompt and spec-panel) and pinned; additive sentence keeps the pin; owner must confirm code is not "the orchestrator"; fallback is v2 `repair=False`. |
| X-002 | Neither | 62 | No recovery rate exists for gateway models; E1 is four confirmed of five, Agent path, one length cause. |
| X-003 | Hybrid | 72 | A's 4 is a floor (hidden refs faults) and 19.5 percent on B's population; B's 44 reviewer runs fall to roughly the residual in v1; reflect's residual is non-length for both. |
| X-004 | Hybrid | 82 | Both hold only if first-pass state is carried: `first_pass_state` plus `repaired_lines_rate` and `dropped_lines_rate`. |
| U-001 | Variant 1 | 80 | The keyword keeps the five over-limit pins literal and answers C-01 INV-003; add a test that all three call sites pass it. |
| U-002 | Hybrid | 68 | The `refs_norm` exposure is real (`findings.py:321-337`) but measured at 0 of 125: record, do not copy (moved). |
| U-003 | Variant 1 | 85 | The cost-side re-merge is the only measurement that can show the policy harmful. |
| U-004 | Variant 1 | 80 | `repaired_lines_rate` per model, with B's `dropped_lines_rate` as the counterpart. |
| U-005 | Hybrid | 72 | Valid only in an open reflect stage for a non-`complete` earlier attempt; v1 has no manifest. |
| U-006 | Variant 2 | 85 | Adopt as the M1 population and the admission curve, with the population caveat. |
| U-007 | Variant 2 | 80 | Adopt, restated as four confirmed, one unconfirmed, Agent path. |
| U-008 | Variant 2 | 80 | Adopt the refusal with the acknowledgement exit; acknowledgement mirrors C-02 `defer`. |
| U-009 | Variant 2 | 80 | Adopt `blocking_state` and the conservation property (covers bad `prior` lines). |
| U-010 | Variant 2 | 70 | Adopt T-B5: the re-ask holds only the reviewer's own block and rejected lines and grants no tool. |
| U-011 | Variant 2 | 68 | B-raise as a documented, separable owner-decision lever; not in the default policy. |
| A-001 | Neither | 75 | QUALIFY: the audit-D base orders the policies but cannot state a recovery percentage; M1 uses two frozen populations. |
| A-002 | Neither | 78 | ACCEPT for verbatim single-line anchors (89 of 89); open for multi-line and code; missing-anchor rows exist today under any policy. |
| A-003 | Neither | 72 | REJECT stationarity (moved from QUALIFY): CO-8 changes the claim rate; both policies are written to hold either way, A's repair costs about nothing when the rate falls. |
| A-004 | Hybrid | 80 | ACCEPT, now quantified: C-02 INV-009, C-02 B5 and the C-03 floor (at least 7 of 264). |
| A-005 | Hybrid | 76 | QUALIFY: true only while shadow lasts; leaving shadow requires `first_pass_state` to be carried. |
| A-006 | Hybrid | 78 | REJECT the unconditional form, accept the narrow form (reflect manifest, open stage, non-`complete` earlier attempt); v1 record is the replacement report. |

## 5. Where I moved from Round 1, and why

1. "At most 4 residual lines" to "at least 4, population-dependent": code order of checks (`findings.py:96-118`) and B's replay.
2. "INV-009 unchanged by A" to "A removes it for length-only faults": `findings.py:186-187` and `ledger.py:139-140` collect priors from invalid blocks.
3. "SKILL.md:343 needs one sentence changed" to "add one sentence": a test pins the old substrings (`test_shadow_skill_contract.py:229-232`).
4. C-004: Hybrid to Variant 2 (adopt B's refusal), because INV-I covers the residual and the rule is cheap; its fire rate is 0 in the study data once the cut exists.
5. C-010 from Variant 1 to Hybrid and C-013 from Variant 2 to Hybrid: cut anchors need a rendered note; the first-pass carrier is exact and cheap, so A can own it.
6. Copy-to-`refs` demoted to a recorded flag (C-008, U-002): B's 0 of 125 and the ladder.
7. The v1 re-ask is refusal-driven (no new command): N1.
8. "10 blocking claims" corrected to 22 in B's replay population (10 is audit-D's).
9. A-003: QUALIFY to REJECT stationarity.
10. Pin count: "five" replaced by the per-site count (N8).

## 6. Proposed resolution text (12 bullets)

1. **Cut first, in the parsers (a).** Both `parse_block` functions take `repair=False`; the production call sites `ledger.py:128`, `cluster_cmd.py:151` and `verify_cmd.py:133` pass `repair=True` (a test checks every production call site passes it). One pure `repair_line(obj)` in the shared limits module cuts `anchor`, `anchor2` and a citation `quote` to the first 200 characters of their flattened form and `claim` to 297 plus `...`, before `_check_finding` and `check_finding`, and touches no other field and no `prior` line. Direct-parser pins stay unmodified.
2. **Itemise everything that is still dropped (a).** Each residual drop and each cut is recorded as `{line, finding_id, blocking_state (true, false, unknown), rule, field, original_chars, kept_chars, original_sha256}`, never reviewer text; the report file is never edited; a conservation test holds per block (non-blank lines = kept + priors + dropped); the merged report's `### Lx` block prints "shortened from N" next to the anchor status.
3. **Re-ask trigger (b).** Only for what remains invalid after the cut. In the v1 spec loop the trigger is the dropped-blocking refusal (item 8); lines that said `blocking: false` are itemised and not re-asked. In reflect the E1 rule stands (an invalid block after repair gets one bounded re-ask) plus B's amendment (an invalid block that carries a prior line is re-asked too).
4. **Re-ask transport (b).** Stateless: the original brief, the reviewer's own block and the parser's per-line errors, whole block returned; no other reviewer's content, no new tool grant, no `--resume` dependency (an optimisation only where a transport proves it). A transport that cannot re-ask degrades to itemise plus the refusal.
5. **Re-ask record (b).** Reflect: attempt 2 recorded before the `collected` commit, only while the earlier attempt is not `complete` (`manifest.py:371-383`). v1: the replacement report goes to the re-run `merge` and its `report_sha256` is in that round's entry. The record shape is C-08's.
6. **`block_ok` (c).** `block_ok` is the real parser verdict on the repaired lines: a length-only block is True (v1) or `complete` (v2); any residual fault is False. Reviewer entries add `repaired` and `dropped`; C-02 counts `block_ok`; C-03 counts `complete`, and may count only `repaired == 0` blocks for its floor as a recorded parameter (default off).
7. **First-pass carrier (d).** The parse result gains `repairs` and `first_pass_state` (`state` unless complete, else `invalid` when `repairs` is non-empty); `cluster_cmd.py:155-163` and `verify_cmd.py:136-138` emit both beside the unchanged `state`; `findings_block_compliance_rate` is the share of cards whose `first_pass_state` is complete; a differential test against a `repair=False` parse must show zero mismatches; `repaired_lines_rate` and `dropped_lines_rate` per model sit beside it.
8. **Dropped-blocking refusal (e).** At the end of `merge_round`, after the quorum check and on a deep copy swapped in on success (`test_review_ledger.py:373`), if the derived verdict would be PASS and an unacknowledged residual dropped line has `blocking_state` true or unknown, raise the C-03 refusal subtype: exit 12, `{"refusal": "dropped_blocking", reviewers, dropped}`, ledger file unchanged. An owner-and-reason acknowledgement option on `merge` lifts it, is recorded and listed in the report. No refusal when a blocking row survives; the dropped ids are printed.
9. **Raise lever (f).** Not part of the policy. Briefs state the limits from the constants (CO-8). After that change, measure first-pass compliance and `repaired_lines_rate`; any raise of the constants is a separate owner decision that rewrites 3 assertion sites (4 with `card_convert`, 5 only if the quote limit is raised) and reruns M1 and M2.
10. **Measurements (g).** M1 offline replay of the cut on two frozen populations (audit-D, 264 merges and 92 lines; B's 154 invalid lines), reporting passes-parser, locates-uniquely, `refs_changed` and residual by rule. M2 re-merge of the 264 merges with repair on and off, counting added blocking rows judged false and PASS-to-FAIL flips. M3 two-judge claim-meaning test. M4 stateless re-ask on the residual lines, per transport. M5 unit tests: no-op on every valid fixture line, boundaries 200/201 and 300/301 with and without repair, idempotence, no invented anchor, conservation, differential first-pass. M6 live `repaired_lines_rate` per model.
11. **Kill lines (g), written to a file before the first run; the owner may change the numbers.** K1: fewer than 90 percent of over-limit anchor, anchor2 and quote fields pass the parser and locate uniquely on audit-D (75 percent on a code or multi-line corpus once one exists) demotes that field class to itemise plus re-ask. K2: more than 20 percent of blocking claims judged to lose a decision-relevant clause (both judges) moves claims to re-ask-first. K3: repair is wrong if the blocking rows it adds are judged false more than 10 percentage points above the base rate of kept blocking rows, or if any merge flips PASS to FAIL through a false repaired row the cap of 3 reviews cannot clear. K4: the re-ask half is wrong if recovery is under 60 percent over at least 20 residual lines or if any re-ask changes a line it was not asked about. K5: the refusal is wrong if it fires on more than 5 of 264 merges after the cut or if any refusal has no re-ask or acknowledgement exit.
12. **`SKILL.md:343` (h).** Leave the existing Normalize sentences byte-identical (they are pinned at `tests/cli/reflect/test_shadow_skill_contract.py:229-232`); add one sentence after them: the package's parser step shortens over-limit fields in code, records every shortening, and the orchestrator still never edits a finding; the first-parse compliance rate reads `first_pass_state`. The owner confirms that package code is not "the orchestrator"; if not, the v2 call sites stay at `repair=False` (itemise and re-ask only) and the v1 `merge` keeps the repair, because no text rule binds it.

END-OF-ADVOCATE-FILE
