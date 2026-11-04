**Invariant probe results: the consensus FAIL verdict stands, but both of its blocking fixes are incomplete.**

ID: INV-001
CATEGORY: sufficiency_challenge
ASSUMPTION: Running Task 16 (suite, lint, sync, staging) before Tasks 14 and 15 resolves C-001.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: Task 16 is the only `git add .dev/tasks` step (plan:236). The plan's own constraint says the package "and its `artifacts/`" are always staged (plan:23; managed-workspace.md:36). Tasks 14 and 15 write `t14-tier-smoke.md` and `t15-clickup-smoke.md` after that step, so both stay unstaged. That is a quoted-constraint breach, which is blocking under a `## Constraints` heading (SKILL.md:93) and blocking at the managed FINAL (qa.md:272). Task 15 may also "update the fixtures and script" (plan:219), but its AC only re-runs one test file (plan:224). After the reorder, an edit to `src/superclaude/.../clickup_claim.py` gets no `make sync-dev`, `make verify-sync`, `make lint` or full `uv run pytest`, which leaves source.md:400 and :475 unmet on that path.
RECOMMENDATION: Keep the suite task before the smoke tasks. Add to Task 15: "after any fixture or script edit, run `make sync-dev`, `make verify-sync`, `make lint`, `uv run pytest tests/skills`". End both smoke tasks with `git add .dev/tasks`.

ID: INV-002
CATEGORY: sufficiency_challenge
ASSUMPTION: The reorder alone removes the "blocked" contradiction.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The reorder changes only what is gated. The criteria at plan:213 and :223 still require "reported as blocked rather than passed". The ledger allows `complete` only with `compliant` (ledger.md:60).
- **Branch A:** an evidence-type AC with a truthful "E-TIER-UNAVAILABLE / not run" row counts as met (qa.md:83-87). The task is then marked `complete compliant`, which is a silent pass.
- **Branch B:** an unmet AC goes to the fix pass, the repair round and the A3-A5 ladder (qa.md:245). Advisers then try to fix a missing token, and the run halts with `E-HALT-QA` (qa.md:247).
- With the smoke tasks last, a Branch B halt also means the managed archive gate never runs (managed-workspace.md:47, :61).

RECOMMENDATION: Rewrite plan:213 and :223 as pure evidence ACs: "the artifact truthfully records served / E-TIER-UNAVAILABLE / not run, with the reason". State in the plan's Goal (plan:15) that the smoke checks may end pending. Drop "reported as blocked" from the acceptance criteria.

ID: INV-003
CATEGORY: interaction_effects
ASSUMPTION: Having the user export the variables before starting the session resolves A-001 with no side effects.
STATUS: UNADDRESSED
SEVERITY: HIGH
EVIDENCE: The no-token check at plan:49 only says "With `CLICKUP_API_TOKEN` unset" and gives no way to force it. If the token and workspace are exported in the session that runs Task 2, or in a resumed or retried Task 2, the script does a live `GET /user`, pages through the real workspace, and sends a `PUT` assignment when a real task links issue #302 (source.md:303-309). That is an unapproved ClickUp write, outside the plan's two live checks (plan:24-25). The plan also never requires the tests to remove the variables from the environment (plan:44), so the "skipped without token" tests depend on the real environment. The fix turns U-001 from minor into the default path.
RECOMMENDATION: At plan:49 use `env -u CLICKUP_API_TOKEN -u CLICKUP_WORKSPACE_ID uv run --no-project python ...`. Require `monkeypatch.delenv` in `test_clickup_claim.py`. Say the token is exported only for the session that runs the smoke tasks. Forbid `echo`, `env`, `printenv` and `set -x` on the token.

ID: INV-004
CATEGORY: guard_conditions
ASSUMPTION: Task 15 can compare live response shapes with the fixtures without handling the secret.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: The script prints only status JSON (plan:42; source.md:302-310), never the raw responses. To get the shapes the agent must make ad-hoc raw calls (for example `curl` with an Authorization header) or patch the script. `GET /user` returns personal data, which could then be copied into committed fixtures (plan:219) and into the transcript.
RECOMMENDATION: Specify how the comparison is done, for example a `--dump-shapes` debug mode that prints key paths only. Require that live values are never copied into fixtures.

ID: INV-005
CATEGORY: interaction_effects
ASSUMPTION: The C-002 fix ("run ACs 3 and 4, no writes") is safe to add.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE:
- plan:25 says "The only live checks in this plan are the two the source schedules". A new live task breaches that constraint (SKILL.md:93) unless plan:25 is changed too.
- AC 3 needs the Wave 1 T3 spawn (source.md:147, :155). It therefore has the same session-restart and tier-availability dependency as Task 14 (plan:209). Placed before the suite task, it would bring C-001 back.
- If the Wave 2 guard is faulty, the run reaches `gh issue edit --add-assignee` (source.md:162), a live GitHub write with no approval at that moment.

RECOMMENDATION: Amend plan:25. Put the AC 3 and AC 4 runs after the suite task, next to the smoke tasks. Ask the user before any run against a real issue.

ID: INV-006
CATEGORY: count_divergence
ASSUMPTION: Adding the never-pass-`model` rule to claim.md and create.md satisfies "every ref".
STATUS: UNADDRESSED (the consensus fix is too narrow)
SEVERITY: LOW
EVIDENCE: There are five refs (source.md:354-358; plan:91-95), and source.md:132 says "`SKILL.md` and every ref". The plan covers only tiers.md (plan:95, :103). The consensus fix names two more, so chains.md and labels.md are still missing, and the test checks only two files (plan:121).
RECOMMENDATION: Put the rule in all five refs and have the test iterate over `refs/*.md`.

ID: INV-007
CATEGORY: collection_boundaries
ASSUMPTION: The merged-PR list covers every PR merged since the issue was created.
STATUS: UNADDRESSED (inherited from the spec)
SEVERITY: MEDIUM
EVIDENCE: The `gh pr list ... --json ...` call at source.md:149 has no `--limit`, and `gh pr list --help` says "(default 30)". Task 5 copies "the gh commands exactly as written" (plan:91). For an issue older than 30 merged PRs, the accuracy check silently misses later PRs.
RECOMMENDATION: Add `--limit 200` (or page through results) in claim.md, and have the worker record when the result was truncated.

ID: INV-008
CATEGORY: collection_boundaries
ASSUMPTION: "Page through ... `page=<p>`" is fully specified.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Neither plan:42 nor source.md:304 gives the starting page. ClickUp's "page to fetch (starts at 0)" comes from the clickrup wrapper docs (peter.solymos.org), not from the official developer.clickup.com reference. The page-cap test (plan:44) does not pin page 0. Starting at page 1 skips the first 100 tasks. Only the live smoke check, which is likely to be blocked, would catch that. Invalid `CLICKUP_MAX_PAGES` values (0, negative, non-integer) are also undefined, because exit code 2 covers command-line arguments only (plan:42).
RECOMMENDATION: State "page starts at 0" and pin it in a fixture test. Define what happens on an invalid `CLICKUP_MAX_PAGES`.

ID: INV-009
CATEGORY: state_variables
ASSUMPTION: The skill directory contains only text files when Tasks 7 and 13 scan it for `src/superclaude`.
STATUS: UNADDRESSED
SEVERITY: MEDIUM
EVIDENCE: Tasks 1 and 2 load their scripts by path, the same way `test_workflow_archive.py:22-28` does. That normally writes `scripts/__pycache__/*.pyc`, which embeds the absolute source path containing `src/superclaude/` (inferred from CPython behaviour; not run). `__pycache__/` is gitignored (.gitignore:2), so it stays on disk. The Task 7 test "no file under the skill contains `src/superclaude/`" (plan:121) and the Task 13 `grep -rn` (plan:198, :202) could both report it. GNU grep 3.11 reports binary matches. `sync-dev` and `verify-sync` skip `__pycache__` (Makefile:117, :178), so sync itself is unaffected.
RECOMMENDATION: Make the test skip `__pycache__` and binary files, and use `grep -rIn` in Task 13.

ID: INV-010
CATEGORY: count_divergence
ASSUMPTION: "Under 500 lines" is measured the same way in the AC and the test.
STATUS: UNADDRESSED
SEVERITY: LOW
EVIDENCE: The AC uses `wc -l` (plan:112) and the test counts lines in Python (plan:121). For a file without a final newline, `wc -l` reports one line fewer (retry.md:79 records this exact off-by-one), so the two can disagree at 500.
RECOMMENDATION: Have the test use the same count as `wc -l`, or set the limit at 499 lines.

ID: INV-011
CATEGORY: count_divergence
ASSUMPTION: The plan's counts match the spec.
STATUS: ADDRESSED
SEVERITY: LOW
EVIDENCE: These all match: 14 templates (plan:68 = source.md:359), 5 refs, 3 agents, 9 STOP codes (plan:109 = source.md:328-340), 6 chains and 4 notes (plan:93 = source.md:227-238), 5 flags (plan:133), and 9 return-contract fields (plan:109 = source.md:353). The tier keys exist (ccsession-models.json:78, :93, :104). Three counts are only partly checked: the 100-150 line command size (plan:133) has no AC; the 22-request worst case (source.md:312) excludes the one 429 retry; and `E-CREATE-ONLY-FLAG` is not pinned by the command test (plan:135).
RECOMMENDATION: None needed. Optionally pin the STOP rules in `test_issue_command.py`.

**Files and lines re-Read**
- Debate files: `.work/r1-v1.md:1-83`, `r1-v2.md:1-85`, `r1-v3.md:1-108`, `r2-v1.md:1-70`, `r2-v2.md:1-89`, `r2-v3.md:1-82`, `diff-analysis.md:1-105`
- Plan: `TASK-WF-scIssueCommand-20261104-064713.md:1-236`
- Spec: `source.md:1-475`
- Executor:
  - `sc-implement-protocol/SKILL.md:1-178`
  - `refs/retry.md:1-140`, `:197-228`
  - `refs/qa.md:78-103`, `:240-287`
  - `refs/ledger.md:52-83`
  - `refs/managed-workspace.md` (Grep: lines 20-87)
- Other files:
  - `Makefile:61`, `:109-120`, `:166-181`
  - `tests/skills/test_workflow_archive.py:20-32`
  - `pyproject.toml:108-125`
  - `.gitignore:2`, `:239-261`
  - `ccsession-models.json:78`, `:93`, `:104`
- Commands and searches: local `gh pr|issue|label list --help` for the `--limit` defaults; `grep --version`; `find` for `__pycache__`; a Tavily search for ClickUp page indexing.

| DONE | NEXT |
|---|---|
| Probed all six categories; found three HIGH problems the consensus missed (INV-001 to INV-003) and six MEDIUM or LOW ones | Orchestrator: keep FAIL. Before adopting the two blocking fixes, add the staging and resync steps from INV-001, the AC rewrite from INV-002, and the Task 2 environment isolation from INV-003 |
