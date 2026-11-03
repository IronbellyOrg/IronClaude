# Round 2 Rebuttal: Variant B advocate (reviewer card 2, qa persona)

Citation key as in `diff-analysis.md`: `A:N`, `B:N`, `C:N` are card lines. `TL:N` is the plan. `SRC:N` is `source.md`. `qa.md:N` and `retry.md:N` are files under `~/.claude/skills/sc-implement-protocol/refs/`. `R1-A`, `R1-B`, `R1-C` and `R2-A` are the earlier statements. I opened every line I cite in this round. Checks I ran in this round are marked "(run today)".

Position in one line: the verdict stays FAIL. R3-F1 is blocking. R1-F3/R3-F5 also meets the blocking test I proposed in Round 1, so I nominate it as a second blocker. It is recorded as "can halt", at lower confidence than R3-F1, because only one kind of gate can catch it. I agree with A's grade on every other finding. I correct two of A's example hits, which are false matches and not write verbs.

## 1. Responses to criticisms of Variant B

**1.1 "B:81-82 says no task instruction breaches the Constraints. TL:21 against TL:90 shows that is false."** (R1-A Weakness 1, R1-C Weakness 1, diff-analysis X-001.) **Conceded, as in Round 1.** I re-checked it today. TL:21 says "P0 edits no command, skill or agent file". TL:90 says "copy the file byte for byte to `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`". That folder holds `SKILL.md` and an existing `refs/HOW-WE-WORK.md` (listed today), so Task 4 edits an existing file inside a skill package.

**1.2 "B listed quoted-constraint-breach as a halt path but did not test TL:21 against Task 4."** (R1-C Weakness 1.) **Conceded.** The method was right and I applied it badly. Section 2 applies the same method strictly to Task 6. That is why I now nominate a finding that my own card missed.

**1.3 "B's coverage is thin: it missed the Task 6 phase slot, the 'at most 10' phrase and the installed-path rule."** (R1-C Weakness 4.) **Conceded.** All three are real, and I verified them in Round 1.

**1.4 "R2-3 is redundant: TL:69 already orders a full read of the build script."** (R1-A Weakness 2, R1-C Weakness 4, my calibrator at B:96.) **Conceded.** R2-3 merges into A's R1-F5 at minor. The useful evidence is `scripts/build_superclaude_plugin.py:75`, not my empty hunk. The empty hunk H4 belongs in the report's notes on evidence gaps, not in the finding list.

**1.5 "R2-1 is over-graded."** (R1-A Weakness 3.) **Conceded in Round 1. I keep it at minor, against C's should-fix.** TL:19 still says "AC-0.8 is a P1 check (section 7.3)", and SRC:298-306 has no AC-0.8. No gate can act on that sentence. B2 covers "delivered text or code" (qa.md:50), and plan text is not delivered. The managed FINAL returns `issues` when "a plan `## Constraints` item is violated" (qa.md:310), and no edit can violate a scope note about a check that does not exist. The class stays drift.

**1.6 "B's PASS rests on a lenient reading it never states."** (R1-C Weakness 3, diff-analysis X-001.) **Conceded.**

**1.7 "B missed Task 7's environment risk."** (My calibrator, B:99.) **Conceded.** I checked it in Round 1: both Orca paths exist, so it needs a note only.

**1.8 "B's self-audit cites a 452-line spec."** (B:100.) **Conceded.** `wc -l source.md` prints 451 (run today).

**1.9 Points that still stand.** No one disputed B's structural checks. Every pytest target that Tasks 3 and 4 name exists, and source-order execution satisfies the Depends-on graph (B:68-74). R2-2 also stands at minor, and I accept C's proposal to fold R3-F10's re-staging step into it. Its value is the handoff itself: the phase report lives in the live plan (SRC:238), AC-0.6 and AC-0.7 results must appear "in the phase report" (SRC:303-304), and Task 8 hands nothing over (TL:154).

## 2. Ruling on R1-F3 / R3-F5 (the Task 6 phase slot)

### 2.1 Can TL:125 be met for every hit? No.

TL:125 says that each hit "must be either allowed by WC-9 ... or listed on an explicit allowlist in the test, with a one-line reason and the phase that converts its command." That is a closed choice between two options, and the second option needs a phase. I grouped today's hits by file (run today; 109 matching lines across the three scan roots with a plain regex).

| Group | Files and lines (run today) | Is there a true "phase that converts its command"? |
|---|---|---|
| (a) A command on the never-as-worker list, with no phase at all | `commands/git.md:67` (`/sc:git commit --smart-commit`) and `:75` (`/sc:git merge ...`) | **No.** Section 4 commands "are never dispatched as workers and get no `--unattended` mode" (SRC:188). `/sc:git` is on the list (SRC:61, SRC:193). |
| (b) pr-submit | `commands/pr-submit.md:30` and 45 lines under `skills/sc-pr-submit-protocol/` (46 of the 109 lines) | **Only a conditional one.** P4 converts pr-submit "only if D3 (b) is chosen" (SRC:224, SRC:234). The approved text says it gets "no `--unattended` mode and no Phase 4 changes" (SRC:201). A bare "P4" is false. "P4, only if D3 (b) is adopted" is true. |
| (c) A file that no command owns | `skills/sc-crash-recovery/SKILL.md:4` (`Bash(git stash *)` in allowed-tools); `skills/task-builder/SKILL.md` (a standalone skill; WC-9 says its CLI-mode `git add -A` "is refused", SRC:77) | **No.** No command file exists for crash-recovery (Glob today: `commands/` has `task.md`, but no `crash-recovery.md` and no `task-builder.md`). For task-builder, the true category is the spec's "refused under `--unattended`" (SRC:305), which TL:125 removes ("At P0 no command is refused under `--unattended` yet"). |
| (d) Read-only lines and false matches | 26 `gh pr view\|list\|checks\|diff\|status` lines; `task-builder/SKILL.md:1087, 2169` (`git merge-base`, read-only); `agents/learning-guide.md:3, 34, 42, 50` ("throu**gh pr**actical" contains `gh pr`) | It depends. A read-only line inside a command that some phase converts (for example auggie-review, P2) has a phase. A false match has neither a write verb nor a meaningful phase. |

**Correction to R2-A section 1.3.** A says "Write verbs appear in `src/superclaude/agents/learning-guide.md`". They do not. Its four hits are the substring `gh pr` inside "through practical". The two `git merge` hits in task-builder are `git merge-base`, which is read-only. This makes the finding wider, not weaker. A scanner without word boundaries produces hits that fit neither of TL:125's two categories. The solid phase-less examples are groups (a) and (c), plus group (b) unless the entry uses the conditional wording.

### 2.2 What QA does with each choice

The executor has three options for a hit in groups (a) or (c).

1. **Write a truthful "none".** For example: "phase: none; never a worker (section 4)". A reviewer is asked "does the diff violate ... an explicit task instruction?" (qa.md:339) and can quote "with a one-line reason and the phase that converts its command" from TL:125. The Read-back checks only that "the quoted text is byte-present in the plan Constraints or a task instruction" (qa.md:61). It is. Any confirmed yes is blocking (qa.md:81). The inherited cap does not apply, because Task 6 creates the test text, so its origin is `new` (qa.md:166).
2. **Invent a phase.** That is B2, "a claim in delivered text or code is false against live source" (qa.md:50). The anchor does not even need the spec. Task 1 writes the never-as-worker list, including `/sc:git` and `/sc:pr-submit`, into `WORKER-CONTRACT.md` (TL:45). That file is live source in the same tree. SRC:201 and SRC:188 also contradict an invented phase.
3. **Add a third category.** For example: "never a worker". This leaves TL:125's "either ... or" choice, so it is the same B4 breach as option 1.

**No repair closes it.** No entry text for groups (a) and (c) is both true and gives a phase. A repair can only swap a B4 breach for a B2 false claim. If the adviser disputes the finding or the instruction, the run ends in a `dispute` halt (retry.md:72, retry.md:107, qa.md:281). Otherwise the ladder ends in `ladder-end` (qa.md:280). One point that no one has raised also applies to R3-F1: once a reviewer flags the finding, every later reviewer must mark it "resolved, open or regressed from the diff" (qa.md:333). An unchanged "none" entry reads as `open`, so a lenient re-reviewer cannot clear a finding that a strict one raised.

**Would an invented phase pass?** It passes only if no Task 6 reviewer checks the phase values against the contract or the spec. In that case the run completes and ships a false classification into the test that every later phase extends (SRC:306: "Each later phase extends the list"). The P1 plan would then build on a test that says pr-submit or git converts at some phase, which contradicts D3 (a). That is a silent defect, so it is worse than a halt.

### 2.3 Grade: second blocker, recorded as "can halt" (confidence 0.6)

In Round 1, I proposed this test: a plan defect is blocking when it opens a halt that no in-run repair can close. R1-F3/R3-F5 meets both mechanical conditions that make R3-F1 blocking. The breach is quotable, so it passes the Read-back. And no delivered text is both true and compliant. To grade R3-F1 blocking and this finding should-fix, the panel would have to weigh reviewer leniency. Under the panel's own method, reviewer leniency does not set severity: the reviewer's label is never read (qa.md:79).

A's reason for keeping it at should-fix is that a truthful "none" answers a question whose premise is false, and that SRC:305 asks only for "a reason" (R2-A section 2.5). That cover is real, and it is why my confidence is 0.6 and not higher. But it lives in the spec, not in the review input. The reviewer gets the task brief and the plan Constraints (qa.md:323-324), and nothing in either one says a hit may lack a phase. R3-F1 has better cover inside the review input: TL:24 names "their plugin copies".

Two facts pull in opposite directions, and I state both.
- **Weaker than R3-F1:** only the per-task reviews of Task 6 can catch it. The managed FINAL returns `issues` for an unmet AC, missing evidence, a later contradiction, a violated plan Constraint or a failed log (qa.md:310). A breached task instruction is not on that list. Task 6's acceptance checks (TL:128-131) never mention the phase, so B1 cannot fire either.
- **Stronger than R3-F1:** R3-F1 is one copied file. Here every phase-less entry is its own quotable breach, and with pr-submit counted as an unconditional entry, that is about half of all hits.

If the panel decides that one gate type is not enough for blocking, I accept "should-fix, must be fixed in the same revision as R3-F1". The verdict and the work are the same either way.

**Fix.** Restore the spec's categories in TL:125, and use C's keys (path, verb and stripped line text, never line numbers; C:108-110):
1. allowed by WC-9;
2. refused or deferred under `--unattended` in the phase that converts its command (name the phase);
3. never a worker (section 2.1 list, section 4, D3 (a)), with no phase;
4. no command converts this file (standalone skill or agent), with a reason;
5. read-only or a false match. Better still, scan with word boundaries and leave out read-only subcommands (`git merge-base`, `gh pr view|list|checks|diff|status`).

### 2.4 Why R3-F2 stays should-fix under the same test

TL:22 limits the contract to what sections 2.1 to 2.3 say. Task 2 must list the section 3.1 flags and mark `--report-dir` "from P1" (TL:58, AC at TL:62). For the flags, a delivered text that is both true and compliant does exist. Section 2.3 itself requires "every flag section 3 lists as required" (SRC:84), so listing those flags restates section 2.3. The section TL:22 points the reviewer to removes the conflict. Only the "from P1" label lacks that cover. It is one label in one template, and section 2.3 does carry the idea of a phase ("where the command accepts it at this phase", SRC:84). R3-F2 has the FINAL route, because TL:22 is a Constraint. Under a purely mechanical rule, I would accept blocking for the label alone. I grade it should-fix at 0.6, fixed in the same revision with C's added clause (C:46-47).

## 3. Severity for every finding (agree or dispute R2-A section 3)

| Merged finding | R2-A grade | My position | Basis |
|---|---|---|---|
| R3-F1: TL:21 against the Task 4 skill-folder write (TL:90, TL:93) | blocking | **Agree**, recorded as "can halt" | Two gate types (qa.md:52/61, qa.md:310/286); unrepairable; plus the qa.md:333 point in section 2.2 |
| R1-F4: installed-path rule missing from the Constraints | should-fix, fix first | **Agree** | Nothing in the run halts on it, and it ships broken text; A's Constraints line (A:84-85) makes it quotable |
| R1-F3 + R3-F5: Task 6 phase slot | should-fix | **Dispute: blocking, can halt (0.6)**; I accept should-fix in the same revision as a fallback | Section 2 |
| R3-F2: TL:22 against the Task 2 template | should-fix | **Agree** (0.6) | Section 2.4 |
| R1-F1 + R3-F3: "at most 10" and the quoted-phrase rule | should-fix | **Agree** | TL:104 asks for "at least one" quoted phrase, so the test can assert both "at most 10" (TL:112) and "maximum of 10 inputs" (SRC:122). A repair closes it. |
| R1-F2: Task 8 evidence files | should-fix | **Agree** | An absent evidence file is unmet (qa.md:85), but the executor can save it, so one repair round at most |
| R3-F4: no sync check if Task 3 adds a plugin core copy | should-fix, conditional | **Agree** | The route through qa.md:310 ("a later change contradicts it") exists only if the copy is added |
| R3-F6: routing-guide ASCII and heading-slice tests | should-fix | **Agree** | Test line 341 and slice line 1091; Task 4's own run catches them, which costs a repair round |
| R1-F5 + R2-3: Task 3 deciding evidence | minor | **Agree** | Section 1.4 |
| R2-1: phantom AC-0.8 | minor | **Agree** (my own finding, downgraded) | Section 1.5 |
| R2-2 + R3-F10: handoff to the live plan, re-staging | minor | **Agree** | Section 1.9 |
| R3-F7, R3-F8, R3-F9, R3-F11 | minor | **Agree** | No route to a halt; all maintainability or wording issues |
| B matrix_omissions | drop, keep as an appendix note | **Agree** | Bookkeeping only (B:61) |
| Task 7 environment | drop, note only | **Agree** | Both paths exist (checked in Round 1) |

## 4. Shared assumptions

- **A-009: ACCEPT (re-checked today).** `src/superclaude/cli/install_core.py:30-32` defines `install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`. That matches TL:72's keyword call and its `ok, msg` unpacking. Line 36 says the function copies every `.md` file in `core/`. `KNOWN_CORE_FILES` (lines 13-27) does not list `WORKER-CONTRACT.md` yet. Task 1 adds it, which is a separate requirement.
- **A-010: ACCEPT (re-checked today).** The merge base is `c118b5a59d365b894c5f2caa2270ec9986812934`. The AC-0.3 deletion check on `src/superclaude/core/HOW-WE-WORK.md` printed nothing. No task before Task 4 touches that file (TL:31-74).
- **A-011: ACCEPT, with A's refinement (re-checked today).** The full SRC:246-253 pipeline printed nothing (stage exits `0 1 1 1 1 1`). The first stage does find matches, but only in `src/superclaude/skills/ccsession-tag/` (`ccsession`, `models.py`, `README.md`), which SRC:249 excludes. The scan is clean today because of that exclusion. Any new hit can come only from this plan's edits outside the five excluded paths.

## 5. Still-contested points

| ID | My position | Confidence |
|---|---|---|
| X-001 / S-001 (verdict) | FAIL | 0.90 |
| X-002 / U-006 (R3-F1) | Blocking, recorded as "can halt"; not over-graded | 0.80 |
| C-001 (R1-F3 + R3-F5) | Second blocker, recorded as "can halt". The instruction cannot be met truthfully for groups (a) and (c). Fallback: should-fix in the same revision. | 0.60 |
| R2-A section 1.3 example hits | Corrected: the learning-guide hits and the task-builder `git merge-base` hits are false matches. The solid phase-less hits are git.md, crash-recovery, task-builder, and pr-submit unless its entry uses the conditional wording. | 0.90 |
| X-003 / U-007 (R3-F2) | Should-fix, fixed in the same revision. I would accept blocking for the "from P1" label only under a purely mechanical rule. | 0.60 |
| U-001 (R1-F4) | Should-fix, fix first | 0.80 |
| C-003 (R1-F1 + R3-F3) | Should-fix; a repair closes it inside the run | 0.80 |
| U-002 (R1-F2) | Should-fix | 0.75 |
| U-008 (R3-F4) | Should-fix, conditional on Task 3 adding the copy | 0.70 |
| C-005 (R3-F6) | Should-fix, citations at lines 341 and 1091 | 0.65 |
| U-003 (R2-1) | Minor, drift (C still says should-fix) | 0.75 |
| U-004 + U-012 (R2-2 + R3-F10) | Minor, merged | 0.75 |
| C-002 / X-004 (R1-F5 + R2-3) | Minor, A's evidence | 0.85 |
| A-011 | Accept; the scan is clean only because of its exclusions | 0.90 |
