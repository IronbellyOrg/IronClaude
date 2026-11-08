# Reflect report: pre-execution audit of the issue-watcher task file

```yaml
contract_version: 1.8.0
status: success
mode: pre
tier_reached: 2
confidence_calibrated: 0.82
citations_total: 191
citations_revalidated: 101
citations_dropped: 0
citations_inferred: 8
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 101` - the 36 finding citations plus a 65-row sample of the 155 inferred-requirement rows, re-read by independent evidence validators.
> - `citations_dropped: 0` - drops observed in the sample (gates promotion; no promotion applies in pre mode).
> - `citations_dropped_extrapolated: 0` - projection, recording only.
> Every inferred-row quote and all 70 finding evidence lines were also checked by a script (verbatim match inside the cited lines); this is extra evidence, not a replacement for the validators.
> The extrapolated value is telemetry, not a verdict.

## Verdict

**Not signed off (`verdict: fail` for the task file's `reflect_pre` block).** The merged register holds 2 blocking and 11 minor findings. Parsed-only `coverage_pct` is 0.9231 (at or above the 0.90 floor), but the union coverage including inferred requirements is 0.8631 (below it) and two blocking defects remain open. The build is not blocked by this verdict; per the task-builder rule the unmapped items go to the Open Questions section and nothing is rewritten.

Spec: `docs/designs/issue-watcher.md` (935 lines). Task file: `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md` (209 items). Run: Tier 2, `--depth deep` (hard override), 3 heterogeneous reviewers, blind calibration, adversarial merge (convergence 1.00, status partial because 3 high-severity invariant probes stayed unresolved), two evidence validators.

## Coverage

| Measure | Value |
|---|---|
| Parsed requirements (T-1..T-13, design section 7.4) | 13, matched 12 |
| Inferred requirements kept after span dedup | 155 (2 dropped as overlapping a parsed span) |
| `coverage_pct` (parsed only) | 0.9231 |
| `coverage_pct_union` | 0.8631 |
| `S_dev_density` | 0.1369 |
| Unmapped parsed | T-2 |
| Unmapped union rows | 23 |
| Task items | 209 |
| Best-practice grade | 4 of 5 (all three reviewers) |

The containment matcher is lexical, so the 22 unmapped inferred rows were judged by the reviewers; every row they read was found covered or covered under a declared deviation (see Coverage resolution). The only rows with a real gap are AC-6 and AC-14 (findings M-004, M-003).

## Findings (gap registry, most severe first)

### M-001: Step 10.6 runs the POST reflect with --remediate after the single checkpoint commit and tells the runner to apply the remediations the skill offers

- **Severity:** blocking
- **Category:** sequencing
- **Source findings:** R3-001, R1-002
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:864` - --mode post --remediate --diff <BASE SHA>..HEAD
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:866` - If the skill surfaces any Regression or any unauthorized Drift, apply the remediations the skill offers under `--remediate`
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:854` - ensuring exactly one new commit exists on top of BASE
- **Claim:** Step 10.6 runs the POST reflect with --remediate after the single checkpoint commit and tells the runner to apply the remediations the skill offers. Those edits land after every gate, outside the BASE..HEAD audit range, and are never committed, because Step 10.7 stages only .dev/tasks with no second commit (DF-07). The handoff also needs an explicit yes that the bypass-mode runner subagent has no user to give.
- **Debate outcome:** X-001: unanimous VALID-BLOCKING, 95%. Fix option not agreed (INV-001 HIGH, unresolved).
- **Default remediation:** Make the Step 10.6 POST reflect report-only: drop --remediate from the Step 10.6 skill arguments and replace item 3 at TF:866 with "any Regression or unauthorized Drift HALTs the task; write it to the Task Log and report it to the owner; do not edit source and do not create a second commit". A re-gate after remediation is not sufficient (INV-001), and the runner must never answer the remediation handoff itself (INV-002). If the owner later chooses a re-gate, it uses the PASS-baseline verdict defined in M-002 (INV-003).

### M-002: The lint, format and affected-test gates require exit 0 while also saying a finding or failure in a file the task did not touch is recorded and not fi

- **Severity:** blocking
- **Category:** contradiction
- **Source findings:** R3-002
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:699` - a finding in a file this task did not touch (the local `uv run ruff` is not the pinned 0.15.20) is recorded and NOT fixed
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:702` - ensuring all three commands exit 0; a hit in a file this task did not touch is recorded and not fixed
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:693` - a failure in a file this task did not touch is investigated for causality and recorded, not fixed, if it is pre-existing
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:735` - every row is PASS (a FAIL is fixed and its step re-run before this item is marked complete)
- **Claim:** The lint, format and affected-test gates require exit 0 while also saying a finding or failure in a file the task did not touch is recorded and not fixed. A pre-existing finding therefore makes the gate fail with no permitted fix, yet the gate record requires every row PASS, any failing command is a finding, and the post-fix re-runs HALT when a command cannot be made to pass. The task has no passing path on a repository with any pre-existing lint or test failure.
- **Debate outcome:** X-008: unanimous VALID-BLOCKING, 95%; attack A-004 (pre-existing findings are out of scope) rejected 3/3. Site list not agreed complete (INV-004, INV-005 HIGH, unresolved).
- **Default remediation:** (a) Add a P1 baseline step that records the output of `make lint`, the pinned ruff 0.15.20 format check and the G-2 affected test subset before any source change. (b) Define one PASS-baseline verdict once (exit 0, or every finding and failure is already in the P1 baseline and lies in a file this task did not touch) and reference it at every site: G-2 TF:693; G-4/G-5 TF:699 and TF:702; the gate record TF:735 and the lens TF:745; the per-phase G-4 items TF:260, TF:390 and TF:517; the Gate A-D post-fix re-runs TF:306, 321, 433, 448, 560, 575, 657 and 672; the Final and M4 re-runs TF:778, 793, 821 and 836; and the Gate C lens TF:530. (c) Add the same carve-out to the 3.G2, 9.F2, 9.F11 and 9.F16 agent prompts. (d) Record the lint-architecture prerequisite as its own baseline row and run `uv run ruff check .` directly as well, so ruff always checks the new package even when lint-architecture exits 1 (INV-006). (e) Pin the ruff version used for the baseline and for every comparison (INV-007).

### M-003: Step 6.2 implements the cycle-level stderr fallback when the audit append fails, and the design requires every exit to write an audit line or the stde

- **Severity:** minor
- **Category:** coverage_gap
- **Source findings:** R2-002
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `docs/designs/issue-watcher.md:887` - Every exit writes a schema-valid audit line or the stderr fallback; rotation keeps 4 files
  - `docs/designs/issue-watcher.md:722` - Stderr fallback (`audit.stderr_fallback(reason, exit)`): one JSON line with `kind`, `ts`, `host`, `exit`, `reason` only
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:460` - with `audit.stderr_fallback` when the append fails
- **Claim:** Step 6.2 implements the cycle-level stderr fallback when the audit append fails, and the design requires every exit to write an audit line or the stderr fallback, but the Step 6.6 cycle test list covers only the parseable-line case for each exit code and never injects an append failure into run_cycle.
- **Debate outcome:** X-006: unanimous VALID-MINOR, 95%.
- **Default remediation:** Add a case to the Step 6.6 test item (TF:472): inject an OSError into the audit append inside run_cycle and assert that exactly one stderr line is written with only kind, ts, host, exit and reason, and that the exit code is unchanged.

### M-004: Step 6.2 requires a closed issue, a lost label, a voided approval or a changed Project status to give revalidation_failed with no entry, but the Step 

- **Severity:** minor
- **Category:** coverage_gap
- **Source findings:** R2-001
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `docs/designs/issue-watcher.md:879` - `pending` with `launches` 1 is saved before the launcher is called; the re-read failure skips
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:460` - a closed issue, a lost label, a voided approval or a changed Project status gives `revalidation_failed` with no entry
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:475` - FR-011 (a re-read showing the issue closed gives `revalidation_failed` with no entry;
- **Claim:** Step 6.2 requires a closed issue, a lost label, a voided approval or a changed Project status to give revalidation_failed with no entry, but the Step 6.7 test list covers only the closed-issue case.
- **Debate outcome:** X-007: unanimous VALID-MINOR, 95%.
- **Default remediation:** Add the lost-label, voided-approval and changed-Project-status re-read cases to the Step 6.7 test list (TF:475), each asserting revalidation_failed and no entry.

### M-005: The Step 4.1c wording of backoff_elapsed drops the design's "attempts < 3" conjunct of transition T-2

- **Severity:** minor
- **Category:** coverage_gap
- **Source findings:** R1-001
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `docs/designs/issue-watcher.md:479` - \| T-2 \| `failed` \| now >= `updated_at` + 10 min and `attempts` < 3 \| eligible \| none (re-runs every check) \|
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:336` - `backoff_elapsed(entry, now)` (now >= `updated_at` + 10 min)
- **Claim:** The Step 4.1c wording of backoff_elapsed drops the design's "attempts < 3" conjunct of transition T-2. The behaviour is still covered, because run_cycle applies the attempts check, so the defect is in the wording only.
- **Debate outcome:** X-002: unanimous VALID-MINOR, 95%. T-2 judged covered.
- **Default remediation:** Restore the conjunct at TF:336, or state there that the attempts < 3 check of T-2 is applied in run_cycle and name the test that covers attempts == 3.

### M-006: When the owner withdraws the commit, base-sha.txt is never used and the POST reflect is to run on the working-tree diff (OQ-51), but the Step 10.6 pro

- **Severity:** minor
- **Category:** contradiction
- **Source findings:** R1-003
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:848` - the POST reflect runs with the working-tree diff against HEAD as its change set, and that is documented as an Open Question; see OQ-51
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:860` - first read the SHA from `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/phase-outputs/plans/base-sha.txt` and substitute it for the text `<BASE SHA>`
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:860` - do not paraphrase, summarize, reorder or omit any part
- **Claim:** When the owner withdraws the commit, base-sha.txt is never used and the POST reflect is to run on the working-tree diff (OQ-51), but the Step 10.6 prompt allows only the <BASE SHA> substitution and forbids any other change to the prompt, so the runner has no permitted argument text for that branch.
- **Debate outcome:** C-001: 95% minor (the branch is declared by OQ-51; only the argument text is missing).
- **Default remediation:** Give the Step 10.6 prompt (TF:860) explicit substitution text for the withdrawn-commit branch of TF:848 (the working-tree diff against HEAD), and state that an empty HEAD..HEAD audit is forbidden and does not satisfy Done.

### M-007: The Step 8.x rationale says xdist is supplied "exactly as" CI line 29 does, but CI installs it into the environment with uv pip install, while the tas

- **Severity:** minor
- **Category:** wrong_citation
- **Source findings:** R1-004
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:611` - xdist is not a project dependency, so it is supplied ad hoc exactly as `.github/workflows/test.yml:29` does
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:611` - uv run --offline --with "pytest-xdist>=3.5,<4" pytest -n auto tests/issue_watch/
  - `.github/workflows/test.yml:29` - uv pip install -e ".[dev]" "pytest-xdist>=3.5,<4"
- **Claim:** The Step 8.x rationale says xdist is supplied "exactly as" CI line 29 does, but CI installs it into the environment with uv pip install, while the task supplies it ad hoc with uv run --offline --with. The cited line names a different mechanism.
- **Debate outcome:** C-002: 95% minor.
- **Default remediation:** Correct the TF:611 rationale to say the same version range as .github/workflows/test.yml:29 is used, supplied with uv run --with instead of being installed into the environment.

### M-008: G-10 compares pyproject.toml and the Makefile against the index only (git diff without HEAD or --cached), so a change that is already staged is not se

- **Severity:** minor
- **Category:** gate_weakness
- **Source findings:** R1-005
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:723` - git diff --exit-code pyproject.toml Makefile; echo "EXIT=$?"
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:723` - this gate is run again in P10 after staging
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:851` - PASS only when EVERY staged path starts with one of the six prefixes
- **Claim:** G-10 compares pyproject.toml and the Makefile against the index only (git diff without HEAD or --cached), so a change that is already staged is not seen, and the gate is run again in P10 after staging. The staged-path allowlist at Step 10.3 is the only check that catches it.
- **Debate outcome:** C-003: 95% minor (backstopped by TF:851, INV-014 ADDRESSED).
- **Default remediation:** Change G-10 at TF:723 to compare against HEAD so staged changes are seen: git diff --exit-code HEAD -- pyproject.toml Makefile .github/.

### M-009: The per-phase test-run loop at TF:690 says re-run until PASSED with no attempt cap and no HALT, unlike the Final re-run rule at TF:778

- **Severity:** minor
- **Category:** gate_weakness
- **Source findings:** R3-003
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:690` - IF FAILED, fix the cause (never weaken an assertion) and re-run until PASSED, recording each fix
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:778` - re-run until it passes, recording each fix; IF it cannot be made to pass, HALT
- **Claim:** The per-phase test-run loop at TF:690 says re-run until PASSED with no attempt cap and no HALT, unlike the Final re-run rule at TF:778.
- **Debate outcome:** C-004: 95% minor.
- **Default remediation:** Cap the TF:690 loop the way TF:778 does: if the failure cannot be made to pass (or meet the PASS-baseline verdict of M-002), HALT and record it in the Task Log.

### M-010: The post-fix re-runs repeat Steps 9.4 to 9.16 only, so final-change-set.md (Step 9.F1), final-gate-record.md and ac-trace.md are not regenerated after

- **Severity:** minor
- **Category:** sequencing
- **Source findings:** R3-004
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:742` - a table of every created or changed file (path, line count, creating phase)
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:778` - re-run Steps 9.4 to 9.16 (gate commands G-1 to G-11) in order
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:729` - a GAP is fixed by adding the missing test
- **Claim:** The post-fix re-runs repeat Steps 9.4 to 9.16 only, so final-change-set.md (Step 9.F1), final-gate-record.md and ac-trace.md are not regenerated after a fix cycle, and the M4 reviewers then read a stale change set.
- **Debate outcome:** C-005: 95% minor.
- **Default remediation:** After each post-fix re-run, regenerate final-change-set.md (TF:742), final-gate-record.md (TF:735) and ac-trace.md (TF:729) before any M4 prompt (TF:800) is spawned.

### M-011: Step 4.1 has record import parse_utc, format_utc and valid_issue_number from predicates, while the design import table allows record to take predicate

- **Severity:** minor
- **Category:** contradiction
- **Source findings:** R3-005
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:330` - `predicates` of the package (`parse_utc`, `format_utc`, `valid_issue_number`)
  - `docs/designs/issue-watcher.md:239` - \| `record` \| `predicates` (types only, for `Entry` fields that hold an issue number) \| `superclaude.cli.swarm.atomic` \| none \|
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:751` - check every module of `src/superclaude/cli/issue_watch/` against the import table of `docs/designs/issue-watcher.md` lines 233-242
- **Claim:** Step 4.1 has record import parse_utc, format_utc and valid_issue_number from predicates, while the design import table allows record to take predicates for types only. The departure is not among the declared decisions, so the Final lens and the M4 reviewers, which check against that table and the 29 listed departures, would report it.
- **Debate outcome:** C-006: 67% minor; variant-2 dissented (BLOCKING) and was outvoted 2/3.
- **Default remediation:** Declare the record -> predicates function import as a departure in the TF Open Questions, and add it to the Final lens at TF:751 and to the M4 departure lists (preamble TF:797, prompts TF:806, TF:818 and TF:833).

### M-012: Step 7.x requires the main.py diff to show only the added registration lines, while the later format step tells the worker to fix any finding inside t

- **Severity:** minor
- **Category:** contradiction
- **Source findings:** R3-007
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:502` - ensuring `git diff -- src/superclaude/cli/main.py` shows only these added lines (two code lines plus blank separators) and nothing else in the file changed
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:520` - fix any finding inside those files
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:520` - re-run until both commands exit 0
- **Claim:** Step 7.x requires the main.py diff to show only the added registration lines, while the later format step tells the worker to fix any finding inside the touched files and re-run until exit 0. A pre-existing format hit in main.py would force an edit that breaks the only-these-lines check.
- **Debate outcome:** C-008: 95% minor.
- **Default remediation:** Make TF:502 and TF:520 agree: a format hit in main.py outside the added lines is judged by the PASS-baseline verdict of M-002 and is recorded, not fixed.

### M-013: A failure of the final git add .dev/tasks is only logged and never reverts Done, so the owner is not told that the task package is left unstaged

- **Severity:** minor
- **Category:** gate_weakness
- **Source findings:** R3-008
- **Evidence (re-read by the merge step and by a script; sampled by a validator):**
  - `.dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md:875` - a failure of this staging command is logged in that section and never reverts the Done status
- **Claim:** A failure of the final git add .dev/tasks is only logged and never reverts Done, so the owner is not told that the task package is left unstaged.
- **Debate outcome:** C-009: 67% minor; variant-2 dissented (BLOCKING) and was outvoted 2/3.
- **Default remediation:** State at TF:875 that a staging failure is logged as a follow-up for the owner (a NEEDS OWNER DECISION line naming the unstaged paths).

Dropped from the register: R3-006 (declared deviation DF-46 (R06:180); conceded 3/3 in debate (C-007)).

## Coverage resolution

| Requirement | Final judgement | Task items | Note |
|---|---|---|---|
| [INFERRED] T-2 | covered | Step 4.1c, Step 4.4, Step 6.7 | Wording gap only, see M-005 (attempts < 3 applied in run_cycle). |
| [INFERRED] INF-016 | covered | Step 5.5, Step 6.7, Step 7.4 | Resolved in debate X-005. |
| [INFERRED] INF-123 | partially_covered | Step 7.7, Step 9.5 | Declared deviation DF-05 (R06:28): affected subset locally, full suite CI only. Not a defect (X-003). |
| [INFERRED] INF-155 | partially_covered | Step 9.5, Step 9.9, Step 9.15, Step 9.17 | Declared deviation DF-05 (R06:28). Not a defect (X-004). |
| [INFERRED] INF-146 | partially_covered | Step 2.8, Step 6.6, Step 7.4, Step 7.5 | Cycle-level stderr fallback untested, see M-003 (X-006). |
| [INFERRED] AC-14 | partially_covered | Step 2.3, Step 6.2, Step 7.1, Step 7.2, Step 2.8, Step 6.6 | Cycle-level stderr fallback untested, see M-003 (X-006). |
| [INFERRED] AC-6 | partially_covered | Step 4.1b, Step 4.1c, Step 6.2, Step 6.7, Step 8.2, Step 6.10 | Lost-label, voided-approval and changed-Project-status revalidation cases untested, see M-004 (X-007). |
| [INFERRED] INF-138 | partially_covered | Step 6.7 | Set to partially_covered to match AC-6 (INV-009); see M-004. |

These judgements come from reviewer reading of the task file; they were not re-read line by line by the orchestrator, hence the `[INFERRED]` tag.

## Unresolved invariant probes (adversarial merge)

- INV-001 (high): a re-gate after the POST reflect remediation is not enough for M-001; the report-only change in M-001 is the recommended fix.
- INV-004 (high): the site list for M-002 may be incomplete; the fix defines one baseline verdict and references it at every site.
- INV-005 (high): the M-002 conflict also covers the affected-test gate (G-2), not only lint and format.
- Medium warnings (do not block): INV-002, INV-003, INV-006, INV-008, INV-010.

## Inferred requirements (Pass 2)

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | For at most one such issue per cycle it starts one ordinary top-level agent session through `orca agent launch` with the prompt `/sc:issue --claim <N>`, after durably recording the dispatch. | docs/designs/issue-watcher.md:15-15 | containment (Step 5.1, ratio 0.696) |
| INF-002 | At most one claim session per issue per intact, single dispatch store per login. | docs/designs/issue-watcher.md:17-17 | containment (Step 9.2, ratio 0.6) |
| INF-003 | Trigger label plus approval label, approval actor checked against an allow-list, Project Status `Backlog` | docs/designs/issue-watcher.md:21-21 | containment (Step 2.2, ratio 0.714) |
| INF-004 | `is_intended_owner`: assignee set exactly {own login}; discovery pre-filters with `--assignee` | docs/designs/issue-watcher.md:22-22 | containment (Step 6.2, ratio 0.8) |
| INF-005 | Local dispatch record written durably (`pending`, `launches` + 1) before the spawn, plus the claim marker | docs/designs/issue-watcher.md:23-23 | containment (Step 9.M2, ratio 0.727) |
| INF-006 | No cron entry is enabled and `enabled` stays `false` until an owner-run live test (FU-1) shows the prompt running as a slash command, records the session's permission mode, and replaces every `_assumed_shape` fixture with captured replies under which `tests/issue_watch/` still passes. | docs/designs/issue-watcher.md:33-33 | none |
| INF-007 | The owner commits that record as `docs/designs/issue-watcher-live-test.md`; neither this design nor its implementation writes it. | docs/designs/issue-watcher.md:33-33 | containment (Step 6.2, ratio 0.786) |
| INF-008 | D1 option A (workspace-side poller, pull); D2 claim-only; D3 only a validated integer issue number reaches a session prompt. | docs/designs/issue-watcher.md:39-39 | none |
| INF-009 | The poller never assigns, comments or moves Project items. | docs/designs/issue-watcher.md:44-44 | none |
| INF-010 | The prompt is built only by `launch.build_claim_prompt(n)`, which accepts an `int` (not `bool`) in 1..999999999 and returns `/sc:issue --claim <n>`. No other text reaches the prompt. | docs/designs/issue-watcher.md:45-45 | containment (Step 5.1, ratio 0.938) |
| INF-011 | Module constant `launch.ORCA_AGENT`, pinned by a unit test to the `--agent` value of the seed brief's launch line. Not configurable. | docs/designs/issue-watcher.md:66-66 | containment (Step 5.1, ratio 0.857) |
| INF-012 | Every repository-scoped `gh` call names `IronbellyOrg/IronClaude`; zero `SuperClaude-Org`, zero `{owner}` placeholder (NFR-003). | docs/designs/issue-watcher.md:67-67 | containment (Step 9.F7, ratio 0.733) |
| INF-013 | `gh`, `git` and Orca run as argv lists with `shell=False` (NFR-004). | docs/designs/issue-watcher.md:68-68 | containment (Step 8.3, ratio 0.7) |
| INF-014 | Linux only; `once`, `check-config`, `init-state` exit 2 elsewhere. | docs/designs/issue-watcher.md:69-69 | containment (Step 6.1, ratio 0.75) |
| INF-015 | Network-FS deny-list for `state_dir`: nfs, nfs4, cifs, smb3, sshfs, fuse.sshfs, 9p. | docs/designs/issue-watcher.md:69-69 | containment (Step 6.1, ratio 0.846) |
| INF-016 | NG-1 push designs B/C/D; NG-2 no GitHub write (REST GET only; GraphQL POST only with a constant query without `mutation`); NG-3 no Project writes; NG-4 no session constraint beyond the deployment gate; NG-5 no daemon mode, no in-cycle retry, no automatic Orca retry. | docs/designs/issue-watcher.md:70-70 | none |
| INF-017 | Fail closed, no label-only mode (OD-4). | docs/designs/issue-watcher.md:72-72 | containment (Step 2.2, ratio 0.6) |
| INF-018 | `launch.find_orca(runner, which)` mirrors it with injected seams. `_ORCA_CLIS` (line 35) is imported, not copied. | docs/designs/issue-watcher.md:83-83 | containment (Step 5.1, ratio 0.818) |
| INF-019 | The poller runs `git -C <abs worktree> remote get-url origin` with a timeout and compares the parsed `owner/repo` case-insensitively with `ironbellyorg/ironclaude`. | docs/designs/issue-watcher.md:84-84 | containment (Step 5.1, ratio 0.778) |
| INF-020 | `record` calls it, then fsyncs the state directory itself (NFR-011). | docs/designs/issue-watcher.md:85-85 | containment (Step 6.1, ratio 0.625) |
| INF-021 | Only the paging rule is reused: a page under 100 ends the read, a repeated id fails, the read must complete. | docs/designs/issue-watcher.md:86-86 | containment (Step 3.1c, ratio 0.75) |
| INF-022 | The NFR-014 dependency rules need a new AST test, `tests/issue_watch/test_module_boundaries.py`. The package must not rebind `ID_PATTERNS`, `THRESHOLDS` or any other `contracts.__all__` name and must not contain an `ID_PATTERNS` body literal such as `FR-\d+(?:\.\d+)?` (`contracts/__init__.py:64-77`). | docs/designs/issue-watcher.md:90-90 | none |
| INF-023 | NFR-012 forbids a new dependency. | docs/designs/issue-watcher.md:96-96 | containment (Step 8.3, ratio 0.6) |
| INF-024 | `status` prints the full original argv plus `--retry-launch <id>`, with `cwd` (section 10.2). | docs/designs/issue-watcher.md:101-101 | containment (Step 5.1, ratio 0.833) |
| INF-025 | Section 6.3: the text wins; after one launch the remaining candidates get no stamp and no decision line. | docs/designs/issue-watcher.md:104-104 | containment (Step 6.1, ratio 0.818) |
| INF-026 | The Click group is `issue_watch_group`, exposed as `superclaude issue-watch`. | docs/designs/issue-watcher.md:110-110 | containment (Step 7.1, ratio 0.857) |
| INF-027 | `once` \| `--dry-run`, `--config <path>` \| Non-blocking `flock`, whole cycle \| `dispatch.json` (not in dry-run), `audit.jsonl`, `dry-run.json` (dry-run only) \| `gh`, `git`, Orca probe, Orca launch (not in dry-run) \| 0, 2, 3, 4, 5, 6, 7, 75 | docs/designs/issue-watcher.md:114-114 | containment (Step 6.2, ratio 0.8) |
| INF-028 | `status` \| `--json`, `--config <path>` \| None (read-only) \| None; no file's mtime changes (FR-021) \| None \| 0 healthy, 1 unhealthy (age above 900 s or no qualifying cycle), 2 config invalid, 6 store unreadable | docs/designs/issue-watcher.md:115-115 | containment (Step 7.4, ratio 0.667) |
| INF-029 | `check-config` \| `--config <path>` \| None \| None \| None \| 0 valid, 2 invalid or platform unsupported or network-FS `state_dir` | docs/designs/issue-watcher.md:116-116 | containment (Step 6.1, ratio 0.714) |
| INF-030 | `init-state` \| `--config <path>` \| Creates it \| Creates `state_dir` (0700), `dispatch.json` (0600), `lock` (0600) \| None \| 0 created, 2 config or platform, 6 a store already exists or the directory is unwritable | docs/designs/issue-watcher.md:117-117 | containment (Step 7.1, ratio 0.773) |
| INF-031 | `reset <N> --forfeit-guarantee` \| `--config <path>` \| Non-blocking `flock` \| Removes entry N; appends its `consumed_at` to `consumed_log`; one audit line \| None \| 0 done, 2 usage (entry not `abandoned`/`unknown`, or flag missing), 6 store, 75 lock held | docs/designs/issue-watcher.md:118-118 | containment (Step 7.5, ratio 0.786) |
| INF-032 | `reset --rate-limit` \| `--config <path>` \| Non-blocking `flock` \| Clears `next_permitted_at`; one audit line \| None \| 0, 6, 75 | docs/designs/issue-watcher.md:119-119 | containment (Step 7.2, ratio 0.733) |
| INF-033 | `reset` with both `<N>` and `--rate-limit`, or with neither, is a usage error (exit 2). `reset <N>` without `--forfeit-guarantee` is a usage error. | docs/designs/issue-watcher.md:121-121 | containment (Step 7.2, ratio 1.0) |
| INF-034 | Loaded by `cycle.load_config(path) -> Config`; validated by the same function `check-config` uses. | docs/designs/issue-watcher.md:125-125 | containment (Step 6.1, ratio 0.636) |
| INF-035 | `enabled` \| bool \| no \| `false` \| A JSON boolean; `false` makes `once` exit 0 `not_enabled` before any external call | docs/designs/issue-watcher.md:130-130 | containment (Step 6.1, ratio 0.75) |
| INF-036 | `labels.trigger` \| string \| no \| `issue-watch:trigger` \| Non-empty, at most 50 characters, no control characters; matched exact and case-sensitive | docs/designs/issue-watcher.md:131-131 | containment (Step 6.1, ratio 0.765) |
| INF-037 | `project_id` \| string \| yes \| none \| Matches `^PVT_[A-Za-z0-9_-]{1,64}$` [PROPOSAL; Projects v2 node-id prefix is UNVERIFIED, FU-3] | docs/designs/issue-watcher.md:133-133 | none |
| INF-038 | `owner_account_id` \| int \| no \| absent \| If present, an `int` (not `bool`) in 1..10^20−1; a mismatch with `gh api user` `.id` is exit 2 `account_id_mismatch` at cycle time | docs/designs/issue-watcher.md:134-134 | containment (Step 6.1, ratio 0.647) |
| INF-039 | `worktree` \| string \| yes \| none \| Absolute path, existing directory (`worktree_invalid`) | docs/designs/issue-watcher.md:135-135 | containment (Step 6.1, ratio 0.889) |
| INF-040 | `approvers_file` \| string \| yes \| none \| Absolute path; file rules below (`approvers_invalid`) | docs/designs/issue-watcher.md:136-136 | containment (Step 6.1, ratio 0.7) |
| INF-041 | `state_dir` \| string \| no \| `${XDG_STATE_HOME:-$HOME/.local/state}/superclaude/issue-watch/` \| Absolute after expansion; not on a deny-listed filesystem (`state_dir_unwritable` is exit 6 only when writing fails; a network FS is exit 2 `config_invalid`) | docs/designs/issue-watcher.md:137-137 | containment (Step 6.1, ratio 0.818) |
| INF-042 | Unknown keys are rejected (exit 2), so a typo such as `enable` cannot silently leave the poller on its default. | docs/designs/issue-watcher.md:139-139 | none |
| INF-043 | `check-config` prints the file's mtime (UTC ISO 8601) and the entry count (R10), and nothing else about its content. | docs/designs/issue-watcher.md:151-151 | containment (Step 7.4, ratio 0.733) |
| INF-044 | 2 \| Usage, config, platform, origin, Orca probe \| `config_invalid`, `approvers_invalid`, `platform_unsupported`, `worktree_invalid`, `origin_mismatch`, `orca_not_found`, `account_id_mismatch` | docs/designs/issue-watcher.md:158-158 | none |
| INF-045 | 3 \| GitHub auth, scope, timeout, non-JSON \| `login_invalid`, `gh_auth_failed`, `gh_timeout`, `gh_non_json`, `project_read_failed` | docs/designs/issue-watcher.md:159-159 | containment (Step 6.2, ratio 0.909) |
| INF-046 | 4 \| Discovery truncated or duplicated \| `truncated`, `discovery_duplicate` | docs/designs/issue-watcher.md:160-160 | containment (Step 3.1c, ratio 0.8) |
| INF-047 | 5 \| Rate limited \| `rate_limited`, `rate_limit_clamped` | docs/designs/issue-watcher.md:161-161 | containment (Step 3.1b, ratio 0.75) |
| INF-048 | 6 \| Store or lock \| `store_invalid`, `store_missing`, `lock_missing`, `lock_invalid`, `state_dir_unwritable` | docs/designs/issue-watcher.md:162-162 | containment (Step 7.2, ratio 1.0) |
| INF-049 | 7 \| An entry was written `failed`, `unknown` or `abandoned` `spawn_error` this cycle \| `prompt_invalid`, `revalidation_transient`, `launch_unknown`, `spawn_error` | docs/designs/issue-watcher.md:163-163 | containment (Step 6.2, ratio 0.909) |
| INF-050 | 75 \| Lock held or the lock inode changed \| `lock_held` | docs/designs/issue-watcher.md:164-164 | containment (Step 6.2, ratio 0.857) |
| INF-051 | When several conditions hold, the cycle exits with the first of 2, 6, 7, 5, 3, 4. | docs/designs/issue-watcher.md:166-166 | none |
| INF-052 | Exit 75 applies only when the lock was not taken, or its inode changed, and nothing else ran. | docs/designs/issue-watcher.md:166-166 | containment (Step 6.2, ratio 0.6) |
| INF-053 | Precedence is computed by one pure function, `cycle.resolve_exit(conditions: frozenset[int]) -> int`. | docs/designs/issue-watcher.md:166-166 | containment (Step 6.1, ratio 0.909) |
| INF-054 | `CommandResult` dataclass; `Runner` Protocol; `SubprocessRunner.run(argv, timeout)` which rejects a `str` argv with `TypeError`, runs `subprocess.run(list, shell=False, capture_output=True, text=True, timeout=t, stdin=DEVNULL)`, truncates stderr to 500 bytes (T11), and maps `TimeoutExpired` to `CommandResult(timed_out=True)` and `OSError` to `CommandResult(spawn_error=...)` | docs/designs/issue-watcher.md:218-218 | containment (Step 2.1, ratio 0.921) |
| INF-055 | Builds every `gh` argv from module constants (section 8); runs it through the runner with a timeout supplied by the cycle; parses JSON; follows paging; classifies replies into `ok`, `timeout`, `non_json`, `auth_failed`, `scope_missing`, `rate_limited`, `transient` (5xx), `failed`; counts calls against the per-cycle `CallBudget` | docs/designs/issue-watcher.md:219-219 | none |
| INF-056 | Frozen dataclasses (`Login`, `DiscoveredIssue`, `LabelEvent`, `IssueSnapshot`, `ProjectItem`, `MarkerEvidence`, `EditEvidence`); pure functions for each Section 3 definition; `CLAIM_MARKER`; `is_intended_owner`; `approval_of(events, ...) -> ApprovalResult`; `eligibility_order(...)` | docs/designs/issue-watcher.md:220-220 | containment (Step 2.2, ratio 0.947) |
| INF-057 | `Store` Protocol; `FileStore` (load, validate, migrate, save); `Lock` (open with `O_NOFOLLOW`, `flock`, inode check); `Entry` and `StoreDoc` dataclasses; one function per section 7 transition row; `sweep(store, now)`; `day_cap_count(store, now)`; `disabled_present(state_dir)`; `init_state(state_dir, now)` | docs/designs/issue-watcher.md:221-221 | containment (Step 4.1a, ratio 0.625) |
| INF-058 | `ORCA_AGENT` constant; `build_claim_prompt(n)`; `find_orca(runner, which)`; `parse_origin(url)`; `check_origin(runner, worktree, timeout)`; `Launcher` Protocol; `OrcaLauncher.launch(...) -> LaunchOutcome` | docs/designs/issue-watcher.md:222-222 | containment (Step 5.1, ratio 0.938) |
| INF-059 | `AuditLog.append(line)` (one `os.write` on an `O_APPEND` fd), `AuditLog.rotate_if_needed()` (called only by a lock holder), `stderr_fallback(line)`; the `REASONS` frozenset with kind and exit per reason; line builders `cycle_line(...)`, `decision_line(...)`, `warning_line(...)` | docs/designs/issue-watcher.md:223-223 | containment (Step 2.3, ratio 1.0) |
| INF-060 | `Config` and `load_config`; `validate_approvers`; `Clock` Protocol and `SystemClock`; `Deadline` (240 s, 5 s floor, 120 s launch cutoff); `run_cycle(deps, dry_run) -> CycleResult`; `resolve_exit`; `status_report(store, audit, now)`; the NFR-013 reducer `slo_numbers(lines, store, now)` | docs/designs/issue-watcher.md:224-224 | containment (Step 6.1, ratio 0.75) |
| INF-061 | Anything not listed is forbidden; `tests/issue_watch/test_module_boundaries.py` walks each module's AST and fails on any other `superclaude.*` import. | docs/designs/issue-watcher.md:231-231 | containment (Step 8.8, ratio 0.786) |
| INF-062 | Platform check (`sys.platform == "linux"`), `load_config`, `enabled` (skipped in dry-run), `validate_approvers`, worktree absolute and a directory, network-FS check of `state_dir` via `/proc/self/mountinfo` | docs/designs/issue-watcher.md:344-344 | containment (Step 6.1, ratio 0.81) |
| INF-063 | `record.sweep(store, now)`: every `pending` -> `abandoned` `pending_orphan`; every `launched` past `lease_expires_at` -> `abandoned` `claim_not_observed` (dry-run: report only) | docs/designs/issue-watcher.md:350-350 | containment (Step 4.1c, ratio 0.933) |
| INF-064 | Order candidates: never-examined first (ascending number), then by `considered[n]` ascending; drop to `max_candidates` | docs/designs/issue-watcher.md:352-352 | containment (Step 2.2, ratio 0.727) |
| INF-065 | Per candidate, GitHub checks in order: marker (for every entry state that can reach `claimed`), approval events, edit timestamps, `projectItems` | docs/designs/issue-watcher.md:354-354 | containment (Step 6.2, ratio 0.857) |
| INF-066 | First fully eligible candidate: `find_orca` (cached), `build_claim_prompt`, re-read, day cap, DISABLED, origin re-check, `pending` write, spawn | docs/designs/issue-watcher.md:355-355 | containment (Step 6.2, ratio 0.778) |
| INF-067 | Health stamp: only an exit-0 cycle that is not DISABLED, `not_enabled`, `disabled_mid_cycle` or dry-run writes `last_completed_cycle_at` | docs/designs/issue-watcher.md:357-357 | containment (Step 6.2, ratio 1.0) |
| INF-068 | Dry-run differences: step 1 ignores `enabled`; steps 7, 12 and 13 compute but do not write `dispatch.json`; | docs/designs/issue-watcher.md:362-362 | containment (Step 6.2, ratio 0.769) |
| INF-069 | "Examined" stops at the first eligible candidate: after the launch, and after any launch-step outcome, later candidates are neither read nor stamped (FR-016, PF-029). | docs/designs/issue-watcher.md:386-386 | containment (Step 6.2, ratio 0.778) |
| INF-070 | Failure is exit 6 with the file untouched (NFR-011). | docs/designs/issue-watcher.md:439-439 | containment (Step 6.6, ratio 0.833) |
| INF-073 | Day cap \| 6 in (now − 24 h, now] \| count `t` with now − 24 h < t <= now over every entry's `consumed_at` and `consumed_log` | docs/designs/issue-watcher.md:500-500 | containment (Step 4.1c, ratio 1.0) |
| INF-074 | Marker window \| at or after `pending_at` − 300 s; else after the current `approved_at` \| `marker_time >= pending_at - 300s` | docs/designs/issue-watcher.md:502-502 | containment (Step 6.2, ratio 0.7) |
| INF-075 | serialise with `json.dumps(doc, sort_keys=True, indent=2, ensure_ascii=True).encode() + b"\n"`; call `write_prepared_bytes(state_dir / "dispatch.json", data)`; then `os.chmod(path, 0o600)`; then open `state_dir` with `os.open(dir, O_RDONLY \| O_DIRECTORY)`, `os.fsync(fd)`, close. | docs/designs/issue-watcher.md:509-509 | containment (Step 4.1b, ratio 0.871) |
| INF-076 | `fd = os.open(lock, O_RDWR \\| O_NOFOLLOW \\| O_CLOEXEC)` \| `FileNotFoundError`: 6 `lock_missing`; `ELOOP` (symlink): 6 `lock_invalid`; `EISDIR`: 6 `lock_invalid` | docs/designs/issue-watcher.md:515-515 | containment (Step 4.1b, ratio 0.857) |
| INF-077 | `fcntl.flock(fd, LOCK_EX \\| LOCK_NB)` \| `BlockingIOError`: 75 `lock_held` | docs/designs/issue-watcher.md:517-517 | containment (Step 4.1b, ratio 0.75) |
| INF-078 | At no point can a rerun see `launches == 0` for an issue whose spawn may have started, which is the at-most-once argument. | docs/designs/issue-watcher.md:533-533 | containment (Step 8.4, ratio 0.6) |
| INF-079 | G1 \| Own login (FR-002) \| `gh api user --include` \| parse the status line, headers, blank line, then JSON; keep `.login`, `.id`, header `Date` | docs/designs/issue-watcher.md:543-543 | containment (Step 3.2, ratio 0.762) |
| INF-080 | G2 \| Discovery (FR-003) \| `gh issue list --repo R --state open --label <trigger> --assignee <login> --json number,labels,assignees,state -L 100` | docs/designs/issue-watcher.md:544-544 | containment (Step 3.1a, ratio 0.95) |
| INF-081 | G3 \| Events (FR-005, FR-006, renamed check) \| `gh api --method GET repos/R/issues/N/events -F per_page=100 -F page=P --jq EVENTS_JQ` | docs/designs/issue-watcher.md:545-545 | containment (Step 3.1a, ratio 0.8) |
| INF-082 | G4 \| Claim marker (FR-009) \| `gh api --method GET repos/R/issues/N/comments -F per_page=100 -F page=P --jq MARKER_JQ` | docs/designs/issue-watcher.md:546-546 | containment (Step 3.1a, ratio 0.882) |
| INF-083 | G5 \| Edit timestamps (Section 3 Unchanged) \| `gh api graphql -f query=EDITS_QUERY -F number=N [-f after=<cursor>]` | docs/designs/issue-watcher.md:547-547 | containment (Step 3.1a, ratio 0.75) |
| INF-084 | G6 \| Project items (FR-007) \| `gh api graphql -f query=PROJECT_ITEMS_QUERY -F number=N [-f after=<cursor>]` | docs/designs/issue-watcher.md:548-548 | containment (Step 3.1a, ratio 0.75) |
| INF-085 | G7 \| Re-read issue (FR-011) \| `gh api --method GET repos/R/issues/N --jq REREAD_JQ` | docs/designs/issue-watcher.md:549-549 | containment (Step 3.1a, ratio 0.857) |
| INF-086 | `--method GET` is written on every REST path call. | docs/designs/issue-watcher.md:554-554 | containment (Step 3.G7, ratio 0.833) |
| INF-087 | A test asserts no query constant contains `mutation` (NG-2) and every constant contains the literal repository. | docs/designs/issue-watcher.md:555-555 | containment (Step 8.3, ratio 0.909) |
| INF-088 | No argv names `title`, `body` or a comment body field as an output field. | docs/designs/issue-watcher.md:556-556 | containment (Step 3.1a, ratio 0.889) |
| INF-089 | Project ids are compared in Python (`project.id == config.project_id`); the id never enters an argv, so a hostile config value cannot alter a query. | docs/designs/issue-watcher.md:558-558 | none |
| INF-090 | Launch argv (FR-013), exactly 12 elements, built by `launch.launch_argv(orca, worktree, prompt) -> list[str]`: | docs/designs/issue-watcher.md:618-618 | containment (Step 5.1, ratio 0.867) |
| INF-091 | exit 0 without that id, non-JSON, non-zero exit, `agent_session_operation_unknown` anywhere in stdout or stderr \| `unknown` \| `unknown`, `operation_id` kept if one was parsed | docs/designs/issue-watcher.md:634-634 | containment (Step 5.1, ratio 0.944) |
| INF-092 | Orca launch \| 120 s, never shortened \| not started when `elapsed() > 120`; the step ends with no entry and no reason other than a `budget_exhausted` decision line | docs/designs/issue-watcher.md:647-647 | containment (Step 6.2, ratio 0.812) |
| INF-093 | Latest `labeled` approval event; `actor_id` in the approvers set; later `unlabeled` voids it | docs/designs/issue-watcher.md:658-658 | containment (Step 2.2, ratio 0.9) |
| INF-094 | `actor_type == "User"` and login not ending `[bot]` | docs/designs/issue-watcher.md:659-659 | containment (Step 2.2, ratio 1.0) |
| INF-095 | Body, non-own comments and `renamed` events all older than the approval | docs/designs/issue-watcher.md:660-660 | containment (Step 2.2, ratio 0.875) |
| INF-096 | Deployment gate; no permission flag in the argv | docs/designs/issue-watcher.md:666-666 | containment (Step 5.G7, ratio 0.8) |
| INF-097 | `lstat`, `S_ISREG`, `st_uid`, mode `& 0o022 == 0`, line regex, at least one ID | docs/designs/issue-watcher.md:669-669 | containment (Step 6.1, ratio 0.8) |
| INF-098 | An id that fails it is stored as `null` and the outcome is `unknown`. | docs/designs/issue-watcher.md:689-689 | containment (Step 5.1, ratio 0.833) |
| INF-099 | The property test draws `n` from integers, hostile strings, floats and booleans, and asserts every recorded `--prompt` matches `^/sc:issue --claim [1-9][0-9]{0,8}$`. | docs/designs/issue-watcher.md:693-693 | containment (Step 8.3, ratio 0.867) |
| INF-100 | One JSON object per line, written with one `os.write` on an `O_WRONLY \| O_APPEND \| O_CREAT` fd (mode 0600). | docs/designs/issue-watcher.md:699-699 | containment (Step 2.3, ratio 0.857) |
| INF-101 | `rate_remaining`, titles, bodies, label names and stderr text are never keys (NFR-006, T11). | docs/designs/issue-watcher.md:718-718 | none |
| INF-102 | if `audit.jsonl` is at least 5 MiB, `os.replace` `.3` to `.4`, `.2` to `.3`, `.1` to `.2`, current to `.1`, then a directory fsync. The exit-75 path appends and never rotates. | docs/designs/issue-watcher.md:720-720 | containment (Step 2.3, ratio 0.867) |
| INF-103 | `retry[].argv` is the original 12-element launch argv with `--retry-launch <operation_id>` inserted before `--json`, rebuilt from the entry, `ORCA_AGENT` and `build_claim_prompt(issue)` | docs/designs/issue-watcher.md:741-741 | containment (Step 5.1, ratio 0.941) |
| INF-104 | (a) p95 of the `launched` decision `ts` minus its `approved_at`; (b) share of exit-0 cycle lines over 7 days, excluding `disabled`, `not_enabled` and `dry_run`; (c) share of `launched` entries that reached `claimed` before `lease_expires_at`; (d) count of `stale` entries. | docs/designs/issue-watcher.md:745-745 | containment (Step 6.3, ratio 0.917) |
| INF-105 | `src/superclaude/cli/main.py` \| Two lines after line 561, same pattern as `reflect_group` (lines 559 and 561) | docs/designs/issue-watcher.md:760-760 | containment (Step 7.3, ratio 0.867) |
| INF-106 | `tests/issue_watch/__init__.py`, `conftest.py` \| Package marker (C14); `FakeRunner`, `FakeClock`, `FakeLauncher`, `tmp_state` fixtures | docs/designs/issue-watcher.md:761-761 | containment (Step 6.4, ratio 0.714) |
| INF-107 | `tests/issue_watch/test_{runner,github,predicates,record,launch,audit,cycle,cli}.py` \| One file per module | docs/designs/issue-watcher.md:762-762 | containment (Step 5.G4, ratio 0.933) |
| INF-108 | `tests/issue_watch/test_{cli_e2e,security_invariants,crash_injection,concurrency,no_shell,no_text,origin_parity,marker_contract,find_orca_parity,module_boundaries,slo_helper}.py` \| Spec-named and design-added cross-cutting tests | docs/designs/issue-watcher.md:763-763 | none |
| INF-109 | `tests/issue_watch/fixtures/_assumed_shape/*.json` \| Assumed `gh` and Orca replies, replaced by FU-1 | docs/designs/issue-watcher.md:764-764 | containment (Step 3.5, ratio 0.818) |
| INF-110 | `tests/issue_watch/stubs/gh`, `stubs/orca` \| Executable PATH stubs for `test_cli_e2e.py` | docs/designs/issue-watcher.md:765-765 | containment (Step 8.1, ratio 0.909) |
| INF-111 | `docs/designs/issue-watcher-setup.md` \| Runbook steps 1 to 10 for the owner | docs/designs/issue-watcher.md:766-766 | containment (Step 9.1, ratio 1.0) |
| INF-112 | Not changed: `pyproject.toml` (no dependency, no marker, no entry point), `Makefile`, CI, any file under `.claude/`. | docs/designs/issue-watcher.md:768-768 | containment (Step 9.15, ratio 1.0) |
| INF-113 | No test runs a real `gh`, `orca`, `git` or network call. Every external effect goes through a fake or a PATH stub. | docs/designs/issue-watcher.md:772-772 | containment (Step 8.G7, ratio 0.6) |
| INF-114 | `test_crash_injection.py` \| per C1 to C5, run, crash, rerun: total fresh launches per issue ≤ 1 (NFR-005) | docs/designs/issue-watcher.md:784-784 | containment (Step 8.4, ratio 0.846) |
| INF-115 | `test_concurrency.py` \| two `multiprocessing` processes on one `tmp_path` store: one exits 75 `lock_held`, one launch total | docs/designs/issue-watcher.md:785-785 | containment (Step 8.5, ratio 0.933) |
| INF-116 | `test_cycle.py::test_fifty_cycles` \| 50 cycles over a changing fixture: `launches` never exceeds 1 per issue | docs/designs/issue-watcher.md:786-786 | containment (Step 6.8, ratio 1.0) |
| INF-117 | `test_cycle.py::test_acceptance_property` \| for N in {1, 2, 6, 7, 50, 99}: at most 1 launch per cycle; after 24 h of cycles exactly min(N, 6) launched and the rest `day_cap`; after +24 h one more per cycle | docs/designs/issue-watcher.md:787-787 | containment (Step 6.8, ratio 0.947) |
| INF-118 | `test_no_shell.py` \| AST: no `shell=True`, no `os.system`, no `subprocess` outside `runner.py` | docs/designs/issue-watcher.md:788-788 | containment (Step 8.6, ratio 1.0) |
| INF-119 | `test_no_text.py` \| hostile titles, bodies and stderr (`PWNED-TITLE`) never appear in audit, store, prompt or stdout | docs/designs/issue-watcher.md:789-789 | containment (Step 8.7, ratio 0.714) |
| INF-120 | `test_module_boundaries.py` \| AST import graph matches section 5.3; no module named `select` | docs/designs/issue-watcher.md:790-790 | containment (Step 8.8, ratio 0.8) |
| INF-121 | `test_marker_contract.py` \| `CLAIM_MARKER` occurs in `refs/claim.md` and `templates/claim-comment.md`, read through the dual surface | docs/designs/issue-watcher.md:791-791 | containment (Step 5.8, ratio 0.8) |
| INF-122 | `uv run pytest tests/issue_watch/ -v` \| spec line 366 \| fast loop | docs/designs/issue-watcher.md:797-797 | containment (Step 9.M1, ratio 0.7) |
| INF-123 | `make test` \| `Makefile:13-15` \| CI uses `-n auto` (`test.yml:47`), C11 | docs/designs/issue-watcher.md:798-798 | none |
| INF-124 | `make lint` \| `Makefile:48-50` \| includes `lint-architecture` (C8); ruff 0.15.20, select `E,F,I,N,W,TID`, line length 88, py310 (`pyproject.toml:54,174-184`) | docs/designs/issue-watcher.md:799-799 | none |
| INF-125 | `uv run ruff format --check src/ tests/` \| `test.yml:106` \| no make target (C10) | docs/designs/issue-watcher.md:800-800 | containment (Step 3.G2, ratio 0.692) |
| INF-126 | `make verify-deps` \| `Makefile:356-358`, `test.yml:123` \| passes with no new dependency | docs/designs/issue-watcher.md:801-801 | containment (Step 9.9, ratio 0.667) |
| INF-127 | The Python floor is 3.10 (`pyproject.toml:16`, CI `test.yml:22`): no `tomllib`, no `datetime.UTC` (use `timezone.utc`). | docs/designs/issue-watcher.md:805-805 | containment (Step 6.1, ratio 0.625) |
| INF-128 | `max_launches_per_cycle` \| 1 \| caps blast radius of a bad cycle | docs/designs/issue-watcher.md:812-812 | none |
| INF-129 | call cap \| 35, 3 reserved \| worst cycle 37 calls, 8.88% of 5,000 an hour | docs/designs/issue-watcher.md:814-814 | none |
| INF-130 | day cap \| 6 per rolling 24 h \| bounds sessions the owner must review | docs/designs/issue-watcher.md:816-816 | containment (Step 9.M1, ratio 0.625) |
| INF-131 | The implementer records each UNVERIFIED answer in the matching `_assumed_shape` fixture name and in `issue-watcher-live-test.md`. | docs/designs/issue-watcher.md:847-847 | containment (Step 5.1, ratio 0.692) |
| INF-132 | All criteria run under `uv run pytest tests/issue_watch/` with fakes or PATH stubs only. | docs/designs/issue-watcher.md:870-870 | containment (Step 8.G2, ratio 0.8) |
| INF-133 | One `once` runs the FR-001 order; `FakeRunner` sees G1 first and no argv after an exit decision | docs/designs/issue-watcher.md:874-874 | containment (Step 6.7, ratio 0.692) |
| INF-134 | Discovery argv equals the FR-003 literal; 100 results or a repeated number exits 4 | docs/designs/issue-watcher.md:875-875 | containment (Step 6.6, ratio 0.818) |
| INF-135 | Approval table: outsider, bot, unlabel, relabel, incomplete history, edit after approval each skip with their reason | docs/designs/issue-watcher.md:876-876 | none |
| INF-136 | Project and owner tables: wrong project, not Backlog, unassigned, other assignee skip | docs/designs/issue-watcher.md:877-877 | containment (Step 2.7, ratio 0.7) |
| INF-137 | An own-login marker comment yields `claimed` and no launch | docs/designs/issue-watcher.md:878-878 | containment (Step 6.2, ratio 0.714) |
| INF-138 | `pending` with `launches` 1 is saved before the launcher is called; the re-read failure skips | docs/designs/issue-watcher.md:879-879 | containment (Step 6.2, ratio 0.778) |
| INF-139 | Every recorded prompt matches the D3 regex over the hostile corpus; non-int input raises | docs/designs/issue-watcher.md:880-880 | none |
| INF-140 | Launch argv equals the 12-element list; outcome table maps to `launched`, `failed`, `unknown`, `abandoned` | docs/designs/issue-watcher.md:881-881 | containment (Step 5.1, ratio 0.769) |
| INF-141 | No automatic retry; `status` lists the full retry argv for an `unknown` entry | docs/designs/issue-watcher.md:882-882 | containment (Step 7.4, ratio 0.889) |
| INF-142 | Budget, day cap and `consumed_log` hold through `reset`; acceptance property passes | docs/designs/issue-watcher.md:883-883 | none |
| INF-143 | Second process exits 75; symlinked or foreign lock exits 6 | docs/designs/issue-watcher.md:884-884 | containment (Step 8.5, ratio 0.75) |
| INF-144 | `DISABLED` and `enabled: false` exit 0 before any external call | docs/designs/issue-watcher.md:885-885 | containment (Step 6.2, ratio 1.0) |
| INF-145 | Dry-run writes only `dry-run.json` and audit; the real store is byte-identical | docs/designs/issue-watcher.md:886-886 | containment (Step 4.3, ratio 0.818) |
| INF-146 | Every exit writes a schema-valid audit line or the stderr fallback; rotation keeps 4 files | docs/designs/issue-watcher.md:887-887 | containment (Step 2.8, ratio 0.636) |
| INF-147 | Shared-input failures map to exits 2, 3, 5, 6, 7 with the precedence 2, 6, 7, 5, 3, 4 | docs/designs/issue-watcher.md:888-888 | none |
| INF-148 | Origin mismatch exits 2; parity table agrees with `origin_repo.py` | docs/designs/issue-watcher.md:889-889 | containment (Step 6.6, ratio 0.625) |
| INF-149 | Each verb's exit codes match section 4; `check-config` and `status` write nothing | docs/designs/issue-watcher.md:890-890 | containment (Step 6.1, ratio 0.8) |
| INF-150 | Rate limit persists `next_permitted_at`, clamps to 3600 s, and `reset --rate-limit` clears it | docs/designs/issue-watcher.md:891-891 | containment (Step 6.6, ratio 0.8) |
| INF-151 | A sleeping stub ends with `gh_timeout`; no launch starts after 120 s | docs/designs/issue-watcher.md:892-892 | none |
| INF-152 | Argv prefix scan: only G1 to G7, `--method GET`, no upstream name | docs/designs/issue-watcher.md:893-893 | containment (Step 3.6, ratio 0.667) |
| INF-153 | `test_no_shell.py` passes | docs/designs/issue-watcher.md:894-894 | containment (Step 2.1, ratio 0.667) |
| INF-154 | Crash points C1 to C5 and 50 cycles never exceed one launch per issue | docs/designs/issue-watcher.md:895-895 | containment (Step 8.G6, ratio 0.727) |
| INF-155 | No new dependency; gates in section 13 pass | docs/designs/issue-watcher.md:896-896 | containment (Step 9.F4, ratio 0.667) |
| INF-156 | `slo_numbers` returns the four values on a fixture log | docs/designs/issue-watcher.md:897-897 | containment (Step 6.9, ratio 0.833) |
| INF-157 | Module-boundary and parity tests pass | docs/designs/issue-watcher.md:898-898 | containment (Step 5.G6, ratio 0.8) |

Postscript: 2 rows (INF-071, INF-072) were dropped at extraction because their quote overlaps a parsed requirement span (parsed wins; not citation drops).

## Validator context doubts
- M-002-E4: Line 735 says every gate row must be PASS and a FAIL is fixed. M-002-E1 to E3 (lines 693, 699, 702) say a failure in a file this task did not touch is recorded and not fixed. If M-002 claims these rules are consistent, this entry only shows the 'all PASS' requirement. It does not show how a pre-existing failure in an untouched file is meant to resolve. Treat it as support for a contradiction claim only, not for a harmony claim.

## Inferred-claim audit

- `citations_inferred: 8`
- Inferred-fraction: `8 / 191` = 0.04

## Recommendations

### Recommendation R-001: Make the Step 10.6 POST reflect report-only: drop --remediate from the Step 10.6 skill arguments and replace item 3 at TF:866 with "any Regr

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** Make the Step 10.6 POST reflect report-only: drop --remediate from the Step 10.6 skill arguments and replace item 3 at TF:866 with "any Regression or unauthorized Drift HALTs the task; write it to the Task Log and report it to the owner; do not edit source and do not create a second commit". A re-gate after remediation is not sufficient (INV-001), and the runner must never answer the remediation handoff itself (INV-002). If the owner later chooses a re-gate, it uses the PASS-baseline verdict defined in M-002 (INV-003).
- **Verifier:** Re-read Step 10.6 (task file lines 860-868): the skill arguments hold no `--remediate` and item 3 says HALT; `grep -n -- '--remediate' <task file>` shows no hit in Step 10.6.
- **Linked deviation(s):** M-001
- **Priority:** P0

### Recommendation R-002: (a) Add a P1 baseline step that records the output of `make lint`, the pinned ruff 0.15.20 format check and the G-2 affected test subset bef

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** (a) Add a P1 baseline step that records the output of `make lint`, the pinned ruff 0.15.20 format check and the G-2 affected test subset before any source change. (b) Define one PASS-baseline verdict once (exit 0, or every finding and failure is already in the P1 baseline and lies in a file this task did not touch) and reference it at every site: G-2 TF:693; G-4/G-5 TF:699 and TF:702; the gate record TF:735 and the lens TF:745; the per-phase G-4 items TF:260, TF:390 and TF:517; the Gate A-D post-fix re-runs TF:306, 321, 433, 448, 560, 575, 657 and 672; the Final and M4 re-runs TF:778, 793, 821 and 836; and the Gate C lens TF:530. (c) Add the same carve-out to the 3.G2, 9.F2, 9.F11 and 9.F16 agent prompts. (d) Record the lint-architecture prerequisite as its own baseline row and run `uv run ruff check .` directly as well, so ruff always checks the new package even when lint-architecture exits 1 (INV-006). (e) Pin the ruff version used for the baseline and for every comparison (INV-007).
- **Verifier:** Re-read Steps 9.7, 9.8 and 9.5 and confirm each defines PASS against the P1 baseline record; `grep -c 'PASS-baseline' <task file>` is at least 20 and the baseline item exists in Phase 1.
- **Linked deviation(s):** M-002
- **Priority:** P0

### Recommendation R-003: Add a case to the Step 6.6 test item (TF:472): inject an OSError into the audit append inside run_cycle and assert that exactly one stderr l

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** Add a case to the Step 6.6 test item (TF:472): inject an OSError into the audit append inside run_cycle and assert that exactly one stderr line is written with only kind, ts, host, exit and reason, and that the exit code is unchanged.
- **Verifier:** Re-read Step 6.6 (task file line 472): it names an injected append OSError and the five-key stderr line.
- **Linked deviation(s):** M-003
- **Priority:** P1

### Recommendation R-004: Add the lost-label, voided-approval and changed-Project-status re-read cases to the Step 6.7 test list (TF:475), each asserting revalidation

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** Add the lost-label, voided-approval and changed-Project-status re-read cases to the Step 6.7 test list (TF:475), each asserting revalidation_failed and no entry.
- **Verifier:** Re-read Step 6.7 (task file line 475): it lists lost-label, voided-approval and changed-Project-status re-read cases.
- **Linked deviation(s):** M-004
- **Priority:** P1

### Recommendation R-005: Restore the conjunct at TF:336, or state there that the attempts < 3 check of T-2 is applied in run_cycle and name the test that covers atte

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** Restore the conjunct at TF:336, or state there that the attempts < 3 check of T-2 is applied in run_cycle and name the test that covers attempts == 3.
- **Verifier:** Re-read Step 4.1c (task file line 336): the `attempts` < 3 conjunct or the pointer to the covering test is present.
- **Linked deviation(s):** M-005
- **Priority:** P2

### Recommendation R-006: Give the Step 10.6 prompt (TF:860) explicit substitution text for the withdrawn-commit branch of TF:848 (the working-tree diff against HEAD)

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** Give the Step 10.6 prompt (TF:860) explicit substitution text for the withdrawn-commit branch of TF:848 (the working-tree diff against HEAD), and state that an empty HEAD..HEAD audit is forbidden and does not satisfy Done.
- **Verifier:** Re-read Step 10.6 (task file line 860): the withdrawn-commit substitution text exists and says an empty HEAD..HEAD audit does not satisfy Done.
- **Linked deviation(s):** M-006
- **Priority:** P1

### Recommendation R-007: Correct the TF:611 rationale to say the same version range as .github/workflows/test.yml:29 is used, supplied with uv run --with instead of 

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** Correct the TF:611 rationale to say the same version range as .github/workflows/test.yml:29 is used, supplied with uv run --with instead of being installed into the environment.
- **Verifier:** Re-read task file line 611: it says the same version range as `.github/workflows/test.yml:29`, supplied with `uv run --with`.
- **Linked deviation(s):** M-007
- **Priority:** P2

### Recommendation R-008: Change G-10 at TF:723 to compare against HEAD so staged changes are seen: git diff --exit-code HEAD -- pyproject.toml Makefile .github/

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** Change G-10 at TF:723 to compare against HEAD so staged changes are seen: git diff --exit-code HEAD -- pyproject.toml Makefile .github/.
- **Verifier:** Re-read task file line 723: the G-10 command compares against HEAD.
- **Linked deviation(s):** M-008
- **Priority:** P2

### Recommendation R-009: Cap the TF:690 loop the way TF:778 does: if the failure cannot be made to pass (or meet the PASS-baseline verdict of M-002), HALT and record

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** Cap the TF:690 loop the way TF:778 does: if the failure cannot be made to pass (or meet the PASS-baseline verdict of M-002), HALT and record it in the Task Log.
- **Verifier:** Re-read task file line 690: the loop ends in HALT after a stated attempt cap.
- **Linked deviation(s):** M-009
- **Priority:** P2

### Recommendation R-010: After each post-fix re-run, regenerate final-change-set.md (TF:742), final-gate-record.md (TF:735) and ac-trace.md (TF:729) before any M4 pr

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** After each post-fix re-run, regenerate final-change-set.md (TF:742), final-gate-record.md (TF:735) and ac-trace.md (TF:729) before any M4 prompt (TF:800) is spawned.
- **Verifier:** Re-read Steps 9.F13 and 9.F18: they regenerate the three record files before the M4 prompts.
- **Linked deviation(s):** M-010
- **Priority:** P1

### Recommendation R-011: Declare the record -> predicates function import as a departure in the TF Open Questions, and add it to the Final lens at TF:751 and to the 

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** Declare the record -> predicates function import as a departure in the TF Open Questions, and add it to the Final lens at TF:751 and to the M4 departure lists (preamble TF:797, prompts TF:806, TF:818 and TF:833).
- **Verifier:** `grep -n 'parse_utc' <task file>` shows the Open Question and the departure lists (lines 751, 797, 806, 818, 833).
- **Linked deviation(s):** M-011
- **Priority:** P2

### Recommendation R-012: Make TF:502 and TF:520 agree: a format hit in main.py outside the added lines is judged by the PASS-baseline verdict of M-002 and is recorde

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** Make TF:502 and TF:520 agree: a format hit in main.py outside the added lines is judged by the PASS-baseline verdict of M-002 and is recorded, not fixed.
- **Verifier:** Re-read task file lines 502 and 520: they give the same rule for main.py.
- **Linked deviation(s):** M-012
- **Priority:** P2

### Recommendation R-013: State at TF:875 that a staging failure is logged as a follow-up for the owner (a NEEDS OWNER DECISION line naming the unstaged paths)

- **File:** .dev/tasks/to-do/TASK-RF-issue-watcher-20261107-150955/TASK-RF-issue-watcher-20261107-150955.md
- **Change:** State at TF:875 that a staging failure is logged as a follow-up for the owner (a NEEDS OWNER DECISION line naming the unstaged paths).
- **Verifier:** Re-read task file line 875: it names the NEEDS OWNER DECISION line for a staging failure.
- **Linked deviation(s):** M-013
- **Priority:** P2

## Run notes

- Degraded components: `auggie` (tool not available in this session; native Grep and Read used), `graph:unverified` (codegraph readiness check not run; reviewers used Read, Grep and Glob only), `env-aliases` not degraded (three aliases set).
- `executor_class_resolved: false` (no executor exists in pre mode); calibrator class opus is also a reviewer class, so `calibrator_diversity: degraded`; `t2_vendor_diversity: single`.
- Reviewer 2 (haiku) returned markdown instead of the requested YAML; its card is kept verbatim.
- Tier 3: remediation was offered (`--remediate`) and not accepted: the task-builder rule for the PRE gate allows no automatic builder loop, and no user is present to answer the opt-in prompt. The findings go to the task file's Open Questions section instead.
- Memory: `last-pass` written under `.superclaude/memory/reflect/`; the tracked `docs/memory/reflect/deviation-patterns-*.md` file was not written, to keep the worktree free of unrelated changes (best-effort per the error matrix).
