# Round 1 statement: Advocate for Variant 1 (V1, sonnet:analyzer)

Subject: three reviewer cards on plan TASK-WF-brainstormFixBri-20261106-113538 against its brief (source.md).
Lens: evidence quality and logical consistency. Focus: correctness, coverage, deviation-classification.

## Position

V1 is the only card that tested the amended live-check sentence (plan:128) for behaviour, not just for presence of its words. That is where the plan's one High-severity question lives (X-003: does the sentence have a false-FAIL path, against plan:133's "no known false FAIL"). V1 found three real tensions there (C-007, C-008, C-011) that V2 and V3 did not probe. I do not claim V1 is the best card overall. V2 is better on literal per-correction coverage and V3 is better on the mechanical fix for the shared P2. A merged result should take V2's table (S-001), V3's byte-check mechanism (C-001), and V1's sentence-behaviour findings (C-007, C-008, C-011, X-003).

Evidence I re-verified this round (all read from disk):
- Spec step 4 Pass rule is "both commands exit 0" (spec:286). Step 5 condition 2 requires the command call be "a top-level message, not a subagent message" (spec:296). "Not verifiable" paragraph is spec:300.
- `src/superclaude/commands/analyze.md:97`: a refused run is "printed in chat only"; `:98`: the contract is written on every outcome.
- `refs/handoff-routing.md:77`: enrichment sources run "via `Task` agents"; a timeout records `skipped`.
- `lc10-result.md:13` (done folder): "Step 5 condition 2 also covers the nested calls ... both with sidechain False". The lc10 precedent therefore reads condition 2 as reaching nested Skill calls.
- No file under `tests/` mentions `orca-worker-contract-spec` (Grep, no files). Nothing tests Task 6's edits.
- `source.md` has no "does not contain" / negative-pin instruction, so the negative pin at plan:144 is a plan addition (relevant to C-002).

## Steelman of V2

V2 is the only card that executes the brief's own checking instrument. The brief prints a Verifier line for each of F-1..F-17; V2 runs each against the plan with plan line numbers, and reports 14 pass and 3 fail, plus Part 4 and Part 5. That is exactly the "coverage" focus of this review, and it makes the result auditable by line. It found real literal mismatches the other cards missed: the plan's extra negative pin against F-7's "exactly these pins" (verified: the brief has no negative-pin instruction), F-12's "every pin added under F-3" quantifier (verified: source.md:161 vs the independent `only by a /sc:analyze call` pin), and Task 1's own negative AC quoting the phrase F-14 says must be absent (plan:45). It also keeps the brief's "copy exactly" rule visible (Part 4 heading, source.md:213) and notes the residual risks were paraphrased. Its 0.93 self-confidence is high, but its calibrated 0.81 is the joint highest.

## Steelman of V3

V3 reads the plan as a maintainer would and finds structural gaps with cheap, concrete fixes. Task 3 is the only wording task with no diff-shape AC (plan:74-77 vs plan:46, :61, :145), so an appended new line would pass every Task 3 check. Task 5's HEAD check lacks the `git cat-file -e` guard that Task 4 has (plan:95 vs plan:111; verified), and plan:90 claims every pin fails on pre-change text while plan:95 and :111 test one phrase per file. Its byte-check mechanism for the shared P2 (save the fenced text, `grep -cF -f`) is the cleanest answer to "copied character for character" and, being equality rather than a pin, does not collide with F-7. It checked the anchors and slice boundaries thoroughly, and it wrote R3-1 with a self-voiding verifier, which is good practice. Calibrated 0.81.

## Strengths claimed

1. Sentence-level probing. V1 asked, clause by clause, what a checker can actually observe. "Returns no tool error" says little for a Skill call that merely loads a command; "did not refuse" has no recorded marker (analyze.md:97, verified); so a missed refusal makes a folder "required and absent". That is a false FAIL and sits against plan:133.
2. Interaction with the spec the plan leaves untouched. The sentence accepts a Skill call "in one of its subagent files", but condition 2 (spec:296) and the lc10 precedent (lc10-result.md:13) require top-level calls, and the routing ref sends enrichment through `Task` agents (handoff-routing.md:77). The plan never mentions this. It is real, and the plan already has a place for it (Constraints, plan:26).
3. Logical-consistency catch on "only when" (necessary, not sufficient). Low stakes, but the sentence is the owner's text and the right output is an owner note, which is how V1 classed it.
4. Honest `unverified` list (S-002). It said what it could not run (git, make lint, session encoding), and E-1 and E-2 later settled two of those. That is the right way to label inference.
5. It correctly kept the plan's wording byte-identical to source.md:219 (checked_clean). No card found a mismatch there.

## Weaknesses identified in V2 and V3

V2:
- Its verifier table tests text presence. A "pass" on F-1 (plan:122, :128) says the words are there; it does not test what the sentence does. It states the qualifications are "retained" without asking whether they can be observed. That is why it is silent on C-008 and C-011 and answers "no" on X-003.
- Three of its "fails" (F-12, F-14, partly F-7) are defects in the brief's verifier wording, not plan defects. Scoring them as plan failures misattributes. For F-12 the plan did the right thing and V2 says so.
- R2-02's fix (move the negative pin out of the AC) would remove a guard against the old wording coming back. Recording it as a Necessary deviation next to plan:131 keeps the guard and fixes the classification.
- R2-06 concerns the reflect run's own coverage matrix, not the plan; it does not change the plan.
- R2-01 asks for exact-equality ACs but gives no mechanism.
- 0.93 self-confidence for a card that ran nothing and did not probe behaviour is over-claimed.

V3:
- R3-1 (P2) is void: E-1 shows the status has only `A`/`R` lines plus this package's `??`, which the exemption covers. Rating it P2 overstated it; the card hedged ("[INFERRED]") but still ranked it equal to the real P2.
- R3-5 is mostly void: E-2 shows `make lint` exits 0 today. Only the "record the exit code" piece survives.
- R3-7 is a style quibble; plan:153 explicitly names the status snapshot as "the one non-log file", so the sentence is self-explaining.
- R3-8 overstates. When the cause is a missing or unreadable session file, spec:300 does fail step 5 and the live check "is not recorded as passed", so risk 4's wording is accurate for that cause. The real gap (readable file, unrecognised call) is risk 2.
- No probing of the live-check sentence's behaviour at all, so it is silent on X-003.
- R3-2's exact_change text is garbled (it tries `grep -cxF`, abandons it, then offers `grep -cF -f`). A `-f` file with a blank line would match every line, so the check needs care.

## Concessions

Citation errors in V1's card (line numbers were brief-file offsets or off by a few lines). I re-read the plan and spec:
- R1-F4: "plan:46 (Task 1 criterion 1)" should be plan:44. "plan:115 (Constraints dirty files)" should be plan:27.
- R1-F1: criteria "plan:142-145" should be plan:143-145.
- R1-F6: "plan:114" should be plan:26; "spec:375" should be spec:296; "lc10-result.md:401" should be lc10-result.md:13.
- R1-F7: "plan:136" should be plan:137; "spec:379" should be spec:300; "lc10-result.md:396" is a brief offset and I did not re-locate it.
- R1-F5: "plan:115" should be plan:27.
- Correct as cited: plan:128, :133, :135, :138, :145, :157, :158; source.md:109, :219; handoff-routing.md:77; analyze.md:97 and :98 (file is `src/superclaude/commands/analyze.md`); Makefile:48-50.

Substance:
- R1-F4 is void today (E-1: none of the six files is modified). A start-state failure would also be loud (the Task 6 `git diff --stat` would not match), not silent.
- R1-F5 is moot today (E-2: `make lint` exits 0, formatting clean).
- R1-F7 is the weakest finding. Its target (risk 4) is the owner's accepted-by-design wording, and Part 4 says to record the risks, not rework them. It should be folded into V3's R3-8 as one owner note, with no plan edit.
- R1-F1's "four fragments" fix is more fragile than V3's whole-text byte check and sits awkwardly with F-7's "exactly these pins". I withdraw the fragment list in favour of V3's mechanism.
- V1 missed V2's three literal-verifier mismatches (F-7 extra pin, F-12, F-14) and V3's Task 3 diff-shape and Task 5 guard gaps. V1 has no per-correction coverage table, which for a "coverage" focus is a real gap.
- V1's own "correct run" framing in R1-F3 has a limit: a refused call means the worker passed a refusable directory, which is itself a defect, so the false FAIL needs both a refusal and a checker that misses it. That makes it a residual risk to record, not a plan defect.

## Per-point positions

| Point | Superior | One-line reason |
|---|---|---|
| S-001 | V2 | The full F-1..F-17 table is the right instrument for a coverage review; caveat: it tests text presence, not behaviour. |
| S-002 | V1 | The explicit `unverified` list is the right labelling; E-1 and E-2 then settled two of its items. Low value. |
| C-001 | V3 (mechanism); V1 (targeting) | V3's saved-text `grep -cF -f` check is simplest and covers Tasks 1-3 and 6; V1 correctly says Task 6 is the weak spot (no test reads the spec, verified). Net V3. |
| C-002 | V2 | Only V2 saw it; verified that source.md has no negative-pin instruction, so plan:144 is an unrecorded addition. Fix: record as a Necessary deviation (plan:131), keep the pin. |
| C-003 | V2 | Real contradiction inside the brief (source.md:161 vs the independent analyze-only pin). Brief defect, not plan defect; a one-line note is enough. |
| C-004 | none / all equal | A plan cannot pin the absence of a string without naming it (plan:45); the F-14 verifier is itself loose. Not worth a plan change. |
| C-005 | V2 on the literal rule; none on action | Part 4 says copy exactly (source.md:213), the plan dropped INV ids, spec line refs and the INFERRED tag. Substance is intact. V1's "narrow it" runs against the same rule. |
| C-006 | V2 | Unique and valid, but it concerns the review's coverage artifact, not the plan. Process note. |
| C-007 | V1 | Only V1 saw "only when" gives a necessary, not sufficient, condition (source.md:219). Owner note. |
| C-008 | V1 | Verified analyze.md:97 (refusal in chat only) and :98. The refusal clause has no recorded marker; plan:133's "no known false FAIL" is slightly overstated. |
| C-009 | none / all equal | V1 and V3 agree; void today per E-1; a failure would be loud. |
| C-010 | V3 | V3 adds the exit-code recording point; the baseline part is void per E-2. V1's version is moot. |
| C-011 | V1 | Unique. Verified: lc10-result.md:13 reads condition 2 as reaching nested calls, and handoff-routing.md:77 routes enrichment through `Task` agents. The sentence accepts subagent files; the spec's step 5 condition 2 asks for top-level. Owner note. |
| C-012 | V1 slightly, V3 acceptable | When the session file is the cause, spec:300 does block the PASS (V1 is right). The remaining step-4-only gap is the owner-note content V3 wrote. Do not copy risk 4 differently; leave plan text. |
| C-013 | none / all equal | V3's only singleton P2 is void per E-1. |
| C-014 | V3 | Verified: Task 3 has no diff-shape AC; a new physical line would pass (plan:74-77). Cheap one-line AC. |
| C-015 | V3 | Verified plan:95 has `git cat-file -e`, plan:111 does not; plan:90's "every pin fails" claim exceeds what plan:95 and :111 test. Minor. |
| C-016 | none / all equal | plan:153 already says "the one non-log file"; not confusing. |
| X-001 | V3's owner-note form | The plan keeps the brief's risk 4 wording; the real gap is an owner note. V2's verbatim demand is formally right but changes nothing of substance; V1's narrowing edits owner text. |
| X-002 | V3 | A whole-text byte check implements Part 4's "copy exactly" and is not a pin, so it does not conflict with F-7. V1's "record it" hedge is unnecessary. |
| X-003 | V1 | The sentence has two unrecorded false-FAIL paths (missed refusal; nested analyze call in a subagent vs condition 2), both needing unusual conditions. Record as residual risks and owner notes; no sentence change. V2's "no" rests on text presence only. |

## A-001 response

QUALIFY (partly contradicted by E-3).

Why not ACCEPT: E-3 shows the per-task reviewer receives the task text and compares the diff to "explicit instructions on the task" (qa.md:9, :13-17); "copied character for character" is such an instruction, and a visible paraphrase of a fenced block is a candidate B4 finding (qa.md:52, "the reviewer can quote that text"). So a paraphrase would not pass unchecked by design. The "QA checks only the AC" premise is wrong as stated.

Why not REJECT: the reviewer is an LLM comparing meaning. Under qa.md:42 a drift that keeps meaning is `minor`, not `blocking`. A dropped clause such as the `skipped` carve-out is easy to miss when reading a long sentence. Task 6 has no test behind it (verified), and the plan's own history (plan:20) shows two earlier plans failed on exactly this sentence. A deterministic byte check costs one grep.

Effect on rating: C-001 drops from P2 to P3 for Tasks 1-3 (pins plus reviewer cover them). It stays P2 for Task 6 only. If the arbiter weighs E-3 heavily, P3 across the board is defensible, and I would accept that.

## Priority table (every finding of every card)

| Finding | Priority | Note |
|---|---|---|
| R1-F1 | P2 (Task 6); P3 (Tasks 1-3) | Replace my fragment list with V3's whole-text `grep -cF -f` check; merge with R2-01 and R3-2. |
| R1-F2 | P3 | Owner note only; do not edit the owner's sentence. |
| R1-F3 | P3 | Add one residual-risk line (refusal clause is read from chat text; literal `--report-dir` match). Do not change the sentence. |
| R1-F4 | drop | Void per E-1; failure would be loud. Merge with R3-6. |
| R1-F5 | drop | Moot per E-2. |
| R1-F6 | P3 | Owner note beside plan:26: condition 2 applies to the command under test, not to nested calls through `Task` agents. |
| R1-F7 | P3 (merge into R3-8) | One owner note; no plan edit. |
| R2-01 | P3 (Tasks 1-3); P2 (Task 6) | Same as R1-F1 and R3-2; one merged AC. |
| R2-02 | P3 | Record the negative pin as a Necessary deviation next to plan:131; keep the pin. |
| R2-03 | P3 | Brief defect note; the plan is right. |
| R2-04 | drop | Cannot pin absence without naming the string; no plan change. |
| R2-05 | P3 | Optional: restore the INFERRED label and spec line refs in risks 1, 2, 4. |
| R2-06 | P3 | Process note about the review's matrix; no plan change. |
| R3-1 | drop | Void per E-1. |
| R3-2 | P2 (Task 6); P3 (Tasks 1-3) | Preferred mechanism for the merged AC; add a blank-line caution for `-f`. |
| R3-3 | P3 | Add the Task 3 `git diff --stat` AC (one line changed). |
| R3-4 | P3 | Add the `git cat-file -e` guard to Task 5, or narrow plan:90 to "the shared directory pin". |
| R3-5 | P3 (exit-code recording only); drop (baseline) | Baseline void per E-2. |
| R3-6 | drop | Void per E-1; merge with R1-F4. |
| R3-7 | drop | plan:153 already names the exception. |
| R3-8 | P3 | Owner note; merge R1-F7 into it. |
