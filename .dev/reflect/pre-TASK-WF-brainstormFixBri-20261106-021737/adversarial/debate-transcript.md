# Adversarial Debate Transcript

## Metadata

- Mode: A (compare existing artifacts)
- Subject: three reviewer cards (V1 = reviewer-1 analyzer, V2 = reviewer-2 qa, V3 = reviewer-3 refactorer) auditing the plan `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md`
- Depth: standard
- Rounds completed: Round 1 (advocate statements), Round 2 (rebuttals), Round 2.5 (invariant probe). Round 3 does not run at `--depth standard`.
- Convergence: 88.5% (23 of 26 scored diff points agreed)
- Threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 3
- Scored diff points (denominator): 26 (S 2 + C 14 + X 5 + A 5), from `diff-analysis.md`
- Final status: BLOCKED_BY_INVARIANTS (blocking item INV-019)

## Round 1: Advocate Statements

### Variant 1 Advocate

# Round 1 advocate statement: Variant 1 (reviewer-1, analyzer, sonnet)

Paths below are relative to the repo root unless absolute. "plan" = `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md`; "brief" = `source.md` in the same folder.

## Position summary

V1 is the best-calibrated card: it is the only one that tags what it did not verify, it finds the one defect that is reproducible with a single command (the vacuous `git show HEAD:` check), and it correctly places the F-16 wording as a documentation nit rather than a blocker. V1 is not the best card on the main defect: V3 found the listed-contract vs "listed paths exist" conflict with better evidence than V1, and V1 under-invested by tagging it INFERRED when the supporting file (`src/superclaude/commands/analyze.md`) was one Read away.

## Steelman

### Variant 2 (qa)
Strongest version: a plan audited against a brief is audited against the brief's own verifiers. F-16's verifier reads "Constraints contains the quoted line" (`source.md:201`) and F-13's reads "Task 7 contains the quoted sentence" (`source.md:171`). The plan satisfies neither literally (plan:25, plan:152), and unlike the one departure it does record (plan:131, the Task 6 placement deviation), these two are silent. A coverage audit that lets a plan substitute its own wording for a brief-mandated line, without recording it, has no way to tell a considered deviation from drift. V2 also gets the classification of C-003 right: the widening to "the logs and the status snapshot" is forced by F-2, which adds `status-after.txt`, so it is a Necessary deviation that only lacks its note. V2 is also the only card that checked whether the coverage matrix sampled all of the brief (R2-5), and it independently verified that the unsampled spans (Part 2, Part 3 preamble, Part 4) are in fact satisfied (plan:133-137 record the four residual risks).
What it gets right: the verifiers are literally unsatisfied, and the departures are unrecorded. That is accurate (`source.md:199` vs plan:25).

### Variant 3 (refactorer)
Strongest version: the plan makes a claim ("has no known false FAIL on a correct run", plan:133) and its own text refutes it. Task 1 writes "The nested contract is listed in `artifacts`, also when the call failed" (plan:38). Task 6 writes "every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`" (plan:128), and the same sentence admits the per-source timeout "can stop `/sc:analyze` before it writes". So a worker following Task 1 literally lists a path that Task 6's check then requires to exist, and a timed-out call fails a correct run. V3 backs this with `src/superclaude/commands/analyze.md:97-98` (a refused directory writes no contract, "printed in chat only") and WC-4 (`artifacts` = "every other file written", `src/superclaude/core/WORKER-CONTRACT.md:32`). V3 also found something no one else did: `domain` and `enrichment_used` are fields of brainstorm's own contract, and with `--report-dir` the worker contract is a separate file that only lists the own contract in `artifacts` (`src/superclaude/commands/brainstorm.md:154`), so the live-check sentence reads them from the wrong file (R3-3). V3 verified R3-6 correctly: the spec already names the Skill and Agent tools (`orca-worker-contract-spec.md:60,62`), so residual risk 2 overstates what is inferred.
What it gets right: the conflict is real, it is Grounded, and it contradicts a claim the plan makes.

## Strengths claimed

1. **A-1 is the only finding in the set that I reproduced as a real, mechanically vacuous check.** The Task 4 acceptance bullet gives the full path for `SKILL.md` but only "the same command for `refs/handoff-routing.md`" for the routing half (plan:95). I ran `git show HEAD:refs/handoff-routing.md 2>&1`: `fatal: path 'refs/handoff-routing.md' does not exist in 'HEAD'`. Piped into `grep -c`, that gives `0`, which is exactly the "required" outcome. So an executor who shortens the path passes the check without testing anything, and there is no pipefail. With the full path, `git show HEAD:src/superclaude/skills/sc-brainstorm-protocol/refs/handoff-routing.md | grep -c 'writes no nested directory'` also prints 0, so the two outcomes are indistinguishable in the log. Neither V2 nor V3 saw this. (Evidence: plan:95, plan:111.)
2. **A-5 / C-004 is correct about today's tree and V3's premise is not.** `git status --porcelain` today shows `A  .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/...` (four files, staged) and `?? .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/` (this package). So `git add .dev/tasks` does not flip the earlier package from `??` to `A`. V3's R3-2 P1 depends on the earlier package being untracked, which it is not. V1 said so and tagged its own claim INFERRED; V3 tagged R3-2 INFERRED too but still rated it P1.
3. **Honest tagging (S-002).** V1 marks A-2, A-3 and A-5 INFERRED where it had not read the supporting text. V2 marks every finding Grounded, including R2-3, whose "residual exposure: anything the final review or a mid-run reflect pass writes under .dev/" is an inference about executor behavior, not a quoted fact.
4. **Correct reading of F-16 (C-002).** The plan's wording ("committed to a branch the live-check worktree is built from") matches spec 7.2 (`orca-worker-contract-spec.md:282`: "the phase's edits are committed to the feature branch or a scratch branch with the user's authorization"). The brief's "commits and merges" is the weaker, less accurate sentence: the spec requires a commit to a branch, not a merge. Treating this as P1 (V2) overstates it. The plan's `plan:25` says what the spec says.
5. **A-4 / C-003 adds the literal-verifier and the factual-falseness points together.** The brief's F-13 verifier wants "it writes only the logs under `./artifacts/`" (`source.md:169-171`). The plan has a wider sentence (plan:152) that is still false because `make sync-dev` rewrites `.claude/` (plan:21 says so itself). V1 states both defects in one finding.
6. **A-7 confirms the slicing mechanics in detail** (`SKILL.md:195` is a one-line paragraph, line 196 blank, line 197 is `Quality-tier tracking`; Tier 1 heading line 16, Tier 2 line 24, Final fallback line 33; the new phrases are substrings of both write/writes forms; `_removals()` adds exactly 2 collect-only cases). That is the part of the plan that carries the tests' correctness, and V1 checked it against the files.

## Weaknesses identified

1. **V1 under-weighted the biggest finding (A-2, tagged INFERRED P2).** `src/superclaude/commands/analyze.md:97-98` was available and says the contract "is written on every outcome" only once a usable report directory exists; otherwise "the refusal is printed in chat only". V1 cited `brainstorm.md:153` (which says the same for brainstorm's own refusal) and not `analyze.md`. V3 cited `analyze.md:97-98` and WC-4 and tagged Grounded. That is better evidence, and V1's INFERRED tag understates a real conflict with plan:133. V1 also did not propose a fix.
2. **V1 missed C-007 (domain/enrichment_used live in brainstorm's own contract).** I confirmed the premise: `brainstorm.md:154` says with `--report-dir` the worker contract is separate and "lists the own contract in `artifacts`"; `SKILL.md:369-371` shows `domain` and `enrichment_used` as fields of the skill's own contract. V3 R3-3 is correct, V1 is silent.
3. **V1 did not classify its deviations.** Under the deviation-classification focus, A-4 and the F-16 note are both departures from a brief-mandated sentence; V1 calls one "false" and the other "correct" but never says Necessary deviation, Drift or Authorized expansion. V2 did classify C-003 as a necessary deviation.
4. **A-3 (no exit codes recorded) is overstated.** `make` prints `make: *** [target] Error N` on failure and the pytest log ends with a pass/fail summary, so a log without those lines does show exit 0 in practice. The format-check observation (CI runs `ruff format --check`) is valid but unverified against the plan's own scope: the plan's lint bullet says only "no new ruff finding". V1 rated this P2 with the same weight as A-1.
5. **A-6 (anchor "begins Check the contract") is a pure cosmetic point** (spec line 286 begins "4. Check the contract"; plan:125 says the line "begins" with the quoted text). V1 spent a P2 slot on it. V2 did the same (R2-4).
6. **V1 listed seven findings with zero P1.** If X-001 turns out to be a plan-blocking conflict, V1 had no P1 at all. Its blind calibrated confidence (0.73) against self-confidence 0.80 is consistent with that miss.

## Concessions

- X-001: V3 is right on substance and evidence; V1 should have read `analyze.md` and tagged it Grounded. The severity is still arguable as P2: the refusal edge needs a nested directory under an already-validated report dir to be refused (conditions at `analyze.md:97`: `.git/`, `.codegraph/`, `.claude/` skill folders, or cannot be created), which is nearly unreachable. The timeout edge is the real one, and plan:128 admits it.
- The remedy V3 proposes ("reword the skill sentence") conflicts with brief Part 4 ("copy exactly, do not paraphrase", `source.md:213`), and the plan copied Part 4 byte for byte. The defect is in the brief's mandated wording and the plan inherits it. The honest plan-level fix is to add it as a fifth residual risk or ask the owner to change the brief, not to reword unilaterally. Neither V1 nor V3 said that.
- V2 is right that the F-16 and F-13 verifiers are not literally satisfied and that no departure note exists. V1 agreed on F-16 in its `card_claims_disputed` but called it a nit.
- V3 R3-3, R3-5 and R3-6 are valid and V1 has no counterpart. I verified R3-5 (`handoff-routing.md:77`: on timeout "record quality_tier: `skipped`") and R3-6 (`spec:60,62` name "Skill tool" and "Agent tool").
- V2's R2-5 (matrix completeness) is a legitimate, low-value note that V1 did not make.

## Shared assumptions

- **A-001: QUALIFY.** I read `analyze.md:97-98`: the contract "is written on every outcome" once a usable report directory exists, and an unusable one is refused "printed in chat only". WC-4 (`WORKER-CONTRACT.md:31`) says the same ("written on every outcome") with the refusal carve-out in its last sentences, and WC-4 line 32 defines `artifacts` as "every other file written". So the assumption holds as a design rule. It does not cover a hard stop by the per-source timeout, which plan:128 itself says "can stop `/sc:analyze` before it writes". The two edge cases that make a listed path missing (refusal, kill) are both off the normal path, and refusal under a validated parent directory is close to unreachable.
- **A-002: QUALIFY.** `/sc:implement` checks "compliance with its criteria" (the plan's own acceptance bullets; `src/superclaude/core/CLAUDE.md`, level 3 row), not the brief's verifiers. A gap against a brief verifier (C-002, C-003) therefore does not block execution; it is a coverage-audit finding. A plan bullet that cannot pass on a correct run (a false FAIL, as in C-001 or C-004) does block it. So the assumption should be split by which document the verifier lives in.
- **A-003: QUALIFY.** Verified today: earlier package `001016` staged (`A`), `install_core.py` and `tests/cli/test_how_we_work_install.py` modified (` M`), this package `??`. But bullet 3 compares a snapshot before Task 1 with one after Task 7, so baseline drift before Task 1 is neutralized by design. Only writes between the two snapshots matter. One extra exposure from today's state: `.dev/reflect/pre-TASK-WF-brainstormFixBri-20261106-001016/` and `...021737/` are untracked (`??`). Any new untracked path under `.dev/reflect/` created during the run would be a new line outside the six files and the package folder.
- **A-004: ACCEPT.** Exact-substring pins are what the brief mandates (Part 4 "Task 4 pins", `source.md:232`) and they are consistent with the file's own helpers. They check presence, not placement; the paragraph and tier slices supply placement.
- **A-005: QUALIFY.** The brief does not say a plan must record a departure from a mandated sentence; this is a reviewer convention. But the plan sets its own precedent: plan:131 records its Task 6 placement deviation explicitly. So an unrecorded departure at plan:25 and plan:152 is inconsistent with the plan's own practice. That justifies a note-level finding, not a P1.

## Diff-point positions

| Point | Superior position (V1, V2, V3, none, or split) | One-line evidence |
|---|---|---|
| S-001 | none | Finding and P1 counts measure severity bias, not quality; V1 7/0, V2 5/1, V3 8/2 |
| S-002 | V1 | V1 tags unverified claims INFERRED; V2 tags all Grounded though R2-3 is an inference about executor writes |
| C-001 | V3 | `analyze.md:97-98` plus plan:38/128/133 show the conflict; V1's INFERRED tag undersells it; P2 severity is more defensible than P1 because the wording is brief-mandated (`source.md:217,229,237`) |
| C-002 | split | V2 is right that the F-16 verifier is unmet and unrecorded (`source.md:199`, plan:25); V1 is right that the plan's wording matches spec `:282` and the issue is a note, not P1 |
| C-003 | split | V2 classifies it as a Necessary deviation forced by F-2 (plan:152); V1 adds that the sentence is still false because `make sync-dev` writes `.claude/` (plan:21) |
| C-004 | V1 | `git status --porcelain` today shows the earlier package staged (`A`), so V3's premise is false; residual risk is other untracked paths |
| C-005 | V1 | Reproduced: `git show HEAD:refs/handoff-routing.md` fails with `fatal: path ... does not exist`, `grep -c` then prints the "required" 0 (plan:95) |
| C-006 | V1 | Only raiser; valid but low value because `make` and pytest print failure lines (plan:152, :155-156) |
| C-007 | V3 | `brainstorm.md:154` and `SKILL.md:369-371`: `domain` and `enrichment_used` live in the own contract, not the worker contract |
| C-008 | V3 | Only raiser; valid note, but the brief limits edits to six files (plan:21), so the plan cannot add a twin edit |
| C-009 | V3 | `handoff-routing.md:77`: on timeout the tier records `skipped`, so "this tier's quality_tier" overstates; wording is brief-mandated (`source.md:230`) |
| C-010 | V3 | `spec:60,62` already name the Skill and Agent tools, so only Task is inferred (plan:135) |
| C-011 | V3 | Task 1 says "before any edit" (plan:33) but Tasks 2, 3, 6 carry no Depends-on line (plan:49,64,115) |
| C-012 | V2 | Only V2 checked matrix coverage of Part 2, the Part 3 preamble and Part 4; low impact, plan satisfies them |
| C-013 | none | All three agree: line 286 begins "4. Check the contract"; cosmetic (V1 A-6, V2 R2-4) |
| C-014 | none | V1 A-7, V2 anchors and V3 R3-8 all confirm pins, slicing and the Part 4 byte-for-byte copy |
| X-001 | V3 | Grounded on `analyze.md:97-98`; plan:128 itself admits the timeout stop; severity P2 is more defensible than P1 |
| X-002 | V1 | Index today: earlier package `A`, so the premise of R3-2 is false; matters only if someone unstages it |
| X-003 | V1 | Plan:25 matches spec `:282` (commit to a branch, no merge); V2's P1 overstates a wording nit |
| X-004 | split | V2 classifies correctly (Necessary deviation, unrecorded); V1 correctly adds that it is also not literally true |
| X-005 | V1 | Executor outputs stay in the package; only untracked paths elsewhere (for example under `.dev/reflect/`) can trip bullet 3, and V2's exposure is unquantified |
| A-001 | QUALIFY | `analyze.md:97-98` and WC-4 support it, but plan:128 admits a timeout stop that writes no contract |
| A-002 | QUALIFY | `/sc:implement` judges the plan's own bullets, not the brief's verifiers; only unpassable plan bullets block it |
| A-003 | QUALIFY | Tree matches today (verified), but bullet 3's before/after snapshot design neutralizes pre-Task-1 drift; mid-run writes are the real exposure |
| A-004 | ACCEPT | Brief Part 4 mandates exact pins; slices supply placement |
| A-005 | QUALIFY | Reviewer convention, not a brief rule; plan:131 sets the precedent, so the omission is a note-level finding |

### Variant 2 Advocate

# Round 1 - Advocate for Variant 2 (reviewer-2, qa persona)

Evidence below was Read this turn: plan, source.md Part 2/3/4/5, `src/superclaude/commands/analyze.md:92-101`, `src/superclaude/commands/brainstorm.md:152-157`, `src/superclaude/core/WORKER-CONTRACT.md:12-16,30-32`, `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md:280-286`, `.gitignore`, `src/superclaude/skills/sc-implement-protocol/SKILL.md:9`.

## Position summary

V2 is the only card that audits the plan against the brief's own fidelity rules (source.md:34: "the task acceptance criteria of the new plan must contain a check equivalent to its verifier"; Part 4 "copy exactly"), and it correctly finds two silent departures (F-16 line, F-13 sentence). V2 is the thinnest card, though: it missed the listed-contract conflict (C-001) that V3 found, and its P1 on F-16 is overstated on substance.

## Steelman

### Variant 1 (analyzer)
Strongest version: V1 is the only card that tested the plan's checks rather than reading them. It found that Task 4's `git show HEAD:` check, written with a short path, can pass without testing anything (plan:95 says "the same command for `refs/handoff-routing.md`"), and that no exit codes are recorded (plan:152). It checked the index and showed Task 7 bullet 3 is not vacuous today because the earlier package is already staged. And it saw that the plan's F-16 wording ("a branch the live-check worktree is built from") matches spec:282, which says the edits are committed to "the feature branch or a scratch branch with the user's authorization", with no merge step. That is right: I read spec:282 and it names no merge.
Critique: (a) A-2 (the listed-contract conflict) is filed P2 INFERRED although `analyze.md:98` ("written on every outcome") and `analyze.md:97` (refused directory: "printed in chat only") are directly on disk, and plan:133 states "no known false FAIL"; that is Grounded. (b) V1 calls the F-16 departure a "documentation nit" and never asks the brief's own question (source.md:34): where is the AC check equivalent to the F-16 verifier? The plan has none, and it also does not record why it departs, although it records another departure at plan:131. (c) A-1 says Task 5's check is weak because "grep -c exits 1"; the AC says "prints 0", so the exit code is irrelevant there. That half is overstated. (d) The Task 4 half of A-1 is real: a reader can fairly take "the same command" to mean the same full path, so the weakness is narrower than V1 presents.

### Variant 3 (refactorer)
Strongest version: R3-1 is the best finding on any card. Task 1 tells the worker "The nested contract is listed in `artifacts`, also when the call failed" (plan:38). Task 6 requires "every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`" without the `skipped`/refused carve-outs, which attach only to the later "required" clause (plan:128). The plan itself admits `/sc:analyze` can stop before writing (plan:128, the timeout parenthesis). A worker that follows Task 1 literally lists a contract that was never written, and the check then fails a correct run. That falsifies the plan's own claim at plan:133. R3-3 is also correct and unique: brainstorm.md:154 says that with `--report-dir` the worker contract is a separate file that only lists brainstorm's own contract, while `domain` and `enrichment_used` are fields of the own contract (brainstorm.md:65,102,156,191).
Critique: (a) R3-2 is a P1 resting on a premise V3 itself says was "not verified" (that the earlier package is untracked). The index shows it staged, so the P1 is false today. (b) V3 demands that the plan reword the skill sentence, but Part 4 (source.md:213-233) says "copy exactly, do not paraphrase". The defect is in the brief, and a rewording by the plan would be an unrecorded departure of the kind V3 ignores on F-16 and F-13. V3 is inconsistent about whether brief fidelity matters. (c) R3-4, R3-5 and R3-6 (companion sentence, "this tier's quality_tier", "Skill/Agent/Task all inferred") target sentences that Part 4 mandates verbatim (source.md:221, 230, 239). They are brief defects, not plan defects, and a plan review should say so. (d) V3 is silent on C-002/C-003, the two places where the plan really does not match the brief text.

## Strengths claimed

1. **Brief-fidelity audit with line evidence (R2-1).** Brief F-16 (source.md:199) requires the Constraints line "The edits reach the next live plan only after the owner commits and merges them; this plan does not commit." The plan carries a different sentence (plan:25). The verifier is "Constraints contains the quoted line" (source.md:201), and the plan has no equivalent AC. V1 confirms the departure; V3 never mentions it.
2. **Unrecorded-departure discipline.** The plan records one departure explicitly (plan:131, "Necessary deviation from the brief, recorded here"). Its silence on F-16 and F-13 is therefore inconsistent with its own practice, which is exactly what V2 reports.
3. **F-13 widening is forced, not careless (R2-2).** F-2 adds `status-after.txt`, so the brief's sentence "it writes only the logs under `./artifacts/`" cannot stay literal; plan:152 adds "and the status snapshot". V2 classifies it as a necessary deviation that needs recording and also notes it is still untrue because `make sync-dev` rewrites `.claude/` (plan:21 says so). V1 reaches the second point, not the first.
4. **Honest classification of R2-5.** V2 checked that the plan does satisfy Part 2/Part 4 spans and reports only a matrix-completeness defect. It does not inflate this. Source.md:34 (the "equivalent check" rule) is the preamble span the matrix never sampled, and it is the rule that gives R2-1 its force.
5. **Cheap, correct anchors.** R2-4 (step 4 line begins "4. Check the contract", spec:286) is confirmed by my Read of spec:286.

## Weaknesses identified

1. **V2 missed C-001 entirely.** This is the highest-severity item in the diff analysis. A QA card that reads plan:38 and plan:128 should have caught it; the evidence (analyze.md:97-98, plan:133) was one file away.
2. **R2-1 is P1 but should be P2.** Spec:282 requires only commit to a feature/scratch branch with the user's authorization; the brief's "commits and merges" is stronger than the spec. The plan's wording is arguably more accurate, and it still covers a P2 author on another branch, because it says a branch the worktree is built from. The real defect is unrecorded departure plus missing AC check, not a lost scenario.
3. **R2-3 is tagged Grounded but is speculation.** "Anything /sc:implement's final review or a mid-run reflect pass writes under .dev/" names no concrete file. The only support is that `.gitignore` has no rule for `.dev/reflect/` (I grepped it: no match), so such a write would appear as `??`. That is a plausible risk, not an observed one, and V1's check that executor outputs stay in the package is more specific.
4. **Short card.** Five findings, no INFERRED tags. Calibration across the three cards is better on V1 and V3, which separate checked from inferred.
5. **R2-2 says "necessary deviation" in the same breath as "departure unrecorded"; the card does not say what the plan should have written.** A fix line would have made it actionable.

## Concessions

- C-001/X-001: V3 is right. The defect exists, and plan:133's "no known false FAIL" is untrue because the plan concedes a timeout can leave no contract. I would keep it at P1 only in the narrow sense that it contradicts a stated plan claim.
- C-004/X-002: V1 is right that the P1 premise (earlier package untracked) is false today.
- C-005, C-006: V1's catches are real and V2 saw neither.
- C-007: V3 is right (brainstorm.md:154).
- F-16: V1 is right on substance (spec:282).
- V2's own P1 rating should be P2.

## Shared assumptions

- **A-001: QUALIFY.** `analyze.md:98` says the contract "is written on every outcome" and `analyze.md:97` says an unusable directory is refused with "printed in chat only"; WC-4 (WORKER-CONTRACT.md:31-32) defines `artifacts` as "every other file written". That supports the refusal edge. It does not cover a timeout kill before write, which is the plan's own carve-out (plan:128) and is not a handled "outcome" of the command. So the assumption holds for refusal and fails for the timeout path.
- **A-002: QUALIFY.** `/sc:implement` does "spec-compliance QA against that task's AC" (sc-implement-protocol SKILL.md:9). Task ACs are judged as written, so an unpassable AC blocks. But the F-16 Constraints line is in no task AC, so it will not block implement; it is a brief-fidelity matter for the pre-execution review. C-002 is therefore a recording/coverage defect, not an execution blocker.
- **A-003: QUALIFY.** Task 1 snapshots state before any edit and Task 7 compares to it, so changes before Task 1 cancel. Only changes after the snapshot matter (new untracked paths such as `.dev/reflect/` output, which is not gitignored). Today's index facts are from the diff analysis, not re-run by me.
- **A-004: ACCEPT.** Exact-substring pins are what the brief mandates (source.md:232-233) and are simple to verify. The weakness V1 found is in the `git show` verification of the pins, not in the pins.
- **A-005: QUALIFY.** The brief does not state a rule that the plan must record every departure. But it does state a rule that each F-n must have an equivalent AC check (source.md:34), and the plan's own practice at plan:131 is to record departures. Silence is a gap against those two, not against a free-standing reviewer convention.

## Diff-point positions

| Point | Superior position | One-line evidence |
|---|---|---|
| S-001 | none | Counts reflect depth, not correctness; V3's two P1s are one real (R3-1) and one on a false premise (R3-2). |
| S-002 | split | V1 and V3 separate checked from inferred; V2 tags R2-3 Grounded though speculative. |
| C-001 | V3 | plan:38 vs plan:128, analyze.md:97-98, plan:133 "no known false FAIL"; the sentence itself is brief-mandated (source.md:229, 217). |
| C-002 | split | V2: departure unrecorded, no AC equivalent (source.md:34, 199, 201; plan:25); V1: plan wording matches spec:282. P2, not P1. |
| C-003 | split | V2 shows the widening is forced by F-2 (plan:152); V1 shows the wanted literal sentence is absent and sync-dev still writes `.claude/`. |
| C-004 | V1 | Earlier package is staged; V3's untracked premise is false today; V2's exposure is real but unquantified. |
| C-005 | V1 | plan:95 gives only a short path for the routing ref; empty `git show` output makes `grep -c` print 0. |
| C-006 | V1 | plan:152 saves outputs to files with no exit-code capture; the AC asks to "show" exit 0. |
| C-007 | V3 | brainstorm.md:154 says with `--report-dir` the worker contract is separate and lists the own contract; `domain` and `enrichment_used` are own-contract fields. |
| C-008 | V3 | Companion sentence is general and the installed twin gets no edit; I did not re-verify WORKER-CONTRACT.md:24, and the wording is brief-mandated (source.md:221). |
| C-009 | V3 | plan:54 says "this tier's quality_tier" for a scan that can be recorded skipped; wording is brief-mandated (source.md:230). |
| C-010 | V3 | The spec names Skill and Agent already per V3's cites (spec:60,62); the residual-risk text is brief-mandated (source.md:239). Low. |
| C-011 | V3 | Plan shows Tasks 2, 3, 6 with no Depends-on line while Task 1 says "before any edit" (plan:33). |
| C-012 | V2 | The matrix skips the Part 3 preamble (source.md:34, the equivalent-check rule); the plan itself complies. |
| C-013 | split | V1 and V2 both right: spec:286 begins "4. Check the contract". |
| C-014 | none | All three confirm pins, slices and Part 4 copying; no disagreement. |
| X-001 | V3 | The conflict exists and falsifies plan:133; P1 is defensible only as contradiction of the plan's own claim. |
| X-002 | V1 | The earlier package is staged today; V3's P1 depends on an unverified premise. |
| X-003 | split | V1 right on substance (spec:282); V2 right that it is unrecorded and lacks an AC check; neither is P1. |
| X-004 | V2 | Forced by F-2 (necessary deviation), unrecorded, and still untrue because of sync-dev (plan:21). |
| X-005 | split | V1: executor outputs stay in the package; V2: `.dev/reflect/` is not gitignored, so other writes are possible. Nobody measured it. |
| A-001 | QUALIFY | Holds for refusal (analyze.md:97-98), not for the timeout kill the plan itself names (plan:128). |
| A-002 | QUALIFY | Implement judges per-task AC (SKILL.md:9); the F-16 line is in no task AC. |
| A-003 | QUALIFY | Task 1's snapshot neutralizes earlier state; only post-snapshot changes matter. |
| A-004 | ACCEPT | Exact-substring pins are what the brief mandates (source.md:232-233). |
| A-005 | QUALIFY | Not a brief rule, but source.md:34 and the plan's own practice at plan:131 make silence a gap. |

### Variant 3 Advocate

# Round 1, Advocate 3 (Variant 3: reviewer-3 card, refactorer persona)

Focus: correctness, coverage, deviation classification. All file:line citations below were Read or grepped on disk in this round.

## Position summary (1-3 sentences)

V3 is the only card that finds two real false-FAIL paths in the live-check text (R3-1, the listed-contract conflict, and R3-3, `domain` and `enrichment_used` read from the wrong contract on a `--report-dir` run). Together they show that plan:133's "no known false FAIL on a correct run" is not established. But V3 over-tags R3-1 as Grounded P1, rests R3-2 on a premise the index disproves, and misses the two literal-verifier departures (F-13, F-16). Its weakest point is that it blames the plan for text the brief requires to be copied exactly, so the right remedy for R3-1 and R3-3 is a brief amendment by the owner, not a rewrite of the plan.

## Steelman (one block per opposing variant)

**V1 (analyzer, 0.80).** Strongest version: V1 is the best-calibrated card. It finds the same listed-contract conflict as V3 (A-2) but tags it INFERRED, which is honest, because no run has yet shown a worker listing an unwritten contract. It is the only card to find that Task 4's `git show HEAD:refs/handoff-routing.md` check passes without testing anything. That check is plan:95. With the short path, `git show` exits 128 with empty output, `grep -c` prints 0, and without pipefail the AC "prints 0" is met, so the check proves nothing (C-005). It checked the index before judging Task 7 bullet 3 (A-5), and today's index confirms it: the `...001016` package shows 3 `A` lines, so `git add .dev/tasks` flips nothing there. It also notes, correctly, that plan:25's wording matches spec:282 ("committed to the feature branch or a scratch branch with the user's authorization", no merge). The brief's "commits and merges" is therefore the less accurate sentence.
Critique: A-2 is left at P2 although plan:133 asserts in the plan's own voice that the sentence has "no known false FAIL", and a P2 live-plan author will trust that line. V1 also misses R3-3, which is a second false-FAIL path on the ordinary `--report-dir` route (brainstorm.md:153; SKILL.md:369-381). A-4's "false as written" is partly soft: plan:21 defines the `.claude/` rewrite as "output, not edits". The word "only" still makes the Task 7 sentence inaccurate, so the point stands, but at nit level.

**V2 (qa, 0.87).** Strongest version: V2 is the only card that held each Part 3 verifier against the plan text literally. It found that F-16 (source.md:199-201 vs plan:25) and F-13 (source.md:169-171 vs plan:152) are both carried non-verbatim, and that neither departure is recorded, while the plan does record its F-1/F-7 departure (plan:131). That is exactly the deviation-classification discipline the brief demands: Part 3 says "Apply all of them" and requires an equivalent check per verifier (source.md:34). R2-2 classifies the F-13 widening correctly as forced by F-2: status-after.txt is not a log, so it is a Necessary deviation, but an unrecorded one. R2-5 is a fair completeness note on the coverage matrix.
Critique: R2-1 at P1 is overstated. The substitute is more correct (spec:282). Constraints carry no acceptance bullet, and `/sc:implement` judges task ACs through a closed template it may not reword (sc-implement-protocol refs/qa.md:318). So the departure cannot block execution; it is a benign Drift to record, not a blocker. V2 is silent on C-001/X-001, the highest-severity item in the diff, and on R3-3, so its 0.87 self-confidence is not earned on correctness coverage. R2-3 names a residual false-FAIL exposure but does not size it. Managed packages keep their ledger as the sibling progress.md (implement.md:58), which removes the main candidate.

## Strengths claimed (numbered, with evidence)

1. **R3-1 is grounded on the text, and it refutes plan:133.** Task 1's applied text ends "The nested contract is listed in `artifacts`, also when the call failed." (plan:38). Task 6's sentence requires "every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`" (plan:128). The carve-outs (`skipped`, "did not refuse that directory") attach only to the later "required only when" clause, not to the "listed paths exist" clause. The same sentence admits that the timeout "can stop `/sc:analyze` before it writes" (plan:128). `/sc:analyze` refuses an unusable directory "printed in chat only" (analyze.md:97), so no contract exists. The routing ref records a timeout as `skipped` (handoff-routing.md:77). A failed call that never wrote is therefore reachable, and the skill tells the worker to list it. plan:133's "no known false FAIL" is contradicted by plan:128's own parenthesis. V1 reached the same conflict (A-2); V3 goes further in naming the specific claim it falsifies.
2. **R3-3 is a unique, grounded false-FAIL path on the ordinary route.** The diff analysis lists it as U-003. With `--report-dir` "the worker contract is a separate `<report-dir>/return-contract.yaml` that lists the own contract in `artifacts`" (brainstorm.md:153; SKILL.md:379-381). `domain` and `enrichment_used` are fields of the own contract (SKILL.md:369, 371). Spec 7.2 step 4 checks `<contract>`, the WC-4 path (spec:286). A checker that follows the sentence literally finds neither field on a `--report-dir` run. Unlike R3-1, this needs no misbehaving worker.
3. **R3-8 confirmation is the most complete.** It checks byte-for-byte copy across Tasks 1, 2, 3 and both Task 6 sentences against source.md:217, 221, 229-231. It also checks that each new phrase occurs once, so the `_removals` cases bite. It checks that the Tier 2 bullet stays in the `test_codegraph_adoption` slice and that no installed text names a `src/superclaude/` path. Plan:38, 54, 69, 122 and 128 match source.md Part 4 on re-read.
4. **Small textual accuracy findings hold.** R3-5: the routing bullet says the scan is recorded "with this tier's `quality_tier`" (plan:54), but a timeout records `skipped` (handoff-routing.md:77). R3-6: spec:62 already names "the Skill tool or the Agent tool", so only `Task` is inferred in residual risk 2 (plan:135). R3-4: WORKER-CONTRACT.md:24 is the installed twin of spec:62 and gets no matching edit; no test ties them (grep of tests/ finds no spec reference).

## Weaknesses identified (numbered, with evidence)

1. **R3-2 is wrong today.** Its premise, "if the earlier package were untracked", is false. `git status --porcelain .dev/tasks` shows `A  .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-001016/...` (3 lines), and the only `??` is this package, which the bullet exempts (plan:157). It should not have been P1. Withdrawn as a defect; at most a note conditional on A-003.
2. **R3-1 is over-tagged.** The text conflict is Grounded. The false FAIL is not: it needs a worker that lists a file it did not write, and WC-4 defines `artifacts` as "every other file written" (WORKER-CONTRACT.md:32). A worker obeying WC-4 over the skill sentence never lists an unwritten contract, and then the check's FAIL would be a true WC-4 violation. The honest tag is "Grounded conflict, INFERRED failure"; V1's INFERRED is closer.
3. **V3 blames the plan for brief-mandated text.** "The nested contract is listed in `artifacts`, also when the call failed." is in source.md:229. The live-check sentence is source.md:217. "No known false FAIL" is source.md:237. The residual risks, including the Skill/Agent/Task inference, are source.md:238-241. The routing bullet is source.md:230. All are under "copy exactly, do not paraphrase" (source.md:213). The plan copied them faithfully. V3's proposed reword of the skill sentence would itself be an unrecorded deviation from Part 4. The correct classification is a brief-level defect with plan fidelity intact, and the remedy is an owner amendment of Part 4. This applies to R3-1, R3-3, R3-5 and R3-6.
4. **R3-7 does not bite under the executor.** `/sc:implement` runs "Default sequential in source order. Parallel only when the source marks a set independent" (sc-implement-protocol SKILL.md:97). Task 1 runs first, so missing Depends-on lines on Tasks 2, 3 and 6 cannot reorder them. It is a nit for manual runs only.
5. **There is a coverage gap on V3's own focus area.** Despite a "deviation-classification" focus, V3 missed both literal-verifier departures (F-13 at plan:152, F-16 at plan:25), the `git show` vacuity (plan:95), and the step 4 anchor imprecision (plan:125 vs spec:286, "4. Check the contract").
6. **R3-4 asks for a seventh file.** Fixing the twin drift needs a WORKER-CONTRACT.md edit, which the six-file constraint forbids (plan:21; source.md:247). It is an out-of-scope note for the owner, not a plan defect.

## Concessions

- C-004/X-002 go to V1: the index disproves R3-2's premise.
- C-005 goes to V1: a real vacuous check that V3 missed.
- C-002 and C-003 go to V2 on classification: both are unrecorded departures from literal verifiers. On C-002, V1 is right on substance and severity (spec:282).
- S-002 goes to V1: its INFERRED tagging is better calibrated than V3's Grounded tag on R3-1.
- R3-7 is withdrawn to nit (SKILL.md:97). R3-2 is withdrawn.
- V3's P1 count of 2 should be at most 1 (R3-1, and even that is qualified). R3-3 deserves equal or higher priority than R3-1, because it fails on a correct worker.

## Shared assumptions (A-001 to A-005: ACCEPT/REJECT/QUALIFY + reason)

- **A-001: QUALIFY.** analyze.md:97-98 confirms it for `/sc:analyze` with a usable directory: the contract "is written on every outcome", and a refusal is "printed in chat only". WC-4 (WORKER-CONTRACT.md:31-32) generalizes it to any command. It does not hold when the caller cuts the nested call off. The brainstorm per-source timeout records `skipped` (handoff-routing.md:77), and plan:128 itself says that timeout "can stop `/sc:analyze` before it writes". "Every outcome" is the nested command's promise, not a guarantee the caller can rely on. WC-11 is not material here: it governs parallel-safe paths, not contract existence.
- **A-002: QUALIFY.** `/sc:implement` judges the plan's task ACs through a closed review template it may not reword (sc-implement-protocol refs/qa.md:318). So Task 7 bullet 3 (C-004) is judged literally. But the brief's Part 3 verifiers are not ACs. F-16 lives in Constraints, which has no AC (plan:25), and F-13's sentence is task body text, not an AC bullet (plan:152). C-002 and C-003 are therefore review-fidelity findings, not execution blockers.
- **A-003: ACCEPT.** It was verified today: 953 `A`, 3 `R`, 1 `??` under `.dev/tasks/`, and the earlier package is staged. The before/after snapshot design (plan:33, 157) makes the check independent of the baseline content, as long as no one changes the baseline during the run. Only a mid-run unstage or a new untracked path under `.dev/` breaks it.
- **A-004: ACCEPT.** Exact substrings are right here. The shared phrase `no nested directory and no nested contract` is a substring of both the write and writes forms (F-12, source.md:159-161). Each new phrase occurs once, so the `_removals` mutation cases bite.
- **A-005: QUALIFY.** The brief never states it as a general rule. But it does demand recording for F-1 and F-7 (source.md:42, 109), and Part 3 makes every verifier binding (source.md:34). An unrecorded departure from a quoted mandatory line is therefore a fidelity finding in this audit. The plan already models the recording form at plan:131. The obligation is to record, not to copy a worse sentence: F-16's substitute is better (spec:282), and F-13's widening is forced by F-2.

## Diff-point positions

| Point | Superior position | One-line evidence |
|---|---|---|
| S-001 | none | Finding counts are not merit; V3's 2 P1s shrink to at most 1 (R3-2's premise is disproved by the index), and V2's P1 is overstated |
| S-002 | V1 | A-2 INFERRED is right: the false FAIL needs a worker that breaks WORKER-CONTRACT.md:32; V3 tagged R3-1 Grounded |
| C-001 | split (V3 substance, V1 tag) | plan:128 admits analyze "can stop ... before it writes" and analyze.md:97 refuses chat-only, so plan:133's claim fails; but the text is brief-mandated (source.md:229, 217, 237) |
| C-002 | split (V2 classification, V1 substance) | plan:25 departs from source.md:199 unrecorded (V2); spec:282 says commit to a feature or scratch branch, no merge, so the plan's wording is better (V1); P2 |
| C-003 | V2 | Widening forced by F-2's status-after.txt (plan:152); Necessary deviation left unrecorded; "only" is also inaccurate given sync-dev (plan:21) |
| C-004 | V1 | `git status` shows the `...001016` package as `A`; the only `??` is this package, exempted at plan:157 |
| C-005 | V1 | plan:95 short path: `git show` fails, `grep -c` prints 0, no pipefail, so the AC passes vacuously |
| C-006 | V1 | plan:152, 155 save output to files with no `exit=$?`; low impact |
| C-007 | V3 | brainstorm.md:153 and SKILL.md:369-381: with `--report-dir`, `domain` and `enrichment_used` sit in the own contract, not at spec:286's `<contract>` |
| C-008 | V3 (as out-of-scope note) | WORKER-CONTRACT.md:24 twin unedited; no test ties it to the spec; the fix would need a seventh file (plan:21) |
| C-009 | V3 | handoff-routing.md:77 records a timeout as `skipped`, not the tier value stated at plan:54 (brief text source.md:230) |
| C-010 | V3 | spec:62 already names "the Skill tool or the Agent tool"; only Task is inferred (plan:135, from source.md:239) |
| C-011 | none | sc-implement-protocol SKILL.md:97 runs tasks sequentially in source order, so Task 1 always runs first |
| C-012 | V2 | Matrix completeness only; V2 itself confirms the plan satisfies the unsampled spans |
| C-013 | split (V1, V2) | spec:286 begins "4. Check the contract", plan:125 quotes it without the "4."; cosmetic |
| C-014 | split (all three) | Part 4 copied byte for byte: plan:38, 54, 69, 122, 128 vs source.md:229-231, 221, 217 |
| X-001 | V3 (qualified) | The conflict is real and refutes plan:133; but the failure is INFERRED (WORKER-CONTRACT.md:32) and the fix belongs in brief Part 4, so high P2 or a qualified P1 |
| X-002 | V1 | Today's index shows the earlier package staged; R3-2's premise is false |
| X-003 | V1 | P2: Constraints have no AC (qa.md:318 judges ACs only) and spec:282 backs the plan's wording |
| X-004 | V2 | Necessary deviation (forced by F-2) but unrecorded; the "only" overstatement is minor (plan:21 calls the `.claude/` writes output) |
| X-005 | split (V1, V2) | V1: managed ledger is the sibling progress.md (implement.md:58); V2: other `.dev/` writers stay unenumerated |
| A-001 | QUALIFY | analyze.md:97-98 holds for a usable directory, but a caller timeout can cut the call off before it writes (handoff-routing.md:77; plan:128) |
| A-002 | QUALIFY | Literal judging applies to task ACs (qa.md:318); F-16 and F-13 are not ACs, so they are not blockers |
| A-003 | ACCEPT | Index verified today (953 A, 3 R, 1 ??); the before/after snapshot design absorbs the baseline |
| A-004 | ACCEPT | Shared phrase is a substring of both verb forms (source.md:159-161); each pin occurs once |
| A-005 | QUALIFY | Not stated as a rule, but source.md:34, 42, 109 make recording expected; the plan models it at plan:131 |

## Round 2: Rebuttals

### Variant 1 Advocate

# Round 2 rebuttal: Advocate for Variant 1 (reviewer-1, analyzer)

"plan" = `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md`; "brief" = `source.md` in the same folder. Everything cited below was Read or run this round unless marked otherwise.

## Response to criticisms

Criticisms of V1 raised by Advocate 2 (A2) and Advocate 3 (A3) in Round 1, each answered.

| # | Criticism (who) | Answer | Verdict |
|---|---|---|---|
| 1 | A-2 filed P2 INFERRED although `analyze.md:97-98` was on disk; should be Grounded (A2, A3) | Conceded for the text conflict. I Read `analyze.md:97-98`: the contract "is written on every outcome" once a usable report directory exists; an unusable one is "refusal printed in chat only". The conflict between plan:38 and plan:128 is therefore Grounded. The failure is still INFERRED: it needs a worker that lists a file it did not write, and WC-4 (`WORKER-CONTRACT.md:32`) defines `artifacts` as "every other file written". So the honest tag is "Grounded conflict, INFERRED failure". My tag was wrong on the first half. | Concede tag; keep P2 |
| 2 | A-2 left at P2 although plan:133 says "no known false FAIL" and a P2 author will trust it (A3) | Partly conceded. plan:133 is false as written because plan:128 itself says the timeout "can stop `/sc:analyze` before it writes". But plan:133 copies brief:237 word for word. Severity stays P2: see "Updated assessment (a)" for likelihood. | Concede that I should have named plan:133; keep P2 |
| 3 | V1 missed R3-3 (`domain` and `enrichment_used` in the wrong contract) (A3) | Conceded that I missed it. But A3 calls it a false FAIL "on the ordinary route" and "on a correct worker". That is wrong. `WORKER-CONTRACT.md:192` ("`/sc:brainstorm` ... `--output <dir>`") and spec line 142 (brainstorm row: `--output <dir>`, contract at `<output>/return-contract.yaml`) say a conforming brief passes `--output`, and with `--output` the worker fields are added to brainstorm's own contract (`brainstorm.md:154`). Under a conforming brief `domain` and `enrichment_used` ARE in the step 4 contract. R3-3 bites only a non-conforming brief that passes `--report-dir`. Real, but a P3 note. | Concede miss; reject "ordinary route" |
| 4 | F-16 called a "nit"; V1 never asks where the AC check equivalent to the verifier is (brief:34) (A2) | Partly conceded. I did not ask the brief:34 question. Answer to it: there is none, and the verifier is literal ("Constraints contains the quoted line", brief:201). But `/sc:implement` judges task ACs through a closed template (`qa.md:318`). The only Constraints hook is `quoted-constraint-breach` (`qa.md:52`), which needs a diff that violates a Constraints item; no diff can violate a sentence about when edits reach a live plan. So it cannot block execution: a recording gap, not P1. | Concede the gap; keep P2/note |
| 5 | My R1 claim that the brief's "commits and merges" is "weaker/less accurate" than the plan's wording (implied by A2, A3 agreeing only on substance) | I overstated. Spec 7.2 (line 282) describes the P1 case: commit to a feature or scratch branch. For a P2 author on another branch the edits must be on THAT worktree's base branch, which in practice means merged. The brief's sentence is not wrong; the plan's "a branch the live-check worktree is built from" is equivalent in effect but not the quoted line. | Concede: "plan's wording is the correct one" was too strong |
| 6 | A-1: Task 5's half is overstated; the AC says "prints 0", so `grep -c` exit 1 is irrelevant (A2) | Conceded. Task 5 uses the full path (plan:111), so `git show` works and the count is a real 0. Withdrawn. | Concede, withdraw Task 5 half |
| 7 | A-1: Task 4's half is narrower than presented, because "the same command" can be read as the same full path (A2) | Partly conceded. I ran both forms just now: `git show HEAD:refs/handoff-routing.md 2>&1 \| grep -c ...` prints 0, and the full-path form also prints 0. So the log cannot tell a missing file from a missing phrase. The vacuity is real only if the executor shortens the path; a careful reading of "the same command" avoids it. Narrowed to a P3 hardening note (add `git show` exit status or a positive control). Still the only reproduced mechanical weakness. | Concede scope; keep as note |
| 8 | A-4 "false as written" is soft because plan:21 calls the `.claude/` rewrite "output, not edits" (A3) | Partly conceded. plan:21 is about "edit only these six files". The Task 7 sentence says "it writes only ... under `./artifacts/`" while the same task runs `make sync-dev`, which writes `.claude/`. The word "only" is inaccurate, but the brief's own F-13 sentence (brief:169) has the same flaw. So the falseness is brief-owned and a nit. | Concede to nit |
| 9 | A-3 (no exit codes) overstated (my own R1 weakness; A2 and A3 call it low) | Stand by the narrow part only: the format-check observation (`pyproject.toml:50-54`, CI runs `ruff format --check`) is valid; the exit-code part is weak because `make` prints `Error N` on failure. | Concede exit-code part |
| 10 | S-002: V1 better calibrated (A2, A3 agree) | Not a criticism; accepted with the caveat in row 1. | n/a |

## Updated assessment

### (a) The listed-contract conflict (C-001 / X-001)

What the files say:
- plan:38 (copied from brief:229): "The nested contract is listed in `artifacts`, also when the call failed."
- plan:128 (copied from brief:217): "every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`" with no carve-out in that clause. The carve-outs ("`skipped`", "did not refuse that directory") attach only to the later "required only when" clause. The same sentence admits the per-source timeout "can stop `/sc:analyze` before it writes".
- `analyze.md:97-98`: contract written on every outcome once the directory is usable; unusable directory is refused, chat only, no contract.
- WC-4 (`WORKER-CONTRACT.md:31-32`): `artifacts` = "every other file written".
- `SKILL.md:388`: `artifacts` includes "the nested contracts". `handoff-routing.md:77`: timeout records `quality_tier: skipped`.

Is it a real false FAIL? Yes, on one narrow path. Reachability of each trigger:
- Refusal. The nested directory sits under the report directory that brainstorm already validated against the same rule set (`brainstorm.md:153` vs `analyze.md:97`). A refusal of `nested/analyze-<n>/` needs a creation or write failure. Effectively unreachable.
- Timeout. Wave 2A runs sources in parallel Task agents with a 120 s limit (`handoff-routing.md:77`). A `/sc:analyze` that is cut off before it writes is reachable. Then the skill says to list the nested contract ("also when the call failed"). A worker following WC-4 lists only what exists. A worker following the skill's "unconditionally" sentence lists the path. Check: FAIL on a run the spec calls correct (skip and record).
- Frequency evidence: the only real run on record (`lc10-result.md`, line 13) made no `/sc:analyze` call at all.

Severity: P2 (high end). It needs (analyze route taken) AND (timeout before write) AND (worker lists an unwritten file). It cannot block `/sc:implement` (it is text in a spec), and it is a false FAIL in a future live check, which the owner can see and overrule. The only P1-flavoured argument is that plan:133 states "no known false FAIL", and the plan itself holds the counter-fact (plan:128). That makes plan:133 untrue in the plan's own voice. I keep P2 and I keep that plan:133 is wrong.

### (b) Who owns the defect: the plan or the brief?

The brief owns the wording. Part 4 says "copy exactly, do not paraphrase" (brief:213). plan:38 equals brief:229; plan:128 equals brief:217. Brief:225 ("keep the nested contract listed in `artifacts` unconditionally, a failed call's included") and brief:237 ("no known false FAIL") are the brief's own claims. So the plan is faithful and the brief is internally inconsistent.

The plan owns two smaller things:
1. It repeated "no known false FAIL" (plan:133) while its own plan:128 sentence contains the counter-fact. Part 4 asks the plan to record the four residual risks; it does not forbid recording a fifth in the opposite direction. The plan records one deviation openly (plan:131), so it could have recorded this.
2. Nobody flagged the conflict to the owner. A plan-level reviewer's remedy is an owner decision on Part 4, not a unilateral reword by the plan (V3's proposal would itself be an unrecorded departure from Part 4).

### (c) Other disputed facts, checked this round

- X-002 / C-004 (earlier package untracked?). Run just now: `git status --porcelain -- .dev/tasks/to-do` shows the earlier package `...001016` as `A` (three files) and only `?? .dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/` untracked; `git ls-files` for the 021737 folder prints 0. R3-2's premise is false today. The `??`-to-`A` flip of this package is what plan:157 exempts. Unchanged.
- A-002 (does `/sc:implement` judge the brief's verifiers?). `qa.md:318`: a closed template filled with seven slots; the reviewer may not add, remove or reword any criterion. The plan's task ACs are what get judged. Brief verifiers for F-16 and F-13 are not ACs, and F-13's sentence is task body text. So C-002 and C-003 cannot block execution.
- C-011 (missing Depends-on). `sc-implement-protocol/SKILL.md:97`: "Default sequential in source order". Grep confirms the line exists. Task 1 runs first. R3-7 only bites a manual out-of-order run. I now side with A3: nit, no winner.
- C-007 (R3-3). See criticism row 3: brief table passes `--output`, so the sentence is right for conforming briefs.

### (d) F-16 and F-13 departure (C-002, C-003)

Classification: Necessary deviation (F-13, forced by F-2, which adds `status-after.txt` that is not a log) and benign Drift (F-16, a rewording that keeps the intent), both unrecorded. Neither blocks. Both are fidelity notes (P3/low P2) because the brief's own Part 3 says "Apply all of them" and each verifier is a literal quote. The cheapest repair is zero-cost: put the brief's literal F-16 line in Constraints (it is true and harmless), or add one sentence recording the departure next to plan:131. For F-13, record "the sentence names the status snapshot because F-2 adds it; `make sync-dev` also rewrites `.claude/`".

### Other variants, adversarial view

- V2: right that two literal verifiers are unmet and unrecorded; wrong at P1; R2-3 tagged Grounded though it is inference; blind to C-001 and C-005. Strongest on brief-fidelity discipline.
- V3: strongest evidence on C-001; R3-2 rests on a false premise; R3-3 overstated as "ordinary route"; R3-7 not reachable under the executor; blames the plan for brief-mandated text on R3-1, R3-4, R3-5, R3-6.
- V1: three real finds (C-005 narrowed, C-004, the reproduction), one mis-tag (A-2), one miss (R3-3), no P1 and no fix proposal.

## New evidence

1. `WORKER-CONTRACT.md:192` and spec line 142: a conforming `/sc:brainstorm` brief passes `--output <dir>`. This downgrades R3-3 / C-007 to a non-conforming-brief note.
2. `lc10-result.md:13`: the only real run made no nested `/sc:analyze` call. The C-001 path has not been observed.
3. Ran `git show HEAD:refs/handoff-routing.md ... | grep -c ...` and the full-path form: both print `0`. Confirms the log cannot tell "file missing" from "phrase missing" (C-005 narrowed to Task 4's routing half).
4. `qa.md:52`: `/sc:implement` does look at plan Constraints, but only for a diff that violates a Constraints item (`quoted-constraint-breach`). F-16's line is not diff-checkable.
5. Index today: earlier package `A`, this package `??` only.

## Proposed wording fix

Goal: remove the plan:38 / plan:128 conflict without touching the Task 1 tail, so the rule "keep the nested contract listed unconditionally, a failed call's included" (brief:225) is untouched.

Smallest change: one parenthesis inside the Part 4 live-check sentence (brief:217, copied to plan:128). Leave brief:229 and plan:38 as they are.

Replace, in the Part 4 "Task 6 live-check sentence":

```text
every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`, and every
```

with:

```text
every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml` (not checked for a call whose `codebase` entry is `skipped` or whose directory `/sc:analyze` refused), and every
```

Why this works:
- It moves the two carve-outs that already exist in the "required only when" clause (`skipped`, "did not refuse that directory") forward to the "listed paths exist" clause, so both clauses agree.
- A call that crashes but is recorded `failed` still has to have written a contract (`analyze.md:98`, WC-4), so a missing file there is a true FAIL. This is the intent of the unconditional-listing rule.
- Task 1's tail "The nested contract is listed in `artifacts`, also when the call failed." and its AC (plan:45) stay byte for byte.
- No test pin changes. The Task 6 ACs (plan:142-143: `lc10`, `a source: codebase entry`, `neither quality_tier nor source records`) still hold.
- Matching edit in the plan: the same parenthesis in plan:128, and either keep plan:133 or add a fifth residual note: "A `/sc:analyze` call cut off by the per-source timeout may leave a listed path with no contract; the carve-out in the first clause covers it."

Not recommended: changing Task 1's tail to "listed whenever written". It is the brief's F-14 text, it would break the Task 1 AC (plan:45), and it reintroduces a condition that brief:225 forbids.

Optional hardening notes (not part of the fix): add the full repo path to Task 4's second `git show` command (plan:95) and require `git show` to exit 0; record the F-16 and F-13 departures in one sentence beside plan:131.

## Final diff-point positions

| Point | Final superior position | Changed since Round 1? | One-line evidence |
|---|---|---|---|
| S-001 | none | no | Counts reflect depth and bias, not correctness; V2's P1 and V3's second P1 do not survive checks |
| S-002 | V1 | no | V1 tags A-3, A-5 INFERRED correctly; caveat: its A-2 tag was wrong for the text conflict (`analyze.md:97-98` is on disk) |
| C-001 | V3 | no | plan:38 vs plan:128 vs `analyze.md:97-98`; real only on timeout; P2; wording is brief-owned (brief:217, 229, 237) |
| C-002 | split (V2 on recording, V1 on severity) | no | Verifier literal (brief:201) and unrecorded; no AC can judge it (`qa.md:318`); I withdraw "plan wording is more correct" |
| C-003 | V2 | yes | Widening forced by F-2 and unrecorded; "only" is also untrue due to sync-dev, but brief:169 has the same flaw |
| C-004 | V1 | no | Index run today: earlier package `A`, only this package `??`; exempted at plan:157 |
| C-005 | V1 | no | Reproduced: short and full path both print 0; narrowed to Task 4 routing half (Task 5 half withdrawn) |
| C-006 | V1 | no | Only raiser; format-check point valid (`pyproject.toml:50-54`), exit-code point weak; low |
| C-007 | V3 | no | `brainstorm.md:154`, `SKILL.md:369-381`; but briefs pass `--output` (`WORKER-CONTRACT.md:192`), so note-level only |
| C-008 | V3 | no | Only raiser; out-of-scope note, the fix needs a seventh file (plan:21) |
| C-009 | V3 | no | `handoff-routing.md:77` records `skipped` on timeout; brief-mandated wording (brief:230) |
| C-010 | V3 | no | Spec already names Skill and Agent tools (`spec:62`); only Task inferred (plan:135) |
| C-011 | none | yes | `sc-implement-protocol/SKILL.md:97` runs tasks in source order; Task 1 always first |
| C-012 | V2 | no | Only V2 checked matrix coverage; plan satisfies the spans; low |
| C-013 | none | no | All agree line 286 begins "4. Check the contract"; cosmetic |
| C-014 | none | no | All three confirm pins, slices and the byte-for-byte Part 4 copy |
| X-001 | V3 | no | Conflict real, fix belongs in brief Part 4; P2 (timeout path, unobserved in `lc10-result.md:13`), not P1 |
| X-002 | V1 | no | `git status` today: earlier package `A` |
| X-003 | split | no | Not P1 (Constraints line not an AC, `qa.md:318`); both V1 and V2 partly right; see C-002 |
| X-004 | V2 | yes | Necessary deviation (F-2), unrecorded; V1's extra point is brief-owned |
| X-005 | split (V1, V2) | no | Executor ledger stays in the package (`implement.md:58`); other `.dev/` writers unenumerated and unmeasured |
| A-001 | QUALIFY | no | Holds for a usable directory (`analyze.md:97-98`), not for a caller timeout (`handoff-routing.md:77`, plan:128) |
| A-002 | QUALIFY | no | `/sc:implement` judges task ACs through a closed template (`qa.md:318`); brief verifiers are not ACs |
| A-003 | QUALIFY | no | Tree matches today; before/after snapshot absorbs pre-Task-1 drift; only mid-run untracked paths matter |
| A-004 | ACCEPT | no | Brief mandates exact pins; slices supply placement |
| A-005 | QUALIFY | no | Reviewer convention; plan:131 sets the recording habit, so omission is a note, not a blocker |

### Variant 2 Advocate

# Round 2 rebuttal: Advocate for Variant 2 (reviewer-2, qa)

"plan" = `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md`; "brief" = `source.md` in the same folder. Everything cited was Read or run this round.

## Response to criticisms

| # | Criticism of V2 (who) | Answer | Verdict |
|---|---|---|---|
| 1 | R2-1 (F-16 line) is P1 but overstated: the plan's wording matches spec 7.2 (`spec:282`: commit to "the feature branch or a scratch branch with the user's authorization", no merge) (A1 R1, A3 R1) | Read `spec:282`: confirmed, no merge step. The plan wording ("committed to a branch the live-check worktree is built from", plan:25) states the spec's own requirement and still covers a P2 author on another branch. The brief's "commits and merges" is a simplification. A1's R2 retraction ("equivalent in effect, not the quoted line") is the right middle: same effect, not the verifier's literal line. I concede P1. | Concede severity (P1 to note/P3). Keep: verifier literal and departure unrecorded. |
| 2 | Constraints carry no AC; `/sc:implement` judges ACs through a closed template, so F-16 cannot block (A3 R1, A1 R2) | Read `qa.md:318`: the template is closed, seven slots, "may not add, remove or reword any criterion". True for per-task reviews. But the managed FINAL (`qa.md:310`) also reads "the plan's `## Constraints`" and returns `issues` when "a plan `## Constraints` item is violated"; per-task Q4 (`qa.md:339`) is "quoted-constraint-breach" against a diff. Both need a diff that breaches a Constraints item. A line about when edits reach a live plan cannot be breached by a diff, except by committing, which both wordings forbid ("this plan does not commit"). So neither wording can block execution. Conceded. | Concede: not an execution blocker. It stays a brief-fidelity finding for this audit. |
| 3 | R2-1 "drops the motivating scenario" (my own claim) | Withdrawn. Plan:25 names "a branch the live-check worktree is built from", which is exactly the scenario (`spec:282`). Only the word "merges" is lost, and the spec does not require it. | Withdrawn |
| 4 | R2-3 is tagged Grounded but is an inference about executor writes; unsized (A1 R1, A3 R1, A1 R2) | Conceded on tag: it is INFERRED. On size I now have evidence against my own claim. `implement.md:58`: a managed package always uses the sibling `progress.md` ledger; retries go to `<pkg>/artifacts/retries/` (`managed-workspace.md`). `git status --porcelain` today shows `.dev/reflect/pre-...001016/` and `pre-...021737/` as collapsed `??` directory lines. New files inside an already-untracked directory do not create a new line, so only a new top-level untracked path outside the package would trip bullet 3. `.dev/reflect/` is not gitignored (`git check-ignore` returns nothing), so a brand-new `.dev/reflect/<new>/` would be a new line, but `/sc:implement` has no step that creates one. Exposure is small. | Concede: INFERRED, small. R2-3 drops to a note. |
| 5 | V2 missed C-001/X-001 and C-005 (A2 R1 (mine), A3 R1, A1 R2) | True. I read plan:38 and plan:128 as separate edits and did not set them side by side. A QA card should have. No excuse. | Concede |
| 6 | V2 missed R3-3 (C-007) (A3 R1) | True; see below, C-007 is also lower than A3 claims. | Concede miss |
| 7 | S-002: V2 tags every finding Grounded (A1 R1) | Fair for R2-3 only. R2-1, R2-2, R2-4, R2-5 each quote both sides (brief line vs plan line). | Concede for R2-3 only |
| 8 | R2-2 (F-13 sentence) says "necessary deviation" but offers no fix (my own R1 weakness) | Fix: record it beside plan:131 ("the sentence names the status snapshot because F-2 adds it; `make sync-dev` also rewrites `.claude/`"), or write the brief's literal sentence and accept the F-2 conflict. Brief:169 itself says "writes only the logs", so the "only" flaw is brief-owned. | Concede; supply fix |
| 9 | C-012/C-013 are cosmetic (A3, A1) | Agreed. C-012: the plan satisfies the unsampled spans. C-013: spec:286 begins "4. Check the contract". | Concede (low) |
| 10 | V2's 0.87 self-confidence is unearned (A3 R1) | Agreed in effect: the blind calibration for V1 was 0.73 with 7 findings; V2's five findings missed the highest-severity defect. | Concede |

## Updated assessment

Steelman first: V1 reproduced a mechanical check weakness; V3 found the only plan-text defect that contradicts a claim the plan makes in its own voice (plan:133) and a second fragility (R3-3); A1 and A3 both held V2 to the right standard on severity, since a Constraints line cannot block the executor. My R1 P1 does not survive.

### (a) V1's proposed fix for the listed-contract conflict

V1 replaces, in the live-check sentence, "exists and holds its own `return-contract.yaml`, and every" with the same text plus "(not checked for a call whose `codebase` entry is `skipped` or whose directory `/sc:analyze` refused), and every".

Correct? Mostly yes.
- It moves into the first clause the two carve-outs that already sit in the "required only when" clause (plan:128). Both clauses then agree.
- A crash recorded as anything other than `skipped` still has to leave a contract: `analyze.md:98` says the contract "is written on every outcome" once the directory is usable. A missing file there is a true FAIL, which is the intent of brief:225.
- `skipped` is checkable from the contract itself (`SKILL.md:371-373`: `quality_tier: primary | fallback_1 | skipped`; `handoff-routing.md:77` records `skipped` on timeout).

Keeps brief:225 intact? Yes. It does not touch plan:38 (the Task 1 tail "listed in `artifacts`, also when the call failed" stays byte for byte) and it keeps the listing unconditional. The carve-out is on the check, not on the listing.

Testable? Partly. The `skipped` branch is testable from the contract. The "refused" branch is not observable from files: `analyze.md:97` says a refusal is "printed in chat only", so it needs the session file, and the existing last clause already says the session file may be "not verifiable". Where it is not verifiable, the refused carve-out cannot be invoked and the first clause fails exactly as today. That is the same edge V1 itself calls "effectively unreachable". Acceptable, but the sentence should say so or accept it.

Does it need a matching plan change? Yes, three:
1. Plan:128 must carry the parenthesis. But plan:128 is brief Part 4's sentence, "copy exactly, do not paraphrase" (brief:213). The F-1 verifier (brief:45) requires Task 6 to carry the sentence "byte for byte as in replacement_wording". So V1's fix is itself an unrecorded departure from the brief's highest-priority (P1) verifier unless the owner amends Part 4 first, or the plan records it next to plan:131 as a Necessary deviation. V1 downplays unrecorded departures elsewhere; here its own fix creates one.
2. Plan:133 ("no known false FAIL") is true only after that change. Without it, plan:133 must be narrowed.
3. The Task 6 AC (plan:143) pins three substrings (`lc10`, `a source: codebase entry`, `neither quality_tier nor source records`). None is touched, so no AC edit is needed. AC 144 (two lines changed) is unaffected. There is also no AC that checks "byte for byte", so the plan's ACs cannot detect either the brief's wording or V1's. That gap exists today (F-1's verifier asks for byte equality; AC 143 gives three substrings).

Alternative that needs no sentence change: keep Part 4 byte for byte and, in the plan only, replace plan:133's "no known false FAIL" with an honest statement and add a fifth residual risk in the false-FAIL direction ("a `/sc:analyze` call cut off by the per-source timeout can leave a listed path with no contract; the first clause then fails a correct run"). This is cheaper, makes no unrecorded change to brief wording, and surfaces the problem to the owner. My recommendation: do the alternative now, and ask the owner to approve V1's parenthesis as a Part 4 amendment.

### (b) Does `/sc:implement` judge the brief's verifiers? (qa.md:318)

Read: `qa.md:318` is a closed template; the orchestrator "fills only the seven slots" and "may not add, remove or reword any criterion". The slots include `{global_constraints}` and `{task_brief}`, and Q4 is "quoted-constraint-breach: does the diff violate a quoted plan constraint ... or an explicit task instruction". So V1 is right: brief verifiers are not judged. Only plan text is.

Consequences:
- C-002 (F-16): the Constraints line cannot be breached by a diff (only by committing), so it cannot block. Severity: note/P3. Fidelity finding only.
- C-003 (F-13): the sentence is task body text, i.e. an "explicit task instruction" (Q4), and Q3 asks about mutation "outside the task's declared outputs". A strict reviewer could mark Task 7's "writes only logs and snapshot" false (Q2 false-claim: "a recipe ... followed as written" does not do what the text says, because `make sync-dev` rewrites `.claude/`). But plan:21 labels those writes "output, not edits", the `.claude/` copies are gitignored so they never reach the diff or the status snapshot, and Task 7 produces no delivered text. The realistic chance of a blocking finding is low but not zero. So C-003 is P3, with a one-clause fix ("and the gitignored `.claude/` copies").
- The managed FINAL (`qa.md:310`) reads Constraints and returns `issues` for "a plan `## Constraints` item is violated". That also needs a breach.
So V2's A-002 point survives only as "fidelity, not blocker".

### (c) C-007 and the live-check "the contract"

V1 is right for a conforming brief. Read: spec line 142 (3.1 brainstorm row, column "Brief must pass"): `--output <dir>`; `WORKER-CONTRACT.md:192`: same; `brainstorm.md:154`: "With `--output` the worker fields are added to the command's own `<output>/return-contract.yaml`"; `SKILL.md:369-371`: `domain` and `enrichment_used` are fields of that own contract. So under a conforming brief, `<contract>` in 7.2 step 4 (`spec:286`) holds `domain`, `enrichment_used` and the worker fields together. R3-3 bites only a brief that passes `--report-dir`, which `brainstorm.md:153` allows but the spec's brief table does not. Two caveats keep it from being nothing: the Task 6 sentence does not say "with `--output`", so a P2 author who passes `--report-dir` gets a false FAIL on the `source: codebase` entry; and the `nested/analyze-` paths in the sentence are relative to the report dir either way. Verdict: V3 found a real fragility, V1 is right that it is a note (P3), not an "ordinary-route" false FAIL as A3 argued.

### Other variants, adversarial view
- V1: best on mechanical probes; A-2 tag wrong in the text-conflict half; fix proposal (a) is good but creates its own Part 4 departure; its A-5 "executor outputs stay in the package" is better evidence than my R2-3.
- V3: best evidence on C-001; R3-2 false today (index shows 001016 staged); R3-7 does not bite (`sc-implement-protocol/SKILL.md:97`: "Default sequential in source order"); R3-3 overstated; R3-4 to R3-6 are brief-mandated wording the plan cannot change without a recorded deviation.
- V2 (mine): the only card to hold the plan to the brief's literal verifiers; but missed C-001, and overrated severity.

## New evidence

1. `qa.md:310,318,339`: FINAL reads Constraints and fails only on a violated item; per-task Q4 needs a diff breach. Neither can fire on the F-16 line.
2. `git status --porcelain` today (this round): `001016` is `A`; `.dev/reflect/pre-...001016/` and `pre-...021737/` are collapsed `??` directory lines; `.dev/reflect/` is not gitignored. New files inside an existing untracked directory add no line; this shrinks X-005.
3. Ran `git show HEAD:refs/handoff-routing.md ... | grep -c ...`: prints 0; the full-path form also prints 0 and `git show` exits 0 on the full path. Confirms C-005 (Task 4 routing half only).
4. `sc-implement-protocol/SKILL.md:97` exists ("Default sequential in source order"), which shrinks C-011.
5. V1's fix applied to plan:128 would break the byte-for-byte verifier of F-1 (brief:45); AC 143 cannot detect it either way.
6. `brainstorm.md:154` vs `153`: `--output` and `--report-dir` are both legal in the command, but only `--output` is in the spec's brief table (`spec:142`, `WORKER-CONTRACT.md:192`).

## Final diff-point positions

| Point | Final superior position | Changed since Round 1? | One-line evidence |
|---|---|---|---|
| S-001 | none | no | Counts reflect depth and bias; V2's P1 and V3's R3-2 P1 do not survive |
| S-002 | V1 | yes (was split) | V1 tags A-3/A-5 INFERRED; V2 tagged R2-3 Grounded wrongly; V3 tagged R3-1 failure Grounded (WC-4 `artifacts` = files written) |
| C-001 | V3 (on evidence), P2 | no | plan:38 vs plan:128 vs `analyze.md:97-98`; real on timeout; wording brief-owned (brief:217,229,237) |
| C-002 | split (V2 on recording, V1 on severity) | no | verifier literal (brief:201) and unrecorded; plan wording matches `spec:282`; not blockable (`qa.md:310,318,339`); P3 |
| C-003 | V2 (classification), V1 for the "only" point | no | forced by F-2 (status-after.txt), unrecorded; "only" is brief-owned (brief:169); P3 |
| C-004 | V1 | no | `git status` today: `001016` is `A`; only this package `??`, exempted at plan:157 |
| C-005 | V1 | no | Run this round: short and full path both print 0; narrow to Task 4 routing half (plan:95) |
| C-006 | V1 | no | Only raiser; format-check point valid, exit-code point weak; low |
| C-007 | split (V3 found it, V1 sets severity P3) | yes (was V3) | `spec:142`, `WORKER-CONTRACT.md:192`, `brainstorm.md:154`: conforming briefs pass `--output`; bites only `--report-dir` briefs |
| C-008 | V3 (as an out-of-scope note) | no | Twin `WORKER-CONTRACT.md:24` unedited; a fix needs a seventh file (plan:21) |
| C-009 | V3 | no | `handoff-routing.md:77` records `skipped` on timeout; wording brief-mandated (brief:230) |
| C-010 | V3 | no | `spec:60,62` already name Skill and Agent; only Task inferred |
| C-011 | none | yes (was V3) | `sc-implement-protocol/SKILL.md:97` sequential in source order; Task 1 runs first |
| C-012 | V2 | no | Only V2 checked matrix coverage; plan satisfies the spans; low |
| C-013 | none | yes (was split) | All three agree, cosmetic: `spec:286` begins "4. Check the contract" |
| C-014 | none | no | All three confirm pins, slices and Part 4 copy |
| X-001 | V3 (P2) | no | Conflict real; failure only on timeout; unobserved in practice; fix is a Part 4 amendment (V1's parenthesis) or a narrowed plan:133 |
| X-002 | V1 | no | Index today: earlier package `A` |
| X-003 | split (V1 on severity, V2 on recording) | no | Not P1; `spec:282` supports the plan; departure still unrecorded |
| X-004 | V2 | no | Necessary deviation (F-2), unrecorded; "only" flaw brief-owned |
| X-005 | V1 | yes (was split) | `implement.md:58` ledger is the sibling `progress.md`; collapsed `??` lines; V2's exposure is small and INFERRED |
| A-001 | QUALIFY | no | `analyze.md:97-98` holds for a usable directory; not for a caller timeout (`handoff-routing.md:77`, plan:128) |
| A-002 | QUALIFY | no | `qa.md:318`: task ACs/constraints judged, brief verifiers not; C-002/C-003 are fidelity notes, C-003 carries a small Q2 risk |
| A-003 | QUALIFY | no | Before/after snapshot (plan:33,157) absorbs baseline; only mid-run changes matter |
| A-004 | ACCEPT | no | Brief mandates exact pins (brief:232-233); slices supply placement |
| A-005 | QUALIFY | no | Not a brief rule; brief:34 and plan:131 make silence a note-level gap |

### Variant 3 Advocate

# Round 2 rebuttal: Advocate for Variant 3 (reviewer-3, refactorer, opus)

"plan" = `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md`; "brief" = `source.md` in the same folder; "spec" = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`. Every file:line below was Read or grepped this round. Index facts come from `diff-analysis.md:19` (the orchestrator's check), because I cannot run git here.

## Response to criticisms

Steelman first. Advocates 1 and 2 are right on the main point. V3 found the strongest evidence for C-001, but it priced the finding too high and aimed the fix at the wrong document. Each criticism of V3 is answered below.

| # | Criticism (who) | Answer | Verdict |
|---|---|---|---|
| 1 | R3-1 is P2, not P1: narrow edge, brief-owned, never observed (A1 R1/R2, A2 R2) | **They are right.** (a) The wording is the brief's own: plan:38 = brief:229, plan:128 = brief:217, plan:133 = brief:237, and all of it sits under "copy exactly, do not paraphrase" (brief:213). (b) The failure needs three things at once: the analyze route is taken, the call is cut off or refused before it writes, and the worker lists a file it did not write. (c) The only real run made no nested `/sc:analyze` call (`lc10-result.md:13`, re-grepped this round). (d) It cannot block `/sc:implement`: it is spec text, not a task AC. What I keep: plan:133 says "no known false FAIL" in the plan's own voice, and plan:128 holds the counter-fact ("can stop `/sc:analyze` before it writes"). So plan:133 is false as written. | **Concede P1 to P2 (high). Keep that plan:133 is false.** |
| 2 | R3-1 is over-tagged Grounded (A1, A2, A3-R1) | Conceded. The text conflict is Grounded: `analyze.md:97-98` and plan:38 against plan:128. The false FAIL is INFERRED. WC-4 defines `artifacts` as "every other file written" (`WORKER-CONTRACT.md:32`), so a worker that puts WC-4 ahead of its skill never lists an unwritten contract. Steelman of my side: the skill's own contract template lists "the nested contracts" without condition (`SKILL.md:388`), and Task 1 adds "also when the call failed". A worker reads its skill before the shared contract, so listing an unwritten file is plausible. Plausible is still not observed. | **Concede: Grounded conflict, INFERRED failure.** |
| 3 | R3-1's remedy (reword the skill sentence to "listed when it was written") is itself an unrecorded Part 4 departure (A1 R1/R2, A2 R1) | Conceded, and it is worse than that. The reword breaks brief:225 ("keeps the nested contract listed in `artifacts` unconditionally, a failed call's included, never 'only for a command that ran'"). "When it was written" is a condition. It also breaks Task 1's AC (plan:45), which requires the paragraph to end with the exact sentence. | **Withdraw my reword.** The fix belongs in the check sentence, not in the listing rule (see the C-001 section). |
| 4 | R3-2 rests on a false premise (A1, A2) | `diff-analysis.md:19`: the earlier package `...001016` is staged (`A`), and only this package is `??`, which plan:157 exempts. The premise is false today. | **Withdraw.** At most a note that depends on A-003. |
| 5 | R3-3 is not an "ordinary route" false FAIL; conforming briefs pass `--output` (A1 R2, A2 R2) | **They are right.** Spec:142 (brainstorm row, "Brief must pass") says `--output <dir>`, and `WORKER-CONTRACT.md:192` says the same. With `--output`, the worker fields go into the command's own `<output>/return-contract.yaml` (`brainstorm.md:154`), which also holds `domain` and `enrichment_used` (`SKILL.md:369-373`). So under a conforming brief the step-4 contract holds every field the sentence reads. "Ordinary route" was my Round 1 advocate's overstatement. A residue is real: the sentence does not say "with `--output`", and `brainstorm.md:153` still allows `--report-dir`. | **Downgrade to a P3 note.** |
| 6 | R3-4, R3-5 and R3-6 are notes about text the brief mandates (A1, A2) | **They are right on ownership.** R3-4's companion sentence is brief:221, R3-5's routing bullet is brief:230, and R3-6's residual risk is brief:239. The facts still hold: `handoff-routing.md:77` records `skipped` on a timeout, not "this tier's `quality_tier`", and spec:60 and spec:62 already name "the Skill tool or the Agent tool". These are brief-level notes for the owner, not plan defects. The plan copied the text faithfully, as R3-8 itself confirms. R3-4 is weaker still (see New evidence 3). | **Concede: brief-owned notes.** |
| 7 | R3-7 does not bite under the executor (A1 R2, A2 R2) | `sc-implement-protocol/SKILL.md:97` (grepped): "Default sequential in source order". Task 1 always runs first. | **Withdraw to nit.** It matters only for a manual out-of-order run. |
| 8 | V3 missed the F-13 and F-16 literal-verifier departures, the `git show` vacuity and the step-4 anchor (A1, A2) | True. For a card whose focus was deviation classification, missing both unrecorded departures (plan:25 against brief:199; plan:152 against brief:169) is the bigger miss. | **Concede.** |
| 9 | V3 is inconsistent about brief fidelity: it ignores F-13 and F-16 yet proposes its own departure (A2 R1) | Fair. Point 3 withdraws the departure. | **Concede.** |

## Updated assessment

Adversarial view of each variant, mine first.

- **V3 (mine).** It found the best evidence for the one plan sentence the plan's own text refutes (plan:133 against plan:128). Its secondary false-FAIL path (R3-3) shrinks to a note once the brief table is read. Two of its eight findings are withdrawn (R3-2, R3-7). Three are re-owned to the brief (R3-4, R3-5, R3-6). The one P1 becomes a high P2, and its proposed fix was wrong. V3's net value is C-001's evidence and R3-8's byte-for-byte confirmation. The blind calibration should land below its 0.74 self-confidence.
- **V1.** It has the best mechanical probe (C-005, narrowed to Task 4's routing half). It got the index right on C-004 and proposed the right fix shape for C-001. Weakness: its parenthesis carries a refusal exception that no file can show without the session file, and V1 did not say what happens when the session file is missing (handled in the C-001 section).
- **V2.** It is the only card that held the plan to the brief's literal verifiers (C-002, C-003). It missed C-001, and its P1 did not survive (its own R2 concedes this). Its option (b) is cheap, but it fixes the wrong reader (below).

Severity outcome: **no P1 survives on any card.** The plan is executable as written. Before `/sc:implement`, one owner decision is worth taking: C-001. After execution, the same spec line would need a second edit, and F-1's byte-for-byte rule (brief:45) would then point at stale text.

## New evidence

1. **A refusal is not covered by the existing `skipped` exception.** A timeout records `skipped` (`handoff-routing.md:77`). But no file maps a refused or failed `/sc:analyze` call to `skipped`. The brief forbids stating any tier for any `/sc:analyze` outcome (brief:225). Tier 2 activates "if Tier 1 returns error OR empty result" (`handoff-routing.md:31`), so a refused call can end up recorded as `fallback_1` or `primary`. So the refusal exception in any fix is load-bearing, and it cannot be dropped in favour of a `skipped`-only exception.
2. **The refusal exception can only be judged from the session file.** `analyze.md:97` prints a refusal "in chat only". The existing required-folder clause already relies on the session file and ends "when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS" (plan:128). Under V1's parenthesis alone, a listed path that is missing, with a non-`skipped` entry and no readable session file, can only be judged FAIL. On a correct run, that is a false FAIL. It is near-unreachable, because the nested directory sits under a parent that brainstorm already validated against the same refusal list (`brainstorm.md:153` against `analyze.md:97`). But it keeps plan:133 literally false. Spec:300 shows the intended handling for unreadable evidence: `not verifiable`, never PASS, owner accepts in writing.
3. **R3-4's "twin drift" already exists.** Spec:62 says the step must be gate-free "per its section 3 row"; the installed twin `WORKER-CONTRACT.md:24` has no such words. The two texts were never byte-identical, so the companion sentence adds drift of the same kind. That makes R3-4 an even weaker owner note.
4. `lc10-result.md:13`: "no nested `/sc:analyze` call was made". The C-001 path has never been observed.
5. A grep of `tests/` for `orca-worker-contract-spec` finds no match. No test reads the spec, so a Part 4 amendment changes no test pin.
6. Spec:142 brainstorm row: `--output <dir>`. This confirms that R3-3 applies only to a non-conforming brief.

## Recommended resolution of C-001

**Pick: (a) the owner amends brief Part 4. Use V1's parenthesis plus one clause in the sentence's tail, and the plan mirrors the change.**

Option (b) is rejected as the resolution. A live-plan author reads only the spec's 7.2 step 4 sentence. The plan's residual-risk notes (plan:133-137) stay in this package, Task 6 leaves "everything else in the spec as it is" (plan:139), and the package is archived to `.dev/tasks/done/`. Under (b), the false FAIL stays in the one sentence the P2 author uses, and only the plan becomes honest about it. Option (b) is acceptable only as a fallback if the owner declines (a). In that case, plan:133 must be narrowed and a fifth risk added, exactly as Advocate 2 wrote.

My own option (c), changing Task 1's listing sentence, is rejected. It breaks brief:225 and the AC at plan:45 (see Response 3).

**Exact replacement text** (apply in brief Part 4 "Task 6 live-check sentence", brief:217, and identically in plan:128):

Edit 1. Replace

```text
every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml`, and every
```

with

```text
every `nested/analyze-` path listed in `artifacts` exists and holds its own `return-contract.yaml` (not checked for a call whose `codebase` entry is `skipped` or whose directory `/sc:analyze` refused), and every
```

Edit 2. Replace

```text
when the session file is not verifiable, this last clause is recorded `not verifiable`, never PASS
```

with

```text
when the session file is not verifiable, this last clause, and a listed path that is missing while the `codebase` entry is not `skipped`, are recorded `not verifiable`, never PASS
```

Edit 3. Change residual risk 4 (brief:241 and plan:137). Replace "The required-folder clause depends on the session file" with "The required-folder clause and the refusal exception depend on the session file". The rest of the bullet stays.

Checks against the constraints:

- **brief:225 (listing stays unconditional).** Held. Task 1's tail "The nested contract is listed in `artifacts`, also when the call failed." (plan:38) is untouched. The exception is on the check, not on the listing.
- **True FAILs are kept.** A call with a usable directory that failed must still have written its contract ("written on every outcome", `analyze.md:98`). Its listed path is still checked, so a missing file there is still a FAIL.
- **What the live-plan author reads.** The final spec sentence now carries both exceptions in the clause they apply to. Edit 2 routes the one unjudgeable case to the spec's existing `not verifiable` handling (spec:300) instead of a FAIL. The author needs no plan note to avoid a false FAIL.
- **plan:133 ("no known false FAIL")** becomes true. The only new leniency is that a missing path with an unreadable session file is recorded `not verifiable` instead of FAIL. That still blocks PASS until the owner accepts the gap in writing, which residual risk 4 already covers (Edit 3).

ACs and pins that change: **none.**

- Task 6 ACs (plan:142-144) still find `lc10`, ``a `source: codebase` entry`` and ``neither `quality_tier` nor `source` records``, and the edit is still one changed line in step 4.
- Task 1's AC (plan:45) is unchanged.
- No test reads the spec (New evidence 5).
- What must change: the plan text itself (plan:128 and plan:137) must match the amended Part 4, because F-1's verifier compares Task 6 byte for byte with the replacement wording (brief:45). Do this before `/sc:implement`, by owner amendment and a regenerate or a two-line plan edit. Otherwise Task 6 writes the old sentence into the spec.
- Known gap, not caused by this fix: no Task 6 AC checks byte equality (Advocate 2, R2 point 3).

## Final diff-point positions

| Point | Final superior position | Changed since Round 1? | One-line evidence |
|---|---|---|---|
| S-001 | none | no | No P1 survives on any card; counts measure bias, not merit |
| S-002 | V1 | no | V3's R3-1 failure is INFERRED (`WORKER-CONTRACT.md:32`); V2 tagged R2-3 Grounded wrongly |
| C-001 | split (V3 evidence; V1 severity P2 and fix shape) | yes | plan:38 vs plan:128 vs `analyze.md:97-98`; brief-owned (brief:213,217,229,237); fix = Part 4 amendment above |
| C-002 | split (V2 recording, V1 severity) | no | plan:25 vs brief:199 unrecorded; not blockable by a Constraints line (`qa.md:318`, per A1/A2); P3 |
| C-003 | V2 | no | Widening forced by F-2's status-after.txt (plan:152); unrecorded; "only" flaw is brief-owned (brief:169) |
| C-004 | V1 | no | `diff-analysis.md:19`: earlier package `A`, this package `??` exempted at plan:157 |
| C-005 | V1 | no | plan:95 "the same command" for the routing ref; short path fails and still prints 0; narrowed to Task 4 routing half |
| C-006 | V1 | no | Only raiser; format-check point valid, exit-code point weak; low |
| C-007 | split (V3 found it, V1 set severity P3) | yes | spec:142 and `WORKER-CONTRACT.md:192` require `--output`; `brainstorm.md:154` puts all fields in one contract then |
| C-008 | V3 (out-of-scope owner note) | no | Brief-mandated (brief:221); spec:62 and `WORKER-CONTRACT.md:24` already differ; fix needs a seventh file (plan:21) |
| C-009 | V3 (brief-owned note) | no | `handoff-routing.md:77` records `skipped` on timeout; text is brief:230 |
| C-010 | V3 (brief-owned note) | no | spec:60,62 name the Skill and Agent tools; text is brief:239 |
| C-011 | none | no | `sc-implement-protocol/SKILL.md:97` "Default sequential in source order" |
| C-012 | V2 | no | Matrix completeness only; plan satisfies the unsampled spans |
| C-013 | split (V1, V2) | no | spec:286 begins "4. Check the contract"; cosmetic |
| C-014 | none (all three agree) | no | plan:38,54,69,122,128 equal brief:229,230,231,221,217 |
| X-001 | V3 on evidence, P2 | yes | Real conflict, unobserved (`lc10-result.md:13`), not blockable; plan:133 false until Part 4 is amended |
| X-002 | V1 | no | `diff-analysis.md:19`: earlier package staged; R3-2 withdrawn |
| X-003 | split (V1 severity, V2 recording) | yes | spec:282 supports the plan's wording; departure from brief:199 still unrecorded; not P1 |
| X-004 | V2 | no | Necessary deviation forced by F-2, unrecorded; "only" overstatement shared with brief:169 |
| X-005 | V1 | yes | Ledger is the sibling progress.md (`implement.md:58`, per A1/A2); V2 conceded its exposure is small and INFERRED |
| A-001 | QUALIFY | no | Holds for a usable directory (`analyze.md:98`); fails for a caller timeout (`handoff-routing.md:77`); a refusal writes nothing and maps to no fixed tier (`handoff-routing.md:31`, brief:225) |
| A-002 | QUALIFY | no | Task ACs are judged literally; brief verifiers and the Constraints line are not ACs, so C-002 and C-003 are fidelity notes |
| A-003 | QUALIFY | yes | Before/after snapshot (plan:33,157) absorbs the baseline; only mid-run changes or an unstage of `...001016` break it |
| A-004 | ACCEPT | no | Exact-substring pins mandated (brief:232-233); each new phrase occurs once |
| A-005 | QUALIFY | no | Not a brief rule, but brief:34,42 and plan:131 make an unrecorded departure a note-level gap |

## Round 2.5: Invariant Probe

# Invariant Probe Results

## Round 2.5 — Fault-Finder Analysis

"plan" = `.dev/tasks/to-do/TASK-WF-brainstormFixBri-20261106-021737/TASK-WF-brainstormFixBri-20261106-021737.md`; "brief" = `source.md` in the same folder; "spec" = `.dev/orca-command-refactor/specs/orca-worker-contract-spec.md`; "amended sentence" = plan:128 with V1's parenthesis plus V3's Edits 2 and 3 (round2-advocate-1.md:79-96, round2-advocate-3.md:48-89). Tree state was read this round with `git --no-optional-locks status --porcelain`.

| ID | Category | Assumption | Status | Severity | Evidence |
|---|---|---|---|---|---|
| INV-001 | state_variables | Task 7 bullet 3 holds on a correct run: at Task 1 the earlier package `...001016` is `A`, this package and every `.dev/reflect/pre-*` folder are single collapsed `??` lines, the archived P1 package is `A`/`R`, and test, lint and sync-dev byproducts are ignored. The `git add .dev/tasks` flip of this package is exempt as "a path under this package's folder". | ADDRESSED | LOW | git status this round (only `A`/`R` under `.dev/tasks/done/`, no `??` there); `.gitignore:2,48,56,127,177`; plan:157; round2-advocate-2.md:12 |
| INV-002 | state_variables | `status-before.txt` is a true pre-edit baseline. The only check is AC plan:44, "exists and was written before the first edit", which a literal reader passes on existence alone. A snapshot taken late absorbs any earlier out-of-scope edit into the baseline, and bullet 3 then cannot see it, because it inspects only new lines. A checkable guard is missing, for example "`status-before.txt` names none of the six files". | UNADDRESSED | LOW | plan:33, plan:44, plan:157 |
| INV-003 | state_variables | Nobody changes the tree during the run. A baseline line that changes state (for example ` M src/superclaude/cli/install_core.py` becoming `MM`, made by another session) shows up as a new line that names neither the six files nor the package, so bullet 3 fails. The consensus accepts this: only mid-run changes matter. | ADDRESSED | LOW | plan:27, plan:157; round2-advocate-3.md:118 (A-003 QUALIFY) |
| INV-004 | guard_conditions | The `git show HEAD:` absence checks prove the pins fail on pre-change text. The consensus fix (full repo path plus a `git show` exit-0 guard or pipefail) closes the vacuous pass. Remaining edge: if the owner commits Tasks 1-3 before Task 4 runs, HEAD holds the phrase and the AC fails loudly, not vacuously. | ADDRESSED | MEDIUM | plan:95, plan:111; round2-advocate-1.md:17, :100; round2-advocate-2.md:67 |
| INV-005 | guard_conditions | The Task 6 ACs enforce the amended sentence. They do not: plan:142-144 pin `lc10`, ``a `source: codebase` entry``, ``neither `quality_tier` nor `source` records``, `7.2 step 4` and "two lines changed". All of these are present in both the old plan:128 and the amended sentence. If the brief is amended but plan:128/137 are not regenerated, or are regenerated imperfectly, Task 6 writes the old sentence and every AC passes. The consensus names the gap ("no Task 6 AC checks byte equality") but adds no pin, such as `not checked for a call whose`. | UNADDRESSED | MEDIUM | plan:128, plan:142-144; round2-advocate-3.md:88-89; round2-advocate-2.md:40 |
| INV-006 | guard_conditions | Each Task 1 AC token proves the edit. `skipped` and `nested/analyze-` are already in the pre-change paragraph (`quality_tier: skipped`, `nested/analyze-<n>/`), so those two pins pass without the edit. The other pins (`fallback_1`, the shared phrase, `only by a /sc:analyze call`, the exact ending) carry the proof. | ADDRESSED | LOW | SKILL.md:195; plan:45, plan:90 |
| INV-007 | count_divergence | `-k brainstorm` collects 17 today and 19 after the edit. Enumeration: content[brainstorm] 1; removals 12 (4 flags, 6 phrases, 2 nested); nested_propagation[brainstorm] 1; test_only_brainstorm_lists_nested_commands 1; ac_1_4_assertion_holds[brainstorm-section] 1; ac_1_4_check_fails[brainstorm-section:...] 1. That is 17. Only `_removals` reads `phrases`, so the edit adds exactly 2. The plan's baseline-plus-2 rule holds. | ADDRESSED | LOW | test_worker_contract.py:286-296, :519-527, :554-568, :901-906, :955-983 |
| INV-008 | count_divergence | The stated line numbers stay valid across Task 2's two inserts. The first insert after line 22 shifts the Tier 2 lines by one (31 to 32, 33 to 34). An executor that trusts "line 31" after the first insert puts the bullet between `quality_tier: fallback_1` and `Activation`. Task 4's tier-slice pins still pass there (the slice runs to `**Final fallback`); only Task 2's AC "follows the Tier 2 `Activation` line" catches it. | ADDRESSED | LOW | handoff-routing.md:22-33; plan:51, plan:61, plan:88 |
| INV-009 | count_divergence | The "exactly once" tier-slice counts are well defined. `**Tier 1 (primary)**` occurs three times (lines 16, 42, 63), and "first" pins the codebase one. The first `**Final fallback` after the Tier 2 anchor is line 33. Each slice gets exactly one new bullet. | ADDRESSED | LOW | handoff-routing.md:16, :24, :33, :42, :63; plan:88 |
| INV-010 | collection_boundaries | Zero nested folders (the lc10 replay: auggie unavailable, `fallback_1`, no `/sc:analyze` call). Under the amended sentence the `source: codebase` entry is present, no `nested/analyze-` path is listed, no directory exists and no call names one, so the result is PASS. | ADDRESSED | LOW | lc10-result.md:8, :13; plan:128 |
| INV-011 | collection_boundaries | A listed `nested/analyze-` path is a directory. `artifacts` lists files ("every other file written"; for brainstorm "the nested contracts"), so a listed entry is `nested/analyze-1/return-contract.yaml` or a report file inside that folder. "exists and holds its own `return-contract.yaml`" is a directory predicate. A literal checker tests `<listed file>/return-contract.yaml` and fails a correct analyze run. Neither V1's parenthesis nor V3's Edits 1-3 fix the file-versus-directory typing. | UNADDRESSED | MEDIUM | WORKER-CONTRACT.md:32; SKILL.md:388; plan:128; source.md:217 |
| INV-012 | collection_boundaries | Refused directory and timed-out call. The amended parenthesis exempts `skipped` and refused calls from the first clause. Edit 2 routes a missing listed path with a non-`skipped` entry and an unreadable session file to `not verifiable`. A failed call with a usable directory must still have written its contract, so its true FAIL is kept. | ADDRESSED | MEDIUM | diff-analysis.md:15 (analyze.md:97-98); handoff-routing.md:31, :77; round2-advocate-3.md:33-34, :50-81 |
| INV-013 | collection_boundaries | One `codebase` entry maps to one call. `enrichment_used` holds one entry per source, but the parenthesis speaks of "a call". With two or more `nested/analyze-<n>/` folders the `skipped`/refused carve-out cannot tell which call it covers, and only the adversarial F1 retry has a defined next number. Wrong only in the false-PASS direction. | UNADDRESSED | LOW | SKILL.md:371-373; brainstorm.md:157; round2-advocate-1.md:88 |
| INV-014 | collection_boundaries | Step 4's `<contract>` holds `domain` and `enrichment_used`. True with `--output` (one file). With `--report-dir` those fields are in the own contract that the worker contract lists in `artifacts`. Conforming briefs pass `--output`, and the consensus keeps this as a P3 note. | ADDRESSED | LOW | brainstorm.md:153-154; SKILL.md:381; round2-advocate-2.md:56; round2-advocate-3.md:15 |
| INV-015 | interaction_effects | The Part 4 amendment and F-1's byte-for-byte verifier conflict. They are compatible only if the owner amends source.md:217 (and residual risk 4 at :241, plus the "no known false FAIL" claim at :237) first, and plan:128/133/137 then mirror it. The consensus prescribes that order; a plan-only edit would be an unrecorded departure. | ADDRESSED | MEDIUM | source.md:45, :213, :217, :237, :241; round2-advocate-2.md:38; round2-advocate-3.md:88 |
| INV-016 | interaction_effects | The amended live-check sentence changes no pin or AC of Tasks 4-6. Confirmed: Tasks 4 and 5 read only `src` files (the SKILL, the ref, the command), no test reads the spec, the Task 6 substrings survive the amendment, and the edit stays one changed line. | ADDRESSED | LOW | test_brainstorm_protocol.py:11-13; test_worker_contract.py:20; plan:142-144; round2-advocate-3.md:37 |
| INV-017 | interaction_effects | The shared phrase carries the owner rule everywhere. The spec text the live-plan author reads (companion plan:122, live check plan:128, amended or not) never uses `no nested directory and no nested contract`. It also never states the contract half ("lists no nested contract in `artifacts`"). Its second clause only checks that existing folders are listed. brief:225 binds only Tasks 1-3, so this breaks no rule, but the spec holds half of the rule. | UNADDRESSED | LOW | plan:122, plan:128; source.md:59, :225 |
| INV-018 | interaction_effects | The amendment's "refused" carve-out contradicts the companion sentence "exists only for a nested command that actually ran, a run that failed included". It does not: that sentence states a necessary condition only, so a refused or timed-out call that writes nothing is consistent with it. | ADDRESSED | LOW | plan:122; round2-advocate-1.md:88 |
| INV-019 | sufficiency_challenge | "The next live plan will not repeat the lc10 false FAIL." Falsifier: Wave 2A hands each source to a `Task` agent, and the codebase row offers `/sc:analyze` OR auggie, with the nested `--report-dir` in the same paragraph. Suppose the worker writes the Task prompt "invoke /sc:analyze ... --report-dir <dir>/nested/analyze-1/" and the agent then takes the auggie or `fallback_1` path (lc10's own path). That Task call "passes `--report-dir .../nested/analyze-1/` with a number", the entry is `fallback_1` (not `skipped`) and nothing was refused. The amended sentence therefore requires `nested/analyze-1/`, and lc10's false FAIL recurs. The clause keys on text passed to any Skill/Agent/Task call, not on an actual `/sc:analyze` invocation. INFERRED: lc10's record lists only Skill calls. Fix: require a Skill call that invokes `sc:analyze` with that `--report-dir`. | UNADDRESSED | HIGH | SKILL.md:183, :187, :195; handoff-routing.md:77; plan:128; lc10-result.md:13 |
| INV-020 | sufficiency_challenge | The next live-plan author reads 7.2 step 4. The lc10 extra was not taken from 7.2. The P1 brief author wrote it from decision D-P1-4 (a propagation rule), and both the archived brief and plan still carry the wrong extra and stay unedited. The owner follow-up says "change the check wording in the next live plan". AC-1.2 and the P2 rows give no pointer to the new 7.2 step 4 sentence. A P2 author who copies the archived P1 brainstorm row repeats lc10. plan:131's premise ("every later live plan attaches its step-4 extras there") is unverified. | UNADDRESSED | MEDIUM | decisions/APPROVED.md:64; TASK-WF-p1LivePlanBrief source.md:62 and plan:275; p1-owner-decisions-20261105.md:9; spec:318, :325-332; plan:19, plan:131 |
| INV-021 | sufficiency_challenge | The corrected wording covers the next brainstorm live check. From P2 the research wave has the same split: Tier 1 is a nested Skill and Tier 2 is a WebSearch tool, and research-deep's fallback is itself nested. No "writes no nested directory" wording or live-check extra exists for it, so a P2 extra written by analogy repeats the false-FAIL class on the research wave. Recorded only as an open conflict. | UNADDRESSED | MEDIUM | plan:26; source.md:245; handoff-routing.md:42-73 |
| INV-022 | sufficiency_challenge | "Once run" is enough. The edits reach a live check only after they are committed to the live worktree's base branch and installed into `~/.claude` from it. The plan forbids both, and plan:25 records this precondition in substance (F-16's literal wording aside). | ADDRESSED | LOW | plan:24-25; spec:282 |

## Summary

- **Total findings**: 22
- **ADDRESSED**: 14
- **UNADDRESSED**: 8
  - HIGH: 1
  - MEDIUM: 4
  - LOW: 3

## Scoring Matrix

Confidence bands: unanimous 90-99, majority 60-89, split 50; +5 to +10 inside the band when the losing advocate explicitly conceded. No point is 100%, because no point had every advocate concede to a single winner with nothing reserved. Evidence cites the FINAL Round 2 tables and statements (`rounds/round2-advocate-N.md`, abbreviated R2-AN).

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | none | 92% | All three R2 tables say finding counts measure depth and bias, not merit. R2-A3 adds that no P1 survives on any card. |
| S-002 | V1 | 95% | All three give V1 for honest INFERRED tagging. V2 conceded R2-3 was INFERRED (R2-A2 rows 4 and 7) and V3 conceded R3-1's failure is INFERRED (R2-A3 row 2). |
| C-001 | V3 | 80% | A1 and A2 give V3 on evidence (plan:38 vs plan:128 vs `analyze.md:97-98`) at P2; A3 labels it split, crediting V1 for severity and the fix shape. All three agree the wording is brief-owned (brief:213, 217, 229, 237) and plan:133 is false as written. |
| C-002 | split | 50% | All three label it split: V2 is right that the F-16 verifier (brief:201) is unmet and unrecorded, V1 is right that it is not P1 and cannot block execution (`qa.md:310,318,339`, R2-A2 rows 1-2). No single winner, so unresolved under the rule. |
| C-003 | V2 | 85% | A1 moved to V2 in Round 2 (Necessary deviation forced by F-2, unrecorded) and A3 agrees. A2 gives V2 but credits V1 for the "only"/sync-dev point, which all three call brief-owned (brief:169). |
| C-004 | V1 | 97% | All three: the index shows `...001016` staged (`A`) and only this package `??`, exempted at plan:157 (R2-A1 section c). V3 withdrew R3-2 (R2-A3 row 4). |
| C-005 | V1 | 94% | A1 and A2 each ran the short and full path; both print 0, so the log cannot tell a missing file from a missing phrase (R2-A1 and R2-A2 New evidence 3). Narrowed to Task 4's routing half; the Task 5 half was withdrawn (R2-A1 row 6). |
| C-006 | V1 | 90% | All three give V1 as the only raiser, at low value. The format-check point stands (`pyproject.toml:50-54`); the exit-code point was conceded weak (R2-A1 row 9). |
| C-007 | split | 50% | A1 gives V3 at note level; A2 and A3 label it split (V3 found it, V1 set severity P3) because conforming briefs pass `--output` (spec:142, `WORKER-CONTRACT.md:192`, `brainstorm.md:154`). Substance is shared (real fragility, P3) but the labels differ, so unresolved. |
| C-008 | V3 | 90% | All three give V3 as an out-of-scope owner note; a fix needs a seventh file (plan:21). R2-A3 New evidence 3 adds that spec:62 and `WORKER-CONTRACT.md:24` already differ. |
| C-009 | V3 | 92% | All three: `handoff-routing.md:77` records `skipped` on a timeout, not "this tier's quality_tier". R2-A3 row 6 re-owns the text to the brief (brief:230). |
| C-010 | V3 | 92% | All three: spec:60 and spec:62 already name the Skill and Agent tools, so only Task is inferred. R2-A3 row 6 re-owns the text to the brief (brief:239). |
| C-011 | none | 93% | A1 and A2 moved from V3 to none and V3 withdrew R3-7 (R2-A3 row 7). `sc-implement-protocol/SKILL.md:97` runs tasks "Default sequential in source order", so Task 1 always runs first. |
| C-012 | V2 | 90% | All three give V2 as the only card that checked matrix coverage. The plan satisfies the unsampled spans, so impact is low. |
| C-013 | none | 70% | A1 and A2 say none, A3 says split (V1, V2). All agree spec:286 begins "4. Check the contract" and the point is cosmetic. |
| C-014 | none | 97% | All three confirm pins, slices and the byte-for-byte Part 4 copy (plan:38, 54, 69, 122, 128 equal brief:229, 230, 231, 221, 217; R2-A3 table). |
| X-001 | V3 | 92% | All three give V3 on evidence at P2: the conflict is real, the failure INFERRED and unobserved (`lc10-result.md:13`), and not blockable. V3 conceded P1 to P2 (R2-A3 row 1). |
| X-002 | V1 | 97% | All three: the earlier package is staged today, so R3-2's premise is false. V3 withdrew R3-2 (R2-A3 row 4). |
| X-003 | split | 50% | All three label it split (V1 on severity, V2 on recording); V2 conceded its P1 (R2-A2 row 1). No single winner, so unresolved under the rule. |
| X-004 | V2 | 93% | A1 moved to V2 in Round 2: a Necessary deviation forced by F-2, unrecorded. All three call the "only" overstatement brief-owned (brief:169). |
| X-005 | V1 | 78% | A2 and A3 moved to V1: the managed ledger is the sibling `progress.md` (`implement.md:58`) and new files in collapsed `??` directories add no line (R2-A2 row 4). A1 kept split (V1, V2); V2 conceded its exposure is small and INFERRED. |
| A-001 | QUALIFY | 95% | All three, both rounds: holds for a usable directory (`analyze.md:97-98`), fails for a caller timeout (`handoff-routing.md:77`, plan:128). R2-A3 adds that a refusal maps to no fixed tier (`handoff-routing.md:31`, brief:225). |
| A-002 | QUALIFY | 95% | All three, both rounds: `/sc:implement` judges task ACs through a closed template (`qa.md:318`); brief verifiers and the Constraints line are not ACs, so C-002 and C-003 are fidelity notes. |
| A-003 | QUALIFY | 90% | A1 and A2 QUALIFY both rounds; A3 moved from ACCEPT to QUALIFY in Round 2. The before/after snapshot (plan:33, 157) absorbs the baseline; only mid-run changes or an unstage break it. |
| A-004 | ACCEPT | 97% | All three, both rounds: exact-substring pins are what the brief mandates (brief:232-233), and slices supply placement. |
| A-005 | QUALIFY | 93% | All three, both rounds: not a brief rule, but brief:34, brief:42 and plan:131 make an unrecorded departure a note-level gap, not a blocker. |

## Per-Point Tracking

### Rule used

1. Each advocate's position is the label in its "Superior position" column (Round 1) or "Final superior position" column (Round 2), normalized as follows. A label that names one variant first, with a qualifier that only restates severity or ownership (for example "V3 (P2)", "V3 (brief-owned note)", "V3 (as an out-of-scope note)"), counts as that variant. A label that begins "split" counts as `split`, whatever variants its parenthesis names. `none` (no variant superior, all equal) is a substantive position and counts. For A- points the position is ACCEPT, REJECT or QUALIFY.
2. `split` is not a winner and never counts toward agreement, even when two or three advocates write the same split composition.
3. agreed = true when at least 2 of 3 normalized positions are the same non-split position. Unanimous = 3 of 3 the same with no qualifier crediting a different variant; majority = otherwise agreed (2 of 3, or 3 of 3 where one label credits a second variant for a sub-point). Otherwise agreed = false and winner = split.
4. The Round 2 FINAL tables decide `agreed` and `winner`. Round 1 is recorded for movement only.

Position order in each cell: A1 / A2 / A3. Q = QUALIFY, ACC = ACCEPT.

| Point | Level | Round 1 positions | R1 agreed | Round 2 positions | Agreement | agreed | winner |
|---|---|---|---|---|---|---|---|
| S-001 | L2 | none / none / none | yes | none / none / none | unanimous | true | none |
| S-002 | L1 | V1 / split / V1 | yes | V1 / V1 / V1 | unanimous | true | V1 |
| C-001 | L3 | V3 / V3 / split | yes | V3 / V3 / split | majority | true | V3 |
| C-002 | L1 | split / split / split | no | split / split / split | split | false | split |
| C-003 | L1 | split / split / V2 | no | V2 / V2 (credits V1) / V2 | majority | true | V2 |
| C-004 | L3 | V1 / V1 / V1 | yes | V1 / V1 / V1 | unanimous | true | V1 |
| C-005 | L3 | V1 / V1 / V1 | yes | V1 / V1 / V1 | unanimous | true | V1 |
| C-006 | L2 | V1 / V1 / V1 | yes | V1 / V1 / V1 | unanimous | true | V1 |
| C-007 | L2 | V3 / V3 / V3 | yes | V3 / split / split | split | false | split |
| C-008 | L2 | V3 / V3 / V3 | yes | V3 / V3 / V3 | unanimous | true | V3 |
| C-009 | L1 | V3 / V3 / V3 | yes | V3 / V3 / V3 | unanimous | true | V3 |
| C-010 | L1 | V3 / V3 / V3 | yes | V3 / V3 / V3 | unanimous | true | V3 |
| C-011 | L2 | V3 / V3 / none | yes | none / none / none | unanimous | true | none |
| C-012 | L2 | V2 / V2 / V2 | yes | V2 / V2 / V2 | unanimous | true | V2 |
| C-013 | L1 | none / split / split | no | none / none / split | majority | true | none |
| C-014 | L2 | none / none / split | yes | none / none / none | unanimous | true | none |
| X-001 | L3 | V3 / V3 / V3 | yes | V3 / V3 / V3 | unanimous | true | V3 |
| X-002 | L3 | V1 / V1 / V1 | yes | V1 / V1 / V1 | unanimous | true | V1 |
| X-003 | L1 | V1 / split / V1 | yes | split / split / split | split | false | split |
| X-004 | L1 | split / V2 / V2 | yes | V2 / V2 / V2 | unanimous | true | V2 |
| X-005 | L3 | V1 / split / split | no | split / V1 / V1 | majority | true | V1 |
| A-001 | L3 | Q / Q / Q | yes | Q / Q / Q | unanimous | true | QUALIFY |
| A-002 | L3 | Q / Q / Q | yes | Q / Q / Q | unanimous | true | QUALIFY |
| A-003 | L3 | Q / Q / ACC | yes | Q / Q / Q | unanimous | true | QUALIFY |
| A-004 | L1 | ACC / ACC / ACC | yes | ACC / ACC / ACC | unanimous | true | ACCEPT |
| A-005 | L2 | Q / Q / Q | yes | Q / Q / Q | unanimous | true | QUALIFY |

Totals: Round 1, 22 of 26 agreed (84.6%; unresolved C-002, C-003, C-013, X-005). Round 2, 23 of 26 agreed (88.5%; unresolved C-002, C-007, X-003).

Movement between rounds:
- Resolved in Round 2: C-003 (A1 moved to V2), C-013 (A2 moved to none), X-005 (A2 and A3 moved to V1).
- Lost agreement in Round 2: C-007 (A2 and A3 relabelled split after accepting that conforming briefs pass `--output`) and X-003 (A1 and A3 relabelled split). Neither flipped to a different single winner, so this is not oscillation under the skill's definition.
- C-002 was split in both rounds, with the same composition from all three advocates.
- Sensitivity note: if identical split compositions counted as agreement, C-002 and X-003 would be resolved (25 of 26). The final status does not change, because the invariant gate blocks either way.

## Taxonomy Coverage

Each point was tagged with exactly one level by scanning its text in `diff-analysis.md` for the skill's signal terms (L3: state, guard, boundary, invariant, validation rule, transition, concurrency; L2: architecture, API, component, module, interface, dependency, organization; L1: naming, formatting, wording, style, cosmetic, presentation), priority L3 > L2 > L1, default L2. A- points with state, guard or boundary terms are L3. The diff analysis's own Level column was kept for every C- point; it agrees with the signal scan.

| Level | Count | Points | Agreed |
|---|---|---|---|
| L3 state mechanics | 9 | C-001 (false FAIL guard), C-004 (git-status delta guard), C-005 (vacuous `git show` guard), X-001 (false FAIL guard), X-002 (index state), X-005 (tree-state exposure), A-001 (refused-directory boundary), A-002 (validation rule), A-003 (tree state) | 9 of 9 |
| L2 structural | 8 | S-001 (card organization, default), C-006, C-007 (which contract holds the fields: interface), C-008, C-011 (task dependency), C-012, C-014, A-005 (default) | 7 of 8 (C-007 unresolved) |
| L1 surface | 9 | S-002 (tag presentation), C-002, C-003, C-009, C-010, C-013, X-003 (severity of a wording departure), X-004 (wording), A-004 (wording pins) | 7 of 9 (C-002, X-003 unresolved) |

Coverage gate: PASS. All three levels have more than zero points, and every point was addressed by all three advocates in both rounds. No forced round is needed.

## Shared Assumptions

| A-NNN | Round 1 (A1 / A2 / A3) | Round 2 (A1 / A2 / A3) | Verdict |
|---|---|---|---|
| A-001 | QUALIFY: holds for a usable directory (`analyze.md:97-98`, WC-4), not for a timeout stop (plan:128) / QUALIFY: holds for refusal, fails for the timeout kill / QUALIFY: "every outcome" is the nested command's promise; a caller timeout cuts it off (`handoff-routing.md:77`) | QUALIFY (same reason) / QUALIFY (same reason) / QUALIFY: adds that a refusal writes nothing and maps to no fixed tier (`handoff-routing.md:31`, brief:225) | QUALIFY, unanimous. Promoted state/boundary assumption; it underlies C-001, X-001 and INV-012. |
| A-002 | QUALIFY: implement judges the plan's own bullets, not the brief's verifiers / QUALIFY: per-task AC judged (`sc-implement-protocol/SKILL.md:9`); F-16 is in no AC / QUALIFY: closed template (`qa.md:318`); F-16 and F-13 are not ACs | QUALIFY (`qa.md:318`) / QUALIFY: adds that FINAL reads Constraints but needs a breach (`qa.md:310,339`); C-003 carries a small Q2 risk / QUALIFY (same reason) | QUALIFY, unanimous. C-002 and C-003 are fidelity notes, not execution blockers. |
| A-003 | QUALIFY: tree matches today; snapshot design neutralizes pre-Task-1 drift / QUALIFY: only post-snapshot changes matter / ACCEPT: index verified today (953 A, 3 R, 1 ??) | QUALIFY / QUALIFY / QUALIFY: only mid-run changes or an unstage of `...001016` break it | QUALIFY, unanimous in Round 2 (A3 moved from ACCEPT). Consistent with INV-001 and INV-003 (ADDRESSED). |
| A-004 | ACCEPT: brief mandates exact pins; slices supply placement / ACCEPT (brief:232-233) / ACCEPT: shared phrase is a substring of both verb forms | ACCEPT / ACCEPT / ACCEPT | ACCEPT, unanimous. INV-006 notes two Task 1 pins are already in the pre-change text but the other pins carry the proof. |
| A-005 | QUALIFY: reviewer convention; plan:131 sets the precedent / QUALIFY: brief:34 and plan:131 make silence a gap / QUALIFY: brief:34, 42, 109 make recording expected | QUALIFY / QUALIFY / QUALIFY | QUALIFY, unanimous. An unrecorded departure is a note-level gap, not a blocker. |

## Convergence Assessment

- Points resolved: 23 of 26
- Alignment: 88.5%
- Threshold: 80%
- Gate 1, score: PASS (88.5% >= 80%). Round 1 was also above threshold (84.6%), so the majority was stable over 2 rounds.
- Gate 2, taxonomy coverage: PASS (L1 9, L2 8, L3 9; all levels addressed).
- Gate 3, invariants: FAIL. UNADDRESSED rows in `invariant-probe.md`: HIGH 1 (INV-019), MEDIUM 4 (INV-005, INV-011, INV-020, INV-021), LOW 3 (INV-002, INV-013, INV-017).

```text
CONVERGENCE BLOCKED: 1 HIGH-severity UNADDRESSED invariant(s) detected
Blocking items: INV-019
These invariant violations must be resolved before convergence can be declared.
Action: Address the flagged items in a subsequent debate round or acknowledge as accepted risk.

WARNING: 4 MEDIUM-severity UNADDRESSED invariant(s) detected
Items: INV-005, INV-011, INV-020, INV-021
These items do not block convergence but should be reviewed.
```

- INV-019 in one line: the amended live-check sentence keys on any Skill/Agent/Task call that passes `--report-dir .../nested/analyze-1/`, so a Task agent that takes the auggie or `fallback_1` path makes the sentence require a folder that was never created, and the lc10 false FAIL recurs (INFERRED; proposed fix: require a Skill call that invokes `sc:analyze` with that `--report-dir`).
- Final status: **BLOCKED_BY_INVARIANTS**
- Unresolved point IDs: C-002, C-007, X-003
- Blocking INV IDs: INV-019
- Round 3: not run (`--depth standard`).
- Base-variant selection and merge planning are out of scope here (Step 3 and later).
