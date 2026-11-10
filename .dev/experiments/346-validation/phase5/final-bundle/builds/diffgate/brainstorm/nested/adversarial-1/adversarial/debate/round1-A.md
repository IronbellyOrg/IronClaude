# Round 1: Variant A advocate (opus, architect)

## Position summary

Variant A should be the base of the merge. Its main parts are worker-owned script steps, a token-level surface, one `DG` line grammar behind a `PROFILES` seam, and a test plan that is the only one to find both existing-test breaks. Together they give the smallest mechanism that fails closed and that later adopters can reuse without changing the script. A should take in four parts from the others: C's removal of the `src/superclaude` line, B's `via=` escape and explicit fix map, and B's more cautious R3 forecast.

## Steelman of Variant B

B's strongest case is that it is the only variant that tests its mechanism against recorded data before predicting anything (U-007). Section 1 says: "Replaying the fix-map gate over the round-2 revision of `flg-r2` ... Total 5 to 2, blocking 1 to 1. Honest reading: the gate removes noise and growth and leaves the induced blocker that a mapped fix produced." That replay is why B's forecast (mean 3.5, "Probability that both replicates meet the R3 bar: about 0.25", section 9) is the best-grounded one of the three. B also names the right failure mode in advance. F1 "wrong lever" (U-011) separates a scope problem from a per-fix defect-rate problem, and it is the most useful falsification condition in any variant. B's `via=` escape (C-013, U-008) is the only mechanism that lets a real regression on an unchanged line block, and it is quote-checked and capped (`VIA_CAP = 2`). The explicit `fixmap-r<N>.txt` with `declined` lines (C-014) makes the reviser's claims auditable and gives under-fixing a visible place, which addresses A-003 directly. B's staged delivery (Stage A inert, Stage B arm, Stage C fold; U-013) is also good refactoring discipline. Each stage can be reverted on its own.

## Steelman of Variant C

C's strongest case is integrity. C is the only variant whose copied command would not ship a `src/superclaude/...` read into an installed primitive (U-016; verified, `src/superclaude/commands/spec-panel.md:220` reads `src/superclaude/examples/release-spec-template.md`). It is also the only variant that separates implementation acceptance from experiment success (section 14, 15 criteria; S-003). C takes the hardest line on the cheapest way to cheat the gate: a MAJOR blocks only with a "confirmed concrete wrong implementer outcome", and "A nonempty outcome string is necessary but not sufficient" (section 4 step 6; C-019). Repair footprints approved before editing (U-015) close the loophole that A and B leave open, where a valid id is pasted onto an unrelated edit. C's state hygiene (exclusive-create lock, generation compare, symlink refusal, 2 MiB and 100,000-line caps; C-035, U-018) is the most complete. The spread check (U-017) is the right statistical guard for n = 2. C is also the most honest about cost: "about 5-13 added minutes per full loop ... Do not call this free" (section 10).

## Key strengths claimed

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

## Weaknesses identified in Variant B

1. **The no-`src/superclaude` rule and the byte-identical drift guard cannot both hold (X-016).** B 8.1: "Every other line is byte-identical to the original". B 8.3 drift guard: "every `## ` section body other than `Review Loop`, `Diffgate` ... equals `spec-panel.md`'s". B 8.3 and 8.5 also require "no `src/superclaude` string anywhere in the variant". Line 220 of the source (re-verified) breaks one of the two whichever way B goes. A has the same defect (X-015, conceded below), but B adds a test that pins it permanently.
2. **The test plan misses `test_routing_refresh.py` (X-012).** B 8.3 lists the tests that "must keep passing without edit" and leaves this one out. As written, adding the command fails line 648.
3. **Graceful degradation hides format failure.** B section 4 tier 3: "the script does not fail the run and does not loop. It degrades fail-safe", exit 0. B's own C1 (missing `verdict:` line or missing `FINDINGS none`) is "hard", yet on the second pass a report with no findings block still gets a derived verdict. B open question 7 admits "I chose degrade so a format error can never block a document review". A blocks exactly that case (A 4.3 step 4: "A missing or empty section can never become PASS").
4. **The reviewer still writes a verdict line (X-006).** C1 requires "a last non-blank line `verdict: PASS|FAIL`" before `check`. C13 then rejects a mismatch once and lets the derived verdict win. This asks the reviewer to compose a verdict that will be overridden anyway, and it spends a reject round on nothing. A's reviewer writes no verdict, and the script prints `verdict_line`.
5. **Arbitrary thresholds sit in the grammar.** `OUTCOME_MIN = 25` turns a judgement rule into a padding rule. B R3 concedes: "pad `outcome` to 25 characters". `FIX_BUDGET_BYTES = 1500` is "calibration UNVERIFIED" (5.2), and `docs/designs/spec-panel-review-loop.md` line 73 already rejects a size limit (X-013).
6. **Its own replay count is off (X-018).** B says "the gate would have allowed 13", but under B's own F1, line 5 carries blocking id N1 and is mappable, which gives 14. The error is small, but it is in the one piece of evidence B leans on most.
7. **Concurrency is left open.** R11: "two workers writing one directory at once are not locked (atomic replace only)." That is acceptable for S1, but it is a risk for the "later adopters" B ranks first (rf-qa).

## Weaknesses identified in Variant C

1. **The design breaks a test that C's own acceptance criteria require to pass (X-017).** C section 8: "Do not edit ... worker contract". 14.14 requires `tests/skills/test_worker_contract.py` to pass. `_check_no_unattended_sections` (line 831, set equality at 837) fails as soon as a new command carries `## Unattended mode`, and C's rewritten section is exactly that. The same applies to X-012 for `test_routing_refresh.py` ("Do not edit ... routing table").
2. **It puts the most weight on the least reliable actor (C-001, X-001).** C section 2: "The coordinator owns transitions and runs the helper." C section 7 then lists as still-prose "whether the coordinator actually invokes the helper". B's critique applies: the coordinator "is also a prose follower". C makes every acceptance depend on that actor's confirmation file (U-014), which, by C's own account, proves presence and not truth ("Presence of a confirmation is checkable; truth of its semantic judgment is not").
3. **A second reject throws away the review (C-011, X-002).** "A second reject marks the run invalid and escalates", with "no new fix cycle". On S1 an anchoring mistake is the expected failure, so the most likely error ends the replicate as invalid. C 9 then says "not a successful replicate", so the experiment pays for a full rerun. A's demotion keeps the run alive and counts the cost.
4. **Whitespace and reflow are inconsistent (X-003, X-009).** C keeps "427's whitespace-only exclusion" for the eligibility mask but also requires "Every group, including whitespace edits, must be covered once, owned by an open blocker". A whitespace fix therefore cannot open scope, yet it needs a blocking owner. C also treats a reflow as a real delta ("No silent flattening"), and on hard-wrapped text that turns cosmetic rewraps into reviewable surface. The surface then grows, which works against the purpose of the gate.
5. **The measurement does not say which count gates the bar (X-008).** The bar row is "Open CRITICAL+MAJOR proxy". The same section says deferred CRITICAL/MAJOR are "excluded from the scoped blocker metric" and also that the recorder "retains the original severity proxy counting rule". A and B both fix this before the run: deferred findings count.
6. **The command text is not given verbatim (S-004).** The seven bullet changes are "described in summary form only". The command text is what a worker obeys, so leaving it as a description postpones the hardest part. A 8.1 gives all nine bullets as single physical lines, ready for the pins.
7. **It is heavy for an experiment arm.** Plugin mirrors (X-011) are not required. `tests/commands/test_routing_plugin_parity.py` lines 42-48 pin only the README-listed commands (fact check). Footprint pre-approval, confirmation files and strict-JSON drafts make the cost "5-13 added minutes per full loop" (C section 10). The `Skill`-tool activation requirement (U-019) adds a load step that a by-path script call does not need.

## Concessions

1. **X-015 is real and High.** A 8.1 says "A byte copy ... with these changes only" and "Nothing else changes". A 8.5 tests that "the string `src/superclaude` is absent". Line 220 (re-verified) makes the specified test fail on the specified file. Fix: adopt C's removal of that line from `## Tool Coordination` (U-016) and name it in 8.1 as a tenth change.
2. **The R3 forecast is overconfident (X-007).** A's "about 60% that both replicates meet the proxy bar" rests on scaling flg-r2 ("scaled to a third of the rows"). It has no replay, and A does not address flg-r1 (R3 = 6) at all. B's replay-grounded 0.25 is better calibrated. A should keep its point forecast but drop its confidence to B's range unless flg-r1 is read first.
3. **The implicit fix mapping is loose (C-014).** Under V2, a hunk is mapped if "its removed or replaced words overlap that finding's quote". A large rewrite that touches one word of a blocking quote therefore passes. A has no `declined` outlet, so under-fixing (A-003) appears only as `open` priors. B's explicit map with `declined` lines is better and should be merged in. A's inline-id path can stay as an accepted alternative form of the map.
4. **There is no mechanism for action at a distance (C-013, X-005).** A section 10 admits "A reviewer that reads only the surface may not notice B". B's capped `via=` is a real improvement, and A should adopt it.
5. **The "P1 plus P2 with exactly 31 entries" claim is overstated.** Per the fact check, line 1564 checks only that `UNATTENDED_EXPECT` has 31 entries.
6. **There are no implementation acceptance criteria separate from the experiment (S-003), and the safety limits are thin.** C's section 14 and its size, symlink and lock limits (U-018) are missing from A.
7. **Remaining prose residuals.** A coordinator who passes a new `--ledger` path starts a fresh review 1 ("Prose only", A section 10). B's `--expect-round` (U-010) is a cheap mechanical fix A lacks. Renumbering noise and inline id clutter are also unresolved (A open question 3).
8. **The cost estimate is probably low (C-027).** "7 to 10 per loop" leaves out the reviewer's correction turns and the reviser's map work. C's envelope is more honest.

## Shared assumptions

- A-001: QUALIFY: A narrows the recovery protocol to one scripted command per exit code (`close` again, then `close --demote`; exit 4 goes back to the reviser), so little improvisation is needed, but compliance is still assumed. Recovery-path compliance should be recorded as a validity input per replicate, not only as cost.
- A-002: QUALIFY: Token-level anchoring limits where findings can sit, but nothing limits how many a reviewer raises per changed span. Findings per changed token should be recorded as a secondary metric so that a density effect is visible instead of assumed away.
- A-003: QUALIFY: Under A, prior blockers left open count in the R3 proxy, so the effect is measured, not hidden. A has no `declined` outlet, though, and should adopt B's, so that under-fixing is explicit rather than showing up as stalled gates.
- A-004: REJECT: The added brief lines ("fix only the ids in the brief file it names", A 8.9) are prose that could produce part of the effect on their own. The result must either be claimed as "script plus brief lines" or include a briefs-only ablation arm.
- A-005: QUALIFY: A's review-1 change is the smallest of the three (DG lines only, no footprints or confirmations), so the assumption is most plausible for A. Review-1 blocker counts should still be checked against Arm B's 13 to 17 as a stated validity check.
- A-006: REJECT: A's causal story (N5 from F22 to N12) is drawn only from flg-r2, and flg-r1 is the replicate that fails the bar (R3 = 6). Read flg-r1's review-3 report before any paid run (B open question 12).

## Per-point positions

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
