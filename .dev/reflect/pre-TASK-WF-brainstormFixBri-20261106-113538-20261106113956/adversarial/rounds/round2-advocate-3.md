# Round 2 Advocate Statement: Variant 3 (opus:refactorer card)

Debate: sc:adversarial Mode A, Round 2 (rebuttals, last speaker). Subject: plan `TASK-WF-brainstormFixBri-20261106-113538.md` against its brief `source.md`.

Citation aliases match the other advocates: `plan` and `source` (both in `/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-P1/.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-113538/`), `spec` (`.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`), `analyze` (`src/superclaude/commands/analyze.md`), `qa` (`~/.claude/skills/sc-implement-protocol/refs/qa.md`), `lc10` (`.dev/tasks/done/TASK-WF-p1LivePlanBrief-20261105-164506/artifacts/lc10-result.md`). I re-read plan:30-159 and source:160-245 this round.

## Position

The three advocates now agree on the substance. One merged P2 remains: the plan needs acceptance criteria that compare the edited text with the brief's text in full, for Tasks 1, 2, 3 and 6 (source:34 together with the byte-for-byte verifiers at source:45 and :71). Everything else is P3 or dropped. My contribution this round is to replace R3-2's garbled mechanism with a corrected one. I ran it against the plan read-only (section 3): all five extractions are non-empty and match.

## (1) Response to criticisms of V3

| # | Criticism (who) | Verdict | Evidence |
|---|---|---|---|
| a | R3-7 is a style point. The "writes only the logs" sentence is mandated by the brief, and plan:153 already names the exception (V1 R1, V2 R1, V1 R2, V2 R2) | **Concede, drop.** | source:169 prescribes the sentence word for word ("Do not edit any source file in this task; it writes only the logs under `./artifacts/`."), and the F-13 verifier at source:171 checks that the plan "contains the quoted sentence". Any rewrite of that sentence would fail F-13. My exact_change kept the sentence and reworded only the following one. V2 is right that "Besides the logs" still leaves a literal exception inside "only", so my rewrite does not remove the tension. plan:153 already names both exceptions (`status-after.txt` and the `.claude/` copies). No gain, so I drop it. |
| b | R3-2's exact_change is garbled: it starts with `grep -cxF`, abandons it, and ends with `grep -cF -f` (V1 R1) | **Concede.** | The text mixed two mechanisms and, as written in Round 1, let the executor type the reference file itself (the self-reference flaw I conceded in Round 1). The corrected mechanism is in section 3: no pattern file, the text extracted from `./source.md` by line number, and an exact expected count. |
| c | `grep -f` with a blank line in the pattern file matches every line (V1 R1) | **Concede, and fixed by the corrected form.** | Measured: `grep -cF -- '' <plan>` prints 158, the plan's line count. The corrected AC passes one pattern with `--`, not a `-f` file, and requires the count to be exactly 1 (or 2 for Task 2). An empty or failed extraction would print the target's line count (237 for handoff-routing.md, measured with `wc -l`), not 1 or 2. So that failure is loud, not vacuous. |
| d | R3-1 was rated P2 while marked [INFERRED] (V1 R1, V2 R1) | **Conceded in Round 1; drop.** | E-1: `git status --porcelain -- .dev/tasks` shows only A and R lines plus this package's `??`. The finding's own void condition is met. |
| e | R3-5's baseline half is void (V1, V2) | **Conceded in Round 1; keep only the exit status.** | E-2: `make lint` exits 0. plan:156-157 ask the logs to "show ... exiting 0", which needs the exit status recorded. That half survives at P3. |
| f | R3-8 overgeneralises risk 4 (V1 R1, V2 R1) | **Conceded in Round 1; drop.** | source:243 and plan:137 condition the risk on a "missing or ambiguous" session file. spec:300 then fails step 5 and holds the phase short of PASS until the owner accepts in writing. The readable-but-unrecognised-call case is risk 2 (source:241). |
| g | V3 did not probe the live-check sentence's behaviour, so it says nothing on X-003 (V1 R1) | **Concede.** | V3 checked text, anchors and verification recipes, not what a checker can observe. V1's paths (analyze:97 chat-only refusal; lc10:13 reading condition 2 as reaching nested calls, against plan:128's "or in one of its subagent files") are real. V1 wins X-003. |
| h | V3's whole-text check needs explicit justification against F-7's "exactly these pins" (V2 R1) | **Hold; now accepted by V1 and V2 in Round 2.** | source:111 fixes the pin list of the F-7 AC. source:34 separately requires "a check equivalent to its verifier" for each correction, and the F-1 and F-3 verifiers are byte equality (source:45, :71). A whole-text equality criterion is a different criterion. Task 6's pin list stays exactly as F-7 has it. V2's round-2 table records the same conclusion at X-002. |
| i | R3-3 is weak because plan:66 already says "append" and E-3 enforces instructions (V2 R1) | **Partly concede; keep at P3.** | E-3 (qa:9, :17) makes the instruction reviewable, so this is not a blocker. Tasks 1, 2 and 6 each carry a `git diff --stat` shape criterion (plan:46, :61, :145) and Task 3 alone does not (plan:74-77). Adding it is one line and brings Task 3 in line with its siblings. |
| j | R3-4: Task 5 already says "the new phrase" in the singular, so only the guard matters (V2 R1) | **Concede the narrowing.** | plan:111 tests one phrase and says so. The real gaps are (1) the missing `git cat-file -e` guard, which plan:95 has, and (2) plan:90's "every paragraph-slice pin and every tier-slice pin fails" claim, which plan:95's two greps do not fully demonstrate (they cover one phrase per file, not ``only by a `/sc:analyze` call`` or `fallback_1`). Both are P3. |
| k | V2 R2-04's semantic rewording would delete F-14's guard (my R1 criticism of V2) | **Superseded; I adopt V1's form.** | V1 R2 (3).5: write the pattern with a character class, for example `only for a nested command that r[a]n`, in an explicitly regex (not `-F`) absence check. plan:45's line then no longer contains the literal string, and the guard still catches the old clause. V2 R2 agrees. |

## (2) Updated assessment of V1 and V2

**V1.** It made the decisive move on C-001 in Round 2. It extended its P2 from Task 6 alone to all four fenced-text tasks, because source:34 is a rule about what the ACs must contain and E-3 does not discharge it. It also dropped R1-F7, R1-F4 and R1-F5, which removes all of V1's void findings. Its X-003 probing (C-007, C-008, C-011) is the best behavioural analysis among the cards, and with the qualification V1 itself accepted ("plausible", not "known", false FAIL), the three are correctly placed as P3 owner notes rather than plan edits. Its character-class fix for C-004 is the best answer to that dispute. Remaining weakness: V1's Round 1 citations were brief-file offsets in several places, which V1 itself corrected. No open disagreement between V1 and V3.

**V2.** It conceded C-001 back to P2 on the source:34 basis and adopted source-derived extraction. It kept the negative pin at plan:144 and recorded it instead of removing it. Both moves close my Round 1 disputes with V2. Its per-verifier table (S-001) remains the most auditable coverage instrument and is the reason C-002 through C-006 exist at all. V2's point on qa:42 versus qa:52 and :61 is correct and sharper than V1's Round 1 reading. A character-for-character instruction is reviewable even when meaning is preserved, so the reviewer is not blind to drift. That still does not satisfy source:34, as V2 now agrees. One small open item: V2's R2-05 action restores "spec pointers and INFERRED" in addition to the INV references. I agree, because source:213 and :237 require the risks as written. plan:134-137 differ from source:240-243 in exactly those spans: "Related: INV-022", "(spec:62)", "INFERRED", "(spec:302 says only ...)", "spec:300" and "INV-023".

**Net.** The three cards are complementary, and no card is superior overall. V2 is best on literal coverage, V1 on sentence behaviour, and V3 on the verification mechanism and the consistency of task shape.

## (3) New evidence

1. **E-4 (orchestrator):** plan:38, :54, :69, :122 and :128 are byte-exact substrings of source:231, :232, :233, :223 and :219 today. So the plan copied the texts exactly. The C-001 gap is only that no AC checks that the executed edit carries the same bytes into the target files. This confirms C-001 is a coverage gap in the ACs, not a wording defect, and it keeps the severity at P2 rather than raising it.
2. **The corrected mechanism, run read-only against the plan (Bash, this round).** The reference text is extracted from `./source.md`, which no task edits:
   - Task 1: `sed -n '231s/.*with: "\(.*\)" Task 1 AC.*/\1/p' ./source.md` gives 412 characters.
   - Task 2: `sed -n '232s/.*31): "\(.*\)" `grep.*/\1/p' ./source.md` gives 261 characters.
   - Task 3: `sed -n '233s/.*bullet: "\(.*\)" Leave.*/\1/p' ./source.md` gives 361 characters.
   - Companion: `sed -n '223p' ./source.md` gives 450 characters.
   - Live-check: `sed -n '219p' ./source.md` gives 1210 characters.

   Each of the five, passed as `grep -cF -- "<text>" <plan>`, prints 1, and with `-x` also prints 1, so each matches a whole fenced line of the plan. None of the five applied texts contains a double quote, so the quote-delimited extraction is safe (source:231-233 read this round).
3. **Proposed AC wording (replaces R3-2's exact_change).**
   - Task 1: `grep -cF -- "$(sed -n '231s/.*with: "\(.*\)" Task 1 AC.*/\1/p' ./source.md)" src/superclaude/skills/sc-brainstorm-protocol/SKILL.md` prints 1.
   - Task 2: the same with the :232 extraction and `-cxF` (the bullet is a whole line) against `refs/handoff-routing.md` prints 2.
   - Task 3: the :233 extraction with `-cF` against `src/superclaude/commands/brainstorm.md` prints 1.
   - Task 6: `sed -n '223p'` and `sed -n '219p'`, each with `-cF` against the spec, each prints 1.

   These are added criteria. Every F-7 pin (plan:143-145) and every Task 1-3 pin stays. An empty extraction yields the empty pattern, which prints the target's line count (158 on the plan, 237 on handoff-routing.md), so the "prints 1 or 2" expectation fails loudly.
4. **source:169 and :171** (read this round) make R3-7's target sentence a verbatim requirement with a presence verifier, which settles C-016.
5. **source:240-243 against plan:134-137** (read this round): the dropped spans are listed in section 2 under V2. No behavioural content is lost; it is a Part 4 copy-exactness deviation (source:213, :237).

## (4) Final per-point table (all 22 points)

| Point | Winner | Reason |
|---|---|---|
| S-001 | V2 | The per-verifier F-1..F-17 table is the coverage instrument the brief implies. Caveat: it tests presence, not behaviour. |
| S-002 | V1 | Its separate unverified list labels the inference correctly; E-1 and E-2 settled two of its items. |
| C-001 | V3 | source:34 together with the byte verifiers at source:45 and :71 requires equality ACs for Tasks 1, 2, 3 and 6. Use the corrected mechanism in (3).3, with the text extracted from `./source.md`. P2. |
| C-002 | V2 | Only V2 detected the extra negative pin (plan:144 against source:111's "exactly these pins"). Keep the pin and record it as a Necessary deviation next to plan:131. |
| C-003 | V2 | A contradiction inside the brief (source:161 against the independent analyze-only pin at source:234). P3 owner note; the plan is right to keep both pins. |
| C-004 | V2 (detection), V1 (fix) | plan:45 quotes the string that source:181 says Task 1 must not contain. Fix with a regex character class; keep the guard. P3. |
| C-005 | V2 | Risks 1, 2 and 4 are paraphrased (plan:134-137 against source:240-243). Restore them verbatim. P3. |
| C-006 | V2 | The verifier rows are missing from the review's coverage matrix. A repair to the review artifact, not to the plan. P3. |
| C-007 | V1 | "only when" is a necessary condition, not a sufficient one, in the owner's text (source:219). Owner note. |
| C-008 | V1 | analyze:97: a refusal is printed in chat only. Inferred checker risk, not a reproduced false FAIL. P3. |
| C-009 | none | Not violated today (E-1); plan:33 already records the start state. |
| C-010 | V3 | Exit-status recording only; E-2 removes the baseline half. |
| C-011 | V1 | lc10:13 reads condition 2 as covering nested calls, against spec:296 and plan:128's subagent-file clause. P3 owner note. |
| C-012 | V2 | Risk 4 is conditioned on a missing or ambiguous session file and is true under spec:300. |
| C-013 | none | Void under E-1. |
| C-014 | V3 | Task 3 alone lacks a `git diff --stat` criterion (plan:74-77 against :46, :61 and :145). P3. |
| C-015 | V3 | plan:111 lacks the `git cat-file -e` guard at plan:95; plan:90 claims more than plan:95 shows. P3. |
| C-016 | none | source:169 and :171 mandate the sentence; plan:153 qualifies it. My R3-7 is dropped. |
| X-001 | V2 | Copy risk 4 verbatim, INV-023 and spec:300 included; its claim is true. |
| X-002 | V3 | Equality is required separately by source:34; F-7 (source:111) governs only the pin list. All three advocates now agree. |
| X-003 | V1 | Two real but conditional paths (missed refusal; condition-2 scope). Owner notes and a residual-risk line; no change to the sentence. |
| A-001 | none | QUALIFY. E-3 (qa:9, :17, :21) refutes the "QA checks only the AC" premise, so a paraphrase would not go unchecked. C-001 stays P2 on the independent basis of source:34. |

## (5) Final priority for every finding

The three P2 rows form one merged correction.

| Finding | Priority | Action |
|---|---|---|
| R1-F1 | P2, merge | One fix with R2-01 and R3-2, covering Tasks 1, 2, 3 and 6. |
| R1-F2 | P3 | Owner note on "only when"; the copy stays byte-exact. |
| R1-F3 | P3 | Residual-risk note: the refusal is visible only in chat (analyze:97), and `--report-dir` is matched literally. No change to the sentence. |
| R1-F4 | drop | E-1; plan:33 already records the start state. |
| R1-F5 | drop | E-2. |
| R1-F6 | P3 | Owner note on the scope of spec:296 condition 2, citing lc10:13. Top of the owner list. |
| R1-F7 | drop | spec:300 makes risk 4 true. |
| R2-01 | P2, merge | Same fix as R1-F1. |
| R2-02 | P3 | Keep the plan:144 pin and record it as a Necessary deviation next to plan:131. |
| R2-03 | P3 | Owner note on the brief contradiction (source:161 against :234). |
| R2-04 | P3 | Use the regex character class in plan:45's absence check; keep the guard. |
| R2-05 | P3 | Restore risks 1, 2 and 4 verbatim from source:240, :241 and :243. |
| R2-06 | P3 | Fix in the review's coverage matrix, not in the plan. |
| R3-1 | drop | Void under E-1. |
| R3-2 | P2, merge | The mechanism for the merged fix, in the corrected form of (3).3: a single `--` pattern extracted from `./source.md`, an exact expected count, and no `-f` file. Supersedes my Round 1 exact_change. |
| R3-3 | P3 | Add `git diff --stat -- src/superclaude/commands/brainstorm.md` shows one line changed (one insertion, one deletion) to Task 3. |
| R3-4 | P3 | Add the `git cat-file -e HEAD:src/superclaude/commands/brainstorm.md` guard to plan:111. Narrow plan:90 to the phrases plan:95 actually tests, or add the missing HEAD greps. |
| R3-5 | P3, narrowed | Record each Task 7 command's exit status in its log; no baseline machinery. |
| R3-6 | drop | Duplicate of R1-F4; void under E-1. |
| R3-7 | drop | source:169 and :171 mandate the sentence; plan:153 qualifies it. |
| R3-8 | drop | spec:300; conceded in Round 1. |

**Net result for the synthesis.** One P2: a whole-text equality AC for Tasks 1, 2, 3 and 6 with the reference text extracted from `./source.md`, added next to the existing pins. All other retained findings are P3 fidelity repairs or owner notes. Do not edit any owner-prescribed sentence.

**Limits.** I ran only the read-only extraction and grep against the plan and source. No task was executed, so the target files do not yet contain the texts, and the ACs in (3).3 were not run against them. No test, worker or session-encoding experiment was run.
