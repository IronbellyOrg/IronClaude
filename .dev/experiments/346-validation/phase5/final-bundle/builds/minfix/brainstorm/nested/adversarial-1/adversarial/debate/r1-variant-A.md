# Round 1 advocate: Variant A (opus, architect)

## Position summary

Variant A has the best overall structure. The reviewer sets the budget class, the coordinator gets no new duty (so the briefs change only by the command name), the next re-review's own checker run is the one that counts, the Review Loop keeps exactly seven bullets, and no finding ids go into the spec. A's budget numbers and termination rule are weaker than B's, though. A should take B's per-finding sizes (about 80/120 words), B's baseline hash and B's script-side `enforce`, and C's exit-code layout. C adds coordinator duties that unchanged briefs cannot deliver. B lets the reviser grant its own overrides and adds an eighth bullet.

Ground truth checked for this round (read-only):
- `spec-panel.md:256-264`: 7 bullets, and bullet 6 carries the "cites its finding id" clause.
- `ARMB-REPORT.md:13-14,20,37`: R3 proxy 8/4/6/1, blocking 8/4/4/1, means 6.0/5.5/3.5, and growth 63.5/29.7/30.0. Line 37 explains why proxy and blocking differ.
- `install_skills.py:47-54`: strips only the `sc-` prefix.
- `tests/skills/test_worker_contract.py:831-839`: the set of command files with an Unattended mode section must match an exact list.
- `seed-brief.md:41,46,51`.
- A rough re-count of flg-r2 cycle 1 per-finding words (`specs/history/spec-v1-draft.md` against `spec-v2-after-round1.md`, stdlib `difflib`, read-only).

## Steelman of B

B's strongest argument is that it is the only variant that measured which kinds of fix produced which next-round findings, and then built its gates from that measurement.

- **The causal premise.** B finds that size alone does not predict a blocking child. "Size and normative-word count do not separate the groups ... A pure size cap will therefore cut growth and will not, by itself, cut review-3 blocking" (B:87; table at B:79-85). It pairs the size budget with gates on the chain classes it traced:
  - A: non-blocking parent.
  - B: universal or closed claim.
  - C: check recipe.
  - D: a deletion was on offer.
  - E: the reviewer's own recommendation was flawed.
  Classes A to D cover 11 of 13 traced items (B:63-71, B:222). Those gates are the only part of any variant aimed directly at the review-3 count rather than at growth. Its R3 prediction (3.0, band 2.1-4.0) is derived from stated measured and assumed rows, with the assumptions labelled (B:399-409).
- **Termination without model compliance.** `enforce --in-place` reverts every hunk of each failing finding and every unattributed hunk, writes atomically, and refuses to run without a ledger (B:210-211). Its property test checks that `check` returns 0 after `enforce` (B:322, test 19 at B:327). This is the strongest mechanical-enforcement answer to "what happens to an over-budget fix".
- **It fits the real S1 constraints.** B quotes the S1 reviser brief's ownership clause, "write ONLY your output file(s)" (B:131). So the ledger goes in the disposition file the brief already requires (B:134), and only the script writes `.fixcheck/`. B also shows from the logs that task briefs outrank 427 prose: "The Task 6 brief wins" (B:33). This is the strongest evidence for a rule that does not depend on which brief wins.
- **Change one thing at a time.** The experiment file is built on the exact 472-line text Arms A and B ran, and the repository file on current `src/` (B:362). That is the right way to isolate minfix from base drift.
- **Better measurement.** The `attacks: L<n>/<id>` tag (B:111) turns the hand-traced fix-to-child chains into a computed column. That makes the next experiment more informative whatever the result.
- **Calibration and honesty.** The cap replay (B:89-98) shows the real cost of each cap value: 11 of 17 MAJOR fixes over 80 words. B states P(bar a) of about 0.3 openly (B:409).

## Steelman of C

C's strongest argument is that it is the only variant with no attribution heuristic at all. The checker rebuilds the candidate from the baseline plus the ledger's edits and requires byte equality: "Any discrepancy is `UNATTRIBUTED_CHANGE`; even formatting churn fails. The checker does not trust reported sizes or an LLM's diff" (C:90). A and B both depend on a sentence splitter and quote containment (A-001). C does not, so the success criterion "every changed sentence attributed to a finding id" (seed:52) holds by construction rather than by a matching rule.

C also gets right:
- **Integrity.** The coordinator pins a state hash outside the reviser's write set and passes it as `--state-sha256` (C:47-49). State is created exclusively, idempotent on identical inputs, and treats different contents as a conflict (C:47). Input hardening covers size bounds, symlink and alias rejection, duplicate JSON keys and deterministic output (C:216, C:269-271). It is the only variant that would survive an adversarial reading of "mechanical".
- **Separation of duties for overrides.** "The reviser can request but cannot grant an override" (C:102). The grant is bound to the hash of that finding's exact edits, so any change invalidates it (C:122). This answers the seed's "how to stop it becoming the default path" (seed:61) better than B's self-granted overrides.
- **Exit codes that do not collide.** Exit 2 is reserved for `argparse` usage errors (C:263), which is what Python's `argparse` actually returns. Exit 70 marks an internal error, and exit 5 an output-write failure (C:262-267). A and B both use exit 2 for a policy breach, so a mistyped invocation looks like an over-budget fix.
- **Honest about stopping outcomes.** "If both replicates halt through escalation with no clean PASS, report a safer bounded loop, **not proven convergence**" (C:321). It also gives a rule to carry escalated obligations forward (C:304, C:321).
- **The deletion risk.** C caps removed words because "narrowing/deletion may 'fix' ambiguity by eliminating an obligation" (C:338). A and B do not discuss this risk.
- **The worker probe.** "Show that a fresh worker loaded the new command and executed the installed checker on a tiny valid and invalid fixture; merely reading a command file is not proof of invocation" (C:289). That matches this project's own WC-7 lesson.

## Strengths claimed

1. **No new coordinator duty, so the brief change really is one line.** "The coordinator gets no new duty, so the S1 briefs change only by the command name" (A:37). The reviewer writes every checker input (A:41-49). The reviser and the re-review run the same command line, which the reviewer writes into the report (A:48, A:66). The seed's success criterion requires "same briefs with the one-line name substitution" (seed:51). A meets it without hidden work. C does not (X-012: C:47, C:94 against C:126). B also meets it, at the price of five subcommands.
2. **Compliance does not change the outcome.** "This run is authoritative: it does not matter whether the reviser ran the checker" (A:66). "an over-budget fix is never credited" (A:67, U-003). A reviser who skips the checker gains nothing, because the over-budget finding stays `open` in the very count the bar uses. This is the strongest answer among the three to AP-04 ("the reviser actually runs the checker"). B can only detect skipping and void the replicate (B:230). C can only stop (C:137).
3. **The override is granted by a party independent of the reviser, needs no coordinator, and is closed to fix-induced findings.** Class `L` is set by the reviewer with a reason, at most one per report, "never for an `origin=changed` finding (its first remedy is to narrow or revert the change that caused it)" (A:50; U-006). The checker enforces the count and the reason line (exit 3, A:50, A:109). The person granting the larger budget is the one who judged the finding, not the one spending the budget. B's reviser grants its own overrides (A:50 vs B:178). C needs a coordinator file that unchanged briefs never ask for.
4. **A condition-word counter based on measured evidence.** In trt-r1, 5 of 6 R3 blocking findings were FR-8 GAP rows on guards the revision created (A:31). Condition words grew by +7 to +50 per cycle against 68 in the draft (A:15-22). A caps new `if unless when whenever except otherwise` at 1 per `B` fix (A:76, A:80; U-001). Neither other variant counts new guards, although FR-8 turns each one into a MAJOR GAP row.
5. **The Review Loop keeps seven bullets.** Bullets 2, 5 and 6 are replaced in place and the bullet order stays as in 427 (A:163). This matches the seed's "keep its 7 bullets" (seed:41) literally. A test imports `BULLET_NAMES` from the 427 pin test (A:248). Bullet 6 is rewritten so that it no longer says "each added paragraph or table cites its finding id" (A:118). C keeps that clause next to "does not need finding-id decorations" (X-003).
6. **The variant copy cannot drift silently.** "Derivation pin: build the expected variant from `src/superclaude/commands/spec-panel.md` by the five region rules ... and assert byte equality" (A:247). The budget constants exist only in the script: "Budget numbers are deliberately not in the command: the checker prints them (preflight) and its constants are the only source" (A:183). A test pins the SKILL.md table to `fixcheck.CLASSES` (A:250). B keeps a second copy of the numbers in the command and needs test M4 to keep it equal (B:333). C puts its numbers in prose in three places (command, SKILL.md, design doc).
7. **A test break the others missed.** A removes `## Unattended mode` from the variant because `tests/skills/test_worker_contract.py:831-839` requires the set of commands with that heading to equal a fixed list (A:162; U-005). I re-read those lines: `_check_no_unattended_sections` asserts `set(have) == set(UNATTENDED_COMMANDS)`. B's repository file and C's file both copy the current 486-line `spec-panel.md` (B:241, C:149), which has that section. So both would fail that test unless the list is edited, and neither mentions it.
8. **No finding ids in the spec.** "ids in the spec are added text the next review citation-checks" (A:118). Section 1 counts 25-61 id citations added per cycle (A:33). B's own data shows the cost: "flg-r2 Part 2 flagged 4 of 28 changed citations; flg-r1 R3-5, R3-6 are minor children of citation edits" (B:476). Yet B makes the tags free (B:165).
9. **Falsifiers that test the causal premises, not just the bar.**
   - Falsifier 1: the checker passes but R3 stays above 3, meaning minimality is not enough.
   - Falsifier 2: 3 or more carried blocking findings, meaning the budget turns fix-induced findings into unfixed ones.
   - Falsifier 3: few sites but many new findings, meaning surface is not the driver.
   - Falsifier 4: no better than Arm B's 3.5.
   (A:324-328.) Metric M9 splits R3 open findings into carried and new (A:305, U-007). This is the split that separates "the budget worked" from "the budget hid findings by leaving them unfixed", which C names as a risk (C:345) but does not measure as a column.
10. **Open to later adopters without any later change.** The checker lives in a folder named for its function (`fix-budget`), not after the command. Its contract is "document-agnostic: any loop that writes `reviewed-copy:` and `fix-budget:` lines" (A:258). A assesses fit per adopter (rf-qa good, reflect weak, implement needs a second unitiser, A:259-261) and writes out the promotion path (A:262). The skill name `sc-spec-panel-minfix-protocol` (C:151) ties a general tool to one command.
11. **Additive install and clean rollback.** `test ! -e` guards come before `cp -p`, nothing is overwritten, three sha256 values go to the watcher, and rollback is two `rm` commands (A:270-276, A:290). The sed substitution handles a token at line end and leaves `/sc:spec-panel-*` names alone (A:283-286). B's pattern only matches `/sc:spec-panel @` (B:367).

## Weaknesses in B

1. **The party being budgeted grants its own exemptions.** The reviser writes `override: gap-fill | multi-site | contradiction`, up to 2 per cycle, and each one doubles that finding's limits (B:178). On top of that, the reviewer may flag `large` on a quarter of the blocking ids (B:128). In the worst case, at 13 blocking ids, 2 + 4 = 6 findings run at double budget in one cycle. This is the "override becomes the default path" problem the seed names (seed:61). A 10-word reason does not stop it, because the reviser writes the reason.
2. **The cycle growth cap reverts the wrong fixes.** "for `CYCLE-GROWTH` the findings with the highest gross are reverted first" (B:211). The highest gross belongs to class C (120 words) and to overridden fixes. So a growth breach removes the CRITICAL fixes first, the findings that matter most, and keeps several small MAJOR fixes.
3. **A non-zero minor budget reopens class A, B's own strongest chain class.** Minor findings get 12 words, net 0, 1 entry, and 36 words per cycle (B:176-178). B's own open question admits the cost: "each changed citation is a new attack surface ... A strict 0 would be a cleaner mechanical rule" (B:476). Class A is the class B rates most removable (0.9, B:404). A 12-word allowance turns that mechanical removal back into a judgment call.
4. **An eighth bullet against the seed's "keep its 7 bullets" (seed:41).** Bullet 8 plus a new `## Fix Budget` section (B:252-290) puts the budget in two places in the command (bullet and section) and a third in the script. That is why it needs test M4 for number sync (B:333). It also repeats the whole budget table inside the Reviser brief (B:286), so the prose copies grow with every retune.
5. **Ids in the spec are free, against B's own evidence (B:165 vs B:476).**
6. **The repository file breaks `test_worker_contract.py`.** It is "a copy of `spec-panel.md` (486 lines ...) ... a 12-line `## Unattended mode` section" (B:241). The check at test lines 831-839 requires the set of command files with that section to equal a fixed list (verified). B lists other tests that "may need a row" (B:248) but not this one.
7. **Exit code 2 means over budget, but `argparse` also exits 2 on a usage error** (B:203-204 vs C:263). A reviser who mistypes a subcommand reads a budget breach and cuts down good text. The same defect is in A (see Concessions).
8. **Lenient failure thresholds.** It fails only at "mean review-3 proxy 5 or more, or both replicates 4 or more" (B:421). A mean of 3.5-4.5 is "Promising, not proven: extend to four replicates" (B:425). The pre-registered bar is 3 or less. A result of 4.0 fails the bar but under B's table it buys more replicates rather than counting as a failure.
9. **A larger surface for the model to operate.** There are five subcommands (B:303), a reviser sequence of `snapshot`, `check`, optionally `check`, `enforce` and `check` (B:285-288), and 20-31 extra tool calls per loop (B:436). Every extra step is a place for a prose-compliance failure that only V7 detects after the fact.
10. **The brief substitution is brittle.** `s#/sc:spec-panel @#/sc:spec-panel-minfix @#` (B:367) misses any invocation not followed by a space and `@` (for example a flag first, or a line end). B does not show that every T05/T07/T09 invocation has that shape.

## Weaknesses in C

1. **Coordinator duties that the unchanged briefs never assign (X-012).** The coordinator must:
   - "Use the helper's `freeze` operation ... before dispatching the reviser" (C:47);
   - pin the state hash (C:49);
   - "The coordinator runs `check` after the reviser" (C:94);
   - grant overrides (C:102);
   - promote accepted candidates (C:271).

   Yet C claims the convention "lets the experiment keep Arm B's briefs unchanged apart from the command name" (C:126). The command file is loaded by the reviewing worker, not by the coordinator, so nothing in Arm B's briefs makes the coordinator freeze or check. C concedes that "Coordinator freeze/check work is an explicitly measured part of the treatment" (C:285). In practice the S1 arm either changes more than one line of brief, which breaks seed:51, or runs without the gate.
2. **It relies on the LLM to produce byte offsets.** Edits carry "zero-based half-open **baseline** byte ranges" in UTF-8 (C:81, C:90). Any mismatch is `UNATTRIBUTED_CHANGE`. S1 contains multibyte characters (curly quotes, arrows and dashes are common in these specs). A reviser counting bytes by hand will fail the check on correct edits, and the one cut-down attempt (C:96) goes to fixing offsets instead of narrowing text. The rigour moves the heuristic's fragility from the checker into the model, which is the less reliable party. The fix is easy: accept `before`/`after` strings and let `check` compute the offsets. C does not propose it.
3. **Heavy machine authoring for the reviewer.** Every finding, minor ones included, needs a JSON object with `severity`, `blocking`, `hard_gate`, `wrong_outcome` and unique verbatim `targets` quotes (C:27-45). Zero matches or multiple matches stop preparation (C:45). This changes review 1, which AP-15 assumes stays the same (C:43 makes `wrong_outcome` mandatory), and it is the most failure-prone input in any variant (C:340, "Fragile machine input").
4. **"Admit nothing" throws away good fixes.** "If the second check fails, admit nothing, retain the last accepted specification and escalate" (C:96). A single unattributed byte in one finding's edit discards every in-budget fix of the cycle. That pushes the R3 count up through carried open findings, which is the under-fixing failure A's falsifier 2 targets.
5. **The removal cap penalises the move it asks for.** C says "delete or narrow before adding" (C:66) but caps gross removed words at 120 per MAJOR (C:58). Deleting an over-long faulty paragraph-line, the cheapest correct fix, can breach the cap. Deletions are what the next review cannot attack as new text.
6. **A prediction without a derivation.** R3 proxy "1 / 1, mean 1.0" (C:313) is described as "deliberately testable forecasts" (C:317). Yet C lists "Does smaller text actually reduce new blocking outcomes?" as "the main experiment" (C:352). A forecast that bold, with the causal question openly unresolved and no arithmetic, gives the judges no basis for estimating whether the bar is reachable.
7. **Scope and inconsistency.**
   - Seven new files, including `plugins/` mirrors and a design doc (C:145-156), against a theme that is meant to be additive and minimal.
   - Its bullet 6 still says "each added paragraph or table cites its finding id in the external fix ledger" (C:167) while also saying "The document does not need finding-id decorations" (C:90) (X-003).
   - Like B, it copies the current 486-line `spec-panel.md` (C:149) and so breaks `test_worker_contract.py:831-839` (verified).
   - It also edits the copied command's template lookup (C:160), which is a second unrelated change in the variant.
8. **A tool named after one command.** `sc-spec-panel-minfix-protocol` (C:151) ties a document-agnostic checker to one command. It installs safely, because `install_skills.py:47-54` strips only `sc-`. But rf-qa or `/sc:implement` would then call a script inside another command's protocol folder, or the folder has to be renamed at promotion time.

## Concessions

1. **A's class-`B` budget of 40 words is probably miscalibrated, and this is A's largest weakness.** A's calibration claim is "62-79% of findings added 40 words or fewer" (A:26, A:82). It counts only words in sentences that cite the id, which A itself calls a lower bound for attribution. B counts the same run (flg-r2 cycle 1) as blocking F1-F13 "mean 108, min 58" (B:28; X-010). My own rough re-count (sentence units split as in A:198, `difflib` on v1 against v2, read-only) gives:
   - Charging each changed site to the F-ids newly cited in it: median 82 words over all 21 findings, and every blocking fix from F1 to F13 is between 58 and 164 words.
   - Charging only the sentences that cite the id: median 48.5, with only about 2 of 13 blocking fixes at 40 words or fewer.

   The re-count is rough: site charging can over-attribute and sentence charging under-attributes. Either way, the 40-word cap would put most blocking fixes over budget. A's prediction of "1-3 escalations" (A:319) does not follow from it, and falsifier 2 (A:326) would probably fire. A should take B's 80/120 (MAJOR/CRITICAL), keep the 2-site cap under review, and run the planned dry run (A:353) on a real cycle before any worker sees the numbers.
2. **No baseline integrity.** A runs `cp -p` and hashes nothing (A:42, A:351(e), A:368). B's `reviewed_sha256` in the report, plus a STALE-BASE refusal (B:109, B:131), costs one hash line and closes the "copy taken after someone edited the spec" residual. A should fold it into `check`: the reviewer writes the hash, and `check` refuses on a mismatch. That needs no extra subcommand.
3. **Termination depends on the model.** A's reviser restores `revert_to` text by hand (A:62). B's `enforce` is strictly better on the "mechanical first" constraint (seed:42). A should adopt a script-side revert of whole findings. It should not adopt B's largest-first growth revert, and it should still warn about A-002.
4. **Exit code 2 collides with argparse** (A:108 vs C:263). Use C's layout: argparse keeps 2, and a breach gets its own code.
5. **The re-review reads reviser reasons.** A's checker report carries `why_not_narrow` inside `changes` (A:97). A itself names the anchoring risk (A:355). B's "copy only numbers and ids, never ledger prose" (B:111) is better. A should drop reasons from the report that the re-review reads.
6. **A missing checker is handled too softly.** "checker exit 1 or 3 is recorded and the re-review continues without it" (A:174). A does catch this through validity checks V-M1 to V-M3 (A:308). But B's `E-FIXCHECK-MISSING` at the start of the run (B:106) stops a treatment-less replicate before it costs a loop.
7. **A separate ledger file may conflict with the S1 ownership clause.** "write ONLY your output file(s)" (B:131). A's `<report stem>-ledger.jsonl` (A:56) is a new file the reviser authors. B's fenced block inside the disposition file avoids that conflict and should be adopted.
8. **A's predictions are judgment calls.** Growth of 7% and R3 of 2.5 (A:314, A:317) are not derived the way B's are (B:391, B:407). With the cap at 80 instead of 40, A's growth prediction would move toward B's 13%. A's R3 figure has no stronger basis than B's chain-class arithmetic.
9. **No cycle-level cap.** A's ceiling follows only from the per-finding caps (A:314). A computed cycle stop (B:178, C:62) is cheap defence in depth.
10. **Experiment base text.** B's two-base approach (B:362) isolates the change better than A's "current master minus Unattended mode" (A:157-162). That approach still differs from the 472-line text Arm B ran by the extra Usage line, the `--target-release` sentence and the "Native reasoning" line (B:241). For the repository file, A's removal of Unattended mode is still needed.

## Per-point positions table

| id | preferred | reason |
|---|---|---|
| S-001 | A (tie) | All three use the seed's 8 sections in the same order; nothing separates them |
| S-002 | A | Same content with fewer headings; B's fenced pseudo-headings (B:120-265) make it harder to navigate |
| S-003 | B | Six tables (growth, per-finding words, chains, classes, predictors, cap replay) make the strongest evidence section |
| S-004 | A | Grouped by actor and phase (reviewer, reviser, re-review), which matches the loop's roles; reference tables come after the steps |
| S-005 | A | A file table, then one H3 per artifact, with later adopters as a separate assessment |
| S-006 | B | The derivation tables (B:387-409) let a reader recompute the predictions |
| S-007 | B | Detection, mitigation and residual columns for each risk |
| C-001 | B | A block covering every finding with derived classes; A's blocking-only list loses minor ids from the record |
| C-002 | B | 80 words fits measured blocking fixes (min 58); A's 40 rests on a lower-bound attribution (see Concessions 1) |
| C-003 | B | Consistent with C-002; 120 words is replay-calibrated (B:98) |
| C-004 | A | Zero edits for non-blocking findings is the cleanest mechanical rule and removes class-A chains; B concedes 0 is cleaner (B:476) |
| C-005 | C | A fixed cycle cap is cheap; B's largest-first revert hits CRITICAL fixes first (B:211) |
| C-006 | B | Universal and exec-recipe gates target measured classes B and C; A's condition-word counter (U-001) should be added |
| C-007 | B | A fenced block in the disposition file respects the S1 "write ONLY your output file(s)" clause (B:131) |
| C-008 | B | Quote containment plus derived `op` can be built and tested; C's LLM byte offsets are fragile (C:81) |
| C-009 | B | A hash in the report plus a STALE-BASE refusal, with no coordinator duty; A has none and C needs a coordinator |
| C-010 | B | `sc-fixcheck` follows the repo naming, is general, and is safe under `install_skills.py:47-54`; C's name is tied to one command |
| C-011 | A | One `check:` line written by the reviewer is the smallest operating surface for the model; integrity can be added as flags |
| C-012 | C | Leaves exit 2 to argparse and separates input, hash and output failures; A and B collide on 2 |
| C-013 | B | Script-side `enforce` guarantees termination without model compliance |
| C-014 | A | The reviewer grants it: independent of the reviser, no coordinator duty, closed to `origin=changed` findings |
| C-015 | A (tie) | All three keep FR-8/FR-9 in the standard class with an override for larger gap fills |
| C-016 | A | Keeps 7 bullets (seed:41) and rewrites bullet 6 consistently; B adds bullet 8; C keeps a contradicting id clause |
| C-017 | A | Ids are added text that gets citation-checked; B's own data shows children of citation edits (B:476) |
| C-018 | A | The re-review's own checker run is authoritative whatever the reviser did |
| C-019 | B | Stop at the start of the run when the script is missing; record stale receipts as a validity failure, without blocking |
| C-020 | C | The fresh-worker invocation probe (C:289) proves delivery, not just presence |
| C-021 | A | The sed handles line end and hyphenated names; B's `@` pattern is brittle; C's is prose |
| C-022 | A | No new coordinator duty keeps the briefs to one line (B is equal on this) |
| C-023 | B | Experiment file on the 472-line 427 text isolates the change; the repository file must still drop Unattended mode (A:162) |
| C-024 | B | Derived from the chain classes, with assumptions labelled; A's is judgment and C's is unsupported |
| C-025 | B | Replay-derived; A's 7% assumed a 40-word cap that will not hold |
| C-026 | A | Four falsifiers that test the mechanism's causal premises, plus M9 |
| C-027 | B | The highest and most candid estimate, expressed as a share of a 78-minute loop |
| C-028 | A | A fit assessment per adopter plus a written promotion path |
| C-029 | B | Chain taxonomy, cap replay, and an honest non-predictor table; A's per-finding numbers are a lower bound |
| C-030 | B | 19 behaviour tests including an `enforce` property test; A's byte-equality derivation pin should be added |
| X-001 | A | Zero budget for minor findings (C agrees); B's 12 words reopens class A |
| X-002 | A | Seven bullets with bullet 6 replaced matches seed:41 and stays internally consistent |
| X-003 | A | No ids in the spec, consistently; C contradicts itself and B makes ids free |
| X-004 | C | The only scheme that does not overload argparse's exit 2 |
| X-005 | B | The script reverts whole findings, so termination is mechanical; C's admit-nothing discards good fixes |
| X-006 | A | The reviewer, not the budgeted reviser (B) and not an unbriefed coordinator (C) |
| X-007 | B | Fail closed at the start if the checker cannot run; do not stop mid-loop on a stale receipt |
| X-008 | B | Numbers and ids only, never reviser prose; A's report leaks `why_not_narrow` |
| X-009 | A | Free deletions keep delete-first incentive-compatible; the next review catches a lost obligation on the changed lines |
| X-010 | B | The re-count supports B: blocking fixes are 58-164 words when charged by site |
| X-011 | B | Size alone does not separate parents with blocking children from those without (B:87); A's n = 6 site correlation is weak |
| X-012 | A | No coordinator duty; C's claim of unchanged briefs contradicts its own freeze and check duties |
| X-013 | A | Strict and aligned with the pre-registered bar; B's 3.5-4.5 "promising" band is a soft escape |
| X-014 | B | The 472-line base changes one thing at a time |

Tally: A 22, B 25, C 4 (51 points). A wins most of the structural and contract points (who acts, what the command says, how drift and compliance are handled). B wins most of the calibration, evidence and termination points.

## Shared assumption responses

**A-001 (the sentence splitter is accurate enough): QUALIFY.**
- The risk is real, and A is more exposed to it than B, because A caps sites at 2 per `B` fix (A:76) while B caps ledger entries at 4 (B:175). A mis-split that turns one edit into two runs costs A half its site budget.
- Two points limit the damage:
  - The splitter `(?<=[.!?;])\s+` (A:198) runs on both baseline and revised text. A mis-split such as "e.g. " or a `;` inside a code span is reproduced the same way on both sides, so unchanged text still aligns and no false site appears. Mis-splits matter only inside changed paragraphs.
  - Ledger matching is substring containment in either direction (A:208-209), which tolerates a unit boundary that falls inside a quoted sentence.
- No variant has measured the false-breach rate. The right mitigation is B's replay harness before any worker run (B:479, U-014) together with A's planned dry run on flg-r2 cycle 2 (A:353).
- C does not escape the dependency (C:45, C:81). It moves it onto reviewer quotes and model-written byte offsets, which is worse for a model-written input (Weaknesses in C, item 2).
- Status: a pre-run gate is required. Accept the assumption only after the replay shows a false-breach rate below an agreed threshold.

**A-002 (partial admission is safe): QUALIFY.**
- The assumption is unstated in all three variants, and B's own trace shows the failure exists: N3 came from the interaction of F2 and F11 (B:48).
- A names the related risk ("Cross-site inconsistency ... the likeliest way minfix raises a count", A:350) but not the cross-finding case.
- Under the 427 re-review, a kept fix that depends on a reverted one shows up as an `origin=changed` finding on the kept text. It is detected, but it costs a review slot. Reverting whole findings (B:211) avoids half-fixes inside one finding, not across findings.
- Cheap mitigation: when the ledger cites two ids for one site (A:209, B:159), revert or keep them together. Log the coupled reverts as their own column so the experiment measures how often this happens.

**A-003 (deferred non-blocking MAJOR findings stay out of the R3 proxy): QUALIFY, mostly holds.**
- The proxy does count severity, not grade. `ARMB-REPORT.md:13-14,37` shows flg-r1 at R3 proxy 6 against 4 blocking, because R3-7 and R3-8 are MAJOR findings graded minor.
- But those two were children of changed text (B:59, B:56: R2-7 and R2-1). Under a zero budget the text of a non-blocking finding is not touched. Bullet 5 then confines the re-review to changed lines, and makes an `origin=unchanged` finding a minor note unless it quotes a changed line (`spec-panel.md:262`).
- So an untouched, deferred MAJOR note should not reappear in the R3 report. A zero budget removes the route by which such notes became R3 MAJOR findings (the F22 to N5 to N12 chain, A:29).
- The residual: a re-reviewer who ignores the scope and re-lists old notes. This argues for zero rather than B's 12 words. It also argues for reporting both the proxy and the 427 blocking count (C's M2, C:302; ARMB already shows both) and counting re-listed deferred notes separately in M9.

**A-004 (one cut-down attempt brings most over-budget fixes within the cap): REJECT, for A's numbers in particular.**
- The re-count in Concessions 1 shows flg-r2 blocking fixes at 58-164 words when charged by site. At A's 40-word cap nearly every blocking fix would start over budget.
- No variant offers evidence that a model hits a numeric word target in one retry. B's replay already puts 11 of 17 MAJOR fixes over 80 words (B:98).
- The likely outcome at 40 words is many reverts and escalations, which falsifier 2 would catch (A:326). Even at B's 80, a pre-registered retry setting (B:424) is necessary rather than optional.
- Mitigations:
  - Raise A's `B` class to about 80.
  - Make the breach report give a target ("cut 34 words from site 2"), not just the measured value.
  - Pre-register the escalation-rate threshold that triggers a retune.
  - Count first-attempt overruns and cut-down success as metrics (A's M6/M8, B:383).
