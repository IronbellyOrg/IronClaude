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
