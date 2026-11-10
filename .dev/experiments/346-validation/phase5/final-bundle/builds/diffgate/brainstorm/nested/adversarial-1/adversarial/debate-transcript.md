# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel, Round 2 sequential A, B, C) plus Round 2.5 invariant probe; Round 3 skipped (depth=standard)
- Convergence achieved: 99% point agreement (68 of 69 points: 62 of 63 S/C/X points plus 6 of 6 A points by majority)
- Convergence threshold: 75%
- Gate status: BLOCKED_BY_INVARIANTS (7 HIGH-severity UNADDRESSED items in invariant-probe.md: INV-001, INV-004, INV-015, INV-016, INV-027, INV-034, INV-036)
- Taxonomy coverage: L1 (S-points, wording), L2 (C/X structural points), L3 (state and guard points such as X-001, X-002, X-003, X-009, INV state_variables) all covered
- Focus areas: All
- Advocate count: 3 (A = opus:architect, B = sonnet:refactorer, C = haiku:qa)
- Orchestrator evidence added before Round 2: debate/evidence-flg-r1.md (resolves shared assumption A-006)
- Full statements are kept as separate files in debate/ and included verbatim below.

## Round 1: Advocate Statements

### Variant A Advocate (file debate/round1-A.md)

# Round 1: Variant A advocate (opus, architect)

#### Position summary

Variant A should be the base of the merge. Its main parts are worker-owned script steps, a token-level surface, one `DG` line grammar behind a `PROFILES` seam, and a test plan that is the only one to find both existing-test breaks. Together they give the smallest mechanism that fails closed and that later adopters can reuse without changing the script. A should take in four parts from the others: C's removal of the `src/superclaude` line, B's `via=` escape and explicit fix map, and B's more cautious R3 forecast.

#### Steelman of Variant B

B's strongest case is that it is the only variant that tests its mechanism against recorded data before predicting anything (U-007). Section 1 says: "Replaying the fix-map gate over the round-2 revision of `flg-r2` ... Total 5 to 2, blocking 1 to 1. Honest reading: the gate removes noise and growth and leaves the induced blocker that a mapped fix produced." That replay is why B's forecast (mean 3.5, "Probability that both replicates meet the R3 bar: about 0.25", section 9) is the best-grounded one of the three. B also names the right failure mode in advance. F1 "wrong lever" (U-011) separates a scope problem from a per-fix defect-rate problem, and it is the most useful falsification condition in any variant. B's `via=` escape (C-013, U-008) is the only mechanism that lets a real regression on an unchanged line block, and it is quote-checked and capped (`VIA_CAP = 2`). The explicit `fixmap-r<N>.txt` with `declined` lines (C-014) makes the reviser's claims auditable and gives under-fixing a visible place, which addresses A-003 directly. B's staged delivery (Stage A inert, Stage B arm, Stage C fold; U-013) is also good refactoring discipline. Each stage can be reverted on its own.

#### Steelman of Variant C

C's strongest case is integrity. C is the only variant whose copied command would not ship a `src/superclaude/...` read into an installed primitive (U-016; verified, `src/superclaude/commands/spec-panel.md:220` reads `src/superclaude/examples/release-spec-template.md`). It is also the only variant that separates implementation acceptance from experiment success (section 14, 15 criteria; S-003). C takes the hardest line on the cheapest way to cheat the gate: a MAJOR blocks only with a "confirmed concrete wrong implementer outcome", and "A nonempty outcome string is necessary but not sufficient" (section 4 step 6; C-019). Repair footprints approved before editing (U-015) close the loophole that A and B leave open, where a valid id is pasted onto an unrelated edit. C's state hygiene (exclusive-create lock, generation compare, symlink refusal, 2 MiB and 100,000-line caps; C-035, U-018) is the most complete. The spread check (U-017) is the right statistical guard for n = 2. C is also the most honest about cost: "about 5-13 added minutes per full loop ... Do not call this free" (section 10).

#### Key strengths claimed

1. **The installer analysis decides the skill's name, and it is verified.** A section 3.2: "A skill named `sc-spec-panel-diffgate` would be silently skipped and its stale copy deleted, because `commands/spec-panel-diffgate.md` exists and calls the script by path." I re-read `src/superclaude/cli/install_skills.py`: `_has_corresponding_command` (line 40) returns true when the command exists and the skill is not in `skill_activation_targets` (line 57). This is U-002, and it was the reason for A's decision, not something A happened to get right.
2. **Only A finds both existing-test breaks (U-003).** For `tests/recommend/test_routing_refresh.py`, line 33 is `_POST_REFRESH_ADDITIONS = {"graph", "impact", "issue"}` and line 648 asserts `shipped - _POST_REFRESH_ADDITIONS == active` (re-verified). A 8.6 adds `spec-panel-diffgate` to that set. B omits the edit and C forbids it (X-012). For `test_worker_contract.py`, A's `UNATTENDED_VARIANTS` map plus a parity test (8.6) keeps the 31-entry `UNATTENDED_EXPECT` count intact. C forbids any edit there and therefore fails line 837 (X-017).
3. **The surface is token-level, so its granularity matches S1's one-paragraph-per-line layout (U-001, C-008).** A 3.1: "A line diff turns a one-word citation fix into a whole paragraph of surface", at about 240 bytes a line. A 3.5 runs a second `SequenceMatcher` over tokens inside changed blocks, so the anchor rule C5 ("at least one occurrence of the quote overlaps at least one changed token") is tight. B's line hunks plus `MERGE_GAP = 2` and display context, and C's 3-line unified diff, both make the anchorable region larger than the change. That larger region is the anchor-gaming room the seed brief asks to close.
4. **Severity drift on carried findings cannot happen, because of the grammar (C-020).** A V4: "`DG-STATUS` ... has no severity field: it stays at the severity and blocking status of the review that raised it." This needs no rule to enforce. A parser cannot accept a field the grammar does not have. B's C10 forces `open` only for untouched anchors and still uses reviewer labels for blocking (R12). C reaches the same freeze, but through ledger checks.
5. **The extension seam is real and small (U-006, C-034).** A 3.6: "One dict, `PROFILES`, holds the severity vocabulary and the blocking rule ... nothing else in the script knows which reviewer produced the report." The cap is a module constant (`CAP_REVIEWS = 3`, "not a flag, so no caller can raise it"). rf-qa adopts it with one profile entry (A section 11). B says it is "document-agnostic" but hardcodes `OUTCOME_MIN`, `VIA_CAP` and the `fr` key into the grammar. C defers generalisation and forbids a "generic plugin system", which rules out the cheapest adoption path.
6. **Failure is graded so that no step degrades silently (C-011, X-002).** A 4.3: a second reject runs `close --demote`. "Demotion can only move toward FAIL for prior findings and toward 'note' for new ones; it never invents a PASS from a broken status line". A non-demotable failure "ends the run without a verdict". B's tier 3 always returns exit 0 with `degraded: yes`, even for C1 format failures, though C1 is marked hard. C's "a second reject marks the run invalid" throws away a whole review and its accepted blockers whenever an anchor is mistyped. A demotes what it can (anchors), stops on what it cannot (structure), and counts demotions as falsification condition 4.
7. **A forged ledger buys nothing (U-004, C-035).** A 4.4: "The next `open` therefore replays the check: it re-runs `check` on the recorded report (`report_sha256` must still match) ... any difference with the ledger is exit 2." This covers the main tamper path, a worker with Write access, in one function (`replay`), with no lock files or generation counters.
8. **Low friction in review 1 (A-005, C-006).** Review 1 changes only by adding `DG` lines with `anchor=doc` (A step R1.b). Quotes are JSON strings, so `json.loads` parses them without ambiguity (4.1). B's `[[...]]` delimiters break on quoted text that contains `]]`. C's strict JSON draft with repair footprints and coordinator confirmations changes review 1 more than either, and that makes the A-005 comparability worry worst for C.
9. **Placement fits the loop's real actors (C-001, X-001).** The reviewer runs `open` and `close`, the reviser runs `gate`, and `open` runs the gate again with authority ("Reviser skips the gate | The next `open` runs the same gate and exits 4", A section 2 skip table). Every step is locked to the next, so no actor's honesty is the only safeguard. B reached the same conclusion ("an Orca coordinator or a human is also a prose follower"). C's coordinator-runs-everything design adds about ten coordinator steps and parent Read-backs per loop (C section 10).
10. **The blindness audit attributes misses correctly (C-033).** A section 9: misses are "classified by the script's history: text written by fix 1 or fix 2 that the loop closed, or text present since the original. Only the first kind measures what diffgate hides." B's audit is "if budget allows"; C has none.

#### Weaknesses identified in Variant B

1. **The no-`src/superclaude` rule and the byte-identical drift guard cannot both hold (X-016).** B 8.1: "Every other line is byte-identical to the original". B 8.3 drift guard: "every `## ` section body other than `Review Loop`, `Diffgate` ... equals `spec-panel.md`'s". B 8.3 and 8.5 also require "no `src/superclaude` string anywhere in the variant". Line 220 of the source (re-verified) breaks one of the two whichever way B goes. A has the same defect (X-015, conceded below), but B adds a test that pins it permanently.
2. **The test plan misses `test_routing_refresh.py` (X-012).** B 8.3 lists the tests that "must keep passing without edit" and leaves this one out. As written, adding the command fails line 648.
3. **Graceful degradation hides format failure.** B section 4 tier 3: "the script does not fail the run and does not loop. It degrades fail-safe", exit 0. B's own C1 (missing `verdict:` line or missing `FINDINGS none`) is "hard", yet on the second pass a report with no findings block still gets a derived verdict. B open question 7 admits "I chose degrade so a format error can never block a document review". A blocks exactly that case (A 4.3 step 4: "A missing or empty section can never become PASS").
4. **The reviewer still writes a verdict line (X-006).** C1 requires "a last non-blank line `verdict: PASS|FAIL`" before `check`. C13 then rejects a mismatch once and lets the derived verdict win. This asks the reviewer to compose a verdict that will be overridden anyway, and it spends a reject round on nothing. A's reviewer writes no verdict, and the script prints `verdict_line`.
5. **Arbitrary thresholds sit in the grammar.** `OUTCOME_MIN = 25` turns a judgement rule into a padding rule. B R3 concedes: "pad `outcome` to 25 characters". `FIX_BUDGET_BYTES = 1500` is "calibration UNVERIFIED" (5.2), and `docs/designs/spec-panel-review-loop.md` line 73 already rejects a size limit (X-013).
6. **Its own replay count is off (X-018).** B says "the gate would have allowed 13", but under B's own F1, line 5 carries blocking id N1 and is mappable, which gives 14. The error is small, but it is in the one piece of evidence B leans on most.
7. **Concurrency is left open.** R11: "two workers writing one directory at once are not locked (atomic replace only)." That is acceptable for S1, but it is a risk for the "later adopters" B ranks first (rf-qa).

#### Weaknesses identified in Variant C

1. **The design breaks a test that C's own acceptance criteria require to pass (X-017).** C section 8: "Do not edit ... worker contract". 14.14 requires `tests/skills/test_worker_contract.py` to pass. `_check_no_unattended_sections` (line 831, set equality at 837) fails as soon as a new command carries `## Unattended mode`, and C's rewritten section is exactly that. The same applies to X-012 for `test_routing_refresh.py` ("Do not edit ... routing table").
2. **It puts the most weight on the least reliable actor (C-001, X-001).** C section 2: "The coordinator owns transitions and runs the helper." C section 7 then lists as still-prose "whether the coordinator actually invokes the helper". B's critique applies: the coordinator "is also a prose follower". C makes every acceptance depend on that actor's confirmation file (U-014), which, by C's own account, proves presence and not truth ("Presence of a confirmation is checkable; truth of its semantic judgment is not").
3. **A second reject throws away the review (C-011, X-002).** "A second reject marks the run invalid and escalates", with "no new fix cycle". On S1 an anchoring mistake is the expected failure, so the most likely error ends the replicate as invalid. C 9 then says "not a successful replicate", so the experiment pays for a full rerun. A's demotion keeps the run alive and counts the cost.
4. **Whitespace and reflow are inconsistent (X-003, X-009).** C keeps "427's whitespace-only exclusion" for the eligibility mask but also requires "Every group, including whitespace edits, must be covered once, owned by an open blocker". A whitespace fix therefore cannot open scope, yet it needs a blocking owner. C also treats a reflow as a real delta ("No silent flattening"), and on hard-wrapped text that turns cosmetic rewraps into reviewable surface. The surface then grows, which works against the purpose of the gate.
5. **The measurement does not say which count gates the bar (X-008).** The bar row is "Open CRITICAL+MAJOR proxy". The same section says deferred CRITICAL/MAJOR are "excluded from the scoped blocker metric" and also that the recorder "retains the original severity proxy counting rule". A and B both fix this before the run: deferred findings count.
6. **The command text is not given verbatim (S-004).** The seven bullet changes are "described in summary form only". The command text is what a worker obeys, so leaving it as a description postpones the hardest part. A 8.1 gives all nine bullets as single physical lines, ready for the pins.
7. **It is heavy for an experiment arm.** Plugin mirrors (X-011) are not required. `tests/commands/test_routing_plugin_parity.py` lines 42-48 pin only the README-listed commands (fact check). Footprint pre-approval, confirmation files and strict-JSON drafts make the cost "5-13 added minutes per full loop" (C section 10). The `Skill`-tool activation requirement (U-019) adds a load step that a by-path script call does not need.

#### Concessions

1. **X-015 is real and High.** A 8.1 says "A byte copy ... with these changes only" and "Nothing else changes". A 8.5 tests that "the string `src/superclaude` is absent". Line 220 (re-verified) makes the specified test fail on the specified file. Fix: adopt C's removal of that line from `## Tool Coordination` (U-016) and name it in 8.1 as a tenth change.
2. **The R3 forecast is overconfident (X-007).** A's "about 60% that both replicates meet the proxy bar" rests on scaling flg-r2 ("scaled to a third of the rows"). It has no replay, and A does not address flg-r1 (R3 = 6) at all. B's replay-grounded 0.25 is better calibrated. A should keep its point forecast but drop its confidence to B's range unless flg-r1 is read first.
3. **The implicit fix mapping is loose (C-014).** Under V2, a hunk is mapped if "its removed or replaced words overlap that finding's quote". A large rewrite that touches one word of a blocking quote therefore passes. A has no `declined` outlet, so under-fixing (A-003) appears only as `open` priors. B's explicit map with `declined` lines is better and should be merged in. A's inline-id path can stay as an accepted alternative form of the map.
4. **There is no mechanism for action at a distance (C-013, X-005).** A section 10 admits "A reviewer that reads only the surface may not notice B". B's capped `via=` is a real improvement, and A should adopt it.
5. **The "P1 plus P2 with exactly 31 entries" claim is overstated.** Per the fact check, line 1564 checks only that `UNATTENDED_EXPECT` has 31 entries.
6. **There are no implementation acceptance criteria separate from the experiment (S-003), and the safety limits are thin.** C's section 14 and its size, symlink and lock limits (U-018) are missing from A.
7. **Remaining prose residuals.** A coordinator who passes a new `--ledger` path starts a fresh review 1 ("Prose only", A section 10). B's `--expect-round` (U-010) is a cheap mechanical fix A lacks. Renumbering noise and inline id clutter are also unresolved (A open question 3).
8. **The cost estimate is probably low (C-027).** "7 to 10 per loop" leaves out the reviewer's correction turns and the reviser's map work. C's envelope is more honest.

#### Shared assumptions

- A-001: QUALIFY: A narrows the recovery protocol to one scripted command per exit code (`close` again, then `close --demote`; exit 4 goes back to the reviser), so little improvisation is needed, but compliance is still assumed. Recovery-path compliance should be recorded as a validity input per replicate, not only as cost.
- A-002: QUALIFY: Token-level anchoring limits where findings can sit, but nothing limits how many a reviewer raises per changed span. Findings per changed token should be recorded as a secondary metric so that a density effect is visible instead of assumed away.
- A-003: QUALIFY: Under A, prior blockers left open count in the R3 proxy, so the effect is measured, not hidden. A has no `declined` outlet, though, and should adopt B's, so that under-fixing is explicit rather than showing up as stalled gates.
- A-004: REJECT: The added brief lines ("fix only the ids in the brief file it names", A 8.9) are prose that could produce part of the effect on their own. The result must either be claimed as "script plus brief lines" or include a briefs-only ablation arm.
- A-005: QUALIFY: A's review-1 change is the smallest of the three (DG lines only, no footprints or confirmations), so the assumption is most plausible for A. Review-1 blocker counts should still be checked against Arm B's 13 to 17 as a stated validity check.
- A-006: REJECT: A's causal story (N5 from F22 to N12) is drawn only from flg-r2, and flg-r1 is the replicate that fails the bar (R3 = 6). Read flg-r1's review-3 report before any paid run (B open question 12).

#### Per-point positions

| Point | Superior approach (A, B, C, or "A+B" style merge, or "tie") | One-line reason |
|---|---|---|
| S-001 | C | C's outline adds separate test-plan and acceptance sections that A and B lack. |
| S-002 | C | Tiered P0/P1 tests plus live and manual semantic checks are easier to execute and audit than a list inside "Exact changes". |
| S-003 | C | Implementation acceptance kept apart from experiment success stops a forecast from passing as done. |
| S-004 | A | Only A gives every replacement bullet verbatim as one physical line, ready for text pins. |
| S-005 | A+B | A's signature list fixes the interfaces; B's named constants and per-part line budget bound the size. |
| S-006 | A+B | Both give one shared exit table with a "Who acts" column; C's single sentence gives the caller less guidance. |
| S-007 | B | B's UNVERIFIED tags and flg-r2 replay ground its evidence better than A's dense citations alone. |
| S-008 | A+B | A's bullet-keyed table maps 1:1 to 427; B's 12-concern table catches extra rows such as step order. |
| S-009 | A+C | A's residual-risk column plus C's separate cost envelope. |
| S-010 | C | C gives every open question a default, so no interface is left undefined. |
| C-001 | A+B | Worker-owned steps locked to each other do not depend on the coordinator's obedience; A's `open` re-running the gate adds authority. |
| C-002 | A | `sc-diffgate` is named from a verified installer analysis and needs no Skill activation. |
| C-003 | A+B | Keep A's split between read-only (`gate`, `check`, `status`) and state-changing (`open`, `close`) steps; fold `final` into `close` as B does. |
| C-004 | A+C | One JSON object per call (A), with verdict and execution success as separate fields (C). |
| C-005 | A+C | A's who-acts table, with C's rule that a valid FAIL verdict is exit 0. |
| C-006 | A | JSON-string quotes in a Markdown block parse without ambiguity at low reviewer cost; B's `[[ ]]` can collide and C's strict draft is heavy. |
| C-007 | A+C | A's small file set, organized in C's per-round subdirectories. |
| C-008 | A | A token-level surface matches S1's one-paragraph lines and narrows the room for anchor gaming. |
| C-009 | A | `H<k>.<n>` is readable and never repeats across reviews; C's digest adds little that the ledger hash does not already give. |
| C-010 | A+C | A's C1-C13, plus C's rule that every claimed anchor is validated, not only the first. |
| C-011 | A | Demote what is demotable and stop on structural failure: no silent PASS (unlike B), no discarded review (unlike C). |
| C-012 | A+B | A legal non-blocking outlet stops forced anchors; C's reject wastes a repair round. |
| C-013 | B | Capped, quote-checked `via=` is the only mechanism that covers action at a distance. |
| C-014 | B | An explicit fix map with `declined` lines is auditable and makes under-fixing visible; A's implicit overlap is loose. |
| C-015 | A | Report bytes and do not budget them, as the design doc line 73 rejects a size limit. |
| C-016 | tie | All three reject a severity ceiling for the same sound reason. |
| C-017 | A+C | A's end-of-loop appendix with demoted findings, plus C's statement that PASS is scoped. |
| C-018 | A | The reviewer writes no verdict and the script prints it; C's full report rendering adds cost without adding authority. |
| C-019 | C | Coordinator confirmation of the wrong outcome is the only rule that is not satisfied by padding. |
| C-020 | A | A grammar without a severity field makes drift on carried findings impossible by construction. |
| C-021 | tie | All three keep minor findings away from the reviser. |
| C-022 | A | A token-stream comparison drops pure reflow and still exposes edited words; C turns cosmetic rewraps into surface. |
| C-023 | B | Grounded in a replay and realistic about flg-r1; A's 60% is overconfident. |
| C-024 | tie | All forecasts sit well under 44.4%, which 427 already met. |
| C-025 | A+B | B's F1 "wrong lever", plus A's demotion-rate and stall conditions. |
| C-026 | A+B | Counting deferred findings in the bar metric stops a win by deferral. |
| C-027 | C | The most complete accounting, including parent Read-backs and repair rounds. |
| C-028 | A+C | A's hash of the untouched `spec-panel.md` and its never-`--force` rule, plus C's hashes of all installed files and transcript check. |
| C-029 | A | Ignoring the flags with a printed note is the least code and is safe with the ledger in charge. |
| C-030 | A+C | Only A fixes both existing-test breaks; C's isolated-HOME install test is worth adding. |
| C-031 | A+B | A verbatim copy with the name swapped is pinnable against the parent; C's rewrite needs new contract tests. |
| C-032 | A+B | No mirror is needed per `test_routing_plugin_parity.py` lines 42-48; a separate design note keeps 427's doc historical. |
| C-033 | A | A blindness audit classified by ledger history isolates what the gate hid. |
| C-034 | A+C | A's PROFILES path to adoption, with C's caution not to replace the `/sc:implement` FINAL or weaken rf-qa guards. |
| C-035 | A+C | A's ledger replay, plus C's lock, symlink and size limits. |
| X-001 | A+B | Worker-run steps with mutual locks; the coordinator is also a prose follower. |
| X-002 | A | Graded demotion keeps the run alive without letting a broken report reach PASS. |
| X-003 | A | A word-identical reflow carries no change to review; edited words inside a reflow still surface. |
| X-004 | A+B | An unanchored finding becomes a normal deferral, not a reject. |
| X-005 | B | `via=` lets a real regression on an unchanged line block, within a cap. |
| X-006 | A+C | The reviewer writes no verdict, which removes a pointless reject cycle. |
| X-007 | B | B's 0.25 rests on a replay; A's 60% extrapolates from one replicate. |
| X-008 | A+B | Both state before the run that deferred findings count; C leaves the gating count ambiguous. |
| X-009 | A+B | Whitespace-only changes are never hunks, so they never need an owner; C's rule contradicts its own mask. |
| X-010 | A | Ignore the flags with a note: the least work for the same safety. |
| X-011 | A+B | The parity test pins only README-listed commands, so a mirror is unneeded scope. |
| X-012 | A | Only A plans the required `_POST_REFRESH_ADDITIONS` edit. |
| X-013 | A | Rejecting a byte budget follows the design doc's own line 73. |
| X-014 | A | A by-path call with a name that does not match the command removes any dependence on Skill activation. |
| X-015 | C | A contradicts itself; C's removal of line 220 is the fix A should adopt. |
| X-016 | C | B contradicts itself; C is the only variant whose copy is clean. |
| X-017 | A | A's `UNATTENDED_VARIANTS` map keeps the worker-contract test passing; C's plan fails it. |
| X-018 | tie | This is B's own counting slip; A and C take no position on it. |

### Variant B Advocate (file debate/round1-B.md)

# Round 1 statement: Variant B (variant-2-sonnet-refactorer.md)

Sources read in full: variant-2-sonnet-refactorer.md (B), variant-1-opus-architect.md (A), variant-3-haiku-qa.md (C), diff-analysis.md, seed-brief.md. Repository facts re-checked in this worktree with Grep and Read: `src/superclaude/commands/spec-panel.md:220` (contains `src/superclaude/examples/release-spec-template.md`), `tests/recommend/test_routing_refresh.py:33` and `:648`, `tests/skills/test_worker_contract.py:831-837`.

#### Position summary

B is the smallest mechanism that closes the measured escapes (self-computed diff, self-tagged origin, unmapped reviser edits, unchecked count and verdict) while staying revertible at every stage and honest about what it cannot fix. The worker that owns each step runs the script, a failed report degrades fail-safe instead of ending the run, and the one replay B ran on recorded data predicts a bar miss (mean 3.5), which is the most credible forecast of the three. B loses on diff granularity, on one missed existing-test edit, and on one copy-versus-grep contradiction, and I say so below.

#### Steelman of Variant A

The strongest version of A: it is the most engineered answer to the actual S1 spec shape. The spec is one paragraph per line (about 240 bytes a line, A section 3.1), so a line-level surface turns a one-word citation fix into a whole paragraph. A's two-pass diff (line, then token inside changed blocks, section 3.5) makes the surface the changed words, and its anchor rule C5 requires the quote to overlap a changed token. That is the most direct answer to the seed brief's granularity question.

A also gets several repository facts right that the others miss. It is the only variant that works out the installer naming trap (a skill called `sc-spec-panel-diffgate` would be skipped and its stale copy deleted, section 3.2, verified in `install_skills.py`), the only one that finds both existing tests a new command file breaks (`test_routing_refresh.py:648` and `test_worker_contract.py:837`, section 8.6, both verified here), and the only one with a ledger replay on `open` (section 4.4) so a hand-edited ledger "buys nothing". V4 pins severity structurally: `DG-STATUS` has no severity field, so carried findings cannot drift upward. The reviewer writes no verdict, which removes a reject path. A rejects a hard byte budget with a verified citation (`docs/designs/spec-panel-review-loop.md` line 73). Its evidence citations are the densest of the three, and it is the only plan that names both of the existing-test edits a new command file needs.

#### Steelman of Variant C

The strongest version of C: it treats the loop as an acceptance gate with an evidence trail, not a convenience script, and it admits where the script ends. Its confirmation file puts a second party (the coordinator) between a reviewer's claim and the verdict, so "the reviewer proposes, the parent derives" (the `qa.md` model) is kept literally. Its repair footprints, approved before any edit, are the only mechanism that closes the hole all three variants admit: a valid finding id pasted onto an unrelated edit (A's "id gaming", B's R5, C's footprint section). Its deterministic hunk ids (SHA-256 of both document hashes and coordinates) cannot be replayed across rounds. Its deletion handling is the most exact (old-side anchors, insertion-boundary footprints, a delete-only test case). Its test matrix covers empty diff, BOM, CRLF, repeated lines and duplicate JSON keys.

C also has facts and ideas the others lack. It alone spots that the copied command ships a repository-only read (`spec-panel.md:220`) into an installed primitive (U-016, verified). It requires the worker to invoke the variant through the Skill tool and to show that in the transcript (U-019). It adds a spread check so a pass is "not proven" unless the effect exceeds within-arm spread (U-017). It separates implementation acceptance from experiment success (section 14) and labels every new name PROPOSED. It will not claim a scoped PASS certifies the whole document, and it prints that sentence in the final summary.

#### Key strengths claimed

1. **B is the only variant that tested its mechanism on recorded data before forecasting.** Section 1 replays the fix gate over flg-r2: five review-3 items (N12, N13, N14, N15, C-R3-15) become two, blocking stays 1 to 1, and the induced blocker N12 survives ("the gate removes noise and growth and leaves the induced blocker that a mapped fix produced"). B then predicts mean 3.5 and "about 0.25" for both replicates meeting the bar (section 9). A predicts 2.0 and 60% from a scaling argument ("scaled to a third of the rows", A section 9); C gives 1.5 with no probability. Only B's forecast has a data point under it, and B is the one that predicts its own bar may fail (X-007). For a pre-registered experiment, that is the property that matters.
2. **The lock sits on the actor that is inside the loop, and every skip is loud.** Section 3: "an Orca coordinator or a human is also a prose follower, and the reviewer cannot wait on it." Section 2 lists six skip cases and what stops each: no `begin` means `check` exits 5; no `fixcheck` means the next `begin` exits 5; an edit after `fixcheck` changes the sha. C moves every call to the coordinator (C section 2), and C's own section 10 says parent Read-back "can cost more than the helper itself" and budgets 5 to 13 added minutes a loop. The failure the design doc names (427 section 12: a coordinator that drops the flags starts a fresh first review) lives in exactly that actor.
3. **One answer on a bad report, and it never wastes a session.** Section 4 gives three tiers: unanchored is a normal deferral, a hard violation gets one in-session repair, and a second failure degrades fail-safe (`degraded: yes`, exit 0). B states the invariant: "a lazy report can add an `open` prior (a spurious blocker) but can never smuggle in an unanchored blocker." A ends the run with no verdict on a non-demotable second reject (A 4.3 step 4, and "1 extra reviewer session per non-demotable reject", A section 10). C marks the run `invalid` after a second reject (C section 4) and counts it "not a successful replicate" (C section 9).
4. **The fix gate is explicit, auditable and has an exit for honest non-fixes.** F1 to F3 (section 5.2) require every hunk to carry exactly one blocking id, and every blocking id to have a hunk or a `declined` line with a reason. A has no `declined` path (its map is implicit: an id pasted in the added text, or removed words overlapping the quote, A V2). B also prints chains (`R1.5 -> R2.1 -> R3.2`, section 5.3) and says a length-3 chain means "revise this region by hand" instead of another cycle. That is a measured, countable record of the regeneration the experiment is about.
5. **Minimal-risk, revertible transformation path.** Section 8 splits the work into Stage A (inert: skill folder, script, script tests, nothing references them), Stage B (the experiment arm: one new command file), and Stage C (fold into `spec-panel.md` only after the S1 bar, a separate PR). The variant is made with a `sed` rename so every untouched line stays byte-identical and drift is reviewable with `diff` (8.1). A drift-guard test compares every untouched `## ` section body to `spec-panel.md` (R10), which addresses the debt of a forked command. This is the smallest footprint: four subcommands, about 350 lines, no plugin mirror, no ledger lock. C adds plugin mirrors, an annex to the 427 design doc, an exclusive-create lock, symlink refusal and size limits.
6. **A pre-registered falsification that separates the levers.** F1 "wrong lever" (section 9): R3 of 5 or more with 70% or more of review-3 blockers on mapped fix hunks means scope and fix gates worked and the per-fix defect rate is the driver, so the next idea must act on fix quality. A and C do not pre-register that split. The primary metric `R3-proxy-all` counts deferred findings by their reviewer label so the arm cannot win by deferring (section 9), which is the reading A also adopts and C leaves ambiguous (X-008).
7. **A legal route for a real cross-reference regression.** `via=H<i> via_quote=[[...]]` (rules C7, C11) lets a blocker sit on an unchanged line only if it quotes the changed hunk it depends on, at most 2 per review. A names the failure this prevents in its own section 6 ("a reviewer that sees a real problem in unchanged text and has nowhere to put it is the one most tempted to force an anchor"), and then offers only `anchor=none`. B also adds `--expect-round N` so a fresh or wrong directory exits 5 instead of quietly starting review 1 (section 2, R9).
8. **Less machinery shared between steps.** The same diff routine serves `begin` and `fixcheck`, so a fix hunk id and the next surface's hunk id are the same id and the surface can print "H2 = the fix for R1.3" (section 3 step 6). One computation, one id space, no second code path to drift.

#### Weaknesses identified in Variant A

1. **The fix map is implicit and trivially gamed.** A's V2 maps a hunk when "its added text carries the id of an open blocking finding of review k, or its removed or replaced words overlap that finding's quote". Pasting `(R1.4)` onto any edit passes. A's own risk table says so ("A valid id pasted onto an unrelated edit passes the gate") and also accepts that inline ids clutter the spec. There is no `declined` line, so an unfixed blocker leaves no recorded reason. B's explicit map with `declined`, `added_bytes` per id and `fixes:` printed on the next surface makes the same gaming visible to the next reviewer (section 5.2, R5).
2. **A bad report can end the run with no verdict.** A's rule table marks C1, C2, C3, C6, C11, C12 and C13 "no" for demotable, and 4.3 step 4 says a non-demotable failure after the second try "ends the run without a verdict". In the unattended path that means a failed contract and a re-dispatched reviewer session (A section 10). B degrades every hard violation to a recorded, fail-safe outcome in the same session.
3. **Renumbering noise is named and left unsolved.** A's risk table: "Renumbering headings or lists makes many one-token hunks, each needing an id" with mitigation "None in v1". At token level, every renumbered heading is a hunk the reviser must map, which is the opposite of the simplification the seed asks for. B's merge gap and `coverage:` warning (R4) at least make a degenerate surface visible.
4. **`DG-COVER` costs tokens and A says it proves nothing.** C13 requires the reviewer to list every hunk id and A labels it "Weak evidence: it proves the reviewer named every hunk, not that it read each one" (section 4.2). It is a per-hunk typing tax with no assurance, a pure debt line item.
5. **The forecast leans on an untested density assumption and on one replicate's story.** A section 9 says fix 2 touches 3 to 5 ids "instead of 15 rows" and predicts 1 to 3 findings, and section 5 says N5 "would never have existed". That is a narrative about flg-r2 (A-006) and assumes a smaller surface yields fewer findings rather than denser ones (A-002). A gives 60% that both replicates meet the bar with no replay behind it.
6. **A's plan fails its own text test.** Section 8.1 makes "a byte copy" of `spec-panel.md` and 8.5 requires the string `src/superclaude` to be absent. Line 220 of the source contains `src/superclaude/examples/release-spec-template.md` (verified here), so the two requirements cannot both hold (X-015). I note this is the same flaw as B's X-016, so it does not separate A from B. It separates both from C.

#### Weaknesses identified in Variant C

1. **Every call is run by the coordinator, the weakest actor.** C section 2: "The coordinator owns transitions and runs the helper." C section 10 admits "No harness permission boundary forces a cooperative coordinator to obey." The measured 427 failure is exactly a coordinator that drops a flag or a copy and starts a fresh review. C locks the loop at the point where that failure lives. B's worker-owned steps put the lock where a skipped step stops the next step (B section 2).
2. **The confirmation file is a hand-written prose duty that decides the verdict.** C section 3: "Presence of a confirmation is checkable; truth of its semantic judgment is not." Blocking is derived from "confirmed" evidence (C section 4 step 6). That moves judgement from the reviewer to the coordinator and makes the verdict depend on a file nobody can verify, against the seed constraint "Mechanical over prose; every remaining prose rule named with its residual risk". C names the risk but adds the duty.
3. **Review 1 gets the largest contract change, which risks the shared baseline (A-005).** Each finding needs strict JSON with exact anchor objects and a repair footprint (line ranges plus exact text or neighbouring-line hashes), duplicate keys are rejected, and a second reject ends the replicate as invalid (C sections 3, 4, 9). Review 1 is where 13 to 17 blockers are written, so the format tax is highest there, and a format slip costs a whole replicate.
4. **C's plan fails two existing tests it says must pass.** `_check_no_unattended_sections` requires `set(have) == set(UNATTENDED_COMMANDS)` (`test_worker_contract.py:837`, verified), and C's variant carries a rewritten `## Unattended mode` (X-017). `test_routing_refresh.py:648` asserts `shipped - _POST_REFRESH_ADDITIONS == active` over every command file (verified), so a new command breaks it (X-012). C section 8 forbids editing both and section 14.14 requires them to pass. B's plan also misses the second one (conceded below); C misses both and forbids the fix.
5. **Scope creep creates debt the seed did not ask for.** The seed lists "One new command file (variant), one new helper script, one new test file, docs" (seed Q2). C adds plugin mirrors of the command and skill with parity tests (X-011; A verified in 8.8, and the fact check confirms, that `test_routing_plugin_parity.py` only mirrors README-listed commands), an annex edit to the historical 427 design doc, an exclusive-create lock, symlink refusal, 2 MiB and 100,000-line limits, crash-resume tests, an isolated-HOME install test and 15 acceptance criteria. C also says the plugin copy has "unrelated one-word drift"; the fact check shows it also lacks a Usage line and the whole `## Unattended mode` section. Each mirror is another file to keep in step.
6. **The legal outlet for an unanchored finding is turned into a reject.** C section 4 step 5: a new claim with no eligible anchor that appears in `findings` is rejected and recorded as a deferred candidate (X-004). A and B treat it as an ordinary deferral. C's rule spends the one-repair allowance on something the design says should be free.
7. **Reflow becomes surface, and the bar metric is ambiguous.** C treats "a reflow or move across physical lines" as a real delta with "no heuristic move detection" (X-003), on a spec where one paragraph is one line. C section 9's table says "Open CRITICAL+MAJOR proxy" while the recorder "retains the original severity proxy counting rule" and a deferred CRITICAL is "excluded from the scoped blocker metric" (X-008). A pre-registered bar must say which count gates it.
8. **Footprints reproduce the under-fix risk with no escape.** C's own risk table: "Mechanical containment is not minimality", and legitimate adjacent fixes "may fail the map and force manual replanning". A rejected map ends as `fix-rejected` and the coordinator "must stop and ask for a decision" (C sections 2, 10). That can leave a prior blocker open at R3 (A-003) with no `declined` record.
9. **The most optimistic forecast carries the longest validity list.** C predicts 1 and 2 (mean 1.5) with no probability, while its own validity rules turn a missing checker call, a changed run id or an invalid termination into a non-replicate (section 9). That is more ways to lose a replicate than B's single pre-registered F4 check.

#### Concessions

1. **X-012 is real and B misses it.** B 8.3 lists existing tests that "must keep passing without edit" and omits `tests/recommend/test_routing_refresh.py`. Line 648 (`shipped - _POST_REFRESH_ADDITIONS == active`) fails once `spec-panel-diffgate.md` exists. A found it (section 8.6, `_POST_REFRESH_ADDITIONS` gets `"spec-panel-diffgate"`); B must adopt that edit.
2. **X-016 is real.** B promises a byte-identical copy, a drift guard that compares untouched section bodies, and a grep for `src/superclaude` that "must print nothing". Line 220 of `spec-panel.md` (`## Tool Coordination`) makes these unsatisfiable together. C's removal of that line (U-016) is the fix; the drift guard must then exempt `## Tool Coordination` or compare after that one substitution.
3. **X-018 is a small counting error.** Under B's own F1, a hunk carrying the blocking id N1 is mappable, so the flg-r2 gate would have allowed 14 lines, not 13. B also writes "Title line 11" for the title that is on line 10, and misdescribes the plugin drift as "one word".
4. **Line-level hunks are weaker than A's token-level surface on the S1 shape.** B leaves granularity as open question 3. On a one-paragraph-per-line spec a one-word edit surfaces about 240 bytes. A's U-001 is the better answer.
5. **`[[...]]` anchors are weaker than JSON-quoted values.** An anchor containing `]]` breaks B's grammar; A's `json.loads` tokens do not have that limit.
6. **B keeps a reviewer-written `verdict:` line as a hard rule (C1, X-006).** That is an avoidable reject path. A (the script prints `verdict_line`, the command appends it) and C (the script renders the report) are simpler. B should take A's way.
7. **B has no ledger replay and no write lock.** A's U-004 closes the hand-edited ledger cheaply; B's R11 leaves it open and says concurrent writers are "not locked".
8. **B's constants are guesses.** `FIX_BUDGET_BYTES = 1500`, `VIA_CAP = 2` and `OUTCOME_MIN = 25` are uncalibrated (B open question 4); `OUTCOME_MIN` can be padded to pass (B R3). A's rule (an `outcome` other than `-`) has the same checkability with no arbitrary number.
9. **B's replay is one replicate, partly hand-counted.** Only flg-r2 was read, one count is marked UNVERIFIED, and flg-r1's composition is unread (B open question 12). B's forecast of 3.5 and 0.25 is a judgement from that, not a measurement.
10. **B's own forecast says the bar probably fails.** That is honest, but it also means B's design, as written, is the one least likely to deliver the pass the seed asks for. B's defence is that F1 then says why.
11. **B lacks C's Skill-tool invocation check (U-019) and spread check (U-017), and A's ledger-history classification of the blind audit (C-033).** All three should be merged in.

#### Shared assumptions

- A-001: QUALIFY: B makes recovery a single rerun of one command with line-numbered reasons in `reject-rN.txt` and degrades instead of blocking, so little improvisation is needed, but nothing in B measures recovery compliance; it should be recorded as a validity input per replicate.
- A-002: QUALIFY: Some of the effect is real (B's replay removed 3 of 5 review-3 items that sat on minor-only or unchanged lines), but whether a reviewer packs the same number of findings onto fewer lines is unmeasured; record hunks per surface and findings per hunk.
- A-003: QUALIFY: It holds only if revisers do not `declined` or under-fix; B's F2 leaves a declined id `open` and B's own budget note says a hard gate "would push revisers to under-fix", so the R3 proxy must report open priors separately from new findings.
- A-004: REJECT: B's brief adds "Your task list is `<DIR>/reviser-brief-r<N>.md`, not the whole report" and a `fixcheck` line (section 8.5), which are prose that can change reviser behaviour without the script; attribution needs a briefs-only arm, or B's validity gate (accepted `check` and `fixcheck` in the ledger) must be paired with one.
- A-005: QUALIFY: B's one-line `FINDING` grammar is a modest tax and its F4 pre-registers the check, but it is not zero, and C's JSON with footprints is a far larger change; review-1 blocker counts must be compared with Arm B as a validity gate.
- A-006: REJECT: B states this is not established (open question 12: only flg-r2 was read); B's replay and its 5-and-2 split both assume flg-r1 looks similar, so read flg-r1's review-3 report before any run is paid for.

#### Per-point positions

| Point | Superior approach (A, B, C, or "A+B" style merge, or "tie") | One-line reason |
|---|---|---|
| S-001 | tie | Outline shape does not change behaviour; all three are navigable. |
| S-002 | C | A separate tiered test section (P0 and P1) is easier for an implementer to execute than a table row. |
| S-003 | C | Implementation acceptance kept apart from experiment success is a real clarity gain that B's staging only partly covers. |
| S-004 | A+B | A gives all nine bullets paste-ready; B's keeping bullets 2, 3 and 7 literal is the smaller diff against 427; C's summary form is worst. |
| S-005 | B | A skeleton with named constants and a per-part line budget gives the reviewer a size limit and a cut list. |
| S-006 | tie | A and B both give one table with a "who acts" column; C's single sentence is thinner. |
| S-007 | A+B | A has the densest file and line citations; B adds explicit UNVERIFIED tags and a worked replay. |
| S-008 | tie | A is keyed to the seven pinned bullets, B to twelve concerns; each is checkable. |
| S-009 | tie | A's table, B's stable R-ids and C's separate cost envelope each add something; none changes the design. |
| S-010 | C | A stated default per question leaves no interface undefined; A and B leave some open. |
| C-001 | B | The worker that owns the step runs it, so a skipped step stops the next one; the coordinator is a prose follower. |
| C-002 | A | A explains the installer naming trap (verified); either of B's or C's names also installs. |
| C-003 | B | Four subcommands is the smallest set that covers begin, check, fix and status; `status` is cuttable. |
| C-004 | tie | Key:value suits a model reader, JSON suits scripts; C's separate verdict and execution fields are the useful part. |
| C-005 | B | One meaning and one action per code (reject, usage, missing, closed, order, corrupt); C's "0 includes a valid FAIL" is worth adopting. |
| C-006 | A | JSON-quoted values are unambiguous and avoid B's `]]` limit; C's whole JSON draft plus footprints is too heavy. |
| C-007 | tie | A's and B's flat files are close in size; C's per-round folders and lock are more than the experiment needs. |
| C-008 | A | Token-level surface fits S1's one-paragraph-per-line spec; B's line-level hunks surface about 240 bytes for a one-word fix. |
| C-009 | A | Hunk ids unique across reviews avoid stale-id reuse; B's shared fix-map and surface ids are the property to keep. |
| C-010 | A | Requiring the quote to overlap a changed token is stricter than B's anchor-on-the-`at`-lines; B's hard versus soft split is worth keeping. |
| C-011 | B | Degrade fail-safe in the same session never wastes a review; A can end a run with no verdict and C ends it invalid. |
| C-012 | A+B | An unanchored finding is a normal deferral, not a reject; C's whole-report reject spends the repair on a free outcome. |
| C-013 | B | `via=` with a quote check and a cap of 2 gives a legal route; A and C push a reviewer to force an anchor on the changed line. |
| C-014 | B | An explicit map with `declined` is the smallest mechanism that closes the measured escape; C's footprints are stronger but need coordinator pre-approval. |
| C-015 | B | An advisory byte report with no gate fits the design doc's no-size-limit rule and still makes a large fix visible. |
| C-016 | tie | All three reject a severity ceiling at review 3 for the same reason. |
| C-017 | B+C | B's `seen: rounds 2,3` and the rule that deferred ids are not legal `cites=` targets, plus C's "scoped PASS" disclosure line. |
| C-018 | A | The script prints the verdict line and the command appends it; B's reviewer-written line is an avoidable reject path. |
| C-019 | A | Presence of an `outcome` is as checkable as B's 25-character threshold and has no arbitrary, paddable constant. |
| C-020 | A | V4 pins carried severity by grammar (no severity field on `DG-STATUS`), which removes upward drift structurally. |
| C-021 | tie | All three give the reviser blocking ids only. |
| C-022 | A+B | Reflow and whitespace-only edits yield no hunk (A tokens, B joined words); B adds a coverage warning; C turns reflow into surface. |
| C-023 | B | B's forecast rests on a replay and states a 0.25 chance for the bar; A's and C's are unsupported by recorded data. |
| C-024 | tie | All three forecasts clear the 44.4% growth bar; the spread between 20% and 27% is not decision-relevant. |
| C-025 | B+C | B's F1 "wrong lever" separates scope from per-fix defect rate; C's spread check says when a pass is "not proven". |
| C-026 | A+B | The bar metric counts deferred findings by their reviewer label so deferring cannot win; C leaves the gating count unstated. |
| C-027 | tie | Each variant costs its own design honestly; C's cost is the highest because of Read-back, A's and B's are close. |
| C-028 | B+C | B's `--expect-round` and `sed` brief rewrite plus C's Skill-tool invocation check; all three hash the new files and avoid `--force`. |
| C-029 | B | Removing the 427 flags from the variant's Usage is simplest; silently ignoring them (A) can mask a coordinator error and verifying them (C) adds code. |
| C-030 | A+B | A's two existing-test edits are what make the suite green; B's fixtures and drift guard are the useful extra. |
| C-031 | A+B | A byte-equal `## Unattended mode` with the name swapped inherits reviewed text and passes the equality test; C's rewrite breaks the pinned count. |
| C-032 | A+B | No plugin mirror is needed (parity test only mirrors README-listed commands); a new design doc leaves the historical 427 doc untouched. |
| C-033 | A+B | A classifies audit misses by ledger history (fix-written versus original); B runs the audit for every arm so the arms are comparable. |
| C-034 | tie | All three agree on rf-qa first, `/sc:reflect` conditional, `/sc:implement` final review not replaced. |
| C-035 | A | A's ledger replay on `open` gives the most protection per line; C's lock, symlink and size limits are over-scoped, and B has neither. |
| X-001 | B | The worker that owns the step runs the script; a coordinator-run chain puts the lock on the actor that fails in 427. |
| X-002 | B | Degrade fail-safe (`degraded: yes`, exit 0) is one path with no wasted session; demote-or-end (A) and invalid (C) both cost a review. |
| X-003 | A+B | A reflowed paragraph with the same words is not a hunk; C's flat reflow-as-delta inflates the surface on S1. |
| X-004 | A+B | An unanchored finding is an ordinary deferral; C's reject spends the one repair on it. |
| X-005 | B | `via` with a quote check and a cap of 2 gives the reviewer a bounded legal route instead of pressure to force an anchor. |
| X-006 | A+C | The reviewer writes no verdict and the script supplies the last line; B's hard `verdict:` rule is an extra reject path. |
| X-007 | B | B's replay-based mean 3.5 and 0.25 chance is the forecast with data under it; A's 2.0 and C's 1.5 are optimistic and unmeasured. |
| X-008 | A+B | The bar counts deferred CRITICAL and MAJOR findings by label; C's second count leaves the gating metric unstated. |
| X-009 | tie | A and B drop whitespace-only hunks (less noise); C maps even whitespace edits (safer for indentation that carries meaning); the trade is unresolved. |
| X-010 | B | Dropping `--re-review` and `--baseline` from the variant's Usage is simplest; ignoring (A) or verifying (C) keeps dead flags. |
| X-011 | A+B | No plugin mirror is needed, verified by the parity test scope; C's mirrors add files and parity tests. |
| X-012 | A | Only A adds `"spec-panel-diffgate"` to `_POST_REFRESH_ADDITIONS`; B omits it and C forbids it (all verified at `test_routing_refresh.py:33` and `:648`). |
| X-013 | tie | A rejects a gate and B's budget is advisory only, so they do not truly conflict; C takes no position. |
| X-014 | A+B | A's naming analysis stands, and calling the script by path is consistent with it; C's Skill-call activation is a legitimate alternative, not an error. |
| X-015 | C | Line 220 of `spec-panel.md` ships a repository path into an installed primitive; C alone removes it (B has the same flaw as A). |
| X-016 | C | C's removal of line 220 resolves the contradiction; B's drift guard must then exempt `## Tool Coordination`. |
| X-017 | A+B | The variant's `## Unattended mode` needs a `UNATTENDED_VARIANTS`-style test edit; C forbids the edit its own plan requires. |
| X-018 | tie | B's 13 versus 14 is a minor counting slip with no effect on the design. |

### Variant C Advocate (file debate/round1-C.md)

#### Position summary

Variant C is the strongest acceptance-safety foundation because it checks both review anchors and preapproved repair footprints, preserves genuine fix-induced blockers, and stops rather than converting a twice-invalid report into a successful review (C sections 3-5). It is not ready unchanged: adopt A's regression-test integration and all-discovered primary metric, add A's independent blindness audit, and treat B's conservative forecast as better supported than C's optimistic forecast (A sections 8.6 and 9; B section 9; diff-analysis X-008, X-012 and X-017).

Citation key: A means `variant-1-opus-architect.md`, B means `variant-2-sonnet-refactorer.md`, C means `variant-3-haiku-qa.md`, and DA means `diff-analysis.md`, all in the supplied adversarial directory. These are proposal claims, not executed results. DA's Fact check says the experiment evidence is outside this working tree and its figures are unverified here; I therefore use the reported F22/N5/N12 sequence as a design example, not independently established causal evidence. Repository checks below are limited to the specific source excerpts read during this debate.

#### Steelman of Variant A

A attacks the actual granularity problem rather than merely renaming scope rules. Its section 3.1 says S1 uses approximately 240-byte paragraph lines, and its section 3.5 computes changed tokens within changed lines. That is a persuasive way to prevent a one-word correction from reopening an entire paragraph, with a concrete test oracle in section 8.4: "One changed word in a 300-character line" produces a changed span containing that word.

A also has the most complete integration reconnaissance. Section 8.6 identifies the shipped-command inventory and unattended-section set checks, and DA's Fact check confirms both. Its section 9 counts deferred and demoted labels in the primary proxy and requires a fresh final-document blindness audit. Those choices directly test whether apparent convergence is just suppressed reporting. Section 4.4's replay of accepted reports is a useful consistency check, although not a security boundary against an owner able to replace every artifact.

The strongest case for A is therefore a small reviewer-facing change with precise eligibility and measurable blindness, not a claim that token matching proves semantic correctness. A itself admits anchor gaming, id gaming, and false PASS from demotion in section 10.

#### Steelman of Variant B

B provides the best skeptical account of the proposed causal mechanism. Its section 1 replay says the last review's five items become two while "blocking 1 to 1" stays unchanged. Unlike an optimistic surface-size argument, this explicitly distinguishes removing noise from fixing the defect-generation rate. Its section 9 F1 asks whether high remaining counts on mapped fix hunks show that scope is the wrong lever.

B's explicit sidecar fix map is clearer and less intrusive than A's implicit mapping through document ids or deleted quotes (B section 5.2; A V2). B also anticipates wrong-directory resets with `--expect-round`, records fix chains, and proposes independently revertible inert and experiment stages (sections 2, 5.3 and 8). These are strong operational and regression-risk choices. B section 12 honestly identifies worker permissions as an experiment-blocking uncertainty and admits that the worse replicate's finding composition has not been read.

The strongest case for B is a cheaper, observable experiment that may correctly fail its success bar. Its cautious forecast and explicit alternatives to the scope hypothesis are strengths, not lack of advocacy (B sections 1 and 9).

#### Key strengths claimed

1. **C distinguishes invalid evidence from a valid negative review.** Section 4 says, "A second reject marks the run invalid," preserves diagnostics, and prohibits another fix cycle. Section 3 explicitly separates operation success from the review verdict. P0 state tests then require that persistence failures and invalid drafts never produce PASS (section 13). This is a testable acceptance property, not simply the word "fail-closed."

2. **C checks where a repair may occur, not merely which id it claims.** Section 3 requires each actual edit group to have exactly one open blocking owner and fit a footprint approved before editing. Coupled sites must be listed beforehand. Section 13 tests undeclared sibling edits, minor-owned spelling corrections, boundary insertions, and merged adjacent fixes. A valid id on an unrelated distant change is insufficient under C, whereas A V2 and B F1 lack this coordinate-containment requirement. C section 5 correctly concedes that a semantically unrelated change inside an approved footprint can still pass mechanical checks.

3. **C does not confuse an outcome string with confirmed harm.** Section 4 requires a coordinator-confirmed concrete wrong implementer outcome: "A nonempty outcome string is necessary but not sufficient." Section 3 pins confirmation to the draft and surface digests. The manual semantic cases in section 13 contrast a real changed-rule dependency with an unrelated complaint quoting the same changed line. This does not automate semantics; it makes responsibility and observed acceptance evidence explicit.

4. **C has the strongest deletion and context boundary oracles.** Section 3 gives deletions an exact old-side quote and a current insertion-boundary repair footprint. Section 13 tests both a genuine lost-rule finding and a deleted line falsely claimed as current. It separately rejects unchanged context inside an otherwise valid hunk. Those cases directly cover boundary errors that a broad hunk-membership check can miss.

5. **C preserves the hard case rather than purchasing convergence with a severity ceiling.** Section 5 states that new defects introduced by authorized fixes "are not capped to minor" and that the cap guarantees termination, not correctness. Section 13's complete stubbed chain ends with an R3 child still open, followed by refusal of a fourth review or third fix. This is a concrete regression test for the very failure the proposal must not hide.

6. **C makes release criteria and operational failures inspectable.** Sections 13-14 cover strict JSON duplicate keys, zero findings, stale ids, all-anchor validation, report-copy hashes, isolated HOME installation, original-command preservation, lock contention, crash recovery, and resource limits. Section 8 also removes the copied package-only template lookup, unlike A's and B's copy-preservation promises. The source excerpt at `/home/coder/workspaces/worktrees/IronClaude/bs346-diffgate/src/superclaude/commands/spec-panel.md`, under `## Tool Coordination`, confirms that lookup exists.

7. **C limits what a successful experiment may mean.** Sections 6 and 9 say scoped PASS is not permission to ship, call historical controls historical, require the effect to exceed observed spread, and carry early-PASS bytes forward without an extra repair. Section 10 prices coordinator Read-backs and rejected reports rather than describing helper runtime as the whole cost. The metric ambiguity discussed below must be fixed before these safeguards support a valid comparison.

#### Weaknesses identified in Variant A

1. **Demotion can turn an evidence failure into a misleading scoped PASS.** A section 4.3 sends twice-invalid new findings to `deferred: unanchored`; section 10 explicitly names "False PASS from demotion." Counting demotions in the experiment proxy is useful but does not repair the operational acceptance signal. C section 4's invalid termination is safer for the seed's demand that enforcement be mechanical, with a measured cost for unusable output.

2. **A's fix gate authorizes labels, not bounded repairs.** V2 accepts a hunk if added text carries a blocking id or removed words overlap a finding quote. Section 10 acknowledges that "A valid id pasted onto an unrelated edit passes the gate." The fact that the next reviewer sees it once does not prevent unnecessary growth or fix-induced defects. C's preapproved footprints reduce this concrete escape without claiming semantic minimality (C sections 3 and 5).

3. **Report replay is not independent confirmation.** A section 4.4 recomputes syntax, anchor membership and arithmetic from the recorded report. A section 7 still leaves the truth of the outcome and resolution to reviewer judgment. C sections 3-4 add a separate coordinator decision and test its exact draft binding. That separation costs more, but it checks a different failure mode than replaying the same formal inputs.

4. **A's copy rule contradicts its own portability test.** Section 8.1 promises a byte copy with only the enumerated changes and "Nothing else changes," while section 8.5 forbids the package-source string. DA X-015 identifies the existing template lookup; the source excerpt read here confirms it. C section 8 explicitly removes it. A's strongest integration work does not excuse this independently failing acceptance condition.

5. **Token precision is not enough evidence for the forecast.** A section 9 scales fix rows and predicts mean proxy 2.0, while section 5 admits missed defects on closed fix text will not reopen. DA A-002 and A-006 identify unmeasured density and replicate-composition assumptions. Keep A's token-level experiment and blindness audit, but do not treat its probability estimates or smaller surface as demonstrated quality improvement.

#### Weaknesses identified in Variant B

1. **"Degrades fail-safe" is safe against one error direction, not all of them.** B section 4 tier 3 moves malformed finding-level claims to deferred and returns exit 0. That prevents unanchored blockers, but can remove a real changed-line blocker from acceptance. B's own section 12 question 7 acknowledges the trade. C stops invalid instead, preserving the distinction between malformed evidence and no blocker.

2. **Merged hunk ranges permit unrelated unchanged anchors.** B section 3 merges candidate hunks separated by up to two lines; C6 then checks whether the cited range lies inside the reviewable hunk range. A gap line inside that merged range can therefore become eligible even though it did not change. C section 3 explicitly says context lines never become eligible merely by sharing a hunk, and section 13 tests that condition. B's pure-deletion policy, which permits neighboring current lines, also needs C's explicit old-side loss evidence to avoid confusing absence with current text.

3. **The `via` quota bounds discovery rather than harm.** B C11 accepts at most two dependency findings through unchanged text, and section 12 admits that number is a guess. If three real changed-rule regressions exist, the third should not cease blocking because it is third. C section 7 keeps the changed cause as the primary anchor and requires dependency confirmation without a discovery quota. That still permits unchanged context to explain the consequence.

4. **A sidecar map without containment still permits id laundering.** B F1-F3 validate ownership labels and coverage, and section 10 R5 concedes that an unrelated edit can map to a blocker. The 1,500-byte advisory warning cannot reject that edit and is explicitly uncalibrated (sections 5.2 and 12). C's footprints are the stronger mechanical check; B's warning can remain optional observability, not a substitute for authorization.

5. **The claimed minimal transformation has two confirmed integration holes.** B section 8.4 refuses routing-test edits, but DA X-012 and the read shipped-command equality show that adding the command requires inventory accommodation. B section 8.1 preserves all untouched sections while section 8.3 prohibits package-source references; DA X-016 and the copied template lookup make both promises incompatible. B's drift guard is valuable after the legitimate exception is explicitly specified.

6. **The worked replay is useful but internally overprecise.** B section 1 assigns the line carrying both N1 and N11 to the minor group, yet F1 permits its blocking N1 owner. DA X-018 correctly points out that the claimed 13 allowed lines becomes 14 under B's stated rule. The replay supports a qualitative noise reduction hypothesis, not the exact line ratio used in the forecast.

#### Concessions (genuine weaknesses of Variant C)

1. **C cannot meet its own regression promise without changing existing tests.** Section 8 forbids edits to the routing and worker-contract surfaces, while sections 13-14 require their regression checks to pass. The read excerpts at `/home/coder/workspaces/worktrees/IronClaude/bs346-diffgate/tests/recommend/test_routing_refresh.py` show shipped commands must match the active inventory after enumerated exclusions. The read `/home/coder/workspaces/worktrees/IronClaude/bs346-diffgate/tests/skills/test_worker_contract.py` helper requires exact equality of unattended-section names. A new command with that heading violates both expectations. Accept A's explicit variant registration approach, but adapt its unattended assertions to C's intentionally changed failure semantics rather than requiring byte identity (DA X-012 and X-017; A section 8.6; C section 8).

2. **C's bar metric is ambiguous and must lose to A+B's definition.** C section 9 says it retains the original proxy rule, but labels the bar "Open CRITICAL+MAJOR proxy" and separates deferred claims into another count. DA X-008 identifies a real ambiguity, not a wording preference. Pre-register all-discovered critical+major, including deferred and rejected/demoted proposed labels as applicable, as the comparison metric; report scoped effective blocking separately. Do not claim an early clean PASS solely because severe discovered claims were moved out of scope (A section 9; B section 9).

3. **C lacks an independent blindness audit.** Raw drafts and ancestry cannot reveal a defect no reviewer recorded. A section 9's fresh final-document review, classified into original and fix-written text, is superior for that failure. Add it as an out-of-loop observation, with no automatic new fix cycle; C section 13's semantic fixtures do not replace it.

4. **C's optimistic forecast has weak support.** The proposed 1 and 2 proxies in section 9 are expressly "hypotheses, not calibrated estimates." Neither the unexamined worse replicate nor the possibility of denser findings on fewer lines supports that precision (DA A-002 and A-006). B's lower-confidence forecast and wrong-lever condition are better choices until composition and actual runs are examined. All historical experimental counts remain unverified in this checkout (DA Fact check).

5. **Strictness adds real failure modes and under-fixing risk.** C section 10 admits adjacent legitimate fixes can merge into a rejected mixed-owner group and valid structural repairs can expand the surface. Sections 3 and 10 add more state, coordinator confirmations and roughly 5-13 minutes of estimated overhead. Footprint rejection must be measured alongside unresolved priors, not congratulated as scope control when a correct repair cannot be expressed (C section 12 question 3; DA A-003).

6. **C's line-level policy leaves large paragraph surface and whitespace blindness.** A section 3.1's one-paragraph-per-line observation challenges C's precision. C section 10 explicitly says ignoring spaces and tabs can hide indentation, shell-argument and Markdown changes. C's raw-edit ownership is stronger than silently ignoring those edits, but it does not make them eligible blockers. Test semantic whitespace fixtures and report that limitation, rather than claiming general document correctness (C sections 3, 10 and 13).

7. **C overstates the plugin rationale and mixes two acceptance layers.** DA's Fact check contradicts C's description of existing plugin drift as one word, and DA confirms parity is not mandatory for every new command. A+B's source-only experimental delivery is smaller unless plugin runtime is explicitly in scope. Also C section 14 calls implementation acceptance separate from experiment success but includes the S1 screen as criterion 15; split those gates clearly. C section 8's removal of the source-only lookup remains necessary regardless of whether mirrors ship.

8. **No actor-placement choice creates an unskippable harness.** C section 7 admits the coordinator may omit the helper, while A section 2 and B section 2 admit wrong-directory resets. C's confirmation file checks presence, not truth (section 3). Require transcript evidence, wrong-directory and nonzero-exit recovery probes, and disclose invalid runs and costs rather than claiming a sandbox. B section 12's worker-permission smoke preflight should also be retained.

#### Shared assumptions

A-001: QUALIFY: Recovery compliance is an acceptance condition to observe, not a property conferred by exit codes; exercise nonzero exits, stale state and attempted directory resets, then require matching transcript and ledger evidence (C sections 4 and 13; DA A-001).
A-002: REJECT: Smaller scope does not logically imply fewer real findings; record findings per eligible line or token alongside distinct defects, deferred counts and the independent blindness audit before attributing a gain to narrowing (A section 9; B section 1; DA A-002).
A-003: QUALIFY: Blocking-only ownership can reduce gratuitous edits but also prevent valid coupled repairs; count unresolved priors, legitimate footprint/map rejections and stalls as harms, not just prevented growth (C sections 10 and 12 question 3; B F2; DA A-003).
A-004: REJECT: Added scope instructions can change behavior without enforcement, so historical comparisons identify only the combined treatment; a briefs-only arm is needed to isolate the script's contribution (C section 8 calls the step lines treatment; DA A-004).
A-005: QUALIFY: Full-document eligibility in R1 does not mean unchanged elicitation when JSON, footprints and confirmation are new; compare R1 counts, labels and formatting failure rates before using Arm B as an interchangeable baseline (C sections 3 and 9; DA A-005).
A-006: REJECT: One best replicate's ancestry cannot establish the worse replicate's composition; inspect both before defending the forecast, or label it an unsupported extrapolation as B section 12 question 12 does (DA A-006 and Fact check).

#### Per-point positions

| Point | Superior approach (A, B, C, or "A+B" style merge, or "tie") | One-line reason |
|---|---|---|
| S-001 | C | Separate test and acceptance sections make review obligations easier to inspect, though criterion 15 must move to the experiment gate (C sections 13-14). |
| S-002 | C | P0 eligibility, edit ownership and crash/state oracles exceed the compact case lists, with explicit negative cases (C section 13; A 8.4; B 8.3). |
| S-003 | C | Numbered implementation criteria expose omissions independently of an optimistic forecast (C section 14). |
| S-004 | A+C | A's verbatim replacement bullets reduce implementation ambiguity; preserve C's stricter acceptance ownership within that format (A 8.1; C section 8). |
| S-005 | A+B | Named functions and a bounded outline are more actionable than C's prose outline; estimates are budgets, not proof (A 8.3; B 8.2; C section 8). |
| S-006 | A+B | Shared exit tables with an actor column are easier to test and act on than C's inline sentence (A 3.3; B section 3; C section 3). |
| S-007 | B+C | Preserve B's explicit unverified tags and C's PROPOSED labels; dense citations cannot verify absent experiment evidence (B section 1; C section 1; DA Fact check). |
| S-008 | A | Bullet-by-bullet mapping with residual risk gives the clearest trace from the existing contract to enforcement (A section 7). |
| S-009 | C | Cost envelope plus guard-and-residual table makes semantic and operational limits explicit (C section 10). |
| S-010 | B+C | B identifies setup blockers; C defines initial defaults so open questions do not silently select runtime behavior (B section 12; C section 12). |
| C-001 | C | Independent coordinator acceptance adds semantic confirmation that worker-owned script calls alone cannot provide (C sections 2-4; B section 3). |
| C-002 | C | Explicit protocol activation and complete-directory lookup reduce mixed-install risk; all three names can install (C section 3; DA Fact check). |
| C-003 | B | Four subcommands keep the user interface smaller; command count alone does not justify weakening C's confirmation semantics (B section 3; C section 3). |
| C-004 | C | Structured stdout, explanatory stderr and separate execution/verdict fields support unambiguous automation (C section 3). |
| C-005 | B+C | B's actor-action table is clearer; retain C's explicit valid-FAIL-versus-helper-failure distinction (B section 3; C section 3). |
| C-006 | C | Strict JSON, duplicate-key rejection and digest-bound confirmation avoid a second authoritative Markdown interpretation (C sections 3-4). |
| C-007 | C | Per-round artifacts, generation checks and locking support precise crash and concurrency tests despite added storage (C sections 3 and 13). |
| C-008 | A+C | A's changed-token precision targets long paragraphs; C's exact old/new eligibility and context exclusion are necessary safety constraints (A 3.5; C section 3). |
| C-009 | C | Round, content and coordinate-bound ids reject stale identical-looking hunks without relying on caller memory (C section 3). |
| C-010 | C | Checking every claimed anchor and the exact confirmation digest closes partial-validity shortcuts (C section 4 step 4; section 13). |
| C-011 | C | Twice-invalid evidence stops invalid rather than becoming a potentially false scoped PASS through deferral (C section 4; A 4.3; B section 4). |
| C-012 | C | Explicit deferred placement plus rejection of an unanchored claimed finding best matches the seed's scripted rejection criterion (C section 4; seed Success Criteria). |
| C-013 | C | Anchor the changed cause and confirm the dependency; do not hide a third genuine regression behind B's quota (C section 7; B C11). |
| C-014 | C | Preapproved coordinate footprints prevent distant unrelated changes from passing on a valid ownership label alone (C sections 3 and 5). |
| C-015 | C | Approved repair area is a defensible authorization boundary; an uncalibrated advisory byte threshold is only observability (C section 5; B 5.2). |
| C-016 | tie | All reject severity ceilings that would hide genuine last-round fix-induced defects (A section 5; B 5.4; C section 5). |
| C-017 | C | Invalid termination also discloses deferred candidates, with explicit unverified locations and scoped-PASS limits (C section 6). |
| C-018 | C | Rendering accepted records and verdict together eliminates reviewer verdict reconciliation and append-order mistakes (C section 4 step 8). |
| C-019 | C | A coordinator-confirmed wrong outcome is stronger than a nonempty or 25-character string (C section 4; A 4.1; B C12). |
| C-020 | C | Immutable outcome/grade plus footprint-intersecting regression evidence makes identity drift explicitly testable (C sections 3-4). |
| C-021 | tie | Each design excludes minor ids from repair authorization; C adds raw-edit containment as a separate advantage (A V3; B F1; C section 5). |
| C-022 | C | Preserve physical changes rather than assuming reflow is semantically inert, and require ownership even for ignored raw whitespace (C section 3). |
| C-023 | B | The conservative estimate and acknowledged surviving mapped blocker are better grounded than C's mean 1.5 forecast (B section 9; C section 9). |
| C-024 | B+C | B gives explicit assumptions and C labels forecasts uncalibrated; no proposal has measured treatment growth (B section 9; C section 9). |
| C-025 | A+B+C | Combine A's blindness failure, B's wrong-lever diagnosis and C's integrity/spread checks without metric substitution (all section 9). |
| C-026 | A+B | Count deferred severity labels in the primary proxy; keep C's scoped blocking count secondary (A section 9; B section 9; DA X-008). |
| C-027 | C | Explicitly budgeting parent Read-backs, writes and repair overhead is more complete than helper runtime alone (C section 10). |
| C-028 | B+C | Keep B's expected-round defense and C's mandatory state, installed hashes and observed Skill invocation (B section 2; C section 8). |
| C-029 | C | Supplied predecessor paths must match pinned history rather than being ignored or silently stripped (C sections 3 and 8). |
| C-030 | A+C | C supplies richer behavior/install tests; A supplies the existing inventory and unattended registration changes C missed (C section 13; A 8.6; DA X-012/X-017). |
| C-031 | C | A helper failure must not publish an unchecked report as successful unattended execution (C section 8). |
| C-032 | A+B | Source-only experimental delivery and a separate design note are smaller; DA's Fact check does not establish a universal mirror requirement (A 8.8; B 8.4). |
| C-033 | A | A mandatory fresh blindness audit detects defects absent from all drafts; C's ancestry inspection cannot (A section 9; C section 9). |
| C-034 | C | Explicitly preserve full FINAL and rf-qa stop rules rather than presenting scoped repair review as equivalent assurance (C section 11). |
| C-035 | C | Exclusive locking, generation checks and crash tests address races that atomic replacement alone does not (C sections 3, 10 and 13; B R11). |
| X-001 | C | Coordinator acceptance is worthwhile separation of judgment, but it remains cooperative enforcement rather than an unskippable harness (C sections 2 and 7). |
| X-002 | C | Stop invalid after one repair; do not silently relabel malformed evidence to keep the loop moving (C section 4; A 4.3; B section 4). |
| X-003 | C | Physical reflow may change Markdown structure, so conservative visible eligibility is safer than unconditional token-equivalence filtering (C sections 3 and 10). |
| X-004 | C | An unchanged observation has a legal deferred array; calling it an accepted finding first must trigger a repair, not soft acceptance (C section 4 step 5). |
| X-005 | A+C | Anchor the changed cause with unchanged context as evidence; B's two-item escape cap can suppress a real third consequence (A section 10; C section 7; B C11). |
| X-006 | C | Only the generated accepted report owns the verdict, avoiding B's redundant reviewer verdict requirement (C section 4; B C1). |
| X-007 | B | An admitted likely bar failure is more credible than an optimistic extrapolation from unverified best-run ancestry (B section 9; DA A-006). |
| X-008 | A+B | All-discovered primary counts prevent a narrower verdict definition from winning the historical comparison by deferral (A section 9; B section 9; C section 9 ambiguity). |
| X-009 | C | Ignoring a raw whitespace edit for eligibility does not justify authorizing that edit without a blocker owner (C section 3; A 3.5; B section 3). |
| X-010 | C | Verify retained predecessor flags and reject mismatches instead of discarding potentially useful integrity evidence (C sections 3 and 8). |
| X-011 | A+B | No general mirror requirement is established; test the selected source-install surface before adding plugin delivery scope (DA Fact check; A 8.8; B 8.4). |
| X-012 | A | A explicitly accommodates shipped-command inventory equality; B omits it and C incorrectly forbids the needed change (A 8.6; DA Fact check). |
| X-013 | C | Preapproved footprint containment avoids an arbitrary advisory threshold without imposing a hard size limit that prevents valid repairs (C sections 3 and 5; B 5.2). |
| X-014 | C | Explicit Skill activation and isolated discovery testing make loading observable; installer facts do not require A's naming choice (C section 8; DA Fact check). |
| X-015 | C | Remove the copied package-only template read rather than promise both byte preservation and no package-source lookup (C section 8; A 8.1/8.5; DA X-015). |
| X-016 | C | Declare the portability fix as an allowed drift-guard exception; B's untouched-copy and no-source-string requirements conflict (C section 8; B 8.1/8.3; DA X-016). |
| X-017 | A+C | Register the new unattended command as A proposes, but test C's stricter failure contract rather than demanding unchanged section bytes (A 8.6; C section 8; DA X-017). |
| X-018 | A+C | C's recomputed exact edit groups avoid B's replay accounting shortcut; B's own F1 admits the line with blocking N1 ownership (C section 3; B section 1 and F1; DA X-018). |

## Round 2: Rebuttals

### Variant A Rebuttal (file debate/round2-A.md)

# Round 2: Variant A advocate (opus, architect)

Sources: round1-A.md, round1-B.md, round1-C.md, evidence-flg-r1.md, variant-1-opus-architect.md sections 4-12, diff-analysis.md. New reads (read-only) in `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r1/.dev/orca-command-refactor/review/`: `disposition-round2.md` lines 1-40 and `spec-panel-round3.md` lines 141-146.

#### Response to criticisms

### From round1-B.md

1. **B-1: the fix map is implicit and easy to game.** Concede. A's V2 (a hunk is mapped if its added text carries an open blocking id or its removed words overlap that finding's quote) is loose, and it has no `declined` outlet. The merge should use B's explicit `fixmap` with `declined <id> <reason>` lines and checks F1 to F3. A keeps only one thing here: the gate also runs inside `open`, so a skipped map stops the next review. One caveat from flg-r1: the four parent fixes there were real, mapped fixes of blocking findings. A stricter map closes id laundering. It does not touch the chains that drove that replicate's count.
2. **B-2: a bad report can end the run with no verdict.** Partly conceded. Most of A's non-demotable rules can become demotable or can be dropped. C13 (`DG-COVER`) goes away (see B-4). C12 becomes moot because the reviewer writes no verdict, so any stray `verdict:` line is stripped. The script writes the C11 header. A C6 label outside the vocabulary is recorded as `deferred: unanchored` with its raw label kept for the proxy count. A C2 duplicate id is renumbered by the script. Only C1 (no parseable `## Diffgate findings` section) and C3 (a finding id in the prose that is missing from the section) still stop the run. In both cases the script cannot tell what the reviewer meant to block on, so B's degrade would have to invent a verdict. In the merged design that stop happens rarely and fails closed.
3. **B-3: renumbering noise is named and left unsolved.** Concede, with a mechanical fix. The explicit map gets a `renumber H<k>.<n>` line. The script accepts it only if every changed token in the hunk is a digit run in a list or heading number position. The hunk still appears on the next surface, so nothing is hidden. It just needs no blocking owner.
4. **B-4: `DG-COVER` costs tokens and proves nothing.** Concede. Drop C13 and `DG-COVER`. A's own text already rated it weak evidence.
5. **B-5: the forecast rests on an untested density assumption and on one replicate's story.** Fully conceded, and flg-r1 now shows it was wrong (next section). A's section 9 said flg-r1's fix 2 made "about 5" blockers from 15 rows and that scaling to a third of the rows would cut them. The recorded data show 4 blockers from 4 blocking fixes. Cutting the 10 non-blocking rows removes one proxy item (R3-7) and no blocker. A's 60% and its "N5 would never have existed" story do not generalise.
6. **B-6: the byte copy contradicts the no-`src/superclaude` test (X-015).** Concede. Adopt C's removal of the `src/superclaude/examples/release-spec-template.md` read in `## Tool Coordination`, list it as the tenth change in A 8.1, and exempt that section in B's drift guard.

### From round1-C.md

1. **C-1: demotion can turn an evidence failure into a misleading scoped PASS.** Partly conceded. The experiment metric is already honest because demoted findings count in the R3 proxy. The operational verdict is the gap. Fix: if the demoted set holds any finding labelled critical or major, or blocking-grade under the profile, the script cannot print a clean PASS. The line reads `PASS (scoped; N demoted blocking-grade findings listed below)`, and the experiment's alternative "clean PASS by review 3" criterion does not credit it. I still reject C's invalid termination. Anchoring mistakes are the expected failure, and ending the replicate throws away a valid review and its accepted blockers.
2. **C-2: A's gate authorizes labels, not bounded repairs.** Conceded on labels (see B-1). Rejected on footprints as the fix. In flg-r1, R2-2 changed three lines (SPEC3:67, 188, 198) and R2-3 changed three lines (182, 183, 189). Each was a legitimate, mapped fix of a blocker, and each still produced a review-3 blocker. A pre-approved footprint would have contained both fixes and stopped neither chain. Footprints defend against laundering, which no replicate has shown, and they cost a coordinator step per blocker. Keep them out of the S1 arm. Report `bytes_by_id` and hunks per id instead.
3. **C-3: report replay is not independent confirmation.** Agreed, and A never claimed it was. Replay makes a hand-edited ledger worthless. It does not judge whether an outcome is true. C's confirmation file does not judge that either, by C's own account ("Presence of a confirmation is checkable; truth of its semantic judgment is not"). Both leave semantic truth to a model. The difference is cost, and replay is cheaper.
4. **C-4: the copy rule contradicts the portability test.** Concede. This is the same issue as B-6, with the same fix.
5. **C-5: token precision is not evidence for the forecast.** Concede. flg-r1 shows why: every review-3 blocker sits on words a blocking fix wrote, so a narrower surface still contains all of them. Token precision cuts review cost and anchor-gaming room. It does not cut the count of fix-induced blockers.

#### Updated assessment of B and C

**B gains the most from this round.** flg-r1 bears out its forecast (mean 3.5, about 0.25 for both replicates) and its falsification F1 "wrong lever" (R3 of 5 or more with 70% or more of blockers on mapped fix hunks). Under a diffgate arm, a flg-r1-like replicate lands at about 5 with 100% of blockers on mapped blocking-fix text, which is F1 exactly. B's fix-chain printing (U-009) is now the most useful ledger output, because every flg-r1 review-3 blocker is a length-3 chain (finding 8 -> R2-2 -> R3-1, and so on). B's remaining weaknesses are the ones B conceded: line-level hunks on paragraph lines, a reviewer-written verdict, degrade-everything on structural failure, paddable constants, and the missing `test_routing_refresh.py` edit. The merge I would accept: A's script structure, grammar, token surface, test integration and `PROFILES` seam, plus B's explicit map, `declined`, `via=`, `--expect-round`, chains, F1, staging and forecast.

**C's strongest machinery targets a failure the data do not show.** Footprints, coordinator confirmation and invalid termination guard against id laundering, padded outcomes and malformed evidence. flg-r1's count came from small, legitimate, mapped fixes that were themselves defective, and none of C's guards acts on that. C's cost (5 to 13 added minutes per loop and replicates lost to invalid termination) therefore buys protection the S1 question does not need. C is right that no variant should buy convergence by relabelling, and flg-r1 makes that warning more important, because a relabelling rule is now the only thing that could make the bar pass on a flg-r1-like run. C's other contributions belong in the merge: U-016 (line 220), separate acceptance criteria, the spread check, the Skill-invocation transcript check, old-side deletion anchors, the scoped-PASS sentence, the isolated-HOME install test, and valid FAIL exiting 0.

#### flg-r1 evidence: revised prediction and any in-theme lever

**What flg-r1 shows.** Review 3 has proxy 6 and 4 blockers. All 4 blockers sit on text written by fixes of blocking findings: R3-1 on R2-2's fix, R3-2 on R2-3's fix, R3-3 on R2-1's fix, and R3-4 on R2-1's and R2-4's fixes. Each review-2 blocker in turn sits on text written by a round-1 blocking fix. A blocking-only fix gate (all three variants) removes R3-7 and nothing else. R3-8, a MAJOR label graded minor, sits on SPEC3:64, which blocking fixes also wrote, so it stays.

**Revised Variant A prediction for the S1 bar.**

| Quantity | Round 1 (A section 9) | Revised |
|---|---|---|
| flg-r1-like replicate, R3 critical+major proxy | (not addressed) | 4 to 5 (4 blockers, plus R3-8's MAJOR label; R3-7 removed) |
| flg-r2-like replicate | 1 to 3 | 0 to 2 (N5 and N12 may never exist if fix 1 skips F22) |
| Mean over two fresh replicates | 2.0 | about 3.0 (range 1 to 5) |
| P(both replicates 3 or fewer) | about 60% | about 0.25, the same as B |
| P(at least one replicate triggers B's F1) | n/a | about 0.5 |
| Growth after 2 fix cycles | 15% to 25%, P about 0.95 | 15% to 25%, P about 0.9 (Arm B's flg-r1 already sits at 27.8%) |

The reason is that the observed per-blocking-fix defect rate at fix 2 swings from about 0.17 (flg-r2: 6 blocking fixes, 1 new blocker) to 1.0 (flg-r1: 4 fixes, 4 blockers). With two fresh replicates, the bar passes only if both draw a low rate. Diffgate does not change that rate. It removes noise from minor fixes and makes the chains visible.

**Is there an in-theme lever that acts on blocking-fix-induced chains without relabelling or hiding real defects?** I checked each of the four parts of the theme.

- **Computed surface: no.** The four blockers sit on new words that blocking fixes wrote. V1 puts that text in scope by design, and the token-level surface still contains it. Narrowing the surface further would mean not reviewing fix text, which is hiding.
- **Anchor checker: no.** Each blocker anchors on changed words and cites other lines as evidence. R3-4, for example, anchors on WC-4's new text at SPEC3:64 and cites WC-6 at SPEC3:66, a line no fix-2 row lists as changed. A's C5 accepts that legitimately. Rejecting such findings would be hiding.
- **Fix gate: no reduction.** All four parent fixes were mapped blocking fixes, and two of them changed only three lines. A byte budget or a footprint would not have stopped them. A stricter gate can only push revisers toward under-fixing, which moves the count from "new" to "open prior" (A-003). Both count the same in the proxy.
- **Ledger: detection only.** Before fix 2, the ledger can compute that each review-2 blocker sits on text a round-1 blocking fix wrote. In flg-r1 that recurrence flag would have fired on all 4. The ledger can print the chain, mark the region "second attempt", and, under B's rule, escalate a length-3 chain to a person. Escalating to a person leaves the unattended loop that S1 measures, so it is not an honest lever for this bar. Any rule that downgrades, defers or excludes recurrence blockers is relabelling and is ruled out.

**Honest answer: no mechanism inside the diffgate theme lowers the count of blocking-fix-induced blockers without relabelling or hiding them.** The closest candidate is a reviser aid, not a gate. `gate` could print, for each of the reviser's own hunks, the unchanged lines that share an identifier token with it (WC-6, AC-1.2, `--report-dir`), so the reviser checks for knock-on conflicts before the next review. Two of flg-r1's four blockers (R3-3 and R3-4) have that cross-reference shape. R3-2 does not, because it rests on an external fact about `git status`. This aid is mechanical input but a prose-dependent action, it is unmeasured, and I expect its effect to be small. It needs its own ablation arm and must not count as part of the diffgate result.

**What follows for the experiment.** A should adopt B's F1 as its primary diagnostic and pre-register the forecast above. If the owner runs S1 anyway, the result most likely to be learned is a measured per-blocking-fix defect rate under scope control. That is useful, but it is not a pass. The lever that F1 points to, fix quality, sits outside this theme.

#### New evidence

1. **The S1 spec really is one paragraph per line, and fix text is paragraph-sized.** flg-r1's `disposition-round2.md` section 3 reports 67,886 bytes and 293 lines before fix 2, 73,807 bytes and 293 lines after, "60 lines changed", and "every edit stayed inside existing lines". A line-level surface for review 3 would therefore be 60 paragraph lines. This supports A's token-level surface (C-008) on cost and anchor precision, not on count.
2. **Small fixes produced blockers.** R2-2 changed SPEC3:67, 188 and 198, and R2-3 changed 182, 183 and 189 (evidence note). Each produced a review-3 blocker. That is direct evidence against size or footprint containment as a convergence lever (C-014, C-015, X-013).
3. **The reviser deliberately spread blocking fixes.** `disposition-round2.md` method: "Root causes, not single cells: where a fix changed a shared rule, every passage that depends on it was brought into line in the same revision (listed under 'Knock-on edits' in the R2-1 and R2-4 rows)." Knock-on edits carry the blocking id, so every variant's gate passes them. R3-3 and R3-4 sit on R2-1 and R2-4 text. No gate design can tell a knock-on edit from the core fix without semantics.
4. **The chains recur on the same lines.** The same method note says settled round-1 fixes were "reopened only where a finding names them (R2-2 on finding 8, R2-3 on finding 9 ...)". Lines 67 and 188 were written by finding 8's fix, reopened by R2-2, and then cited by R3-1. A ledger can detect this recurrence mechanically, which supports B's chain output (U-009).
5. **The review-3 blockers are real defects with a dependency shape.** `spec-panel-round3.md` lines 141-144: R3-1 (a closed list in 7.2 step 5 against WC-7), R3-2 (`git status --porcelain --untracked-files=all` misses ignored paths, tested in a scratch repo), R3-3 (new P1 scope against AC-1.2 at SPEC3:200), and R3-4 (the WC-4 report directory against WC-6 and the Resume column). All anchor on changed text, so none needs `via=`. That narrows X-005 to a rare case.

#### Shared assumptions

- A-001: QUALIFY: the merged recovery path (correct once, then demote, stop only on C1 or C3) needs little improvisation, but compliance is assumed; record it per replicate as a validity input.
- A-002: QUALIFY: flg-r1 shows a smaller surface removes noise from minor fixes (R3-7) but not blockers, which sit on blocking-fix text; record findings per changed token so a density effect is visible.
- A-003: QUALIFY: any gate stricter than "mapped to a blocker" can only move counts from new to open prior; report open priors and `declined` lines separately from new findings.
- A-004: REJECT: the added brief lines are prose that can act without the script; claim the combined treatment or add a briefs-only arm, and keep the reviser cross-reference aid in its own arm.
- A-005: QUALIFY: A's DG-line change is the smallest review-1 change, but review-1 blocker counts must still be checked against Arm B's 13 to 17 as a validity gate.
- A-006: REJECT: now answered by evidence: flg-r2's composition does not hold for flg-r1, and A withdraws the forecast and causal story it built on flg-r2.

#### Per-point positions (updated)

| Point | Superior approach (A, B, C, merge like A+B, or tie) | One-line reason |
|---|---|---|
| S-001 | C | Separate test and acceptance sections; all three advocates now prefer C or call it a tie. |
| S-002 | C | Tiered P0/P1 tests with negative cases are the easiest to execute; fold A's 16 script cases into C's tiers. |
| S-003 | C | Implementation acceptance kept apart from experiment success, with C's criterion 15 moved to the experiment gate as C concedes. |
| S-004 | A+C | A's verbatim bullets as single physical lines, plus C's removal of the line-220 template read as a tenth listed change. |
| S-005 | A+B | A's signatures fix the interfaces; B's named constants and line budget bound the size. |
| S-006 | A+B | One shared exit table with a who-acts column; all three advocates accept this. |
| S-007 | B+C | flg-r1 shows dense citations did not stop A's wrong causal story; B's UNVERIFIED tags and replay plus C's PROPOSED labels are the better discipline. |
| S-008 | A+B | A's bullet-keyed residual-risk table plus B's extra concerns such as step order. |
| S-009 | A+C | A's residual column plus C's separate cost envelope. |
| S-010 | B+C | B flags experiment blockers; C gives every question a default. |
| C-001 | A+B | Worker-owned steps locked to each other; the coordinator only reads `status`; C's confirmation checks presence, not truth, by C's own account. |
| C-002 | A | The verified installer analysis decides the name; a by-path call plus C's transcript check of that call is enough. |
| C-003 | A+B | B's smaller set (fold `final` into `close`, `status` optional), keeping A's rule that `open` re-runs the gate. |
| C-004 | A+C | One JSON object per call, with separate verdict and execution-success fields. |
| C-005 | B+C | B's one-meaning-per-code table with C's rule that a valid FAIL exits 0. |
| C-006 | A | JSON-string quotes in DG lines; B concedes `[[...]]` breaks on `]]`; C's strict JSON draft is the largest review-1 change (A-005). |
| C-007 | tie | File layout does not change behaviour; flat files or per-round folders both work. |
| C-008 | A+C | Token-level surface for paragraph lines (flg-r1: 60 changed lines, line count unchanged), plus C's rule that context is never eligible. |
| C-009 | A | `H<k>.<n>` never repeats and is shared by the gate and the next surface; a digest adds nothing the ledger hash lacks. |
| C-010 | A+C | A's rules without C13, plus C's validation of every claimed anchor. |
| C-011 | A+B+C | Demote or degrade anchor failures (A, B), stop only on C1 or C3 (A), and never print a clean PASS when blocking-grade findings were demoted (C). |
| C-012 | A+B | An unanchored finding is a free deferral; C's reject spends the one repair on a legal outcome. |
| C-013 | B | Quote-checked `via=` gives a legal route; over-cap `via` findings should be deferred and still counted in the proxy, which answers C's third-regression worry. |
| C-014 | B | An explicit map with `declined`; footprints would not have stopped flg-r1's chains (R2-2 and R2-3 changed three lines each). |
| C-015 | A+B | Report bytes and hunks per id with no gate; flg-r1 shows small fixes still induce blockers. |
| C-016 | tie | All three reject a severity ceiling; flg-r1 makes a ceiling the obvious relabelling trap. |
| C-017 | B+C | B's `seen:` rounds and no-cite rule plus C's scoped-PASS sentence; A's appendix placement is compatible. |
| C-018 | A+C | The reviewer writes no verdict and the script supplies it; B now agrees. |
| C-019 | A | Presence of an outcome with no paddable constant; C's confirmation is presence-only by C's own words and costs a coordinator step. |
| C-020 | A | No severity field on carried status lines makes upward drift impossible by grammar. |
| C-021 | tie | All three keep minors away from the reviser; in flg-r1 this removes only R3-7. |
| C-022 | A+B | A word-identical reflow is not a hunk; B's coverage warning flags a degenerate surface. |
| C-023 | B | flg-r1 bears B out: 4 of 4 review-3 blockers sit on blocking fixes; A withdraws its 60%. |
| C-024 | tie | All forecasts clear 44.4%; Arm B's flg-r1 already sits at 27.8%. |
| C-025 | A+B+C | B's F1 as the primary diagnosis, A's blindness and demotion conditions, C's spread check. |
| C-026 | A+B | The all-discovered count gates the bar; C concedes. |
| C-027 | C | The most complete accounting; A's estimate omitted correction turns. |
| C-028 | A+B+C | A's hash of the untouched `spec-panel.md` and no `--force`, B's `--expect-round`, C's installed-file hashes and transcript check. |
| C-029 | B | Dropping the 427 flags from Usage is simplest; ignoring them (A) keeps dead text. |
| C-030 | A+B+C | A's two existing-test edits, B's drift guard with a `## Tool Coordination` exemption, C's isolated-HOME install test. |
| C-031 | A+B | A verbatim `## Unattended mode` with the name swapped stays pinnable; A's C1/C3 stop already marks the contract failed, which covers C's concern. |
| C-032 | A+B | No mirror is needed and a separate design note keeps 427's doc historical; C concedes. |
| C-033 | A | A fresh-review blindness audit classified by ledger history; all three now agree. |
| C-034 | A+C | The `PROFILES` seam for rf-qa, with C's limits on replacing `/sc:implement` FINAL or weakening rf-qa guards. |
| C-035 | A+C | Ledger replay plus C's lock and size limits, which are cheap in a script meant for reuse. |
| X-001 | A+B | Same as C-001: worker-run steps with mutual locks. |
| X-002 | A+B+C | Same as C-011: demote, stop only on structure, no clean PASS with demoted blocking-grade findings. |
| X-003 | A+B | A word-identical reflow carries nothing to review; edited words inside it still surface. |
| X-004 | A+B | Same as C-012. |
| X-005 | B | `via=` covers the case it exists for, but all flg-r1 review-3 blockers anchored on changed words, so it is a narrow escape, not a driver. |
| X-006 | A+C | Same as C-018. |
| X-007 | B | flg-r1 evidence supports B's 0.25; A's revised forecast now matches it. |
| X-008 | A+B | Same as C-026. |
| X-009 | A+B | Whitespace-only edits are not hunks and need no owner. |
| X-010 | B | Same as C-029. |
| X-011 | A+B | The parity test pins only README-listed commands. |
| X-012 | A | Only A plans the `_POST_REFRESH_ADDITIONS` edit; B and C concede. |
| X-013 | A+B | No gate, bytes reported; R2-2 and R2-3 show a size gate would not have helped. |
| X-014 | A+B | A name that does not match the command, called by path; C's Skill activation is a legitimate alternative, not an error. |
| X-015 | C | A concedes; remove the line-220 read. |
| X-016 | C | Same fix; B's drift guard exempts `## Tool Coordination`. |
| X-017 | A | Register the variant in a `UNATTENDED_VARIANTS` map; the verbatim section keeps parity with the parent. |
| X-018 | tie | B conceded the 13 versus 14 slip; it has no design effect. |

### Variant B Rebuttal (file debate/round2-B.md)

# Round 2: Variant B advocate (sonnet, refactorer)

Sources: round1-A.md, round1-B.md, round1-C.md, round2-A.md, evidence-flg-r1.md, diff-analysis.md, variant-2-sonnet-refactorer.md (grep for C1, degrade, FIX_BUDGET). New read-only checks in `/home/coder/workspaces/worktrees/IronClaude/exp346-ab-flg-r1/.dev/orca-command-refactor/`: `review/disposition-round2.md` lines 1-45, `review/spec-panel-round3.md` lines 138-151, and token counts on `specs/orca-worker-contract-spec.md` (lines 64, 66, 67, 162, 188, 200). Round1-C is the only C text so far; C has not yet rebutted.

#### Response to criticisms

### From round1-A.md (A's weaknesses of B)

1. **A-W1, byte-identical copy and drift guard contradict "no `src/superclaude`" (X-016).** Concede. Adopt C's removal of the line-220 template read (U-016) as a named change in the variant. The drift guard compares every untouched `## ` body to `spec-panel.md`, and for `## Tool Coordination` compares after that one substitution.
2. **A-W2, `test_routing_refresh.py` is missing from B's plan (X-012).** Concede. Stage B adds `"spec-panel-diffgate"` to `_POST_REFRESH_ADDITIONS`, as A's 8.6 does.
3. **A-W3, graceful degradation hides format failure.** Partly concede. Structure failures (no FINDING lines and no `FINDINGS none`, or a round line that disagrees with the ledger) that survive the one repair now exit 1 with no verdict, which is A's rule. Everything else still degrades. A degraded run can no longer print a clean PASS: it prints `PASS (scoped; N degraded or deferred blocking-grade findings)`, which is C's disclosure. What I keep: degraded and deferred findings stay in `R3-proxy-all` by their reviewer label, so degrading cannot win the bar.
4. **A-W4, reviewer writes a `verdict:` line (X-006).** Concede. The reviewer writes none; `check` prints the verdict line and the command appends it. Rule C1's verdict clause and C13 are deleted, which removes a reject path.
5. **A-W5, arbitrary constants.** Concede both. `OUTCOME_MIN = 25` is replaced by A's rule (an `outcome` other than `-`), which has the same checkability and no padding threshold. `FIX_BUDGET_BYTES` and the `over_budget` flag are removed; the gate reports `bytes_by_id` and hunks per id as figures only. flg-r1 supports removal: R2-2 and R2-3 were three-line fixes and each still produced a review-3 blocker, so a byte budget would not have fired where it mattered. Fewer constants is less debt.
6. **A-W6, replay count 13 versus 14 (X-018).** Concede. The gate would have allowed 14 lines. I now state the replay only qualitatively (noise removed, the induced blocker kept).
7. **A-W7, concurrency left open.** Concede the cheap half. `begin` re-runs `check` on the recorded report and exits 2 on any ledger mismatch (A's U-004), and a single exclusive-create lock file guards writes (a few lines). C's size limits and symlink refusal are cut as over-scope for an experiment arm.

### From round1-C.md (C's weaknesses of B)

1. **C-W1, degrade is safe in one error direction only.** Covered by A-W3 above. The other direction (a real changed-line blocker removed from acceptance) stays visible: it is listed in `deferred.md` with `reason=unanchored`, counted in the bar, and named in the scoped-PASS line.
2. **C-W2, `MERGE_GAP = 2` lets unchanged gap lines become eligible anchors.** Concede; this was a real hole. Eligibility now comes only from lines that changed, tested at token level (A's C5 overlap rule). `MERGE_GAP` only groups adjacent changed lines into one hunk id for the fix map and the display; gap lines and display context are never eligible. Pure deletions use C's old-side quote plus an insertion-boundary anchor.
3. **C-W3, the `via` cap bounds discovery, not harm.** Partly concede. Evidence: in flg-r1 none of the 10 review-3 findings needed `via` (all anchor on changed lines), so the cap is a rare-case guard, not a driver. Fix: a `via` finding over the cap is not dropped; it is deferred with `reason=via-cap`, counted in the proxy, and forces the scoped-PASS wording. `VIA_CAP` remains a guess and its use is recorded.
4. **C-W4, a sidecar map without containment permits id laundering.** Partly concede. Footprints are the only mechanism of the three that closes laundering, and I say so. But the data show no laundering: the flg-r1 reviser tagged every changed passage with its `R2-N` id and listed knock-on edits per row (`disposition-round2.md` lines 11-12), and the four blocking fixes were genuine. Footprints would have contained R2-2 and R2-3 (three lines each) and stopped neither chain, at the cost of a coordinator step per blocker. Position: not in the S1 arm. Hardening trigger for later: if the `bytes_by_id` audit finds mapped edits with no word overlap with the finding's quote, add footprints then.
5. **C-W5, two integration holes (X-012, X-016).** Concede; same as A-W1 and A-W2.
6. **C-W6, the replay is overprecise (X-018).** Concede; same as A-W6.

### From round2-A.md (A's rebuttal remarks on B)

1. **Line-level hunks on paragraph lines.** Concede the eligibility part: anchors are now checked at token level. Counter on ids: A's token-level hunks needed a new `renumber H<k>.<n>` rule that depends on parsing "a digit run in a list or heading number position". Block-level ids avoid the problem, because a renumbered list merges into one hunk that needs one owner. Merge: token overlap decides which text can carry a blocker; block ids decide who owns an edit.
2. **Reviser-written verdict, degrade-everything, paddable constants, missing routing edit.** All four conceded above (A-W4, A-W3, A-W5, A-W2).
3. **"Escalating a length-3 chain to a person leaves the unattended loop."** Concede. The chain line is a report line only (`R1.5 -> R2.1 -> R3.2`). The "revise this region by hand" advice moves to the end-of-loop summary; no rule halts on chain length. The only halt is 427's own `halt: escalate` at a FAIL at the cap.
4. **Fix map inline-id convenience.** A's inline form has one real advantage: flg-r1 revisers already tag changed spec passages with `R2-N`. Merge: `fixcheck` pre-fills `fixmap` candidates from inline `R<k>.<j>` tags in the added text, and the reviser confirms or writes `declined`. The explicit file stays the authority.

#### Updated assessment of A and C

**A.** Stronger than in round 1 and closest to a base for the merge. It conceded the implicit fix map, `DG-COVER`, the line-220 contradiction and its 60% forecast, and its stop-only-on-C1/C3 rule now matches what I conceded. Its honest answer to the flg-r1 question (no honest lever) is correct. What still favors A: token-level eligibility (I adopt it), the verified installer naming analysis, both existing-test edits, ledger replay, `PROFILES`, the grammar with no severity field on carried lines. What still favors B over A: explicit `declined` and map, `via=`, `--expect-round`, chains, F1, staging, and the one replay on recorded data. A's new `renumber` rule is a heuristic parser rule that block ids make unnecessary.

**C.** Round 1 showed the most careful acceptance design, and flg-r1 sharpens the cost side. Footprints, coordinator confirmation and invalid termination guard against laundering, padded outcomes and malformed evidence. None of those appears in the flg-r1 data, and none would have changed its count. Invalid termination is also worse with n=2: a single mistyped anchor discards a replicate. C's integrity parts stay in the merge: U-016 (line 220), U-017 (spread check), U-019 (Skill-invocation transcript check where a skill is used), the acceptance-versus-experiment split, old-side deletion anchors, valid FAIL exiting 0, the scoped-PASS sentence, the isolated-HOME install test. C's own concessions (metric ambiguity X-008, missing two existing-test edits, ungrounded forecast) stand. I withhold a final view of C's rebuttal until it exists.

#### flg-r1 evidence: revised prediction and any in-theme lever

**What flg-r1 shows for B.** In flg-r1 review 3, all 4 blockers sit on text written by blocking fixes (R3-1 on R2-2, R3-2 on R2-3, R3-3 on R2-1, R3-4 on R2-1 and R2-4), and each review-2 blocker sits on text a round-1 blocking fix wrote. A blocking-only fix gate removes R3-7 (a MAJOR label graded minor, on a minor-only fix) and nothing else. That is B's F1 "wrong lever" case. B's round-1 guess of "about 5 and 2" fits this, but it was a judgement made without reading flg-r1 (my open question 12), so the match supports the replay method and not more.

**Revised B prediction for the S1 bar.**

| Quantity | B round 1 | B revised |
|---|---|---|
| flg-r1-like replicate, R3 critical+major proxy | about 5 (guess, flg-r1 unread) | 5 (4 blockers + R3-8's MAJOR label; R3-7 removed) |
| flg-r2-like replicate | about 2 | about 2 (replay: 5 to 2) |
| Mean over two fresh replicates | 3.5 | 3.5 (range 1.5 to 5.5) |
| P(both replicates 3 or fewer) | about 0.25 | about 0.2 |
| P(F1 fires in at least one replicate) | not stated | about 0.55 |
| Growth after 2 fix cycles (44.4% bar) | mean 23%, about 0.9 | same; flg-r1 Arm B is already at 27.8% and the gate drops minor-fix growth |

Reason for 0.2: the per-blocking-fix defect rate at fix 2 swings between runs (flg-r1: 4 blockers from 4 blocking fixes; flg-r2, as A and B both reported: about 1 from 6). With two fresh draws the bar passes only if both draw the low rate and land at 3 or fewer. Diffgate does not change that rate. S1 as written is therefore mostly a measurement of that rate under scope control, and I expect it to say "bar missed, F1 fires" about as often as it says "bar met".

**Two edits to B that follow.**
- F1 is re-based on the bar instead of a separate constant: F1 fires when the R3 proxy is above 3 and at least 70% of review-3 blocking findings sit on mapped fix hunks. The old "R3 of 5 or more" is brittle: remove R3-8 (a label graded minor) from flg-r1 and the proxy is 4, the mechanism is identical, and F1 would not fire.
- Report the label proxy (the bar) and the 427-blocking count side by side. In flg-r1, 2 of 6 proxy items (R3-7, R3-8) are MAJOR labels graded minor. That label noise of about 2 is large against a bar of 3.

**Is there an in-theme lever that acts on blocking-fix chains without relabelling or hiding?** I went through the four parts as A did and agree with A's verdict, with one correction to A's candidate.

- **Computed surface: no.** The four blockers sit on new words that blocking fixes wrote. Narrowing the surface further means not reviewing fix text, which is hiding. I also checked that the surface would have changed nothing for review 3: every SPEC3 line named in the origin column of all 10 review-3 findings falls in a changed-line list of `disposition-round2.md`.
- **Anchor checker: no.** Each blocker anchors on changed words and cites other lines as evidence. Rejecting those would be hiding.
- **Fix gate: no reduction.** All four parent fixes were mapped blocking fixes. A stricter gate (budget or footprint) only pushes revisers to under-fix, which moves a finding from new to open prior (A-003) and counts the same in the proxy.
- **Ledger: detection only.** It can flag, before fix 2, that a review-2 blocker sits on text a round-1 blocking fix wrote (recurrence), and it prints the chain. In flg-r1 this would have fired on all 4. Any rule that downgrades, defers or excludes recurrence blockers is relabelling and is ruled out. I withdraw B's halt-on-chain-length as a rule (see response to round2-A, item 3); it is a report line.

**A's candidate, the cross-reference closure aid** (the fix gate prints, for each reviser hunk, the unchanged lines sharing an identifier token with it). A estimated two of four flg-r1 blockers have that shape. I tested the line pairs the review names, counting WC/AC/SA/FR/D ids and `--flag` tokens on the spec:

| Blocker | Conflict pair | Result |
|---|---|---|
| R3-1 | SPEC3:67 and 188 | Share `WC-7`, but both lines were changed by the same fix (R2-2), so closure adds nothing the surface does not already show |
| R3-2 | `git status` behaviour | External fact; no identifier link |
| R3-3 | SPEC3:162 (changed) and 200 (unchanged) | Line 162 does not name `AC-1.2`, which appears only on line 200; they share `WC-4` and `P1`, and `WC-4` occurs on 14 lines, so the real hit would be one of 14 |
| R3-4 | SPEC3:64 and 66 | No shared identifier (64 carries `WC-4`, `WC-5`; 66 carries `WC-6`, `--retry-of`); the link is conceptual ("fresh dir" versus retry) |

Ceiling on flg-r1: no clean hit, one hit buried among 14 lines, out of four. The reviser had also already worked by root cause with explicit knock-on lists and still missed these. So the aid's expected effect is about 0 to 1 blockers, reached only if the reviser reads a noisy list. It would need its own ablation arm and must not count toward the diffgate result.

**Honest answer: no mechanism inside the diffgate theme lowers fix-induced blockers without relabelling or hiding real defects.** What the theme can legitimately do is make the result interpretable: print chains, report chain-length distribution, apply the re-based F1, report label and blocking counts, and apply C's spread check so a single swing of the rate (0.17 versus 1.0 at n=2) is not read as an effect. The lever F1 points to is fix quality, which is outside this theme. One consequence for delivery, in the refactorer's minimal-risk spirit: ship Stage A (inert script, tests, skill) on its own merits, since the self-computed diff, checked origin tags and checked counts do not depend on the bar; run Stage B as the experiment; gate Stage C (fold into `spec-panel.md`) on the pre-registered result classes (bar met; bar missed with F1; bar missed without F1), not on the bar alone. If the owner wants a decision-grade answer on convergence, a third replicate per arm buys more than any added machinery.

#### New evidence

1. **The scope gate would have changed none of flg-r1's review-3 findings.** I cross-checked each SPEC3 line in the origin column (67, 188, 183, 189, 88-90, 162, 64, 102-128, 70, 107, 93, 112) against the changed-line lists in `disposition-round2.md`: all fall inside changed lines. The computed surface would agree with the reviewers' own origin tags. For this run diffgate's value is verification of the tag, not a smaller count.
2. **The fix gate has very little to remove in flg-r1.** Lines touched only by minor rows in fix 2 are 62, 70, 107, 202 and 234, five of the 60 changed lines (60 per `disposition-round2.md` section 3; the blocking-row ranges such as 102-128 make this an approximate figure). The flg-r2 replay removed 3 of 5 review-3 items; flg-r1 removes 1 of 6.
3. **Closure-list ceiling measured** (table above): zero clean hits and one buried hit on four blockers.
4. **Label noise.** Two of six proxy items (R3-7, R3-8) are MAJOR labels that 427 graded minor.
5. **Revisers already produce a fix map.** The flg-r1 reviser tagged every changed passage with `R2-N` (except a pure reorder) and listed knock-on edits per row. An explicit map is a by-product; pre-filling it from inline tags makes B's map nearly free.
6. **Variance between replicates is large.** flg-r1 fix 2: 4 of 4 blocking fixes produced a blocker. I verified this one; the 1-of-6 flg-r2 figure is A's and B's round-1 number and I did not re-read flg-r2 this round. At n=2 the within-arm spread swallows any plausible effect, so C's spread check should be part of the pre-registered pass rule.
7. **Test addition.** Add an flg-r1-shaped fixture to `tests/skills/fixtures/diffgate/`: four mapped blocking fixes, four new blockers on those hunks, one MAJOR label graded minor on a shared line, one minor-only line. Expected outputs: the gate allows all four fix hunks and drops the minor-only line, chains of length 3 print, F1 fires, label proxy 5 and blocking count 4. This pins the very case this round turned up, at no model cost.

#### Shared assumptions (A-001..A-006: ACCEPT|REJECT|QUALIFY: one-line reason, updated)

- A-001: QUALIFY: one scripted command per exit code leaves little to improvise, but compliance is assumed; record recovery-path compliance per replicate as a validity input.
- A-002: QUALIFY: flg-r1 shows narrowing removes noise (R3-7) but not blockers (10 of 10 findings were already on changed text); record hunks per surface and findings per hunk before attributing any gain to density.
- A-003: QUALIFY: all four flg-r1 parent fixes were mapped, so under-fixing was not the issue there, but a stricter gate can only move counts from new to open prior; report open priors and `declined` lines apart from new findings.
- A-004: REJECT: the added brief lines and the `fixcheck` line are prose that can change reviser behaviour without the script; claim the combined treatment or add a briefs-only arm.
- A-005: QUALIFY: B's one-line grammar (now with JSON-quoted anchors and no verdict line) is a smaller review-1 tax than before; check review-1 blocker counts against Arm B's 13 to 17 as a validity gate.
- A-006: REJECT: now answered by evidence; flg-r2 composition does not hold for flg-r1 (all 4 blockers sit on blocking-fix chains), so any forecast resting on flg-r2 alone is unsupported.

#### Per-point positions (updated)

| Point | Superior approach (A, B, C, merge like A+B, or tie) | One-line reason |
|---|---|---|
| S-001 | C | Separate test and acceptance sections; all three advocates now prefer C or call it a tie. |
| S-002 | C | Tiered P0/P1 tests with negative cases are easiest to run; fold A's 16 script cases and the flg-r1-shaped fixture into them. |
| S-003 | C | Implementation acceptance apart from experiment success; move C's criterion 15 to the experiment gate. |
| S-004 | A+C | A's nine verbatim bullets as single physical lines, plus C's removal of the line-220 read as a tenth listed change. |
| S-005 | A+B | A's signatures fix the interfaces; B's named constants and per-part line budget bound the size (with B's cut constants gone). |
| S-006 | A+B | One exit table with a who-acts column; all three advocates accept it. |
| S-007 | B+C | flg-r1 showed dense citations did not protect a causal story; UNVERIFIED tags, a replay and PROPOSED labels are the better discipline. |
| S-008 | A+B | A's bullet-keyed residual-risk table plus B's extra concerns such as step order. |
| S-009 | A+C | A's residual column plus C's separate cost envelope. |
| S-010 | B+C | B flags experiment blockers; C gives every question a default. |
| C-001 | A+B | The worker that owns each step runs it, `begin` re-runs the fix gate, the coordinator only reads `status`; C's confirmation checks presence, not truth. |
| C-002 | A | The verified installer analysis decides the name (`sc-diffgate`, called by path); add C's transcript check of that call. |
| C-003 | A+B | B's four-subcommand set (`final` folded into `close`/`check`) with A's rule that `begin` re-runs the gate. |
| C-004 | A+C | One JSON object per call with separate verdict and execution-success fields is easier to test; I withdraw the key:value preference. |
| C-005 | B+C | One meaning per code in B's table, plus C's rule that a valid FAIL exits 0. |
| C-006 | A+B | A's JSON-quoted values (no `[[ ]]` limit) carrying B's `via=`, `cites=`, `declined` fields; C's strict JSON draft is the largest review-1 change. |
| C-007 | tie | File layout does not change behaviour; flat files are smaller, per-round folders are tidier. |
| C-008 | A+B | Token-level eligibility (A) with block-level hunk ids for ownership (B); no `renumber` rule needed. |
| C-009 | A | `H<k>.<n>` never repeats across reviews and is shared by the gate and the next surface; a digest adds nothing the ledger hash lacks. |
| C-010 | A+C | A's token-overlap rule C5 plus C's validation of every claimed anchor; B's hard versus soft split stays. |
| C-011 | A+B+C | Demote or degrade anchor failures, stop only on structure, never print a clean PASS when blocking-grade findings were degraded or deferred. |
| C-012 | A+B | An unanchored finding is a free deferral; C's reject spends the one repair on a legal outcome. |
| C-013 | B | Quote-checked `via=`; over-cap findings deferred but counted in the proxy and shown in the scoped-PASS line (this answers C's worry). |
| C-014 | B | Explicit map with `declined`, pre-filled from inline tags; footprints would not have stopped flg-r1's chains (R2-2 and R2-3 were 3-line fixes). |
| C-015 | A+B | Report `bytes_by_id` and hunks per id, no gate and no threshold; I drop B's budget. |
| C-016 | tie | All three reject a severity ceiling; flg-r1 makes it the obvious relabelling trap. |
| C-017 | B+C | B's `seen: rounds 2,3` and the no-cite rule for deferred ids, plus C's scoped-PASS sentence. |
| C-018 | A+C | The reviewer writes no verdict and the script supplies it; B now agrees. |
| C-019 | A | Presence of an outcome, no paddable constant; C's confirmation is presence-only by C's own words and adds a coordinator step. |
| C-020 | A | No severity field on carried status lines makes upward drift impossible by grammar. |
| C-021 | tie | All three keep minors away from the reviser; in flg-r1 this removes only R3-7. |
| C-022 | A+B | A word-identical reflow is not a hunk; B's `coverage:` warning flags a degenerate surface. |
| C-023 | B | flg-r1 bears out a bar miss: 4 of 4 review-3 blockers sit on blocking fixes; A withdrew its 60%. |
| C-024 | tie | All forecasts clear 44.4%; flg-r1 Arm B is already at 27.8%. |
| C-025 | A+B+C | B's F1 re-based on the bar as the primary diagnosis, A's blindness and demotion conditions, C's spread check. |
| C-026 | A+B | The all-discovered count by reviewer label gates the bar; C concedes. |
| C-027 | C | The most complete accounting (Read-backs, correction turns); A and B estimates omit some of it. |
| C-028 | A+B+C | A's hash of the untouched `spec-panel.md` and no `--force`, B's `--expect-round`, C's installed-file hashes and transcript check. |
| C-029 | B | Dropping the 427 flags from the variant's Usage is simplest; ignoring (A) keeps dead text and verifying (C) adds code. |
| C-030 | A+B+C | A's two existing-test edits, B's fixtures and drift guard (with the `## Tool Coordination` exemption), C's isolated-HOME install test. |
| C-031 | A+B | Verbatim `## Unattended mode` with the name swapped stays pinnable against the parent; registered through A's `UNATTENDED_VARIANTS`. |
| C-032 | A+B | No plugin mirror is needed (parity test pins only README-listed commands); a separate design note keeps 427's doc historical. |
| C-033 | A | A fresh-review blindness audit, misses classified by ledger history; all three now agree. |
| C-034 | A+C | A's `PROFILES` seam toward rf-qa, with C's limits on replacing the `/sc:implement` FINAL review or weakening rf-qa guards. |
| C-035 | A+C | A's ledger replay plus C's exclusive-create lock; size limits and symlink refusal are cut as over-scope. |
| X-001 | A+B | Worker-run steps with mutual locks; the coordinator is also a prose follower. |
| X-002 | A+B+C | Same as C-011: stop only on structure, degrade the rest, no clean PASS with degraded blocking-grade findings. |
| X-003 | A+B | A word-identical reflow carries nothing to review; edited words inside it still surface. |
| X-004 | A+B | Same as C-012. |
| X-005 | B | `via=` covers the case it exists for; flg-r1 had 0 of 10 findings needing it, so it is a narrow escape, not a driver. |
| X-006 | A+C | Same as C-018. |
| X-007 | B | flg-r1 supports about 0.2 for both replicates meeting the bar; A's revised forecast now matches. |
| X-008 | A+B | Same as C-026; deferred and degraded findings count by label. |
| X-009 | A+B | Whitespace-only edits are not hunks and need no owner; C's rule contradicts its own mask. |
| X-010 | B | Same as C-029. |
| X-011 | A+B | The parity test pins only README-listed commands, so a mirror is unneeded scope. |
| X-012 | A | Only A plans the `_POST_REFRESH_ADDITIONS` edit; B and C concede. |
| X-013 | A+B | No gate, bytes reported only; flg-r1's 3-line fixes show a size gate would not have helped. |
| X-014 | A+B | A name that does not match the command, called by path; C's Skill activation is a legitimate alternative, not an error. |
| X-015 | C | A concedes; remove the line-220 read. |
| X-016 | C | Same fix; B's drift guard exempts `## Tool Coordination`. |
| X-017 | A | Register the variant through `UNATTENDED_VARIANTS`; a verbatim section keeps parity with the parent. |
| X-018 | tie | B conceded the 13 versus 14 slip; it has no design effect. |

### Variant C Rebuttal (file debate/round2-C.md)

#### Response to criticisms

C withdraws its R3 mean 1.5 forecast. The strongest common design is now a smaller A+B mechanism with C's acceptance tests and honest failure reporting, not C unchanged. Mechanical enforcement, semantic review and experimental success are separate properties. None implies the others.

Evidence key: R1-A, R1-B, R1-C, R2-A and R2-B mean the corresponding debate statements. C means variant-3-haiku-qa.md. E means evidence-flg-r1.md, the verified orchestrator note. Proposal descriptions and reported replays are not executed treatment results. I also directly read the flg-r1 disposition's method and table and the review-3 numbered findings. No helper implementation or live treatment was tested in this round.

### Criticisms in round1-A.md

1. **A-R1-1, incompatible regression promises, X-012 and X-017. Concede.** C forbids integration changes that its own acceptance criteria require. Adopt A's explicit registration of the added command in the inventory and unattended checks. Preserve the original command's assertions; add variant assertions rather than weakening shared checks. C's Round 1 concession remains binding.

2. **A-R1-2, all transitions rely on the coordinator, C-001 and X-001. Concede placement, qualify judgment.** Worker-owned calls with the next step rechecking the preceding gate are a better normal execution path. Coordinator confirmation checks a different property, a second reading of a semantic claim, but does not make invocation unavoidable. Require transcript and ledger agreement whatever actor runs the helper. Do not require a coordinator confirmation file for every finding in the S1 arm.

3. **A-R1-3, second rejection discards the review, C-011 and X-002. Partly concede.** One repair followed by invalid termination is too costly for a merely unanchored observation. Accept normal deferral for a parseable unanchored claim, keep accepted blockers, and default missing prior statuses to open. Retain a hard stop for unreadable structure, inconsistent history or a verdict that cannot be derived without inventing records. An invalid attempt must remain in experiment accounting, not disappear into a replacement replicate.

4. **A-R1-4, whitespace ownership contradicts eligibility and reflow inflates scope, X-003 and X-009. Reject the alleged logical contradiction; concede the precision cost.** Authorization asks whether an edit was permitted; eligibility asks whether a new finding may block on it. Those are different masks. A raw whitespace edit can require authorization without opening new blocking scope. C nevertheless inherits a real whitespace-blindness risk. Adopt A's token precision for substantive edits, but do not assume every word-identical Markdown change is harmless. The list-collapse case in New evidence needs a policy before filtering physical boundaries.

5. **A-R1-5, ambiguous bar count, X-008. Concede.** The bar uses the all-discovered critical+major proxy, including deferred and degraded proposed labels, with distinct findings counted once. Effective blocking is a separate diagnostic. Neither a scoped PASS nor confirmation-based regrading may replace the primary count.

6. **A-R1-6, replacement command text is not verbatim, S-004. Concede.** Use A's literal replacement-bullet format, with every intended change listed, including C's portability correction. An implementer must not have to invent precedence or recovery wording from a prose summary.

7. **A-R1-7, experiment-arm weight, mirrors and Skill activation. Mostly concede.** Drop plugin mirrors and the historical-design annex from this experiment. Use a separate design note and test the selected source-install surface. A by-path helper call does not need an additional protocol Skill call merely to run Python. Where the command requires Skill activation, observed invocation still matters. Keep isolated-install, output-collision, persistence and boundary tests. The 5-13 minute cost was an estimate to measure, not evidence that the work is justified.

### Criticisms in round1-B.md

1. **B-R1-1, the coordinator is the same actor that dropped the old flags. Concede.** Worker-run steps, mutual gate checks and an expected-round check reduce that failure opportunity better than C's coordinator-only chain. They remain cooperative enforcement, not a permission boundary.

2. **B-R1-2, a handwritten confirmation file decides the verdict. Partly concede.** C explicitly names that residual risk, so it does not conceal a prose dependency. A second reader can disagree with a reviewer; that is more than checking an outcome string. But the script proves only that a decision exists and matches its inputs. Its truth is not mechanical, and its benefit has not been measured. Leave mandatory per-finding confirmation out of the minimal S1 treatment rather than credit it with convergence.

3. **B-R1-3, R1 format tax threatens comparability. Concede.** Strict JSON, footprints and confirmation alter elicitation most when the first review has many findings. Prefer A's JSON-quoted machine records without a reviewer verdict. Still check R1 labels, counts, formatting failures and cost against the historical arm. Equal full-document eligibility does not establish an unchanged baseline.

4. **B-R1-4, two existing tests fail while C forbids fixing them. Concede.** This repeats A-R1-1 and needs the same explicit integration changes. A found both breaks; C did not.

5. **B-R1-5, scope creep and inaccurate plugin description. Mostly concede.** C's one-word-drift description was wrong, and mirrors are not required for this experiment. Remove mirror delivery, parity work and the annex. Retain a small lock, digest checks, collision checks and failure-injection tests because the helper writes authority-bearing state. Size and symlink defenses are boundary hardening, not evidence of better convergence; they must not be used to sell the S1 hypothesis.

6. **B-R1-6, unanchored findings consume the repair allowance, X-004. Concede.** Ordinary unanchored observations should go directly to the deferred list without a whole-report repair. A false exact quote, stale id or corrupted state is different and still needs explicit diagnostics. Test both cases rather than treating every anchor failure alike.

7. **B-R1-7, reflow expands scope and the metric is ambiguous. Concede the metric and paragraph granularity; qualify reflow.** Use the all-discovered proxy and token-level eligibility within changed text. A blanket token-equality filter also hides structural Markdown changes, so the claimed superiority of filtering every reflow is too broad. A declared S1 plain-prose policy is narrower than general document correctness.

8. **B-R1-8, footprints can prevent legitimate repairs and lack a declined outlet. Concede.** Adopt B's explicit map and declined records, with unresolved priors remaining counted. Pre-approved footprints prevent distant id laundering but can reject correct coupled edits or force broad authorizations. Their rejection rate and semantic benefit are unmeasured. Do not include them as a required S1 convergence lever. The overlapping-owner case in New evidence strengthens the case against C's coarse single-owner groups.

9. **B-R1-9, optimistic forecast plus many validity exclusions. Concede.** Mean 1.5 is withdrawn. Invalid runs are observed failures to complete the treatment, not low-count outcomes. Pre-register the attempted replicate slots and publish failures and costs; no quiet replacement of inconvenient invalid runs. See the revised forecast below.

### Criticisms and defenses in round2-A.md

1. **A-R2-C1, ending on expected anchor errors wastes otherwise useful evidence. Accept the revised graded recovery, with a stronger acceptance label.** Keep recoverable records and defer the bad anchor after the allowed repair, but a qualified PASS must not satisfy an early clean-PASS success criterion. A's proposed line beginning with PASS and a qualification is better disclosure than a bare PASS, yet downstream readers can still misread it. Expose a machine-readable degraded or incomplete-acceptance status as well as the scoped verdict.

2. **A-R2-C2, footprints would contain the legitimate flg-r1 fixes and stop neither small chain. Concede the convergence claim.** The disposition shows R2-2 and R2-3 are genuine small repairs, not unrelated edits carrying borrowed ids. A footprint does not establish the repaired rule's correctness. It remains a stronger defense against distant laundering, but that failure is not demonstrated as the cause of this replicate's count. Keep it out of the minimal S1 arm.

3. **A-R2-C3, confirmation does not determine semantic truth and replay is cheaper. Qualify.** Replay and second-reader confirmation serve different purposes. Replay detects inconsistency; a coordinator may notice a mistaken causal claim. The statement that confirmation checks presence, not truth is a limit on the script, not proof that the parent does no useful reading. However, neither reading nor the evidence supplied establishes that this extra pass would have prevented any flg-r1 child. Do not assign it a numerical benefit.

4. **A-R2-C4, portability copy contradiction now resolved. Accept.** A's named removal and B's corresponding drift-guard exception incorporate C's correction. C no longer claims this as an unresolved A defect.

5. **A-R2-C5, token precision cannot remove genuine blocking-fix children. Concede.** Every actual flg-r1 blocker remains reviewable. Token precision reduces anchor slack and review cost, not the number of these defects.

6. **A-R2 assessment, C's strongest guards target unshown failures. Mostly accept for S1, reject as a general dismissal of integrity tests.** Footprints and semantic confirmations have no demonstrated convergence return here. Malformed input, stale state and output collisions are still normal test surfaces for a stateful helper. Cheap negative tests do not require a paid replicate to fail first. Reduce runtime duties without dropping the tests that prove accepted records were actually checked.

7. **A-R2 lever claim, any stricter gate can only move new blockers to open priors. Qualify the universal claim.** Rejecting an unrelated edit can prevent a genuine new defect, so that is not a theorem about every input. It is the correct prediction for these legitimate blocking fixes: no evidence says containment would repair them. I accept A's four-part no-demonstrated-lever conclusion for flg-r1 and do not count its proposed cross-reference aid as part of diffgate.

8. **A-R2 table positions, activation, reuse and minimal state. Accept the smaller path with limits.** A's installer-compatible by-path design is legitimate; C's longer protocol name was also installer-compatible. A small severity-profile seam does not require a generic plugin framework, so C's non-goal need not forbid it. Adopt replay plus locking, retain boundary tests, and do not replace the broader FINAL or rf-qa rules with a scoped checker.

### Criticisms and defenses in round2-B.md

1. **B-R2 assessment, invalid termination is especially costly at n=2. Concede the cost; reject mistyped-anchor equals automatic lost replicate under the revised merge.** C's original policy allowed one repair, so one typo alone did not discard a replicate. Still, twice-invalid output should not be the default outcome for an ordinary scope error. The graded recovery above preserves evidence while structural failure remains an explicit failed attempt.

2. **B-R2-C4, laundering is unobserved and footprints would not change the small chains. Accept for the experiment.** Footprints should not be presented as the missing convergence mechanism. B's proposed later trigger, no word overlap with a quote, is only an audit signal: a legitimate coupled repair can lack that overlap, and laundering can occur within the quoted paragraph. Retain that limitation if hardening is deferred.

3. **B-R2-C3, over-cap via claims are deferred, counted and disclosed. Partial improvement, not full resolution.** This answers the metric-hiding objection but not the acceptance objection: a third genuine dependency-caused blocker may still leave the effective blocking set solely because it is third. Prefer B's explicit changed-cause dependency evidence without an arbitrary discovery quota. If the quota stays for S1, over-cap severe claims must prevent an unqualified acceptance and an early clean-PASS credit.

4. **B-R2-A7 and C-035, size and symlink defenses are over-scope. Partly concede.** No evidence makes the particular numerical limits necessary to S1 convergence. A lock alone is also not protection against output aliasing the specification or a partial write being accepted. Keep digest, alias and persistence tests; keep the helper from writing the target; treat resource limits as a declared input envelope, not a measured quality gain. Do not add a broad security framework.

5. **B-R2 assessment, none of C's guards would change the count. Accept the mechanical reading, qualify the counterfactual.** Containment and presence checks do not remove these valid blockers. A second semantic reader might notice a defect, but that possibility is not measured evidence and warrants no lower forecast. C's mandatory confirmation would also change the treatment, cost and R1 baseline, so it cannot be treated as a free extra gate.

6. **B-R2 delivery claim, Stage C can depend on result classes rather than the bar alone. Reject automatic promotion on a diagnostic failure.** A bar miss with F1 can justify retaining an experimental verifier by explicit owner decision. It does not satisfy the pre-registered convergence goal or authorize folding the variant into the original command. A third replicate could improve estimation, but it is a separate experiment decision, not a post-hoc addition to S1.

7. **B-R2 defenses on eligibility and format. Accept the actual improvements.** Token eligibility with context excluded, old-side deletion evidence, no reviewer verdict, removal of padding and byte thresholds, replay and locking address real Round 1 objections. B is materially stronger after those changes. Its claim that block-level ids remove the renumbering problem is incomplete: an effective renumber-only block still needs a legal owner or a declared cosmetic-edit exception. Grouping reduces map entries, not that authorization obligation.

#### Updated assessment of A and B

**A is the best implementation base after its concessions.** Keep its installer analysis, literal command changes, test integration, JSON-quoted records, token-overlap eligibility, carried-status grammar and replay. It now accepts an explicit map, no DG-COVER, the portability correction and a much lower success forecast. Remaining tests must cover token filtering of structural Markdown, a renumber-only edit without an open blocker, and degraded output that must not become early clean PASS. Its revised probability is a judgment, not a fitted estimate from two observations.

**B supplies the best experiment diagnosis and several operating details.** Keep explicit maps with declined reasons, expected-round checks, fix-chain reporting, staged delivery, the all-discovered proxy, and F1 rebased to proxy above 3 rather than at least 5. Its revised eligibility, deletion handling and verdict ownership answer my strongest parser and scope criticisms. The remaining via quota is arbitrary, and partial degradation needs a distinct acceptance status. Its new flg-r1-shaped fixture is useful, but an actual treatment replay must recompute text and ownership rather than hardcode five as a universal answer.

**Merge position.** Use A's formal checker and integration work, B's explicit mapping and observable experiment, and C's tiered negative tests, installation test, scoped-acceptance warning, separate acceptance gates and cost accounting. Remove C's mandatory per-finding coordinator duties, plugin mirrors and pre-approved footprints from the minimal S1 arm. Retain raw-edit accounting and state-integrity tests. None of this establishes that the convergence bar will pass.

#### flg-r1 evidence: revised prediction and any in-theme lever

### What the evidence establishes

E resolves A-006 against the shared extrapolation. Four R3 blocking findings sit on legitimate blocking fixes, and their R2 parents themselves arose from blocking fixes. R3-7 is the one severe-label item attributed only to a minor fix. R3-8 is severe-labelled but graded minor and shares a line touched by blocking and minor repairs. The current review has label proxy 6 and effective blocking 4. A blocking-only repair gate has no demonstrated way to remove any of those four real blockers.

The usual retrospective estimate is therefore proxy about 5 after removing R3-7. Line ancestry is not a replay of the revised document, so R3-8's exact survival under removal of the minor edit is uncertain. Even if that fifth item disappears, four blockers still exceed the bar of three. This is enough to withdraw C's 1 and 2 forecast without pretending to know a counterfactual review exactly.

### Revised prediction

| Quantity | Revised C position |
|---|---|
| flg-r1-like valid replicate | R3 proxy about 4-5, central 5; four genuine blockers remain in scope |
| flg-r2-like valid replicate | About 1-2, central 2, based on the reported replay rather than a new treatment run |
| Two-replicate mean | Central 3.5; plausible paired range 2.5-3.5 for those two historical shapes, not a confidence interval for fresh runs |
| Both replicates at 3 or fewer | Unlikely; about 0.2 as an explicitly uncalibrated planning judgment, no more optimistic than revised B |
| Original C completed-success probability | No higher than that planning judgment because stricter invalidation and footprint duties add completion failures |
| Growth | Retain C's provisional central 27%, roughly 24-30%, below 44.4%; no measured treatment growth and no credit for an invalid or stalled run |
| Whole S1 bar | Predict a miss on convergence, with growth more likely to pass; do not multiply invented independent probabilities |

The central mean alone is insufficient: S1 requires both replicates to meet the count threshold. A low flg-r2-like result does not offset a flg-r1-like failure. Invalid or halted-before-R3 attempts have no measured R3 value; record them as unsuccessful attempts, never as zero. C's spread check remains a separate evidence-strength check, not a significance test or an excuse to change primary thresholds.

### In-theme lever and the C-specific counterfactual

1. **Computed surface.** Agree with A and B: the four blockers remain on fix-written text. Removing that text from eligibility would hide the defects. Token precision can tighten evidence and save reading, but does not repair the rules.

2. **Anchor checker.** Agree for this case: the claims have changed causes and concrete consequences. A valid membership checker should admit them. A bad quote must be repaired; a real harmful consequence must not be converted into a lower count because of format.

3. **Fix gate and pre-approved footprints.** Agree that C has no demonstrated preventive effect here. R2-2 and R2-3 are small legitimate repairs. The other parents contain justified coupled edits. A footprint narrow enough to reject a necessary coupled repair can instead leave an old blocker open, which still counts. Footprints are an authorization defense, not a fix-correctness oracle. The shared-line ownership complication makes C's original gate more likely to stall, not more likely to pass honestly.

4. **Ledger.** Agree that chains are detection and diagnosis, not prevention. Record multiple parent links when evidence supports them, recurring regions, open priors, declined fixes and new blockers separately. Accept B's threshold-based F1. Do not halt early on chain length to manufacture a low R3 count, demote a recurring blocker, or add a third fix.

5. **Coordinator confirmation.** A and B are right about the missing demonstrated benefit, but too categorical if they mean a second reader could never notice the defect. C asks the parent to judge the current wrong outcome and evidence for resolving a prior finding; it does not require a complete adversarial review of every proposed repair against all dependencies and external behavior. R3-2 requires knowledge about ignored-path coverage, while R3-3 and R3-4 require acceptance-set and retry-lifetime reasoning. C does not mechanically perform those checks. No evidence shows its confirmation would have caught even one, and S1's count bar would require preventing enough of them without replacing them with open priors. Give confirmation zero forecast benefit unless separately tested.

6. **Proposed aids.** A's identifier-linked context aid is not a proven gate. B's reported pair inspection limits its useful reach and shows conceptual links can lack shared identifiers. Adding semantic cross-reference checks, a second repair reviewer or targeted ignored-path tests could address fix quality, but would be an additional treatment, not a result of the four mechanical parts alone.

**Conclusion:** no demonstrated in-theme lever prevents flg-r1's blocking-fix chains without hiding valid findings or changing the treatment. C cannot honestly predict S1 success from coordinator confirmation or footprint containment. The defensible gain is enforceable scope and interpretable failures, not guaranteed convergence.

#### New evidence

1. **Direct source confirmation, not a new experiment.** I read flg-r1's disposition method and table and its review-3 numbered findings in this round. They confirm that the reviser already checked source claims, tested part of the git-status behavior, followed the review's recommended pass condition for R2-2, and listed knock-on edits. The later defects are not explained simply by failing to map a repair or failing to read the original finding. These reads support the supplied evidence note rather than adding a new replicate.

2. **New test implication: token equality can erase Markdown structure.** Compare `1. First\n2. Second\n` with `1. First 2. Second\n`. A whitespace-split token stream is identical, yet two list items become one. This is a derived negative fixture, not an executed parser test. It challenges unconditional reflow suppression, not token precision within substantive edits. Acceptance must state whether such structural changes remain visible and what authorization they require.

3. **New test implication: unique coarse ownership is too restrictive.** E attributes R3-4 to R2-1 and R2-4, which both touch the same paragraph line. C derives one parent from one zero-context edit-group owner and rejects mixed-owner groups. Line ancestry alone does not prove the exact token allocation, but supplies a realistic fixture shape: two legitimate blockers repaired in one paragraph, followed by a child depending on both. Test either nonoverlapping token-owned groups or explicit complete multi-owner coverage and plural parent links. Do not fabricate a unique causal parent just to satisfy the schema.

4. **New acceptance implication: proxy preservation and release acceptance are different safeguards.** A third genuine via claim deferred by a quota still counts toward the proxy, so the experiment cannot win by that deferral. It can nevertheless be absent from effective blocking. Test that degraded or quota-limited acceptance cannot satisfy early clean PASS, even when the current-round label count happens to be three or fewer. A qualified text line alone is not a machine-readable assurance boundary.

5. **New accounting implication: invalid replacements select for easy runs.** C's old validity list creates more opportunities to terminate before the endpoint. Quietly rerunning invalid slots until two complete changes the population being compared. Freeze attempted slots, record completion rate and cost, and require a separately declared rerun decision. This is a design inference, not evidence that any advocate has actually replaced a replicate.

#### Shared assumptions (A-001..A-006: ACCEPT|REJECT|QUALIFY: one-line reason, updated)

- A-001: QUALIFY: exits do not prove recovery compliance; require transcript and ledger agreement, reset probes and explicit failed-attempt accounting.
- A-002: REJECT: flg-r1 leaves all four blockers on blocking-fix text, so smaller scope is not a justified predictor of fewer blockers; record density and blind-audit results.
- A-003: QUALIFY: blocking-only maps remove gratuitous edits but may under-fix or stall; count open priors, declined repairs and legitimate authorization rejections separately.
- A-004: REJECT: brief changes and helper enforcement are a combined treatment unless a briefs-only comparison isolates them.
- A-005: QUALIFY: machine records alter R1 elicitation, especially under original C; compare counts, labels, formatting failures and cost rather than assuming a shared baseline.
- A-006: REJECT: verified flg-r1 ancestry contradicts extrapolating the flg-r2 minor-fix story to both replicates.

#### Per-point positions (updated)

| Point | Superior approach (A, B, C, merge like A+B, or tie) | One-line reason |
|---|---|---|
| S-001 | C | Separate test and acceptance sections expose obligations without making the forecast an implementation criterion. |
| S-002 | C | Retain tiered negative tests and add the flg-r1-shaped chain and structural Markdown cases. |
| S-003 | C | Split implementation acceptance, experiment completion and the convergence bar; move criterion 15 out of implementation acceptance. |
| S-004 | A+C | Use A's literal bullets with C's portability correction named as an allowed extra change. |
| S-005 | A+B | Concrete signatures and a bounded outline are clearer than C's prose-only outline. |
| S-006 | A+B | One exit table with the actor and next action makes recovery testable. |
| S-007 | B+C | Replays and explicit unverified or proposed labels separate evidence from a plausible story. |
| S-008 | A+B | Combine literal-bullet traceability with additional ordering and state concerns. |
| S-009 | A+C | A's residual-risk mapping and C's full cost envelope cover different failure costs. |
| S-010 | B+C | Setup blockers need explicit resolution, and remaining questions need declared defaults. |
| C-001 | A+B | Worker-owned calls with mutual gate checks reduce coordinator-only sequencing duties. |
| C-002 | A | A's installer-compatible by-path helper is smaller; retain isolated discovery and observed invocation checks. |
| C-003 | A+B | Use a small command set while making the next review rerun the preceding fix gate. |
| C-004 | A+C | One structured stdout object must separate operation success, verdict and degraded acceptance. |
| C-005 | B+C | Use B's actor-action table and C's distinction between valid audit FAIL and execution failure. |
| C-006 | A+B | JSON-quoted machine records with explicit map fields impose less R1 change than C's full draft and confirmation pair. |
| C-007 | tie | Flat or per-round layout is secondary to immutable inputs, digest checks and tested atomic transitions. |
| C-008 | A+B+C | Token eligibility, block-level map grouping and strict context exclusion need old-side deletion and structural-boundary tests. |
| C-009 | A+B | Round-qualified ids bound through ledger hashes can be shared between fix checking and the next surface. |
| C-010 | A+C | Validate token overlap and every claimed anchor, including repeated-text occurrences and old/new side. |
| C-011 | A+B+C | Defer recoverable scope errors, stop on structural uncertainty and never credit degraded output as clean acceptance. |
| C-012 | A+B | A parseable unanchored observation is an ordinary deferral, not a whole-report repair. |
| C-013 | B+C | Keep B's explicit changed-cause dependency evidence without a quota that suppresses a genuine third blocker. |
| C-014 | B | Explicit maps with declined reasons are sufficient for S1; footprints add unmeasured containment cost and stall risk. |
| C-015 | A+B | Report bytes and hunks per owner without an arbitrary size gate or advisory threshold. |
| C-016 | tie | All correctly refuse to relabel genuine last-round defects to force convergence. |
| C-017 | B+C | Keep deferred history and no-fix authorization, disclose scope limits, and preserve invalid-run diagnostics. |
| C-018 | A+C | Only checked helper output supplies the authoritative verdict; the reviewer writes none. |
| C-019 | A | Outcome presence is mechanically checkable; mandatory coordinator confirmation has no demonstrated S1 benefit. |
| C-020 | A+C | Omit severity from carried statuses and test immutable identity plus legitimate changed-text regression. |
| C-021 | tie | Only blockers authorize substantive repairs; minor-only fixes must not silently become treatment work. |
| C-022 | A+C | Keep token precision and raw-edit accounting without silently erasing structural Markdown changes. |
| C-023 | B | B's cautious forecast and surviving-blocker analysis replace C's unsupported mean 1.5. |
| C-024 | B+C | Growth forecasts are provisional and must include completion and stall accounting, not merely smaller output. |
| C-025 | A+B+C | Combine threshold-based F1, blindness and degradation checks, integrity checks and the separate spread screen. |
| C-026 | A+B | All-discovered critical+major labels gate the bar; effective blocking is reported separately. |
| C-027 | C | Cost includes confirmation, map work, correction turns and failed attempts rather than script runtime alone. |
| C-028 | A+B+C | Pin original and installed files, expected round, state identity and observed command/helper invocation. |
| C-029 | B | Remove obsolete predecessor flags from the new interface and reject unsupported use rather than silently ignoring it. |
| C-030 | A+B+C | Combine A's integration edits, B's allowed-change drift guard and fixtures, and C's isolated-install and negative tests. |
| C-031 | A+B+C | Reuse pinned unattended text where possible, but explicitly test execution failure and prohibit unchecked report publication. |
| C-032 | A+B | Source-only experimental delivery and a separate design note avoid unnecessary mirrors and historical-doc edits. |
| C-033 | A | A mandatory fresh blindness audit classified by text history reveals defects absent from every draft. |
| C-034 | A+C | A small profile seam is acceptable, but scoped review must not replace full FINAL or weaken rf-qa rules. |
| C-035 | A+C | Replay, locking and boundary/persistence tests protect state without claiming a sandbox or convergence benefit. |
| X-001 | A+B | Put routine calls on the acting worker and verify the preceding gate at the next transition. |
| X-002 | A+B+C | Preserve recoverable findings, stop when structure is unknowable and distinguish degraded acceptance from clean PASS. |
| X-003 | A+C | Token-equivalent plain rewrap and structural Markdown changes cannot safely share an unconditional exclusion rule. |
| X-004 | A+B | Ordinary unanchored observations should be deferred without spending the report-repair allowance. |
| X-005 | B+C | Explicit dependency evidence is useful, but an arbitrary via quota must not remove a real blocker from acceptance. |
| X-006 | A+C | The reviewer writes no authoritative verdict; the helper derives and publishes it. |
| X-007 | B | The flg-r1 evidence supports likely failure of the both-replicates bar, not C's original optimistic extrapolation. |
| X-008 | A+B | Deferred and degraded proposed severe labels stay in the primary all-discovered metric. |
| X-009 | C | Raw edit authorization and new-finding eligibility are distinct; ignoring whitespace for one does not authorize unlimited edits. |
| X-010 | B | A smaller declared interface is preferable to keeping unused predecessor flags and their verification logic. |
| X-011 | A+B | No universal mirror requirement was established for this source-install experiment. |
| X-012 | A | Explicit inventory accommodation is required; C's prohibition on that edit was wrong. |
| X-013 | A+B | Report sizes without gating; small legitimate fixes in flg-r1 still created blockers. |
| X-014 | A+B | By-path helper invocation is legitimate; preserve Skill evidence only where activation is actually required. |
| X-015 | C | Remove the copied repository-only example lookup as an explicit change. |
| X-016 | B+C | Apply the portability correction through a precise allowed drift-guard transformation. |
| X-017 | A+C | Register the variant without weakening original unattended assertions, then test its actual failure semantics. |
| X-018 | tie | B corrected the replay count; use recomputed fixtures rather than defend the obsolete exact ratio. |

## Round 3: Final Arguments

Skipped: depth=standard.

## Shared Assumption Responses (final, Round 2)

| A-NNN | A | B | C | Majority |
|---|---|---|---|---|
| A-001 | QUALIFY | QUALIFY | QUALIFY | QUALIFY (agreed) |
| A-002 | QUALIFY | QUALIFY | REJECT | QUALIFY (agreed) |
| A-003 | QUALIFY | QUALIFY | QUALIFY | QUALIFY (agreed) |
| A-004 | REJECT | REJECT | REJECT | REJECT (agreed) |
| A-005 | QUALIFY | QUALIFY | QUALIFY | QUALIFY (agreed) |
| A-006 | REJECT | REJECT | REJECT | REJECT (agreed; answered by debate/evidence-flg-r1.md) |
No omissions: every advocate addressed A-001 to A-006 in both rounds.

## Scoring Matrix

Winner = the position named by all three (95%) or by two of three (75%) Round 2 advocates; 'unresolved' = no majority (50%).

| Diff Point | Winner | Confidence | Evidence Summary (Round 2 positions) |
|------------|--------|------------|-----------------|
| C-001 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| C-002 | A | 95% | A: A, B: A, C: A |
| C-003 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| C-004 | A+C | 95% | A: A+C, B: A+C, C: A+C |
| C-005 | B+C | 95% | A: B+C, B: B+C, C: B+C |
| C-006 | A+B | 75% | A: A, B: A+B, C: A+B |
| C-007 | tie | 95% | A: tie, B: tie, C: tie |
| C-008 | unresolved | 50% | A: A+C, B: A+B, C: A+B+C |
| C-009 | A | 75% | A: A, B: A, C: A+B |
| C-010 | A+C | 95% | A: A+C, B: A+C, C: A+C |
| C-011 | A+B+C | 95% | A: A+B+C, B: A+B+C, C: A+B+C |
| C-012 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| C-013 | B | 75% | A: B, B: B, C: B+C |
| C-014 | B | 95% | A: B, B: B, C: B |
| C-015 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| C-016 | tie | 95% | A: tie, B: tie, C: tie |
| C-017 | B+C | 95% | A: B+C, B: B+C, C: B+C |
| C-018 | A+C | 95% | A: A+C, B: A+C, C: A+C |
| C-019 | A | 95% | A: A, B: A, C: A |
| C-020 | A | 75% | A: A, B: A, C: A+C |
| C-021 | tie | 95% | A: tie, B: tie, C: tie |
| C-022 | A+B | 75% | A: A+B, B: A+B, C: A+C |
| C-023 | B | 95% | A: B, B: B, C: B |
| C-024 | tie | 75% | A: tie, B: tie, C: B+C |
| C-025 | A+B+C | 95% | A: A+B+C, B: A+B+C, C: A+B+C |
| C-026 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| C-027 | C | 95% | A: C, B: C, C: C |
| C-028 | A+B+C | 95% | A: A+B+C, B: A+B+C, C: A+B+C |
| C-029 | B | 95% | A: B, B: B, C: B |
| C-030 | A+B+C | 95% | A: A+B+C, B: A+B+C, C: A+B+C |
| C-031 | A+B | 75% | A: A+B, B: A+B, C: A+B+C |
| C-032 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| C-033 | A | 95% | A: A, B: A, C: A |
| C-034 | A+C | 95% | A: A+C, B: A+C, C: A+C |
| C-035 | A+C | 95% | A: A+C, B: A+C, C: A+C |
| S-001 | C | 95% | A: C, B: C, C: C |
| S-002 | C | 95% | A: C, B: C, C: C |
| S-003 | C | 95% | A: C, B: C, C: C |
| S-004 | A+C | 95% | A: A+C, B: A+C, C: A+C |
| S-005 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| S-006 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| S-007 | B+C | 95% | A: B+C, B: B+C, C: B+C |
| S-008 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| S-009 | A+C | 95% | A: A+C, B: A+C, C: A+C |
| S-010 | B+C | 95% | A: B+C, B: B+C, C: B+C |
| X-001 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| X-002 | A+B+C | 95% | A: A+B+C, B: A+B+C, C: A+B+C |
| X-003 | A+B | 75% | A: A+B, B: A+B, C: A+C |
| X-004 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| X-005 | B | 75% | A: B, B: B, C: B+C |
| X-006 | A+C | 95% | A: A+C, B: A+C, C: A+C |
| X-007 | B | 95% | A: B, B: B, C: B |
| X-008 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| X-009 | A+B | 75% | A: A+B, B: A+B, C: C |
| X-010 | B | 95% | A: B, B: B, C: B |
| X-011 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| X-012 | A | 95% | A: A, B: A, C: A |
| X-013 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| X-014 | A+B | 95% | A: A+B, B: A+B, C: A+B |
| X-015 | C | 95% | A: C, B: C, C: C |
| X-016 | C | 75% | A: C, B: C, C: B+C |
| X-017 | A | 75% | A: A, B: A, C: A+C |
| X-018 | tie | 95% | A: tie, B: tie, C: tie |

## Convergence Assessment
- Points resolved: 68 of 69 (S/C/X: 62 of 63; A: 6 of 6)
- Alignment: 99%
- Threshold: 75%
- Round 1 alignment (S/C/X only): 60% (38 of 63); Round 2: 98% (62 of 63)
- Invariant probe: 40 findings; 20 ADDRESSED; 20 UNADDRESSED (7 HIGH, 11 MEDIUM, 2 LOW)
- Status: BLOCKED_BY_INVARIANTS. CONVERGENCE BLOCKED: 7 HIGH-severity UNADDRESSED invariant(s) detected. Blocking items: INV-001, INV-004, INV-015, INV-016, INV-027, INV-034, INV-036. No further round at depth=standard; base is force-selected by score and the refactoring plan adopts each item's stated Resolution, recorded as such (not as a debated outcome).
- WARNING: 11 MEDIUM-severity UNADDRESSED invariant(s): INV-003, INV-006, INV-009, INV-017, INV-022, INV-025, INV-026, INV-028, INV-038, INV-039, INV-040.
- Unresolved points: C-008 (surface granularity: A+C vs A+B vs A+B+C; all three include A's token-level surface)
- Substantive consensus reached in Round 2: no mechanism inside the diffgate theme lowers blocking-fix-induced blockers without relabelling or hiding them; forecast R3 proxy mean about 3.0 to 3.5, P(both replicates at 3 or fewer) about 0.2 to 0.25, growth about 20% to 27% (bar 44.4%).
