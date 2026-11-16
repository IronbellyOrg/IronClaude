# Round 2 rebuttal: advocate for Variant 1 (haiku-class card), written by an opus-class agent

Paths as in Round 1 ("plan", "spec", "plan-input" = PF/09-plan-input.md). Every file:line below was Read or Grepped in this session on 2026-11-15 unless marked [UNVERIFIED] or [inferred]. "Other advocate" = round1-advocate-2-haiku.md.

## 1. Response to each criticism of Variant 1

The other advocate's section D raises four criticisms. All four are about what Variant 1 missed, not about anything it claimed.

- **D1 (missed the Task 33 scan false positives): CONCEDE.** Confirmed by Grep: `src/superclaude/cli/pipeline/fmea_classifier.py:304,323` and `src/superclaude/cli/roadmap/remediate_parser.py:55,301`. Variant 1's citations never left the plan and spec.
- **D2 (missed rf-qa-qualitative's label-driven verdicts): CONCEDE.** `src/superclaude/agents/rf-qa-qualitative.md:240` "**FAIL** — Any CRITICAL or IMPORTANT issue exists" survives Task 28 as written (plan:340).
- **D3 (Checked bullet on classifier restrictions too broad): CONCEDE in part.** I already conceded in Round 1 that no acceptance check enforces plan:23 and no task reports the input counts that plan-input:15 requires. I hold that the bullet's literal claim is true: plan:23 and plan:135 ("State that M, C and E are asked only when code supplies their inputs") forbid the behaviour, and plan:197 keeps authority off.
- **D4 (missed the tech-research offer and the hooks path): CONCEDE.** plan:273 has no offer; `hooks/hooks.json` does not exist at the repo root.

**Corrections to my own Round 1.**
- **Pair count.** I repeated Variant 2's "7 pairs" although my own Grep output listed 8. The other advocate is right: 239/240, 290/291, 361/362, 428/429, 499/500, 566/567, 745/746 and 783/784 in `src/superclaude/agents/rf-qa-qualitative.md`.
- **Task 39 "catches" the registry contradiction.** That was wrong. See Q1: Task 39 detects it but gives no way to resolve it.
- **Citing plan:365 as a text pin for the cap.** The text pin for `pragmatic.md` is real (`tests/skills/test_review_severity_rule.py:215` defines `CANONICAL_CAP_TEXT`, and line 229 asserts it against the style file). plan:365, however, is Task 30's criterion for the task skill, and the task skill does not hold that text at all (new finding N1 in section 2).

**Where the other advocate supports Variant 1, and I accept it.** C-002, C-003, C-004 and C-012/X-001 go to Variant 1 (other advocate's table, lines 65-67, 75, 77). It also keeps V1 F2 and V1 F6 blocking (lines 130, 134). I adopt F2 (Q1 below). F6 is answered in Q2.

## 2. Updated assessment of Variant 2 (new evidence only)

- **F3 is stronger than its card says.** It has 8 pairs, not 7. M12 is still "rf-qa FAIL count per pilot gate" (spec:974), so the pilot's only FAIL-count metric does not observe rf-qa-qualitative. That makes the leftover label-based FAILs a silent failure, not one a pilot metric would expose (Q4).
- **F5 is stronger.** The output style's once-per-loop ask is the only offer tech-research has in stage 2 (spec:323 "the output-style ask applies only at gates with no carrier offer"). Task 26 moves that bullet (`pragmatic.md:230`, "asks the user once per loop whether to open an issue") out of the style into the full rule (plan:316). From stage 3 on, tech-research has no offer step at all.
- **F6 is stronger (seeded half).** The planted set is used by more than the pilot entry condition. RT1 counts "any safety-class escape in the audit or the seeded set" (spec:985), and RT3 needs a planted set "large enough to see 5 points; size it in the plan" (spec:987). Without the set, two of the pilot's revert triggers have nothing to measure (Q3).
- **F7's hooks limb is weaker under the new test.** Q6 makes "a wrong coordinate or path where the plan states the intent" non-blocking, and plan:321 states the intent ("The hook `pragmatic-subagent.js` still finds and injects the file").
- **New finding N1 (neither card): Task 30's cap criterion checks text the task skill does not hold.** plan:365: "The cap text `at most 2 fix cycles (3 reviews), then escalate to the user with the open blocking findings` is still present word for word (`CANONICAL_CAP_TEXT` pins it)." A Grep of `src/superclaude/skills/task/SKILL.md` for `at most 2|then escalate to the user` returns no match. The skill's cap sentences read "After 2 fix cycles (3 reviews), HALT and escalate to the user with the open blocking findings" (`task/SKILL.md:258`, `:372`, `:409`). `CANONICAL_CAP_TEXT` (`tests/skills/test_review_severity_rule.py:215`) is asserted only against the output style and `canonical_rule_bullets()` (lines 229-230), not against the task skill. As written, the criterion cannot pass. Under Q6 it is non-blocking, because the intent ("the cap is unchanged") is stated and the fix is mechanical: check lines 258, 372 and 409 instead.

## 3. The six questions

### Q1. Does Task 39 catch both halves of the registry finding?

**No. It detects both halves and resolves neither. Blocking, both halves. This reverses my Round 1 call on the document-review half.**

plan:459: "set every registry row to `v2` where its file now holds the digest". That is an instruction to raise rows. It says nothing about rows that are already `v2` without a digest, and nothing about resetting to `legacy`. plan:462 then requires "`... test_review_severity_registry.py -v` passes with strict T2".

- **Document-review half.** Task 35 has already set the row to `v2` ("Update registry rows to `v2`", plan:416), while its own criterion allows "the pointer plus the ledger sentence" (plan:419). The file holds no definition sentence today (Grep of `document_review_loop_prompts.md` for `Grade every review finding` returns nothing; lines 31, 32 and 48 carry the Medium wording). So when Task 39's test runs, the row is `v2`, its file holds no digest, and T1 ("every registry row's file holds exactly one digest", plan:237) fails. The plan gives three possible fixes and picks none: reset to `legacy` (which contradicts Task 35), add the digest (which contradicts Task 35's pointer-only allowance and the file's own-scale role, plan:146), or invent a version value for pointer-only own-scale rows. That is a design decision. Blocking under Q6(i).
- **Task-skill half.** Task 11 creates no task-skill row (plan:146), so when Task 30 says "Update the registry row for the task skill to `v2`" (plan:361), the executor has two paths. (a) Skip, because no row exists; then the row does not exist when Task 39 runs, T1 passes vacuously, and Task 30's instruction was silently dropped. (b) Add a row at `v2`; then T1 fails at Task 39 because Task 30 adds no digest and the spec gives the task skill no digest move (spec:947). In (b) the failure is detected and the fix needs a decision (is the task skill a carrier at all?). In (a) nothing detects it. Blocking under Q6(i) for path (b) and (ii) for path (a).

### Q2. Variant 1 F6 (fresh findings): blocking or a recorded deferral?

**Not a recorded deferral, because the plan records nothing. Blocking under Q6(ii) as written; one line fixes it.**

- plan-input:16: "The plan's second test round needs fresh findings that were not in the 318, plus findings a reviewer called minor that later proved real." plan-input:11 calls this list the "Reconciliation the plan must carry".
- A case-insensitive Grep of the plan for `fresh|second evaluation|second test|circular|outside the 318` returns no match. The plan never mentions the item, so it is not a deferral. Task 4 carries only the second half, as a reviewer-called-minor set (plan:66).
- **What the shadow runs do and do not measure.** Task 16 "reads findings plus a judge answers file" and records verdicts "beside the reviewer's label" (plan:203). Its judges are `FixtureJudge` ("recorded answers") and `ReviewerJudge` ("the reviewer's own label read through the scale map as 0 or 1") (plan:180). With no recorded answers, it records `classifier=unavailable` (plan:208). Tasks 21 and 22 call it in shadow (plan:261, 273). On fresh live findings, then, the shadow runs measure ledger volume, the `consumer-unknown` share, offer outcomes and safety-route hits (spec:946 exit list). The classifier side is either unavailable (no fixture answers exist for new findings) or the reviewer's label read back (`ReviewerJudge`), so agreement with the reviewer is close to true by construction [inferred from plan:180]. They do not measure agreement with any independent label on findings outside the 318. No panel consensus exists for those findings (consensus is only for the 318, plan:54), and no judge that could answer them is built (plan:22).
- **Flag on the criterion.** Nothing in this plan consumes the missing result: authority stays off (plan:197), and the evidence feeds OD4, which is outside the plan. So Q6(ii) over-calls the harm. But the plan must carry the item (plan-input:11) and is silent about it. Fix: one sentence in the plan's Constraints, "the fresh-findings classifier evaluation (plan-input item 4) waits for a judge under OD3; stage 2 ledger rows are its frame." With that sentence the item becomes the explicit owner-left item that Q6 calls non-blocking.

### Q3. Variant 2 F6 (seeded-recall set): is "no executor can produce" true?

**False for seeded recall. Blocking under Q6(i), seeded half only.**

- plan:20: "Their entry conditions need things no executor can produce: the owner's go, at least 5 observed shadow runs with zero safety misses, seeded recall met, and stage 0c done." That is true for the owner's go and arguably for observed runs. It is false for stage 0c, which Task 3 produces (plan:54). It is also false for seeded recall.
- spec:680 gives an executable procedure: "Plant known defects in a held-out deliverable, across four classes ... Review it under the old rule and the new rule with the same reviewers." An agent can write a deliverable with planted defects and spawn reviewers under the two rule texts. Task 3 already does the same thing for the 318 findings with three blind agents and two texts (plan:54). spec:680 also names a candidate starting set (the 44-defect ledger) and says to "plant fresh defects for the real test".
- spec:987 assigns the sizing to the plan: "the planted set must be large enough to see 5 points; size it in the plan". The plan does not size it.
- Why blocking and not owner-gated: the Phase 4 stop does catch the absence, but the owner cannot clear it without work that the plan neither contains nor sizes. Sizing (classes, n per class to see a 5-point drop) is a design decision the spec assigned to the plan, which meets Q6(i). The exemption in plan:20 rests on a false premise, so this is not an item "the plan explicitly leaves to the owner" in Q6's sense. The set also feeds RT1 and RT3 (spec:985, 987).
- **The 8.2 audit half stays non-blocking.** It samples "every non-blocking row of the audit window" (spec:665) during the pilot, and plan:20 already gates Phase 5 on "the pilot's audit window".

### Q4. Variant 2 F3: count, M12, and blocking status

- **Count: 8 pairs.** Grep of `\*\*FAIL\*\*|\*\*PASS\*\*` over `src/superclaude/agents/rf-qa-qualitative.md` gives 239/240, 290/291, 361/362, 428/429, 499/500, 566/567, 745/746 and 783/784. Each FAIL line reads "**FAIL** — Any CRITICAL or IMPORTANT issue exists. ... MINOR issues never fail the review."
- **M12** is defined on rf-qa only: "rf-qa FAIL count per pilot gate | FAIL verdicts per gate in the stage 3 pilot; flat counts falsify the pilot. Rule 6 is reported as a known counter-example until OD16 is decided" (spec:974).
- **Blocking: yes, under Q6(ii), 60%.** The spec contradicts itself. L6 (spec:275) covers "the fixed FAIL triggers in the QA agents (lines that fail a review by label or by a fixed rule ...)", and these 8 lines fail by label. But the 10.4 inventory lists only Rule 6 for this file (spec:854), and stage 3 applies "L6 for rf-qa, and Rule 6 if OD16 chooses (b)" (spec:947). After Task 28 the agent holds the v2 digest ("the label a reviewer used ... is information, never the grade", spec:203) next to 8 instructions that FAIL by label. The precedence sentence (spec:205) does not settle it, because both texts are the agent's own instructions. No later step catches it: Task 32 re-pins Rule 6 and the `## Critical Rules` block hash (plan:383), Phase 5 does not touch the file, and M12 does not observe it. The fix needs a decision the plan does not make: extend L6 to this file at stage 3, or record the 8 lines as kept mechanical gates in the scale map. The decision belongs in both the spec and the plan.

### Q5. Variant 1 F5: where does the harm appear?

**In stage 2. Blocking. Fix is one line.**

- Stage 1 alone is low-harm. It edits no carrier, and its rollback is "delete the new files" (spec:945). Its only edits to existing files are code wiring: Task 16 adds to the subcommand tuple in `cli/review/__init__.py` (plan:203), and Task 18 adds a read-only check to `doctor.py` (plan:225).
- The harm is in stage 2, which the same "one pass" covers (plan:20). Task 21 edits the live task skill (plan:261), Task 22 edits tech-research (plan:273), and Task 23 edits `core/WORKER-CONTRACT.md` (plan:284), each followed by `make sync-dev`. From then on, real runs write ledgers and replace the style's once-per-loop ask with a per-run offer (spec:946). None of this waits for the owner to have seen the stage 0 numbers (spec:940 "No stage starts before ... the owner has seen the numbers"; spec:945 stage 1 entry "stage 0 result written; owner go"). If stage 0b or 0c (Tasks 2 and 3) showed an escape rate or recall loss that argued for stopping, the owner would see it only at the Phase 4 stop, after the live edits.
- Q6(ii): a silently skipped gate that no later step catches. Blocking.
- **One-line fix (plan:20):** "Run `/sc:implement` on Phase 1 alone, then stop until the owner has read the stage 0 results and says go in chat; Phases 2 and 3 may then run in one pass."

### Q6. The test criterion applied to every finding of both cards

| Finding | Call | Limb | Evidence |
|---|---|---|---|
| V1 F1 rule.md vs T2 | BLOCKING | (i) | T2 fails on "any file that holds ... a fence opener and is not a registry row" (plan:237); rule.md must hold the fence (plan:101, 104) and has no row (plan:146). The two fixes, an exemption or a row of a new kind (which breaks "exactly the 11 carriers", plan:150), are a design choice the plan does not make. |
| V1 F2 / V2 F2 document-review row | BLOCKING | (i) | Q1: the row is `v2` (plan:416), the file holds a pointer only (plan:419), and T1 fails at plan:462; plan:459 does not say how to resolve it. |
| V1 F3 / V2 F2 task-skill row | BLOCKING | (i) or (ii) | Q1: plan:361 targets a row plan:146 never creates. Either the instruction is silently dropped, or a `v2` row without a digest fails T1. |
| V1 F4 sweep not in the task skill | BLOCKING | (ii) | plan:273 wires the sweep for tech-research only; plan:261 and 361 give the task skill none; spec:274 makes the sweep the only promotion path. Nothing later adds it. |
| V1 F5 no owner go before stage 1 | BLOCKING | (ii) | Q5: plan:20 against spec:940 and 945; the harm lands in stage 2. |
| V1 F6 fresh findings | BLOCKING as written; flagged | (ii) | Q2: a required item (plan-input:11, 16) with no mention in the plan. **Flag:** the criterion over-calls, because nothing in the plan consumes the result (plan:197). One recorded deferral sentence makes it non-blocking under the owner-left exemption. |
| V2 F1 Task 33 scan | BLOCKING | (i) | The phrases occur in `fmea_classifier.py:304,323` and `remediate_parser.py:55,301`; the allow-list is limited to plan:394 and 399; so plan:397 cannot pass. Choosing between allow-listing code and narrowing the scan to Markdown is a design decision. |
| V2 F3 rf-qa-qualitative, 8 pairs | BLOCKING | (ii) | Q4: these are silent label-based FAILs beside the v2 digest after Task 28 (plan:340), and neither Task 32 (plan:383) nor M12 (spec:974) observes them. The gap starts in the spec (spec:275 vs 854 and 947). |
| V2 F4 classifier inputs: enforcement limb | NON-BLOCKING | missing extra check, plan forbids it | plan:23 and plan:135 forbid asking M, C and E without code inputs; plan:197 keeps authority off. The parity with sketch:46-47 required by plan:183 puts the row in code but enables it for no gate. |
| V2 F4 classifier inputs: row-count limb | BLOCKING as written; flagged | (ii) | plan-input:15 "report how many rows had each" has no producing task (plan:203-208). **Flag:** same over-call as V1 F6 (no consumer inside the plan). Fix: add the counts to Task 16's printed matrix. |
| V2 F5 offers | BLOCKING | (ii) | plan:273 has no offer, and no halt offer exists anywhere (plan:261; spec:323, 946). After Task 26 (plan:316) tech-research has no offer at all. |
| V2 F6 seeded recall | BLOCKING | (i) | Q3: the premise at plan:20 is false; spec:680 is executable and spec:987 assigns the sizing to the plan. |
| V2 F6 8.2 audit | NON-BLOCKING | owner-left | plan:20 gates Phase 5 on the pilot's audit window; spec:665 samples pilot rows. |
| V2 F7 line pins (Tasks 21, 22, 26) | NON-BLOCKING | wrong coordinate, intent stated | Each pin names its content (plan:266, 277, 320); the fix is to pin by text. |
| V2 F7 hooks path | NON-BLOCKING | wrong path, intent stated | plan:321 states the intent; `src/superclaude/hooks/hooks.json:173` passes the intended check. The other advocate calls it blocking (its line 144); Q6's path clause decides against that. |
| V2 F8 Task 24 pin | NON-BLOCKING | plan forbids the wrong behaviour | plan:299 bounds the pin to "before Task 26". |
| V2 F9 wording slips | NON-BLOCKING | wording | plan:150 and plan:399. |
| N1 (new) Task 30 cap criterion | NON-BLOCKING | wrong text, intent stated | plan:365 names text absent from `task/SKILL.md`; the real cap sentences are at :258, :372 and :409. |

**Final blocking list (deduplicated).**
1. V1 F1: rule.md rejected by T2.
2. V1 F2 = V2 F2 (document-review half): `v2` row without a digest; Task 39 does not resolve it.
3. V1 F3 = V2 F2 (task-skill half): a row that does not exist, and no digest.
4. V1 F4: no final-gate sweep in the task skill.
5. V1 F5: no owner go after stage 0.
6. V1 F6: fresh-findings evaluation neither planned nor deferred (flagged: becomes non-blocking with one deferral sentence).
7. V2 F1: Task 33 scan fails on two code files.
8. V2 F3: 8 label-based FAIL pairs left in rf-qa-qualitative.
9. V2 F4, row-count limb (flagged like item 6).
10. V2 F5: tech-research offer and the halt offer.
11. V2 F6, seeded-recall half.

**Where the criterion may give a wrong answer.**
- Items 6 and 9: limb (ii) treats every missing required result as blocking, even when nothing inside the plan consumes it. In both cases the consumer is OD4, outside the plan. I keep them on the list because the plan is silent where it must carry them (plan-input:11). Each needs one sentence or one printed count, not a redesign.
- V2 F7 hooks path: the criterion calls it non-blocking, and I agree, but only because plan:321 states its intent in prose. An acceptance command that fails on every correct run is the kind of defect an executor's per-task QA reports as a failed check. Graders should expect a QA stall here even though the defect is not blocking.
- The "explicitly left to the owner" exemption should not cover V2 F6. plan:20 leaves seeded recall to the owner on a false premise, and spec:987 assigns the sizing to the plan.
