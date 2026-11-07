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
