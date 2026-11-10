# Round 1 advocate statement: Variant B (variant-2-sonnet-analyzer.md)

Citation form: `A:NN`, `B:NN`, `C:NN` are lines of variant-1, variant-2, variant-3; `diff:NN` is diff-analysis.md; `seed:NN` is seed-brief.md. "Replication" means a check I ran read-only on the S1 files for this round.

## Position summary

Variant B is the best base to build on. It is the only design whose caps come from a per-finding measurement that I could replicate, the only one with a script-side revert (`enforce`) that ends the cycle even when the model ignores the cut-down request, and the only one that leaves the coordinator and the S1 briefs untouched apart from a one-line, verified substitution. B is not the winner as written: its review-3 prediction (mean 3.0, P(bar a) about 0.3) is optimistic, it breaks the seed's "7 bullets" rule, and it should take A's zero minor budget, A's authoritative re-review run, A's reviewer-granted override and A's drop of `## Unattended mode`.

## Steelman of A

**Strongest argument.** The attack surface is the number of sites, and a mechanism can be small and complete: three parts only (a reviewer-written class, a ledger, one stdlib checker, A:37), one invocation for both reviser and re-review (A:48, A:215), about 200 lines (A:221), no coordinator duty because the reviewer copies the exact reviewed file itself (A:42). The re-review re-runs the checker and treats its result as authoritative, "it does not matter whether the reviser ran the checker" (A:66), and an over-budget fix is never credited (A:67).

**What A genuinely gets right.**
1. The condition-word counter (A:80, A:129). It is backed by trt-r1 review 3, where 5 of 6 blocking findings are FR-8 GAP rows on guards the revision created (A:31). B's chain classes were traced only on flg-r1, flg-r2 and ctl-r1 (B:38), so B has no class for this chain.
2. The test break nobody else saw (U-005). I verified it: `tests/skills/test_worker_contract.py:831-839` asserts the set of commands with a `## Unattended mode` heading equals `UNATTENDED_COMMANDS`, and it runs at lines 1011 and 1124. A new command file copied from current `src/` (B and C both do that) adds `spec-panel-minfix` to the set and fails the test. A removes the section (A:162).
3. Falsifier 3, "surface is not the driver" (A:327), and falsifier 4 against Arm B's 3.5 (A:328). They test the causal premise and the cost of the mechanism directly, and they use the seed bar (proxy above 3 fails).
4. The override authority is the reviewer, with one per report and never for an `origin=changed` finding (A:50). That is the right party to judge "no class-C fix can close this".
5. It keeps seven bullets (A:163), which is what seed:41 asks for.
6. Ids stay out of the spec (A:118). The checker counts a finding id as a new id, so 427's inline tags stop being text the next review citation-checks.

## Steelman of C

**Strongest argument.** Integrity before size. C rebuilds the candidate from the frozen baseline plus byte-range edits and requires byte equality, so any untracked byte is `UNATTRIBUTED_CHANGE` (C:90) whatever a splitter would have said. State and baseline are hash-pinned and the pin is held outside the reviser's write set (C:47-49). An override is bound to the hash of the finding's exact edits (C:104-122). Output is canonical and deterministic with a distinct exit 70 for crashes (C:218-271). Inputs are hardened: 2 MiB bound, symlink and alias rejection, duplicate JSON keys rejected (C:216).

**What C genuinely gets right.**
1. It is the most candid about what is prose and what is mechanical (C:139) and about what a passing run would prove: "a safer bounded loop, not proven convergence" (C:321). An escalation is not a PASS (C:18).
2. `wrong_outcome` is required for every blocking MAJOR (C:36, C:43), which makes 427's own "names a concrete wrong outcome" test a structural field.
3. A removal cap (C:58, C:210) answers a real failure mode: a reviser can "fix" a finding by deleting an obligation (C:338).
4. The `-protocol` skill name is install-safe. I verified `install_skills.py:41-56` strips only the `sc-` prefix, so `spec-panel-minfix-protocol` matches no command file. A's sweep warning (A:151) applies only to a bare `sc-spec-panel-minfix`.
5. The smallest edit to 427's loop text: bullet 6 replaced, bullet 5 appended, a section added, seven bullets kept (C:164-182).

## Strengths claimed

1. **The caps rest on a measurement that replicates, and the neighbours' do not.** B reports 13 blocking fixes in flg-r2 cycle 1 with mean 108 words, min 58, max 186 (B:28), and a cap replay: an 80-word cap puts 11 of 17 MAJOR fixes over (B:92-98). Replication: I attributed the v1-to-v2 diff of `specs/history/` hunk by hunk to the `(F<n>)` ids inside each hunk, splitting shared hunks evenly (my script, not B's). The 13 blocking fixes come out at mean 116, median 126, with 0 of 13 at or under 40 words. A's "median 38 words, 62-79% of findings at 40 or fewer" (A:26) counts only the sentence that cites the id and says itself that 44-77% of added words are unattributed (A:26). In my run 3 of 21 tagged findings are at or under 40 words (14%). Flat caps would force these cuts across the 13 blocking fixes (1,507 words in total): A's 40 needs 987 (66%), C's 60 needs 729 (48%), B's 80 needs 509 (34%). The CRITICAL classes lower all three. Caveat: one loop, one cycle, written by an unconstrained reviser.
2. **It treats the causal premise as open and designs around that.** B's own data say size alone does not separate fixes with a blocking child from fixes without (114 against 105 words, B:80-87) and that the critical+major transition ratio is 0.72 in control and 0.66 in 427 (B:87). I re-derived both ratios from ARMB-REPORT line 13 and they hold (0.715 and 0.66). In my attribution the children-having fixes are larger (mean 130 against 107), so the direction is mild, not absent. B therefore adds gates keyed to the five traced chain classes (B:65-71, B:224-225) rather than relying on size alone, and derives its proxy forecast through them (B:399-409). A claims the surface is the driver on "weak, n = 6" (A:25) and C lists it as the main unanswered question (C:352) while predicting 1.0.
3. **`enforce` is the only termination guarantee that does not need the model.** It reverts every hunk of each failing finding whole, writes atomically, re-runs `check`, and refuses to run without a ledger (B:210-211). A property test pins "after `enforce`, `check` is 0" (B:327, test 19). A leaves the revert to the reviser (A:62). C admits nothing if the second check fails (C:96).
4. **It fits the real S1 briefs, which I checked.** `T05`, `T07` and `T09` each contain `/sc:spec-panel @.dev/...` once; `T06`, `T08` and `T10` contain it zero times. B's single `s#/sc:spec-panel @#/sc:spec-panel-minfix @#` (B:367) therefore changes exactly the three review briefs and nothing else. The coordinator has no new duty (B:105, B:131). `T05` and `T06` both say "Ownership: write ONLY your output file(s)", and `T06` says "apply confirmed findings", the clause that beats 427's bullet 7 in practice (flg-r1 disposition, "The Task 6 brief wins", B:33). B is the only design that engages that ownership clause: the ledger lives inside the disposition file the brief already requires and the script writes `.fixcheck/` (B:131-134, B:452). A adds a reviewer-authored `-reviewed.md` and a reviser-authored `-ledger.jsonl` (A:42, A:56). C adds `state.json` and `ledger.json` (C:47, C:68).
5. **Attribution is by unit diff, so a splitter error costs little.** On the S1 draft, A's splitter (`(?<=[.!?;])\s+`) gives 435 boundaries, 4 inside code spans and 126 (29%) followed by a lowercase letter, which are semicolon clauses. B's splitter with the capital-letter lookahead gives 288 boundaries, 0 inside code spans, 0 lowercase. B's caps (gross, net, add-only) are word counts inside a hunk, so they do not move when a unit boundary moves. A's `sites` and `new sentences` caps do.
6. **The measurement can test the mechanism, not only the outcome.** `attacks: L<n>/<finding id>` is computed from the receipt's line map (B:111) and turns the hand-traced chains of B:36-62 into a column (B:384). V7 voids a replicate whose reviser never ran the checker (B:381). A retry at 100/60 is pre-registered if more than 40% of blocking ids are escalated (B:424). The first implementation task is a replay harness over the six recorded loops, with a 10% deviation test (B:479). That harness catches tokenisation defects before a worker sees them.
7. **Two-tier availability rule.** If the script cannot run, the command stops with `E-FIXCHECK-MISSING` (B:106), so an arm cannot run silently unbudgeted. If the reviser did not comply, the next review records `STALE` or `MISSING` and the replicate is voided (B:110). That keeps data from a loop that is informative, and stops a loop that is contaminated. A continues in both cases (A:174); C stops in both (C:126).
8. **The cost estimate is itemised.** 20 to 31 tool calls, +8 to 18 minutes, 10% to 23% of a 78-minute loop, with sessions at 0 (B:432-440). A says 9 to 15 (A:343) and C about 10 (C:325), neither with the same breakdown. The honest price of B is that it is the most expensive of the three.

## Weaknesses in A

1. **The 40/30 class-B cap is calibrated on an undercount.** See Strength 1: A's "62-79% already fit 40 words" (A:26, A:82) comes from counting only the sentence that cites the id. On hunk attribution 0 of 13 blocking fixes in flg-r2 cycle 1 fit 40 words, and the cut needed is about 66% of the words. A's forecast of "1-3 escalations over both cycles" (A:319) has no derivation, and A's own falsifier 2 (3 or more carried open blocking findings at review 3, A:326) is the likely outcome if the cut-down fails. A's 7% growth forecast (A:314) also assumes the reviser complies with that cap.
2. **`open (over budget)` works against the success metric.** A re-review marks an over-budget finding `open` "whatever its text now says" (A:67, A:174). If the reviser merely skipped the checker, the fix stays in the spec as attack surface and is also counted as an open blocking finding in the review-3 proxy. The bar counts open findings, so that rule can only raise the number it is judged on.
3. **The override is unavailable in the cycle that needs it.** `L` is "never for an `origin=changed` finding" (A:50). AB-REPORT line 30 gives 89% (R2) and 100% (R3) of new findings as `origin=changed`. In cycle 2, nearly every finding is therefore capped at 40 words, which includes FR-8/FR-9 gap fills. One `L` per report (A:78) is thin for that.
4. **`new sentences` inherits the splitter's semicolon rule.** A splits on `;` (A:80, A:198) and gives class B one new sentence (A:76). On the S1 draft, 126 of 435 boundaries (29%) are followed by a lowercase letter. A 40-word fix of the form "X; Y" is two sentences and breaches. This is A-001 on A's own numbers.
5. **Baseline is unhashed.** The reviewer's `cp -p` copy has no hash, and A says nothing hashes the report or the copy (A:351, A:368). B's `snapshot` refuses a changed spec (`STALE-BASE`, B:131) at the cost of one call.
6. **Extra authored files against a real ownership clause.** `T05` and `T06` say "write ONLY your output file(s)". A has the reviewer write `-reviewed.md` (A:42) and the reviser write `-ledger.jsonl` (A:56). A does not mention the clause. A literal-minded worker refuses or skips, and the mechanism silently does not run.
7. **Attribution has no teeth at the re-review.** Unattributed sites "are not graded blocking" (A:67) and are only counted. A names this itself (A:375). B's `enforce` reverts them (B:211).
8. **Anchoring.** The re-review reads a checker report that carries the reviser's quoted old and new sentences (A:68). A lists the anchoring risk as untested (A:355, A:377). B keeps the reviewer to numbers and ids (B:111).

## Weaknesses in C

1. **The coordinator duties are not in the briefs, so the mechanism may never run.** C needs `freeze` before the reviser is dispatched (C:47), `check` after it (C:94), pinned hashes and grants (C:102), while claiming the convention "lets the experiment keep Arm B's briefs unchanged apart from the command name" (C:126). The S1 review briefs carry only a run line (`T05` and `T07` verified), and the command file is read by the reviewing worker, not the coordinator. No instruction reaches the coordinator. Either nobody freezes, or the briefs change and the one-line substitution claim is false (X-012). This is C's largest buildability defect.
2. **Admission can fall to all-or-nothing.** After a second failed check, "admit nothing, retain the last accepted specification and escalate" (C:96). With 60-word caps (C:58) and 11 of 13 blocking fixes over 60 on my replication, a reviser who misses one edit loses the whole cycle. Every blocker is then open at review 3, which is control-like or worse. The reviser can always pass by escalating every edit, so a rational reviser under a tight cap escalates widely. Both paths raise the review-3 count, and C's forecast of 1 and 1 (C:313) has no derivation and sits beside C's own admission that whether smaller text reduces blocking is "the main experiment" (C:352).
3. **Fragile machine input at the reviser.** The reviser must supply baseline byte offsets (C:81, C:90) and every reviser change outside a reviewer-registered target is `UNATTRIBUTED_CHANGE` (C:45). The S1 draft is pure ASCII (I checked: 57,763 bytes, 57,763 characters, 0 non-ASCII lines), so multibyte arithmetic is not the problem. Absolute offsets into a 57 KB file are, unless the reviser copies a target's range whole. C lists "Fragile machine input" itself (C:340). A reviser also cannot propagate a fix to a second site the reviewer did not quote, which is the propagation tension in B:447.
4. **Caps without evidence.** "Initial engineering choices, not empirically optimized limits" (C:62). C has no per-finding measurement (C-029). On my replication 60 words needs a 48% cut.
5. **Scope.** Seven new files with plugin mirrors and a design doc (C:145-160), against the seed's scope discipline. Whether any parity test requires a `plugins/` mirror is unverified (B:248). The mirror adds a drift surface.
6. **The removal cap fights the ladder.** The design says delete or narrow before adding (C:66) and then caps removed words at 120 and 240 (C:58). A reviser's own removals in the 427 loops run 84 to 379 words per cycle (B:20), so the cap rarely binds, yet it adds a failure path to the one lever that class D chains (3 of 13) need.
7. **Self-approved override in S1.** A grant needs "a logged user approval or a finding's explicit reviewer recommendation" (C:102). In a coordinator-run loop with no user in it, the coordinator approves itself. C names this as a trust boundary (C:122).

## Concessions

1. **The review-3 forecast is optimistic.** B:407 computes 12 x r squared with a pooled review-1 proxy of 12. B's own table puts Arm B's review 1 at 16 and 17 (B:401), and the variant is built on Arm B's briefs. ARMB-REPORT line 32 attributes that gap to spread or counting, which justifies pooling, but with 16.5 the same three r values give 2.9, 4.1 and 5.6. Also B:407 has no term for blocking findings carried open because they were escalated or reverted, and B:98 says 11 of 17 MAJOR fixes are over the cap. B:422 catches this in the failure table, but the central 3.0 does not include it. My own judgement, not data: P(mean at most 3) is nearer 0.3 and P(bar a) nearer 0.2 than B's 0.5 and 0.3. A includes a carried term (A:317). B should adopt it.
2. **Bullet 8 breaks the seed.** seed:41 says "keep its 7 bullets". B adds an eighth (B:252, B:259). Fold it into bullet 6 as C does (C:164) and move the rest to `## Fix Budget`. The byte-identical claim for bullets 1-7 (B:254) is lost and test M3 must be re-pinned.
3. **B missed the `## Unattended mode` test.** Its repository file is built on current `src/` (B:241, B:362), which keeps the section, so `tests/skills/test_worker_contract.py:831-839` (run at 1011 and 1124) fails. B:248 names five tests that may need a row and not this one. A's drop is right for the repository file.
4. **The 12-word minor budget contradicts B's own cause table.** B:226 says touching minor text "is what made it blocking-eligible", then B:176 lets 12 words touch it. B:476 half-admits zero is cleaner. Take zero (A:75, C:57). That also settles A-003 more cleanly.
5. **Reviser-granted override is weak.** A ledger `override:` code with a 10-word self-authored reason (B:178) is the loophole C's text warns about (C:122). Keep the reviewer's `large` flag (B:128), which is A's `L`, and drop the reviser-side path.
6. **The re-review is not authoritative.** Step 1.2 runs `verify --receipt ... --revised` without a ledger (B:110), although B:318 says `verify` can re-run `check` when a ledger is given. A reviser who skips the checker yields `MISSING` and no budget effect. The fix is already in hand: Arm B's re-review receives `--baseline <saved copy>`, so the reviewer can run `check` with that baseline, the spec and the disposition's ledger itself, as A does (A:66).
7. **Too many call types and a crash that reads as bad input.** Five subcommands and 20 to 31 calls (B:303, B:436) is the heaviest of the three. `hash` folds into `snapshot` and `verify` into `check`. Exit 1 is both B's input error (B:203) and Python's uncaught-exception code. C's distinct 70 is cleaner (C:267).
8. **Missing chain class.** B's classes A-E come from flg and ctl loops (B:38), not trt-r1, where A found 5 of 6 review-3 blockers were FR-8 GAPs on new guards (A:31). Add A's condition-word counter.
9. **A-002 is unaddressed.** `enforce` reverts whole findings (B:211), which removes half-fixes of one finding but not dependence between findings. B traces N3 to an F2 plus F11 interaction itself (B:48).

## Per-point positions table

Where a row says "tie", the letter is a nominal lean only. Rows where I prefer another variant are marked in the Concessions section or in the reason.

| id | preferred | reason |
|---|---|---|
| S-001 | B (tie) | Same eight sections in seed order in all three; no quality signal. |
| S-002 | B (tie) | Heading count does not touch the criteria; B's depth helps tracing but is longer. |
| S-003 | B | Six tables make each evidence claim checkable; A and C give one table and less per-finding data. |
| S-004 | A | Actor and phase numbering 1-11 is the easiest to build from; B's reference H3s interrupt the steps. |
| S-005 | B (tie A) | Literal bullet, literal section, script outline and test list per artifact. |
| S-006 | B | Derivation tables show how 13% and 3.0 were reached; A and C give numbers with less derivation. |
| S-007 | B | Detection, mitigation and residual columns per risk, plus a prose-only list. |
| C-001 | B | Class derived from severity and grade; every finding listed so a dropped id is caught; lighter than C's JSON; no reviewer-chosen letters as in A. |
| C-002 | B | 80/50 needs a 34% cut in my replication against 48% (C) and 66% (A), so the least forced escalation. It still binds 11 of 13. |
| C-003 | B (tie C) | Same 120 gross as C; B adds net and add-only caps. |
| C-004 | A (tie C) | Zero is simpler and removes B's own contradiction (B:226 against B:176). |
| C-005 | B | A computed 10% cycle cap with largest-first revert catches a runaway cycle (ctl-r2 +3,165 words, B:227); A has none. |
| C-006 | B | Universal and exec-recipe gates tie to chain classes B and C; add A's condition-word counter (trt-r1, A:31). |
| C-007 | B | Ledger sits in the disposition file the brief already requires; A and C add authored files against "write ONLY your output file(s)" (T05, T06 verified). |
| C-008 | B | A unit diff attributes every hunk without LLM byte arithmetic; C's byte equality is stronger at sub-unit level but is fragile input. |
| C-009 | B | Hash plus `snapshot` plus `STALE-BASE` with no coordinator duty; A has no hash, C needs the coordinator. |
| C-010 | B (tie) | `install_skills.py:41-56` strips only `sc-`; `fix-budget`, `sc-fixcheck` and `sc-spec-panel-minfix-protocol` are all install-safe. |
| C-011 | A | One invocation is simplest for a reviser; B should merge `hash` into `snapshot` and `verify` into `check`. |
| C-012 | C | Canonical deterministic JSON and a distinct crash code 70; B's text report plus receipt is second. |
| C-013 | B | `enforce` reverts whole failing findings without model compliance; A depends on the reviser, C can discard the whole cycle. |
| C-014 | A | The reviewer is the right authority; B's reviser-side override is self-authored; C's grant is self-approval in S1. |
| C-015 | B (tie) | B names the outcome: a GAP graded minor gets the minor budget (flg-r1 R3-7, R3-8, B:481). |
| C-016 | C | seed:41 keeps 7 bullets and C edits only bullets 5 and 6 plus a section; B's bullet 8 breaks the seed. |
| C-017 | A | Ids in the spec are attack surface (4 of 28 changed citations flagged in flg-r2 part 2, B:476); attribution lives in the ledger. |
| C-018 | A | An authoritative checker re-run at the re-review beats B's receipt check (B can do the same with `--baseline`). |
| C-019 | B | Stop when the tool cannot run; record and void when the reviser did not comply; A silently continues, C stops every loop. |
| C-020 | B (tie C) | Pre-flight `hash --file README.md` from inside a worktree plus `cp -n`; C's fixture probe is as good. |
| C-021 | B | Verified: T05, T07, T09 contain `/sc:spec-panel @`, T06, T08, T10 contain none. B's one `sed` touches exactly the review briefs; C's prose is not mechanical. |
| C-022 | B (tie A) | No coordinator duty; C's duties appear in no brief (X-012). |
| C-023 | A | The repository file must drop `## Unattended mode` (test_worker_contract.py:831-839, 1011, 1124); one file, not two. |
| C-024 | B | Only forecast with a derivation and disclosed assumed rows. I concede it is optimistic (Concessions 1). |
| C-025 | B | 14.4% from a tagged-word replay and a 16.1% arithmetic ceiling; A's 7% assumes full compliance with a 40-word cap. |
| C-026 | A | Four pre-registered falsifiers including the causal one, and a fail line equal to the seed bar; B's 5-or-more line is looser (X-013). |
| C-027 | B | Itemised and most honest (20-31 calls); A's 9-15 and C's 10 are less derived. |
| C-028 | A (tie) | One short fit assessment per adopter; out of scope for all three. |
| C-029 | B | Six loops, tables, replicable (my mean 116 against B's 108); A's 62-79% is an undercount (A:26). |
| C-030 | B (tie A) | Behaviour tests plus a property test of `enforce`; C's mirrors and design doc are scope; A's derivation pin is good. |
| X-001 | A | Zero for non-blocking findings; matches A-003 and keeps the rule mechanical. |
| X-002 | C | Seven bullets kept per seed:41 with the smallest edit. |
| X-003 | A | No ids in the spec; C contradicts itself (C:90 against C:167). |
| X-004 | C | Distinct exit 70 for crashes; Python's uncaught-exception exit is 1, which B and A use for something else. |
| X-005 | B | A script-side revert ends the cycle without model compliance. |
| X-006 | A | The reviewer grants; B's `large` flag is the same path. |
| X-007 | B | Two-tier rule: tool missing stops, reviser non-compliance is recorded and voids the replicate. |
| X-008 | B | Reviewer reads numbers and ids only. flg-r2 round 3 already decided statuses "by reading the spec text at the cited line, not `disposition-round2.md`" (round-3 report line 27, verified). |
| X-009 | B (tie A) | Deleting is the lever for class D; free deletes fit the ladder. Report removed words per cycle without capping them. |
| X-010 | B | My replication: 13 blocking fixes mean 116, median 126, none at or under 40 words; A counts only sentences that cite the id. |
| X-011 | B | Only variant that gates on chain classes and says size alone is not enough; my replication gives 130 against 107 words, a mild lean. |
| X-012 | B (tie A) | No coordinator duty; C's duties are absent from the unchanged briefs. |
| X-013 | A | A's fail line (proxy above 3) is the seed bar; B's 5-or-more line is looser. |
| X-014 | B | Experiment copy built on the 472-line 427 text Arm B ran, one change at a time; the repository file follows C-023 (A). |

## Shared assumption responses

**A-001 (regex sentence splitter is accurate enough): QUALIFY.** I measured both splitters on the S1 draft (`spec-v1-draft.md`, 8,148 words, flg-r2 history). A's `(?<=[.!?;])\s+` gives 435 boundaries: 4 inside code spans (0.9%), 0 after e.g./i.e./etc./vs./cf./no., and 126 (29%) followed by a lowercase letter, which are clause splits at `;`. B's version with the capital-letter lookahead gives 288 boundaries with 0 in code spans and 0 followed by lowercase. So mis-splits inside code spans are rare on the draft. The exposure depends on the metric. A's `sites` and `new sentences` caps count units directly and are inflated by the semicolon rule. B's gross, net and add-only caps are word counts inside a hunk and do not move with unit boundaries; only `entries` and quote matching do, and the 40-character unique-substring match (B:159) absorbs most of that. Not measured: revised text (different punctuation), table cells, and C's replacement dependency, which is quote uniqueness at `freeze` (C:45). The B replay harness (B:479) would measure it before any worker runs.

**A-002 (partial admission is safe): QUALIFY.** It holds only when the kept fixes do not depend on the reverted ones. The evidence against full independence is in the variants themselves: N3 traces to F2 plus F11 (B:48). `enforce` reverts a finding whole (B:211) and leaves the text the reviewer already saw, so the worst case is a kept fix that refers to something absent, an `origin=changed` finding on the next review. No variant handles it. A cheap handle is a `depends:` ledger field that cascades the revert. `attacks:` (B:111) would at least measure how often it happens.

**A-003 (deferred MAJOR notes do not re-enter the review-3 proxy): QUALIFY.** The proxy counts severity, not the blocking grade: ARMB-REPORT line 37 says flg-r1 R3-7 and R3-8 are MAJOR graded minor and "proxy and blocking differ in Arm B and nowhere else". Under the re-review flags, text the reviser did not touch is outside the changed-line scope, and an `origin=unchanged` finding is a minor note (spec-panel.md line 262, bullet 5), so a deferred note is mostly not re-raised at MAJOR. Without those flags (treatment A) the whole document is re-read and the assumption fails. Two consequences: (a) the experiment must keep Arm B's flags, which all three variants do (diff:113); (b) a nonzero minor budget, B's 12 words, makes the touched text changed and in scope, so it can re-enter the proxy. That is another reason to take zero. Cheap test: count `origin=unchanged` critical+major items at R2 and R3 and report them beside the proxy.

**A-004 (one cut-down brings fixes within cap, escalations stay at 1-3): REJECT as stated.** Nothing in the three documents measures a reviser hitting a numeric target in one retry. The pressure is large: revisers wrote 3.6 times the text the reviewer asked for (B:34), and on my replication the needed cuts are 34% (B), 48% (C) and 66% (A) of blocking words, with 11 of 13, 11 of 13 and 13 of 13 fixes over the cap. B's own "1 to 3" (B:412) is unsupported too. The assumption matters differently by design: B reverts only the failing findings and so converts a missed cut into an escalation (B:211); A converts it into a reviser-run revert (A:62); C can discard the whole cycle (C:96). In B and A the cost lands in the review-3 count as carried open blockers, so each should forecast a carried term and use falsifier 2 (A:326).

**AP-02 (smaller fixes cause fewer next-round findings), flagged CONTRADICTED in the diff: QUALIFY.** B's own table shows only weak separation by size (B:87). My attribution shows a mild lean (130 against 107 words, n = 13, no significance). Size is a plausible partial cause, not an established one, which is why B's budget is paired with class gates and why `attacks:` is worth its cost.
