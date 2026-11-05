# F2 result: Phase 2 spec review resolution and tasklist (issue #323)

Status: COMPLETE (finalizer F2, 2026-10-29). Planning only: no source, test or doc was edited, nothing staged or committed. `git status --short` shows only untracked `.dev/` content.

## 1. Tasklist package

- Package: `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/`
  - Plan: `TASK-WF-phase2CodegraphI-20261029-192001.md` (schema `workflow-plan/1.2`, 7 phases = spec groups G0-G6, 16 tasks = spec tasks T0, T0b, T2 step 0, T1, T2, T3, T3b, T4-T12).
  - `source.md`: byte-exact snapshot of the final revised spec (`cmp` clean).
  - `return-contract.yaml`: contract 1.1, `status: success`, `reflect_status: partial`.
  - `progress.md`: `/sc:implement` ledger header plus the `PLAN:` hash pin of the final plan and source (no task lines, so `/sc:implement` starts at Task 1).
- Execute with: `/sc:implement .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/TASK-WF-phase2CodegraphI-20261029-192001.md`
- Brief must-keeps, checked in the final plan:
  - Every task has a runnable acceptance command.
  - Every phase ends with a commit point and an issue-#323 comment: Tasks 2, 5, 8, 9, 13 and 15 end their groups. Task 16's commit point is the comment itself, because nothing changes in the repository after the merge.
  - The simple / mid / complex decision rules are in Constraints. Mid decisions use `/sc:adversarial --compare … --depth quick`; complex ones use `/sc:adversarial --compare …`.
  - Task 14 is the final full verification: the full suite against the baseline, plus `make lint` and `make verify-sync`. Task 16 is the post-merge live check.

## 2. Reflect status

- Advisory `/sc:reflect --mode pre` (workflow Wave 4). Report: `.dev/reflect/pre-phase2CodegraphI-20261029192356/REPORT.md`; contract: `.dev/reflect/pre-phase2CodegraphI-20261029192356/return-contract.yaml`. **Status: partial.**
- Path:
  - **Tier 1:** C = 0.71 from a blind calibrator.
  - **Coverage forced Tier 2:** coverage was flagged `parsed-sparse`. That flag means the spec has no labelled requirement ids, so all 104 requirements came from inference.
  - **Two reviewers:** sonnet (analyzer) and glm-5.3 (qa). Both were blind-calibrated, at 0.80 and 0.74.
  - **Adversarial merge:** convergence 1.0 and 19 findings, with 2 hidden-error corrections applied (INV-001, INV-006).
  - **Evidence gate:** 189 of 193 citations re-read and 0 dropped; all 104 inferred-requirement rows checked.
- Why it is partial:
  - **Invariant gate:** the merge's invariant gate is BLOCKED_BY_INVARIANTS. Its two corrections were applied but not debated again, because standard depth has no third round.
  - **Input drift:** `.dev/codegraph-migration/specs/phase-1-removal-spec.md` changed at 20:28:20Z while reflect was running, most likely F1's concurrent edit. Only Task 2's check reads that file.
- Coverage: 0 real gaps. 64 of 104 rows matched by word containment. The other 40 are covered by section reference (39) or are Coder-owned (1).
- Fixes applied after reflect: the brief says to fix plan defects by editing the generated plan.
  - **Plan:** all 19 merged findings (M-01 to M-19) are fixed in the plan. M-15 and M-16 are notes on the reflect artifacts and need no plan change.
  - **Spec, origin spec:** the 8 findings that came from the spec were fixed there too: M-02, M-08, M-09, M-10, M-11, M-13, M-18, M-19.
  - **Spec, calibrator:** two spec contradictions found by the calibrator were also fixed:
    - the commit point for the stdio client;
    - T12's read-only rule.
- Plan fixes that matter most:
  - Task 1's `.claude/` guard had an inverted exit code.
  - Task 16's local-scope check aborted the live checks, so it is now recorded and report-only; user scope still gates, and the removal commands are printed.
  - Task 7's retire-test lookup matches nothing today, so the gate could pass without running the test; it now must find the file.
  - U11 moved to Task 5.
  - The non-gating `&&` and `!` check lines were split into one condition per line.
  - Task 14's evidence is now copied before the gate runs, and always committed.
  - Artifact paths use a lookup that works whether the package is under `to-do/` or `done/`.
- The re-run gate checks on the final plan pass: no numbered or checkbox lines; Tasks 1-16 contiguous, each with acceptance criteria; 7 phases; all 12 bash blocks pass `bash -n`.

## 3. Review findings applied

- Spec: `.dev/codegraph-migration/specs/phase-2-codegraph-install-spec.md`. Its `## Review resolution` section has two tables.
  - **First pass (task R review):** X-1, X-2, X-5, X-9, X-10, X-11, X-14, X-15, X-21 and X-25 are applied. X-11 needed a corrected command, because the review's own pipe fails under pipefail. F2 found and fixed 3 more defects:
    - F2-1: T10's `comm` line could not fail;
    - F2-2: the baseline pipe failed under pipefail;
    - F2-3: tests U24 and U25 were assigned to no task.
  - The Phase 3 findings (X-3, X-6 to X-8, X-13, X-18 to X-20, X-22, X-23) and the Phase 1 findings (X-4, X-12, X-16, X-17, X-24) are listed as other phases' work. No other phase's spec was edited.
  - **Second pass:** the reflect findings, M-02 to M-19 and C-1 and C-2.
- Coder handoff (N=2): both files under `.dev/codegraph-migration/handoff/` were updated for X-1, X-2 and X-10.
  - **Registration JSON:** it now includes `CODEGRAPH_MCP_TOOLS`, and the Coder side is told to read `MCP_TOOLS`, `VERSION` and `SHA256` from IronClaude's `install_codegraph.py` at the pinned SHA.
  - **Guidance block:** it is rewritten without `codegraph_explore` and sits between `SUPERCLAUDE_CODEGRAPH_BEGIN/END` markers. Coder re-syncs it on every pin bump instead of appending it once.
  - **"Done means" checks:** two new `jq` checks.
- Key Phase 2 addition: T2 step 0 is the schema-cost check that chooses `CODEGRAPH_MCP_TOOLS`.
  - F2 re-measured it with the spec's own client against the W4 sandbox binary on 2026-10-29: D = 7,597 bytes, inside the 6,000 to 8,000 byte undecided band.
  - The same run showed the explicit list hides `codegraph_explore` and blocks calls to it, which was UNVERIFIED before (X-25).
  - Because D is in the undecided band, the executor's session measurement (Leg B) decides between the 7 tools and `status` only. Without a logged-in `claude`, the value is `status`.

## Decisions

| Decision | Options considered | Method | Rationale |
|---|---|---|---|
| How Phase 2 measures the tool-list schema cost (T2 step 0) | A stdio byte proxy; B real headless-session tokens; C byte gate plus a recorded session check | adversarial quick (`.dev/codegraph-migration/decisions/F2-schema-cost-method/`, merged `adversarial/F2-schema-cost-method-merged.md`; A 0.870, C 0.829, B 0.701; 15/15) | Followed the merge: A's byte measurement is the gate, in three bands. Inside the 6,000 to 8,000 byte band B decides, and the run never blocks (C's rule). |
| Phase 2 owns `CODEGRAPH_MCP_TOOLS` in one `MCP_TOOLS` constant: seven tools on pass, `status` on fail | leave it to Phase 3; hard-code the JSON | self (forced by review X-1 and `orchestration/README.md:40`) | Only Phase 2 can change the installer, and one constant feeds the installer, tests, layer 2, T12 and Coder (spec D25). |
| Guidance block between markers, re-synced by Coder on every pin bump | append once, guarded by the first line | self (forced by X-2 and X-10) | Appending once would freeze the first wording on Coder (D26). |
| Post-merge check T12 has no repository commit; the issue comment is the record | an evidence file on a follow-up branch | self | Nothing should change in the repository after the merge (D27). |
| Corrected the review's X-11 baseline-diff command | apply it verbatim | self | The verbatim pipe exits non-zero under pipefail (D28). |
| T8 re-adds the CI step only if Phase 1 deleted it | always re-add | self (X-15) | This works whichever way F1 resolves X-15 (D29). |
| X-14: the Phase 2 hunk only states the hook switch's scope and the prefix convention | rename Phase 3's switch | self | The rename belongs to Phase 3 (F3); this run does not edit another phase's spec. |
| No adversarial run for applying the review findings | spawn one per finding | self | Each finding was settled by checking the cited source; none had two viable options. |
| `source.md` written by `cp` plus a `cmp` check, not by the Write tool | Write tool | self (necessary deviation from the workflow protocol) | The protocol requires a byte-exact copy, and copying the file is the only exact way for an 860-line spec. |
| Refreshed `source.md` after each post-snapshot spec fix | leave the snapshot stale | self | The plan and its snapshot must match the final spec; `/sc:implement` re-pins hashes before its first task starts. |
| Edited the generated plan after reflect | leave reflect advisory only (the workflow protocol rule) | self (forced by the coordinator brief, step 2) | The brief says to fix plan defects in the plan; the edit is a separate step after the workflow finished. |
| Kept final verification Task 14 although the workflow protocol rejects verification-only tasks | drop it | self (brief step 3 requires it) | Task 14 also fixes what the gate finds and commits its evidence, so it is not verification-only. |
| Created `progress.md` with only the ledger header and `PLAN:` pin | leave it to `/sc:implement` | self (brief's observable acceptance) | This is the format `/sc:implement` writes itself, so it resumes cleanly at Task 1. |
| Accepted reflect `partial` without re-running it | re-run reflect | self | The drift is another finalizer's file and only Task 2's check reads it; the blocked invariants were applied as corrections (M-02, M-18). |
| Two reviewers instead of three | three | protocol-forced | The executor class (opus) is excluded from the reviewer pool and no backfill class exists. |
| Artifact paths in shell use `$(echo .dev/tasks/*/<id>)/artifacts` | hard-code the `to-do/` path (the merge's M-04 fix) | self | A hard-coded `.dev/tasks/to-do/` path breaks the workflow gate rule once the package is archived. |
