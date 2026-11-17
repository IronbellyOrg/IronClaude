# Adversarial Debate Transcript

## Metadata
- Depth: standard
- Rounds completed: 2 (Round 1 parallel statements, Round 2 sequential rebuttals) plus Round 2.5 (invariant probe)
- Convergence achieved: 100% on per-point winners after Round 2 (Round 1: all 9 points already had the same winner or an agreed split; the only grade gaps were C-003 to C-005)
- Convergence threshold: 80%
- Focus areas: correctness, coverage, deviation-classification
- Advocate count: 2 (variant 1: opus class; variant 2: haiku class). Judge and scorers: sonnet class. Fault-finder: opus class.
- Taxonomy coverage: L1 (S-001, C-002), L2 (X-001, C-003, C-004), L3 (C-001, C-005, A-001, A-002) all covered
- Invariant probe: 13 entries; HIGH and UNADDRESSED: 1 (INV-006, the SubagentStart hook confound), carried into the merged card as blocking finding F2 and not accepted as risk

## Round 1: Advocate Statements

### Variant 1 Advocate (opus class)

#### Round 1, advocate for variant 1

##### Position summary
V1's finding is true and blocking; the merged verdict must be NEEDS-REVISION. PLAN:52 says "Re-run `uv run python 08-test/evaluate.py` from PF first and confirm the figures still match the file". evaluate.py:110 writes `results.md` unconditionally, with no output-path option. Lines 1-52 regenerate identically from the 15 answer files; lines 54-93 (Diagnosis, AUCs, limits, the 7.6 kappa and per-kind table) are deleted, and no PF script can rebuild them (Grep `kappa|AUC` over PF `*.py`: no match).

Task 3 does require the in-place rerun: "first" puts it before the comparison, so the file is compared with itself and the check is vacuous. Afterwards PLAN:55 ("each figure ... with its source line in PF `08-test/results.md`") is unmeetable for kappa, the 52.6/65.3 split and the AUCs (results.md:58-65, 87-89), and Task 9's M, C, E citation (PLAN:123, :128) points at evidence (results.md:58-74) that is gone. It also breaks PLAN:21.

Recoverability: results.md is staged, never committed (`git ls-files -s` blob d9616dd; empty `git log`; status `A`, working tree equal to index). `git checkout -- <path>` restores it only until the next `git add .dev/tasks`, which CLAUDE.md rule 4 (and source.md:13) requires; then the blob is a dangling object findable by `git fsck` until gc. No other copy: the "added by hand after the run" heading occurs only in results.md and the two cards quoting it. Recovery is luck, not design.

Fix (a decision): **no in-place rerun.** Task 3 cites figures from the current file. A reproducibility check, if wanted, copies `05-scoring/`, `07-classifier/`, `08-test/` to a temp folder, runs there, and diffs stdout (evaluate.py:111) against results.md:1-52; kappa, split and AUCs are stated as hand-added and unreproduced. New acceptance line: "PF `08-test/results.md` is byte-identical before and after the task."

##### Steelman
V2 is the broader review: it verified Task 9's anchors (spec :572, :609, :944, :946-947, :974, :985-986), pragmatic.md:221-231 (confirmed), the 17-finding card and the ledger, found three real gaps V1 missed, and honestly says it did not re-derive Task 3.

##### Strengths claimed
- All V1 citations re-read true (PLAN:52, :21, :104; evaluate.py:110; results.md:54, 83-89; spec :572 "15 to 20", :609 "was empty").
- Only V1 applies pragmatic.md:231: a data-loss consequence is blocking whatever its label.

##### Weaknesses of the opponent
- V2's "every live path I checked exists" never tested Task 3's command against evaluate.py, so its PASS rests on an unchecked task.
- Its findings are true but low-stakes: C-002 holds (source.md:13 vs PLAN:17-26); C-005 holds (PLAN:77, :90; stage-requests/README.md:32); its Wilson arithmetic holds (73 defects at p 0.95, 138 at p 0.90); the QA folder has 139 files (Glob).
- Its own C-002 (always staged) is what makes the C-001 loss stick in the git index.

##### Concessions
- V1 missed C-002, C-003 and C-005. C-003 is real (PLAN:42-48 fixes seed, n and reproducibility, not the frame or the "uncorrected" test); non-blocking, since `stage0b_escape.py` encodes the frame.
- "Deletes ... Task 9's evidence pointer" overstates: the path survives, its content (results.md:58-74) goes.
- Two Checked bullets make V1 a thin record.

##### Shared assumptions
- **A-001: ACCEPT.** C-001 does not even need it: evaluate.py derives `HERE` from its own location (:11) and has no flag, and copying the script alone fails because `ROOT = HERE.parent` must hold `05-scoring/` and `07-classifier/`. No careful executor avoids the overwrite.
- **A-002: QUALIFY.** Both read the rule the same way; V2 correctly keeps its MAJOR F2 non-blocking (no concrete wrong outcome). They differ in what they found: only V1 found a data-loss consequence, which pragmatic.md:231 makes blocking.

##### Per-point table
POINT S-001 | winner: V2 | confidence: 70% | V2's four Checked bullets name more verified anchors than V1's two; shape does not change correctness.
POINT X-001 | winner: V1 | confidence: 88% | evaluate.py:110 overwrites results.md:54-93, and no PF script regenerates those lines; data loss is blocking under pragmatic.md:231, so PASS-with-notes is wrong.
POINT C-001 | winner: V1 | confidence: 92% | PLAN:52 orders the rerun "first", evaluate.py:110 has no output option, and the only other copy is an uncommitted index blob that the always-staged `git add` replaces.
POINT C-002 | winner: V2 | confidence: 90% | source.md:13 asks for "always staged"; PLAN:17-26 omits it; minor because CLAUDE.md still binds the executor.
POINT C-003 | winner: V2 | confidence: 75% | PLAN:42-48 leaves the frame and the "uncorrected" test to the executor; non-blocking.
POINT C-004 | winner: both | confidence: 80% | PLAN:104 makes the advisory fallback explicit (V1), and at p 0.90 to 0.95 the Wilson half-width needs 73 to 138 defects per class, so the fallback is near certain (V2).
POINT C-005 | winner: V2 | confidence: 80% | PLAN:77 and :90 both include the Task 2 sample, and stage-requests/README.md:32 has stage 2 evaluate both sets.
POINT A-001 | winner: both | confidence: 85% | ACCEPT; for C-001 the overwrite follows from evaluate.py:11 and :110 whatever the executor's care.
POINT A-002 | winner: V1 | confidence: 70% | QUALIFY; only V1 applies the data-loss clause of pragmatic.md:231, and V2 applies the MAJOR clause correctly to its own F2.

### Variant 2 Advocate (haiku class)

#### Round 1 — Advocate for Variant 2 (haiku class)

<!-- Persisted by the orchestrator from one message; the advocate does not write files. P = the stage 0 plan file; F = the program folder `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115` (the advocate's own abbreviations). Text unchanged. -->

V2 adds useful measurement warnings, but its PASS verdict is wrong. Steelman V1: Task 3 explicitly orders a destructive rerun, not merely a calculation. P = `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md`; F = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115`.

V2 correctly spots the missing staging constraint and the undocumented sampling choices (P:17-26,42-48). But P:52 says rerun first; F/08-test/evaluate.py:110 replaces results.md without reproducing its handwritten diagnosis or measurements (results.md:54-93). This violates P:21 and removes required evidence. V2 missed a blocker. Its claim that a short spec cannot hold enough defects is overstated: size alone proves no impossibility, and P:104 explicitly permits advisory results.

Concede V1's blocking verdict. Keep V2's sampling warning and conditional overlap warning; neither establishes an inevitable wrong result.
A-001 QUALIFY: follow explicit commands, but account for guards; P:21 conflicts with P:52.
A-002 ACCEPT: demonstrated evidence loss is blocking, unlike an optional measurement fallback.

POINT S-001 | winner: both | confidence: 99% | minor | Card layout changes no outcome.
POINT X-001 | winner: V1 | confidence: 99% | blocking | P:52 requires overwrite despite P:21.
POINT C-001 | winner: V1 | confidence: 99% | blocking | F/08-test/evaluate.py:110 omits results.md:54-93.
POINT C-002 | winner: V2 | confidence: 99% | minor | P:17-26 omits requested staging constraint.
POINT C-003 | winner: V2 | confidence: 94% | nonblocking warning | P:42-48 records seed, not extraction or matching rules.
POINT C-004 | winner: V1 | confidence: 95% | minor | P:104 expressly permits advisory intervals; impossibility claim unsupported.
POINT C-005 | winner: V2 | confidence: 92% | nonblocking warning | P:77,90 reuse sample; pooling is not required.
POINT A-001 | winner: both | confidence: 96% | qualified | P:21,52 conflict; literal execution exposes loss.
POINT A-002 | winner: V1 | confidence: 99% | blocking | Required evidence disappears; no execution needed to establish overwrite.

## Round 2: Rebuttals

### Variant 1 Advocate (opus class)

#### Round 2, advocate for variant 1 (rebuttal)

##### 1. Grades
- **C-002: minor.** source.md:13 asks for the constraint and PLAN:17-26 leaves it out, but global CLAUDE.md rule 4 still binds the executor, so no task behaves differently.
- **C-003: Medium.** PLAN:42 leaves the frame and the "uncorrected" test open, but PLAN:46 requires a reproducible `stage0b_escape.py`, so the frame is recorded in that code. It is a real weakness, not a silent wrong result.
- **C-004: minor (note, not a defect).** PLAN:104 already makes the advisory fallback the plan's answer. V2's arithmetic is correct (73 defects at p 0.95, 138 at p 0.90), so the fallback is near certain, but nothing goes wrong.
- **C-005: Medium.** PLAN:77 and :90 put the same sample in two sets. stage-requests/README.md:32 names them separately, so the double count occurs only if the stage 2 package pools them. This is a follow-up candidate for that package.

##### 2. Fix for C-001
In **Task 3**, replace the last sentence of PLAN:52 with: "Do not run `08-test/evaluate.py` in PF; it overwrites `results.md` (evaluate.py:110), including hand-added lines 54-93. To check the figures, copy PF `05-scoring/`, `07-classifier/` and `08-test/` to a temporary folder, run `uv run python evaluate.py` there, and compare its printed output with PF `08-test/results.md` lines 1-52. Kappa, the per-kind split and the per-question AUCs were added by hand; cite them from the file."
New acceptance line: "`./artifacts/stage0a-result.md` records the SHA-256 of PF `08-test/results.md` before and after the task, and the two match." I use a hash, not `git diff`, because a `git add .dev/tasks` in between would hide the change.

##### 3. Where the opponent is wrong
- **A-001 "account for guards":** neither Task 3 nor evaluate.py has a guard. PLAN:21 is a constraint that contradicts PLAN:52's command, so the plan leaves the executor a decision it does not make. That is the brief's first blocking clause, on top of data loss.
- **C-004 "impossibility claim unsupported":** V2 made no impossibility claim. It said every gating class "will almost certainly" fall back, and it conceded that "the request allows that fallback". Its numbers are right. V1 wins only the grade (not a defect).

##### 4. Task 10 acceptance lines
**No.** PLAN:139-142 require paths and headlines, limits, definitions, staging decisions, ledger and the closing sentence. None requires the owner-decision list (OD3, OD4) or the five key findings that PLAN:136 asks for, though source.md:17 asks for the five findings. Grade: **Medium**. The body still instructs the executor, but per-task QA against acceptance would pass a summary that omits them. The fix is one added line, "lists OD3 and OD4 and the five key findings", with no decision needed.

##### POINT lines
POINT C-001 | winner: V1 | confidence: 95% | blocking
POINT C-002 | winner: V2 | confidence: 90% | minor
POINT C-003 | winner: V2 | confidence: 85% | Medium
POINT C-004 | winner: V1 (grade); V2 arithmetic correct | confidence: 75% | minor
POINT C-005 | winner: V2 | confidence: 85% | Medium
POINT A-002 | winner: V1 | confidence: 90% | blocking (data-loss clause, pragmatic.md:231)

### Variant 2 Advocate (haiku class)

#### Round 2 — Advocate for Variant 2 (haiku class)

<!-- Persisted by the orchestrator from one message; the advocate does not write files. P = the stage 0 plan file `.dev/tasks/to-do/TASK-WF-blockerStage0-20261116-021044/TASK-WF-blockerStage0-20261116-021044.md`; F = `.dev/tasks/to-do/BLOCKER-CLASSIFICATION-PROGRAM-20261115` (the advocate's own abbreviations). Text unchanged. -->

- C-002: agree, minor. P:17-26 omits staging, but the global rule still applies.
- C-003: agree, Medium, nonblocking. P:42 leaves selection and matching choices open; P:46 requires reproducibility, not a written explanation of those choices.
- C-004: agree, minor note. P:100,104 explicitly allow advisory intervals. I retract my "impossibility" characterization; V2 said "almost certainly," though "cannot hold" was too categorical.
- C-005: agree, Medium, nonblocking. P:77,90 overlap; separate reporting need not double-count anything.
- Task 10: agree, Medium. P:136 requires owner decisions and five key findings; P:139-142 omit both. The body remains binding.

The C-001 fix works with genuine independent copies preserving the sibling layout. Execute the copied `08-test/evaluate.py`, not merely from a different working directory: F/08-test/evaluate.py:11-19 resolves inputs relative to the script; :110 writes beside it. Copied `truth_table.py` has no import-time file writes. Avoid symlinked scripts or linked output files. Matching before/after hashes detect alteration but do not prevent it. This was source inspection, not an executed trial.

POINT C-001 | V1 | 99% | blocking
POINT C-002 | V2 | 99% | minor
POINT C-003 | V2 | 94% | Medium, nonblocking
POINT C-004 | both | 95% | minor note
POINT C-005 | V2 | 94% | Medium, nonblocking
POINT A-002 | V1 | 99% | blocking

## Round 2.5: Invariant Probe

See `invariant-probe.md` (13 entries; HIGH and UNADDRESSED: INV-006; MEDIUM and UNADDRESSED: INV-002, INV-005, INV-007).

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|------------------|
| S-001 | both | 85% | Card shape changes no outcome; V2 records more verified anchors |
| X-001 | V1 | 97% | Task 3 overwrites results.md (evaluate.py:110); V2's advocate conceded the PASS; merged verdict NEEDS-REVISION |
| C-001 | V1 | 97% | PLAN:52 orders the rerun; evaluate.py:110 writes in place; hand-added lines 54-93 have no generator; fix: no in-place rerun, check on a real copy |
| C-002 | V2 | 95% | source.md:13 constraint missing from PLAN:17-26; minor |
| C-003 | V2 | 90% | Task 2 frame unrecorded; Medium (the script records it in code) |
| C-004 | both | 90% | Advisory fallback near certain but allowed (PLAN:104); minor note |
| C-005 | V2 | 90% | Tasks 5 and 6 share the Task 2 sample; Medium (a stage 2 pooling risk) |
| A-001 | both | 92% | QUALIFY by V2's advocate, ACCEPT by V1's: literal execution exposes the PLAN:21 against PLAN:52 conflict |
| A-002 | V1 | 90% | Data loss is blocking under the severity rule; an optional measurement fallback is not |

## Convergence Assessment

- Points resolved: 9 of 9 (winners)
- Alignment: 100%
- Threshold: 80%
- Status: CONVERGED on diff points; the one HIGH UNADDRESSED probe item (INV-006) is carried into the merged card as F2
- Unresolved points: none
