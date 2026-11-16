# Round 1, advocate for variant 1

## Position summary
V1's finding is true and blocking; the merged verdict must be NEEDS-REVISION. PLAN:52 says "Re-run `uv run python 08-test/evaluate.py` from PF first and confirm the figures still match the file". evaluate.py:110 writes `results.md` unconditionally, with no output-path option. Lines 1-52 regenerate identically from the 15 answer files; lines 54-93 (Diagnosis, AUCs, limits, the 7.6 kappa and per-kind table) are deleted, and no PF script can rebuild them (Grep `kappa|AUC` over PF `*.py`: no match).

Task 3 does require the in-place rerun: "first" puts it before the comparison, so the file is compared with itself and the check is vacuous. Afterwards PLAN:55 ("each figure ... with its source line in PF `08-test/results.md`") is unmeetable for kappa, the 52.6/65.3 split and the AUCs (results.md:58-65, 87-89), and Task 9's M, C, E citation (PLAN:123, :128) points at evidence (results.md:58-74) that is gone. It also breaks PLAN:21.

Recoverability: results.md is staged, never committed (`git ls-files -s` blob d9616dd; empty `git log`; status `A`, working tree equal to index). `git checkout -- <path>` restores it only until the next `git add .dev/tasks`, which CLAUDE.md rule 4 (and source.md:13) requires; then the blob is a dangling object findable by `git fsck` until gc. No other copy: the "added by hand after the run" heading occurs only in results.md and the two cards quoting it. Recovery is luck, not design.

Fix (a decision): **no in-place rerun.** Task 3 cites figures from the current file. A reproducibility check, if wanted, copies `05-scoring/`, `07-classifier/`, `08-test/` to a temp folder, runs there, and diffs stdout (evaluate.py:111) against results.md:1-52; kappa, split and AUCs are stated as hand-added and unreproduced. New acceptance line: "PF `08-test/results.md` is byte-identical before and after the task."

## Steelman
V2 is the broader review: it verified Task 9's anchors (spec :572, :609, :944, :946-947, :974, :985-986), pragmatic.md:221-231 (confirmed), the 17-finding card and the ledger, found three real gaps V1 missed, and honestly says it did not re-derive Task 3.

## Strengths claimed
- All V1 citations re-read true (PLAN:52, :21, :104; evaluate.py:110; results.md:54, 83-89; spec :572 "15 to 20", :609 "was empty").
- Only V1 applies pragmatic.md:231: a data-loss consequence is blocking whatever its label.

## Weaknesses of the opponent
- V2's "every live path I checked exists" never tested Task 3's command against evaluate.py, so its PASS rests on an unchecked task.
- Its findings are true but low-stakes: C-002 holds (source.md:13 vs PLAN:17-26); C-005 holds (PLAN:77, :90; stage-requests/README.md:32); its Wilson arithmetic holds (73 defects at p 0.95, 138 at p 0.90); the QA folder has 139 files (Glob).
- Its own C-002 (always staged) is what makes the C-001 loss stick in the git index.

## Concessions
- V1 missed C-002, C-003 and C-005. C-003 is real (PLAN:42-48 fixes seed, n and reproducibility, not the frame or the "uncorrected" test); non-blocking, since `stage0b_escape.py` encodes the frame.
- "Deletes ... Task 9's evidence pointer" overstates: the path survives, its content (results.md:58-74) goes.
- Two Checked bullets make V1 a thin record.

## Shared assumptions
- **A-001: ACCEPT.** C-001 does not even need it: evaluate.py derives `HERE` from its own location (:11) and has no flag, and copying the script alone fails because `ROOT = HERE.parent` must hold `05-scoring/` and `07-classifier/`. No careful executor avoids the overwrite.
- **A-002: QUALIFY.** Both read the rule the same way; V2 correctly keeps its MAJOR F2 non-blocking (no concrete wrong outcome). They differ in what they found: only V1 found a data-loss consequence, which pragmatic.md:231 makes blocking.

## Per-point table
POINT S-001 | winner: V2 | confidence: 70% | V2's four Checked bullets name more verified anchors than V1's two; shape does not change correctness.
POINT X-001 | winner: V1 | confidence: 88% | evaluate.py:110 overwrites results.md:54-93, and no PF script regenerates those lines; data loss is blocking under pragmatic.md:231, so PASS-with-notes is wrong.
POINT C-001 | winner: V1 | confidence: 92% | PLAN:52 orders the rerun "first", evaluate.py:110 has no output option, and the only other copy is an uncommitted index blob that the always-staged `git add` replaces.
POINT C-002 | winner: V2 | confidence: 90% | source.md:13 asks for "always staged"; PLAN:17-26 omits it; minor because CLAUDE.md still binds the executor.
POINT C-003 | winner: V2 | confidence: 75% | PLAN:42-48 leaves the frame and the "uncorrected" test to the executor; non-blocking.
POINT C-004 | winner: both | confidence: 80% | PLAN:104 makes the advisory fallback explicit (V1), and at p 0.90 to 0.95 the Wilson half-width needs 73 to 138 defects per class, so the fallback is near certain (V2).
POINT C-005 | winner: V2 | confidence: 80% | PLAN:77 and :90 both include the Task 2 sample, and stage-requests/README.md:32 has stage 2 evaluate both sets.
POINT A-001 | winner: both | confidence: 85% | ACCEPT; for C-001 the overwrite follows from evaluate.py:11 and :110 whatever the executor's care.
POINT A-002 | winner: V1 | confidence: 70% | QUALIFY; only V1 applies the data-loss clause of pragmatic.md:231, and V2 applies the MAJOR clause correctly to its own F2.
