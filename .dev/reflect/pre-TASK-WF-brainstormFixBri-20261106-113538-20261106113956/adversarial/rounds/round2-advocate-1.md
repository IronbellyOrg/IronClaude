# Round 2 Advocate Statement: Variant 1 (sonnet:analyzer card)

Debate: sc:adversarial Mode A, Round 2 (rebuttals). Subject: the plan `TASK-WF-brainstormFixBri-20261106-113538.md` against its brief `source.md`, both in `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/`.

Citation aliases (same files as Round 1 and the other advocates): `plan`, `source` (the brief), `spec` (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`), `analyze` (`src/superclaude/commands/analyze.md`), `qa` (`~/.claude/skills/sc-implement-protocol/refs/qa.md`), `lc10` (`.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc10-result.md`). `alias:N` is line N, re-read in this round unless marked.

## Position

I changed my position on one issue and conceded two of my own findings. The rest stands.

1. **C-001 is P2 for all four fenced-text tasks (1, 2, 3, 6).** I moved from "P2 for Task 6, P3 elsewhere" to V3's position. The reason is source.md:34, which I had not read in Round 1.
2. **Risk 4 stays verbatim (X-001) and my R1-F7 is dropped.** V2 and V3 are right: spec:300 makes the risk true for the cases it names.
3. **X-003 stays as owner notes, not plan or sentence changes.** Both paths are real, but neither is a defect the plan introduced.
4. **The negative pins (C-002, R2-04) are kept.** C-002 is recorded as a deviation. R2-04 gets a cheaper fix than either V2 or V3 proposed.

## (1) Response to criticisms of V1

| # | Criticism (who) | Verdict | Evidence |
|---|---|---|---|
| a | R1-F1 covers Task 6 only; Tasks 1-3 carry the same instruction and verifier (V3) | **Concede.** | plan:35 and plan:66 say "copied character for character" for Tasks 1-3; F-3's verifier is "Tasks 1-3 carry the applied text byte for byte" (source:71). My Round 1 split on severity (Task 6 P2, others P3) has no basis in the brief: the verifier is the same for all four. |
| b | "Known false FAIL" is overstated; a missed refusal is a checker error, not a defect of the trigger (V2) | **Partly concede.** | analyze:97 says the refusal is "printed in chat only", so the sentence has no recorded marker for it. But the sentence at plan:128 excludes refused calls, so a correct checker reads the chat. Inferred risk, never reproduced. I withdraw "known" and keep "plausible". |
| c | R1-F7 (narrow risk 4) is void (V2, V3) | **Concede, drop.** | plan:137 already conditions the risk on "missing or ambiguous"; spec:300 says step 5 is then "not passed" and the phase is not PASS "until the owner accepts the gap in writing". The same session file drives both clauses. Risk 4 is true for the case it names. Also drop my merged R3-8. |
| d | R1-F5 lint baseline is weakened by E-2 (V3) | **Already conceded in Round 1; drop.** | E-2: `make lint` exits 0. |
| e | R1-F4 six-file clean check is not violated today (V3) | **Concede it is not a current defect; drop.** | E-1. plan:33 already saves `git status --porcelain` before any edit, and Task 7 compares against it. V3's "cheap guard" is optional; I do not carry it. |
| f | The condition-2 path (R1-F6) is not a false FAIL of the sentence (V2 implicit) | **Hold, at P3 owner note.** | See (3) below. spec:296 speaks of "the command", not of its nested calls. lc10:13 read it as covering nested calls ("Step 5 condition 2 also covers the nested calls ... sidechain False"). A checker that reuses the lc10 reading would fail a correct run in which `/sc:analyze` is called from a subagent, a case plan:128 expressly accepts and handoff-routing.md:77 makes likely (enrichment through `Task` agents). The risk is real, comes from precedent in this repo, and belongs to the spec and the brief, not to the plan. |

## (2) Updated assessment of V2 and V3

**V2 (haiku:qa).** The per-verifier table remains the best deviation-classification artifact (S-001, C-002, C-003, C-004, C-005). Two corrections to its Round 1 position:

- V2's A-001 REJECT is right about E-3 (qa:9, :15-17, :21: the per-task reviewer sees the task text and "explicit instructions") but answers the wrong question. The C-001 gap is not "will a reviewer catch a paraphrase". It is "does the plan's acceptance criteria contain 'a check equivalent to' each verifier" (source:34). F-1's verifier is "byte for byte" (source:45) and F-3's is "byte for byte" (source:71). A substring pin set (plan:143-145 for Task 6) is not equivalent to a byte comparison. V2's own qualification (Round 1: "source:34 separately asks for AC checks equivalent to each correction's verifier") grants the premise and then downgrades the severity for an unrelated reason. I place C-001 at P2.
- V2 says the equality check must not silently widen F-7's "exactly these pins" (source:111). Agreed, and the resolution is simple: F-7 governs the pin list; source:34 requires a separate verifier-equivalent check. They do not compete (X-002).

V2 is right on R2-03 (a contradiction inside the brief; P3 owner note), R2-06 (a review-artifact repair; P3), R2-05 (restore the paraphrased risks; P3), and on dropping my R1-F7.

**V3 (opus:refactorer).** V3's mechanism is the best of the three (`grep -cF -f`, all four tasks) and V3's own correction is needed and correct: the reference text must be extracted from `source.md`, not typed by the executor, or a paraphrase lands in both files and the check still passes. I adopt it. V3's consistency findings R3-3 and R3-4 are real P3 items. V3 correctly dropped R3-1 and R3-8.

Where V3 is weaker: R3-7 (rewrite plan:153) cannot remove the literal tension, because source:169 prescribes the sentence "Do not edit any source file in this task; it writes only the logs under `./artifacts/`" and plan:153 follows it with an explicit exception for `status-after.txt` and the `.claude/` copies. I drop it. V3 also calls R2-04's rewording harmful; the harm is avoidable (see R2-04 below).

## (3) New evidence

1. **source.md:34 and the verifiers at source:45 and :71** (read this round). "For each [correction], the task acceptance criteria of the new plan must contain a check equivalent to its verifier." F-1 and F-3 verifiers are byte-equality statements. This is a brief rule about AC content, so E-3 does not answer it.
2. **source.md:111 (F-7) and :34 do not conflict.** F-7's verifier says the AC "lists exactly these pins and 'two lines changed'". The byte check is a different criterion and is demanded by :34 with F-1's verifier. Task 6's AC still lists exactly the F-7 pins.
3. **The INV identifiers are external to the plan and the spec.** `INV-02` has no match in `spec`; in `plan` there is no `INV-0` string at all. source:240 and :243 carry "Related: INV-022" and "(accepted by design, INV-023)", and plan:134 and :137 drop them. This supports R2-05 as a real (P3) copy-exactness deviation (Part 4, source:213 and :237). It does not support a claim of lost behavior.
4. **spec:296 versus lc10:13 (re-read).** spec:296 says "the Skill or command call is a top-level message". lc10:13 applied it to the `/sc:adversarial` call made by the command and recorded "both with sidechain False". So there is precedent for reading condition 2 as covering nested Skill calls. plan:128 accepts a `Skill` call "in one of its subagent files". These two readings collide for a nested `/sc:analyze` made inside a subagent.
5. **R2-04 has a fix that satisfies both V2 and V3.** F-14's verifier (source:181) says Task 1 "no longer contains" the quoted string. plan:45 quotes that string inside a negative AC, so a plain grep for the string hits the AC. Writing the AC's pattern with a character class (for example `only for a nested command that r[a]n`) keeps the enforcement (V3's concern) and removes the literal (V2's concern). I checked that nothing in the plan's Task 1 text needs the literal.
6. **plan:153 versus source:169.** The sentence is mandated by the brief; the plan qualifies it in the next clause. No change.

## (4) Final per-point table (all 22 points)

| Point | Winner | Reason |
|---|---|---|
| S-001 | V2 | Per-verifier table; found C-002 to C-005. |
| S-002 | V1 | Separate unverified list; E-1 and E-2 now settle the git and lint unknowns. |
| C-001 | V3 | Whole-text check for Tasks 1, 2, 3 and 6, mandated by source:34 with the F-1 and F-3 verifiers; reference text extracted from `source.md`. V1's Task-6-only scope and V2's P3 are both superseded. |
| C-002 | V2 | Only V2 detected the added negative pin (plan:144; source:111 says "exactly these pins"). Action: keep it, record it as a Necessary deviation next to plan:131, because it is the only mechanical guard against the M-01 defect. |
| C-003 | V2 | Real contradiction in the brief (source:161 versus the independent pin at source:63). P3 owner note; the plan correctly keeps both pins. |
| C-004 | V2 | Detection is correct (plan:45 quotes the forbidden string). P3, optional, with the character-class form from (3).5. |
| C-005 | V2 | Risks 1, 2 and 4 were reworded and references dropped (plan:134-138 against source:240-244). P3: restore verbatim. |
| C-006 | V2 | Only V2 noticed the missing verifier rows. P3, a review-artifact repair, not a plan change. |
| C-007 | V1 | The "only when" necessary-versus-sufficient reading is in the owner text. Owner note; no plan change. |
| C-008 | V1 | analyze:97 supports the chat-only refusal edge case. P3, inferred risk. |
| C-009 | none | Not violated today (E-1). |
| C-010 | V3 | Exit status recording only (plan:156-157 asks the logs to show "exiting 0"); E-2 removes the baseline half. |
| C-011 | V1 | lc10:13 against spec:296 and plan:128. P3 owner note. |
| C-012 | V2 | Changed from my Round 1 "V1 slightly". Risk 4 is conditioned and true under spec:300. |
| C-013 | none | Void under E-1. |
| C-014 | V3 | Task 3 is the only wording task with no diff-shape criterion. P3. |
| C-015 | V3 | plan:111 lacks the `git cat-file -e` guard that plan:95 has. P3. |
| C-016 | none | source:169 mandates the sentence; plan:153 qualifies it at once. |
| X-001 | V2 | Changed from "V3's owner-note form". Both V2 and V3 now agree: risk 4 verbatim, with the INV-023 reference restored under R2-05. |
| X-002 | V3 | The byte check comes from source:34 and the F-1 and F-3 verifiers; F-7 governs only the pin list. |
| X-003 | V1 | Both paths are real but neither is a plan defect. Condition 2: owner note on the spec (say it applies to the command under test). Missed refusal: residual-risk note. No change to the sentence. |
| A-001 | none | QUALIFY. E-3 shows a paraphrase is not unchecked, but C-001 stands on source:34 whatever the reviewer does. |

## (5) Final priority for every finding

P3 means retain as a minor repair, clarification or owner note. Merge means fold into the named finding.

| Finding | Priority | Action |
|---|---|---|
| R1-F1 | P2 | Merge into one fix with R2-01 and R3-2. Scope: Tasks 1, 2, 3 and 6. |
| R1-F2 | P3 | Owner note on "only when"; copy stays byte-exact. |
| R1-F3 | P3 | Residual-risk note: chat-only refusal (analyze:97) and the literal `--report-dir` match. No sentence change. |
| R1-F4 | drop | Not violated (E-1); plan:33 already records the start state. |
| R1-F5 | drop | E-2. |
| R1-F6 | P3 | Owner note on spec:296 (condition 2 scope), citing lc10:13. Top of the owner list. |
| R1-F7 | drop | Conceded; spec:300 makes risk 4 true. |
| R2-01 | P2 | Merge into the R1-F1/R3-2 fix. |
| R2-02 | P3 | Keep the pin; record it as a Necessary deviation next to plan:131. |
| R2-03 | P3 | Owner note on the brief contradiction (source:161 versus :63). |
| R2-04 | P3 | Optional: rewrite plan:45's pattern with a character class; do not remove the check. |
| R2-05 | P3 | Restore risks 1, 2 and 4 verbatim from source:240, :241 and :243, including the INV references. |
| R2-06 | P3 | Fix in the review's coverage matrix, not in the plan. |
| R3-1 | drop | Void under E-1. |
| R3-2 | P2 | The mechanism for the merged fix: `grep -cF -f` against text extracted from `./source.md` (line 219 for the live-check sentence, line 223 for the companion sentence, the quoted spans in source:231-233 for Tasks 1-3), run on the edited file. |
| R3-3 | P3 | Add a `git diff --stat` criterion to Task 3. |
| R3-4 | P3 | Add the `git cat-file -e` guard to Task 5's HEAD grep and narrow its "pins fail" claim. |
| R3-5 | P3 | Exit status only: append `exit=<status>` to each Task 7 log. |
| R3-6 | drop | Merged duplicate of R1-F4; not violated (E-1). |
| R3-7 | drop | source:169 prescribes the sentence; the plan qualifies it. |
| R3-8 | drop | Conceded by V3 and by me; spec:300. |

**Net result for the synthesis.** One P2 (the merged whole-text check, V3's mechanism with extraction from the brief), the rest P3 or dropped. Do not edit the owner-prescribed sentences. The condition-2 and missed-refusal paths go to the owner as notes.

**Not done.** I ran no test, no worker and no byte comparison of the plan's fenced texts against source.md in this round; the match of plan:38, :54, :69, :122 and :128 with source.md rests on side-by-side reading by all three cards.
