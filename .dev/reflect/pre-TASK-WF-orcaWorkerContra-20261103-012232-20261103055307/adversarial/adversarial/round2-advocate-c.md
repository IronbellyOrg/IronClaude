# Round 2 Rebuttal: Variant C advocate (reviewer card 3, refactorer)

Citation key as in `diff-analysis.md`: `A:N`, `B:N`, `C:N` are card lines. `TL:N` is the plan. `SRC:N` is `source.md`. `qa.md:N` and `retry.md:N` are files under `~/.claude/skills/sc-implement-protocol/refs/`. `R1-A`, `R1-B`, `R1-C`, `R2-A` and `R2-B` are the earlier statements. I opened every line I cite in this round. Checks I ran in this round are marked "(run today)".

Position in one line: the verdict is FAIL with R3-F1 as the only blocking finding. B is right that TL:125 cannot be met truthfully for some hits, and that a strict Task 6 reviewer could halt the run on it. I still grade R1-F3/R3-F5 should-fix, to be fixed in the same plan revision as R3-F1, because it can be caught at only one gate and the executor can write a true answer into the slot. I concede R2-1 to minor and accept every other grade in R2-A section 3.

## 1. Responses to criticisms of Variant C

**1.1 "R3-F1 overstates certainty: C says a strict reviewer 'ends the run'"** (R1-B Weakness 3). **Conceded.** C:15-17 does say "strict", but the merged report should say "can halt", not "will halt". The halt needs one reviewer to answer yes to question 4 (qa.md:339). The grade does not change. No repair can satisfy both TL:21 and TL:90/TL:93: drop the copy and the `cmp` check at TL:93 fails, keep it and the breach stays. The ladder then ends in `ladder-end` (qa.md:280), or an adviser dispute ends in a `dispute` halt (retry.md:72, retry.md:107).

**1.2 "C under-cited its own blocker: the managed FINAL is a second gate"** (R1-A Weakness 7, diff-analysis X-002 point 7). **Conceded, as in Round 1.** TL:21 is a `## Constraints` item. The managed FINAL reads the plan's Constraints and returns `issues` when "a plan `## Constraints` item is violated" (qa.md:310), and that ends in `E-ARCHIVE-BLOCKED` (qa.md:286). I also accept B's added point: once any reviewer flags the finding, every later reviewer must mark it "resolved, open or regressed from the diff" (qa.md:333). An unchanged copy reads as `open`.

**1.3 "R3-F3 has the wrong deviation class and overstates the trap"** (R1-A Weakness 4, R1-B Weakness 5, my calibrator at C:226). **Conceded.** The class is drift for A's concrete instance: TL:112 says "at most 10" is "as written in section 2.3", but SRC:122 says "maximum of 10 inputs". The class is none for the general mechanism. I also withdraw one claim in my card. C:55-57 says Task 5's "only way out is to edit WORKER-CONTRACT.md, a file Task 5 does not own". Task 5 does not own that file, but nothing in TL:104-119 forbids Task 5 to add to it. Adding a spec phrase breaks none of Tasks 1-2's acceptance checks, which ask for presence, not exact wording (TL:45, TL:61). So a repair closes it, as R2-A section 2.3 says. The FINAL route through "a later change contradicts it" (qa.md:310) needs three things at once: a paraphrase, a plugin copy from Task 3, and a contract edit without re-copying. Should-fix.

**1.4 "R3-F6 cites the wrong line and is over-graded"** (R1-A Weakness 5, R1-B Weakness 4). **Citation conceded.** The `"### 3.14 "` to `"## 4. "` slice is at `tests/core/test_how_we_work_routing_table.py:1091`, and a second slice, `"### 3.13 "` to `"### 3.14 "`, is at line 819 (grep, run today). The ASCII test is at line 341. **The grade question is settled:** A moved R3-F6 up to should-fix (R2-A section 1.7), and B agrees (R2-B section 3).

**1.5 "R3-F4 depends on a copy the evidence argues against; fold it into R1-F5"** (R1-A Weakness 6). **Settled in my favour.** A withdrew the fold (R2-A section 1.4) because there is a route inside the run: if Task 3 adds the copy and a later task edits the contract, Task 3's `cmp` check (TL:74) fails at the end state, and the FINAL returns `issues` (qa.md:310). R3-F4 stays a standalone should-fix that matters only if Task 3 adds the copy.

**1.6 "R3-F5 under-states the edge case: leave the phase out and you breach the instruction; invent one and you write a false claim"** (R1-B Weakness 2). **Conceded.** Section 2 rules on it. I also correct my own card. C:97-99 says the scan "also matches hits in agents ... that no phase converts". That is wrong. The only agent hits are four lines in `src/superclaude/agents/learning-guide.md` (lines 3, 34, 42 and 50), where "throu**gh pr**actical" contains `gh pr` (grep, run today). They are false matches, not write verbs. B made the same correction to A (R2-B section 2.1). My counts of 40 `gh pr` hits and about 121 hit sites came from the grounding hunk's regex. B counts 109 lines with a plain regex. The count depends on the regex, and no grade depends on the count. The correction supports my fix: classify hits by path, verb and stripped line text, and scan with word boundaries (C:108-110).

**1.7 "X-004: C treats an added plugin core copy as a live option"** (diff-analysis X-004). **Kept, and now agreed.** SRC:252 excludes `plugins/superclaude/core/WORKER-CONTRACT.md` by name, so the spec expects a copy may exist. `scripts/build_superclaude_plugin.py:75` shows that core is not distributed. A and B both now say Task 3 should cite both facts (R2-A section 1.4, R2-B section 1.4).

**1.8 "R2-1 (phantom AC-0.8) is minor, not should-fix"** (R2-A and R2-B tables, against my Round 1 grade). **Conceded.** TL:19 is plan text, and B2 covers only "delivered text or code" (qa.md:50). No edit can violate a scope note about a check that does not exist, so the FINAL's Constraints check (qa.md:310) cannot fire either. Minor, class drift.

**1.9 R3-F2.** In Round 1 I said I would accept minor. Both A and B grade it should-fix, and I keep should-fix. The section 3.1 flags have cover: section 2.3 itself says "every flag section 3 lists as required" (SRC:84). The "from P1" marker (TL:58) has weaker cover, and TL:22 is a Constraint, so the FINAL can read it (qa.md:310).

## 2. Ruling on B's second blocker (R1-F3 + R3-F5, the Task 6 phase slot)

### 2.1 Can the executor meet TL:125 without inventing a phase? Not literally.

TL:125: each hit "must be either allowed by WC-9 ... or listed on an explicit allowlist in the test, with a one-line reason and the phase that converts its command." I checked the hits that have no true phase (run today):

| Hit | Why no phase converts it |
|---|---|
| `src/superclaude/commands/git.md:67` (`/sc:git commit --smart-commit`) and `:75` (`/sc:git merge feature-branch --interactive`) | `/sc:git` is never a worker and gets no `--unattended` mode (SRC:61, SRC:188, SRC:193). These lines are usage examples of the slash command, not shell git calls, but a plain `git commit` / `git merge` match finds them. |
| `src/superclaude/skills/sc-crash-recovery/SKILL.md:4` (`Bash(git stash *)` in `allowed-tools`) | No command file exists: `commands/` has `git.md`, `task.md` and `pr-submit.md`, but no `crash-recovery.md` (Glob, run today). The phrase "its command" has nothing to refer to. |
| `src/superclaude/skills/task-builder/SKILL.md:408` (`git add .dev/tasks`) and `:2237` (CLI-mode `git add -A`) | No `task-builder.md` command exists. WC-9 says the line 2237 call "is refused" (SRC:77), which is the spec's third category, "refused under `--unattended`" (SRC:305). TL:125 removes that category ("At P0 no command is refused under `--unattended` yet"). |
| pr-submit hits | A bare phase is false: pr-submit gets "no `--unattended` mode and no Phase 4 changes" (SRC:201). A conditional phase is true: "P4 only if D3 (b) is chosen" (SRC:224, SRC:234). |

For the first three groups, the only true value for the slot is "none". "The phase that converts its command" assumes that such a phase exists. So the instruction cannot be met both literally and truthfully. Would "no phase converts it" satisfy it? It fills the slot with a true value, but it names no phase. Whether that counts as compliance is up to the reviewer. **I concede B's factual claim.**

### 2.2 Does qa.md:52 make the gap a halt? It makes a halt reachable, not certain.

- qa.md:52 lets B4 fire on "an explicit task instruction", and TL:125 is one.
- The Read-back checks only that "the quoted text is byte-present in the plan Constraints or a task instruction" (qa.md:61). TL:125's text will pass.
- Task 6 creates the test, so the origin is `new` and the inherited cap does not apply (qa.md:169). Any confirmed yes is blocking (qa.md:81).
- A blocking finding fails the attempt. It does not halt by itself. A halt comes only when the ladder cannot close the finding (qa.md:280), or when the adviser disputes it because the AC is "contradictory or infeasible" (retry.md:72, retry.md:107). No repair can supply a true phase, so a strict yes that persists does end in a halt.

So the mechanism is the same as R3-F1's: one reviewer's yes, then a conflict no repair can close.

### 2.3 Why I still grade it should-fix (confidence 0.6)

B's Round 1 test says a defect is blocking when it opens a halt that no in-run repair can close. This finding passes that test. I do not think the test alone is enough to grade a plan before it runs, because any instruction that can be read strictly passes it. The grade should also weigh how plain the breach is and how many gates can catch it. On both counts this finding is clearly weaker than R3-F1.

1. **The kind of conflict differs.** In R3-F1, two plan texts order and forbid the same act. Every possible output breaches one of them (TL:21 against TL:90 and TL:93), and the diff does what TL:21 forbids in plain words: it writes a file under `skills/`. Here, one instruction assumes something that is false for some hits, and a true null value fills its slot. To answer yes, a reviewer must decide that an honest "none" is a breach, not the correct answer. That is a harder yes to give.
2. **Only one gate can catch it.** R3-F1 can be caught by the Task 4 review and by the managed FINAL. This finding can be caught only by the Task 6 reviews. The FINAL returns `issues` for an unmet AC, missing evidence, a later change that contradicts an AC, a violated plan Constraint, or a failed log (qa.md:310). A breached task instruction is not on that list. Task 6's acceptance checks (TL:128-131) never mention the phase, so the FINAL's unmet-AC route cannot fire either. B agrees (R2-B section 2.3). If the Task 6 A1 review passes, nothing else reads the slot.
3. **The executor can put the reason in the diff.** It can write each entry as "phase: none; never a worker (source.md section 4)", and keep the same reasons in `./artifacts/ac-0.9-hits.txt`, which TL:125 already requires. The reviewer receives the diff (qa.md:326). In R3-F1, nothing the executor writes can change where TL:90 puts the copy.
4. **B's "stays open" point (qa.md:333) raises the cost once the finding is triggered, not the chance that it is triggered.** It applies only after a first strict yes.

Two facts keep my confidence at 0.6. B's mechanical test is met. And the other outcome is a silent defect: an executor that invents a phase writes a false claim (B2) against the never-as-worker list that Task 1 puts in `WORKER-CONTRACT.md` (TL:45). That false claim then ships into the test that every later phase extends (SRC:306). Neither fact makes this a likely halt, but both make it a must-fix.

**Ruling:** should-fix, fixed in the same revision as R3-F1. The report records: "can halt, through the Task 6 review only". If the panel adopts B's mechanical test as its rule, the finding is blocking, and I would not contest that. The verdict (FAIL) and the work (one plan revision) are the same either way.

**Fix:** use B's five categories (R2-B section 2.3) and my keys: repo-relative path, verb and stripped line text, never line numbers (C:108-110). Scan with word boundaries. Record slash-command usage lines (`/sc:git commit`) and read-only subcommands (`git merge-base`, `gh pr view|list|checks|diff|status`) as "not a write call", so they are not counted as write-verb hits.

## 3. Final grade for every finding

I accept R2-A's section 3 table with one change: R2-1 is minor (section 1.8), as A already has it.

| Merged finding | Cards | Final grade | Class | My position |
|---|---|---|---|---|
| TL:21 against the Task 4 skill-folder copy (TL:90, TL:93) | R3-F1 | **blocking**, recorded as "can halt" | drift | Confirm. Two gates (qa.md:52/61, qa.md:310/286). Fix: C:26-28 |
| Installed-path rule missing from the Constraints | R1-F4 | should-fix, fix first | none | Confirm. No gate in the run reads repo `CLAUDE.md` (qa.md:310 reads plan Constraints); the defect ships into other projects |
| Task 6 phase slot, read-only and false-match hits, keying | R1-F3 + R3-F5 | should-fix, same revision as R3-F1, "can halt (Task 6 review only)" | drift | Confirm should-fix against B's blocking (section 2) |
| TL:22 against the Task 2 template | R3-F2 | should-fix, same revision | drift | Confirm (section 1.9) |
| "at most 10" and the quoted-phrase rule | R1-F1 + R3-F3 | should-fix | drift (instance), none (mechanism) | Confirm (section 1.3) |
| Task 8 evidence files | R1-F2 | should-fix | none | Confirm. A missing evidence file is unmet (qa.md:85), but Task 8 can save it in one repair round |
| An added plugin core copy has no sync check | R3-F4 | should-fix, applies only if Task 3 adds the copy | none | Confirm (section 1.5) |
| Routing-guide ASCII and heading-slice tests | R3-F6 | should-fix | none | Confirm, with citations at lines 341, 819 and 1091 |
| Task 3 deciding evidence | R1-F5 + R2-3 | minor | none | Confirm; cite the build-script line 75 and SRC:252 |
| Phantom AC-0.8 | R2-1 | minor | drift | Confirm (conceded from should-fix) |
| Live-plan handoff and re-staging | R2-2 + R3-F10 | minor | none | Confirm the merge |
| Hard-coded negative for `## Unattended mode` | R3-F7 | minor | none | Confirm |
| Template flags unchecked against command files | R3-F8 | minor | none | Confirm |
| Goal says "every copy" | R3-F9 | minor | none | Confirm |
| No verify-sync baseline; tests/docs and tests/unit not covered | R3-F11 | minor | none | Confirm |
| Coverage-matrix omissions | B matrix_omissions | drop; keep as an appendix note | none | Confirm |
| Task 7 environment | A self-audit; B and C calibrators | drop; note only | none | Confirm; A and B both found the paths present |

## 4. Shared assumptions A-009, A-010, A-011

- **A-009: ACCEPT (re-checked today).** `src/superclaude/cli/install_core.py:30-32` defines `install_core_files(target_path: Path = None, force: bool = False) -> Tuple[bool, str]`. That matches TL:72's keyword call and its `ok, msg` unpacking. Line 36 says the function copies all `.md` files from `src/superclaude/core/`, so the new file installs with no other change.
- **A-010: ACCEPT (re-checked today).** The merge base is `c118b5a59d365b894c5f2caa2270ec9986812934`. `git diff --numstat "$(git merge-base master HEAD)" -- src/superclaude/core/HOW-WE-WORK.md | awk '$2 != 0'` printed nothing. No task before Task 4 touches that file (TL:31-74).
- **A-011: ACCEPT, with A's and B's refinement (re-checked today).** The full SRC:246-253 pipeline printed nothing, with stage exits `0 1 1 1 1 1`. The first stage does match lines, so the scan is clean only because line 249 excludes `src/superclaude/skills/ccsession-tag/`. Any new hit in Tasks 4 or 8 can come only from this plan's edits outside the five excluded paths.

## 5. Still-contested points

| ID | My position | Confidence |
|---|---|---|
| X-001 / S-001 (verdict) | FAIL | 0.90 |
| X-002 / U-006 (R3-F1) | Blocking, recorded as "can halt"; not over-graded | 0.80 |
| C-001 (R1-F3 + R3-F5, B's second blocker) | Should-fix, fixed in the same revision as R3-F1, recorded as "can halt through the Task 6 review only". TL:125 cannot be met literally and truthfully for the git.md, crash-recovery and task-builder hits, but a true "none" fills the slot and only one gate can catch it. I would not contest blocking if the panel adopts B's mechanical test. | 0.60 |
| C-001 example hits | The agent hits are false matches (learning-guide "through practical"); my card's claim about agent hits is withdrawn. The solid hits with no phase are git.md:67/75, crash-recovery SKILL.md:4 and task-builder SKILL.md:408/2237, plus pr-submit unless the entry uses the conditional wording | 0.90 |
| X-003 / U-007 (R3-F2) | Should-fix, fixed in the same revision | 0.65 |
| U-003 (R2-1) | Minor, drift (conceded from should-fix) | 0.80 |
| C-003 (R1-F1 + R3-F3) | Should-fix; repairable inside the run; my "only way out" claim withdrawn | 0.80 |
| U-008 (R3-F4) | Standalone should-fix, applies only if Task 3 adds the copy | 0.70 |
| C-005 (R3-F6) | Should-fix; citations at lines 341, 819 and 1091 | 0.70 |
| U-001 (R1-F4) | Should-fix, fix first | 0.80 |
| A-011 | Accept; the scan is clean only because of its exclusions | 0.90 |
