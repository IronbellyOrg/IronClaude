# Reviewer 1 card (sonnet class, analyzer lens), persisted by the orchestrator

Self-reported confidence 0.80. Plan cited as plan:N (`.dev/tasks/to-do/TASK-WF-buildRelease1OfT-20261111-164757/TASK-WF-buildRelease1OfT-20261111-164757.md`); SPECDIR is `.dev/issues/409/bmad/spec-orca-observer/`.

Blocking
- R1-1 drift: Task 4 (plan:78) omits the blank-`dispatchId` rule and the `identity unknown` flag (`adapter-contract.md:44`) and the AD-7 rule that the next non-PARTIAL cycle replaces the previous cycle's UNKNOWN-id rows (`ARCHITECTURE-SPINE.md:112`); AD-19 retention (`ARCHITECTURE-SPINE.md:184`) then piles up ghost rows and blank-id rows collapse into one.
- R1-2 drift: T29 is half mapped; `acceptance-tests.md:32` needs no ESC/C1/Cf in render or export of `injection`, but Task 2 (plan:49-56) tests the sanitizer only and Tasks 10 and 11 do not assert injection at screen or export level, although plan:22 claims every applicable test is mapped.
- R1-3 drift: Task 13 (plan:225) registers the command before and independently of Task 14 (plan:238), while `release-gates.md:11` makes the golden samples and T32 the R1 live gate and `release-gates.md:5` says a failed gate keeps the previous view.

Minor
- R1-4: authorization rests on a chat message (plan:23); `ARCHITECTURE-SPINE.md:82` and `release-gates.md:34` keep the stricter reading until the owner's dated record exists; skipping T50 removes the input to DIRECTION-SELECTED (`release-gates.md:23`).
- R1-5: T32 `FAILED (shape)` is tested only in Task 14 (needs live Orca); cursor outcomes `cursor-stalled`, `cursor-rejected`, `empty-page` have no acceptance criterion (plan:108-117).
- R1-6: conftest's fake Runner needs the allow-list from `adapter.py` (Task 6) but Task 6 depends on Task 5 (circular) [INFERRED].
- R1-7: Task 8's literal list (plan:140) omits `messages UNVERIFIED (not read)`, `source warnings: n (inspector)`, `source counts: active a / ...`, `new baseline at HH:MM (observer started)`, and its criteria do not assert PARTIAL, mismatch, `cycle overran`, `filter <expr>`, `one Run only`, `reported T1-T2`.
- R1-8: `--width`, `--fixture`, `--once --width` (plan:210) are not defined in SPECDIR and not listed as plan-author rules (plan:26).
- R1-9: Task 14's timeout rule (plan:238) can lower the value (3.1 s slowest gives 9.3 s, below the 10 s default).
- R1-10: Task 5's "lists all ten variants" (plan:100) breaks when Task 14 adds four golden files; golden file format unspecified.
- R1-11: Task 1 (plan:35) handles SIGINT and SIGTERM only; `owner-decisions-and-risks.md:45` also lists SIGHUP and SIGTSTP with re-entry on SIGCONT; Task 2 depends on Task 1 so a failed spike blocks offline tasks, against plan:26.
- R1-12: FixtureSource has no `source.namespace` (card F1 confirmed).
- R1-13: Task 11 omits the ordering rule that rows with both timestamps unknown sort last (`snapshot-export-schema.md:72`); its worktree-term scan (plan:197) would trip on `shared-unmapped`.
- R1-14: the "SPECDIR wins" clause (plan:19) names only `merged-requirements.md`, not SNAPSRC (its line 103 lists `stage.detail` and `stage.activity`).
- R1-15: Constraints say CD-4 gets only spec-fixed rules (plan:25) but Task 3 sets `MIN_ROWS=8` (plan:62).

Checked and fine: dropping `runs_read` follows CD-10; Task 6's T2 reading; dependency order otherwise sound; cited paths exist.
