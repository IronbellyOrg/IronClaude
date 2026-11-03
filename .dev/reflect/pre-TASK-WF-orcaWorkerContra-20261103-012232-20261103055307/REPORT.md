# Reflection report: pre-execution review of the P0 static plan

```yaml
contract_version: 1.8.0
status: partial
mode: pre
tier_reached: 2
confidence_calibrated: 0.85
citations_total: 182
citations_revalidated: 82
citations_dropped: 1
citations_inferred: 0
citation_budget_policy: sampled
coverage_degraded: parsed-sparse
```

> **Citation budget: sampled mode**
> - `citations_revalidated: 82`: the size of the re-Read sample (82 of 182). It holds all 15 citations on blocking findings, plus 30% of the rest and a 10% spot-check (`artifacts/citation-sample.yaml`).
> - `citations_dropped: 1`: the number of drops in the sample (`artifacts/evidence-validation.yaml`).
> - `citations_dropped_extrapolated: 2`: `round(1 x 182/82)`. This is recorded only and does not gate promotion.
>
> The extrapolated value is telemetry, not a verdict. The sample-count is what the validator actually examined; the extrapolation is what it would have found if the budget had permitted a full re-Read.

## Summary

**Verdict: FAIL.** Do not run this plan as written. It has two blocking defects; both are wording fixes to the plan.

- **Blocking D-001 (Constraints and Task 4):** TL:21 says "P0 edits no command, skill or agent file", but Task 4 must overwrite `plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md`, a file inside a skill package. No repair can satisfy both, and either the Task 4 review or the final archive review can halt on it. The spec only says "no command edits" (source.md:220). The debate was unanimous after Round 1.
- **Blocking D-016 (Task 1, raised by the invariant probe, not debated):** Task 1's wider baseline suite already has 8 failing tests today. Task 1 saves that raw log as evidence. The final archive review returns `issues` when a cited log shows a failure, which ends in `E-ARCHIVE-BLOCKED`. Fix: name the 8 known failures as the accepted baseline, and cite the per-test comparison instead of the raw log.
- **Should-fix (10):**
  - The contract file needs an installed-paths-only rule (D-002).
  - Task 6's "phase that converts its command" cannot be stated for every hit (D-003). The vote was 2-1 for should-fix over blocking.
  - TL:22 must also allow the section 3.1 flags (D-004).
  - "at most 10" is not the spec's wording (D-005).
  - Task 8 lacks evidence files (D-006).
  - The plugin core copy has no sync check (D-007).
  - The routing-guide tests require ASCII and fixed heading slices (D-008).
  - The wider test run rewrites a tracked `perf.json` (D-017).
  - The `gh api` "post" definition catches GET reads (D-018).
  - The quoted-phrase rule collides with the no-copy rule (D-019).
- **Minor (7):** D-009 to D-015. Among them is a stale "AC-0.8" mention; that check is AC-1.8 in P1.
- **Run conditions:** the plan fixes must be made by hand, or through a fresh `/sc:workflow` package, before the first `/sc:implement` start, because the executor pins the plan hash. Run with no other writer in this worktree.
- **Method:** a Tier 2 review by three reviewers on three model classes (sonnet, glm, opus), blind-calibrated by fable at 0.86, 0.82 and 0.88. The merge was an adversarial debate: 2 rounds plus an invariant probe. Convergence was 1.00 but blocked by INV-001. 82 of 182 citations were re-Read and 1 was dropped.
- **Coverage:** 29 of 105 inferred spec requirements match a plan task by word containment (0.28). Most unmatched rows are deferred by the spec's two-part rule (source.md:238) or are cited by identifier.

## Deviations

### Deviation D-001: Constraint TL:21 forbids skill-file edits; Task 4 must overwrite a file inside the sc-recommend skill package (blocking; merged id M-01)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:21
- **Mapped tasklist item:** Task 4
- **Spec section:** source.md:220
- **Evidence:** cited lines TL:21, TL:24, TL:90, TL:93, SRC:220, qa.md:52, qa.md:61, qa.md:310, qa.md:286. Re-Read 9 of its citations, 0 dropped. Example: "P0 edits no command, skill or agent file (`./source.md` section 6, P0 row: 'no command edits')." (TL:21, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity settled by the adversarial debate. Can halt: Task 4 QA (B4) or managed FINAL (violated Constraint); no repair satisfies both TL:21 and TL:93. Reviewers: [{'reviewer': 3, 'variant': 'C', 'calibrated_confidence': 0.88}].
- **Default remediation:** Reword TL:21: P0 edits no command file, no SKILL.md and no agent file; the only file written under a skills directory is the byte-for-byte copy of HOW-WE-WORK.md in plugins/superclaude/skills/sc-recommend/refs/ that Task 4 makes.

### Deviation D-002: Installed-path rule missing from Constraints; a literal restatement ships src/superclaude paths and evidence ids into an installed core file (should-fix; merged id M-02)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:17-27
- **Mapped tasklist item:** Task 1, Task 2
- **Spec section:** source.md:59
- **Evidence:** cited lines TL:17-27, TL:22, TL:37, SRC:59. Re-Read 2 of its citations, 0 dropped. Example: "## Constraints (lines 17-27): none is an installed-path rule; line 22 restates spec text into the contract file" (TL:17-27, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity settled by the adversarial debate. Reviewers: [{'reviewer': 1, 'variant': 'A', 'calibrated_confidence': 0.86}].
- **Default remediation:** Add a Constraints line: WORKER-CONTRACT.md and the HOW-WE-WORK.md section use installed ~/.claude/ paths only and copy no CAPS:/INV- ids or src/superclaude/ paths.

### Deviation D-003: Task 6 requires a converting phase for every allowlisted hit; many hits have none, some are read-only or false matches, and keys are unspecified (should-fix; merged id M-03)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:125
- **Mapped tasklist item:** Task 6
- **Spec section:** source.md:61, source.md:201, source.md:224, source.md:305
- **Evidence:** cited lines TL:125, SRC:61, SRC:201, SRC:224, SRC:305. Re-Read 1 of its citations, 0 dropped. Example: "**`/sc:pr-submit` (D3).** It is never an Orca worker ... gets no `--unattended` mode and no Phase 4 changes." (SRC:201, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity settled by the adversarial debate. Can halt: Task 6 review only. Reviewers: [{'reviewer': 1, 'variant': 'A', 'calibrated_confidence': 0.86}, {'reviewer': 3, 'variant': 'C', 'calibrated_confidence': 0.88}].
- **Default remediation:** Replace TL:125's two-way rule with five categories (WC-9 allowed; refused or deferred in a named phase; never a worker; no command converts this file; read-only or false match), key by path, verb and stripped line text, scan with word boundaries; ship with M-18.

### Deviation D-004: Constraint TL:22 limits the contract to sections 2.1-2.3 while Task 2 adds section 3.1 flags and a section 6 marker (should-fix; merged id M-04)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:22
- **Mapped tasklist item:** Task 2
- **Spec section:** source.md:59, source.md:84, source.md:220
- **Evidence:** cited lines TL:22, TL:58, SRC:59, SRC:84, SRC:220. Re-Read 3 of its citations, 0 dropped. Example: "`WORKER-CONTRACT.md` restates only what `./source.md` sections 2.1, 2.2 and 2.3 say and adds no rule the spec lacks." (TL:22, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity settled by the adversarial debate. Can halt: Task 2 QA or managed FINAL, for the 'from P1' marker only. Reviewers: [{'reviewer': 3, 'variant': 'C', 'calibrated_confidence': 0.88}].
- **Default remediation:** Add to TL:22: plus, in the brief template only, the section 3.1 Brief-must-pass flags and the section 6 phase markers (--report-dir from P1).

### Deviation D-005: Task 5 must pin 'at most 10' 'as written in section 2.3', but the spec says 'maximum of 10 inputs'; Tasks 1-2 need not supply quotable phrases (should-fix; merged id M-05)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:56
- **Mapped tasklist item:** Task 1, Task 2, Task 5
- **Spec section:** source.md:122
- **Evidence:** cited lines TL:56, TL:104, TL:112, SRC:122. Re-Read 1 of its citations, 0 dropped. Example: "- the fan-in caps 'at most 10' (as written in section 2.3) and 'at least 2';" (TL:112, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity settled by the adversarial debate. Reviewers: [{'reviewer': 1, 'variant': 'A', 'calibrated_confidence': 0.86}, {'reviewer': 3, 'variant': 'C', 'calibrated_confidence': 0.88}].
- **Default remediation:** Use the spec's 'maximum of 10 inputs' / 'never exceeds 10' in TL:56 and TL:112 and drop '(as written in section 2.3)'; Tasks 1-2 record the phrase each rule is tested on, worded per M-19.

### Deviation D-006: Task 8 needs an evidence file for each of 11 checks; no task saves files for AC-0.1, AC-0.2, AC-0.3 (should-fix; merged id M-06)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:47
- **Mapped tasklist item:** Task 1, Task 3, Task 4, Task 8
- **Spec section:** n/a
- **Evidence:** cited lines TL:47, TL:72, TL:93-94, TL:147-152, TL:157, qa.md:85. Re-Read 3 of its citations, 0 dropped. Example: "- The AC-0.1 install check in `./source.md` section 7.3 ... exits 0: `uv run python -c 'import pathlib, tempfile; ..." (TL:72, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity settled by the adversarial debate. Reviewers: [{'reviewer': 1, 'variant': 'A', 'calibrated_confidence': 0.86}].
- **Default remediation:** In Task 8, re-run AC-0.1, AC-0.2, AC-0.3, AC-C1 and AC-C2 and save each output to ./artifacts/<id>.txt as the report's evidence.

### Deviation D-007: An added plugin core copy of WORKER-CONTRACT.md has no sync check (should-fix; merged id M-07)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:69
- **Mapped tasklist item:** Task 3, Task 5
- **Spec section:** n/a
- **Evidence:** cited lines TL:69, TL:74. One citation of this finding (qa.md:310) fell in the re-Read sample. It was dropped as unrelated (see Grounding Gaps G-036). TL:69 and TL:74 were not in the sample and are not revalidated.
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity settled by the adversarial debate. Reviewers: [{'reviewer': 3, 'variant': 'C', 'calibrated_confidence': 0.88}].
- **Default remediation:** If Task 3 adds the copy, Task 5 asserts it is byte-identical to the src file (pattern: test_plugin_mirror_matches_src).

### Deviation D-008: Routing-guide tests (ASCII only; fixed heading slices) constrain the new Orca section (should-fix; merged id M-08)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:90
- **Mapped tasklist item:** Task 4
- **Spec section:** n/a
- **Evidence:** cited lines TL:90, TL:93, tests/core/test_how_we_work_routing_table.py:341, tests/core/test_how_we_work_routing_table.py:819, tests/core/test_how_we_work_routing_table.py:1091. Re-Read 2 of its citations, 0 dropped. Example: "def test_guide_is_ascii_except_the_ruling_example():" (tests/core/test_how_we_work_routing_table.py:341, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity settled by the adversarial debate. Reviewers: [{'reviewer': 3, 'variant': 'C', 'calibrated_confidence': 0.88}].
- **Default remediation:** Add to Task 4: the new section is ASCII only and is a new top-level section after the last one, outside the level-table and routing markers.

### Deviation D-009: Task 3 does not name the evidence that decides the plugin copy (minor; merged id M-09)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:69
- **Mapped tasklist item:** Task 3
- **Spec section:** source.md:252
- **Evidence:** cited lines TL:69, SRC:252, scripts/build_superclaude_plugin.py:75, tests/commands/test_routing_plugin_parity.py:3, tests/commands/test_impact_command.py:309. Re-Read 2 of its citations, 0 dropped. Example: "  | grep -v '^plugins/superclaude/core/WORKER-CONTRACT\.md:' \" (SRC:252, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity settled by the adversarial debate. Reviewers: [{'reviewer': 1, 'variant': 'A', 'calibrated_confidence': 0.86}, {'reviewer': 2, 'variant': 'B', 'calibrated_confidence': 0.82}].
- **Default remediation:** Name build-script line 75, the parity test, the one test that reads a plugin core copy, and SRC:252's by-name exclusion in Task 3.

### Deviation D-010: Constraints cite AC-0.8, which does not exist (minor; merged id M-10)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:19
- **Mapped tasklist item:** Task 0
- **Spec section:** source.md:304-306
- **Evidence:** cited lines TL:19, SRC:304-306. None of this finding's citations fell in the re-Read sample; they are counted as not revalidated.
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity settled by the adversarial debate. Reviewers: [{'reviewer': 2, 'variant': 'B', 'calibrated_confidence': 0.82}].
- **Default remediation:** Delete the AC-0.8 sentence or replace it with 'the P1 checks are AC-1.1 to AC-1.8 (section 7.3)'.

### Deviation D-011: No handoff of static results into the live plan's phase report; re-staging omitted from next steps (minor; merged id M-11)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:19
- **Mapped tasklist item:** Task 8
- **Spec section:** source.md:238, source.md:303-304
- **Evidence:** cited lines TL:19, TL:154, SRC:238, SRC:303-304. Re-Read 2 of its citations, 0 dropped. Example: "...The live checks (AC-0.4, AC-0.5, AC-0.6) and the P0 phase report belong to the P0 live plan, which is written after this plan's checks pass." (TL:19, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity settled by the adversarial debate. Reviewers: [{'reviewer': 2, 'variant': 'B', 'calibrated_confidence': 0.82}, {'reviewer': 3, 'variant': 'C', 'calibrated_confidence': 0.88}].
- **Default remediation:** End the static report with a 'results the P0 live plan must cite' list and add the coordinator's re-staging of .dev/tasks and AC-C4 re-run to the next steps.

### Deviation D-012: Hard-coded negative check for Unattended mode sections (minor; merged id M-12)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:115
- **Mapped tasklist item:** Task 5
- **Spec section:** source.md:306
- **Evidence:** cited lines TL:115, SRC:306. Re-Read 1 of its citations, 0 dropped. Example: "It also asserts that no file in `src/superclaude/commands/` has an `## Unattended mode` section, because no command accepts `--unattended` after P0" (TL:115, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity settled by the adversarial debate. Reviewers: [{'reviewer': 3, 'variant': 'C', 'calibrated_confidence': 0.88}].
- **Default remediation:** Write it as a cumulative per-phase map, {'P0': set()}; optionally also assert at least 45 command files were scanned (INV-011).

### Deviation D-013: Brief-template flags are not checked against the command files (minor; merged id M-13)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:58
- **Mapped tasklist item:** Task 2, Task 5
- **Spec section:** n/a
- **Evidence:** cited lines TL:58. None of this finding's citations fell in the re-Read sample; they are counted as not revalidated.
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity settled by the adversarial debate. Reviewers: [{'reviewer': 3, 'variant': 'C', 'calibrated_confidence': 0.88}].
- **Default remediation:** In Task 5, assert each template flag exists in its command file, except the flags marked 'from P1'.

### Deviation D-014: Goal says every copy gets the Orca section; Task 4 leaves the CLAUDE.md copy unchanged (minor; merged id M-14)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:15
- **Mapped tasklist item:** Task 4
- **Spec section:** n/a
- **Evidence:** cited lines TL:15, TL:90. Re-Read 1 of its citations, 0 dropped. Example: "Goal: ... The routing guide has an Orca section in every copy the repo keeps." (TL:15, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity settled by the adversarial debate. Reviewers: [{'reviewer': 3, 'variant': 'C', 'calibrated_confidence': 0.88}].
- **Default remediation:** Reword the Goal: the Orca section is in HOW-WE-WORK.md and its plugin copy; the CLAUDE.md level-table copy is unchanged.

### Deviation D-015: No make verify-sync baseline; tests/docs and tests/unit not in the wider baseline (minor; merged id M-15)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:33-35
- **Mapped tasklist item:** Task 1, Task 4
- **Spec section:** n/a
- **Evidence:** cited lines TL:33-35, TL:96. Re-Read 1 of its citations, 0 dropped. Example: "- The AC-C1 scan in `./source.md` section 7.1 prints nothing, and `make verify-sync` exits 0 (AC-C2)." (TL:96, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity settled by the adversarial debate. Reviewers: [{'reviewer': 3, 'variant': 'C', 'calibrated_confidence': 0.88}].
- **Default remediation:** In Task 1 also save make verify-sync output, and add tests/docs and tests/unit to the wider baseline and Task 4's comparison.

### Deviation D-016: Task 1's wider baseline already has 8 failures; the managed FINAL can read the cited log as a failure and block archiving (blocking; merged id M-16)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:35
- **Mapped tasklist item:** Task 1, Task 4
- **Spec section:** n/a
- **Evidence:** cited lines TL:35, TL:48, TL:95, qa.md:310, qa.md:294, qa.md:286. Re-Read 6 of its citations, 0 dropped. Example: "- the wider baseline that Task 4 compares against: run `uv run pytest tests/core tests/commands tests/recommend tests/cli -q -rf` and save its full output to `./artifacts/t1-baseline-wider.txt`." (TL:35, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity raised by the Round 2.5 invariant probe; NOT adjudicated by the advocates. Can halt: managed FINAL (E-ARCHIVE-BLOCKED), depending on whether the FINAL follows qa.md:310 or qa.md:294. Reviewers: none (probe only).
- **Default remediation:** In TL:35 and TL:95 state that pre-existing failures are expected, list the 8 failing test ids as the accepted baseline, and cite the per-test comparison file rather than the raw log.

### Deviation D-017: The wider test run rewrites a tracked perf.json, which enters Task 1 and Task 4 diffs (should-fix; merged id M-17)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:35
- **Mapped tasklist item:** Task 1, Task 4, Task 8
- **Spec section:** n/a
- **Evidence:** cited lines TL:35, TL:95, TL:154, qa.md:51. Re-Read 2 of its citations, 0 dropped. Example: "- the wider baseline that Task 4 compares against: run `uv run pytest tests/core tests/commands tests/recommend tests/cli -q -rf` ..." (TL:35, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity raised by the Round 2.5 invariant probe; NOT adjudicated by the advocates. Reviewers: none (probe only).
- **Default remediation:** Add --deselect tests/cli/eval/test_perf_home_setup.py to the wider runs, or git restore .dev/releases/current/cliEval/evidence/T02.15/perf.json after each run.

### Deviation D-018: TL:125 counts -f/-F as a gh api post, so GET reads that pass -F are posts under the plan (should-fix; merged id M-18)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:125
- **Mapped tasklist item:** Task 6
- **Spec section:** source.md:305
- **Evidence:** cited lines TL:125, SRC:305, qa.md:50, qa.md:52. Re-Read 1 of its citations, 0 dropped. Example: "`false-claim` | B2 wrong statement | ... a recipe or instruction followed as written does not do what the text says it does ..." (qa.md:50, re-Read 2026-11-03).
- **Classification:** drift
- **Classification rationale:** drift: the plan departs from, narrows or misstates the spec without an authorizing line. Severity raised by the Round 2.5 invariant probe; NOT adjudicated by the advocates. Reviewers: none (probe only).
- **Default remediation:** Define a gh api post as a gh api call whose method is not GET; ship with M-03.

### Deviation D-019: Task 5's quoted-phrase rule can collide with TL:22's no-copy rule for WC-12, WC-13 and heartbeats (should-fix; merged id M-19)

- **Location:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md:22
- **Mapped tasklist item:** Task 1, Task 2, Task 5
- **Spec section:** source.md:59
- **Evidence:** cited lines TL:22, TL:46, TL:104-105, SRC:59. Re-Read 2 of its citations, 0 dropped. Example: "- The worker-session part contains no `orca orchestration` verb syntax copied from Orca's guides and no fixed heartbeat cadence; it points to the dispatch preamble for both." (TL:46, re-Read 2026-11-03).
- **Classification:** none
- **Classification rationale:** none: not a departure from the spec; a plan-quality or executor-compatibility defect (no taxonomy class applies). Severity raised by the Round 2.5 invariant probe; NOT adjudicated by the advocates. Reviewers: none (probe only).
- **Default remediation:** Say 'a phrase', exempt the worker-session duties from verbatim copying, and name the phrase to pin for WC-12, WC-13 and heartbeats.

## Grounding Gaps

Per section 11.2, a citation the evidence validator dropped is listed here together with its claim. UC-1 writes no `grounding-gaps.yaml`, so this section adds no human-decision flag.

### Gap G-036

- **Hunk ref:** qa.md:310 (cited by D-007, merged id M-07)
- **Evidence missing:** the citation offered for "An added plugin core copy of WORKER-CONTRACT.md has no sync check". Validator: The line is about the FINAL reviewer's inputs and verdicts and says nothing about plugin core copies or a sync check.
- **Why not classifiable:** the claim's class does not change (the finding keeps its other citations); only this support is removed.
- **Next evidence needed:** cite the Makefile verify-sync scope lines (H6 in `artifacts/grounding-hunks.md`), which show that verify-sync checks no core copy.

## Unaddressed invariants from the adversarial merge

The merge's invariant probe (adversarial/adversarial/invariant-probe.md) left these open. INV-001, INV-002, INV-010 and INV-014 are carried as deviations D-016 to D-019 above. INV-001 is HIGH, so the merge is not counted as converged (`convergence_status: BLOCKED_BY_INVARIANTS`).

| ID | Severity | Category | Open assumption |
|---|---|---|---|
| INV-001 | HIGH | sufficiency_challenge | Fixing R3-F1 and the should-fixes is enough for per-task QA and the managed FINAL to pass |
| INV-002 | MEDIUM | state_variables | Running the plan's test commands changes no tracked file |
| INV-005 | MEDIUM | state_variables | Someone applies the agreed plan fix before execution |
| INV-007 | MEDIUM | state_variables | Only the executor writes in this worktree during the run |
| INV-010 | MEDIUM | interaction_effects | The merged Task 6 category 'read-only or a false match' fits the plan's definition of a gh api post |
| INV-011 | LOW | collection_boundaries | The P0 'no Unattended mode section' assertion checks something real |
| INV-014 | MEDIUM | interaction_effects | Task 5's quoted-phrase rule is compatible with TL:22 for the worker-session duties |
| INV-015 | LOW | interaction_effects | The installed-path Constraint and the quoted-phrase rule can both be met |
| INV-016 | LOW | interaction_effects | Task 5 can safely add missing spec phrases to WORKER-CONTRACT.md |
| INV-017 | LOW | interaction_effects | Rewording TL:21 to 'P0 edits no command file' creates no new literal breach |

Run conditions (not plan defects):
- INV-005: Apply the plan fixes by hand, or through a fresh /sc:workflow package, before the first T<id>: start line; any later plan change stops the run with E-PLAN-CHANGED.
- INV-007: Run /sc:implement with no other writer in this worktree, or in its own worktree; a sibling commit halts the run on head-moved.

## Inferred requirements (Pass 2)

Pass 2 gives 105 quote-pinned requirement rows; Pass 1 found no labelled requirement IDs. 29 rows match a plan task by word containment. Most of the unmatched rows are deferred, either to the P0 live plan (the spec's two-part rule, source.md:238) or to the P1-P4 plans. The rest are cited by identifier ("WC-2", "Section 2.3 in full"), which word containment cannot match.

| INF id | Verbatim quote | Citation (file:line) | Match result |
|---|---|---|---|
| INF-001 | **Worker run**: a session that received an Orca preamble carrying a Task ID and a Dispatch ID. Only such a session may send lifecycle messages; a session the user started, inside or outside Orca, is an ordinary session | `source.md:54` | unmatched (best T1 0.3889) |
| INF-002 | The mode is selected only by the flag (decision D1, section 9: option (c) as amended). No command detects Orca, its preamble or its environment. | `source.md:55` | matched T1 (0.7222) |
| INF-003 | **Flag parse rule**: `--unattended` counts only as a standalone argument token outside any quoted argument. | `source.md:56` | unmatched (best T1 0.5455) |
| INF-004 | **Person-mode flags are refused**: under `--unattended`, every command refuses the flags that exist to involve a person: `--interactive`, `--format interactive` (explain), `--mode socratic` (business-panel), `--watch` (test), `--monitor 1` (pr-submit). | `source.md:57` | unmatched (best T1 0.381) |
| INF-005 | **Report directory**: the directory that holds the worker contract (WC-4). Under `--unattended` the brief passes exactly one: either the command's own existing directory-valued output flag (`--output <dir>` or `--output-dir <dir>`), or the new flag `--report-dir <dir>` (for a command without such a flag, or a brief that does not pass it). | `source.md:58` | matched T1 (0.6923) |
| INF-006 | **Contract file**: one shared document, proposed as `src/superclaude/core/WORKER-CONTRACT.md`, installed to `~/.claude/WORKER-CONTRACT.md`. | `source.md:59` | unmatched (best T1 0.5833) |
| INF-007 | For the worker-session duties (WC-3, WC-5, WC-7, WC-12, WC-13 and heartbeats) it states only the IronClaude-specific rule (outcome mapping from `worker_status`, including WC-5's P0 brief override, top-level only, ask only when the brief allows it) and points to the dispatch preamble as the authority for Orca verb syntax and heartbeat cadence; it never copies them | `source.md:59` | matched T1 (0.8056) |
| INF-008 | Each changed command adds a short `## Unattended mode` section that lists only its own gate resolutions and report file and points to the installed contract path, so the shared rules are written once. | `source.md:59` | matched T1 (0.625); deferred to later phase plan |
| INF-009 | **Brief guard** (worker session, from P1): it applies only in a session whose current prompt carries a live Orca preamble with Task and Dispatch IDs (see "Worker run"). Before invoking anything, the worker checks every `Command:` line of its brief (section 2.3, "Brief layout"), and only those lines. | `source.md:60` | unmatched (best T2 0.5312) |
| INF-010 | **Never-as-worker list**: `/sc:agent`, `/sc:git`, `/sc:help`, `/sc:pm`, `/sc:spawn` and `/sc:swarm-wizard` (section 4), plus `/sc:pr-submit` while the answer to D3 keeps it off workers. | `source.md:61` | matched T1 (0.7222) |
| INF-011 | **Nested propagation rule**: under `--unattended`, a command that invokes another `/sc:` command or protocol skill, through the Skill tool or the Agent tool, passes `--unattended` when the invoked command accepts it at this phase, together with its own report directory `<caller report-dir>/nested/<command>-<n>/` (WC-4, WC-11). | `source.md:62` | matched T1 (0.6786) |
| INF-012 | WC-1 \| **No prompt before the agent is ready.** Nothing in the launch path (wrapper, hook, startup command) may wait on a person before Claude's input box is ready. | `source.md:69` | unmatched (best T7 0.3529); deferred to P0 live plan |
| INF-013 | WC-2 \| **No person-blocking step in unattended mode.** Under `--unattended` the command never calls `AskUserQuestion`, never ends its turn on a chat question or `[yes / no]` offer, and never says STOP AND WAIT. | `source.md:70` | unmatched (best T1 0.3) |
| INF-014 | WC-3 \| **Questions go to the coordinator, not to a local prompt.** The brief fixes the policy for a blocked gate; under `ask the coordinator` the worker applies the eligibility test below and makes no other choice. | `source.md:71` | unmatched (best T4 0.2857) |
| INF-015 | WC-4 \| **One report file, known before dispatch, written on every outcome.** In unattended mode the command writes `<report-dir>/return-contract.yaml`, where `<report-dir>` is the one report directory the brief passes (section 2.1): either the command's own directory-valued `--output` / `--output-dir`, or `--report-dir`. | `source.md:72` | matched T1 (0.7308) |
| INF-016 | WC-5 \| **Outcome mapping.** The worker sends `worker_done` exactly once from its own top-level session. | `source.md:73` | unmatched (best T1 0.5833) |
| INF-017 | WC-6 \| **Every retry is a new Task.** A Task's brief cannot change after creation (`task-update` changes only `--status` and `--result`, `task-update --help` line 3), and a re-run into the first attempt's directories could mix its files with the retry's. | `source.md:74` | unmatched (best T2 0.4231) |
| INF-018 | WC-7 \| **Run at the top level, never inside a subagent.** The worker runs the command directly in its own session; it never wraps the command in an Agent-tool subagent. | `source.md:75` | unmatched (best T1 0.4375) |
| INF-019 | WC-8 \| **No Orca fan-out from inside a command.** A command never calls `worker-start`, `dispatch` or `task-create`. | `source.md:76` | matched T7 (0.6) |
| INF-020 | WC-9 \| **No outward action from a worker; local commits only by grant.** Under `--unattended` every outward default (push, merge into a shared branch, PR, GitHub post, install on a shared or real target, VM, paid external run) is off, and no brief can turn it on (D4); the coordinator performs those actions (section 2.3). | `source.md:77` | unmatched (best T2 0.3889) |
| INF-021 | WC-10 \| **Liveness during long waits.** The worker sends heartbeats at the cadence its preamble sets (5 minutes in current preambles). | `source.md:78` | unmatched (best T1 0.4) |
| INF-022 | WC-11 \| **Parallel-safe writes.** Two workers in one worktree must never write the same file. | `source.md:79` | unmatched (best T1 0.5455) |
| INF-023 | WC-12 \| **Coordinator follow-ups are pulled, not pushed.** The worker runs `check` at natural checkpoints and once before `worker_done`; if `check` returns `consumer_fenced` it stops without sending `worker_done`. | `source.md:80` | unmatched (best T1 0.2222) |
| INF-024 | WC-13 \| **No Orca fan-out from the worker session.** The worker's top-level session never calls `worker-start`, `dispatch` or `task-create`, Orca's low-level dispatch, or `orca-cli` `worktree create --agent` or `agent launch`, at any depth setting. | `source.md:81` | matched T7 (0.7391) |
| INF-025 | For each Task the coordinator's brief states: the exact command line, including `--unattended` where the command accepts it at this phase, and every flag section 3 lists as required, written as a `Command:` line in the layout below; the report directory, unique to this Task, so the contract path is known before dispatch (WC-4, WC-11); the blocked-gate policy line, `On a blocked gate: report blocked` or `On a blocked gate: ask the coordinator` (WC-3); whether the end-of-Task local commit is authorized, quoting the user's instruction word for word (D4); at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5) | `source.md:84` | unmatched (best T2 0.5439) |
| INF-026 | **Brief layout.** The brief puts the preamble-facing instructions and the guard line before the commands, and gives each command its own labelled `Command:` line in run order (for example `Command: /sc:load ...`, then the converted command), so the Task text never starts with `/sc:`. | `source.md:86` | unmatched (best T2 0.5417) |
| INF-027 | Guard line: `Guard: before running anything, check every Command: line below under the brief guard in ~/.claude/WORKER-CONTRACT.md; on a refusal run nothing and send worker_done --outcome failed with a body starting "guard refused:".` | `source.md:86` | unmatched (best T2 0.5) |
| INF-028 | **Feature worktree and child worktrees.** Every worktree is created by Orca at Orca's default location, never with raw `git worktree add` and never under `.dev/worktrees/`. | `source.md:88` | matched T2 (0.7333) |
| INF-029 | **Git and GitHub ownership.** The coordinator performs every git and GitHub outward action, and every install, VM or paid run, in its own conversation, only when the user's instruction names that action, and confirms with the person at the moment of action unless that instruction is in its live conversation (`sk/sc-post-release-protocol/SKILL.md:351`). | `source.md:90` | unmatched (best T2 0.2857) |
| INF-030 | Every such action targets `IronbellyOrg/IronClaude`: never the SuperClaude upstream, and never through Orca's issue or PR linking while Orca records the project as the upstream. | `source.md:90` | unmatched (best T4 0.3125) |
| INF-031 | Before any push that would publish worker commits the person has not seen, the coordinator shows them to the person and pushes only on the person's go; no earlier pre-authorization waives this. | `source.md:90` | unmatched (best T4 0.35) |
| INF-032 | **Reading a result before anything depends on it.** Orca settles a Task on any valid `worker_done` (`CAPS:77`) and does not start ready Tasks itself (`CAPS:92`), so the coordinator decides what runs next: | `source.md:92` | unmatched (best T2 0.4583) |
| INF-033 | `partial`: dependents do not start until the coordinator has read the contract's `report_path` and recorded, in its own run notes, whether the partial deliverable is usable; an unusable one is handled like `failed`. | `source.md:94` | unmatched (best T5 0.35) |
| INF-034 | `failed` or `blocked`: dependents do not start; the coordinator retries per WC-6, answers per the example below, or reports the failure to the person. | `source.md:95` | unmatched (best T2 0.2308) |
| INF-035 | No contract, and a `worker_done --outcome failed` body that starts `guard refused:`: a brief-guard refusal; nothing ran. The coordinator fixes the brief in a new Task (WC-6), never re-creates it unchanged, and allows at most 2 brief fixes for the same work (3 attempts); a third refusal escalates to the person. | `source.md:96` | unmatched (best T1 0.3939) |
| INF-036 | Every dependent Task is created only after all its inputs have settled and been admitted under the bullets above, with `--deps` naming the Tasks that actually succeeded (an original Task or its replacement). | `source.md:97` | unmatched (best T2 0.3889) |
| INF-037 | The coordinator starts only Tasks it created itself. A ready Task it did not create is not started; it is reported to the person with its spec text. | `source.md:98` | unmatched (best T5 0.5294) |
| INF-038 | *Freeze.* A plan is frozen when its latest implement contract is `blocked`, or `failed` with any STOP code other than `E-RESUME-NEEDED`. | `source.md:101` | unmatched (best T1 0.2857) |
| INF-039 | *Lifting the freeze.* The freeze lifts only when the person's explicit hand-back is recorded in the coordinator's run notes **and** the ledger shows the matching state: | `source.md:107` | unmatched (best T6 0.4) |
| INF-040 | *Check before a resume Task under (c).* The coordinator reads the ledger and the worktree, never edits either, and dispatches only if all of the following hold. | `source.md:112` | unmatched (best T2 0.4) |
| INF-041 | *Placement.* The resume Task starts in the halted worktree by selector (`worker-start --worktree path:<absolute worktree path>`), never in a new or child worktree. | `source.md:120` | unmatched (best T2 0.4615) |
| INF-042 | The coordinator plans N no larger than the merge command's maximum of 10 inputs (`cmd/adversarial.md:15`); a re-run replaces its input rather than adding one, so the admitted count never exceeds 10. Create the merge Task only when at least 2 inputs are admitted, and list every dropped input and its reason in its brief. | `source.md:122` | unmatched (best T2 0.4118) |
| INF-043 | These run as workers now only if the brief uses the stated flags and avoids the inputs that trigger a gate; the worker reports the named file until Phase 1 adds the contract. | `source.md:137` | unmatched (best T1 0.4286) |
| INF-044 | Fix its own contract filename to `<output>/adversarial/return-contract.yaml` (P1); the worker contract is `<output>/return-contract.yaml` and lists that file in `artifacts` (WC-4) | `source.md:141` | matched T1 (0.6429); deferred to later phase plan |
| INF-045 | Under `--unattended`, make `--remediate` follow the existing headless auto-accept rule instead of the `[yes / no]` prompt (P2) | `source.md:148` | unmatched (best T4 0.3846); deferred to later phase plan |
| INF-046 | on `E-HALT-QA` or `E-NO-RULING`, stop with the halt recorded in the ledger and the contract as blocked, carrying the Ruling question, the STOP code in `reason` | `source.md:169` | unmatched (best T5 0.2308); deferred to later phase plan |
| INF-047 | the "Resume? [Y/n]" prompt is replaced by the explicit resume flag (resume only when passed); `--interactive` refused | `source.md:178` | unmatched (best T6 0.3636); deferred to later phase plan |
| INF-048 | Without `--unattended`, every prompt, approval gate, default flag value, output path and outward default stays as it is today, including the auggie-review PR posting default and every `AskUserQuestion`. | `source.md:208` | unmatched (best T1 0.2632) |
| INF-049 | No command, skill or agent file runs an `orca` or `orca-ide` command, and none requires Orca to be installed or running. | `source.md:209` | unmatched (best T1 0.4167) |
| INF-050 | The new contract file and report files are written only in unattended mode or when the caller passes the new output flag. | `source.md:210` | matched T1 (0.8462); deferred to later phase plan |
| INF-051 | Command-file edits in Phases 1-3 are additive: a new `## Unattended mode` section and new flags. | `source.md:211` | unmatched (best T4 0.4); deferred to later phase plan |
| INF-052 | `src/superclaude/` stays the source of truth; `.claude/` copies come from `make sync-dev` and are never staged. The routing guide gains an Orca section without changing any existing routing row, and its two mirrored copies are updated as the repo requires. | `source.md:212` | unmatched (best T4 0.5926) |
| INF-053 | The existing headless rule of `/sc:reflect` under `claude --print` keeps working exactly as today; `--unattended` reuses it and does not replace it. | `source.md:213` | unmatched (best T1 0.375); deferred to later phase plan |
| INF-054 | Each phase is independently useful and leaves standalone behaviour unchanged (section 5). Later phases do not start until the earlier phase's checks in section 7 pass. | `source.md:216` | unmatched (best T6 0.3684) |
| INF-055 | Write `src/superclaude/core/WORKER-CONTRACT.md` (the contents section 2.1 assigns to it, plus a coordinator brief template listing the section 3.1 flags), add it to `KNOWN_CORE_FILES`, add an Orca section to `HOW-WE-WORK.md` and its two mirrored copies, and add the static test file `tests/skills/test_worker_contract.py` (proposed name). Then run three ready commands as real Orca workers, invoked directly, to close evidence gap 1.4 (1), and confirm the two Orca behaviours later checks rely on (AC-0.5, AC-0.6). | `source.md:220` | unmatched (best T1 0.434) |
| INF-056 | The WC-4 contract, the report-directory rule, the flag parse rule and the person-mode refusal (section 2.1) for the P1 commands only; `--unattended` is added to a command only in the phase that converts its gates, so no command accepts the flag while it can still prompt; output flags for commands that lack one; the small fixes to ready commands. | `source.md:221` | matched T1 (0.625); deferred to later phase plan |
| INF-057 | Each default-on gate resolves per its section 3 row; WC-10 wait splitting for cli-eval. | `source.md:222` | unmatched (best T1 0.4167); deferred to later phase plan |
| INF-058 | Reconcile command and skill where they disagree; make memory writes parallel-safe. | `source.md:223` | unmatched (best T6 0.3); deferred to later phase plan |
| INF-059 | Apply the approved D2-D4 outcomes: the implement halt path, post-release with every outward step off (D4), pr-submit as a worker only if D3 (b) is chosen. | `source.md:224` | unmatched (best T2 0.2778); deferred to later phase plan |
| INF-060 | none (smoke runs use each command's existing flags) | `source.md:230` | unmatched (best T2 0.375) |
| INF-061 | Each phase is one written plan executed under the repo's level-3 route (`/sc:workflow`, then `/sc:implement` when execution is requested), because each touches more than one source file (hard limit at `src/superclaude/core/CLAUDE.md:66` and `src/superclaude/core/HOW-WE-WORK.md:22`). | `source.md:238` | unmatched (best T1 0.4074) |
| INF-062 | **AC-C1** (SA-2, WC-8). Pass: prints nothing. | `source.md:244` | matched T8 (0.6667) |
| INF-063 | **AC-C2** (SA-5). Pass: exits 0. | `source.md:256` | matched T4 (0.8) |
| INF-064 | **AC-C3**. Before the phase starts, save the output below as the baseline; after the phase, run it again. | `source.md:261` | matched T1 (0.7778) |
| INF-065 | **AC-C4** (`CLAUDE.md:16`). Pass: prints nothing. | `source.md:266` | matched T8 (0.6667) |
| INF-066 | **AC-C5** (SA-4: edits are additive). Run for every command file the phase edits without a named defect fix. | `source.md:271` | unmatched (best T8 0.5) |
| INF-067 | **AC-C6** (D5, non-goal 2). Pass: prints exactly one line per Orca profile and every line is `"nestedWorkerMaxDepth":1`. | `source.md:276` | unmatched (best T7 0.5714) |
| INF-068 | For each command under test, the coordinator runs the steps below with one worker in a fresh disposable worktree that holds the phase's edits, so step 6 can attribute every change to the worker under test (WC-11 allows sharing a worktree in normal use; the check does not). | `source.md:282` | unmatched (best T8 0.3846); deferred to P0 live plan |
| INF-069 | AC-0.1 \| `uv run python -c "from superclaude.cli.install_core import KNOWN_CORE_FILES; assert 'WORKER-CONTRACT.md' in KNOWN_CORE_FILES"`, then the install check in the block below the table, then `uv run pytest tests/skills/test_worker_contract.py -q`, which asserts the file states each rule section 2.1 assigns to it and the section 2.3 dependent-creation and fan-in rules | `source.md:298` | matched T1 (0.7273) |
| INF-070 | AC-0.2 \| `cmp src/superclaude/core/HOW-WE-WORK.md plugins/superclaude/skills/sc-recommend/refs/HOW-WE-WORK.md` and the level-table test the repo already runs (`CLAUDE.md:334`) \| identical; tests pass | `source.md:299` | matched T4 (0.7) |
| INF-071 | AC-0.3 \| The deletions check in the block below the table, on `src/superclaude/core/HOW-WE-WORK.md` \| prints nothing: no existing routing line removed (SA-5) | `source.md:300` | matched T4 (0.7647) |
| INF-072 | 7.2 live check on `/sc:troubleshoot "<real symptom>" --output-dir <dir>` (no `--fix`, no `--depth deep`), `/sc:workflow "<small change>" --handoff none`, `/sc:adversarial --compare <two files> --depth quick --output <dir>`, each run directly by the worker (no Agent-tool wrapper, verified in the step-5 transcript) \| steps 1-7 pass. | `source.md:301` | unmatched (best T2 0.2778); deferred to P0 live plan |
| INF-073 | AC-0.5 \| WC-1: `worker-start` with the user's normal launch setup (the same shell wrapper, hooks and startup command a person's sessions use), timed \| exit 0, `state: ready`, and the start returns in under 45 s. | `source.md:302` | unmatched (best T6 0.16); deferred to P0 live plan |
| INF-074 | AC-0.6 \| Read one AC-0.4 transcript with `worker-read --source transcript --json` and record whether tool calls appear by name (for example `Bash`, `Agent`, `AskUserQuestion`) | `source.md:303` | unmatched (best T1 0.2941); deferred to P0 live plan |
| INF-075 | AC-0.7 \| Read-only trace in Orca's installed code, starting from the AC-0.7 block below the table, of (1) which calls check nesting depth: `worker-start`, `dispatch`, `task-create`, low-level dispatch, `worktree create --agent`, `agent launch`; and (2) what depth Orca gives a session the person opens (expected 0, `CAPS:97`). | `source.md:304` | matched T7 (0.9118) |
| INF-076 | AC-0.9 \| Write-verb audit: `test_worker_contract.py` scans the skills, commands and agents under `src/superclaude/` (the installed primitives' source) for git and gh write verbs (`add`, `commit`, `push`, `merge`, `worktree add/remove`, `stash`, `update-ref`, `gh pr`, `gh api` posts) | `source.md:305` | matched T6 (0.8929) |
| INF-077 | The test also asserts that `WORKER-CONTRACT.md` states the brief guard (its four refusal conditions, the three exact reason texts, and the `guard refused:` prefix for case 3), the never-as-worker list and the nested propagation rule | `source.md:306` | matched T1 (0.9167); deferred to later phase plan |
| INF-078 | AC-1.2 \| 7.2 live check on each P1 command with `--unattended` and its report directory (`--output <dir>` or `--report-dir <dir>`) | `source.md:307` | matched T1 (0.6429); deferred to later phase plan |
| INF-079 | AC-1.3 \| For two P1 commands, run once with no `--unattended` and no new output flag, then `git status --short`. | `source.md:308` | matched T1 (0.7143); deferred to later phase plan |
| INF-080 | AC-1.4 \| `grep -n 'return-contract.yaml' src/superclaude/skills/sc-adversarial-protocol/SKILL.md` and the workflow return-contract ref | `source.md:309` | unmatched (best T8 0.3333); deferred to later phase plan |
| INF-081 | AC-1.5 \| WC-4 missing report directory: `/sc:analyze src/ --unattended` with neither `--output` nor `--report-dir`, as a 7.2 live check whose steps 3-4 are replaced by this row's conditions | `source.md:310` | unmatched (best T1 0.4762); deferred to later phase plan |
| INF-082 | AC-1.6 \| Person-mode refusal (section 2.1): `/sc:test --watch --unattended --report-dir <dir>` as a 7.2 live check | `source.md:311` | unmatched (best T1 0.5); deferred to later phase plan |
| INF-083 | AC-1.7 \| Brief-guard refusals (section 2.1), one 7.2 live check per case, with steps 3-4 replaced by this row's conditions. | `source.md:312` | unmatched (best T1 0.4375); deferred to later phase plan |
| INF-084 | AC-1.8 \| WC-9 commit grant: a commit-authorized worker started with `--worktree new-child --base-branch <feature branch>`, with the four records of AC-4.2 taken before dispatch and after the run | `source.md:313` | unmatched (best T1 0.2778); deferred to later phase plan |
| INF-085 | AC-2.1 \| `test_worker_contract.py` gains one assertion per gate listed in the section 3 row, for example the auggie-review section names both `--no-post-pr` and `--no-remediation-offer`; for cli-eval, the eval wait step names a single-wait limit of at most 240 s (WC-10) | `source.md:314` | unmatched (best T5 0.2692); deferred to later phase plan |
| INF-086 | AC-2.2 \| Gate-trigger run per P2 command: a 7.2 live check whose brief carries `On a blocked gate: report blocked` and input that hits the gate (for example `/sc:tdd "auth" --unattended --output <file> --report-dir <dir>` with a bare topic; `/sc:cli-eval run --unattended --report-dir <dir>` with no `--suite`). | `source.md:315` | unmatched (best T2 0.3667); deferred to later phase plan |
| INF-087 | AC-2.3 \| Happy-path run per P2 command with every required flag in the brief \| 7.2 passes with `--outcome succeeded` | `source.md:316` | unmatched (best T1 0.4615); deferred to later phase plan |
| INF-088 | AC-2.4 \| `/sc:auggie-review <PR> --unattended --output-dir <dir>` on a fork PR; before and after, `gh api repos/IronbellyOrg/IronClaude/pulls/<PR>/reviews --jq length` and `.../pulls/<PR>/comments --jq length` | `source.md:317` | unmatched (best T6 0.2778); deferred to later phase plan |
| INF-089 | AC-2.5 \| A person runs `/sc:cli-eval run` and `/sc:cleanup <dir> --interactive` in a plain session (manual check) | `source.md:318` | unmatched (best T4 0.3077); deferred to later phase plan |
| INF-090 | AC-2.6 \| WC-3 and WC-6, the section 2.3 worked example run live: T1 hits the tdd gate and reports blocked; the coordinator creates T2 with the answer and new directories; then a third Task T3 with the same bare-topic input and `On a blocked gate: ask the coordinator`, where the coordinator answers the `ask`. | `source.md:319` | unmatched (best T2 0.2667); deferred to later phase plan |
| INF-091 | AC-2.9 \| Brief guard, discriminating run: `/sc:tdd "auth" --output <file> --report-dir <dir>` (bare topic, no `--unattended`) as a 7.2 live check, with steps 3-4 replaced by this row's conditions | `source.md:320` | unmatched (best T1 0.44); deferred to later phase plan |
| INF-092 | AC-2.8 \| `--unattended` parse rule (section 2.1): `/sc:troubleshoot "the worker ignores --unattended"` run by a person in a plain session (manual check) | `source.md:321` | unmatched (best T1 0.5); deferred to later phase plan |
| INF-093 | AC-3.1 \| `test_worker_contract.py` asserts that `cmd/validate-roadmap.md` and `sk/sc-validate-roadmap-protocol/SKILL.md` name the same report filename | `source.md:322` | unmatched (best T1 0.25); deferred to later phase plan |
| INF-094 | AC-3.2 \| `/sc:roadmap <spec> --unattended --output <dir>` with an existing `<dir>/.session-memory.md` and no resume flag \| starts fresh, no `[Y/n]` in the transcript, contract written | `source.md:323` | unmatched (best T1 0.3684); deferred to later phase plan |
| INF-095 | AC-3.3 \| `test -d` on the default target in `cmd/validate-tests.md`; `/sc:validate-tests --report <path> --unattended --report-dir <dir>` | `source.md:324` | unmatched (best T1 0.2857); deferred to later phase plan |
| INF-096 | AC-3.4 \| Two workers in one worktree each run `/sc:save --unattended --report-dir <own dir>` | `source.md:325` | matched T1 (0.6923); deferred to later phase plan |
| INF-097 | AC-4.1 \| `/sc:implement <plan> --unattended --report-dir <dir>` with the brief line `On a blocked gate: ask the coordinator` (the policy most likely to relay a Ruling), on a plan with one acceptance criterion that cannot be met | `source.md:326` | unmatched (best T2 0.3478); deferred to later phase plan |
| INF-098 | AC-4.2 \| `/sc:post-release <version> --unattended --output <dir>` with no authorization flags | `source.md:327` | unmatched (best T1 0.4); deferred to later phase plan |
| INF-099 | AC-4.3 \| If D3 allows pr-submit as a worker: one 7.2 run on a scratch fork PR; `worker-read` transcript inspected for Bash waits | `source.md:328` | unmatched (best T1 0.25); deferred to later phase plan |
| INF-100 | AC-4.4 \| (1) Before the coordinator ever launches a pr-submit session: on each Chat UI setting the user uses (chat, terminal) | `source.md:329` | unmatched (best T2 0.2857); deferred to later phase plan |
| INF-101 | AC-4.5 \| Two workers in one feature: one `/sc:implement` task whose rollback is forced, in a child worktree, and one report-only worker in the parent | `source.md:330` | unmatched (best T2 0.375); deferred to later phase plan |
| INF-102 | Before P1, when no command writes a contract, a brief that states the AC-0.4 report file and outcome rule replaces this mapping for that Task. | `source.md:73` | matched T1 (0.9375) |
| INF-103 | at P0 only, the command's report file and the outcome rule AC-0.4 gives for it (WC-5) | `source.md:84` | matched T2 (1.0) |
| INF-104 | The static plan holds the edits and the checks that need no live Orca run. The live plan holds the 7.2 live checks and the phase report. | `source.md:238` | matched T8 (0.7692) |
| INF-105 | The `--outcome` is `failed` when the file is missing or empty, or its status is `failed` or `blocked`; otherwise it is `succeeded`. | `source.md:301` | unmatched (best T1 0.4545); deferred to P0 live plan |

Postscript: 42 of the 105 rows were in the re-Read sample. 42 quotes matched their cited lines and 0 rows were dropped. `coverage_pct_union` (0.2762), `unmapped_requirements_union` and `S_dev_density` (0.7238) need no recompute.

## Inferred-claim audit

- `citations_inferred: 0`
- Inferred-fraction: `0 / 182` = 0.00

## Recommendations

### Recommendation R-001: Fix M-01 in Task 4

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Reword TL:21: P0 edits no command file, no SKILL.md and no agent file; the only file written under a skills directory is the byte-for-byte copy of HOW-WE-WORK.md in plugins/superclaude/skills/sc-recommend/refs/ that Task 4 makes.
- **Verifier:** re-Read the edited plan lines against TL:21, TL:24, TL:90, TL:93, SRC:220, qa.md:52, qa.md:61, qa.md:310, qa.md:286, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-01 is not raised again.
- **Linked deviation(s):** D-001
- **Priority:** P0

### Recommendation R-016: Fix M-16 in Task 1, Task 4

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** In TL:35 and TL:95 state that pre-existing failures are expected, list the 8 failing test ids as the accepted baseline, and cite the per-test comparison file rather than the raw log.
- **Verifier:** re-Read the edited plan lines against TL:35, TL:48, TL:95, qa.md:310, qa.md:294, qa.md:286, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-16 is not raised again.
- **Linked deviation(s):** D-016
- **Priority:** P0

### Recommendation R-002: Fix M-02 in Task 1, Task 2

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Add a Constraints line: WORKER-CONTRACT.md and the HOW-WE-WORK.md section use installed ~/.claude/ paths only and copy no CAPS:/INV- ids or src/superclaude/ paths.
- **Verifier:** re-Read the edited plan lines against TL:17-27, TL:22, TL:37, SRC:59, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-02 is not raised again.
- **Linked deviation(s):** D-002
- **Priority:** P1

### Recommendation R-003: Fix M-03 in Task 6

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Replace TL:125's two-way rule with five categories (WC-9 allowed; refused or deferred in a named phase; never a worker; no command converts this file; read-only or false match), key by path, verb and stripped line text, scan with word boundaries; ship with M-18.
- **Verifier:** re-Read the edited plan lines against TL:125, SRC:61, SRC:201, SRC:224, SRC:305, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-03 is not raised again.
- **Linked deviation(s):** D-003
- **Priority:** P1

### Recommendation R-004: Fix M-04 in Task 2

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Add to TL:22: plus, in the brief template only, the section 3.1 Brief-must-pass flags and the section 6 phase markers (--report-dir from P1).
- **Verifier:** re-Read the edited plan lines against TL:22, TL:58, SRC:59, SRC:84, SRC:220, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-04 is not raised again.
- **Linked deviation(s):** D-004
- **Priority:** P1

### Recommendation R-005: Fix M-05 in Task 1, Task 2, Task 5

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Use the spec's 'maximum of 10 inputs' / 'never exceeds 10' in TL:56 and TL:112 and drop '(as written in section 2.3)'; Tasks 1-2 record the phrase each rule is tested on, worded per M-19.
- **Verifier:** re-Read the edited plan lines against TL:56, TL:104, TL:112, SRC:122, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-05 is not raised again.
- **Linked deviation(s):** D-005
- **Priority:** P1

### Recommendation R-006: Fix M-06 in Task 1, Task 3, Task 4, Task 8

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** In Task 8, re-run AC-0.1, AC-0.2, AC-0.3, AC-C1 and AC-C2 and save each output to ./artifacts/<id>.txt as the report's evidence.
- **Verifier:** re-Read the edited plan lines against TL:47, TL:72, TL:93-94, TL:147-152, TL:157, qa.md:85, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-06 is not raised again.
- **Linked deviation(s):** D-006
- **Priority:** P1

### Recommendation R-007: Fix M-07 in Task 3, Task 5

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** If Task 3 adds the copy, Task 5 asserts it is byte-identical to the src file (pattern: test_plugin_mirror_matches_src).
- **Verifier:** re-Read the edited plan lines against TL:69, TL:74, qa.md:310, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-07 is not raised again.
- **Linked deviation(s):** D-007
- **Priority:** P1

### Recommendation R-008: Fix M-08 in Task 4

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Add to Task 4: the new section is ASCII only and is a new top-level section after the last one, outside the level-table and routing markers.
- **Verifier:** re-Read the edited plan lines against TL:90, TL:93, tests/core/test_how_we_work_routing_table.py:341, tests/core/test_how_we_work_routing_table.py:819, tests/core/test_how_we_work_routing_table.py:1091, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-08 is not raised again.
- **Linked deviation(s):** D-008
- **Priority:** P1

### Recommendation R-017: Fix M-17 in Task 1, Task 4, Task 8

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Add --deselect tests/cli/eval/test_perf_home_setup.py to the wider runs, or git restore .dev/releases/current/cliEval/evidence/T02.15/perf.json after each run.
- **Verifier:** re-Read the edited plan lines against TL:35, TL:95, TL:154, qa.md:51, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-17 is not raised again.
- **Linked deviation(s):** D-017
- **Priority:** P1

### Recommendation R-018: Fix M-18 in Task 6

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Define a gh api post as a gh api call whose method is not GET; ship with M-03.
- **Verifier:** re-Read the edited plan lines against TL:125, SRC:305, qa.md:50, qa.md:52, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-18 is not raised again.
- **Linked deviation(s):** D-018
- **Priority:** P1

### Recommendation R-019: Fix M-19 in Task 1, Task 2, Task 5

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Say 'a phrase', exempt the worker-session duties from verbatim copying, and name the phrase to pin for WC-12, WC-13 and heartbeats.
- **Verifier:** re-Read the edited plan lines against TL:22, TL:46, TL:104-105, SRC:59, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-19 is not raised again.
- **Linked deviation(s):** D-019
- **Priority:** P1

### Recommendation R-009: Fix M-09 in Task 3

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Name build-script line 75, the parity test, the one test that reads a plugin core copy, and SRC:252's by-name exclusion in Task 3.
- **Verifier:** re-Read the edited plan lines against TL:69, SRC:252, scripts/build_superclaude_plugin.py:75, tests/commands/test_routing_plugin_parity.py:3, tests/commands/test_impact_command.py:309, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-09 is not raised again.
- **Linked deviation(s):** D-009
- **Priority:** P2

### Recommendation R-010: Fix M-10 in Task 0

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Delete the AC-0.8 sentence or replace it with 'the P1 checks are AC-1.1 to AC-1.8 (section 7.3)'.
- **Verifier:** re-Read the edited plan lines against TL:19, SRC:304-306, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-10 is not raised again.
- **Linked deviation(s):** D-010
- **Priority:** P2

### Recommendation R-011: Fix M-11 in Task 8

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** End the static report with a 'results the P0 live plan must cite' list and add the coordinator's re-staging of .dev/tasks and AC-C4 re-run to the next steps.
- **Verifier:** re-Read the edited plan lines against TL:19, TL:154, SRC:238, SRC:303-304, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-11 is not raised again.
- **Linked deviation(s):** D-011
- **Priority:** P2

### Recommendation R-012: Fix M-12 in Task 5

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Write it as a cumulative per-phase map, {'P0': set()}; optionally also assert at least 45 command files were scanned (INV-011).
- **Verifier:** re-Read the edited plan lines against TL:115, SRC:306, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-12 is not raised again.
- **Linked deviation(s):** D-012
- **Priority:** P2

### Recommendation R-013: Fix M-13 in Task 2, Task 5

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** In Task 5, assert each template flag exists in its command file, except the flags marked 'from P1'.
- **Verifier:** re-Read the edited plan lines against TL:58, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-13 is not raised again.
- **Linked deviation(s):** D-013
- **Priority:** P2

### Recommendation R-014: Fix M-14 in Task 4

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** Reword the Goal: the Orca section is in HOW-WE-WORK.md and its plugin copy; the CLAUDE.md level-table copy is unchanged.
- **Verifier:** re-Read the edited plan lines against TL:15, TL:90, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-14 is not raised again.
- **Linked deviation(s):** D-014
- **Priority:** P2

### Recommendation R-015: Fix M-15 in Task 1, Task 4

- **File:** .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261103-012232/TASK-WF-orcaWorkerContra-20261103-012232.md
- **Change:** In Task 1 also save make verify-sync output, and add tests/docs and tests/unit to the wider baseline and Task 4's comparison.
- **Verifier:** re-Read the edited plan lines against TL:33-35, TL:96, then re-run the `/sc:workflow` pre-review on the revised plan and confirm M-15 is not raised again.
- **Linked deviation(s):** D-015
- **Priority:** P2
