# Proposed wording for the Decision test (drafted by the agent, from runs B, B-rerun, B-rerun2)

THROWAWAY proposal. Nothing installed. Not a decision for the owner to word; the owner decides only whether to adopt it.

## What the three runs showed (evidence, all in the sibling folders' RUN-RECORD.md)

| Finding | What a wrong build does | Rule as it reads today | Grade the runs gave | Grade the owner ruled |
|---|---|---|---|---|
| Tie order: plan says "alphabetically", spec says "plain codepoint order" | A locale-aware sort passes the plan check, breaks the spec | Decision fits ("the plan line is itself an acceptance check") | Blocking | Blocking |
| Tie at the top-N cut: plan never says the cut follows the sort | Keeps first-seen order at the cut; passes every planned check, including the spec example; prints `zebra` where the spec requires `apple` | Debate said "the spec settles it, so the check is only weak" and "nothing named rests on it" | Medium (and missing from the card in rerun 2) | Blocking |
| No-words file: plan says "an empty file", spec says "(no words)" | Returns early on a zero-byte file, prints a blank line for a punctuation-only file; passes plan line 22 | Same reasoning, "nothing named rests on it" | Note or Medium | Blocking |
| "on stdout" dropped from the plan | A build printing results to stderr; other plan lines name stderr only for errors | same | Note or Medium | Medium (stays) |

## Why the rule misfires

The Decision test says a finding blocks when correcting the text would change "an acceptance check ... that the deliverable rests on". Reviewers read "rests on" as "some later step visibly depends on it today", and answer "nothing named rests on it". But when the flawed text IS the acceptance check, correcting it changes the acceptance check by definition. The rule never says so, and it never says what to do when the spec is right and the plan's check is weaker than the spec. Two more things pushed grades down: "the spec settles it" (true, and irrelevant, because the plan is what gets built and tested), and the rule gives no test for "weak check", so each reviewer guessed.

Two different defects are also mixed together and need different grades:
- The spec is silent or ambiguous (what `FILE` means in an error text, what "letters" covers). The plan copies it. Fixing it needs the spec author. That is Medium, unless the plan asserts an exact value that depends on the choice.
- The spec is clear and the plan's check is weaker than the spec. A wrong build passes. Fixing it is a plan edit. That is Blocking.

## Proposed text (replaces nothing; added after the **Decision** sentence of the Blocking definition)

> **Weak check.** A plan, tasklist or test that states an acceptance check weaker than a requirement the spec clearly states is a Decision finding, because the check is the named item that correcting the text changes. It is Blocking when you can name (a) one plausible implementation (a library default, a common shortcut, the first obvious way) that passes the check as written, (b) one input on which that implementation violates the spec, and (c) what the spec requires on that input (output, exit code or message). Write all three in the finding. "The spec already says it" and "nothing later depends on it today" are not reasons to downgrade: the plan is what gets built and tested. It is Medium when another listed check would catch the same wrong implementation, when the difference cannot be seen in output, exit code or message (wording, or a stream the plan's other lines already pin), or when you cannot name the implementation and the input. When the spec itself is silent or ambiguous and the plan only copies it, the finding is Medium (the spec author decides), unless a plan check asserts an exact value that depends on the choice; then it is Blocking.

## Proposed reviewer step (added to the reviewer agent's Responsibilities, before "Return a structured deviation list")

> **Probe each acceptance check with a wrong implementation.** For every acceptance check in the plan, name one plausible wrong implementation that would still pass it. If you cannot, the check is strong. If you can, test the spec line it verifies: does the wrong implementation violate that line on some input? If yes, apply the Weak check rule above. Spend the effort on checks whose spec line states an exact output, order, default, limit or exit code.

## How it sorts the four rows above (my reasoning, to be checked by the test run)

- Tie order: (a) locale sort, (b) `éa` vs `fa`, (c) codepoint order. Blocking.
- Tie at the cut: (a) first-seen cut then sort, (b) `zebra apple` with N=1, (c) `apple`. Blocking.
- No-words: (a) early return on zero bytes, (b) punctuation-only file, (c) no output and exit 0. Blocking.
- stdout: a build printing results to stderr would fail any test that captures stdout, and the plan's error lines already name stderr; (a) is not plausible. Medium or Note.

Side effects I expect and the owner should know about: the default of 10 (plan checks never use more than 10 words) would also become Blocking, as would any other check a plausible wrong build can pass. That is the intended reach, but it will raise blocking counts on weak plans.

## What wording cannot fix

Recall. In rerun 2 no reviewer found the tie at the cut at all; the grading text is not reached for a finding nobody writes. The reviewer step above is the part meant to fix that.

---

# Test result and revision (added after running three reviewers on a private patched agent copy, 2026-11-18)

Setup: reviewers read `patched/reflect-reviewer-patched.md` (installed agent file plus the Weak check bullet and the probe step), same briefs and plan, no owner rulings, no merge. Reviewers were general-purpose agents told to read it and stay read-only (so not the real restricted agent type). Models that answered (transcripts): reviewer-1 claude-sonnet-5-5, reviewer-2 **gpt-6.1-sol** (third time), reviewer-3 claude-opus-5-5. One run each.

| Point | Before (B-rerun cards) | With the proposed wording | Verdict |
|---|---|---|---|
| Tie order | R1 Medium-ish, R2 none, R3 Medium; blocking only after merge | All three Blocking (Decision), each naming a wrong build, an input and the spec result | Works |
| Tie at the cut | No card raised it | R1 named the `most_common` build inside its tie-order blocking row; R3 named it as its own row but graded it Medium: "Plan:15 is the only check that would catch this, and row 1 shows it is weak" | Found by 2 of 3. Not graded Blocking: R3 used my "another listed check would catch it" exception with a check it had itself called weak |
| No-words file | R3 Note | Not raised by any reviewer | Not fixed |
| Default of 10 | Medium (probe only) | R3 row 4 Medium, with the build and the 11-word input named | Under-applied: all three parts of the clause were met and it still said Medium ("half of each line untested") |
| `FILE` in error text | Medium or Blocking depending on step | R1 and R3 Blocking (plan asserts an exact string that depends on the choice) | Consistent with my exception |
| `tokenize.py` clash | R3 found it only in run B | R1 found it (Blocking); R2, R3 did not | One of three |
| New Blocking rows | none | R1: interior apostrophes removed (plausible); R2: valid UTF-8 `café` rejected by an "ASCII-only decoder" (not plausible: such a build is hard to write by accident) | Some inflation. Blocking counts R1 5 / R2 2 / R3 3, against 0 / 1 / 2 in B |
| Labels | Severity column kept | Still kept; R2 wrote "Blocking (Decision)" next to Severity MEDIUM | Not fixed by this wording |

## Revisions to the proposal (three, each from a miss above)

1. The "another listed check would catch the same wrong implementation" exception counts only if that other check is itself strong, meaning you could not name a plausible wrong build that passes it. A check you have flagged as weak cannot rescue another weak check. (R3 row 5.)
2. Make "plausible" concrete: the build a competent implementer would write by following the plan literally with a library default or the first obvious approach, without trying to break it. A build that needs a deliberately odd choice (an ASCII-only decoder) is not plausible. (R2 row 1.)
3. Extend the reviewer step: after probing each acceptance check, walk every spec line that states behaviour on an edge input (empty, no words, fewer than N, a missing or invalid value, a default) and ask whether any plan check would fail a wrong build on that input. If no check touches that spec line's input at all, that is a Missing finding on the check, not only a weak one. (No-words file; default of 10.)

Revised Weak check text, same place: replace its last sentence with: "It is Medium when another listed check that you could not break with a plausible wrong implementation would catch the same wrong implementation, when the difference cannot be seen in output, exit code or message, or when you cannot name the implementation and the input. A plausible implementation is one a competent implementer would write by following the plan literally with a library default or the first obvious approach, not one that needs a deliberately odd choice."

## What is still open

- Recall of the no-words file stayed zero; revision 3 is untested.
- Blocking counts went up on every card (inflation risk is real; revision 2 is meant to limit it, untested).
- The Severity column still sits beside the grade.
- The merge step (adversarial skill) would need the same text; not tested with this wording.
- All of this is one run per reviewer. Run B showed the same reviewer finding or missing the tokenize clash across runs, so single results are weak evidence.

---

# Second test (revised wording), 2026-11-18

Setup: same three reviewers, patched agent copy test2/patched/reflect-reviewer-patched2.md (revisions 1-3 applied), plan copy with corrected header paths (test2/), no rulings, no merge. One run each; reviewers were general-purpose agents, read-only by instruction. Models that answered (transcripts):
R1 requested=sonnet answered-by:       6 claude-sonnet-5-5 
R2 requested=haiku answered-by:       8 gpt-6.1-sol 
R3 requested=opus answered-by:      10 claude-opus-5-5 

| Point | Test 1 (first wording) | Test 2 (revised) | Verdict |
|---|---|---|---|
| Tie order | 3 of 3 Blocking, wrong build named | **0 of 3 Blocking.** R1 Medium ("I could not name an input the plan's checks reliably reject"), R3 row 8 graded LOW: "The first obvious way (Python sorted) is codepoint order, so a competent implementer is unlikely to get it wrong", R2 did not raise it | **Regression caused by revision 2** (the "plausible" definition). The reviewer used it to dismiss the item the owner ruled blocking |
| Tie at the cut | R1 inside tie-order row; R3 Medium | R3 Blocking (Decision) with build, input (`c b a`, `--top 2`) and spec result; R1 Medium (named the build, no failing input); R2 not raised | 1 of 3 Blocking, 2 of 3 found |
| No-words file | not raised by any | R2 Blocking (Missing) with the early-return build and `!!!`; R3 Blocking (Missing) with build and input; R1 Medium (build named) | **Fixed by revision 3: 2 of 3 Blocking, 3 of 3 found** |
| Default of 10 | R3 Medium | R3 Medium again (build `default=None` named; no >10-word input in the plan); R1, R2 not raised | Still under-applied |
| `FILE` in error text | R1, R3 Blocking | R1, R3 Blocking | Stable |
| `tokenize.py` clash | R1 Blocking | R3 only, and only as an advisory correctness gap: "The spec says nothing about file names, so this does not gate" | Worse: the advisory channel in the agent file hid it |
| Blocking rows | R1 5, R2 2, R3 3 | R1 2, R2 1, R3 **6** | R3 inflated: its row 2 says the exact-message check at plan:28 would catch the bug it names; row 3 (only FileNotFoundError caught) and row 5 (omitted argument, argparse message) are arguable |

## What this says (my reasoning)

1. Revision 3 (walk spec edge-input lines) is the part that works: it is what found the no-words file and helped find the tie at the cut. Keep it.
2. Revision 2 backfired. Defining "plausible" as "a competent implementer would write it by following the plan literally" invited the reviewer to argue the implementer would not make the mistake. The owner-ruled item (tie order) was dismissed exactly that way. Drop the "competent implementer unlikely" framing. Replace with: a plausible implementation is one that follows a reading the plan's own words allow, or a library default, a common idiom, or the first obvious approach. If the plan's word ("alphabetically") has a reading different from the spec's (dictionary or locale order), a build following that reading counts. Do not let the reviewer decide how likely the mistake is.
3. Revision 1 (another check counts only if strong) could not be judged: R2 used the old exception in a Medium for "up to n" (the exact example check catches it), correctly. No evidence of harm.
4. The advisory "no-spec correctness gap" channel in the reviewer agent file says such gaps never gate unless Safety. The tokenize.py clash breaks the plan's own T1 and T5 checks, so it is a Decision finding on the plan, even though the spec is silent on file names. The agent file's channel is meant for code that conforms to the spec but is wrong; a plan whose own check cannot run is not that. Proposed one-sentence addition to the Weak check clause: "A defect that makes a check in the plan itself fail or unrunnable as written (a module name shadowing the standard library, a command no task creates) is not a no-spec gap; grade it as a Decision or Missing finding on that check."
5. Inflation remains (R3 had 6 blocking rows). The three-part naming requirement did not stop rows whose own text says another check catches the bug (R3 row 2). Add: "If your own finding says a listed check would catch the wrong implementation, the finding is Medium."
6. Default of 10 stayed Medium twice even with the build named; the clause has no way to say "the plan's inputs never reach the case". Add to the edge-input walk: "A default or limit is an edge input: ask whether any plan input exceeds it."

## Revised revisions (what I now propose, replacing revision 2 and adding 4-6)
- Replace the "plausible" sentence with: "An implementation counts as plausible when it follows a reading the plan's own words allow, a library default, a common idiom, or the first obvious approach. Do not judge how likely the mistake is."
- Add the sentence from point 4 (plan-defects are not no-spec gaps).
- Add the sentence from point 5 (own-finding-says-caught means Medium).
- Add the default/limit sentence from point 6 to the edge-input walk.

Untested. One run each; run B and the reruns show the same reviewer finding or missing the same defect across runs, so single results are weak.

---

# Third test (further-revised wording), 2026-11-19

Setup: same three reviewers, patched agent copy test3/patched/reflect-reviewer-patched3.md (plausible redefined; own-finding-says-caught means Medium; plan defects are not no-spec gaps; limit is an edge input), plan copy test3/, no rulings, no merge. One run each. Models that answered (transcripts):
- R1 requested=sonnet answered-by:  6 claude-sonnet-5-5 
- R2 requested=haiku answered-by:  8 gpt-6.1-sol 
- R3 requested=opus answered-by:  7 claude-opus-5-5 

| Point | Test 2 | Test 3 | Verdict |
|---|---|---|---|
| Tie order (owner: Blocking) | 0 of 3 Blocking | **3 of 3 Blocking (Decision)**, each with build, input, spec result (R1 `zebra élan`, R2 `z é`, R3 `zebra élan`) | Fixed |
| Tie at the cut (owner: Blocking) | 1 of 3 | R1 named the `most_common` build but graded Medium (row 5, because "plan:15 would catch it"); R2, R3 did not raise it | **Worse: 0 of 3 Blocking.** R1 used the own-finding-says-caught sentence against a check it had itself called weak |
| No-words file (owner: Blocking) | 2 of 3 | R2 Blocking (Missing), build and `--- ...` named; R1 Note; R3 Medium ("could not name a plausible wrong implementation that passes plan:16 and fails here") though R2 and test 2 named one | 1 of 3 (was 2 of 3) |
| Default of 10 | Medium | R3 Blocking (Missing) with `default=None` build and an 11-word input; R2 row 1 Blocking on a different count claim | Fixed (1 of 3 raised it) |
| `FILE` in error text | R1, R3 Blocking | R1, R3 Blocking; R3 also row 8 (omitted FILE) Blocking | Stable |
| `tokenize.py` clash | R3 advisory only | **R1 and R3 Blocking (Decision)**, as findings on the plan's own checks | Fixed by the plan-defect sentence |
| Blocking counts | R1 2, R2 1, R3 6 | R1 4, R2 4, R3 **8** | Inflation worse |
| Doubtful new blockers | R3 rows 2, 3, 5 | R2 row 1 (build that stops at 3 results) and row 2 (results logged to stderr); R3 rows 7 (one test per line), 8 | R2 and R3 still produce implausible-build blockers, and now name the build a plausible one by the new definition |

## What this says

1. The three added sentences did what they were for: tie order is back to 3 of 3, the tokenize clash is graded as a plan defect, the default of 10 got a Blocking.
2. They did not fix, and one made worse, the tie at the cut: the "if your own finding says another check would catch it, it is Medium" sentence let R1 downgrade a build it had named, relying on a check (plan:15) that the same reviewer calls weak in row 4. Revise it: "...another check would catch it, and you could not break that check with a plausible wrong implementation (apply the same test to it)". That is the old revision 1 wording; the shorter sentence dropped the condition.
3. Inflation is the main remaining problem (R3: 8 Blocking, 12 rows). "Plausible: any library default, common idiom or first obvious approach, or any reading the plan's words allow" is permissive enough that a reviewer can supply a build for nearly any check. The rule has no cost on the reviewer side. An honest option the owner may prefer to decide: require at most one Blocking row per spec line, merged by spec line, so that rows 3, 7 and 8 style splits of one defect do not multiply; or leave inflation to the merge step, which removed it in runs B and B-rerun2 (merge dropped or downgraded weak rows). Not tested.
4. The no-words file is found by test and reviewer luck as much as by wording: it went 0, 2, 1 of 3 across the three tests with the same wording idea. One run each is too noisy to say the edge-input walk is reliable.
5. The "haiku" slot (gpt-6.1-sol) keeps producing the no-words blocker and the doubtful ones in equal measure; every test so far had it. A real haiku might behave differently; UNVERIFIED.

## State of the proposal
Text to adopt, if the owner adopts anything: the Weak check clause and probe step as in test3/patched/reflect-reviewer-patched3.md, with the own-finding sentence replaced as in point 2 above (untested in that form). Untested pieces: that replacement; any merge-step run with this wording; any inflation control. Installed files unchanged.

---

# Fourth test (own-finding sentence restored with its condition), 2026-11-19

Setup: same three reviewers, patched agent test4/patched/reflect-reviewer-patched4.md (test 3 text, with the own-finding sentence now: Medium only if you could not break the other check with a plausible wrong implementation; if you can, it does not rescue), plan copy test4/, no rulings, no merge. One run each. Models (transcripts):
- R1 requested=sonnet answered-by:  6 claude-sonnet-5-5 
- R2 requested=haiku answered-by:  15 gpt-6.1-sol 
- R3 requested=opus answered-by:  7 claude-opus-5-5 

| Point | Test 2 | Test 3 | Test 4 | Note |
|---|---|---|---|---|
| Tie order (owner: Blocking) | 0 of 3 | 3 of 3 | **2 of 3** Blocking (R1, R2); R3 Medium with build and input named | R3 graded Medium although its own row 6 says one-test-per-line leaves cases open |
| Tie at the cut (owner: Blocking) | 1 of 3 | 0 of 3 | **1 of 3** (R1 row 4: build `most_common` + `zebra apple`, folded into the tie-order Blocking row); R2 and R3 did not raise it | Recovered to test 2 level, not to 3 of 3 |
| No-words file (owner: Blocking) | 2 of 3 | 1 of 3 | **1 of 3** (R2 Blocking Missing, `... !!!`); R3 Note ("could not find a plausible wrong implementation ... plan:9 and plan:16 already make it print nothing"); R1 did not raise it | Stuck at 1 to 2 of 3 across tests 2-4 |
| Default of 10 | Medium | 1 Blocking | **2 of 3 Blocking** (R1 row 6, R3 row 5), build and 11-word input named | Fixed |
| `FILE` in error text | stable | stable | R1, R3 Blocking | Stable |
| `tokenize.py` clash | advisory only | 2 of 3 | **2 of 3 Blocking** (R1, R3) | Stable |
| Blocking rows | 2 / 1 / 6 | 4 / 4 / 8 | **5 / 5 / 6** | Inflation unchanged (R2 blocks all five rows it writes) |

## What this says

1. The restored condition worked as intended on its target: the tie at the cut is raised again (R1), and the tie order is back to Blocking on R1 and R2. It is not reliable: R3 downgraded the tie order, using wording from the plausible definition itself (it named a build and an input and still wrote Medium; its reason is not stated).
2. Default of 10, tokenize clash, FILE: stable and correct across tests 3 and 4. The edge-input walk and the plan-defect sentence are doing real work.
3. The no-words file never reaches 3 of 3. The one reviewer who grades it Blocking is the same each time (R2, the gpt-6.1-sol slot); R3 explicitly argues no plausible wrong build exists, and in fairness the early-return build is a specific choice. This may be a legitimate disagreement about plausibility, not a wording defect. The owner ruled it Blocking; wording alone has not reproduced that ruling more than 2 of 3 times.
4. Inflation is flat at 5 to 6 Blocking rows per card, up from 0 to 2 in run B. Most of it is real findings the owner's rulings agree with (tie order, default of 10, tokenize clash, command, FILE). The rest are doubtful: R2 "one test per line" style rows, R3 row 6 (one test per line, FileNotFoundError only). Row-splitting by one defect across several rows is visible (R3 rows 3 and 6). Not tested: merge-step dedup with this wording.
5. R2's all-five-Blocking pattern and gpt-6.1-sol identity are confounded; every test so far used that slot.

## Recommendation (agent's, not a decision)
Adopt the test-4 text as the reviewer rule (private copy test4/patched/reflect-reviewer-patched4.md; Weak check clause, probe step with edge-input walk, plan-defect sentence, own-finding sentence with its condition). Accept that the no-words file will be Blocking on some runs and not others; if the owner wants it always Blocking, state it as a rule: "A spec line that names an empty or no-input case ('no words', 'empty') is an edge input; if the plan's check names a narrower input (a zero-byte file), the gap is Blocking (Missing) without needing a plausible wrong build." That sentence is untested. Next test, if wanted: that sentence, plus a merge-step run with the text to see if inflation is cut. Installed files unchanged throughout.
