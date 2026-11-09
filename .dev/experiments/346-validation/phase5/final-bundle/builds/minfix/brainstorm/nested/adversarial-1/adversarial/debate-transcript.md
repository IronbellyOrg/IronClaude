# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 advocate statements, Round 2 rebuttals), plus the Round 2.5 invariant probe. Round 3 skipped: depth=standard.
- Convergence achieved: 96.4% (53 of 55 diff points agreed by majority; `debate/convergence-r2.md`)
- Convergence threshold: 75%
- Focus areas: All
- Advocate count: 3
- Variants: A = `variant-1-opus-architect.md` (opus:architect); B = `variant-2-sonnet-analyzer.md` (sonnet:analyzer); C = `variant-3-haiku-backend.md` (haiku:backend)
- Citation key for this transcript: `r1A`/`r1B`/`r1C` = `debate/r1-variant-{A,B,C}.md`; `r2A`/`r2B`/`r2C` = `debate/r2-variant-{A,B,C}.md`; `CV` = `debate/convergence-r2.md`; `IP` = `invariant-probe.md`; `DA` = `diff-analysis.md`. Line numbers in the Scoring Matrix point to each advocate's Round 2 "Updated per-point positions" row for that point.

## Round 1: Advocate Statements

The statements below are appended verbatim from `debate/r1-variant-{A,B,C}.md`. Their headings are kept as written, so they nest under each advocate heading only by position.

### Variant A Advocate (opus:architect)

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

### Variant B Advocate (sonnet:analyzer)

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

### Variant C Advocate (haiku:backend)

# Round 1 — Variant C

## Position summary

**Prefer C's transaction contract:** exact reconstruction, pinned inputs, one budget owner and externally granted exceptions make admission reproducible rather than a reviser's assertion (C §2, lines 43–49, 62, 88–98, 122). C is not experiment-ready as written: its coordinator-dispatch gap is real, and its forecast of one remaining critical/major finding per replicate is unsupported; borrow A's actor placement and B's experimental discipline before implementing it (A:37–42; B:362,397–409; C:126,313,352).

## Steelman of A

A's strongest argument is operational fit. “The coordinator gets no new duty” (A §2, line 37), because the reviewer saves the baseline and the report tells the reviser exactly what to run (A:42–62). That is genuinely better than assuming a command loaded by a review worker can instruct its parent coordinator. The existing command assigns the coordinator only count/prior-report/saved-copy duties (P:261), so A minimizes a real delivery problem rather than just reducing file count.

A also identifies a concrete mechanism worth testing: the non-blocking F22 → N5 → N12 chain (A §1, lines 28–30), and limits condition words because new guards produce further boundary-table work (A:80,129). The chain itself is corroborated: D1:37,39 records F22 applied despite being non-blocking; R2:48 names its new defective check; R3:35,84–89 traces N12 to the N5 fix. Its direct checker rerun and explicit carried-versus-new diagnostic are good controls against trusting a reviser's claimed resolution (A:66–68,305).

## Steelman of B

B's strongest argument is that **smaller is not necessarily more correct**. Its evidence section separates non-blocking edits, universal claims, executable checks, unused deletion options and flawed recommendations (B §1.3–1.5, lines 40–87). It explicitly says “Size and normative-word count do not separate the groups” (B:87). R2:27–38 independently supports its contract-shape, path-root and overly broad claim examples; R3:35 shows a fix resolving its parent while introducing another blocker. A size-only success claim would miss exactly these cases.

B also gives the clearest calibration sensitivity: at a 60-word MAJOR cap 13/17 historical fixes exceed it, at 80 words 11/17 do (B:89–98). These are B's measurements, not independently reproduced here, but its method and uncertainty are more inspectable than C's uncalibrated constants. Its source-matched experiment build (B:362), machine-derived child links (B:111,384) and reviewer blindness to ledger explanations (B:111,477) are sound. Atomic whole-finding restoration is an honest attempt to make the retry terminate without another model complying (B:210–211); my objection below is its input attribution and dependency assumptions, not that operational goal.

## Strengths claimed

### Citation key and evidence boundary

A/B/C are design proposals, not implemented checkers. All four comparison inputs were read fully in chunks of at most 120 lines. Ground-truth citations below are independent file reads, not quotations accepted solely from a variant. No checker, measurement script, experiment or installation was run for this debate; historical per-finding word estimates remain the proposing author's estimates.

- **A**: `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/brainstorms/346-minfix/nested/adversarial-1/adversarial/variant-1-opus-architect.md`.
- **B**: `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/brainstorms/346-minfix/nested/adversarial-1/adversarial/variant-2-sonnet-analyzer.md`.
- **C**: `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/brainstorms/346-minfix/nested/adversarial-1/adversarial/variant-3-haiku-backend.md`.
- **P**: `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/src/superclaude/commands/spec-panel.md`.
- **AB**: `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/AB-REPORT.md`.
- **ARM**: `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/ARMB-REPORT.md`.
- **D1**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/disposition.md`.
- **D2**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/disposition-round2.md`.
- **R1**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel.md`.
- **R2**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round2.md`.
- **R3**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/spec-panel-round3.md`.
- **Q3**: `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r1/.dev/orca-command-refactor/review/spec-panel-round3.md`.

1. **An admission contract, not a fuzzy attribution score.** C §2 Step 3 says “Compare the reconstruction with the supplied candidate byte-for-byte” and “even formatting churn fails” (C:90). A instead allows substring matching in either direction and splits words among matching ids (A:208–210); B uses normalized old quotes and a ten-word new-text prefix (B:159,164–166). C therefore has a concrete, testable invariant: accepted candidate bytes equal baseline bytes plus exactly the registered edits. It does not establish that the owner finding actually warrants the edit; C explicitly reserves semantic adequacy for review (C:88,128,334).

2. **The reviewer bounds the write scope before the reviser acts.** Exact unique quotes become baseline byte ranges at freeze time (C:45–47); every edit must stay inside its owner's target (C:90). The report identity includes its raw hash, not merely a reusable F1 label (C:43). This matters because the real revisions propagate findings into many statements, including extra related fixes (D2:13,19–24). C distinguishes an intended propagation from a reviser silently broadening the target; it may reject necessary propagation, but cannot quietly authorize it through a loose match.

3. **Replay and retry preserve evidence.** “Existing state with exactly the same inputs is an idempotent success; different contents are a conflict” (C §2 Step 1, line 47). A cut-down reconstructs from the same baseline, not the failed candidate (C:96); identical inputs produce byte-identical results, and checks do not mutate review counts or source files (C §4, line 271). This is a better recovery contract than turning an altered baseline into a new starting point. Hashes detect changes only relative to the independent pin; they are not proof against a coordinator controlling all inputs (C:49).

4. **No multiplying allowance by multiple labels.** C assigns each edit one owner; links can show that it answers another finding but cannot pool budget (C:62,88). A divides a site's words among k ids (A:210), and B allows two ids with equal splitting (B:159). C's rule gives a shared F2/F3/F4 mechanism one chargeable owner instead of extra room merely because it answers three findings; the real run explicitly chose one shared mechanism (D1:77).

5. **Authorization is separate from editing.** “The reviser can request but cannot grant an override” (C §2 Step 5, line 102). The grant is tied to the exact edit digest and cannot change scope, grade, minor status or cycle cap (C:122). That is a meaningful contract boundary beyond B's reviser-authored reason of ten words (B:178). The truth of the approval remains trusted coordinator behavior, not cryptographic proof of user consent (C:122,339).

6. **Failed accounting does not consume scarce semantic reviews.** Only a current exit 0 admits re-review; missing or stale inputs stop rather than degrade (C:126). This directly respects the scarce three-review limit in P:261. It is stricter than A's continue-without-checker path (A:109,174) and B's stale/missing-receipt continuation (B:110). Semantic review still independently checks the wrong outcome: “budget_ok is not semantic PASS” (C:128).

7. **Growth has an actual byte bound.** With two cycle caps of 6,144 gross added bytes, maximum accepted net addition is 12,288 bytes, about 21.3% of the 57,763-byte starting document (C:62,317; AB:6). Unlike word-to-byte estimates, this directly bounds the byte-growth metric. It is not convergence evidence: AB:19–25 already shows 29.7% growth without meeting the proxy bar; ARM:20–26 repeats that separation.

8. **Operational failures are first-class results.** C separately defines malformed input, stale pins, failed output writes and unexpected failure; a report-write failure cannot emit usable acceptance (C:259–271). Its proposed tests include interrupted freeze/retry, output aliasing, duplicate JSON keys, UTF-8 boundaries and stale receipts (C:275). These are appropriate boundary tests for the proposed file protocol, not claims of tests already passing. C also requires a fresh worker to execute valid and invalid fixtures, not merely read a command (C:289); AB:45–47 independently explains why personal installation delivery must be tested on this machine.

## Weaknesses in A

1. **A detects breaches but does not consistently deny admission.** Its re-review continues on input error or crash (A:109,174); unattributed sites are reviewed normally rather than treated as blocking process failures (A:67). Its own enforcement table concedes “one review spent on an over-budget fix” (A:365). That is not a complete mechanical admission gate under the three-review constraint (P:261). C's fail-closed rule is the stronger API contract (C:126,262–267).

2. **Its trust anchor is editable and its attribution can dilute a charge.** A admits “nothing hashes” the report and that altering its class line is a residual risk (A:351); its matcher divides words between matching ids (A:208–212). Neither guarantees that a site's full cost stays with one authorized obligation. C's pinned report/state and single-owner accounting directly address those weaknesses (C:43–49,62,90). This is a correctness advantage even for accidental edits; no hostile reviser need be assumed.

3. **The 40-word calibration is not settled.** A's median 38 words for flg-r2 cycle 1 and 44–77% unattributed upper-bound estimate (A:26) coexist with B's 13 blocking fixes all at least 58 words and 260 untagged words (B:24–29). Those methods cannot be treated as the same per-finding measurement. I have verified disposition coverage (D1:16–39), not independently recounted its spans. A's 40-word cap and claim that 62–79% fit therefore need a common counting/replay method before being accepted as calibrated. C's 60 is uncalibrated too; declaring that is more honest, not evidence that 60 is optimal (C:62).

4. **Word ceilings do not prove a byte-growth ceiling.** A's approximate 16% ceiling uses added words divided by starting words while labeling the growth metric bytes (A:314). Very long identifiers or multibyte words need not retain the historical bytes-per-word ratio. C measures gross UTF-8 insertion bytes directly (C:210,317). A's estimate remains a useful forecast, not a hard byte guarantee.

## Weaknesses in B

1. **Its minor-edit allowance contradicts a strict minimal-fix contract.** B permits 12 words per minor, 36 per cycle (B:176–178), while telling disposition rows to say “budget 0” (B:133,284). The real loop's F22 was explicitly non-blocking (R1:63–65), was edited (D1:37), and spawned a new check defect (R2:48). B's bounded correction might avoid that particular chain (B:233), but that counterfactual is not observed evidence. Zero edits is a simpler rule and matches P:259's “minor findings are notes and never trigger a revision.”

2. **Self-granted exceptions weaken the very budget being tested.** Up to two reviser-written override reasons double limits; reviewer `large` flags provide further doubled limits without using those overrides (B:128,178). The syntax is mechanically checkable, but the reviser can expand its own allowance by describing the work as a contradiction. C separates request from authorization and pins the exact edits (C:102,122). A's reviewer-only grant is also better than self-authorization (A:78).

3. **Automatic rollback acts on approximate matching.** B normalizes emphasis/whitespace, accepts a unique 40-character fragment and new-text prefix, and treats moved units as free (B:159,164–166). It then reconstructs an in-place result by reverting failing hunks (B:211). Atomic replacement prevents a torn file, but does not prove the right text was selected or the kept edits are independent. C never lets its checker rewrite the document and checks exact candidate reconstruction instead (C:90,94). Partial-admission semantic dependencies remain a concession for C too.

4. **B does not mechanically enforce named scope.** Its `named` flag is “Informational, never failing” (B:168). A reviser can accurately ledger an edit not actually named by the blocker, receive a warning, and still pass numerical accounting. C registers targets before dispatch and rejects out-of-target edits (C:45–47,90). This is a narrower and more testable interpretation of P:263.

5. **B's failure table softens the actual experimental bar.** It calls means 3.5–4.5 promising and suggests more replicates (B:425), although ARM:23–26 says a mean of 3.5 was not proven. More data can be reasonable research; it is not this screen succeeding. B:426 also labels mean/each ≤3 plus growth and validity “Bar met” without rechecking the spread condition that B:378 itself requires. C explicitly retains all three comparisons in its falsifier (C:319,345).

6. **Its hard-gate handling needs correction.** B's final open question allows an FR-8/FR-9 GAP graded minor to receive minor budget (B:481). That reflects observed grader inconsistency, not the actual rule: P:259 says FR-8/FR-9 findings are blocking; R1:63 gives an observed contrary F22 grade. A checker should surface that disagreement rather than silently encode the inconsistent grade. C's structural rule requires a hard-gate finding to be blocking (C:43).

## Concessions

1. **C's coordinator gap is a blocking design defect for the proposed experiment.** C requires freeze before dispatch and coordinator check/promotion afterward (C:47–49,94,271), yet says unchanged briefs plus a review-command substitution deliver those duties (C:126,282–285,297). An instruction loaded by a dispatched reviewing worker does not itself dispatch work in the parent. P:261's existing coordinator responsibilities do not include this new contract. Prefer A's reviewer/reviser-local delivery for this point (A:37–42), or explicitly authorize and test new coordinator instructions; the latter is an additional treatment change, not a one-line-only experiment. C's claimed delivery must not be accepted on prose alone.

2. **Withdraw confidence in C's 1/1 proxy forecast.** C labels it UNVERIFIED but provides no derivation (C:309–319); it also calls smaller-text causation the main unanswered question (C:352). B supplies a counterweight: fix size did not separate child-producing fixes in its small sample (B:77–87). The defensible claim is that C should bound growth and expose rejected work; its chance of getting the proxy to ≤3 is unknown. B's assumed-probability derivation is a better sensitivity analysis, though not a validated prediction (B:403–409).

3. **C's strict machine contract can prevent useful fixes.** Unique quotes, UTF-8 byte offsets and exact equality avoid ambiguous matching but increase authoring errors (C:45,81,90,340). A 60-word/512-byte budget plus 120-word removal cap can reject a correct multi-site repair; C acknowledges under-fixing and destructive deletion (C:331,335,338). It has no replay-based false-breach measurement. Prefer B's common-method replay before fixing the initial constants (B:479), not informal assurances that most cuts will fit.

4. **Partial admission is not semantic atomicity.** C lets valid edits remain while other obligations escalate (C:96,98). A/B do something similar (A:62; B:211). R2:28,37 directly shows the F2 path rule interacting with F11 placement, so a whole-finding rollback need not preserve cross-finding consistency. C's single-owner links solve accounting, not a dependency graph. A selected design must either reject the whole coupled change set or have independent review check the retained combination; this is a required correction, not existing implemented behavior.

5. **C has a growth guarantee, not an obligation-preservation proof.** Its removal cap limits destructive rewrites but does not prove that deletion preserves required behavior (C:338). Reviewer targets can themselves be overbroad (C:334); a tiny wrong replacement can still create CRITICAL defects (C:134). Hashes establish input continuity, not truth, minimality, valid approval provenance or correct severity (C:139).

6. **The proxy can count notes that the budget intentionally leaves alone.** ARM:13–14 records six critical/major findings but four blockers in flg-r1 R3; ARM:37 explicitly attributes the difference to MAJOR findings graded minor. Zero edits must not be marketed as removing those findings from a severity-count metric. C records proxy and actual blocking separately (C:302), but does not justify assuming deferred MAJOR notes vanish. The primary tally must retain them when open/reported under the pre-registered counting rule, even if the review verdict permits minor notes.

7. **C expands the implementation and has packaging risks still to verify.** C adds mirrors, a design document, strict input checks and richer exit states (C:149–160,195–216,259–275), while A/B offer smaller file sets (A:140–149; B:239–248). Its current-command copy is a poorer controlled-experiment base than B's exact 427 text; ARM:6 confirms the historical 472-line command differs from the restored 486-line machine version. C's preserved Unattended section also needs the enumeration-test check A identifies (A:162); that test was not independently read here, so it is a reported integration risk, not a verified failure. C §4's table actually names nine files when both mirror rows are expanded (C:149–156); the diff summary's “7” is not an authoritative count.

8. **Costs are estimates, and C does not eliminate skipped execution.** C estimates roughly 10 calls normally, 18–22 with retries, and human escalation can wait indefinitely (C:325–327). Its coordinator can still skip the checker (C:137,342). A runtime receipt proves an invoked check on particular bytes, not an operating-system security barrier or a demonstrated convergence benefit. Keep the proposed valid/invalid fresh-worker probe and measured cost logging; do not claim tests, packaging or runtime performance have already passed (C:275,289,327).

## Per-point positions table

“Preferred” selects the best approach on that specific point, not an assertion that the entire selected variant works unchanged. Equal shared structure still receives the required explicit choice. There are 51 positions: seven structural, thirty content and fourteen contradictions.

| id | preferred | reason |
|---|---|---|
| S-001 | C | Same eight-section order; C leads with a concrete admission invariant rather than additional machinery (C:3–5,20,130,141,277,295,323,349). Structural tie, C's opening is clearer. |
| S-002 | C | C's steps and inline schemas give a compact contract organization (C:20–128); B's many subsections are more useful for evidence than operating instructions (B:100–214). |
| S-003 | B | Cap replay, chain classes and negative predictors make the evidence auditable, unlike C's report-level calibration (B:63–98; C:9–16,62). |
| S-004 | C | Freeze → budget → ledger → check → authorization → re-review exposes state transitions in operational order (C:22–128); its actor-delivery defect remains X-012. |
| S-005 | A | Per-artifact changes plus derivation pins make additive implementation scope easy to inspect, without C's extra mirrors/document (A:140–162,246–252; C:149–156). |
| S-006 | B | Separating growth arithmetic from proxy sensitivity shows what is measured versus assumed (B:387–409); C's proxy table has no derivation (C:313). |
| S-007 | B | Detection/mitigation/residual columns operationalize risks and expose ownership problems (B:444–456); C's two-column table is candid but less diagnostic (C:329–343). |
| C-001 | C | All findings and explicit severity/blocking/hard-gate fields permit structural validation; classes are derived rather than selected by the reviser (C:24–53). |
| C-002 | B | For the initial MAJOR word allowance, prefer replay-informed 80 over uncalibrated 60 or contested 40; 13/17 exceeded 60 in B's stated method (B:89–98; C:62). Still requires independent replay. |
| C-003 | C | C retains 120 gross words but also bounds bytes and removals, which better contains destructive or long-token rewrites (C:55–60,210). |
| C-004 | C | Explicit zero edits and one deferred disposition per non-blocker avoid B's 12-versus-0 ambiguity (C:57,88; B:133,176). |
| C-005 | C | A fixed gross word/byte cycle ceiling includes overrides and cannot be purchased by unrelated deletion (C:62); A has no independent cycle cap (A:73–82). |
| C-006 | A | The condition-word tripwire directly targets added guards and has a stated causal trace; retain its heuristic limitation rather than call it semantic proof (A:31,80,129). |
| C-007 | C | One strict JSON object binds every disposition and exact edit to frozen state; duplicate keys and absent coverage fail explicitly (C:68–90,195). |
| C-008 | C | Unique registered target ranges plus byte reconstruction avoid fuzzy substring matching and budget splitting (C:45,90; A:208–212; B:159,166). |
| C-009 | C | Exclusive idempotent freeze and an independently pinned state hash detect stale/tampered evidence instead of trusting an editable baseline (C:47–49). |
| C-010 | A | A's neutral `fix-budget` name makes command/helper distinction explicit and explains the installer concern (A:151). Installer behavior was not independently checked here; no claim that C's protocol suffix is actually swept. |
| C-011 | C | Two operations with explicit input paths and paired authorization pins are easier to bound than B's mutation-capable five-operation API (C:189–204; B:303–318). |
| C-012 | C | Stable JSON plus separate input/hash/output/internal failure states gives callers actionable errors without accidental acceptance (C:218,257–271). |
| C-013 | C | Rebuild one cut-down from the original baseline; on another failure retain the accepted document, not a script-mutated approximation (C:94–98). Partial-success semantic coupling still needs correction. |
| C-014 | C | One externally authorized grant bound to exact edits is more accountable than reviser-authored doubling (C:102–122; B:178). |
| C-015 | C | FR-8/FR-9 remain blocking but do not automatically earn larger edits; authorization needs a concrete necessity (C:43,53,102; P:259). |
| C-016 | C | Amend bullet 6 and append admission to bullet 5 while retaining seven bullets, rather than B's eighth bullet (C:164–182; B:252–259). |
| C-017 | C | External attribution avoids growing normative text; every changed byte still counts rather than making citation annotations free (C:90,210; B:165). |
| C-018 | B | Verify receipts by recomputation and expose only numerical/line-map evidence; keeping reasons out avoids unnecessary anchoring (B:111,318,477; R3:27). |
| C-019 | C | Missing/malformed/stale evidence halts admission, matching the no-silent-fallback principle already present in P:258 (C:126). |
| C-020 | C | A fresh-worker valid/invalid execution probe tests actual delivery, beyond logging copied hashes (C:287–291; AB:45–47). |
| C-021 | C | Literal invocation-token replacement is unambiguous about preserving flags and not rewriting similarly named commands (C:281–285); exact resulting briefs must still be inspected. |
| C-022 | A | Reviewer-local saving and reviser-local checks reach actors through the existing report channel; C's new parent duties have no demonstrated dispatch route (A:37–42; C:47,94,126). |
| C-023 | B | Use the exact historical 427 text for the installed experiment and current source only for the repository artifact (B:362); ARM:6 confirms these are different bases. |
| C-024 | B | Assumption-labeled transition sensitivity is preferable to C's unexplained 1/1 forecast (B:403–409; C:313,352), though neither establishes actual success probability. |
| C-025 | C | Its 21.3% bound follows directly from gross byte caps, unlike converting capped word growth into byte-growth ceilings (C:317; A:314; B:392). The 15% forecast remains unverified. |
| C-026 | C | Preserve proxy ≤3, every-control and spread conditions; no-growth/all-escalation outcomes cannot masquerade as convergence (C:319–321,345; ARM:23–26). |
| C-027 | B | The per-role tool-call table is the most inspectable cost breakdown, including cut-down work (B:434–440). All variants' timing remains estimated (C:325–327). |
| C-028 | C | Keep later adoption separate and do not inherit the three-review count or widen implementation criteria (C:293,356), rather than designing new adapter options now (B:342). |
| C-029 | B | Child-chain analysis and cap replay provide a stronger starting calibration than report-level growth or incompatible span-attribution estimates (B:22–98; A:26; C:62). Measurements need independent reproduction. |
| C-030 | C | Runtime integrity tests cover interrupted preparation, UTF-8, tampering and unsafe outputs, essential for C's proposed contract (C:275). Its full file set is larger than needed and should be bounded during planning (C:149–156). |
| X-001 | C | Zero edits is an unequivocal non-blocker rule; B's small allowance changes known minor text into new review surface (C:57,62; B:176–178; R2:48). |
| X-002 | C | Seven bullets are preserved with an explicit external-ledger amendment, not a contradictory additional bullet layered over old inline attribution (C:167–182; B:254–259; P:263). |
| X-003 | C | Put finding ownership in the external ledger without a free-word exemption for annotations (C:90,167,210); B excludes such tags (B:165). |
| X-004 | C | Define nonzero categories, canonical status and output-failure behavior so automation never mistakes a missing receipt for acceptance (C:257–271). Exact integer choices are conventions, not inherent quality. |
| X-005 | C | A checker should validate, not automatically overwrite candidate bytes selected through heuristic hunks (C:94,271; B:164–166,211). Keep the last accepted document recoverable. |
| X-006 | C | Separate authority from the reviser and invalidate approval if the edit changes (C:102,122), rather than accept a self-written override reason (B:178). |
| X-007 | C | A stale/missing physical input stops admission; degraded checking is not the promised mechanical gate (C:126; A:174; B:110). |
| X-008 | B | Keep ledger reasons out of the next review; actual wrong outcomes and computed spans suffice (B:111,477). Real R3 explicitly judged spec text rather than dispositions (R3:27). |
| X-009 | C | Bound removals because an unrestricted deletion can discard required behavior; the cap contains damage without proving semantic preservation (C:58–59,210,338). |
| X-010 | B | Prefer B's explicit whole-fix attribution and sensitivity table for calibration, not A's id-bearing-sentence lower coverage (B:24–29,89–98; A:26). Neither count was independently recomputed here. |
| X-011 | B | Negative predictor evidence defeats a confident size→convergence claim; smaller fixes can still follow a wrong recommendation (B:77–87; R2:36; C:352). |
| X-012 | A | A actually assigns new work to the command-loaded reviewer and report-reading reviser; C's convention alone cannot instruct the parent coordinator (A:37–42; C:126,285). |
| X-013 | C | A proxy mean above 3 fails this screen, even if further research might be worthwhile; retain the spread comparison too (C:319,345; B:425–426; ARM:23–26). |
| X-014 | B | Match the exact 472-line comparator for causal isolation, rather than C's current-command copy (B:362; C:149; ARM:6). |

## Shared assumption responses

| id | response | evidence and consequence |
|---|---|---|
| A-001 | QUALIFY | Reject an untested claim that regex sentence boundaries are reliable enough for enforcement. A splits after punctuation and B normalizes/splits cells and sentences (A:198–199; B:164), while the real second revision added 6,073 bytes with only one extra line (D2:57). C avoids that particular parser assumption through unique exact anchors and byte reconstruction (C:45,90), but transfers failure risk to quote uniqueness and reviser offsets (C:340). Accept sub-line accounting only with executable fixtures for tables, punctuation in code/paths, repeated quotes, Unicode boundaries and the real long-line documents; C:275 proposes several, not a proven false-breach rate. |
| A-002 | REJECT | Partial admission is not automatically safe. R2:28,37 directly ties the new relative-path defect to F2's table and F11's separate placement rule; B:48 independently identifies that interaction. Reverting a whole finding is not reverting all dependent semantics (B:211), and C's “Valid edits may remain” has the same gap (C:96). Before admitting a partially retained candidate, the contract must preserve coupled changes together or require an independent consistency check of the retained combination. Accounting links alone do not establish this. |
| A-003 | REJECT | A severity proxy cannot silently exclude a deferred non-blocking MAJOR. ARM:13–14,37 reports six critical/major versus four blocking findings in flg-r1 R3. R1:63–65 is a concrete MAJOR/non-blocking F22; P:260 permits minor notes in a semantic PASS but does not redefine a severity tally. Count severity and actual blocking separately as C:302 requires, preserve terminal obligations under C:321, and do not assume zero edits mechanically lowers the primary proxy. The exact pre-registered rule for carried/re-listed notes must be fixed before treatment results, not adjusted to make the budget win. |
| A-004 | REJECT | One cut-down is a cost/termination policy, not evidence that models usually meet a numerical cap after it. B's replay has 11/17 MAJOR fixes above even 80 words (B:98), yet predicts only 1–3 escalations (B:412); A predicts the same order (A:319). No reviewed ground-truth report demonstrates a budget-driven retry, so there is no observed retry-success rate. Keep the single-attempt bound (C:96), measure first/second-check outcomes and escalated obligations (C:307), and treat high escalation as failure to demonstrate convergence, not low-growth success (C:321,345). |

**Decision for the merge:** select C's exact, fail-closed accounting core, but do not authorize an experiment from C unchanged. Resolve the coordinator delivery gap using A's actor-local approach, use B's comparator-matched build and replay method, and withdraw the unsupported 1/1 forecast; those changes matter because the verified reports already show that low growth and resolved parent findings can coexist with a failed final proxy (ARM:13–26; R3:15,35).

**Scope and remaining risk:** only this debate file was created; no code, Git, installation or network work was performed. Runtime correctness, per-finding recounts, packaging behavior, checker cost and actual convergence remain untested.

## Round 2: Rebuttals

The rebuttals below are appended verbatim from `debate/r2-variant-{A,B,C}.md`.

### Variant A Rebuttal (opus:architect)

# Round 2 rebuttal: Variant A (opus, architect)

Citation form: `A:NN`, `B:NN`, `C:NN` are lines of variant-1, variant-2, variant-3; `rB:NN`, `rC:NN` are lines of `debate/r1-variant-B.md` and `debate/r1-variant-C.md`; `rA:NN` is my own Round 1 statement.

## Response to criticisms

Each criticism raised against Variant A in the B and C Round 1 statements, with my answer. "Concede" means A's text should change in the merge.

### From B (rB:43-52)

| # | Criticism | Answer |
|---|---|---|
| B1 | The 40/30 class-`B` cap is calibrated on an undercount: 0 of 13 flg-r2 blocking fixes fit 40 words; A's "1-3 escalations" is underived (rB:45) | **Concede.** I already conceded this in Round 1 (rA:100-104): my own rough re-count put every F1-F13 fix between 58 and 164 words. B's independent replication (mean 116, median 126, rB:34) and B's cap replay (B:92-98) agree. A takes 80/120 (MAJOR/CRITICAL). A's 7% growth (A:314) and 2.5 proxy (A:317) assumed compliance with 40 words and are withdrawn as stated. |
| B2 | `open (over budget)` can only raise the metric the bar uses (rB:46) | **Partly contest.** In the experiment a reviser who skips the checker does not produce a counted replicate: A's validity rule V-M2 requires "a ledger and a `fixcheck.json` ... for each cycle", and a failing replicate "is re-run, not counted" (A:308). So the rule does not inflate the measured proxy through non-compliance. Once B's script-side revert is adopted (B:211), over-budget text is reverted before the re-review, so the rule fires only when the reviser also skipped the revert. In that case marking the finding open is the honest record: crediting a fix that broke the budget would hide the breach. I concede B's narrower point that the over-budget text stays in the spec as surface; that is the cost of a non-compliant cycle, and the experiment voids it anyway. |
| B3 | `L` is "never for an `origin=changed` finding", and 89%/100% of new findings are `origin=changed` (AB-REPORT line 30, which I re-read), so the override is effectively cycle-1 only (rB:47) | **Concede in part.** The fact is right. My reason (A:50: "its first remedy is to narrow or revert the change that caused it") still holds as a default, because reverting a cycle-1 site is free under A's rule that removals cost nothing (A:80). But a revert can reopen the parent blocking finding, and A gives no path for that case. Amendment: keep one `L` per report, granted by the reviewer; drop the absolute ban and replace it with a required reason that says why reverting the parent change would reopen a blocking finding. That stays checkable for presence (exit 3 on a missing reason, A:50). |
| B4 | `new sentences` inherits the splitter's semicolon rule; 126 of the draft's boundaries are followed by a lowercase letter (rB:48) | **Concede, verified.** My own count on `spec-v1-draft.md` finds the same 126 lowercase-next boundaries, plus 155 and 172 in the two revisions (New evidence 3). A fix of the form "X; Y" is two sentences and would breach class `B`'s limit of 1. A adopts B's capital-letter lookahead (B:164) and keeps sites only as a soft count; the word caps carry the budget. |
| B5 | Baseline unhashed (rB:49) | **Concede** (as in rA:105). The reviewer records `reviewed_sha256` (B:109) and the checker refuses a mismatch. |
| B6 | Extra authored files against the briefs' ownership clause (rB:50) | **Concede, and the evidence is stronger than B said.** The Arm B R2 reviewer template says "write ONLY your output file; ... no edits to the spec or any other file" (T07 template, New evidence 1). A's reviewer `cp -p` to `-reviewed.md` (A:42) is exactly an "other file" at R2. A's ledger file (A:56) also conflicts with T08's "write ONLY disposition-round2.md". A drops both: the ledger goes into the disposition file (B:134) and the reviewer writes only a hash. |
| B7 | Attribution has no teeth at the re-review: unattributed sites "are not graded blocking" (rB:51) | **Concede.** A named this itself as open question 2 (A:375). With B's revert adopted, unattributed hunks are restored to baseline text by the script before review (B:211), so the question goes away without process-only FAILs. |
| B8 | Anchoring: the report the re-review reads carries the reviser's quoted text and `why_not_narrow` (rB:52) | **Concede** (as in rA:108). The re-review copies only numbers and ids (B:111). |

### From C (rC:54-62)

| # | Criticism | Answer |
|---|---|---|
| C1 | A detects breaches but does not deny admission: the re-review continues on input error or crash (A:109, A:174) (rC:56) | **Concede for missing or malformed inputs.** 427's own bullet 1 already says "if a named file is unreadable or empty ... stop and say which, and never fall back to a first review" (`spec-panel.md` line 258, re-read). C's fail-closed rule (C:126) is the same house style; A's "continue without it" breaks it. A's own validity rule re-runs such a replicate anyway (A:330), so continuing only spends a review slot on data that is thrown away. I contest one part: "unattributed sites are reviewed normally" stops mattering once the script reverts them (B7). |
| C2 | The trust anchor is editable, and a site matched by k ids splits its words evenly, which can dilute a charge (rC:58) | **Concede both.** The hash answers the first (B5). The second is a real accounting hole that B shares (B:159): a shared site cited for three ids gets three allowances. A adopts C's single-owner rule (C:62, C:88): each hunk is charged to one finding; other ids may be linked but do not add budget. |
| C3 | The 40-word calibration is not settled (rC:60) | **Concede** (B1). |
| C4 | A word ceiling is not a byte ceiling; A labels growth in bytes and computes the 16% bound in words (rC:62) | **Concede the wording.** A:314 derives "about 16%" from added words over 8,148 draft words, under a column labelled bytes. The draft is pure ASCII (New evidence 4), so the word-to-byte ratio is stable on S1, but the claim should say "about 16% in words". The fix costs nothing: A's report already computes `bytes_added` per finding (A:94), so the merged checker can enforce C's byte cycle cap (C:62) alongside the word caps. |

Net: of 12 criticisms I concede 10 fully and 2 in part (B2, B3). None of them touches A's structural core: who acts (no coordinator duty), who grants the override (the reviewer), the seven bullets, no finding ids in the spec, the authoritative re-review run, and the `## Unattended mode` drop. Both B and C endorse most of that core (rB:13-19, rC:9-11, rC:80, rC:150).

## Updated assessment

**B, after its defence.** B's Round 1 statement is the strongest of the three. Its calibration claim now rests on two independent counts (B's tags and B's replication, rB:34; my site re-count, rA:101), and its self-concessions match mine almost point for point: zero minor budget (rB:69), reviewer-granted override only (rB:70), seven bullets (rB:67), the `## Unattended mode` test break (rB:68), an authoritative re-review run (rB:71), the condition-word counter (rB:73) and an optimistic proxy forecast (rB:66). With those taken, B's design and A's converge. What B still has that I would not merge:
- Five subcommands and 20-31 extra calls (B:303, B:436). B itself proposes folding `hash` into `snapshot` and `verify` into `check` (rB:72). I would go further: one `check` with a `--revert` flag that does what `enforce --in-place` does.
- Even budget splitting across two ids (B:159), the same hole C found in A (C2 above).
- Approximate matching (40-character unique substring, 10-word `new` prefix, B:159). C's objection that `enforce` reverts on that basis (rC:70) is fair, but it is a matcher-precision issue that B's replay harness (B:479) measures before any worker runs. I keep `enforce`.
- I withdraw my Round 1 criticism of B's brief substitution (rA:74). The briefs show B's pattern hits exactly the three review briefs (New evidence 5).

**C, after its defence.** C's statement is candid: it concedes the coordinator delivery gap as "a blocking design defect" and prefers A's actor-local placement (rC:80, rC:130, rC:150), withdraws the 1/1 forecast (rC:82) and accepts partial-admission coupling as a required correction (rC:86). Three of its points moved me:
- **Single-owner accounting** (rC:44). It closes a budget-pooling hole in both A and B.
- **Fail closed on missing inputs** (rC:48). It matches 427 bullet 1 word for word.
- **Hard-gate structural validation** (rC:76; C:43). A CRITICAL or FR-8/FR-9 finding must be blocking. That reports the grader inconsistency B:481 would otherwise encode as a minor budget.

C's exact byte reconstruction remains the strongest integrity invariant, but it should not ask a model for byte offsets. The checker can find each `before` string in the frozen target and compute offsets itself; a unique `before` inside the reviewer's registered target is enough. My Round 1 argument that S1 is full of multibyte characters (rA:86) was wrong for the draft (New evidence 4), so the real cost is absolute positions in a 57 KB file, not encoding. C's coordinator-owned grants and `state.json` still need a coordinator duty that no brief delivers. That is why the override authority stays with the reviewer.

**Where the merge should land (architect's view).** Take A's structure, B's calibration and termination, and C's contract details:
- From A: actor placement (reviewer writes inputs, reviser and re-review run the checker, no coordinator duty); reviewer-only override; seven bullets with bullet 6 rewritten; no ids in the spec; budget constants only in the script; `## Unattended mode` dropped from the repository file; the four causal falsifiers.
- From B: 80/120 caps; script-side revert; ledger in the disposition file; hash plus stale-base refusal; the capital-lookahead splitter; `attacks:`; replay harness first; the 472-line base for the experiment file; the narrow brief substitution.
- From C: exit codes (argparse keeps 2, crash 70); fail closed on missing physical inputs; single-owner charging; hard-gate validation; a byte cycle cap; the fresh-worker valid/invalid probe.

## New evidence

All checks were read-only, run for this round.

1. **The R2 reviewer brief forbids any other file.** `phase2/S1/briefs/templates/T07-R2-reviewer.TEMPLATE.txt`: "Ownership: write ONLY your output file; planning only, no edits to the spec or any other file". The other briefs say:
   - T05 (R1 reviewer): "write ONLY your output file(s)".
   - T09 (R3 reviewer): "write ONLY that file".
   - T06 (R1 reviser): "write ONLY your output file(s)".
   - T08 (R2 reviser): "edit ONLY the spec and write ONLY disposition-round2.md".

   Consequences:
   - A's reviewer-written `-reviewed.md` (A:42) breaks T07.
   - A's reviser-written ledger file (A:56) breaks T08.
   - B's script-written `.fixcheck/` files are a weaker conflict with T08, since the reviser still causes the write. B flags this itself (B:452).
   - The lowest-risk merge has workers write no extra files. The reviewer runs a read-only `hash`. The reviser's ledger lives in the disposition file. The baseline is a script snapshot, and its acceptance by a literal-minded reviser is confirmed in a pilot (B:451).
2. **427 already fails closed on missing inputs.** `src/superclaude/commands/spec-panel.md` bullet 1 (line 258): "if a named file is unreadable or empty, or the prior report has no `review: N of 3` header, stop and say which, and never fall back to a first review". C's rule (C:126) extends existing house style. A's "continue without it" (A:174) and B's "STALE ... and MISSING do not stop the review" (B:110) depart from it.
3. **Splitter counts on S1** (stdlib `re` over the whole text of `exp346-ab-flg-r2/.../specs/history/`):

   | file | A's `(?<=[.!?;])\s+` boundaries | of which next char lowercase | of which after `;` | B's lookahead boundaries |
   |---|---|---|---|---|
   | v1 draft | 564 | 126 | 258 | 349 |
   | v2 after round 1 | 653 | 155 | 301 | 402 |
   | v3 after round 2 | 694 | 172 | 325 | 425 |

   My totals differ from B's 435/288 (rB:38) because I ran the regex over the whole file, so line-end boundaries count too. The lowercase-next figure on the draft (126) matches B exactly. Revised text has more of these splits, so A's `new sentences` and `sites` counts get noisier exactly where they are measured.
4. **Encoding.** `spec-v1-draft.md`: 57,763 bytes, 57,763 characters, 0 non-ASCII. v2: 4 non-ASCII characters (8 extra bytes). v3: 13 (26 extra bytes). B's "pure ASCII" claim for the draft is right (rB:58). My Round 1 claim of common multibyte characters (rA:86) is withdrawn. Byte offsets in cycle 2 would cross a handful of multibyte characters, which is a minor risk.
5. **Brief invocations.** `/sc:spec-panel @.d...` appears once in T05, T07 and T09 (task text and templates) and not in T06, T08 or T10. The R4 briefs outside Arm B's loop (T11, T13, T15, T17) contain prose mentions such as "/sc:spec-panel and", "/sc:spec-panel," and "/sc:spec-panel.". A's `sed` (A:283), applied "in every brief", would rewrite those prose mentions too if those files were ever used. B's `@`-anchored pattern (B:367) touches exactly the three Arm B review briefs. B's is the better choice for S1.
6. **Arm B's review-1 proxy was 16 and 17** (ARMB-REPORT lines 10-16, re-read). This confirms B's own concession that pooling the review-1 proxy at 12 (B:401, B:407) flatters its forecast (rB:66). With 16.5 and B's middle r of 0.50, review 3 comes to about 4.1, not 3.0. Any merged forecast should start from Arm B's 16.5, because the arm uses Arm B's briefs.
7. **Installer rule, re-read.** `src/superclaude/cli/install_skills.py` `_has_corresponding_command` strips only the `sc-` prefix and does not strip `-protocol`. So `fix-budget`, `sc-fixcheck` and `sc-spec-panel-minfix-protocol` all install. My A:151 warning applies only to a bare `sc-spec-panel-minfix`. Folder naming is not a differentiator.

## Updated per-point positions

| id | preferred (A/B/C) | changed since R1? | reason |
|---|---|---|---|
| S-001 | A (tie) | no | Same eight sections in seed order in all three |
| S-002 | A | no | Same content with fewer headings; B's pseudo-headings are harder to navigate |
| S-003 | B | no | Six evidence tables, independently replicated (rB:34, rA:101) |
| S-004 | A | no | Steps grouped by actor (reviewer, reviser, re-review); B also prefers A here (rB:85) |
| S-005 | A | no | A file table, then one H3 per artifact; C agrees (rC:106) |
| S-006 | B | no | Derivation tables let a reader recompute (and correct, New evidence 6) the forecast |
| S-007 | B | no | Detection, mitigation and residual columns per risk |
| C-001 | B | no | Every finding listed with a derived class; lighter than C's JSON. Add C's hard-gate check (see C-015) |
| C-002 | B | no | 80/50 fits the measured blocking fixes; A's 40 is withdrawn (B1) |
| C-003 | B | no | 120/80, consistent with C-002 |
| C-004 | A | no | Zero edits for non-blocking findings; B concedes it (rB:69), C agrees |
| C-005 | C | no | A fixed word and byte cycle cap; it answers C4 too. B's largest-first revert hits CRITICAL fixes first |
| C-006 | B | no | Universal and exec-recipe gates plus A's condition-word counter (B accepts it, rB:73) |
| C-007 | B | no | Ledger inside the disposition file; T08 says "write ONLY disposition-round2.md" (New evidence 1) |
| C-008 | B | yes (amended) | Unit diff with B's lookahead splitter, but charged to one owner per hunk as C does (C2); drop the even split that A and B both use |
| C-009 | B | no | Hash plus stale-base refusal with no coordinator duty; A's reviewer copy breaks T07 (New evidence 1) |
| C-010 | B (tie) | no | All three names install safely (New evidence 7); naming is not a differentiator |
| C-011 | A | no | One `check` invocation, with B's revert as a `--revert` flag rather than a separate subcommand |
| C-012 | C | no | argparse keeps exit 2; crash 70; separate input, hash and output failures |
| C-013 | B | no | Script-side revert of whole failing findings guarantees termination; C's admit-nothing discards good fixes |
| C-014 | A | partly | The reviewer grants it, one per report. The absolute `origin=changed` ban becomes a required reason (B3) |
| C-015 | C | yes | All keep FR-8/FR-9 in the standard class, but C alone validates that a hard-gate or CRITICAL finding is blocking (C:43), as 427 bullet 2 requires. B:481 would budget a minor-graded GAP at minor |
| C-016 | A | no | Seven bullets, bullet 6 rewritten consistently with no id clause; C is close but keeps the id clause (C:167) |
| C-017 | A | no | No ids in the spec; B concedes they are attack surface (B:476) |
| C-018 | A | no | The re-review's own checker run counts, copying only numbers and ids (B's rule); B concedes (rB:71) |
| C-019 | C | yes | Stop on missing or stale physical inputs, as 427 bullet 1 already does (New evidence 2); A's validity rule voids such a replicate anyway (A:330) |
| C-020 | C | no | The fresh-worker valid/invalid probe proves delivery |
| C-021 | B | yes | Verified: B's `@`-anchored pattern hits exactly T05, T07 and T09. A's pattern would also rewrite prose mentions in the R4 briefs (New evidence 5) |
| C-022 | A | no | No coordinator duty; C concedes the gap (rC:80) |
| C-023 | B | no | The 472-line base for the experiment file; the repository file still drops `## Unattended mode` |
| C-024 | B | no | Only derived forecast, but restart it from Arm B's review-1 proxy of 16.5 (New evidence 6), which gives about 4.1 |
| C-025 | B | no | Replay-derived growth; label ceilings by unit. C's 21.3% is the only byte-true bound and should be stated beside it |
| C-026 | A | no | Four causal falsifiers at the seed bar; keep C's spread condition explicit (A states it at A:322) |
| C-027 | B | no | Itemised and most candid |
| C-028 | A | no | One fit assessment per adopter; not designed now (C agrees on separation) |
| C-029 | B | no | Replicated twice; A's per-finding numbers are an undercount |
| C-030 | B | no | Behaviour tests plus the `enforce` property test; add A's derivation pin and C's integrity cases |
| X-001 | A | no | Zero for non-blocking findings; all three advocates now agree |
| X-002 | A | no | Seven bullets with bullet 6 replaced; C is equal on count, B concedes (rB:67) |
| X-003 | A | no | No ids in the spec, consistently; C contradicts itself (C:90 against C:167) |
| X-004 | C | no | The only layout that does not overload argparse's exit 2 |
| X-005 | B | no | The script reverts whole findings; add C's coupled-revert correction (A-002) |
| X-006 | A | no | The reviewer, independent of the reviser, with no unbriefed coordinator |
| X-007 | C | yes | Fail closed on missing or stale inputs (New evidence 2); continuing spends a review slot on a voided replicate |
| X-008 | B | no | Numbers and ids only; A's report leaked `why_not_narrow` (conceded) |
| X-009 | A | no | Free deletions keep delete-first worth doing. Report removed words per cycle (A's M7). B's data: removals run 84-379 words per cycle, so C's cap rarely binds but adds a failure path to the cheapest fix |
| X-010 | B | no | Two independent re-counts support B |
| X-011 | B | no | Size alone does not separate parents (B:87); B's replication shows only a mild lean (rB:35) |
| X-012 | A | no | No coordinator duty; C concedes (rC:150) |
| X-013 | A | no | The fail line is the seed bar; B's 3.5-4.5 "promising" band is a soft escape |
| X-014 | B | no | The 472-line base changes one thing at a time |
| A-001 | B | no (QUALIFY stands, now with numbers) | 126 to 172 lowercase-next splits per file (New evidence 3). Use B's lookahead splitter and word caps that do not depend on boundaries; run the replay harness (B:479) before any worker run |
| A-002 | B | no (QUALIFY) | `enforce` reverts whole findings; add a coupled revert for hunks linked to more than one id (rA:188) and C's demand that coupled changes are kept or dropped together (rC:86). Measure with `attacks:` |
| A-003 | A | no (QUALIFY, mostly holds) | Zero minor budget keeps deferred text `origin=unchanged`, which bullet 5 caps at minor. Report the proxy and 427's blocking count separately (C:302) |
| A-004 | B | no (REJECT as stated) | No evidence of one-retry compliance. `enforce` turns a miss into a recorded escalation; pre-register B's retry at 100/60 (B:424); count carried blockers (A's M9) |

Tally: A 21, B 27, C 7 (55 rows; Round 1 was A 22, B 25, C 4 over 51). Changes since Round 1:
- Moved to C: C-015, C-019, X-007.
- Moved to B: C-021.
- Amended toward C: C-008 (single owner).
- Amended in A's text: C-014 (override reason instead of a ban).

The A rows that remain are the structural and contract points: actor placement, override authority, the Review Loop shape, ids, the re-review's authority and the falsifiers.

### Variant B Rebuttal (sonnet:analyzer)

# Round 2 - Variant B (sonnet, analyzer)

## Response to criticisms

Citation form: `A:NN`, `B:NN`, `C:NN` are lines of variant-1, variant-2, variant-3; `rA:NN`, `rB:NN`, `rC:NN` are lines of the Round 1 statements; `r2A:NN` is A's Round 2 rebuttal; `AR:NN` is ARMB-REPORT.md; `SP:NN` is `src/superclaude/commands/spec-panel.md`. Numbers marked "my script" were computed read-only for this round from the table at AR:13.

### 1. A's claim that Arm B's review-1 proxy of 16.5 moves B's forecast from 3.0 to about 4.1 (r2A:80)

**Arithmetic: correct.** B:407 is review-1 proxy times r squared. With 16.5 and r = 0.50 the result is 4.1; with r = 0.42 and 0.58 it is 2.9 and 5.6 (my script). This matches what I conceded in rB:66. The central 3.0 should not stand as a point forecast.

**Premise: not supported by the data A cites, and A's re-basing is internally inconsistent.** Four counter-points:

| # | Point | Evidence |
|---|---|---|
| 1 | The six recorded loops show no positive link between review-1 and review-3 proxy. Correlation of R1 and R3 is -0.54 (n = 6, not significant, but the wrong sign for A's scaling). | AR:13: R1 = 11, 12, 9, 9, 16, 17; R3 = 8, 4, 6, 5, 6, 1 (my script). Per-loop R3/R1: control 0.73, 0.33; treatment A 0.67, 0.56; Arm B 0.38, 0.06. The arm with the highest R1 had the lowest R3 mean (3.5). |
| 2 | R1 is run identically in every arm; the flags only enter at R2 and R3. | AR:6 ("Only difference from treatment A: the round 2 and round 3 review briefs"); AR:32 ("not an Arm B effect"). Treatment A used the same 427 text and got R1 = 9, 9, so the command text does not explain 16, 17. |
| 3 | I do not accept AR:32's "run-to-run spread" as proof either. | Within-arm R1 pairs are tight (11/12, 9/9, 16/17) and between-arm gaps are wide. That looks more like an arm-level cause (time separation, AR:35; flg-r1 master peeks, AR:18 and AR:36) than noise. The honest statement is that R1 for a new arm is unknown between 9 and 16.5, with 12.3 the pooled mean of all six (my script). |
| 4 | A kept r = 0.50, which B:407 derived from the 427 blend (0.66) times a 25% replacement cut. Re-basing R1 to Arm B while keeping the blend's r mixes two regimes. | The 0.66 is a mean of eight per-transition ratios over four 427-text loops (reproduced; control 0.715 over four). Split by arm, treatment A (no flags) runs at 0.81 as a mean of transition ratios (0.77 pooled) and Arm B (the arm A says to start from) at 0.51 (0.41 pooled) (my script). With Arm B's own r and R1 = 16.5 the no-cut model gives 2.8 to 4.3, against Arm B's realised mean of 3.5, so the model reproduces Arm B. A's 4.1 for Arm C is then "no gain over Arm B". Applying B:407's cut factors (0.63 to 0.88) on top of Arm B's own r gives 1.1 to 3.3 at R1 = 16.5, and 0.8 to 2.4 at R1 = 12. |

**What I take from it.** The 4.1 is one cell of a sensitivity grid and not the corrected forecast. Each cell rests on n = 4 transitions per arm, so the grid shows how little the data pin down, not a better estimate.

| R1 assumed | r = 0.42 | r = 0.50 | r = 0.58 | Arm B r (0.41 to 0.51) with cut |
|---|---|---|---|---|
| 9 (treatment A level) | 1.6 | 2.3 | 3.0 | 0.6 to 1.8 |
| 12 (pooled) | 2.1 | 3.0 | 4.0 | 0.8 to 2.4 |
| 16.5 (Arm B level) | 2.9 | 4.1 | 5.6 | 1.1 to 3.3 |

Updated forecast, labelled judgment: central 3.3, band 1.1 to 5.6. P(mean at most 3) about 0.4, P(bar a, every replicate at most 3) about 0.2 to 0.25. The carried-escalation term I conceded in rB:66 pushes up; Arm B's own lower r pushes down; I leave the net near the old centre but with a wider band. The forecast never decided between the designs (calibration and termination do), so I do not defend a number beyond this.

### 2. Remaining A criticisms (rA:63-74, r2A:35-39)

| # | Criticism | Answer |
|---|---|---|
| A1 | Reviser grants its own overrides (B:178), worst case 2 + 4 = 6 doubled findings (rA:65) | **Concede** (already rB:70). Drop the reviser-side `override:` path; keep only the reviewer's `large` flag, which is A's `L`. |
| A2 | Cycle cap `enforce` reverts the highest-gross findings first, which are the CRITICAL ones (B:211) | **Concede.** The order is wrong. Revert lowest-severity, smallest-class findings first, or use a fixed cap (C-005). See positions. |
| A3 | A 12-word minor budget reopens chain class A (B:176-178) | **Concede** (rB:69). Zero. B:226 and B:176 contradict each other and B:476 half-admits it. |
| A4 | An eighth bullet breaks seed:41 | **Concede** (rB:67). Fold into bullet 6 and a section. |
| A5 | Ids are free in the spec (B:165) against B's own evidence (B:476) | **Concede.** Ids belong in the ledger only. |
| A6 | The repository file breaks `test_worker_contract.py:831-839` | **Concede** (rB:68). Drop `## Unattended mode` from the repository file. |
| A7 | Exit 2 means over budget but argparse also exits 2 | **Concede** (X-004 to C). |
| A8 | The 3.5 to 4.5 band reads as "promising" instead of failing the bar | **Concede, and the point is stronger than A made it.** AR:23 calls a 3.5 mean "NOT MET". B:425 must read "bar not met; extend to four replicates as research, not as a pass". B:426 also lacks the spread condition (c) that B:378 requires (AR:25 shows (c) failing for the proxy). Row 6 of B:419-426 must add it. |
| A9 | Five subcommands and 20 to 31 calls (B:303, B:436) | **Concede in part.** Fold `hash` into `snapshot`, and `verify` into `check`. I keep `enforce` as its own verb (see A13). |
| A10 | The `@`-anchored sed misses invocations without ` @` (rA:74) | **Answered by A.** r2A:39 and r2A:79 verified that T05, T07 and T09 each contain `/sc:spec-panel @` once and T06, T08, T10 none; A withdrew it. I re-counted the templates directory: T07 and T09 contain it once, T08 and T10 zero. |
| A11 | Even split of a shared site's words across two ids (B:159) (r2A:37) | **Concede.** One owner per hunk (C's rule, C:62, C:88); other ids may be linked but add no budget. |
| A12 | Approximate matching (40-character substring, 10-word prefix) feeds an automatic revert (r2A:38) | **Partly concede.** The revert itself is exact (baseline bytes), the approximation only chooses attribution, and the error direction is over-revert, which is the safe direction for the budget. `check` runs again after `enforce`. But a wrongly attributed hunk can revert a good fix, so the replay harness (B:479) must report a mis-attribution rate, with a pre-agreed ceiling, before any worker runs. |
| A13 | Replace `enforce` by a `check --revert` flag (r2A:36) | **Contest.** The authoritative re-review run that I adopt from A must be read-only. The T07 and T09 templates say "write ONLY your output file; planning only, no edits to the spec or any other file" and "write ONLY that file; do not edit the spec" (verified in the templates). A mutating flag on the same verb that the reviewer runs is one typo from a violation, and `check` must also be stdout-only in reviewer use (A's `<stem>-fixcheck.json` file, A:86, would break T07). Keep "only `enforce --in-place` ever writes the spec" (B:211) as a safety property. |

### 3. C's criticisms of B (rC:64-76, rC:84-94)

| # | Criticism | Answer |
|---|---|---|
| C1 | Minor allowance contradicts a minimal-fix contract (rC:66) | **Concede.** Zero. |
| C2 | Self-granted exceptions (rC:68) | **Concede.** As A1. |
| C3 | Automatic rollback acts on approximate matching and a checker should validate, not overwrite (rC:70) | **Partly contest.** See A12 for the safety direction. C's own alternative (admit nothing and keep the last accepted spec, C:96) discards good fixes and C concedes the coupling problem anyway (rC:86). I keep script-side revert of whole findings, with C's coupled-revert correction. |
| C4 | `named` is informational, so out-of-scope edits pass (B:168) (rC:72) | **Partly concede.** C's registered-target check is the easier invariant to test. I keep it informational on evidence: B:447 shows both failure modes in the logs (ctl-r1 R2 N4 and N2 are "residue of round-1" findings that propagation would prevent; flg-r2 N3 and N6 are what propagation caused). A hard target gate trades one for the other. Decide when `named: no` shares are measured (B:475). |
| C5 | The failure table softens the bar (rC:74) | **Concede.** As A8. |
| C6 | An FR-8/FR-9 GAP graded minor gets the minor budget (B:481) (rC:76) | **Concede, verified.** SP:259 (bullet 2): "CRITICAL and FR-8/FR-9 findings are blocking". B:128 says the same, and B:481 then encodes a grader inconsistency as a minor budget. A hard-gate or CRITICAL finding graded minor must be an input error (exit 1), as C:43 does, not a budget class. |
| C7 | B:98's 11 of 17 over-cap result does not support "1 to 3 escalations" (rC:161) | **Concede** (A-004). A-004 in my table is "B, as a termination mechanism", not as a prediction. |

### 4. A correction to my own Round 1

I endorsed "C contradicts itself (C:90 against C:167)" on X-003 (rB:121). That was wrong. C:167 says each added paragraph "cites its finding id in the external fix ledger", which puts the id in the ledger and not in the document, the same as C:90. The diff's X-003 contradiction is overstated for C; B (ids free, B:165) is the only outlier. I withdraw the claim.

## Updated assessment

**A, after its defence.** A conceded 10 of 12 criticisms fully and 2 in part (r2A:31), and its Round 2 text now lands almost where B does: 80/120 caps, a script-side revert, the ledger inside the disposition file, hash plus stale-base refusal, no extra files written by workers. What still separates A from the merge, and why it is good:
- **Actor placement.** The reviewer writes every checker input and the reviser and the re-review read the same command line from the report. No coordinator duty. This is the best answer to the unbriefed-coordinator defect (X-012) and I take it.
- **Reviewer-only override, no ids in the spec, seven bullets, `## Unattended mode` dropped, the condition-word counter, the four causal falsifiers.** All verified or conceded. I take them.
- **What I would not take from A.** (1) The `check --revert` fold (A13): the re-review run must be read-only under the T07 and T09 ownership clauses. (2) The `-reviewed.md` copy and the `-ledger.jsonl` file, which A itself dropped (r2A:18). (3) The 4.1 re-basing (response 1): it keeps a 427-blend r on an Arm B R1. (4) Its "continue without the checker" rule, which A itself now drops (r2A:26).
- **A's A-004 position is the weakest of its R1 text** and A now concedes it (r2A:13). The remaining weakness is its forecast of 2.5, which assumed a 40-word cap that nobody now defends; A has not replaced it with a derivation.

**C, after its defence.** C's Round 1 text is honest about its own limits (rC:80 concedes the coordinator gap as "a blocking design defect", rC:82 withdraws the 1/1 forecast, rC:86 accepts the partial-admission coupling). Three things in C are better than B and I now take them:
- **Fail closed on a missing or stale physical input** (C:126). It is the house style of SP:258 bullet 1 ("never fall back to a first review"), and a review slot is the scarcest resource in the loop (3 reviews, SP:261). I move C-019 and X-007 to C.
- **A structural check that a hard-gate or CRITICAL finding is blocking** (C:43). It turns B:481's grader inconsistency into an input error. I move C-015 to C.
- **A fixed gross cycle cap that includes overrides, in bytes as well as words** (C:62), and the fresh-worker valid and invalid probe (C:289). B's relative 10% cap reverts in the wrong order (A2) and a probe proves delivery where a pre-flight hash only proves the script runs. I move C-005 and C-020 to C.

What I still reject in C: coordinator-run `freeze`, `check` and promotion with no route through the briefs (X-012; C conceded); all-or-nothing admission after a second failed check (C:96); a mandatory `wrong_outcome` JSON field on every blocking MAJOR for review 1, which changes the first review (AP-15) and is not needed by the budget; the removal cap (X-009; B's data put reviser removals at 84 to 379 words a cycle, so it rarely binds but adds a failure path to the cheapest fix); and seven new files with plugin mirrors that no test requires (new evidence 4). C's byte-exact reconstruction remains the strongest integrity invariant. With A's amendment (the checker finds each `before` string and computes the byte offsets, so the model supplies no offsets) it becomes buildable, and it is the right second-stage hardening after the replay harness shows the unit-diff attribution error rate.

**Where the merge should land (analyzer's view).**
1. Actors and delivery: A. Calibration, evidence, termination: B. Contract details and fail-closed: C.
2. Order of work: replay harness over the six recorded loops first (B:479), with a pre-agreed mis-attribution ceiling; then a one-replicate pilot to see whether a literal-minded reviser runs the script (B:451); then the n = 2 arm.
3. Forecast: a stated range (1.1 to 5.6), not 2.5, 3.0 or 1.0. The pre-registered fail line stays at the seed bar (mean above 3 fails), as A and C have it.

## New evidence

All read-only; the script ran under a private `/tmp` directory and was removed.

1. **R1 versus R3 across the six recorded loops** (AR:13; my script). Correlation -0.54, n = 6. Per-loop R3/R1: 0.73, 0.33 (control); 0.67, 0.56 (treatment A); 0.38, 0.06 (Arm B). Per-arm mean of transition ratios: control 0.715, treatment A 0.81, Arm B 0.51. Pooled sums: 0.718, 0.767, 0.409. With Arm B's own ratios and R1 = 16.5 the no-cut model gives 2.8 to 4.3 against a realised 3.5. Use: A's 4.1 re-basing does not follow, and neither does my 3.0. The full grid is in the response to criticisms, section 1.
2. **The re-review ownership clauses, verified in the S1 templates.** T07: "Ownership: write ONLY your output file; planning only, no edits to the spec or any other file". T09: "Ownership: write ONLY that file; do not edit the spec". T08: "edit ONLY the spec and write ONLY disposition-round2". Consequences for the merge:
   - The re-review's authoritative `check` run (A's design, adopted) must write nothing: stdout only, no receipt, no `-fixcheck.json`.
   - B's `.fixcheck/` writes at the reviser (T08) are still a literal conflict (B:452 row 7). The conflict is weaker than A's reviewer-authored file because the script writes it, but it is not zero. The pilot (B:451) decides.
   - The reviser's ledger inside the disposition file (B:134) is the only variant of the three that fits all three clauses.
3. **A baseline copy is already a coordinator duty in 427, and the S1 harness already makes it before each reviser.** SP:261 (bullet 4): "The coordinator keeps the review count, the prior-findings file and the saved copy". The coordinator log (lines 59 to 69) shows history copies saved by the coordinator at fixed paths, and the file times in `exp346-ab-flg-r2/.dev/orca-command-refactor/specs/history/` are 12:49 for `spec-v1-draft.md` (before review 1) and 13:12 for `spec-v2-after-round1.md` (after fix cycle 1, before review 2). Use: the reviewer's `reviewed_sha256` can be cross-checked against that existing copy at no cost, and a script-written `base-<N>.md` is redundant wherever the path is named. Limit: T06 and T08 do not name the path, so the reviser still cannot find it without a brief change; I keep `snapshot` as the fallback.
4. **No test forces a plugin mirror for a new command.** `tests/commands/test_routing_plugin_parity.py:41-47` mirrors four named commands only (`help`, `recommend`, `workflow`, `implement`) plus the `sc-recommend` tree. `tests/skills/test_spec_panel_review_loop.py:19-22` pins `spec-panel.md` in `src/` and `plugins/` only, and its T3 seven-bullet pin (line 83) is on those two files. Use: this closes my own UNVERIFIED at B:248 (no mirror is required for `spec-panel-minfix` or its skill) and removes the test-based argument for C's mirrors and design doc (C-030). The seven-bullet limit for the variant rests on seed:41, not on that test; the pin binds at promotion (B:480).
5. **C:167 is consistent with C:90.** Verified in the file: bullet 6 says each added paragraph "cites its finding id in the external fix ledger". The X-003 contradiction in the diff and in my Round 1 does not hold for C (response 4).
6. **FR-8/FR-9 are blocking by rule.** SP:259 (bullet 2) verified. B:128 states this; B:481 then contradicts it. The checker should reject a hard-gate or CRITICAL finding graded minor as an input error.

## Updated per-point positions

"Tie" means the letter is a nominal lean. Letter changes since Round 1: C-005, C-015, C-019, C-020, X-007 moved to C; C-016 and X-002 moved to A. C-008 keeps its letter with amended content.

| id | preferred (A/B/C) | changed since R1? | reason |
|---|---|---|---|
| S-001 | B | no | Tie: the same eight sections in seed order in all three. |
| S-002 | B | no | Tie: heading count does not touch any criterion. |
| S-003 | B | no | Six evidence tables, replicated by A (r2A:13) and by me (rB:34). |
| S-004 | A | no | Steps grouped by actor and phase are the easiest to build from; B's reference H3s interrupt the steps. |
| S-005 | B | no | Tie with A: literal bullet, section, script outline and test list per artifact. |
| S-006 | B | no | Derivation tables let a reader recompute the forecast, and A did (response 1). |
| S-007 | B | no | Detection, mitigation and residual columns per risk. |
| C-001 | B | no | Every finding listed with a derived class; add C's check that a hard-gate or CRITICAL finding is blocking (C:43). |
| C-002 | B | no | 80/50 needs the smallest cut (34% against 48% and 66%, rB:34); A withdrew 40. |
| C-003 | B | no | Tie with C: 120 gross; B adds net and add-only caps. |
| C-004 | A | no | Zero edits for non-blocking findings; B, A and C now agree. |
| C-005 | C | yes | A fixed gross cap that includes overrides, in words and bytes (C:62). B's relative 10% cap reverts the CRITICAL fixes first (A2). |
| C-006 | B | no | Universal and exec-recipe gates; add A's condition-word counter and C's byte counters. |
| C-007 | B | no | The ledger inside the disposition file fits T08 "write ONLY disposition-round2" (new evidence 2). |
| C-008 | B | yes (amended) | Unit diff with the capital-letter lookahead, but one owner per hunk (C:62, C:88) instead of an even split. The replay harness gates the mis-attribution rate. |
| C-009 | B | no | Reviewer hash plus stale-base refusal, with no coordinator duty; cross-check against the coordinator's saved copy (new evidence 3). |
| C-010 | B | no | Tie: `install_skills.py` strips only `sc-`, so all three folder names install (A and I both read it). |
| C-011 | A | no | One invocation for the model; fold `hash` into `snapshot` and `verify` into `check`; `enforce` stays its own verb (A13). |
| C-012 | C | no | argparse keeps exit 2; crash 70; separate input, hash and output failures. |
| C-013 | B | no | Script-side revert of whole findings guarantees termination; C's admit-nothing discards good fixes. Add the coupled-revert correction (A-002). |
| C-014 | A | no | The reviewer grants it, one per report; B's reviser-side path is dropped (A1). |
| C-015 | C | yes | A hard-gate or CRITICAL finding graded minor is an input error (C:43, SP:259), not a minor budget (B:481). |
| C-016 | A | yes | Bullets 2, 5, 6 amended in place, seven bullets, the budget numbers only in the script. A's bullet 6 carries the command line, so it needs no coordinator duty; C's text depends on a coordinator freeze (X-012). C:167 is not a contradiction (response 4), so this is about delivery, not ids. |
| C-017 | A | no | No ids in the spec; the id lives in the ledger. C is equivalent (C:90, C:167); B is the outlier. |
| C-018 | A | no | The re-review's own run is authoritative, in stdout-only mode; the report copies numbers and ids, never ledger prose (B:111). |
| C-019 | C | yes | Stop on a missing or stale receipt or physical input, as SP:258 bullet 1 does. A review slot is the scarce resource; a voided replicate is then impossible by construction. |
| C-020 | C | yes | The fresh-worker valid and invalid probe proves delivery and execution (C:289); my pre-flight hash only proves the script runs. Keep both. |
| C-021 | B | no | The `@`-anchored pattern touches exactly the review briefs (T07, T09 verified; A verified T05). |
| C-022 | B | no | Tie with A: no coordinator duty in either; C's duties have no route through the briefs. |
| C-023 | A | no | The repository file must drop `## Unattended mode` (`test_worker_contract.py:831-839`); the experiment file still uses the 472-line base (X-014). |
| C-024 | B | no | Only forecast with a derivation, but restated as a range, 1.1 to 5.6, central 3.3 (response 1); P(mean at most 3) about 0.4, P(bar a) about 0.2 to 0.25. |
| C-025 | B | no | 14.4% replay-derived and a 16.1% arithmetic ceiling; C's 21.3% byte bound should be stated beside it. |
| C-026 | A | no | Fail line at the seed bar, with causal falsifiers; B:425 and B:426 must be corrected (A8). |
| C-027 | B | no | Itemised cost breakdown. |
| C-028 | A | no | Tie: one short fit assessment per adopter; out of scope for all three. |
| C-029 | B | no | Chain taxonomy and cap replay; replicated twice (rB:34, rA:101). |
| C-030 | B | no | Tie with A: behaviour tests plus the `enforce` property test; no plugin mirror is required by any test (new evidence 4), so C's mirrors are scope. |
| X-001 | A | no | Zero for non-blocking findings; all three agree. |
| X-002 | A | yes | Seven bullets, bullet 6 replaced with the command line in it; C is equal on count but its text depends on a coordinator freeze. B's bullet 8 is conceded. |
| X-003 | A | no | No ids in the spec. Withdrawn from Round 1: "C contradicts itself" (response 4); the only outlier is B. |
| X-004 | C | no | The only layout that keeps argparse's exit 2 free; crash 70. |
| X-005 | B | no | The script reverts whole findings; add the coupled revert; revert order lowest class first. |
| X-006 | A | no | The reviewer grants; not the reviser (B), not an unbriefed coordinator (C). |
| X-007 | C | yes | Stop with a named input error on a missing or stale input; same reason as C-019. |
| X-008 | B | no | Numbers and ids only; flg-r2 round 3 judged statuses from the spec text, not from the disposition. |
| X-009 | B | no | Tie with A: free deletes keep delete-first worth doing; report removed words per cycle, do not cap them. |
| X-010 | B | no | Two independent re-counts (rB:34, rA:101) against A's lower-bound attribution. |
| X-011 | B | no | Size alone does not separate parents with blocking children (B:87); mild lean only (rB:35). |
| X-012 | B | no | Tie with A: no coordinator duty; C conceded the gap (rC:80). |
| X-013 | A | no | The fail line is the seed bar, and AR:23 calls a 3.5 mean "NOT MET". B's "promising" row stays a research action, not a pass. |
| X-014 | B | no | The 472-line base for the experiment file changes one thing at a time (AR:6). |
| A-001 | B | no | QUALIFY stands: B's lookahead splitter and word caps that do not move with unit boundaries; the replay harness gates it before any worker run. |
| A-002 | B | no | QUALIFY stands: `enforce` reverts whole findings; add a `depends:` cascade, a coupled revert for hunks linked to more than one id, and measure with `attacks:`. |
| A-003 | A | no | QUALIFY stands: zero minor budget keeps deferred text out of the changed-line scope; report the proxy and the 427 blocking count separately (C:302). |
| A-004 | B | no | Rejected as a prediction, kept as a termination mechanism: `enforce` converts a missed cut into a recorded escalation; pre-register the 100/60 retry (B:424). |

Tally (55 rows): B 32, A 16, C 7. Round 1 was B 37 (including ties), A 14, C 4 over the same 55 rows (counting the nominal letter of each tie); the seven moves are listed in the first line of this section.

### Variant C Rebuttal (haiku:backend)

# Round 2 — Variant C

## Response to criticisms

Citation key: `A`, `B`, `C` are the three variant files named in the assignment; `r1A/B/C` and `r2A/B` are their corresponding debate files. Their common folder is `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/brainstorms/346-minfix/nested/adversarial-1/adversarial`. Numbers after a key are source line numbers, not claims that a proposed checker exists.

Additional independently read sources:
- `P` = `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/src/superclaude/commands/spec-panel.md`.
- `ARM` = `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase4/ARMB-REPORT.md`; `AB` is `AB-REPORT.md` in that same folder.
- `R1`, `R2`, `R3`, `D2` = `spec-panel.md`, `spec-panel-round2.md`, `spec-panel-round3.md`, `disposition-round2.md` under `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r2/.dev/orca-command-refactor/review/`.
- `T07`, `T08`, `T09` = `T07-R2-reviewer.TEMPLATE.txt`, `T08-R2-reviser.TEMPLATE.txt`, `T09-R3-reviewer.TEMPLATE.txt` under `/home/coder/workspaces/worktrees/IronClaude/exp346-p1-logs/.dev/experiments/346-validation/phase2/S1/briefs/templates/`.
- `W` = `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/tests/skills/test_worker_contract.py`; `PAR` = `/home/coder/workspaces/worktrees/IronClaude/bs346-minfix/tests/commands/test_routing_plugin_parity.py`.

The following covers the criticisms in r1A:76–96, r1B:54–62, their related comparison claims and both earlier Round 2 rebuttals. Amendments below are debate positions, not edits to the original variants.

| Criticism and source | Answer, evidence and resulting position |
|---|---|
| Unbriefed coordinator must freeze, pin, check, authorize and promote (r1A:78–85; r1B:56; r2A:41–46; r2B:77). | **Concede.** C:47–49,94,126,271 assign those duties but do not deliver instructions to the parent through the review worker. Existing coordinator duties are count/report/copy, not this protocol (P:261). Prefer A's actor placement, amended by B's in-disposition ledger and reviewer hash. C's independent coordinator pin cannot simply be claimed to survive that simplification; preserving it would need an explicitly authorized coordinator change. C is not experiment-ready. |
| Reviser must invent byte offsets; A originally blamed multibyte S1 text (r1A:86; r1B:58; r2A:46; r2B:77). | **Concede the authoring defect; accept A's correction of its encoding claim.** C:45 computes reviewer-target offsets, but C:81,90 still demand reviser edit offsets. Have the checker locate the exact `before` string uniquely within the registered target and compute positions; ambiguity remains an error. This is a proposed correction, not something C already specifies. Keep exact reconstruction, not fuzzy matching. No encoding recount was run here; r2A:78 corrects r1A's draft claim. |
| Every finding needs heavy JSON, unique targets and a blocking-MAJOR wrong-outcome field; this changes review 1 (r1A:87; r2B:77). | **Concede cost and first-review change; contest that the outcome concept is new or useless.** P:259 already requires a concrete wrong outcome for ordinary blocking MAJORs; C:43 makes its presence inspectable, not true. Keep all-finding identity/grade coverage and hard-gate validation, but prefer B's lighter findings block for the first experiment; avoid a duplicated explanation field when the report already states it. Non-blockers need no edit targets. Target quality and authoring failures still require measurement. |
| One failed byte on the second attempt loses good fixes; all-escalation is cheap (r1A:88; r1B:57; r2A:106; r2B:54,77). | **Concede usefulness risk, not permission to admit failed accounting.** C:96 permits valid edits to remain during the single cut-down; whole-cycle refusal happens only if that second candidate still fails. C:98,257 distinguish accounting acceptance from unresolved obligations; C:332 names all-escalation. Retain a fail-closed final admission boundary. A/B's selective revert may preserve useful fixes, but neither numerical pass nor whole-finding rollback proves retained changes are mutually consistent. Coupled changes must be kept/dropped together; undeclared dependencies remain a semantic risk. |
| Removal caps obstruct delete-first and rarely bind (r1A:89; r1B:61; r2A:132; r2B:77). | **Concede the numeric cap as an initial policy.** C:338 itself says removal limits do not prove obligation preservation. Prefer free deletions within registered scope, with removals reported and the original wrong outcome independently rechecked. The cited 84–379 figures are cycle totals (B:20), whereas C:58–59 are per-finding caps, so those totals alone do not establish how often the cap binds. Remove it for unsupported calibration and conflicting deletion incentives, not a demonstrated low binding rate. |
| C's 60/512 constants and 1/1 proxy forecast lack calibration or derivation (r1A:90; r1B:57,59; r2A:41; r2B:77). | **Concede.** Withdraw the 1/1 forecast, not merely its confidence label. Prefer B's replay-informed 80/120 word starting values pending common-method replay; no historical unconstrained fix size proves a minimum correct size. Reconcile byte limits with the chosen word caps during replay, rather than retaining 512 bytes and calling 80 words the effective allowance. C's 600-word/6,144-byte cycle bounds are policy choices, not convergence evidence (C:62,317,352). |
| C adds unnecessary mirrors/documentation and repeats constants (r1A:51,92; r1B:60; r2B:77,94). | **Concede narrower scope and drift risk.** Expanded C:149–156 actually names nine files, not seven: command and mirror, helper/script and their two mirrors, two tests, one document. Prefer command/helper/script/two-test initial implementation, deriving copied tables from tested constants as A:183,250 proposes. PAR:41–47 requires four named command mirrors, not this new command; that does not prove no other test anywhere could require one. No blanket test-suite absence claim was independently established here. |
| C contradicts itself about finding ids in the spec (r1A:93,141,158; r1B:121; still r2A:126). | **Contest.** C:167 explicitly says the id is cited **in the external fix ledger**; C:90 says the document needs no decorations. They agree. B correctly withdraws this criticism at r2B:60–62,95. A's surviving Round 2 assertion is unsupported. Prefer external attribution and no free-word exemption for inline tags. |
| Copying current command preserves an Unattended heading and breaks enumeration (r1A:94; r1B:15; r2A:49; r2B:39). | **Concede, independently verified as static incompatibility, not a test run.** P:451–461 contains that heading. W:831–839 enumerates all command files and requires an exact approved set. The proposed name would add an unapproved member. Take A's omission of that section/associated usage flags for the repository variant; take B's exact historical comparator base for the experiment (ARM:6). Do not weaken the enumeration test. |
| Replacing the copied command's template lookup is an unrelated second change (r1A:95). | **Concede experimental confounding; retain the compatibility concern.** P:220 names a maintainer-source template path, and C:160 discloses replacing it. A controlled minfix experiment should not count a repair to that separate mode as minfix's effect. Prefer the comparator-matched build and isolate any required installed-path correction as an explicitly disclosed compatibility deviation, not invisible cleanup. |
| Helper name is tied to one command (r1A:96; r1A:60; r2A:81). | **Concede naming portability; no demonstrated install defect.** Prefer a neutral helper name (A or B). A/B report all three install safely after reading the installer; I did not independently inspect that source in this round, so this is not new packaging evidence. Folder renaming is not a convergence mechanism. |
| Coordinator grants amount to self-approval without a user (r1B:62; r2A:46; r2B:77). | **Partly contest, then change the preferred actor.** C:102 permits logged user approval **or explicit reviewer recommendation**, not the coordinator's invented rationale; C:122 admits provenance is trusted. Executing a genuine reviewer recommendation is not the reviser granting itself room. But the delivery defect remains. Prefer A's reviewer-only, single larger-fix decision; adopt r2A:15's reasoned treatment of changed-origin repairs rather than an absolute ban. Edit-digest binding is stronger only where a real later authorization channel exists; reviewer preauthorization is not the same guarantee. |
| Reviewer reads ledger explanations, and mandatory check output violates reviewer ownership (r1A:108; r1B:126; r2B:46,89–92). | **Concede both interface issues.** C:128 checks actual wrong outcomes before ledger claims, but there is no need to expose reasons afterward. Keep A's authoritative rerun with B's numbers/ids/line spans only. T07:1 forbids any other file; T09:1 permits only its report. C:190,218's required output file needs a read-only, stdout-only reviewer path. Do not give reviewers a mutating check flag; B's separation of checking from rewriting is better than r2A:36's combined verb. |
| Metrics omit carried-vs-new, costs are optimistic, and a skipped checker remains possible (r1A:59; r1B:41; r2A:119–120). | **Partly concede.** Add A's explicit carried/new column and B's per-role cost accounting. C:302,307,321 retain open obligations and escalation diagnostics, so omission of a named column is not permission to discard them. C:137,342 admits skipping is possible; receipts plus actual fresh-worker execution show delivery, not harness enforcement. No runtime/cost/per-finding recount was performed here. |
| Exact rollback plus a post-check makes B's heuristic selection safe enough (r2A:38; r2B:45,54). | **Contest semantic safety, accept the bounded operational benefit.** B:211 can restore exact baseline text and still select the wrong finding's hunk. A second budget check proves numerical compliance, not obligation preservation. R2:28,37 documents an F2/F11 interaction; whole-finding revert alone does not remove it. B's mis-attribution replay gate is necessary evidence, but its tolerated rate is not yet specified or measured. Retain C's exact selection/reconstruction, with tool-derived positions. |

These are merge recommendations, not authorization to implement or run the experiment.

## Updated assessment

**A improves substantially after its defenses.** It withdraws the 40-word calibration and its associated growth/proxy forecasts, abandons extra reviewer/ledger files, accepts hashes, one budget owner, failure on missing inputs and a byte cycle cap (r2A:13,17–29). Actor-local delivery, reviewer-only larger-fix decisions, seven bullets and an authoritative next-review check remain its strongest contributions. I now prefer that operating structure over C's parent-owned transaction machinery for this particular experiment.

Two objections remain. First, combining checking with a mutating flag (r2A:36) weakens the reviewer/reviser boundary; B's separate read-only check is better (r2B:46). Second, A's assertion that ASCII makes the word/byte ratio stable is not a bound: arbitrarily long ASCII identifiers still defeat conversion from words to bytes (r2A:29). Retain the actual byte counter/cap. A's repeated id-contradiction claim also needs withdrawal, as B has done.

**B remains the best empirical starting point, not the strongest admission contract.** It now accepts zero minor edits, no reviser-approved exemptions, single-owner charging, hard-gate validation, failure on stale/missing inputs and C's cycle cap/probe (r2B:34–44,57,72–75). Its placement of the ledger inside an already authorized disposition is better than C's separate JSON file. Its distinction between read-only checking and explicit rewriting is worth preserving even if the merge ultimately rejects automatic rewriting.

B still leaves named scope informational (r2B:55; B:475), and its defense of over-revert as safe is safe only for the numerical budget, not for the outstanding obligation. A partial revert can preserve a new rule while removing its supporting definition. Replay should report attribution errors and preservation of complete coupled edits, not just a final exit zero. Script-generated files are still writes caused by the worker; a pilot can reveal noncompliance but cannot authorize an otherwise forbidden write. This is a remaining protocol conflict, not a question a successful pilot automatically settles (B:452).

**Forecast dispute.** Prefer B's sensitivity treatment over either C's withdrawn 1/1 or A's proposed single rebased value. ARM:6,32 confirms that Arm B's extra flags start only at R2/R3, so its high R1 counts are not established effects of those flags. ARM:13 confirms the different R1 pairs and large final spread; ARM:35–36 preserves timing and exposure caveats. B correctly notes that scaling one regime's starting count with another regime's transition rate is only a sensitivity case (r2B:18–28). Its new central number and probabilities remain judgment, however; neither that range nor the observed R1 range is a validated predictive interval. No variant has measured a budget-driven cut-down success rate.

**Updated merge recommendation.** Use A's role delivery and reviewer authorization; B's lighter findings block, existing-file ledger, comparator-matched build, replay and per-role cost accounting; C's exact reconstruction with checker-derived locations, single-owner charging, hard-gate validation, deterministic failure contract, gross byte/word cycle ceiling and fresh-worker valid/invalid probe. Remove the numeric removal ceiling, unnecessary mirrors and separate design document from the initial implementation. Keep all actual blocker outcomes and severity-proxy accounting independent of policy acceptance. Do not claim that this hybrid exists or has proven convergence.

## New evidence

These are newly connected ground-truth observations for this rebuttal, not new experimental measurements. Previously cited chains, the enumeration test and B's mirror-test observation are corroborations above, not claimed discoveries.

1. **An untouched MAJOR note demonstrably persists through both re-reviews.** R1:121–123 grades F16 MAJOR/FR-8 GAP but non-blocking. R2:42 explicitly says “No text added”, leaves it open and calls it non-blocking; R3:47 says neither revision reopened it and it remains a note. This directly qualifies r2A:140/r2B:157's suggestion that zero edits keeps deferred text out of later reports: it may stay out of the new-findings pass and still persist in status prose. It also shows a second concrete hard-gate/grade conflict beyond F22. Do not silently rewrite the published proxy or assume this note must already have been counted as a fresh R3 MAJOR; the published counting convention and a separate carried-obligation tally must be distinguished. The examples establish persistence, not its exact contribution to the historical proxy.

2. **The real reviser already declined an extra copy on ownership grounds.** D2:61 records that no new baseline was written because the brief allowed only the spec and the disposition file. This is observed behavior, not just the hypothetical literal-minded worker in B:452. A proposal that has that worker create `.fixcheck/`, state or receipt files still needs a contract-compatible delivery route; moving the write into a script does not change the authorized write set. Reuse the existing saved copy where available and keep reviewer checking stdout-only. If required extra writes cannot be assigned without changing briefs, report that delivery defect rather than declare it settled by a pilot.

No test, checker implementation, token/offset recount, installation or live loop was run. No conclusion about runtime integrity or convergence follows from these file reads.

## Updated per-point positions

The preferred letter selects a component, not approval of that variant unchanged. “Changed” compares with r1C:102–152; amendments that keep the same preferred letter are stated in the reason. For A-001..A-004, Round 1 gave a response rather than a preferred letter, so “no” means the QUALIFY/REJECT stance at r1C:158–161 is unchanged; C is the closest preferred accounting/measurement treatment.

| id | preferred (A/B/C) | changed since R1? (yes/no) | reason |
|---|---|---|---|
| S-001 | C | no | Same eight-section order; retain the explicit admission invariant as the opening, not a success forecast. |
| S-002 | C | no | Compact operational sections remain readable; heading count is not evidence of correctness. |
| S-003 | B | no | Chain classes, negative predictors and cap replay expose the strongest empirical case (B:63–98). |
| S-004 | A | yes | Actor/phase organization makes delivery explicit; C's parent-owned transitions do not reach their actors. |
| S-005 | A | no | Per-artifact responsibilities and derivation pins bound initial implementation scope. |
| S-006 | B | no | Growth arithmetic and proxy sensitivity are separate; use the Round 2 sensitivity correction, not the old point forecast. |
| S-007 | B | no | Detection, mitigation and residual columns make unresolved risks inspectable. |
| C-001 | B | yes | Use a lighter all-findings block with derived classes, adding C's hard-gate validation; avoid duplicate wrong-outcome prose. |
| C-002 | B | no | 80 added words is the better replay-informed starting choice, not a proven correct minimum; replay byte limits too. |
| C-003 | B | yes | 120 gross words with net/add-only controls; keep C's byte measurements but drop unsupported removal ceilings. |
| C-004 | C | no | Zero edits and explicit deferral per non-blocker; B now concedes its nonzero allowance (r2B:36). |
| C-005 | C | no | Gross cycle word and byte ceilings include grants and cannot be bought with deletions; numeric choices remain provisional policy. |
| C-006 | B | yes | Universal/check-recipe diagnostics plus A's condition counter and C's byte counts; no lexical detector proves semantic novelty. |
| C-007 | B | yes | Put the ledger in the authorized disposition file; preserve C's exact before/after text and one-owner schema inside it. |
| C-008 | C | no | Exact target-contained reconstruction; amend input to derive offsets from unique before strings in the checker. |
| C-009 | B | yes | Reviewer hash and stale-base refusal fit role delivery; use the existing saved copy. This is not C's independently pinned coordinator boundary. |
| C-010 | A | no | Neutral function-based helper naming; no argument that C's protocol suffix is swept by the installer. |
| C-011 | C | no | A small explicit preparation/check API with checking non-mutating; actor placement and stdout-only reviewer use need amendment. |
| C-012 | C | no | Deterministic JSON and distinct usage/input/hash/output/internal failures; reviewer use must not write an extra report file. |
| C-013 | C | no | One cut-down from the original baseline, then no admission if still invalid. Keep declared coupled edits together; reject unsafe partial salvage. |
| C-014 | A | yes | One reviewer-authorized larger fix is deliverable without new parent duties; require reasons when reverting a changed-origin parent would reopen a blocker. |
| C-015 | C | no | Reject hard-gate/CRITICAL minor-grade conflicts rather than assign a minor budget; P:259 supports it. |
| C-016 | A | yes | Actor-local brief/check instructions in seven amended bullets; C's external-id clause is consistent, but coordinator delivery is not. |
| C-017 | C | no | External attribution is already C's explicit wording; do not exclude inline finding tags/citations from actual added-text accounting. |
| C-018 | A | yes | The next review's own read-only check is authoritative; adopt B's numbers/ids/spans-only presentation. |
| C-019 | C | no | Missing, malformed or stale physical inputs stop admission, matching P:258. |
| C-020 | C | no | Fresh-worker valid/invalid execution probe tests delivery, not merely presence of an installed file. |
| C-021 | B | yes | For these S1 briefs the narrow invocation substitution is supported by both earlier Round 2 reads; inspect resulting briefs and retain the flags. |
| C-022 | A | no | No unbriefed new parent duties. A's reviewer-written copy is separately withdrawn; do not retain that part. |
| C-023 | B | no | Historical comparator base for the installed experiment; repository artifact also needs A's Unattended omission. |
| C-024 | B | no | Sensitivity with assumptions is preferable to C's withdrawn 1/1; Round 2 probabilities remain judgment, not measured success odds. |
| C-025 | C | no | The 21.3% bound is in actual bytes if two 6,144-byte caps apply; word-based forecasts are not byte guarantees. Withdraw confidence in the 15% point prediction. |
| C-026 | C | no | Keep proxy, every-control and spread tests; all-escalation cannot count as convergence. Add A's carried/new causal diagnostic. |
| C-027 | B | no | Per-role cost table is the most inspectable; all timings remain unmeasured estimates. |
| C-028 | C | no | Later adoption stays separate, with separate severity mapping and caps; no speculative adapter modes now. |
| C-029 | B | no | Whole-fix replay and child-chain analysis beat incompatible id-sentence calibration; no independent recount claimed here. |
| C-030 | B | yes | Smaller initial file set plus behavior/replay tests; import C's integrity fixtures and A's derivation pin, not unnecessary mirrors/document. |
| X-001 | C | no | Zero non-blocker edits, with every deferred id retained in accounting. |
| X-002 | A | yes | Seven bullets with actor-local obligations and no eighth bullet; C is equal on count and external attribution, not delivery. |
| X-003 | C | no | C:90 and C:167 agree: ids live in the external ledger. B has withdrawn the alleged contradiction. |
| X-004 | C | no | Distinct failure categories with usage exit 2 reserved and internal failure separate; no failure becomes acceptance. |
| X-005 | C | no | Validation never overwrites the specification; partial automatic recovery must not be mistaken for semantic atomicity. |
| X-006 | A | yes | Reviewer grants the bounded larger allowance; C's post-edit digest guarantee is not retained without a real approval channel. |
| X-007 | C | no | Stop on missing or stale inputs rather than spend a review on an unbudgeted candidate. |
| X-008 | B | no | Keep reviser explanations out of semantic judging; use actual spec/evidence plus computed ids and spans. |
| X-009 | B | yes | Free in-scope deletions, measured and independently rechecked; a numeric removal cap does not establish obligation preservation. |
| X-010 | B | no | Better-supported whole-fix measurement; A withdraws its conflicting 40-word calibration (r2A:13). |
| X-011 | B | no | Size alone is not established as the cause; detect defect classes and measure carried versus new findings. |
| X-012 | A | no | Local actor delivery answers the coordinator gap; file conventions cannot instruct a parent session. |
| X-013 | C | no | Preserve the complete pre-registered bar, including spread; more research after failure is not a pass. |
| X-014 | B | no | Exact historical 427 comparator text changes one thing at a time (ARM:6), unlike copying all current behavior. |
| A-001 | C | no | QUALIFY: exact quotes avoid splitter dependence, but quote uniqueness and tool-derived offset handling need executable replay/fixtures. |
| A-002 | C | no | REJECT assumed independence: coupled fixes must be admitted/dropped together; shared budget links do not reveal all semantic dependencies. |
| A-003 | C | no | REJECT automatic disappearance: F16 persists untouched through R2/R3. Separate the frozen historical proxy convention from carried severity/blocking obligations. |
| A-004 | C | no | REJECT one-retry success as a prediction. Bound retries, measure successful cut-downs and carry escalations; no cap-fitting rate has been observed. |

Recommended next step for the merge: produce one coherent actor/write-set contract before implementation planning, then replay its actual accounting rules and run the authorized delivery probe. This matters because a numerically strict gate that workers cannot execute is not a delivered treatment.

Only this debate output was created or edited. No code, tests, installation, Git or network operations were performed; runtime behavior and convergence remain unverified.

## Round 2.5: Invariant Probe

Full results: `invariant-probe.md` (fault-finder table INV-001..INV-032, with a suggested resolution for each UNADDRESSED HIGH item at IP:49-59).

- Total findings: 32
- ADDRESSED: 9 (INV-004, 010, 011, 017, 018, 022, 024, 025, 032)
- UNADDRESSED: 23 (HIGH 10, MEDIUM 13, LOW 0)

UNADDRESSED HIGH items (block convergence):

| ID | Category | Gap in the consensus |
|----|----------|----------------------|
| INV-001 | state_variables | The reviser's `snapshot` must write `.fixcheck/` files, but the T08 brief allows writing only the spec and the disposition file, so an obedient reviser leaves no receipt and the fail-closed re-review stops. |
| INV-002 | state_variables | Prior blocking findings carried into cycle 2 are not listed in the review-2 `fixbudget` block, so they get budget 0 and stay open into review 3. |
| INV-005 | guard_conditions | Real S1 review 1 grades FR-8 GAP findings (F22, F16) non-blocking, so the agreed hard-gate validation would stop cycle 1 with an input error that no actor can repair. |
| INV-006 | guard_conditions | The winning exit codes are C's, but the winning reviser steps and `enforce` triggers are keyed to B's codes, and C's action table assigns actions to the coordinator. |
| INV-007 | guard_conditions | A fail-closed stop before review 3 is neither a PASS nor a justified escalation, and no rule turns it into one. |
| INV-012 | count_divergence | The 600-word cycle cap is below the sum of per-finding caps for 13 blocking ids, and no agreed revert order decides which fixes survive. |
| INV-023 | interaction_effects | FR-8/FR-9 gap fills need guard branches, but the MAJOR class allows 1 normative and 1 condition word, so fills breach and escalate or re-trigger FR-8. |
| INV-026 | sufficiency_challenge | S1 chains show within-budget fixes with blocking children, so the budget alone does not drive review 3 to 3 or fewer. |
| INV-027 | sufficiency_challenge | In trt-r1, 5 of 6 review-3 blockers are guard GAPs from short revisions, and the condition-word list misses guard words such as `where`. |
| INV-028 | sufficiency_challenge | No cut-down success rate is measured; with 11 of 17 MAJOR fixes over cap, 4 or more carried blockers would fail the review-3 bar with no new findings. |

## Scoring Matrix

Winners are the per-point majorities in CV:5-61 (at least 2 of 3 advocates). Taxonomy levels come from a literal, case-insensitive whole-word scan of each point's row in `diff-analysis.md` for the protocol's signal terms (priority L3 > L2 > L1, default L2); the matched term is shown in brackets. Confidence calibration: unanimous 95%, or 90% when an advocate marked the point a tie; majority 70%, plus 10% when the dissenting advocate marked the point a tie with the winner or the winning variant's own advocate dissented (so both losing advocates conceded); split points are unresolved at 50%. No point is at 100% because no point was explicitly conceded by every advocate.

| Diff Point | Taxonomy level | Winner | Confidence | Evidence Summary |
|------------|----------------|--------|------------|------------------|
| S-001 | L2 | Unresolved | 50% | Each advocate chose its own variant, and A and B call it a tie: all three use the same eight sections in seed order (r2A:87, r2B:104, r2C:66). No majority exists. |
| S-002 | L2 | Unresolved | 50% | Each advocate prefers its own heading count (r2A:88, r2B:105, r2C:67), and B says heading count touches no criterion. No majority exists. |
| S-003 | L2 | Variant B | 95% | All three prefer B's six evidence tables, which A and B independently replicated (r2A:89, r2B:106, r2C:68). |
| S-004 | L2 | Variant A | 95% | All three prefer steps grouped by actor and phase; C moved to A in Round 2 because its own parent-owned transitions do not reach their actors (r2B:107, r2C:69). |
| S-005 | L2 | Variant A | 80% | A and C prefer a file table followed by one H3 per artifact (r2A:91, r2C:70). B's dissent is marked a tie with A (r2B:108). |
| S-006 | L2 | Variant B | 95% | All three prefer B's derivation tables, which let a reader recompute the forecast, as A did (r2A:92, r2B:109, r2C:71). |
| S-007 | L2 | Variant B | 95% | All three prefer B's detection, mitigation and residual columns per risk (r2A:93, r2B:110, r2C:72). |
| C-001 | L2 | Variant B | 95% | All three adopt B's all-findings block with a derived class, amended with C's hard-gate check; C moved to B in Round 2 (r2A:94, r2B:111, r2C:73). |
| C-002 | L2 | Variant B | 95% | All three adopt B's 80/50 MAJOR budget as fitting the measured blocking fixes, and A withdrew its 40-word cap (r2A:95, r2B:112, r2C:74). |
| C-003 | L2 | Variant B | 90% | All three adopt 120 gross words with B's net and add-only caps (r2A:96, r2C:75). B marks it a tie with C (r2B:113). |
| C-004 | L2 | Variant A | 70% | A and B agree on zero edits for non-blocking findings, B conceding its 12-word allowance (r2A:97, r2B:114). C keeps its own letter for the same zero-edit rule (r2C:76). |
| C-005 | L2 | Variant C | 95% | All three adopt C's fixed gross word and byte cycle cap including overrides; A and B moved to C because B's relative cap reverts CRITICAL fixes first (r2A:98, r2B:115, r2C:77). |
| C-006 | L2 | Variant B | 95% | All three adopt B's universal and exec-recipe gates, adding A's condition-word counter and C's byte counters (r2A:99, r2B:116, r2C:78). |
| C-007 | L2 | Variant B | 95% | All three put the ledger inside the disposition file to fit T08's single write target; C moved to B (r2A:100, r2B:117, r2C:79). |
| C-008 | L2 | Variant B | 70% | A and B adopt B's lookahead splitter, amended to one owner per hunk (r2A:101, r2B:118). C keeps exact target-contained reconstruction (r2C:80). |
| C-009 | L3 [state] | Variant B | 95% | All three adopt the reviewer hash plus stale-base refusal with no coordinator duty; C moved to B (r2A:102, r2B:119, r2C:81). |
| C-010 | L2 | Variant B | 70% | A and B call the folder name a tie because all three names install (r2A:103, r2B:120). C prefers A's neutral naming (r2C:82). |
| C-011 | L3 [state] | Variant A | 70% | A and B prefer one `check` invocation with B's revert folded in (r2A:104, r2B:121). C keeps its own two-subcommand API (r2C:83). |
| C-012 | L2 | Variant C | 95% | All three adopt C's exit layout: argparse keeps 2, crash is 70, and input, hash and output failures are separate (r2A:105, r2B:122, r2C:84). |
| C-013 | L2 | Variant B | 70% | A and B prefer the script-side revert of whole failing findings because it guarantees termination (r2A:106, r2B:123). C keeps admit-nothing (r2C:85). |
| C-014 | L2 | Variant A | 95% | All three give the override to the reviewer, one per report; B dropped its reviser path and C moved to A (r2A:107, r2B:124, r2C:86). |
| C-015 | L2 | Variant C | 95% | All three treat a hard-gate or CRITICAL finding graded minor as an input error; A and B moved to C (r2A:108, r2B:125, r2C:87). IP INV-005 challenges this rule against the real S1 review 1. |
| C-016 | L2 | Variant A | 95% | All three adopt seven bullets amended in place; B and C moved to A on delivery grounds (r2A:109, r2B:126, r2C:88). |
| C-017 | L2 | Variant A | 70% | A and B keep finding ids out of the spec, B conceding (r2A:110, r2B:127). C keeps its own equivalent external-attribution wording (r2C:89). |
| C-018 | L2 | Variant A | 95% | All three make the re-review's own read-only checker run authoritative, copying numbers and ids only; C moved to A (r2A:111, r2B:128, r2C:90). |
| C-019 | L2 | Variant C | 95% | All three stop on missing or stale inputs, as 427 bullet 1 does; A and B moved to C (r2A:112, r2B:129, r2C:91). IP INV-001 and INV-007 show this stop has no repair or escalation path. |
| C-020 | L3 [guard] | Variant C | 95% | All three adopt C's fresh-worker valid/invalid probe as proof of delivery; B moved to C (r2A:113, r2B:130, r2C:92). |
| C-021 | L2 | Variant B | 95% | All three adopt B's `@`-anchored substitution, verified to hit exactly the review briefs; A and C moved to B (r2A:114, r2B:131, r2C:93). |
| C-022 | L2 | Variant A | 80% | A and C reject any unbriefed coordinator duty (r2A:115, r2C:94). B's dissent is marked a tie with A (r2B:132). |
| C-023 | L2 | Variant B | 80% | A and C choose B's 472-line base for the experiment file (r2A:116, r2C:95). B's own advocate voted A because the repository file must drop `## Unattended mode` (r2B:133). |
| C-024 | L2 | Variant B | 95% | All three prefer B's derived forecast, restated with wider uncertainty (A about 4.1, B 1.1-5.6), and C withdrew its 1/1 (r2A:117, r2B:134, r2C:96). |
| C-025 | L2 | Variant B | 70% | A and B prefer replay-derived growth with C's byte bound stated beside it (r2A:118, r2B:135). C keeps its 21.3% byte bound (r2C:97). |
| C-026 | L2 | Variant A | 70% | A and B set the fail line at the seed bar with causal falsifiers (r2A:119, r2B:136). C keeps its proxy, every-control and spread tests (r2C:98). |
| C-027 | L2 | Variant B | 95% | All three prefer B's itemised cost breakdown (r2A:120, r2B:137, r2C:99). |
| C-028 | L2 | Variant A | 70% | A and B (B as a tie) prefer one short fit assessment per adopter (r2A:121, r2B:138). C keeps adoption fully separate (r2C:100). |
| C-029 | L2 | Variant B | 95% | All three prefer B's chain taxonomy and cap replay, replicated twice (r2A:122, r2B:139, r2C:101). |
| C-030 | L2 | Variant B | 90% | All three prefer B's behaviour tests plus the `enforce` property test; C moved to B (r2A:123, r2C:102). B marks it a tie with A (r2B:140). |
| X-001 | L2 | Variant A | 70% | A and B adopt zero budget for non-blocking findings (r2A:124, r2B:141). C keeps its own letter for the same rule (r2C:103). |
| X-002 | L2 | Variant A | 95% | All three adopt seven bullets with bullet 6 replaced; B conceded its bullet 8 and C moved to A (r2A:125, r2B:142, r2C:104). |
| X-003 | L2 | Variant A | 70% | A and B keep finding ids out of the spec (r2A:126, r2B:143). C keeps its own letter, and B withdrew its claim that C contradicts itself (r2C:105). |
| X-004 | L2 | Variant C | 95% | All three adopt C's exit-code meanings, the only layout that keeps argparse's exit 2 free (r2A:127, r2B:144, r2C:106). IP INV-006 shows the winning reviser steps still use B's codes. |
| X-005 | L2 | Variant B | 70% | A and B have the script revert whole findings, with a coupled revert added (r2A:128, r2B:145). C holds that validation never overwrites the spec (r2C:107). |
| X-006 | L2 | Variant A | 95% | All three give override authority to the reviewer; C moved to A (r2A:129, r2B:146, r2C:108). |
| X-007 | L2 | Variant C | 95% | All three fail closed on a missing or stale input; A and B moved to C (r2A:130, r2B:147, r2C:109). |
| X-008 | L2 | Variant B | 95% | All three keep reviser prose out of the next review, passing numbers and ids only (r2A:131, r2B:148, r2C:110). |
| X-009 | L2 | Variant B | 70% | B and C adopt free in-scope deletions that are measured, not capped; C moved to B (r2B:149, r2C:111). A keeps its own letter for the same free-deletion rule (r2A:132). |
| X-010 | L2 | Variant B | 95% | All three accept B's whole-fix measurement, recounted twice, and A withdrew its 40-word calibration (r2A:133, r2B:150, r2C:112). |
| X-011 | L2 | Variant B | 95% | All three accept that fix size alone does not separate parents with blocking children (r2A:134, r2B:151, r2C:113). |
| X-012 | L2 | Variant A | 80% | A and C reject coordinator duties that unchanged briefs cannot deliver (r2A:135, r2C:114). B's dissent is marked a tie with A (r2B:152). |
| X-013 | L2 | Variant A | 70% | A and B set the fail line at the seed bar and reject B's "promising" band as a pass (r2A:136, r2B:153). C keeps its complete bar including spread (r2C:115). |
| X-014 | L2 | Variant B | 95% | All three use the exact 472-line 427 text for the experiment file so only one thing changes (r2A:137, r2B:154, r2C:116). |
| A-001 | L2 [dependency] | Variant B | 70% | A and B QUALIFY the splitter assumption: use B's lookahead splitter, gated by the replay harness (r2A:138, r2B:155). C prefers exact quotes (r2C:117). |
| A-002 | L2 | Variant B | 70% | A and B QUALIFY partial admission: `enforce` reverts whole findings with a coupled revert (r2A:139, r2B:156). C rejects the independence assumption outright (r2C:118). |
| A-003 | L2 | Variant A | 70% | A and B QUALIFY: a zero minor budget keeps deferred text unchanged, with the proxy and blocking counts reported separately (r2A:140, r2B:157). C rejects the assumption, citing F16's persistence (r2C:119). |
| A-004 | L2 | Variant B | 70% | All three reject one-retry success as a prediction; A and B keep `enforce` as the termination mechanism (r2A:141, r2B:158). C prefers bounded retries without partial salvage (r2C:120). |

**Points won per variant** (Step 3 tiebreaker input): Variant A 18, Variant B 28, Variant C 7, unresolved 2 (S-001, S-002). Total 55.

## Convergence Assessment
- Points resolved: 53 of 55
- Alignment: 96.4% (53 / 55 = 0.964, CV:63)
- Threshold: 75%
- Agreement gate: PASS (96.4% >= 75%). Unanimous 31, majority 22, split 2.
- Taxonomy coverage: L1 = 0, L2 = 52, L3 = 3 (C-009, C-011, C-020). All three levels covered: **No** (L1 has zero coverage).
  - Taxonomy gate: FAIL. Per the forced_round_trigger rule, a forced debate round targeting L1 (naming, formatting, wording, style, cosmetic, presentation) is required before convergence can be declared. It was not dispatched within this assembly step.
  - Note on tagging: the scan is literal. The three L3 tags come from incidental tokens (`state.json`, `--state-sha256`, `test ! -e` guards), and many L2-tagged points (for example C-013, C-019, X-005, X-007) discuss guard and state behaviour in other words. S-001 (section order) and S-002 (heading count) match the protocol's L1 examples ("section ordering preferences", "markdown formatting") but contain no L1 signal term; they were debated in both rounds and are the two unresolved points. If they are re-tagged L1 by judgment, the taxonomy gate passes and the status becomes BLOCKED_BY_INVARIANTS.
- Invariant probe gate: FAIL.

  ```
  CONVERGENCE BLOCKED: 10 HIGH-severity UNADDRESSED invariant(s) detected
  Blocking items: INV-001, INV-002, INV-005, INV-006, INV-007, INV-012, INV-023, INV-026, INV-027, INV-028
  These invariant violations must be resolved before convergence can be declared.
  Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.
  ```

  ```
  WARNING: 13 MEDIUM-severity UNADDRESSED invariant(s) detected
  Items: INV-003, INV-008, INV-009, INV-013, INV-014, INV-015, INV-016, INV-019, INV-020, INV-021, INV-029, INV-030, INV-031
  These items do not block convergence but should be reviewed.
  ```
- Status: BLOCKED_BY_TAXONOMY
  - Agreement is at or above the threshold, but taxonomy level L1 has zero coverage. The invariant gate also fails independently (10 HIGH UNADDRESSED); BLOCKED_BY_INVARIANTS would apply once L1 is covered.
- Unresolved points: S-001, S-002
- Forced round for L1 (dispatched by the orchestrator after this assembly, per forced_round_trigger; files `debate/forced-L1-variant-{A,B,C}.md`). Each advocate raised four L1 points. Outcomes by 2-of-3 majority:
  - Checker skill folder name: `sc-fixcheck` (B), unanimous (L1-A1, L1-B1, L1-C1).
  - Budget class labels where a person reads them: spelled-out names (`CRITICAL`, `blocking MAJOR`, `minor`, `override`), A and C (L1-A2, L1-C3); B preferred terse labels.
  - Name of the added command section: `## Fix Budget` (B), B and C (L1-B2, L1-C4); A did not raise it.
  - Single-advocate points recorded, not resolved by vote: budget numbers live only in the checker constants and the command points to its preflight output (L1-A4); bullet 6 keeps 427's wording word for word and appends (L1-A3); one `fix*` artifact name family (L1-B4); field name `finding_id` (L1-C2).
  - S-001: all three say it is not a real split (all variants use the same 8 H2 sections in the seed's order); resolved: keep that order. S-002: A and B prefer numbered H3s per mechanism step; resolved to that, C dissenting (lighter subdivision).
  - After the forced round: L1 coverage > 0 (12 L1 points debated), diff points resolved 55 of 55 (S-001 and S-002 resolved by the forced round), so the taxonomy gate passes.
- **Final status after the forced round: BLOCKED_BY_INVARIANTS** (agreement and taxonomy pass; 10 HIGH UNADDRESSED invariants remain).
- Next step under the protocol: depth standard has no Round 3 ("Round 3 skipped: depth=standard"), so the debate ends without convergence. Per the no_convergence rule, Step 3 force-selects the base by combined score and documents the non-convergence for user review. The 10 HIGH UNADDRESSED items (INV-001, 002, 005, 006, 007, 012, 023, 026, 027, 028) are carried into `refactor-plan.md` as required changes, with the suggested resolutions at IP:49-59 as the starting point. Whether to run the forced L1 round first is for the calling command to decide.
