# SPEC variant 2 (analyzer): loosen blocker classification, record and offer follow-ups

Status: Complete (variant 2 of the adversarial comparison; requirements and design options only)
Persona: analyzer. Lens: root cause and evidence.
Date: 2026-11-15. Branch `ironbelly/shadow-runs`.

## 0. How to read this spec

This is a requirements and design-options spec. It contains no implementation code. Nothing under `src/`, `tests/`, `.claude/` or `~/.claude/` was edited to produce it.

**Evidence labels.** Every statement about the repository carries one of these:

| Label | Meaning |
|---|---|
| [V] | I ran a Read, Grep, `stat`, `cmp` or `uv run` in this session and saw it |
| [E] | Taken from an enrichment file or `jev-uses.md`, not re-checked by me |
| [J] | My own judgment or reading, not a measurement |
| [U] | Unverified |

Where an enrichment file and the code disagree, the code wins and the text says so. Section 16 lists the spot checks I ran and the claims I found false or weak.

**Short names used below.**

| Name | Plain meaning |
|---|---|
| R2 | the run-2 task folder `.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/` |
| PF | this program folder `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115/` |
| Gate 1, 2, 3 | the QA checkpoints after research (phase 3), synthesis (phase 5) and the final report (phase 6) in run 2 |
| F_0, F_1, F_2 | the number of open blocking findings at review 1, 2 and 3 of a gate (the cycle controls in R2 use these names) |
| P3-001 | a finding id: "P3" is phase 3 (Gate 1), then a serial number. NEW-1 and NEW-2 are the two findings the first fix introduced |
| Medium | the existing class for a real weakness that blocks nothing (`pragmatic.md:230`); the spec keeps this word |
| Note | the existing "minor" class: wording, formatting, a wrong pointer on a true statement |
| Decision basis | the list of things the deliverable rests on (section 4.3) |
| Consumer | a named later reader of a statement: a recommendation, a table a later step reads, an acceptance check |
| Ledger | the per-run list of recorded follow-up findings (section 6) |
| Jev, Noul, Score | the TypeSafe model and its two answer types: Noul returns a probability that a yes-or-no statement is true; Score returns a probability per level on a short scale |
| Truth table | a small table in ordinary code that turns the model's yes-or-no answers into a verdict |
| Shadow mode | the classifier records its verdict beside the reviewer's label and gates nothing |

**The three boldest design choices in this variant.**

1. The rule is a counterfactual test on a named consumer, not a list of defect kinds (sections 4 and 5). A finding blocks when correcting the text would change something a named reader acts on. The reviewer must write that consumer down; "unknown consumer" is a recorded Medium, never a silent pass.
2. Over-blocking has six causes, and only one of them is the wording of the rule (section 2). The cheapest fixes for the others are not classification changes: stop merging reviewer grades by "highest wins", make fix passes run mechanical checks before re-review, and give upstream gates a declared consumer list. The classifier is a measurement and consistency tool, not the fix.
3. The guardrail is measured, not asserted (section 8): a blind audit of non-blocking findings by a reviewer that does not use the rule, a seeded-defect recall test, and numeric revert triggers with sample sizes that can support them.

## 1. Problem statement

Review gates across the framework call too many findings "blocking". A blocking finding halts the run, forces a fix pass and a re-review, and spends one of at most two fix cycles. The sentence that defines "blocking" says a false claim is blocking whatever its consequence. In run 2 (2026-11-14) that produced fix cycles for findings that changed no decision.

What is true and what is loose in that statement, from my own checks:

- The definition is real and is copied. `Grade every review finding as blocking or minor` is present in exactly 11 files under `src/superclaude` [V: Grep, section 10.1]. The preamble's "21 files, 109 occurrences" is not reproducible; the 21 is a count of listed paths, not of copies [E: `rule-copies-and-tests.md` section 1.1; the 11 re-verified by me].
- Gate 1 did spend a second fix cycle and a third review on two table-pipe defects, but the gate then passed. It is loose to say the defects "failed a gate" [V: `R2/qa/gate1-cycle-control.md`].
- A partial answer exists (the Medium class and `follow-up candidates`). It is stated in prose in three files, performed by no code, and absent from the QA agents and loops that produce most findings [V: Grep, 3 files, 7 occurrences; E for the absence list].

What the owner wants, restated as requirements: real blockers are still found; findings that change no decision are recorded and the user is offered a choice (resolve, file, ignore) instead of a halt; a blocker classifier with a confidence score exists and is validated before it gates anything. Security, data-loss and safety findings are never downgraded.

## 2. Root cause: why the current rule over-blocks

### 2.1 What run 2 actually measured, and what it did not

| Gate | Before | After | Source | Limit of the evidence |
|---|---|---|---|---|
| Gate 1 (research files) | 11 blocking at review 1 (F_0 = 11), average score 2.09 | 6 blocking, average 1.64 (minus 45 and minus 22 percent) | `R2/qa/grading-override.md:30` [V] | A retrospective re-grade: Gate 1 closed under the old definition. The override file was last written at 12:48:30; the Gate 1 control file at 12:20:21 [V: `stat`]. The orchestrator that re-graded also wrote the rule [J]. |
| Gate 2 (synthesis) | the 15 lens reports' own blocking counts summed to 23 | F_0 = 8 after the override and de-duplication | `R2/qa/gate2-cycle-control.md:7` [V] | No control run under the old rule. De-duplication and re-grading cannot be separated. |
| Gate 3 (final report) | 110 findings | 2 blocking, 108 minor; one fix cycle, F_1 = 0 | `R2/qa/gate3-cycle-control.md:7,26` [V] | Same rule graded the audit that followed (Gates 4, 5 and the final check). No independent check. |

Three further limits matter for the metrics in section 13:

- The "average severity score" falls mechanically when a finding moves from blocking to minor. It is not independent of the grading rule [J].
- The five findings the override would have downgraded at Gate 1 (P3-001, P3-002, P3-006, P3-007, P3-013) were in fact fixed in Gate 1 cycle 1, and the final report states the corrected figures: "14 terra + 2 luna", "six uses of Medium", "175 prose spawn lines" [V: `R2/RESEARCH-REPORT-review-panel-unification-run2.md` lines 331, 1015, 3066 to 3068]. So Gate 1 gives no evidence on whether downgrading them would have let a wrong figure through.
- The stated cost "about 25 minutes" for the extra Gate 1 cycle is not supported by file times. Cycle 2 (from the first cycle's last verifier at 12:15:53 to the control file at 12:20:21) took about 4.5 minutes; the whole Gate 1 loop after consolidation (11:58:47 to 12:20:21) took about 22 minutes [V: `stat`; last-write times, not logged start times, so [U] as wall-clock]. The "12:23" printed in the cycle-control header is later than the file's last write, so those header times are not clock times [V]. The benefit of this change is therefore more about avoided work and wrong halts than about minutes.

### 2.2 The six causes

| # | Cause | Where it lives | Run-2 findings it produced | How sure |
|---|---|---|---|---|
| RC1 | The definition blocks any false claim, with no test of consequence. | `pragmatic.md:225`, and the same sentence in the other 10 files (section 10.1) [V]. The reviewer brief at `pragmatic.md:221` also tells every reviewer to hunt for "false claims" [V]. | P3-001, P3-002, P3-006, P3-007, P3-013: five of the 11 review-1 findings (the five the override moved to minor) [V: `qa-consolidated-findings-phase3.md` table 1a, `grading-override.md:30`]. Each is a true statement that something is false; none names a decision that rests on it. | High. Under the written rule these were graded correctly. The rule over-blocks by design, not because reviewers erred. |
| RC2 | Reviewer grades are merged by "highest wins". | `src/superclaude/skills/task/SKILL.md:252`: "Preserve the highest severity rating when duplicates disagree" [V]. | In Gate 1 the merge notes say P3-002, P3-009, P3-013 and P3-015 combine items "some reports graded minor" [V: `qa-consolidated-findings-phase3.md:38`]. P3-015 was graded blocking by one report and minor by at least four. With 15 reviewers per gate, the chance that at least one calls a borderline item blocking approaches 1. Gate 2: 23 reviewer-level blocking counts became 8 after consolidation [V]. | High that the rule exists; medium on how much of the 23 to 8 it explains [J]. |
| RC3 | A fix pass can introduce defects, and a mechanical defect then costs a review cycle. | `R2/qa/qa-verification-structural-phase3-c1.md:85`: "NEW blocking issues introduced by the fix: 2 (NEW-1, NEW-2)"; the fix log touches both rows [V]. | NEW-1 (row VL-24-211) and NEW-2 (row VL-20-625): an unescaped `\|` inside a backticked command gave 8 pipes instead of 7. They alone forced fix cycle 2. No fix-step check counted pipes before handing back. | High. A classification change alone does not remove this. |
| RC4 | Upstream gates cannot apply a "does a decision rest on it" test, because the decision does not exist yet. | Gate 1 reviews research files before the synthesis whose recommendation they feed (phase 5 comes after phase 3) [V: file layout]. | The override's re-grade used knowledge of later phases. A Gate 1 reviewer had no list of consumers. | Medium [J]. |
| RC5 | There is no record path, so a downgrade is unsafe for the reviewer. | The prose at `pragmatic.md:230` and `spec-panel.md:260` is performed by no code [E]. `spec-panel.md` Unattended section (lines 455 to 465) never mentions the follow-up list [V]. Run 2 wrote the marker "(minor under grading override)" 838 times (825 matching lines) in 64 files of `R2/qa/` with no consolidated follow-up file [V: grep, raw counts, not de-duplicated]. | Every minor either vanishes into a lens report or gets labelled blocking so that someone fixes it. A reviewer who wants a defect to survive has one reliable move: call it blocking [J]. | Medium; the incentive argument is judgment. |
| RC6 | The word means different things in different primitives. | `pragmatic.md:230` says a Medium finding never fails a review. `sc-tasklist-protocol/SKILL.md:1614` treats "High or Medium (blocking)" findings as halting [V both]. `card_convert.py:82` maps `important` and `medium` to non-blocking while `rf-qa.md:111` treats IMPORTANT as blocking [V both]. | Not a run-2 finding; a consistency risk for any single-rule change. | High on the facts; the effect is [J]. |

Consequence for the design: a rewrite of `pragmatic.md:225` fixes RC1 only. RC2, RC3 and RC4 need loop and consolidation changes (section 4.6). RC5 needs the ledger (section 6). RC6 needs the one-source design (section 9).

### 2.3 How the existing "stricter" definitions grade the same findings

Four stricter ideas already exist: the spec-panel MAJOR test (`spec-panel.md:259`) [V], the stoprule rubric B1 to B3 (`~/.claude/skills/sc-spec-panel-stoprule-protocol/refs/rubric.md`, installed only) [V], the `/sc:implement` four answers (`qa.md:35-52`) [V], and the run-2 override. They do not agree. My reading, not a measurement [J]:

| Finding | Old rule | Stoprule B1 to B3 | Run-2 override | Proposed (this spec) |
|---|---|---|---|---|
| P3-001 false stale-doc label | blocking | probably blocking: B3(b) "a claim about a source that the source's quoted text contradicts", and a wrong outcome is named (a non-existent gap item) | minor | Medium |
| P3-002 "four" versus "six" meanings | blocking | minor (no reader gets a wrong result) | minor | Medium |
| P3-009 "no contract file" versus "file exists but is not valid YAML" | blocking | blocking | blocking | Blocking |
| NEW-1 pipe breaks a row | graded blocking by the reviewer; the text lists "formatting" as minor | minor (not in the B3 list) | minor | Blocking only if a consumer reads the table by column position; else Note (section 5, case 6) |
| P3-013 stale figures with the correction elsewhere | blocking | minor | minor | Medium |
| A recipe that deletes a directory through an unset variable | blocking | blocking, B3(e) | blocking | Blocking |

The one finding where the run-2 override and the reviewer's own evidence disagree is NEW-1 and NEW-2. The override says a shape defect is minor when it "does not change the meaning of a cell a later phase reads" (`grading-override.md:16`). The verifier wrote that a column-position read now puts `defect` into the destination slot and that ledger 24 is one of the six ledgers the value inventory is built from "by destination" (`qa-verification-structural-phase3-c1.md:39`) [V]. If that is true, the override graded against its own text. The proposed rule does not settle this by opinion; it makes the consumer check part of the finding (section 4).

## 3. Goals and non-goals

**Goals**

| # | Goal | How it is checked |
|---|---|---|
| G1 | Real blockers are still found and still halt. | Seeded-defect recall and the blind audit (section 8) |
| G2 | A finding that changes no decision never halts and never spends a fix cycle. | F_0 and fix-cycle counts per gate (section 13) |
| G3 | Every non-blocking finding is recorded in one place, with evidence, and the user is offered a choice. | Ledger present on every run; offer text in the final summary |
| G4 | One definition of "blocking" is reachable by an installed path, with a test that catches drift in the copies. | Drift test (section 11) |
| G5 | The classifier gives a verdict and a confidence band per finding, is validated on a scored table, and gates nothing until validated. | Five runs, agreement report (section 7.6) |
| G6 | Primitives with their own severity scale keep it, with a written mapping onto the shared rule. | Section 9.3 |
| G7 | Each cause in section 2.2 has a named remedy, or a stated decision not to fix it. | Section 2.2 last paragraph |

**Non-goals**

- Hitting the 35 percent score target. The owner said it need not be strictly met; no threshold below is tuned to reach it.
- Any edit under `src/`, `tests/`, `.claude/` or `~/.claude/` in this step. More than five files change, so a `/sc:workflow` plan must exist first.
- Replacing `/sc:implement` `refs/qa.md`. It keeps its own severity model (`pragmatic.md:228` says so [V]).
- Changing Python code that assigns severity by rule (roadmap structural checkers, audit wiring gate, PR severity router) [E: `severity-models-and-loops.md` section 5].
- Extending `/sc:issue` in version 1. It takes one description and files one issue, is on the never-as-worker list (`WORKER-CONTRACT.md:23` [V]) and has no unattended path.
- Letting the classifier carry the rule change. The rule and the loop changes stand without it.
- Any Jev API call, account or key request in this program step. The key is a dependency, stated as one.
- Raising or lowering the cap of 2 fix cycles.

## 4. The proposed rule in plain words

### 4.1 The rule

The text below is written to be copied into the shared rule document (section 9). It is the one paragraph every copy must hold word for word.

> Grade each finding by what changes if the flawed text is corrected. A finding is **Blocking** only when at least one of these holds, and the finding must say which one and give the evidence:
>
> 1. **Decision.** Correcting the text would change a named decision, recommendation, destination, outcome, acceptance check or quoted number that the deliverable (or a named later step) rests on; or the stated reason for such an item is false or unsupported.
> 2. **Missing.** A required deliverable, section or step, named by the task, the template or the acceptance criteria, is absent in substance.
> 3. **Safety.** Following the text would lose or expose data or a secret, break a safety boundary, or act outside the declared scope. This is never downgraded, whatever label or consequence a reviewer gave it.
>
> Everything else is recorded and never blocks, never starts a fix pass and never appears in a reviser brief. A real defect in substance that nothing named rests on is **Medium**. A defect of form only (wording, formatting that changes no value a reader or a program uses, a wrong tag, label, citation or line number on a true statement) is a **Note**. The label a reviewer used (CRITICAL, IMPORTANT, MAJOR, High) is information, never the grade.

### 4.2 The test a reviewer applies, and the table it produces

Counterfactual: replace the flawed text with the true version. Does any item in the decision basis change?

| Safety risk? | Required item missing? | A named consumer exists? | Correcting the text changes the consumer's output? | Class |
|---|---|---|---|---|
| yes | - | - | - | Blocking (Safety) |
| no | yes | - | - | Blocking (Missing) |
| no | no | yes | yes | Blocking (Decision) |
| no | no | yes | no | Medium (or Note if form only) |
| no | no | none found after looking | - | Medium (Note if form only) |
| no | no | could not be established | - | Medium, tagged `consumer-unknown`, listed first in the offer |

Two rules keep the table honest:

- **Stated reasons count.** A recommendation rests on the reasons the deliverable gives for it. A false reason makes the recommendation "unsupported" even when the recommendation itself would survive. This is why P3-008 ("works in every runtime", built on an unverified row) stays blocking while P3-002 (a miscount whose conclusion holds at any count of two or more) does not (section 5).
- **Form defects with a program as consumer.** A form defect is a Note unless a named consumer reads the structure by position or pattern and the defect changes a value that consumer uses. Then it is graded as Decision. This is code-checkable: the reviewer names the consumer and the check, and the consolidator runs it. It is the rule that decides NEW-1 and NEW-2.

A finding that bundles several defects is split first; each part is graded alone. The finding is Blocking if any part is, and the blocking part is stated in one line so the fix agent does not rework the Medium parts.

### 4.3 The decision basis: what it is, where it comes from

"Rests on" means one of three things: the deliverable's stated reason for an item cites the statement; the item is computed from the statement; or a later named step reads the statement as input.

| Deliverable kind | Decision-basis items | Source of the list | Available today? |
|---|---|---|---|
| Final research report or synthesis | recommendation, option ranking, destinations in the inventory, conflict-log outcomes, numbers quoted in those, stated reasons | the report's own sections, named by its template; a code check finds the quoted figure inside them | Yes [J] |
| Research input file (an upstream gate) | the declared consumers: which later item reads which figure, row or column | a consumer line per phase output in the task file ("feeds item X, reads column Y") | No. Without it, every finding is `consumer-unknown` and lands as Medium [J] |
| Spec | requirements, acceptance criteria, boundary-table rows, quoted constraints and non-goals | the spec's headings | Yes [J] |
| Tasklist | acceptance criteria, ordering and dependency edges, quoted constraints | the tasklist's items | Yes [J] |
| Code change under `/sc:implement` | acceptance criteria, declared outputs, quoted constraints | `qa.md` already collects them (`ac-outcome-missing`, `quoted-constraint-breach`) [V] | Yes |

Three ways to obtain the list, with a recommendation:

| Option | Idea | Strength | Weakness |
|---|---|---|---|
| A. Producer-declared | the deliverable carries a short "rests on" block written by its author | cheapest for the reviewer | the author can shrink the list to dodge blockers |
| B. Reviewer-named | each finding names its consumer and what would change | works with no new artifact | a reviewer can invent a consumer |
| C. Code reference check | code searches the decision-basis sections for the quoted figure, row id or claim | cannot be argued with | covers only quotable items |

Recommendation: B for every finding, verified by C wherever the item is quotable, with A required only for upstream phase outputs (the consumer line). The audit in section 8 checks for shrinking.

### 4.4 Loop and consolidation changes the rule needs

| # | Change | Cause it answers | Where |
|---|---|---|---|
| L1 | The consolidator grades by the rule and keeps every reviewer's own grade visible. "Highest severity wins" is replaced. When reviewers disagree and the evidence cannot decide it, the finding is Medium tagged `disputed`; if the reviewer who said blocking named a consumer and the code check confirms it, it is Blocking. | RC2 | `task/SKILL.md:252`, `361`; the same line in `task-builder`, `tech-research` [E for the last two] |
| L2 | A fix pass runs every mechanical check that exists over the lines it edited before it hands back: table pipe count, byte-present quotes, recomputed counts, link existence. The results go into the fix log. A defect a verifier finds that the fix introduced carries `origin: fix-induced` and is graded by the same rule. | RC3 | `rf-qa.md` Fix Cycle section; `task/SKILL.md:254` |
| L3 | The cap and the regression and monotonicity halts count Blocking findings only (they already count "blocking", so this follows from the definition). At the cap the escalation offers three choices: fix by hand, accept and file (the finding becomes a follow-up tagged `accepted-blocker`), or stop. The cap stays at 2 fix cycles. | RC1 | `rf-qa.md:402-415` [E]; `task/SKILL.md:258` [V], `372` [E] |
| L4 | The task builder writes a consumer line for each phase output. | RC4 | `task-builder` and the MDTM templates 01 and 02 [E] |
| L5 | Medium and Note findings are never rechecked. A fix that touches a Medium row's location does not reopen it. | RC1 | same text as today (`pragmatic.md:226`) [V] |

### 4.5 What does not change

Security, data-loss and safety findings stay blocking, including a finding the reviewer called minor or Medium. The verdict stays binary (PASS or FAIL). A review with no finding is still valid and must say what it checked (`pragmatic.md:222`) [V]. A reviewer still never invents a finding and never works to a quota.

## 5. The decision-basis test and worked examples

Each case gives the verdict under the proposed rule and the reason, written as the consumer the reviewer would have to name. Cases 1 to 10 come from the run-2 Gate 1 findings (text read in `R2/qa/qa-consolidated-findings-phase3.md` table 1a and `qa-verification-structural-phase3-c1.md`) [V]. Cases 11 to 14 are realistic cases I constructed. Verdicts are my application of the rule [J], not measurements.

| # | Case | Old rule | Proposed | Reason: consumer, and what would change |
|---|---|---|---|---|
| 1 | P3-001: research file labels a docstring "stale" but quotes only half its sentence; the full sentence matches the code (`findings_v2.py:3-4`) | Blocking | **Medium** | Consumer named by the reviewer: the gap list in the synthesis. Correcting removes one list entry. No recommendation, destination or quoted number changes. Hard case: flips to Blocking if the owner counts a gap-list entry as decision basis (decision D5). |
| 2 | P3-002: one file says "Medium has four meanings", another found six | Blocking | **Medium** | Consumer: a headline figure in a table row. The conclusion "the word is ambiguous" holds at any count of two or more. Nothing changes. The final report states "six uses" (line 1015) [V]. |
| 3 | P3-009: "3 runs have no `return-contract.yaml`"; the file exists but is not valid YAML (an unquoted `[1m]` alias inside a list) | Blocking (CRITICAL) | **Blocking (Decision)** | Consumer: the recommendation on the contract writer. The true fact adds a requirement (quote or escape aliases containing brackets) that the wrong fact hides. The finding's own proposed fix says so. |
| 4 | P3-003: "reflect has no fix loop"; code shows a bounded loop that is dormant | Blocking | **Blocking (Decision)** | Consumer: the overlap matrix cell for the "ledger and rounds" capability, which feeds a report section. The cell value changes from "absent" to a qualified statement. |
| 5 | P3-005: file says finding location type is "not a core blocker"; two probes show a finding with no `anchor` raises a KeyError in the ledger path | Blocking | **Blocking (Decision)** | The claim is the stated reason for a recommendation about an adapter. A reproduced failure makes the reason false. |
| 6 | NEW-1 and NEW-2: a fix left an unescaped `\|` in a backticked command, so two ledger rows have 8 cells instead of 7 | Blocking | **Blocking if a consumer reads the table by column position, else Note** | The verifier states the value inventory is built from the ledgers "by destination" and that Destination reads `question` instead of `EVAL` on row VL-20-625 [V]. The consolidator runs one check: does the inventory step parse by position or by header? If by position, 2 destinations are wrong: Decision. If by header, nothing changes: Note. Either way, rule L2 (section 4.4) would have prevented the cycle. |
| 7 | P3-006: two files give 185 and 175 for a spawn-line count | Blocking | **Medium** | Consumer: the synthesis. At Gate 1 the reviewer could not say whether a recommendation uses the figure, so `consumer-unknown`. The final report carries it only as a correction ("use 175, or 44 structured", lines 3068 and 3387) and as open question OQ23 (line 4686) [V]; I did not find a recommendation that rests on it [U: not a full read of the report]. |
| 8 | P3-007: plugin mirror of the Review Loop: "softens the hard gate" is false (it extends it); "25 changed lines" is 18; plus counts that depend on definition | Blocking | **Split.** "Softens" and the line count: **Medium**. Any row whose destination changes: **Blocking** | The finding bundles four defects with different consumers. The reviewer must name any row whose destination (CORE, MODULE, DROP) would change. VL-24-396 is marked CORE in the finding; if its destination survives the correction, nothing blocks. |
| 9 | P3-013: ledger rows still quote "16 empty terra reviews" and "four verdict flips" while sibling rows and the register carry the correction | Blocking | **Medium** | The override already names this class: a stale figure with a discoverable correction (`grading-override.md:17`) [V]. Consumer: the synthesis, which "must not quote 16 empty terra". The final report says "14 terra + 2 luna" (line 331) [V]. |
| 10 | P3-008: a takeaway says one exchange design "works in every runtime", built on a row tagged unverified; the measured smoke rows time out | Blocking | **Blocking (Decision)** | The claim is the stated reason for choosing that design. The recommendation (leave exchange optional) would survive, but its reason is unsupported (rule 4.2, "stated reasons count"). |
| 11 | A task recipe runs `rm -rf "$DIR/"` and `DIR` can be unset; the reviewer wrote "nit: quoting" | minor | **Blocking (Safety)** | Following the recipe can delete the wrong tree. The label is irrelevant; Safety is never downgraded. |
| 12 | A template requires an "Acceptance" section and the deliverable has none | Blocking | **Blocking (Missing)** | A required section is absent. If the section exists but is thin and its checks can still pass, the finding is **Medium**. If the checks cannot pass, Decision. |
| 13 | A citation says `file.py:120` and the true claim now sits at line 131 | minor | **Note** | True statement, moved pointer. No consumer reads the number. |
| 14 | A docstring says a function returns `None` on failure; the code raises | Blocking | **Medium, `consumer-unknown`**; **Blocking (Decision)** if the finding names a caller that tests for `None` | A false claim with no named reader is a real defect nobody acts on yet. It goes first in the offer so a person can say whether a caller exists. |

Three observations from the table:

- The proposed rule agrees with the run-2 override on 8 of the 10 Gate 1 cases. It differs on case 6 (consumer check instead of a blanket minor) and case 8 (split instead of a blanket minor) [J]. Both differences ask the reviewer to name a consumer, which is the point of the design.
- Cases 1 and 7 show the real risk of the test: it moves the judgment from "is this false" to "does anything rest on it", and a reviewer can answer "nothing" too easily. That is why the audit (section 8) samples Medium and Note findings, not blockers.
- Case 14 shows `consumer-unknown` doing real work. Without it, the choice is silent pass or blind block.

## 6. Record-and-offer behaviour

### 6.1 Flow

1. Each reviewer writes every finding with the fields in 6.2, including `rests_on` (the named consumer, or `none`, or `unknown`) and a one-line `why not blocking` for Medium and Note findings.
2. The consolidator grades by the shared rule (L1), merges duplicates, runs the code checks for any `rests_on` that names a program consumer, and writes the ledger.
3. Only Blocking findings go to the fix agent and the reviser brief. Medium and Note findings are never rechecked.
4. The fix agent runs the mechanical checks over its edits (L2) before verification.
5. At the end of the run, and at any escalation halt, the top-level session shows the offer (6.3). It never offers per loop.
6. Nothing is created without the user's answer. Filing writes the issue number back into the ledger rows.

Cadence changes from "once per loop" (`pragmatic.md:230` [V]) to once per run, because run 2 had five gate cycle-control files plus a final validation [V: listing of `R2/qa/`], so a per-loop question would be asked six times for one list. The test that pins the old wording changes with it (section 11).

### 6.2 Ledger format

One Markdown file per run, `follow-ups.md`, in the run's report directory. A header block holds the run id, date, tier counts and the classifier mode. Medium findings get a full row. Note findings get a short row (id, location, one line) in a second table, so the file does not grow into the 838-line marker pile that run 2 produced [V: raw match count, not de-duplicated].

| Column | Content |
|---|---|
| `id` | `FU-<gate>-<n>`, stable across reviews of the same gate |
| `tier` | Medium or Note |
| `source` | gate, review number, reviewing agent, and the grade it gave |
| `location` | `path:line` or a row id |
| `finding` | one line |
| `evidence` | the verbatim quote and the `path:line` that shows it |
| `rests_on` | `none` / `unknown` / the named consumer that does not change |
| `why not blocking` | one line, required |
| `tags` | any of `consumer-unknown`, `disputed`, `fix-induced`, `accepted-blocker`, `unsettled` |
| `proposed fix` | one line |
| `suggested type` | bug, refactor, docs, test (the shape `sc-troubleshoot-protocol/refs/report-template.md` already uses for follow-up tasks [E]) |
| `status` | open, resolved, filed, dismissed |
| `issue` | the issue number once filed |

De-duplication key: location plus a hash of the quote. Sort order: `consumer-unknown`, then `disputed`, then Medium by consumer, then Notes. The offer shows counts and the first five rows, never the whole list.

### 6.3 Offer wording (draft)

> Review follow-ups. This run recorded N Medium findings (K have no known consumer and need your eye) and M notes. None blocked. They are in `<path>/follow-ups.md`.
> 1. Resolve now: one fix pass over the Medium findings you pick, mechanical checks only, no new review loop.
> 2. File one issue that lists all N Medium findings. (Recommended)
> 3. File individually: tell me which ids.
> 4. Leave them in the ledger.
> Nothing is filed until you answer.

### 6.4 Unattended runs

- The run records only. It writes the ledger, lists its path in `artifacts` of the return contract, and keeps `worker_status` at `succeeded` or `partial`, because follow-ups never fail a review. This fits the existing default at `pragmatic.md:230` ("only records the list") [V] and the rule that an unattended command never asks (`WORKER-CONTRACT.md` WC-2 [E]).
- Proposal, not existing behaviour: one optional contract key `follow_up_ledger` (a path) and a count. The contract rules already allow extra keys beside a command's own [E: WC-4 line 35]; no such key exists today.
- Filing is done by the coordinator or the top-level session after the person says yes. Workers have no outward actions, and `/sc:issue` is on the never-as-worker list [V: `WORKER-CONTRACT.md:23`].
- A classifier verdict of `SHOW_USER` in an unattended run means the reviewer's own label stands and the row gets the tag `unsettled` (section 7.3).

### 6.5 Batching into one issue

`/sc:issue --create` takes one description (free text or `@path`) and files one issue; there is no `--repo`, preview or dry-run option; its Complexity field follows `--depth` [V: `~/.claude/commands/sc/issue.md:9,31,36-42,46`]. It has no ledger input and no batch mode [E].

| Option | What happens | Verdict |
|---|---|---|
| A. Umbrella description | The session renders the open Medium rows into one description file (sections like the backlog template: what was found, evidence, done when, pick-up note) and runs `/sc:issue --create @file --mode bug --type <area> --depth standard`. Rows get `status: filed` and the issue number. | **Recommended for version 1.** No change to `/sc:issue`. |
| B. One issue per row | Many issues from one run. | Rejected: 108 non-blocking findings came from one Gate 3 review alone [V: `gate3-cycle-control.md:26`]. |
| C. Extend `/sc:issue` with `--ledger` | Per-row fan-out, write-back, an unattended path. | Later, only if A shows demand. Needs a change to a never-as-worker command. |

Option A leaves three gaps, stated rather than hidden: the Complexity field cannot differ from the depth, the four templates fit one feature or bug better than a list, and `/sc:issue` may ask the user about new material in a draft [E: `follow-up-and-issue-mechanisms.md` section 3]. Filing is therefore an attended step. The target repository is always `IronbellyOrg/IronClaude`, resolved from `origin`; no Orca link flag is passed for this repo (project `CLAUDE.md` [V]).

### 6.6 Where the ledger lives per primitive

| Primitive | Ledger location | Note |
|---|---|---|
| task skill, tech-research | `${TASK_DIR}qa/follow-ups.md`, next to the consolidated findings [V: `R2/qa/` exists] | the task skill already has a **Follow-Up Items** path for out-of-scope findings (`task/SKILL.md:361` [V]); the ledger absorbs it |
| spec-panel | `<report-dir>/follow-ups.md` and the report's `follow-up candidates` section | the Unattended section (`spec-panel.md:455-465`) gains one line [V that it has none today] |
| `/sc:implement` | keeps `notes.md`; the ledger holds a pointer row | `qa.md` has a closed list of interrupts and writes no ruling for minors-only replays [E]; do not add an ask |
| reflect | `<output>/follow-ups.md`; Drift with no decision basis is a candidate (section 9.3) | [E] |
| pr-submit | keeps its report-only list | own tier router, stays [E] |

### 6.7 What "resolve now" does

One fix agent with fix authorization works only on the ids the user picked, runs the L2 checks, and appends what it changed to the ledger row (`status: resolved`). If the agent finds that a picked Medium finding is in fact decision-bearing, it stops and says so; it does not widen the edit. There is no re-review loop; a person who wants one starts a new review.

## 7. The blocker classifier concept and its Jev use

Source material: `PF/02-brainstorm/jev-uses.md` (the Jev design, [E] unless noted) and the sketch `PF/02-brainstorm/blocker_truth_table_sketch.py` (referenced, not copied).

### 7.1 Role

The classifier is a second, independent judge of one finding at a time. It reads only the finding record (quote, span, stated outcome, evidence excerpt, `rests_on`, and the decision basis when code can supply it). It cannot open files or count, so code does every exact check first (quote present, required section present, figure recounted) and passes the result in as state. Its value is **consistency and measurement**: the same rule applied to every finding, with the reviewer's own label recorded beside it. It does not fix RC1, RC3 or RC4; it addresses the grader variance behind RC2 and gives the program a way to measure the rule. The spec therefore requires that the rule and the loop changes stand without it.

### 7.2 Questions

Each question is one yes-or-no statement phrased so that a "yes" means the condition is present. No question uses the word "blocking". The decision stays in the truth table in code.

| Id | Plain statement the model judges | Needs from code |
|---|---|---|
| S | Following the quoted text would delete, overwrite or expose data or a secret, or act outside the declared scope, **in a way the task did not ask for**. | nothing |
| M | A required item named in the finding is absent in substance. | code confirms the section or deliverable is not present by name first |
| C | The quoted text breaks a quoted constraint or non-goal. | the constraint lines |
| W | A reader or test following the quoted text exactly would produce a specific wrong result. | nothing |
| E | The evidence excerpt shows that a statement in the quote is false. | code marks the excerpt verified or not |
| D | A decision-basis item would be wrong or unsupported if the quote stays. | the decision-basis excerpts (4.3) |

This is six questions, not the ten in `jev-uses.md` section 3. T (true in substance, only the pointer wrong), F (only form), I (intent inferable) and G (a suggestion, not a defect) feed no cell of the truth table; `jev-uses.md` itself says they mostly explain why a finding is on the ledger. They cost calls, widen the over-fitting surface and can be filled by the reviewer's `why not blocking` line. I keep them out of the gating path. The S wording change ("that the task did not ask for") is mine: as written in `jev-uses.md` ("would delete, overwrite or expose data"), a recipe that deliberately deletes its own temp directory would score yes. [J]

**Variant for upstream gates.** D needs a decision basis that does not exist for research inputs (section 4.3). Option Q replaces D with a statement the finding record can answer alone: "the finding names a specific later reader or step that uses the quoted text". Code then checks the named consumer exists. The property tests in 7.3 apply to either version.

### 7.3 Truth table

The sketch turns each question's probability into Y, N, U (unsettled) or UNSET (skipped or failed; never read as N), then applies: S = Y gives BLOCKING; M = Y or C = Y gives BLOCKING; otherwise "wrong" is W or E, and the pair (wrong, D) selects one of BLOCKING, SHOW_USER, FOLLOW_UP or NOTE; an unsettled S lifts anything below SHOW_USER to SHOW_USER and never lowers BLOCKING. I re-ran it: 4096 input combinations, each returns one verdict, and 0 monotonicity violations in the sketch's own check [V: `uv run python`].

What the sketch's check does not cover, which the spec must say:

| Finding | Evidence | What the spec requires |
|---|---|---|
| The check skips every transition that starts or ends at UNSET. "Monotone in every input" holds on the answered scale N, U, Y only. | the sketch's check excludes `UNSET` moves [V: code read]; I counted 432 of 18,432 UNSET-to-answered transitions that lower the verdict: 216 on D, 108 on W, 108 on E [V: `uv run python`] | State it as a design rule: UNSET means "send to a person", so answering a question can lower a verdict. The property test covers the answered scale and a separate test pins the UNSET rule. |
| The first draft had a precedence bug (511 violations) [E] | the lesson is stated in `jev-uses.md` section 4 | Keep two property tests: every combination has one outcome; no answer can lower a verdict that S, M or C already made BLOCKING. |
| Whether the (wrong N, D Y) cell NOTE is right is untested | `jev-uses.md` itself logs the cell as a possible mis-answer | Count it per run; do not tune it. |

Verdict meanings are as in `jev-uses.md`: BLOCKING; FOLLOW_UP (Medium); NOTE; SHOW_USER (the classifier will not decide); UNDETERMINED (no usable answer, go to the next judge).

### 7.4 Confidence

The owner asked for a confidence score. Three facts constrain it: a Noul returns only P(yes) and no confidence field; the Score and Choice `confidence` measures how peaked the answer is, not how likely it is right [E: `confidence.md`, SKILL.md]; and whether Jev's probabilities are calibrated for "does this finding name a wrong outcome" is unknown until measured [E, and I agree].

My changes to `jev-uses.md` section 5:

- The weakest-link formulas mix two biases. For BLOCKING by W and D, `min(pW, pD)` is an upper bound on the joint probability, so it flatters a confirm. For a downgrade, `1 minus min(1, pS + pM + pC + min(pW, pD))` is a union bound that can reach zero when four mid-sized terms are added, which would send nearly everything to SHOW_USER. Both are defensible as conservative for a downgrade, but neither is a probability, and calling the result "confidence" invites readers to treat it as one.
- Report an ordinal **band** until a reliability table exists: `high` (every decisive question is outside the unsettled band in at least 2 of 3 replicates and the verdict is the same in all 3), `medium`, `low`. Print the raw probabilities and the replicate spread beside it. Numbers replace bands only after the calibration step below shows the bins are reliable.
- Keep the asymmetry: a downgrade needs a higher bar than a confirm (placeholders `tau_down` 0.85 and `tau_block` 0.70 from `jev-uses.md`), fitted on one half of the scored table and checked on the other half. With 30 to 40 rows the held-out half is 15 to 20 rows, so report counts, not percentages alone.
- Replicates: pin the model id (`jev-1.14.0`, not an alias) and send 3 requests per finding. Because the vendor may cache identical requests [U], vary the field order between replicates so the spread measures real sensitivity.

### 7.5 Judges, shadow mode, key dependency

| Order | Judge | Needs | Status |
|---|---|---|---|
| 1 | Jev (`jev-1.14.0`) | an API key; permission to send finding text off the machine | no key in this environment [E: `jev-uses.md` section 1; I did not re-search] |
| 2 | a tool-less LLM judge that returns a probability per question | none | precedent: the `finding-grader` agent, which returns one boolean per claim; it exists only under `~/.claude/agents/`, not in `src/superclaude/agents/` [V: ls]. Using it means adding it to `src` or writing a new agent, so it belongs in section 10. |
| 3 | the reviewer's own label as a 0 or 1 | none | today's behaviour; the baseline the others must match |

If the last judge is the only one left, the reviewer's label stands and the row records `classifier=unavailable`. A call error is never an N. Every result records which judge produced it, and results from different judges are not compared.

**Without a key, these still work:** the question module, the thresholds config, the truth table and its property tests, the judge interface with its four implementations (Jev, LLM, reviewer, fixture), pre-written request payloads for every scored finding, and the five runs with the LLM judge [E]. **With a key:** the Jev runs, which are the only way to measure Jev's agreement, flip rate and calibration.

**Go or no-go for Jev (my addition).** Jev joins only if, on the same table, it matches the LLM judge's agreement and has a lower flip rate, at an acceptable latency, after the owner has decided the privacy question (D3 in section 15). The docs give no accuracy figure for this task; no superiority is assumed. The listed price (about $0.08 for five runs of 40 findings with 3 replicates [E: arithmetic checks: 600 requests at about $0.000126]) is not the real cost; privacy, dependency and per-gate latency are.

**Shadow mode.** The classifier writes its verdict and band into the ledger row and the finding record beside the reviewer's label and gates nothing. A per-run table shows the disagreement matrix. Exit criteria to anything stronger are fixed in advance (section 13).

**Gating, if it ever happens, is one-directional.** The classifier may route a reviewer-Blocking finding to a person with "probably not blocking" (SHOW_USER). It never auto-downgrades. In an unattended run no person is present, so the reviewer's label stands. The benefit in unattended runs then comes from the rule and loop changes alone. I recommend this stance (D4).

### 7.6 Test plan and its limits

| Item | Requirement |
|---|---|
| Table | at least 30 past blocking findings, each scored blind 1 to 5 by three independent agents, averaged, with a minimum blocking threshold [per `00-issue-description.md`] |
| Five runs | the same table, five times, per judge; report per-finding flip rate across runs |
| Reported | agreement with the validated label, Cohen's kappa, the full confusion matrix with counts, recall on validated blockers (the costly error is calling a validated blocker non-blocking), per deliverable kind (tasklist, spec), the band reliability table, and the spread of the three scorers |
| Contested rows | rows where the three scorers differ by 2 or more are reported separately, not folded into the average |
| Intervals | with n = 30 and 27 agreements (90 percent), the 95 percent Wilson interval is about 74 to 96 percent [computed]. Do not claim a point figure |

Three weaknesses in the validation design that I would fix before the runs:

1. **Circular labels.** `jev-uses.md` recommendation 4 makes the five Score situations the same sentences as the human 1 to 5 scoring rubric. Then agreement measures rubric consistency, not truth. Fix: the three scorers score blind without the Score-level text, or half the table is scored each way; report the gap.
2. **Selection bias.** The table holds only findings some reviewer flagged blocking. It cannot show a real blocker a reviewer called minor, which is the error that matters most here. The audit in section 8 supplies those cases. The table also holds no code-review findings, so a classifier result says nothing about code [E: `jev-uses.md` risk 11].
3. **Missing decision basis.** If D is UNSET for most rows, nearly every wrong-outcome row lands in SHOW_USER and the classifier adds nothing. Enable the classifier only for deliverable kinds where section 4.3 says the basis exists, and report how many table rows had a decision basis.

## 8. Guardrails against hiding real defects

The failure to prevent: a real, decision-bearing defect is graded Medium or Note, recorded on a list nobody reads, and ships. The 825-line scale of the run-2 follow-up markers [V] shows how easily a list becomes a place where findings stop being read.

### 8.1 Guardrails

| # | Guardrail | Mechanism | Answers |
|---|---|---|---|
| GR1 | Safety is never downgraded. | Three layers: the rule text; a code scan of every Medium and Note finding for destructive and secret vocabulary (delete, overwrite, force, token, secret, password, chmod and similar, kept in one list) that sends a hit to a second reviewer; the classifier question S in shadow mode | the seed constraint |
| GR2 | A finding without `rests_on` is invalid. A Medium or Note without `why not blocking` is invalid. | the consolidator rejects the finding and asks the reviewer again | "nothing depends on it" cannot be said silently |
| GR3 | The consumer is checked by code where it can be. | quote present; figure found inside the decision-basis sections; for a table consumer, one parse-by-position check | a reviewer inventing or hiding a consumer |
| GR4 | Unknown is not a pass. | `consumer-unknown` Medium, listed first in the offer | RC4 |
| GR5 | Consolidation cannot silently overturn a reviewer's blocking grade. | A blocking grade stands unless the code check disproves the named consumer. Otherwise the finding is `disputed` and shown first | RC2, without re-creating "highest wins" |
| GR6 | Required items are checked by code before any model judgment. | the required-section list comes from the template or acceptance criteria, not from the deliverable | a producer shrinking its own basis |
| GR7 | Final-gate sweep. | At the last gate before delivery, every open Medium is re-tested: does its flawed text or figure appear, uncorrected, in a decision-basis section of the final deliverable? If yes, it is Blocking at that gate | RC4: by then the decision basis exists, so the upstream gap closes |
| GR8 | Re-review only when a Blocking finding was fixed (as today). | unchanged | no new loop |
| GR9 | A sampled audit of non-blocking findings (8.2). | blind reviewer, measured rate | measures the error that matters |
| GR10 | Seeded-defect recall (8.3). | planted defects across the classes | catches a rule that is simply too loose |
| GR11 | A per-run override still wins. | the grading-override file mechanism run 2 used (`R2/qa/grading-override.md`) keeps working as the revert path for one run [V] | a fast manual brake |

### 8.2 Measured false-negative audit

| Element | Design |
|---|---|
| Unit | one non-blocking finding (Medium or Note) from a completed run, taken from the ledger and the reviewers' notes |
| Frame | every non-blocking row of the audit window (5 runs or 60 rows, whichever is later) |
| Strata | tier (Medium, Note); tag (`consumer-unknown`, `disputed`, none); deliverable kind; whether the reviewer's own grade was blocking and consolidation lowered it, or the reviewer said minor. Oversample the first two risk groups to about half the sample |
| Auditor | a different model class from the reviewers, blind to the reviewer's grade and the ledger tier, shown the deliverable and the finding and **no rule text**. Asked: "if this text stays, would a reader acting on the deliverable do something wrong or reach a wrong decision? Name it." A second auditor shown the old rule text is the comparison arm |
| Escape (operational) | a sampled finding escaped if (a) its flawed text or number appears uncorrected in a later deliverable's decision-basis section (a rule-free code check), or (b) the blind auditor names a concrete wrong result and a second auditor and a code check agree, or (c) a person later reports the defect as consequential |
| Sample size | with zero escapes, the 95 percent upper bound is about 3 divided by n: 5.0 percent at n = 60, 3.0 percent at n = 100, 2.0 percent at n = 150 [computed]. So n = 60 can only support a claim of "under 5 percent". A revert trigger below that is not testable at n = 60 |
| Report | escapes over n with a Wilson 95 percent interval, per stratum and pooled, per window and rolling |
| Safety | every sampled finding also goes through the GR1 vocabulary scan. Any safety-class escape is a revert trigger regardless of rate |
| Who | not the reviewer family, not the classifier. The owner reviews the sample list and every escape |

### 8.3 Seeded-defect recall

Plant known defects in a held-out deliverable, across four classes: decision-bearing false claim, missing required section, safety risk, and cosmetic. Review it under the old rule and the new rule with the same reviewers. Required: safety recall equals the old rule's; recall of decision-bearing and missing items stays within 5 points of the old rule's; the share of cosmetic items that block falls. A candidate existing set is the 44-defect spec ledger (20 blocking, 19 medium, 5 minor), validated by 20 agents, named in a run-2 scope file [E: seen as text at `R2/research/scope/06-brainstorm-process-redesign.md:242`; the artifact itself is [U]]. That file also says the whole #346 series was tuned on it, so use it as a sanity check and plant fresh defects for the real test.

### 8.4 Stage 0b: a retrospective escape test I can already specify

Run 2 gives one rule-free check today. Take a random sample of de-duplicated minors from Gates 2 to 5 and the final validation (the checks that ran under the override), and for each test by code whether its flawed text or figure appears uncorrected in `R2/RESEARCH-REPORT-review-panel-unification-run2.md`. The count of hits over n, with its interval, is a first escape estimate that does not depend on the same rule that graded the findings. Limit: the report was itself produced under the override, so a minor that was corrected anyway cannot be told apart from one that never mattered. State that in the result.

## 9. One source of truth and which primitives keep their own scale

### 9.1 Where the shared rule lives

| Option | Install path | Mirrors | Verdict |
|---|---|---|---|
| 1. `src/superclaude/core/REVIEW-SEVERITY.md` | `~/.claude/REVIEW-SEVERITY.md`. `install_core_files` globs `core/*.md` (`install_core.py:58` [V]); a new name is copied even on an existing install without `--force` (line 70 skips only files that already exist [V]). No installer change. Adding the name to `KNOWN_CORE_FILES` (`install_core.py:14-29` [V]) only affects the installed-files listing. | the project `.claude/` is not synced for `core/` and the plugin tree is hand-maintained [E: Makefile and build script, not re-read by me] | **Recommended** |
| 2. `src/superclaude/rules/prompts/review-severity.md` | `~/.claude/rules/prompts/`, and shipped to plugin users by the build [E] | precedent: `document_review_loop_prompts.md` is identical in `src` and the plugin [E] | Good for plugin reach; a second copy to keep in step |
| 3. Keep the long text in `pragmatic.md` | already installed | none | Rejected: an output style loads into every session, so the tiers, ledger format and examples would cost tokens everywhere |

Consumers name the installed path `~/.claude/REVIEW-SEVERITY.md` and never a `src/superclaude/...` path (project `CLAUDE.md` rule [V]). The two plugin-reachable files (`spec-panel.md` and the review-loop prompts) are the only rule carriers a plugin-only install gets today [E]; they keep the inline block (9.2) and name both surfaces. I recommend no plugin mirror of the long document in version 1 [J].

### 9.2 Inline core block plus a two-way drift test

A pointer alone depends on a reviewer choosing to read a file. The present design works because the sentences are inline: the test pins S1 to S3 verbatim in 10 files [E: `test_review_severity_rule.py`, `S1_S3_FILES`]. So:

- The shared document holds the long text: tiers, examples, ledger format, the offer. It also holds one marked block, the paragraph in section 4.1.
- Every consumer carries that block inline, word for word, plus one line pointing at the shared document.
- A test extracts the block from the shared document and checks it is present in every file of a manifest (the 11 files of section 10.1 plus the variants in 10.2).
- A second, reverse test scans for the block's opening phrase and for the old phrase `Grade every review finding as blocking or minor` across the tracked `src` and `plugins` trees and fails when a file carries either but is not in the manifest. Today's test uses a fixed list, so a new copy cannot be detected [E: `S1_S3_FILES`; the reverse scan is my requirement].
- No `src/superclaude` string appears in the shared document, as a test asserts for other installed documents [E: section 4.5 of `rule-copies-and-tests.md`].

### 9.3 Primitives that keep their own scale, and how each maps

| Primitive | Keeps | Maps to the shared rule | Change |
|---|---|---|---|
| `/sc:implement` `refs/qa.md` | its four checklist answers and parent-side derivation (`qa.md:35-52` [V]; identical in `src` and `~/.claude` [V: `cmp`]) | `ac-outcome-missing` is Missing; `harmful-effect` is Safety; `quoted-constraint-breach` is Decision (quoted constraints belong to the decision basis); `false-claim` blocks any false claim in delivered text or code and has no "rests on" qualifier | **None in v1.** It already derives severity by rule and it covers code, where a false claim in a delivered file can break a caller. A "rests on" qualifier on `false-claim` is an owner decision (D8). |
| spec-panel (`spec-panel.md:259`) | CRITICAL, MAJOR, MINOR and the Medium tier | the MAJOR test ("names a concrete wrong outcome an implementer would produce") is the Decision condition in other words | "CRITICAL is blocking" with no consequence test, and a dimensional mismatch that is always CRITICAL (`spec-panel.md:372` [E]), are broader than the rule; narrow them to the three conditions. The stoprule rubric is frozen: "a change is a new version" (`rubric.md:1` [V]), and those variants exist only under `~/.claude/` [V], so aligning them is a separate decision (D10). |
| `cli/review/card_convert.py` | its word translator (`important` and `medium` map to non-blocking, line 82 [V]) | none: the reviewer's word decides the Boolean | No code change. Document that `rf-qa.md:111` treats IMPORTANT as blocking [V] and that the new rule makes labels information only. |
| reflect deviation taxonomy | Authorized, Necessary, Drift, Regression | Regression contradicts an acceptance criterion: Decision. Drift blocks promotion today (`sc-reflect-protocol/SKILL.md:1540` [V]) | Keep in v1. Drift's default remediation is already an authorize-or-revert question to the user [E]; run 2 had no reflect evidence. A Drift with no decision basis becoming a follow-up is owner decision D6. |
| tasklist protocol | High, Medium, Low | `sc-tasklist-protocol/SKILL.md:1614` makes "High or Medium (blocking)" halt the skill [V]. The same word means "never fails a review" in `pragmatic.md:230` [V] | Align Medium to non-blocking, or rename it. No run evidence on tasklist; decide with the program's tasklist data (D7). |
| rf-qa lens scale (CRITICAL, IMPORTANT, MINOR) | the labels, as information | `pragmatic.md:229` ("CRITICAL and IMPORTANT are blocking") is replaced by "the label is information, the rule decides" | Removes the S5 sentence in the 7 files that carry it [E]; tests pin it (section 11). |
| PR severity router, roadmap structural checkers, audit wiring gate, adversarial invariant probe | their own tiers | none | Stay: code-assigned or a debate gate, not a review loop [E]. |

## 10. Files and primitives that would change

All paths are under `src/superclaude/` unless stated. This is a list for the `/sc:workflow` plan, not an edit list. Because far more than five files change, a written plan must exist before any edit.

### 10.1 The 11 files that carry the definition

Pattern: `Grade every review finding as blocking or minor`. Grep over `src/superclaude`: 11 files, 11 matches [V]. Lines below are from that Grep.

| File | Line | Group |
|---|---|---|
| `output-styles/pragmatic.md` | 225 | output style; reaches every subagent. Also lines 221 (reviewer hunting brief) to 231 [V: Read] |
| `agents/rf-qa.md` | 108 | QA agent |
| `agents/rf-qa-qualitative.md` | 108 | QA agent |
| `templates/documents/agent_template_qa.md` | 161 | template |
| `templates/documents/skill_template.md` | 828 | template |
| `templates/workflow/01_mdtm_template_generic_task.md` | 644 | template |
| `templates/workflow/02_mdtm_template_complex_task.md` | 655 | template |
| `rules/prompts/automated_qa_workflow_qa_prompt.md` | 11 | QA prompt |
| `rules/prompts/doc_code_analyst_qa_prompt.md` | 27 | QA prompt |
| `rules/prompts/documentation_expert_qa_prompt.md` | 28 | QA prompt |
| `rules/prompts/recruiting_expert_qa_prompt.md` | 27 | QA prompt |

The "21 files, 109 occurrences" figure: the issue's component table lists 19 paths plus `spec-panel.md` and `card_convert.py`, which is 21 paths; 8 of the 19 carry no definition sentence; no pattern gives 109 [E: `rule-copies-and-tests.md` section 1.1 and `draft-notes.md`]. I tried only the definition pattern and got 11 [V]. The code wins: 11.

### 10.2 Variants and carriers of the Medium mechanism

| File | What it carries | Pattern and count |
|---|---|---|
| `commands/spec-panel.md` | own scale; Review Loop bullets at lines 259 to 261 [V]; FR-8 at 332 [E] | `follow-up candidates`: 3 matches |
| `rules/prompts/document_review_loop_prompts.md` | reviewer briefs; Medium wording at 31, 32, 48 [E] | `follow-up candidates`: 3 matches |
| `output-styles/pragmatic.md` | Medium and the spec-panel scale at 230 to 231 [V] | `follow-up candidates`: 1 match |
| `cli/review/card_convert.py` | word translator, lines 71 to 83 [V] | no change |

Across `src/superclaude`, `follow-up candidates` matches 7 times in 3 files [V: Grep count]. The plugin copies of the first two files exist [E]; `spec-panel.md` differs between `src` and the plugin [E].

### 10.3 Loop and consolidation text (the cap and fix-cycle family)

A loose pattern, `2 fix cycles`, matches 22 files and 139 times [E]; most of these carry the cap, not the definition. Those that need an edit because they say who counts, merges or escalates:

| Group | Files and lines | Edit |
|---|---|---|
| Task skill | `skills/task/SKILL.md`: 252 (merge, "highest severity") [V], 254 (fix agent) [V], 258 (halt at the cap) [V], 361 (Follow-Up Items) [V], 372 [E] | L1, L2, L3, ledger |
| QA agents | `agents/rf-qa.md` 398, 402 to 415, 549 [E]; `agents/rf-qa-qualitative.md` 110, 809, 994 [E]; `agents/rf-task-builder.md` 383 to 389, 415 to 421 [E] | cap counts Blocking only; fix-step checks |
| Builders and researchers | `skills/task-builder/SKILL.md` 875 [E]; `skills/tech-research/SKILL.md` 488 to 490, 517 to 519, 555, 562 [E]; `skills/roadmap`, `readme`, `tech-reference`, `operational-guide` cap lines [E] | point at the shared rule; consumer line (L4) in the task builder |
| Tasklist | `skills/sc-tasklist-protocol/SKILL.md` 1439, 1610, 1614 [V] | align "Medium (blocking)" (D7) |
| Reflect | `skills/sc-reflect-protocol/SKILL.md` 1540 [V] | only if D6 says so |
| Routing doc | `core/HOW-WE-WORK.md` 65 [E] | the level text names the cap; check wording |

### 10.4 New files and mirrors

| Item | Note |
|---|---|
| `core/REVIEW-SEVERITY.md` | the shared document (9.1) |
| a classifier package, a question module, a thresholds config, a judge interface | location is a plan decision; code, so it is outside the "requirements only" boundary of this spec |
| the finding-grader agent in `agents/` | today installed only [V]; needed if the LLM judge builds on it (D10) |
| a post-fix mechanical-check helper (L2) | the checks that exist today are ad hoc [E]; the helper is new |
| `plugins/superclaude/` twins of `spec-panel.md` and the review-loop prompts | hand-maintained; the plugin tree holds none of the other 11 files [E] |
| project `.claude/` copies | made by `make sync-dev` for agents, templates, commands and skills, never staged; `core/`, `rules/`, `output-styles/` are not synced [E] |

Estimated size: about 30 to 40 source files plus 8 test modules and 2 fixtures [J].

## 11. Tests that pin the rule text, and what changes

Eight test modules pin the rule or the Medium text, plus two fixtures [E: `rule-copies-and-tests.md` section 3]. I confirmed that the nine paths below exist [V: `ls`] and that `canonical_rule_bullets()` is defined at `tests/skills/test_review_severity_rule.py:78-96` and imported by three test files [V: Grep] (this file, `test_review_severity_mapping.py` and `test_implement_severity_static.py`).

| Test module | What it pins [E unless marked] | Breaks if | Change |
|---|---|---|---|
| `tests/skills/test_review_severity_rule.py` | five bullets after the binary-verdict bullet of `pragmatic.md` [V: 66 to 96]; S1 to S3 verbatim in 10 files; S5 in 6; two edit tables of 161 and 139 rows; banned phrases | any S1 to S5 bullet is reworded or moved; a copy differs; an `old`/`new` row no longer holds | rewrite around the shared block (9.2); regenerate or retire the two edit-table fixtures |
| `tests/skills/test_review_severity_mapping.py` | spec-panel bullets 2 and 3 and the `pragmatic.md` Medium bullets, including "asks the user once per loop whether to open an issue" | the Medium wording, the cadence (D2) or the position after S5 changes | update literals; add ledger and offer pins |
| `tests/skills/test_implement_severity_static.py` | `pragmatic.md` S2 and S4 exact strings; the rest pins `qa.md` | S2 or S4 is reworded | keep S2 and S4 text or update the two literals; `qa.md` pins stay |
| `tests/skills/test_review_loop_extension.py` | `at most 2 fix cycles (3 reviews)` in the spec-panel cap bullet | the cap bullet changes | cap stays; no change expected |
| `tests/skills/test_review_prompt_overrides.py` | brief lint and the zero-finding sentences | a pinned sentence is removed when text is consolidated | keep those sentences |
| `tests/audit/test_nfr_conv_9_zero_trust.py` | byte-exact PASS and FAIL bullets in `rf-qa.md` and its `.claude` mirror | those bullets are reworded | keep, or update both together |
| `tests/audit/test_severity_floor_unweakened.py` | a SHA-256 of rf-qa-qualitative's `## Critical Rules` block; Rule 6 never softened | any line in that block changes | the severity section is at lines 106 to 111, ahead of the later `QA Phase` headings [V: heading list]; whether it sits inside the hashed block is [U]. Re-pin only if the Critical Rules block is edited |
| `tests/audit/test_dnsp_all_agents_fail_bypass.py` | a hash of the `rf-team-lead` fix-cycle line | that line changes | no change unless the cap text moves |

New tests the plan must add:

| # | Test | Pins |
|---|---|---|
| T1 | two-way drift test | block present in each manifest file; no unregistered carrier (9.2) |
| T2 | truth-table property tests | one verdict per combination; monotone on N, U, Y; an explicit UNSET rule; no answer lowers a verdict made BLOCKING by S, M or C |
| T3 | ledger fixture | required columns; no Medium row without `why not blocking`; de-duplication key |
| T4 | reviewer template pin | `rests_on` and `why not blocking` appear in each reviewer brief |
| T5 | consolidation pin | the phrase "Preserve the highest severity rating" is gone from the task skill |
| T6 | unattended pin | the unattended text says "records only" and lists the ledger in `artifacts` |
| T7 | classifier fixture replay | a fixture judge reproduces verdicts; hostile quoted instructions do not change a verdict |
| T8 | shadow default | gating is off by default |
| T9 | no `src/superclaude` path in the shared document or any consumer line | as the other installed-text tests do |

## 12. Rollout stages

Each stage has an entry, an exit and a rollback. No stage starts before the previous exit is met and the owner has seen the numbers.

| Stage | What happens | Exit criteria | Rollback |
|---|---|---|---|
| 0. Measure offline (this program) | 0a: the scored table and five classifier runs. 0b: the retrospective escape test on run 2 (8.4). 0c: three blind agents that did not write the rule re-grade the table under the old text and the new text, paired. | A written result: how many old-blocking rows become non-blocking, the confusion matrix, an escape estimate with its interval. A go or no-go for stage 1. | nothing changed |
| 1. Shadow and ledger, rule unchanged | The task skill and tech-research gates write the ledger and show the offer. Reviewers keep the old definition but must also emit `rests_on`. The classifier runs in shadow mode. This gives paired data (old label against the `rests_on` class) before `rests_on` carries any rule. | At least 5 runs; ledger volume known; the offer answered; shadow agreement reported; zero safety misses in shadow; share of `consumer-unknown` known | stop writing the ledger; harmless |
| 2. Switch the two reach points | The shared document; `pragmatic.md`, `rf-qa.md` and `rf-qa-qualitative.md` carry the block; L1, L2 and L3 take effect. A per-run override file stays as the brake. | One audit window (8.2) with the revert triggers in section 13 not tripped; seeded recall (8.3) met | restore the old block from git; keep the ledger |
| 3. Other copies | Templates, QA prompts, builders, researchers, spec-panel narrowing; the two-way drift test goes live | Drift test green; a second audit window clear | per-file restore |
| 4. Primitives with their own scale | Tasklist Medium, reflect Drift, the `qa.md` qualifier, stoprule alignment, and any classifier gating | Each only with its own data and an owner decision (D4 to D8, D10). Classifier gating only after two consecutive clear audit windows | per primitive |

Why stage 1 comes before stage 2: the whole design rests on reviewers being able to name a consumer honestly. Stage 1 measures that while the old definition still decides, so a failure costs nothing.

## 13. Metrics, measurement plan and revert triggers

### 13.1 Metrics

| # | Metric | Definition | Baseline source | Direction |
|---|---|---|---|---|
| M1 | Blocking findings per gate | F_0 under the rule in force | stage 1 paired data. Run-2 reference: Gate 1 11 (old rule), Gate 2 23 reviewer-level and 8 consolidated, Gate 3 2 [V] | down |
| M2 | Fix cycles and third reviews per gate | count | stage 1 | down |
| M3 | Gate wall-clock | from the run's own logs. Not from cycle-control headers, which are not clock times [V] | stage 1 | down |
| M4 | Escape rate | escapes over n in the audit, with a Wilson interval (8.2) | none; the audit creates it | at or below the trigger |
| M5 | Seeded-defect recall | per class, new rule against old rule (8.3) | the old rule, same planted set | not below the old rule's |
| M6 | `consumer-unknown` share of Medium findings | count | stage 1 | down over time |
| M7 | Ledger size and offer outcome | rows per run; share of offers answered; filed, dismissed, ignored | stage 1 | answered, not ignored |
| M8 | `disputed` share | findings where reviewers disagree and the evidence cannot decide | stage 1 | down |
| M9 | Fix-induced findings per fix pass | `origin: fix-induced` count over fix passes | Gate 1 of run 2: 2 findings in 1 fix pass [V] | down |
| M10 | Classifier agreement, kappa, recall on validated blockers, flip rate, S misses | section 7.6 | the scored table | reported, not gated |

The owner's 35 percent score target is not a metric and gates nothing.

### 13.2 Revert triggers

A revert means: restore the previous block for the stage in force and go back to the stage before. Each trigger is stated with what it can actually detect.

| # | Trigger | Detects | Note on power |
|---|---|---|---|
| RT1 | Any safety-class escape in the audit or the seeded set | a Safety finding graded Medium or Note | zero tolerance; needs no sample size |
| RT2 | In an audit window, the 95 percent Wilson lower bound on the escape rate exceeds 2 percent | a rate that is confidently above 2 percent | at n = 60 this is 4 or more escapes (3 of 60 gives a lower bound of about 1.7 percent; 4 of 60 about 2.6 percent) [computed]. Two escapes in a window is a yellow flag: the owner reviews each one |
| RT3 | Seeded recall of decision-bearing or missing items falls more than 5 points below the old rule, or safety recall falls below it | a rule that is simply too loose | the planted set must be large enough to see 5 points; size it in the plan |
| RT4 | The owner reports a decision-bearing defect that shipped from the ledger | escape type (c) | counts as an escape in M4 |
| RT5 | After 5 runs under stage 2, M1 is not at least 25 percent lower than stage 1 | no benefit | a stop-and-investigate trigger, not an automatic revert, and not tied to the 35 percent target |
| RT6 | M9 is not lower than baseline | L2 is not working | fix L2; the rule can stay |
| RT7 | M6 exceeds 40 percent of Medium findings | the decision basis is not being supplied | redesign L4 and the consumer line; the 40 percent is a placeholder to set from stage 1 |
| RT8 | The offer is ignored in 3 consecutive runs | ledger rot | redesign the offer; not a rule revert |

RT2's wording matters. A rule such as "revert if the escape rate exceeds 2 percent" cannot be tested at n = 60, because 0 escapes in 60 only supports "under 5 percent". Triggers are therefore stated as interval bounds, and windows pool runs until the sample supports the claim.

## 14. Risks

| # | Risk | Evidence | Mitigation |
|---|---|---|---|
| R1 | Reviewers answer "nothing rests on it" too easily; the test moves the judgment, it does not remove it. | case 1 and case 7 in section 5 | GR2, GR3, GR7, the audit samples non-blocking findings |
| R2 | The decision basis does not exist at upstream gates, so most findings become `consumer-unknown` Medium and the loosening is really a loosening of everything. | RC4; section 4.3 table | L4 consumer line; M6 and RT7 watch it; GR7 re-tests Medium findings at the final gate |
| R3 | A producer shrinks its own decision basis to avoid blockers. | option A in 4.3 | GR6: required items come from the template or acceptance criteria |
| R4 | Ledger rot: a list nobody reads. | 838 markers and no consolidated list in run 2 [V] | one offer per run, counts plus five rows, M7, RT8 |
| R5 | An unattended run records the ledger and the coordinator never opens it. | a ledger listed in `artifacts` is not read automatically [E: `WORKER-CONTRACT.md` reading rule] | the coordinator rules must name the ledger count as a thing to read; part of the plan |
| R6 | The classifier lends authority to a downgrade. | a number looks like a measurement | band not number until calibrated; shadow; one-directional gating (7.5) |
| R7 | Privacy, availability and cost of Jev. | `legal.md` zero data retention only for enterprise [E]; no key [E] | decision D3; the judge chain with a fallback; classifier advisory so an outage costs nothing |
| R8 | Over-fitting the classifier to 30 to 40 rows; circular rubric. | section 7.6 | held-out half; independent scoring rubric; contested rows reported apart |
| R9 | Test churn is large: the S1 to S5 pins, 161 plus 139 edit-table rows, byte-exact bullets in two audit tests. | [E: section 11 table] | stage the work; move pins to the shared block; retire the edit tables deliberately |
| R10 | Install drift: an existing install keeps old copies of changed files unless run with `--force` or `update`, while a new core file is copied. A machine can hold the new shared document and an old `pragmatic.md`. | `install_core.py:70` skips existing files [V]; stale `pragmatic.md.bak.*` under `~/.claude/output-styles/` [E] | the drift test checks the repo only; the plan must add an install-state note to the release text. Not solved by this spec |
| R11 | "Medium" stays overloaded outside this rule. | PR router Medium routes to `--fix`; tasklist Medium blocks [E, V] | a glossary line in the shared document; D7 |
| R12 | The L2 checks exist only for some structure types. | the checks used in run 2 were ad hoc scripts [E] | start with table shape, quote presence and recounts; say plainly what is not covered |
| R13 | The benefit is smaller in minutes than the issue says. | cycle 2 took about 4.5 minutes by file times [V] | argue the case on avoided wrong halts, regression risk and decision quality, not on minutes |

## 15. Owner decisions, each with a recommendation

| # | Decision | Recommendation | Why |
|---|---|---|---|
| D1 | Where does the shared rule live? | `core/REVIEW-SEVERITY.md`, with the block inline in every copy | installs with no installer change [V]; inline copies keep the rule reliable when nothing is read |
| D2 | How often is the user offered the follow-up list? | once per run, plus at any escalation halt | run 2 had six gate checks; a per-loop question would be asked six times |
| D3 | May finding text (private-fork excerpts) go to TypeSafe? Request a key and a budget? | Decide the privacy question first. Yes for the five-run experiment only if the account has zero data retention or the processing contract is accepted; else use the LLM judge only | a decision for the owner, before any key is requested [E] |
| D4 | May the classifier ever gate? | No auto-downgrade. At most one-directional: route a reviewer-Blocking finding to a person as "probably not blocking" | no person in unattended runs, so the reviewer's label stands there; hiding risk is the larger cost |
| D5 | Does a gap-list or open-question entry count as decision basis? | No. It is a list of what is unknown, not something a recommendation rests on | otherwise case 1 flips and Gate 1 findings of that kind block again |
| D6 | Does a reflect Drift with no decision basis become a follow-up? | Defer. No reflect evidence in run 2; Drift already ends in a user decision | decide after the program's own reflect data |
| D7 | Tasklist "High or Medium (blocking)": make Medium non-blocking or rename it? | Align Medium to non-blocking, after the tasklist rows of the scored table are read | the same word means "never fails" elsewhere [V] |
| D8 | Add a "rests on" qualifier to `/sc:implement` `false-claim`? | Not in v1 | it covers code, where a false claim in a delivered file can break a caller; it already derives severity by rule |
| D9 | Who supplies the decision basis? | Reviewer-named, code-checked where quotable; a consumer line from the task builder for upstream phase outputs | 4.3 options B and C, with a narrow A |
| D10 | Bring `finding-grader` and the stoprule variants into `src`, and version the rubric? | Bring `finding-grader` in only if the LLM judge builds on it. Leave the stoprule variants alone for now | they are installed only [V]; the rubric is frozen by design |
| D11 | Replace "highest severity wins" in consolidation? | Yes (L1) | RC2; a one-line change with large effect |
| D12 | Grade a form defect as Decision when a named program consumer reads it by position (the NEW-1 rule)? | Yes | it is code-checkable and it is what the run-2 override's own text says |
| D13 | Keep Note rows in the ledger or count them only? | Short rows (id, location, one line) | bounds volume; the full detail stays in the lens reports |

## 15b. Order of work (for the `/sc:workflow` plan)

1. Stage 0 measurement, including the retrospective escape test.
2. Stage 1: ledger, offer and shadow classifier on the task skill and tech-research gates.
3. The consolidation and fix-step changes L1 and L2. They help even if the rule text stays as it is, because they address RC2 and RC3.
4. The shared document and the two reach-point files (stage 2).
5. Everything else, behind the drift test.

## 16. What was verified and what was not

### 16.1 Spot checks I ran (all in this session)

| # | Claim checked | Source of the claim | Result |
|---|---|---|---|
| 1 | The definition sentence is in 11 files, 11 matches | seed brief, `rule-copies-and-tests.md` | Confirmed by Grep; file and line list in section 10.1 |
| 2 | `pragmatic.md` lines 225 to 231 hold the rule, the exemption, the label map, Medium and the spec-panel scale | enrichment | Confirmed by Read. New: line 221 also tells reviewers to hunt "false claims" |
| 3 | `follow-up candidates` is in 3 files, 7 matches | enrichment | Confirmed by Grep count |
| 4 | `spec-panel.md` Review Loop bullets at 259 to 261 and no follow-up mention in the Unattended section (455 to 465) | enrichment | Confirmed by Read |
| 5 | `rf-qa.md` lines 108 to 111 carry the rule | enrichment | Confirmed by Read |
| 6 | `qa.md` lines 35 to 54 derive severity from four answers; `src` and installed copy are identical | enrichment, `jev-uses.md` | Confirmed by Read and `cmp` |
| 7 | `install_core.py` globs `core/*.md` at line 58, skips existing files at line 70, lists 12 known core names | enrichment | Confirmed by Read |
| 8 | Tasklist treats "High or Medium (blocking)" as halting (line 1614) | enrichment | Confirmed by Grep (also 1439 and 1610) |
| 9 | Reflect promotion gate: Drift and Regression block (line 1540) | enrichment | Confirmed by Grep |
| 10 | `card_convert.py` maps `important` and `medium` to non-blocking (lines 71 to 83) | enrichment | Confirmed by Read |
| 11 | Task skill lines 252 ("highest severity"), 254, 258, 361 (Follow-Up Items) | enrichment | Confirmed by Read and Grep |
| 12 | `test_review_severity_rule.py` lines 66 to 96 define `canonical_rule_bullets()`; 9 listed test files exist; 3 test files import it | enrichment | Confirmed by Read, `ls` and Grep |
| 13 | `/sc:issue` is on the never-as-worker list (`WORKER-CONTRACT.md:23`); `issue.md` lines 9, 31, 36 to 42, 46 | enrichment | Confirmed by Grep and Read |
| 14 | `finding-grader` and the stoprule skill exist only under `~/.claude/`; the rubric text | enrichment, `jev-uses.md` | Confirmed by `ls` (no `src` copy) and Read of `rubric.md` |
| 15 | The truth-table sketch passes 4096 cases with 0 monotonicity violations | `jev-uses.md` | Confirmed by `uv run python`; but see 16.2 item 4 |
| 16 | Gate 2 F_0 = 8 from reviewer counts of 23; Gate 3 F_0 = 2, 108 minor | preamble | Confirmed in the two cycle-control files |
| 17 | NEW-1 and NEW-2 were introduced by the fix | `severity-models-and-loops.md` section 7 | Confirmed (`qa-verification-structural-phase3-c1.md:85`; fix log names both rows) |
| 18 | The five Gate 1 downgrade candidates were corrected in the final report | my own check | Confirmed at report lines 331, 1015, 3066 to 3068, 3387, 4686 |

### 16.2 Claims I found false, loose or weak in the inputs

1. **"21 files, 109 occurrences"** (preamble, issue): false as a copy count. The definition is in 11 files. The 21 is a count of listed paths, and 109 is not reproducible [V for 11; E for the origin].
2. **"Gate 1 cost about 25 minutes extra"** (issue, preamble): weak. File last-write times put cycle 2 at about 4.5 minutes and the whole Gate 1 loop after consolidation at about 22 minutes [V: `stat`; [U] as wall-clock]. The "12:23" in the cycle-control header is later than that file's last write (12:20:21), so the header times are not clock times [V].
3. **"Two table-pipe defects each failed a gate"**: loose. They failed review 2 of one gate; the gate passed at review 3 [V].
4. **"The truth table is monotone in every input"** (`jev-uses.md`): true only on the answered states. 432 of 18,432 transitions from UNSET to an answered state lower the verdict (216 on D, 108 on W, 108 on E) [V]. This is an intended rule if stated as one.
5. **"Measured effect" of the stricter rule**: a retrospective re-grade by the author of the rule, after Gate 1 had closed under the old definition [V: file times; the override text itself says Gate 1 is closed under the earlier definition]. The average-score metric moves mechanically with the grade [J].
6. **The run-2 override on NEW-1 and NEW-2** conflicts with the verifier's own evidence about a column-position read (section 2.3) [V].
7. **`jev-uses.md` recommendation 4** (share one rubric between the human 1 to 5 scoring and the Jev Score levels) makes the validation circular (section 7.6) [J].
8. **`jev-uses.md` section 3 lists ten questions**, of which four (T, F, I, G) feed no cell of its own truth table [V: its section 4 table uses S, M, C, W, E, D only].

### 16.3 Not verified

- Jev: nothing about its accuracy, calibration, price, retention terms or the absence of a key was re-checked; I did not read `docs.typesafe.ai` again. All Jev facts are [E] from `jev-uses.md`. No Jev API call, account or key request was made.
- The loop line numbers marked [E] in section 10.3 (rf-qa 398 to 415 and 549, rf-qa-qualitative, rf-task-builder, task-builder 875, tech-research, readme, roadmap) were not re-read.
- `Makefile` `sync-dev` and `verify-sync`, the plugin build script and the plugin tree contents; `install_user_setup.py` and the rest of the installer.
- Whether the value-inventory step in run 2 parses ledger tables by column position (this decides NEW-1) [U].
- Whether any recommendation in the final run-2 report rests on the 175 or 185 spawn-line figure (I found it only as a correction and an open question) [U: not a full read of a report of several thousand lines].
- The 44-defect ledger artifact named as a recall candidate; the existence of any real caller of `convert_card` outside `src`, `scripts` and `tests`; `cli/tasklist/gates.py`; whether the severity section of `rf-qa-qualitative.md` sits inside the hashed Critical Rules block.
- Every verdict in section 5 and every classification in section 2.3 is my application of a proposed rule, not a measurement, and no classifier has been run.

Status: Complete (design and requirements only; no source file, test, installed file or GitHub object was changed).
