# Reflect report: pre-execution check of the issue-346 ponytail plan

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.77
citations_total: 22
citations_revalidated: 22
citations_dropped: 0
citations_inferred: 3
citation_budget_policy: full_reread
coverage_degraded: parsed-sparse
```

Plan: `.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md` (12 tasks, 5 phases). Spec: `.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md`.
Why `partial`: the nested adversarial merge returned `partial` (its fault-finder raised two candidates no reviewer debated, P-01 and P-02 below). `confidence_calibrated` is the mean of the three calibrated reviewer cards (0.76, 0.75, 0.81).
Why Tier 2: the spec has no labelled requirement ids, so all 109 requirements were inferred (`coverage_degraded: parsed-sparse`, a table-wide bar on a Tier-1 stop); the plan touches three domains (code, tests, docs).

## Verdict

The plan covers the spec's sections 3 and 4 and the four owner decisions, but two blocking defects must be fixed in the plan before `/sc:implement` runs: two of Task 8's checks cannot both pass (F-01), and Task 2 drops the FR-8/FR-9 protection the spec requires (F-02). Seven minor findings follow. This check is advisory: the plan file was not edited.

## Coverage

- `coverage_pct`: null (no parsed ids). `coverage_pct_union`: 0.789 (86 of 109 inferred requirements match one task by word containment). `S_dev_density`: 0.211. Matrix: `artifacts/coverage-matrix.yaml`.
- Of the 23 unmatched rows, 11 are in sections the plan excludes on purpose (2.8 placements, 5 measurement); most of the rest are delivered by a task with lower word overlap. In-scope rows no task delivers: INF-057 (plugin-mirror question) and INF-087 ("Adopt nowhere until S1 shows an effect"); both are settled by the plan's Constraints, not by a task.

## Inferred requirements (Pass 2)

109 rows, all quote-checked against their cited `source.md` lines by the mapper; the full table (id, quote, citation, match result) is in `artifacts/coverage-matrix.yaml`. No row was dropped.

## Deviations (UC-1: plan against spec)

### Deviation D-1: Variant omits the `## Unattended mode` section
- **Location:** plan Task 7 (TASK-WF-spec-20261108-181547.md:134)
- **Spec section:** 3.1 row 1 ("Byte copy ... with only these differences", source.md:180)
- **Evidence:** the section exists at src/superclaude/commands/spec-panel.md:451; tests/skills/test_worker_contract.py:830-839 requires the set of commands with that section to equal its fixed list.
- **Classification:** authorized (owner ruling msg_7b27feaade5e, recorded in the plan Constraints)
- **Default remediation:** none; see F-03 for the leftover Usage-line flags.

### Deviation D-2: Plan edits a test the spec does not list
- **Location:** plan Task 7, `tests/recommend/test_routing_refresh.py` line 33
- **Evidence:** tests/recommend/test_routing_refresh.py:647-648 asserts `shipped - _POST_REFRESH_ADDITIONS == active`, which a new command file breaks.
- **Classification:** necessary
- **Default remediation:** none.

### Deviation D-3: Owner count keeps deferred and demoted findings open
- **Location:** plan Task 5 (TASK-WF-spec-20261108-181547.md:104)
- **Spec section:** 2.6 ("recorded as minor and closed, not open")
- **Classification:** authorized (owner decision in the coordinator brief)

### Deviation D-4: Six S1 briefs copied, T10 included
- **Location:** plan Task 12
- **Spec section:** 4 names T05-T09 (source.md:254)
- **Classification:** authorized (owner ruling msg_2000b167e322). Recorded as N-01: the plan should name the ruling.

## Findings (merged by the adversarial pass)

Blocking:

- **F-01. Two Task 8 checks cannot both pass.** Task 8 requires the variant to equal `spec-panel.md` line for line except the listed differences, and forbids any `src/superclaude` string in it (TASK-WF-spec-20261108-181547.md:147). `src/superclaude/commands/spec-panel.md:220` already contains `src/superclaude/examples/release-spec-template.md`, and Task 7's differences (TASK-WF-spec-20261108-181547.md:134) do not touch that line. The conflict comes from the spec itself (source.md:239). Cards 1. Owner choice needed.
- **F-02. FR-8/FR-9 protection is not recorded.** The spec protects CRITICAL, FR-8 and FR-9 ids regardless of the blocking grade (source.md:218) and requires a test that "`MAJOR (FR-8 GAP)` graded minor counts as protected" (source.md:231). Task 2 records only "the severity label (CRITICAL, MAJOR, MINOR or unknown) and the blocking flag per id" (TASK-WF-spec-20261108-181547.md:55), so `check` cannot refuse reverting such a finding. Cards 1, 3.

Minor:

- **F-03.** The variant's Usage line keeps `[--unattended] [--report-dir <dir>] [--improve]` (src/superclaude/commands/spec-panel.md:23), which only the removed section defines; Task 8 checks only the heading. The copied Fix Audit sentence "behaves exactly as `/sc:spec-panel`" (source.md:194) is then no longer true. Cards 1, 3.
- **F-04.** The spec gives exit code 2 for "verdict unparseable or inconsistent" (source.md:183); Task 5 gives exit 2 only for "an unparseable table" (TASK-WF-spec-20261108-181547.md:101). The FAIL line is still forced. Cards 1, 2, 3.
- **F-05.** Task 5 counts "every id logged `DOWNGRADE` in `D/check.log`" (TASK-WF-spec-20261108-181547.md:104), and Task 3 writes those lines even on CHECK_FAIL; this contradicts Task 5's check "with the audit skipped both numbers are equal" (TASK-WF-spec-20261108-181547.md:115). Cards 1, 3.
- **F-06.** Task 4 replaces the spec, then reads it back and writes logs (TASK-WF-spec-20261108-181547.md:87), but says nothing about restoring the spec if a step after the replace fails. The spec's own section 3.3 shares the gap. Card 2.
- **F-07.** The spec says to stage `src/`, `tests/`, `docs/` and `.dev/tasks` (source.md:174); Task 8 stages only `src/` and `tests/` paths (TASK-WF-spec-20261108-181547.md:149) and no task stages `docs/` or `.dev/tasks`. Cards 1, 3.
- **F-08.** The no-`src/superclaude` check leaves out `scripts/fix_audit.py`, which is also installed. Card 1.
- **F-09.** Task 2's brief-comparison test reads `source.md` inside the plan package, which moves to `.dev/tasks/done/` on completion. Card 1.

## Undebated fault-finder candidates (not findings)

- [INFERRED] P-01: on the not-triggered and skipped paths `state.json` may hold no review-2 grades, which `verdict` needs to filter prior findings by grade. Check before Task 5 runs.
- [INFERRED] P-02: in `any-severity` mode the computed 427 verdict can be PASS while T09's own line is FAIL; the spec says the report line is printed beside, not cross-checked, while also saying the script never turns a FAIL into a PASS. Owner reading needed.
- [INFERRED] P-03/P-04: APPLY_STOP records no audit state; no test expects a final `verdict: PASS`.

## Inferred-claim audit

- `citations_inferred: 3`
- Inferred-fraction: 3 / 22 = 0.14
- Evidence validator: 22 of 22 citations re-read, 0 dropped (all 22 re-read, so the policy is full re-read).

## Recommendations

### Recommendation R-001: Settle the Task 8 drift and no-src checks
- **File:** .dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md (Tasks 7 and 8)
- **Change:** either scope the no-src check to the new text (Fix Audit section, SKILL.md, the brief, fix_audit.py) and require the variant's count of `src/superclaude` to equal the original's, or list line 220 as one more difference (owner choice).
- **Verifier:** `uv run pytest tests/skills/test_spec_panel_ponytail.py -q` passes with both checks active.
- **Linked:** F-01, F-08. **Priority:** P0

### Recommendation R-002: Record and test FR-8/FR-9 protection
- **File:** same plan, Tasks 2 and 3
- **Change:** record a per-id `protected` flag (CRITICAL, FR-8 or FR-9) in `D/state.json` and use it in the class rule and K6; add the `MAJOR (FR-8 GAP)` graded-minor test and a `CHECK_FAIL K6` case for reverting it.
- **Verifier:** `uv run pytest tests/skills/test_fix_audit_script.py -q` includes and passes both tests.
- **Linked:** F-02. **Priority:** P0

### Recommendation R-003: Close the minor gaps in Tasks 4, 5, 7, 8 and 9
- **File:** same plan
- **Change:** Task 7 drops `[--unattended] [--report-dir <dir>]` from the variant Usage line (and decides `[--improve]`); Task 5 states exit 2 on DISAGREE and reads DOWNGRADE lines only when the audit applied; Task 4 restores `D/current-before-audit.md` on any failure after the replace; Task 8 adds `fix_audit.py` to the no-src check; Task 9 and a closing step stage `docs/designs/spec-panel-ponytail.md` and `.dev/tasks`; Task 2 locates `source.md` with a `.dev/tasks/*/` glob or embeds the brief.
- **Verifier:** each change appears in the named task's acceptance criteria.
- **Linked:** F-03 to F-09. **Priority:** P1
